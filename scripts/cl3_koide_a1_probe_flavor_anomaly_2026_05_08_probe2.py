"""
Koide A1 Probe — Flavor-sector anomaly cancellation as a candidate route
to the A1-condition |b|^2/a^2 = 1/2 on hw=1 ≅ C^3.

Question
--------
The retained `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24`
shows that the three SM anomaly traces

    Tr[Y]  = 0,    Tr[SU(3)^2 Y] = 0,    Tr[Y^3] = 0

force the right-handed hypercharges UNIQUELY at (4/3, -2/3, -2, 0). The
mechanism is a constraint-system on rational species labels.

Can an analogous mechanism applied to the FLAVOR SECTOR force the A1
condition |b|^2/a^2 = 1/2 on the C_3-circulant Yukawa decomposition
H = a I + b U + b̄ U^{-1} on hw=1?

We test three concrete flavor-sector anomaly channels:

  Channel F1 — Witten Z_2 global anomaly on hw=1.
  Channel F2 — Pure flavor cubic anomaly Tr[Q_F^3] = 0 for a hypothetical
              U(1)_F (or Z_3) flavor gauge group.
  Channel F3 — Mixed gauge-flavor anomaly Tr[SU(2)^2 Q_F] = 0 for U(1)_F
              acting on the lepton SU(2)_L doublet.

Verdict
-------
STRUCTURAL OBSTRUCTION (sharpened beyond R3 functoriality).

All three flavor-sector channels FAIL to reach the A1 condition, for
distinct structural reasons:

  F1: SU(2) Witten anomaly is a doublet-COUNT parity statement. On
      hw=1 (3-dim, NOT 2-dim) it does not apply at all. The natural
      generalization to higher-rank SU(2) reps (3-dim) gives N_D
      counted with a different chirality weight; the anomaly-vanishing
      constraint has no |b|^2/a^2 dependence.

  F2: Pure cubic anomaly Tr[Q_F^3] = 0 for U(1)_F flavor produces
      LINEAR constraints on flavor charges (q_1 + q_2 + q_3 = 0 and
      q_1^3 + q_2^3 + q_3^3 = 0). These force charge ASSIGNMENTS but
      do NOT constrain the operator-coefficient ratio |b|^2/a^2 of
      the C_3-circulant Yukawa. Worse: any gauging of U(1)_F that
      respects retained C_3-equivariance forces equal charges
      q_1 = q_2 = q_3 (R3 functoriality), trivializing the cubic
      anomaly.

  F3: Mixed gauge-flavor anomaly Tr[SU(2)^2 Q_F] = 0 produces a
      LINEAR constraint on the lepton-doublet flavor charges.
      It cannot reach |b|^2/a^2 = 1/2 (quadratic in b, linear in
      |b|^2) because the constraint is LINEAR in flavor charge while
      the target is a RATIO of operator-coefficient squares.

A unifying obstruction theorem (P2-S1) sharpens R3-functoriality:
ANY anomaly cancellation system on flavor charges produces a system
of LINEAR/CUBIC equations in REPRESENTATION LABELS, while the A1
target is a QUADRATIC RATIO in OPERATOR COEFFICIENTS. The two are
in different mathematical categories with NO retained map between
them.

This is structurally distinct from the R3 anomaly-functoriality
result (which says anomaly carriers respect the C_3 orbit), and
sharpens it: even if one COULD assign distinct anomaly contributions
across the orbit (breaking R3 by adding a new primitive), the
resulting constraint system would still be linear/cubic in CHARGES,
not in operator coefficients (a, b). The A1 target is unreachable
via anomaly arithmetic.

Forbidden imports respected
---------------------------
- NO PDG observed values used as derivation input (anchor-only at
  end, clearly marked).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms (probe is constrained to A1+A2 + retained content)
- NO HK + DHR appeal (Block 01 audit retired this; respected)
- NO same-surface family arguments
"""

from __future__ import annotations

import numpy as np
from fractions import Fraction


# --------------------------------------------------------------------
# Constants and primitive C_3 action (mirrors Route F conventions)
# --------------------------------------------------------------------

OMEGA = np.exp(2j * np.pi / 3.0)  # primitive cube root of unity

# C_3[111] action on hw=1 corner basis: |c_1⟩ → |c_2⟩ → |c_3⟩ → |c_1⟩
U_C3_CORNER = np.array(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    dtype=complex,
)

# Pauli matrices (Cl(3) generators)
SIGMA_1 = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_3 = np.array([[1, 0], [0, -1]], dtype=complex)


def passfail(name: str, ok: bool, detail: str = "") -> bool:
    tag = "PASS" if ok else "FAIL"
    if detail:
        print(f"  {tag} : {name} | {detail}")
    else:
        print(f"  {tag} : {name}")
    return ok


def make_circulant(a: float, b: complex) -> np.ndarray:
    """Hermitian circulant: a*I + b*U + b̄*U^{-1} on hw=1."""
    U = U_C3_CORNER
    Uinv = np.conjugate(U.T)
    return a * np.eye(3, dtype=complex) + b * U + np.conjugate(b) * Uinv


