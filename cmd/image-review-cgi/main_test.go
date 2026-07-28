package main

import (
	"io"
	"net/http"
	"net/http/httptest"
	"net/url"
	"path/filepath"
	"strings"
	"testing"
)

func testApp(t *testing.T) *app {
	t.Helper()

	db, err := openDB(filepath.Join(t.TempDir(), "image-review.sqlite"))
	if err != nil {
		t.Fatalf("open test database: %v", err)
	}
	t.Cleanup(func() {
		db.Close()
	})

	items := []struct {
		id     string
		status string
		brief  string
	}{
		{"pending-one", "pending", "Pending lifecycle image"},
		{"commented-one", "commented", "Commented workflow image"},
		{"rejected-one", "rejected", "Rejected roadmap image"},
		{"approved-one", "approved", "Approved service map"},
		{"processed-one", "processed", "Published dashboard image"},
	}
	for _, item := range items {
		_, err := db.Exec(`
			INSERT INTO candidates(
				id, batch_id, target_path, topic_path, slide_ref, brief, prompt,
				candidate_url, current_slide_url, proposed_slide_url, candidate_rel_path,
				status
			)
			VALUES (?, '2026-07-28', ?, 'content/part-01/topic', 'slide 3', ?, 'Use accessible labels',
			        ?, ?, ?, ?, ?)`,
			item.id,
			"content/part-01/topic/images/"+item.id+".png",
			item.brief,
			"/image-review/candidates/"+item.id+"/candidate.png",
			"/image-review/candidates/"+item.id+"/current-slide.png",
			"/image-review/candidates/"+item.id+"/proposed-slide.png",
			item.id+"/candidate.png",
			item.status,
		)
		if err != nil {
			t.Fatalf("insert %s: %v", item.id, err)
		}
	}
	return &app{db: db}
}

func responseBody(t *testing.T, response *http.Response) string {
	t.Helper()
	defer response.Body.Close()
	body, err := io.ReadAll(response.Body)
	if err != nil {
		t.Fatalf("read response: %v", err)
	}
	return string(body)
}

func TestIndexIsACompactStatusFilteredList(t *testing.T) {
	server := httptest.NewServer(testApp(t))
	defer server.Close()

	response, err := http.Get(server.URL + "/")
	if err != nil {
		t.Fatalf("get index: %v", err)
	}
	body := responseBody(t, response)

	for _, want := range []string{
		"Unapproved",
		"Approved",
		"Published",
		`href="?candidate=pending-one&amp;from=unapproved"`,
		"Awaiting review",
		"Commented",
		"Rejected",
	} {
		if !strings.Contains(body, want) {
			t.Errorf("index does not contain %q", want)
		}
	}
	if strings.Contains(body, "<img") {
		t.Error("index unexpectedly expands candidate images")
	}
	if strings.Contains(body, "Approved service map") {
		t.Error("default unapproved filter includes an approved candidate")
	}
}

func TestIndexCanShowApprovedCandidates(t *testing.T) {
	server := httptest.NewServer(testApp(t))
	defer server.Close()

	response, err := http.Get(server.URL + "/?status=approved")
	if err != nil {
		t.Fatalf("get approved index: %v", err)
	}
	body := responseBody(t, response)

	if !strings.Contains(body, "Approved service map") {
		t.Error("approved filter omits approved candidate")
	}
	if strings.Contains(body, "Pending lifecycle image") {
		t.Error("approved filter includes pending candidate")
	}
	if !strings.Contains(body, `aria-current="page">Approved`) {
		t.Error("approved filter is not marked as current")
	}
}

