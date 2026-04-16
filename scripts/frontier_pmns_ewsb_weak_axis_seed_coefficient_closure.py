#!/usr/bin/env python3
"""
Exact coefficient-closure theorem on the compatible weak-axis seed patch:
the canonical active coefficients are explicit up to one exchange sheet,
and even right-Gram data do not distinguish the two sheets.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0

CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
FZ3 = (1.0 / math.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, np.exp(2j * math.pi / 3.0), np.exp(4j * math.pi / 3.0)],
        [1.0, np.exp(4j * math.pi / 3.0), np.exp(2j * math.pi / 3.0)],
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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def compact(text: str) -> str:
    return text.replace(" ", "").replace("\n", "").replace("`", "")


def weak_axis_seed_h(a: float, b: float) -> np.ndarray:
    return FZ3.conj().T @ np.diag([a, b, b]) @ FZ3


def mu_nu_delta(a: float, b: float) -> tuple[float, float, float]:
    mu = (a + 2.0 * b) / 3.0
    nu = (a - b) / 3.0
    delta = mu * mu - 4.0 * nu * nu
    return mu, nu, delta


def seed_sheet_coefficients(a: float, b: float) -> tuple[float, float]:
    mu, _nu, delta = mu_nu_delta(a, b)
    x2 = (mu + math.sqrt(delta)) / 2.0
    y2 = (mu - math.sqrt(delta)) / 2.0
    return math.sqrt(x2), math.sqrt(y2)


def seed_y(x: float, y: float) -> np.ndarray:
    return x * np.eye(3, dtype=complex) + y * CYCLE


def part1_the_seed_patch_has_exact_closed_form_coefficients() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ON THE COMPATIBLE SEED PATCH THE COEFFICIENTS ARE EXACTLY CLOSED")
    print("=" * 88)

    a, b = 2.0, 1.0
    mu, nu, delta = mu_nu_delta(a, b)
    x, y = seed_sheet_coefficients(a, b)
    y_plus = seed_y(x, y)
    h_seed = weak_axis_seed_h(a, b)

    check("The compatible patch has Delta >= 0", delta >= -1e-12, f"Delta={delta:.6f}")
    check("The closed-form coefficients satisfy x^2+y^2=mu", abs((x * x + y * y) - mu) < 1e-12,
          f"x^2+y^2={x*x+y*y:.6f}, mu={mu:.6f}")
    check("The closed-form coefficients satisfy xy=nu", abs((x * y) - nu) < 1e-12,
          f"xy={x*y:.6f}, nu={nu:.6f}")
    check("The closed-form seed sheet reproduces H_seed exactly",
          np.linalg.norm(y_plus @ y_plus.conj().T - h_seed) < 1e-12,
          f"kernel err={np.linalg.norm(y_plus @ y_plus.conj().T - h_seed):.2e}")


def part2_the_residual_sheet_is_exactly_x_exchange_y() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE RESIDUAL COEFFICIENT SHEET IS EXACTLY THE EXCHANGE x<->y")
    print("=" * 88)

    a, b = 2.0, 1.0
    x, y = seed_sheet_coefficients(a, b)
    y_plus = seed_y(x, y)
    y_minus = seed_y(y, x)
    h_seed = weak_axis_seed_h(a, b)

    check("On the generic compatible patch B<A<4B, x>y>0", x > y > 0.0,
          f"x={x:.6f}, y={y:.6f}")
    check("The two seed sheets are distinct canonical Yukawa data", np.linalg.norm(y_plus - y_minus) > 1e-6,
          f"sheet distance={np.linalg.norm(y_plus - y_minus):.6f}")
    check("The exchanged sheet gives the same Hermitian seed",
          np.linalg.norm(y_minus @ y_minus.conj().T - h_seed) < 1e-12,
          f"kernel err={np.linalg.norm(y_minus @ y_minus.conj().T - h_seed):.2e}")


def part3_even_right_gram_data_collapse_on_the_seed_patch() -> None:
    print("\n" + "=" * 88)
    print("PART 3: EVEN RIGHT-GRAM DATA CANNOT DISTINGUISH THE TWO SEED SHEETS")
    print("=" * 88)

    a, b = 2.0, 1.0
    x, y = seed_sheet_coefficients(a, b)
    y_plus = seed_y(x, y)
    y_minus = seed_y(y, x)
    h_seed = weak_axis_seed_h(a, b)
    k_plus = y_plus.conj().T @ y_plus
    k_minus = y_minus.conj().T @ y_minus

    check("The seed sheet is normal, so Y Y^dag = Y^dag Y", np.linalg.norm(y_plus @ y_plus.conj().T - k_plus) < 1e-12,
          f"normal err={np.linalg.norm(y_plus @ y_plus.conj().T - k_plus):.2e}")
    check("The two seed sheets have the same right Gram matrix", np.linalg.norm(k_plus - k_minus) < 1e-12,
          f"K diff={np.linalg.norm(k_plus - k_minus):.2e}")
    check("That common right Gram matrix is exactly H_seed", np.linalg.norm(k_plus - h_seed) < 1e-12,
          f"K-H diff={np.linalg.norm(k_plus - h_seed):.2e}")


def part4_boundary_edges_are_exact_and_explicit() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE COMPATIBLE-PATCH EDGES ARE EXACT AND EXPLICIT")
    print("=" * 88)

    a0, b0 = 1.0, 1.0
    x0, y0 = seed_sheet_coefficients(a0, b0)
    y0_plus = seed_y(x0, y0)
    y0_minus = seed_y(y0, x0)

    a1, b1 = 4.0, 1.0
    x1, y1 = seed_sheet_coefficients(a1, b1)

    check("At A=B, one sheet is the diagonal monomial edge", np.linalg.norm(y0_plus - np.eye(3, dtype=complex)) < 1e-12,
          f"edge err={np.linalg.norm(y0_plus - np.eye(3, dtype=complex)):.2e}")
    check("At A=B, the exchanged sheet is the cyclic monomial edge", np.linalg.norm(y0_minus - CYCLE) < 1e-12,
          f"edge err={np.linalg.norm(y0_minus - CYCLE):.2e}")
    check("At A=4B the two seed sheets merge", abs(x1 - y1) < 1e-12,
          f"x-y={x1-y1:.2e}")


def part5_note_and_atlas_record_the_new_coefficient_closure() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NOTE AND ATLAS RECORD THE SEED-PATCH COEFFICIENT CLOSURE")
    print("=" * 88)

    note = read("docs/PMNS_EWSB_WEAK_AXIS_SEED_COEFFICIENT_CLOSURE_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    cnote = compact(note)

    check("The note records the exact two-sheet formulas Y_+ and Y_-",
          "Y_+=x_+I+y_+C" in cnote and "Y_-=y_+I+x_+C" in cnote)
    check("The note records that even right-Gram data collapse on the seed patch",
          "Y_+^dagY_+=Y_-^dagY_-=H_seed" in cnote)
    check("The atlas carries the PMNS EWSB weak-axis seed coefficient closure row",
          "| PMNS EWSB weak-axis seed coefficient closure |" in atlas)


def main() -> int:
    print("=" * 88)
    print("PMNS EWSB WEAK-AXIS SEED COEFFICIENT CLOSURE")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS EWSB weak-axis Z3 seed")
    print("  - PMNS branch-conditioned quadratic-sheet closure")
    print("  - PMNS branch sheet nonforcing")
    print("  - PMNS right-Gram sheet fixing")
    print()
    print("Question:")
    print("  On the compatible weak-axis seed patch, do we already get full")
    print("  coefficient closure, or is there still a generic post-Hermitian")
    print("  reconstruction problem?")

    part1_the_seed_patch_has_exact_closed_form_coefficients()
    part2_the_residual_sheet_is_exactly_x_exchange_y()
    part3_even_right_gram_data_collapse_on_the_seed_patch()
    part4_boundary_edges_are_exact_and_explicit()
    part5_note_and_atlas_record_the_new_coefficient_closure()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer on the compatible weak-axis seed patch:")
    print("    - the canonical active coefficients are explicit in closed form")
    print("    - the residual ambiguity is exactly the exchange sheet x<->y")
    print("    - and even right-Gram data collapse there, because both sheets")
    print("      have the same K = Y^dag Y = H_seed")
    print()
    print("  So on this patch the remaining full-closure object is no longer")
    print("  a generic coefficient fit and no longer a right-Gram datum.")
    print("  It is one genuinely Y-level sheet-selection law.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
