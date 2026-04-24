#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- exhaustively sweep line-3 + singleton
configurations on (4,4,2) to characterize which force det_K3 = 0.

Context
-------
Iter 29 found that on (4,4,2), the defect {(1,0,0), (2,0,0),
(3,0,0), (0,3,1)} gives det_K3 = 0 exactly, without the defect
being central-reflection-paired. The z-plane-separation pattern
(line-3 at z=0, singleton at z=1) held for all 4 tested z=1
singletons on the y=0 line-3, but broke on the y=2 line-3 where
one z=1 singleton gave det != 0.

Goal
----
Exhaustively enumerate all (line-3, isolated-balanced-singleton)
configurations on (4,4,2) and characterize which give det=0 vs
det != 0. Test multiple candidate patterns:
  H1 z-separation: singleton in opposite z-plane from line-3.
  H2 corner singleton: singleton at cuboid corner (any axis max/min).
  H3 parity invariant: some additional arithmetic invariant forces 0.
  H4 z-column: singleton shares z-column with line-3 endpoint.

Method
------
For each line-3 position (x-oriented or y-oriented, no z-lines
since L3=2), for each isolated balanced singleton (correct parity
to balance + not adjacent to line), compute det_K3. Cross-tabulate
result by multiple structural features; identify pattern(s) that
cleanly separate det=0 from det != 0.

Structural features computed per (line-3, singleton):
- line_dir (x or y)
- line_z (0 or 1)
- single_z (0 or 1)
- z_sep (line_z != single_z)
- line_start_coords
- singleton_coords
- singleton_at_corner (x in {0, L1-1}, y in {0, L2-1}, z anywhere)
- singleton_at_edge (exactly 2 of x,y,z at boundary extremes)
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
    return B


def det_K3(bound, removed):
    B = build_B(bound, removed)
    if B is None:
        return None
    return int(round(abs(np.linalg.det(B))))


def is_corner(site, bound):
    return (site[0] in (0, bound[0] - 1)
            and site[1] in (0, bound[1] - 1)
            and site[2] in (0, bound[2] - 1))


def is_boundary(site, bound):
    """At least one coordinate at boundary."""
    return (site[0] in (0, bound[0] - 1)
            or site[1] in (0, bound[1] - 1)
            or site[2] in (0, bound[2] - 1))


def boundary_rank(site, bound):
    """How many of x,y,z are at a boundary (0 or L-1)."""
    count = 0
    for i in range(3):
        if site[i] == 0 or site[i] == bound[i] - 1:
            count += 1
    return count


# ---------------------------------------------------------------------------
# Enumerate line-3 configurations on (4,4,2).
# ---------------------------------------------------------------------------

bound = (4, 4, 2)
L1, L2, L3 = bound
base = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
base_set = set(base)

lines = []
# x-direction line-3: positions (i, j, k), (i+1, j, k), (i+2, j, k).
for i_start in range(L1 - 2):
    for j in range(L2):
        for k in range(L3):
            line = frozenset({(i_start, j, k), (i_start + 1, j, k), (i_start + 2, j, k)})
            lines.append((line, "x", (i_start, j, k)))
# y-direction line-3
for i in range(L1):
    for j_start in range(L2 - 2):
        for k in range(L3):
            line = frozenset({(i, j_start, k), (i, j_start + 1, k), (i, j_start + 2, k)})
            lines.append((line, "y", (i, j_start, k)))

# z-direction line-3: needs L3 >= 3. L3=2, so none.

record(
    "line3_count_on_442",
    len(lines) == 32,
    f"Line-3 positions on (4,4,2): x-lines {sum(1 for _, d, _ in lines if d == 'x')}, "
    f"y-lines {sum(1 for _, d, _ in lines if d == 'y')}. Total {len(lines)} "
    f"(expected 16 x + 16 y = 32).",
)


# ---------------------------------------------------------------------------
# For each line-3, enumerate isolated balanced singletons and test.
# ---------------------------------------------------------------------------

results = []
for (line, direction, start) in lines:
    line_parities = [sum(s) % 2 for s in line]
    line_evens = sum(1 for p in line_parities if p == 0)
    line_odds = sum(1 for p in line_parities if p == 1)
    # Need singleton of parity such that evens_removed == odds_removed.
    if line_evens > line_odds:
        need_parity = 1  # odd singleton to balance
    elif line_odds > line_evens:
        need_parity = 0
    else:
        continue  # should not happen for line-3 (always imbalance by 1)

    # Line neighbors
    line_neighbors = set()
    for s in line:
        for mu in (1, 2, 3):
            for d in (-1, 1):
                v = list(s); v[mu - 1] += d; v = tuple(v)
                if v in base_set:
                    line_neighbors.add(v)
    line_neighbors -= line

    # Enumerate singletons
    line_z = next(iter(line))[2]  # all line-3 sites share z since line is x/y-oriented

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
        results.append({
            "line": tuple(sorted(line)),
            "direction": direction,
            "line_start": start,
            "line_z": line_z,
            "singleton": s,
            "single_z": s[2],
            "z_sep": s[2] != line_z,
            "singleton_at_corner": is_corner(s, bound),
            "singleton_boundary_rank": boundary_rank(s, bound),
            "det": det,
            "is_zero": det == 0,
        })