func TestDetailShowsOneCandidateAndResponsiveReviewControls(t *testing.T) {
	server := httptest.NewServer(testApp(t))
	defer server.Close()

	response, err := http.Get(server.URL + "/?candidate=pending-one&from=unapproved")
	if err != nil {
		t.Fatalf("get detail: %v", err)
	}
	body := responseBody(t, response)

	for _, want := range []string{
		"Pending lifecycle image",
		"Generated image",
		"Current slide",
		"Proposed slide",
		`name="action" value="approve"`,
		`name="action" value="reject"`,
		`name="action" value="comment"`,
		`name="from" value="unapproved"`,
		`href="?status=unapproved"`,
		"@media (max-width: 720px)",
	} {
		if !strings.Contains(body, want) {
			t.Errorf("detail does not contain %q", want)
		}
	}
	if count := strings.Count(body, "<img"); count != 3 {
		t.Errorf("detail contains %d images, want 3", count)
	}
	if strings.Contains(body, "Approved service map") {
		t.Error("detail includes another candidate")
	}
}

func TestReviewRedirectsBackToTheCandidateDetail(t *testing.T) {
	application := testApp(t)
	server := httptest.NewServer(application)
	defer server.Close()

	client := server.Client()
	client.CheckRedirect = func(_ *http.Request, _ []*http.Request) error {
		return http.ErrUseLastResponse
	}
	form := url.Values{
		"id":      {"pending-one"},
		"action":  {"approve"},
		"comment": {"Ready to publish"},
		"from":    {"unapproved"},
	}
	response, err := client.PostForm(server.URL+"/", form)
	if err != nil {
		t.Fatalf("post review: %v", err)
	}
	response.Body.Close()

	if response.StatusCode != http.StatusSeeOther {
		t.Fatalf("review status = %d, want %d", response.StatusCode, http.StatusSeeOther)
	}
	location := response.Header.Get("Location")
	for _, want := range []string{"candidate=pending-one", "saved=approved", "from=unapproved"} {
		if !strings.Contains(location, want) {
			t.Errorf("redirect %q does not contain %q", location, want)
		}
	}

	var status, comment string
	if err := application.db.QueryRow(
		`SELECT status, review_comment FROM candidates WHERE id = 'pending-one'`,
	).Scan(&status, &comment); err != nil {
		t.Fatalf("load reviewed candidate: %v", err)
	}
	if status != "approved" || comment != "Ready to publish" {
		t.Errorf("saved review = (%q, %q), want (approved, Ready to publish)", status, comment)
	}
}

func TestReviewRedirectRetainsTheCGIScriptPath(t *testing.T) {
	for _, action := range []string{"reject", "comment"} {
		t.Run(action, func(t *testing.T) {
			application := testApp(t)
			form := url.Values{
				"id":      {"pending-one"},
				"action":  {action},
				"comment": {"Needs another pass"},
				"from":    {"unapproved"},
			}
			request := httptest.NewRequest(
				http.MethodPost,
				"https://professional-practice.industrial-linguistics.com/cgi-bin/image-review.cgi?candidate=pending-one",
				strings.NewReader(form.Encode()),
			)
			request.Header.Set("Content-Type", "application/x-www-form-urlencoded")
			response := httptest.NewRecorder()

			application.ServeHTTP(response, request)

			if response.Code != http.StatusSeeOther {
				t.Fatalf("review status = %d, want %d", response.Code, http.StatusSeeOther)
			}
			location := response.Header().Get("Location")
			wantPrefix := "/cgi-bin/image-review.cgi?candidate=pending-one"
			if !strings.HasPrefix(location, wantPrefix) {
				t.Errorf("redirect = %q, want prefix %q", location, wantPrefix)
			}
			if strings.HasPrefix(location, "/cgi-bin/?") {
				t.Errorf("redirect drops the CGI script name: %q", location)
			}
		})
	}
}

func TestUnknownCandidateReturnsNotFound(t *testing.T) {
	server := httptest.NewServer(testApp(t))
	defer server.Close()

	response, err := http.Get(server.URL + "/?candidate=missing")
	if err != nil {
		t.Fatalf("get missing detail: %v", err)
	}
	response.Body.Close()
	if response.StatusCode != http.StatusNotFound {
		t.Errorf("missing detail status = %d, want %d", response.StatusCode, http.StatusNotFound)
	}
}
