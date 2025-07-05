package main

import (
	"bytes"
	"crypto/md5"
	"encoding/binary"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/asticode/go-astisub"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
	"github.com/go-audio/audio"
	"github.com/go-audio/wav"
	"github.com/spf13/cobra"
)

type Config struct {
	VTTFile       string
	DefaultVoice  string
	APIKeyFile    string
	TempDir       string
	OutputFile    string
	Limit         int
	Padding       time.Duration
	VoiceMappings map[string]string
	DryRun        bool
	S3Bucket      string  // New S3 bucket parameter
	OutputFormat  string  // New parameter for output format
	AutoPad       bool    // Automatically add sufficient padding
	AutoSpeed     bool    // Automatically speed up segments that are too long
	Speed         float64 // Default speed for all segments
}

// PCMAudio represents decoded PCM audio data
type PCMAudio struct {
	Data       []float64
	SampleRate int
}

type AudioSegment struct {
	Path      string
	StartTime time.Duration
	EndTime   time.Duration
	Text      string
	Checksum  string  // Added checksum field
	Speed     float64 // Speed factor for this segment (default 1.0)
}

// VoiceSettings represents the voice settings for ElevenLabs TTS.
type VoiceSettings struct {
	Speed float64 `json:"speed,omitempty"`
}

// TTSRequest is our request body for ElevenLabs TTS conversion.
type TTSRequest struct {
	Text          string         `json:"text"`
	ModelID       string         `json:"model_id"`
	PreviousText  string         `json:"previous_text,omitempty"`
	NextText      string         `json:"next_text,omitempty"`
	VoiceSettings *VoiceSettings `json:"voice_settings,omitempty"`
	OutputFormat  string         `json:"output_format,omitempty"` // This is a query param, not in the JSON. It shouldn't be here.
}

// rawPCMToPCMAudio converts a raw PCM byte slice (16-bit, little-endian) into a PCMAudio struct.
func rawPCMToPCMAudio(raw []byte, sampleRate int) (*PCMAudio, error) {
	if len(raw)%2 != 0 {
		return nil, fmt.Errorf("raw PCM data length is not even")
	}
	numSamples := len(raw) / 2
	data := make([]float64, numSamples)
	for i := 0; i < numSamples; i++ {
		// Read 2 bytes as little-endian int16.
		sample := int16(binary.LittleEndian.Uint16(raw[i*2 : i*2+2]))
		data[i] = float64(sample) / 32768.0
	}
	return &PCMAudio{
		Data:       data,
		SampleRate: sampleRate,
	}, nil
}

const (
	silenceThreshold  = 0.001 // Adjust this value based on testing
	minSilenceSamples = 100   // Minimum number of samples to consider as silence
)

// Now we'll change how we handle mixing audio since we're working with PCM files
func loadPCMAudio(filePath string) (*PCMAudio, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open audio file %s: %v", filePath, err)
	}
	defer file.Close()

	decoder := wav.NewDecoder(file)
	buffer, err := decoder.FullPCMBuffer()
	if err != nil {
		return nil, fmt.Errorf("failed to decode WAV file %s: %v", filePath, err)
	}

	// Convert int samples to float64
	data := make([]float64, len(buffer.Data))
	for i, sample := range buffer.Data {
		data[i] = float64(sample) / 32768.0
	}

	return &PCMAudio{
		Data:       data,
		SampleRate: buffer.Format.SampleRate,
	}, nil
}

func trimEndSilence(pcm *PCMAudio) *PCMAudio {
	// Start from the end and find the last non-silent sample
	lastNonSilent := len(pcm.Data) - 1
	silenceCount := 0

	for i := len(pcm.Data) - 1; i >= 0; i-- {
		if abs(pcm.Data[i]) > silenceThreshold {
			// If we haven't accumulated enough silence samples, don't trim
			if silenceCount < minSilenceSamples {
				lastNonSilent = len(pcm.Data) - 1
			}
			break
		}
		silenceCount++
		lastNonSilent = i - 1
	}

	// If we found silence at the end, create new trimmed PCM data
	if lastNonSilent < len(pcm.Data)-1 {
		return &PCMAudio{
			Data:       pcm.Data[:lastNonSilent+1],
			SampleRate: pcm.SampleRate,
		}
	}

	return pcm
}

