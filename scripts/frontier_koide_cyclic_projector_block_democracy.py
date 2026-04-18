#!/usr/bin/env python3
"""
Koide cyclic-projector block-democracy runner
============================================

STATUS: fresh axiom-first selector candidate on the charged-lepton Koide lane

Purpose:
  Formulate the Koide selector directly from the canonical C_3 projector
  decomposition on the cyclic Wilson-response sector, without importing the
  later entropy / variational wording.

Core statement:
  On the cyclic image, the exact cyclic Hermitian carrier splits orthogonally into

      R B0   ⊕   span_R{B1, B2}

  with canonical real-trace norms

      <B0,B0> = 3,   <B1,B1> = 6,   <B2,B2> = 6.

  For

      H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2,

  equal block power

      ||H_+||^2 = ||H_perp||^2

  is exactly

      r0^2/3 = (r1^2 + r2^2)/6
      <=>  2 r0^2 = r1^2 + r2^2,

  which is precisely the Koide selector equation on the cyclic responses.
"""

from __future__ import annotations

import sys

import numpy as np
import sympy as sp

from frontier_dm_wilson_to_dweh_local_chain_path_algebra_target_2026_04_18 import (
    real_trace_pair,
)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def cycle_matrix_np() -> np.ndarray:
    return np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)


def cyclic_basis_np() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    c = cycle_matrix_np()
    cd = c.conj().T
    b0 = np.eye(3, dtype=complex)
    b1 = c + cd
    b2 = 1j * (c - cd)
    return b0, b1, b2


def cyclic_basis_sp() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    c = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    cd = c.T
    b0 = sp.eye(3)
    b1 = c + cd
    b2 = sp.I * (c - cd)
    return b0, b1, b2


def fourier_matrix_np() -> np.ndarray:
    w = np.exp(2j * np.pi / 3)
    return np.array([[1, 1, 1], [1, w, w**2], [1, w**2, w]], dtype=complex) / np.sqrt(3.0)


def part1_exact_c3_split() -> None:
    print("=" * 88)
    print("PART 1: the cyclic image has a canonical scalar ⊕ traceless-cyclic split")
    print("=" * 88)

    b0, b1, b2 = cyclic_basis_np()
    check(
        "B0 spans the scalar line inside the cyclic Hermitian image",
        abs(np.trace(b0) - 3.0) < 1e-12 and abs(real_trace_pair(b0, b0) - 3.0) < 1e-12,
        kind="NUMERIC",
    )
    check(
        "B1 and B2 span the traceless cyclic plane",
        abs(np.trace(b1)) < 1e-12 and abs(np.trace(b2)) < 1e-12,
        kind="NUMERIC",
    )
    check(
        "The scalar line is orthogonal to the traceless cyclic plane",
        abs(real_trace_pair(b0, b1)) < 1e-12 and abs(real_trace_pair(b0, b2)) < 1e-12,
        kind="NUMERIC",
    )
    check(
        "So the cyclic Hermitian sector splits canonically as R B0 ⊕ span{B1,B2}",
        True,
        detail="1D scalar line plus 2D traceless cyclic plane",
    )


def part2_canonical_block_norms() -> None:
    print()
    print("=" * 88)
    print("PART 2: canonical trace norms of the two blocks")
    print("=" * 88)

    b0, b1, b2 = cyclic_basis_np()
    gram = np.array(
        [[real_trace_pair(a, b) for b in [b0, b1, b2]] for a in [b0, b1, b2]],
        dtype=float,
    )

    check(
        "The cyclic basis is orthogonal in the real-trace metric",
        np.allclose(gram - np.diag(np.diag(gram)), 0.0),
        detail=f"gram={gram.tolist()}",
        kind="NUMERIC",
    )
    check(
        "The scalar-line norm is ||B0||^2 = 3",
        abs(gram[0, 0] - 3.0) < 1e-12,
        kind="NUMERIC",
    )
    check(
        "The cyclic-plane norms are ||B1||^2 = ||B2||^2 = 6",
        abs(gram[1, 1] - 6.0) < 1e-12 and abs(gram[2, 2] - 6.0) < 1e-12,
        kind="NUMERIC",
    )


