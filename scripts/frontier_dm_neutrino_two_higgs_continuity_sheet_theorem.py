#!/usr/bin/env python3
"""
DM-side continuity theorem fixing the residual two-Higgs sheet.

Question:
  Once the DM CP-supporting circulant right-Gram target lands on the canonical
  local two-Higgs lane, does the residual x <-> y sheet ambiguity remain
  physically open?

Answer:
  No, not on the DM lane.

  On the CP-admissible circulant subcone d >= 2 r, the canonical two-Higgs
  realization is forced onto the symmetric slice x_i = x and y_i = y. The
  remaining two solutions differ only by x <-> y. But:

      x_+^2 = (d + sqrt(d^2 - 4 r^2))/2
      y_+^2 = (d - sqrt(d^2 - 4 r^2))/2

  is the unique sheet that tends continuously to the retained universal bridge
  Y = sqrt(d) I as r -> 0, while the swapped sheet tends to a pure
  cycle-supported monomial class.

Boundary:
  This does not derive d, r, or delta from the bare axiom. It proves that on
  the DM circulant subcone the residual two-Higgs sheet is no longer an open
  datum once continuity to the retained universal Dirac bridge is imposed.
"""

from __future__ import annotations

import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

CYCLE = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
    ],
    dtype=complex,
)


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


def canonical_two_higgs_y(x: float, y: float, delta: float) -> np.ndarray:
    return np.diag([x, x, x]).astype(complex) + np.diag([y, y, y * np.exp(1j * delta)]).astype(complex) @ CYCLE


def right_gram(y: np.ndarray) -> np.ndarray:
    return y.conj().T @ y


def canonical_circulant_target(d: float, r: float, delta: float) -> np.ndarray:
    return np.array(
        [
            [d, r, r * np.exp(-1j * delta)],
            [r, d, r],
            [r * np.exp(1j * delta), r, d],
        ],
        dtype=complex,
    )


def sheet_roots(d: float, r: float) -> tuple[tuple[float, float], tuple[float, float]]:
    disc = max(d * d - 4.0 * r * r, 0.0)
    root = math.sqrt(disc)
    xp2 = 0.5 * (d + root)
    yp2 = 0.5 * (d - root)
    x_plus = math.sqrt(max(xp2, 0.0))
    y_plus = math.sqrt(max(yp2, 0.0))
    return (x_plus, y_plus), (y_plus, x_plus)


def support_profile(y: np.ndarray) -> tuple[float, float]:
    identity_weight = float(np.linalg.norm(np.diag(np.diag(y))))
    cycle_weight = float(np.linalg.norm(y - np.diag(np.diag(y))))
    return identity_weight, cycle_weight


def part1_the_cp_admissible_circulant_subcone_has_exactly_two_sheets() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE DM CIRCULANT SUBCONE HAS EXACTLY TWO SYMMETRIC SHEETS")
    print("=" * 88)

    d = 1.20
    r = 0.35
    delta = 0.80
    (x_plus, y_plus), (x_minus, y_minus) = sheet_roots(d, r)
    k_target = canonical_circulant_target(d, r, delta)
    k_plus = right_gram(canonical_two_higgs_y(x_plus, y_plus, delta))
    k_minus = right_gram(canonical_two_higgs_y(x_minus, y_minus, delta))

    check(
        "Both quadratic sheets solve the same circulant right-Gram target",
        np.linalg.norm(k_target - k_plus) < 1e-12 and np.linalg.norm(k_target - k_minus) < 1e-12,
        f"errors=({np.linalg.norm(k_target-k_plus):.2e}, {np.linalg.norm(k_target-k_minus):.2e})",
    )
    check(
        "The two sheets differ only by x <-> y",
        abs(x_plus - y_minus) < 1e-12 and abs(y_plus - x_minus) < 1e-12,
        f"plus=({x_plus:.6f},{y_plus:.6f}), minus=({x_minus:.6f},{y_minus:.6f})",
    )

    print()
    print("  So on the DM circulant subcone the residual ambiguity is no longer a")
    print("  generic seven-quantity mess. It is exactly one swap x <-> y.")


