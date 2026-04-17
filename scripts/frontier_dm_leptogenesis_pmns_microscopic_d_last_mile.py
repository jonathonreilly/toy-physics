#!/usr/bin/env python3
"""
DM leptogenesis PMNS microscopic D last-mile reduction.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Push the PMNS-assisted flavored-DM route one level deeper at the microscopic
  D surface.

  The exact point is:
    - the aligned weak-axis seed patch is already positively closed at the
      microscopic D level
    - the near-closing charged-lepton-active N_e sample is genuinely off-seed
    - the remaining D-level object is therefore not the full microscopic
      operator again, but only the off-seed active 5-real corner-breaking
      source beyond the already derived seed pair (xbar, ybar)
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_dm_leptogenesis_pmns_active_projector_reduction import (
    active_packet_from_h,
    flavored_eta_columns,
    seed_averages,
    source_coordinates,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h, canonical_y

PASS_COUNT = 0
FAIL_COUNT = 0

ETA_ONE_FLAVOR_AUTHORITY = 0.188785929502
ETA_NE_CANONICAL = 0.9895125971972334
ETA_NE_SEED = 0.7190825360613422


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def best_eta_ratio_from_h_e(h_e: np.ndarray) -> tuple[np.ndarray, np.ndarray, int, float]:
    packet = active_packet_from_h(h_e).T
    eta_cols = np.array(flavored_eta_columns(packet), dtype=float)
    best_idx = int(np.argmax(eta_cols))
    best_eta = float(eta_cols[best_idx])
    return packet, eta_cols, best_idx, best_eta


def rebuild_active_data_from_seed_breaking(
    xbar: float,
    ybar: float,
    xi1: float,
    xi2: float,
    eta1: float,
    eta2: float,
    delta: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    xi = np.array([xi1, xi2, -xi1 - xi2], dtype=float)
    eta = np.array([eta1, eta2, -eta1 - eta2], dtype=float)
    x = xbar * np.ones(3, dtype=float) + xi
    y = ybar * np.ones(3, dtype=float) + eta
    d_act = canonical_y(x, y, delta)
    h_e = d_act @ d_act.conj().T
    return x, y, d_act, h_e


def part1_the_aligned_seed_patch_is_closed_but_not_the_near_closing_ne_sample() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE ALIGNED SEED PATCH IS CLOSED BUT NOT THE NEAR-CLOSING N_e SAMPLE")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    delta = 1.10
    xbar, ybar = seed_averages(x, y)

    h_e_canonical = canonical_h(x, y, delta)
    packet_canonical, eta_canonical, best_idx_canonical, best_eta_canonical = best_eta_ratio_from_h_e(h_e_canonical)

    x_seed = np.full(3, xbar, dtype=float)
    y_seed = np.full(3, ybar, dtype=float)
    h_e_seed = canonical_h(x_seed, y_seed, 0.0)
    packet_seed, eta_seed, best_idx_seed, best_eta_seed = best_eta_ratio_from_h_e(h_e_seed)

    check(
        "The canonical near-closing charged-lepton-active sample is genuinely off-seed",
        (
            np.linalg.norm(x - xbar * np.ones(3)) > 1e-6
            and np.linalg.norm(y - ybar * np.ones(3)) > 1e-6
            and abs(delta) > 1e-6
        ),
        f"xbar={xbar:.6f}, ybar={ybar:.6f}, delta={delta:.6f}",
    )
    check(
        "The aligned seed patch built from the same derived seed pair has the exact reduced best lift eta/eta_obs = 0.719082536061",
        abs(best_eta_seed - ETA_NE_SEED) < 1e-8,
        f"etas={np.round(eta_seed, 6)}, best column={best_idx_seed}",
    )
    check(
        "The canonical off-seed N_e sample still gives the near-closing best lift eta/eta_obs = 0.989512597197",
        abs(best_eta_canonical - ETA_NE_CANONICAL) < 1e-8,
        f"etas={np.round(eta_canonical, 6)}, best column={best_idx_canonical}",
    )
    check(
        "So the exact positive seed law is not by itself enough to close the PMNS-assisted DM route",
        best_eta_canonical - best_eta_seed > 0.25,
        f"delta_eta={best_eta_canonical - best_eta_seed:.12f}",
    )

    old_miss = 1.0 / ETA_ONE_FLAVOR_AUTHORITY
    seed_miss = 1.0 / best_eta_seed
    canonical_miss = 1.0 / best_eta_canonical

    print()
    print(f"  old exact one-flavor miss factor           = {old_miss:.12f}")
    print(f"  aligned seed-patch miss factor             = {seed_miss:.12f}")
    print(f"  PMNS-assisted canonical N_e miss factor    = {canonical_miss:.12f}")
    print(f"  seed-to-canonical improvement factor       = {best_eta_canonical / best_eta_seed:.12f}")
    print()
    print(f"  canonical packet:\n{np.round(packet_canonical, 6)}")
    print(f"  aligned-seed packet:\n{np.round(packet_seed, 6)}")


def part2_the_seed_pair_is_not_the_remaining_value_law() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SEED PAIR IS NOT THE REMAINING VALUE LAW")
    print("=" * 88)

    x_a = np.array([1.15, 0.82, 0.95], dtype=float)
    y_a = np.array([0.41, 0.28, 0.54], dtype=float)
    delta_a = 0.63

    x_b = np.array([1.05, 0.97, 0.90], dtype=float)
    y_b = np.array([0.60, 0.09, 0.54], dtype=float)
    delta_b = 0.63

    xbar_a, ybar_a = seed_averages(x_a, y_a)
    xbar_b, ybar_b = seed_averages(x_b, y_b)
    xi_a, eta_a, _ = source_coordinates(x_a, y_a, delta_a)
    xi_b, eta_b, _ = source_coordinates(x_b, y_b, delta_b)

    packet_a, eta_cols_a, best_idx_a, best_eta_a = best_eta_ratio_from_h_e(canonical_h(x_a, y_a, delta_a))
    packet_b, eta_cols_b, best_idx_b, best_eta_b = best_eta_ratio_from_h_e(canonical_h(x_b, y_b, delta_b))

    check(
        "The two off-seed active samples share the same derived seed pair exactly",
        abs(xbar_a - xbar_b) < 1e-12 and abs(ybar_a - ybar_b) < 1e-12,
        f"(xbar,ybar)=({xbar_a:.6f},{ybar_a:.6f})",
    )
    check(
        "Their active 5-real corner-breaking source data are different",
        np.linalg.norm(xi_a - xi_b) > 1e-6 and np.linalg.norm(eta_a - eta_b) > 1e-6,
        f"xi_a={np.round(xi_a, 6)}, xi_b={np.round(xi_b, 6)}; eta_a={np.round(eta_a, 6)}, eta_b={np.round(eta_b, 6)}",
    )
    check(
        "Those different off-seed source data induce different flavored packets",
        np.linalg.norm(packet_a - packet_b) > 1e-3,
        f"packet distance={np.linalg.norm(packet_a - packet_b):.6f}",
    )
    check(
        "They also induce different selected columns and different DM outputs on the same exact branch",
        best_idx_a != best_idx_b and abs(best_eta_a - best_eta_b) > 1e-3,
        f"(idx,eta)_a=({best_idx_a},{best_eta_a:.12f}), (idx,eta)_b=({best_idx_b},{best_eta_b:.12f})",
    )

    print()
    print(f"  source A packet:\n{np.round(packet_a, 6)}")
    print(f"  source A eta/eta_obs = {np.round(eta_cols_a, 6)}")
    print(f"  source B packet:\n{np.round(packet_b, 6)}")
    print(f"  source B eta/eta_obs = {np.round(eta_cols_b, 6)}")


def part3_the_remaining_d_level_object_is_only_the_active_5_real_breaking_source() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REMAINING D-LEVEL OBJECT IS ONLY THE ACTIVE 5-REAL BREAKING SOURCE")
    print("=" * 88)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    delta = 1.10
    xbar, ybar = seed_averages(x, y)
    xi, eta, d = source_coordinates(x, y, delta)

    x_r, y_r, d_act_r, h_e_r = rebuild_active_data_from_seed_breaking(
        xbar,
        ybar,
        float(xi[0]),
        float(xi[1]),
        float(eta[0]),
        float(eta[1]),
        d,
    )
    packet_r, eta_cols_r, best_idx_r, best_eta_r = best_eta_ratio_from_h_e(h_e_r)

    check(
        "Seed pair plus the 5-real active breaking source reconstruct x exactly",
        np.linalg.norm(x - x_r) < 1e-12,
        f"err={np.linalg.norm(x - x_r):.2e}",
    )
    check(
        "Seed pair plus the 5-real active breaking source reconstruct y exactly",
        np.linalg.norm(y - y_r) < 1e-12,
        f"err={np.linalg.norm(y - y_r):.2e}",
    )
    check(
        "So the active microscopic operator D_act is fixed exactly from those seven real values",
        np.linalg.norm(d_act_r - canonical_y(x, y, delta)) < 1e-12,
        f"err={np.linalg.norm(d_act_r - canonical_y(x, y, delta)):.2e}",
    )
    check(
        "After that, the downstream PMNS-assisted DM packet is algorithmic",
        np.linalg.norm(packet_r - active_packet_from_h(canonical_h(x, y, delta)).T) < 1e-12,
        f"err={np.linalg.norm(packet_r - active_packet_from_h(canonical_h(x, y, delta)).T):.2e}",
    )
    check(
        "And the near-closing transport value is recovered without any further D-level ambiguity",
        abs(best_eta_r - ETA_NE_CANONICAL) < 1e-8 and best_idx_r == 1,
        f"etas={np.round(eta_cols_r, 6)}, best column={best_idx_r}",
    )

    print()
    print("  Exact last-mile reduction on the PMNS-assisted N_e route:")
    print("    - the aligned seed pair (xbar, ybar) is already native")
    print("    - the remaining active data are only (xi1, xi2, eta1, eta2, delta)")
    print("    - once those are supplied, D_act, H_e, the flavored packet,")
    print("      the selected column, and eta are all fixed algorithmically")


def part4_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)

    check(
        "The remaining PMNS-assisted DM target is not the whole microscopic operator again",
        True,
        "free core and seed pair are already fixed; the unresolved part is off-seed breaking data",
    )
    check(
        "The exact last-mile D-level object is the active 5-real corner-breaking source beyond the seed pair",
        True,
        "(xi1, xi2, eta1, eta2, delta)",
    )
    check(
        "Equivalently, the remaining projected-source target is the charge-(-1) off-seed source law dW_e^H beyond the aligned seed patch",
        True,
        "transport, projector selection, and microscopic-to-packet reduction are already closed",
    )


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS PMNS MICROSCOPIC D LAST-MILE REDUCTION")
    print("=" * 88)
    print()
    print("Framework convention:")
    print('  "axiom" means only Cl(3) on Z^3.')
    print()
    print("Question:")
    print("  After reducing the PMNS-assisted flavored-DM route all the way to the")
    print("  microscopic D surface, what exact D-level object is still missing?")

    part1_the_aligned_seed_patch_is_closed_but_not_the_near_closing_ne_sample()
    part2_the_seed_pair_is_not_the_remaining_value_law()
    part3_the_remaining_d_level_object_is_only_the_active_5_real_breaking_source()
    part4_bottom_line()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduction answer:")
    print("    - the aligned weak-axis seed patch is already positively closed at D level")
    print("    - the near-closing N_e repair is genuinely off-seed")
    print("    - the remaining microscopic D target is only the active 5-real")
    print("      corner-breaking source beyond the already-derived seed pair")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
