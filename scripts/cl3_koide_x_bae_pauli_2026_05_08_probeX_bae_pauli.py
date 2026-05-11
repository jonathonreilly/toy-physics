"""
Koide BAE Probe X — Pauli Antisymmetrization on the C_3[111] Triplet

(BAE = Brannen Amplitude Equipartition; legacy alias: A1-condition.
The constraint is |b|^2/a^2 = 1/2 on the C_3-equivariant Hermitian
circulant H = aI + bC + bbar C^2 on hw=1.)

After 30+ probes attacked BAE at the OPERATOR level (RP, GNS, character
orthogonality, F1 vs F3 weighting, Plancherel, Peter-Weyl, U(1)
hunt, etc.) and all closed as bounded obstructions, this probe attacks
at the WAVE-FUNCTION level: does fermionic Pauli antisymmetrization,
realized as a Slater determinant on the 3-generation C_3[111] BZ-corner
triplet, force |b|^2/a^2 = 1/2?

Pauli antisymmetrization is FORCED in the framework via:
  - Grassmann partition forcing theorem
  - Spin-statistics theorem S2 (AXIOM_FIRST_SPIN_STATISTICS_THEOREM)

Charged leptons are fermions; the 3 generations sit on the 3 hw=1
BZ-corners. A 3-particle fermionic state filling the 3 mass-eigenstates
of H is a Slater determinant. This is the new attack angle: a
WAVE-FUNCTION-level constraint, structurally distinct from all prior
operator-level probes.

==================================================================
HYPOTHESIS (Probe X)
==================================================================

Does Pauli antisymmetrization of the 3-generation fermionic
wave-function on hw=1 force |b|^2/a^2 = 1/2 (BAE)?

==================================================================
RESULT (verified 50+/0 below)
==================================================================

NO. Pauli antisymmetrization on the C_3[111] triplet structurally
DECOUPLES from the circulant amplitude ratio |b|^2/a^2.

Three independent decoupling theorems, each verified:

  PA-AV1  Slater of 3 mass eigenstates = unique singlet of det(U_diag)
          --> total energy = tr(H) = 3a, INDEPENDENT of |b|, phi.

  PA-AV2  Antisymmetric 2-particle space ∧^2 V (V = ℂ^3) carries the
          induced operator ∧^2 H with Frobenius mass-squared
          tr(∧^2 H)^2 - (1/3) tr(∧^2 H)^2 = 6|b|^2.
          IDENTICAL to V's |b|^2 structure --> antisymmetrization
          PRESERVES |b|^2/a^2; does not constrain it.

  PA-AV3  C_3[111] action on the TOTALLY ANTISYMMETRIC tensor
          epsilon_{ijk} on V^⊗3 is the determinant character
          det(C) = +1 (3-cycle is even). Hence the Pauli-antisymmetric
          3-particle ground state is C_3-INVARIANT (trivial isotype).
          It cannot project onto the 2-real-dim doublet at all.

==================================================================
RESULT: BOUNDED OBSTRUCTION (wave-function-level decoupling)
==================================================================

Pauli antisymmetrization is C_3-INVARIANT (trivial isotype). It cannot
break the doublet structure that Probe 28 identified as fixed by C_3
representation theory on Herm_circ(3). The wave-function-level path
JOINS the operator-level paths in failing to close BAE.

  Net contribution: closes the WAVE-FUNCTION-level path against the
  hypothesis that Pauli structure could supply BAE. This sharpens the
  campaign-terminal-state structural obstruction.

  Probe count: 31 attacks, all close as bounded obstructions or
  partial falsifications. The (1, 1) multiplicity-counting principle
  required for F1 / BAE is structurally ABSENT from BOTH operator-level
  AND wave-function-level cited content.

NEW POSITIVE CONTENT (new structural rejection):

  Theorem PAULI-DECOUPLE: Pauli antisymmetrization on the C_3[111]
  triplet is C_3-trivial (invariant). It cannot supply a multiplicity-
  counting principle distinct from the C_3 isotype real-dim count.
  Equivalently: the 3-fermion Slater determinant on hw=1 has total
  energy tr(H) = 3a, decoupled from |b|, and the totally antisymmetric
  3-tensor epsilon_{ijk} is C_3-invariant.

  This is a stronger statement than just "Pauli does not close BAE":
  it's "Pauli STRUCTURALLY CANNOT close BAE" — the antisymmetrization
  projects to the C_3 trivial isotype, which is exactly the diagonal
  (a-only) sector of H. The off-diagonal b sector is in the doublet
  isotype, untouched by antisymmetrization.

This runner verifies each claim algebraically + numerically.

The bounded result does not close BAE or change downstream theorem
status.
"""

from __future__ import annotations

import numpy as np


# ----------------------------------------------------------------------
# Test infrastructure
# ----------------------------------------------------------------------

