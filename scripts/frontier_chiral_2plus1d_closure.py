#!/usr/bin/env python3
"""
2+1D Chiral Walk — Full 10-Property Closure Card

Architecture: 4-component state on (y,z) grid.
  Components: psi_{+y}, psi_{-y}, psi_{+z}, psi_{-z}
  Per layer: (1) Coin — symmetric unitary on y-pair and z-pair,
             (2) Shift in each direction.
  Lorentzian theta coupling for gravity.

Coin matrix (symmetric, unitary, zero-drift):
  C(theta) = [[cos(theta), i*sin(theta)],
              [i*sin(theta), cos(theta)]]
"""

import numpy as np
from scipy import stats

# ─── Global parameters ───────────────────────────────────────────────
N_YZ = 21
N_LAYERS = 20
THETA0 = np.pi / 4   # Hadamard-like angle for maximal spread
STRENGTH = 5e-4
CENTER_Y, CENTER_Z = 10, 10
MASS_Y, MASS_Z = 10, 14  # offset 4 in z


# ─── Helpers ─────────────────────────────────────────────────────────

def make_state(n_yz=N_YZ):
    """4 x n_yz x n_yz complex array, zero-initialized."""
    return np.zeros((4, n_yz, n_yz), dtype=complex)


def init_source(state, y, z):
    """
    Balanced source: equal amplitude on all 4 components at (y,z).
    This ensures no inherent directional bias.
    """
    state[0, y, z] = 0.5
    state[1, y, z] = 0.5
    state[2, y, z] = 0.5
    state[3, y, z] = 0.5


def coin_layer(state, theta_field):
    """
    Apply symmetric unitary coin at every site.
    C(theta) = [[cos(theta), i*sin(theta)],
                [i*sin(theta), cos(theta)]]
    """
    c = np.cos(theta_field)
    s = np.sin(theta_field)
    isj = 1j * s
    new0 = c * state[0] + isj * state[1]
    new1 = isj * state[0] + c * state[1]
    new2 = c * state[2] + isj * state[3]
    new3 = isj * state[2] + c * state[3]
    state[0] = new0
    state[1] = new1
    state[2] = new2
    state[3] = new3


def shift_layer(state):
    """
    Shift each chirality one step in its direction (periodic boundary).
    comp 0 (+y): shift y+1, comp 1 (-y): shift y-1
    comp 2 (+z): shift z+1, comp 3 (-z): shift z-1
    """
    state[0] = np.roll(state[0], +1, axis=0)
    state[1] = np.roll(state[1], -1, axis=0)
    state[2] = np.roll(state[2], +1, axis=1)
    state[3] = np.roll(state[3], -1, axis=1)


def theta_field_arr(strength, mass_y, mass_z, n_yz=N_YZ, center_y=None, center_z=None):
    """Lorentzian theta: theta0 * (1 - strength/(r+0.1))."""
    if center_y is None:
        center_y = n_yz // 2
    if center_z is None:
        center_z = n_yz // 2
    yy, zz = np.meshgrid(np.arange(n_yz), np.arange(n_yz), indexing='ij')
    r = np.sqrt((yy - mass_y)**2 + (zz - mass_z)**2)
    f = strength / (r + 0.1)
    return THETA0 * (1.0 - f)


def propagate(n_layers, strength=0.0, mass_y=MASS_Y, mass_z=MASS_Z,
              barrier_layer=None, slit_positions=None,
              source_y=CENTER_Y, source_z=CENTER_Z, n_yz=N_YZ):
    """
    Propagate state through n_layers.
    barrier_layer: if set, apply absorption barrier at that layer.
    slit_positions: list of z-values that are open (all others blocked at barrier).
    """
    center_y = n_yz // 2
    center_z = n_yz // 2
    state = make_state(n_yz)
    # Adjust source and mass positions for different grid sizes
    sy = source_y - CENTER_Y + center_y
    sz = source_z - CENTER_Z + center_z
    my = mass_y - CENTER_Y + center_y
    mz = mass_z - CENTER_Z + center_z
    init_source(state, sy, sz)
    tf = theta_field_arr(strength, my, mz, n_yz, center_y, center_z)

    for layer in range(n_layers):
        coin_layer(state, tf)
        shift_layer(state)
        if barrier_layer is not None and layer == barrier_layer:
            if slit_positions is not None:
                # Adjust slit positions for different grid sizes
                mask = np.ones((n_yz, n_yz), dtype=bool)
                for sz_slit in slit_positions:
                    adj_z = sz_slit - CENTER_Z + center_z
                    if 0 <= adj_z < n_yz:
                        mask[:, adj_z] = False
                state[:, mask] = 0.0

    return state, center_z


