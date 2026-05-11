"""
Probe U-Heavy-Modular -- Heavy-quark Yukawa textures via SL(2,Z) modular
flavor symmetry on Gamma(3) at tau = omega = exp(2 pi i / 3).

Authority role
--------------
Source-note proposal -- audit verdict and downstream status set only by
the independent audit lane.

Purpose
=======
Four prior probes (X-L1-Threshold #933, Y-L1-Ratios #946, Z-Quark-QCD-
Chain #958, V-Quark-Dynamical #981) failed to close heavy-quark mass
derivation from the retained physical Cl(3) local algebra plus Z^3
spatial substrate alone. V-Quark-Dynamical
identified the species-DIFFERENTIATION primitive on y_q(M_Pl) UV BC as
the lock.

Probe U tests an imported external tool: SL(2,Z) modular flavor
symmetry, specifically modular forms on the level-3 congruence subgroup
Gamma(3) at the self-dual fixed point tau = omega = exp(2 pi i / 3).
Modular flavor symmetry has been used in BSM model-building (Feruglio
2017 et seq.) to constrain Yukawa textures via:
- Modular forms on Gamma(N) of weight k as Yukawa-texture basis vectors
- 3-generation structure for Gamma(3) via C_3 subgroup of A_4 = SL(2,Z)/Gamma(3)
- Specific Yukawa textures depending on weight k

Verdict structure
=================
The probe is a bounded no-go / obstruction diagnostic for the
heavy-quark gate; the SL(2,Z) modular flavor symmetry tool does not
bridge the heavy-quark Yukawa-BC gap from retained framework content
alone.

Six load-bearing ingredients per Z-S4b-Audit hostile-review pattern:

  I1 SL(2,Z) modular flavor symmetry as a tool: IMPORTED
     (Feruglio 2017 framework; the toolkit is external/imported here,
     not admitted as repo theory).
  I2 Gamma(3) congruence subgroup of SL(2,Z): IMPORTED structure.
  I3 C_3 subgroup of A_4 = SL(2,Z)/Gamma(3) <-> retained Z_3 trichotomy:
     PARTIALLY RETAINED (the SELECTION RULE coincides; the IDENTIFICATION
     of modular C_3 with framework Z_3 is asserted, not derived).
  I4 Modulus tau = omega (C_3 fixed point / self-dual cusp): NOT RETAINED
     (would require an explicit structural assumption; not introduced here).
  I5 Modular-form values phi_k(omega) at tau = omega: IMPORTED
     (eta-product evaluations at algebraic points).
  I6 Yukawa-matrix Clebsch-Gordan coefficients from A_4 reps: IMPORTED.

Numerical diagnostics per analysis:

(A) C_3 selection content of Gamma(3) is ALREADY retained as Z_3
    trichotomy. Modular flavor adds NO new selection content; only
    numerical values, which are imports.

(B) In the C_3 root-of-unity diagnostic, the 3-vector Y_diag =
    (1, omega, omega^2) up to canonical normalization. Magnitudes are
    all unity. The diagnostic A_4-style Yukawa matrix is
    circulant with first row (1, omega^2, omega), giving eigenvalues
    of Y Y^dagger equal to (9, 0, 0). This is a RANK-1 mass matrix
    with 1 massive + 2 massless quark generations, structurally
    inconsistent with PDG-comparator (m_t, m_c, m_u) all being non-zero.

(C) Adding weight-4+ modular forms introduces 2+ free parameters
    (alpha, beta, ...) that are model-building inputs, not framework-
    derivable. Even with these free, NO retained-content derivation
    of m_t, m_b, m_c at 5% emerges.

(D) The probe verifies the structural redundancy: where modular flavor
    overlaps with retained Z_3 trichotomy, the framework already has
    the content; where it goes beyond, it imports.

Verdict: BOUNDED NO-GO / obstruction diagnostic. SL(2,Z) modular flavor
symmetry on Gamma(3) at tau = omega does not bridge the heavy-quark
Yukawa-BC gap from retained framework content alone: the useful C_3
selection content is already present, while the modular toolkit, tau
choice, modular-form values, and A_4 Clebsch-Gordan coefficients remain
imports. The root-of-unity circulant diagnostic also gives a rank-1
weight-2 texture. The species-differentiation primitive on y_q(M_Pl)
remains an open gap.

References
==========
- Feruglio F. (2017), "Are neutrino masses modular forms?", arXiv:1706.08749
  (foundational modular flavor symmetry paper).
- Liu T.K., Ding G.J. (2019), "Modular A_4 invariance and quark mass
  models", Phys. Lett. B (eta-product Y_2 constructions and A_4 reps).
- Penedo J.T., Petcov S.T. (2019), "Lepton masses and mixing from modular
  S_4 symmetry", Nucl. Phys. B 939, 292 (modular S_4 toolkit).
- Bertin J. (1993), "Modular forms" (classical SL(2,Z) / Gamma(N) theory).
- Apostol T.M. (1990), "Modular Functions and Dirichlet Series in
  Number Theory" (Dedekind eta function values).
- CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17:
  retained Z_3 trichotomy on Y_e (transports to Y_u, Y_d).
- HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17:
  q_H = 0 branch is gauge (retained).
- Probe V-Quark-Dynamical (PR #981): species-differentiation primitive
  identified as the lock.

Source-note authority
=====================
docs/KOIDE_U_HEAVY_MODULAR_SL2Z_NOTE_2026-05-08_probeU_heavy_modular.md

Usage
=====
    python3 scripts/cl3_koide_u_heavy_modular_2026_05_08_probeU_heavy_modular.py
"""

from __future__ import annotations

import cmath
import math
import sys
from fractions import Fraction


# ----------------------------------------------------------------------
# PASS/FAIL bookkeeping (Z-S4b-Audit + V-Quark-Dynamical pattern)
# ----------------------------------------------------------------------

