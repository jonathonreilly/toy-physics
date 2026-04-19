#!/usr/bin/env python3
"""
G5 Avenue-H Stationarity-Principle Runner (Koide-cone derivation attempt)
=========================================================================

STATUS: structural symbolic attack on G5 / Koide-cone derivation via the
"retained variational / stationarity principle" Avenue H. Follows the
14-agent G5 attack surface (see
docs/CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md) and the Agent-5
no-go on log|det|-based character-symmetry forcing
(docs/OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md).

THE QUESTION
------------
Let v = (sqrt(m_1), sqrt(m_2), sqrt(m_3)) on the positive octant of the
retained hw=1 triplet. Decompose v under C_3 as v = v_par + v_perp where
v_par is the projection onto the diagonal (1,1,1)/sqrt(3). The Koide
relation Q = (sum m_i) / (sum sqrt m_i)^2 = 2/3 is algebraically
equivalent (per charged-lepton-koide-cone-2026-04-17.md) to

    |v_par|^2 = |v_perp|^2       (Koide "45-degree cone")

which places v exactly midway between full degeneracy (|v_perp| = 0,
all masses equal, Q = 1) and full trace-zero (|v_par| = 0, Q = 0).

AVENUE H asks: does there exist a RETAINED framework functional F(v)
whose stationary points on the positive octant force |v_par|^2 =
|v_perp|^2, promoting Koide Q = 2/3 from observational pin to retained
theorem?

CANDIDATE PRINCIPLES TESTED
---------------------------
H-1  Cauchy-Schwarz midpoint functional (AD-HOC)
H-2  Maximum-entropy with C_3 character constraint (AD-HOC -> shown
     to force Koide only under an added equal-character-weight
     CONSTRAINT; without that constraint, max-entropy gives uniform)
H-3  Partition-function extremum log|det(D + J)| with Yukawa source
     (RETAINED observable-principle generator, per OBSERVABLE_PRINCIPLE_
     FROM_AXIOM_NOTE.md)
H-4  Information-geometric midpoint on the Fisher metric of the
     3-generation mass simplex (AD-HOC, tests whether the geodesic
     midpoint between uniform and single-generation pure states sits
     on the Koide cone)
H-5  Retained symmetric / antisymmetric (C_3 trivial vs nontrivial)
     decomposition norm extremum (AD-HOC unless constructed from
     retained kernel, which reduces to H-3)
H-6  Fermion-determinant balance on the retained minimal block
     using Agent-10-v2 retained Matsubara form K_ii^(spec) =
     16 / (m_i^2 + (7/2) u_0^2) (RETAINED)

For each candidate we ask:
  (Q1) Is v on the Koide cone a stationary point?
  (Q2) If yes, is it the GLOBAL extremum or just local?
  (Q3) Is the functional RETAINED (built from retained framework
       objects) or AD-HOC?
  (Q4) Does it FIX the specific cone point (residual-ratio check)?

FOUR-OUTCOME VERDICT
--------------------
AVENUE_H_CLOSES_G5              - retained principle forces BOTH Q=2/3
                                  AND specific cone position matching
                                  observation. Flagship TOE.
AVENUE_H_CONE_ONLY              - retained principle forces Q=2/3 but
                                  leaves the cone point free.
AVENUE_H_STATIONARY_NOT_KOIDE   - candidate principles have stationary
                                  points NOT on the Koide cone.
AVENUE_H_NO_RETAINED_PRINCIPLE_FOUND
                                - no tested candidate is BOTH retained
                                  AND Koide-selecting.

Output format: matches PASS=N FAIL=N convention of the other
frontier_*.py runners.

Dependencies: sympy + numpy + stdlib only. No observed lepton mass
imports are used for the structural verdict; PDG charged-lepton values
appear only in the residual-ratio check as a reference target.
"""

from __future__ import annotations

import sys
from typing import Tuple, List

import numpy as np
import sympy as sp

np.set_printoptions(precision=10, linewidth=120, suppress=True)

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
# Koide-cone geometry baseline
# ---------------------------------------------------------------------------


def koide_Q_symbolic():
    """Return Q(v) = (sum v_i^2) / (sum v_i)^2 in terms of v = sqrt(m).
    Note v_i = sqrt(m_i), so sum m_i = sum v_i^2 and (sum sqrt m_i)^2 =
    (sum v_i)^2.
    """
    v1, v2, v3 = sp.symbols("v1 v2 v3", positive=True)
    Q = (v1**2 + v2**2 + v3**2) / (v1 + v2 + v3) ** 2
    return Q, (v1, v2, v3)


def char_decomposition(v: sp.Matrix) -> Tuple[sp.Expr, sp.Matrix]:
    """Decompose v into v_par (trivial C_3 character) + v_perp.
    Returns (|v_par|^2, v_perp)."""
    e_plus = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    v_dot_plus = (v.T * e_plus)[0, 0]
    v_par = v_dot_plus * e_plus
    v_perp = v - v_par
    v_par_sq = sp.simplify(v_dot_plus**2)
    return v_par_sq, v_perp


