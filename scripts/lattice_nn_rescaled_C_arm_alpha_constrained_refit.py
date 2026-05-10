#!/usr/bin/env python3
"""Alpha-constrained refit of C_arm on the rescaled NN harness.

The upstream continuum diagnostic fitted sigma_arm(h) = C * h^alpha as a
2-parameter log-linear regression on the four fine-h points h <= 0.25 and
obtained

    C_arm_unconstrained = 2.7107
    alpha_unconstrained = 0.5256
    R^2                 = 0.9996

The upstream C_arm coherent-saddle support note derived from a coherent
path-integral saddle on the per-step lateral characteristic function the
closed form

    C_arm_analytic = sqrt( L_2 / ( sqrt(2)/c + 2 ) )  =  2.4855

with c = exp(-BETA pi^2 / 16) at BETA = 0.8 and L_2 = 2 L_total / 3
the post-slit propagation length.

The apparent residual

    ( C_arm_unconstrained - C_arm_analytic ) / C_arm_analytic = +9.06%
    ( C_arm_analytic       - C_arm_unconstrained ) / C_arm_unconstrained = -8.31%

is consistent with a finite-window fit-protocol artifact: the unconstrained
fit lets alpha drift to 0.5256 to absorb the finite-h cosine phase factor in
the saddle, which biases the prefactor C upward to compensate. This runner
uses the upstream geodesic-continuum comparison protocol alpha = 1/2; the
alpha-constrained prefactor is therefore the per-h evaluation

    C_arm(h) := sigma_arm(h) / sqrt(h)

and the h -> 0 estimator

    C_arm_extrap := C_arm(h_finest).

This runner does that. It loads the per-h sigma_arm values from PR
the upstream runner cache, computes C_arm(h) under the alpha = 1/2
comparison protocol, and reports the residual against the coherent-saddle
analytic 2.4855 and against the upstream unconstrained fit 2.7107. It also
includes a freshly measured row at h = 0.015625 (one factor of 2 finer than
the upstream continuum note's finest grid point), measured by the same
function used in that runner.

Outcome registered (this run):

  - residual at h = 0.03125 closes to 0.504% under alpha-constrained fit
  - residual at h = 0.015625 closes to 0.268%
  - the 8.31% apparent gap is explained within this bounded comparison by
    the finite-window fit protocol; the analytic and numerical constants
    agree pointwise at the finest measured h to better than half a percent

Usage:
    python3 scripts/lattice_nn_rescaled_C_arm_alpha_constrained_refit.py
"""

from __future__ import annotations

import math
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------------------
# Frozen harness parameters (must match
# scripts/lattice_nn_rescaled_continuum_identification.py and
# scripts/lattice_nn_rescaled_C_arm_derivation.py)
# ---------------------------------------------------------------------------

BETA = 0.8
K_PHYS = 5.0
PHYS_L = 40.0
FANOUT = 3.0
SLIT_Y = 3.0


def c_factor() -> float:
    """exp(-BETA * (pi/4)^2 * 4) = exp(-BETA pi^2 / 16) for the +/-1 edges."""
    return math.exp(-BETA * math.pi * math.pi / 16.0)


def C_arm_analytic() -> float:
    """Closed-form geodesic constant from the C_arm support note.

    C_arm^2 = L_2 / ( sqrt(2)/c + 2 ),   L_2 = 2 L_total / 3.
    """
    c = c_factor()
    denom = math.sqrt(2.0) / c + 2.0
    L_2 = 2.0 * PHYS_L / 3.0
    return math.sqrt(L_2 / denom)


# ---------------------------------------------------------------------------
# Upstream raw data: per-h sigma_arm values from
#   logs/runner-cache/lattice_nn_rescaled_continuum_identification.txt
# (cached on main; identical to the upstream runner output).
# ---------------------------------------------------------------------------

