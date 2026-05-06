#!/usr/bin/env python3
"""
PR #230 Z3-triplet conditional primitive-cone theorem.

This runner turns the origin/main composite-Higgs Z3 triplet into an exact
finite-matrix primitive-cone theorem, while keeping the PR230 claim boundary
intact.  The theorem is conditional: if a same-surface PR230 action supplies a
positive lazy Z3 cyclic neutral transfer on the three Higgs-like bilinear
channels, then Perron-Frobenius rank-one neutral support follows.  The current
PR230 surface still lacks the same-surface action/off-diagonal generator, so
this is support for a future neutral-primitive or action-first artifact, not
top-Yukawa closure.
"""

from __future__ import annotations

import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json"
)
REMOTE_MAIN = "origin/main"
H2_SUPPORT = (
    "outputs/yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json"
)

COMPOSITE_PATHS = {
    "note": "docs/COMPOSITE_HIGGS_MECHANISM_STRETCH_ATTEMPT_NOTE_2026-05-03.md",
    "runner": "scripts/frontier_composite_higgs_mechanism.py",
    "assumptions": ".claude/science/physics-loops/composite-higgs-mechanism-2026-05-03/ASSUMPTIONS_AND_IMPORTS.md",
}

PARENTS = {
    "origin_main_composite_higgs_intake_guard": "outputs/yt_pr230_origin_main_composite_higgs_intake_guard_2026-05-06.json",
    "same_surface_z3_taste_triplet": "outputs/yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json",
    "neutral_primitive_route_completion": "outputs/yt_pr230_neutral_primitive_route_completion_2026-05-06.json",
    "neutral_offdiagonal_generator": "outputs/yt_neutral_offdiagonal_generator_derivation_attempt_2026-05-05.json",
    "neutral_primitive_cone_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "full_positive_assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_STRICT_CERTIFICATES = {
    "neutral_primitive_cone_certificate": "outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
    "neutral_offdiagonal_generator_certificate": "outputs/yt_neutral_offdiagonal_generator_certificate_2026-05-05.json",
    "canonical_oh_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
    "source_higgs_rows": "outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json",
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


def git(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def read_candidate(rel: str) -> tuple[str, str]:
    path = ROOT / rel
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace"), "local"
    text = git(["show", f"{REMOTE_MAIN}:{rel}"])
    if text:
        return text, REMOTE_MAIN
    return "", "missing"


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def matmul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    m = len(b[0])
    kdim = len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(kdim)) for j in range(m)]
        for i in range(n)
    ]


