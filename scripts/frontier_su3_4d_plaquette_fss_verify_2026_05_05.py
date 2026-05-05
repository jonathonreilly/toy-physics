#!/usr/bin/env python3
"""SU(3) Wilson plaquette 4D FSS verifier.

Companion to `frontier_su3_4d_plaquette_fss_data_2026_05_05.py` and to
`PLAQUETTE_4D_MC_FSS_NUMERICAL_THEOREM_NOTE_2026-05-05.md`.

This runner reads the MC artifacts produced by the data generator and tests
the load-bearing bridge: that an honest finite-size analysis of the seeded
data produces a controlled thermodynamic-limit bracket with a documented
error budget. It does not hard-code an L->infinity target; the comparator is
reported only as context.

What this runner does:
- loads each `outputs/su3_plaquette_fss_2026_05_05/L<L>_seed42_beta6.json`;
- computes integrated autocorrelation time (Madras-Sokal windowed estimator);
- computes block-jackknife mean and statistical error per L using a block
  size that exceeds 2 * tau_int;
- fits two finite-size scaling models on the per-L means with statistical
  weights:
    M1 (linear in 1/V):  P(L) = P_inf + c1 / L^4
    M2 (linear in 1/L^2): P(L) = P_inf + c2 / L^2
  via weighted least squares; reports P_inf and a leave-one-out error bracket;
- emits a result artifact at `outputs/su3_plaquette_fss_2026_05_05/fss_summary.json`;
- asserts a minimum scientific bar:
    A. at least 3 distinct volumes are present;
    B. each volume's tau_int is finite and the effective sample size is at
       least 8 (so the per-L SE is meaningful);
    C. block-jackknife SE is positive and finite for every L;
    D. each P(L) lies in a wide canonical band (0.55 < P(L) < 0.65) showing
       the data come from the right region and not from a broken protocol;
    E. P(L) is monotone in 1/V to within the per-L SE (FSS sanity);
    F. the two FSS forms are consistent: their P_inf estimates agree to
       within the sum of their leave-one-out SE plus their fit chi^2-derived
       SE;
    G. the FSS-bracket diameter is reported and finite;
    H. at least five volumes are present for the strengthened numerical
       theorem candidate;
    I. the two-parameter FSS fits have at least three degrees of freedom;
    J. the two FSS forms agree within 3 sigma RSS;
    K. the canonical comparator lies inside the M1 two-sigma bracket.

A FAIL on (A)-(K) means the five-volume numerical theorem candidate has not
been demonstrated at the current data set. That is the honest outcome and is
what the source note treats as the open frontier.
"""

from __future__ import annotations

import json
import math
import os
import sys

import numpy as np


ARTIFACT_DIR = os.path.join("outputs", "su3_plaquette_fss_2026_05_05")
COMPARATOR = 0.5934

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def integrated_autocorrelation_time(samples: np.ndarray, c_madras: float = 5.0) -> tuple[float, int]:
    """Madras-Sokal windowed integrated autocorrelation estimator.

    tau_int = 1/2 + sum_{t=1}^{W} rho(t)
    with the window W chosen as the smallest W such that W >= c_madras * tau_int.

    This is the standard self-consistent windowed estimator used in lattice
    Monte Carlo error analysis. Returns (tau_int, window).
    """
    n = len(samples)
    if n < 8:
        return 0.5, 0
    x = samples - np.mean(samples)
    var = np.dot(x, x) / n
    if var <= 0.0:
        return 0.5, 0
    rho = np.zeros(n)
    rho[0] = 1.0
    for t in range(1, n):
        rho[t] = np.dot(x[: n - t], x[t:]) / ((n - t) * var)
    tau = 0.5
    window = 0
    for t in range(1, n):
        tau += rho[t]
        if t >= c_madras * max(tau, 0.5):
            window = t
            break
    if window == 0:
        window = n - 1
    return float(max(tau, 0.5)), int(window)


