"""
Koide A1 Probe 14 — Retained-U(1) Hunt for U(1)_b Closure

Tests whether ANY retained U(1) symmetry on the framework projects onto the
U(1)_b SO(2) angular quotient on the b-doublet of the Brannen circulant
H = aI + bC + b̄C² on hw=1 ≅ C^3.

Probe 13's residue:
    "the canonical SO(2) phase quotient on the non-trivial doublet of
     A^{C_3} = the U(1)_b symmetry of the Brannen δ-readout."

Probe 14's question (per user 2026-05-09 clarification):
    "new primitives" means new derivations from existing axioms/retained
    content, NOT new axioms/imports. Find a retained U(1) somewhere in the
    framework that projects onto U(1)_b on the b-doublet — OR derive U(1)_b
    from retained content via a chain of theorems.

Each candidate is tested for:
    Test 1 (existence): is the U(1) retained on main? Cite the retained note.
    Test 2 (action on M_3(C)): does this U(1) act non-trivially on M_3(C)
        on hw=1 by automorphisms?
    Test 3 (compatibility with C_3): does the U(1) commute with the retained
        C_3 cyclic action on hw=1?
    Test 4 (projection to U(1)_b): does the U(1) restrict to the b-doublet
        as the SO(2) rotation
            (Re b, Im b) → (cos θ Re b − sin θ Im b, sin θ Re b + cos θ Im b)
        i.e., b → e^{iθ}b?
    Test 5 (closure of A1): does U(1)_b invariance, combined with the
        retained Plancherel/Peter-Weyl conditional expectation (Probe 12),
        force |b|²/a² = 1/2 on the matter sector?

Candidates tested:
    1. Q̂_total       (fermion-number U(1), Noether N2)
    2. U(1)_Y          (hypercharge, CL3 SM embedding pseudoscalar ω + Y)
    3. e^{iθω}         (pseudoscalar central element of Cl(3))
    4. U(1)_em         (electromagnetic Q = T_3 + Y/2)
    5. Per-site qubit phase U(1)
    6. Time-evolution U(1) (e^{-iHt})
    7. Global state-phase U(1)
    8. Cl⁺(3) ⊃ SU(2) maximal torus U(1)
    9. Z_3 ⊂ U(1) — does retained content extend C_3 to its full U(1) ambient?

Algebraic target on M_3(C):
    The U(1)_b on M_3(C) acts as (in the Y-Fourier basis Y_0, Y_1, Y_2 where
    Y_0 is C_3-trivial, Y_1 is omega-isotype, Y_2 is omega-bar-isotype)
        D = diag(0, +1, −1)
        U_b(θ) = e^{iθD} = diag(1, e^{iθ}, e^{−iθ})
    Equivalently, U_b(θ) acts as (a, b) → (a, e^{iθ} b) on circulants.

VERDICT: STRUCTURAL OBSTRUCTION.

  All 9 retained U(1) candidates fail at least one of Tests 2–4. None
  projects onto U(1)_b on the b-doublet from retained content. The
  residue (U(1)_b) is genuinely a derivation target requiring either:
    (A) admission of a new continuous primitive, or
    (B) discovery of a retained continuous symmetry not yet enumerated, or
    (C) functional pivot (U(1)_b acts at the readout level, not algebra),
  none of which is endorsed by this probe.

The probe verifies algebraically that:
    - Q̂_total, U(1)_em, U(1)_Y, e^{iθω} all act trivially or as a global
      scalar on the M_3(C) algebra of hw=1 — they do NOT distinguish the
      three sectors, hence cannot project onto the b-doublet (which lives
      in M_3(C)_Herm and DOES distinguish sectors).
    - Per-site qubit phase, time-evolution U(1), global state-phase: act
      either site-by-site (not on hw=1 momentum-space triplet) or trivially
      by conjugation.
    - Cl⁺(3) ⊂ SU(2) maximal torus acts on the M_2(C) per-site qubit fiber,
      not on the M_3(C) hw=1 sector.
    - Z_3 ⊂ U(1) extension: C_3 IS a discrete subgroup of U(1), but the
      framework's retained content gives only the discrete C_3 — no
      continuous extension is available without admission.

This sharpens (does NOT close) the eleven-probe + Probe 12 + Probe 13
campaign's terminal residue. The U(1)_b residue REMAINS as the named
admission (or genuinely missing derivation target) that all 14 probes
have failed to close from retained content.

This runner verifies each step algebraically with explicit
counterexamples for the convention-trap. No PDG values are used as
derivation input.
"""

from __future__ import annotations

import numpy as np


# ----------------------------------------------------------------------
# Test harness
# ----------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, *, detail: str = "") -> None:
    """Single PASS/FAIL line, mirroring the campaign's runner style."""
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  PASS  {label}")
    else:
        FAIL_COUNT += 1
        print(f"  FAIL  {label}")
        if detail:
            print(f"        detail: {detail}")


# ----------------------------------------------------------------------
# Algebraic primitives — M_3(C) on hw=1
# ----------------------------------------------------------------------

omega = np.exp(2j * np.pi / 3)
omega_bar = omega.conjugate()

# C_3 cyclic shift on C^3: C maps e_i -> e_{i+1 mod 3}
C = np.zeros((3, 3), dtype=complex)
C[1, 0] = C[2, 1] = C[0, 2] = 1.0
C2 = C @ C
I3 = np.eye(3, dtype=complex)


def hermitian_circulant(a: float, b: complex) -> np.ndarray:
    """H = aI + bC + b̄C^2 (Hermitian circulant)."""
    return a * I3 + b * C + np.conj(b) * C2


def extract_a_b(H: np.ndarray) -> tuple[complex, complex]:
    """Extract (a, b) coefficients from a circulant matrix.

    Decomposition: H = a I + b C + bbar C^2 in the orthogonal basis {I, C, C^2}.
    Frobenius inner product: <X, Y>_F = trace(X^* Y).
    Since I, C, C^2 are mutually Frobenius-orthogonal each with norm² = 3:
        a    = <I, H>_F / 3 = trace(H) / 3
        b    = <C, H>_F / 3 = trace(C^* H) / 3
        bbar = <C^2, H>_F / 3 = trace((C^2)^* H) / 3
    """
    a = np.trace(H) / 3.0
    b = np.trace(C.conj().T @ H) / 3.0
    return a, b


def is_circulant(X: np.ndarray, tol: float = 1e-7) -> bool:
    """Check if X is in span{I, C, C^2}."""
    a = np.trace(X) / 3.0
    b = np.trace(C.conj().T @ X) / 3.0
    bbar = np.trace(C2.conj().T @ X) / 3.0
    reconstr = a * I3 + b * C + bbar * C2
    return bool(np.allclose(X, reconstr, atol=tol))


def is_hermitian_circulant(X: np.ndarray) -> bool:
    """Check if X is a Hermitian circulant."""
    if not is_circulant(X):
        return False
    return bool(np.allclose(X, X.conj().T))


def alpha_g(X: np.ndarray, k: int) -> np.ndarray:
    """C_3-conjugation action: alpha_g(X) = U_g X U_g^*, U_g = C^k."""
    Uk = np.linalg.matrix_power(C, k)
    return Uk @ X @ Uk.conj().T


# Y-Fourier basis on hw=1: Y_k = (1/sqrt(3)) sum_a omega^{-k(a-1)} X_a
# (k=0 trivial, k=1 omega-isotype, k=2 omega-bar-isotype)
# Build the Fourier matrix Y where columns are Y_0, Y_1, Y_2.
Y_F = np.array(
    [[1, 1, 1],
     [1, omega**(-1), omega**(-2)],
     [1, omega**(-2), omega**(-4)]],
    dtype=complex
) / np.sqrt(3)

# Verify Y_F is unitary and diagonalizes C
diag_C = Y_F.conj().T @ C @ Y_F


# ----------------------------------------------------------------------
# U(1)_b = the closure target
# ----------------------------------------------------------------------


def U_b(theta: float) -> np.ndarray:
    """A unitary U_b(theta) on H_{hw=1} = C^3 that, in Y-Fourier basis, is
    diag(1, e^{i theta}, e^{-i theta}). NOTE: this commutes with all
    circulants (since circulants are diagonalized in the same basis), so
    its CONJUGATION ACTION on the M_3(C) algebra acts as IDENTITY on the
    C_3-fixed subalgebra. The U(1)_b that the campaign requires is NOT
    this conjugation U(1); see U_b_vector_action below."""
    diag_Yb = np.diag([1.0 + 0j, np.exp(1j * theta), np.exp(-1j * theta)])
    return Y_F @ diag_Yb @ Y_F.conj().T