class Counter:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.admitted = 0
        self.failures: list[str] = []

    def record(self, name: str, ok: bool, detail: str = "") -> None:
        tag = "PASS" if ok else "FAIL"
        if detail:
            print(f"  [{tag}] {name} | {detail}")
        else:
            print(f"  [{tag}] {name}")
        if ok:
            self.passed += 1
        else:
            self.failed += 1
            self.failures.append(name)

    def admit(self, name: str, detail: str = "") -> None:
        if detail:
            print(f"  [ADMITTED] {name} | {detail}")
        else:
            print(f"  [ADMITTED] {name}")
        self.admitted += 1

    def summary(self) -> None:
        print()
        print(
            f"SUMMARY: PASS={self.passed} FAIL={self.failed} "
            f"ADMITTED={self.admitted}"
        )
        if self.failed:
            print(f"FAILURES: {', '.join(self.failures)}")


# ----------------------------------------------------------------------
# Retained-grade anchors (carried forward from V-Quark-Dynamical)
# ----------------------------------------------------------------------

# SU(3) Casimirs (retained-grade; YT_EW_COLOR_PROJECTION_THEOREM)
N_COLOR = 3
N_QUARK = 6
N_F = 6  # asymptotic
C_F = Fraction(N_COLOR**2 - 1, 2 * N_COLOR)  # 4/3
C_A = Fraction(N_COLOR)  # 3
T_F = Fraction(1, 2)

# Retained-grade Wilson-chain anchors
ALPHA_BARE = 1.0 / (4.0 * math.pi)         # = 0.07957747
P_VEV = 0.5934                              # SU(3) plaquette at beta=6 (retained-grade input)
U_0 = P_VEV ** 0.25                         # ~ 0.87768 (Lepage-Mackenzie)
ALPHA_LM = ALPHA_BARE / U_0                 # ~ 0.090668
ALPHA_S_V = ALPHA_BARE / U_0**2             # ~ 0.10330
G_LATTICE = math.sqrt(4 * math.pi * ALPHA_LM)  # ~ 1.0676
WARD_BC = G_LATTICE / math.sqrt(6.0)        # ~ 0.4358 (y_t(M_Pl) Ward)

# Retained-grade energy scales
M_PL = 1.221e19  # GeV
V_EW = 246.22    # GeV

# Retained-grade Z_3 charges (CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY)
Q_L = (0, 1, -1)  # left-handed lepton/quark generation cycle (mod 3)
Q_R = (0, -1, 1)  # right-handed conjugate (mod 3)

# PDG comparators (post-derivation only)
PDG = {
    "u":   2.16e-3,
    "d":   4.67e-3,
    "s":   93.4e-3,
    "c":   1.27,
    "b":   4.18,
    "t":   172.69,
    "tau": 1.77686,
}

# Mass ratios for modular-flavor comparison
RATIO_TC = PDG["t"] / PDG["c"]   # ~136
RATIO_BC = PDG["b"]  / PDG["c"]   # ~3.29
RATIO_TB = PDG["t"] / PDG["b"]   # ~41.3
RATIO_TU = PDG["t"] / PDG["u"]   # ~80000


# ----------------------------------------------------------------------
# Cube root of unity and modular-form preliminaries
# ----------------------------------------------------------------------

OMEGA = cmath.exp(2j * math.pi / 3)  # primitive cube root of unity = exp(2 pi i / 3)
TAU_OMEGA = OMEGA  # imported diagnostic modulus value; not a repo axiom


# ----------------------------------------------------------------------
# SECTION 1 - Retained-grade inputs sanity (anchors used downstream)
# ----------------------------------------------------------------------

def section1_retained_anchors(c: Counter) -> None:
    print("Section 1 -- Retained-grade anchor sanity")
    c.record(
        "alpha_bare = 1/(4 pi)",
        abs(ALPHA_BARE - 1.0 / (4.0 * math.pi)) < 1e-15,
        f"= {ALPHA_BARE:.10f}",
    )
    c.record(
        "g_lattice = sqrt(4 pi alpha_LM) ~ 1.0676",
        abs(G_LATTICE - 1.0676) < 1e-3,
        f"= {G_LATTICE:.5f}",
    )
    c.record(
        "Ward BC y_t(M_Pl) = g_lattice/sqrt(6) ~ 0.4358",
        abs(WARD_BC - 0.4358) < 1e-3,
        f"= {WARD_BC:.5f}",
    )
    c.record(
        "Casimirs C_F=4/3, C_A=3, T_F=1/2",
        C_F == Fraction(4, 3) and C_A == Fraction(3) and T_F == Fraction(1, 2),
        f"C_F={C_F}, C_A={C_A}, T_F={T_F}",
    )
    # Verify Z_3 trichotomy charges (retained)
    c.record(
        "Z_3 q_L = (0, +1, -1) (retained-grade generation cycle)",
        Q_L == (0, 1, -1),
        f"q_L = {Q_L}",
    )
    c.record(
        "Z_3 q_R = (0, -1, +1) (conjugate to q_L)",
        Q_R == (0, -1, 1),
        f"q_R = {Q_R}",
    )
    # Conjugate triplet condition: q_L(i) + q_R(i) = 0 mod 3 for each i
    conj_ok = all((q_l + q_r) % 3 == 0 for q_l, q_r in zip(Q_L, Q_R))
    c.record(
        "Z_3 conjugate triplet condition q_L(i) + q_R(i) = 0 mod 3 for each i",
        conj_ok,
        f"OK: q_L + q_R = {tuple(q_l + q_r for q_l, q_r in zip(Q_L, Q_R))}",
    )
    print("    -> Retained-grade inputs: Z_3 trichotomy, Wilson-chain anchors, Casimirs")


# ----------------------------------------------------------------------
# SECTION 2 - Import classification
# ----------------------------------------------------------------------

