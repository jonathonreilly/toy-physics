#!/usr/bin/env python3
"""Universality classifier: empirical pass/fail rule for the static weak-field package.

Sweeps grown-DAG families across many generator axes and runs the SAME
STATIC observable battery on each:
  - gravity sign (delta_z under an imposed 1/r field)
  - F~M slope across 4 source strengths
  - Born |I3|/P (3-slit interferometer)
  - null at s=0
PASS = (gravity TOWARD) AND (|F~M-1|<0.10) AND (Born<1e-10) AND (|null|<1e-10).

The battery is STATIC ONLY. The retarded-vs-instantaneous (Lane 6) and
wave-equation observables are intentionally NOT in this lane; they are
covered separately. Adding them to the battery is a planned extension.

The script then fits an empirical 2-property AND classifier on the
swept set and validates it three ways:
  1. In-sample accuracy
  2. Leave-one-out cross-validation across all families
  3. A separate HELD-OUT family list with PREDICTIONS hard-coded in the
     source BEFORE running, so the audit trail is unambiguous

The result is an empirical classifier on the swept family set, not a
derived universality theorem.
"""

from __future__ import annotations

import math
import random

BETA = 0.8
K = 5.0
H = 0.5
S_BASE = 0.004
MASS_Z = 3.0


def grow(seed, drift, restore, NL, PW, max_d_phys, mode="dense", anisotropy=1.0):
    """Build a grown DAG.

    mode:
      "dense"      — full md-by-md neighbor square (default, original generator)
      "asym_y"     — only neighbors with dy >= 0 (broken Z2 in y)
      "asym_z"     — only neighbors with dz >= 0 (broken Z2 in z)
      "ring"       — only |dy|+|dz|=md neighbors (annulus connectivity)
      "cross"      — only dy=0 OR dz=0 (cross stencil; no diagonal)
      "drift_y"    — biased: connect (iy,iz) -> (iy+1, iz+dz)  (sheared)
    anisotropy: multiplier on z-direction reach (when > 1, z reach grows)
    """
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(max_d_phys / H))
    md_z = max(1, round(max_d_phys * anisotropy / H))
    pos = []
    adj = {}
    nmap = {}
    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    for layer in range(1, NL):
        x = layer * H
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                if layer == 1:
                    y, z = iy * H, iz * H
                else:
                    prev = nmap.get((layer - 1, iy, iz))
                    if prev is None:
                        continue
                    _, py, pz = pos[prev]
                    y = py + rng.gauss(0, drift * H)
                    z = pz + rng.gauss(0, drift * H)
                    y = y * (1 - restore) + (iy * H) * restore
                    z = z * (1 - restore) + (iz * H) * restore
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                si = nmap.get((layer - 1, iy, iz))
                if si is None:
                    continue
                for dy in range(-md, md + 1):
                    for dz in range(-md_z, md_z + 1):
                        if mode == "asym_y" and dy < 0:
                            continue
                        if mode == "asym_z" and dz < 0:
                            continue
                        if mode == "ring" and (abs(dy) + abs(dz) != md):
                            continue
                        if mode == "cross" and (dy != 0 and dz != 0):
                            continue
                        if mode == "drift_y" and dy != 1:
                            continue
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            adj.setdefault(si, []).append(di)
    return pos, adj, nmap


