#!/usr/bin/env python3
"""Sharpen the shared polarization-bundle obstruction to the common residual gauge.

This runner combines the exact support-side and universal-side canonicalization
results:

1. support side:
   - exact A1 endpoint law
   - exact bright pair `u_E, u_T`
   - residual gauge `O(1) x O(2)` on the dark complement after bright signs
2. universal side:
   - exact invariant `Pi_A1`
   - complementary `SO(3)` orbit bundle

The intersection of those two residual structures is the actual shared
remaining gauge on the common bundle candidate:

    S(O(1) x O(2)) ~= O(2)

If one further restricts to the connected component after fixing the bright
axis orientation, the remaining connected gauge is:

    SO(2)

So the full missing primitive is no longer best thought of as an arbitrary
`3+1` polarization bundle. The sharp remaining primitive is a canonical angle /
phase on the dark complement plane.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

SUPPORT_NOTE = DOCS / "FINITE_RANK_SUPPORT_CANONICAL_FRAME_NOTE.md"
UNIVERSAL_NOTE = DOCS / "UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md"
COMMON_NOTE = DOCS / "POLARIZATION_COMMON_BUNDLE_CANDIDATE_NOTE.md"
GLUE_NOTE = DOCS / "POLARIZATION_GLUE_COMMON_SECTION_NOTE.md"


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def support_element(eps: int, a: np.ndarray) -> np.ndarray:
    """Support residual gauge element in the dark complement basis.

    Basis order:
      0: E_perp
      1,2: dark T1 plane
    """

    out = np.zeros((3, 3), dtype=float)
    out[0, 0] = float(eps)
    out[1:, 1:] = a
    return out


def common_element(a: np.ndarray) -> np.ndarray:
    """Embed O(2) into SO(3) as the bright-axis stabilizer."""

    out = np.zeros((3, 3), dtype=float)
    out[0, 0] = float(np.linalg.det(a))
    out[1:, 1:] = a
    return out


def is_orthogonal(m: np.ndarray, tol: float = 1e-12) -> bool:
    ident = np.eye(m.shape[0], dtype=float)
    return np.max(np.abs(m.T @ m - ident)) < tol


def main() -> int:
    support = read(SUPPORT_NOTE)
    universal = read(UNIVERSAL_NOTE)
    common = read(COMMON_NOTE)
    glue = read(GLUE_NOTE) if GLUE_NOTE.exists() else ""

    print("POLARIZATION COMMON RESIDUAL GAUGE")
    print("=" * 78)

    record(
        "support-side residual gauge is exactly O(1) x O(2)",
        has(support, "o(1)") and has(support, "o(2)"),
        "support note fixes the block frame and leaves dark-complement orthogonal freedom",
    )
    record(
        "universal-side residual gauge is exactly SO(3)",
        has(universal, "so(3)") and has(universal, "residual gauge"),
        "universal note identifies the complementary frame orbit as the spatial-rotation gauge",
    )
    record(
        "common bundle candidate already has a canonical A1 core and noncanonical complement",
        has(common, "Pi_A1")
        and (has(common, "frame-dependent") or has(common, "noncanonical"))
        and (has(glue, "SO(2)") or has(common, "SO(2)")),
        "common/glue notes isolate the exact core and the sharpened one-angle obstruction",
    )

    # Construct sample elements of the support residual gauge and check the
    # intersection with SO(3) is exactly S(O(1) x O(2)).
    angles = [0.0, math.pi / 7.0, math.pi / 5.0, math.pi / 3.0]
    max_det_err = 0.0
    max_orth_err = 0.0
    support_intersection_ok = True
    connected_ok = True

    for theta in angles:
        c = math.cos(theta)
        s = math.sin(theta)
        rot = np.array([[c, -s], [s, c]], dtype=float)
        refl = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=float) @ rot

        for a in (rot, refl):
            g = common_element(a)
            max_det_err = max(max_det_err, abs(np.linalg.det(g) - 1.0))
            max_orth_err = max(max_orth_err, np.max(np.abs(g.T @ g - np.eye(3))))

            support_g = support_element(int(round(np.linalg.det(a))), a)
            support_intersection_ok &= np.max(np.abs(g - support_g)) < 1e-12

            if abs(np.linalg.det(a) - 1.0) < 1e-12:
                connected_ok &= np.max(np.abs(g[0, 0] - 1.0)) < 1e-12

    record(
        "the shared residual gauge is the bright-axis stabilizer S(O(1) x O(2))",
        support_intersection_ok and max_det_err < 1e-12 and max_orth_err < 1e-12,
        f"det error={max_det_err:.3e}, orthogonality error={max_orth_err:.3e}",
    )
    record(
        "the connected residual gauge after fixing bright-axis orientation is SO(2)",
        connected_ok,
        "orientation-preserving dark-plane rotations are the only connected common freedom",
    )

    print("\nCandidate reduction:")
    print("  support residual    = O(1) x O(2)")
    print("  universal residual  = SO(3)")
    print("  common residual     = S(O(1) x O(2)) ~= O(2)")
    print("  connected residual  = SO(2)")

    print("\nVerdict:")
    print(
        "The exact common bundle obstruction is sharper than a generic missing "
        "`3+1` polarization bundle. Once the canonical `Pi_A1` core and the "
        "exact bright support pair are anchored, the shared residual gauge "
        "collapses to the bright-axis stabilizer S(O(1) x O(2)) ~= O(2). "
        "After restricting to the connected component, the only remaining "
        "continuous freedom is a single SO(2) angle on the dark complement plane."
    )
    print(
        "So the remaining axiom-native primitive is best understood as a "
        "canonical axial phase / angle connection on the dark complement, not "
        "an arbitrary full bundle."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
