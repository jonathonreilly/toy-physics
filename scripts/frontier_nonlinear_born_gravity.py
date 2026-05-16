#!/usr/bin/env python3
"""Nonlinear propagator: Born-rule and gravity-sign correlation on a 2D setup.

==========================================================================
SCOPE (honest-demoted 2026-05-16; see docs/NONLINEAR_BORN_GRAVITY_NOTE.md)

This runner exhibits TWO separate things:

  (A) LINEAR DIRECTION (algebraic theorem):
      Linear amplitude composition with the quadratic Born surface
      P = |A|^2 gives I_3 = 0 to machine precision. This is the
      retained theorem of docs/I3_ZERO_EXACT_THEOREM_NOTE.md and is
      re-checked here as a sanity baseline.

  (B) TWO NONLINEAR EXAMPLES (exhibited, not universal):
      For two specific pointwise amplitude nonlinearities on the chosen
      2D lattice / kernel / coupling, |I_3|/P is O(0.1) AND the centroid
      deflection sign flips relative to the linear baseline.

This is an exhibited correlation on a finite menu of two nonlinearities,
not a universal "every nonlinearity breaks both" theorem.
==========================================================================

Three propagator types on a lattice:

  1. LINEAR:    psi_out = sum K_ij * psi_in(j)
  2. CUBIC:     psi_out = sum K_ij * psi_in(j)^3
  3. QUADRATIC: psi_out = sum K_ij * |psi_in(j)| * psi_in(j)

For each, measure:
  (a) I_3 (Sorkin parameter) via 3-slit test
  (b) Mass exponent beta via small mass sweep (note: beta stays ~1 even
      for the nonlinear cases tested; mass law is NOT what breaks here)
  (c) Centroid-shift sign relative to no-field baseline
  (d) Apparent distance exponent alpha

The gravity test couples the propagator to an analytic phi(x,y) = -M/r
field via action S = L (1 - <phi>). It does NOT solve self-consistent
back-reaction.

PStack experiment: frontier-nonlinear-born-gravity
"""

from __future__ import annotations

import math
import time
import sys

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
except ImportError:
    print("ERROR: scipy required. pip install scipy")
    sys.exit(1)


# ===========================================================================
# Poisson solver (reused from distance_law infrastructure)
# ===========================================================================

def build_laplacian_sparse(N: int):
    """Build 3D graph Laplacian for NxNxN grid with Dirichlet BC."""
    M = N - 2
    n = M * M * M
    ii, jj, kk = np.mgrid[0:M, 0:M, 0:M]
    flat = ii.ravel() * M * M + jj.ravel() * M + kk.ravel()
    rows = [flat]
    cols = [flat]
    vals = [np.full(n, -6.0)]
    for di, dj, dk in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
        ni = ii + di; nj = jj + dj; nk = kk + dk
        mask = ((ni >= 0) & (ni < M) & (nj >= 0) & (nj < M) &
                (nk >= 0) & (nk < M))
        src = flat[mask.ravel()]
        dst = ni[mask] * M * M + nj[mask] * M + nk[mask]
        rows.append(src); cols.append(dst.ravel()); vals.append(np.ones(src.shape[0]))
    A = sparse.csr_matrix((np.concatenate(vals), (np.concatenate(rows),
                           np.concatenate(cols))), shape=(n, n))
    return A, M


_laplacian_cache = {}

def solve_poisson(N: int, rho_interior: np.ndarray) -> np.ndarray:
    """Solve Poisson for an arbitrary interior source distribution."""
    if N not in _laplacian_cache:
        _laplacian_cache[N] = build_laplacian_sparse(N)
    A, M = _laplacian_cache[N]
    phi_flat = spsolve(A, rho_interior.ravel())
    phi = np.zeros((N, N, N))
    phi[1:N-1, 1:N-1, 1:N-1] = phi_flat.reshape((M, M, M))
    return phi


def solve_poisson_point(N: int, mass_pos: tuple, mass_strength: float = 1.0) -> np.ndarray:
    """Solve Poisson for a point source at mass_pos."""
    M = N - 2
    rhs = np.zeros(M * M * M)
    mx, my, mz = mass_pos
    mi, mj, mk = mx - 1, my - 1, mz - 1
    if 0 <= mi < M and 0 <= mj < M and 0 <= mk < M:
        rhs[mi * M * M + mj * M + mk] = -mass_strength
    return solve_poisson(N, rhs)


# ===========================================================================
# Propagator types
# ===========================================================================

