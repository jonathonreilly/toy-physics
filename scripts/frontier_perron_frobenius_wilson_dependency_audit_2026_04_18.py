#!/usr/bin/env python3
"""
Audit which current PF-branch statements depend on Wilson robustness.
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
    note = read("docs/PERRON_FROBENIUS_WILSON_DEPENDENCY_AUDIT_NOTE_2026-04-18.md")
    parent = read("docs/GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md")
    parent_boundary = read("docs/PERRON_FROBENIUS_PARENT_INTERTWINER_BOUNDARY_NOTE_2026-04-17.md")
    path_target = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_CHAIN_PATH_ALGEBRA_TARGET_NOTE_2026-04-18.md")
    path_cert = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_PATH_ALGEBRA_MINIMAL_CERTIFICATE_NOTE_2026-04-18.md")
    path_nogo = read("docs/PERRON_FROBENIUS_STEP2_WILSON_LOCAL_PATH_ALGEBRA_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-18.md")
    slab = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_ONE_SLAB_ORTHOGONAL_KERNEL_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md")
    rim = read("docs/GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md")
    pmns_sole = read("docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    pmns_readout = read("docs/PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md")
    finite_packet = read("docs/GAUGE_VACUUM_PLAQUETTE_FINITE_SAMPLE_PACKET_NONCLOSURE_NOTE_2026-04-17.md")
    cyclic_bulk = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_CYCLIC_BULK_REDUCTION_NOTE_2026-04-17.md")
    global_closure = read("docs/PERRON_FROBENIUS_GLOBAL_SELECTOR_CURRENT_STACK_CLOSURE_NOTE_2026-04-17.md")

    print("=" * 112)
    print("PERRON-FROBENIUS WILSON DEPENDENCY AUDIT")
    print("=" * 112)
    print()

    check(
        "The repo already ties step 1 and the positive reopening route directly to the Wilson surface",
        "Yes, on the Wilson gauge surface." in parent
        and "canonical plaquette / `theta` descendants" in parent
        and "step 1 is closed only on the Wilson gauge surface" in parent_boundary
        and "`Phi_chain : A_chain -> End(H_W)`" in path_target,
        detail="Wilson parent plus Wilson-local source route are already explicit branch objects",
    )
    check(
        "The repo already packages the sharpest positive Wilson route as the local path-algebra certificate and says the current bank does not realize it",
        "minimal local path-algebra `2-edge + 3` certificate" in path_cert
        and "current bank still does **not** realize the local path-algebra" in path_cert
        and "does **not** already realize `Phi_chain`" in path_nogo,
        detail="positive Wilson reopening really hinges on the local Phi_chain route",
    )
    check(
        "The repo already makes the plaquette operator-side integral identifications Wilson-dependent",
        "Then the one-slab orthogonal kernel is exactly the Wilson/Haar integral" in slab
        and "one exact local Wilson/Haar rim integral" in rim,
        detail="positive operator interpretation of K_beta^env and B_beta(W) is Wilson-structured",
    )
    check(
        "The repo already records non-Wilson-only blockers: PMNS sole-axiom triviality, Wilson-free PMNS readout, and plaquette nonclosure",
        "stays trivial" in pmns_sole
        and "exactly `(I3, I3)`" in pmns_sole
        and "external Wilson or plaquette input is involved." in pmns_readout
        and "remaining PMNS-native blocker is no longer fixed-slice readout" in pmns_readout
        and "no finite sample packet" in finite_packet
        and "still does not determine the reduced cyclic bulk object" in cyclic_bulk,
        detail="Wilson is not the only blocker on the current branch",
    )
    check(
        "The current-stack global closure note already remains negative for reasons beyond a positive Wilson bridge alone",
        "does **not** yet derive one common sole-axiom global PF selector" in global_closure
        and "no finite sample packet can determine it." in global_closure
        and "operator-plus-projection" in global_closure,
        detail="global negative closure already cites PMNS and plaquette blockers directly",
    )

    check(
        "The new audit note records the asymmetric dependency map in review-safe form",
        "Wilson robustness matters **asymmetrically**." in note
        and "What depends directly on Wilson robustness" in note
        and "What does **not** become positive merely by reopening Wilson" in note
        and "Inference from the cited notes" in note,
        detail="the note separates exact repo evidence from branch-level inference",
        bucket="SUPPORT",
    )
    check(
        "The new audit note identifies Wilson as the main positive reopening lever while keeping PMNS and plaquette blockers live",
        "Wilson is the main positive reopening lever" in note
        and "PMNS triviality and plaquette nonclosure are still live blockers" in note,
        detail="the branch consequence is stated without overclaiming a Wilson theorem",
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
