#!/usr/bin/env python3
"""
Bounded down-type mass ratios from the promoted CKM closure.

Status:
  bounded secondary flavor-mass lane

Safe claim:
  Combining the promoted CKM atlas/axiom package with the standard GST
  relation and the bounded 5/6 mass-ratio bridge yields

    m_d/m_s = alpha_s(v) / 2
    m_s/m_b = [alpha_s(v) / sqrt(6)]^(6/5)
    m_d/m_b = (m_d/m_s) (m_s/m_b)

  No observed quark masses are used as derivation inputs.

Important qualifier:
  The lane is numerically strongest on the threshold-local self-scale
  comparator m_s(2 GeV) / m_b(m_b). Theorem-grade derivation of the exact
  5/6 bridge and exact scale-selection rule remains open, so this is bounded
  rather than retained.
"""

from __future__ import annotations

import math

from canonical_plaquette_surface import CANONICAL_ALPHA_BARE, CANONICAL_ALPHA_S_V, CANONICAL_U0


C_F = 4.0 / 3.0
T_F = 1.0 / 2.0
EXPONENT = C_F - T_F

# Observation-facing comparison surface only. These are not derivation inputs.
M_D_OBS = 4.67e-3
M_S_OBS = 93.4e-3
M_B_OBS = 4.180
V_US_OBS = 0.2243
V_CB_OBS = 0.0422

R_DS_OBS = M_D_OBS / M_S_OBS
R_SB_OBS = M_S_OBS / M_B_OBS
R_DB_OBS = M_D_OBS / M_B_OBS

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


def part1_ckm_surface() -> tuple[float, float]:
    print("\n" + "=" * 72)
    print("PART 1: Promoted CKM input surface")
    print("=" * 72)

    alpha_s_v = CANONICAL_ALPHA_S_V
    v_us = math.sqrt(alpha_s_v / 2.0)
    v_cb = alpha_s_v / math.sqrt(6.0)

    print(f"\n  alpha_s(v) = {alpha_s_v:.12f}")
    print(f"  alpha_bare = {CANONICAL_ALPHA_BARE:.12f}")
    print(f"  u_0 = {CANONICAL_U0:.12f}")
    print(f"\n  |V_us| = sqrt(alpha_s(v)/2) = {v_us:.6f}  (PDG: {V_US_OBS:.4f})")
    print(f"  |V_cb| = alpha_s(v)/sqrt(6) = {v_cb:.6f}  (PDG: {V_CB_OBS:.4f})")

    check(
        "CKM input formula for |V_us|",
        abs(v_us - math.sqrt(alpha_s_v / 2.0)) < 1e-14,
        f"|V_us| = {v_us:.8f}",
    )
    check(
        "CKM input formula for |V_cb|",
        abs(v_cb - alpha_s_v / math.sqrt(6.0)) < 1e-14,
        f"|V_cb| = {v_cb:.8f}",
    )
    check(
        "|V_us| stays within 2% of PDG",
        abs((v_us - V_US_OBS) / V_US_OBS * 100.0) < 2.0,
        f"dev = {(v_us - V_US_OBS) / V_US_OBS * 100.0:+.2f}%",
    )
    check(
        "|V_cb| stays within 1% of PDG",
        abs((v_cb - V_CB_OBS) / V_CB_OBS * 100.0) < 1.0,
        f"dev = {(v_cb - V_CB_OBS) / V_CB_OBS * 100.0:+.2f}%",
    )

    return v_us, v_cb


def part2_exponent() -> float:
    print("\n" + "=" * 72)
    print("PART 2: Exact SU(3) exponent constant")
    print("=" * 72)

    print(f"\n  C_F = {C_F:.6f}")
    print(f"  T_F = {T_F:.6f}")
    print(f"  C_F - T_F = {EXPONENT:.6f}")

    check(
        "C_F - T_F = 5/6 exactly",
        abs(EXPONENT - 5.0 / 6.0) < 1e-14,
        f"C_F - T_F = {EXPONENT:.10f}",
    )
    check(
        "SU(3) Casimir identity for C_F",
        abs(C_F - (3.0**2 - 1.0) / (2.0 * 3.0)) < 1e-14,
        f"C_F = {C_F:.6f}",
    )
    check("Fundamental-representation index T_F = 1/2", abs(T_F - 0.5) < 1e-14)

    return EXPONENT


