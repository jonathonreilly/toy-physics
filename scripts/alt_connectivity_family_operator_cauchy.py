#!/usr/bin/env python3
"""ALT-connectivity grown DAG family operator-Cauchy continuum-bridge probe.

Companion experiment to the rescaled NN lane context. The question this
runner attacks:

  Does the operator-Cauchy continuum-bridge method extend from the rescaled
  NN harness to the alt-connectivity grown DAG family?

Harness structure (per
`docs/ALT_CONNECTIVITY_FAMILY_{BASIN,FAILURE}_NOTE.md`):

- Geometry: `grow(drift, seed)` from `gate_b_no_restore_farfield`
  - drift in [0.0, 0.5] is the per-layer Gaussian-jitter scale
  - seed is the RNG seed; controls per-seed DAG realization
  - lattice spacing H = 0.5 is HARDCODED at module scope; not a free knob in
    this harness
- Connectivity: parity-rotated sector-transition rule from
  `ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP._build_alt_connectivity` on top of the
  grown DAG
- Observable: signed centroid shift of the detector-layer amplitude under
  point-charge sources (gravity-style response)

Refinement-axis decision
------------------------

The rescaled NN harness uses lattice spacing h -> 0 as the natural refinement
parameter. The alt-connectivity grown DAG family has NO clean h-like
refinement knob:

- H is hardcoded at module scope (refining it would require rebuilding the
  grow function, which the harness does not export)
- drift -> 0 is the regular-grid limit, which is a degenerate harness point
  (the construction is intrinsically stochastic; drift=0 is a separate
  family)
- generation/layer index NL is not a refinement axis in the usual sense
- there is no PDE limit lurking under this construction

What the harness DOES have is a stochastic ensemble over seed.  For fixed
drift > 0 the ensemble-mean observable should converge as the ensemble size
N -> infinity if the harness has any continuum limit at all.

We therefore adapt operator-Cauchy from spacing-refinement to
ensemble-refinement:

  vec(N; drift)_{obs, y_m} := (1/N) sum_{seed=0}^{N-1}
      obs(seed, drift, y_m)

with N geometric in {2, 4, 8, 16, 32, 64}.  If
||vec(N) - vec(2N)||_2 ~ C * N^r with r < -0.4 and R^2 >= 0.85, the ensemble
expectation E[obs] has candidate numerical support on this harness. If that
gate fails (e.g., non-monotonic seed-mean drift, oscillation, divergence), the
harness has a sharp bounded null-result for this adapted test and we identify
the bounded mechanism.

Observable basis (mirrors the rescaled NN 5-vector philosophy, adapted to this
harness's natural observable set):

  - plus       : signed centroid shift under a +1 point source
  - minus      : signed centroid shift under a -1 point source
  - neutral    : |centroid shift under cancelling +/- pair|
  - double     : signed centroid shift under a +2 source
  - exponent   : log2(double/plus); weak-charge scaling exponent

Source-position basis: three independent source z values
{SOURCE_Z_LOW, SOURCE_Z_MID, SOURCE_Z_HIGH}. Together that is a 15-dim
observable vector independent of N, matching the rescaled NN comparison basis.

Guards
------

- zero-source baseline at every (seed, drift): exact (<1e-12) at drift=0,
  finite-but-bounded for drift>0 (the harness construction guarantees
  zero-source = 0 exactly for any seed; we report max |zero| as a sanity
  check)
- neutral cancellation residual is reported and goes into the Cauchy vector
  as one of the observables; it is its own diagnostic
- a basin-membership flag is recorded per seed (zero=0, neutral=0, plus>0,
  minus<0, |exponent-1|<0.05) so we can stratify Cauchy-on-basin vs
  Cauchy-on-all-seeds

Drift point: 0.10 (mid-basin, comparatively stable per the basin note's
"zero-drift and mid-drift rows are especially stable" finding).

Exit code is nonzero if the zero-source baseline leaks or if this no-go runner
unexpectedly finds a passing ensemble-Cauchy fit.

Cost: each (drift, seed) pair is ~4-5 s on this lattice (NL=25, H=0.5,
PW=8).  With N=64 max and 3 source positions = 64*3 ~ 192 measurements
shared across mass positions per seed; ~13 min wallclock total.
"""

from __future__ import annotations