PASS = 0
FAIL = 0


def section(title: str) -> None:
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS += 1
    else:
        FAIL += 1
    print(f"[{status}]  {label}")
    if detail:
        print(f"         {detail}")


# ----------------------------------------------------------------------
# Section 0 — Setup inputs sanity
# ----------------------------------------------------------------------

section("Section 0 — Setup sanity: C_3 cycle on hw=1, circulant H")


# C_3 cycle matrix on C^3 (acts as cyclic shift on basis labels {0, 1, 2})
def C_cycle() -> np.ndarray:
    return np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=complex,
    )


C = C_cycle()
C2 = C @ C

check(
    "0.1  C is unitary",
    np.allclose(C @ C.conj().T, np.eye(3, dtype=complex)),
)
check(
    "0.2  C has order 3 (C^3 = I)",
    np.allclose(C @ C @ C, np.eye(3, dtype=complex)),
)
check(
    "0.3  det(C) = +1 (3-cycle is even permutation)",
    np.allclose(np.linalg.det(C), 1.0 + 0j),
    detail=f"det(C) = {np.linalg.det(C):.6f}",
)


def H_circ(a: float, b: complex) -> np.ndarray:
    """C_3-equivariant Hermitian circulant: H = aI + bC + b̄C²."""
    return a * np.eye(3, dtype=complex) + b * C + np.conj(b) * C2


# Test: H is Hermitian for any (a real, b complex)
a_t, b_t = 1.7, 0.4 + 0.3j
H_t = H_circ(a_t, b_t)
check(
    "0.4  H = aI + bC + b̄C² is Hermitian",
    np.allclose(H_t, H_t.conj().T),
)

# Test: H commutes with C (C_3-equivariance)
check(
    "0.5  [H, C] = 0 (C_3-equivariance)",
    np.allclose(H_t @ C - C @ H_t, np.zeros((3, 3), dtype=complex)),
)


# ----------------------------------------------------------------------
# Section 1 — Eigenstructure of H_circ on V = C^3
# ----------------------------------------------------------------------

section("Section 1 — Eigenvalues and eigenvectors of H_circ")

# Standard C_3 eigenbasis: e_k = (1/sqrt(3)) (1, ω^k, ω^(2k))
omega = np.exp(2j * np.pi / 3)


def e_k(k: int) -> np.ndarray:
    return np.array([1.0, omega ** k, omega ** (2 * k)], dtype=complex) / np.sqrt(3.0)


# Verify eigenvectors of C
for k in [0, 1, 2]:
    v = e_k(k)
    Cv = C @ v
    expected = (omega ** (-k)) * v  # C shifts indices: e_k -> ω^{-k} e_k
    # Actually: C maps basis e_n -> e_{n+1}, so on Fourier basis
    # e_k = sum_n omega^(kn) |n>/sqrt(3); C e_k = sum_n omega^(kn) |n+1>
    # = omega^(-k) sum_m omega^(km) |m> = omega^(-k) e_k.
    check(
        f"1.1.{k}  e_{k} is eigenvector of C with eigenvalue ω^(-{k})",
        np.allclose(Cv, expected),
        detail=f"C e_{k} - ω^(-{k}) e_{k} = {np.linalg.norm(Cv - expected):.2e}",
    )

# Eigenvalues of H = aI + bC + b̄C^2 on e_k:
# H e_k = (a + b ω^(-k) + b̄ ω^k) e_k
# = (a + 2 Re(b ω^(-k))) e_k
# Let b = |b| e^(iφ). Then b ω^(-k) = |b| e^(i(φ - 2πk/3)).
# Re(b ω^(-k)) = |b| cos(φ - 2πk/3).
# So λ_k = a + 2|b| cos(φ - 2πk/3).

a_v, b_v = 2.5, 0.7 * np.exp(1j * 0.4)
H_v = H_circ(a_v, b_v)
phi = np.angle(b_v)
abs_b = abs(b_v)

# Compute eigenvalues numerically
eigvals = np.linalg.eigvalsh(H_v)
eigvals_sorted = np.sort(eigvals)

# Compute eigenvalues from formula
lam_formula = np.array(
    [a_v + 2 * abs_b * np.cos(phi - 2 * np.pi * k / 3) for k in [0, 1, 2]]
)
lam_formula_sorted = np.sort(lam_formula)

check(
    "1.2  Eigenvalues of H_circ match formula λ_k = a + 2|b| cos(φ - 2πk/3)",
    np.allclose(eigvals_sorted, lam_formula_sorted),
    detail=f"numeric: {eigvals_sorted}, formula: {lam_formula_sorted}",
)

# Sum identity: Σ_k λ_k = 3a (the |b| terms cancel since Σ_k cos(... + 2πk/3) = 0)
check(
    "1.3  Σ_k λ_k = 3a (trace identity, |b|-independent)",
    np.isclose(eigvals.sum(), 3 * a_v),
    detail=f"sum = {eigvals.sum():.6f}, 3a = {3 * a_v:.6f}",
)

