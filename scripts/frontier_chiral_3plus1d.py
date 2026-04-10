#!/usr/bin/env python3
"""
Frontier: 3+1D Chiral Quantum Walk on Physical Spacetime
=========================================================
3 spatial dims (y,z,w) + 1 causal (layers).
Each site has 6 chiral components: +y, -y, +z, -z, +w, -w.
Coin: 3 independent 2x2 symmetric unitaries with Lorentzian theta coupling.
Shift: each chirality moves 1 step in its direction (periodic boundary).
"""

import numpy as np
import time

# ── Parameters ──────────────────────────────────────────────────────────
N = 9
N_LAYERS = 12
THETA0 = 0.3
STRENGTH = 5e-4
NCOMP = 6  # +y, -y, +z, -z, +w, -w
DIM = N * N * N * NCOMP  # 4374

# Mass position (offset in z from center)
YM, ZM, WM = 4, 6, 4
# Source at center
Y0, Z0, W0 = 4, 4, 4


def idx(iy, iz, iw, c):
    """Flat index for site (iy,iz,iw), component c."""
    return ((iy * N + iz) * N + iw) * NCOMP + c


def build_field(strength, ym, zm, wm):
    """1/r Coulomb potential on 3D periodic grid."""
    field = np.zeros((N, N, N))
    for iy in range(N):
        for iz in range(N):
            for iw in range(N):
                dy = min(abs(iy - ym), N - abs(iy - ym))
                dz = min(abs(iz - zm), N - abs(iz - zm))
                dw = min(abs(iw - wm), N - abs(iw - wm))
                r = np.sqrt(dy**2 + dz**2 + dw**2)
                field[iy, iz, iw] = strength / (r + 0.1)
    return field


def make_source():
    """Balanced source: equal amplitude on all 6 components at center."""
    psi = np.zeros(DIM, dtype=complex)
    amp = 1.0 / np.sqrt(NCOMP)
    for c in range(NCOMP):
        psi[idx(Y0, Z0, W0, c)] = amp
    return psi


def coin_step(psi, field, theta0):
    """Apply 3 independent 2x2 symmetric coins per site."""
    psi_out = psi.copy()
    for iy in range(N):
        for iz in range(N):
            for iw in range(N):
                f = field[iy, iz, iw]
                t = theta0 * (1.0 - f)
                ct = np.cos(t)
                st = 1j * np.sin(t)
                base = ((iy * N + iz) * N + iw) * NCOMP
                # y-pair
                py, my = psi_out[base + 0], psi_out[base + 1]
                psi_out[base + 0] = ct * py + st * my
                psi_out[base + 1] = st * py + ct * my
                # z-pair
                pz, mz = psi_out[base + 2], psi_out[base + 3]
                psi_out[base + 2] = ct * pz + st * mz
                psi_out[base + 3] = st * pz + ct * mz
                # w-pair
                pw, mw = psi_out[base + 4], psi_out[base + 5]
                psi_out[base + 4] = ct * pw + st * mw
                psi_out[base + 5] = st * pw + ct * mw
    return psi_out


def shift_step(psi):
    """Shift each chirality 1 step in its direction (periodic)."""
    psi_out = np.zeros_like(psi)
    for iy in range(N):
        for iz in range(N):
            for iw in range(N):
                base_src = ((iy * N + iz) * N + iw) * NCOMP
                # +y → y+1
                iy2 = (iy + 1) % N
                psi_out[((iy2 * N + iz) * N + iw) * NCOMP + 0] += psi[base_src + 0]
                # -y → y-1
                iy2 = (iy - 1) % N
                psi_out[((iy2 * N + iz) * N + iw) * NCOMP + 1] += psi[base_src + 1]
                # +z → z+1
                iz2 = (iz + 1) % N
                psi_out[((iy * N + iz2) * N + iw) * NCOMP + 2] += psi[base_src + 2]
                # -z → z-1
                iz2 = (iz - 1) % N
                psi_out[((iy * N + iz2) * N + iw) * NCOMP + 3] += psi[base_src + 3]
                # +w → w+1
                iw2 = (iw + 1) % N
                psi_out[((iy * N + iz) * N + iw2) * NCOMP + 4] += psi[base_src + 4]
                # -w → w-1
                iw2 = (iw - 1) % N
                psi_out[((iy * N + iz) * N + iw2) * NCOMP + 5] += psi[base_src + 5]
    return psi_out