# Heavy compute / sweep runner -- `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
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

from ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP import (  # noqa: E402
    Family,
    _build_alt_connectivity,
    _centroid_z,
    _field_from_sources,
    _propagate,
)
from gate_b_no_restore_farfield import grow  # noqa: E402


# Refinement axis: ensemble size, geometric grid
N_GRID: List[int] = [2, 4, 8, 16, 32, 64]
DRIFT: float = 0.10  # mid-basin per ALT_CONNECTIVITY_FAMILY_BASIN_NOTE

# Source-position basis: three z positions for the 15-component comparison vector
SOURCE_Z_GRID: List[float] = [2.0, 3.0, 4.0]

# Observable basis: 5 framework observables per source position
OBSERVABLES: List[str] = ["plus", "minus", "neutral", "double", "exponent"]

# Basin gate per the existing harness convention
ZERO_TOL = 1e-12
NEUTRAL_TOL = 1e-12
EXP_TOL = 0.05


def measure_seed(drift: float, seed: int,
                 source_z_grid: List[float]) -> Dict:
    """Measure the 5-vector at each source-z for a single (drift, seed).

    Returns a dict with per-source-z observables plus a max(|zero|) guard.
    """
    pos, adj, layers, _ = grow(drift, seed)
    fam = Family(pos, layers, adj)
    alt = _build_alt_connectivity(fam)
    det = alt.layers[-1]
    free = _propagate(alt.positions, alt.adj, [0.0] * len(alt.positions))
    z_free = _centroid_z(free, alt.positions, det)
    out = {"zero_guard_max": 0.0, "per_z": {}}
    for source_z in source_z_grid:

        def run(charge: int) -> float:
            field = _field_from_sources(
                alt.positions, alt.layers, [(source_z, charge)]
            )
            amps = _propagate(alt.positions, alt.adj, field)
            return _centroid_z(amps, alt.positions, det) - z_free

        # Per-harness convention: the zero-charge response should be 0 exactly.
        zero = run(0)
        plus = run(+1)
        minus = run(-1)
        # Neutral cancellation residual
        field_pm = _field_from_sources(
            alt.positions, alt.layers,
            [(source_z, +1), (source_z, -1)],
        )
        amps_pm = _propagate(alt.positions, alt.adj, field_pm)
        neutral_signed = (
            _centroid_z(amps_pm, alt.positions, det) - z_free
        )
        neutral = abs(neutral_signed)
        double = run(+2)
        if abs(plus) > 1e-30 and abs(double) > 1e-30:
            exponent = math.log(abs(double / plus)) / math.log(2.0)
        else:
            exponent = math.nan

        ok_basin = (
            abs(zero) < ZERO_TOL
            and neutral < NEUTRAL_TOL
            and plus > 0.0
            and minus < 0.0
            and not math.isnan(exponent)
            and abs(exponent - 1.0) < EXP_TOL
        )

        out["per_z"][source_z] = {
            "zero": zero,
            "plus": plus,
            "minus": minus,
            "neutral": neutral,
            "double": double,
            "exponent": exponent,
            "ok_basin": ok_basin,
        }
        out["zero_guard_max"] = max(out["zero_guard_max"], abs(zero))

    return out


def ensemble_vector(per_seed: List[Dict],
                    on_basin_only: bool) -> List[float]:
    """Build the 15-dim observable vector from a seed ensemble.

    Components are ordered as [obs_0 @ z_0, obs_0 @ z_1, ..., obs_4 @ z_2].
    On-basin filtering keeps only seeds whose row passes the basin gate at
    that source_z; entries with no surviving seeds are NaN.
    """
    vec: List[float] = []
    for obs in OBSERVABLES:
        for source_z in SOURCE_Z_GRID:
            vals: List[float] = []
            for sd in per_seed:
                cell = sd["per_z"][source_z]
                if on_basin_only and not cell["ok_basin"]:
                    continue
                v = cell[obs]
                if v is not None and not math.isnan(v):
                    vals.append(v)
            vec.append(sum(vals) / len(vals) if vals else math.nan)
    return vec


def l2_diff(a: List[float], b: List[float]) -> float:
    s = 0.0
    for ai, bi in zip(a, b):
        if math.isnan(ai) or math.isnan(bi):
            continue
        s += (ai - bi) ** 2
    return math.sqrt(s)


