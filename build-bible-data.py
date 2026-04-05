#!/usr/bin/env python3
"""Regenerate bible-data.js after editing the bible/ chapter .txt files."""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bible")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bible-data.js")


def main():
    data = {}
    for book in sorted(os.listdir(ROOT)):
        bp = os.path.join(ROOT, book)
        if not os.path.isdir(bp):
            continue
        book_data = {}
        for fname in os.listdir(bp):
            if not (fname.startswith("Chapter ") and fname.endswith(".txt")):
                continue
            fp = os.path.join(bp, fname)
            with open(fp, encoding="utf-8") as f:
                verses = [line.strip() for line in f if line.strip()]
            book_data[fname] = verses
        if book_data:
            data[book] = book_data
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8") as out:
        out.write("window.__BIBLE_DATA__=")
        out.write(payload)
        out.write(";\n")
    print(f"Wrote {OUT} ({len(data)} books, {os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