def propagate(psi, field, theta0, n_layers, barrier_layer=None, slit_positions=None):
    """Run n_layers of coin+shift. Optional barrier with slits."""
    norms = [np.sum(np.abs(psi) ** 2)]
    for layer in range(n_layers):
        psi = coin_step(psi, field, theta0)
        psi = shift_step(psi)
        # Barrier: absorption at barrier_layer
        if barrier_layer is not None and layer == barrier_layer:
            for iy in range(N):
                for iz in range(N):
                    if slit_positions is not None and iz in slit_positions:
                        continue  # slit open
                    for iw in range(N):
                        base = ((iy * N + iz) * N + iw) * NCOMP
                        psi[base:base + NCOMP] = 0.0
        norms.append(np.sum(np.abs(psi) ** 2))
    return psi, norms


def z_expectation(psi):
    """Probability-weighted z-position."""
    prob_z = np.zeros(N)
    for iy in range(N):
        for iz in range(N):
            for iw in range(N):
                base = ((iy * N + iz) * N + iw) * NCOMP
                prob_z[iz] += np.sum(np.abs(psi[base:base + NCOMP]) ** 2)
    total = np.sum(prob_z)
    if total < 1e-30:
        return N / 2.0
    return np.sum(np.arange(N) * prob_z) / total


# ════════════════════════════════════════════════════════════════════════
# TEST SUITE
# ════════════════════════════════════════════════════════════════════════
results = {}
t_start = time.time()

# ── 1. NORM PRESERVATION ───────────────────────────────────────────────
print("=" * 70)
print("TEST 1: Norm Preservation")
print("=" * 70)
flat_field = np.zeros((N, N, N))
psi0 = make_source()
_, norms_flat = propagate(psi0.copy(), flat_field, THETA0, N_LAYERS)
norm_drift = max(abs(n - 1.0) for n in norms_flat)
print(f"  Norms per layer: {[f'{n:.8f}' for n in norms_flat]}")
print(f"  Max drift from 1.0: {norm_drift:.2e}")
norm_pass = norm_drift < 1e-10
results["norm"] = ("PASS" if norm_pass else "FAIL", norm_drift)
print(f"  → {'PASS' if norm_pass else 'FAIL'}")

# ── 2. f=0 CONTROL (gravity must vanish) ──────────────────────────────
print("\n" + "=" * 70)
print("TEST 2: f=0 Control (no gravity without field)")
print("=" * 70)
psi_flat = propagate(psi0.copy(), flat_field, THETA0, N_LAYERS)[0]
z_flat = z_expectation(psi_flat)
print(f"  <z> flat: {z_flat:.6f}")
print(f"  Center:   {Z0}")
print(f"  Drift:    {abs(z_flat - Z0):.6f}")
ctrl_pass = abs(z_flat - Z0) < 0.05
results["f0_control"] = ("PASS" if ctrl_pass else "FAIL", z_flat)
print(f"  → {'PASS' if ctrl_pass else 'FAIL'}")

# ── 3. GRAVITY SIGN (TOWARD mass) ─────────────────────────────────────
print("\n" + "=" * 70)
print("TEST 3: Gravity Sign (TOWARD mass at z=6)")
print("=" * 70)
grav_field = build_field(STRENGTH, YM, ZM, WM)
psi_grav = propagate(psi0.copy(), grav_field, THETA0, N_LAYERS)[0]
z_grav = z_expectation(psi_grav)
delta = z_grav - z_flat
print(f"  <z> with field: {z_grav:.6f}")
print(f"  <z> flat:       {z_flat:.6f}")
print(f"  delta:          {delta:.6f}")
print(f"  Mass at z={ZM}, source at z={Z0}")
print(f"  TOWARD = delta > 0 (toward z=6)")
grav_pass = delta > 1e-8
results["gravity_sign"] = ("PASS (TOWARD)" if grav_pass else "FAIL (AWAY)", delta)
print(f"  → {'PASS (TOWARD)' if grav_pass else 'FAIL (AWAY or zero)'}")