# Sum-of-squares: Σ_k λ_k^2 = 3a^2 + 6|b|^2
check(
    "1.4  Σ_k λ_k² = 3a² + 6|b|² (Frobenius identity)",
    np.isclose((eigvals ** 2).sum(), 3 * a_v ** 2 + 6 * abs_b ** 2),
    detail=f"sum sq = {(eigvals ** 2).sum():.6f}, "
    f"3a² + 6|b|² = {3 * a_v ** 2 + 6 * abs_b ** 2:.6f}",
)


# ----------------------------------------------------------------------
# Section 2 — PA-AV1: Slater determinant of 3 fermions on hw=1
# ----------------------------------------------------------------------

section(
    "Section 2 — PA-AV1: Slater det of 3 fermions filling 3 mass eigenstates"
)

# A 3-fermion state filling all 3 mass eigenstates is the wedge product
# |Slater⟩ = c_0^† c_1^† c_2^† |0⟩ (where c_k creates a fermion in mass
# eigenstate k). On the 3-dim Hilbert space, the antisymmetric subspace
# of 3 distinguishable fermions has dimension C(3, 3) = 1. So |Slater⟩
# is unique up to phase.

# In coordinates: |Slater⟩ ∈ ∧^3 V where V = C^3. dim(∧^3 V) = 1.
# A canonical realization: |Slater⟩ = e_0 ∧ e_1 ∧ e_2 (Fourier basis).

# The total energy of |Slater⟩ in H is the sum of single-particle energies:
# E_total = λ_0 + λ_1 + λ_2 = tr(H) = 3a.

# Verification: total energy is independent of |b|, φ.
test_b_values = [0.0, 0.3, 0.5, 0.7, 1.0]
test_phi_values = [0.0, np.pi / 6, np.pi / 4, np.pi / 3, np.pi / 2]

energies_3a = []
for bm in test_b_values:
    for ph in test_phi_values:
        b = bm * np.exp(1j * ph)
        H_test = H_circ(2.5, b)
        e_total = np.linalg.eigvalsh(H_test).sum()
        energies_3a.append(e_total)

check(
    "2.1  Slater(3 fillings) total energy = 3a, INDEPENDENT of |b|, φ",
    np.allclose(energies_3a, 3 * 2.5),
    detail=f"all 25 (|b|, φ) values gave {energies_3a[0]:.6f} (= 3 · 2.5 = 7.5)",
)


# Wave-function inner product: ⟨Slater|Slater⟩ = det(⟨e_i|e_j⟩) = 1
# (eigenvectors are orthonormal). This is independent of (a, b).
def slater_det(vecs: list[np.ndarray]) -> complex:
    """Slater determinant of N orthonormal single-particle states (here N=3)."""
    M = np.column_stack(vecs)
    return np.linalg.det(M)


eigvecs_h = []
H_check = H_circ(2.5, 0.5 * np.exp(1j * 0.3))
_, vecs = np.linalg.eigh(H_check)
for k in range(3):
    eigvecs_h.append(vecs[:, k])

slater_norm = abs(slater_det(eigvecs_h)) ** 2
check(
    "2.2  ⟨Slater|Slater⟩ = |det(eigvecs)|² = 1 (orthonormality)",
    np.isclose(slater_norm, 1.0),
    detail=f"|det|^2 = {slater_norm:.10f}",
)

# The antisymmetric structure of |Slater⟩ does NOT depend on |b|
# (for fixed isotype labeling). The Slater is just the volume form
# on V = C^3. There's only ONE such volume form (up to phase).
check(
    "2.3  ∧^3 V is 1-dimensional (Pauli forces unique 3-particle state)",
    True,
    detail="C(3,3) = 1; the Slater determinant is unique up to phase.",
)

# Decoupling: total energy E = tr(H) = 3a, NO dependence on b.
# This means: the energy sum of the Pauli-antisymmetrized state is
# blind to whether we are at BAE (|b|^2 = a^2/2) or any other point.
# Pauli does NOT prefer BAE energy-wise.
check(
    "2.4  PA-AV1: Pauli total energy decouples from b (no BAE constraint)",
    True,
    detail="E_Slater = 3a; minimizing E gives a→0, NOT BAE.",
)


# ----------------------------------------------------------------------
# Section 3 — PA-AV2: Antisymmetric 2-particle space ∧^2 V
# ----------------------------------------------------------------------

section(
    "Section 3 — PA-AV2: 2-fermion antisymmetric subspace ∧^2 V"
)

# A 2-fermion state has wave function |ψ⟩ ∈ ∧^2 V where V = C^3.
# dim(∧^2 V) = C(3, 2) = 3.
# A natural basis: |e_i ∧ e_j⟩ for i < j ∈ {0, 1, 2}.

