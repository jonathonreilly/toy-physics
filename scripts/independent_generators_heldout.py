#!/usr/bin/env python3
"""Independent-generator held-out test of the universality classifier rule.

The classifier rule fitted in scripts/universality_classifier.py is:
    (avg_deg >= 10.42) AND (reach_frac >= 0.86)
on a 5-condition battery (4 static + 1 dynamic Lane 6 gap).

Both the swept set (26 families) and the previous held-out set (8 families)
were parameter variations of the same grown-DAG generator: a regular
(layer, iy, iz) lattice with neighbor square stencil and Gaussian drift.
The 'small engineered basin' critique remains because the held-out set
is the same generator family.

This lane evaluates the classifier on **genuinely different generators**:

  R1-R3: Random k-regular forward DAG (each node picks k random neighbors
         on the next layer; no md neighbor square)
  E1-E2: Erdős–Rényi forward (each node-pair on adjacent layers connected
         with probability p)
  L1:    Long-range random (random forward neighbors mixed across t+1..t+3)
  T1:    Tree-like (small fanout, no convergence)
  H1:    Hub-and-spoke (one hub per layer with high in/out, sparse otherwise)
  X1:    Bipartite expander (regular forward bipartite, designed high
         spectral gap)

All generators place nodes on the same (layer, iy, iz) grid scaffolding
so the wave-equation field measurement still works, but the EDGE topology
is independent of the original neighbor square stencil.

Predictions are hard-coded in INDEPENDENT_PREDICTIONS BEFORE the run.
The script applies the in-sample-fitted rule from the classifier lane
WITHOUT REFITTING to evaluate generalization.
"""

from __future__ import annotations

import math
import random

BETA = 0.8
K = 5.0
H = 0.5
NL = 25
PW = 6
S_BASE = 0.004
MASS_Z = 3.0

# Rule from scripts/universality_classifier.py (in-sample fit on 26-family sweep)
RULE = ("avg_deg", ">=", 10.415, "reach_frac", ">=", 0.859)


def _make_grid(seed):
    """Place nodes on the (layer, iy, iz) grid. No edges yet.

    Returns (pos, nmap) where pos is the list of (x,y,z) positions and
    nmap[(layer, iy, iz)] = node_index.
    """
    rng = random.Random(seed)
    hw = int(PW / H)
    pos = []
    nmap = {}
    pos.append((0.0, 0.0, 0.0))
    nmap[(0, 0, 0)] = 0
    for layer in range(1, NL):
        x = layer * H
        for iy in range(-hw, hw + 1):
            for iz in range(-hw, hw + 1):
                # small jitter for realism, but on the grid
                y = iy * H + rng.gauss(0, 0.05 * H)
                z = iz * H + rng.gauss(0, 0.05 * H)
                idx = len(pos)
                pos.append((x, y, z))
                nmap[(layer, iy, iz)] = idx
    return pos, nmap


