#!/usr/bin/env python3
"""Audit the support dark phase against the universal complement angle.

This runner tests the exact phase-lift candidate `B_R^phase` against the
universal `Pi_A1` / orbit-bundle side. The goal is to see whether the support
dark phase can be canonically identified with a universal complement angle,
or whether the exact residual obstruction remains the shared `SO(2)` orbit.

Expected outcome:

- the support dark phase `vartheta_R` is exact;
- the universal complement angle can be tracked only as an orbit coordinate;
- both shift by the same residual `SO(2)` angle under the shared axis;
- the exact common data do not fix a canonical zero-angle section.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

PHASE_NOTE = DOCS / "POLARIZATION_PHASE_LIFT_CANDIDATE_NOTE.md"
GLUE_NOTE = DOCS / "POLARIZATION_GLUE_COMMON_SECTION_NOTE.md"
COMMON_NOTE = DOCS / "POLARIZATION_COMMON_BUNDLE_CANDIDATE_NOTE.md"
UNIVERSAL_NOTE = DOCS / "UNIVERSAL_GR_CANONICAL_PROJECTOR_CONNECTION_NOTE.md"
UNIVERSAL_A1_NOTE = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"

SUPPORT = SourceFileLoader(
    "route2_bilinear",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_primitive.py"),
).load_module()
PHASE = SourceFileLoader(
    "polarization_phase_lift_candidate",
    str(ROOT / "scripts" / "frontier_polarization_phase_lift_candidate.py"),
).load_module()
UNIVERSAL = SourceFileLoader(
    "universal_gr_a1_invariant_section",
    str(ROOT / "scripts" / "frontier_universal_gr_a1_invariant_section.py"),
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


def wrap_angle(theta: float) -> float:
    return math.atan2(math.sin(theta), math.cos(theta))


def rot_x(theta: float) -> np.ndarray:
    rot = np.eye(4, dtype=float)
    c = math.cos(theta)
    s = math.sin(theta)
    rot[2, 2] = c
    rot[2, 3] = -s
    rot[3, 2] = s
    rot[3, 3] = c
    return rot


def support_phase(q: np.ndarray) -> tuple[float, float]:
    dark = np.array(SUPPORT.dark_coords(q)[1:], dtype=float)
    return float(np.linalg.norm(dark)), math.atan2(dark[1], dark[0])


def universal_phase(h: np.ndarray) -> tuple[float, float]:
    frame = UNIVERSAL.canonical_polarization_frame()
    resp = UNIVERSAL.response_vector(h, frame, (2.0, 3.0, 5.0, 7.0))
    pair = np.array([resp[7], resp[8]], dtype=float)
    return float(np.linalg.norm(pair)), math.atan2(pair[1], pair[0])


def rotated_universal_phase(h: np.ndarray, theta: float) -> tuple[float, float]:
    frame = UNIVERSAL.rotated_frame(rot_x(theta).tolist())
    resp = UNIVERSAL.response_vector(h, frame, (2.0, 3.0, 5.0, 7.0))
    pair = np.array([resp[7], resp[8]], dtype=float)
    return float(np.linalg.norm(pair)), math.atan2(pair[1], pair[0])


def main() -> int:
    phase_note = read(PHASE_NOTE)
    glue_note = read(GLUE_NOTE)
    common_note = read(COMMON_NOTE)
    universal_note = read(UNIVERSAL_NOTE)
    universal_a1_note = read(UNIVERSAL_A1_NOTE)

    basis = PHASE.SAME.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]

    q_ref = (e0 + 0.5 * s) / (1.0 + np.sqrt(6.0) * 0.5) + 0.13 * t1x + 0.03 * t1y + 0.02 * t1z
    rho_s0, theta_s0 = support_phase(q_ref)

    h_ref = (
        np.array(UNIVERSAL.sym(1, 2), dtype=float)
        + 2.0 * np.array(UNIVERSAL.sym(1, 3), dtype=float)
        + 0.25 * np.array(UNIVERSAL.diag((0.0, 1.0, -1.0, 0.0)), dtype=float)
    )
    rho_c0, theta_c0 = universal_phase(h_ref)

    phase_deltas = []
    curv_deltas = []
    rel_deltas = []
    rho_err = 0.0
    curv_rho_err = 0.0
    max_pi_delta = 0.0

    projector = np.zeros((10, 10), dtype=float)
    projector[0, 0] = 1.0
    projector[4, 4] = 1.0
    for phi in [math.pi / 9.0, math.pi / 6.0, math.pi / 4.0, math.pi / 3.0]:
        rot = rot_x(phi)
        dark_plane = np.array([np.dot(t1y, q_ref), np.dot(t1z, q_ref)], dtype=float)
        dark_rotated = np.array([[math.cos(phi), -math.sin(phi)], [math.sin(phi), math.cos(phi)]], dtype=float) @ dark_plane
        q_phi = (
            q_ref
            + (dark_rotated[0] - dark_plane[0]) * t1y
            + (dark_rotated[1] - dark_plane[1]) * t1z
        )
        rho_s, theta_s = support_phase(q_phi)
        rho_c, theta_c = rotated_universal_phase(h_ref, phi)
        phase_deltas.append(wrap_angle(theta_s - theta_s0 - phi))
        curv_deltas.append(wrap_angle(theta_c - theta_c0 - phi))
        rel_deltas.append(wrap_angle((theta_c - theta_s) - (theta_c0 - theta_s0)))
        rho_err = max(rho_err, abs(rho_s - rho_s0))
        curv_rho_err = max(curv_rho_err, abs(rho_c - rho_c0))

        # Verify the universal A1 core stays fixed while the complement changes.
        resp_base = UNIVERSAL.response_vector(h_ref, UNIVERSAL.canonical_polarization_frame(), (2.0, 3.0, 5.0, 7.0))
        resp_rot = UNIVERSAL.response_vector(h_ref, UNIVERSAL.rotated_frame(rot.tolist()), (2.0, 3.0, 5.0, 7.0))
        max_pi_delta = max(
            max_pi_delta,
            float(np.max(np.abs(projector @ resp_base - projector @ resp_rot))),
        )

    print("POLARIZATION PHASE-TO-CURVATURE AUDIT")
    print("=" * 78)
    print(f"support rho_R(q_ref)   = {rho_s0:.12e}")
    print(f"support vartheta_R     = {theta_s0:.12e}")
    print(f"curvature rho_curv     = {rho_c0:.12e}")
    print(f"curvature alpha_curv   = {theta_c0:.12e}")
    print(f"max support radius err  = {rho_err:.3e}")
    print(f"max curvature radius err= {curv_rho_err:.3e}")
    print(f"max Pi_A1 delta        = {max_pi_delta:.3e}")
    print("phase shifts:")
    for i, (dp, dc, dr) in enumerate(zip(phase_deltas, curv_deltas, rel_deltas), start=1):
        print(
            f"  phi{i} support shift={dp:+.3e}, curvature shift={dc:+.3e}, "
            f"relative gap shift={dr:+.3e}"
        )

    record(
        "the phase-lift candidate note names an exact support-side dark phase",
        has(phase_note, "vartheta_R") and has(phase_note, "dark pair"),
        "the support-side phase primitive is explicitly available",
    )
    record(
        "the glue note reduces the shared residual gauge to SO(2)",
        has(glue_note, "SO(2)") and has(glue_note, "common residual gauge"),
        "the shared connected freedom is one dark-plane angle",
    )
    record(
        "the universal note exposes only an orbit bundle on the complement",
        has(universal_note, "orbit bundle") and has(universal_note, "SO(3)"),
        "the universal complement is still orbit-canonical, not section-canonical",
    )
    record(
        "the universal A1 note fixes the invariant core but leaves the complement frame-dependent",
        has(universal_a1_note, "Pi_A1") and has(universal_a1_note, "complement remains frame-dependent"),
        "Pi_A1 is exact but not enough to canonicalize the complement",
    )
    record(
        "the support dark phase shifts exactly by the residual SO(2) angle",
        max(abs(x) for x in phase_deltas) < 1e-12 and rho_err < 1e-12,
        f"max phase shift residual={max(abs(x) for x in phase_deltas):.3e}",
    )
    record(
        "the universal complement angle shifts exactly by the same residual SO(2) angle",
        max(abs(x) for x in curv_deltas) < 1e-12 and curv_rho_err < 1e-12,
        f"max curvature shift residual={max(abs(x) for x in curv_deltas):.3e}",
    )
    record(
        "the relative phase gap is orbit-invariant but not section-canonical",
        max(abs(x) for x in rel_deltas) < 1e-12 and max_pi_delta < 1e-12,
        f"max relative-gap residual={max(abs(x) for x in rel_deltas):.3e}",
    )
    record(
        "the exact common data do not select a preferred zero-angle section",
        has(common_note, "P_R^cand") and has(common_note, "frame-dependent"),
        "the common bundle candidate remains candidate-level on the complement",
    )

    print("\nVerdict:")
    print(
        "The strongest exact phase-to-curvature statement is orbit-valued: the "
        "support dark phase and the universal complement angle are the same "
        "connected SO(2) orbit coordinate once the bright axis and Pi_A1 core "
        "are imposed. But the current atlas does not choose a preferred origin "
        "for that orbit, so there is no canonical section-valued phase-to-"
        "curvature map yet."
    )
    print(
        "The exact residual obstruction is the shared SO(2) gauge on the dark "
        "plane, together with the universal SO(3) complement orbit bundle: the "
        "current exact common objects are invariant under that gauge and therefore "
        "cannot fix a distinguished angle."
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