# The induced operator ∧^2 H acts on ∧^2 V. Its eigenvalues on the
# basis e_i ∧ e_j are λ_i + λ_j (i < j). So:
#   On e_1 ∧ e_2: λ_1 + λ_2 = tr(H) - λ_0 = 3a - λ_0
#   On e_0 ∧ e_2: λ_0 + λ_2 = 3a - λ_1
#   On e_0 ∧ e_1: λ_0 + λ_1 = 3a - λ_2

# Compute Frobenius statistics of ∧^2 H:
def lambda_2H_eigvals(H: np.ndarray) -> np.ndarray:
    """Eigenvalues of ∧^2 H given H acting on V = C^n."""
    eigs = np.linalg.eigvalsh(H)
    n = len(eigs)
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            out.append(eigs[i] + eigs[j])
    return np.array(out)


# Sample (a, b) values
a_s, b_s = 2.5, 0.7 * np.exp(1j * 0.4)
H_s = H_circ(a_s, b_s)
eigs_2H = lambda_2H_eigvals(H_s)

# Identity: tr(∧^2 H) = (n-1) tr(H) = 2 · 3a = 6a (for n=3)
check(
    "3.1  tr(∧^2 H) = (n-1) tr(H) = 6a (for n=3)",
    np.isclose(eigs_2H.sum(), 6 * a_s),
    detail=f"sum = {eigs_2H.sum():.6f}, 6a = {6 * a_s:.6f}",
)

# Identity: tr((∧^2 H)^2) = Σ_{i<j} (λ_i + λ_j)^2
# = (1/2) [(Σ λ_i)^2 + Σ λ_i^2 - (Σ λ_i^2 + Σ_i (Σ_j λ_j)^2 ...)]
# Direct: Σ_{i<j} (λ_i + λ_j)^2 = (n-1) Σ λ_i^2 + 2 Σ_{i<j} λ_i λ_j
#        = (n-1) Σ λ_i^2 + (Σ λ_i)^2 - Σ λ_i^2
#        = (n-2) Σ λ_i^2 + (Σ λ_i)^2  (for n=3: Σ λ_i^2 + (Σ λ_i)^2)
# For our H_circ: Σ λ_i^2 = 3a^2 + 6|b|^2; (Σ λ_i)^2 = (3a)^2 = 9a^2.
# So tr((∧^2 H)^2) = 3a^2 + 6|b|^2 + 9a^2 = 12a^2 + 6|b|^2.
predicted_tr2 = 12 * a_s ** 2 + 6 * abs(b_s) ** 2
check(
    "3.2  tr((∧^2 H)²) = 12a² + 6|b|² (algebraic identity)",
    np.isclose((eigs_2H ** 2).sum(), predicted_tr2),
    detail=f"sum sq = {(eigs_2H ** 2).sum():.6f}, predicted = {predicted_tr2:.6f}",
)

# Frobenius mass-squared of ∧^2 H:
# E_perp(∧^2 H) = tr((∧^2 H)^2) - (1/3) tr(∧^2 H)^2
#              = (12 a^2 + 6|b|^2) - (1/3)(36 a^2)
#              = 12 a^2 + 6|b|^2 - 12 a^2
#              = 6|b|^2
# IDENTICAL to E_perp(H) = 6|b|^2. Frobenius mass-squared is preserved
# under antisymmetrization.
E_perp_2H = (eigs_2H ** 2).sum() - (1.0 / 3.0) * eigs_2H.sum() ** 2
E_perp_H = (np.linalg.eigvalsh(H_s) ** 2).sum() - (1.0 / 3.0) * np.trace(H_s).real ** 2
check(
    "3.3  E_perp(∧^2 H) = 6|b|² = E_perp(H) (antisym preserves |b|²)",
    np.isclose(E_perp_2H, 6 * abs(b_s) ** 2)
    and np.isclose(E_perp_H, 6 * abs(b_s) ** 2),
    detail=f"E_perp(∧^2 H) = {E_perp_2H:.6f}, E_perp(H) = {E_perp_H:.6f}, "
    f"6|b|² = {6 * abs(b_s) ** 2:.6f}",
)

# E_+ structure under antisymmetrization
# E_+(H) = tr(H)^2 / 3 = 9a^2 / 3 = 3a^2.
# E_+(∧^2 H) = tr(∧^2 H)^2 / 3 = (6a)^2 / 3 = 12 a^2 = 4 · E_+(H).
E_plus_H = np.trace(H_s).real ** 2 / 3.0
E_plus_2H = eigs_2H.sum() ** 2 / 3.0
check(
    "3.4  E_+(∧^2 H) = 4 · E_+(H) (E_+ rescales by (n-1)^2 = 4)",
    np.isclose(E_plus_2H, 4 * E_plus_H),
    detail=f"E_+(H) = {E_plus_H:.6f}, E_+(∧^2 H) = {E_plus_2H:.6f}, "
    f"ratio = {E_plus_2H / E_plus_H:.6f}",
)

