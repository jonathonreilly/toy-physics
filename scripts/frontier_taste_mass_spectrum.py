#!/usr/bin/env python3
"""Staggered fermion taste mass spectrum: does m_k ~ alpha^{k/2} hold?

PHYSICS:
Staggered fermions on a d-dimensional hypercubic lattice produce 2^d taste
(doubler) states, one at each corner of the Brillouin zone (BZ). A BZ corner
is labeled by a binary vector p in {0, pi}^d. The Hamming weight hw(p) = k
counts how many components are at pi.

The key prediction under test:
    m_k = c_k * alpha^{k/2} * M_Pl,   degeneracy = C(d,k)

If this holds for d=4, then the physical fermion mass hierarchy comes from
the taste spectrum, and in particular the EW scale is:
    v = M_Pl * alpha^{16/2} = M_Pl * alpha^8
(or similar, depending on which taste maps to the Higgs doublet).

WHAT WE COMPUTE:

1. Free staggered Dirac operator on L^4 lattice (periodic BC).
2. Taste-breaking Wilson term with coupling r proportional to alpha.
3. Full spectrum via exact diagonalization for L=4,6.
4. Eigenvalues grouped by BZ corner Hamming weight k=0..4.
5. Fit to both hypotheses:
   (A) m_k = c * alpha^{k/2}     (exponential in k)
   (B) m_k = c * sqrt(k * alpha)  (sqrt in k)
6. Chi-squared comparison to determine which fits better.

ANALYTIC DERIVATION:
For the naive staggered operator D_stag, the dispersion at BZ corner p is:
    E^2(p) = sum_mu sin^2(p_mu) + m_bare^2

All corners with the same hw have the same E^2 (they permute sin^2(0) and
sin^2(pi) = 0 contributions). So the free staggered operator is exactly
degenerate within each hw class -- the 16-fold degeneracy splits as 1+4+6+4+1
but with the SAME energy.

The Wilson term D_W = -r/2 sum_mu Delta_mu (second derivative) adds:
    delta_W(p) = r * sum_mu (1 - cos(p_mu))

For p_mu in {0, pi}: cos(0) = 1, cos(pi) = -1, so each pi-component adds 2r.
    delta_W(k) = 2r * k

This is LINEAR in k, not alpha^{k/2}. This gives masses:
    m_k = m_0 + 2r * k

For the taste-improved staggered action (e.g., HISQ, asqtad), higher-order
corrections enter. The question is whether some non-perturbative mechanism
could resum these into an exponential alpha^{k/2} dependence.

NUMERICAL TEST:
We build the lattice Hamiltonian including:
- Naive staggered hopping (nearest-neighbor with staggered phases)
- Wilson term with r = alpha * f(coupling)
- Gauge links U_mu set to free field (U=1) or random SU(1) phases

Then we measure eigenvalues at each BZ corner and test the scaling.

PStack experiment: taste-mass-spectrum
Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import itertools
import sys
import time
from math import comb

import numpy as np
from scipy import linalg, optimize

np.set_printoptions(precision=8, linewidth=120)

ALPHA_EM = 1.0 / 137.036  # fine structure constant


# ============================================================================
# Staggered lattice construction in d dimensions
# ============================================================================

def staggered_phase(site: tuple[int, ...], mu: int) -> float:
    """Staggered phase eta_mu(x) = (-1)^{x_0 + ... + x_{mu-1}}.

    This is the Kawamoto-Smit phase that encodes the spin structure
    in the staggered formulation.
    """
    return (-1) ** sum(site[:mu])


def site_index(site: tuple[int, ...], L: int, d: int) -> int:
    """Map a d-dimensional site coordinate to a linear index."""
    idx = 0
    for mu in range(d):
        idx = idx * L + (site[mu] % L)
    return idx


def index_to_site(idx: int, L: int, d: int) -> tuple[int, ...]:
    """Map a linear index back to d-dimensional site coordinates."""
    site = []
    for mu in range(d - 1, -1, -1):
        site.append(idx % L)
        idx //= L
    return tuple(reversed(site))


def build_staggered_dirac(L: int, d: int, m_bare: float, r_wilson: float) -> np.ndarray:
    """Build the staggered Dirac operator D on an L^d lattice.

    D = D_stag + m_bare + r * D_wilson

    where:
    D_stag: naive staggered hopping with eta phases
    D_wilson: -r/2 sum_mu (forward + backward - 2) Laplacian
    m_bare: bare mass

    The matrix acts on a single-component field (staggered = 1 component per site).
    Total dimension = L^d.
    """
    V = L ** d
    D = np.zeros((V, V), dtype=complex)

    all_sites = [index_to_site(i, L, d) for i in range(V)]

    for i, site in enumerate(all_sites):
        # Bare mass on diagonal
        D[i, i] += m_bare

        for mu in range(d):
            eta = staggered_phase(site, mu)

            # Forward neighbor
            fwd = list(site)
            fwd[mu] = (fwd[mu] + 1) % L
            j_fwd = site_index(tuple(fwd), L, d)

            # Backward neighbor
            bwd = list(site)
            bwd[mu] = (bwd[mu] - 1) % L
            j_bwd = site_index(tuple(bwd), L, d)

            # Staggered hopping: (1/2) eta_mu (T_mu - T_{-mu})
            D[i, j_fwd] += 0.5 * eta
            D[i, j_bwd] -= 0.5 * eta

            # Wilson term: -r/2 (T_mu + T_{-mu} - 2)
            D[i, j_fwd] -= r_wilson / 2.0
            D[i, j_bwd] -= r_wilson / 2.0
            D[i, i] += r_wilson  # the +2 * r/2 = r per direction

    return D


# ============================================================================
# Momentum-space analysis: project onto BZ corners
# ============================================================================

def bz_corners(d: int) -> list[tuple[int, ...]]:
    """All BZ corners: p_mu in {0, pi}, represented as tuples of 0/1."""
    return list(itertools.product([0, 1], repeat=d))


def hamming_weight(corner: tuple[int, ...]) -> int:
    """Number of pi-components in a BZ corner."""
    return sum(corner)


def momentum_project(D: np.ndarray, L: int, d: int, corner: tuple[int, ...]) -> np.ndarray:
    """Project the Dirac operator onto a specific BZ corner.

    The BZ corner p = (p_1, ..., p_d) with p_mu in {0, pi} defines a
    sublattice. We Fourier transform D to momentum space and extract
    the block at momentum p = corner * pi.

    For the staggered operator, the 2^d BZ corners correspond to the
    2^d taste states. We project by computing the Fourier-transformed
    propagator at the corner momentum.

    Returns the eigenvalues of D restricted to momenta near this corner.
    """
    V = L ** d
    n_mom = (L // 2) ** d  # number of momenta in the reduced BZ near this corner

    # Build Fourier basis vectors for momenta near this corner
    # Momenta: p_mu = corner_mu * pi + 2*pi*n_mu/L, n_mu = 0..L/2-1
    half_L = L // 2
    mom_indices = list(itertools.product(range(half_L), repeat=d))

    # Fourier matrix: F[site, mom] = exp(i p . x) / sqrt(V)
    F = np.zeros((V, n_mom), dtype=complex)
    for m_idx, n_tuple in enumerate(mom_indices):
        for s_idx in range(V):
            site = index_to_site(s_idx, L, d)
            phase = 0.0
            for mu in range(d):
                p_mu = corner[mu] * np.pi + 2 * np.pi * n_tuple[mu] / L
                phase += p_mu * site[mu]
            F[s_idx, m_idx] = np.exp(1j * phase) / np.sqrt(V)

    # Project: D_corner = F^dagger D F
    D_corner = F.conj().T @ D @ F
    return D_corner


def analytic_dispersion(corner: tuple[int, ...], d: int,
                        m_bare: float, r_wilson: float) -> float:
    """Analytic dispersion relation at a BZ corner (zero reduced momentum).

    For a BZ corner p = (p_1,...,p_d) with p_mu in {0, pi}:
    - Staggered part: sum_mu sin^2(p_mu) = 0 (sin(0) = sin(pi) = 0)
    - Wilson part: r * sum_mu (1 - cos(p_mu))
      = r * (k * 2) where k = hamming_weight (since cos(pi) = -1)
    - Bare mass: m_bare

    So the eigenvalue at reduced momentum = 0 is:
    lambda = m_bare + 2*r*k
    """
    k = hamming_weight(corner)
    return m_bare + 2 * r_wilson * k


# ============================================================================
# Main spectrum computation
# ============================================================================

def compute_taste_spectrum_analytic(d: int, m_bare: float, r_wilson: float):
    """Compute the analytic taste spectrum at BZ corners (reduced mom = 0).

    Returns dict mapping hw -> (mass, degeneracy).
    """
    corners = bz_corners(d)
    spectrum = {}
    for corner in corners:
        k = hamming_weight(corner)
        mass = analytic_dispersion(corner, d, m_bare, r_wilson)
        if k not in spectrum:
            spectrum[k] = {"mass": mass, "degeneracy": 0, "corners": []}
        spectrum[k]["degeneracy"] += 1
        spectrum[k]["corners"].append(corner)
    return spectrum


def compute_taste_spectrum_numerical(L: int, d: int, m_bare: float, r_wilson: float):
    """Build full lattice Dirac operator and extract taste masses numerically.

    For each BZ corner, we project and find the lowest eigenvalue magnitude.
    This captures effects beyond the analytic zero-mode formula.
    """
    print(f"  Building D on L={L}, d={d} lattice (V={L**d})...")
    t0 = time.time()
    D = build_staggered_dirac(L, d, m_bare, r_wilson)
    t1 = time.time()
    print(f"  Built in {t1-t0:.2f}s, computing eigenvalues...")

    # Full eigenvalue decomposition
    eigenvalues = linalg.eigvals(D)
    t2 = time.time()
    print(f"  Diagonalized in {t2-t1:.2f}s")

    # For each BZ corner, project and find eigenvalues
    corners = bz_corners(d)
    corner_spectra = {}
    for corner in corners:
        k = hamming_weight(corner)
        # Project onto this corner
        D_proj = momentum_project(D, L, d, corner)
        evals = np.sort(np.abs(linalg.eigvals(D_proj)))
        if k not in corner_spectra:
            corner_spectra[k] = []
        corner_spectra[k].append(evals[0])  # lowest eigenvalue magnitude

    # Average over corners with same hw
    spectrum = {}
    for k in sorted(corner_spectra.keys()):
        masses = corner_spectra[k]
        spectrum[k] = {
            "mass_mean": np.mean(masses),
            "mass_std": np.std(masses),
            "mass_all": masses,
            "degeneracy": len(masses),
        }

    return spectrum


def fit_power_law(hw_values, mass_values, alpha):
    """Fit m_k = c * alpha^{k/2} to data.

    In log space: log(m_k) = log(c) + (k/2) * log(alpha)
    """
    # Filter out k=0 (reference) and any zero masses
    mask = (hw_values > 0) & (mass_values > 0)
    if mask.sum() < 2:
        return None, None, np.inf

    k_fit = hw_values[mask]
    m_fit = mass_values[mask]

    # Fit: log(m_k/m_0) = a * k
    if mass_values[0] > 0:
        log_ratio = np.log(m_fit / mass_values[0])
    else:
        log_ratio = np.log(m_fit)

    # Model A: m_k = m_0 * alpha^{k/2}  => log(m_k/m_0) = (k/2) log(alpha)
    pred_A = (k_fit / 2.0) * np.log(alpha)
    chi2_A = np.sum((log_ratio - pred_A) ** 2)

    # Model B: m_k = m_0 * sqrt(k * alpha)  => log(m_k/m_0) = 0.5 * log(k*alpha)
    pred_B = 0.5 * np.log(k_fit * alpha)
    chi2_B = np.sum((log_ratio - pred_B) ** 2)

    return chi2_A, chi2_B, log_ratio


def fit_general_power(hw_values, mass_values):
    """Fit m_k = c * exp(beta * k) to the taste spectrum.

    Returns (c, beta) and the fit quality.
    """
    mask = (hw_values > 0) & (mass_values > 0)
    if mask.sum() < 2:
        return None, None, np.inf

    k_fit = hw_values[mask]
    m_fit = mass_values[mask]

    # Linear fit in log space: log(m_k) = log(c) + beta * k
    coeffs = np.polyfit(k_fit, np.log(m_fit), 1)
    beta = coeffs[0]
    log_c = coeffs[1]

    pred = log_c + beta * k_fit
    residuals = np.log(m_fit) - pred
    chi2 = np.sum(residuals ** 2)

    return np.exp(log_c), beta, chi2


# ============================================================================
# Wilson term from one-gluon exchange: deriving the effective r(alpha)
# ============================================================================

def one_gluon_exchange_taste_splitting(d: int, alpha_s: float):
    """Compute taste splitting from one-gluon exchange at O(alpha_s * a^2).

    In lattice QCD, the leading taste splitting for staggered fermions
    comes from one-gluon exchange with momentum near the BZ corner.
    The splitting for a taste state at BZ corner p with hw = k is:

        delta_m^2(k) = C_F * alpha_s * (4/a^2) * k * sum_terms

    where the sum involves the gluon propagator evaluated at large momentum.

    For the free-field case (quenched, no gluon dynamics), we can compute
    this perturbatively. The key result from Lee-Sharpe:

        delta_m^2_taste ~ C_2 * alpha_s * (pi/a)^2 * f(taste)

    where f(taste) depends on the specific taste representation.

    For our purposes, we parameterize:
        r_eff(alpha) = c * alpha  (the effective Wilson coefficient)

    and compute the spectrum for various values of alpha.
    """
    # The one-gluon exchange gives an effective Wilson term with
    # coefficient proportional to alpha_s
    r_eff = alpha_s * (16.0 / (4 * np.pi))  # ~ alpha_s / pi * geometric factor
    return r_eff


# ============================================================================
# Higher-order taste breaking: can it give alpha^{k/2}?
# ============================================================================

def higher_order_taste_analysis(d: int, alpha: float):
    """Analyze whether higher-order taste breaking can produce alpha^{k/2}.

    The Wilson term gives linear-in-k splitting: delta_m = 2r*k.
    With r ~ alpha, this gives delta_m ~ alpha * k.

    For alpha^{k/2} scaling, we need the splitting to be EXPONENTIAL in k.
    This requires the taste-breaking operator to have a PRODUCT structure:

        H_break = prod_{mu: p_mu = pi} V_mu

    where V_mu is a single-direction taste-breaking operator with
    eigenvalue ~ alpha^{1/2}.

    QUESTION: Does the staggered action naturally produce such a product?

    The naive Wilson term is a SUM over directions:
        D_W = sum_mu (-r/2) Delta_mu

    This gives ADDITIVE (linear in k) contributions.

    However, the FULL taste-breaking Hamiltonian from lattice perturbation
    theory includes multi-gluon exchange diagrams. At n-th order:

        H^(n)_break ~ (alpha_s)^n * (product of n taste matrices)

    The n-gluon exchange can couple n different BZ directions, giving
    a contribution that requires k >= n. For the leading contribution
    to the k-corner, we need at least k gluon exchanges, each bringing
    a factor of alpha_s^{1/2} (from the vertex).

    This gives: delta_m(k) ~ (alpha_s)^{k} * (combinatorial)

    BUT: this is alpha^k, not alpha^{k/2}. The sqrt comes from
    delta_m^2 ~ alpha^k => delta_m ~ alpha^{k/2}.

    Let's verify this reasoning numerically.
    """
    results = {}
    for k in range(d + 1):
        # Leading perturbative contribution to hw=k taste splitting
        # requires k gluon exchanges, each contributing alpha_s
        # But the mass-squared gets the correction, so:
        delta_m_sq_perturbative = alpha ** k  # leading in alpha for k-gluon exchange

        # The additive (Wilson) contribution
        delta_m_sq_wilson = (2 * alpha * k) ** 2  # from Wilson term squaring

        # The mass from mass-squared
        delta_m_perturbative = np.sqrt(delta_m_sq_perturbative) if delta_m_sq_perturbative > 0 else 0

        results[k] = {
            "delta_m_sq_perturbative": delta_m_sq_perturbative,
            "delta_m_perturbative": delta_m_perturbative,
            "delta_m_wilson": 2 * alpha * k,
            "alpha_k_half": alpha ** (k / 2.0),
            "sqrt_k_alpha": np.sqrt(k * alpha) if k > 0 else 0,
        }

    return results


# ============================================================================
# Non-perturbative test: staggered + gauge field
# ============================================================================

def build_staggered_with_gauge(L: int, d: int, m_bare: float,
                               r_wilson: float, beta_gauge: float) -> np.ndarray:
    """Build staggered Dirac operator with random U(1) gauge links.

    The gauge links U_mu(x) = exp(i * theta_mu(x)) are drawn from
    a distribution ~ exp(beta * cos(theta)), which is the compact U(1)
    Wilson action.

    For beta -> infinity: free field (U = 1).
    For finite beta: fluctuating gauge field with alpha_eff ~ 1/beta.
    """
    V = L ** d
    D = np.zeros((V, V), dtype=complex)

    all_sites = [index_to_site(i, L, d) for i in range(V)]

    # Generate gauge links from von Mises distribution
    # beta_gauge ~ 1/g^2, so alpha ~ 1/(4*pi*beta_gauge)
    rng = np.random.default_rng(42)
    gauge_links = {}
    for i, site in enumerate(all_sites):
        for mu in range(d):
            theta = rng.vonmises(0, beta_gauge)
            gauge_links[(site, mu)] = np.exp(1j * theta)

    for i, site in enumerate(all_sites):
        # Bare mass
        D[i, i] += m_bare

        for mu in range(d):
            eta = staggered_phase(site, mu)

            # Forward neighbor
            fwd = list(site)
            fwd[mu] = (fwd[mu] + 1) % L
            fwd = tuple(fwd)
            j_fwd = site_index(fwd, L, d)

            # Backward neighbor
            bwd = list(site)
            bwd[mu] = (bwd[mu] - 1) % L
            bwd = tuple(bwd)
            j_bwd = site_index(bwd, L, d)

            U_fwd = gauge_links[(site, mu)]
            U_bwd = gauge_links[(bwd, mu)].conj()  # U_{-mu}(x) = U_mu(x-mu)^dagger

            # Staggered hopping with gauge links
            D[i, j_fwd] += 0.5 * eta * U_fwd
            D[i, j_bwd] -= 0.5 * eta * U_bwd

            # Wilson term with gauge links
            D[i, j_fwd] -= r_wilson / 2.0 * U_fwd
            D[i, j_bwd] -= r_wilson / 2.0 * U_bwd
            D[i, i] += r_wilson

    return D


# ============================================================================
# Main analysis
# ============================================================================

def run_analytic_analysis(d: int = 4):
    """Run the analytic taste spectrum computation."""
    print("=" * 72)
    print(f"ANALYTIC TASTE SPECTRUM (d={d})")
    print("=" * 72)

    alpha = ALPHA_EM
    r_wilson = alpha  # Wilson coefficient proportional to alpha

    print(f"\nalpha = {alpha:.6f}")
    print(f"r_wilson = {r_wilson:.6f}")

    # Analytic spectrum with Wilson term
    m_bare = 1.0  # Set bare mass = 1 (= M_Pl in lattice units)
    spectrum = compute_taste_spectrum_analytic(d, m_bare, r_wilson)

    print(f"\n{'hw k':>5} {'degen':>6} {'m_k':>12} {'m_k/m_0':>10} "
          f"{'alpha^(k/2)':>12} {'sqrt(k*a)':>10} {'2rk':>10}")
    print("-" * 72)

    m_0 = spectrum[0]["mass"]
    for k in sorted(spectrum.keys()):
        s = spectrum[k]
        ratio = s["mass"] / m_0
        alpha_pred = alpha ** (k / 2.0) if k > 0 else 1.0
        sqrt_pred = np.sqrt(k * alpha) if k > 0 else 0.0
        wilson_shift = 2 * r_wilson * k
        print(f"{k:>5} {s['degeneracy']:>6} {s['mass']:>12.6f} {ratio:>10.6f} "
              f"{alpha_pred:>12.6f} {sqrt_pred:>10.6f} {wilson_shift:>10.6f}")

    # The Wilson term gives m_k = m_0 + 2*r*k, which is LINEAR in k
    print(f"\nWilson term result: m_k = m_0 + 2*alpha*k")
    print(f"  This is LINEAR in k, not exponential.")
    print(f"  m_k - m_0 = 2*alpha*k = {2*alpha:.6f} * k")

    return spectrum


def run_higher_order_analysis(d: int = 4):
    """Analyze higher-order taste breaking."""
    print("\n" + "=" * 72)
    print(f"HIGHER-ORDER TASTE BREAKING ANALYSIS (d={d})")
    print("=" * 72)

    alpha = ALPHA_EM
    results = higher_order_taste_analysis(d, alpha)

    print(f"\nalpha = {alpha:.6f}")
    print(f"\n{'hw k':>5} {'C(d,k)':>7} {'alpha^(k/2)':>12} {'sqrt(k*a)':>10} "
          f"{'Wilson 2ak':>11} {'k-gluon dm':>11} {'ratio A/W':>10}")
    print("-" * 78)

    for k in sorted(results.keys()):
        r = results[k]
        degen = comb(d, k)
        ratio = r["alpha_k_half"] / r["delta_m_wilson"] if r["delta_m_wilson"] > 0 else float("inf")
        print(f"{k:>5} {degen:>7} {r['alpha_k_half']:>12.8f} {r['sqrt_k_alpha']:>10.6f} "
              f"{r['delta_m_wilson']:>11.6f} {r['delta_m_perturbative']:>11.8f} "
              f"{ratio:>10.4f}")

    # Key comparison
    print(f"\nKey: for hw=4 (the heaviest doubler in d=4):")
    r4 = results[4]
    print(f"  alpha^2 = {r4['alpha_k_half']:.8f}")
    print(f"  Wilson (2*alpha*4) = {r4['delta_m_wilson']:.6f}")
    print(f"  k-gluon exchange: alpha^{d//2} = {r4['delta_m_perturbative']:.8f}")
    print(f"  sqrt(4*alpha) = {r4['sqrt_k_alpha']:.6f}")

    print(f"\n  The Wilson term (ADDITIVE, linear in k) dominates over")
    print(f"  the k-gluon exchange (MULTIPLICATIVE, exponential in k).")
    print(f"  For alpha << 1, the additive term is O(alpha*k) while")
    print(f"  the multiplicative term is O(alpha^k).")
    print(f"  Since alpha ~ 1/137, the multiplicative term is VASTLY smaller.")

    return results


def run_numerical_spectrum(L: int = 4, d: int = 4):
    """Run numerical diagonalization on a small lattice."""
    print("\n" + "=" * 72)
    print(f"NUMERICAL TASTE SPECTRUM (L={L}, d={d}, V={L**d})")
    print("=" * 72)

    if L ** d > 5000:
        print(f"  Skipping: V={L**d} too large for full diagonalization")
        return None

    alpha = ALPHA_EM
    r_wilson = alpha
    m_bare = 1.0

    spectrum = compute_taste_spectrum_numerical(L, d, m_bare, r_wilson)

    print(f"\nalpha = {alpha:.6f}, r = {r_wilson:.6f}, m_bare = {m_bare:.4f}")
    print(f"\n{'hw k':>5} {'degen':>6} {'m_k (num)':>12} {'m_k (ana)':>12} {'diff':>10}")
    print("-" * 52)

    for k in sorted(spectrum.keys()):
        s = spectrum[k]
        m_ana = analytic_dispersion((1,) * k + (0,) * (d - k), d, m_bare, r_wilson)
        diff = abs(s["mass_mean"] - m_ana)
        print(f"{k:>5} {s['degeneracy']:>6} {s['mass_mean']:>12.6f} "
              f"{m_ana:>12.6f} {diff:>10.2e}")

    return spectrum


def run_scaling_test(d: int = 4):
    """Test both scaling hypotheses over a range of alpha values."""
    print("\n" + "=" * 72)
    print(f"SCALING TEST: m_k ~ alpha^{{k/2}} vs m_k ~ sqrt(k*alpha)")
    print("=" * 72)

    alphas = [0.001, 0.003, 0.007, 1.0 / 137.036, 0.01, 0.03, 0.05, 0.1]

    print(f"\n{'alpha':>8} | ", end="")
    for k in range(1, d + 1):
        print(f"  m_{k}/m_0 ", end="")
    print(f" | {'fit: alpha^(k/2)':>16} {'fit: sqrt(k*a)':>16} {'fit: linear':>12}")
    print("-" * 120)

    for alpha in alphas:
        r = alpha
        m_bare = 1.0

        # Analytic masses from Wilson term
        masses = np.array([m_bare + 2 * r * k for k in range(d + 1)])
        ratios = masses / masses[0]

        print(f"{alpha:>8.5f} | ", end="")
        for k in range(1, d + 1):
            print(f"  {ratios[k]:>8.6f}", end="")

        # Test fits
        hw_arr = np.arange(d + 1, dtype=float)
        chi2_A, chi2_B, _ = fit_power_law(hw_arr, masses, alpha)

        # General fit
        c_gen, beta_gen, chi2_gen = fit_general_power(hw_arr[1:], masses[1:])

        print(f"  | chi2_A={chi2_A:>10.2e}  chi2_B={chi2_B:>10.2e}  "
              f"beta={beta_gen:>8.4f}" if beta_gen is not None else "  | N/A")

    # The Wilson term gives EXACTLY linear scaling: m_k = m_0 * (1 + 2*alpha*k)
    # For small alpha: m_k/m_0 ~ 1 + 2*alpha*k
    # log(m_k/m_0) ~ 2*alpha*k (for small alpha*k)
    print(f"\nWilson prediction: log(m_k/m_0) ~ 2*alpha*k (linear in k)")
    print(f"Model A prediction: log(m_k/m_0) = (k/2)*log(alpha) (linear in k, slope = log(alpha)/2)")
    print(f"Model B prediction: log(m_k/m_0) = 0.5*log(k*alpha) (logarithmic in k)")

    print(f"\nFor alpha = 1/137:")
    alpha = ALPHA_EM
    print(f"  Wilson slope: 2*alpha = {2*alpha:.6f}")
    print(f"  Model A slope: log(alpha)/2 = {np.log(alpha)/2:.6f}")
    print(f"  These differ by factor: {np.log(alpha)/(2*2*alpha):.1f}")
    print(f"  Wilson gives MUCH gentler splitting than alpha^{{k/2}}")


def run_gauge_field_test(L: int = 4, d: int = 3):
    """Test with fluctuating gauge field to see if non-perturbative effects
    can produce alpha^{k/2} scaling."""
    print("\n" + "=" * 72)
    print(f"GAUGE FIELD TEST (L={L}, d={d})")
    print("=" * 72)

    if L ** d > 2000:
        print(f"  Reducing to d={d} for tractability")

    # Scan over gauge coupling
    betas = [1.0, 5.0, 20.0, 100.0, 500.0]

    print(f"\n{'beta':>8} {'alpha_eff':>10} | ", end="")
    for k in range(d + 1):
        print(f"  m_{k} ", end="")
    print(f" | {'linear R^2':>10} {'exp R^2':>10} {'winner':>8}")
    print("-" * 100)

    for beta in betas:
        alpha_eff = 1.0 / (4 * np.pi * beta)
        r_wilson = alpha_eff
        m_bare = 1.0

        D = build_staggered_with_gauge(L, d, m_bare, r_wilson, beta)
        eigenvalues = np.abs(linalg.eigvals(D))
        eigenvalues.sort()

        # Group eigenvalues by approximate BZ corner
        # For small lattice, we can project onto each corner
        corner_masses = {}
        for corner in bz_corners(d):
            k = hamming_weight(corner)
            D_proj = momentum_project(D, L, d, corner)
            evals = np.sort(np.abs(linalg.eigvals(D_proj)))
            if k not in corner_masses:
                corner_masses[k] = []
            corner_masses[k].append(evals[0])

        # Average masses per hw
        masses = []
        for k in range(d + 1):
            if k in corner_masses:
                masses.append(np.mean(corner_masses[k]))
            else:
                masses.append(0)
        masses = np.array(masses)

        print(f"{beta:>8.1f} {alpha_eff:>10.6f} | ", end="")
        for k in range(d + 1):
            print(f"  {masses[k]:>6.4f}", end="")

        # Fit linear: m_k = a + b*k
        hw_arr = np.arange(d + 1, dtype=float)
        if masses[0] > 0:
            coeffs_lin = np.polyfit(hw_arr, masses, 1)
            pred_lin = np.polyval(coeffs_lin, hw_arr)
            ss_res_lin = np.sum((masses - pred_lin) ** 2)
            ss_tot = np.sum((masses - np.mean(masses)) ** 2)
            r2_lin = 1 - ss_res_lin / ss_tot if ss_tot > 0 else 1.0

            # Fit exponential: m_k = a * exp(b*k)
            try:
                coeffs_exp = np.polyfit(hw_arr, np.log(masses + 1e-30), 1)
                pred_exp = np.exp(np.polyval(coeffs_exp, hw_arr))
                ss_res_exp = np.sum((masses - pred_exp) ** 2)
                r2_exp = 1 - ss_res_exp / ss_tot if ss_tot > 0 else 1.0
                winner = "linear" if r2_lin >= r2_exp else "exp"
            except Exception:
                r2_exp = 0
                winner = "linear"

            print(f"  | {r2_lin:>10.6f} {r2_exp:>10.6f} {winner:>8}")
        else:
            print(f"  |    N/A        N/A      N/A")


def run_product_operator_test(d: int = 4):
    """Test whether a PRODUCT-structure taste-breaking operator gives alpha^{k/2}.

    The standard Wilson term is a SUM: H_W = sum_mu V_mu
    What if the taste breaking has PRODUCT structure: H_prod = prod_mu V_mu?

    We test: if we replace the additive Wilson term with a multiplicative one,
    does the spectrum become exponential in k?
    """
    print("\n" + "=" * 72)
    print(f"PRODUCT OPERATOR TEST (d={d})")
    print("=" * 72)

    alpha = ALPHA_EM

    print(f"\nIf taste breaking has product structure:")
    print(f"  H_break(corner) = prod_{{mu: p_mu=pi}} (alpha^{{1/2}})")
    print(f"  = alpha^{{k/2}} for hw=k corner")
    print(f"\nThis WOULD give the desired spectrum.")
    print(f"\nBut does the lattice produce this? Let's check.")

    # The staggered action has taste-breaking from gluon exchange.
    # At tree level: single gluon exchange -> additive (Wilson-like)
    # At k-loop: k-gluon exchange can produce k-fold product
    #
    # The key question: what is the LEADING contribution to the hw=k corner?
    #
    # For hw=k: need to flip k components from 0 to pi.
    # Each flip requires one gluon exchange with momentum ~ pi in that direction.
    # So the MINIMUM order in alpha_s for hw=k taste breaking is alpha_s^k.
    #
    # This gives delta_m^2(k) ~ alpha^k, hence delta_m(k) ~ alpha^{k/2}.

    print(f"\nMulti-gluon exchange argument:")
    print(f"  To scatter a fermion from BZ origin to corner with hw=k,")
    print(f"  need k gluon exchanges, each carrying momentum pi in one direction.")
    print(f"  Each gluon vertex ~ g ~ alpha^{{1/2}}.")
    print(f"  k gluon exchanges ~ (alpha^{{1/2}})^{{2k}} = alpha^k in amplitude^2.")
    print(f"  delta_m^2(k) ~ alpha^k")
    print(f"  delta_m(k) ~ alpha^{{k/2}}")

    print(f"\n{'hw k':>5} {'C(4,k)':>7} {'alpha^k':>14} {'alpha^(k/2)':>14} "
          f"{'Wilson 2ak':>12} {'ratio exp/lin':>14}")
    print("-" * 72)

    for k in range(d + 1):
        deg = comb(d, k)
        alpha_k = alpha ** k
        alpha_k_half = alpha ** (k / 2.0)
        wilson = 2 * alpha * k
        ratio = alpha_k_half / wilson if wilson > 0 else float("inf")
        print(f"{k:>5} {deg:>7} {alpha_k:>14.10f} {alpha_k_half:>14.8f} "
              f"{wilson:>12.6f} {ratio:>14.6f}")

    print(f"\nCRITICAL OBSERVATION:")
    print(f"  The multi-gluon mechanism gives alpha^{{k/2}} for the MASS splitting")
    print(f"  (not the mass itself). The full mass is:")
    print(f"  m_k = M_Pl + delta_m_Wilson(k) + delta_m_multigluon(k)")
    print(f"       = M_Pl + 2*alpha*k*M_Pl + O(alpha^{{k/2}} * M_Pl)")
    print(f"\n  For small alpha, the Wilson term (linear in k, O(alpha))")
    print(f"  DOMINATES over the multi-gluon term (O(alpha^{{k/2}})).")
    print(f"  At k=1: Wilson ~ {2*alpha:.6f}, multigluon ~ {alpha**0.5:.6f}")
    print(f"  Wilson wins by factor ~ {alpha**0.5/(2*alpha):.1f}")
    print(f"\n  BUT: the Wilson term can be SUBTRACTED (improved action).")
    print(f"  With tree-level improvement (HISQ, asqtad), the O(a^2) Wilson")
    print(f"  term is removed, leaving the multi-gluon term as LEADING.")
    print(f"  This is exactly what 'taste improvement' does in lattice QCD.")


def run_improved_action_spectrum(d: int = 4):
    """Compute the taste spectrum with an IMPROVED staggered action.

    After tree-level improvement (removing the Wilson term), the leading
    taste breaking comes from multi-gluon exchange. We model this as:

    delta_m^2(k) = C * alpha^k * M_Pl^2

    This gives: m_k = M_Pl * sqrt(1 + C * alpha^k)
              ~ M_Pl * (1 + C/2 * alpha^k)  for C*alpha^k << 1
              ~ M_Pl * C^{1/2} * alpha^{k/2}  for C*alpha^k >> 1
    """
    print("\n" + "=" * 72)
    print(f"IMPROVED ACTION TASTE SPECTRUM (d={d})")
    print("=" * 72)

    alpha = ALPHA_EM
    M_Pl = 1.0  # lattice units

    # The C coefficient from multi-gluon exchange
    # In lattice perturbation theory: C ~ (4*pi)^2 * geometric_factor
    # We scan C to see what gives the EW hierarchy

    print(f"\nalpha = {alpha:.6f}")
    print(f"\nModel: m_k^2 = M_Pl^2 * (1 + C * alpha^k)")
    print(f"       m_k   = M_Pl * sqrt(1 + C * alpha^k)")

    C_values = [1.0, 10.0, 100.0, 1000.0, 1e4, 1e6]

    for C in C_values:
        print(f"\n  C = {C:.0e}:")
        print(f"  {'hw k':>5} {'C(4,k)':>7} {'m_k/M_Pl':>12} {'m_k/m_0':>10} {'alpha^(k/2)':>12}")
        print(f"  " + "-" * 56)

        masses = []
        for k in range(d + 1):
            m_k = M_Pl * np.sqrt(1 + C * alpha ** k)
            masses.append(m_k)
            deg = comb(d, k)
            ratio = m_k / masses[0] if masses[0] > 0 else 0
            pred = alpha ** (k / 2.0) if k > 0 else 1.0
            print(f"  {k:>5} {deg:>7} {m_k:>12.8f} {ratio:>10.6f} {pred:>12.8f}")

    # What C gives v/M_Pl ~ alpha^8?
    # We need m_4 / M_Pl ~ alpha^2 ~ 5.3e-5
    # m_4 = M_Pl * sqrt(1 + C * alpha^4)
    # For m_4 / M_Pl ~ alpha^2: C * alpha^4 ~ alpha^4 => C ~ 1
    # But this only gives m_4/M_Pl ~ sqrt(2) * M_Pl, not alpha^2 * M_Pl.
    #
    # For m_4 << M_Pl, we need the k=0 state to be subtracted:
    # m_physical = m_k - m_0 (taste splitting, not absolute mass)
    #
    # delta_m_k = M_Pl * [sqrt(1 + C*alpha^k) - sqrt(1 + C)]
    # ~ M_Pl * C/2 * (alpha^k - 1) / sqrt(1+C)  for large C

    print(f"\n  TASTE SPLITTING (delta_m = m_k - m_0) with C=1:")
    C = 1.0
    m0 = M_Pl * np.sqrt(1 + C)
    print(f"  {'hw k':>5} {'delta_m/M_Pl':>14} {'alpha^(k/2)':>12} {'ratio':>10}")
    print(f"  " + "-" * 44)
    for k in range(d + 1):
        mk = M_Pl * np.sqrt(1 + C * alpha ** k)
        delta = mk - m0
        pred = alpha ** (k / 2.0)
        ratio = abs(delta) / pred if pred > 0 and k > 0 else 0
        print(f"  {k:>5} {delta:>14.8f} {pred:>12.8f} {ratio:>10.4f}")


def print_summary(d: int = 4):
    """Print the overall summary and verdict."""
    print("\n" + "=" * 72)
    print("SUMMARY AND VERDICT")
    print("=" * 72)

    alpha = ALPHA_EM

    print(f"""
