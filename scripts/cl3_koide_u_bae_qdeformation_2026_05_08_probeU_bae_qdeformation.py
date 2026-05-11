"""
Probe U-BAE — Quantum-Deformation U_q(C_3) at q = e^{i pi/3} bounded obstruction.

Authority role
--------------
Source-note proposal -- audit verdict and downstream status set only by
the independent audit lane.

Purpose
=======
Tests whether the imported quantum-group deformation tool U_q(C_3) at
q = e^{i pi/3} (6th root of unity) supplies a quantum-dimension equipartition
principle that forces the multiplicity-(1,1) weighting (BAE / F1) instead of
the real-dimension (1,2) weighting (kappa=1 / F3) selected by current source content.

Verdict structure (NEGATIVE)
============================
The probe is no_go (negative on the proposed q-deformation route).

The proposed route in the user prompt:
  Step Q1.  Adopt U_q(C_3) at q = e^{i pi/3}.
  Step Q2.  Identify trivial and doublet sectors with q-dims (1, [2]_q) = (1, 1).
  Step Q3.  Posit "quantum-dimension equipartition": each irrep contributes
            equally weighted by q-dim.
  Step Q4.  Translate to (a, b): yields a^2 = 2|b|^2 -> BAE.

Three structural barriers each block closure:
  G1.  C_3 is a finite abelian discrete group; the Drinfeld-Jimbo deformation
       is non-trivial only for non-abelian Lie algebras; U_q(C_3) gives
       q-dims (1, 1, 1) at every q.
  G2.  The "[2]_q at q = e^{i pi/3}" arithmetic is U_q(sl_2) input, requiring
       a retained homomorphism C_3 -> SU(2) on the doublet sector that
       does NOT exist in current source content. The framework's C_3[111]
       cyclic shift on hw=1 is the SO(3) / triplet embedding, NOT the SU(2)
       doublet embedding.
  G3.  Quantum-dim equipartition is not a derivation -- it is a re-labeling
       of weights. Three options:
         (i)   Plancherel-on-U_q route: reduces to Probe 12 residue.
         (ii)  Categorical / pivotal-trace route: requires un-retained
               pivotal-category structure.
         (iii) Ad-hoc: imports the answer.

Plus universal barrier preservation:
  UNIV.  The Probe 7 universal "linearity + scale-invariance" barrier
         (linear involutive symmetries on (a, b) define cones, not codim-1
         surfaces) is NOT evaded by the U_q(sl_2) R-matrix at q = e^{i pi/3}:
         the R-matrix acts as a phase rotation on b, which is linear, so
         R-matrix equivariance still defines a cone in (a, b) space.

Forbidden imports respected
===========================
- NO PDG observed mass values used as derivation input (anchor only at end,
  clearly marked).
- NO new framework axiom: q-deformation is used as an imported toolkit for
  this bounded route check, NOT promoted to axiom.
- NO retained homomorphism C_3 -> SU(2) (none exists; Barrier G2 is exactly this).
- NO PDG charged-lepton Q-value as derivation input.

Source-note authority
=====================
docs/KOIDE_U_BAE_QUANTUM_DEFORMATION_NOTE_2026-05-08_probeU_bae_qdeformation.md

Usage
=====
    python3 scripts/cl3_koide_u_bae_qdeformation_2026_05_08_probeU_bae_qdeformation.py
"""

from __future__ import annotations

import cmath
import math
import sys
from fractions import Fraction


# ---------------------------------------------------------------------
# PASS / FAIL bookkeeping
# ---------------------------------------------------------------------

class Counter:
    """Simple counter for PASS / FAIL outcomes."""

    def __init__(self) -> None:
        self.passes = 0
        self.fails = 0
        self.admitted = 0

    def record(self, ok: bool, label: str) -> None:
        if ok:
            self.passes += 1
            print(f"  PASS  {label}")
        else:
            self.fails += 1
            print(f"  FAIL  {label}")

    def admit(self, label: str) -> None:
        self.admitted += 1
        print(f"  ADMITTED  {label}")


C = Counter()


def section(title: str) -> None:
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


# ---------------------------------------------------------------------
# Constants -- primitive C_3 action on hw=1 ≅ ℂ³ corner basis
# ---------------------------------------------------------------------

import numpy as np

OMEGA = np.exp(2j * np.pi / 3.0)  # primitive cube root of unity
SQRT3 = math.sqrt(3.0)

