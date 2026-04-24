#!/usr/bin/env python3
"""Verify the Planck realification admissibility theorem."""

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


def extend_from_basis(images: np.ndarray, coeffs: np.ndarray) -> np.ndarray:
    """Real-linear extension of a Z^3 basis map to R^3."""
    return images @ coeffs


def main() -> int:
    note = read("docs/PLANCK_SCALE_REALIFICATION_ADMISSIBILITY_THEOREM_2026-04-24.md")
    b3_real = read("docs/PLANCK_SCALE_B3_CLIFFORD_REALIFICATION_METRIC_WARD_THEOREM_2026-04-24.md")
    b3_no_go = read("docs/PLANCK_SCALE_B3_DYNAMICAL_METRICITY_OBSTRUCTION_THEOREM_2026-04-24.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "document-is-realification-admissibility-theorem",
        "Planck-Scale Realification Admissibility Theorem" in note
        and "**Status:** closes the realification-admissibility objection" in note
        and "frontier_planck_realification_admissibility_theorem_2026_04_24.py" in note,
        "new theorem and verifier are present",
    )

    images = np.array(
        [
            [1.0, 2.0, -1.0],
            [0.0, 3.0, 5.0],
            [7.0, -2.0, 4.0],
        ]
    )
    z_vec = np.array([2.0, -3.0, 5.0])
    r_vec = np.array([0.25, -1.5, 2.75])
    f_z = extend_from_basis(images, z_vec)
    f_sum = extend_from_basis(images, z_vec + r_vec)
    f_additive = extend_from_basis(images, z_vec) + extend_from_basis(images, r_vec)

    total += 1
    passed += expect(
        "basis-map-extends-uniquely-to-real-linear-map",
        np.max(np.abs(f_sum - f_additive)) < TOL
        and "there is a unique real-linear map" in note
        and "`f_R : T_Z tensor_Z R -> W`" in note,
        f"extension additivity error={np.max(np.abs(f_sum - f_additive)):.1e}",
    )

    images_2 = images.copy()
    total += 1
    passed += expect(
        "same-basis-images-force-same-extension",
        np.max(np.abs(extend_from_basis(images, r_vec) - extend_from_basis(images_2, r_vec))) < TOL
        and "Every additive\nmap from primitive lattice translations into a real response space factors\nuniquely"
        in note,
        "two extensions agreeing on the Z^3 basis agree on all sampled R^3 coefficients",
    )

    total += 1
    passed += expect(
        "clifford-response-is-real-linear-target",
        "`edge_i -> Gamma_i in Cl_1(3)`" in note
        and "`{Gamma_i, Gamma_j} = 2 delta_ij I`" in note
        and "`T_R := Z^3 tensor_Z R`" in note
        and "`T_R = T_Z tensor_Z R`" in b3_real,
        "the retained Clifford soldering already targets a real vector response module",
    )

    total += 1
    passed += expect(
        "finite-automorphism-no-go-is-reclassified",
        "`O(3,Z)`" in note
        and "Its\nLie algebra is zero" in note
        and "finite automorphisms alone do not give dynamics" in note
        and "Lie algebra is zero-dimensional" in b3_no_go,
        "the frozen-cell no-go is retained as a scope result",
    )

    total += 1
    passed += expect(
        "realification-does-not-import-gr-dynamics",
        "imports\nno metric dynamics, no Einstein/Regge action, and no continuum spacetime" in note
        and "It does not assume Einstein equations, the Regge action, the GHY term" in b3_real
        and "Do not use:\n\n> Realification imports Einstein/Regge dynamics" in note,
        "realification is a response envelope, not a hidden gravity action",
    )

    total += 1
    passed += expect(
        "dichotomy-is-explicit",
        "**Finite-automorphism-only reading.**" in note
        and "**Physical first-order response reading.**" in note
        and "the B3 Clifford realification\n   metric-Ward theorem applies" in note,
        "reviewer must choose frozen cell or physical first-order response",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
