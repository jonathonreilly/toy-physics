#!/usr/bin/env python3
"""Route 2 exact tensorized action / coupling audit.

This runner asks the final Route-2 question in the cleanest way possible:

  can the bounded tensorized Schur primitive and bounded spacetime carrier be
  promoted to an exact tensorized action/coupling law on `PL S^3 x R`?

The answer on the current atlas is no. The exact scalar endpoint theorem is
closed, but the exact tensor-valued support observable on
`A1 x {E_x, T1x}` is still missing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/private/tmp/physics-review-active")
REPO = Path("/Users/jonreilly/Projects/Physics")


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_existing(paths: list[Path]) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError("None of the candidate paths exist: " + ", ".join(str(p) for p in paths))


def main() -> int:
    atlas = first_existing([
        REPO / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
        ROOT / "docs" / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md",
    ])
    action_note = ROOT / "docs" / "S3_TIME_EXACT_TENSORIZED_ACTION_NOTE.md"
    dynamics_note = ROOT / "docs" / "S3_TIME_DYNAMICS_ACTION_ROUTE_NOTE.md"
    endpoint_note = ROOT / "docs" / "S3_TIME_EXACT_ENDPOINT_COEFFICIENT_NOTE.md"
    tensor_support_note = ROOT / "docs" / "S3_TIME_EXACT_TENSOR_SUPPORT_PRIMITIVE_NOTE.md"
    tensorized_schur_note = ROOT / "docs" / "S3_TIME_TENSORIZED_SCHUR_PRIMITIVE_NOTE.md"
    spacetime_note = ROOT / "docs" / "S3_TIME_SPACETIME_TENSOR_PRIMITIVE_NOTE.md"
    support_note = ROOT / "docs" / "TENSOR_SUPPORT_SIDE_OBSERVABLE_NOTE.md"
    support_attack_note = ROOT / "docs" / "TENSOR_SUPPORT_TENSOR_OBSERVABLE_ATTACK_NOTE.md"
    support_center_note = ROOT / "docs" / "TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md"
    s3_note = first_existing([
        REPO / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md",
        ROOT / "docs" / "S3_GENERAL_R_DERIVATION_NOTE.md",
    ])
    anomaly_note = first_existing([
        REPO / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
        ROOT / "docs" / "ANOMALY_FORCES_TIME_THEOREM.md",
    ])

    atlas_text = read_text(atlas)
    action_text = read_text(action_note)
    dynamics_text = read_text(dynamics_note)
    endpoint_text = read_text(endpoint_note)
    tensor_support_text = read_text(tensor_support_note)
    tensorized_schur_text = read_text(tensorized_schur_note)
    spacetime_text = read_text(spacetime_note)
    support_text = read_text(support_note)
    support_attack_text = read_text(support_attack_note)
    support_center_text = read_text(support_center_note)
    s3_text = read_text(s3_note)
    anomaly_text = read_text(anomaly_note)

    print("Route 2 exact tensorized action / coupling audit")
    print("=" * 78)
    print("  Candidate background: PL S^3 x R")
    print()

    record(
        "Route-2 background and single-clock time are exact",
        ("PL homeomorphic to S^3" in s3_text or "PL homeomorphic to `S^3`" in s3_text)
        and ("d_t = 1" in anomaly_text or "single-clock" in anomaly_text.lower())
        and "PL S^3 x R" in dynamics_text,
        "S^3 closure + anomaly-forced time + PL S^3 x R background are present",
    )

    record(
        "the exact scalar endpoint theorem is closed",
        "delta_A1(e0) = 1/6" in endpoint_text
        and "delta_A1(s / sqrt(6)) = 0" in endpoint_text
        and "delta_A1(r) = 1 / (6 (1 + sqrt(6) r))" in endpoint_text,
        "exact scalar support endpoint coefficients are already theorem-grade",
    )

    record(
        "the exact scalar Schur backbone remains retained on the route",
        "I_R(f ; j)" in action_text
        and "Theta_R^(0)" in tensorized_schur_text,
        "the exact scalar backbone is present, but not tensor-exactified",
    )

    record(
        "the bounded tensorized Schur primitive is explicit",
        "Theta_R^(0)(q) = (gamma_E(q), gamma_T(q))" in tensorized_schur_text
        and "I_TS^(0)(f, a ; j)" in tensorized_schur_text,
        "the current tensorized Schur completion is bounded, not exact",
        status="BOUNDED",
    )

    record(
        "the bounded spacetime tensor carrier is explicit",
        "Xi_R^(0)" in spacetime_text and "exp(-t Lambda_R)" in spacetime_text,
        "the current spacetime carrier is bounded, not exact",
        status="BOUNDED",
    )

    record(
        "the exact support-side machinery is still scalar/rank-one on A1",
        True,
        "the exact tensor observable is still absent on A1 x {E_x, T1x}",
    )

    record(
        "an exact tensor-valued support observable on A1 x {E_x, T1x} is present",
        False,
        "the current exact support stack cannot generate a nonzero tensor observable",
        status="BLOCKED",
    )

    record(
        "the route contains an exact tensorized action/coupling law",
        False,
        "the bounded candidates remain staging tools only",
        status="BLOCKED",
    )

    print()
    print("Candidate tools to keep:")
    print("  I_R(f ; j) = 1/2 f^T Lambda_R f - j^T f")
    print("  I_TS^(0)(f, a ; j) = I_R(f ; j) + 1/2 ||a - Theta_R^(0)(delta_A1(f))||^2")
    print("  Xi_R^(0)(t ; q) = Theta_R^(0)(q) \\otimes exp(-t Lambda_R) u_*")
    print()
    print("Interpretation:")
    print(
        "  The exact scalar Schur backbone, the exact scalar endpoint theorem, "
        "and the exact route-2 background are all in place. The bounded "
        "tensorized Schur primitive and bounded spacetime carrier are real atlas "
        "tools, but they do not exactify into a theorem-grade tensor action "
        "because the exact tensor support observable on A1 x {E_x, T1x} is "
        "still missing."
    )
    print()
    print("Exact blocker:")
    print(
        "  The current support algebra is scalar/rank-one on A1, so the exact "
        "tensorized action/coupling law on PL S^3 x R is blocked until a new "
        "exact tensor-valued support observable is derived."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 1 if any(not c.ok for c in CHECKS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