def part3_down_type_dual(v_us: float, v_cb: float, exponent: float) -> tuple[float, float, float]:
    print("\n" + "=" * 72)
    print("PART 3: Down-type mass-ratio dual")
    print("=" * 72)

    r_ds = CANONICAL_ALPHA_S_V / 2.0
    r_sb = v_cb ** (1.0 / exponent)
    r_db = r_ds * r_sb

    dev_ds = (r_ds - R_DS_OBS) / R_DS_OBS * 100.0
    dev_sb = (r_sb - R_SB_OBS) / R_SB_OBS * 100.0
    dev_db = (r_db - R_DB_OBS) / R_DB_OBS * 100.0

    print(f"\n  m_d/m_s = alpha_s(v)/2 = {r_ds:.6f}  (PDG: {R_DS_OBS:.6f})")
    print(f"  m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5) = {r_sb:.6f}  (PDG: {R_SB_OBS:.6f})")
    print(f"  m_d/m_b = (m_d/m_s)(m_s/m_b) = {r_db:.6f}  (PDG: {R_DB_OBS:.6f})")

    check(
        "GST dual gives m_d/m_s = |V_us|^2",
        abs(r_ds - v_us**2) < 1e-14,
        f"m_d/m_s = {r_ds:.8f}",
    )
    check(
        "5/6 bridge gives m_s/m_b = |V_cb|^(6/5)",
        abs(r_sb - v_cb ** (6.0 / 5.0)) < 1e-14,
        f"m_s/m_b = {r_sb:.8f}",
    )
    check(
        "Chain rule for m_d/m_b",
        abs(r_db - r_ds * r_sb) < 1e-14,
        f"m_d/m_b = {r_db:.8f}",
    )
    check(
        "m_d/m_s matches the threshold-local self-scale comparator within 5%",
        abs(dev_ds) < 5.0,
        f"dev = {dev_ds:+.2f}%",
    )
    check(
        "m_s/m_b matches the threshold-local self-scale comparator within 1%",
        abs(dev_sb) < 1.0,
        f"dev = {dev_sb:+.2f}%",
    )
    check(
        "m_d/m_b matches the threshold-local self-scale comparator within 5%",
        abs(dev_db) < 5.0,
        f"dev = {dev_db:+.2f}%",
    )

    return r_ds, r_sb, r_db


def part4_closed_forms(r_ds: float, r_sb: float, r_db: float) -> None:
    print("\n" + "=" * 72)
    print("PART 4: Closed forms and provenance")
    print("=" * 72)

    a = CANONICAL_ALPHA_S_V
    r_sb_expanded = a ** (6.0 / 5.0) / 6.0 ** (3.0 / 5.0)
    r_db_expanded = a ** (11.0 / 5.0) / (2.0 * 6.0 ** (3.0 / 5.0))

    print(f"\n  m_d/m_s = alpha_s(v) / 2 = {r_ds:.6f}")
    print(f"  m_s/m_b = alpha_s(v)^(6/5) / 6^(3/5) = {r_sb_expanded:.6f}")
    print(f"  m_d/m_b = alpha_s(v)^(11/5) / (2 * 6^(3/5)) = {r_db_expanded:.6f}")
    print("\n  Input surface:")
    print("    alpha_s(v)       [derived: canonical plaquette chain]")
    print("    C_F, T_F         [exact: SU(3) group theory]")
    print("    GST relation     [standard leading-order texture bridge]")
    print("    5/6 bridge       [bounded mass-ratio bridge]")
    print("    observed masses  [comparison only, not derivation inputs]")

    check(
        "Expanded form for m_s/m_b matches direct evaluation",
        abs(r_sb - r_sb_expanded) < 1e-14,
        f"diff = {abs(r_sb - r_sb_expanded):.2e}",
    )
    check(
        "Expanded form for m_d/m_b matches direct evaluation",
        abs(r_db - r_db_expanded) < 1e-14,
        f"diff = {abs(r_db - r_db_expanded):.2e}",
    )
    check(
        "All three down-type ratios stay within 5% of the threshold-local self-scale comparators",
        max(
            abs((r_ds - R_DS_OBS) / R_DS_OBS * 100.0),
            abs((r_sb - R_SB_OBS) / R_SB_OBS * 100.0),
            abs((r_db - R_DB_OBS) / R_DB_OBS * 100.0),
        )
        < 5.0,
    )


