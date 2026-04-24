#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- test the UNION of iter 32's
bipartition-preserving partial-reflection lemma and iter 23's
bipartition-flipping central-reflection lemma as a single
classifier for det_K3 = 0 on line-3 + singleton defects.

Context
-------
Iter 32 showed the bipartition-preserving partial-reflection
lemma is sufficient but not necessary (71.2% accuracy across
1720 line-3 + singleton configs on 5 L3=2 cuboids; zero false
positives, 496 false negatives).

On (4,4,2), iter 32 gave 0 TP of 128 det=0 cases -- all come
from iter 23's central sigma (bipartition-flipping), not
covered by iter 32's framework.

This iteration tests whether the UNION of iter 32 + iter 23
tests covers all 1720 cases.

Tests applied per configuration
-------------------------------
Test A (iter 32): exists bipartition-preserving phi = rho_S
(S subset {1,2,3}) such that:
  (i) rho_S(defect) = defect,
  (ii) rho_S preserves bipartition (delta_S even),
  (iii) all epsilon_mu = +1 under rho_S,
  (iv) sign(sigma_e) * sign(sigma_o) = -1.

Test B (iter 23): central rho_{123} is an automorphism of the
truncated graph AND:
  (i) L1 + L2 + L3 is even (so rho_{123} flips bipartition),
  (ii) L1 is even (so epsilon_2 = -1),
  (iii) n_bi is odd.

Predict det = 0 iff Test A OR Test B passes. Otherwise predict
det != 0. Compare with actual det values.

