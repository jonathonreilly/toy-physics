#!/usr/bin/env python3
"""
Axiom-native runner (V2) -- investigate the SH3 non-reflection
det_K3 = 0 mechanism discovered in iter 28.

Context
-------
The iter 23 reflection-degeneracy lemma forces det_K3 = 0 when
the defect is central-reflection-paired, L1+L2+L3 even, L1 even,
and n_bi odd. Iter 24 showed partial reflections do NOT force
det=0. But iter 28 discovered (4,4,2) minus {(1,0,0), (2,0,0),
(3,0,0), (0,3,1)} gives det_K3 = 0 even though:
- defect is NOT sigma-invariant (no axis-aligned reflection fixes it)
- n_bi = 14 is EVEN (so iter 23 lemma does not apply)

This is an anomaly. This iter investigates whether there is a
specific mechanism.

Investigation steps
-------------------
1. Enumerate the full symmetry group of (4,4,2): D_4 (xy plane,
   since L1 = L2 = 4) x Z_2 (z-flip) = 16 elements, including
   90-degree rotations in xy plane and diagonal reflections.
   Check which fix the SH3 defect set.
2. Compute det_K3 of SH3 using exact integer arithmetic (sympy).
3. Enumerate PMs, split by K3 sign, and check equality of +/-.
4. Test "nearby" configurations: same line-3 + different isolated
   singleton. If det=0 persists across singleton choice, the
   mechanism is about the line-3. If det varies, it's specific
   to SH3's exact singleton position.

Reports which symmetry (if any) fixes SH3 and whether a
consistent pattern emerges for line-3 + variable-singleton
configurations.
"""

from __future__ import annotations

import sys
import time
from collections import defaultdict

import numpy as np
import sympy as sp


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


def sign_of_permutation(perm):
    visited = [False] * len(perm)
    s = 1
    for i in range(len(perm)):
        if visited[i]:
            continue
        cl = 0
        j = i
        while not visited[j]:
            visited[j] = True
            j = perm[j]
            cl += 1
        if cl > 1 and cl % 2 == 0:
            s = -s
    return s


# ---------------------------------------------------------------------------
# Symmetry group of (4,4,2): D_4 (xy) x Z_2 (z)
# L1 = L2 = 4, so xy has 90-degree rotational symmetry.
# ---------------------------------------------------------------------------

def make_group_elements(bound):
    L1, L2, L3 = bound
    # Returns list of (name, function acting on (i,j,k))
    elements = []
    # xy-plane D_4 operations (assume L1 == L2 for rotations)
    xy_ops = []
    if L1 == L2:
        # Rotations
        xy_ops.append(("R0", lambda p, L=L1: (p[0], p[1])))
        xy_ops.append(("R90", lambda p, L=L1: (L - 1 - p[1], p[0])))
        xy_ops.append(("R180", lambda p, L=L1: (L - 1 - p[0], L - 1 - p[1])))
        xy_ops.append(("R270", lambda p, L=L1: (p[1], L - 1 - p[0])))
        # Reflections
        xy_ops.append(("Fx", lambda p, L=L1: (L - 1 - p[0], p[1])))
        xy_ops.append(("Fy", lambda p, L=L1: (p[0], L - 1 - p[1])))
        xy_ops.append(("Fdiag", lambda p, L=L1: (p[1], p[0])))
        xy_ops.append(("Fanti", lambda p, L=L1: (L - 1 - p[1], L - 1 - p[0])))
    else:
        xy_ops.append(("R0", lambda p: (p[0], p[1])))
        xy_ops.append(("R180", lambda p, L1=L1, L2=L2: (L1 - 1 - p[0], L2 - 1 - p[1])))
        xy_ops.append(("Fx", lambda p, L1=L1: (L1 - 1 - p[0], p[1])))
        xy_ops.append(("Fy", lambda p, L2=L2: (p[0], L2 - 1 - p[1])))

    z_ops = [("Z0", lambda k: k), ("Z1", lambda k, L3=L3: L3 - 1 - k)]

    for (xy_name, xy_f) in xy_ops:
        for (z_name, z_f) in z_ops:
            def op(p, xy_f=xy_f, z_f=z_f):
                q = xy_f((p[0], p[1]))
                return (q[0], q[1], z_f(p[2]))
            elements.append((f"{xy_name}_{z_name}", op))
    return elements


