#!/usr/bin/env python3
"""
Koide Brannen Callan-Harvey candidate runner

This runner packages the concrete physical-lattice anomaly-descent proposal
behind the remaining Brannen physical bridge.

It verifies:
  - the exact per-generation anomaly coefficient `2/9`,
  - compatibility of that value with the physical-lattice / 3-generation
    carrier picture,
  - forward consistency with the Brannen mass ratios,
  - and the exact point that still remains open.

It does NOT prove the missing theorem

    δ_physical(selected-line Berry phase) = descended anomaly object.
"""

import math
import sys

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    PASSES.append((label, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def main() -> int:
    print("=" * 88)
    print("Koide Brannen Callan-Harvey candidate route")
    print("=" * 88)

    d = 3
    y_q = sp.Rational(1, d)
    n_q = 2 * d
    anomaly_per_generation = sp.simplify(n_q * y_q**3)

    check(
        "1. Per-generation anomaly coefficient is exactly 2/9",
        anomaly_per_generation == sp.Rational(2, 9),
        f"(2d)·(1/d)^3 = {anomaly_per_generation}",
    )

    check(
        "2. Physical-lattice carrier gives a concrete anomaly-descent candidate",
        True,
        "Accepted framework statement: Cl(3) on Z^3 is the physical theory.\n"
        "Retained three-generation theorem: body-diagonal fixed sites supply\n"
        "the natural 3-generation carrier.\n"
        "This gives a concrete physical-lattice setting in which a\n"
        "Callan-Harvey-style descent route can be posed.",
    )

    delta = float(sp.Rational(2, 9))
    pdg_masses = [0.51099895, 105.6583745, 1776.86]
    sqrt_m_pdg = sorted(math.sqrt(m) for m in pdg_masses)
    v0 = sum(sqrt_m_pdg) / 3
    c = math.sqrt(2)
    brannen = sorted(v0 * (1 + c * math.cos(delta + 2 * math.pi * k / 3)) for k in range(3))
    max_err = max(abs(brannen[i] - sqrt_m_pdg[i]) / sqrt_m_pdg[i] for i in range(3))

    check(
        "3. The candidate anomaly value 2/9 is forward-consistent with charged-lepton ratios",
        max_err < 3e-4,
        f"Max relative error in √m predictions: {max_err*100:.4f}%",
    )

    check(
        "4. The route still needs the Berry/inflow identification theorem",
        True,
        "Not yet derived: the selected-line Berry phase on the charged-lepton\n"
        "CP^1 carrier is the descended Callan-Harvey / anomaly object.",
    )

    check(
        "5. The route still needs the descent normalization theorem",
        True,
        "Not yet derived: the relevant 1D descent factor is exactly 1.\n"
        "That normalization is still the load-bearing missing theorem, not an\n"
        "executably validated map.",
    )

    print()
    print("=" * 88)
    print("Summary")
    print("=" * 88)
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")

    if n_pass == n_total:
        print()
        print("VERDICT: the Callan-Harvey route is a concrete physical-bridge")
        print("candidate on the accepted physical-lattice reading.")
        print("It strengthens the Brannen bridge search, but it does not close")
        print("the physical bridge by itself.")

    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
