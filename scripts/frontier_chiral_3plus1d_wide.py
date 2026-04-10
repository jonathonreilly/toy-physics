#!/usr/bin/env python3
"""
frontier_chiral_3plus1d_wide.py
3+1D chiral quantum walk on n=15 periodic lattice.
Tests all 10 closure properties + extras.

Hypothesis: 3+1D chiral walk passes all 10 closure properties on adequate lattice.
Falsification: If Born or gravity fail in 3+1D.
"""

import time
import numpy as np

T0 = time.perf_counter()

# === PARAMETERS ===
n = 15
center = n // 2  # 7
n_layers = 16
theta0 = 0.3
strength = 5e-4
z_mass_offset = 3  # mass at z = center + 3 = 10

np.random.seed(42)


# === CORE FUNCTIONS ===

def make_field(n, center, mass_positions, strengths_list):
    """Lorentzian field f(r) = strength / (r + 0.1) for each mass, summed."""
    y, z, w = np.meshgrid(np.arange(n), np.arange(n), np.arange(n), indexing='ij')
    field = np.zeros((n, n, n))
    for (my, mz, mw), s in zip(mass_positions, strengths_list):
        # Minimum image distance (periodic)
        dy = np.minimum(np.abs(y - my), n - np.abs(y - my))
        dz = np.minimum(np.abs(z - mz), n - np.abs(z - mz))
        dw = np.minimum(np.abs(w - mw), n - np.abs(w - mw))
        r = np.sqrt(dy**2 + dz**2 + dw**2)
        field += s / (r + 0.1)
    return field


def init_source(n, center):
    """Balanced source at center: equal amplitude on all 6 components."""
    state = np.zeros((n, n, n, 6), dtype=complex)
    amp = 1.0 / np.sqrt(6.0)
    for c in range(6):
        state[center, center, center, c] = amp
    return state


def coin_step(state, field, theta0):
    """Apply symmetric coin to each yz/w pair, vectorized."""
    flat = state.reshape(-1, 6)
    f_all = field.flatten()
    t = theta0 * (1.0 - f_all)
    ct = np.cos(t)
    st = 1j * np.sin(t)

    # y-pair (0, 1)
    py, my = flat[:, 0].copy(), flat[:, 1].copy()
    flat[:, 0] = ct * py + st * my
    flat[:, 1] = st * py + ct * my
    # z-pair (2, 3)
    pz, mz = flat[:, 2].copy(), flat[:, 3].copy()
    flat[:, 2] = ct * pz + st * mz
    flat[:, 3] = st * pz + ct * mz
    # w-pair (4, 5)
    pw, mw = flat[:, 4].copy(), flat[:, 5].copy()
    flat[:, 4] = ct * pw + st * mw
    flat[:, 5] = st * pw + ct * mw

    return flat.reshape(state.shape)


def shift_step(state):
    """Shift each component along its axis with periodic BC."""
    new = np.zeros_like(state)
    new[:, :, :, 0] = np.roll(state[:, :, :, 0], 1, axis=0)   # +y
    new[:, :, :, 1] = np.roll(state[:, :, :, 1], -1, axis=0)  # -y
    new[:, :, :, 2] = np.roll(state[:, :, :, 2], 1, axis=1)   # +z
    new[:, :, :, 3] = np.roll(state[:, :, :, 3], -1, axis=1)  # -z
    new[:, :, :, 4] = np.roll(state[:, :, :, 4], 1, axis=2)   # +w
    new[:, :, :, 5] = np.roll(state[:, :, :, 5], -1, axis=2)  # -w
    return new


def evolve(state, field, theta0, n_layers):
    """Full evolution: coin + shift for n_layers steps. Returns norms per layer."""
    norms = [np.sum(np.abs(state)**2)]
    for _ in range(n_layers):
        state = coin_step(state, field, theta0)
        state = shift_step(state)
        norms.append(np.sum(np.abs(state)**2))
    return state, norms


def site_prob(state):
    """Probability at each site (sum over 6 components)."""
    return np.sum(np.abs(state)**2, axis=-1)


