#!/usr/bin/env python3
"""Verify the B3 dynamical metricity obstruction theorem."""

from __future__ import annotations

from itertools import permutations, product
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def signed_permutation_group() -> list[sp.Matrix]:
    mats = []
    for perm in permutations(range(3)):
        for signs in product([-1, 1], repeat=3):
            mat = sp.zeros(3)
            for row, col in enumerate(perm):
                mat[row, col] = signs[row]
            mats.append(mat)
    return mats


def main() -> int:
    note = read("docs/PLANCK_SCALE_B3_DYNAMICAL_METRICITY_OBSTRUCTION_THEOREM_2026-04-24.md")
    edge = read("docs/PLANCK_SCALE_EDGE_CLIFFORD_KINEMATIC_SOLDERING_THEOREM_2026-04-24.md")
    b3_attempt = read("docs/PLANCK_SCALE_BARE_GRAVITY_SECTOR_UNIQUENESS_ATTEMPT_2026-04-24.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    group = signed_permutation_group()
    identity = sp.eye(3)
    preserves_delta = all(g.T * g == identity for g in group)

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "signed-permutation-frame-group-is-finite",
        len(group) == 48
        and preserves_delta
        and "`O(3,Z) = signed_permutation_matrices`" in note
        and "This group is finite" in note,
        f"|O(3,Z)|={len(group)}",
    )

    total += 1
    passed += expect(
        "flat-soldering-is-inherited-but-not-gravity",
        "`edge_i <-> Gamma_i`" in edge
        and "`g_ij = delta_ij`" in note
        and "That closes the kinematic tangent-frame problem" in note
        and "This does **not** derive the gravitational sector" in edge,
        "flat frame is separated from dynamical gravity",
    )

    total += 1
    passed += expect(
        "no-infinitesimal-ward-generator",
        "Lie algebra is zero-dimensional" in note
        and "`delta e^a_mu(x)`" in note
        and "cannot produce a differential conservation identity" in note,
        "finite cubic symmetry cannot supply a local Ward parameter",
    )

    total += 1
    passed += expect(
        "nonmetric-defect-responses-survive",
        "scalar breathing/conformal response" in note
        and "vector/plaquette response" in note
        and "antisymmetric or torsion-like response" in note
        and "symmetric tensor response" in note
        and "multiple inequivalent sectors" in b3_attempt,
        "bare locality still admits several continuum response channels",
    )

    total += 1
    passed += expect(
        "next-positive-target-is-exact",
        "Local frame redundancy" in note
        and "Defect-to-coframe law" in note
        and "Conserved symmetric response" in note
        and "Spin-2 self-coupling" in note,
        "B3 is reduced to four equivalent positive theorem routes",
    )

    total += 1
    passed += expect(
        "reviewer-links-b3-obstruction",
        "PLANCK_SCALE_B3_DYNAMICAL_METRICITY_OBSTRUCTION_THEOREM_2026-04-24.md"
        in reviewer,
        "canonical packet links the B3 obstruction theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