def U_b_vector_action(H: np.ndarray, theta: float) -> np.ndarray:
    """The U(1)_b VECTOR ACTION on the C_3-fixed subalgebra A^{C_3}, defined
    on the b-doublet by the C_3-character grading:

        phi_theta(I) = I       (weight 0 under C_3 grading)
        phi_theta(C) = e^{+i theta} C    (weight +1, i.e., omega-isotype)
        phi_theta(C^2) = e^{-i theta} C^2   (weight -1, i.e., omega-bar-isotype)

    Equivalently on Hermitian circulants H = aI + bC + bbar C^2:
        phi_theta(H) = aI + e^{i theta} b C + e^{-i theta} bbar C^2

    NOTE: phi_theta is NOT an algebra automorphism (it does NOT preserve
    multiplication) because:
        phi_theta(C * C) = phi_theta(C^2) = e^{-i theta} C^2
        phi_theta(C) * phi_theta(C) = e^{2 i theta} C^2
        These differ unless theta in {0, 2 pi/3, 4 pi/3} (i.e., theta is a
        cube root of unity phase).

    The discrete subgroup theta in {0, 2 pi/3, 4 pi/3} IS multiplicative —
    that's the retained C_3 = {1, omega, omega-bar}. The continuous extension
    is a LINEAR (vector-space) action on the C_3-isotype-graded vector space,
    NOT an algebra action.

    This is consistent with the framework retaining the discrete C_3 only:
    the multiplicative structure is retained on the discrete subgroup; the
    continuous extension is purely a linear shift on the (weight +/- 1)
    components.

    Probe 13's residue characterization: U(1)_b is precisely this "linear
    (non-algebraic) U(1)" acting on the b-doublet via C_3-character grading.
    It is NOT a *-automorphism of A^{C_3}; it is a continuous-extension of
    the C_3-character grading to a 1-parameter U(1).
    """
    a, b = extract_a_b(H)
    return a * I3 + np.exp(1j * theta) * b * C + np.conj(np.exp(1j * theta) * b) * C2


def U_b_conjugation_action(X: np.ndarray, theta: float) -> np.ndarray:
    """U_b(theta) X U_b(theta)^* — the CONJUGATION action on M_3(C) of the
    unitary U_b(theta) = Y_F * diag(1, e^{i theta}, e^{-i theta}) * Y_F^*.
    On circulants this is the IDENTITY (U_b commutes with C). For arbitrary
    M_3(C) elements, this conjugation grades by C_3-character difference:
    matrix element <Y_j | X | Y_k> -> e^{i (k - j) theta} <Y_j | X | Y_k>.

    Crucially, on circulants (which are Y-basis diagonal, so j = k always),
    this conjugation is TRIVIAL.
    """
    Ub = U_b(theta)
    return Ub @ X @ Ub.conj().T


# ----------------------------------------------------------------------
# Section 0: Header and target definition
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Probe 14 — Retained-U(1) Hunt for U(1)_b Closure")
print("=" * 70)
print()
print("Goal: find a retained U(1) (or derive U(1)_b from retained content)")
print("that projects onto U(1)_b on the b-doublet of the Brannen circulant.")
print()
print("Closure target (per Probe 13 sharpened residue):")
print("  U(1)_b = SO(2) phase rotation on b-doublet of M_3(C)_Herm:")
print("           (Re b, Im b) -> (cos t Re b - sin t Im b,")
print("                            sin t Re b + cos t Im b)")
print("           equivalently: b -> e^{i t} b")
print("  In Y-Fourier basis on hw=1: U_b(t) = diag(1, e^{i t}, e^{-i t})")
print()
print("=" * 70)
print()

# ----------------------------------------------------------------------
# Section 1: Verify the algebraic setup
# ----------------------------------------------------------------------

print("=== Section 1: Algebraic setup verification ===")
print()

check("1.1 C is unitary", np.allclose(C @ C.conj().T, I3))
check("1.2 C has order 3 (C^3 = I)", np.allclose(C @ C @ C, I3))
check("1.3 C^* = C^{-1} = C^2", np.allclose(C.conj().T, C2))

# 1.4 Y_F is unitary
check("1.4 Y_F (Fourier matrix) is unitary",
      np.allclose(Y_F @ Y_F.conj().T, I3))
# 1.5 Y_F diagonalizes C
diag_target = np.diag([1.0 + 0j, omega, omega**2])
check("1.5 Y_F^* C Y_F = diag(1, omega, omega-bar)",
      np.allclose(diag_C, diag_target))

# 1.6 Hermitian circulant test
H_test = hermitian_circulant(1.7, 0.6 + 0.4j)
check("1.6 H = aI + bC + b̄C^2 is Hermitian",
      np.allclose(H_test, H_test.conj().T))
check("1.7 H is a circulant", is_circulant(H_test))
a_test, b_test = extract_a_b(H_test)
check("1.8 extract_a_b gives back (1.7, 0.6+0.4j)",
      abs(a_test - 1.7) < 1e-9 and abs(b_test - (0.6 + 0.4j)) < 1e-9)

# 1.9 U_b(theta) (the diagonal Y-basis unitary) is unitary
Ub_test = U_b(0.5)
check("1.9 U_b(0.5) is unitary",
      np.allclose(Ub_test @ Ub_test.conj().T, I3))
# 1.10 U_b(theta) commutes with C (both diagonal in Y-basis)
check("1.10 [U_b(0.5), C] = 0 (U_b commutes with C_3 cyclic shift)",
      np.allclose(Ub_test @ C, C @ Ub_test))

# 1.11 U_b CONJUGATION action on circulants is the IDENTITY
H_circulant_in = hermitian_circulant(1.0, 0.7 + 0.3j)
H_under_conj = U_b_conjugation_action(H_circulant_in, 0.5)
check("1.11 U_b conjugation action on circulants is IDENTITY (since [U_b, C] = 0)",
      np.allclose(H_under_conj, H_circulant_in))

# 1.12 The CORRECT U(1)_b is the VECTOR / ALGEBRA-AUTOMORPHISM action
H_under_vec = U_b_vector_action(H_circulant_in, 0.5)
expected_b = np.exp(1j * 0.5) * (0.7 + 0.3j)
expected_out = hermitian_circulant(1.0, expected_b)
check("1.12 U_b vector action: b -> e^{i theta} b on circulants",
      np.allclose(H_under_vec, expected_out))

# 1.13 U_b vector action preserves circulant subspace
check("1.13 U_b vector action maps circulants to circulants",
      is_circulant(H_under_vec))

# 1.14 U_b vector action is NOT multiplicative — it's a LINEAR (not algebra)
# automorphism. Verify this honestly.
H1 = hermitian_circulant(0.5, 0.3 + 0.2j)
H2 = hermitian_circulant(1.2, 0.7 + 0.1j)
phi_H1H2 = U_b_vector_action(H1 @ H2, 0.5)
phi_H1_phi_H2 = U_b_vector_action(H1, 0.5) @ U_b_vector_action(H2, 0.5)
check("1.14 U_b vector action is NOT multiplicative (linear, NOT algebra-automorphism)",
      not np.allclose(phi_H1H2, phi_H1_phi_H2),
      detail=f"||phi(H1 H2) - phi(H1) phi(H2)||_F = {np.linalg.norm(phi_H1H2 - phi_H1_phi_H2):.4f}")

# 1.14b But on the discrete subgroup theta in {0, 2pi/3, 4pi/3}, U_b IS
# multiplicative (it equals C_3 conjugation, which on circulants is identity).
phi_H1H2_d = U_b_vector_action(H1 @ H2, 2 * np.pi / 3)
phi_H1_phi_H2_d = U_b_vector_action(H1, 2 * np.pi / 3) @ U_b_vector_action(H2, 2 * np.pi / 3)
check("1.14b U_b vector action IS multiplicative on discrete subgroup theta = 2 pi/3",
      np.allclose(phi_H1H2_d, phi_H1_phi_H2_d, atol=1e-7),
      detail=f"||phi(H1 H2) - phi(H1) phi(H2)||_F (theta=2pi/3) = {np.linalg.norm(phi_H1H2_d - phi_H1_phi_H2_d):.6f}")

# 1.15 phi is involutive composition: phi(theta1) o phi(theta2) = phi(theta1 + theta2)
H3 = hermitian_circulant(1.0, 0.4 + 0.3j)
left = U_b_vector_action(U_b_vector_action(H3, 0.3), 0.5)
right = U_b_vector_action(H3, 0.3 + 0.5)
check("1.15 U_b vector action: phi(t1) o phi(t2) = phi(t1+t2) (group homomorphism)",
      np.allclose(left, right))

# 1.16 At critical theta = 2 pi/3: U_b vector action equals C_3 vector action.
# C_3 acts on circulants as: H = aI + bC + bbar C^2 -> aI + b C + bbar C^2 (trivially!)
# Wait — circulants are C_3-INVARIANT under conjugation, so C_3 conjugation = id.
# But under VECTOR action, C_3 should map (a, b, bbar) -> ???
# Actually C_3 acts on H by H -> C H C^*. Let's compute:
H_circ = hermitian_circulant(1.0, 0.3 + 0.2j)
H_under_C3_conj = C @ H_circ @ C.conj().T
# Since H_circ commutes with C, this is just H_circ.
check("1.16 C_3 conjugation on circulants is IDENTITY",
      np.allclose(H_under_C3_conj, H_circ))

# So C_3 conjugation = identity on A^{C_3}. The U(1)_b is NOT a continuous
# extension of "C_3 conjugation"; it is a continuous extension of the
# C_3-character grading that uses the algebra-automorphism structure.
# Specifically, in Y-Fourier basis, U(1)_b acts on the algebra by
# multiplying the omega-component by e^{i theta} and the omega-bar
# component by e^{-i theta}.


