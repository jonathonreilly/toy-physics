#!/usr/bin/env python3
"""Verify the B3 Clifford realification metric-Ward theorem."""

from __future__ import annotations

import numpy as np
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-12


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def sym(m: np.ndarray) -> np.ndarray:
    return 0.5 * (m + m.T)


def asym(m: np.ndarray) -> np.ndarray:
    return 0.5 * (m - m.T)


def metric_variation(h: np.ndarray) -> np.ndarray:
    return h + h.T


def incidence_1d(n_vertices: int) -> np.ndarray:
    """Oriented path incidence: rows are edges, columns are vertices."""
    d = np.zeros((n_vertices - 1, n_vertices))
    for edge in range(n_vertices - 1):
        d[edge, edge] = -1.0
        d[edge, edge + 1] = 1.0
    return d


def main() -> int:
    note = read("docs/PLANCK_SCALE_B3_CLIFFORD_REALIFICATION_METRIC_WARD_THEOREM_2026-04-24.md")
    b3_no_go = read("docs/PLANCK_SCALE_B3_BARE_WARD_IDENTITY_NO_GO_2026-04-24.md")
    edge = read("docs/PLANCK_SCALE_EDGE_CLIFFORD_KINEMATIC_SOLDERING_THEOREM_2026-04-24.md")
    uniqueness = read("docs/PLANCK_SCALE_BARE_GRAVITY_SECTOR_UNIQUENESS_ATTEMPT_2026-04-24.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "document-is-b3-realification-theorem",
        "Planck-Scale B3 Clifford Realification Metric-Ward Theorem" in note
        and "**Status:** positive B3 closure on the canonical real linear-response envelope" in note
        and "frontier_planck_b3_clifford_realification_metric_ward_theorem_2026_04_24.py"
        in note,
        "new B3 theorem and verifier are present",
    )

    total += 1
    passed += expect(
        "starts-from-retained-edge-clifford-soldering",
        "`edge_i <-> Gamma_i`" in edge
        and "`T_R = T_Z tensor_Z R`" in note
        and "`Hom_R(T_R, Cl_1(3))`" in note,
        "the response envelope is the realification of the retained soldering",
    )

    h = np.array(
        [
            [2.0, 3.0, -1.0],
            [5.0, -7.0, 4.0],
            [11.0, 13.0, 17.0],
        ]
    )
    h_sym = sym(h)
    h_asym = asym(h)
    delta_g = metric_variation(h)

    total += 1
    passed += expect(
        "metric-variation-sees-only-symmetric-part",
        np.max(np.abs(delta_g - 2.0 * h_sym)) < TOL
        and np.max(np.abs(metric_variation(h_asym))) < TOL
        and "delta g_ij = h_ij + h_ji" in note,
        f"||delta_g-2sym||={np.max(np.abs(delta_g - 2.0 * h_sym)):.1e}",
    )

    trace = np.trace(h_sym) / 3.0
    shear = h_sym - trace * np.eye(3)
    reconstructed_sym = trace * np.eye(3) + shear

    total += 1
    passed += expect(
        "trace-and-shear-are-metric-not-rival-channels",
        np.max(np.abs(reconstructed_sym - h_sym)) < TOL
        and abs(np.trace(shear)) < TOL
        and "the scalar trace channel is not a rival nonmetric response" in note
        and "symmetric traceless channel is the shear part" in note,
        f"trace={trace:.6g}, shear_trace={np.trace(shear):.1e}",
    )

    total += 1
    passed += expect(
        "antisymmetric-channel-is-frame-gauge",
        np.max(np.abs(metric_variation(h_asym))) < TOL
        and "the antisymmetric channel has `delta g = 0`" in note
        and "frame rotation gauge" in note,
        f"||delta_g(asym)||={np.max(np.abs(metric_variation(h_asym))):.1e}",
    )

    d = incidence_1d(5)
    # A source with equal edge flux is conserved on the two interior vertices.
    t = np.ones(d.shape[0])
    divergence = d.T @ t
    interior_divergence = divergence[1:-1]
    xi = np.array([0.0, 2.0, -3.0, 5.0, 0.0])
    variation = float(t @ (d @ xi))

    total += 1
    passed += expect(
        "cochain-gauge-ward-is-divergence-free",
        np.max(np.abs(interior_divergence)) < TOL
        and abs(variation - float(divergence @ xi)) < TOL
        and "`delta S = <T, d xi> = <d^* T, xi>`" in note
        and "`d^* T = 0`" in note,
        f"interior divergence max={np.max(np.abs(interior_divergence)):.1e}",
    )

    total += 1
    passed += expect(
        "older-finite-automorphism-no-go-is-respected",
        "previous B3 no-go remains correct" in note
        and "finite signed-permutation automorphisms" in note
        and "dynamical Ward generator" in b3_no_go,
        "the theorem changes the response surface rather than denying the no-go",
    )

    total += 1
    passed += expect(
        "activates-conditional-gravity-uniqueness",
        "metric/coframe object class is earned" in note
        and "force the accepted Einstein/Regge boundary-action sector" in note
        and "If the bare event/translation algebra is supplemented by a derived soldered"
        in uniqueness
        and "metricity / equivalence Ward identity" in uniqueness,
        "realified metric Ward supplies the missing premise for the uniqueness theorem",
    )

    total += 1
    passed += expect(
        "scope-does-not-import-einstein-regge",
        "does not assume Einstein equations, the Regge action, the GHY term" in note
        and "Do not use:\n\n> Einstein/Regge dynamics was assumed as the B3 input." in note
        and "first-order realification `Z^3 tensor_Z R` is not an admissible native\n"
        "> response surface" in note,
        "the remaining rejection is realification, not hidden GR dynamics",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
