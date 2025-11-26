#!/usr/bin/env python3
"""
Build manifest system for incremental builds
Tracks file hashes and determines what needs to be rebuilt
"""

import sys
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

MANIFEST_FILE = Path(".build-manifest.json")

class BuildManifest:
    def __init__(self, manifest_file: Path = MANIFEST_FILE):
        self.manifest_file = manifest_file
        self.data = self._load()

    def _load(self) -> Dict:
        """Load manifest from file"""
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load manifest: {e}")
                return {}
        return {}

    def save(self):
        """Save manifest to file"""
        try:
            with open(self.manifest_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error: Failed to save manifest: {e}")

    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file"""
        if not file_path.exists():
            return ""

        md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception:
            return ""

    def get_source_hashes(self, topic_path: Path) -> Dict[str, str]:
        """Get hashes of all source files for a topic"""
        hashes = {}

        # Slides
        slides_file = topic_path / "slides.md"
        if slides_file.exists():
            hashes['slides.md'] = self.get_file_hash(slides_file)

        # Narratives
        narratives_dir = topic_path / "narratives"
        if narratives_dir.exists():
            for narrative_file in sorted(narratives_dir.glob("*.md")):
                rel_path = str(narrative_file.relative_to(topic_path))
                hashes[rel_path] = self.get_file_hash(narrative_file)

        # Images in the topic directory
        images_dir = topic_path / "images"
        if images_dir.exists():
            for img_file in sorted(images_dir.glob("*.*")):
                rel_path = str(img_file.relative_to(topic_path))
                hashes[rel_path] = self.get_file_hash(img_file)

        return hashes

    def get_output_hashes(self, topic_path: Path) -> Dict[str, str]:
        """Get hashes of all output files for a topic"""
        hashes = {}

        # VTT file
        vtt_file = topic_path / "subtitles.vtt"
        if vtt_file.exists():
            hashes['subtitles.vtt'] = self.get_file_hash(vtt_file)

        # Audio file
        audio_file = topic_path / "audio.wav"
        if audio_file.exists():
            hashes['audio.wav'] = self.get_file_hash(audio_file)

        # Video file
        video_file = topic_path / "final.mp4"
        if video_file.exists():
            hashes['final.mp4'] = self.get_file_hash(video_file)

        return hashes

    def needs_rebuild(self, topic_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Determine if a topic needs to be rebuilt
        Returns (needs_rebuild, reason)
        """
        topic_key = str(topic_path)

        # Get current source hashes
        current_sources = self.get_source_hashes(topic_path)

        # Get previous build info
        previous_build = self.data.get(topic_key, {})
        previous_sources = previous_build.get('sources', {})

        # Check if any source files changed
        for file_path, current_hash in current_sources.items():
            previous_hash = previous_sources.get(file_path, "")
            if current_hash != previous_hash:
                return True, f"Source file changed: {file_path}"

        # Check if any source files were deleted
        for file_path in previous_sources:
            if file_path not in current_sources:
                return True, f"Source file deleted: {file_path}"

        # Check if outputs exist
        expected_outputs = ['subtitles.vtt', 'audio.wav', 'final.mp4']
        for output_file in expected_outputs:
            file_path = topic_path / output_file
            if not file_path.exists():
                return True, f"Missing output: {output_file}"

        # Check if this topic was never built
        if not previous_build:
            return True, "Never built before"

        return False, None

    def update_build_info(self, topic_path: Path, test_results: Dict = None):
        """Update build information for a topic"""
        topic_key = str(topic_path)

        self.data[topic_key] = {
            'sources': self.get_source_hashes(topic_path),
            'outputs': self.get_output_hashes(topic_path),
            'last_built': datetime.now().isoformat(),
            'tests': test_results or {}
        }

        self.save()

    def get_topics_to_build(self, content_dir: Path) -> List[Tuple[Path, str]]:
        """
        Get list of topics that need to be built
        Returns list of (topic_path, reason) tuples
        """
        topics_to_build = []

        # Find all topic directories (directories with slides.md)
        for part_dir in sorted(content_dir.glob("part-*")):
            if not part_dir.is_dir():
                continue

            for topic_dir in sorted(part_dir.iterdir()):
                if not topic_dir.is_dir():
                    continue

                slides_file = topic_dir / "slides.md"
                if not slides_file.exists():
                    continue

                needs_rebuild, reason = self.needs_rebuild(topic_dir)
                if needs_rebuild:
                    topics_to_build.append((topic_dir, reason))

        return topics_to_build

    def mark_build_failed(self, topic_path: Path, error: str):
        """Mark a build as failed"""
        topic_key = str(topic_path)

        if topic_key not in self.data:
            self.data[topic_key] = {}

        self.data[topic_key]['last_build_failed'] = True
        self.data[topic_key]['last_error'] = error
        self.data[topic_key]['last_attempted'] = datetime.now().isoformat()

        self.save()

    def get_build_status(self) -> Dict:
        """Get summary of build status"""
        status = {
            'total_topics': 0,
            'built': 0,
            'failed': 0,
            'never_built': 0
        }

        for topic_key, info in self.data.items():
            status['total_topics'] += 1

            if info.get('last_build_failed'):
                status['failed'] += 1
            elif info.get('last_built'):
                status['built'] += 1
            else:
                status['never_built'] += 1

        return status

def main():
    if len(sys.argv) < 2:
        print("Usage: build_manifest.py <command> [args]")
        print("\nCommands:")
        print("  check [content-dir]     - Check what needs to be built")
        print("  update <topic-path>     - Update manifest after successful build")
        print("  status                  - Show build status summary")
        print("  reset                   - Clear manifest (rebuild everything)")
        sys.exit(1)

    command = sys.argv[1]
    manifest = BuildManifest()

    if command == "check":
        content_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("content")
        topics_to_build = manifest.get_topics_to_build(content_dir)

        print(f"\n{'=' * 70}")
        print(f"BUILD STATUS CHECK")
        print(f"{'=' * 70}\n")

        if not topics_to_build:
            print("✅ Everything up to date - nothing to build")
        else:
            print(f"Found {len(topics_to_build)} topic(s) that need to be built:\n")
            for topic_path, reason in topics_to_build:
                print(f"  📹 {topic_path}")
                print(f"     Reason: {reason}\n")

        print(f"{'=' * 70}\n")

    elif command == "update":
        if len(sys.argv) < 3:
            print("Error: topic-path required")
            sys.exit(1)

        topic_path = Path(sys.argv[2])
        manifest.update_build_info(topic_path)
        print(f"✅ Updated manifest for {topic_path}")

    elif command == "status":
        status = manifest.get_build_status()

        print(f"\n{'=' * 70}")
        print(f"BUILD STATUS SUMMARY")
        print(f"{'=' * 70}\n")
        print(f"  Total topics: {status['total_topics']}")
        print(f"  ✅ Built: {status['built']}")
        print(f"  ❌ Failed: {status['failed']}")
        print(f"  ⚪ Never built: {status['never_built']}")
        print(f"{'=' * 70}\n")

    elif command == "reset":
        if MANIFEST_FILE.exists():
            MANIFEST_FILE.unlink()
            print("✅ Manifest cleared - everything will be rebuilt")
        else:
            print("ℹ️  No manifest to clear")

    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)

if __name__ == '__main__':
    main()