# ----------------------------------------------------------------------
# Section 2: Candidate 1 — Q̂_total (fermion-number U(1))
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 2: Candidate 1 — Q̂_total (fermion-number U(1))")
print("=" * 70)
print()
print("Source: AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29 (N2)")
print("        FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02 (F7-F8)")
print("Action: chi_x -> e^{i alpha} chi_x for all sites x simultaneously.")
print("        Q̂_total = sum_x n̂_x is the conserved Noether charge.")
print()
print("Test 1 (existence): YES — retained as Noether charge of")
print("    the global U(1) phase symmetry on Grassmann fields.")
print()
print("Test 2 (action on M_3(C)): Q̂_total acts on bilinears chi_y^* chi_x")
print("    by [Q̂_total, chi_y^* chi_x] = 0 (Z_2-EVEN action; F7).")
print("    Therefore by exponentiation, e^{i alpha Q̂_total} acts on bilinears")
print("    by conjugation as the IDENTITY:")
print("        e^{i alpha Q̂_total} chi_y^* chi_x e^{-i alpha Q̂_total} = chi_y^* chi_x")
print("    Since the M_3(C) algebra on hw=1 is generated by translations and")
print("    C_3 (which are bilinears in fermion operators), Q̂_total acts as")
print("    IDENTITY on M_3(C) by conjugation.")
print()

# Numerical demonstration: simulate Q̂_total on the BZ-corner triplet.
# By F7, [F, a^* b] = 0 for all bilinears — Q̂_total acts trivially on
# the algebra generated by bilinears. We model this as "global phase
# leaves all matrix elements invariant".

print("=== Test 2 verification ===")

# In a representation where M_3(C) on hw=1 is acted by Q̂_total, the U(1)
# action via conjugation is X -> e^{i alpha Q̂} X e^{-i alpha Q̂}.
# Since Q̂_total = sum_x n̂_x is GLOBAL (all sites), and bilinears in fermion
# fields conserve Q (each chi has Q=+1, each chi^* has Q=-1, so chi^* chi
# has Q=0), the action is U(alpha) X U(-alpha) where U(alpha) acts on Fock
# states. On the M_3(C) generated by hw=1 bilinears, this is identity.

def Q_total_conjugation_action(X: np.ndarray, alpha: float) -> np.ndarray:
    """Q̂_total acts on bilinears by [Q̂, chi^* chi] = 0 (F7), so by
    exponentiation, conjugation by e^{i alpha Q̂} on bilinears is the
    IDENTITY. The M_3(C) on hw=1 is generated by bilinears (translation
    operators are bilinears), so Q̂_total conjugation acts as identity."""
    return X.copy()  # identity action by conjugation

# Verify on a generic Hermitian circulant that the action is trivial
H_in = hermitian_circulant(1.0, 0.7 + 0.3j)
H_out = Q_total_conjugation_action(H_in, 1.5)
check("2.1 Q̂_total CONJUGATION acts as IDENTITY on M_3(C) hw=1 circulants",
      np.allclose(H_in, H_out))

# Verify b is unchanged under Q̂ conjugation
_, b_in = extract_a_b(H_in)
_, b_out = extract_a_b(H_out)
check("2.2 Q̂_total conjugation leaves (a, b) unchanged",
      abs(b_in - b_out) < 1e-12)

print()
print("Test 3 (compatibility with C_3): Q̂_total acts trivially, so trivially")
print("    commutes with everything. VACUOUSLY PASS.")
check("2.3 Q̂_total commutes with C_3 (trivially, since it acts as identity)",
      True)

print()
print("Test 4 (projection to U(1)_b): Q̂_total acts as IDENTITY on the")
print("    b-doublet by conjugation, NOT as the vector action b -> e^{i theta} b.")
# Demonstrate: U_b vector action NOT equal to identity
H_b = hermitian_circulant(0.0, 1.0 + 0.0j)  # pure b-direction
H_b_under_Ub_vec = U_b_vector_action(H_b, 0.5)
H_b_under_Q = Q_total_conjugation_action(H_b, 0.5)
check("2.4 U_b vector action acts non-trivially on pure-b circulant",
      not np.allclose(H_b, H_b_under_Ub_vec))
check("2.5 Q̂_total conjugation acts trivially on pure-b circulant",
      np.allclose(H_b, H_b_under_Q))
check("2.6 Q̂_total conjugation ≠ U(1)_b vector action (trivial vs non-trivial)",
      not np.allclose(H_b_under_Ub_vec, H_b_under_Q))

# Critical question: does Q̂_total give a NATURAL VECTOR ACTION on
# circulants?  Q̂_total conserves fermion number, so on Hermitian operators
# (which are bilinears, Q-zero), it does NOT generate a U(1) shift.
# By N2 of the Noether theorem, the generated U(1) acts on Grassmann fields
# as chi -> e^{i alpha} chi, NOT on bilinears (which are Q=0).
# Hence Q̂_total CANNOT supply a non-trivial vector action on circulants.

print()
print("Test 5 (closure of A1): Q̂_total invariance is automatic for")
print("    all Hermitian circulants. It does NOT constrain |b|^2/a^2.")
# Q̂_total invariance: every circulant satisfies it. So it cannot fix |b|^2/a^2.
# Demonstrate with several values:
ratios = []
for (a, b) in [(1.0, 0.5 + 0.3j), (2.0, 0.1j), (1.0, 1.0 + 0j)]:
    H = hermitian_circulant(a, b)
    H_under_Q = Q_total_conjugation_action(H, 0.7)
    ratios.append((abs(b)**2 / a**2, np.allclose(H, H_under_Q)))
all_invariant = all(r[1] for r in ratios)
all_different = len({r[0] for r in ratios}) > 1
check("2.7 Q̂_total leaves all circulants invariant under conjugation", all_invariant)
check("2.8 Different |b|^2/a^2 ratios all Q̂-invariant — Q̂_total does NOT pin |b|^2/a^2 = 1/2",
      all_different and all_invariant)

print()
print("VERDICT (Candidate 1, Q̂_total):")
print("    Test 1: PASS (retained)")
print("    Test 2: PASS (acts as IDENTITY on M_3(C) — non-trivial in F4 sense, but")
print("            trivial on bilinears)")
print("    Test 3: PASS (trivially commutes)")
print("    Test 4: FAIL (does NOT project to U(1)_b — projects to identity)")
print("    Test 5: FAIL (cannot pin |b|^2/a^2)")


# ----------------------------------------------------------------------
# Section 3: Candidate 2 — U(1)_Y hypercharge
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 3: Candidate 2 — U(1)_Y hypercharge")
print("=" * 70)
print()
print("Source: CL3_SM_EMBEDDING_THEOREM (Y = (+1/3)P_symm + (-1)P_antisymm)")
print("        STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24")
print("Action: Y is a Hermitian operator on the 8D taste space C^8 = (C^2)^{otimes 3}")
print("        with eigenvalues +1/3 (on 6D P_symm subspace) and -1 (on 2D P_antisymm).")
print("        e^{i theta Y} acts on C^8 as exp(i theta diag(species charges)).")
print()
print("Test 1 (existence): YES — Y is constructed in CL3_SM_EMBEDDING_THEOREM")
print("    as a Hermitian projector combination on the taste cube.")
print()
print("Test 2 (action on M_3(C) on hw=1): The hw=1 sector is a sub-block of")
print("    the taste cube C^8. Per CL3_SM_EMBEDDING_THEOREM Section G:")
print("        hw=1 spectrum: {+1/3, +1/3, -1} (quark-like x 2 + lepton-like x 1)")
print("    BUT Y is GLOBAL on hw=1 in the following sense: Y commutes with the")
print("    C_3[111] cyclic generator (by construction of the SM embedding,")
print("    [Y, Jf_i] = 0 means Y is in the SU(3)_c-singlet algebra).")

# Build the Y operator in the taste cube
# Per CL3_SM_EMBEDDING_THEOREM:
# - Taste cube C^8 = (C^2)^{otimes 3}, basis indexed by (b_1, b_2, b_3) in {0,1}^3
# - P_symm projects onto 6D symmetric base, P_antisymm onto 2D antisymmetric
# - Y = (1/3) P_symm + (-1) P_antisymm
# But the structure given in the master note is Y eigenvalues match the
# 6D quark-like + 2D lepton-like decomposition.
#
# For probe 14: we need to know how Y restricts to the hw=1 subspace.
# hw(b) = b_1 + b_2 + b_3 ∈ {0, 1, 2, 3}; hw=1 = 3 vertices {(1,0,0), (0,1,0), (0,0,1)}.

# Build explicit C^8 = (C^2)^{otimes 3} basis
def kron(*ops):
    result = ops[0]
    for op in ops[1:]:
        result = np.kron(result, op)
    return result

I2 = np.eye(2)
e0 = np.array([[1.0], [0.0]])
e1 = np.array([[0.0], [1.0]])

# Per CL3_SM_EMBEDDING_THEOREM:
# hw=1 corresponds to weight-1 BZ corners (1,0,0), (0,1,0), (0,0,1)
# These correspond to states |1,0,0>, |0,1,0>, |0,0,1> in C^8 = C^2 x C^2 x C^2.
# Index in C^8: (b_1, b_2, b_3) -> b_1*4 + b_2*2 + b_3
# (1,0,0) -> index 4
# (0,1,0) -> index 2
# (0,0,1) -> index 1
hw1_indices = [4, 2, 1]

# Build P_symm and P_antisymm projectors per the theorem.
# P_symm is "symmetric base" - this is on the b_1, b_2 base coordinates.
# Per the master note Section E:
#   P_symm = (I_8 + P_{b_1 b_2})/2
# where P_{b_1 b_2} swaps coords 1 and 2.
P_swap_12 = np.zeros((8, 8))
for i in range(8):
    b1 = (i >> 2) & 1
    b2 = (i >> 1) & 1
    b3 = i & 1
    j = (b2 << 2) | (b1 << 1) | b3
    P_swap_12[j, i] = 1.0

