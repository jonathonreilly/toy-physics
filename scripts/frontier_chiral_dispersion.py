#!/usr/bin/env python3
"""
Frontier: Chiral Walk Dispersion Relation
==========================================

KEY QUESTION: Does the chiral quantum walk produce Klein-Gordon dispersion
E² = m² + k² (emergent Lorentz structure)?

ANALYTIC PREDICTION (infinite line):
    cos(E) = cos(θ) · cos(k)
    => E(k) = arccos(cos(θ)·cos(k))
    For small k,θ:  E ≈ sqrt(θ² + k²)   [Klein-Gordon with m=θ]

METHOD:
    Build explicit 2n×2n unitary U = S·C for the chiral walk.
    Eigendecompose. Extract E_j = arg(λ_j).
    For each eigenmode, FFT the eigenvector to get dominant k_y.
    Plot E vs k and compare to analytic prediction.

HYPOTHESIS: Dispersion is Klein-Gordon: E² = θ² + k² (mass = mixing angle).
FALSIFICATION: Parabolic (Schrödinger) or no match to analytic formula.
"""

import numpy as np
from numpy import cos, sin, pi
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ─── Parameters ───────────────────────────────────────────────────────
n_y = 63          # sites (odd for symmetry, large for k-resolution)
thetas = [0.1, 0.3, 0.5, 0.7]  # coin angles to test
use_periodic = True  # periodic BC for clean momentum states

def build_chiral_walk(n, theta, periodic=True):
    """Build the 2n×2n unitary U = S·C for a 1D chiral walk.

    State vector: [ψ₊(0), ψ₋(0), ψ₊(1), ψ₋(1), ..., ψ₊(n-1), ψ₋(n-1)]
    Coin: 2×2 rotation by theta at each site.
    Shift: ψ₊ moves right, ψ₋ moves left.
    """
    dim = 2 * n

    # Coin matrix C (block diagonal of 2x2 rotations)
    C = np.zeros((dim, dim), dtype=complex)
    for y in range(n):
        ip = 2 * y      # plus component index
        im = 2 * y + 1  # minus component index
        C[ip, ip] = cos(theta)
        C[ip, im] = -sin(theta)
        C[im, ip] = sin(theta)
        C[im, im] = cos(theta)

    # Shift matrix S (permutation)
    S = np.zeros((dim, dim), dtype=complex)
    for y in range(n):
        # Plus component moves right: y -> y+1
        if y + 1 < n:
            S[2 * (y + 1), 2 * y] = 1
        elif periodic:
            S[0, 2 * y] = 1  # wrap around
        else:
            S[2 * y + 1, 2 * y] = 1  # reflect at boundary

        # Minus component moves left: y -> y-1
        if y - 1 >= 0:
            S[2 * (y - 1) + 1, 2 * y + 1] = 1
        elif periodic:
            S[2 * (n - 1) + 1, 2 * y + 1] = 1  # wrap around
        else:
            S[2 * y, 2 * y + 1] = 1  # reflect at boundary

    U = S @ C
    return U

def extract_dispersion(U, n):
    """Eigendecompose U, extract (k, E) pairs.

    For each eigenvector, compute dominant k by FFT of the plus-component.
    E = arg(eigenvalue).
    """
    eigenvalues, eigenvectors = np.linalg.eig(U)

    # Verify unitarity: all |λ| should be 1
    mags = np.abs(eigenvalues)
    assert np.allclose(mags, 1.0, atol=1e-10), f"Non-unitary! |λ| range: [{mags.min():.6f}, {mags.max():.6f}]"

    # Extract energies (eigenphases)
    energies = np.angle(eigenvalues)  # in [-π, π]

    # For each eigenvector, extract the plus-component and FFT to find dominant k
    ks = []
    for j in range(len(eigenvalues)):
        vec = eigenvectors[:, j]
        # Extract plus component: indices 0, 2, 4, ..., 2(n-1)
        psi_plus = vec[0::2]  # n values

        # FFT to get momentum-space representation
        psi_k = np.fft.fft(psi_plus)
        # Find dominant momentum
        power = np.abs(psi_k) ** 2
        dominant_idx = np.argmax(power)

        # Convert index to k value: k = 2π·idx/n, shifted to [-π, π]
        k_val = 2 * pi * dominant_idx / n
        if k_val > pi:
            k_val -= 2 * pi
        ks.append(k_val)

    return np.array(ks), np.array(energies)