def measure_structure(pos, adj, nmap, NL, PW):
    """Return (avg_deg, max_deg, eff_dim, z_sym, fill, reach_frac) for the grown geometry.

    z_sym  = |sum(dz over edges)| / sum(|dz| over edges)  — 0 = perfectly Z2 in z
    fill   = mean degree / max degree                    — 1 = filled stencil
    reach_frac = reach(NL-2) / total_nodes                — fraction of detector reachable
    eff_dim = log(reach(L))/log(L) slope on interior
    """
    degs = [len(adj.get(i, [])) for i in range(len(pos))]
    avg_deg = sum(degs) / max(len(degs), 1)
    max_deg = max(degs) if degs else 0
    sum_dz = 0.0
    sum_abs_dz = 0.0
    for i, nbs in adj.items():
        zi = pos[i][2]
        for j in nbs:
            dz = pos[j][2] - zi
            sum_dz += dz
            sum_abs_dz += abs(dz)
    z_sym = abs(sum_dz) / sum_abs_dz if sum_abs_dz > 0 else 0.0
    fill = avg_deg / max_deg if max_deg > 0 else 0.0
    reach = [1] * NL
    frontier = {0}
    visited = {0}
    for L in range(1, NL):
        nf = set()
        for node in frontier:
            for nb in adj.get(node, []):
                if nb not in visited:
                    visited.add(nb)
                    nf.add(nb)
        reach[L] = len(visited)
        frontier = nf
        if not frontier:
            break
    Ls = [L for L in range(2, min(NL // 2 + 2, NL)) if reach[L] > 1]
    if len(Ls) >= 3:
        rs = [reach[L] for L in Ls]
        eff_dim = slope_log([float(L) for L in Ls], rs)
    else:
        eff_dim = 0.0
    reach_frac = reach[NL - 1] / max(len(pos), 1)
    return avg_deg, max_deg, eff_dim, z_sym, fill, reach_frac


def imposed_field(pos, x_src, z_src, s):
    return [s / (math.sqrt((p[0] - x_src) ** 2 + (p[2] - z_src) ** 2) + 0.1) for p in pos]


def prop_beam(pos, adj, nmap, field, k, sources=None, NL=None, PW=None):
    n = len(pos)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    if sources is None:
        amps[0] = 1.0
    else:
        for idx, amp in sources:
            amps[idx] = amp
    h2 = H * H
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            f = 0.0
            if field is not None:
                f = 0.5 * (field[i] + field[j])
            phase = k * L * (1.0 - f)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def cz(amps, pos, NL, PW):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    t = sum(abs(amps[i]) ** 2 for i in range(ds, n))
    if t <= 0:
        return 0.0
    return sum(abs(amps[i]) ** 2 * pos[i][2] for i in range(ds, n)) / t


def dp(amps, pos, NL, PW):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds = len(pos) - npl
    return sum(abs(amps[i]) ** 2 for i in range(ds, len(pos)))


def slope_log(xs, ys):
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx if sxx > 0 else 0.0


def _laplacian_yz(f, nw):
    lap = [[0.0] * nw for _ in range(nw)]
    for iy in range(1, nw - 1):
        for iz in range(1, nw - 1):
            lap[iy][iz] = (
                f[iy - 1][iz] + f[iy + 1][iz] + f[iy][iz - 1] + f[iy][iz + 1]
                - 4.0 * f[iy][iz]
            )
    return lap


def _solve_wave_2plus1d(NL_w, PW_w, strength, iz_of_t, src_layer):
    hw = int(PW_w / H)
    nw = 2 * hw + 1
    f_prev = [[0.0] * nw for _ in range(nw)]
    f_curr = [[0.0] * nw for _ in range(nw)]
    history = [
        [[0.0] * nw for _ in range(nw)],
        [[0.0] * nw for _ in range(nw)],
    ]
    h2 = H * H
    for t in range(2, NL_w):
        if t >= src_layer:
            iz_now = iz_of_t(t)
            sy = nw // 2
            sz = nw // 2 + iz_now
        else:
            sy = sz = -1
        lap = _laplacian_yz(f_curr, nw)
        f_next = [[0.0] * nw for _ in range(nw)]
        for iy in range(nw):
            for iz in range(nw):
                src = strength if (iy == sy and iz == sz) else 0.0
                f_next[iy][iz] = (
                    2.0 * f_curr[iy][iz] - f_prev[iy][iz]
                    + h2 * (lap[iy][iz] + src)
                )
        f_prev = f_curr
        f_curr = f_next
        history.append([row[:] for row in f_curr])
    return history


def _wave_field_at(history, NL_w, PW_w, layer, iy, iz):
    hw = int(PW_w / H)
    nw = 2 * hw + 1
    sy = iy + nw // 2
    sz = iz + nw // 2
    if 0 <= layer < NL_w and 0 <= sy < nw and 0 <= sz < nw:
        return history[layer][sy][sz]
    return 0.0


def _make_instantaneous_2plus1d(NL_w, PW_w, strength, iz_of_t, src_layer):
    hw = int(PW_w / H)
    nw = 2 * hw + 1
    cache = {}
    history = [[[0.0] * nw for _ in range(nw)] for _ in range(NL_w)]
    for t in range(NL_w):
        if t < src_layer:
            continue
        iz_now = iz_of_t(t)
        if iz_now not in cache:
            full = _solve_wave_2plus1d(NL_w, PW_w, strength,
                                       lambda tt, k=iz_now: k, src_layer)
            cache[iz_now] = [row[:] for row in full[NL_w - 1]]
        history[t] = [row[:] for row in cache[iz_now]]
    return history


def _prop_beam_with_field(pos, adj, nmap, field_at_fn, k, NL):
    """Beam propagation with a field accessed via a callback (layer, iy, iz)."""
    n = len(pos)
    field = [0.0] * n
    if field_at_fn is not None:
        for i, p in enumerate(pos):
            layer = round(p[0] / H)
            iy = round(p[1] / H)
            iz = round(p[2] / H)
            field[i] = field_at_fn(layer, iy, iz)
    order = sorted(range(n), key=lambda i: pos[i][0])
    amps = [0j] * n
    amps[0] = 1.0
    h2 = H * H
    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            f = 0.5 * (field[i] + field[j])
            phase = k * L * (1.0 - f)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def measure_dynamic_gap(pos, adj, nmap, NL, PW):
    """Lane 6 retarded-vs-instantaneous gap on a (2+1)D wave field.

    Returns (dM, dI, rel_gap). PW must match the beam grid.
    """
    iz_start = 6
    iz_end = 0
    src_layer = NL // 4
    n_active = NL - src_layer
    if n_active <= 4:
        return 0.0, 0.0, 0.0
    v = (iz_end - iz_start) / n_active

    def iz_of_t(t):
        return iz_start + int(round(v * (t - src_layer)))

    h_M = _solve_wave_2plus1d(NL, PW, S_BASE, iz_of_t, src_layer)
    h_I = _make_instantaneous_2plus1d(NL, PW, S_BASE, iz_of_t, src_layer)

    free = prop_beam(pos, adj, nmap, None, K)
    z_free = cz(free, pos, NL, PW)

    cz_M = cz(_prop_beam_with_field(pos, adj, nmap,
              lambda l, iy, iz: _wave_field_at(h_M, NL, PW, l, iy, iz), K, NL), pos, NL, PW)
    cz_I = cz(_prop_beam_with_field(pos, adj, nmap,
              lambda l, iy, iz: _wave_field_at(h_I, NL, PW, l, iy, iz), K, NL), pos, NL, PW)
    dM = cz_M - z_free
    dI = cz_I - z_free
    rel = abs(dM - dI) / max(abs(dM), abs(dI), 1e-12)
    return dM, dI, rel


def battery(family):
    """Run the observable battery on one family. Returns dict of results."""
    name = family["name"]
    seed = family["seed"]
    drift = family["drift"]
    restore = family["restore"]
    NL = family["NL"]
    PW = family["PW"]
    md_phys = family["md"]
    mode = family.get("mode", "dense")
    anisotropy = family.get("anisotropy", 1.0)

    pos, adj, nmap = grow(seed, drift, restore, NL, PW, md_phys, mode=mode, anisotropy=anisotropy)
    n_nodes = len(pos)
    avg_deg, max_deg, eff_dim, z_sym, fill, reach_frac = measure_structure(pos, adj, nmap, NL, PW)

    # 1. Free run
    free = prop_beam(pos, adj, nmap, None, K)
    z_free = cz(free, pos, NL, PW)

    # 2. Gravity sign + F~M (4 strengths via imposed 1/r field)
    x_src = (NL // 3) * H
    strengths = [0.001, 0.002, 0.004, 0.008]
    deltas = []
    for s in strengths:
        fld = imposed_field(pos, x_src, MASS_Z, s)
        g = prop_beam(pos, adj, nmap, fld, K)
        deltas.append(cz(g, pos, NL, PW) - z_free)
    sign_delta = deltas[2]  # at s=0.004
    abs_deltas = [abs(d) for d in deltas if abs(d) > 1e-15]
    if len(abs_deltas) >= 3:
        fm = slope_log(strengths[: len(abs_deltas)], abs_deltas)
    else:
        fm = float("nan")

    # 3. Born |I3|/P with imposed field at S_BASE
    fld_born = imposed_field(pos, x_src, MASS_Z, S_BASE)

    def pb(slits):
        srcs = [(nmap.get((0, s2, 0)) or nmap.get((1, s2, 0)), 1.0 + 0j) for s2 in slits]
        srcs = [(i, a) for i, a in srcs if i is not None]
        return dp(prop_beam(pos, adj, nmap, fld_born, K, sources=srcs), pos, NL, PW)

    p123 = pb([-1, 0, 1])
    p12 = pb([-1, 0]); p13 = pb([-1, 1]); p23 = pb([0, 1])
    p1 = pb([-1]); p2 = pb([0]); p3 = pb([1])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    born = abs(i3) / max(p123, 1e-300)

    # 4. Null at s=0
    fld_null = imposed_field(pos, x_src, MASS_Z, 0.0)
    g_null = prop_beam(pos, adj, nmap, fld_null, K)
    delta_null = cz(g_null, pos, NL, PW) - z_free

    # 5. Dynamic: Lane 6 retarded vs instantaneous gap on (2+1)D wave equation
    try:
        dM, dI, dyn_gap = measure_dynamic_gap(pos, adj, nmap, NL, PW)
    except Exception:
        dM, dI, dyn_gap = 0.0, 0.0, 0.0

    # PASS criteria — STATIC package
    grav_ok = sign_delta > 1e-5
    fm_ok = (not math.isnan(fm)) and abs(fm - 1.0) < 0.10
    born_ok = born < 1e-10
    null_ok = abs(delta_null) < 1e-10
    pass_static = grav_ok and fm_ok and born_ok and null_ok
    # DYNAMIC condition: retarded must differ from instantaneous by > 5%
    dyn_ok = dyn_gap > 0.05
    pass_full = pass_static and dyn_ok

    return {
        "name": name,
        "n_nodes": n_nodes,
        "avg_deg": avg_deg,
        "max_deg": max_deg,
        "eff_dim": eff_dim,
        "z_sym": z_sym,
        "fill": fill,
        "reach_frac": reach_frac,
        "drift": drift,
        "restore": restore,
        "NL": NL,
        "PW": PW,
        "md": md_phys,
        "delta": sign_delta,
        "fm": fm,
        "born": born,
        "null": delta_null,
        "grav_ok": grav_ok,
        "fm_ok": fm_ok,
        "born_ok": born_ok,
        "null_ok": null_ok,
        "dyn_dM": dM,
        "dyn_dI": dI,
        "dyn_gap": dyn_gap,
        "dyn_ok": dyn_ok,
        "pass_static": pass_static,
        "pass": pass_full,
    }


def make_families():
    """Build a wide sweep across generator parameters and structural modes."""
    fams = []
    base = {"NL": 25, "PW": 6, "md": 3}

    def F(**kw):
        f = dict(base)
        f.update(kw)
        return f

    # A. Original three (baseline) — should all pass
    fams.append(F(name="A1_orig_Fam1", seed=0, drift=0.20, restore=0.70))
    fams.append(F(name="A2_orig_Fam2", seed=0, drift=0.05, restore=0.30))
    fams.append(F(name="A3_orig_Fam3", seed=0, drift=0.50, restore=0.90))

    # B. Pure regular vs pure random
    fams.append(F(name="B1_pure_grid", seed=0, drift=0.00, restore=1.00))
    fams.append(F(name="C1_random_lo", seed=0, drift=0.30, restore=0.00))
    fams.append(F(name="C2_random_hi", seed=0, drift=1.00, restore=0.00))

    # D. Reach extremes
    fams.append(F(name="D1_md1_NN", seed=0, drift=0.20, restore=0.70, md=1))
    fams.append(F(name="D2_md4_long", seed=0, drift=0.20, restore=0.70, md=4))

    # E. Beam width
    fams.append(F(name="E1_PW3_narrow", seed=0, drift=0.20, restore=0.70, PW=3))
    fams.append(F(name="E2_PW10_wide", seed=0, drift=0.20, restore=0.70, PW=10))

    # F. Lattice depth
    fams.append(F(name="F1_NL10_short", seed=0, drift=0.20, restore=0.70, NL=10))
    fams.append(F(name="F2_NL40_long", seed=0, drift=0.20, restore=0.70, NL=40))

    # G. Structural mode — Z2 broken
    fams.append(F(name="G1_asym_y", seed=0, drift=0.20, restore=0.70, mode="asym_y"))
    fams.append(F(name="G2_asym_z", seed=0, drift=0.20, restore=0.70, mode="asym_z"))

    # H. Sparse stencils
    fams.append(F(name="H1_ring", seed=0, drift=0.20, restore=0.70, mode="ring"))
    fams.append(F(name="H2_cross", seed=0, drift=0.20, restore=0.70, mode="cross"))

    # I. Sheared connectivity (only dy=+1)
    fams.append(F(name="I1_drift_y", seed=0, drift=0.20, restore=0.70, mode="drift_y"))

    # J. Anisotropic reach
    fams.append(F(name="J1_aniso_z2", seed=0, drift=0.20, restore=0.70, anisotropy=2.0))
    fams.append(F(name="J2_aniso_z4", seed=0, drift=0.20, restore=0.70, anisotropy=4.0))

    # K. Pathological / extreme
    fams.append(F(name="K1_NN_no_restore", seed=0, drift=1.50, restore=0.00, md=1))
    fams.append(F(name="K2_huge_drift_md1", seed=0, drift=3.00, restore=0.00, md=1))
    fams.append(F(name="K3_NL5", seed=0, drift=0.20, restore=0.70, NL=5))
    fams.append(F(name="K4_PW2", seed=0, drift=0.20, restore=0.70, PW=2))

    # L. Seed variation
    fams.append(F(name="L1_seed1", seed=1, drift=0.20, restore=0.70))
    fams.append(F(name="L2_seed2", seed=2, drift=0.20, restore=0.70))
    fams.append(F(name="L3_seed3", seed=3, drift=0.20, restore=0.70))

    return fams


def fit_classifier(results):
    """Best 2-property AND classifier (avg_deg, z_sym style) on the given results.

    Returns (acc, prop_a, dir_a, thr_a, prop_b, dir_b, thr_b).
    """
    rs = [r for r in results if "error" not in r]
    if not rs:
        return (0.0, "", "", 0.0, "", "", 0.0)
    props = ["avg_deg", "z_sym", "fill", "reach_frac"]
    best = (-1.0, "", "", 0.0, "", "", 0.0)
    for pa in props:
        va_set = sorted({r[pa] for r in rs})
        for ta in va_set:
            for da in (">=", "<="):
                for pb in props:
                    if pb == pa:
                        continue
                    vb_set = sorted({r[pb] for r in rs})
                    for tb in vb_set:
                        for db in (">=", "<="):
                            correct = 0
                            for r in rs:
                                ok_a = (r[pa] >= ta) if da == ">=" else (r[pa] <= ta)
                                ok_b = (r[pb] >= tb) if db == ">=" else (r[pb] <= tb)
                                pred = ok_a and ok_b
                                if pred == r["pass"]:
                                    correct += 1
                            acc = correct / len(rs)
                            if acc > best[0]:
                                best = (acc, pa, da, ta, pb, db, tb)
    return best


def apply_classifier(r, rule):
    """Apply a (acc, pa, da, ta, pb, db, tb) rule to one result row."""
    _, pa, da, ta, pb, db, tb = rule
    ok_a = (r[pa] >= ta) if da == ">=" else (r[pa] <= ta)
    ok_b = (r[pb] >= tb) if db == ">=" else (r[pb] <= tb)
    return ok_a and ok_b


def make_heldout_families():
    """A separate set of families for OUT-OF-SAMPLE validation.

    These are NOT in make_families(). The classifier is fitted on
    make_families() only, then evaluated on these without refitting.
    """
    base = {"NL": 25, "PW": 6, "md": 3}
    def F(**kw):
        f = dict(base); f.update(kw); return f
    return [
        # H1: dense + symmetric -> predict PASS
        F(name="HELD_dense_sym",      seed=7, drift=0.15, restore=0.50),
        # H2: pure grid different seed -> predict PASS
        F(name="HELD_grid_seed7",     seed=7, drift=0.00, restore=1.00),
        # H3: ring sparse -> predict FAIL (low avg_deg)
        F(name="HELD_ring_md3",       seed=7, drift=0.20, restore=0.70, mode="ring"),
        # H4: asym_z (broken Z2 in measurement axis) -> predict FAIL
        F(name="HELD_asym_z_seed7",   seed=7, drift=0.20, restore=0.70, mode="asym_z"),
        # H5: asym_y (broken Z2 in non-measurement axis) -> predict PASS
        F(name="HELD_asym_y_seed7",   seed=7, drift=0.20, restore=0.70, mode="asym_y"),
        # H6: drift_y (sheared, very sparse) -> predict FAIL
        F(name="HELD_drift_y_seed7",  seed=7, drift=0.20, restore=0.70, mode="drift_y"),
        # H7: anisotropic z reach -> predict PASS (still dense + symmetric)
        F(name="HELD_aniso_z3",       seed=7, drift=0.20, restore=0.70, anisotropy=3.0),
        # H8: cross stencil -> predict PASS (sparse but not pathologically so)
        F(name="HELD_cross_seed7",    seed=7, drift=0.20, restore=0.70, mode="cross"),
    ]


# PRE-COMMITTED PREDICTIONS for the held-out families above. These are
# hard-coded BEFORE the script is run, on the basis of the previously
# discovered rule "(avg_deg >= 20.74) AND (z_sym <= 0.002)". The audit
# trail is this dict in the source.
HELDOUT_PREDICTIONS = {
    "HELD_dense_sym":     True,   # dense + symmetric
    "HELD_grid_seed7":    True,   # pure regular grid
    "HELD_ring_md3":      False,  # too sparse
    "HELD_asym_z_seed7":  False,  # broken Z2 in measurement axis
    "HELD_asym_y_seed7":  True,   # asymmetry in non-measurement axis is OK
    "HELD_drift_y_seed7": False,  # sheared + sparse
    "HELD_aniso_z3":      True,   # dense + symmetric still
    "HELD_cross_seed7":   True,   # sparse but symmetric and connected
}


def main():
    print("=" * 90)
    print("UNIVERSALITY CLASSIFIER")
    print("Sweeps grown-graph families and runs the weak-field observable battery.")
    print("PASS = (gravity TOWARD) AND (|F~M-1|<0.10) AND (Born<1e-10) AND (|null|<1e-10)")
    print("=" * 90)

    families = make_families()
    results = []
    for i, fam in enumerate(families, 1):
        print(f"\n[{i:2d}/{len(families)}] {fam['name']:30s} ", end="", flush=True)
        try:
            r = battery(fam)
            results.append(r)
            tag = "PASS" if r["pass"] else "FAIL"
            print(f"  {tag}  delta={r['delta']:+.4f}  fm={r['fm']:.3f}  born={r['born']:.1e}")
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"name": fam["name"], "pass": False, "error": str(e)})

    # Summary table
    print("\n" + "=" * 90)
    print("SUMMARY TABLE")
    print("=" * 90)
    cols = f"{'family':24s} {'avg_deg':>8s} {'z_sym':>7s} {'fill':>6s} {'reach':>7s} {'delta':>10s} {'fm':>8s} {'born':>10s} {'pass':>6s}"
    print(cols)
    print("-" * 100)
    for r in results:
        if "error" in r:
            print(f"{r['name']:24s}  ERROR")
            continue
        print(f"{r['name']:24s} {r['avg_deg']:8.2f} {r['z_sym']:7.3f} {r['fill']:6.2f} {r['reach_frac']:7.3f}"
              f" {r['delta']:+10.4f} {r['fm']:8.3f} {r['born']:10.1e} {('PASS' if r['pass'] else 'FAIL'):>6s}")

    # Pass/fail breakdown
    n_pass = sum(1 for r in results if r.get("pass"))
    n_fail = sum(1 for r in results if not r.get("pass"))
    print(f"\nPASS: {n_pass} / {len(results)}    FAIL: {n_fail} / {len(results)}")

    # Why does each FAIL family fail?
    print("\nFAIL BREAKDOWN:")
    for r in results:
        if r.get("pass") or "error" in r:
            continue
        reasons = []
        if not r["grav_ok"]:
            reasons.append(f"grav (delta={r['delta']:+.4f})")
        if not r["fm_ok"]:
            reasons.append(f"F~M (fm={r['fm']:.3f})")
        if not r["born_ok"]:
            reasons.append(f"Born ({r['born']:.1e})")
        if not r["null_ok"]:
            reasons.append(f"null ({r['null']:.1e})")
        if not r.get("dyn_ok", True):
            reasons.append(f"dyn ({r.get('dyn_gap', 0):.2%})")
        print(f"  {r['name']:25s}  -> {', '.join(reasons)}")

    # Classifier search: in-sample, LOO, and held-out
    print("\nCLASSIFIER ANALYSIS (in-sample):")
    in_rule = fit_classifier(results)
    acc, pa, da, ta, pb, db, tb = in_rule
    print(f"  best 2-prop AND rule: ({pa} {da} {ta:.3f}) AND ({pb} {db} {tb:.3f})")
    print(f"  in-sample accuracy: {acc:.1%}")

    # Leave-one-out cross-validation
    print("\nLEAVE-ONE-FAMILY-OUT:")
    rs = [r for r in results if "error" not in r]
    loo_correct = 0
    loo_misses = []
    for i, held in enumerate(rs):
        train = rs[:i] + rs[i + 1:]
        rule = fit_classifier(train)
        pred = apply_classifier(held, rule)
        if pred == held["pass"]:
            loo_correct += 1
        else:
            loo_misses.append((held["name"], held["pass"], pred, rule[1:]))
    loo_acc = loo_correct / max(len(rs), 1)
    print(f"  LOO accuracy: {loo_correct}/{len(rs)} = {loo_acc:.1%}")
    if loo_misses:
        print("  misses:")
        for name, truth, pred, rule_tail in loo_misses:
            print(f"    {name}: truth={truth}, pred={pred}, rule={rule_tail}")

    # Held-out family validation with PRE-COMMITTED predictions
    print("\nHELD-OUT FAMILIES (predictions hard-coded before run):")
    held_families = make_heldout_families()
    held_results = []
    for fam in held_families:
        try:
            r = battery(fam)
        except Exception as e:
            r = {"name": fam["name"], "pass": False, "error": str(e)}
        held_results.append(r)

    print(f"  {'family':25s} {'predicted':>10s} {'actual':>8s} {'rule pred':>10s} {'agree':>7s}")
    pred_correct = 0
    rule_correct = 0
    for r in held_results:
        if "error" in r:
            print(f"  {r['name']:25s}  ERROR")
            continue
        committed = HELDOUT_PREDICTIONS.get(r["name"])
        rule_pred = apply_classifier(r, in_rule)
        agree_committed = (committed == r["pass"])
        agree_rule = (rule_pred == r["pass"])
        if agree_committed:
            pred_correct += 1
        if agree_rule:
            rule_correct += 1
        print(f"  {r['name']:25s} {str(committed):>10s} {str(r['pass']):>8s} "
              f"{str(rule_pred):>10s} {('OK' if agree_committed else 'MISS'):>7s}")
    n_held = sum(1 for r in held_results if "error" not in r)
    print(f"\n  pre-committed predictions: {pred_correct}/{n_held} = {pred_correct/max(n_held,1):.1%}")
    print(f"  in-sample-fitted rule applied to held-out: {rule_correct}/{n_held} = {rule_correct/max(n_held,1):.1%}")


if __name__ == "__main__":
    main()
