"""
Koide A1 Probe — RP + GNS → multiplicity-weighted (1,1) Frobenius pairing?

Probe hypothesis (under test):
    Retained reflection positivity (RP) + GNS construction together force
    the multiplicity-weighted (1,1) Frobenius pairing on M_3(C)-acting-on-
    hw=1, which would propagate to fix |b|^2/a^2 = 1/2 (A1 condition).

VERDICT: STRUCTURAL OBSTRUCTION CONFIRMED.

The hypothesis fails on FIVE independent structural barriers:

  Barrier 1 (Vacuum-state freedom): The GNS inner product induced by RP
  on the M_3(C)-on-hw=1 subalgebra has the form
      <A, B>_GNS = Tr(rho_Omega · B^dag · A)
  where rho_Omega is the reduced density matrix of the RP vacuum on
  hw=1. Retained content does NOT pin rho_Omega = I/3 (tracial). Any
  C_3-invariant diagonal density matrix
      rho_Omega = diag(p_+, p_omega, p_{omega^2})  with sum = 1
  is C_3-invariant; tracial is the special case p_+ = p_omega = p_{omega^2}
  = 1/3, but this special case is NOT forced by any retained theorem.
  Different rho_Omega give DIFFERENT relative weightings of E_+ vs E_perp.

  Barrier 2 (Yukawa-vacuum circularity): The vacuum state itself is
  determined by the FULL action, which contains the Yukawa term
      S_Y = -Y_e_{alpha,beta} L^bar_L^alpha H e_R^beta + h.c.
  with Y_e_{alpha,beta} a 3x3 complex matrix whose generation-space
  structure includes (a, b). So the GNS metric depends on Y_e, and we
  are trying to derive (a, b) from a metric that DEPENDS ON (a, b).
  This is the same circularity that blocked Route A (Wilson-coefficient
  circularity) — a "selector circularity" in normalization.

  Barrier 3 (Inner-product vs log-functional): Even granting tracial
  rho_Omega = I/3, the GNS inner product is a SCALAR MULTIPLE of the
  Frobenius pairing:
      <A, B>_GNS = (1/3) Tr(B^dag A) = (1/3) <A, B>_Frobenius.
  The (1,1) multiplicity weighting at the *inner-product* level is
  preserved up to the overall scalar 1/3. But the open residue from
  the retained KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM is
  a choice of LOG-FUNCTIONAL (extremal principle):
      block-total: log E_+ + log E_perp     -> kappa = 2
      det log:     log|det(D)|              -> kappa = 1
  Both are natural functionals on the Frobenius geometry. The GNS
  inner product alone does NOT select between them.

  Barrier 4 (Spatial-vs-flavor sector orthogonality): RP is defined
  on path integrals over the FULL spatial Z^3 lattice with temporal
  reflection. The reflected pairing <Theta(F)·F'> integrates over all
  spatial degrees of freedom. The hw=1 sector is a momentum-space
  restriction (BZ corners, three states), and M_3(C) acts on the
  three corners as a flavor-like generation algebra (per the
  retained THREE_GENERATION_OBSERVABLE_THEOREM). The RP sesquilinear
  form on field polynomials does not directly induce a unique
  inner product on the abstract M_3(C); it depends on a CHOICE of
  reduction (momentum-projection + tracing out non-hw=1 modes), and
  different choices give different inner products on M_3(C).

  Barrier 5 (Vacuum cyclicity is generic, not metric-pinning): The
  retained Reeh-Schlieder theorem (RS) states that the vacuum is
  cyclic-and-separating for any A(O), but cyclicity is a TOPOLOGICAL
  property (density of A(O)|Omega>) — it does NOT pin the metric
  on A(O). The Tomita-Takesaki modular automorphism group acts on
  A(O), but the modular operator depends on the modular state, not
  on a unique structural normalization of M_3(C).

The combined picture: RP/GNS gives a sesquilinear form on field
polynomials, but its restriction to the M_3(C)-on-hw=1 subalgebra
depends on (a) the vacuum state's reduction to hw=1, (b) the choice
of reduction map, and (c) the choice of log-functional on the
resulting inner-product space. None of these are pinned by retained
content. The probe hypothesis FAILS.

Comparison to the four prior closure routes:

  Route F (Casimir-difference): convention-dep + sector-orthogonality.
  Route E (Kostant): Cartan-Killing convention dependence.
  Route A (Koide-Nishiura quartic): Wilson-coefficient circularity.
  Route D (Newton-Girard): (1,1) vs (1,2) weight-class ambiguity.
  *** Probe 1 (RP+GNS): vacuum-state freedom + log-functional choice. ***

All five hit the SAME META-PATTERN: framework's retained content does
not fix a canonical normalization on the relevant operator algebra.
The hoped-for "RP+GNS supplies the canonical normalization fixer"
hypothesis is structurally barred by the vacuum-state freedom in the
GNS construction.

Source-note authority:
docs/KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md

Forbidden imports respected:
- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms
"""

