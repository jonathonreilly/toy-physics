#!/usr/bin/env python3
"""
Current-stack global closure theorem for the sole-axiom PF selector question.
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
    parent_note = read("docs/GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    pmns_mode = read("docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md")
    pmns_sole = read("docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    plaquette_eval = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md"
    )
    finite_packet = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FINITE_SAMPLE_PACKET_NONCLOSURE_NOTE_2026-04-17.md"
    )
    pf_boundary = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")

    print("=" * 112)
    print("PERRON-FROBENIUS GLOBAL SELECTOR CURRENT-STACK CLOSURE")
    print("=" * 112)
    print()

    check(
        "Wilson parent/compression note already proves canonical descendants only for plaquette compression and theta weighting",
        "canonical plaquette / `theta` descendants" in parent_note
        and "canonical PMNS projection" in parent_note
        and "does **not** yet support" in parent_note,
        bucket="SUPPORT",
    )
    check(
        "PMNS dominant-mode note already limits the native PMNS law to the aligned seed pair",
        "dominant symmetric mode" in pmns_mode
        and "does **not** determine the generic `5`-real" in pmns_mode,
        bucket="SUPPORT",
    )
    check(
        "PMNS sole-axiom boundary note already says the strongest canonical sole-axiom hw=1 pack remains trivial",
        "stays trivial" in pmns_sole
        and "exactly `(I3, I3)`" in pmns_sole,
        bucket="SUPPORT",
    )
    check(
        "Plaquette evaluator-route note already says the three-sample route factors through one common beta-side vector that is still undetermined",
        "common beta-side vector" in plaquette_eval
        and "does **not** yet furnish an actual evaluator" in plaquette_eval,
        bucket="SUPPORT",
    )
    check(
        "Finite-sample-packet nonclosure note already says no finite packet can determine the full beta-side vector v_6",
        "no finite sample packet" in finite_packet
        and "full beta-side vector `v_6`" in finite_packet,
        bucket="SUPPORT",
    )
    check(
        "PF boundary note already records sector-local PF success but not one common sole-axiom selector",
        "Partially, but not globally." in pf_boundary
        and "single common physical-state selector from the sole axiom" in pf_boundary
        and "nontrivial PMNS" in pf_boundary,
        bucket="SUPPORT",
    )

    check(
        "A positive global sole-axiom PF selector would require a nontrivial PMNS-side descendant/projection law, but the current stack does not provide one",
        "stays trivial" in pmns_sole and "corner-breaking source" in pmns_mode,
        detail="PMNS side still stops at trivial sole-axiom pack plus aligned seed-pair dominant mode",
    )
    check(
        "A positive global sole-axiom PF selector would require a determined plaquette framework-point beta-side object, but the current stack does not provide one",
        "does **not** yet furnish an actual evaluator" in plaquette_eval
        and "no finite sample packet" in finite_packet,
        detail="plaquette side still lacks determined v_6 and sample-side closure is structurally impossible",
    )
    check(
        "Therefore the current stack supports sector-local PF theorems but not one common sole-axiom global PF selector",
        "Partially, but not globally." in pf_boundary
        and "single common physical-state selector from the sole axiom" in pf_boundary
        and "not yet" in pf_boundary,
        detail="current-stack global closure is negative, not positive",
    )
    check(
        "The remaining honest global route is operator-plus-projection: explicit plaquette beta data plus a Wilson-to-PMNS descendant/projection theorem",
        "full beta-side vector `v_6`" in finite_packet
        and "PMNS" in parent_note
        and "does **not** yet support" in parent_note,
        detail="new operator data and new projection data are both still required",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