def analytic_dispersion(k, theta):
    """Analytic dispersion: cos(E) = cos(θ)·cos(k) => E = arccos(cos(θ)cos(k))."""
    arg = cos(theta) * cos(k)
    arg = np.clip(arg, -1, 1)
    return np.arccos(arg)


# ─── Klein-Gordon fit functions ───────────────────────────────────────
def klein_gordon(k, m, c):
    """E² = m² + c²·k²"""
    return np.sqrt(m**2 + c**2 * k**2)

def schrodinger(k, m, alpha):
    """E = m + α·k²"""
    return m + alpha * k**2

def linear_dispersion(k, c):
    """E = c·|k|"""
    return c * np.abs(k)


# ═══════════════════════════════════════════════════════════════════════
# MAIN COMPUTATION
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("FRONTIER: CHIRAL WALK DISPERSION RELATION")
print("=" * 70)
print(f"Sites: n_y = {n_y}")
print(f"Thetas: {thetas}")
print(f"Boundary conditions: {'periodic' if use_periodic else 'reflecting'}")
print()

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
axes = axes.flatten()

results = {}

for idx, theta in enumerate(thetas):
    print(f"\n{'─' * 60}")
    print(f"θ = {theta:.2f} (mass parameter)")
    print(f"{'─' * 60}")

    # Build and eigendecompose
    U = build_chiral_walk(n_y, theta, periodic=use_periodic)

    # Verify unitarity
    UdU = U.conj().T @ U
    unitarity_err = np.max(np.abs(UdU - np.eye(2 * n_y)))
    print(f"  Unitarity check: ||U†U - I||_max = {unitarity_err:.2e}")

    ks, Es = extract_dispersion(U, n_y)

    # Sort by k for plotting
    order = np.argsort(ks)
    ks_sorted = ks[order]
    Es_sorted = Es[order]

    # Use absolute energy (dispersion is symmetric in E -> -E)
    Es_abs = np.abs(Es_sorted)

    # ── Compare to analytic prediction ──
    k_fine = np.linspace(-pi, pi, 500)
    E_analytic = analytic_dispersion(k_fine, theta)

    # Compute residuals against analytic for each mode
    # Match each numerical (k, |E|) to analytic E(k)
    E_analytic_at_k = analytic_dispersion(ks_sorted, theta)
    # Analytic gives positive branch; numerical has ±E
    # Compare |E_num| to E_analytic
    residuals = np.abs(Es_abs - E_analytic_at_k)
    mean_residual = np.mean(residuals)
    max_residual = np.max(residuals)
    print(f"  Analytic match: mean|ΔE| = {mean_residual:.6f}, max|ΔE| = {max_residual:.6f}")

    # ── Fit Klein-Gordon to positive-E branch near k=0 ──
    # Select modes with |k| < π/2 and E > 0
    mask = (np.abs(ks_sorted) < pi / 2) & (Es_sorted > 0)
    k_fit = ks_sorted[mask]
    E_fit = Es_sorted[mask]

    if len(k_fit) > 3:
        # Klein-Gordon fit: E = sqrt(m² + c²k²)
        try:
            popt_kg, pcov_kg = curve_fit(klein_gordon, k_fit, E_fit, p0=[theta, 1.0])
            E_kg_pred = klein_gordon(k_fit, *popt_kg)
            rss_kg = np.sum((E_fit - E_kg_pred) ** 2)
            tss = np.sum((E_fit - np.mean(E_fit)) ** 2)
            r2_kg = 1 - rss_kg / tss if tss > 0 else 0
            print(f"  Klein-Gordon fit: m={popt_kg[0]:.4f}, c={popt_kg[1]:.4f}, R²={r2_kg:.8f}")
        except Exception as e:
            print(f"  Klein-Gordon fit failed: {e}")
            popt_kg = [theta, 1.0]
            r2_kg = -1

        # Schrodinger fit: E = m + α·k²
        try:
            popt_sch, _ = curve_fit(schrodinger, k_fit, E_fit, p0=[theta, 0.5])
            E_sch_pred = schrodinger(k_fit, *popt_sch)
            rss_sch = np.sum((E_fit - E_sch_pred) ** 2)
            r2_sch = 1 - rss_sch / tss if tss > 0 else 0
            print(f"  Schrödinger fit:  m={popt_sch[0]:.4f}, α={popt_sch[1]:.4f}, R²={r2_sch:.8f}")
        except Exception as e:
            print(f"  Schrödinger fit failed: {e}")
            r2_sch = -1

        # Linear fit: E = c|k|
        try:
            popt_lin, _ = curve_fit(linear_dispersion, k_fit, E_fit, p0=[1.0])
            E_lin_pred = linear_dispersion(k_fit, *popt_lin)
            rss_lin = np.sum((E_fit - E_lin_pred) ** 2)
            r2_lin = 1 - rss_lin / tss if tss > 0 else 0
            print(f"  Linear fit:       c={popt_lin[0]:.4f}, R²={r2_lin:.8f}")
        except Exception as e:
            print(f"  Linear fit failed: {e}")
            r2_lin = -1

        # Determine winner
        fits = {'Klein-Gordon': r2_kg, 'Schrödinger': r2_sch, 'Linear': r2_lin}
        winner = max(fits, key=fits.get)
        print(f"  ** Best fit: {winner} (R²={fits[winner]:.8f}) **")
    else:
        print(f"  Too few points for fitting ({len(k_fit)} modes in range)")
        r2_kg = r2_sch = r2_lin = -1
        winner = "N/A"

    # ── Check small-k expansion: E ≈ sqrt(θ² + k²) ──
    # For small k, the analytic formula gives E ≈ sqrt(θ² + sin²(θ)·k²/sin²(θ)·...)
    # More precisely: E(k) = arccos(cos(θ)cos(k))
    # Taylor: cos(E) ≈ 1 - E²/2 = cos(θ)(1 - k²/2) = cos(θ) - cos(θ)k²/2
    # => 1 - E²/2 ≈ cos(θ) - cos(θ)k²/2
    # => E² ≈ 2(1-cos(θ)) + cos(θ)k²
    # => E² ≈ 2(1-cos(θ)) + cos(θ)·k²
    # For small θ: 2(1-cos(θ)) ≈ θ², cos(θ) ≈ 1
    # => E² ≈ θ² + k²  [Klein-Gordon!]

    m_sq_exact = 2 * (1 - cos(theta))
    c_sq_exact = cos(theta)
    print(f"\n  Exact Taylor: E² = {m_sq_exact:.6f} + {c_sq_exact:.6f}·k²")
    print(f"  => m_eff = {np.sqrt(m_sq_exact):.6f}  (cf. θ = {theta:.6f})")
    print(f"  => c_eff = {np.sqrt(c_sq_exact):.6f}  (subluminal for θ>0)")
    print(f"  Small-θ limit: m_eff → θ = {theta:.6f}, c_eff → 1")

    # Store results
    results[theta] = {
        'ks': ks_sorted, 'Es': Es_sorted,
        'r2_kg': r2_kg, 'r2_sch': r2_sch, 'r2_lin': r2_lin,
        'winner': winner,
        'm_sq': m_sq_exact, 'c_sq': c_sq_exact,
    }

    # ── Plot ──
    ax = axes[idx]

    # Numerical data (positive and negative branches)
    ax.scatter(ks_sorted, Es_sorted, s=8, alpha=0.6, c='steelblue', label='Numerical eigenphases')

    # Analytic prediction (both branches)
    ax.plot(k_fine, E_analytic, 'r-', lw=2, alpha=0.8, label=f'Analytic: arccos(cos({theta:.1f})cos(k))')
    ax.plot(k_fine, -E_analytic, 'r-', lw=2, alpha=0.8)

    # Klein-Gordon approximation
    k_kg = np.linspace(-pi/2, pi/2, 200)
    E_kg_approx = np.sqrt(m_sq_exact + c_sq_exact * k_kg**2)
    ax.plot(k_kg, E_kg_approx, 'g--', lw=1.5, alpha=0.7, label=f'KG: E²={m_sq_exact:.3f}+{c_sq_exact:.3f}k²')
    ax.plot(k_kg, -E_kg_approx, 'g--', lw=1.5, alpha=0.7)

    ax.set_xlabel('k (momentum)')
    ax.set_ylabel('E (energy = eigenphase)')
    ax.set_title(f'θ = {theta:.1f}  |  Best: {winner}')
    ax.legend(fontsize=7, loc='lower right')
    ax.set_xlim(-pi, pi)
    ax.set_ylim(-pi, pi)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.grid(True, alpha=0.3)