def prob_z(state):
    """Marginal probability distribution over z (sum over y and components)."""
    p = np.sum(np.abs(state)**2, axis=(0, 1))
    total = p.sum()
    if total > 0:
        p /= total
    return p


def center_of_mass_z(state, center_z=None):
    """Probability-weighted center of mass in z."""
    n_yz = state.shape[2]
    if center_z is None:
        center_z = n_yz // 2
    p = prob_z(state)
    zz = np.arange(n_yz)
    return np.sum(p * zz)


def total_prob(state):
    """Total probability (norm squared)."""
    return np.sum(np.abs(state)**2)


# ─── PROPERTY TESTS ──────────────────────────────────────────────────

def test_born(verbose=True):
    """P1: Born rule — 3-slit interference |I3|/P."""
    # Use barrier at layer 5 (even) so z=8,10,12 have support
    barrier = 5
    slits_all = [8, 10, 12]

    def run_slits(slit_list):
        st, _ = propagate(N_LAYERS, strength=0.0,
                          barrier_layer=barrier, slit_positions=slit_list)
        return np.sum(np.abs(st)**2, axis=(0, 1))

    p_abc = run_slits([8, 10, 12])
    p_ab = run_slits([8, 10])
    p_ac = run_slits([8, 12])
    p_bc = run_slits([10, 12])
    p_a = run_slits([8])
    p_b = run_slits([10])
    p_c = run_slits([12])

    I3 = p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c
    ratio = np.sum(np.abs(I3)) / max(np.sum(p_abc), 1e-30)
    passed = ratio < 0.01
    if verbose:
        print(f"  P1  Born |I3|/P = {ratio:.6f}  {'PASS' if passed else 'FAIL'}")
        print(f"       P(ABC)={np.sum(p_abc):.6f}, P(A)={np.sum(p_a):.6f}, "
              f"P(B)={np.sum(p_b):.6f}, P(C)={np.sum(p_c):.6f}")
    return passed, ratio


def test_dtv(verbose=True):
    """P2: Distinguishability d_TV between upper/lower slit."""
    barrier = 5

    st_upper, _ = propagate(N_LAYERS, strength=0.0,
                            barrier_layer=barrier, slit_positions=[12])
    st_lower, _ = propagate(N_LAYERS, strength=0.0,
                            barrier_layer=barrier, slit_positions=[8])

    p_u = prob_z(st_upper)
    p_l = prob_z(st_lower)
    dtv = 0.5 * np.sum(np.abs(p_u - p_l))
    passed = dtv > 0.1
    if verbose:
        print(f"  P2  d_TV = {dtv:.4f}  {'PASS' if passed else 'FAIL'}")
    return passed, dtv


def test_f0_control(verbose=True):
    """P3: f=0 control — no field, gravity must vanish."""
    st, cz = propagate(N_LAYERS, strength=0.0)
    com = center_of_mass_z(st)
    delta = com - cz
    passed = abs(delta) < 0.05
    if verbose:
        print(f"  P3  f=0 delta = {delta:.6f}  {'PASS' if passed else 'FAIL'}")
        print(f"       COM_z = {com:.6f}, norm = {total_prob(st):.6f}")
    return passed, delta


def test_f_prop_m(verbose=True):
    """P4: F proportional to M — sweep strength, fit alpha."""
    st_base, cz = propagate(N_LAYERS, strength=0.0)
    com_base = center_of_mass_z(st_base)

    strengths = np.array([1e-4, 3e-4, 5e-4, 8e-4, 1e-3, 2e-3])
    deltas = []
    for s in strengths:
        st, _ = propagate(N_LAYERS, strength=s, mass_y=MASS_Y, mass_z=MASS_Z)
        com = center_of_mass_z(st)
        deltas.append(com - com_base)
    deltas = np.array(deltas)

    if verbose:
        for s, d in zip(strengths, deltas):
            print(f"       strength={s:.1e}: delta={d:.6f}")

    valid = (np.abs(deltas) > 1e-12) & (strengths > 0)
    if valid.sum() >= 3:
        slope, intercept, r, p, se = stats.linregress(
            np.log(strengths[valid]), np.log(np.abs(deltas[valid])))
        passed = abs(slope - 1.0) < 0.35
    else:
        slope, r = 0.0, 0.0
        passed = False
    if verbose:
        print(f"  P4  F~M alpha = {slope:.3f} (r={r:.3f})  {'PASS' if passed else 'FAIL'}")
    return passed, slope


