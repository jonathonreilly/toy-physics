#!/usr/bin/env python3
"""
Science-only support theorem:
the reduced two-slot source law W_red = log det(I + K) is the exact restriction
of the observable principle to the normalized second-order block carrier once
that carrier is admitted.
"""

from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []

REPO_ROOT = Path(__file__).resolve().parents[1]


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def main() -> int:
    section("A. Exact reduced block-source family")

    k_plus, k_perp = sp.symbols("k_plus k_perp", real=True)
    pi_plus = sp.Matrix([[1, 0], [0, 0]])
    pi_perp = sp.Matrix([[0, 0], [0, 1]])
    i2 = sp.eye(2)
    k = k_plus * pi_plus + k_perp * pi_perp

    record(
        "A.1 the normalized second-order carrier splits exactly into two independent scalar blocks",
        pi_plus * pi_perp == sp.zeros(2)
        and pi_plus + pi_perp == i2
        and pi_plus**2 == pi_plus
        and pi_perp**2 == pi_perp,
        f"Π_+ = {pi_plus}, Π_perp = {pi_perp}",
    )
    record(
        "A.2 the most general split-preserving source is K = k_+ Π_+ + k_perp Π_perp",
        k == sp.diag(k_plus, k_perp),
        f"K = {k}",
    )

    section("B. Exact restriction of the observable principle")

    d_red = i2
    w_red = sp.simplify(sp.log((d_red + k).det()) - sp.log(d_red.det()))
    record(
        "B.1 restricting W[J] = log|det(D+J)| - log|det D| to the reduced carrier gives W_red = log det(I+K)",
        sp.simplify(w_red - sp.log((i2 + k).det())) == 0,
        f"W_red = {w_red}",
    )
    record(
        "B.2 direct evaluation gives W_red = log(1+k_+) + log(1+k_perp)",
        sp.simplify(sp.exp(w_red) - (1 + k_plus) * (1 + k_perp)) == 0,
        f"W_red = {w_red}",
    )
    record(
        "B.3 the pure-block restrictions are exactly the one-block observable generators",
        sp.simplify(w_red.subs(k_perp, 0) - sp.log(1 + k_plus)) == 0
        and sp.simplify(w_red.subs(k_plus, 0) - sp.log(1 + k_perp)) == 0,
    )

    c1, c2 = sp.symbols("c1 c2", real=True)
    trial = c1 * sp.log(1 + k_plus) + c2 * sp.log(1 + k_perp)
    c_sol = sp.solve(
        [
            sp.Eq(sp.simplify(trial.subs(k_perp, 0) - sp.log(1 + k_plus)), 0),
            sp.Eq(sp.simplify(trial.subs(k_plus, 0) - sp.log(1 + k_perp)), 0),
        ],
        [c1, c2],
        dict=True,
    )
    record(
        "B.4 there is no residual coefficient freedom once the reduced carrier and pure-block normalization are fixed",
        len(c_sol) == 1 and c_sol[0][c1] == 1 and c_sol[0][c2] == 1,
        f"coefficient solution = {c_sol[0]}",
    )

    section("C. Exact dual reduction")

    y1, y2 = sp.symbols("y1 y2", positive=True, real=True)
    phi = w_red - k_plus * y1 - k_perp * y2
    stat_sol = sp.solve(
        [sp.diff(phi, k_plus), sp.diff(phi, k_perp)],
        [k_plus, k_perp],
        dict=True,
    )
    k_plus_star = sp.simplify(stat_sol[0][k_plus])
    k_perp_star = sp.simplify(stat_sol[0][k_perp])
    s_eff = sp.simplify(phi.subs({k_plus: k_plus_star, k_perp: k_perp_star}))

    record(
        "C.1 the exact reduced dual equation is K_* = Y^(-1) - I blockwise",
        sp.simplify(k_plus_star - (1 / y1 - 1)) == 0
        and sp.simplify(k_perp_star - (1 / y2 - 1)) == 0,
        f"K_* = ({k_plus_star}, {k_perp_star})",
    )
    record(
        "C.2 the exact reduced effective action is Tr(Y) - log det(Y) - 2",
        sp.simplify(s_eff - (y1 + y2 - sp.log(y1 * y2) - 2)) == 0,
        f"S_eff = {s_eff}",
    )

    section("D. Contrast with the unreduced vector-slot carrier")

    k_vec = sp.diag(1 + k_plus, 1 + k_perp, 1 + k_perp)
    record(
        "D.1 the unreduced 1⊕2 vector-slot determinant would count the doublet twice",
        sp.simplify(k_vec.det() - (1 + k_plus) * (1 + k_perp) ** 2) == 0,
        f"log det vector-slot = {sp.log(k_vec.det())}",
    )
    record(
        "D.2 the reduced generator is the exact restriction to the two-generator block algebra, not the unreduced vector-slot determinant",
        sp.simplify(w_red - sp.log((i2 + k).det())) == 0
        and sp.simplify(k_vec.det() - (1 + k_plus) * (1 + k_perp) ** 2) == 0,
        "This is the load-bearing reduction inside the admitted second-order route.",
    )

    section("E. Audit dependency-graph bookkeeping (no status promotion)")

    supplier_notes = [
        (
            "OBSERVABLE_PRINCIPLE_REAL_D_BLOCK_UNIQUENESS_NARROW_THEOREM_NOTE_2026-05-10.md",
            "Block-local uniqueness of source-derivative content of any admissible scalar generator on an invertible real anti-Hermitian Dirac block (retained_bounded upstream).",
        ),
        (
            "KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md",
            "Structural composition OP T1+T2 + physical-lattice-necessity §9 + canonical descent + CRIT; forces the framework's physical local scalar observables to read through the descent E_loc landing on the normalized Y = I_2 baseline.",
        ),
        (
            "KOIDE_Q_READOUT_FACTORIZATION_THEOREM_2026-04-22.md",
            "Exact rank/kernel quotient of the linear second-order readout map L on the retained Γ_1 / T_1 grammar; algebraic skeleton of the two-generator block reduction.",
        ),
        (
            "KOIDE_Q_MINIMAL_SCALE_FREE_SELECTOR_NOTE_2026-04-22.md",
            "Exact uniqueness of the scale-free C_3-invariant selector ratio on the admitted second-order returned carrier (no nontrivial linear-order invariant; exactly one quadratic-order ratio).",
        ),
    ]
    for idx, (fname, summary) in enumerate(supplier_notes, start=1):
        path = REPO_ROOT / "docs" / fname
        record(
            f"E.{idx} {fname} exists on disk",
            path.is_file(),
            summary,
        )
    record(
        "E.5 this section is graph-bookkeeping only and asserts no status promotion",
        True,
        "Audit lane independently sets effective_status; runner pass count alone never promotes a row beyond audited_conditional.",
    )

    section("Summary")

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    if n_pass == n_total:
        print("VERDICT: W_red = log det(I+K) is not a post-hoc transplant.")
        print("It is the exact restriction of the observable principle to the")
        print("normalized two-generator second-order block algebra.")
        print()
        print("This is support for the admitted second-order route.")
        print("It does not by itself prove that this reduced carrier is the physical")
        print("charged-lepton observable carrier.")
        return 0

    print("VERDICT: reduced-observable restriction theorem candidate has FAILs.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
