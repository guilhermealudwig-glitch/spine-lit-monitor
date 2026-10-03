# Revisão Literária Semanal — Cirurgia de Coluna (Hermes cron job)

Job autônomo do [Hermes Agent](https://hermes-agent.nousresearch.com/docs) que roda todo
domingo às 8h: busca no PubMed os artigos da semana sobre cirurgia de coluna, tria por
relevância e entrega um digest em português (markdown + PDF) no chat.

**Foco:** cirurgia minimamente invasiva (MIS), endoscopia biportal/UBE, doença degenerativa
lombar, deformidade do adulto, fusões (TLIF/ALIF/LLIF/OLIF).

## Arquivos

| Arquivo | Papel |
|---|---|
| `PROMPT.md` | Instruções completas do job (o prompt do cron é só "leia este arquivo") |
| `SKILL.md` | Skill `surgical-literature-monitor` (instalar em `~/.hermes/skills/` ou no perfil Hermes) |
| `scripts/pubmed_search.py` | Busca PubMed (E-utilities) por tópico, dedupe, escreve `pubmed_shortlist.tsv` |
| `scripts/make_pdf.sh` | Digest markdown → PDF (pandoc ou Edge headless; fallback HTML) |
| `literature-monitor/` | Saídas: `digest-YYYY-MM-DD.md` / `.pdf` (estado: dedupe contra semanas anteriores) |

## Instalar no Hermes (desktop ou VM)

```bash
# 1. Skill no perfil
cp SKILL.md ~/.hermes/skills/research/surgical-literature-monitor/SKILL.md
# (ou, no Windows/perfil Hermes:
#  cp SKILL.md ~/AppData/Local/hermes/profiles/<profile>/skills/research/surgical-literature-monitor/SKILL.md)

# 2. Criar o job (de dentro de uma sessão Hermes, com gateway rodando)
hermes cron add spine-lit-monitor \
    --schedule "0 8 * * 0" \
    --workdir <diretorio-deste-repo> \
    --file PROMPT.md
```

Alternativa: pelo próprio Hermes — *"crie um cron job `every sunday 8am` com a skill
`surgical-literature-monitor` e o prompt 'Leia PROMPT.md no workdir e execute à risca'"*.

## Dependências

- Rede: PubMed E-utilities (sem chave, usa rate limit público)
- PDF: `pandoc` (qualquer OS) ou Microsoft Edge headless (Windows); sem nenhum dos dois, fica HTML
- Python 3.10+ apenas stdlib para a busca

## Notas

- Se o PubMed estiver inacessível, o job reporta a falha — nunca inventa artigos.
- Dedupe: cada execução compara PMUIDs com `literature-monitor/all_ids.txt` do ciclo anterior.