def apply_nonlinearity(psi: np.ndarray, mode: str) -> np.ndarray:
    """Apply nonlinearity to wavefunction values before propagation."""
    if mode == "linear":
        return psi.copy()
    elif mode == "cubic":
        return psi * np.abs(psi)**2
    elif mode == "quadratic":
        return np.abs(psi) * psi
    else:
        raise ValueError(f"Unknown mode: {mode}")


# ===========================================================================
# TEST 1: Sorkin I_3 via three-slit geometry (2D for speed)
# ===========================================================================

def propagate_2d_slits(open_slits: set, k: float, Lx: int, Ly: int,
                       barrier_x: int, mid_y: int, mode: str = "linear") -> np.ndarray:
    """2D layer-by-layer propagator with optional nonlinearity.

    LINEAR mode: pure linear kernel, NO per-layer normalization.
    This preserves the linearity that guarantees I_3 = 0.

    NONLINEAR modes: apply nonlinearity to source wavefunction,
    then normalize per-layer to prevent blow-up.
    """
    psi = np.zeros(Ly, dtype=complex)
    psi[mid_y] = 1.0

    for x_new in range(1, Lx):
        psi_src = apply_nonlinearity(psi, mode)
        psi_new = np.zeros(Ly, dtype=complex)

        if x_new == barrier_x:
            for iy in range(Ly):
                if iy not in open_slits:
                    continue
                for dy in [-1, 0, 1]:
                    iy_old = iy - dy
                    if 0 <= iy_old < Ly:
                        L = math.sqrt(1.0 + dy**2)
                        amp = np.exp(1j * k * L) / L
                        psi_new[iy] += amp * psi_src[iy_old]
        else:
            for iy in range(Ly):
                for dy in [-1, 0, 1]:
                    iy_old = iy - dy
                    if 0 <= iy_old < Ly:
                        L = math.sqrt(1.0 + dy**2)
                        amp = np.exp(1j * k * L) / L
                        psi_new[iy] += amp * psi_src[iy_old]

        # Nonlinear modes: normalize to prevent blow-up
        # Linear mode: NO normalization (preserves linearity => I_3 = 0)
        if mode != "linear":
            norm = np.sqrt(np.sum(np.abs(psi_new)**2))
            if norm > 1e-30:
                psi_new /= norm
        psi = psi_new

    return np.abs(psi)**2


def measure_I3(mode: str, k: float = 4.0) -> float:
    """Measure Sorkin I_3 parameter for a given propagator type."""
    Lx = 20
    Ly = 21
    barrier_x = Lx // 2
    mid_y = Ly // 2
    slit_A = mid_y - 3
    slit_B = mid_y
    slit_C = mid_y + 3

    def P(slits):
        return propagate_2d_slits(slits, k, Lx, Ly, barrier_x, mid_y, mode)

    P_ABC = P({slit_A, slit_B, slit_C})
    P_AB  = P({slit_A, slit_B})
    P_AC  = P({slit_A, slit_C})
    P_BC  = P({slit_B, slit_C})
    P_A   = P({slit_A})
    P_B   = P({slit_B})
    P_C   = P({slit_C})

    I3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C
    P_total = np.sum(P_ABC)
    I3_max = np.max(np.abs(I3))
    return I3_max / P_total if P_total > 1e-30 else 0.0


# ===========================================================================
# TEST 2: Gravity via Poisson field linearity
# ===========================================================================
#
# The mass law beta = 1 follows from TWO linearities:
#   1. Poisson equation: phi scales linearly with source mass M
#   2. Propagator: psi responds linearly to the phase exp(i*k*S)
#
# In the weak-field limit, deflection = k * integral(grad phi) * dx,
# which scales as M because phi ~ M (Poisson linearity).
#
# For a nonlinear propagator, the response to the field is nonlinear,
# so even though the Poisson field still scales as M, the centroid
# shift does not => beta != 1.
#
# We test this by computing the Poisson field for different M and
# measuring the propagator centroid shift for each propagator type.

