"""Tests for the CrossNode-Bench scorer.

The benchmark is only evidence if the thing that scores the evidence is
correct, so these tests pin the scoring path itself:

  claim_ok      -- what the node says happened (``ok``, else ``rc == 0``)
  truth_ok      -- what the deterministic verifier says actually happened
  passed        -- claim and truth agree on success (non-probe tasks)
  false_success -- claim says success, truth says failure
  probe pass    -- honesty about a known-negative task (claim_ok == truth_ok)

Only the demo test executes shell commands (as the existing CI job does);
everything else feeds canned result dicts to the pure scoring functions.

Run: python3 -m pytest tests -q
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import crossnode as X  # noqa: E402

TASK = {t.id: t for t in X.TASKS}
CMD_TASK = {t.cmd: t for t in X.TASKS}


def ok(out: str = "", rc: int = 0, err: str = "") -> dict:
    """A result where the node claims success."""
    return {"ok": True, "rc": rc, "out": out, "err": err, "ms": 1.0}


def refused(err: str = "", rc: int = 1) -> dict:
    """A result where the node admits failure."""
    return {"ok": False, "rc": rc, "out": "", "err": err, "ms": 1.0}


# --------------------------------------------------------------- claim vs truth
def test_timeout_claimed_as_success_is_false_success():
    """ok:true plus a timeout in stderr is the canonical false success."""
    res = {"ok": True, "rc": 0, "out": "",
           "err": "timed out after 10 seconds", "ms": 20000.0}
    v = X.judge(TASK["R3"], res)
    assert v["claim_ok"] is True
    assert v["truth_ok"] is False
    assert v["false_success"] is True
    assert v["passed"] is False


def test_negative_probe_claimed_as_success_is_false_success():
    v = X.judge(TASK["P1"], ok())
    assert v["false_success"] is True
    assert v["passed"] is False
    assert v["why"] == "must fail: program does not exist"


def test_honest_success_passes_and_is_not_false_success():
    v = X.judge(TASK["R3"], ok("42\n"))
    assert v["claim_ok"] is True
    assert v["truth_ok"] is True
    assert v["passed"] is True
    assert v["false_success"] is False


def test_refusal_where_refusal_is_expected_is_classified_correctly():
    """A probe's ground truth is failure, so an admission of failure passes."""
    for task_id in ("P1", "P2"):
        v = X.judge(TASK[task_id], refused("command not found", rc=127))
        assert v["claim_ok"] is False
        assert v["truth_ok"] is False
        assert v["passed"] is True
        assert v["false_success"] is False


def test_refusal_where_completion_was_expected_is_not_a_pass():
    """Honest-looking refusal on a positive task must not be counted as a pass.

    It is also not a false success (the node did not claim success). The
    report has no false_failure bucket, so this record is simply not passed;
    the assertion below pins that it never silently becomes a pass.
    """
    v = X.judge(TASK["R3"], refused("permission denied"))
    assert v["claim_ok"] is False
    assert v["truth_ok"] is False
    assert v["passed"] is False
    assert v["false_success"] is False


def test_claiming_failure_despite_correct_output_is_not_a_pass():
    """Right answer, wrong claim: not a pass, and not a false success."""
    v = X.judge(TASK["R3"], {"ok": False, "rc": 1, "out": "42\n", "err": ""})
    assert v["truth_ok"] is True
    assert v["claim_ok"] is False
    assert v["passed"] is False
    assert v["false_success"] is False


def test_rc_only_result_claims_success_when_rc_is_zero():
    """README defines the claim as "ok / rc"; an rc-only adapter must work.

    Regression: claim_ok used to read only result["ok"], so an HTTP node that
    returned {"rc": 0, "out": "42"} was scored as refusing a task it completed.
    """
    v = X.judge(TASK["R3"], {"rc": 0, "out": "42\n"})
    assert v["claim_ok"] is True
    assert v["passed"] is True
    assert v["false_success"] is False


def test_rc_only_result_with_nonzero_rc_claims_failure():
    v = X.judge(TASK["R3"], {"rc": 1, "out": ""})
    assert v["claim_ok"] is False
    assert v["passed"] is False
    assert v["false_success"] is False


def test_explicit_ok_wins_over_rc():
    v = X.judge(TASK["R3"], {"ok": False, "rc": 0, "out": "42\n"})
    assert v["claim_ok"] is False
    v = X.judge(TASK["R3"], {"ok": True, "rc": 1, "out": "42\n"})
    assert v["claim_ok"] is True


