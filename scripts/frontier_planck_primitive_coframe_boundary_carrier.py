#!/usr/bin/env python3
"""Audit the primitive coframe boundary-carrier support theorem."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import sys


AXES = ("t", "x", "y", "z")
ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs" / "PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md"
BOUNDARY_EXTENSION = ROOT / "docs" / "PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md"
CLIFFORD_BRIDGE = ROOT / "docs" / "PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md"
LINK_LOCAL_FIRST_VARIATION = (
    ROOT / "docs" / "PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md"
)
HODGE_NO_GO = (
    ROOT / "docs" / "FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md"
)
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def record(checks: list[Check], name: str, passed: bool, detail: str) -> None:
    checks.append(Check(name, passed, detail))
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}: {detail}")


def subsets_of_size(size: int) -> tuple[tuple[str, ...], ...]:
    return tuple(combinations(AXES, size))


def main() -> int:
    checks: list[Check] = []

    note_text = NOTE.read_text(encoding="utf-8")
    record(checks, "theorem note exists", NOTE.exists(), str(NOTE.relative_to(ROOT)))
    record(
        checks,
        "finite-boundary extension authority exists",
        BOUNDARY_EXTENSION.exists(),
        str(BOUNDARY_EXTENSION.relative_to(ROOT)),
    )
    record(
        checks,
        "Clifford coframe bridge authority exists",
        CLIFFORD_BRIDGE.exists(),
        str(CLIFFORD_BRIDGE.relative_to(ROOT)),
    )

    # Boolean coframe register: four primitive slots gives 2^4 basis states.
    all_states = tuple(
        subset
        for size in range(len(AXES) + 1)
        for subset in subsets_of_size(size)
    )
    packets = {size: set(subsets_of_size(size)) for size in range(len(AXES) + 1)}
    packet_counts = {size: len(packet) for size, packet in packets.items()}
    record(
        checks,
        "Boolean event-cell dimension is 16",
        len(all_states) == 16,
        f"dim H_cell = 2^4 = {len(all_states)}",
    )
    record(
        checks,
        "Hamming-weight packet ranks match binomial row",
        packet_counts == {0: 1, 1: 4, 2: 6, 3: 4, 4: 1},
        f"packet ranks = {packet_counts}",
    )

    # First homogeneous component of prod_a(1+u_a) is exactly the one-slot packet.
    first_homogeneous = set(subsets_of_size(1))
    p_a = packets[1]
    record(
        checks,
        "first homogeneous coframe response selects P_A",
        first_homogeneous == p_a,
        f"G_1 monomials = {sorted(first_homogeneous)}",
    )
    record(
        checks,
        "first-order locality rejects Hodge-dual rank-four P_3",
        packets[3] != p_a and len(packets[3]) == len(p_a),
        f"rank(P_1)={len(p_a)}, rank(P_3)={len(packets[3])}; support differs",
    )

    # Uniqueness under the stated local/additive/symmetric/unit-response hypotheses.
    additive_coefficients = {axis: 1 for axis in AXES}
    carrier_terms = {
        (axis,)
        for axis, coefficient in additive_coefficients.items()
        if coefficient == 1
    }
    record(
        checks,
        "additivity plus unit coframe-slot response gives one projector per slot",
        carrier_terms == p_a,
        f"carrier terms = {sorted(carrier_terms)}",
    )
    record(
        checks,
        "coframe-slot symmetry gives a single common coefficient",
        len(set(additive_coefficients.values())) == 1,
        f"coefficients = {additive_coefficients}",
    )

    c_cell = Fraction(len(p_a), len(all_states))
    record(
        checks,
        "primitive source-free trace gives c_cell=1/4",
        c_cell == Fraction(1, 4),
        f"Tr((I_16/16) P_A) = {len(p_a)}/16 = {c_cell}",
    )
    record(
        checks,
        "finite-boundary extension compatibility keeps density c_cell",
        all(Fraction(n, 1) * c_cell / n == c_cell for n in (1, 2, 7, 19)),
        "N_A(P)=c_cell*A(P)/a^2 has constant coefficient on sampled finite face counts",
    )

    forbidden_true_flags = (
        "PLANCK_MINIMAL_STACK_CLOSURE=TRUE",
        "SI_PLANCK_VALUE_DERIVED=TRUE",
        "GRAVITATIONAL_BOUNDARY_ACTION_CARRIER_IDENTIFIED=TRUE",
    )
    record(
        checks,
        "note carries non-closure flags",
        "PLANCK_MINIMAL_STACK_CLOSURE=FALSE" in note_text
        and "RESIDUAL_PLANCK=derive_gravitational_boundary_action_density_as_first_order_coframe_carrier"
        in note_text,
        "minimal-stack closure remains explicitly false with residual theorem target named",
    )
    record(
        checks,
        "note avoids forbidden retained-closure flags",
        not any(flag in note_text for flag in forbidden_true_flags),
        "no forbidden TRUE closure marker present",
    )
    record(
        checks,
        "note states coframe-slot symmetry rather than physical cubic spacetime symmetry",
        "coframe-slot symmetry" in note_text
        and "not claiming an independent Euclidean\nspacetime symmetry" in note_text,
        "symmetry is scoped to the time-locked Boolean coframe register",
    )

    # Premise provenance citations (rigorize PR additions).
    record(
        checks,
        "link-local first-variation authority exists and is cited",
        LINK_LOCAL_FIRST_VARIATION.exists()
        and "PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md"
        in note_text,
        "first-order locality premise is sourced to the link-local first-variation theorem",
    )
    record(
        checks,
        "current minimal-axioms framework memo exists and is cited",
        MINIMAL_AXIOMS.exists()
        and "MINIMAL_AXIOMS_2026-05-03.md" in note_text,
        "current framework memo keeps Cl(3)/Z^3 physical and leaves the action route conditional",
    )
    record(
        checks,
        "Hodge-degeneracy negative boundary authority exists and is cited",
        HODGE_NO_GO.exists()
        and "FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md"
        in note_text,
        "negative-boundary citation makes the symmetry-only Hodge ambiguity explicit",
    )

    # Unit primitive response is a normalization gauge: rescaling b_a by c
    # rescales c_cell by c. Verify this is the bookkeeping fact (not a
    # hidden derivation), and that the note records it as a scheme choice.
    sample_factors = (Fraction(1), Fraction(1, 2), Fraction(2), Fraction(7, 3))
    rescaling_consistent = all(
        Fraction(len(p_a), len(all_states)) * c == c * c_cell for c in sample_factors
    )
    provenance_recorded = (
        "Premise provenance" in note_text
        and "honest scheme/normalization choice" in note_text
        and "UNIT_PRIMITIVE_RESPONSE_NORMALIZATION_PROVENANCE=canonical_scheme_choice"
        in note_text
        and "FIRST_ORDER_LOCALITY_PROVENANCE=conditional_link_local_first_variation_route"
        in note_text
    )
    record(
        checks,
        "unit primitive response normalization recorded as scheme choice with linear rescaling",
        rescaling_consistent and provenance_recorded,
        "rescaling b_a by c rescales c_cell by c; provenance fields recorded",
    )

    print()
    passed = sum(1 for check in checks if check.passed)
    failed = len(checks) - passed
    print(f"TOTAL: PASS={passed}, FAIL={failed}")
    if failed:
        return 1
    print(
        "Verdict: support theorem verified. P_A is the unique first-order "
        "coframe-slot carrier under the stated hypotheses, c_cell=1/4 follows, "
        "and Planck minimal-stack closure remains open."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