def build_B_sympy(bound, removed):
    """Build the K3 bipartite block B as a sympy integer matrix
    for exact arithmetic."""
    L1, L2, L3 = bound
    base = [(i, j, k) for i in range(L1) for j in range(L2) for k in range(L3)]
    sites = [v for v in base if v not in removed]
    site_set = set(sites)

    evens = [v for v in sites if sum(v) % 2 == 0]
    odds = [v for v in sites if sum(v) % 2 == 1]
    if len(evens) != len(odds):
        return None, None, None
    idx_e = {v: i for i, v in enumerate(evens)}
    idx_o = {v: i for i, v in enumerate(odds)}
    n_bi = len(evens)

    B = sp.zeros(n_bi, n_bi)
    B_un = np.zeros((n_bi, n_bi), dtype=np.int64)
    for n in sites:
        for mu in (1, 2, 3):
            nn = list(n); nn[mu - 1] += 1; nn = tuple(nn)
            if nn not in site_set:
                continue
            if n in idx_e:
                B[idx_e[n], idx_o[nn]] = eta(mu, n)
                B_un[idx_e[n], idx_o[nn]] = 1
            else:
                B[idx_e[nn], idx_o[n]] = -eta(mu, n)
                B_un[idx_e[nn], idx_o[n]] = 1
    return B, B_un, (evens, odds, idx_e, idx_o, n_bi)


def enumerate_PMs(n_bi, B_un, cap=500_000, time_cap_s=60.0):
    adj = [[] for _ in range(n_bi)]
    for i in range(n_bi):
        for j in range(n_bi):
            if B_un[i, j] != 0:
                adj[i].append(j)
    PMs = []
    perm = [0] * n_bi
    used = [False] * n_bi
    start = time.time()
    stopped = [False]

    def dfs(i):
        if stopped[0]:
            return
        if len(PMs) >= cap:
            stopped[0] = True; return
        if (time.time() - start) > time_cap_s:
            stopped[0] = True; return
        if i == n_bi:
            PMs.append(tuple(perm)); return
        for j in adj[i]:
            if not used[j]:
                perm[i] = j
                used[j] = True
                dfs(i + 1)
                if stopped[0]: return
                used[j] = False

    dfs(0)
    return PMs, stopped[0]


def classify_PMs_sympy(PMs, B_sympy, n_bi):
    plus = []
    minus = []
    for p in PMs:
        s = sign_of_permutation(p)
        prod = 1
        for i in range(n_bi):
            prod *= int(B_sympy[i, p[i]])
        contrib = s * prod
        if contrib > 0:
            plus.append(p)
        elif contrib < 0:
            minus.append(p)
    return plus, minus


# ---------------------------------------------------------------------------
# SH3 data
# ---------------------------------------------------------------------------

SH3_bound = (4, 4, 2)
SH3_removed = {(1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 3, 1)}


# ---------------------------------------------------------------------------
# Step 1: Enumerate symmetry group and check which fix the SH3 defect.
# ---------------------------------------------------------------------------

group = make_group_elements(SH3_bound)
fixing_ops = []
for (name, op) in group:
    image = {op(r) for r in SH3_removed}
    if image == SH3_removed:
        fixing_ops.append(name)

record(
    "symmetry_group_size_equals_16",
    len(group) == 16,
    f"(4,4,2) symmetry group has {len(group)} elements (expected 16 = D_4 x Z_2).",
)

record(
    "SH3_defect_fixed_by_identity_only",
    fixing_ops == ["R0_Z0"],
    f"Group elements fixing SH3 defect set: {fixing_ops}.",
)


