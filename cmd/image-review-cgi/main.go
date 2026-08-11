package main

import (
	"database/sql"
	"fmt"
	"html"
	"log"
	"net/http"
	"net/http/cgi"
	"net/url"
	"os"
	"strings"

	_ "github.com/mattn/go-sqlite3"
)

const defaultDBPath = "/vhosts/professional-practice.industrial-linguistics.com/db/image-review.sqlite"
const defaultLogPath = "/vhosts/professional-practice.industrial-linguistics.com/db/image-review-cgi.log"

var logFile *os.File

type app struct {
	db *sql.DB
}

type candidate struct {
	ID               string
	BatchID          string
	TargetPath       string
	TopicPath        string
	SlideRef         string
	Brief            string
	Prompt           string
	CandidateURL     string
	CurrentSlideURL  string
	ProposedSlideURL string
	CandidateRelPath string
	Status           string
	ReviewComment    string
	ReviewedBy       sql.NullString
	ReviewedAt       sql.NullString
	ProcessedAt      sql.NullString
	RequeuedAt       sql.NullString
	CreatedAt        string
	UpdatedAt        string
}

func main() {
	configureLogging()

	dbPath := strings.TrimSpace(os.Getenv("IMAGE_REVIEW_DB"))
	if dbPath == "" {
		dbPath = defaultDBPath
	}

	db, err := openDB(dbPath)
	if err != nil {
		log.Fatalf("open image review db: %v", err)
	}
	defer db.Close()

	handler := &app{db: db}
	if isCGIRequest() {
		if err := cgi.Serve(handler); err != nil {
			log.Fatalf("serve cgi: %v", err)
		}
		return
	}

	addr := "127.0.0.1:8097"
	log.Printf("serving image review UI on http://%s with %s", addr, dbPath)
	log.Fatal(http.ListenAndServe(addr, handler))
}

func configureLogging() {
	path := strings.TrimSpace(os.Getenv("IMAGE_REVIEW_LOG"))
	if path == "" {
		path = defaultLogPath
	}
	f, err := os.OpenFile(path, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0640)
	if err != nil {
		return
	}
	logFile = f
	log.SetOutput(logFile)
}

func isCGIRequest() bool {
	if os.Getenv("GATEWAY_INTERFACE") != "" || os.Getenv("FCGI_ROLE") != "" {
		return true
	}
	return os.Getenv("REQUEST_METHOD") != "" &&
		(os.Getenv("SERVER_PROTOCOL") != "" || os.Getenv("SCRIPT_NAME") != "" || os.Getenv("REQUEST_URI") != "")
}

func openDB(path string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", path)
	if err != nil {
		return nil, err
	}

	pragmas := []string{
		"PRAGMA busy_timeout = 5000",
		"PRAGMA foreign_keys = ON",
		"PRAGMA journal_mode = DELETE",
	}
	for _, pragma := range pragmas {
		if _, err := db.Exec(pragma); err != nil {
			db.Close()
			return nil, err
		}
	}

	if _, err := db.Exec(schemaSQL); err != nil {
		db.Close()
		return nil, err
	}
	return db, nil
}

func (a *app) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodGet:
		if strings.TrimSpace(r.URL.Query().Get("candidate")) != "" {
			a.renderDetail(w, r)
			return
		}
		a.renderIndex(w, r)
	case http.MethodPost:
		a.handleReview(w, r)
	default:
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
	}
}

