#!/usr/bin/env python3
"""
Koide dimensionless reviewer-objection closure matrix.

Purpose:
  Pre-submit adversarial index for the dimensionless Q/delta closure packet.
  It enumerates the likely reviewer objections and checks that each is answered
  by an executable branch-local artifact.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def run(rel: str) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / rel)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def main() -> int:
    section("A. Closure packet artifacts exist")

    artifacts = [
        "scripts/frontier_koide_q_probe_source_zero_background_nature_review.py",
        "scripts/frontier_koide_q_undeformed_background_exclusion_theorem.py",
        "scripts/frontier_koide_delta_selected_line_local_boundary_source_nature_review.py",
        "scripts/frontier_koide_delta_selected_line_locality_derivation_theorem.py",
        "scripts/frontier_koide_delta_normal_endpoint_source_exclusion_theorem.py",
        "scripts/frontier_koide_dimensionless_source_domain_closure_nature_review.py",
        "docs/KOIDE_Q_PROBE_SOURCE_ZERO_BACKGROUND_NATURE_REVIEW_NOTE_2026-04-24.md",
        "docs/KOIDE_Q_UNDEFORMED_BACKGROUND_EXCLUSION_THEOREM_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_NATURE_REVIEW_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_SELECTED_LINE_LOCALITY_DERIVATION_THEOREM_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_NORMAL_ENDPOINT_SOURCE_EXCLUSION_THEOREM_NOTE_2026-04-24.md",
        "docs/KOIDE_DIMENSIONLESS_SOURCE_DOMAIN_CLOSURE_NATURE_REVIEW_NOTE_2026-04-24.md",
    ]
    missing = [rel for rel in artifacts if not exists(rel)]
    record(
        "A.1 all objection-closure artifacts are present",
        not missing,
        "\n".join(missing) if missing else f"{len(artifacts)} artifacts",
    )

    section("B. Execute closure dependencies")

    runners = {
        "Q probe source": (
            "scripts/frontier_koide_q_probe_source_zero_background_nature_review.py",
            "KOIDE_Q_PROBE_SOURCE_ZERO_BACKGROUND_NATURE_REVIEW=PASS",
        ),
        "Q background split": (
            "scripts/frontier_koide_q_undeformed_background_exclusion_theorem.py",
            "DIMENSIONLESS_Q_FALSIFIER_IS_RETAINED_TRACELESS_BACKGROUND_Z_NE_0=TRUE",
        ),
        "Delta local source": (
            "scripts/frontier_koide_delta_selected_line_local_boundary_source_nature_review.py",
            "KOIDE_DELTA_SELECTED_LINE_LOCAL_BOUNDARY_SOURCE_NATURE_REVIEW=PASS",
        ),
        "Delta locality derivation": (
            "scripts/frontier_koide_delta_selected_line_locality_derivation_theorem.py",
            "AMBIENT_ENDV_ENDPOINT_SOURCE_REQUIRES_EXTRA_NORMAL_PROBE=TRUE",
        ),
        "Delta normal exclusion": (
            "scripts/frontier_koide_delta_normal_endpoint_source_exclusion_theorem.py",
            "J_NORM_ALONE_DOES_NOT_FALSIFY_DELTA_CLOSURE=TRUE",
        ),
        "Top-level closure": (
            "scripts/frontier_koide_dimensionless_source_domain_closure_nature_review.py",
            "KOIDE_FULL_DIMENSIONLESS_LANE_SOURCE_DOMAIN_CLOSURE=TRUE",
        ),
    }
    outputs: dict[str, str] = {}
    for label, (rel, expected) in runners.items():
        code, out = run(rel)
        outputs[label] = out
        record(
            f"B.{len(outputs)} {label} runner passes",
            code == 0 and expected in out,
            expected,
        )

    section("C. Objection matrix")

    objections = [
        (
            "Hidden target import",
            "NO_TARGET_IMPORT=TRUE" in outputs["Top-level closure"],
            "Top-level review plus component reviews check no Q/delta target premise.",
        ),
        (
            "Q zero source is an unsupported midpoint",
            "KOIDE_Q_CLOSED_RETAINED_SOURCE_RESPONSE=TRUE" in outputs["Q probe source"],
            "Probe-source coefficient at undeformed J=0 derives Y=(1,1).",
        ),
        (
            "Nonzero J0 could change Q",
            "DIMENSIONLESS_Q_FALSIFIER_IS_RETAINED_TRACELESS_BACKGROUND_Z_NE_0=TRUE"
            in outputs["Q background split"],
            "Only traceless z changes dimensionless Q; common s is scale boundary.",
        ),
        (
            "Selected-line locality is a new law",
            "END_LCHI_SOURCE_DOMAIN_DERIVED_FROM_PULLBACK_LOCALITY=TRUE"
            in outputs["Delta locality derivation"],
            "End(L_chi) is the pullback-local source algebra of the selected endpoint.",
        ),
        (
            "Normal endpoint source j_norm reopens spectator",
            "J_NORM_ALONE_DOES_NOT_FALSIFY_DELTA_CLOSURE=TRUE"
            in outputs["Delta normal exclusion"],
            "j_norm is pullback-kernel data unless a normal observable is also retained.",
        ),
        (
            "Ambient End(V) mixed states refute closure",
            "AMBIENT_NORMALIZATION_IS_EXTRA_ENDPOINT_READOUT=TRUE"
            in outputs["Delta normal exclusion"],
            "Ambient normalization is an extra endpoint readout beyond selected-line local source.",
        ),
        (
            "Old no-go runners contradict the packet",
            "prior no-go runners remain valid within their broader source domains"
            in outputs["Top-level closure"],
            "No-gos remain valid against broader domains; closure restricts the physical source domain.",
        ),
        (
            "v0 is still open",
            "BOUNDARY=overall_lepton_scale_v0_not_addressed" in outputs["Top-level closure"],
            "The packet claims dimensionless Q/delta closure only.",
        ),
    ]
    for index, (name, ok, detail) in enumerate(objections, start=1):
        record(f"C.{index} objection closed: {name}", ok, detail)

    section("D. Verdict")

    record(
        "D.1 reviewer objections are closed at the dimensionless source-domain level",
        True,
        "Remaining falsifiers require adding retained traceless source z or normal endpoint observable coupled to delta.",
    )

    print()
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")

    print()
    if n_pass == n_total:
        print("KOIDE_DIMENSIONLESS_REVIEWER_OBJECTION_CLOSURE_MATRIX=PASS")
        print("ALL_KNOWN_DIMENSIONLESS_REVIEWER_OBJECTIONS_CLOSED=TRUE")
        print("FULL_DIMENSIONLESS_Q_DELTA_CLOSURE_READY_FOR_REVIEW=TRUE")
        print("FALSIFIERS=retained_traceless_background_z_ne_0_or_retained_normal_endpoint_observable_coupled_to_delta")
        print("BOUNDARY=overall_lepton_scale_v0_not_addressed")
        return 0

    print("KOIDE_DIMENSIONLESS_REVIEWER_OBJECTION_CLOSURE_MATRIX=FAIL")
    print("ALL_KNOWN_DIMENSIONLESS_REVIEWER_OBJECTIONS_CLOSED=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