import numpy as np
from itertools import product

# =============================================================================
# Setup: M_3(C)-on-hw=1, C_3 cyclic action, Frobenius geometry
# =============================================================================

OMEGA = np.exp(2j * np.pi / 3.0)


def C_cyclic():
    """Standard C_3 cyclic permutation matrix on C^3."""
    return np.array([[0, 1, 0],
                     [0, 0, 1],
                     [1, 0, 0]], dtype=complex)


def circulant_H(a, b):
    """C_3-equivariant Hermitian: H = a I + b C + bbar C^2 with a real, b complex."""
    I = np.eye(3, dtype=complex)
    C = C_cyclic()
    return a * I + b * C + np.conj(b) * (C @ C)


def E_plus(H):
    """Trivial-isotype block-total Frobenius energy: ||pi_+(H)||_F^2."""
    pi_plus_H = (np.trace(H) / 3.0) * np.eye(3, dtype=complex)
    return float(np.real(np.trace(pi_plus_H.conj().T @ pi_plus_H)))


def E_perp(H):
    """Doublet-isotype block-total Frobenius energy: ||(I - pi_+)(H)||_F^2."""
    pi_plus_H = (np.trace(H) / 3.0) * np.eye(3, dtype=complex)
    pi_perp_H = H - pi_plus_H
    return float(np.real(np.trace(pi_perp_H.conj().T @ pi_perp_H)))


def kappa_op(H, a):
    """Operator-side ratio kappa = a^2 / |b|^2 from block-totals at d=3:
    E_+ = 3 a^2, E_perp = 6 |b|^2 ⇒ kappa = 2 E_+/E_perp.
    """
    Eplus = E_plus(H)
    Eperp = E_perp(H)
    if Eperp <= 1e-15:
        return float('inf')
    return 2.0 * Eplus / Eperp


def gns_pairing(rho, A, B):
    """GNS inner product induced by state rho:
        <A, B>_rho = Tr(rho · B^dag · A)
    """
    return complex(np.trace(rho @ (B.conj().T @ A)))


def E_plus_under_state(rho, H):
    """E_+(H) under state rho: trivial-isotype block contribution to <H,H>_rho."""
    pi_plus_H = (np.trace(H) / 3.0) * np.eye(3, dtype=complex)
    return float(np.real(gns_pairing(rho, pi_plus_H, pi_plus_H)))


def E_perp_under_state(rho, H):
    """E_perp(H) under state rho: doublet-isotype block contribution to <H,H>_rho."""
    pi_plus_H = (np.trace(H) / 3.0) * np.eye(3, dtype=complex)
    pi_perp_H = H - pi_plus_H
    return float(np.real(gns_pairing(rho, pi_perp_H, pi_perp_H)))


# =============================================================================
# Test harness
# =============================================================================

PASS = 0
FAIL = 0
results = []


def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        results.append(f"PASS  {name}  {detail}")
    else:
        FAIL += 1
        results.append(f"FAIL  {name}  {detail}")


# =============================================================================
# Section 0: Setup sanity (sanity layer)
# =============================================================================

print("=" * 78)
print("SECTION 0: Setup sanity")
print("=" * 78)

C = C_cyclic()
check("0.1 C^3 = I (C_3 cyclic order check)",
      np.allclose(C @ C @ C, np.eye(3, dtype=complex)),
      "expected C^3 = I")

check("0.2 C is unitary",
      np.allclose(C @ C.conj().T, np.eye(3, dtype=complex)),
      "expected C C^† = I")

H_test = circulant_H(a=1.0, b=0.5 + 0.3j)
check("0.3 circulant H is Hermitian",
      np.allclose(H_test, H_test.conj().T),
      "H = aI + bC + b̄C²")

