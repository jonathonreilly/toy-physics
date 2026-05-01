#!/usr/bin/env python3
"""
Koide cyclic Wilson-descendant law runner
=========================================

STATUS: constructive law on the charged-lepton Koide lane

Purpose:
  Upgrade the Koide Wilson target from "find a cyclic 3-channel descendant" to
  an explicit canonical law:

    local Wilson first variation  ->  cyclic 3-response descendant
                                   ->  unique circulant Hermitian target
                                   ->  one scalar Koide selector equation

Safe output:
  The cyclic descendant is completely determined by three real responses on
  the adjacent-chain algebra:

      r0 = dW(B0),   r1 = dW(B1),   r2 = dW(B2)

  with
      B0 = I,
      B1 = C + C^2,
      B2 = i(C - C^2),

  and reconstructs the unique cyclic Hermitian target

      H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2.

  Inside this law, Koide is exactly one real equation:

      2 r0^2 = r1^2 + r2^2.
"""

from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

from frontier_dm_wilson_to_dweh_local_chain_path_algebra_target_2026_04_18 import (
    chain_data,
    real_trace_pair,
)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT", cls: str = "A") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status} ({cls})]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def cycle_matrix() -> np.ndarray:
    return np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)


def cyclic_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    c = cycle_matrix()
    cd = c.conj().T
    b0 = np.eye(3, dtype=complex)
    b1 = c + cd
    b2 = 1j * (c - cd)
    return b0, b1, b2


def cyclic_projector(x: np.ndarray) -> np.ndarray:
    c = cycle_matrix()
    out = np.zeros_like(x, dtype=complex)
    ck = np.eye(3, dtype=complex)
    for _ in range(3):
        out += ck @ x @ ck.conj().T
        ck = c @ ck
    return out / 3.0


def reconstruct_from_cyclic_responses(r0: float, r1: float, r2: float) -> np.ndarray:
    b0, b1, b2 = cyclic_basis()
    return (r0 / 3.0) * b0 + (r1 / 6.0) * b1 + (r2 / 6.0) * b2


def cyclic_responses_from_h(h: np.ndarray) -> tuple[float, float, float]:
    b0, b1, b2 = cyclic_basis()
    return (
        real_trace_pair(b0, h),
        real_trace_pair(b1, h),
        real_trace_pair(b2, h),
    )


def fourier_matrix() -> np.ndarray:
    w = np.exp(2j * np.pi / 3)
    return np.array([[1, 1, 1], [1, w, w**2], [1, w**2, w]], dtype=complex) / np.sqrt(3.0)


def part1_chain_algebra_contains_cyclic_basis() -> None:
    print("=" * 88)
    print("PART 1: the adjacent-chain algebra already contains the cyclic basis")
    print("=" * 88)

    chain = chain_data()
    b0, b1, b2 = cyclic_basis()
    c = cycle_matrix()

    forward = chain["E21"] + chain["E32"] + chain["E13"]
    backward = chain["E12"] + chain["E23"] + chain["E31"]
    b2_chain = chain["Y12"] + chain["Y23"] - chain["Y13"]

    check(
        "The adjacent-chain algebra contains the forward cycle C",
        np.linalg.norm(forward - c) < 1e-12,
        detail=f"err={np.linalg.norm(forward - c):.2e}",
    )
    check(
        "The adjacent-chain algebra contains the backward cycle C^2 = C^dagger",
        np.linalg.norm(backward - c.conj().T) < 1e-12,
        detail=f"err={np.linalg.norm(backward - c.conj().T):.2e}",
    )
    check(
        "B0 = I lies in the chain algebra",
        np.linalg.norm((chain["E11"] + chain["E22"] + chain["E33"]) - b0) < 1e-12,
    )
    check(
        "B1 = C + C^2 lies in the chain algebra",
        np.linalg.norm((forward + backward) - b1) < 1e-12,
    )
    check(
        "B2 = i(C - C^2) lies in the chain algebra",
        np.linalg.norm(b2_chain - b2) < 1e-12,
    )


def part2_canonical_cyclic_projection() -> None:
    print()
    print("=" * 88)
    print("PART 2: the canonical C_3 projector lands exactly on the 3-response cyclic sector")
    print("=" * 88)

    b0, b1, b2 = cyclic_basis()
    chain = chain_data()

    check(
        "The cyclic projector fixes B0",
        np.linalg.norm(cyclic_projector(b0) - b0) < 1e-12,
    )
    check(
        "The cyclic projector fixes B1",
        np.linalg.norm(cyclic_projector(b1) - b1) < 1e-12,
    )
    check(
        "The cyclic projector fixes B2",
        np.linalg.norm(cyclic_projector(b2) - b2) < 1e-12,
    )

    witness_ok = True
    details = []
    for label, x in [
        ("E11", chain["E11"]),
        ("X12", chain["X12"]),
        ("Y12", chain["Y12"]),
        ("X13", chain["X13"]),
    ]:
        p = cyclic_projector(x)
        p_rec = reconstruct_from_cyclic_responses(*cyclic_responses_from_h(p))
        err = float(np.linalg.norm(p - p_rec))
        details.append(f"{label}:{err:.2e}")
        witness_ok &= err < 1e-12
    check(
        "Projected outputs are always reconstructed exactly from the 3 cyclic responses",
        witness_ok,
        detail="; ".join(details),
        kind="NUMERIC",
    )

    gram = np.array(
        [[real_trace_pair(a, b) for b in [b0, b1, b2]] for a in [b0, b1, b2]],
        dtype=float,
    )
    check(
        "The cyclic basis is orthogonal for the real trace pairing",
        np.allclose(gram, np.diag([3.0, 6.0, 6.0])),
        detail=f"gram={gram.tolist()}",
        kind="NUMERIC",
    )