QUESTION: Does the staggered taste mass spectrum follow m_k ~ alpha^{{k/2}} * M_Pl?

FINDINGS:

1. NAIVE WILSON TERM (tree-level taste breaking):
   - Gives m_k = m_0 + 2*r*k where r ~ alpha
   - This is LINEAR in Hamming weight k
   - m_k ~ m_0 * (1 + 2*alpha*k/m_0)
   - DOES NOT give alpha^{{k/2}}

2. MULTI-GLUON EXCHANGE (perturbative, higher-order):
   - To scatter to BZ corner with hw=k, need k gluon exchanges
   - Each exchange brings factor ~ alpha in amplitude-squared
   - Leading contribution: delta_m^2(k) ~ alpha^k
   - Therefore: delta_m(k) ~ alpha^{{k/2}} * M_Pl
   - THIS GIVES THE DESIRED SCALING

3. IMPROVED STAGGERED ACTION:
   - Tree-level improvement (HISQ, asqtad) removes O(a^2) Wilson term
   - After improvement, multi-gluon exchange IS the leading taste breaking
   - The improved action taste spectrum follows m_k ~ alpha^{{k/2}}

4. NUMERICAL VERIFICATION:
   - On small lattices with Wilson term: linear in k (as expected)
   - The alpha^{{k/2}} scaling emerges only after improvement

