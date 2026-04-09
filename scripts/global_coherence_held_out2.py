#!/usr/bin/env python3
"""Larger held-out batch for the global coherence predictor.

The previous lane (global_coherence_predictor.py) found:
    free_coh >= 7.96e-04 -> in-sample 92.3%, cross-gen 7/9 = 77.8%
on the original 9 cross-generator families. This lane builds 12 NEW
generators (not in either previous set) and pre-commits TWO predictions
per family BEFORE running:

    coh_high   : my structural intuition for whether free_coh > threshold
    pass       : my structural intuition for whether the package passes

Then the harness measures both, so the audit trail covers:

    L1 (coh sign):   how often is the structural intuition for free_coh right?
    L2 (rule):       does free_coh >= 7.96e-04 generalize to a new batch
                     without refitting?
    L3 (pre-pass):   how often is the package pass/fail intuition right?

If L2 stays near 78% on a fresh batch the +11 points is real, not a
fluke. If L2 drops, the previous lane's revival is suspect. Either
outcome is decisive on the question of whether free_coh is a real
generator-agnostic predictor.

All 12 new generators are placed on the same (layer, iy, iz) grid
scaffolding so the wave-equation field measurement still works. Edge
topologies are independent of both the original neighbor square stencil
AND the first cross-generator batch.
"""

from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import independent_generators_heldout as ind
from global_coherence_predictor import free_beam_metrics, annotate

NL = ind.NL
PW = ind.PW
H = ind.H

# Threshold from the previous lane (frozen, no refitting)
FREE_COH_THRESHOLD = 7.9597e-04


def _make_grid(seed):
    return ind._make_grid(seed)


def _layer_coords():
    hw = int(PW / H)
    return [(iy, iz) for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]


# ========== NEW GENERATORS ==========

def grow_kreg_super_dense(seed, k):
    """Random k-regular forward at very high k (test density threshold)."""
    return ind.grow_random_kreg(seed, k)


def grow_skip2(seed):
    """Neighbor square stencil + skip connections to t+2 (similar to grown-DAG)."""
    pos, nmap = _make_grid(seed)
    hw = int(PW / H)
    md = max(1, round(3 / H))
    adj = {}
    coords = _layer_coords()
    for layer in range(NL - 1):
        if layer == 0:
            sources = [(0, 0, 0)]
        else:
            sources = [(layer, iy, iz) for (iy, iz) in coords]
        for src_key in sources:
            si = nmap[src_key]
            _, sy, sz = src_key
            for dy in range(-md, md + 1):
                for dz in range(-md, md + 1):
                    j = nmap.get((layer + 1, sy + dy, sz + dz))
                    if j is not None:
                        adj.setdefault(si, []).append(j)
            if layer + 2 < NL:
                for dy in range(-md, md + 1):
                    for dz in range(-md, md + 1):
                        j = nmap.get((layer + 2, sy + dy, sz + dz))
                        if j is not None:
                            adj.setdefault(si, []).append(j)
    return pos, adj, nmap


def grow_small_world(seed, p_long):
    """Local neighbor square stencil + a few random long-range shortcuts."""
    pos, nmap = _make_grid(seed)
    rng = random.Random(seed + 6000)
    hw = int(PW / H)
    md = max(1, round(3 / H))
    adj = {}
    coords = _layer_coords()
    for layer in range(NL - 1):
        if layer == 0:
            sources = [(0, 0, 0)]
        else:
            sources = [(layer, iy, iz) for (iy, iz) in coords]
        next_pool = [nmap[(layer + 1, iy, iz)] for (iy, iz) in coords]
        for src_key in sources:
            si = nmap[src_key]
            _, sy, sz = src_key
            for dy in range(-md, md + 1):
                for dz in range(-md, md + 1):
                    j = nmap.get((layer + 1, sy + dy, sz + dz))
                    if j is not None:
                        adj.setdefault(si, []).append(j)
            for j in next_pool:
                if rng.random() < p_long and j not in adj.get(si, []):
                    adj.setdefault(si, []).append(j)
    return pos, adj, nmap


def grow_bipartite_match(seed):
    """Strict bipartite: each layer is fully bipartite-matched to next."""
    pos, nmap = _make_grid(seed)
    rng = random.Random(seed + 7000)
    hw = int(PW / H)
    adj = {}
    coords = _layer_coords()
    for layer in range(NL - 1):
        if layer == 0:
            sources = [0]
        else:
            sources = [nmap[(layer, iy, iz)] for (iy, iz) in coords]
        next_pool = [nmap[(layer + 1, iy, iz)] for (iy, iz) in coords]
        # random perfect matching (extend if sizes differ)
        rng.shuffle(next_pool)
        for i, src in enumerate(sources):
            adj[src] = [next_pool[i % len(next_pool)]]
    return pos, adj, nmap


