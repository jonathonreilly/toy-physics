#!/usr/bin/env python3
"""Second-order Kubo extension — does it explain the failing-family pathology?

The first-order Kubo lane (linear_response_true_kubo.py) derived
d(cz)/ds at s=0 via a parallel perturbation propagator B_j = d(amp_j)/ds
and matched the measured response at r = 0.97 across 44 families.

The range-of-validity lane (kubo_range_of_validity.py) showed that on
a strict linearity-regime subset (15/41 families, selected without the
F~M label), measured F~M is within 1.6% of 1.0. The other 26/41 families
fall outside the strict linear regime, with documented nonlinear
ratio patterns:

  G2_asym_z: ratio flips sign 0.17 → 0.05 → -0.19 → -0.69 (sign flip)
  K3_NL5:    ratio ≈ 2 throughout (systematic factor of 2)
  H1_ring:   ratio drifts 0.55 → 0.58 → 0.65 → 0.80 (s-dependent drift)

This lane derives the **second-order** term in the Kubo expansion by
adding a THIRD parallel propagator C_j = d²(amp_j)/ds² at s=0, with
recurrence (same path-sum structure as A and B):

  C_j = Σ_{i→j} [C_i + 2·g_e·B_i + g_e²·A_i] · exp(ikL) · w · h²/L²

where g_e = -i k L_e / r_edge is the per-edge perturbation factor.
The predicted response is:

  predicted_delta_cz(s) = kubo₁ · s + (1/2) · kubo₂ · s²

where kubo₂ = d²(cz)/ds² at s=0, computed from A, B, C via chain rule.

Tests:
  1. Compute kubo₁ and kubo₂ on all 44 families
  2. Predict delta_cz(s) at the four battery strengths
  3. Compare to measured (residual = measured - predicted)
  4. Check whether the failing families' ratio patterns are explained
  5. Compute the new linearity ratio (measured / predicted) — should be
     much closer to 1 than first-order alone
  6. Re-evaluate the linearity-regime subset with the second-order
     prediction; expect it to grow significantly
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
H = uc.H
K_PHASE = uc.K
BETA = 0.8
STRENGTHS = [0.001, 0.002, 0.004, 0.008]


def perturbation_propagator_2nd(pos, adj, nmap, NL, PW, x_src, z_src, k_phase=K_PHASE):
    """Compute A, B, C in a single pass — first three terms of Kubo expansion.

    A_j = Σ T_P                       (free amplitude)
    B_j = -ik Σ T_P Q_P               (first derivative of amp at s=0)
    C_j = -k² Σ T_P Q_P²              (second derivative of amp at s=0)

    Recurrences (per incoming edge i→j with perturbation factor g = -ikL/r):
        A_j += A_i * φ * w'
        B_j += (B_i + g * A_i) * φ * w'
        C_j += (C_i + 2*g*B_i + g²*A_i) * φ * w'
    where φ = exp(ikL) and w' = w·h²/L².
    """
    n = len(pos)
    A = [0j] * n
    B = [0j] * n
    C = [0j] * n
    A[0] = 1.0 + 0j
    order = sorted(range(n), key=lambda i: pos[i][0])
    h2 = H * H
    for i in order:
        ai = A[i]
        bi = B[i]
        ci = C[i]
        if abs(ai) < 1e-30 and abs(bi) < 1e-30 and abs(ci) < 1e-30:
            continue
        for j in adj.get(i, []):
            dx = pos[j][0] - pos[i][0]
            dy = pos[j][1] - pos[i][1]
            dz = pos[j][2] - pos[i][2]
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            mx = 0.5 * (pos[i][0] + pos[j][0])
            mz = 0.5 * (pos[i][2] + pos[j][2])
            r_field = math.sqrt((mx - x_src) ** 2 + (mz - z_src) ** 2) + 0.1
            phase = k_phase * L
            phi = complex(math.cos(phase), math.sin(phase))
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            wprime = w * h2 / (L * L)
            phi_w = phi * wprime
            # per-edge perturbation factor g = -i k L / r
            g = complex(0.0, -k_phase * L / r_field)
            # Second-order: C_j += (C_i + 2 g B_i + g² A_i) · phi · w'
            C[j] += (ci + 2.0 * g * bi + g * g * ai) * phi_w
            # First-order: B_j += (B_i + g A_i) · phi · w'
            B[j] += (bi + g * ai) * phi_w
            # Free: A_j += A_i · phi · w'
            A[j] += ai * phi_w
    return A, B, C


def kubo_first_and_second(pos, adj, nmap, NL, PW):
    """Compute kubo₁ = d(cz)/ds and kubo₂ = d²(cz)/ds² at s=0."""
    x_src = (NL // 3) * H
    A, B, C = perturbation_propagator_2nd(pos, adj, nmap, NL, PW, x_src, MASS_Z)
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds = n - npl

    # Free total and centroid
    weights0 = [abs(A[i]) ** 2 for i in range(ds, n)]
    zs = [pos[i][2] for i in range(ds, n)]
    T0 = sum(weights0)
    if T0 <= 0:
        return 0.0, 0.0, 0.0
    cz_0 = sum(w * z for w, z in zip(weights0, zs)) / T0

    # First-order pieces
    # d|amp|²/ds = 2 Re[A* B]
    dW1 = [2.0 * (A[i].conjugate() * B[i]).real for i in range(ds, n)]
    # d²|amp|²/ds² = 2 Re[A* C] + 2 |B|²
    dW2 = [2.0 * (A[i].conjugate() * C[i]).real + 2.0 * abs(B[i]) ** 2
           for i in range(ds, n)]

    T1 = sum(dW1)  # dT/ds
    T2 = sum(dW2)  # d²T/ds²
    N1 = sum(dw * z for dw, z in zip(dW1, zs))  # dN/ds where N = Σ |amp|² z
    N2 = sum(dw * z for dw, z in zip(dW2, zs))  # d²N/ds²

    # cz(s) = N(s) / T(s)
    # d(cz)/ds = N'/T - (N/T²) T' = N1/T0 - cz_0 * T1/T0
    kubo1 = N1 / T0 - cz_0 * T1 / T0

    # d²(cz)/ds² = d/ds [N'/T - cz · T'/T]
    # Apply quotient rule carefully:
    # N''/T - 2 N' T' / T² + 2 N (T')² / T³ - N T'' / T²
    # which simplifies to:
    # = N''/T - kubo1 * T1/T0 - cz_0 * T2/T0 - cz_0 * T1²/T0² + N1*T1/T0² ...
    # Cleanest form using cz_0, kubo1:
    # cz(s) = N/T
    # cz' = (N' - cz T') / T
    # cz'' = (N'' - cz' T' - cz T'' - cz' T') / T = (N'' - 2 cz' T' - cz T'') / T
    kubo2 = (N2 - 2.0 * kubo1 * T1 - cz_0 * T2) / T0

    return cz_0, kubo1, kubo2


def measured_cz_at(pos, adj, nmap, NL, PW, s):
    hw = int(PW / H)
    npl = (2 * hw + 1) ** 2
    n = len(pos)
    ds_idx = n - npl
    if s == 0.0:
        amps = ind.prop_beam(pos, adj, nmap, None, K_PHASE)
    else:
        x_src = (NL // 3) * H
        fld = uc.imposed_field(pos, x_src, MASS_Z, s)
        amps = ind.prop_beam(pos, adj, nmap, fld, K_PHASE)
    weights = [abs(amps[i]) ** 2 for i in range(ds_idx, n)]
    zs = [pos[i][2] for i in range(ds_idx, n)]
    T = sum(weights)
    if T <= 0:
        return 0.0
    return sum(w * z for w, z in zip(weights, zs)) / T


def collect_one(name, group, pos, adj, nmap, NL, PW, battery_pass):
    cz_0, kubo1, kubo2 = kubo_first_and_second(pos, adj, nmap, NL, PW)
    measured_cz = [measured_cz_at(pos, adj, nmap, NL, PW, s) for s in STRENGTHS]
    measured_dcz = [m - cz_0 for m in measured_cz]
    pred_1 = [kubo1 * s for s in STRENGTHS]
    pred_2 = [kubo1 * s + 0.5 * kubo2 * s * s for s in STRENGTHS]
    return {
        "name": name,
        "group": group,
        "pass": battery_pass,
        "kubo1": kubo1,
        "kubo2": kubo2,
        "cz_0": cz_0,
        "measured": measured_dcz,
        "pred_1": pred_1,
        "pred_2": pred_2,
    }


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
            rows.append(collect_one(r["name"], "swept",
                                    pos, adj, nmap, fam["NL"], fam["PW"], r["pass"]))
        except Exception as e:
            rows.append({"name": fam.get("name", "?"), "group": "swept", "error": str(e)})
    return rows


def collect_scaffolded():
    rows = []
    for name, builder in ind.make_independent_families():
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            rows.append(collect_one(name, "scaffolded",
                                    pos, adj, nmap, ind.NL, ind.PW, r["pass"]))
        except Exception as e:
            rows.append({"name": name, "group": "scaffolded", "error": str(e)})
    return rows


def collect_off_scaffold():
    rows = []
    for name, builder in offs.make_off_scaffold_families():
        try:
            pos, adj, nmap = builder()
            r = ind.battery(name, pos, adj, nmap)
            rows.append(collect_one(name, "off_scaffold",
                                    pos, adj, nmap, offs.NL, offs.PW, r["pass"]))
        except Exception as e:
            rows.append({"name": name, "group": "off_scaffold", "error": str(e)})
    return rows


def main():
    print("=" * 100)
    print("SECOND-ORDER KUBO EXTENSION")
    print("Third parallel propagator C_j = d²(amp_j)/ds² at s=0")
    print("Prediction: delta_cz(s) ≈ kubo₁ · s + (1/2) · kubo₂ · s²")
    print("=" * 100)

    print("\nA. Swept (26)...")
    swept = collect_swept()
    print("B. Scaffolded (9)...")
    scaf = collect_scaffolded()
    print("C. Off-scaffold (9)...")
    off = collect_off_scaffold()
    valid = [r for r in swept + scaf + off if "error" not in r]

    # Detailed table for the three known-pathological families
    focus = {"H1_ring", "G2_asym_z", "K3_NL5", "L1_longrange_k12",
             "OF9_stretched", "G1_asym_y"}
    print("\n" + "=" * 100)
    print("FOCUS: families with known nonlinear ratio patterns")
    print("=" * 100)
    print(f"{'family':22s} {'kubo1':>11s} {'kubo2':>11s} "
          f"{'meas/pred1':>15s} {'meas/pred2':>15s}")
    for r in valid:
        if r["name"] not in focus:
            continue
        m_p1 = []
        m_p2 = []
        for i, s in enumerate(STRENGTHS):
            p1 = r["pred_1"][i]
            p2 = r["pred_2"][i]
            m = r["measured"][i]
            m_p1.append(f"{m/p1:.3f}" if abs(p1) > 1e-12 else "  nan ")
            m_p2.append(f"{m/p2:.3f}" if abs(p2) > 1e-12 else "  nan ")
        print(f"{r['name']:22s} {r['kubo1']:+11.3f} {r['kubo2']:+11.3f} "
              f"  {','.join(m_p1):>13s}   {','.join(m_p2):>13s}")

    # Aggregate: how often is the second-order prediction within 10% at s=0.008?
    print("\n" + "=" * 100)
    print("LINEARITY RATIO AT EACH s — first-order vs second-order prediction")
    print("=" * 100)
    print(f"{'s':>8s}  {'1st order':>12s}  {'2nd order':>12s}")
    for i, s in enumerate(STRENGTHS):
        ratios_1 = []
        ratios_2 = []
        for r in valid:
            if abs(r["pred_1"][i]) < 1e-12:
                continue
            ratios_1.append(abs(r["measured"][i] / r["pred_1"][i] - 1.0))
            if abs(r["pred_2"][i]) > 1e-12:
                ratios_2.append(abs(r["measured"][i] / r["pred_2"][i] - 1.0))
        n1 = sum(1 for x in ratios_1 if x < 0.10)
        n2 = sum(1 for x in ratios_2 if x < 0.10)
        print(f"  s={s:.4f}  in 10% band: {n1}/{len(ratios_1)} (1st)  "
              f"{n2}/{len(ratios_2)} (2nd)")

    # Linearity-regime subset under second-order prediction
    print("\n" + "=" * 100)
    print("LINEARITY-REGIME SUBSET (max |measured/pred - 1| < 0.10 at all 4 strengths)")
    print("=" * 100)
    n_in_1 = 0
    n_in_2 = 0
    for r in valid:
        ratios_1 = []
        ratios_2 = []
        for i, s in enumerate(STRENGTHS):
            if abs(r["pred_1"][i]) < 1e-12:
                ratios_1.append(float("inf"))
            else:
                ratios_1.append(abs(r["measured"][i] / r["pred_1"][i] - 1.0))
            if abs(r["pred_2"][i]) < 1e-12:
                ratios_2.append(float("inf"))
            else:
                ratios_2.append(abs(r["measured"][i] / r["pred_2"][i] - 1.0))
        if max(ratios_1) < 0.10:
            n_in_1 += 1
        if max(ratios_2) < 0.10:
            n_in_2 += 1
    print(f"  first-order linearity regime:  {n_in_1}/{len(valid)} = {n_in_1/len(valid):.1%}")
    print(f"  second-order linearity regime: {n_in_2}/{len(valid)} = {n_in_2/len(valid):.1%}")
    print(f"  growth from 1st to 2nd order: +{n_in_2 - n_in_1} families")

    # Residuals at s=0.008: how much does the second-order term reduce the residual?
    print("\n" + "=" * 100)
    print("RESIDUAL REDUCTION at s=0.008 (measured - predicted)")
    print("=" * 100)
    res_1 = []
    res_2 = []
    for r in valid:
        i = 3  # s = 0.008
        m = r["measured"][i]
        p1 = r["pred_1"][i]
        p2 = r["pred_2"][i]
        res_1.append(abs(m - p1))
        res_2.append(abs(m - p2))
    if res_1:
        sum_1 = sum(res_1)
        sum_2 = sum(res_2)
        med_1 = sorted(res_1)[len(res_1) // 2]
        med_2 = sorted(res_2)[len(res_2) // 2]
        print(f"  sum |residual| (1st order): {sum_1:.4f}")
        print(f"  sum |residual| (2nd order): {sum_2:.4f}")
        print(f"  reduction factor: {sum_1/sum_2:.2f}x" if sum_2 > 0 else "  (sum_2 = 0)")
        print(f"  median |residual| (1st): {med_1:.6f}")
        print(f"  median |residual| (2nd): {med_2:.6f}")

    # Final verdict
    print("\n" + "=" * 100)
    print("VERDICT")
    print("=" * 100)
    growth = n_in_2 - n_in_1
    if growth >= 5 and n_in_2 / len(valid) > 0.5:
        print(f"  STRONG — second-order Kubo grows the linearity regime by +{growth}")
        print(f"  ({n_in_1}/{len(valid)} → {n_in_2}/{len(valid)}). Higher-order corrections")
        print("  capture a meaningful fraction of the previously-failing families.")
    elif growth > 0:
        print(f"  MODERATE — second-order grows linearity regime by +{growth}")
        print(f"  ({n_in_1}/{len(valid)} → {n_in_2}/{len(valid)}).")
        print("  Some progress, but most failing families still need higher orders or")
        print("  full path-sum.")
    elif growth == 0:
        print(f"  NULL — second order did not change the linearity-regime count.")
        print("  Failing families need either much higher orders or a different framework.")
    else:
        print(f"  WORSE — second-order prediction makes the linearity regime SHRINK by {-growth}.")
        print("  Either the recurrence has a bug or the second-order term overshoots.")


if __name__ == "__main__":
    main()
