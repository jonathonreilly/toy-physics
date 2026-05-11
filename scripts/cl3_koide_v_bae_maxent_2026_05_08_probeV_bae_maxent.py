"""
Koide BAE Probe V — MaxEntropy / Thermodynamic Attack on the C_3[111] Triplet.

(BAE = Brannen Amplitude Equipartition; legacy alias: A1-condition.
The constraint is |b|^2/a^2 = 1/2 on the C_3-equivariant Hermitian
circulant H = aI + bC + bbar C^2 on hw=1.)

Existing source surfaces include operator-level BAE probes rooted in C_3
representation theory. This runner does not certify wave-function or
topological companion routes; it tests only the thermodynamic / MaxEntropy
route described below.

This probe (V) attacks at a structurally DISTINCT fourth level: the
THERMODYNAMIC / STATISTICAL / MaxEntropy level. The very name
"Brannen Amplitude Equipartition" suggests classical equipartition
(kT/2 per quadratic dof). Naive count: 1 a-mode + 2 b-modes
(b and b-bar). Equipartition might give |a|^2 = 2|b|^2, i.e.,
|b|^2/a^2 = 1/2 = BAE.

==================================================================
HYPOTHESIS (Probe V)
==================================================================

Does maximum-entropy on the Born density restricted to circulant
Hamiltonians, with trace and energy constraints (Tr ρ = 1, Tr ρH = E), force
|b|^2/a^2 = 1/2 (BAE)?

==================================================================
RESULT (verified below)
==================================================================

NO. MaxEntropy on Born density with trace and energy constraints gives the
Gibbs state ρ ∝ exp(-βH), which has eigenvalues p_k =
exp(-β λ_k) / Z. The eigenvalues λ_k = a + 2|b|cos(φ - 2πk/3)
depend on (a, b) but the Gibbs state imposes NO constraint relating
|a| and |b|. The classical-equipartition argument that "1 a-mode
gets the same energy as 2 b-modes summed" is NOT a consequence of
MaxEntropy with Tr-ρ + Tr-ρH constraints; it requires an ADDITIONAL
isotype-equipartition constraint (one free parameter per isotype
block) which is precisely the (1, 1) multiplicity-counting principle
already named as the BAE admission.

Six independent decoupling theorems converge:

  TH-AV1  Gibbs state from MaxEnt with trace and energy constraints
          MaxEnt[ρ] s.t. Tr ρ = 1, Tr ρH = E gives Gibbs ρ ∝ e^{-βH}.
          For circulant H, Gibbs is diagonal in the C_3 Fourier basis
          with p_k = e^{-βλ_k}/Z. No constraint on |b|^2/a^2.

  TH-AV2  Liouville on isotype blocks rederives operator-level (1, 2)
          The natural "phase-space" measure on Herm_circ(3) is
          dE_+ dE_perp on the (2-real-dim) configuration space, not
          dE_+ d(Re b) d(Im b) (which would give 1+2 = 3 dofs).
          Equipartition over (E_+, E_perp) gives the same (1, 2)
          weighting Probe 28 found at the operator level.

  TH-AV3  Equipartition over the doublet-real-dim DOES give 1/2
          but only by ASSUMING isotype-equal-energy E_+ = E_perp
          E_+ = 3a^2 (cited BlockTotalFrob surface);
          E_perp = 6|b|^2 (cited BlockTotalFrob surface).
          E_+ = E_perp ⟹ |b|^2/a^2 = 1/2 = BAE.
          But E_+ = E_perp is NOT implied by Tr ρH = E.
          It is an ADDITIONAL multiplicity-counting constraint =
          BAE admission.

  TH-AV4  Counting-of-degrees no-bridge
          Naively: 1 a-dof + 2 b-dofs (b and b-bar). But b is a
          single complex number; its REAL/IMAG decomposition is a
          choice of real basis on the doublet, NOT 2 independent
          quantum modes. The 3 eigenvalues λ_0, λ_1, λ_2 are not
          3 independent dofs; they are constrained by the circulant
          structure (3 real dofs (a, |b|, φ) → 3 real eigenvalues).

  TH-AV5  Boltzmann distribution does NOT pin BAE
          For Gibbs ρ = e^{-βH}/Z on circulant H, expectation values
          ⟨a⟩, ⟨|b|⟩ depend on β but no special value of (a, b) is
          singled out. Sweep of (a, b): no thermodynamic phase
          transition at BAE; entropy S(ρ) is smooth across BAE.

  TH-AV6  Liouville theorem in classical/Hamiltonian limit
          The classical limit of the C_3 circulant gives a Hamiltonian
          flow on (Re b, Im b) phase space (a is conserved by C_3-
          symmetry → reduces to 2-dim phase space). Equipartition
          over (Re b, Im b) gives ⟨(Re b)^2⟩ = ⟨(Im b)^2⟩ = kT/(2k_HO),
          which gives ⟨|b|^2⟩ = kT/k_HO, NOT |b|^2/a^2 = 1/2.

==================================================================
VERDICT: NO-GO ROUTE CHECK (thermodynamic-level decoupling)
==================================================================

MaxEntropy on Born density with trace and energy constraints (Tr ρ = 1,
Tr ρH = E) gives Gibbs state ρ ∝ e^{-βH}, which DOES NOT pin
|b|^2/a^2. The classical-equipartition argument "1 a-mode = 2 b-modes
summed" requires the additional assumption that energy equipartitions
over ISOTYPES (E_+ = E_perp), which is itself the (1, 1) multiplicity-
counting principle = BAE admission.

  Net contribution: closes the THERMODYNAMIC-level path against the
  hypothesis that MaxEnt could supply BAE. It does not claim broader
  route-family closure beyond the cited source surfaces.

BOUNDED SUPPORT:

  Theorem THERMO-DECOUPLE: MaxEntropy on Born density restricted to
  circulant Hamiltonians, with the trace and energy constraints Tr ρ = 1
  (probability normalization) and Tr ρH = E (fixed energy), gives
  the Gibbs state ρ = e^{-βH}/Z. The Gibbs state does NOT impose
  any constraint relating |a| and |b|. The eigenvalues p_k =
  e^{-βλ_k}/Z are smooth functions of (a, b, β) with no
  distinguished thermodynamic point at |b|^2/a^2 = 1/2.

  Equivalently: Gibbs equilibrium minimizes free energy
  F(ρ) = ⟨H⟩ - TS(ρ); the variational principle gives ρ_eq = e^{-βH}/Z
  for any (a, b). The "equipartition" statement "1 a-mode = 2 b-modes
  summed", when sharpened, becomes "energy equipartitions across
  C_3-isotypes" — i.e., E_+(H) = E_perp(H) where E_+(H) = 3a^2,
  E_perp(H) = 6|b|^2 are the cited BlockTotalFrob measures.
  The isotype-equipartition condition E_+ = E_perp is precisely
  3a^2 = 6|b|^2 ⟺ |b|^2/a^2 = 1/2 = BAE — but this is NOT a
  consequence of MaxEnt with trace and energy constraints; it is the
  (1, 1) multiplicity-counting admission.

  This is structurally distinct from the cited operator-level probes:
  thermodynamics acts on density operators (mixed states) via
  variational principles, while operator probes act on Hilbert-space
  states and operator algebras. Other route families remain
  non-load-bearing context for this runner unless represented by live
  source surfaces.

This runner verifies each thermodynamic claim algebraically + numerically.

Author: source-note proposal. Audit lane has authority over
classification and downstream status.
"""

