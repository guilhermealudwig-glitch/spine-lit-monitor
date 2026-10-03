#!/usr/bin/env python3
"""PubMed query helpers for the weekly spine surgery literature monitor.

Usage (inside the cron agent session):
    python scripts/pubmed_search.py [--days 7]
Prints a deduped list of PMUIDs per topic to stdout, and writes
abstracts for the shortlist to pubmed_abstracts.txt in the workdir.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

TOPICS = {
    "MIS": '("minimally invasive" OR MIS OR tubular) AND (lumbar OR spine) AND surgery',
    "UBE": '"biportal endoscopic spinal surgery" OR UBE',
    "Endoscopic spine surgery": "endoscopic spine surgery",
    "Lumbar degenerative": "lumbar degenerative disease AND (stenosis OR spondylolisthesis OR \"disc herniation\")",
    "Adult deformity": "adult spinal deformity AND (scoliosis OR \"sagittal alignment\")",
    "Fusion techniques": "transforaminal lumbar interbody fusion OR TLIF OR ALIF OR LLIF OR OLIF",
}


def esearch(term: str, days: int, retmax: int = 60) -> list[str]:
    params = {
        "db": "pubmed",
        "term": term,
        "retmax": retmax,
        "retmode": "json",
        "datetype": "edat",
        "reldate": days,
        "sort": "date",
    }
    url = f"{EUTILS}/esearch.fcgi?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    return data["esearchresult"].get("idlist", [])


def esummary(ids: list[str]) -> dict:
    if not ids:
        return {}
    url = f"{EUTILS}/esummary.fcgi?db=pubmed&id={','.join(ids)}&retmode=json"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)["result"]


def fetch_abstract(pmid: str) -> str:
    url = f"{EUTILS}/efetch.fcgi?db=pubmed&id={pmid}&rettype=abstract&retmode=text"
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main() -> None:
    days = 7
    if "--days" in sys.argv:
        days = int(sys.argv[sys.argv.index("--days") + 1])

    seen: dict[str, str] = {}
    per_topic: dict[str, list[str]] = {}
    for topic, term in TOPICS.items():
        try:
            ids = esearch(term, days)
        except Exception as e:
            print(f"ERROR esearch {topic}: {e}", file=sys.stderr)
            continue
        per_topic[topic] = ids
        for pmid in ids:
            seen.setdefault(pmid, topic)

    if not seen:
        print("NO_RESULTS (PubMed unreachable or zero hits) — report failure, never fabricate.")
        sys.exit(2)

    summary = esummary(list(seen))
    lines = []
    for pmid, topic in sorted(seen.items()):
        doc = summary.get(pmid, {})
        title = doc.get("title", "?")
        journal = (doc.get("source") or "?")
        date = (doc.get("pubdate") or "?")
        authors = doc.get("authors") or []
        first = authors[0]["name"] if authors else "?"
        lines.append(f"{pmid}\t{topic}\t{first} et al.\t{title}\t{journal}\t{date}")

    print(f"# PMUIDs fetched: {len(seen)} across {len(per_topic)} topics")
    print("\n".join(lines))

    Path("pubmed_shortlist.tsv").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
