# OpenTelemetry span attributes

One span per claim, emitted after the probe. No measurement changes; attributes are
metadata only.

| Attribute | Type | Cardinality | Example | Required |
|---|---|---|---|---|
| `crossnode.run_id` | string | per run | `run-36` | yes |
| `crossnode.task_id` | string | per task | `R1` | yes |
| `crossnode.node` | string | per node | `node-a` | yes |
| `crossnode.kind` | string | 1 of `read, action, cross, probe` | `action` | yes |
| `crossnode.claim_ok` | boolean | 2 | `true` | yes |
| `crossnode.truth_ok` | boolean | 2 | `false` | yes |
| `crossnode.verdict` | string | `pass, false_success, true_failure, false_failure, unverifiable` | `false_success` | yes |
| `crossnode.false_success` | boolean | 2 | `true` | yes |
| `crossnode.dur_ms` | double | continuous | `31.6` | no |
| `crossnode.mismatch_class` | string | `M1..M4`, empty | `M2` | no |
| `crossnode.evidence_sha256` | string | per record | `eda02d9c…` | no |

Forbidden attributes: prompts, outputs, credentials, hostnames beyond the declared node id,
or any field that is not already public in the evidence record.
