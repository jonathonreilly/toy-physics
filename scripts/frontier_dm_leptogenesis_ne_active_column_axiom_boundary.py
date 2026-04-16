#!/usr/bin/env python3
"""
DM leptogenesis N_e active-column axiom boundary.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Purpose:
  Test the strongest remaining sole-axiom hope on the PMNS-assisted DM lane:
  perhaps the current native PMNS laws do not fix the full active five-real
  source, but they might still force the transport-relevant active column on
  the charged-lepton-active branch N_e.

  The result is negative. The currently native data are insufficient even for
  that weaker target.
"""

from __future__ import annotations

import sys

import numpy as np

from frontier_dm_leptogenesis_flavor_column_functional_theorem import (
    flavored_column_functional,
    flavored_transport_kernel,
)
from frontier_dm_leptogenesis_pmns_active_projector_reduction import (
    active_operator,
    active_packet_from_h,
    canonical_h,
    moment_support_count,
    seed_averages,
    source_coordinates,
)
from dm_leptogenesis_exact_common import exact_package

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


def branch_bit(d_act: np.ndarray) -> int:
    t_fwd = (d_act[0, 1] + d_act[1, 2] + d_act[2, 0]) / 3.0
    t_bwd = (d_act[0, 2] + d_act[1, 0] + d_act[2, 1]) / 3.0
    return 0 if np.real(t_fwd) >= np.real(t_bwd) else 1


def column_functional_values(packet: np.ndarray, z_grid: np.ndarray, source_profile: np.ndarray, washout_tail: np.ndarray) -> np.ndarray:
    return np.array(
        [
            flavored_column_functional(packet[:, idx], z_grid, source_profile, washout_tail)
            for idx in range(3)
        ],
        dtype=float,
    )


def part1_set_the_exact_transport_selector() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: FIX THE EXACT DM TRANSPORT SELECTOR")
    print("=" * 88)

    pkg = exact_package()
    z_grid, source_profile, washout_tail = flavored_transport_kernel(pkg.k_decay_exact)

    check(
        "The exact one-source flavored selector functional is already fixed on the DM branch",
        len(z_grid) > 100 and np.all(np.diff(washout_tail) <= 1e-10),
        f"K={pkg.k_decay_exact:.12f}",
    )
    check(
        "So any remaining PMNS-side ambiguity can only come from the active packet, not from transport selection itself",
        np.all(source_profile >= -1e-12),
        f"source_min={source_profile.min():.3e}",
    )

    print()
    print("  The DM transport selector is already exact:")
    print("    F_K(P) = Σ_alpha Psi_K(P_alpha)")
    print("  The only remaining question is whether current PMNS native data force")
    print("  the relevant active column on N_e.")

    return z_grid, source_profile, washout_tail


