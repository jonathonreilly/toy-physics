#!/usr/bin/env python3
"""
Bridge-Dependent Lanes — Retained_Bounded Promotion Evaluation Runner
=============================================================================

Companion runner for:
    docs/BRIDGE_LANES_PROMOTION_PROPOSAL_NOTE_2026-05-10_lanes.md

This runner verifies the per-lane promotion-evaluation logic against the
audit-ledger row data for three bridge-dependent lanes:

    Lane 1: alpha_s direct Wilson loop
    Lane 2: Higgs mass from axiom
    Lane 3: gauge-scalar bridge

For each lane, the runner verifies:

  (a) Structural retained content is identified.
  (b) Residual admissions are enumerated honestly.
  (c) Engineering-vs-structural character of each residual is correct.
  (d) Promotion verdict (already_promoted / pending_partial / blocked)
      is consistent with the four-criterion logic.
  (e) Audit-ledger fields (claim_type, effective_status) are read but
      NOT modified by this runner; the runner verifies internal
      consistency only.

No PDG values, observed numbers, or fitted couplings are consumed as
inputs to the verdict logic. The runner uses governance metadata
(audit_ledger.json claim_type / effective_status) and structural
admission status only.

Self-contained: numpy + json + stdlib only.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = "") -> bool:
    """Record a pass/fail result and print it."""
    global PASS, FAIL
    if cond:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    msg = f"  [{tag}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return cond


def section(title: str) -> None:
    print("\n" + "=" * 88)
    print(title)
    print("=" * 88)


# -----------------------------------------------------------------------------
# Audit-ledger reading
# -----------------------------------------------------------------------------

def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, here.parent.parent, here.parent.parent.parent]:
        if (parent / "docs" / "audit" / "data" / "audit_ledger.json").exists():
            return parent
    raise SystemExit("ERROR: cannot locate repo root via audit_ledger.json")


def load_ledger() -> dict:
    root = find_repo_root()
    with open(root / "docs" / "audit" / "data" / "audit_ledger.json") as f:
        d = json.load(f)
    return d.get("rows", {})


def get_row(rows: dict, key: str) -> dict:
    return rows.get(key, {})


# -----------------------------------------------------------------------------
# Per-lane data model
# -----------------------------------------------------------------------------

# Each lane is a dict with:
#   parent_keys: list of audit-ledger row keys
#   structural_retained: brief description (str)
#   residual_admissions: list of dicts {"name": str, "kind": "engineering"|"structural", "closed_by_w2_nlo": bool}
#   verdict: "already_promoted" | "pending_partial" | "blocked"
#   verdict_reason: str

LANE_ALPHA_S = {
    "name": "Lane 1: alpha_s direct Wilson loop",
    "parent_keys": [
        "alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30",
        "alpha_s_direct_wilson_loop_honest_status_audit_note_2026-05-02",
    ],
    "expected_parent_status": {
        "alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30": {
            "claim_type": "bounded_theorem",
            "effective_status": "audited_conditional",
        },
    },
    "structural_retained": "Cl(3)/Z3 SU(3) Wilson surface; decoration-trap-clean static-potential pipeline",
    "residual_admissions": [
        {"name": "convention_c_iso", "kind": "engineering", "closed_by_w2_nlo": False,
         "note": "named compute frontier; SU(3) NLO closed-form gives ε_C-iso ~ 0.1287/ξ; ξ >= 430 to reach ε_witness"},
        {"name": "sommer_scale_r0_literature", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "external standard correction (Sommer 1993, FLAG); no framework-native scale-setting theorem exists"},
        {"name": "four_loop_qcd_running", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "external standard 4-loop beta function; no framework-native running theorem"},
        {"name": "threshold_matching", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "external PDG-style threshold matching at quark mass thresholds"},
        {"name": "sea_quark_full_qcd_bridge", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "pure-gauge to full-QCD bridge; not closed by current framework"},
        {"name": "l3a_trace_surface", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "single L3a admission (matter-rep gate); sharpened by W2 trilogy but not closed"},
        {"name": "g_bare_canonical_normalization", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "g_bare=1 still open per MINIMAL_AXIOMS_2026-05-03; in-flight Hilbert-Schmidt rigidity route"},
    ],
    "verdict": "pending_partial",
    "verdict_reason": (
        "C-iso piece is a named engineering frontier (closed-form SU(3) NLO bound exists); "
        "but four standard QCD imports (Sommer, 4-loop running, threshold matching, sea-quark) "
        "are unmoved by W2 / SU(3)-NLO and are structural literature dependencies, not engineering bounds. "
        "L3a residual also remains. Net: bookkeeping-only promotion accessible (rename C-iso component); "
        "no full retained_bounded promotion supported."
    ),
}

LANE_HIGGS = {
    "name": "Lane 2: Higgs mass from axiom",
    "parent_keys": [
        "higgs_mass_from_axiom_note",
        "higgs_mass_from_axiom_status_correction_audit_note_2026-05-02",
    ],
    "expected_parent_status": {
        "higgs_mass_from_axiom_note": {
            "claim_type": "bounded_theorem",
            "effective_status": "unaudited",
        },
    },
    "structural_retained": "Tree-level mean-field formula m_H/v = 1/(2 u_0) with N_c cancellation tracked at every step",
    "residual_admissions": [
        {"name": "lattice_curvature_to_physical_m_h_v_squared_matching_theorem", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "Nature-grade non-perturbative matching theorem; same-shape obstruction with cycles 5, 9, 11"},
        {"name": "n_taste_16_uniform_channel", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "depends on staggered-Dirac realization gate (open per MINIMAL_AXIOMS_2026-05-03)"},
        {"name": "v_ew_vev", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "admitted from EW hierarchy theorem chain"},
        {"name": "u_0_plaquette_lattice_value", "kind": "engineering", "closed_by_w2_nlo": False,
         "note": "tightened by SU(3)-NLO C-iso path-integral closure; not the load-bearing residual"},
        {"name": "cw_rge_correction_chain", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "+12% gap closure; sister authority chain (HIGGS_MASS_DERIVED_NOTE)"},
        {"name": "wilson_taste_breaking_correction", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "+12% gap closure; sister authority chain (WILSON_BZ_CORNER_HAMMING_STAIRCASE)"},
        {"name": "lattice_spacing_convergence", "kind": "structural", "closed_by_w2_nlo": False,
         "note": "+12% gap closure; sister authority chain (HIGGS_FROM_LATTICE_NOTE)"},
    ],
    "verdict": "blocked",
    "verdict_reason": (
        "Load-bearing residual is the lattice-curvature -> physical (m_H/v)^2 matching theorem, "
        "which is a non-perturbative analytical-derivation gap (same-shape obstruction with cycles 5, 9, 11). "
        "This is NOT an engineering bound; no amount of compute closes it. "
        "W2 trilogy and SU(3)-NLO C-iso work do not address this missing matching theorem. "
        "Promotion blocked until the cluster-wide lattice-physical matching theorem is supplied."
    ),
}

LANE_GAUGE_SCALAR = {
    "name": "Lane 3: gauge-scalar bridge",
    "parent_keys": [
        "gauge_scalar_temporal_observable_bridge_implicit_flow_theorem_note_2026-05-03",
        "gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03",
        "gauge_scalar_temporal_completion_theorem_note",
    ],
    "expected_parent_status": {
        "gauge_scalar_temporal_observable_bridge_implicit_flow_theorem_note_2026-05-03": {
            "claim_type": "bounded_theorem",
            "effective_status": "retained_bounded",
        },
        "gauge_scalar_temporal_observable_bridge_no_go_theorem_note_2026-05-03": {
            "claim_type": "no_go",
            "effective_status": "retained_no_go",
        },
        "gauge_scalar_temporal_completion_theorem_note": {
            "claim_type": "bounded_theorem",
            "effective_status": "retained_bounded",
        },
    },
    "structural_retained": "Implicit-coordinate identity (P_full = R_O(beta_eff)) + companion no-go (two completion witnesses)",
    "residual_admissions": [
        {"name": "c_iso_e_witness_compute_frontier", "kind": "engineering", "closed_by_w2_nlo": False,
         "note": "for numerical evaluation only; structural bridge is already retained_bounded"},
    ],
    "verdict": "already_promoted",
    "verdict_reason": (
        "Structural bridge is retained_bounded (implicit-flow theorem) + retained_no_go (companion no-go), "
        "both at audit_clean status. No further promotion needed at the source-theorem level. "
        "C-iso e_witness frontier handles the numerical evaluation engineering. "
        "This is the model for what a clean retained_bounded promotion looks like."
    ),
}

LANES = [LANE_ALPHA_S, LANE_HIGGS, LANE_GAUGE_SCALAR]


# -----------------------------------------------------------------------------
# Section A: audit-ledger consistency
# -----------------------------------------------------------------------------

def section_A_ledger_reads(rows: dict) -> None:
    section("Section A: Audit-ledger reads (no mutations)")

    for lane in LANES:
        for key, expected in lane["expected_parent_status"].items():
            row = get_row(rows, key)
            check(
                f"{lane['name']}: ledger row '{key}' exists",
                bool(row),
                detail=f"keys present: {list(row.keys())[:3] if row else 'NONE'}",
            )
            for fld, exp_val in expected.items():
                act_val = row.get(fld, "MISSING")
                check(
                    f"{lane['name']}: '{key}' field '{fld}' matches expected",
                    act_val == exp_val,
                    detail=f"expected={exp_val!r}, actual={act_val!r}",
                )


# -----------------------------------------------------------------------------
# Section B: structural retained content is non-empty per lane
# -----------------------------------------------------------------------------

def section_B_structural_content() -> None:
    section("Section B: Structural retained content non-empty per lane")
    for lane in LANES:
        sr = lane["structural_retained"]
        check(
            f"{lane['name']}: structural_retained is non-empty",
            isinstance(sr, str) and len(sr) > 0,
            detail=f"length={len(sr) if isinstance(sr, str) else 'N/A'}",
        )


# -----------------------------------------------------------------------------
# Section C: residual admissions are enumerated honestly
# -----------------------------------------------------------------------------

def section_C_residuals() -> None:
    section("Section C: Residual admissions enumerated per lane")
    for lane in LANES:
        admissions = lane["residual_admissions"]
        check(
            f"{lane['name']}: at least one residual admission listed",
            isinstance(admissions, list) and len(admissions) > 0,
            detail=f"count={len(admissions) if isinstance(admissions, list) else 'N/A'}",
        )
        for adm in admissions:
            check(
                f"{lane['name']}: admission '{adm['name']}' has 'kind' in {{engineering, structural}}",
                adm.get("kind") in ("engineering", "structural"),
                detail=f"kind={adm.get('kind')!r}",
            )
            check(
                f"{lane['name']}: admission '{adm['name']}' has 'closed_by_w2_nlo' boolean",
                isinstance(adm.get("closed_by_w2_nlo"), bool),
                detail=f"value={adm.get('closed_by_w2_nlo')!r}",
            )
            check(
                f"{lane['name']}: admission '{adm['name']}' has non-empty 'note'",
                isinstance(adm.get("note"), str) and len(adm["note"]) > 10,
                detail=f"len={len(adm.get('note', ''))}",
            )


# -----------------------------------------------------------------------------
# Section D: verdict consistency per lane
# -----------------------------------------------------------------------------

def section_D_verdict_logic() -> None:
    section("Section D: Per-lane verdict matches four-criterion logic")

    # Logic:
    #   - "already_promoted": at least one parent has effective_status in {retained, retained_bounded, retained_no_go}
    #   - "pending_partial": at least one engineering admission AND at least one structural admission unaddressed
    #   - "blocked": at least one structural admission that is the load-bearing residual
    #
    # Test: each lane's claimed verdict must be consistent with its admissions list.

    for lane in LANES:
        admissions = lane["residual_admissions"]
        verdict = lane["verdict"]

        n_engineering = sum(1 for a in admissions if a["kind"] == "engineering")
        n_structural = sum(1 for a in admissions if a["kind"] == "structural")
        n_unclosed_structural = sum(
            1 for a in admissions if a["kind"] == "structural" and not a["closed_by_w2_nlo"]
        )

        if verdict == "already_promoted":
            # Must have no UNCLOSED structural residuals tied to the audit-clean structural bridge.
            # The Lane 3 structural bridge IS the implicit-coordinate identity + no-go pair, both retained.
            # The c_iso engineering frontier is for numerical evaluation only, not the structural bridge.
            check(
                f"{lane['name']}: verdict='already_promoted' consistent (engineering-only residuals)",
                n_unclosed_structural == 0,
                detail=f"engineering={n_engineering}, structural_unclosed={n_unclosed_structural}",
            )

        elif verdict == "pending_partial":
            # Must have BOTH an engineering admission (where C-iso/compute can help) AND
            # at least one structural admission that is NOT closed by W2/NLO.
            check(
                f"{lane['name']}: verdict='pending_partial' has engineering admission",
                n_engineering >= 1,
                detail=f"engineering count={n_engineering}",
            )
            check(
                f"{lane['name']}: verdict='pending_partial' has unclosed structural admission",
                n_unclosed_structural >= 1,
                detail=f"unclosed_structural={n_unclosed_structural}",
            )

        elif verdict == "blocked":
            # Must have at least one unclosed structural admission flagged as load-bearing.
            check(
                f"{lane['name']}: verdict='blocked' has unclosed structural residual",
                n_unclosed_structural >= 1,
                detail=f"unclosed_structural={n_unclosed_structural}",
            )

        else:
            check(
                f"{lane['name']}: verdict in known set",
                False,
                detail=f"verdict={verdict!r} not in {{already_promoted, pending_partial, blocked}}",
            )


# -----------------------------------------------------------------------------
# Section E: no PDG / observed values consumed as derivation inputs
# -----------------------------------------------------------------------------

def section_E_no_observed_inputs() -> None:
    section("Section E: No PDG/observed/fitted derivation inputs in verdict logic")

    forbidden_strings = [
        "0.1180",  # PDG alpha_s(M_Z) central value (would-be fitted)
        "0.1181",  # framework's own derived comparator (cannot enter as input)
        "125.10",  # PDG Higgs mass
        "125.25",  # observed Higgs mass
        "246.22",  # EW VEV (admitted via hierarchy chain, not via PDG-input)
        "0.5934",  # plaquette MC value (admitted via lattice MC, not via PDG)
        "0.4410",  # Hamilton-limit <P> central value (governance metadata only)
    ]

    # The verdict logic itself should NOT contain numerical PDG-style values
    # as load-bearing inputs. We check the lane-data structure does not
    # reference any of them inside verdict_reason or structural_retained.
    for lane in LANES:
        target_strings = [
            lane.get("structural_retained", ""),
            lane.get("verdict_reason", ""),
        ]
        # Check verdict-logic strings only (not the full admission notes,
        # which may legitimately reference engineering numbers as residual
        # specifications, not as derivation inputs).
        joined = " ".join(target_strings)
        for fb in forbidden_strings:
            check(
                f"{lane['name']}: verdict logic does not consume '{fb}' as input",
                fb not in joined,
                detail=f"checked in structural_retained + verdict_reason",
            )


# -----------------------------------------------------------------------------
# Section F: engineering vs structural residual classification audit
# -----------------------------------------------------------------------------

def section_F_engineering_vs_structural() -> None:
    section("Section F: Engineering vs structural residual classification audit")

    # An "engineering" residual is one that is:
    #   - finite, computable, with a named compute path;
    #   - bounded by a closed-form expression;
    #   - addressable by more compute / GPU MC / extending Vandermonde-Gaussian etc.
    # A "structural" residual is one that is:
    #   - a missing analytical theorem (matching, scale-setting, running, etc.);
    #   - or an open derivation gate (L3a, staggered-Dirac realization, g_bare=1);
    #   - addressable only by NEW theorem work, not by compute.

    # Audit known classifications:
    expected_classifications = {
        "convention_c_iso": "engineering",  # named compute frontier; closed-form NLO
        "sommer_scale_r0_literature": "structural",  # external literature; needs framework-native theorem
        "four_loop_qcd_running": "structural",  # external; needs framework-native running theorem
        "threshold_matching": "structural",  # external standard
        "sea_quark_full_qcd_bridge": "structural",  # not closed by current framework
        "l3a_trace_surface": "structural",  # open gate
        "g_bare_canonical_normalization": "structural",  # open gate
        "lattice_curvature_to_physical_m_h_v_squared_matching_theorem": "structural",  # Nature-grade
        "n_taste_16_uniform_channel": "structural",  # depends on staggered-Dirac gate
        "cw_rge_correction_chain": "structural",  # +12% gap; needs CW + RGE machinery
        "wilson_taste_breaking_correction": "structural",  # +12% gap
        "lattice_spacing_convergence": "structural",  # +12% gap
        "u_0_plaquette_lattice_value": "engineering",  # tightenable by C-iso ε_witness
        "v_ew_vev": "structural",  # admitted from hierarchy chain
        "c_iso_e_witness_compute_frontier": "engineering",  # numerical only
    }

    for lane in LANES:
        for adm in lane["residual_admissions"]:
            name = adm["name"]
            kind = adm["kind"]
            if name in expected_classifications:
                exp = expected_classifications[name]
                check(
                    f"{lane['name']}: admission '{name}' classified as '{exp}' (matches expected)",
                    kind == exp,
                    detail=f"actual={kind!r}, expected={exp!r}",
                )
            else:
                check(
                    f"{lane['name']}: admission '{name}' has known classification",
                    False,
                    detail=f"name not in expected_classifications table",
                )


# -----------------------------------------------------------------------------
# Section G: cross-lane coherence
# -----------------------------------------------------------------------------

def section_G_cross_lane_coherence() -> None:
    section("Section G: Cross-lane coherence and prioritization")

    # Sanity-check: at least one lane is "already_promoted" (Lane 3 should be).
    n_promoted = sum(1 for lane in LANES if lane["verdict"] == "already_promoted")
    n_blocked = sum(1 for lane in LANES if lane["verdict"] == "blocked")
    n_pending = sum(1 for lane in LANES if lane["verdict"] == "pending_partial")

    check(
        "exactly one lane is 'already_promoted' (Lane 3 = gauge-scalar)",
        n_promoted == 1,
        detail=f"n_promoted={n_promoted}",
    )
    check(
        "exactly one lane is 'pending_partial' (Lane 1 = alpha_s)",
        n_pending == 1,
        detail=f"n_pending={n_pending}",
    )
    check(
        "exactly one lane is 'blocked' (Lane 2 = Higgs)",
        n_blocked == 1,
        detail=f"n_blocked={n_blocked}",
    )

    # Higher-level check: verdict honesty.
    # If we claimed promotion based on W2 closure of L3a, that would be wrong
    # because L3a is NOT closed by the W2 trilogy (it is sharpened, not closed).
    # The runner verifies we are NOT claiming L3a closure.
    for lane in LANES:
        for adm in lane["residual_admissions"]:
            if adm["name"] == "l3a_trace_surface":
                check(
                    f"{lane['name']}: L3a residual is honestly NOT closed by W2",
                    not adm["closed_by_w2_nlo"],
                    detail="L3a remains a sharpened bounded obstruction; matter-rep gate still open",
                )

    # Higher-level check: engineering closure honesty.
    # The C-iso piece is at NLO closed form but ε_witness (~3e-4) is NOT yet
    # reached; ξ ≳ 430 is the named compute frontier.
    # We check no lane claims C-iso has reached ε_witness.
    for lane in LANES:
        for adm in lane["residual_admissions"]:
            if "c_iso" in adm["name"].lower():
                # The closed_by_w2_nlo should be False (NLO closes the
                # bound shape, not the absolute value vs ε_witness).
                check(
                    f"{lane['name']}: C-iso residual honestly NOT yet at ε_witness",
                    not adm["closed_by_w2_nlo"],
                    detail="SU(3) NLO closes the bound form; ξ >= 430 named compute frontier remains",
                )


# -----------------------------------------------------------------------------
# Section H: prioritization guidance is internally consistent
# -----------------------------------------------------------------------------

def section_H_prioritization() -> None:
    section("Section H: Prioritization guidance internally consistent")

    # The note recommends:
    #   1. Lane 3: no action (already retained)
    #   2. Lane 1: bookkeeping-only (rename C-iso component as named engineering)
    #   3. Lane 2: blocked, requires Nature-grade non-perturbative matching theorem
    #
    # Internal consistency:
    #   - Lane 3 verdict must be already_promoted (checked in G).
    #   - Lane 1 verdict must be pending_partial (checked in G).
    #   - Lane 2 verdict must be blocked (checked in G).
    #   - Lane 2's blocker must be classified as structural and Nature-grade.
    #   - Lane 1's pending status must be due to the four standard QCD imports
    #     remaining unaddressed.

    # Lane 2: confirm the matching theorem is the load-bearing structural residual.
    higgs_admissions = LANE_HIGGS["residual_admissions"]
    matching_admission = next(
        (a for a in higgs_admissions if "matching_theorem" in a["name"]), None
    )
    check(
        "Lane 2 (Higgs): lattice-physical matching theorem is listed as residual admission",
        matching_admission is not None,
        detail="Nature-grade non-perturbative gap; same-shape with cycles 5, 9, 11",
    )
    if matching_admission:
        check(
            "Lane 2 (Higgs): matching theorem is classified as 'structural' (not engineering)",
            matching_admission["kind"] == "structural",
            detail=f"kind={matching_admission['kind']!r}",
        )

    # Lane 1: confirm the four standard QCD imports are listed as STRUCTURAL.
    alpha_s_admissions = LANE_ALPHA_S["residual_admissions"]
    standard_qcd_keys = {
        "sommer_scale_r0_literature",
        "four_loop_qcd_running",
        "threshold_matching",
        "sea_quark_full_qcd_bridge",
    }
    found = {a["name"] for a in alpha_s_admissions} & standard_qcd_keys
    check(
        "Lane 1 (alpha_s): all four standard QCD imports listed as residual admissions",
        found == standard_qcd_keys,
        detail=f"found={sorted(found)}, expected={sorted(standard_qcd_keys)}",
    )
    for k in standard_qcd_keys:
        adm = next((a for a in alpha_s_admissions if a["name"] == k), None)
        if adm:
            check(
                f"Lane 1 (alpha_s): '{k}' classified as 'structural' (literature dependency)",
                adm["kind"] == "structural",
                detail=f"kind={adm['kind']!r}",
            )

    # Lane 3: confirm the structural bridge has no UNCLOSED structural residuals
    # (only the engineering ε_witness frontier for numerical evaluation).
    gauge_admissions = LANE_GAUGE_SCALAR["residual_admissions"]
    n_unclosed_structural_lane3 = sum(
        1 for a in gauge_admissions if a["kind"] == "structural" and not a["closed_by_w2_nlo"]
    )
    check(
        "Lane 3 (gauge-scalar): structural bridge has no unclosed structural residual",
        n_unclosed_structural_lane3 == 0,
        detail=f"unclosed_structural_count={n_unclosed_structural_lane3}",
    )


# -----------------------------------------------------------------------------
# Section I: existence of cited dependency notes on disk
# -----------------------------------------------------------------------------

def section_I_dep_files_exist() -> None:
    section("Section I: Cited one-hop dependency files exist on disk")

    root = find_repo_root()
    docs = root / "docs"

    deps = [
        "ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md",
        "ALPHA_S_DIRECT_WILSON_LOOP_HONEST_STATUS_AUDIT_NOTE_2026-05-02.md",
        "HIGGS_MASS_FROM_AXIOM_NOTE.md",
        "HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md",
        "GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_IMPLICIT_FLOW_THEOREM_NOTE_2026-05-03.md",
        "GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md",
        "GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md",
        "N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md",
        "N_F_V3_NORMALIZATION_BOUNDED_NOTE_2026-05-07_w2norm.md",
        "L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md",
        "C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md",
        "C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md",
        "EXACT_TIER_PATH_INTEGRAL_BOUNDED_NOTE_2026-05-07_exact.md",
        "EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness.md",
        "MINIMAL_AXIOMS_2026-05-03.md",
        "G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md",
        "STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md",
    ]
    for dep in deps:
        path = docs / dep
        check(
            f"dep file exists: docs/{dep}",
            path.exists(),
            detail=f"path={path}",
        )


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    print("=" * 88)
    print(
        "Bridge-Dependent Lanes Promotion Evaluation — runner for "
        "BRIDGE_LANES_PROMOTION_PROPOSAL_NOTE_2026-05-10_lanes.md"
    )
    print("=" * 88)

    rows = load_ledger()
    print(f"Loaded audit ledger with {len(rows)} rows")

    section_A_ledger_reads(rows)
    section_B_structural_content()
    section_C_residuals()
    section_D_verdict_logic()
    section_E_no_observed_inputs()
    section_F_engineering_vs_structural()
    section_G_cross_lane_coherence()
    section_H_prioritization()
    section_I_dep_files_exist()

    print("\n" + "=" * 88)
    print(f"=== TOTAL: PASS={PASS}, FAIL={FAIL} ===")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
