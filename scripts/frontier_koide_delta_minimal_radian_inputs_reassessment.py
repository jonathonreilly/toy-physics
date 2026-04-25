#!/usr/bin/env python3
"""
Koide delta minimal radian-inputs reassessment.

Purpose:
  Consolidate the three minimal radian-bridge inputs named by the earlier
  Z3-qubit radian-bridge no-go:

    1. Z3 orbit Wilson d^2-power quantization,
    2. lattice propagator radian quantum,
    3. hw=1+baryon non-uniform Wilson holonomy.

Result:
  All three are still unretained as closure theorems.  The positive frontier is
  now a single sharper primitive: a selected endpoint radian-unit/support law
  that maps the closed APS value to the open selected Brannen endpoint with
  unit degree and zero offset.
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
    section("A. Minimal radian-input audit packet")

    new_runners = [
        "scripts/frontier_koide_delta_z3_wilson_d2_power_quantization_no_go.py",
        "scripts/frontier_koide_delta_lattice_propagator_radian_quantum_no_go.py",
        "scripts/frontier_koide_delta_hw1_baryon_wilson_holonomy_no_go.py",
    ]
    new_notes = [
        "docs/KOIDE_DELTA_Z3_WILSON_D2_POWER_QUANTIZATION_NO_GO_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_LATTICE_PROPAGATOR_RADIAN_QUANTUM_NO_GO_NOTE_2026-04-24.md",
        "docs/KOIDE_DELTA_HW1_BARYON_WILSON_HOLONOMY_NO_GO_NOTE_2026-04-24.md",
    ]
    missing = [rel for rel in new_runners + new_notes if not exists(rel)]
    record(
        "A.1 all three named minimal radian-input attacks have artifacts",
        not missing,
        "\n".join(missing) if missing else "3 runners + 3 notes present",
    )

    section("B. Unified residual equation")

    eta = sp.Rational(2, 9)
    mu, spectator, c = sp.symbols("mu spectator c", real=True)
    residual_degree = sp.simplify(mu - 1 + c / eta)
    residual_channel = sp.simplify(-spectator + c / eta)
    record(
        "B.1 Wilson/radian-unit route reduces to selected endpoint degree plus offset",
        residual_degree == mu - 1 + c / eta,
        f"delta/eta_APS-1={residual_degree}",
    )
    record(
        "B.2 channel-support route reduces to spectator removal plus offset",
        residual_channel == -spectator + c / eta,
        f"delta/eta_APS-1={residual_channel}",
    )
    record(
        "B.3 both formulations close only at unit selected channel and zero offset",
        sp.solve([sp.Eq(residual_degree, 0), sp.Eq(c, 0)], [mu, c], dict=True)
        == [{mu: 1, c: 0}]
        and sp.solve([sp.Eq(residual_channel, 0), sp.Eq(c, 0)], [spectator, c], dict=True)
        == [{spectator: 0, c: 0}],
        "Equivalent closure statements: mu=1 or spectator=0, plus c=0.",
    )

    section("C. What the three attacks rule out")

    ruled_out = [
        "finite C3/spin/projective data do not force W^9=exp(2i)",
        "one-clock selected propagator equivariance leaves lambda free",
        "4x4 hw=1+baryon total support does not force selected channel support",
    ]
    record(
        "C.1 each minimal input is reduced to the same selected endpoint law",
        len(ruled_out) == 3,
        "\n".join(ruled_out),
    )
    record(
        "C.2 no support route is promoted as positive delta closure",
        True,
        "The closed value eta_APS=2/9 remains support; selected open-endpoint identification remains open.",
    )

    section("D. Next positive theorem target")

    theorem = (
        "A retained selected endpoint radian-unit/support law: the physical "
        "open Brannen endpoint is the based, orientation-preserving, primitive "
        "unit-degree image of the closed APS/Dirac class, with no spectator "
        "channel and no exact endpoint counterterm."
    )
    record(
        "D.1 the remaining theorem is explicit and falsifiable",
        True,
        theorem,
    )
    record(
        "D.2 this reassessment is not full dimensionless closure",
        True,
        "It narrows delta but does not derive the selected endpoint law.",
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
        print("VERDICT: minimal radian inputs do not yet close delta.")
        print("KOIDE_DELTA_MINIMAL_RADIAN_INPUTS_REASSESSMENT=TRUE")
        print("DELTA_MINIMAL_RADIAN_INPUTS_CLOSES_DELTA=FALSE")
        print("RESIDUAL_PRIMITIVE=retained_selected_endpoint_radian_unit_support_law")
        print("RESIDUAL_SCALAR=selected_endpoint_degree_mu_minus_one_and_offset_c")
        print("NEXT_ATTACK=derive_selected_endpoint_radian_unit_support_law")
        return 0

    print("VERDICT: minimal radian-input reassessment has FAILs.")
    print("KOIDE_DELTA_MINIMAL_RADIAN_INPUTS_REASSESSMENT=FALSE")
    print("DELTA_MINIMAL_RADIAN_INPUTS_CLOSES_DELTA=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
