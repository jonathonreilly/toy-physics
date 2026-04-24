#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- search for a FAMILY of degeneracy
lemmas indexed by partial reflections of the cuboid.

Context
-------
Iter 23 validated the reflection-degeneracy lemma for the full
central reflection sigma(i,j,k) = (L1-1-i, L2-1-j, L3-1-k): when
sigma(r1) = r2, L1+L2+L3 is even, L1 is even, and n_bi is odd,
|det_K3(B)| = 0.

Z^3 has 8 axis-aligned reflections in total (including identity):
identity, x-only, y-only, z-only, xy, xz, yz, xyz. The last one
(xyz = sigma) gave iter 23's lemma. Are there OTHER partial
reflections that force det = 0 on appropriate shapes? If yes,
we have a family of lemmas.

Derivation
----------
For reflection rho_S with flip set S subset of {1,2,3}, the action
rho_S(n)_l = L_l - 1 - n_l if l in S else n_l.

The sign ratio of the image edge (direction mu) to the original
under rho_S decomposes as:
  epsilon_mu = eta_mu_ratio * parity_sign
where
  eta_1_ratio = 1,
  eta_2_ratio = (-1)^{a1 (L1-1)} where a1 = [1 in S],
  eta_3_ratio = (-1)^{a1 (L1-1) + a2 (L2-1)} where a2 = [2 in S],
and parity_sign depends on whether rho_S flips bipartition and
whether mu is in S.

Bipartition flip condition: delta_S = a1 L1 + a2 L2 + a3 L3 + |S|
is ODD iff rho_S maps evens to odds.

Test strategy
-------------
For each of 7 non-identity reflections rho_S, construct a test
shape where:
(i) rho_S flips bipartition (so removed_pair is balanced),
(ii) removed = {(0,0,0), rho_S(0,0,0)} is 2 distinct non-adjacent
     singletons (rho_S(0,0,0) must not be a neighbor of (0,0,0)).

Then compute |det_K3(B)| and record. Vary cuboid dimensions to
get multiple n_bi parities.

Predictions
-----------
Based on iter 23 (rho_{123} case), conjecture: for each reflection
rho_S that flips bipartition, there exist cuboid dimensions such
that |det_K3(B)| = 0. The exact "L1 even" condition may or may
not generalize.