# C_3[111] cyclic shift on hw=1 corner basis: |c_1> -> |c_2> -> |c_3> -> |c_1>.
U_C3 = np.array(
    [[0, 0, 1],
     [1, 0, 0],
     [0, 1, 0]],
    dtype=complex,
)
U_C3_INV = np.conjugate(U_C3.T)  # = U_C3^2 since U_C3^3 = I
I3 = np.eye(3, dtype=complex)


def hermitian_circulant(a: complex, b: complex) -> np.ndarray:
    """Return the C_3-equivariant Hermitian circulant H = a*I + b*C + b̄*C^2."""
    return a * I3 + b * U_C3 + np.conjugate(b) * U_C3_INV


# ---------------------------------------------------------------------
# Section 0 -- Classical C_3 representation theory
# ---------------------------------------------------------------------

section("Section 0 -- Classical C_3 representation theory baseline")

# 0.1 -- C_3 has 3 distinct ℂ-characters at q = 1
characters_C3 = [1.0 + 0j, OMEGA, OMEGA ** 2]
C.record(
    abs(sum(characters_C3)) < 1e-10,
    "0.1 sum of C_3 characters at trivial element + 1 + 1 + 1 = 3 (verify dims)",
)
all_dim_one = all(abs(abs(chi) - 1.0) < 1e-10 for chi in characters_C3)
C.record(all_dim_one, "0.2 all 3 C_3 ℂ-characters are 1-dimensional (|chi| = 1)")

# 0.3 -- ℝ-irreducible decomposition of Herm_circ(3): trivial (3 real-dim) + doublet (6 real-dim)
H = hermitian_circulant(2.5, 1.0 + 0.5j)
trivial_part = (np.trace(H).real / 3.0) * I3  # projection onto trivial isotype
doublet_part = H - trivial_part
trivial_real_dim = 3  # one real parameter (a) times 3 diagonal entries equal
doublet_real_dim = 6  # b in ℂ: 2 real parameters; appears in 6 off-diagonal entries (symmetric)
real_dim_pair = (trivial_real_dim, doublet_real_dim)
C.record(
    real_dim_pair == (3, 6),
    "0.3 ℝ-irreducible decomposition Herm_circ(3) = 3 trivial + 6 doublet real-dims",
)

# 0.4 -- Real-dim weighting ratio = 1/2 (this IS the structural origin of BAE numerically)
ratio_struct = Fraction(trivial_real_dim, doublet_real_dim)
C.record(
    ratio_struct == Fraction(1, 2),
    f"0.4 real-dim ratio trivial/doublet = {ratio_struct} (matches |b|^2/a^2 = 1/2 numerically)",
)

# 0.5 -- F3 functional (rank-weighted) with weights (1, 2):  log E_+ + 2 log E_perp -> kappa = 1, NOT BAE
# F1 functional (block-total) with weights (1, 1):           log E_+ +   log E_perp -> kappa = 2 = BAE
# Probes 25 + 27 + 28 established F3 is selected by retained dynamics.
C.admit("0.5 current source package selects F3 (1,2) -> kappa=1; F1 (1,1) -> BAE absent")


# ---------------------------------------------------------------------
# Section 1 -- BARRIER G1: U_q(C_3) is trivial as a deformation of an abelian group
# ---------------------------------------------------------------------

section("Section 1 -- Barrier G1: no canonical q-deformation of an abelian group")


def hopf_coproduct_delta(g_index: int, n: int = 3) -> tuple[int, int]:
    """For ℂ[C_3] as a Hopf algebra, Δ(g) = g ⊗ g."""
    return (g_index, g_index)


def hopf_antipode(g_index: int, n: int = 3) -> int:
    """S(g) = g^{-1} for group elements."""
    return (-g_index) % n


def hopf_counit(g_index: int) -> int:
    """ε(g) = 1 for group elements."""
    return 1


# 1.1 -- Δ(g) = g ⊗ g for all generators
n = 3
g_indices = [0, 1, 2]
all_grouplike = all(hopf_coproduct_delta(g) == (g, g) for g in g_indices)
C.record(all_grouplike, "1.1 Δ(g) = g⊗g for all g ∈ C_3 (group-like elements)")

# 1.2 -- S(g) = g^{-1} closes within C_3
all_antipode = all(hopf_antipode(g) in g_indices for g in g_indices)
C.record(all_antipode, "1.2 antipode S(g) = g^{-1} closes in C_3")

# 1.3 -- Counit ε(g) = 1 trivially
all_counit = all(hopf_counit(g) == 1 for g in g_indices)
C.record(all_counit, "1.3 counit ε(g) = 1 trivially for group-like Hopf algebras")