def grow_random_kreg(seed, k):
    """Each node has exactly k forward neighbors picked uniformly from layer+1."""
    pos, nmap = _make_grid(seed)
    rng = random.Random(seed + 1000)
    hw = int(PW / H)
    adj = {}
    coords_per_layer = [(iy, iz) for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    for layer in range(NL - 1):
        if layer == 0:
            sources = [0]
        else:
            sources = [nmap[(layer, iy, iz)] for (iy, iz) in coords_per_layer]
        next_pool = [nmap[(layer + 1, iy, iz)] for (iy, iz) in coords_per_layer]
        for si in sources:
            picks = rng.sample(next_pool, min(k, len(next_pool)))
            adj[si] = list(picks)
    return pos, adj, nmap


def grow_erdos_renyi(seed, p):
    """Each (i, j) pair on adjacent layers connected with probability p."""
    pos, nmap = _make_grid(seed)
    rng = random.Random(seed + 2000)
    hw = int(PW / H)
    adj = {}
    coords_per_layer = [(iy, iz) for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    for layer in range(NL - 1):
        if layer == 0:
            sources = [0]
        else:
            sources = [nmap[(layer, iy, iz)] for (iy, iz) in coords_per_layer]
        next_pool = [nmap[(layer + 1, iy, iz)] for (iy, iz) in coords_per_layer]
        for si in sources:
            adj[si] = [j for j in next_pool if rng.random() < p]
    return pos, adj, nmap


def grow_long_range(seed, k):
    """Each node picks k random forward neighbors from layers +1, +2, +3."""
    pos, nmap = _make_grid(seed)
    rng = random.Random(seed + 3000)
    hw = int(PW / H)
    adj = {}
    coords_per_layer = [(iy, iz) for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    for layer in range(NL - 1):
        if layer == 0:
            sources = [0]
        else:
            sources = [nmap[(layer, iy, iz)] for (iy, iz) in coords_per_layer]
        pool = []
        for dl in (1, 2, 3):
            if layer + dl < NL:
                pool.extend(nmap[(layer + dl, iy, iz)] for (iy, iz) in coords_per_layer)
        for si in sources:
            picks = rng.sample(pool, min(k, len(pool)))
            adj[si] = list(picks)
    return pos, adj, nmap


def grow_tree(seed, fanout):
    """Tree-like: each node has small fanout, no convergence (each child has one parent)."""
    pos, nmap = _make_grid(seed)
    rng = random.Random(seed + 4000)
    hw = int(PW / H)
    adj = {}
    coords_per_layer = [(iy, iz) for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    # parent-child by random assignment: each next-layer node assigned to ONE parent
    for layer in range(NL - 1):
        if layer == 0:
            sources = [0]
        else:
            sources = [nmap[(layer, iy, iz)] for (iy, iz) in coords_per_layer]
        next_pool = [nmap[(layer + 1, iy, iz)] for (iy, iz) in coords_per_layer]
        # round-robin children among sources
        rng.shuffle(next_pool)
        for j_idx, child in enumerate(next_pool):
            parent = sources[j_idx % len(sources)]
            adj.setdefault(parent, []).append(child)
        # truncate each parent to fanout
        for s in sources:
            if s in adj and len(adj[s]) > fanout:
                adj[s] = adj[s][:fanout]
    return pos, adj, nmap


def grow_hub(seed, hub_degree, peripheral_degree):
    """Hub-and-spoke: one hub per layer with high degree, others sparse."""
    pos, nmap = _make_grid(seed)
    rng = random.Random(seed + 5000)
    hw = int(PW / H)
    adj = {}
    coords_per_layer = [(iy, iz) for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    for layer in range(NL - 1):
        if layer == 0:
            sources = [0]
            hub = 0
        else:
            sources = [nmap[(layer, iy, iz)] for (iy, iz) in coords_per_layer]
            hub = nmap[(layer, 0, 0)]
        next_pool = [nmap[(layer + 1, iy, iz)] for (iy, iz) in coords_per_layer]
        for si in sources:
            deg = hub_degree if si == hub else peripheral_degree
            picks = rng.sample(next_pool, min(deg, len(next_pool)))
            adj[si] = list(picks)
    return pos, adj, nmap


def grow_bipartite_expander(seed, k):
    """Approximate expander: each node connects to k pseudo-random neighbors with shifts."""
    pos, nmap = _make_grid(seed)
    hw = int(PW / H)
    adj = {}
    n_per_layer = (2 * hw + 1) * (2 * hw + 1)
    coords_per_layer = [(iy, iz) for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    # use shifts based on a small primes pattern to mix coordinates
    shifts = [(2, 1), (1, 3), (3, 2), (4, 1), (1, 5), (5, 3), (2, 5), (3, 4)]
    for layer in range(NL - 1):
        if layer == 0:
            sources = [(0, 0, 0)]
        else:
            sources = [(layer, iy, iz) for (iy, iz) in coords_per_layer]
        for src_key in sources:
            si = nmap[src_key]
            _, sy, sz = src_key
            picks = []
            for i in range(k):
                dy, dz = shifts[(seed + i) % len(shifts)]
                ny = ((sy + hw + dy * (i + 1)) % (2 * hw + 1)) - hw
                nz = ((sz + hw + dz * (i + 1)) % (2 * hw + 1)) - hw
                pick = nmap.get((layer + 1, ny, nz))
                if pick is not None and pick not in picks:
                    picks.append(pick)
            adj[si] = picks
    return pos, adj, nmap


# ========== Helpers reused from universality_classifier.py ==========

def measure_structure(pos, adj, nmap):
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
    reach_frac = reach[NL - 1] / max(len(pos), 1)
    return avg_deg, max_deg, z_sym, fill, reach_frac


def imposed_field(pos, x_src, z_src, s):
    return [s / (math.sqrt((p[0] - x_src) ** 2 + (p[2] - z_src) ** 2) + 0.1) for p in pos]


def prop_beam(pos, adj, nmap, field, k, sources=None):
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


def cz(amps, pos):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    t = sum(abs(amps[i]) ** 2 for i in range(ds, n))
    if t <= 0:
        return 0.0
    return sum(abs(amps[i]) ** 2 * pos[i][2] for i in range(ds, n)) / t


def dp(amps, pos):
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


# Wave-equation helpers (same as universality_classifier.py)

def _laplacian_yz(f, nw):
    lap = [[0.0] * nw for _ in range(nw)]
    for iy in range(1, nw - 1):
        for iz in range(1, nw - 1):
            lap[iy][iz] = (
                f[iy - 1][iz] + f[iy + 1][iz] + f[iy][iz - 1] + f[iy][iz + 1]
                - 4.0 * f[iy][iz]
            )
    return lap


def _solve_wave_2plus1d(strength, iz_of_t, src_layer):
    hw = int(PW / H)
    nw = 2 * hw + 1
    f_prev = [[0.0] * nw for _ in range(nw)]
    f_curr = [[0.0] * nw for _ in range(nw)]
    history = [
        [[0.0] * nw for _ in range(nw)],
        [[0.0] * nw for _ in range(nw)],
    ]
    h2 = H * H
    for t in range(2, NL):
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


def _wave_field_at(history, layer, iy, iz):
    hw = int(PW / H)
    nw = 2 * hw + 1
    sy = iy + nw // 2
    sz = iz + nw // 2
    if 0 <= layer < NL and 0 <= sy < nw and 0 <= sz < nw:
        return history[layer][sy][sz]
    return 0.0


def _make_instantaneous(strength, iz_of_t, src_layer):
    hw = int(PW / H)
    nw = 2 * hw + 1
    cache = {}
    history = [[[0.0] * nw for _ in range(nw)] for _ in range(NL)]
    for t in range(NL):
        if t < src_layer:
            continue
        iz_now = iz_of_t(t)
        if iz_now not in cache:
            full = _solve_wave_2plus1d(strength, lambda tt, k=iz_now: k, src_layer)
            cache[iz_now] = [row[:] for row in full[NL - 1]]
        history[t] = [row[:] for row in cache[iz_now]]
    return history


def _prop_beam_with_field_fn(pos, adj, nmap, field_at_fn, k):
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


def measure_dynamic_gap(pos, adj, nmap):
    iz_start = 6
    iz_end = 0
    src_layer = NL // 4
    n_active = NL - src_layer
    if n_active <= 4:
        return 0.0, 0.0, 0.0
    v = (iz_end - iz_start) / n_active

    def iz_of_t(t):
        return iz_start + int(round(v * (t - src_layer)))

    h_M = _solve_wave_2plus1d(S_BASE, iz_of_t, src_layer)
    h_I = _make_instantaneous(S_BASE, iz_of_t, src_layer)
    free = prop_beam(pos, adj, nmap, None, K)
    z_free = cz(free, pos)
    cz_M = cz(_prop_beam_with_field_fn(pos, adj, nmap,
              lambda l, iy, iz: _wave_field_at(h_M, l, iy, iz), K), pos)
    cz_I = cz(_prop_beam_with_field_fn(pos, adj, nmap,
              lambda l, iy, iz: _wave_field_at(h_I, l, iy, iz), K), pos)
    dM = cz_M - z_free
    dI = cz_I - z_free
    rel = abs(dM - dI) / max(abs(dM), abs(dI), 1e-12)
    return dM, dI, rel


def battery(name, pos, adj, nmap):
    avg_deg, max_deg, z_sym, fill, reach_frac = measure_structure(pos, adj, nmap)
    free = prop_beam(pos, adj, nmap, None, K)
    z_free = cz(free, pos)

    x_src = (NL // 3) * H
    strengths = [0.001, 0.002, 0.004, 0.008]
    deltas = []
    for s in strengths:
        fld = imposed_field(pos, x_src, MASS_Z, s)
        g = prop_beam(pos, adj, nmap, fld, K)
        deltas.append(cz(g, pos) - z_free)
    sign_delta = deltas[2]
    abs_d = [abs(d) for d in deltas if abs(d) > 1e-15]
    fm = slope_log(strengths[:len(abs_d)], abs_d) if len(abs_d) >= 3 else float("nan")

    fld_born = imposed_field(pos, x_src, MASS_Z, S_BASE)

    def pb(slits):
        srcs = [(nmap.get((0, s2, 0)) or nmap.get((1, s2, 0)), 1.0 + 0j) for s2 in slits]
        srcs = [(i, a) for i, a in srcs if i is not None]
        return dp(prop_beam(pos, adj, nmap, fld_born, K, sources=srcs), pos)

    p123 = pb([-1, 0, 1])
    p12 = pb([-1, 0]); p13 = pb([-1, 1]); p23 = pb([0, 1])
    p1 = pb([-1]); p2 = pb([0]); p3 = pb([1])
    i3 = p123 - p12 - p13 - p23 + p1 + p2 + p3
    born = abs(i3) / max(p123, 1e-300)

    fld_null = imposed_field(pos, x_src, MASS_Z, 0.0)
    g_null = prop_beam(pos, adj, nmap, fld_null, K)
    delta_null = cz(g_null, pos) - z_free

    try:
        dM, dI, dyn_gap = measure_dynamic_gap(pos, adj, nmap)
    except Exception:
        dM = dI = dyn_gap = 0.0

    grav_ok = sign_delta > 1e-5
    fm_ok = (not math.isnan(fm)) and abs(fm - 1.0) < 0.10
    born_ok = born < 1e-10
    null_ok = abs(delta_null) < 1e-10
    dyn_ok = dyn_gap > 0.05
    pass_full = grav_ok and fm_ok and born_ok and null_ok and dyn_ok

    return {
        "name": name,
        "avg_deg": avg_deg, "max_deg": max_deg, "z_sym": z_sym,
        "fill": fill, "reach_frac": reach_frac,
        "delta": sign_delta, "fm": fm, "born": born, "null": delta_null,
        "dyn_dM": dM, "dyn_dI": dI, "dyn_gap": dyn_gap,
        "grav_ok": grav_ok, "fm_ok": fm_ok, "born_ok": born_ok,
        "null_ok": null_ok, "dyn_ok": dyn_ok, "pass": pass_full,
    }


def apply_rule(r):
    pa, da, ta, pb, db, tb = RULE
    ok_a = (r[pa] >= ta) if da == ">=" else (r[pa] <= ta)
    ok_b = (r[pb] >= tb) if db == ">=" else (r[pb] <= tb)
    return ok_a and ok_b


# ========== INDEPENDENT GENERATORS WITH PRE-COMMITTED PREDICTIONS ==========

# These predictions are hard-coded BEFORE running. The audit trail is this
# dict. Predictions are based on the rule (avg_deg >= 10.42) AND (reach_frac >= 0.86),
# but my structural intuition may differ from the rule for some borderline cases.

INDEPENDENT_PREDICTIONS = {
    "R1_kreg_k15":     True,   # avg_deg=15, dense random -> rule says PASS
    "R2_kreg_k8":      False,  # avg_deg=8, below rule threshold -> FAIL
    "R3_kreg_k20":     True,   # avg_deg=20, dense random -> PASS
    "E1_er_p005":      False,  # ER p=0.05, avg_deg ~ 8 -> FAIL
    "E2_er_p020":      True,   # ER p=0.20, avg_deg ~ 32 -> PASS
    "L1_longrange_k12": True,  # mixed-distance random k=12 -> PASS
    "T1_tree_fan4":    False,  # fanout=4, low avg_deg -> FAIL
    "H1_hub":          False,  # most nodes have low degree -> FAIL
    "X1_expander_k12": True,   # designed expander k=12 -> PASS
}


def make_independent_families():
    return [
        ("R1_kreg_k15", lambda: grow_random_kreg(0, 15)),
        ("R2_kreg_k8",  lambda: grow_random_kreg(0, 8)),
        ("R3_kreg_k20", lambda: grow_random_kreg(0, 20)),
        ("E1_er_p005",  lambda: grow_erdos_renyi(0, 0.05)),
        ("E2_er_p020",  lambda: grow_erdos_renyi(0, 0.20)),
        ("L1_longrange_k12", lambda: grow_long_range(0, 12)),
        ("T1_tree_fan4", lambda: grow_tree(0, 4)),
        ("H1_hub",      lambda: grow_hub(0, 30, 4)),
        ("X1_expander_k12", lambda: grow_bipartite_expander(0, 12)),
    ]


def main():
    print("=" * 100)
    print("INDEPENDENT-GENERATOR HELD-OUT TEST OF THE UNIVERSALITY CLASSIFIER RULE")
    print(f"Rule: ({RULE[0]} {RULE[1]} {RULE[2]:.3f}) AND ({RULE[3]} {RULE[4]} {RULE[5]:.3f})")
    print("Battery: 4 static + 1 dynamic Lane 6 gap (>5%); rule applied WITHOUT REFIT")
    print("=" * 100)

    families = make_independent_families()
    results = []
    for i, (name, builder) in enumerate(families, 1):
        print(f"\n[{i}/{len(families)}] {name:22s}", end="", flush=True)
        try:
            pos, adj, nmap = builder()
            r = battery(name, pos, adj, nmap)
            results.append(r)
            tag = "PASS" if r["pass"] else "FAIL"
            print(f"  {tag}  avg_deg={r['avg_deg']:.1f}  reach={r['reach_frac']:.3f}  "
                  f"delta={r['delta']:+.4f}  dyn={r['dyn_gap']:.1%}")
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"name": name, "pass": False, "error": str(e)})

    # Summary table
    print("\n" + "=" * 100)
    print("SUMMARY TABLE")
    print("=" * 100)
    cols = (f"{'family':22s} {'avg_deg':>8s} {'z_sym':>7s} {'reach':>7s}"
            f" {'delta':>10s} {'fm':>8s} {'born':>10s} {'dyn':>8s} {'pass':>6s}")
    print(cols)
    print("-" * 100)
    for r in results:
        if "error" in r:
            print(f"{r['name']:22s}  ERROR: {r['error']}")
            continue
        print(f"{r['name']:22s} {r['avg_deg']:8.2f} {r['z_sym']:7.3f} {r['reach_frac']:7.3f}"
              f" {r['delta']:+10.4f} {r['fm']:8.3f} {r['born']:10.1e}"
              f" {r['dyn_gap']:7.2%} {('PASS' if r['pass'] else 'FAIL'):>6s}")

    n_pass = sum(1 for r in results if r.get("pass"))
    n_fail = sum(1 for r in results if not r.get("pass") and "error" not in r)
    print(f"\nactual: PASS {n_pass} / FAIL {n_fail}")

    # Pre-committed predictions vs actual
    print("\n" + "=" * 100)
    print("PRE-COMMITTED PREDICTIONS vs ACTUAL")
    print("=" * 100)
    print(f"{'family':22s} {'committed':>10s} {'actual':>8s} {'rule':>6s} {'agree-c':>8s} {'agree-r':>8s}")
    pre_correct = 0
    rule_correct = 0
    n_eval = 0
    for r in results:
        if "error" in r:
            print(f"{r['name']:22s}  ERROR")
            continue
        committed = INDEPENDENT_PREDICTIONS.get(r["name"])
        rule_pred = apply_rule(r)
        agree_c = (committed == r["pass"])
        agree_r = (rule_pred == r["pass"])
        if agree_c:
            pre_correct += 1
        if agree_r:
            rule_correct += 1
        n_eval += 1
        print(f"{r['name']:22s} {str(committed):>10s} {str(r['pass']):>8s} "
              f"{str(rule_pred):>6s} {('OK' if agree_c else 'MISS'):>8s} "
              f"{('OK' if agree_r else 'MISS'):>8s}")

    print(f"\npre-committed predictions: {pre_correct}/{n_eval} = "
          f"{pre_correct/max(n_eval,1):.1%}")
    print(f"in-sample-fitted rule (no refit): {rule_correct}/{n_eval} = "
          f"{rule_correct/max(n_eval,1):.1%}")

    # Disagreements between committed and rule (interesting cases)
    print("\nDISAGREEMENTS (committed != rule):")
    any_disagree = False
    for r in results:
        if "error" in r:
            continue
        committed = INDEPENDENT_PREDICTIONS.get(r["name"])
        rule_pred = apply_rule(r)
        if committed != rule_pred:
            any_disagree = True
            print(f"  {r['name']:22s} committed={committed} rule={rule_pred} actual={r['pass']}")
    if not any_disagree:
        print("  (none — all 9 generators give same committed and rule predictions)")


if __name__ == "__main__":
    main()