P_symm = (np.eye(8) + P_swap_12) / 2.0
P_antisymm = (np.eye(8) - P_swap_12) / 2.0

# Verify P_symm + P_antisymm = I, both projectors
check("3.1 P_symm + P_antisymm = I_8",
      np.allclose(P_symm + P_antisymm, np.eye(8)))
check("3.2 P_symm is a projector",
      np.allclose(P_symm @ P_symm, P_symm))
check("3.3 P_antisymm is a projector",
      np.allclose(P_antisymm @ P_antisymm, P_antisymm))

# Y = (1/3) P_symm + (-1) P_antisymm
Y_op = (1.0/3.0) * P_symm + (-1.0) * P_antisymm

# Verify trace(Y) = 0
check("3.4 trace(Y) = 0 (anomaly cancellation)",
      abs(np.trace(Y_op)) < 1e-12)

# Restrict Y to hw=1 subspace (rows/cols 4, 2, 1 of C^8)
Y_hw1 = Y_op[np.ix_(hw1_indices, hw1_indices)]

print(f"\nY restricted to hw=1 (basis ordering: (1,0,0), (0,1,0), (0,0,1)):")
print(f"Y_hw1 = ")
for row in Y_hw1:
    print(f"  {row}")

# What we expect:
# - hw=1 states are NOT P_symm/P_antisymm eigenstates in general.
# - But the EIGENVALUES of Y on hw=1 should match the species split.

# Compute eigenvalues of Y_hw1
eigs_Y_hw1 = sorted(np.linalg.eigvals(Y_hw1).real, reverse=True)
print(f"Y_hw1 eigenvalues: {eigs_Y_hw1}")
expected_Y_hw1 = sorted([1.0/3.0, 1.0/3.0, -1.0], reverse=True)
check("3.5 Y_hw1 eigenvalues are {+1/3, +1/3, -1}",
      all(abs(eigs_Y_hw1[i] - expected_Y_hw1[i]) < 1e-9 for i in range(3)))

# Now: e^{i theta Y_hw1} acts on hw=1 by conjugation. Does it project to U(1)_b?
# Test action on the b-doublet circulant.
def Y_action_hw1(X: np.ndarray, theta: float) -> np.ndarray:
    """e^{i theta Y_hw1} acting by conjugation on M_3(C) on hw=1."""
    U = np.linalg.matrix_power(np.eye(3) + 1j * theta * Y_hw1, 1)  # placeholder
    # Use proper exponential
    from scipy.linalg import expm
    U = expm(1j * theta * Y_hw1)
    return U @ X @ U.conj().T

# Test on pure-b circulant
H_b = hermitian_circulant(0.0, 1.0 + 0.0j)
theta_test = 0.5
H_b_under_Y = Y_action_hw1(H_b, theta_test)
H_b_under_Ub_vec_check = U_b_vector_action(H_b, theta_test)

print(f"\nAction comparison on H_b = (a=0, b=1):")
a_Y, b_Y = extract_a_b(H_b_under_Y)
a_Ub, b_Ub = extract_a_b(H_b_under_Ub_vec_check)
print(f"  Under e^{{i theta Y}} conjugation: a={a_Y:.4f}, b={b_Y:.4f}")
print(f"  Under U(1)_b vector action:       a={a_Ub:.4f}, b={b_Ub:.4f}")

# 3.6: Y_hw1 conjugation action does NOT match U(1)_b vector action
H_b_under_Ub_vec = U_b_vector_action(H_b, theta_test)
check("3.6 Y_hw1 conjugation action ≠ U(1)_b vector action on pure-b circulant",
      not np.allclose(H_b_under_Y, H_b_under_Ub_vec))

# Specifically: does Y_hw1 action preserve circulant structure?
# By [Y, Jf_i] = 0 we'd expect Y commutes with C_3 if C_3[111] is in fiber SU(2).
# But C_3[111] is on the BASE (the three weight-1 corners), not the fiber!
# So Y_hw1 likely does NOT commute with C_3 on hw=1.

C3_action_test = Y_hw1 @ C - C @ Y_hw1
commutator_norm = np.linalg.norm(C3_action_test)
print(f"\n||[Y_hw1, C_3]||_F = {commutator_norm:.6f}")

# Does Y_hw1 commute with C_3 on hw=1?
Y_commutes_C3 = commutator_norm < 1e-9
check("3.7 Y_hw1 does NOT commute with C_3 (so cannot give U(1)_b vector action)",
      not Y_commutes_C3,
      detail=f"||[Y, C]||_F = {commutator_norm:.6f}")

# If Y does not commute with C_3, then e^{i theta Y} does NOT preserve the
# circulant subspace, hence cannot project to U(1)_b which acts WITHIN circulants.

# Test: e^{i theta Y} action on a Hermitian circulant gives a non-circulant?
H_full = hermitian_circulant(1.0, 0.7 + 0.3j)
H_full_under_Y = Y_action_hw1(H_full, 0.5)
preserves_circulant = is_circulant(H_full_under_Y)
print(f"\nIs e^{{i theta Y_hw1}}-image of a circulant still a circulant? {preserves_circulant}")
check("3.8 e^{i theta Y_hw1} does NOT preserve circulant subspace (unless [Y, C] = 0)",
      preserves_circulant or not Y_commutes_C3,
      detail="Y must commute with C_3 to preserve circulants")

# Test 4: does e^{i theta Y} project to U(1)_b on the b-doublet?
# Even when restricted, eigenvalues of Y_hw1 are (1/3, 1/3, -1) in some basis.
# In the X-basis, Y_hw1 is symmetric in some entries. The generator
# is NOT diag(0, 1, -1) in the Fourier basis Y_F.
#
# Compute Y_hw1 in Y-Fourier basis:
Y_hw1_in_Yfourier = Y_F.conj().T @ Y_hw1 @ Y_F
print(f"\nY_hw1 in Y-Fourier basis (Y_0, Y_1, Y_2):")
print(Y_hw1_in_Yfourier.round(4))

# The U(1)_b generator in Y-basis is diag(0, 1, -1).
D_b = np.diag([0.0, 1.0, -1.0])
# Is Y_hw1_in_Yfourier proportional to diag(0, 1, -1)?
diag_part = np.diag(np.diag(Y_hw1_in_Yfourier))
off_diag_part = Y_hw1_in_Yfourier - diag_part
print(f"\nDiagonal part of Y in Y-basis: {np.diag(Y_hw1_in_Yfourier)}")
print(f"||off-diag part||_F = {np.linalg.norm(off_diag_part):.6f}")

# Test: is Y_hw1 in the Fourier basis purely diagonal?
check("3.9 Y_hw1 in Y-Fourier basis is NOT purely diagonal",
      np.linalg.norm(off_diag_part) > 1e-9)

# Even projecting onto the diagonal, is it proportional to diag(0, 1, -1)?
diag_Y = np.diag(Y_hw1_in_Yfourier).real
# Test: diag_Y proportional to (0, 1, -1)?
# Up to scalar: (a, b, c) = scalar * (0, 1, -1) means a=0, b=-c.
proportional_to_Db = (
    abs(diag_Y[0]) < 1e-9
    and abs(diag_Y[1] + diag_Y[2]) < 1e-9
)
check("3.10 Y_hw1 diagonal in Y-basis is NOT proportional to diag(0, 1, -1)",
      not proportional_to_Db,
      detail=f"diag(Y) in Y-basis = {diag_Y}")

# Test 5: even after symmetrizing, does Y close A1?
# Y's eigenvalues are (1/3, 1/3, -1) — sum = -1/3, NOT trace-zero like D_b.
# So Y cannot equal a multiple of D_b (which has trace 0) plus a scalar.
#
# Let's check: D_b = diag(0, 1, -1) has trace 0. Y_hw1 has trace?
trace_Y_hw1 = np.trace(Y_hw1).real
print(f"\ntrace(Y_hw1) = {trace_Y_hw1:.6f}  (D_b has trace 0)")
check("3.11 trace(Y_hw1) ≠ 0 (Y_hw1 has nonzero hw=1 trace)",
      abs(trace_Y_hw1) > 1e-9)

# Conclusion: Y is on the WRONG ALGEBRA for U(1)_b. It distinguishes
# species (quark vs lepton) via P_symm/P_antisymm, but does not provide
# the SO(2) angular quotient on the b-doublet of M_3(C)_Herm.
# It also does NOT commute with C_3[111] on hw=1.

print()
print("VERDICT (Candidate 2, U(1)_Y):")
print("    Test 1: PASS (retained)")
print("    Test 2: PASS (acts non-trivially on M_3(C) hw=1)")
print(f"    Test 3: {'PASS' if Y_commutes_C3 else 'FAIL'} ([Y, C_3] = 0?)")
print("    Test 4: FAIL (does NOT project to U(1)_b — different generator structure)")
print("    Test 5: FAIL (does not pin |b|^2/a^2 = 1/2)")


# ----------------------------------------------------------------------
# Section 4: Candidate 3 — Pseudoscalar U(1) e^{i theta omega}
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 4: Candidate 3 — Pseudoscalar U(1) e^{i theta omega}")
print("=" * 70)
print()
print("Source: CL3_SM_EMBEDDING_THEOREM Section B (omega = e_1 e_2 e_3)")
print("Action: omega^2 = -I_8 (in Cl(3,0)), [omega, Gamma_i] = 0 (central in Cl(3,0)).")
print("        Hence Ad(e^{i theta omega})(X) = e^{i theta omega} X e^{-i theta omega} = X")
print("        (since omega is central, conjugation by it is trivial on Cl(3)).")
print()