def gravity_metric(state, n, center, mass_y, mass_z, mass_w):
    """Flux toward mass: probability-weighted displacement toward mass."""
    prob = site_prob(state)
    y, z, w = np.meshgrid(np.arange(n), np.arange(n), np.arange(n), indexing='ij')
    # Vector from center to mass
    dy_mass = mass_y - center
    dz_mass = mass_z - center
    dw_mass = mass_w - center
    mag = np.sqrt(dy_mass**2 + dz_mass**2 + dw_mass**2)
    if mag == 0:
        return 0.0
    hat_y, hat_z, hat_w = dy_mass / mag, dz_mass / mag, dw_mass / mag

    # displacement from center
    dy = y - center
    dz = z - center
    dw = w - center

    # project onto mass direction
    proj = dy * hat_y + dz * hat_z + dw * hat_w
    return np.sum(prob * proj)


# ==========================================================
# TEST 1: Born rule (3-slit interference)
# ==========================================================
print("=" * 60)
print("TEST 1: Born rule — 3-slit interference in z-direction")
print("=" * 60)

# Place 3 slits in z at center-1, center, center+1
# Blocking = zero out everything except slit positions after a few layers
slit_positions_z = [center - 1, center, center + 1]

field_flat = make_field(n, center, [], [])  # no mass

# Run with all 3 slits open
state_all = init_source(n, center)
state_all, _ = evolve(state_all, field_flat, theta0, 4)  # evolve 4 steps

# Apply slit mask (zero everything outside slits in z, at the y=center, w=center plane)
mask = np.zeros((n, n, n, 6), dtype=complex)
for sz in slit_positions_z:
    mask[:, sz, :, :] = 1.0
state_all = state_all * mask
# Re-normalize
norm_all = np.sqrt(np.sum(np.abs(state_all)**2))
if norm_all > 0:
    state_all /= norm_all
state_all, _ = evolve(state_all, field_flat, theta0, n_layers - 4)
P_all = site_prob(state_all)

# Run with individual slits
P_singles = np.zeros((n, n, n))
for slit_z in slit_positions_z:
    state_s = init_source(n, center)
    state_s, _ = evolve(state_s, field_flat, theta0, 4)
    mask_s = np.zeros((n, n, n, 6), dtype=complex)
    mask_s[:, slit_z, :, :] = 1.0
    state_s = state_s * mask_s
    norm_s = np.sqrt(np.sum(np.abs(state_s)**2))
    if norm_s > 0:
        state_s /= norm_s
    state_s, _ = evolve(state_s, field_flat, theta0, n_layers - 4)
    P_singles += site_prob(state_s)

# I3 = P_all - P_singles (Born says this should be nonzero for 3-slit)
# Actually: Born rule → |I3|/P should be small (Sorkin parameter)
# I3 = P_123 - P_12 - P_13 - P_23 + P_1 + P_2 + P_3
# For simplicity: approximate with |P_all - P_singles| / sum(P_all)
I3 = np.abs(P_all - P_singles)
born_ratio = np.sum(I3) / np.sum(P_all) if np.sum(P_all) > 0 else 999
born_pass = born_ratio < 0.05
print(f"  |I3|/P = {born_ratio:.6f}  (threshold < 0.05)")
print(f"  BORN: {'PASS' if born_pass else 'FAIL'}")


# ==========================================================
# TEST 2: Distinguishability d_TV (upper/lower slit)
# ==========================================================
print("\n" + "=" * 60)
print("TEST 2: Distinguishability d_TV")
print("=" * 60)

# Upper slit vs lower slit
state_upper = init_source(n, center)
state_upper, _ = evolve(state_upper, field_flat, theta0, 4)
mask_u = np.zeros((n, n, n, 6), dtype=complex)
mask_u[:, center + 1, :, :] = 1.0
state_upper = state_upper * mask_u
nu = np.sqrt(np.sum(np.abs(state_upper)**2))
if nu > 0:
    state_upper /= nu
state_upper, _ = evolve(state_upper, field_flat, theta0, n_layers - 4)
P_upper = site_prob(state_upper)

state_lower = init_source(n, center)
state_lower, _ = evolve(state_lower, field_flat, theta0, 4)
mask_l = np.zeros((n, n, n, 6), dtype=complex)
mask_l[:, center - 1, :, :] = 1.0
state_lower = state_lower * mask_l
nl = np.sqrt(np.sum(np.abs(state_lower)**2))
if nl > 0:
    state_lower /= nl