n_total = len(results)
n_zero = sum(1 for r in results if r["is_zero"])
n_nonzero = n_total - n_zero

record(
    "exhaustive_sweep_size",
    n_total >= 200,
    f"Tested {n_total} (line-3, singleton) configurations. "
    f"det=0: {n_zero} ({n_zero / n_total * 100:.1f}%). "
    f"det!=0: {n_nonzero} ({n_nonzero / n_total * 100:.1f}%).",
)


# ---------------------------------------------------------------------------
# Hypothesis H1: z-separation forces det=0.
# ---------------------------------------------------------------------------

h1_zsep_and_zero = sum(1 for r in results if r["z_sep"] and r["is_zero"])
h1_zsep_total = sum(1 for r in results if r["z_sep"])
h1_same_and_zero = sum(1 for r in results if not r["z_sep"] and r["is_zero"])
h1_same_total = sum(1 for r in results if not r["z_sep"])

h1_perfect = (h1_zsep_and_zero == h1_zsep_total and h1_same_and_zero == 0
              and h1_zsep_total > 0 and h1_same_total > 0)

record(
    "H1_z_separation_perfect_predictor",
    h1_perfect,
    f"H1 (z-separation => det=0): z-sep-and-zero={h1_zsep_and_zero}/{h1_zsep_total}, "
    f"z-same-and-zero={h1_same_and_zero}/{h1_same_total}. Perfect? {h1_perfect}.",
)

# How strong? (probability of correctness as a classifier)
h1_correct = h1_zsep_and_zero + (h1_same_total - h1_same_and_zero)
record(
    "H1_z_separation_correct_fraction",
    h1_correct == n_total,
    f"H1 classifier (z-sep <=> det=0) matches {h1_correct}/{n_total} cases.",
)


# ---------------------------------------------------------------------------
# Hypothesis H2: corner singleton forces det=0.
# ---------------------------------------------------------------------------

h2_corner_and_zero = sum(1 for r in results if r["singleton_at_corner"] and r["is_zero"])
h2_corner_total = sum(1 for r in results if r["singleton_at_corner"])
h2_noncorner_and_zero = sum(1 for r in results if not r["singleton_at_corner"] and r["is_zero"])
h2_noncorner_total = sum(1 for r in results if not r["singleton_at_corner"])

h2_perfect = (h2_corner_and_zero == h2_corner_total and h2_noncorner_and_zero == 0
              and h2_corner_total > 0 and h2_noncorner_total > 0)

record(
    "H2_corner_singleton_perfect_predictor",
    h2_perfect,
    f"H2 (corner singleton => det=0): corner-and-zero={h2_corner_and_zero}/{h2_corner_total}, "
    f"noncorner-and-zero={h2_noncorner_and_zero}/{h2_noncorner_total}. Perfect? {h2_perfect}.",
)


# ---------------------------------------------------------------------------
# Hypothesis H3: joint condition (z-separated AND some additional feature).
# Test H3a: z-separated AND singleton at boundary_rank >= 2 (edge or corner).
# ---------------------------------------------------------------------------

h3a_zsep_edge_and_zero = sum(
    1 for r in results if r["z_sep"] and r["singleton_boundary_rank"] >= 2 and r["is_zero"]
)
h3a_zsep_edge_total = sum(
    1 for r in results if r["z_sep"] and r["singleton_boundary_rank"] >= 2
)

record(
    "H3a_zsep_edge_singleton_zero_count",
    h3a_zsep_edge_total > 0,
    f"H3a (z-separated AND singleton at edge/corner): "
    f"{h3a_zsep_edge_and_zero}/{h3a_zsep_edge_total} give det=0.",
)


# ---------------------------------------------------------------------------
# Hypothesis H4: z-column match -- singleton shares (x,y) column with a
# line-3 endpoint at opposite z.
# ---------------------------------------------------------------------------

def shares_column_with_line_endpoint(singleton, line):
    """Does singleton have the same (x,y) as any site in the line, but at different z?"""
    for s in line:
        if singleton[0] == s[0] and singleton[1] == s[1] and singleton[2] != s[2]:
            return True
    return False


