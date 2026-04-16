#!/usr/bin/env python3
"""
DM neutrino post-canonical positive polar section.

Question:
  After the exact post-canonical extension/support-class reduction and the
  raw right-frame orbit obstruction, does the generic full-rank DM right orbit
  still admit a canonical intrinsic representative that makes the remaining
  slot-supported bridge readable from H = Y Y^dag alone?

Answer:
  Yes.

  On the generic full-rank patch, the exact right orbit admits the unique
  positive polar representative

      Y_+(H) = H^(1/2).

  For that representative,

      K_+(H) = Y_+(H)^dag Y_+(H) = H,

  so the remaining post-canonical singlet-doublet slot carrier is read
  directly from the Hermitian data through

      K_Z3(H) = U_Z3^dag H U_Z3
      a(H) = (K_Z3(H))_01
      b(H) = (K_Z3(H))_02.

  The physical heavy-neutrino-basis CP tensor is then

      Im[(K_mass)01^2] = Im[((a-b)^2)/2]
      Im[(K_mass)02^2] = Im[((a+b)^2)/2].

  So the old raw right-frame blocker is not the final endpoint. The generic
  full-rank right orbit already carries a canonical intrinsic bridge from H.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

PI = np.pi
OMEGA = np.exp(2j * PI / 3.0)
CYCLE = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]], dtype=complex)
UZ3 = (1.0 / np.sqrt(3.0)) * np.array(
    [
        [1.0, 1.0, 1.0],
        [1.0, OMEGA, OMEGA * OMEGA],
        [1.0, OMEGA * OMEGA, OMEGA],
    ],
    dtype=complex,
)
R = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
        [0.0, -1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0)],
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


def canonical_y(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    phase_block = np.diag(np.array([y[0], y[1], y[2] * np.exp(1j * delta)], dtype=complex))
    return np.diag(np.asarray(x, dtype=complex)) + phase_block @ CYCLE


def sqrt_psd(h: np.ndarray) -> np.ndarray:
    evals, vecs = np.linalg.eigh(h)
    evals = np.clip(evals, 0.0, None)
    return vecs @ np.diag(np.sqrt(evals)) @ vecs.conj().T


def right_rotation(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, c, -s],
            [0.0, s, c],
        ],
        dtype=complex,
    )


def z3_kernel_from_h(h: np.ndarray) -> np.ndarray:
    return UZ3.conj().T @ h @ UZ3


def z3_kernel_from_y(y: np.ndarray) -> np.ndarray:
    return z3_kernel_from_h(y @ y.conj().T)


def slot_pair_from_h(h: np.ndarray) -> tuple[complex, complex]:
    kz = z3_kernel_from_h(h)
    return kz[0, 1], kz[0, 2]


def mass_basis_kernel_from_h(h: np.ndarray) -> np.ndarray:
    return R.T @ z3_kernel_from_h(h) @ R


def cp_pair_from_h(h: np.ndarray) -> tuple[float, float]:
    km = mass_basis_kernel_from_h(h)
    return float(np.imag(km[0, 1] ** 2)), float(np.imag(km[0, 2] ** 2))


def part1_generic_right_orbit_has_unique_positive_representative() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE GENERIC DM RIGHT ORBIT HAS A UNIQUE POSITIVE REPRESENTATIVE")
    print("=" * 88)

    y = canonical_y(
        np.array([1.10, 0.80, 1.30], dtype=float),
        np.array([0.45, 0.62, 0.57], dtype=float),
        2.0 * PI / 3.0,
    )
    u_r = right_rotation(0.41) @ np.diag(np.array([1.0, np.exp(0.23j), np.exp(-0.31j)], dtype=complex))
    y_rot = y @ u_r.conj().T
    h = y @ y.conj().T
    h_rot = y_rot @ y_rot.conj().T
    p = sqrt_psd(h)
    p_rot = sqrt_psd(h_rot)

    check(
        "The exact right orbit preserves H = Y Y^dag",
        np.linalg.norm(h - h_rot) < 1e-12,
        f"H difference = {np.linalg.norm(h - h_rot):.2e}",
    )
    check(
        "The polar representative is positive Hermitian",
        np.linalg.norm(p - p.conj().T) < 1e-12 and np.min(np.linalg.eigvalsh(p)) >= -1e-12,
        f"Hermitian error = {np.linalg.norm(p - p.conj().T):.2e}",
    )
    check(
        "The polar representative squares exactly to H",
        np.linalg.norm(p @ p - h) < 1e-10,
        f"P^2 - H error = {np.linalg.norm(p @ p - h):.2e}",
    )
    check(
        "The same right orbit yields the same unique positive representative",
        np.linalg.norm(p - p_rot) < 1e-10,
        f"polar difference = {np.linalg.norm(p - p_rot):.2e}",
    )

    print()
    print("  So the raw right-frame obstruction is not a total no-section theorem.")
    print("  The generic full-rank DM right orbit already has Y_+(H) = H^(1/2).")
    return h


def part2_the_postcanonical_bridge_is_read_directly_from_h(h: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE POST-CANONICAL SLOT BRIDGE IS INTRINSIC ON THE POSITIVE SECTION")
    print("=" * 88)

    p = sqrt_psd(h)
    kz_h = z3_kernel_from_h(h)
    kz_p = z3_kernel_from_y(p)
    a_h, b_h = slot_pair_from_h(h)
    a_p, b_p = slot_pair_from_h(p @ p.conj().T)
    km = mass_basis_kernel_from_h(h)

    check(
        "On the positive section the right kernel is exactly K_+(H) = H",
        np.linalg.norm(p.conj().T @ p - h) < 1e-10,
        f"K_+ - H error = {np.linalg.norm(p.conj().T @ p - h):.2e}",
    )
    check(
        "The Z_3-basis kernel is therefore read directly from H",
        np.linalg.norm(kz_h - kz_p) < 1e-10,
        f"K_Z3 difference = {np.linalg.norm(kz_h - kz_p):.2e}",
    )
    check(
        "The intrinsic singlet-doublet slot pair is exactly a(H), b(H)",
        abs(a_h - a_p) < 1e-10 and abs(b_h - b_p) < 1e-10,
        f"a(H)={a_h:.6f}, b(H)={b_h:.6f}",
    )
    check(
        "The mass-basis singlet-doublet entries are the exact linear slot combinations",
        abs(km[0, 1] - (a_h - b_h) / np.sqrt(2.0)) < 1e-10
        and abs(km[0, 2] - (a_h + b_h) / np.sqrt(2.0)) < 1e-10,
        f"K01={km[0,1]:.6f}, K02={km[0,2]:.6f}",
    )
    check(
        "The physical CP tensor is already nonzero on the branch sample",
        abs(np.imag(km[0, 1] ** 2)) > 1e-8 or abs(np.imag(km[0, 2] ** 2)) > 1e-8,
        f"cp_pair={cp_pair_from_h(h)}",
    )

    print()
    print("  The remaining bridge is no longer tied to an arbitrary orbit")
    print("  representative. On the positive section it is an intrinsic function of H.")


def part3_generic_full_rank_h_patch_is_cp_supporting() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE GENERIC FULL-RANK H PATCH IS CP-SUPPORTING ON THE POSITIVE SECTION")
    print("=" * 88)

    rng = np.random.default_rng(17)
    good = True
    nonzero = 0
    for _ in range(80):
        x = rng.uniform(0.2, 1.6, size=3)
        y = rng.uniform(0.2, 1.6, size=3)
        delta = float(rng.uniform(0.3, 2.5))
        h = canonical_y(x, y, delta) @ canonical_y(x, y, delta).conj().T
        cp1, cp2 = cp_pair_from_h(h)
        if abs(cp1) > 1e-8 or abs(cp2) > 1e-8:
            nonzero += 1
        else:
            good = False
            break

    check(
        "Random generic canonical samples give nonzero intrinsic CP on the positive section",
        good,
        f"nonzero count = {nonzero}",
    )
    check(
        "So the positive polar section is not generically CP-empty",
        good,
        "the raw right-frame blocker was stronger than the true generic endpoint",
    )

    print()
    print("  The generic full-rank H patch already carries a constructive intrinsic")
    print("  post-canonical bridge. The next question is which H-law the branch fixes.")


def part4_bank_records_the_new_endpoint() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE BANK RECORDS THE NEW POSITIVE-SECTION ENDPOINT")
    print("=" * 88)

    note = read("docs/DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md")
    atlas = read("docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    blocker = read("docs/DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md")

    check(
        "The new note states Y_+(H) = H^(1/2) and K_+(H) = H",
        "Y_+(H)" in note and "K_+(H) = H" in note,
    )
    check(
        "The atlas carries the DM post-canonical polar section row",
        "| DM neutrino post-canonical positive polar section |" in atlas,
    )
    check(
        "The blocker note now says the raw right-frame obstruction is no longer the final endpoint",
        "Y_+(H) = H^(1/2)" in blocker
        or "generic full-rank patch" in blocker
        or "generic right orbit already has one" in blocker
        or "Hermitian-data side" in blocker,
    )

    print()
    print("  The branch endpoint is now cleaner: the remaining obstruction is not")
    print("  a generic no-section claim, but whatever H-law the branch actually fixes.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO POST-CANONICAL POSITIVE POLAR SECTION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Can the generic full-rank DM right orbit make the post-canonical")
    print("  slot-supported bridge intrinsic from H = Y Y^dag alone?")

    h = part1_generic_right_orbit_has_unique_positive_representative()
    part2_the_postcanonical_bridge_is_read_directly_from_h(h)
    part3_generic_full_rank_h_patch_is_cp_supporting()
    part4_bank_records_the_new_endpoint()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact positive-section answer:")
    print("    - the generic full-rank right orbit has the unique positive representative Y_+(H)=H^(1/2)")
    print("    - on that representative, K_+(H)=H")
    print("    - the post-canonical singlet-doublet slot bridge is read intrinsically from H")
    print("    - the generic full-rank H patch is CP-supporting on that route")
    print()
    print("  So the raw right-frame obstruction is not the last blocker.")
    print("  The live DM question moves to the Hermitian-data law H itself.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
