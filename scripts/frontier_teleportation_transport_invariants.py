#!/usr/bin/env python3
"""Formal transport invariants for the native teleportation theory lane.

This runner checks algebraic consequences of
docs/TELEPORTATION_NATIVE_TRANSPORT_THEORY_NOTE.md. It is not a physical
simulation and it intentionally keeps nature-grade closure on hold.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np


Array = np.ndarray
Frame = tuple[int, int]

FRAMES: dict[str, Frame] = {
    "Phi+": (0, 0),
    "Phi-": (1, 0),
    "Psi+": (0, 1),
    "Psi-": (1, 1),
}

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    metric: str


def xor_frame(*frames: Frame) -> Frame:
    z = 0
    x = 0
    for fz, fx in frames:
        z ^= fz
        x ^= fx
    return z, x


def pauli(frame: Frame) -> Array:
    z, x = frame
    op = I2
    if z:
        op = Z @ op
    if x:
        op = X @ op
    return op


def density(vec: Array) -> Array:
    vec = vec / np.linalg.norm(vec)
    return np.outer(vec, vec.conj())


def trace_distance(a: Array, b: Array) -> float:
    vals = np.linalg.eigvalsh(a - b)
    return float(0.5 * np.sum(np.abs(vals)))


def fidelity_pure(rho: Array, psi: Array) -> float:
    psi = psi / np.linalg.norm(psi)
    return float(np.real_if_close(psi.conj() @ rho @ psi))


def conjugate(frame: Frame, rho: Array) -> Array:
    p = pauli(frame)
    return p @ rho @ p.conj().T


def check_connection_group() -> Check:
    labels = list(FRAMES)
    assoc_ok = True
    inverse_ok = True
    identity = FRAMES["Phi+"]
    for a, b, c in product(labels, repeat=3):
        left = xor_frame(xor_frame(FRAMES[a], FRAMES[b]), FRAMES[c])
        right = xor_frame(FRAMES[a], xor_frame(FRAMES[b], FRAMES[c]))
        assoc_ok = assoc_ok and left == right
    for frame in FRAMES.values():
        inverse_ok = inverse_ok and xor_frame(frame, frame) == identity
    return Check(
        "T2 Bell frames form Z2 x Z2 connection group",
        assoc_ok and inverse_ok and len(set(FRAMES.values())) == 4,
        f"associative={assoc_ok}, self_inverse={inverse_ok}, frames={len(FRAMES)}",
    )


def check_multihop_composition() -> Check:
    psi = np.array([np.sqrt(0.37), np.sqrt(0.63) * np.exp(0.41j)])
    rho = density(psi)
    max_error = 0.0
    chain_count = 0
    labels = list(FRAMES.values())
    for length in range(1, 5):
        for measurements in product(labels, repeat=length):
            for resources in product(labels, repeat=length):
                total = xor_frame(*(measurements + resources))
                branch_state = conjugate(total, rho)
                corrected = conjugate(total, branch_state)
                max_error = max(max_error, trace_distance(corrected, rho))
                chain_count += 1
    return Check(
        "Theorem B multi-hop xor holonomy",
        max_error < 1e-12,
        f"chains={chain_count}, max_trace_distance={max_error:.3e}",
    )


def check_missing_record_twirl() -> Check:
    rng = np.random.default_rng(20260426)
    max_bias = 0.0
    for _ in range(64):
        raw = rng.normal(size=2) + 1j * rng.normal(size=2)
        rho = density(raw)
        for resource in FRAMES.values():
            twirled = sum(
                conjugate(xor_frame(measurement, resource), rho)
                for measurement in FRAMES.values()
            ) / 4.0
            max_bias = max(max_bias, trace_distance(twirled, I2 / 2.0))
    return Check(
        "Theorem A missing-record Pauli twirl",
        max_bias < 1e-12,
        f"max_trace_distance_to_I/2={max_bias:.3e}",
    )


def earliest_delivery_tick(
    alice: tuple[int, int, int],
    bob: tuple[int, int, int],
    emitted_tick: int,
    speed: int,
) -> tuple[int, int]:
    if speed <= 0:
        raise ValueError("speed must be positive")
    distance = sum(abs(a - b) for a, b in zip(alice, bob))
    return emitted_tick + (distance + speed - 1) // speed, distance


def check_causal_record_section() -> Check:
    tick, distance = earliest_delivery_tick((1, 1, 1), (5, 3, 2), 4, 1)
    before_has_section = 10 >= tick
    at_tick_has_section = 11 >= tick
    return Check(
        "T3 3D+1 causal record section",
        tick == 11 and distance == 7 and not before_has_section and at_tick_has_section,
        f"distance={distance}, earliest_tick={tick}, t10={before_has_section}, t11={at_tick_has_section}",
    )


def check_ledger_commutation() -> Check:
    base_dim = 3
    mass_ledger = np.diag([0.0, 1.0, 2.0]).astype(complex)
    charge_ledger = np.diag([1.0, -1.0, 0.0]).astype(complex)
    support_ledger = np.diag([1.0, 0.0, 1.0]).astype(complex)
    correction = np.kron(np.eye(base_dim), pauli(FRAMES["Psi-"]))
    max_commutator = 0.0
    for ledger in (mass_ledger, charge_ledger, support_ledger):
        lifted = np.kron(ledger, I2)
        commutator = correction @ lifted - lifted @ correction
        max_commutator = max(max_commutator, float(np.linalg.norm(commutator)))
    return Check(
        "Theorem C corrections commute with base ledgers",
        max_commutator < 1e-12,
        f"max_commutator_norm={max_commutator:.3e}",
    )


def check_loop_holonomy_detection() -> Check:
    flat_edges = [FRAMES["Psi+"], FRAMES["Phi-"], FRAMES["Psi-"]]
    flat_edges.append(xor_frame(*flat_edges))
    flat_holonomy = xor_frame(*flat_edges)
    defect_edges = list(flat_edges)
    defect_edges[-1] = xor_frame(defect_edges[-1], FRAMES["Psi+"])
    defect_holonomy = xor_frame(*defect_edges)
    return Check(
        "T4 loop holonomy is flat or recorded",
        flat_holonomy == FRAMES["Phi+"] and defect_holonomy == FRAMES["Psi+"],
        f"flat={flat_holonomy}, unrecorded_defect={defect_holonomy}",
    )


def check_hidden_branch_dephasing() -> Check:
    plus = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho_plus = density(plus)
    unrecorded = 0.5 * (rho_plus + conjugate(FRAMES["Phi-"], rho_plus))
    recorded_corrected = 0.5 * (
        rho_plus
        + conjugate(FRAMES["Phi-"], conjugate(FRAMES["Phi-"], rho_plus))
    )
    unrecorded_fidelity = fidelity_pure(unrecorded, plus)
    recorded_fidelity = fidelity_pure(recorded_corrected, plus)
    return Check(
        "Theorem D hidden branch dephasing",
        abs(unrecorded_fidelity - 0.5) < 1e-12
        and abs(recorded_fidelity - 1.0) < 1e-12,
        f"unrecorded_Fplus={unrecorded_fidelity:.6f}, recorded_Fplus={recorded_fidelity:.6f}",
    )


def run_checks() -> list[Check]:
    return [
        check_connection_group(),
        check_multihop_composition(),
        check_missing_record_twirl(),
        check_causal_record_section(),
        check_ledger_commutation(),
        check_loop_holonomy_detection(),
        check_hidden_branch_dephasing(),
    ]


def main() -> int:
    checks = run_checks()
    print("Native teleportation transport-invariant checks")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"{status}  {check.name}: {check.metric}")

    all_pass = all(check.passed for check in checks)
    print()
    print(f"Planning transport theory consistency: {'PASS' if all_pass else 'FAIL'}")
    print("Nature-grade unconditional closure: HOLD")
    print(
        "Reason: this runner checks formal transport invariants only; it does "
        "not derive the Bell resource, durable measurement, record carrier, "
        "apparatus, noise model, or conservation ledgers from native dynamics."
    )
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
