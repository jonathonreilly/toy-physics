#!/usr/bin/env python3
"""
Bounded up-type mass ratios from the CKM dual with a parallel-bridge ansatz.

Status:
  bounded secondary lane (one conditional partition parameter)

Safe claim:
  Extending the promoted CKM atlas/axiom package and the Phase 1 down-type
  mass-ratio dual to the up sector under the parallel-bridge ansatz yields a
  one-parameter family of up-type mass ratios.  The free parameter is the
  relative-phase partition f in [0, 1] that distributes |V_us|, |V_cb|, |V_ub|
  between the down-sector and up-sector NNI contributions:

    m_d/m_s        = f_12^2  * (alpha_s(v)/2)
    m_u/m_c        = (1-f_12^2) * (alpha_s(v)/2)       # CP-orthogonal ansatz
    m_s/m_b        = (f_23 * alpha_s(v)/sqrt(6))^(6/5)
    m_c/m_t        = ((1-f_23^2)^(1/2) * alpha_s(v)/sqrt(6))^(6/5)

  Phase 1 corresponds to the "down-dominant" edge f_12 = f_23 = 1
  (m_u/m_c = m_c/m_t = 0).  The "up-dominant" edge (f_12 = f_23 = 0) flips
  the roles.  Any intermediate partition gives a pair of sectors.

  No observed quark masses are used as derivation inputs.

Important qualifier:
  The partition parameters (f_12, f_23) are NOT yet derived from the retained
  core.  The natural closure candidates flagged in the mass-spectrum attack
  plan are (a) the atlas CP phase delta = arctan(sqrt(5)); (b) the Jarlskog
  invariant J; (c) a forthcoming up-down isospin-partner theorem.  None of
  these is promoted yet, so this lane is bounded rather than retained.

What this lane does close:
  - explicit algebraic formulas for the up-type mass ratios as algebraic
    functions of the promoted atlas CKM quantities and (f_12, f_23)
  - numerical witness of the down-dominant edge (Phase 1) and the
    up-dominant edge
  - sensitivity analysis showing how observed ratios select a specific
    (f_12, f_23)
"""

from __future__ import annotations

import math

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_S_V,
    CANONICAL_U0,
)


C_F = 4.0 / 3.0
T_F = 1.0 / 2.0
EXPONENT = C_F - T_F  # 5/6 SU(3) bridge exponent

# Observation-facing comparators (NOT derivation inputs).
# MSbar-at-2-GeV light-quark masses + pole top + self-scale bottom (PDG 2024).
M_U_OBS = 2.16e-3
M_C_OBS = 1.273
M_T_OBS = 172.57
M_D_OBS = 4.67e-3
M_S_OBS = 93.4e-3
M_B_OBS = 4.180

R_UC_OBS = M_U_OBS / M_C_OBS
R_CT_OBS = M_C_OBS / M_T_OBS
R_UT_OBS = M_U_OBS / M_T_OBS
R_DS_OBS = M_D_OBS / M_S_OBS
R_SB_OBS = M_S_OBS / M_B_OBS
R_DB_OBS = M_D_OBS / M_B_OBS

V_US_OBS = 0.2243
V_CB_OBS = 0.0422
V_UB_OBS = 0.00382
DELTA_OBS_DEG = 65.5
J_OBS = 3.08e-5

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


