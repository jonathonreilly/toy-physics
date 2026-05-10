#!/usr/bin/env python3
"""2D mirror operator-Cauchy continuum-bridge probe.

Companion experiment to the rescaled NN lane (existence PR #957,
identification PR #968, kernel PRs #1003 / #1007 / #1055, parameter
universality #1054, NNLO residual #1056) and to the alt-connectivity grown
DAG family null-result (PR #1008).

Question
--------

Does the operator-Cauchy continuum-bridge method extend from the rescaled
NN harness to the exact 2D mirror harness retained in
``scripts/mirror_2d_validation.py`` (``gen_2d_mirror``)?

Harness structure
-----------------

The 2D mirror harness ``gen_2d_mirror(nl, npl_half, yr, cr, seed)``:

- adds layers x = 0 .. nl-1 along the propagation axis
- each non-source layer carries 2 * npl_half random nodes mirrored across
  y = 0 with random ordinates in [0.5, yr]
- one chokepoint layer at ``bl = nl // 3`` reverts to single-layer
  connectivity; every other layer carries two-layer connectivity
- connect radius ``cr`` is fixed in physical units; the layer spacing along
  x is unit; ``yr`` is fixed transverse extent

Refinement-axis decision
------------------------

Unlike the rescaled NN harness (h -> 0), the 2D mirror has no per-edge
lattice-spacing knob. The natural lattice-resolution analog is N (number of
layers). The transverse extent ``yr`` and intra-layer density ``npl_half``
remain fixed, so increasing N adds layers at fixed physical density.

If a continuum T_inf exists for this harness, then the 5-dim observable
vector
    vec(N) := [ MI(N), 1-pur(N), d_TV(N), gravity(N), Born(N) ]
(each entry seed-averaged) should be Cauchy in N: pairwise increments
``||vec(N_i) - vec(N_{i+1})||_2`` should decay as a power of N with R^2 high
on a log-log fit.

If the gravity-side weakness reported in MIRROR_2D_GRAVITY_LAW_NOTE
(``R^2 = 0.015 / 0.167 / 0.075`` on scaling, mass window, distance tail)
is a finite-N artifact, the Cauchy gate should still pass on the smoother
observables.

If non-monotonicity is structural (chokepoint-driven multi-saddle
interference, mirror parity, etc.), the Cauchy gate fails and we document
the structural mechanism.

Refinement grid
---------------

N in {25, 40, 60, 80, 100, 150, 200}. The first five match
MIRROR_2D_GRAVITY_LAW_NOTE; 150 and 200 extend the lane (timing test for a
single seed: N=150 ~1.4 s, N=200 ~1.9 s; full sweep at 8 seeds completes in
a couple of minutes).

Observable basis
----------------

Five framework observables, mirroring the structure already reported by
``scripts/mirror_2d_validation.py``:

    obs_0 = MI            (slit-detector mutual information, bits)
    obs_1 = decoh         (1 - pur_min)
    obs_2 = dTV           (total-variation between branch outcome dists)
    obs_3 = gravity       (signed Born-weighted centroid shift under mass)
    obs_4 = born          (Sorkin three-slit |I3| / P)

The vector is 5-dim (a single source / detector configuration per N) and
seed-averaged over 8 seeds matching the mirror_2d_validation default. We
also record per-component pairwise increments to diagnose which
observables (if any) are Cauchy in N when the joint vector is not.

Guards
------

- monotonicity flag: per-component, we check whether the seed-mean is
  monotone in N. The MIRROR_2D_GRAVITY_LAW_NOTE evidence shows MI peaks at
  N=60; this is the bounded mechanism we are probing.
- Born guard: all rows should remain at the linear-propagator floor
  (~1e-15); a non-floor row would invalidate the harness.

Cost: ~2 minutes for 8 seeds x 7 N values.

Verdict
-------

The runner reports:

- joint Cauchy fit (r and R^2 on ||vec(N) - vec(N')||_2 vs N_geom)
- per-component Cauchy fits
- per-component monotonicity in N

and decides:

  PASS  (Cauchy)        : r < -0.4 AND R^2 >= 0.85 on the 5-dim joint
  PARTIAL (mixed)       : some components Cauchy, others not
  NULL  (no continuum)  : joint fit fails, components non-monotone

Honest non-monotonicity is the expected outcome given the existing
weak-R^2 gravity-law fits; this runner converts that empirical observation
into a structural diagnosis.
"""

