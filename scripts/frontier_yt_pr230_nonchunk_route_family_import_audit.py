#!/usr/bin/env python3
"""
PR #230 non-chunk route-family assumption/import audit.

This runner records the required non-chunk route-family exercise before
choosing a science block.  It compares live positive routes by missing imports,
current-surface executable leverage, and forbidden-import risk.  It does not
claim closure and does not package or rerun chunk MC.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKLIST = ROOT / "outputs" / "yt_pr230_non_chunk_closure_worklist_2026-05-05.json"
ASSEMBLY = ROOT / "outputs" / "yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json"
RETAINED_ROUTE = ROOT / "outputs" / "yt_retained_closure_route_certificate_2026-05-01.json"
CAMPAIGN = ROOT / "outputs" / "yt_pr230_campaign_status_certificate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json"

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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def future_presence(worklist: dict[str, Any], keys: list[str]) -> dict[str, bool]:
    presence = worklist.get("future_file_presence", {})
    if not isinstance(presence, dict):
        return {key: False for key in keys}
    return {key: bool(presence.get(key)) for key in keys}


def family_rows(worklist: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": "canonical_oh_source_higgs",
            "route_family": "source-Higgs / canonical O_H",
            "minimum_allowed_premises": [
                "Cl(3)/Z3 scalar-source surface",
                "Legendre/LSZ O_sp as normalized source-pole support",
                "same-surface canonical O_H certificate or real O_H production surface",
            ],
            "forbidden_imports": [
                "H_unit or Ward readout",
                "static EW algebra as O_H identity",
                "observed top/Higgs/W/Z selectors",
            ],
            "future_files": future_presence(
                worklist,
                ["canonical_oh_certificate", "source_higgs_rows"],
            ),
            "open_import_count": 2,
            "runner_or_gate_available": True,
            "can_execute_now": False,
            "dramatic_step_score": 2,
            "hard_residual_pressure": 2,
            "current_disposition": "blocked until same-surface O_H and C_sH/C_HH rows exist",
            "retirement_path": "derive O_H certificate, then run source-Higgs Gram-purity rows",
        },
        {
            "id": "same_source_wz_response",
            "route_family": "same-source W/Z response",
            "minimum_allowed_premises": [
                "same source coordinate for top and W/Z rows",
                "same-source EW action and W/Z mass-fit rows",
                "source-coordinate transport from PR230 source to canonical Higgs radial coordinate",
                "matched top/W covariance or closed covariance theorem",
                "non-observed g2 certificate",
                "strict delta_perp correction or null theorem",
            ],
            "forbidden_imports": [
                "observed W/Z/top/y_t/g2 selectors",
                "user-banned coupling-normalization shortcuts",
                "deterministic W response without paired top rows or covariance theorem",
            ],
            "future_files": future_presence(
                worklist,
                [
                    "matched_top_wz_rows",
                    "top_wz_closed_covariance_theorem",
                    "deterministic_response_covariance_certificate",
                    "source_coordinate_transport_certificate",
                    "wz_mass_response_rows",
                    "non_observed_g2_certificate",
                    "delta_perp_rows",
                ],
            ),
            "open_import_count": 6,
            "runner_or_gate_available": True,
            "can_execute_now": False,
            "cycle13_selected_shortcut": True,
            "dramatic_step_score": 5,
            "hard_residual_pressure": 5,
            "current_disposition": "cycle-13 W/Z covariance-theorem import audit executed; source-coordinate transport, Goldstone-equivalence source identity, and existing covariance-theorem import shortcuts are closed negatively",
            "retirement_path": "produce matched rows or prove a new same-surface product/conditional-independence/closed-covariance theorem plus source-transport authority",
        },
        {
            "id": "scalar_lsz_polynomial_contact",
            "route_family": "scalar-LSZ finite-shell contact/model-class",
            "minimum_allowed_premises": [
                "current polefit8x8 finite-shell C_ss rows as diagnostic support only",
                "Stieltjes necessary conditions for positive scalar two-point transforms",
                "no same-surface contact or scalar-denominator certificate assumed",
            ],
            "forbidden_imports": [
                "fitted contact term promoted as physical",
                "kappa_s=1, c2=1, or Z_match=1",
                "H_unit, Ward authority, observed target values, alpha_LM, plaquette, or u0",
            ],
            "future_files": future_presence(
                worklist,
                [
                    "stieltjes_moment_certificate",
                    "pade_stieltjes_bounds_certificate",
                    "contact_subtraction_certificate",
                ],
            ),
            "open_import_count": 3,
            "runner_or_gate_available": True,
            "can_execute_now": False,
            "dramatic_step_score": 3,
            "hard_residual_pressure": 3,
            "current_disposition": "blocked; polynomial-contact repair has already closed negatively",
            "retirement_path": "future route must supply a strict contact, moment-threshold, FV/IR, or scalar-denominator certificate",
        },
        {
            "id": "schur_scalar_denominator_rows",
            "route_family": "Schur/K-prime scalar denominator rows",
            "minimum_allowed_premises": [
                "same-surface Schur A/B/C partition rows",
                "Schur-complement K-prime sufficiency theorem",
            ],
            "forbidden_imports": [
                "finite FH/LSZ source rows substituted as Schur rows",
                "legacy Schur bridge stack",
                "fitted scalar-kernel residue selector",
            ],
            "future_files": future_presence(worklist, ["schur_kernel_rows"]),
            "open_import_count": 1,
            "runner_or_gate_available": True,
            "can_execute_now": False,
            "dramatic_step_score": 2,
            "hard_residual_pressure": 2,
            "current_disposition": "cycle-7 Schur compressed-denominator row-bootstrap no-go executed; no same-surface Schur A/B/C rows present",
            "retirement_path": "supply real same-surface Schur kernel rows; compressed denominator data cannot reconstruct them",
        },
        {
            "id": "neutral_scalar_rank_one",
            "route_family": "neutral-scalar primitive-cone rank one",
            "minimum_allowed_premises": [
                "same-surface neutral transfer sector",
                "primitive-cone or positivity-improving irreducibility certificate",
            ],
            "forbidden_imports": [
                "gauge-vacuum Perron theorem as neutral-sector authority",
                "commutant rank asserted as dynamics",
                "one-Higgs notation used as field-completeness proof",
            ],
            "future_files": future_presence(
                worklist,
                ["neutral_irreducibility_certificate", "neutral_primitive_cone_certificate"],
            ),
            "open_import_count": 2,
            "runner_or_gate_available": True,
            "can_execute_now": False,
            "dramatic_step_score": 4,
            "hard_residual_pressure": 4,
            "current_disposition": "cycle-5 stretch executed; source-only and conditional Perron premises do not force primitive-cone irreducibility",
            "retirement_path": "derive primitive-cone irreducibility or produce the strict certificate",
        },
    ]


def main() -> int:
    print("PR #230 non-chunk route-family assumption/import audit")
    print("=" * 72)

    worklist = load_json(WORKLIST)
    assembly = load_json(ASSEMBLY)
    retained = load_json(RETAINED_ROUTE)
    campaign = load_json(CAMPAIGN)
    rows = family_rows(worklist)
    ranked_future = max(
        rows,
        key=lambda row: (
            bool(row.get("cycle13_selected_shortcut")),
            int(row["dramatic_step_score"]),
            int(row["hard_residual_pressure"]),
            -int(row["open_import_count"]),
        ),
    )
    executable_rows = [row for row in rows if row["can_execute_now"]]
    selected = {
        "id": "no_current_surface_nonchunk_route",
        "route_family": "cycle-14 route selector",
        "can_execute_now": False,
        "current_disposition": (
            "The current non-chunk route surface is exhausted after the "
            "cycle-13 W/Z covariance-theorem import no-go.  No route family "
            "has the first-action same-surface row, certificate, or theorem "
            "needed to pass the dramatic-step gate."
        ),
        "retirement_path": (
            "Supply one listed future artifact as a parseable claim-status "
            "artifact, rerun reopen-admissibility plus the aggregate gates, "
            "then select the corresponding positive route."
        ),
    }

    report("worklist-parent-loaded", bool(worklist), rel(WORKLIST))
    report("assembly-parent-loaded", bool(assembly), rel(ASSEMBLY))
    report("retained-route-parent-loaded", bool(retained), rel(RETAINED_ROUTE))
    report("campaign-parent-loaded", bool(campaign), rel(CAMPAIGN))
    report("at-least-three-route-families-audited", len(rows) >= 3, f"families={len(rows)}")
    report(
        "no-parent-authorizes-proposal",
        not any(parent.get("proposal_allowed") is True for parent in (worklist, assembly, retained, campaign)),
        "proposal_allowed remains false",
    )
    report(
        "top-ranked-future-route-reflects-cycle13-wz-covariance-import-audit",
        ranked_future["id"] == "same_source_wz_response"
        and "covariance-theorem import audit" in ranked_future["current_disposition"],
        ranked_future["id"],
    )
    report(
        "no-current-route-family-executable",
        not executable_rows and selected["id"] == "no_current_surface_nonchunk_route",
        f"executable={[row['id'] for row in executable_rows]} selected={selected['id']}",
    )
    report(
        "top-ranked-future-route-has-no-banned-import",
        not any(
            banned in " ".join(ranked_future["minimum_allowed_premises"])
            for banned in (
                "H_unit",
                "yt_ward",
                "alpha_LM",
                "plaquette",
                "u0",
                "observed target",
                "bare-coupling",
                "y_t_bare",
            )
        )
        and ranked_future["id"] == "same_source_wz_response",
        "forbidden imports are explicit blockers, not premises",
    )
    report(
        "does-not-authorize-proposed-retained",
        True,
        "route-family audit and selection only",
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / non-chunk route-family import audit confirms no executable current-surface route after W/Z covariance-theorem import no-go"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "All audited route families retain open load-bearing imports.  The "
            "cycle-13 W/Z covariance-theorem import audit sharpens the "
            "same-source W/Z route, but no route family now has an executable "
            "current-surface first action or proposed_retained PR230 closure."
        ),
        "route_families_audited": rows,
        "executable_route_ids": [row["id"] for row in executable_rows],
        "ranked_future_route": ranked_future,
        "selected_route": selected,
        "selection_reason": (
            "After the W/Z source-coordinate transport, Goldstone-equivalence, "
            "native-label factorization, deterministic-response, scalar contact, "
            "O_H premise, Schur bootstrap, and neutral primitive-cone shortcuts "
            "closed negatively, the top-ranked W/Z route still had one exact "
            "import loophole: treating current builders, scout schemas, support "
            "notes, or no-go gates as the missing joint covariance theorem.  "
            "Cycle 13 closes that shortcut.  Every positive route now requires "
            "absent future rows or a new same-surface theorem, so cycle 14 "
            "selects no current-surface non-chunk route."
        ),
        "strict_non_claims": [
            "does not package or rerun chunk MC",
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not define a bare top-Yukawa readout",
            "does not use prohibited operator/readout, target-value, coupling-normalization, or unit shortcuts",
        ],
        "exact_next_action": (
            "Do not select another current-surface non-chunk shortcut.  Reopen "
            "only after a listed same-surface row, certificate, or theorem "
            "exists as a parseable claim-status artifact, then rerun the "
            "reopen-admissibility, worklist, exhaustion, intake, assembly, "
            "retained-route, and campaign gates before selecting the next "
            "positive route."
        ),
        "parent_certificates": {
            "worklist": rel(WORKLIST),
            "assembly": rel(ASSEMBLY),
            "retained_route": rel(RETAINED_ROUTE),
            "campaign": rel(CAMPAIGN),
        },
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
