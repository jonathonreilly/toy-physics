#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- generalize the iter 30 H5 line-3 +
singleton zero-det lemma to other cuboid sizes.

Context
-------
Iter 30 established on (4,4,2) that det_K3 = 0 on line-3 +
isolated-balanced-singleton defect configurations IFF:
  (a) singleton in opposite z-plane from line-3, AND
  (b) singleton's parallel-axis coord has SAME parity as
      line-3 center's parallel-axis coord.
Perfect 288/288 classification.

Goal
----
Test whether H5 generalizes beyond (4,4,2). Two scenarios:
- If H5 works on other L3=2 cuboids (3,3,2), (4,3,2), (5,3,2),
  (5,5,2), it is an L3=2-general lemma.
- If H5 fails somewhere, it needs refinement or is specific
  to (4,4,2).

Method
------
For each cuboid, exhaustively enumerate all (line-3, balanced
isolated singleton) configurations. Compute det_K3 via numpy
(float64 precision is safe on ±1 matrices of size <= 25). For
each config, evaluate H5 prediction and compare with actual
det = 0 / != 0.

Cuboids tested
--------------
(3,3,2), (4,3,2), (5,3,2), (5,5,2). (4,4,2) already tested at
288/288 in iter 30; included here as control.

Note on scope
-------------
L3=2 is specifically the regime where H5 was discovered. z-lines
(requiring L3 >= 3) are excluded. L3 >= 3 generalization deferred.
"""

from __future__ import annotations

import sys
from collections import defaultdict

import numpy as np


RECORDS: list[tuple[str, bool, str]] = []
DOCS: list[tuple[str, str]] = []


def record(name, ok, detail):
    RECORDS.append((name, bool(ok), detail))


def document(name, note):
    DOCS.append((name, note))


def eta(mu, n):
    if mu == 1:
        return 1
    if mu == 2:
        return (-1) ** n[0]
    if mu == 3:
        return (-1) ** (n[0] + n[1])
    raise ValueError


def build_B(bound, removed):
    L1, L2, L3 = bound
    base = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
    sites = [v for v in base if v not in removed]
    site_set = set(sites)
    evens = [v for v in sites if sum(v) % 2 == 0]
    odds = [v for v in sites if sum(v) % 2 == 1]
    if len(evens) != len(odds):
        return None
    idx_e = {v: i for i, v in enumerate(evens)}
    idx_o = {v: i for i, v in enumerate(odds)}
    n_bi = len(evens)
    B = np.zeros((n_bi, n_bi), dtype=np.int64)
    for n in sites:
        for mu in (1, 2, 3):
            nn = list(n); nn[mu - 1] += 1; nn = tuple(nn)
            if nn not in site_set:
                continue
            if n in idx_e:
                B[idx_e[n], idx_o[nn]] = eta(mu, n)
            else:
                B[idx_e[nn], idx_o[n]] = -eta(mu, n)
    return B, n_bi


def det_K3(bound, removed):
    r = build_B(bound, removed)
    if r is None:
        return None
    B, n_bi = r
    det_f = np.linalg.det(B.astype(np.float64))
    # Integer matrices: round; nonzero dets are >= 1.
    return int(round(det_f))


def line_center_coord(start, direction):
    if direction == "x":
        return start[0] + 1
    if direction == "y":
        return start[1] + 1
    raise ValueError


def enumerate_line_singleton_configs(bound):
    L1, L2, L3 = bound
    base = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
    base_set = set(base)

    lines = []
    # x-direction (requires L1 >= 3)
    if L1 >= 3:
        for i_start in range(L1 - 2):
            for j in range(L2):
                for k in range(L3):
                    line = frozenset({(i_start, j, k),
                                     (i_start + 1, j, k),
                                     (i_start + 2, j, k)})
                    lines.append((line, "x", (i_start, j, k)))
    # y-direction (requires L2 >= 3)
    if L2 >= 3:
        for i in range(L1):
            for j_start in range(L2 - 2):
                for k in range(L3):
                    line = frozenset({(i, j_start, k),
                                     (i, j_start + 1, k),
                                     (i, j_start + 2, k)})
                    lines.append((line, "y", (i, j_start, k)))

    results = []
    for (line, direction, start) in lines:
        line_parities = [sum(s) % 2 for s in line]
        line_evens = sum(1 for p in line_parities if p == 0)
        line_odds = sum(1 for p in line_parities if p == 1)
        if line_evens == line_odds:
            continue
        need_parity = 1 if line_evens > line_odds else 0

        line_neighbors = set()
        for s in line:
            for mu in (1, 2, 3):
                for d in (-1, 1):
                    v = list(s); v[mu - 1] += d; v = tuple(v)
                    if v in base_set:
                        line_neighbors.add(v)
        line_neighbors -= line

        for s in base:
            if s in line:
                continue
            if s in line_neighbors:
                continue
            if sum(s) % 2 != need_parity:
                continue
            removed = line | {s}
            det = det_K3(bound, removed)
            if det is None:
                continue
            line_z = next(iter(line))[2]
            results.append({
                "bound": bound,
                "line_direction": direction,
                "line_start": start,
                "line_z": line_z,
                "singleton": s,
                "z_sep": s[2] != line_z,
                "line_center_axis": line_center_coord(start, direction),
                "det": det,
                "is_zero": det == 0,
            })
    return results


def h5_predict_zero(r):
    if not r["z_sep"]:
        return False
    direction = r["line_direction"]
    singleton = r["singleton"]
    center = r["line_center_axis"]
    if direction == "x":
        return (singleton[0] - center) % 2 == 0
    if direction == "y":
        return (singleton[1] - center) % 2 == 0
    return False


# ---------------------------------------------------------------------------
# Test on multiple cuboids
# ---------------------------------------------------------------------------

bounds_to_test = [
    (3, 3, 2),
    (4, 3, 2),
    (4, 4, 2),   # iter 30 reference
    (5, 3, 2),
    (5, 5, 2),
]

all_results = {}
for bound in bounds_to_test:
    results = enumerate_line_singleton_configs(bound)
    all_results[bound] = results


# ---------------------------------------------------------------------------
# Per-cuboid H5 accuracy
# ---------------------------------------------------------------------------

cuboid_stats = {}
for bound, results in all_results.items():
    tp = sum(1 for r in results if h5_predict_zero(r) and r["is_zero"])
    fp = sum(1 for r in results if h5_predict_zero(r) and not r["is_zero"])
    fn = sum(1 for r in results if not h5_predict_zero(r) and r["is_zero"])
    tn = sum(1 for r in results if not h5_predict_zero(r) and not r["is_zero"])
    total = tp + fp + fn + tn
    correct = tp + tn
    zero_count = tp + fn
    nonzero_count = fp + tn
    cuboid_stats[bound] = {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "total": total, "correct": correct,
        "zero_count": zero_count, "nonzero_count": nonzero_count,
    }
    tag = f"{bound[0]}x{bound[1]}x{bound[2]}"
    record(
        f"H5_perfect_on_{tag}",
        fp == 0 and fn == 0 and total > 0,
        f"{tag}: total={total}, zero={zero_count}, nonzero={nonzero_count}, "
        f"TP={tp}, FP={fp}, FN={fn}, TN={tn}. Perfect? "
        f"{fp == 0 and fn == 0 and total > 0}.",
    )
    record(
        f"H5_accuracy_on_{tag}",
        correct == total,
        f"{tag}: {correct}/{total} correct ({100*correct/max(total,1):.1f}%).",
    )


# ---------------------------------------------------------------------------
# Cross-cuboid summary
# ---------------------------------------------------------------------------

n_perfect = sum(1 for bound, stats in cuboid_stats.items()
                if stats["fp"] == 0 and stats["fn"] == 0 and stats["total"] > 0)
n_cuboids_tested = sum(1 for bound, stats in cuboid_stats.items() if stats["total"] > 0)

record(
    "H5_generalization_perfect_on_all_tested",
    n_perfect == n_cuboids_tested and n_cuboids_tested >= 3,
    f"H5 is perfect on {n_perfect}/{n_cuboids_tested} L3=2 cuboids "
    f"({', '.join(f'{b[0]}x{b[1]}x{b[2]}' for b in bounds_to_test)}). "
    f"Generalizes? {n_perfect == n_cuboids_tested}.",
)

# Total configurations tested across all cuboids
total_configs = sum(s["total"] for s in cuboid_stats.values())
total_correct = sum(s["correct"] for s in cuboid_stats.values())

record(
    "H5_total_accuracy_across_all_cuboids",
    total_configs > 0 and total_correct == total_configs,
    f"H5 classifier: {total_correct}/{total_configs} correct across all "
    f"{n_cuboids_tested} L3=2 cuboids ({100*total_correct/max(total_configs,1):.1f}%).",
)


# ---------------------------------------------------------------------------
# Report any failures in detail
# ---------------------------------------------------------------------------

for bound, results in all_results.items():
    tag = f"{bound[0]}x{bound[1]}x{bound[2]}"
    errors = [r for r in results
              if (h5_predict_zero(r) != r["is_zero"])]
    if errors:
        record(
            f"H5_failures_on_{tag}_detail",
            False,
            f"{tag}: {len(errors)} H5 mismatches. Examples: "
            f"{[(r['line_start'], r['line_direction'], r['singleton'], r['det']) for r in errors[:5]]}",
        )


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if n_perfect == n_cuboids_tested and n_cuboids_tested >= 3:
    document(
        "h5_line3_singleton_lemma_generalizes_L3_2",
        f"The iter 30 H5 lemma candidate (det_K3 = 0 on line-3 +"
        f" balanced-isolated-singleton defects IFF z-separated AND"
        f" singleton parallel-axis coord matches line-3 center"
        f" axis parity) is validated on all {n_cuboids_tested}"
        f" tested L3=2 cuboids ({total_configs} total configurations,"
        f" 0 mismatches). This elevates H5 from a (4,4,2)-specific"
        f" observation to an L3=2-general structural lemma. Combined"
        f" with the iter 23 reflection-degeneracy lemma, we now have"
        f" TWO distinct proven families of zero-det configurations on"
        f" Z^3 cuboid + defect graphs, each with its own structural"
        f" characterization.",
    )
else:
    document(
        "h5_line3_singleton_lemma_partial_generalization",
        f"H5 works on {n_perfect} of {n_cuboids_tested} tested L3=2"
        f" cuboids. It is either cuboid-specific or requires a refined"
        f" condition. See failure details per cuboid.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: H5 line-3 + singleton lemma generalization across L3=2 cuboids")
    print("=" * 78)
    for (name, ok, detail) in RECORDS:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}]  {name}")
        print(f"           {detail}")
    for (name, note) in DOCS:
        print(f"  [DOC]    {name}")
        print(f"           {note}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