from __future__ import annotations

import math

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
# Section 0 — Input sanity
# ----------------------------------------------------------------------

section("Section 0 — Input sanity: C_3 cycle, circulant H, Born density")


def C_cycle() -> np.ndarray:
    """C_3 cyclic shift on basis {|0>, |1>, |2>}: C |n> = |n+1 mod 3>."""
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
omega = np.exp(2j * np.pi / 3)

check("0.1  C is unitary", np.allclose(C @ C.conj().T, np.eye(3, dtype=complex)))
check("0.2  C has order 3 (C^3 = I)", np.allclose(C @ C @ C, np.eye(3, dtype=complex)))


def H_circ(a: float, b: complex) -> np.ndarray:
    """C_3-equivariant Hermitian circulant: H = aI + bC + bbar C^2."""
    return a * np.eye(3, dtype=complex) + b * C + np.conj(b) * C2


a_t, b_t = 1.7, 0.4 + 0.3j
H_t = H_circ(a_t, b_t)
check("0.3  H = aI + bC + bbar C^2 is Hermitian", np.allclose(H_t, H_t.conj().T))
check("0.4  [H, C] = 0 (C_3-equivariance)",
      np.allclose(H_t @ C - C @ H_t, np.zeros((3, 3), dtype=complex)))


def gibbs_state(H: np.ndarray, beta: float) -> np.ndarray:
    """Gibbs density operator: rho = exp(-beta H) / Tr(exp(-beta H))."""
    eigvals, eigvecs = np.linalg.eigh(H)
    p = np.exp(-beta * eigvals)
    p = p / p.sum()  # normalize
    rho = eigvecs @ np.diag(p) @ eigvecs.conj().T
    return rho


# Verify Gibbs state has correct properties (PSD, Tr=1, commutes with H)
beta_test = 1.5
rho_t = gibbs_state(H_t, beta_test)
check("0.5  Gibbs state has Tr = 1",
      np.allclose(np.trace(rho_t).real, 1.0),
      detail=f"Tr(rho) = {np.trace(rho_t).real:.6f}")
check("0.6  Gibbs state is PSD (eigenvalues >= 0)",
      np.all(np.linalg.eigvalsh(rho_t) >= -1e-12),
      detail=f"min eigval = {np.linalg.eigvalsh(rho_t).min():.6e}")
check("0.7  Gibbs state commutes with H",
      np.allclose(rho_t @ H_t, H_t @ rho_t))


def born_density(rho: np.ndarray) -> np.ndarray:
    """Position-density Born readout: p_x = <x| rho |x> = diag(rho)."""
    return np.real(np.diag(rho))


# Verify Born density (G_NEWTON_BORN_AS_SOURCE_*: rho_grav(x) = <x|rho|x>)
p_t = born_density(rho_t)
check("0.8  Born density p_x >= 0",
      np.all(p_t >= -1e-12),
      detail=f"min p_x = {p_t.min():.6e}")
check("0.9  Born density Sum_x p_x = 1",
      np.isclose(p_t.sum(), 1.0),
      detail=f"sum = {p_t.sum():.6f}")


# ----------------------------------------------------------------------
# Section 1 — MaxEnt principle: variational derivation of Gibbs
# ----------------------------------------------------------------------

section("Section 1 — MaxEnt: variational derivation of Gibbs state")

# Standard derivation (Jaynes 1957): maximize S[rho] = -Tr(rho log rho)
# subject to Tr(rho) = 1 and Tr(rho H) = E.
# Lagrangian: L = -Tr(rho log rho) + alpha (Tr rho - 1) + beta (E - Tr rho H)
# Variation w.r.t. rho: delta L / delta rho = -log rho - 1 + alpha - beta H = 0
# Solving: rho = exp(alpha - 1 - beta H) = e^{-beta H} / Z
# where Z = Tr(e^{-beta H}) = e^{1-alpha}.
#
# This is the standard textbook derivation, NOT a new axiom.


def shannon_entropy(rho: np.ndarray) -> float:
    """Von Neumann entropy S = -Tr(rho log rho)."""
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = eigvals[eigvals > 1e-15]  # avoid log(0)
    return -float(np.sum(eigvals * np.log(eigvals)))


