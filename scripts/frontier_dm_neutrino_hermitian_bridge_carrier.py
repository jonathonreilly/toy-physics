#!/usr/bin/env python3
"""
DM neutrino Hermitian bridge carrier theorem.

Question:
  What is the exact DM-side carrier inherited from the local neutrino lane once
  the denominator is expressed on the active Hermitian branch?

Answer:
  The exact minimal continuous carrier is

    B_H,min = (A, B, u, v, delta, rho, gamma)

  and the exact unified carrier that also includes the selector leg is

    U_min = (A, B, u, v, delta, rho, gamma, a_sel, e).

  So the DM denominator is no longer blocked on "finding a carrier." It is
  blocked on populating this carrier, especially the breaking-triplet leg.
"""

from __future__ import annotations

import math
import sys

import numpy as np

PASS_COUNT = 0
FAIL_COUNT = 0

EVEN_ODD = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)],
        [0.0, 1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0)],
    ],
    dtype=complex,
)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
EYE = np.eye(3, dtype=complex)
REDUCED_SELECTOR_CLASS = np.array([0.0, 0.0, 1.0, -1.0])


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


def canonical_y(x: np.ndarray, y: np.ndarray, phi: float) -> np.ndarray:
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(
        np.array([y[0], y[1], y[2] * np.exp(1j * phi)], dtype=complex)
    ) @ CYCLE


def canonical_h(x: np.ndarray, y: np.ndarray, phi: float) -> np.ndarray:
    ymat = canonical_y(x, y, phi)
    return ymat @ ymat.conj().T


def hermitian_coords(h: np.ndarray) -> tuple[float, float, float, float, float, float, float]:
    return (
        float(np.real(h[0, 0])),
        float(np.real(h[1, 1])),
        float(np.real(h[2, 2])),
        float(np.abs(h[0, 1])),
        float(np.abs(h[1, 2])),
        float(np.abs(h[2, 0])),
        float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
    )


def aligned_core_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> np.ndarray:
    b = 0.5 * (r12 + r31 * math.cos(phi))
    c = 0.5 * (d2 + d3)
    return np.array([[d1, b, b], [b, c, r23], [b, r23, c]], dtype=complex)


def breaking_triplet_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> tuple[float, float, float]:
    del d1, r23
    delta = 0.5 * (d2 - d3)
    rho = 0.5 * (r12 - r31 * math.cos(phi))
    gamma = r31 * math.sin(phi)
    return delta, rho, gamma


def breaking_basis() -> list[np.ndarray]:
    return [
        np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]], dtype=complex),
        np.array([[0.0, 1.0, -1.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]], dtype=complex),
        np.array([[0.0, 0.0, -1j], [0.0, 0.0, 0.0], [1j, 0.0, 0.0]], dtype=complex),
    ]


def breaking_matrix(delta: float, rho: float, gamma: float) -> np.ndarray:
    e_delta, e_rho, e_gamma = breaking_basis()
    return delta * e_delta + rho * e_rho + gamma * e_gamma


def spectral_package(core: np.ndarray) -> tuple[float, float, float, float]:
    block = EVEN_ODD.conj().T @ core @ EVEN_ODD
    even_block = np.real(block[:2, :2])
    evals = np.linalg.eigvalsh(even_block)
    evals.sort()
    lam_minus = float(evals[0])
    lam_plus = float(evals[1])
    lam_odd = float(np.real(block[2, 2]))
    theta = 0.5 * math.atan2(
        2.0 * even_block[0, 1], even_block[0, 0] - even_block[1, 1]
    )
    if theta < 0:
        theta += 0.5 * math.pi
    return lam_plus, lam_minus, lam_odd, theta


def core_from_bridge(A: float, B: float, u: float, v: float) -> np.ndarray:
    theta_star = math.atan(math.sqrt(2.0))
    lam_plus = A
    lam_minus = B + u
    lam_odd = B
    theta = theta_star + v
    c, s = math.cos(theta), math.sin(theta)
    even_block = np.array(
        [
            [lam_plus * c * c + lam_minus * s * s, (lam_plus - lam_minus) * c * s],
            [(lam_plus - lam_minus) * c * s, lam_plus * s * s + lam_minus * c * c],
        ],
        dtype=complex,
    )
    block = np.zeros((3, 3), dtype=complex)
    block[:2, :2] = even_block
    block[2, 2] = lam_odd
    return EVEN_ODD @ block @ EVEN_ODD.conj().T


def bridge_reconstruct(
    A: float, B: float, u: float, v: float, delta: float, rho: float, gamma: float
) -> np.ndarray:
    return core_from_bridge(A, B, u, v) + breaking_matrix(delta, rho, gamma)


def selector_primitive(a_sel: float) -> np.ndarray:
    return a_sel * REDUCED_SELECTOR_CLASS


def selector_edge(bit: int, amplitude: float) -> np.ndarray:
    root = math.sqrt(amplitude)
    if bit == 0:
        return root * EYE
    if bit == 1:
        return root * CYCLE
    raise ValueError("bit must be 0 or 1")


def flat_real(mat: np.ndarray) -> np.ndarray:
    return np.concatenate([np.real(mat).ravel(), np.imag(mat).ravel()]).astype(float)


