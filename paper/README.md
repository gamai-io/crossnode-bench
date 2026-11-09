# Preprint

**Evidence-Gated Agent Execution: Measuring and Preventing False Success in Tool-Using LLM Agents**  
v0.2.0 — 2026-11-09 — preprint draft, not peer reviewed.

Files:
- `preprint.md` — source
- `preprint.pdf` — rendered PDF
- `preprint.html` — intermediate HTML
- `style.css` — print styling

Build:

```bash
cd paper
pandoc preprint.md -s --css style.css -o preprint.html
weasyprint preprint.html preprint.pdf
```

The draft states its limitations explicitly:
- 25,600 cross-node probes are a **controlled** detection-recall test, not a field rate.
- The guard blind set is 40 items and self-authored.
- LUMI guarded rerun is **1/10,000 (0.01%) — FAIL**; earlier 0/10k was not reproduced.
- No independent audit; raw per-trial logs are not included in the public pack.

Data: `../dataset/` and `../dataset/DATASHEET.md`.