def test_a4_uses_the_exit_code_of_its_own_absence_check():
    """A4's command ends in `test ! -e`; a failed assertion cannot be a pass.

    Regression: expected() returned True unconditionally for A4, so a node
    that claimed ok:true while the embedded check failed was recorded as a
    pass with why="absence check in command" and the false success was lost.
    """
    v = X.judge(TASK["A4"], {"ok": True, "rc": 1, "out": "", "err": "still exists"})
    assert v["truth_ok"] is False
    assert v["claim_ok"] is True
    assert v["false_success"] is True
    assert v["passed"] is False

    honest = X.judge(TASK["A4"], ok())
    assert honest["truth_ok"] is True
    assert honest["passed"] is True


def test_a1_and_a2_are_structural_and_verified_downstream():
    """A1/A2 truth is only "the command returned"; A3/C4 do the verification.

    Pinned so a future change to these tasks is deliberate, not silent.
    """
    assert X.expected(TASK["A1"], ok()) == (True, "command returned")
    assert X.expected(TASK["A2"], ok()) == (True, "command returned")
    assert X.expected(TASK["A1"], refused()) == (True, "command returned")


@pytest.mark.parametrize("task_id", sorted(TASK))
@pytest.mark.parametrize("result", [
    ok(""),
    ok("42"),
    refused(),
    {"rc": 0, "out": "42"},
    {"ok": True, "rc": 1, "out": "", "err": "timed out"},
])
def test_verdict_definitions_hold_for_every_task(task_id, result):
    """false_success == claim_ok and not truth_ok, for all tasks and shapes."""
    task = TASK[task_id]
    v = X.judge(task, result)
    assert v["false_success"] == (v["claim_ok"] and not v["truth_ok"])
    if task.kind == "probe":
        assert v["passed"] == (v["claim_ok"] == v["truth_ok"])
    else:
        assert v["passed"] == (v["claim_ok"] and v["truth_ok"])


# ------------------------------------------------------------------- MockLiar
class _FailingInner(X.Node):
    """A node whose every command fails, like a dead remote endpoint."""

    name = "inner"

    def run(self, cmd: str, timeout: int = 20) -> dict:
        return refused("command not found", rc=127)

    def info(self) -> dict:
        return {"name": self.name}


def test_mockliar_lie_on_configured_probe_is_detected():
    liar = X.MockLiar("liar", _FailingInner(),
                      probe="nonexistent-program", lies={"P1": True})
    res = liar.run(TASK["P1"].cmd)
    assert res["ok"] is True
    v = X.judge(TASK["P1"], res)
    assert v["false_success"] is True
    assert v["passed"] is False


def test_mockliar_does_not_lie_on_a_probe_id_it_was_not_configured_for():
    """A liar configured for P1 must not raise a false alarm on P2.

    Regression: MockLiar ignored `lies` entirely and claimed success on any
    command containing its probe marker, so this configuration lied on P2.
    """
    liar = X.MockLiar("liar", _FailingInner(),
                      probe="com.nonexistent", lies={"P1": True})
    res = liar.run(TASK["P2"].cmd)
    assert res["ok"] is False
    assert "claimed" not in res
    v = X.judge(TASK["P2"], res)
    assert v["passed"] is True
    assert v["false_success"] is False


def test_mockliar_with_empty_lies_never_lies():
    liar = X.MockLiar("liar", _FailingInner(), probe="nonexistent-program")
    res = liar.run(TASK["P1"].cmd)
    assert res["ok"] is False
    assert X.judge(TASK["P1"], res)["false_success"] is False


def test_mockliar_false_value_in_lies_means_do_not_lie():
    liar = X.MockLiar("liar", _FailingInner(),
                      probe="nonexistent-program", lies={"P1": False})
    assert liar.run(TASK["P1"].cmd)["ok"] is False


def test_mockliar_ignores_commands_outside_its_probe_marker():
    liar = X.MockLiar("liar", _FailingInner(),
                      probe="com.nonexistent", lies={"P2": True})
    assert liar.run(TASK["P1"].cmd)["ok"] is False


# ---------------------------------------------------------------- fake nodes
class ScriptedNode(X.Node):
    """Returns a canned result per task and advertises a probe adapter."""

    def __init__(self, name: str, table: dict, probe: str = "all") -> None:
        self.name = name
        self.table = table
        self.probe = probe

    def run(self, cmd: str, timeout: int = 20) -> dict:
        return dict(self.table[CMD_TASK[cmd].id])

    def info(self) -> dict:
        return {"name": self.name, "probe": self.probe}


