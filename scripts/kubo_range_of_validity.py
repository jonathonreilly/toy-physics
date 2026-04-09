#!/usr/bin/env python3
"""Range of validity of the first-order Kubo prediction.

The true first-order Kubo expression (linear_response_true_kubo.py)
gives d(cz)/ds at s = 0 with r = 0.97 correlation to the measured
finite-difference at s = 0.001.

First-order linear response implies delta_z(s) ≈ kubo_true · s,
which means |delta_z| ∝ s^1.0, i.e., F~M = 1 EXACTLY by construction.
The battery measures F~M by log-log slope across s in {0.001, 0.002,
0.004, 0.008}. If the linear regime holds up to s = 0.008, the
measured F~M should be ≈ 1.0 on Kubo-matching families.

This lane tests whether:
  1. For families with good Kubo agreement at s = 0.001, the measured
     delta_z(s) stays linear in s across all four battery strengths.
  2. The per-family deviation from linearity correlates with kubo_true.
  3. The swept-family F~M values from the battery are consistent with
     pure first-order Kubo (F~M ≈ 1) on the Kubo-matching subset.

Decisive observable: for each family, compute
   predicted delta_z(s) = kubo_true * s
   measured delta_z(s)  at four s values
   linearity ratio = measured(s) / (kubo_true * s)
If the ratio stays near 1.0 across all s, linear response holds and
F~M = 1 is derived from first-order Kubo.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import universality_classifier as uc
import independent_generators_heldout as ind
import global_coherence_off_scaffold as offs
from linear_response_true_kubo import true_kubo_dcz_ds

MASS_Z = uc.MASS_Z
H = uc.H
K_PHASE = uc.K
STRENGTHS = [0.001, 0.002, 0.004, 0.008]


def measured_cz_at(pos, adj, nmap, NL, PW, s):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds_idx = n - npl

    def cz_from_amps(amps):
        weights = [abs(amps[i]) ** 2 for i in range(ds_idx, n)]
        zs = [pos[i][2] for i in range(ds_idx, n)]
        total = sum(weights)
        if total <= 0:
            return 0.0
        return sum(w * z for w, z in zip(weights, zs)) / total

    if s == 0.0:
        amps = ind.prop_beam(pos, adj, nmap, None, K_PHASE)
    else:
        x_src = (NL // 3) * H
        fld = uc.imposed_field(pos, x_src, MASS_Z, s)
        amps = ind.prop_beam(pos, adj, nmap, fld, K_PHASE)
    return cz_from_amps(amps)


def fit_fm(strengths, abs_deltas):
    """Log-log slope of |delta_z| vs s."""
    valid = [(s, d) for s, d in zip(strengths, abs_deltas) if d > 1e-15]
    if len(valid) < 2:
        return float("nan")
    lx = [math.log(s) for s, _ in valid]
    ly = [math.log(d) for _, d in valid]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx if sxx > 0 else float("nan")


def analyze_family(pos, adj, nmap, NL, PW):
    """Compute kubo_true, measured cz at multiple s, F~M."""
    kubo, cz_free = true_kubo_dcz_ds(pos, adj, nmap, NL, PW)
    cz_0 = measured_cz_at(pos, adj, nmap, NL, PW, 0.0)
    deltas = []
    for s in STRENGTHS:
        cz_s = measured_cz_at(pos, adj, nmap, NL, PW, s)
        deltas.append(cz_s - cz_0)
    abs_deltas = [abs(d) for d in deltas]
    fm = fit_fm(STRENGTHS, abs_deltas)
    # linearity ratios: measured(s) / (kubo_true * s)
    ratios = []
    for s, d in zip(STRENGTHS, deltas):
        pred = kubo * s
        if abs(pred) > 1e-12:
            ratios.append(d / pred)
        else:
            ratios.append(float("nan"))
    return {
        "kubo": kubo,
        "cz_free": cz_free,
        "deltas": deltas,
        "fm": fm,
        "ratios": ratios,
    }


def collect_all():
    rows = []
    for fam in uc.make_families():
        try:
            pos, adj, nmap = uc.grow(
                fam["seed"], fam["drift"], fam["restore"],
                fam["NL"], fam["PW"], fam["md"],
                mode=fam.get("mode", "dense"),
                anisotropy=fam.get("anisotropy", 1.0),
            )
            r = uc.battery(fam)
            NL = fam["NL"]
            PW = fam["PW"]
            info = analyze_family(pos, adj, nmap, NL, PW)
            rows.append({
                "name": r["name"],
                "group": "swept",
                "pass": r["pass"],
                **info,
            })
        except Exception as e:
            rows.append({"name": fam.get("name", "?"), "group": "swept", "error": str(e)})

    for name, builder in ind.make_independent_families():
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            info = analyze_family(pos, adj, nmap, ind.NL, ind.PW)
            rows.append({
                "name": name,
                "group": "scaffolded",
                "pass": r["pass"],
                **info,
            })
        except Exception as e:
            rows.append({"name": name, "group": "scaffolded", "error": str(e)})

    for name, builder in offs.make_off_scaffold_families():
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            info = analyze_family(pos, adj, nmap, offs.NL, offs.PW)
            rows.append({
                "name": name,
                "group": "off_scaffold",
                "pass": r["pass"],
                **info,
            })
        except Exception as e:
            rows.append({"name": name, "group": "off_scaffold", "error": str(e)})

    return rows


def main():
    print("=" * 100)
    print("KUBO RANGE OF VALIDITY — does the first-order linear prediction hold up to s = 0.008?")
    print("Predicted: delta_z(s) = kubo_true * s  (=> F~M = 1 exactly)")
    print("Measured:  delta_z(s) at s in {0.001, 0.002, 0.004, 0.008}")
    print("Test: measured / predicted ratio — near 1.0 means linear regime holds")
    print("=" * 100)

    rows = collect_all()
    valid = [r for r in rows if "error" not in r and abs(r["kubo"]) > 1e-6]

    print(f"\n{'family':30s} {'group':>12s} {'pass':>5s} {'kubo':>10s} {'F~M':>7s}"
          f" {'r@0.001':>8s} {'r@0.002':>8s} {'r@0.004':>8s} {'r@0.008':>8s}")
    print("-" * 110)
    for r in valid:
        ratios = r["ratios"]
        rs = [f"{x:8.3f}" if not math.isnan(x) else "   nan  " for x in ratios]
        tag = "PASS" if r["pass"] else "FAIL"
        print(f"{r['name']:30s} {r['group']:>12s} {tag:>5s} {r['kubo']:+10.3f} {r['fm']:7.3f}"
              f" {rs[0]} {rs[1]} {rs[2]} {rs[3]}")

    # Summary: how close is F~M to 1 for Kubo-matching families?
    print("\nF~M DISTRIBUTION by group (Kubo-matching families only):")
    for group in ["swept", "scaffolded", "off_scaffold"]:
        rs = [r for r in valid if r["group"] == group and not math.isnan(r["fm"])]
        if not rs:
            continue
        fms = [r["fm"] for r in rs]
        mean_fm = sum(fms) / len(fms)
        dev_fm = [abs(f - 1.0) for f in fms]
        mean_dev = sum(dev_fm) / len(dev_fm)
        print(f"  {group:>15s}: mean F~M = {mean_fm:.4f}  "
              f"mean |F~M - 1| = {mean_dev:.4f}  (N={len(rs)})")

    # Linearity at each s (median ratio)
    print("\nMEDIAN LINEARITY RATIO (measured(s) / (kubo_true * s)) at each s:")
    for i, s in enumerate(STRENGTHS):
        ratios_at_s = [r["ratios"][i] for r in valid if not math.isnan(r["ratios"][i])]
        if not ratios_at_s:
            continue
        ratios_at_s.sort()
        median = ratios_at_s[len(ratios_at_s) // 2]
        mean_r = sum(ratios_at_s) / len(ratios_at_s)
        print(f"  s = {s:.4f}: median ratio = {median:.4f}  mean = {mean_r:.4f}  (N={len(ratios_at_s)})")

    # ========================================================================
    # INDEPENDENT SUBSET 1: linearity-regime families (no F~M label used)
    # Criterion: max |ratio - 1| across all four battery strengths < 0.10
    # This selects families where first-order linear response actually dominates
    # ========================================================================
    print("\nINDEPENDENT SUBSET 1 — LINEARITY-REGIME (|ratio-1|<0.10 at all four s)")
    print("(criterion uses ONLY measured(s) vs kubo_true*s; no F~M label involved)")
    linear_regime = []
    for r in valid:
        ratios = r["ratios"]
        if any(math.isnan(x) for x in ratios):
            continue
        max_dev = max(abs(x - 1.0) for x in ratios)
        if max_dev < 0.10:
            linear_regime.append(r)
    print(f"  N = {len(linear_regime)} / {len(valid)}")
    if linear_regime:
        fms = [r["fm"] for r in linear_regime if not math.isnan(r["fm"])]
        if fms:
            dev_fm = [abs(f - 1.0) for f in fms]
            print(f"  measured F~M on this subset:")
            print(f"    mean F~M       = {sum(fms)/len(fms):.4f}")
            print(f"    mean |F~M - 1| = {sum(dev_fm)/len(dev_fm):.4f}")
            print(f"    max  |F~M - 1| = {max(dev_fm):.4f}")
            print(f"    all in band    = {all(d < 0.10 for d in dev_fm)}")
        # how many of these are battery PASS, FAIL?
        n_pass_in_linear = sum(1 for r in linear_regime if r["pass"])
        n_fail_in_linear = len(linear_regime) - n_pass_in_linear
        print(f"  battery breakdown: PASS {n_pass_in_linear}, FAIL {n_fail_in_linear}")

    # ========================================================================
    # INDEPENDENT SUBSET 2: sign-agreement families (no F~M label used)
    # Criterion: kubo_true and measured at s=0.001 both nonzero AND same sign
    # ========================================================================
    print("\nINDEPENDENT SUBSET 2 — SIGN-AGREEMENT (kubo & measured both nonzero, same sign)")
    print("(criterion uses ONLY kubo_true and measured signs; no F~M label involved)")
    sign_agree = []
    for r in valid:
        if abs(r["kubo"]) < 1e-6:
            continue
        d = r["deltas"][0]  # measured at s=0.001
        if abs(d) < 1e-9:
            continue
        if (r["kubo"] > 0) == (d > 0):
            sign_agree.append(r)
    print(f"  N = {len(sign_agree)} / {len(valid)}")
    if sign_agree:
        fms = [r["fm"] for r in sign_agree if not math.isnan(r["fm"])]
        if fms:
            dev_fm = [abs(f - 1.0) for f in fms]
            print(f"  measured F~M on this subset:")
            print(f"    mean F~M       = {sum(fms)/len(fms):.4f}")
            print(f"    mean |F~M - 1| = {sum(dev_fm)/len(dev_fm):.4f}")
            print(f"    max  |F~M - 1| = {max(dev_fm):.4f}")
            n_in_band = sum(1 for d in dev_fm if d < 0.10)
            print(f"    in 0.10 band  = {n_in_band}/{len(dev_fm)}")
        n_pass_in_sa = sum(1 for r in sign_agree if r["pass"])
        n_fail_in_sa = len(sign_agree) - n_pass_in_sa
        print(f"  battery breakdown: PASS {n_pass_in_sa}, FAIL {n_fail_in_sa}")

    # ========================================================================
    # SANITY (DEPENDENT on F~M label, kept for transparency only — DO NOT cite as independent)
    # ========================================================================
    print("\nSANITY (DEPENDENT — battery PASS subset uses |F~M-1|<0.10 by definition)")
    print("(this is circular and is reported only for cross-checking with the independent subsets)")
    passing = [r for r in valid if r["pass"] and not math.isnan(r["fm"])]
    if passing:
        fms = [r["fm"] for r in passing]
        dev_fm = [abs(f - 1.0) for f in fms]
        print(f"  N = {len(passing)}")
        print(f"  mean F~M = {sum(fms)/len(fms):.4f}  (TAUTOLOGICAL: PASS already requires |F~M-1|<0.10)")
        print(f"  mean |F~M - 1| = {sum(dev_fm)/len(dev_fm):.4f}")

    print("\n" + "=" * 100)
    print("VERDICT (independent subsets only)")
    print("=" * 100)
    if linear_regime:
        fms_lr = [r["fm"] for r in linear_regime if not math.isnan(r["fm"])]
        if fms_lr:
            mean_dev_lr = sum(abs(f - 1.0) for f in fms_lr) / len(fms_lr)
            in_band_lr = sum(1 for f in fms_lr if abs(f - 1.0) < 0.10)
            print(f"  Linearity-regime subset (independent of F~M): N = {len(linear_regime)}")
            print(f"    mean |F~M - 1| = {mean_dev_lr:.4f}")
            print(f"    in band        = {in_band_lr}/{len(fms_lr)}")
            if mean_dev_lr < 0.05 and in_band_lr == len(fms_lr):
                print("    STRONG — F~M ≈ 1 holds on the linearity-regime subset selected without")
                print("    the F~M label. First-order Kubo derives F~M = 1 in the linear regime.")
            elif mean_dev_lr < 0.10:
                print("    MODERATE — F~M close to 1 in the linear-regime subset.")
            else:
                print("    NEGATIVE — even in the linearity-regime subset, F~M drifts from 1.")


if __name__ == "__main__":
    main()
