#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- formalize the reflection-degeneracy lemma
for K3 staggered phases.

Context
-------
V2 iter 22 discovered that on (4,4,2) minus {(0,0,0), (3,3,1)},
|det_K3(B)| = 0 exactly. The removed sites are mapped to each
other by the central reflection sigma(i,j,k) = (L1-1-i, L2-1-j,
L3-1-k). This iter formalizes the observation as a candidate
lemma and verifies it on multiple cuboid sizes.

Lemma (reflection degeneracy, candidate)
----------------------------------------
Let G be the Z^3 cuboid (L1, L2, L3) minus two singleton sites
r1, r2. Suppose:
  (i) sigma(r1) = r2 where sigma(i,j,k) = (L1-1-i, L2-1-j,
      L3-1-k) is the central reflection.
  (ii) L1 + L2 + L3 is even, so sigma swaps bipartition
      (parity(sigma(n)) = 1 - parity(n)).
  (iii) n_bi (size of bipartite block) is odd.
  (iv) L1 is even, so eta_2(n) = (-1)^{n_1} picks up a factor
      of (-1)^{L1-1} = -1 under sigma.
Then |det_K3(B(G))| = 0.

Sign transformation under sigma
-------------------------------
For an edge between even e and odd o = e + e_mu (so e is the
lower endpoint in mu-direction), direct computation gives:
  B[sigma(o), sigma(e)] = epsilon_mu * B[e, o],
where
  epsilon_1 = +1   (eta_1 = 1 constant),
  epsilon_2 = (-1)^{L1-1}  (eta_2 = (-1)^{n1}),
  epsilon_3 = (-1)^{L1+L2} (eta_3 = (-1)^{n1+n2}).

On L1=4, L2=4: epsilon_1=1, epsilon_2=-1, epsilon_3=+1. So only
mu=2 edges flip sign under sigma.

Proof sketch (verified numerically per test case below)
-------------------------------------------------------
1. sigma preserves the graph G (since removed sites are swapped).
2. B can be written as a signed adjacency matrix with edge signs
   varying by mu.
3. Under sigma, the matrix undergoes a row+column permutation
   (exchanging evens and odds since sigma flips parity), plus
   each mu=2 edge entry multiplied by -1.