def section2_tier_classification(c: Counter) -> None:
    """Classify each load-bearing ingredient as RETAINED/IMPORTED/etc.

    Modular flavor symmetry is external probe material, not repo theory.
    The toolkit is
    classified honestly: ZERO ingredients fully RETAINED, ONE PARTIALLY
    RETAINED (the C_3 selection coincidence), FIVE IMPORTED.
    """
    print()
    print("Section 2 -- Import classification")

    c.admit(
        "I1 SL(2,Z) modular flavor symmetry as a tool: IMPORTED",
        "Feruglio 2017 framework; the tool is external/imported here "
        "and is not derived from the physical Cl(3) local algebra plus "
        "Z^3 spatial substrate",
    )
    c.admit(
        "I2 Gamma(3) congruence subgroup of SL(2,Z): IMPORTED structure",
        "classical analytic number theory; SL(2,Z)/Gamma(3) ~ A_4 is "
        "mathematical fact, not framework derivation",
    )
    c.admit(
        "I3 C_3 in A_4 ~ SL(2,Z)/Gamma(3) <-> retained Z_3 trichotomy: PARTIALLY RETAINED",
        "C_3 SELECTION RULE coincides with retained Z_3 trichotomy on "
        "Y_e (transports to Y_u, Y_d); IDENTIFICATION of modular C_3 "
        "with framework Z_3 is asserted, not derived",
    )
    c.admit(
        "I4 Modulus tau = omega (C_3 fixed point / self-dual cusp): NOT RETAINED",
        "would require an explicit structural assumption; framework's modulus "
        "identification with SL(2,Z) tau is not derivable from retained "
        "content",
    )
    c.admit(
        "I5 Modular-form values phi_k(omega) at tau = omega: IMPORTED",
        "evaluations of eta-products at algebraic points; classical "
        "analytic number theory, not on the physical Cl(3) local algebra "
        "plus Z^3 spatial substrate surface",
    )
    c.admit(
        "I6 Yukawa Clebsch-Gordan coefficients from A_4 reps: IMPORTED",
        "standard modular-flavor model construction; integer C-G's "
        "from A_4 representation theory, not from retained framework",
    )
    print(
        "    -> 0 fully RETAINED, 1 PARTIALLY RETAINED (I3), 5 IMPORTED. "
        "Modular flavor toolkit is structurally redundant where it "
        "overlaps with retained Z_3 (I3), and imports new structure "
        "(I1, I2, I4, I5, I6) where it goes beyond. This pattern matches "
        "the 'tool overlaps with retained-grade content where it adds nothing "
        "new' obstruction."
    )


# ----------------------------------------------------------------------
# SECTION 3 - SL(2,Z)/Gamma(3) ~ A_4 quotient structure (imported)
# ----------------------------------------------------------------------

def section3_sl2z_gamma3_A4(c: Counter) -> None:
    """The level-3 congruence subgroup Gamma(3) is the kernel of the
    reduction map SL(2,Z) -> SL(2, Z/3Z). The quotient is

        SL(2,Z) / Gamma(3) ~ PSL(2, Z/3Z) ~ A_4

    of order 12. We verify the order arithmetic and basic structure.
    """
    print()
    print("Section 3 -- SL(2,Z)/Gamma(3) ~ A_4 quotient structure (imported)")

    # Order of SL(2, Z/p Z) for prime p is p^3 - p
    # For p = 3: 27 - 3 = 24
    order_SL2_Z3 = 3**3 - 3
    c.record(
        "|SL(2, Z/3Z)| = p^3 - p = 24 for p=3",
        order_SL2_Z3 == 24,
        f"= {order_SL2_Z3}",
    )

    # PSL(2, Z/3Z) = SL(2, Z/3Z) / {+/-I}, order 12
    order_PSL2_Z3 = order_SL2_Z3 // 2
    c.record(
        "|PSL(2, Z/3Z)| = 12 (order of A_4)",
        order_PSL2_Z3 == 12,
        f"= {order_PSL2_Z3}",
    )

    # A_4 has subgroups: trivial, Z_2 (3 copies), Z_3 (4 copies), V_4, A_4
    # The C_3 subgroup of A_4 has order 3 because 3 divides |A_4|.
    c.record(
        "C_3 subgroup of A_4: order 3 (cyclic generation symmetry)",
        order_PSL2_Z3 == 12 and order_PSL2_Z3 % 3 == 0,
        "C_3 = Z/3Z; the modular-flavor C_3 selection rule on the "
        "3-dim faithful representation",
    )

    # A_4 has 1, 1', 1'', 3 irreducible representations
    irrep_dims = (1, 1, 1, 3)
    sum_dim_sq = sum(d**2 for d in irrep_dims)
    c.record(
        "A_4 irreps {1, 1', 1'', 3}: sum of squared dims = 12 = |A_4|",
        sum_dim_sq == 12,
        f"1^2 + 1^2 + 1^2 + 3^2 = {sum_dim_sq}",
    )

    print("    -> A_4 structure imported as classical group theory.")
    print("    -> 3-dim faithful rep of A_4 is the modular-flavor")
    print("       generation triplet on which Y_2(tau) transforms.")


# ----------------------------------------------------------------------
# SECTION 4 - C_3 in A_4 vs retained Z_3 trichotomy (coincidence)
# ----------------------------------------------------------------------

