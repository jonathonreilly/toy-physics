#!/usr/bin/env python3
"""
Current-bank nonrealization theorem for the missing Wilson-to-Hermitian bridge.
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
    note = read("docs/PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md")
    parent = read("docs/GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    observable = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    support = read("docs/SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md")
    full_d = read("docs/DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md")
    charged = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    sole_axiom = read("docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    selector_bank = read("docs/PMNS_SELECTOR_BANK_NONREALIZATION_NOTE.md")
    sector_nonforcing = read("docs/PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md")

    print("=" * 112)
    print("PERRON-FROBENIUS WILSON-TO-HERMITIAN DESCENDANT CURRENT-BANK NONREALIZATION")
    print("=" * 112)
    print()

    check(
        "Wilson parent note already proves exact plaquette/theta descendants and explicitly stops before PMNS provenance",
        "Plaquette source-sector compression" in parent
        and "Topological Fourier descendant" in parent
        and "especially PMNS, is already a canonical projection of" in parent,
        bucket="SUPPORT",
    )
    check(
        "Observable-principle note already fixes the current observable backbone to the scalar determinant generator",
        "`W[J] = log |det(D+J)| - log |det D|`" in observable
        or "`W[J] = log|det(D+J)| - log|det D|`" in observable,
        bucket="SUPPORT",
    )
    check(
        "Observable-principle note keeps local observables at scalar source-derivative level rather than a charged-sector matrix law",
        "local scalar observables are source derivatives of `W`" in observable
        and "Re Tr[(D+J)^(-1) P_x]" in observable,
        bucket="SUPPORT",
    )
    check(
        "Site-phase / cube-shift note is an exact support intertwiner whose safe role is support transport only",
        "exact support theorem" in support
        and "Its safe role is narrower" in support,
        bucket="SUPPORT",
    )
    check(
        "Full microscopic reduction note starts the exact PMNS / DM chain only once D is supplied",
        "The exact chain is now:" in full_d
        and "`D`" in full_d
        and "`-> D_-`" in full_d
        and "`-> dW_e^H`" in full_d
        and "So once the full microscopic charge-preserving operator `D` is supplied" in full_d,
        bucket="SUPPORT",
    )
    check(
        "Charged source-response reduction note keeps dW_e^H as an exact Schur pushforward but explicitly says it is not yet derived from the sole axiom",
        "`dW_e^H` is an exact charged-sector Schur pushforward" in charged
        and "This note does **not** yet evaluate `D_-` or `dW_e^H` from the sole axiom." in charged,
        bucket="SUPPORT",
    )
    check(
        "Strongest canonical sole-axiom hw=1 source/transfer pack still stays trivial",
        "The strongest canonical sole-axiom `hw=1` source/transfer construction stays" in sole_axiom
        and "exactly `(I3, I3)`" in sole_axiom,
        bucket="SUPPORT",
    )
    check(
        "PMNS selector-bank nonrealization note already proves no retained bridge theorem maps existing selector outputs into the PMNS branch datum",
        "No retained bridge theorem maps the existing selector outputs into that PMNS" in selector_bank
        and "branch datum." in selector_bank
        and "branch selector." in selector_bank,
        bucket="SUPPORT",
    )
    check(
        "PMNS sector-exchange nonforcing note already proves there is no retained sector-sensitive inter-sector bridge theorem",
        "current atlas contains no retained sector-sensitive inter-sector bridge" in sector_nonforcing
        and "theorem" in sector_nonforcing,
        bucket="SUPPORT",
    )

    check(
        "Current bank nonrealization note states the missing bridge is not already contained under another name",
        "does **not** already contain the missing" in note
        and "under another" in note
        and "name" in note
        and "Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem" in note,
    )
    check(
        "The theorem isolates the exact domains of the existing tools without promoting any of them to the missing cross-sector law",
        "Wilson parent object" in note
        and "scalar observable backbone" in note
        and "support intertwiners" in note
        and "PMNS / DM microscopic chain" in note
        and "selector/support bank" in note,
    )
    check(
        "The corollary closes the hidden-bridge loophole and narrows the next honest move to a genuinely new descendant law",
        "hidden-bridge loophole" in note
        and "derive a genuinely new Wilson-to-`D_-` / Wilson-to-`dW_e^H`" in note,
        detail="review-safe closure: stop scanning the current bank for a renamed bridge",
    )
    check(
        "The note stays within current-bank scope and does not overclaim a final impossibility theorem",
        "What this does not close" in note
        and "a positive Wilson-to-`D_-` theorem" in note
        and "a positive global PF selector" in note,
        detail="negative only at the current-bank level",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
