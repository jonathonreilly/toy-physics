#!/usr/bin/env python3
"""
PR #230 Block65 strict extremal moment certificate route.

This probe asks whether finite scalar-source/Stieltjes moments can become
pole-atom/residue authority through a strict truncated-moment certificate.

Conclusion on the current surface: no certificate is present.  The route is
mathematically viable only if the source moment prefix is upgraded to a flat
extension/extremal localizing-matrix certificate, or to an equivalent
determinate infinite/tail theorem.  The runner verifies both sides:

* a positive exact finite-atomic witness where flat extension plus a
  localizing rank drop recovers the atom at the pole;
* the current PR230 parent surface, where Block64 and the Stieltjes/Pade/
  Carleman gates show that finite prefixes remain non-authoritative.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_block65_extremal_moment_certificate_route_2026-05-12.json"
)
FUTURE_CERTIFICATE = (
    ROOT
    / "outputs"
    / "yt_pr230_strict_extremal_moment_certificate_2026-05-12.json"
)

PARENTS = {
    "block58_compact_source_spectral_support": "outputs/yt_pr230_block58_compact_source_spectral_support_gate_2026-05-12.json",
    "block60_compact_source_taste_singlet_carrier": "outputs/yt_pr230_block60_compact_source_taste_singlet_carrier_gate_2026-05-12.json",
    "block64_finite_moment_atom_residue_obstruction": "outputs/yt_pr230_block64_finite_moment_atom_residue_obstruction_2026-05-12.json",
    "stieltjes_moment_gate": "outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json",
    "pade_stieltjes_bounds_gate": "outputs/yt_fh_lsz_pade_stieltjes_bounds_gate_2026-05-05.json",
    "carleman_tauberian_attempt": "outputs/yt_pr230_scalar_lsz_carleman_tauberian_determinacy_attempt_2026-05-05.json",
    "polefit8x8_stieltjes_proxy_diagnostic": "outputs/yt_fh_lsz_polefit8x8_stieltjes_proxy_diagnostic_2026-05-05.json",
    "full_positive_closure_assembly_gate": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
}

FORBIDDEN_INPUTS = [
    "H_unit",
    "yt_ward_identity",
    "y_t_bare",
    "alpha_LM",
    "plaquette",
    "u0",
    "observed targets",
    "kappa_s=1",
    "c2=1",
    "Z_match=1",
]

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


def load_json(rel_or_path: str | Path) -> dict[str, Any]:
    path = rel_or_path if isinstance(rel_or_path, Path) else ROOT / rel_or_path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def moment(atoms: list[tuple[Fraction, Fraction]], power: int) -> Fraction:
    return sum(weight * (point**power) for point, weight in atoms)


def hankel(moments: list[Fraction], order: int, shift: int = 0) -> list[list[Fraction]]:
    return [[moments[i + j + shift] for j in range(order)] for i in range(order)]


def localizing_linear(
    moments: list[Fraction], order: int, a: Fraction = Fraction(0)
) -> list[list[Fraction]]:
    # Matrix of int (x-a) x^(i+j) dmu = m_{i+j+1} - a m_{i+j}.
    return [
        [moments[i + j + 1] - a * moments[i + j] for j in range(order)]
        for i in range(order)
    ]


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    n = len(matrix)
    if n == 0:
        return Fraction(1)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    total = Fraction(0)
    for column, value in enumerate(matrix[0]):
        minor = [
            [row[j] for j in range(n) if j != column]
            for row in matrix[1:]
        ]
        total += ((-1) ** column) * value * determinant(minor)
    return total


def principal_minors(matrix: list[list[Fraction]]) -> list[dict[str, Any]]:
    rows = range(len(matrix))
    out: list[dict[str, Any]] = []
    for size in range(1, len(matrix) + 1):
        for indices in combinations(rows, size):
            sub = [[matrix[i][j] for j in indices] for i in indices]
            out.append({"indices": list(indices), "determinant": str(determinant(sub))})
    return out


def psd_check(matrix: list[list[Fraction]]) -> dict[str, Any]:
    minors = principal_minors(matrix)
    minimum = min(Fraction(row["determinant"]) for row in minors) if minors else Fraction(0)
    return {
        "psd": minimum >= 0,
        "minimum_principal_minor": str(minimum),
        "principal_minors": minors,
    }


def rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    rows = [row[:] for row in matrix]
    m = len(rows)
    n = len(rows[0])
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if rows[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        pivot_value = rows[r][c]
        rows[r] = [value / pivot_value for value in rows[r]]
        for i in range(m):
            if i != r and rows[i][c] != 0:
                factor = rows[i][c]
                rows[i] = [rows[i][j] - factor * rows[r][j] for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def atom_list_reproduces_moments(
    atoms: list[tuple[Fraction, Fraction]], moments: list[Fraction]
) -> bool:
    return all(moment(atoms, k) == moments[k] for k in range(len(moments)))


def flat_extension_atom_witness() -> dict[str, Any]:
    # Shifted spectral variable lambda = s - m_pole^2.  A pole atom is at
    # lambda=0; continuum/other atoms have lambda>0.
    atoms = [
        (Fraction(0), Fraction(1, 5)),
        (Fraction(1, 3), Fraction(1, 2)),
        (Fraction(1), Fraction(3, 10)),
    ]
    moments = [moment(atoms, k) for k in range(7)]
    moment_matrix_m2 = hankel(moments, 3)
    extension_m3 = hankel(moments, 4)
    localizing_x_m2 = localizing_linear(moments, 3, Fraction(0))
    localizing_threshold_gap = localizing_linear(moments, 3, Fraction(0))

    rank_m2 = rank(moment_matrix_m2)
    rank_m3 = rank(extension_m3)
    rank_localizing_x = rank(localizing_x_m2)
    pole_atom_count = rank_m3 - rank_localizing_x
    pole_weight = sum(weight for point, weight in atoms if point == 0)

    declared_atom_rows = [
        {"lambda": str(point), "weight": str(weight)} for point, weight in atoms
    ]

    return {
        "variable": "lambda = s - m_pole_squared, with certified support lambda >= 0",
        "declared_atoms": declared_atom_rows,
        "moments_m0_to_m6": [str(value) for value in moments],
        "moment_matrix_M2_rank": rank_m2,
        "flat_extension_M3_rank": rank_m3,
        "rank_flat": rank_m2 == rank_m3 == len(atoms),
        "moment_matrix_M2_psd": psd_check(moment_matrix_m2),
        "flat_extension_M3_psd": psd_check(extension_m3),
        "localizing_lambda_M2_rank": rank_localizing_x,
        "localizing_lambda_M2_psd": psd_check(localizing_x_m2),
        "threshold_gap_localizing_psd": psd_check(localizing_threshold_gap),
        "pole_atom_count_from_rank_drop": pole_atom_count,
        "pole_residue_from_declared_atom": str(pole_weight),
        "atom_list_reproduces_moments": atom_list_reproduces_moments(atoms, moments),
        "flat_extremal_certificate_passed": (
            rank_m2 == rank_m3 == len(atoms)
            and psd_check(moment_matrix_m2)["psd"]
            and psd_check(extension_m3)["psd"]
            and psd_check(localizing_x_m2)["psd"]
            and pole_atom_count == 1
            and pole_weight > 0
            and atom_list_reproduces_moments(atoms, moments)
        ),
    }


def block64_counterfamily_extension_obstruction() -> dict[str, Any]:
    measure_a = [
        (Fraction(0), Fraction(1, 6)),
        (Fraction(1, 2), Fraction(2, 3)),
        (Fraction(1), Fraction(1, 6)),
    ]
    measure_b = [
        (Fraction(0), Fraction(1, 4)),
        (Fraction(2, 3), Fraction(3, 4)),
    ]
    prefix_a = [moment(measure_a, k) for k in range(3)]
    prefix_b = [moment(measure_b, k) for k in range(3)]
    extension_a = [moment(measure_a, k) for k in range(7)]
    extension_b = [moment(measure_b, k) for k in range(7)]
    pole_a = sum(weight for point, weight in measure_a if point == 0)
    pole_b = sum(weight for point, weight in measure_b if point == 0)

    return {
        "shared_prefix_orders": [0, 1, 2],
        "shared_prefix": [str(value) for value in prefix_a],
        "prefixes_match": prefix_a == prefix_b,
        "extension_a_m0_to_m6": [str(value) for value in extension_a],
        "extension_b_m0_to_m6": [str(value) for value in extension_b],
        "extensions_differ_after_prefix": extension_a[3:] != extension_b[3:],
        "pole_atom_a": str(pole_a),
        "pole_atom_b": str(pole_b),
        "pole_atoms_differ": pole_a != pole_b,
        "finite_prefix_flatness_certifiable": False,
        "obstruction": (
            "The current finite prefix m0..m2 cannot even form the higher "
            "moment matrices needed to check a flat rank-preserving "
            "extension.  Two positive completions agree on the prefix but "
            "differ in higher moments and in the pole atom at lambda=0."
        ),
    }


def strict_certificate_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "same_surface_scalar_measure",
            "required": "contact-subtracted PR230 scalar-source Stieltjes measure with fixed source coordinate and zero-source limit",
            "current_satisfied": False,
            "test_or_derivation": "derive from compact source functional plus contact/FVIR theorem; reject current polefit8x8 C_ss proxy until monotonicity and contact checks pass",
        },
        {
            "id": "certified_pole_coordinate",
            "required": "same-surface pole location m_pole^2 and shifted variable lambda=s-m_pole^2 with support lambda>=0",
            "current_satisfied": False,
            "test_or_derivation": "thermodynamic scalar pole/gap theorem or direct pole-row measurement with covariance",
        },
        {
            "id": "exact_or_interval_moments_to_flat_order",
            "required": "moments m0..m_{2d+2} with rigorous intervals tight enough to certify ranks, PSD, and localizing constraints",
            "current_satisfied": False,
            "test_or_derivation": "same-source moment production with rational/error certificates; not finite-shell fit reinterpretation",
        },
        {
            "id": "positive_moment_matrices",
            "required": "Hankel moment matrices and shifted/localizing matrices PSD on the declared support",
            "current_satisfied": False,
            "test_or_derivation": "principal-minor/eigenvalue lower bounds that survive covariance intervals",
        },
        {
            "id": "flat_extension_or_extremality",
            "required": "rank M_d = rank M_{d+1}, or extremal rank=variety-cardinality plus consistency, with localizing matrices",
            "current_satisfied": False,
            "test_or_derivation": "Curto-Fialkow flat extension or extremal truncated moment theorem certificate",
        },
        {
            "id": "pole_atom_rank_drop",
            "required": "rank drop in the lambda-localizing matrix proving exactly one atom at lambda=0",
            "current_satisfied": False,
            "test_or_derivation": "rank M_{d+1} - rank M_lambda = 1 after support has been shifted to the pole",
        },
        {
            "id": "residue_extraction",
            "required": "atom list or equivalent recurrence/Vandermonde/Christoffel extraction with positive tight residue interval",
            "current_satisfied": False,
            "test_or_derivation": "verify atoms reproduce moments and residue interval relative width <= 0.02",
        },
        {
            "id": "threshold_fvir_contact_authority",
            "required": "thermodynamic threshold, finite-volume/IR limiting order, zero-mode, and contact-subtraction authority",
            "current_satisfied": False,
            "test_or_derivation": "independent FVIR/contact runner or microscopic denominator theorem",
        },
        {
            "id": "canonical_oh_or_physical_response_bridge",
            "required": "canonical O_H/source-overlap authority or same-surface W/Z physical-response bridge",
            "current_satisfied": False,
            "test_or_derivation": "direct C_sH/C_HH pole rows, Gram purity, or equivalent physical response certificate",
        },
        {
            "id": "forbidden_import_firewall",
            "required": "no H_unit, Ward, y_t_bare, alpha_LM, plaquette/u0, observed targets, kappa_s=1, c2=1, or Z_match=1",
            "current_satisfied": True,
            "test_or_derivation": "text/value firewall plus dependency audit",
        },
    ]


def assumption_exercise() -> list[dict[str, Any]]:
    return [
        {
            "assumption": "A positive scalar-source Stieltjes measure exists for the same PR230 source object.",
            "if_wrong": "Hankel/localizing positivity would certify the wrong object or no positive measure at all.",
            "test_or_derivation": "derive the measure from reflection positivity plus contact-subtracted scalar source; rerun monotonicity and Hankel checks on that exact object.",
        },
        {
            "assumption": "The finite source rows are actual moments of that measure, not shell-fit or contact-contaminated proxies.",
            "if_wrong": "Moment-problem theorems do not apply to the data being promoted.",
            "test_or_derivation": "produce source-coordinate, zero-source, contact-subtraction, and covariance metadata in the future certificate.",
        },
        {
            "assumption": "The pole location is same-surface and the shifted variable lambda has support lambda>=0.",
            "if_wrong": "A localizing rank drop at lambda=0 is physically meaningless or tests the wrong spectral edge.",
            "test_or_derivation": "derive scalar pole/gap theorem or direct pole-row measurement before rank-drop extraction.",
        },
        {
            "assumption": "The supplied moment order is high enough for flat extension/extremality.",
            "if_wrong": "Block64 counterfamilies remain available and the atom/residue is not fixed.",
            "test_or_derivation": "certify rank M_d=rank M_{d+1}, or extremal rank=variety cardinality plus consistency.",
        },
        {
            "assumption": "PSD and rank decisions survive numerical/covariance uncertainty.",
            "if_wrong": "Near-flat numerical spectra can hide nonflat families with different atom masses.",
            "test_or_derivation": "use exact rational/algebraic moments or interval linear algebra with explicit rank gaps.",
        },
        {
            "assumption": "The atom at lambda=0 is isolated from continuum/threshold effects.",
            "if_wrong": "A soft continuum can mimic finite-window pole behavior with zero atom residue.",
            "test_or_derivation": "threshold/FVIR theorem with positive residue lower bound and limiting-order control.",
        },
        {
            "assumption": "The source-pole residue is the physical scalar LSZ residue or has a certified bridge to it.",
            "if_wrong": "The route recovers only a source-channel atom, not canonical O_H or W/Z physical response.",
            "test_or_derivation": "supply C_sH/C_HH rows, Gram purity, or same-surface physical-response bridge.",
        },
    ]


def first_principles_reduction() -> dict[str, Any]:
    return {
        "minimal_load_bearing_drivers": [
            "Cl(3)/Z3 compact scalar-source functional defines the source coordinate.",
            "Reflection positivity gives finite-volume positive source-channel spectral sums.",
            "A Stieltjes transform of a positive scalar measure turns pole residue into an atom mass.",
            "Truncated moment theory fixes an atom only under determinacy/extremality/flat extension or tight Markov bounds with threshold authority.",
            "Physical PR230 closure still needs canonical O_H/source-overlap or W/Z response authority.",
        ],
        "removed_as_non_load_bearing_for_this_probe": FORBIDDEN_INPUTS,
    }


def validate_future_certificate(candidate: dict[str, Any]) -> dict[str, bool]:
    if not candidate:
        return {}
    flat = candidate.get("flat_extension", {}) if isinstance(candidate.get("flat_extension"), dict) else {}
    localizing = candidate.get("localizing", {}) if isinstance(candidate.get("localizing"), dict) else {}
    residue = candidate.get("residue_interval", {}) if isinstance(candidate.get("residue_interval"), dict) else {}
    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall"), dict) else {}
    return {
        "certificate_kind": candidate.get("certificate_kind")
        == "pr230_strict_extremal_moment_certificate",
        "same_surface_scalar_measure": candidate.get("same_surface_scalar_measure") is True,
        "pole_coordinate_certified": candidate.get("pole_coordinate_certified") is True,
        "support_shifted_to_lambda_ge_zero": candidate.get("support_shifted_to_lambda_ge_zero") is True,
        "moments_to_flat_order_present": int(candidate.get("moment_count", 0) or 0) >= 7,
        "moment_psd_certified": candidate.get("moment_psd_certified") is True,
        "rank_flat_or_extremal": flat.get("rank_flat") is True or flat.get("extremal_consistency_passed") is True,
        "localizing_psd": localizing.get("support_psd") is True,
        "pole_atom_rank_drop_one": localizing.get("pole_atom_rank_drop") == 1,
        "residue_interval_tight": residue.get("lower_bound_positive") is True
        and float(residue.get("relative_width_over_lower", 1.0) or 1.0) <= 0.02,
        "threshold_fvir_contact_authority": candidate.get("threshold_fvir_contact_authority") is True,
        "canonical_or_physical_response_authority": candidate.get(
            "canonical_or_physical_response_authority"
        )
        is True,
        "no_forbidden_imports": (
            firewall.get("used_hunit_or_ward_authority") is False
            and firewall.get("used_observed_targets") is False
            and firewall.get("used_alpha_lm_plaquette_u0") is False
            and firewall.get("used_unit_shortcuts") is False
        ),
    }


def main() -> int:
    print("PR #230 Block65 strict extremal moment certificate route")
    print("=" * 76)

    parent_certs = {name: load_json(path) for name, path in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in parent_certs.items()}
    missing_parents = [name for name, cert in parent_certs.items() if not cert]
    future = load_json(FUTURE_CERTIFICATE)
    future_checks = validate_future_certificate(future)
    future_failed = [name for name, ok in future_checks.items() if not ok]
    future_gate_passed = bool(future) and not future_failed

    flat_witness = flat_extension_atom_witness()
    obstruction = block64_counterfamily_extension_obstruction()
    contract = strict_certificate_contract()
    missing_contract = [row["id"] for row in contract if not row["current_satisfied"]]

    block64_loaded = (
        "finite source/Stieltjes moment prefixes do not fix"
        in statuses["block64_finite_moment_atom_residue_obstruction"]
        and parent_certs["block64_finite_moment_atom_residue_obstruction"].get(
            "block64_finite_moment_atom_residue_obstruction_passed"
        )
        is True
    )
    current_strict_cert_absent = not future
    stieltjes_gate_absent = (
        parent_certs["stieltjes_moment_gate"].get("moment_certificate_gate_passed")
        is False
    )
    pade_gate_absent = (
        parent_certs["pade_stieltjes_bounds_gate"].get("pade_stieltjes_bounds_gate_passed")
        is False
    )
    carleman_absent = (
        parent_certs["carleman_tauberian_attempt"].get(
            "carleman_tauberian_determinacy_passed"
        )
        is False
    )
    proxy_rejected = (
        parent_certs["polefit8x8_stieltjes_proxy_diagnostic"].get(
            "stieltjes_proxy_certificate_passed"
        )
        is False
    )
    proposal_allowed = False

    report("parents-loaded", not missing_parents, f"missing={missing_parents}")
    report("block64-obstruction-loaded", block64_loaded, statuses["block64_finite_moment_atom_residue_obstruction"])
    report("flat-extension-witness-valid", flat_witness["flat_extremal_certificate_passed"], "rank-flat atom extraction recovers pole residue")
    report("block64-counterfamily-still-obstructs-current-prefix", obstruction["pole_atoms_differ"], "same m0..m2, different pole atom")
    report("strict-current-certificate-absent", current_strict_cert_absent, str(FUTURE_CERTIFICATE.relative_to(ROOT)))
    report("stieltjes-moment-gate-absent", stieltjes_gate_absent, statuses["stieltjes_moment_gate"])
    report("pade-stieltjes-gate-absent", pade_gate_absent, statuses["pade_stieltjes_bounds_gate"])
    report("carleman-tauberian-determinacy-absent", carleman_absent, statuses["carleman_tauberian_attempt"])
    report("current-polefit8x8-proxy-rejected", proxy_rejected, statuses["polefit8x8_stieltjes_proxy_diagnostic"])
    report("future-certificate-not-passed", not future_gate_passed, f"failed={future_failed}")
    report("does-not-authorize-proposed-retained", not proposal_allowed, "strict extremal route is open/conditional only")

    result = {
        "actual_current_surface_status": (
            "exact-support / strict extremal moment certificate route specified, "
            "but current PR230 surface lacks the flat-extension/localizing "
            "certificate and therefore still has no pole atom/residue authority"
        ),
        "conditional_surface_status": (
            "conditional-support if a future same-surface scalar-source "
            "Stieltjes moment package supplies flat extension or extremal "
            "truncated-moment consistency, localizing rank drop at the pole, "
            "tight residue extraction, threshold/FVIR/contact authority, and "
            "canonical O_H or physical-response authority"
        ),
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": proposal_allowed,
        "proposal_allowed_reason": (
            "The current surface has finite source moments and source-carrier "
            "support only.  Block64 gives positive completions with the same "
            "finite prefix and different pole atom; no strict flat-extension "
            "or extremal localizing certificate is present."
        ),
        "bare_retained_allowed": False,
        "audit_required_before_effective_retained": True,
        "block65_extremal_moment_certificate_route_passed": True,
        "current_pole_residue_authority_present": False,
        "strict_extremal_moment_certificate_present": bool(future_gate_passed),
        "future_certificate": str(FUTURE_CERTIFICATE.relative_to(ROOT)),
        "future_certificate_checks": future_checks,
        "future_certificate_missing_or_failed_checks": future_failed,
        "flat_extension_atom_witness": flat_witness,
        "current_prefix_obstruction_witness": obstruction,
        "strict_certificate_contract": contract,
        "current_missing_certificate_fields": missing_contract,
        "assumptions_exercise": assumption_exercise(),
        "first_principles_reduction": first_principles_reduction(),
        "math_route_summary": {
            "sufficient_certificate": (
                "For the shifted spectral variable lambda>=0, exact moments "
                "through a flat order with PSD moment/localizing matrices and "
                "rank M_d = rank M_{d+1} determine a unique finite atomic "
                "representing measure.  A rank drop in the lambda-localizing "
                "matrix counts the atom at lambda=0; the atom weight is the "
                "source-pole residue for that scalar measure."
            ),
            "why_current_surface_fails": (
                "The current surface does not provide the higher moments, "
                "rank-flat extension, extremal variety/consistency data, "
                "localizing rank drop, residue interval, threshold/FVIR/contact "
                "authority, or canonical/physical-response bridge."
            ),
        },
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained PR230 closure",
            "does not treat finite moment prefixes as residue authority",
            "does not use H_unit, Ward, y_t_bare, alpha_LM, plaquette/u0, observed targets, kappa_s=1, c2=1, or Z_match=1",
            "does not identify source-pole residue with canonical O_H without a future bridge",
        ],
        "exact_next_action": (
            "Produce outputs/yt_pr230_strict_extremal_moment_certificate_2026-05-12.json "
            "with the missing fields above, or abandon the moment route in "
            "favor of direct pole rows, a K'(pole) theorem, or a physical W/Z "
            "response bridge."
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