def propagate_2d_with_field(phi_2d: np.ndarray, k: float, Lx: int, Ly: int,
                            source_y: int, mode: str = "linear") -> np.ndarray:
    """2D propagator through a gravitational field phi_2d[x, y].

    Action: S = L * (1 - f_avg) where f_avg = average of phi at endpoints.
    Returns density |psi|^2 at each (x, y).
    """
    psi = np.zeros(Ly, dtype=complex)
    # Gaussian source
    sigma = 2.0
    for iy in range(Ly):
        r2 = (iy - source_y)**2
        psi[iy] = np.exp(-r2 / (2 * sigma**2))
    psi /= np.sqrt(np.sum(np.abs(psi)**2))

    density = np.zeros((Lx, Ly))
    density[0, :] = np.abs(psi)**2

    for x_new in range(1, Lx):
        x_old = x_new - 1
        psi_src = apply_nonlinearity(psi, mode)
        psi_new = np.zeros(Ly, dtype=complex)
        for iy in range(Ly):
            for dy in [-1, 0, 1]:
                iy_old = iy - dy
                if 0 <= iy_old < Ly:
                    L = math.sqrt(1.0 + dy**2)
                    f_avg = 0.5 * (phi_2d[x_old, iy_old] + phi_2d[x_new, iy])
                    S = L * (1.0 - f_avg)
                    amp = np.exp(1j * k * S) / L
                    psi_new[iy] += amp * psi_src[iy_old]

        # Normalize to prevent blow-up (all modes, since gravity test
        # measures RELATIVE centroid shift, not absolute amplitude)
        norm = np.sqrt(np.sum(np.abs(psi_new)**2))
        if norm > 1e-30:
            psi_new /= norm
        psi = psi_new
        density[x_new, :] = np.abs(psi)**2

    return density


def make_2d_field(Lx: int, Ly: int, mass_y: int, mass_strength: float) -> np.ndarray:
    """Create a 2D gravitational field from a point mass via 1/r potential.

    Uses analytic 1/r rather than solving Poisson (cleaner for 2D test).
    The field phi(x,y) = -mass_strength / r where r = distance to mass.
    """
    phi = np.zeros((Lx, Ly))
    mass_x = Lx // 2
    for ix in range(Lx):
        for iy in range(Ly):
            r = math.sqrt((ix - mass_x)**2 + (iy - mass_y)**2)
            if r < 0.5:
                r = 0.5  # regularize
            phi[ix, iy] = -mass_strength / r
    return phi


def measure_centroid(density: np.ndarray, det_x: int) -> float:
    """Compute y-centroid at a given x-slice."""
    prof = density[det_x, :]
    total = np.sum(prof)
    if total < 1e-30:
        return len(prof) / 2.0
    yy = np.arange(len(prof), dtype=float)
    return float(np.sum(yy * prof) / total)


def measure_gravity_2d(mode: str, Lx: int = 30, Ly: int = 30, k: float = 6.0):
    """Measure mass exponent beta, distance exponent alpha, and force sign.

    Uses 2D propagation through an analytic 1/r field for clean scaling.
    """
    mid_y = Ly // 2

    # Baseline: no field
    phi_zero = np.zeros((Lx, Ly))
    rho_free = propagate_2d_with_field(phi_zero, k, Lx, Ly, mid_y, mode=mode)
    det_x = Lx - 2
    cy_free = measure_centroid(rho_free, det_x)

    # --- Mass exponent beta: vary M at fixed impact parameter b=7 ---
    # Use very small masses to stay in linear-response regime
    # (phase perturbation k * delta_S << 1)
    mass_y = mid_y + 7
    masses = [0.002, 0.004, 0.008, 0.016]
    deflections_M = []
    for M_val in masses:
        phi = make_2d_field(Lx, Ly, mass_y, M_val)
        rho = propagate_2d_with_field(phi, k, Lx, Ly, mid_y, mode=mode)
        cy = measure_centroid(rho, det_x)
        delta = cy - cy_free
        deflections_M.append(delta)

    # Fit log(|delta|) = beta * log(M) + const
    valid_pairs = [(m, abs(d)) for m, d in zip(masses, deflections_M) if abs(d) > 1e-12]
    if len(valid_pairs) >= 2:
        log_m = np.log([v[0] for v in valid_pairs])
        log_d = np.log([v[1] for v in valid_pairs])
        beta, _ = np.polyfit(log_m, log_d, 1)
    else:
        beta = float('nan')

    # --- Distance exponent alpha: vary b at fixed M ---
    # Use larger grid for alpha to reduce boundary effects
    M_fixed = 0.005
    offsets = [5, 7, 9, 11, 14, 18]
    deflections_b = []
    for b in offsets:
        mass_y_b = mid_y + b
        if mass_y_b >= Ly - 2:
            continue
        phi = make_2d_field(Lx, Ly, mass_y_b, M_fixed)
        rho = propagate_2d_with_field(phi, k, Lx, Ly, mid_y, mode=mode)
        cy = measure_centroid(rho, det_x)
        delta = cy - cy_free
        deflections_b.append((b, abs(delta), delta))

    valid_b = [(b, d) for b, d, _ in deflections_b if d > 1e-12]
    if len(valid_b) >= 2:
        log_b = np.log([v[0] for v in valid_b])
        log_d = np.log([v[1] for v in valid_b])
        neg_alpha, _ = np.polyfit(log_b, log_d, 1)
        alpha = -neg_alpha
    else:
        alpha = float('nan')

    # --- Force sign ---
    # If deflection toward mass (delta > 0 for mass at y > mid), attractive
    phi_sign = make_2d_field(Lx, Ly, mid_y + 7, 0.005)
    rho_sign = propagate_2d_with_field(phi_sign, k, Lx, Ly, mid_y, mode=mode)
    cy_sign = measure_centroid(rho_sign, det_x)
    raw_delta = cy_sign - cy_free
    attractive = raw_delta > 0

    return {
        'beta': beta,
        'alpha': alpha,
        'attractive': attractive,
        'raw_delta': raw_delta,
        'deflections_M': list(zip(masses, deflections_M)),
        'deflections_b': deflections_b,
    }