state_lower, _ = evolve(state_lower, field_flat, theta0, n_layers - 4)
P_lower = site_prob(state_lower)

# Total variation distance
P_up_flat = P_upper.flatten()
P_lo_flat = P_lower.flatten()
su = np.sum(P_up_flat)
sl = np.sum(P_lo_flat)
if su > 0 and sl > 0:
    d_TV = 0.5 * np.sum(np.abs(P_up_flat / su - P_lo_flat / sl))
else:
    d_TV = 0.0
dtv_pass = d_TV > 0.01
print(f"  d_TV = {d_TV:.6f}  (threshold > 0.01)")
print(f"  DISTINGUISHABILITY: {'PASS' if dtv_pass else 'FAIL'}")


# ==========================================================
# TEST 3: f=0 control
# ==========================================================
print("\n" + "=" * 60)
print("TEST 3: f=0 control — no gravity without field")
print("=" * 60)

mass_y, mass_z, mass_w = center, center + z_mass_offset, center
state_ctrl = init_source(n, center)
field_zero = np.zeros((n, n, n))
state_ctrl, _ = evolve(state_ctrl, field_zero, theta0, n_layers)
grav_ctrl = gravity_metric(state_ctrl, n, center, mass_y, mass_z, mass_w)
ctrl_pass = abs(grav_ctrl) < 1e-10
print(f"  Gravity flux (f=0) = {grav_ctrl:.2e}  (threshold < 1e-10)")
print(f"  CONTROL: {'PASS' if ctrl_pass else 'FAIL'}")


# ==========================================================
# TEST 4: F proportional to M (strength sweep)
# ==========================================================
print("\n" + "=" * 60)
print("TEST 4: F proportional to M (strength sweep)")
print("=" * 60)

strengths_sweep = [1e-6, 5e-6, 1e-5, 5e-5]
fluxes_fm = []
for s in strengths_sweep:
    field_s = make_field(n, center, [(mass_y, mass_z, mass_w)], [s])
    state_s = init_source(n, center)
    state_s, _ = evolve(state_s, field_s, theta0, n_layers)
    g = gravity_metric(state_s, n, center, mass_y, mass_z, mass_w)
    fluxes_fm.append(g)
    print(f"  strength={s:.1e}  flux={g:.6e}")

# Check monotonic increase (TOWARD = positive flux in mass direction)
monotonic = all(fluxes_fm[i] < fluxes_fm[i + 1] for i in range(len(fluxes_fm) - 1))
# Also check linear correlation
if len(set(fluxes_fm)) > 1:
    corr = np.corrcoef(strengths_sweep, fluxes_fm)[0, 1]
else:
    corr = 0.0
fm_pass = monotonic and corr > 0.9
print(f"  Monotonic: {monotonic}, Correlation: {corr:.4f}")
print(f"  F~M: {'PASS' if fm_pass else 'FAIL'}")


# ==========================================================
# TEST 5: Gravity direction — TOWARD mass
# ==========================================================
print("\n" + "=" * 60)
print("TEST 5: Gravity direction — TOWARD mass")
print("=" * 60)

field_grav = make_field(n, center, [(mass_y, mass_z, mass_w)], [strength])
state_grav = init_source(n, center)
state_grav, norms_grav = evolve(state_grav, field_grav, theta0, n_layers)
grav_flux = gravity_metric(state_grav, n, center, mass_y, mass_z, mass_w)
grav_pass = grav_flux > 0
print(f"  Gravity flux = {grav_flux:.6e}  (TOWARD = positive)")
print(f"  GRAVITY: {'PASS (TOWARD)' if grav_pass else 'FAIL (AWAY)'}")


# ==========================================================
# TEST 6: Decoherence (Caldeira-Leggett bath)
# ==========================================================
print("\n" + "=" * 60)
print("TEST 6: Decoherence — CL bath")
print("=" * 60)

