#!/usr/bin/env bash
# Local fallback gate: verify the hash-chain, then enforce OPA policy if `opa` is installed.
# Usage: ./gate.sh <chained.jsonl> <manifest.json> [signed:true|false] [fsr_threshold] [coverage_threshold]
set -euo pipefail
cd "$(dirname "$0")"

EVIDENCE=${1:?usage: gate.sh <chained.jsonl> <manifest.json> [signed] [fsr] [cov]}
MANIFEST=${2:?usage: gate.sh <chained.jsonl> <manifest.json> [signed] [fsr] [cov]}
SIGNED=${3:-false}
FSR_MAX=${4:-0.02}
COV_MIN=${5:-0.95}

python3 tools/evidence.py verify --in "$EVIDENCE" --manifest "$MANIFEST" >/dev/null
echo "chain: OK"

python3 - "$EVIDENCE" "$MANIFEST" "$SIGNED" "$FSR_MAX" "$COV_MIN" > /tmp/crossnode_gate_input.json <<'PY'
import json, sys
evidence, manifest, signed, fsr_max, cov_min = sys.argv[1:6]
records = 0
fs = 0
verifiable = 0
with open(evidence, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        records += 1
        if r.get("false_success") is not None:
            verifiable += 1
        if r.get("false_success") is True:
            fs += 1
m = json.load(open(manifest, encoding="utf-8"))
payload = {
    "signed": signed.lower() == "true",
    "manifest": m,
    "metrics": {
        "records": records,
        "false_success": fs,
        "false_success_rate": (fs / records) if records else 0.0,
        "coverage": (verifiable / records) if records else 0.0,
    },
    "thresholds": {"false_success_rate": float(fsr_max), "coverage": float(cov_min)},
}
json.dump(payload, sys.stdout, sort_keys=True)
PY

if command -v opa >/dev/null 2>&1; then
  RESULT=$(opa eval -d gate.rego -i /tmp/crossnode_gate_input.json -f raw 'data.crossnode.gate.allow')
  echo "opa allow: $RESULT"
  if [ "$RESULT" != "true" ]; then
    opa eval -d gate.rego -i /tmp/crossnode_gate_input.json -f pretty 'data.crossnode.gate.deny'
    exit 1
  fi
else
  echo "opa not installed; running built-in threshold check"
  python3 - <<'PY'
import json
p = json.load(open("/tmp/crossnode_gate_input.json", encoding="utf-8"))
m, t = p["metrics"], p["thresholds"]
deny = []
if not p["signed"]:
    deny.append("evidence is not signed (cosign bundle missing)")
if m["records"] <= 0:
    deny.append("no records")
if m["false_success_rate"] > t["false_success_rate"]:
    deny.append("false_success_rate %.6f > %.6f" % (m["false_success_rate"], t["false_success_rate"]))
if m["coverage"] < t["coverage"]:
    deny.append("coverage %.6f < %.6f" % (m["coverage"], t["coverage"]))
if deny:
    print("\n".join(deny))
    raise SystemExit(1)
print("allow: true")
PY
fi
