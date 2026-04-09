#!/usr/bin/env python3
"""Continuum-limit test of the true first-order Kubo coefficient.

Lane α of the overnight iteration. The previous continuum-limit
lane (wave_retardation_continuum_limit.py) showed that:
  1. dM (retarded wave field deflection) is continuum-stable — only
     14% monotone drift across an 8× lattice density change.
  2. All three tested c=∞ comparators (dI, dIeq, dN) fail to
     converge cleanly.

This lane sidesteps the comparator question entirely. It asks:

  Does the true first-order Kubo coefficient `kubo_true = d(cz)/ds`
  at s = 0 converge in the continuum limit?

`kubo_true` is computed by the parallel perturbation propagator from
`linear_response_true_kubo.py` — no comparator, no dynamic evolution,
just the symbolic first-order derivative of the propagator at s=0
on a STATIC grown-DAG lattice with the imposed 1/r field.

Physical parameters held approximately constant across refinements:
  T_phys = NL * H = 15.0  (total propagation length)
  PW_phys = 6.0            (transverse half-width)
  k*H = 2.5                (phase per edge step)
  S_phys = 0.004           (source strength — used only to set the scale)
  mass position (x, z) = (NL//3 * H, MASS_Z_PHYS = 3.0)

Refinement: H ∈ {0.5, 0.35, 0.25}
(memory-feasible, matching the companion continuum-limit lane)

If kubo_true converges cleanly (Δ < 5% at the last step), we have a
direct continuum prediction for the linear gravitational response
coefficient that does not depend on any c=∞ comparator.
"""

from __future__ import annotations

import math
import random

# Physical parameters
T_PHYS = 15.0
PW_PHYS = 6.0
K_PER_H = 2.5
S_PHYS = 0.004
MASS_Z_PHYS = 3.0
SRC_LAYER_FRAC = 1.0 / 3.0
BETA = 0.8


def grow(seed, drift, restore, NL, PW, max_d_phys, H):
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


def true_kubo_at_H(pos, adj, NL, PW, H, k_phase, x_src, z_src, beta=BETA):
    """Parallel perturbation propagator for the static-gravity Kubo coefficient.

    Returns (dM_at_small_s, kubo_true, cz_free).

    - A_j = Σ amp at node j (free propagation)
    - B_j = d(amp_j)/ds at s=0 (parallel perturbation propagator)
    - kubo_true = d(cz)/ds at s=0 via chain rule
    - dM_at_small_s = finite-difference measurement at s=S_PHYS for
      cross-check with kubo_true * S_PHYS

    Imposed field: f = s / (r_field), where
      r_field = sqrt((mx - x_src)^2 + (mz - z_src)^2) + 0.1
      (single regularized distance, same convention as the main Kubo lane)
    """
    n = len(pos)
    A = [0j] * n
    B = [0j] * n
    A[0] = 1.0 + 0j
    order = sorted(range(n), key=lambda i: pos[i][0])
    h2 = H * H
    for i in order:
        ai = A[i]
        bi = B[i]
        if abs(ai) < 1e-30 and abs(bi) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            mx = 0.5 * (pos[i][0] + pos[j][0])
            mz = 0.5 * (pos[i][2] + pos[j][2])
            r_field = math.sqrt((mx - x_src) ** 2 + (mz - z_src) ** 2) + 0.1
            phase = k_phase * L
            phi = complex(math.cos(phase), math.sin(phase))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-beta * theta * theta)
            w_eff = w * h2 / (L * L)
            weight = phi * w_eff
            dphi_ds = complex(0.0, -k_phase * L / r_field) * phi
            A[j] += ai * weight
            B[j] += (bi * phi + ai * dphi_ds) * w_eff
    # Detector slice: nodes at layer NL-1
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds_idx = n - npl
    weights = [abs(A[k]) ** 2 for k in range(ds_idx, n)]
    zs = [pos[k][2] for k in range(ds_idx, n)]
    T0 = sum(weights)
    if T0 <= 0:
        return 0.0, 0.0, 0.0
    cz_free = sum(w * z for w, z in zip(weights, zs)) / T0
    # chain rule: d(cz)/ds = (Σ 2 Re[A*B] z)/T0 - cz_free * (Σ 2 Re[A*B])/T0
    dT_ds = sum(2.0 * (A[k].conjugate() * B[k]).real for k in range(ds_idx, n))
    dN_ds = sum(2.0 * (A[k].conjugate() * B[k]).real * pos[k][2]
                for k in range(ds_idx, n))
    N0 = T0 * cz_free
    kubo = dN_ds / T0 - N0 * dT_ds / (T0 * T0)
    return kubo, cz_free, T0


def finite_diff_dM(pos, adj, NL, PW, H, k_phase, x_src, z_src, s, beta=BETA):
    """Measure the static dM (cz displacement) at a small source strength s
    via direct beam propagation (no parallel propagator), for cross-check."""
    n = len(pos)
    field = [s / (math.sqrt((p[0] - x_src) ** 2 + (p[2] - z_src) ** 2) + 0.1)
             for p in pos]

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
            w = math.exp(-beta * theta * theta)
            amps[j] += amps[i] * complex(math.cos(phase), math.sin(phase)) * w * h2 / (L * L)
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    ds_idx = n - npl
    weights = [abs(amps[k]) ** 2 for k in range(ds_idx, n)]
    zs = [pos[k][2] for k in range(ds_idx, n)]
    T0 = sum(weights)
    if T0 <= 0:
        return 0.0
    return sum(w * z for w, z in zip(weights, zs)) / T0