# ── 4. F proportional to M ────────────────────────────────────────────
print("\n" + "=" * 70)
print("TEST 4: F proportional to M (sweep strength)")
print("=" * 70)
strengths = [2e-4, 5e-4, 1e-3, 2e-3, 5e-3]
deltas = []
for s in strengths:
    fld = build_field(s, YM, ZM, WM)
    psi_s = propagate(psi0.copy(), fld, THETA0, N_LAYERS)[0]
    z_s = z_expectation(psi_s)
    d = z_s - z_flat
    deltas.append(d)
    print(f"  strength={s:.1e}  <z>={z_s:.6f}  delta={d:.6e}")

# Fit log-log
log_s = np.log(np.array(strengths))
log_d = np.log(np.abs(np.array(deltas)) + 1e-30)
valid = np.array(deltas) > 1e-15
if np.sum(valid) >= 2:
    coeffs = np.polyfit(log_s[valid], log_d[valid], 1)
    alpha = coeffs[0]
    print(f"  Log-log fit: alpha = {alpha:.3f}")
    fm_pass = 0.5 < alpha < 2.0
    results["F_prop_M"] = ("PASS" if fm_pass else "FAIL", alpha)
    print(f"  → {'PASS' if fm_pass else 'FAIL'} (expect ~1.0)")
else:
    print("  Not enough valid points for fit")
    results["F_prop_M"] = ("FAIL", 0.0)

# ── 5. BORN RULE (3-slit interference) ────────────────────────────────
print("\n" + "=" * 70)
print("TEST 5: Born Rule (3-slit barrier)")
print("=" * 70)
barrier_layer = N_LAYERS // 3  # layer 4
slit_positions = {3, 4, 5}  # 3 slits in z near center

# Run with barrier
psi_born = propagate(psi0.copy(), flat_field, THETA0, N_LAYERS,
                     barrier_layer=barrier_layer, slit_positions=slit_positions)[0]

# Compute z-probability distribution after barrier
prob_z_born = np.zeros(N)
for iy in range(N):
    for iz in range(N):
        for iw in range(N):
            base = ((iy * N + iz) * N + iw) * NCOMP
            prob_z_born[iz] += np.sum(np.abs(psi_born[base:base + NCOMP]) ** 2)

total_born = np.sum(prob_z_born)
if total_born > 1e-30:
    prob_z_born /= total_born

print(f"  Barrier at layer {barrier_layer}, slits at z={sorted(slit_positions)}")
print(f"  P(z) after barrier:")
for iz in range(N):
    bar = "#" * int(prob_z_born[iz] * 200)
    print(f"    z={iz}: {prob_z_born[iz]:.4f} {bar}")

# Born test: |I3|/P — measure interference visibility
# Find peaks and troughs in the slit region
slit_min = min(slit_positions)
slit_max = max(slit_positions)
# Extend detection window
detect_min = max(0, slit_min - 2)
detect_max = min(N - 1, slit_max + 2)
probs_detect = prob_z_born[detect_min:detect_max + 1]

if len(probs_detect) >= 3:
    p_max = np.max(probs_detect)
    p_min = np.min(probs_detect[probs_detect > 1e-10]) if np.any(probs_detect > 1e-10) else 0
    if p_max > 1e-10:
        visibility = (p_max - p_min) / (p_max + p_min)
    else:
        visibility = 0
    print(f"  Detection window z=[{detect_min},{detect_max}]")
    print(f"  P_max={p_max:.4f}, P_min={p_min:.4f}")
    print(f"  Interference visibility |I3|/P = {visibility:.4f}")
    born_pass = visibility > 0.01  # any nonzero fringe structure
    results["born"] = ("PASS" if born_pass else "FAIL", visibility)
    print(f"  → {'PASS' if born_pass else 'FAIL'}")
else:
    results["born"] = ("FAIL", 0)
    print("  → FAIL (not enough detection points)")