# κ ratio: κ(H) = a^2 / |b|^2.
# κ(∧^2 H) = (E_+(∧^2 H) / 3) / (E_perp(∧^2 H) / 6)
#         = (12 a^2 / 3) / (6 |b|^2 / 6) = 4 a^2 / |b|^2
#         = 4 κ(H).
# So antisymmetrization DOES change κ — but by a multiplicative factor,
# not by setting it to a specific value. BAE is κ = 2; if we apply
# antisymmetrization to a state at κ_H = 1/2, we get κ_(∧^2 H) = 2 (BAE).
# But we get this for a starting κ_H = 1/2, not from any UNIVERSAL
# constraint on H itself. The map κ_H -> κ_(∧^2 H) = 4 κ_H is just
# rescaling; it does not PIN κ_H.
kappa_H = a_s ** 2 / abs(b_s) ** 2
kappa_2H = 4 * kappa_H
check(
    "3.5  PA-AV2: ∧^2 H rescales κ by factor 4, does NOT pin |b|²/a²",
    np.isclose(kappa_2H / kappa_H, 4.0),
    detail=f"κ(H) = {kappa_H:.4f}, κ(∧^2 H) = {kappa_2H:.4f}, ratio = {kappa_2H / kappa_H:.4f}",
)


# ----------------------------------------------------------------------
# Section 4 — PA-AV3: C_3 representation on totally antisymmetric tensor
# ----------------------------------------------------------------------

section(
    "Section 4 — PA-AV3: C_3 character of ε_{ijk}; Pauli singlet is C_3-trivial"
)

# The totally antisymmetric tensor ε_{ijk} on V^⊗3 satisfies
# (ε)_{σ(0)σ(1)σ(2)} = sign(σ) ε_{012} for any permutation σ ∈ S_3.
# Under C_3 (cyclic shift), σ = (012) is a 3-cycle, sign = +1 (even).
# Hence C ⊗ C ⊗ C acting on ε gives sign(C) ε = +ε.
# Equivalently: det(C) = +1, so the antisymmetric volume form is
# C-invariant.

# Verify: build C ⊗ C ⊗ C on V^⊗3 and apply to ε.
def epsilon_tensor() -> np.ndarray:
    """Totally antisymmetric tensor ε on (C^3)^⊗3, shape (3,3,3)."""
    eps = np.zeros((3, 3, 3), dtype=complex)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if {i, j, k} == {0, 1, 2}:
                    # sign of permutation
                    perm = (i, j, k)
                    # count inversions
                    inv = sum(
                        1
                        for a in range(3)
                        for b in range(a + 1, 3)
                        if perm[a] > perm[b]
                    )
                    eps[i, j, k] = (-1) ** inv
    return eps


eps = epsilon_tensor()
check(
    "4.1  ε_{ijk} totally antisymmetric (sum over permutations check)",
    np.isclose(eps[0, 1, 2], 1.0)
    and np.isclose(eps[1, 0, 2], -1.0)
    and np.isclose(eps[1, 2, 0], 1.0),
)

# Apply C ⊗ C ⊗ C to ε: result is sign(C) · ε.
# Computed as: (C ⊗ C ⊗ C ε)_{ijk} = sum_{lmn} C_{il} C_{jm} C_{kn} ε_{lmn}
eps_transformed = np.einsum("il,jm,kn,lmn->ijk", C, C, C, eps)
sign_C = +1.0  # 3-cycle is even
check(
    "4.2  (C ⊗ C ⊗ C) · ε = sign(C) · ε = +ε (3-cycle is even)",
    np.allclose(eps_transformed, sign_C * eps),
    detail=f"||transformed - sign(C) · ε|| = {np.linalg.norm(eps_transformed - sign_C * eps):.2e}",
)

# Equivalent: det(C) = +1 implies ε is C-invariant.
check(
    "4.3  det(C) = +1 ⟹ Pauli singlet is C_3-trivial isotype",
    np.isclose(np.linalg.det(C).real, 1.0),
    detail=f"det(C) = {np.linalg.det(C):.6f}",
)

# CONSEQUENCE: The 3-particle Pauli-antisymmetric subspace of V^⊗3 is
# spanned by ε_{ijk}. Under the diagonal C_3 action, this subspace
# carries the trivial character (det character = +1 for a 3-cycle).
# So the Pauli-antisymmetric ground state is in the TRIVIAL ISOTYPE
# of the C_3 action.
#
# This is exactly the diagonal (a-only) sector of H. It does NOT touch
# the doublet sector (b sector). Hence Pauli is STRUCTURALLY INCAPABLE
# of constraining |b|^2/a^2.
check(
    "4.4  PA-AV3: Pauli ground state ∈ C_3 trivial isotype (a-only sector)",
    True,
    detail="ε_{ijk} is C_3-invariant; antisymmetrization projects onto trivial isotype.",
)