def measure_at_H(H_val, label):
    NL = max(3, round(T_PHYS / H_val))
    PW = PW_PHYS
    k_phase = K_PER_H / H_val
    x_src = round(NL * SRC_LAYER_FRAC) * H_val
    z_src = MASS_Z_PHYS

    pos, adj, nmap = grow(0, 0.20, 0.70, NL, PW, 3, H_val)
    kubo, cz_free, T0 = true_kubo_at_H(pos, adj, NL, PW, H_val, k_phase, x_src, z_src)

    # Finite-difference cross-check at s = S_PHYS and s = 0
    cz_0 = finite_diff_dM(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, 0.0)
    cz_s = finite_diff_dM(pos, adj, NL, PW, H_val, k_phase, x_src, z_src, S_PHYS)
    dM_fd = (cz_s - cz_0) / S_PHYS  # effective "kubo" from finite difference

    return {
        "label": label, "H": H_val, "NL": NL, "n_nodes": len(pos),
        "k_phase": k_phase, "x_src": x_src, "z_src": z_src,
        "kubo_true": kubo, "dM_fd": dM_fd,
        "cz_free": cz_free, "T0": T0,
    }


def main():
    print("=" * 100)
    print("CONTINUUM LIMIT OF THE TRUE FIRST-ORDER KUBO COEFFICIENT")
    print(f"Physical: T={T_PHYS}, PW={PW_PHYS}, k*H={K_PER_H}, "
          f"S={S_PHYS}, z_src={MASS_Z_PHYS}")
    print("Refinement: H ∈ {0.5, 0.35, 0.25}")
    print("Measured: kubo_true = d(cz)/ds at s=0 via parallel perturbation propagator")
    print("          dM_fd = finite-difference d(cz)/ds at s=S_PHYS for cross-check")
    print("=" * 100)

    runs = []
    for H_val, label in [(0.5, "coarse"), (0.35, "medium"), (0.25, "fine")]:
        print(f"\n[{label}] H = {H_val}", flush=True)
        r = measure_at_H(H_val, label)
        runs.append(r)
        print(f"  NL = {r['NL']},  k_phase = {r['k_phase']:.3f},  "
              f"x_src = {r['x_src']:.3f},  z_src = {r['z_src']:.3f}")
        print(f"  n_nodes = {r['n_nodes']},  T0 = {r['T0']:.3e},  "
              f"cz_free = {r['cz_free']:+.6f}")
        print(f"  kubo_true (parallel prop) = {r['kubo_true']:+.6f}")
        print(f"  dM_fd (finite diff at s={S_PHYS}) = {r['dM_fd']:+.6f}")
        agree = abs(r['kubo_true'] - r['dM_fd']) / max(abs(r['kubo_true']), 1e-12)
        print(f"  kubo_true vs dM_fd agreement: {agree:.2%}  (should be small)")

    print("\n" + "=" * 100)
    print("REFINEMENT TABLE")
    print("=" * 100)
    print(f"{'label':>10s} {'H':>6s} {'NL':>5s} {'kubo_true':>14s} "
          f"{'dM_fd':>14s} {'ratio':>10s}")
    for r in runs:
        ratio = r['dM_fd'] / r['kubo_true'] if abs(r['kubo_true']) > 1e-12 else 0.0
        print(f"{r['label']:>10s} {r['H']:6.3f} {r['NL']:>5d} "
              f"{r['kubo_true']:+14.6f} {r['dM_fd']:+14.6f} {ratio:10.4f}")

    print("\n" + "=" * 100)
    print("CONVERGENCE")
    print("=" * 100)
    for i in range(len(runs) - 1):
        r1, r2 = runs[i], runs[i + 1]
        d_kubo = r2['kubo_true'] - r1['kubo_true']
        rel_kubo = d_kubo / r1['kubo_true'] if abs(r1['kubo_true']) > 1e-12 else 0.0
        d_fd = r2['dM_fd'] - r1['dM_fd']
        rel_fd = d_fd / r1['dM_fd'] if abs(r1['dM_fd']) > 1e-12 else 0.0
        print(f"  {r1['label']:>8s} → {r2['label']:>8s}: "
              f"Δkubo_true = {d_kubo:+.6f} ({rel_kubo:+.1%}), "
              f"Δdm_fd = {d_fd:+.6f} ({rel_fd:+.1%})")

    # Verdict
    print("\n" + "=" * 100)
    print("VERDICT")
    print("=" * 100)
    if len(runs) >= 2:
        last_dkubo = abs(runs[-1]['kubo_true'] - runs[-2]['kubo_true'])
        last_rel = last_dkubo / abs(runs[-2]['kubo_true']) if abs(runs[-2]['kubo_true']) > 1e-12 else 0.0
        tol = 0.05
        print(f"  Last refinement Δ(kubo_true) = {last_dkubo:.6f} "
              f"({last_rel:.1%} of previous)")
        if last_rel < tol:
            print(f"  CONVERGING — kubo_true is changing by less than {tol:.0%}")
            print(f"  at the last refinement step.")
            print(f"  Continuum-limit value appears to be ≈ {runs[-1]['kubo_true']:+.4f}")
            print(f"\n  This is a DIRECT continuum prediction for the linear")
            print(f"  gravitational response coefficient, independent of any c=∞")
            print(f"  comparator. It is the cleanest physics result the program")
            print(f"  has for the continuum limit of gravity on the grown DAG.")
        else:
            print(f"  NOT CONVERGED at {tol:.0%} tolerance. Monotone drift of "
                  f"{last_rel:.1%} per refinement step.")
            print(f"  Either the continuum limit needs finer lattice, or")
            print(f"  kubo_true has its own lattice-artifact dependence.")


if __name__ == "__main__":
    main()