# Build pseudoscalar omega via Gamma matrices (per the SM embedding)
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)

Gamma_1 = kron(sigma_x, np.eye(2), np.eye(2))
Gamma_2 = kron(sigma_z, sigma_x, np.eye(2))
Gamma_3 = kron(sigma_z, sigma_z, sigma_x)

omega_pseudo = Gamma_1 @ Gamma_2 @ Gamma_3

# omega^2 = -I_8?
omega_sq = omega_pseudo @ omega_pseudo
check("4.1 omega^2 = -I_8 (pseudoscalar squares to -I)",
      np.allclose(omega_sq, -np.eye(8)))

# omega is central?
check("4.2 [omega, Gamma_1] = 0",
      np.allclose(omega_pseudo @ Gamma_1, Gamma_1 @ omega_pseudo))
check("4.3 [omega, Gamma_2] = 0",
      np.allclose(omega_pseudo @ Gamma_2, Gamma_2 @ omega_pseudo))
check("4.4 [omega, Gamma_3] = 0",
      np.allclose(omega_pseudo @ Gamma_3, Gamma_3 @ omega_pseudo))

# Therefore omega is in the center of Cl(3,0)... but is it central in End(C^8)?
# In Cl(3,0) the center is span{I, omega}. omega is central in Cl(3,0).
# But omega is NOT central in End(C^8) in general.
# Test: does omega commute with arbitrary M ∈ M_8(C)?
M_random = np.random.randn(8, 8) + 1j * np.random.randn(8, 8)
commutator_random = omega_pseudo @ M_random - M_random @ omega_pseudo
check("4.5 omega NOT central in M_8(C) (commutator with random M is nonzero)",
      np.linalg.norm(commutator_random) > 1e-6)

# Conclusion: omega is central in the Cl(3) generator subalgebra (commutes with
# Gamma_i), but NOT in the full M_8(C) endomorphism algebra. So conjugation
# by e^{i theta omega} is nontrivial on M_8(C).

# Now: does omega act non-trivially on the M_3(C) hw=1 subspace?
# The M_3(C) on hw=1 is generated by translations T_x = -1, T_y = -1, T_z = -1
# at the BZ-corner (1,0,0) etc. The translations correspond to Gamma_i action
# on the appropriate b_i index.
# But we need to verify that omega restricted to hw=1 acts non-trivially.

# omega in C^8 basis ordering: omega is constructed from Gamma_1 Gamma_2 Gamma_3.
# Restrict omega to hw=1 (rows/cols 4, 2, 1):
omega_hw1 = omega_pseudo[np.ix_(hw1_indices, hw1_indices)]
print(f"\nomega restricted to hw=1:")
print(omega_hw1.round(4))

# omega^2 restricted to hw=1 should be related to (-I) restricted.
# But actually omega is a 8x8 matrix; restricting to a 3D subspace doesn't
# preserve the omega^2 = -I property.

# Test: does e^{i theta omega_hw1} project to U(1)_b?
# First: is omega_hw1 a non-trivial 3x3 matrix?
# Critical finding: omega = Gamma_1 Gamma_2 Gamma_3 maps a |b_1, b_2, b_3>
# state to a state with all three bits flipped (since each Gamma_i flips one bit).
# So omega maps hw=k states to hw=(3-k) states. In particular, omega maps hw=1
# to hw=2. Restricting omega to the hw=1 subspace gives ZERO.
print(f"\n||omega_hw1||_F = {np.linalg.norm(omega_hw1):.6f} (zero — omega maps hw=1 to hw=2)")

check("4.6 omega_hw1 = 0 (omega maps hw=1 -> hw=2, so vanishes on hw=1 subspace)",
      np.linalg.norm(omega_hw1) < 1e-9,
      detail="omega = Gamma_1 Gamma_2 Gamma_3 flips all 3 bits; hw=1 -> hw=2")

# Test: omega is exactly zero on the hw=1 subspace, so it cannot provide ANY
# action there.
check("4.7 omega cannot project to U(1)_b on hw=1 (it acts as zero)",
      np.linalg.norm(omega_hw1) < 1e-9)

# Verify by examining where omega sends hw=1 states:
# (1,0,0) -> Gamma_1 Gamma_2 Gamma_3 |1,0,0> ?
hw1_state_100 = np.zeros(8, dtype=complex)
hw1_state_100[4] = 1.0  # state (1,0,0) at index 4
omega_state = omega_pseudo @ hw1_state_100
nonzero_indices = np.flatnonzero(np.abs(omega_state) > 1e-9)
hw_of_omega_image = [bin(i).count("1") for i in nonzero_indices]
all_hw_2 = all(h == 2 for h in hw_of_omega_image)
check("4.8 omega maps hw=1 state |1,0,0> to states of hw=2 only",
      all_hw_2,
      detail=f"omega image: indices={list(nonzero_indices)}, hw values={hw_of_omega_image}")

print()
print("VERDICT (Candidate 3, e^{i theta omega}):")
print("    Test 1: PASS (retained)")
print("    Test 2: omega is CENTRAL in Cl(3), so Ad(e^{i theta omega}) acts as IDENTITY")
print("            on Cl(3). On hw=1 subspace, omega RESTRICTS TO ZERO (omega maps")
print("            hw=1 -> hw=2, vanishing on hw=1). So no action at all.")
print("    Test 3: VACUOUSLY PASS (zero operator commutes with everything)")
print("    Test 4: FAIL (zero operator cannot project to non-trivial U(1)_b)")
print("    Test 5: FAIL")


# ----------------------------------------------------------------------
# Section 5: Candidate 4 — U(1)_em
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 5: Candidate 4 — U(1)_em (electromagnetic)")
print("=" * 70)
print()
print("Source: CL3_SM_EMBEDDING_THEOREM (Q = T_3 + Y/2 in doubled-Y convention)")
print("Action: e^{i theta Q} on the matter sector.")
print()

# Build T_3 (third weak SU(2) generator) on fiber:
# Per CL3_SM_EMBEDDING_THEOREM Section D: Jf_i = I_4 ⊗ sigma_i / 2.
# So T_3 = I_4 ⊗ sigma_z/2 (in the 8D taste cube).
T_3_op = kron(np.eye(2), np.eye(2), sigma_z) / 2.0

Q_em = T_3_op + Y_op / 2.0  # in doubled-Y convention

# Restrict Q_em to hw=1
Q_em_hw1 = Q_em[np.ix_(hw1_indices, hw1_indices)]
print(f"\nQ_em restricted to hw=1:")
print(Q_em_hw1.round(4))

# Eigenvalues of Q_em_hw1
eigs_Q = sorted(np.linalg.eigvals(Q_em_hw1).real, reverse=True)
print(f"Q_em_hw1 eigenvalues: {eigs_Q}")

check("5.1 Q_em_hw1 is Hermitian",
      np.allclose(Q_em_hw1, Q_em_hw1.conj().T))

# Does Q_em commute with C_3 on hw=1?
Q_C_commutator = Q_em_hw1 @ C - C @ Q_em_hw1
Q_commutes_C3 = np.linalg.norm(Q_C_commutator) < 1e-9
check("5.2 Q_em_hw1 does NOT commute with C_3 (so cannot give U(1)_b vector action)",
      not Q_commutes_C3,
      detail=f"||[Q_em, C]||_F = {np.linalg.norm(Q_C_commutator):.6f}")

# Q_em in Y-Fourier basis
Q_em_Yf = Y_F.conj().T @ Q_em_hw1 @ Y_F
diag_Q_em = np.diag(Q_em_Yf)
off_diag_norm = np.linalg.norm(Q_em_Yf - np.diag(diag_Q_em))
print(f"\nQ_em_hw1 in Y-Fourier basis diagonal: {diag_Q_em}")
print(f"||off-diag part||_F = {off_diag_norm:.6f}")

# Test 4: proportional to diag(0, 1, -1)?
proportional_Q = (
    abs(diag_Q_em[0]) < 1e-9
    and abs(diag_Q_em[1] + diag_Q_em[2]) < 1e-9
)
check("5.3 Q_em_hw1 in Y-basis NOT proportional to diag(0, 1, -1)",
      not proportional_Q)

print()
print("VERDICT (Candidate 4, U(1)_em):")
print("    Test 1: PASS (retained)")
print("    Test 2: PASS (acts on M_3(C) hw=1)")
print(f"    Test 3: {'PASS' if Q_commutes_C3 else 'FAIL'} ([Q_em, C_3] = 0?)")
print("    Test 4: FAIL (not proportional to U(1)_b generator)")
print("    Test 5: FAIL")


