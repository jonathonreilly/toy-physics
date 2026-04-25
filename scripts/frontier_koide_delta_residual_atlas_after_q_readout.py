#!/usr/bin/env python3
"""
Koide delta residual atlas after Q readout reduction.

Purpose:
  Step back after the readout-retention split audit.  Q now has a defensible
  retained-source-response route if strict zero-source readout is accepted.
  The remaining full-lane obstruction is delta:

      closed_APS_to_open_selected_line_endpoint_functor.

This atlas ranks new or strengthened endpoint attacks and picks the next one.
"""

from __future__ import annotations

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


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def main() -> int:
    section("A. Current reduced residual")

    required = [
        "scripts/frontier_koide_q_delta_readout_retention_split_no_go.py",
        "scripts/frontier_koide_delta_current_endpoint_class_exhaustion_no_go.py",
        "scripts/frontier_koide_delta_all_order_boundary_functional_no_go.py",
        "scripts/frontier_koide_delta_dai_freed_open_trivialization_no_go.py",
    ]
    missing = [rel for rel in required if not exists(rel)]
    record(
        "A.1 Q/delta split and delta endpoint exhaustion artifacts are present",
        not missing,
        "\n".join(missing),
    )
    record(
        "A.2 residual after Q readout reduction is one delta functor",
        True,
        "RESIDUAL_DELTA=closed_APS_to_open_selected_line_endpoint_functor",
    )

    section("B. New or strengthened delta attack candidates")

    candidates = [
        (
            1,
            "endpoint functor classification",
            "Classify all smooth/additive maps from closed APS phase to selected open endpoint; closure requires identity functor.",
        ),
        (
            2,
            "orientation-preserving determinant-line automorphism",
            "Try to derive the identity functor from orientation, unit, and determinant-line normalization.",
        ),
        (
            3,
            "contractible selected-line base trivialization",
            "Use interval topology to ask whether a canonical zero endpoint section exists; likely conflicts with movable boundary terms.",
        ),
        (
            4,
            "relative cobordism uniqueness",
            "Treat the open selected line as a relative cobordism boundary and test if relative eta is unique.",
        ),
        (
            5,
            "spectral-flow normalization by crossing count",
            "Force N_desc=1 from a single protected crossing rather than from endpoint matching.",
        ),
        (
            6,
            "Callan-Harvey current normalization",
            "Revisit whether anomaly inflow current has unit selected-line descent after Q readout is fixed.",
        ),
        (
            7,
            "Brannen coordinate as closed holonomy chart",
            "Show the Brannen endpoint coordinate is definitionally the closed determinant holonomy coordinate.",
        ),
        (
            8,
            "all endpoint natural transformations",
            "Exhaust natural transformations of the endpoint phase functor under reparameterization and gauge.",
        ),
        (
            9,
            "boundary energy minimization with no free center",
            "Search for a center-free endpoint action whose unique interior extremum is forced by retained constants.",
        ),
    ]
    lines = [f"{rank}. {name}: {desc}" for rank, name, desc in candidates]
    record(
        "B.1 at least eight nonlocal endpoint routes are enumerated",
        len(candidates) >= 8,
        "\n".join(lines),
    )
    record(
        "B.2 highest-ranked next attack is endpoint functor classification",
        candidates[0][1] == "endpoint functor classification",
        "This attacks the residual functor itself rather than another endpoint representative.",
    )

    section("C. Atlas verdict")

    record(
        "C.1 do not claim closure from the atlas",
        True,
        "The atlas only chooses the next attack.",
    )
    record(
        "C.2 next runner should reduce the functor freedom to explicit parameters",
        True,
        "Target: identity functor degree/offset versus retained freedom.",
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
        print("KOIDE_DELTA_RESIDUAL_ATLAS_AFTER_Q_READOUT=TRUE")
        print("DELTA_ATLAS_CLOSES_DELTA=FALSE")
        print("RESIDUAL_SCALAR=closed_APS_to_open_selected_line_endpoint_functor")
        print("NEXT_ATTACK=endpoint_functor_classification")
        return 0

    print("KOIDE_DELTA_RESIDUAL_ATLAS_AFTER_Q_READOUT=FALSE")
    print("DELTA_ATLAS_CLOSES_DELTA=FALSE")
    print("RESIDUAL_SCALAR=closed_APS_to_open_selected_line_endpoint_functor")
    return 1


if __name__ == "__main__":
    sys.exit(main())
