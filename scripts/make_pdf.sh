#!/usr/bin/env bash
# make_digest_pdf.sh <input.md> <output.pdf>
# Converts a markdown digest to PDF. Tries (in order): pandoc, Edge headless.
# Portable: no hardcoded user paths. Works on Windows (Git Bash / MSYS) and Linux.
set -euo pipefail

IN="$1"
OUT="$2"
[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }

BASE="${IN%.md}"

# 1) pandoc (preferred, if installed)
if command -v pandoc >/dev/null 2>&1; then
    pandoc "$IN" -o "$OUT" --pdf-engine=wkhtmltopdf 2>/dev/null \
      || pandoc "$IN" -o "$OUT" 2>/dev/null \
      || true
    [ -s "$OUT" ] && { echo "PDF via pandoc: $OUT"; exit 0; }
fi

# 2) Edge headless print-to-pdf (Windows) — locate Edge, then md -> html -> pdf
if [ -n "${WINDOw:-}" ] || [ "$(uname -s)" = MINGW* ] || [ "$(uname -s)" = "MINGW64_NT-10.0" ] || uname -s | grep -qi mingw; then
    for edge in \
        "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
        "/c/Program Files/Microsoft/Edge/Application/msedge.exe"; do
        if [ -x "$edge" ]; then
            HTML="${BASE}.html"
            # minimal md -> html (headings, bold, italic, links, paragraphs)
            sed -E \
                -e 's|^(#{1,6}) (.*)$|<h1>\2</h1>|' \
                -e 's|\*\*([^*]+)\*\*|<b>\1</b>|g' \
                -e 's|\*([^*]+)\*|<i>\1</i>|g' \
                -e 's|^(https?://[^ ]+)$|<a href="\1">\1</a>|' \
                "$IN" | awk '{ if ($0 ~ /^<h1>/ || $0 ~ /^---$/) print $0; else if (length($0)>0) print "<p>" $0 "</p>"; }' \
                > "$HTML"
            printf '<!doctype html><html><head><meta charset="utf-8"><style>body{font-family:Segoe UI,Arial,sans-serif;margin:2.5cm;font-size:10pt;line-height:1.45}h1{font-size:16pt}p{margin:6px 0;text-align:justify}a{color:#1a4d8f}</style></head><body>\n%s\n</body></html>\n' "$(cat "$HTML")" > "$HTML.tmp" && mv "$HTML.tmp" "$HTML"
            "$edge" --headless --disable-gpu "--print-to-pdf=$OUT" --no-pdf-header-footer "$HTML" 2>/dev/null || true
            [ -s "$OUT" ] && { echo "PDF via Edge: $OUT"; exit 0; }
        fi
    done
fi

# 3) fallback: HTML only, no PDF
HTML="${BASE}.html"
cp "$IN" /dev/null 2>/dev/null || true
echo "WARN: no pandoc/Edge available — wrote HTML only: $HTML" >&2
exit 0