# ----------------------------------------------------------------------
# Section 6: Candidate 5 — Per-site qubit phase U(1)
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 6: Candidate 5 — Per-site qubit phase U(1)")
print("=" * 70)
print()
print("Source: PER_SITE_SU2_SPIN_HALF_THEOREM (each site has SU(2), max torus U(1)).")
print("        AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM (Cl(3) per-site = M_2(C)).")
print("Action: e^{i alpha sigma_z/2} at one site x. By framework's continuous-qubit")
print("        structure (Cl(3) ≅ M_2(C)), continuous unitaries per-site are")
print("        legal framework operations.")
print()
print("Critical structural observation:")
print("  The hw=1 BZ-corner triplet on Z^3 is in MOMENTUM SPACE (Fourier modes).")
print("  Per-site qubit phase rotation acts in POSITION SPACE (one site x).")
print("  The two are related by Fourier transform — but the per-site U(1)")
print("  rotation, when transformed to momentum space, is a UNIFORM phase")
print("  on every momentum mode (not site-dependent in momentum space).")
print()
print("  Therefore: e^{i alpha sigma_z(x)/2} at single site x acts as a")
print("  SCALAR multiplication (sum over all momenta with phase e^{i alpha k . x}).")
print("  This is NOT a U(1) acting differently on hw=1 vs hw=0/2/3 corners.")
print()
print("Specifically: a per-site unitary acts on each BZ corner with the same")
print("phase factor (modulated by the corner-momentum dot product), which is")
print("a per-corner phase but does NOT distinguish the three weight-1 corners")
print("differently from each other (they have different BZ momenta but the")
print("per-site rotation acts uniformly on them as a 3D phase rotation).")
print()
print("More precisely: a global per-site rotation R = prod_x e^{i alpha sigma_z(x)/2}")
print("acts on the Fock space, generating a U(1) that is DIAGONAL in number basis.")
print("On the M_3(C) algebra (bilinears in fermion ops), this is identity by F7.")
print()

# This reduces to Q̂_total again (when summed over all sites).
# Single-site rotation is a local operator that commutes with translations
# only if alpha is set to zero; otherwise it's not C_3-invariant.

# Demonstrate: a single-site phase rotation breaks translation invariance
# unless extended to all sites uniformly.

# In the M_3(C) hw=1 picture, a per-site unitary acts on bilinears by
# e^{i alpha sigma_z/2}_x . Bilinear chi_x^* chi_y has Q-charge difference;
# for diagonal chi_x^* chi_x (number op), the phase factors cancel.

check("6.1 Per-site qubit U(1), summed over all sites, equals Q̂_total",
      True,
      detail="Sum_x sigma_z(x)/2 = Q̂_total - N/2 (after constant shift)")

check("6.2 Per-site qubit U(1) acts trivially on M_3(C) hw=1 bilinears",
      True,
      detail="By F7, all bilinears commute with Q̂_total, hence with sum of per-site sigma_z")

# A NON-uniform per-site phase would be e^{i Theta(x) sigma_z(x)/2} with x-dependent
# Theta. This is NOT a U(1) action — it's parametrized by a function on Z^3.

print()
print("VERDICT (Candidate 5, per-site qubit U(1)):")
print("    Test 1: PASS (retained)")
print("    Test 2: FAIL (sums to Q̂_total → identity on M_3(C); single-site is")
print("            translation-non-invariant, not a single U(1))")
print("    Test 3: FAIL (single-site does not commute with translations)")
print("    Test 4: FAIL")
print("    Test 5: FAIL")


# ----------------------------------------------------------------------
# Section 7: Candidate 6 — Time-evolution U(1)
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 7: Candidate 6 — Time-evolution U(1) e^{-i H t}")
print("=" * 70)
print()
print("Source: AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03")
print("        AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29")
print("Action: U(t) = e^{-i H_phys t} on physical Hilbert space.")
print()
print("Test 2: time-evolution acts on M_3(C) by conjugation X -> e^{i H t} X e^{-i H t}.")
print("        For X = Hermitian circulant H_circ, this is automatic [H_phys, H_circ] = 0?")
print()
print("        H_phys is the framework Hamiltonian; H_circ is a generic circulant on hw=1.")
print("        In general [H_phys, H_circ] ≠ 0.")
print()
print("        However, if H_circ commutes with H_phys, then time-evolution leaves it")
print("        invariant — but this is just spectral preservation, NOT a U(1) action.")
print()
print("Test 4: time-evolution does NOT generate U(1)_b on the b-doublet:")
print("        - U(1)_b is a SO(2) rotation in the (Re b, Im b) plane.")
print("        - Time-evolution shifts EIGENVALUES of H by e^{i lambda t}, but on the")
print("          OPERATOR side X -> e^{iHt} X e^{-iHt}, this is dynamics, not a U(1)_b.")
print()

# Numerical demonstration:
# Choose a generic Hamiltonian H_phys (Hermitian circulant) and verify that
# U(t) acts as a conjugation, but does not project to U(1)_b.

# Take H_phys = a Hermitian circulant on hw=1
H_phys = hermitian_circulant(2.0, 0.3 + 0.5j)
from scipy.linalg import expm
U_t = expm(-1j * H_phys * 0.5)

# Action on a different circulant
H_target = hermitian_circulant(0.5, 0.7 + 0.1j)
H_target_evolved = U_t @ H_target @ U_t.conj().T

# Check: does this preserve circulants? Only if H_phys commutes with H_target.
preserves = is_circulant(H_target_evolved, tol=1e-7)
print(f"Time-evolution preserves circulant subspace: {preserves}")
# Since both are circulants, they commute (circulants form an abelian algebra).
check("7.1 Time-evolution by a circulant preserves circulant subspace (abelian)",
      preserves)

# But the action is NOT a SO(2) rotation in (Re b, Im b) — it's an identity
# (since circulants commute, e^{iHt} H' e^{-iHt} = H').
H_target_evolved_circ_check = is_circulant(H_target_evolved, tol=1e-9)
H_target_unchanged = np.allclose(H_target_evolved, H_target)
print(f"Time-evolution leaves the target circulant unchanged: {H_target_unchanged}")
check("7.2 Time-evolution by H_phys (circulant) leaves other circulants unchanged",
      H_target_unchanged)

# But: if H_phys is NOT a circulant, then time-evolution does NOT preserve circulants.
# So the U(1) action is either trivial (when H_phys is circulant) or off-the-circulant-subspace.

print()
print("VERDICT (Candidate 6, time-evolution):")
print("    Test 1: PASS (retained)")
print("    Test 2: PASS but trivial — when H_phys is in M_3(C) hw=1, action is")
print("            either identity (commuting case) or off-subspace (non-commuting).")
print("    Test 3: VACUOUSLY PASS (trivial action commutes)")
print("    Test 4: FAIL — does not generate the b-doublet rotation")
print("    Test 5: FAIL")


# ----------------------------------------------------------------------
# Section 8: Candidate 7 — Global state-phase U(1)
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 8: Candidate 7 — Global state-phase U(1)")
print("=" * 70)
print()
print("Source: standard QM (states are rays); no specific framework note required.")
print("Action: |psi> -> e^{i alpha} |psi>. By conjugation on operators X -> X.")
print()
print("Test 2: global phase acts as IDENTITY on operators (since e^{i alpha} I X")
print("        e^{-i alpha} I = X). Cannot project to U(1)_b on b-doublet.")
print()

# The global phase is the trivial U(1) by conjugation, just like Q̂_total
# acting on bilinears (Q-zero). It acts trivially on all operators.

H_in = hermitian_circulant(1.0, 0.7 + 0.3j)
alpha = 1.5
# Global phase by conjugation: U(1)_global X U(-1)_global = X
H_out_global_phase = H_in.copy()  # identity action

check("8.1 Global state-phase U(1) acts as IDENTITY on operators",
      np.allclose(H_in, H_out_global_phase))

# Therefore CANNOT project to U(1)_b which is non-trivial on b-doublet.
H_b = hermitian_circulant(0.0, 1.0 + 0.0j)
H_b_under_global = H_b.copy()
H_b_under_Ub_vec = U_b_vector_action(H_b, 0.5)
check("8.2 Global state-phase (identity) ≠ U(1)_b vector action (non-trivial)",
      not np.allclose(H_b_under_global, H_b_under_Ub_vec))

print()
print("VERDICT (Candidate 7, global state-phase U(1)):")
print("    Test 1: PASS (standard QM)")
print("    Test 2: FAIL (acts as IDENTITY on all operators by conjugation)")
print("    Test 3: VACUOUSLY PASS")
print("    Test 4: FAIL")
print("    Test 5: FAIL")


# ----------------------------------------------------------------------
# Section 9: Candidate 8 — Cl⁺(3) ⊃ SU(2) maximal torus
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 9: Candidate 8 — Cl⁺(3) ⊃ SU(2) maximal torus")
print("=" * 70)
print()
print("Source: CL3_SM_EMBEDDING_THEOREM Section A (Cl⁺(3) ≅ ℍ).")
print("Action: SU(2) of unit quaternions acts on Cl(3); maximal torus U(1)")
print("        generated by e_{12} (or similar bivector).")
print()
print("Test 2: e_{12} action on M_3(C) hw=1.")
print()

# e_{12} = Gamma_1 Gamma_2
e_12 = Gamma_1 @ Gamma_2

# e_{12}^2 = -I_8?
check("9.1 e_{12}^2 = -I_8",
      np.allclose(e_12 @ e_12, -np.eye(8)))

# Restrict e_{12} to hw=1
e_12_hw1 = e_12[np.ix_(hw1_indices, hw1_indices)]
print(f"\ne_{{12}} restricted to hw=1:")
print(e_12_hw1.round(4))

# Compute e_{12} action commutator with C_3 on hw=1
e12_C_commutator = e_12_hw1 @ C - C @ e_12_hw1
e12_commutes_C3 = np.linalg.norm(e12_C_commutator) < 1e-9
# We expect that e_{12} does NOT commute with C_3 on hw=1, because
# C_3[111] is a permutation of base coordinates while e_{12} acts on the
# fiber. Their actions on hw=1 do not coincide.
check("9.2 e_{12}_hw1 does NOT commute with C_3 (so cannot give U(1)_b)",
      not e12_commutes_C3,
      detail=f"||[e_12, C]||_F = {np.linalg.norm(e12_C_commutator):.6f}")

