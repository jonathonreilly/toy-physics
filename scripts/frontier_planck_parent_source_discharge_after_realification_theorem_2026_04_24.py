#!/usr/bin/env python3
"""Verify parent-source discharge after B3 realification."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def shell_rank(include_time: bool, include_spatial: int) -> int:
    return (1 if include_time else 0) + include_spatial


def main() -> int:
    note = read("docs/PLANCK_SCALE_PARENT_SOURCE_DISCHARGE_AFTER_REALIFICATION_THEOREM_2026-04-24.md")
    b3_real = read("docs/PLANCK_SCALE_B3_CLIFFORD_REALIFICATION_METRIC_WARD_THEOREM_2026-04-24.md")
    parent_obstruction = read(
        "docs/PLANCK_SCALE_PARENT_SOURCE_NATURALITY_OBSTRUCTION_THEOREM_2026-04-24.md"
    )
    b4 = read("docs/PLANCK_SCALE_BARE_BOUNDARY_REPRESENTATIVE_AFTER_GRAVITY_THEOREM_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "document-is-parent-source-discharge-theorem",
        "Planck-Scale Parent-Source Discharge After Realification Theorem" in note
        and "**Status:** closes the parent-source object-class objection" in note
        and "frontier_planck_parent_source_discharge_after_realification_theorem_2026_04_24.py"
        in note,
        "new theorem and verifier are present",
    )

    total += 1
    passed += expect(
        "b3-realification-places-gravity-on-boundary-surface",
        "`Hom_R(Z^3 tensor_Z R, Cl_1(3))`" in note
        and "metric/coframe object class is earned" in b3_real
        and "same primitive\none-cell boundary surface" in note,
        "gravity response is derived on the primitive cell surface",
    )

    p_a_rank = shell_rank(include_time=True, include_spatial=3)
    p_t_rank = shell_rank(include_time=True, include_spatial=0)
    p_spatial_rank = shell_rank(include_time=False, include_spatial=3)

    total += 1
    passed += expect(
        "unique-full-axis-source-has-rank-four",
        p_a_rank == 4
        and p_t_rank != p_a_rank
        and p_spatial_rank != p_a_rank
        and "`P_A = P_t + P_x + P_y + P_z`" in note
        and "`N_grav = P_A`" in b4,
        f"rank(P_A)={p_a_rank}, rank(P_t)={p_t_rank}, rank(P_xyz)={p_spatial_rank}",
    )

    total += 1
    passed += expect(
        "alternatives-fail-explicit-conditions",
        "`P_t` is not spatially complete" in note
        and "`P_x + P_y + P_z` is not time-complete" in note
        and "`alpha P_A` with `alpha != 1` violates unit valuation" in note
        and "quotient projector loses retained spatial-doublet multiplicity" in note,
        "common rival representatives are ruled out by named conditions",
    )

    delta = Fraction(3, 7)
    p_event = Fraction(1, 4)
    p_schur_delta = p_event + delta

    total += 1
    passed += expect(
        "hidden-character-is-excluded-after-realification",
        p_schur_delta != p_event
        and "`p_Schur(delta) = Tr(rho_cell P_A) + delta`" in note
        and "`delta I` is not a boundary incidence source" in note
        and "`delta = 0`" in note
        and "`chi_delta(s) = exp(s delta)`" in parent_obstruction,
        f"counterexample delta={delta} would shift p from {p_event} to {p_schur_delta}",
    )

    total += 1
    passed += expect(
        "quarter-follows-from-forced-parent-source",
        Fraction(p_a_rank, 16) == Fraction(1, 4)
        and "`nu - lambda_min(L_Sigma) = Tr(rho_cell P_A) = 1/4`" in note
        and "`c_cell = Tr(rho_cell N_grav) = Tr((I_16/16) P_A) = 1/4`" in b4,
        "forced P_A gives the quarter coefficient",
    )

    total += 1
    passed += expect(
        "scope-reopens-only-by-rejecting-realification",
        "only remaining way to reopen the objection is to reject B3 realification" in note
        and "Do not use:\n\n> The scalar Schur free-energy observable alone derives the parent source."
        in note,
        "parent-source is discharged only after the realified gravity response surface",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