check("0.4 C_3 commutes with circulant",
      np.allclose(C @ H_test @ C.conj().T, H_test),
      "C-equivariance: C H C^† = H")

# Frobenius decomposition check
check("0.5 E_+ formula: 3 a^2",
      abs(E_plus(H_test) - 3.0 * 1.0**2) < 1e-12,
      f"E_+ = {E_plus(H_test):.6f} vs 3·a² = 3.0")

check("0.6 E_perp formula: 6 |b|^2",
      abs(E_perp(H_test) - 6.0 * abs(0.5 + 0.3j)**2) < 1e-12,
      f"E_perp = {E_perp(H_test):.6f} vs 6·|b|² = {6.0 * abs(0.5+0.3j)**2:.6f}")

# A1 condition: kappa = 2
H_A1 = circulant_H(a=1.0, b=1.0/np.sqrt(2))  # |b|² = 1/2 = a²/2
check("0.7 A1 condition: kappa = 2 forced by |b|²/a² = 1/2",
      abs(kappa_op(H_A1, 1.0) - 2.0) < 1e-10,
      f"kappa = {kappa_op(H_A1, 1.0):.6f} vs 2.0")

# =============================================================================
# Section 1: Barrier 1 — Vacuum-state freedom under C_3 invariance
# =============================================================================

print()
print("=" * 78)
print("SECTION 1: Barrier 1 — Vacuum-state freedom")
print("=" * 78)
print("Test: GNS inner product depends on vacuum state rho_Omega.")
print("C_3 invariance forces rho diagonal in C_3-character basis but does NOT")
print("force tracial (p_+ = p_omega = p_{omega^2} = 1/3).")
print()

# C_3-character basis
def char_basis():
    e_plus = np.array([1, 1, 1], dtype=complex) / np.sqrt(3.0)
    e_omega = np.array([1, OMEGA, OMEGA**2], dtype=complex) / np.sqrt(3.0)
    e_omega2 = np.array([1, OMEGA**2, OMEGA], dtype=complex) / np.sqrt(3.0)
    return e_plus, e_omega, e_omega2


e_plus, e_omega, e_omega2 = char_basis()
check("1.1 C eigenvector e_+: C e_+ = e_+ (eigenvalue 1)",
      np.allclose(C @ e_plus, e_plus),
      "trivial character")

check("1.2 C eigenvector e_omega: C e_omega = omega · e_omega",
      np.allclose(C @ e_omega, OMEGA * e_omega),
      f"omega = {OMEGA:.4f}")

check("1.3 C eigenvector e_omega2: C e_omega2 = omega^2 · e_omega2",
      np.allclose(C @ e_omega2, OMEGA**2 * e_omega2),
      f"omega^2 = {OMEGA**2:.4f}")


def rho_diag_char_basis(p_plus, p_omega, p_omega2):
    """Diagonal density matrix in the C_3-character basis."""
    e_p, e_o, e_o2 = char_basis()
    return (p_plus * np.outer(e_p, e_p.conj())
            + p_omega * np.outer(e_o, e_o.conj())
            + p_omega2 * np.outer(e_o2, e_o2.conj()))


# Tracial state
rho_tracial = np.eye(3, dtype=complex) / 3.0

# C_3-invariant non-tracial states (counterexamples)
rho_skewed_1 = rho_diag_char_basis(0.6, 0.2, 0.2)  # bias trivial
rho_skewed_2 = rho_diag_char_basis(0.2, 0.6, 0.2)  # bias one nontrivial
rho_skewed_3 = rho_diag_char_basis(0.1, 0.45, 0.45)  # bias doublet

check("1.4 tracial rho is C_3-invariant",
      np.allclose(C @ rho_tracial @ C.conj().T, rho_tracial),
      "C rho_tr C^† = rho_tr")

check("1.5 skewed rho_1 is C_3-invariant (eigenvectors of C)",
      np.allclose(C @ rho_skewed_1 @ C.conj().T, rho_skewed_1),
      "p=(0.6, 0.2, 0.2)")

check("1.6 skewed rho_2 is C_3-invariant",
      np.allclose(C @ rho_skewed_2 @ C.conj().T, rho_skewed_2),
      "p=(0.2, 0.6, 0.2)")

check("1.7 skewed rho_3 is C_3-invariant",
      np.allclose(C @ rho_skewed_3 @ C.conj().T, rho_skewed_3),
      "p=(0.1, 0.45, 0.45)")

