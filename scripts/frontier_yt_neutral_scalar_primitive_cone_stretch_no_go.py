#!/usr/bin/env python3
"""
PR #230 neutral-scalar primitive-cone stretch no-go.

After the W/Z source-transport route closed negatively, the remaining
non-chunk bridge surface still needs a same-surface neutral-sector
irreducibility theorem if the rank-one route is to replace missing O_H or W/Z
rows.  This runner performs the required first-principles stretch attempt: it
uses only current PR230 source/neutral premises and checks whether they force a
primitive neutral transfer cone.

They do not.  A source-invisible reducible neutral completion preserves all
source-only rows while leaving an orthogonal neutral direction outside the
primitive cone.  The result is a no-go boundary plus stuck-fanout synthesis,
not a closure claim.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_neutral_scalar_primitive_cone_stretch_no_go_2026-05-05.json"
)

PARENTS = {
    "primitive_cone_gate": "outputs/yt_neutral_scalar_primitive_cone_certificate_gate_2026-05-05.json",
    "irreducibility_authority_audit": "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json",
    "positivity_improving_support": "outputs/yt_positivity_improving_neutral_scalar_rank_one_support_2026-05-03.json",
    "direct_positivity_attempt": "outputs/yt_neutral_scalar_positivity_improving_direct_closure_attempt_2026-05-03.json",
    "commutant_rank_no_go": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
    "dynamical_rank_one_attempt": "outputs/yt_neutral_scalar_dynamical_rank_one_closure_attempt_2026-05-02.json",
    "top_coupling_tomography": "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json",
    "non_source_rank_repair": "outputs/yt_non_source_response_rank_repair_sufficiency_2026-05-03.json",
    "source_higgs_gram": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "wz_source_transport_no_go": "outputs/yt_wz_source_coordinate_transport_no_go_2026-05-05.json",
    "schur_row_absence": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
}

FORBIDDEN_IMPORTS = [
    "external top, Higgs, W, Z, Yukawa, or gauge targets",
    "unit-operator or matrix-element renaming authority",
    "Ward-identity readout authority",
    "lattice gauge-normalization or bare gauge-coupling shortcut",
    "unit overlap assumptions such as kappa_s=1, cos(theta)=1, c2=1, or Z_match=1",
    "source-only C_ss rows promoted to O_H, Schur A/B/C rows, or W/Z rows",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def strongly_connected(matrix: list[list[float]], tolerance: float = 1.0e-12) -> bool:
    n = len(matrix)
    graph = [[j for j, value in enumerate(row) if value > tolerance] for row in matrix]
    reverse = [[i for i in range(n) if matrix[i][j] > tolerance] for j in range(n)]

    def reachable(adjacency: list[list[int]]) -> set[int]:
        seen = {0}
        queue: deque[int] = deque([0])
        while queue:
            node = queue.popleft()
            for child in adjacency[node]:
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
        return seen

    return len(reachable(graph)) == n and len(reachable(reverse)) == n


def multiply(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    n = len(left)
    return [
        [sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def primitive_power_positive(matrix: list[list[float]], tolerance: float = 1.0e-12) -> dict[str, Any]:
    n = len(matrix)
    power = [row[:] for row in matrix]
    max_power = max(1, n * n - 2 * n + 2)
    for exponent in range(1, max_power + 1):
        if all(value > tolerance for row in power for value in row):
            return {"positive": True, "first_positive_power": exponent}
        power = multiply(power, matrix)
    return {"positive": False, "first_positive_power": None}


def source_rows(mass_sq: float, residue: float, shells: list[float]) -> list[dict[str, float]]:
    return [
        {
            "p_hat_sq": shell,
            "C_ss": residue / (shell + mass_sq),
        }
        for shell in shells
    ]


def source_invisible_reducible_completion() -> dict[str, Any]:
    shells = [0.0, 0.2679491924311227, 0.5358983848622454, 1.0]
    source_mass_sq = 0.25
    source_residue = 1.0
    orthogonal_masses = [1.4, 2.0, 3.2]
    rows = source_rows(source_mass_sq, source_residue, shells)
    completions = []
    for mass_sq in orthogonal_masses:
        transfer = [[0.82, 0.0], [0.0, 0.61]]
        completions.append(
            {
                "basis": ["source_created_neutral", "orthogonal_neutral"],
                "orthogonal_mass_sq": mass_sq,
                "neutral_transfer_matrix": transfer,
                "source_vector": [1.0, 0.0],
                "source_rows": rows,
                "same_source_rows_as_all_other_completions": True,
                "strongly_connected": strongly_connected(transfer),
                "primitive_power": primitive_power_positive(transfer),
                "orthogonal_direction_visible_to_source_only_rows": False,
            }
        )
    return {
        "construction_type": "algebraic non-data counterfamily",
        "shells_p_hat_sq": shells,
        "source_mass_sq": source_mass_sq,
        "source_residue": source_residue,
        "completions": completions,
        "all_preserve_source_rows": True,
        "all_fail_primitive_cone": all(
            not row["strongly_connected"] and not row["primitive_power"]["positive"]
            for row in completions
        ),
    }


def fanout_frames() -> list[dict[str, str]]:
    return [
        {
            "frame": "source-only rows",
            "attempt": "Use C_ss pole data to force the neutral cone to one primitive component.",
            "wall": "A decoupled orthogonal neutral block leaves C_ss unchanged.",
            "disposition": "blocked",
        },
        {
            "frame": "conditional Perron support",
            "attempt": "Apply the existing positivity-improving rank-one theorem directly.",
            "wall": "The theorem requires the primitive-cone certificate as an input; current data do not prove strong connectivity.",
            "disposition": "conditional support only",
        },
        {
            "frame": "symmetry or commutant labels",
            "attempt": "Reduce neutral-sector dimension from labels alone.",
            "wall": "Existing commutant and dynamical rank-one no-gos leave rank-two positive completions.",
            "disposition": "blocked",
        },
        {
            "frame": "non-source rank repair",
            "attempt": "Use an extra bridge observable to expose the orthogonal direction.",
            "wall": "The needed O_H/C_sH/C_HH, W/Z, or Schur A/B/C rows are absent.",
            "disposition": "future row route only",
        },
        {
            "frame": "gauge or reflection positivity import",
            "attempt": "Import irreducibility from a nearby positive gauge/Perron surface.",
            "wall": "The authority audit rejects imports that are not the same neutral scalar transfer sector.",
            "disposition": "blocked",
        },
    ]


def minimal_premise_set() -> dict[str, Any]:
    return {
        "A_min": [
            "current PR230 same-source scalar-source surface",
            "source-created neutral pole support rows as source-side evidence only",
            "conditional Perron/rank-one support theorem when a primitive cone is supplied",
            "current no-go memory for O_H, W/Z, Schur, source-only, and neutral rank shortcuts",
        ],
        "forbidden_imports": FORBIDDEN_IMPORTS,
    }


def main() -> int:
    print("PR #230 neutral-scalar primitive-cone stretch no-go")
    print("=" * 72)

    parents = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    statuses = {name: status(cert) for name, cert in parents.items()}
    counterfamily = source_invisible_reducible_completion()
    fanout = fanout_frames()
    premise_set = minimal_premise_set()

    conditional_support_loaded = (
        "positivity-improving neutral-scalar rank-one theorem"
        in statuses["positivity_improving_support"]
        and parents["positivity_improving_support"].get("positivity_improving_rank_one_theorem_passed")
        is True
        and parents["positivity_improving_support"].get("positivity_improving_certificate_present")
        is False
    )
    primitive_gate_absent = (
        "primitive-cone certificate gate" in statuses["primitive_cone_gate"]
        and parents["primitive_cone_gate"].get("primitive_cone_certificate_gate_passed") is False
    )
    authority_absent = (
        "irreducibility authority absent" in statuses["irreducibility_authority_audit"]
        and parents["irreducibility_authority_audit"].get("neutral_scalar_irreducibility_certificate_present")
        is False
    )
    direct_attempt_blocked = (
        "positivity-improving direct theorem not derived" in statuses["direct_positivity_attempt"]
        and parents["direct_positivity_attempt"].get("direct_positivity_improving_theorem_derived")
        is False
    )
    source_only_rows_insufficient = (
        counterfamily["all_preserve_source_rows"] and counterfamily["all_fail_primitive_cone"]
    )
    fanout_complete = len(fanout) == 5 and all(row["disposition"] for row in fanout)
    forbidden_imports_are_blockers = all(
        token not in " ".join(premise_set["A_min"])
        for token in ("unit-operator", "Ward", "gauge-normalization", "external target")
    )
    stretch_no_go_passed = (
        not missing
        and not proposal_allowed
        and conditional_support_loaded
        and primitive_gate_absent
        and authority_absent
        and direct_attempt_blocked
        and source_only_rows_insufficient
        and fanout_complete
        and forbidden_imports_are_blockers
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("minimal-premise-set-recorded", len(premise_set["A_min"]) == 4, "A_min entries=4")
    report("forbidden-imports-are-blockers-not-premises", forbidden_imports_are_blockers, "forbidden imports excluded from A_min")
    report("conditional-perron-support-loaded", conditional_support_loaded, statuses["positivity_improving_support"])
    report("primitive-cone-certificate-still-absent", primitive_gate_absent, statuses["primitive_cone_gate"])
    report("irreducibility-authority-still-absent", authority_absent, statuses["irreducibility_authority_audit"])
    report("direct-positivity-attempt-still-blocked", direct_attempt_blocked, statuses["direct_positivity_attempt"])
    report("source-invisible-reducible-counterfamily", source_only_rows_insufficient, "source C_ss rows unchanged; transfer not primitive")
    report("stuck-fanout-recorded", fanout_complete, f"frames={len(fanout)}")
    report("neutral-primitive-cone-stretch-no-go-passed", stretch_no_go_passed, "current premises do not force irreducibility")
    report("does-not-authorize-proposed-retained", True, "neutral-rank stretch no-go only")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / neutral-scalar primitive-cone stretch no-go on current PR230 surface"
        ),
        "verdict": (
            "Current PR230 source/neutral premises do not force a primitive "
            "neutral transfer cone.  Source-only rows are compatible with a "
            "reducible orthogonal neutral completion, while the existing Perron "
            "rank-one theorem remains conditional on the very primitive-cone "
            "certificate that is absent."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No same-surface primitive-cone or neutral-sector irreducibility "
            "certificate is present; source-only rows and conditional Perron "
            "support do not remove the orthogonal neutral direction."
        ),
        "bare_retained_allowed": False,
        "primitive_cone_stretch_no_go_passed": stretch_no_go_passed,
        "minimal_premise_set": premise_set,
        "source_invisible_reducible_counterfamily": counterfamily,
        "stuck_fanout": fanout,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not infer neutral irreducibility from source-only rows",
            "does not synthesize O_H/C_sH/C_HH, W/Z, Schur, or matched response rows",
            "does not use unit-operator, Ward-readout, external-target, gauge-normalization, bare-Yukawa-symbol, or bare-gauge-coupling algebra",
            "does not package or rerun chunk MC",
        ],
        "exact_next_action": (
            "Supply a strict same-surface neutral primitive-cone certificate, "
            "or pivot to another future-row route: O_H/C_sH/C_HH pole rows, "
            "same-source W/Z rows with identities, Schur A/B/C kernel rows, or "
            "a scalar-LSZ moment/threshold/FV certificate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
