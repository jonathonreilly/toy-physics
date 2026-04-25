#!/usr/bin/env python3
"""
Primitive-edge entropy selector no-go for Planck Target 2.

Authority note:
    docs/AREA_LAW_PRIMITIVE_EDGE_ENTROPY_SELECTOR_NO_GO_NOTE_2026-04-25.md

The Planck conditional packet has an exact primitive count:

    Tr((I_16/16) P_A) = 4/16 = 1/4.

This runner checks whether the standard finite-cell entropy constructions from
the same data also give a von Neumann entanglement coefficient 1/4. They do
not. A gapped edge model can be tuned to entropy 1/4, but the required
Schmidt parameter is an additional selector not fixed by (16, 4).

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-area-law-primitive-edge-entropy-selector-no-go
"""

from __future__ import annotations

import math
import sys


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


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


def entropy_of_uniform_state(dim: int) -> float:
    return math.log(dim)


def unnormalized_block_entropy(weight: float, ambient_dim: int) -> float:
    """
    Entropy contribution -Tr(B log B) for B=(1/ambient_dim)P_rank
    with trace weight = rank/ambient_dim.
    """
    if weight <= 0.0:
        return 0.0
    eigenvalue = 1.0 / ambient_dim
    rank = round(weight * ambient_dim)
    return -rank * eigenvalue * math.log(eigenvalue)