type SegmentInfo struct {
	Path         string
	VTTStartTime time.Duration
	VTTEndTime   time.Duration
	PCMData      *PCMAudio
	RenderStart  int // in samples
	RenderEnd    int // in samples
	Text         string
	Speed        float64 // Speed factor
}

// calculateRequiredPadding simulates the mixing process to determine how much padding is needed
func calculateRequiredPadding(segments []AudioSegment, totalDuration time.Duration, sampleRate int) (time.Duration, error) {
	// Load and decode all segments first
	segInfos := make([]SegmentInfo, len(segments))
	for i, segment := range segments {
		pcm, err := loadPCMAudio(segment.Path)
		if err != nil {
			return 0, fmt.Errorf("failed to decode WAV file %s: %v", segment.Path, err)
		}

		pcm = trimEndSilence(pcm)

		segInfos[i] = SegmentInfo{
			Path:         segment.Path,
			VTTStartTime: segment.StartTime,
			VTTEndTime:   segment.EndTime,
			PCMData:      pcm,
			RenderStart:  -1,
			RenderEnd:    -1,
			Text:         segment.Text,
			Speed:        segment.Speed,
		}
	}

	// Track the last rendered end position in samples
	var lastRenderedEnd int = 0

	// Simulate mixing segments to determine the total required length
	for i, segInfo := range segInfos {
		desiredStart := int(segInfo.VTTStartTime.Seconds() * float64(sampleRate))
		actualStart := desiredStart

		// If this segment would overlap with the previous one
		if actualStart < lastRenderedEnd {
			var vttGap time.Duration
			if i > 0 {
				vttGap = segInfo.VTTStartTime - segInfos[i-1].VTTEndTime
			}

			var delay float64
			if vttGap > 0 {
				delay = vttGap.Seconds() / 5
			}

			actualStart = lastRenderedEnd + int(delay*float64(sampleRate))
		}

		// Update segment info with actual render positions
		segInfos[i].RenderStart = actualStart
		segInfos[i].RenderEnd = actualStart + len(segInfo.PCMData.Data)
		lastRenderedEnd = segInfos[i].RenderEnd
	}

	// Calculate required duration in seconds
	requiredSamples := lastRenderedEnd
	requiredDuration := time.Duration(float64(requiredSamples) / float64(sampleRate) * float64(time.Second))

	// Calculate how much extra padding we need beyond the VTT duration
	extraPadding := requiredDuration - totalDuration
	if extraPadding < 0 {
		extraPadding = 0
	}

	// Add a small buffer to ensure we have enough padding (extra 0.5 seconds)
	return extraPadding + 500*time.Millisecond, nil
}

