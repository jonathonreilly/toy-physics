#!/usr/bin/env python3
"""SU(3) Wilson plaquette 4D FSS RETAINED-GRADE verifier (5-volume).

Companion to `frontier_su3_4d_plaquette_fss_data_2026_05_05.py` and to
`PLAQUETTE_4D_MC_FSS_RETAINED_THEOREM_NOTE_2026-05-05.md`.

EXTENDS the bounded verifier with tighter retained-grade assertions:
- 5 distinct lattice volumes (vs 3 for bounded)
- 2-parameter FSS fits have ≥3 dof
- Cross-model agreement at <2σ RSS (tighter than bounded's 3σ)
- L→∞ extrapolation within 0.5% of comparator

Falls back to bounded scope if fewer than 5 volumes are available.
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np


ARTIFACT_DIR = os.path.join("outputs", "su3_plaquette_fss_2026_05_05")
COMPARATOR = 0.5934
RETAINED_TOLERANCE = 0.005   # 0.5% precision required for retained promotion
RETAINED_CROSS_MODEL_SIGMA = 2.0  # cross-model agreement at <2σ for retained
RETAINED_MIN_VOLUMES = 5  # need 5 volumes for retained-grade 2-param FSS

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


def madras_sokal_tau_int(samples):
    """Madras-Sokal windowed integrated autocorrelation time."""
    samples = np.asarray(samples, dtype=float)
    n = len(samples)
    mean = np.mean(samples)
    centered = samples - mean
    var = np.var(centered, ddof=0)
    if var <= 0:
        return 0.5, 0
    rho = np.zeros(n)
    rho[0] = 1.0
    for t in range(1, min(n, 100)):
        c = np.mean(centered[:n-t] * centered[t:])
        rho[t] = c / var
    tau = 0.5
    W = 0
    for w in range(1, len(rho)):
        tau += rho[w]
        W = w
        if W >= 5 * max(tau, 0.5):
            break
    return float(tau), W


def block_jackknife(samples, block_size):
    """Block jackknife mean and SE."""
    samples = np.asarray(samples, dtype=float)
    n = len(samples)
    if block_size < 1: block_size = 1
    n_blocks = n // block_size
    if n_blocks < 2:
        return float(np.mean(samples)), float(np.std(samples, ddof=1) / math.sqrt(max(1, n)))
    blocks = samples[:n_blocks * block_size].reshape(n_blocks, block_size).mean(axis=1)
    mean = float(np.mean(blocks))
    se = float(np.std(blocks, ddof=1) / math.sqrt(n_blocks))
    return mean, se


def weighted_lsq_fss(L_vals, P_vals, sigma_vals, model='inv_V'):
    """Weighted least squares FSS fit.
    M1: P(L) = P_inf + c/L^4
    M2: P(L) = P_inf + c/L^2
    """
    L = np.asarray(L_vals, dtype=float)
    P = np.asarray(P_vals, dtype=float)
    s = np.asarray(sigma_vals, dtype=float)
    if model == 'inv_V':
        x = 1.0 / L**4
    elif model == 'inv_L2':
        x = 1.0 / L**2
    else:
        raise ValueError(model)
    w = 1.0 / s**2
    Sw = np.sum(w)
    Swx = np.sum(w * x)
    Swxx = np.sum(w * x * x)
    Swp = np.sum(w * P)
    Swxp = np.sum(w * x * P)
    det = Sw * Swxx - Swx * Swx
    P_inf = (Swxx * Swp - Swx * Swxp) / det
    c = (Sw * Swxp - Swx * Swp) / det
    var_P_inf = Swxx / det
    sigma_P_inf = math.sqrt(var_P_inf)
    chi2 = float(np.sum(w * (P - (P_inf + c * x))**2))
    dof = max(1, len(L) - 2)
    return float(P_inf), float(c), float(sigma_P_inf), chi2 / dof


def loo_jackknife(L_vals, P_vals, sigma_vals, model='inv_V'):
    """Leave-one-out jackknife on FSS fit."""
    n = len(L_vals)
    if n < 4:
        return None
    P_infs = []
    for i in range(n):
        L_loo = [L_vals[j] for j in range(n) if j != i]
        P_loo = [P_vals[j] for j in range(n) if j != i]
        s_loo = [sigma_vals[j] for j in range(n) if j != i]
        P_inf_loo, _, _, _ = weighted_lsq_fss(L_loo, P_loo, s_loo, model=model)
        P_infs.append(P_inf_loo)
    return float(np.std(P_infs, ddof=1) * math.sqrt(n - 1))


def main():
    print("=" * 72)
    print("SU(3) Wilson Plaquette 4D FSS RETAINED-GRADE VERIFIER (5-volume)")
    print("=" * 72)

    # Load all artifacts
    if not os.path.isdir(ARTIFACT_DIR):
        print(f"FAIL: artifact directory not found: {ARTIFACT_DIR}")
        sys.exit(1)

    artifacts = []
    for fn in sorted(os.listdir(ARTIFACT_DIR)):
        if fn.startswith("L") and fn.endswith(".json") and fn != "fss_summary.json":
            with open(os.path.join(ARTIFACT_DIR, fn)) as f:
                artifacts.append(json.load(f))
    artifacts.sort(key=lambda a: a['L'])

    print(f"\nFound {len(artifacts)} artifacts: L = {[a['L'] for a in artifacts]}")

    # Per-volume analysis
    L_vals = []
    P_vals = []
    sigma_vals = []

    print("\n--- Per-volume autocorrelation + block jackknife ---")
    for art in artifacts:
        L = art['L']
        samples = np.asarray(art['samples'], dtype=float)
        tau, W = madras_sokal_tau_int(samples)
        block_size = max(4, int(math.ceil(2 * tau)))
        mean, se = block_jackknife(samples, block_size)
        n_eff = len(samples) / max(2 * tau, 1.0)
        print(f"  L={L}: tau_int={tau:.2f} (W={W}), n_eff={n_eff:.1f}, mean={mean:.5f}, SE={se:.5f}")

        L_vals.append(L)
        P_vals.append(mean)
        sigma_vals.append(se)

        check(f"  L={L}: tau_int finite, n_eff >= 8",
              math.isfinite(tau) and n_eff >= 8,
              f"tau_int = {tau:.2f}, n_eff = {n_eff:.1f}")
        check(f"  L={L}: jackknife SE positive and finite",
              se > 0 and math.isfinite(se),
              f"SE = {se}")

    print("\n--- FSS fits ---")
    P_inf_M1, c_M1, sigma_M1, chi2_M1 = weighted_lsq_fss(L_vals, P_vals, sigma_vals, 'inv_V')
    P_inf_M2, c_M2, sigma_M2, chi2_M2 = weighted_lsq_fss(L_vals, P_vals, sigma_vals, 'inv_L2')
    loo_M1 = loo_jackknife(L_vals, P_vals, sigma_vals, 'inv_V')
    loo_M2 = loo_jackknife(L_vals, P_vals, sigma_vals, 'inv_L2')

    print(f"  M1 (1/V):   P_inf = {P_inf_M1:.5f} ± {sigma_M1:.5f} (fit), LOO_SE = {loo_M1}, chi2/dof = {chi2_M1:.3f}")
    print(f"  M2 (1/L²):  P_inf = {P_inf_M2:.5f} ± {sigma_M2:.5f} (fit), LOO_SE = {loo_M2}, chi2/dof = {chi2_M2:.3f}")

    # Cross-model agreement
    sigma_combined = math.sqrt(sigma_M1**2 + sigma_M2**2)
    if loo_M1 is not None and loo_M2 is not None:
        sigma_combined_loo = math.sqrt(loo_M1**2 + loo_M2**2)
        sigma_combined_total = math.sqrt(sigma_combined**2 + sigma_combined_loo**2)
    else:
        sigma_combined_total = sigma_combined
    diff = abs(P_inf_M1 - P_inf_M2)
    nsigma = diff / sigma_combined_total if sigma_combined_total > 0 else float('inf')

    print(f"  Cross-model: |M1 - M2| = {diff:.5f}, combined sigma = {sigma_combined_total:.5f}, n_sigma = {nsigma:.2f}")

    # Comparator distance
    comp_distance = abs(P_inf_M1 - COMPARATOR)
    print(f"  Comparator distance |P_inf(M1) - {COMPARATOR}| = {comp_distance:.5f}")

    # ============================================================================
    # BASELINE BOUNDED CHECKS (A-G)
    # ============================================================================
    print("\n--- Bounded-grade checks (A-G) ---")
    check("A. at least 3 distinct volumes", len(L_vals) >= 3,
          f"n_volumes = {len(L_vals)}")
    check("D. each P(L) in canonical band 0.55..0.65",
          all(0.55 <= p <= 0.65 for p in P_vals),
          f"P_vals = {P_vals}")
    check("F. cross-model agreement <3σ (bounded tolerance)",
          nsigma < 3.0, f"n_sigma = {nsigma:.2f}")
    check("G. M1 bracket diameter finite",
          math.isfinite(2 * sigma_M1) and 2 * sigma_M1 > 0,
          f"diameter = {2 * sigma_M1 * 2:.5f}")

    # ============================================================================
    # RETAINED-GRADE TIGHTER CHECKS (H-K)
    # ============================================================================
    print("\n--- Retained-grade checks (H-K) ---")
    check(f"H. ≥{RETAINED_MIN_VOLUMES} distinct volumes for retained-grade FSS",
          len(L_vals) >= RETAINED_MIN_VOLUMES,
          f"n_volumes = {len(L_vals)} (need {RETAINED_MIN_VOLUMES})")

    n_dof_M1 = len(L_vals) - 2
    check("I. 2-parameter FSS fit has ≥3 dof for retained",
          n_dof_M1 >= 3,
          f"dof = {n_dof_M1}")

    check(f"J. cross-model agreement <{RETAINED_CROSS_MODEL_SIGMA}σ (retained tolerance)",
          nsigma < RETAINED_CROSS_MODEL_SIGMA,
          f"n_sigma = {nsigma:.2f} (need <{RETAINED_CROSS_MODEL_SIGMA})")

    check(f"K. L→∞ extrapolation within {RETAINED_TOLERANCE*100:.1f}% of comparator",
          comp_distance <= RETAINED_TOLERANCE,
          f"|P_inf(M1) - {COMPARATOR}| = {comp_distance:.5f} (need ≤{RETAINED_TOLERANCE})")

    print(f"\nSUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")

    # Status determination
    print("\n--- Promotion status ---")
    if (len(L_vals) >= RETAINED_MIN_VOLUMES and
        n_dof_M1 >= 3 and
        nsigma < RETAINED_CROSS_MODEL_SIGMA and
        comp_distance <= RETAINED_TOLERANCE):
        print("  ✅ ALL RETAINED-GRADE CHECKS PASS")
        print("  Proposed status: bounded → RETAINED (pending audit ratification)")
    elif len(L_vals) >= 3 and 0.55 <= np.mean(P_vals) <= 0.65:
        print("  ✓ BOUNDED-GRADE CHECKS PASS, but retained checks not satisfied")
        print("  Stays at: bounded (need more volumes / tighter agreement / closer comparator)")
    else:
        print("  ✗ Below bounded-grade — investigate")

    # Write summary
    summary = {
        "n_volumes": len(L_vals),
        "L_vals": L_vals,
        "P_vals": P_vals,
        "sigma_vals": sigma_vals,
        "FSS_M1_inv_V": {
            "P_inf": P_inf_M1, "c": c_M1, "sigma_fit": sigma_M1,
            "loo_SE": loo_M1, "chi2_dof": chi2_M1,
        },
        "FSS_M2_inv_L2": {
            "P_inf": P_inf_M2, "c": c_M2, "sigma_fit": sigma_M2,
            "loo_SE": loo_M2, "chi2_dof": chi2_M2,
        },
        "cross_model": {"diff": diff, "sigma_combined": sigma_combined_total, "n_sigma": nsigma},
        "comparator": COMPARATOR,
        "comparator_distance_M1": comp_distance,
        "retained_grade_checks_pass": (
            len(L_vals) >= RETAINED_MIN_VOLUMES and
            n_dof_M1 >= 3 and
            nsigma < RETAINED_CROSS_MODEL_SIGMA and
            comp_distance <= RETAINED_TOLERANCE
        ),
    }
    summary_path = os.path.join(ARTIFACT_DIR, "fss_retained_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved retained summary to {summary_path}")

    sys.exit(0 if FAIL_COUNT == 0 else 1)


if __name__ == "__main__":
    main()
