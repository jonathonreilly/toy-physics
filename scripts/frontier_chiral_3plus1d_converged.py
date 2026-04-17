#!/usr/bin/env python3
"""
Frontier closure card: 3+1D chiral walk — CONVERGED regime (n=21, N=16).
10/10 property test + convergence verification.

Architecture: 6-component state on n^3 grid.
  Components: psi_{+y}, psi_{-y}, psi_{+z}, psi_{-z}, psi_{+w}, psi_{-w}
  Coin: symmetric Lorentzian [[cos th, i sin th],[i sin th, cos th]] per pair
  Shift: np.roll along each spatial axis
  theta(r) = theta0 * (1 - strength/(r+0.1))
  Periodic BCs, balanced source at center.
"""

import numpy as np
import time

# ── Parameters ──────────────────────────────────────────────────────
N_DEFAULT = 21       # grid size (converged regime n>=17)
L_DEFAULT = 16       # layers (converged regime N>=14)
THETA0 = 0.3
STRENGTH = 5e-4

def make_state(n):
    """Balanced source: equal amplitude on all 6 components at center."""
    psi = np.zeros((6, n, n, n), dtype=np.complex128)
    c = n // 2
    amp = 1.0 / np.sqrt(6.0)
    for k in range(6):
        psi[k, c, c, c] = amp
    return psi

def min_image_dist(n, mass_pos):
    """Minimum-image distance from each site to mass_pos on periodic grid."""
    c = np.arange(n)
    dy = np.abs(c[:, None, None] - mass_pos[0])
    dy = np.minimum(dy, n - dy)
    dz = np.abs(c[None, :, None] - mass_pos[1])
    dz = np.minimum(dz, n - dz)
    dw = np.abs(c[None, None, :] - mass_pos[2])
    dw = np.minimum(dw, n - dw)
    return np.sqrt(dy**2 + dz**2 + dw**2)

def apply_coin_and_shift(psi, n, theta_grid):
    """Apply Lorentzian coin to each pair then shift."""
    cos_t = np.cos(theta_grid)
    sin_t = np.sin(theta_grid)
    new_psi = np.zeros_like(psi)
    # Coin on each pair: (0,1)=+y/-y, (2,3)=+z/-z, (4,5)=+w/-w
    for pair_idx, (a, b) in enumerate([(0,1), (2,3), (4,5)]):
        pa = psi[a]
        pb = psi[b]
        new_psi[a] = cos_t * pa + 1j * sin_t * pb
        new_psi[b] = 1j * sin_t * pa + cos_t * pb
    # Shift: +y -> roll axis0 by -1, -y -> roll axis0 by +1, etc.
    shifts = [(-1, 0), (+1, 0), (0, -1), (0, +1), (0, -1), (0, +1)]
    axes  = [0, 0, 1, 1, 2, 2]
    out = np.zeros_like(new_psi)
    for k in range(6):
        out[k] = np.roll(new_psi[k], shifts[k][0] if axes[k] == 0 else shifts[k][1], axis=axes[k])
    # Correct: each component shifts along its own axis
    result = np.zeros_like(new_psi)
    # +y (comp 0): shift along axis 0 by -1
    result[0] = np.roll(new_psi[0], -1, axis=0)
    # -y (comp 1): shift along axis 0 by +1
    result[1] = np.roll(new_psi[1], +1, axis=0)
    # +z (comp 2): shift along axis 1 by -1
    result[2] = np.roll(new_psi[2], -1, axis=1)
    # -z (comp 3): shift along axis 1 by +1
    result[3] = np.roll(new_psi[3], +1, axis=1)
    # +w (comp 4): shift along axis 2 by -1
    result[4] = np.roll(new_psi[4], -1, axis=2)
    # -w (comp 5): shift along axis 2 by +1
    result[5] = np.roll(new_psi[5], +1, axis=2)
    return result

