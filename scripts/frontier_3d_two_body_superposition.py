#!/usr/bin/env python3
"""
frontier_3d_two_body_superposition.py

Test whether propagation is linear in an ANALYTICALLY ADDITIVE external
field on the 3D ordered lattice with valley-linear action.

NOTE (from review): This script builds two single-mass analytic 1/r
fields and DEFINES field_ab = field_a + field_b directly. It therefore
tests whether the propagator responds linearly to an already-additive
field, NOT whether the retained multi-source field solver (derive_node_field)
produces additive fields. The 0.01% error shows propagator linearity
in the field coupling, not gravitational superposition from first principles.

A true multi-source superposition test would need to solve the Laplacian
field with BOTH mass clusters simultaneously and compare to the sum
of individually-solved fields.

Hypothesis: Propagation is linear in the field coupling (delta(A+B) = delta(A) + delta(B)
  when field(A+B) = field(A) + field(B) by construction).
Falsification: If superposition error > 10% even with additive fields.
"""

import math
import numpy as np

# --- constants ---
BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
STRENGTH = 5e-5


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
        n = self.n; hw = self.hw; nl = self.nl; nw = self._nw; hm = self._hm
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
                ym = max(0, -dy); yM = min(nw, nw - dy)
                zm = max(0, -dz); zM = min(nw, nw - dz)
                if ym >= yM or zm >= zM:
                    continue
                yr = np.arange(ym, yM); zr = np.arange(zm, zM)
                siy, siz = np.meshgrid(yr, zr, indexing='ij')
                si = siy.ravel() * nw + siz.ravel()
                di = (siy.ravel() + dy) * nw + (siz.ravel() + dz)
                a = sa[si]; nz = np.abs(a) > 1e-30
                if not np.any(nz):
                    continue
                lf = 0.5 * (sf[si[nz]] + df[di[nz]])
                # Valley-linear action: S = L(1-f)
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field_spatial(lat, z_mass_phys, strength):
    """Spatial-only 1/r field (no causal x in radius)."""
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    my, mz = lat.pos[mi, 1], lat.pos[mi, 2]
    r_spatial = np.sqrt((lat.pos[:, 1] - my)**2 + (lat.pos[:, 2] - mz)**2) + 0.1
    return strength / r_spatial, mi


def setup_slits(lat):
    bl = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = lat.nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if lat.pos[i, 1] >= 0.5]
    sb = [i for i in bi if lat.pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked, bl


def z_centroid(lat, amps):
    """Compute z-centroid at the detector (last layer)."""
    ls = lat._ls[-1]
    det = amps[ls:ls + lat.npl]
    prob = np.abs(det) ** 2
    total = prob.sum()
    if total < 1e-30:
        return 0.0
    z_vals = lat.pos[ls:ls + lat.npl, 2]
    return np.sum(z_vals * prob) / total


def run_config(lat, field, blocked):
    """Run propagation and return z-centroid."""
    amps = lat.propagate(field, K, blocked)
    return z_centroid(lat, amps)


def main():
    print("=" * 65)
    print("3D Two-Body Superposition Test (Valley-Linear Action)")
    print("=" * 65)

    h = 0.5
    W = 6
    L = 12
    lat = Lattice3D(L, W, h)
    print(f"Lattice: L={L}, W={W}, h={h}")
    print(f"  nodes={lat.n}, layers={lat.nl}, nodes/layer={lat.npl}")
    print(f"  BETA={BETA}, K={K}, STRENGTH={STRENGTH}")

    _, _, _, blocked, _ = setup_slits(lat)
    print(f"  slit barrier at layer {lat.nl // 3}, blocked={len(blocked)} nodes")

    # Mass positions (both on +z side, asymmetric)
    z_a = 2.0
    z_b = 4.0
    print(f"\nMass A at z={z_a}, Mass B at z={z_b}")

    # Build fields
    field_none = np.zeros(lat.n)
    field_a, mi_a = make_field_spatial(lat, z_a, STRENGTH)
    field_b, mi_b = make_field_spatial(lat, z_b, STRENGTH)
    field_ab = field_a + field_b  # exact superposition of source fields

    print(f"  Mass A node: {mi_a}, Mass B node: {mi_b}")
    print(f"  field_a range: [{field_a.min():.6e}, {field_a.max():.6e}]")
    print(f"  field_b range: [{field_b.min():.6e}, {field_b.max():.6e}]")
    print(f"  field_ab range: [{field_ab.min():.6e}, {field_ab.max():.6e}]")

    # Run 4 configurations
    print("\nRunning propagations...")
    configs = {
        "no mass": field_none,
        "mass A":  field_a,
        "mass B":  field_b,
        "A + B":   field_ab,
    }

    results = {}
    for name, field in configs.items():
        zc = run_config(lat, field, blocked)
        results[name] = zc
        print(f"  {name:10s}: z-centroid = {zc:.8f}")

    # Compute deltas
    base = results["no mass"]
    delta_a = results["mass A"] - base
    delta_b = results["mass B"] - base
    delta_ab = results["A + B"] - base
    delta_sum = delta_a + delta_b

    # Determine directions
    def direction(d, z_mass):
        if abs(d) < 1e-12:
            return "NONE"
        # Mass is at +z; TOWARD means centroid shifts toward +z
        return "TOWARD" if d > 0 else "AWAY"

    print("\n" + "=" * 65)
    print("RESULTS")
    print("=" * 65)
    print(f"{'Config':10s} | {'z-centroid':>12s} | {'delta':>12s} | direction")
    print("-" * 65)
    print(f"{'no mass':10s} | {base:12.8f} | {'0':>12s} | ")
    for name, z_mass in [("mass A", z_a), ("mass B", z_b), ("A + B", (z_a + z_b) / 2)]:
        d = results[name] - base
        dr = direction(d, z_mass)
        print(f"{name:10s} | {results[name]:12.8f} | {d:+12.8f} | {dr}")

    print()
    print(f"delta(A) + delta(B) = {delta_sum:+.8e}")
    print(f"delta(A+B)          = {delta_ab:+.8e}")

    if abs(delta_ab) > 1e-15:
        error = abs(delta_ab - delta_sum) / abs(delta_ab) * 100
    else:
        error = 0.0
    print(f"Superposition error = {error:.1f}%")

    print()
    if error < 10:
        print("VERDICT: Superposition HOLDS (<10% error).")
        print("  -> 2D failure was dimension-specific, NOT structural.")
    else:
        print("VERDICT: Superposition FAILS (>=10% error).")
        print("  -> Nonlinearity is structural to phase-valley mechanism.")

    # Additional diagnostics
    print("\n--- Diagnostics ---")
    print(f"delta(A) = {delta_a:+.8e}")
    print(f"delta(B) = {delta_b:+.8e}")
    print(f"delta(A)+delta(B) = {delta_sum:+.8e}")
    print(f"delta(A+B) = {delta_ab:+.8e}")
    print(f"Nonlinear residual = {delta_ab - delta_sum:+.8e}")
    if abs(delta_sum) > 1e-15:
        print(f"Residual/sum ratio = {abs(delta_ab - delta_sum) / abs(delta_sum) * 100:.1f}%")


if __name__ == "__main__":
    main()