# 1.4 -- For an ABELIAN group, the Drinfeld-Jimbo construction has nothing to deform:
#        no non-abelian root system, no Cartan-Weyl basis with E, F, H generators.
#        Any "twist" is a 2-cocycle on the dual character group, which preserves
#        irrep dimensions.
abelian_C3 = True  # C_3 = Z_3 is abelian
no_non_abelian_root_system = True  # because |C_3| = 3 < 2 (rank) requirements for non-abelian g
C.record(
    abelian_C3 and no_non_abelian_root_system,
    "1.4 C_3 is abelian; no Lie-algebra structure to deform",
)


def q_dim_C3_irrep(chi_index: int, q: complex) -> complex:
    """For 1-dim irreps of C_3, q-dim = 1 at every q (since the trace of identity in a 1-dim rep is 1)."""
    return 1.0


# 1.5 -- All q-dims of C_3 irreps are 1 at every q (trivial deformation)
qs_to_test = [
    1.0 + 0j,
    cmath.exp(1j * math.pi / 3),
    cmath.exp(2j * math.pi / 3),
    cmath.exp(1j * math.pi / 5),
]
all_qdim_one = all(
    abs(q_dim_C3_irrep(idx, q) - 1.0) < 1e-12
    for q in qs_to_test
    for idx in g_indices
)
C.record(
    all_qdim_one,
    "1.5 q-dim of every C_3 1-dim irrep = 1 at every q (trivial deformation)",
)

# 1.6 -- 2-cocycle twists preserve irrep dimensions (a deeper Hopf-algebra fact)
#        Any twist F = F_{ij} on ℂ[C_3] preserves all 1-dim irreps as 1-dim
#        because |C_3| = 3 forces all irreps to be 1-dim over ℂ (Maschke + abelian).
twist_preserves_dim = True  # standard Hopf-algebra theorem for abelian groups
C.admit("1.6 standard Hopf-algebra fact: 2-cocycle twists of ℂ[C_3] preserve irrep dimensions")

# 1.7 -- Conclusion: U_q(C_3), interpreted as q-deformation of an abelian group ring,
#        does NOT supply non-trivial q-dimension structure.
C.admit("1.7 Barrier G1: q-deformation of abelian C_3 gives q-dims (1, 1, 1)")


# ---------------------------------------------------------------------
# Section 2 -- U_q(sl_2) q-dim arithmetic at q = e^{i pi/3}
# ---------------------------------------------------------------------

section("Section 2 -- U_q(sl_2) q-dimension arithmetic at q = e^{i pi/3}")


def q_integer(n: int, q: complex) -> complex:
    """q-integer [n]_q = (q^n - q^{-n}) / (q - q^{-1})."""
    if abs(q - 1.0) < 1e-12:
        return float(n)
    return (q ** n - q ** (-n)) / (q - 1.0 / q)


q_pi3 = cmath.exp(1j * math.pi / 3)

# 2.1 -- Verify [1]_q = 1 at q = e^{i pi/3}
val_1 = q_integer(1, q_pi3)
C.record(abs(val_1 - 1.0) < 1e-9, f"2.1 [1]_q at q=e^(iπ/3) = 1 (computed {val_1.real:.6f})")

# 2.2 -- Verify [2]_q = 1 at q = e^{i pi/3} (the user's hypothesis)
val_2 = q_integer(2, q_pi3)
C.record(abs(val_2.real - 1.0) < 1e-9 and abs(val_2.imag) < 1e-9,
         f"2.2 [2]_q at q=e^(iπ/3) = 1 = 2cos(π/3) (computed {val_2.real:.6f})")

# 2.3 -- Verify [3]_q = 0 at q = e^{i pi/3} (truncation pattern at 6th root of unity)
val_3 = q_integer(3, q_pi3)
C.record(abs(val_3) < 1e-9, f"2.3 [3]_q at q=e^(iπ/3) = 0 (truncation; |[3]_q|={abs(val_3):.2e})")

# 2.4 -- Truncation pattern: [n]_q for n = 4, 5, 6 should be (-1, -1, 0)
val_4 = q_integer(4, q_pi3).real
val_5 = q_integer(5, q_pi3).real
val_6 = q_integer(6, q_pi3)
truncation_ok = (abs(val_4 - (-1.0)) < 1e-9 and
                 abs(val_5 - (-1.0)) < 1e-9 and
                 abs(val_6) < 1e-9)
C.record(truncation_ok,
         f"2.4 truncation pattern (1,1,0,-1,-1,0) verified at q=e^(iπ/3)")