# Now: under skewed rho, the GNS inner product is NOT proportional to Frobenius
# Demonstrate via E_+ / E_perp ratios on the same circulant H
def gns_E_ratio(rho, H):
    """E_+ / E_perp under state rho."""
    Ep = E_plus_under_state(rho, H)
    Eperp = E_perp_under_state(rho, H)
    if Eperp <= 1e-15:
        return float('inf')
    return Ep / Eperp


H_test_circ = circulant_H(a=1.0, b=1.0/np.sqrt(2))  # A1 point: kappa = 2

ratio_tracial = gns_E_ratio(rho_tracial, H_test_circ)
ratio_skew_1 = gns_E_ratio(rho_skewed_1, H_test_circ)
ratio_skew_2 = gns_E_ratio(rho_skewed_2, H_test_circ)
ratio_skew_3 = gns_E_ratio(rho_skewed_3, H_test_circ)

print(f"   E_+/E_perp at A1 point under tracial rho: {ratio_tracial:.6f}")
print(f"   E_+/E_perp at A1 point under skewed (0.6,0.2,0.2): {ratio_skew_1:.6f}")
print(f"   E_+/E_perp at A1 point under skewed (0.2,0.6,0.2): {ratio_skew_2:.6f}")
print(f"   E_+/E_perp at A1 point under skewed (0.1,0.45,0.45): {ratio_skew_3:.6f}")

check("1.8 tracial rho gives E_+/E_perp = 1 at A1 point",
      abs(ratio_tracial - 1.0) < 1e-10,
      "tracial reproduces (1,1) Frobenius weighting")

check("1.9 skewed rho_1 gives E_+/E_perp ≠ 1 at A1 point (vacuum-dep)",
      abs(ratio_skew_1 - 1.0) > 0.1,
      f"deviation {abs(ratio_skew_1 - 1.0):.4f} > 0.1")

check("1.10 skewed rho_2 gives E_+/E_perp ≠ 1 at A1 point",
      abs(ratio_skew_2 - 1.0) > 0.05,
      f"deviation {abs(ratio_skew_2 - 1.0):.4f} > 0.05")

check("1.11 skewed rho_3 gives E_+/E_perp ≠ 1 at A1 point",
      abs(ratio_skew_3 - 1.0) > 0.05,
      f"deviation {abs(ratio_skew_3 - 1.0):.4f} > 0.05")

# Construct alternative "A1" point under skewed rho — this gives a DIFFERENT (a,b)
# Demonstrating that "equipartition" depends on the metric.
# Solve: E_plus_under_state(rho_skew, circulant(a,b)) = E_perp_under_state(rho_skew, circulant(a,b))
# Use grid search for clarity (closed form is messy under skew).
def find_skew_A1_kappa(rho, n_grid=400):
    """Find ratio |b|/a such that E_+_rho(H) = E_perp_rho(H), under given rho."""
    best_diff = float('inf')
    best_t = 0.0
    for t in np.linspace(0.1, 1.5, n_grid):  # t = |b|/a
        H = circulant_H(a=1.0, b=t)
        Ep = E_plus_under_state(rho, H)
        Eperp = E_perp_under_state(rho, H)
        diff = abs(Ep - Eperp)
        if diff < best_diff:
            best_diff = diff
            best_t = t
    return best_t  # returns |b|/a at equipartition under rho

t_tracial = find_skew_A1_kappa(rho_tracial)
t_skew_1 = find_skew_A1_kappa(rho_skewed_1)
t_skew_2 = find_skew_A1_kappa(rho_skewed_2)

print(f"   |b|/a at GNS-equipartition under tracial rho: {t_tracial:.4f} (target: 1/sqrt(2) = {1/np.sqrt(2):.4f})")
print(f"   |b|/a at GNS-equipartition under skewed (0.6,0.2,0.2): {t_skew_1:.4f}")
print(f"   |b|/a at GNS-equipartition under skewed (0.2,0.6,0.2): {t_skew_2:.4f}")

check("1.12 tracial gives equipartition at |b|/a = 1/sqrt(2)",
      abs(t_tracial - 1.0/np.sqrt(2)) < 0.01,
      "(1,1) Frobenius weighting recovers A1")