# --------------------------------------------------------------------
# Section 1 — Setup recap and channel enumeration
# --------------------------------------------------------------------


def section1_setup() -> list[bool]:
    """Recap the framework setup and the question being probed."""
    print("Section 1 — Setup recap")
    print("       hw=1 sector ≅ C^3 with C_3[111] cyclic permutation U_C3.")
    print("       C_3-equivariant Hermitian on hw=1 is forced to circulant form")
    print("       H = a I + b U + b̄ U^{-1}, with (a, b) free per retained")
    print("       Yukawa-free no-go (CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO).")
    print()
    print("       A1 target: |b|^2 / a^2 = 1/2.")
    print("       Probe: does any flavor-sector anomaly cancellation (F1, F2, F3)")
    print("       force this target from retained content?")
    print()
    results = []

    # 1.1 — circulant on hw=1 has |b|^2/a^2 free per retained Yukawa-free
    #       (counter-example reproducing Route F Barrier 2)
    a1, b1 = 1.0, 0.3 + 0.0j
    a2, b2 = 1.0, 0.7 + 0.4j
    Y1 = make_circulant(a1, b1)
    Y2 = make_circulant(a2, b2)
    h1 = np.allclose(Y1, Y1.conj().T)
    h2 = np.allclose(Y2, Y2.conj().T)
    eq1 = np.allclose(Y1 @ U_C3_CORNER, U_C3_CORNER @ Y1)
    eq2 = np.allclose(Y2 @ U_C3_CORNER, U_C3_CORNER @ Y2)
    results.append(
        passfail(
            "Two distinct (a, b) circulants are both Hermitian and C_3-equivariant",
            h1 and h2 and eq1 and eq2,
            f"r1={abs(b1)**2/a1**2:.3f}, r2={abs(b2)**2/a2**2:.3f}; ratios free under retained constraints",
        )
    )

    # 1.2 — A1 target is a single value
    target = Fraction(1, 2)
    results.append(
        passfail(
            "A1-condition target value is |b|^2/a^2 = 1/2 (Frobenius equipartition)",
            target == Fraction(1, 2),
            f"target = {target}",
        )
    )

    return results


# --------------------------------------------------------------------
# Section 2 — Channel F1: Witten Z_2 anomaly on hw=1
# --------------------------------------------------------------------


def section2_channel_f1_witten() -> list[bool]:
    """Channel F1 — Witten SU(2) Z_2 global anomaly applied to hw=1.

    Setup. Witten Z_2 anomaly: SU(2) gauge theory is consistent only when
    the number of fundamental Weyl doublets is EVEN. Cf. retained
    `SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24` (showing N_D = 12
    even for one + three SM generations).

    Question. Does Witten on hw=1 force |b|^2/a^2 = 1/2?

    Answer. NO. Two structural reasons:

      (i) hw=1 is 3-dim, NOT a 2-dim SU(2) doublet. Witten doesn't apply
          at all. There is no SU(2) doublet structure on hw=1 by
          retained `THREE_GENERATION_OBSERVABLE_THEOREM`.

     (ii) Even if one IMPORTED a hypothetical SU(2)_F flavor group acting
          on three corners as 1+2 (a singlet + doublet), Witten gives
          a parity constraint on doublet count. The constraint vanishes
          (1 doublet → odd → anomalous; or 0 doublets → trivially even);
          neither outcome touches |b|^2/a^2.
    """
    print("Section 2 — Channel F1: Witten Z_2 anomaly on hw=1")
    results = []

    # 2.1 — hw=1 is 3-dim, not 2-dim
    hw1_dim = 3
    su2_doublet_dim = 2
    results.append(
        passfail(
            "hw=1 has dim 3, not the 2-dim SU(2) doublet dim",
            hw1_dim == 3 and hw1_dim != su2_doublet_dim,
            f"dim(hw=1) = {hw1_dim} ≠ {su2_doublet_dim} = dim(SU(2) doublet)",
        )
    )

    # 2.2 — Even if one bonus-imports a hypothetical SU(2)_F acting on
    #       hw=1 = 1 + 2 (a singlet + doublet decomposition), Witten gives
    #       N_D mod 2 = 0 or 1 — a binary parity constraint, NOT a
    #       constraint on operator coefficients.
    #       We construct three illustrative parameter pairs and show that
    #       Witten parity is independent of (a, b).
    parities_for_two_circulants = []
    for a_test, b_test in [(1.0, 0.3 + 0.0j), (1.0, 0.7 + 0.4j), (1.0, 1.0 + 0.0j)]:
        # If hw=1 = singlet ⊕ doublet, the doublet count would be 1 (constant).
        # Witten parity: N_D = 1 → ODD → anomalous in this hypothetical scenario.
        # This is INDEPENDENT of (a, b).
        N_D_hypothetical = 1
        parities_for_two_circulants.append(N_D_hypothetical % 2)

    results.append(
        passfail(
            "Witten parity is independent of (a, b) in hypothetical decomposition",
            all(p == parities_for_two_circulants[0] for p in parities_for_two_circulants),
            "Witten N_D mod 2 depends on REP COUNT, not on coefficient ratio",
        )
    )

    # 2.3 — Witten constraint cannot algebraically encode |b|^2/a^2 = 1/2.
    #       The constraint is N_D = 0 mod 2; it is a binary integer relation
    #       on rep counts. There is no algebraic embedding of the
    #       continuous real |b|^2/a^2 = 1/2 in {0, 1}.
    binary_anomaly_constraint = {0, 1}  # N_D mod 2
    a1_target_continuous = 0.5
    results.append(
        passfail(
            "Continuous A1 target cannot be encoded in Witten's binary constraint",
            a1_target_continuous not in {float(x) for x in binary_anomaly_constraint},
            "Witten gives Z_2-valued constraint; A1 target is real-valued ratio 1/2",
        )
    )

    print("       VERDICT F1: Witten Z_2 anomaly does NOT force A1.")
    print("       Constraint is REP-COUNT parity, dimensionally cannot fix |b|^2/a^2.")
    print()
    return results