func mixAudio(segments []AudioSegment, totalDuration time.Duration, sampleRate int, padding time.Duration, autoSpeed bool) (*PCMAudio, error) {
	// Calculate total samples needed (including padding)
	totalSamples := int((totalDuration + padding).Seconds() * float64(sampleRate))
	mixedData := make([]float64, totalSamples)

	// Load and decode all segments first
	segInfos := make([]SegmentInfo, len(segments))
	for i, segment := range segments {
		// Read and decode WAV file instead of MP3
		pcm, err := loadPCMAudio(segment.Path)
		if err != nil {
			return nil, fmt.Errorf("failed to decode WAV file %s: %v", segment.Path, err)
		}

		// Apply trimming to the loaded audio
		pcm = trimEndSilence(pcm)

		segInfos[i] = SegmentInfo{
			Path:         segment.Path,
			VTTStartTime: segment.StartTime,
			VTTEndTime:   segment.EndTime,
			PCMData:      pcm,
			RenderStart:  -1, // Will be set during mixing
			RenderEnd:    -1, // Will be set during mixing
			Text:         segment.Text,
			Speed:        segment.Speed,
		}
	}

	// Track the last rendered end position in samples
	var lastRenderedEnd int = 0

	// Mix segments with collision avoidance
	for i, segInfo := range segInfos {
		// Calculate initial desired start position
		desiredStart := int(segInfo.VTTStartTime.Seconds() * float64(sampleRate))
		actualStart := desiredStart

		// If this segment would overlap with the previous one
		if actualStart < lastRenderedEnd {
			// Calculate the VTT gap between this and previous segment
			var vttGap time.Duration
			if i > 0 {
				vttGap = segInfo.VTTStartTime - segInfos[i-1].VTTEndTime
			}

			// Calculate delay to add (one fifth of the VTT gap, if exists)
			var delay float64
			if vttGap > 0 {
				delay = vttGap.Seconds() / 5
				fmt.Printf("We're running late, so let's put a gap of %v instead of %v\n",
					time.Duration(float64(time.Second)*delay), vttGap)
			}

			// New start position is after the last rendered end plus the calculated delay
			actualStart = lastRenderedEnd + int(delay*float64(sampleRate))
		}

		// Check if we would exceed the buffer
		if actualStart >= len(mixedData) {
			// Calculate the needed padding
			neededPadding := time.Duration(float64(actualStart-len(mixedData)+len(segInfo.PCMData.Data))/float64(sampleRate)*float64(time.Second)) + 500*time.Millisecond
			return nil, fmt.Errorf("segment %d would exceed output duration (even with current padding). "+
				"You need approximately %v of additional padding. Current padding: %v, Total needed: %v",
				i+1, neededPadding, padding, padding+neededPadding)
		}

		// Mix this segment at the calculated position
		endPos := actualStart + len(segInfo.PCMData.Data)
		if endPos > len(mixedData) {
			// Calculate the needed padding
			neededPadding := time.Duration(float64(endPos-len(mixedData))/float64(sampleRate)*float64(time.Second)) + 500*time.Millisecond
			return nil, fmt.Errorf("segment %d exceeds output duration while mixing. "+
				"You need approximately %v of additional padding. Current padding: %v, Total needed: %v",
				i+1, neededPadding, padding, padding+neededPadding)
		}

		for j, sample := range segInfo.PCMData.Data {
			pos := actualStart + j
			mixedData[pos] += sample
		}

		// Update segment info with actual render positions
		segInfos[i].RenderStart = actualStart
		segInfos[i].RenderEnd = actualStart + len(segInfo.PCMData.Data)
		lastRenderedEnd = segInfos[i].RenderEnd

		fmt.Printf("Segment %d (text = %s) was supposed to start at %v/%v-%v.\n", i+1, segInfo.Text, desiredStart, segInfo.VTTStartTime, segInfo.VTTEndTime)

		// Log the timing adjustment if it was needed
		if actualStart != desiredStart {
			delay := time.Duration(float64(actualStart-desiredStart) / float64(sampleRate) * float64(time.Second))
			fmt.Printf("Segment %d delayed by %v to avoid collision\n", i+1, delay)
		}

		requiredDuration := segInfo.VTTEndTime - segInfo.VTTStartTime
		actualDuration := time.Duration(float64(time.Second) * float64(segInfos[i].RenderEnd-segInfos[i].RenderStart) / float64(sampleRate))
		fmt.Printf("So it actually went from  %v - %v (%v) instead of (%v)\n",
			segInfos[i].RenderStart, segInfos[i].RenderEnd, actualDuration, requiredDuration)

		// If using autospeed and the segment is over the required duration, flag it for regeneration
		if autoSpeed && actualDuration > requiredDuration {
			return nil, fmt.Errorf("segment %d duration %v exceeds required duration %v; needs to be regenerated with autospeed",
				i+1, actualDuration, requiredDuration)
		}
	}

	// Normalize the mixed audio to prevent clipping
	maxAmp := 0.0
	for _, sample := range mixedData {
		if abs(sample) > maxAmp {
			maxAmp = abs(sample)
		}
	}

	if maxAmp > 1.0 {
		for i := range mixedData {
			mixedData[i] /= maxAmp
		}
	}

	return &PCMAudio{
		Data:       mixedData,
		SampleRate: sampleRate,
	}, nil
}