def safe_power_fit(xs: List[float],
                   ys: List[float]) -> Tuple[float, float, float]:
    pts = [(x, abs(y)) for x, y in zip(xs, ys) if x > 0 and abs(y) > 0]
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


def main() -> int:
    t0 = time.time()
    print("=" * 110)
    print("ALT-CONNECTIVITY GROWN DAG FAMILY OPERATOR-CAUCHY PROBE")
    print(f"  drift fixed at {DRIFT} (mid-basin per BASIN_NOTE)")
    print(f"  refinement axis: ensemble size N in {N_GRID}")
    print(f"  source-position basis: source_z in {SOURCE_Z_GRID}")
    print(f"  observable basis: {OBSERVABLES}")
    print(f"  vector dimension: {len(OBSERVABLES)} x {len(SOURCE_Z_GRID)} "
          f"= {len(OBSERVABLES) * len(SOURCE_Z_GRID)}")
    print("=" * 110)
    print()

    n_max = max(N_GRID)
    per_seed: List[Dict] = []
    zero_max = 0.0
    n_basin_per_z: Dict[float, int] = {z: 0 for z in SOURCE_Z_GRID}

    print(f"  {'seed':>5s}  "
          + "  ".join([f"plus@z={z:.0f}" for z in SOURCE_Z_GRID])
          + f"  {'zero_max':>10s}  {'basin_z@2/3/4':>14s}  {'dt':>6s}")
    print("  " + "-" * 100)

    for seed in range(n_max):
        ts = time.time()
        m = measure_seed(DRIFT, seed, SOURCE_Z_GRID)
        per_seed.append(m)
        zero_max = max(zero_max, m["zero_guard_max"])
        basin_flags = []
        for z in SOURCE_Z_GRID:
            cell = m["per_z"][z]
            if cell["ok_basin"]:
                n_basin_per_z[z] += 1
                basin_flags.append("Y")
            else:
                basin_flags.append("n")
        plus_strs = "  ".join(
            [f"{m['per_z'][z]['plus']:+10.3e}" for z in SOURCE_Z_GRID]
        )
        dt = time.time() - ts
        print(f"  {seed:>5d}  {plus_strs}  {m['zero_guard_max']:10.2e}  "
              f"   {'/'.join(basin_flags):>10s}    {dt:5.1f}s")

    print()
    print(f"  total measurement time: {time.time() - t0:.0f}s")
    print()

    # --- Guards ---
    print("=" * 110)
    print("GUARDS")
    print("=" * 110)
    zero_ok = zero_max < ZERO_TOL
    print(f"  zero-source baseline (max |zero| across all seeds, "
          f"source_z): {zero_max:.2e}  "
          f"{'PASS' if zero_ok else 'FAIL'}")
    for z in SOURCE_Z_GRID:
        print(f"  basin membership at source_z = {z}: "
              f"{n_basin_per_z[z]}/{n_max} seeds  "
              f"(per ALT_CONNECTIVITY_FAMILY_BASIN_NOTE, seed-selective)")
    print()

    # --- Ensemble Cauchy: all-seeds ---
    print("=" * 110)
    print("ENSEMBLE-CAUCHY (ALL SEEDS)")
    print(f"  vec(N) := ensemble mean over seeds 0..N-1; "
          f"||vec(N) - vec(2N)||_2 ~ C * N^r")
    print("=" * 110)
    print()

    all_pairs = [(N_GRID[i], N_GRID[i + 1])
                 for i in range(len(N_GRID) - 1)]

    def cauchy_curve(on_basin_only: bool
                     ) -> Tuple[List[Tuple[int, int, float]], List[float],
                                List[float]]:
        rows = []
        xs = []
        ys = []
        for N1, N2 in all_pairs:
            v1 = ensemble_vector(per_seed[:N1], on_basin_only)
            v2 = ensemble_vector(per_seed[:N2], on_basin_only)
            l2 = l2_diff(v1, v2)
            rows.append((N1, N2, l2))
            N_geom = math.sqrt(N1 * N2)
            if l2 > 0 and not math.isnan(l2):
                xs.append(N_geom)
                ys.append(l2)
        return rows, xs, ys

    rows, xs, ys = cauchy_curve(on_basin_only=False)
    print(f"  {'N1':>5s} -> {'N2':>5s}   {'||vec(N1) - vec(N2)||_2':>26s}")
    for N1, N2, l2 in rows:
        print(f"  {N1:>5d} -> {N2:>5d}   {l2:26.6e}")
    r, C, r2 = safe_power_fit(xs, ys)
    print()
    print(f"  Fit on {len(xs)} pts: "
          f"||vec(N) - vec(2N)||_2 ~ C * N^r")
    print(f"    r   = {r:+.4f}  (Cauchy if r < -0.4)")
    print(f"    C   = {C:.4e}")
    print(f"    R^2 = {r2:.4f}")

    # Cauchy on the ensemble axis: r should be negative.  CLT predicts
    # r = -1/2; we require r < -0.4 with R^2 >= 0.85 as a Cauchy-on-ensemble
    # gate because ensemble
    # variance dominates the increment at small N).
    all_cauchy_ok = (
        not math.isnan(r) and r < -0.4
        and not math.isnan(r2) and r2 >= 0.85
    )
    print(f"    GATE r < -0.4 AND R^2 >= 0.85: "
          f"{'PASS' if all_cauchy_ok else 'FAIL'}")
    if all_cauchy_ok and r < 0:
        # Tail-bound from the finest point.  Geometric ratio (N -> 2N) on
        # a CLT-style decay gives tail-sum ~ y_finest / (1 - 2^r).
        y_finest = ys[-1]
        ratio = 2.0 ** r
        tail = y_finest * ratio / (1.0 - ratio) if ratio < 1.0 else math.inf
        print(f"    Tail-sum bound on ||vec_inf - vec(N={N_GRID[-1]})||_2: "
              f"<= {tail:.4e}")

    # --- Ensemble Cauchy: on-basin ---
    print()
    print("=" * 110)
    print("ENSEMBLE-CAUCHY (ON-BASIN SEEDS ONLY)")
    print("  same fit, but per-component we restrict to seeds whose row "
          "passes the basin gate")
    print("=" * 110)
    print()
    rows_b, xs_b, ys_b = cauchy_curve(on_basin_only=True)
    print(f"  {'N1':>5s} -> {'N2':>5s}   {'||vec(N1) - vec(N2)||_2':>26s}")
    for N1, N2, l2 in rows_b:
        print(f"  {N1:>5d} -> {N2:>5d}   {l2:26.6e}")
    r_b, C_b, r2_b = safe_power_fit(xs_b, ys_b)
    print()
    print(f"  Fit on {len(xs_b)} pts: "
          f"||vec(N) - vec(2N)||_2 ~ C * N^r")
    print(f"    r   = {r_b:+.4f}")
    print(f"    C   = {C_b:.4e}")
    print(f"    R^2 = {r2_b:.4f}")
    basin_cauchy_ok = (
        not math.isnan(r_b) and r_b < -0.4
        and not math.isnan(r2_b) and r2_b >= 0.85
    )
    print(f"    GATE r < -0.4 AND R^2 >= 0.85: "
          f"{'PASS' if basin_cauchy_ok else 'FAIL'}")
    if basin_cauchy_ok and r_b < 0:
        y_finest_b = ys_b[-1]
        ratio_b = 2.0 ** r_b
        tail_b = (y_finest_b * ratio_b / (1.0 - ratio_b)
                  if ratio_b < 1.0 else math.inf)
        print(f"    Tail-sum bound on ||vec_inf - vec(N={N_GRID[-1]})||_2: "
              f"<= {tail_b:.4e}")

    # --- Per-component decay rates (diagnostic) ---
    print()
    print("=" * 110)
    print("PER-COMPONENT CAUCHY DECAY RATES (all-seeds vec)")
    print("=" * 110)
    print(f"  {'observable':>10s}  {'source_z':>8s}  "
          f"{'r':>9s}  {'C':>10s}  {'R^2':>8s}")
    per_component_rates: List[float] = []
    for obs in OBSERVABLES:
        for source_z in SOURCE_Z_GRID:
            xs_c = []
            ys_c = []
            for N1, N2 in all_pairs:
                v1: List[float] = []
                v2: List[float] = []
                for sd in per_seed[:N1]:
                    val = sd["per_z"][source_z][obs]
                    if val is not None and not math.isnan(val):
                        v1.append(val)
                for sd in per_seed[:N2]:
                    val = sd["per_z"][source_z][obs]
                    if val is not None and not math.isnan(val):
                        v2.append(val)
                if not v1 or not v2:
                    continue
                m1 = sum(v1) / len(v1)
                m2 = sum(v2) / len(v2)
                delta = abs(m2 - m1)
                if delta > 0:
                    xs_c.append(math.sqrt(N1 * N2))
                    ys_c.append(delta)
            if len(xs_c) >= 2:
                rc, Cc, r2c = safe_power_fit(xs_c, ys_c)
                per_component_rates.append(rc)
                print(f"  {obs:>10s}  {source_z:>8.1f}  "
                      f"{rc:+9.4f}  {Cc:10.4e}  {r2c:8.4f}")

    # --- Summary verdict ---
    print()
    print("=" * 110)
    print("VERDICT")
    print("=" * 110)
    if all_cauchy_ok or basin_cauchy_ok:
        print("  Operator-Cauchy continuum-bridge method EXTENDS to the "
              "alt-connectivity grown DAG family")
        print("  on the ensemble-refinement axis.")
        print(f"    all-seeds: r = {r:+.4f}, R^2 = {r2:.4f}  "
              f"{'PASS' if all_cauchy_ok else 'FAIL'}")
        print(f"    on-basin:  r = {r_b:+.4f}, R^2 = {r2_b:.4f}  "
              f"{'PASS' if basin_cauchy_ok else 'FAIL'}")
        if not math.isnan(r) and r < 0:
            cl_dist = abs(r - (-0.5))
            if cl_dist < 0.12:
                print(f"    decay rate r = {r:+.4f} is consistent with the "
                      f"CLT prediction r = -1/2 (CLT distance "
                      f"{cl_dist:.3f}); identification: ensemble mean is "
                      f"the CLT limit of i.i.d. seed-realizations of the "
                      f"alt-connectivity construction.")
            else:
                print(f"    decay rate r = {r:+.4f} differs from the CLT "
                      f"prediction r = -1/2 by {cl_dist:.3f}; "
                      f"identification of an ensemble-limit vector is "
                      f"not established by this bounded test.")
        print()
        print("  This is the harness's adapted operator-Cauchy bridge: the "
              "spacing-refinement axis is not available")
        print("  (H hardcoded), so we use ensemble-refinement.  The L2 "
              "norm shrinks as a power of N; partial sums of")
        print("  Cauchy increments are summable; the ensemble expectation "
              "exists as a 15-dim continuum vector.")
    else:
        print("  Operator-Cauchy continuum-bridge method does NOT extend "
              "cleanly to the alt-connectivity grown DAG family.")
        print(f"    all-seeds: r = {r:+.4f}, R^2 = {r2:.4f}  FAIL")
        print(f"    on-basin:  r = {r_b:+.4f}, R^2 = {r2_b:.4f}  FAIL")
        print()
        print("  Structural reason for the bounded scope:")
        print("    - the alt-connectivity harness has no clean h-like "
              "refinement parameter (H hardcoded, drift=0 is a degenerate")
        print("      point, and the construction is intrinsically "
              "stochastic)")
        print("    - the ensemble-refinement substitute is contaminated "
              "by the seed-selective sign-orientation boundary "
              "(BASIN_NOTE: 32/45 rows pass; FAILURE_NOTE: 13 sign "
              "flips)")
        print("    - on-basin restriction may help but breaks the i.i.d. "
              "structure required for CLT-style decay")
        print()
        print("  This is a SHARP BOUNDED NULL-RESULT: the harness's "
              "bounded scope is structural to its construction.")

    print(f"\n  Total wallclock: {time.time() - t0:.0f}s")

    expected_no_go = not all_cauchy_ok and not basin_cauchy_ok
    print(f"  Expected no-go check (both ensemble gates fail): "
          f"{'PASS' if expected_no_go else 'FAIL'}")

    # Exit: pass only when the zero-source baseline is clean and the documented
    # no-go is actually observed. If a Cauchy fit closes, this runner's no-go
    # claim has been contradicted and the runner must fail.
    if not zero_ok:
        return 1
    if not expected_no_go:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
