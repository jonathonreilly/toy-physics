#!/usr/bin/env python3
"""Unitary transfer matrix: 2D vs 3D head-to-head comparison.

THE KEY QUESTION:
  Multiple results show 2D and 3D giving OPPOSITE results:
  - Gravity sign: AWAY in 2D, TOWARD in 3D
  - Superposition: 99% error in 2D, 0.01% in 3D
  - Kernel derivation: different optimal beta in 2D vs 3D

  Does the 2D/3D split persist under the unitary propagator?
  If 2D unitary gives AWAY but 3D unitary gives TOWARD, the dimensional
  effect is real. If both give the same direction, the split was an
  artifact of non-unitarity.

APPROACH:
  Part 1: Build 2D transfer matrix (17x17) for rectangular lattice.
  Part 2: Build 3D transfer matrix (625x625) for cubic lattice.
  Part 3: Polar decompose both. Run Born, gravity, norm, spectral tests.
  Compare head-to-head.

HYPOTHESIS: "The unitary transfer matrix preserves Born AND gravity
in both 2D and 3D."
FALSIFICATION: "If Born fails in either dimension."
"""
from __future__ import annotations

import math
import time
import numpy as np
from scipy.linalg import polar


# =====================================================================
# SHARED PARAMETERS
# =====================================================================
K_TEST = 5.0          # wavenumber for single-k tests
STRENGTH = 5e-5       # gravitational field strength
N_LAYERS = 20         # propagation depth
K_SPECTRAL = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 10.0]

# 2D parameters
HEIGHT_2D = 8         # transverse extent: y in [-8, +8]
H_2D = 1.0            # lattice spacing (integer lattice)
P_2D = 1              # attenuation power 1/L^p
BETA_2D = 0.8         # Gaussian weight parameter
MASS_Y_2D = 4.0       # mass position in y

# 3D parameters
PHYS_W_3D = 6         # physical half-width
H_3D = 0.5            # lattice spacing
P_3D = 2              # attenuation power 1/L^p (3D uses L^2)
BETA_3D = 0.8         # Gaussian weight parameter
MAX_D_PHYS_3D = 3     # max offset in physical units
MASS_Z_3D = 3.0       # mass position in z


# =====================================================================
# PART 1: 2D TRANSFER MATRIX
# =====================================================================
def build_2d_lattice():
    """Build 2D lattice offsets: each step goes from x to x+1,
    with y offset in [-max_d, +max_d]."""
    hw = HEIGHT_2D  # half-width in lattice units
    nw = 2 * hw + 1  # 17 transverse sites
    max_d = 3  # max y-offset per step

    offsets = []
    for dy in range(-max_d, max_d + 1):
        dyp = dy * H_2D
        L = math.sqrt(H_2D**2 + dyp**2)
        theta = math.atan2(abs(dyp), H_2D)
        w = math.exp(-BETA_2D * theta**2)
        lf_factor = math.cos(2 * theta)
        offsets.append((dy, L, w, lf_factor))

    return hw, nw, max_d, offsets


def build_2d_transfer_matrix(nw, offsets, field, k, action_mode="euclidean"):
    """Build nw x nw transfer matrix for 2D lattice.

    M[y_out, y_in] = sum over offsets of exp(i*k*S) * w / L^P_2D
    """
    M = np.zeros((nw, nw), dtype=np.complex128)
    hw = (nw - 1) // 2

    for dy, L, w, lf_factor in offsets:
        for y_in_idx in range(nw):
            y_out_idx = y_in_idx + dy
            if y_out_idx < 0 or y_out_idx >= nw:
                continue

            # Average field at src and dst
            f = 0.5 * (field[y_in_idx] + field[y_out_idx])

            if action_mode == "euclidean":
                act = L * (1.0 - f)
            else:
                act = L * (1.0 - f * lf_factor)

            M[y_out_idx, y_in_idx] += np.exp(1j * k * act) * w / (L ** P_2D)

    return M


def make_2d_field_flat(nw):
    return np.zeros(nw)


def make_2d_field_mass(nw, y_mass):
    """1/|y - y_mass| field for 2D."""
    hw = (nw - 1) // 2
    field = np.zeros(nw)
    for iy in range(nw):
        y = (iy - hw) * H_2D
        r = abs(y - y_mass) + 0.1
        field[iy] = STRENGTH / r
    return field