def part2_continuity_to_the_retained_universal_bridge_picks_the_plus_sheet() -> None:
    print("\n" + "=" * 88)
    print("PART 2: CONTINUITY TO THE RETAINED UNIVERSAL BRIDGE PICKS THE PHYSICAL SHEET")
    print("=" * 88)

    d = 1.0
    delta = 0.70
    small_rs = [1e-1, 1e-2, 1e-4]
    plus_identity_dominant = True
    minus_cycle_dominant = True
    details = []

    for r in small_rs:
        (x_plus, y_plus), (x_minus, y_minus) = sheet_roots(d, r)
        y_plus_mat = canonical_two_higgs_y(x_plus, y_plus, delta)
        y_minus_mat = canonical_two_higgs_y(x_minus, y_minus, delta)
        id_plus, cyc_plus = support_profile(y_plus_mat)
        id_minus, cyc_minus = support_profile(y_minus_mat)
        plus_identity_dominant &= id_plus > cyc_plus
        minus_cycle_dominant &= cyc_minus > id_minus
        details.append(
            f"r={r:.0e}: plus(id={id_plus:.4f},cyc={cyc_plus:.4f}) minus(id={id_minus:.4f},cyc={cyc_minus:.4f})"
        )

    check(
        "The plus sheet tends to the retained universal bridge Y = sqrt(d) I",
        plus_identity_dominant and abs(sheet_roots(d, small_rs[-1])[0][0] - math.sqrt(d)) < 1e-6,
        "; ".join(details),
    )
    check(
        "The swapped sheet tends instead to a pure cycle-supported monomial class",
        minus_cycle_dominant and abs(sheet_roots(d, small_rs[-1])[1][1] - math.sqrt(d)) < 1e-6,
        "; ".join(details),
    )

    print()
    print("  So the retained universal bridge is not just a background limit.")
    print("  It anchors the physical two-Higgs sheet on the DM lane.")


def part3_the_selected_sheet_is_explicit_and_merges_only_on_the_boundary() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE SELECTED DM SHEET IS EXPLICIT AND MERGES ONLY AT d = 2 r")
    print("=" * 88)

    d_bulk = 1.10
    r_bulk = 0.30
    (x_plus, y_plus), (x_minus, y_minus) = sheet_roots(d_bulk, r_bulk)

    d_edge = 1.00
    r_edge = 0.50
    (x_edge_plus, y_edge_plus), (x_edge_minus, y_edge_minus) = sheet_roots(d_edge, r_edge)

    check(
        "On the physical DM sheet, x >= y with explicit closed form roots",
        x_plus > y_plus > 0.0 and x_minus < y_minus,
        f"plus=({x_plus:.6f},{y_plus:.6f}) minus=({x_minus:.6f},{y_minus:.6f})",
    )
    check(
        "The two sheets merge only on the exact boundary d = 2 r",
        abs(x_edge_plus - y_edge_plus) < 1e-12 and abs(x_edge_minus - y_edge_minus) < 1e-12,
        f"edge=({x_edge_plus:.6f},{y_edge_plus:.6f})",
    )

    print()
    print("  The physical sheet is therefore explicit:")
    print("      x^2 = (d + sqrt(d^2 - 4 r^2))/2")
    print("      y^2 = (d - sqrt(d^2 - 4 r^2))/2")
    print("  with the swap discarded by continuity to the universal bridge.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO TWO-HIGGS CONTINUITY SHEET THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - DM neutrino two-Higgs right-Gram bridge")
    print("  - DM leptogenesis universal-Yukawa no-go")
    print("  - retained universal Dirac bridge Y = y_0 I")
    print()
    print("Question:")
    print("  Once the DM circulant target lands on the canonical two-Higgs lane,")
    print("  does the residual x <-> y sheet remain physically open?")

    part1_the_cp_admissible_circulant_subcone_has_exactly_two_sheets()
    part2_continuity_to_the_retained_universal_bridge_picks_the_plus_sheet()
    part3_the_selected_sheet_is_explicit_and_merges_only_on_the_boundary()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact DM-side sheet answer:")
    print("    - the residual ambiguity on the circulant subcone is only x <-> y")
    print("    - continuity to the retained universal bridge picks the x >= y sheet")
    print("    - the physical sheet is explicit in closed form")
    print()
    print("  So the DM branch no longer needs an extra admitted right-sensitive")
    print("  scalar just to fix the two-Higgs sheet on this circulant lane.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())