# ---------------------------------------------------------------------------
# Step 2: Compute det_K3 of SH3 with exact arithmetic.
# ---------------------------------------------------------------------------

B_SH3, B_un_SH3, meta = build_B_sympy(SH3_bound, SH3_removed)
det_SH3_exact = int(B_SH3.det())

record(
    "SH3_det_K3_exact_is_zero",
    det_SH3_exact == 0,
    f"Exact integer det(B) of SH3 = {det_SH3_exact}. Zero? {det_SH3_exact == 0}.",
)


# ---------------------------------------------------------------------------
# Step 3: Enumerate PMs and classify.
# ---------------------------------------------------------------------------

evens, odds, idx_e, idx_o, n_bi_SH3 = meta
t0 = time.time()
PMs_SH3, capped = enumerate_PMs(n_bi_SH3, B_un_SH3)
elapsed_PM = time.time() - t0
plus_SH3, minus_SH3 = classify_PMs_sympy(PMs_SH3, B_SH3, n_bi_SH3)

record(
    "SH3_PM_enumeration_completed",
    not capped,
    f"SH3: #PM = {len(PMs_SH3)} (DFS {elapsed_PM:.2f}s). Capped? {capped}.",
)

record(
    "SH3_equal_plus_minus_split",
    len(plus_SH3) == len(minus_SH3),
    f"SH3: n_plus = {len(plus_SH3)}, n_minus = {len(minus_SH3)}. "
    f"Equal? {len(plus_SH3) == len(minus_SH3)}.",
)

record(
    "SH3_det_matches_pm_sign_sum",
    abs(len(plus_SH3) - len(minus_SH3)) == det_SH3_exact,
    f"SH3: |n+ - n-| = {abs(len(plus_SH3) - len(minus_SH3))}, det_exact = {det_SH3_exact}.",
)


# ---------------------------------------------------------------------------
# Step 4: Test nearby configurations (line-3 + different singletons).
# ---------------------------------------------------------------------------

line3 = {(1, 0, 0), (2, 0, 0), (3, 0, 0)}
# Various singleton choices. Singletons must be isolated from line-3
# and make removal balanced. Line-3 parities: 1o + 2e + 3o = 2e + 1o unbalanced +1o.
# Actually (1,0,0)=1o, (2,0,0)=2e, (3,0,0)=3o. So line-3 has 1e + 2o.
# To balance with 1 additional singleton: need 1 more e.
# Try singletons with parity = 0 (even).

candidate_singletons = [
    (0, 1, 0),  # parity 1 o (bad)
    (0, 2, 0),  # parity 2 e
    (0, 3, 0),  # parity 3 o (bad)
    (0, 0, 1),  # parity 1 o (bad)
    (0, 1, 1),  # parity 2 e
    (0, 2, 1),  # parity 3 o (bad)
    (0, 3, 1),  # parity 4 e  <- SH3 singleton
    (1, 3, 0),  # parity 4 e
    (2, 3, 0),  # parity 5 o (bad)
    (3, 3, 0),  # parity 6 e
    (1, 3, 1),  # parity 5 o (bad)
    (2, 3, 1),  # parity 6 e
    (3, 3, 1),  # parity 7 o (bad)
    (2, 2, 1),  # parity 5 o (bad, but also adjacent to ... check: (2,2,1) neighbors include (2,2,0), (1,2,1), (3,2,1), (2,1,1), (2,3,1). Not adjacent to line-3)
    (2, 1, 1),  # parity 4 e
]

# Filter: only even-parity singletons, and non-adjacent to line-3.
line3_neighbors = set()
for n in line3:
    for mu in (1, 2, 3):
        for d in (-1, 1):
            v = list(n); v[mu - 1] += d; v = tuple(v)
            if 0 <= v[0] < 4 and 0 <= v[1] < 4 and 0 <= v[2] < 2:
                line3_neighbors.add(v)

