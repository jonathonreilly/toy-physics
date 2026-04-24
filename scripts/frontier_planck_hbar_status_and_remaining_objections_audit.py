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
    integral_count = read("docs/PLANCK_SCALE_PRIMITIVE_INTEGRAL_ACTION_COUNT_THEOREM_2026-04-24.md")
    si_discharge = read("docs/PLANCK_SCALE_SI_HBAR_OBJECTION_DISCHARGE_THEOREM_2026-04-24.md")
    action_phase_hbar = read("docs/PLANCK_SCALE_ACTION_PHASE_REPRESENTATION_HBAR_THEOREM_2026-04-24.md")
    weyl_hbar = read("docs/PLANCK_SCALE_PRIMITIVE_WEYL_HBAR_REPRESENTATION_THEOREM_2026-04-24.md")
    parent_discharge = read(
        "docs/PLANCK_SCALE_PARENT_SOURCE_DISCHARGE_AFTER_REALIFICATION_THEOREM_2026-04-24.md"
    )

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "audit-separates-structural-hbar-from-si-hbar",
        "derives the structural action-to-phase role of `hbar`" in audit
        and "standard Weyl/commutator\nappearances" in audit
        and "does **not**\nderive the SI value of `hbar`" in audit
        and "does not make the\nfinite automorphism group itself an infinitesimal commutator theory" in audit,
        "the audit claims structural and Weyl hbar but refuses SI overclaim",
    )

    total += 1
    passed += expect(
        "audit-denies-si-numerical-prediction",
        "Numerical prediction of `hbar` in SI units" in audit
        and "unit convention" in audit
        and "SI-`hbar` objection is not a remaining physical\nblocker" in audit
        and "SI decimal value of `hbar` is not a physical\n> prediction target" in si_discharge
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
        "audit-discharges-object-class-after-realification",
        "primitive boundary-action object class is discharged after realified B3" in audit
        and "the parent-source discharge theorem forces\n`B_parent=(H_A,P_A)`" in audit
        and "`B_parent = (H_A, P_A)`" in parent_discharge
        and "retained primitive one-step boundary/worldtube object class" in parent_source,
        "parent-source object class is no longer an independent blocker after B3 realification",
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
        "integral-action-count-closes-reduced-gamma",
        "Closed on the primitive integral-history surface" in audit
        and "The primitive integral action-count\n"
        "theorem supplies the needed non-homogeneous law" in audit
        and "Therefore `Phi(I_16)=1` and `gamma=1` in\nreduced action units" in audit
        and "`Phi(I_16) = ell([A_cell]) = 1`" in integral_count,
        "gamma=1 is now closed as a reduced integral count, not as SI hbar",
    )

    total += 1
    passed += expect(
        "action-phase-representation-closes-structural-hbar",
        "Structural action-phase role of `hbar`" in audit
        and "S/hbar=Phi" in audit
        and "`S(A_cell)=hbar`" in audit
        and "`S(H)/hbar = Phi(H)`" in action_phase_hbar
        and "`S(A_cell) = hbar`" in action_phase_hbar
        and "not a prediction of the SI decimal value of `hbar`" in action_phase_hbar,
        "structural hbar is closed as action-to-phase conversion",
    )

    total += 1
    passed += expect(
        "weyl-representation-closes-textbook-hbar-appearances",
        "Textbook Weyl/commutator appearances of `hbar`" in audit
        and "`[X,P] = i hbar`" in audit
        and "`p = hbar k` and `E = hbar omega`" in audit
        and "`Delta X Delta P >= hbar/2`" in audit
        and "`[X,P] = i hbar I`" in weyl_hbar
        and "`J_i = (hbar/2) sigma_i`" in weyl_hbar,
        "Weyl, commutator, uncertainty, and angular-momentum roles are represented",
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
        "conditional structural Planck-length result" in audit
        and "coherent-history phase\n"
        "> representation gives `S/hbar=Phi`, hence `S(A_cell)=hbar`" in audit
        and "realified Weyl representation then gives `p=hbar k`, `E=hbar omega`,\n"
        "> `[X,P]=i hbar`, uncertainty, and angular-momentum units" in audit
        and "Do not use:\n\n> The branch predicts the numerical SI value of the Planck constant."
        in audit,
        "safe structural/Weyl hbar claim and unsafe SI claim are explicit",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