def singleton_at_line_row(singleton, line):
    """Does singleton share y,z with a line endpoint extended (x beyond line)?
    For x-line, test if singleton has same y,z as line but x outside the line's x-range."""
    line_list = sorted(line)
    direction = None
    # Determine direction
    if line_list[0][1] == line_list[1][1] and line_list[0][2] == line_list[1][2]:
        direction = "x"
    elif line_list[0][0] == line_list[1][0] and line_list[0][2] == line_list[1][2]:
        direction = "y"
    else:
        return False
    if direction == "x":
        ys = {s[1] for s in line}
        zs = {s[2] for s in line}
        return singleton[1] in ys and singleton[2] in zs and singleton[0] not in {s[0] for s in line}
    if direction == "y":
        xs = {s[0] for s in line}
        zs = {s[2] for s in line}
        return singleton[0] in xs and singleton[2] in zs and singleton[1] not in {s[1] for s in line}
    return False


for r in results:
    r["shares_z_column"] = shares_column_with_line_endpoint(r["singleton"], set(r["line"]))
    r["on_line_row_outside_line"] = singleton_at_line_row(r["singleton"], set(r["line"]))


h4_zsep_and_shares_col = [r for r in results if r["z_sep"] and r["shares_z_column"]]
h4_zsep_not_shares = [r for r in results if r["z_sep"] and not r["shares_z_column"]]

h4_shares_zero = sum(1 for r in h4_zsep_and_shares_col if r["is_zero"])
h4_shares_total = len(h4_zsep_and_shares_col)
h4_not_shares_zero = sum(1 for r in h4_zsep_not_shares if r["is_zero"])
h4_not_shares_total = len(h4_zsep_not_shares)

record(
    "H4_zsep_and_shares_zcolumn",
    h4_shares_total > 0,
    f"H4 (z-sep AND shares z-column with line endpoint): "
    f"{h4_shares_zero}/{h4_shares_total} give det=0.",
)
record(
    "H4_zsep_but_not_shares_zcolumn",
    h4_not_shares_total > 0,
    f"H4 (z-sep but NO shared z-column): "
    f"{h4_not_shares_zero}/{h4_not_shares_total} give det=0.",
)


# ---------------------------------------------------------------------------
# Aggregate by line direction and z to see patterns.
# ---------------------------------------------------------------------------

breakdown_by_line_kind = defaultdict(lambda: {"total": 0, "zero": 0,
                                               "zsep_total": 0, "zsep_zero": 0,
                                               "same_total": 0, "same_zero": 0})

for r in results:
    key = (r["direction"], r["line_z"], r["line_start"][0:2])  # direction + z + start (dropped k)
    # Use a simpler key: just (direction, line_z).
    simple_key = (r["direction"], r["line_z"])
    bd = breakdown_by_line_kind[simple_key]
    bd["total"] += 1
    if r["is_zero"]:
        bd["zero"] += 1
    if r["z_sep"]:
        bd["zsep_total"] += 1
        if r["is_zero"]:
            bd["zsep_zero"] += 1
    else:
        bd["same_total"] += 1
        if r["is_zero"]:
            bd["same_zero"] += 1

for simple_key, bd in sorted(breakdown_by_line_kind.items()):
    direction, line_z = simple_key
    record(
        f"breakdown_{direction}_line_z{line_z}",
        bd["total"] > 0,
        f"{direction}-line at z={line_z}: {bd['zero']}/{bd['total']} det=0. "
        f"z-sep: {bd['zsep_zero']}/{bd['zsep_total']} zero. "
        f"z-same: {bd['same_zero']}/{bd['same_total']} zero.",
    )


# ---------------------------------------------------------------------------
# Investigate z-sep failures (z-separated but det != 0)
# ---------------------------------------------------------------------------

zsep_failures = [r for r in results if r["z_sep"] and not r["is_zero"]]

record(
    "zsep_failures_count",
    len(zsep_failures) >= 0,
    f"z-separated but det!=0 (exceptions to H1): {len(zsep_failures)} cases. "
    f"Examples: {[(r['line_start'], r['direction'], r['singleton'], r['det']) for r in zsep_failures[:10]]}.",
)

# Cluster these by features
zsep_fail_lines = defaultdict(list)
for r in zsep_failures:
    zsep_fail_lines[(r["direction"], r["line_start"], r["line_z"])].append(
        (r["singleton"], r["det"])
    )

record(
    "zsep_failures_line_distribution",
    len(zsep_fail_lines) >= 0,
    f"z-separation failures span {len(zsep_fail_lines)} distinct line-3 "
    f"positions.",
)


# ---------------------------------------------------------------------------
# Investigate z-same successes (not z-separated but det == 0, violating H1)
# ---------------------------------------------------------------------------

zsame_successes = [r for r in results if not r["z_sep"] and r["is_zero"]]

