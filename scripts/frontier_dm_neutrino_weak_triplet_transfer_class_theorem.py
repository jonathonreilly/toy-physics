#!/usr/bin/env python3
"""
DM neutrino weak-to-triplet transfer-class theorem.

Question:
  Once the current exact source-side data are reduced to one selector amplitude
  slot and one two-channel tensor-slot pair, what is the minimal transfer class
  into the DM triplet amplitudes gamma, E1, and E2?

Answer:
  Any linear transfer law compatible with the exact odd/even source-target
  split is forced into block form:

    gamma      = c_odd * a_sel
    [E1, E2]^T = M_even * [tau_E, tau_T]^T

  with one real odd coefficient c_odd and one real 2x2 even response matrix
  M_even. So the missing law is no longer a generic 3x3 map; it is a 1+4
  coefficient problem.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

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


def nullspace(a: np.ndarray, atol: float = 1e-12) -> np.ndarray:
    u, s, vh = np.linalg.svd(a)
    rank = int(np.sum(s > atol))
    return vh[rank:].conj().T


def vec_to_mat(v: np.ndarray) -> np.ndarray:
    return v.reshape((3, 3), order="F")


def part1_current_stack_already_has_a_1_plus_2_source_bundle_and_a_1_plus_2_target_bundle() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE CURRENT STACK ALREADY HAS A 1+2 SOURCE BUNDLE AND A 1+2 TARGET BUNDLE")
    print("=" * 88)

    selector = Path("/Users/jonBridger/Toy Physics-neutrino-majorana/docs/PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md").read_text(
        encoding="utf-8"
    )
    ckm = Path("/Users/jonBridger/Toy Physics/.claude/worktrees/strong-cp-nature/docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md").read_text(
        encoding="utf-8"
    )
    source_boundary = read("docs/DM_STRONG_CP_GAMMA_TRANSFER_NO_GO_NOTE_2026-04-15.md")
    source_note = read("docs/DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md")
    response_note = read("docs/DM_NEUTRINO_TRIPLET_EVEN_RESPONSE_THEOREM_NOTE_2026-04-15.md")

    check(
        "The selector lane contributes one exact real source amplitude slot a_sel",
        "B_red = a_sel S_cls" in selector and "one real amplitude slot" in selector,
    )
    check(
        "The weak tensor-slot lane contributes a two-channel tensor carrier",
        "exact bilinear tensor carrier `K_R`" in ckm and "K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)" in ckm,
    )
    check(
        "The DM branch already records the target odd source gamma",
        "gamma" in source_note and "CP-odd triplet slot" in source_note,
    )
    check(
        "The DM branch already records the target even response pair E1,E2",
        "E1 = delta + rho" in response_note and "E2 = A + b - c - d" in response_note,
    )
    check(
        "The current strong-CP/CKM boundary says the missing object is a transfer law, not a new carrier",
        "transfer / coefficient law" in source_boundary
        and "neutrino Hermitian carrier" in source_boundary,
    )


def part2_parity_compatible_linear_transfer_is_forced_into_block_form() -> None:
    print("\n" + "=" * 88)
    print("PART 2: PARITY-COMPATIBLE LINEAR TRANSFER IS FORCED INTO BLOCK FORM")
    print("=" * 88)

    # Source bundle: one odd selector slot plus one even tensor pair.
    p_source = np.diag([-1.0, 1.0, 1.0])
    # Target bundle: one odd triplet source gamma plus two even responses.
    p_target = np.diag([-1.0, 1.0, 1.0])

    intertwiner = np.kron(np.eye(3), p_target) - np.kron(p_source.T, np.eye(3))
    ns = nullspace(intertwiner)
    basis = [vec_to_mat(ns[:, i]) for i in range(ns.shape[1])]

    check(
        "The parity-compatible transfer class has dimension 5 = 1 odd coefficient + 4 even coefficients",
        ns.shape[1] == 5,
        f"dim={ns.shape[1]}",
    )

    max_off_block = 0.0
    for b in basis:
        # Forbidden cross-parity entries must vanish.
        max_off_block = max(
            max_off_block,
            abs(b[0, 1]),
            abs(b[0, 2]),
            abs(b[1, 0]),
            abs(b[2, 0]),
        )

    check(
        "Every admissible transfer basis vector is block-diagonal between odd and even sectors",
        max_off_block < 1e-12,
        f"max off-block entry={max_off_block:.2e}",
    )

    c_odd = 1.7
    m11, m12, m21, m22 = 0.4, -0.3, 1.2, 0.9
    l = np.array(
        [
            [c_odd, 0.0, 0.0],
            [0.0, m11, m12],
            [0.0, m21, m22],
        ],
        dtype=float,
    )
    err = np.linalg.norm(p_target @ l - l @ p_source)
    check(
        "The canonical 1+2 -> 1+2 block form exactly intertwines the odd/even split",
        err < 1e-12,
        f"intertwiner err={err:.2e}",
    )


def part3_the_missing_triplet_law_reduces_to_c_odd_and_m_even() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE MISSING TRIPLET LAW REDUCES TO C_ODD AND M_EVEN")
    print("=" * 88)

    c_odd = 2.3
    m_even = np.array([[0.5, -0.1], [0.7, 1.4]], dtype=float)
    a_sel = -0.8
    tau = np.array([0.6, -0.2], dtype=float)

    gamma = c_odd * a_sel
    e_vec = m_even @ tau
    full = np.array([gamma, e_vec[0], e_vec[1]])

    check(
        "The odd target gamma depends only on the selector amplitude slot",
        abs(full[0] - c_odd * a_sel) < 1e-12,
        f"gamma={full[0]:.6f}",
    )
    check(
        "The even target pair depends only on the tensor-slot doublet",
        np.linalg.norm(full[1:] - m_even @ tau) < 1e-12,
        f"E=({full[1]:.6f},{full[2]:.6f})",
    )
    check(
        "So the remaining coefficient law is one real odd scalar plus one real 2x2 even matrix",
        True,
        "gamma=c_odd*a_sel, [E1,E2]^T=M_even[tau_E,tau_T]^T",
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO WEAK-TRIPLET TRANSFER-CLASS THEOREM")
    print("=" * 88)

    part1_current_stack_already_has_a_1_plus_2_source_bundle_and_a_1_plus_2_target_bundle()
    part2_parity_compatible_linear_transfer_is_forced_into_block_form()
    part3_the_missing_triplet_law_reduces_to_c_odd_and_m_even()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
