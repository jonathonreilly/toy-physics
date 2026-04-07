#!/usr/bin/env python3
"""3rd predictor: local per-node Z2 asymmetry.

The independent-generators lane gave a NEGATIVE result: the rule
(avg_deg >= 10.42) AND (reach_frac >= 0.86) failed to generalize from
the grown-DAG family to genuinely different generators (44.4%
pre-committed, 66.7% rule). The honest hypothesis from that result:

> "Random k-regular at the same nominal avg_deg can have global z_sym
>  near zero (averaged over many random picks) but each individual node
>  can have nonzero local z-asymmetry. The neighbor-square stencil has
>  local z_sym = 0 for every node by construction. The required
>  predictor is statistical Z2 symmetry under dense random sampling,
>  i.e. the variance of node-level dz, not just the mean."

This lane builds that 3rd predictor (`local_z_asym` = mean over nodes of
|sum(dz over outgoing edges) / sum(|dz| over outgoing edges)|) and
asks: does adding it to the classifier search space close the
cross-generator generalization gap?

The classifier is **fitted only on the 26 swept set** and **applied
without refit** to the 9 independent generators.

Decisive metric:
- Old rule (no local_z_asym): 6/9 cross-generator accuracy
- New best 3-property rule: ?/9 cross-generator accuracy

If the new rule materially improves cross-generator accuracy without
overfitting in-sample, the classifier program is alive. If it does
not, the classifier program is exhausted on this generator family
and the next move is matter/inertial closure or analytic derivation.
"""

from __future__ import annotations

import math
import sys
import os

# Reuse all generators, helpers, and battery from the independent-generators lane
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import independent_generators_heldout as ind
import universality_classifier as uc


def local_z_asym(pos, adj):
    """Mean over source nodes of |sum(dz_out)| / sum(|dz_out|).

    For a node with all outgoing edges Z2-symmetric in z (e.g., the
    neighbor square stencil), this is 0. For random k-regular, it is
    distributed around 0 with variance ~ 1/sqrt(k). For asymmetric
    stencils, it is large.
    """
    total = 0.0
    n_nodes = 0
    for i, nbs in adj.items():
        if not nbs:
            continue
        zi = pos[i][2]
        sum_dz = 0.0
        sum_abs = 0.0
        for j in nbs:
            dz = pos[j][2] - zi
            sum_dz += dz
            sum_abs += abs(dz)
        if sum_abs > 0:
            total += abs(sum_dz) / sum_abs
            n_nodes += 1
    return total / max(n_nodes, 1)


def annotate(result, pos, adj):
    """Add local_z_asym to a battery result row."""
    result["local_z_asym"] = local_z_asym(pos, adj)
    return result


def fit_3prop_classifier(results, props=("avg_deg", "z_sym", "fill", "reach_frac", "local_z_asym")):
    """Search the best 3-property AND classifier on the given results."""
    rs = [r for r in results if "error" not in r]
    if not rs:
        return None
    best = (-1.0,) + ("",) * 9
    for pa in props:
        va_set = sorted({r[pa] for r in rs})
        for ta in va_set:
            for da in (">=", "<="):
                for pb in props:
                    if pb == pa:
                        continue
                    vb_set = sorted({r[pb] for r in rs})
                    for tb in vb_set:
                        for db in (">=", "<="):
                            for pc in props:
                                if pc in (pa, pb):
                                    continue
                                vc_set = sorted({r[pc] for r in rs})
                                for tc in vc_set:
                                    for dc in (">=", "<="):
                                        correct = 0
                                        for r in rs:
                                            ok_a = (r[pa] >= ta) if da == ">=" else (r[pa] <= ta)
                                            ok_b = (r[pb] >= tb) if db == ">=" else (r[pb] <= tb)
                                            ok_c = (r[pc] >= tc) if dc == ">=" else (r[pc] <= tc)
                                            if (ok_a and ok_b and ok_c) == r["pass"]:
                                                correct += 1
                                        acc = correct / len(rs)
                                        if acc > best[0]:
                                            best = (acc, pa, da, ta, pb, db, tb, pc, dc, tc)
    return best


def apply_3prop(r, rule):
    if rule is None:
        return False
    _, pa, da, ta, pb, db, tb, pc, dc, tc = rule
    ok_a = (r[pa] >= ta) if da == ">=" else (r[pa] <= ta)
    ok_b = (r[pb] >= tb) if db == ">=" else (r[pb] <= tb)
    ok_c = (r[pc] >= tc) if dc == ">=" else (r[pc] <= tc)
    return ok_a and ok_b and ok_c