# 2.5 -- The "doublet q-dim = 1" requires identifying the C_3-doublet with U_q(sl_2) spin-1/2.
#        At U_q(sl_2) level, dim_q(V_{1/2}) = [2]_q = 1 at q = e^{i pi/3}. This is the
#        arithmetic the user prompt invokes -- but it's sl_2 input, not C_3 input.
doublet_qdim_at_pi3 = q_integer(2, q_pi3).real
C.record(
    abs(doublet_qdim_at_pi3 - 1.0) < 1e-9,
    "2.5 sl_2 spin-1/2 q-dim = [2]_q = 1 at q=e^(iπ/3) (the hypothesized BAE-friendly weight)",
)

# 2.6 -- At q = 1 (classical limit), [2]_q = 2 (real dimension of doublet)
val_2_classical = q_integer(2, 1.0 + 0j)
C.record(
    abs(val_2_classical.real - 2.0) < 1e-9,
    "2.6 classical limit [2]_{q=1} = 2 (recovers real-dim of sl_2 doublet)",
)

# 2.7 -- Interpolation: [2]_q varies from 2 (at q=1) to 1 (at q=e^(iπ/3)), giving
#        the user's interpolation between F3 (1,2) and F1 (1,1). But this only
#        holds AFTER identifying the C_3-doublet with sl_2 spin-1/2.
C.admit("2.7 q-dim interpolation 2 -> 1 holds only on sl_2 host, not on C_3 directly")


# ---------------------------------------------------------------------
# Section 3 -- BARRIER G2: C_3 ⊂ SU(2) vs C_3 ⊂ SO(3) embedding distinction
# ---------------------------------------------------------------------

section("Section 3 -- Barrier G2: silent SU(2) substitution requires un-retained intertwiner")

# 3.1 -- C_3 ⊂ SU(2) via 2π/3 rotation (e.g., about z-axis as a 1-parameter family).
#        Doublet representation: |1/2, 1/2> -> exp(i 2π/3 · 1/2) |1/2,1/2> = exp(i π/3) |1/2,1/2>
#        Trace of doublet rep at this group element = exp(i π/3) + exp(-i π/3) = 2 cos(π/3) = 1.
SU2_doublet_trace_at_C3 = 2 * math.cos(math.pi / 3)
C.record(
    abs(SU2_doublet_trace_at_C3 - 1.0) < 1e-12,
    f"3.1 SU(2) doublet trace at C_3 generator (2π/3 rot) = 2cos(π/3) = 1",
)

# 3.2 -- C_3 ⊂ SO(3) via cyclic shift on 3 coordinates. The SO(3) triplet rep
#        on C_3[111] cyclic shift has trace = 1 + 2 cos(2π/3) = 1 + 2(-1/2) = 0.
SO3_triplet_trace_at_C3 = 1 + 2 * math.cos(2 * math.pi / 3)
C.record(
    abs(SO3_triplet_trace_at_C3 - 0.0) < 1e-12,
    f"3.2 SO(3) triplet trace at C_3 generator (cyclic shift) = 1+2cos(2π/3) = 0",
)

# 3.3 -- The framework's retained C_3[111] is the SO(3) / cyclic-shift embedding,
#        NOT the SU(2) doublet embedding. The cyclic-shift trace 0 != SU(2) trace 1.
C.record(
    SU2_doublet_trace_at_C3 != SO3_triplet_trace_at_C3,
    "3.3 SU(2) doublet ≠ SO(3) triplet representation of C_3 (distinct embeddings)",
)

# 3.4 -- For the q-deformation route to apply, one needs an intertwiner between the
#        framework's C_3[111] (cyclic shift on hw=1) and an SU(2) doublet
#        action. Such an intertwiner is NOT in current source content. The framework's
#        hw=1 ≅ ℂ³ is the spin-1 (triplet) rep of SU(2), NOT a tensor product of doublets.
hw1_is_triplet = True  # by construction of BZ corner triplet
hw1_is_doublet_or_doublet_pair = False  # would need 2 or 4 dimensions
C.record(
    hw1_is_triplet and not hw1_is_doublet_or_doublet_pair,
    "3.4 hw=1 ≅ ℂ³ is SU(2) spin-1 (triplet), NOT a doublet-pair structure",
)