def evolve(n, n_layers, strength, mass_positions=None):
    """Evolve state for n_layers steps with given mass configuration."""
    psi = make_state(n)
    c = n // 2
    if mass_positions is None:
        mass_positions = [(c, c, c)]
    # Precompute theta grid (sum over all masses)
    theta_grid = np.full((n, n, n), THETA0)
    for mp in mass_positions:
        r = min_image_dist(n, mp)
        f = strength / (r + 0.1)
        theta_grid = theta_grid * (1.0 - f)  # multiplicative: each mass modifies
    # Re-derive: theta(r) = theta0 * prod_masses (1 - strength/(r_i + 0.1))
    # Actually per spec: theta(r) = theta0*(1-f), f = strength/(r+0.1)
    # For multiple masses, use additive f
    theta_grid = np.full((n, n, n), THETA0)
    total_f = np.zeros((n, n, n))
    for mp in mass_positions:
        r = min_image_dist(n, mp)
        total_f += strength / (r + 0.1)
    theta_grid = THETA0 * (1.0 - total_f)

    for _ in range(n_layers):
        psi = apply_coin_and_shift(psi, n, theta_grid)
    return psi

def probability_density(psi):
    """Total probability density at each site."""
    return np.sum(np.abs(psi)**2, axis=0)

def gravity_sign(n, n_layers, strength, mass_offset=3):
    """Check if probability flows TOWARD or AWAY from mass.

    TOWARD = net probability shift toward the mass (positive delta between source and mass).
    We compare delta on the mass side vs the opposite side.
    """
    c = n // 2
    # No mass (control)
    psi0 = evolve(n, n_layers, 0.0)
    rho0 = probability_density(psi0)
    # Mass at offset in z
    mass_pos = [(c, c, c + mass_offset)]
    psi1 = evolve(n, n_layers, strength, mass_pos)
    rho1 = probability_density(psi1)
    delta = rho1 - rho0
    # Force proxy: net probability change in a shell between source and mass
    # vs equivalent shell on opposite side
    toward_val = 0.0
    away_val = 0.0
    for dz in range(1, mass_offset + 1):
        toward_val += delta[c, c, c + dz]
    for dz in range(1, mass_offset + 1):
        away_val += delta[c, c, c - dz]
    # TOWARD if more probability accumulates on the mass side than opposite side
    is_toward = toward_val > away_val
    return is_toward, toward_val, away_val

def born_test(n, n_layers, strength):
    """Born rule: 3 slits in z-direction with absorption barrier."""
    c = n // 2
    barrier_layer = 6  # even layer for parity
    slit_positions = [c - 2, c, c + 2]  # 3 slits in y dimension

    # Run with all 3 slits open: evolve, then at barrier_layer apply absorption
    psi_full = make_state(n)
    theta_grid_flat = np.full((n, n, n), THETA0)

    # Evolve barrier_layer steps
    for step in range(n_layers):
        psi_full = apply_coin_and_shift(psi_full, n, theta_grid_flat)
        if step == barrier_layer - 1:
            # Apply absorption: zero out everything except slit positions in y
            mask = np.zeros((n, n, n), dtype=bool)
            for sy in slit_positions:
                mask[sy, :, :] = True
            for k in range(6):
                psi_full[k] = psi_full[k] * mask

    rho_full = probability_density(psi_full)

    # Run with each slit individually
    rho_singles = []
    for slit_y in slit_positions:
        psi_s = make_state(n)
        for step in range(n_layers):
            psi_s = apply_coin_and_shift(psi_s, n, theta_grid_flat)
            if step == barrier_layer - 1:
                mask = np.zeros((n, n, n), dtype=bool)
                mask[slit_y, :, :] = True
                for k in range(6):
                    psi_s[k] = psi_s[k] * mask
        rho_singles.append(probability_density(psi_s))

    rho_sum = sum(rho_singles)
    # Interference: I3 = rho_full - rho_sum
    I3 = rho_full - rho_sum
    # Born metric: |I3| / total probability
    P_total = np.sum(rho_full)
    I3_norm = np.sum(np.abs(I3))
    ratio = I3_norm / P_total if P_total > 0 else 0.0
    return ratio

