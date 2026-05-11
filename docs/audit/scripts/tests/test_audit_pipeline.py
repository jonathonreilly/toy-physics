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
            "auditor_model": "gpt-5.5",
            "auditor_reasoning_effort": "xhigh",
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
            "auditor_model": "claude-opus-4.1",
            "auditor_reasoning_effort": "xhigh",
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

    def test_archived_failed_row_refreshes_note_hash(self):
        m = _import("seed_audit_ledger")
        _patch_repo_root(m, self.tmp_root)
        body = "# archived failed note\n\nRETRACTED.\n"
        note_path = "archive_unlanded/stale/NOTE.md"
        self.fx.write_note(note_path, body)
        import hashlib
        current_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        self.fx.write_graph({"nodes": {}})
        self.fx.write_ledger(
            {
                "schema_version": 1,
                "rows": {
                    "archived_failed": {
                        "claim_id": "archived_failed",
                        "note_path": note_path,
                        "title": "archived failed note",
                        "runner_path": None,
                        "deps": [],
                        "note_hash": "stalehash",
                        "previous_audits": [],
                        "audit_status": "audited_failed",
                        "claim_type": "no_go",
                        "claim_type_provenance": "audited",
                        "claim_scope": "archived failed scope",
                    }
                },
            }
        )

        seeded = m.seed()
        row = seeded["rows"]["archived_failed"]

        self.assertEqual(row["audit_status"], "audited_failed")
        self.assertEqual(row["note_hash"], current_hash)
        self.assertEqual(seeded["stats"]["preserved_archived_failed"], 1)


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

    def test_criticality_bump_soft_reset_propagates_as_retained(self):
        """A row in the criticality-bump soft-reset state (audit_in_progress
        + awaiting_cross_confirmation + first_audit on file) keeps its
        effective_status at retained. Downstream rows depending on it stay
        retained — the criticality bump does not force them to re-audit."""
        m = _import("compute_effective_status")
        soft_reset_row = {
            "claim_id": "soft_reset_dep",
            "deps": [],
            "audit_status": "audit_in_progress",
            "blocker": "awaiting_cross_confirmation",
            "claim_type": "positive_theorem",
            "claim_type_provenance": "audited_pending_cross_confirmation_after_criticality_bump",
            "cross_confirmation": {
                "first_audit": {
                    "auditor": "auditor-1",
                    "auditor_family": "codex-gpt-5.5",
                    "independence": "cross_family",
                    "verdict": "audited_clean",
                    "claim_type": "positive_theorem",
                    "claim_scope": "test scope",
                    "load_bearing_step_class": "A",
                },
                "second_audit": None,
                "status": "awaiting_second",
            },
        }
        rows = {
            "soft_reset_dep": soft_reset_row,
            "child": {
                "claim_id": "child",
                "deps": ["soft_reset_dep"],
                "audit_status": "audited_clean",
                "claim_type": "positive_theorem",
            },
        }
        new_rows, _ = m.compute_effective(rows)
        self.assertEqual(new_rows["soft_reset_dep"]["effective_status"], "retained")
        self.assertTrue(
            new_rows["soft_reset_dep"]["effective_status_reason"].startswith(
                "awaiting_cross_confirmation_after_criticality_bump:"
            )
        )
        # Child's chain still closes against the first-pass clean evidence.
        self.assertEqual(new_rows["child"]["effective_status"], "retained")

    def test_criticality_bump_soft_reset_with_disagreement_drops(self):
        """Once cross-confirmation disagrees, the soft-reset state ends and
        the row drops to audit_in_progress. Downstream rows then properly
        see the chain break and are flagged for re-audit."""
        m = _import("compute_effective_status")
        rows = {
            "disagreed_dep": {
                "claim_id": "disagreed_dep",
                "deps": [],
                "audit_status": "audit_in_progress",
                "blocker": "cross_confirmation_disagreement",  # not awaiting_cross_confirmation
                "claim_type": "positive_theorem",
                "claim_type_provenance": "audited_pending_cross_confirmation_after_criticality_bump",
                "cross_confirmation": {
                    "first_audit": {"verdict": "audited_clean"},
                    "second_audit": {"verdict": "audited_conditional"},
                    "status": "disagreement",
                },
            },
            "child": {
                "claim_id": "child",
                "deps": ["disagreed_dep"],
                "audit_status": "audited_clean",
                "claim_type": "positive_theorem",
            },
        }
        new_rows, _ = m.compute_effective(rows)
        self.assertEqual(new_rows["disagreed_dep"]["effective_status"], "audit_in_progress")
        self.assertEqual(new_rows["child"]["effective_status"], "retained_pending_chain")

    def test_born_critical_first_pass_does_not_trigger_soft_reset_path(self):
        """A born-critical claim in first-pass audit_in_progress (NOT from a
        criticality bump) keeps the standard audit_in_progress effective_status.
        The soft-reset path requires the specific provenance flag set by
        invalidate_stale_audits.py — apply_audit.py uses a different
        provenance for first-pass rows."""
        m = _import("compute_effective_status")
        rows = {
            "born_critical": {
                "claim_id": "born_critical",
                "deps": [],
                "audit_status": "audit_in_progress",
                "blocker": "awaiting_cross_confirmation",
                "claim_type": "positive_theorem",
                "claim_type_provenance": "audited_pending_cross_confirmation",  # NOT the bump suffix
                "cross_confirmation": {
                    "first_audit": {"verdict": "audited_clean"},
                    "second_audit": None,
                    "status": "awaiting_second",
                },
            },
        }
        new_rows, _ = m.compute_effective(rows)
        self.assertEqual(new_rows["born_critical"]["effective_status"], "audit_in_progress")

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

    def test_backfill_scope_reports_notice_not_warning(self):
        m = _import("audit_lint")
        _patch_repo_root(m, self.tmp_root)
        rows = {
            "legacy_scope": {
                "claim_id": "legacy_scope",
                "audit_status": "audited_conditional",
                "claim_type": "positive_theorem",
                "claim_scope": f"{m.BACKFILL_SCOPE_PREFIX}; placeholder",
                "effective_status": "audited_conditional",
                "notes_for_re_audit_if_any": "missing_bridge_theorem: repair",
                "auditor_family": "codex-gpt-5.5",
                "criticality": "leaf",
            },
        }
        self._write_minimal_ledger(rows)
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = m.main()
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("legacy_backfill_scope", out)
        self.assertIn("notices", out)
        self.assertNotIn("warnings:", out)

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


