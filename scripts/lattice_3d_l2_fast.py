#!/usr/bin/env python3
"""3D 1/L^2 kernel — memory-efficient layer-by-layer propagation.

Instead of pre-computing all edges, compute each layer's contributions
on the fly. This uses O(npl * edges_per_node) memory per layer instead
of O(total_edges) total.

Enables h=0.25 with W=6, max_d_phys=3 (the full dense lattice).
"""

from __future__ import annotations
import math
import time
import numpy as np

BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8


class Lattice3D:
    def __init__(self, phys_l, phys_w, max_d_phys, h):
        self.h = h
        self.phys_w = phys_w
        self.nl = int(phys_l / h) + 1
        self.hw = int(phys_w / h)
        self.max_d = max(1, round(max_d_phys / h))
        self.npl = (2 * self.hw + 1) ** 2
        self.n = self.nl * self.npl

        # Node positions and mapping
        self.pos = np.zeros((self.n, 3))
        self.nmap = {}
        self._layer_start = np.zeros(self.nl, dtype=np.int64)
        idx = 0
        for layer in range(self.nl):
            self._layer_start[layer] = idx
            x = layer * h
            for iy in range(-self.hw, self.hw + 1):
                for iz in range(-self.hw, self.hw + 1):
                    self.pos[idx] = (x, iy * h, iz * h)
                    self.nmap[(layer, iy, iz)] = idx
                    idx += 1

        # Pre-compute displacement offsets for one layer transition
        offsets = []
        self._h_measure = h * h  # h^(d-1) for d=3 (2 transverse dims)
        for diy in range(-self.max_d, self.max_d + 1):
            for diz in range(-self.max_d, self.max_d + 1):
                dy_phys = diy * h
                dz_phys = diz * h
                L = math.sqrt(h * h + dy_phys * dy_phys + dz_phys * dz_phys)
                theta = math.atan2(math.sqrt(dy_phys**2 + dz_phys**2), h)
                w = math.exp(-BETA * theta * theta)
                offsets.append((diy, diz, L, w))
        self._offsets = offsets
        self._n_offsets = len(offsets)

    def node_idx(self, layer, iy, iz):
        return self._layer_start[layer] + (iy + self.hw) * (2 * self.hw + 1) + (iz + self.hw)

    def propagate_l2(self, field, k, blocked_set):
        n = self.n
        hw = self.hw
        nl = self.nl
        amps = np.zeros(n, dtype=np.complex128)

        # Source at origin
        src = self.nmap.get((0, 0, 0), 0)
        amps[src] = 1.0

        blocked = np.zeros(n, dtype=bool)
        for b in blocked_set:
            blocked[b] = True

        # Layer-by-layer propagation
        nw = 2 * hw + 1
        for layer in range(nl - 1):
            ls = self._layer_start[layer]
            ld = self._layer_start[layer + 1] if layer + 1 < nl else n

            # Get source layer amplitudes
            src_amps = amps[ls:ls + self.npl].copy()
            src_blocked = blocked[ls:ls + self.npl]
            src_amps[src_blocked] = 0

            # Skip if no signal in this layer
            if np.max(np.abs(src_amps)) < 1e-30:
                continue

            src_field = field[ls:ls + self.npl]
            dst_field = field[ld:ld + self.npl]
            dst_blocked = blocked[ld:ld + self.npl]

            # For each offset, compute contributions
            for diy, diz, L, w in self._offsets:
                # Source nodes: all (iy, iz) in layer
                # Destination: (iy+diy, iz+diz) in layer+1
                # Valid range: src iy in [-hw, hw], dst iy = src_iy + diy in [-hw, hw]
                # So src_iy in [max(-hw, -hw-diy), min(hw, hw-diy)]
                src_iy_min = max(0, -diy)
                src_iy_max = min(nw, nw - diy)
                src_iz_min = max(0, -diz)
                src_iz_max = min(nw, nw - diz)

                if src_iy_min >= src_iy_max or src_iz_min >= src_iz_max:
                    continue

                # Build source and destination index slices
                # Source: (iy, iz) -> flat index = iy*nw + iz
                # Dest: (iy+diy, iz+diz) -> flat = (iy+diy)*nw + (iz+diz)

                # Use meshgrid for vectorized indexing
                src_iy_range = np.arange(src_iy_min, src_iy_max)
                src_iz_range = np.arange(src_iz_min, src_iz_max)
                si_iy, si_iz = np.meshgrid(src_iy_range, src_iz_range, indexing='ij')
                si_flat = si_iy.ravel() * nw + si_iz.ravel()
                di_flat = (si_iy.ravel() + diy) * nw + (si_iz.ravel() + diz)

                # Get amplitudes and fields
                sa = src_amps[si_flat]
                nonzero = np.abs(sa) > 1e-30
                if not np.any(nonzero):
                    continue

                # Compute action for each edge
                sf = src_field[si_flat[nonzero]]
                df = dst_field[di_flat[nonzero]]
                lf = 0.5 * (sf + df)
                dl = L * (1 + lf)
                ret = np.sqrt(np.maximum(dl * dl - L * L, 0))
                act = dl - ret

                # Phase contribution (h^2 measure prevents overflow at fine h;
                # cancels in all ratio-based observables like centroid/Born/MI)
                contrib = sa[nonzero] * np.exp(1j * k * act) * w * self._h_measure / (L * L)

                # Zero out blocked destinations
                db = dst_blocked[di_flat[nonzero]]
                contrib[db] = 0

                # Scatter add
                np.add.at(amps[ld:ld + self.npl], di_flat[nonzero], contrib)

        return amps


