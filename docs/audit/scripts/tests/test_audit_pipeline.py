#!/usr/bin/env python3
"""Smoke + behavior tests for the audit pipeline scripts.

These are deliberately small, self-contained, and run without touching
the live ledger. Each test patches the relevant module's REPO_ROOT to a
temporary directory so the script reads/writes only the test fixture.

Run via:
  python3 -m unittest docs.audit.scripts.tests.test_audit_pipeline
or:
  python3 docs/audit/scripts/tests/test_audit_pipeline.py
"""
from __future__ import annotations

import importlib
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECT_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = REPO_ROOT / "audit" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def _import(module_name: str):
    """Force a fresh import each test."""
    if module_name in sys.modules:
        del sys.modules[module_name]
    return importlib.import_module(module_name)


def _import_codex_audit_runner():
    """Import the repo-root codex audit runner without changing sys.path."""
    module_name = "codex_audit_runner_under_test"
    if module_name in sys.modules:
        del sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(
        module_name, PROJECT_ROOT / "scripts" / "codex_audit_runner.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class CleanLedgerFixture:
    """Build a minimal but valid audit_ledger.json + citation_graph.json
    on a temporary REPO_ROOT for unit-style testing."""

    def __init__(self, tmpdir: Path):
        self.tmpdir = tmpdir
        self.audit_dir = tmpdir / "docs" / "audit"
        self.data_dir = self.audit_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        (self.tmpdir / "docs").mkdir(parents=True, exist_ok=True)

    def write_note(self, rel_path: str, body: str) -> Path:
        path = self.tmpdir / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        return path

    def write_runner(self, rel_path: str, body: str) -> Path:
        path = self.tmpdir / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        return path

    def write_ledger(self, ledger: dict) -> None:
        (self.data_dir / "audit_ledger.json").write_text(
            json.dumps(ledger, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def write_graph(self, graph: dict) -> None:
        (self.data_dir / "citation_graph.json").write_text(
            json.dumps(graph, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def read_ledger(self) -> dict:
        return json.loads((self.data_dir / "audit_ledger.json").read_text(encoding="utf-8"))


def _patch_repo_root(module, tmp_root: Path) -> None:
    """Override the module-level REPO_ROOT-derived paths."""
    module.REPO_ROOT = tmp_root
    module.DATA_DIR = tmp_root / "docs" / "audit" / "data"
    module.LEDGER_PATH = module.DATA_DIR / "audit_ledger.json"
    if hasattr(module, "GRAPH_PATH"):
        module.GRAPH_PATH = module.DATA_DIR / "citation_graph.json"
    if hasattr(module, "SUMMARY_PATH"):
        # Either compute_effective_status (effective_status_summary) or
        # compute_load_bearing (load_bearing_summary). Set both files under
        # tmp data dir; only the relevant one is written.
        module.SUMMARY_PATH = module.DATA_DIR / "effective_status_summary.json"
    if hasattr(module, "OUTPUT_PATH"):
        module.OUTPUT_PATH = module.DATA_DIR / "auditor_reliability.json"


class ApplyAuditTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_root = Path(self._tmp.name)
        self.fx = CleanLedgerFixture(self.tmp_root)

    def _seed_one_row(self, cid: str, *, audit_status="unaudited",
                      claim_type=None, deps=None,
                      criticality="leaf", note_body="# test\n"):
        path = f"docs/{cid.upper()}.md"
        self.fx.write_note(path, note_body)
        import hashlib
        note_hash = hashlib.sha256(note_body.encode("utf-8")).hexdigest()
        ledger = {
            "schema_version": 1,
            "rows": {
                cid: {
                    "claim_id": cid,
                    "note_path": path,
                    "note_hash": note_hash,
                    "deps": list(deps or []),
                    "audit_status": audit_status,
                    "claim_type": claim_type,
                    "criticality": criticality,
                    "previous_audits": [],
                }
            },
        }
        self.fx.write_ledger(ledger)
        return path, note_hash

    def test_apply_clean_verdict_writes_snapshot_with_runner_hash(self):
        m = _import("apply_audit")
        _patch_repo_root(m, self.tmp_root)

        runner_path = "scripts/test_runner.py"
        runner_body = "print('PASS=1 FAIL=0')\n"
        self.fx.write_runner(runner_path, runner_body)

        path, note_hash = self._seed_one_row("test_clean_row", criticality="leaf")
        # Add runner_path to ledger row
        led = self.fx.read_ledger()
        led["rows"]["test_clean_row"]["runner_path"] = runner_path
        self.fx.write_ledger(led)

        audit = {
            "claim_id": "test_clean_row",
            "verdict": "audited_clean",
            "claim_type": "positive_theorem",
            "claim_scope": "test scope",
            "auditor": "test-auditor",
            "auditor_family": "codex-gpt-5.5",
            "independence": "cross_family",
            "load_bearing_step_class": "C",
            "load_bearing_step": "test step",
            "chain_closes": True,
            "chain_closure_explanation": "ok",
            "verdict_rationale": "ok",
        }
        ok, msg = m.apply_one(led, audit)
        self.assertTrue(ok, msg)
        snap = led["rows"]["test_clean_row"].get("audit_state_snapshot")
        self.assertIsNotNone(snap)
        self.assertIn("runner_hash", snap)
        # Runner hash matches actual file hash
        import hashlib
        expected = hashlib.sha256(runner_body.encode("utf-8")).hexdigest()
        self.assertEqual(snap["runner_hash"], expected)

    def test_weak_independence_blocks_audited_clean(self):
        m = _import("apply_audit")
        _patch_repo_root(m, self.tmp_root)
        path, _ = self._seed_one_row("test_weak", criticality="medium")
        led = self.fx.read_ledger()
        audit = {
            "claim_id": "test_weak",
            "verdict": "audited_clean",
            "claim_type": "positive_theorem",
            "claim_scope": "test",
            "auditor": "weak-auditor",
            "auditor_family": "claude-opus",
            "independence": "weak",
            "load_bearing_step_class": "C",
        }
        ok, msg = m.apply_one(led, audit)
        self.assertFalse(ok)
        self.assertIn("weak", msg)


class SeedLedgerTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_root = Path(self._tmp.name)
        self.fx = CleanLedgerFixture(self.tmp_root)

    def test_archive_prior_audit_clears_audit_state_snapshot(self):
        # Regression test for issue #3 in the audit-framework review:
        # archive_prior_audit must clear audit_state_snapshot, not leave it
        # in place where it would confuse invalidate_stale_audits + lint.
        m = _import("seed_audit_ledger")
        row_with_snapshot = {
            "claim_id": "test",
            "audit_status": "audited_clean",
            "audit_state_snapshot": {"criticality": "high", "deps": []},
            "previous_audits": [],
        }
        new_row = m.archive_prior_audit(dict(row_with_snapshot))
        # Snapshot should be in EMPTY_AUDIT (now None), not preserved
        self.assertIsNone(new_row.get("audit_state_snapshot"))
        # Prior values archived
        self.assertEqual(len(new_row["previous_audits"]), 1)

    def test_existing_unaudited_row_clears_stale_audit_residue(self):
        m = _import("seed_audit_ledger")
        _patch_repo_root(m, self.tmp_root)
        body = "# test\nClaim type: no_go\n"
        self.fx.write_note("docs/test.md", body)
        import hashlib
        note_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        self.fx.write_graph(
            {
                "nodes": {
                    "test": {
                        "path": "docs/test.md",
                        "title": "test",
                        "runner_path": None,
                        "deps": [],
                        "note_hash": note_hash,
                        "claim_type_seed_hint": "no_go",
                        "claim_type_author_hint": None,
                        "claim_type_author_hint_raw": None,
                    }
                }
            }
        )
        self.fx.write_ledger(
            {
                "schema_version": 1,
                "rows": {
                    "test": {
                        "claim_id": "test",
                        "note_path": "docs/test.md",
                        "title": "test",
                        "runner_path": None,
                        "deps": [],
                        "note_hash": note_hash,
                        "previous_audits": [{"verdict": "old"}],
                        "audit_status": "unaudited",
                        "auditor": "stale-auditor",
                        "auditor_family": "codex-gpt-5",
                        "independence": "fresh_context",
                        "load_bearing_step": "stale step",
                        "chain_closes": True,
                        "audit_state_snapshot": {"criticality": "medium"},
                        "cross_confirmation": {"status": "confirmed"},
                        "claim_type": "positive_theorem",
                        "claim_type_provenance": "audited",
                        "claim_scope": "stale scope",
                    }
                },
            }
        )

        seeded = m.seed()
        row = seeded["rows"]["test"]

        self.assertEqual(row["audit_status"], "unaudited")
        self.assertIsNone(row["auditor"])
        self.assertIsNone(row["auditor_family"])
        self.assertIsNone(row["independence"])
        self.assertIsNone(row["load_bearing_step"])
        self.assertIsNone(row["chain_closes"])
        self.assertIsNone(row["audit_state_snapshot"])
        self.assertIsNone(row["cross_confirmation"])
        self.assertEqual(row["claim_type"], "no_go")
        self.assertEqual(row["claim_type_provenance"], "migration_hint")
        self.assertIsNone(row["claim_scope"])
        self.assertEqual(row["previous_audits"], [{"verdict": "old"}])


class ComputeEffectiveStatusTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_root = Path(self._tmp.name)
        self.fx = CleanLedgerFixture(self.tmp_root)

    def test_clean_positive_with_clean_dep_is_retained(self):
        m = _import("compute_effective_status")
        rows = {
            "parent": {
                "claim_id": "parent",
                "deps": [],
                "audit_status": "audited_clean",
                "claim_type": "positive_theorem",
            },
            "child": {
                "claim_id": "child",
                "deps": ["parent"],
                "audit_status": "audited_clean",
                "claim_type": "positive_theorem",
            },
        }
        new_rows, _cycles = m.compute_effective(rows)
        self.assertEqual(new_rows["parent"]["effective_status"], "retained")
        self.assertEqual(new_rows["child"]["effective_status"], "retained")

    def test_clean_with_unaudited_dep_is_pending_chain(self):
        m = _import("compute_effective_status")
        rows = {
            "parent": {
                "claim_id": "parent",
                "deps": [],
                "audit_status": "unaudited",
                "claim_type": "positive_theorem",
            },
            "child": {
                "claim_id": "child",
                "deps": ["parent"],
                "audit_status": "audited_clean",
                "claim_type": "positive_theorem",
            },
        }
        new_rows, _cycles = m.compute_effective(rows)
        self.assertEqual(new_rows["child"]["effective_status"], "retained_pending_chain")

    def test_main_drops_stale_top_level_timestamp_keys(self):
        m = _import("compute_effective_status")
        _patch_repo_root(m, self.tmp_root)
        ledger = {
            "schema_version": 1,
            "generated_at": "2026-01-01T00:00:00+00:00",
            "effective_status_computed_at": "2026-01-01T00:00:00+00:00",
            "load_bearing_computed_at": "2026-01-01T00:00:00+00:00",
            "invalidation_run_at": "2026-01-01T00:00:00+00:00",
            "rows": {},
        }
        self.fx.write_ledger(ledger)
        m.main()
        post = self.fx.read_ledger()
        for stale in ("generated_at", "effective_status_computed_at",
                      "load_bearing_computed_at", "invalidation_run_at"):
            self.assertNotIn(stale, post)


class ComputeAuditorReliabilityTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_root = Path(self._tmp.name)
        self.fx = CleanLedgerFixture(self.tmp_root)

    def test_cross_confirmation_counts_actual_participants(self):
        m = _import("compute_auditor_reliability")
        _patch_repo_root(m, self.tmp_root)
        self.fx.write_ledger(
            {
                "schema_version": 1,
                "rows": {
                    "confirmed_cross_family": {
                        "claim_id": "confirmed_cross_family",
                        "audit_status": "audited_clean",
                        "auditor_family": "codex-gpt-5",
                        "criticality": "leaf",
                        "cross_confirmation": {
                            "status": "confirmed",
                            "first_audit": {
                                "auditor_family": "codex-gpt-5.5",
                                "verdict": "audited_clean",
                            },
                            "second_audit": {
                                "auditor_family": "codex-gpt-5",
                                "verdict": "audited_clean",
                            },
                        },
                    },
                    "third_pass_cross_family": {
                        "claim_id": "third_pass_cross_family",
                        "audit_status": "audited_conditional",
                        "auditor_family": "codex-gpt-5",
                        "criticality": "leaf",
                        "cross_confirmation": {
                            "status": "third_confirmed_second",
                            "first_audit": {
                                "auditor_family": "codex-gpt-5.5",
                                "verdict": "audited_clean",
                            },
                            "second_audit": {
                                "auditor_family": "codex-gpt-5",
                                "verdict": "audited_conditional",
                            },
                            "third_audit": {
                                "auditor_family": "codex-gpt-5",
                                "verdict": "audited_conditional",
                            },
                        },
                    },
                },
            }
        )

        self.assertEqual(m.main(), 0)
        out = json.loads(
            (self.fx.data_dir / "auditor_reliability.json").read_text(encoding="utf-8")
        )
        gpt5 = out["auditor_family_summary"]["codex-gpt-5"]
        gpt55 = out["auditor_family_summary"]["codex-gpt-5.5"]

        self.assertEqual(gpt5["cross_confirmation_pairs_seen"], 2)
        self.assertEqual(gpt55["cross_confirmation_pairs_seen"], 2)
        self.assertEqual(gpt5["cross_confirmation_pairs_agreed_first_try"], 1)
        self.assertEqual(gpt55["cross_confirmation_pairs_agreed_first_try"], 1)
        self.assertEqual(gpt55["bias_direction_breakdown"]["more_lenient"], 1)
        self.assertEqual(out["totals"]["total_cross_confirmation_pairs"], 2)
        self.assertEqual(out["totals"]["total_cross_confirmation_family_participations"], 4)
        self.assertEqual(out["totals"]["overall_agreement_rate"], 0.5)


class AuditLintTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_root = Path(self._tmp.name)
        self.fx = CleanLedgerFixture(self.tmp_root)

    def _write_minimal_ledger(self, rows: dict) -> None:
        # Provide a synthetic citation_graph.json so the cycle scan does
        # not blow up.
        graph_nodes = {
            cid: {"deps": list(row.get("deps") or [])}
            for cid, row in rows.items()
        }
        self.fx.write_graph({"nodes": graph_nodes, "edges": []})
        # Each row needs note_path that exists on disk + matching note_hash
        import hashlib
        for cid, row in rows.items():
            np = row.get("note_path") or f"docs/{cid}.md"
            row["note_path"] = np
            body = row.get("_body", f"# {cid}\n")
            row.pop("_body", None)
            (self.tmp_root / np).parent.mkdir(parents=True, exist_ok=True)
            (self.tmp_root / np).write_text(body, encoding="utf-8")
            row["note_hash"] = hashlib.sha256(body.encode("utf-8")).hexdigest()
            row.setdefault("deps", [])
        self.fx.write_ledger({"schema_version": 1, "rows": rows})

    def test_conditional_without_repair_class_warns(self):
        m = _import("audit_lint")
        _patch_repo_root(m, self.tmp_root)
        rows = {
            "test_cond": {
                "claim_id": "test_cond",
                "audit_status": "audited_conditional",
                "claim_type": "positive_theorem",
                "claim_scope": "real scope here",
                "effective_status": "audited_conditional",
                "notes_for_re_audit_if_any": "re-audit when X is closed",
                "auditor_family": "codex-gpt-5.5",
                "criticality": "leaf",
            },
        }
        self._write_minimal_ledger(rows)
        # Capture stdout
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = m.main()
        out = buf.getvalue()
        # Should pass (warnings only) but include a warning about repair-class
        self.assertEqual(rc, 0)
        self.assertIn("audited_conditional notes_for_re_audit_if_any", out)

    def test_legacy_auditor_family_warns(self):
        m = _import("audit_lint")
        _patch_repo_root(m, self.tmp_root)
        rows = {
            "legacy": {
                "claim_id": "legacy",
                "audit_status": "audited_clean",
                "claim_type": "positive_theorem",
                "claim_scope": "real scope",
                "effective_status": "retained",
                "auditor_family": "codex-current",  # legacy
                "auditor": "x",
                "criticality": "leaf",
                "load_bearing_step_class": "C",
            },
        }
        self._write_minimal_ledger(rows)
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            m.main()
        self.assertIn("legacy", buf.getvalue())
        self.assertIn("codex-current", buf.getvalue())

    def test_stale_top_level_timestamp_errors(self):
        m = _import("audit_lint")
        _patch_repo_root(m, self.tmp_root)
        # Build empty rows ledger but with stale timestamp key
        self.fx.write_graph({"nodes": {}, "edges": []})
        ledger = {
            "schema_version": 1,
            "generated_at": "2026-01-01T00:00:00+00:00",
            "rows": {},
        }
        self.fx.write_ledger(ledger)
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = m.main()
        self.assertEqual(rc, 1)
        self.assertIn("stale timestamp key", buf.getvalue())


class ComputeAuditQueueTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_root = Path(self._tmp.name)

    def test_cycle_break_instruction_names_manual_source_graph_repair(self):
        m = _import("compute_audit_queue")
        m.CYCLE_INVENTORY_PATH = self.tmp_root / "cycle_inventory.json"
        m.CYCLE_INVENTORY_PATH.write_text(
            json.dumps(
                {
                    "cycles": [
                        {
                            "cycle_id": "cycle-1",
                            "length": 2,
                            "max_transitive_descendants": 7,
                            "nodes": [
                                {"claim_id": "z_node"},
                                {"claim_id": "a_node"},
                            ],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        rows = {
            "a_node": {"transitive_descendants": 7, "audit_status": "unaudited"},
            "z_node": {"transitive_descendants": 7, "audit_status": "unaudited"},
        }

        targets = m.cycle_break_targets(rows)

        self.assertEqual(targets[0]["primary_break_target"], "a_node")
        self.assertNotIn("runner_pipeline", targets[0]["instruction"])
        self.assertIn("source-graph repair", targets[0]["instruction"])


class CodexAuditRunnerModelPolicyTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_root = Path(self._tmp.name)

    def _model(self, slug: str, *, priority: int = 0, xhigh: bool = True) -> dict:
        levels = [{"effort": "high"}]
        if xhigh:
            levels.append({"effort": "xhigh"})
        return {
            "slug": slug,
            "priority": priority,
            "supported_reasoning_levels": levels,
        }

    def test_best_cached_model_uses_highest_full_gpt_version_not_cache_order(self):
        m = _import_codex_audit_runner()
        (self.tmp_root / "models_cache.json").write_text(
            json.dumps(
                {
                    "models": [
                        self._model("gpt-5.4"),
                        self._model("gpt-5.3-codex"),
                        self._model("gpt-5.5"),
                        self._model("gpt-5.6-mini"),
                        self._model("gpt-6", xhigh=False),
                    ]
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.dict(os.environ, {"CODEX_HOME": str(self.tmp_root)}):
            model, source = m.best_cached_codex_model()

        self.assertEqual(model, "gpt-5.5")
        self.assertIn("models_cache.json", source)


if __name__ == "__main__":
    unittest.main()
