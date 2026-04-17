#!/usr/bin/env python3
"""frontier_3d_laplacian_closure.py

CRITICAL GAP: Every 3D lattice result uses analytic 1/r fields. Nobody has
tested with a SELF-CONSISTENT Laplacian field solver. The 2D infrastructure
has derive_node_field (Laplacian relaxation from persistent nodes), but the
3D infrastructure doesn't.

This script:
  1. Builds a 2D Laplacian relaxation solver for the spatial (iy, iz) plane
     (both nonlinear matching derive_node_field and linear variant)
  2. Compares field profiles: analytic 1/r vs nonlinear Laplacian vs linear Laplacian
  3. Reruns the closure card (Born, k=0, gravity sign, F~M) using each field type
  4. Head-to-head comparison table

HYPOTHESIS: "The Laplacian field gives the same gravity direction and similar
  F~M as the analytic field."
FALSIFICATION: "If gravity sign flips or F~M deviates by >30%, the analytic
  field is misleading."
"""

from __future__ import annotations
import math
import time

try:
    import numpy as np
except ModuleNotFoundError as exc:
    raise SystemExit("numpy is required.") from exc

# --- Constants (match lattice_3d_valley_linear_card.py) ---
BETA = 0.8
K = 5.0
LAM = 10.0
N_YBINS = 8
PHYS_W = 6
PHYS_L = 12
H = 0.5
MAX_D_PHYS = 3
STRENGTH = 5e-5


# ======================================================================
# Lattice3D (identical to valley_linear_card)
# ======================================================================

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
                act = L * (1 - lf)
                c = a[nz] * np.exp(1j * k * act) * w * hm / (L * L)
                c[db[di[nz]]] = 0
                np.add.at(amps[ld:ld + self.npl], di[nz], c)
        return amps


# ======================================================================
# Field solvers
# ======================================================================

def make_field_analytic(lat, z_mass_phys, strength):
    """Analytic 1/r field centered on a spatial mass position."""
    iz = round(z_mass_phys / lat.h)
    gl = 2 * lat.nl // 3
    mi = lat.nmap.get((gl, 0, iz))
    if mi is None:
        return np.zeros(lat.n), None
    mx, my, mz = lat.pos[mi]
    r = np.sqrt((lat.pos[:, 0] - mx)**2 + (lat.pos[:, 1] - my)**2 +
                (lat.pos[:, 2] - mz)**2) + 0.1
    return strength / r, mi


def solve_laplacian_nonlinear(lat, z_mass_phys, strength, tol=1e-8, max_iter=400):
    """Nonlinear Laplacian relaxation on 2D spatial plane, broadcast to all layers.

    Matches the 2D derive_node_field logic:
      field[i] = support[i] * strength + (1 - support[i]) * avg(neighbors)
    where support = 1 at the mass position, 0 elsewhere.
    Boundary: field = 0 at edges (|iy| = hw or |iz| = hw).
    """
    hw = lat.hw
    nw = 2 * hw + 1
    iz_mass = round(z_mass_phys / lat.h)

    # Source: single mass at (iy=0, iz=iz_mass)
    support = np.zeros((nw, nw))
    yi_mass = 0 + hw  # iy=0 -> array index hw
    zi_mass = iz_mass + hw
    if 0 <= zi_mass < nw:
        support[yi_mass, zi_mass] = 1.0

    # Laplacian relaxation (4-connectivity for standard discrete Laplacian)
    field_2d = support.copy() * strength
    for it in range(max_iter):
        old = field_2d.copy()
        for yi in range(1, nw - 1):
            for zi in range(1, nw - 1):
                avg = (field_2d[yi + 1, zi] + field_2d[yi - 1, zi] +
                       field_2d[yi, zi + 1] + field_2d[yi, zi - 1]) / 4.0
                field_2d[yi, zi] = support[yi, zi] * strength + (1.0 - support[yi, zi]) * avg
        # Boundary = 0 (already zero at edges since we skip them)
        if np.max(np.abs(field_2d - old)) < tol:
            break

    # Broadcast to all layers
    field = np.zeros(lat.n)
    for layer in range(lat.nl):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                idx = lat.nmap.get((layer, iy, iz))
                if idx is not None:
                    field[idx] = field_2d[iy + hw, iz + hw]
    return field