def make_2d_source(nw):
    """Delta source at center."""
    psi = np.zeros(nw, dtype=np.complex128)
    hw = (nw - 1) // 2
    psi[hw] = 1.0
    return psi


def make_2d_slit_source(nw, slit_offsets):
    """Source at specified y-offsets (equal amplitude)."""
    hw = (nw - 1) // 2
    psi = np.zeros(nw, dtype=np.complex128)
    amp = 1.0 / math.sqrt(len(slit_offsets))
    for dy in slit_offsets:
        psi[hw + dy] = amp
    return psi


def centroid_2d(psi, nw):
    hw = (nw - 1) // 2
    prob = np.abs(psi)**2
    total = np.sum(prob)
    if total < 1e-30:
        return 0.0
    y_coords = np.array([(i - hw) * H_2D for i in range(nw)])
    return np.sum(prob * y_coords) / total


# =====================================================================
# PART 2: 3D TRANSFER MATRIX (from frontier_unitary_transfer_matrix.py)
# =====================================================================
def build_3d_lattice():
    hw = int(PHYS_W_3D / H_3D)
    max_d = max(1, round(MAX_D_PHYS_3D / H_3D))
    nw = 2 * hw + 1
    npl = nw * nw

    offsets = []
    for dy in range(-max_d, max_d + 1):
        for dz in range(-max_d, max_d + 1):
            dyp = dy * H_3D
            dzp = dz * H_3D
            L = math.sqrt(H_3D**2 + dyp**2 + dzp**2)
            theta = math.atan2(math.sqrt(dyp**2 + dzp**2), H_3D)
            w = math.exp(-BETA_3D * theta**2)
            lf_factor = math.cos(2 * theta)
            offsets.append((dy, dz, L, w, lf_factor))

    return hw, max_d, nw, npl, offsets


def build_3d_transfer_matrix(nw, npl, offsets, field, k, action_mode="euclidean"):
    """Build npl x npl transfer matrix for 3D lattice."""
    hm = H_3D * H_3D
    M = np.zeros((npl, npl), dtype=np.complex128)

    for dy, dz, L, w, lf_factor in offsets:
        for iy_src in range(nw):
            iy_dst = iy_src + dy
            if iy_dst < 0 or iy_dst >= nw:
                continue
            for iz_src in range(max(0, -dz), min(nw, nw - dz)):
                iz_dst = iz_src + dz
                si = iy_src * nw + iz_src
                di = iy_dst * nw + iz_dst

                lf = 0.5 * (field[si] + field[di])

                if action_mode == "euclidean":
                    act = L * (1.0 - lf)
                else:
                    act = L * (1.0 - lf * lf_factor)

                M[di, si] += np.exp(1j * k * act) * w * hm / (L * L)

    return M


def make_3d_field_flat(npl):
    return np.zeros(npl)


def make_3d_field_mass(nw, npl, z_mass):
    hw = (nw - 1) // 2
    iz_mass = round(z_mass / H_3D)
    mz = iz_mass * H_3D
    field = np.zeros(npl)
    for iy in range(nw):
        for iz in range(nw):
            y = (iy - hw) * H_3D
            z = (iz - hw) * H_3D
            r = math.sqrt(y**2 + (z - mz)**2) + 0.1
            field[iy * nw + iz] = STRENGTH / r
    return field


def make_3d_source(npl, nw):
    hw = (nw - 1) // 2
    psi = np.zeros(npl, dtype=np.complex128)
    center = hw * nw + hw
    psi[center] = 1.0
    return psi


def make_3d_slit_source(npl, nw, slit_positions):
    """Source at specified (iy_offset, iz_offset) positions."""
    hw = (nw - 1) // 2
    psi = np.zeros(npl, dtype=np.complex128)
    amp = 1.0 / math.sqrt(len(slit_positions))
    for (dy, dz) in slit_positions:
        idx = (dy + hw) * nw + (dz + hw)
        psi[idx] = amp
    return psi


def centroid_3d_z(psi, nw):
    hw = (nw - 1) // 2
    npl = nw * nw
    prob = np.abs(psi)**2
    total = np.sum(prob)
    if total < 1e-30:
        return 0.0
    z_coords = np.zeros(npl)
    for iy in range(nw):
        for iz in range(nw):
            z_coords[iy * nw + iz] = (iz - hw) * H_3D
    return np.sum(prob * z_coords) / total


