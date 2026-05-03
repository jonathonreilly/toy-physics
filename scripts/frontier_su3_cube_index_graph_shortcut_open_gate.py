"""Open-gate runner for the SU(3) L_s=2 cube index-graph shortcut.

This runner does not claim the actual nontrivial cube Wigner/intertwiner
trace. It verifies the cyclic index graph used by the proposed shortcut and
computes the conditional Perron value obtained if the nontrivial traces reduce
to the uniform pairing ansatz

    T_lambda(candidate) = d_lambda^(N_components - N_links).

The missing audited step is proving that the real SU(3) nontrivial cube
traces equal this candidate graph trace.

Run:
    python3 scripts/frontier_su3_cube_index_graph_shortcut_open_gate.py
"""

from __future__ import annotations

import math
import sys
from typing import Dict, List, Tuple

import numpy as np
from scipy.special import iv


BETA = 6.0
EPSILON_WITNESS = 3.03e-4
BRIDGE_SUPPORT_TARGET = 0.5935306800


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def wilson_character_coefficient(p: int, q: int, mode_max: int, arg: float) -> float:
    """SU(3) Wilson character coefficient c_(p,q)(beta) by Bessel determinant."""
    lam = [p + q, q, 0]
    total = 0.0
    for mode in range(-mode_max, mode_max + 1):
        mat = np.array(
            [[iv(mode + lam[j] + i - j, arg) for j in range(3)] for i in range(3)],
            dtype=float,
        )
        total += float(np.linalg.det(mat))
    return total


def all_plaquettes_with_links() -> List[Tuple[Tuple[int, int, int], int, int, List[Tuple[int, int, int, int]]]]:
    """Enumerate the 12 L_s=2 PBC plaquettes with forward directed links."""
    plaquettes = []
    for plane_dir1, plane_dir2 in [(0, 1), (0, 2), (1, 2)]:
        orth = ({0, 1, 2} - {plane_dir1, plane_dir2}).pop()
        for orth_val in range(2):
            for start_in_plane_idx in range(2):
                site = [0, 0, 0]
                site[plane_dir1] = start_in_plane_idx
                site[plane_dir2] = 0
                site[orth] = orth_val
                start = tuple(site)
                cur = list(site)
                links = []
                for direction in [plane_dir1, plane_dir2, plane_dir1, plane_dir2]:
                    links.append((cur[0], cur[1], cur[2], direction))
                    cur[direction] = (cur[direction] + 1) % 2
                plaquettes.append((start, plane_dir1, plane_dir2, links))

    seen = set()
    unique = []
    for plaquette in plaquettes:
        link_set = frozenset(plaquette[3])
        if link_set not in seen:
            seen.add(link_set)
            unique.append(plaquette)
    return unique


def link_to_plaquette_slots(plaquettes: List[Tuple]) -> Dict[Tuple[int, int, int, int], List[Tuple[int, int]]]:
    out: Dict[Tuple[int, int, int, int], List[Tuple[int, int]]] = {}
    for p_idx, (_, _, _, links) in enumerate(plaquettes):
        for slot, link in enumerate(links):
            out.setdefault(link, []).append((p_idx, slot))
    return out


def build_index_graph(plaquettes: List[Tuple]) -> Tuple[int, List[Tuple[int, int]]]:
    """Build cyclic-index identifications induced by shared links."""
    n_nodes = 4 * len(plaquettes)
    edges: List[Tuple[int, int]] = []
    for occurrences in link_to_plaquette_slots(plaquettes).values():
        if len(occurrences) != 2:
            continue
        (p_a, slot_a), (p_b, slot_b) = occurrences
        in_a = 4 * p_a + (slot_a - 1) % 4
        out_a = 4 * p_a + slot_a
        in_b = 4 * p_b + (slot_b - 1) % 4
        out_b = 4 * p_b + slot_b
        edges.append((in_a, in_b))
        edges.append((out_a, out_b))
    return n_nodes, edges


def count_connected_components(n_nodes: int, edges: List[Tuple[int, int]]) -> int:
    parent = list(range(n_nodes))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for a, b in edges:
        union(a, b)
    return len({find(i) for i in range(n_nodes)})


def candidate_rho(beta: float, nmax: int, n_components: int, mode_max: int = 200) -> Dict[Tuple[int, int], float]:
    """Candidate rho under the unproved uniform-pairing trace ansatz."""
    arg = beta / 3.0
    c00 = wilson_character_coefficient(0, 0, mode_max, arg)
    rho: Dict[Tuple[int, int], float] = {}
    for p in range(nmax + 1):
        for q in range(nmax + 1):
            dim = dim_su3(p, q)
            coeff = wilson_character_coefficient(p, q, mode_max, arg)
            topological_factor = float(dim ** (n_components - 24))
            rho[(p, q)] = ((dim * coeff / c00) ** 12) * topological_factor
    norm = rho[(0, 0)]
    return {key: value / norm for key, value in rho.items()}