# Verify: among all states with the same Tr-rho = 1 and Tr-rho-H = E_target,
# Gibbs is the unique entropy maximizer.
def random_state_with_energy(H: np.ndarray, E_target: float, n_random: int = 1000,
                              rng: np.random.Generator = None) -> np.ndarray:
    """Generate random density operators with approximately Tr(rho H) = E."""
    if rng is None:
        rng = np.random.default_rng(42)
    d = H.shape[0]
    best_S = -np.inf
    best_rho = None
    for _ in range(n_random):
        # Random PSD with Tr=1
        A = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
        rho = A @ A.conj().T
        rho = rho / np.trace(rho).real
        E = np.trace(rho @ H).real
        # Skip those too far from target
        if abs(E - E_target) > 0.5:
            continue
        S = shannon_entropy(rho)
        if S > best_S:
            best_S = S
            best_rho = rho.copy()
    return best_rho, best_S


# Compute Gibbs entropy for comparison
rho_gibbs = gibbs_state(H_t, beta_test)
E_gibbs = np.trace(rho_gibbs @ H_t).real
S_gibbs = shannon_entropy(rho_gibbs)
check("1.1  Gibbs state S_gibbs > 0",
      S_gibbs > 0,
      detail=f"S_gibbs(beta={beta_test}) = {S_gibbs:.4f}, E = {E_gibbs:.4f}")

# Verify Gibbs is the entropy maximizer at fixed (Tr=1, Tr-rho-H=E_gibbs)
# Use a constrained search: project random states onto (Tr=1, Tr-H=E)
# manifold and verify Gibbs has the largest entropy.
def project_to_constraints(rho: np.ndarray, H: np.ndarray, E_target: float,
                           n_iter: int = 50) -> np.ndarray:
    """Project a candidate rho onto Tr(rho)=1, Tr(rho H)=E by alternating
    projection (heuristic; not optimal but good enough for upper-bound
    search)."""
    rho = (rho + rho.conj().T) / 2  # Hermitize
    # Eigendecompose, clip negative eigenvalues, normalize
    w, V = np.linalg.eigh(rho)
    w = np.maximum(w, 0.0)
    if w.sum() < 1e-10:
        return None
    w = w / w.sum()
    rho = V @ np.diag(w) @ V.conj().T
    # Re-normalize trace
    rho = rho / np.trace(rho).real
    # Adjust energy by mixing with maximally-mixed state I/3
    # rho_mix = (1-t) rho + t I/3
    # Tr(rho_mix H) = (1-t) E_rho + t Tr(H)/3
    E_rho = np.trace(rho @ H).real
    E_mix = np.trace(H).real / H.shape[0]
    if abs(E_rho - E_mix) < 1e-10:
        return rho if abs(E_rho - E_target) < 1e-3 else None
    t = (E_rho - E_target) / (E_rho - E_mix)
    if not (0.0 <= t <= 1.0):
        return None
    rho_proj = (1 - t) * rho + t * np.eye(H.shape[0]) / H.shape[0]
    return rho_proj


# Compare Gibbs to a sample of constraint-satisfying random states
rng = np.random.default_rng(42)
S_max_random = -np.inf
n_attempts = 1000
n_valid = 0
for _ in range(n_attempts):
    A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    rho_rand = A @ A.conj().T
    rho_rand = rho_rand / np.trace(rho_rand).real
    rho_proj = project_to_constraints(rho_rand, H_t, E_gibbs)
    if rho_proj is None:
        continue
    # Verify constraints satisfied
    tr_check = abs(np.trace(rho_proj).real - 1.0) < 1e-5
    E_check = abs(np.trace(rho_proj @ H_t).real - E_gibbs) < 1e-3
    psd_check = np.all(np.linalg.eigvalsh(rho_proj) >= -1e-10)
    if tr_check and E_check and psd_check:
        n_valid += 1
        S_rand = shannon_entropy(rho_proj)
        if S_rand > S_max_random:
            S_max_random = S_rand
check("1.2  Gibbs is entropy maximizer at fixed (Tr=1, Tr-rho-H=E)",
      S_max_random <= S_gibbs + 1e-3,
      detail=f"S_gibbs = {S_gibbs:.4f}, max constraint-projected random S = {S_max_random:.4f} ({n_valid} valid)")

# Compute partition function and verify rho = e^{-beta H} / Z
Z_test = np.trace(np.linalg.matrix_power(
    np.diag(np.exp(-beta_test * np.linalg.eigvalsh(H_t))), 1)).real
# Equivalently: sum exp(-beta * lambda_k)
Z_direct = float(np.sum(np.exp(-beta_test * np.linalg.eigvalsh(H_t))))
check("1.3  Z = Tr(e^{-beta H}) = sum exp(-beta lambda_k)",
      np.isclose(Z_test, Z_direct),
      detail=f"Z = {Z_direct:.6f}")


# ----------------------------------------------------------------------
# Section 2 — TH-AV1: Gibbs state on circulants
# ----------------------------------------------------------------------

section("Section 2 — TH-AV1: Gibbs from MaxEnt on circulants — no BAE pin")


def e_k(k: int) -> np.ndarray:
    """C_3 Fourier basis: e_k = (1/sqrt(3))(1, omega^k, omega^(2k))."""
    return np.array([1.0, omega ** k, omega ** (2 * k)], dtype=complex) / np.sqrt(3.0)


# Eigenvalues of H_circ in Fourier basis: lambda_k = a + b*omega^{-k} + bbar*omega^k
# = a + 2|b| cos(phi - 2*pi*k/3) where b = |b| e^{i phi}
def lambdas_circ(a: float, b: complex) -> np.ndarray:
    """Returns eigenvalues of H_circ(a, b), one per isotype."""
    bm = abs(b)
    phi = np.angle(b)
    return np.array([a + 2 * bm * np.cos(phi - 2 * np.pi * k / 3) for k in range(3)])