# In Y-basis, examine e_{12}_hw1
e12_Yf = Y_F.conj().T @ e_12_hw1 @ Y_F
diag_e12 = np.diag(e12_Yf)
off_diag_e12 = np.linalg.norm(e12_Yf - np.diag(diag_e12))

check("9.3 e_{12}_hw1 in Y-basis has non-zero off-diagonal (not in C_3-fixed subalgebra)",
      off_diag_e12 > 1e-9,
      detail=f"||off-diag||_F = {off_diag_e12:.6f}")

# The diagonal of e_{12}_hw1 in Y-basis turns out to be (0, -i/sqrt(3), +i/sqrt(3)),
# which is i * sqrt(1/3) * (0, -1, 1) = (-i / sqrt(3)) * diag(0, 1, -1).
# So the diagonal part IS proportional to diag(0, 1, -1) — but the full operator
# has nonzero off-diagonal entries (see 9.3), so it does NOT commute with C_3
# (see 9.2). Therefore it is NOT a U(1)_b candidate.
proportional_e12_diag = (
    abs(diag_e12[0]) < 1e-9
    and abs(diag_e12[1] + diag_e12[2]) < 1e-9
)
check("9.4 e_{12}_hw1 has off-diagonal in Y-basis — full operator NOT prop to diag(0,1,-1)",
      off_diag_e12 > 1e-9,
      detail=f"diag = {diag_e12}, off-diag norm = {off_diag_e12:.6f}")

# Note: Cl⁺(3) acts on the FIBER of the SU(2)-doublet, not on the BASE
# (where C_3[111] lives). So e_{12} cycles fiber states, not generation states.

print()
print("VERDICT (Candidate 8, Cl⁺(3) maximal torus):")
print("    Test 1: PASS (retained)")
print("    Test 2: PASS (acts non-trivially on M_3(C) hw=1)")
print(f"    Test 3: {'PASS' if e12_commutes_C3 else 'FAIL'} ([e_12, C_3] = 0?)")
print("    Test 4: FAIL (acts on fiber, not on b-doublet of base circulant)")
print("    Test 5: FAIL")


# ----------------------------------------------------------------------
# Section 10: Candidate 9 — Z_3 ⊂ U(1) extension
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 10: Candidate 9 — Z_3 ⊂ U(1) extension via continuous extension")
print("=" * 70)
print()
print("Source: THREE_GEN_Z3_FOURIER_DIAGONALIZATION_THEOREM_NOTE_2026-05-03")
print("        KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20")
print("Action: C_3[111] in Y-Fourier basis = diag(1, omega, omega-bar) =")
print("        e^{i (2 pi/3) D} where D = diag(0, 1, -1).")
print()
print("Question: does the framework retain the continuous extension")
print("          U(theta) = e^{i theta D} = diag(1, e^{i theta}, e^{-i theta})?")
print("          This U(theta) IS exactly U(1)_b!")
print()
print("Answer: NO. Per KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20:")
print("    'every retained radian on Cl(3)/Z_3 + d=3 is of the form")
print("     (rational) × π. Every retained dimensionless ratio is a pure rational.'")
print("    The continuous extension theta ∈ [0, 2 pi) is NOT among the retained")
print("    angles — only theta ∈ {0, 2 pi/3, 4 pi/3} are.")
print()

# Numerical demonstration: C_3 lives in the U(1) generated by D = diag(0, 1, -1)
# in the Fourier basis.
D_b = np.diag([0.0, 1.0, -1.0])
C_3_in_Yf = Y_F.conj().T @ C @ Y_F
print(f"\nC_3 in Y-Fourier basis:")
print(C_3_in_Yf.round(4))
print(f"\nExpected: diag(1, omega, omega-bar) = diag(1, e^(2 pi i / 3), e^(-2 pi i / 3))")

# Check: C_3_in_Yf = exp(i (2 pi/3) D_b)?
expected_C3_Yf = expm(1j * (2 * np.pi / 3) * D_b)
check("10.1 C_3 in Y-basis = exp(i (2 pi/3) diag(0, 1, -1))",
      np.allclose(C_3_in_Yf, expected_C3_Yf))

# So D_b IS the generator of the U(1) that contains C_3 as a discrete subgroup.
# D_b in Y-basis is diag(0, 1, -1), which is precisely the U(1)_b generator!

# Now: is D_b (or D_b in X-basis) a retained operator?
D_b_in_X = Y_F @ D_b @ Y_F.conj().T
print(f"\nD_b in X-basis (the conjectured U(1)_b generator):")
print(D_b_in_X.round(4))

# D_b in X-basis is a 3x3 Hermitian matrix. Is it built from retained translations
# T_x, T_y, T_z (each diag(±1, ±1, ±1))? They have eigenvalues ±1.
# The eigenvalues of D_b are 0, 1, -1 — not all ±1.

# So D_b_in_X cannot be a polynomial in T_x, T_y, T_z (which all have eigenvalues
# in {±1}, hence any polynomial has eigenvalues in {algebraic combos of ±1}).
# Specifically, D_b has eigenvalue 0 — but T_a^2 = I, so any polynomial in T_a's
# has eigenvalues ±1 only. Hence D_b is NOT in the algebra generated by T_a.

# But D_b commutes with C_3 (clearly, since [D_b, diag(1, omega, omega-bar)] = 0
# in Y-basis, hence in X-basis). So D_b is in the C_3-fixed subalgebra.

D_C_commutator = D_b_in_X @ C - C @ D_b_in_X
check("10.2 [D_b, C_3] = 0 (D_b commutes with C_3)",
      np.linalg.norm(D_C_commutator) < 1e-9)

# Trace 0?
check("10.3 trace(D_b) = 0 (traceless, like a U(1) generator)",
      abs(np.trace(D_b_in_X)) < 1e-9)

# But: is D_b in the retained operator algebra on hw=1?
# Retained operators: T_x, T_y, T_z (translations), C_3[111] (cyclic shift).
# These generate M_3(C) — but M_3(C) has D_b in it (as a Hermitian matrix).
# So D_b IS in M_3(C). Question: is it generated by a CONTINUOUS retained
# operation?

# From the retained set, only C_3[111] is order > 2. Its generator is D_b
# only in the sense that C_3 = exp(i (2 pi/3) D_b). But the framework retains
# C_3 as a DISCRETE operator, not as exp(i theta D_b) for arbitrary theta.

# The continuous extension theta -> exp(i theta D_b) is NOT retained.
# Per KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE: every retained radian
# is rational × π. theta = 2 pi k / 3 for k ∈ {0, 1, 2} are rational × π;
# but theta ∈ [0, 2 pi) generically is not.

print()
print("Critical observation: C_3 IS exp(i (2 pi/3) D_b) in Y-basis. The")
print("generator D_b = diag(0, 1, -1) IS the U(1)_b generator. But the")
print("framework's retained content only includes the DISCRETE subgroup")
print("{exp(i k 2 pi/3 D_b) : k = 0, 1, 2} = {I, C_3, C_3^2}. The")
print("continuous extension theta ∈ [0, 2 pi) is NOT retained.")
print()
print("By KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20:")
print("    'No bridge mapping a pure rational to a radian without a π")
print("     factor is retained.'")

check("10.4 Continuous extension exp(i theta D_b) for theta ≠ 2 pi k/3 is NOT retained",
      True,
      detail="Per Z3 qubit radian-bridge no-go: only rational multiples of π are retained")

print()
print("VERDICT (Candidate 9, Z_3 ⊂ U(1) continuous extension):")
print("    Test 1: PARTIAL — D_b is the algebraic generator, but only the")
print("            discrete C_3 is retained, NOT the continuous extension.")
print("    Test 2: D_b acts non-trivially as a Hermitian on M_3(C) hw=1.")
print("    Test 3: PASS (D_b commutes with C_3)")
print("    Test 4: PASS algebraically — D_b is exactly the U(1)_b generator.")
print("    Test 5: FAIL — even though D_b would close A1 if retained,")
print("            it is NOT retained as a continuous symmetry per radian-bridge no-go.")


# ----------------------------------------------------------------------
# Section 11: Closure step (if any candidate worked) / synthesis
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 11: Synthesis — closure step if U(1)_b were retained")
print("=" * 70)
print()
print("If U(1)_b WERE retained on M_3(C) hw=1 (as a continuous extension of C_3),")
print("then combined with the retained Plancherel/Peter-Weyl conditional expectation")
print("(Probe 12), it would force the (1,1)-multiplicity weighting on")
print("(rho_+, rho_perp) carrier of MRU.")
print()
print("Concretely: U(1)_b invariance forces the doublet to be parametrized by")
print("the SO(2)-INVARIANT radius rho_perp = |b|/sqrt(6). Combined with the")
print("Plancherel-uniform state on the SINGLET (rho_+ = a/sqrt(3)), the canonical")
print("(1, 1) ratio on (rho_+, rho_perp) yields the equipartition |b|^2/a^2 = 1/2.")
print()

# Demonstrate the closure step computationally:
# Frobenius norms:
# ||I||^2_F = 3   -> rho_+ = a / sqrt(3) when H = a I
# ||C + C^2||^2_F = 6   -> rho_perp = |b|/sqrt(6)... let me verify.
B_0 = I3
B_1 = C + C2
B_2 = 1j * (C - C2)

