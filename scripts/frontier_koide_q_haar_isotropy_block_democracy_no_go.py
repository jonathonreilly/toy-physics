#!/usr/bin/env python3
"""
Koide Q Haar/isotropy block-democracy no-go.

This runner tests a sharp representation-theoretic naturality route:

    retained C_3 carrier + natural Haar/isotropic measure
    -> equal real-irrep block totals
    -> K_TL = 0.

The result is negative.  Haar/O(3)-isotropic source ensembles equalize energy
per real dimension, not total energy per C_3 isotype block.  Since the singlet
has rank 1 and the real doublet has rank 2, isotropy gives E_perp/E_+ = 2,
which is off Koide.  General C_3-invariant Gaussian ensembles leave one
variance ratio free; selecting the Koide block-total law is exactly an extra
prior/measure primitive.
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
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def q_from_ratio(r: sp.Expr) -> sp.Expr:
    """Koide Q in the retained block-energy coordinate R = E_perp/E_plus."""
    return sp.simplify((1 + r) / 3)


def ktl_from_ratio(r: sp.Expr) -> sp.Expr:
    """Traceless source scalar in the trace-2 normalized two-block carrier."""
    y = sp.simplify(2 / (1 + r))
    return sp.simplify((1 - y) / (y * (2 - y)))


def main() -> int:
    section("A. C_3 projectors and ranks")

    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)
    J = sp.ones(3, 3)
    P_plus = sp.Rational(1, 3) * J
    P_perp = I3 - P_plus

    record(
        "A.1 P_plus and P_perp are the retained singlet/doublet projectors",
        P_plus**2 == P_plus
        and P_perp**2 == P_perp
        and P_plus * P_perp == sp.zeros(3, 3)
        and sp.simplify(C * P_plus - P_plus * C) == sp.zeros(3, 3)
        and sp.simplify(C * P_perp - P_perp * C) == sp.zeros(3, 3),
        f"rank(P_plus)={P_plus.rank()}, rank(P_perp)={P_perp.rank()}",
    )
    record(
        "A.2 the two blocks have unequal real dimensions",
        sp.trace(P_plus) == 1 and sp.trace(P_perp) == 2,
        "dim(+)=1, dim(perp)=2.",
    )

    section("B. General C_3-invariant Gaussian source")

    sigma_plus, sigma_perp = sp.symbols("sigma_plus sigma_perp", positive=True, real=True)
    covariance = sp.simplify(sigma_plus**2 * P_plus + sigma_perp**2 * P_perp)
    record(
        "B.1 Sigma = sigma_plus^2 P_plus + sigma_perp^2 P_perp is C_3-invariant",
        sp.simplify(C * covariance * C.T - covariance) == sp.zeros(3, 3),
        "C_3 covariance leaves one positive variance ratio.",
    )

    e_plus = sp.simplify(sp.trace(P_plus * covariance))
    e_perp = sp.simplify(sp.trace(P_perp * covariance))
    r = sp.simplify(e_perp / e_plus)
    record(
        "B.2 expected block-energy ratio is dimension-weighted",
        sp.simplify(r - 2 * sigma_perp**2 / sigma_plus**2) == 0,
        f"E_plus={e_plus}, E_perp={e_perp}, R=E_perp/E_plus={r}",
    )

    q = q_from_ratio(r)
    ktl = ktl_from_ratio(r)
    record(
        "B.3 Koide block democracy requires a non-isotropic variance ratio",
        sp.solve(sp.Eq(r, 1), sigma_plus**2, dict=True) == [
            {sigma_plus**2: 2 * sigma_perp**2}
        ],
        f"R=1 requires sigma_plus^2 = 2 sigma_perp^2; K_TL(R)={ktl}, Q(R)={q}",
    )

    section("C. Haar/O(3)-isotropic specialization")

    isotropic_r = sp.simplify(r.subs(sigma_plus, sigma_perp))
    isotropic_q = sp.simplify(q_from_ratio(isotropic_r))
    isotropic_ktl = sp.simplify(ktl_from_ratio(isotropic_r))
    record(
        "C.1 Haar/O(3) isotropy gives equal variance per real dimension",
        isotropic_r == 2,
        f"R_iso={isotropic_r}; block totals follow ranks 1:2.",
    )
    record(
        "C.2 the Haar/isotropic point is off Koide",
        isotropic_q != sp.Rational(2, 3) and isotropic_ktl != 0,
        f"Q_iso={isotropic_q}, K_TL_iso={isotropic_ktl}",
    )

    alpha_plus = sp.Rational(1, 2)
    alpha_perp = sp.Rational(2, 2)
    mean_p_plus = sp.simplify(alpha_plus / (alpha_plus + alpha_perp))
    mean_p_perp = sp.simplify(alpha_perp / (alpha_plus + alpha_perp))
    record(
        "C.3 the Haar block-total law is Beta(1/2,1), not equal block totals",
        mean_p_plus == sp.Rational(1, 3) and mean_p_perp == sp.Rational(2, 3),
        f"E[p_plus]={mean_p_plus}, E[p_perp]={mean_p_perp}; no interior equal-block mode.",
    )

    section("D. Equal-block prior is an extra primitive")

    block_prior_r = sp.Rational(1, 1)
    block_prior_q = q_from_ratio(block_prior_r)
    block_prior_ktl = ktl_from_ratio(block_prior_r)
    record(
        "D.1 equal total block weights do land on the Koide leaf",
        block_prior_q == sp.Rational(2, 3) and block_prior_ktl == 0,
        f"R_block={block_prior_r}, Q={block_prior_q}, K_TL={block_prior_ktl}",
    )
    record(
        "D.2 equal total block weights differ from Haar/isotropic naturality",
        block_prior_r != isotropic_r,
        "Block-total democracy is not the Haar push-forward of an isotropic real carrier.",
    )

    section("E. Explicit retained off-Koide countermeasure")

    sigma_iso = {sigma_plus: 1, sigma_perp: 1}
    sigma_koide = {sigma_plus: sp.sqrt(2), sigma_perp: 1}
    record(
        "E.1 isotropic covariance is retained and gives nonzero K_TL",
        sp.simplify((covariance.subs(sigma_iso)) - I3) == sp.zeros(3, 3)
        and isotropic_ktl == sp.Rational(3, 8),
        "Sigma=I is maximally natural by O(3), but it gives R=2 and K_TL=3/8.",
    )
    record(
        "E.2 Koide covariance is anisotropic at the real-dimension level",
        sp.simplify((covariance.subs(sigma_koide)) - I3) != sp.zeros(3, 3),
        "The Koide total-block law weights the one-dimensional singlet twice per real dimension.",
    )

    section("F. Verdict")

    record(
        "F.1 Haar/isotropic naturality does not force K_TL=0",
        True,
        "It selects equal energy per real dimension, hence R=2, Q=1, and K_TL=3/8.",
    )
    record(
        "F.2 Q remains open after the Haar/isotropy audit",
        True,
        "Residual primitive: justify equal total real-isotype block weights rather than Haar/rank weights.",
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
        print("VERDICT: Haar/isotropic representation naturality does not close Q.")
        print("It gives dimension-weighted block totals, not the equal-total-block")
        print("law equivalent to K_TL=0.")
        print()
        print("KOIDE_Q_HAAR_ISOTROPY_BLOCK_DEMOCRACY_NO_GO=TRUE")
        print("Q_HAAR_ISOTROPY_CLOSES_Q=FALSE")
        print("RESIDUAL_PRIOR=equal_total_real_isotype_block_weights_equiv_K_TL=0")
        return 0

    print("VERDICT: Haar/isotropy audit has FAILs.")
    print()
    print("KOIDE_Q_HAAR_ISOTROPY_BLOCK_DEMOCRACY_NO_GO=FALSE")
    print("Q_HAAR_ISOTROPY_CLOSES_Q=FALSE")
    print("RESIDUAL_PRIOR=equal_total_real_isotype_block_weights_equiv_K_TL=0")
    return 1


if __name__ == "__main__":
    sys.exit(main())

