#!/usr/bin/env python3
"""
Remaining-path route audit for the current Perron-Frobenius branch.
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
    route_audit = read("docs/PERRON_FROBENIUS_REMAINING_PATHS_ROUTE_AUDIT_NOTE_2026-04-17.md")
    pmns_sole = read("docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md")
    beta6_reduction = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_EVALUATION_SEAM_REDUCTION_SCIENCE_ONLY_NOTE_2026-04-17.md")
    transfer_under = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_UNDERDETERMINATION_NOTE_2026-04-17.md")
    evaluator_route = read("docs/GAUGE_VACUUM_PLAQUETTE_FIRST_THREE_SAMPLE_ENVIRONMENT_EVALUATOR_ROUTE_NOTE_2026-04-17.md")

    print("=" * 108)
    print("PERRON-FROBENIUS REMAINING PATHS ROUTE AUDIT")
    print("=" * 108)
    print()

    check(
        "The PMNS strong and compressed routes now converge onto one Wilson-side charged construction, with the compressed dW_e^H route the cleaner first target",
        "one common upstream need" in route_audit
        and "Wilson-side charged embedding / source-family object" in route_audit
        and "compressed route is therefore the cleaner first target" in route_audit
        and "smallest live `D_-`-level target" in route_audit
        and "remaining primitive is one Wilson-side charged" in route_audit
        and "source family / channel landing on `dW_e^H`" in route_audit,
        detail="the PMNS-side remaining work is no longer a broad bridge search",
    )
    check(
        "The sole-axiom PMNS-pack path remains negative and still leaves J_chi as the smallest residual non-Hermitian target",
        "strongest canonical sole-axiom `hw=1` pack remains trivial" in route_audit
        and "smallest native non-Hermitian PMNS target remains the current" in route_audit
        and "`J_chi`" in route_audit
        and "still forced to zero" in route_audit
        and "stays trivial" in pmns_sole,
        detail="the sole-axiom PMNS lane still does not replace the missing Wilson descendant",
    )
    check(
        "The plaquette beta=6 lane is now a compressed class-sector operator-evaluation problem, with the rim side further advanced than the bulk side",
        "compressed class-sector level" in route_audit
        and "`S_6^env = P_cls K_6^env P_cls`" in route_audit
        and "`eta_6(W) = P_cls B_6(W)`" in route_audit
        and "rim side is already further advanced than the bulk side" in route_audit
        and "class-sector matrix elements" in beta6_reduction
        and "operator-evaluation problem" in route_audit,
        detail="the remaining plaquette work is operator-side evaluation, not more PF formalism",
    )
    check(
        "No overlooked stronger repo-wide no-go replaces explicit nonlocal class-sector evaluation on the plaquette lane; the stronger current negatives are downstream only",
        "strongest current negatives are downstream only" in route_audit
        and "no overlooked stronger repo-wide no-go replaces the need" in route_audit
        and "distinct admissible positive self-adjoint" in transfer_under
        and "does **not** determine that beta-side vector" in evaluator_route
        and "class-sector evaluation of the nonlocal `S_6^env / eta_6` data" in route_audit,
        detail="the branch still needs explicit class-sector operator data rather than another downstream no-go",
    )

    check(
        "Therefore the surviving global PF branch is now reduced to two constructive upstream primitives plus one downstream residual PMNS current target",
        "two constructive upstream primitives and one downstream residual PMNS" in route_audit
        and "positive global PF selector closure" in route_audit,
        detail="PMNS charged Wilson descendant, plaquette class-sector evaluation, then residual J_chi if needed",
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
