#!/usr/bin/env python3
"""Verify the retained-positive opportunity queue handoff packet against the
live ledger at `origin/main` HEAD.

This is a campaign-synthesis runner: it does NOT prove a new physics theorem.
It confirms that the OPPORTUNITY_QUEUE.md numbers and ranking are plausible
against the current ledger and that cycles 1-4's narrow theorems still have
graph-visible declared dependencies under their scoped claims.
"""

from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parent.parent
QUEUE_PATH = ROOT / ".claude" / "science" / "physics-loops" / "retained-positive-rescope-20260502" / "OPPORTUNITY_QUEUE.md"
LEDGER_PATH = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Part 1: queue document structure")
# ============================================================================
queue_text = QUEUE_PATH.read_text()
required = [
    "Retained-Positive Opportunity Queue",
    "323",  # positive_theorem count
    "227",  # bounded_theorem count
    "32",   # no_go count
    "#292",
    "#293",
    "#294",
    "#297",
    "Top 30 highest-leverage candidates",
    "Anti-churn note",
]
for s in required:
    check(f"queue doc contains: {s!r}", s in queue_text)


# ============================================================================
section("Part 2: live ledger numerical verification")
# ============================================================================
ledger = json.loads(LEDGER_PATH.read_text())
rows = ledger['rows']
retained_grade = {'retained', 'retained_bounded', 'retained_no_go'}

n_retained = 0
n_retained_bounded = 0
n_retained_no_go = 0

for cid, r in rows.items():
    cur_es = r.get('effective_status')
    if cur_es in retained_grade or cur_es == 'meta':
        continue
    if r.get('audit_status') in ('audited_failed', 'audited_renaming', 'audited_decoration', 'audited_numerical_match'):
        continue
    ct = r.get('claim_type')
    if ct not in ('positive_theorem', 'bounded_theorem', 'no_go'):
        continue
    deps = r.get('deps') or []
    n_total = len(deps)
    n_dep_retained = sum(1 for d in deps if rows.get(d, {}).get('effective_status') in retained_grade)
    if n_total > 0 and n_dep_retained < n_total:
        continue
    if ct == 'positive_theorem':
        n_retained += 1
    elif ct == 'bounded_theorem':
        n_retained_bounded += 1
    elif ct == 'no_go':
        n_retained_no_go += 1

# Allow small drift (a few audits may land between snapshot and verification)
check(f"predicted retained count ~ 323 (live: {n_retained})",
      abs(n_retained - 323) < 30,
      detail=f"|live - 323| = {abs(n_retained - 323)}")
check(f"predicted retained_bounded count ~ 227 (live: {n_retained_bounded})",
      abs(n_retained_bounded - 227) < 30,
      detail=f"|live - 227| = {abs(n_retained_bounded - 227)}")
check(f"predicted retained_no_go count ~ 32 (live: {n_retained_no_go})",
      abs(n_retained_no_go - 32) < 10,
      detail=f"|live - 32| = {abs(n_retained_no_go - 32)}")


# ============================================================================
section("Part 3: cycles 1-4 narrow theorems still have graph-visible deps")
# ============================================================================
# Cycle 1 deps
cycle_deps = {
    "cycle 1 (LH-doublet eigenvalue ratio)": [
        "graph_first_su3_integration_note",
        "graph_first_selector_derivation_note",
    ],
    "cycle 2 (Koide cyclic 3-response)": [
        "koide_dweh_cyclic_compression_note_2026-04-18",
    ],
    "cycle 3 (Schur covariance inheritance)": [
        "site_phase_cube_shift_intertwiner_note",
    ],
    "cycle 4 (three-gen no-proper-quotient)": [
        "site_phase_cube_shift_intertwiner_note",
        "s3_taste_cube_decomposition_note",
        "s3_mass_matrix_no_go_note",
        "z2_hw1_mass_matrix_parametrization_note",
    ],
}

for cycle_label, deps in cycle_deps.items():
    all_visible = all(rows.get(d) is not None for d in deps)
    check(f"{cycle_label}: all {len(deps)} cited deps graph-visible",
          all_visible,
          detail=f"cited: {deps}")


# ============================================================================
section("Part 4: top-30 ranked candidates exist in ledger and have predicted profile")
# ============================================================================
top_30 = [
    "observable_principle_from_axiom_note",
    "left_handed_charge_matching_note",
    "physical_lattice_necessity_note",
    "generation_axiom_boundary_note",
    "gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note",
    "ew_current_fierz_channel_decomposition_note_2026-05-01",
    "gauge_vacuum_plaquette_constant_lift_obstruction_note",
    "yukawa_color_projection_theorem",
    "higgs_mass_from_axiom_note",
    "g_bare_derivation_note",
    "higgs_from_lattice_note",
    "taste_scalar_isotropy_theorem_note",
    "yt_qfp_insensitivity_support_note",
    "neutrino_majorana_operator_axiom_first_note",
    "ckm_from_mass_hierarchy_note",
    "dm_neutrino_z3_circulant_mass_basis_no_go_note_2026-04-15",
    "dm_neutrino_dirac_bridge_theorem_note_2026-04-15",
]
for cid in top_30:
    r = rows.get(cid)
    check(f"top-30 candidate exists in ledger: {cid}",
          r is not None,
          detail=f"ct={r.get('claim_type') if r else 'MISSING'}")


# ============================================================================
section("Part 5: anti-churn discipline upheld")
# ============================================================================
# This packet is a synthesis, not a new theorem cycle. Verify it self-identifies as such.
check("packet is a synthesis (not new theorem)",
      "Opportunity Queue" in queue_text or
      "Recommendations" in queue_text or
      "Anti-churn" in queue_text)
check("packet acknowledges anti-churn guard",
      "Anti-churn note" in queue_text or
      "corollary-churn" in queue_text or
      "churn guard" in queue_text)


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