from __future__ import annotations


# Heavy compute / sweep runner -- AUDIT_TIMEOUT_SEC mirrors the convention
# from alt_connectivity_family_operator_cauchy.py.
AUDIT_TIMEOUT_SEC = 1800

import math
import os
import sys
import time
from typing import Dict, List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.mirror_2d_validation import measure_family  # noqa: E402


# Refinement axis: layer count N; geometric-ish grid.
# {25, 40, 60, 80, 100} reproduces the existing primary-runner sweep.
# {150, 200} extends the lane to probe whether the non-monotonicity
# observed at N <= 100 damps at larger N.
N_GRID: List[int] = [25, 40, 60, 80, 100, 150, 200]

# Fixed harness knobs (matching scripts/mirror_2d_validation.py defaults)
NPL_HALF: int = 12
YR: float = 10.0
CONNECT_RADIUS: float = 2.5
N_SEEDS: int = 8
K_BAND: List[float] = [3.0, 5.0, 7.0]

# Observable basis: 5 framework observables per N.
OBSERVABLES: List[str] = ["MI", "decoh", "dTV", "gravity", "born"]


def mean(vals: List[float]) -> float:
    clean = [v for v in vals if v is not None and not math.isnan(v)]
    if not clean:
        return math.nan
    return sum(clean) / len(clean)


def safe_power_fit(xs: List[float],
                   ys: List[float]) -> Tuple[float, float, float]:
    pts = [(x, abs(y)) for x, y in zip(xs, ys)
           if x > 0 and abs(y) > 0 and not math.isnan(y)]
    if len(pts) < 2:
        return math.nan, math.nan, math.nan
    lx = [math.log(x) for x, _ in pts]
    ly = [math.log(y) for _, y in pts]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    denom = sum((x - mx) ** 2 for x in lx)
    if denom <= 0:
        return math.nan, math.nan, math.nan
    slope = sum((x - mx) * (y - my) for x, y in zip(lx, ly)) / denom
    intercept = my - slope * mx
    ss_tot = sum((y - my) ** 2 for y in ly)
    ss_res = sum(
        (y - (slope * x + intercept)) ** 2 for x, y in zip(lx, ly)
    )
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else math.nan
    return slope, math.exp(intercept), r2


def l2_diff(a: List[float], b: List[float]) -> float:
    s = 0.0
    n = 0
    for ai, bi in zip(a, b):
        if math.isnan(ai) or math.isnan(bi):
            continue
        s += (ai - bi) ** 2
        n += 1
    if n == 0:
        return math.nan
    return math.sqrt(s)


def monotonicity(vals: List[float]) -> str:
    """Return 'inc', 'dec', 'non-mono', or 'undef'."""
    clean = [v for v in vals if v is not None and not math.isnan(v)]
    if len(clean) < 3:
        return "undef"
    diffs = [clean[i + 1] - clean[i] for i in range(len(clean) - 1)]
    if all(d >= -1e-9 for d in diffs):
        return "inc"
    if all(d <= 1e-9 for d in diffs):
        return "dec"
    return "non-mono"