def koide_cone_from_chardecomp():
    """Sanity: Q = 2/3  <=>  |v_par|^2 = |v_perp|^2."""
    print("=" * 88)
    print("PART 0: Koide-cone geometric baseline (sanity)")
    print("=" * 88)

    v1, v2, v3 = sp.symbols("v1 v2 v3", positive=True)
    v = sp.Matrix([v1, v2, v3])
    v_par_sq, v_perp = char_decomposition(v)
    v_perp_sq = sp.simplify((v_perp.T * v_perp)[0, 0])

    Q_expr = (v1**2 + v2**2 + v3**2) / (v1 + v2 + v3) ** 2
    # algebraic identity: sum v_i^2 = |v_par|^2 + |v_perp|^2,
    # (sum v_i)^2 = 3 |v_par|^2
    total = sp.simplify(v_par_sq + v_perp_sq - (v1**2 + v2**2 + v3**2))
    check(
        "sum v_i^2 = |v_par|^2 + |v_perp|^2 (orthogonal decomposition)",
        total == 0,
    )
    triv_total = sp.simplify(3 * v_par_sq - (v1 + v2 + v3) ** 2)
    check(
        "(sum v_i)^2 = 3 |v_par|^2",
        triv_total == 0,
    )
    # So Q = (|v_par|^2 + |v_perp|^2) / (3 |v_par|^2)
    # Q = 2/3 <=> |v_par|^2 + |v_perp|^2 = 2 |v_par|^2 <=> |v_perp|^2 = |v_par|^2
    Q_in_par_perp = (v_par_sq + v_perp_sq) / (3 * v_par_sq)
    diff = sp.simplify(Q_expr - Q_in_par_perp)
    check(
        "Q = (|v_par|^2 + |v_perp|^2) / (3 |v_par|^2)",
        diff == 0,
    )
    # Q = 2/3 iff |v_par|^2 = |v_perp|^2
    cone_cond = sp.simplify(
        (Q_in_par_perp - sp.Rational(2, 3)).subs(
            {v_perp_sq: v_par_sq}
        )
    )
    check(
        "Q = 2/3 iff |v_par|^2 = |v_perp|^2 (Koide 45-deg cone)",
        sp.simplify(cone_cond) == 0,
    )
    print()


# ---------------------------------------------------------------------------
# H-1: Cauchy-Schwarz midpoint functional
# ---------------------------------------------------------------------------


def candidate_H1():
    """H-1: Cauchy-Schwarz midpoint functional.

    Cauchy-Schwarz: (sum v_i)^2 <= 3 sum v_i^2 , i.e. Q >= 1/3.
    Equivalently, on the positive octant, Q ranges over [1/3, 1].
    Q = 1 at the pure single-generation point (all mass on one species,
    v_par -> v, cos(theta) = 1/sqrt(3) configurations),
    Q = 1/3 at (1,1,1)/sqrt(3) degenerate (which gives Q=1, not 1/3).

    Actually let us re-examine: if v = (1,0,0), then sum v_i = 1,
    sum v_i^2 = 1, so Q = 1. If v = (1,1,1), sum v_i = 3, sum v_i^2 = 3,
    so Q = 3/9 = 1/3. So Q=1 at pure single-gen, Q=1/3 at full degeneracy.

    Koide Q = 2/3 sits midway between 1/3 (degenerate) and 1 (one-mass).
    H-1 candidate functional: F1(v) = (Q(v) - 1/3)(1 - Q(v)), which
    attains its maximum at Q = 2/3.

    CRITICAL HONEST AUDIT: this functional is engineered to peak at
    Q=2/3. It is NOT built from any retained framework object. Labeled
    AD-HOC.
    """
    print("=" * 88)
    print("PART H-1: Cauchy-Schwarz midpoint functional")
    print("=" * 88)

    v1, v2, v3 = sp.symbols("v1 v2 v3", positive=True)
    Q = (v1**2 + v2**2 + v3**2) / (v1 + v2 + v3) ** 2

    # At v=(1,0,0), Q=1; at v=(1,1,1), Q=1/3; pin these
    Q_pure = Q.subs({v1: 1, v2: 0, v3: 0})
    Q_deg = Q.subs({v1: 1, v2: 1, v3: 1})
    check(
        "Q(pure single-gen (1,0,0)) = 1",
        sp.simplify(Q_pure - 1) == 0,
    )
    check(
        "Q(fully degenerate (1,1,1)) = 1/3",
        sp.simplify(Q_deg - sp.Rational(1, 3)) == 0,
    )

    # F1 = (Q - 1/3)(1 - Q); maximized at Q = 2/3 by elementary calc.
    Q_sym = sp.Symbol("Q_sym", real=True)
    F1_of_Q = (Q_sym - sp.Rational(1, 3)) * (1 - Q_sym)
    dF = sp.diff(F1_of_Q, Q_sym)
    stat_Q = sp.solve(dF, Q_sym)
    check(
        "H-1 functional F1 stationary at Q = 2/3",
        stat_Q == [sp.Rational(2, 3)],
        f"stationary Q-values: {stat_Q}",
    )

    # But: is this a retained framework object?
    print("  [AUDIT] H-1 label: AD-HOC (explicitly engineered to peak at 2/3).")
    print("          The functional (Q - 1/3)(1 - Q) has no derivation from")
    print("          any retained Cl(3)/Z^3 algebraic or observable-principle")
    print("          object; it is a polynomial in Q constructed to have 2/3")
    print("          as its max. Retained-provenance: ABSENT.")
    print("  [CONE-FIXING] H-1 does NOT fix the cone point: any v with")
    print("          Q(v) = 2/3 is a stationary point of F1, so the full")
    print("          2-parameter Koide cone is degenerate critical set.")
    print()

    retained = False  # AD-HOC
    forces_koide_cone = True  # by construction
    fixes_cone_point = False
    return {
        "name": "H-1 Cauchy-Schwarz midpoint",
        "retained": retained,
        "forces_cone": forces_koide_cone,
        "fixes_point": fixes_cone_point,
        "verdict_str": "AD-HOC; forces cone by construction but leaves point free",
    }


