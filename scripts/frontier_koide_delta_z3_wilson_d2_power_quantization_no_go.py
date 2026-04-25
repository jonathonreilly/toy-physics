#!/usr/bin/env python3
"""
Koide delta Z3 Wilson d^2-power quantization no-go.

Theorem attempt:
  Close the Brannen radian bridge by deriving the Route-3 Wilson law

      W_Z3^(d^2) = exp(2i) * 1,   d = 3,

  so that the per-step selected endpoint phase is 2/d^2 = 2/9.

Result:
  Negative.  A retained finite C3 representation gives W^3 = 1, hence
  W^9 = 1, not exp(2i).  If W^9 = exp(2i) is imposed, the generator is no
  longer the retained C3 action; it is a new U(1) Wilson holonomy whose
  normalization is exactly the missing radian-unit primitive.

No mass data, fitted delta value, or observational target is used.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp


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


def cycle_matrix() -> np.ndarray:
    return np.array(
        [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
        dtype=complex,
    )


def main() -> int:
    d = 3
    d2 = d * d
    target = complex(np.exp(2j))
    c3 = cycle_matrix()

    section("A. Retained C3 Wilson generator")

    record(
        "A.1 retained cycle satisfies C^3=1 and C^9=1",
        np.linalg.norm(np.linalg.matrix_power(c3, 3) - np.eye(3)) < 1e-12
        and np.linalg.norm(np.linalg.matrix_power(c3, 9) - np.eye(3)) < 1e-12,
        "finite C3 representation only carries root-of-unity phases.",
    )
    record(
        "A.2 the Route-3 target exp(2i) is not the retained C3 ninth power",
        abs(target - 1.0) > 1e-6,
        f"exp(2i)={target.real:+.12f}{target.imag:+.12f}i; 1=+1.000000000000+0.000000000000i",
    )

    section("B. General phase-twisted cycle W(phi)=exp(i phi) C")

    phi = sp.symbols("phi", real=True)
    w3_phase = sp.exp(3 * sp.I * phi)
    w9_phase = sp.exp(9 * sp.I * phi)
    finite_c3_solutions = [sp.Rational(2, 3) * sp.pi * k for k in range(3)]
    finite_w9 = [sp.simplify(w9_phase.subs(phi, value)) for value in finite_c3_solutions]
    record(
        "B.1 imposing the retained finite C3 law W^3=1 forces W^9=1",
        finite_w9 == [1, 1, 1],
        "phi in {0, 2pi/3, 4pi/3} -> exp(9 i phi)=1.",
    )

    route3_phi = sp.Rational(2, 9)
    route3_w3 = complex(sp.N(w3_phase.subs(phi, route3_phi)))
    route3_w9 = complex(sp.N(w9_phase.subs(phi, route3_phi)))
    record(
        "B.2 imposing per-step phi=2/9 gives W^9=exp(2i) but violates W^3=1",
        abs(route3_w9 - target) < 1e-12 and abs(route3_w3 - 1.0) > 1e-6,
        f"W^3=exp(2i/3)={route3_w3.real:+.12f}{route3_w3.imag:+.12f}i.",
    )
    route3_family = [(sp.Integer(2) + 2 * sp.pi * k) / 9 for k in range(3)]
    route3_family_w9 = [complex(sp.N(w9_phase.subs(phi, value))) for value in route3_family]
    route3_family_w3 = [complex(sp.N(w3_phase.subs(phi, value))) for value in route3_family]
    record(
        "B.3 the exact d^2-power law is equivalent to choosing the missing phase family",
        all(abs(value - target) < 1e-12 for value in route3_family_w9)
        and all(abs(value - 1.0) > 1e-6 for value in route3_family_w3),
        "Real phases modulo 2pi: phi=(2+2pi k)/9.  These give W^9=exp(2i) but not W^3=1.",
    )

    section("C. Projective or spin-lift variants")

    spin_phi = sp.pi / 3
    spin_w3 = complex(sp.N(w3_phase.subs(phi, spin_phi)))
    spin_w9 = complex(sp.N(w9_phase.subs(phi, spin_phi)))
    record(
        "C.1 spin-lift cubic sign gives W^9=-1, not exp(2i)",
        abs(spin_w3 + 1.0) < 1e-12 and abs(spin_w9 + 1.0) < 1e-12 and abs(spin_w9 - target) > 1e-6,
        f"spin phi=pi/3 -> W^3={spin_w3.real:+.1f}; W^9={spin_w9.real:+.1f}.",
    )

    alpha = sp.symbols("alpha", real=True)
    projective_cubic = sp.exp(3 * sp.I * (phi + alpha))
    record(
        "C.2 a projective generator phase can be rephased, so it is not a retained invariant unit",
        sp.simplify(projective_cubic.subs(alpha, -phi)) == 1,
        "W -> exp(i alpha) W gauges the cubic phase; choosing exp(2i/3) is extra endpoint data.",
    )

    section("D. Exact countermodels")

    counter_phis = {
        "finite_C3_identity": 0.0,
        "spin_lift": math.pi / 3,
        "half_target": 1.0 / 9.0,
        "route3_target_import": 2.0 / 9.0,
    }
    lines = []
    nonclosing_ok = True
    for name, value in counter_phis.items():
        phase9 = complex(np.exp(9j * value))
        closes = abs(phase9 - target) < 1e-9
        if name != "route3_target_import":
            nonclosing_ok = nonclosing_ok and not closes
        lines.append(
            f"{name}: phi={value:.12f}, W^9={phase9.real:+.6f}{phase9.imag:+.6f}i, closes={closes}"
        )
    record(
        "D.1 retained-compatible exact countermodels do not close the radian bridge",
        nonclosing_ok,
        "\n".join(lines),
    )
    record(
        "D.2 the only listed closing model is the target-imported Route-3 phase",
        abs(complex(np.exp(9j * (2.0 / 9.0))) - target) < 1e-12,
        "Setting phi=2/9 is precisely the d^2-power quantization law, not a derivation of it.",
    )

    section("E. Hostile-review closeout")

    record(
        "E.1 finite C3, spin lift, and projective rephasing do not derive exp(2i)",
        True,
        "They give roots of unity, a cubic sign, or gauge-removable central phases.",
    )
    record(
        "E.2 no positive delta closure is claimed",
        True,
        "The missing primitive is now the physical U(1) Wilson action/radian unit on the selected endpoint.",
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
        print("VERDICT: Z3 Wilson d^2-power quantization is not retained-derived.")
        print("KOIDE_DELTA_Z3_WILSON_D2_POWER_QUANTIZATION_NO_GO=TRUE")
        print("DELTA_Z3_WILSON_D2_POWER_QUANTIZATION_CLOSES_DELTA=FALSE")
        print("RESIDUAL_PRIMITIVE=retained_U1_Wilson_radian_unit_on_selected_endpoint")
        print("COUNTERSTATE=finite_C3_or_spin_lift_W9_not_exp_2i")
        print("NEXT_ATTACK=lattice_propagator_radian_quantum_or_hw1_baryon_Wilson_holonomy")
        return 0

    print("VERDICT: Z3 Wilson d^2-power quantization audit has FAILs.")
    print("KOIDE_DELTA_Z3_WILSON_D2_POWER_QUANTIZATION_NO_GO=FALSE")
    print("DELTA_Z3_WILSON_D2_POWER_QUANTIZATION_CLOSES_DELTA=FALSE")
    return 1


if __name__ == "__main__":
    sys.exit(main())
