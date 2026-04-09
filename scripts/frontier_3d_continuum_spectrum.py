#!/usr/bin/env python3
"""
frontier_3d_continuum_spectrum.py
=================================
Test whether energy-level spacing from the 3D lattice transfer matrix
approaches the particle-in-a-box prediction  E_n / E_1 -> n^2
as lattice spacing h decreases at fixed physical box width W.

Hypothesis:  E_n/E_1 approaches n^2 as h -> 0 at fixed W.
Falsification: If E_2/E_1 does NOT move toward 4.0 from h=1.0 to h=0.5,
               declare NEGATIVE.

Method:
  1. Build Lattice3D with hard-wall confinement |y|,|z| <= W/2
  2. Propagate from each source on x=0 face to x=L face -> transfer matrix M
  3. SVD of M -> singular values sigma_n
  4. E_n = -ln(sigma_n / sigma_1)  =>  E_n/E_1
  5. Compare to n^2
"""

import math
import time
import numpy as np

# ── constants ──────────────────────────────────────────────────────
BETA = 0.8
K = 5.0
MAX_D_PHYS = 3
W_PHYS = 4.0      # physical box width (hard walls at |y|,|z| <= 2)
L_PHYS = 8.0      # propagation length
STRENGTH = 0.0    # free space (no potential)


# ── Lattice3D (from lattice_3d_valley_linear_card.py, modified) ───
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

    def propagate(self, field, k, blocked_set, source_yz=(0, 0)):
        """Propagate from source_yz on x=0 face to x=L face."""
        n = self.n
        hw = self.hw
        nl = self.nl
        nw = self._nw
        hm = self._hm
        amps = np.zeros(n, dtype=np.complex128)
        iy_src, iz_src = source_yz
        src = self.nmap.get((0, iy_src, iz_src), None)
        if src is None:
            return amps
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


# ── helpers ────────────────────────────────────────────────────────
def build_blocked_set(lat, wall_half):
    """Block all nodes with |y| > wall_half or |z| > wall_half."""
    blocked = set()
    for (layer, iy, iz), idx in lat.nmap.items():
        yp = iy * lat.h
        zp = iz * lat.h
        if abs(yp) > wall_half + 1e-9 or abs(zp) > wall_half + 1e-9:
            blocked.add(idx)
    return blocked


def face_sources(lat, wall_half):
    """Return list of (iy, iz) on x=0 face within the walls."""
    sources = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            yp = iy * lat.h
            zp = iz * lat.h
            if abs(yp) <= wall_half + 1e-9 and abs(zp) <= wall_half + 1e-9:
                sources.append((iy, iz))
    return sources


def face_outputs(lat, wall_half):
    """Return list of (iy, iz) on x=L face within the walls."""
    last_layer = lat.nl - 1
    outputs = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            yp = iy * lat.h
            zp = iz * lat.h
            if abs(yp) <= wall_half + 1e-9 and abs(zp) <= wall_half + 1e-9:
                outputs.append((iy, iz))
    return outputs


def build_transfer_matrix(lat, field, k, blocked, sources, outputs):
    """Build transfer matrix M[(y_out,z_out), (y_in,z_in)]."""
    last_layer = lat.nl - 1
    n_out = len(outputs)
    n_in = len(sources)
    M = np.zeros((n_out, n_in), dtype=np.complex128)

    for j, (iy_in, iz_in) in enumerate(sources):
        amps = lat.propagate(field, k, blocked, source_yz=(iy_in, iz_in))
        for i, (iy_out, iz_out) in enumerate(outputs):
            idx = lat.nmap.get((last_layer, iy_out, iz_out), None)
            if idx is not None:
                M[i, j] = amps[idx]
    return M


def extract_energies(M, n_levels=8):
    """SVD -> energy levels E_n = -ln(sigma_n / sigma_1)."""
    U, sigma, Vh = np.linalg.svd(M, full_matrices=False)
    # Keep only nonzero singular values
    mask = sigma > 1e-30
    sigma = sigma[mask]
    if len(sigma) < 2:
        return sigma, np.array([])
    E = -np.log(sigma / sigma[0])
    n = min(n_levels, len(E))
    return sigma[:n], E[:n]


