#!/usr/bin/env python3
"""Exact reduction of PMNS nonzero-current production on the strong route.

Question:
  After fixed-slice readout closure, what is the strongest honest next
  PMNS-native microscopic target for producing nonzero J_chi?

Answer:
  On the strong PMNS-native microscopic lane, the remaining production object
  is exactly the active off-seed five-real packet
  (xi1, xi2, eta1, eta2, delta) beyond the already closed seed pair.

  Seed pair plus that packet reconstruct the active block exactly, so J_chi is
  algorithmic from it. Distinct packets with the same seed-facing transport
  summaries still carry distinct nonzero J_chi.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_pmns_c3_nontrivial_current_boundary import nontrivial_character_current
from frontier_pmns_corner_transport_active_block import (
    active_corner_transport,
    decompose_seed_breaking,
    orbit_average_transport,
    transport_breaking_vector,
)
from frontier_pmns_transfer_operator_dominant_mode import projected_transfer_kernel_from_active_block
from pmns_lower_level_utils import circularity_guard

ROOT = Path(__file__).resolve().parents[1]
np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def active_five_real_packet(x: np.ndarray, y: np.ndarray, delta: float) -> tuple[float, float, float, float, float]:
    xbar, ybar, xi, eta, d = decompose_seed_breaking(x, y, delta)
    return float(xi[0]), float(xi[1]), float(eta[0]), float(eta[1]), float(d)


def rebuild_from_seed_and_packet(
    xbar: float,
    ybar: float,
    packet: tuple[float, float, float, float, float],
) -> np.ndarray:
    xi1, xi2, eta1, eta2, delta = packet
    x = np.array([xbar + xi1, xbar + xi2, xbar - xi1 - xi2], dtype=float)
    y = np.array([ybar + eta1, ybar + eta2, ybar - eta1 - eta2], dtype=float)
    return active_corner_transport(x, y, delta)


def sample_a() -> tuple[np.ndarray, np.ndarray, float]:
    return (
        np.array([1.15, 0.82, 0.95], dtype=float),
        np.array([0.41, 0.28, 0.54], dtype=float),
        0.63,
    )


def sample_b() -> tuple[np.ndarray, np.ndarray, float]:
    return (
        np.array([1.20, 0.79, 0.93], dtype=float),
        np.array([0.52, 0.17, 0.54], dtype=float),
        0.63,
    )


def part1_seed_pair_plus_active_five_real_packet_reconstructs_the_current_exactly() -> None:
    print("\n" + "=" * 96)
    print("PART 1: SEED PAIR PLUS ACTIVE FIVE-REAL PACKET RECONSTRUCTS J_chi EXACTLY")
    print("=" * 96)

    x = np.array([0.24, 0.38, 1.07], dtype=float)
    y = np.array([0.09, 0.22, 0.61], dtype=float)
    delta = 1.10
    xbar, ybar, _xi, _eta, _d = decompose_seed_breaking(x, y, delta)
    packet = active_five_real_packet(x, y, delta)

    target = active_corner_transport(x, y, delta)
    rebuilt = rebuild_from_seed_and_packet(xbar, ybar, packet)
    j_target = nontrivial_character_current(target)
    j_rebuilt = nontrivial_character_current(rebuilt)

    check(
        "The active off-seed five-real packet has the expected five coordinates",
        len(packet) == 5,
        f"packet={np.round(np.array(packet), 6)}",
    )
    check(
        "Seed pair plus the active five-real packet reconstruct the active block exactly",
        np.linalg.norm(rebuilt - target) < 1e-12,
        f"err={np.linalg.norm(rebuilt - target):.2e}",
    )
    check(
        "The reconstructed active block carries the exact same native current J_chi",
        abs(j_rebuilt - j_target) < 1e-12,
        f"J_rebuilt={j_rebuilt:.6f}, J_target={j_target:.6f}",
    )
    check(
        "So nonzero J_chi is algorithmic once the seed pair and active five-real packet are supplied",
        abs(j_target) > 1e-6,
        f"J_target={j_target:.6f}",
    )


def part2_same_seed_facing_transport_data_still_allow_distinct_nonzero_currents() -> None:
    print("\n" + "=" * 96)
    print("PART 2: SAME SEED-FACING TRANSPORT DATA STILL ALLOW DISTINCT NONZERO J_chi")
    print("=" * 96)

    x_a, y_a, delta_a = sample_a()
    x_b, y_b, delta_b = sample_b()
    a = active_corner_transport(x_a, y_a, delta_a)
    b = active_corner_transport(x_b, y_b, delta_b)

    xbar_a, ybar_a, xi_a, eta_a, d_a = decompose_seed_breaking(x_a, y_a, delta_a)
    xbar_b, ybar_b, xi_b, eta_b, d_b = decompose_seed_breaking(x_b, y_b, delta_b)
    packet_a = np.array(active_five_real_packet(x_a, y_a, delta_a), dtype=float)
    packet_b = np.array(active_five_real_packet(x_b, y_b, delta_b), dtype=float)
    current_a = nontrivial_character_current(a)
    current_b = nontrivial_character_current(b)
    transfer_a = projected_transfer_kernel_from_active_block(a)
    transfer_b = projected_transfer_kernel_from_active_block(b)
    orbit_a = orbit_average_transport(a)
    orbit_b = orbit_average_transport(b)

    check(
        "The witness pair shares the same exact seed pair",
        abs(xbar_a - xbar_b) < 1e-12 and abs(ybar_a - ybar_b) < 1e-12,
        f"(xbar,ybar)=({xbar_a:.12f},{ybar_a:.12f})",
    )
    check(
        "The projected transfer kernel is identical on the witness pair",
        np.linalg.norm(transfer_a - transfer_b) < 1e-12,
        f"err={np.linalg.norm(transfer_a - transfer_b):.2e}",
    )
    check(
        "The orbit-averaged corner-transport moments are identical on the witness pair",
        all(abs(lhs - rhs) < 1e-12 for lhs, rhs in zip(orbit_a, orbit_b)),
        f"orbit_a={orbit_a}, orbit_b={orbit_b}",
    )
    check(
        "The active five-real packets are genuinely different",
        np.linalg.norm(packet_a - packet_b) > 1e-6
        and np.linalg.norm(transport_breaking_vector(xi_a, eta_a, d_a) - transport_breaking_vector(xi_b, eta_b, d_b)) > 1e-6,
        f"packet_a={np.round(packet_a, 6)}, packet_b={np.round(packet_b, 6)}",
    )
    check(
        "Those different packets already move the native current J_chi",
        abs(current_a - current_b) > 1e-6 and abs(current_a) > 1e-6 and abs(current_b) > 1e-6,
        f"J_a={current_a:.6f}, J_b={current_b:.6f}",
    )


def part3_existing_exact_notes_position_this_as_the_strong_production_target() -> None:
    print("\n" + "=" * 96)
    print("PART 3: EXISTING EXACT NOTES POSITION THIS AS THE STRONG PRODUCTION TARGET")
    print("=" * 96)

    production = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_NOTE_2026-04-17.md")
    transfer = read("docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md")
    corner = read("docs/PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md")
    current = read("docs/PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md")
    d_last = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md")

    check(
        "The fixed-slice production-boundary note already says the open PMNS object is production of nonzero J_chi",
        "nontrivial fixed-slice holonomy-pair" in production
        and "equivalently nonzero `chi = J_chi`" in production,
    )
    check(
        "The transfer-dominant-mode note already says the seed law stops before the off-seed five-real source",
        "does not determine the `5`-real off-seed" in transfer
        and "corner-breaking source" in transfer,
    )
    check(
        "The corner-transport note already says the same transport summaries are blind to the active five-real packet",
        "blind to the active 5-real" in corner or "blind to the five real corner-breaking coordinates" in corner,
    )
    check(
        "The native current boundary note already says the missing PMNS source object is nonzero J_chi",
        "derive a sole-axiom law producing nonzero `J_chi`" in current,
    )
    check(
        "The microscopic D last-mile note already says the remaining strong-route content is only the active off-seed five-real source",
        "remaining `D`-level object is only the active `5`-real breaking source" in d_last
        and "(xi_1, xi_2, eta_1, eta_2, delta)" in d_last,
    )


def part4_circularity_guard() -> None:
    print("\n" + "=" * 96)
    print("PART 4: CIRCULARITY GUARD")
    print("=" * 96)

    ok_current, bad_current = circularity_guard(nontrivial_character_current, {"u", "v", "w", "x", "y", "delta", "tau", "q"})
    ok_transfer, bad_transfer = circularity_guard(
        projected_transfer_kernel_from_active_block, {"u", "v", "w", "x", "y", "delta", "tau", "q"}
    )
    check("The native current functional takes no PMNS-side target values as inputs", ok_current, f"bad={bad_current}")
    check("The seed-facing transfer projection takes no PMNS-side target values as inputs", ok_transfer, f"bad={bad_transfer}")


def main() -> int:
    print("=" * 96)
    print("PMNS NONZERO CURRENT ACTIVE FIVE-REAL REDUCTION")
    print("=" * 96)
    print()
    print("Question:")
    print("  After fixed-slice readout closure, what is the strongest honest next")
    print("  PMNS-native microscopic target for producing nonzero J_chi?")

    part1_seed_pair_plus_active_five_real_packet_reconstructs_the_current_exactly()
    part2_same_seed_facing_transport_data_still_allow_distinct_nonzero_currents()
    part3_existing_exact_notes_position_this_as_the_strong_production_target()
    part4_circularity_guard()

    print("\n" + "=" * 96)
    print("RESULT")
    print("=" * 96)
    print("  Exact PMNS-native strong-route production reduction:")
    print("    - seed pair plus the active off-seed five-real packet reconstruct")
    print("      the active block and hence J_chi exactly")
    print("    - the current seed-facing transport laws already fix the seed data")
    print("      but leave that packet free")
    print("    - explicit same-seed witnesses then carry distinct nonzero J_chi")
    print()
    print("  So the strongest honest next theorem target on the PMNS-native strong")
    print("  production lane is exactly a sole-axiom law for the active off-seed")
    print("  five-real packet.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