def main() -> int:
    t0 = time.time()
    print("=" * 110)
    print("2D MIRROR OPERATOR-CAUCHY CONTINUUM-BRIDGE PROBE")
    print(f"  harness: gen_2d_mirror(nl, npl_half={NPL_HALF}, "
          f"yr={YR}, cr={CONNECT_RADIUS}, seed)")
    print(f"  refinement axis: layer count N in {N_GRID}")
    print(f"  observables: {OBSERVABLES}")
    print(f"  seeds: {N_SEEDS}  (matches mirror_2d_validation default)")
    print(f"  k-band: {K_BAND}")
    print("=" * 110)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    # per_N["MI"][N] = list of seed-level values
    per_N: Dict[str, Dict[int, List[float]]] = {
        o: {n: [] for n in N_GRID} for o in OBSERVABLES
    }
    n_ok_per_N: Dict[int, int] = {n: 0 for n in N_GRID}
    born_max = 0.0

    print(f"  {'N':>4s}  {'seed':>4s}  {'MI':>9s}  {'1-pur':>8s}  "
          f"{'d_TV':>8s}  {'gravity':>10s}  {'born':>10s}  {'dt':>5s}")
    print("  " + "-" * 80)
    for nl in N_GRID:
        for seed in seeds:
            ts = time.time()
            row = measure_family(
                n_layers=nl,
                npl_half=NPL_HALF,
                yr=YR,
                connect_radius=CONNECT_RADIUS,
                seed=seed,
                family="mirror",
                k_band=K_BAND,
            )
            dt = time.time() - ts
            if row is None:
                print(f"  {nl:4d}  {seed:4d}  {'FAIL':>9s}  "
                      f"{'-':>8s}  {'-':>8s}  {'-':>10s}  "
                      f"{'-':>10s}  {dt:4.1f}s")
                continue
            per_N["MI"][nl].append(row["MI"])
            per_N["decoh"][nl].append(1.0 - row["pur_min"])
            per_N["dTV"][nl].append(row["dTV"])
            per_N["gravity"][nl].append(row["gravity"])
            per_N["born"][nl].append(row["born"])
            n_ok_per_N[nl] += 1
            born_max = max(born_max, abs(row["born"])
                           if not math.isnan(row["born"]) else 0.0)
            print(f"  {nl:4d}  {seed:4d}  {row['MI']:9.6f}  "
                  f"{1.0 - row['pur_min']:8.4f}  {row['dTV']:8.4f}  "
                  f"{row['gravity']:+10.4f}  {row['born']:10.2e}  "
                  f"{dt:4.1f}s")

    print()
    print(f"  total measurement wallclock: {time.time() - t0:.0f}s")
    print()

    # --- Guards ---
    print("=" * 110)
    print("GUARDS")
    print("=" * 110)
    born_ok = born_max < 1e-10
    print(f"  Born floor (max |I3|/P): {born_max:.2e}  "
          f"{'PASS' if born_ok else 'FAIL'}  (linear-propagator floor "
          f"expected ~1e-15)")
    for nl in N_GRID:
        print(f"  n_ok at N={nl}: {n_ok_per_N[nl]}/{N_SEEDS}")
    if min(n_ok_per_N.values()) < 3:
        print("  WARN: some N have fewer than 3 surviving seeds; their "
              "Cauchy entries are noisy.")
    print()

    # --- Build seed-mean vec(N) ---
    print("=" * 110)
    print("SEED-MEAN OBSERVABLE TABLE")
    print("=" * 110)
    print(f"  {'N':>4s}  " + "  ".join([f"{o:>10s}" for o in OBSERVABLES]))
    print("  " + "-" * (6 + len(OBSERVABLES) * 12))
    vecs: Dict[int, List[float]] = {}
    for nl in N_GRID:
        v: List[float] = []
        for o in OBSERVABLES:
            v.append(mean(per_N[o][nl]))
        vecs[nl] = v
        print(f"  {nl:4d}  " + "  ".join([f"{x:+10.4e}" for x in v]))
    print()

    # --- Per-component monotonicity ---
    print("=" * 110)
    print("PER-COMPONENT MONOTONICITY IN N")
    print("=" * 110)
    print(f"  {'observable':>10s}  {'monotonicity':>14s}  "
          f"{'min':>12s}  {'max':>12s}  {'first':>12s}  {'last':>12s}")
    component_mono: Dict[str, str] = {}
    for o in OBSERVABLES:
        vals = [vecs[nl][OBSERVABLES.index(o)] for nl in N_GRID]
        m = monotonicity(vals)
        component_mono[o] = m
        clean = [v for v in vals if not math.isnan(v)]
        if clean:
            print(f"  {o:>10s}  {m:>14s}  {min(clean):+12.4e}  "
                  f"{max(clean):+12.4e}  {clean[0]:+12.4e}  "
                  f"{clean[-1]:+12.4e}")
        else:
            print(f"  {o:>10s}  {m:>14s}  {'-':>12s}  "
                  f"{'-':>12s}  {'-':>12s}  {'-':>12s}")
    print()

    # --- Joint operator-Cauchy on the 5-dim vector ---
    print("=" * 110)
    print("JOINT OPERATOR-CAUCHY ON THE 5-DIM OBSERVABLE VECTOR")
    print(f"  ||vec(N_i) - vec(N_{{i+1}})||_2 across consecutive N in "
          f"the grid, fit vs sqrt(N_i * N_{{i+1}})")
    print("=" * 110)
    print()

    pairs = [(N_GRID[i], N_GRID[i + 1]) for i in range(len(N_GRID) - 1)]
    rows: List[Tuple[int, int, float]] = []
    xs: List[float] = []
    ys: List[float] = []
    print(f"  {'N1':>4s} -> {'N2':>4s}   "
          f"{'||vec(N1) - vec(N2)||_2':>26s}")
    for (N1, N2) in pairs:
        d = l2_diff(vecs[N1], vecs[N2])
        rows.append((N1, N2, d))
        print(f"  {N1:>4d} -> {N2:>4d}   {d:26.6e}")
        if d > 0 and not math.isnan(d):
            xs.append(math.sqrt(N1 * N2))
            ys.append(d)
    r, C, r2 = safe_power_fit(xs, ys)
    print()
    print(f"  Fit on {len(xs)} pts: "
          f"||vec(N_i) - vec(N_{{i+1}})||_2 ~ C * N^r")
    print(f"    r   = {r:+.4f}")
    print(f"    C   = {C:.4e}")
    print(f"    R^2 = {r2:.4f}")
    joint_cauchy_ok = (
        not math.isnan(r) and r < -0.4
        and not math.isnan(r2) and r2 >= 0.85
    )
    print(f"    GATE r < -0.4 AND R^2 >= 0.85: "
          f"{'PASS' if joint_cauchy_ok else 'FAIL'}")
    print()

    # --- Per-component Cauchy fits ---
    print("=" * 110)
    print("PER-COMPONENT CAUCHY DECAY RATES (seed-mean increments)")
    print("=" * 110)
    print(f"  {'observable':>10s}  {'r':>9s}  {'C':>10s}  "
          f"{'R^2':>8s}  {'Cauchy?':>9s}")
    per_comp_cauchy: Dict[str, bool] = {}
    for o in OBSERVABLES:
        oi = OBSERVABLES.index(o)
        xs_c: List[float] = []
        ys_c: List[float] = []
        for (N1, N2) in pairs:
            a = vecs[N1][oi]
            b = vecs[N2][oi]
            if math.isnan(a) or math.isnan(b):
                continue
            delta = abs(b - a)
            if delta > 0:
                xs_c.append(math.sqrt(N1 * N2))
                ys_c.append(delta)
        if len(xs_c) >= 2:
            rc, Cc, r2c = safe_power_fit(xs_c, ys_c)
            ok = (not math.isnan(rc) and rc < -0.4
                  and not math.isnan(r2c) and r2c >= 0.85)
            per_comp_cauchy[o] = ok
            print(f"  {o:>10s}  {rc:+9.4f}  {Cc:10.4e}  {r2c:8.4f}  "
                  f"{'PASS' if ok else 'FAIL':>9s}")
        else:
            per_comp_cauchy[o] = False
            print(f"  {o:>10s}  {'-':>9s}  {'-':>10s}  {'-':>8s}  "
                  f"{'FAIL':>9s}")
    print()

    # --- Identification stub (only if joint passes) ---
    if joint_cauchy_ok:
        print("=" * 110)
        print("IDENTIFICATION STUB")
        print("=" * 110)
        if not math.isnan(r):
            cl_half_dist = abs(r - (-0.5))
            cl_one_dist = abs(r - (-1.0))
            if cl_half_dist < 0.12:
                print(f"  decay rate r = {r:+.4f} consistent with the "
                      f"CLT prediction r = -1/2 (distance {cl_half_dist:.3f})")
                print("  identification candidate: ensemble-mean of "
                      "i.i.d. seed-realizations satisfies a CLT-style "
                      "law on the 5-dim observable vector")
            elif cl_one_dist < 0.20:
                print(f"  decay rate r = {r:+.4f} closer to a "
                      f"deterministic 1/N scaling (distance {cl_one_dist:.3f})")
                print("  identification candidate: deterministic O(1/N) "
                      "discretization error in the 5-dim observable")
            else:
                print(f"  decay rate r = {r:+.4f} does not match a "
                      f"standard CLT (-1/2) or O(1/N) scaling")
                print("  identification deferred to follow-up: the "
                      "harness Cauchy-converges but the limiting structure "
                      "is non-canonical on this 5-dim basis.")
        print()

    # --- Verdict ---
    print("=" * 110)
    print("VERDICT")
    print("=" * 110)
    n_comp_pass = sum(1 for ok in per_comp_cauchy.values() if ok)
    n_non_mono = sum(1 for m in component_mono.values() if m == "non-mono")
    if joint_cauchy_ok:
        verdict = "POSITIVE"
        print(f"  POSITIVE: the 2D mirror harness ADMITS an "
              f"operator-Cauchy continuum bridge")
        print(f"    on the layer-count refinement axis N -> infinity.")
        print(f"    Joint fit: r = {r:+.4f}, R^2 = {r2:.4f}")
        print(f"    Components that pass Cauchy gate: {n_comp_pass}/"
              f"{len(OBSERVABLES)}")
        print()
        print("  This contradicts the preliminary dismissal in "
              "MIRROR_2D_GRAVITY_LAW_NOTE based on weak gravity-law fits;")
        print("  the operator-Cauchy probe is structural rather than "
              "law-fit-dependent.")
    elif n_comp_pass > 0:
        verdict = "PARTIAL"
        non_mono_list = ", ".join(
            o for o, m in component_mono.items() if m == "non-mono"
        )
        print(f"  PARTIAL: {n_comp_pass}/{len(OBSERVABLES)} components "
              f"admit a Cauchy fit, but the joint 5-dim vector does not.")
        print(f"    Joint fit: r = {r:+.4f}, R^2 = {r2:.4f}")
        print(f"    Non-monotone components: {n_non_mono}/"
              f"{len(OBSERVABLES)} ({non_mono_list})")
        print()
        print("  The 2D mirror harness has a partial continuum bridge "
              "on a subspace of the 5-dim observable basis.")
        print("  The non-Cauchy components carry the bounded "
              "non-monotonicity reported in MIRROR_2D_GRAVITY_LAW_NOTE.")
    else:
        verdict = "NULL"
        print("  SHARP BOUNDED NULL: the 2D mirror harness does NOT admit "
              "a clean operator-Cauchy continuum bridge")
        print("  on the layer-count refinement axis.")
        non_mono_list = ", ".join(
            o for o, m in component_mono.items() if m == "non-mono"
        )
        print(f"    Joint fit: r = {r:+.4f}, R^2 = {r2:.4f}  FAIL")
        print(f"    Components that pass Cauchy gate: {n_comp_pass}/"
              f"{len(OBSERVABLES)} (none)")
        print(f"    Non-monotone components: {n_non_mono}/"
              f"{len(OBSERVABLES)} ({non_mono_list})")
        print()
        print("  Structural reason:")
        print("    - the 2D mirror harness has no spacing-refinement "
              "knob; N adds layers at FIXED physical density")
        print("      (npl_half and yr are held constant)")
        print("    - the chokepoint at layer N // 3 reverts the "
              "connectivity for exactly one layer; as N grows, the "
              "chokepoint's relative location stays at 1/3 but its")
        print("      absolute layer index changes, so the path-integral "
              "saddles around it do not have a fixed continuum target")
        print("    - the upstream / downstream subgraph sizes "
              "(barrier_layer = N // 3, gravity_layer = 2N // 3) move "
              "with N, so observables sample different geometric")
        print("      configurations at each N rather than refining a "
              "single one")
        print("    - this is structurally distinct from the rescaled NN "
              "harness, which keeps the physical domain fixed and "
              "refines edge spacing h")
        print("    - the bounded null in MIRROR_2D_GRAVITY_LAW_NOTE "
              "(weak gravity-side R^2) is now explained: it is a "
              "consequence of the harness not refining a single")
        print("      physical configuration but rather walking through "
              "a family of configurations indexed by N")
    print()

    # --- Reconciliation with MIRROR_2D_GRAVITY_LAW_NOTE ---
    print("=" * 110)
    print("RECONCILIATION WITH MIRROR_2D_GRAVITY_LAW_NOTE")
    print("=" * 110)
    print("  MIRROR_2D_GRAVITY_LAW_NOTE reports primary-runner fits on the")
    print("  same harness (N in {25, 40, 60, 80, 100}):")
    print("    gravity scaling      R^2 = 0.015")
    print("    mass window          R^2 = 0.167")
    print("    distance tail        R^2 = 0.075")
    print()
    print("  This operator-Cauchy probe extends the lane to N=150 and 200")
    print(f"  and tests whether the bounded null narrows. Result: {verdict}.")
    print()

    print(f"  Total wallclock: {time.time() - t0:.0f}s")
    print()

    # Exit code: pass when guard checks succeed regardless of Cauchy
    # outcome. A NULL verdict is a valid scientific outcome; what we
    # cannot tolerate is a Born-floor violation or a complete data drop.
    if not born_ok:
        return 1
    if sum(n_ok_per_N.values()) < N_SEEDS * len(N_GRID) // 2:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