func (a *app) handleReview(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, "invalid form", http.StatusBadRequest)
		return
	}

	id := strings.TrimSpace(r.FormValue("id"))
	action := strings.TrimSpace(r.FormValue("action"))
	comment := strings.TrimSpace(r.FormValue("comment"))
	from := normaliseFilter(r.FormValue("from"))
	if id == "" {
		http.Error(w, "missing candidate id", http.StatusBadRequest)
		return
	}

	status := ""
	switch action {
	case "approve":
		status = "approved"
	case "reject":
		status = "rejected"
	case "comment":
		status = "commented"
	default:
		http.Error(w, "unknown review action", http.StatusBadRequest)
		return
	}

	user := remoteUser()
	tx, err := a.db.Begin()
	if err != nil {
		http.Error(w, "database error", http.StatusInternalServerError)
		log.Printf("begin review tx: %v", err)
		return
	}
	defer tx.Rollback()

	res, err := tx.Exec(`
		UPDATE candidates
		SET status = ?,
		    review_comment = ?,
		    reviewed_by = ?,
		    reviewed_at = CURRENT_TIMESTAMP,
		    processed_at = NULL,
		    requeued_at = NULL,
		    updated_at = CURRENT_TIMESTAMP
		WHERE id = ?`,
		status, comment, user, id,
	)
	if err != nil {
		http.Error(w, "database error", http.StatusInternalServerError)
		log.Printf("update candidate %s: %v", id, err)
		return
	}
	affected, _ := res.RowsAffected()
	if affected == 0 {
		http.Error(w, "candidate not found", http.StatusNotFound)
		return
	}

	if _, err := tx.Exec(`
		INSERT INTO review_events(candidate_id, actor, action, comment)
		VALUES (?, ?, ?, ?)`,
		id, user, action, comment,
	); err != nil {
		http.Error(w, "database error", http.StatusInternalServerError)
		log.Printf("insert review event for %s: %v", id, err)
		return
	}

	if err := tx.Commit(); err != nil {
		http.Error(w, "database error", http.StatusInternalServerError)
		log.Printf("commit review for %s: %v", id, err)
		return
	}

	http.Redirect(
		w,
		r,
		reviewPath(r)+"?candidate="+url.QueryEscape(id)+"&saved="+url.QueryEscape(status)+"&from="+url.QueryEscape(from),
		http.StatusSeeOther,
	)
}

func reviewPath(r *http.Request) string {
	if scriptName := strings.TrimSpace(os.Getenv("SCRIPT_NAME")); strings.HasPrefix(scriptName, "/") {
		return scriptName
	}
	if r.URL != nil && strings.HasPrefix(r.URL.Path, "/") && r.URL.Path != "" {
		return r.URL.Path
	}
	return "/"
}

func (a *app) renderIndex(w http.ResponseWriter, r *http.Request) {
	items, err := a.loadCandidates()
	if err != nil {
		http.Error(w, "database error", http.StatusInternalServerError)
		log.Printf("load candidates: %v", err)
		return
	}

	filter := normaliseFilter(r.URL.Query().Get("status"))
	visibleItems := filterCandidates(items, filter)

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	renderPageStart(
		w,
		"Image review",
		"Choose a suggested update to inspect its image, slide comparison and review controls.",
	)
	fmt.Fprint(w, `<main class="page index-page">`)
	renderSummary(w, items)
	renderFilters(w, items, filter)

	if len(visibleItems) == 0 {
		fmt.Fprintf(
			w,
			`<div class="empty-state"><h2>No %s items</h2><p>There are no image updates in this view.</p><a class="button-link" href="?status=all">Show all updates</a></div>`,
			h(filterLabel(filter)),
		)
	} else {
		fmt.Fprintf(w, `<div class="list-heading"><h2>%s</h2><span>%d %s</span></div>`, h(filterLabel(filter)), len(visibleItems), plural(len(visibleItems), "item", "items"))
		fmt.Fprint(w, `<ol class="review-list">`)
		for _, item := range visibleItems {
			renderIndexItem(w, item, filter)
		}
		fmt.Fprint(w, `</ol>`)
	}

	renderPageEnd(w)
}