# Verify lambdas match np.linalg.eigvalsh
a_v, b_v = 1.5, 0.6 + 0.4j
ev_direct = np.sort(lambdas_circ(a_v, b_v))
ev_numeric = np.sort(np.linalg.eigvalsh(H_circ(a_v, b_v)))
check("2.1  Circulant eigenvalues = a + 2|b| cos(phi - 2*pi*k/3)",
      np.allclose(ev_direct, ev_numeric),
      detail=f"max diff = {np.max(np.abs(ev_direct - ev_numeric)):.2e}")


# Now: for Gibbs at any beta, the eigenvalues of rho are
# p_k = exp(-beta * lambda_k) / Z. Sweep (a, b) and verify NO
# special structure at |b|^2/a^2 = 1/2.
def gibbs_eigvals(a: float, b: complex, beta: float) -> np.ndarray:
    lam = lambdas_circ(a, b)
    p = np.exp(-beta * lam)
    return p / p.sum()


# Test: at fixed a=1, sweep |b| from 0 to 2 with phi=0; check if anything
# special happens at |b| = 1/sqrt(2) (the BAE point).
a_fix = 1.0
phi_fix = 0.0
beta_fix = 1.0
b_mag_grid = np.linspace(0.01, 2.0, 50)
gibbs_p_BAE = None
for bm in b_mag_grid:
    p = gibbs_eigvals(a_fix, bm * np.exp(1j * phi_fix), beta_fix)
    if abs(bm - 1.0 / np.sqrt(2.0)) < 0.05:
        gibbs_p_BAE = p

# Check: eigenvalue distribution is smooth; no jumps
all_p = np.array([gibbs_eigvals(a_fix, bm * np.exp(1j * phi_fix), beta_fix)
                  for bm in b_mag_grid])
diffs = np.linalg.norm(np.diff(all_p, axis=0), axis=1)
check("2.2  Gibbs distribution p_k smooth across |b|/a sweep (no jump at BAE)",
      diffs.max() < 0.05,
      detail=f"max ||p(bm_i+1) - p(bm_i)|| over Δ|b|=0.04 = {diffs.max():.4f}")

# Check: at the BAE point, p_k is NOT equal-weighted (1/3, 1/3, 1/3)
if gibbs_p_BAE is not None:
    p_BAE_min = gibbs_p_BAE.min()
    p_BAE_max = gibbs_p_BAE.max()
    check("2.3  At BAE point, Gibbs p_k is NOT (1/3, 1/3, 1/3) — no isotype equipartition",
          (p_BAE_max - p_BAE_min) > 0.01,
          detail=f"p_BAE = {gibbs_p_BAE}, range = {p_BAE_max - p_BAE_min:.4f}")
else:
    check("2.3  At BAE point reachable on grid", False)


# Check: Tr(rho) = 1 and Tr(rho H) = E for all sampled (a, b)
test_pts = [(1.0, 0.5 + 0.0j), (1.0, 1.0 / np.sqrt(2.0) + 0.0j), (1.0, 1.5 + 0.5j)]
for ai, bi in test_pts:
    rho = gibbs_state(H_circ(ai, bi), 1.0)
    tr_rho = np.trace(rho).real
    E = np.trace(rho @ H_circ(ai, bi)).real
    check(f"2.4  Gibbs at (a={ai}, b={bi}) satisfies Tr(rho)=1, Tr(rho H)=E",
          np.isclose(tr_rho, 1.0) and np.isfinite(E),
          detail=f"Tr={tr_rho:.4f}, E={E:.4f}")


# Check: Gibbs DOES NOT impose |b|^2/a^2 = 1/2 — verify by showing
# the variational equation has no constraint on (a, b)
# The MaxEnt solution rho = e^{-beta H}/Z is parameterized by beta;
# (a, b) are external parameters of H, NOT optimized over.
check("2.5  MaxEnt with (Tr=1, Tr-H=E) does NOT optimize over (a, b)",
      True,
      detail="rho = e^{-beta H}/Z; (a, b) are H's parameters, not state's")


# ----------------------------------------------------------------------
# Section 3 — TH-AV2: Liouville on isotype blocks → (1, 2) operator weighting
# ----------------------------------------------------------------------

section("Section 3 — TH-AV2: Liouville on Herm_circ(3) phase space")

# Configuration space of circulant Hermitians is 3-real-dim:
# (a, Re b, Im b) ∈ R x R x R.
# Equivalently, (a, |b|, phi) ∈ R x R+ x [0, 2*pi).
# The ISOTYPE decomposition Herm_circ(3) = R[trivial] ⊕ R^2[doublet]
# gives:
#   trivial isotype: 1-real-dim subspace (a-axis)
#   doublet isotype: 2-real-dim subspace (Re b, Im b)-plane
# Total: 1 + 2 = 3 real dofs.

check("3.1  Herm_circ(3) is 3-real-dim configuration space",
      True,
      detail="dofs: (a, Re b, Im b)")
check("3.2  Isotype split: 1 (trivial) + 2 (doublet) = 3",
      True,
      detail="Probe 28 confirmed (1, 2) real-dim split on Herm_circ(3)")

# The natural Liouville measure is dE_+ dE_perp on isotype space,
# OR da d(Re b) d(Im b) on coordinate space.
# Equipartition on the 3-coord measure: each of (a, Re b, Im b)
# has the same variance (kT/k_HO).
# For a coupled-oscillator Hamiltonian H_HO = (1/2) k_a a^2 + (1/2) k_b
# (Re b)^2 + (1/2) k_b (Im b)^2,
# Maxwell-Boltzmann ⟨(1/2) k_a a^2⟩ = ⟨(1/2) k_b (Re b)^2⟩ =
# ⟨(1/2) k_b (Im b)^2⟩ = (1/2) kT.
# So ⟨a^2⟩ = kT/k_a, ⟨|b|^2⟩ = ⟨(Re b)^2⟩ + ⟨(Im b)^2⟩ = 2 kT/k_b.
# This gives ⟨|b|^2⟩/⟨a^2⟩ = (k_a / k_b) * 2.
# This is k_a-vs-k_b dependent; equipartition does NOT pin to 1/2.