func abs(x float64) float64 {
	if x < 0 {
		return -x
	}
	return x
}

func saveToWAV(pcm *PCMAudio, outputPath string) error {
	outFile, err := os.Create(outputPath)
	if err != nil {
		return fmt.Errorf("failed to create output file: %v", err)
	}
	defer outFile.Close()

	// Create WAV encoder
	enc := wav.NewEncoder(outFile, pcm.SampleRate, 16, 1, 1)
	defer enc.Close()

	// Convert float64 samples to int
	buf := &audio.IntBuffer{
		Format: &audio.Format{
			NumChannels: 1,
			SampleRate:  pcm.SampleRate,
		},
		Data: make([]int, len(pcm.Data)),
	}

	for i, sample := range pcm.Data {
		buf.Data[i] = int(sample * 32767.0)
	}

	// Write the buffer
	if err := enc.Write(buf); err != nil {
		return fmt.Errorf("failed to write audio data: %v", err)
	}

	return nil
}

// Calculate checksum for audio segment
func calculateChecksum(text, prevText, nextText, voiceID string, speed float64) string {
	h := md5.New()
	io.WriteString(h, text)
	io.WriteString(h, prevText)
	io.WriteString(h, nextText)
	io.WriteString(h, voiceID)
	io.WriteString(h, fmt.Sprintf("%.2f", speed)) // Include speed in checksum
	return hex.EncodeToString(h.Sum(nil))
}

// textToSpeech makes a POST request to ElevenLabs TTS API.
func textToSpeech(apiKey, voiceID string, req TTSRequest) ([]byte, error) {
	url := fmt.Sprintf("https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=%s", voiceID, req.OutputFormat)

	payload, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %v", err)
	}

	client := &http.Client{Timeout: 3600 * time.Second}
	httpReq, err := http.NewRequest("POST", url, bytes.NewReader(payload))
	if err != nil {
		return nil, fmt.Errorf("failed to create HTTP request: %v", err)
	}

	httpReq.Header.Set("xi-api-key", apiKey)
	httpReq.Header.Set("Content-Type", "application/json")
	httpReq.Header.Set("Accept", "audio/pcm") // Only accept wav files

	resp, err := client.Do(httpReq)
	if err != nil {
		return nil, fmt.Errorf("failed to make HTTP request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("non-200 response: %d - %s", resp.StatusCode, string(body))
	}

	audioData, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body: %v", err)
	}

	return audioData, nil
}

// Helper function to print segment information in a readable format
func printSegmentInfo(segments []AudioSegment) {
	fmt.Println("\n=== SEGMENTS INFORMATION ===")
	fmt.Printf("Total segments: %d\n\n", len(segments))

	for i, segment := range segments {
		fmt.Printf("Segment #%d:\n", i+1)
		fmt.Printf("  Path: %s\n", segment.Path)
		fmt.Printf("  Checksum: %s\n", segment.Checksum)
		fmt.Printf("  Start Time: %v\n", segment.StartTime)
		fmt.Printf("  End Time: %v\n", segment.EndTime)
		fmt.Printf("  Duration: %v\n", segment.EndTime-segment.StartTime)
		if segment.Speed != 1.0 {
			fmt.Printf("  Speed: %.2f\n", segment.Speed)
		}
		fmt.Printf("  Text: %s\n\n", segment.Text)
	}
	fmt.Println("=== END OF SEGMENTS INFORMATION ===")

}

// S3 helper functions
func checkS3ForFile(bucket, key string) (bool, error) {
	sess, err := session.NewSession()
	if err != nil {
		return false, fmt.Errorf("failed to create AWS session: %v", err)
	}

	svc := s3.New(sess)
	_, err = svc.HeadObject(&s3.HeadObjectInput{
		Bucket: aws.String(bucket),
		Key:    aws.String(key),
	})

	if err != nil {
		// If the error is a not found error, return false but no error
		if strings.Contains(err.Error(), "NotFound") {
			return false, nil
		}
		return false, fmt.Errorf("error checking S3: %v", err)
	}

	return true, nil
}