If accuracy is 1720/1720: the union gives a complete
characterization. If false negatives remain: additional
mechanisms (e.g., non-central bipartition-flipping reflections,
or SH3-type non-automorphism bijections) are needed.
"""

from __future__ import annotations

import sys

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
    return B, evens, odds, idx_e, idx_o, n_bi


def det_K3(bound, removed):
    r = build_B(bound, removed)
    if r is None:
        return None
    B = r[0]
    return int(round(np.linalg.det(B.astype(np.float64))))


def rho_S(n, bound, S):
    L = bound
    return tuple((L[l] - 1 - n[l]) if (l + 1) in S else n[l] for l in range(3))


def bipartition_preserves(bound, S):
    L1, L2, L3 = bound
    a1 = 1 if 1 in S else 0
    a2 = 1 if 2 in S else 0
    a3 = 1 if 3 in S else 0
    delta = a1 * L1 + a2 * L2 + a3 * L3 + len(S)
    return delta % 2 == 0


def epsilon_mu_func(bound, S, mu):
    L1, L2, L3 = bound
    a1 = 1 if 1 in S else 0
    a2 = 1 if 2 in S else 0
    if mu == 1:
        return 1
    if mu == 2:
        return (-1) ** (a1 * (L1 - 1))
    if mu == 3:
        return (-1) ** (a1 * (L1 - 1) + a2 * (L2 - 1))
    raise ValueError


def perm_sign(perm):
    n = len(perm)
    visited = [False] * n
    sign = 1
    for i in range(n):
        if visited[i]:
            continue
        cycle_len = 0
        j = i
        while not visited[j]:
            visited[j] = True
            j = perm[j]
            cycle_len += 1
        if cycle_len > 1 and cycle_len % 2 == 0:
            sign = -sign
    return sign


def test_A_partial_reflection(bound, removed, S, evens, odds, idx_e, idx_o):
    """Iter 32 test: bipartition-preserving partial reflection forces det=0."""
    image = {rho_S(r, bound, S) for r in removed}
    if image != set(removed):
        return False
    if not bipartition_preserves(bound, S):
        return False
    if not all(epsilon_mu_func(bound, S, mu) == 1 for mu in (1, 2, 3)):
        return False
    sigma_e = [idx_e[rho_S(e, bound, S)] for e in evens]
    sigma_o = [idx_o[rho_S(o, bound, S)] for o in odds]
    return perm_sign(sigma_e) * perm_sign(sigma_o) == -1


def test_B_central_sigma(bound, removed, n_bi):
    """Iter 23 test: central sigma with iter 23 conditions."""
    S = frozenset({1, 2, 3})
    image = {rho_S(r, bound, S) for r in removed}
    if image != set(removed):
        return False
    L1, L2, L3 = bound
    # Condition (i) L1+L2+L3 even (sigma flips bipartition)
    if (L1 + L2 + L3) % 2 != 0:
        return False
    # Condition (ii) L1 even (epsilon_2 = -1)
    if L1 % 2 != 0:
        return False
    # Condition (iii) n_bi odd
    if n_bi % 2 != 1:
        return False
    return True


def enumerate_configs(bound):
    L1, L2, L3 = bound
    base = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
    base_set = set(base)
    lines = []
    if L1 >= 3:
        for i_start in range(L1 - 2):
            for j in range(L2):
                for k in range(L3):
                    line = frozenset({(i_start, j, k),
                                     (i_start + 1, j, k),
                                     (i_start + 2, j, k)})
                    lines.append((line, "x", (i_start, j, k)))
    if L2 >= 3:
        for i in range(L1):
            for j_start in range(L2 - 2):
                for k in range(L3):
                    line = frozenset({(i, j_start, k),
                                     (i, j_start + 1, k),
                                     (i, j_start + 2, k)})
                    lines.append((line, "y", (i, j_start, k)))
    configs = []
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
            if s in line or s in line_neighbors:
                continue
            if sum(s) % 2 != need_parity:
                continue
            configs.append({
                "bound": bound,
                "line": tuple(sorted(line)),
                "direction": direction,
                "line_start": start,
                "singleton": s,
                "removed": line | {s},
            })
    return configs


# ---------------------------------------------------------------------------
# Run on all 5 L3=2 cuboids
# ---------------------------------------------------------------------------

bounds_to_test = [(3, 3, 2), (4, 3, 2), (4, 4, 2), (5, 3, 2), (5, 5, 2)]

all_results = {}
for bound in bounds_to_test:
    configs = enumerate_configs(bound)
    results = []
    for cfg in configs:
        r = build_B(bound, cfg["removed"])
        if r is None:
            continue
        B, evens, odds, idx_e, idx_o, n_bi = r
        det = int(round(np.linalg.det(B.astype(np.float64))))
        # Apply Test A across all 7 partial reflections
        test_A_passes = False
        for S in [frozenset({1}), frozenset({2}), frozenset({3}),
                  frozenset({1, 2}), frozenset({1, 3}), frozenset({2, 3}),
                  frozenset({1, 2, 3})]:
            if test_A_partial_reflection(bound, cfg["removed"], S,
                                          evens, odds, idx_e, idx_o):
                test_A_passes = True
                break
        test_B_passes = test_B_central_sigma(bound, cfg["removed"], n_bi)
        predicted_zero = test_A_passes or test_B_passes
        results.append({
            **cfg,
            "det": det,
            "is_zero": det == 0,
            "test_A": test_A_passes,
            "test_B": test_B_passes,
            "predicted_zero": predicted_zero,
        })
    all_results[bound] = results


# ---------------------------------------------------------------------------
# Per-cuboid accuracy
# ---------------------------------------------------------------------------

cuboid_stats = {}
for bound, results in all_results.items():
    tp = sum(1 for r in results if r["predicted_zero"] and r["is_zero"])
    fp = sum(1 for r in results if r["predicted_zero"] and not r["is_zero"])
    fn = sum(1 for r in results if not r["predicted_zero"] and r["is_zero"])
    tn = sum(1 for r in results if not r["predicted_zero"] and not r["is_zero"])
    total = tp + fp + fn + tn
    cuboid_stats[bound] = {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "total": total}
    tag = f"{bound[0]}x{bound[1]}x{bound[2]}"
    record(
        f"union_perfect_on_{tag}",
        fp == 0 and fn == 0 and total > 0,
        f"{tag}: TP={tp}, FP={fp}, FN={fn}, TN={tn}, total={total}. "
        f"Perfect? {fp == 0 and fn == 0 and total > 0}.",
    )


# ---------------------------------------------------------------------------
# Decomposition: Test A vs Test B coverage per cuboid
# ---------------------------------------------------------------------------

for bound, results in all_results.items():
    a_only = sum(1 for r in results if r["test_A"] and not r["test_B"])
    b_only = sum(1 for r in results if not r["test_A"] and r["test_B"])
    both = sum(1 for r in results if r["test_A"] and r["test_B"])
    neither = sum(1 for r in results if not r["test_A"] and not r["test_B"])
    tag = f"{bound[0]}x{bound[1]}x{bound[2]}"
    record(
        f"decomposition_on_{tag}",
        (a_only + b_only + both + neither) == cuboid_stats[bound]["total"],
        f"{tag}: A-only={a_only}, B-only={b_only}, both={both}, neither={neither}.",
    )


# ---------------------------------------------------------------------------
# Cross-cuboid summary
# ---------------------------------------------------------------------------

total_all = sum(s["total"] for s in cuboid_stats.values())
total_tp = sum(s["tp"] for s in cuboid_stats.values())
total_tn = sum(s["tn"] for s in cuboid_stats.values())
total_fp = sum(s["fp"] for s in cuboid_stats.values())
total_fn = sum(s["fn"] for s in cuboid_stats.values())

n_perfect = sum(1 for s in cuboid_stats.values()
                if s["fp"] == 0 and s["fn"] == 0 and s["total"] > 0)

record(
    "union_total_accuracy",
    total_all > 0 and (total_tp + total_tn) == total_all,
    f"Union test (iter 32 A OR iter 23 B): total accuracy "
    f"{total_tp + total_tn}/{total_all}. TP={total_tp}, FP={total_fp}, "
    f"FN={total_fn}, TN={total_tn}.",
)

record(
    "union_perfect_on_all_cuboids",
    n_perfect == len(bounds_to_test),
    f"Perfect on {n_perfect}/{len(bounds_to_test)} cuboids.",
)


# ---------------------------------------------------------------------------
# Report false-negative details (configs det=0 not caught by either test)
# ---------------------------------------------------------------------------

all_fn = []
for bound, results in all_results.items():
    for r in results:
        if not r["predicted_zero"] and r["is_zero"]:
            all_fn.append((bound, r))

record(
    "remaining_false_negatives_count",
    len(all_fn) == 0,
    f"Remaining false negatives (det=0 not covered by A or B): "
    f"{len(all_fn)}. Examples: "
    f"{[(b, r['line_start'], r['direction'], r['singleton']) for (b, r) in all_fn[:5]]}",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if n_perfect == len(bounds_to_test) and total_fp == 0 and total_fn == 0:
    document(
        "union_lemma_covers_all_zero_det_cases",
        f"The union of iter 32 (bipartition-preserving partial"
        f" reflection lemma) and iter 23 (central sigma lemma)"
        f" perfectly characterizes det_K3 = 0 on line-3 + singleton"
        f" defect configurations across all 5 tested L3=2 cuboids"
        f" (1720 / 1720 correct). The unified structural claim:"
        f" det=0 iff (exists a bipartition-preserving partial"
        f" reflection rho_S fixing defect with all epsilon_mu = +1"
        f" and sign product -1) OR (central rho_{{123}} fixes defect"
        f" with L1+L2+L3 even, L1 even, n_bi odd). This is a"
        f" COMPLETE characterization via two distinct symmetry"
        f" mechanisms.",
    )
elif total_fp == 0 and total_fn > 0:
    document(
        "union_lemma_sufficient_not_complete",
        f"Union of iter 32 + iter 23 covers {total_all - total_fn} of"
        f" {total_all} det=0 cases correctly. FN={total_fn}, FP=0."
        f" Additional zero-det mechanisms remain: likely include"
        f" non-central bipartition-flipping reflections (rho_{{12}},"
        f" rho_{{13}}, rho_{{23}}) and possibly SH3-type"
        f" non-automorphism configurations.",
    )
else:
    document(
        "union_lemma_has_false_positives",
        f"Union test has false positives ({total_fp}), indicating"
        f" a bug in the test logic. Investigate.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: UNION of iter 32 + iter 23 reflection lemmas test")
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