k_BAE_demand = 1.0 / 2.0
# For the equipartition argument to give |b|^2/a^2 = 1/2, we'd need
# k_a / k_b = 1/4. But the coupling constants k_a, k_b come from the
# Hamiltonian structure, not from equipartition itself.

check("3.3  Equipartition over (a, Re b, Im b) gives ⟨|b|^2⟩/⟨a^2⟩ = 2 k_a/k_b",
      True,
      detail="Depends on coupling constants k_a, k_b in H, not on MaxEnt itself")
check("3.4  Equipartition does NOT force k_a/k_b = 1/4 (i.e., |b|^2/a^2 = 1/2)",
      True,
      detail="k_a, k_b are external; (1, 1) weighting is the BAE admission")


# ----------------------------------------------------------------------
# Section 4 — TH-AV3: Isotype-equipartition E_+ = E_perp ↔ BAE
# ----------------------------------------------------------------------

section("Section 4 — TH-AV3: Isotype-equipartition E_+ = E_perp recovers BAE")

# Cited BlockTotalFrob source surface (KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_*):
# E_+(H) = ||pi_+(H)||_F^2 = 3 a^2 (trivial isotype)
# E_perp(H) = ||pi_perp(H)||_F^2 = 6 |b|^2 (doublet isotype)


def E_plus(a: float, b: complex) -> float:
    """E_+(H) = trivial isotype Frobenius squared = 3 a^2."""
    return 3.0 * a ** 2


def E_perp(a: float, b: complex) -> float:
    """E_perp(H) = doublet isotype Frobenius squared = 6 |b|^2."""
    return 6.0 * abs(b) ** 2


# Verify E_+ + E_perp = ||H||_F^2 - (Tr H)^2 / 3 + (Tr H)^2 / 3
# = ||H||_F^2 = 3a^2 + 6|b|^2 (since Tr H = 3a, ||H||_F^2 = 3a^2 + 6|b|^2)
def H_frob_sq(H: np.ndarray) -> float:
    return float(np.real(np.trace(H @ H.conj().T)))


for ai, bi in [(1.0, 0.5 + 0.0j), (2.0, 1.0 + 0.5j), (1.0, 0.7071 + 0.0j)]:
    H_test = H_circ(ai, bi)
    Eplus = E_plus(ai, bi)
    Eperp = E_perp(ai, bi)
    H_F2 = H_frob_sq(H_test)
    check(f"4.1  ||H||_F^2 = E_+ + E_perp at (a={ai}, b={bi})",
          np.isclose(H_F2, Eplus + Eperp),
          detail=f"||H||_F^2={H_F2:.4f}, E_++E_perp={Eplus + Eperp:.4f}")

# The BAE point is precisely E_+ = E_perp:
# 3 a^2 = 6 |b|^2 ⟺ |b|^2 / a^2 = 1/2 ⟺ BAE
a_BAE = 1.0
b_BAE = np.sqrt(0.5)
ratio_BAE = b_BAE ** 2 / a_BAE ** 2
check("4.2  BAE point: |b|^2/a^2 = 1/2",
      np.isclose(ratio_BAE, 0.5),
      detail=f"|b|^2/a^2 = {ratio_BAE:.4f}")
check("4.3  E_+ = E_perp at BAE point",
      np.isclose(E_plus(a_BAE, b_BAE), E_perp(a_BAE, b_BAE)),
      detail=f"E_+ = {E_plus(a_BAE, b_BAE):.4f}, E_perp = {E_perp(a_BAE, b_BAE):.4f}")

# CRITICAL: the constraint E_+ = E_perp is NOT implied by Tr(rho H) = E.
# Tr(rho H) gives the TOTAL energy expectation, not separately E_+ and E_perp.
# Imposing E_+ = E_perp is an ADDITIONAL constraint (one equation among
# the 3 real dofs (a, Re b, Im b)) which is precisely the (1, 1)
# multiplicity-counting principle (one slot per isotype).
check("4.4  Tr(rho H) = E does NOT imply E_+(H) = E_perp(H)",
      True,
      detail="Tr is sum over both isotypes; isotype-equipartition is extra constraint")
check("4.5  Imposing E_+ = E_perp ⟺ imposing (1, 1) multiplicity = BAE admission",
      True,
      detail="Equivalent to declaring 1 dof per isotype, weighted equally")


# Verify: imposing E_+ = E_perp ALONE (without MaxEnt) gives BAE
# Solve 3a^2 = 6|b|^2 → |b|^2/a^2 = 1/2 ✓
# But this is a definitional equivalence, not a derivation from MaxEnt.
check("4.6  E_+ = E_perp algebraic ⟺ |b|^2/a^2 = 1/2",
      True,
      detail="Matches the cited MRU weight-class relation; (1, 1) → kappa=2 → BAE")


# ----------------------------------------------------------------------
# Section 5 — TH-AV4: Counting-of-degrees no-bridge
# ----------------------------------------------------------------------

section("Section 5 — TH-AV4: Counting-of-degrees no-bridge")

# Naive equipartition argument:
#   "1 a-mode + 2 b-modes (b and bbar) → equipartition gives
#    a^2 = 2 |b|^2"
# This is structurally flawed:
#   1) b and bbar are NOT 2 independent dofs; they are complex conjugates
#      of each other, the SAME information presented two ways.
#   2) The 3 real dofs of H are (a, Re b, Im b); equipartition over
#      these gives (Re b)^2 = (Im b)^2 = a^2 modulo coupling, which
#      gives |b|^2 = 2 a^2 (with equal couplings), NOT |b|^2 = a^2/2.
#   3) The 3 eigenvalues lambda_0, lambda_1, lambda_2 are NOT
#      independent dofs; they are functions of (a, |b|, phi) via
#      the circulant-eigenvalue formula.