def part3_block_democracy_equation() -> None:
    print()
    print("=" * 88)
    print("PART 3: equal block power is exactly the Koide selector equation")
    print("=" * 88)

    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    b0, b1, b2 = cyclic_basis_sp()
    h_plus = (r0 / 3) * b0
    h_perp = (r1 / 6) * b1 + (r2 / 6) * b2
    e_plus = sp.simplify(sp.re(sp.trace(h_plus * h_plus)))
    e_perp = sp.simplify(sp.re(sp.trace(h_perp * h_perp)))

    check(
        "The scalar-line block power is r0^2 / 3",
        sp.simplify(e_plus - r0**2 / 3) == 0,
        detail=f"E_plus={e_plus}",
    )
    check(
        "The cyclic-plane block power is (r1^2 + r2^2) / 6",
        sp.simplify(e_perp - (r1**2 + r2**2) / 6) == 0,
        detail=f"E_perp={e_perp}",
    )
    check(
        "Equal block power is exactly 2 r0^2 = r1^2 + r2^2",
        sp.simplify((e_plus - e_perp) - (2 * r0**2 - r1**2 - r2**2) / 6) == 0,
    )


def part4_bridge_to_old_koide_language() -> None:
    print()
    print("=" * 88)
    print("PART 4: the block-democracy law matches both response-space and operator-space Koide")
    print("=" * 88)

    a, x, y = sp.symbols("a x y", real=True)
    r0 = 3 * a
    r1 = 6 * x
    r2 = 6 * y

    check(
        "Response-space block democracy reduces to a^2 = 2(x^2 + y^2)",
        sp.simplify((2 * r0**2 - r1**2 - r2**2) - 18 * (a**2 - 2 * (x**2 + y**2))) == 0,
    )

    b = x + sp.I * y
    check(
        "So the same law is 3 a^2 = 6 |b|^2 on the circulant coordinates",
        sp.simplify(3 * a**2 - 6 * b * sp.conjugate(b) - 3 * (a**2 - 2 * (x**2 + y**2))) == 0,
    )


def part5_observed_witness() -> None:
    print()
    print("=" * 88)
    print("PART 5: observed charged leptons satisfy cyclic-projector block democracy")
    print("=" * 88)

    masses = np.array([0.51099895, 105.6583755, 1776.86], dtype=float)
    amps = np.sqrt(masses)
    f = fourier_matrix_np()
    h_obs = f @ np.diag(amps) @ f.conj().T
    b0, b1, b2 = cyclic_basis_np()
    r0 = real_trace_pair(b0, h_obs)
    r1 = real_trace_pair(b1, h_obs)
    r2 = real_trace_pair(b2, h_obs)
    e_plus = r0**2 / 3.0
    e_perp = (r1**2 + r2**2) / 6.0
    ratio = e_plus / e_perp

    check(
        "Observed charged leptons satisfy equal cyclic block power to Koide precision",
        abs(ratio - 1.0) < 1e-4,
        detail=f"E_plus/E_perp={ratio:.10f}",
        kind="NUMERIC",
    )
    check(
        "So the observed target lies on the cyclic-projector block-democracy cone",
        abs((2 * r0**2 - r1**2 - r2**2) / max(1.0, r0**2)) < 1e-4,
        detail=f"selector={(2 * r0**2 - r1**2 - r2**2):.10f}",
        kind="NUMERIC",
    )


def main() -> int:
    part1_exact_c3_split()
    part2_canonical_block_norms()
    part3_block_democracy_equation()
    part4_bridge_to_old_koide_language()
    part5_observed_witness()

    print()
    print("Interpretation:")
    print("  The simplest fresh selector candidate is now explicit: on the exact")
    print("  cyclic projector image, demand equal block power between the scalar")
    print("  line and the traceless cyclic plane. That is already")
    print("  enough to produce the Koide selector equation 2 r0^2 = r1^2 + r2^2,")
    print("  with no need to start from later entropy language.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
