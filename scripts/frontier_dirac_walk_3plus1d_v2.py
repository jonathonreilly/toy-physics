#!/usr/bin/env python3
"""
4-Component Dirac Walk v2 — Reversed Coupling + Symmetrized Split-Step
=======================================================================
FIXES from v1:
  1. REVERSED gravity coupling: m(r) = m0*(1+f) instead of m0*(1-f).
     Higher mass near source -> slower particle -> probability accumulates
     -> TOWARD gravity (time-dilation mechanism).
  2. SYMMETRIZED split-step: alternate S_z*S_y*S_x*C and S_x*S_y*S_z*C
     per layer to restore cubic symmetry. Bloch analysis uses the
     symmetrized operator U = (S_z*S_y*S_x*C) * (S_x*S_y*S_z*C).
  3. Also test single-step U = S_x*S_y*S_z*C (reversed order) to see
     if the anisotropy is order-dependent.

HYPOTHESIS: Reversed coupling flips gravity AWAY->TOWARD.
  Symmetrized step pushes KG R^2 from 0.91 toward 0.99.

FALSIFICATION: If gravity stays AWAY with reversed coupling, the Dirac
  walk gravity mechanism is fundamentally different from the chiral walk.
"""

import numpy as np
from scipy import stats
import time

# ============================================================================
# Gamma matrices (Dirac representation)
# ============================================================================
gamma0 = np.diag([1, 1, -1, -1]).astype(complex)

gamma1 = np.array([
    [0, 0, 0, 1], [0, 0, 1, 0],
    [0, -1, 0, 0], [-1, 0, 0, 0]
], dtype=complex)

gamma2 = np.array([
    [0, 0, 0, -1j], [0, 0, 1j, 0],
    [0, 1j, 0, 0], [-1j, 0, 0, 0]
], dtype=complex)

gamma3 = np.array([
    [0, 0, 1, 0], [0, 0, 0, -1],
    [-1, 0, 0, 0], [0, 1, 0, 0]
], dtype=complex)


def get_projectors(gamma_product):
    """Get ±1 eigenspace projectors for a Hermitian matrix with eigenvalues ±1."""
    evals, evecs = np.linalg.eigh(gamma_product)
    Pp = sum(np.outer(evecs[:,i], evecs[:,i].conj()) for i in range(4) if evals[i] > 0)
    Pm = sum(np.outer(evecs[:,i], evecs[:,i].conj()) for i in range(4) if evals[i] < 0)
    return Pp, Pm


# Precompute projectors (these are constant)
Px_p, Px_m = get_projectors(gamma0 @ gamma1)
Py_p, Py_m = get_projectors(gamma0 @ gamma2)
Pz_p, Pz_m = get_projectors(gamma0 @ gamma3)


# ============================================================================
# Coin and Shifts
# ============================================================================

def dirac_coin(mass):
    return np.cos(mass) * np.eye(4, dtype=complex) + 1j * np.sin(mass) * gamma0


def coin_step(psi_4d, mass_field, n):
    cm = np.cos(mass_field)
    sm = np.sin(mass_field)
    out = np.zeros_like(psi_4d)
    out[0] = (cm + 1j*sm) * psi_4d[0]
    out[1] = (cm + 1j*sm) * psi_4d[1]
    out[2] = (cm - 1j*sm) * psi_4d[2]
    out[3] = (cm - 1j*sm) * psi_4d[3]
    return out


def shift_dir(psi_4d, n, Pp, Pm, axis):
    """Conditional shift along given axis using projectors."""
    out = np.zeros_like(psi_4d)
    for c in range(4):
        pp = sum(Pp[c,d] * psi_4d[d] for d in range(4))
        pm = sum(Pm[c,d] * psi_4d[d] for d in range(4))
        out[c] += np.roll(pp, -1, axis=axis)
        out[c] += np.roll(pm, +1, axis=axis)
    return out


