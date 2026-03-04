#!/usr/bin/env python3
"""
Standalone validation script for CSE572 Homework 0.
Run this after generating single.txt to verify it meets all requirements.
"""

def validate_dataset(filepath="single.txt"):
    valid_genres = {
        "pop", "rock", "hiphop", "rb", "country", "jazz", "edm",
        "classical", "kpop", "latin", "folk", "metal", "reggae", "other"
    }

    errors = []
    warnings = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: File '{filepath}' not found!")
        return False

    print(f"Validating: {filepath}")
    print("=" * 50)
    print(f"Total lines: {len(lines)} (expected: 50)")

    if len(lines) != 50:
        warnings.append(f"Expected 50 lines, got {len(lines)}")

    seen_titles = set()

    for i, line in enumerate(lines):
        line_num = i + 1
        parts = line.strip().split("||")

        # Check field count (must be exactly 8)
        if len(parts) != 8:
            errors.append(f"Line {line_num}: Wrong field count ({len(parts)} instead of 8)")
            continue

        rank, title, artist, r_date, genre, lang, lyrics, source = parts

        # Check rank is sequential
        try:
            if int(rank) != line_num:
                warnings.append(f"Line {line_num}: Rank is {rank}, expected {line_num}")
        except ValueError:
            errors.append(f"Line {line_num}: Invalid rank '{rank}'")

        # Check for duplicates
        title_key = (title.lower(), artist.lower())
        if title_key in seen_titles:
            errors.append(f"Line {line_num}: Duplicate entry '{title}' by '{artist}'")
        seen_titles.add(title_key)

        # Check date format and year
        if len(r_date) < 4:
            errors.append(f"Line {line_num}: Invalid date format '{r_date}'")
        elif r_date < "2025-01-01":
            errors.append(f"Line {line_num}: Date {r_date} is before 2025")

        # Check genre validity
        genres = genre.split(",")
        for g in genres:
            if g.strip() not in valid_genres:
                errors.append(f"Line {line_num}: Invalid genre '{g}'. Must be one of: {', '.join(sorted(valid_genres))}")

        # Check lyrics for illegal characters
        illegal_chars = set("[]{}|\\")
        found_illegal = [c for c in lyrics if c in illegal_chars]
        if found_illegal:
            errors.append(f"Line {line_num}: Lyrics contain illegal characters: {set(found_illegal)}")

        # Check lyrics length
        if len(lyrics.strip()) < 50:
            warnings.append(f"Line {line_num}: Very short lyrics ({len(lyrics)} chars) - possibly instrumental?")

        # Check source URL
        if not source.startswith("http"):
            warnings.append(f"Line {line_num}: Source doesn't look like a URL: {source[:50]}...")

    # Print results
    print()
    if errors:
        print("ERRORS (must fix):")
        for err in errors:
            print(f"  [X] {err}")

    if warnings:
        print("\nWARNINGS (review recommended):")
        for warn in warnings:
            print(f"  [!] {warn}")

    if not errors and not warnings:
        print("\n[OK] VALIDATION PASSED! File is ready for submission.")
        return True
    elif not errors:
        print("\n[OK] No critical errors. Review warnings above.")
        return True
    else:
        print(f"\n[FAIL] Found {len(errors)} error(s). Please fix before submitting.")
        return False


if __name__ == "__main__":
    import sys
    filepath = sys.argv[1] if len(sys.argv) > 1 else "single.txt"
    validate_dataset(filepath)
