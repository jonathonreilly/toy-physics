#!/usr/bin/env python3
"""Continuum-limit refinement of the wave-retardation gap.

The previous lab-card lane (wave_retardation_velocity_sweep.py) showed
that the Lane 6 / Lane 8b 25-30% retardation gap is configuration-dependent
and does not have a clean v/c power law. The two specific blockers were:
  - The gap depends on n_active, NL, source-onset, and trajectory range
    in ways that don't reduce to a single physical scaling
  - Different parameterizations of the same nominal v/c give wildly
    different gaps

This lane tests whether those configuration-dependence problems are
**lattice artifacts that vanish in the continuum limit**.

Setup:
  - Fix PHYSICAL parameters across the refinement sweep:
      T_phys (total time NL*H)
      D_phys (source displacement iz_range*H)
      PW_phys (transverse half-width)
      lambda_phys (=> k_phys * H = constant per edge)
      s_phys, mass_z_phys, src_layer_fraction, regularizer
  - Refine the lattice: H ∈ {0.5, 0.25, 0.125}
  - At each H:
      NL = round(T_phys / H)
      iz_range = round(D_phys / H)
      PW = PW_phys (in physical units; the integer hw = PW/H grows)
      k_phase = K_PER_H / H (so k*H stays constant)
  - Compute (dM, dI, rel_gap) at each refinement
  - If rel_gap converges to a finite value as H → 0:
      we have a continuum prediction independent of lattice details
  - If rel_gap diverges or oscillates:
      the Lane 6 result is fundamentally a lattice artifact

This is the (2+1)D version (matching Lane 6) for tractability. The
(3+1)D promotion would require a 19³ → 73³ field cube at H=0.125,
which is infeasible in pure Python.
"""

from __future__ import annotations

import math
import random

# Physical parameters held constant across refinements (match Lane 6 setup)
T_PHYS_LAYERS = 30 * 0.5    # 15.0 physical "time" units (Lane 6: NL=30, H=0.5)
IZ_START_PHYS = 3.0         # Lane 6: iz_start=6 at H=0.5 → physical z = 3.0
IZ_END_PHYS = 0.0           # Lane 6: iz_end=0 at H=0.5 → physical z = 0.0
PW_PHYS = 6.0               # 6.0 physical transverse half-width
SRC_LAYER_FRAC = 1.0 / 3.0  # source becomes active at NL/3
S_PHYS = 0.004              # field source strength (dimensionless)
MASS_Z_PHYS = 3.0           # mass position in physical z
K_PER_H = 5.0 * 0.5         # k_phase * H product (= 2.5 phase per edge step at the reference)
BETA = 0.8                  # propagator angular weight (dimensionless)


def grow(seed, drift, restore, NL, PW, max_d_phys, H):
    """Build a grown DAG with explicit lattice spacing H."""
    rng = random.Random(seed)
    hw = int(PW / H)
    md = max(1, round(max_d_phys / H))
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
                    for dz in range(-md, md + 1):
                        di = nmap.get((layer, iy + dy, iz + dz))
                        if di is not None:
                            adj.setdefault(si, []).append(di)
    return pos, adj, nmap


def laplacian_yz(f, nw):
    lap = [[0.0] * nw for _ in range(nw)]
    for iy in range(1, nw - 1):
        for iz in range(1, nw - 1):
            lap[iy][iz] = (
                f[iy - 1][iz] + f[iy + 1][iz] + f[iy][iz - 1] + f[iy][iz + 1]
                - 4.0 * f[iy][iz]
            )
    return lap


def solve_wave(NL, PW, H, strength, iz_of_t, src_layer):
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
        lap = laplacian_yz(f_curr, nw)
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