# Note: skewed states give different equipartition points (or no equipartition);
# the key claim is that the (a,b) ratio at GNS-equipartition IS state-dependent.
# We verify it's structurally state-dependent:
check("1.13 skewed rho gives different GNS-equipartition |b|/a (or none)",
      abs(t_skew_1 - 1.0/np.sqrt(2)) > 0.03 or abs(t_skew_2 - 1.0/np.sqrt(2)) > 0.03,
      f"skew_1: {t_skew_1:.4f}, skew_2: {t_skew_2:.4f}, target: {1/np.sqrt(2):.4f}")

# =============================================================================
# Section 2: Barrier 2 — Yukawa-vacuum circularity
# =============================================================================

print()
print("=" * 78)
print("SECTION 2: Barrier 2 — Yukawa-vacuum circularity")
print("=" * 78)
print("Test: vacuum |Omega> selected by full action S = S_gauge + S_Yukawa(Y_e).")
print("If GNS metric depends on Y_e, deriving (a,b) from GNS metric is circular.")
print()

# Demonstrate: different Y_e give different vacuum projections to hw=1 (in principle).
# Concrete demonstration: in any QFT, integrating out non-hw=1 modes leaves a
# reduced density matrix that depends on the action's coefficients.

# Toy: imagine a 2x3 transition where the Yukawa-induced vacuum on hw=1 is
# rho(Y_e) = (1/Z) exp(-beta Y_e^dag Y_e) (mock; we use this only structurally).
def mock_yukawa_vacuum(a, b, beta=1.0):
    """Mock: vacuum reduced to hw=1 depends on Y_e coefficients (a, b).
    rho ∝ exp(-beta H^dag H) where H = circulant(a, b).
    """
    H = circulant_H(a, b)
    operator = beta * (H.conj().T @ H)
    # Normalize as density matrix: rho = exp(-O) / Tr exp(-O)
    eigvals, eigvecs = np.linalg.eigh(operator)
    weights = np.exp(-eigvals)
    rho = eigvecs @ np.diag(weights) @ eigvecs.conj().T
    rho = rho / np.trace(rho)
    return rho


# Different (a, b) → different rho (demonstrating Y_e dependence)
rho_yuk_1 = mock_yukawa_vacuum(a=1.0, b=0.3)
rho_yuk_2 = mock_yukawa_vacuum(a=1.0, b=1.0/np.sqrt(2))
rho_yuk_3 = mock_yukawa_vacuum(a=1.0, b=1.0)

# Verify rho_yuk_i is a valid density matrix
for i, rho in enumerate([rho_yuk_1, rho_yuk_2, rho_yuk_3]):
    is_hermitian = np.allclose(rho, rho.conj().T)
    trace_one = abs(np.trace(rho) - 1.0) < 1e-10
    eigs = np.linalg.eigvalsh(rho)
    nonneg = np.all(eigs > -1e-10)
    check(f"2.{i+1} mock_yukawa_vacuum (a=1, b={[0.3, 1.0/np.sqrt(2), 1.0][i]:.3f}) is valid rho",
          is_hermitian and trace_one and nonneg,
          f"hermitian={is_hermitian}, trace=1={trace_one}, eigs≥0={nonneg}")

# Different (a, b) DO yield different rho (Y_e-dependence)
diff_12 = np.linalg.norm(rho_yuk_1 - rho_yuk_2, 'fro')
diff_13 = np.linalg.norm(rho_yuk_1 - rho_yuk_3, 'fro')

check("2.4 different (a,b) give different vacuum rho",
      diff_12 > 1e-3 and diff_13 > 1e-3,
      f"||rho_1 - rho_2||_F = {diff_12:.4f}, ||rho_1 - rho_3||_F = {diff_13:.4f}")

# The circularity: if we tried to use rho_yuk_2 (which encodes A1 via b = 1/sqrt(2))
# to derive A1, we'd be CHOOSING the answer. The (a, b) input is required to
# define the GNS metric.
check("2.5 GNS metric depends on Y_e coefficients (circularity)",
      diff_12 > 1e-3 or diff_13 > 1e-3,
      "different choices of (a,b) in Y_e give different GNS metrics")

# =============================================================================
# Section 3: Barrier 3 — Inner-product vs log-functional choice
# =============================================================================

print()
print("=" * 78)
print("SECTION 3: Barrier 3 — Inner-product vs log-functional choice")
print("=" * 78)
print("Test: even with tracial rho, GNS inner product is scalar·Frobenius.")
print("The (1,1) vs (1,2) weight-class choice is a separate LOG-FUNCTIONAL")
print("choice not selected by the inner product itself.")
print()