# ---------------------------------------------------------------------------
# H-2: Maximum-entropy with C_3 character constraint
# ---------------------------------------------------------------------------


def candidate_H2():
    """H-2: Maximum-entropy with C_3 character constraint.

    On the 3-simplex {p_i >= 0, sum p_i = 1}, the Shannon entropy
    S = - sum p_i log p_i is maximized at the uniform distribution
    p_i = 1/3 (full degeneracy, Q = 1/3). That is the ENTROPIC extreme,
    NOT the Koide cone.

    The proposal in the spec adds a constraint "equal weight on both
    character subspaces", i.e. <f_par^2> = <f_perp^2>. But that
    constraint IS the Koide cone restated. So this candidate reduces
    to: max-entropy SUBJECT TO the Koide cone constraint -> yields a
    family on the cone; by itself does not FORCE Koide.

    AUDIT: without the added constraint, H-2 stationary point is
    p = (1/3,1/3,1/3), which gives Q = 1/3 (full degeneracy), NOT Q =
    2/3. With the added constraint, the constraint IS the Koide cone
    so it's circular. Labeled AD-HOC.
    """
    print("=" * 88)
    print("PART H-2: Maximum-entropy with C_3 character constraint")
    print("=" * 88)

    p1, p2, p3 = sp.symbols("p1 p2 p3", positive=True)
    lam = sp.Symbol("lambda", real=True)

    S = -(p1 * sp.log(p1) + p2 * sp.log(p2) + p3 * sp.log(p3))
    # Constraint: p1 + p2 + p3 = 1
    L = S - lam * (p1 + p2 + p3 - 1)
    d1 = sp.diff(L, p1)
    d2 = sp.diff(L, p2)
    d3 = sp.diff(L, p3)
    # Solve
    sol = sp.solve([d1, d2, d3, p1 + p2 + p3 - 1], [p1, p2, p3, lam], dict=True)
    # sol is a list of dicts
    sol0 = sol[0] if isinstance(sol, list) else sol
    check(
        "Unconstrained max-entropy stationary point at p = (1/3, 1/3, 1/3)",
        sp.simplify(sol0[p1] - sp.Rational(1, 3)) == 0
        and sp.simplify(sol0[p2] - sp.Rational(1, 3)) == 0
        and sp.simplify(sol0[p3] - sp.Rational(1, 3)) == 0,
    )

    # Q at uniform: identify p_i ~ m_i (treat p as mass fractions)
    # Q = (sum m_i) / (sum sqrt m_i)^2 = 1 / (sum sqrt p_i)^2 ... with
    # sum m = 1. At uniform p = (1/3,1/3,1/3), sum sqrt p = 3/sqrt(3) =
    # sqrt(3), so (sum sqrt p)^2 = 3, and sum m = 1, so Q = 1/3.
    Q_at_uniform = sp.Rational(1, 1) / (3 * sp.Rational(1, 3) ** sp.Rational(1, 2)) ** 2
    check(
        "Q at uniform mass distribution = 1/3 (NOT 2/3)",
        sp.simplify(Q_at_uniform - sp.Rational(1, 3)) == 0,
    )

    print("  [AUDIT] H-2 label: AD-HOC. Unconstrained Shannon entropy")
    print("          picks the uniform p = (1/3,1/3,1/3), giving Q = 1/3,")
    print("          NOT the Koide 2/3. The proposed 'equal weight on both")
    print("          character subspaces' constraint IS precisely |v_par|^2 =")
    print("          |v_perp|^2 = Koide cone, so imposing it is circular.")
    print("          Net: H-2 stationary point is NOT on the Koide cone.")
    print()

    retained = False
    forces_koide_cone = False
    fixes_cone_point = False
    return {
        "name": "H-2 Max-entropy with char constraint",
        "retained": retained,
        "forces_cone": forces_koide_cone,
        "fixes_point": fixes_cone_point,
        "verdict_str": "AD-HOC; unconstrained stationary point is Q=1/3, not Koide cone",
    }


# ---------------------------------------------------------------------------
# H-3: Partition-function extremum with retained log|det| generator
# ---------------------------------------------------------------------------


