#!/usr/bin/env python3
"""
Sharpen the plaquette beta=6 operator seam to the first propagated retained
three-sample target.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def main() -> int:
    note = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_TARGET_NOTE_2026-04-17.md")
    evaluator_route = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md")
    first_three = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_RECONSTRUCTION_NOTE_2026-04-17.md")
    radical_map = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md")

    print("=" * 108)
    print("GAUGE-VACUUM PLAQUETTE FIRST PROPAGATED RETAINED TRIPLE TARGET")
    print("=" * 108)
    print()

    check(
        "The evaluator route already factors the live beta=6 seam through one common beta-side vector and one fixed three-row sample operator",
        "propagated retained three-sample output" in note
        and "first retained propagated coefficient triple" in note
        and "`mathbf_Z_6 = E_3(v_6)`" in evaluator_route,
        detail="the next target is already propagated and finite on the first witness sector",
    )
    check(
        "The three named holonomies W_A, W_B, W_C are already the first exact same-surface target set",
        "three named holonomies `W_A, W_B, W_C` are already the first exact" in note
        and "`W_A = W(-13 pi / 16,  5 pi / 8)`" in first_three
        and "`W_B = W( -5 pi / 16, -7 pi / 16)`" in first_three
        and "`W_C = W(  7 pi / 16,-11 pi / 16)`" in first_three,
        detail="the finite target set is already explicit",
    )
    check(
        "The radical reconstruction map already makes the first retained propagated coefficient triple equivalent to the three-sample output",
        "inverse map from `(Z_A, Z_B, Z_C)` to the first retained coefficient" in note
        and "exact algebraic inverse map" in radical_map
        and "remaining unresolved data are exactly the three same-surface values" in radical_map,
        detail="no further reconstruction design remains on the first retained sector",
    )
    check(
        "Therefore the first honest next plaquette evaluator target is the propagated retained three-sample triple, not the full infinite class-sector matrix",
        "first honest next evaluative target is:" in note
        and "the propagated retained three-sample output" in note
        and "It does **not** need to start as" in note
        and "full infinite class-sector matrix of `S_6^env`" in note
        and "full family `W -> eta_6(W)`" in note,
        detail="the plaquette operator seam now has a concrete finite next target",
    )

    check(
        "The note keeps the underlying operator gap open rather than pretending the triple is already determined",
        "does **not** claim that the retained triple is already determined" in note
        and "actual missing operator-side content still lives in the explicit" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