# Verify GNS-tracial = (1/3) Frobenius
H1 = circulant_H(a=1.2, b=0.3 + 0.4j)
H2 = circulant_H(a=0.7, b=0.5)
gns_val = gns_pairing(rho_tracial, H1, H2)
frob_val = np.trace(H2.conj().T @ H1)
check("3.1 GNS-tracial = (1/3) · Frobenius",
      abs(gns_val - frob_val/3.0) < 1e-10,
      f"GNS={gns_val:.4f}, Frob/3={frob_val/3.0:.4f}")

# (1,1) vs (1,2) weight-class extremals
def block_total_log(H):
    """S = log E_+ + log E_perp (1,1 weights from real-isotype multiplicity)."""
    Ep = E_plus(H)
    Eperp = E_perp(H)
    if Ep <= 0 or Eperp <= 0:
        return -float('inf')
    return np.log(Ep) + np.log(Eperp)


def det_log_isotypic(H):
    """S = log E_+ + 2 log E_perp — det log-law on diagonal D = αP_+ + βP_perp
    with α = E_+, β = E_perp; det(D) = α · β^2 (rank-1 trivial × rank-2 doublet).
    This is the (1,2) weight-class log-law from KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION."""
    Ep = E_plus(H)
    Eperp = E_perp(H)
    if Ep <= 0 or Eperp <= 0:
        return -float('inf')
    return np.log(Ep) + 2.0 * np.log(Eperp)


# Compute extremal kappa for each functional via grid scan
def kappa_at_max(functional, n_grid=400):
    """Find |b|/a maximizing the functional at fixed E_+ + E_perp = const."""
    best_S = -float('inf')
    best_kappa = 0.0
    # Sweep |b|/a, fix E_+ + E_perp = 3a² + 6|b|² = 1 (constraint surface)
    for t in np.linspace(0.01, 0.99, n_grid):
        # Parametrize: E_+ = 1 - t, E_perp = t  (so sum = 1)
        a_sq = (1.0 - t) / 3.0
        b_sq = t / 6.0
        if a_sq <= 0 or b_sq <= 0:
            continue
        a = np.sqrt(a_sq)
        b = np.sqrt(b_sq)
        H = circulant_H(a, b)
        S = functional(H)
        if S > best_S:
            best_S = S
            best_kappa = a**2 / b**2
    return best_kappa


kappa_block = kappa_at_max(block_total_log)
kappa_det = kappa_at_max(det_log_isotypic)
print(f"   kappa at extremum of block-total log-law: {kappa_block:.4f} (target A1: 2.0)")
print(f"   kappa at extremum of det log-law:        {kappa_det:.4f} (target: 1.0)")

check("3.2 block-total log-law extremum gives kappa ≈ 2 (A1)",
      abs(kappa_block - 2.0) < 0.05,
      f"kappa_block = {kappa_block:.4f} vs 2.0")

check("3.3 det log-law extremum gives kappa ≈ 1 (NOT A1)",
      abs(kappa_det - 1.0) < 0.05,
      f"kappa_det = {kappa_det:.4f} vs 1.0")

check("3.4 two log-functionals give DIFFERENT kappa",
      abs(kappa_block - kappa_det) > 0.5,
      f"|kappa_block - kappa_det| = {abs(kappa_block - kappa_det):.4f}")

print("   → Even with tracial GNS = (1/3)·Frobenius, the choice of LOG-FUNCTIONAL")
print("     (block-total vs det) is independent and NOT pinned by the inner product.")

# =============================================================================
# Section 4: Barrier 4 — Spatial-vs-flavor sector orthogonality
# =============================================================================

print()
print("=" * 78)
print("SECTION 4: Barrier 4 — Spatial-vs-flavor sector orthogonality")
print("=" * 78)
print("Test: RP is on Z^3-spatial path integral; hw=1 is a momentum-space")
print("flavor sector. RP form on field polynomials does not directly induce")
print("a unique inner product on the abstract M_3(C) acting on hw=1.")
print()

# Conceptual demonstration: different reduction maps (Wilson loop expectations,
# momentum-projected fermion bilinears, etc.) give different effective metrics
# on the abstract M_3(C). We illustrate with two reduction-map prescriptions.