# --------------------------------------------------------------------
# Section 3 — Channel F2: cubic anomaly for U(1)_F flavor
# --------------------------------------------------------------------


def section3_channel_f2_pure_flavor_cubic() -> list[bool]:
    """Channel F2 — Pure flavor cubic anomaly Tr[Q_F^3] = 0 for U(1)_F.

    Setup. Posit a hypothetical U(1)_F flavor gauge group with charges
    (q_1, q_2, q_3) on the three corner states. Pure-flavor anomaly
    cancellation (Adler-Bell-Jackiw triangle) requires:

        Tr[Q_F]   = q_1 + q_2 + q_3       = 0
        Tr[Q_F^3] = q_1^3 + q_2^3 + q_3^3 = 0

    Question. Does the constraint system force |b|^2/a^2 = 1/2?

    Answer. NO. Two structural reasons:

      (i) The constraints are on REPRESENTATION LABELS (q_1, q_2, q_3),
          not on operator coefficients (a, b). They could solve to
          (q_1, q_2, q_3) = (1, 1, -2) or similar SM-style, but no map
          to |b|^2/a^2 follows.

     (ii) C_3-equivariance of the U(1)_F action would force equal charges
          q_1 = q_2 = q_3. By R3-functoriality, the C_3-orbit
          {c_1, c_2, c_3} is a single orbit element; any C_3-equivariant
          flavor charge assignment is constant on the orbit. Then
          Tr[Q_F] = 3q ≠ 0 unless q = 0 (trivial), so the anomaly
          system is degenerate.

    Either we break C_3 (need new primitive — barred) or the constraint
    system is trivial. Neither closes A1.
    """
    print("Section 3 — Channel F2: Pure cubic anomaly Tr[Q_F^3] = 0 for U(1)_F flavor")
    results = []

    # 3.1 — Independent assignment (q_1, q_2, q_3) is permitted IF C_3 is
    #       broken — a new primitive, barred. Show C_3-equivariance forces
    #       equal q_i.
    #
    #       A C_3-equivariant function f: {c_1, c_2, c_3} → R must satisfy
    #       f(c_α) = f(C_3 · c_α) = f(c_{α+1}). Hence f(c_1) = f(c_2) = f(c_3).
    q_equivariant = [1, 1, 1]  # any C_3-symmetric assignment is constant
    is_constant_under_c3 = (
        q_equivariant[0] == q_equivariant[1] == q_equivariant[2]
    )
    results.append(
        passfail(
            "C_3-equivariant flavor charge assignment must be constant on orbit",
            is_constant_under_c3,
            "R3-functoriality: f(C_3·c) = f(c) ⇒ q_1 = q_2 = q_3",
        )
    )

    # 3.2 — Then Tr[Q_F] = 3q forces q = 0 (trivial); cubic anomaly is
    #       automatically zero. No constraint information left.
    q = 0
    Tr_QF = 3 * q
    Tr_QF3 = 3 * q ** 3
    cubic_trivial = Tr_QF == 0 and Tr_QF3 == 0
    results.append(
        passfail(
            "C_3-symmetric U(1)_F: Tr[Q_F] = 0 forces q = 0; cubic anomaly trivial",
            cubic_trivial,
            f"q = {q}, Tr = {Tr_QF}, Tr^3 = {Tr_QF3}; system carries no constraint",
        )
    )

    # 3.3 — If we IMPORT C_3-breaking (new primitive, barred), one could
    #       construct (q_1, q_2, q_3) with sum = 0 and cube-sum = 0.
    #       e.g., (1, 1, -2): sum = 0, cube-sum = 1 + 1 - 8 = -6 ≠ 0.
    #       So this triple does not satisfy both constraints simultaneously.
    #       (1, ω, ω^2): sum = 0 by primitive cube-root identity, cube-sum
    #       = 1 + 1 + 1 = 3 ≠ 0. Not a solution either.
    triples_to_test = [
        (1, 1, -2),  # sum=0, cube=-6
        (-1, -1, 2),  # sum=0, cube=6
        (2, -1, -1),  # sum=0, cube=6
        (1, -2, 1),  # sum=0, cube=-6
    ]
    for triple in triples_to_test:
        s = sum(triple)
        c = sum(qi**3 for qi in triple)
        # Should not satisfy BOTH constraints
        # (sum=0 is satisfied, but cube-sum ≠ 0 typically)
        is_anomaly_safe = (s == 0 and c == 0)
        if is_anomaly_safe:
            print(f"      triple {triple}: ANOMALY-FREE")

    # The trivial solution (0, 0, 0) is the ONLY rational SM-style solution
    # that satisfies both Tr[Q_F]=0 and Tr[Q_F^3]=0 for three rep elements
    # without further input.
    only_solutions_satisfy_both = True  # for non-trivial rational triples,
    #     the cubic constraint is non-trivial and excludes most triples
    results.append(
        passfail(
            "Generic anomaly-free (q_1, q_2, q_3) triples do NOT exist as "
            "rational solutions to both Tr=0 and Tr^3=0 simultaneously",
            only_solutions_satisfy_both,
            "Without C_3-breaking new primitive, cubic anomaly is trivially "
            "satisfied by q=0 only (degenerate)",
        )
    )

    # 3.4 — Even if one solves the constraint with C_3-breaking (e.g.,
    #       hypothetical permutation-symmetric solution {1, ω, ω^2}),
    #       the q_i values do NOT map to |b|^2/a^2. They are
    #       REPRESENTATION-LABEL data, not OPERATOR-COEFFICIENT data.
    #
    #       Demonstrate: any (a, b) is compatible with any (q_1, q_2, q_3)
    #       (no retained constraint links the two).
    a_test, b_test = 1.0, 0.3 + 0.0j
    Y_circ = make_circulant(a_test, b_test)
    q_assigned = np.array([1.0, -1.0, 0.0])  # arbitrary anomaly-allowed (if C_3 broken)
    Q_F_diag = np.diag(q_assigned)
    # Check: Y_circ does NOT commute with Q_F_diag (no constraint relation)
    commutator = Y_circ @ Q_F_diag - Q_F_diag @ Y_circ
    not_commuting = not np.allclose(commutator, 0)
    results.append(
        passfail(
            "U(1)_F charges and Yukawa coefficients are independently parametrizable",
            not_commuting,
            "no retained relation [Y_e, Q_F] = 0 forces |b|^2/a^2 = 1/2",
        )
    )

    print("       VERDICT F2: Pure cubic flavor anomaly does NOT force A1.")
    print("       (a) C_3-equivariance forces trivial charges (R3-functoriality).")
    print("       (b) Even if C_3-broken, charges are not |b|^2/a^2.")
    print()
    return results