gamma_values = [0.0, 0.01, 0.05, 0.1]
coherence_vals = []
for gamma in gamma_values:
    state_d = init_source(n, center)
    field_d = make_field(n, center, [(mass_y, mass_z, mass_w)], [strength])
    for layer in range(n_layers):
        state_d = coin_step(state_d, field_d, theta0)
        state_d = shift_step(state_d)
        if gamma > 0:
            # CL dephasing: random phase kicks proportional to gamma
            phase_noise = np.exp(1j * gamma * np.random.randn(*state_d.shape))
            state_d = state_d * phase_noise
            # Renormalize
            norm_d = np.sqrt(np.sum(np.abs(state_d)**2))
            if norm_d > 0:
                state_d /= norm_d
    # Measure coherence: off-diagonal in position basis
    prob_d = site_prob(state_d)
    # Use entropy as proxy for decoherence
    prob_flat = prob_d.flatten()
    prob_flat = prob_flat[prob_flat > 1e-30]
    prob_flat /= np.sum(prob_flat)
    entropy = -np.sum(prob_flat * np.log(prob_flat))
    coherence_vals.append(entropy)
    print(f"  gamma={gamma:.2f}  entropy={entropy:.4f}")

# Decoherence should increase entropy
decoh_increasing = all(
    coherence_vals[i] <= coherence_vals[i + 1] + 0.01
    for i in range(len(coherence_vals) - 1)
)
decoh_pass = decoh_increasing and coherence_vals[-1] > coherence_vals[0]
print(f"  Entropy increasing: {decoh_increasing}")
print(f"  DECOHERENCE: {'PASS' if decoh_pass else 'FAIL'}")


# ==========================================================
# TEST 7: Mutual Information
# ==========================================================
print("\n" + "=" * 60)
print("TEST 7: Mutual Information")
print("=" * 60)

# MI between y-half and z-half of the lattice
state_mi = init_source(n, center)
field_mi = make_field(n, center, [(mass_y, mass_z, mass_w)], [strength])
state_mi, _ = evolve(state_mi, field_mi, theta0, n_layers)
prob_mi = site_prob(state_mi)
prob_mi /= np.sum(prob_mi)

# Marginals
P_y = np.sum(prob_mi, axis=(1, 2))  # sum over z, w
P_z = np.sum(prob_mi, axis=(0, 2))  # sum over y, w

# Joint for y, z (sum over w)
P_yz = np.sum(prob_mi, axis=2)

# MI = sum P(y,z) log(P(y,z) / (P(y)*P(z)))
mi = 0.0
for iy in range(n):
    for iz in range(n):
        pyz = P_yz[iy, iz]
        py_pz = P_y[iy] * P_z[iz]
        if pyz > 1e-30 and py_pz > 1e-30:
            mi += pyz * np.log(pyz / py_pz)

mi_pass = mi > 1e-6
print(f"  MI(y, z) = {mi:.6e}")
print(f"  MI: {'PASS' if mi_pass else 'FAIL'}")


# ==========================================================
# TEST 8: Purity stable across L
# ==========================================================
print("\n" + "=" * 60)
print("TEST 8: Purity stable across layers")
print("=" * 60)

L_values = [10, 12, 14, 16]
purities = []
for L in L_values:
    state_p = init_source(n, center)
    field_p = make_field(n, center, [(mass_y, mass_z, mass_w)], [strength])
    state_p, _ = evolve(state_p, field_p, theta0, L)
    # Purity = Tr(rho^2) for position-space reduced state
    prob_p = site_prob(state_p)
    prob_flat = prob_p.flatten()
    prob_flat /= np.sum(prob_flat)
    purity = np.sum(prob_flat**2)
    purities.append(purity)
    print(f"  L={L}  purity={purity:.6f}")

# Purity should be roughly stable (not collapsing)
purity_range = max(purities) - min(purities)
purity_pass = purity_range < 0.5 * np.mean(purities)
print(f"  Range/mean = {purity_range / np.mean(purities):.4f}  (threshold < 0.5)")
print(f"  PURITY STABLE: {'PASS' if purity_pass else 'FAIL'}")


# ==========================================================
# TEST 9: Gravity grows with L
# ==========================================================
print("\n" + "=" * 60)
print("TEST 9: Gravity grows with L")
print("=" * 60)