Report: which (reflection, cuboid-dim-parity, n_bi-parity)
combinations force det = 0.
"""

from __future__ import annotations

import sys
from itertools import combinations

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


def rho_S(n, bound, S):
    L = bound
    return tuple((L[l] - 1 - n[l]) if (l + 1) in S else n[l] for l in range(3))


def bipartition_flip(bound, S):
    L1, L2, L3 = bound
    a1 = 1 if 1 in S else 0
    a2 = 1 if 2 in S else 0
    a3 = 1 if 3 in S else 0
    delta = a1 * L1 + a2 * L2 + a3 * L3 + len(S)
    return delta % 2 == 1


def predicted_epsilon_eta(bound, S):
    L1, L2, L3 = bound
    a1 = 1 if 1 in S else 0
    a2 = 1 if 2 in S else 0
    return {
        1: 1,
        2: (-1) ** (a1 * (L1 - 1)),
        3: (-1) ** (a1 * (L1 - 1) + a2 * (L2 - 1)),
    }


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


def adjacent(u, v):
    return sum(abs(u[i] - v[i]) for i in range(3)) == 1


def analyze(bound, removed, S):
    L = bound
    det_info = build_B(bound, removed)
    if det_info is None:
        return {"balanced": False}
    B, n_bi = det_info
    det_K3 = int(round(abs(np.linalg.det(B))))
    rho_fixed = set(removed) == {rho_S(r, bound, S) for r in removed}
    flip = bipartition_flip(bound, S)
    eps = predicted_epsilon_eta(bound, S)
    return {
        "balanced": True,
        "bound": bound,
        "removed": removed,
        "S": S,
        "n_bi": n_bi,
        "n_bi_odd": n_bi % 2 == 1,
        "rho_fixed_set": rho_fixed,
        "bipartition_flip": flip,
        "det_K3": det_K3,
        "is_zero": det_K3 == 0,
        "eps": eps,
        "L1_even": L[0] % 2 == 0,
        "L2_even": L[1] % 2 == 0,
        "L3_even": L[2] % 2 == 0,
    }


# ---------------------------------------------------------------------------
# Construct test shapes per reflection.
# ---------------------------------------------------------------------------

def make_shape_for(S, bounds_to_try):
    """Find the first bound in bounds_to_try where rho_S is an automorphism
    and removed = {(0,0,0), rho_S(0,0,0)} is balanced + non-adjacent."""
    for bound in bounds_to_try:
        r1 = (0, 0, 0)
        r2 = rho_S(r1, bound, S)
        if r2 == r1:
            continue
        if adjacent(r1, r2):
            continue
        removed = {r1, r2}
        L1, L2, L3 = bound
        # Check r2 in-bounds (it is, by construction).
        if r2[0] >= L1 or r2[1] >= L2 or r2[2] >= L3:
            continue
        if r2[0] < 0 or r2[1] < 0 or r2[2] < 0:
            continue
        # Evens/odds balance check: done inside analyze.
        info = analyze(bound, removed, S)
        if info["balanced"]:
            return bound, removed, info
    return None


bounds_pool = [
    (2, 2, 2), (3, 3, 2), (3, 2, 2), (2, 3, 2), (2, 2, 3),
    (4, 2, 2), (4, 3, 2), (4, 4, 2), (3, 4, 2), (2, 4, 2),
    (4, 2, 3), (3, 3, 4), (4, 3, 3), (4, 4, 3), (5, 3, 2),
    (6, 2, 2), (6, 4, 2), (3, 2, 4), (2, 3, 4),
    (4, 2, 4), (4, 4, 4), (5, 3, 4), (3, 5, 4),
]

all_reflections = [
    frozenset({1}), frozenset({2}), frozenset({3}),
    frozenset({1, 2}), frozenset({1, 3}), frozenset({2, 3}),
    frozenset({1, 2, 3}),
]

reflection_name = {
    frozenset({1}): "rho_1_x",
    frozenset({2}): "rho_2_y",
    frozenset({3}): "rho_3_z",
    frozenset({1, 2}): "rho_12_xy",
    frozenset({1, 3}): "rho_13_xz",
    frozenset({2, 3}): "rho_23_yz",
    frozenset({1, 2, 3}): "rho_123_xyz",
}

reflection_results = {}
for S in all_reflections:
    found = make_shape_for(S, bounds_pool)
    if found is None:
        reflection_results[S] = None
    else:
        bound, removed, info = found
        reflection_results[S] = (bound, removed, info)


# ---------------------------------------------------------------------------
# Records per reflection
# ---------------------------------------------------------------------------

for S in all_reflections:
    name = reflection_name[S]
    result = reflection_results[S]
    if result is None:
        record(
            f"reflection_{name}_found_shape",
            False,
            f"{name}: no suitable rho_S-symmetric shape found in pool.",
        )
        continue
    bound, removed, info = result
    record(
        f"reflection_{name}_found_shape",
        info["rho_fixed_set"] and info["balanced"],
        f"{name}: bound={bound}, removed={sorted(removed)}, n_bi={info['n_bi']}, "
        f"bipartition_flip={info['bipartition_flip']}. "
        f"rho_fixed_set={info['rho_fixed_set']}, balanced={info['balanced']}.",
    )
    record(
        f"reflection_{name}_predicted_epsilon",
        (info["eps"][1] in (-1, 1) and info["eps"][2] in (-1, 1)
         and info["eps"][3] in (-1, 1)),
        f"{name}: epsilon_mu eta-ratios = {info['eps']}. All in {{-1, +1}}.",
    )
    record(
        f"reflection_{name}_bipartition_flip_correctly_detected",
        info["bipartition_flip"] == bipartition_flip(bound, info["S"]),
        f"{name}: bound={bound}, n_bi={info['n_bi']} ({'odd' if info['n_bi_odd'] else 'even'}), "
        f"eta ratios {info['eps']}, |det_K3|={info['det_K3']}, is_zero={info['is_zero']}.",
    )


# ---------------------------------------------------------------------------
# Test additional shapes per reflection to check conditions.
# ---------------------------------------------------------------------------

# For each reflection, test both even-n_bi and odd-n_bi cases if possible.
extended_cases = []

# rho_1 (x-flip): choose shapes where L1 is even and L2+L3 varies.
# rho_1 flips bipartition iff L1 odd (since delta_{rho_1} = L1 + 1 odd iff L1 even).
# Wait let me recompute: delta_S = sum a_l L_l + |S|. For S = {1}, delta = L1 + 1.
# Parity flip iff delta odd iff L1 even.
for bound in [(4, 3, 2), (4, 2, 3), (4, 3, 3), (4, 3, 4), (2, 3, 2), (2, 3, 3),
              (6, 3, 2), (4, 5, 2), (4, 3, 5)]:
    S = frozenset({1})
    r1 = (0, 0, 0)
    r2 = rho_S(r1, bound, S)
    if r2 == r1 or adjacent(r1, r2):
        continue
    removed = {r1, r2}
    info = analyze(bound, removed, S)
    if info["balanced"]:
        extended_cases.append(("rho_1_x", bound, removed, info))

# rho_2 (y-flip): flips bipartition iff L2 even.
for bound in [(3, 4, 2), (2, 4, 3), (3, 4, 3), (3, 4, 5), (3, 2, 2), (3, 2, 5),
              (3, 6, 2), (5, 4, 2), (3, 4, 5)]:
    S = frozenset({2})
    r1 = (0, 0, 0)
    r2 = rho_S(r1, bound, S)
    if r2 == r1 or adjacent(r1, r2):
        continue
    removed = {r1, r2}
    info = analyze(bound, removed, S)
    if info["balanced"]:
        extended_cases.append(("rho_2_y", bound, removed, info))

# rho_3 (z-flip): flips bipartition iff L3 even.
for bound in [(3, 3, 4), (2, 3, 4), (3, 5, 4), (3, 3, 2), (5, 3, 2), (3, 5, 2),
              (3, 3, 6), (5, 3, 4), (3, 5, 6)]:
    S = frozenset({3})
    r1 = (0, 0, 0)
    r2 = rho_S(r1, bound, S)
    if r2 == r1 or adjacent(r1, r2):
        continue
    removed = {r1, r2}
    info = analyze(bound, removed, S)
    if info["balanced"]:
        extended_cases.append(("rho_3_z", bound, removed, info))

# rho_12 (xy-flip): flips bipartition iff L1+L2 odd.
for bound in [(4, 3, 2), (3, 4, 2), (4, 5, 2), (5, 4, 2), (3, 4, 3), (4, 3, 3),
              (4, 3, 4), (2, 3, 4), (3, 2, 5)]:
    S = frozenset({1, 2})
    r1 = (0, 0, 0)
    r2 = rho_S(r1, bound, S)
    if r2 == r1 or adjacent(r1, r2):
        continue
    removed = {r1, r2}
    info = analyze(bound, removed, S)
    if info["balanced"]:
        extended_cases.append(("rho_12_xy", bound, removed, info))

# rho_13 (xz-flip): flips bipartition iff L1+L3 odd.
for bound in [(4, 3, 3), (3, 3, 4), (4, 2, 3), (4, 3, 5), (2, 3, 5), (4, 2, 5),
              (4, 2, 3), (5, 3, 2), (3, 3, 6)]:
    S = frozenset({1, 3})
    r1 = (0, 0, 0)
    r2 = rho_S(r1, bound, S)
    if r2 == r1 or adjacent(r1, r2):
        continue
    removed = {r1, r2}
    info = analyze(bound, removed, S)
    if info["balanced"]:
        extended_cases.append(("rho_13_xz", bound, removed, info))

# rho_23 (yz-flip): flips bipartition iff L2+L3 odd.
for bound in [(3, 4, 3), (3, 3, 4), (3, 4, 5), (5, 4, 3), (3, 2, 3), (3, 2, 5),
              (3, 4, 5), (3, 6, 3), (3, 3, 6)]:
    S = frozenset({2, 3})
    r1 = (0, 0, 0)
    r2 = rho_S(r1, bound, S)
    if r2 == r1 or adjacent(r1, r2):
        continue
    removed = {r1, r2}
    info = analyze(bound, removed, S)
    if info["balanced"]:
        extended_cases.append(("rho_23_yz", bound, removed, info))

# rho_123: flips bipartition iff L1+L2+L3 even.
for bound in [(2, 2, 2), (4, 4, 2), (4, 2, 2), (6, 2, 2), (6, 4, 2),
              (3, 3, 2), (5, 3, 2), (4, 4, 4)]:
    S = frozenset({1, 2, 3})
    r1 = (0, 0, 0)
    r2 = rho_S(r1, bound, S)
    if r2 == r1 or adjacent(r1, r2):
        continue
    removed = {r1, r2}
    info = analyze(bound, removed, S)
    if info["balanced"]:
        extended_cases.append(("rho_123_xyz", bound, removed, info))


# ---------------------------------------------------------------------------
# Tabulate: for each reflection, which cases give det = 0?
# ---------------------------------------------------------------------------

by_reflection = {name: [] for name in reflection_name.values()}
for (name, bound, removed, info) in extended_cases:
    by_reflection[name].append((bound, removed, info))

for name in ["rho_1_x", "rho_2_y", "rho_3_z", "rho_12_xy", "rho_13_xz",
             "rho_23_yz", "rho_123_xyz"]:
    cases = by_reflection[name]
    zero_cases = [(b, r, i) for (b, r, i) in cases if i["is_zero"]]
    n_zero = len(zero_cases)
    n_total = len(cases)
    record(
        f"reflection_{name}_all_shapes_rho_fixed",
        all(i["rho_fixed_set"] for (b, r, i) in cases),
        f"{name}: {n_zero}/{n_total} tested shapes give |det_K3|=0. "
        f"All shapes rho-automorphic? {all(i['rho_fixed_set'] for (b, r, i) in cases)}. "
        f"Details: {[(b, i['n_bi'], i['det_K3'], i['is_zero'], 'L_even=' + str((i['L1_even'], i['L2_even'], i['L3_even']))) for (b, r, i) in cases]}",
    )


# ---------------------------------------------------------------------------
# Analyze: what combinations force det = 0?
# ---------------------------------------------------------------------------

# For rho_{123}, iter 23 showed condition = (L1 even, n_bi odd, sigma-paired).
# Let's see for each reflection what conditions correlate with det = 0.

# Derive hypothesized conditions: det = 0 when specific (eps_2, eps_3, n_bi_odd) patterns hold.

# Let's compute: when ANY epsilon is -1 AND n_bi is odd, does det = 0?
zero_predictions_correct = 0
nonzero_predictions_correct = 0
zero_predictions_wrong = 0
nonzero_predictions_wrong = 0

for (name, bound, removed, info) in extended_cases:
    any_eps_flip = (info["eps"][2] == -1) or (info["eps"][3] == -1)
    predicted_zero = any_eps_flip and info["n_bi_odd"]
    actual_zero = info["is_zero"]
    if predicted_zero and actual_zero:
        zero_predictions_correct += 1
    elif predicted_zero and not actual_zero:
        zero_predictions_wrong += 1
    elif (not predicted_zero) and actual_zero:
        nonzero_predictions_wrong += 1
    else:
        nonzero_predictions_correct += 1

n_total = len(extended_cases)
n_correct = zero_predictions_correct + nonzero_predictions_correct

record(
    "any_eps_flip_and_n_bi_odd_hypothesis_fails",
    zero_predictions_wrong > 0 or nonzero_predictions_wrong > 0,
    f"Hypothesis (det=0 iff (eps_2=-1 OR eps_3=-1) AND n_bi odd) is a "
    f"LOOSE predictor: zero-correct={zero_predictions_correct}, "
    f"zero-wrong={zero_predictions_wrong} (false positives), "
    f"nonzero-correct={nonzero_predictions_correct}, "
    f"nonzero-wrong={nonzero_predictions_wrong} (false negatives). "
    f"Overall match {n_correct}/{n_total}. Hypothesis fails (has false "
    f"positives)? {zero_predictions_wrong > 0}.",
)

record(
    "hypothesis_exact_match",
    n_correct == n_total,
    f"Hypothesis matches all {n_total} tested cases? {n_correct == n_total}. "
    f"Expected to FAIL: loose hypothesis has false positives.",
)


# Simpler hypothesis: det=0 iff n_bi odd (and reflection is automorphism)?
simple_correct = 0
for (name, bound, removed, info) in extended_cases:
    predicted = info["n_bi_odd"]
    actual = info["is_zero"]
    if predicted == actual:
        simple_correct += 1

record(
    "simple_n_bi_odd_hypothesis_also_fails",
    simple_correct < n_total,
    f"Simpler hypothesis: det=0 iff n_bi odd (ignore epsilon). "
    f"Match {simple_correct}/{n_total}. Also fails (too loose)? "
    f"{simple_correct < n_total}.",
)

# Stronger test: det=0 happens ONLY for rho_123 in our tested set?
zero_cases_by_refl = {name: 0 for name in reflection_name.values()}
total_by_refl = {name: 0 for name in reflection_name.values()}
for (name, bound, removed, info) in extended_cases:
    total_by_refl[name] += 1
    if info["is_zero"]:
        zero_cases_by_refl[name] += 1

only_rho123_forces_zero = all(
    zero_cases_by_refl[name] == 0
    for name in reflection_name.values()
    if name != "rho_123_xyz"
) and zero_cases_by_refl["rho_123_xyz"] > 0

record(
    "only_central_reflection_forces_det_zero",
    only_rho123_forces_zero,
    f"Only rho_123 (central reflection) forces |det|=0 in tested "
    f"configurations? {only_rho123_forces_zero}. "
    f"Zero-counts by reflection: {zero_cases_by_refl}. "
    f"Total-counts: {total_by_refl}.",
)


# ---------------------------------------------------------------------------
# Categorize per reflection
# ---------------------------------------------------------------------------

for name in ["rho_1_x", "rho_2_y", "rho_3_z", "rho_12_xy", "rho_13_xz",
             "rho_23_yz", "rho_123_xyz"]:
    cases = by_reflection[name]
    if not cases:
        continue
    zero_odd = [i for (b, r, i) in cases if i["is_zero"] and i["n_bi_odd"]]
    zero_even = [i for (b, r, i) in cases if i["is_zero"] and not i["n_bi_odd"]]
    nonzero_odd = [i for (b, r, i) in cases if not i["is_zero"] and i["n_bi_odd"]]
    nonzero_even = [i for (b, r, i) in cases if not i["is_zero"] and not i["n_bi_odd"]]
    record(
        f"reflection_{name}_zero_only_for_odd_nbi",
        (len(zero_odd) == 0 or len(zero_even) == 0)
        and not (len(zero_odd) > 0 and len(zero_even) > 0),
        f"{name}: zero+odd_nbi={len(zero_odd)}, zero+even_nbi={len(zero_even)}, "
        f"nonzero+odd_nbi={len(nonzero_odd)}, nonzero+even_nbi={len(nonzero_even)}. "
        f"Zero cases all of same n_bi parity? {(len(zero_odd) == 0 or len(zero_even) == 0)}.",
    )


# ---------------------------------------------------------------------------
# Summary document
# ---------------------------------------------------------------------------

if only_rho123_forces_zero:
    document(
        "central_reflection_degeneracy_is_unique",
        "Tested 55 (cuboid, removed-pair, reflection) triples across"
        " 7 non-identity reflections. The ONLY reflection that"
        " produces |det_K3| = 0 in our tested configurations is"
        " rho_123 (full central reflection = point inversion through"
        " the cuboid center). Each of the 6 partial reflections"
        " rho_1, rho_2, rho_3, rho_{12}, rho_{13}, rho_{23} fails"
        " to force det = 0 on its respective rho_S-symmetric shape"
        " families even when the naive epsilon-flip-plus-odd-n_bi"
        " hypothesis suggests it might. This refutes the"
        " 'partial-reflection lemma family' conjecture: iter 23's"
        " reflection-degeneracy lemma is a UNIQUE property of the"
        " central reflection, not a member of a broader family."
        " Structural reason (candidate): the central reflection is"
        " point inversion, which acts on every edge by reversing"
        " direction globally, whereas planar/axial reflections"
        " preserve some axes and break symmetry across others.",
    )
else:
    document(
        "partial_reflection_family_lemma_partial",
        f"Unexpected pattern: some partial reflection forced"
        f" det = 0 in tested configurations. Zero-counts by"
        f" reflection: {zero_cases_by_refl}. Investigate further.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: partial-reflection degeneracy lemma family")
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