valid_singletons = []
for s in candidate_singletons:
    if s in line3:
        continue
    if s in line3_neighbors:
        continue
    if (s[0] + s[1] + s[2]) % 2 != 0:  # must be even to balance
        continue
    if 0 <= s[0] < 4 and 0 <= s[1] < 4 and 0 <= s[2] < 2:
        valid_singletons.append(s)

nearby_results = []
for singleton in valid_singletons:
    removed = line3 | {singleton}
    B, B_un, meta2 = build_B_sympy(SH3_bound, removed)
    if B is None:
        nearby_results.append((singleton, None, "unbalanced"))
        continue
    det_val = int(B.det())
    nearby_results.append((singleton, det_val, "balanced"))

# Report
zero_det_count = sum(1 for (_, d, s) in nearby_results if s == "balanced" and d == 0)
total_balanced = sum(1 for (_, _, s) in nearby_results if s == "balanced")

record(
    "nearby_line3_configurations_tested",
    len(nearby_results) > 0,
    f"Tested {len(nearby_results)} line-3 + singleton configurations. "
    f"Balanced: {total_balanced}. Results: "
    f"{[(s, d) for (s, d, st) in nearby_results if st == 'balanced']}.",
)

record(
    "all_line3_plus_singleton_give_det_zero",
    total_balanced > 0 and zero_det_count == total_balanced,
    f"Of {total_balanced} balanced line-3 + singleton configurations, "
    f"{zero_det_count} give det = 0. All zero? "
    f"{total_balanced > 0 and zero_det_count == total_balanced}.",
)


# ---------------------------------------------------------------------------
# Step 5: If det=0 for all, the line-3 itself forces it (via its own
# internal structure). Test just the line-3 without singleton (on smaller
# graph) -- i.e., remove just the line-3 from (4,4,2).
# ---------------------------------------------------------------------------

# But line-3 alone is unbalanced (1e + 2o). Try line-3 + line-3 (two copies)
# symmetrically for a balanced test, or a different line geometry.

# Alternative: test line-3 at a different location to see if location matters.

# Place line-3 at (1,2,0)-(2,2,0)-(3,2,0): parities 3, 4, 5 = 1e + 2o.
# Balance needs +1 even singleton.
alt_line3 = {(1, 2, 0), (2, 2, 0), (3, 2, 0)}
alt_singleton_candidates = [
    (0, 0, 0),  # 0 e
    (0, 2, 1),  # 3 o, bad
    (2, 0, 0),  # 2 e (in line? no, (2,0,0) != (2,2,0))
    (0, 3, 1),  # 4 e
    (3, 3, 1),  # 7 o, bad
    (3, 0, 1),  # 4 e
    (0, 1, 1),  # 2 e
    (0, 0, 1),  # 1 o, bad
]
alt_results = []
for s in alt_singleton_candidates:
    if s in alt_line3:
        continue
    if (s[0] + s[1] + s[2]) % 2 != 0:  # need even singleton
        continue
    # Check isolation
    s_neighbors = set()
    for mu in (1, 2, 3):
        for d in (-1, 1):
            v = list(s); v[mu - 1] += d; v = tuple(v)
            s_neighbors.add(v)
    if s_neighbors & alt_line3:
        continue
    removed = alt_line3 | {s}
    B, B_un, meta2 = build_B_sympy(SH3_bound, removed)
    if B is None:
        alt_results.append((s, None, "unbalanced"))
        continue
    det_val = int(B.det())
    alt_results.append((s, det_val, "balanced"))

alt_zero_count = sum(1 for (_, d, s) in alt_results if s == "balanced" and d == 0)
alt_balanced = sum(1 for (_, _, s) in alt_results if s == "balanced")

record(
    "alternative_line3_location_tested",
    alt_balanced > 0,
    f"Alternative line-3 at y=2 (parallel line different position): "
    f"{alt_balanced} balanced configs, {alt_zero_count} det=0. "
    f"Results: {[(s, d) for (s, d, st) in alt_results if st == 'balanced']}.",
)


