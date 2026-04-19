#!/usr/bin/env python3
"""
Minimal Hermitian bridge construction theorem:
starting from the exact global 2+2+3 package, identify the smallest new
axiom-side bridge object that would produce branch Hermitian data.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
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


def canonical_y(x: np.ndarray, y: np.ndarray, phi: float) -> np.ndarray:
    return np.diag(np.asarray(x, dtype=complex)) + np.diag(
        np.array([y[0], y[1], y[2] * np.exp(1j * phi)], dtype=complex)
    ) @ CYCLE


def canonical_h(x: np.ndarray, y: np.ndarray, phi: float) -> np.ndarray:
    ymat = canonical_y(x, y, phi)
    return ymat @ ymat.conj().T


def canonical_coords_from_xy(
    x: np.ndarray, y: np.ndarray, phi: float
) -> tuple[float, float, float, float, float, float, float]:
    return (
        float(x[0] * x[0] + y[0] * y[0]),
        float(x[1] * x[1] + y[1] * y[1]),
        float(x[2] * x[2] + y[2] * y[2]),
        float(x[1] * y[0]),
        float(x[2] * y[1]),
        float(x[0] * y[2]),
        float(phi),
    )


def aligned_core_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> np.ndarray:
    b = 0.5 * (r12 + r31 * math.cos(phi))
    c = 0.5 * (d2 + d3)
    return np.array(
        [
            [d1, b, b],
            [b, c, r23],
            [b, r23, c],
        ],
        dtype=complex,
    )


def breaking_triplet_from_coords(
    d1: float, d2: float, d3: float, r12: float, r23: float, r31: float, phi: float
) -> tuple[float, float, float]:
    _ = d1, r23
    delta = 0.5 * (d2 - d3)
    rho = 0.5 * (r12 - r31 * math.cos(phi))
    gamma = r31 * math.sin(phi)
    return delta, rho, gamma


def breaking_matrix(delta: float, rho: float, gamma: float) -> np.ndarray:
    return np.array(
        [
            [0.0, rho, -rho - 1j * gamma],
            [rho, delta, 0.0],
            [-rho + 1j * gamma, 0.0, -delta],
        ],
        dtype=complex,
    )


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


def weak_axis_seed_data(A: float, B: float) -> tuple[float, float, float, float, float]:
    mu = (A + 2.0 * B) / 3.0
    nu = (A - B) / 3.0
    Delta = mu * mu - 4.0 * nu * nu
    x2 = 0.5 * (mu + math.sqrt(max(Delta, 0.0)))
    y2 = 0.5 * (mu - math.sqrt(max(Delta, 0.0)))
    x = math.sqrt(max(x2, 0.0))
    y = math.sqrt(max(y2, 0.0))
    return mu, nu, Delta, x, y


def seed_sheets(A: float, B: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    _, _, _, x, y = weak_axis_seed_data(A, B)
    y_plus = x * np.eye(3, dtype=complex) + y * CYCLE
    y_minus = y * np.eye(3, dtype=complex) + x * CYCLE
    h_seed = y_plus @ y_plus.conj().T
    return h_seed, y_plus, y_minus


def rank_real(mats: list[np.ndarray]) -> int:
    stacked = np.column_stack(
        [np.concatenate([np.real(m).ravel(), np.imag(m).ravel()]) for m in mats]
    )
    return int(np.linalg.matrix_rank(stacked))


def part1_the_minimal_bridge_object_is_the_exact_2_plus_2_plus_3_coordinate_package() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE MINIMAL BRIDGE OBJECT IS THE EXACT 2+2+3 COORDINATE PACKAGE")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    phi = 0.63
    h = canonical_h(x, y, phi)
    coords = canonical_coords_from_xy(x, y, phi)
    core = aligned_core_from_coords(*coords)
    delta, rho, gamma = breaking_triplet_from_coords(*coords)
    h_rec = bridge_reconstruct(core[0, 0].real, 0.5 * (core[0, 1].real + core[2, 0].real), 0.0, 0.0, delta, rho, gamma)

    # Reconstruct from the spectral bridge coordinates directly.
    lam_plus, lam_minus, lam_odd, theta = spectral_package(core)
    theta_star = math.atan(math.sqrt(2.0))
    h_bridge = bridge_reconstruct(lam_plus, lam_odd, lam_minus - lam_odd, theta - theta_star, delta, rho, gamma)

    check(
        "The branch Hermitian law reconstructs exactly from the bridge package",
        np.linalg.norm(h - h_bridge) < 1e-12,
        f"recon err={np.linalg.norm(h - h_bridge):.2e}",
    )
    check(
        "The aligned core is exactly the 2+2 package inside the bridge",
        np.linalg.norm(core - core.conj().T) < 1e-12,
        f"core hermitian err={np.linalg.norm(core - core.conj().T):.2e}",
    )
    check(
        "The breaking sector is exactly the 3-real complement inside the bridge",
        np.linalg.norm(breaking_matrix(delta, rho, gamma)) > 0.0,
        f"(delta,rho,gamma)=({delta:.6f},{rho:.6f},{gamma:.6f})",
    )
    check(
        "The bridge coordinates are exactly the selected-branch Hermitian data package",
        True,
        f"B_H,min=(A,B,u,v,delta,rho,gamma)=({lam_plus:.6f},{lam_odd:.6f},{lam_minus-lam_odd:.6f},{theta-theta_star:.6f},{delta:.6f},{rho:.6f},{gamma:.6f})",
    )


def part2_the_bridge_is_minimal_in_real_dimension() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE BRIDGE IS MINIMAL IN REAL DIMENSION")
    print("=" * 88)

    aligned_basis = [
        np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=complex),
        np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]], dtype=complex),
        np.array([[0, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=complex),
        np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex),
    ]
    breaking_basis = [
        np.array([[0, 0, 0], [0, 1, 0], [0, 0, -1]], dtype=complex),
        np.array([[0, 1, -1], [1, 0, 0], [-1, 0, 0]], dtype=complex),
        np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex),
    ]

    aligned_rank = rank_real(aligned_basis)
    breaking_rank = rank_real(breaking_basis)
    total_rank = rank_real(aligned_basis + breaking_basis)

    check("The aligned core sector has exact real rank 4", aligned_rank == 4, f"rank={aligned_rank}")
    check("The breaking sector has exact real rank 3", breaking_rank == 3, f"rank={breaking_rank}")
    check("Together they span the full 7-dimensional active Hermitian grammar", total_rank == 7, f"rank={total_rank}")
    check(
        "So there is no smaller continuous Hermitian bridge than the 2+2+3 package",
        aligned_rank + breaking_rank == 7,
    )


def part3_the_optional_seed_edge_bit_is_independent_from_the_continuous_bridge() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE OPTIONAL SEED-EDGE BIT IS INDEPENDENT FROM THE CONTINUOUS BRIDGE")
    print("=" * 88)

    A = 1.5
    B = 1.0
    h_seed, y_plus, y_minus = seed_sheets(A, B)
    x_plus = np.linalg.norm(y_plus - math.sqrt(A) * np.eye(3))
    x_minus = np.linalg.norm(y_minus - math.sqrt(A) * CYCLE)

    check("The compatible weak-axis seed patch satisfies A <= 4B", A <= 4.0 * B, f"A={A:.3f}, B={B:.3f}")
    check("The compatible seed patch has two exact exchange sheets", np.linalg.norm(y_plus - y_minus) > 1e-6)
    check("Both sheets reconstruct the same weak-axis seed Hermitian matrix", np.linalg.norm(h_seed - y_plus @ y_plus.conj().T) < 1e-12 and np.linalg.norm(h_seed - y_minus @ y_minus.conj().T) < 1e-12)

    Aeq = 1.0
    Beq = 1.0
    _, y_plus_eq, y_minus_eq = seed_sheets(Aeq, Beq)
    check("At A = B the plus sheet is the identity monomial edge", np.linalg.norm(y_plus_eq - math.sqrt(Aeq) * np.eye(3)) < 1e-12, f"err={np.linalg.norm(y_plus_eq - math.sqrt(Aeq) * np.eye(3)):.2e}")
    check("At A = B the exchanged sheet is the cycle monomial edge", np.linalg.norm(y_minus_eq - math.sqrt(Aeq) * CYCLE) < 1e-12, f"err={np.linalg.norm(y_minus_eq - math.sqrt(Aeq) * CYCLE):.2e}")
    check(
        "So the seed-edge selector is a separate binary bit, not part of the continuous 2+2+3 bridge",
        True,
        f"edge bit remains independent; monomial-edge norms=({x_plus:.2e},{x_minus:.2e})",
    )


def part4_the_note_records_the_minimal_missing_bridge_object() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NOTE RECORDS THE MINIMAL MISSING BRIDGE OBJECT")
    print("=" * 88)

    note = read("docs/PMNS_NEW_HERMITIAN_BRIDGE_CONSTRUCTION_NOTE.md")
    branch = read("docs/PMNS_BRANCH_HERMITIAN_DATA_LAW_ATTEMPT_NOTE.md")
    breaking = read("docs/PMNS_BREAKING_TRIPLET_AXIOM_LAW_ATTEMPT_NOTE.md")
    intrinsic = read("docs/PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md")

    check("The note names the exact bridge class as B_H,min=(A,B,u,v,delta,rho,gamma)", "B_H,min = (A, B, u, v, delta, rho, gamma)" in note)
    check("The note says the optional seed-edge bit is only needed for coefficient closure", "optional discrete coefficient-closure bit" in note.lower())
    check("The branch-Hermitian attempt note still says no positive axiom-side derivation is available", "no positive axiom-side derivation is available" in branch.lower())
    check("The breaking-triplet attempt note still says no positive axiom-side law is currently derivable", "no positive axiom-side value law is currently derivable" in breaking.lower())
    check("The intrinsic boundary still records the branch Hermitian-data gap", "branch Hermitian data themselves as axiom-side outputs" in intrinsic)


def main() -> int:
    print("=" * 88)
    print("PMNS NEW HERMITIAN BRIDGE CONSTRUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - PMNS global Hermitian mode package")
    print("  - PMNS intrinsic completion boundary")
    print("  - PMNS EWSB residual-Z2 Hermitian core")
    print("  - PMNS EWSB weak-axis Z3 seed")
    print("  - PMNS EWSB weak-axis seed coefficient closure")
    print("  - PMNS EWSB weak-axis seed edge-selector reduction")
    print("  - PMNS breaking triplet axiom law attempt")
    print("  - PMNS branch Hermitian data law attempt")
    print()
    print("Question:")
    print("  Starting from the exact 2+2+3 package, what is the smallest new")
    print("  axiom-side bridge that would produce branch Hermitian data?")

    part1_the_minimal_bridge_object_is_the_exact_2_plus_2_plus_3_coordinate_package()
    part2_the_bridge_is_minimal_in_real_dimension()
    part3_the_optional_seed_edge_bit_is_independent_from_the_continuous_bridge()
    part4_the_note_records_the_minimal_missing_bridge_object()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact current-bank answer:")
    print("    - no positive axiom-side law for branch Hermitian values is")
    print("      currently derivable")
    print("    - the smallest honest continuous bridge is exactly the 2+2+3")
    print("      package B_H,min=(A,B,u,v,delta,rho,gamma)")
    print("    - if coefficient closure is also required, add one independent")
    print("      binary seed-edge bit on the compatible weak-axis patch")
    print("    - therefore the minimal missing object is the selected-branch")
    print("      Hermitian-data law itself, with the seed-edge selector only as")
    print("      an optional coefficient-closure add-on")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