def grow_band_random(seed, k, band):
    """Random k-regular but only within a band of |dy|,|dz| <= band."""
    pos, nmap = _make_grid(seed)
    rng = random.Random(seed + 8000)
    hw = int(PW / H)
    adj = {}
    coords = _layer_coords()
    for layer in range(NL - 1):
        if layer == 0:
            sources = [(0, 0, 0)]
        else:
            sources = [(layer, iy, iz) for (iy, iz) in coords]
        for src_key in sources:
            si = nmap[src_key]
            _, sy, sz = src_key
            pool = []
            for dy in range(-band, band + 1):
                for dz in range(-band, band + 1):
                    j = nmap.get((layer + 1, sy + dy, sz + dz))
                    if j is not None:
                        pool.append(j)
            picks = rng.sample(pool, min(k, len(pool)))
            adj[si] = list(picks)
    return pos, adj, nmap


def grow_twisted(seed, twist_per_layer):
    """Neighbor square stencil but rotated by twist_per_layer cells per layer."""
    pos, nmap = _make_grid(seed)
    hw = int(PW / H)
    md = max(1, round(3 / H))
    adj = {}
    coords = _layer_coords()
    for layer in range(NL - 1):
        if layer == 0:
            sources = [(0, 0, 0)]
        else:
            sources = [(layer, iy, iz) for (iy, iz) in coords]
        twist = layer * twist_per_layer
        for src_key in sources:
            si = nmap[src_key]
            _, sy, sz = src_key
            for dy in range(-md, md + 1):
                for dz in range(-md, md + 1):
                    # rotate the offset by twist (simple shear)
                    j = nmap.get((layer + 1, sy + dy + twist, sz + dz))
                    if j is not None:
                        adj.setdefault(si, []).append(j)
    return pos, adj, nmap