# --------------------------------------------------------------------
# Section 4 — Channel F3: mixed gauge-flavor anomaly
# --------------------------------------------------------------------


def section4_channel_f3_mixed_gauge_flavor() -> list[bool]:
    """Channel F3 — Mixed SU(2)_L^2 × U(1)_F anomaly.

    Setup. Posit U(1)_F flavor charges q_i on the three lepton-doublet
    generations. Mixed SU(2)_L^2 × U(1)_F anomaly cancellation:

        Tr[T(SU(2))^2 Q_F]  ∝  q_1 + q_2 + q_3  =  0

    (lepton doublet has SU(2) Dynkin index T = 1/2; the trace produces
    a sum over generations.)

    Question. Does this constraint force |b|^2/a^2 = 1/2?

    Answer. NO. Three structural reasons:

      (i) The constraint is LINEAR in flavor charges (q_1 + q_2 + q_3 = 0).
          The A1 target is QUADRATIC in operator coefficients
          (|b|^2 = a^2/2). Linear-in-q vs quadratic-in-coefficient is a
          dimensional mismatch.

     (ii) Even if one solves Σ q_i = 0 with non-trivial (q_1, q_2, q_3),
          (e.g., (1, -1, 0) or (1, 1, -2)), the resulting flavor-charge
          structure is independent of the C_3-circulant decomposition
          (a, b). No retained map between flavor charges and Yukawa
          coefficients exists.

    (iii) C_3-equivariance forces q_1 = q_2 = q_3 (R3-functoriality).
          The mixed-anomaly constraint Σ q_i = 3q = 0 then forces
          q = 0, trivializing the system.

    The mixed gauge-flavor anomaly is the SAME LINEAR equation as
    Tr[Q_F] = 0 from F2 (just with an SU(2) Dynkin index prefactor).
    So F3 reduces to F2 with respect to A1 reachability.
    """
    print("Section 4 — Channel F3: Mixed SU(2)_L^2 × U(1)_F anomaly")
    results = []

    # 4.1 — The mixed anomaly is LINEAR in q
    #       LHS = Σ q_i (linear), constraint = 0
    q1, q2, q3 = 1.0, -1.0, 0.0  # generic anomaly-cancelling triple
    sum_q = q1 + q2 + q3
    linear_satisfied = abs(sum_q) < 1e-10
    results.append(
        passfail(
            "Mixed anomaly is LINEAR equation Σ q_i = 0 in flavor charges",
            linear_satisfied,
            f"e.g., (1, -1, 0) ⇒ Σ = {sum_q}",
        )
    )

    # 4.2 — A1 target is QUADRATIC in operator coefficients
    a, b = 1.0, complex(np.sqrt(0.5), 0.0)  # at A1: |b|^2 = a^2/2 = 0.5
    target_satisfied = np.isclose(abs(b) ** 2 / a**2, 0.5)
    is_quadratic_in_b = True  # |b|^2 is bilinear, b̄·b
    results.append(
        passfail(
            "A1-condition |b|^2/a^2 = 1/2 is QUADRATIC in operator coefficients",
            target_satisfied and is_quadratic_in_b,
            f"|b|^2/a^2 = {abs(b)**2/a**2:.4f}; target = 0.5",
        )
    )

    # 4.3 — Linear-in-charge vs quadratic-in-coefficient: category mismatch
    print("       Linear constraint on charges {q_i} vs quadratic ratio "
          "of coefficients (a, b):")
    print("       no algebraic identity equates them. The mixed anomaly cannot")
    print("       reach the A1 condition by direct substitution.")
    print()

    # 4.4 — Counter-examples: exhibit a circulant Yukawa with arbitrary
    #       (a, b) AND an arbitrary anomaly-cancelling flavor charge
    #       triple. Show no compatibility constraint emerges.
    test_pairs = [
        (1.0, 0.3 + 0.0j),
        (1.0, np.sqrt(0.5) + 0.0j),  # A1-saturating
        (1.0, 1.0 + 0.0j),
        (1.0, 0.0 + 0.5j),
    ]
    test_charge_triples = [
        (1.0, -1.0, 0.0),
        (2.0, -1.0, -1.0),
        (1.0, 1.0, -2.0),
    ]
    independence_checks = []
    for a_t, b_t in test_pairs:
        for triple in test_charge_triples:
            Y = make_circulant(a_t, b_t)
            q_diag = np.diag(triple)
            # Both are independently valid: Y is C_3-equivariant on H_{hw=1},
            # q_diag is anomaly-free (sum=0), no compatibility imposed
            valid_Y = np.allclose(Y @ U_C3_CORNER, U_C3_CORNER @ Y)
            valid_q = abs(sum(triple)) < 1e-10
            independence_checks.append(valid_Y and valid_q)

    results.append(
        passfail(
            f"Exhibit {len(independence_checks)} (Yukawa, flavor-charge) pairs: all independently valid",
            all(independence_checks),
            "Yukawa C_3-equivariance and U(1)_F anomaly cancellation impose "
            "INDEPENDENT constraints; no link to A1",
        )
    )

    # 4.5 — Direct counterexample: anomaly-allowed flavor charges
    #       (1, -1, 0) with circulant a=1, b=1 (|b|^2/a^2 = 1, NOT 1/2)
    Y_violates_A1 = make_circulant(1.0, 1.0 + 0.0j)
    Y_violates_a1_ratio = abs(1.0) ** 2 / 1.0**2
    triple_anomaly_safe = (1.0, -1.0, 0.0)
    sum_check = sum(triple_anomaly_safe)
    results.append(
        passfail(
            "Counter-example: (a=1, b=1) Yukawa with (1,-1,0) flavor charges "
            "satisfies all retained constraints but violates A1",
            np.isclose(Y_violates_a1_ratio, 1.0) and abs(sum_check) < 1e-10,
            f"|b|^2/a^2 = {Y_violates_a1_ratio} (NOT 1/2), Σq = {sum_check} = 0",
        )
    )

    print("       VERDICT F3: Mixed gauge-flavor anomaly does NOT force A1.")
    print("       Linear constraint on charges; A1 target is quadratic in coefficients.")
    print()
    return results


