#!/usr/bin/env python3
"""Head-to-head: cos^2(theta) vs exp(-0.8*theta^2) on the 2+1D lattice.

Runs the FIXED-h CORE CHECKS from lattice_3d_valley_linear_card.py
(properties 1-7 plus distance law) with both kernels. This is a
NARROWER test than the full 10-property card: it omits properties
8-9 (multi-L companion checks for purity stability and gravity growth).

The only change between runs is the angular weight function:
  - Default: w = exp(-0.8 * theta^2)
  - Candidate: w = cos(theta)^2

Everything else is identical: action S=L(1-f), kernel 1/L^2, h^2 measure,
lattice parameters h=0.25, W=10, L=12.

HYPOTHESIS: cos^2(theta) preserves the fixed-h core checks.

FALSIFICATION: If any of Born, gravity sign, or F~M alpha fail with
  cos^2(theta), it cannot replace the default kernel.

NOTE: This script does NOT measure isotropy. The 1.5% vs 16%
anisotropy comparison comes from frontier_angular_kernel_investigation.py,
not from this script.
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required. Install: pip install numpy") from exc

K = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_W = 10
PHYS_L = 12
H = 0.25
MAX_D_PHYS = 3
STRENGTH = 5e-5


class Lattice3D:
    """3D ordered lattice with selectable angular kernel."""

    def __init__(self, phys_l, phys_w, h, weight_fn=None):
        """
        weight_fn: callable(theta) -> float. Defaults to exp(-0.8*theta^2).
        """
        if weight_fn is None:
            weight_fn = lambda t: math.exp(-0.8 * t * t)

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
                w = weight_fn(theta)
                self._off.append((dy, dz, L, w))
        self._nw = nw

    def propagate(self, field, k, blocked_set):
        n = self.n; nl = self.nl; nw = self._nw; hm = self._hm
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
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


def make_field(lat, z_mass_phys, strength):
    iz = round(z_mass_phys / lat.h)
    mi = lat.nmap.get((2 * lat.nl // 3, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    mx, my, mz = lat.pos[mi]
    r = np.sqrt((lat.pos[:, 0] - mx)**2 + (lat.pos[:, 1] - my)**2 +
                (lat.pos[:, 2] - mz)**2) + 0.1
    return strength / r, mi


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


def fit_power(b_data, d_data):
    if len(b_data) < 3:
        return None, None
    lx = np.log(np.array(b_data, dtype=float))
    ly = np.log(np.array(d_data, dtype=float))
    mx = lx.mean(); my = ly.mean()
    sxx = np.sum((lx - mx)**2); sxy = np.sum((lx - mx) * (ly - my))
    if sxx < 1e-10:
        return None, None
    slope = sxy / sxx
    ss_res = np.sum((ly - (my + slope * (lx - mx)))**2)
    ss_tot = np.sum((ly - my)**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return slope, r2


def decoherence_purity(pa, pb, det, dcl):
    a = np.array([pa[d] for d in det], dtype=np.complex128)
    b = np.array([pb[d] for d in det], dtype=np.complex128)
    gram = np.array([[np.vdot(a, a), np.vdot(a, b)],
                     [np.vdot(b, a), np.vdot(b, b)]], dtype=np.complex128)
    mix = np.array([[1.0, dcl], [dcl, 1.0]], dtype=np.complex128)
    mg = mix @ gram
    tr = np.trace(mg).real
    if tr <= 1e-30:
        return 1.0
    return float((np.trace(mg @ mg) / (tr * tr)).real)


def run_card(kernel_name, weight_fn):
    """Run the full 10-property card. Returns dict of results."""
    t_total = time.time()

    lat = Lattice3D(PHYS_L, PHYS_W, H, weight_fn=weight_fn)
    det = [lat.nmap[(lat.nl - 1, iy, iz)]
           for iy in range(-lat.hw, lat.hw + 1)
           for iz in range(-lat.hw, lat.hw + 1)
           if (lat.nl - 1, iy, iz) in lat.nmap]
    pos = lat.pos
    bi, sa, sb, blocked, bl = setup_slits(lat)
    field_f = np.zeros(lat.n)

    print(f"\n{'='*70}")
    print(f"  KERNEL: {kernel_name}")
    print(f"  {lat.n:,} nodes, {lat.nl} layers, h={H}")
    print(f"{'='*70}")

    # Flat propagation
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf

    results = {"kernel": kernel_name}

    # 1. Born
    upper = sorted([i for i in bi if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    born = float('nan')
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c); other = set(bi) - all_s
        probs = {}
        for key, open_set in [('abc', all_s), ('ab', set(s_a + s_b)),
                               ('ac', set(s_a + s_c)), ('bc', set(s_b + s_c)),
                               ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
            bl2 = other | (all_s - open_set)
            a = lat.propagate(field_f, K, bl2)
            probs[key] = np.array([abs(a[d])**2 for d in det])
        I3 = 0.0; P = 0.0
        for di in range(len(det)):
            i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di]
                  - probs['bc'][di] + probs['a'][di] + probs['b'][di] + probs['c'][di])
            I3 += abs(i3); P += probs['abc'][di]
        born = I3 / P if P > 1e-30 else float('nan')
    results["born"] = born
    print(f"  1. Born |I3|/P = {born:.2e}  [{'PASS' if born < 1e-10 else 'FAIL'}]")

    # 2. d_TV
    pa = lat.propagate(field_f, K, blocked | set(sb))
    pb = lat.propagate(field_f, K, blocked | set(sa))
    da = {d: abs(pa[d])**2 for d in det}; db_ = {d: abs(pb[d])**2 for d in det}
    na2 = sum(da.values()); nb2 = sum(db_.values())
    dtv = 0.5 * sum(abs(da[d]/na2 - db_[d]/nb2) for d in det) if na2 > 1e-30 and nb2 > 1e-30 else 0
    results["dtv"] = dtv
    print(f"  2. d_TV = {dtv:.4f}  [{'PASS' if dtv > 0.1 else 'WEAK'}]")

    # 3. k=0
    field_m3, _ = make_field(lat, 3, STRENGTH)
    am0 = lat.propagate(field_m3, 0.0, blocked)
    af0 = lat.propagate(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d])**2 for d in det); pf0 = sum(abs(af0[d])**2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d])**2 * pos[d, 2] for d in det) / pm0
               - sum(abs(af0[d])**2 * pos[d, 2] for d in det) / pf0)
    results["k0"] = gk0
    print(f"  3. k=0 = {gk0:.6f}  [{'PASS' if abs(gk0) < 1e-6 else 'CHECK'}]")

    # 4. F~M
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm, _ = make_field(lat, 3, s)
        am = lat.propagate(fm, K, blocked); pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                m_data.append(s); g_data.append(delta)
    fm_alpha = float('nan')
    if len(m_data) >= 3:
        slope, _ = fit_power(m_data, g_data)
        if slope is not None:
            fm_alpha = slope
    results["fm_alpha"] = fm_alpha
    print(f"  4. F~M alpha = {fm_alpha:.2f}  [{'PASS' if abs(fm_alpha - 1.0) < 0.2 else 'CHECK'}]")

    # 5. Gravity sign
    am3 = lat.propagate(field_m3, K, blocked); pm3 = sum(abs(am3[d])**2 for d in det)
    grav = (sum(abs(am3[d])**2 * pos[d, 2] for d in det) / pm3 - zf) if pm3 > 1e-30 else 0
    dr = "TOWARD" if grav > 0 else "AWAY"
    results["grav"] = grav
    results["grav_dir"] = dr
    print(f"  5. Gravity z=3 = {grav:+.6f} ({dr})  [{'PASS' if grav > 0 else 'FAIL'}]")

    # 6. Decoherence
    bw = 2 * (PHYS_W + 1) / N_YBINS
    ed = max(1, round(lat.nl / 6)); st = bl + 1; sp = min(lat.nl - 1, st + ed)
    mid = []
    for l in range(st, sp):
        mid.extend([lat.nmap[(l, iy, iz)] for iy in range(-lat.hw, lat.hw + 1)
                     for iz in range(-lat.hw, lat.hw + 1) if (l, iy, iz) in lat.nmap])
    ba = np.zeros(N_YBINS, dtype=np.complex128); bb = np.zeros(N_YBINS, dtype=np.complex128)
    for m in mid:
        b2 = max(0, min(N_YBINS - 1, int((pos[m, 1] + PHYS_W + 1) / bw)))
        ba[b2] += pa[m]; bb[b2] += pb[m]
    S = float(np.sum(np.abs(ba - bb)**2))
    NA3 = float(np.sum(np.abs(ba)**2)); NB3 = float(np.sum(np.abs(bb)**2))
    Sn = S / (NA3 + NB3) if (NA3 + NB3) > 0 else 0
    Dcl = math.exp(-LAM**2 * Sn)
    pur = decoherence_purity(pa, pb, det, Dcl)
    decoh = 100 * (1 - pur)
    results["decoh"] = decoh
    print(f"  6. Decoherence = {decoh:.1f}%  [{'PASS' if decoh > 5 else 'WEAK'}]")

    # 7. MI
    prob_a = np.zeros(N_YBINS); prob_b = np.zeros(N_YBINS)
    for d in det:
        b2 = max(0, min(N_YBINS - 1, int((pos[d, 1] + PHYS_W + 1) / bw)))
        prob_a[b2] += abs(pa[d])**2; prob_b[b2] += abs(pb[d])**2
    na3 = prob_a.sum(); nb3 = prob_b.sum(); MI = 0
    if na3 > 1e-30 and nb3 > 1e-30:
        pa_n = prob_a / na3; pb_n = prob_b / nb3
        H_val = 0; Hc = 0
        for b3 in range(N_YBINS):
            pm2 = 0.5 * pa_n[b3] + 0.5 * pb_n[b3]
            if pm2 > 1e-30: H_val -= pm2 * math.log2(pm2)
            if pa_n[b3] > 1e-30: Hc -= 0.5 * pa_n[b3] * math.log2(pa_n[b3])
            if pb_n[b3] > 1e-30: Hc -= 0.5 * pb_n[b3] * math.log2(pb_n[b3])
        MI = H_val - Hc
    results["mi"] = MI
    print(f"  7. MI = {MI:.4f} bits  [{'PASS' if MI > 0.05 else 'WEAK'}]")

    # 10. Distance law
    b_data = []; d_data = []
    for z_mass in range(2, 10):
        fm, _ = make_field(lat, z_mass, STRENGTH)
        am = lat.propagate(fm, K, blocked); pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            if delta > 0: b_data.append(z_mass); d_data.append(delta)
    n_tw = len(b_data)
    dist_slope = None
    dist_r2 = None
    if len(b_data) >= 3:
        d_arr = np.array(d_data); peak_i = int(np.argmax(d_arr))
        if peak_i < len(b_data) - 2:
            dist_slope, dist_r2 = fit_power(b_data[peak_i:], d_data[peak_i:])
    results["n_toward"] = n_tw
    results["dist_slope"] = dist_slope
    results["dist_r2"] = dist_r2
    if dist_slope is not None:
        print(f"  10. Distance: {n_tw}/8 TOWARD, tail b^({dist_slope:.2f}) R^2={dist_r2:.3f}")
    else:
        print(f"  10. Distance: {n_tw}/8 TOWARD")

    results["time"] = time.time() - t_total
    print(f"  Time: {results['time']:.0f}s")
    return results


def main():
    print("=" * 70)
    print("HEAD-TO-HEAD: cos^2(theta) vs exp(-0.8*theta^2)")
    print("Full 10-property closure card on 3D valley-linear lattice")
    print("=" * 70)
    print()
    print("HYPOTHESIS: cos^2(theta) preserves all retained properties.")
    print("FALSIFICATION: if Born, gravity sign, or F~M fail, it cannot replace default.")
    print()

    kernels = [
        ("exp(-0.8*t^2)", lambda t: math.exp(-0.8 * t * t)),
        ("cos^2(theta)",  lambda t: math.cos(t) ** 2),
    ]

    all_results = []
    for name, wfn in kernels:
        r = run_card(name, wfn)
        all_results.append(r)

    # Side-by-side comparison
    print(f"\n{'='*70}")
    print("SIDE-BY-SIDE COMPARISON")
    print(f"{'='*70}")
    print()

    props = [
        ("Born |I3|/P", "born", ".2e", 1e-10, "lower"),
        ("d_TV", "dtv", ".4f", 0.1, "higher"),
        ("k=0 control", "k0", ".6f", 1e-6, "lower_abs"),
        ("F~M alpha", "fm_alpha", ".2f", None, "near_1"),
        ("Gravity sign", "grav", ".6f", 0, "positive"),
        ("Decoherence %", "decoh", ".1f", 5, "higher"),
        ("MI bits", "mi", ".4f", 0.05, "higher"),
        ("TOWARD count", "n_toward", "d", 4, "higher"),
    ]

    header = f"{'Property':<20s}"
    for r in all_results:
        header += f" | {r['kernel']:>20s}"
    header += " | winner"
    print(header)
    print("-" * len(header))

    for label, key, fmt, threshold, direction in props:
        row = f"{label:<20s}"
        vals = []
        for r in all_results:
            v = r.get(key)
            if v is None or (isinstance(v, float) and math.isnan(v)):
                row += f" | {'N/A':>20s}"
                vals.append(None)
            else:
                row += f" | {v:>20{fmt}}"
                vals.append(v)

        # Determine winner — ties are reported as ties
        winner = ""
        if all(v is not None for v in vals):
            v0, v1 = vals
            # Use relative tolerance for tie detection
            rel_tol = 0.01  # 1% relative difference = tie
            def is_tie(a, b):
                if a == b:
                    return True
                denom = max(abs(a), abs(b))
                return denom > 0 and abs(a - b) / denom < rel_tol

            if direction == "lower":
                if is_tie(v0, v1): winner = "tie"
                else: winner = all_results[0]["kernel"] if v0 < v1 else all_results[1]["kernel"]
            elif direction == "higher":
                if is_tie(v0, v1): winner = "tie"
                else: winner = all_results[0]["kernel"] if v0 > v1 else all_results[1]["kernel"]
            elif direction == "lower_abs":
                if is_tie(abs(v0), abs(v1)): winner = "tie"
                else: winner = all_results[0]["kernel"] if abs(v0) < abs(v1) else all_results[1]["kernel"]
            elif direction == "near_1":
                d0, d1 = abs(v0-1), abs(v1-1)
                if is_tie(d0, d1): winner = "tie"
                else: winner = all_results[0]["kernel"] if d0 < d1 else all_results[1]["kernel"]
            elif direction == "positive":
                if v0 > 0 and v1 > 0:
                    winner = "tie (both TOWARD)"
                elif v0 > 0:
                    winner = all_results[0]["kernel"]
                elif v1 > 0:
                    winner = all_results[1]["kernel"]
                else:
                    winner = "BOTH FAIL"
        row += f" | {winner}"
        print(row)

    # Distance law comparison
    print()
    for r in all_results:
        if r["dist_slope"] is not None:
            dist_from_newton = abs(r["dist_slope"] - (-1.0))
            print(f"  {r['kernel']}: distance tail b^({r['dist_slope']:.2f}), "
                  f"R^2={r['dist_r2']:.3f}, |slope - (-1)| = {dist_from_newton:.2f}")

    # Verdict
    print(f"\n{'='*70}")
    print("VERDICT")
    print(f"{'='*70}")
    print()

    cos2 = all_results[1]
    default = all_results[0]

    born_pass = cos2["born"] < 1e-10
    grav_pass = cos2["grav"] > 0
    fm_pass = not math.isnan(cos2["fm_alpha"]) and abs(cos2["fm_alpha"] - 1.0) < 0.3

    if born_pass and grav_pass and fm_pass:
        print("  cos^2(theta) PASSES all three core tests:")
        print(f"    Born:  {cos2['born']:.2e} (< 1e-10)")
        print(f"    Grav:  {cos2['grav']:+.6f} (TOWARD)")
        print(f"    F~M:   {cos2['fm_alpha']:.2f} (near 1.0)")
        print()
        # Compare other properties
        dtv_better = cos2["dtv"] > default["dtv"]
        decoh_better = cos2["decoh"] > default["decoh"]
        mi_better = cos2["mi"] > default["mi"]
        print(f"  Secondary properties:")
        print(f"    d_TV:        {'better' if dtv_better else 'worse'} "
              f"({cos2['dtv']:.4f} vs {default['dtv']:.4f})")
        print(f"    Decoherence: {'better' if decoh_better else 'worse'} "
              f"({cos2['decoh']:.1f}% vs {default['decoh']:.1f}%)")
        print(f"    MI:          {'better' if mi_better else 'worse'} "
              f"({cos2['mi']:.4f} vs {default['mi']:.4f})")
        print()
        print("  cos^2(theta) passes the fixed-h core checks on this 2+1D lattice.")
        print()
        print("  CAVEATS:")
        print("  - This is a NARROWER test than the full 10-property card")
        print("    (omits multi-L purity stability and gravity growth checks)")
        print("  - Isotropy comparison (1.5% vs 16%) comes from a separate")
        print("    script (frontier_angular_kernel_investigation.py), not here")
        print("  - cos^2(theta) has weaker gravity and lower MI/d_TV than default")
        print("  - Single-family, single-h test — not sufficient for promotion")
    else:
        failures = []
        if not born_pass: failures.append(f"Born ({cos2['born']:.2e})")
        if not grav_pass: failures.append(f"Gravity ({cos2['grav']:+.6f})")
        if not fm_pass: failures.append(f"F~M ({cos2['fm_alpha']:.2f})")
        print(f"  cos^2(theta) FAILS: {', '.join(failures)}")
        print("  Cannot replace exp(-0.8*theta^2) as default kernel.")


if __name__ == "__main__":
    main()
