# CrossNode-Bench evidence archive — v1.4.0 (recount guide)

Source: Zenodo record 10.5281/zenodo.24092188 (concept 10.5281/zenodo.23920505).

## Sadrzaj
| Fajl | Sta je | SHA-256 |
|---|---|---|
| evidence_chained.jsonl | 12,344 raw evidence zapisa, hash-chain + Merkle (v1.2.2 run) | e79a43f4a51ee94fb70a8f82eca7e01e71ebc6b5766aa898b93a8cd6ee10b97e |
| manifest.json | chain manifest (records=12344, merkle_root) | a84642af61634ff70745f36c6f9483b2588e89987a954b5910d1d660cc884df8 |
| vultr_honest_evidence.jsonl.gz | real 9-node Vultr fleet, 25,600 honest records | 960b661424b2c2a147ad2179d15aeab357a34ce6e45b3e8564066fe824e87049 |
| vultr_liar_evidence.jsonl.gz | controlled liar run, 28,800 records (400 false successes) | 372851594aae1ee554a46b817a0c466fad3edda4f3e9a0ecff2df9a081789674 |
| vultr_aggregate_2026-11-09.json | agregat koji treba da se poklopi sa prebrojavanjem | (u SHA256SUMS.txt) |

## Nezavisno prebrojavanje (bez naseg koda)

    # 1) hash-chain + Merkle
    python3 tools/evidence.py verify --in evidence_chained.jsonl --manifest manifest.json
    # ocekivano: {"merkle_root":"eda02d9c...d11d2d","ok":true,"records":12344}

    # 2) prebroj tvrdnje i false success iz raw JSONL
    python3 - <<'PY'
    import json
    n=fs=claims=cov=0
    for line in open('evidence_chained.jsonl'):
        r=json.loads(line); n+=1
        if r.get('claim_ok'): claims+=1
        if r.get('truth_ok') is not None: cov+=1
        if r.get('claim_ok') and r.get('truth_ok') is False: fs+=1
    print(n, claims, fs, cov/n)
    PY
    # ocekivano: 12344 11206 53 1.0

    # 3) Vultr flota iz gz
    python3 - <<'PY'
    import gzip,json
    for f in ('vultr_honest_evidence.jsonl.gz','vultr_liar_evidence.jsonl.gz'):
        n=fs=0
        for line in gzip.open(f,'rt'):
            r=json.loads(line); n+=1
            if r.get('claim_ok') and r.get('truth_ok') is False: fs+=1
        print(f,n,fs)
    PY
    # ocekivano: vultr_honest_evidence.jsonl.gz 25600 0
    #            vultr_liar_evidence.jsonl.gz   28800 400

## Granica (vazno za tekst predloga)
- Raw logs za kontrolisani cross-node 25,600 run NISU u javnom packu (samo aggregate + tasks.json).
- Raw JSONL koji JESTE u arhivi: evidence_chained.jsonl (12,344) + Vultr honest/liar (25,600 + 28,800).
- Zato recenica smije da se odnosi SAMO na ove tri grupe, ne na svih 25,600 cross-node probe-a.
