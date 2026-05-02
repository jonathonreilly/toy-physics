#!/usr/bin/env python3
"""Poisson/CHSH to teleportation-resource audit.

Status: planning / first artifact. This script asks a narrow question:

    Does the existing Poisson-driven CHSH ground state already contain a
    deterministic, high-fidelity encoded Bell pair usable as the resource for
    ordinary quantum state teleportation?

It does not claim matter teleportation, charge transfer, mass transfer, or FTL
transport. It only audits the two-species state produced by the existing
`frontier_bell_inequality.py` machinery.
"""

from __future__ import annotations

import argparse
import dataclasses
import math
import sys
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.linalg import eigh


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from frontier_bell_inequality import (  # noqa: E402
    build_H1,
    build_H2_tensor,
    build_pair_hop_X,
    build_poisson,
    build_sublattice_Z,
    chsh_horodecki,
    lattice_1d,
    lattice_2d,
    lattice_3d,
)


I2 = np.eye(2, dtype=complex)
X2 = np.array([[0, 1], [1, 0]], dtype=complex)
Y2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z2 = np.array([[1, 0], [0, -1]], dtype=complex)

OUTCOME_ORDER = ((0, 0), (1, 0), (0, 1), (1, 1))
OUTCOME_LABELS = {
    (0, 0): "Phi+",
    (1, 0): "Phi-",
    (0, 1): "Psi+",
    (1, 1): "Psi-",
}


@dataclasses.dataclass(frozen=True)
class AuditCase:
    label: str
    dim: int
    side: int
    mass: float
    G: float


@dataclasses.dataclass(frozen=True)
class SiteFactorization:
    logical: np.ndarray
    env: np.ndarray
    env_labels: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]


DEFAULT_CASES = (
    AuditCase("1d_null", dim=1, side=8, mass=0.0, G=0.0),
    AuditCase("1d_poisson_chsh", dim=1, side=8, mass=0.0, G=1000.0),
    AuditCase("2d_poisson_chsh", dim=2, side=4, mass=0.0, G=1000.0),
)


def lattice_for_case(case: AuditCase):
    if case.dim == 1:
        return lattice_1d(case.side)
    if case.dim == 2:
        return lattice_2d(case.side)
    if case.dim == 3:
        return lattice_3d(case.side)
    raise ValueError(f"unsupported dimension: {case.dim}")


def ground_state_resource(case: AuditCase) -> dict[str, object]:
    n, adj, parity, _coords = lattice_for_case(case)
    H1 = build_H1(n, adj, parity, mass=case.mass)
    V = build_poisson(n, adj)
    H2 = build_H2_tensor(H1, V, case.G, n)
    evals, evecs = eigh(H2)
    psi = evecs[:, 0]

    Z = build_sublattice_Z(n, parity)
    X = build_pair_hop_X(n)
    full_chsh, _T = chsh_horodecki(psi, Z, X, Z, X, n)
    return {
        "n": n,
        "adj": adj,
        "parity": parity,
        "ground_energy": float(evals[0]),
        "psi": psi,
        "full_chsh": float(full_chsh),
    }


def coords_from_index(index: int, dim: int, side: int) -> tuple[int, ...]:
    coords: list[int] = []
    remaining = index
    for power in range(dim - 1, -1, -1):
        stride = side**power
        coord = remaining // stride
        coords.append(coord)
        remaining %= stride
    return tuple(coords)