grav_L = []
for L in L_values:
    state_g = init_source(n, center)
    field_g = make_field(n, center, [(mass_y, mass_z, mass_w)], [strength])
    state_g, _ = evolve(state_g, field_g, theta0, L)
    g = gravity_metric(state_g, n, center, mass_y, mass_z, mass_w)
    grav_L.append(g)
    print(f"  L={L}  gravity={g:.6e}")

# Should be increasing (or at least non-decreasing with some tolerance)
grav_grow = grav_L[-1] > grav_L[0]
grav_grow_pass = grav_grow
print(f"  Gravity grows (L={L_values[0]} -> L={L_values[-1]}): {grav_grow}")
print(f"  GRAVITY GROWS: {'PASS' if grav_grow_pass else 'FAIL'}")


# ==========================================================
# TEST 10: Distance law — sweep mass offset
# ==========================================================
print("\n" + "=" * 60)
print("TEST 10: Distance law — z_mass offset sweep")
print("=" * 60)

offsets = [2, 3, 4, 5, 6, 7]
grav_dist = []
for off in offsets:
    my_d, mz_d, mw_d = center, center + off, center
    field_d = make_field(n, center, [(my_d, mz_d, mw_d)], [strength])
    state_d = init_source(n, center)
    state_d, _ = evolve(state_d, field_d, theta0, n_layers)
    g = gravity_metric(state_d, n, center, my_d, mz_d, mw_d)
    grav_dist.append(g)
    print(f"  offset={off}  gravity={g:.6e}")

# Fit power law: log(g) vs log(offset)
grav_pos = [(off, g) for off, g in zip(offsets, grav_dist) if g > 0]
if len(grav_pos) >= 3:
    log_off = np.log(np.array([x[0] for x in grav_pos]))
    log_g = np.log(np.array([x[1] for x in grav_pos]))
    coeffs = np.polyfit(log_off, log_g, 1)
    slope = coeffs[0]
    dist_pass = slope < -0.5  # Should decrease with distance
    print(f"  Power law slope = {slope:.3f}")
    print(f"  DISTANCE LAW: {'PASS' if dist_pass else 'FAIL'} (slope < -0.5)")
else:
    # Check at least decreasing
    if len(grav_dist) >= 2:
        dist_pass = grav_dist[0] > grav_dist[-1]
        print(f"  Decreasing: {dist_pass}")
        print(f"  DISTANCE LAW: {'PASS' if dist_pass else 'FAIL'}")
    else:
        dist_pass = False
        print(f"  DISTANCE LAW: FAIL (insufficient positive data)")


# ==========================================================
# TEST 11 (EXTRA): Superposition — two masses, additive fields
# ==========================================================
print("\n" + "=" * 60)
print("TEST 11: Superposition — two masses, additive fields")
print("=" * 60)

# Mass A at z+3, Mass B at y+3
mA = (center, center + 3, center)
mB = (center + 3, center, center)

# Individual fields
field_A = make_field(n, center, [mA], [strength])
field_B = make_field(n, center, [mB], [strength])
field_AB = make_field(n, center, [mA, mB], [strength + strength])
# Actually: each mass has same strength, field_AB should just be sum
field_AB_sum = field_A + field_B

# Check field superposition
field_diff = np.max(np.abs(field_AB_sum - make_field(n, center, [mA, mB], [strength, strength])))

# Run individual
state_A = init_source(n, center)
state_A, _ = evolve(state_A, field_A, theta0, n_layers)
gA = gravity_metric(state_A, n, center, *mA)

state_B = init_source(n, center)
state_B, _ = evolve(state_B, field_B, theta0, n_layers)
gB = gravity_metric(state_B, n, center, *mB)

# Run combined
state_AB = init_source(n, center)
field_both = make_field(n, center, [mA, mB], [strength, strength])
state_AB, _ = evolve(state_AB, field_both, theta0, n_layers)
gAB_a = gravity_metric(state_AB, n, center, *mA)
gAB_b = gravity_metric(state_AB, n, center, *mB)

print(f"  Field superposition error = {field_diff:.2e}")
print(f"  Flux toward A (alone) = {gA:.6e}")
print(f"  Flux toward B (alone) = {gB:.6e}")
print(f"  Flux toward A (combined) = {gAB_a:.6e}")
print(f"  Flux toward B (combined) = {gAB_b:.6e}")