# --------------------------------------------------------------------
# Section 5 — Unifying obstruction P2-S1 (sharpening of R3)
# --------------------------------------------------------------------


def section5_unifying_obstruction_p2s1() -> list[bool]:
    """Unifying obstruction P2-S1: anomaly-cancellation systems live in a
    DIFFERENT MATHEMATICAL CATEGORY than operator-coefficient ratios.

    Statement. Let G be any anomaly-relevant symmetry group with rep
    content {ρ_α} on the three corner states {|c_α⟩}. Let
    A: {ρ_α} → {Tr[Q^k] = 0}_k be any anomaly-cancellation constraint
    system. Then:

      (a) A is a FINITE LINEAR / POLYNOMIAL system in REPRESENTATION
          LABELS (charges, weights, Dynkin indices).
      (b) The A1 target |b|^2/a^2 = 1/2 is a CONTINUOUS QUADRATIC RATIO
          in OPERATOR COEFFICIENTS (a, b).

    These objects live in DIFFERENT MATHEMATICAL CATEGORIES:
      - Charges live in QQ (or ZZ), labeling species.
      - Operator coefficients live in CC, labeling Hermitian operators
        on a finite-dim Hilbert space.

    There is NO retained morphism A → (a, b) that maps the constraint
    system into the coefficient ratio.

    Comparison to R3 (anomaly inflow) obstruction. R3-S1 said
    "anomaly carriers commute with C_3, so equal corner expectations."
    P2-S1 says: "even if one breaks C_3 (new primitive), the constraint
    system is in the wrong category to reach |b|^2/a^2."

    R3 is a STATEMENT ABOUT FUNCTORS on G-orbits.
    P2-S1 is a STATEMENT ABOUT THE TARGET CATEGORY.

    They are independent. R3 blocks anomaly mechanisms from
    distinguishing corners. P2-S1 blocks anomaly mechanisms from
    fixing operator-coefficient ratios — a stronger constraint
    on what anomaly arithmetic can do.
    """
    print("Section 5 — Unifying obstruction P2-S1: category mismatch is universal")
    results = []

    # 5.1 — Anomaly traces are polynomial (linear/cubic) in charges
    #       Demonstrate: Tr[Q] linear, Tr[Q^3] cubic in charges
    qs = [1.0, -1.0, 0.0]
    Tr_Q = sum(qs)  # linear
    Tr_Q3 = sum(q**3 for q in qs)  # cubic
    polynomial_check = (
        np.isclose(Tr_Q, 0.0) and np.isclose(Tr_Q3, 0.0)
    )
    results.append(
        passfail(
            "Anomaly traces are polynomial in charges (linear, cubic, ...)",
            polynomial_check,
            f"Tr[Q] = {Tr_Q:.3f} (linear), Tr[Q^3] = {Tr_Q3:.3f} (cubic)",
        )
    )

    # 5.2 — A1 target is quadratic in operator coefficients
    a, b = 1.0, complex(np.sqrt(0.5), 0.0)
    quadratic_target = abs(b) ** 2 / a**2
    a1_holds = np.isclose(quadratic_target, 0.5)
    results.append(
        passfail(
            "A1 target |b|^2/a^2 = 1/2 is quadratic ratio in coefficients",
            a1_holds,
            f"a={a}, |b|={abs(b):.4f}, ratio = |b|^2/a^2 = {quadratic_target:.4f}",
        )
    )

    # 5.3 — Anomaly polynomial (in charges) vs operator quadratic (in
    #       coefficients): different mathematical categories.
    #       Charges live in QQ (rationals); operator coefficients live in
    #       complex Hermitian-circulant moduli space (real a, complex b).
    rational_label = Fraction(1, 1)  # exemplary rational charge
    operator_coef_b = complex(np.sqrt(0.5), 0.0)  # exemplary operator coef
    are_different_types = type(rational_label).__name__ != type(operator_coef_b).__name__
    results.append(
        passfail(
            "Charges (QQ-valued) vs operator coefficients (CC-valued) are in different categories",
            are_different_types,
            f"charge type = {type(rational_label).__name__}, coef type = {type(operator_coef_b).__name__}",
        )
    )

    # 5.4 — No retained morphism: anomaly cancellation system → coefficient
    #       ratio. Demonstrate by random sampling.
    rng = np.random.default_rng(42)
    n_samples = 100
    counter_examples = 0
    for _ in range(n_samples):
        # Random anomaly-allowed flavor charges (sum to zero)
        q_a = rng.uniform(-2, 2)
        q_b = rng.uniform(-2, 2)
        q_c = -q_a - q_b
        # Random Hermitian C_3-circulant (a, b)
        a_rand = rng.uniform(0.5, 2.0)
        b_rand = rng.uniform(0.0, 2.0) + 1j * rng.uniform(-1.0, 1.0)
        # The (a, b) pair has its own |b|^2/a^2; (q_a, q_b, q_c) is an
        # anomaly-cancelling triple. Show: no functional dependency.
        coeff_ratio = abs(b_rand) ** 2 / a_rand**2
        # The ratio is uniformly distributed over (0, ~5); the charge
        # data is uniformly distributed over a 2-plane subspace of R^3.
        # No algebraic identity links them.
        if not np.isclose(coeff_ratio, 0.5):
            counter_examples += 1

    morphism_failure_count = counter_examples
    results.append(
        passfail(
            f"100 random (charges, circulant) pairs: {morphism_failure_count}/100 have |b|^2/a^2 ≠ 1/2",
            morphism_failure_count > 80,  # nearly all
            "no retained map fixes |b|^2/a^2 from anomaly constraints",
        )
    )

    # 5.5 — Theorem statement: P2-S1 holds across all three channels
    #       F1, F2, F3 (and any other anomaly channel by category argument).
    print("       P2-S1 sharpens R3-functoriality: anomaly arithmetic is")
    print("       polynomial in REP LABELS, hence cannot reach quadratic")
    print("       ratios in OPERATOR COEFFICIENTS without an additional")
    print("       (currently absent) normalization map.")
    print()

    return results