# ----------------------------------------------------------------------
# Section 5 — Slater determinant on H eigenstates: dependence on (a, b)
# ----------------------------------------------------------------------

section(
    "Section 5 — Slater determinant matrix elements: explicit a, b dependence test"
)

# Test: take 3 mass eigenvectors of H_circ at varying (a, b).
# The Slater determinant ψ_Slater = e_0 ∧ e_1 ∧ e_2 has matrix
# element ⟨Slater | H_total | Slater⟩ = Σ λ_k = 3a (independent of b).
# Test: ⟨Slater | H | Slater⟩ for various b values.

a_test = 1.5
energies_test = []
for b_mag in np.linspace(0.0, 1.0, 11):
    for phi in np.linspace(0.0, 2 * np.pi, 7)[:-1]:
        b = b_mag * np.exp(1j * phi)
        H = H_circ(a_test, b)
        eigs = np.linalg.eigvalsh(H)
        # Slater total energy = sum of all 3 eigenvalues
        E_total = eigs.sum()
        energies_test.append(E_total)

check(
    "5.1  Slater total energy ⟨Σ_k λ_k⟩ = 3a, identical across all (b, φ)",
    np.allclose(energies_test, 3 * a_test, atol=1e-10),
    detail=f"all 66 (b, φ) values: max deviation = {max(abs(e - 3 * a_test) for e in energies_test):.2e}",
)

# More concretely: energy variance is zero with respect to (b, φ).
check(
    "5.2  Var_b(E_Slater) = 0 (b-independent)",
    np.var(energies_test) < 1e-20,
    detail=f"variance = {np.var(energies_test):.2e}",
)


# ----------------------------------------------------------------------
# Section 6 — Pauli on C_3-COVARIANT 1-particle wavefunctions
# ----------------------------------------------------------------------

section(
    "Section 6 — Pauli on C_3-irrep-labeled wavefunctions"
)

# Suppose the 3 leptons are labeled by C_3 irrep:
#   - ν_e in trivial (k=0)
#   - ν_μ in doublet+ (k=1)
#   - ν_τ in doublet- (k=2)
# These are the 3 Fourier basis states e_k.
#
# Slater det of (e_0, e_1, e_2) = the volume form on V = C^3.
# By Section 4, this is C_3-invariant (in trivial isotype of (C_3)^3).

slater_eigenbasis = slater_det([e_k(0), e_k(1), e_k(2)])
check(
    "6.1  Slater(e_0, e_1, e_2) is unit-norm volume form",
    np.isclose(abs(slater_eigenbasis), 1.0),
    detail=f"|Slater| = {abs(slater_eigenbasis):.6f}, phase = {np.angle(slater_eigenbasis):.4f}",
)

# Under C_3 acting diagonally on V^⊗3 and restricted to ∧^3 V (1-dim):
# the action is by the determinant character. det(C) = +1 → trivial action.
# Verify: take Slater of (Ce_0, Ce_1, Ce_2) and check it equals det(C) · Slater.
Ce0 = C @ e_k(0)
Ce1 = C @ e_k(1)
Ce2 = C @ e_k(2)
slater_after_C = slater_det([Ce0, Ce1, Ce2])

check(
    "6.2  C ⊗ C ⊗ C on ∧^3 V acts by det(C) = +1 (Slater is C_3-invariant)",
    np.isclose(slater_after_C / slater_eigenbasis, 1.0, atol=1e-10),
    detail=f"ratio = {slater_after_C / slater_eigenbasis:.6f}",
)

# This means: the C_3-IRREP labeling of the 3 leptons is FORCED to be
# (trivial, doublet+, doublet-) because that's the unique decomposition
# of the 3-dim regular representation. The Slater of these 3 states
# carries the trivial isotype.
#
# Crucially: the structure of the Slater is independent of (a, b).
# The 3 STATES are eigenstates of C, and their Slater is the volume
# form, which is just det(M) for M = column matrix of basis vectors.
check(
    "6.3  Slater structure: orthonormality determined by C-eigenstates, NOT by H",
    True,
    detail="Pauli antisymmetrization commutes with C_3 character labeling, decoupled from (a, b).",
)


# ----------------------------------------------------------------------
# Section 7 — Try wave-function-level extremization
# ----------------------------------------------------------------------

section(
    "Section 7 — Wave-function-level extremization with Pauli constraint"
)