def make_field(lat, z_mass_phys, strength):
    pos = lat.pos
    gl = 2 * lat.nl // 3
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    mx, my, mz = pos[mi]
    r = np.sqrt((pos[:, 0] - mx)**2 + (pos[:, 1] - my)**2 + (pos[:, 2] - mz)**2) + 0.1
    return strength / r, mi


def setup_slits(lat):
    pos = lat.pos
    nmap = lat.nmap
    bl = lat.nl // 3
    bi = []
    for iy in range(-lat.hw, lat.hw + 1):
        for iz in range(-lat.hw, lat.hw + 1):
            idx = nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if pos[i, 1] >= 0.5]
    sb = [i for i in bi if pos[i, 1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked, bl


def fit_power(b_data, d_data):
    if len(b_data) < 3:
        return None, None
    lx = np.log(b_data)
    ly = np.log(d_data)
    mx = lx.mean(); my = ly.mean()
    sxx = np.sum((lx - mx)**2)
    sxy = np.sum((lx - mx) * (ly - my))
    if sxx < 1e-10:
        return None, None
    slope = sxy / sxx
    ss_res = np.sum((ly - (my + slope * (lx - mx)))**2)
    ss_tot = np.sum((ly - my)**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return slope, r2


def run_test(phys_l, phys_w, max_d_phys, h, strength):
    print(f"\n{'='*60}")
    t0 = time.time()
    lat = Lattice3D(phys_l, phys_w, max_d_phys, h)
    t_gen = time.time() - t0
    print(f"h={h}: {lat.n:,} nodes, {lat.nl} layers, "
          f"~{lat._n_offsets} edges/node ({t_gen:.1f}s gen)")

    det = [lat.nmap[(lat.nl-1, iy, iz)]
           for iy in range(-lat.hw, lat.hw+1)
           for iz in range(-lat.hw, lat.hw+1)
           if (lat.nl-1, iy, iz) in lat.nmap]
    bi, sa, sb, blocked, bl = setup_slits(lat)
    pos = lat.pos

    field_f = np.zeros(lat.n)
    t1 = time.time()
    af = lat.propagate_l2(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        print("  NO SIGNAL")
        return
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
    print(f"  Free prop: {time.time()-t1:.1f}s")

    # Born check (quick — just 7 propagations)
    t1 = time.time()
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    born = float('nan')
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c)
        other = set(bi) - all_s
        probs = {}
        for key, open_set in [('abc', all_s), ('ab', set(s_a+s_b)),
                               ('ac', set(s_a+s_c)), ('bc', set(s_b+s_c)),
                               ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
            bl2 = other | (all_s - open_set)
            a = lat.propagate_l2(field_f, K, bl2)
            probs[key] = np.array([abs(a[d])**2 for d in det])
        I3 = 0; P = 0
        for di in range(len(det)):
            i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
                  - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else float('nan')
    print(f"  Born: {born:.2e} ({'PASS' if born < 1e-10 else 'FAIL'}) ({time.time()-t1:.1f}s)")

    # Distance law
    max_z = min(int(phys_w * 0.85), lat.hw)
    z_values = list(range(2, max_z + 1))
    b_data = []; d_data = []
    for z_mass in z_values:
        t1 = time.time()
        fm, mi = make_field(lat, z_mass, strength)
        if mi is None:
            print(f"    z={z_mass}: no mass node")
            continue
        am = lat.propagate_l2(fm, K, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        dt = time.time() - t1
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            sign = "T" if delta > 0 else "A"
            print(f"    z={z_mass}: {delta:+.6f} ({sign}) [{dt:.1f}s]")
            if delta > 0:
                b_data.append(z_mass); d_data.append(delta)

    print(f"  TOWARD: {len(b_data)}/{len(z_values)}")

    if len(b_data) >= 3:
        b_arr = np.array(b_data, dtype=float)
        d_arr = np.array(d_data, dtype=float)
        # Find peak
        peak_i = np.argmax(d_arr)
        # Fit tail
        if peak_i < len(b_data) - 2:
            tail_b = b_arr[peak_i:]
            tail_d = d_arr[peak_i:]
            slope, r2 = fit_power(tail_b, tail_d)
            if slope is not None:
                print(f"  TAIL (z>={b_data[peak_i]}): b^({slope:.2f}), R²={r2:.3f}")
        # Fit all
        slope2, r22 = fit_power(b_arr, d_arr)
        if slope2 is not None:
            print(f"  ALL: b^({slope2:.2f}), R²={r22:.3f}")

    # MI + Decoherence (quick)
    pa = lat.propagate_l2(field_f, K, blocked | set(sb))
    pb = lat.propagate_l2(field_f, K, blocked | set(sa))
    bw = 2 * (phys_w + 1) / N_YBINS
    prob_a = np.zeros(N_YBINS); prob_b = np.zeros(N_YBINS)
    for d in det:
        b2 = max(0, min(N_YBINS-1, int((pos[d, 1] + phys_w + 1) / bw)))
        prob_a[b2] += abs(pa[d])**2; prob_b[b2] += abs(pb[d])**2
    na3 = prob_a.sum(); nb3 = prob_b.sum()
    MI = 0
    if na3 > 1e-30 and nb3 > 1e-30:
        pa_n = prob_a / na3; pb_n = prob_b / nb3
        H = 0; Hc = 0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30: H -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30: Hc -= 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30: Hc -= 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        MI = H - Hc
    print(f"  MI: {MI:.4f} bits")

    # d_TV
    da = {d: abs(pa[d])**2 for d in det}
    db = {d: abs(pb[d])**2 for d in det}
    na2 = sum(da.values()); nb2 = sum(db.values())
    dtv = 0
    if na2 > 1e-30 and nb2 > 1e-30:
        dtv = 0.5 * sum(abs(da[d]/na2 - db[d]/nb2) for d in det)
    print(f"  d_TV: {dtv:.4f}")

    # Decoherence
    ed = max(1, round(lat.nl/6)); st = bl + 1; sp = min(lat.nl-1, st + ed)
    mid = []
    for l in range(st, sp):
        mid.extend([lat.nmap[(l, iy, iz)] for iy in range(-lat.hw, lat.hw+1)
                    for iz in range(-lat.hw, lat.hw+1) if (l, iy, iz) in lat.nmap])
    ba = np.zeros(N_YBINS, dtype=np.complex128)
    bb = np.zeros(N_YBINS, dtype=np.complex128)
    for m in mid:
        b2 = max(0, min(N_YBINS-1, int((pos[m, 1] + phys_w + 1) / bw)))
        ba[b2] += pa[m]; bb[b2] += pb[m]
    S = float(np.sum(np.abs(ba - bb)**2))
    NA3 = float(np.sum(np.abs(ba)**2)); NB3 = float(np.sum(np.abs(bb)**2))
    Sn = S / (NA3 + NB3) if (NA3 + NB3) > 0 else 0
    Dcl = math.exp(-LAM**2 * Sn)
    rho = {}
    for d1 in det:
        for d2 in det:
            rho[(d1,d2)] = (pa[d1].conjugate()*pa[d2] + pb[d1].conjugate()*pb[d2]
                           + Dcl*pa[d1].conjugate()*pb[d2] + Dcl*pb[d1].conjugate()*pa[d2])
    tr = sum(rho[(d,d)] for d in det).real
    pur = 1.0
    if tr > 1e-30:
        for key in rho: rho[key] /= tr
        pur = sum(abs(v)**2 for v in rho.values()).real
    print(f"  Decoherence: {100*(1-pur):.1f}%")

    total = time.time() - t0
    print(f"  TOTAL: {total:.0f}s")


def main():
    s = 5e-5

    print("3D 1/L^2 KERNEL: CONVERGENCE TEST")
    print("Does the distance tail steepen toward -2 at finer h?")

    # h=0.5 baseline (fast)
    run_test(12, 6, 3, 0.5, s)

    # h=0.25 (the key test)
    run_test(12, 6, 3, 0.25, s)

    print("\n" + "=" * 60)
    print("CONVERGENCE: tail exponent should steepen toward -2.0")
    print("=" * 60)


if __name__ == "__main__":
    main()