def test_gravity_sign(verbose=True):
    """P5: Gravity sign — mass at z=14, COM should shift TOWARD (z>center)."""
    st_base, cz = propagate(N_LAYERS, strength=0.0)
    com_base = center_of_mass_z(st_base)

    st, _ = propagate(N_LAYERS, strength=STRENGTH, mass_y=MASS_Y, mass_z=MASS_Z)
    com = center_of_mass_z(st)
    delta = com - com_base
    toward = delta > 0  # mass is at z=14 > center, so toward means delta > 0
    passed = toward and abs(delta) > 1e-6
    if verbose:
        direction = "TOWARD" if toward else "AWAY"
        print(f"  P5  Gravity sign: delta={delta:.6f} ({direction})  {'PASS' if passed else 'FAIL'}")
        print(f"       COM_base={com_base:.6f}, COM_field={com:.6f}")
    return passed, delta


def test_decoherence(verbose=True):
    """P6: Decoherence — CL bath on binned y-amplitudes."""
    st, _ = propagate(N_LAYERS, strength=STRENGTH)

    N_BINS = 7
    bin_edges = np.linspace(0, N_YZ, N_BINS + 1, dtype=int)

    # Coherent: compute amplitude per bin, then square
    amp_bins_coh = np.zeros(N_BINS, dtype=complex)
    for b in range(N_BINS):
        y0, y1 = bin_edges[b], bin_edges[b+1]
        amp_bins_coh[b] = np.sum(st[:, y0:y1, :])
    p_coh = np.abs(amp_bins_coh)**2
    p_coh_sum = p_coh.sum()
    if p_coh_sum > 0:
        p_coh /= p_coh_sum

    # Decohered: square per site, then sum into bins
    prob_sites = np.sum(np.abs(st)**2, axis=0)
    p_dec = np.zeros(N_BINS)
    for b in range(N_BINS):
        y0, y1 = bin_edges[b], bin_edges[b+1]
        p_dec[b] = np.sum(prob_sites[y0:y1, :])
    p_dec_sum = p_dec.sum()
    if p_dec_sum > 0:
        p_dec /= p_dec_sum

    cl = 1.0 - 0.5 * np.sum(np.abs(p_coh - p_dec))
    passed = cl > 0.8
    if verbose:
        print(f"  P6  Decoherence CL = {cl:.4f}  {'PASS' if passed else 'FAIL'}")
    return passed, cl


def test_mi(verbose=True):
    """P7: Mutual information from slit distributions."""
    barrier = 5
    slits = [8, 10, 12]

    probs_per_slit = []
    for s in slits:
        st, _ = propagate(N_LAYERS, strength=0.0,
                          barrier_layer=barrier, slit_positions=[s])
        pz = np.sum(np.abs(st)**2, axis=(0, 1))
        probs_per_slit.append(pz)

    joint = np.array(probs_per_slit)
    joint_sum = joint.sum()
    if joint_sum > 0:
        joint /= joint_sum

    p_slit = joint.sum(axis=1)
    p_z = joint.sum(axis=0)

    mi = 0.0
    for i in range(len(slits)):
        for j in range(N_YZ):
            if joint[i, j] > 1e-30 and p_slit[i] > 1e-30 and p_z[j] > 1e-30:
                mi += joint[i, j] * np.log(joint[i, j] / (p_slit[i] * p_z[j]))

    passed = mi > 0.01
    if verbose:
        print(f"  P7  MI = {mi:.4f}  {'PASS' if passed else 'FAIL'}")
        print(f"       P(slit) = [{p_slit[0]:.4f}, {p_slit[1]:.4f}, {p_slit[2]:.4f}]")
    return passed, mi


def test_purity_stable(verbose=True):
    """P8: Purity stable across multiple L."""
    Ls = [12, 16, 20, 24]
    purities = []
    for L in Ls:
        st, _ = propagate(L, strength=STRENGTH)
        p = prob_z(st)
        pur = np.sum(p**2)
        purities.append(pur)

    purities = np.array(purities)
    spread = purities.max() - purities.min()
    mean_pur = purities.mean()
    cv = spread / max(mean_pur, 1e-30)
    passed = cv < 0.5
    if verbose:
        print(f"  P8  Purity: mean={mean_pur:.4f}, spread={spread:.4f}, CV={cv:.4f}  "
              f"{'PASS' if passed else 'FAIL'}")
        for L, pu in zip(Ls, purities):
            print(f"        L={L}: purity={pu:.6f}")
    return passed, cv