def dtv_test(n, n_layers):
    """Distinguishability: d_TV between upper and lower slit distributions."""
    c = n // 2
    barrier_layer = 6
    theta_grid_flat = np.full((n, n, n), THETA0)

    rhos = []
    for slit_y in [c - 2, c + 2]:  # upper and lower
        psi_s = make_state(n)
        for step in range(n_layers):
            psi_s = apply_coin_and_shift(psi_s, n, theta_grid_flat)
            if step == barrier_layer - 1:
                mask = np.zeros((n, n, n), dtype=bool)
                mask[slit_y, :, :] = True
                for k in range(6):
                    psi_s[k] = psi_s[k] * mask
        rhos.append(probability_density(psi_s))

    # Normalize
    p1 = rhos[0] / np.sum(rhos[0]) if np.sum(rhos[0]) > 0 else rhos[0]
    p2 = rhos[1] / np.sum(rhos[1]) if np.sum(rhos[1]) > 0 else rhos[1]
    dtv = 0.5 * np.sum(np.abs(p1 - p2))
    return dtv

def f_zero_control(n, n_layers):
    """f=0 control: gravity sign with strength=0 must give no bias."""
    psi0 = evolve(n, n_layers, 0.0)
    rho0 = probability_density(psi0)
    c = n // 2
    # Check symmetry: sum in +z vs -z
    plus_z = np.sum(rho0[c, c, c+1:c+4])
    minus_z = np.sum(rho0[c, c, c-3:c])
    bias = abs(plus_z - minus_z) / (plus_z + minus_z) if (plus_z + minus_z) > 0 else 0.0
    return bias