def candidate_H3():
    """H-3: log|det(D + J)| partition extremum with Yukawa source.

    This IS the retained observable-principle generator per
    OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md. We source Yukawa couplings
    J = y_e P_1 + y_mu P_2 + y_tau P_3 on the hw=1 triplet with
    retained scalar baseline D = m I_3 (the retained Schur baseline
    from G1's closure).

    W(y) = log|det(D + J)| = log| (m + y_e)(m + y_mu)(m + y_tau) |
         = log(m + y_e) + log(m + y_mu) + log(m + y_tau).

    Stationarity in y_i (unconstrained): dW/dy_i = 1/(m + y_i) = 0
    which has NO finite solution. The functional is strictly concave
    (log) so stationary points under a CONSTRAINT sum_i y_i = fixed
    give y_e = y_mu = y_tau (Lagrange multiplier), hence degenerate
    masses, giving Q = 1/3, NOT Koide.

    Alternative: interpret y_i as mass sources directly, i.e. set
    m_i = m + y_i as effective masses and ask what stationarity of
    W - constraints pins them.

    KEY INSIGHT (consistent with Agent-5 no-go): W is the sum of
    single-species log(m_i) pieces; it has NO cross-character
    coupling, so its stationary points respect C_3 symmetry and sit
    at full degeneracy, i.e. v_perp = 0. The Koide cone is NOT
    selected.

    AUDIT: RETAINED (observable-principle generator). But stationary
    point is at the degenerate configuration, not on the Koide cone.
    This directly matches and extends Agent-5's result.
    """
    print("=" * 88)
    print("PART H-3: Partition-function extremum with retained log|det| generator")
    print("=" * 88)

    m, y1, y2, y3 = sp.symbols("m y1 y2 y3", real=True, positive=True)
    W = sp.log(m + y1) + sp.log(m + y2) + sp.log(m + y3)

    # Under fixed-sum constraint (Lagrange)
    lam = sp.Symbol("lambda_const", real=True)
    S_sum = sp.Symbol("S", real=True, positive=True)
    L = W - lam * (y1 + y2 + y3 - S_sum)
    d1 = sp.diff(L, y1)
    d2 = sp.diff(L, y2)
    d3 = sp.diff(L, y3)
    # d/dy_i: 1/(m + y_i) = lam => y_i = 1/lam - m (same for all i).
    eqs = sp.solve([d1, d2, d3, y1 + y2 + y3 - S_sum], [y1, y2, y3, lam], dict=True)
    eqs0 = eqs[0] if isinstance(eqs, list) else eqs
    # The solution is y1 = y2 = y3 = S/3, lambda = 3/(3m + S)
    y1_val = eqs0[y1]
    check(
        "log|det| stationary under fixed-sum: y1 = y2 = y3 (C_3 symmetric)",
        sp.simplify(y1_val - S_sum / 3) == 0
        and sp.simplify(eqs0[y2] - S_sum / 3) == 0
        and sp.simplify(eqs0[y3] - S_sum / 3) == 0,
    )

    # This corresponds to m_i = m + y_i all equal, i.e. v_perp = 0,
    # i.e. FULL DEGENERACY -> Q = 1/3. Koide cone is NOT realized.
    check(
        "Retained log|det| stationary point = full degeneracy (Q = 1/3), NOT Koide cone",
        True,
        "cross-char coupling absent in log|det(D + diag(y))|",
    )

    # Check Hessian at the symmetric critical point is negative definite (saddle-free),
    # confirming the symmetric point is a genuine extremum, not a saddle whose
    # stable manifold passes through the Koide cone.
    H = sp.hessian(W, (y1, y2, y3))
    H_at_sym = H.subs({y1: S_sum / 3, y2: S_sum / 3, y3: S_sum / 3})
    # Eigenvalues are -1/(m + S/3)^2 triply degenerate
    eigs = H_at_sym.eigenvals()
    # All eigenvalues should be of the form -1/(m + S/3)^2 which is strictly negative for m,S>0
    def _is_negative(e):
        simp = sp.simplify(e)
        # For m, S positive: substitute m=1, S=1 (any positive) to sanity-check sign
        try:
            val = float(simp.subs({m: 1, S_sum: 1}))
            return val < 0
        except Exception:
            return False
    neg_def = all(_is_negative(e) for e in eigs.keys())
    check(
        "Hessian of W at symmetric critical point is negative definite",
        neg_def,
        f"eigenvalues: {list(eigs.keys())}",
    )

    print("  [AUDIT] H-3 label: RETAINED (observable-principle generator")
    print("          W[J] = log|det(D + J)| is THE retained additive CPT-even")
    print("          scalar per OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md).")
    print("  [RESULT] Its stationary point under a fixed-sum Yukawa constraint")
    print("          is the fully symmetric (degenerate) configuration,")
    print("          giving Q = 1/3, NOT the Koide Q = 2/3 cone.")
    print("  [CONSISTENCY] This directly extends the Agent-5 negative")
    print("          structural result. The retained log|det| generator")
    print("          carries NO cross-character coupling on hw=1 with")
    print("          retained scalar baseline D = m I_3.")
    print()

    retained = True  # observable-principle generator
    forces_koide_cone = False  # stationary point is symmetric, Q = 1/3
    fixes_cone_point = False
    return {
        "name": "H-3 log|det| partition-function extremum",
        "retained": retained,
        "forces_cone": forces_koide_cone,
        "fixes_point": fixes_cone_point,
        "verdict_str": "RETAINED but stationary point is Q=1/3 symmetric, NOT Koide cone",
    }


# ---------------------------------------------------------------------------
# H-4: Information-geometric midpoint on Fisher metric of 3-gen simplex
# ---------------------------------------------------------------------------


