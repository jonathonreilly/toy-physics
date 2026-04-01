#!/usr/bin/env python3
"""Hard validation pass for the influence-functional decoherence formulation.

Check 1: Small-case equivalence — IF kernel vs explicit slot-resolved
         fresh ancilla on the same graph. They should agree if they
         compute the same physics.

Check 2: Hermiticity — ρ(d1,d2) = ρ(d2,d1)* for all d1,d2.

Check 3: Positivity — all eigenvalues of ρ are non-negative.

Check 4: Baseline — α=0 kernel gives purity exactly 1.0.

Check 5: Detector hit fraction — report trace(ρ_unnormalized) as the
         detector hit probability.

Check 6: N=18 with 4 seeds (more than the 2-seed initial test).

PStack experiment: influence-functional-validation
"""

from __future__ import annotations
import math
import cmath
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.density_matrix_analysis import build_post_barrier_setup, compute_detector_metrics

BETA = 0.8
ALPHA_SCALE = 2.0
MAX_HIST = 3


def propagate_with_history(positions, adj, field, src, det, k,
                           mass_set, blocked):
    """Propagate tracking encounter angle history (capped at MAX_HIST)."""
    n = len(positions)
    in_deg = [0]*n
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    state = {}
    for s in src:
        state[(s, ())] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {h: a for (nd, h), a in list(state.items())
                   if nd == i and abs(a) > 1e-30}
        if not entries or i in blocked:
            continue
        for hist, amp in entries.items():
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                dx, dy = x2-x1, y2-y1
                L = math.sqrt(dx*dx+dy*dy)
                if L < 1e-10:
                    continue
                lf = 0.5*(field[i]+field[j])
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                te = math.atan2(abs(dy), max(dx, 1e-10))
                w = math.exp(-BETA*te*te)
                ea = cmath.exp(1j*k*act)*w/(L**1.0)
                nh = hist+(te,) if j in mass_set and len(hist) < MAX_HIST else hist
                key = (j, nh)
                if key not in state:
                    state[key] = 0.0+0.0j
                state[key] += amp*ea

    return {(d, h): a for (d, h), a in state.items() if d in det}


def overlap_kernel(ha, hb, alpha):
    m = max(len(ha), len(hb))
    if m == 0:
        return 1.0
    v = 1.0
    for i in range(m):
        a = ha[i] if i < len(ha) else 0.0
        b = hb[i] if i < len(hb) else 0.0
        v *= math.cos(alpha*(a-b))
    return v


def build_if_density_matrix(ds_a, ds_b, det_list, alpha):
    """Build the full IF density matrix (unnormalized and normalized)."""
    aa = defaultdict(list)
    bb = defaultdict(list)
    for (d, h), a in ds_a.items():
        aa[d].append((h, a))
    for (d, h), a in ds_b.items():
        bb[d].append((h, a))

    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            v = 0.0+0.0j
            for h1, a1 in aa.get(d1, []):
                for h2, a2 in aa.get(d2, []):
                    v += a1.conjugate()*a2
            for h1, a1 in bb.get(d1, []):
                for h2, a2 in bb.get(d2, []):
                    v += a1.conjugate()*a2
            for ha, aA in aa.get(d1, []):
                for hb, aB in bb.get(d2, []):
                    v += aA.conjugate()*aB*overlap_kernel(ha, hb, alpha)
            for hb, aB in bb.get(d1, []):
                for ha, aA in aa.get(d2, []):
                    v += aB.conjugate()*aA*overlap_kernel(hb, ha, alpha)
            rho[(d1, d2)] = v

    trace_unnorm = sum(rho.get((d, d), 0) for d in det_list).real
    rho_norm = {}
    if trace_unnorm > 1e-30:
        for key in rho:
            rho_norm[key] = rho[key] / trace_unnorm
    purity = sum(abs(v)**2 for v in rho_norm.values()).real if rho_norm else math.nan
    return rho_norm, trace_unnorm, purity