func (a *app) renderDetail(w http.ResponseWriter, r *http.Request) {
	id := strings.TrimSpace(r.URL.Query().Get("candidate"))
	item, found, err := a.loadCandidate(id)
	if err != nil {
		http.Error(w, "database error", http.StatusInternalServerError)
		log.Printf("load candidate %s: %v", id, err)
		return
	}
	if !found {
		http.Error(w, "candidate not found", http.StatusNotFound)
		return
	}

	from := normaliseFilter(r.URL.Query().Get("from"))
	saved := strings.TrimSpace(r.URL.Query().Get("saved"))
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	renderPageStart(w, "Review suggested update", "Compare the current slide with the proposed image treatment, then record a decision.")

	fmt.Fprint(w, `<main class="page detail-page">`)
	fmt.Fprintf(w, `<a class="back-link" href="?status=%s">← Back to %s</a>`, h(from), h(strings.ToLower(filterLabel(from))))
	if saved != "" {
		fmt.Fprintf(w, `<div class="saved-notice" role="status">Review saved as <strong>%s</strong>.</div>`, h(statusLabel(saved)))
	}

	fmt.Fprint(w, `<article class="candidate-detail">`)
	fmt.Fprint(w, `<header class="detail-header">`)
	fmt.Fprint(w, `<div>`)
	fmt.Fprintf(w, `<div class="eyebrow">%s · %s</div>`, h(item.BatchID), h(item.SlideRef))
	fmt.Fprintf(w, `<h1>%s</h1>`, h(item.Brief))
	fmt.Fprintf(w, `<div class="candidate-id">%s</div>`, h(item.ID))
	fmt.Fprint(w, `</div>`)
	renderStatus(w, item.Status)
	fmt.Fprint(w, `</header>`)

	fmt.Fprint(w, `<dl class="metadata">`)
	metadata(w, "Target", item.TargetPath)
	metadata(w, "Topic", item.TopicPath)
	metadata(w, "Batch", item.BatchID)
	metadata(w, "Slide", item.SlideRef)
	if item.ReviewedBy.Valid || item.ReviewedAt.Valid {
		metadata(w, "Last reviewed", strings.TrimSpace(item.ReviewedBy.String+" "+item.ReviewedAt.String))
	}
	fmt.Fprint(w, `</dl>`)

	if strings.TrimSpace(item.Prompt) != "" {
		fmt.Fprintf(w, `<section class="note"><h2>Image brief</h2><p>%s</p></section>`, h(item.Prompt))
	}
	if strings.TrimSpace(item.ReviewComment) != "" {
		fmt.Fprintf(w, `<section class="note review-comment"><h2>Review comment</h2><p>%s</p></section>`, h(item.ReviewComment))
	}

	fmt.Fprint(w, `<section class="visual-review" aria-labelledby="visual-review-heading">`)
	fmt.Fprint(w, `<div class="section-heading"><div><div class="eyebrow">Suggested update</div><h2 id="visual-review-heading">Generated image</h2></div></div>`)
	imageFigure(w, "Generated image", item.CandidateURL, "hero-figure")
	fmt.Fprint(w, `<div class="section-heading comparison-heading"><div><div class="eyebrow">In context</div><h2>Slide comparison</h2></div></div>`)
	fmt.Fprint(w, `<div class="slide-comparison">`)
	imageFigure(w, "Current slide", item.CurrentSlideURL, "")
	imageFigure(w, "Proposed slide", item.ProposedSlideURL, "proposed")
	fmt.Fprint(w, `</div></section>`)

	fmt.Fprintf(w, `<form class="review-panel" method="post" action="?candidate=%s">`, h(url.QueryEscape(item.ID)))
	fmt.Fprint(w, `<div><div class="eyebrow">Your decision</div><h2>Review this update</h2><p>Comments are retained with the candidate for the next image pass.</p></div>`)
	fmt.Fprintf(w, `<input type="hidden" name="id" value="%s">`, h(item.ID))
	fmt.Fprintf(w, `<input type="hidden" name="from" value="%s">`, h(from))
	fmt.Fprintf(w, `<label for="review-comment">Comment <span>(optional)</span></label><textarea id="review-comment" name="comment" placeholder="What should change in the next version?">%s</textarea>`, h(item.ReviewComment))
	fmt.Fprint(w, `<div class="actions">`)
	fmt.Fprint(w, `<button type="submit" name="action" value="approve">Approve</button>`)
	fmt.Fprint(w, `<button type="submit" name="action" value="reject">Reject</button>`)
	fmt.Fprint(w, `<button type="submit" name="action" value="comment">Save comment</button>`)
	fmt.Fprint(w, `</div></form>`)
	fmt.Fprint(w, `</article>`)

	renderPageEnd(w)
}

func renderPageStart(w http.ResponseWriter, title string, subtitle string) {
	fmt.Fprint(w, `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#182d46">
<title>`)
	fmt.Fprint(w, h(title))
	fmt.Fprint(w, ` · Professional Practice</title>
<link rel="stylesheet" href="/image-review/review.css">
</head>
<body>
<header class="site-header">
<a class="brand" href="?">IT Professional Practice</a>
<h1>`)
	fmt.Fprint(w, h(title))
	fmt.Fprint(w, `</h1>
<p>`)
	fmt.Fprint(w, h(subtitle))
	fmt.Fprint(w, `</p>
</header>
`)
}

func renderPageEnd(w http.ResponseWriter) {
	fmt.Fprint(w, `</main></body></html>`)
}

func renderSummary(w http.ResponseWriter, items []candidate) {
	fmt.Fprint(w, `<section class="summary" aria-label="Review totals">`)
	summaryItem(w, countFilter(items, "unapproved"), "Unapproved")
	summaryItem(w, countStatus(items, "approved"), "Approved")
	summaryItem(w, countStatus(items, "processed"), "Published")
	summaryItem(w, len(items), "All updates")
	fmt.Fprint(w, `</section>`)
}

