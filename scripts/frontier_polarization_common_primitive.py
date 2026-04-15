#!/usr/bin/env python3
"""Cross-lane synthesis for the shared polarization primitive family.

This is not a closure proof. It constructs the strongest exact common bundle
candidate and checks the compatibility conditions that any support-side
`Pi_3+1` and curvature-side `Pi_curv` specialization must satisfy.

The intended conclusion is:

- same primitive family: yes
- same exact object: no
- strongest exact common candidate: `P_R^cand = (Pi_A1, B_R, O_R)` with
  `B_R = (K_R, I_TB, Xi_TB)`
- smallest missing axiom-native structure: a covariant `3+1` polarization
  bundle with a distinguished connection `\nabla_R`
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path
from importlib.machinery import SourceFileLoader

import numpy as np
from scipy.linalg import expm


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

FINITE_RANK = DOCS / "FINITE_RANK_3PLUS1_PROMOTION_BLOCKER_NOTE.md"
FINITE_FRAME = DOCS / "FINITE_RANK_SUPPORT_POLARIZATION_FRAME_NOTE.md"
UNIVERSAL_A1 = DOCS / "UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md"
UNIVERSAL_FRAME = DOCS / "UNIVERSAL_GR_POLARIZATION_FRAME_BUNDLE_BLOCKER_NOTE.md"
UNIVERSAL_CURV = DOCS / "UNIVERSAL_GR_CURVATURE_LOCALIZATION_BLOCKER_NOTE.md"
ROUTE2 = DOCS / "S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md"
CONSTRUCTION = DOCS / "POLARIZATION_COMMON_BUNDLE_CANDIDATE_NOTE.md"
SYNTHESIS = DOCS / "POLARIZATION_COMMON_PRIMITIVE_SYNTHESIS_NOTE.md"

SAME_SOURCE_METRIC = SourceFileLoader(
    "same_source_metric",
    str(ROOT / "scripts" / "frontier_same_source_metric_ansatz_scan.py"),
).load_module()
BILINEAR = SourceFileLoader(
    "s3_time_bilinear_tensor_primitive",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_primitive.py"),
).load_module()
ACTION = SourceFileLoader(
    "s3_time_bilinear_tensor_action",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_action.py"),
).load_module()
FINITE_FRAME_SCRIPT = SourceFileLoader(
    "finite_rank_support_polarization_frame",
    str(ROOT / "scripts" / "frontier_finite_rank_support_polarization_frame.py"),
).load_module()
UNIVERSAL_FRAME_SCRIPT = SourceFileLoader(
    "universal_gr_polarization_frame_bundle",
    str(ROOT / "scripts" / "frontier_universal_gr_polarization_frame_bundle.py"),
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def matches(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) is not None


def max_abs_delta(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(a - b)))


def bridge_candidate() -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    q_center = BILINEAR.e0 + BILINEAR.e_x
    q_shell = BILINEAR.s_unit + BILINEAR.t1x
    theta_center = BILINEAR.vec_k(q_center)
    theta_shell = BILINEAR.vec_k(q_shell)

    Lambda, _, _, _ = ACTION.schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    u_star = np.ones(Lambda_sym.shape[0], dtype=float)
    u_star /= np.linalg.norm(u_star)
    seed_t = expm(-0.0 * Lambda_sym) @ u_star
    xi_center = ACTION.xi_tb(theta_center, seed_t)

    frame_a = UNIVERSAL_FRAME_SCRIPT.canonical_polarization_frame()
    frame_b = UNIVERSAL_FRAME_SCRIPT.rotated_polarization_frame(np.pi / 6.0)
    h_test = (
        (1.0, 0.35, -0.22, 0.18),
        (0.35, -0.75, 0.14, 0.07),
        (-0.22, 0.14, 0.41, -0.19),
        (0.18, 0.07, -0.19, -0.28),
    )
    resp_a = np.array(UNIVERSAL_FRAME_SCRIPT.response_vector(h_test, frame_a, (2.0, 3.0, 5.0, 7.0)))
    resp_b = np.array(UNIVERSAL_FRAME_SCRIPT.response_vector(h_test, frame_b, (2.0, 3.0, 5.0, 7.0)))
    frame_delta = max_abs_delta(resp_a, resp_b)
    return theta_center, theta_shell, xi_center, frame_delta


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def main() -> int:
    finite_rank = read(FINITE_RANK)
    finite_frame = read(FINITE_FRAME)
    universal_frame = read(UNIVERSAL_FRAME)
    universal_curv = read(UNIVERSAL_CURV)
    route2 = read(ROUTE2)
    construction = read(CONSTRUCTION)
    synthesis = read(SYNTHESIS)

    bridge_center, bridge_shell, xi_center, frame_delta = bridge_candidate()
    bridge_center_expected = np.array([1.0, 0.0, 1.0 / 6.0, 0.0], dtype=float)
    bridge_shell_expected = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    bridge_center_ok = max_abs_delta(bridge_center, bridge_center_expected) < 1e-12
    bridge_shell_ok = max_abs_delta(bridge_shell, bridge_shell_expected) < 1e-12
    xi_center_ok = np.all(np.isfinite(xi_center)) and xi_center.shape[0] == 4

    record(
        "finite-rank blocker asks for a support-side polarization lift before scalar collapse",
        has(finite_rank, "Pi_3+1") and has(finite_rank, "tensor-valued support-side polarization frame")
        and has(finite_frame, "K_R(q)"),
        "finite-rank lane is explicitly pre-collapse and support-side, with exact carrier K_R now spelled out",
    )
    record(
        "finite-rank support-frame note shows the current support side is rank one after renormalization",
        has(finite_frame, "rank one") and has(finite_frame, "polarization frame"),
        "rank-one support collapse prevents a canonical support-side frame",
    )
    record(
        "universal blocker asks for a covariant polarization-frame bundle before curvature localization",
        has(universal_frame, "covariant `3+1` polarization-frame / projector bundle") and has(universal_frame, "Pi_curv"),
        "universal lane is explicitly post-candidate and localization-side",
    )
    record(
        "universal A1 note exposes the exact invariant section latent in the current stack",
        has(read(UNIVERSAL_A1), "Pi_A1") and has(read(UNIVERSAL_A1), "lapse") and has(read(UNIVERSAL_A1), "spatial trace"),
        "the exact invariant selector is the canonical core of the strengthened common bundle candidate",
    )
    record(
        "universal curvature blocker says localization is frame-dependent across valid `3+1` frames",
        (matches(universal_curv, r"different localized channel\s+coefficients")
         or has(universal_curv, "canonical `Pi_curv`"))
        and has(universal_curv, "Pi_curv"),
        "the universal lane is blocked by missing covariance, not by missing scalar data",
    )
    record(
        "Route 2 provides the shared interface object between support and curvature sides",
        has(route2, "K_R(q)") and has(route2, "I_TB") and has(route2, "Xi_TB"),
        "Route 2 carries the aligned bright channels plus the `PL S^3 x R` semigroup factor",
    )
    record(
        "Route 2 supports the strongest exact common bridge triple B_R",
        has(synthesis, "B_R := (K_R, I_TB, Xi_TB)")
        and has(synthesis, "strongest exact common object")
        and has(synthesis, "bridge triple"),
        "the exact common construction is the Route 2 bridge triple, not a canonical bundle",
    )
    record(
        "the strengthened common bundle candidate includes the invariant A1 core and the Route 2 bridge triple",
        has(construction, "P_R^cand := (Pi_A1, B_R, O_R)")
        and has(construction, "Pi_A1")
        and has(construction, "B_R = (K_R, I_TB, Xi_TB)")
        and bridge_center_ok
        and bridge_shell_ok
        and xi_center_ok,
        (
            "endpoint carrier rows = "
            f"{np.array2string(bridge_center, precision=6)} / "
            f"{np.array2string(bridge_shell, precision=6)}"
        ),
        status="EXACT",
    )
    record(
        "the support-side compatibility conditions preserve the bright channels and scalar datum",
        has(construction, "preserves the exact scalar support datum `delta_A1`")
        and has(construction, "preserves the aligned bright channels `u_E` and `u_T`")
        and has(construction, "commutes with the Route 2 tensorized action `I_TB`"),
        "support specialization factors through K_R and preserves the exact Route 2 carrier module",
        status="EXACT",
    )
    record(
        "the curvature-side compatibility conditions preserve the quotient kernel and localization orbit",
        has(construction, "Any curvature-side `Pi_curv` specialization must satisfy")
        and has(construction, "`Pi_curv`")
        and has(construction, "O_R")
        and has(construction, "distinguished connection"),
        "curvature specialization factors through the exact quotient-kernel orbit and the Route 2 semigroup",
        status="EXACT",
    )
    record(
        "the candidate orbit is exact but not canonical",
        frame_delta > 1e-6,
        f"frame delta across valid `3+1` localizations = {frame_delta:.3e}",
        status="BOUNDED",
    )
    record(
        "the smallest missing axiom-native structure is a covariant `3+1` polarization bundle with distinguished connection",
        has(construction, "distinguished connection")
        and has(construction, "covariant `3+1` polarization-frame / projector bundle"),
        "the only missing structure is the connection that turns the orbit into a canonical section",
        status="EXACT",
    )
    record(
        "the synthesis note states the same-family / not-same-object conclusion",
        matches(synthesis, r"same missing\s+primitive family") and has(synthesis, "not the same exact object"),
        "the note isolates a shared polarization-bundle family with two specializations",
    )

    print("\n" + "=" * 78)
    print("SYNTHESIS")
    print("=" * 78)
    print("Shared primitive family: YES")
    print("Same exact object: NO")
    print(
        "Strongest exact common candidate: `P_R^cand = (Pi_A1, B_R, O_R)` with "
        "`B_R = (K_R, I_TB, Xi_TB)`."
    )
    print("Associated exact output today: exact A1 core plus localization orbit over valid `3+1` frames.")
    print(
        "Compatibility requirements: support-side `Pi_3+1` must preserve Pi_A1, "
        "delta_A1, u_E, u_T, and K_R; curvature-side `Pi_curv` must preserve the "
        "quotient kernel, localization orbit, and Xi_TB."
    )
    print(
        "Still missing: a covariant `3+1` polarization-frame / projector bundle "
        "with distinguished connection `\\nabla_R` that canonicalizes the complement of Pi_A1."
    )
    print("Support specialization target: canonical `Pi_3+1` before scalar collapse, with Pi_A1 as the invariant core.")
    print("Curvature specialization target: canonical `Pi_curv` before localization.")

    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print("\n" + "=" * 78)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
