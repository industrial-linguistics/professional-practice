#!/usr/bin/env python3
"""
Pre-generation content validation
Level 1: Fast validation before any generation happens
"""

import sys
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
import json

class ValidationResult:
    def __init__(self, passed: bool, message: str = "", warnings: List[str] = None):
        self.passed = passed
        self.message = message
        self.warnings = warnings or []

    def __bool__(self):
        return self.passed

def count_words(text: str) -> int:
    """Count words in text"""
    return len(text.split())

def validate_markdown_syntax(file_path: Path) -> ValidationResult:
    """Basic markdown syntax validation"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for common issues
        warnings = []

        # Check for unclosed code blocks
        code_blocks = content.count('```')
        if code_blocks % 2 != 0:
            return ValidationResult(False, f"Unclosed code block in {file_path}")

        # Check for broken links
        broken_links = re.findall(r'\[([^\]]+)\]\(\s*\)', content)
        if broken_links:
            warnings.append(f"Empty links found: {broken_links}")

        return ValidationResult(True, warnings=warnings)

    except Exception as e:
        return ValidationResult(False, f"Failed to read {file_path}: {e}")

def count_marp_slides(slides_file: Path) -> int:
    """Count slides in Marp markdown file"""
    with open(slides_file, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    slide_count = 0
    front_matter_count = 0
    in_front_matter = False

    for line in lines:
        trimmed = line.strip()

        if trimmed == '---':
            if front_matter_count < 2:
                front_matter_count += 1
                if front_matter_count == 1:
                    in_front_matter = True
                elif front_matter_count == 2:
                    in_front_matter = False
            elif not in_front_matter:
                slide_count += 1

    # Add 1 for the first slide
    if slide_count > 0 or len(content) > 0:
        slide_count += 1

    return slide_count

def validate_content_structure(topic_path: Path) -> ValidationResult:
    """Validate content structure and file existence"""

    # Check for required files
    slides_md = topic_path / "slides.md"
    narratives_dir = topic_path / "narratives"

    if not slides_md.exists():
        return ValidationResult(False, f"slides.md not found in {topic_path}")

    if not narratives_dir.exists():
        return ValidationResult(False, f"narratives directory not found in {topic_path}")

    # Find all narrative files
    narrative_files = sorted(narratives_dir.glob("*.md"))

    if len(narrative_files) == 0:
        return ValidationResult(False, f"No narrative files found in {narratives_dir}")

    # Count slides
    try:
        slide_count = count_marp_slides(slides_md)
    except Exception as e:
        return ValidationResult(False, f"Failed to count slides: {e}")

    # Check slide/narrative count match
    if slide_count != len(narrative_files):
        return ValidationResult(
            False,
            f"Mismatch: {slide_count} slides but {len(narrative_files)} narratives in {topic_path}"
        )

    # Validate markdown syntax
    md_result = validate_markdown_syntax(slides_md)
    if not md_result:
        return md_result

    warnings = md_result.warnings

    # Validate each narrative
    for narrative_file in narrative_files:
        md_result = validate_markdown_syntax(narrative_file)
        if not md_result:
            return md_result
        warnings.extend(md_result.warnings)

        # Check word count
        with open(narrative_file, 'r', encoding='utf-8') as f:
            text = f.read()

        word_count = count_words(text)

        if word_count < 20:
            warnings.append(f"{narrative_file.name}: Very short ({word_count} words)")
        elif word_count > 250:
            warnings.append(f"{narrative_file.name}: Very long ({word_count} words, target: 80-120)")

    return ValidationResult(
        True,
        f"✓ {topic_path.name}: {slide_count} slides, {len(narrative_files)} narratives",
        warnings
    )

def validate_topics(topic_paths: List[Path]) -> Dict[str, ValidationResult]:
    """Validate multiple topics"""
    results = {}

    for topic_path in topic_paths:
        if not topic_path.exists():
            results[str(topic_path)] = ValidationResult(False, f"Path not found: {topic_path}")
            continue

        results[str(topic_path)] = validate_content_structure(topic_path)

    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_content.py <topic-path> [<topic-path> ...]")
        print("Example: validate_content.py content/part-01/overview")
        sys.exit(1)

    topic_paths = [Path(p) for p in sys.argv[1:]]
    results = validate_topics(topic_paths)

    # Print results
    print("\n" + "=" * 70)
    print("CONTENT VALIDATION RESULTS")
    print("=" * 70)

    all_passed = True
    total_warnings = 0

    for topic_path, result in results.items():
        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"\n{status} {topic_path}")
        print(f"  {result.message}")

        if result.warnings:
            print(f"  Warnings:")
            for warning in result.warnings:
                print(f"    ⚠️  {warning}")
            total_warnings += len(result.warnings)

        if not result.passed:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print(f"✅ All validations passed")
        if total_warnings > 0:
            print(f"⚠️  {total_warnings} warning(s) found")
    else:
        print("❌ Validation failed")
    print("=" * 70 + "\n")

    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)

if __name__ == '__main__':
    main()