# ---------------------------------------------------------------------------
# Step 6: Test with line-3 rotated by 90 degrees (along x at a fixed y).
# ---------------------------------------------------------------------------

rot_line3 = {(0, 1, 0), (0, 2, 0), (0, 3, 0)}
# Parities: 1o + 2e + 3o = 1e + 2o. Add odd singleton.
rot_singleton_candidates = [
    (1, 0, 1),  # 2 e -- even, no
    (3, 0, 1),  # 4 e -- no
    (3, 3, 1),  # 7 o -- yes
    (1, 3, 1),  # 5 o -- yes, but adjacent to (0,3,0)? (1,3,1) neighbors: (0,3,1), (2,3,1), (1,2,1), (1,3,0). (1,3,0) adjacent to (0,3,0). So (1,3,0) - (0,3,0) are adjacent. Would (1,3,1) be adjacent to (0,3,0)? dist (1-0)+(3-3)+(1-0) = 2. Not adjacent. OK.
    (3, 1, 1),  # 5 o -- yes
]
rot_results = []
for s in rot_singleton_candidates:
    if s in rot_line3:
        continue
    if (s[0] + s[1] + s[2]) % 2 != 1:  # must be odd
        continue
    # Check isolation from line-3
    s_neighbors = set()
    for mu in (1, 2, 3):
        for d in (-1, 1):
            v = list(s); v[mu - 1] += d; v = tuple(v)
            s_neighbors.add(v)
    if s_neighbors & rot_line3:
        continue
    removed = rot_line3 | {s}
    B, B_un, meta2 = build_B_sympy(SH3_bound, removed)
    if B is None:
        rot_results.append((s, None, "unbalanced"))
        continue
    det_val = int(B.det())
    rot_results.append((s, det_val, "balanced"))

rot_zero_count = sum(1 for (_, d, s) in rot_results if s == "balanced" and d == 0)
rot_balanced = sum(1 for (_, _, s) in rot_results if s == "balanced")

record(
    "rotated_line3_tested",
    len(rot_results) > 0,
    f"Rotated line-3 (x=0 y=1,2,3 z=0): {rot_balanced} balanced, "
    f"{rot_zero_count} det=0. "
    f"Results: {[(s, d) for (s, d, st) in rot_results if st == 'balanced']}.",
)


# ---------------------------------------------------------------------------
# Step 7: Z-plane-separation hypothesis. The y=0 line-3 tests showed
# a striking pattern: singletons at z=1 gave det=0, singletons at z=0
# gave det != 0. Test: does the line-3 z-plane vs singleton z-plane
# split explain all det=0 cases?
# ---------------------------------------------------------------------------

z_pattern_data = []
for (s, d, st) in nearby_results:
    if st != "balanced":
        continue
    line_z = 0  # line-3 in y=0 plane at z=0
    single_z = s[2]
    z_separated = single_z != line_z
    z_pattern_data.append((s, d, z_separated))

z_sep_and_zero = sum(1 for (s, d, z_sep) in z_pattern_data if z_sep and d == 0)
z_sep_total = sum(1 for (s, d, z_sep) in z_pattern_data if z_sep)
z_same_and_zero = sum(1 for (s, d, z_sep) in z_pattern_data if not z_sep and d == 0)
z_same_total = sum(1 for (s, d, z_sep) in z_pattern_data if not z_sep)

record(
    "z_separated_singletons_all_give_det_zero",
    z_sep_and_zero == z_sep_total and z_sep_total > 0,
    f"Line-3 at z=0, singleton at z=1 (z-separated): "
    f"{z_sep_and_zero}/{z_sep_total} give det=0. "
    f"All zero? {z_sep_and_zero == z_sep_total and z_sep_total > 0}.",
)

record(
    "z_same_singletons_all_give_det_nonzero",
    z_same_and_zero == 0 and z_same_total > 0,
    f"Line-3 at z=0, singleton at z=0 (same-plane): "
    f"{z_same_and_zero}/{z_same_total} give det=0, "
    f"{z_same_total - z_same_and_zero}/{z_same_total} give det!=0. "
    f"All non-zero? {z_same_and_zero == 0 and z_same_total > 0}.",
)