def solve_laplacian_linear(lat, z_mass_phys, strength, tol=1e-8, max_iter=400):
    """Linear Laplacian relaxation: field = source + avg(neighbors).

    Unlike the nonlinear version, there is no (1-support) coupling.
    field[i] = support[i] * strength + avg(neighbors)
    This is a standard Poisson equation with source term.
    Boundary: field = 0 at edges.
    """
    hw = lat.hw
    nw = 2 * hw + 1
    iz_mass = round(z_mass_phys / lat.h)

    support = np.zeros((nw, nw))
    yi_mass = 0 + hw
    zi_mass = iz_mass + hw
    if 0 <= zi_mass < nw:
        support[yi_mass, zi_mass] = 1.0

    # Linear relaxation (Gauss-Seidel for Laplace with source)
    field_2d = support.copy() * strength
    for it in range(max_iter):
        old = field_2d.copy()
        for yi in range(1, nw - 1):
            for zi in range(1, nw - 1):
                avg = (field_2d[yi + 1, zi] + field_2d[yi - 1, zi] +
                       field_2d[yi, zi + 1] + field_2d[yi, zi - 1]) / 4.0
                field_2d[yi, zi] = support[yi, zi] * strength + avg
        # Boundary = 0
        field_2d[0, :] = 0; field_2d[-1, :] = 0
        field_2d[:, 0] = 0; field_2d[:, -1] = 0
        if np.max(np.abs(field_2d - old)) < tol:
            break

    field = np.zeros(lat.n)
    for layer in range(lat.nl):
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                idx = lat.nmap.get((layer, iy, iz))
                if idx is not None:
                    field[idx] = field_2d[iy + hw, iz + hw]
    return field


# ======================================================================
# Slit setup
# ======================================================================

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


# ======================================================================
# Run closure tests for a given field type
# ======================================================================

def run_closure(lat, det, blocked, sa, sb, zf, field_fn, label):
    """Run Born, k=0, gravity sign, F~M for one field type."""
    pos = lat.pos
    bi_all, _, _, _, bl = setup_slits(lat)

    results = {}

    # 1. Born (field-independent, but run for completeness)
    upper = sorted([i for i in bi_all if pos[i, 1] > 1], key=lambda i: pos[i, 1])
    lower = sorted([i for i in bi_all if pos[i, 1] < -1], key=lambda i: -pos[i, 1])
    middle = [i for i in bi_all if abs(pos[i, 1]) <= 1 and abs(pos[i, 2]) <= 1]
    field_f = np.zeros(lat.n)
    born = float('nan')
    if upper and lower and middle:
        s_a, s_b, s_c = [upper[0]], [lower[0]], [middle[0]]
        all_s = set(s_a + s_b + s_c); other = set(bi_all) - all_s
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
    results['born'] = born

    # 2. k=0 control
    field_m3 = field_fn(lat, 3, STRENGTH)
    am0 = lat.propagate(field_m3, 0.0, blocked)
    af0 = lat.propagate(field_f, 0.0, blocked)
    pm0 = sum(abs(am0[d])**2 for d in det)
    pf0 = sum(abs(af0[d])**2 for d in det)
    gk0 = 0
    if pm0 > 1e-30 and pf0 > 1e-30:
        gk0 = (sum(abs(am0[d])**2 * pos[d, 2] for d in det) / pm0
               - sum(abs(af0[d])**2 * pos[d, 2] for d in det) / pf0)
    results['k0'] = gk0

    # 3. Gravity sign at z=3
    am3 = lat.propagate(field_m3, K, blocked)
    pm3 = sum(abs(am3[d])**2 for d in det)
    grav = (sum(abs(am3[d])**2 * pos[d, 2] for d in det) / pm3 - zf) if pm3 > 1e-30 else 0
    results['grav'] = grav

    # 4. F~M scaling
    m_data = []; g_data = []
    for s in [1e-6, 2e-6, 5e-6, 1e-5, 2e-5, 5e-5]:
        fm = field_fn(lat, 3, s)
        am = lat.propagate(fm, K, blocked)
        pm = sum(abs(am[d])**2 for d in det)
        if pm > 1e-30:
            zm = sum(abs(am[d])**2 * pos[d, 2] for d in det) / pm
            delta = zm - zf
            if delta > 0:
                m_data.append(s)
                g_data.append(delta)
    fm_alpha = float('nan')
    if len(m_data) >= 3:
        slope, _ = fit_power(m_data, g_data)
        if slope is not None:
            fm_alpha = slope
    results['fm_alpha'] = fm_alpha

    return results