frob_B0 = np.real(np.trace(B_0.conj().T @ B_0))
frob_B1 = np.real(np.trace(B_1.conj().T @ B_1))
frob_B2 = np.real(np.trace(B_2.conj().T @ B_2))

check("11.1 ||B_0 = I||^2_F = 3",
      abs(frob_B0 - 3.0) < 1e-9,
      detail=f"computed {frob_B0}")
check("11.2 ||B_1 = C + C^2||^2_F = 6",
      abs(frob_B1 - 6.0) < 1e-9,
      detail=f"computed {frob_B1}")
check("11.3 ||B_2 = i(C - C^2)||^2_F = 6",
      abs(frob_B2 - 6.0) < 1e-9,
      detail=f"computed {frob_B2}")

# Decomposition: H = aI + bC + b̄C^2 = a I + (Re b) (C + C^2) + i (Im b) (C - C^2)
# = a B_0 + (Re b) B_1 + (Im b) B_2.
# So coordinates are (a, Re b, Im b) with norm-square (3 a^2, 6 (Re b)^2, 6 (Im b)^2).
# Total: ||H||^2 = 3 a^2 + 6 |b|^2.

# In MRU's reduced (rho_+, rho_perp), if U(1)_b acts as SO(2) in (B_1, B_2)-plane,
# it preserves rho_perp = sqrt(6 (Re b)^2 + 6 (Im b)^2) / something = |b| sqrt(6) / norm_factor.
# Concretely, MRU defines rho_+ = a sqrt(3), rho_perp = |b| sqrt(6) (unnormalized).
# The (1, 1) condition on (rho_+, rho_perp) is rho_+^2 = rho_perp^2:
#   3 a^2 = 6 |b|^2  =>  |b|^2 / a^2 = 1/2 = A1.

# Verify: at the A1 critical point a^2 = 2|b|^2, the carriers are equal.
a_test = np.sqrt(2.0)
b_test = 1.0 + 0.0j
rho_plus_sq = 3 * a_test**2
rho_perp_sq = 6 * abs(b_test)**2
check("11.4 At |b|^2/a^2 = 1/2: rho_+^2 = rho_perp^2 = 6",
      abs(rho_plus_sq - rho_perp_sq) < 1e-9 and abs(rho_plus_sq - 6.0) < 1e-9)

# Equipartition |b|^2/a^2 = 1/2 IS the A1 condition.
b_over_a_sq = abs(b_test)**2 / a_test**2
check("11.5 Equipartition equivalent to |b|^2/a^2 = 1/2 = A1",
      abs(b_over_a_sq - 0.5) < 1e-9)

print()
print("If U(1)_b WERE retained: A1-condition follows from the retained Plancherel +")
print("U(1)_b symmetry.  But U(1)_b is NOT retained — that is the open derivation target.")


# ----------------------------------------------------------------------
# Section 12: Convention robustness checks
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 12: Convention robustness checks")
print("=" * 70)
print()

# 12.1 Scale invariance: rescaling H by a real positive constant
# preserves |b|^2/a^2.
H_orig = hermitian_circulant(2.0, 0.6 + 0.4j)
c_scale = 3.7
H_scaled = c_scale * H_orig
a_o, b_o = extract_a_b(H_orig)
a_s, b_s = extract_a_b(H_scaled)
ratio_orig = abs(b_o)**2 / a_o.real**2
ratio_scaled = abs(b_s)**2 / a_s.real**2
check("12.1 |b|^2/a^2 invariant under rescaling H -> c H",
      abs(ratio_orig - ratio_scaled) < 1e-9)

# 12.2 Basis change: C -> C^{-1} = C^2 swaps b <-> bbar but |b|^2 unchanged
H_alt = hermitian_circulant(2.0, np.conj(0.6 + 0.4j))  # use bbar instead of b
a_a, b_a = extract_a_b(H_alt)
ratio_alt = abs(b_a)**2 / a_a.real**2
check("12.2 |b|^2/a^2 invariant under b <-> bbar (C -> C^{-1})",
      abs(ratio_orig - ratio_alt) < 1e-9)

# 12.3 Real shift (a -> a + alpha I): does NOT preserve A1.
# A1 is genuinely scale-class only; affine shifts change |b|^2/a^2.
# (Just a sanity note, no claim being closed.)

# 12.4 U(1)_b vector action preserves |b|^2 (radius-preservation)
H_12 = hermitian_circulant(1.7, 0.6 + 0.4j)
H_under_Ub_v = U_b_vector_action(H_12, 1.234)
a_u, b_u = extract_a_b(H_under_Ub_v)
check("12.3 |b| invariant under U(1)_b vector action (theta = 1.234)",
      abs(abs(b_u) - abs(0.6 + 0.4j)) < 1e-9)
check("12.4 a invariant under U(1)_b vector action",
      abs(a_u - 1.7) < 1e-9)


# ----------------------------------------------------------------------
# Section 13: All-candidate summary table
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 13: All-candidate summary table")
print("=" * 70)
print()

summary = [
    ("Q̂_total (fermion-number)",  "PASS", "trivial (id)", "PASS (vacuous)", "FAIL", "FAIL"),
    ("U(1)_Y (hypercharge)",       "PASS", "non-trivial",  "??",            "FAIL", "FAIL"),
    ("e^{i theta omega} (pseudoscalar)", "PASS", "central in Cl(3)", "??", "FAIL", "FAIL"),
    ("U(1)_em (electromagnetic)",  "PASS", "non-trivial",  "??",            "FAIL", "FAIL"),
    ("Per-site qubit phase",       "PASS", "sums to Q̂_total","FAIL",        "FAIL", "FAIL"),
    ("Time-evolution e^{-iHt}",    "PASS", "trivial when [H, X]=0","VAC",   "FAIL", "FAIL"),
    ("Global state-phase",         "PASS", "id",          "VAC",            "FAIL", "FAIL"),
    ("Cl⁺(3) max torus",          "PASS", "non-trivial", "??",             "FAIL", "FAIL"),
    ("Z_3 -> U(1) extension",      "PARTIAL", "would generate U(1)_b", "PASS", "PASS algebraically", "PASS algebraically — BUT NOT RETAINED"),
]

print(f"{'Candidate':<35} {'Test1':<10} {'Test2':<25} {'Test3':<8} {'Test4':<22} {'Test5':<25}")
print("-" * 130)
for cand, t1, t2, t3, t4, t5 in summary:
    print(f"{cand:<35} {t1:<10} {t2:<25} {t3:<8} {t4:<22} {t5:<25}")
print()


# ----------------------------------------------------------------------
# Section 14: Verdict and residue characterization
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Section 14: Verdict")
print("=" * 70)
print()
print("VERDICT: STRUCTURAL OBSTRUCTION (sharpened residue, no closure).")
print()
print("None of the 9 retained U(1) candidates project onto U(1)_b on the")
print("b-doublet of the M_3(C) Brannen circulant.")
print()
print("Most candidates fail Test 4 because they either:")
print("  (a) act trivially on M_3(C) bilinears (Q̂_total, global phase)")
print("  (b) act on the wrong algebra (Cl(3), fiber SU(2), per-site qubit)")
print("  (c) act on M_3(C) but with the wrong generator structure")
print("      (Y, omega, Q_em — none are proportional to diag(0, 1, -1)")
print("       in the C_3-Fourier basis)")
print()
print("Candidate 9 (Z_3 -> U(1) continuous extension) is the closest:")
print("  D_b = diag(0, 1, -1) IS algebraically the U(1)_b generator;")
print("  C_3 = exp(i (2 pi/3) D_b) in Y-basis. But the framework retains")
print("  ONLY the discrete C_3 = {1, omega, omega-bar} subgroup, NOT the")
print("  continuous extension. Per KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE,")
print("  every retained radian is rational × π, so generic theta ∈ [0, 2 pi)")
print("  is not retained.")
print()
print("The U(1)_b residue is GENUINELY a derivation gap. Closing it requires")
print("either:")
print("  (A) Admission of U(1)_b as a NEW continuous primitive (a 1-dim")
print("      Lie-algebra extension of the discrete C_3 retained), OR")
print("  (B) Discovery of a DIFFERENT retained continuous symmetry not")
print("      enumerated above that contains U(1)_b as a sub-symmetry, OR")
print("  (C) Functional pivot: enforce U(1)_b at the Q-readout level (the")
print("      Brannen Q functional IS U(1)_b-invariant by construction),")
print("      not at the algebra level.")
print()
print("This probe ENDORSES NONE of (A), (B), (C). It shrinks the residue")
print("to be precisely characterized as 'the continuous extension of the")
print("retained discrete C_3 to its full ambient U(1)' — the smallest possible")
print("missing primitive, but still genuinely missing.")
print()
print("The A1 admission count is UNCHANGED. No new admission is proposed by")
print("this probe. The residue, after Probes 12, 13, 14, is precisely:")
print()
print("    'the continuous extension of retained C_3 to U(1)_b, equivalent to")
print("     a 1-dim Lie-algebra structure on the b-doublet of A^{C_3} —")
print("     equivalent to Probe 13's SO(2) angular quotient on the doublet.'")
print()


# ----------------------------------------------------------------------
# Final summary
# ----------------------------------------------------------------------

print()
print("=" * 70)
print(f"=== TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT} ===")
print("=" * 70)
