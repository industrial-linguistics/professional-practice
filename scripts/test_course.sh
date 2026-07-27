#!/usr/bin/env bash
set -euo pipefail

python3 scripts/validate_html_course.py
python3 scripts/validate_textbook_sources.py
python3 scripts/validate_narratives.py
python3 scripts/report_narrative_mismatches.py
python3 scripts/build_textbook.py
python3 scripts/build_elearning.py
python3 scripts/validate_html_course.py --check-output
python3 scripts/build_scorm.py --skip-elearning-build
python3 scripts/validate_scorm_package.py

secret_file="state/secrets/image-review-basic-auth.env"
if [[ -f "$secret_file" ]]; then
  python3 scripts/validate_html_course.py --auth-smoke --secret-file "$secret_file"
else
  echo "Skipping auth smoke test: $secret_file not found"
fi