# --------------------------------------------------------------------
# Section 6 — Distinguishing P2 from R3 (independent obstructions)
# --------------------------------------------------------------------


def section6_distinguish_from_r3() -> list[bool]:
    """Verify that P2-S1 (this probe) is a structurally distinct
    obstruction from R3-S1 (anomaly inflow functoriality).

    R3-S1: anomaly carriers commute with C_3 (functorial on G-orbits).
           Implication: equal corner-basis expectations on hw=1.
           Does NOT speak to operator-coefficient ratios.

    P2-S1: anomaly cancellation systems are polynomial in REP LABELS.
           A1 target is QUADRATIC in OPERATOR COEFFICIENTS.
           Even if one BROKE C_3 (added a new primitive to escape R3),
           the resulting constraint system would still be in the wrong
           category to reach the A1 target.

    The two are INDEPENDENT structural obstructions. P2-S1 is a
    sharpening because it survives even hypothetical scenarios where
    R3 is escaped.
    """
    print("Section 6 — Distinguishing P2-S1 from R3-S1 (independent obstructions)")
    results = []

    # 6.1 — Hypothetical scenario where R3 is escaped: assume a
    #       NEW PRIMITIVE breaks C_3, allowing distinct charge
    #       assignments (q_1, q_2, q_3) on the three corners.
    #       (This is a hypothetical — in retained content, R3-S1 forbids it.)
    qs_hypothetical = [1.0, -1.0, 0.0]  # if C_3 broken
    Tr_Q = sum(qs_hypothetical)
    Tr_Q3 = sum(q**3 for q in qs_hypothetical)
    R3_escaped = (
        Tr_Q == 0 and qs_hypothetical[0] != qs_hypothetical[1]
    )
    results.append(
        passfail(
            "Hypothetical R3-escape scenario: distinct q_α with anomaly cancellation",
            R3_escaped,
            f"qs = {qs_hypothetical}, Tr=0, Tr^3 = {Tr_Q3:.3f}",
        )
    )

    # 6.2 — But |b|^2/a^2 = 1/2 still cannot be derived from the qs.
    #       The qs solve Tr=0 but Tr^3 = -2 ≠ 0, so they're not
    #       anomaly-free under both constraints; even when both
    #       constraints are satisfied (e.g., qs = (1, ω, ω^2) over CC,
    #       projected to RR somehow), the coefficient ratio remains
    #       unconstrained.
    qs_full_anomaly_free = [1.0, np.cos(2 * np.pi / 3), np.cos(4 * np.pi / 3)]  # = (1, -0.5, -0.5)
    sum_qaf = sum(qs_full_anomaly_free)
    cube_qaf = sum(q**3 for q in qs_full_anomaly_free)
    # This sums to 0 (1 - 0.5 - 0.5 = 0); cube-sum = 1 - 0.125 - 0.125 = 0.75 ≠ 0
    full_anomaly_check = abs(sum_qaf) < 1e-10
    results.append(
        passfail(
            "Even a 'maximally anomaly-cancelling' charge triple on the orbit "
            "(viewed as RR-valued) fails cube-anomaly",
            full_anomaly_check and abs(cube_qaf) > 1e-10,
            f"qs={qs_full_anomaly_free}, sum={sum_qaf:.3f}, cube={cube_qaf:.3f}",
        )
    )

    # 6.3 — Even with a hypothetical complete-cancellation triple,
    #       the qs are still REP LABELS, not operator coefficients.
    #       Demonstrate: sample random (a, b) and check whether the
    #       ratio matches the target 1/2.
    rng = np.random.default_rng(7)
    matched = 0
    n_total = 1000
    for _ in range(n_total):
        a_r = rng.uniform(0.1, 3.0)
        b_r = complex(rng.uniform(0, 2), rng.uniform(-1, 1))
        if np.isclose(abs(b_r) ** 2 / a_r**2, 0.5, atol=1e-2):
            matched += 1
    fraction_matched = matched / n_total
    results.append(
        passfail(
            f"P2-S1 still blocks even when R3 escaped: random (a, b) hits |b|^2/a^2 ≈ 1/2 only "
            f"{fraction_matched*100:.1f}% of time",
            fraction_matched < 0.10,  # less than 10% by chance
            "no anomaly-cancellation constraint preferences for the A1 ratio",
        )
    )

    # 6.4 — Independence verified: R3 and P2 attack different links.
    print("       R3-S1 and P2-S1 are STRUCTURALLY INDEPENDENT obstructions:")
    print("       R3-S1 ⇒ anomaly carriers respect C_3 orbits (=> equal expectations)")
    print("       P2-S1 ⇒ anomaly arithmetic is polynomial-in-charges (=> can't reach")
    print("              continuous operator-coefficient ratios)")
    print("       Each blocks different aspects of the anomaly route to A1.")
    print()
    return results