def test_gravity_grows(verbose=True):
    """P9: Gravity grows with L — |delta(L)| should increase.
    Use larger grids for larger L to avoid periodic wrap-around artifacts.
    """
    Ls = [8, 12, 16, 20]
    deltas = []
    for L in Ls:
        # Grid size scales with L to avoid boundary effects
        n_yz = max(N_YZ, 2 * L + 5)
        if n_yz % 2 == 0:
            n_yz += 1  # keep odd for center

        st_base, cz = propagate(L, strength=0.0, n_yz=n_yz)
        com_base = center_of_mass_z(st_base)
        st, _ = propagate(L, strength=STRENGTH, n_yz=n_yz)
        com = center_of_mass_z(st)
        deltas.append(com - com_base)

    deltas = np.array(deltas)
    abs_deltas = np.abs(deltas)
    increases = sum(abs_deltas[i+1] > abs_deltas[i] for i in range(len(deltas)-1))
    passed = increases >= 2
    if verbose:
        print(f"  P9  Gravity grows: {increases}/3 increases  {'PASS' if passed else 'FAIL'}")
        for L, d in zip(Ls, deltas):
            print(f"        L={L}: delta={d:.6f}, |delta|={abs(d):.6f}")
    return passed, increases


def test_distance_law(verbose=True):
    """P10: Distance law — |delta| vs z_mass distance."""
    st_base, cz = propagate(N_LAYERS, strength=0.0)
    com_base = center_of_mass_z(st_base)

    z_masses = [12, 13, 14, 15, 16, 17]
    deltas = []
    distances = []
    for zm in z_masses:
        st, _ = propagate(N_LAYERS, strength=STRENGTH, mass_y=MASS_Y, mass_z=zm)
        com = center_of_mass_z(st)
        deltas.append(abs(com - com_base))
        distances.append(abs(zm - CENTER_Z))

    deltas = np.array(deltas)
    distances = np.array(distances)

    valid = deltas > 1e-12
    if valid.sum() >= 3:
        corr, p_val = stats.spearmanr(distances[valid], deltas[valid])
        passed = corr < -0.3
    else:
        corr, p_val = 0.0, 1.0
        passed = False
    if verbose:
        print(f"  P10 Distance law: Spearman r={corr:.3f} (p={p_val:.4f})  "
              f"{'PASS' if passed else 'FAIL'}")
        for d, dl in zip(distances, deltas):
            print(f"        dist={d}: |delta|={dl:.6f}")
    return passed, corr


# ─── MAIN ────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  2+1D CHIRAL WALK — 10-PROPERTY CLOSURE CARD")
    print(f"  Grid: {N_YZ}x{N_YZ}, layers: {N_LAYERS}, theta0: {THETA0:.4f}")
    print(f"  Source: balanced at ({CENTER_Y},{CENTER_Z})")
    print(f"  Mass: ({MASS_Y},{MASS_Z}), strength: {STRENGTH}")
    print(f"  Coin: C(t) = [[cos(t), i*sin(t)], [i*sin(t), cos(t)]]")
    print("=" * 65)

    results = {}

    tests = [
        ("Born |I3|/P", test_born),
        ("d_TV", test_dtv),
        ("f=0 control", test_f0_control),
        ("F~M", test_f_prop_m),
        ("Gravity sign", test_gravity_sign),
        ("Decoherence", test_decoherence),
        ("MI", test_mi),
        ("Purity stable", test_purity_stable),
        ("Gravity grows", test_gravity_grows),
        ("Distance law", test_distance_law),
    ]

    for name, fn in tests:
        print(f"\n--- {name} ---")
        passed, val = fn()
        results[name] = (passed, val)

    # Summary
    print("\n" + "=" * 65)
    print("  SUMMARY")
    print("=" * 65)
    n_pass = sum(1 for v in results.values() if v[0])
    for name, (passed, val) in results.items():
        tag = "PASS" if passed else "FAIL"
        if isinstance(val, (float, np.floating)):
            print(f"  [{tag}] {name}: {val:.6f}")
        else:
            print(f"  [{tag}] {name}: {val}")
    print(f"\n  TOTAL: {n_pass}/10 properties passed")
    print(f"  HYPOTHESIS: {'SUPPORTED' if n_pass >= 9 else 'FALSIFIED'}")
    print("=" * 65)


if __name__ == "__main__":
    main()
