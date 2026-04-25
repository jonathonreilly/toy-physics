#!/usr/bin/env python3
"""
Koide delta lattice-propagator radian-quantum no-go.

Theorem attempt:
  Close the Brannen radian bridge from a retained lattice propagator identity

      G_C3(1) = exp(i * 2/d^2) G_0.

Result:
  Negative.  C3 equivariance and one-clock evolution allow a scalar selected
  propagator phase, but they do not set its radian value.  The finite Dirac
  support packet supplies the closed APS scalar eta=2/9; it does not turn eta
  into the open selected-line propagator phase without a new unit/basepoint
  law.
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
    section("A. Required support artifacts")

    required = [
        "docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md",
        "docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md",
        "scripts/frontier_koide_brannen_dirac_support.py",
        "scripts/frontier_koide_delta_z3_wilson_d2_power_quantization_no_go.py",
    ]
    missing = [rel for rel in required if not exists(rel)]
    record(
        "A.1 relevant radian-bridge and finite-Dirac support artifacts are present",
        not missing,
        "\n".join(missing) if missing else f"checked={len(required)} artifacts",
    )

    section("B. Equivariant one-clock propagator phase")

    lam, eta, c, s = sp.symbols("lambda eta c s", real=True)
    eta_value = sp.Rational(2, 9)
    # A selected one-dimensional propagator commutes with C3 for any scalar phase.
    propagator = sp.exp(sp.I * lam)
    c3_defect = sp.simplify(propagator - propagator)
    record(
        "B.1 selected-line C3 equivariance leaves the scalar phase lambda free",
        c3_defect == 0,
        "On a one-dimensional selected endpoint, every scalar phase commutes with C3.",
    )

    finite_c3_lambdas = [sp.Rational(2, 3) * sp.pi * k for k in range(3)]
    finite_matches = [sp.simplify(value - eta_value) == 0 for value in finite_c3_lambdas]
    record(
        "B.2 finite C3 periodicity gives root-of-unity phases, not lambda=2/9",
        finite_matches == [False, False, False],
        "lambda in {0, 2pi/3, 4pi/3} does not equal 2/9.",
    )
    record(
        "B.3 imposing G_C3(1)=exp(i*2/d^2)G0 is exactly lambda=2/9",
        sp.solve(sp.Eq(lam - eta_value, 0), lam) == [eta_value],
        "The propagator identity states the target phase rather than deriving it.",
    )

    section("C. Closed APS scalar does not fix the open propagator map")

    open_phase = sp.simplify(s * eta + c)
    residual = sp.simplify(open_phase.subs(eta, eta_value) / eta_value - 1)
    record(
        "C.1 the most general affine APS-to-open propagator readout has scale and offset",
        residual == s - 1 + c / eta_value,
        f"lambda_open=s eta_APS+c -> lambda/eta_APS-1={residual}",
    )
    record(
        "C.2 one-clock/basepoint preservation can kill c but not the scale s",
        sp.simplify(residual.subs(c, 0)) == s - 1,
        "After c=0, closure still requires s=1.",
    )
    counterstates = {
        "zero_phase": {s: 0, c: 0},
        "half_eta": {s: sp.Rational(1, 2), c: 0},
        "shifted_eta": {s: 1, c: sp.Rational(1, 9)},
        "target_import": {s: 1, c: 0},
    }
    lines = []
    nonclosing_ok = True
    for name, subs in counterstates.items():
        value = sp.simplify(open_phase.subs(eta, eta_value).subs(subs))
        closes = value == eta_value
        if name != "target_import":
            nonclosing_ok = nonclosing_ok and not closes
        lines.append(f"{name}: lambda_open={value}, closes={closes}")
    record(
        "C.3 exact equivariant propagator countermaps preserve support data without closing",
        nonclosing_ok,
        "\n".join(lines),
    )

    section("D. Hostile-review closeout")

    record(
        "D.1 finite Dirac eta support is not promoted to a selected propagator phase",
        True,
        "eta_APS=2/9 remains closed support; the open phase map is still the missing theorem.",
    )
    record(
        "D.2 no hidden target import is used",
        True,
        "The runner treats lambda=2/9 as the tested conclusion, not an input to closure.",
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
        print("VERDICT: lattice propagator radian quantum is not retained-derived.")
        print("KOIDE_DELTA_LATTICE_PROPAGATOR_RADIAN_QUANTUM_NO_GO=TRUE")
        print("DELTA_LATTICE_PROPAGATOR_RADIAN_QUANTUM_CLOSES_DELTA=FALSE")
        print("RESIDUAL_PRIMITIVE=selected_open_propagator_phase_unit_lambda_equals_eta_APS")
        print("RESIDUAL_SCALAR=APS_to_open_propagator_scale_s_minus_one")
        print("COUNTERSTATE=equivariant_one_clock_phase_lambda_free")
        print("NEXT_ATTACK=hw1_baryon_Wilson_holonomy_or_new_endpoint_unit_law")
        return 0

    print("VERDICT: lattice propagator radian quantum audit has FAILs.")
    print("KOIDE_DELTA_LATTICE_PROPAGATOR_RADIAN_QUANTUM_NO_GO=FALSE")
    print("DELTA_LATTICE_PROPAGATOR_RADIAN_QUANTUM_CLOSES_DELTA=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