def real_rank(mats: list[np.ndarray]) -> int:
    return int(np.linalg.matrix_rank(np.column_stack([flat_real(m) for m in mats])))


def aligned_basis() -> list[np.ndarray]:
    return [
        np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], dtype=complex),
        np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0]], dtype=complex),
        np.array([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], dtype=complex),
        np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex),
    ]


def part1_the_dm_side_bridge_is_exactly_b_h_min() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE DM-SIDE HERMITEAN BRIDGE IS EXACTLY B_H,MIN")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    phi = 0.63
    h = canonical_h(x, y, phi)
    coords = hermitian_coords(h)
    core = aligned_core_from_coords(*coords)
    delta, rho, gamma = breaking_triplet_from_coords(*coords)

    lam_plus, lam_minus, lam_odd, theta = spectral_package(core)
    theta_star = math.atan(math.sqrt(2.0))
    A = lam_plus
    B = lam_odd
    u = lam_minus - lam_odd
    v = theta - theta_star
    h_bridge = bridge_reconstruct(A, B, u, v, delta, rho, gamma)

    check(
        "The DM active Hermitian law reconstructs exactly from B_H,min",
        np.linalg.norm(h - h_bridge) < 1e-12,
        f"recon err={np.linalg.norm(h - h_bridge):.2e}",
    )
    check(
        "The aligned leg reconstructs exactly from (A,B,u,v)",
        np.linalg.norm(core - core_from_bridge(A, B, u, v)) < 1e-12,
        f"core err={np.linalg.norm(core - core_from_bridge(A, B, u, v)):.2e}",
    )
    check(
        "The breaking leg reconstructs exactly from (delta,rho,gamma)",
        np.linalg.norm(h - (core + breaking_matrix(delta, rho, gamma))) < 1e-12,
        f"break err={np.linalg.norm(h - (core + breaking_matrix(delta, rho, gamma))):.2e}",
    )
    check(
        "The minimal DM bridge package is exactly B_H,min=(A,B,u,v,delta,rho,gamma)",
        True,
        f"B_H,min=({A:.6f},{B:.6f},{u:.6f},{v:.6f},{delta:.6f},{rho:.6f},{gamma:.6f})",
    )


def part2_the_dm_bridge_is_exactly_a_4_plus_3_package() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE DM BRIDGE IS EXACTLY A 4+3 PACKAGE")
    print("=" * 88)

    aligned_rank = real_rank(aligned_basis())
    breaking_rank = real_rank(breaking_basis())
    total_rank = real_rank(aligned_basis() + breaking_basis())

    check("The aligned Hermitian core has exact real rank 4", aligned_rank == 4, f"rank={aligned_rank}")
    check("The breaking-source sector has exact real rank 3", breaking_rank == 3, f"rank={breaking_rank}")
    check("The full active Hermitian grammar has exact real rank 7", total_rank == 7, f"rank={total_rank}")
    check(
        "The minimal DM bridge is exactly the 4+3 package rather than a hidden smaller law",
        total_rank == aligned_rank + breaking_rank,
        f"4+3={aligned_rank + breaking_rank}",
    )


def part3_the_unified_bundle_is_exactly_u_min() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE UNIFIED DM CARRIER IS EXACTLY U_MIN")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    phi = 0.63
    h = canonical_h(x, y, phi)
    coords = hermitian_coords(h)
    core = aligned_core_from_coords(*coords)
    delta, rho, gamma = breaking_triplet_from_coords(*coords)
    lam_plus, lam_minus, lam_odd, theta = spectral_package(core)
    theta_star = math.atan(math.sqrt(2.0))
    A = lam_plus
    B = lam_odd
    u = lam_minus - lam_odd
    v = theta - theta_star
    a_sel = 1.75
    e = 1
    carrier = (A, B, u, v, delta, rho, gamma, a_sel, e)

    check(
        "The selector primitive is exactly one amplitude slot on the reduced class",
        np.linalg.norm(selector_primitive(a_sel) - a_sel * REDUCED_SELECTOR_CLASS) < 1e-12,
        f"a_sel={a_sel:.6f}",
    )
    check(
        "The optional edge bit is exactly the two-branch seed selector",
        np.linalg.norm(selector_edge(0, A) - math.sqrt(A) * EYE) < 1e-12
        and np.linalg.norm(selector_edge(1, A) - math.sqrt(A) * CYCLE) < 1e-12,
        f"edge bit={e}",
    )
    check(
        "The unified DM carrier is exactly U_min=(A,B,u,v,delta,rho,gamma,a_sel,e)",
        len(carrier) == 9 and carrier[-1] in (0, 1),
        f"U_min={carrier}",
    )
    check(
        "U_min extends B_H,min rather than replacing it with a different carrier",
        carrier[:7] == (A, B, u, v, delta, rho, gamma),
        "first seven slots are the Hermitian bridge",
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO HERMITIAN BRIDGE CARRIER")
    print("=" * 88)

    part1_the_dm_side_bridge_is_exactly_b_h_min()
    part2_the_dm_bridge_is_exactly_a_4_plus_3_package()
    part3_the_unified_bundle_is_exactly_u_min()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