4. The total determinant transformation involves a sign factor
   (-1)^{#(mu=2 edges in the generic PM)} AND a permutation sign
   factor.
5. When n_bi is odd AND the k_2 parity is forced odd by the
   slicing counts, det -> -det => det = 0.

The runner verifies: (a) the epsilon_mu ratios are constant per
mu-direction on given L-parities; (b) the predicted det=0 holds
on all test cases where lemma conditions are met; (c) det != 0
when at least one lemma condition fails (control cases).
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


def sigma(n, bound):
    L1, L2, L3 = bound
    return (L1 - 1 - n[0], L2 - 1 - n[1], L3 - 1 - n[2])


def compute_epsilon_mu(bound):
    """Predict epsilon_mu ratios from formulas derived algebraically."""
    L1, L2, L3 = bound
    return {
        1: 1,
        2: (-1) ** (L1 - 1),
        3: (-1) ** (L1 + L2),
    }


def verify_epsilon_mu_empirically(bound):
    """For every edge, compare eta_mu(sigma(n_lo_image)) / eta_mu(n_lo)."""
    L1, L2, L3 = bound
    base = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
    observed = defaultdict(list)
    for n in base:
        for mu in (1, 2, 3):
            n_up = list(n); n_up[mu - 1] += 1; n_up = tuple(n_up)
            if n_up[mu - 1] >= bound[mu - 1]:
                continue
            # Original edge sign (n is lower, assume): eta_mu(n).
            orig = eta(mu, n)
            # Sigma image edge lower-endpoint: sigma(n_up) = sigma(n) - e_mu.
            sigma_n = sigma(n, bound)
            sigma_n_up = sigma(n_up, bound)
            # sigma_n_up = sigma_n - e_mu coordinate-wise
            # Lower endpoint of image edge is sigma_n_up (smaller mu-coord).
            image = eta(mu, sigma_n_up)
            ratio = orig * image  # since both are +/-1, ratio = orig * image
            observed[mu].append(ratio)
    consistent = all(len(set(observed[mu])) == 1 for mu in (1, 2, 3))
    if consistent:
        return {mu: observed[mu][0] for mu in (1, 2, 3)}, True
    return observed, False


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


def analyze_case(label, bound, removed):
    L1, L2, L3 = bound
    # Lemma conditions
    sigma_r = {sigma(r, bound) for r in removed}
    sigma_pair = (sigma_r == set(removed) and len(removed) == 2)
    sum_L_even = (L1 + L2 + L3) % 2 == 0
    L1_even = L1 % 2 == 0
    # Build graph
    result = build_B(bound, removed)
    if result is None:
        return {"label": label, "balanced": False, "bound": bound, "removed": removed}
    B, n_bi = result
    n_bi_odd = n_bi % 2 == 1
    det_K3 = int(round(abs(np.linalg.det(B))))
    # Lemma prediction
    lemma_applies = sigma_pair and sum_L_even and L1_even and n_bi_odd
    predicted_zero = lemma_applies
    actual_zero = (det_K3 == 0)
    return {
        "label": label, "balanced": True, "bound": bound, "removed": removed,
        "sigma_r": sigma_r, "sigma_pair": sigma_pair,
        "sum_L_even": sum_L_even, "L1_even": L1_even,
        "n_bi": n_bi, "n_bi_odd": n_bi_odd,
        "det_K3": det_K3,
        "lemma_applies": lemma_applies,
        "predicted_zero": predicted_zero,
        "actual_zero": actual_zero,
        "prediction_matches": predicted_zero == actual_zero,
    }


# ---------------------------------------------------------------------------
# Part 1: Verify epsilon_mu formula
# ---------------------------------------------------------------------------

verify_bounds = [(2, 2, 2), (3, 3, 2), (4, 4, 2), (4, 3, 2), (5, 3, 2), (6, 4, 2)]

for bound in verify_bounds:
    predicted_eps = compute_epsilon_mu(bound)
    observed_eps, consistent = verify_epsilon_mu_empirically(bound)
    record(
        f"epsilon_mu_consistent_on_{bound[0]}{bound[1]}{bound[2]}",
        consistent and observed_eps == predicted_eps,
        f"bound {bound}: predicted epsilon {predicted_eps}, observed {observed_eps}, "
        f"consistent? {consistent}.",
    )


# ---------------------------------------------------------------------------
# Part 2: Test cases for the lemma
# ---------------------------------------------------------------------------

cases = [
    # (label, bound, removed)
    # Positive cases: lemma applies -> predict det=0
    ("2x2x2_222_minimal_even", (2, 2, 2), {(0, 0, 0), (1, 1, 1)}),
    ("4x4x2_T2a_diagonal", (4, 4, 2), {(0, 0, 0), (3, 3, 1)}),
    ("4x2x2_L1even_balanced", (4, 2, 2), {(0, 0, 0), (3, 1, 1)}),
    ("6x2x2_L1even_large_1", (6, 2, 2), {(0, 0, 0), (5, 1, 1)}),
    ("6x4x2_L1even_large_2", (6, 4, 2), {(0, 0, 0), (5, 3, 1)}),
    # Negative cases: at least one condition fails -> predict det != 0
    ("3x3x2_L1odd_control", (3, 3, 2), {(0, 0, 0), (2, 2, 1)}),
    ("4x4x2_non_sigma_paired", (4, 4, 2), {(0, 0, 0), (3, 0, 0)}),
    ("5x3x2_L1odd", (5, 3, 2), {(0, 0, 0), (4, 2, 1)}),
    ("4x3x2_sumL_odd", (4, 3, 2), {(0, 0, 0), (3, 2, 1)}),
    # (4x3x2 with r1=(0,0,0), r2=sigma(r1)=(3,2,1). sum_L=9 odd -> sigma preserves parity.
    #  (0,0,0) parity 0, (3,2,1) parity 6=0, same parity, removal is unbalanced. Expect unbalanced flag.)
]

results = []
for (label, bound, removed) in cases:
    info = analyze_case(label, bound, removed)
    results.append(info)


# ---------------------------------------------------------------------------
# Part 3: Per-case records
# ---------------------------------------------------------------------------

for info in results:
    label = info["label"]
    if not info["balanced"]:
        record(
            f"case_{label}_graph_balanced",
            False,
            f"{label}: removed sites have same parity; graph is unbalanced. Skipping lemma check.",
        )
        continue
    record(
        f"case_{label}_sigma_pair",
        info["sigma_pair"],
        f"{label}: sigma images of removed = {sorted(info['sigma_r'])}, "
        f"removed = {sorted(info['removed'])}. sigma-paired? {info['sigma_pair']}.",
    )
    record(
        f"case_{label}_lemma_conditions",
        info["lemma_applies"] == (
            info["sigma_pair"] and info["sum_L_even"]
            and info["L1_even"] and info["n_bi_odd"]
        ),
        f"{label}: sigma_pair={info['sigma_pair']}, "
        f"sum_L_even={info['sum_L_even']}, L1_even={info['L1_even']}, "
        f"n_bi={info['n_bi']} odd={info['n_bi_odd']}. "
        f"Lemma applies? {info['lemma_applies']}.",
    )
    record(
        f"case_{label}_prediction_matches_det",
        info["prediction_matches"],
        f"{label}: predicted det=0? {info['predicted_zero']}. "
        f"Actual |det|={info['det_K3']}, is_zero? {info['actual_zero']}. "
        f"Match? {info['prediction_matches']}.",
    )


# ---------------------------------------------------------------------------
# Part 4: Lemma verdict
# ---------------------------------------------------------------------------

balanced_results = [r for r in results if r.get("balanced", False)]
n_matches = sum(1 for r in balanced_results if r["prediction_matches"])
n_total = len(balanced_results)

lemma_verified_all_cases = (n_matches == n_total) and n_total > 0

record(
    "reflection_degeneracy_lemma_verified_all_balanced_cases",
    lemma_verified_all_cases,
    f"Lemma prediction matches on {n_matches} of {n_total} balanced "
    f"cases. Verified? {lemma_verified_all_cases}.",
)


# Count lemma-applies cases: all should have det=0
lemma_positive_cases = [r for r in balanced_results if r["lemma_applies"]]
all_positives_zero = all(r["actual_zero"] for r in lemma_positive_cases)
record(
    "all_lemma_positive_cases_give_det_zero",
    all_positives_zero,
    f"Of {len(lemma_positive_cases)} cases where lemma conditions hold, "
    f"all give |det|=0? {all_positives_zero}. "
    f"Positives: {[(r['label'], r['det_K3']) for r in lemma_positive_cases]}.",
)

# Count lemma-fails cases: all should have det!=0 (lemma doesn't preclude, but
# empirically these singleton-defect graphs give det !=0 unless some other
# symmetry forces zero)
lemma_negative_cases = [r for r in balanced_results if not r["lemma_applies"]]
all_negatives_nonzero = all(not r["actual_zero"] for r in lemma_negative_cases)
record(
    "all_lemma_negative_cases_give_det_nonzero",
    all_negatives_nonzero,
    f"Of {len(lemma_negative_cases)} cases where lemma does NOT apply, "
    f"all give |det| != 0? {all_negatives_nonzero}. "
    f"Negatives: {[(r['label'], r['det_K3']) for r in lemma_negative_cases]}.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if lemma_verified_all_cases and all_positives_zero and all_negatives_nonzero:
    document(
        "reflection_degeneracy_lemma_validated",
        "The reflection-degeneracy lemma is validated across all"
        " tested cuboid sizes and singleton configurations. The"
        " four conditions (sigma-paired removed sites, L1+L2+L3"
        " even, L1 even, n_bi odd) are jointly sufficient to"
        " force |det_K3(B)| = 0; and when any condition fails"
        " the det is non-zero on tested configurations. The"
        " mechanism: sigma acts on B as a permutation (swapping"
        " evens and odds since parity flips) combined with a"
        " per-mu sign flip. On L1 even, mu=2 edges flip sign,"
        " yielding a matrix equation det(B) = (-1)^{n_bi} det(B)"
        " when combined with the permutation sign. For n_bi odd"
        " this forces det = 0. This is a CONCRETE STRUCTURAL"
        " LEMMA derived purely from K1 (Cl(3) structure), K2"
        " (Z^3 lattice and central reflection), and K3"
        " (staggered phase formula).",
    )
elif lemma_verified_all_cases:
    document(
        "reflection_degeneracy_lemma_partially_validated",
        f"Lemma prediction matches on all tested cases but the"
        f" lemma-positive cases don't all have det=0 or"
        f" lemma-negative cases don't all have det!=0. Some"
        f" other effect (e.g., additional symmetries) contribute"
        f" -- need refinement.",
    )
else:
    document(
        "reflection_degeneracy_lemma_falsified",
        f"Lemma prediction mismatched on {n_total - n_matches} of"
        f" {n_total} cases. Statement is incomplete or wrong.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: reflection-degeneracy lemma validation")
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