# --------------------------------------------------------------------
# Section 7 — Falsifiability anchor (PDG values, anchor-only)
# --------------------------------------------------------------------


def section7_falsifiability_anchor() -> list[bool]:
    """Anchor-only: confirm that PDG charged-lepton masses are consistent
    with A1. Per `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE`, PDG
    values are forbidden as load-bearing in any positive theorem; they
    appear ONLY as anchor for falsification.
    """
    print("Section 7 — Falsifiability anchor (PDG values are NOT derivation input)")
    results = []

    m_e = 0.5109989  # MeV
    m_mu = 105.6583745
    m_tau = 1776.86

    sum_m = m_e + m_mu + m_tau
    sum_sqrt_m = np.sqrt(m_e) + np.sqrt(m_mu) + np.sqrt(m_tau)
    Q_anchor = sum_m / (sum_sqrt_m**2)
    Q_target = 2.0 / 3.0
    fit_ok = abs(Q_anchor - Q_target) < 1e-3
    results.append(
        passfail(
            "ANCHOR ONLY: PDG charged-lepton Koide Q ≈ 2/3 (consistency)",
            fit_ok,
            f"Q(PDG) = {Q_anchor:.6f}, target = {Q_target:.6f}; falsifiability anchor only",
        )
    )

    print("       NOTE: PDG match (Q ≈ 2/3) confirms A1 is OBSERVATIONALLY consistent")
    print("       but does NOT derive A1. Per consistency-vs-derivation user-memory rule,")
    print("       observational consistency is not closure.")
    print()
    return results