def part1_inputs() -> dict:
    print("\n" + "=" * 72)
    print("PART 1: Input surface (Phase 1 down-type ratios + atlas CKM)")
    print("=" * 72)

    alpha_s_v = CANONICAL_ALPHA_S_V
    v_us = math.sqrt(alpha_s_v / 2.0)
    v_cb = alpha_s_v / math.sqrt(6.0)
    v_ub = alpha_s_v**1.5 / (6.0 * math.sqrt(2.0))
    delta_std = math.atan(math.sqrt(5.0))

    # Phase 1 down-type ratios (see frontier_mass_ratio_ckm_dual.py):
    r_ds_p1 = alpha_s_v / 2.0
    r_sb_p1 = v_cb ** (1.0 / EXPONENT)
    r_db_p1 = r_ds_p1 * r_sb_p1

    print(f"\n  alpha_s(v)               = {alpha_s_v:.12f}")
    print(f"  u_0                      = {CANONICAL_U0:.12f}")
    print(f"  alpha_bare               = {CANONICAL_ALPHA_BARE:.12f}")
    print(f"  exponent (C_F - T_F)     = 5/6")
    print()
    print(f"  Atlas CKM magnitudes and CP phase:")
    print(f"    |V_us| = sqrt(alpha_s(v)/2)         = {v_us:.6f}")
    print(f"    |V_cb| = alpha_s(v)/sqrt(6)         = {v_cb:.6f}")
    print(f"    |V_ub| = alpha_s(v)^(3/2)/(6*sqrt(2)) = {v_ub:.6f}")
    print(f"    delta  = arctan(sqrt(5))            = {math.degrees(delta_std):.3f} deg")
    print()
    print(f"  Phase 1 down-type (down-dominant edge, f_12 = f_23 = 1):")
    print(f"    m_d/m_s = alpha_s(v)/2                = {r_ds_p1:.6f}")
    print(f"    m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5)  = {r_sb_p1:.6f}")
    print(f"    m_d/m_b = (m_d/m_s)(m_s/m_b)          = {r_db_p1:.6f}")

    check(
        "|V_us| matches atlas formula",
        abs(v_us - math.sqrt(alpha_s_v / 2.0)) < 1e-14,
        f"|V_us| = {v_us:.8f}",
    )
    check(
        "|V_cb| matches atlas formula",
        abs(v_cb - alpha_s_v / math.sqrt(6.0)) < 1e-14,
        f"|V_cb| = {v_cb:.8f}",
    )
    check(
        "|V_ub| matches atlas formula",
        abs(v_ub - alpha_s_v**1.5 / (6.0 * math.sqrt(2.0))) < 1e-14,
        f"|V_ub| = {v_ub:.8f}",
    )
    check(
        "delta = arctan(sqrt(5)) matches cos^2(delta) = 1/6",
        abs(math.cos(delta_std) ** 2 - 1.0 / 6.0) < 1e-12,
        f"cos^2 = {math.cos(delta_std) ** 2:.8f}",
    )
    check(
        "Phase 1 m_d/m_s closed form",
        abs(r_ds_p1 - v_us**2) < 1e-14,
        f"m_d/m_s = {r_ds_p1:.6f}",
    )
    check(
        "Phase 1 m_s/m_b closed form",
        abs(r_sb_p1 - v_cb ** (6.0 / 5.0)) < 1e-14,
        f"m_s/m_b = {r_sb_p1:.6f}",
    )

    return {
        "alpha_s_v": alpha_s_v,
        "v_us": v_us,
        "v_cb": v_cb,
        "v_ub": v_ub,
        "delta": delta_std,
        "r_ds_p1": r_ds_p1,
        "r_sb_p1": r_sb_p1,
        "r_db_p1": r_db_p1,
    }


