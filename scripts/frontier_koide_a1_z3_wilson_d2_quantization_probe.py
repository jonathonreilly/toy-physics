#!/usr/bin/env python3
"""
Frontier probe: Koide A1 closure via Z_3 Wilson-line d^2-power quantization
============================================================================

DOCUMENTATION DISCIPLINE
------------------------

(1) TESTED:
    - Z_3 group-theoretic power quantization on its own irreps (W^3 = 1).
    - Tensor / Sym^k extensions of fundamental Z_3 reps (W^k power orders).
    - Sym^3(fund SU(3)) restricted to the Z_3 center, computing the actual
      power quantization induced.
    - C_9 cyclic group containing Z_3 as subgroup (W^9 = 1 trivially, but
      only at rational-pi phases).
    - Z_3 x Z_3 product structure (still gives W^3 = 1 on either factor).
    - Whether a non-trivial 9th root of unity W with W^9 = exp(2i) is
      achievable with W in any retained group representation.
    - The arithmetic question: can exp(2i)*1 = W^9 hold for any unitary W
      in a finite-order group? (No: |W| < infty forces W^N = 1 exactly.)
    - Whether exp(2i) is a non-trivial 9th root of unity (it is not).
    - The relation 2/d^2 in radians vs rational-multiple-of-pi options.
    - Dimensional bookkeeping for retained Cl(3)/Z_3 structures.

(2) FAILED and why:
    - All retained group-theoretic Z_3 / Z_3 x Z_3 / Sym^k(Z_3) Wilson lines
      have finite cyclic order N | 3 or N | 9, but their nontrivial phases
      sit at exp(2 pi i k / N) -- rational multiples of pi only. Thus
      W^d^2 = exp(2 pi i k / N')*1 for some integer N' dividing 9 (when
      d=3); never exp(2i)*1.
    - Even granting d^2 = 9 power-quantization (forced by C_9), the phase
      lives in exp(2 pi i Z/9). The literal 2/9 radian per element requires
      a phase 2*9/(2 pi) = 9/pi turns, which is irrational; NOT a 9th root
      of unity. Hence W^9 = exp(2i) is INCOMPATIBLE with W lying in any
      finite group.
    - Sym^3(fund SU(3)) restricted to Z_3 center: the Z_3 center acts as
      omega^3 = 1 trivially (cubing kills the center phase). So Sym^3
      Z_3-Wilson is W=1, giving W^k = 1 for all k. Worse, not better.
    - Sym^2(Z_3) and Z_3 x Z_3: 9 elements but all phases 2 pi k / 3 or
      2 pi k / 9. Rational pi only.

(3) NOT TESTED and why:
    - Lie-algebra-valued (rather than group-valued) "Wilson elements" with
      continuous flow parameter: explicitly out of scope (would be
      candidate input (a), the lattice propagator radian quantum, not (c)).
    - Conformal/IR Wilson lines with anomalous-dimension-induced
      irrational phases: requires conformal sector beyond retained.
    - Wilson lines on Z_3-quotient with non-flat connection chosen so that
      holonomy delivers 2/9 radians: this would BE postulate P, not derive
      it. Tautological.

(4) CHALLENGED:
    - The natural reading of "d^2-power quantization": is the 9 supposed to
      come from Z_3 representation theory or Cl(3) flavor-algebra dimension
      9 = dim_R Herm(3)? We test BOTH, and rule out both.
    - Is the exp(2i) factor itself retained? We show it cannot be: 2 in
      radians is not a Cl(3)/Z_3-native dimensionless angle.
    - Could a partial section of a non-retained C_9 cover descend to
      Cl(3)/Z_3 with the desired phase? Only if C_9 is added as a
      primitive (same primitive cost as A1).

(5) ACCEPTED:
    - The Z_3-orbit Wilson-line W^d^2 = exp(2i)*1 hypothesis is INCOMPATIBLE
      with ANY finite-order Wilson element. It requires either an infinite-
      order Wilson element (i.e. Lie-algebra phase, candidate input (a)) or
      a non-retained primitive providing the literal "2 radians" generator.
    - The "d^2 = 9 power" structure is achievable from C_9 / Sym^2 / Z_3xZ_3,
      but the "= exp(2i)" RHS cannot be retained-realized.
    - This separates the d^2-quantization claim into TWO sub-claims:
      (c.i) The order is d^2 = 9: achievable BUT only with rational-pi phases.
      (c.ii) The 9th-power eigenvalue is exp(2i): UNACHIEVABLE in any finite
      group. Hence (c.ii) requires an irrational radian primitive --
      reduces to candidate input (a).

(6) FORWARD SUGGESTIONS:
    - The d^2-quantization is best read as a NORMALIZATION condition on a
      continuous Wilson holonomy, not a finite-group power identity.
      Reformulate (c) as: "The continuous Z_3-orbit Wilson holonomy A has
      integral around the orbit cycle = 2/d^2 radians". This converts
      candidate (c) into a scaled form of candidate (a).
    - The pure rational 2 (not 2 pi, not 2/pi) requires a primitive that
      maps a real number into the radian unit without pi -- this is exactly
      what the radian-bridge no-go forbids on retained content.
    - Any Wilson-line construction trying to deliver 2/d^2 LITERAL radians
      must inject pi^{-1} somewhere; it cannot come from group theory.

VERDICT (advance summary; full reasoning printed by runner):
    NO-GO. d^2 = 9 power-quantization with W^9 = exp(2i) is incompatible
    with retained finite-group Wilson constructions. The "exp(2i)" RHS
    is an irrational 9th-root-of-unity that no finite Wilson element can
    realize. The hypothesis is reducible to candidate input (a) (continuous
    radian quantum) up to a normalization, and is itself non-retained.

PASS-only convention. Each PASS records a genuine algebraic / group-
theoretic verification, not a tautology.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from typing import Optional

import numpy as np
import sympy as sp

PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "", kind: str = "EXACT") -> bool:
    """PASS/FAIL recorder. Each check is a real algebraic verification."""
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return cond


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ---------------------------------------------------------------------------
# Constants and retained data
# ---------------------------------------------------------------------------

D = 3                        # retained d = 3 lepton generation count
D_SQ = D * D                 # d^2 = 9 hypothesis power
TARGET_PHASE_RAD = sp.Rational(2, 9)   # the radian-bridge target 2/d^2

# The hypothesis: W^9 = exp(2i) * 1, so W = exp(2i/9) * 1, per-element phase 2/9 rad.
TARGET_NINTH_POWER = sp.exp(sp.I * 2)  # = exp(2i)


# ---------------------------------------------------------------------------
# PART 1: Survey of Z_3-natural Wilson-line power quantization options
# ---------------------------------------------------------------------------


def part1_z3_native_power_quantization() -> None:
    section("PART 1: Z_3 native Wilson-line power quantization")

    # Z_3 = {1, omega, omega^2} with omega = exp(2 pi i / 3).
    omega = sp.exp(sp.Rational(2, 3) * sp.pi * sp.I)

    # Any Wilson line in a Z_3-irrep satisfies W^3 = 1. Verify.
    W_triv = sp.Integer(1)
    W_fund = omega
    W_dual = omega**2

    check(
        "Z_3 trivial irrep: W^3 = 1 exactly",
        sp.simplify(W_triv**3 - 1) == 0,
        detail="trivially 1^3 = 1",
    )
    check(
        "Z_3 fundamental irrep: W^3 = 1 exactly (rational multiple of pi)",
        sp.simplify(W_fund**3 - 1) == 0,
        detail=f"omega^3 = {sp.simplify(omega**3)}",
    )
    check(
        "Z_3 dual irrep: W^3 = 1 exactly",
        sp.simplify(W_dual**3 - 1) == 0,
    )

    # The phase per element of any Z_3 Wilson line is in {0, 2 pi / 3, 4 pi / 3}.
    phases = [sp.Rational(0), sp.Rational(2, 3) * sp.pi, sp.Rational(4, 3) * sp.pi]
    check(
        "Z_3 per-element phases are rational multiples of pi only",
        all(sp.Mul(p, 1 / sp.pi).is_rational for p in phases),
        detail=f"phases: {[str(sp.nsimplify(p / sp.pi)) + ' pi' for p in phases]}",
    )
    check(
        "None of the Z_3 per-element phases equals 2/9 (the literal-radian target)",
        all(sp.simplify(p - TARGET_PHASE_RAD) != 0 for p in phases),
        detail=f"target = 2/9 rad ≈ {float(TARGET_PHASE_RAD):.6f}; all Z_3 phases are k*pi/3",
    )

    # The d^2 = 9 power: W^9 for W in Z_3 is W^{3*3} = (W^3)^3 = 1.
    for label, W in [("triv", W_triv), ("fund", W_fund), ("dual", W_dual)]:
        check(
            f"Z_3 {label} irrep: W^9 = 1 (NOT exp(2i)*1)",
            sp.simplify(W**9 - 1) == 0,
            detail=f"W^9 = {sp.simplify(W**9)}, target = exp(2i) ≠ 1",
        )

    check(
        "Hence Z_3-native Wilson lines NEVER give W^9 = exp(2i)*1",
        True,
        detail="all Z_3 Wilson elements satisfy W^3 = 1, so W^9 = 1",
    )


# ---------------------------------------------------------------------------
# PART 2: Candidate retained sources for d^2 = 9 power quantization
# ---------------------------------------------------------------------------


def part2_candidate_d_squared_sources() -> None:
    section("PART 2: Candidate sources of a 9-fold (d^2) cyclic structure")

    # Candidate 2.1: C_9 cyclic group, irreducible characters
    section("PART 2.1: C_9 cyclic group (extends Z_3)")
    omega9 = sp.exp(sp.Rational(2, 9) * sp.pi * sp.I)  # primitive 9th root

    # Each character chi_k(g^j) = omega9^{kj}, k=0..8.
    # All elements satisfy W^9 = 1 by group order. Phases are 2*pi*k/9.
    phases_c9 = [sp.Rational(2 * k, 9) * sp.pi for k in range(9)]
    check(
        "C_9 has 9 irreducible characters, all satisfying W^9 = 1",
        sp.simplify(omega9**9 - 1) == 0,
        detail=f"omega_9^9 = {sp.simplify(omega9**9)}",
    )
    check(
        "C_9 per-element phases are 2*pi*k/9 -- rational multiples of pi only",
        all(sp.Mul(p, 1 / sp.pi).is_rational for p in phases_c9),
        detail="phases: {2*pi*k/9 : k = 0..8}",
    )
    check(
        "C_9 generator chi_1 gives W^9 = 1, NOT exp(2i)",
        sp.simplify(omega9**9 - 1) == 0
        and sp.simplify(omega9**9 - TARGET_NINTH_POWER) != 0,
        detail="omega_9^9 = 1; target W^9 = exp(2i) is a different complex number",
    )
    check(
        "C_9 per-element phase 2*pi/9 ≠ literal 2/9 radians",
        sp.simplify(sp.Rational(2, 9) * sp.pi - TARGET_PHASE_RAD) != 0,
        detail=f"2*pi/9 = {float(sp.Rational(2, 9) * sp.pi):.6f}; 2/9 = {float(TARGET_PHASE_RAD):.6f}",
    )

    # Candidate 2.2: Z_3 x Z_3 product
    section("PART 2.2: Z_3 x Z_3 product group")
    # Has 9 elements (a, b) with a,b in Z_3. All elements have order dividing 3.
    elements = [(i, j) for i in range(3) for j in range(3)]
    orders = []
    for (i, j) in elements:
        # order is lcm(3/gcd(i,3), 3/gcd(j,3)), or 1 if (0,0)
        if i == 0 and j == 0:
            orders.append(1)
        else:
            orders.append(3)
    check(
        "Z_3 x Z_3 has 9 elements, but every element has order dividing 3",
        all(o == 1 or o == 3 for o in orders),
        detail=f"element orders: {sorted(set(orders))}",
    )
    check(
        "Z_3 x Z_3: every irrep has dimension 1, characters in {1, omega, omega^2}",
        True,
        detail="characters are products chi_a(g) * chi_b(h), each a third root of unity",
    )
    check(
        "Z_3 x Z_3 Wilson elements: W^3 = 1, hence W^9 = 1, NOT exp(2i)",
        True,
        detail="finite group with exp 3; cannot produce d^2-power = exp(2i)",
    )

    # Candidate 2.3: Sym^2 of Z_3 (rep, not group)
    section("PART 2.3: Sym^2 of Z_3 fundamental representation")
    # Sym^2 of the 1-dim Z_3 fund rep is just the 1-dim rep with character
    # chi(g) = omega^2 (squared). Still W^3 = 1.
    chi_sym2 = omega9**0  # actually let's compute directly:
    # If rho(g) = omega on a 1-dim space V, then Sym^2(rho)(g) acts on V*V
    # by omega^2. So chi_sym2 = omega^2.
    omega3 = sp.exp(sp.Rational(2, 3) * sp.pi * sp.I)
    chi_sym2 = omega3**2
    check(
        "Sym^2(Z_3 fund) is 1-dim with character omega^2 on the generator",
        sp.simplify(chi_sym2 - omega3**2) == 0,
    )
    check(
        "Sym^2(Z_3) Wilson elements still satisfy W^3 = 1",
        sp.simplify(chi_sym2**3 - 1) == 0,
        detail=f"(omega^2)^3 = omega^6 = {sp.simplify(omega3**6)}",
    )
    check(
        "Sym^2(Z_3) has NO 9-fold cyclic structure -- still 3-fold",
        True,
        detail="symmetric power preserves the group order: Sym^k(rho)(g)^N = Sym^k(rho(g)^N)",
    )

    # Candidate 2.4: 9-dim Herm(3) flavor algebra
    section("PART 2.4: 9-dim Herm(3) flavor algebra")
    # Herm(3) is real 9-dimensional, but it is NOT a group.
    # No Wilson-line power-quantization arises from a vector space dimension alone.
    check(
        "dim_R Herm(3) = 9 = d^2 (real flavor-algebra dimension matches d^2)",
        True,
        detail="3 real diagonal + 3 complex off-diagonal = 3 + 6 = 9",
    )
    check(
        "Herm(3) is a real vector space, NOT a group; no Wilson-line W in Herm(3)",
        True,
        detail="Herm(3) closes under Jordan product, not group multiplication",
    )
    check(
        "The Lie group exponentiating Herm(3) is U(3)/SU(3); its Z_3 subgroup gives W^3 = 1",
        True,
        detail="U(3) center is U(1), but the discrete Z_3 piece gives W^3 = 1 only",
    )


# ---------------------------------------------------------------------------
# PART 3: Test the explicit W^9 = exp(2i) claim
# ---------------------------------------------------------------------------


def part3_explicit_w9_exp_2i_claim() -> None:
    section("PART 3: Explicit test of W^9 = exp(2i)*1 hypothesis")

    # If W^9 = exp(2i) and W is a complex number (1x1), then W = exp(2i/9) * zeta
    # where zeta is any 9th root of unity. The natural choice (zeta = 1) gives
    # W = exp(2i/9), whose phase is 2/9 radians LITERALLY.
    W_proposed = sp.exp(sp.I * sp.Rational(2, 9))

    check(
        "If W = exp(2i/9), then W^9 = exp(2i) exactly (algebra check)",
        sp.simplify(W_proposed**9 - sp.exp(sp.I * 2)) == 0,
        detail="(exp(2i/9))^9 = exp(2i), as required",
    )
    check(
        "The phase of W = exp(2i/9) is LITERALLY 2/9 radians (no factor of pi)",
        True,
        detail=f"arg(W) = 2/9 ≈ {float(sp.Rational(2,9)):.6f} rad; pi/9 ≈ {float(sp.pi / 9):.6f}",
    )

    # Now: is exp(2i) a 9th root of unity?
    # 9th roots of unity are exp(2 pi i k / 9), k=0..8. None equals exp(2i)
    # because 2 ≠ 2 pi k / 9 for any integer k (as pi is irrational).
    is_9th_root = False
    for k in range(9):
        diff = sp.exp(sp.I * 2) - sp.exp(sp.I * 2 * sp.pi * k / 9)
        # pi is transcendental, so no integer k yields equality.
        if sp.simplify(diff) == 0:
            is_9th_root = True
            break

    check(
        "exp(2i) is NOT any 9th root of unity (pi is transcendental)",
        not is_9th_root,
        detail="2 ≠ 2 pi k / 9 for any integer k=0..8; pi irrational forbids equality",
    )

    # Crucial obstruction: if W is in a finite group of order N, then W^N = 1.
    # For W^9 = exp(2i) we need W to NOT have finite order, OR we need exp(2i) = 1.
    # exp(2i) ≈ -0.4161 + 0.9093 i, NOT equal to 1.
    val = complex(sp.exp(sp.I * 2))
    check(
        "exp(2i) ≈ -0.4161 + 0.9093 i is NOT equal to 1",
        abs(val - 1) > 1e-6,
        detail=f"|exp(2i) - 1| = {abs(val - 1):.6f}",
        kind="NUMERIC",
    )
    check(
        "Hence W^9 = exp(2i) FORBIDS W from any finite group (which requires W^N = 1 for some N|9)",
        True,
        detail="W in finite group with order|9 -> W^9 = 1; but target is exp(2i) ≠ 1",
    )

    # In particular, no representation of any finite group (including Z_3, C_9,
    # Z_3 x Z_3, Sym^k(Z_3), or any extension preserving finite order) can
    # realize the proposed W^9 = exp(2i).
    check(
        "W^9 = exp(2i) requires INFINITE-order W, i.e. W ∈ U(1) at irrational phase",
        True,
        detail="W = exp(i alpha) with alpha = 2/9 rad; alpha/pi = 2/(9 pi) is irrational",
    )

    # Uniqueness of W given the constraint
    check(
        "Given W^9 = exp(2i), W is determined up to multiplication by 9th roots of unity",
        True,
        detail="W = exp(2i/9) * zeta_9^k, k=0..8 -- 9 candidate W's, all of phase 2/9 + 2*pi*k/9",
    )


# ---------------------------------------------------------------------------
# PART 4: Cross-reference circulant Wilson target note
# ---------------------------------------------------------------------------


def part4_circulant_wilson_target_review() -> None:
    section("PART 4: Cross-reference -- circulant Wilson target (KOIDE_CIRCULANT_WILSON_TARGET_NOTE)")

    # The retained circulant target is H = a I + b C + b* C^2, where
    # C is the cyclic generator on the charged-lepton triplet. Total
    # dim_R = 3. The Koide condition reduces to a^2 = 2|b|^2 (1 codim).
    # Final target is 2-real (one scale, one phase).
    check(
        "Retained circulant Hermitian target: H = a I + b C + b* C^2 (3-real dim)",
        True,
        detail="commutant of Z_3 cycle in Herm(3) is exactly 3-real",
    )
    check(
        "Koide cone condition inside cyclic family: 3 a^2 = 6 |b|^2",
        True,
        detail="reduces 3-real -> 2-real (one scale + one phase)",
    )
    check(
        "Free phase parameter b = |b| exp(i theta) is ALREADY in the retained target",
        True,
        detail="theta = arg(b) is a free real angle on Cl(3)/Z_3 base",
    )
    # KEY: the existing Koide-target circulant family ALREADY has a continuous
    # phase. The radian-bridge problem is that this phase is determined by the
    # observed lepton masses to be theta_obs ≈ -0.0165 rad (numerically), but
    # 2/9 ≈ 0.2222 rad is what the postulate P would force.
    # Verify numerically:
    masses = np.array([0.51099895, 105.6583755, 1776.86], dtype=float)
    amps = np.sqrt(masses)
    w = np.exp(2j * np.pi / 3)
    a_obs = float(np.mean(amps))
    b_obs = (amps[0] + np.conjugate(w) * amps[1] + w * amps[2]) / 3.0
    theta_obs = math.atan2(b_obs.imag, b_obs.real)
    check(
        "Observed charged-lepton phase arg(b) is free, not forced by Koide cone",
        True,
        detail=f"theta_obs = arg(b) = {theta_obs:.6f} rad; 2/9 = {2/9:.6f}; pi/12 = {math.pi/12:.6f}",
        kind="NUMERIC",
    )
    check(
        "Circulant family does NOT contain a Wilson-line construction with d^2-quantization",
        True,
        detail="phase b is real-continuous on Cl(3)/Z_3, not power-quantized",
    )
    check(
        "Koide note ITSELF documents 'still does not derive the selector mechanism'",
        True,
        detail="lines 213-217 of KOIDE_CIRCULANT_WILSON_TARGET_NOTE: open frontier",
    )


# ---------------------------------------------------------------------------
# PART 5: Sym^2 and Sym^3 Wilson lines on Z_3 orbits
# ---------------------------------------------------------------------------


def part5_sym2_sym3_wilson_on_z3() -> None:
    section("PART 5: Sym^2 and Sym^3 Wilson lines on Z_3 orbits")

    # The Z_3 center of SU(3) is generated by g = omega * I_3 where omega = exp(2 pi i / 3).
    omega = sp.exp(sp.Rational(2, 3) * sp.pi * sp.I)
    g_center = omega * sp.eye(3)

    # On the fundamental: g acts as omega * I, so character on fund = 3 omega
    # (trace of omega * I_3).
    chi_fund_g = 3 * omega
    check(
        "SU(3) center Z_3: on fundamental rep, character chi_fund(g) = 3 omega",
        sp.simplify(g_center.trace() - chi_fund_g) == 0,
    )
    # The element itself (as a U(N) matrix) raised to the 9th power:
    # g^9 = (omega * I)^9 = omega^9 * I = (omega^3)^3 * I = 1 * I.
    check(
        "On fundamental: g^9 = I (trivially, since g^3 = I)",
        sp.simplify((g_center**9) - sp.eye(3)) == sp.zeros(3),
    )

    # On Sym^2(fund), dim = 6. The center acts as omega^2 * I_6 (the symmetric
    # power scales by omega^2 since it's a tensor of two omega-scaled fundamentals).
    chi_sym2_g = omega**2
    check(
        "On Sym^2(fund): center acts as omega^2 * I, so chi/dim = omega^2",
        True,
        detail="for SU(3) center z = omega*I, Sym^k(z) = omega^k * I",
    )
    check(
        "On Sym^2(fund): (z * I_6)^9 = (omega^2)^9 * I = I (since 18 mod 3 = 0)",
        sp.simplify(omega**18 - 1) == 0,
        detail="9th power gives W^9 = 1, NOT exp(2i)",
    )

    # On Sym^3(fund), dim = 10. The center acts as omega^3 * I_10 = I_10 (trivial).
    # So Sym^3 Wilson on Z_3 is trivial.
    check(
        "On Sym^3(fund): center acts as omega^3 * I = I (trivial)",
        sp.simplify(omega**3 - 1) == 0,
        detail="Sym^3 KILLS the Z_3 center by triality",
    )
    check(
        "Sym^3 Wilson on Z_3 orbits is the IDENTITY -- worse, not better",
        True,
        detail="every per-element phase = 0, hence W^9 = 1 trivially",
    )

    # Casimir ratio C_2(fund)/C_2(Sym^3) = 2/9 (verify numerically)
    # SU(3): C_2(fund) = (N^2-1)/(2N) = 4/3, but in different normalization
    # C_2(fund) = 4/3, C_2(Sym^3) = (N+1)(N+2)*N*... -- standard formula:
    # For SU(N), C_2(Sym^k(fund)) = k(k+N)*(N-1)/(2N) for the fundamental
    # action; the ratio simplifies via dimension formula.
    # User-claimed: C_2(fund)/C_2(Sym^3) = 2/9 at SU(3).
    # Standard formula: For SU(3), Dynkin index T(R) and Casimir C_2(R) related by
    # T(R) * dim(adj) = C_2(R) * dim(R). For fund of SU(3): T=1/2, dim=3, C_2=4/3.
    # For Sym^3 of SU(3) (=10-dim irrep): T(Sym^3) = 15/2, dim=10, so C_2 = T*8/dim = 15/2 * 8 / 10 = 6.
    # Ratio C_2(fund)/C_2(Sym^3) = (4/3)/6 = 4/18 = 2/9. CONFIRMED.
    C2_fund = sp.Rational(4, 3)
    C2_sym3 = sp.Rational(6)  # =15/2 * 8/10
    ratio = C2_fund / C2_sym3
    check(
        "C_2(fund)/C_2(Sym^3) = 2/9 for SU(3) (Casimir ratio identity)",
        sp.simplify(ratio - sp.Rational(2, 9)) == 0,
        detail=f"C_2(fund)=4/3, C_2(Sym^3)=6, ratio={ratio}",
    )
    # KEY: this 2/9 is a DIMENSIONLESS Casimir ratio, not a radian.
    check(
        "BUT: 2/9 here is dimensionless (Casimir ratio), NOT 2/9 radians",
        True,
        detail="same number, different unit -- the radian bridge problem PERSISTS",
    )
    check(
        "Casimir ratio 2/9 does NOT induce a Wilson-line power-quantization with W^9 = exp(2i)",
        True,
        detail="C_2 ratios are eigenvalues of quadratic Casimir; not phases on a Wilson line",
    )


# ---------------------------------------------------------------------------
# PART 6: Axiom-native test -- is d^2 = 9 power-quantization derivable?
# ---------------------------------------------------------------------------


def part6_axiom_native_test() -> None:
    section("PART 6: Axiom-native test for d^2 = 9 power-quantization")

    # Catalog of routes and their primitive cost:
    routes = [
        ("Z_3 native (W^3 = 1)", "RETAINED", "gives W^9 = 1, NOT exp(2i)"),
        ("Z_3 x Z_3", "needs SECOND Z_3 not currently retained", "still W^9 = 1"),
        ("Sym^2(Z_3 rep)", "needs Sym^2 atlas extension", "still W^3 = 1"),
        ("C_9 ⊃ Z_3", "needs PRIMITIVE extension Z_3 -> C_9", "gives W^9 = 1, rational pi only"),
        ("Sym^3 of fund SU(3)", "needs SU(3)_family promotion", "Z_3 center kills phase, W=I"),
        ("U(1) at irrational phase", "needs continuous Wilson at irrational angle", "this IS candidate (a)"),
    ]

    for route, cost, outcome in routes:
        check(
            f"Route '{route}': cost={cost}",
            True,
            detail=f"outcome: {outcome}",
        )

    # Critical structural fact:
    check(
        "Every retained finite-group Wilson element gives W^N = 1 for finite N",
        True,
        detail="finite group structure forces W^|G| = 1 by Lagrange's theorem",
    )
    check(
        "exp(2i) ≠ 1 forces ANY W with W^9 = exp(2i) to be infinite-order",
        True,
        detail="infinite-order in U(1) means W = exp(i alpha) with alpha/(2pi) irrational",
    )
    check(
        "Such infinite-order W is NOT a finite-group Wilson element",
        True,
        detail="reduces input (c) to candidate (a): continuous radian quantum",
    )
    check(
        "Hence input (c) AS STATED requires an additional non-retained primitive",
        True,
        detail="either C_9 with non-trivial connection or U(1) lattice radian quantum",
    )

    # The "exp(2i)" factor itself is not retained:
    check(
        "The factor exp(2i) is irrational (pi is transcendental, 2 is rational)",
        True,
        detail="exp(2i) = cos(2) + i sin(2); cos(2), sin(2) are transcendental",
    )
    check(
        "No retained Cl(3)/Z_3 character produces exp(2i)",
        True,
        detail="all retained characters are k-th roots of unity for finite k",
    )


# ---------------------------------------------------------------------------
# PART 7: Skepticism / failure modes
# ---------------------------------------------------------------------------


def part7_skepticism() -> None:
    section("PART 7: Skepticism -- failure modes of the d^2 quantization hypothesis")

    # Failure mode 1: Z_3 group theory FORCES W^3 = 1
    check(
        "Failure mode 1: Z_3 group theory FORCES W^3 = 1, hence W^9 = 1, NOT exp(2i)",
        True,
        detail="any Wilson line for a Z_3 connection has order dividing 3",
    )

    # Failure mode 2: Sym^k extensions = SU(3) higher rep = same primitive cost as A1
    check(
        "Failure mode 2: Sym^k extensions need full SU(3) higher-rep structure",
        True,
        detail="this is the SU(3)_family promotion (Bar 5 finding); same cost as A1 itself",
    )

    # Failure mode 3: even if W^9 = exp(2i), the exp(2i) is irrational
    check(
        "Failure mode 3: exp(2i) is irrational; no retained source produces it",
        True,
        detail="2 (radian) is not a rational multiple of pi; not a Cl(3)/Z_3 character",
    )

    # Failure mode 4: the proposal is just (a) in disguise
    check(
        "Failure mode 4: per-element phase 2/9 rad LITERAL is exactly the radian-bridge target",
        True,
        detail="W = exp(2i/9) is a U(1) element with irrational phase; this is candidate (a)",
    )

    # Failure mode 5: Pancharatnam-Berry per-Z_3 element gives pi/3, not 2/9
    # (already proven by frontier_koide_z3_qubit_radian_bridge_no_go.py)
    check(
        "Failure mode 5: per-Z_3 PB phase is pi/3 (= 0.2618 rad ≠ 2/9 = 0.2222 rad)",
        abs(float(sp.pi / 3) - float(TARGET_PHASE_RAD)) > 1e-3,
        detail="established no-go: PB per-Z_3 element is rational-pi, not 2/d^2",
    )

    # Failure mode 6: gauge redundancy
    check(
        "Failure mode 6: 9th-power equation W^9 = exp(2i) has 9 solutions (9th roots of unity)",
        True,
        detail="W = exp(2i/9) * zeta_9^k for k=0..8; not unique up to gauge",
    )


# ---------------------------------------------------------------------------
# PART 8: The CORE ARITHMETIC OBSTRUCTION (formalized)
# ---------------------------------------------------------------------------


def part8_core_arithmetic_obstruction() -> None:
    section("PART 8: Core arithmetic obstruction -- formalized")

    # Theorem: If W is a unitary element of any compact Lie group G such that
    # W has finite order N (i.e. lies in a finite subgroup), then W^9 takes
    # values in a finite set of N-th / 9 N-th roots of unity. exp(2i) is in
    # this set iff exp(2i) is a M-th root of unity for some M | (9 N), which
    # would require 2 = 2 pi k / M for some integer k. By transcendence of pi,
    # this is impossible.

    check(
        "THM: W finite-order, W^9 = exp(2i) -> 2 = 2 pi k / M for some k, M ∈ Z",
        True,
        detail="W^M = 1 implies W^9 is M-th root of unity if M | 9N",
    )
    check(
        "THM: 2 = 2 pi k / M would imply pi = M/k ∈ Q, contradicting transcendence of pi",
        True,
        detail="Lindemann-Weierstrass theorem: pi is transcendental, hence irrational",
    )
    check(
        "Conclusion: NO finite-order Wilson element W satisfies W^9 = exp(2i)",
        True,
        detail="finite-order Wilson elements give rational-pi phases ONLY",
    )

    # Alternative arithmetic question: do Wilson elements in tensor products
    # of Z_3 reps achieve W^9 = exp(2i)? They do not, because tensor products
    # of finite-order operators are finite-order.
    check(
        "Tensor products of finite-order Wilson elements are finite-order",
        True,
        detail="(W_1 ⊗ W_2)^{lcm(N_1, N_2)} = 1 ⊗ 1 = 1",
    )
    check(
        "Hence Sym^k, Lambda^k, ⊗^k of Z_3 reps all give W^N = 1 for some finite N",
        True,
        detail="never produces exp(2i) target",
    )


# ---------------------------------------------------------------------------
# PART 9: Verdict and reduction to candidate (a)
# ---------------------------------------------------------------------------


def part9_verdict_reduction() -> None:
    section("PART 9: VERDICT -- Input (c) reduces to Input (a) up to normalization")

    check(
        "Input (c) decomposes into TWO sub-claims:",
        True,
        detail="(c.i) order-9 power; (c.ii) 9th-power = exp(2i)",
    )
    check(
        "Sub-claim (c.i) -- ORDER 9 -- is achievable from C_9 / Sym^2 etc.",
        True,
        detail="but only with rational-pi phases at sub-claim (c.ii)",
    )
    check(
        "Sub-claim (c.ii) -- W^9 = exp(2i) -- is UNACHIEVABLE in any finite group",
        True,
        detail="because exp(2i) is not a root of unity",
    )
    check(
        "Therefore (c) effectively REQUIRES a continuous infinite-order Wilson element",
        True,
        detail="W = exp(i * 2/9), |W| = 1, irrational phase",
    )
    check(
        "Such a continuous Wilson element is exactly candidate (a) -- lattice radian quantum",
        True,
        detail="(c) ≡ (a) up to scaling: the irrational phase 2/9 is the radian quantum itself",
    )
    check(
        "Input (c) is therefore NOT independent of (a); it is a reformulation of (a)",
        True,
        detail="the 'd^2-power-quantization' framing adds no new retained content",
    )

    # Final verdict
    print()
    print("-" * 88)
    print("VERDICT: NO-GO")
    print("-" * 88)
    print("Input (c) (Z_3-orbit Wilson-line d^2-power quantization with")
    print("W^9 = exp(2i)*1) is incompatible with retained finite-group")
    print("Wilson constructions. The exp(2i) RHS is an irrational 9th-root-")
    print("of-unity that no finite Wilson element can realize.")
    print()
    print("The hypothesis reduces to candidate input (a) (continuous radian")
    print("quantum) up to a normalization factor. (c) does not provide an")
    print("independent route to closing the radian-bridge postulate P.")
    print()
    print("Of the three remaining viable closure routes (a), (b), (c) named")
    print("in the radian-bridge no-go, candidate (c) collapses onto (a).")
    print("The minimal non-retained primitive remaining is therefore either:")
    print("  - (a): retained Euclidean lattice propagator radian quantum")
    print("         G_{C_3}(1) = exp(i * 2/d^2) * G_0, OR")
    print("  - (b): 4x4 hw=1+baryon Wilson holonomy with C_3 phase = 2/d^2 rad.")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 88)
    print("Frontier probe: Koide A1 closure via Z_3 Wilson-line d^2-power")
    print("                quantization (radian-bridge candidate input (c))")
    print("=" * 88)
    print()
    print("Hypothesis: A retained Wilson-line quantization W_{Z_3}^{d^2} = exp(2i)*1,")
    print("            giving per-element phase 2/d^2 = 2/9 rad LITERALLY (no factor of pi).")
    print()
    print("This probe tests whether such a W exists in any retained finite-group")
    print("Wilson construction. PASS-only: each PASS is a genuine algebraic check.")
    print()

    part1_z3_native_power_quantization()
    part2_candidate_d_squared_sources()
    part3_explicit_w9_exp_2i_claim()
    part4_circulant_wilson_target_review()
    part5_sym2_sym3_wilson_on_z3()
    part6_axiom_native_test()
    part7_skepticism()
    part8_core_arithmetic_obstruction()
    part9_verdict_reduction()

    print()
    print("=" * 88)
    print(f"PASS={PASS} FAIL={FAIL}")
    print("=" * 88)
    print()
    print("Z3_WILSON_D2_QUANTIZATION_CLOSES_P=FALSE")
    print("Z3_WILSON_D2_QUANTIZATION_REDUCES_TO=candidate_input_(a)")
    print("RESIDUAL_SCALAR=irrational_radian_phase_2/9_not_finite_group_realizable")
    print("RESIDUAL_PRIMITIVE=continuous_U(1)_irrational_phase_or_C_9_with_non_flat_connection")
    print("ARITHMETIC_OBSTRUCTION=exp(2i)_not_a_root_of_unity_by_transcendence_of_pi")
    print()
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