# ======================================================================
# Main
# ======================================================================

def main():
    t_total = time.time()

    print("=" * 72)
    print("FRONTIER: 3D LAPLACIAN CLOSURE TEST")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}")
    print(f"  Comparing: Analytic 1/r vs Nonlinear Laplacian vs Linear Laplacian")
    print("=" * 72)
    print()

    lat = Lattice3D(PHYS_L, PHYS_W, H)
    det = [lat.nmap[(lat.nl - 1, iy, iz)]
           for iy in range(-lat.hw, lat.hw + 1)
           for iz in range(-lat.hw, lat.hw + 1)
           if (lat.nl - 1, iy, iz) in lat.nmap]
    bi, sa, sb, blocked, bl = setup_slits(lat)
    pos = lat.pos

    print(f"  Lattice: {lat.n:,} nodes, {lat.nl} layers, nw={lat._nw}")
    print()

    # Free propagation (reference)
    field_f = np.zeros(lat.n)
    af = lat.propagate(field_f, K, blocked)
    pf = sum(abs(af[d])**2 for d in det)
    zf = sum(abs(af[d])**2 * pos[d, 2] for d in det) / pf
    print(f"  Free z-centroid: {zf:.6f}")
    print()

    # ------------------------------------------------------------------
    # PART 2: Field profile comparison
    # ------------------------------------------------------------------
    print("-" * 72)
    print("PART 2: Field profiles along z-axis at y=0 (mass at z=3)")
    print("-" * 72)

    z_mass = 3
    field_ana, _ = make_field_analytic(lat, z_mass, STRENGTH)

    t0 = time.time()
    field_nl = solve_laplacian_nonlinear(lat, z_mass, STRENGTH)
    t_nl = time.time() - t0

    t0 = time.time()
    field_lin = solve_laplacian_linear(lat, z_mass, STRENGTH)
    t_lin = time.time() - t0

    print(f"  Nonlinear Laplacian converged in {t_nl:.2f}s")
    print(f"  Linear Laplacian converged in {t_lin:.2f}s")
    print()

    # Profile along z-axis at y=0 for the middle-ish layer
    ref_layer = 2 * lat.nl // 3
    print(f"  Field profile at layer={ref_layer} (x={ref_layer*H:.1f}), iy=0:")
    print(f"  {'iz':>4s}  {'z_phys':>6s}  {'Analytic':>12s}  {'NL-Lapl':>12s}  {'Lin-Lapl':>12s}")
    for iz in range(-lat.hw, lat.hw + 1):
        idx = lat.nmap.get((ref_layer, 0, iz))
        if idx is not None:
            a_val = field_ana[idx]
            nl_val = field_nl[idx]
            li_val = field_lin[idx]
            print(f"  {iz:4d}  {iz*H:6.1f}  {a_val:12.6e}  {nl_val:12.6e}  {li_val:12.6e}")
    print()

    # Field statistics
    print("  Field statistics (all nodes):")
    for name, f in [("Analytic", field_ana), ("NL-Lapl", field_nl), ("Lin-Lapl", field_lin)]:
        print(f"    {name:12s}: max={np.max(f):.6e}, mean={np.mean(f):.6e}, "
              f"sum={np.sum(f):.6e}")
    print()

    # ------------------------------------------------------------------
    # PART 3: Closure card for each field type
    # ------------------------------------------------------------------
    print("-" * 72)
    print("PART 3: Closure card (Born, k=0, gravity, F~M)")
    print("-" * 72)
    print()

    def analytic_fn(lat, z, s):
        f, _ = make_field_analytic(lat, z, s)
        return f

    field_types = [
        ("Analytic 1/r", analytic_fn),
        ("NL-Laplacian", solve_laplacian_nonlinear),
        ("Lin-Laplacian", solve_laplacian_linear),
    ]

    all_results = {}
    for label, fn in field_types:
        t0 = time.time()
        print(f"  Running: {label}...")
        res = run_closure(lat, det, blocked, sa, sb, zf, fn, label)
        elapsed = time.time() - t0
        all_results[label] = res

        born_pass = "PASS" if res['born'] < 1e-10 else "FAIL"
        k0_pass = "PASS" if abs(res['k0']) < 1e-6 else "CHECK"
        grav_dir = "TOWARD" if res['grav'] > 0 else "AWAY"
        grav_pass = "PASS" if res['grav'] > 0 else "FAIL"
        fm_pass = "PASS" if abs(res['fm_alpha'] - 1.0) < 0.3 else "CHECK"

        print(f"    Born:      {res['born']:.2e}  [{born_pass}]")
        print(f"    k=0:       {res['k0']:.6f}  [{k0_pass}]")
        print(f"    Gravity:   {res['grav']:+.6f} ({grav_dir})  [{grav_pass}]")
        print(f"    F~M alpha: {res['fm_alpha']:.2f}  [{fm_pass}]")
        print(f"    ({elapsed:.0f}s)")
        print()

    # ------------------------------------------------------------------
    # PART 4: Head-to-head comparison table
    # ------------------------------------------------------------------
    print("-" * 72)
    print("PART 4: Head-to-head comparison")
    print("-" * 72)
    print()

    header = f"  {'Test':18s} | {'Analytic 1/r':>14s} | {'NL-Laplacian':>14s} | {'Lin-Laplacian':>14s}"
    print(header)
    print("  " + "-" * len(header.strip()))

    r_ana = all_results["Analytic 1/r"]
    r_nl = all_results["NL-Laplacian"]
    r_lin = all_results["Lin-Laplacian"]

    print(f"  {'Born |I3|/P':18s} | {r_ana['born']:14.2e} | {r_nl['born']:14.2e} | {r_lin['born']:14.2e}")
    print(f"  {'k=0 control':18s} | {r_ana['k0']:14.6f} | {r_nl['k0']:14.6f} | {r_lin['k0']:14.6f}")
    print(f"  {'Gravity z=3':18s} | {r_ana['grav']:+14.6f} | {r_nl['grav']:+14.6f} | {r_lin['grav']:+14.6f}")
    print(f"  {'F~M alpha':18s} | {r_ana['fm_alpha']:14.2f} | {r_nl['fm_alpha']:14.2f} | {r_lin['fm_alpha']:14.2f}")

    # Directions
    dirs = []
    for label in ["Analytic 1/r", "NL-Laplacian", "Lin-Laplacian"]:
        d = "TOWARD" if all_results[label]['grav'] > 0 else "AWAY"
        dirs.append(d)
    print(f"  {'Gravity dir':18s} | {dirs[0]:>14s} | {dirs[1]:>14s} | {dirs[2]:>14s}")
    print()

    # ------------------------------------------------------------------
    # Verdict
    # ------------------------------------------------------------------
    print("=" * 72)
    print("VERDICT")
    print("=" * 72)

    # Check: same gravity direction?
    ana_toward = r_ana['grav'] > 0
    nl_toward = r_nl['grav'] > 0
    lin_toward = r_lin['grav'] > 0

    same_dir_nl = ana_toward == nl_toward
    same_dir_lin = ana_toward == lin_toward

    print(f"  Gravity direction matches analytic?")
    print(f"    NL-Laplacian: {'YES' if same_dir_nl else 'NO -- FALSIFIED'}")
    print(f"    Lin-Laplacian: {'YES' if same_dir_lin else 'NO -- FALSIFIED'}")

    # Check: F~M within 30%?
    if not math.isnan(r_ana['fm_alpha']) and not math.isnan(r_nl['fm_alpha']):
        dev_nl = abs(r_nl['fm_alpha'] - r_ana['fm_alpha']) / abs(r_ana['fm_alpha']) * 100
        print(f"  F~M deviation (NL vs analytic): {dev_nl:.1f}%  "
              f"[{'OK' if dev_nl < 30 else 'FALSIFIED'}]")

    if not math.isnan(r_ana['fm_alpha']) and not math.isnan(r_lin['fm_alpha']):
        dev_lin = abs(r_lin['fm_alpha'] - r_ana['fm_alpha']) / abs(r_ana['fm_alpha']) * 100
        print(f"  F~M deviation (Lin vs analytic): {dev_lin:.1f}%  "
              f"[{'OK' if dev_lin < 30 else 'FALSIFIED'}]")

    overall = same_dir_nl and same_dir_lin
    print()
    if overall:
        print("  HYPOTHESIS SUPPORTED: Laplacian fields reproduce analytic gravity direction.")
    else:
        print("  HYPOTHESIS FALSIFIED: Laplacian field gives different gravity behavior.")

    print(f"\n  Total time: {time.time() - t_total:.0f}s")
    print("=" * 72)


if __name__ == "__main__":
    main()
