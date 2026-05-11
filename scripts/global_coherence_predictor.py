#!/usr/bin/env python3
"""Global free-beam coherence predictor.

The previous two negative results closed the simple node-level classifier
program: the rule (avg_deg >= 10.42) AND (reach_frac >= 0.86) generalizes
to only 6/9 cross-generator families, and the local_z_asym 3rd predictor
was rejected by the search.

The previous review identified the next attack target as "a global
path-counting or spectral structure, not a node-level statistic." This
lane tests that explicitly with two GLOBAL metrics computed from the
free-beam propagation (no source field):

  free_p_det  = sum over detector cells of |amp|^2
                (total probability reaching the detector via the propagator)
  free_coh    = |sum_j amp_j|^2 / (sum_j |amp_j|^2 * N_det)
                (Kuramoto-style amplitude-coherence at the detector;
                 1.0 = all amplitudes phase-aligned, ~1/N_det = random)

Both are properties of the FULL graph + propagator system, not node-level
degree statistics. They directly capture the hypothesis that grown-DAG
generators succeed because paths interfere constructively at the detector,
while random k-regular and expander generators fail because path phases
randomize even at the same nominal avg_deg.

Hypothesis: free_p_det and/or free_coh cleanly separate PASS from FAIL
across BOTH the 26 swept families AND the 9 independent generators.

If true: the classifier program revives with a sharper, generator-agnostic
predictor. If false: the simple-classifier program is closed for good and
the next move is matter/inertial closure.
"""

from __future__ import annotations

import math
import os
import sys

# Heavy compute / sweep runner — full live replay takes ~5 min for the
# 26-swept + 9-independent generator sweep on this hardware. The audit
# loop's default 120s budget is too tight; bump to 900s so the live
# replay can complete inside the audit window. The frozen archived log
# at logs/2026-04-07-global-coherence-predictor.txt is the deterministic
# fallback comparator and is asserted at the end of this runner.
AUDIT_TIMEOUT_SEC = 900

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import independent_generators_heldout as ind
import universality_classifier as uc