def main():
    print("=" * 100)
    print("LOCAL Z-ASYM PREDICTOR — 3-PROPERTY CLASSIFIER, CROSS-GENERATOR HELD-OUT")
    print("Tests whether adding local_z_asym closes the cross-generator gap")
    print("Classifier fitted ONLY on 26 swept families; applied WITHOUT REFIT to 9 independent")
    print("=" * 100)

    # === A. Re-measure the 26 swept grown-DAG families ===
    print("\nA. Re-measuring 26 swept grown-DAG families with local_z_asym...")
    swept_families = uc.make_families()
    swept_results = []
    for i, fam in enumerate(swept_families, 1):
        try:
            r = uc.battery(fam)
            # rebuild the geometry to compute local_z_asym
            pos, adj, nmap = uc.grow(
                fam["seed"], fam["drift"], fam["restore"],
                fam["NL"], fam["PW"], fam["md"],
                mode=fam.get("mode", "dense"),
                anisotropy=fam.get("anisotropy", 1.0),
            )
            annotate(r, pos, adj)
            swept_results.append(r)
            print(f"  [{i:2d}/{len(swept_families)}] {r['name']:25s}  "
                  f"local_z_asym={r['local_z_asym']:.4f}  "
                  f"{'PASS' if r['pass'] else 'FAIL'}")
        except Exception as e:
            print(f"  [{i:2d}/{len(swept_families)}] {fam['name']:25s}  ERROR: {e}")

    # === B. Re-measure the 9 independent generators ===
    print("\nB. Re-measuring 9 independent generators with local_z_asym...")
    indep = ind.make_independent_families()
    indep_results = []
    for i, (name, builder) in enumerate(indep, 1):
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            annotate(r, pos, adj)
            indep_results.append(r)
            print(f"  [{i}/9] {name:22s}  local_z_asym={r['local_z_asym']:.4f}  "
                  f"{'PASS' if r['pass'] else 'FAIL'}")
        except Exception as e:
            print(f"  [{i}/9] {name:22s}  ERROR: {e}")

    # === C. Local z-asym distribution by group ===
    print("\nC. local_z_asym distribution")
    print(f"  {'group':>30s}  {'min':>8s} {'mean':>8s} {'max':>8s}")
    for label, rs in [
        ("swept PASS (grown-DAG, pass)", [r for r in swept_results if r["pass"]]),
        ("swept FAIL (grown-DAG, fail)", [r for r in swept_results if not r["pass"]]),
        ("indep PASS (cross-gen, pass)", [r for r in indep_results if r["pass"]]),
        ("indep FAIL (cross-gen, fail)", [r for r in indep_results if not r["pass"]]),
    ]:
        if not rs:
            print(f"  {label:>30s}  (empty)")
            continue
        vals = [r["local_z_asym"] for r in rs]
        print(f"  {label:>30s}  {min(vals):8.4f} {sum(vals)/len(vals):8.4f} {max(vals):8.4f}")

    # === D. Fit 3-property classifier on the 26 swept set ONLY ===
    print("\nD. Fitting 3-property AND classifier on 26 swept set ONLY")
    rule = fit_3prop_classifier(swept_results)
    if rule is None:
        print("  no valid fit")
        return
    acc, pa, da, ta, pb, db, tb, pc, dc, tc = rule
    print(f"  best 3-property rule:")
    print(f"    ({pa} {da} {ta:.4f}) AND ({pb} {db} {tb:.4f}) AND ({pc} {dc} {tc:.4f})")
    print(f"  in-sample accuracy on 26 swept: {acc:.1%}")

    # === E. Apply WITHOUT REFIT to 9 independent generators ===
    print("\nE. Applying 3-property rule WITHOUT REFIT to 9 independent generators")
    print(f"  {'family':22s} {'actual':>8s} {'rule':>6s} {'agree':>7s}")
    rule_correct = 0
    n_eval = 0
    for r in indep_results:
        if "error" in r:
            continue
        n_eval += 1
        rule_pred = apply_3prop(r, rule)
        agree = (rule_pred == r["pass"])
        if agree:
            rule_correct += 1
        print(f"  {r['name']:22s} {str(r['pass']):>8s} {str(rule_pred):>6s} "
              f"{('OK' if agree else 'MISS'):>7s}")
    cross_acc = rule_correct / max(n_eval, 1)
    print(f"\n  cross-generator (no refit): {rule_correct}/{n_eval} = {cross_acc:.1%}")

    # === F. Compare to old 2-property rule ===
    print("\nF. COMPARISON to old 2-property rule (avg_deg >= 10.42 AND reach_frac >= 0.86)")
    old_correct = 0
    for r in indep_results:
        if "error" in r:
            continue
        ok_a = r["avg_deg"] >= 10.415
        ok_b = r["reach_frac"] >= 0.859
        old_pred = ok_a and ok_b
        if old_pred == r["pass"]:
            old_correct += 1
    old_acc = old_correct / max(n_eval, 1)
    print(f"  old 2-property cross-generator: {old_correct}/{n_eval} = {old_acc:.1%}")
    print(f"  new 3-property cross-generator: {rule_correct}/{n_eval} = {cross_acc:.1%}")

    # === G. Verdict ===
    print("\nG. VERDICT")
    if cross_acc > old_acc + 0.10:
        print(f"  IMPROVED — adding local_z_asym moves cross-generator from "
              f"{old_acc:.0%} to {cross_acc:.0%}")
        print("  classifier program is alive with a 3-property rule")
    elif cross_acc >= old_acc:
        print(f"  MARGINAL — cross-generator {old_acc:.0%} -> {cross_acc:.0%}")
        print("  local_z_asym does not materially help; the classifier program is")
        print("  empirical-only on this generator family")
    else:
        print(f"  WORSE — cross-generator dropped from {old_acc:.0%} to {cross_acc:.0%}")
        print("  the new predictor overfits in-sample and degrades generalization")
        print("  the classifier program is exhausted; move to matter or analytic next")


if __name__ == "__main__":
    main()