def f_prop_m_test(n, n_layers):
    """F proportional to M: sweep strength, check linear scaling."""
    c = n // 2
    strengths = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
    forces = []
    psi0 = evolve(n, n_layers, 0.0)
    rho0 = probability_density(psi0)
    for s in strengths:
        mass_pos = [(c, c, c + 3)]
        psi1 = evolve(n, n_layers, s, mass_pos)
        rho1 = probability_density(psi1)
        delta = rho1 - rho0
        # Force proxy: net probability shift toward mass
        force = sum(delta[c, c, c + dz] for dz in range(1, 4))
        forces.append(force)
    forces = np.array(forces)
    strengths = np.array(strengths)
    # Linear fit: F = a * strength + b
    coeffs = np.polyfit(strengths, forces, 1)
    # R^2
    predicted = np.polyval(coeffs, strengths)
    ss_res = np.sum((forces - predicted)**2)
    ss_tot = np.sum((forces - np.mean(forces))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return r2, coeffs[0], forces

def decoherence_test(n, n_layers):
    """Decoherence via classical noise bath: Born ratio should decrease."""
    c = n // 2
    theta_grid_flat = np.full((n, n, n), THETA0)
    barrier_layer = 6
    slit_positions = [c - 2, c, c + 2]

    def run_with_noise(noise_strength):
        rng = np.random.RandomState(42)
        psi = make_state(n)
        for step in range(n_layers):
            if noise_strength > 0:
                # Apply random phase noise (classical bath)
                phase = rng.uniform(-noise_strength, noise_strength, (n, n, n))
                phase_factor = np.exp(1j * phase)
                for k in range(6):
                    psi[k] = psi[k] * phase_factor
            psi = apply_coin_and_shift(psi, n, theta_grid_flat)
            if step == barrier_layer - 1:
                mask = np.zeros((n, n, n), dtype=bool)
                for sy in slit_positions:
                    mask[sy, :, :] = True
                for k in range(6):
                    psi[k] = psi[k] * mask
        return probability_density(psi)

    # No noise
    rho_full_clean = run_with_noise(0.0)

    # Get single-slit sum for clean
    rho_singles_clean = []
    for slit_y in slit_positions:
        psi_s = make_state(n)
        for step in range(n_layers):
            psi_s = apply_coin_and_shift(psi_s, n, theta_grid_flat)
            if step == barrier_layer - 1:
                mask = np.zeros((n, n, n), dtype=bool)
                mask[slit_y, :, :] = True
                for k in range(6):
                    psi_s[k] = psi_s[k] * mask
        rho_singles_clean.append(probability_density(psi_s))
    I3_clean = np.sum(np.abs(rho_full_clean - sum(rho_singles_clean)))
    P_clean = np.sum(rho_full_clean)
    born_clean = I3_clean / P_clean if P_clean > 0 else 0.0

    # With noise
    rho_full_noisy = run_with_noise(0.5)
    # Single slits with noise
    rho_singles_noisy = []
    for slit_y in slit_positions:
        rng = np.random.RandomState(42)
        psi_s = make_state(n)
        for step in range(n_layers):
            phase = rng.uniform(-0.5, 0.5, (n, n, n))
            phase_factor = np.exp(1j * phase)
            for k in range(6):
                psi_s[k] = psi_s[k] * phase_factor
            psi_s = apply_coin_and_shift(psi_s, n, theta_grid_flat)
            if step == barrier_layer - 1:
                mask = np.zeros((n, n, n), dtype=bool)
                mask[slit_y, :, :] = True
                for k in range(6):
                    psi_s[k] = psi_s[k] * mask
        rho_singles_noisy.append(probability_density(psi_s))
    I3_noisy = np.sum(np.abs(rho_full_noisy - sum(rho_singles_noisy)))
    P_noisy = np.sum(rho_full_noisy)
    born_noisy = I3_noisy / P_noisy if P_noisy > 0 else 0.0

    return born_clean, born_noisy, born_noisy < born_clean

def mutual_information_test(n, n_layers):
    """MI between left/right halves of the lattice."""
    psi = evolve(n, n_layers, STRENGTH, [(n//2, n//2, n//2)])
    rho = probability_density(psi)
    rho_norm = rho / np.sum(rho)

    # Marginals: left half (y < c) and right half (y >= c)
    c = n // 2
    # Joint distribution over (left_y, right_y) summed over z,w
    # Simplify: use y-marginal and z-marginal
    p_y = np.sum(rho_norm, axis=(1, 2))  # shape (n,)
    p_z = np.sum(rho_norm, axis=(0, 2))  # shape (n,)
    p_yz = np.sum(rho_norm, axis=2)      # shape (n, n)

    # MI(Y;Z) = sum p(y,z) log(p(y,z) / (p(y)*p(z)))
    mi = 0.0
    for iy in range(n):
        for iz in range(n):
            if p_yz[iy, iz] > 1e-30 and p_y[iy] > 1e-30 and p_z[iz] > 1e-30:
                mi += p_yz[iy, iz] * np.log(p_yz[iy, iz] / (p_y[iy] * p_z[iz]))
    return mi

def purity_stable_test():
    """Purity stable across L = {12, 14, 16, 18} — all in converged regime."""
    n = N_DEFAULT
    purities = {}
    for L in [12, 14, 16, 18]:
        psi = evolve(n, L, STRENGTH, [(n//2, n//2, n//2)])
        # Purity = sum |psi|^4 / (sum |psi|^2)^2
        rho = probability_density(psi)
        purity = np.sum(rho**2) / np.sum(rho)**2
        purities[L] = purity
    vals = list(purities.values())
    cv = np.std(vals) / np.mean(vals) if np.mean(vals) > 0 else 0.0
    return purities, cv

def gravity_grows_test():
    """Gravity grows with L (number of layers)."""
    n = N_DEFAULT
    c = n // 2
    psi0_cache = {}
    forces = {}
    for L in [12, 14, 16, 18]:
        psi0 = evolve(n, L, 0.0)
        rho0 = probability_density(psi0)
        mass_pos = [(c, c, c + 3)]
        psi1 = evolve(n, L, STRENGTH, mass_pos)
        rho1 = probability_density(psi1)
        delta = rho1 - rho0
        force = sum(delta[c, c, c + dz] for dz in range(1, 4))
        forces[L] = force
    # Check monotonic increase
    vals = [forces[L] for L in [12, 14, 16, 18]]
    monotonic = all(vals[i] <= vals[i+1] for i in range(len(vals)-1))
    return forces, monotonic

def distance_law_test(n, n_layers):
    """Distance law: force vs offset, check power-law scaling.

    Restrict offsets to 2..n//4 to avoid periodic wrapping.
    Force proxy: total delta between source and mass (sum over sites c+1..c+dz),
    same metric used in gravity_sign.
    """
    c = n // 2
    max_offset = min(7, n // 4)
    offsets = list(range(2, max_offset + 1))
    forces = []
    psi0 = evolve(n, n_layers, 0.0)
    rho0 = probability_density(psi0)
    for dz in offsets:
        mass_pos = [(c, c, c + dz)]
        psi1 = evolve(n, n_layers, STRENGTH, mass_pos)
        rho1 = probability_density(psi1)
        delta = rho1 - rho0
        # Force: net probability shift in the region between source and mass
        force = sum(delta[c, c, c + dd] for dd in range(1, dz + 1))
        forces.append(force)
    forces_arr = np.array(forces)
    offsets_arr = np.array(offsets, dtype=float)
    # Use absolute values for log-log fit (force should decrease with distance)
    abs_forces = np.abs(forces_arr)
    valid = abs_forces > 1e-30
    if np.sum(valid) < 3:
        return 0.0, 0.0, dict(zip(offsets, forces))
    log_r = np.log(offsets_arr[valid])
    log_f = np.log(abs_forces[valid])
    coeffs = np.polyfit(log_r, log_f, 1)
    exponent = coeffs[0]
    predicted = np.polyval(coeffs, log_r)
    ss_res = np.sum((log_f - predicted)**2)
    ss_tot = np.sum((log_f - np.mean(log_f))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return exponent, r2, dict(zip(offsets, forces))

def convergence_check():
    """Verify convergence: N=10,12,14,16,18 at n=21."""
    n = N_DEFAULT
    c = n // 2
    results = {}
    psi0_base = evolve(n, 10, 0.0)  # just to warm up, recompute per L
    for L in [10, 12, 14, 16, 18]:
        toward, t_val, a_val = gravity_sign(n, L, STRENGTH)
        results[L] = {'toward': toward, 't': t_val, 'a': a_val}
    return results


# ── MAIN ────────────────────────────────────────────────────────────
if __name__ == '__main__':
    t0 = time.time()
    n = N_DEFAULT
    L = L_DEFAULT
    c = n // 2
    print(f"3+1D Chiral Walk — CONVERGED Closure Card")
    print(f"n={n} ({n**3} sites, {6*n**3} state dim), N={L} layers")
    print(f"theta0={THETA0}, strength={STRENGTH}")
    print("=" * 65)

    score = 0

    # 1. Born |I3|/P
    print("\n[1] Born |I3|/P (3-slit interference)...")
    born = born_test(n, L, STRENGTH)
    p1 = born > 0.01
    print(f"    |I3|/P = {born:.6f}  {'PASS' if p1 else 'FAIL'} (need >0.01)")
    if p1: score += 1

    # 2. d_TV distinguishability
    print("\n[2] d_TV (upper/lower slit)...")
    dtv = dtv_test(n, L)
    p2 = dtv > 0.01
    print(f"    d_TV = {dtv:.6f}  {'PASS' if p2 else 'FAIL'} (need >0.01)")
    if p2: score += 1

    # 3. f=0 control
    print("\n[3] f=0 control (no mass bias)...")
    bias = f_zero_control(n, L)
    p3 = bias < 0.01
    print(f"    bias = {bias:.8f}  {'PASS' if p3 else 'FAIL'} (need <0.01)")
    if p3: score += 1

    # 4. F proportional to M
    print("\n[4] F proportional to M (linear scaling)...")
    r2_fm, slope_fm, forces_fm = f_prop_m_test(n, L)
    p4 = r2_fm > 0.9
    print(f"    R^2 = {r2_fm:.6f}, slope = {slope_fm:.6e}")
    print(f"    forces = {[f'{f:.4e}' for f in forces_fm]}")
    print(f"    {'PASS' if p4 else 'FAIL'} (need R^2 > 0.9)")
    if p4: score += 1

    # 5. Gravity sign TOWARD
    print("\n[5] Gravity sign...")
    toward, t_val, a_val = gravity_sign(n, L, STRENGTH)
    p5 = toward
    print(f"    toward={t_val:.6e}, away={a_val:.6e}")
    print(f"    {'TOWARD' if toward else 'AWAY'}  {'PASS' if p5 else 'FAIL'}")
    if p5: score += 1

    # 6. Decoherence
    print("\n[6] Decoherence (CL bath reduces interference)...")
    bc, bn, decoh = decoherence_test(n, L)
    p6 = decoh
    print(f"    Born clean = {bc:.6f}, Born noisy = {bn:.6f}")
    print(f"    {'PASS' if p6 else 'FAIL'} (noisy < clean)")
    if p6: score += 1

    # 7. Mutual information
    print("\n[7] Mutual information (Y;Z)...")
    mi = mutual_information_test(n, L)
    p7 = mi > 0.0
    print(f"    MI = {mi:.6e}  {'PASS' if p7 else 'FAIL'} (need >0)")
    if p7: score += 1

    # 8. Purity stable
    print("\n[8] Purity stable across L={12,14,16,18}...")
    purities, cv = purity_stable_test()
    p8 = cv < 0.5
    for ll, pu in purities.items():
        print(f"    L={ll}: purity = {pu:.6e}")
    print(f"    CV = {cv:.4f}  {'PASS' if p8 else 'FAIL'} (need CV < 0.5)")
    if p8: score += 1

    # 9. Gravity grows with L
    print("\n[9] Gravity grows with L...")
    gforces, mono = gravity_grows_test()
    p9 = mono
    for ll, gf in gforces.items():
        print(f"    L={ll}: force = {gf:.6e}")
    print(f"    Monotonic: {mono}  {'PASS' if p9 else 'FAIL'}")
    if p9: score += 1

    # 10. Distance law
    print("\n[10] Distance law (power-law exponent)...")
    exp_dl, r2_dl, forces_dl = distance_law_test(n, L)
    p10 = r2_dl > 0.7
    for dd, ff in forces_dl.items():
        print(f"    offset={dd}: force = {ff:.6e}")
    print(f"    exponent = {exp_dl:.3f}, R^2 = {r2_dl:.4f}")
    print(f"    {'PASS' if p10 else 'FAIL'} (need R^2 > 0.7)")
    if p10: score += 1

    # ── Summary ─────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print(f"SCORE: {score}/10")
    results = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
    labels = ["Born", "d_TV", "f=0", "F~M", "TOWARD", "Decoh", "MI", "Purity", "GravGrow", "DistLaw"]
    for lab, res in zip(labels, results):
        print(f"  {lab:10s} {'PASS' if res else 'FAIL'}")
    print("=" * 65)

    # ── Convergence check ───────────────────────────────────────
    print("\n--- CONVERGENCE CHECK (n=21, varying N) ---")
    conv = convergence_check()
    for ll in [10, 12, 14, 16, 18]:
        r = conv[ll]
        tag = "TOWARD" if r['toward'] else "AWAY"
        print(f"  N={ll:2d}: {tag}  (toward={r['t']:.4e}, away={r['a']:.4e})")

    elapsed = time.time() - t0
    print(f"\nTotal time: {elapsed:.1f}s")
    print("\nHYPOTHESIS: 3+1D chiral walk passes 10/10 in converged regime.")
    if score == 10:
        print("RESULT: CONFIRMED")
    else:
        fails = [lab for lab, res in zip(labels, results) if not res]
        print(f"RESULT: FALSIFIED — failed: {', '.join(fails)}")