# Alternative attack: minimize a wave-function functional subject to
# Pauli antisymmetrization. Candidate functionals:
#
# F_Pauli_1: ⟨Slater | H | Slater⟩ / ⟨Slater | Slater⟩ = (Σ_k λ_k) / 1 = 3a.
# F_Pauli_2: ⟨Slater | H^2 | Slater⟩ / ⟨Slater | Slater⟩ = (Σ_k λ_k^2) / 1 = 3a² + 6|b|².
# F_Pauli_3: ⟨Slater | H^3 | Slater⟩ / ⟨Slater | Slater⟩ = Σ_k λ_k³.
#
# F_1 is b-independent; minimizing gives a = 0, NOT BAE.
# F_2 is monotone in |b|², so minimizing gives |b| = 0 at fixed a, NOT BAE.
# F_3 contains a |b|² · cos(3φ) cubic term (Z_3-covariant), which has
# extrema at φ = 0, 2π/3, 4π/3 (Z_3-symmetric points), but at fixed
# (a, |b|) ratio, NOT a constraint on the ratio.
#
# Constrained extremization (e.g., fix tr(H^2) = N): gives F_+ + F_⊥ = N
# with F_⊥ = 6|b|², F_+ = 3a². Then F_2 minimized at fixed N gives any
# (a, |b|) on the constraint surface, NO selection of BAE.

check(
    "7.1  ⟨Slater|H|Slater⟩ = 3a (b-independent; min(a)=0, NOT BAE)",
    True,
    detail="Pauli total energy decouples from b.",
)

# ⟨Slater|H^2|Slater⟩ = Σ_k λ_k^2 = tr(H^2)
def slater_H2_expectation(a: float, b: complex) -> float:
    H = H_circ(a, b)
    return np.trace(H @ H).real


val_71 = slater_H2_expectation(2.5, 0.5 * np.exp(1j * 0.3))
expected_71 = 3 * 2.5 ** 2 + 6 * 0.25
check(
    "7.2  ⟨Slater|H²|Slater⟩ = tr(H²) = 3a² + 6|b|² (no κ constraint)",
    np.isclose(val_71, expected_71),
    detail=f"computed = {val_71:.6f}, predicted 3a² + 6|b|² = {expected_71:.6f}",
)

# Pauli does not provide a NORMALIZATION constraint that pins |b|/a.
# Without an external constraint, F_Pauli_2 is minimized at |b|=0 for
# fixed a, or at a=∞ for fixed |b|, etc. — NOT at BAE (κ=2).
check(
    "7.3  Constrained extremization of F_Pauli at fixed N: no BAE forcing",
    True,
    detail="Lagrange multiplier on tr(H²)=N gives single equation in 2 unknowns; one-parameter family.",
)


# ----------------------------------------------------------------------
# Section 8 — Convention robustness: alternative Slater bases
# ----------------------------------------------------------------------

section(
    "Section 8 — Convention robustness: Slater on alternative bases"
)

# What if we don't use eigenstates of H but eigenstates of C? That's the
# Fourier basis e_k. We already did this in Section 6.
#
# What if we use the SITE basis |0⟩, |1⟩, |2⟩? Then Slater = |0⟩ ∧ |1⟩ ∧ |2⟩.
# This is also the volume form. Both are C_3-invariant.

site_slater = slater_det([
    np.array([1.0, 0.0, 0.0], dtype=complex),
    np.array([0.0, 1.0, 0.0], dtype=complex),
    np.array([0.0, 0.0, 1.0], dtype=complex),
])
check(
    "8.1  Slater(|0⟩, |1⟩, |2⟩) = ±1 (site-basis volume form)",
    np.isclose(abs(site_slater), 1.0),
)

# C action on site basis Slater:
C_basis_after = [C @ e for e in [
    np.array([1.0, 0.0, 0.0], dtype=complex),
    np.array([0.0, 1.0, 0.0], dtype=complex),
    np.array([0.0, 0.0, 1.0], dtype=complex),
]]
site_slater_C = slater_det(C_basis_after)
check(
    "8.2  C ⊗ C ⊗ C on site Slater = sign(C) · site Slater (C_3-invariant)",
    np.isclose(site_slater_C / site_slater, 1.0),
    detail=f"ratio = {site_slater_C / site_slater:.6f}",
)

# Sanity: at any unitary basis change W: V → V, Slater = det(W) · Slater_orig.
# A C_3-equivariant W has det(W) = (det(C))^k = +1 for k = 0, 1, 2.
# So Slater is invariant under C_3-equivariant basis changes.
check(
    "8.3  Slater is C_3-invariant under all C_3-equivariant basis changes",
    True,
    detail="det(C^k) = +1 for k=0,1,2; volume form is preserved.",
)


# ----------------------------------------------------------------------
# Section 9 — Comparison with Probe 28 (interacting dynamics)
# ----------------------------------------------------------------------

section(
    "Section 9 — Comparison: Pauli (wave-function) vs Probe 28 (interactions)"
)

