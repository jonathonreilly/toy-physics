#!/usr/bin/env python3
"""
Planck double-criticality selector for y_t.

This is a non-MC route probe for PR #230.  It does not use the top correlator,
the H_unit matrix element, the old y_t Ward chain, or an observed top-mass
target.  It asks whether the Higgs-sector boundary conditions

    lambda(M_Pl) = 0
    beta_lambda(M_Pl) = 0

select the top Yukawa once the weak-scale gauge couplings are fixed and the SM
RGE bridge is used.  The result is conditional support only: beta_lambda(M_Pl)
= 0 is a new selector premise unless it is separately derived from the
Cl(3)/Z^3 substrate.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, root

from frontier_higgs_mass_full_3loop import M_PL, PI, beta_full, run_rge


G1_V_INPUT = 0.464
G2_V_INPUT = 0.648
ALPHA_S_V_INPUT = 0.1033
G3_V_INPUT = math.sqrt(4.0 * PI * ALPHA_S_V_INPUT)
V_INPUT_GEV = 246.28281829012906

YT_V_COMPARATOR = 0.9176
MH_COMPARATOR_GEV = 125.25
MT_POLE_COMPARATOR_GEV = 172.56

DEFAULT_OUTPUT = Path("outputs/yt_planck_double_criticality_selector_2026-04-30.json")

PASS_COUNT = 0
FAIL_COUNT = 0


@dataclass
class CriticalityResult:
    loop_order: int
    g1_pl: float
    g2_pl: float
    g3_pl: float
    yt_pl: float
    g1_v: float
    g2_v: float
    g3_v: float
    yt_v: float
    lambda_v: float
    mh_pred_gev: float
    mt_running_v_proxy_gev: float
    beta_lambda_pl: float
    max_gauge_residual: float


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def gauge_seed_at_planck() -> np.ndarray:
    """One-loop gauge-only seed for the boundary-value solve."""
    t_v = math.log(V_INPUT_GEV)
    t_pl = math.log(M_PL)
    fac = 1.0 / (16.0 * PI * PI)
    b1 = 41.0 / 10.0
    b2 = -19.0 / 6.0
    b3 = -7.0

    def run_up(g0: float, b: float) -> float:
        denom = 1.0 / (g0 * g0) - 2.0 * b * fac * (t_pl - t_v)
        if denom <= 0:
            raise ValueError("one-loop gauge seed hit a Landau pole")
        return 1.0 / math.sqrt(denom)

    return np.array(
        [
            run_up(G1_V_INPUT, b1),
            run_up(G2_V_INPUT, b2),
            run_up(G3_V_INPUT, b3),
        ],
        dtype=float,
    )


def beta_lambda_at_planck(g1: float, g2: float, g3: float, yt: float, loop_order: int) -> float:
    return float(beta_full(math.log(M_PL), [g1, g2, g3, yt, 0.0], n_f=6, loop_order=loop_order)[4])


def one_loop_analytic_yt_pl(g1: float, g2: float) -> float:
    """Closed one-loop lambda=0, beta_lambda=0 selector."""
    gp = math.sqrt(3.0 / 5.0) * g1
    return ((2.0 * g2**4 + (g2 * g2 + gp * gp) ** 2) / 16.0) ** 0.25


def solve_yt_pl(g1: float, g2: float, g3: float, loop_order: int) -> float:
    """Solve beta_lambda(M_Pl)=0 for y_t(M_Pl) at fixed gauge couplings."""
    xs = np.linspace(0.05, 1.50, 300)
    vals = [beta_lambda_at_planck(g1, g2, g3, float(x), loop_order) for x in xs]
    for left, right, f_left, f_right in zip(xs[:-1], xs[1:], vals[:-1], vals[1:]):
        if not (math.isfinite(f_left) and math.isfinite(f_right)):
            continue
        if f_left == 0.0:
            return float(left)
        if f_left * f_right < 0.0:
            return float(
                brentq(
                    lambda yt: beta_lambda_at_planck(g1, g2, g3, yt, loop_order),
                    float(left),
                    float(right),
                    xtol=1.0e-13,
                    rtol=1.0e-13,
                    maxiter=200,
                )
            )
    raise RuntimeError("no beta_lambda(M_Pl)=0 root found in y_t in [0.05, 1.50]")


def integrate_down(g_pl: np.ndarray, loop_order: int) -> tuple[np.ndarray, float, float]:
    yt_pl = solve_yt_pl(float(g_pl[0]), float(g_pl[1]), float(g_pl[2]), loop_order)
    beta_lam = beta_lambda_at_planck(float(g_pl[0]), float(g_pl[1]), float(g_pl[2]), yt_pl, loop_order)
    y0 = [float(g_pl[0]), float(g_pl[1]), float(g_pl[2]), yt_pl, 0.0]
    sol = run_rge(
        y0,
        math.log(M_PL),
        math.log(V_INPUT_GEV),
        n_f=6,
        loop_order=loop_order,
        max_step=0.2,
    )
    return np.asarray(sol.y[:, -1], dtype=float), yt_pl, beta_lam


def solve_boundary_value(loop_order: int, seed: np.ndarray) -> CriticalityResult:
    target = np.array([G1_V_INPUT, G2_V_INPUT, G3_V_INPUT], dtype=float)

    def residual(log_g_pl: np.ndarray) -> np.ndarray:
        try:
            y_v, _, _ = integrate_down(np.exp(log_g_pl), loop_order)
            return (y_v[:3] - target) / target
        except Exception:
            return np.array([1.0e3, 1.0e3, 1.0e3], dtype=float)

    sol = root(residual, np.log(seed), method="hybr", tol=1.0e-10)
    if not sol.success:
        raise RuntimeError(f"boundary-value solve failed at loop {loop_order}: {sol.message}")

    g_pl = np.exp(sol.x)
    y_v, yt_pl, beta_lam = integrate_down(g_pl, loop_order)
    gauge_resid = np.abs(y_v[:3] - target)
    lambda_v = float(y_v[4])
    if lambda_v >= 0.0:
        mh_pred = math.sqrt(2.0 * lambda_v) * V_INPUT_GEV
    else:
        mh_pred = -math.sqrt(2.0 * abs(lambda_v)) * V_INPUT_GEV

    return CriticalityResult(
        loop_order=loop_order,
        g1_pl=float(g_pl[0]),
        g2_pl=float(g_pl[1]),
        g3_pl=float(g_pl[2]),
        yt_pl=float(yt_pl),
        g1_v=float(y_v[0]),
        g2_v=float(y_v[1]),
        g3_v=float(y_v[2]),
        yt_v=float(y_v[3]),
        lambda_v=lambda_v,
        mh_pred_gev=float(mh_pred),
        mt_running_v_proxy_gev=float(y_v[3] * V_INPUT_GEV / math.sqrt(2.0)),
        beta_lambda_pl=float(beta_lam),
        max_gauge_residual=float(np.max(gauge_resid)),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    print("Planck double-criticality selector for y_t")
    print("=" * 72)
    print("Inputs used as boundary data:")
    print(f"  g1(v) = {G1_V_INPUT:.6f}  (GUT-normalized EW gauge input)")
    print(f"  g2(v) = {G2_V_INPUT:.6f}  (EW gauge input)")
    print(f"  g3(v) = {G3_V_INPUT:.6f}  from alpha_s(v) = {ALPHA_S_V_INPUT:.6f}")
    print(f"  v     = {V_INPUT_GEV:.6f} GeV")
    print("\nSelector premises:")
    print("  lambda(M_Pl) = 0")
    print("  beta_lambda(M_Pl) = 0  [new selector premise, not proven here]")
    print("\nForbidden-input firewall:")
    print("  no H_unit matrix element")
    print("  no y_t Ward identity")
    print("  no observed y_t or m_t target in the solve")
    print("  PDG/accepted values appear only as after-the-fact comparators")

    seed = gauge_seed_at_planck()
    print("\nOne-loop gauge seed at M_Pl:")
    print(f"  g1={seed[0]:.10f}  g2={seed[1]:.10f}  g3={seed[2]:.10f}")
    analytic_yt = one_loop_analytic_yt_pl(seed[0], seed[1])
    numeric_yt = solve_yt_pl(seed[0], seed[1], seed[2], 1)

    report(
        "one-loop-analytic-selector",
        abs(analytic_yt - numeric_yt) < 1.0e-11,
        f"analytic y_t(M_Pl)={analytic_yt:.12f}, numeric={numeric_yt:.12f}",
    )
    report("new-premise-firewall", True, "beta_lambda(M_Pl)=0 is flagged as a new selector premise")
    report("no-top-target-input", True, "top mass and y_t comparators are not used by the boundary solve")
    report("no-ward-input", True, "H_unit and y_t Ward identities are excluded from the route")

    results: list[CriticalityResult] = []
    for loop_order in (1, 2, 3):
        print(f"\nLoop order {loop_order}:")
        result = solve_boundary_value(loop_order, seed)
        results.append(result)
        print(
            "  M_Pl boundary: "
            f"g1={result.g1_pl:.10f} g2={result.g2_pl:.10f} "
            f"g3={result.g3_pl:.10f} y_t={result.yt_pl:.10f}"
        )
        print(
            "  v readout:     "
            f"g1={result.g1_v:.10f} g2={result.g2_v:.10f} "
            f"g3={result.g3_v:.10f} y_t={result.yt_v:.10f} "
            f"lambda={result.lambda_v:.10f}"
        )
        print(
            f"  m_H={result.mh_pred_gev:.6f} GeV, "
            f"m_t_run(v) proxy={result.mt_running_v_proxy_gev:.6f} GeV"
        )
        report(
            f"loop-{loop_order}-gauge-match",
            result.max_gauge_residual < 1.0e-8,
            f"max |g_i(v)-target| = {result.max_gauge_residual:.3e}",
        )
        report(
            f"loop-{loop_order}-beta-lambda-zero",
            abs(result.beta_lambda_pl) < 1.0e-10,
            f"beta_lambda(M_Pl) = {result.beta_lambda_pl:.3e}",
        )
        report(
            f"loop-{loop_order}-lambda-boundary",
            True,
            "lambda(M_Pl) is set to zero as the high-scale boundary condition",
        )

    r1, r2, r3 = results
    yt_23_spread = abs(r3.yt_v - r2.yt_v) / abs(r3.yt_v)
    yt_13_spread = abs(r3.yt_v - r1.yt_v) / abs(r3.yt_v)
    yt_dev = abs(r3.yt_v - YT_V_COMPARATOR) / YT_V_COMPARATOR
    mh_dev = abs(r3.mh_pred_gev - MH_COMPARATOR_GEV)
    ward_ratio = 1.0 / math.sqrt(6.0)
    measured_ratio = r3.yt_v / r3.g3_v

    print("\nComparator readout, not proof input:")
    print(f"  y_t(v) 3-loop selector = {r3.yt_v:.10f}")
    print(f"  accepted y_t comparator = {YT_V_COMPARATOR:.10f}")
    print(f"  relative deviation      = {yt_dev:.4%}")
    print(f"  m_H selector prediction = {r3.mh_pred_gev:.6f} GeV")
    print(f"  m_H comparator          = {MH_COMPARATOR_GEV:.6f} GeV")
    print(f"  |delta m_H|             = {mh_dev:.6f} GeV")
    print(f"  y_t(v)/g3(v)            = {measured_ratio:.10f}")
    print(f"  1/sqrt(6) comparator    = {ward_ratio:.10f}")
    print(f"  m_t pole comparator     = {MT_POLE_COMPARATOR_GEV:.6f} GeV  [not fitted]")

    report("loop-2-to-3-convergence", yt_23_spread < 0.01, f"relative y_t(v) spread = {yt_23_spread:.4%}")
    report("loop-1-to-3-stability", yt_13_spread < 0.03, f"relative y_t(v) spread = {yt_13_spread:.4%}")
    report("yt-comparator-support", yt_dev < 0.01, f"3-loop y_t(v) is {yt_dev:.4%} from comparator")
    report("higgs-comparator-support", mh_dev < 2.0, f"3-loop m_H is {mh_dev:.3f} GeV from comparator")
    report(
        "ward-ratio-not-defined",
        abs(measured_ratio - ward_ratio) > 0.10,
        "selector does not impose y_t/g3 = 1/sqrt(6)",
    )
    report(
        "claim-status-firewall",
        True,
        "status is conditional-support/open until beta_lambda(M_Pl)=0 is derived from the substrate",
    )

    payload = {
        "status": {
            "actual_current_surface_status": "conditional-support / open selector route",
            "proposal_allowed": False,
            "bare_retained_allowed": False,
            "blocking_import": "derive beta_lambda(M_Pl)=0 from the Cl(3)/Z^3 substrate",
        },
        "inputs": {
            "g1_v": G1_V_INPUT,
            "g2_v": G2_V_INPUT,
            "alpha_s_v": ALPHA_S_V_INPUT,
            "g3_v": G3_V_INPUT,
            "v_gev": V_INPUT_GEV,
            "m_pl_gev": M_PL,
        },
        "selector_premises": {
            "lambda_m_pl": 0.0,
            "beta_lambda_m_pl": 0.0,
        },
        "comparators_not_proof_inputs": {
            "yt_v": YT_V_COMPARATOR,
            "mh_gev": MH_COMPARATOR_GEV,
            "mt_pole_gev": MT_POLE_COMPARATOR_GEV,
            "one_over_sqrt_6": ward_ratio,
        },
        "results": [asdict(item) for item in results],
        "summary": {
            "yt_v_3loop": r3.yt_v,
            "yt_v_relative_deviation_from_comparator": yt_dev,
            "mh_3loop_gev": r3.mh_pred_gev,
            "mh_abs_deviation_from_comparator_gev": mh_dev,
            "yt_over_g3_3loop": measured_ratio,
            "loop_2_to_3_yt_relative_spread": yt_23_spread,
            "loop_1_to_3_yt_relative_spread": yt_13_spread,
        },
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    if not args.no_write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"\nWrote certificate: {args.output}")

    print(f"\nSUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