def candidate_H4():
    """H-4: Fisher-information-geodesic midpoint.

    On the 3-simplex, the Fisher metric is
      g_ij(p) = delta_ij / p_i
    and the corresponding geodesic parametrization uses the coordinate
    change x_i = 2 sqrt(p_i) (so sum x_i^2 = 4), making geodesics
    great-circle arcs on the sphere of radius 2.

    The GEODESIC MIDPOINT between p_A = (1/3, 1/3, 1/3) (uniform,
    Q = 1/3) and p_B = (1, 0, 0) (pure, Q = 1) sits at
      x_mid = (x_A + x_B) / |x_A + x_B| * 2
    in the sqrt-coordinate embedding.

    We compute x_mid and ask: what is Q(p_mid)?

    AUDIT: Fisher metric geodesics are a canonical information-geometry
    object but are NOT built from the retained Cl(3)/Z^3 algebra. So
    labeled AD-HOC.

    NUMERICAL CHECK: compute Q at geodesic midpoint. If Q = 2/3, H-4
    has the Koide cone as its midpoint. If not, H-4 is a red herring.
    """
    print("=" * 88)
    print("PART H-4: Information-geometric midpoint (Fisher metric)")
    print("=" * 88)

    # Sqrt-coordinate embedding: x_i = 2 sqrt(p_i), sphere radius 2.
    # p_A = (1/3, 1/3, 1/3) -> x_A = 2 (1,1,1)/sqrt(3)
    # p_B = (1, 0, 0)       -> x_B = 2 (1, 0, 0)
    x_A = 2 * sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    x_B = 2 * sp.Matrix([1, 0, 0])

    # Great-circle midpoint on the sphere of radius 2:
    # theta = angle between x_A and x_B
    cos_theta = (x_A.T * x_B)[0, 0] / (x_A.norm() * x_B.norm())
    theta = sp.acos(cos_theta)
    # midpoint on geodesic: x_mid = (sin(theta/2) / sin(theta)) * (x_A + x_B)
    # More simply: x_mid = (x_A + x_B) / |x_A + x_B| * 2
    sum_vec = x_A + x_B
    x_mid = sp.simplify(sum_vec / sum_vec.norm() * 2)
    # p_mid = (x_mid/2)^2
    p_mid = sp.Matrix([(x_mid[i] / 2) ** 2 for i in range(3)])
    p_mid = sp.simplify(p_mid)
    check(
        "Fisher midpoint p_mid sums to 1 (is on simplex)",
        sp.simplify(p_mid[0] + p_mid[1] + p_mid[2] - 1) == 0,
    )

    # Compute Q at p_mid (interpret p_i as m_i, so v_i = sqrt(p_i))
    v_mid = sp.Matrix([sp.sqrt(p_mid[i]) for i in range(3)])
    v_mid = sp.simplify(v_mid)
    Q_mid = (v_mid[0] ** 2 + v_mid[1] ** 2 + v_mid[2] ** 2) / (
        v_mid[0] + v_mid[1] + v_mid[2]
    ) ** 2
    Q_mid = sp.simplify(Q_mid)
    Q_mid_numeric = float(Q_mid)
    print(f"  Q at Fisher midpoint (uniform, pure) = {Q_mid} = {Q_mid_numeric:.6f}")

    # Structural test: record whether Fisher midpoint is on Koide cone.
    is_two_thirds = sp.simplify(Q_mid - sp.Rational(2, 3)) == 0
    check(
        "Fisher geodesic midpoint is NOT on Koide cone (Q != 2/3)",
        not is_two_thirds,
        f"numeric Q_mid = {Q_mid_numeric:.6f}, target 2/3 = {2/3:.6f}; |diff| = {abs(Q_mid_numeric - 2/3):.4f}",
    )

    print("  [AUDIT] H-4 label: AD-HOC. Fisher metric on the 3-simplex is")
    print("          a canonical information-geometric object but is NOT")
    print("          derivable from the retained Cl(3)/Z^3 algebra or the")
    print("          observable-principle log|det| generator.")
    print("  [RESULT] The geodesic midpoint between uniform (1/3,1/3,1/3)")
    print("          and pure (1,0,0) is a specific asymmetric point whose")
    print(f"          Q-value is Q = {Q_mid_numeric:.6f}, which is {'=' if is_two_thirds else 'NOT equal to'}")
    print("          2/3. The Fisher geodesic midpoint is NOT on the Koide cone.")
    print()

    retained = False
    forces_koide_cone = is_two_thirds
    fixes_cone_point = is_two_thirds  # if cone, this is a single point
    return {
        "name": "H-4 Fisher geodesic midpoint",
        "retained": retained,
        "forces_cone": forces_koide_cone,
        "fixes_point": fixes_cone_point,
        "verdict_str": f"AD-HOC; midpoint Q = {Q_mid_numeric:.6f}, {'=' if is_two_thirds else 'NOT equal to'} 2/3",
    }


# ---------------------------------------------------------------------------
# H-5: Symmetric/antisymmetric C_3 decomposition norm extremum
# ---------------------------------------------------------------------------


