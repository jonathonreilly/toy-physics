#!/usr/bin/env python3
"""
PR #230 key-blocker closure attempt.

The Ward repair loop narrowed the top-Yukawa analytic blocker to one
physics question: does the current repo already contain a retained authority
for the source-selected scalar pole residue and the relative scalar/gauge
dressing needed to turn the Ward/source coefficient into a physical Yukawa
readout?

This runner tests every plausible existing authority family against that
target.  A clean run is a reproducible negative boundary: it means the
current PR #230 surface does not yet close retained y_t, and it states the
precise theorem or measurement still needed.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_key_blocker_closure_attempt_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def read(path: str) -> str:
    full = ROOT / path
    if not full.exists():
        return ""
    return full.read_text(encoding="utf-8", errors="ignore")


def ledger_rows() -> dict[str, dict]:
    return json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]


def status(rows: dict[str, dict], key: str) -> str | None:
    return rows.get(key, {}).get("effective_status")


def term_hits(text: str, terms: list[str]) -> list[str]:
    lower = text.lower()
    return [term for term in terms if term.lower() in lower]


def main() -> int:
    print("PR #230 key-blocker closure attempt")
    print("=" * 72)

    rows = ledger_rows()

    candidates = [
        {
            "route": "old_ward_h_unit",
            "ledger_key": "yt_ward_identity_derivation_theorem",
            "files": [
                "docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md",
                "scripts/frontier_yt_ward_identity_derivation.py",
            ],
            "tests": ["H_unit", "matrix element", "y_t_bare"],
            "closes_pole_residue": False,
            "closes_common_dressing": False,
            "reason": (
                "Computes the 1/sqrt(6) H_unit overlap but the audit marks the "
                "physical readout as audited_renaming."
            ),
        },
        {
            "route": "rconn_color_projection",
            "ledger_key": "yt_color_projection_correction_note",
            "files": [
                "docs/YT_COLOR_PROJECTION_CORRECTION_NOTE.md",
                "docs/YUKAWA_COLOR_PROJECTION_THEOREM.md",
                "docs/RCONN_DERIVED_NOTE.md",
            ],
            "tests": ["Z_phi", "R_conn", "scalar"],
            "closes_pole_residue": False,
            "closes_common_dressing": False,
            "reason": (
                "Provides channel arithmetic, but the ledger says the scalar "
                "LSZ/pole-residue bridge is audited_conditional."
            ),
        },
        {
            "route": "source_higgs_legendre_ssb",
            "ledger_key": None,
            "files": [
                "docs/YT_SOURCE_HIGGS_LEGENDRE_SSB_BRIDGE_NOTE_2026-05-01.md",
                "scripts/frontier_yt_source_higgs_legendre_ssb_bridge.py",
            ],
            "tests": ["kappa_H", "Legendre", "two-point residue"],
            "closes_pole_residue": False,
            "closes_common_dressing": False,
            "reason": (
                "Closes SSB bookkeeping conditionally once a canonical scalar "
                "coefficient is supplied; it explicitly leaves kappa_H open."
            ),
        },
        {
            "route": "source_higgs_kappa_obstruction",
            "ledger_key": None,
            "files": [
                "docs/YT_SOURCE_HIGGS_KAPPA_RESIDUE_OBSTRUCTION_NOTE_2026-05-01.md",
                "scripts/frontier_yt_source_higgs_kappa_residue_obstruction.py",
            ],
            "tests": ["kappa_H", "LSZ", "scalar two-point"],
            "closes_pole_residue": False,
            "closes_common_dressing": False,
            "reason": (
                "Proves counts plus SSB do not select kappa_H; it is a no-go "
                "boundary, not a closure theorem."
            ),
        },
        {
            "route": "scalar_lsz_residue_bridge",
            "ledger_key": None,
            "files": [
                "docs/YT_SCALAR_LSZ_RESIDUE_BRIDGE_NOTE_2026-05-01.md",
                "scripts/frontier_yt_scalar_lsz_residue_bridge.py",
            ],
            "tests": ["LSZ", "Z_phi", "R_conn"],
            "closes_pole_residue": False,
            "closes_common_dressing": False,
            "reason": (
                "Shows R_conn is not enough to derive the physical scalar LSZ "
                "residue."
            ),
        },
        {
            "route": "common_dressing",
            "ledger_key": None,
            "files": [
                "docs/YT_COMMON_DRESSING_OBSTRUCTION_NOTE_2026-05-01.md",
                "scripts/frontier_yt_common_dressing_obstruction.py",
            ],
            "tests": ["common", "dressing", "scalar"],
            "closes_pole_residue": False,
            "closes_common_dressing": False,
            "reason": (
                "Proves current Ward/gauge identities do not enforce common "
                "scalar/gauge dressing."
            ),
        },
        {
            "route": "one_higgs_selector",
            "ledger_key": "sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26",
            "files": [
                "docs/SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md",
            ],
            "tests": ["Qbar_L", "H", "u_R"],
            "closes_pole_residue": False,
            "closes_common_dressing": False,
            "reason": (
                "Selects the allowed SM Yukawa operator pattern but not its "
                "source-to-canonical scalar residue."
            ),
        },
        {
            "route": "ew_higgs_kinetic_normalization",
            "ledger_key": "ew_higgs_gauge_mass_diagonalization_theorem_note_2026-04-26",
            "files": [
                "docs/EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md",
                "scripts/frontier_ew_higgs_gauge_mass_diagonalization.py",
            ],
            "tests": ["Higgs", "kinetic", "mass"],
            "closes_pole_residue": False,
            "closes_common_dressing": False,
            "reason": (
                "Uses the canonical elementary-Higgs convention for EW mass "
                "diagonalization; it does not derive the composite/source "
                "operator pole residue that couples to the Ward coefficient."
            ),
        },
        {
            "route": "taste_scalar_isotropy",
            "ledger_key": "taste_scalar_isotropy_theorem_note",
            "files": ["docs/TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md"],
            "tests": ["taste", "scalar", "isotropy"],
            "closes_pole_residue": False,
            "closes_common_dressing": False,
            "reason": (
                "Controls scalar direction/isotropy data, not the dynamical "
                "two-point pole residue."
            ),
        },
        {
            "route": "neutrino_scalar_two_point_analogue",
            "ledger_key": "neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary_note_2026-04-29",
            "files": [
                "docs/NEUTRINO_LANE4_SR2_PFAFFIAN_SCALAR_TWO_POINT_BOUNDARY_NOTE_2026-04-29.md",
            ],
            "tests": ["scalar", "two-point", "boundary"],
            "closes_pole_residue": False,
            "closes_common_dressing": False,
            "reason": (
                "Useful analogue in the neutrino lane, but it does not supply "
                "the top-sector scalar source residue or dressing theorem."
            ),
        },
    ]

    candidate_results = []
    for candidate in candidates:
        file_texts = {path: read(path) for path in candidate["files"]}
        combined = "\n".join(file_texts.values())
        files_present = all(bool(text) for text in file_texts.values())
        hits = term_hits(combined, candidate["tests"])
        evidence_present = files_present and bool(hits)
        key = candidate["ledger_key"]
        effective_status = status(rows, key) if key else None
        closes = candidate["closes_pole_residue"] and candidate["closes_common_dressing"]
        candidate_results.append(
            {
                "route": candidate["route"],
                "ledger_key": key,
                "effective_status": effective_status,
                "files": candidate["files"],
                "evidence_terms": candidate["tests"],
                "evidence_term_hits": hits,
                "evidence_present": evidence_present,
                "closes_pole_residue": candidate["closes_pole_residue"],
                "closes_common_dressing": candidate["closes_common_dressing"],
                "closes_key_blocker": closes,
                "reason": candidate["reason"],
            }
        )
        report(
            f"candidate-scanned-{candidate['route']}",
            evidence_present,
            f"status={effective_status}; hits={hits}; closes_key_blocker={closes}",
        )

    clean_closures = [row for row in candidate_results if row["closes_key_blocker"]]
    retained_authorities = [
        row
        for row in candidate_results
        if row["effective_status"] == "retained" and row["closes_key_blocker"]
    ]
    explicit_no_go_count = sum(
        any(
            token in (row["route"] + " " + row["reason"]).lower()
            for token in ["obstruction", "no-go", "not enough", "not enforce"]
        )
        for row in candidate_results
    )

    report("all-candidate-families-covered", len(candidate_results) == 10, f"covered={len(candidate_results)}")
    report("no-current-candidate-closes-key-blocker", not clean_closures, f"closures={clean_closures}")
    report("no-retained-authority-closes-key-blocker", not retained_authorities, f"retained={retained_authorities}")
    report("negative-boundaries-present", explicit_no_go_count >= 3, f"explicit_no_go_count={explicit_no_go_count}")

    required_theorem = {
        "name": "top-sector scalar source pole-residue and common-dressing theorem",
        "must_derive": [
            "construct the source-selected scalar two-point function C_OO(p) from the retained Cl(3)/Z^3 Wilson-staggered action",
            "show that C_OO(p) has the physical Higgs-carrier pole used by the Yukawa readout",
            "compute or bound the pole residue Z_phi and the source-to-canonical factor kappa_H",
            "derive the scalar/gauge dressing ratio, or measure it independently, without alpha_LM or H_unit matrix-element authority",
            "only then map the Ward/source coefficient to a physical y_t/g_s readout",
        ],
        "equivalent_measurement": (
            "a strict production correlator certificate measuring m_t and y_t "
            "directly at a physically suitable scale/heavy-top treatment"
        ),
    }

    result = {
        "actual_current_surface_status": "open / key blocker not closed",
        "verdict": (
            "The closure attempt found no existing retained authority that derives "
            "the scalar source pole residue and common scalar/gauge dressing needed "
            "to repair the Ward physical-readout route.  Existing artifacts either "
            "compute tree-level/channel/operator arithmetic, close SSB bookkeeping "
            "conditionally, or record no-go boundaries.  Retained top-Yukawa closure "
            "therefore still requires the named scalar two-point residue theorem or "
            "a strict direct physical measurement certificate."
        ),
        "candidate_results": candidate_results,
        "clean_closures": clean_closures,
        "retained_authorities": retained_authorities,
        "required_theorem": required_theorem,
        "strict_non_claims": [
            "does not promote yt_ward_identity_derivation_theorem",
            "does not define y_t_bare by a H_unit matrix element",
            "does not use observed m_t or y_t as derivation input",
            "does not certify direct production measurement",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