PR968_ROWS: List[Dict[str, float]] = [
    {"h": 1.00000,  "mu_a": +3.4458, "mu_b": -3.4458,
     "sigma_a": 2.9876, "sigma_b": 2.9876,
     "MI_obs": 0.5022, "dtv_obs": 0.7455, "born": 4.94e-16},
    {"h": 0.50000,  "mu_a": +3.5638, "mu_b": -3.4126,
     "sigma_a": 2.0785, "sigma_b": 2.0643,
     "MI_obs": 0.7420, "dtv_obs": 0.9046, "born": 3.92e-16},
    {"h": 0.25000,  "mu_a": +3.3168, "mu_b": -3.2725,
     "sigma_a": 1.3198, "sigma_b": 1.3096,
     "MI_obs": 0.9470, "dtv_obs": 0.9877, "born": 5.96e-16},
    {"h": 0.12500,  "mu_a": +3.1701, "mu_b": -3.1666,
     "sigma_a": 0.8990, "sigma_b": 0.8979,
     "MI_obs": 0.9972, "dtv_obs": 0.9996, "born": 9.90e-16},
    {"h": 0.06250,  "mu_a": +3.0895, "mu_b": -3.0895,
     "sigma_a": 0.6282, "sigma_b": 0.6282,
     "MI_obs": 1.0000, "dtv_obs": 1.0000, "born": 8.69e-16},
    {"h": 0.03125,  "mu_a": +3.0467, "mu_b": -3.0467,
     "sigma_a": 0.4416, "sigma_b": 0.4416,
     "MI_obs": 1.0000, "dtv_obs": 1.0000, "born": 1.23e-15},
]

# Upstream unconstrained fit (printed verbatim from the cached log)
C_ARM_UNCONSTRAINED = 2.7107
ALPHA_UNCONSTRAINED = 0.5256

# Whether to (re)measure h = 0.015625. If False, use the hardcoded value
# from this runner's first measurement (recorded below). Recommended True
# the first time to verify, False thereafter to keep the runner fast.
MEASURE_FINER_H = True
H_FINER = 0.015625
# Verified value from a fresh measurement on this branch (kept as a
# fallback if MEASURE_FINER_H is set False or the import fails):
SIGMA_FINER_FALLBACK = 0.3115


def measure_finer_row() -> Optional[Dict[str, float]]:
    """Measure sigma_arm at H_FINER using the upstream runner's function."""
    try:
        from lattice_nn_rescaled_continuum_identification import (
            measure_arm_distribution,
        )
    except Exception as exc:  # pragma: no cover
        print(f"  [warn] could not import measure_arm_distribution: {exc}")
        return None

    print(f"  [info] measuring h = {H_FINER} via the upstream "
          f"measure_arm_distribution(...) - this takes ~70s")
    t0 = time.time()
    r = measure_arm_distribution(H_FINER)
    dt = time.time() - t0
    if r is None:
        print(f"  [warn] measure_arm_distribution returned None")
        return None
    print(f"  [info] h = {H_FINER}: dt = {dt:.1f}s, n = {r['n']}, "
          f"mu = (+{r['mu_a']:.4f}, {r['mu_b']:+.4f}), "
          f"sigma = ({r['sigma_a']:.4f}, {r['sigma_b']:.4f}), "
          f"MI = {r['MI_obs']:.6f}, d_TV = {r['dtv_obs']:.6f}, "
          f"Born = {r['born']:.2e}")
    return {
        "h": H_FINER,
        "mu_a": r["mu_a"], "mu_b": r["mu_b"],
        "sigma_a": r["sigma_a"], "sigma_b": r["sigma_b"],
        "MI_obs": r["MI_obs"], "dtv_obs": r["dtv_obs"],
        "born": r["born"],
        "_measured": True,
        "_elapsed_sec": dt,
        "_n_nodes": r["n"],
    }


def reldiff(pred: float, ref: float) -> float:
    return (pred - ref) / ref


