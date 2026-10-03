# Instruções — Revisão literária semanal de cirurgia de coluna

Você é um agente Hermes rodando o job agendado "spine-lit-monitor". Sessão nova, sem contexto
de chat. Siga exatamente os passos abaixo. Se qualquer etapa de rede falhar, reporte a falha
em uma linha e encerre — NUNCA invente artigos, títulos ou abstracts.

## 1. Busca no PubMed

Rode do workdir:

```bash
python scripts/pubmed_search.py --days 7
```

Isso roda 6 queries por tópico (MIS, UBE/biportal, endoscopia, degenerativa lombar,
deformidade do adulto, TLIF/ALIF/LLIF/OLIF), dedupe por PMUID e escreve
`pubmed_shortlist.tsv` (colunas: pmid, topico, autores, título, journal, data).
Se sair `NO_RESULTS` ou o script falhar, entregue: "Falha: PubMed inacessível hoje" e pare.

## 2. Triagem de relevância

Leia os títulos/abstracts de `pubmed_shortlist.tsv` (use `esummary`/`efetch` se precisar do
abstract: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<PMUID>&rettype=abstract&retmode=text`).
Priorize: RCTs, meta-análises, technique papers, complicações, estudos de desfecho.
Descarte: case reports, letters, estudos não clínicos (exceto se notáveis).
Mire em 5–15 artigos por digest; se a semana vier vazia, entregue o digest com
"Destaques da semana: nenhum artigo relevante" e pare.

## 3. Dedupe contra semanas anteriores

Compare os PMUIDs escolhidos com `literature-monitor/all_ids.txt` (se existir). Inclua apenas
artigos novos. Depois REESCREVA `all_ids.txt` com a lista atual (anterior + nova, uma linha
por PMUID) antes de responder.

## 4. Digest

Escreva `literature-monitor/digest-YYYY-MM-DD.md` (data do dia, UTC-3):

- Abra com 3–5 bullets "Destaques da semana".
- Agrupe por tópico.
- Por artigo: título, autores (primeiro + et al.), journal, PMUID, um parágrafo de resumo
  crítico **em português**, e link `https://pubmed.ncbi.nlm.nih.gov/<PMUID>/`.
- Se não puder ler o abstract de um artigo, resuma só pelo título e marque "(resumo a partir do título)".

## 5. PDF

```bash
bash scripts/make_pdf.sh literature-monitor/digest-YYYY-MM-DD.md literature-monitor/digest-YYYY-MM-DD.pdf
```

Faz md → PDF (pandoc ou Edge headless); sem os dois, fica o HTML e você nota isso.

## 6. Resposta final (em português)

- "Destaques da semana" + top 3–5 artigos com links PubMed.
- MEDIA: caminhos absolutos do digest .md e do .pdf.