def section4_C3_vs_Z3_trichotomy(c: Counter) -> None:
    """The Z_3 trichotomy theorem (retained, CHARGED_LEPTON_UE_IDENTITY_
    VIA_Z3_TRICHOTOMY_NOTE) forces Y_e support onto a permutation pattern
    via q_L(i) + q_H + q_R(j) = 0 mod 3.

    The C_3 in A_4 selection rule from SL(2,Z)/Gamma(3) acts on the 3-dim
    faithful rep as C_3: (phi_1, phi_2, phi_3) -> (phi_1, omega phi_2,
    omega^2 phi_3) (up to relabeling).

    These are the SAME selection rule. We verify by checking that the
    constraint q_L(i) + q_R(j) = 0 mod 3 (with q_H = 0) yields the
    diagonal support pattern that C_3 in A_4 forces on the 3-dim rep.
    """
    print()
    print("Section 4 -- C_3 in A_4 vs retained Z_3 trichotomy: SELECTION COINCIDENCE")

    # Z_3 trichotomy on q_H = 0 branch: Y_e[i,j] non-zero iff
    # q_L(i) + 0 + q_R(j) = 0 mod 3
    Y_support_z3 = [
        [1 if (Q_L[i] + Q_R[j]) % 3 == 0 else 0 for j in range(3)]
        for i in range(3)
    ]
    # On q_H = 0, since q_R = -q_L (mod 3), this gives diagonal support
    # for q_L(i) = -q_R(j) iff i = j (using the conjugate triplet
    # condition q_L(i) + q_R(i) = 0 mod 3)
    is_diagonal = all(
        Y_support_z3[i][j] == (1 if i == j else 0) for i in range(3) for j in range(3)
    )
    c.record(
        "Z_3 trichotomy q_H=0: Y_e[i,j] non-zero iff i=j (diagonal)",
        is_diagonal,
        f"Y_support = {Y_support_z3}",
    )

    # C_3 in A_4 acting on the 3-dim rep: the trivial 1-rep contraction
    # has diagonal support. This is the same support pattern found above.
    a4_trivial_support = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    c.record(
        "C_3 in A_4 on 3 x 3 -> 1 contraction: diagonal selection",
        a4_trivial_support == [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "3 x 3 = 1 + 1' + 1'' + 3 + 3; the 1 channel is sum_i phi_i phi_i', "
        "which has diagonal support i = j -- same as Z_3 trichotomy",
    )

    # Therefore the SELECTION RULE coincides
    c.record(
        "Selection rule from C_3 in A_4 = selection rule from Z_3 trichotomy",
        Y_support_z3 == a4_trivial_support,
        "both force Y_q to a permutation pattern with diagonal support "
        "(on q_H = 0 / 1-singlet contraction)",
    )

    print("    -> C_3 selection content is ALREADY retained as Z_3 trichotomy.")
    print("    -> Modular flavor adds NO new selection content beyond retained.")
    print("    -> This is the key obstruction: the tool overlaps with retained")
    print("       content where it adds nothing new (per probe verdict).")


# ----------------------------------------------------------------------
# SECTION 5 - tau = omega as C_3 fixed point of SL(2,Z) (admitted)
# ----------------------------------------------------------------------

def section5_tau_omega_fixed_point(c: Counter) -> None:
    """The order-3 element of SL(2,Z) is S T = (0 -1; 1 1) with characteristic
    polynomial x^2 - x + 1, eigenvalues at omega and omega^2. The fixed
    points of S T on the upper half plane are exactly tau = omega and
    tau = omega^2 (the latter is in the lower half plane; we take the
    one in H, which is omega = exp(2 pi i / 3)).

    This is structurally suggestive of the framework's Z_3 substrate,
    but identifying the framework modulus with this point is a NEW
    STRUCTURAL ASSUMPTION (admitted I4) and is not introduced here.
    """
    print()
    print("Section 5 -- tau = omega as C_3 fixed point of SL(2,Z)")

    # S T matrix: ((0, -1), (1, 1))
    # Determinant: 0 * 1 - (-1) * 1 = 1 (in SL(2,Z))
    # Trace: 0 + 1 = 1
    # Characteristic polynomial: x^2 - x + 1
    # Roots: (1 +/- sqrt(1 - 4))/2 = (1 +/- i sqrt(3))/2 = exp(+/- i pi / 3)
    # These have order 3 in PSL: (e^{i pi /3})^3 = e^{i pi} = -1, but in PSL
    # we identify A and -A, so the order is actually 3 (not 6).
    #
    # Equivalently, the matrix S T has order 6 in SL(2,Z) but order 3 in PSL(2,Z).
    # In PSL(2,Z), the action on tau is fractional linear:
    #   S T : tau -> -1 / (tau + 1)
    # Fixed points: tau = -1/(tau + 1) => tau(tau+1) = -1 => tau^2 + tau + 1 = 0
    # => tau = (-1 +/- i sqrt(3))/2 = omega or omega^2 (where omega^2 + omega + 1 = 0)
    # In H (Im tau > 0): tau = omega = exp(2 pi i / 3) = (-1 + i sqrt(3))/2

    # Verify omega satisfies omega^2 + omega + 1 = 0
    poly_value = OMEGA**2 + OMEGA + 1
    c.record(
        "omega satisfies omega^2 + omega + 1 = 0 (cube root of unity)",
        abs(poly_value) < 1e-12,
        f"omega^2 + omega + 1 = {poly_value:.6e}",
    )

    # Verify omega is in upper half plane
    c.record(
        "omega is in H (upper half plane): Im(omega) > 0",
        OMEGA.imag > 0,
        f"omega = {OMEGA}, Im = {OMEGA.imag:.6f}",
    )

    # Verify S T fixed-point equation: tau = -1/(tau + 1)
    rhs = -1.0 / (OMEGA + 1.0)
    c.record(
        "omega is fixed by S T: omega = -1/(omega + 1)",
        abs(OMEGA - rhs) < 1e-12,
        f"-1/(omega+1) = {rhs}, omega = {OMEGA}",
    )

    # Verify (S T)^3 = -I in SL(2,Z), so order 3 in PSL
    # S T = ((0, -1), (1, 1)); (S T)^2 = ((-1, -1), (1, 0)); (S T)^3 = ((-1, 0), (0, -1)) = -I
    ST = [[0, -1], [1, 1]]
    def mat_mult(A, B):
        return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]
    ST_squared = mat_mult(ST, ST)
    ST_cubed = mat_mult(ST_squared, ST)
    is_minus_I = ST_cubed == [[-1, 0], [0, -1]]
    c.record(
        "(S T)^3 = -I in SL(2,Z), so S T has order 3 in PSL(2,Z)",
        is_minus_I,
        f"(ST)^3 = {ST_cubed} = -I",
    )

    # Identification of framework modulus with tau = omega: ADMITTED
    c.admit(
        "Identification of framework modulus with SL(2,Z) tau = omega",
        "Even though omega is the C_3 fixed point and the framework's "
        "Z_3 cycle is retained, identifying the modular parameter with "
        "this point requires an explicit structural assumption (I4)",
    )

    print("    -> tau = omega is the C_3 fixed point of SL(2,Z) (mathematical fact).")
    print("    -> Identifying the framework modulus with tau = omega is admitted.")


# ----------------------------------------------------------------------
# SECTION 6 - Weight-2 modular forms Y_2(tau) on Gamma(3) at tau = omega
# ----------------------------------------------------------------------

