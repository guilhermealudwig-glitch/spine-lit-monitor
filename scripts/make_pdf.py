#!/usr/bin/env python3
"""make_pdf.py <input.md> <output.pdf> — markdown → PDF via python markdown + weasyprint.

Linux-side replacement for make_pdf.sh (which targets Windows/Edge).
Falls back gracefully: if weasyprint is missing, writes .html and exits 0 with a WARN.
"""
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit("usage: make_pdf.py <input.md> <output.pdf>")
    inp, out = Path(sys.argv[1]), Path(sys.argv[2])
    if not inp.is_file():
        sys.exit(f"input not found: {inp}")

    try:
        import markdown
        import weasyprint
    except ImportError:
        html = out.with_suffix(".html")
        html.write_text(
            f"<!doctype html><meta charset=utf-8><pre>{inp.read_text(encoding='utf-8')}</pre>",
            encoding="utf-8",
        )
        print(f"WARN: weasyprint/markdown unavailable — wrote HTML only: {html}")
        return

    body = markdown.markdown(inp.read_text(encoding="utf-8"), extensions=["extra"])
    css = (
        "body{font-family:'DejaVu Sans',sans-serif;margin:2cm;font-size:10pt;"
        "line-height:1.45}h1{font-size:16pt}h2{font-size:13pt}"
        "p{margin:6px 0;text-align:justify}a{color:#1a4d8f;text-decoration:none}"
    )
    html = f"<!doctype html><meta charset='utf-8'><style>{css}</style><body>{body}</body>"
    weasyprint.HTML(string=html).write_pdf(str(out))
    print(f"PDF ok: {out}")


if __name__ == "__main__":
    main()