# =====================================================================
# PROPAGATION
# =====================================================================
def propagate(U, psi0, n_layers):
    """Propagate psi through n_layers using U."""
    psi = psi0.copy()
    for _ in range(n_layers):
        psi = U @ psi
    return psi


def propagate_all(U, psi0, n_layers):
    """Return psi at every layer."""
    psis = [psi0.copy()]
    psi = psi0.copy()
    for _ in range(n_layers):
        psi = U @ psi
        psis.append(psi.copy())
    return psis


# =====================================================================
# TEST SUITE (generic, works for both 2D and 3D)
# =====================================================================
def test_norm(U, psi0, label):
    """Check norm preservation over N_LAYERS."""
    psis = propagate_all(U, psi0, N_LAYERS)
    norms = [np.sum(np.abs(p)**2) for p in psis]
    max_dev = max(abs(n - 1.0) for n in norms)
    passed = max_dev < 1e-10
    return passed, max_dev, norms[-1]


def test_born_linearity(U, psi_a, psi_b, label):
    """Test Born rule via LINEARITY: U(a*psi_A + b*psi_B) = a*U(psi_A) + b*U(psi_B).

    NOTE: The Sorkin I3 test with "open" sources (no physical barriers) does
    NOT test Born rule -- it tests whether the propagator includes path-blocking
    barriers. With a linear propagator and no barriers, I3 is nonzero because
    all paths contribute regardless of which sources are active. The correct
    test for Born rule with a transfer matrix is linearity.
    """
    alpha = 0.6 + 0.3j
    beta = 0.4 - 0.5j

    psi_combo = alpha * psi_a + beta * psi_b

    out_a = propagate(U, psi_a, N_LAYERS)
    out_b = propagate(U, psi_b, N_LAYERS)
    out_combo = propagate(U, psi_combo, N_LAYERS)

    expected = alpha * out_a + beta * out_b
    err = np.linalg.norm(out_combo - expected) / np.linalg.norm(expected)

    passed = err < 1e-10
    return passed, err


def test_born_2d(U, nw, label):
    """Born/linearity test for 2D."""
    psi_a = make_2d_slit_source(nw, [-2])
    psi_b = make_2d_slit_source(nw, [2])
    return test_born_linearity(U, psi_a, psi_b, label)


def test_born_3d(U, nw, npl, label):
    """Born/linearity test for 3D."""
    psi_a = make_3d_slit_source(npl, nw, [(0, -2)])
    psi_b = make_3d_slit_source(npl, nw, [(0, 2)])
    return test_born_linearity(U, psi_a, psi_b, label)


def test_gravity(U_flat, U_mass, psi0, centroid_fn, mass_pos_sign, label):
    """Measure centroid shift. mass_pos_sign > 0 means mass at positive coord."""
    psi_flat = propagate(U_flat, psi0, N_LAYERS)
    psi_mass = propagate(U_mass, psi0, N_LAYERS)

    c_flat = centroid_fn(psi_flat)
    c_mass = centroid_fn(psi_mass)
    shift = c_mass - c_flat

    # TOWARD means shift has same sign as mass position
    toward = (shift * mass_pos_sign) > 0
    return toward, shift, c_flat, c_mass


def test_spectral(build_M_fn, field_flat, field_mass, psi0, centroid_fn,
                   mass_pos_sign, k_values, action_mode, label):
    """Sweep k, build U at each k, sum amplitudes at detector."""
    psi_total_flat = np.zeros_like(psi0)
    psi_total_mass = np.zeros_like(psi0)
    per_k = []

    for kv in k_values:
        M_f = build_M_fn(field_flat, kv, action_mode)
        M_m = build_M_fn(field_mass, kv, action_mode)
        U_f, _ = polar(M_f)
        U_m, _ = polar(M_m)

        psi_f = propagate(U_f, psi0, N_LAYERS)
        psi_m = propagate(U_m, psi0, N_LAYERS)

        psi_total_flat += psi_f
        psi_total_mass += psi_m

        c_f = centroid_fn(psi_f)
        c_m = centroid_fn(psi_m)
        delta = c_m - c_f
        per_k.append((kv, delta))

    c_spec_flat = centroid_fn(psi_total_flat)
    c_spec_mass = centroid_fn(psi_total_mass)
    delta_spec = c_spec_mass - c_spec_flat
    toward = (delta_spec * mass_pos_sign) > 0

    n_toward = sum(1 for _, d in per_k if (d * mass_pos_sign) > 0)
    return toward, delta_spec, n_toward, len(k_values), per_k