record(
    "zsame_successes_count",
    len(zsame_successes) >= 0,
    f"z-same (not separated) but det=0 (also H1 violations): "
    f"{len(zsame_successes)} cases. Examples: "
    f"{[(r['line_start'], r['direction'], r['singleton'], r['det']) for r in zsame_successes[:10]]}.",
)


# ---------------------------------------------------------------------------
# Hypothesis H5: z-separated AND singleton parallel-axis coord has SAME
# parity as line center's parallel-axis coord.
#   For x-line: compare singleton_x vs (start_x + 1).
#   For y-line: compare singleton_y vs (start_y + 1).
# ---------------------------------------------------------------------------

def h5_predict_zero(r):
    if not r["z_sep"]:
        return False
    direction = r["direction"]
    line_start = r["line_start"]
    if direction == "x":
        center_x = line_start[0] + 1
        return (r["singleton"][0] - center_x) % 2 == 0
    if direction == "y":
        center_y = line_start[1] + 1
        return (r["singleton"][1] - center_y) % 2 == 0
    return False


h5_tp = sum(1 for r in results if h5_predict_zero(r) and r["is_zero"])
h5_fp = sum(1 for r in results if h5_predict_zero(r) and not r["is_zero"])
h5_fn = sum(1 for r in results if not h5_predict_zero(r) and r["is_zero"])
h5_tn = sum(1 for r in results if not h5_predict_zero(r) and not r["is_zero"])
h5_perfect = (h5_fp == 0 and h5_fn == 0)

record(
    "H5_zsep_and_axis_parity_perfect_predictor",
    h5_perfect,
    f"H5 (z-sep AND singleton_parallel_axis same parity as line_center): "
    f"TP={h5_tp} (pred zero, is zero), "
    f"FP={h5_fp} (pred zero, not zero), "
    f"FN={h5_fn} (pred not zero, is zero), "
    f"TN={h5_tn} (pred not zero, not zero). "
    f"Perfect? {h5_perfect}.",
)

record(
    "H5_accuracy_over_all_cases",
    (h5_tp + h5_tn) == n_total,
    f"H5 classifier matches {h5_tp + h5_tn}/{n_total} cases. "
    f"Errors: {h5_fp + h5_fn}.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

n_zsep_nonzero = len(zsep_failures)
n_zsame_zero = len(zsame_successes)
h1_accuracy = (n_total - n_zsep_nonzero - n_zsame_zero) / n_total if n_total > 0 else 0

if h5_perfect:
    document(
        "line3_singleton_zero_det_lemma_candidate",
        f"On (4,4,2), det_K3(B) = 0 on line-3 + balanced isolated"
        f" singleton defect configurations is EXACTLY characterized"
        f" by: (a) singleton in opposite z-plane from line-3 AND"
        f" (b) singleton's parallel-axis coordinate (x for x-line,"
        f" y for y-line) has the SAME parity as the line-3 center's"
        f" parallel-axis coordinate. All {n_total} tested"
        f" configurations classified correctly (TP={h5_tp},"
        f" TN={h5_tn}, 0 false positives, 0 false negatives)."
        f" This is a candidate new structural lemma, distinct from"
        f" iter 23 reflection-degeneracy (which required defect"
        f" to be sigma-paired). The line-3 singleton mechanism"
        f" works on NON-sigma-paired defects.",
    )
elif h1_perfect:
    document(
        "z_separation_lemma_validated",
        f"On (4,4,2), line-3 + singleton z-separation <=> det_K3 = 0"
        f" on {h1_zsep_total + h1_same_total} configurations. Simple"
        f" z-separation is sufficient.",
    )
elif h1_accuracy > 0.9:
    document(
        "z_separation_strong_but_imperfect",
        f"H1 (z-sep <=> det=0) is {h1_accuracy*100:.1f}% accurate."
        f" H5 refines this with axis-parity: tested here with"
        f" TP={h5_tp}, FP={h5_fp}, FN={h5_fn}, TN={h5_tn}. Refined"
        f" hypothesis is {(h5_tp + h5_tn)/n_total*100:.1f}% accurate.",
    )
else:
    document(
        "characterization_still_open",
        f"Neither H1 (z-sep) nor H5 (z-sep + axis parity) fully"
        f" characterize det=0. Need further analysis.",
    )


# ---------------------------------------------------------------------------
# Additional: look at all det=0 cases by z-sep status to find structure
# ---------------------------------------------------------------------------

# For each det=0 case, is it z-separated?
z_sep_fraction_among_zeros = (sum(1 for r in results if r["is_zero"] and r["z_sep"])
                              / max(n_zero, 1))
record(
    "z_sep_fraction_among_det_zero_cases",
    z_sep_fraction_among_zeros > 0.5,
    f"Among {n_zero} det=0 cases, "
    f"{z_sep_fraction_among_zeros*100:.1f}% are z-separated.",
)


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: line-3 + singleton exhaustive sweep on (4,4,2)")
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
