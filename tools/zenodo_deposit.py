#!/usr/bin/env python3
"""Create, upload and publish a Zenodo deposition for CrossNode-Bench.

Requires ZENODO_TOKEN with scopes deposit:write and deposit:actions.
Nothing is published without --yes.

  python3 tools/zenodo_deposit.py --check
  python3 tools/zenodo_deposit.py --create --metadata .zenodo.json
  python3 tools/zenodo_deposit.py --upload evidence/evidence_chained.jsonl evidence/manifest.json SPEC.md
  python3 tools/zenodo_deposit.py --publish --yes
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://zenodo.org/api"
TOKEN = os.environ.get("ZENODO_TOKEN", "").strip()
STATE = Path("zenodo_deposition.json")


def _req(method: str, url: str, data: bytes | None = None, ctype: str | None = None) -> dict:
    headers = {"Authorization": "Bearer " + TOKEN} if TOKEN else {}
    if ctype:
        headers["Content-Type"] = ctype
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            body = r.read()
        return json.loads(body.decode("utf-8", "replace")) if body else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:400]
        print("HTTP %s %s: %s" % (e.code, url, detail), file=sys.stderr)
        raise SystemExit(2)


def check() -> int:
    if not TOKEN:
        print("NEMA ZENODO_TOKEN. Napravi token (deposit:write, deposit:actions) na "
              "https://zenodo.org/account/settings/applications/tokens/new i stavi ga u env.")
        return 2
    d = _req("GET", API + "/deposit/depositions?size=1")
    print("token OK; existing depositions visible:", len(d) if isinstance(d, list) else "?")
    return 0


def create(metadata_path: str) -> int:
    if not TOKEN:
        return check()
    meta = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
    d = _req("POST", API + "/deposit/depositions",
             json.dumps({"metadata": meta}).encode(), "application/json")
    STATE.write_text(json.dumps(d, indent=2), encoding="utf-8")
    print("created deposition", d.get("id"), "|", (d.get("links") or {}).get("html", ""))
    return 0


def upload(files: list[str]) -> int:
    if not STATE.exists():
        print("nema %s; prvo --create" % STATE, file=sys.stderr)
        return 2
    state = json.loads(STATE.read_text(encoding="utf-8"))
    bucket = (state.get("links") or {}).get("bucket", "")
    if not bucket:
        print("deposition nema bucket link", file=sys.stderr)
        return 2
    for name in files:
        p = Path(name)
        if not p.exists():
            print("preskacem (nema):", name, file=sys.stderr)
            continue
        _req("PUT", bucket + "/" + p.name, p.read_bytes(), "application/octet-stream")
        print("uploaded", p.name, p.stat().st_size, "bytes")
    return 0


def publish(yes: bool) -> int:
    if not STATE.exists():
        print("nema %s; prvo --create/--upload" % STATE, file=sys.stderr)
        return 2
    state = json.loads(STATE.read_text(encoding="utf-8"))
    dep_id = state.get("id")
    if not yes:
        print("dry-run: publish bi objavio deposition", dep_id, "i dodijelio DOI. Dodaj --yes.")
        return 0
    d = _req("POST", "%s/deposit/depositions/%s/actions/publish" % (API, dep_id))
    print("PUBLISHED", d.get("doi") or (d.get("metadata") or {}).get("doi") or "?")
    print((d.get("links") or {}).get("html", ""))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--create", action="store_true")
    ap.add_argument("--metadata", default=".zenodo.json")
    ap.add_argument("--upload", nargs="*", default=[])
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--yes", action="store_true")
    a = ap.parse_args()
    if a.check:
        return check()
    if a.create:
        return create(a.metadata)
    if a.upload:
        return upload(a.upload)
    if a.publish:
        return publish(a.yes)
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