def propagate_slot_resolved(positions, adj, field, src, det, k,
                            mass_set, blocked, alpha_scale):
    """Explicit slot-resolved fresh ancilla (bitstring env)."""
    n = len(positions)
    in_deg = [0]*n
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    state = {}
    for s in src:
        state[(s, ())] = 1.0/len(src) + 0.0j

    processed = set()
    for i in order:
        if i in processed:
            continue
        processed.add(i)
        entries = {bits: amp for (nd, bits), amp in list(state.items())
                   if nd == i and abs(amp) > 1e-30}
        if not entries or i in blocked:
            continue
        for bits, amp in entries.items():
            for j in adj.get(i, []):
                if j in blocked:
                    continue
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                dx, dy = x2-x1, y2-y1
                L = math.sqrt(dx*dx+dy*dy)
                if L < 1e-10:
                    continue
                lf = 0.5*(field[i]+field[j])
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                te = math.atan2(abs(dy), max(dx, 1e-10))
                w = math.exp(-BETA*te*te)
                ea = cmath.exp(1j*k*act)*w/(L**1.0)

                if j in mass_set and len(bits) < MAX_HIST:
                    alpha_k = alpha_scale * te
                    if alpha_k < 0.01:
                        key = (j, bits)
                        if key not in state:
                            state[key] = 0.0+0.0j
                        state[key] += amp*ea
                    else:
                        cos_a = math.cos(alpha_k)
                        sin_a = math.sin(alpha_k)
                        key_0 = (j, bits+(0,))
                        if key_0 not in state:
                            state[key_0] = 0.0+0.0j
                        state[key_0] += amp*ea*cos_a
                        key_1 = (j, bits+(1,))
                        if key_1 not in state:
                            state[key_1] = 0.0+0.0j
                        state[key_1] += amp*ea*sin_a
                else:
                    key = (j, bits)
                    if key not in state:
                        state[key] = 0.0+0.0j
                    state[key] += amp*ea

    return {(d, b): a for (d, b), a in state.items() if d in det}