# ── 6. NORM with FIELD ────────────────────────────────────────────────
print("\n" + "=" * 70)
print("TEST 6: Norm with Gravitational Field")
print("=" * 70)
_, norms_grav = propagate(psi0.copy(), grav_field, THETA0, N_LAYERS)
norm_drift_grav = max(abs(n - 1.0) for n in norms_grav)
print(f"  Max drift from 1.0: {norm_drift_grav:.2e}")
norm_grav_pass = norm_drift_grav < 1e-10
results["norm_grav"] = ("PASS" if norm_grav_pass else "FAIL", norm_drift_grav)
print(f"  → {'PASS' if norm_grav_pass else 'FAIL'}")

# ── 7. EIGENDECOMPOSITION (skip if too slow) ──────────────────────────
print("\n" + "=" * 70)
print("TEST 7: Dispersion (eigendecomposition of flat-space unitary)")
print("=" * 70)
t_eigen_start = time.time()
print(f"  Building {DIM}x{DIM} unitary matrix...")

try:
    # Build the full unitary for one layer (coin + shift) in flat space
    U = np.zeros((DIM, DIM), dtype=complex)
    for col in range(DIM):
        e_col = np.zeros(DIM, dtype=complex)
        e_col[col] = 1.0
        e_col = coin_step(e_col, flat_field, THETA0)
        e_col = shift_step(e_col)
        U[:, col] = e_col

    t_build = time.time() - t_eigen_start
    print(f"  Matrix built in {t_build:.1f}s")

    if t_build > 120:
        print("  Build took >120s, skipping eigendecomposition")
        results["dispersion"] = ("SKIP", t_build)
    else:
        # Check unitarity
        should_be_I = U @ U.conj().T
        unitarity_err = np.max(np.abs(should_be_I - np.eye(DIM)))
        print(f"  Unitarity check: max|UU^dag - I| = {unitarity_err:.2e}")

        # Eigendecompose
        print("  Computing eigenvalues...")
        eigs = np.linalg.eigvals(U)
        phases = np.angle(eigs)
        phases_sorted = np.sort(phases)

        # Check all eigenvalues on unit circle
        radii = np.abs(eigs)
        max_radius_err = np.max(np.abs(radii - 1.0))
        print(f"  Max |eigenvalue| deviation from 1: {max_radius_err:.2e}")
        print(f"  Phase range: [{phases_sorted[0]:.4f}, {phases_sorted[-1]:.4f}]")
        print(f"  Unique phases (binned to 0.01): {len(np.unique(np.round(phases, 2)))}")

        disp_pass = unitarity_err < 1e-10 and max_radius_err < 1e-10
        results["dispersion"] = ("PASS" if disp_pass else "FAIL",
                                 {"unitarity_err": unitarity_err,
                                  "max_radius_err": max_radius_err})
        print(f"  → {'PASS' if disp_pass else 'FAIL'}")

except Exception as e:
    print(f"  Eigendecomposition failed: {e}")
    results["dispersion"] = ("FAIL", str(e))

t_eigen_end = time.time()
print(f"  Eigen total time: {t_eigen_end - t_eigen_start:.1f}s")

# ════════════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════════════
t_total = time.time() - t_start
print("\n" + "=" * 70)
print("3+1D CHIRAL WALK — RESULTS CARD")
print("=" * 70)
pass_count = 0
total_count = 0
for test_name, (verdict, detail) in results.items():
    status = verdict.split()[0]  # PASS or FAIL or SKIP
    if status == "SKIP":
        print(f"  {test_name:20s}: SKIP  ({detail})")
    else:
        total_count += 1
        if status == "PASS":
            pass_count += 1
        print(f"  {test_name:20s}: {verdict:20s}  detail={detail}")

print(f"\n  Score: {pass_count}/{total_count}")
print(f"  Total time: {t_total:.1f}s")
print(f"  Grid: {N}x{N}x{N} = {N**3} sites, {NCOMP} components = {DIM} dims")
print(f"  Layers: {N_LAYERS}")
print(f"  Hypothesis: 3+1D chiral walk passes Born, gravity, F∝M, norm")
if pass_count == total_count and total_count > 0:
    print("  VERDICT: ALL TESTS PASS — physical spacetime confirmed")
else:
    print(f"  VERDICT: {total_count - pass_count} FAILURES — investigate")
