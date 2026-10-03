---
name: surgical-literature-monitor
description: Use for the weekly Sunday spine surgery literature review.
---

# Weekly spine surgery literature monitor

Goal: produce a weekly digest of relevant spine surgery articles for Guilherme (PGY-5 neurosurgery, HSJ/Porto Alegre — focus: minimally invasive spine surgery, biportal endoscopy, degenerative disease, deformity).

## Search strategy
1. Search PubMed (via E-utilities esearch/esummary, e.g. `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=50&datetype=edat&reldate=7&term=...`) for the last 7 days. Run separate queries per topic and dedupe by PMUID:
   - `("minimally invasive" OR MIS OR "tubular") AND (lumbar OR spine) AND surgery`
   - `biportal endoscopic spinal surgery OR UBE`
   - `endoscopic spine surgery` (uniportal/biportal, discectomy, laminectomy, fusion)
   - `lumbar degenerative disease` (stenosis, spondylolisthesis, disc herniation)
   - `adult spinal deformity` (ASD, scoliosis surgery, sagittal alignment)
   - `transforaminal lumbar interbody fusion OR TLIF OR ALIF OR LLIF OR OLIF`
2. Fetch titles/abstracts (esummary + efetch abstract for shortlisted papers).
3. Filter for relevance — prioridade na leitura: RCTs, meta-análises, technique papers, complicações, estudos de desfecho; drop case reports, letters, estudos não clínicos (exceto se notáveis). Mire em 5–15 artigos por digest.
4. Check the job's previous output (continuity) — do not repeat papers already included in a prior week.

## Output
1. Write a markdown digest in `~/AppData/Local/hermes/profiles/hermes-guilherme/literature-monitor/` named `digest-YYYY-MM-DD.md`: per paper — title, authors (first + et al), journal, PMUID, one-paragraph critical summary in Portuguese, and PubMed link `https://pubmed.ncbi.nlm.nih.gov/<PMUID>/`. Group by topic; open with a 3-5 bullet 'Destaques da semana'.
2. Convert the digest to PDF in the same folder (same name, .pdf) — e.g. via pandoc, or wkhtmltopdf/weasyprint; if none available, generate a clean HTML file and note it.
3. Final chat response: the 'Destaques da semana' + top 3-5 papers with PubMed links, and MEDIA: paths to the digest and PDF. Respond in Portuguese.

If the network fails or PubMed is unreachable, report the failure plainly — never fabricate articles.