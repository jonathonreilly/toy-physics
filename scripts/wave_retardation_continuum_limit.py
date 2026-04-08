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
  - Hold PHYSICAL parameters APPROXIMATELY constant across the
    refinement sweep (integer rounding of NL / src_layer / iz_range
    is unavoidable — see the discretization caveat in the note):
      T_phys (total time NL*H)
      iz_start_phys, iz_end_phys (source start / end positions)
      PW_phys (transverse half-width)
      k*H (= constant per edge)
      s_phys, mass_z_phys, src_layer_fraction
  - Refine the lattice: H ∈ {0.5, 0.35, 0.25}   (memory-feasible)
    A first attempt at H ∈ {0.5, 0.25, 0.125} ran out of memory on
    the (2+1)D harness (at H=0.125 the beam DAG has ~1.13M nodes
    and the adjacency map exhausts available RAM). The refinement
    schedule used here is cost ratio ~8x from coarse to fine rather
    than ~64x.
  - At each H:
      NL = round(T_phys / H)
      iz_start = round(IZ_START_PHYS / H)
      iz_end   = round(IZ_END_PHYS / H)
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


def make_instantaneous_equilibrated(NL_dyn, PW, H, strength, iz_of_t,
                                    src_layer, equilib_multiplier=3):
    """BETTER comparator: cached static slice from a LONG equilibration solve.

    Same construction as make_instantaneous, but each static problem is
    solved on NL_equilib = equilib_multiplier * NL_dyn layers instead of
    NL_dyn. The late-time slice is taken from the long solve, so the
    cached static field is much closer to the true wave-equation static
    limit. Tests whether the dI instability is just incomplete
    equilibration at finite NL.
    """
    hw = int(PW / H)
    nw = 2 * hw + 1
    NL_eq = max(NL_dyn + 5, NL_dyn * equilib_multiplier)
    cache = {}
    history = [[[0.0] * nw for _ in range(nw)] for _ in range(NL_dyn)]
    # The equilibration solve uses its own src_layer_eq that's small enough
    # to leave time for equilibration.
    src_layer_eq = max(1, NL_eq // 10)
    for t in range(NL_dyn):
        if t < src_layer:
            continue
        iz_now = iz_of_t(t)
        if iz_now not in cache:
            full = solve_wave(NL_eq, PW, H, strength,
                              lambda tt, k=iz_now: k, src_layer_eq)
            cache[iz_now] = [row[:] for row in full[NL_eq - 1]]
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
    h_Ieq = make_instantaneous_equilibrated(
        NL, PW, H_val, S_PHYS, iz_of_t, src_layer, equilib_multiplier=3
    )
    h_N = make_imposed_newton(NL, PW, H_val, S_PHYS, iz_of_t, src_layer)

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    free = prop_beam(pos, adj, nmap, None, k_phase, NL, PW, H_val)
    z_free = cz(free, pos, NL, PW, H_val)
    cz_M = cz(prop_beam(pos, adj, nmap, h_M, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_I = cz(prop_beam(pos, adj, nmap, h_I, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_Ieq = cz(prop_beam(pos, adj, nmap, h_Ieq, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    cz_N = cz(prop_beam(pos, adj, nmap, h_N, k_phase, NL, PW, H_val), pos, NL, PW, H_val)
    dM = cz_M - z_free
    dI = cz_I - z_free
    dIeq = cz_Ieq - z_free
    dN = cz_N - z_free

    diff_MI = dM - dI
    rel_MI = abs(diff_MI) / max(abs(dM), abs(dI), 1e-12)
    diff_MIeq = dM - dIeq
    rel_MIeq = abs(diff_MIeq) / max(abs(dM), abs(dIeq), 1e-12)
    diff_MN = dM - dN
    rel_MN = abs(diff_MN) / max(abs(dM), abs(dN), 1e-12)
    diff_IN = dI - dN
    rel_IN = abs(diff_IN) / max(abs(dI), abs(dN), 1e-12)
    diff_IeqN = dIeq - dN
    rel_IeqN = abs(diff_IeqN) / max(abs(dIeq), abs(dN), 1e-12)

    return {
        "label": label, "H": H_val, "NL": NL, "iz_traversal": iz_traversal,
        "iz_start": iz_start, "iz_end": iz_end, "src_layer": src_layer,
        "n_active": n_active, "v_per_layer": v_phys, "k_phase": k_phase,
        "n_nodes": len(pos),
        "dM": dM, "dI": dI, "dIeq": dIeq, "dN": dN,
        "diff_MI": diff_MI, "rel_MI": rel_MI,
        "diff_MIeq": diff_MIeq, "rel_MIeq": rel_MIeq,
        "diff_MN": diff_MN, "rel_MN": rel_MN,
        "diff_IN": diff_IN, "rel_IN": rel_IN,
        "diff_IeqN": diff_IeqN, "rel_IeqN": rel_IeqN,
    }


def main():
    print("=" * 100)
    print("WAVE-RETARDATION CONTINUUM-LIMIT REFINEMENT")
    D_phys = IZ_START_PHYS - IZ_END_PHYS
    v_target = -D_phys / (T_PHYS_LAYERS * (1 - SRC_LAYER_FRAC))
    print(f"Physical parameters held APPROXIMATELY constant:")
    print(f"  T_phys (total propagation 'time' = NL*H) = {T_PHYS_LAYERS}")
    print(f"  iz_start_phys = {IZ_START_PHYS}, iz_end_phys = {IZ_END_PHYS}")
    print(f"  D_phys (source displacement) = {D_phys}")
    print(f"  PW_phys (transverse half-width) = {PW_PHYS}")
    print(f"  k*H (phase per edge step) = {K_PER_H}")
    print(f"  S_phys (field source strength) = {S_PHYS}")
    print(f"  v/c target = {v_target:+.4f}  (realized v/c drifts due to")
    print(f"                                 integer rounding of NL / src_layer /")
    print(f"                                 iz_range; see per-run values below)")
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
        print(f"  dM = {r['dM']:+.6f}")
        print(f"  dI (cached static, NL_dyn)   = {r['dI']:+.6f}")
        print(f"  dIeq (equilibrated static, 3*NL) = {r['dIeq']:+.6f}")
        print(f"  dN (imposed Newton)          = {r['dN']:+.6f}")
        print(f"  rel_MI   = {r['rel_MI']:.2%}  (M vs cached static)")
        print(f"  rel_MIeq = {r['rel_MIeq']:.2%}  (M vs equilibrated static)")
        print(f"  rel_MN   = {r['rel_MN']:.2%}  (M vs imposed Newton)")
        print(f"  rel_IeqN = {r['rel_IeqN']:.2%}  (equilibrated vs imposed Newton)")

    print("\n" + "=" * 100)
    print("REFINEMENT TABLE — beam deflection values and relative gaps")
    print("=" * 100)
    print(f"{'label':>8s} {'H':>6s} {'NL':>4s} {'dM':>10s} {'dI':>10s} "
          f"{'dIeq':>10s} {'dN':>10s}")
    for r in runs:
        print(f"{r['label']:>8s} {r['H']:6.3f} {r['NL']:>4d} "
              f"{r['dM']:+10.6f} {r['dI']:+10.6f} "
              f"{r['dIeq']:+10.6f} {r['dN']:+10.6f}")
    print()
    print(f"{'label':>8s} {'rel_MI':>10s} {'rel_MIeq':>10s} {'rel_MN':>10s} "
          f"{'rel_IeqN':>10s}")
    for r in runs:
        print(f"{r['label']:>8s} {r['rel_MI']:10.2%} {r['rel_MIeq']:10.2%} "
              f"{r['rel_MN']:10.2%} {r['rel_IeqN']:10.2%}")

    if len(runs) >= 2:
        print("\n" + "=" * 100)
        print("CONVERGENCE — three quantities, two comparators")
        print("=" * 100)
        for key, label in [("dM", "dM (retarded wave field)"),
                           ("dI", "dI (cached static, NL_dyn)"),
                           ("dIeq", "dIeq (equilibrated static, 3*NL_dyn)"),
                           ("dN", "dN (imposed Newton at current pos)"),
                           ("rel_MI", "rel_MI = (M - I) / max(|M|,|I|)"),
                           ("rel_MIeq", "rel_MIeq = (M - Ieq) / max(|M|,|Ieq|)"),
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
        print("VERDICT — three comparators compared")
        print("=" * 100)
        last_MI_change = abs(runs[-1]["rel_MI"] - runs[-2]["rel_MI"])
        last_MIeq_change = abs(runs[-1]["rel_MIeq"] - runs[-2]["rel_MIeq"])
        last_MN_change = abs(runs[-1]["rel_MN"] - runs[-2]["rel_MN"])
        last_IeqN_change = abs(runs[-1]["rel_IeqN"] - runs[-2]["rel_IeqN"])
        rel_tol = 0.05

        print(f"  Δ(rel_MI)   last step = {last_MI_change:.4f}  "
              f"(cached static, NL_dyn)")
        print(f"  Δ(rel_MIeq) last step = {last_MIeq_change:.4f}  "
              f"(equilibrated static, 3*NL_dyn)")
        print(f"  Δ(rel_MN)   last step = {last_MN_change:.4f}  "
              f"(imposed Newton)")
        print(f"  Δ(rel_IeqN) last step = {last_IeqN_change:.4f}  "
              f"(equilibrated static vs imposed Newton — should → 0)")
        print()

        # Is the equilibrated static slice now converging to imposed Newton?
        first_IeqN = runs[0]["rel_IeqN"]
        last_IeqN = runs[-1]["rel_IeqN"]
        if last_IeqN < first_IeqN * 0.5:
            print(f"  dIeq → dN convergence: rel_IeqN drops {first_IeqN:.2%} → "
                  f"{last_IeqN:.2%}")
            print(f"  The equilibrated static slice IS converging to the imposed")
            print(f"  Newton potential as the lattice refines — meaning the wave-")
            print(f"  equation static limit equals the Poisson solution in the continuum.")
        else:
            print(f"  dIeq → dN: rel_IeqN = {first_IeqN:.2%} → {last_IeqN:.2%} "
                  f"(not converging)")

        # Main verdict: does MIeq converge where MI did not?
        if last_MIeq_change < rel_tol and last_MI_change > rel_tol:
            print(f"\n  IMPROVED — equilibrated-static rel_MIeq converges")
            print(f"  ({last_MIeq_change:.4f} < {rel_tol}) where the NL_dyn cached")
            print(f"  static rel_MI did not ({last_MI_change:.4f}).")
            print(f"  The dI instability WAS incomplete equilibration.")
            print(f"  Continuum-limit rel_MIeq ≈ {runs[-1]['rel_MIeq']:.2%}")
        elif last_MIeq_change < last_MI_change * 0.5:
            print(f"\n  PARTIAL — equilibrated static is more stable than cached static")
            print(f"  (Δ_MIeq = {last_MIeq_change:.4f} < Δ_MI = {last_MI_change:.4f})")
            print(f"  but neither is strictly converged.")
        elif last_MIeq_change < last_MI_change:
            print(f"\n  MARGINAL — equilibrated static marginally better than cached static")
        else:
            print(f"\n  NEGATIVE — equilibrated static is no better than cached static")
            print(f"  (Δ_MIeq = {last_MIeq_change:.4f} ≥ Δ_MI = {last_MI_change:.4f})")
            print(f"  The dI instability is NOT just incomplete equilibration.")


if __name__ == "__main__":
    main()