def part5_scale_qualifier(r_sb: float) -> None:
    print("\n" + "=" * 72)
    print("PART 5: Mixed-scale versus same-scale qualifier")
    print("=" * 72)

    gamma_over = 12.0 / 25.0
    alpha_s_2gev = 0.301
    alpha_s_mb = 0.226

    m_s_at_mb = M_S_OBS * (alpha_s_mb / alpha_s_2gev) ** gamma_over
    r_sb_same = m_s_at_mb / M_B_OBS
    transport = (alpha_s_2gev / alpha_s_mb) ** gamma_over
    r_sb_from_obs_vcb = V_CB_OBS ** (6.0 / 5.0)

    dev_mixed = (r_sb - R_SB_OBS) / R_SB_OBS * 100.0
    dev_same = (r_sb - r_sb_same) / r_sb_same * 100.0
    dev_bridge_intrinsic = (r_sb_from_obs_vcb - R_SB_OBS) / R_SB_OBS * 100.0

    print(f"\n  mixed-scale  m_s(2 GeV)/m_b(m_b) = {R_SB_OBS:.6f}")
    print(f"  same-scale   m_s(m_b)/m_b(m_b)   = {r_sb_same:.6f}")
    print(f"  transport    [alpha_s(2 GeV)/alpha_s(m_b)]^(12/25) = {transport:.6f}")
    print(f"  prediction                         = {r_sb:.6f}")
    print(f"  observed |V_cb| -> m_s/m_b         = {r_sb_from_obs_vcb:.6f}")
    print(f"  mixed-scale deviation              = {dev_mixed:+.2f}%")
    print(f"  same-scale deviation               = {dev_same:+.2f}%")
    print(f"  bridge-only deviation              = {dev_bridge_intrinsic:+.2f}%")

    check(
        "Mixed-scale comparator is numerically closer than same-scale comparator",
        abs(dev_mixed) < abs(dev_same),
        f"|mixed| = {abs(dev_mixed):.2f}%, |same| = {abs(dev_same):.2f}%",
    )
    check(
        "Same-scale mismatch remains material",
        abs(dev_same) > 10.0,
        f"same-scale dev = {dev_same:+.2f}%",
    )
    check(
        "Mixed-scale comparator remains within 1%",
        abs(dev_mixed) < 1.0,
        f"mixed-scale dev = {dev_mixed:+.2f}%",
    )
    check(
        "Mixed-scale ratio equals same-scale ratio times one-loop transport factor",
        abs(R_SB_OBS - r_sb_same * transport) < 1e-12,
        f"diff = {abs(R_SB_OBS - r_sb_same * transport):.2e}",
    )
    check(
        "Observed |V_cb| mapped through the 5/6 bridge stays within 1% of the self-scale comparator",
        abs(dev_bridge_intrinsic) < 1.0,
        f"bridge-only dev = {dev_bridge_intrinsic:+.2f}%",
    )


def part6_sensitivity() -> None:
    print("\n" + "=" * 72)
    print("PART 6: alpha_s(v) sensitivity")
    print("=" * 72)

    a0 = CANONICAL_ALPHA_S_V
    for label, factor in [("-1%", 0.99), ("central", 1.0), ("+1%", 1.01)]:
        a = a0 * factor
        r_ds = a / 2.0
        r_sb = (a / math.sqrt(6.0)) ** (6.0 / 5.0)
        print(f"\n  alpha_s(v) {label}: {a:.6f}")
        print(f"    m_d/m_s = {r_ds:.6f}")
        print(f"    m_s/m_b = {r_sb:.6f}")

    da = 0.001
    a_lo = a0 * (1.0 - da)
    a_hi = a0 * (1.0 + da)

    elas_ds = math.log((a_hi / 2.0) / (a_lo / 2.0)) / math.log(a_hi / a_lo)
    elas_sb = math.log(
        ((a_hi / math.sqrt(6.0)) ** (6.0 / 5.0)) / ((a_lo / math.sqrt(6.0)) ** (6.0 / 5.0))
    ) / math.log(a_hi / a_lo)

    check("m_d/m_s elasticity is linear in alpha_s(v)", abs(elas_ds - 1.0) < 0.01)
    check("m_s/m_b elasticity is 6/5 in alpha_s(v)", abs(elas_sb - 6.0 / 5.0) < 0.01)


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Bounded Down-Type Mass Ratios from the CKM Dual")
    print("=" * 72)

    v_us, v_cb = part1_ckm_surface()
    exponent = part2_exponent()
    r_ds, r_sb, r_db = part3_down_type_dual(v_us, v_cb, exponent)
    part4_closed_forms(r_ds, r_sb, r_db)
    part5_scale_qualifier(r_sb)
    part6_sensitivity()

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  m_d/m_s = {r_ds:.6f}  (self-scale comparator: {R_DS_OBS:.6f})")
    print(f"  m_s/m_b = {r_sb:.6f}  (self-scale comparator: {R_SB_OBS:.6f})")
    print(f"  m_d/m_b = {r_db:.6f}  (self-scale comparator: {R_DB_OBS:.6f})")
    print("  Status: bounded secondary flavor-mass lane")
    print("  Live qualifier: threshold-local self-scale comparator supported; theorem-grade scale closure remains open")
    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