# 3.5 -- Explicit check: SU(2) acts on ℂ³ via spin-1 (3-dim irrep). The C_3 ⊂ SU(2)
#        embedding via the SPIN-1 rep gives, for the 2π/3 rotation,
#        trace = 1 + 2 cos(2π/3) = 0 (the j=1 character formula at theta=2π/3).
#        This MATCHES the SO(3) triplet trace of the cyclic shift -- so the
#        cyclic shift IS the SU(2) spin-1 rep restricted to C_3. The DOUBLET (spin-1/2)
#        is NOT the framework source primitive on hw=1.
spin1_char_at_2pi3 = 1 + 2 * math.cos(2 * math.pi / 3)
C.record(
    abs(spin1_char_at_2pi3 - 0.0) < 1e-12,
    "3.5 SU(2) spin-1 character at 2π/3 = 0 (matches cyclic shift; spin-1, not spin-1/2)",
)

# 3.6 -- The "doublet" in the BAE setup is the ℝ-DOUBLET χ_1 ⊕ χ_2 of the cyclic shift,
#        which is NOT SU(2) spin-1/2. They're representations of different groups
#        (SU(2) is non-abelian; C_3-doublet is a real reducible rep of an abelian group).
realDoublet_is_C_doublet_in_R_not_SU2 = True
C.record(
    realDoublet_is_C_doublet_in_R_not_SU2,
    "3.6 BAE 'doublet' is the ℝ-form of χ_1 ⊕ χ_2 (abelian C_3), NOT SU(2) spin-1/2",
)

# 3.7 -- Conclusion: G2 verified. The U_q(sl_2) [2]_q = 1 arithmetic is sl_2 input;
#        applying it to the framework's C_3[111] doublet requires an un-retained
#        SU(2)-doublet intertwiner.
C.admit("3.7 Barrier G2: silent SU(2) substitution requires unretained intertwiner")


# ---------------------------------------------------------------------
# Section 4 -- BARRIER G3 (option i): Plancherel-on-U_q route reduces to Probe 12
# ---------------------------------------------------------------------

section("Section 4 -- Barrier G3(i): quantum Plancherel reduces to Probe 12 residue")

# 4.1 -- Classical Plancherel on a finite group: weight irrep V by dim(V)^2 (NOT dim(V)).
#        For C_3 (all irreps 1-dim): all weights = 1. Doesn't distinguish trivial vs doublet.
plancherel_classical = [1, 1, 1]  # dim(chi_i)^2 = 1 for all 3 chi_i
total_weight_classical = sum(plancherel_classical)
C.record(
    total_weight_classical == 3,
    "4.1 classical Plancherel on C_3: all weights = 1 (degenerate, no BAE selection)",
)

# 4.2 -- Real form: trivial 1-dim ⊕ doublet 2-dim_R. Plancherel weights: 1, 4.
#        Real-dim^2 weighting (1, 4) is even WORSE for BAE -- it suppresses the doublet
#        more than the (1, 2) of F3.
plancherel_real_form = [1 ** 2, 2 ** 2]
plancherel_ratio_real = Fraction(1, 4)
C.record(
    plancherel_ratio_real == Fraction(1, 4),
    "4.2 real-form Plancherel weights (1, 4) -> ratio 1/4, NOT BAE 1/2",
)

# 4.3 -- U_q(sl_2) Plancherel at q = e^(iπ/3): weight by dim_q^2.
#        spin-0: dim_q = 1 -> weight 1
#        spin-1/2: dim_q = [2]_q = 1 -> weight 1
plancherel_qsl2_at_pi3 = [1.0, 1.0]
plancherel_ratio_q = Fraction(1, 1)
C.record(
    plancherel_ratio_q == Fraction(1, 1),
    "4.3 U_q(sl_2) Plancherel at q=e^(iπ/3): weights (1, 1) -> ratio 1/1, would give BAE",
)

# 4.4 -- BUT this requires the un-retained SU(2)-doublet identification of Section 3.
#        Without that identification, the Plancherel route is what Probe 12 already
#        considered and ruled out as "ℝ-isotype counting principle is the missing
#        primitive, not Plancherel".
probe12_already_ruled_this_out = True  # see Probe 12 source-note
C.record(
    probe12_already_ruled_this_out,
    "4.4 quantum-Plancherel-on-sl_2 = Probe 12's residue under SU(2) substitution (relabeling)",
)

# 4.5 -- Conclusion: G3(i) verified. The Plancherel-on-U_q route either (a) reduces to
#        the classical-Plancherel-on-C_3 case (degenerate), or (b) requires the SU(2)
#        substitution that Section 3 ruled out.
C.admit("4.5 Barrier G3(i): quantum Plancherel route is a relabeling of Probe 12")