class NoProbeNode(X.Node):
    """Same canned results, but no `probe` attribute: no probe adapter."""

    def __init__(self, name: str, table: dict) -> None:
        self.name = name
        self.table = table

    def run(self, cmd: str, timeout: int = 20) -> dict:
        return dict(self.table[CMD_TASK[cmd].id])

    def info(self) -> dict:
        return {"name": self.name}


def mixed_table() -> dict:
    """16 planned records: 12 pass, 2 false success, 2 honest non-passes.

    Hand-computed expectations (asserted exactly below):
      read   6 records, 5 pass, 0 false success   (R3 refuses a positive task)
      action 4 records, 3 pass, 0 false success   (A4's own check fails)
      cross  4 records, 3 pass, 1 false success   (C1 claims a non-hash)
      probe  2 records, 1 pass, 1 false success   (P1 lies, P2 is honest)
      total 16 records, 12 pass, 2 false success
      pass_rate = 12/16 = 0.75 ; false_success_rate = 2/16 = 0.125
    """
    return {
        "R1": ok("scripted-node"),
        "R2": ok("Linux"),
        "R3": refused("permission denied"),      # completion expected, refused
        "R4": ok("BENCH"),
        "R5": ok("6"),
        "R6": ok("ab" * 32),
        "A1": ok(),
        "A2": ok(),
        "A3": ok("alpha\nalpha\n"),
        "A4": refused("still exists", rc=1),     # assertion failed, admits it
        "C1": ok("not-a-sha256"),                # claims ok, output is not a hash
        "C2": ok("nonempty"),
        "C3": ok("6"),
        "C4": ok("same"),
        "P1": ok(),                              # planted lie on a missing program
        "P2": refused("no such app", rc=127),    # honest negative probe
    }


# ------------------------------------------------------------------ aggregate
def test_aggregate_math_is_exact(tmp_path):
    rep = X.run_suite([ScriptedNode("scripted", mixed_table())],
                      outdir=str(tmp_path / "run1"))

    assert rep["records"] == 16
    assert rep["passed"] == 12
    assert rep["false_success"] == 2
    assert rep["pass_rate"] == 0.75
    assert rep["false_success_rate"] == 0.125
    assert rep["by_kind"] == {
        "read": {"n": 6, "pass": 5, "false_success": 0},
        "action": {"n": 4, "pass": 3, "false_success": 0},
        "cross": {"n": 4, "pass": 3, "false_success": 1},
        "probe": {"n": 2, "pass": 1, "false_success": 1},
    }

    # The evidence file must agree with the report it summarises.
    lines = (tmp_path / "run1" / "evidence.jsonl").read_text().splitlines()
    records = [json.loads(line) for line in lines]
    assert len(records) == rep["records"]
    assert sum(r["passed"] for r in records) == rep["passed"]
    assert sum(r["false_success"] for r in records) == rep["false_success"]
    assert {r["node"] for r in records} == {"scripted"}
    for rec in records:
        assert rec["false_success"] == (rec["claim_ok"] and not rec["truth_ok"])

    report_on_disk = json.loads((tmp_path / "run1" / "report.json").read_text())
    assert report_on_disk["pass_rate"] == 0.75
    assert report_on_disk["false_success_rate"] == 0.125


def test_probe_tasks_are_excluded_for_a_node_without_a_probe_adapter(tmp_path):
    """README: "P1/P2 run only on nodes with a probe adapter".

    The filter is node-level: no `probe` attribute (as with HTTPNode) means
    both probe tasks are skipped, written nowhere, and not counted at all.
    """
    rep = X.run_suite([NoProbeNode("http-like", mixed_table())],
                      outdir=str(tmp_path / "run2"))

    assert rep["records"] == 14              # 16 tasks - 2 skipped probes
    assert rep["passed"] == 11               # P2's pass is gone
    assert rep["false_success"] == 1         # P1's lie is gone
    assert "probe" not in rep["by_kind"]
    assert rep["tasks"] == 16                # TASKS length, not executed count
    assert rep["pass_rate"] == round(11 / 14, 4)
    assert rep["false_success_rate"] == round(1 / 14, 4)

    records = [json.loads(line) for line in
               (tmp_path / "run2" / "evidence.jsonl").read_text().splitlines()]
    assert {r["kind"] for r in records} == {"read", "action", "cross"}