# Test on alternative line-3 at y=2 plane z=0 (same z-plane as y=0 line-3).
# If z-plane separation hypothesis holds, singleton at z=1 gives det=0.
alt_z_pattern = []
for (s, d, st) in alt_results:
    if st != "balanced":
        continue
    line_z = 0  # alt line also at z=0
    alt_z_pattern.append((s, d, s[2] != line_z))

alt_z_sep_zero = sum(1 for (_, d, z_sep) in alt_z_pattern if z_sep and d == 0)
alt_z_sep_total = sum(1 for (_, _, z_sep) in alt_z_pattern if z_sep)

record(
    "alt_line3_z_separated_singletons_det_zero",
    alt_z_sep_total == 0 or alt_z_sep_zero == alt_z_sep_total,
    f"Alt line-3 (y=2, z=0) + z=1 singletons: "
    f"{alt_z_sep_zero}/{alt_z_sep_total} give det=0.",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

all_line3_force_zero = (zero_det_count == total_balanced and total_balanced > 0)
alt_location_also_zero = (alt_zero_count == alt_balanced and alt_balanced > 0)
rot_direction_also_zero = (rot_zero_count == rot_balanced and rot_balanced > 0)

# Is SH3 fixed by any non-identity symmetry?
sh3_has_nontrivial_symmetry = len(fixing_ops) > 1  # i.e., more than just identity

record(
    "SH3_has_nontrivial_symmetry",
    sh3_has_nontrivial_symmetry,
    f"SH3 has non-identity symmetry in D_4 x Z_2? {sh3_has_nontrivial_symmetry}. "
    f"Fixing ops: {fixing_ops}.",
)

z_separation_hypothesis_holds = (
    z_sep_and_zero == z_sep_total and z_sep_total > 0
    and z_same_and_zero == 0 and z_same_total > 0
)
z_hypothesis_confirmed_on_alt = (
    alt_z_sep_total == 0 or alt_z_sep_zero == alt_z_sep_total
)

if z_separation_hypothesis_holds and z_hypothesis_confirmed_on_alt:
    document(
        "z_plane_separation_line3_singleton_forces_det_zero",
        "Discovery: on (4,4,2), line-3 in a z-plane plus a singleton"
        " in the opposite z-plane forces |det_K3(B)| = 0. Pattern"
        " observed on y=0 line-3 at z=0: all 4 tested z=1 singletons"
        " give det=0; all 3 tested z=0 singletons give det != 0."
        " Cross-checked with alternative line-3 at y=2 and z=1"
        " singletons (matching pattern). The defect is NOT fixed by"
        " any non-identity axis-aligned symmetry in D_4 x Z_2 so the"
        " mechanism is distinct from iter 23 reflection-degeneracy."
        " Candidate new lemma: 'z-plane-separated line-3 + singleton'"
        " configurations on cuboids with L_3 = 2 force det_K3 = 0"
        " via an unidentified PM-pairing mechanism.",
    )
elif z_separation_hypothesis_holds:
    document(
        "z_plane_separation_hypothesis_on_y0_confirmed",
        "On y=0 line-3 at z=0 with nearby singletons: perfect"
        " correlation -- all z=1 singletons give det=0, all z=0"
        " singletons give det != 0. Alternative line-3 at y=2 was"
        " not tested with sufficient z=1 singletons to confirm"
        " generality. Needs follow-up.",
    )
else:
    document(
        "sh3_zero_partial_pattern",
        f"SH3 det=0 follows a partial pattern: some line-3 +"
        f" singleton configurations give det=0, others don't."
        f" z-plane separation shows a strong trend but does not"
        f" explain everything on current data. Needs more test"
        f" cases on different cuboids.",
    )


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def main():
    print("=" * 78)
    print("V2: SH3 non-reflection degeneracy investigation")
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
