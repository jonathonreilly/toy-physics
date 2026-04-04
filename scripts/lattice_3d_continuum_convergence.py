#!/usr/bin/env python3
"""3D dense lattice: continuum convergence of distance law, F∝M, and signal speed.

Key question: as h→0, does the distance exponent converge to -2 (Newtonian)?

The challenge: RG scaling s=s₀/h² can push the field past the linear
distance-law regime at fine spacing. Solution: at each h, scan field
strengths to find the linear regime, then compare exponents.

Tests:
  1. Distance exponent at h=1.0, 0.5 (match field strengths to linear regime)
  2. F∝M scaling at h=1.0, 0.5
  3. Signal speed (group velocity) at h=1.0, 0.5
"""

from __future__ import annotations
import math
import cmath
import time
from collections import defaultdict

BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_W = 6
MAX_D = 3


def generate(phys_l, h=1.0):
    nl = int(phys_l / h) + 1
    hw = int(PHYS_W / h)
    max_d = max(1, round(MAX_D / h))  # Keep physical reach ~3 units at any h
    pos = []
    adj = defaultdict(list)
    nmap = {}
    for layer in range(nl):
        x = layer * h
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                idx = len(pos)
                pos.append((x, iy * h, iz * h))
                nmap[(layer, iy, iz)] = idx
    for layer in range(nl - 1):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer, iy, iz))
                if si is None:
                    continue
                for diy in range(-max_d, max_d + 1):
                    iyn = iy + diy
                    if abs(iyn) > hw:
                        continue
                    for diz in range(-max_d, max_d + 1):
                        izn = iz + diz
                        if abs(izn) > hw:
                            continue
                        di = nmap.get((layer + 1, iyn, izn))
                        if di is not None:
                            adj[si].append(di)
    return pos, dict(adj), nl, hw, nmap