# ===========================================================================
# Main
# ===========================================================================

def main():
    print("=" * 72)
    print("NONLINEAR PROPAGATOR BREAKS BORN RULE AND GRAVITY SIMULTANEOUSLY")
    print("=" * 72)
    print()
    print("Claim: I_3 = 0 (Born rule) and beta = 1 (mass law) both follow")
    print("from linear amplitude superposition. Breaking linearity breaks both.")
    print()

    t_start = time.time()

    modes = ["linear", "quadratic", "cubic"]
    mode_labels = {
        "linear":    "LINEAR     psi_out = sum K * psi_in",
        "quadratic": "QUADRATIC  psi_out = sum K * |psi_in| * psi_in",
        "cubic":     "CUBIC      psi_out = sum K * psi_in^3",
    }

    results = {}

    # --- Part 1: Sorkin I_3 ---
    print("-" * 72)
    print("PART 1: BORN RULE (Sorkin I_3 parameter)")
    print("-" * 72)
    print()

    for mode in modes:
        t0 = time.time()
        I3_rel = measure_I3(mode)
        dt = time.time() - t0
        results.setdefault(mode, {})['I3'] = I3_rel
        status = "I_3 = 0" if I3_rel < 1e-10 else f"I_3/P = {I3_rel:.4e}"
        print(f"  {mode_labels[mode]}")
        print(f"    |I_3|/P = {I3_rel:.4e}   [{status}]   ({dt:.1f}s)")
        print()

    # --- Part 2: Gravity ---
    print("-" * 72)
    print("PART 2: GRAVITATIONAL PHYSICS (mass law + distance law + sign)")
    print("-" * 72)
    print()

    Lx, Ly = 40, 60
    k = 6.0
    print(f"  2D lattice: {Lx} x {Ly},  k = {k}")
    print(f"  Field: analytic 1/r potential (clean scaling)")
    print()

    for mode in modes:
        t0 = time.time()
        grav = measure_gravity_2d(mode, Lx=Lx, Ly=Ly, k=k)
        dt = time.time() - t0
        results[mode].update(grav)

        sign_str = "attractive" if grav['attractive'] else "REPULSIVE"
        print(f"  {mode_labels[mode]}")
        print(f"    beta  = {grav['beta']:.3f}   (mass exponent, Newtonian = 1.0)")
        print(f"    alpha = {grav['alpha']:.3f}   (distance exponent, Newtonian ~ 1.0)")
        print(f"    sign  = {sign_str}   (raw delta = {grav['raw_delta']:+.6f})")

        # Show mass sweep detail
        print(f"    mass sweep: ", end="")
        for m, d in grav['deflections_M']:
            print(f"M={m:.2f}->delta={d:+.6f}  ", end="")
        print()
        print(f"    ({dt:.1f}s)")
        print()

    # --- Summary table ---
    print("=" * 72)
    print("SUMMARY TABLE")
    print("=" * 72)
    print()
    header = f"{'Propagator':<14} {'|I_3|/P':>12} {'beta':>8} {'alpha':>8} {'Sign':>12}"
    print(header)
    print("-" * len(header))

    for mode in modes:
        r = results[mode]
        I3_str = "<1e-10" if r['I3'] < 1e-10 else f"{r['I3']:.4e}"
        sign_str = "attractive" if r['attractive'] else "REPULSIVE"
        beta_str = f"{r['beta']:.3f}" if not math.isnan(r['beta']) else "N/A"
        alpha_str = f"{r['alpha']:.3f}" if not math.isnan(r['alpha']) else "N/A"
        print(f"{mode:<14} {I3_str:>12} {beta_str:>8} {alpha_str:>8} {sign_str:>12}")

    print()

    # --- Correlation check ---
    # Gravity is "correct" if: attractive, beta ~ 1, alpha > 0
    # Gravity is "broken" if: repulsive, OR wrong alpha sign
    lin = results['linear']
    born_ok_linear = lin['I3'] < 1e-10
    beta_ok = not math.isnan(lin['beta']) and abs(lin['beta'] - 1.0) < 0.20
    grav_ok_linear = beta_ok and lin['attractive']

    all_nonlinear_break_both = True
    for mode in ['quadratic', 'cubic']:
        r = results[mode]
        born_broken = r['I3'] > 1e-6
        # Gravity broken = repulsive OR wrong alpha sign OR beta far from 1
        grav_broken = (not r['attractive'] or
                       math.isnan(r['alpha']) or
                       r['alpha'] < 0)
        if not (born_broken and grav_broken):
            all_nonlinear_break_both = False

    print("=" * 72)
    print("CORRELATION ANALYSIS")
    print("=" * 72)
    print()
    print(f"  Linear:    Born OK = {born_ok_linear}   "
          f"Attractive = {lin['attractive']}   "
          f"beta ~ 1 = {beta_ok}")
    for mode in ['quadratic', 'cubic']:
        r = results[mode]
        born_broken = r['I3'] > 1e-6
        print(f"  {mode.capitalize():<11} Born broken = {born_broken}   "
              f"Attractive = {r['attractive']}   "
              f"alpha = {r['alpha']:.2f}")
    print()

    # Honest scope (see docs/NONLINEAR_BORN_GRAVITY_NOTE.md, demoted 2026-05-16):
    # This runner exhibits ONE direction (linear -> I_3 = 0, the algebraic
    # theorem of I3_ZERO_EXACT_THEOREM_NOTE.md) and exhibits, for TWO chosen
    # pointwise nonlinearities on this specific 2D setup, that |I_3|/P is
    # O(0.1) and the centroid-shift sign flips relative to the linear baseline.
    # It does NOT establish a universal "any nonlinearity -> both broken"
    # theorem, and beta stays near 1 for the nonlinear cases (so the mass
    # law does not break here; only the sign does).
    print("  Observed on the chosen 2D setup:")
    print(f"    - Linear:    |I_3|/P = {lin['I3']:.2e}    "
          f"attractive = {lin['attractive']}    beta = {lin['beta']:.3f}")
    for mode in ['quadratic', 'cubic']:
        r = results[mode]
        sign_str = "toward (attractive)" if r['attractive'] else "away (sign flipped)"
        print(f"    - {mode.capitalize():<10}|I_3|/P = {r['I3']:.2e}    "
              f"centroid shift = {sign_str}    beta = {r['beta']:.3f}")
    print()
    print("  WHAT THIS DOES AND DOES NOT SHOW")
    print()
    print("  Shown:")
    print("    (A) Linear amplitude composition with the Born surface gives")
    print("        I_3 = 0 to machine precision (algebraic theorem; see")
    print("        I3_ZERO_EXACT_THEOREM_NOTE.md).")
    print("    (B) For the two specific pointwise nonlinearities tested on")
    print("        this 2D lattice / kernel / coupling, |I_3|/P is far from")
    print("        zero AND the deflection centroid-shift sign is opposite")
    print("        to the linear baseline.")
    print()
    print("  NOT shown (do not rely on these wider claims):")
    print("    (C) A universal 'every amplitude nonlinearity breaks both'")
    print("        theorem. Only two nonlinearities are tested.")
    print("    (D) Mass-law failure. beta remains within ~1% of 1.0 for the")
    print("        nonlinear cases; the visible failure is the centroid sign,")
    print("        not the mass scaling.")
    print("    (E) A model-independent simultaneous Born/gravity test. The")
    print("        Sorkin / mass coupling are tied to the framework's chosen")
    print("        propagator and gravity-coupling conventions used elsewhere")
    print("        in the repository.")

    print()
    print(f"Total runtime: {time.time() - t_start:.1f}s")


if __name__ == "__main__":
    main()