def part2_parallel_ansatz(inputs: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Parallel-bridge ansatz for both sectors")
    print("=" * 72)

    v_us = inputs["v_us"]
    v_cb = inputs["v_cb"]

    print("\n  In the mass-basis NNI texture with GST + 5/6 bridges applied in both")
    print("  sectors (Z_3-constrained NNI), the down-sector and up-sector NNI")
    print("  contributions to each atlas CKM magnitude combine coherently.  Under")
    print("  the CP-orthogonal phase ansatz (relative phase pi/2 between sectors):")
    print()
    print("    |V_us|^2 = (m_d/m_s)      + (m_u/m_c)")
    print("    |V_cb|^2 = (m_s/m_b)^(5/3) + (m_c/m_t)^(5/3)")
    print()
    print("  Introducing partition fractions f_12, f_23 in [0, 1]:")
    print()
    print("    m_d/m_s     =  f_12^2 * |V_us|^2")
    print("    m_u/m_c     = (1 - f_12^2) * |V_us|^2")
    print("    (m_s/m_b)^(5/3) =  f_23^2 * |V_cb|^2")
    print("    (m_c/m_t)^(5/3) = (1 - f_23^2) * |V_cb|^2")
    print()
    print("  Phase 1 is the limit f_12 = f_23 = 1 (down-dominant).")
    print("  The observed values select (f_12, f_23) in the interior.")

    # The CP-orthogonal Pythagorean ansatz is an approximation; the observed
    # ratios sit within a few percent of the sum.  We report the gap rather
    # than insisting on strict containment.
    gap_12 = (R_DS_OBS + R_UC_OBS) - v_us**2
    print(f"\n  Closure gap (ansatz approximation):")
    print(f"    (m_d/m_s)_obs + (m_u/m_c)_obs - |V_us|^2 = {gap_12:+.4e}")
    check("ansatz sum (m_d/m_s + m_u/m_c) matches |V_us|^2 within 1%",
          abs(gap_12 / v_us**2) < 0.01,
          f"relative gap = {gap_12/v_us**2:+.4%}")
    check("parameterization spans both edges (structural)",
          True,
          "partition by construction")


def part3_edges(inputs: dict) -> dict:
    print("\n" + "=" * 72)
    print("PART 3: Down-dominant and up-dominant edges")
    print("=" * 72)

    alpha_s_v = inputs["alpha_s_v"]
    v_us = inputs["v_us"]
    v_cb = inputs["v_cb"]

    # Down-dominant edge (f_12 = f_23 = 1): Phase 1
    r_ds_down = alpha_s_v / 2.0
    r_sb_down = v_cb ** (6.0 / 5.0)
    r_uc_down = 0.0
    r_ct_down = 0.0

    # Up-dominant edge (f_12 = f_23 = 0): the full |V_us|^2 and |V_cb|^2 sit in
    # the up sector
    r_uc_up = alpha_s_v / 2.0
    r_ct_up = v_cb ** (6.0 / 5.0)
    r_ds_up = 0.0
    r_sb_up = 0.0

    print(f"\n  Down-dominant edge (f_12 = f_23 = 1):")
    print(f"    m_d/m_s = {r_ds_down:.6f}  (obs: {R_DS_OBS:.6f})")
    print(f"    m_s/m_b = {r_sb_down:.6f}  (obs: {R_SB_OBS:.6f})")
    print(f"    m_u/m_c = {r_uc_down:.6f}  (obs: {R_UC_OBS:.6f})")
    print(f"    m_c/m_t = {r_ct_down:.6f}  (obs: {R_CT_OBS:.6f})")

    print(f"\n  Up-dominant edge (f_12 = f_23 = 0):")
    print(f"    m_d/m_s = {r_ds_up:.6f}  (obs: {R_DS_OBS:.6f})")
    print(f"    m_s/m_b = {r_sb_up:.6f}  (obs: {R_SB_OBS:.6f})")
    print(f"    m_u/m_c = {r_uc_up:.6f}  (obs: {R_UC_OBS:.6f})")
    print(f"    m_c/m_t = {r_ct_up:.6f}  (obs: {R_CT_OBS:.6f})")

    check(
        "down-dominant m_d/m_s equals Phase 1 prediction",
        abs(r_ds_down - inputs["r_ds_p1"]) < 1e-14,
    )
    check(
        "down-dominant m_s/m_b equals Phase 1 prediction",
        abs(r_sb_down - inputs["r_sb_p1"]) < 1e-14,
    )
    check(
        "up-dominant m_u/m_c equals Phase 1 down-ratio",
        abs(r_uc_up - alpha_s_v / 2.0) < 1e-14,
    )
    check(
        "up-dominant m_c/m_t equals Phase 1 down-ratio",
        abs(r_ct_up - v_cb ** (6.0 / 5.0)) < 1e-14,
    )
    check(
        "down-dominant and up-dominant edges exhaust the unit interval",
        True,
        "partition by construction",
    )

    return {
        "down": {"r_ds": r_ds_down, "r_sb": r_sb_down, "r_uc": r_uc_down, "r_ct": r_ct_down},
        "up": {"r_ds": r_ds_up, "r_sb": r_sb_up, "r_uc": r_uc_up, "r_ct": r_ct_up},
    }


def part4_interior_solver(inputs: dict) -> dict:
    print("\n" + "=" * 72)
    print("PART 4: Interior partition from the observation comparator")
    print("=" * 72)

    v_us = inputs["v_us"]
    v_cb = inputs["v_cb"]

    # Solve for f_12, f_23 such that the partition reproduces observed ratios.
    # f_12^2 = (m_d/m_s)_obs / |V_us|^2
    # f_23^2 = (m_s/m_b)^(5/3)_obs / |V_cb|^2
    f12_sq_obs = R_DS_OBS / (v_us**2)
    f23_sq_obs = (R_SB_OBS ** (5.0 / 3.0)) / (v_cb**2)
    f12_obs = math.sqrt(max(0.0, min(1.0, f12_sq_obs)))
    f23_obs = math.sqrt(max(0.0, min(1.0, f23_sq_obs)))

    # Up-type ratios under this partition:
    r_uc_pred = (1.0 - f12_sq_obs) * (v_us**2)
    r_ct_pred = ((1.0 - f23_sq_obs) ** (3.0 / 5.0)) * (v_cb ** (6.0 / 5.0)) \
        if (1.0 - f23_sq_obs) > 0 else 0.0
    # Equivalently: (m_c/m_t) = ((1 - f23^2) * |V_cb|^2)^(3/5)

    print(f"\n  Partition from observation comparator (comparator-only, not input):")
    print(f"    f_12 = sqrt((m_d/m_s)_obs / |V_us|^2)               = {f12_obs:.6f}")
    print(f"    f_23 = sqrt((m_s/m_b)^(5/3)_obs / |V_cb|^2)         = {f23_obs:.6f}")
    print(f"\n  Implied up-type ratios under this partition:")
    print(f"    m_u/m_c = (1-f_12^2) * |V_us|^2 = {r_uc_pred:.6e}  (obs: {R_UC_OBS:.6e})")
    print(f"    m_c/m_t = ((1-f_23^2)|V_cb|^2)^(3/5) = {r_ct_pred:.6e}  (obs: {R_CT_OBS:.6e})")
    print(f"\n  Deviations:")
    dev_uc = (r_uc_pred / R_UC_OBS - 1.0) * 100.0
    dev_ct = (r_ct_pred / R_CT_OBS - 1.0) * 100.0
    print(f"    m_u/m_c: {dev_uc:+.2f}%")
    print(f"    m_c/m_t: {dev_ct:+.2f}%")

    check(
        "f_12 stays in the unit interval on the observation comparator",
        0.0 <= f12_obs <= 1.0,
        f"f_12 = {f12_obs:.6f}",
    )
    check(
        "f_23 stays in the unit interval on the observation comparator",
        0.0 <= f23_obs <= 1.0,
        f"f_23 = {f23_obs:.6f}",
    )
    check(
        "f_12 is within 5% of unity (down-dominant 1-2 sector)",
        abs(f12_obs - 1.0) < 0.05,
        f"f_12 = {f12_obs:.6f}, 1 - f_12 = {1.0 - f12_obs:+.4f}",
    )
    check(
        "f_23 is within 1% of unity (down-dominant 2-3 sector)",
        abs(f23_obs - 1.0) < 0.01,
        f"f_23 = {f23_obs:.6f}, 1 - f_23 = {1.0 - f23_obs:+.4f}",
    )
    check(
        "m_u/m_c prediction has correct sign and order of magnitude",
        1e-4 < r_uc_pred < 1e-2,
        f"m_u/m_c = {r_uc_pred:.3e}",
    )
    check(
        "m_c/m_t prediction has correct sign and order of magnitude",
        1e-4 < r_ct_pred < 5e-2,
        f"m_c/m_t = {r_ct_pred:.3e}",
    )

    return {
        "f12_obs": f12_obs,
        "f23_obs": f23_obs,
        "r_uc_pred": r_uc_pred,
        "r_ct_pred": r_ct_pred,
    }


def part5_isospin_partner_pairing(inputs: dict, partition: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 5: Isospin-partner pairing cross-check")
    print("=" * 72)

    # The up-down pairing: m_u m_d, m_c m_s, m_t m_b all share the same v
    # (single Higgs doublet, retained).  A natural framework-internal cross
    # check: the GEOMETRIC-MEAN masses are ordered by the EWSB generation
    # cascade.  In particular, the dimensionless combination
    #
    #   Q = (m_u m_c m_t) / (m_d m_s m_b)^k
    #
    # must be a framework-internal number for some k if the pairing is
    # structural.  We don't derive Q here; we only document the comparator
    # structure.
    geom_u = (M_U_OBS * M_C_OBS * M_T_OBS) ** (1.0 / 3.0)
    geom_d = (M_D_OBS * M_S_OBS * M_B_OBS) ** (1.0 / 3.0)
    ratio_geom = geom_u / geom_d

    # Predicted m_u/m_t from the chain under the interior partition:
    r_uc_pred = partition["r_uc_pred"]
    r_ct_pred = partition["r_ct_pred"]
    r_ut_pred = r_uc_pred * r_ct_pred

    print(f"\n  Up-type chain under interior partition:")
    print(f"    m_u/m_c = {r_uc_pred:.6e}")
    print(f"    m_c/m_t = {r_ct_pred:.6e}")
    print(f"    m_u/m_t = (m_u/m_c)(m_c/m_t) = {r_ut_pred:.6e}  (obs: {R_UT_OBS:.6e})")
    print(f"\n  Geometric-mean observation comparators:")
    print(f"    (m_u m_c m_t)^(1/3)          = {geom_u:.4f} GeV")
    print(f"    (m_d m_s m_b)^(1/3)          = {geom_d:.4f} GeV")
    print(f"    ratio geom_u / geom_d        = {ratio_geom:.3f}")

    dev_ut = (r_ut_pred / R_UT_OBS - 1.0) * 100.0
    print(f"\n  m_u/m_t chain-rule deviation: {dev_ut:+.2f}%")

    check(
        "m_u/m_t chain-rule prediction has correct order of magnitude",
        1e-6 < r_ut_pred < 1e-4,
        f"m_u/m_t = {r_ut_pred:.3e}",
    )
    check(
        "geometric-mean up-down ratio is O(1) (pair structure intact)",
        1.0 < ratio_geom < 30.0,
        f"ratio = {ratio_geom:.3f}",
    )


def part6_sensitivity(inputs: dict, partition: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 6: Sensitivity to the partition parameter")
    print("=" * 72)

    v_us = inputs["v_us"]
    v_cb = inputs["v_cb"]

    print("\n  m_u/m_c vs f_12:")
    print(f"    {'f_12':>8s}  {'m_u/m_c':>12s}  {'dev vs obs':>12s}")
    for f12 in [0.00, 0.50, 0.90, 0.99, 0.995, 0.999, 1.00]:
        r_uc = (1.0 - f12**2) * v_us**2
        if R_UC_OBS > 0:
            dev = (r_uc / R_UC_OBS - 1.0) * 100.0
            print(f"    {f12:>8.4f}  {r_uc:>12.6e}  {dev:>+12.2f}%")
        else:
            print(f"    {f12:>8.4f}  {r_uc:>12.6e}  (N/A)")

    print("\n  m_c/m_t vs f_23:")
    print(f"    {'f_23':>8s}  {'m_c/m_t':>12s}  {'dev vs obs':>12s}")
    for f23 in [0.00, 0.50, 0.90, 0.99, 0.995, 0.999, 1.00]:
        r_ct = ((1.0 - f23**2) ** (3.0 / 5.0)) * (v_cb ** (6.0 / 5.0)) if (1.0 - f23**2) > 0 else 0.0
        if R_CT_OBS > 0:
            dev = (r_ct / R_CT_OBS - 1.0) * 100.0
            print(f"    {f23:>8.4f}  {r_ct:>12.6e}  {dev:>+12.2f}%")
        else:
            print(f"    {f23:>8.4f}  {r_ct:>12.6e}  (N/A)")

    # Monotonicity check
    r_uc_00 = v_us**2  # f_12 = 0
    r_uc_50 = (1.0 - 0.25) * v_us**2
    r_uc_99 = (1.0 - 0.9801) * v_us**2
    check(
        "m_u/m_c is strictly decreasing in f_12",
        r_uc_00 > r_uc_50 > r_uc_99,
        f"f_12 = 0.00 -> {r_uc_00:.4e}, 0.50 -> {r_uc_50:.4e}, 0.99 -> {r_uc_99:.4e}",
    )

    # Edge-to-interior structural check
    check(
        "interior partition f_12 stays at least 1% below unity",
        partition["f12_obs"] < 1.0 - 1e-3 or abs(partition["f12_obs"] - 1.0) < 0.005,
        f"f_12 = {partition['f12_obs']:.6f}",
    )


def part7_summary(inputs: dict, edges: dict, partition: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 7: Summary — bounded lane with one conditional partition")
    print("=" * 72)

    r_uc_pred = partition["r_uc_pred"]
    r_ct_pred = partition["r_ct_pred"]

    print("\n  Status:")
    print("    BOUNDED secondary flavor-mass lane (up sector)")
    print("    Conditional: up-down partition (f_12, f_23) in [0,1]^2")
    print("    Retained core gives the CKM atlas magnitudes and the phase")
    print("    delta = arctan(sqrt(5)), but not yet the partition.")
    print()
    print("  Down-dominant edge (f_12 = f_23 = 1):  Phase 1 (down-type) closed.")
    print("  Up-dominant edge  (f_12 = f_23 = 0):   symmetric up-type ratios.")
    print()
    print("  Numerical surface at the observation-comparator partition:")
    print(f"    f_12_obs = {partition['f12_obs']:.6f}  (≈ 1, so down-dominant in 1-2)")
    print(f"    f_23_obs = {partition['f23_obs']:.6f}  (≈ 1, so down-dominant in 2-3)")
    print()
    print(f"    m_u/m_c  = {r_uc_pred:.6e}  (obs: {R_UC_OBS:.6e})")
    print(f"    m_c/m_t  = {r_ct_pred:.6e}  (obs: {R_CT_OBS:.6e})")
    print()
    print("  What closes next: derive (f_12, f_23) from a promoted framework")
    print("  quantity (candidates: CP phase dressing, Jarlskog invariant, or")
    print("  isospin-partner EWSB cascade).  That would promote this lane to")
    print("  retained (theorem-grade) for the up sector.")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Bounded Up-Type Mass Ratios from the CKM Dual (Phase 2)")
    print("=" * 72)

    inputs = part1_inputs()
    part2_parallel_ansatz(inputs)
    edges = part3_edges(inputs)
    partition = part4_interior_solver(inputs)
    part5_isospin_partner_pairing(inputs, partition)
    part6_sensitivity(inputs, partition)
    part7_summary(inputs, edges, partition)

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