def make_instantaneous(NL, PW, H, strength, iz_of_t, src_layer):
    """OLD comparator: cached late-time slice of static wave-equation solve.

    Lattice-artifact-sensitive (see continuum-limit note); kept for
    backward compatibility with the original Lane 6 setup.
    """
    hw = int(PW / H)
    nw = 2 * hw + 1
    cache = {}
    history = [[[0.0] * nw for _ in range(nw)] for _ in range(NL)]
    for t in range(NL):
        if t < src_layer:
            continue
        iz_now = iz_of_t(t)
        if iz_now not in cache:
            full = solve_wave(NL, PW, H, strength, lambda tt, k=iz_now: k, src_layer)
            cache[iz_now] = [row[:] for row in full[NL - 1]]
        history[t] = [row[:] for row in cache[iz_now]]
    return history


def make_imposed_newton(NL, PW, H, strength, iz_of_t, src_layer):
    """NEW comparator: imposed `s / (r + 0.1)` field at each layer with the
    source at its CURRENT physical position iz_of_t(t)*H.

    This is the literal c=infinity Newtonian potential evaluated against
    a time-varying source position. It has no wave-equation equilibration,
    no cache keys, no incomplete propagation — just the analytic
    instantaneous potential at each layer.

    Setup: at layer t, for each (iy, iz) cell on the field grid,
    compute the 2D Euclidean distance from the cell's physical position
    (layer*H, iz*H) to the source's current position (src_layer*H, iz_of_t(t)*H).
    Field value = strength / (distance + 0.1).
    """
    hw = int(PW / H)
    nw = 2 * hw + 1
    history = [[[0.0] * nw for _ in range(nw)] for _ in range(NL)]
    x_src_phys = src_layer * H
    for t in range(NL):
        if t < src_layer:
            continue
        z_src_phys = iz_of_t(t) * H
        layer_x = t * H
        for iy in range(nw):
            for iz in range(nw):
                # Cell physical (y, z) — wave equation field is 2D in (y, z),
                # so the "x" axis for the distance is the layer index
                z_phys = (iz - hw) * H
                dist = math.sqrt((layer_x - x_src_phys) ** 2
                                 + (z_phys - z_src_phys) ** 2) + 0.1
                history[t][iy][iz] = strength / dist
    return history


def field_at(history, NL, PW, H, layer, iy, iz):
    hw = int(PW / H)
    nw = 2 * hw + 1
    sy = iy + nw // 2
    sz = iz + nw // 2
    if 0 <= layer < NL and 0 <= sy < nw and 0 <= sz < nw:
        return history[layer][sy][sz]
    return 0.0


def prop_beam(pos, adj, nmap, history, k_phase, NL, PW, H):
    n = len(pos)
    hw = int(PW / H)
    field = [0.0] * n
    if history is not None:
        for layer in range(NL):
            for iy in range(-hw, hw + 1):
                for iz in range(-hw, hw + 1):
                    idx = nmap.get((layer, iy, iz))
                    if idx is not None:
                        field[idx] = field_at(history, NL, PW, H, layer, iy, iz)
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
            phase = k_phase * L * (1.0 - f)
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    return amps


def cz(amps, pos, NL, PW, H):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    weights = [abs(amps[i]) ** 2 for i in range(ds, n)]
    zs = [pos[i][2] for i in range(ds, n)]
    total = sum(weights)
    if total <= 0:
        return 0.0
    return sum(w * z for w, z in zip(weights, zs)) / total