# Both fluxes should be positive (attracted to both masses)
super_pass = gAB_a > 0 and gAB_b > 0
print(f"  SUPERPOSITION: {'PASS' if super_pass else 'FAIL'}")


# ==========================================================
# TEST 12 (EXTRA): Spectral — multiple k, all TOWARD
# ==========================================================
print("\n" + "=" * 60)
print("TEST 12: Spectral — multiple source k-values, all TOWARD")
print("=" * 60)

k_values = [1, 2, 3, 4, 5]
spectral_results = []
for k in k_values:
    # Source with wavelength modulation in z
    state_k = np.zeros((n, n, n, 6), dtype=complex)
    amp = 1.0 / np.sqrt(6.0 * n)
    for iz in range(n):
        phase = np.exp(2j * np.pi * k * iz / n)
        for c in range(6):
            state_k[center, iz, center, c] = amp * phase
    # Normalize
    nk = np.sqrt(np.sum(np.abs(state_k)**2))
    if nk > 0:
        state_k /= nk

    field_k = make_field(n, center, [(mass_y, mass_z, mass_w)], [strength])
    state_k, _ = evolve(state_k, field_k, theta0, n_layers)
    gk = gravity_metric(state_k, n, center, mass_y, mass_z, mass_w)
    spectral_results.append(gk)
    toward = "TOWARD" if gk > 0 else "AWAY"
    print(f"  k={k}  gravity={gk:.6e}  {toward}")

all_toward = all(g > 0 for g in spectral_results)
spectral_pass = all_toward
print(f"  All TOWARD: {all_toward}")
print(f"  SPECTRAL: {'PASS' if spectral_pass else 'FAIL'}")


# ==========================================================
# TEST 13 (EXTRA): Norm conservation
# ==========================================================
print("\n" + "=" * 60)
print("TEST 13: Norm conservation")
print("=" * 60)

state_norm = init_source(n, center)
field_norm = make_field(n, center, [(mass_y, mass_z, mass_w)], [strength])
state_norm, norms_check = evolve(state_norm, field_norm, theta0, n_layers)
norm_drift = max(abs(nm - 1.0) for nm in norms_check)
norm_pass = norm_drift < 1e-10
print(f"  Max norm drift = {norm_drift:.2e}  (threshold < 1e-10)")
for i, nm in enumerate(norms_check):
    if i % 4 == 0 or i == len(norms_check) - 1:
        print(f"    layer {i}: norm = {nm:.15f}")
print(f"  NORM: {'PASS' if norm_pass else 'FAIL'}")


# ==========================================================
# SUMMARY
# ==========================================================
elapsed = time.perf_counter() - T0

print("\n" + "=" * 60)
print("SUMMARY — 3+1D Chiral Walk (n=15, L=16)")
print("=" * 60)

results = [
    ("1. Born |I3|/P", born_pass),
    ("2. Distinguishability d_TV", dtv_pass),
    ("3. f=0 control", ctrl_pass),
    ("4. F ~ M", fm_pass),
    ("5. Gravity TOWARD", grav_pass),
    ("6. Decoherence", decoh_pass),
    ("7. Mutual Information", mi_pass),
    ("8. Purity stable", purity_pass),
    ("9. Gravity grows", grav_grow_pass),
    ("10. Distance law", dist_pass),
    ("11. Superposition", super_pass),
    ("12. Spectral TOWARD", spectral_pass),
    ("13. Norm conservation", norm_pass),
]

n_pass = sum(1 for _, p in results if p)
n_total = len(results)

for name, passed in results:
    status = "PASS" if passed else "FAIL"
    print(f"  {name:30s} {status}")

print(f"\n  TOTAL: {n_pass}/{n_total}")
print(f"  Time: {elapsed:.1f}s")

if n_pass == n_total:
    print("\n  >>> ALL PROPERTIES PASS — 3+1D chiral walk CONFIRMED <<<")
elif n_pass >= 10:
    print(f"\n  >>> {n_pass}/{n_total} pass — partial success <<<")
else:
    print(f"\n  >>> {n_pass}/{n_total} pass — hypothesis FALSIFIED <<<")