func summaryItem(w http.ResponseWriter, count int, label string) {
	fmt.Fprintf(w, `<div class="summary-item"><strong>%d</strong><span>%s</span></div>`, count, h(label))
}

func renderFilters(w http.ResponseWriter, items []candidate, active string) {
	filters := []struct {
		value string
		label string
		count int
	}{
		{"unapproved", "Unapproved", countFilter(items, "unapproved")},
		{"approved", "Approved", countStatus(items, "approved")},
		{"processed", "Published", countStatus(items, "processed")},
		{"all", "All", len(items)},
	}
	fmt.Fprint(w, `<nav class="filters" aria-label="Filter image updates">`)
	for _, filter := range filters {
		className := "filter"
		current := ""
		if filter.value == active {
			className += " active"
			current = ` aria-current="page"`
		}
		fmt.Fprintf(w, `<a class="%s" href="?status=%s"%s>%s <span>%d</span></a>`, className, h(filter.value), current, h(filter.label), filter.count)
	}
	fmt.Fprint(w, `</nav>`)
}

func renderIndexItem(w http.ResponseWriter, item candidate, filter string) {
	fmt.Fprint(w, `<li>`)
	fmt.Fprintf(w, `<a class="review-row" href="?candidate=%s&amp;from=%s">`, h(url.QueryEscape(item.ID)), h(filter))
	fmt.Fprint(w, `<div>`)
	fmt.Fprintf(w, `<h3>%s</h3>`, h(item.Brief))
	fmt.Fprintf(w, `<div class="row-meta">%s · %s</div>`, h(item.BatchID), h(valueOrDash(item.SlideRef)))
	fmt.Fprintf(w, `<div class="target">%s</div>`, h(item.TargetPath))
	fmt.Fprint(w, `</div>`)
	renderStatus(w, item.Status)
	fmt.Fprint(w, `</a></li>`)
}

func renderStatus(w http.ResponseWriter, status string) {
	fmt.Fprintf(w, `<span class="status status-%s">%s</span>`, h(status), h(statusLabel(status)))
}

func statusLabel(status string) string {
	switch strings.ToLower(strings.TrimSpace(status)) {
	case "pending":
		return "Awaiting review"
	case "approved":
		return "Approved"
	case "rejected":
		return "Rejected"
	case "commented":
		return "Commented"
	case "processed":
		return "Published"
	default:
		return status
	}
}

func normaliseFilter(filter string) string {
	switch strings.ToLower(strings.TrimSpace(filter)) {
	case "approved":
		return "approved"
	case "processed":
		return "processed"
	case "all":
		return "all"
	default:
		return "unapproved"
	}
}

func filterLabel(filter string) string {
	switch filter {
	case "approved":
		return "Approved"
	case "processed":
		return "Published"
	case "all":
		return "All updates"
	default:
		return "Unapproved"
	}
}

func filterCandidates(items []candidate, filter string) []candidate {
	if filter == "all" {
		return items
	}
	filtered := make([]candidate, 0, len(items))
	for _, item := range items {
		if filter == "unapproved" {
			if item.Status != "approved" && item.Status != "processed" {
				filtered = append(filtered, item)
			}
			continue
		}
		if item.Status == filter {
			filtered = append(filtered, item)
		}
	}
	return filtered
}

func countFilter(items []candidate, filter string) int {
	return len(filterCandidates(items, filter))
}

func countStatus(items []candidate, status string) int {
	count := 0
	for _, item := range items {
		if item.Status == status {
			count++
		}
	}
	return count
}

func plural(count int, singular string, plural string) string {
	if count == 1 {
		return singular
	}
	return plural
}

func valueOrDash(value string) string {
	if strings.TrimSpace(value) == "" {
		return "-"
	}
	return value
}

