#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- test the GENERALIZED reflection lemma
as a necessary-and-sufficient condition for det_K3 = 0 on line-3
+ singleton defect configurations.

Context
-------
Iter 23 proved that central reflection sigma with L1+L2+L3 even,
L1 even, n_bi odd forces det_K3 = 0.
Iter 30's H5 empirically characterized det=0 on (4,4,2) perfectly
(288/288) but failed to generalize (iter 31: 80-97% on other
L3=2 cuboids with zero false positives, up to 32 false negatives).
Iter 31's investigation of false negatives revealed the real
mechanism: partial reflections rho_S (S subset of {1,2,3}) can
force det=0 when they fix the defect AND have a net transformation
factor = -1.

Lemma candidate (generalized)
-----------------------------
Let phi = rho_S be a partial reflection of the cuboid (L1, L2, L3).
If:
  (i) phi(defect) = defect (phi is a graph automorphism of G).
  (ii) phi preserves bipartition (delta_S = sum_{l in S} L_l + |S|
       is even).
  (iii) All epsilon_mu under phi equal +1 (i.e., a_1 (L_1 - 1) even
        AND a_1 (L_1 - 1) + a_2 (L_2 - 1) even).
  (iv) sign(sigma_e) * sign(sigma_o) = -1, where sigma_e, sigma_o
       are the induced permutations on G's remaining evens, odds.
Then det_K3(B) = 0.

Test
----
For each (line-3, singleton) configuration from iter 31's sweep
(on (3,3,2), (4,3,2), (4,4,2), (5,3,2), (5,5,2)), compute
whether any non-identity phi in {rho_1, rho_2, rho_3, rho_{12},
rho_{13}, rho_{23}, rho_{123}} satisfies (i)-(iv). Predict det=0
iff at least one such phi exists. Compare with actual det=0.

Iter 23 (central sigma) cases are bipartition-flipping and not
covered by this bipartition-preserving formulation. They should
continue to apply via iter 23's mechanism. Here we check only
the bipartition-preserving partial reflection family, expecting
it to explain ALL iter 31 false negatives.
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


def epsilon_mu(bound, S, mu):
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


def all_epsilons_plus(bound, S):
    return all(epsilon_mu(bound, S, mu) == 1 for mu in (1, 2, 3))


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


def phi_forces_det_zero(bound, removed, S, evens, odds, idx_e, idx_o):
    """Check if phi = rho_S is a bipartition-preserving graph automorphism
    of the truncated graph such that the partial reflection forces det=0."""
    # (i) phi(defect) == defect
    image = {rho_S(r, bound, S) for r in removed}
    if image != set(removed):
        return False, "not-automorphism"
    # (ii) bipartition preserved
    if not bipartition_preserves(bound, S):
        return False, "flips-bipartition"
    # (iii) all epsilons = +1
    if not all_epsilons_plus(bound, S):
        return False, "nontrivial-epsilons"
    # (iv) sign(sigma_e) * sign(sigma_o) = -1
    sigma_e = [idx_e[rho_S(e, bound, S)] for e in evens]
    sigma_o = [idx_o[rho_S(o, bound, S)] for o in odds]
    sign_e = perm_sign(sigma_e)
    sign_o = perm_sign(sigma_o)
    if sign_e * sign_o != -1:
        return False, "sign-product-positive"
    return True, "forces-zero"


def line_center_coord(start, direction):
    if direction == "x":
        return start[0] + 1
    if direction == "y":
        return start[1] + 1
    raise ValueError


# ---------------------------------------------------------------------------
# Enumerate configurations on multiple cuboids.
# ---------------------------------------------------------------------------

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
            removed = line | {s}
            configs.append({
                "bound": bound,
                "line": tuple(sorted(line)),
                "direction": direction,
                "line_start": start,
                "line_z": next(iter(line))[2],
                "singleton": s,
                "removed": removed,
            })
    return configs


bounds_to_test = [(3, 3, 2), (4, 3, 2), (4, 4, 2), (5, 3, 2), (5, 5, 2)]

all_configs_and_det = {}
for bound in bounds_to_test:
    configs = enumerate_configs(bound)
    results = []
    for cfg in configs:
        det = det_K3(bound, cfg["removed"])
        if det is None:
            continue
        r = build_B(bound, cfg["removed"])
        B, evens, odds, idx_e, idx_o, n_bi = r
        # Find any forcing phi
        forcing_phis = []
        for S in [frozenset({1}), frozenset({2}), frozenset({3}),
                  frozenset({1, 2}), frozenset({1, 3}), frozenset({2, 3}),
                  frozenset({1, 2, 3})]:
            forces, reason = phi_forces_det_zero(bound, cfg["removed"], S,
                                                 evens, odds, idx_e, idx_o)
            if forces:
                forcing_phis.append(S)
        results.append({
            **cfg,
            "det": det,
            "is_zero": det == 0,
            "forcing_phis": forcing_phis,
            "predicted_zero": len(forcing_phis) > 0,
        })
    all_configs_and_det[bound] = results