func downloadFromS3(bucket, key, destPath string) error {
	sess, err := session.NewSession()
	if err != nil {
		return fmt.Errorf("failed to create AWS session: %v", err)
	}

	// Create a file to write the S3 object to
	file, err := os.Create(destPath)
	if err != nil {
		return fmt.Errorf("failed to create file: %v", err)
	}
	defer file.Close()

	// Create a downloader
	downloader := s3manager.NewDownloader(sess)
	_, err = downloader.Download(file, &s3.GetObjectInput{
		Bucket: aws.String(bucket),
		Key:    aws.String(key),
	})

	if err != nil {
		return fmt.Errorf("failed to download file: %v", err)
	}

	return nil
}

func uploadToS3(bucket, key, filePath string) error {
	sess, err := session.NewSession()
	if err != nil {
		return fmt.Errorf("failed to create AWS session: %v", err)
	}

	// Open the file
	file, err := os.Open(filePath)
	if err != nil {
		return fmt.Errorf("failed to open file: %v", err)
	}
	defer file.Close()

	// Create an uploader
	uploader := s3manager.NewUploader(sess)
	_, err = uploader.Upload(&s3manager.UploadInput{
		Bucket: aws.String(bucket),
		Key:    aws.String(key),
		Body:   file,
	})

	if err != nil {
		return fmt.Errorf("failed to upload file: %v", err)
	}

	return nil
}

