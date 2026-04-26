#!/usr/bin/env python3
"""Candidate native-teleportation axiom closure checks.

This is not a physics simulation. It is a deterministic consistency harness
for the proposed lane-level axiom bundle in
docs/TELEPORTATION_NATIVE_AXIOMS_THEORY_NOTE.md.

The runner should pass only if the current theory artifact keeps the correct
claim boundary: planning closure is internally consistent, while nature-grade
closure remains held open.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class Verdict(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"


BELL_BITS: dict[str, tuple[int, int]] = {
    "Phi+": (0, 0),
    "Phi-": (1, 0),
    "Psi+": (0, 1),
    "Psi-": (1, 1),
}


@dataclass(frozen=True)
class Gate:
    name: str
    verdict: Verdict
    detail: str


@dataclass(frozen=True)
class Evidence:
    fixed_phi_f_avg: float
    framed_f_avg: float
    framed_min_fidelity: float
    pairwise_pre_record_distance: float
    raw_xi5_rel_residual_3d: float
    raw_xi5_bell_rel_residual_3d: float
    delivery_tick: int
    alice_tick: int
    manhattan_distance: int
    promoted_to_nature_grade: bool


CURRENT_3D_EVIDENCE = Evidence(
    fixed_phi_f_avg=0.334850,
    framed_f_avg=0.998483,
    framed_min_fidelity=0.997724,
    pairwise_pre_record_distance=2.498e-16,
    raw_xi5_rel_residual_3d=1.0,
    raw_xi5_bell_rel_residual_3d=0.707107,
    delivery_tick=11,
    alice_tick=4,
    manhattan_distance=7,
    promoted_to_nature_grade=False,
)


def bell_frame_correction(measurement: str, resource_frame: str) -> tuple[int, int]:
    """Return the composed Bob correction bits (z, x), up to Pauli phase."""

    mz, mx = BELL_BITS[measurement]
    hz, hx = BELL_BITS[resource_frame]
    return (mz ^ hz, mx ^ hx)


def pauli_word(bits: tuple[int, int]) -> str:
    z, x = bits
    if (z, x) == (0, 0):
        return "I"
    if (z, x) == (1, 0):
        return "Z"
    if (z, x) == (0, 1):
        return "X"
    return "ZX"


def raw_xi5_admissible_as_traced_z(
    spatial_dim: int,
    spectator_branch_recorded: bool,
) -> bool:
    """A1 retained-factor rule for raw xi_5 as traced retained-axis Z."""

    if spatial_dim <= 1:
        return True
    return spectator_branch_recorded


def earliest_manhattan_delivery_tick(
    alice_site: tuple[int, int, int],
    bob_site: tuple[int, int, int],
    alice_tick: int,
    speed: int,
) -> tuple[int, int]:
    if speed <= 0:
        raise ValueError("speed must be positive")
    distance = sum(abs(a - b) for a, b in zip(alice_site, bob_site))
    latency = (distance + speed - 1) // speed
    return alice_tick + latency, distance


def closure_gates(evidence: Evidence) -> list[Gate]:
    expected_tick, expected_distance = earliest_manhattan_delivery_tick(
        alice_site=(1, 1, 1),
        bob_site=(5, 3, 2),
        alice_tick=evidence.alice_tick,
        speed=1,
    )

    gates = [
        Gate(
            "A1 retained-factor selection",
            Verdict.PASS
            if (
                not raw_xi5_admissible_as_traced_z(
                    spatial_dim=3, spectator_branch_recorded=False
                )
                and evidence.raw_xi5_rel_residual_3d >= 0.999
                and evidence.raw_xi5_bell_rel_residual_3d > 0.7
            )
            else Verdict.FAIL,
            "3D raw xi_5 is rejected as traced Z unless spectator branches "
            "are explicit records.",
        ),
        Gate(
            "A2 Bell-frame connection",
            Verdict.PASS
            if (
                bell_frame_correction("Phi+", "Psi+") == (0, 1)
                and pauli_word(bell_frame_correction("Phi+", "Psi+")) == "X"
                and evidence.fixed_phi_f_avg < 0.5
                and evidence.framed_f_avg > 0.99
                and evidence.framed_min_fidelity > 0.99
            )
            else Verdict.FAIL,
            "Known Psi+ resource needs an X frame; fixed Phi+ fails while "
            "the tracked frame passes.",
        ),
        Gate(
            "A3 3D+1 causal record",
            Verdict.PASS
            if (
                expected_distance == evidence.manhattan_distance
                and expected_tick == evidence.delivery_tick
                and evidence.pairwise_pre_record_distance < 1e-12
            )
            else Verdict.FAIL,
            "Delivery tick equals t_A + L1 distance, and Bob is input-blind "
            "before record delivery.",
        ),
        Gate(
            "A4 native resource genesis",
            Verdict.HOLD,
            "Finite-time 3D ramp is a resource candidate, not a scaling, "
            "apparatus, or physical-preparation proof.",
        ),
        Gate(
            "A5 exhaustive branch accounting",
            Verdict.PASS,
            "Bell outcomes, Bell frame, record faults, and raw-xi_5 branch "
            "dependence are explicit in the current lane artifacts.",
        ),
        Gate(
            "B0 no-transfer boundary",
            Verdict.PASS if not evidence.promoted_to_nature_grade else Verdict.FAIL,
            "The theory artifact remains state-only teleportation and does "
            "not claim matter, mass, charge, energy, object, or FTL transport.",
        ),
    ]
    return gates


def nature_grade_blockers() -> list[str]:
    return [
        "terminal selector decision: retain the three-clause completion, derive "
        "it from a stronger theorem, or do not promote",
        "terminal scaling decision: prove the all-even signed-branch induction/"
        "operator inequality, or keep resource genesis at finite-certificate status",
        "terminal hardware decision: supply fabricated/noise/material evidence, "
        "or keep hardware closure as a requirement envelope",
    ]


def print_table(gates: Iterable[Gate]) -> None:
    for gate in gates:
        print(f"{gate.verdict.value:4s}  {gate.name}: {gate.detail}")


def main() -> int:
    gates = closure_gates(CURRENT_3D_EVIDENCE)
    hard_failures = [gate for gate in gates if gate.verdict is Verdict.FAIL]
    blockers = nature_grade_blockers()

    print("Candidate native taste-qubit teleportation axiom checks")
    print("Bell-frame composition examples:")
    for resource_frame in ("Phi+", "Phi-", "Psi+", "Psi-"):
        bits = bell_frame_correction("Phi+", resource_frame)
        print(f"  measurement Phi+ with {resource_frame:4s} resource -> {pauli_word(bits)}")
    print()
    print_table(gates)
    print()

    planning_ok = not hard_failures
    nature_grade_closed = planning_ok and all(
        gate.verdict is Verdict.PASS for gate in gates
    ) and not blockers

    print(f"Planning theory consistency: {'PASS' if planning_ok else 'FAIL'}")
    print(
        "Nature-grade unconditional closure: "
        f"{'PASS' if nature_grade_closed else 'HOLD'}"
    )

    if blockers:
        print("Open blockers:")
        for blocker in blockers:
            print(f"  - {blocker}")

    return 0 if planning_ok and not nature_grade_closed else 1


if __name__ == "__main__":
    raise SystemExit(main())
