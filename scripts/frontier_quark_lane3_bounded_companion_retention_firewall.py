#!/usr/bin/env python3
"""Lane 3 bounded-companion retention firewall.

The current quark-mass packet contains strong bounded companion matches, but
it does not retain the five non-top quark masses. This runner verifies the
claim boundary using repo-local notes and the current numerical support
surface.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


PASS_COUNT = 0
FAIL_COUNT = 0

ROOT = Path(__file__).resolve().parents[1]


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# Existing runner comparator constants. These are not derivation inputs.
M_U_OBS = 2.16e-3
M_C_OBS = 1.273
M_T_OBS = 172.57
M_D_OBS = 4.67e-3
M_S_OBS = 93.4e-3
M_B_OBS = 4.180

R_UC_OBS = M_U_OBS / M_C_OBS
R_CT_OBS = M_C_OBS / M_T_OBS
R_DS_OBS = M_D_OBS / M_S_OBS
R_SB_OBS = M_S_OBS / M_B_OBS


def part1_repo_claim_state() -> None:
    section("Part 1: repo claim-state guardrails")
    lane = read("docs/lanes/open_science/03_QUARK_MASS_RETENTION_OPEN_LANE_2026-04-26.md")
    packet = read("docs/QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md")
    down = read("docs/DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md")
    up = read("docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md")
    bottom = read("docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md")

    check(
        "Lane 3 stub says only top is retained",
        "the top mass is retained; the remaining five quark" in lane
        and "the only retained quark mass" in lane
        and "Direct retention of m_d, m_s, m_b, m_u, m_c" in lane,
    )
    check(
        "review packet says no retained-spectrum promotion",
        "It does not promote the full" in packet
        and "quark spectrum to retained closure" in packet
        and "full quark-spectrum closure is not yet a retained framework claim" in packet,
    )
    check(
        "down-type note is bounded, not retained",
        "**Status:** bounded secondary lane" in down
        and "This lane is **bounded**, not retained or theorem-grade" in down,
    )
    check(
        "up-amplitude scan says no retained derivation of a_u",
        "does **not** derive the remaining" in up
        and "no retained derivation of `a_u`" in up,
    )
    check(
        "b-Yukawa note closes species-uniform Ward reuse negatively",
        "species-uniform interpretation" in bottom
        and "falsifies" in bottom
        and "species-differentiation primitive" in bottom,
    )


def part2_down_type_ratio_firewall() -> None:
    section("Part 2: down-type ratio support is not absolute mass retention")
    alpha = CANONICAL_ALPHA_S_V
    v_cb = alpha / math.sqrt(6.0)
    exponent = 5.0 / 6.0
    r_ds = alpha / 2.0
    r_sb = v_cb ** (1.0 / exponent)
    r_db = r_ds * r_sb
    dev_ds = (r_ds - R_DS_OBS) / R_DS_OBS
    dev_sb = (r_sb - R_SB_OBS) / R_SB_OBS

    print(f"  alpha_s(v) = {alpha:.12f}")
    print(f"  m_d/m_s = {r_ds:.8f}; comparator deviation = {dev_ds:+.2%}")
    print(f"  m_s/m_b = {r_sb:.8f}; comparator deviation = {dev_sb:+.2%}")
    print(f"  m_d/m_b = {r_db:.8f}")

    check(
        "down-type formulas reproduce the bounded support values",
        abs(r_ds - 0.051651908061) < 1.0e-10
        and abs(r_sb - 0.02238973) < 1.0e-7,
    )
    check(
        "down-type ratios match threshold-local comparators but remain bounded",
        abs(dev_ds) < 0.05 and abs(dev_sb) < 0.01,
        f"dev_ds={dev_ds:+.2%}, dev_sb={dev_sb:+.2%}",
    )

    mb_anchor_a = M_B_OBS
    mb_anchor_b = 2.0 * M_B_OBS
    masses_a = (r_db * mb_anchor_a, r_sb * mb_anchor_a, mb_anchor_a)
    masses_b = (r_db * mb_anchor_b, r_sb * mb_anchor_b, mb_anchor_b)
    ratio_preserved = (
        abs((masses_a[0] / masses_a[1]) - (masses_b[0] / masses_b[1])) < 1.0e-14
        and abs((masses_a[1] / masses_a[2]) - (masses_b[1] / masses_b[2])) < 1.0e-14
    )
    check(
        "ratio formulas leave an arbitrary absolute bottom anchor",
        ratio_preserved and abs(masses_b[2] / masses_a[2] - 2.0) < 1.0e-14,
        f"m_b anchors {mb_anchor_a:.2f} GeV and {mb_anchor_b:.2f} GeV preserve ratios",
    )


def part3_up_type_partition_firewall() -> None:
    section("Part 3: up-type branch remains partition/scalar-law bounded")
    alpha = CANONICAL_ALPHA_S_V
    v_us = math.sqrt(alpha / 2.0)
    v_cb = alpha / math.sqrt(6.0)

    f12_obs = math.sqrt(R_DS_OBS / (v_us * v_us))
    f23_obs = math.sqrt((R_SB_OBS ** (5.0 / 3.0)) / (v_cb * v_cb))
    r_uc = (1.0 - f12_obs * f12_obs) * v_us * v_us
    r_ct = (math.sqrt(1.0 - f23_obs * f23_obs) * v_cb) ** (6.0 / 5.0)
    dev_uc = (r_uc - R_UC_OBS) / R_UC_OBS
    dev_ct = (r_ct - R_CT_OBS) / R_CT_OBS

    print(f"  f_12 comparator partition = {f12_obs:.6f}")
    print(f"  f_23 comparator partition = {f23_obs:.6f}")
    print(f"  m_u/m_c from comparator partition = {r_uc:.9e} ({dev_uc:+.2%})")
    print(f"  m_c/m_t from comparator partition = {r_ct:.9e} ({dev_ct:+.2%})")

    check(
        "up-type comparator partition is close to the down-dominant edge",
        0.98 < f12_obs < 1.0 and 0.99 < f23_obs < 1.0,
        f"f12={f12_obs:.6f}, f23={f23_obs:.6f}",
    )
    check(
        "m_u/m_c is near comparator but still partition-selected",
        abs(dev_uc) < 0.05,
        f"dev_uc={dev_uc:+.2%}",
    )
    check(
        "current CP-orthogonal m_c/m_t remains about an order low",
        dev_ct < -0.80,
        f"dev_ct={dev_ct:+.2%}",
    )


def part4_ward_reuse_firewall() -> None:
    section("Part 4: top Ward identity does not species-uniformly retain m_b")
    y_t_ward = 1.0 / math.sqrt(6.0)
    bottom_framework = 145.07
    ratio = bottom_framework / M_B_OBS

    print(f"  y_t/g_s Ward ratio = 1/sqrt(6) = {y_t_ward:.10f}")
    print(f"  species-uniform b prediction from existing analysis = {bottom_framework:.2f} GeV")
    print(f"  observed comparator m_b(m_b) = {M_B_OBS:.2f} GeV")
    print(f"  overshoot = {ratio:.1f}x")

    check(
        "top Ward ratio is exact but top-channel scoped",
        abs(y_t_ward - 0.4082482904638631) < 1.0e-15,
    )
    check(
        "species-uniform physical reuse overshoots m_b by > 30x",
        ratio > 30.0,
        f"ratio={ratio:.1f}x",
    )
    check(
        "absolute non-top Yukawas require species differentiation",
        "species-differentiation primitive" in read("docs/YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md"),
        "species-uniform reading closed negatively; new primitive required",
    )


def part5_safe_endpoint() -> None:
    section("Part 5: safe endpoint")
    lane = read("docs/lanes/open_science/03_QUARK_MASS_RETENTION_OPEN_LANE_2026-04-26.md")
    note = read("docs/QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md")
    check(
        "CKM closure is not a five-mass closure theorem",
        "CKM closure is a mixing theorem, not a mass-retention theorem" in note,
        "mixing package needs mass-ratio bridges and selectors before retention",
    )
    check(
        "Lane 3 honest status is open, not retained closure",
        "ACCEPTED CRITICAL OPEN SCIENCE LANE" in lane
        and "the remaining five quark" in lane
        and "Lane 3 remains open" in note,
        "open gates: 5/6 NP proof, up scalar/partition law, generation-stratified Ward",
    )
    check(
        "firewall does not use observed masses as derivation inputs",
        "No observed quark mass is used as a derivation input" in note,
        "PDG values are comparator/sensitivity only",
    )


def main() -> int:
    print("=" * 88)
    print("LANE 3 QUARK BOUNDED-COMPANION RETENTION FIREWALL")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the current CKM/quark-mass support packet be promoted to")
    print("  retained m_u, m_d, m_s, m_c, and m_b closure?")
    print()
    print("Answer:")
    print("  No. The packet is strong bounded support, not five-mass retention.")

    part1_repo_claim_state()
    part2_down_type_ratio_firewall()
    part3_up_type_partition_firewall()
    part4_ward_reuse_firewall()
    part5_safe_endpoint()

    print()
    print("=" * 88)
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
