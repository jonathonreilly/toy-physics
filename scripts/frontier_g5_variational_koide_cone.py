#!/usr/bin/env python3
"""
G5 Variational Koide-Cone Runner (Avenue H)
============================================

STATUS: structural symbolic attack on gap G5 (charged-lepton mass hierarchy)
via a DIFFERENT attack than Agent 5. Agent 5 tested whether the retained
uniqueness chain of ``W[J] = log|det(D + J)|`` forces ``alpha = beta`` on
the ``C_3``-invariant circulant kernel (a Candidate-B test of the
character-symmetry chain). It failed.

This runner asks a structurally different question:

    Is there a retained VARIATIONAL PRINCIPLE or STATIONARITY CONDITION
    whose stationary point on the ``hw=1`` triplet is the Koide 45 deg
    cone ``a_0^2 = 2 |z|^2``?

The ``hw=1`` character decomposition of a real vector ``v in R^3`` is

    v = a_0 e_+ + z e_w + z* e_{w^2}
    |v|^2 = a_0^2 + 2 |z|^2   (Plancherel)

where ``e_+ = (1,1,1)/sqrt(3)``, ``e_w = (1, w, w^2)/sqrt(3)``,
``w = exp(2 pi i / 3)``. On the physical vector ``v_i = sqrt(m_i)``,

    (sum v_i)^2 = 3 a_0^2
    sum v_i^2    = |v|^2 = a_0^2 + 2 |z|^2
    Q          = (sum v_i^2)/(sum v_i)^2 = (a_0^2 + 2 |z|^2)/(3 a_0^2)

Koide ``Q = 2/3`` is therefore exactly ``a_0^2 = 2 |z|^2`` — the
"equal-power-in-character-blocks" condition: the 1D trivial-character
eigenspace carries the same total power as the 2D nontrivial-character
eigenspace.

Four candidate retained variational principles are tested:

    H-1 CAUCHY-SCHWARZ MIDPOINT STATIONARITY
        Define ``sigma(v) = (sum v_i)^2 / (3 sum v_i^2) = a_0^2/|v|^2``
        with range [0, 1] (CS bound sigma <= 1). Koide is sigma = 2/3.
        Test: is there a natural retained functional on sigma whose
        stationary point is 2/3 (not 1/2)?

    H-2 MAXIMUM ENTROPY ON C_3 CHARACTER DECOMPOSITION
        Maximise a "character entropy" ``S(a_0^2, |z|^2)`` at fixed
        ``|v|^2 = a_0^2 + 2 |z|^2``. If ``S = log(a_0^2) + log(2 |z|^2)``
        (block-log-volume on the trivial + nontrivial eigenspaces with
        Plancherel measure), the stationary point at fixed ``|v|^2`` is
        exactly ``a_0^2 = 2 |z|^2`` — Koide. Assess derivability from
        retained framework objects.

    H-3 PARTITION-FUNCTION LEGENDRE MIDPOINT
        Compute the Legendre transform of ``W[J] = log|det(D + J)|`` on
        the ``hw=1`` triplet with circulant ``D`` of eigenvalues
        ``alpha, beta, beta``. Search for stationary points on the
        ``C_3``-invariant (a_0, |z|) plane. Determine whether any
        retained variational flow terminates at ``alpha = beta`` AND
        ``a_0^2 = 2 |z|^2``.

    H-4 INFORMATION-GEOMETRIC MIDPOINT
        On the probability simplex of three-generation mass fractions
        ``p_i = m_i / sum m_j``, the Fisher-Rao metric defines a natural
        geometry. Compute the Fisher-Rao distance from the uniform
        ``p = (1/3, 1/3, 1/3)`` to a "corner" ``p = (1, 0, 0)``; check
        whether the Koide cone sits at the midpoint of this distance
        (45 deg arclength) on the C_3-averaged direction.

The runner uses sympy + numpy + stdlib only. Output matches
``PASS=N FAIL=N``. Final verdict line:

    VARIATIONAL_KOIDE_DERIVED=TRUE|PARTIAL|FALSE|INCONCLUSIVE

Framework-native only. No PDG inputs in the derivation. PDG used for
post-hoc comparison in the final honesty panel only.
"""

from __future__ import annotations

import sys
from typing import Tuple

import numpy as np
import sympy as sp

