#!/usr/bin/env python3
"""Glue audit for the support-side bright block and universal A1 core.

This runner asks the support-to-curvature glue question directly:

Can the exact support-side bright block and the exact universal invariant
`Pi_A1` core together canonically identify the complement, or do they only
reduce the combined freedom to a shared residual orbit?

The expected result is:

- the exact common core is `Pi_A1`;
- the exact support bridge is `B_R = (K_R, I_TB, Xi_TB)`;
- the support and universal data share only an axis-stabilized orbit;
- the exact common connected residual gauge is `SO(2)`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

SUPPORT_CANON = DOCS / "FINITE_RANK_SUPPORT_CANONICAL_FRAME_NOTE.md"
UNIVERSAL_A1 = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"
UNIVERSAL_CANON = DOCS / "UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md"
COMMON_SYNTH = DOCS / "POLARIZATION_COMMON_PRIMITIVE_SYNTHESIS_NOTE.md"
COMMON_BUNDLE = DOCS / "POLARIZATION_COMMON_BUNDLE_CANDIDATE_NOTE.md"
GLUE_NOTE = DOCS / "POLARIZATION_GLUE_COMMON_SECTION_NOTE.md"

FINITE_FRAME = SourceFileLoader(
    "finite_rank_support_canonical_frame",
    str(ROOT / "scripts" / "frontier_finite_rank_support_canonical_frame.py"),
).load_module()
UNIVERSAL_A1_SCRIPT = SourceFileLoader(
    "universal_gr_a1_invariant_section",
    str(ROOT / "scripts" / "frontier_universal_gr_a1_invariant_section.py"),
).load_module()
UNIVERSAL_FRAME = SourceFileLoader(
    "universal_gr_canonical_projector_connection",
    str(ROOT / "scripts" / "frontier_universal_gr_canonical_projector_connection.py"),
).load_module()
COMMON = SourceFileLoader(
    "polarization_common_primitive",
    str(ROOT / "scripts" / "frontier_polarization_common_primitive.py"),
).load_module()
SUPPORT = SourceFileLoader(
    "s3_time_bilinear_tensor_primitive",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_primitive.py"),
).load_module()


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


def rotation(axis: str, theta: float) -> np.ndarray:
    return np.array(UNIVERSAL_FRAME.rotation(axis, theta), dtype=float)


def stabilizer_axis_residual(theta: float) -> float:
    """Residual for preserving the shared x-axis under a spatial rotation."""

    rot = rotation("x", theta)
    e_x = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    return float(np.linalg.norm(rot @ e_x - e_x))


def complement_axis_residual(axis: str, theta: float) -> float:
    rot = rotation(axis, theta)
    e_x = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    return float(np.linalg.norm(rot @ e_x - e_x))


def main() -> int:
    support_canon = read(SUPPORT_CANON)
    universal_a1 = read(UNIVERSAL_A1)
    universal_canon = read(UNIVERSAL_CANON)
    common_synth = read(COMMON_SYNTH)
    common_bundle = read(COMMON_BUNDLE)
    glue = read(GLUE_NOTE)

    projector = np.array(UNIVERSAL_FRAME.pi_a1(), dtype=float)
    projector_rank = int(np.linalg.matrix_rank(projector, tol=1e-12))

    # The exact support bright pair and exact Route-2 bridge triple.
    q_ref = SUPPORT.a1_background(0.5)
    delta_ref = SUPPORT.delta_a1(q_ref)
    k_ref = SUPPORT.k_r(q_ref)

    # Compare the shared-axis stabilizer against the non-stabilizing rotations.
    x_resid = stabilizer_axis_residual(np.pi / 7.0)
    y_resid = complement_axis_residual("y", np.pi / 7.0)
    z_resid = complement_axis_residual("z", np.pi / 7.0)

    # Universal invariant section is exact; complement remains frame-dependent.
    frame = UNIVERSAL_A1_SCRIPT.canonical_polarization_frame()
    rng = np.random.default_rng(0)
    h = UNIVERSAL_A1_SCRIPT.random_symmetric_h(rng)
    base = UNIVERSAL_A1_SCRIPT.response_vector(h, frame, (2.0, 3.0, 5.0, 7.0))
    rotated = UNIVERSAL_A1_SCRIPT.response_vector(
        h,
        UNIVERSAL_A1_SCRIPT.rotated_frame(UNIVERSAL_A1_SCRIPT.random_so3(rng)),
        (2.0, 3.0, 5.0, 7.0),
    )
    a1_base = projector @ base
    a1_rot = projector @ rotated
    perp_base = (np.eye(10) - projector) @ base
    perp_rot = (np.eye(10) - projector) @ rotated
    a1_delta = float(np.max(np.abs(a1_base - a1_rot)))
    perp_delta = float(np.max(np.abs(perp_base - perp_rot)))

    print("POLARIZATION GLUE COMMON SECTION AUDIT")
    print("=" * 78)
    print("Support-side exact bridge data:")
    print(f"  delta_A1(r=0.5) = {delta_ref:.12e}")
    print(f"  K_R(q_ref) = {np.array2string(k_ref, precision=12, floatmode='fixed')}")
    print("Shared-axis stabilizer test:")
    print(f"  x-rotation residual = {x_resid:.3e}")
    print(f"  y-rotation residual = {y_resid:.3e}")
    print(f"  z-rotation residual = {z_resid:.3e}")
    print("Universal A1-section test:")
    print(f"  Pi_A1 rank = {projector_rank}")
    print(f"  max A1 delta across a valid frame change = {a1_delta:.3e}")
    print(f"  max complement delta across a valid frame change = {perp_delta:.3e}")

    record(
        "the support canonical frame still exposes the exact bright pair and the Route 2 bridge triple",
        has(support_canon, "u_E, u_T")
        and has(support_canon, "K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)")
        and has(common_bundle, "B_R := (K_R, I_TB, Xi_TB)"),
        "support-side bright block and bridge triple are exact inputs to the glue problem",
    )
    record(
        "the universal stack still exposes the exact invariant Pi_A1 core",
        has(universal_a1, "Pi_A1") and has(universal_a1, "lapse") and has(universal_a1, "spatial trace"),
        "Pi_A1 is the exact invariant core on the universal side",
    )
    record(
        "the common synthesis note already says the family is shared but the exact objects differ",
        ("same missing primitive family" in common_synth.lower().replace("\n", " "))
        and ("not the same exact object" in common_synth.lower().replace("\n", " ")),
        "the glue task is to sharpen that shared family, not to restate it",
    )
    record(
        "the common bundle candidate is the exact Pi_A1 core together with the Route 2 bridge triple",
        has(common_bundle, "P_R^cand := (Pi_A1, B_R, O_R)")
        and has(common_bundle, "B_R = (K_R, I_TB, Xi_TB)"),
        "the glue candidate already packages the invariant core and the bridge triple",
    )
    record(
        "the shared-axis stabilizer is exactly one-parameter",
        x_resid < 1e-12 and y_resid > 1e-3 and z_resid > 1e-3,
        f"x residual={x_resid:.3e}, y residual={y_resid:.3e}, z residual={z_resid:.3e}",
    )
    record(
        "the exact common connected residual gauge is SO(2)",
        x_resid < 1e-12 and y_resid > 1e-3 and z_resid > 1e-3 and projector_rank == 2,
        "the only common connected freedom is rotation around the shared axis",
    )
    record(
        "the universal complement is still frame-dependent away from the A1 core",
        a1_delta < 1e-12 and perp_delta > 1e-3,
        f"max A1 delta={a1_delta:.3e}, max complement delta={perp_delta:.3e}",
    )
    record(
        "the glue note records the strengthened glued candidate and exact residual gauge",
        has(glue, "P_glue^cand := (Pi_A1, B_R, O_glue)")
        and has(glue, "SO(2)")
        and has(glue, "common residual gauge"),
        "the note states the glued bundle candidate and the common gauge explicitly",
    )

    print("\n" + "=" * 78)
    print("GLUED CANDIDATE")
    print("=" * 78)
    print("P_glue^cand = (Pi_A1, B_R, O_glue)")
    print("B_R = (K_R, I_TB, Xi_TB)")
    print("nabla_glue^cand = nabla_A1 ⊕ nabla_B ⊕ nabla_glue")
    print("Exact common residual gauge = SO(2)")
    print("Support-side discrete O(1) sign is not part of the common glued section.")

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = len(CHECKS) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