def measure_at_H(H_val, label):
    """One refinement step at lattice spacing H_val."""
    NL = max(3, round(T_PHYS_LAYERS / H_val))
    PW = PW_PHYS
    k_phase = K_PER_H / H_val
    src_layer = max(1, int(SRC_LAYER_FRAC * NL))
    n_active = NL - src_layer
    if n_active < 2:
        return None

    # Match Lane 6 geometry: iz_start = round(IZ_START_PHYS / H), iz_end = 0
    iz_start = round(IZ_START_PHYS / H_val)
    iz_end = round(IZ_END_PHYS / H_val)
    iz_traversal = iz_start - iz_end
    v_per_layer = (iz_end - iz_start) / n_active
    v_phys = v_per_layer  # in units of c (since c = 1 cell/layer)

    iz_of_t = lambda t, sl=src_layer, vpl=v_per_layer, izs=iz_start: izs + int(round(vpl * (t - sl)))

    h_M = solve_wave(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)
    h_I = make_instantaneous(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)
    h_N = make_imposed_newton(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    free = prop_beam(pos, adj, nmap, None, k_phase, NL, PW, H_val)
    z_free = cz(free, pos, NL, PW, H_val)
    cz_M = cz(prop_beam(pos, adj, nmap, h_M, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_I = cz(prop_beam(pos, adj, nmap, h_I, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_N = cz(prop_beam(pos, adj, nmap, h_N, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    dM = cz_M - z_free
    dI = cz_I - z_free
    dN = cz_N - z_free

    diff_MI = dM - dI
    rel_MI = abs(diff_MI) / max(abs(dM), abs(dI), 1e-12)
    diff_MN = dM - dN
    rel_MN = abs(diff_MN) / max(abs(dM), abs(dN), 1e-12)
    diff_IN = dI - dN
    rel_IN = abs(diff_IN) / max(abs(dI), abs(dN), 1e-12)

    return {
        "label": label, "H": H_val, "NL": NL, "iz_traversal": iz_traversal,
        "iz_start": iz_start, "iz_end": iz_end, "src_layer": src_layer,
        "n_active": n_active, "v_per_layer": v_phys, "k_phase": k_phase,
        "n_nodes": len(pos),
        "dM": dM, "dI": dI, "dN": dN,
        "diff_MI": diff_MI, "rel_MI": rel_MI,
        "diff_MN": diff_MN, "rel_MN": rel_MN,
        "diff_IN": diff_IN, "rel_IN": rel_IN,
    }


def main():
    print("=" * 100)
    print("WAVE-RETARDATION CONTINUUM-LIMIT REFINEMENT")
    D_phys = IZ_START_PHYS - IZ_END_PHYS
    v_phys = -D_phys / (T_PHYS_LAYERS * (1 - SRC_LAYER_FRAC))
    print(f"Physical parameters held constant:")
    print(f"  T_phys (total propagation 'time' = NL*H) = {T_PHYS_LAYERS}")
    print(f"  iz_start_phys = {IZ_START_PHYS}, iz_end_phys = {IZ_END_PHYS}")
    print(f"  D_phys (source displacement) = {D_phys}")
    print(f"  PW_phys (transverse half-width) = {PW_PHYS}")
    print(f"  k*H (phase per edge step) = {K_PER_H}")
    print(f"  S_phys (field source strength) = {S_PHYS}")
    print(f"  v/c at every refinement = {v_phys:+.4f}")
    print("=" * 100)

    runs = []
    # Memory-feasible refinement: H = 0.5 → 0.35 → 0.25 (cost ratio ~ 8x not 64x)
    for H_val, label in [(0.5, "coarse"), (0.35, "medium"), (0.25, "fine")]:
        print(f"\n[{label}] H = {H_val}", flush=True)
        r = measure_at_H(H_val, label)
        if r is None:
            print("  too small NL — skipped")
            continue
        runs.append(r)
        print(f"  NL = {r['NL']}, iz_range = {r['iz_traversal']}, "
              f"k_phase = {r['k_phase']:.3f}")
        print(f"  src_layer = {r['src_layer']}, n_active = {r['n_active']}, "
              f"v_per_layer = {r['v_per_layer']:+.4f}")
        print(f"  n_nodes = {r['n_nodes']}")
        print(f"  dM = {r['dM']:+.6f}, dI (cached static) = {r['dI']:+.6f}, "
              f"dN (imposed Newton) = {r['dN']:+.6f}")
        print(f"  M - I = {r['diff_MI']:+.6f}, rel_MI = {r['rel_MI']:.2%}")
        print(f"  M - N = {r['diff_MN']:+.6f}, rel_MN = {r['rel_MN']:.2%}")
        print(f"  I - N = {r['diff_IN']:+.6f}, rel_IN = {r['rel_IN']:.2%}")

    print("\n" + "=" * 100)
    print("REFINEMENT TABLE")
    print("=" * 100)
    print(f"{'label':>8s} {'H':>6s} {'NL':>4s} {'dM':>10s} {'dI':>10s} {'dN':>10s}"
          f" {'rel_MI':>9s} {'rel_MN':>9s} {'rel_IN':>9s}")
    for r in runs:
        print(f"{r['label']:>8s} {r['H']:6.3f} {r['NL']:>4d} "
              f"{r['dM']:+10.6f} {r['dI']:+10.6f} {r['dN']:+10.6f} "
              f"{r['rel_MI']:9.2%} {r['rel_MN']:9.2%} {r['rel_IN']:9.2%}")

    if len(runs) >= 2:
        print("\n" + "=" * 100)
        print("CONVERGENCE — three quantities, two comparators")
        print("=" * 100)
        for key, label in [("dM", "dM (retarded wave field)"),
                           ("dI", "dI (cached static slice)"),
                           ("dN", "dN (imposed Newton at current pos)"),
                           ("rel_MI", "rel_MI = (M - I) / max(|M|,|I|)"),
                           ("rel_MN", "rel_MN = (M - N) / max(|M|,|N|)")]:
            print(f"\n  {label}:")
            for i in range(len(runs) - 1):
                r1 = runs[i]
                r2 = runs[i + 1]
                v1 = r1[key]
                v2 = r2[key]
                if isinstance(v1, float) and abs(v1) > 1e-12:
                    print(f"    {r1['label']:>8s}({v1:+.6f}) → "
                          f"{r2['label']:>8s}({v2:+.6f})  "
                          f"Δ = {v2-v1:+.6f} ({(v2-v1)/v1:+.1%})")
                else:
                    print(f"    {r1['label']:>8s}({v1:+.6f}) → "
                          f"{r2['label']:>8s}({v2:+.6f})  "
                          f"Δ = {v2-v1:+.6f}")

        # Verdict
        print("\n" + "=" * 100)
        print("VERDICT")
        print("=" * 100)
        last_MI_change = abs(runs[-1]["rel_MI"] - runs[-2]["rel_MI"])
        last_MN_change = abs(runs[-1]["rel_MN"] - runs[-2]["rel_MN"])
        rel_tol = 0.05  # 5% absolute tolerance on rel_gap

        print(f"  Last refinement Δ(rel_MI) = {last_MI_change:.4f}  "
              f"(old comparator)")
        print(f"  Last refinement Δ(rel_MN) = {last_MN_change:.4f}  "
              f"(imposed-Newton comparator)")
        print()
        if last_MN_change < rel_tol and last_MI_change > rel_tol:
            print(f"  IMPROVED — imposed-Newton comparator IS converging")
            print(f"  ({last_MN_change:.4f} < {rel_tol}) where the cached-static")
            print(f"  comparator was NOT ({last_MI_change:.4f} > {rel_tol}).")
            print(f"  The dI instability was a comparator construction artifact.")
            print(f"  Continuum-limit rel_MN ≈ {runs[-1]['rel_MN']:.2%}")
        elif last_MN_change < last_MI_change * 0.5:
            print(f"  PARTIAL — imposed-Newton comparator is more stable than")
            print(f"  the cached-static one (Δ_MN = {last_MN_change:.4f} < "
                  f"Δ_MI = {last_MI_change:.4f})")
            print(f"  but neither is strictly converged at this resolution.")
        elif last_MN_change < last_MI_change:
            print(f"  MARGINAL — imposed-Newton slightly more stable than cached-static")
            print(f"  (Δ_MN = {last_MN_change:.4f} < Δ_MI = {last_MI_change:.4f}) but")
            print(f"  not converged.")
        else:
            print(f"  NEGATIVE — imposed-Newton comparator is no better than cached-static")
            print(f"  (Δ_MN = {last_MN_change:.4f} ≥ Δ_MI = {last_MI_change:.4f}).")
            print(f"  The dI instability is NOT just a comparator construction artifact.")
            print(f"  The wave-retardation magnitude is fundamentally lattice-dependent.")


if __name__ == "__main__":
    main()
