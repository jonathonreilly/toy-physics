#!/usr/bin/env python3
"""
PR #230 isolated-pole Gram factorization theorem.

This block proves the exact support statement behind the future source-Higgs
Gram-purity route: at a nondegenerate isolated scalar pole, the residue matrix
for any finite operator family factorizes as z_i z_j.  Therefore the
source-Higgs 2x2 Gram determinant is zero once the source operator and a
certified canonical O_H are known to overlap with the same isolated pole.

It does not supply O_H, production C_sH/C_HH rows, pole isolation, or the
canonical-Higgs identity; those remain open PR #230 blockers.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_isolated_pole_gram_factorization_theorem_2026-05-03.json"

PARENTS = {
    "source_higgs_gram_purity_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "complete_source_spectrum_no_go": "outputs/yt_complete_source_spectrum_identity_no_go_2026-05-02.json",
    "source_pole_purity_cross_correlator": "outputs/yt_source_pole_purity_cross_correlator_gate_2026-05-02.json",
}

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


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def outer_residue(overlaps: list[float]) -> list[list[float]]:
    return [[float(a) * float(b) for b in overlaps] for a in overlaps]


def determinant_2x2(matrix: list[list[float]]) -> float:
    return float(matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])


def rank_two_degenerate_residue(overlaps_a: list[float], overlaps_b: list[float]) -> list[list[float]]:
    return [
        [float(a1) * float(a2) + float(b1) * float(b2) for a2, b2 in zip(overlaps_a, overlaps_b)]
        for a1, b1 in zip(overlaps_a, overlaps_b)
    ]


def examples() -> dict[str, Any]:
    isolated_rows = []
    for z_s, z_h in ((1.0, 0.4), (2.0, -0.8), (0.35, 1.7)):
        matrix = outer_residue([z_s, z_h])
        dgamma = 1.0 / matrix[0][0]
        res_sp_h = matrix[0][1] * math.sqrt(dgamma)
        delta_sp_h = matrix[1][1] - res_sp_h * res_sp_h
        isolated_rows.append(
            {
                "z_source": z_s,
                "z_higgs": z_h,
                "residue_matrix": matrix,
                "gram_determinant": determinant_2x2(matrix),
                "Dprime_ss_at_pole": dgamma,
                "Res_C_spH": res_sp_h,
                "Delta_spH": delta_sp_h,
                "rho_spH_abs": abs(res_sp_h / math.sqrt(matrix[1][1])) if matrix[1][1] > 0 else float("nan"),
            }
        )

    scaled_source_rows = []
    z_s, z_h = 1.3, 0.9
    for scale in (0.25, 1.0, 4.0):
        matrix = outer_residue([scale * z_s, z_h])
        dgamma = 1.0 / matrix[0][0]
        res_sp_h = matrix[0][1] * math.sqrt(dgamma)
        scaled_source_rows.append(
            {
                "source_scale": scale,
                "Res_C_ss": matrix[0][0],
                "Res_C_sH": matrix[0][1],
                "Res_C_HH": matrix[1][1],
                "Res_C_spH": res_sp_h,
                "Delta_spH": matrix[1][1] - res_sp_h * res_sp_h,
            }
        )

    degenerate_matrix = rank_two_degenerate_residue([1.0, 0.0], [0.0, 1.0])
    return {
        "isolated_non_degenerate_rows": isolated_rows,
        "source_rescaling_rows": scaled_source_rows,
        "degenerate_counterexample": {
            "description": "two independent states at the same pole give a positive rank-two residue matrix",
            "residue_matrix": degenerate_matrix,
            "gram_determinant": determinant_2x2(degenerate_matrix),
        },
    }


def main() -> int:
    print("PR #230 isolated-pole Gram factorization theorem")
    print("=" * 72)

    parents = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    witness = examples()
    isolated_rows = witness["isolated_non_degenerate_rows"]
    scaled_rows = witness["source_rescaling_rows"]
    degenerate = witness["degenerate_counterexample"]

    gram_factorization_ok = all(abs(float(row["gram_determinant"])) < 1.0e-12 for row in isolated_rows)
    osp_factorization_ok = all(abs(float(row["Delta_spH"])) < 1.0e-12 and abs(float(row["rho_spH_abs"]) - 1.0) < 1.0e-12 for row in isolated_rows)
    source_rescaling_invariant = (
        max(float(row["Res_C_spH"]) for row in scaled_rows)
        - min(float(row["Res_C_spH"]) for row in scaled_rows)
        < 1.0e-12
        and all(abs(float(row["Delta_spH"])) < 1.0e-12 for row in scaled_rows)
    )
    degenerate_assumption_necessary = abs(float(degenerate["gram_determinant"])) > 0.5

    gram_gate_open = (
        "source-Higgs Gram purity gate not passed" in status(parents["source_higgs_gram_purity_gate"])
        and parents["source_higgs_gram_purity_gate"].get("source_higgs_gram_purity_gate_passed") is False
    )
    builder_rows_absent = "rows absent" in status(parents["source_higgs_builder"])
    postprocessor_waits = "awaiting production certificate" in status(parents["source_higgs_postprocessor"])
    operator_absent = "canonical-Higgs operator certificate absent" in status(parents["canonical_higgs_operator_gate"])
    source_only_not_enough = (
        "source-functional LSZ identifiability" in status(parents["source_functional_lsz_identifiability"])
        and parents["source_functional_lsz_identifiability"].get("proposal_allowed") is False
    )
    complete_source_no_go = "complete source spectrum" in status(parents["complete_source_spectrum_no_go"])
    purity_gate_open = "source-pole purity cross-correlator gate not passed" in status(
        parents["source_pole_purity_cross_correlator"]
    )

    theorem_passed = gram_factorization_ok and osp_factorization_ok and source_rescaling_invariant

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("isolated-pole-residue-factorizes", gram_factorization_ok, "Res(C_ij)=z_i z_j gives det=0")
    report("osp-normalized-gram-factorizes", osp_factorization_ok, "Delta_spH=0 and |rho_spH|=1")
    report("source-rescaling-invariant", source_rescaling_invariant, "O_sp normalization removes source scale")
    report("nondegeneracy-assumption-necessary", degenerate_assumption_necessary, str(degenerate))
    report("source-higgs-gram-gate-still-open", gram_gate_open, status(parents["source_higgs_gram_purity_gate"]))
    report("source-higgs-rows-still-absent", builder_rows_absent and postprocessor_waits, status(parents["source_higgs_builder"]))
    report("canonical-oh-still-absent", operator_absent, status(parents["canonical_higgs_operator_gate"]))
    report("source-only-closure-still-blocked", source_only_not_enough and complete_source_no_go, "source-only data do not name O_H")
    report("cross-correlator-purity-gate-still-open", purity_gate_open, status(parents["source_pole_purity_cross_correlator"]))
    report("theorem-is-exact-support-not-closure", theorem_passed, f"theorem_passed={theorem_passed}")

    result = {
        "actual_current_surface_status": "exact-support / isolated-pole Gram factorization theorem",
        "conditional_surface_status": (
            "If a future certificate supplies a nondegenerate isolated scalar pole "
            "shared by O_sp and certified O_H, then O_sp-Higgs Gram purity follows."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The theorem is exact support only; PR #230 still lacks certified O_H, "
            "production C_sH/C_HH pole rows, pole isolation, and the retained-route gate."
        ),
        "isolated_pole_gram_factorization_theorem_passed": theorem_passed,
        "theorem_statement": (
            "For Euclidean two-point functions with a nondegenerate isolated scalar "
            "pole and operator overlaps z_i=<0|O_i|phi>, the pole residue matrix "
            "factorizes as Res C_ij = z_i z_j.  Therefore every 2x2 Gram determinant "
            "at that pole vanishes.  With O_sp = O_s / sqrt(Res C_ss), "
            "Delta_spH = Res(C_HH)-Res(C_sp,H)^2 = 0 and |rho_spH|=1."
        ),
        "assumptions": [
            "same Hilbert space and same scalar superselection sector",
            "nondegenerate isolated pole separated from continuum/other poles",
            "operators have finite nonzero overlap with the pole",
            "pole residues are extracted at the same pole on the same ensemble/surface",
        ],
        "necessary_assumption_counterexample": degenerate,
        "witness": witness,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not supply or define canonical O_H",
            "does not manufacture C_sH or C_HH pole rows",
            "does not prove pole isolation, nondegeneracy, FV/IR control, or canonical-Higgs identity",
            "does not use H_unit, yt_ward_identity, observed top/y_t/W/Z values, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Use this theorem as the exact support layer for future source-Higgs "
            "rows: supply a certified O_H, production same-pole C_ss/C_sH/C_HH "
            "residues with nondegenerate pole isolation, then rerun the "
            "O_sp-normalized Gram postprocessor and retained-route gate."
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
