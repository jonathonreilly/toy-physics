#!/usr/bin/env python3
"""True first-order Kubo propagator — the real analytic derivation.

The previous lane (linear_response_derivation.py) used a HEURISTIC
first-moment predictor:
    kubo_heuristic = cz_weighted_by_1/|z-z_src| - cz_free
and found r = 0.56 / 0.72 off-scaffold / 79.5% classification on 44
families. Three residual cases (H1_ring, G2_asym_z, L1_longrange)
produced honest sign disagreements.

This lane computes the **TRUE** first-order Kubo response by direct
symbolic differentiation of the propagator with respect to the field
source strength s.

For amp_j = Σ_paths exp(i k L (1-f)) * weight, differentiating at s=0:

    (d amp_j / ds)_0 = Σ_paths [Σ_edges (-i k L_edge / r_edge)] * A_free

This can be computed incrementally via a SECOND propagator B_i that
runs alongside the standard propagator A_i:

    A_j = Σ_{i → j} A_i * exp(i k L) * w * h²/L²
    B_j = Σ_{i → j} [B_i - i k A_i L / r_edge] * exp(i k L) * w * h²/L²

with A_0 = 1, B_0 = 0 at the source. The recurrence is the same shape
as the standard propagator — just two amplitudes per node.

Then:
    d|amp_j|²/ds = 2 Re[A_j^* B_j]
    d cz/ds = Σ_j (z_j - cz_free) * d|amp_j|²/ds / Σ_j |A_j|²

This IS the analytic first-order response. It should match the
measured finite-difference response exactly, up to finite-difference
error. If it does, we have the derivation. If the simple heuristic
from the previous lane agrees with the true expression, the heuristic
is justified as an approximation. If not, we know exactly what the
heuristic was missing.

Tests:
  1. Correlation of kubo_true with measured d(cz)/ds across 44 families
  2. Sign agreement
  3. Pass classification accuracy (no fitting)
  4. Comparison to kubo_heuristic on the three residual cases
"""

from __future__ import annotations


# Heavy compute / sweep runner — `AUDIT_TIMEOUT_SEC = 1800`
# means the audit-lane precompute and live audit runner allow up to
# 30 min of wall time before recording a timeout. The 120 s default
# ceiling is too tight under concurrency contention; see
# `docs/audit/RUNNER_CACHE_POLICY.md`.
AUDIT_TIMEOUT_SEC = 1800

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import universality_classifier as uc
import independent_generators_heldout as ind
import global_coherence_off_scaffold as offs

MASS_Z = uc.MASS_Z
S_SMALL = 0.001
H = uc.H
BETA = 0.8
K_PHASE = uc.K


def perturbation_propagator(pos, adj, nmap, NL, PW, x_src, z_src, k_phase=K_PHASE):
    """Compute A (standard amplitude) and B (= dA/ds at s=0) in a single pass.

    The field is f = s / (|(x,z) - (x_src, z_src)| + 0.1) — the same imposed
    1/r field used by the battery. At s=0:
        phase factor = exp(i k L)
        dphase/ds = -i k L / r_edge   where r_edge is the field distance
                                      at the edge midpoint.
    """
    n = len(pos)
    A = [0j] * n
    B = [0j] * n
    A[0] = 1.0 + 0j
    # B[0] = 0 (initial condition: amp is 1, derivative is 0)
    order = sorted(range(n), key=lambda i: pos[i][0])
    h2 = H * H
    for i in order:
        ai = A[i]
        bi = B[i]
        if abs(ai) < 1e-30 and abs(bi) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            # midpoint of the edge
            mx = 0.5 * (pos[i][0] + pos[j][0])
            mz = 0.5 * (pos[i][2] + pos[j][2])
            r_field = math.sqrt((mx - x_src) ** 2 + (mz - z_src) ** 2) + 0.1
            # propagator factor at s=0: exp(i k L)
            phase = k_phase * L
            phi = complex(math.cos(phase), math.sin(phase))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            weight = phi * w * h2 / (L * L)
            # A recurrence
            A[j] += ai * weight
            # B recurrence: includes dphase/ds factor on A_i
            # d phase / ds = d/ds [k L (1-f)] = -k L df/ds = -k L * (1/r_field)
            # so d(phi)/ds|_{s=0} = i * d phase/ds * phi = -i k L / r_field * phi
            # Wait: phi = exp(i * phase_total). d phi / ds = i * d phase_total/ds * phi
            # phase_total = k L (1 - s/r_field), so d phase_total/ds = -k L / r_field
            # d phi/ds = -i k L / r_field * phi
            dphi_ds = complex(0.0, -k_phase * L / r_field) * phi
            # chain rule: d(A_i * phi)/ds = B_i * phi + A_i * dphi_ds
            # but we want B_j (the derivative of amp at j), which accumulates
            # all the contributions from edges into j
            B[j] += (bi * phi + ai * dphi_ds) * w * h2 / (L * L)
    return A, B


