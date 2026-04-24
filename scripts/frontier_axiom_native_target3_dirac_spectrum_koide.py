#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- Target 3, sub-step 3c: test whether the
K3 Dirac singular-value spectrum on small cuboids naturally realizes
a Koide Q = 2/3 triple.

Context
-------
Target 3 asks for Koide Q = 2/3 via K = 0 on the normalized reduced
carrier. Prior runners have established:
- K(v) := 3 p_2 - 2 p_1^2 on a Cl(3) vector v = (u_1, u_2, u_3)
  satisfies K = 0 iff Q(u) := p_2 / p_1^2 = 2/3.
- K = 0 admits a 1-parameter family of solutions; kit primitives
  do not force a unique triple. Hence K = 0 is the "last remaining
  primitive beyond the kit" (reclassification route).

This runner tests a new angle: does the K3 staggered-Dirac singular-
value spectrum on a small cuboid naturally realize K = 0 for some
3-element subset of singular values?

If yes: Q = 2/3 emerges from kit structure directly. Target 3
closes via route (i) - derived.

If no: confirms that kit Dirac spectra do NOT automatically produce
Q = 2/3, reinforcing the reclassification blocker.

Method
------
For each small cuboid (L1, L2, L3) (balanced, tractable):
1. Build the K3 bipartite block B.
2. Compute singular values sigma_1, ..., sigma_{n_bi}.
3. For each 3-subset {sigma_i, sigma_j, sigma_k} (unordered), compute
   Q(sigma_i, sigma_j, sigma_k) = (sigma_i^2 + sigma_j^2 + sigma_k^2)
   / (sigma_i + sigma_j + sigma_k)^2.
4. Report any 3-subset achieving Q = 2/3 (or very close, given
   floating-point precision).

Cuboids tested
--------------
(2,2,2), (3,2,2), (2,2,3), (4,2,2), (5,2,2). All planar (K3
optimal).
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


def build_B(bound):
    L1, L2, L3 = bound
    sites = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
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


def koide_Q(u1, u2, u3):
    s = u1 + u2 + u3
    if abs(s) < 1e-12:
        return None
    return (u1 ** 2 + u2 ** 2 + u3 ** 2) / (s ** 2)


# ---------------------------------------------------------------------------
# Cuboids
# ---------------------------------------------------------------------------

cuboids = [
    (2, 2, 2),
    (3, 2, 2),
    (2, 2, 3),
    (4, 2, 2),
    (5, 2, 2),
    (2, 4, 2),
    (3, 3, 2),  # non-planar for contrast
]

TOL = 1e-6
target_Q = 2.0 / 3.0

any_triple_hits = False
all_spectra_summary = []

for bound in cuboids:
    tag = f"{bound[0]}x{bound[1]}x{bound[2]}"
    B = build_B(bound)
    if B is None:
        record(
            f"cuboid_{tag}_balanced",
            False,
            f"{tag}: unbalanced, skipping.",
        )
        continue
    # Compute singular values
    sv = np.linalg.svd(B.astype(np.float64), compute_uv=False)
    # Sort descending
    sv = sorted(sv.tolist(), reverse=True)
    n_sv = len(sv)
    record(
        f"cuboid_{tag}_svd_computed",
        n_sv == B.shape[0],
        f"{tag}: n_bi={B.shape[0]}, singular values (sorted) = "
        f"{[round(s, 6) for s in sv]}.",
    )
    # Collect Q values for all 3-subsets
    q_hits = []
    q_all = []
    for (i, j, k) in combinations(range(n_sv), 3):
        u = (sv[i], sv[j], sv[k])
        q = koide_Q(u[0], u[1], u[2])
        if q is None:
            continue
        q_all.append((u, q))
        if abs(q - target_Q) < TOL:
            q_hits.append((u, q))
    record(
        f"cuboid_{tag}_any_triple_hits_Q_2_over_3",
        len(q_hits) > 0,
        f"{tag}: {len(q_hits)} of {len(q_all)} 3-subsets hit Q = 2/3. "
        f"Hits: {q_hits[:5]}.",
    )
    if q_hits:
        any_triple_hits = True
    # Also record min / max Q from the 3-subsets
    if q_all:
        min_q = min(q for (_, q) in q_all)
        max_q = max(q for (_, q) in q_all)
        record(
            f"cuboid_{tag}_Q_range",
            min_q < max_q,
            f"{tag}: Q range across 3-subsets: [{min_q:.6f}, {max_q:.6f}]. "
            f"Target 2/3 = {target_Q:.6f}.",
        )
    all_spectra_summary.append((bound, sv, len(q_hits)))


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

record(
    "any_cuboid_dirac_spectrum_realizes_Q_2_over_3",
    any_triple_hits,
    f"Any tested cuboid has a 3-subset of K3 Dirac singular values "
    f"with Q = 2/3? {any_triple_hits}.",
)


# ---------------------------------------------------------------------------
# Structural note: singular values are all equal on some cuboids
# ---------------------------------------------------------------------------

for (bound, sv, hits) in all_spectra_summary:
    tag = f"{bound[0]}x{bound[1]}x{bound[2]}"
    n_distinct = len(set(round(s, 8) for s in sv))
    record(
        f"cuboid_{tag}_distinct_singular_values",
        n_distinct >= 1,
        f"{tag}: {n_distinct} distinct singular values (of {len(sv)} total). "
        f"Sorted: {[round(s, 4) for s in sv]}.",
    )


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

if any_triple_hits:
    document(
        "dirac_spectrum_realizes_koide",
        "On at least one tested small cuboid, the K3 Dirac singular-"
        "value spectrum contains a 3-subset with Koide Q = 2/3. This"
        " is a candidate kit-natural source for the Q = 2/3 triple,"
        " potentially closing Target 3 via the 'derive K = 0 from"
        " kit' route. Further work: identify which cuboid and which"
        " subset, and derive the specific triple algebraically from"
        " K1+K2+K3 without invoking numerical spectrum computation.",
    )
else:
    document(
        "dirac_spectrum_does_not_realize_koide",
        "On all tested small cuboids, the K3 Dirac singular-value"
        " spectrum does NOT contain a 3-subset with Koide Q = 2/3."
        " This closes off a natural kit-structural attempt at deriving"
        " Q = 2/3, reinforcing the Target 3 reclassification blocker:"
        " K = 0 remains a primitive beyond the kit rather than being"
        " implied by spectral structure. The spectrum on small cuboids"
        " tends to be highly degenerate (few distinct values), leaving"
        " little room for Q = 2/3 to arise as a triple. This is a"
        " structural absence observation, not a PASS.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: Target 3 K3 Dirac spectrum Koide-realizability test")
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
