#!/usr/bin/env python3
"""Bounded finite-volume SU(3) Wilson plaquette MC support.

This runner is deliberately modest. It checks that the accepted full
3 spatial + 1 temporal Wilson surface at beta=6 is numerically in the
canonical plaquette region already at small periodic volumes. It does not
claim an analytic solution and it does not establish a thermodynamic-limit
precision value.
"""

from __future__ import annotations

import time

import numpy as np


SEED = 42
BETA = 6.0
CANONICAL_COMPARATOR = 0.5934

PASS_COUNT = 0
FAIL_COUNT = 0


GM = np.array(
    [
        [[0, 1, 0], [1, 0, 0], [0, 0, 0]],
        [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]],
        [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
        [[0, 0, -1j], [0, 0, 0], [1j, 0, 0]],
        [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
        [[0, 0, 0], [0, 0, -1j], [0, 1j, 0]],
        [[1, 0, 0], [0, 1, 0], [0, 0, -2]] / np.sqrt(3),
    ],
    dtype=complex,
)


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def random_perturbation(epsilon: float) -> np.ndarray:
    coeffs = np.random.randn(8) * epsilon
    hamiltonian = sum(coeffs[k] * GM[k] for k in range(8)) / 2.0
    eigvals, eigvecs = np.linalg.eigh(hamiltonian)
    return eigvecs @ np.diag(np.exp(1j * eigvals)) @ eigvecs.conj().T


def build_4d_lattice(ls: int, lt: int) -> tuple[int, list[tuple[list[tuple[int, int]], int]]]:
    dims = [ls, ls, ls, lt]
    n_sites = ls * ls * ls * lt

    def site(x: int, y: int, z: int, t: int) -> int:
        return x + ls * y + ls * ls * z + ls * ls * ls * t

    def coords_for(s: int) -> list[int]:
        t = s // (ls**3)
        rem = s - t * ls**3
        z = rem // (ls**2)
        rem -= z * ls**2
        y = rem // ls
        x = rem - y * ls
        return [x, y, z, t]

    link_signs: list[int] = []
    link_idx: dict[tuple[int, int], int] = {}
    for s in range(n_sites):
        coords = coords_for(s)
        for direction in range(4):
            new_coords = coords.copy()
            new_coords[direction] = (new_coords[direction] + 1) % dims[direction]
            link_idx[(s, direction)] = len(link_signs)
            link_signs.append(1)

    plaquettes: list[tuple[list[tuple[int, int]], int]] = []
    for s in range(n_sites):
        coords = coords_for(s)
        for i in range(4):
            for j in range(i + 1, 4):
                l1 = link_idx[(s, i)]
                s1_coords = coords.copy()
                s1_coords[i] = (s1_coords[i] + 1) % dims[i]
                s1 = site(*s1_coords)
                l2 = link_idx[(s1, j)]
                s3_coords = coords.copy()
                s3_coords[j] = (s3_coords[j] + 1) % dims[j]
                s3 = site(*s3_coords)
                l3 = link_idx[(s3, i)]
                l4 = link_idx[(s, j)]
                plaquette_sign = link_signs[l1] * link_signs[l2] * link_signs[l3] * link_signs[l4]
                plaquettes.append(([(l1, +1), (l2, +1), (l3, -1), (l4, -1)], plaquette_sign))

    return len(link_signs), plaquettes


def avg_plaquette(plaquettes: list[tuple[list[tuple[int, int]], int]], links: list[np.ndarray]) -> float:
    total = 0.0
    for face_links, sign in plaquettes:
        matrix = np.eye(3, dtype=complex)
        for link_id, orientation in face_links:
            if orientation == +1:
                matrix = matrix @ links[link_id]
            else:
                matrix = matrix @ links[link_id].conj().T
        total += sign * np.real(np.trace(matrix)) / 3.0
    return float(total / len(plaquettes))


def metropolis_sweep(
    links: list[np.ndarray],
    plaquettes: list[tuple[list[tuple[int, int]], int]],
    epsilon: float,
    link_to_faces: list[list[int]],
) -> float:
    n_accept = 0
    n_total = 0
    for link_id in range(len(links)):
        old_link = links[link_id].copy()
        new_link = random_perturbation(epsilon) @ old_link
        old_sum = 0.0
        new_sum = 0.0
        for face_id in link_to_faces[link_id]:
            face_links, sign = plaquettes[face_id]
            old_matrix = np.eye(3, dtype=complex)
            for lid, orientation in face_links:
                if orientation == +1:
                    old_matrix = old_matrix @ links[lid]
                else:
                    old_matrix = old_matrix @ links[lid].conj().T
            old_sum += sign * np.real(np.trace(old_matrix))

            links[link_id] = new_link
            new_matrix = np.eye(3, dtype=complex)
            for lid, orientation in face_links:
                if orientation == +1:
                    new_matrix = new_matrix @ links[lid]
                else:
                    new_matrix = new_matrix @ links[lid].conj().T
            links[link_id] = old_link
            new_sum += sign * np.real(np.trace(new_matrix))

        delta_action = -(BETA / 3.0) * (new_sum - old_sum)
        n_total += 1
        if delta_action < 0 or np.random.rand() < np.exp(-delta_action):
            links[link_id] = new_link
            n_accept += 1
    return n_accept / n_total


def run_test(ls: int, lt: int, n_thermalize: int, n_measure: int) -> tuple[float, float]:
    print(f"\n4D periodic Wilson MC: Ls={ls}, Lt={lt}")
    n_links, plaquettes = build_4d_lattice(ls, lt)
    link_to_faces: list[list[int]] = [[] for _ in range(n_links)]
    for face_id, (face_links, _) in enumerate(plaquettes):
        for link_id, _ in face_links:
            if face_id not in link_to_faces[link_id]:
                link_to_faces[link_id].append(face_id)

    print(f"  sites={ls**3 * lt}, links={n_links}, plaquettes={len(plaquettes)}")
    links = [np.eye(3, dtype=complex) for _ in range(n_links)]
    epsilon = 0.5
    start = time.time()

    for i in range(n_thermalize):
        acceptance = metropolis_sweep(links, plaquettes, epsilon, link_to_faces)
        if (i + 1) % 100 == 0:
            print(f"  thermalize {i + 1}: P={avg_plaquette(plaquettes, links):.4f}, t={time.time() - start:.0f}s")
            if acceptance > 0.6:
                epsilon *= 1.05
            elif acceptance < 0.4:
                epsilon *= 0.95

    samples: list[float] = []
    for i in range(n_measure):
        metropolis_sweep(links, plaquettes, epsilon, link_to_faces)
        if i % 5 == 0:
            samples.append(avg_plaquette(plaquettes, links))
        if (i + 1) % 100 == 0:
            mean = float(np.mean(samples))
            err = float(np.std(samples) / np.sqrt(len(samples)))
            print(f"  measure {i + 1}: P={mean:.4f} +/- {err:.4f}, t={time.time() - start:.0f}s")

    mean = float(np.mean(samples))
    err = float(np.std(samples) / np.sqrt(len(samples)))
    print(f"  result Ls={ls}, Lt={lt}: P = {mean:.4f} +/- {err:.4f}")
    return mean, err


def main() -> int:
    np.random.seed(SEED)
    print("=" * 78)
    print("SU(3) WILSON PLAQUETTE 4D FINITE-VOLUME SUPPORT")
    print("=" * 78)
    print(f"seed={SEED}, beta={BETA}, comparator={CANONICAL_COMPARATOR}")

    p22, e22 = run_test(2, 2, n_thermalize=500, n_measure=300)
    p33, e33 = run_test(3, 3, n_thermalize=500, n_measure=200)

    print("\nBounded checks")
    check(
        "L=2 full 3+1D periodic Wilson run remains in the expected small-volume beta=6 band",
        0.60 <= p22 <= 0.65,
        detail=f"P22={p22:.4f} +/- {e22:.4f}",
    )
    check(
        "L=3 full 3+1D periodic Wilson run is in the canonical plaquette region",
        0.585 <= p33 <= 0.610,
        detail=f"P33={p33:.4f} +/- {e33:.4f}",
    )
    check(
        "the L=3 value is close to, but does not prove, the canonical L->infinity comparator",
        abs(p33 - CANONICAL_COMPARATOR) < 0.015,
        detail=f"delta={p33 - CANONICAL_COMPARATOR:+.4f}",
    )
    check(
        "the finite-volume result supports the full 3+1D surface rather than a spatial-only minimal-block reading",
        p33 > 0.55,
        detail="support-only numerical separation; not an analytic closure",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 78)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