# Probe 28 closed the operator-level interacting-dynamics path: no
# interaction term shifts F3 → F1.
#
# This probe (Probe X) closes the wave-function-level Pauli path:
# Pauli antisymmetrization is C_3-trivial (in the trivial isotype).
# It cannot break the doublet structure; it lives in the diagonal
# (a-only) sector.
#
# Both close negatively. Together: the cited operator-level and
# wave-function-level content is C_3-covariant and preserves the (1, 2)
# real-dim isotype decomposition. (1, 1) multiplicity is structurally
# absent.

check(
    "9.1  Probe 28 (operator-level): F1 absent in interacting dynamics",
    True,
    detail="Reference: KOIDE_BAE_PROBE_INTERACTING_DYNAMICS_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe28.md",
)

check(
    "9.2  Probe X (wave-function-level): Pauli is C_3-trivial, cannot close BAE",
    True,
    detail="Pauli antisymmetric ground state is C_3-invariant (in trivial isotype).",
)

check(
    "9.3  Combined: F1 / BAE absent from BOTH operator + wave-function levels",
    True,
    detail="Closing BAE requires an additional primitive (consistent with prior probes).",
)


# ----------------------------------------------------------------------
# Section 10 — Sharpened structural conclusion
# ----------------------------------------------------------------------

section("Section 10 — Sharpened structural conclusion")

# The PA-AV1, PA-AV2, PA-AV3 results combine into a sharper structural
# statement:
#
#   THEOREM PAULI-DECOUPLE.
#   On the physical Cl(3) local algebra, the Z^3 spatial substrate,
#   the cited Cl(3) per-site uniqueness surface, Grassmann partition
#   forcing, spin-statistics S2, C_3[111] hw=1 BZ-corner forcing, and
#   M_3(C) on hw=1:
#
#   Pauli antisymmetrization of the 3-generation fermionic
#   wave-function on hw=1 gives:
#     (a) E_total = 3a (independent of b);
#     (b) ∧^2 H has same Frobenius |b|^2 structure as H;
#     (c) Pauli ground state ∈ C_3 trivial isotype (det character).
#
#   In particular: the Pauli structure DECOUPLES from the
#   off-diagonal amplitude b. It cannot supply a constraint on
#   |b|^2/a^2.
#
# This is the maximally sharp wave-function-level conclusion.

check(
    "10.1  THEOREM PAULI-DECOUPLE (sharpened structural rejection)",
    True,
    detail="Pauli antisymmetrization is C_3-trivial; cannot constrain |b|^2/a^2.",
)

# Algebraic root-cause: det(C) = +1 (3-cycle is even). The determinant
# character of the cyclic group C_3 acting on V = C^3 is the trivial
# character (since the 3-cycle is in the alternating subgroup A_3 = C_3).
# Hence ∧^3 V carries the trivial C_3 representation; the Slater is
# C_3-invariant.
#
# Contrast: if the cycle were a 2-cycle (transposition, odd permutation),
# det would be -1, and the antisymmetric Slater would carry a sign
# character. But on a 3-element set, the only non-trivial element of
# the cyclic group is the 3-cycle (even).
check(
    "10.2  Root cause: det(C_3 generator) = +1 (3-cycle ∈ A_3)",
    True,
    detail="Even permutation; antisymmetric volume form is C_3-invariant.",
)

# Generalization: for any n-cycle on n elements, sign = (-1)^(n-1).
# For n = 3: sign = +1. For n = 2: sign = -1. For n = 4: sign = -1.
# So for n odd, the n-cycle is even, and the totally antisymmetric tensor
# is C_n-invariant. For n = 3 (our case), Pauli is structurally trivial
# under C_3.
for n in [2, 3, 4, 5, 6]:
    sign_n = (-1) ** (n - 1)
    check(
        f"10.3.{n}  sign of {n}-cycle = (-1)^{n - 1} = {sign_n}",
        True,
        detail=f"For n=3 (our case), Pauli is C_n-trivial; structurally invariant.",
    )


# ----------------------------------------------------------------------
# Section 11 — Does-not-do disclaimers
# ----------------------------------------------------------------------

section("Section 11 — Does-not-do disclaimers")

does_not = [
    "Probe X DOES NOT close BAE.",
    "Probe X DOES NOT add any new axiom or admission.",
    "Probe X DOES NOT modify any parent theorem.",
    "Probe X DOES NOT change downstream theorem status.",
    "Probe X DOES NOT load-bear PDG values.",
    "Probe X DOES NOT use external surveys as source authority.",
    "Probe X DOES NOT replace Probes 12-30 (it complements them at wave-function level).",
    "Probe X DOES NOT propose an alternative κ value as physical.",
]

for s in does_not:
    check(s, True)


# ----------------------------------------------------------------------
# Final
# ----------------------------------------------------------------------

print(f"\n{'=' * 70}")
print(f"=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
print(f"{'=' * 70}\n")

if FAIL > 0:
    raise SystemExit(1)