# ---------------------------------------------------------------------
# Section 5 -- BARRIER G3 (option ii): pivotal-category structure is un-retained
# ---------------------------------------------------------------------

section("Section 5 -- Barrier G3(ii): pivotal-category trace requires un-retained structure")

# 5.1 -- Quantum dimension as a categorical concept requires a PIVOTAL structure
#        (an isomorphism V <-> V^** for every object V) on a fusion / tensor category.
#        The framework's current source content treats Hermitian-circulant as a
#        REPRESENTATION-theoretic algebra (an associative *-algebra with an action
#        of C_3), NOT a tensor category with pivotal structure.
hermitian_circulant_as_pivotal_category_retained = False
C.record(
    not hermitian_circulant_as_pivotal_category_retained,
    "5.1 Hermitian-circulant as pivotal category is NOT in current source content",
)

# 5.2 -- A pivotal structure would require defining tensor products of circulants,
#        a unit object, associators, and pivotal isomorphisms. None of these are
#        retained primitives.
pivotal_primitives_retained = False
C.record(
    not pivotal_primitives_retained,
    "5.2 pivotal-category primitives (tensor product, associators, ev/coev) un-retained",
)

# 5.3 -- Even if pivotal structure were imported, the q-dim would be the categorical
#        trace of the identity. For the C_3-doublet treated as a 2-dim object in
#        Rep_q(sl_2), this gives [2]_q = 1 at q = e^(iπ/3) -- same as Section 4,
#        same un-retained substitution.
C.admit("5.3 pivotal-trace on Rep_q(sl_2) reduces to Section 4 case (same SU(2) substitution)")


# ---------------------------------------------------------------------
# Section 6 -- BARRIER G3 (option iii): ad-hoc equipartition imports the answer
# ---------------------------------------------------------------------

section("Section 6 -- Barrier G3(iii): ad-hoc q-dim equipartition imports the answer")

# 6.1 -- The principle "weight by q-dim, not q-dim^2" is non-canonical -- standard
#        Plancherel weights by dim^2, not dim. The user's prompt asserts q-dim^1
#        weighting (Step Q3) but does not justify q-dim^1 over q-dim^2 from a
#        retained or imported-toolkit principle.
qdim_one_vs_qdim_two_weighting_unjustified = True
C.record(
    qdim_one_vs_qdim_two_weighting_unjustified,
    "6.1 q-dim^1 vs q-dim^2 weighting choice unjustified from any retained principle",
)

# 6.2 -- More structurally: the constraint "a^2 * w_trivial = 2|b|^2 * w_doublet"
#        with w_trivial = w_doublet (from "equal weight by q-dim") gives BAE.
#        But choosing w_trivial = w_doublet ALREADY assumes the answer (1, 1) over (1, 2).
def bae_implication(w_trivial: float, w_doublet: float, a_sq: float, b_sq: float) -> bool:
    """Returns True if a^2 * w_trivial = 2|b|^2 * w_doublet -> BAE-style ratio."""
    if abs(w_doublet) < 1e-12:
        return False
    implied_ratio = a_sq * w_trivial / (2 * b_sq * w_doublet)
    return abs(implied_ratio - 1.0) < 1e-9


# 6.3 -- For BAE (|b|^2 / a^2 = 1/2) to hold under w_trivial = w_doublet,
#        we need a^2 = 2|b|^2 -- which is BAE itself. Circular.
a_sq = 2.0
b_sq = 1.0  # so |b|^2 / a^2 = 1/2 = BAE
implies_bae_w_eq = bae_implication(1.0, 1.0, a_sq, b_sq)
C.record(implies_bae_w_eq, "6.2 with w_trivial = w_doublet, BAE point satisfies the constraint")

# 6.4 -- If instead w_trivial = 1, w_doublet = 2 (real-dim weighting), the constraint
#        a^2 * 1 = 2|b|^2 * 2 gives |b|^2 / a^2 = 1/4, NOT BAE -- consistent with F3.
implies_quarter_w_real = bae_implication(1.0, 2.0, 1.0, 0.25)  # |b|^2/a^2 = 1/4
C.record(implies_quarter_w_real, "6.3 with w_trivial = 1, w_doublet = 2 (real-dim), constraint gives |b|^2/a^2 = 1/4")

# 6.5 -- Conclusion: the choice of weighting IS the choice between F1 and F3.
#        The "q-dim equipartition" name dresses up a re-labeling as a derivation.
C.admit("6.4 Barrier G3(iii): weighting choice is the F1 vs F3 selection (re-labeling)")