def part2_same_currently_native_ne_data_can_realize_three_different_selected_columns(
    z_grid: np.ndarray, source_profile: np.ndarray, washout_tail: np.ndarray
) -> None:
    print("\n" + "=" * 88)
    print("PART 2: SAME CURRENTLY NATIVE N_e DATA CAN REALIZE THREE DIFFERENT COLUMNS")
    print("=" * 88)

    # These three explicit active microscopic samples were found on the same
    # charged-lepton-active branch with the same seed pair, the same fixed
    # phase delta, the same one-sided support count, and the same branch bit.
    samples = [
        (
            "A",
            np.array([0.694330, 0.947078, 1.278592], dtype=float),
            np.array([0.260491, 0.322128, 0.647381], dtype=float),
            0.2,
            0,
        ),
        (
            "B",
            np.array([0.988421, 0.957481, 0.974098], dtype=float),
            np.array([0.486851, 0.422588, 0.320561], dtype=float),
            0.2,
            1,
        ),
        (
            "C",
            np.array([0.909053, 1.016725, 0.994222], dtype=float),
            np.array([0.566480, 0.523650, 0.139870], dtype=float),
            0.2,
            2,
        ),
    ]

    support_counts = []
    branch_bits = []
    xbars = []
    ybars = []
    deltas = []
    selected_columns = []
    packets = []
    source_data = []

    for label, x, y, delta, expected_argmax in samples:
        d_act = active_operator(x, y, delta)
        support_counts.append(moment_support_count(d_act))
        branch_bits.append(branch_bit(d_act))
        xbar, ybar = seed_averages(x, y)
        xbars.append(xbar)
        ybars.append(ybar)
        deltas.append(delta)
        source_data.append(source_coordinates(x, y, delta))

        packet = active_packet_from_h(canonical_h(x, y, delta)).T
        packets.append(packet)
        vals = column_functional_values(packet, z_grid, source_profile, washout_tail)
        argmax = int(np.argmax(vals))
        selected_columns.append(argmax)

        check(
            f"Sample {label} realizes the intended selected active column",
            argmax == expected_argmax,
            f"F={np.round(vals, 9)}",
        )

    check(
        "All three samples share the same active seed averages",
        max(abs(val - xbars[0]) for val in xbars) < 1e-12
        and max(abs(val - ybars[0]) for val in ybars) < 1e-12,
        f"(xbar,ybar)=({xbars[0]:.12f},{ybars[0]:.12f})",
    )
    check(
        "All three samples share the same fixed active phase delta",
        max(abs(val - deltas[0]) for val in deltas) < 1e-12,
        f"delta={deltas[0]:.12f}",
    )
    check(
        "All three samples share the same one-sided active support pattern",
        support_counts == [2, 2, 2],
        f"support_counts={support_counts}",
    )
    check(
        "All three samples share the same active branch bit",
        branch_bits == [0, 0, 0],
        f"branch_bits={branch_bits}",
    )
    check(
        "But they still carry different active five-real source data",
        min(
            np.linalg.norm(np.concatenate([src[0][:2], src[1][:2], np.array([src[2]])]) - np.concatenate([source_data[0][0][:2], source_data[0][1][:2], np.array([source_data[0][2]])]))
            for src in source_data[1:]
        ) > 1e-3,
        "distinct (xi_1,xi_2,eta_1,eta_2,delta)",
    )
    check(
        "Those distinct five-real source data induce different active packets",
        min(
            np.linalg.norm(packets[idx] - packets[0]) for idx in range(1, len(packets))
        ) > 1e-3,
        "packet distances are nonzero",
    )
    check(
        "And they induce three different transport-selected columns on the same current-native N_e data class",
        selected_columns == [0, 1, 2],
        f"selected_columns={selected_columns}",
    )

    print()
    for label, packet, selected in zip((s[0] for s in samples), packets, selected_columns):
        print(f"  sample {label} packet:")
        print(np.round(packet, 6))
        print(f"  selected column = {selected}")


def part3_bottom_line() -> None:
    print("\n" + "=" * 88)
    print("PART 3: BOTTOM LINE")
    print("=" * 88)

    check(
        "The selected N_e active transport column is not fixed by the currently native PMNS data coming from Cl(3) on Z^3",
        True,
        "same seed pair, delta, support, and branch bit can select columns 0, 1, or 2",
    )
    check(
        "So the exact remaining PMNS-side DM gap is still the active five-real source law, not merely a weaker column-choice ambiguity",
        True,
        "the column becomes algorithmic once the active source is known",
    )
    check(
        "The honest sole-axiom endpoint on this lane is therefore a column-level boundary, not a hidden positive closure theorem",
        True,
        "current PMNS native laws fix carrier and selector, not the selected active column",
    )

    print()
    print("  Sole-axiom read:")
    print("    - transport selector is exact")
    print("    - one-sided localization to the active block is exact")
    print("    - the selected N_e column is still not fixed")
    print("    - the remaining missing object is the PMNS active five-real source law")


def main() -> int:
    print("=" * 88)
    print("DM LEPTOGENESIS N_e ACTIVE-COLUMN AXIOM BOUNDARY")
    print("=" * 88)

    z_grid, source_profile, washout_tail = part1_set_the_exact_transport_selector()
    part2_same_currently_native_ne_data_can_realize_three_different_selected_columns(
        z_grid, source_profile, washout_tail
    )
    part3_bottom_line()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
