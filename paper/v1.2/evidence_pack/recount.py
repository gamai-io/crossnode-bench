#!/usr/bin/env python3
"""Independent recount of every number reported in the manuscript.

Inputs (download from the public archive, or point --honest/--liar/--trust/--lumi
at local copies):
  honest : vultr_honest_evidence.jsonl.gz   (Zenodo 24369933 / repo results/...)
  liar   : vultr_liar_evidence.jsonl.gz
  trust  : trust_evidence_25600.jsonl.gz
  trust2 : trust_evidence_19200.jsonl.gz   (optional, 4-node sibling)
  lumi   : lumi_guard_model_101140.jsonl.gz
"""
import argparse, gzip, json, math, os, sys, collections

def rows(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)

def is_fs(r):
    if "false_success" in r:
        return bool(r.get("false_success"))
    return bool(r.get("claim_ok")) and r.get("truth_ok") is False

def pct(v, p):
    v = sorted(v)
    if not v: return None
    i = int(round((len(v) - 1) * p))
    return v[i]

def fleet(path):
    nodes = collections.Counter(); ms = []; fs = 0; fs_nodes = collections.Counter()
    cats = collections.Counter(); n = 0; claims = 0; runs = set(); tasks = set()
    for r in rows(path):
        n += 1
        nodes[r.get("node")] += 1
        runs.add(r.get("run")); tasks.add(r.get("task"))
        if r.get("claim_ok"): claims += 1
        if isinstance(r.get("ms"), (int, float)): ms.append(r["ms"])
        if is_fs(r):
            fs += 1; fs_nodes[r.get("node")] += 1
            cats[(r.get("task"), r.get("note"))] += 1
    return {"records": n, "claims": claims, "nodes": dict(nodes), "n_nodes": len(nodes),
            "false_success": fs, "false_success_nodes": dict(fs_nodes),
            "categories": {f"{k[0]}|{k[1]}": v for k, v in cats.items()},
            "p50_ms": pct(ms, 0.5), "p95_ms": pct(ms, 0.95),
            "runs": len(runs), "tasks": len(tasks),
            "records_per_node": dict(nodes)}

def trust(path):
    n = fs = claims = 0; runs = set(); nodes = set()
    for r in rows(path):
        n += 1; runs.add(r.get("run")); nodes.add(r.get("node"))
        if r.get("claim_ok"): claims += 1
        if is_fs(r): fs += 1
    return {"records": n, "claims": claims, "false_success": fs,
            "runs": len(runs), "nodes": len(nodes)}

def lumi(path):
    per = collections.defaultdict(lambda: {"n": 0, "fs": 0, "guard": 0, "fs_guard": 0, "models": set()})
    tot = {"n": 0, "fs": 0, "guard": 0, "fs_guard": 0}
    by_case = collections.defaultdict(lambda: {"n": 0, "fs": 0, "guard": 0, "fs_guard": 0})
    for r in rows(path):
        rid = r.get("run_id", "?"); d = per[rid]
        c = by_case[r.get("case", "?")]
        g = bool((r.get("harness") or {}).get("guard"))
        fs = is_fs(r)
        for t in (d, c, tot):
            t["n"] += 1
            if g: t["guard"] += 1
            if fs:
                t["fs"] += 1
                if g: t["fs_guard"] += 1
        m = str(r.get("model", "")).rstrip("/").split("/")[-1]
        if m: d["models"].add(m)
    per = {k: {**v, "models": sorted(v["models"])} for k, v in sorted(per.items())}
    return {"total": tot, "per_run": per, "per_case": {k: v for k, v in sorted(by_case.items())}}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--honest", required=True)
    ap.add_argument("--liar", required=True)
    ap.add_argument("--trust", required=True)
    ap.add_argument("--lumi", required=True)
    ap.add_argument("--trust2", help="optional 4-node sibling run (trust_evidence_19200.jsonl.gz)")
    ap.add_argument("--json-out")
    a = ap.parse_args()
    out = {"honest": fleet(a.honest), "liar": fleet(a.liar),
           "trust_25600": trust(a.trust)}
    if a.trust2:
        out["trust_19200"] = trust(a.trust2)
    out["lumi"] = lumi(a.lumi)
    txt = json.dumps(out, indent=1, ensure_ascii=False)
    print(txt)
    if a.json_out:
        open(a.json_out, "w").write(txt)

if __name__ == "__main__":
    main()