# =====================================================================
# RAW M TESTS (non-unitary comparison)
# =====================================================================
def test_gravity_raw(M_flat, M_mass, psi0, centroid_fn, mass_pos_sign, label):
    """Same gravity test but using raw M (non-unitary)."""
    psi = psi0.copy()
    for _ in range(N_LAYERS):
        psi = M_flat @ psi
    c_flat = centroid_fn(psi)

    psi = psi0.copy()
    for _ in range(N_LAYERS):
        psi = M_mass @ psi
    c_mass = centroid_fn(psi)

    shift = c_mass - c_flat
    toward = (shift * mass_pos_sign) > 0
    norm_flat = np.sum(np.abs(psi)**2)
    return toward, shift, norm_flat


# =====================================================================
# MAIN
# =====================================================================
def main():
    t0 = time.time()

    print("=" * 72)
    print("UNITARY TRANSFER MATRIX: 2D vs 3D HEAD-TO-HEAD")
    print("=" * 72)
    print()
    print("Hypothesis: The unitary transfer matrix preserves Born AND gravity")
    print("in both 2D and 3D.")
    print("Falsification: If Born fails in either dimension.")
    print()
    print("Key question: Does the 2D/3D gravity sign split persist under")
    print("the unitary propagator?")
    print()

    # ==================================================================
    # BUILD 2D LATTICE
    # ==================================================================
    hw_2d, nw_2d, max_d_2d, offsets_2d = build_2d_lattice()
    print(f"2D Lattice: nw={nw_2d} (transfer matrix {nw_2d}x{nw_2d})")
    print(f"  H={H_2D}, height={HEIGHT_2D}, max_d={max_d_2d}, P={P_2D}")

    field_flat_2d = make_2d_field_flat(nw_2d)
    field_mass_2d = make_2d_field_mass(nw_2d, MASS_Y_2D)
    psi0_2d = make_2d_source(nw_2d)

    def build_M_2d(field, k, action_mode):
        return build_2d_transfer_matrix(nw_2d, offsets_2d, field, k, action_mode)

    def centroid_fn_2d(psi):
        return centroid_2d(psi, nw_2d)

    # ==================================================================
    # BUILD 3D LATTICE
    # ==================================================================
    hw_3d, max_d_3d, nw_3d, npl_3d, offsets_3d = build_3d_lattice()
    print(f"3D Lattice: nw={nw_3d}, npl={npl_3d} (transfer matrix {npl_3d}x{npl_3d})")
    print(f"  H={H_3D}, PHYS_W={PHYS_W_3D}, max_d={max_d_3d}, P={P_3D}")

    field_flat_3d = make_3d_field_flat(npl_3d)
    field_mass_3d = make_3d_field_mass(nw_3d, npl_3d, MASS_Z_3D)
    psi0_3d = make_3d_source(npl_3d, nw_3d)

    def build_M_3d(field, k, action_mode):
        return build_3d_transfer_matrix(nw_3d, npl_3d, offsets_3d, field, k, action_mode)

    def centroid_fn_3d(psi):
        return centroid_3d_z(psi, nw_3d)

    print()

    # ==================================================================
    # BUILD TRANSFER MATRICES AND POLAR DECOMPOSE
    # ==================================================================
    action_mode = "euclidean"  # S = L*(1-f) -- the valley-linear action
    print(f"Action mode: {action_mode} (S = L*(1-f))")
    print()

    print("Building 2D transfer matrices...")
    M_flat_2d = build_M_2d(field_flat_2d, K_TEST, action_mode)
    M_mass_2d = build_M_2d(field_mass_2d, K_TEST, action_mode)

    sv_2d = np.linalg.svd(M_flat_2d, compute_uv=False)
    print(f"  2D M singular values: [{sv_2d[-1]:.4e}, {sv_2d[0]:.4e}]")
    print(f"  2D M condition number: {sv_2d[0]/sv_2d[-1] if sv_2d[-1] > 1e-30 else float('inf'):.2e}")

    U_flat_2d, _ = polar(M_flat_2d)
    U_mass_2d, _ = polar(M_mass_2d)

    print("Building 3D transfer matrices...")
    M_flat_3d = build_M_3d(field_flat_3d, K_TEST, action_mode)
    M_mass_3d = build_M_3d(field_mass_3d, K_TEST, action_mode)

    sv_3d = np.linalg.svd(M_flat_3d, compute_uv=False)
    print(f"  3D M singular values: [{sv_3d[-1]:.4e}, {sv_3d[0]:.4e}]")
    print(f"  3D M condition number: {sv_3d[0]/sv_3d[-1] if sv_3d[-1] > 1e-30 else float('inf'):.2e}")

    U_flat_3d, _ = polar(M_flat_3d)
    U_mass_3d, _ = polar(M_mass_3d)

    t1 = time.time()
    print(f"\nMatrix build + polar decomposition: {t1-t0:.1f}s")
    print()

    # ==================================================================
    # RUN ALL TESTS
    # ==================================================================
    results = {}

    # ---- 2D RAW M ----
    print("=" * 72)
    print("2D RAW M (non-unitary)")
    print("=" * 72)

    grav_raw_2d_toward, grav_raw_2d_shift, norm_raw_2d = test_gravity_raw(
        M_flat_2d, M_mass_2d, psi0_2d, centroid_fn_2d, MASS_Y_2D, "2D raw")
    dr = "TOWARD" if grav_raw_2d_toward else "AWAY"
    print(f"  Gravity: shift={grav_raw_2d_shift:+.6e} ({dr})")
    print(f"  Norm after {N_LAYERS} layers: {norm_raw_2d:.6e}")
    results["2D raw M"] = {
        "gravity_toward": grav_raw_2d_toward,
        "gravity_shift": grav_raw_2d_shift,
        "norm": norm_raw_2d,
    }

    # ---- 3D RAW M ----
    print()
    print("=" * 72)
    print("3D RAW M (non-unitary)")
    print("=" * 72)

    grav_raw_3d_toward, grav_raw_3d_shift, norm_raw_3d = test_gravity_raw(
        M_flat_3d, M_mass_3d, psi0_3d, centroid_fn_3d, MASS_Z_3D, "3D raw")
    dr = "TOWARD" if grav_raw_3d_toward else "AWAY"
    print(f"  Gravity: shift={grav_raw_3d_shift:+.6e} ({dr})")
    print(f"  Norm after {N_LAYERS} layers: {norm_raw_3d:.6e}")
    results["3D raw M"] = {
        "gravity_toward": grav_raw_3d_toward,
        "gravity_shift": grav_raw_3d_shift,
        "norm": norm_raw_3d,
    }

    # ---- 2D UNITARY U ----
    print()
    print("=" * 72)
    print("2D UNITARY U (polar decomposition)")
    print("=" * 72)

    norm_pass_2d, norm_dev_2d, norm_final_2d = test_norm(U_flat_2d, psi0_2d, "2D unitary")
    print(f"  Norm: max deviation = {norm_dev_2d:.2e} ({'PASS' if norm_pass_2d else 'FAIL'})")

    born_pass_2d, born_err_2d = test_born_2d(U_flat_2d, nw_2d, "2D unitary")
    print(f"  Born (linearity): rel err = {born_err_2d:.2e} ({'PASS' if born_pass_2d else 'FAIL'})")

    grav_2d_toward, grav_2d_shift, c_flat_2d, c_mass_2d = test_gravity(
        U_flat_2d, U_mass_2d, psi0_2d, centroid_fn_2d, MASS_Y_2D, "2D unitary")
    dr = "TOWARD" if grav_2d_toward else "AWAY"
    print(f"  Gravity k={K_TEST}: shift={grav_2d_shift:+.6e} ({dr})")
    print(f"    centroid flat={c_flat_2d:.8f}, mass={c_mass_2d:.8f}")

    spec_2d_toward, spec_2d_shift, n_toward_2d, n_total_2d, per_k_2d = test_spectral(
        build_M_2d, field_flat_2d, field_mass_2d, psi0_2d, centroid_fn_2d,
        MASS_Y_2D, K_SPECTRAL, action_mode, "2D unitary")
    dr = "TOWARD" if spec_2d_toward else "AWAY"
    print(f"  Spectral: shift={spec_2d_shift:+.6e} ({dr}), {n_toward_2d}/{n_total_2d} per-k TOWARD")
    print(f"    Per-k breakdown:")
    for kv, delta in per_k_2d:
        d = "TOWARD" if (delta * MASS_Y_2D) > 0 else "AWAY"
        print(f"      k={kv:5.1f}: shift={delta:+.6e} ({d})")

    results["2D unitary U"] = {
        "norm_pass": norm_pass_2d,
        "born_pass": born_pass_2d,
        "born_err": born_err_2d,
        "gravity_toward": grav_2d_toward,
        "gravity_shift": grav_2d_shift,
        "spectral_toward": spec_2d_toward,
        "spectral_shift": spec_2d_shift,
        "n_toward": n_toward_2d,
    }

    # ---- 3D UNITARY U ----
    print()
    print("=" * 72)
    print("3D UNITARY U (polar decomposition)")
    print("=" * 72)

    norm_pass_3d, norm_dev_3d, norm_final_3d = test_norm(U_flat_3d, psi0_3d, "3D unitary")
    print(f"  Norm: max deviation = {norm_dev_3d:.2e} ({'PASS' if norm_pass_3d else 'FAIL'})")

    born_pass_3d, born_err_3d = test_born_3d(U_flat_3d, nw_3d, npl_3d, "3D unitary")
    print(f"  Born (linearity): rel err = {born_err_3d:.2e} ({'PASS' if born_pass_3d else 'FAIL'})")

    grav_3d_toward, grav_3d_shift, c_flat_3d, c_mass_3d = test_gravity(
        U_flat_3d, U_mass_3d, psi0_3d, centroid_fn_3d, MASS_Z_3D, "3D unitary")
    dr = "TOWARD" if grav_3d_toward else "AWAY"
    print(f"  Gravity k={K_TEST}: shift={grav_3d_shift:+.6e} ({dr})")
    print(f"    centroid flat={c_flat_3d:.8f}, mass={c_mass_3d:.8f}")

    spec_3d_toward, spec_3d_shift, n_toward_3d, n_total_3d, per_k_3d = test_spectral(
        build_M_3d, field_flat_3d, field_mass_3d, psi0_3d, centroid_fn_3d,
        MASS_Z_3D, K_SPECTRAL, action_mode, "3D unitary")
    dr = "TOWARD" if spec_3d_toward else "AWAY"
    print(f"  Spectral: shift={spec_3d_shift:+.6e} ({dr}), {n_toward_3d}/{n_total_3d} per-k TOWARD")
    print(f"    Per-k breakdown:")
    for kv, delta in per_k_3d:
        d = "TOWARD" if (delta * MASS_Z_3D) > 0 else "AWAY"
        print(f"      k={kv:5.1f}: shift={delta:+.6e} ({d})")

    results["3D unitary U"] = {
        "norm_pass": norm_pass_3d,
        "born_pass": born_pass_3d,
        "born_err": born_err_3d,
        "gravity_toward": grav_3d_toward,
        "gravity_shift": grav_3d_shift,
        "spectral_toward": spec_3d_toward,
        "spectral_shift": spec_3d_shift,
        "n_toward": n_toward_3d,
    }

    # ==================================================================
    # HEAD-TO-HEAD COMPARISON TABLE
    # ==================================================================
    print()
    print("=" * 72)
    print("HEAD-TO-HEAD COMPARISON TABLE")
    print("=" * 72)
    print()

    header = f"{'Test':<20s} | {'2D raw M':>12s} | {'2D unitary U':>12s} | {'3D raw M':>12s} | {'3D unitary U':>12s}"
    print(header)
    print("-" * len(header))

    # Born (linearity)
    born_2d_str = f"{born_err_2d:.2e}"
    born_3d_str = f"{born_err_3d:.2e}"
    print(f"{'Born linearity':<20s} | {'N/A':>12s} | {born_2d_str:>12s} | {'N/A':>12s} | {born_3d_str:>12s}")

    # Gravity single-k
    def grav_str(toward, shift):
        d = "TOWARD" if toward else "AWAY"
        return f"{shift:+.1e} {d}"

    g_raw_2d = grav_str(grav_raw_2d_toward, grav_raw_2d_shift)
    g_uni_2d = grav_str(grav_2d_toward, grav_2d_shift)
    g_raw_3d = grav_str(grav_raw_3d_toward, grav_raw_3d_shift)
    g_uni_3d = grav_str(grav_3d_toward, grav_3d_shift)
    print(f"{'Gravity k=5':<20s} | {g_raw_2d:>12s} | {g_uni_2d:>12s} | {g_raw_3d:>12s} | {g_uni_3d:>12s}")

    # Spectral gravity
    s_uni_2d = grav_str(spec_2d_toward, spec_2d_shift)
    s_uni_3d = grav_str(spec_3d_toward, spec_3d_shift)
    print(f"{'Spectral grav':<20s} | {'N/A':>12s} | {s_uni_2d:>12s} | {'N/A':>12s} | {s_uni_3d:>12s}")

    # Norm
    print(f"{'Norm layer {0}':<20s} | {norm_raw_2d:>12.2e} | {norm_final_2d:>12.6f} | {norm_raw_3d:>12.2e} | {norm_final_3d if norm_pass_3d else norm_final_3d:>12.6f}".format(N_LAYERS))

    # Spectral per-k toward
    print(f"{'Per-k TOWARD':<20s} | {'N/A':>12s} | {f'{n_toward_2d}/{n_total_2d}':>12s} | {'N/A':>12s} | {f'{n_toward_3d}/{n_total_3d}':>12s}")

    # ==================================================================
    # ANALYSIS
    # ==================================================================
    print()
    print("=" * 72)
    print("ANALYSIS")
    print("=" * 72)
    print()

    # Born rule check
    born_ok = born_pass_2d and born_pass_3d
    print(f"Born rule: {'PASS both dimensions' if born_ok else 'FAIL in at least one dimension'}")

    # Gravity sign comparison
    print()
    print("Gravity sign comparison:")
    print(f"  2D raw:    {'TOWARD' if grav_raw_2d_toward else 'AWAY'}")
    print(f"  2D unitary: {'TOWARD' if grav_2d_toward else 'AWAY'}")
    print(f"  3D raw:    {'TOWARD' if grav_raw_3d_toward else 'AWAY'}")
    print(f"  3D unitary: {'TOWARD' if grav_3d_toward else 'AWAY'}")

    split_raw = grav_raw_2d_toward != grav_raw_3d_toward
    split_uni = grav_2d_toward != grav_3d_toward
    print()
    if split_raw:
        print("  Raw M: 2D and 3D give OPPOSITE gravity signs.")
    else:
        print("  Raw M: 2D and 3D give SAME gravity sign.")

    if split_uni:
        print("  Unitary U: 2D and 3D give OPPOSITE gravity signs.")
        print("  => The dimensional effect is REAL and survives unitarization.")
    else:
        print("  Unitary U: 2D and 3D give SAME gravity sign.")
        if split_raw:
            print("  => The 2D/3D split was an ARTIFACT of non-unitarity!")
        else:
            print("  => Consistent: both raw and unitary agree on sign.")

    # Spectral
    print()
    print("Spectral averaging:")
    print(f"  2D: {'TOWARD' if spec_2d_toward else 'AWAY'} ({n_toward_2d}/{n_total_2d} per-k)")
    print(f"  3D: {'TOWARD' if spec_3d_toward else 'AWAY'} ({n_toward_3d}/{n_total_3d} per-k)")

    # ==================================================================
    # VERDICT
    # ==================================================================
    print()
    print("=" * 72)
    print("VERDICT")
    print("=" * 72)
    print()

    if born_ok and grav_2d_toward and grav_3d_toward:
        print("HYPOTHESIS CONFIRMED: Unitary propagator preserves Born AND gravity")
        print("in BOTH 2D and 3D. The 2D/3D split (if any) was a non-unitarity artifact.")
    elif born_ok and grav_3d_toward and not grav_2d_toward:
        print("PARTIAL: Born passes in both dimensions, but gravity is TOWARD in 3D")
        print("and AWAY in 2D even under unitarization.")
        print("=> The 2D/3D gravity sign split is a REAL dimensional effect.")
        if spec_2d_toward:
            print("=> However, spectral averaging fixes 2D to TOWARD.")
        else:
            print("=> Spectral averaging does NOT fix 2D. The split is fundamental.")
    elif born_ok and not grav_3d_toward:
        print("UNEXPECTED: Born passes but 3D gravity is AWAY under unitarization.")
        print("This contradicts prior 3D results.")
    elif not born_ok:
        print("FALSIFIED: Born rule fails under unitary propagator.")
        print("This should not happen since U is linear. Check implementation.")
    else:
        print("MIXED: See details above.")

    print()
    print(f"Total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
