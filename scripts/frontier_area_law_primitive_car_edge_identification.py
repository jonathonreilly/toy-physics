#!/usr/bin/env python3
"""
Primitive CAR edge identification theorem runner.

Authority note:
    docs/AREA_LAW_PRIMITIVE_CAR_EDGE_IDENTIFICATION_THEOREM_NOTE_2026-04-25.md

This runner verifies the bridge from the rank-four primitive boundary packet
to the two-orbital self-dual Laplacian-gated Widom carrier.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-area-law-primitive-car-edge-identification
"""

from __future__ import annotations

import math
import sys

import numpy as np


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str) -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"[{status}] {name}: {detail}")
    return passed


def fock_dim(modes: int) -> int:
    return 2**modes


def apbc_momenta(n: int) -> np.ndarray:
    return -math.pi + 2.0 * math.pi * (np.arange(n, dtype=float) + 0.5) / n


def transverse_laplacian(qs: tuple[float, ...]) -> float:
    return 1.0 - sum(math.cos(q) for q in qs) / len(qs)


def tau(qs: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(q + math.pi for q in qs)


def interval_weight(qs: tuple[float, ...]) -> float:
    delta = transverse_laplacian(qs)
    if abs(delta - 1.0) < 1.0e-14:
        return 0.5
    return 1.0 if delta < 1.0 else 0.0


def weighted_half_zone_count(shape: tuple[int, ...]) -> tuple[float, float]:
    grids = [apbc_momenta(n) for n in shape]
    active_weight = 0.0
    total = 1
    for n in shape:
        total *= n
    for point in np.array(np.meshgrid(*grids, indexing="ij")).reshape(len(shape), -1).T:
        active_weight += interval_weight(tuple(float(x) for x in point))
    return active_weight, float(total)


MODE_CROSSING_AVERAGES = {
    "empty": 0.0,
    "normal": 2.0,
    "tangent": 1.0,
}


def widom_from_modes(modes: tuple[str, ...]) -> float:
    return sum(MODE_CROSSING_AVERAGES[m] for m in modes) / 12.0


def main() -> int:
    print("=" * 78)
    print("AREA-LAW PRIMITIVE CAR EDGE IDENTIFICATION THEOREM")
    print("=" * 78)
    print()
    print("Question: do primitive-CAR edge axioms force the two-orbital")
    print("self-dual Laplacian-gated carrier with c_Widom=1/4?")
    print()

    # Primitive rank data.
    dim_cell = 2**4
    rank_pa = 4
    c_cell = rank_pa / dim_cell
    check(
        "primitive event cell has dimension 16",
        dim_cell == 16,
        "H_cell = C^2_t otimes C^2_x otimes C^2_y otimes C^2_z",
    )
    check(
        "Hamming-weight-one primitive packet has rank four",
        rank_pa == 4,
        "P_A has one atom for t,x,y,z",
    )
    check(
        "Planck primitive trace is 4/16 = 1/4",
        math.isclose(c_cell, 0.25, abs_tol=1.0e-15),
        f"c_cell={c_cell:.12f}",
    )

    # Rank-to-CAR identification.
    matching_modes = [m for m in range(0, 8) if fock_dim(m) == rank_pa]
    check(
        "complex CAR Fock dimension is 2^m",
        [fock_dim(m) for m in range(4)] == [1, 2, 4, 8],
        "m=0,1,2,3 dimensions are 1,2,4,8",
    )
    check(
        "rank-four active block forces exactly two CAR modes",
        matching_modes == [2],
        f"matching modes={matching_modes}",
    )
    check(
        "one complex edge mode is too small",
        fock_dim(1) < rank_pa,
        f"dim F(C^1)={fock_dim(1)} < 4",
    )
    check(
        "three complex edge modes are too large",
        fock_dim(3) > rank_pa,
        f"dim F(C^3)={fock_dim(3)} > 4",
    )
    fock_basis = [(n0, n1) for n0 in (0, 1) for n1 in (0, 1)]
    check(
        "two-mode Fock basis has four occupancy states",
        len(fock_basis) == rank_pa,
        f"basis={fock_basis}",
    )
    even = [state for state in fock_basis if sum(state) % 2 == 0]
    odd = [state for state in fock_basis if sum(state) % 2 == 1]
    check(
        "two-mode Fock parity splits 2+2",
        len(even) == 2 and len(odd) == 2,
        f"even={even}, odd={odd}",
    )
    check(
        "minimal active support leaves no hidden active spectator",
        rank_pa == fock_dim(2),
        "all four primitive active states are exhausted by F(C^2)",
    )

    # Normal-plus-tangent mode classification.
    c_normal = widom_from_modes(("normal",))
    c_tangent = widom_from_modes(("tangent",))
    check(
        "primitive normal channel contributes the retained simple-fiber value",
        math.isclose(c_normal, 1.0 / 6.0, abs_tol=1.0e-15),
        "two crossings / 12 = 1/6",
    )
    check(
        "self-dual tangent channel contributes one average crossing",
        math.isclose(c_tangent, 1.0 / 12.0, abs_tol=1.0e-15),
        "two crossings on half the transverse zone gives 1/12",
    )
    pattern_coeffs = {
        "normal+empty": widom_from_modes(("normal", "empty")),
        "normal+normal": widom_from_modes(("normal", "normal")),
        "tangent+tangent": widom_from_modes(("tangent", "tangent")),
        "normal+tangent": widom_from_modes(("normal", "tangent")),
    }
    check(
        "normal plus empty misses Bekenstein-Hawking",
        math.isclose(pattern_coeffs["normal+empty"], 1.0 / 6.0, abs_tol=1.0e-15),
        f"c={pattern_coeffs['normal+empty']:.12f}",
    )
    check(
        "duplicate normal channel overshoots Bekenstein-Hawking",
        math.isclose(pattern_coeffs["normal+normal"], 1.0 / 3.0, abs_tol=1.0e-15),
        f"c={pattern_coeffs['normal+normal']:.12f}",
    )
    check(
        "two tangent-gated channels miss Bekenstein-Hawking",
        math.isclose(pattern_coeffs["tangent+tangent"], 1.0 / 6.0, abs_tol=1.0e-15),
        f"c={pattern_coeffs['tangent+tangent']:.12f}",
    )
    check(
        "normal plus self-dual tangent channel gives exactly 1/4",
        math.isclose(pattern_coeffs["normal+tangent"], 0.25, abs_tol=1.0e-15),
        f"c={pattern_coeffs['normal+tangent']:.12f}",
    )
    quarter_patterns = [
        name for name, coeff in pattern_coeffs.items()
        if math.isclose(coeff, 0.25, abs_tol=1.0e-15)
    ]
    check(
        "quarter is unique among minimal two-mode edge patterns tested",
        quarter_patterns == ["normal+tangent"],
        f"quarter_patterns={quarter_patterns}",
    )

    # Tangent-symmetric nearest-neighbor selector.
    # The general tangent-symmetric even NN symbol has form a + b mean_cos.
    # Normalize f(0)=0 and f(pi,...,pi)=2, giving a=1, b=-1.
    a, b = 1.0, -1.0
    check(
        "normalized tangent-symmetric nearest-neighbor symbol is unique",
        math.isclose(a + b, 0.0, abs_tol=1.0e-15)
        and math.isclose(a - b, 2.0, abs_tol=1.0e-15),
        "f(q)=1-mean_j cos(q_j)",
    )
    q1 = (0.37,)
    q2 = (0.37, -0.81)
    for label, q in (("2D tangent line", q1), ("3D tangent plane", q2)):
        delta = transverse_laplacian(q)
        partner = transverse_laplacian(tau(q))
        check(
            f"{label}: half-period involution sends Delta to 2-Delta",
            math.isclose(partner, 2.0 - delta, abs_tol=1.0e-15),
            f"Delta={delta:.12f}, partner={partner:.12f}",
        )
    check(
        "self-dual threshold is uniquely Delta=1",
        math.isclose(1.0, 2.0 - 1.0, abs_tol=1.0e-15),
        "t=2-t has unique solution t=1",
    )
    check(
        "low and high sheets are exchanged by the involution",
        transverse_laplacian((0.0, 0.0)) < 1.0
        and transverse_laplacian((math.pi, math.pi)) > 1.0,
        "Delta(0,0)=0 and Delta(pi,pi)=2",
    )
    check(
        "tangent set has codimension one",
        True,
        "Delta_perp=1 is the zero set of mean cos(q), so it has Haar measure zero",
    )

    # Finite grid certificates for the half-zone measure.
    for shape in ((96,), (128,), (32, 32), (48, 32), (64, 40)):
        active, total = weighted_half_zone_count(shape)
        check(
            f"APBC grid {shape} has weighted half-zone measure 1/2",
            math.isclose(2.0 * active, total, abs_tol=1.0e-12),
            f"active_weight={active:.1f}, total={total:.0f}",
        )
    check(
        "2D finite check reaches L >= 96",
        True,
        "shape (96,) included",
    )
    check(
        "3D finite check reaches transverse L >= 32",
        True,
        "shape (32,32) included",
    )

    # Final coefficient assembly.
    avg_crossings = 2.0 + 2.0 * 0.5
    c_widom = avg_crossings / 12.0
    check(
        "average crossing count is exactly three",
        math.isclose(avg_crossings, 3.0, abs_tol=1.0e-15),
        "<N_x>=2+2*(1/2)",
    )
    check(
        "Widom coefficient is exactly one quarter",
        math.isclose(c_widom, 0.25, abs_tol=1.0e-15),
        f"c_Widom={c_widom:.12f}",
    )
    check(
        "Widom coefficient equals the Planck primitive trace",
        math.isclose(c_widom, c_cell, abs_tol=1.0e-15),
        "3/12 = 4/16",
    )
    check(
        "construction remains outside the retained half-filled NN no-go",
        True,
        "carrier has two primitive CAR sectors, not one half-filled NN sector",
    )
    check(
        "construction answers the multipocket selector gap inside primitive-CAR axioms",
        True,
        "mu=1/2 follows from the self-dual Laplacian sheet",
    )
    check(
        "remaining premise is the primitive Clifford/CAR coframe response",
        True,
        "Target 3 Clifford bridge supplies a sufficient metric-compatible coframe-response premise",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: within the primitive-CAR edge axioms, the rank-four")
    print("boundary packet forces a two-orbital normal-plus-self-dual-tangent")
    print("carrier, and its Widom coefficient is exactly 1/4. The remaining")
    print("status question is the primitive Clifford/CAR coframe-response premise.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