class InvalidateStaleAuditsCriticalityBumpTest(unittest.TestCase):
    """Per FRESH_LOOK_REQUIREMENTS.md §4, criticality bumps fall into three
    cases:

    - 'noop': the existing audit already qualifies, OR the verdict is
      terminal-non-clean (cross-confirmation doesn't apply).
    - 'soft_reset': audited_clean + non-weak independence + bump to
      critical without cross-confirmation. Mirrors apply_audit's
      first-pass flow: audit_in_progress + awaiting_cross_confirmation,
      first-audit evidence preserved as cross_confirmation.first_audit.
    - 'invalidate': audit fundamentally fails the new tier
      (e.g. weak independence bumping to high/critical).
    """

    def _categorize(self, *, audit_status="audited_clean", indep, cc_status, target):
        m = _import("invalidate_stale_audits")
        row = {"audit_status": audit_status, "independence": indep}
        if cc_status is not None:
            row["cross_confirmation"] = {"status": cc_status}
        return m._categorize_criticality_bump(row, target)

    def test_bump_to_medium_is_always_noop(self):
        # No special requirement at medium. Even weak audits stay live.
        self.assertEqual(self._categorize(indep="weak", cc_status=None, target="medium"), "noop")
        self.assertEqual(self._categorize(indep=None, cc_status=None, target="medium"), "noop")
        self.assertEqual(
            self._categorize(audit_status="audited_conditional", indep="cross_family",
                             cc_status=None, target="medium"),
            "noop",
        )

    def test_bump_to_high_with_non_weak_indep_is_noop(self):
        for indep in ("cross_family", "fresh_context", "strong"):
            self.assertEqual(self._categorize(indep=indep, cc_status=None, target="high"), "noop")

    def test_bump_to_high_with_weak_indep_invalidates(self):
        self.assertEqual(self._categorize(indep="weak", cc_status=None, target="high"), "invalidate")
        self.assertEqual(self._categorize(indep=None, cc_status=None, target="high"), "invalidate")

    def test_bump_to_critical_with_cross_confirmation_is_noop(self):
        for cc in ("confirmed", "third_confirmed_first", "third_confirmed_second"):
            self.assertEqual(
                self._categorize(indep="cross_family", cc_status=cc, target="critical"),
                "noop",
            )

    def test_bump_to_critical_with_weak_indep_invalidates(self):
        # Independence floor cannot be salvaged by cross-confirmation.
        self.assertEqual(
            self._categorize(indep="weak", cc_status="confirmed", target="critical"),
            "invalidate",
        )
        self.assertEqual(
            self._categorize(indep=None, cc_status=None, target="critical"),
            "invalidate",
        )

    def test_bump_to_critical_clean_no_cc_is_soft_reset(self):
        # The user's case: audited_clean + non-weak indep + bump to critical
        # without cross-confirmation -> soft reset, not full invalidate.
        self.assertEqual(
            self._categorize(indep="cross_family", cc_status=None, target="critical"),
            "soft_reset",
        )
        self.assertEqual(
            self._categorize(indep="fresh_context", cc_status=None, target="critical"),
            "soft_reset",
        )
        self.assertEqual(
            self._categorize(indep="cross_family", cc_status="awaiting_second", target="critical"),
            "soft_reset",
        )

    def test_terminal_non_clean_verdict_bumps_are_noops(self):
        # Cross-confirmation doesn't apply to non-clean verdicts; criticality
        # bump leaves them in their final state.
        for status in ("audited_conditional", "audited_numerical_match",
                       "audited_renaming", "audited_decoration", "audited_failed"):
            self.assertEqual(
                self._categorize(audit_status=status, indep="cross_family",
                                 cc_status=None, target="critical"),
                "noop",
                f"terminal verdict {status} should be noop",
            )

    def test_detect_invalidation_emits_distinct_reason_prefixes(self):
        m = _import("invalidate_stale_audits")
        with mock.patch.object(m.rc, "runner_sha256", return_value=None):
            base_snap = {
                "criticality": "high",
                "deps": [],
                "dep_effective_status": {},
                "runner_hash": None,
            }
            # Soft reset path: audited_clean + cross_family + bump to critical, no cc.
            row_soft = {
                "audit_status": "audited_clean",
                "deps": [],
                "criticality": "critical",
                "independence": "cross_family",
                "cross_confirmation": None,
                "audit_state_snapshot": base_snap,
            }
            reason = m.detect_invalidation(row_soft, {})
            self.assertIsNotNone(reason)
            self.assertTrue(reason.startswith("criticality_soft_reset:high->critical"))

            # Hard invalidate path: weak indep at high.
            row_hard = {
                "audit_status": "audited_clean",
                "deps": [],
                "criticality": "high",
                "independence": "weak",
                "cross_confirmation": None,
                "audit_state_snapshot": {**base_snap, "criticality": "leaf"},
            }
            reason = m.detect_invalidation(row_hard, {})
            self.assertIsNotNone(reason)
            self.assertTrue(reason.startswith("criticality_increased:leaf->high"))

            # Noop path: audited_clean + cross_family + bump to high.
            row_noop = {
                "audit_status": "audited_clean",
                "deps": [],
                "criticality": "high",
                "independence": "cross_family",
                "cross_confirmation": None,
                "audit_state_snapshot": {**base_snap, "criticality": "leaf"},
            }
            self.assertIsNone(m.detect_invalidation(row_noop, {}))

    def test_soft_reset_preserves_audit_evidence_as_first_audit(self):
        """A soft reset must mirror apply_audit's first-pass flow: clean
        evidence stays live as cross_confirmation.first_audit, audit_status
        flips to audit_in_progress + awaiting_cross_confirmation."""
        m = _import("invalidate_stale_audits")
        row = {
            "audit_status": "audited_clean",
            "auditor": "test-auditor-1",
            "auditor_family": "codex-gpt-5.5",
            "auditor_model": "gpt-5.5",
            "auditor_reasoning_effort": "xhigh",
            "independence": "cross_family",
            "audit_date": "2026-05-09T10:00:00+00:00",
            "claim_type": "positive_theorem",
            "claim_scope": "test scope",
            "load_bearing_step_class": "A",
            "cross_confirmation": None,
            "previous_audits": [],
        }
        out = m.soft_reset_to_cross_confirmation_pending(
            row, "criticality_soft_reset:high->critical"
        )
        self.assertEqual(out["audit_status"], "audit_in_progress")
        self.assertEqual(out["blocker"], "awaiting_cross_confirmation")
        self.assertEqual(out["claim_type_provenance"], "audited_pending_cross_confirmation_after_criticality_bump")
        cc = out["cross_confirmation"]
        self.assertEqual(cc["status"], "awaiting_second")
        self.assertIsNone(cc["second_audit"])
        first = cc["first_audit"]
        self.assertEqual(first["auditor"], "test-auditor-1")
        self.assertEqual(first["auditor_family"], "codex-gpt-5.5")
        self.assertEqual(first["independence"], "cross_family")
        self.assertEqual(first["claim_type"], "positive_theorem")
        self.assertEqual(first["claim_scope"], "test scope")
        self.assertEqual(first["load_bearing_step_class"], "A")
        self.assertEqual(first["verdict"], "audited_clean")
        # The clean evidence must NOT be archived to previous_audits — it
        # is still live as the first audit. apply_audit's first-pass flow
        # also doesn't archive on first-pass.
        self.assertEqual(out["previous_audits"], [])
        # The auditor + claim_type fields must remain on the live row
        # (the cross-confirmation second pass needs them for comparison).
        self.assertEqual(out["auditor"], "test-auditor-1")
        self.assertEqual(out["claim_type"], "positive_theorem")
        self.assertEqual(out["claim_scope"], "test scope")


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


class CodexAuditRunnerReauditCandidatesTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_root = Path(self._tmp.name)

    def test_reaudit_role_records_independence_against_prior_auditor(self):
        m = _import_codex_audit_runner()

        same_family = {
            "audit_status": "audited_conditional",
            "auditor_family": "codex-gpt-5.5",
        }
        role, independence = m.determine_audit_role(
            same_family,
            "codex-gpt-5.5",
            is_reaudit_candidate=True,
        )
        self.assertEqual((role, independence), ("reaudit", "fresh_context"))

        cross_family = {
            "audit_status": "audited_failed",
            "auditor_family": "claude-sonnet",
        }
        role, independence = m.determine_audit_role(
            cross_family,
            "codex-gpt-5.5",
            is_reaudit_candidate=True,
        )
        self.assertEqual((role, independence), ("reaudit", "cross_family"))

    def test_reaudit_role_still_skips_judicial_blockers(self):
        m = _import_codex_audit_runner()

        role, reason = m.determine_audit_role(
            {
                "audit_status": "audited_conditional",
                "blocker": "cross_confirmation_disagreement",
            },
            "codex-gpt-5.5",
            is_reaudit_candidate=True,
        )

        self.assertEqual(role, "skip")
        self.assertIn("judicial review needed", reason)

    def test_load_reaudit_candidates_normalizes_sorts_and_filters_streams(self):
        m = _import_codex_audit_runner()
        path = self.tmp_root / "reaudit_candidates.json"
        path.write_text(
            json.dumps(
                {
                    "candidates": [
                        {
                            "claim_id": "medium_dep",
                            "criticality": "medium",
                            "criticality_rank": 1,
                            "transitive_descendants": 10,
                            "load_bearing_score": 2.0,
                        }
                    ],
                    "runner_drift_candidates": [
                        {
                            "claim_id": "critical_runner",
                            "criticality": "critical",
                            "criticality_rank": 3,
                            "transitive_descendants": 1,
                            "load_bearing_score": 1.0,
                            "queue_reason": "custom_runner_reason",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        m.REAUDIT_CANDIDATES_PATH = path

        rows = m.load_reaudit_candidates()

        self.assertEqual([r["claim_id"] for r in rows], ["critical_runner", "medium_dep"])
        self.assertTrue(all(r["ready"] for r in rows))
        self.assertEqual(rows[0]["queue_reason"], "custom_runner_reason")
        self.assertEqual(rows[1]["queue_reason"], "reaudit_candidate")
        self.assertEqual(rows[1]["audit_status"], "unaudited")

        dep_only = m.load_reaudit_candidates(include_runner_drift=False)
        self.assertEqual([r["claim_id"] for r in dep_only], ["medium_dep"])


class RelabelUnverifiedCodexAuditsTest(unittest.TestCase):
    def test_relabels_below_floor_row_and_matching_cross_confirmation(self):
        m = _import("relabel_unverified_codex_audits")
        row = {
            "audit_status": "audited_conditional",
            "auditor": "codex-audit-loop",
            "auditor_family": "codex-gpt-5",
            "cross_confirmation": {
                "first_audit": {
                    "auditor": "codex-audit-loop",
                    "auditor_family": "codex-gpt-5",
                },
                "second_audit": {
                    "auditor": "independent-human",
                    "auditor_family": "codex-gpt-5",
                },
            },
        }

        relabeled, cc_count = m.relabel_row(row)

        self.assertTrue(relabeled)
        self.assertEqual(cc_count, 1)
        self.assertEqual(row["auditor_family"], "codex-gpt-5.5")
        self.assertEqual(row["previous_auditor_family"], "codex-gpt-5")
        self.assertEqual(
            row["cross_confirmation"]["first_audit"]["auditor_family"],
            "codex-gpt-5.5",
        )
        self.assertEqual(
            row["cross_confirmation"]["second_audit"]["auditor_family"],
            "codex-gpt-5",
        )
        self.assertEqual(
            row["relabel_reason"],
            "operator_pre_floor_policy_relabel_2026-05-06",
        )

    def test_skips_pending_or_already_marked_rows(self):
        m = _import("relabel_unverified_codex_audits")
        self.assertFalse(
            m.is_unverified_codex_label(
                {"audit_status": "unaudited", "auditor_family": "codex-gpt-5"}
            )
        )
        self.assertFalse(
            m.is_unverified_codex_label(
                {
                    "audit_status": "audited_clean",
                    "auditor_family": "codex-gpt-5",
                    "previous_auditor_family": "codex-current",
                }
            )
        )
        self.assertFalse(
            m.is_unverified_codex_label(
                {"audit_status": "audited_clean", "auditor_family": "claude-opus"}
            )
        )

    def test_audit_lint_model_floor_helper(self):
        m = _import("audit_lint")
        self.assertFalse(m.codex_family_meets_minimum("codex-gpt-5"))
        self.assertTrue(m.codex_family_meets_minimum("codex-gpt-5.5"))
        self.assertTrue(m.codex_family_meets_minimum("codex-gpt-6"))
        self.assertTrue(m.codex_family_meets_minimum("claude-opus"))


class RestoreOveraggressivelyInvalidatedAuditsTest(unittest.TestCase):
    """One-shot restoration of audits over-aggressively invalidated before
    PR #907's policy refinement."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp_root = Path(self._tmp.name)
        self.fx = CleanLedgerFixture(self.tmp_root)

    def _archived_audit(self, *, audit_status="audited_clean",
                        independence="cross_family", cc_status=None,
                        invalidation_reason="criticality_increased:medium->critical",
                        claim_type="positive_theorem",
                        auditor_family="codex-gpt-5.5",
                        notes_for_re_audit_if_any=None):
        archived = {
            "audit_status": audit_status,
            "independence": independence,
            "auditor": "codex-test",
            "auditor_family": auditor_family,
            "claim_type": claim_type,
            "claim_scope": "test scope",
            "load_bearing_step_class": "A",
            "audit_state_snapshot": {"criticality": "leaf", "deps": []},
            "audit_date": "2026-05-09T11:00:00+00:00",
            "archived_at": "2026-05-09T15:00:00+00:00",
            "invalidation_reason": invalidation_reason,
        }
        if notes_for_re_audit_if_any is not None:
            archived["notes_for_re_audit_if_any"] = notes_for_re_audit_if_any
        if cc_status is not None:
            archived["cross_confirmation"] = {
                "first_audit": {"verdict": "audited_clean"},
                "second_audit": None,
                "status": cc_status,
            }
        return archived

    def _seed_with_archived(self, cid: str, archived: dict, *,
                            current_status="unaudited") -> dict:
        return {
            "claim_id": cid,
            "note_path": f"docs/{cid.upper()}.md",
            "note_hash": "deadbeef",
            "deps": [],
            "audit_status": current_status,
            "previous_audits": [archived],
        }

    def _import_and_patch(self):
        m = _import("restore_overaggressively_invalidated_audits")
        m.REPO_ROOT = self.tmp_root
        m.DATA_DIR = self.tmp_root / "docs" / "audit" / "data"
        m.LEDGER_PATH = m.DATA_DIR / "audit_ledger.json"
        return m

    def test_categorize_archived_mirrors_invalidate_policy(self):
        m = self._import_and_patch()
        # leaf/medium: any audit qualifies
        self.assertEqual(
            m.categorize_criticality_bump_for_archived(
                self._archived_audit(audit_status="audited_conditional"), "medium"),
            "noop",
        )
        # high requires non-weak
        self.assertEqual(
            m.categorize_criticality_bump_for_archived(
                self._archived_audit(independence="weak"), "high"),
            "invalidate",
        )
        self.assertEqual(
            m.categorize_criticality_bump_for_archived(
                self._archived_audit(independence="cross_family"), "high"),
            "noop",
        )
        # critical: cc-confirmed -> noop, weak -> invalidate, otherwise soft_reset
        self.assertEqual(
            m.categorize_criticality_bump_for_archived(
                self._archived_audit(cc_status="confirmed"), "critical"),
            "noop",
        )
        self.assertEqual(
            m.categorize_criticality_bump_for_archived(
                self._archived_audit(independence="weak"), "critical"),
            "invalidate",
        )
        self.assertEqual(
            m.categorize_criticality_bump_for_archived(
                self._archived_audit(independence="cross_family"), "critical"),
            "soft_reset",
        )

    def test_select_restore_candidates_picks_criticality_increased(self):
        m = self._import_and_patch()
        rows = {
            "ok_to_restore": self._seed_with_archived(
                "ok_to_restore",
                self._archived_audit(invalidation_reason="criticality_increased:leaf->medium"),
            ),
            "soft_reset_target": self._seed_with_archived(
                "soft_reset_target",
                self._archived_audit(
                    invalidation_reason="criticality_increased:high->critical",
                    independence="cross_family", cc_status=None,
                ),
            ),
            "weak_at_critical_skip": self._seed_with_archived(
                "weak_at_critical_skip",
                self._archived_audit(
                    invalidation_reason="criticality_increased:leaf->critical",
                    independence="weak",
                ),
            ),
        }
        crit, dep_weak = m.select_restore_candidates(rows)
        self.assertIn("ok_to_restore", crit)
        self.assertIn("soft_reset_target", crit)
        self.assertNotIn("weak_at_critical_skip", crit)
        self.assertEqual(dep_weak, [])

    def test_select_restore_candidates_picks_dep_weakened_only_from_crit_set(self):
        m = self._import_and_patch()
        # downstream_in_set's dep is in crit_set; downstream_orphan's dep is not.
        rows = {
            "soft_reset_dep": self._seed_with_archived(
                "soft_reset_dep",
                self._archived_audit(
                    invalidation_reason="criticality_increased:medium->critical",
                ),
            ),
            "downstream_in_set": self._seed_with_archived(
                "downstream_in_set",
                self._archived_audit(
                    invalidation_reason="dep_weakened:soft_reset_dep:retained_bounded->audit_in_progress",
                    claim_type="positive_theorem",
                ),
            ),
            "downstream_orphan": self._seed_with_archived(
                "downstream_orphan",
                self._archived_audit(
                    invalidation_reason="dep_weakened:unrelated_dep:retained->unaudited",
                    claim_type="positive_theorem",
                ),
            ),
        }
        crit, dep_weak = m.select_restore_candidates(rows)
        self.assertIn("soft_reset_dep", crit)
        dep_weak_cids = {cid for cid, _, _ in dep_weak}
        self.assertEqual(dep_weak_cids, {"downstream_in_set"})

    def test_dep_weakened_not_restored_when_dep_remains_weaker(self):
        m = self._import_and_patch()
        rows = {
            "conditional_dep": self._seed_with_archived(
                "conditional_dep",
                self._archived_audit(
                    audit_status="audited_conditional",
                    invalidation_reason="criticality_increased:high->critical",
                    notes_for_re_audit_if_any="other: terminal conditional remains conditional",
                ),
            ),
            "downstream_still_weakened": self._seed_with_archived(
                "downstream_still_weakened",
                self._archived_audit(
                    audit_status="audited_numerical_match",
                    invalidation_reason=(
                        "dep_weakened:conditional_dep:"
                        "audited_numerical_match->audited_conditional"
                    ),
                ),
            ),
        }
        crit, dep_weak = m.select_restore_candidates(rows)
        self.assertIn("conditional_dep", crit)
        self.assertEqual(dep_weak, [])

    def test_lint_incompatible_archived_audits_stay_invalidated(self):
        m = self._import_and_patch()
        missing_scope = self._archived_audit(
            invalidation_reason="criticality_increased:leaf->medium",
        )
        missing_scope.pop("claim_scope")
        rows = {
            "missing_scope": self._seed_with_archived("missing_scope", missing_scope),
            "low_model_floor": self._seed_with_archived(
                "low_model_floor",
                self._archived_audit(
                    invalidation_reason="criticality_increased:leaf->medium",
                    auditor_family="codex-gpt-5",
                ),
            ),
            "conditional_missing_repair_class": self._seed_with_archived(
                "conditional_missing_repair_class",
                self._archived_audit(
                    audit_status="audited_conditional",
                    invalidation_reason="criticality_increased:leaf->medium",
                ),
            ),
        }
        crit, dep_weak = m.select_restore_candidates(rows)
        self.assertEqual(crit, {})
        self.assertEqual(dep_weak, [])

    def test_noncritical_blocker_keeps_candidate_invalidated(self):
        m = self._import_and_patch()
        archived = self._archived_audit(
            invalidation_reason="criticality_increased:medium->critical",
        )
        archived["audit_state_snapshot"] = {
            "criticality": "medium",
            "deps": ["weak_dep"],
            "dep_effective_status": {"weak_dep": "retained_bounded"},
        }
        rows = {
            "candidate": self._seed_with_archived("candidate", archived),
            "weak_dep": {
                "claim_id": "weak_dep",
                "audit_status": "audited_conditional",
                "effective_status": "audited_conditional",
                "note_path": "docs/WEAK_DEP.md",
                "deps": [],
            },
        }
        rows["candidate"]["deps"] = ["weak_dep"]

        crit, dep_weak = m.select_restore_candidates(rows)
        self.assertEqual(crit, {})
        self.assertEqual(dep_weak, [])

    def test_other_invalidation_reasons_are_not_touched(self):
        m = self._import_and_patch()
        rows = {
            "hash_drift": self._seed_with_archived(
                "hash_drift",
                self._archived_audit(invalidation_reason="runner_hash_changed:abc->def"),
            ),
            "deps_changed": self._seed_with_archived(
                "deps_changed",
                self._archived_audit(
                    invalidation_reason="deps_changed:dep_added:new_dep_xyz",
                ),
            ),
            "claim_scope_drift": self._seed_with_archived(
                "claim_scope_drift",
                self._archived_audit(
                    invalidation_reason="dep_claim_scope_changed:some_dep",
                ),
            ),
        }
        crit, dep_weak = m.select_restore_candidates(rows)
        self.assertEqual(crit, {})
        self.assertEqual(dep_weak, [])

    def test_restore_audit_from_previous_copies_archived_fields_back(self):
        m = self._import_and_patch()
        archived = self._archived_audit(
            audit_status="audited_clean",
            independence="fresh_context",
            invalidation_reason="criticality_increased:leaf->critical",
            cc_status=None,
        )
        row = {
            "claim_id": "test_row",
            "note_path": "docs/TEST.md",
            "note_hash": "abc",
            "deps": [],
            "audit_status": "unaudited",  # over-aggressively invalidated
            "claim_type": None,
            "claim_type_provenance": "needs_reaudit_after_invalidation",
            "auditor": None,
            "previous_audits": [archived],
        }
        new_row = m.restore_audit_from_previous(row)
        self.assertEqual(new_row["audit_status"], "audited_clean")
        self.assertEqual(new_row["independence"], "fresh_context")
        self.assertEqual(new_row["claim_type"], "positive_theorem")
        self.assertEqual(new_row["claim_scope"], "test scope")
        self.assertEqual(new_row["auditor"], "codex-test")
        # The archive entry is removed from previous_audits.
        self.assertEqual(new_row["previous_audits"], [])

    def test_idempotent_on_already_audited_rows(self):
        """A row that's currently audited (not unaudited) is not a candidate."""
        m = self._import_and_patch()
        rows = {
            "live_audited": dict(
                self._seed_with_archived(
                    "live_audited",
                    self._archived_audit(invalidation_reason="criticality_increased:leaf->medium"),
                    current_status="audited_clean",
                )
            ),
        }
        crit, dep_weak = m.select_restore_candidates(rows)
        self.assertEqual(crit, {})
        self.assertEqual(dep_weak, [])

    def test_main_writes_restored_ledger(self):
        m = self._import_and_patch()
        m.DATA_DIR.mkdir(parents=True, exist_ok=True)
        archived_clean = self._archived_audit(
            invalidation_reason="criticality_increased:leaf->medium",
        )
        archived_dep_weak = self._archived_audit(
            invalidation_reason="dep_weakened:soft_reset_dep:retained->unaudited",
        )
        ledger = {
            "schema_version": 1,
            "rows": {
                "soft_reset_dep": self._seed_with_archived("soft_reset_dep", archived_clean),
                "downstream": self._seed_with_archived("downstream", archived_dep_weak),
            },
        }
        m.LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True))

        with mock.patch.object(sys, "argv", ["restore", ""]):
            sys.argv = ["restore"]
            rc = m.main()
        self.assertEqual(rc, 0)

        out = json.loads(m.LEDGER_PATH.read_text(encoding="utf-8"))
        soft = out["rows"]["soft_reset_dep"]
        down = out["rows"]["downstream"]
        self.assertEqual(soft["audit_status"], "audited_clean")
        self.assertEqual(soft["claim_type"], "positive_theorem")
        self.assertEqual(soft["previous_audits"], [])
        self.assertEqual(down["audit_status"], "audited_clean")
        self.assertEqual(down["previous_audits"], [])


if __name__ == "__main__":
    unittest.main()