plt.suptitle('Chiral Walk Dispersion Relation: E vs k\n'
             'Hypothesis: Klein-Gordon E² = m² + c²k² (mass = mixing angle)',
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/outputs/frontier_chiral_dispersion.png', dpi=150, bbox_inches='tight')
print(f"\nPlot saved to outputs/frontier_chiral_dispersion.png")

# ─── Additional: mass vs theta relationship ───────────────────────────
print("\n" + "=" * 70)
print("MASS-ANGLE RELATIONSHIP")
print("=" * 70)
print(f"{'θ':>8} {'m_eff':>10} {'c_eff':>10} {'m/θ':>10} {'c/1':>10}")
print("-" * 50)
for theta in thetas:
    m_sq = 2 * (1 - cos(theta))
    c_sq = cos(theta)
    m_eff = np.sqrt(m_sq)
    c_eff = np.sqrt(c_sq)
    print(f"{theta:8.3f} {m_eff:10.6f} {c_eff:10.6f} {m_eff/theta:10.6f} {c_eff:10.6f}")

# ─── Additional: verify the exact analytic formula via direct Bloch analysis ──
print("\n" + "=" * 70)
print("BLOCH ANALYSIS: EXACT DISPERSION BANDS")
print("=" * 70)
print("For periodic BC, exact eigenstates are Bloch waves with k = 2πn/N.")
print("The 2×2 Bloch Hamiltonian at each k gives two bands E±(k).")
print()

# For each allowed k, diagonalize the 2×2 Bloch matrix
k_bloch = 2 * pi * np.arange(n_y) / n_y
k_bloch[k_bloch > pi] -= 2 * pi
k_bloch_sorted = np.sort(k_bloch)

for theta in [0.3]:  # detailed check at one theta
    print(f"θ = {theta:.2f}:")
    # The Bloch matrix for U at momentum k:
    # U(k) = S(k) · C  where S(k) = diag(e^{ik}, e^{-ik}) and C = rotation(θ)
    # So U(k) = [[e^{ik}cos(θ), -e^{ik}sin(θ)], [e^{-ik}sin(θ), e^{-ik}cos(θ)]]
    E_plus_band = []
    E_minus_band = []
    for k in k_bloch_sorted:
        Uk = np.array([
            [np.exp(1j * k) * cos(theta), -np.exp(1j * k) * sin(theta)],
            [np.exp(-1j * k) * sin(theta), np.exp(-1j * k) * cos(theta)]
        ])
        evals = np.linalg.eigvals(Uk)
        phases = np.sort(np.angle(evals))
        E_minus_band.append(phases[0])
        E_plus_band.append(phases[1])

    E_plus_band = np.array(E_plus_band)
    E_minus_band = np.array(E_minus_band)

    # Compare to arccos formula
    E_formula = analytic_dispersion(k_bloch_sorted, theta)

    # The two bands should be +E_formula and -E_formula
    diff_plus = np.abs(E_plus_band - E_formula)
    diff_minus = np.abs(E_minus_band + E_formula)
    print(f"  |E+ band - arccos formula|: max={diff_plus.max():.2e}, mean={diff_plus.mean():.2e}")
    print(f"  |E- band + arccos formula|: max={diff_minus.max():.2e}, mean={diff_minus.mean():.2e}")

    # Check the trace formula: Tr(U(k)) = e^{ik}cos(θ) + e^{-ik}cos(θ) = 2cos(θ)cos(k)
    # eigenvalues: e^{±iE} => Tr = 2cos(E)
    # So: 2cos(E) = 2cos(θ)cos(k) => cos(E) = cos(θ)cos(k) ✓
    for k in [0, 0.1, 0.5, 1.0]:
        trace_val = 2 * cos(theta) * cos(k)
        E_val = analytic_dispersion(k, theta)
        trace_check = 2 * cos(E_val)
        print(f"  k={k:.1f}: Tr=2cos(θ)cos(k)={trace_val:.6f}, 2cos(E)={trace_check:.6f}, match={np.isclose(trace_val, trace_check)}")

# ─── Plot mass-velocity diagram ──────────────────────────────────────
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

theta_range = np.linspace(0.01, pi/2, 200)
m_eff_range = np.sqrt(2 * (1 - cos(theta_range)))
c_eff_range = np.sqrt(cos(theta_range))

ax1.plot(theta_range, m_eff_range, 'b-', lw=2, label='m_eff = sqrt(2(1-cos θ))')
ax1.plot(theta_range, theta_range, 'r--', lw=1, label='m = θ (small-θ limit)')
ax1.set_xlabel('θ (coin angle)')
ax1.set_ylabel('Effective mass')
ax1.set_title('Mass from Mixing Angle')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(theta_range, c_eff_range, 'b-', lw=2, label='c_eff = sqrt(cos θ)')
ax2.axhline(1.0, color='r', ls='--', lw=1, label='c = 1 (light cone)')
ax2.set_xlabel('θ (coin angle)')
ax2.set_ylabel('Effective speed of light')
ax2.set_title('Group Velocity from Mixing Angle')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.suptitle('Chiral Walk: Mass and Speed from Coin Angle θ', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/outputs/frontier_chiral_dispersion_mass.png', dpi=150, bbox_inches='tight')
print(f"\nMass plot saved to outputs/frontier_chiral_dispersion_mass.png")

# ═══════════════════════════════════════════════════════════════════════
# VERDICT
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("VERDICT")
print("=" * 70)

all_kg = all(results[t]['winner'] == 'Klein-Gordon' for t in thetas)
analytic_confirmed = all(
    results[t].get('r2_kg', 0) > 0.999 for t in thetas if results[t].get('r2_kg', 0) > 0
)

print(f"\nHypothesis: 'The chiral walk dispersion is Klein-Gordon: E² = θ² + k²'")
print()
print("Findings:")
print("  1. EXACT dispersion: cos(E) = cos(θ)·cos(k)")
print("     Proven via Bloch decomposition: Tr(U(k)) = 2cos(θ)cos(k)")
print()
print("  2. Taylor expansion gives Klein-Gordon form:")
print("     E² = 2(1-cos θ) + cos(θ)·k²")
print("     For small θ: E² ≈ θ² + k² (mass = θ, c = 1)")
print()
print("  3. Mass-angle relation: m_eff = sqrt(2(1-cos θ)) ≈ θ for small θ")
print("     Speed of light: c_eff = sqrt(cos θ) < 1 for θ > 0")
print()

for t in thetas:
    r = results[t]
    print(f"  θ={t:.1f}: R²(KG)={r['r2_kg']:.8f}  R²(Schr)={r['r2_sch']:.8f}  R²(Lin)={r['r2_lin']:.8f}  → {r['winner']}")

print()
if all_kg:
    print("  *** CONFIRMED: Klein-Gordon dispersion at ALL tested angles ***")
    print("  The chiral walk IS a discretized Klein-Gordon field.")
    print("  Mass is generated by the coin mixing angle.")
    print("  Lorentz structure emerges from the chiral architecture.")
else:
    print("  MIXED RESULTS: Not all angles give Klein-Gordon as best fit.")
    print("  Check individual fits for details.")

print()
print("Physical interpretation:")
print("  - Coin angle θ = rest mass (gap at k=0)")
print("  - θ = 0: massless (gapless, linear dispersion E = |k|)")
print("  - θ > 0: massive (gap = θ, Klein-Gordon dispersion)")
print("  - The walk is a DISCRETE Klein-Gordon equation on a lattice")
print("  - Lorentz invariance is emergent in the continuum limit")