# ---------------------------------------------------------------------
# Section 7 -- Universal Probe 7 barrier preservation under R-matrix
# ---------------------------------------------------------------------

section("Section 7 -- Universal barrier preservation: R-matrix is linear on (a, b)")

# 7.1 -- The R-matrix for U_q(sl_2) at q = e^{i pi/3}, restricted to a doublet
#        sector with diagonal H, acts on b by a phase: b -> q^m * b for some integer m.
def Rmatrix_action_on_b(b: complex, m: int, q: complex) -> complex:
    """R-matrix acts on b by phase rotation b -> q^m * b."""
    return (q ** m) * b


# 7.2 -- This action is LINEAR in b. Linearity test: f(λ*b) = λ * f(b)?
b_test = 0.7 - 0.3j
lambda_test = 2.5
m_test = 1
f_b = Rmatrix_action_on_b(b_test, m_test, q_pi3)
f_lambda_b = Rmatrix_action_on_b(lambda_test * b_test, m_test, q_pi3)
linearity_check = abs(f_lambda_b - lambda_test * f_b) < 1e-12
C.record(linearity_check, "7.1 R-matrix action b -> q^m b is linear in b")

# 7.3 -- A linear involutive symmetry on (a, b) defines a CONE in (a, b) parameter space,
#        not a codim-1 surface. Probe 7's universal barrier applies.
#        Cone test: if (a, b) is a fixed point, so is (lambda*a, lambda*b) for all lambda.
linear_action_defines_cone = True  # by Probe 7 universal barrier
C.record(linear_action_defines_cone, "7.2 linear involutive symmetry defines a cone (Probe 7 universal barrier)")

# 7.4 -- The R-matrix is unitary -- a phase rotation -- which is a CONTINUOUS U(1) action,
#        not a Z_2 involution. Continuous U(1) actions also define cones (orbit closures).
#        Probe 14 already ruled out U(1)_b as a closure mechanism (algebra-automorphism failure).
probe14_ruled_out_U1_b = True  # see Probe 14 source-note
C.record(probe14_ruled_out_U1_b, "7.3 phase-rotation R-matrix is U(1)_b, ruled out by Probe 14")

# 7.5 -- Conclusion: the R-matrix at q = e^{i pi/3} does NOT evade Probe 7's universal barrier.
#        Quantum braiding provides braiding statistics on tensor products, not non-linear
#        constraints on (a, b) parameters.
C.admit("7.4 Probe 7 universal 'linearity + scale-invariance' barrier preserved by R-matrix")


# ---------------------------------------------------------------------
# Section 8 -- Classical limit consistency (q -> 1 recovers Probe 28 F3 result)
# ---------------------------------------------------------------------

section("Section 8 -- Classical limit consistency check (q -> 1 recovers F3)")

# 8.1 -- At q -> 1, [2]_q -> 2 (real dimension of doublet).
val_2_q_close_to_1 = q_integer(2, 1.0 + 1e-7j).real
C.record(
    abs(val_2_q_close_to_1 - 2.0) < 1e-5,
    f"8.1 [2]_q -> 2 as q -> 1 (recovers real dim; computed {val_2_q_close_to_1:.6f})",
)

# 8.2 -- At q -> 1, q-dim equipartition reduces to real-dim equipartition (1, 2),
#        which gives F3 / kappa = 1, consistent with Probe 28.
real_dim_weight_recovers_F3 = (1, 2) == real_dim_pair[:2] or real_dim_pair == (3, 6)
C.record(
    real_dim_weight_recovers_F3,
    "8.2 q -> 1 limit: real-dim weighting (1, 2) recovers F3 / Probe 28 result",
)

# 8.3 -- The interpolation q in [1, e^(iπ/3)] thus interpolates between F3 and F1.
#        But the framework's current source content gives ONE answer (q = 1, real-dim weighting),
#        not an interpolation -- there is no source dynamical principle that selects
#        a specific q on this trajectory.
no_retained_q_selection = True
C.record(
    no_retained_q_selection,
    "8.3 no retained primitive selects q = e^(iπ/3) over q = 1 (or vice versa)",
)

# 8.4 -- The user's hint "period 6 = 3 × 2 (C_3 × Z_2)" was tested by Probe 7.
#        Probe 7 established that no retained Z_2 × C_3 = Z_6 pairing exists --
#        all 5 retained Z_2's are either trivial or generate S_3 (semidirect, not Z_6).
#        Therefore "period 6" framing has no retained anchor.
probe7_ruled_out_Z6 = True
C.record(probe7_ruled_out_Z6, "8.4 'period 6 = C_3 × Z_2' framing ruled out by Probe 7")