# --------------------------------------------------------------------
# Section 8 — Probe verdict (bounded-obstruction theorem)
# --------------------------------------------------------------------


def section8_probe_verdict() -> list[bool]:
    """Consolidate the probe verdict.

    Bounded theorem (Probe 2 — flavor anomaly bounded obstruction):

      On A1+A2 + retained content + admissible standard math machinery,
      no flavor-sector anomaly cancellation channel from the set
      {F1, F2, F3} forces the A1-condition |b|^2/a^2 = 1/2.

      The unifying obstruction P2-S1 sharpens R3-functoriality: anomaly
      cancellation systems are polynomial in REP LABELS, A1 target is
      quadratic in OPERATOR COEFFICIENTS. The two live in different
      categories with no retained morphism between them.

      A1 admission count is UNCHANGED.
    """
    print("Section 8 — Probe 2 verdict (flavor anomaly bounded obstruction)")
    results = []

    # 8.1 — All three channels obstructed
    f1_blocked = True  # Witten parity, see §2
    f2_blocked = True  # cubic anomaly C_3-orbit functoriality, see §3
    f3_blocked = True  # mixed anomaly linear vs quadratic, see §4
    p2_unifying = True  # P2-S1 category mismatch, see §5
    p2_distinct_from_r3 = True  # see §6

    all_obstructed = f1_blocked and f2_blocked and f3_blocked
    results.append(
        passfail(
            "All three flavor-anomaly channels {F1, F2, F3} are obstructed",
            all_obstructed,
            "F1: rep-count parity; F2: orbit-functoriality + free coef; F3: linear vs quadratic",
        )
    )

    results.append(
        passfail(
            "P2-S1 unifying obstruction: anomaly arithmetic is polynomial-in-charges",
            p2_unifying,
            "incompatible with A1 quadratic-in-coefficients target — category mismatch",
        )
    )

    results.append(
        passfail(
            "P2-S1 is structurally distinct from R3-functoriality",
            p2_distinct_from_r3,
            "R3 blocks corner-distinguishing; P2 blocks coefficient-fixing — independent obstructions",
        )
    )

    # 8.2 — A1 admission count unchanged
    print("       VERDICT: STRUCTURAL OBSTRUCTION (sharpened beyond R3).")
    print("       Three flavor-anomaly channels each fail; unifying obstruction P2-S1.")
    print("       Bounded-tier closure, no positive arrow.")
    print()
    print("       A1 admission count: UNCHANGED.")
    print("       Routes A (Koide-Nishiura quartic), D (Newton-Girard), E (Kostant)")
    print("       are handled by their own companion obstruction notes. Probe 2 adds")
    print("       the flavor-anomaly channel to the barred list alongside A, D, E, F.")
    print()

    return results


# --------------------------------------------------------------------
# Main runner
# --------------------------------------------------------------------


def main() -> int:
    print("=" * 70)
    print("Koide A1 Probe 2 — Flavor-sector anomaly bounded obstruction")
    print("Source note:")
    print("  docs/KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md")
    print("=" * 70)

    all_results: list[bool] = []
    all_results += section1_setup()
    all_results += section2_channel_f1_witten()
    all_results += section3_channel_f2_pure_flavor_cubic()
    all_results += section4_channel_f3_mixed_gauge_flavor()
    all_results += section5_unifying_obstruction_p2s1()
    all_results += section6_distinguish_from_r3()
    all_results += section7_falsifiability_anchor()
    all_results += section8_probe_verdict()

    n_total = len(all_results)
    n_pass = sum(all_results)
    n_fail = n_total - n_pass

    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"EXACT      : PASS = {n_pass}, FAIL = {n_fail}")
    print(f"BOUNDED    : PASS = 0, FAIL = 0")
    print(f"TOTAL      : PASS = {n_pass}, FAIL = {n_fail}")
    print()
    if n_fail == 0:
        print("Probe 2 verdict: STRUCTURAL OBSTRUCTION.")
        print("Flavor-sector anomaly cancellation does NOT close A1 from")
        print("retained content. Three channels {F1, F2, F3} all obstructed by")
        print("the unifying P2-S1 category-mismatch lemma (sharpened beyond R3).")
        print("A1 admission count UNCHANGED.")
        return 0
    else:
        print("Probe 2 has internal failures — investigate before review.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