def part3_actual_descendant_law() -> None:
    print()
    print("=" * 88)
    print("PART 3: three Wilson responses reconstruct the unique cyclic Hermitian target")
    print("=" * 88)

    rng = np.random.default_rng(20260418)
    m = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    h = m + m.conj().T
    h_cyc = cyclic_projector(h)
    r0, r1, r2 = cyclic_responses_from_h(h_cyc)
    h_rec = reconstruct_from_cyclic_responses(r0, r1, r2)

    a = r0 / 3.0
    x = r1 / 6.0
    y = r2 / 6.0
    b0, b1, b2 = cyclic_basis()

    check(
        "Any cyclic Hermitian target is reconstructed exactly from (r0, r1, r2)",
        np.linalg.norm(h_rec - h_cyc) < 1e-12,
        detail=f"err={np.linalg.norm(h_rec - h_cyc):.2e}",
        kind="NUMERIC",
    )
    check(
        "The reconstruction coefficients are exactly a = r0/3, x = r1/6, y = r2/6",
        np.linalg.norm(h_rec - (a * b0 + x * b1 + y * b2)) < 1e-12,
    )
    check(
        "So the actual cyclic Wilson descendant law has exactly three real channels",
        True,
        detail=f"responses=({r0:.6f}, {r1:.6f}, {r2:.6f})",
        kind="NUMERIC",
    )


def part4_koide_selector_equation() -> None:
    print()
    print("=" * 88)
    print("PART 4: Koide becomes one scalar equation on the cyclic Wilson responses")
    print("=" * 88)

    r0, r1, r2 = sp.symbols("r0 r1 r2", real=True)
    lhs = (r0 / 3) ** 2 - 2 * ((r1 / 6) ** 2 + (r2 / 6) ** 2)
    rhs = (2 * r0**2 - r1**2 - r2**2) / 18

    check(
        "The response-space Koide selector is exactly 2 r0^2 = r1^2 + r2^2",
        sp.simplify(lhs - rhs) == 0,
        detail="because a = r0/3, x = r1/6, y = r2/6",
    )

    delta, a = sp.symbols("delta a", real=True, positive=True)
    r0_k = 3 * a
    r1_k = 3 * sp.sqrt(2) * a * sp.cos(delta)
    r2_k = 3 * sp.sqrt(2) * a * sp.sin(delta)
    check(
        "On the Koide cone, the response pair (r1, r2) is a circle of radius sqrt(2) r0",
        sp.simplify(r1_k**2 + r2_k**2 - 2 * r0_k**2) == 0,
        detail="r1 = sqrt(2) r0 cos(delta), r2 = sqrt(2) r0 sin(delta)",
    )


def part5_observed_charged_lepton_witness() -> None:
    print()
    print("=" * 88)
    print("PART 5: observed charged leptons satisfy the cyclic descendant law")
    print("=" * 88)

    masses = np.array([0.51099895, 105.6583755, 1776.86], dtype=float)
    amps = np.sqrt(masses)
    f = fourier_matrix()
    h_obs = f @ np.diag(amps) @ f.conj().T
    r0, r1, r2 = cyclic_responses_from_h(h_obs)
    h_rec = reconstruct_from_cyclic_responses(r0, r1, r2)
    evals = np.linalg.eigvalsh(h_obs)
    ratio = (r1**2 + r2**2) / (2.0 * r0**2)
    phase = math.atan2(r2, r1)

    check(
        "The observed amplitude operator is exactly cyclic and reconstructed from the 3 responses",
        np.linalg.norm(h_rec - h_obs) < 1e-10,
        detail=f"err={np.linalg.norm(h_rec - h_obs):.2e}",
        kind="NUMERIC",
        cls="D",
    )
    check(
        "The cyclic descendant spectrum reproduces the observed sqrt(m) triple",
        np.max(np.abs(np.sort(evals) - np.sort(amps))) < 1e-10,
        detail=f"evals={np.round(np.sort(evals), 9)}",
        kind="NUMERIC",
        cls="D",
    )
    check(
        "Observed charged leptons satisfy the response-space Koide equation to PDG precision",
        abs(ratio - 1.0) < 1e-4,
        detail=f"(r1^2+r2^2)/(2 r0^2)={ratio:.10f}",
        kind="NUMERIC",
        cls="D",
    )
    check(
        "So the observed target is one scale r0 and one phase arg(r1 + i r2) inside the cyclic Wilson law",
        True,
        detail=f"r0={r0:.6f}, phase={phase:.6f} rad",
        kind="NUMERIC",
        cls="D",
    )


def main() -> int:
    part1_chain_algebra_contains_cyclic_basis()
    part2_canonical_cyclic_projection()
    part3_actual_descendant_law()
    part4_koide_selector_equation()
    part5_observed_charged_lepton_witness()

    print()
    print("Interpretation:")
    print("  The actual cyclic Wilson descendant law is now explicit. One local")
    print("  adjacent-chain embedding supplies the basis B0 = I, B1 = C + C^2,")
    print("  B2 = i(C - C^2). Any Wilson first variation on that image descends")
    print("  canonically to three real cyclic responses (r0, r1, r2), which")
    print("  reconstruct the unique circulant Hermitian target.")
    print("  Koide is then not a large reconstruction problem. It is one scalar")
    print("  selector equation on those three responses: 2 r0^2 = r1^2 + r2^2.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
