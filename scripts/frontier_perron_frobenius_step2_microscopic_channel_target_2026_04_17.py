#!/usr/bin/env python3
"""
Reduction of the live step-2A PF target to a Wilson-to-charged microscopic
channel.
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
    note = read("docs/PERRON_FROBENIUS_STEP2_MICROSCOPIC_CHANNEL_TARGET_NOTE_2026-04-17.md")
    step2_positive = read("docs/PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md")
    charged = read("docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md")
    projector_interface = read("docs/DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md")
    support_pullback = read("docs/PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS STEP-2 MICROSCOPIC CHANNEL TARGET")
    print("=" * 108)
    print()

    check(
        "Step-2 minimal positive-completion note says the upstream Wilson-to-Hermitian descendant law comes before any residual PMNS bridge amplitude",
        "Wilson-to-Hermitian descendant law" in step2_positive
        and "one upstream descendant law" in step2_positive
        and "at most one downstream reduced bridge amplitude" in step2_positive,
        bucket="SUPPORT",
    )
    check(
        "Charged source-response note says dW_e^H is the Schur pushforward of D_- and reconstructs H_e",
        "`L_e = Schur_{E_e}(D_-)`" in charged
        and "`dW_e^H` reconstructs `H_e`" in charged,
        bucket="SUPPORT",
    )
    check(
        "PMNS projector-interface note says the projector packet is automatic once the Hermitian pair is supplied",
        "once that pair is supplied, the PMNS matrix is readable" in projector_interface
        and "the flavored transport projector packet is then automatic" in projector_interface,
        bucket="SUPPORT",
    )
    check(
        "Charged-support pullback boundary note excludes pure support pullback as the source of the missing charged embedding/compression object",
        "does **not** supply a Wilson-side charged" in support_pullback
        and "pure pullback of `E_e`" in support_pullback,
        bucket="SUPPORT",
    )

    check(
        "Microscopic-channel target note records that the unresolved content is not support labeling, projector readout, or downstream Hermitian packet algebra",
        "remaining unresolved content is not" in note
        and "support labeling" in note
        and "projector readout" in note
        and "downstream Hermitian packet algebra" in note,
    )
    check(
        "Microscopic-channel target note records that the live unresolved object is a Wilson-to-charged microscopic channel with Wilson-to-D_- as the cleanest target",
        "live unresolved step-2A object is exactly a new" in note
        and "Wilson-to-charged microscopic channel" in note
        and "Wilson-to-`D_-` law" in note,
    )
    check(
        "Microscopic-channel target note records that dW_e^H, H_e, and the projector packet are already downstream once the microscopic law is supplied",
        "the charged codomain data `E_e`, `dW_e^H`, `H_e`, and the projector packet" in note
        and "are all downstream once the charged microscopic law is supplied" in note,
        detail="cleanest constructive target is now explicit",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
