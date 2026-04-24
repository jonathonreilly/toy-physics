#!/usr/bin/env python3
"""Hostile-review audit for hbar status and remaining objections."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def main() -> int:
    audit = read("docs/PLANCK_SCALE_HBAR_STATUS_AND_REMAINING_OBJECTIONS_AUDIT_2026-04-23.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")
    area = read("docs/PLANCK_SCALE_AREA_ACTION_NORMALIZATION_THEOREM_2026-04-23.md")
    action_phase = read("docs/PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md")
    information = read("docs/PLANCK_SCALE_INFORMATION_ACTION_UNIT_MAP_THEOREM_LANE_2026-04-23.md")
    parent_source = read("docs/PLANCK_SCALE_BOUNDARY_PARENT_SOURCE_EQUIVALENCE_THEOREM_2026-04-23.md")
    phase_trace = read("docs/PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md")
    gamma_period = read("docs/PLANCK_SCALE_GAMMA_PHASE_PERIOD_OBSTRUCTION_THEOREM_2026-04-24.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "audit-denies-hbar-derivation",
        "does **not** derive `hbar`" in audit
        and "not a\nnumerical SI prediction of `hbar`" in audit,
        "the audit does not overclaim the hbar axis",
    )

    total += 1
    passed += expect(
        "audit-denies-si-numerical-prediction",
        "Numerical prediction of `hbar` in SI units" in audit
        and "unit convention" in audit
        and "BIPM" in audit
        and "NIST" in audit,
        "post-2019 SI guardrail is explicit",
    )

    total += 1
    passed += expect(
        "area-normalization-imports-hbar",
        "`hbar` be the reduced Planck constant" in area
        and "`l_P^2 := hbar G / c_light^3`" in area
        and "Imported physical normalization" in area,
        "final length normalization imports hbar rather than deriving it",
    )

    total += 1
    passed += expect(
        "audit-states-dimensionless-planck-claim",
        "`a^2 c_light^3 / (hbar G) = 1`" in audit
        and "`a^2 / l_P^2 = 1`" in audit,
        "the physical Planck claim is dimensionless",
    )

    total += 1
    passed += expect(
        "audit-keeps-object-class-objection-live",
        "primitive boundary-action object class remains the top live denial" in audit
        and "retained primitive one-step boundary/worldtube object class" in parent_source,
        "the top remaining rejection is physical object-class identification",
    )

    total += 1
    passed += expect(
        "audit-keeps-p1-scope-objection-live",
        "older minimal ledger alone still does not prove" in audit
        and "`rho_cell = I_16 / 16`" in audit,
        "source-free state semantics are scoped as an authorized surface",
    )

    total += 1
    passed += expect(
        "action-phase-ratio-reduced-to-gamma",
        "`a^2 / l_P^2 = 8 pi q_* / eps_*`" in action_phase
        and "`a^2/l_P^2 = gamma`" in audit
        and "`gamma = 1`" in phase_trace,
        "the first-principles action-phase lane is reduced to gamma = 1",
    )

    total += 1
    passed += expect(
        "information-action-kappa-reduced-to-gamma",
        "`q_* = kappa_info I_*`" in information
        and "`kappa_info = gamma/32 per bit`" in audit
        and "`kappa_info = q_* / I_* = gamma / 32 per bit`" in phase_trace,
        "the information/action unit map has the same gamma scalar obstruction",
    )

    total += 1
    passed += expect(
        "phase-period-obstruction-is-narrow",
        "bare U(1) periodicity or\nfinite roots alone cannot select" in audit
        and "does not reject projective/central-extension\nattacks" in audit
        and "A 16th root gives phase\n`exp(2 pi i / 16)`" in gamma_period,
        "the audit scrutinizes the no-go before blocking central-extension routes",
    )

    total += 1
    passed += expect(
        "reviewer-links-hbar-audit",
        "PLANCK_SCALE_HBAR_STATUS_AND_REMAINING_OBJECTIONS_AUDIT_2026-04-23.md" in reviewer,
        "canonical reviewer packet points to the hbar-status audit",
    )

    total += 1
    passed += expect(
        "safe-claim-preserved",
        "conditional structural Planck-length result, not a derivation of `hbar`" in audit
        and "Do not use:\n\n> The branch derives the Planck constant." in audit,
        "safe and unsafe claims are explicit",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