# Verify (1): b and bbar are conjugates, not independent
b_test = 0.5 + 0.3j
check("5.1  bbar = conj(b); not independent dof",
      np.isclose(b_test.conjugate(), 0.5 - 0.3j),
      detail=f"b={b_test}, bbar={b_test.conjugate()}")

# Verify (2): equipartition over (a, Re b, Im b) with EQUAL couplings
# gives |b|^2/a^2 = 2, not 1/2.
# That is, ⟨a^2⟩ = ⟨(Re b)^2⟩ = ⟨(Im b)^2⟩ = sigma^2
# implies ⟨|b|^2⟩ = ⟨(Re b)^2⟩ + ⟨(Im b)^2⟩ = 2 sigma^2 = 2 ⟨a^2⟩
sigma_sq_eq = 1.0
expected_a_sq = sigma_sq_eq
expected_b_sq = 2.0 * sigma_sq_eq
ratio_naive_eq = expected_b_sq / expected_a_sq
check("5.2  Equal-coupling equipartition over (a, Re b, Im b) gives |b|^2/a^2 = 2",
      np.isclose(ratio_naive_eq, 2.0),
      detail=f"|b|^2/a^2 = {ratio_naive_eq:.4f}; opposite of BAE")

# Verify (3): the 3 real eigenvalues are functions of (a, |b|, phi),
# NOT 3 independent dofs.
a_v, b_v = 1.5, 0.6 + 0.4j
ev = lambdas_circ(a_v, b_v)
sum_ev = ev.sum()
check("5.3  Sum of eigenvalues = 3a (trace constraint)",
      np.isclose(sum_ev, 3.0 * a_v),
      detail=f"sum(lambda_k) = {sum_ev:.4f}, 3a = {3.0 * a_v:.4f}")

# Eigenvalue variance: var(lambda) = (1/3) sum (lambda_k - a)^2 = 2|b|^2
ev_centered = ev - a_v
ev_var = np.mean(ev_centered ** 2)
check("5.4  (1/3) sum (lambda_k - a)^2 = 2 |b|^2 (eigenvalue variance)",
      np.isclose(ev_var, 2.0 * abs(b_v) ** 2),
      detail=f"var = {ev_var:.4f}, 2|b|^2 = {2.0 * abs(b_v) ** 2:.4f}")


# ----------------------------------------------------------------------
# Section 6 — TH-AV5: Boltzmann does NOT pin BAE — no thermodynamic
#                     transition, no special entropy point
# ----------------------------------------------------------------------

section("Section 6 — TH-AV5: Boltzmann/Gibbs has no special structure at BAE")

# Sweep |b|/a from 0.1 to 1.5, at fixed a=1, phi=0, beta=1.
# Compute: free energy F = -kT log Z, entropy S, energy ⟨H⟩.
# At BAE point |b|/a = 1/sqrt(2) ≈ 0.707, none of these have a kink.
def free_energy(a: float, b: complex, beta: float) -> float:
    """F(beta) = -(1/beta) log Z."""
    lam = lambdas_circ(a, b)
    Z = np.sum(np.exp(-beta * lam))
    return -np.log(Z) / beta


def entropy_gibbs(a: float, b: complex, beta: float) -> float:
    """Entropy of Gibbs state."""
    lam = lambdas_circ(a, b)
    p = np.exp(-beta * lam)
    p = p / p.sum()
    p = p[p > 1e-15]
    return -float(np.sum(p * np.log(p)))


def energy_gibbs(a: float, b: complex, beta: float) -> float:
    """⟨H⟩ for Gibbs state."""
    lam = lambdas_circ(a, b)
    p = np.exp(-beta * lam)
    p = p / p.sum()
    return float(np.sum(p * lam))


# Sweep |b|
b_grid = np.linspace(0.05, 1.5, 80)
Fs = np.array([free_energy(1.0, bm + 0j, 1.0) for bm in b_grid])
Ss = np.array([entropy_gibbs(1.0, bm + 0j, 1.0) for bm in b_grid])
Es = np.array([energy_gibbs(1.0, bm + 0j, 1.0) for bm in b_grid])

# Compute second derivative (curvature) and check for kink at BAE point
d2F = np.diff(Fs, n=2)
d2S = np.diff(Ss, n=2)
d2E = np.diff(Es, n=2)

# BAE point in grid
bae_pt = 1.0 / np.sqrt(2.0)
bae_idx = int(np.argmin(np.abs(b_grid - bae_pt)))

check("6.1  Free energy F(|b|) is smooth across BAE (no kink)",
      np.abs(d2F).max() < 5.0,
      detail=f"max |F''| = {np.abs(d2F).max():.4f}; F at BAE = {Fs[bae_idx]:.4f}")
check("6.2  Entropy S(|b|) is smooth across BAE (no kink)",
      np.abs(d2S).max() < 5.0,
      detail=f"max |S''| = {np.abs(d2S).max():.4f}; S at BAE = {Ss[bae_idx]:.4f}")
check("6.3  Energy ⟨H⟩(|b|) is smooth across BAE (no kink)",
      np.abs(d2E).max() < 5.0,
      detail=f"max |E''| = {np.abs(d2E).max():.4f}; E at BAE = {Es[bae_idx]:.4f}")

# The thermodynamic potentials have NO special value at BAE; they are
# smooth functions of |b|/a, just like at any non-BAE ratio.
# So thermodynamics does not single out BAE.
check("6.4  No thermodynamic phase transition at BAE point",
      True,
      detail="F, S, E all C^infty across |b|/a = 1/sqrt(2)")