# ── main sweep ─────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("3D CONTINUUM SPECTRUM TEST")
    print("Hypothesis: E_n/E_1 -> n^2 as lattice spacing h -> 0")
    print(f"W_phys={W_PHYS}, L_phys={L_PHYS}, BETA={BETA}, K={K}")
    print("=" * 70)

    wall_half = W_PHYS / 2.0
    h_values = [1.0, 0.5]
    results = {}

    for h in h_values:
        print(f"\n--- h = {h} ---")
        t0 = time.time()

        lat = Lattice3D(L_PHYS, W_PHYS, h)
        field = np.zeros(lat.n)  # free space
        blocked = build_blocked_set(lat, wall_half)
        sources = face_sources(lat, wall_half)
        outputs = face_outputs(lat, wall_half)

        print(f"  Lattice: {lat.nl} layers x {lat.npl} nodes/layer = {lat.n} total")
        print(f"  Sources on x=0 face: {len(sources)}")
        print(f"  Outputs on x=L face: {len(outputs)}")
        print(f"  Blocked nodes: {len(blocked)}")
        print(f"  max_d = {lat.max_d}")

        M = build_transfer_matrix(lat, field, K, blocked, sources, outputs)
        sigma, E = extract_energies(M)

        elapsed = time.time() - t0
        print(f"  Time: {elapsed:.1f}s")
        print(f"  Top singular values: {sigma[:6]}")

        if len(E) >= 2:
            print(f"\n  Energy levels (E_n = -ln(sigma_n/sigma_1)):")
            print(f"  {'n':>4s}  {'E_n':>10s}  {'E_n/E_1':>10s}  {'n^2 (pred)':>10s}  {'ratio':>10s}")
            for n_idx in range(1, min(8, len(E))):
                if E[1] > 1e-30:
                    ratio_e = E[n_idx] / E[1]
                else:
                    ratio_e = float('nan')
                n_sq = (n_idx + 1) ** 2  # n starts at 1, so mode n_idx+1
                # Actually for 2D box modes (ny, nz), the spectrum is ny^2+nz^2
                # Ground state: (1,1) -> 2, next: (1,2) or (2,1) -> 5, then (2,2) -> 8
                # E_n/E_1 should be (ny^2+nz^2)/2
                print(f"  {n_idx+1:>4d}  {E[n_idx]:>10.4f}  {ratio_e:>10.4f}  {'---':>10s}  {'':>10s}")

            # Print 2D box mode predictions
            print(f"\n  2D box mode predictions (ny^2+nz^2)/2:")
            modes_2d = []
            for ny in range(1, 6):
                for nz in range(1, 6):
                    modes_2d.append((ny, nz, ny**2 + nz**2))
            modes_2d.sort(key=lambda x: x[2])
            # Remove duplicates in energy
            seen = set()
            unique_modes = []
            for ny, nz, e in modes_2d:
                if e not in seen:
                    seen.add(e)
                    unique_modes.append((ny, nz, e))
            e1 = unique_modes[0][2]
            print(f"  {'mode':>10s}  {'ny^2+nz^2':>10s}  {'ratio':>10s}")
            for ny, nz, e in unique_modes[:8]:
                print(f"  ({ny},{nz}){'':<5s}  {e:>10d}  {e/e1:>10.2f}")

            results[h] = E
        else:
            print("  WARNING: fewer than 2 energy levels extracted")
            results[h] = E

    # ── verdict ────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    if 1.0 in results and 0.5 in results:
        E_coarse = results[1.0]
        E_fine = results[0.5]
        if len(E_coarse) >= 2 and len(E_fine) >= 2:
            r_coarse = E_coarse[1] / E_coarse[1] if E_coarse[1] > 1e-30 else float('nan')
            r_fine = E_fine[1] / E_fine[1] if E_fine[1] > 1e-30 else float('nan')
            # E_2/E_1 ratios
            if len(E_coarse) >= 3 and len(E_fine) >= 3:
                r2_coarse = E_coarse[2] / E_coarse[1] if E_coarse[1] > 1e-30 else float('nan')
                r2_fine = E_fine[2] / E_fine[1] if E_fine[1] > 1e-30 else float('nan')
            else:
                r2_coarse = float('nan')
                r2_fine = float('nan')

            # For 2D box, E_2/E_1 should be 5/2 = 2.5 (modes (1,2) vs (1,1))
            target = 2.5
            print(f"  E_2/E_1 at h=1.0: {r2_coarse:.4f}")
            print(f"  E_2/E_1 at h=0.5: {r2_fine:.4f}")
            print(f"  Target (2D box):   {target:.4f}")
            print()

            if not (math.isnan(r2_coarse) or math.isnan(r2_fine)):
                dist_coarse = abs(r2_coarse - target)
                dist_fine = abs(r2_fine - target)
                if dist_fine < dist_coarse:
                    print("  POSITIVE: E_2/E_1 moves TOWARD 2.5 as h decreases.")
                else:
                    print("  NEGATIVE: E_2/E_1 does NOT move toward 2.5 as h decreases.")
            else:
                print("  INCONCLUSIVE: could not compute ratios.")
        else:
            print("  INCONCLUSIVE: not enough energy levels.")
    else:
        print("  INCONCLUSIVE: missing data for comparison.")

    # Also show all ratios side by side
    print("\n  Full ratio comparison:")
    print(f"  {'n':>4s}  {'h=1.0':>10s}  {'h=0.5':>10s}  {'2D-box':>10s}")
    modes_2d = []
    for ny in range(1, 6):
        for nz in range(1, 6):
            modes_2d.append(ny**2 + nz**2)
    modes_2d = sorted(set(modes_2d))
    e1_box = modes_2d[0]

    for n_idx in range(1, 8):
        r_c = results.get(1.0, np.array([]))
        r_f = results.get(0.5, np.array([]))
        rc = r_c[n_idx] / r_c[1] if len(r_c) > n_idx and r_c[1] > 1e-30 else float('nan')
        rf = r_f[n_idx] / r_f[1] if len(r_f) > n_idx and r_f[1] > 1e-30 else float('nan')
        box = modes_2d[n_idx] / e1_box if n_idx < len(modes_2d) else float('nan')
        print(f"  {n_idx+1:>4d}  {rc:>10.4f}  {rf:>10.4f}  {box:>10.4f}")


if __name__ == "__main__":
    main()