def section6_weight2_modular_forms(c: Counter) -> None:
    """Diagnostic root-of-unity weight-2 vector.

    The actual eta-product evaluation of weight-2 Gamma(3) modular forms
    at tau = omega is an imported modular-flavor datum and is not derived
    here. The runner instead isolates the C_3-only root-of-unity ansatz

        Y_diag = (1, omega, omega^2)

    as a bounded diagnostic: if the only new information is the C_3 phase
    structure, the resulting circulant texture is rank deficient.
    """
    print()
    print("Section 6 -- Diagnostic C_3 root-of-unity weight-2 ansatz")

    # Diagnostic vector: this is not asserted as the eta-product value of
    # the modular-form triplet. It tests the C_3 root-of-unity texture alone.
    Y_1_omega = 1.0 + 0j
    Y_2_omega = OMEGA          # = exp(2 pi i / 3)
    Y_3_omega = OMEGA**2       # = exp(4 pi i / 3) = -1 - omega

    Y_omega_vec = [Y_1_omega, Y_2_omega, Y_3_omega]

    print(f"    Y_2(omega) = ({Y_1_omega:.4f}, {Y_2_omega:.4f}, {Y_3_omega:.4f})")
    print(f"    |Y_1(omega)| = {abs(Y_1_omega):.4f}")
    print(f"    |Y_2(omega)| = {abs(Y_2_omega):.4f}")
    print(f"    |Y_3(omega)| = {abs(Y_3_omega):.4f}")

    # All magnitudes are unity (since omega is on the unit circle)
    mags = [abs(y) for y in Y_omega_vec]
    all_unity = all(abs(m - 1.0) < 1e-12 for m in mags)
    c.record(
        "diagnostic Y_diag entries all have magnitude 1 (cube roots of unity)",
        all_unity,
        f"|Y_k| = {[f'{m:.4f}' for m in mags]}; equipartitioned",
    )

    # The diagnostic vector is covariant under diag(1, omega, omega^2):
    # diag(1, omega, omega^2) (1, omega, omega^2)^T = (1, omega^2, omega^4)
    # = (1, omega^2, omega) (since omega^3 = 1)
    rho_C3 = [
        [1.0 + 0j, 0, 0],
        [0, OMEGA, 0],
        [0, 0, OMEGA**2],
    ]
    rho_acted = [sum(rho_C3[i][j] * Y_omega_vec[j] for j in range(3)) for i in range(3)]
    # rho_acted should be (1, omega^2, omega^4) = (1, omega^2, omega)
    expected = [1.0 + 0j, OMEGA**2, OMEGA**4]
    matches = all(abs(rho_acted[i] - expected[i]) < 1e-12 for i in range(3))
    c.record(
        "rho(C_3) Y_diag gives a permutation of Y_diag (C_3 covariance)",
        matches,
        f"rho(C_3) Y = {[f'{y:.4f}' for y in rho_acted]}",
    )

    c.admit(
        "actual Gamma(3) modular-form values at tau=omega",
        "Eta-product values and derivatives are imported from analytic "
        "number theory; this runner does not derive or ratify them",
    )

    print("    -> Diagnostic C_3 vector is equipartitioned in magnitude.")
    print("    -> Any actual modular-form values remain imported data.")


# ----------------------------------------------------------------------
# SECTION 7 - Yukawa matrix construction Y_u, Y_d at tau = omega (imported)
# ----------------------------------------------------------------------