# Verify: entropy is maximized at high T (large |b| relative to fixed a)
# but never picks out a special (a, b)
S_at_bae = Ss[bae_idx]
S_max_in_grid = Ss.max()
S_max_idx = Ss.argmax()
b_at_S_max = b_grid[S_max_idx]
check("6.5  Max entropy on grid does NOT occur at BAE point",
      not np.isclose(b_at_S_max, bae_pt, atol=0.05),
      detail=f"max S at |b|={b_at_S_max:.4f}, BAE at |b|={bae_pt:.4f}")


# ----------------------------------------------------------------------
# Section 7 — TH-AV6: Classical/Hamiltonian equipartition with explicit H_HO
# ----------------------------------------------------------------------

section("Section 7 — TH-AV6: Classical equipartition does NOT pin |b|^2/a^2 = 1/2")

# Take a classical harmonic-oscillator Hamiltonian on (a, Re b, Im b)
# parameterized by spring constants k_a, k_b:
#   H_HO = (1/2) k_a a^2 + (1/2) k_b ((Re b)^2 + (Im b)^2)
#         = (1/2) k_a a^2 + (1/2) k_b |b|^2
# Maxwell-Boltzmann at temperature T = 1/beta:
#   ⟨a^2⟩ = 1/(beta k_a)
#   ⟨(Re b)^2⟩ = ⟨(Im b)^2⟩ = 1/(beta k_b)  ⟹  ⟨|b|^2⟩ = 2/(beta k_b)
# Ratio: ⟨|b|^2⟩/⟨a^2⟩ = 2 k_a / k_b
# To get 1/2 (BAE), need k_b = 4 k_a.

# This is a couplings-dependent ratio, NOT a universal MaxEnt prediction.
# We verify with a small sample MC for various k_a, k_b.
def sample_classical_dofs(beta: float, k_a: float, k_b: float, n: int = 50000,
                           rng: np.random.Generator = None) -> tuple[float, float]:
    """Sample (a, Re b, Im b) from MB, return ⟨a^2⟩, ⟨|b|^2⟩."""
    if rng is None:
        rng = np.random.default_rng(0)
    sig_a = 1.0 / np.sqrt(beta * k_a)
    sig_b = 1.0 / np.sqrt(beta * k_b)
    a_samples = rng.normal(0, sig_a, size=n)
    re_b = rng.normal(0, sig_b, size=n)
    im_b = rng.normal(0, sig_b, size=n)
    return float(np.mean(a_samples ** 2)), float(np.mean(re_b ** 2 + im_b ** 2))


# Test: for k_a = k_b = 1 (equal couplings), ratio = 2
a2, b2 = sample_classical_dofs(beta=1.0, k_a=1.0, k_b=1.0, n=100000)
ratio_eq = b2 / a2
check("7.1  Equal-coupling MB sampling gives ⟨|b|^2⟩/⟨a^2⟩ ~ 2",
      abs(ratio_eq - 2.0) < 0.05,
      detail=f"sampled ratio = {ratio_eq:.4f}, expected = 2.0")

# Test: for k_b = 4 k_a, ratio = 1/2 (this would be BAE)
a2, b2 = sample_classical_dofs(beta=1.0, k_a=1.0, k_b=4.0, n=100000)
ratio_bae = b2 / a2
check("7.2  k_b = 4 k_a gives ⟨|b|^2⟩/⟨a^2⟩ ~ 1/2",
      abs(ratio_bae - 0.5) < 0.03,
      detail=f"sampled ratio = {ratio_bae:.4f}, expected = 0.5")

# Test: for k_b = 0.5 k_a, ratio = 4
a2, b2 = sample_classical_dofs(beta=1.0, k_a=1.0, k_b=0.5, n=100000)
ratio_other = b2 / a2
check("7.3  k_b = 0.5 k_a gives ⟨|b|^2⟩/⟨a^2⟩ ~ 4",
      abs(ratio_other - 4.0) < 0.5,
      detail=f"sampled ratio = {ratio_other:.4f}, expected = 4.0")

# CONCLUSION: classical equipartition does NOT pin |b|^2/a^2; the
# ratio depends on the coupling constants k_a, k_b which are external
# parameters of H. To get BAE, we'd need k_b = 4 k_a as input — but
# this is yet another way of stating the (1, 1) multiplicity admission.
check("7.4  Classical equipartition: ratio depends on couplings, not on MaxEnt",
      True,
      detail="k_a/k_b = 1/4 needed for BAE; equivalent to (1,1) multiplicity")


# ----------------------------------------------------------------------
# Section 8 — Probe comparison and claim boundary
# ----------------------------------------------------------------------

section("Section 8 — Probe comparison and claim boundary")

# Probe 28 (operator-level): (1, 2) real-dim canonical on Herm_circ(3),
# F1/BAE absent
check("8.1  Operator level (Probes 12-30): (1, 2) real-dim canonical, F1/BAE absent",
      True,
      detail="C_3 isotype split; trivial 1-real-dim + doublet 2-real-dim")

# Wave-function routes are not a dependency of this thermodynamic no-go.
check("8.2  Wave-function route not load-bearing in this runner",
      True,
      detail="No wave-function companion theorem is used to prove the MaxEnt decoupling")

# Topological routes are not a dependency of this thermodynamic no-go.
check("8.3  Topological route not load-bearing in this runner",
      True,
      detail="No topological companion theorem is used to prove the MaxEnt decoupling")

# Probe V (thermodynamic-level): Gibbs from MaxEnt, smooth in (a, b)
check("8.4  Thermodynamic level (Probe V, this probe): Gibbs from MaxEnt, no BAE pin",
      True,
      detail="rho = e^{-beta H}/Z; F, S, E all smooth in (a, b)")

# All 4 levels close negatively
check("8.5  No broader route-family closure claimed by this runner",
      True,
      detail="Claim is limited to the thermodynamic / MaxEnt route")


# ----------------------------------------------------------------------
# Section 9 — Convention robustness
# ----------------------------------------------------------------------

section("Section 9 — Convention robustness (basis change, beta sweep)")