def step_xyz_c(psi, mass_field, n):
    """U = S_x * S_y * S_z * C(m) — one ordering."""
    psi = coin_step(psi, mass_field, n)
    psi = shift_dir(psi, n, Pz_p, Pz_m, 2)
    psi = shift_dir(psi, n, Py_p, Py_m, 1)
    psi = shift_dir(psi, n, Px_p, Px_m, 0)
    return psi


def step_zyx_c(psi, mass_field, n):
    """U = S_z * S_y * S_x * C(m) — reversed ordering."""
    psi = coin_step(psi, mass_field, n)
    psi = shift_dir(psi, n, Px_p, Px_m, 0)
    psi = shift_dir(psi, n, Py_p, Py_m, 1)
    psi = shift_dir(psi, n, Pz_p, Pz_m, 2)
    return psi


def step_symmetric(psi, mass_field, n, layer_idx):
    """Alternating ordering per layer for symmetrization."""
    if layer_idx % 2 == 0:
        return step_zyx_c(psi, mass_field, n)
    else:
        return step_xyz_c(psi, mass_field, n)


# ============================================================================
# Bloch Analysis
# ============================================================================

def bloch_kg(mass0, n=9, mode="sym"):
    """Bloch KG analysis.
    mode: "zyx" = S_z*S_y*S_x*C, "xyz" = S_x*S_y*S_z*C, "sym" = product of both
    """
    C4 = dirac_coin(mass0)
    ks_raw = 2 * np.pi * np.arange(n) / n

    all_E2, all_k2 = [], []
    axis_data = {'x': ([], []), 'y': ([], []), 'z': ([], [])}

    for mx in range(n):
        kx = ks_raw[mx]
        kx_c = kx if kx <= np.pi else kx - 2*np.pi
        Sx = np.exp(1j*kx)*Px_p + np.exp(-1j*kx)*Px_m
        for my in range(n):
            ky = ks_raw[my]
            ky_c = ky if ky <= np.pi else ky - 2*np.pi
            Sy = np.exp(1j*ky)*Py_p + np.exp(-1j*ky)*Py_m
            for mz in range(n):
                kz = ks_raw[mz]
                kz_c = kz if kz <= np.pi else kz - 2*np.pi
                Sz = np.exp(1j*kz)*Pz_p + np.exp(-1j*kz)*Pz_m

                if mode == "zyx":
                    Uk = Sz @ Sy @ Sx @ C4
                elif mode == "xyz":
                    Uk = Sx @ Sy @ Sz @ C4
                elif mode == "sym":
                    # Two-step product: (S_x*S_y*S_z*C) * (S_z*S_y*S_x*C)
                    U1 = Sz @ Sy @ Sx @ C4
                    U2 = Sx @ Sy @ Sz @ C4
                    Uk = U2 @ U1
                    # Eigenphases of the two-step are 2× the single-step energy
                else:
                    raise ValueError(f"Unknown mode: {mode}")

                eigs_k = np.linalg.eigvals(Uk)
                phases = np.angle(eigs_k)
                if mode == "sym":
                    phases = phases / 2.0  # two steps -> halve the phase

                k2 = kx_c**2 + ky_c**2 + kz_c**2
                for ph in phases:
                    all_E2.append(ph**2)
                    all_k2.append(k2)

                if my == 0 and mz == 0 and mx > 0:
                    for ph in phases:
                        axis_data['x'][0].append(kx_c**2)
                        axis_data['x'][1].append(ph**2)
                if mx == 0 and mz == 0 and my > 0:
                    for ph in phases:
                        axis_data['y'][0].append(ky_c**2)
                        axis_data['y'][1].append(ph**2)
                if mx == 0 and my == 0 and mz > 0:
                    for ph in phases:
                        axis_data['z'][0].append(kz_c**2)
                        axis_data['z'][1].append(ph**2)

    all_E2 = np.array(all_E2)
    all_k2 = np.array(all_k2)

    mask = all_k2 < 1.0
    E2_s, k2_s = all_E2[mask], all_k2[mask]

    if len(E2_s) > 10:
        sl, ic, rv, _, _ = stats.linregress(k2_s, E2_s)
        r2 = rv**2
        m_fit = np.sqrt(abs(ic))
        c2 = sl
    else:
        r2, m_fit, c2 = 0.0, 0.0, 0.0

    axis_slopes = {}
    for ax, (k2a, e2a) in axis_data.items():
        k2a, e2a = np.array(k2a), np.array(e2a)
        m_ax = k2a < 1.0
        if np.sum(m_ax) > 3:
            s, _, _, _, _ = stats.linregress(k2a[m_ax], e2a[m_ax])
            axis_slopes[ax] = s

    return r2, m_fit, c2, axis_slopes


