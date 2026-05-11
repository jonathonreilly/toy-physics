"""Review runner for the substep-4 positive-ratchet open gate.

The companion note is
docs/STAGGERED_DIRAC_SUBSTEP4_POSITIVE_RATCHET_STRETCH_ATTEMPT_NOTE_2026-05-10.md.

This runner does not audit or promote the substep-4 claim. It verifies the
finite algebra fact used by the narrowed open-gate boundary and checks that
the route/probe bookkeeping table has no blank coverage rows.
"""

from __future__ import annotations

import sys
from typing import Dict, List

import numpy as np


PREMISE_COVERAGE: List[Dict[str, object]] = [
    {
        "premise": "physical Cl(3) local algebra",
        "recorded_context": [
            "framework baseline in the substep-4 target note",
            "used throughout the AC-readout route and BAE probe packets",
        ],
    },
    {
        "premise": "Z^3 spatial substrate",
        "recorded_context": [
            "framework baseline in the substep-4 target note",
            "used throughout the AC-readout route and BAE probe packets",
        ],
    },
    {
        "premise": "reflection positivity and OS reconstruction",
        "recorded_context": [
            "AC-readout route 5 GNS-lift discussion",
            "BAE probe 1 Frobenius/GNS context",
        ],
    },
    {
        "premise": "Reeh-Schlieder cyclicity",
        "recorded_context": [
            "AC-readout route 5 single-sector discussion",
        ],
    },
    {
        "premise": "cluster decomposition and unique vacuum",
        "recorded_context": [
            "AC-readout route 5 single-sector discussion",
        ],
    },
    {
        "premise": "Lieb-Robinson microcausality",
        "recorded_context": [
            "AC-readout route 5 spectrum framing",
            "BAE probe 17 spectrum-preservation context",
        ],
    },
    {
        "premise": "lattice Noether fermion number",
        "recorded_context": [
            "AC-readout route 5 integer-spectrum context",
        ],
    },
    {
        "premise": "single-clock codimension-1 evolution",
        "recorded_context": [
            "AC-readout route 2 single-clock obstruction",
            "AC-readout route 5 spectrum-positivity context",
        ],
    },
    {
        "premise": "Kawamoto-Smit phase form",
        "recorded_context": [
            "AC-readout route 5 commutation with C_3 action",
            "BAE probes 21 and 23",
        ],
    },
    {
        "premise": "hw=1 BZ-corner M_3(C) algebra",
        "recorded_context": [
            "AC-readout route 5 vectors 2 through 7",
        ],
    },
    {
        "premise": "no proper exact quotient on the hw=1 triplet",
        "recorded_context": [
            "AC-readout route 5 vector 2",
        ],
    },
    {
        "premise": "C_3[111] cyclic-axis permutation",
        "recorded_context": [
            "AC-readout route 5 GNS unitary-lift discussion",
            "AC-readout routes 1 through 4 C_3-breaking attempts",
        ],
    },
]


def m3c_basis() -> List[np.ndarray]:
    """Return the standard matrix-unit basis for M_3(C)."""
    basis: List[np.ndarray] = []
    for i in range(3):
        for j in range(3):
            matrix = np.zeros((3, 3), dtype=complex)
            matrix[i, j] = 1.0
            basis.append(matrix)
    return basis


def commutator(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return left @ right - right @ left


def check_trivial_center() -> Dict[str, object]:
    """Verify that the center of M_3(C) is C * I_3."""
    basis = m3c_basis()
    identity = np.eye(3, dtype=complex)
    tolerance = 1e-12

    identity_is_central = all(
        np.linalg.norm(commutator(identity, basis_element)) <= tolerance
        for basis_element in basis
    )

    off_diagonal = basis[1]
    transpose = basis[3]
    off_diagonal_is_not_central = (
        np.linalg.norm(commutator(off_diagonal, transpose)) > tolerance
    )

    images = []
    for candidate in basis:
        flattened_commutators = []
        for basis_element in basis:
            flattened_commutators.extend(
                commutator(candidate, basis_element).flatten()
            )
        images.append(flattened_commutators)

    commutator_matrix = np.array(images)
    rank = int(np.linalg.matrix_rank(commutator_matrix, tol=tolerance))
    center_dimension = 9 - rank

    return {
        "identity_is_central": bool(identity_is_central),
        "off_diagonal_is_not_central": bool(off_diagonal_is_not_central),
        "commutator_rank": rank,
        "center_dimension": int(center_dimension),
        "trivial_center": center_dimension == 1,
    }


def check_bookkeeping_table() -> Dict[str, object]:
    """Check that each named premise has at least one recorded context row."""
    missing = [
        row["premise"]
        for row in PREMISE_COVERAGE
        if not row.get("recorded_context")
    ]
    return {
        "premise_count": len(PREMISE_COVERAGE),
        "missing_context": missing,
        "all_have_context": not missing,
    }


def main() -> int:
    pass_count = 0
    fail_count = 0

    print("=" * 72)
    print("SUBSTEP-4 POSITIVE RATCHET OPEN-GATE RUNNER")
    print("=" * 72)

    center = check_trivial_center()
    print("\n(A) M_3(C) center check")
    print(f"  identity central: {center['identity_is_central']}")
    print(f"  off-diagonal noncentral witness: {center['off_diagonal_is_not_central']}")
    print(f"  commutator-map rank: {center['commutator_rank']} / 9")
    print(f"  computed center dimension: {center['center_dimension']}")

    if center["identity_is_central"]:
        pass_count += 1
        print("  [PASS] identity commutes with every matrix unit")
    else:
        fail_count += 1
        print("  [FAIL] identity failed the centrality check")

    if center["off_diagonal_is_not_central"]:
        pass_count += 1
        print("  [PASS] off-diagonal matrix unit is not central")
    else:
        fail_count += 1
        print("  [FAIL] off-diagonal noncentral witness failed")

    if center["trivial_center"]:
        pass_count += 1
        print("  [PASS] Z(M_3(C)) = C * I_3")
    else:
        fail_count += 1
        print("  [FAIL] center dimension is not 1")

    coverage = check_bookkeeping_table()
    print("\n(B) Recorded route/probe bookkeeping")
    print(f"  premise count: {coverage['premise_count']}")
    print(f"  rows without context: {coverage['missing_context']}")
    if coverage["all_have_context"]:
        pass_count += 1
        print("  [PASS] no blank coverage rows")
    else:
        fail_count += 1
        print("  [FAIL] at least one premise lacks recorded context")

    print("\n" + "=" * 72)
    print(f"TOTAL: PASS={pass_count} FAIL={fail_count}")
    print("=" * 72)
    if fail_count == 0:
        print("VERDICT: supports open_gate boundary only; no theorem promotion")
    else:
        print("VERDICT: runner failed")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