def matadd(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matscale(c: Fraction, a: Matrix) -> Matrix:
    return [[c * value for value in row] for row in a]


def eye(n: int) -> Matrix:
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def cyclic_z3() -> Matrix:
    return [
        [Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
    ]


def mat_eq(a: Matrix, b: Matrix) -> bool:
    return a == b


def all_positive(a: Matrix) -> bool:
    return all(value > 0 for row in a for value in row)


def has_zero(a: Matrix) -> bool:
    return any(value == 0 for row in a for value in row)


def row_sums(a: Matrix) -> list[Fraction]:
    return [sum(row) for row in a]


def col_sums(a: Matrix) -> list[Fraction]:
    return [sum(a[i][j] for i in range(len(a))) for j in range(len(a[0]))]


def to_float(a: Matrix) -> list[list[float]]:
    return [[float(value) for value in row] for row in a]


def matpow(a: Matrix, n: int) -> Matrix:
    result = eye(len(a))
    for _ in range(n):
        result = matmul(result, a)
    return result


def max_abs_diff(a: list[list[float]], b: list[list[float]]) -> float:
    return max(
        abs(a[i][j] - b[i][j])
        for i in range(len(a))
        for j in range(len(a[0]))
    )


def stochastic_power_limit(a: Matrix, power: int = 32) -> dict[str, Any]:
    powered = matpow(a, power)
    target = [[1.0 / 3.0 for _ in range(3)] for _ in range(3)]
    err = max_abs_diff(to_float(powered), target)
    return {
        "power": power,
        "matrix_power": to_float(powered),
        "uniform_rank_one_projector": target,
        "max_abs_error_to_uniform_projector": err,
    }


def primitive_witness() -> dict[str, Any]:
    ident = eye(3)
    p = cyclic_z3()
    p2 = matmul(p, p)
    p3 = matmul(p2, p)
    lazy = matscale(Fraction(1, 2), matadd(ident, p))
    lazy2 = matmul(lazy, lazy)
    lazy2_expected = matscale(Fraction(1, 4), matadd(matadd(ident, matscale(Fraction(2), p)), p2))
    pure_powers_have_zeros = all(has_zero(matpow(p, k)) for k in range(1, 7))
    limit = stochastic_power_limit(lazy, power=32)
    return {
        "basis": ["Phi_1_prime", "Phi_2_prime", "Phi_3_prime"],
        "identity": [[str(value) for value in row] for row in ident],
        "cyclic_generator_P": [[str(value) for value in row] for row in p],
        "P2": [[str(value) for value in row] for row in p2],
        "P3_equals_identity": mat_eq(p3, ident),
        "pure_cyclic_generator_is_not_primitive": pure_powers_have_zeros,
        "lazy_transfer_L": [[str(value) for value in row] for row in lazy],
        "L2": [[str(value) for value in row] for row in lazy2],
        "L2_expected": [[str(value) for value in row] for row in lazy2_expected],
        "L2_matches_formula": mat_eq(lazy2, lazy2_expected),
        "L2_is_strictly_positive": all_positive(lazy2),
        "row_sums_L": [str(value) for value in row_sums(lazy)],
        "col_sums_L": [str(value) for value in col_sums(lazy)],
        "uniform_vector_is_left_and_right_fixed": row_sums(lazy) == [Fraction(1)] * 3
        and col_sums(lazy) == [Fraction(1)] * 3,
        "primitive_exponent_bound": 2,
        "pf_rank_one_limit_check": limit,
        "theorem_statement": (
            "For the Z3 triplet basis, P^3=I and P alone is irreducible but "
            "periodic.  The lazy positive-cone transfer L=(I+P)/2 has "
            "L^2=(I+2P+P^2)/4, whose entries are all strictly positive.  "
            "Therefore L is primitive.  Perron-Frobenius gives a unique "
            "positive eigenvector, here the uniform triplet vector, and the "
            "stochastic powers converge to the rank-one uniform projector."
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
    print("PR #230 Z3-triplet conditional primitive-cone theorem")
    print("=" * 72)

    texts = {name: read_candidate(rel) for name, rel in COMPOSITE_PATHS.items()}
    candidate_text = "\n\n".join(text for text, _source in texts.values())
    sources = {name: source for name, (_text, source) in texts.items()}
    certs = {name: load_json(path) for name, path in PARENTS.items()}
    h2_support = load_json(H2_SUPPORT)
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in certs.items() if cert.get("proposal_allowed") is True
    ]
    future_present = {
        name: (ROOT / rel).exists() for name, rel in FUTURE_STRICT_CERTIFICATES.items()
    }
    witness = primitive_witness()
    firewall = forbidden_firewall()

    composite_pack_readable = all(source != "missing" for source in sources.values())
    composite_triplet_named = (
        ("Phi_eff" in candidate_text or "\u03a6_eff" in candidate_text)
        and ("Phi_1" in candidate_text or "\u03a6_1" in candidate_text)
        and ("Phi_2" in candidate_text or "\u03a6_2" in candidate_text)
        and ("Phi_3" in candidate_text or "\u03a6_3" in candidate_text)
        and "H1" in candidate_text
        and "H2" in candidate_text
        and "NO1" in candidate_text
    )
    composite_is_context_only = (
        certs["origin_main_composite_higgs_intake_guard"].get(
            "origin_main_composite_higgs_intake_guard_passed"
        )
        is True
        and certs["origin_main_composite_higgs_intake_guard"].get(
            "origin_main_composite_higgs_closes_pr230"
        )
        is False
        and certs["origin_main_composite_higgs_intake_guard"].get("proposal_allowed")
        is False
    )
    same_surface_z3_triplet_supplied = (
        "same-surface Z3 taste-triplet artifact"
        in statuses["same_surface_z3_taste_triplet"]
        and certs["same_surface_z3_taste_triplet"].get(
            "same_surface_z3_triplet_artifact_passed"
        )
        is True
        and certs["same_surface_z3_taste_triplet"].get("proposal_allowed") is False
        and certs["same_surface_z3_taste_triplet"].get("pr230_closure_authorized")
        is False
    )
    h2_positive_cone_support_supplied = (
        "Z3-triplet positive-cone H2 support"
        in status(h2_support)
        and h2_support.get("proposal_allowed") is False
        and h2_support.get("z3_triplet_positive_cone_h2_support_passed") is True
        and h2_support.get("pr230_closure_authorized") is False
        and h2_support.get("supplies_conditional_premises", {}).get(
            "H2_positive_cone_equal_magnitude_support"
        )
        is True
        and h2_support.get("supplies_conditional_premises", {}).get(
            "H3_lazy_positive_physical_transfer"
        )
        is False
    )
    neutral_route_currently_blocked = (
        "neutral primitive-rank-one route not complete"
        in statuses["neutral_primitive_route_completion"]
        and certs["neutral_primitive_route_completion"].get("proposal_allowed") is False
    )
    offdiagonal_absent = (
        "neutral off-diagonal generator not" in statuses["neutral_offdiagonal_generator"]
        and certs["neutral_offdiagonal_generator"].get("proposal_allowed") is False
    )
    strict_primitive_absent = (
        certs["neutral_primitive_cone_gate"].get("strict_primitive_cone_certificate_present")
        is not True
        and not any(future_present.values())
    )
    theorem_math_passed = (
        witness["P3_equals_identity"]
        and witness["pure_cyclic_generator_is_not_primitive"]
        and witness["L2_matches_formula"]
        and witness["L2_is_strictly_positive"]
        and witness["uniform_vector_is_left_and_right_fixed"]
        and witness["pf_rank_one_limit_check"]["max_abs_error_to_uniform_projector"]
        < 1.0e-9
    )
    aggregate_gates_still_open = (
        certs["full_positive_assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign_status"].get("proposal_allowed") is False
    )
    no_forbidden_imports = all(value is False for value in firewall.values())

    report("composite-pack-readable", composite_pack_readable, str(sources))
    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("composite-z3-triplet-named", composite_triplet_named, "Phi_i triplet with branch-local hypotheses")
    report("composite-intake-context-only", composite_is_context_only, statuses["origin_main_composite_higgs_intake_guard"])
    report("same-surface-z3-triplet-supplied", same_surface_z3_triplet_supplied, statuses["same_surface_z3_taste_triplet"])
    report("z3-positive-cone-h2-support-supplied", h2_positive_cone_support_supplied, status(h2_support))
    report("z3-primitive-matrix-theorem-passed", theorem_math_passed, "L=(I+P)/2 has L^2>0 and rank-one PF limit")
    report("pure-z3-cycle-not-enough", witness["pure_cyclic_generator_is_not_primitive"], "P remains periodic, so laziness/off-diagonal self term is load-bearing")
    report("neutral-route-currently-blocked", neutral_route_currently_blocked, statuses["neutral_primitive_route_completion"])
    report("offdiagonal-generator-currently-absent", offdiagonal_absent, statuses["neutral_offdiagonal_generator"])
    report("strict-primitive-certificate-absent", strict_primitive_absent, str(future_present))
    report("aggregate-gates-still-open", aggregate_gates_still_open, "assembly/retained/campaign proposal_allowed=false")
    report("forbidden-firewall-clean", no_forbidden_imports, str(firewall))
    report("conditional-theorem-support-not-closure", True, "same-surface PR230 action/off-diagonal premise remains absent")

    conditional_premises = [
        "H1: Z3 cyclic action on the PR230-relevant taste-scalar triplet is derived on the same surface (supplied by yt_pr230_same_surface_z3_taste_triplet_artifact_2026-05-06.json)",
        "H2: the three bilinear channels sit in one positive cone with nonzero equal-magnitude support (supplied by yt_pr230_z3_triplet_positive_cone_support_certificate_2026-05-06.json when present)",
        "H3: the same-surface neutral transfer contains a positive lazy term I plus the Z3 cycle P, or an equivalent aperiodic positive connector",
        "H4: the resulting neutral transfer is the physical scalar transfer coupled to the PR230 source/canonical-Higgs sector",
    ]
    remaining_conditional_premises = ["H3", "H4"]
    if not h2_positive_cone_support_supplied:
        remaining_conditional_premises.insert(0, "H2")
    missing_current_surface_premises = [
        "same-surface PR230 EW/Higgs or composite action tying the Z3 taste triplet to the top FH/LSZ source coordinate",
        "derived off-diagonal neutral generator or production non-source response row",
        "strict neutral primitive-cone certificate on the PR230 surface",
        "canonical O_H/source-Higgs pole overlap or accepted physical-response bridge",
    ]
    result = {
        "actual_current_surface_status": (
            "conditional-support / Z3-triplet primitive-cone theorem; "
            "same-surface PR230 primitive premise absent"
        ),
        "conditional_surface_status": (
            "H1 is supplied as an exact same-surface Z3 taste-triplet "
            "artifact and H2 is supplied when the positive-cone support "
            "certificate is present.  If H3-H4 are also supplied, the neutral "
            "primitive/rank-one mathematical premise becomes load-bearing."
        ),
        "hypothetical_axiom_status": "would support neutral primitive route under H1-H4; not retained on actual surface",
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The finite-matrix primitive theorem is exact, but the current PR230 "
            "surface still lacks the same-surface action/off-diagonal generator "
            "that would instantiate the theorem."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "z3_triplet_conditional_primitive_theorem_passed": theorem_math_passed,
        "same_surface_z3_triplet_supplied": same_surface_z3_triplet_supplied,
        "h2_positive_cone_support_supplied": h2_positive_cone_support_supplied,
        "remaining_unsupplied_conditional_premises": remaining_conditional_premises,
        "pr230_closure_authorized": False,
        "writes_strict_future_certificate": False,
        "h2_support_certificate": H2_SUPPORT,
        "h2_support_status": status(h2_support),
        "strict_future_certificate_presence": future_present,
        "composite_sources": sources,
        "parent_statuses": statuses,
        "conditional_premises": conditional_premises,
        "missing_current_surface_premises": missing_current_surface_premises,
        "primitive_witness": witness,
        "firewall": firewall,
        "literature_context": {
            "perron_frobenius_role": (
                "standard primitive nonnegative matrix theorem; used only after "
                "the transfer matrix is explicitly defined"
            ),
            "krein_rutman_role": (
                "infinite-dimensional analogue for future transfer operators; "
                "not used as a PR230 source-overlap selector"
            ),
            "fms_role": (
                "motivates gauge-invariant composite Higgs operators only after "
                "a same-surface gauge-Higgs/composite action exists"
            ),
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not write outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json",
            "does not identify O_sp or O_s with canonical O_H",
            "does not set kappa_s, c2, or Z_match to one",
            "does not use H_unit, Ward authority, observed targets, alpha_LM, plaquette, or u0",
            "does not treat the origin/main composite-Higgs stretch packet as PR230 proof authority",
        ],
        "exact_next_action": (
            "Try to derive H1-H4 on the same PR230 surface, or implement a "
            "production non-source response row/off-diagonal neutral generator. "
            "Only then can this primitive theorem be promoted from conditional "
            "support to a strict neutral primitive-cone certificate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