# ============================================================================
# Evolution helpers
# ============================================================================

def min_image_dist(n, mass_pos):
    c = np.arange(n)
    dx = np.abs(c[:, None, None] - mass_pos[0]); dx = np.minimum(dx, n - dx)
    dy = np.abs(c[None, :, None] - mass_pos[1]); dy = np.minimum(dy, n - dy)
    dz = np.abs(c[None, None, :] - mass_pos[2]); dz = np.minimum(dz, n - dz)
    return np.sqrt(dx**2 + dy**2 + dz**2)


def make_mass_field(n, mass0, strength, mass_positions, coupling="reversed"):
    """Build spatially-varying mass field.
    coupling="reversed": m(r) = m0*(1+f) — higher mass near source (time-dilation)
    coupling="standard": m(r) = m0*(1-f) — lower mass near source (original chiral)
    """
    mf = np.full((n, n, n), mass0)
    if mass_positions and strength > 0:
        total_f = np.zeros((n, n, n))
        for mp in mass_positions:
            r = min_image_dist(n, mp)
            total_f += strength / (r + 0.1)
        if coupling == "reversed":
            mf = mass0 * (1.0 + total_f)
        else:
            mf = mass0 * (1.0 - total_f)
    return mf


def evolve(n, n_layers, mass0, strength=0.0, mass_positions=None,
           step_mode="sym", coupling="reversed"):
    psi = np.zeros((4, n, n, n), dtype=np.complex128)
    c_idx = n // 2
    for k in range(4):
        psi[k, c_idx, c_idx, c_idx] = 0.5

    mf = make_mass_field(n, mass0, strength, mass_positions, coupling)

    for layer in range(n_layers):
        if step_mode == "sym":
            psi = step_symmetric(psi, mf, n, layer)
        elif step_mode == "zyx":
            psi = step_zyx_c(psi, mf, n)
        elif step_mode == "xyz":
            psi = step_xyz_c(psi, mf, n)
    return psi


def prob_density(psi):
    return np.sum(np.abs(psi)**2, axis=0)


# ============================================================================
# Closure Card
# ============================================================================