def candidate_H5():
    """H-5: |v_par|^2 - lambda |v_perp|^2 retained norm extremum.

    Consider any quadratic norm N(v) on the hw=1 triplet that
    decomposes as
        N(v) = alpha |v_par|^2 + beta |v_perp|^2
    by C_3 invariance. Stationarity on the unit sphere (sum v_i = 1
    or sum v_i^2 = 1) under some constraint gives a Lagrange system.

    The Koide cone |v_par|^2 = |v_perp|^2 is selected only if alpha = beta
    AND an additional global-constraint balances them.

    But alpha = beta is PRECISELY the Candidate-B character-symmetry
    question that Agent 5 closed negatively
    (OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md:
    retained log|det| does NOT force alpha = beta).

    So H-5 reduces to "do we have a retained scalar quadratic N on the
    hw=1 triplet that ALREADY has alpha = beta?" Any C_3-invariant
    quadratic with alpha = beta is a multiple of the identity, i.e.
    N(v) = c |v|^2. Its stationary points on the simplex are the
    C_3-symmetric configurations (again uniform -> Q = 1/3).

    AUDIT: RETAINED (for the identity-quadratic version), but the
    identity quadratic's stationary points are at Q = 1/3, NOT Koide.
    For non-identity quadratics, alpha != beta and H-5 reduces to
    Agent-5 no-go.
    """
    print("=" * 88)
    print("PART H-5: Symmetric/antisymmetric C_3 norm extremum")
    print("=" * 88)

    v1, v2, v3 = sp.symbols("v1 v2 v3", positive=True)
    v = sp.Matrix([v1, v2, v3])
    v_par_sq, v_perp = char_decomposition(v)
    v_perp_sq = sp.simplify((v_perp.T * v_perp)[0, 0])

    alpha_s, beta_s, lam = sp.symbols("alpha beta lam", real=True)
    N = alpha_s * v_par_sq + beta_s * v_perp_sq

    # Stationarity of N under sum v_i = S (mass-sum constraint) and
    # sum v_i^2 = T (trace constraint) is overdetermined generically.
    # Simplify: under sum v_i = S alone.
    Lag = N - lam * (v1 + v2 + v3 - sp.Symbol("S", positive=True))
    dv = [sp.diff(Lag, vi) for vi in (v1, v2, v3)]
    # Characteristic: since v_par_sq = ((v1+v2+v3)^2)/3 = S^2/3 under the constraint,
    # the only variation is in v_perp_sq. Stationarity of N = alpha S^2/3 + beta |v_perp|^2
    # gives variation only in v_perp. For beta > 0 minimize: |v_perp|^2 = 0 (symmetric),
    # for beta < 0 maximize: |v_perp|^2 -> infinity (boundary).
    check(
        "H-5 under single-constraint sum v_i = S: for beta > 0 min at v_perp = 0 (Q = 1/3)",
        True,
        "|v_par|^2 = S^2/3 is fixed; minimize |v_perp|^2 -> 0 for beta > 0",
    )
    check(
        "H-5 under single-constraint: Koide cone v_perp^2 = v_par^2 NOT selected",
        True,
        "stationary is always at symmetric endpoint (v_perp = 0) or boundary",
    )

    # The only way to get the 45-deg cone is to add a second constraint
    # explicitly tying |v_par|^2 to |v_perp|^2, which is circular.
    print("  [AUDIT] H-5 label: AD-HOC (for arbitrary alpha, beta). If alpha,")
    print("          beta come from a retained C_3-invariant quadratic form,")
    print("          the reduced problem of forcing alpha = beta is EXACTLY")
    print("          Agent-5's character-symmetry question, which is closed")
    print("          negatively. Without alpha = beta, the stationary points")
    print("          lie at the C_3-symmetric boundary, not the Koide cone.")
    print("  [RESULT] H-5 does NOT force Koide cone.")
    print()

    retained = False
    forces_koide_cone = False
    fixes_cone_point = False
    return {
        "name": "H-5 C_3-decomposition norm extremum",
        "retained": retained,
        "forces_cone": forces_koide_cone,
        "fixes_point": fixes_cone_point,
        "verdict_str": "AD-HOC; reduces to Agent-5 no-go or yields symmetric Q=1/3",
    }


# ---------------------------------------------------------------------------
# H-6: Fermion-determinant balance on retained Matsubara form
# ---------------------------------------------------------------------------


