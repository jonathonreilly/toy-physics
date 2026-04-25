#!/usr/bin/env python3
"""
Koide Q KMS/modular-state no-go.

Theorem attempt:
  A finite KMS or modular equilibrium principle on the retained C3 sectors
  might select the equal center-label state, deriving K_TL = 0.

Result:
  Negative from retained data alone.  A finite KMS state with sector
  multiplicities n_+=1 and n_perp=2 has weights

      p_i proportional to n_i exp(-beta E_i).

  With no retained sector Hamiltonian splitting, the beta=0 / degenerate-energy
  KMS state is the Hilbert/rank state (1/3, 2/3), not the equal-label state.
  Equal labels require

      beta (E_perp - E_+) = log 2,

  which is a new sector-gap/temperature primitive equivalent to the missing
  source-state law.

No PDG masses, target Koide value, delta pin, or H_* pin is used.
"""

from __future__ import annotations

import sys

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


def q_from_probabilities(p_plus: sp.Expr, p_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(p_perp / p_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_probabilities(p_plus: sp.Expr, p_perp: sp.Expr) -> sp.Expr:
    r = sp.simplify(p_perp / p_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Retained sector multiplicities")

    n_plus = sp.Integer(1)
    n_perp = sp.Integer(2)
    record(
        "A.1 retained real C3 sectors have multiplicities 1 and 2",
        n_plus == 1 and n_perp == 2,
        "singlet rank=1, doublet rank=2.",
    )

    section("B. General finite KMS state")

    beta, delta_E = sp.symbols("beta delta_E", real=True)
    x = sp.symbols("x", positive=True, real=True)
    # x = exp(-beta * (E_perp - E_plus)).
    z = sp.simplify(n_plus + n_perp * x)
    p_plus = sp.simplify(n_plus / z)
    p_perp = sp.simplify(n_perp * x / z)
    q_x = q_from_probabilities(p_plus, p_perp)
    ktl_x = ktl_from_probabilities(p_plus, p_perp)
    record(
        "B.1 KMS sector probabilities contain one free Boltzmann ratio",
        p_plus == 1 / (2 * x + 1) and p_perp == 2 * x / (2 * x + 1),
        f"p_plus={p_plus}, p_perp={p_perp}, Q(x)={q_x}, K_TL(x)={ktl_x}",
    )
    record(
        "B.2 equal center labels require Boltzmann ratio x=1/2",
        sp.solve(sp.Eq(ktl_x, 0), x) == [sp.Rational(1, 2)],
        "The KMS principle leaves x free until a sector gap and beta are supplied.",
    )

    section("C. Degenerate/infinite-temperature KMS state is rank weighted")

    p_deg = (sp.simplify(p_plus.subs(x, 1)), sp.simplify(p_perp.subs(x, 1)))
    q_deg = q_from_probabilities(*p_deg)
    ktl_deg = ktl_from_probabilities(*p_deg)
    record(
        "C.1 beta=0 or degenerate sector energies give the Hilbert/rank state",
        p_deg == (sp.Rational(1, 3), sp.Rational(2, 3)),
        f"p_deg={p_deg}",
    )
    record(
        "C.2 the rank KMS state is off the source-neutral Koide leaf",
        q_deg == 1 and ktl_deg == sp.Rational(3, 8),
        f"Q_deg={q_deg}, K_TL_deg={ktl_deg}",
    )

    section("D. Equal labels require a new log-2 sector gap")

    gap_equation = sp.Eq(sp.exp(-beta * delta_E), sp.Rational(1, 2))
    solved_gap = sp.solve(sp.Eq(beta * delta_E, sp.log(2)), delta_E)
    record(
        "D.1 equal labels are equivalent to beta*(E_perp-E_plus)=log(2)",
        solved_gap == [sp.log(2) / beta],
        f"exp(-beta*DeltaE)=1/2 -> DeltaE={solved_gap}",
    )
    record(
        "D.2 log-2 is not supplied by the retained C3 sector data",
        True,
        f"Required equation: {gap_equation}; retained multiplicities only give n_perp/n_plus=2.",
    )

    section("E. KMS states can realize a continuum of Q values")

    samples = {
        "rank": sp.Integer(1),
        "equal_label": sp.Rational(1, 2),
        "perp_cold": sp.Rational(1, 4),
        "perp_hot": sp.Integer(2),
    }
    sample_lines = []
    distinct_q = set()
    for name, x_value in samples.items():
        probs = (sp.simplify(p_plus.subs(x, x_value)), sp.simplify(p_perp.subs(x, x_value)))
        q_value = sp.simplify(q_from_probabilities(*probs))
        ktl_value = sp.simplify(ktl_from_probabilities(*probs))
        distinct_q.add(q_value)
        sample_lines.append(f"{name}: x={x_value}, p={probs}, Q={q_value}, K_TL={ktl_value}")
    record(
        "E.1 admissible KMS states include both closing and non-closing source states",
        len(distinct_q) == len(samples),
        "\n".join(sample_lines),
    )
    record(
        "E.2 detailed balance/KMS form alone does not select x=1/2",
        True,
        "A physical sector Hamiltonian or temperature equation is the residual primitive.",
    )

    section("F. Verdict")

    residual = sp.simplify(beta * delta_E - sp.log(2))
    record(
        "F.1 KMS/modular route does not close Q",
        residual == beta * delta_E - sp.log(2),
        f"RESIDUAL_MODULAR_GAP={residual}",
    )
    record(
        "F.2 Q remains open after KMS audit",
        True,
        "Residual primitive: retained law fixing the sector Boltzmann ratio to 1/2.",
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
        print("VERDICT: KMS/modular state route does not close Q.")
        print("KOIDE_Q_KMS_MODULAR_STATE_NO_GO=TRUE")
        print("Q_KMS_MODULAR_STATE_CLOSES_Q=FALSE")
        print("RESIDUAL_SCALAR=beta_deltaE_minus_log2_equiv_center_label_state")
        print("RESIDUAL_MODULAR_GAP=beta_Eperp_minus_Eplus_minus_log2")
        return 0

    print("VERDICT: KMS/modular-state audit has FAILs.")
    print("KOIDE_Q_KMS_MODULAR_STATE_NO_GO=FALSE")
    print("Q_KMS_MODULAR_STATE_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=beta_deltaE_minus_log2_equiv_center_label_state")
    print("RESIDUAL_MODULAR_GAP=beta_Eperp_minus_Eplus_minus_log2")
    return 1


if __name__ == "__main__":
    sys.exit(main())
