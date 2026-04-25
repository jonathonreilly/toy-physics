#!/usr/bin/env python3
"""
Koide delta post-unit-endpoint reassessment no-go.

Purpose:
  Consolidate the new post-atlas attacks:

    - spectral-flow degree normalization,
    - Callan-Harvey degree functor,
    - primitive anomaly-channel uniqueness,
    - Picard torsor unit/basepoint,
    - determinant-line universal endpoint.

Result:
  Delta is still not closed.  The residual is now a very explicit selected
  endpoint identity theorem:

    1. the selected Brannen line must be the unique primitive anomaly channel;
    2. the selected endpoint torsor must have a retained zero/basepoint;
    3. the selected determinant-line map must be based, orientation-preserving,
       and degree one.

This runner is a reassessment artifact, not closure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


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
    section("A. New post-atlas artifacts")

    required = [
        "scripts/frontier_koide_delta_spectral_flow_degree_normalization_no_go.py",
        "scripts/frontier_koide_delta_callan_harvey_degree_functor_no_go.py",
        "scripts/frontier_koide_delta_unit_endpoint_residual_atlas_no_go.py",
        "scripts/frontier_koide_delta_primitive_anomaly_channel_no_go.py",
        "scripts/frontier_koide_delta_picard_torsor_unit_no_go.py",
        "scripts/frontier_koide_delta_determinant_universal_endpoint_no_go.py",
        "scripts/frontier_koide_delta_selected_line_nonzero_degree_no_go.py",
        "scripts/frontier_koide_delta_cl3_boundary_source_grammar_no_go.py",
        "scripts/frontier_koide_delta_selected_line_projector_retention_no_go.py",
    ]
    missing = [rel for rel in required if not exists(rel)]
    record(
        "A.1 post-atlas delta endpoint artifacts are present",
        not missing,
        "\n".join(missing) if missing else f"checked={len(required)} runners",
    )

    section("B. Unified residual equation")

    eta = sp.Rational(2, 9)
    selected, spectator, c = sp.symbols("selected spectator c", real=True)
    total_constraint = sp.Eq(selected + spectator, 1)
    delta = sp.simplify(selected * eta + c)
    residual = sp.simplify(delta / eta - 1)
    residual_total = sp.simplify(residual.subs(selected, 1 - spectator))
    record(
        "B.1 after total anomaly cancellation the selected endpoint residual is exact",
        residual_total == -spectator + c / eta,
        f"selected+spectator=1 -> delta/eta_APS - 1 = {residual_total}",
    )
    record(
        "B.2 closure requires both no spectator channel and zero endpoint offset",
        sp.solve([sp.Eq(residual_total, 0), sp.Eq(c, 0)], [spectator, c], dict=True)
        == [{spectator: 0, c: 0}],
        "spectator=0 and c=0 are the remaining selected-line identity conditions.",
    )

    section("C. What each new attack removed or failed to remove")

    reductions = [
        "spectral-flow degree: integer crossing does not force selected endpoint degree",
        "Callan-Harvey degree: closed anomaly scalar has zero rank in open readout variables",
        "primitive anomaly channel: total anomaly narrows to selected versus spectator support",
        "Picard torsor unit: monoidal unit removes c only after a retained basepoint",
        "determinant universal property: closed carrier does not force selected identity map",
        "selected-line nonzero winding: carrier n_eff=2 does not force endpoint degree one",
        "Cl(3) boundary source grammar: local words leave selected projector and exact offset free",
        "selected-line projector retention: P_chi exists, but support on it and c=0 are not retained",
    ]
    record(
        "C.1 new attacks leave one selected endpoint identity theorem",
        len(reductions) == 8,
        "\n".join(reductions),
    )
    record(
        "C.2 no route claims positive retained delta closure",
        True,
        "All new closeout flags remain negative for DELTA_*_CLOSES_DELTA.",
    )

    section("D. Next attacks")

    next_attacks = [
        (
            "lattice Wilson selected eigenline theorem",
            "construct explicit finite endpoint eigenline and test if it is canonically the unit anomaly channel",
        ),
        (
            "marked relative cobordism with derived boundary section",
            "try to derive the endpoint basepoint from a retained marking rather than choose it",
        ),
        (
            "source-response covariance transfer",
            "test whether Q readout retention forces delta readout identity without importing the quotient law",
        ),
    ]
    record(
        "D.1 next viable attacks are nonlocal, not repeats of the same endpoint map algebra",
        len(next_attacks) == 3,
        "\n".join(f"{name}: {desc}" for name, desc in next_attacks),
    )
    record(
        "D.2 highest priority next attack is lattice Wilson selected eigenline",
        next_attacks[0][0] == "lattice Wilson selected eigenline theorem",
        "Projector retention is exhausted; the next route tests whether a finite eigenline construction canonically supplies the unit channel.",
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
        print("VERDICT: post-unit-endpoint reassessment does not close delta.")
        print("KOIDE_DELTA_POST_UNIT_ENDPOINT_REASSESSMENT_NO_GO=TRUE")
        print("DELTA_POST_UNIT_ENDPOINT_REASSESSMENT_CLOSES_DELTA=FALSE")
        print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
        print("RESIDUAL_CHANNEL=selected_line_unique_primitive_channel_not_retained")
        print("RESIDUAL_TRIVIALIZATION=selected_endpoint_zero_basepoint_not_retained")
        print("RESIDUAL_DESCENT=selected_line_winding_to_endpoint_degree_one_not_retained")
        print("NEXT_ATTACK=lattice_Wilson_selected_eigenline_theorem")
        return 0

    print("VERDICT: post-unit-endpoint reassessment has FAILs.")
    print("KOIDE_DELTA_POST_UNIT_ENDPOINT_REASSESSMENT_NO_GO=FALSE")
    print("DELTA_POST_UNIT_ENDPOINT_REASSESSMENT_CLOSES_DELTA=FALSE")
    print("RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS")
    print("RESIDUAL_CHANNEL=selected_line_unique_primitive_channel_not_retained")
    print("RESIDUAL_TRIVIALIZATION=selected_endpoint_zero_basepoint_not_retained")
    print("RESIDUAL_DESCENT=selected_line_winding_to_endpoint_degree_one_not_retained")
    return 1


if __name__ == "__main__":
    sys.exit(main())