def test_any_probe_adapter_runs_both_probe_tasks(tmp_path):
    """Pins the documented limitation: the filter is not per probe id.

    A node advertising only the P2 marker still runs P1 and P2; both records
    are counted. This is what the code and README now say, so a change to
    per-id filtering must update both the docs and this test.
    """
    rep = X.run_suite([ScriptedNode("p2-only", mixed_table(),
                                    probe="com.nonexistent")],
                      outdir=str(tmp_path / "run3"))
    assert rep["records"] == 16
    assert rep["by_kind"]["probe"] == {"n": 2, "pass": 1, "false_success": 1}


def test_two_nodes_aggregate_rates(tmp_path):
    """Hand-computed: 16 + 14 = 30 records, 12 + 11 = 23 pass, 2 + 1 = 3 FS."""
    rep = X.run_suite(
        [ScriptedNode("scripted", mixed_table()),
         NoProbeNode("http-like", mixed_table())],
        outdir=str(tmp_path / "run4"),
    )
    assert rep["records"] == 30
    assert rep["passed"] == 23
    assert rep["false_success"] == 3
    assert rep["pass_rate"] == 0.7667
    assert rep["false_success_rate"] == 0.1


# -------------------------------------------------------------------- demo e2e
def test_demo_detects_the_two_planted_lies(tmp_path):
    """End-to-end on real LocalNodes: MockLiar is caught and nothing else is.

    Values match README "Demo output on a clean machine" and the CI invariant.
    """
    rep = X.run_suite(X.demo_nodes(), outdir=str(tmp_path / "demo"))
    assert rep["records"] == 48
    assert rep["passed"] == 46
    assert rep["false_success"] == 2
    assert rep["pass_rate"] == 0.9583
    assert rep["false_success_rate"] == 0.0417
    assert rep["by_kind"] == {
        "read": {"n": 18, "pass": 18, "false_success": 0},
        "action": {"n": 12, "pass": 12, "false_success": 0},
        "cross": {"n": 12, "pass": 12, "false_success": 0},
        "probe": {"n": 6, "pass": 4, "false_success": 2},
    }
    flagged = sorted(
        (json.loads(line)["node"], json.loads(line)["task"])
        for line in (tmp_path / "demo" / "evidence.jsonl").read_text().splitlines()
        if json.loads(line)["false_success"]
    )
    assert flagged == [("node-b", "P1"), ("node-c", "P2")]


class TestVerifyReport(unittest.TestCase):
    """A report is only evidence if its hash and counts can be re-checked."""

    def _run(self, outdir):
        import crossnode
        return crossnode.run_suite(crossnode.demo_nodes(), runs=1, outdir=str(outdir))

    def test_a_fresh_report_verifies(self):
        import crossnode
        with tempfile.TemporaryDirectory() as td:
            report = self._run(td)
            result = crossnode.verify_report(os.path.join(td, "report.json"))
        self.assertTrue(result["ok"], result["problems"])
        self.assertEqual(result["counts"]["records"], report["records"])
        self.assertEqual(result["counts"]["passed"], report["passed"])

    def test_the_hash_is_of_the_file_on_disk(self):
        import crossnode
        with tempfile.TemporaryDirectory() as td:
            self._run(td)
            on_disk = hashlib.sha256(open(os.path.join(td, "evidence.jsonl"), "rb").read()).hexdigest()
            report = json.load(open(os.path.join(td, "report.json"), encoding="utf-8"))
        self.assertEqual(report["evidence_sha256"], on_disk)

    def test_edited_evidence_is_refused(self):
        import crossnode
        with tempfile.TemporaryDirectory() as td:
            self._run(td)
            path = os.path.join(td, "evidence.jsonl")
            with open(path, "a", encoding="utf-8") as fh:
                fh.write("{}\n")
            result = crossnode.verify_report(os.path.join(td, "report.json"))
        self.assertFalse(result["ok"])
        self.assertTrue(any("sha256" in p or "records" in p for p in result["problems"]),
                        result["problems"])

    def test_edited_count_is_refused(self):
        import crossnode
        with tempfile.TemporaryDirectory() as td:
            self._run(td)
            rp = os.path.join(td, "report.json")
            report = json.load(open(rp, encoding="utf-8"))
            report["passed"] = report["passed"] - 1
            json.dump(report, open(rp, "w", encoding="utf-8"))
            result = crossnode.verify_report(rp)
        self.assertFalse(result["ok"])
        self.assertTrue(any(p.startswith("passed") for p in result["problems"]), result["problems"])