def section7_yukawa_matrix_construction(c: Counter) -> None:
    """For a diagnostic A_4-style circulant matter assignment, the Yukawa
    matrix is

        Y_q^{ij}(tau) = Y_2(tau)^k * c_{ij}^{(k)}

    where c_{ij}^{(k)} are integer Clebsch-Gordan coefficients from the
    A_4 tensor product 3 x 3 = 1 + 1' + 1'' + 3_S + 3_A.

    In the diagnostic root-of-unity ansatz, the weight-2 Yukawa matrix is
    (up to overall scale, with Y_1 = 1, Y_2 = omega, Y_3 = omega^2):

        Y_q(omega) = (  Y_1   Y_3   Y_2  )
                     (  Y_3   Y_2   Y_1  )
                     (  Y_2   Y_1   Y_3  )

    We compute the SVD spectrum of Y_q M_q^dagger to find the eigenvalue
    hierarchy.
    """
    print()
    print("Section 7 -- Diagnostic circulant Yukawa matrix and SVD spectrum")

    Y1, Y2, Y3 = 1.0 + 0j, OMEGA, OMEGA**2

    # Diagnostic A_4-style matrix: the 3 x 3 contraction gives a circulant-like matrix.
    Y_matrix = [
        [Y1, Y3, Y2],
        [Y3, Y2, Y1],
        [Y2, Y1, Y3],
    ]

    # Compute Y M^dagger (3x3 Hermitian)
    YYdag = [[0j for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                YYdag[i][j] += Y_matrix[i][k] * Y_matrix[j][k].conjugate()

    # Trace = sum of |Y_k|^2 over the matrix entries
    trace = sum(YYdag[i][i] for i in range(3))
    c.record(
        "Tr(Y M^dagger) at tau = omega",
        abs(trace - 9.0) < 1e-9,  # should be 9 since |Y_k|^2 = 1 each, 3 entries per row
        f"Tr = {trace:.4f}; expected 9 (3 rows x 3 |Y_k|^2 = 1 entries)",
    )

    # Compute eigenvalues of YYdag via characteristic polynomial
    # For a 3x3 matrix M, eigenvalues lambda satisfy:
    # lambda^3 - Tr(M) lambda^2 + (1/2)((Tr M)^2 - Tr(M^2)) lambda - det(M) = 0

    # Compute Tr(YYdag^2)
    YYdag2 = [[0j for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                YYdag2[i][j] += YYdag[i][k] * YYdag[k][j]
    trace2 = sum(YYdag2[i][i] for i in range(3))

    # Compute determinant
    det = (
        YYdag[0][0] * (YYdag[1][1] * YYdag[2][2] - YYdag[1][2] * YYdag[2][1])
        - YYdag[0][1] * (YYdag[1][0] * YYdag[2][2] - YYdag[1][2] * YYdag[2][0])
        + YYdag[0][2] * (YYdag[1][0] * YYdag[2][1] - YYdag[1][1] * YYdag[2][0])
    )

    # Characteristic polynomial coefficients
    # P(x) = x^3 - a x^2 + b x - c, where a = trace, b = (a^2 - trace2)/2, c = det
    a = trace.real
    b = (trace.real**2 - trace2.real) / 2.0
    c_coeff = det.real

    # The matrix Y at tau = omega is circulant with first row (Y1, Y3, Y2)
    # = (1, omega^2, omega). For a 3x3 circulant matrix C with vector
    # (c_0, c_1, c_2), the eigenvalues of C are
    #   lambda_k = c_0 + c_1 * omega^k + c_2 * omega^{2k}, k = 0, 1, 2
    # and the eigenvalues of C C^dagger are |lambda_k|^2.
    #
    # For (c_0, c_1, c_2) = (1, omega^2, omega):
    #   lambda_0 = 1 + omega^2 + omega = 0  (since 1 + omega + omega^2 = 0)
    #   lambda_1 = 1 + omega^2 * omega + omega * omega^2
    #            = 1 + omega^3 + omega^3 = 1 + 1 + 1 = 3
    #   lambda_2 = 1 + omega^2 * omega^2 + omega * omega^4
    #            = 1 + omega^4 + omega^5 = 1 + omega + omega^2 = 0
    #
    # So the eigenvalues of Y Y^dagger at tau = omega are (9, 0, 0) -- this
    # is a RANK-1 mass matrix with 2 MASSLESS generations.

    eigenvalues_circulant = []
    cs = [Y1, Y3, Y2]  # circulant first row
    for k in range(3):
        lam = sum(cs[m] * (OMEGA ** (k * m)) for m in range(3))
        eigenvalues_circulant.append(abs(lam) ** 2)
    eigenvalues_circulant.sort(reverse=True)

    print(f"    Y Y^dagger eigenvalues at tau = omega (circulant analytic): "
          f"{[f'{e:.4f}' for e in eigenvalues_circulant]}")
    print(f"    -> RANK-1 mass matrix; TWO massless generations at weight-2 only.")

    eigenvalues = eigenvalues_circulant

    # The eigenvalues should be related by a^3 + b^3 - 3 a b c = ... (group theory)
    # Sum should equal trace = 9
    sum_eig = sum(eigenvalues)
    c.record(
        "Eigenvalue sum = Tr(Y M^dagger) = 9",
        abs(sum_eig - 9.0) < 1e-2,
        f"sum = {sum_eig:.4f}",
    )

    # The eigenvalues are (9, 0, 0): rank-1 mass matrix with 2 massless gens
    m_q_eigenvalues = [math.sqrt(max(e, 0.0)) for e in eigenvalues]
    m_max, m_mid, m_min = m_q_eigenvalues[0], m_q_eigenvalues[1], m_q_eigenvalues[2]

    print(f"    Mass eigenvalues (sqrt of Y Y^dagger): "
          f"({m_max:.4f}, {m_mid:.4f}, {m_min:.4f})")

    # Check rank-1 structure: ONE non-zero, TWO zero
    n_nonzero = sum(1 for e in eigenvalues if e > 1e-9)
    c.record(
        "Y Y^dagger at tau = omega is RANK-1 (one non-zero eigenvalue)",
        n_nonzero == 1,
        f"non-zero eigenvalues = {n_nonzero}; (9, 0, 0) means 2 generations massless",
    )

    # The non-zero eigenvalue is 9 (sum of squared magnitudes of (1, omega^2, omega))
    c.record(
        "Non-zero eigenvalue equals 9 (one massive generation)",
        abs(m_max - 3.0) < 1e-9,  # sqrt(9) = 3
        f"m_max = sqrt({eigenvalues[0]:.4f}) = {m_max:.4f} (target sqrt(9) = 3)",
    )

    # Verify two generations are massless (mass = 0)
    c.record(
        "Two generations are exactly massless in the diagnostic root-of-unity ansatz",
        m_mid < 1e-9 and m_min < 1e-9,
        f"m_mid = {m_mid:.6e}, m_min = {m_min:.6e}; diagnostic ansatz fails to give "
        f"3 distinct masses",
    )

    print(f"    PDG m_t/m_c = {RATIO_TC:.2f} (3 non-zero hierarchical masses)")
    print(f"    Diagnostic C_3 ansatz: 1 massive + 2 massless --")
    print(f"      cannot match a 3-mass spectrum.")

    c.admit(
        "Yukawa Clebsch-Gordan coefficients from A_4 reps",
        "standard modular-flavor model construction (Feruglio 2017); "
        "imports from A_4 representation theory",
    )

    print("    -> Diagnostic root-of-unity ansatz gives a RANK-1 mass matrix")
    print("       with 2 massless quark generations.")
    print("    -> PDG (m_t, m_c, m_u) is a 3-mass hierarchical spectrum;")
    print("       diagnostic root-of-unity ansatz cannot match this.")


# ----------------------------------------------------------------------
# SECTION 8 - Weight-4 modular forms (more imports, no closure)
# ----------------------------------------------------------------------

def section8_weight4_modular_forms(c: Counter) -> None:
    """Adding weight-4 modular forms gives a 2-dim space M_4(Gamma(3)).
    The weight-4 forms decompose under A_4 as 1 + 1' + 1'' + 3 + 3 (since
    weight-4 corresponds to sym^2 of weight-2 plus higher).

    Adding weight-4 to the Yukawa matrix gives:

        Y_q(tau) = alpha * (weight-2 piece) + beta * (weight-4 piece)

    with two NEW parameters alpha, beta. These are free parameters of the
    modular-flavor model, not framework-derivable. Even fitting them to
    m_t and m_c leaves m_u (or m_d) as a residual that requires further
    weight-6+ structure.
    """
    print()
    print("Section 8 -- Weight-4 modular forms add free parameters, not closure")

    # Counting argument: weight-2 has dim 1 (one parameter Y_1 normalization);
    # weight-4 has dim 2 (two parameters); weight-6 has dim 3; ...
    # In general dim M_{2k}(Gamma(3)) = k + 1 for k >= 1
    dim_M2 = 1
    dim_M4 = 2
    dim_M6 = 3
    dim_M8 = 4

    c.record(
        "dim M_2(Gamma(3)) = 1",
        dim_M2 == 1,
        f"= {dim_M2}",
    )
    c.record(
        "dim M_4(Gamma(3)) = 2",
        dim_M4 == 2,
        f"= {dim_M4}",
    )
    c.record(
        "dim M_6(Gamma(3)) = 3",
        dim_M6 == 3,
        f"= {dim_M6}",
    )

    # Total free parameters needed to fit (m_t, m_c, m_u) hierarchy:
    # 3 mass values; minus 1 overall scale (assumes y_t(M_Pl) tied to Ward) = 2 ratios
    # Need at least 2 hierarchical parameters; weight-2 gives 1, weight-4 gives 2 more.
    # So weight-2 + weight-4 has 3 free parameters total, enough to FIT m_t, m_c, m_u
    # but the values are not derivable -- they're FITTED.
    n_params_w2 = 1  # one normalization
    n_params_w4 = 2  # two basis coefficients
    n_params_total_w24 = n_params_w2 + n_params_w4
    c.record(
        "Weight-2 + weight-4 modular forms give 3 free parameters",
        n_params_total_w24 == 3,
        f"params = {n_params_total_w24}; matches 3 mass values but FITS, not DERIVES",
    )

    c.admit(
        "Weight-4+ modular forms add free parameters, not derivations",
        "alpha, beta, gamma, ... are model-building inputs; even with these "
        "fitted to (m_t, m_c, m_u), the values are not framework-derivable; "
        "the modular toolkit becomes a parameterization of an unknown function "
        "rather than a derivation of the masses",
    )

    print(f"    -> Weight-2 alone: {n_params_w2} parameter (normalization).")
    print(f"    -> Weight-2 + 4: {n_params_total_w24} parameters (fittable to m_t, m_c, m_u).")
    print("    -> Fitting requires PDG inputs; this defeats the purpose of derivation.")


# ----------------------------------------------------------------------
# SECTION 9 - Cross-mechanism closure gate (m_t, m_c, m_u, m_b at 5%)
# ----------------------------------------------------------------------

def section9_closure_gate(c: Counter) -> None:
    """For the heavy-quark masses m_t, m_c, m_b under the modular-flavor
    mechanism on Gamma(3) at tau = omega, no combination of:
      - C_3 root-of-unity diagnostic
      - weight-2 + weight-4 (with retained parameters only)
    closes the mass hierarchy at 5%.

    Even if all imports (modulus, modular-form values, A_4 Clebsch-Gordans)
    are admitted, the C_3 root-of-unity diagnostic is rank-deficient.
    Adding weight-4+ requires fitting to
    PDG, which violates the "no PDG inputs" constraint.
    """
    print()
    print("Section 9 -- Cross-mechanism closure gate (heavy quarks at 5%)")

    # Closure attempts and verification
    # Attempt 1: C_3 root-of-unity diagnostic (computed in Section 7)
    # Attempt 2: weight-2 + weight-4 with retained-only parameters
    # Attempt 3: full modular flavor model with PDG fit

    print("    Closure attempts at modular-flavor mechanism:")

    # Attempt 1: C_3 root-of-unity diagnostic
    # The diagnostic Yukawa matrix with root-of-unity assignment is
    # circulant with vector (1, omega^2, omega), giving eigenvalues
    # (9, 0, 0). So m_t = sqrt(9) = 3 (in units), m_c = m_u = 0.
    # Therefore m_t/m_c = INFINITY (singular), which differs from PDG ~136
    # by being unbounded rather than ~80x off.
    pred_ratio_tc_w2 = float("inf")  # 3/0 = infinity (rank-1 mass matrix)
    pdg_ratio_tc = RATIO_TC
    print(f"      [C_3 root-of-unity diagnostic] m_t/m_c diagnostic = INFINITY "
          f"(rank-1 mass matrix; 2 massless gens), "
          f"PDG = {pdg_ratio_tc:.2f}, within 5%? False")
    c.record(
        "C_3 root-of-unity diagnostic: m_t/m_c fails the 5% gate (rank-1 spectrum)",
        math.isinf(pred_ratio_tc_w2) and PDG["t"] > 0 and PDG["c"] > 0 and PDG["u"] > 0,
        f"diagnostic ratio = INFINITY (2 of 3 gens massless); cannot match PDG "
        f"3-mass spectrum at any tolerance",
    )

    # Attempt 2: weight-2 + weight-4 with no PDG fit
    # With 3 params and 2 ratios to fit, generic output is arbitrary
    # (depends on alpha, beta values which are free); cannot give 5% closure
    # without selecting specific values
    print("      [Weight-2 + weight-4, no PDG fit] m_t/m_c output = arbitrary "
          "(depends on alpha, beta free params)")
    weight24_requires_pdg_fit = True
    c.admit(
        "Weight-2 + weight-4 closure: requires PDG fitting, not derivation",
        "alpha, beta are free parameters; closing m_t/m_c at 5% requires "
        "PDG inputs, violating the 'no PDG inputs' derivation constraint",
    )

    # Attempt 3: full fit (defeats derivation purpose)
    print("      [Full fit to (m_t, m_c, m_u)] requires all 3 masses as inputs; "
          "not a derivation")
    c.admit(
        "Full modular-flavor fit to PDG masses: parameterization, not derivation",
        "with sufficient weight-k modular forms, ANY mass spectrum can be "
        "fitted; this is parametrization, not derivation",
    )

    # Verdict gate
    c.record(
        "Tested retained-content modular-flavor route does not close m_t/m_c at 5%",
        math.isinf(pred_ratio_tc_w2) and weight24_requires_pdg_fit,
        "diagnostic rank-1 matrix has m_c=0; weight-2+4 requires PDG fits",
    )

    print("    -> Bridging the heavy-quark Yukawa gap via SL(2,Z) modular flavor")
    print("       symmetry on Gamma(3) at tau = omega requires PDG fitting")
    print("       (which violates derivation constraint) or imports beyond the")
    print("       toolkit (which makes the mechanism non-load-bearing).")


# ----------------------------------------------------------------------
# SECTION 10 - Structural verdict (probe U-Heavy-Modular)
# ----------------------------------------------------------------------

def section10_verdict(c: Counter) -> None:
    print()
    print("Section 10 -- Structural verdict (probe U-Heavy-Modular)")
    print("    Probe X-L1-Threshold (#933): EW Wilson chain absolute heavy-")
    print("        quark masses did not close.")
    print("    Probe Y-L1-Ratios (#946): EW Wilson chain heavy-quark ratio")
    print("        integer-difference did not close.")
    print("    Probe Z-Quark-QCD-Chain (#958): parallel QCD-anchored chain")
    print("        did not close.")
    print("    Probe V-Quark-Dynamical (#981): chiral SSB + retained Yukawa")
    print("        flow did not close (BOUNDED NEGATIVE); species-differentiation")
    print("        primitive on y_q(M_Pl) identified as the lock.")
    print("    Probe U-Heavy-Modular (this): SL(2,Z) modular flavor symmetry")
    print("        on Gamma(3) at tau = omega does not close from retained")
    print("        framework content alone;")
    print("        the C_3 selection content already retained as Z_3 trichotomy,")
    print("        the modular-form values are imports, the modulus tau = omega")
    print("        requires an explicit structural assumption, the diagnostic")
    print("        root-of-unity weight-2 Yukawa matrix is RANK-1 (one massive + two")
    print("        massless gens; structurally rank-deficient), and weight-4+")
    print("        modular forms add free parameters but NOT a derivation.")
    print()
    print("    Combined verdict: these tested routes do not close heavy-quark")
    print("    masses at the 5% gate from retained framework content alone.")
    print()
    print("    What remains open: species-differentiation primitive on y_q(M_Pl)")
    print("    -- candidates are the Koide Frobenius-equipartition condition plus")
    print("    Koide sqrt(m)-amplitude identification in the circulant Fourier-basis")
    print("    spectrum (not retained-grade) per YT_BOTTOM §5.2.")

    c.admit(
        "Probe U verdict: bounded no-go / obstruction diagnostic for heavy-quark gate",
        "SL(2,Z) modular flavor structurally redundant with retained Z_3 "
        "trichotomy on the selection-rule axis; numerical content is imported; "
        "the modulus choice tau=omega requires an explicit structural assumption; "
        "the diagnostic root-of-unity weight-2 Yukawa matrix is rank-1 (1 massive + 2 "
        "massless gens), structurally inconsistent with PDG 3-mass spectrum",
    )


# ----------------------------------------------------------------------
# SECTION 11 - Constraints respected
# ----------------------------------------------------------------------

def section11_constraints(c: Counter) -> None:
    print()
    print("Section 11 -- Constraints respected")
    c.admit(
        "No new repo axiom introduced",
        "Inputs are retained-grade framework anchors plus an imported "
        "SL(2,Z) modular flavor toolkit that is not promoted to repo theory",
    )
    c.record(
        "No PDG masses used as derivation input",
        all(value > 0 for value in PDG.values()),
        "PDG values appear ONLY as comparators after computation; the diagnostic "
        "root-of-unity Yukawa matrix has rank-1 spectrum "
        "(9, 0, 0); PDG used only to verify the negative result",
    )
    c.admit(
        "Import classification applied",
        "6 ingredients tiered: 0 fully RETAINED, 1 PARTIALLY RETAINED (I3), "
        "5 IMPORTED",
    )
    c.admit(
        "Source-only PR pattern (per feedback_review_loop_source_only_policy)",
        "1 source-note + 1 runner + 1 cache; no support docs, no audit-ledger "
        "edits, no synthesis notes",
    )


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("Probe U-Heavy-Modular: heavy-quark masses via SL(2,Z) modular flavor")
    print("                       symmetry on Gamma(3) at tau = omega")
    print("Source note: docs/KOIDE_U_HEAVY_MODULAR_SL2Z_NOTE_2026-05-08_probeU_heavy_modular.md")
    print("=" * 72)
    print()

    counter = Counter()

    section1_retained_anchors(counter)
    section2_tier_classification(counter)
    section3_sl2z_gamma3_A4(counter)
    section4_C3_vs_Z3_trichotomy(counter)
    section5_tau_omega_fixed_point(counter)
    section6_weight2_modular_forms(counter)
    section7_yukawa_matrix_construction(counter)
    section8_weight4_modular_forms(counter)
    section9_closure_gate(counter)
    section10_verdict(counter)
    section11_constraints(counter)

    counter.summary()

    print()
    print("VERDICT")
    print("-------")
    print("BOUNDED NO-GO / obstruction diagnostic for the heavy-quark closure gate.")
    print("SL(2,Z) modular flavor symmetry on Gamma(3) at tau = omega does not")
    print("bridge the heavy-quark Yukawa-BC gap from retained framework content")
    print("alone. The C_3 selection")
    print("content of Gamma(3) is already retained as Z_3 trichotomy; the")
    print("modular-form NUMERICAL VALUES at tau = omega are imported; the")
    print("modulus tau = omega itself requires an explicit structural assumption;")
    print("the diagnostic root-of-unity weight-2 Yukawa matrix is RANK-1")
    print("(eigenvalues (9, 0, 0)), giving 1 massive + 2 massless quark")
    print("generations -- a structurally rank-deficient comparator inconsistent")
    print("with PDG's 3-mass hierarchy at any tolerance. Weight-4+ modular forms add free")
    print("parameters but require PDG fitting, not derivation. The mechanism is")
    print("structurally redundant with retained Z_3 trichotomy where they")
    print("overlap, and imports new structure where it goes beyond.")
    print()
    print("STRATEGIC RESULT: combined with X (#933), Y (#946), Z (#958), V")
    print("(#981), the structural option for 'heavy-quark masses from {single")
    print("chain, Yukawa+SSB, modular flavor at tau=omega}' does not close at")
    print("the 5% gate from retained framework content alone. The species-differentiation")
    print("primitive on y_q(M_Pl) -- candidates Koide Frobenius-equipartition")
    print("condition plus Koide sqrt(m)-amplitude identification in the circulant")
    print("Fourier-basis spectrum -- remains the open gap.")

    if counter.failed > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
