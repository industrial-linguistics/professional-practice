package main

import (
	"database/sql"
	"fmt"
	"html"
	"log"
	"net/http"
	"net/http/cgi"
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
		a.renderList(w, r)
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

	http.Redirect(w, r, "./image-review.cgi#"+urlFragment(id), http.StatusSeeOther)
}

func (a *app) renderList(w http.ResponseWriter, _ *http.Request) {
	items, err := a.loadCandidates()
	if err != nil {
		http.Error(w, "database error", http.StatusInternalServerError)
		log.Printf("load candidates: %v", err)
		return
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	fmt.Fprint(w, `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Professional Practice Image Review</title>
<style>
:root {
  color-scheme: light;
  --ink: #1d2430;
  --muted: #667085;
  --line: #d8dde6;
  --panel: #f7f8fb;
  --accent: #2456a6;
  --ok: #126b3a;
  --bad: #9d2424;
}
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: var(--ink);
  background: #fff;
}
header {
  border-bottom: 1px solid var(--line);
  padding: 20px max(24px, calc((100vw - 1220px) / 2));
}
main {
  max-width: 1220px;
  margin: 0 auto;
  padding: 24px;
}
h1 {
  font-size: 24px;
  margin: 0 0 6px;
}
.meta, .empty, .small {
  color: var(--muted);
  font-size: 14px;
}
.candidate {
  border: 1px solid var(--line);
  border-radius: 8px;
  margin: 0 0 24px;
  overflow: hidden;
}
.candidate-header {
  background: var(--panel);
  border-bottom: 1px solid var(--line);
  display: grid;
  gap: 8px;
  grid-template-columns: 1fr auto;
  padding: 14px 16px;
}
.candidate h2 {
  font-size: 18px;
  margin: 0;
}
.status {
  align-self: start;
  border: 1px solid var(--line);
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  padding: 4px 10px;
  text-transform: uppercase;
}
.status-approved { color: var(--ok); }
.status-rejected { color: var(--bad); }
.details {
  display: grid;
  gap: 8px;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  padding: 14px 16px;
}
.detail {
  font-size: 14px;
}
.detail strong {
  display: block;
  font-size: 12px;
  letter-spacing: .02em;
  text-transform: uppercase;
  color: var(--muted);
}
.images {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  padding: 0 16px 16px;
}
figure {
  margin: 0;
}
figcaption {
  color: var(--muted);
  font-size: 13px;
  margin: 0 0 6px;
}
img {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 6px;
  box-sizing: border-box;
  display: block;
  height: auto;
  max-width: 100%;
  width: 100%;
}
.review {
  border-top: 1px solid var(--line);
  display: grid;
  gap: 10px;
  padding: 14px 16px 16px;
}
textarea {
  border: 1px solid var(--line);
  border-radius: 6px;
  box-sizing: border-box;
  font: inherit;
  min-height: 74px;
  padding: 8px;
  width: 100%;
}
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
button {
  border: 1px solid var(--line);
  border-radius: 6px;
  cursor: pointer;
  font: inherit;
  font-weight: 600;
  padding: 8px 12px;
}
button[value="approve"] {
  background: #e8f5ee;
  border-color: #9fd5b9;
  color: var(--ok);
}
button[value="reject"] {
  background: #faecec;
  border-color: #ebb2b2;
  color: var(--bad);
}
button[value="comment"] {
  background: #eef3fb;
  border-color: #afc2e4;
  color: var(--accent);
}
.comment {
  background: #fffdf4;
  border: 1px solid #eadf9f;
  border-radius: 6px;
  font-size: 14px;
  margin: 0 16px 14px;
  padding: 10px;
}
@media (max-width: 900px) {
  .images { grid-template-columns: 1fr; }
  .candidate-header { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<header>
<h1>Professional Practice Image Review</h1>
<div class="meta">Approve final images, reject unsuitable candidates, or leave comments for the next generation pass.</div>
</header>
<main>
`)

	if len(items) == 0 {
		fmt.Fprint(w, `<p class="empty">No image candidates have been registered yet.</p>`)
	}

	for _, item := range items {
		a.renderCandidate(w, item)
	}

	fmt.Fprint(w, `</main></body></html>`)
}

func (a *app) renderCandidate(w http.ResponseWriter, item candidate) {
	statusClass := "status-" + strings.ToLower(item.Status)
	fmt.Fprintf(w, `<section class="candidate" id="%s">`, html.EscapeString(urlFragment(item.ID)))
	fmt.Fprint(w, `<div class="candidate-header">`)
	fmt.Fprintf(w, `<div><h2>%s</h2><div class="small">%s</div></div>`, h(item.Brief), h(item.ID))
	fmt.Fprintf(w, `<div class="status %s">%s</div>`, h(statusClass), h(item.Status))
	fmt.Fprint(w, `</div>`)

	fmt.Fprint(w, `<div class="details">`)
	detail(w, "Target", item.TargetPath)
	detail(w, "Topic", item.TopicPath)
	detail(w, "Slide", item.SlideRef)
	detail(w, "Batch", item.BatchID)
	if item.ReviewedBy.Valid || item.ReviewedAt.Valid {
		detail(w, "Reviewed", strings.TrimSpace(item.ReviewedBy.String+" "+item.ReviewedAt.String))
	}
	fmt.Fprint(w, `</div>`)

	if strings.TrimSpace(item.Prompt) != "" {
		fmt.Fprintf(w, `<div class="comment"><strong>Prompt/spec:</strong> %s</div>`, h(item.Prompt))
	}
	if strings.TrimSpace(item.ReviewComment) != "" {
		fmt.Fprintf(w, `<div class="comment"><strong>Review comment:</strong> %s</div>`, h(item.ReviewComment))
	}

	fmt.Fprint(w, `<div class="images">`)
	imageFigure(w, "Generated image", item.CandidateURL)
	imageFigure(w, "Current slide", item.CurrentSlideURL)
	imageFigure(w, "Proposed slide", item.ProposedSlideURL)
	fmt.Fprint(w, `</div>`)

	fmt.Fprintf(w, `<form class="review" method="post" action="./image-review.cgi#%s">`, html.EscapeString(urlFragment(item.ID)))
	fmt.Fprintf(w, `<input type="hidden" name="id" value="%s">`, h(item.ID))
	fmt.Fprintf(w, `<textarea name="comment" placeholder="Comment for a regeneration pass">%s</textarea>`, h(item.ReviewComment))
	fmt.Fprint(w, `<div class="actions">`)
	fmt.Fprint(w, `<button type="submit" name="action" value="approve">Approve</button>`)
	fmt.Fprint(w, `<button type="submit" name="action" value="reject">Reject</button>`)
	fmt.Fprint(w, `<button type="submit" name="action" value="comment">Comment</button>`)
	fmt.Fprint(w, `</div></form>`)
	fmt.Fprint(w, `</section>`)
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

func detail(w http.ResponseWriter, label string, value string) {
	if strings.TrimSpace(value) == "" {
		value = "-"
	}
	fmt.Fprintf(w, `<div class="detail"><strong>%s</strong>%s</div>`, h(label), h(value))
}

func imageFigure(w http.ResponseWriter, label string, src string) {
	if strings.TrimSpace(src) == "" {
		fmt.Fprintf(w, `<figure><figcaption>%s</figcaption><div class="empty">Missing preview</div></figure>`, h(label))
		return
	}
	fmt.Fprintf(w, `<figure><figcaption>%s</figcaption><img src="%s" alt="%s"></figure>`, h(label), h(src), h(label))
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

func urlFragment(value string) string {
	replacer := strings.NewReplacer(
		" ", "-",
		"/", "-",
		".", "-",
		"_", "-",
		":", "-",
	)
	return replacer.Replace(value)
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