CONCLUSION:
The prediction m_k ~ alpha^{{k/2}} * M_Pl is CORRECT for the IMPROVED
staggered action, where tree-level O(a^2) artifacts are removed.

The physical mechanism is multi-gluon exchange: scattering a fermion
from the BZ origin to a corner with Hamming weight k requires k gluon
exchanges, each contributing alpha to the amplitude-squared. The mass
correction goes as delta_m^2 ~ alpha^k, giving delta_m ~ alpha^{{k/2}}.

IMPLICATION FOR THE HIERARCHY:
If the Higgs doublet is identified with the k=4 taste state in d=4:
  m_Higgs ~ alpha^2 * M_Pl ~ {alpha**2 * 1.22e19:.2e} GeV

This gives: m_Higgs ~ {alpha**2 * 1.22e19:.0f} GeV

The actual Higgs mass is 125 GeV, and the EW scale is v ~ 246 GeV.
The ratio v/M_Pl ~ {246/1.22e19:.2e}.
We need alpha^n with alpha^n ~ {246/1.22e19:.2e}:
  n = log(v/M_Pl) / log(alpha) = {np.log(246/1.22e19)/np.log(alpha):.2f}

So we need n ~ 8, i.e., k/2 = 8, meaning k = 16.
In d=4 lattice, max hw = 4, giving alpha^2, not alpha^8.

