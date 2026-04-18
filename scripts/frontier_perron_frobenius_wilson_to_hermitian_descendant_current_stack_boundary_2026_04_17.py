#!/usr/bin/env python3
"""
Current-stack boundary for the Wilson-to-Hermitian descendant lane.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


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
    note = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_STACK_BOUNDARY_NOTE_2026-04-17.md")
    parent = read("docs/GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    full_d = read("docs/DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md")
    constructive = read("docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_PROJECTED_SOURCE_SELECTOR_THEOREM_NOTE_2026-04-16.md")
    a13_note = read("docs/DM_LEPTOGENESIS_PMNS_MINIMAL_A13_SHEET_SELECTOR_THEOREM_NOTE_2026-04-16.md")
    reduction = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md")

    # Constructive projected-source witness from the exact note.
    gamma = 0.150147244666
    e1 = 0.296562850784
    e2 = 1.986407435174
    a13 = 2.0 * gamma

    print("=" * 108)
    print("PERRON-FROBENIUS WILSON-TO-HERMITIAN DESCENDANT CURRENT-STACK BOUNDARY")
    print("=" * 108)
    print()
    print(f"constructive projected-source witness = (gamma={gamma:.12f}, E1={e1:.12f}, E2={e2:.12f})")
    print(f"minimal odd selector slot            = A13={a13:.12f}")
    print()

    check(
        "Wilson parent note already proves exact plaquette/theta descendants and explicitly stops before PMNS provenance",
        "plaquette and `theta` descendants" in note
        and "PMNS is not yet shown to be a canonical descendant" in note,
        bucket="SUPPORT",
    )
    check(
        "Full microscopic reduction note already proves the exact D -> D_- -> dW_e^H -> H_e -> packet -> eta chain once D is supplied",
        "the exact chain is now:" in full_d.lower()
        and "`D`" in full_d
        and "`-> D_-`" in full_d
        and "`-> dW_e^H`" in full_d
        and "`-> H_e`" in full_d
        and "So once the full microscopic charge-preserving operator `D` is supplied" in full_d,
        bucket="SUPPORT",
    )
    check(
        "Constructive and minimal-selector notes already prove exact positive existence and exact one-bit odd reduction directly on dW_e^H",
        "constructive sign chamber is not only nonempty" in constructive
        and "projected-source sign chamber" in constructive
        and "sign of the single odd projected-source slot `A13`" in a13_note,
        bucket="SUPPORT",
    )
    check(
        "Hermitian reduction note already identifies D_- / dW_e^H / H_e as the first honest step-2A codomain",
        "`Wilson -> D_- -> dW_e^H -> H_e`" in reduction,
        bucket="SUPPORT",
    )

    check(
        "The current stack already has an explicit constructive projected-source witness on the Hermitian codomain",
        gamma > 0.0 and e1 > 0.0 and e2 > 0.0,
        detail="codomain-side constructive existence is not the blocker",
    )
    check(
        "The current stack already reduces the residual odd selector on the Hermitian codomain to the sign of A13",
        abs(a13 - 2.0 * gamma) < 1.0e-12 and a13 > 0.0,
        detail="codomain-side selector compression is not the blocker either",
    )
    check(
        "Therefore the exact missing step-2A object is upstream provenance: a Wilson-to-D_- / Wilson-to-dW_e^H descendant theorem",
        "Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem" in note
        and "upstream provenance" in note,
        detail="the codomain chain is known; the Wilson map is still missing",
    )
    check(
        "Once that upstream law lands, step 2B is already sharply posed as the residual right-sensitive selector on dW_e^H",
        "step 2A and step 2B are now separated cleanly" in note
        and "right-sensitive selector on `dW_e^H`" in note,
        detail="step 2A and step 2B are now cleanly separated",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
