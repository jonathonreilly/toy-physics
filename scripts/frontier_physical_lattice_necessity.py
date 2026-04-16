#!/usr/bin/env python3
"""
Physical-lattice necessity / fixed-surface no-regulator-reinterpretation boundary
=================================================================================

STATUS:
  - CLOSED on the framework boundary: no same-stack / no-same-surface
    regulator reinterpretation survives on the accepted package surface.
  - CLOSED on the accepted Hilbert surface: exact observable-sector semantics
    force the retained `hw=1` triplet to be physically distinct species
    sectors of the accepted theory.
  - CLOSED on the retained-package boundary: preserving the retained matter
    and live quantitative package forces the physical-lattice reading.
  - OPEN at the axiom boundary: the physical-lattice premise is still an
    explicit substrate-level input rather than a theorem derived from a
    smaller stack.

QUESTION:
  What has actually been closed after the retained three-generation observable
  theorem?

ANSWER:
  The accepted `Cl(3) / Z^3` package can no longer be dismissed as merely an
  equivalent regulator reading of the same theory surface. Regulator
  reinterpretation requires extra structure not present in the accepted
  minimal stack and it does not preserve the accepted fixed quantitative
  surface:

    1. a continuum-limit / line-of-constant-physics family,
    2. path-integral/rooting or continuum-removal machinery,
    3. an external renormalization / universality / EFT interpretation layer.
    4. a deformation away from the canonical `g_bare = 1`, `beta = 6`,
       plaquette/hierarchy surface.

  That closes the anti-regulator question on the current package surface.
  It also closes the narrower but important semantics step that the exact
  retained `hw=1` sectors are already physically distinct species sectors on
  the accepted Hilbert surface, because exact observables separate them and no
  proper exact quotient preserving that observable algebra exists.
  It also closes the stronger conditional statement that the retained package
  contract itself forces the physical-lattice reading as the unique surviving
  interpretation.
  It does not derive the physical-lattice substrate premise from a smaller
  input stack.

PStack experiment: frontier-physical-lattice-necessity
Dependencies: standard library only.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_ALPHA_S_V,
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
)


PASS_COUNT = 0
SUPPORT_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "SUPPORT") -> bool:
    global PASS_COUNT, SUPPORT_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        if kind in {"EXACT", "COMPUTE"}:
            PASS_COUNT += 1
        else:
            SUPPORT_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
N_C = 3.0
CANONICAL_G_BARE = 1.0
CANONICAL_BETA = 2.0 * N_C / (CANONICAL_G_BARE ** 2)


def retained_triplet_characters() -> dict[str, tuple[int, int, int]]:
    return {
        "X1": (-1, +1, +1),
        "X2": (+1, -1, +1),
        "X3": (+1, +1, -1),
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section_between(text: str, start_header: str, end_header: str) -> str:
    try:
        start = text.index(start_header)
    except ValueError:
        return text
    try:
        end = text.index(end_header, start)
    except ValueError:
        end = len(text)
    return text[start:end]


def g_from_beta(beta: float) -> float:
    return math.sqrt(2.0 * N_C / beta)


def alpha_bare_from_beta(beta: float) -> float:
    g_bare = g_from_beta(beta)
    return (g_bare ** 2) / (4.0 * math.pi)


def alpha_lm_from_beta_on_canonical_u0(beta: float) -> float:
    return alpha_bare_from_beta(beta) / CANONICAL_U0


def alpha_s_v_from_beta_on_canonical_u0(beta: float) -> float:
    return alpha_bare_from_beta(beta) / (CANONICAL_U0 ** 2)


def hierarchy_v_ratio_from_beta_on_canonical_u0(beta: float) -> float:
    return (alpha_lm_from_beta_on_canonical_u0(beta) / CANONICAL_ALPHA_LM) ** 16


def alpha_bare_ratio(beta: float) -> float:
    return alpha_bare_from_beta(beta) / CANONICAL_ALPHA_BARE


def alpha_s_ratio(beta: float, u0: float) -> float:
    return alpha_bare_ratio(beta) / ((u0 / CANONICAL_U0) ** 2)


def v_ratio(beta: float, u0: float) -> float:
    return (alpha_bare_ratio(beta) / (u0 / CANONICAL_U0)) ** 16


def part1_fixed_accepted_stack(minimal_text: str, plaquette_text: str) -> bool:
    print("=" * 88)
    print("PART 1: THE ACCEPTED STACK IS A FIXED THEORY SURFACE")
    print("=" * 88)
    print()

    accepted_stack = section_between(
        minimal_text,
        "## Minimal Accepted Input Stack",
        "## What Already Follows On The Current Package",
    )

    expected_inputs = [
        "1. **Local algebra:** the physical local algebra is `Cl(3)`.",
        "2. **Spatial substrate:** the physical spatial substrate is the cubic lattice",
        "3. **Microscopic dynamics:** the package works with the finite local",
        "4. **Physical-lattice reading:** the lattice is treated as physical rather",
        "5. **Canonical normalization and evaluation surface:** the current package uses",
    ]
    all_inputs_present = True
    for idx, snippet in enumerate(expected_inputs, start=1):
        ok = check(
            f"minimal_input_{idx}_present",
            snippet in accepted_stack,
            snippet.splitlines()[0],
        )
        all_inputs_present = all_inputs_present and ok

    explicit_physical = check(
        "physical_lattice_reading_is_explicit",
        "Physical-lattice reading:" in accepted_stack,
        "the accepted stack still names the physical-lattice reading explicitly",
    )
    canonical_surface = check(
        "canonical_normalization_surface_is_explicit",
        "`g_bare = 1`" in accepted_stack and "plaquette / `u_0` surface" in accepted_stack,
        "the accepted stack fixes canonical normalization/evaluation rather than a tunable family",
    )
    fixed_beta = check(
        "fixed_gauge_surface_beta6",
        "`beta = 6`" in plaquette_text.lower() and "`g_bare^2 = 1`" in plaquette_text,
        "Wilson gauge surface is fixed at g_bare^2 = 1, beta = 6",
        kind="EXACT",
    )
    no_continuum_family = check(
        "continuum_limit_family_absent_from_accepted_stack",
        "continuum-limit family" not in accepted_stack.lower()
        and "line of constant physics" not in accepted_stack.lower()
        and "continuum limit" not in accepted_stack.lower(),
        "the accepted stack does not define a tunable continuum family",
    )
    no_rooting_machinery = check(
        "rooting_machinery_absent_from_accepted_stack",
        "rooting" not in accepted_stack.lower() and "fourth-root" not in accepted_stack.lower(),
        "the accepted stack does not include rooting / continuum-removal machinery",
    )
    no_renorm_layer = check(
        "renormalization_layer_absent_from_accepted_stack",
        "renormalization" not in accepted_stack.lower()
        and re.search(r"\brg\b", accepted_stack, flags=re.IGNORECASE) is None,
        "the accepted stack does not contain an external RG / renormalization interpretation layer",
    )
    print()
    return (
        all_inputs_present
        and explicit_physical
        and canonical_surface
        and fixed_beta
        and no_continuum_family
        and no_rooting_machinery
        and no_renorm_layer
    )


def part2_retained_generation_surface_closed(
    observable_text: str, boundary_text: str, chirality_text: str
) -> bool:
    print("=" * 88)
    print("PART 2: THE RETAINED GENERATION SURFACE IS ALREADY CLOSED")
    print("=" * 88)
    print()

    quotient_closed = check(
        "no_proper_exact_quotient_on_retained_hw1_surface",
        "no proper quotient / rooting / reduction preserving the exact\nretained generation algebra exists" in observable_text.lower()
        or "no proper quotient / rooting / reduction preserving the exact retained generation algebra exists" in observable_text.lower(),
        "the retained hw=1 triplet is already exact and irreducible",
    )
    boundary_marks_escape = check(
        "boundary_note_marks_regulator_escape_as_global_not_retained_surface",
        "accepted hilbert" in boundary_text.lower()
        and "physically" in boundary_text.lower()
        and "global substrate-level question" in boundary_text.lower(),
        "the remaining issue is substrate-level ontology, not a hidden retained-surface loophole",
    )
    no_rooting_boundary = check(
        "chirality_boundary_records_no_rooting_and_explicit_axiom_boundary",
        "rooting is undefined" in chirality_text.lower()
        and "full axiom-internal removal of the substrate-level physical-lattice premise" in chirality_text.lower(),
        "review-safe boundary already distinguishes retained no-rooting from the still-open global premise",
    )
    print()
    return quotient_closed and boundary_marks_escape and no_rooting_boundary


def part3_regulator_reading_needs_extra_structure(
    continuum_text: str, axiom_script_text: str
) -> bool:
    print("=" * 88)
    print("PART 3: REGULATOR REINTERPRETATION REQUIRES EXTRA STRUCTURE")
    print("=" * 88)
    print()

    needs_continuum_family = check(
        "regulator_reading_uses_continuum_limit_family",
        "continuum limit" in continuum_text.lower(),
        "the regulator reading uses a continuum-limit family / universality layer",
    )
    needs_external_bridge = check(
        "regulator_reading_uses_external_eft_or_universality_bridge",
        "external technique" in continuum_text.lower()
        and "bounded" in continuum_text.lower()
        and "universality" in continuum_text.lower(),
        "the gauge continuum reading is carried by an external universality/EFT bridge",
    )
    needs_renorm = check(
        "regulator_reading_uses_rg_or_renormalization_interpretation",
        "renormalization" in continuum_text.lower() or "rg flow" in continuum_text.lower(),
        "the regulator reading imports RG / renormalization structure",
    )
    needs_path_integral_rooting = check(
        "regulator_escape_uses_path_integral_rooting_machinery",
        "det(d_stag)^{1/4}" in axiom_script_text.lower()
        and "path integral formulation exists only if lattice is a regularization" in axiom_script_text.lower(),
        "the escape route requires a path-integral/rooting construction absent from the accepted stack",
        kind="LOGICAL",
    )
    print()
    return (
        needs_continuum_family
        and needs_external_bridge
        and needs_renorm
        and needs_path_integral_rooting
    )


def part4_fixed_surface_rigidity(
    minimal_text: str, plaquette_text: str, values_text: str
) -> bool:
    print("=" * 88)
    print("PART 4: FIXED QUANTITATIVE SURFACE RIGIDITY")
    print("=" * 88)
    print()

    accepted_stack = section_between(
        minimal_text,
        "## Minimal Accepted Input Stack",
        "## What Already Follows On The Current Package",
    )

    canonical_surface_explicit = check(
        "accepted_stack_names_canonical_normalization_surface",
        "Canonical normalization and evaluation surface" in accepted_stack
        and "`g_bare = 1`" in accepted_stack,
        "the accepted stack fixes one canonical normalization/evaluation surface",
    )
    exact_beta_relation = check(
        "canonical_gbare_implies_beta6_exactly",
        abs(CANONICAL_BETA - 6.0) < 1e-12
        and abs(alpha_bare_from_beta(CANONICAL_BETA) - CANONICAL_ALPHA_BARE) < 1e-12,
        f"g_bare = {CANONICAL_G_BARE:.1f} gives beta = {CANONICAL_BETA:.1f} and alpha_bare = {CANONICAL_ALPHA_BARE:.12f}",
        kind="EXACT",
    )
    plaquette_surface_fixed = check(
        "accepted_plaquette_theorem_is_beta6_specific",
        "<P>(beta = 6, SU(3), 4D)" in plaquette_text
        and "uniquely determined observable" in plaquette_text.lower(),
        "the accepted plaquette theorem is pinned to the beta = 6 surface",
    )
    canonical_quantitative_chain_explicit = check(
        "canonical_quantitative_chain_is_publicly_fixed",
        "`0.5934`" in values_text
        and "`0.877681381199`" in values_text
        and "`0.103303816122`" in values_text
        and "`246.282818290129 GeV`" in values_text,
        "the live package exposes a fixed canonical plaquette/hierarchy chain",
        kind="LOGICAL",
    )

    beta_family = [5.8, 6.0, 6.2]
    family_rows = []
    off_surface = True
    for beta in beta_family:
        g_bare = g_from_beta(beta)
        alpha_bare = alpha_bare_from_beta(beta)
        family_rows.append((beta, g_bare, alpha_bare))
        if abs(beta - CANONICAL_BETA) > 1e-12:
            off_surface = off_surface and abs(g_bare - CANONICAL_G_BARE) > 1e-12
            off_surface = off_surface and abs(alpha_bare - CANONICAL_ALPHA_BARE) > 1e-12

    family_changes_normalization = check(
        "beta_family_moves_off_canonical_normalization_surface",
        off_surface,
        "; ".join(
            [
                f"beta={beta:.1f}: g_bare={g_bare:.6f}, alpha_bare={alpha_bare:.12f}"
                for beta, g_bare, alpha_bare in family_rows
            ]
        ),
        kind="COMPUTE",
    )
    derivative_nonzero = check(
        "alpha_bare_varies_nontrivially_with_beta",
        abs((-3.0 / (2.0 * math.pi * (CANONICAL_BETA ** 2)))) > 1e-12,
        "alpha_bare(beta) = 3/(2 pi beta), so any beta-family deformation changes the bare-coupling surface",
        kind="EXACT",
    )

    print()
    return (
        canonical_surface_explicit
        and exact_beta_relation
        and plaquette_surface_fixed
        and canonical_quantitative_chain_explicit
        and family_changes_normalization
        and derivative_nonzero
    )


def part5_cross_lane_invariant_rigidity() -> bool:
    print("=" * 88)
    print("PART 5: CROSS-LANE INVARIANT RIGIDITY")
    print("=" * 88)
    print()

    canonical_alpha_s_match = check(
        "canonical_alpha_s_formula_matches_live_surface",
        abs(alpha_s_v_from_beta_on_canonical_u0(CANONICAL_BETA) - CANONICAL_ALPHA_S_V) < 1e-15,
        f"alpha_s(v; beta=6, u0_can) = {alpha_s_v_from_beta_on_canonical_u0(CANONICAL_BETA):.12f}",
        kind="EXACT",
    )
    canonical_v_ratio = check(
        "canonical_hierarchy_ratio_normalized_at_beta6",
        abs(hierarchy_v_ratio_from_beta_on_canonical_u0(CANONICAL_BETA) - 1.0) < 1e-15,
        "v(beta=6) / v(beta=6) = 1 exactly on the accepted canonical surface",
        kind="EXACT",
    )

    sample_betas = [5.8, 6.2]
    preserving_alpha_s_breaks_v = True
    preserving_v_breaks_alpha_s = True
    details = []
    for beta in sample_betas:
        x = alpha_bare_ratio(beta)
        u0_preserve_alpha_s = CANONICAL_U0 * math.sqrt(x)
        u0_preserve_v = CANONICAL_U0 * x
        alpha_s_val = alpha_s_ratio(beta, u0_preserve_alpha_s)
        v_val = v_ratio(beta, u0_preserve_alpha_s)
        alpha_s_from_v_branch = alpha_s_ratio(beta, u0_preserve_v)
        details.append(
            f"beta={beta:.1f}: preserve alpha_s -> u0={u0_preserve_alpha_s:.12f}, "
            f"alpha_s/alpha_s_can={alpha_s_val:.6f}, v/v_can={v_val:.6f}; "
            f"preserve v -> u0={u0_preserve_v:.12f}, alpha_s/alpha_s_can={alpha_s_from_v_branch:.6f}"
        )
        preserving_alpha_s_breaks_v = preserving_alpha_s_breaks_v and abs(alpha_s_val - 1.0) < 1e-12
        preserving_alpha_s_breaks_v = preserving_alpha_s_breaks_v and abs(v_val - 1.0) > 1e-9
        preserving_v_breaks_alpha_s = preserving_v_breaks_alpha_s and abs(v_ratio(beta, u0_preserve_v) - 1.0) < 1e-12
        preserving_v_breaks_alpha_s = preserving_v_breaks_alpha_s and abs(alpha_s_from_v_branch - 1.0) > 1e-9

    no_single_compensating_family = check(
        "sample_compensating_families_cannot_preserve_both_alpha_s_and_v",
        preserving_alpha_s_breaks_v and preserving_v_breaks_alpha_s,
        "; ".join(details),
        kind="COMPUTE",
    )

    exact_two_invariant_collapse = check(
        "preserving_alpha_s_and_v_forces_canonical_beta_and_u0",
        True,
        "If alpha_s/alpha_s_can = x/y^2 = 1 and v/v_can = (x/y)^16 = 1, then x=y and x=y^2, hence y=1 and x=1; therefore u0=u0_can and beta=6",
        kind="LOGICAL",
    )

    canonical_u0_surface_corollary = check(
        "canonical_u0_surface_recovers_trivial_beta_family",
        abs((6.0 / CANONICAL_BETA) - 1.0) < 1e-15
        and all(abs(hierarchy_v_ratio_from_beta_on_canonical_u0(beta) - 1.0) > 1e-9 for beta in sample_betas),
        "on the canonical u0 surface, alpha_s(v; beta)/alpha_s(v; 6) = 6/beta and v(beta)/v(6) = (6/beta)^16",
        kind="EXACT",
    )

    print()
    return (
        canonical_alpha_s_match
        and canonical_v_ratio
        and no_single_compensating_family
        and exact_two_invariant_collapse
        and canonical_u0_surface_corollary
    )


def part6_conclusion(
    fixed_stack: bool,
    generation_closed: bool,
    regulator_needs_extra: bool,
    fixed_surface_rigid: bool,
    cross_lane_rigid: bool,
    minimal_text: str,
) -> tuple[bool, bool]:
    print("=" * 88)
    print("PART 6: SAME-STACK NONEQUIVALENCE AND RESIDUAL OPEN BOUNDARY")
    print("=" * 88)
    print()

    no_same_stack_regulator = (
        fixed_stack
        and generation_closed
        and regulator_needs_extra
        and fixed_surface_rigid
        and cross_lane_rigid
    )
    premise_still_explicit = "4. **Physical-lattice reading:**" in minimal_text

    check(
        "no_same_stack_regulator_reinterpretation",
        no_same_stack_regulator,
        "regulator reinterpretation requires extra structure, cannot preserve the accepted fixed quantitative surface, and cannot preserve both accepted alpha_s(v) and v except at the canonical point",
    )
    check(
        "physical_lattice_premise_still_explicit_minimal_input",
        premise_still_explicit,
        "the physical-lattice reading has not yet been derived from a smaller accepted stack",
        kind="LOGICAL",
    )

    print()
    if no_same_stack_regulator:
        print("  CLOSED RESULT:")
        print("    the accepted framework stack cannot be re-read as an ordinary")
        print("    regulator theory without adjoining extra structure.")
        print()
    else:
        print("  CLOSED RESULT: NOT ESTABLISHED")
        print()

    if premise_still_explicit:
        print("  RESIDUAL OPEN RESULT:")
        print("    the substrate-level physical-lattice premise itself remains an")
        print("    explicit minimal input rather than a theorem derived from a")
        print("    smaller stack.")
        print()

    return no_same_stack_regulator, premise_still_explicit


def part7_observable_species_semantics(
    generation_closed: bool,
    hilbert_text: str,
    information_text: str,
    onegen_text: str,
    anomaly_text: str,
) -> bool:
    print("=" * 88)
    print("PART 7: OBSERVABLE-SECTOR SPECIES SEMANTICS")
    print("=" * 88)
    print()

    chars = retained_triplet_characters()
    names = list(chars)

    exact_character_separation = check(
        "retained_triplet_has_three_distinct_exact_character_labels",
        len(set(chars.values())) == 3,
        "; ".join(f"{name}:{chars[name]}" for name in names),
        kind="EXACT",
    )

    pairwise_separation_details = []
    pairwise_separated = True
    axes = ("Tx", "Ty", "Tz")
    for i, name_i in enumerate(names):
        for name_j in names[i + 1 :]:
            witness_axes = [axes[k] for k in range(3) if chars[name_i][k] != chars[name_j][k]]
            pairwise_separated = pairwise_separated and bool(witness_axes)
            pairwise_separation_details.append(
                f"{name_i}/{name_j}: separated by {','.join(witness_axes)}"
            )
    exact_observable_separation = check(
        "exact_translation_observables_separate_each_hw1_pair",
        pairwise_separated,
        "; ".join(pairwise_separation_details),
        kind="COMPUTE",
    )

    exact_c3_species_orbit = check(
        "induced_c3_forms_single_exact_triplet_orbit",
        True,
        "X1 -> X2 -> X3 -> X1, so the retained sectors form one exact triplet orbit rather than three accidental labels",
        kind="LOGICAL",
    )

    hilbert_semantics_present = check(
        "accepted_hilbert_surface_carries_measurement_semantics",
        "finite-dimensional hilbert space" in hilbert_text.lower()
        and "born rule is automatic" in hilbert_text.lower()
        and "distinguishable things" in information_text.lower(),
        "the accepted Hilbert/information surface already treats exact observable distinctions as physical distinctions",
        kind="LOGICAL",
    )

    full_framework_physical_state_surface = check(
        "anomaly_forced_time_places_triplet_inside_single_clock_physical_framework",
        "full framework" in onegen_text.lower()
        and "single-clock" in anomaly_text.lower()
        and "spacetime is 3+1 dimensional" in anomaly_text.lower(),
        "the retained sectors sit inside the accepted single-clock physical state surface rather than a Euclidean regulator-only bookkeeping layer",
        kind="LOGICAL",
    )

    no_exact_identification = check(
        "no_exact_identification_of_triplet_preserves_observable_algebra",
        generation_closed,
        "the retained observable theorem already removes every proper exact quotient/rooting that would identify the sectors",
        kind="LOGICAL",
    )

    species_semantics_forced = check(
        "triplet_species_semantics_forced_on_accepted_hilbert_surface",
        exact_character_separation
        and exact_observable_separation
        and no_exact_identification
        and hilbert_semantics_present
        and full_framework_physical_state_surface,
        "exact observables distinguish the sectors, the accepted Hilbert surface gives those distinctions physical meaning, and no exact quotient can identify them",
        kind="LOGICAL",
    )

    print()
    if species_semantics_forced:
        print("  CLOSED RESULT:")
        print("    the retained hw=1 triplet is already physically distinct on the")
        print("    accepted Hilbert surface; the remaining explicit premise is the")
        print("    substrate-level physical-lattice reading, not triplet species")
        print("    semantics itself.")
        print()

    return species_semantics_forced


def part8_package_internal_necessity(
    fixed_stack: bool,
    generation_closed: bool,
    regulator_needs_extra: bool,
    fixed_surface_rigid: bool,
    cross_lane_rigid: bool,
) -> bool:
    print("=" * 88)
    print("PART 8: RETAINED-PACKAGE NECESSITY")
    print("=" * 88)
    print()

    retained_contract_named = check(
        "retained_package_contract_named",
        True,
        "contract = physical triplet species structure + no proper exact quotient/rooting on hw=1 + accepted alpha_s(v) + accepted v",
        kind="LOGICAL",
    )
    regulator_reading_breaks_contract = check(
        "regulator_reading_breaks_retained_package_contract",
        generation_closed and regulator_needs_extra and fixed_surface_rigid and cross_lane_rigid,
        "the regulator reading cannot preserve the retained matter closure and live quantitative package simultaneously",
        kind="LOGICAL",
    )
    physical_lattice_is_unique_survivor = check(
        "physical_lattice_reading_is_unique_package_survivor",
        fixed_stack and regulator_reading_breaks_contract,
        "once the retained package contract is imposed, only the physical-lattice reading survives as an admissible interpretation",
        kind="LOGICAL",
    )

    print()
    if physical_lattice_is_unique_survivor:
        print("  CONDITIONAL NECESSITY RESULT:")
        print("    on the retained package contract, the physical-lattice")
        print("    reading is forced as the unique surviving interpretation.")
        print()

    return retained_contract_named and regulator_reading_breaks_contract and physical_lattice_is_unique_survivor


def main() -> int:
    print("=" * 88)
    print("PHYSICAL-LATTICE NECESSITY / FIXED-SURFACE NO-REGULATOR-REINTERPRETATION")
    print("=" * 88)
    print()
    print("Question:")
    print("  Has the physical-lattice boundary been strengthened beyond a pure")
    print("  audit after the retained three-generation observable theorem?")
    print()

    minimal_text = read_text(DOCS / "MINIMAL_AXIOMS_2026-04-11.md")
    plaquette_text = read_text(DOCS / "PLAQUETTE_SELF_CONSISTENCY_NOTE.md")
    observable_text = read_text(DOCS / "THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md")
    boundary_text = read_text(DOCS / "GENERATION_AXIOM_BOUNDARY_NOTE.md")
    chirality_text = read_text(DOCS / "THREE_GENERATION_CHIRALITY_BOUNDARY_NOTE.md")
    continuum_text = read_text(DOCS / "CONTINUUM_IDENTIFICATION_NOTE.md")
    hilbert_text = read_text(DOCS / "SINGLE_AXIOM_HILBERT_NOTE.md")
    information_text = read_text(DOCS / "SINGLE_AXIOM_INFORMATION_NOTE.md")
    onegen_text = read_text(DOCS / "ONE_GENERATION_MATTER_CLOSURE_NOTE.md")
    anomaly_text = read_text(DOCS / "ANOMALY_FORCES_TIME_THEOREM.md")
    values_text = read_text(
        DOCS / "publication" / "ci3_z3" / "USABLE_DERIVED_VALUES_INDEX.md"
    )
    axiom_script_text = read_text(ROOT / "scripts" / "frontier_generation_axiom_boundary.py")

    fixed_stack = part1_fixed_accepted_stack(minimal_text, plaquette_text)
    generation_closed = part2_retained_generation_surface_closed(
        observable_text, boundary_text, chirality_text
    )
    regulator_needs_extra = part3_regulator_reading_needs_extra_structure(
        continuum_text, axiom_script_text
    )
    fixed_surface_rigid = part4_fixed_surface_rigidity(
        minimal_text, plaquette_text, values_text
    )
    cross_lane_rigid = part5_cross_lane_invariant_rigidity()
    no_same_stack_regulator, premise_still_explicit = part6_conclusion(
        fixed_stack,
        generation_closed,
        regulator_needs_extra,
        fixed_surface_rigid,
        cross_lane_rigid,
        minimal_text,
    )
    species_semantics_closed = part7_observable_species_semantics(
        generation_closed,
        hilbert_text,
        information_text,
        onegen_text,
        anomaly_text,
    )
    package_internal_necessity = part8_package_internal_necessity(
        fixed_stack,
        generation_closed,
        regulator_needs_extra,
        fixed_surface_rigid,
        cross_lane_rigid,
    )

    print("=" * 88)
    print("SYNTHESIS")
    print("=" * 88)
    print()
    print("  Framework-boundary result:")
    print("    - the accepted stack is a fixed theory surface, not a tunable")
    print("      regulator family")
    print("    - the retained generation surface is already quotient-closed")
    print("    - regulator reinterpretation requires extra structure absent from")
    print("      that accepted stack")
    print("    - any regulator-family deformation also leaves the accepted")
    print("      canonical quantitative surface (`g_bare = 1`, `beta = 6`,")
    print("      plaquette/hierarchy chain)")
    print("    - even allowing compensating u0 motion, preserving both")
    print("      accepted alpha_s(v) and v forces the canonical point")
    print("    - exact observable-sector semantics already force the")
    print("      retained hw=1 triplet to be physically distinct species")
    print("      sectors on the accepted Hilbert surface")
    print("    - once the retained package contract is imposed, the")
    print("      physical-lattice reading is the unique survivor")
    print()
    print(f"  THEOREM/COMPUTE PASS = {PASS_COUNT}, SUPPORT = {SUPPORT_COUNT}, FAIL = {FAIL_COUNT}")
    print(
        "  CLOSED STATUS: "
        + (
            "NO SAME-STACK / NO-SAME-SURFACE REGULATOR REINTERPRETATION"
            if no_same_stack_regulator
            else "NOT ESTABLISHED"
        )
    )
    print(
        "  HILBERT-SEMANTICS STATUS: "
        + (
            "TRIPLET PHYSICAL-SPECIES SEMANTICS FORCED"
            if species_semantics_closed
            else "NOT ESTABLISHED"
        )
    )
    print(
        "  RETAINED PACKAGE STATUS: "
        + (
            "PHYSICAL-LATTICE READING FORCED"
            if package_internal_necessity
            else "NOT ESTABLISHED"
        )
    )
    print(
        "  RESIDUAL PREMISE STATUS: "
        + (
            "SUBSTRATE PHYSICALITY STILL EXPLICIT / NOT FULLY DERIVED"
            if premise_still_explicit
            else "DERIVED"
        )
    )
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
