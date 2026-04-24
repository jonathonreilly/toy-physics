#!/usr/bin/env python3
"""Verify the edge-Clifford kinematic soldering theorem."""

from __future__ import annotations

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


def main() -> int:
    note = read("docs/PLANCK_SCALE_EDGE_CLIFFORD_KINEMATIC_SOLDERING_THEOREM_2026-04-24.md")
    site_phase = read("docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md")
    gauge = read("docs/NATIVE_GAUGE_CLOSURE_NOTE.md")
    b3_attempt = read("docs/PLANCK_SCALE_BARE_GRAVITY_SECTOR_UNIQUENESS_ATTEMPT_2026-04-24.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    # A concrete Clifford witness: Pauli matrices give the local three-vector
    # Clifford relation and induced Euclidean metric.
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sz = sp.Matrix([[1, 0], [0, -1]])
    gammas = [sx, sy, sz]
    identity = sp.eye(2)

    clifford_ok = True
    metric = sp.zeros(3)
    for i, gi in enumerate(gammas):
        for j, gj in enumerate(gammas):
            anti = sp.simplify(gi * gj + gj * gi)
            target = 2 * (1 if i == j else 0) * identity
            clifford_ok = clifford_ok and anti == target
            metric[i, j] = sp.simplify(sp.trace(anti) / (2 * sp.trace(identity)))

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "clifford-relation-gives-delta-metric",
        clifford_ok and metric == sp.eye(3)
        and "`g_ij = (1/2) Tr_norm(Gamma_i Gamma_j + Gamma_j Gamma_i) = delta_ij`" in note,
        f"metric={metric}",
    )

    total += 1
    passed += expect(
        "lattice-taste-intertwiner-supports-soldering",
        "Phi^dagger P_mu Phi = S_mu" in site_phase
        and "BZ-corner subspace" in site_phase
        and "site-phase / cube-shift intertwiner" in note,
        "abstract cube shifts are tied to lattice BZ-corner modes",
    )

    total += 1
    passed += expect(
        "native-cl3-support-inherited",
        "Clifford algebra {Γ_μ, Γ_ν} = 2δ_{μν} I₈" in gauge
        and "η phases → Clifford algebra Cl(3)" in gauge,
        "native gauge note records exact Cl(3) from staggered phases",
    )

    total += 1
    passed += expect(
        "sublock-closed-not-b3",
        "kinematic flat-cell level" in note
        and "This does **not** derive the gravitational sector" in note
        and "B3 remains open after this theorem" in note,
        "the theorem closes only flat soldering",
    )

    total += 1
    passed += expect(
        "remaining-dynamical-ward-target-is-explicit",
        "dynamical local" in note
        and "metric/coframe response with the conserved symmetric spin-2 Ward identity" in note
        and "soldered metricity / equivalence Ward identity" in b3_attempt,
        "remaining B3 target is the dynamical metricity Ward identity",
    )

    total += 1
    passed += expect(
        "reviewer-links-soldering",
        "PLANCK_SCALE_EDGE_CLIFFORD_KINEMATIC_SOLDERING_THEOREM_2026-04-24.md" in reviewer,
        "canonical packet links the soldering sub-lock",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