def main() -> int:
    print("=" * 100)
    print("NN LATTICE RESCALED-LANE C_arm ALPHA-CONSTRAINED REFIT")
    print("  Scoped comparison protocol: alpha = 1/2")
    print("  Estimator: C_arm(h) := sigma_arm(h) / sqrt(h),  per-h, no log-fit")
    print("=" * 100)
    print()

    C_an = C_arm_analytic()
    print(f"Analytic constant (C_arm support note closed form):")
    print(f"  c                  = exp(-BETA pi^2 / 16) = {c_factor():.6f}")
    print(f"  L_2                = 2 L_total / 3        = {2 * PHYS_L / 3:.6f}")
    print(f"  C_arm_analytic     = sqrt(L_2 / (sqrt(2)/c + 2)) = {C_an:.6f}")
    print()
    print(f"Unconstrained 2-parameter fit (upstream continuum note):")
    print(f"  C_arm_unconstrained = {C_ARM_UNCONSTRAINED}")
    print(f"  alpha_unconstrained = {ALPHA_UNCONSTRAINED}     "
          f"(geodesic prediction: 0.5)")
    print()

    rows: List[Dict[str, float]] = list(PR968_ROWS)

    # Optionally extend with the freshly measured h = 0.015625 row.
    finer_row: Optional[Dict[str, float]] = None
    if MEASURE_FINER_H:
        print("-" * 100)
        print(f"OPTIONAL: extend grid by one factor of 2 (h = {H_FINER})")
        print("-" * 100)
        finer_row = measure_finer_row()
        if finer_row is None:
            print("FAIL: finer-h measurement is required when MEASURE_FINER_H is True.")
            return 1
        rows.append(finer_row)
        print()

    # If not measured, still record the fallback verified value.
    if finer_row is None:
        rows.append({
            "h": H_FINER,
            "mu_a": +3.0239, "mu_b": -3.0239,
            "sigma_a": SIGMA_FINER_FALLBACK,
            "sigma_b": SIGMA_FINER_FALLBACK,
            "MI_obs": 1.0, "dtv_obs": 1.0, "born": 1.32e-15,
            "_measured": False,
        })

    # ------------------------------------------------------------------
    # Per-h C_arm under alpha = 1/2 constraint
    # ------------------------------------------------------------------
    print("=" * 100)
    print("PER-h ALPHA-CONSTRAINED C_arm  (alpha fixed at 1/2)")
    print("=" * 100)
    print()
    print(f"  {'h':>10s}  {'sigma_a':>8s}  {'sigma_b':>8s}  "
          f"{'C_arm_a':>9s}  {'C_arm_b':>9s}  {'C_arm':>9s}  "
          f"{'res_an':>9s}  {'res_un':>9s}  note")
    print(f"  {'-' * 110}")

    for r in rows:
        h = r["h"]
        sa = r["sigma_a"]
        sb = r["sigma_b"]
        sqrt_h = math.sqrt(h)
        Ca = sa / sqrt_h
        Cb = sb / sqrt_h
        Cavg = 0.5 * (Ca + Cb)
        res_an = reldiff(Cavg, C_an) * 100.0
        res_un = reldiff(Cavg, C_ARM_UNCONSTRAINED) * 100.0
        flag = ""
        if abs(h - H_FINER) < 1e-9:
            tag = "measured" if r.get("_measured") else "fallback"
            flag = f"new finer point ({tag})"
        elif h <= 0.25 and h not in (1.0, 0.5):
            flag = "fine-h (used in upstream fit)"
        else:
            flag = "coarse-h transient"
        print(f"  {h:10.6f}  {sa:8.4f}  {sb:8.4f}  "
              f"{Ca:9.4f}  {Cb:9.4f}  {Cavg:9.4f}  "
              f"{res_an:+8.3f}%  {res_un:+8.3f}%  {flag}")

    # ------------------------------------------------------------------
    # Closure summary
    # ------------------------------------------------------------------
    fine_rows = [r for r in rows if r["h"] <= 0.25 + 1e-9]
    finest = min(fine_rows, key=lambda r: r["h"])
    sigma_finest_avg = 0.5 * (finest["sigma_a"] + finest["sigma_b"])
    C_extrap = sigma_finest_avg / math.sqrt(finest["h"])
    res_an_extrap = reldiff(C_extrap, C_an) * 100.0
    res_un_extrap = reldiff(C_extrap, C_ARM_UNCONSTRAINED) * 100.0

    print()
    print("=" * 100)
    print("CLOSURE SUMMARY")
    print("=" * 100)
    print()
    print(f"  Finest measured h          = {finest['h']:.6f}")
    print(f"  sigma_arm(h_finest) (avg)  = {sigma_finest_avg:.6f}")
    print(f"  C_arm_constrained_extrap   = sigma_arm(h_finest) / sqrt(h_finest)")
    print(f"                             = {C_extrap:.6f}")
    print()
    print(f"  C_arm support analytic     = {C_an:.6f}")
    print(f"  Upstream unconstrained fit = {C_ARM_UNCONSTRAINED:.6f}")
    print()
    print(f"  Residual (extrap vs analytic)        = {res_an_extrap:+.3f}%")
    print(f"  Residual (extrap vs unconstrained C) = {res_un_extrap:+.3f}%")
    print()

    # h = 0.03125 specific line, since the prompt's acceptance criterion
    # is anchored there.
    h_target = 0.03125
    target = next((r for r in rows if abs(r["h"] - h_target) < 1e-9), None)
    if target is not None:
        sigma_t = 0.5 * (target["sigma_a"] + target["sigma_b"])
        C_t = sigma_t / math.sqrt(h_target)
        res_t = reldiff(C_t, C_an) * 100.0
        print(f"  At h = 0.03125 (acceptance criterion):")
        print(f"    C_arm_constrained     = {C_t:.6f}")
        print(f"    residual vs analytic  = {res_t:+.3f}%   "
              f"(acceptance: |residual| <= 2%)")
        target_passes = abs(res_t) <= 2.0
        sub_one_percent = abs(res_t) < 1.0
        if sub_one_percent:
            print("    BOUNDED PASS: residual < 1% under alpha-constrained fit.")
            print("    The 8.3% reported gap is removed by the scoped fit protocol.")
            print("    Analytic and numerical constants agree pointwise at h = 0.03125.")
        elif target_passes:
            print("    BOUNDED PASS: residual <= 2% under alpha-constrained fit.")
        else:
            print("    MIXED CASE: residual > 2%, gap not closed by fit protocol.")

    # If the new finer point exists, also state it.
    if finer_row is not None:
        sigma_fnew = 0.5 * (finer_row["sigma_a"] + finer_row["sigma_b"])
        C_fnew = sigma_fnew / math.sqrt(H_FINER)
        res_fnew = reldiff(C_fnew, C_an) * 100.0
        print()
        print(f"  At h = {H_FINER} (newly measured this run):")
        print(f"    sigma_arm (avg)       = {sigma_fnew:.6f}")
        print(f"    C_arm_constrained     = {C_fnew:.6f}")
        print(f"    residual vs analytic  = {res_fnew:+.3f}%")
        if abs(res_fnew) < 1.0:
            print("    The residual continues to shrink monotonically as h -> 0,")
            print("    consistent with the bounded geodesic saddle model being")
            print("    the leading-order comparison surface.")

    # Trend in C_arm(h) - C_an as h shrinks
    print()
    print("  Convergence of (C_arm(h) - C_arm_analytic)/C_arm_analytic:")
    print(f"    {'h':>10s}  {'res_an (%)':>10s}")
    for r in sorted(rows, key=lambda x: -x["h"]):
        h = r["h"]
        if h > 0.25 + 1e-9:
            continue
        sigma = 0.5 * (r["sigma_a"] + r["sigma_b"])
        C = sigma / math.sqrt(h)
        res = reldiff(C, C_an) * 100.0
        print(f"    {h:10.6f}  {res:+10.3f}")

    residual_rows = []
    for r in sorted(rows, key=lambda x: -x["h"]):
        h = r["h"]
        if h > 0.25 + 1e-9:
            continue
        sigma = 0.5 * (r["sigma_a"] + r["sigma_b"])
        C = sigma / math.sqrt(h)
        residual_rows.append(abs(reldiff(C, C_an) * 100.0))
    monotonic_ok = all(
        b <= a + 1e-9 for a, b in zip(residual_rows, residual_rows[1:])
    )
    born_ok = finest.get("born", 1.0) < 1e-12
    symmetry_ok = (
        abs(finest["sigma_a"] - finest["sigma_b"]) <= 1e-3
        and abs(abs(finest["mu_a"]) - SLIT_Y) < 1.0
        and abs(abs(finest["mu_b"]) - SLIT_Y) < 1.0
    )
    target_ok = target is not None and abs(res_t) <= 2.0
    finest_ok = abs(res_an_extrap) <= 2.0

    print()
    print("  Runner gates:")
    print(f"    h = 0.03125 residual <= 2%: {'PASS' if target_ok else 'FAIL'}")
    print(f"    finest residual <= 2%:      {'PASS' if finest_ok else 'FAIL'}")
    print(f"    residuals shrink with h:    {'PASS' if monotonic_ok else 'FAIL'}")
    print(f"    finest Born residual <1e-12:{'PASS' if born_ok else 'FAIL'}")
    print(f"    finest arm symmetry/drift:  {'PASS' if symmetry_ok else 'FAIL'}")

    return 0 if (target_ok and finest_ok and monotonic_ok and born_ok and symmetry_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
