# Cover message — manuscript v1.2

## EN

**Subject:** Manuscript v1.2 — corrections after your comments, with the recount for every number

Dear [Name],

thank you for the detailed comments. I have worked through all ten points, and in doing so found two further problems that are now corrected as well. v1.2 replaces v1.1 in full; the point-by-point answer is in `RESPONSE_TO_REVIEW.md`.

What changed, in short:

1. **The "0/10,000 under the gate" claim is gone.** The only gated denominator is 30,798. All 24 runs are now listed (Appendix A.2), including the 1,000-record runs with 7, 1 and 0 false successes, so nothing depends on the choice of run.
2. **The 10,000-record split is explained instead of implied.** The two runs with zero contain 4,167 gated records each; the single false success in the other two runs lies outside the gated case types.
3. **New analysis, because the gate is assigned by case type.** Five of the twelve case types are gated. The same five case types give **5,495 false successes in 11,353 ungated records and none in 30,798 gated records**, and a matched pair of 10,000-record runs on the same model and day with identical prompt hashes gives **1,683 against 0**. This replaces the record-level split as the substantive result. It is presented as quasi-experimental, with §5.5 stating that run-level factors are not controlled and that a paired on/off run is the next step.
4. **Mistral is separated.** 168 gated records → 0 false successes; 232 unguarded → 198. The `false_note` values are `contains`, `exact` and `refuse` — answer-check failures, not tool-execution lies — so the 49.5% is excluded from cross-model statements.
5. **The liar test is labelled as simulated** (`MockLiar`) and no longer reads as a result about real agents.
6. **No ratio over the 12,344 chained set** is reported anywhere; it is integrity-only, and §3.1 says so. The 0.43% and 36,550 figures appear in no version.
7. **Identifiers resolved.** The paper now cites the artifact by concept DOI 10.5281/zenodo.23920505 with v1.6.3 (documentation-only change, so the data digests still hold) and lists v1.6.2 and v1.6.0 as previous versions. The manuscript is deposited as a new preprint version, not as an attachment to a Software record.
8. **The dataset README is rewritten in English**, with a gated column, a per-case table and the mapping to the numbers in the paper; the Bosnian note is gone. Same content in the repository and in the artifact.
9. **Data protection checked**: six e-mail-shaped strings in 101,140 text fields, all placeholders; no identification numbers; no telephone numbers. Model licences are declared per model, and a hash-and-length variant without raw Llama text reproduces every count if required.
10. **Aggregate-only material stays aggregate-only** and is declared as such in three places.

Tested commands: `python3 recount.py --honest … --liar … --trust … --trust2 … --lumi …` prints every number in Sections 4.1–4.5 and Appendix A.2 and matches `recount_output.json`.

Attached: `manuscript_v1.2.pdf`, `MANUSCRIPT.md`, `RESPONSE_TO_REVIEW.md`, `recount.py`, `recount_output.json`, `EVIDENCE_LINKS.md`, `CHANGELOG_v1.2.md`.

Best regards,
Renato Šuster
GAMA TRADE d.o.o. / gamAI, Usora, Bosnia and Herzegovina
renato@gamatrade.ba · +387 63 277 572

---

## BS

**Naslov:** Rad v1.2 — ispravke po tvojim primjedbama, sa ponovnim obračunom za svaki broj

Poštovani [ime],

hvala na detaljnim primjedbama. Prošao sam svih deset tačaka i usput našao još dva problema, pa su i oni ispravljeni. v1.2 u potpunosti zamjenjuje v1.1; odgovor po tačkama je u `RESPONSE_TO_REVIEW.md`.

Ukratko:

1. **Tvrdnja „0/10.000 pod gate-om" je uklonjena.** Jedini imenilac je 30.798. Svih 24 runa su sada u Appendix A.2, uključujući 1.000-runove sa 7, 1 i 0 lažnih uspjeha — ništa ne zavisi od izbora runa.
2. **Podjela 10.000 je objašnjena, ne implicirana.** Dva runa sa nulom imaju po 4.167 gated zapisa; jedini lažni uspjeh u druga dva runa je van gated tipova.
3. **Nova analiza, jer se gate dodjeljuje po tipu zadatka.** Gated je 5 od 12 tipova. Istih pet tipova daje **5.495 lažnih uspjeha u 11.353 negated zapisa i nijedan u 30.798 gated**, a upareni par 10.000-runova (isti model, isti dan, isti `prompt_sha`) daje **1.683 prema 0**. To zamjenjuje record-level podjelu kao glavni rezultat; u §5.5 stoji da je kvazi-eksperiment i da upareni on/off run tek slijedi.
4. **Mistral je izdvojen.** 168 gated → 0; 232 negated → 198. `false_note` je `contains`, `exact`, `refuse` — promašaji provjere odgovora, ne laganje agenta — pa se 49,5% ne koristi u cross-model tvrdnjama.
5. **Liar test je označen kao simuliran** (`MockLiar`), više ne izgleda kao rezultat o stvarnim agentima.
6. **Nijedan odnos nad 12.344 zapisa** se ne navodi; taj set služi samo za integritet. Brojevi 0,43% i 36.550 ne postoje ni u jednoj verziji.
7. **Identifikatori riješeni.** Rad citira koncept DOI 10.5281/zenodo.23920505 i v1.6.3 (mijenja se samo dokumentacija, pa digesti podataka važe), a v1.6.2 i v1.6.0 su navedeni kao prethodne verzije. Rad ide kao nova verzija preprina, ne kao prilog Software zapisu.
8. **README dataseta je na engleskom**, sa kolonom gated, tabelom po tipu zadatka i mapiranjem na brojeve iz rada; bosanski TODO je izbrisan. Isti sadržaj u repou i u artefaktu.
9. **Podaci provjereni:** šest e-mail stringova u 101.140 polja, svi placeholderi; nula matičnih brojeva; nula telefona. Licence modela su navedene; hash+len varijanta bez Llama teksta reprodukuje svaki broj ako zatreba.
10. **Agregati ostaju agregati** i tako su deklarisani na tri mjesta.

Provjereno: `python3 recount.py --honest … --liar … --trust … --trust2 … --lumi …` daje svaki broj iz §4.1–4.5 i Appendix A.2 i poklapa se sa `recount_output.json`.

Prilozi: `manuscript_v1.2.pdf`, `MANUSCRIPT.md`, `RESPONSE_TO_REVIEW.md`, `recount.py`, `recount_output.json`, `EVIDENCE_LINKS.md`, `CHANGELOG_v1.2.md`.

Srdačan pozdrav,
Renato Šuster