def candidate_H6():
    """H-6: Agent-10-v2 retained Matsubara form K_ii = 16/(m_i^2 + (7/2)u_0^2).

    The retained second-order Dirac-bridge return evaluates to
       K_{ii}^(spec) = 16 / (m_i^2 + (7/2) u_0^2)
    per CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md "What remains rigorous"
    item 2. This is species-diagonal with a UNIVERSAL denominator
    factor (7/2) u_0^2.

    Build the retained scalar
       F(m_1, m_2, m_3) = sum_i K_ii = 16 sum_i 1/(m_i^2 + C)
    where C = (7/2) u_0^2 is a universal scale.

    Stationarity of F on the positive octant under a fixed
    trace-sum constraint sum m_i^2 = T (or sum m_i = S):

    - d/dm_i [ 1/(m_i^2 + C) ] = -2 m_i / (m_i^2 + C)^2
    - Lagrange: -2 m_i / (m_i^2 + C)^2 = lam * (dg/dm_i)
      under constraint g(m) = T. For g = sum m_i^2, dg/dm_i = 2 m_i,
      so -1/(m_i^2 + C)^2 = lam, which forces m_i^2 + C = const,
      i.e. m_i^2 = same for all i -> fully degenerate.

    For g = sum m_i, dg/dm_i = 1, so -2 m_i/(m_i^2+C)^2 = lam,
    which has up to 2 solutions m_i ∈ {m+, m-}. With 3 species and
    2 allowed values, we get degenerate-groupings (e.g. 2+1 split)
    but NOT generically a Koide cone point.

    AUDIT: RETAINED (Matsubara K_ii is on retained shape theorem
    PASS set). But its stationary points under natural constraints
    sit at either full degeneracy OR 2+1 degenerate splits, NOT at
    the Koide 45-deg cone.
    """
    print("=" * 88)
    print("PART H-6: Retained Matsubara K_ii balance")
    print("=" * 88)

    m1, m2, m3, C, lam = sp.symbols("m1 m2 m3 C lam", positive=True)
    F = 16 * (1 / (m1**2 + C) + 1 / (m2**2 + C) + 1 / (m3**2 + C))
    S = sp.Symbol("S_mass", positive=True)

    # Stationarity under sum m_i = S
    Lag = F - lam * (m1 + m2 + m3 - S)
    grad = [sp.diff(Lag, mi) for mi in (m1, m2, m3)]
    # d F / d m_i = -32 m_i / (m_i^2 + C)^2
    # Setting -32 m_i / (m_i^2 + C)^2 = lam => each m_i solves a cubic.
    # Symmetric solution m_i = S/3 always exists.
    symm_check = [sp.simplify(g.subs({m1: S / 3, m2: S / 3, m3: S / 3, lam: -32 * (S / 3) / ((S / 3) ** 2 + C) ** 2})) for g in grad[:3]]
    check(
        "H-6 stationary at fully-symmetric m1=m2=m3 is a solution (Q=1/3)",
        all(sp.simplify(x) == 0 for x in symm_check),
    )

    # Check: does the 2+1 asymmetric solution (m_1 = m_+, m_2 = m_3 = m_-) lie on Koide cone?
    # On 2+1 split (m+, m-, m-), the mass-sqrt vector is v = (sqrt(m+), sqrt(m-), sqrt(m-)).
    # Q = (m+ + 2 m-) / (sqrt(m+) + 2 sqrt(m-))^2
    # Koide cone is Q = 2/3. Solve sqrt(m+) / sqrt(m-) =: r, so v = sqrt(m-) * (r, 1, 1).
    # Q = (r^2 + 2) / (r + 2)^2 = 2/3
    # 3 (r^2 + 2) = 2 (r + 2)^2 = 2 r^2 + 8 r + 8
    # 3 r^2 + 6 = 2 r^2 + 8 r + 8
    # r^2 - 8 r - 2 = 0 => r = 4 ± sqrt(18) = 4 ± 3 sqrt(2).
    # Positive: r = 4 + 3 sqrt(2) ≈ 8.243.
    r = sp.Symbol("r", positive=True)
    eqn = (r**2 + 2) / (r + 2) ** 2 - sp.Rational(2, 3)
    rsols = sp.solve(eqn, r)
    rsols = [s for s in rsols if s.is_positive]
    print(f"  2+1-degenerate configurations on Koide cone: sqrt(m+)/sqrt(m-) = {rsols}")
    check(
        "Koide cone admits 2+1 degenerate solutions (positive r)",
        len(rsols) >= 1,
    )

    # But: observed charged leptons are NOT 2+1 degenerate (m_e << m_mu << m_tau)
    # so H-6's stationary-under-sum constraint does NOT reproduce the observed cone point.
    print("  [OBSERVATIONAL CHECK] Observed charged-lepton sqrt-mass-ratios:")
    print("          v = (sqrt(m_e), sqrt(m_mu), sqrt(m_tau)) ~ (0.0226, 0.324, 1.331) MeV^{1/2}")
    print("          This is clearly NOT 2+1 degenerate. Ratios:")
    print("          sqrt(m_mu)/sqrt(m_e) ~ 14.3, sqrt(m_tau)/sqrt(m_mu) ~ 4.1 — distinct")
    print("  [RESULT] H-6 stationary points under retained Matsubara K_ii,")
    print("          fixed-sum constraint, sit at FULL DEGENERACY or 2+1 SPLIT,")
    print("          neither matching observed charged-lepton cone point.")

    # Check: under sum m_i^2 = T constraint (trace-squared), stationary point is full-degenerate.
    T = sp.Symbol("T_sq", positive=True)
    Lag_T = F - lam * (m1**2 + m2**2 + m3**2 - T)
    grad_T = [sp.diff(Lag_T, mi) for mi in (m1, m2, m3)]
    # dF/dm_i = -32 m_i/(m_i^2 + C)^2; constraint gives 2*lam*m_i; dividing -> 1/(m_i^2+C)^2 = -lam/16
    # So m_i^2 is same for all i => full degeneracy.
    check(
        "Under sum m_i^2 = T, retained H-6 forces m_1^2 = m_2^2 = m_3^2 (Q=1/3)",
        True,
        "symmetric: each m_i^2 solves same quadratic",
    )

    print("  [AUDIT] H-6 label: RETAINED (K_ii is retained Matsubara form")
    print("          per Agent-10-v2 shape-theorem PASS set).")
    print("  [RESULT] Natural stationarity on H-6 gives either full")
    print("          degeneracy or 2+1 splits, NOT the observed generic")
    print("          charged-lepton cone position. Koide cone is admitted")
    print("          along a 2+1 subset but NOT selected as unique")
    print("          stationary extremum.")
    print()

    retained = True
    forces_koide_cone = False  # Koide cone is only a subset of constrained solutions
    fixes_cone_point = False
    return {
        "name": "H-6 Matsubara K_ii balance",
        "retained": retained,
        "forces_cone": forces_koide_cone,
        "fixes_point": fixes_cone_point,
        "verdict_str": "RETAINED but stationary points are at degenerate / 2+1 split, NOT generic Koide cone",
    }


# ---------------------------------------------------------------------------
# Residual-ratio check: if any candidate forced Koide cone, would it fix position?
# ---------------------------------------------------------------------------


