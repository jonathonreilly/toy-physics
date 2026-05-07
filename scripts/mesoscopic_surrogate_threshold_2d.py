#!/usr/bin/env python3
"""2D threshold sweep for the mesoscopic-surrogate two-stage lane.

Question:
  Does shrinking the surrogate-source support produce a clear threshold where
  two-stage sourced-response stability collapses on the retained 2D family?

This is intentionally cheap:
  - retained 2D ordered-lattice family only
  - same broad-source construction as the two-stage companion
  - sweep top-N support sizes from very small to broad

The safe question is not whether the surrogate ever works. The safe question is
whether there is a support threshold below which the two-stage stability falls
apart.
"""

from __future__ import annotations

import os
import sys

try:
    import numpy as np
except ModuleNotFoundError:
    system_python = "/usr/bin/python3"
    if os.path.exists(system_python) and sys.executable != system_python:
        os.execv(system_python, [system_python, "-u", __file__, *sys.argv[1:]])
    raise SystemExit("numpy is required for this harness. On this machine use /usr/bin/python3.")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.mesoscopic_surrogate_two_stage_2d import (  # noqa: E402
    FIELD_STRENGTH,
    H,
    MAX_D_PHYS,
    PACKET_SIGMA,
    PHYS_L,
    PHYS_W,
    PROBE_Y,
    SOURCE_Y,
    detector,
    generate,
    overlap,
    point_packet,
    point_source_field,
    propagate_packet,
    profile_centroid,
    profile_spread,
    stage_metrics,
    topn_compress,
    y_profile,
)


TOPN_VALUES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 20, 25, 32, 40, 49, 64, 81)
STABILITY_REL_ERR = 0.01
STABILITY_CARRY = 0.99


def pass_check(label: str, condition: bool, detail: str) -> int:
    """Print an audit-readable check line and fail closed on violation."""
    if condition:
        print(f"  [PASS C] {label}: {detail}")
        return 1
    print(f"  [FAIL C] {label}: {detail}")
    raise AssertionError(label)


def main() -> None:
    pos, adj, nl, hw, nmap = generate(PHYS_L, PHYS_W, MAX_D_PHYS, H)
    n = len(pos)
    det = detector(nl, hw, nmap)

    bl = nl // 3
    bi = [nmap[(bl, iy)] for iy in range(-hw, hw + 1) if (bl, iy) in nmap]
    slit_iy = max(1, round(3.0 / H))
    sa = [nmap[(bl, iy)] for iy in range(slit_iy, hw + 1) if (bl, iy) in nmap]
    sb = [nmap[(bl, iy)] for iy in range(-hw, -slit_iy + 1) if (bl, iy) in nmap]
    blocked = set(bi) - set(sa + sb)

    probe_init = point_packet(n, nmap, PROBE_Y)
    free_amps = propagate_packet(pos, adj, np.zeros(n, dtype=float), probe_init, blocked, n)
    free_profile = y_profile(np.array(free_amps, dtype=np.complex128), det, pos, H)

    print("=" * 100)
    print("MESOSCOPIC SURROGATE TWO-STAGE THRESHOLD SWEEP (2D)")
    print("  Retained 2D ordered-lattice family")
    print(f"  h={H}, W={PHYS_W}, L={PHYS_L}, source_y={SOURCE_Y}, sigma={PACKET_SIGMA}")
    print("  Goal: does shrinking source support produce a clear threshold in two-stage")
    print("        sourced-response stability?")
    print("=" * 100)
    print()
    print(f"Free-profile centroid: {profile_centroid(free_profile, H):+.4f}")
    print(f"Free-profile spread:   {profile_spread(free_profile, H):.4f}")
    print(f"Probe launch y:        {PROBE_Y:+.4f}")
    print()
    print(
        f"{'topN':>6s} {'cap1':>7s} {'r1':>8s} {'r2':>8s} "
        f"{'delta2/delta1':>12s} {'carry':>7s} {'stable?':>8s}"
    )
    print("-" * 78)

    stable_topns = []
    rows = []
    for topn in TOPN_VALUES:
        src1, cap1 = topn_compress(free_profile, topn)
        stage1 = stage_metrics(pos, adj, n, nl, nmap, det, blocked, free_profile, src1, probe_init, FIELD_STRENGTH)
        src2, cap2 = topn_compress(stage1["dist_profile"], topn)
        stage2 = stage_metrics(pos, adj, n, nl, nmap, det, blocked, free_profile, src2, probe_init, FIELD_STRENGTH)
        carry = overlap(src1, src2)
        rel = abs(stage2["ratio"] - stage1["ratio"]) / max(abs(stage1["ratio"]), 1e-30)
        stable = rel <= STABILITY_REL_ERR and carry >= STABILITY_CARRY
        row = {
            "topn": topn,
            "cap1": cap1,
            "cap2": cap2,
            "stage1_ratio": stage1["ratio"],
            "stage2_ratio": stage2["ratio"],
            "ratio_rel_err": rel,
            "carry": carry,
            "stable": stable,
        }
        rows.append(row)
        if stable:
            stable_topns.append(topn)
        delta_ratio = stage2["ratio"] / stage1["ratio"] if abs(stage1["ratio"]) > 1e-30 else 0.0
        print(
            f"{topn:6d} {cap1:7.3f} {stage1['ratio']:8.3f} {stage2['ratio']:8.3f} "
            f"{delta_ratio:12.3f} {carry:7.3f} {('YES' if stable else 'NO'):>8s}"
        )

    print()
    if stable_topns:
        print(f"First stable topN in scanned range: {stable_topns[0]}")
        print(f"Stable topNs in scanned range: {stable_topns}")
    else:
        print("No stable topN found in the scanned range.")

    print()
    print("SAFE READ")
    print("  - If stability is present for all scanned topN, there is no sharp support")
    print("    threshold in this 2D companion family.")
    print("  - If stability fails only below some topN, that would identify a real")
    print("    mesoscopic support floor.")
    print("  - The honest output is whichever of those two cases the frozen scan shows.")

    min_carry = min(row["carry"] for row in rows)
    max_ratio_rel_err = max(row["ratio_rel_err"] for row in rows)
    worst_ratio_row = max(rows, key=lambda row: row["ratio_rel_err"])
    pass_count = 0
    print()
    print("AUDIT CHECKS")
    pass_count += pass_check(
        "frozen_topN_support_list_scanned",
        tuple(row["topn"] for row in rows) == TOPN_VALUES,
        f"scanned topN={list(TOPN_VALUES)}",
    )
    pass_count += pass_check(
        "all_scanned_topN_stable",
        stable_topns == list(TOPN_VALUES),
        f"stable_topNs={stable_topns}",
    )
    pass_count += pass_check(
        "stage_ratio_relative_error_within_one_percent",
        max_ratio_rel_err <= STABILITY_REL_ERR,
        (
            f"max_rel_err={max_ratio_rel_err:.6g} <= {STABILITY_REL_ERR:.6g} "
            f"at topN={worst_ratio_row['topn']}"
        ),
    )
    pass_count += pass_check(
        "support_carry_floor",
        min_carry >= STABILITY_CARRY,
        f"min_carry={min_carry:.6g} >= {STABILITY_CARRY:.6g}",
    )
    pass_count += pass_check(
        "no_sharp_collapse_in_scanned_range",
        stable_topns and stable_topns[0] == TOPN_VALUES[0],
        f"first stable topN={stable_topns[0] if stable_topns else None}",
    )
    print()
    print(f"SUMMARY: PASS={pass_count} FAIL=0")


if __name__ == "__main__":
    main()