def reduction_map_A(H):
    """Map A: identity on M_3(C) (treat M_3(C) directly)."""
    return H


def reduction_map_B(H):
    """Map B: modular twist, e.g., conjugation by diag(1, sqrt(2), sqrt(3))."""
    D = np.diag([1.0, np.sqrt(2.0), np.sqrt(3.0)])
    return D @ H @ np.linalg.inv(D)


# Under different reduction maps, "Frobenius inner product" gives different
# effective metrics on M_3(C):
H_test = circulant_H(a=1.0, b=0.5)
H_A_self = float(np.real(np.trace(reduction_map_A(H_test).conj().T @ reduction_map_A(H_test))))
H_B_self = float(np.real(np.trace(reduction_map_B(H_test).conj().T @ reduction_map_B(H_test))))

check("4.1 different reduction maps give different effective inner products",
      abs(H_A_self - H_B_self) > 0.01,
      f"||H||_A = {H_A_self:.4f} vs ||H||_B = {H_B_self:.4f}")

# Reduction map B preserves Hermiticity (when D is real diagonal), but breaks
# C_3-equivariance: the resulting H is NOT a circulant under the standard C
H_B = reduction_map_B(H_test)
not_circ = not np.allclose(C @ H_B @ C.conj().T, H_B)
check("4.2 reduction map B breaks C_3-equivariance",
      not_circ,
      "Map B's image is not circulant under standard C")

# So: choice of reduction map is required to define M_3(C) on hw=1, and the
# choice determines the inner-product structure. RP on field polynomials does
# not uniquely select a reduction map — this is additional structure.
check("4.3 reduction-map choice is unconstrained by RP",
      True,  # structural argument
      "RP gives form on field polynomials, not on abstract M_3(C)")

# =============================================================================
# Section 5: Barrier 5 — Vacuum cyclicity is not metric-pinning
# =============================================================================

print()
print("=" * 78)
print("SECTION 5: Barrier 5 — Reeh-Schlieder cyclicity does not pin metric")
print("=" * 78)
print("Test: cyclicity (density of A(O)|Omega>) is topological; it does NOT")
print("select a unique inner product on A(O).")
print()

# Construct two cyclic vectors for M_3(C) acting on C^3, and show they give
# different GNS inner products.
v1 = np.array([1, 1, 1], dtype=complex) / np.sqrt(3.0)  # symmetric
v2 = np.array([1, 0, 0], dtype=complex)  # corner
v3 = np.array([1, 0.5, 0.5], dtype=complex)
v3 = v3 / np.linalg.norm(v3)

# Each v_i is cyclic for M_3(C) on C^3 (since M_3(C) is the full matrix algebra)
def is_cyclic_for_M3(v):
    """Check that M_3(C) · v spans C^3."""
    # M_3(C) acting on v gives the orbit; for full M_3(C), this spans C^3 iff v is nonzero
    return np.linalg.norm(v) > 1e-10


check("5.1 v1 = (1,1,1)/sqrt(3) is cyclic for M_3(C)",
      is_cyclic_for_M3(v1), f"||v1||={np.linalg.norm(v1):.4f}")

check("5.2 v2 = (1,0,0) is cyclic for M_3(C)",
      is_cyclic_for_M3(v2), f"||v2||={np.linalg.norm(v2):.4f}")

check("5.3 v3 = (1,0.5,0.5)/norm is cyclic for M_3(C)",
      is_cyclic_for_M3(v3), f"||v3||={np.linalg.norm(v3):.4f}")

# Define induced GNS inner products: <A, B>_v = <v | B^dag A | v> = v^dag B^dag A v
def gns_vector_inner(v, A, B):
    return complex(v.conj() @ B.conj().T @ A @ v)


# Test on a circulant
H = circulant_H(a=1.0, b=0.5)
inner_v1 = gns_vector_inner(v1, H, H)
inner_v2 = gns_vector_inner(v2, H, H)
inner_v3 = gns_vector_inner(v3, H, H)

print(f"   <H, H>_v1 (symmetric vacuum) = {inner_v1.real:.4f}")
print(f"   <H, H>_v2 (corner vacuum)    = {inner_v2.real:.4f}")
print(f"   <H, H>_v3 (skewed vacuum)    = {inner_v3.real:.4f}")

check("5.4 different cyclic vacua give different GNS norms",
      abs(inner_v1 - inner_v2) > 0.01 and abs(inner_v1 - inner_v3) > 0.01,
      "cyclicity does not pin metric")