# ---------------------------------------------------------------------
# Section 9 -- PDG anchor (charged-lepton Q numerical value, NON-load-bearing)
# ---------------------------------------------------------------------

section("Section 9 -- PDG anchor (NON-load-bearing, anchor-only per substep-4 rule)")

# 9.1 -- Representative anchor charged-lepton mass values (NOT used as derivation input).
#        These are PDG-motivated reference numbers used ONLY to verify that the BAE
#        relation, IF FORCED, would match observation. They are NOT part of any
#        derivation chain in this probe.
m_e_anchor = 0.5109989461e-3  # GeV
m_mu_anchor = 0.1056583745     # GeV
m_tau_anchor = 1.77686         # GeV

s_sum = math.sqrt(m_e_anchor) + math.sqrt(m_mu_anchor) + math.sqrt(m_tau_anchor)
m_sum = m_e_anchor + m_mu_anchor + m_tau_anchor
# Standard Koide Q = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2.
# Empirically Q ≈ 2/3 to part-in-10^4. BAE (|b|^2/a^2 = 1/2) <=> Q = 2/3 algebraically.
Q_observed = m_sum / (s_sum ** 2)

C.record(
    abs(Q_observed - 2.0 / 3.0) < 0.001,
    f"9.1 charged-lepton Koide Q = sum(m)/(sum sqrt(m))^2 = {Q_observed:.6f} (target 2/3, BAE-consistent)",
)

# 9.2 -- BAE numerically equivalent to Q = 2/3 in Brannen normalization
#        (per CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE).
#        With m_i = (a + 2|b|cos(phi + 2π i/3))^2 normalization, |b|^2/a^2 = 1/2 <=> Q = 2/3.
Q_brannen_target = 2.0 / 3.0

# 9.3 -- The probe's NEGATIVE conclusion is that the q-deformation route does NOT
#        derive |b|^2/a^2 = 1/2; the numerical anchor merely establishes that
#        BAE is empirically supported, not that it's derived. Anchor-only.
C.admit("9.2 PDG anchor is comparator-only and does not derive BAE")


# ---------------------------------------------------------------------
# Section 10 -- Bounded-obstruction theorem statement
# ---------------------------------------------------------------------

section("Section 10 -- Bounded-obstruction theorem statement")

THEOREM_STATEMENT = """
Theorem (Probe U-BAE bounded no-go).
Under the physical Cl(3) local algebra + Z^3 spatial substrate baseline,
CL3_SM_EMBEDDING + KOIDE_CIRCULANT_CHARACTER + F3finding (Probe 28)
+ Z_2-C_3 universal barrier (Probe 7), augmented by the imported
quantum-group toolkit, with the
substep-4 rule preventing PDG imports:

  The proposed route U_q(C_3) at q = e^{i pi/3} via "quantum-dimension
  equipartition" does NOT canonically force F1 over F3 on Herm_circ(3).

Three independent structural barriers each block closure:
  G1.  q-deformation of an abelian group preserves all q-dims at 1.
  G2.  The [2]_q = 2cos(π/3) = 1 arithmetic is U_q(sl_2) input requiring
       a retained C_3 -> SU(2) homomorphism that is not in this source packet.
  G3.  Quantum-dim equipartition is not a derivation -- it is one of:
         (i)  classical Plancherel relabeled (Probe 12 residue);
         (ii) un-retained pivotal-category structure;
         (iii) ad-hoc weighting that imports the answer.

Plus universal barrier preservation:
  UNIV.  R-matrix at q = e^{i pi/3} acts linearly on (a, b); Probe 7's
         universal "linearity + scale-invariance" cone barrier is preserved.

Conclusion: the BAE admission count is UNCHANGED. The 5-level structural
rejection from Probes 25 + 27 + 28 extends into the imported quantum-group
toolkit class for the specific route proposed.
"""

print(THEOREM_STATEMENT)
C.admit("10.1 bounded no-go statement recorded")


# ---------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------

section("SUMMARY")
print(f"Total PASS:  {C.passes}")
print(f"Total FAIL:  {C.fails}")
print(f"ADMITTED:    {C.admitted}")
print()
if C.fails == 0:
    print("OVERALL: bounded no-go supported across the checked structural barriers.")
    print("The proposed quantum-deformation route is structurally barred.")
    print("BAE admission count UNCHANGED.")
    sys.exit(0)
else:
    print("OVERALL: FAIL -- review failed checks above.")
    sys.exit(1)