func main() {
	var config Config

	rootCmd := &cobra.Command{
		Use:   "voice",
		Short: "Convert VTT subtitles to speech using ElevenLabs",
		RunE: func(cmd *cobra.Command, args []string) error {
			return run(config)
		},
	}

	// Define flags
	homeDir, _ := os.UserHomeDir()
	defaultAPIKeyFile := filepath.Join(homeDir, ".elevenlabs.io")
	defaultTempDir := filepath.Join(os.TempDir(), "voicer-audio")

	rootCmd.Flags().StringVarP(&config.VTTFile, "vtt", "v", "", "VTT file to process (required)")
	defaultVoice := os.Getenv("VOICER_DEFAULT_VOICE")
	if defaultVoice == "" {
		defaultVoice = "Sophia"
	}
	rootCmd.Flags().StringVarP(&config.DefaultVoice, "voice", "d", defaultVoice, "Voice name (Sophia, Karol, Greg) or ElevenLabs voice ID (env: VOICER_DEFAULT_VOICE)")
	rootCmd.Flags().StringVarP(&config.APIKeyFile, "key-file", "k", defaultAPIKeyFile, "File containing ElevenLabs API key")
	rootCmd.Flags().StringVarP(&config.TempDir, "temp-dir", "t", defaultTempDir, "Temporary directory for audio segments")
	rootCmd.Flags().IntVarP(&config.Limit, "limit", "l", 0, "Limit number of segments to process (0 for unlimited)")
	rootCmd.Flags().DurationVarP(&config.Padding, "padding", "p", 0,
		"Extra padding to add to the end of the output audio (e.g. '5s', '1m')")
	rootCmd.Flags().BoolVarP(&config.AutoPad, "autopad", "a", false,
		"Automatically calculate and add sufficient padding to fit all audio segments")
	rootCmd.Flags().BoolVar(&config.AutoSpeed, "autospeed", false,
		"Automatically speed up segments that are too long")
	rootCmd.Flags().Float64VarP(&config.Speed, "speed", "S", 1.0,
		"Default speed for all segments (range: 0.7-1.2)")
	rootCmd.Flags().StringVarP(&config.OutputFile, "output", "o", "output.wav", "Output audio file")
	rootCmd.Flags().BoolVarP(&config.DryRun, "dry-run", "n", false, "Display segments information without processing")

	// New S3 bucket flag
	rootCmd.Flags().StringVarP(&config.S3Bucket, "s3-bucket", "s", "",
		"S3 bucket for caching audio segments (defaults to VOICER_S3_BUCKET env var) [untested]")

	// Output format flag
	rootCmd.Flags().StringVarP(&config.OutputFormat, "format", "f", "pcm_44100",
		"Output format for ElevenLabs API (pcm_44100 is the only one that has been tested)")

	rootCmd.MarkFlagRequired("vtt")
	rootCmd.MarkFlagRequired("output")

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

// voiceIDMap maps voice names to ElevenLabs voice IDs
var voiceIDMap = map[string]string{
	"Sophia": "LtPsVjX1k0Kl4StEMZPK",
	"Karol":  "CpXHPGrpEmAzh8JTmnO8",
	"Greg":   "7yYaoUVdbFZtJwHZqW9F",
}

// getVoiceID returns the voice ID for a given name or ID
func getVoiceID(nameOrID string) string {
	// Check if the name exists in our map
	if id, exists := voiceIDMap[nameOrID]; exists {
		return id
	}
	// If not in the map, assume it's already an ID
	return nameOrID
}

func run(config Config) error {
	// If S3 bucket is not specified, check environment variable
	if config.S3Bucket == "" {
		config.S3Bucket = os.Getenv("VOICER_S3_BUCKET")
	}

	// Ensure temp directory exists
	if err := os.MkdirAll(config.TempDir, 0755); err != nil {
		return fmt.Errorf("failed to create temp directory: %v", err)
	}

	// Read API key
	apiKeyBytes, err := os.ReadFile(config.APIKeyFile)
	if err != nil {
		return fmt.Errorf("failed to read API key file: %v", err)
	}
	apiKey := strings.TrimSpace(string(apiKeyBytes))

	// Open and parse VTT file
	subs, err := astisub.OpenFile(config.VTTFile)
	if err != nil {
		return fmt.Errorf("failed to open VTT file: %v", err)
	}

	// Process subtitles and generate audio segments
	segments := make([]AudioSegment, 0)
	for i, item := range subs.Items {
		if config.Limit > 0 && i >= config.Limit {
			break
		}

		// Extract text
		var text string
		for _, line := range item.Lines {
			for _, lineItem := range line.Items {
				// Extract text, removing speaker tags if present
				currentText := lineItem.Text
				if strings.HasPrefix(currentText, "<v ") && strings.Contains(currentText, ">") {
					parts := strings.SplitN(currentText, ">", 2)
					if len(parts) == 2 {
						currentText = strings.TrimSpace(parts[1])
					}
				}
				text += " " + currentText
			}
		}
		text = strings.TrimSpace(text)

		// Get previous and next text for context
		var prevText, nextText string
		if i > 0 {
			for _, line := range subs.Items[i-1].Lines {
				for _, lineItem := range line.Items {
					prevText += " " + lineItem.Text
				}
			}
			prevText = strings.TrimSpace(prevText)
		}

		if i < len(subs.Items)-1 {
			for _, line := range subs.Items[i+1].Lines {
				for _, lineItem := range line.Items {
					nextText += " " + lineItem.Text
				}
			}
			nextText = strings.TrimSpace(nextText)
		}

		// Use the default speed from config
		speed := config.Speed

		// Get the actual voice ID and calculate checksum based on text, context, voice and speed
		voiceID := getVoiceID(config.DefaultVoice)
		checksum := calculateChecksum(text, prevText, nextText, voiceID, speed)

		// Determine file extension based on output format
		fileExt := ".wav"
		if config.OutputFormat == "mp3_44100" {
			fileExt = ".mp3"
		}

		// Set path based on checksum
		audioFile := filepath.Join(config.TempDir, checksum+fileExt)

		// Add segment to our list
		segments = append(segments, AudioSegment{
			Path:      audioFile,
			StartTime: item.StartAt,
			EndTime:   item.EndAt,
			Text:      text,
			Checksum:  checksum,
			Speed:     speed,
		})
	}

	// If dry-run is enabled, print segment information and exit
	if config.DryRun {
		printSegmentInfo(segments)
		fmt.Println("Dry run completed. No audio files were generated or processed.")
		return nil
	}

	// Process segments possibly with multiple iterations for autospeed
	return processSegments(segments, config, apiKey, subs)
}

func processSegments(segments []AudioSegment, config Config, apiKey string, subs *astisub.Subtitles) error {
	// Keep track of segments that need regeneration
	regenerateIndices := make(map[int]bool)

	// First pass processing each segment
	for i := 0; i < len(segments); i++ {
		// Skip if we're planning to regenerate this segment
		if regenerateIndices[i] {
			continue
		}

		// Process the segment
		if err := processSegment(&segments[i], i, len(segments), config, apiKey); err != nil {
			return err
		}
	}

	// Find the total duration from the subtitles
	var lastEndTime time.Duration
	for _, item := range subs.Items {
		if item.EndAt > lastEndTime {
			lastEndTime = item.EndAt
		}
	}
	totalDuration := lastEndTime

	// Calculate the required padding if autopad is enabled
	padding := config.Padding
	if config.AutoPad {
		fmt.Println("Calculating required padding automatically...")
		requiredPadding, err := calculateRequiredPadding(segments, totalDuration, 44100)
		if err != nil {
			return fmt.Errorf("failed to calculate required padding: %v", err)
		}
		padding = requiredPadding
		fmt.Printf("Using automatically calculated padding of %v\n", padding)
	}

	// Try to mix the audio segments, with autospeed handling if enabled
	fmt.Println("Mixing audio segments...")
	mixed, err := mixAudio(segments, totalDuration, 44100, padding, config.AutoSpeed)
	if err != nil && config.AutoSpeed {
		// Check if it's an error about segment duration
		errMsg := err.Error()
		if strings.Contains(errMsg, "segment") && strings.Contains(errMsg, "duration") && strings.Contains(errMsg, "exceeds required duration") {
			// Parse the segment index from the error message
			var segmentIndex int
			fmt.Sscanf(errMsg, "segment %d", &segmentIndex)
			segmentIndex-- // Convert from 1-based to 0-based indexing

			if segmentIndex >= 0 && segmentIndex < len(segments) {
				// Increment speed for this segment (up to the max of 1.2)
				newSpeed := segments[segmentIndex].Speed + 0.1
				if newSpeed > 1.2 {
					newSpeed = 1.2
				}

				fmt.Printf("Segment %d needs to be regenerated with speed %.1f\n", segmentIndex+1, newSpeed)

				// Update the segment with new speed
				i := segmentIndex
				segment := &segments[i]
				segment.Speed = newSpeed

				// Generate new checksum for the segment with updated speed
				var prevText, nextText string
				if i > 0 {
					prevText = segments[i-1].Text
				}
				if i < len(segments)-1 {
					nextText = segments[i+1].Text
				}
				// Update checksum with new speed and resolved voice ID
				voiceID := getVoiceID(config.DefaultVoice)
				segment.Checksum = calculateChecksum(segment.Text, prevText, nextText, voiceID, newSpeed)
			
				// Determine file extension based on output format and update path
				fileExt := ".wav"
				if config.OutputFormat == "mp3_44100" {
					fileExt = ".mp3"
				}
				segment.Path = filepath.Join(config.TempDir, segment.Checksum+fileExt)

				// Process the segment with the new speed
				if err := processSegment(segment, i, len(segments), config, apiKey); err != nil {
					return err
				}

				// Try mixing again with the updated segment
				return processSegments(segments, config, apiKey, subs)
			}
		}

	}
	// If we get here and still have an error, return it
	if err != nil {
		return fmt.Errorf("failed to mix audio: %v", err)
	}

	// Save the mixed audio
	outputPath := config.OutputFile
	if !strings.HasSuffix(outputPath, ".wav") {
		outputPath = outputPath + ".wav"
	}

	if err := saveToWAV(mixed, outputPath); err != nil {
		return fmt.Errorf("failed to save output file: %v", err)
	}

	fmt.Printf("Created mixed audio file: %s\n", outputPath)

	return nil
}

func processSegment(segment *AudioSegment, i, totalSegments int, config Config, apiKey string) error {
	// Check if file exists locally
	localExists := false
	if _, err := os.Stat(segment.Path); err == nil {
		localExists = true
		fmt.Printf("Segment %d/%d found in local cache: %s\n", i+1, totalSegments, segment.Path)
	}

	// Check S3 if bucket is configured and file doesn't exist locally
	s3Key := filepath.Base(segment.Path)
	s3Exists := false

	if !localExists && config.S3Bucket != "" {
		var err error
		s3Exists, err = checkS3ForFile(config.S3Bucket, s3Key)
		if err != nil {
			fmt.Printf("Warning: Error checking S3: %v\n", err)
		}

		if s3Exists {
			fmt.Printf("Segment %d/%d found in S3 bucket, downloading...\n", i+1, totalSegments)
			if err := downloadFromS3(config.S3Bucket, s3Key, segment.Path); err != nil {
				return fmt.Errorf("failed to download segment from S3: %v", err)
			}
			localExists = true
		}
	}

	// If segment exists either locally or in S3, skip generation
	if localExists {
		fmt.Printf("Using cached segment %d/%d: %s\n", i+1, totalSegments, segment.Path)
		return nil
	}

	// Create TTS request with context and output format
	ttsRequest := TTSRequest{
		Text:         segment.Text,
		ModelID:      "eleven_multilingual_v2",
		OutputFormat: config.OutputFormat,
	}

	// If speed is not default, add voice settings
	if segment.Speed != 1.0 {
		ttsRequest.VoiceSettings = &VoiceSettings{
			Speed: segment.Speed,
		}
		fmt.Printf("Using speed %.2f for segment %d\n", segment.Speed, i+1)
	}

	// Add previous and next text for context
	if i > 0 {
		ttsRequest.PreviousText = segment.Text
	}
	if i < totalSegments-1 {
		ttsRequest.NextText = segment.Text
	}

	// Get the actual voice ID from the name or ID
	voiceID := getVoiceID(config.DefaultVoice)
	
	// Generate audio
	fmt.Printf("Generating audio for segment %d/%d (from %v to %v) in %s format using voice %s... %s\n",
		i+1, totalSegments, segment.StartTime, segment.EndTime, config.OutputFormat, config.DefaultVoice, segment.Text)

	audioData, err := textToSpeech(apiKey, voiceID, ttsRequest)
	if err != nil {
		return fmt.Errorf("failed to generate audio for segment %d: %v", i+1, err)
	}

	// Save audio file locally
	if strings.HasPrefix(config.OutputFormat, "pcm") {
		// Convert the raw PCM bytes into a PCMAudio structure.
		pcmAudio, err := rawPCMToPCMAudio(audioData, 44100) // 44100 sample rate per our request
		if err != nil {
			return fmt.Errorf("failed to convert raw PCM to PCMAudio for segment %d: %v", i+1, err)
		}
		// Save as a proper WAV file with header.
		if err := saveToWAV(pcmAudio, segment.Path); err != nil {
			return fmt.Errorf("failed to save audio segment %d: %v", i+1, err)
		}
	} else {
		// For MP3, simply write the bytes. Note that in a previous iteration of this
		// code I could cope with MP3 segments. But now I don't think it will work.
		// (Anyway, there were nasty "pops" so that's why I went away from compressed
		// formats like MP3).
		if err := os.WriteFile(segment.Path, audioData, 0644); err != nil {
			return fmt.Errorf("failed to save audio segment %d: %v", i+1, err)
		}
	}

	fmt.Printf("Created segment %d: %s\n", i+1, segment.Path)

	// Upload to S3 if bucket is configured
	if config.S3Bucket != "" {
		fmt.Printf("Uploading segment %d to S3 bucket %s...\n", i+1, config.S3Bucket)
		if err := uploadToS3(config.S3Bucket, s3Key, segment.Path); err != nil {
			fmt.Printf("Warning: Failed to upload segment to S3: %v\n", err)
		}
	}

	return nil
}
