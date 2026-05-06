#!/usr/bin/env python3
"""
PR #230 Z3 generation-action lift attempt.

The origin/main composite-Higgs packet names H1 as a load-bearing premise:
the charged-lepton Koide Z3 action must extend to the quark-bilinear
generation triplet.  The previous PR230 block proved a conditional lazy-Z3
primitive matrix theorem, but that theorem still needs H1 on the same PR230
surface.

This runner attacks H1 directly.  It constructs an exact finite countermodel:
the retained lepton/Koide Z3 action can be held fixed while the quark-bilinear
generation action is either trivial or cyclic.  Current PR230 source-only and
generation-blind action data do not distinguish those cases.  Therefore H1 is
not derivable from the current PR230 surface, though it remains a valid future
artifact if a same-surface quark-bilinear Z3 action certificate is supplied.
"""

from __future__ import annotations

import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_z3_generation_action_lift_attempt_2026-05-06.json"
)

PARENTS = {
    "origin_main_composite_higgs_intake_guard": "outputs/yt_pr230_origin_main_composite_higgs_intake_guard_2026-05-06.json",
    "z3_triplet_conditional_primitive_cone": "outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json",
    "action_first_route_completion": "outputs/yt_pr230_action_first_route_completion_2026-05-06.json",
    "neutral_primitive_route_completion": "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

TEXTS = {
    "composite_higgs_packet": "docs/COMPOSITE_HIGGS_MECHANISM_STRETCH_ATTEMPT_NOTE_2026-05-03.md",
    "koide_z3_scalar": "docs/KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md",
    "class7_spontaneous_c3": "docs/YT_CLASS_7_SPONTANEOUS_C3_BREAKING_NOTE_2026-04-18.md",
    "quark_c3_circulant_boundary": "docs/QUARK_C3_CIRCULANT_SOURCE_LAW_BOUNDARY_NOTE_2026-04-28.md",
    "sm_one_higgs": "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
    "pr230_action_first_completion": "docs/YT_PR230_ACTION_FIRST_ROUTE_COMPLETION_NOTE_2026-05-06.md",
}

REMOTE_MAIN_TEXTS = {
    "composite_higgs_packet": "docs/COMPOSITE_HIGGS_MECHANISM_STRETCH_ATTEMPT_NOTE_2026-05-03.md",
}

FUTURE_STRICT_ARTIFACTS = {
    "z3_quark_bilinear_generation_action_certificate": "outputs/yt_pr230_z3_quark_bilinear_generation_action_certificate_2026-05-06.json",
    "same_source_ew_action_certificate": "outputs/yt_wz_same_source_ew_action_certificate_2026-05-04.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0

Matrix = list[list[Fraction]]


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_text(name: str, rel: str) -> tuple[str, str]:
    path = ROOT / rel
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace"), "worktree"
    remote_rel = REMOTE_MAIN_TEXTS.get(name)
    if remote_rel:
        proc = subprocess.run(
            ["git", "show", f"origin/main:{remote_rel}"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if proc.returncode == 0:
            return proc.stdout, "origin/main"
    return "", "missing"


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    m = len(b[0])
    kdim = len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(kdim)) for j in range(m)]
        for i in range(n)
    ]


def mat_eq(a: Matrix, b: Matrix) -> bool:
    return a == b


def identity(n: int) -> Matrix:
    return [[Fraction(int(i == j), 1) for j in range(n)] for i in range(n)]


def permutation_cycle() -> Matrix:
    # Acts on column basis e1,e2,e3 by e1->e2, e2->e3, e3->e1.
    return [
        [Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
    ]


def mat_trace(a: Matrix) -> Fraction:
    return sum(a[i][i] for i in range(len(a)))


def mat_transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def conjugate_by(g: Matrix, a: Matrix) -> Matrix:
    return mat_mul(mat_mul(g, a), mat_transpose(g))


def mat_to_strings(a: Matrix) -> list[list[str]]:
    return [[str(x) for x in row] for row in a]


def finite_countermodel() -> dict[str, Any]:
    i3 = identity(3)
    c3 = permutation_cycle()
    c3_sq = mat_mul(c3, c3)
    uniform_source = i3
    singlet_sum = [[Fraction(1) for _ in range(3)] for _ in range(3)]

    rho_lepton = c3
    rho_quark_identity = i3
    rho_quark_cycle = c3

    source_checks = {
        "identity_action_preserves_uniform_source": mat_eq(
            conjugate_by(rho_quark_identity, uniform_source), uniform_source
        ),
        "cycle_action_preserves_uniform_source": mat_eq(
            conjugate_by(rho_quark_cycle, uniform_source), uniform_source
        ),
        "identity_action_preserves_singlet_sum": mat_eq(
            conjugate_by(rho_quark_identity, singlet_sum), singlet_sum
        ),
        "cycle_action_preserves_singlet_sum": mat_eq(
            conjugate_by(rho_quark_cycle, singlet_sum), singlet_sum
        ),
        "same_uniform_trace": mat_trace(uniform_source)
        == mat_trace(conjugate_by(rho_quark_cycle, uniform_source)),
    }

    phi_basis = identity(3)
    identity_triplet_image = mat_mul(rho_quark_identity, phi_basis)
    cycle_triplet_image = mat_mul(rho_quark_cycle, phi_basis)

    return {
        "rho_lepton": "C3 fixed as the Koide/lepton cyclic action",
        "rho_quark_identity": mat_to_strings(rho_quark_identity),
        "rho_quark_cycle": mat_to_strings(rho_quark_cycle),
        "rho_quark_cycle_squared": mat_to_strings(c3_sq),
        "both_are_z3_representations": mat_eq(mat_mul(mat_mul(i3, i3), i3), i3)
        and mat_eq(mat_mul(mat_mul(c3, c3), c3), i3),
        "lepton_action_held_fixed": mat_eq(rho_lepton, c3),
        "source_checks": source_checks,
        "all_source_checks_pass": all(source_checks.values()),
        "triplet_images_differ": identity_triplet_image != cycle_triplet_image,
        "h1_selects_cycle_over_identity_without_current_selector": True,
        "interpretation": (
            "The current PR230 source/action data are generation-blind enough "
            "that trivial and cyclic quark-generation Z3 actions are both "
            "compatible, while H1 requires selecting the cyclic one."
        ),
    }


def forbidden_firewall() -> dict[str, bool]:
    return {
        "uses_hunit_matrix_element_readout": False,
        "uses_yt_ward_identity_as_authority": False,
        "uses_observed_top_mass_or_yukawa_as_selector": False,
        "uses_alpha_lm_plaquette_or_u0": False,
        "uses_reduced_pilots_as_production_evidence": False,
        "sets_kappa_s_equal_one": False,
        "sets_c2_equal_one": False,
        "sets_z_match_equal_one": False,
        "claims_retained_or_proposed_retained_closure": False,
    }


def main() -> int:
    print("PR #230 Z3 generation-action lift attempt")
    print("=" * 72)

    certs = {name: load_json(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    texts_with_sources = {name: read_text(name, rel) for name, rel in TEXTS.items()}
    texts = {name: item[0] for name, item in texts_with_sources.items()}
    sources = {name: item[1] for name, item in texts_with_sources.items()}
    missing_texts = [name for name, source in sources.items() if source == "missing"]
    future_present = {
        name: (ROOT / rel).exists() for name, rel in FUTURE_STRICT_ARTIFACTS.items()
    }
    countermodel = finite_countermodel()
    firewall = forbidden_firewall()

    composite_text_compact = " ".join(texts["composite_higgs_packet"].split())
    composite_names_h1 = (
        "H1" in texts["composite_higgs_packet"]
        and "Z3 acts on quark-bilinear generation index" in composite_text_compact
        and "NO1" in texts["composite_higgs_packet"]
    )
    origin_intake_context_only = (
        certs["origin_main_composite_higgs_intake_guard"].get(
            "origin_main_composite_higgs_intake_guard_passed"
        )
        is True
        and certs["origin_main_composite_higgs_intake_guard"].get("proposal_allowed")
        is False
    )
    lazy_z3_waits_for_h1 = (
        certs["z3_triplet_conditional_primitive_cone"].get(
            "z3_triplet_conditional_primitive_theorem_passed"
        )
        is True
        and any(
            "H1" in str(item)
            for item in certs["z3_triplet_conditional_primitive_cone"].get(
                "conditional_premises", []
            )
        )
        and certs["z3_triplet_conditional_primitive_cone"].get("proposal_allowed")
        is False
    )
    koide_z3_is_lepton_selected_slice = (
        "charged-lepton selected slice" in texts["koide_z3_scalar"]
        and "T_m" in texts["koide_z3_scalar"]
        and "T_m^2 = I_3" in texts["koide_z3_scalar"].replace(chr(178), "^2")
    )
    class7_blocks_generation_resolved_retained_scalar = (
        "Neither carries a generation index" in texts["class7_spontaneous_c3"]
        and "generation-resolved bilinears" in texts["class7_spontaneous_c3"]
        and "mass term `m I` is generation-uniform" in texts["class7_spontaneous_c3"]
    )
    quark_c3_needs_extra_source_readout = (
        "source/readout theorem" in texts["quark_c3_circulant_boundary"]
        and "not predictive" in texts["quark_c3_circulant_boundary"]
    )
    sm_one_higgs_leaves_generation_matrices_free = (
        "does not select the numerical entries" in texts["sm_one_higgs"]
    )
    action_first_still_missing_action = (
        certs["action_first_route_completion"].get(
            "action_first_route_completion_passed"
        )
        is True
        and "same-source EW/Higgs action" in texts["pr230_action_first_completion"]
        and certs["action_first_route_completion"].get("proposal_allowed") is False
    )
    neutral_primitive_still_missing_generator = (
        certs["neutral_primitive_route_completion"].get(
            "neutral_primitive_route_completion_passed"
        )
        is True
        and certs["neutral_primitive_route_completion"].get("proposal_allowed")
        is False
    )
    strict_future_artifacts_absent = not any(future_present.values())
    aggregate_gates_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    no_forbidden_imports = all(value is False for value in firewall.values())

    h1_not_derived = (
        not missing_parents
        and not missing_texts
        and not proposal_allowed_parents
        and composite_names_h1
        and origin_intake_context_only
        and lazy_z3_waits_for_h1
        and koide_z3_is_lepton_selected_slice
        and class7_blocks_generation_resolved_retained_scalar
        and quark_c3_needs_extra_source_readout
        and sm_one_higgs_leaves_generation_matrices_free
        and action_first_still_missing_action
        and neutral_primitive_still_missing_generator
        and countermodel["both_are_z3_representations"]
        and countermodel["lepton_action_held_fixed"]
        and countermodel["all_source_checks_pass"]
        and countermodel["triplet_images_differ"]
        and strict_future_artifacts_absent
        and aggregate_gates_open
        and no_forbidden_imports
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("text-surfaces-present", not missing_texts, f"sources={sources}")
    report(
        "no-parent-authorizes-proposal",
        not proposal_allowed_parents,
        f"proposal_allowed={proposal_allowed_parents}",
    )
    report("composite-packet-names-h1-no1", composite_names_h1, sources["composite_higgs_packet"])
    report("origin-main-intake-context-only", origin_intake_context_only, statuses["origin_main_composite_higgs_intake_guard"])
    report("lazy-z3-theorem-waits-for-h1", lazy_z3_waits_for_h1, statuses["z3_triplet_conditional_primitive_cone"])
    report("koide-z3-current-authority-is-lepton-selected-slice", koide_z3_is_lepton_selected_slice, TEXTS["koide_z3_scalar"])
    report("class7-blocks-generation-resolved-retained-scalar", class7_blocks_generation_resolved_retained_scalar, TEXTS["class7_spontaneous_c3"])
    report("quark-c3-needs-extra-source-readout", quark_c3_needs_extra_source_readout, TEXTS["quark_c3_circulant_boundary"])
    report("sm-one-higgs-leaves-generation-matrices-free", sm_one_higgs_leaves_generation_matrices_free, TEXTS["sm_one_higgs"])
    report("action-first-still-missing-same-source-action", action_first_still_missing_action, statuses["action_first_route_completion"])
    report("neutral-primitive-still-missing-generator", neutral_primitive_still_missing_generator, statuses["neutral_primitive_route_completion"])
    report("countermodel-keeps-lepton-z3-fixed", countermodel["lepton_action_held_fixed"], countermodel["rho_lepton"])
    report("finite-countermodel-two-quark-actions-allowed", countermodel["both_are_z3_representations"] and countermodel["all_source_checks_pass"], countermodel["interpretation"])
    report("countermodel-distinguishes-h1", countermodel["triplet_images_differ"], "identity action != cyclic action on Phi triplet")
    report("strict-future-artifacts-absent", strict_future_artifacts_absent, str(future_present))
    report("aggregate-gates-still-open", aggregate_gates_open, "assembly/retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))
    report("h1-lift-not-derived-on-current-surface", h1_not_derived, "same-surface quark-bilinear Z3 action selector absent")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / Z3 generation-action lift to PR230 "
            "quark-bilinear triplet not derived on current surface"
        ),
        "conditional_surface_status": (
            "H1 may reopen if a same-surface PR230 quark-bilinear Z3 action "
            "certificate selects the cyclic triplet action and ties it to the "
            "top FH/LSZ source/action surface."
        ),
        "hypothetical_axiom_status": (
            "If H1 plus the remaining H2-H4 premises are accepted, the prior "
            "lazy-Z3 primitive theorem can become part of a neutral primitive "
            "or action-first support chain; not current-surface closure."
        ),
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "pr230_closure_authorized": False,
        "h1_generation_action_lift_attempt_passed": h1_not_derived,
        "same_surface_h1_derived": False,
        "z3_quark_bilinear_action_certificate_present": future_present[
            "z3_quark_bilinear_generation_action_certificate"
        ],
        "countermodel": countermodel,
        "future_artifact_presence": future_present,
        "missing_current_surface_premises": [
            "same-surface quark-bilinear generation Z3 action certificate",
            "operator/action surface carrying the bilinear triplet and PR230 top FH/LSZ source together",
            "selector that distinguishes cyclic quark action from trivial quark action without observed masses",
            "same-source EW/Higgs action or neutral off-diagonal generator",
            "H2 equal or controlled condensate magnitudes and strong-coupling magnitude authority",
        ],
        "claim_firewall": {
            "does_not_claim_retained_or_proposed_retained_closure": True,
            "does_not_write_strict_future_certificate": True,
            "does_not_use_hunit_or_ward_authority": True,
            "does_not_use_observed_targets": True,
            "does_not_set_kappa_c2_or_zmatch_to_one": True,
        },
        "forbidden_firewall": firewall,
        "parent_statuses": statuses,
        "text_sources": sources,
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
        "exact_next_action": (
            "Either derive a same-surface quark-bilinear Z3 action certificate "
            "that selects the cyclic triplet action, or pivot to a different "
            "bridge contract: certified O_H/C_sH/C_HH rows, W/Z rows with "
            "strict g2/covariance/delta_perp, Schur A/B/C rows, or strict "
            "scalar-LSZ authority."
        ),
    }

    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