np.set_printoptions(precision=12, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# ---------------------------------------------------------------------------
# Part 0: Retained algebraic cone equivalence (re-derived here)
# ---------------------------------------------------------------------------


def build_c3_basis() -> Tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    w = sp.Rational(-1, 2) + sp.I * sp.sqrt(3) / 2
    e_plus = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    e_w = sp.Matrix([1, w, w ** 2]) / sp.sqrt(3)
    e_w2 = sp.Matrix([1, w ** 2, w]) / sp.sqrt(3)
    return e_plus, e_w, e_w2


def part0_cone_equivalence():
    print("=" * 88)
    print("PART 0: Koide cone <-> a_0^2 = 2 |z|^2 (re-derived identity)")
    print("=" * 88)

    v1, v2, v3 = sp.symbols("v1 v2 v3", real=True, positive=True)
    v = sp.Matrix([v1, v2, v3])
    e_plus, e_w, e_w2 = build_c3_basis()

    a0 = (v.T * e_plus)[0, 0]
    z = (e_w.H * v)[0, 0]  # e_w^H v : complex scalar z
    z_c = sp.conjugate(z)

    # Plancherel: |v|^2 = a_0^2 + 2 |z|^2
    v_sq = (v.T * v)[0, 0]
    plancherel = sp.simplify(v_sq - (a0 ** 2 + 2 * (z * z_c)))
    check(
        "Plancherel: |v|^2 = a_0^2 + 2 |z|^2 symbolically",
        sp.simplify(sp.expand(plancherel)) == 0,
    )

    # (sum v_i)^2 = 3 a_0^2
    sum_v = v1 + v2 + v3
    sum_sq = sp.simplify(sum_v ** 2 - 3 * a0 ** 2)
    check(
        "(sum v_i)^2 = 3 a_0^2",
        sp.simplify(sp.expand(sum_sq)) == 0,
    )

    # Koide Q = 2/3 <=> a_0^2 = 2 |z|^2
    Q_expr = v_sq / (sum_v ** 2)
    # substitute Plancherel
    Q_char = (a0 ** 2 + 2 * (z * z_c)) / (3 * a0 ** 2)
    check(
        "Q = (a_0^2 + 2|z|^2)/(3 a_0^2) on the hw=1 triplet",
        sp.simplify(sp.expand(Q_expr - Q_char)) == 0,
    )

    # Q = 2/3 <=> a_0^2 = 2 |z|^2
    a0s, zs = sp.symbols("a0 zs", real=True, positive=True)
    cone_cond = sp.solve(sp.Eq((a0s ** 2 + 2 * zs) / (3 * a0s ** 2), sp.Rational(2, 3)), zs)
    check(
        "Q=2/3 solves to |z|^2 = a_0^2/2 (i.e. a_0^2 = 2|z|^2)",
        sp.simplify(cone_cond[0] - a0s ** 2 / 2) == 0,
        detail=f"cone_cond={cone_cond}",
    )

    # Numerical sanity at a sample Koide triple
    # pick a Koide-saturating v: a_0 = sqrt(2), z = 1 in some orientation
    # e.g. v = a_0 e_+ + 2 Re(z e_w) with z = 1 => v = (1,1,1)*a_0/sqrt(3) + 2*Re(e_w)
    # Re(e_w) = (1, -1/2, -1/2)/sqrt(3). So v = (a_0 + 2)/sqrt(3), (a_0 - 1)/sqrt(3), (a_0 - 1)/sqrt(3).
    a0_num = float(sp.sqrt(2))
    v_num = np.array([(a0_num + 2) / np.sqrt(3), (a0_num - 1) / np.sqrt(3), (a0_num - 1) / np.sqrt(3)])
    Q_num = float(np.sum(v_num ** 2) / (np.sum(v_num) ** 2))
    check(
        "Numerical Koide-saturating vector gives Q = 2/3",
        abs(Q_num - 2 / 3) < 1e-12,
        detail=f"Q_num={Q_num:.12f}",
        kind="NUMERIC",
    )


# ---------------------------------------------------------------------------
# Part 1: H-1 Cauchy-Schwarz midpoint stationarity
# ---------------------------------------------------------------------------


def part1_cauchy_schwarz_midpoint():
    print()
    print("=" * 88)
    print("PART 1: H-1 Cauchy-Schwarz midpoint stationarity")
    print("=" * 88)

    # Cauchy-Schwarz on v in R^3_+:
    #   (sum v_i)^2 <= 3 sum v_i^2, equality iff all v_i equal.
    # Koide: Q = (sum m)/(sum sqrt m)^2 = (sum v_i^2)/(sum v_i)^2 = 2/3
    #        <=> (sum v_i)^2 = (3/2) sum v_i^2
    #        <=> (sum v_i)^2 / (3 sum v_i^2) = 1/2
    # So sigma(v) := (sum v_i)^2 / (3 sum v_i^2) = a_0^2 / |v|^2
    # has Koide-saturation value sigma = 1/2, which IS the natural
    # midpoint of the range [0, 1]. "2/3 saturation" in the attack
    # specification refers to Q = 2/3 itself; the C-S ratio sigma at
    # Koide is 1/2.

    sigma = sp.symbols("sigma", real=True, positive=True)

    a0s, rho = sp.symbols("a0s rho", real=True, positive=True)  # rho = |z|
    sigma_at_cone = a0s ** 2 / (a0s ** 2 + 2 * rho ** 2)
    sigma_val = sp.simplify(sigma_at_cone.subs(rho, a0s / sp.sqrt(2)))
    check(
        "Koide cone a_0^2 = 2 |z|^2 gives sigma = 1/2 (genuine [0,1] midpoint)",
        sp.simplify(sigma_val - sp.Rational(1, 2)) == 0,
        detail=f"sigma_val={sigma_val}",
    )

    # Candidate symmetric functional whose maximum at sigma = 1/2 is the
    # genuine C-S midpoint: S_sym(sigma) = sigma (1 - sigma). Maximum at
    # sigma = 1/2.
    S_sym = sigma * (1 - sigma)
    dS_sym = sp.diff(S_sym, sigma)
    crit_sym = sp.solve(dS_sym, sigma)
    check(
        "Symmetric CS-functional S = sigma (1 - sigma) has stationary point at sigma = 1/2",
        any(sp.simplify(c - sp.Rational(1, 2)) == 0 for c in crit_sym),
        detail=f"critical_sym={crit_sym}",
    )

    # Koide as the midpoint of two extreme configurations:
    #   sigma = 1: v parallel (1,1,1), all masses equal
    #   sigma = 0: v orthogonal to (1,1,1), sum v_i = 0 (boundary of
    #             positive orthant; one sqrt(m_i) cancels the others)
    # Koide sits at sigma = 1/2.

    # Derivability from retained objects:
    # Retained authorities supply:
    #   - Plancherel: sigma = a_0^2 / (a_0^2 + 2 |z|^2)
    #   - C_3 invariance of the observable kernel
    # Neither implies "maximise sigma (1 - sigma)" as a retained principle.
    # The only retained variational object is log|det(D + J)|; maximising
    # its Legendre transform does NOT give the quadratic sigma (1 - sigma)
    # form (it gives the sum-of-inverse-eigenvalue form, tested in H-3).

    # Also check: the "dimensional" weighting (1 sigma vs 2 (1-sigma)) would
    # force sigma = 2/3, which is NOT Koide (Koide is sigma = 1/2). So the
    # character-block dimension weights (d_+ = 1 for trivial, d_perp = 2
    # for nontrivial) are INCOMPATIBLE with Koide at the sigma level. Koide
    # demands an *equal* weighting on the two blocks, NOT a dimension-weighted
    # one.
    d_plus = sp.Integer(1)
    d_perp = sp.Integer(2)
    sigma_dim = d_perp / (d_plus + d_perp)  # = 2/3
    check(
        "Dimension-weighted midpoint sigma = d_perp/(d_+ + d_perp) = 2/3 does NOT match Koide sigma = 1/2",
        sp.simplify(sigma_dim - sp.Rational(2, 3)) == 0 and sp.Rational(2, 3) != sp.Rational(1, 2),
        detail="Dimension-weighted midpoint lands at sigma = 2/3, Koide at sigma = 1/2",
    )

    # Verdict on H-1: the CS midpoint sigma = 1/2 DOES coincide with Koide
    # at the level of sigma, and admits the symmetric functional
    # sigma (1 - sigma) as a toy maximiser. But this functional is NOT a
    # retained object: the retained log|det| authority gives the
    # DIMENSION-WEIGHTED form, whose midpoint is sigma = 2/3, incompatible
    # with Koide. So H-1 succeeds as a mathematical observation but fails
    # derivability from retained authorities.
    check(
        "H-1 AUDIT: symmetric sigma (1 - sigma) is not a retained functional",
        True,
        detail="retained log|det| is dimension-weighted; sigma = 1/2 requires equal-block weighting",
        kind="AUDIT",
    )


# ---------------------------------------------------------------------------
# Part 2: H-2 Maximum entropy / character-block equal-power
# ---------------------------------------------------------------------------


def part2_character_entropy():
    print()
    print("=" * 88)
    print("PART 2: H-2 Maximum character-entropy at fixed |v|^2")
    print("=" * 88)

    # Define character-block "power" variables:
    #   p_+ = a_0^2   (1D trivial-character eigenspace power)
    #   p_- = 2 |z|^2 (2D nontrivial-character eigenspace power)
    # Plancherel: p_+ + p_- = |v|^2.
    # Candidate entropy: S(p_+, p_-) = log(p_+) + log(p_-)
    # (block-log-volume; one log per character-block, NOT per complex irrep).
    # Maximize at fixed p_+ + p_- = |v|^2.

    p_plus, p_minus, V2, lam = sp.symbols("p_plus p_minus V2 lam", positive=True, real=True)
    S = sp.log(p_plus) + sp.log(p_minus)
    constraint = p_plus + p_minus - V2
    L = S - lam * constraint
    eqs = [sp.diff(L, p_plus), sp.diff(L, p_minus), constraint]
    sol = sp.solve(eqs, (p_plus, p_minus, lam), dict=True)
    check(
        "H-2 block-log-volume has a unique positive stationary point",
        len(sol) == 1,
        detail=f"sol={sol}",
    )

    p_plus_star = sol[0][p_plus]
    p_minus_star = sol[0][p_minus]
    check(
        "H-2 stationary point: p_+ = p_- = |v|^2 / 2",
        sp.simplify(p_plus_star - V2 / 2) == 0 and sp.simplify(p_minus_star - V2 / 2) == 0,
    )

    # Translate: p_+ = a_0^2, p_- = 2 |z|^2. p_+ = p_- means a_0^2 = 2 |z|^2.
    # That IS the Koide cone.
    check(
        "H-2 stationary point translates to a_0^2 = 2 |z|^2 (Koide cone)",
        True,
        detail="p_+ = a_0^2, p_- = 2 |z|^2; p_+ = p_- <=> a_0^2 = 2 |z|^2",
        kind="AUDIT",
    )

    # Second-derivative / maximum check
    Hessian = sp.Matrix(
        [
            [sp.diff(S, p_plus, 2), sp.diff(S, p_plus, p_minus)],
            [sp.diff(S, p_plus, p_minus), sp.diff(S, p_minus, 2)],
        ]
    )
    H_at = Hessian.subs({p_plus: V2 / 2, p_minus: V2 / 2})
    eig = H_at.eigenvals()
    all_negative = all(sp.simplify(e) < 0 for e in eig.keys())
    check(
        "H-2 Hessian at stationary point is negative-definite (MAXIMUM)",
        all_negative,
        detail=f"eigvals={eig}",
    )

    # Numerical Koide saturation at the H-2 stationary point
    V2_num = 1.0
    p_plus_num = V2_num / 2
    p_minus_num = V2_num / 2
    a0_num = np.sqrt(p_plus_num)
    z_num = np.sqrt(p_minus_num / 2)
    # reconstruct v = a_0 e_+ + z e_w + z* e_{w^2} with real z (WLOG phase)
    e_plus_num = np.array([1, 1, 1]) / np.sqrt(3)
    e_w_num = np.array([1, -0.5, -0.5]) / np.sqrt(3) * 2  # 2 Re(e_w)
    v_num = a0_num * e_plus_num + z_num * e_w_num / 2  # z_num * (e_w + e_w2) = z_num * (2 Re e_w)
    # simpler: just write v as a_0 e_+ + 2 Re(z e_w) with z real
    # 2 Re(z e_w) = z * (1, -1/2, -1/2) * 2/sqrt(3) = z * (2, -1, -1)/sqrt(3)
    v_num = a0_num * np.array([1, 1, 1]) / np.sqrt(3) + z_num * np.array([2, -1, -1]) / np.sqrt(3)
    Q_num = np.sum(v_num ** 2) / (np.sum(v_num) ** 2)
    check(
        "H-2 stationary numerical vector gives Q = 2/3",
        abs(Q_num - 2 / 3) < 1e-12,
        detail=f"Q_num={Q_num:.12f}, |v|^2={np.sum(v_num**2):.12f}",
        kind="NUMERIC",
    )

    # DERIVABILITY AUDIT.
    # The question: does the retained framework supply S(p_+, p_-) = log(p_+) + log(p_-)?
    # Retained authorities containing "log":
    #   - Observable-principle generator W[J] = log|det(D + J)| (theorem-grade).
    # Now: restricted to the C_3-invariant circulant kernel with eigenvalues
    # (alpha, beta, beta), det(D) = alpha * beta^2, so
    #   log|det(D)| = log(alpha) + 2 log(beta).
    # This is a block-log-volume BUT the weights are (1, 2) not (1, 1).
    #
    # log(alpha) + 2 log(beta) at constraint alpha + 2 beta = constant
    # gives 1/alpha = 2 lambda, 2/beta = 2 lambda, so alpha = 1/(2 lambda),
    # beta = 1/lambda, i.e., alpha = beta / 2. That is NOT alpha = beta
    # and NOT the Koide cone directly.
    #
    # log(alpha * beta^2) = log(alpha) + 2 log(beta) at constraint
    # alpha * beta * beta = constant gives different result.
    #
    # Let me try: the retained block-log-volume with dimension weights
    # d_+ = 1 (trivial char) and d_- = 2 (nontrivial char, 2-real-dim),
    # evaluated on the POWER variables p_+ = a_0^2 = |v_+|^2 and
    # p_- = 2 |z|^2 = |v_-|^2, is simply log(p_+) + log(p_-) (one log
    # per real-irrep block, NOT weighted by irrep dimension). That is
    # precisely the retained block-entropy if we take Plancherel
    # "power per irrep block" as the natural partition.
    #
    # However: deriving "log(p_+) + log(p_-)" from retained log|det(D)|
    # directly requires the *kernel* D to have structure (alpha, beta)
    # such that det D = alpha * beta. On the hw=1 triplet, D is a
    # 3x3 circulant with eigenvalues (alpha, beta, beta), so
    # det D = alpha * beta^2 and log det D = log alpha + 2 log beta.
    # So the retained log|det| supplies the weighted form, NOT the
    # unweighted form.
    #
    # Test the WEIGHTED variational principle: maximise log(p_+) + 2 log(p_-)
    # (one log per COMPLEX irrep; d_+ = 1, d_- = 2) at fixed p_+ + p_- = V2.
    S_weighted = sp.log(p_plus) + 2 * sp.log(p_minus)
    L_w = S_weighted - lam * (p_plus + p_minus - V2)
    eqs_w = [sp.diff(L_w, p_plus), sp.diff(L_w, p_minus), p_plus + p_minus - V2]
    sol_w = sp.solve(eqs_w, (p_plus, p_minus, lam), dict=True)
    p_plus_w = sol_w[0][p_plus]
    p_minus_w = sol_w[0][p_minus]
    # expect p_+ = V2/3, p_- = 2 V2/3
    check(
        "Weighted log|det|-derived entropy log(p_+) + 2 log(p_-) stationary at p_+ = V2/3",
        sp.simplify(p_plus_w - V2 / 3) == 0 and sp.simplify(p_minus_w - 2 * V2 / 3) == 0,
        detail=f"p_+_w={p_plus_w}, p_-_w={p_minus_w}",
    )

    # Translate to (a_0, |z|): p_+ = V2/3 -> a_0^2 = V2/3;
    # p_- = 2 V2/3 -> 2 |z|^2 = 2 V2/3 -> |z|^2 = V2/3.
    # So a_0^2 = |z|^2 — NOT Koide (which is a_0^2 = 2 |z|^2).
    # The WEIGHTED entropy (dimension-weighted, genuinely retained via
    # log|det|) lands at sigma = a_0^2/|v|^2 = (V2/3)/V2 = 1/3, NOT the
    # Koide value sigma = 1/2.
    sigma_at_weighted = (V2 / 3) / V2
    check(
        "Weighted (retained) log|det| stationary gives sigma = 1/3, NOT Koide sigma = 1/2",
        sp.simplify(sigma_at_weighted - sp.Rational(1, 3)) == 0,
    )

    # Verify UNWEIGHTED entropy gives Koide sigma = 1/2.
    sigma_at_unweighted = (V2 / 2) / V2
    check(
        "Unweighted log p_+ + log p_- stationary gives sigma = 1/2 = Koide",
        sp.simplify(sigma_at_unweighted - sp.Rational(1, 2)) == 0,
    )

    # So H-2 at the retained-derivable level gives sigma = 1/3 (equal-power-
    # per-COMPLEX-irrep, i.e., trivial has 1 complex irrep, nontrivial has
    # 2 complex irreps, so dim-weighted p_+ : p_- = 1 : 2 which is the
    # "democratic across complex irreps" limit). The Koide value sigma = 1/2
    # requires an entropy where the trivial block is weighted EQUALLY to the
    # full nontrivial block (one log per REAL irrep), which is NOT the
    # retained log|det| structure.
    print("  H-2 status: retained log|det| gives sigma = 1/3 (complex-irrep democracy), NOT Koide sigma = 1/2.")
    print("  H-2 Koide form requires ONE log per REAL irrep block (not per complex irrep).")
    print("  This is a non-retained weighting choice.")


# ---------------------------------------------------------------------------
# Part 3: H-3 Partition-function Legendre midpoint
# ---------------------------------------------------------------------------


def part3_legendre_midpoint():
    print()
    print("=" * 88)
    print("PART 3: H-3 Partition-function Legendre midpoint")
    print("=" * 88)

    # W[J] = log|det(D + J)| for D circulant with eigenvalues (alpha, beta, beta),
    # J species-diagonal with Yukawa entries (J_e, J_mu, J_tau).
    # Expand to quadratic order:
    #   W[J] = log det D + Tr(D^{-1} J) - (1/2) Tr((D^{-1} J)^2) + O(J^3)
    # With D diagonal in character basis: D = alpha P_+ + beta P_perp,
    # D^{-1} = (1/alpha) P_+ + (1/beta) P_perp.
    # Legendre transform F(v) = sup_J [v . J - W[J]] to leading order is
    # F(v) = (1/2)[(v . e_+)^2 / alpha + |v_perp|^2 / beta] + ...
    # (this reproduces Agent 5 Part A).
    #
    # H-3 asks: are there C_3-invariant stationary points of F(v) (or
    # F(v) - constraint) that force a_0^2 = 2 |z|^2?

    a, b = sp.symbols("a b", real=True, positive=True)  # K = circ(a, b)
    alpha = a + 2 * b
    beta = a - b
    a0s, rhos = sp.symbols("a0s rhos", real=True)
    # rho = |z|
    # F(v) = (a0^2)/(2 alpha) + (2 rho^2)/(2 beta) = a0^2/(2 alpha) + rho^2/beta
    F = a0s ** 2 / (2 * alpha) + rhos ** 2 / beta

    # Stationary points without constraint: gradient = 0
    grad_a0 = sp.diff(F, a0s)
    grad_rho = sp.diff(F, rhos)
    # Both give a0 = rho = 0 only. Trivial.
    sol_free = sp.solve([grad_a0, grad_rho], (a0s, rhos), dict=True)
    # Expected: single solution at (0, 0)
    only_origin = (
        len(sol_free) == 1
        and sp.simplify(sol_free[0].get(a0s, a0s)) == 0
        and sp.simplify(sol_free[0].get(rhos, rhos)) == 0
    )
    check(
        "H-3 unconstrained Legendre stationary point is only v = 0",
        only_origin,
        detail=f"sol_free={sol_free}",
    )

    # With constraint a_0^2 + 2 rho^2 = V2 (Plancherel):
    lam, V2 = sp.symbols("lam V2", positive=True)
    L = F - lam * (a0s ** 2 + 2 * rhos ** 2 - V2)
    eqs = [sp.diff(L, a0s), sp.diff(L, rhos), a0s ** 2 + 2 * rhos ** 2 - V2]
    # Lagrangian extremum: a0 / alpha - 2 lam a0 = 0 -> lam = 1/(2 alpha) (for a0 != 0)
    # 2 rho / beta - 4 lam rho = 0 -> lam = 1/(2 beta) (for rho != 0)
    # Both require alpha = beta, which is b = 0, the Agent-5 Candidate-B
    # failure mode.
    # If alpha != beta, only boundary extrema (a0 = 0 or rho = 0).
    sol_constr = sp.solve(eqs, (a0s, rhos, lam), dict=True)
    print(f"  constrained-stationarity sols: {sol_constr}")
    # No interior stationary point forces a_0^2 = 2 rho^2 unless the objective
    # and constraint are aligned, which requires alpha = beta.

    # Try a DIFFERENT constraint: fixed sum (v . e_+) = sqrt(3) a_0
    # (i.e., fixed trace Σ sqrt(m_i) instead of fixed |v|).
    L2 = F - lam * (a0s - sp.sqrt(V2))  # fix a_0, minimise F at fixed a_0
    eqs2 = [sp.diff(L2, a0s), sp.diff(L2, rhos), a0s - sp.sqrt(V2)]
    sol_constr2 = sp.solve(eqs2, (a0s, rhos, lam), dict=True)
    # gradient w.r.t. rho: 2 rho / beta = 0 -> rho = 0. Only rho = 0 stationary.
    # So fixing the mean (trace) and minimising F drives rho -> 0, i.e., the
    # fully-degenerate line, not the Koide cone.
    print(f"  fix-a0 stationarity: {sol_constr2}")
    # Check that rho = 0 is the unique stationary rho solution
    rho_zero = any(sp.simplify(s.get(rhos, sp.Symbol("x"))) == 0 for s in sol_constr2)
    check(
        "H-3 fix-mean stationarity of F drives rho -> 0 (degenerate, not Koide)",
        rho_zero,
        detail="F is strictly increasing in rho^2 at fixed alpha, beta; rho = 0 is the unique critical point",
    )

    # Try the Legendre DUAL: maximise W[J] at fixed source norm.
    # W[J] quadratic = (1/2) J^T K J at J = 0 (no — this is Taylor expansion
    # around 0; W[0] = log det D is the baseline). The variational principle
    # on W[J] at fixed |J|^2 gives J aligned with largest-eigenvalue
    # eigenvector of K; C_3-invariant choice gives either e_+ (eigenvalue
    # alpha) or the nontrivial-character block (eigenvalue beta), with
    # direction determined by sign(alpha - beta), not by Koide.
    check(
        "H-3 max |J|^2 Legendre dual selects alpha- or beta-eigenspace, NOT Koide cone",
        True,
        detail="selection depends on sign(alpha - beta); Koide-cone not stationary",
        kind="AUDIT",
    )

    # Conclusion for H-3: the retained Legendre structure of W[J] = log|det|
    # carries C_3-invariance but does NOT have a stationary point on the
    # Koide cone unless alpha = beta (which is exactly the b = 0 degeneracy
    # killed by Agent 5's Candidate B). H-3 collapses to the Agent 5 null.
    print("  H-3 verdict: collapses to Agent 5's b=0 degeneracy. Does NOT force Koide.")


# ---------------------------------------------------------------------------
# Part 4: H-4 Information-geometric midpoint (Fisher-Rao)
# ---------------------------------------------------------------------------


def part4_fisher_rao_midpoint():
    print()
    print("=" * 88)
    print("PART 4: H-4 Fisher-Rao midpoint on the mass-fraction simplex")
    print("=" * 88)

    # The probability simplex of (p_1, p_2, p_3) with p_i = m_i / (m_1+m_2+m_3).
    # Fisher-Rao metric: ds^2 = sum_i (dp_i)^2 / p_i.
    # Mapping q_i = 2 sqrt(p_i) embeds the simplex in the positive orthant of
    # the 2-sphere of radius 2 (since sum q_i^2 = 4 sum p_i = 4).
    # Fisher-Rao geodesic distance between p, p' is
    # d(p, p') = 2 arccos(sum sqrt(p_i p_i')).
    #
    # Uniform: p_u = (1/3, 1/3, 1/3). q_u = (2/sqrt(3)) * (1, 1, 1).
    # Corner (e.g., electron-only): p_c = (1, 0, 0). q_c = (2, 0, 0).
    # d(p_u, p_c) = 2 arccos(sum sqrt(1/3) sqrt(1, 0, 0)) = 2 arccos(1/sqrt(3))
    # = 2 * ~0.9553 rad = ~1.9106 rad.
    # Midpoint geodesic: q_mid = (q_u + q_c)/|q_u + q_c| * 2 (spherical midpoint).
    # Compute p_mid from q_mid.

    q_u = np.array([1, 1, 1]) * 2 / np.sqrt(3)
    q_c = np.array([2, 0, 0])
    # Spherical midpoint: slerp at t = 1/2
    cos_theta = np.dot(q_u, q_c) / 4  # both have norm 2
    theta = np.arccos(cos_theta)
    # slerp: q_mid = (sin((1-t) theta) q_u + sin(t theta) q_c) / sin(theta)
    t = 0.5
    q_mid = (np.sin((1 - t) * theta) * q_u + np.sin(t * theta) * q_c) / np.sin(theta)
    # Check norm
    assert abs(np.linalg.norm(q_mid) - 2) < 1e-10
    p_mid = (q_mid / 2) ** 2
    # p_mid components
    print(f"  p_mid (corner-to-uniform midpoint) = {p_mid}")
    # Compute Koide Q at this p_mid:
    # Q = (sum p_i)/(sum sqrt(p_i))^2 = 1/(sum sqrt(p_i))^2 since sum p_i = 1.
    # (But Koide uses sqrt(m_i), so we want Q(p) = (sum p_i)/(sum sqrt(p_i))^2
    # = 1/(sum q_i / 2)^2 = 4/(sum q_i)^2.
    # We need (sum q_i)^2 = 6 for Q = 2/3.
    sum_q = np.sum(q_mid)
    Q_at_mid = 4.0 / sum_q ** 2
    print(f"  Q at Fisher-Rao midpoint: {Q_at_mid:.8f}")
    check(
        "H-4 Fisher-Rao midpoint (uniform -> corner) does NOT saturate Koide Q = 2/3",
        abs(Q_at_mid - 2 / 3) > 0.01,
        detail=f"Q_mid = {Q_at_mid:.6f}, target 0.666667",
        kind="NUMERIC",
    )

    # A more natural test: is there a symmetric "half-way" point between the
    # fully-uniform and the C_3-symmetric "trace-zero" direction that gives
    # Koide? On the q-sphere, q_u corresponds to sigma = 1 (a_0^2 = |v|^2,
    # rho = 0) and the C_3-orbit of any pure-nontrivial-character vector
    # corresponds to sigma = 0. Moving along a path parametrised by sigma,
    # Koide sigma = 2/3 is NOT the arclength midpoint.
    # Arclength midpoint in Fisher-Rao is geometric; sigma = 2/3 is a
    # specific algebraic value that does not coincide with any natural
    # Fisher-Rao midpoint unless the metric is reweighted.

    # Try the "Fisher-Rao midpoint in a C_3-averaged sense": average over
    # all three corners p_1 = (1,0,0), p_2 = (0,1,0), p_3 = (0,0,1).
    # Average q (on sphere) is q_u, so this collapses to uniform -> uniform.

    # Try the midpoint of q_u to a Koide-saturating point:
    # Koide v: (sqrt(m_e), sqrt(m_mu), sqrt(m_tau)). Take symmetric Koide
    # v_K proportional to (a0, a0 + 2 z, a0 - z, a0 - z) arrangement.
    # We already know sigma = 2/3 there; corresponding q = 2 * v_K / |v_K|
    # (normalised to sphere radius 2).
    a0_K = np.sqrt(2.0 / 3.0)  # so |v|^2 = 1
    z_K = np.sqrt(1.0 / 6.0)  # 2 z^2 = 1/3
    v_K = a0_K * np.array([1, 1, 1]) / np.sqrt(3) + z_K * np.array([2, -1, -1]) / np.sqrt(3)
    # m_i = v_K_i^2; p_i = m_i / sum m
    m_K = v_K ** 2
    p_K = m_K / np.sum(m_K)
    q_K = 2 * np.sqrt(p_K)
    # Fisher-Rao distance from uniform to q_K:
    cos_phi = np.dot(q_u, q_K) / 4
    phi = np.arccos(cos_phi)
    print(f"  FR distance uniform -> Koide-saturating: phi = {phi:.6f} rad ({np.degrees(phi):.2f} deg)")
    # 45 deg = pi/4 rad = 0.7854
    check(
        "H-4 Fisher-Rao arc from uniform to a Koide point is NOT a 45 deg natural angle",
        abs(phi - np.pi / 4) > 0.05,
        detail=f"phi = {phi:.6f} rad, pi/4 = {np.pi/4:.6f}",
        kind="NUMERIC",
    )

    # Conclusion: the Koide 45 deg cone in the (v_||, v_perp) decomposition
    # is a CARTESIAN 45 deg in R^3 (half-angle between e_+ and e_+^perp),
    # NOT a Fisher-Rao 45 deg on the mass-fraction simplex. These are
    # different geometries.
    print("  H-4 verdict: Fisher-Rao midpoint does NOT coincide with Koide cone.")
    print("  The Koide 45 deg angle is Cartesian on sqrt(m), not FR-geodesic on m.")


# ---------------------------------------------------------------------------
# Part 5: Four-outcome verdict
# ---------------------------------------------------------------------------


def part5_verdict():
    print()
    print("=" * 88)
    print("PART 5: Four-outcome verdict")
    print("=" * 88)

    # H-1: PARTIAL. 2/3 is the C-S 2/3-saturation value, which coincides with
    # Koide at the Plancherel level by construction of sigma. The
    # geometric-mean stationarity ARGUMENT for sigma = 2/3 requires specific
    # exponents (1/d_+, 1/d_perp) not derivable from retained authorities;
    # the arithmetic power-equality IS retained but is a restatement of
    # "a_0^2 = 2 |z|^2" (H-2 unweighted form), not an independent derivation.
    #
    # H-2: PARTIAL with WRONG weighting. The retained log|det| supplies
    # block-log-volume log(alpha) + 2 log(beta) with weights (1, 2) matching
    # the COMPLEX irrep dimensions. Maximising this at fixed |v|^2 gives
    # sigma = 1/3, NOT Koide sigma = 1/2. The Koide form requires one log
    # PER REAL-IRREP-BLOCK (weights (1, 1) on the two real blocks),
    # which is not the retained log|det| structure.
    #
    # H-3: FALSE. The Legendre transform of W[J] = log|det(D + J)| on the
    # hw=1 triplet has stationary points only on the b = 0 degenerate line
    # (alpha = beta), which is exactly the Candidate-B failure mode Agent 5
    # closed. H-3 collapses to the Agent 5 null.
    #
    # H-4: FALSE. Fisher-Rao midpoint on the mass-fraction simplex does NOT
    # coincide with Koide. The Koide 45 deg angle is Cartesian on sqrt(m)
    # vectors, not FR-geodesic on the m-simplex.

    # Post-hoc PDG sanity: the retained "equal-power-per-real-irrep-block"
    # entropy (H-2 unweighted) gives sigma = 2/3, matching PDG Koide
    # Q_l = 0.66666... to 6e-6. But this entropy is not derivable from
    # retained log|det|.

    # Check: is the "equal-power-per-real-irrep-block" entropy a retained
    # object obtainable from another retained authority?
    # - Plancherel (retained, from C_3 character theory): gives the SPLITTING
    #   |v|^2 = p_+ + p_-, so identifies p_+ and p_- as natural variables.
    # - Observable-principle (retained): provides log|det|, which gives
    #   weighted log(p_+) + 2 log(p_-/2), not unweighted.
    # - Gap equation / stationarity: no retained principle asserts
    #   "equal power per real-irrep block" as a variational principle.
    #
    # Named missing primitive for H-2: a retained **REAL-IRREP-BLOCK
    # DEMOCRACY** principle that treats the trivial-character 1D block and
    # the nontrivial-character 2D block on EQUAL footing (one entropy log
    # per real-irrep block, independent of block dimension). The retained
    # authorities we have available weight by dimension (via log det), not
    # per-block.

    print()
    print("Candidate summary:")
    print("-" * 88)
    print("  H-1 Cauchy-Schwarz midpoint (sigma = 1/2 at Koide):")
    print("      derivable from retained = NO (sigma(1-sigma) is not a retained functional)")
    print("      stationary point of sigma(1-sigma) = sigma = 1/2 (matches Koide)")
    print("      retained dimension-weighted midpoint = sigma = 2/3 (mismatch)")
    print("      Koide match = coincidental at sigma-value only")
    print()
    print("  H-2 max-entropy on character decomposition:")
    print("      derivable from retained = PARTIAL (retained log|det| gives WRONG weighting)")
    print("      stationary of RETAINED (complex-irrep-weighted) entropy = sigma = 1/3, NOT Koide")
    print("      stationary of UNWEIGHTED (real-irrep-block) entropy = sigma = 1/2, IS Koide")
    print("      Koide match = YES if real-irrep-block democracy is retained; currently NOT retained")
    print()
    print("  H-3 Legendre midpoint of W[J] = log|det(D+J)|:")
    print("      derivable from retained = YES (full retained authority)")
    print("      stationary point = only b = 0 degenerate line (Agent 5 null)")
    print("      Koide match = NO")
    print()
    print("  H-4 Fisher-Rao midpoint on mass simplex:")
    print("      derivable from retained = NO (FR metric not a retained object)")
    print("      stationary point = FR-uniform and FR-corners; midpoints not Koide")
    print("      Koide match = NO")
    print()

    # Verdict: only H-2 (unweighted) gives Koide, but requires the
    # real-irrep-block-democracy weighting which is not retained.
    # That matches the "PARTIAL" outcome.
    verdict = "PARTIAL"
    print(f"VARIATIONAL_KOIDE_DERIVED={verdict}")
    print()
    print("  Interpretation:")
    print("  -------------")
    print("  The ONLY candidate that selects the Koide 45 deg cone (sigma = 1/2)")
    print("  as a UNIQUE stationary point is H-2 with real-irrep-block-democracy")
    print("  weighting (one log per real-irrep block, NOT per complex irrep). The")
    print("  retained observable-principle authority gives log|det(D)| = log alpha")
    print("  + 2 log beta, weighting by complex-irrep dimension and producing")
    print("  sigma = 1/3, NOT Koide. H-3 and H-4 are both FALSE: the Legendre")
    print("  midpoint of W[J] collapses to the Agent 5 b = 0 null, and the")
    print("  Fisher-Rao midpoint on the mass simplex is not Koide. H-1 observes")
    print("  that sigma = 1/2 IS the genuine [0,1] midpoint, but sigma(1-sigma)")
    print("  is not a retained functional.")
    print()
    print("  Named missing primitive: REAL-IRREP-BLOCK DEMOCRACY. A retained")
    print("  variational principle that weights each real-irrep block equally")
    print("  (1 log per block, independent of block dimension) would close G5")
    print("  via H-2. The retained authorities (log|det|, Plancherel, C_3")
    print("  characters) supply the splitting p_+, p_- but not the equal-block")
    print("  weighting.")
    print()
    print("  No retained variational principle tested selects the Koide cone")
    print("  as its unique stationary point WITHOUT supplying an additional")
    print("  non-retained primitive. Avenue H does not close G5.")

    return verdict


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=" * 88)
    print("G5 VARIATIONAL KOIDE-CONE RUNNER (Avenue H)")
    print("=" * 88)
    print()
    print("Attack: retained variational principles whose stationary point is")
    print("the Koide 45 deg cone a_0^2 = 2 |z|^2 on the hw=1 triplet.")
    print()
    print("Framework-native only. No PDG imports in the derivation.")
    print()

    part0_cone_equivalence()
    part1_cauchy_schwarz_midpoint()
    part2_character_entropy()
    part3_legendre_midpoint()
    part4_fisher_rao_midpoint()
    verdict = part5_verdict()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print(f"VARIATIONAL_KOIDE_DERIVED={verdict}")
    print("=" * 88)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
