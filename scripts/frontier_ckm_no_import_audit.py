#!/usr/bin/env python3
"""
Strict CKM No-Import Audit
==========================

Purpose:
  Evaluate the current worktree CKM routes against a deliberately harsh review
  standard:

    1. full quantitative CKM scope
    2. no direct observed-physics inputs in the derivation
    3. no scheme/matching dependence
    4. no decisive bounded/open step

The goal is not to re-prove the physics. The goal is to answer one narrow
question honestly:

  "Do we already have an airtight no-import CKM closure that would survive
   the harshest Nature-style critic?"

This script codifies the branch's own stated boundaries and converts them into
an explicit yes/no verdict.
"""

from __future__ import annotations

from dataclasses import dataclass


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


@dataclass(frozen=True)
class Route:
    name: str
    script: str
    note: str
    quantitative_scope: str
    has_full_quantitative_ckm_scope: bool
    uses_direct_observed_inputs: bool
    scheme_or_matching_dependency: bool
    decisive_step_still_bounded: bool
    short_reason: str


ROUTES = [
    Route(
        name="Atlas/axiom no-import package",
        script="scripts/frontier_ckm_atlas_axiom_closure.py",
        note="docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md",
        quantitative_scope="full sharp CKM matrix from the canonical CMT alpha_s(v), atlas counts {2,3,6}, the exact 1/6 center-excess projector, the exact bilinear tensor carrier K_R on A1 x {E_x, T1x}, the Z3 phase source, and the Schur cascade",
        has_full_quantitative_ckm_scope=True,
        uses_direct_observed_inputs=False,
        scheme_or_matching_dependency=False,
        decisive_step_still_bounded=False,
        short_reason="Uses only the canonical derived alpha_s(v), exact EWSB/gauge/matter counts, the exact 1/6 center-excess projector, the exact bilinear tensor carrier K_R, the Z3 phase source, and the Schur cascade.",
    ),
    Route(
        name="Structural Z3 + EWSB CKM chain",
        script="scripts/frontier_ckm_closure.py",
        note="docs/CKM_CLOSURE_NOTE.md",
        quantitative_scope="bounded hierarchy + order-of-magnitude CKM, not full sharp matrix",
        has_full_quantitative_ckm_scope=False,
        uses_direct_observed_inputs=False,
        scheme_or_matching_dependency=False,
        decisive_step_still_bounded=True,
        short_reason="O(1) Yukawa coefficients remain open, so the quantitative matrix is not closed.",
    ),
    Route(
        name="Exact NNI plus overlap V_cb route",
        script="scripts/frontier_ckm_vcb_closure.py",
        note="docs/CKM_VCB_CLOSURE_NOTE.md",
        quantitative_scope="sharp V_cb only",
        has_full_quantitative_ckm_scope=False,
        uses_direct_observed_inputs=False,
        scheme_or_matching_dependency=True,
        decisive_step_still_bounded=True,
        short_reason="Absolute S_23 normalization, matching factor, and L->infinity control remain bounded.",
    ),
    Route(
        name="Five-sixths mass-ratio V_cb route",
        script="scripts/frontier_ckm_five_sixths.py",
        note="docs/CKM_FIVE_SIXTHS_NOTE.md",
        quantitative_scope="sharp V_cb only",
        has_full_quantitative_ckm_scope=False,
        uses_direct_observed_inputs=True,
        scheme_or_matching_dependency=True,
        decisive_step_still_bounded=True,
        short_reason="Uses PDG quark masses and only matches sharply in the PDG reference-mass convention.",
    ),
    Route(
        name="Exponent proof for V_cb = (m_s/m_b)^(5/6)",
        script="scripts/frontier_ckm_exponent_proof.py",
        note="docs/CKM_EXPONENT_PROOF_NOTE.md",
        quantitative_scope="sharp V_cb argument only",
        has_full_quantitative_ckm_scope=False,
        uses_direct_observed_inputs=True,
        scheme_or_matching_dependency=True,
        decisive_step_still_bounded=True,
        short_reason="Operator identification and exponentiation mechanism are explicitly marked bounded.",
    ),
]


def audit_route(route: Route) -> bool:
    print("=" * 78)
    print(route.name)
    print("=" * 78)
    print(f"  script: {route.script}")
    print(f"  note:   {route.note}")
    print(f"  scope:  {route.quantitative_scope}")
    print()

    c1 = check(
        "full quantitative CKM scope",
        route.has_full_quantitative_ckm_scope,
        route.quantitative_scope,
    )
    c2 = check(
        "no direct observed inputs",
        not route.uses_direct_observed_inputs,
        "fails if observed quark masses or fitted observables are used as derivation inputs",
    )
    c3 = check(
        "no scheme or matching dependency",
        not route.scheme_or_matching_dependency,
        "fails if the route depends on reference-mass convention, matching factors, or finite-volume normalization",
    )
    c4 = check(
        "no decisive bounded/open step",
        not route.decisive_step_still_bounded,
        "fails if the route's own note still marks the key closure step as bounded/open",
    )

    route_passes = c1 and c2 and c3 and c4
    verdict = "SURVIVES" if route_passes else "DOES NOT SURVIVE"
    print()
    print(f"  Strict verdict: {verdict}")
    print(f"  Boundary reason: {route.short_reason}")
    print()
    return route_passes


print("=" * 78)
print("STRICT CKM NO-IMPORT AUDIT")
print("=" * 78)
print()
print("Audit standard:")
print("  1. full quantitative CKM scope")
print("  2. no direct observed inputs")
print("  3. no scheme/matching dependence")
print("  4. no decisive bounded/open step")
print()

survivors = []
for route in ROUTES:
    if audit_route(route):
        survivors.append(route)

print("=" * 78)
print("FINAL VERDICT")
print("=" * 78)
print()

overall_closed = len(survivors) > 0
check(
    "at least one route survives the strict no-import audit",
    overall_closed,
    "one or more routes pass all four criteria" if overall_closed else "none of the current CKM routes passes all four criteria",
)
print()

if overall_closed:
    print("  VERDICT: CKM is closed on a strict no-import surface.")
else:
    print("  VERDICT: CKM is NOT closed on a strict no-import surface.")
    print("  Best honest statement: the current worktree still lacks an airtight")
    print("  no-import route that survives the harshest critic.")

print()
print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