# ---------------------------------------------------------------------------
# Per-cuboid accuracy
# ---------------------------------------------------------------------------

cuboid_stats = {}
for bound, results in all_configs_and_det.items():
    tp = sum(1 for r in results if r["predicted_zero"] and r["is_zero"])
    fp = sum(1 for r in results if r["predicted_zero"] and not r["is_zero"])
    fn = sum(1 for r in results if not r["predicted_zero"] and r["is_zero"])
    tn = sum(1 for r in results if not r["predicted_zero"] and not r["is_zero"])
    total = tp + fp + fn + tn
    cuboid_stats[bound] = {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "total": total}
    tag = f"{bound[0]}x{bound[1]}x{bound[2]}"
    record(
        f"generalized_lemma_perfect_on_{tag}",
        fp == 0 and fn == 0 and total > 0,
        f"{tag}: TP={tp}, FP={fp}, FN={fn}, TN={tn}, total={total}. "
        f"Perfect? {fp == 0 and fn == 0 and total > 0}.",
    )


# ---------------------------------------------------------------------------
# Cross-cuboid summary
# ---------------------------------------------------------------------------

total_all = sum(s["total"] for s in cuboid_stats.values())
total_tp = sum(s["tp"] for s in cuboid_stats.values())
total_tn = sum(s["tn"] for s in cuboid_stats.values())
total_fp = sum(s["fp"] for s in cuboid_stats.values())
total_fn = sum(s["fn"] for s in cuboid_stats.values())

n_perfect_cuboids = sum(1 for s in cuboid_stats.values()
                        if s["fp"] == 0 and s["fn"] == 0 and s["total"] > 0)

record(
    "generalized_lemma_total_accuracy",
    total_all > 0 and (total_tp + total_tn) == total_all,
    f"Generalized partial-reflection lemma accuracy across all 5 L3=2 cuboids: "
    f"TP={total_tp}, FP={total_fp}, FN={total_fn}, TN={total_tn}, "
    f"correct={total_tp + total_tn}/{total_all}.",
)

record(
    "generalized_lemma_perfect_all_cuboids",
    n_perfect_cuboids == len(bounds_to_test),
    f"Perfect on {n_perfect_cuboids}/{len(bounds_to_test)} cuboids.",
)


# ---------------------------------------------------------------------------
# Detail on remaining misclassifications (if any)
# ---------------------------------------------------------------------------

for bound, results in all_configs_and_det.items():
    errors = [r for r in results
              if r["predicted_zero"] != r["is_zero"]]
    if errors:
        tag = f"{bound[0]}x{bound[1]}x{bound[2]}"
        error_types = {}
        for r in errors:
            key = "FN" if r["is_zero"] else "FP"
            error_types.setdefault(key, []).append(
                (r["line_start"], r["direction"], r["singleton"], r["det"])
            )
        record(
            f"errors_on_{tag}_detail",
            len(errors) == 0,
            f"{tag}: {len(errors)} mismatches. Types: "
            f"{ {k: len(v) for k, v in error_types.items()} }. "
            f"Examples: {dict(error_types)}",
        )


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if n_perfect_cuboids == len(bounds_to_test):
    document(
        "generalized_reflection_lemma_validated",
        f"On all 5 tested L3=2 cuboids ({total_all} configurations"
        f" total), det_K3 = 0 on line-3 + singleton defects IFF"
        f" there exists a partial reflection rho_S (S subset of"
        f" {{1,2,3}}) such that (i) rho_S(defect) = defect, (ii)"
        f" rho_S preserves bipartition, (iii) all epsilon_mu = +1"
        f" under rho_S, and (iv) sign(sigma_e) * sign(sigma_o) ="
        f" -1 on the remaining even/odd sites. This generalized"
        f" partial-reflection lemma CORRECTS iter 24's conclusion"
        f" that partial reflections don't force det=0: they DO,"
        f" when combined with appropriate permutation-sign"
        f" conditions on the defect. The lemma is a candidate"
        f" structural theorem for line-3 + singleton defects."
        f" Iter 23 (central sigma) remains a separate lemma for"
        f" bipartition-flipping cases.",
    )
elif total_fp == 0 and total_fn > 0:
    document(
        "generalized_reflection_lemma_sufficient_not_necessary",
        f"Partial-reflection lemma is SUFFICIENT (0 false positives)"
        f" but not NECESSARY ({total_fn} false negatives across"
        f" cuboids). Some det=0 configurations are not explained by"
        f" any partial reflection -- these may be SH3-type"
        f" configurations with no graph automorphism fixing the"
        f" defect, requiring a different mechanism.",
    )
else:
    document(
        "generalized_reflection_lemma_partial",
        f"Partial-reflection lemma accuracy: {(total_tp + total_tn)/total_all*100:.1f}%."
        f" FP={total_fp}, FN={total_fn}. Lemma is not a complete"
        f" characterization; further refinement needed.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: generalized partial-reflection lemma test on L3=2 cuboids")
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
