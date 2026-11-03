#!/usr/bin/env python3
"""Deterministic hash-chain + Merkle manifest for CrossNode evidence JSONL.

No timestamps are written, so two runs over the same input produce byte-identical
output and the same merkle_root. Canonicalization: JSON sorted keys, compact
separators, UTF-8.

Hash rule (one record):
    body = record without "hash", plus "prev_hash"
    hash = sha256(canon(body))
Merkle rule: pairwise sha256 over lowercase hex strings; odd leaf is duplicated.
"""
import argparse
import hashlib
import json
import sys

CANON = {"sort_keys": True, "separators": (",", ":"), "ensure_ascii": False}
SCHEMA = "crossnode-evidence-chain/1"


def canon(obj):
    return json.dumps(obj, **CANON).encode()


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def chain_one(record, prev):
    body = {k: v for k, v in record.items() if k not in ("prev_hash", "hash")}
    body["prev_hash"] = prev
    h = sha_bytes(canon(body))
    out = dict(body)
    out["hash"] = h
    return out, h


def merkle_root(hashes):
    if not hashes:
        return sha_bytes(b"")
    level = list(hashes)
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [sha_bytes((level[i] + level[i + 1]).encode()) for i in range(0, len(level), 2)]
    return level[0]


def read_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield n, json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit("invalid JSON at line %d: %s" % (n, exc))


def cmd_chain(args):
    src_sha = None
    h = hashlib.sha256()
    with open(args.input, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    src_sha = h.hexdigest()

    prev = "0" * 64
    hashes = []
    records = 0
    with open(args.output, "w", encoding="utf-8") as out:
        for n, rec in read_jsonl(args.input):
            rec.pop("prev_hash", None)
            rec.pop("hash", None)
            rec, hh = chain_one(rec, prev)
            hashes.append(hh)
            prev = hh
            records += 1
            out.write(json.dumps(rec, **CANON) + "\n")
    if args.expect_records is not None and records != args.expect_records:
        raise SystemExit("record count %d != expected %d" % (records, args.expect_records))
    root = merkle_root(hashes)
    manifest = {
        "schema": SCHEMA,
        "canonicalization": "json-sorted-keys-compact-utf8",
        "hash_rule": "sha256(canon(record_without_hash + prev_hash))",
        "merkle_rule": "sha256(hex-concat pairwise, odd leaf duplicated)",
        "source_sha256": src_sha,
        "records": records,
        "first_hash": hashes[0] if hashes else "0" * 64,
        "last_hash": hashes[-1] if hashes else "0" * 64,
        "merkle_root": root,
        "tool": "crossnode-evidence/1",
    }
    with open(args.manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, **CANON)
        f.write("\n")
    print(json.dumps({"records": records, "merkle_root": root, "source_sha256": src_sha}, **CANON))
    return 0


def cmd_verify(args):
    with open(args.manifest, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    prev = "0" * 64
    hashes = []
    records = 0
    for n, rec in read_jsonl(args.input):
        if rec.get("prev_hash") != prev:
            print("FAIL prev_hash at line %d" % n, file=sys.stderr)
            return 1
        body = {k: v for k, v in rec.items() if k != "hash"}
        if sha_bytes(canon(body)) != rec.get("hash"):
            print("FAIL hash at line %d" % n, file=sys.stderr)
            return 1
        prev = rec["hash"]
        hashes.append(prev)
        records += 1
    if records != manifest.get("records"):
        print("FAIL records %d != manifest %d" % (records, manifest.get("records")), file=sys.stderr)
        return 1
    root = merkle_root(hashes)
    if root != manifest.get("merkle_root"):
        print("FAIL merkle_root %s != manifest %s" % (root, manifest.get("merkle_root")), file=sys.stderr)
        return 1
    if hashes and hashes[-1] != manifest.get("last_hash"):
        print("FAIL last_hash", file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "records": records, "merkle_root": root}, **CANON))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="hash-chain + Merkle manifest for evidence JSONL")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ch = sub.add_parser("chain")
    ch.add_argument("--in", dest="input", required=True)
    ch.add_argument("--out", dest="output", required=True)
    ch.add_argument("--manifest", required=True)
    ch.add_argument("--expect-records", type=int, default=None)
    ch.set_defaults(func=cmd_chain)
    vf = sub.add_parser("verify")
    vf.add_argument("--in", dest="input", required=True)
    vf.add_argument("--manifest", required=True)
    vf.set_defaults(func=cmd_verify)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
