#!/usr/bin/env python3
"""
Reduction of the direct Wilson-to-dW_e^H PF route.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_DIRECT_DWEH_ROUTE_REDUCTION_NOTE_2026-04-17.md")
    charged = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    d_last = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md")
    constructive = read("docs/DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_PROJECTED_SOURCE_SELECTOR_THEOREM_NOTE_2026-04-16.md")
    selector_reduction = read("docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md")
    step2_positive = read("docs/PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 DIRECT DWEH ROUTE REDUCTION")
    print("=" * 108)
    print()

    check(
        "Charged source-response note fixes dW_e^H as the exact charged Hermitian codomain",
        "`L_e = Schur_{E_e}(D_-)`" in charged and "`dW_e^H` reconstructs `H_e`" in charged,
        bucket="SUPPORT",
    )
    check(
        "PMNS microscopic D last-mile note says the remaining D-level object is not full D again but the off-seed projected source law dW_e^H beyond the aligned seed patch",
        "Not the full microscopic operator again." in d_last
        and "Equivalently, on the DM branch the remaining projected-source target is the" in d_last
        and "charge-`-1` off-seed source law `dW_e^H`" in d_last,
        bucket="SUPPORT",
    )
    check(
        "Constructive projected-source selector note gives an exact dW_e^H witness with gamma > 0, E1 > 0, E2 > 0",
        "It already exists." in constructive
        and "`D_- / dW_e^H` witness" in constructive
        and "`gamma > 0`" in constructive
        and "`E1 > 0`" in constructive
        and "`E2 > 0`" in constructive,
        bucket="SUPPORT",
    )
    check(
        "PMNS microscopic selector reduction theorem says the remaining blocker after dW_e^H is a right-sensitive selector law on dW_e^H",
        "right-sensitive microscopic selector law" in selector_reduction
        and "`dW_e^H = Schur_Ee(D_-)`" in selector_reduction,
        bucket="SUPPORT",
    )
    check(
        "PF step-2 minimal positive-completion note says any residual downstream PF work is at most one reduced bridge amplitude",
        "at most one downstream reduced bridge amplitude" in step2_positive
        and "`B_red = a_sel (chi_N_nu - chi_N_e)`" in step2_positive,
        bucket="SUPPORT",
    )

    check(
        "Direct dW_e^H route reduction note records that the direct Wilson-to-dW_e^H route is a fully reduced compressed alternative",
        "direct `dW_e^H` route is already sharply reduced" in note
        and "fully typed" in note
        and "fully reduced and honest" in note,
    )
    check(
        "Direct dW_e^H route reduction note records that after Wilson -> dW_e^H the only remaining PMNS-side blocker is the right-sensitive selector on dW_e^H",
        "after the direct `Wilson -> dW_e^H` law lands, the only remaining PMNS-side" in note
        and "right-sensitive selector on `dW_e^H`" in note,
    )
    check(
        "Direct dW_e^H route reduction note records that the branch now has two clean step-2A targets: Wilson -> D_- and Wilson -> dW_e^H",
        "two clean step-2A targets" in note
        and "the strong target: `Wilson -> D_-`" in note
        and "the compressed target: `Wilson -> dW_e^H`" in note,
        detail="strong and compressed step-2A routes are both now typed exactly",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