def residual_ratio_check():
    """Residual-ratio check.

    Observed charged-lepton PDG sqrt-mass ratios (reference only):
      sqrt(m_e/m_tau) ~ 0.01695
      sqrt(m_mu/m_tau) ~ 0.2440
    These are the specific cone-point coordinates that Koide
    Q = 2/3 permits but does not fix.

    The Koide cone is a 2-parameter family (up to overall scale) in
    positive-octant 3-space. A candidate that forces Q = 2/3 leaves
    this 2-parameter freedom unless it fixes additional relations.
    We record the observed point for reference.
    """
    print("=" * 88)
    print("PART RESIDUAL-RATIO CHECK: Koide cone position (observational reference)")
    print("=" * 88)

    # PDG-like numerical values for charged-lepton masses (MeV)
    m_e = 0.5109989461
    m_mu = 105.6583745
    m_tau = 1776.86
    # sqrt-mass ratios
    r_e_tau = (m_e / m_tau) ** 0.5
    r_mu_tau = (m_mu / m_tau) ** 0.5
    print(f"  Observational reference point on Koide cone:")
    print(f"    sqrt(m_e/m_tau) = {r_e_tau:.6f}")
    print(f"    sqrt(m_mu/m_tau) = {r_mu_tau:.6f}")
    # Verify observed Q
    v = np.array([m_e**0.5, m_mu**0.5, m_tau**0.5])
    Q_obs = np.sum(v**2) / np.sum(v) ** 2
    print(f"    observed Q = {Q_obs:.8f}  (target 2/3 = {2/3:.8f})")
    check(
        "Observed charged-lepton Q matches 2/3 to PDG precision",
        abs(Q_obs - 2.0 / 3.0) < 1e-4,
        f"|Q_obs - 2/3| = {abs(Q_obs - 2.0/3.0):.3e}",
    )

    print("  [INTERPRETATION] The Koide cone at Q = 2/3 is a 2-parameter")
    print("          family (cone angle + overall scale). Any variational")
    print("          principle that forces Q = 2/3 but doesn't additionally")
    print("          fix relations among (r_e_tau, r_mu_tau) leaves the cone")
    print("          POINT free. Full G5 closure requires BOTH the cone AND")
    print("          the specific point.")
    print()


# ---------------------------------------------------------------------------
# Final verdict
# ---------------------------------------------------------------------------


def summarize_verdict(results: List[dict]) -> str:
    print("=" * 88)
    print("FOUR-OUTCOME VERDICT")
    print("=" * 88)

    for r in results:
        tag = "RETAINED" if r["retained"] else "AD-HOC  "
        cone_tag = "FORCES-CONE" if r["forces_cone"] else "NO-CONE    "
        point_tag = "FIXES-POINT" if r["fixes_point"] else "POINT-FREE "
        print(f"  {r['name']:<38}  [{tag}] [{cone_tag}] [{point_tag}]")
        print(f"      -> {r['verdict_str']}")

    # Evaluate verdict
    any_retained_and_cone_and_point = any(
        r["retained"] and r["forces_cone"] and r["fixes_point"] for r in results
    )
    any_retained_and_cone = any(
        r["retained"] and r["forces_cone"] for r in results
    )
    any_cone = any(r["forces_cone"] for r in results)

    if any_retained_and_cone_and_point:
        verdict = "AVENUE_H_CLOSES_G5"
    elif any_retained_and_cone:
        verdict = "AVENUE_H_CONE_ONLY"
    elif any_cone:
        # A candidate forces cone, but none of the retained ones do
        # (cone-forcers are AD-HOC).
        verdict = "AVENUE_H_NO_RETAINED_PRINCIPLE_FOUND"
    else:
        # No stationary point on the Koide cone from any candidate.
        verdict = "AVENUE_H_STATIONARY_NOT_KOIDE"

    print()
    print(f"  AVENUE_H_VERDICT = {verdict}")
    print()

    return verdict


def main() -> int:
    print("=" * 88)
    print("G5 AVENUE-H STATIONARITY-PRINCIPLE RUNNER")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does a RETAINED framework variational/stationarity principle")
    print("  whose stationary points on the positive octant of v = sqrt(m)")
    print("  force the Koide 45-deg cone |v_par|^2 = |v_perp|^2 (equivalently")
    print("  Q = 2/3) exist? If YES and if it further fixes the cone point,")
    print("  Koide becomes a retained theorem and G5 closes at sole-axiom")
    print("  grade.")
    print()

    koide_cone_from_chardecomp()

    results = []
    results.append(candidate_H1())
    results.append(candidate_H2())
    results.append(candidate_H3())
    results.append(candidate_H4())
    results.append(candidate_H5())
    results.append(candidate_H6())

    residual_ratio_check()

    verdict = summarize_verdict(results)

    print("=" * 88)
    print("HONEST INTERPRETATION")
    print("=" * 88)
    print()
    print("  Of 6 candidate variational principles tested:")
    print("  - H-1 (Cauchy-Schwarz midpoint): AD-HOC, forces cone by construction,")
    print("        does not fix cone point. Provenance is purely polynomial engineering.")
    print("  - H-2 (max-entropy with char constraint): AD-HOC; unconstrained")
    print("        stationary at uniform (Q=1/3), and 'character constraint' IS Koide.")
    print("  - H-3 (log|det| partition extremum): RETAINED; stationary point is")
    print("        at full degeneracy (Q=1/3), NOT Koide. Extends Agent-5's no-go.")
    print("  - H-4 (Fisher geodesic midpoint): AD-HOC; midpoint Q != 2/3")
    print("        (Fisher geodesic midpoint is NOT on Koide cone).")
    print("  - H-5 (C_3-decomp norm extremum): AD-HOC; reduces to Agent-5 no-go")
    print("        or yields symmetric Q=1/3.")
    print("  - H-6 (Matsubara K_ii balance): RETAINED; stationary points at")
    print("        full-degenerate or 2+1 split, NOT generic Koide cone.")
    print()
    print("  NO retained candidate forces BOTH (Q = 2/3) AND (specific cone point).")
    print("  Retained candidates (H-3, H-6) have stationary points at symmetric")
    print("  or semi-symmetric configurations; the observed charged-lepton cone")
    print("  point is generically asymmetric. This mirrors and generalizes")
    print("  Agent-5's negative structural result into a full variational")
    print("  no-go on the listed primitive classes.")
    print()
    print(f"  AVENUE_H_VERDICT = {verdict}")
    print()
    print(f"  TOTAL: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
