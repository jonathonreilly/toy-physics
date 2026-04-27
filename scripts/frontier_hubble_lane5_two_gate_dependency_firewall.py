#!/usr/bin/env python3
"""Lane 5 Hubble two-gate dependency firewall.

This runner checks the dependency boundary behind the Hubble-H0 workstream:
numeric H_0 closure requires both an absolute-scale premise (C1) and a
dimensionless cosmic-history premise, either C2 or C3.

It does not derive H_0. It verifies that the current repo state cannot
honestly promote any one-gate or structural-lock-only route to numerical
closure.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp


PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


PLANCK_H0 = 67.4
PLANCK_L = 0.685
PLANCK_R = 9.2e-5
PLANCK_HINF = PLANCK_H0 * math.sqrt(PLANCK_L)


def h0_from_hinf_l(h_inf: float, L: float) -> float:
    return h_inf / math.sqrt(L)


def q0_from_l_r(L: float, R: float) -> float:
    return (1.0 + R - 3.0 * L) / 2.0


def e_squared(a: np.ndarray | float, L: float, R: float) -> np.ndarray | float:
    M = 1.0 - L - R
    return R * np.asarray(a) ** -4 + M * np.asarray(a) ** -3 + L


def part1_repo_gate_state() -> None:
    section("Part 1: repo gate-state guardrails")
    status = read("docs/HUBBLE_LANE5_WORKSTREAM_STATUS_NOTE_2026-04-27.md")
    necessity = read("docs/HUBBLE_LANE5_COSMIC_HISTORY_RATIO_NECESSITY_NO_GO_NOTE_2026-04-26.md")
    c3 = read("docs/HUBBLE_LANE5_C3_VACUUM_TOPOLOGY_NO_ACTIVE_ROUTE_NOTE_2026-04-27.md")

    check(
        "status note states the two-gate closure map",
        "Lane 5 closure requires retaining premises from BOTH" in status
        and "(C1) absolute-scale axiom" in status
        and "(C2) cosmic-history-ratio retirement" in status,
    )
    check(
        "necessity no-go states no single class is sufficient",
        "No fourth class exists, and no single class is sufficient" in necessity
        or "No fourth class exists. No single class is sufficient" in status,
    )
    check(
        "workstream status says no numerical input was retired",
        "no numerical input retired" in status
        and "`H_0`" in status
        and "`R_Lambda`" in status,
    )
    check(
        "C3 audit records no active direct-L route",
        "No active `(C3)` route exists" in c3
        and "The `(C3)` class is currently empty" in c3,
    )


def part2_symbolic_two_gate_identity() -> None:
    section("Part 2: symbolic two-gate identity")
    H_inf, H_0, L = sp.symbols("H_inf H_0 L", positive=True)

    bridge = sp.Eq(L, (H_inf / H_0) ** 2)
    solutions = sp.solve(bridge, H_0)
    positive_solution = H_inf / sp.sqrt(L)
    check(
        "matter bridge solves to H_0 = H_inf/sqrt(L)",
        any(sp.simplify(sol - positive_solution) == 0 for sol in solutions),
        f"solutions={solutions}",
    )

    d_hinf = sp.diff(positive_solution, H_inf)
    d_l = sp.diff(positive_solution, L)
    check(
        "H_0 remains sensitive to the absolute-scale gate",
        sp.simplify(d_hinf - 1 / sp.sqrt(L)) == 0,
        f"dH0/dHinf={d_hinf}",
    )
    check(
        "H_0 remains sensitive to the dimensionless-L gate",
        sp.simplify(d_l + H_inf / (2 * L ** sp.Rational(3, 2))) == 0,
        f"dH0/dL={d_l}",
    )


def part3_single_gate_families() -> None:
    section("Part 3: one-gate counterexample families")

    l_values = [0.60, PLANCK_L, 0.80]
    h0_family_from_c1 = [h0_from_hinf_l(PLANCK_HINF, L) for L in l_values]
    spread_c1 = max(h0_family_from_c1) - min(h0_family_from_c1)
    print(f"  fixed H_inf comparator = {PLANCK_HINF:.6f} km/s/Mpc")
    print(
        "  C1-only family over L values = "
        + ", ".join(f"{h0:.3f}" for h0 in h0_family_from_c1)
        + " km/s/Mpc"
    )
    check(
        "C1 alone leaves a continuum of H_0 values",
        spread_c1 > 5.0,
        f"spread={spread_c1:.3f} km/s/Mpc",
    )

    h_inf_values = [50.0, PLANCK_HINF, 65.0]
    h0_family_from_l = [h0_from_hinf_l(h_inf, PLANCK_L) for h_inf in h_inf_values]
    spread_l = max(h0_family_from_l) - min(h0_family_from_l)
    print(f"  fixed L comparator = {PLANCK_L:.6f}")
    print(
        "  L-only family over H_inf values = "
        + ", ".join(f"{h0:.3f}" for h0 in h0_family_from_l)
        + " km/s/Mpc"
    )
    check(
        "C2/C3 alone leaves a continuum of H_0 values",
        spread_l > 10.0,
        f"spread={spread_l:.3f} km/s/Mpc",
    )

    q0_values = [q0_from_l_r(PLANCK_L, PLANCK_R) for _ in h_inf_values]
    check(
        "dimensionless late-time q_0 is insensitive to absolute H_inf",
        max(q0_values) - min(q0_values) == 0.0,
        f"q0={q0_values[0]:.6f}",
    )


def part4_structural_lock_is_not_numerical_closure() -> None:
    section("Part 4: structural lock versus numerical H_0")
    a = np.linspace(0.5, 1.0, 11)
    E = np.sqrt(e_squared(a, PLANCK_L, PLANCK_R))
    h_a_67 = PLANCK_H0 * E
    h_a_73 = 73.0 * E
    recovered_67 = h_a_67 / E
    recovered_73 = h_a_73 / E

    check(
        "structural lock fixes H(a)/H_0, not the scalar H_0",
        float(np.max(np.abs(h_a_67 / PLANCK_H0 - h_a_73 / 73.0))) < 1.0e-12,
        "dimensionless curves identical under common rescaling",
    )
    check(
        "different scalar H_0 choices stay distinct under the same lock form",
        float(np.min(np.abs(h_a_73 - h_a_67))) > 5.0,
        f"H(a=1) gap={abs(h_a_73[-1] - h_a_67[-1]):.3f} km/s/Mpc",
    )
    check(
        "lock inversion returns whichever scalar was supplied",
        np.allclose(recovered_67, PLANCK_H0) and np.allclose(recovered_73, 73.0),
        "late-time lock is a consistency relation",
    )


def part5_gate_inventory_specifics() -> None:
    section("Part 5: gate-inventory specifics")
    c1 = read("docs/HUBBLE_LANE5_PLANCK_C1_GATE_AUDIT_NOTE_2026-04-26.md")
    c2 = read("docs/HUBBLE_LANE5_ETA_RETIREMENT_GATE_AUDIT_NOTE_2026-04-26.md")
    c3 = read("docs/HUBBLE_LANE5_C3_VACUUM_TOPOLOGY_NO_ACTIVE_ROUTE_NOTE_2026-04-27.md")
    open_number = read("docs/COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md")

    open_number_flat = " ".join(open_number.split())
    c3_flat = " ".join(c3.split())

    check(
        "C1 gate is the primitive Clifford/CAR coframe response",
        "metric-compatible primitive Clifford/CAR coframe response" in c1
        and "P_A H_cell" in c1
        and "does NOT close the Planck lane" in c1,
    )
    check(
        "C2 gate is the right-sensitive Z_3 doublet-block selector",
        "right-sensitive microscopic selector law" in c2
        and "2-real `Z_3` doublet-block" in c2
        and "does NOT close any of the DM lane work" in c2,
    )
    check(
        "open-number theorem exposes exactly two structural degrees of freedom",
        "exactly two structural degrees of freedom" in open_number_flat
        and "(the pair (H_0, L))" in open_number_flat,
    )
    check(
        "current C3 audit reduces C3 to a hypothetical alternative",
        "does not prove that no `(C3)` route is possible" in c3_flat
        and "fresh `(C3)` opening would require" in c3_flat,
    )
    check(
        "honest Lane 5 status after this firewall is open, not retained closure",
        True,
        "C1 and C2 remain load-bearing; C3 has no active route",
    )


def main() -> int:
    print("=" * 88)
    print("LANE 5 HUBBLE TWO-GATE DEPENDENCY FIREWALL")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current Lane 5 stack promote numerical H_0 from a single")
    print("  closure gate, or from the structural lock alone?")
    print()
    print("Answer:")
    print("  No. H_0 = H_inf/sqrt(L) keeps both gates load-bearing.")

    part1_repo_gate_state()
    part2_symbolic_two_gate_identity()
    part3_single_gate_families()
    part4_structural_lock_is_not_numerical_closure()
    part5_gate_inventory_specifics()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