def propagate(pos, adj, field, k, blocked, n):
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    src = next(i for i, p in enumerate(pos)
               if abs(p[0]) < 1e-10 and abs(p[1]) < 1e-10 and abs(p[2]) < 1e-10)
    amps[src] = 1.0
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            pi, pj = pos[i], pos[j]
            dx = pj[0] - pi[0]
            dy = pj[1] - pi[1]
            dz = pj[2] - pi[2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * cmath.exp(1j * k * act) * w / L
    return amps


def make_field(pos, nmap, gl, z_mass_phys, n, strength, h=1.0):
    """z_mass_phys is in PHYSICAL units. Convert to lattice index via /h."""
    iz = round(z_mass_phys / h)
    mi = nmap.get((gl, 0, iz))
    if mi is None:
        for dz in range(10):
            for sign in [1, -1]:
                mi = nmap.get((gl, 0, iz + sign * dz))
                if mi is not None:
                    break
            if mi is not None:
                break
    if mi is None:
        return [0.0] * n, None
    field = [0.0] * n
    mx, my, mz = pos[mi]
    for i in range(n):
        pi = pos[i]
        r = math.sqrt((pi[0]-mx)**2 + (pi[1]-my)**2 + (pi[2]-mz)**2) + 0.1
        field[i] = strength / r
    return field, mi


def setup_slits(pos, nmap, nl, hw):
    bl = nl // 3
    bi = []
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((bl, iy, iz))
            if idx is not None:
                bi.append(idx)
    sa = [i for i in bi if pos[i][1] >= 0.5]
    sb = [i for i in bi if pos[i][1] <= -0.5]
    blocked = set(bi) - set(sa + sb)
    return bi, sa, sb, blocked, bl


def measure_distance_law(pos, adj, nmap, nl, hw, blocked, det, gl, n, h, strength):
    """Measure distance exponent at given field strength."""
    field_f = [0.0] * n
    af = propagate(pos, adj, field_f, K, blocked, n)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return None, None, None, None, []
    zf = sum(abs(af[d])**2 * pos[d][2] for d in det) / pf

    # Max z_mass depends on hw (physical width)
    max_z = min(int(PHYS_W * 0.8), int(hw * h * 0.8))
    # z=1 is near-field, exclude from fit. Use z=2..5
    z_values = [z for z in [2, 3, 4, 5] if z <= max_z]
    if len(z_values) < 3:
        z_values = [z for z in range(2, max_z + 1)]

    b_data = []
    d_data = []
    directions = []
    details = []
    for z_mass in z_values:
        field_m, _ = make_field(pos, nmap, gl, z_mass, n, strength, h)
        am = propagate(pos, adj, field_m, K, blocked, n)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
            delta = zm - zf
            d_str = "TOWARD" if delta > 0 else "AWAY"
            directions.append(d_str)
            details.append((z_mass, delta, d_str))
            if delta > 0:
                b_data.append(z_mass)
                d_data.append(delta)

    n_toward = sum(1 for d in directions if d == "TOWARD")

    if len(b_data) >= 3:
        lx = [math.log(b) for b in b_data]
        ly = [math.log(d) for d in d_data]
        nn2 = len(lx)
        mx_l = sum(lx) / nn2
        my_l = sum(ly) / nn2
        sxx = sum((x - mx_l)**2 for x in lx)
        sxy = sum((x - mx_l) * (y - my_l) for x, y in zip(lx, ly))
        slope = sxy / sxx if sxx > 1e-10 else 0
        ss_res = sum((y - (my_l + slope * (x - mx_l)))**2 for x, y in zip(lx, ly))
        ss_tot = sum((y - my_l)**2 for y in ly)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        return slope, r2, n_toward, len(directions), details

    return None, None, n_toward, len(directions), details


def measure_fm(pos, adj, nmap, nl, hw, blocked, det, gl, n, h, base_strength):
    """Measure F∝M scaling."""
    field_f = [0.0] * n
    af = propagate(pos, adj, field_f, K, blocked, n)
    pf = sum(abs(af[d])**2 for d in det)
    if pf < 1e-30:
        return None
    zf = sum(abs(af[d])**2 * pos[d][2] for d in det) / pf

    m_data = []
    g_data = []
    z_mass = min(3, int(PHYS_W * 0.5))
    for factor in [0.02, 0.05, 0.1, 0.2, 0.5, 1.0]:
        s = base_strength * factor
        field_m, _ = make_field(pos, nmap, gl, z_mass, n, s, h)
        am = propagate(pos, adj, field_m, K, blocked, n)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d][2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                m_data.append(s)
                g_data.append(delta)

    if len(m_data) >= 3:
        lx = [math.log(m) for m in m_data]
        ly = [math.log(g) for g in g_data]
        nn2 = len(lx)
        mx_l = sum(lx) / nn2
        my_l = sum(ly) / nn2
        sxx = sum((x - mx_l)**2 for x in lx)
        sxy = sum((x - mx_l) * (y - my_l) for x, y in zip(lx, ly))
        return sxy / sxx if sxx > 1e-10 else None
    return None


def measure_signal_speed(pos, adj, nmap, nl, hw, n, h):
    """Measure signal propagation speed via amplitude arrival time.

    Create a localized wave packet at layer 0, propagate with no barriers,
    and measure when the peak amplitude arrives at each layer.
    """
    field_f = [0.0] * n
    # Propagate from source with no barriers
    amps = propagate(pos, adj, field_f, K, set(), n)

    # For each layer, find total amplitude
    layer_amp = {}
    for layer in range(nl):
        total = 0
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                idx = nmap.get((layer, iy, iz))
                if idx is not None:
                    total += abs(amps[idx])**2
        if total > 1e-30:
            layer_amp[layer] = total

    if not layer_amp:
        return None

    # Peak layer (where amplitude is concentrated)
    peak_layer = max(layer_amp, key=layer_amp.get)
    # Signal reaches the detector (last layer with nonzero amplitude)
    layers_with_signal = [l for l, a in layer_amp.items() if a > 1e-20]
    if not layers_with_signal:
        return None

    max_layer = max(layers_with_signal)
    # "Speed" = how far the signal reaches divided by the number of layers
    # On NN lattice, max_speed = 1.0 (diagonal edge = sqrt(2) per step of h in x)
    # On dense lattice, max_speed = sqrt(1 + 2*max_d²) per step

    # Centroid position of the amplitude distribution
    total_amp = sum(layer_amp.values())
    centroid_layer = sum(l * a for l, a in layer_amp.items()) / total_amp
    phys_centroid = centroid_layer * h

    # The signal_speed is the ratio of transverse spread to longitudinal advance
    # Measure the RMS transverse spread at the peak layer
    amps_peak = []
    for iy in range(-hw, hw + 1):
        for iz in range(-hw, hw + 1):
            idx = nmap.get((peak_layer, iy, iz))
            if idx is not None:
                amps_peak.append((iy * h, iz * h, abs(amps[idx])**2))

    total_peak = sum(a for _, _, a in amps_peak)
    if total_peak < 1e-30:
        return None

    y_mean = sum(y * a for y, z, a in amps_peak) / total_peak
    z_mean = sum(z * a for y, z, a in amps_peak) / total_peak
    rms = math.sqrt(sum(((y - y_mean)**2 + (z - z_mean)**2) * a
                        for y, z, a in amps_peak) / total_peak)

    return {
        "peak_layer": peak_layer,
        "max_signal_layer": max_layer,
        "centroid_phys": phys_centroid,
        "rms_transverse": rms,
        "max_phys": max_layer * h,
    }


def main():
    print("=" * 90)
    print("3D DENSE LATTICE: CONTINUUM CONVERGENCE")
    print("  Distance exponent, F∝M, signal speed vs lattice spacing")
    print("=" * 90)
    print()

    phys_l = 12

    # --- Test 1: Distance law convergence ---
    print("TEST 1: DISTANCE LAW EXPONENT vs SPACING")
    print("-" * 70)
    print()

    # At each h, scan field strengths to find the linear distance-law regime
    # The linear regime is where the exponent is negative (gravity decreases with b)
    for h in [1.0, 0.5]:
        t0 = time.time()
        pos, adj, nl, hw, nmap = generate(phys_l, h)
        n = len(pos)
        det = [nmap[(nl-1, iy, iz)] for iy in range(-hw, hw+1)
               for iz in range(-hw, hw+1) if (nl-1, iy, iz) in nmap]
        gl = 2 * nl // 3
        _, _, _, blocked, bl = setup_slits(pos, nmap, nl, hw)

        edges_per = len(adj.get(0, [])) if adj else 0
        print(f"  h={h}: {n} nodes, {2*hw+1}x{2*hw+1} cross-section, "
              f"~{edges_per} edges/node, {nl} layers")

        # Scan field strengths
        best_exp = None
        best_r2 = 0
        best_s = None
        best_toward = 0
        strengths = [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]
        for s in strengths:
            exp_val, r2, n_tw, n_tot, details = measure_distance_law(
                pos, adj, nmap, nl, hw, blocked, det, gl, n, h, s)
            tw_s = f"{n_tw}/{n_tot}" if n_tot else "?"
            if exp_val is not None:
                marker = " <-- LINEAR" if exp_val < 0 else ""
                det_str = " ".join(f"z={z}:{d:+.4f}({dr[0]})"
                                   for z, d, dr in details)
                print(f"    s={s:.0e}: exp={exp_val:+.2f}, R²={r2:.3f}, "
                      f"toward={tw_s}{marker}")
                print(f"      {det_str}")
                if exp_val < 0 and r2 > best_r2:
                    best_exp = exp_val
                    best_r2 = r2
                    best_s = s
                    best_toward = n_tw
            else:
                det_str = ""
                if details:
                    det_str = " | " + " ".join(
                        f"z={z}:{d:+.4f}({dr[0]})" for z, d, dr in details)
                print(f"    s={s:.0e}: too few TOWARD points (toward={tw_s}){det_str}")

        dt = time.time() - t0
        if best_exp is not None:
            print(f"  >> Best: exp={best_exp:+.2f}, R²={best_r2:.3f} at s={best_s:.0e} "
                  f"({dt:.0f}s)")
        else:
            print(f"  >> No negative exponent found ({dt:.0f}s)")
        print()

    # --- Test 2: F∝M convergence ---
    print()
    print("TEST 2: F∝M SCALING vs SPACING")
    print("-" * 70)
    print()

    for h in [1.0, 0.5]:
        t0 = time.time()
        pos, adj, nl, hw, nmap = generate(phys_l, h)
        n = len(pos)
        det = [nmap[(nl-1, iy, iz)] for iy in range(-hw, hw+1)
               for iz in range(-hw, hw+1) if (nl-1, iy, iz) in nmap]
        gl = 2 * nl // 3
        _, _, _, blocked, bl = setup_slits(pos, nmap, nl, hw)

        # Use a moderate base strength for F∝M
        for base_s in [5e-5, 1e-5]:
            alpha = measure_fm(pos, adj, nmap, nl, hw, blocked, det, gl, n, h, base_s)
            if alpha is not None:
                print(f"  h={h}, base_s={base_s:.0e}: F∝M alpha = {alpha:.3f} "
                      f"{'(linear!)' if abs(alpha - 1.0) < 0.2 else ''}")
            else:
                print(f"  h={h}, base_s={base_s:.0e}: F∝M measurement failed")

        dt = time.time() - t0
        print(f"  ({dt:.0f}s)")
        print()

    # --- Test 3: Signal speed ---
    print()
    print("TEST 3: SIGNAL SPEED vs SPACING")
    print("-" * 70)
    print()

    for h in [1.0, 0.5]:
        t0 = time.time()
        pos, adj, nl, hw, nmap = generate(phys_l, h)
        n = len(pos)
        sig = measure_signal_speed(pos, adj, nmap, nl, hw, n, h)
        dt = time.time() - t0
        if sig:
            print(f"  h={h}: peak_layer={sig['peak_layer']}/{nl-1}, "
                  f"max_signal={sig['max_signal_layer']}/{nl-1}")
            print(f"         centroid={sig['centroid_phys']:.2f}/{phys_l}, "
                  f"rms_transverse={sig['rms_transverse']:.3f}")
            print(f"         max_phys_reach={sig['max_phys']:.1f}/{phys_l}")
        else:
            print(f"  h={h}: signal measurement failed")
        print(f"  ({dt:.0f}s)")
        print()

    # --- Summary ---
    print()
    print("=" * 90)
    print("CONVERGENCE SUMMARY")
    print("  Newtonian prediction: distance exponent → -2.0 as h → 0")
    print("  Linear mass: F∝M alpha → 1.0 as h → 0")
    print("  Signal speed: should be h-independent (physical speed)")
    print("=" * 90)


if __name__ == "__main__":
    main()