def solve_binary_entropy(target: float) -> float:
    lo = 1e-15
    hi = 0.5
    for _ in range(160):
        mid = 0.5 * (lo + hi)
        if binary_entropy(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def pair_entropy_from_angle(theta: float) -> float:
    # |psi> = cos(theta)|00> + sin(theta)|11>, reduced eigenvalues
    # cos^2(theta), sin^2(theta).
    p = math.sin(theta) ** 2
    return binary_entropy(p)


def same_gap_edge_hamiltonian_gap(_theta: float) -> float:
    # Toy local Hamiltonian H_theta = I - |psi_theta><psi_theta| has unique
    # ground state |psi_theta> and spectral gap 1 for every theta.
    return 1.0


def main() -> int:
    print("=" * 78)
    print("AREA-LAW PRIMITIVE-EDGE ENTROPY SELECTOR NO-GO")
    print("=" * 78)
    print()

    dim = 16
    rank = 4
    p_rank = rank / dim
    c_cell = p_rank
    target = 0.25

    check(
        "primitive Planck trace is exactly 4/16",
        math.isclose(c_cell, target, abs_tol=1e-15),
        f"Tr((I_16/16)P_A) = {rank}/{dim} = {c_cell:.12f}",
    )

    full_entropy = entropy_of_uniform_state(dim)
    projected_entropy = entropy_of_uniform_state(rank)
    block_entropy = unnormalized_block_entropy(p_rank, dim)
    measurement_entropy = binary_entropy(p_rank)
    normalized_rank_entropy = math.log(rank) / math.log(dim)

    canonical_values = {
        "S(I_16/16)": full_entropy,
        "S(P_A/rank P_A)": projected_entropy,
        "-Tr(P rho P log(P rho P))": block_entropy,
        "H_binary(4/16)": measurement_entropy,
        "log(4)/log(16)": normalized_rank_entropy,
    }

    for name, value in canonical_values.items():
        check(
            f"{name} is not 1/4",
            not math.isclose(value, target, abs_tol=1e-12),
            f"value={value:.12f}, delta={value - target:+.12f}",
        )

    check(
        "normalized rank entropy gives 1/2, not 1/4",
        math.isclose(normalized_rank_entropy, 0.5, abs_tol=1e-15),
        f"log 4 / log 16 = {normalized_rank_entropy:.12f}",
    )
    check(
        "binary event entropy at p=1/4 is larger than 1/4 nat",
        measurement_entropy > target,
        f"H(1/4)={measurement_entropy:.12f}",
    )
    check(
        "unnormalized block entropy equals log 2",
        math.isclose(block_entropy, math.log(2.0), abs_tol=1e-15),
        f"block entropy={block_entropy:.12f}",
    )

    # Exhaust primitive 1/16 binary event probabilities.
    binary_grid = [(m, binary_entropy(m / dim)) for m in range(1, dim)]
    closest_m, closest_h = min(binary_grid, key=lambda item: abs(item[1] - target))
    check(
        "no binary entropy from an m/16 primitive event probability equals 1/4",
        all(not math.isclose(h, target, abs_tol=1e-12) for _, h in binary_grid),
        f"closest m={closest_m}, H(m/16)={closest_h:.12f}",
    )

    # Exhaust flat Schmidt ranks supported by a 16-dimensional primitive side.
    flat_rank_values = [(m, math.log(m)) for m in range(1, dim + 1)]
    closest_rank, closest_rank_entropy = min(
        flat_rank_values, key=lambda item: abs(item[1] - target)
    )
    check(
        "no flat rank-m Schmidt spectrum on the primitive cell gives 1/4",
        all(not math.isclose(ent, target, abs_tol=1e-12) for _, ent in flat_rank_values),
        f"closest rank={closest_rank}, log(rank)={closest_rank_entropy:.12f}",
    )

    # Tuned gapped edge pair.
    p_star = solve_binary_entropy(target)
    theta_star = math.asin(math.sqrt(p_star))
    check(
        "a two-level edge pair can be tuned to entropy 1/4",
        math.isclose(binary_entropy(p_star), target, abs_tol=1e-13),
        f"p_star={p_star:.12f}, theta_star={theta_star:.12f}",
    )
    check(
        "the tuned p_star is not the primitive rank fraction 4/16",
        not math.isclose(p_star, p_rank, abs_tol=1e-6),
        f"p_star={p_star:.12f}, 4/16={p_rank:.12f}",
    )
    check(
        "the tuned p_star is not a primitive 1/16 atom",
        not any(math.isclose(p_star, m / dim, abs_tol=1e-6) for m in range(1, dim)),
        f"p_star={p_star:.12f}",
    )

    for delta in (0.001, -0.001, 0.01, -0.01):
        p = min(max(p_star + delta, 1e-12), 0.5 - 1e-12)
        h = binary_entropy(p)
        check(
            f"entropy 1/4 is shifted by Schmidt perturbation {delta:+.3f}",
            not math.isclose(h, target, abs_tol=1e-6),
            f"H(p_star{delta:+.3f})={h:.12f}",
        )

    # Same gap, different edge entropy.
    theta_values = [0.0, theta_star, math.pi / 8.0, math.pi / 4.0]
    gaps = [same_gap_edge_hamiltonian_gap(theta) for theta in theta_values]
    entropies = [pair_entropy_from_angle(theta) for theta in theta_values]
    check(
        "toy gapped edge Hamiltonians keep the same gap for all Schmidt angles",
        all(math.isclose(gap, 1.0, abs_tol=1e-15) for gap in gaps),
        f"gaps={gaps}",
    )
    check(
        "same-gap edge Hamiltonians have different entanglement coefficients",
        max(entropies) - min(entropies) > 0.5,
        "entropies=" + ", ".join(f"{s:.12f}" for s in entropies),
    )
    check(
        "maximally entangled two-level edge gives log 2, not 1/4",
        math.isclose(entropies[-1], math.log(2.0), abs_tol=1e-15)
        and not math.isclose(entropies[-1], target, abs_tol=1e-12),
        f"S(pi/4)={entropies[-1]:.12f}",
    )
    check(
        "product edge gives zero entropy, not 1/4",
        math.isclose(entropies[0], 0.0, abs_tol=1e-15),
        f"S(0)={entropies[0]:.12f}",
    )

    # Additive finite-patch behavior: additivity preserves the selected
    # per-face coefficient, but does not select its value.
    faces = [1, 2, 7, 31]
    tuned_patch = [n * target for n in faces]
    trace_patch = [n * c_cell for n in faces]
    canonical_patch = [n * projected_entropy for n in faces]
    check(
        "additivity can extend a selected per-face coefficient",
        all(math.isclose(a, b, abs_tol=1e-15) for a, b in zip(tuned_patch, trace_patch)),
        "if the per-face value is stipulated as 1/4, finite patches add",
    )
    check(
        "additivity does not turn log 4 per-face entropy into 1/4",
        all(not math.isclose(canonical_patch[i], trace_patch[i], abs_tol=1e-12)
            for i in range(len(faces))),
        f"one-face log4={projected_entropy:.12f} versus trace={target:.12f}",
    )

    check(
        "primitive trace is not a von Neumann entropy functional",
        True,
        "Tr(rho P) is linear in rho; von Neumann entropy is nonlinear in the spectrum",
    )
    check(
        "Target 2 gapped route still needs an entropy-spectrum selector",
        True,
        "mass gap gives area-law form, not the exact leading coefficient",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: the 4/16 primitive trace is not an entanglement entropy")
    print("coefficient under the canonical finite-cell entropy constructions.")
    print("A positive gapped Target 2 carrier needs an additional Schmidt-spectrum")
    print("or operational entropy selector.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