def run_closure_card(mass0, n=15, n_layers=12, step_mode="sym", coupling="reversed"):
    print(f"\n{'='*70}")
    print(f"CLOSURE CARD: Dirac Walk v2 (mass={mass0:.3f}, {step_mode}, {coupling})")
    print(f"  n={n}, N={n_layers}")
    print(f"{'='*70}")

    c = n // 2
    STRENGTH = 5e-4
    score = 0
    barrier_layer = 6
    slit_positions = [c - 2, c, c + 2]

    def evolve_barrier(slits, noise=0.0):
        psi = np.zeros((4, n, n, n), dtype=np.complex128)
        for k in range(4):
            psi[k, c, c, c] = 0.5
        mf = np.full((n, n, n), mass0)
        rng = np.random.RandomState(42) if noise > 0 else None
        for layer in range(n_layers):
            if noise > 0:
                ph = rng.uniform(-noise, noise, (n,n,n))
                pf = np.exp(1j * ph)
                for k in range(4):
                    psi[k] *= pf
            if step_mode == "sym":
                psi = step_symmetric(psi, mf, n, layer)
            elif step_mode == "zyx":
                psi = step_zyx_c(psi, mf, n)
            else:
                psi = step_xyz_c(psi, mf, n)
            if layer == barrier_layer - 1:
                mask = np.zeros((n,n,n), dtype=bool)
                for sy in slits:
                    mask[sy,:,:] = True
                for k in range(4):
                    psi[k] *= mask
        return prob_density(psi)

    # 1. Born
    print("\n  [1] Born |I3|/P...")
    rho_full = evolve_barrier(slit_positions)
    rho_singles = [evolve_barrier([s]) for s in slit_positions]
    P_total = np.sum(rho_full)
    born = np.sum(np.abs(rho_full - sum(rho_singles))) / P_total if P_total > 0 else 0
    p1 = born > 0.01
    print(f"      |I3|/P = {born:.6f}  {'PASS' if p1 else 'FAIL'}")
    if p1: score += 1

    # 2. d_TV
    print("  [2] d_TV...")
    rho_up = evolve_barrier([c-2])
    rho_dn = evolve_barrier([c+2])
    pu = rho_up / np.sum(rho_up) if np.sum(rho_up) > 0 else rho_up
    pd = rho_dn / np.sum(rho_dn) if np.sum(rho_dn) > 0 else rho_dn
    dtv = 0.5 * np.sum(np.abs(pu - pd))
    p2 = dtv > 0.01
    print(f"      d_TV = {dtv:.6f}  {'PASS' if p2 else 'FAIL'}")
    if p2: score += 1

    # 3. f=0 control
    print("  [3] f=0 control...")
    psi0 = evolve(n, n_layers, mass0, 0.0, step_mode=step_mode, coupling=coupling)
    rho0 = prob_density(psi0)
    pz = np.sum(rho0[c, c, c+1:c+4])
    mz = np.sum(rho0[c, c, c-3:c])
    bias = abs(pz - mz) / (pz + mz) if (pz + mz) > 0 else 0
    p3 = bias < 0.01
    print(f"      bias = {bias:.8f}  {'PASS' if p3 else 'FAIL'}")
    if p3: score += 1

    # 4. F~M
    print("  [4] F~M...")
    rho0 = prob_density(evolve(n, n_layers, mass0, 0.0, step_mode=step_mode))
    strengths = [1e-4, 2e-4, 5e-4, 1e-3, 2e-3]
    forces = []
    for s in strengths:
        rho1 = prob_density(evolve(n, n_layers, mass0, s, [(c,c,c+3)],
                                   step_mode=step_mode, coupling=coupling))
        delta = rho1 - rho0
        force = sum(delta[c, c, c+dz] for dz in range(1, 4))
        forces.append(force)
    fa = np.array(forces)
    sa = np.array(strengths)
    co = np.polyfit(sa, fa, 1)
    pred = np.polyval(co, sa)
    ss_r = np.sum((fa - pred)**2)
    ss_t = np.sum((fa - np.mean(fa))**2)
    r2_fm = 1 - ss_r / ss_t if ss_t > 0 else 0
    p4 = r2_fm > 0.9
    print(f"      R^2 = {r2_fm:.6f}, forces = [{', '.join(f'{f:.4e}' for f in forces)}]")
    print(f"      {'PASS' if p4 else 'FAIL'}")
    if p4: score += 1

    # 5. Gravity sign — test both couplings
    print("  [5] Gravity sign...")
    for coup in ["reversed", "standard"]:
        rho0 = prob_density(evolve(n, n_layers, mass0, 0.0, step_mode=step_mode))
        rho1 = prob_density(evolve(n, n_layers, mass0, STRENGTH, [(c,c,c+3)],
                                   step_mode=step_mode, coupling=coup))
        delta = rho1 - rho0
        tw = sum(delta[c, c, c+dz] for dz in range(1, 4))
        aw = sum(delta[c, c, c-dz] for dz in range(1, 4))
        tag = "TOWARD" if tw > aw else "AWAY"
        print(f"      {coup:10s}: toward={tw:+.4e}, away={aw:+.4e} -> {tag}")
    # Use the configured coupling for the score
    rho0 = prob_density(evolve(n, n_layers, mass0, 0.0, step_mode=step_mode))
    rho1 = prob_density(evolve(n, n_layers, mass0, STRENGTH, [(c,c,c+3)],
                               step_mode=step_mode, coupling=coupling))
    delta = rho1 - rho0
    tw = sum(delta[c, c, c+dz] for dz in range(1, 4))
    aw = sum(delta[c, c, c-dz] for dz in range(1, 4))
    is_toward = tw > aw
    p5 = is_toward
    print(f"      Using {coupling}: {'TOWARD' if is_toward else 'AWAY'}  {'PASS' if p5 else 'FAIL'}")
    if p5: score += 1

    # 6. Decoherence
    print("  [6] Decoherence...")
    rho_noisy = evolve_barrier(slit_positions, noise=0.5)
    P_n = np.sum(rho_noisy)
    bn = np.sum(np.abs(rho_noisy - sum(rho_singles))) / P_n if P_n > 0 else 0
    p6 = bn < born
    print(f"      clean={born:.6f}, noisy={bn:.6f}  {'PASS' if p6 else 'FAIL'}")
    if p6: score += 1

    # 7. MI
    print("  [7] MI...")
    psi_g = evolve(n, n_layers, mass0, STRENGTH, [(c,c,c)],
                   step_mode=step_mode, coupling=coupling)
    rho_g = prob_density(psi_g)
    rho_n = rho_g / np.sum(rho_g)
    p_x = np.sum(rho_n, axis=(1,2))
    p_y = np.sum(rho_n, axis=(0,2))
    p_xy = np.sum(rho_n, axis=2)
    mi = 0.0
    for ix in range(n):
        for iy in range(n):
            if p_xy[ix,iy] > 1e-30 and p_x[ix] > 1e-30 and p_y[iy] > 1e-30:
                mi += p_xy[ix,iy] * np.log(p_xy[ix,iy] / (p_x[ix] * p_y[iy]))
    p7 = mi > 0.0
    print(f"      MI = {mi:.6e}  {'PASS' if p7 else 'FAIL'}")
    if p7: score += 1

    # 8. Purity stable
    print("  [8] Purity stable...")
    purities = {}
    for L in [8, 10, 12]:
        psi = evolve(n, L, mass0, STRENGTH, [(c,c,c)],
                     step_mode=step_mode, coupling=coupling)
        rho = prob_density(psi)
        purities[L] = np.sum(rho**2) / np.sum(rho)**2
    vals = list(purities.values())
    cv = np.std(vals) / np.mean(vals) if np.mean(vals) > 0 else 0
    p8 = cv < 0.5
    for ll, pu in purities.items():
        print(f"      L={ll}: purity={pu:.6e}")
    print(f"      CV={cv:.4f}  {'PASS' if p8 else 'FAIL'}")
    if p8: score += 1

    # 9. Gravity grows
    print("  [9] Gravity grows...")
    gf = {}
    for L in [8, 10, 12]:
        r0 = prob_density(evolve(n, L, mass0, 0.0, step_mode=step_mode))
        r1 = prob_density(evolve(n, L, mass0, STRENGTH, [(c,c,c+3)],
                                 step_mode=step_mode, coupling=coupling))
        d = r1 - r0
        gf[L] = sum(d[c, c, c+dz] for dz in range(1, 4))
    vg = [gf[L] for L in [8, 10, 12]]
    mono = all(vg[i] <= vg[i+1] for i in range(len(vg)-1))
    p9 = mono
    for ll, f in gf.items():
        print(f"      L={ll}: force={f:.4e}")
    print(f"      Monotonic: {mono}  {'PASS' if p9 else 'FAIL'}")
    if p9: score += 1

    # 10. Distance law
    print("  [10] Distance law...")
    max_off = min(5, n // 4)
    offsets = list(range(2, max_off + 1))
    fdl = []
    r0 = prob_density(evolve(n, n_layers, mass0, 0.0, step_mode=step_mode))
    for dz in offsets:
        r1 = prob_density(evolve(n, n_layers, mass0, STRENGTH, [(c,c,c+dz)],
                                 step_mode=step_mode, coupling=coupling))
        d = r1 - r0
        fdl.append(sum(d[c, c, c+dd] for dd in range(1, dz+1)))
    fa = np.array(fdl)
    oa = np.array(offsets, dtype=float)
    af = np.abs(fa)
    valid = af > 1e-30
    if np.sum(valid) >= 3:
        lr = np.log(oa[valid])
        lf = np.log(af[valid])
        cf = np.polyfit(lr, lf, 1)
        pf = np.polyval(cf, lr)
        sr = np.sum((lf - pf)**2)
        st = np.sum((lf - np.mean(lf))**2)
        r2_dl = 1 - sr / st if st > 0 else 0
        exp_dl = cf[0]
    else:
        r2_dl, exp_dl = 0.0, 0.0
    p10 = r2_dl > 0.7
    for i, dz in enumerate(offsets):
        tag = "TOWARD" if fdl[i] > 0 else "AWAY"
        print(f"      offset={dz}: force={fdl[i]:.4e} {tag}")
    print(f"      exponent={exp_dl:.3f}, R^2={r2_dl:.4f}  {'PASS' if p10 else 'FAIL'}")
    if p10: score += 1

    print(f"\n  CLOSURE CARD SCORE: {score}/10")
    labels = ["Born","d_TV","f=0","F~M","TOWARD","Decoh","MI","Purity","GravGrow","DistLaw"]
    results = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
    for lab, res in zip(labels, results):
        print(f"    {lab:10s} {'PASS' if res else 'FAIL'}")
    return score, results


# ============================================================================
# AB Test
# ============================================================================

def ab_test(mass0, n=9, n_layers=12, step_mode="sym"):
    print(f"\n{'='*70}")
    print(f"AHARONOV-BOHM TEST ({step_mode})")
    print(f"{'='*70}")

    c_idx = n // 2

    def evolve_ab(A_flux):
        psi = np.zeros((4, n, n, n), dtype=complex)
        for k in range(4):
            psi[k, c_idx, c_idx, c_idx] = 0.5
        mf = np.full((n,n,n), mass0)

        for layer in range(n_layers):
            psi = coin_step(psi, mf, n)
            # x-shift with AB phase on ALL projector components
            out = np.zeros_like(psi)
            for c in range(4):
                pp = sum(Px_p[c,d] * psi[d] for d in range(4))
                pm = sum(Px_m[c,d] * psi[d] for d in range(4))
                out[c] += np.roll(pp, -1, axis=0) * np.exp(1j*A_flux)
                out[c] += np.roll(pm, +1, axis=0) * np.exp(-1j*A_flux)
            psi = out
            # y and z shifts (no AB)
            psi = shift_dir(psi, n, Py_p, Py_m, 1)
            psi = shift_dir(psi, n, Pz_p, Pz_m, 2)

        rho = prob_density(psi)
        det = c_idx + 3
        return np.sum(rho[det,:,:]) if det < n else 0.0

    A_vals = np.linspace(0, 2*np.pi, 13)
    P_vals = []
    for A in A_vals:
        P = evolve_ab(A)
        P_vals.append(P)
        print(f"  A={A:.2f}: P={P:.6f}")

    Pa = np.array(P_vals)
    V = (np.max(Pa) - np.min(Pa)) / (np.max(Pa) + np.min(Pa)) if np.max(Pa) > 0 else 0
    print(f"\n  AB visibility V = {V:.4f}")
    print(f"  {'PASS' if V > 0.5 else 'FAIL'}")
    return V


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    t_start = time.time()

    print("=" * 70)
    print("4-COMPONENT DIRAC WALK v2 — REVERSED COUPLING + SYMMETRIZED STEP")
    print("=" * 70)
    print("FIX 1: m(r) = m0*(1+f) — higher mass near source -> TOWARD gravity")
    print("FIX 2: Alternating split-step ordering for cubic symmetry")
    print()

    mass0 = 0.1  # best from v1

    # ── Bloch KG for all three orderings ──────────────────────────────
    print("--- Bloch KG Analysis ---")
    for mode in ["zyx", "xyz", "sym"]:
        r2, m, c2, ax = bloch_kg(mass0, n=9, mode=mode)
        slopes = list(ax.values())
        iso = max(slopes)/min(slopes) if min(slopes) > 0 else float('inf')
        print(f"  {mode:4s}: R^2={r2:.6f}, m={m:.4f}, c^2={c2:.4f}, "
              f"slopes=[{', '.join(f'{s:.3f}' for s in slopes)}], iso={iso:.3f}")

    # ── Mass sweep on symmetric mode ──────────────────────────────────
    print("\n--- Mass sweep (symmetric mode) ---")
    best_r2, best_m = 0.0, 0.1
    for mass in np.linspace(0.02, 0.5, 15):
        r2, m_fit, c2, _ = bloch_kg(mass, n=9, mode="sym")
        if r2 > best_r2:
            best_r2, best_m = r2, mass
        print(f"  mass={mass:.3f}: R^2={r2:.6f}")
    print(f"\n  Best: R^2={best_r2:.6f} at mass={best_m:.3f}")

    # ── Quick gravity direction test ──────────────────────────────────
    print("\n--- Gravity direction quick test (n=13, N=10) ---")
    n_test, L_test = 13, 10
    c_test = n_test // 2
    for coup in ["reversed", "standard"]:
        for smode in ["sym", "zyx"]:
            r0 = prob_density(evolve(n_test, L_test, best_m, 0.0, step_mode=smode))
            r1 = prob_density(evolve(n_test, L_test, best_m, 5e-4, [(c_test,c_test,c_test+3)],
                                     step_mode=smode, coupling=coup))
            d = r1 - r0
            tw = sum(d[c_test, c_test, c_test+dz] for dz in range(1, 4))
            aw = sum(d[c_test, c_test, c_test-dz] for dz in range(1, 4))
            tag = "TOWARD" if tw > aw else "AWAY"
            print(f"  {coup:10s} {smode:4s}: toward={tw:+.4e}, away={aw:+.4e} -> {tag}")

    # ── Full closure card with best config ────────────────────────────
    closure_score, _ = run_closure_card(best_m, n=13, n_layers=10,
                                        step_mode="sym", coupling="reversed")

    # ── AB test ───────────────────────────────────────────────────────
    ab_v = ab_test(best_m, n=9, n_layers=10, step_mode="sym")

    # ── VERDICT ───────────────────────────────────────────────────────
    elapsed = time.time() - t_start
    print(f"\n{'='*70}")
    print("FINAL VERDICT")
    print(f"{'='*70}")
    print(f"  Best KG R^2 (sym):  {best_r2:.6f} at mass={best_m:.3f}")
    print(f"  Closure card:       {closure_score}/10")
    print(f"  AB visibility:      {ab_v:.4f}")
    print(f"  KG target R^2>0.99: {'PASS' if best_r2 > 0.99 else 'FAIL'}")
    print(f"  Total time: {elapsed:.1f}s")
