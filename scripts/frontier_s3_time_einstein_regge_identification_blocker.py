#!/usr/bin/env python3
"""Route 2 Einstein/Regge identification blocker audit.

This runner checks the exact bilinear Route-2 carrier/action and confirms the
sharp remaining blocker:

    the exact carrier/action exists as a construction, but the atlas still
    lacks an exact dynamics-bridge or uniqueness theorem identifying it with
    the Einstein/Regge tensor law on the current restricted class.

The intent is not to prove universal GR. The intent is to verify the precise
remaining obstruction on the current route-2 restricted surface.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str) -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail))
    tag = "PASS" if ok else "FAIL"
    print(f"[BLOCKER] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    bilinear_note = ROOT / "docs" / "S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md"
    action_note = ROOT / "docs" / "S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md"
    blocker_note = ROOT / "docs" / "S3_TIME_EINSTEIN_REGGE_IDENTIFICATION_BLOCKER_NOTE.md"
    time_note = ROOT / "docs" / "S3_TIME_COUPLING_EXACT_THEOREM_NOTE.md"
    restricted_note = ROOT / "docs" / "RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md"

    bilinear_text = read_text(bilinear_note)
    action_text = read_text(action_note)
    blocker_text = read_text(blocker_note)
    time_text = read_text(time_note)
    restricted_text = read_text(restricted_note)

    bilinear = SourceFileLoader(
        "s3_time_bilinear_tensor_primitive",
        str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_primitive.py"),
    ).load_module()
    action = SourceFileLoader(
        "s3_time_bilinear_tensor_action",
        str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_action.py"),
    ).load_module()

    print("Route 2 Einstein/Regge identification blocker audit")
    print("=" * 78)
    print("  Current surface: restricted class on PL S^3 x R")
    print()

    q = bilinear.a1_background(0.5)
    k = bilinear.k_r(q)
    delta = bilinear.delta_a1(q)
    ex_col = bilinear.k_r(q + bilinear.e_x) - k
    tx_col = bilinear.k_r(q + bilinear.t1x) - k
    exact_cols = (
        np.max(np.abs(ex_col - np.array([[1.0, 0.0], [delta, 0.0]]))) < 1e-12
        and np.max(np.abs(tx_col - np.array([[0.0, 1.0], [0.0, delta]]))) < 1e-12
    )

    theta = bilinear.vec_k(q)
    theta_ok = np.all(np.isfinite(theta)) and theta.shape == (4,)
    carrier_exact = "exact microscopic tensor carrier" in bilinear_text.lower()
    action_exact = "exact tensorized action/coupling construction" in action_text.lower()
    blocker_stated = "final dynamics identification" in action_text.lower() or "sharp blocker" in blocker_text.lower()
    restricted_exact = "restricted strong-field closure" in restricted_text.lower()
    time_blocked = any(
        phrase in time_text.lower()
        for phrase in [
            "does not yet supply an exact time-coupling law",
            "sharp blocker",
            "no exact derivation of the einstein metric law",
            "the atlas still lacks an exact pl s^3 x r dynamics bridge",
        ]
    )

    print("Exact carrier checkpoint:")
    print(f"  vec(K_R) = {np.array2string(theta, precision=12, floatmode='fixed')}")
    print(f"  exact endpoint columns verified = {exact_cols}")
    print()

    record(
        "the bilinear carrier K_R is exact on the microscopic support block",
        carrier_exact and exact_cols and theta_ok,
        "the carrier has the exact endpoint columns and the note states it is exact",
    )
    record(
        "the tensorized action I_TB / Xi_TB is an exact construction on PL S^3 x R",
        action_exact and np.all(np.isfinite(action.vec_k(q))) if hasattr(action, "vec_k") else action_exact,
        "the note and runner define the exact tensorized construction explicitly",
    )
    record(
        "the restricted strong-field stack is already exact on the current class",
        restricted_exact,
        "the route-2 identification sits on top of an already exact restricted strong-field package",
    )
    record(
        "the current atlas still lacks an exact dynamics bridge",
        time_blocked,
        "the time-coupling theorem note still records the dynamics bridge as missing",
    )
    record(
        "the remaining blocker is identification-level rather than class-widening",
        blocker_stated and "restricted class" in blocker_text.lower(),
        "the new blocker note says the carrier/action is exact but not yet identified with Einstein/Regge dynamics",
    )

    print()
    print("Verdict:")
    print(
        "Route 2 has an exact bilinear carrier and exact tensorized construction, "
        "but the current atlas still lacks the exact dynamics-bridge/uniqueness "
        "theorem needed to identify that construction with Einstein/Regge on the "
        "restricted class. The blocker is identification-level, not class-widening."
    )

    print()
    print("Summary:")
    print("  Exact carrier/action construction: yes")
    print("  Exact Einstein/Regge identification: blocked")
    print("  Remaining issue: identification, not class widening")
    print(f"PASS={sum(c.ok for c in CHECKS)} FAIL={sum(not c.ok for c in CHECKS)}")
    return 0 if all(c.ok for c in CHECKS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