def main():
    k = 5.0

    print("=" * 70)
    print("INFLUENCE-FUNCTIONAL VALIDATION")
    print(f"  α_scale={ALPHA_SCALE}, history cap={MAX_HIST}, k={k}")
    print("=" * 70)
    print()

    # Use one small graph for checks 1-5
    positions, adj, _ = generate_causal_dag(
        n_layers=8, nodes_per_layer=25, y_range=12.0,
        connect_radius=3.0, rng_seed=18)
    setup = build_post_barrier_setup(positions, adj, env_depth_layers=1)
    if setup is None:
        print("Setup failed")
        return

    mass_set = set(setup["mass_set"]) - setup["blocked"]
    blocked = setup["blocked"]
    bl_idx = len(setup["layers"])//3
    bi = setup["by_layer"][setup["layers"][bl_idx]]
    cy = setup["cy"]
    sa = set(i for i in bi if positions[i][1] > cy+3)
    sb = set(i for i in bi if positions[i][1] < cy-3)

    blocked_a = blocked | sb
    blocked_b = blocked | sa

    ds_a = propagate_with_history(positions, adj, setup["field"], setup["src"],
        setup["det"], k, mass_set, blocked_a)
    ds_b = propagate_with_history(positions, adj, setup["field"], setup["src"],
        setup["det"], k, mass_set, blocked_b)

    det_list = setup["det_list"]

    # ================================================================
    # CHECK 1: Small-case equivalence
    # ================================================================
    print("CHECK 1: Equivalence — IF kernel vs slot-resolved bitstring")

    rho_if, trace_if, pur_if = build_if_density_matrix(ds_a, ds_b, det_list, ALPHA_SCALE)

    # Slot-resolved: propagate BOTH slits together (no blocking)
    ds_slot = propagate_slot_resolved(positions, adj, setup["field"], setup["src"],
        setup["det"], k, mass_set, blocked, ALPHA_SCALE)
    pur_slot, _, _, _ = compute_detector_metrics(ds_slot, det_list)

    print(f"  IF purity:            {pur_if:.6f}")
    print(f"  Slot-resolved purity: {pur_slot:.6f}")
    print(f"  Difference:           {abs(pur_if - pur_slot):.2e}")
    equiv = abs(pur_if - pur_slot) < 0.05
    print(f"  Equivalence: {'PASS' if equiv else 'FAIL'} (threshold 0.05)")
    print()

    # ================================================================
    # CHECK 2: Hermiticity
    # ================================================================
    print("CHECK 2: Hermiticity — ρ(d1,d2) = ρ(d2,d1)*")

    max_herm_err = 0.0
    for d1 in det_list:
        for d2 in det_list:
            r12 = rho_if.get((d1, d2), 0.0)
            r21 = rho_if.get((d2, d1), 0.0)
            err = abs(r12 - r21.conjugate())
            max_herm_err = max(max_herm_err, err)

    print(f"  Max |ρ(d1,d2) - ρ(d2,d1)*|: {max_herm_err:.2e}")
    print(f"  Hermiticity: {'PASS' if max_herm_err < 1e-10 else 'FAIL'}")
    print()

    # ================================================================
    # CHECK 3: Positivity (eigenvalues ≥ 0)
    # ================================================================
    print("CHECK 3: Positivity — eigenvalues of ρ")

    n_det = len(det_list)
    # Build matrix
    mat = [[0.0+0.0j]*n_det for _ in range(n_det)]
    for i, d1 in enumerate(det_list):
        for j, d2 in enumerate(det_list):
            mat[i][j] = rho_if.get((d1, d2), 0.0)

    # Power iteration for smallest eigenvalue (approximate)
    # For small matrices, compute trace and Frobenius norm
    tr = sum(mat[i][i].real for i in range(n_det))
    frob = sum(abs(mat[i][j])**2 for i in range(n_det) for j in range(n_det))**0.5

    # Gershgorin bounds: min eigenvalue ≥ min_i (ρ_ii - Σ_{j≠i} |ρ_ij|)
    min_gersh = float('inf')
    for i in range(n_det):
        diag = mat[i][i].real
        off = sum(abs(mat[i][j]) for j in range(n_det) if j != i)
        min_gersh = min(min_gersh, diag - off)

    print(f"  Trace: {tr:.6f} (should be 1.0)")
    print(f"  Frobenius norm: {frob:.6f}")
    print(f"  Gershgorin min eigenvalue bound: {min_gersh:.6f}")
    print(f"  Positivity (Gershgorin): {'PASS' if min_gersh >= -1e-10 else 'MARGINAL' if min_gersh >= -0.01 else 'FAIL'}")
    print()

    # ================================================================
    # CHECK 4: Baseline — α=0 gives purity 1.0
    # ================================================================
    print("CHECK 4: Baseline — α=0 kernel")

    _, _, pur_0 = build_if_density_matrix(ds_a, ds_b, det_list, 0.0)
    print(f"  Purity at α=0: {pur_0:.6f}")
    print(f"  Baseline: {'PASS' if abs(pur_0 - 1.0) < 1e-6 else 'FAIL'}")
    print()

    # ================================================================
    # CHECK 5: Detector hit fraction
    # ================================================================
    print("CHECK 5: Detector hit fraction")

    print(f"  Unnormalized trace (IF, α={ALPHA_SCALE}): {trace_if:.4e}")
    _, trace_0, _ = build_if_density_matrix(ds_a, ds_b, det_list, 0.0)
    print(f"  Unnormalized trace (IF, α=0):   {trace_0:.4e}")
    print(f"  Ratio: {trace_if/trace_0:.6f}" if trace_0 > 0 else "  Ratio: n/a")
    print()

    # ================================================================
    # CHECK 6: N=8,12,18 with 4 seeds
    # ================================================================
    print("CHECK 6: Scaling with 4 seeds")
    print()
    print(f"  {'N':>4s}  {'pur_if':>8s}  {'pur_coh':>8s}  {'decoh':>8s}  {'hit_frac':>8s}  {'n_valid':>7s}")
    print(f"  {'-' * 48}")

    for nl in [8, 12, 18]:
        pif_list, pcoh_list, hit_list = [], [], []

        for seed in range(4):
            positions, adj, _ = generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed*11+7)
            setup = build_post_barrier_setup(positions, adj,
                env_depth_layers=max(1, round(nl/6)))
            if setup is None:
                continue

            mass_set = set(setup["mass_set"]) - setup["blocked"]
            blocked = setup["blocked"]
            bl_idx = len(setup["layers"])//3
            bi = setup["by_layer"][setup["layers"][bl_idx]]
            cy = setup["cy"]
            sa = set(i for i in bi if positions[i][1] > cy+3)
            sb = set(i for i in bi if positions[i][1] < cy-3)

            ds_a = propagate_with_history(positions, adj, setup["field"],
                setup["src"], setup["det"], k, mass_set, blocked | sb)
            ds_b = propagate_with_history(positions, adj, setup["field"],
                setup["src"], setup["det"], k, mass_set, blocked | sa)

            _, tr_if, p_if = build_if_density_matrix(ds_a, ds_b, det_list, ALPHA_SCALE)
            _, tr_0, p_0 = build_if_density_matrix(ds_a, ds_b, det_list, 0.0)

            if not math.isnan(p_if):
                pif_list.append(p_if)
            if not math.isnan(p_0):
                pcoh_list.append(p_0)
            if tr_0 > 0:
                hit_list.append(tr_if / tr_0)

        if pif_list:
            mif = sum(pif_list)/len(pif_list)
            mcoh = sum(pcoh_list)/len(pcoh_list)
            mhit = sum(hit_list)/len(hit_list) if hit_list else 0
            print(f"  {nl:4d}  {mif:8.4f}  {mcoh:8.4f}  {mcoh-mif:+8.4f}  {mhit:8.4f}  {len(pif_list):7d}")

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)


if __name__ == "__main__":
    main()