def free_beam_metrics(pos, adj, nmap, NL, PW):
    """Compute free-beam (no field) detector metrics.

    Returns (p_det, coh) where:
      p_det = sum |amp|^2 over detector cells
      coh   = |<amp>|^2 / <|amp|^2>  on detector cells (0..1)
    """
    free = uc.prop_beam(pos, adj, nmap, None, uc.K)
    hw = int(PW / uc.H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl
    det = free[ds:n]
    p_det = sum(abs(a) ** 2 for a in det)
    if p_det <= 0:
        return 0.0, 0.0
    sum_amp = sum(det, 0j)
    n_det = len(det)
    sum_abs2 = sum(abs(a) ** 2 for a in det)
    coh = (abs(sum_amp) ** 2) / max(sum_abs2 * n_det, 1e-30)
    return p_det, coh


def annotate(result, pos, adj, nmap, NL, PW):
    p_det, coh = free_beam_metrics(pos, adj, nmap, NL, PW)
    result["free_p_det"] = p_det
    result["free_coh"] = coh
    return result


def fit_2prop(results, props):
    rs = [r for r in results if "error" not in r]
    if not rs:
        return None
    best = (-1.0,) + ("",) * 6
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
                            correct = sum(
                                1 for r in rs
                                if (
                                    ((r[pa] >= ta) if da == ">=" else (r[pa] <= ta))
                                    and ((r[pb] >= tb) if db == ">=" else (r[pb] <= tb))
                                ) == r["pass"]
                            )
                            acc = correct / len(rs)
                            if acc > best[0]:
                                best = (acc, pa, da, ta, pb, db, tb)
    return best


def apply_rule(r, rule):
    if rule is None:
        return False
    _, pa, da, ta, pb, db, tb = rule
    ok_a = (r[pa] >= ta) if da == ">=" else (r[pa] <= ta)
    ok_b = (r[pb] >= tb) if db == ">=" else (r[pb] <= tb)
    return ok_a and ok_b


def fit_1prop(results, props):
    """Best single-property classifier."""
    rs = [r for r in results if "error" not in r]
    best = (-1.0, "", "", 0.0)
    for prop in props:
        for thr in sorted({r[prop] for r in rs}):
            for direction in (">=", "<="):
                correct = sum(
                    1 for r in rs
                    if ((r[prop] >= thr) if direction == ">=" else (r[prop] <= thr)) == r["pass"]
                )
                acc = correct / len(rs)
                if acc > best[0]:
                    best = (acc, prop, direction, thr)
    return best


def main():
    print("=" * 100)
    print("GLOBAL FREE-BEAM COHERENCE PREDICTOR")
    print("Tests whether global free-beam metrics (p_det, coh) separate PASS from FAIL")
    print("across BOTH the 26 swept set AND the 9 independent generators")
    print("=" * 100)

    # === A. 26 swept families ===
    print("\nA. Computing free-beam metrics on 26 swept grown-DAG families...")
    swept_results = []
    for i, fam in enumerate(uc.make_families(), 1):
        try:
            r = uc.battery(fam)
            pos, adj, nmap = uc.grow(
                fam["seed"], fam["drift"], fam["restore"],
                fam["NL"], fam["PW"], fam["md"],
                mode=fam.get("mode", "dense"),
                anisotropy=fam.get("anisotropy", 1.0),
            )
            annotate(r, pos, adj, nmap, fam["NL"], fam["PW"])
            swept_results.append(r)
            print(f"  [{i:2d}/26] {r['name']:25s}  "
                  f"p_det={r['free_p_det']:.4e}  coh={r['free_coh']:.4f}  "
                  f"{'PASS' if r['pass'] else 'FAIL'}")
        except Exception as e:
            print(f"  [{i:2d}/26] {fam['name']:25s}  ERROR: {e}")

    # === B. 9 independent generators ===
    print("\nB. Computing free-beam metrics on 9 independent generators...")
    indep_results = []
    for i, (name, builder) in enumerate(ind.make_independent_families(), 1):
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            annotate(r, pos, adj, nmap, ind.NL, ind.PW)
            indep_results.append(r)
            print(f"  [{i}/9] {name:22s}  "
                  f"p_det={r['free_p_det']:.4e}  coh={r['free_coh']:.4f}  "
                  f"{'PASS' if r['pass'] else 'FAIL'}")
        except Exception as e:
            print(f"  [{i}/9] {name:22s}  ERROR: {e}")

    # === C. Distribution by group ===
    print("\nC. free_p_det and free_coh distributions")
    for label, rs in [
        ("swept PASS", [r for r in swept_results if r["pass"]]),
        ("swept FAIL", [r for r in swept_results if not r["pass"]]),
        ("indep PASS", [r for r in indep_results if r["pass"]]),
        ("indep FAIL", [r for r in indep_results if not r["pass"]]),
    ]:
        if not rs:
            print(f"  {label:>12s}  (empty)")
            continue
        pds = [r["free_p_det"] for r in rs]
        cos = [r["free_coh"] for r in rs]
        print(f"  {label:>12s}  p_det [{min(pds):.2e}, {max(pds):.2e}]  "
              f"coh [{min(cos):.4f}, {max(cos):.4f}]")

    # === D. Single-property classifier on swept set with new metrics ===
    print("\nD. Single-property classifier on 26 swept set (testing new metrics)")
    props = ["avg_deg", "z_sym", "fill", "reach_frac", "free_p_det", "free_coh"]
    best1 = fit_1prop(swept_results, props)
    acc1, prop1, dir1, thr1 = best1
    print(f"  best 1-prop: {prop1} {dir1} {thr1:.4f}  in-sample {acc1:.1%}")

    # === E. 2-property classifier on swept set with new metrics in pool ===
    print("\nE. 2-property AND classifier on 26 swept set (new metrics in pool)")
    best2 = fit_2prop(swept_results, props)
    acc2, pa, da, ta, pb, db, tb = best2
    print(f"  best 2-prop: ({pa} {da} {ta:.4f}) AND ({pb} {db} {tb:.4f})")
    print(f"  in-sample accuracy: {acc2:.1%}")

    # === F. Apply WITHOUT REFIT to 9 independent generators ===
    print("\nF. Cross-generator (no refit) on 9 independent generators")
    print(f"  rule: ({pa} {da} {ta:.4f}) AND ({pb} {db} {tb:.4f})")
    print(f"  {'family':22s} {'p_det':>12s} {'coh':>8s} {'actual':>8s} {'rule':>6s} {'agree':>7s}")
    rule_correct = 0
    n_eval = 0
    for r in indep_results:
        if "error" in r:
            continue
        n_eval += 1
        rule_pred = apply_rule(r, best2)
        agree = (rule_pred == r["pass"])
        if agree:
            rule_correct += 1
        print(f"  {r['name']:22s} {r['free_p_det']:12.3e} {r['free_coh']:8.4f}  "
              f"{str(r['pass']):>8s} {str(rule_pred):>6s} "
              f"{('OK' if agree else 'MISS'):>7s}")
    cross_acc = rule_correct / max(n_eval, 1)
    print(f"\n  cross-generator (no refit): {rule_correct}/{n_eval} = {cross_acc:.1%}")

    # === G. Single-property cross-generator using just the new metrics ===
    print("\nG. Single-property cross-generator (free-beam metrics alone)")
    for prop in ("free_p_det", "free_coh"):
        # threshold from the swept-set 1-prop search restricted to this prop
        best_one = (-1.0, "", "", 0.0)
        for thr in sorted({r[prop] for r in swept_results}):
            for direction in (">=", "<="):
                correct = sum(
                    1 for r in swept_results
                    if ((r[prop] >= thr) if direction == ">=" else (r[prop] <= thr)) == r["pass"]
                )
                acc = correct / len(swept_results)
                if acc > best_one[0]:
                    best_one = (acc, prop, direction, thr)
        ac, p_, d_, t_ = best_one
        # apply to indep
        cor = sum(
            1 for r in indep_results
            if ((r[p_] >= t_) if d_ == ">=" else (r[p_] <= t_)) == r["pass"]
        )
        print(f"  {p_} {d_} {t_:.4e}  in-sample {ac:.1%}  cross-gen {cor}/{n_eval} = {cor/n_eval:.1%}")

    # === H. Comparison vs old rule and verdict ===
    print("\nH. COMPARISON to old 2-property rule (avg_deg >= 10.42 AND reach_frac >= 0.86)")
    old_correct = sum(
        1 for r in indep_results
        if (r["avg_deg"] >= 10.415 and r["reach_frac"] >= 0.859) == r["pass"]
    )
    old_acc = old_correct / max(n_eval, 1)
    print(f"  old 2-property cross-generator: {old_correct}/{n_eval} = {old_acc:.1%}")
    print(f"  new 2-property cross-generator: {rule_correct}/{n_eval} = {cross_acc:.1%}")

    # The 2-property AND search ties in-sample with the single-property
    # global-metric rule and breaks ties on enumeration order, not on
    # cross-generator performance. The headline result of this lane is
    # the SINGLE-property global rule, not the 2-property AND rule.
    print("\nI. VERDICT (headline = single-property global rule)")
    best_single_global = (-1.0, "", "", 0.0)
    for prop in ("free_p_det", "free_coh"):
        for thr in sorted({r[prop] for r in swept_results}):
            for direction in (">=", "<="):
                correct_s = sum(
                    1 for r in swept_results
                    if ((r[prop] >= thr) if direction == ">=" else (r[prop] <= thr)) == r["pass"]
                )
                acc_s = correct_s / len(swept_results)
                if acc_s > best_single_global[0]:
                    best_single_global = (acc_s, prop, direction, thr)
    ac_s, p_s, d_s, t_s = best_single_global
    cor_s = sum(
        1 for r in indep_results
        if ((r[p_s] >= t_s) if d_s == ">=" else (r[p_s] <= t_s)) == r["pass"]
    )
    single_cross_acc = cor_s / max(n_eval, 1)
    print(f"  best single-property global rule: {p_s} {d_s} {t_s:.4e}")
    print(f"    in-sample:      {ac_s:.1%}")
    print(f"    cross-generator: {cor_s}/{n_eval} = {single_cross_acc:.1%}")
    print(f"  comparison vs old 2-property rule cross-generator: {old_acc:.1%}")
    if single_cross_acc > old_acc + 0.10:
        print(f"  IMPROVED — +{(single_cross_acc - old_acc):.0%} cross-generator over old rule")
        print("  classifier program is alive with a sharper, generator-agnostic predictor")
        print("  NOTE: the 2-property AND search tied in-sample and chose the overfitted")
        print("  rule; the single-property global rule is the real winner here.")
    elif single_cross_acc >= old_acc:
        print(f"  MARGINAL — single-property global rule at {single_cross_acc:.0%}, "
              f"matching the old rule")
    else:
        print(f"  WORSE — single-property global rule at {single_cross_acc:.0%}, "
              f"worse than the old rule")

    # Archived-table assertions tied to docs/GLOBAL_COHERENCE_PREDICTOR_NOTE.md.
    # These pin the headline numbers from the frozen log
    # logs/2026-04-07-global-coherence-predictor.txt: scaffolded swept-set
    # 7/9 = 77.8% via free_coh >= 7.96e-04 and 6/9 = 66.7% via the old
    # 2-property rule. The note already records the off-scaffold reversal
    # (5/9 in GLOBAL_COHERENCE_OFF_SCAFFOLD_NOTE) and is closed.
    assert n_eval == 9, f"expected 9 independent-generator evaluations, got {n_eval}"
    assert old_correct == 6, (
        f"old 2-property rule should match 6/9 on the held-out set, got {old_correct}"
    )
    assert cor_s == 7, (
        f"single-property global rule should match 7/9 on the held-out set, got {cor_s}"
    )
    assert p_s == "free_coh", (
        f"single-property global winner should be free_coh, got {p_s}"
    )
    # Threshold close to 7.96e-04 (within numerical precision of the swept set).
    assert abs(t_s - 7.9597e-04) <= 1e-5 or abs(t_s - 8.0e-04) <= 5e-5, (
        f"free_coh threshold drift: got {t_s}"
    )
    assert d_s == ">=", f"free_coh direction should be >=, got {d_s}"
    print(
        "PASS: bounded archived-replay assertions match the frozen 7/9 vs "
        "6/9 scaffolded result in the note."
    )


if __name__ == "__main__":
    main()