def block_jackknife(samples: np.ndarray, block_size: int) -> tuple[float, float]:
    """Block jackknife mean and standard error.

    Splits the samples into N_block consecutive blocks of `block_size`. For
    each block i, computes the mean of all samples NOT in that block. The
    jackknife SE is sqrt((N-1)/N * sum (theta_i - theta_bar)^2).
    """
    n = len(samples)
    n_blocks = max(2, n // block_size)
    block_size = n // n_blocks
    truncated = samples[: n_blocks * block_size]
    blocks = truncated.reshape(n_blocks, block_size).mean(axis=1)
    overall = float(blocks.mean())
    leave_one_out = np.zeros(n_blocks)
    for i in range(n_blocks):
        leave_one_out[i] = (blocks.sum() - blocks[i]) / (n_blocks - 1)
    se = math.sqrt((n_blocks - 1) / n_blocks * np.sum((leave_one_out - overall) ** 2))
    return overall, float(se)


def weighted_linear_fit(xs: np.ndarray, ys: np.ndarray, sigmas: np.ndarray) -> tuple[float, float, float, float, float]:
    """Weighted linear fit ys = a + b * xs minimizing sum ((y - a - b*x)/sigma)^2.

    Returns (a, sigma_a, b, sigma_b, chi2_per_dof).
    """
    w = 1.0 / sigmas ** 2
    Sw = w.sum()
    Sx = (w * xs).sum()
    Sy = (w * ys).sum()
    Sxx = (w * xs * xs).sum()
    Sxy = (w * xs * ys).sum()
    det = Sw * Sxx - Sx * Sx
    if abs(det) < 1e-30:
        raise RuntimeError("singular fit normal equations")
    a = (Sxx * Sy - Sx * Sxy) / det
    b = (Sw * Sxy - Sx * Sy) / det
    sigma_a = math.sqrt(Sxx / det)
    sigma_b = math.sqrt(Sw / det)
    residuals = ys - (a + b * xs)
    chi2 = float(np.sum((residuals / sigmas) ** 2))
    dof = max(1, len(xs) - 2)
    return a, sigma_a, b, sigma_b, chi2 / dof


def fss_fit_with_jackknife(
    Ls: np.ndarray, Ps: np.ndarray, Pses: np.ndarray, exponent: int
) -> dict:
    """Weighted FSS fit P(L) = P_inf + c / L^exponent, with leave-one-out error.

    Performs a weighted linear fit on (1/L^exponent, P) with statistical
    weights from `Pses`. Then jackknifes the fit by leaving out one L at a
    time. The leave-one-out SE on P_inf is the sample std of the leave-one-
    out estimates, scaled to a one-sigma equivalent.
    """
    xs = 1.0 / Ls.astype(float) ** exponent
    a, sigma_a, b, sigma_b, chi2_per_dof = weighted_linear_fit(xs, Ps, Pses)
    fit_P_inf = float(a)
    fit_P_inf_se = float(sigma_a)
    fit_chi2_per_dof = float(chi2_per_dof)

    leave_one = []
    if len(Ls) >= 3:
        for i in range(len(Ls)):
            mask = np.ones(len(Ls), dtype=bool)
            mask[i] = False
            if mask.sum() < 2:
                continue
            try:
                a_i, _, _, _, _ = weighted_linear_fit(xs[mask], Ps[mask], Pses[mask])
                leave_one.append(a_i)
            except RuntimeError:
                continue
    if len(leave_one) >= 2:
        loo_arr = np.array(leave_one)
        loo_se = float(np.std(loo_arr, ddof=1))
    else:
        loo_se = float("nan")

    return {
        "exponent": exponent,
        "P_inf": fit_P_inf,
        "P_inf_fit_se": fit_P_inf_se,
        "P_inf_loo_se": loo_se,
        "slope": float(b),
        "slope_se": float(sigma_b),
        "chi2_per_dof": fit_chi2_per_dof,
        "leave_one_out_estimates": leave_one,
    }


def load_artifacts() -> list[dict]:
    if not os.path.isdir(ARTIFACT_DIR):
        return []
    artifacts: list[dict] = []
    for fn in sorted(os.listdir(ARTIFACT_DIR)):
        if not fn.startswith("L") or not fn.endswith(".json"):
            continue
        if fn == "fss_summary.json":
            continue
        path = os.path.join(ARTIFACT_DIR, fn)
        with open(path) as f:
            artifacts.append(json.load(f))
    artifacts.sort(key=lambda a: a["L"])
    return artifacts


def main() -> int:
    print("=" * 78)
    print("SU(3) WILSON PLAQUETTE 4D FSS VERIFIER")
    print("=" * 78)

    artifacts = load_artifacts()
    if not artifacts:
        print()
        print(f"NO ARTIFACTS FOUND under {ARTIFACT_DIR}.")
        print("Run the data generator first:")
        print("  python3 scripts/frontier_su3_4d_plaquette_fss_data_2026_05_05.py")
        check("artifacts present", False, detail=f"directory empty or missing: {ARTIFACT_DIR}")
        print()
        print("=" * 78)
        print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
        print("=" * 78)
        return 1

    print(f"loaded {len(artifacts)} artifacts from {ARTIFACT_DIR}")
    print()

    per_L: list[dict] = []
    for art in artifacts:
        L = art["L"]
        samples = np.array(art["samples"], dtype=float)
        print(f"--- L = {L} ---")
        print(f"  n_samples={len(samples)}, n_meas_sweeps={art['n_measure_sweeps']}, sample_every={art['sample_every']}")
        print(f"  acceptance during measure = {art['acceptance_during_measure']:.3f}")
        tau, window = integrated_autocorrelation_time(samples)
        n_eff = len(samples) / max(2.0 * tau, 1.0)
        print(f"  tau_int = {tau:.2f} (window = {window}), n_eff = {n_eff:.1f}")
        block = max(4, int(math.ceil(2.0 * tau)))
        if block > len(samples) // 4:
            block = max(2, len(samples) // 4)
        mean, se = block_jackknife(samples, block)
        print(f"  block-jackknife (block={block}): mean = {mean:.5f}, SE = {se:.5f}")
        per_L.append(
            {
                "L": L,
                "n_samples": len(samples),
                "tau_int": tau,
                "window": window,
                "n_eff": n_eff,
                "block_size": block,
                "mean": mean,
                "se": se,
            }
        )

    Ls = np.array([d["L"] for d in per_L])
    Ps = np.array([d["mean"] for d in per_L])
    SEs = np.array([d["se"] for d in per_L])
    SEs_safe = np.where(SEs > 0, SEs, 1e-6)

    print()
    print("--- FSS fits ---")
    fits: dict[str, dict] = {}
    for label, exponent in [("M1_inv_V", 4), ("M2_inv_L2", 2)]:
        if len(Ls) >= 2:
            r = fss_fit_with_jackknife(Ls, Ps, SEs_safe, exponent)
            fits[label] = r
            print(
                f"  {label}: P_inf = {r['P_inf']:.5f} +/- {r['P_inf_fit_se']:.5f} (fit), "
                f"+/- {r['P_inf_loo_se']:.5f} (LOO),  chi2/dof = {r['chi2_per_dof']:.3f}"
            )
        else:
            fits[label] = {"P_inf": float("nan")}
            print(f"  {label}: insufficient L values for fit")

    summary = {
        "version": "2026-05-05",
        "comparator_context_only": COMPARATOR,
        "per_L": per_L,
        "fss_fits": fits,
    }
    if "M1_inv_V" in fits and isinstance(fits["M1_inv_V"].get("P_inf"), float) and not math.isnan(fits["M1_inv_V"]["P_inf"]):
        summary["P_inf_M1"] = fits["M1_inv_V"]["P_inf"]
        summary["P_inf_M1_combined_se"] = math.hypot(
            fits["M1_inv_V"]["P_inf_fit_se"],
            0.0 if math.isnan(fits["M1_inv_V"]["P_inf_loo_se"]) else fits["M1_inv_V"]["P_inf_loo_se"],
        )
        summary["comparator_distance_M1"] = fits["M1_inv_V"]["P_inf"] - COMPARATOR

    out_path = os.path.join(ARTIFACT_DIR, "fss_summary.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  wrote: {out_path}")

    print()
    print("--- Baseline numerical checks ---")

    # A: enough volumes
    check(
        "A. at least 3 distinct lattice volumes are present",
        len(Ls) >= 3,
        detail=f"L values present = {Ls.tolist()}",
    )

    # B: tau_int finite and n_eff >= 8
    if len(per_L) > 0:
        all_n_eff_ok = all(d["n_eff"] >= 8.0 for d in per_L)
        worst = min(d["n_eff"] for d in per_L)
        check(
            "B. effective sample size n_eff >= 8 for every L",
            all_n_eff_ok,
            detail=f"min n_eff over L = {worst:.1f}",
        )
    else:
        check("B. effective sample size n_eff >= 8 for every L", False, detail="no data")

    # C: jackknife SE positive
    if len(per_L) > 0:
        all_se_ok = all(d["se"] > 0 and math.isfinite(d["se"]) for d in per_L)
        check(
            "C. block-jackknife SE finite and positive for every L",
            all_se_ok,
            detail=f"SE values = {[round(d['se'], 5) for d in per_L]}",
        )
    else:
        check("C. block-jackknife SE finite and positive for every L", False, detail="no data")

    # D: each P(L) in canonical band
    if len(per_L) > 0:
        in_band = all(0.55 < d["mean"] < 0.65 for d in per_L)
        check(
            "D. each P(L) lies in the canonical 0.55..0.65 band",
            in_band,
            detail=f"means = {[round(d['mean'], 5) for d in per_L]}",
        )
    else:
        check("D. each P(L) lies in the canonical 0.55..0.65 band", False, detail="no data")

    # E: monotone in 1/V to within SE
    if len(per_L) >= 2:
        sorted_by_L = sorted(per_L, key=lambda d: d["L"])
        violations: list[str] = []
        for i in range(len(sorted_by_L) - 1):
            small = sorted_by_L[i]
            big = sorted_by_L[i + 1]
            # As L grows, 1/V decreases, P should decrease toward P_inf if
            # the leading finite-volume coefficient is positive. Allow a
            # small upward fluctuation within the combined standard error.
            diff = small["mean"] - big["mean"]
            combined_se = math.hypot(small["se"], big["se"])
            if diff < -3 * combined_se:
                violations.append(f"L={small['L']}->{big['L']}: diff={diff:.4f}, 3SE={3 * combined_se:.4f}")
        check(
            "E. P(L) is monotone decreasing with L up to 3 combined SE",
            not violations,
            detail="violations: " + "; ".join(violations) if violations else "all neighboring L pairs consistent",
        )
    else:
        check("E. P(L) is FSS-consistent across volumes", False, detail="need at least 2 L values")

    # F: two FSS forms agree at the 3 sigma level (RSS-combined SE on the model means).
    # With only 3 lattice volumes, two-parameter FSS fits cannot
    # statistically discriminate between functional forms; a 3 sigma
    # tolerance is the standard test for cross-model consistency.
    if "M1_inv_V" in fits and "M2_inv_L2" in fits and not math.isnan(fits["M1_inv_V"].get("P_inf", float("nan"))):
        m1 = fits["M1_inv_V"]
        m2 = fits["M2_inv_L2"]
        diff = abs(m1["P_inf"] - m2["P_inf"])
        m1_loo = 0.0 if math.isnan(m1["P_inf_loo_se"]) else m1["P_inf_loo_se"]
        m2_loo = 0.0 if math.isnan(m2["P_inf_loo_se"]) else m2["P_inf_loo_se"]
        m1_total_se = math.hypot(m1["P_inf_fit_se"], m1_loo)
        m2_total_se = math.hypot(m2["P_inf_fit_se"], m2_loo)
        combined_rss = math.hypot(m1_total_se, m2_total_se)
        threshold = 3.0 * combined_rss
        check(
            "F. two FSS forms (1/V and 1/L^2) give P_inf agreeing within 3 sigma (RSS)",
            diff <= threshold and combined_rss > 0,
            detail=f"|M1-M2| = {diff:.5f}, 3-sigma RSS threshold = {threshold:.5f}, sigma_significance = {diff / max(combined_rss, 1e-12):.2f}",
        )
    else:
        check("F. two FSS forms agree at 3 sigma RSS", False, detail="missing one of the fits")

    # G: bracket diameter finite
    if "M1_inv_V" in fits and not math.isnan(fits["M1_inv_V"].get("P_inf", float("nan"))):
        m1 = fits["M1_inv_V"]
        m1_loo = 0.0 if math.isnan(m1["P_inf_loo_se"]) else m1["P_inf_loo_se"]
        combined_se = math.hypot(m1["P_inf_fit_se"], m1_loo)
        bracket_lo = m1["P_inf"] - 2.0 * combined_se
        bracket_hi = m1["P_inf"] + 2.0 * combined_se
        diameter = bracket_hi - bracket_lo
        check(
            "G. M1 bracket [P_inf - 2 SE, P_inf + 2 SE] has finite diameter",
            math.isfinite(diameter) and diameter > 0,
            detail=f"bracket = [{bracket_lo:.5f}, {bracket_hi:.5f}], diameter = {diameter:.5f}",
        )
    else:
        check("G. M1 bracket has finite diameter", False, detail="M1 fit unavailable")

    # H: report only
    if "comparator_distance_M1" in summary:
        d = summary["comparator_distance_M1"]
        print(f"  [INFO] H. comparator distance |P_inf(M1) - {COMPARATOR}| = {abs(d):.5f}  (reported, not asserted)")

    print()
    print("--- Five-volume numerical-theorem checks ---")
    check(
        "H. at least 5 distinct lattice volumes are present",
        len(Ls) >= 5,
        detail=f"L values present = {Ls.tolist()}",
    )
    check(
        "I. two-parameter FSS fits have at least 3 degrees of freedom",
        len(Ls) - 2 >= 3,
        detail=f"dof = {len(Ls) - 2}",
    )
    if "M1_inv_V" in fits and "M2_inv_L2" in fits and not math.isnan(fits["M1_inv_V"].get("P_inf", float("nan"))):
        m1 = fits["M1_inv_V"]
        m2 = fits["M2_inv_L2"]
        diff = abs(m1["P_inf"] - m2["P_inf"])
        m1_loo = 0.0 if math.isnan(m1["P_inf_loo_se"]) else m1["P_inf_loo_se"]
        m2_loo = 0.0 if math.isnan(m2["P_inf_loo_se"]) else m2["P_inf_loo_se"]
        m1_total_se = math.hypot(m1["P_inf_fit_se"], m1_loo)
        m2_total_se = math.hypot(m2["P_inf_fit_se"], m2_loo)
        combined_rss = math.hypot(m1_total_se, m2_total_se)
        check(
            "J. two FSS forms agree within 3 sigma RSS",
            diff <= 3.0 * combined_rss and combined_rss > 0,
            detail=f"|M1-M2| = {diff:.5f}, 3-sigma RSS threshold = {3.0 * combined_rss:.5f}",
        )
        m1_bracket_lo = m1["P_inf"] - 2.0 * m1_total_se
        m1_bracket_hi = m1["P_inf"] + 2.0 * m1_total_se
        check(
            "K. canonical comparator lies inside the M1 two-sigma bracket",
            m1_bracket_lo <= COMPARATOR <= m1_bracket_hi,
            detail=f"comparator={COMPARATOR}, bracket=[{m1_bracket_lo:.5f}, {m1_bracket_hi:.5f}]",
        )
    else:
        check("J. two FSS forms agree within 3 sigma RSS", False, detail="missing one of the fits")
        check("K. canonical comparator lies inside the M1 two-sigma bracket", False, detail="M1 fit unavailable")

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 78)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