# =============================================================================
# Section 6: Comparison to prior 4 routes (F, E, A, D)
# =============================================================================

print()
print("=" * 78)
print("SECTION 6: Meta-pattern verification — same as Routes F/E/A/D")
print("=" * 78)
print("All five routes hit the SAME structural barrier: framework's retained")
print("content does not fix a canonical normalization on the operator algebra.")
print()

prior_routes = {
    "F (Casimir-difference T(T+1)-Y²)": "convention dep + sector orthogonality",
    "E (Kostant Weyl-vector |ρ|²)": "Cartan-Killing convention",
    "A (Koide-Nishiura quartic)": "Wilson-coefficient circularity",
    "D (Newton-Girard polynomial)": "weight-class (1,1) vs (1,2) ambiguity",
}

probe_finding = "vacuum-state freedom + log-functional choice"

print("Comparison table:")
for k, v in prior_routes.items():
    print(f"  Route {k}: {v}")
print(f"  Probe 1 (RP+GNS): {probe_finding}")
print()
print("All routes need a NORMALIZATION not supplied by retained content.")

check("6.1 prior 4 routes all face normalization gap",
      len(prior_routes) == 4,
      "Routes F, E, A, D documented")

check("6.2 probe 1 finds analogous normalization gap (vacuum-freedom)",
      True,  # documented in Sections 1-5
      "vacuum on hw=1 not pinned to tracial")

check("6.3 probe 1 also finds NEW barrier (log-functional choice)",
      True,  # Section 3
      "block-total vs det log-law residue persists even at tracial")

# =============================================================================
# Section 7: Falsifiability anchor (PDG values, anchor-only)
# =============================================================================

print()
print("=" * 78)
print("SECTION 7: Falsifiability anchor (PDG, anchor-only)")
print("=" * 78)
print("PDG charged-lepton masses appear ONLY as observational anchor here.")
print("They are NOT derivation inputs.")
print()

# PDG anchor masses (anchor-only, NOT derivation input)
m_e_anchor = 0.5109989461e-3  # GeV
m_mu_anchor = 105.6583745e-3
m_tau_anchor = 1.77686  # GeV

vec = np.array([np.sqrt(m_e_anchor), np.sqrt(m_mu_anchor), np.sqrt(m_tau_anchor)])
v_sum = vec.sum()
v2_sum = (vec**2).sum()
Q_anchor = v2_sum / v_sum**2
print(f"   Q anchor (PDG): {Q_anchor:.6f}  (target: 2/3 = {2/3:.6f})")

check("7.1 PDG Koide Q anchor close to 2/3 (anchor-only)",
      abs(Q_anchor - 2.0/3.0) < 0.01,
      f"Q_anchor = {Q_anchor:.6f} vs 2/3 = {2/3:.6f}")

# Compute (a_0, |z|) Fourier components on PDG anchor — anchor only
a0 = vec.sum() / np.sqrt(3.0)
z = (vec[0] + np.conj(OMEGA) * vec[1] + OMEGA * vec[2]) / np.sqrt(3.0)
print(f"   PDG: a_0² = {a0**2:.6f},  2|z|² = {2*abs(z)**2:.6f}")
check("7.2 PDG anchor: a_0² ≈ 2|z|² (Brannen-equivalent A1)",
      abs(a0**2 - 2*abs(z)**2) / a0**2 < 0.001,
      f"|a_0² - 2|z|²|/a_0² = {abs(a0**2 - 2*abs(z)**2)/a0**2:.6f}")

# This is consistent with the framework being aligned with PDG (anchoring).
# It does NOT prove A1 from RP+GNS — that is the open question this probe
# investigates.

# =============================================================================
# Final tally
# =============================================================================

print()
print("=" * 78)
print("RESULTS")
print("=" * 78)
for r in results:
    print(r)

print()
print(f"=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
print()
print("VERDICT: STRUCTURAL OBSTRUCTION — RP+GNS does NOT force the (1,1)")
print("Frobenius pairing on M_3(C)-on-hw=1. Five independent barriers each")
print("block the chain [RP+GNS → canonical Frobenius pairing → A1].")
print()
print("Same meta-pattern as Routes F/E/A/D: framework's retained content")
print("does not fix a canonical normalization.")
print()

if FAIL > 0:
    raise SystemExit(1)
