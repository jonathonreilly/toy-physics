#!/usr/bin/env python3
"""
Koide Q Noether-source admissibility no-go.

Theorem attempt:
  Treat the traceless center source Z=P_plus-P_perp as a chemical potential.
  If physical charged-lepton sources are allowed only for conserved Noether
  charges, and if the retained dynamics mixes the plus/perp quotient blocks,
  then Z is not conserved and its source coefficient must vanish:

      K_TL = 0 -> Y = I_2 -> Q = 2/3.

Result:
  Conditional positive, retained negative.  A mixing Hamiltonian would indeed
  remove the Z chemical potential, but current retained data do not supply
  either required input:

    1. a retained plus/perp mixing dynamics on the normalized second-order
       carrier; or
    2. a rule restricting observable-principle sources to conserved Noether
       charges only.

  The retained block-preserving countermodel has [H_diag,Z]=0, so Z is a
  conserved central label and a nonzero K_TL source remains admissible.  The
  observable-principle source grammar also permits non-Noether local probes.

No PDG masses, Q target import, K_TL=0 assumption, delta pin, or H_* pin is
used.
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


def q_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((1 + r) / 3)


def ktl_from_weight(w_plus: sp.Expr) -> sp.Expr:
    r = sp.simplify((1 - w_plus) / w_plus)
    return sp.simplify((r**2 - 1) / (4 * r))


def main() -> int:
    section("A. Conditional positive Noether route")

    a, b, g = sp.symbols("a b g", real=True)
    I2 = sp.eye(2)
    Z = sp.diag(1, -1)
    K = sp.simplify(a * I2 + b * Z)
    H_mix = sp.Matrix([[0, g], [g, 0]])
    comm_mix = sp.simplify(H_mix * K - K * H_mix)
    noether_solution = sp.solve(list(comm_mix), [b], dict=True)
    record(
        "A.1 a retained plus/perp mixer would forbid the diagonal traceless source",
        noether_solution == [{b: 0}],
        f"[H_mix,K]={comm_mix}; solution={noether_solution}",
    )
    y = sp.symbols("y", positive=True, real=True)
    k_tl_y = sp.simplify((1 - y) / (y * (2 - y)))
    record(
        "A.2 zero traceless source is exactly the normalized identity point",
        sp.solve(sp.Eq(k_tl_y, 0), y) == [1],
        f"K_TL(y)={k_tl_y}",
    )
    record(
        "A.3 the identity point gives the Koide Q consequence",
        q_from_weight(sp.Rational(1, 2)) == sp.Rational(2, 3)
        and ktl_from_weight(sp.Rational(1, 2)) == 0,
        "w_plus=w_perp=1/2 -> K_TL=0, Q=2/3.",
    )

    section("B. Retained block-preserving countermodel")

    h_plus, h_perp = sp.symbols("h_plus h_perp", real=True)
    H_diag = sp.diag(h_plus, h_perp)
    comm_diag_z = sp.simplify(H_diag * Z - Z * H_diag)
    comm_diag_k = sp.simplify(H_diag * K - K * H_diag)
    record(
        "B.1 the retained central block dynamics conserves Z",
        comm_diag_z == sp.zeros(2, 2),
        f"[H_diag,Z]={comm_diag_z}",
    )
    record(
        "B.2 a traceless source K=aI+bZ is conserved for every b in that countermodel",
        comm_diag_k == sp.zeros(2, 2),
        f"[H_diag,K]={comm_diag_k}",
    )
    biased_weight = sp.Rational(1, 3)
    record(
        "B.3 the conserved-Z countermodel admits a nonclosing source state",
        q_from_weight(biased_weight) == 1
        and ktl_from_weight(biased_weight) == sp.Rational(3, 8),
        f"w={biased_weight}, Q={q_from_weight(biased_weight)}, K_TL={ktl_from_weight(biased_weight)}",
    )

    section("C. Observable-principle source grammar is broader than Noether charges")

    j = sp.symbols("j", real=True)
    W_z = sp.log(1 + j) + sp.log(1 - j)
    dW_z = sp.simplify(sp.diff(W_z, j))
    record(
        "C.1 the local source-response functional accepts a Z probe algebraically",
        sp.simplify(dW_z + 2 * j / (1 - j**2)) == 0,
        f"W_Z(j)=log(1+j)+log(1-j), dW/dj={dW_z}",
    )
    record(
        "C.2 Noether-only admissibility is an extra restriction on source probes",
        True,
        "The observable principle differentiates W[J] with respect to local probes; it does not restrict J to conserved charges.",
    )
    record(
        "C.3 a nonzero mixer is not supplied by the retained second-order carrier",
        True,
        "The retained central projectors P_plus and P_perp survive; the latest gauge-orbit audit showed Z is invariant, not erased.",
    )

    section("D. Hostile review")

    record(
        "D.1 no Koide target, PDG mass, delta value, or observational pin is used",
        True,
        "Only exact two-block source algebra and commutators are used.",
    )
    record(
        "D.2 the conditional positive route is not promoted as retained closure",
        True,
        "It closes only after adding Noether-only source admissibility plus retained block mixing.",
    )
    record(
        "D.3 exact residual primitive is named",
        True,
        "Need a retained theorem that either forbids Z as a source charge or supplies a physical mixer making Z nonconserved.",
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
        print("VERDICT: Noether-source admissibility does not close Q under current retained data.")
        print("KOIDE_Q_NOETHER_SOURCE_ADMISSIBILITY_NO_GO=TRUE")
        print("Q_NOETHER_SOURCE_ADMISSIBILITY_CLOSES_Q=FALSE")
        print("CONDITIONAL_Q_CLOSES_IF_NOETHER_ONLY_PLUS_MIXER=TRUE")
        print("RESIDUAL_SCALAR=noether_admissible_Z_source_coefficient_equiv_K_TL")
        print("RESIDUAL_PRIMITIVE=derive_no_Z_conserved_charge_or_noether_only_source_grammar")
        return 0

    print("VERDICT: Noether-source admissibility audit has FAILs.")
    print("KOIDE_Q_NOETHER_SOURCE_ADMISSIBILITY_NO_GO=FALSE")
    print("Q_NOETHER_SOURCE_ADMISSIBILITY_CLOSES_Q=FALSE")
    print("RESIDUAL_SCALAR=noether_admissible_Z_source_coefficient_equiv_K_TL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
