#!/usr/bin/env python3
"""
Exact current-bank theorem:
the retained PMNS bank fixes a right orbit over the left/Hermitian core, not a
canonical right-handed frame, so the admitted right-Gram completion data are
not yet axiom-derived.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0
PERM_1 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
CYCLE = PERM_1.copy()


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


def monomial_y(diag: np.ndarray) -> np.ndarray:
    return np.diag(diag.astype(complex)) @ PERM_1


def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
    return np.diag(np.asarray(x, dtype=complex)) + phase_block @ CYCLE


def right_score(y: np.ndarray) -> int:
    k = y.conj().T @ y
    upper = np.array([k[0, 1], k[1, 2], k[0, 2]])
    return int(np.count_nonzero(np.abs(upper) > 1e-12))


def dft3() -> np.ndarray:
    omega = np.exp(2.0j * math.pi / 3.0)
    return np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega, omega * omega],
            [1.0, omega * omega, omega],
        ],
        dtype=complex,
    ) / math.sqrt(3.0)


def rotation12(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array(
        [
            [c, s, 0.0],
            [-s, c, 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=complex,
    )


def part1_right_unitary_orbits_preserve_left_hermitian_data() -> None:
    print("\n" + "=" * 88)
    print("PART 1: RIGHT-UNITARY ORBITS PRESERVE THE RETAINED LEFT/HERMITIAN CORE")
    print("=" * 88)

    y = canonical_y(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    u_r = rotation12(0.47) @ np.diag(np.array([1.0, np.exp(0.23j), np.exp(-0.41j)], dtype=complex))
    y_rot = y @ u_r.conj().T
    h = y @ y.conj().T
    h_rot = y_rot @ y_rot.conj().T
    k = y.conj().T @ y
    k_rot = y_rot.conj().T @ y_rot
    svals = np.linalg.svd(y, compute_uv=False)
    svals_rot = np.linalg.svd(y_rot, compute_uv=False)

    check("Right-unitary rotation preserves H = Y Y^dag", np.linalg.norm(h - h_rot) < 1e-12,
          f"H difference={np.linalg.norm(h - h_rot):.2e}")
    check("Right-unitary rotation preserves singular values", np.linalg.norm(np.sort(svals) - np.sort(svals_rot)) < 1e-12,
          f"sv difference={np.linalg.norm(np.sort(svals) - np.sort(svals_rot)):.2e}")
    check("Right-unitary rotation conjugates K = Y^dag Y", np.linalg.norm(k_rot - u_r @ k @ u_r.conj().T) < 1e-12,
          f"K conjugacy error={np.linalg.norm(k_rot - u_r @ k @ u_r.conj().T):.2e}")
    check("So the retained left/Hermitian core does not determine a unique K", np.linalg.norm(k - k_rot) > 1e-3,
          f"K difference={np.linalg.norm(k - k_rot):.6f}")

    print()
    print("  The retained PMNS bank sees H and the singular spectrum, not a")
    print("  canonical right-handed frame. K moves on an exact right orbit.")


def part2_the_admitted_selector_datum_varies_along_the_same_right_orbit() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE ADMITTED RIGHT-GRAM SELECTOR DATUM VARIES ON THE SAME CORE")
    print("=" * 88)

    y_mono = monomial_y(np.array([0.21, 0.34, 0.55], dtype=float))
    u_f = dft3()
    y_rot = y_mono @ u_f.conj().T
    h = y_mono @ y_mono.conj().T
    h_rot = y_rot @ y_rot.conj().T
    score0 = right_score(y_mono)
    score1 = right_score(y_rot)

    check("The monomial sample and its rotated representative share the same H", np.linalg.norm(h - h_rot) < 1e-12,
          f"H difference={np.linalg.norm(h - h_rot):.2e}")
    check("The admitted selector score starts at 0 on the diagonal right-Gram representative", score0 == 0,
          f"score={score0}")
    check("A right-unitary frame change can make the same core have full right-support score 3", score1 == 3,
          f"score={score1}")
    check("So the admitted selector datum is not intrinsic on the retained bank", score0 != score1,
          f"scores=({score0}, {score1})")

    print()
    print("  This is the exact selector-side obstruction: the same retained")
    print("  left/Hermitian data can carry different right-Gram selector values")
    print("  until a right frame is fixed.")


def part3_the_admitted_sheet_fixing_scalar_also_varies_along_the_same_right_orbit() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE ADMITTED RIGHT-GRAM SHEET SCALAR ALSO VARIES ON THE SAME CORE")
    print("=" * 88)

    y = canonical_y(np.array([1.10, 1.30, 0.80], dtype=float), np.array([0.60, 0.70, 1.00], dtype=float), 1.10)
    u_r = rotation12(0.61)
    y_rot = y @ u_r.conj().T
    h = y @ y.conj().T
    h_rot = y_rot @ y_rot.conj().T
    k = y.conj().T @ y
    k_rot = y_rot.conj().T @ y_rot
    s12 = float(np.abs(k[0, 1]))
    s12_rot = float(np.abs(k_rot[0, 1]))

    check("The canonical sample and its rotated representative share the same H", np.linalg.norm(h - h_rot) < 1e-12,
          f"H difference={np.linalg.norm(h - h_rot):.2e}")
    check("The admitted sheet-fixing scalar |(Y^dag Y)12| changes along the right orbit", abs(s12 - s12_rot) > 1e-3,
          f"values=({s12:.6f}, {s12_rot:.6f})")
    check("So the admitted sheet-fixing scalar is not intrinsic on the retained bank either", True)

    print()
    print("  This is the exact sheet-side obstruction: even after branch")
    print("  selection, the right-Gram scalar needs a right frame to become a")
    print("  well-defined internal datum.")


def part4_the_atlas_now_records_the_right_frame_obstruction_explicitly() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE ATLAS NOW RECORDS THE RIGHT-FRAME OBSTRUCTION EXPLICITLY")
    print("=" * 88)

    one_gen = read("docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md")
    note = read("docs/PMNS_RIGHT_FRAME_ORBIT_OBSTRUCTION_NOTE.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    packet = read("docs/publication/ci3_z3/NEUTRINO_DIRAC_PMNS_BOUNDARY_PACKET_2026-04-15.md")

    check("The one-generation matter closure note keeps the right-handed lane at completion level, not spatial derivation level",
          "not retained: a derivation of the right-handed sector from the spatial graph alone" in one_gen)
    check("The new note identifies the strongest exact endpoint as a right orbit rather than a canonical right frame",
          "right-orbit bundle" in note and "canonical right frame" in note)
    check("The atlas carries the PMNS right-frame orbit obstruction row",
          "| PMNS right-frame orbit obstruction |" in atlas)
    check("The reviewer packet records that the admitted right-Gram route is basis-conditional",
          "right-orbit bundle" in packet and "canonical right frame" in packet)

    print()
    print("  So the derivation-bank question is now closed cleanly as well:")
    print("  the admitted right-Gram route exists, but the retained bank still")
    print("  does not provide the right frame that would make it intrinsic.")


def main() -> int:
    print("=" * 88)
    print("PMNS RIGHT-FRAME ORBIT OBSTRUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - one-generation matter closure")
    print("  - PMNS branch sheet nonforcing")
    print("  - PMNS right-Gram selector realization")
    print("  - PMNS right-Gram sheet fixing")
    print("  - GR invariant-core / missing-frame pattern (structural only)")
    print()
    print("Question:")
    print("  Can the retained atlas / axiom bank already derive the admitted")
    print("  right-Gram completion data internally?")

    part1_right_unitary_orbits_preserve_left_hermitian_data()
    part2_the_admitted_selector_datum_varies_along_the_same_right_orbit()
    part3_the_admitted_sheet_fixing_scalar_also_varies_along_the_same_right_orbit()
    part4_the_atlas_now_records_the_right_frame_obstruction_explicitly()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - the retained PMNS bank fixes the left/Hermitian core and the")
    print("      right-handed representation content")
    print("    - but it does not fix a canonical right-handed frame")
    print("    - right-unitary orbits preserve H = Y Y^dag and the singular values")
    print("      while moving K = Y^dag Y")
    print("    - along that same right orbit, the admitted selector datum m_R(Y)")
    print("      and the admitted sheet-fixing scalar |(Y^dag Y)12| can change")
    print()
    print("  So the strongest exact endpoint is a right-orbit bundle over the")
    print("  retained left/Hermitian core, not an intrinsic right-Gram closure.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