def factor_sites(dim: int, side: int, logical_axis: int | None = None) -> SiteFactorization:
    if side % 2 != 0:
        raise ValueError("KS taste factorization requires an even side length")
    if logical_axis is None:
        logical_axis = dim - 1
    if logical_axis < 0 or logical_axis >= dim:
        raise ValueError("logical_axis is outside the spatial dimension")

    n = side**dim
    logical = np.zeros(n, dtype=int)
    env_raw: list[tuple[tuple[int, ...], tuple[int, ...]]] = []

    for site in range(n):
        coords = coords_from_index(site, dim, side)
        cell = tuple(coord // 2 for coord in coords)
        eta = tuple(coord % 2 for coord in coords)
        spectator = tuple(bit for axis, bit in enumerate(eta) if axis != logical_axis)
        logical[site] = eta[logical_axis]
        env_raw.append((cell, spectator))

    env_labels = tuple(dict.fromkeys(env_raw))
    env_index = {label: index for index, label in enumerate(env_labels)}
    env = np.array([env_index[label] for label in env_raw], dtype=int)
    return SiteFactorization(logical=logical, env=env, env_labels=env_labels)


def amplitudes_by_logical_env(
    psi: np.ndarray, n_sites: int, factors: SiteFactorization
) -> np.ndarray:
    n_env = len(factors.env_labels)
    amp = np.zeros((2, n_env, 2, n_env), dtype=complex)
    for site_a in range(n_sites):
        logical_a = factors.logical[site_a]
        env_a = factors.env[site_a]
        for site_b in range(n_sites):
            logical_b = factors.logical[site_b]
            env_b = factors.env[site_b]
            amp[logical_a, env_a, logical_b, env_b] = psi[site_a * n_sites + site_b]
    return amp


def reduced_logical_resource(amp: np.ndarray) -> np.ndarray:
    rho = np.einsum("aebf,cedf->abcd", amp, amp.conj(), optimize=True)
    rho = rho.reshape(4, 4)
    trace = np.trace(rho)
    if abs(trace) <= 1e-15:
        raise ValueError("logical resource has zero trace")
    return rho / trace


def bell_state(z_bit: int, x_bit: int) -> np.ndarray:
    sign = -1.0 if z_bit else 1.0
    state = np.zeros(4, dtype=complex)
    if x_bit == 0:
        state[0] = 1.0 / math.sqrt(2.0)
        state[3] = sign / math.sqrt(2.0)
    else:
        state[1] = 1.0 / math.sqrt(2.0)
        state[2] = sign / math.sqrt(2.0)
    return state


def bell_projector(z_bit: int, x_bit: int) -> np.ndarray:
    state = bell_state(z_bit, x_bit)
    return np.outer(state, state.conj())


def best_bell_overlap(rho: np.ndarray) -> tuple[float, str]:
    overlaps = []
    for z_bit, x_bit in OUTCOME_ORDER:
        state = bell_state(z_bit, x_bit)
        overlap = float(np.real(state.conj() @ rho @ state))
        overlaps.append((overlap, OUTCOME_LABELS[(z_bit, x_bit)]))
    return max(overlaps, key=lambda item: item[0])


def two_qubit_chsh(rho: np.ndarray) -> float:
    paulis = (X2, Y2, Z2)
    T = np.zeros((3, 3), dtype=float)
    for i, op_a in enumerate(paulis):
        for j, op_b in enumerate(paulis):
            T[i, j] = float(np.real(np.trace(rho @ np.kron(op_a, op_b))))
    eigvals = sorted(np.linalg.eigvalsh(T.T @ T), reverse=True)
    return float(2.0 * math.sqrt(max(eigvals[0] + eigvals[1], 0.0)))


def negativity(rho: np.ndarray) -> float:
    partial_transpose_b = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
    eigvals = np.linalg.eigvalsh(partial_transpose_b)
    return float(sum(abs(value) for value in eigvals if value < 0.0))


def normalize(state: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(state)
    if norm <= 1e-15:
        raise ValueError("cannot normalize a zero vector")
    return state / norm


def random_qubit(rng: np.random.Generator) -> np.ndarray:
    return normalize(rng.standard_normal(2) + 1j * rng.standard_normal(2))


def correction_operator(z_bit: int, x_bit: int) -> np.ndarray:
    z_op = Z2 if z_bit else I2
    x_op = X2 if x_bit else I2
    return z_op @ x_op


def standard_teleportation_stats(
    resource_rho: np.ndarray, trials: int, seed: int
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    fidelities: list[float] = []
    trace_errors: list[float] = []

    for _ in range(trials):
        input_state = random_qubit(rng)
        input_rho = np.outer(input_state, input_state.conj())
        total = np.kron(input_rho, resource_rho).reshape(2, 2, 2, 2, 2, 2)
        output = np.zeros((2, 2), dtype=complex)

        for z_bit, x_bit in OUTCOME_ORDER:
            beta = bell_state(z_bit, x_bit).reshape(2, 2)
            branch = np.einsum("ar,arbcsd,cs->bd", beta.conj(), total, beta)
            correction = correction_operator(z_bit, x_bit)
            output += correction @ branch @ correction.conj().T

        trace_errors.append(abs(float(np.real(np.trace(output))) - 1.0))
        fidelity = float(np.real(input_state.conj() @ output @ input_state))
        fidelities.append(fidelity)

    return {
        "mean": float(np.mean(fidelities)),
        "min": float(np.min(fidelities)),
        "max": float(np.max(fidelities)),
        "max_trace_error": float(np.max(trace_errors)),
    }


def verify_teleportation_convention(seed: int) -> dict[str, float]:
    stats = standard_teleportation_stats(bell_projector(0, 0), trials=16, seed=seed)
    if abs(1.0 - stats["min"]) > 1e-12 or stats["max_trace_error"] > 1e-12:
        raise RuntimeError("standard Bell teleportation convention sanity check failed")
    return stats


def postselected_branch_scan(
    amp: np.ndarray,
    env_labels: Iterable[tuple[tuple[int, ...], tuple[int, ...]]],
    probability_floor: float,
) -> dict[str, object]:
    labels = tuple(env_labels)
    best: dict[str, object] = {
        "bell_fidelity": 0.0,
        "bell_label": "none",
        "probability": 0.0,
        "env_a": None,
        "env_b": None,
        "logical_chsh": 0.0,
        "negativity": 0.0,
    }

    for env_a, label_a in enumerate(labels):
        for env_b, label_b in enumerate(labels):
            branch = amp[:, env_a, :, env_b]
            probability = float(np.real(np.vdot(branch, branch)))
            if probability < probability_floor:
                continue
            branch_state = (branch / math.sqrt(probability)).reshape(4)
            rho = np.outer(branch_state, branch_state.conj())
            fidelity, bell_label = best_bell_overlap(rho)
            if fidelity > float(best["bell_fidelity"]):
                best = {
                    "bell_fidelity": fidelity,
                    "bell_label": bell_label,
                    "probability": probability,
                    "env_a": label_a,
                    "env_b": label_b,
                    "logical_chsh": two_qubit_chsh(rho),
                    "negativity": negativity(rho),
                }
    return best


def audit_case(
    case: AuditCase,
    trials: int,
    seed: int,
    high_fidelity_threshold: float,
    probability_floor: float,
) -> dict[str, object]:
    resource = ground_state_resource(case)
    n_sites = int(resource["n"])
    psi = resource["psi"]
    factors = factor_sites(case.dim, case.side)
    amp = amplitudes_by_logical_env(psi, n_sites, factors)
    rho = reduced_logical_resource(amp)

    bell_fidelity, bell_label = best_bell_overlap(rho)
    teleportation = standard_teleportation_stats(rho, trials=trials, seed=seed)
    postselected = postselected_branch_scan(
        amp,
        factors.env_labels,
        probability_floor=probability_floor,
    )

    purity = float(np.real(np.trace(rho @ rho)))
    logical_chsh = two_qubit_chsh(rho)
    neg = negativity(rho)
    extracted = bool(bell_fidelity >= high_fidelity_threshold)
    return {
        "case": case,
        "n_sites": n_sites,
        "n_env": len(factors.env_labels),
        "ground_energy": resource["ground_energy"],
        "full_chsh": resource["full_chsh"],
        "logical_bell_fidelity": bell_fidelity,
        "logical_bell_label": bell_label,
        "logical_chsh": logical_chsh,
        "purity": purity,
        "negativity": neg,
        "teleportation": teleportation,
        "postselected": postselected,
        "deterministic_high_fidelity_resource": extracted,
    }


def print_result(result: dict[str, object], high_fidelity_threshold: float) -> None:
    case = result["case"]
    assert isinstance(case, AuditCase)
    tel = result["teleportation"]
    post = result["postselected"]
    assert isinstance(tel, dict)
    assert isinstance(post, dict)

    print(f"Case: {case.label}")
    print(
        "  lattice/params: "
        f"dim={case.dim} side={case.side} N={result['n_sites']} "
        f"envs/logical_qubit={result['n_env']} mass={case.mass:g} G={case.G:g}"
    )
    print(f"  ground energy: {result['ground_energy']:.12g}")
    print(f"  full-state CHSH |S| from existing lane: {result['full_chsh']:.6f}")
    print(
        "  traced logical taste-qubit resource: "
        f"best Bell overlap={result['logical_bell_fidelity']:.6f} "
        f"({result['logical_bell_label']}), "
        f"CHSH={result['logical_chsh']:.6f}, "
        f"purity={result['purity']:.6f}, "
        f"negativity={result['negativity']:.6f}"
    )
    print(
        "  standard teleportation with traced resource: "
        f"mean fidelity={tel['mean']:.6f}, min={tel['min']:.6f}, "
        f"max={tel['max']:.6f}, max trace error={tel['max_trace_error']:.3e}"
    )
    print(
        "  best fixed-env postselected branch: "
        f"Bell overlap={post['bell_fidelity']:.6f} ({post['bell_label']}), "
        f"probability={post['probability']:.6e}, "
        f"CHSH={post['logical_chsh']:.6f}, negativity={post['negativity']:.6f}"
    )
    print(f"    env A={post['env_a']} env B={post['env_b']}")
    status = "YES" if result["deterministic_high_fidelity_resource"] else "NO"
    print(
        "  deterministic high-fidelity Bell resource "
        f"(threshold {high_fidelity_threshold:.3f}): {status}"
    )
    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=128, help="random teleportation inputs")
    parser.add_argument("--seed", type=int, default=20260425, help="random seed")
    parser.add_argument(
        "--high-fidelity-threshold",
        type=float,
        default=0.90,
        help="Bell-overlap threshold for calling the traced resource high fidelity",
    )
    parser.add_argument(
        "--probability-floor",
        type=float,
        default=1e-12,
        help="ignore postselected branches below this probability",
    )
    parser.add_argument(
        "--case",
        choices=[case.label for case in DEFAULT_CASES],
        action="append",
        help="case label to run; omit to run the default audit set",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.trials <= 0:
        raise ValueError("--trials must be positive")
    if not (0.0 < args.high_fidelity_threshold <= 1.0):
        raise ValueError("--high-fidelity-threshold must be in (0, 1]")
    if args.probability_floor < 0.0:
        raise ValueError("--probability-floor must be nonnegative")

    requested = set(args.case or [])
    cases = [case for case in DEFAULT_CASES if not requested or case.label in requested]

    print("POISSON/CHSH TELEPORTATION RESOURCE AUDIT")
    print("Status: planning / first artifact; quantum state teleportation resource only")
    print("Extraction: trace cells/spectator tastes, keep the last KS taste bit per species")
    sanity = verify_teleportation_convention(args.seed - 1)
    print(
        "Protocol sanity: ideal Phi+ resource "
        f"mean fidelity={sanity['mean']:.16f}, min={sanity['min']:.16f}, "
        f"max trace error={sanity['max_trace_error']:.3e}"
    )
    print()

    results = [
        audit_case(
            case,
            trials=args.trials,
            seed=args.seed + index,
            high_fidelity_threshold=args.high_fidelity_threshold,
            probability_floor=args.probability_floor,
        )
        for index, case in enumerate(cases)
    ]

    for result in results:
        print_result(result, high_fidelity_threshold=args.high_fidelity_threshold)

    poisson_results = [
        result
        for result in results
        if isinstance(result["case"], AuditCase) and result["case"].G != 0.0
    ]
    moved = any(result["deterministic_high_fidelity_resource"] for result in poisson_results)
    print("Conclusion:")
    if moved:
        print(
            "  A traced deterministic high-fidelity Bell resource was found on at least "
            "one Poisson case. This would need independent hardening before promotion."
        )
    else:
        print(
            "  Limitation remains open: the audited Poisson/CHSH ground states do not yet "
            "provide a deterministic high-fidelity encoded Bell pair."
        )
    print(
        "  CHSH violation in the full C^N x C^N state is not by itself a teleportation "
        "resource derivation."
    )
    print("  Postselected branches, when present, are diagnostics only in this artifact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