func (a *app) loadCandidates() ([]candidate, error) {
	rows, err := a.db.Query(`
		SELECT id, batch_id, target_path, topic_path, slide_ref, brief, prompt,
		       candidate_url, current_slide_url, proposed_slide_url, candidate_rel_path,
		       status, review_comment, reviewed_by, reviewed_at, processed_at, requeued_at,
		       created_at, updated_at
		FROM candidates
		ORDER BY
		  CASE status
		    WHEN 'pending' THEN 0
		    WHEN 'commented' THEN 1
		    WHEN 'rejected' THEN 2
		    WHEN 'approved' THEN 3
		    WHEN 'processed' THEN 4
		    ELSE 5
		  END,
		  created_at DESC,
		  id`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var items []candidate
	for rows.Next() {
		var item candidate
		if err := rows.Scan(
			&item.ID,
			&item.BatchID,
			&item.TargetPath,
			&item.TopicPath,
			&item.SlideRef,
			&item.Brief,
			&item.Prompt,
			&item.CandidateURL,
			&item.CurrentSlideURL,
			&item.ProposedSlideURL,
			&item.CandidateRelPath,
			&item.Status,
			&item.ReviewComment,
			&item.ReviewedBy,
			&item.ReviewedAt,
			&item.ProcessedAt,
			&item.RequeuedAt,
			&item.CreatedAt,
			&item.UpdatedAt,
		); err != nil {
			return nil, err
		}
		items = append(items, item)
	}
	return items, rows.Err()
}

func (a *app) loadCandidate(id string) (candidate, bool, error) {
	var item candidate
	err := a.db.QueryRow(`
		SELECT id, batch_id, target_path, topic_path, slide_ref, brief, prompt,
		       candidate_url, current_slide_url, proposed_slide_url, candidate_rel_path,
		       status, review_comment, reviewed_by, reviewed_at, processed_at, requeued_at,
		       created_at, updated_at
		FROM candidates
		WHERE id = ?`,
		id,
	).Scan(
		&item.ID,
		&item.BatchID,
		&item.TargetPath,
		&item.TopicPath,
		&item.SlideRef,
		&item.Brief,
		&item.Prompt,
		&item.CandidateURL,
		&item.CurrentSlideURL,
		&item.ProposedSlideURL,
		&item.CandidateRelPath,
		&item.Status,
		&item.ReviewComment,
		&item.ReviewedBy,
		&item.ReviewedAt,
		&item.ProcessedAt,
		&item.RequeuedAt,
		&item.CreatedAt,
		&item.UpdatedAt,
	)
	if err == sql.ErrNoRows {
		return candidate{}, false, nil
	}
	if err != nil {
		return candidate{}, false, err
	}
	return item, true, nil
}

func metadata(w http.ResponseWriter, label string, value string) {
	fmt.Fprintf(w, `<div><dt>%s</dt><dd>%s</dd></div>`, h(label), h(valueOrDash(value)))
}

func imageFigure(w http.ResponseWriter, label string, src string, className string) {
	figureClass := ""
	if strings.TrimSpace(className) != "" {
		figureClass = fmt.Sprintf(` class="%s"`, h(className))
	}
	fmt.Fprintf(w, `<figure%s><figcaption>%s</figcaption>`, figureClass, h(label))
	if strings.TrimSpace(src) == "" {
		fmt.Fprint(w, `<div class="missing-preview">Preview unavailable</div></figure>`)
		return
	}
	fmt.Fprintf(w, `<img src="%s" alt="%s" loading="lazy"></figure>`, h(src), h(label))
}

func remoteUser() string {
	user := strings.TrimSpace(os.Getenv("REMOTE_USER"))
	if user == "" {
		return "unknown"
	}
	return user
}

func h(value string) string {
	return html.EscapeString(value)
}

const schemaSQL = `
CREATE TABLE IF NOT EXISTS candidates (
	id TEXT PRIMARY KEY,
	batch_id TEXT NOT NULL DEFAULT '',
	target_path TEXT NOT NULL,
	topic_path TEXT NOT NULL DEFAULT '',
	slide_ref TEXT NOT NULL DEFAULT '',
	brief TEXT NOT NULL DEFAULT '',
	prompt TEXT NOT NULL DEFAULT '',
	candidate_url TEXT NOT NULL,
	current_slide_url TEXT NOT NULL,
	proposed_slide_url TEXT NOT NULL,
	candidate_rel_path TEXT NOT NULL DEFAULT '',
	status TEXT NOT NULL DEFAULT 'pending'
		CHECK (status IN ('pending', 'approved', 'rejected', 'commented', 'processed')),
	review_comment TEXT NOT NULL DEFAULT '',
	reviewed_by TEXT,
	reviewed_at TEXT,
	processed_at TEXT,
	requeued_at TEXT,
	created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS review_events (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	candidate_id TEXT NOT NULL,
	actor TEXT NOT NULL DEFAULT '',
	action TEXT NOT NULL,
	comment TEXT NOT NULL DEFAULT '',
	created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status, created_at);
CREATE INDEX IF NOT EXISTS idx_review_events_candidate ON review_events(candidate_id, created_at);
`
