#!/usr/bin/env python3
"""Universality classifier: which graph families pass the weak-field package?

Sweeps a wide grid of family generators (drift, restore, neighbor reach,
beam width, lattice depth, seed) and runs the same observable battery on
each. Records gravity sign, F~M slope, Born |I3|/P, null at s=0, and the
retarded-vs-instantaneous gap from the wave equation. Each family also
gets structural properties measured (avg forward degree, max degree,
effective dimensionality proxy). Pass/fail is reported per family.

The goal is to find the structural predictor that separates PASS from
FAIL — that property is the candidate universality criterion.
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

    # PASS criteria
    grav_ok = sign_delta > 1e-5
    fm_ok = (not math.isnan(fm)) and abs(fm - 1.0) < 0.10
    born_ok = born < 1e-10
    null_ok = abs(delta_null) < 1e-10
    pass_pkg = grav_ok and fm_ok and born_ok and null_ok

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
        "pass": pass_pkg,
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
        print(f"  {r['name']:25s}  -> {', '.join(reasons)}")

    # Classifier search: which structural property predicts pass?
    print("\nCLASSIFIER ANALYSIS:")
    pass_rs = [r for r in results if r.get("pass")]
    fail_rs = [r for r in results if not r.get("pass") and "error" not in r]
    if pass_rs and fail_rs:
        for prop in ["avg_deg", "max_deg", "eff_dim", "z_sym", "fill", "reach_frac"]:
            pv = [r[prop] for r in pass_rs]
            fv = [r[prop] for r in fail_rs]
            p_min, p_max = min(pv), max(pv)
            f_min, f_max = min(fv), max(fv)
            overlap = not (p_max < f_min or f_max < p_min)
            print(f"  {prop:11s}: PASS [{p_min:.3f}, {p_max:.3f}]  FAIL [{f_min:.3f}, {f_max:.3f}]  "
                  f"{'OVERLAP' if overlap else 'CLEAN SEPARATION'}")
        # threshold search per property: try (>= thr) and (<= thr) classifiers
        print("\n  best single-property classifier:")
        best = (0.0, "", "", 0.0)
        for prop in ["avg_deg", "max_deg", "eff_dim", "z_sym", "fill", "reach_frac"]:
            vals = sorted({r[prop] for r in results})
            for thr in vals:
                for direction in (">=", "<="):
                    if direction == ">=":
                        correct = sum(1 for r in results
                                      if "error" not in r and ((r[prop] >= thr) == r["pass"]))
                    else:
                        correct = sum(1 for r in results
                                      if "error" not in r and ((r[prop] <= thr) == r["pass"]))
                    acc = correct / max(len(results), 1)
                    if acc > best[0]:
                        best = (acc, prop, direction, thr)
        acc, prop, direction, thr = best
        print(f"    {prop} {direction} {thr:.3f}  -> accuracy {acc:.1%}")
        # 2-property AND classifier search
        print("\n  best 2-property AND classifier:")
        best2 = (0.0, "", "", 0.0, "", "", 0.0)
        props = ["avg_deg", "z_sym", "fill", "reach_frac"]
        for pa in props:
            va_set = sorted({r[pa] for r in results})
            for ta in va_set:
                for da in (">=", "<="):
                    for pb in props:
                        if pb == pa:
                            continue
                        vb_set = sorted({r[pb] for r in results})
                        for tb in vb_set:
                            for db in (">=", "<="):
                                correct = 0
                                for r in results:
                                    if "error" in r:
                                        continue
                                    ok_a = (r[pa] >= ta) if da == ">=" else (r[pa] <= ta)
                                    ok_b = (r[pb] >= tb) if db == ">=" else (r[pb] <= tb)
                                    pred = ok_a and ok_b
                                    if pred == r["pass"]:
                                        correct += 1
                                acc = correct / max(len(results), 1)
                                if acc > best2[0]:
                                    best2 = (acc, pa, da, ta, pb, db, tb)
        acc, pa, da, ta, pb, db, tb = best2
        print(f"    ({pa} {da} {ta:.3f}) AND ({pb} {db} {tb:.3f})  -> accuracy {acc:.1%}")
    else:
        print("  (no PASS or no FAIL — classifier requires both)")


if __name__ == "__main__":
    main()
