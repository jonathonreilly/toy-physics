#!/usr/bin/env python3
"""
PR #230 neutral-scalar primitive-cone certificate gate.

This runner turns the neutral-rank route into an executable positive
certificate contract.  It does not prove irreducibility on the current surface.
It checks exactly what a future same-surface neutral-scalar primitive-cone
certificate must supply before the existing conditional Perron/rank-one
support can be used for PR #230.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json"
FUTURE_CERTIFICATE = (
    ROOT / "outputs" / "yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json"
)

PARENTS = {
    "positivity_improving_neutral_scalar_rank_one": (
        "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json"
    ),
    "neutral_scalar_positivity_improving_direct_closure": (
        "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json"
    ),
    "neutral_scalar_irreducibility_authority": (
        "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json"
    ),
    "neutral_scalar_commutant_rank_no_go": (
        "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json"
    ),
    "neutral_scalar_dynamical_rank_one": (
        "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json"
    ),
    "neutral_scalar_top_coupling_tomography": (
        "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json"
    ),
    "non_source_response_rank_repair": (
        "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json"
    ),
}

FORBIDDEN_TEXT_FRAGMENTS = (
    "H_unit",
    "yt_ward_identity",
    "YT_WARD_IDENTITY_DERIVATION_THEOREM",
    "observed top mass",
    "observed y_t",
    "alpha_LM",
    "plaquette",
    "u0",
    "cos(theta)=1",
    "kappa_s=1",
)

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        out: list[str] = []
        for child in value.values():
            out.extend(string_values(child))
        return out
    if isinstance(value, list):
        out = []
        for child in value:
            out.extend(string_values(child))
        return out
    return []


def forbidden_fragment_present(candidate: dict[str, Any]) -> list[str]:
    encoded_values = "\n".join(string_values(candidate))
    return [fragment for fragment in FORBIDDEN_TEXT_FRAGMENTS if fragment in encoded_values]


def as_square_matrix(value: Any) -> np.ndarray | None:
    try:
        matrix = np.asarray(value, dtype=float)
    except (TypeError, ValueError):
        return None
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] == 0:
        return None
    if not np.all(np.isfinite(matrix)):
        return None
    return matrix


def strongly_connected(matrix: np.ndarray, tolerance: float = 1.0e-12) -> bool:
    n = matrix.shape[0]
    graph = [[j for j in range(n) if matrix[i, j] > tolerance] for i in range(n)]
    reverse = [[i for i in range(n) if matrix[i, j] > tolerance] for j in range(n)]

    def reachable(adjacency: list[list[int]], start: int) -> set[int]:
        seen = {start}
        queue: deque[int] = deque([start])
        while queue:
            node = queue.popleft()
            for child in adjacency[node]:
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
        return seen

    return len(reachable(graph, 0)) == n and len(reachable(reverse, 0)) == n


def primitive_power_positive(matrix: np.ndarray, tolerance: float = 1.0e-12) -> dict[str, Any]:
    n = matrix.shape[0]
    power = np.array(matrix, dtype=float)
    max_power = max(1, n * n - 2 * n + 2)
    for exponent in range(1, max_power + 1):
        if np.all(power > tolerance):
            return {"positive": True, "first_positive_power": exponent}
        power = power @ matrix
    return {"positive": False, "first_positive_power": None}


def witness_family() -> dict[str, Any]:
    primitive = np.asarray([[0.62, 0.18], [0.11, 0.71]], dtype=float)
    reducible = np.asarray([[0.91, 0.0], [0.0, 0.88]], dtype=float)
    return {
        "primitive_positive_example": {
            "matrix": primitive.tolist(),
            "nonnegative": bool(np.all(primitive >= 0.0)),
            "strongly_connected": strongly_connected(primitive),
            "primitive_power": primitive_power_positive(primitive),
            "interpretation": (
                "This is the shape a future neutral transfer certificate must "
                "have before Perron/rank-one support can become load-bearing."
            ),
        },
        "reducible_positive_counterexample": {
            "matrix": reducible.tolist(),
            "nonnegative": bool(np.all(reducible >= 0.0)),
            "strongly_connected": strongly_connected(reducible),
            "primitive_power": primitive_power_positive(reducible),
            "interpretation": (
                "This preserves positivity but leaves two invariant neutral "
                "directions, matching the current obstruction."
            ),
        },
    }


def validate_future_certificate(candidate: dict[str, Any]) -> dict[str, bool]:
    matrix = as_square_matrix(candidate.get("neutral_transfer_matrix"))
    primitive_checks = primitive_power_positive(matrix) if matrix is not None else {"positive": False}
    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall"), dict) else {}
    source_overlap = float(candidate.get("source_pole_overlap", 0.0) or 0.0)
    higgs_overlap = float(candidate.get("canonical_higgs_overlap", 0.0) or 0.0)
    return {
        "certificate_kind": candidate.get("certificate_kind")
        == "neutral_scalar_primitive_cone_certificate",
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "neutral_sector_basis_declared": isinstance(candidate.get("neutral_sector_basis"), list)
        and len(candidate.get("neutral_sector_basis", [])) >= 1,
        "transfer_matrix_square": matrix is not None,
        "transfer_matrix_nonnegative": matrix is not None and bool(np.all(matrix >= -1.0e-12)),
        "transfer_graph_strongly_connected": matrix is not None and strongly_connected(matrix),
        "primitive_power_positive": bool(primitive_checks.get("positive")),
        "isolated_lowest_neutral_pole_certified": candidate.get("isolated_lowest_neutral_pole_certified")
        is True,
        "source_pole_overlap_positive": source_overlap > 0.0,
        "canonical_higgs_overlap_positive": higgs_overlap > 0.0,
        "orthogonal_neutral_null_certified": candidate.get("orthogonal_neutral_null_certified") is True,
        "no_observed_selector": firewall.get("used_observed_targets_as_selectors") is False,
        "no_hunit_or_ward_authority": firewall.get("used_hunit_or_ward_authority") is False,
        "no_alpha_lm_or_plaquette": firewall.get("used_alpha_lm_or_plaquette") is False,
        "no_unit_or_cosine_shortcut": firewall.get("set_unit_overlap_or_normalization") is False,
        "no_forbidden_text_fragments": not forbidden_fragment_present(candidate),
    }


def main() -> int:
    print("PR #230 neutral-scalar primitive-cone certificate gate")
    print("=" * 72)

    parents = {name: load_json(ROOT / rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    statuses = {name: status(cert) for name, cert in parents.items()}
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = witness_family()
    future = load_json(FUTURE_CERTIFICATE)
    future_checks = validate_future_certificate(future) if future else {}
    failed_future_checks = [name for name, ok in future_checks.items() if not ok]
    future_gate_passed = bool(future) and not failed_future_checks

    report("parents-loaded", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report(
        "conditional-perron-rank-one-support-loaded",
        "positivity-improving neutral-scalar rank-one theorem"
        in statuses["positivity_improving_neutral_scalar_rank_one"],
        statuses["positivity_improving_neutral_scalar_rank_one"],
    )
    report(
        "direct-neutral-irreducibility-currently-blocked",
        "not derived" in statuses["neutral_scalar_positivity_improving_direct_closure"],
        statuses["neutral_scalar_positivity_improving_direct_closure"],
    )
    report(
        "authority-audit-currently-absent",
        parents["neutral_scalar_irreducibility_authority"].get(
            "neutral_scalar_irreducibility_certificate_present"
        )
        is False,
        statuses["neutral_scalar_irreducibility_authority"],
    )
    report(
        "primitive-positive-example-passes",
        witness["primitive_positive_example"]["strongly_connected"]
        and witness["primitive_positive_example"]["primitive_power"]["positive"],
        "synthetic primitive cone",
    )
    report(
        "reducible-positive-counterexample-rejected",
        witness["reducible_positive_counterexample"]["strongly_connected"] is False
        and witness["reducible_positive_counterexample"]["primitive_power"]["positive"] is False,
        "positive preserving is not enough",
    )
    report(
        "future-primitive-cone-certificate-absent",
        not future,
        str(FUTURE_CERTIFICATE.relative_to(ROOT)),
    )
    if future:
        report(
            "future-primitive-cone-certificate-valid",
            future_gate_passed,
            f"failed={failed_future_checks}",
        )
    report(
        "current-surface-does-not-close-neutral-rank-one",
        not future_gate_passed,
        f"future_gate_passed={future_gate_passed}",
    )
    report("does-not-authorize-proposed-retained", True, "primitive-cone gate is a future contract only")

    result = {
        "actual_current_surface_status": (
            "exact-support / neutral-scalar primitive-cone certificate gate; "
            "strict irreducibility certificate absent"
        ),
        "verdict": (
            "The neutral-rank route now has an executable positive contract.  "
            "A future same-surface primitive-cone certificate must prove a "
            "nonnegative strongly connected neutral transfer matrix with a "
            "positive primitive power, an isolated lowest neutral pole, positive "
            "source and canonical-Higgs overlaps, and a forbidden-import "
            "firewall.  The current surface has only conditional Perron support "
            "and no such certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No strict same-surface neutral-scalar primitive-cone / "
            "irreducibility certificate is present."
        ),
        "bare_retained_allowed": False,
        "primitive_cone_certificate_gate_passed": future_gate_passed,
        "future_certificate": str(FUTURE_CERTIFICATE.relative_to(ROOT)),
        "future_certificate_checks": future_checks,
        "future_certificate_missing_or_failed_checks": failed_future_checks,
        "parent_certificates": PARENTS,
        "witness_family": witness,
        "acceptance_contract": {
            "certificate_kind": "neutral_scalar_primitive_cone_certificate",
            "required_fields": [
                "same_surface_cl3_z3",
                "neutral_sector_basis",
                "neutral_transfer_matrix",
                "isolated_lowest_neutral_pole_certified",
                "source_pole_overlap > 0",
                "canonical_higgs_overlap > 0",
                "orthogonal_neutral_null_certified",
                "firewall.used_observed_targets_as_selectors == false",
                "firewall.used_hunit_or_ward_authority == false",
                "firewall.used_alpha_lm_or_plaquette == false",
                "firewall.set_unit_overlap_or_normalization == false",
            ],
            "mathematical_checks": [
                "neutral_transfer_matrix is square and nonnegative",
                "directed positive-entry graph is strongly connected",
                "some finite matrix power is strictly positive",
            ],
        },
        "strict_non_claims": [
            "does not claim neutral rank-one closure",
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not infer irreducibility from reflection positivity, gauge Perron, symmetry labels, or source-only rows",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, u0, observed targets, or unit-overlap shortcuts",
        ],
        "exact_next_action": (
            "Either supply the strict neutral primitive-cone certificate, measure "
            "same-surface O_H/C_sH/C_HH or W/Z rows, provide Schur A/B/C kernel "
            "rows, or continue scalar-LSZ production toward a certified physical "
            "readout."
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