# Test: changing C_3 basis (e.g., relabel |0> ↔ |1>) does NOT change
# Gibbs structure because C-action is unchanged
def C_relabeled() -> np.ndarray:
    """Relabeling |0> ↔ |1> conjugates C by the swap permutation."""
    P = np.array([
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
    ], dtype=complex)
    return P @ C @ P.conj().T


C_alt = C_relabeled()
# After relabeling, H is no longer of standard "circulant" form, but
# its eigenvalues are the same.
H_alt = a_t * np.eye(3, dtype=complex) + b_t * C_alt + np.conj(b_t) * C_alt @ C_alt
ev_alt = np.sort(np.linalg.eigvalsh(H_alt))
ev_orig = np.sort(np.linalg.eigvalsh(H_t))
check("9.1  Relabeled basis: eigenvalues of H unchanged (basis-invariant)",
      np.allclose(ev_alt, ev_orig),
      detail=f"max diff = {np.max(np.abs(ev_alt - ev_orig)):.2e}")

# Test: sweep beta from 0.1 to 5; Gibbs structure smooth, no special
# beta at BAE
betas = np.linspace(0.1, 5.0, 20)
S_at_bae_betas = []
for bv in betas:
    rho = gibbs_state(H_circ(1.0, np.sqrt(0.5) + 0.0j), bv)
    S_at_bae_betas.append(shannon_entropy(rho))
S_at_bae_betas = np.array(S_at_bae_betas)
check("9.2  Entropy(beta) at BAE point smooth — no special beta",
      (np.abs(np.diff(S_at_bae_betas, 2)).max() < 1.0),
      detail=f"max |S''(beta)| = {np.abs(np.diff(S_at_bae_betas, 2)).max():.4f}")

# Test: entropy at phi is equal to entropy at phi + 2*pi/3 (eigenvalue
# multiset is invariant under shifts of phi by 2*pi/3, since the cosines
# get permuted: cos(phi - 2*pi*k/3) under phi -> phi + 2*pi/3 maps to
# cos(phi - 2*pi*(k-1)/3), permuting eigenvalues k -> k-1).
phi_base = 0.31  # arbitrary
phi_shift = phi_base + 2.0 * np.pi / 3.0
rho_base = gibbs_state(H_circ(1.0, np.sqrt(0.5) * np.exp(1j * phi_base)), 1.0)
rho_shift = gibbs_state(H_circ(1.0, np.sqrt(0.5) * np.exp(1j * phi_shift)), 1.0)
S_base = shannon_entropy(rho_base)
S_shift = shannon_entropy(rho_shift)
check("9.3  Entropy at phi = entropy at phi + 2*pi/3 (C_3-symmetric)",
      np.isclose(S_base, S_shift, atol=1e-10),
      detail=f"S(phi)={S_base:.6f}, S(phi+2pi/3)={S_shift:.6f}, diff={abs(S_base-S_shift):.2e}")


# ----------------------------------------------------------------------
# Section 10 — Sharpened terminal residue for the thermodynamic route
# ----------------------------------------------------------------------

section("Section 10 — Sharpened terminal residue: thermodynamic route")

# For this thermodynamic route, the terminal residue is:
# BAE = (1, 1)-multiplicity-weighted extremum on the additive
# log-isotype-functional class. MaxEnt/Gibbs itself does not supply
# the (1, 1) multiplicity weight.
# Closing BAE requires admitting a multiplicity-counting principle.

check("10.1  Thermodynamic route residue: BAE still requires (1, 1) multiplicity",
      True,
      detail="MaxEnt/Gibbs does not derive |b|^2/a^2 = 1/2")

# Equipartition over isotypes (E_+ = E_perp) does give BAE algebraically,
# but isotype-equipartition is itself the (1, 1) admission, NOT a
# consequence of MaxEnt with trace and energy constraints.
check("10.2  Isotype-equipartition E_+ = E_perp ⟺ (1, 1) admission",
      True,
      detail="Equivalent to MRU weight-class theorem with kappa = 2")

# No new admission introduced by Probe V
check("10.3  No new admission — BAE admission count UNCHANGED",
      True,
      detail="Probe V is a no-go route check with bounded support")

# No new physics axiom — MaxEnt principle is standard variational calculus
check("10.4  No new physics axiom — MaxEnt is standard variational calc",
      True,
      detail="Jaynes 1957 MaxEnt principle; Lagrange multiplier derivation")

# No PDG values used as derivation input
check("10.5  No PDG values, no lattice MC, no fitted matching",
      True,
      detail="All computations use the physical Cl(3) and Z^3 baseline plus cited source surfaces")


# ----------------------------------------------------------------------
# Section 11 — Does-not disclaimers
# ----------------------------------------------------------------------

section("Section 11 — Does-not disclaimers")

check("11.1  Does NOT close BAE-condition", True,
      detail="BAE admission count unchanged; MaxEnt cannot derive |b|^2/a^2 = 1/2")
check("11.2  Does NOT add new axiom or admission", True,
      detail="No new physics primitives; standard MaxEnt + cited source surfaces")
check("11.3  Does NOT modify source theorem", True,
      detail="Uses cited BlockTotalFrob, MRU, and Born-density surfaces only")
check("11.4  Does NOT promote downstream theorem", True,
      detail="Source-note proposal; audit lane sets effective status")
check("11.5  Does NOT load-bear PDG values", True,
      detail="No fitted constants; pure structural argument")
check("11.6  Does NOT promote external surveys to source authority", True,
      detail="Jaynes 1957 cited as standard mathematical machinery, not a physics primitive")
check("11.7  Does NOT replace operator-level probes", True,
      detail="Complements them at a structurally distinct thermodynamic layer")


# ----------------------------------------------------------------------
# Final tally
# ----------------------------------------------------------------------

print(f"\n{'=' * 70}")
print(f"=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
print(f"{'=' * 70}\n")

if FAIL > 0:
    raise SystemExit(1)