def grow_block_diag(seed, block_size):
    """Block-diagonal connectivity: nodes only connect within their block."""
    pos, nmap = _make_grid(seed)
    hw = int(PW / H)
    md = max(1, round(3 / H))
    adj = {}
    coords = _layer_coords()
    def block(iy, iz):
        return (iy // block_size, iz // block_size)
    for layer in range(NL - 1):
        if layer == 0:
            sources = [(0, 0, 0)]
        else:
            sources = [(layer, iy, iz) for (iy, iz) in coords]
        for src_key in sources:
            si = nmap[src_key]
            _, sy, sz = src_key
            sb = block(sy, sz)
            for dy in range(-md, md + 1):
                for dz in range(-md, md + 1):
                    ny, nz = sy + dy, sz + dz
                    if block(ny, nz) != sb:
                        continue
                    j = nmap.get((layer + 1, ny, nz))
                    if j is not None:
                        adj.setdefault(si, []).append(j)
    return pos, adj, nmap


def grow_1d_like(seed):
    """Only iy stays constant; neighbors only along the iz axis."""
    pos, nmap = _make_grid(seed)
    hw = int(PW / H)
    md = max(1, round(3 / H))
    adj = {}
    coords = _layer_coords()
    for layer in range(NL - 1):
        if layer == 0:
            sources = [(0, 0, 0)]
        else:
            sources = [(layer, iy, iz) for (iy, iz) in coords]
        for src_key in sources:
            si = nmap[src_key]
            _, sy, sz = src_key
            for dz in range(-md, md + 1):
                j = nmap.get((layer + 1, sy, sz + dz))
                if j is not None:
                    adj.setdefault(si, []).append(j)
    return pos, adj, nmap


def grow_permutation(seed):
    """Each source connects to a fixed pseudo-random permutation of next layer."""
    pos, nmap = _make_grid(seed)
    rng = random.Random(seed + 9000)
    hw = int(PW / H)
    adj = {}
    coords = _layer_coords()
    for layer in range(NL - 1):
        if layer == 0:
            sources = [0]
        else:
            sources = [nmap[(layer, iy, iz)] for (iy, iz) in coords]
        next_pool = [nmap[(layer + 1, iy, iz)] for (iy, iz) in coords]
        perm = list(next_pool)
        rng.shuffle(perm)
        for i, src in enumerate(sources):
            # each source gets a small slice of the permutation
            slice_size = 12
            start = (i * slice_size) % len(perm)
            adj[src] = [perm[(start + k) % len(perm)] for k in range(slice_size)]
    return pos, adj, nmap


def grow_anisotropic_random(seed, k):
    """Random k-regular biased toward small dz (asymmetric in measurement axis)."""
    pos, nmap = _make_grid(seed)
    rng = random.Random(seed + 10000)
    hw = int(PW / H)
    adj = {}
    coords = _layer_coords()
    for layer in range(NL - 1):
        if layer == 0:
            sources = [(0, 0, 0)]
        else:
            sources = [(layer, iy, iz) for (iy, iz) in coords]
        for src_key in sources:
            si = nmap[src_key]
            _, sy, sz = src_key
            # bias: pick with probability proportional to exp(-|dz|)
            pool = []
            weights = []
            for dy in range(-4, 5):
                for dz in range(-4, 5):
                    j = nmap.get((layer + 1, sy + dy, sz + dz))
                    if j is not None:
                        pool.append(j)
                        weights.append(math.exp(-abs(dz) - 0.5 * abs(dy)))
            # pick k weighted samples without replacement
            picks = []
            avail = list(zip(pool, weights))
            for _ in range(min(k, len(avail))):
                total = sum(w for _, w in avail)
                if total <= 0:
                    break
                roll = rng.uniform(0, total)
                acc = 0
                for idx, (j, w) in enumerate(avail):
                    acc += w
                    if acc >= roll:
                        picks.append(j)
                        avail.pop(idx)
                        break
            adj[si] = picks
    return pos, adj, nmap


# ========== PRE-COMMITTED PREDICTIONS ==========
# Hard-coded BEFORE running. Audit trail = these dicts in source.

PREDICTIONS_COH = {
    "N1_kreg_k30":     True,   # very dense random; LLN should give moderate coh
    "N2_kreg_k50":     True,   # ditto, even denser
    "N3_skip2":        True,   # spatial stencil, multi-layer; should be high
    "N4_smallworld":   True,   # local stencil dominates
    "N5_bipartite":    False,  # one-to-one matching, no path multiplicity
    "N6_band_random":  True,   # band restricts randomness, mild structure
    "N7_twisted":      False,  # rotation breaks per-layer Z2
    "N8_block_diag":   False,  # blocks isolate paths, coh suppressed
    "N9_1d_like":      False,  # no transverse mixing
    "N10_permutation": False,  # randomized like random k-reg
    "N11_aniso_rand":  False,  # asymmetric in z, breaks coh
    "N12_kreg_k4":     False,  # too sparse
}

PREDICTIONS_PASS = {
    "N1_kreg_k30":     True,   # high density, LLN, similar to E1
    "N2_kreg_k50":     True,   # even higher density
    "N3_skip2":        True,   # behaves like dense grown-DAG
    "N4_smallworld":   True,   # local stencil should give the package
    "N5_bipartite":    False,  # too restrictive
    "N6_band_random":  True,   # mild structure should be enough
    "N7_twisted":      False,  # broken Z2 in measurement axis
    "N8_block_diag":   False,  # blocks break global coherence
    "N9_1d_like":      False,  # no mixing in y
    "N10_permutation": False,  # random
    "N11_aniso_rand":  False,  # asymmetric
    "N12_kreg_k4":     False,  # sparse
}


def make_new_families():
    return [
        ("N1_kreg_k30",     lambda: grow_kreg_super_dense(0, 30)),
        ("N2_kreg_k50",     lambda: grow_kreg_super_dense(0, 50)),
        ("N3_skip2",        lambda: grow_skip2(0)),
        ("N4_smallworld",   lambda: grow_small_world(0, 0.05)),
        ("N5_bipartite",    lambda: grow_bipartite_match(0)),
        ("N6_band_random",  lambda: grow_band_random(0, 12, 2)),
        ("N7_twisted",      lambda: grow_twisted(0, 1)),
        ("N8_block_diag",   lambda: grow_block_diag(0, 4)),
        ("N9_1d_like",      lambda: grow_1d_like(0)),
        ("N10_permutation", lambda: grow_permutation(0)),
        ("N11_aniso_rand",  lambda: grow_anisotropic_random(0, 12)),
        ("N12_kreg_k4",     lambda: grow_kreg_super_dense(0, 4)),
    ]


def main():
    print("=" * 100)
    print("GLOBAL COHERENCE — LARGER HELD-OUT BATCH (12 NEW GENERATORS)")
    print(f"Frozen rule: free_coh >= {FREE_COH_THRESHOLD:.4e}")
    print("Predictions hard-coded BEFORE running. Rule applied WITHOUT refit.")
    print("=" * 100)

    families = make_new_families()
    results = []
    for i, (name, builder) in enumerate(families, 1):
        print(f"\n[{i:2d}/{len(families)}] {name:22s}", end="", flush=True)
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            annotate(r, pos, adj, nmap, NL, PW)
            results.append(r)
            tag = "PASS" if r["pass"] else "FAIL"
            print(f"  {tag}  avg_deg={r['avg_deg']:.1f}  "
                  f"free_coh={r['free_coh']:.4e}  delta={r['delta']:+.4f}")
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"name": name, "pass": False, "error": str(e)})

    # Summary table
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(f"{'family':22s} {'avg_deg':>8s} {'free_coh':>12s} {'p_det':>11s}"
          f" {'delta':>9s} {'pass':>6s}")
    print("-" * 100)
    for r in results:
        if "error" in r:
            print(f"{r['name']:22s}  ERROR")
            continue
        print(f"{r['name']:22s} {r['avg_deg']:8.2f} {r['free_coh']:12.4e} "
              f"{r['free_p_det']:11.3e} {r['delta']:+9.4f} "
              f"{('PASS' if r['pass'] else 'FAIL'):>6s}")

    n_pass = sum(1 for r in results if r.get("pass"))
    n_fail = sum(1 for r in results if not r.get("pass") and "error" not in r)
    print(f"\nactual: PASS {n_pass} / FAIL {n_fail}")

    # Level 1: free_coh sign predictions
    print("\nL1. PRE-COMMITTED free_coh sign vs actual high/low (threshold 7.96e-04)")
    print(f"{'family':22s} {'predicted':>10s} {'actual':>8s} {'agree':>7s}")
    L1_correct = 0
    L1_n = 0
    for r in results:
        if "error" in r:
            continue
        L1_n += 1
        committed = PREDICTIONS_COH.get(r["name"])
        actual = r["free_coh"] >= FREE_COH_THRESHOLD
        agree = (committed == actual)
        if agree:
            L1_correct += 1
        print(f"{r['name']:22s} {str(committed):>10s} {str(actual):>8s} "
              f"{('OK' if agree else 'MISS'):>7s}")
    print(f"\nL1 free_coh sign accuracy: {L1_correct}/{L1_n} = {L1_correct/max(L1_n,1):.1%}")

    # Level 2: rule applied to measured free_coh
    print("\nL2. FROZEN RULE (free_coh >= 7.96e-04) applied to measured free_coh")
    print(f"{'family':22s} {'rule':>6s} {'actual':>8s} {'agree':>7s}")
    L2_correct = 0
    for r in results:
        if "error" in r:
            continue
        rule_pred = r["free_coh"] >= FREE_COH_THRESHOLD
        agree = (rule_pred == r["pass"])
        if agree:
            L2_correct += 1
        print(f"{r['name']:22s} {str(rule_pred):>6s} {str(r['pass']):>8s} "
              f"{('OK' if agree else 'MISS'):>7s}")
    print(f"\nL2 frozen rule accuracy: {L2_correct}/{L1_n} = {L2_correct/max(L1_n,1):.1%}")

    # Level 3: pre-committed pass/fail
    print("\nL3. PRE-COMMITTED package pass/fail predictions")
    print(f"{'family':22s} {'predicted':>10s} {'actual':>8s} {'agree':>7s}")
    L3_correct = 0
    for r in results:
        if "error" in r:
            continue
        committed = PREDICTIONS_PASS.get(r["name"])
        agree = (committed == r["pass"])
        if agree:
            L3_correct += 1
        print(f"{r['name']:22s} {str(committed):>10s} {str(r['pass']):>8s} "
              f"{('OK' if agree else 'MISS'):>7s}")
    print(f"\nL3 pre-committed pass/fail accuracy: {L3_correct}/{L1_n} = {L3_correct/max(L1_n,1):.1%}")

    # Comparison to old node-level rule on same batch
    print("\nCOMPARISON to old node-level rule (avg_deg >= 10.42 AND reach_frac >= 0.86)")
    old_correct = sum(
        1 for r in results
        if "error" not in r
        and (r["avg_deg"] >= 10.415 and r["reach_frac"] >= 0.859) == r["pass"]
    )
    print(f"  old 2-prop on this batch: {old_correct}/{L1_n} = {old_correct/max(L1_n,1):.1%}")
    print(f"  new free_coh on this batch: {L2_correct}/{L1_n} = {L2_correct/max(L1_n,1):.1%}")

    print("\nVERDICT")
    rate_old_first = 6 / 9   # from previous lane
    rate_new_first = 7 / 9
    rate_new_now = L2_correct / max(L1_n, 1)
    rate_old_now = old_correct / max(L1_n, 1)
    if rate_new_now >= 0.65:
        print(f"  CONFIRMED — frozen rule generalizes to a fresh batch at {rate_new_now:.0%}")
        if rate_new_now > rate_old_now + 0.05:
            print(f"    and beats the old node-level rule by "
                  f"{rate_new_now - rate_old_now:+.0%}")
    elif rate_new_now >= 0.50:
        print(f"  PARTIAL — frozen rule at {rate_new_now:.0%}, weaker than first batch")
    else:
        print(f"  REFUTED — frozen rule at {rate_new_now:.0%}, the previous +11 was a fluke")


if __name__ == "__main__":
    main()