def measured_response_finite_diff(pos, adj, nmap, NL, PW):
    """Measured d(cz)/ds via finite difference."""
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl

    def cz_from_amps(amps):
        weights = [abs(amps[i]) ** 2 for i in range(ds, n)]
        zs = [pos[i][2] for i in range(ds, n)]
        total = sum(weights)
        if total <= 0:
            return 0.0
        return sum(w * z for w, z in zip(weights, zs)) / total

    free = ind.prop_beam(pos, adj, nmap, None, K_PHASE)
    cz_0 = cz_from_amps(free)
    x_src = (NL // 3) * H
    fld = uc.imposed_field(pos, x_src, MASS_Z, S_SMALL)
    g = ind.prop_beam(pos, adj, nmap, fld, K_PHASE)
    cz_s = cz_from_amps(g)
    return (cz_s - cz_0) / S_SMALL


def true_kubo_dcz_ds(pos, adj, nmap, NL, PW):
    """True first-order d(cz)/ds via the perturbation propagator."""
    x_src = (NL // 3) * H
    A, B = perturbation_propagator(pos, adj, nmap, NL, PW, x_src, MASS_Z)
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl

    # Free centroid and total at s=0
    weights = [abs(A[i]) ** 2 for i in range(ds, n)]
    zs = [pos[i][2] for i in range(ds, n)]
    total = sum(weights)
    if total <= 0:
        return 0.0, 0.0
    cz_free = sum(w * z for w, z in zip(weights, zs)) / total

    # dT/ds = Σ 2 Re[A* B] over detector
    dT_ds = sum(2.0 * (A[i].conjugate() * B[i]).real for i in range(ds, n))
    # d(Σ w_j z_j)/ds
    d_num_ds = sum(2.0 * (A[i].conjugate() * B[i]).real * pos[i][2] for i in range(ds, n))
    # chain rule: d(N/T)/ds = (d N/ds) / T - N * (d T/ds) / T²
    N = total * cz_free
    d_cz_ds = d_num_ds / total - N * dT_ds / (total * total)
    return d_cz_ds, cz_free


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


def collect_swept():
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
            kubo_true, cz_free = true_kubo_dcz_ds(pos, adj, nmap, NL, PW)
            measured = measured_response_finite_diff(pos, adj, nmap, NL, PW)
            rows.append({
                "name": r["name"] + "_swept",
                "group": "swept",
                "pass": r["pass"],
                "kubo_true": kubo_true,
                "measured": measured,
                "cz_free": cz_free,
            })
        except Exception as e:
            rows.append({"name": fam.get("name", "?"), "group": "swept", "error": str(e)})
    return rows


def collect_scaffolded():
    rows = []
    for name, builder in ind.make_independent_families():
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            NL = ind.NL
            PW = ind.PW
            kubo_true, cz_free = true_kubo_dcz_ds(pos, adj, nmap, NL, PW)
            measured = measured_response_finite_diff(pos, adj, nmap, NL, PW)
            rows.append({
                "name": name + "_scaf",
                "group": "scaffolded",
                "pass": r["pass"],
                "kubo_true": kubo_true,
                "measured": measured,
                "cz_free": cz_free,
            })
        except Exception as e:
            rows.append({"name": name, "group": "scaffolded", "error": str(e)})
    return rows


def collect_off_scaffold():
    rows = []
    for name, builder in offs.make_off_scaffold_families():
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            NL = offs.NL
            PW = offs.PW
            kubo_true, cz_free = true_kubo_dcz_ds(pos, adj, nmap, NL, PW)
            measured = measured_response_finite_diff(pos, adj, nmap, NL, PW)
            rows.append({
                "name": name + "_off",
                "group": "off_scaffold",
                "pass": r["pass"],
                "kubo_true": kubo_true,
                "measured": measured,
                "cz_free": cz_free,
            })
        except Exception as e:
            rows.append({"name": name, "group": "off_scaffold", "error": str(e)})
    return rows


def main():
    print("=" * 100)
    print("TRUE FIRST-ORDER KUBO — analytic d(cz)/ds via parallel perturbation propagator")
    print("Compared to finite-difference measured response across 44 families")
    print("=" * 100)

    print("\nA. Swept families (26)...")
    swept = collect_swept()
    print("B. Scaffolded independent (9)...")
    scaf = collect_scaffolded()
    print("C. Off-scaffold (9)...")
    off = collect_off_scaffold()

    all_rows = swept + scaf + off
    valid = [r for r in all_rows if "error" not in r]

    print("\n" + "=" * 100)
    print("RESULTS — kubo_true vs measured")
    print("=" * 100)
    print(f"{'family':30s} {'group':>12s} {'pass':>5s} {'measured':>12s} {'kubo_true':>12s} {'ratio':>10s}")
    print("-" * 100)
    for r in valid:
        tag = "PASS" if r["pass"] else "FAIL"
        ratio = r["kubo_true"] / r["measured"] if abs(r["measured"]) > 1e-10 else float("nan")
        print(f"{r['name']:30s} {r['group']:>12s} {tag:>5s} "
              f"{r['measured']:+12.6f} {r['kubo_true']:+12.6f} {ratio:10.4f}")

    # Overall Pearson
    xs = [r["kubo_true"] for r in valid]
    ys = [r["measured"] for r in valid]
    r_all = pearson(xs, ys)
    print(f"\nOVERALL correlation: r = {r_all:.4f}  (N={len(valid)})")

    print("\nBY GROUP:")
    for group in ["swept", "scaffolded", "off_scaffold"]:
        rs = [r for r in valid if r["group"] == group]
        if not rs:
            continue
        xs_g = [r["kubo_true"] for r in rs]
        ys_g = [r["measured"] for r in rs]
        r_g = pearson(xs_g, ys_g)
        print(f"  {group:>15s}: r = {r_g:.4f}  (N={len(rs)})")

    # Sign agreement
    sign_ok = sum(1 for r in valid if (r["kubo_true"] > 0) == (r["measured"] > 0))
    print(f"\nSIGN AGREEMENT: {sign_ok}/{len(valid)} = {sign_ok/len(valid):.1%}")

    # Ratio statistics for cases where measured > 0
    ratios = [
        r["kubo_true"] / r["measured"]
        for r in valid
        if abs(r["measured"]) > 1e-6
    ]
    if ratios:
        mean_r = sum(ratios) / len(ratios)
        var_r = sum((x - mean_r) ** 2 for x in ratios) / len(ratios)
        print(f"\nRATIO kubo_true / measured (|measured| > 1e-6):")
        print(f"  mean = {mean_r:.4f}")
        print(f"  std  = {math.sqrt(var_r):.4f}")
        print(f"  min  = {min(ratios):.4f}")
        print(f"  max  = {max(ratios):.4f}")

    # Pass classification
    print("\nPASS CLASSIFICATION via kubo_true > 0:")
    correct = sum(1 for r in valid if (r["kubo_true"] > 0) == r["pass"])
    print(f"  {correct}/{len(valid)} = {correct/len(valid):.1%}")

    # Focus on the three residual cases from the previous lane
    print("\nTHREE RESIDUAL CASES (from linear_response_derivation):")
    focus = {"H1_ring_swept", "G2_asym_z_swept", "L1_longrange_k12_scaf"}
    for r in valid:
        if r["name"] in focus:
            print(f"  {r['name']}: measured={r['measured']:+.4f}  "
                  f"kubo_true={r['kubo_true']:+.4f}  "
                  f"sign_agree={(r['kubo_true']>0) == (r['measured']>0)}")

    print("\n" + "=" * 100)
    print("VERDICT")
    print("=" * 100)
    if r_all > 0.95:
        print(f"  EXACT (r={r_all:.4f}) — kubo_true is the true first-order response.")
        print("  The derivation is now closed-form: d(cz)/ds at s=0 is computable")
        print("  analytically from the perturbation propagator with the 1/r_edge factor.")
    elif r_all > 0.85:
        print(f"  STRONG (r={r_all:.4f}) — kubo_true matches measured closely.")
        print("  Residual discrepancy is finite-difference error or second-order contamination.")
    elif r_all > 0.60:
        print(f"  MODERATE (r={r_all:.4f}) — kubo_true is directionally correct but")
        print("  quantitatively off. Either the derivation is missing a term, or the")
        print("  finite-difference epsilon is picking up second-order effects.")
    else:
        print(f"  WEAK (r={r_all:.4f}) — kubo_true does NOT match measured.")
        print("  Either the derivation is wrong or the measured response is not first-order.")


if __name__ == "__main__":
    main()
