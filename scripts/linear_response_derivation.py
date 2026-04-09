#!/usr/bin/env python3
"""Linear-response derivation-adjacent analysis.

Front A target: explain why grown-DAG and dense ER pass while random
k-regular and expander fail at the same nominal avg_deg, or prove that
free_coh cannot be the full answer.

This lane does NOT do another metric search. It tests ONE theoretically
motivated quantity — the **first-moment Kubo predictor** — against the
**measured first-order response** across all 44 families we have
(26 swept + 9 scaffolded + 9 off-scaffold).

Setup:
  1. For each family, compute the free-beam amplitude distribution at
     the detector (no field).
  2. Compute free_cz = centroid of |amp|^2 over detector cells.
  3. Compute weighted_cz = centroid weighted by additional factor
     1/|z_j - z_src| (the known field profile).
  4. First-moment Kubo predictor:
        kubo = weighted_cz - free_cz
     This is the first-moment approximation to d(cz)/ds — it says
     "under a 1/r field at z_src, the centroid shifts toward the
     mass by an amount proportional to how asymmetric the free
     intensity is when weighted by the field profile."
  5. Measured response: delta_z at s = 0.001 (small) from the actual
     battery run. This is the TRUTH d(cz)/ds at first order.

Test: correlation(kubo, measured) across the 44 families. If the
correlation is high AND the signs agree for PASS/FAIL classification,
we have a first-principles predictor (no empirical fit). If it's
weak, it's a no-go at the first-moment level — the derivation needs
to go to second moments or full path-sum expansion.

This is derivation-adjacent because:
  - kubo uses ONLY free-beam amplitudes + known field structure
  - No empirical thresholds or fitted parameters
  - It's the direct first-moment expression from linear response theory
  - If it works: the analytic explanation is "gravity TOWARD ↔ free
    beam amplitude is weighted toward the mass under 1/r"
  - If it doesn't: we have a sharp no-go
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import universality_classifier as uc
import independent_generators_heldout as ind
import global_coherence_off_scaffold as offs

MASS_Z = uc.MASS_Z
S_SMALL = 0.001  # finite-difference epsilon
H = uc.H


def detector_amps_and_positions(amps, pos, NL, PW):
    """Extract detector slice."""
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    det_amps = amps[ds:n]
    det_pos = pos[ds:n]
    return det_amps, det_pos


def free_centroid_z(det_amps, det_pos):
    weights = [abs(a) ** 2 for a in det_amps]
    zs = [p[2] for p in det_pos]
    total = sum(weights)
    if total <= 0:
        return 0.0
    return sum(w * z for w, z in zip(weights, zs)) / total


def kubo_predictor(det_amps, det_pos, z_src):
    """First-moment Kubo-style predictor.

    weighted_cz uses |amp|^2 / |z - z_src| as the effective weight
    (matching the 1/r field profile to first order), then subtracts
    the free centroid.
    """
    w_std = [abs(a) ** 2 for a in det_amps]
    w_field = [abs(a) ** 2 / (abs(p[2] - z_src) + 0.1) for a, p in zip(det_amps, det_pos)]
    zs = [p[2] for p in det_pos]
    T_std = sum(w_std)
    T_field = sum(w_field)
    if T_std <= 0 or T_field <= 0:
        return 0.0, 0.0, 0.0
    cz_free = sum(w * z for w, z in zip(w_std, zs)) / T_std
    cz_weighted = sum(w * z for w, z in zip(w_field, zs)) / T_field
    return cz_free, cz_weighted, (cz_weighted - cz_free)


def measured_response(pos, adj, nmap, NL, PW):
    """Measured linear response = delta_z(s=small) - delta_z(s=0), normalized."""
    # free
    free = ind.prop_beam(pos, adj, nmap, None, uc.K)
    det_free, det_pos = detector_amps_and_positions(free, pos, NL, PW)
    cz_0 = free_centroid_z(det_free, det_pos)
    # with field
    x_src = (NL // 3) * H
    fld = uc.imposed_field(pos, x_src, MASS_Z, S_SMALL)
    g = ind.prop_beam(pos, adj, nmap, fld, uc.K)
    det_g, _ = detector_amps_and_positions(g, pos, NL, PW)
    cz_s = free_centroid_z(det_g, det_pos)
    return (cz_s - cz_0) / S_SMALL


def swept_results():
    results = []
    for fam in uc.make_families():
        pos, adj, nmap = uc.grow(
            fam["seed"], fam["drift"], fam["restore"],
            fam["NL"], fam["PW"], fam["md"],
            mode=fam.get("mode", "dense"),
            anisotropy=fam.get("anisotropy", 1.0),
        )
        try:
            r = uc.battery(fam)
            NL = fam["NL"]
            PW = fam["PW"]
            free = ind.prop_beam(pos, adj, nmap, None, uc.K)
            det_amps, det_pos = detector_amps_and_positions(free, pos, NL, PW)
            cz_free, cz_w, kubo = kubo_predictor(det_amps, det_pos, MASS_Z)
            meas = measured_response(pos, adj, nmap, NL, PW)
            results.append({
                "name": r["name"] + "_swept",
                "group": "swept",
                "pass": r["pass"],
                "measured": meas,
                "kubo": kubo,
                "cz_free": cz_free,
                "cz_weighted": cz_w,
                "free_coh": None,  # filled below if desired
            })
        except Exception as e:
            results.append({"name": fam["name"], "group": "swept", "error": str(e)})
    return results


def scaffolded_indep_results():
    results = []
    for name, builder in ind.make_independent_families():
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            NL = ind.NL
            PW = ind.PW
            free = ind.prop_beam(pos, adj, nmap, None, uc.K)
            det_amps, det_pos = detector_amps_and_positions(free, pos, NL, PW)
            cz_free, cz_w, kubo = kubo_predictor(det_amps, det_pos, MASS_Z)
            meas = measured_response(pos, adj, nmap, NL, PW)
            results.append({
                "name": name + "_scaf",
                "group": "scaffolded",
                "pass": r["pass"],
                "measured": meas,
                "kubo": kubo,
                "cz_free": cz_free,
                "cz_weighted": cz_w,
            })
        except Exception as e:
            results.append({"name": name, "group": "scaffolded", "error": str(e)})
    return results


def offscaffold_results():
    results = []
    for name, builder in offs.make_off_scaffold_families():
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            NL = offs.NL
            PW = offs.PW
            free = ind.prop_beam(pos, adj, nmap, None, uc.K)
            det_amps, det_pos = detector_amps_and_positions(free, pos, NL, PW)
            cz_free, cz_w, kubo = kubo_predictor(det_amps, det_pos, MASS_Z)
            meas = measured_response(pos, adj, nmap, NL, PW)
            results.append({
                "name": name + "_off",
                "group": "off_scaffold",
                "pass": r["pass"],
                "measured": meas,
                "kubo": kubo,
                "cz_free": cz_free,
                "cz_weighted": cz_w,
            })
        except Exception as e:
            results.append({"name": name, "group": "off_scaffold", "error": str(e)})
    return results


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if sxx <= 0 or syy <= 0:
        return 0.0
    return sxy / math.sqrt(sxx * syy)


def main():
    print("=" * 100)
    print("LINEAR-RESPONSE DERIVATION-ADJACENT ANALYSIS")
    print("First-moment Kubo predictor vs measured d(cz)/ds on 44 families")
    print(f"Finite-difference epsilon: s = {S_SMALL}")
    print("=" * 100)

    print("\nA. Computing 26 swept families...")
    swept = swept_results()
    print("\nB. Computing 9 scaffolded independent generators...")
    scaf = scaffolded_indep_results()
    print("\nC. Computing 9 off-scaffold generators...")
    off = offscaffold_results()

    all_results = swept + scaf + off

    print("\n" + "=" * 100)
    print("RESULTS")
    print("=" * 100)
    print(f"{'family':30s} {'group':>12s} {'pass':>5s} {'measured':>12s} {'kubo':>12s} {'cz_free':>10s}")
    print("-" * 100)
    for r in all_results:
        if "error" in r:
            print(f"{r['name']:30s} {r['group']:>12s}  ERROR: {r['error']}")
            continue
        tag = "PASS" if r["pass"] else "FAIL"
        print(f"{r['name']:30s} {r['group']:>12s} {tag:>5s} "
              f"{r['measured']:+12.6f} {r['kubo']:+12.6f} {r['cz_free']:+10.4f}")

    valid = [r for r in all_results if "error" not in r]

    # Overall Pearson correlation
    xs = [r["kubo"] for r in valid]
    ys = [r["measured"] for r in valid]
    r_all = pearson(xs, ys)
    print(f"\nOVERALL correlation(kubo, measured): r = {r_all:.4f}  (N={len(valid)})")

    # By group
    print("\nBY GROUP:")
    for group in ["swept", "scaffolded", "off_scaffold"]:
        rs = [r for r in valid if r["group"] == group]
        if not rs:
            continue
        xs_g = [r["kubo"] for r in rs]
        ys_g = [r["measured"] for r in rs]
        r_g = pearson(xs_g, ys_g)
        print(f"  {group:>15s}: r = {r_g:.4f}  (N={len(rs)})")

    # Sign agreement (for PASS/FAIL classification purposes)
    print("\nSIGN AGREEMENT (kubo predicts measured sign):")
    sign_ok = sum(
        1 for r in valid
        if (r["kubo"] > 0) == (r["measured"] > 0)
    )
    print(f"  {sign_ok}/{len(valid)} = {sign_ok/len(valid):.1%}")

    # Pass classification via kubo > 0
    print("\nPASS CLASSIFICATION (kubo > 1e-4 as a pass predictor):")
    thr = 1e-4
    correct = sum(
        1 for r in valid
        if (r["kubo"] > thr) == r["pass"]
    )
    print(f"  kubo > {thr}: {correct}/{len(valid)} = {correct/len(valid):.1%}")

    # Find best kubo threshold
    candidates = sorted({r["kubo"] for r in valid})
    best = (-1.0, 0.0)
    for thr_c in candidates:
        c = sum(1 for r in valid if (r["kubo"] >= thr_c) == r["pass"])
        acc = c / len(valid)
        if acc > best[0]:
            best = (acc, thr_c)
    print(f"  best kubo threshold: kubo >= {best[1]:.6f}  accuracy {best[0]:.1%}")

    # Compare to measured response as a threshold (trivial upper bound)
    print("\nMEASURED RESPONSE CLASSIFICATION (sanity check upper bound):")
    thr_m = 1e-4
    correct_m = sum(
        1 for r in valid
        if (r["measured"] > thr_m) == r["pass"]
    )
    print(f"  measured > {thr_m}: {correct_m}/{len(valid)} = {correct_m/len(valid):.1%}")

    print("\n" + "=" * 100)
    print("VERDICT")
    print("=" * 100)
    if r_all > 0.85:
        print(f"  STRONG CORRELATION (r={r_all:.3f}) — first-moment Kubo predictor is")
        print("  quantitatively tight with the measured linear response.")
        print("  The analytic derivation target is clear: the package holds iff")
        print("  the free-beam amplitude distribution, weighted by 1/|z - z_src|,")
        print("  has its centroid shifted toward the mass position.")
    elif r_all > 0.5:
        print(f"  MODERATE CORRELATION (r={r_all:.3f}) — the first-moment Kubo")
        print("  predictor partially captures the measured response. Derivation is")
        print("  directionally right but first moment is insufficient; need second")
        print("  moments or path-sum expansion.")
    else:
        print(f"  WEAK CORRELATION (r={r_all:.3f}) — the first-moment Kubo predictor")
        print("  does NOT match the measured linear response at first order.")
        print("  NO-GO at the first-moment level: the package is not determined by")
        print("  a simple 1/r-weighted centroid of the free beam. The derivation")
        print("  must go beyond first-moment linear response.")


if __name__ == "__main__":
    main()
