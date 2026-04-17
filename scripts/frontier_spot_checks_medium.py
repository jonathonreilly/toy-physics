#!/usr/bin/env python3
"""
Frontier Medium Spot Checks — Checks 4 and 6
=============================================

Check 4: VL-3D two-body superposition test
  Place two masses on the 3D ordered lattice.
  Compare propagation with combined field (field_A + field_B)
  to the individual fields. Measure superposition error.

Check 6: Chiral 3+1D spin/chirality tests
  (a) Flat space chirality conservation: propagate pure +z source,
      measure fraction remaining +z at detector.
  (b) Stern-Gerlach: linear gradient field, check spatial separation
      of +z vs -z chiralities.
  (c) Chirality-dependent gravity: pure +z vs pure -z with mass,
      compare deflections.

Hypothesis: VL superposition error < 1%, chirality separates under gradient.
"""

from __future__ import annotations
import math
import time
import numpy as np

# ════════════════════════════════════════════════════════════════════════
# INFRASTRUCTURE: Lattice3D from lattice_3d_valley_linear_card.py
# ════════════════════════════════════════════════════════════════════════

BETA = 0.8
K = 5.0
MAX_D_PHYS = 3


class Lattice3D:
    def __init__(self, phys_l, phys_w, h):
        self.h = h
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(MAX_D_PHYS / h))
        nw = 2 * self.hw + 1
        self.npl = nw ** 2
        self.n = self.nl * self.npl
        self._hm = h * h

        self.pos = np.zeros((self.n, 3))
        self.nmap = {}
        self._ls = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._ls[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    self.pos[idx] = (x, iy * h, iz * h)
                    self.nmap[(layer, iy, iz)] = idx
                    idx += 1

        self._off = []
        for dy in range(-self.max_d, self.max_d + 1):
            for dz in range(-self.max_d, self.max_d + 1):
                dyp = dy * h
                dzp = dz * h
                L = math.sqrt(h * h + dyp * dyp + dzp * dzp)
                theta = math.atan2(math.sqrt(dyp**2 + dzp**2), h)
                w = math.exp(-BETA * theta * theta)
                self._off.append((dy, dz, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n
        hw = self.hw
        nl = self.nl
        nw = self._nw
        hm = self._hm
        amps = np.zeros(n, dtype=np.complex128)
        src = self.nmap.get((0, 0, 0), 0)
        amps[src] = 1.0
        blocked = np.zeros(n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True
        for layer in range(nl - 1):
            ls = self._ls[layer]
            ld = self._ls[layer + 1] if layer + 1 < nl else n
            sa = amps[ls:ls + self.npl].copy()
            sa[blocked[ls:ls + self.npl]] = 0
            if np.max(np.abs(sa)) < 1e-30:
                continue
            sf = field[ls:ls + self.npl]
            df = field[ld:ld + self.npl]
            db = blocked[ld:ld + self.npl]
            for dy, dz, L, w in self._off:
                ym = max(0, -dy)
                yM = min(nw, nw - dy)
                zm = max(0, -dz)
                zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                yr = np.arange(ym, yM)
                zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing='ij')
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]
                nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field_at(lat, z_mass_phys, strength):
    """1/r field from a mass at layer 2/3, z=z_mass_phys."""
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    mx, my, mz = lat.pos[mi]
    r = np.sqrt(
        (lat.pos[:, 0] - mx) ** 2
        + (lat.pos[:, 1] - my) ** 2
        + (lat.pos[:, 2] - mz) ** 2
    ) + 0.1
    return strength / r, mi


# ════════════════════════════════════════════════════════════════════════
# INFRASTRUCTURE: Chiral 3+1D walk from frontier_chiral_3plus1d.py
# ════════════════════════════════════════════════════════════════════════

CH_N = 15
CH_LAYERS = 12
CH_THETA0 = 0.3
NCOMP = 6  # +y, -y, +z, -z, +w, -w
CH_DIM = CH_N * CH_N * CH_N * NCOMP


def ch_idx(iy, iz, iw, c):
    return ((iy * CH_N + iz) * CH_N + iw) * NCOMP + c


def ch_build_field(strength, ym, zm, wm):
    field = np.zeros((CH_N, CH_N, CH_N))
    for iy in range(CH_N):
        for iz in range(CH_N):
            for iw in range(CH_N):
                dy = min(abs(iy - ym), CH_N - abs(iy - ym))
                dz = min(abs(iz - zm), CH_N - abs(iz - zm))
                dw = min(abs(iw - wm), CH_N - abs(iw - wm))
                r = np.sqrt(dy**2 + dz**2 + dw**2)
                field[iy, iz, iw] = strength / (r + 0.1)
    return field


def ch_coin_step(psi, field, theta0):
    psi_out = psi.copy()
    for iy in range(CH_N):
        for iz in range(CH_N):
            for iw in range(CH_N):
                f = field[iy, iz, iw]
                t = theta0 * (1.0 - f)
                ct = np.cos(t)
                st = 1j * np.sin(t)
                base = ((iy * CH_N + iz) * CH_N + iw) * NCOMP
                # y-pair
                py, my_ = psi_out[base + 0], psi_out[base + 1]
                psi_out[base + 0] = ct * py + st * my_
                psi_out[base + 1] = st * py + ct * my_
                # z-pair
                pz, mz = psi_out[base + 2], psi_out[base + 3]
                psi_out[base + 2] = ct * pz + st * mz
                psi_out[base + 3] = st * pz + ct * mz
                # w-pair
                pw, mw = psi_out[base + 4], psi_out[base + 5]
                psi_out[base + 4] = ct * pw + st * mw
                psi_out[base + 5] = st * pw + ct * mw
    return psi_out


def ch_shift_step(psi):
    psi_out = np.zeros_like(psi)
    for iy in range(CH_N):
        for iz in range(CH_N):
            for iw in range(CH_N):
                base_src = ((iy * CH_N + iz) * CH_N + iw) * NCOMP
                iy2 = (iy + 1) % CH_N
                psi_out[((iy2 * CH_N + iz) * CH_N + iw) * NCOMP + 0] += psi[base_src + 0]
                iy2 = (iy - 1) % CH_N
                psi_out[((iy2 * CH_N + iz) * CH_N + iw) * NCOMP + 1] += psi[base_src + 1]
                iz2 = (iz + 1) % CH_N
                psi_out[((iy * CH_N + iz2) * CH_N + iw) * NCOMP + 2] += psi[base_src + 2]
                iz2 = (iz - 1) % CH_N
                psi_out[((iy * CH_N + iz2) * CH_N + iw) * NCOMP + 3] += psi[base_src + 3]
                iw2 = (iw + 1) % CH_N
                psi_out[((iy * CH_N + iz) * CH_N + iw2) * NCOMP + 4] += psi[base_src + 4]
                iw2 = (iw - 1) % CH_N
                psi_out[((iy * CH_N + iz) * CH_N + iw2) * NCOMP + 5] += psi[base_src + 5]
    return psi_out


def ch_propagate(psi, field, theta0, n_layers):
    for _ in range(n_layers):
        psi = ch_coin_step(psi, field, theta0)
        psi = ch_shift_step(psi)
    return psi


def ch_z_expectation(psi):
    prob_z = np.zeros(CH_N)
    for iy in range(CH_N):
        for iz in range(CH_N):
            for iw in range(CH_N):
                base = ((iy * CH_N + iz) * CH_N + iw) * NCOMP
                prob_z[iz] += np.sum(np.abs(psi[base:base + NCOMP]) ** 2)
    total = np.sum(prob_z)
    if total < 1e-30:
        return CH_N / 2.0
    return np.sum(np.arange(CH_N) * prob_z) / total


def ch_z_expectation_component(psi, comp):
    """Expectation of z for a single chiral component."""
    prob_z = np.zeros(CH_N)
    for iy in range(CH_N):
        for iz in range(CH_N):
            for iw in range(CH_N):
                i = ch_idx(iy, iz, iw, comp)
                prob_z[iz] += np.abs(psi[i]) ** 2
    total = np.sum(prob_z)
    if total < 1e-30:
        return CH_N / 2.0, 0.0
    return np.sum(np.arange(CH_N) * prob_z) / total, total


def ch_component_fraction(psi, comp):
    """Fraction of total probability in component comp."""
    total = np.sum(np.abs(psi) ** 2)
    if total < 1e-30:
        return 0.0
    comp_prob = 0.0
    for iy in range(CH_N):
        for iz in range(CH_N):
            for iw in range(CH_N):
                i = ch_idx(iy, iz, iw, comp)
                comp_prob += np.abs(psi[i]) ** 2
    return comp_prob / total


# ════════════════════════════════════════════════════════════════════════
# CHECK 4: VL-3D Two-Body Superposition Test
# ════════════════════════════════════════════════════════════════════════

def run_check4():
    print("=" * 70)
    print("CHECK 4: VL-3D Two-Body Superposition Test")
    print("=" * 70)
    t0 = time.time()

    # Use h=0.5, W=6, L=12 for speed
    lat = Lattice3D(12, 6, 0.5)
    det = [
        lat.nmap[(lat.nl - 1, iy, iz)]
        for iy in range(-lat.hw, lat.hw + 1)
        for iz in range(-lat.hw, lat.hw + 1)
        if (lat.nl - 1, iy, iz) in lat.nmap
    ]
    pos = lat.pos
    strength = 5e-5

    # No barrier for this test
    blocked = set()

    # Free-field baseline
    field_flat = np.zeros(lat.n)
    af = lat.propagate(field_flat, K, blocked)
    pf = sum(abs(af[d]) ** 2 for d in det)
    zf = sum(abs(af[d]) ** 2 * pos[d, 2] for d in det) / pf
    print(f"  Free: <z> = {zf:.6f}, P_det = {pf:.6e}")

    # Mass A at z=2
    field_A, mi_A = make_field_at(lat, 2, strength)
    aA = lat.propagate(field_A, K, blocked)
    pA = sum(abs(aA[d]) ** 2 for d in det)
    zA = sum(abs(aA[d]) ** 2 * pos[d, 2] for d in det) / pA
    deltaA = zA - zf
    print(f"  Mass A (z=2): <z> = {zA:.6f}, delta = {deltaA:+.6f}")

    # Mass B at z=5
    field_B, mi_B = make_field_at(lat, 5, strength)
    aB = lat.propagate(field_B, K, blocked)
    pB = sum(abs(aB[d]) ** 2 for d in det)
    zB = sum(abs(aB[d]) ** 2 * pos[d, 2] for d in det) / pB
    deltaB = zB - zf
    print(f"  Mass B (z=5): <z> = {zB:.6f}, delta = {deltaB:+.6f}")

    # Combined field: field_AB = field_A + field_B (additive superposition)
    field_AB = field_A + field_B
    aAB = lat.propagate(field_AB, K, blocked)
    pAB = sum(abs(aAB[d]) ** 2 for d in det)
    zAB = sum(abs(aAB[d]) ** 2 * pos[d, 2] for d in det) / pAB
    deltaAB = zAB - zf
    print(f"  Mass A+B combined: <z> = {zAB:.6f}, delta = {deltaAB:+.6f}")

    # Superposition prediction: delta(AB) should equal delta(A) + delta(B)
    # in the linear regime (weak field)
    predicted_delta = deltaA + deltaB
    superposition_error = abs(deltaAB - predicted_delta)
    relative_error = superposition_error / abs(predicted_delta) if abs(predicted_delta) > 1e-12 else float('inf')

    print()
    print(f"  Predicted (deltaA + deltaB) = {predicted_delta:+.6f}")
    print(f"  Actual deltaAB              = {deltaAB:+.6f}")
    print(f"  Superposition error (abs)   = {superposition_error:.2e}")
    print(f"  Relative error              = {relative_error:.2%}")

    # Also check detector probability distribution similarity
    # Compare |psi_AB|^2 to what we'd predict from linear combination
    prob_AB = np.array([abs(aAB[d]) ** 2 for d in det])
    prob_AB_norm = prob_AB / prob_AB.sum() if prob_AB.sum() > 1e-30 else prob_AB

    # For the field test, the key measure is whether forces add linearly
    # i.e. the deflection from two masses equals sum of individual deflections
    sp_pass = relative_error < 0.01  # < 1%
    verdict = "PASS" if sp_pass else ("WEAK" if relative_error < 0.05 else "FAIL")
    print(f"\n  VERDICT: {verdict} (superposition error {relative_error:.2%}, threshold < 1%)")
    print(f"  Time: {time.time() - t0:.1f}s")

    # Also test with stronger fields to see nonlinearity onset
    print()
    print("  --- Nonlinearity sweep (increasing strength) ---")
    for s in [5e-5, 2e-4, 1e-3, 5e-3]:
        fA, _ = make_field_at(lat, 2, s)
        fB, _ = make_field_at(lat, 5, s)
        fAB = fA + fB

        aA_s = lat.propagate(fA, K, blocked)
        aB_s = lat.propagate(fB, K, blocked)
        aAB_s = lat.propagate(fAB, K, blocked)

        pA_s = sum(abs(aA_s[d]) ** 2 for d in det)
        pB_s = sum(abs(aB_s[d]) ** 2 for d in det)
        pAB_s = sum(abs(aAB_s[d]) ** 2 for d in det)

        dA_s = sum(abs(aA_s[d]) ** 2 * pos[d, 2] for d in det) / pA_s - zf
        dB_s = sum(abs(aB_s[d]) ** 2 * pos[d, 2] for d in det) / pB_s - zf
        dAB_s = sum(abs(aAB_s[d]) ** 2 * pos[d, 2] for d in det) / pAB_s - zf

        pred = dA_s + dB_s
        err = abs(dAB_s - pred) / abs(pred) if abs(pred) > 1e-12 else float('inf')
        print(f"    s={s:.0e}: dA={dA_s:+.6f}, dB={dB_s:+.6f}, dAB={dAB_s:+.6f}, "
              f"pred={pred:+.6f}, rel_err={err:.2%}")

    return sp_pass, relative_error


# ════════════════════════════════════════════════════════════════════════
# CHECK 6: Chiral 3+1D Spin/Chirality Tests
# ════════════════════════════════════════════════════════════════════════

def run_check6():
    print()
    print("=" * 70)
    print("CHECK 6: Chiral 3+1D Spin/Chirality Tests")
    print(f"  Grid: {CH_N}x{CH_N}x{CH_N}, {CH_LAYERS} layers, {NCOMP} components")
    print("=" * 70)
    t0 = time.time()

    center = CH_N // 2  # = 7

    # ── 6a: Flat space chirality conservation ──
    print()
    print("  --- 6a: Chirality Conservation (flat space) ---")
    flat_field = np.zeros((CH_N, CH_N, CH_N))

    # Pure +z source (component 2)
    psi_pz = np.zeros(CH_DIM, dtype=complex)
    psi_pz[ch_idx(center, center, center, 2)] = 1.0

    psi_pz_out = ch_propagate(psi_pz, flat_field, CH_THETA0, CH_LAYERS)

    # Measure fraction in each component
    comp_names = ["+y", "-y", "+z", "-z", "+w", "-w"]
    print(f"    Source: pure +z at ({center},{center},{center})")
    print(f"    After {CH_LAYERS} layers:")
    fracs = []
    for c in range(NCOMP):
        frac = ch_component_fraction(psi_pz_out, c)
        fracs.append(frac)
        print(f"      {comp_names[c]}: {frac:.4f}")

    frac_pz = fracs[2]  # +z component
    frac_mz = fracs[3]  # -z component
    frac_z_total = frac_pz + frac_mz  # z-pair total

    print(f"    +z fraction retained: {frac_pz:.4f}")
    print(f"    z-pair total (+z + -z): {frac_z_total:.4f}")
    print(f"    Coin mixes within pairs, so z-pair should be conserved = 1/3")

    # The coin mixes +z <-> -z but not with y or w pairs
    # So z-pair fraction should stay at 1/NCOMP * 2 ... no wait.
    # Source is pure +z (1 component out of 6). The coin mixes +z <-> -z
    # but NOT y-pair or w-pair. So after coin, amplitude stays in z-pair.
    # But the shift moves +z in the +z direction and -z in -z direction,
    # which is spatial only.
    # Since source only excites z-pair, y and w pairs should remain zero!
    frac_non_z = sum(fracs[c] for c in [0, 1, 4, 5])
    chirality_conserved = frac_non_z < 0.01  # non-z pairs should be ~0
    print(f"    Non-z-pair fraction: {frac_non_z:.2e}")
    print(f"    z-pair conservation: {'PASS' if chirality_conserved else 'FAIL'}")

    # ── 6b: Stern-Gerlach (gradient field) ──
    print()
    print("  --- 6b: Stern-Gerlach (linear z-gradient) ---")

    # Linear gradient in z: f(z) = gradient * (z - center)
    gradient = 0.02
    grad_field = np.zeros((CH_N, CH_N, CH_N))
    for iz in range(CH_N):
        grad_field[:, iz, :] = gradient * (iz - center)

    # Propagate pure +z
    psi_pz_grad = np.zeros(CH_DIM, dtype=complex)
    psi_pz_grad[ch_idx(center, center, center, 2)] = 1.0
    psi_pz_grad_out = ch_propagate(psi_pz_grad, grad_field, CH_THETA0, CH_LAYERS)

    # Propagate pure -z
    psi_mz_grad = np.zeros(CH_DIM, dtype=complex)
    psi_mz_grad[ch_idx(center, center, center, 3)] = 1.0
    psi_mz_grad_out = ch_propagate(psi_mz_grad, grad_field, CH_THETA0, CH_LAYERS)

    # Measure z-expectation for each
    z_pz, norm_pz = ch_z_expectation_component(psi_pz_grad_out, 2)
    z_mz, norm_mz = ch_z_expectation_component(psi_mz_grad_out, 3)

    # Also full z-expectation
    z_pz_full = ch_z_expectation(psi_pz_grad_out)
    z_mz_full = ch_z_expectation(psi_mz_grad_out)

    separation = z_pz_full - z_mz_full

    print(f"    Gradient: f(z) = {gradient} * (z - {center})")
    print(f"    +z source -> <z> = {z_pz_full:.4f} (comp +z: <z>={z_pz:.4f}, P={norm_pz:.4f})")
    print(f"    -z source -> <z> = {z_mz_full:.4f} (comp -z: <z>={z_mz:.4f}, P={norm_mz:.4f})")
    print(f"    Separation: {separation:+.4f}")
    sg_pass = abs(separation) > 0.01
    print(f"    Stern-Gerlach: {'PASS' if sg_pass else 'FAIL'} "
          f"({'separated' if sg_pass else 'no separation'})")

    # ── 6c: Chirality-dependent gravity ──
    print()
    print("  --- 6c: Chirality-Dependent Gravity ---")

    mass_z = 10
    grav_strength = 5e-4
    grav_field = ch_build_field(grav_strength, center, mass_z, center)
    flat_field_c = np.zeros((CH_N, CH_N, CH_N))

    # Flat-space references
    psi_pz_flat_src = np.zeros(CH_DIM, dtype=complex)
    psi_pz_flat_src[ch_idx(center, center, center, 2)] = 1.0
    psi_pz_flat_out = ch_propagate(psi_pz_flat_src.copy(), flat_field_c, CH_THETA0, CH_LAYERS)
    z_pz_flat = ch_z_expectation(psi_pz_flat_out)

    psi_mz_flat_src = np.zeros(CH_DIM, dtype=complex)
    psi_mz_flat_src[ch_idx(center, center, center, 3)] = 1.0
    psi_mz_flat_out = ch_propagate(psi_mz_flat_src.copy(), flat_field_c, CH_THETA0, CH_LAYERS)
    z_mz_flat = ch_z_expectation(psi_mz_flat_out)

    # With gravity
    psi_pz_grav_out = ch_propagate(psi_pz_flat_src.copy(), grav_field, CH_THETA0, CH_LAYERS)
    z_pz_grav = ch_z_expectation(psi_pz_grav_out)
    delta_pz = z_pz_grav - z_pz_flat

    psi_mz_grav_out = ch_propagate(psi_mz_flat_src.copy(), grav_field, CH_THETA0, CH_LAYERS)
    z_mz_grav = ch_z_expectation(psi_mz_grav_out)
    delta_mz = z_mz_grav - z_mz_flat

    print(f"    Mass at z={mass_z}, source at z={center}")
    print(f"    +z flat: <z>={z_pz_flat:.4f}, with grav: <z>={z_pz_grav:.4f}, "
          f"delta={delta_pz:+.6f} ({'TOWARD' if delta_pz > 0 else 'AWAY'})")
    print(f"    -z flat: <z>={z_mz_flat:.4f}, with grav: <z>={z_mz_grav:.4f}, "
          f"delta={delta_mz:+.6f} ({'TOWARD' if delta_mz > 0 else 'AWAY'})")

    diff = abs(delta_pz - delta_mz)
    avg = 0.5 * (abs(delta_pz) + abs(delta_mz))
    asym = diff / avg if avg > 1e-12 else 0.0

    print(f"    |delta_pz - delta_mz| = {diff:.2e}")
    print(f"    Asymmetry ratio: {asym:.2%}")
    # Since +z moves in +z direction and -z in -z, they explore different
    # spatial regions and should feel gravity differently
    grav_asym_pass = asym > 0.001  # even 0.1% is meaningful
    print(f"    Chirality-dependent gravity: {'PASS' if grav_asym_pass else 'FAIL'}")

    # Also test balanced source for comparison
    psi_bal = np.zeros(CH_DIM, dtype=complex)
    amp = 1.0 / np.sqrt(NCOMP)
    for c in range(NCOMP):
        psi_bal[ch_idx(center, center, center, c)] = amp
    psi_bal_flat_out = ch_propagate(psi_bal.copy(), flat_field_c, CH_THETA0, CH_LAYERS)
    z_bal_flat = ch_z_expectation(psi_bal_flat_out)
    psi_bal_grav_out = ch_propagate(psi_bal.copy(), grav_field, CH_THETA0, CH_LAYERS)
    z_bal_grav = ch_z_expectation(psi_bal_grav_out)
    delta_bal = z_bal_grav - z_bal_flat
    print(f"    Balanced source: delta={delta_bal:+.6f} ({'TOWARD' if delta_bal > 0 else 'AWAY'})")

    elapsed = time.time() - t0
    print(f"\n  Check 6 total time: {elapsed:.1f}s")

    return chirality_conserved, sg_pass, grav_asym_pass


# ════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════

def main():
    t_total = time.time()
    print("=" * 70)
    print("FRONTIER MEDIUM SPOT CHECKS")
    print("Checks 4 and 6")
    print("Hypothesis: VL superposition < 1%, chirality separates under gradient")
    print("=" * 70)
    print()

    sp_pass, sp_err = run_check4()

    ch_conserved, sg_pass, grav_asym_pass = run_check6()

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY — Medium Spot Checks")
    print("=" * 70)
    print(f"  Check 4 (VL-3D two-body superposition):")
    print(f"    Relative error: {sp_err:.2%}")
    print(f"    Verdict: {'PASS' if sp_pass else 'FAIL'} (threshold < 1%)")
    print()
    print(f"  Check 6 (Chiral 3+1D spin/chirality):")
    print(f"    6a Chirality conservation: {'PASS' if ch_conserved else 'FAIL'}")
    print(f"    6b Stern-Gerlach:          {'PASS' if sg_pass else 'FAIL'}")
    print(f"    6c Gravity asymmetry:      {'PASS' if grav_asym_pass else 'FAIL'}")
    print()
    total_pass = sum([sp_pass, ch_conserved, sg_pass, grav_asym_pass])
    print(f"  Score: {total_pass}/4")
    print(f"  Total time: {time.time() - t_total:.1f}s")
    print("=" * 70)


if __name__ == "__main__":
    main()