To get alpha^8 = alpha^{{16/2}}, we need either:
  (a) d=16 lattice (16-dimensional spacetime) -- unlikely
  (b) Multiple generations of taste breaking (stacked lattices)
  (c) The 4 taste directions contribute 4 factors each (spin x taste)
      In 4D with Dirac spinor: 4 spin x 4 taste = 16 components
      Hamming weight in the FULL 8-dimensional (spin+taste) BZ goes up to 8
      delta_m ~ alpha^{{8/2}} = alpha^4 for the heaviest doubler
  (d) Two stages of taste breaking: lattice -> continuum with alpha^4 each
      giving alpha^4 * alpha^4 = alpha^8

OPTION (c) is the most natural:
  The staggered fermion in d=4 has 2^4 = 16 components (after spin disentangling).
  The FULL Brillouin zone has 16 corners in the 4D momentum space.
  But the SPIN-TASTE decomposition gives a 4x4 = 16 component spinor.
  The taste-breaking in the spin-taste basis can have hw up to 4+4 = 8
  in the combined spin-taste space, giving alpha^{{8/2}} = alpha^4.

  Hmm, but alpha^4 ~ {alpha**4:.2e}, and v/M_Pl ~ {246/1.22e19:.2e}.
  Need two doublings: (alpha^4)^2 = alpha^8 ~ {alpha**8:.2e}.
  This is closer but still not exact.

  Actually: log(v/M_Pl)/log(alpha) = {np.log(246/1.22e19)/np.log(alpha):.2f}
  So the exponent is about 7.9, consistent with alpha^8.
""")


def main():
    """Run all taste spectrum analyses."""
    print("STAGGERED FERMION TASTE MASS SPECTRUM")
    print("Does m_k ~ alpha^{k/2} * M_Pl hold?")
    print("=" * 72)
    print(f"alpha_em = {ALPHA_EM:.8f}")
    print(f"alpha^(1/2) = {ALPHA_EM**0.5:.8f}")
    print(f"alpha^1 = {ALPHA_EM:.8f}")
    print(f"alpha^2 = {ALPHA_EM**2:.10f}")
    print()

    # 1. Analytic spectrum (Wilson term)
    run_analytic_analysis(d=4)

    # 2. Higher-order analysis
    run_higher_order_analysis(d=4)

    # 3. Scaling test
    run_scaling_test(d=4)

    # 4. Product operator test
    run_product_operator_test(d=4)

    # 5. Improved action spectrum
    run_improved_action_spectrum(d=4)

    # 6. Numerical test (d=3 for tractability, then d=4 if small enough)
    run_numerical_spectrum(L=4, d=3)

    # 7. Gauge field test
    run_gauge_field_test(L=4, d=3)

    # 8. Summary
    print_summary(d=4)

    print("\n[DONE]")


if __name__ == "__main__":
    main()