def dominant_weights_box(nmax: int) -> List[Tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


def recurrence_neighbors(p: int, q: int) -> List[Tuple[int, int]]:
    out = []
    for a, b in [(p + 1, q), (p - 1, q + 1), (p, q - 1), (p, q + 1), (p + 1, q - 1), (p - 1, q)]:
        if a >= 0 and b >= 0:
            out.append((a, b))
    return out


def build_j(nmax: int) -> Tuple[np.ndarray, List[Tuple[int, int]], Dict[Tuple[int, int], int]]:
    weights = dominant_weights_box(nmax)
    index = {weight: i for i, weight in enumerate(weights)}
    j_op = np.zeros((len(weights), len(weights)), dtype=float)
    for p, q in weights:
        source = index[(p, q)]
        for neighbor in recurrence_neighbors(p, q):
            if neighbor in index:
                j_op[index[neighbor], source] += 1.0 / 6.0
    return j_op, weights, index


def build_local_factor(weights: List[Tuple[int, int]], index: Dict[Tuple[int, int], int], mode_max: int, beta: float) -> np.ndarray:
    arg = beta / 3.0
    coeffs = np.array([wilson_character_coefficient(p, q, mode_max, arg) for p, q in weights], dtype=float)
    dims = np.array([dim_su3(p, q) for p, q in weights], dtype=float)
    c00 = coeffs[index[(0, 0)]]
    a_link = coeffs / (dims * c00)
    return np.diag(a_link ** 4)


def matrix_exp_symmetric(matrix: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(matrix)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def candidate_perron_value(rho: Dict[Tuple[int, int], float], nmax: int = 7, mode_max: int = 200) -> Tuple[float, float]:
    j_op, weights, index = build_j(nmax)
    multiplier = matrix_exp_symmetric(j_op, 3.0)
    d_loc = build_local_factor(weights, index, mode_max, BETA)
    c_env = np.diag(np.array([rho.get(weight, 0.0) for weight in weights], dtype=float))
    transfer = multiplier @ d_loc @ c_env @ multiplier
    vals, vecs = np.linalg.eigh(transfer)
    idx = int(np.argmax(vals))
    psi = vecs[:, idx]
    if np.sum(psi) < 0.0:
        psi = -psi
    return float(psi @ (j_op @ psi)), float(vals[idx])


def driver() -> int:
    pass_count = 0
    support_count = 0
    fail_count = 0

    print("=" * 78)
    print("SU(3) L_s=2 Cube Index-Graph Shortcut Open Gate")
    print("=" * 78)
    print()

    plaquettes = all_plaquettes_with_links()
    print("--- Geometry ---")
    print(f"  unique plaquettes: {len(plaquettes)}")
    if len(plaquettes) == 12:
        print("  PASS: 12 plaquettes constructed")
        pass_count += 1
    else:
        print("  FAIL: expected 12 plaquettes")
        fail_count += 1

    n_nodes, edges = build_index_graph(plaquettes)
    n_components = count_connected_components(n_nodes, edges)
    print()
    print("--- Candidate index graph ---")
    print(f"  nodes: {n_nodes}")
    print(f"  identifications: {len(edges)}")
    print(f"  connected components: {n_components}")
    if (n_nodes, len(edges), n_components) == (48, 48, 8):
        print("  PASS: candidate graph count matches expected L_s=2 shortcut")
        pass_count += 1
    else:
        print("  FAIL: candidate graph count changed")
        fail_count += 1

    print()
    print("--- Candidate topological factor ---")
    exponent = n_components - 24
    print(f"  T_lambda(candidate) = d_lambda^({exponent})")
    if exponent == -16:
        print("  PASS: shortcut exponent is -16")
        pass_count += 1
    else:
        print("  FAIL: shortcut exponent is not -16")
        fail_count += 1

    print()
    print("--- Conditional rho and Perron value ---")
    rho = candidate_rho(BETA, 4, n_components)
    for key, value in sorted(rho.items(), key=lambda item: -abs(item[1]))[:6]:
        print(f"  rho_candidate_{key}(6) = {value:.6e}")
    print("  SUPPORT: rho values are conditional on the uniform-pairing trace ansatz")
    support_count += 1

    p_candidate, eig_candidate = candidate_perron_value(rho)
    print(f"  Perron eigenvalue: {eig_candidate:.10f}")
    print(f"  P_candidate(6): {p_candidate:.10f}")
    if 0.0 < p_candidate < 1.0:
        print("  SUPPORT: candidate Perron value is finite and normalized")
        support_count += 1
    else:
        print("  FAIL: candidate Perron value is out of range")
        fail_count += 1

    print()
    print("--- Bridge comparison ---")
    distance = abs(p_candidate - BRIDGE_SUPPORT_TARGET)
    print(f"  bridge-support target: {BRIDGE_SUPPORT_TARGET:.10f}")
    print(f"  distance: {distance:.6f}")
    print(f"  epsilon_witness: {EPSILON_WITNESS:.3e}")
    if distance > EPSILON_WITNESS:
        print("  SUPPORT: candidate shortcut would not close the bridge witness")
        support_count += 1
    else:
        print("  FAIL: candidate unexpectedly reaches the witness target")
        fail_count += 1

    print()
    print("Open gate:")
    print("  Prove the actual SU(3) Wigner/intertwiner traces equal d_lambda^(-16),")
    print("  or compute the traces and replace this shortcut candidate.")
    print()
    print("=" * 78)
    print(f"SUMMARY: OPEN PASS={pass_count} SUPPORT={support_count} FAIL={fail_count}")
    print("=" * 78)
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(driver())
