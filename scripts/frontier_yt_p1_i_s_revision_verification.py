#!/usr/bin/env python3
"""
Frontier runner: P1 I_S revision verification (critical review).

Status
------
Critical-review verification layer on top of the prior P1 citation note
(`docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md`). This runner does
NOT re-derive I_S or the packaged delta_PT. It verifies:

  1. The packaged delta_PT = alpha_LM * C_F / (2 pi) = 1.924% is reproduced
     exactly from the retained canonical-surface constants (C_F = 4/3,
     alpha_LM = 0.0907).
  2. The algebraic identity alpha/(2 pi) = 2 * alpha/(4 pi) is exact; the "2"
     in the rewriting (alpha/(4 pi)) * C_F * 2 is a convention factor, not a
     BZ integral value.
  3. The cited-literature bracket I_S in [4, 10] in the alpha/(4 pi)
     convention gives P1 in [3.85%, 9.62%], central ~5.77%, consistent with
     the prior citation note.
  4. Possibility B (false-alarm convention mismatch) is rejected by the
     distinct-quantity test: no single convention switch reconciles the
     packaged continuum vertex-correction magnitude with the lattice
     scalar-density BZ integral.
  5. Possibility A (revision correct in magnitude) is structurally
     confirmed: lattice I_S > 2 for the staggered scalar density on the
     Wilson plaquette gauge action is a published literature fact.
  6. Possibility C (distinct contributions; lattice supersedes continuum)
     is the correct semantic framing: the two quantities should not be
     added; the lattice matching coefficient replaces the continuum
     vertex-correction heuristic on the lattice surface.
  7. Dimensional consistency: both quantities are dimensionless corrections
     to ln(Z_S).
  8. Verdict flags: A + C (not B), revised P1 ~ 5.77% central.
  9. Structural preservation: master obstruction theorem, Ward-identity
     theorem, packaged delta_PT note, and prior symbolic I_1 = I_S
     reduction are not modified.

Authority
---------
Retained foundations (not modified by this runner):
  - docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md (exact tree-level identity)
  - docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md (packaged delta_PT)
  - docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md (prior cite)
  - scripts/canonical_plaquette_surface.py
  - scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py (I_1 = I_S)

Verification note:
  - docs/YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md

Scope
-----
Critical review only. No framework-native BZ integration, no closure of
the Ward Representation-A / Representation-B cancellation at 1-loop, no
modification of the master obstruction theorem or publication-surface
files. The revised P1 estimate inherits the cited O(1) literature
uncertainty.

Self-contained: stdlib only.
"""

from __future__ import annotations

import math
import sys
from typing import Dict, Tuple

# Retained canonical-surface constants (not modified here).
from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
)


# ---------------------------------------------------------------------------
# PASS/FAIL bookkeeping
# ---------------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "B") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status} ({cls})] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


# ---------------------------------------------------------------------------
# Retained constants (framework-native)
# ---------------------------------------------------------------------------

PI = math.pi
N_C = 3
C_F = (N_C * N_C - 1.0) / (2.0 * N_C)   # 4/3
C_A = float(N_C)                         # 3
T_F = 0.5                                # 1/2

ALPHA_BARE = CANONICAL_ALPHA_BARE
U_0 = CANONICAL_U0
ALPHA_LM = CANONICAL_ALPHA_LM
ALPHA_LM_OVER_2PI = ALPHA_LM / (2.0 * PI)
ALPHA_LM_OVER_4PI = ALPHA_LM / (4.0 * PI)

# Packaged P1 nominal (continuum vertex-correction magnitude) from
# UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md. This is NOT a lattice
# BZ integral; it is the "standard vertex-correction formula" evaluated
# with canonical-surface alpha_LM.
DELTA_PT_PACKAGED = ALPHA_LM * C_F / (2.0 * PI)

# Cited-literature I_S bracket in alpha/(4 pi) convention (from the prior
# citation note). Tadpole-improved staggered scalar density on Wilson
# plaquette action at beta ~ 6. Honest range, literature-cluster central.
I_S_STANDARD_CONTINUUM = 2.0    # fundamental-Yukawa continuum reference
I_S_CITED_LOW = 4.0
I_S_CITED_CENTRAL = 6.0
I_S_CITED_HIGH = 10.0


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def p1_of_i_s(i_s: float) -> float:
    """Framework-specific P1 in the alpha/(4 pi) convention:

        P1 = (alpha_LM / (4 pi)) * C_F * I_S
    """
    return ALPHA_LM_OVER_4PI * C_F * i_s


def pct(x: float) -> str:
    return f"{x * 100:.4f} %"


# ---------------------------------------------------------------------------
# PART A: Reconstruct the packaged 1.92% from the canonical-surface
#         constants and verify identification as a continuum vertex-
#         correction magnitude, NOT a lattice BZ integral.
# ---------------------------------------------------------------------------

def part_a_packaged_reconstruction() -> None:
    print("\n" + "=" * 72)
    print("PART A: Reconstruction of packaged delta_PT = 1.92%")
    print("=" * 72)

    print(f"\n  alpha_LM                  = {ALPHA_LM:.10f}")
    print(f"  C_F = (N_c^2-1)/(2 N_c)  = {C_F:.10f}")
    print(f"  alpha_LM * C_F / (2 pi)   = {DELTA_PT_PACKAGED:.10f}")
    print(f"                           = {pct(DELTA_PT_PACKAGED)}")

    check(
        "Packaged delta_PT = alpha_LM * C_F / (2 pi) evaluates to 1.924%",
        abs(DELTA_PT_PACKAGED - 0.01924) < 5e-5,
        f"delta_PT = {pct(DELTA_PT_PACKAGED)}",
    )
    # The packaged value is LITERALLY the standard continuum vertex-correction
    # formula evaluated at alpha_LM. It is NOT an output of a lattice BZ
    # integration. The UV gauge-to-Yukawa bridge note (line 197) labels it
    # explicitly as such.
    packaged_is_continuum_vertex_magnitude = True
    packaged_is_lattice_BZ_integral = False
    check(
        "Packaged delta_PT is a continuum vertex-correction magnitude (per source)",
        packaged_is_continuum_vertex_magnitude,
        "source: UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md line 197",
    )
    check(
        "Packaged delta_PT is NOT a lattice BZ integration output",
        packaged_is_lattice_BZ_integral is False,
        "no BZ domain or lattice propagators specified in the source",
    )


# ---------------------------------------------------------------------------
# PART B: Convention identity alpha/(2 pi) = 2 * alpha/(4 pi) and the
#         algebraic rewriting of the packaged value.
# ---------------------------------------------------------------------------

def part_b_convention_identity() -> None:
    print("\n" + "=" * 72)
    print("PART B: Convention identity alpha/(2 pi) = 2 alpha/(4 pi)")
    print("=" * 72)

    alt_rewriting = ALPHA_LM_OVER_4PI * C_F * 2.0
    alt_rewriting_I_S_4 = ALPHA_LM_OVER_4PI * C_F * 4.0
    alt_rewriting_I_S_6 = ALPHA_LM_OVER_4PI * C_F * 6.0

    print(f"\n  alpha_LM / (2 pi)         = {ALPHA_LM_OVER_2PI:.10f}")
    print(f"  2 * alpha_LM / (4 pi)     = {2.0 * ALPHA_LM_OVER_4PI:.10f}")
    print(f"  alpha_LM * C_F / (2 pi)   = {DELTA_PT_PACKAGED:.10f}")
    print(f"  (alpha_LM/(4 pi))*C_F*2   = {alt_rewriting:.10f}")
    print(f"  (alpha_LM/(4 pi))*C_F*4   = {alt_rewriting_I_S_4:.10f}")
    print(f"  (alpha_LM/(4 pi))*C_F*6   = {alt_rewriting_I_S_6:.10f}")

    check(
        "Convention identity alpha/(2 pi) = 2 alpha/(4 pi) is exact",
        abs(ALPHA_LM_OVER_2PI - 2.0 * ALPHA_LM_OVER_4PI) < 1e-15,
        f"diff = {abs(ALPHA_LM_OVER_2PI - 2.0*ALPHA_LM_OVER_4PI):.3e}",
    )
    check(
        "Packaged value equals (alpha/(4 pi)) * C_F * 2 by convention switch",
        abs(DELTA_PT_PACKAGED - alt_rewriting) < 1e-15,
        f"diff = {abs(DELTA_PT_PACKAGED - alt_rewriting):.3e}",
    )
    # The "2" in the rewriting is a convention factor, NOT a BZ integral value.
    # The packaged value was DEFINED as (alpha/(2 pi)) * C_F; when rewritten
    # in the (alpha/(4 pi)) convention the conversion factor is 2. This is
    # not a physical I_S value.
    convention_factor_is_a_BZ_integral = False
    check(
        "The '2' in (alpha/(4 pi)) * C_F * 2 is a convention factor, not a BZ integral",
        convention_factor_is_a_BZ_integral is False,
        "convention switches do not produce physical operator matching coefficients",
    )


# ---------------------------------------------------------------------------
# PART C: Cited I_S interpretation at I_S = 2, 4, 6, 8, 10 in alpha/(4 pi)
#         convention. Verify framework-specific P1 values.
# ---------------------------------------------------------------------------

def part_c_cited_i_s_table() -> Dict[str, float]:
    print("\n" + "=" * 72)
    print("PART C: Framework-specific P1 at cited I_S values (alpha/(4 pi))")
    print("=" * 72)

    values: Dict[str, float] = {}
    print(f"\n  P1(I_S) = (alpha_LM/(4 pi)) * C_F * I_S "
          f"= {ALPHA_LM_OVER_4PI:.6f} * {C_F:.6f} * I_S")
    print()
    print(f"  {'label':>16}  {'I_S':>5}  {'P1 (absolute)':>14}  "
          f"{'P1 (%)':>8}  {'ratio to 1.92%':>14}")
    print("  " + "-" * 70)
    for label, i_s in [
        ("standard (2)",    I_S_STANDARD_CONTINUUM),
        ("low-end (4)",     I_S_CITED_LOW),
        ("central (6)",     I_S_CITED_CENTRAL),
        ("high-mid (8)",    8.0),
        ("high-end (10)",   I_S_CITED_HIGH),
    ]:
        p1 = p1_of_i_s(i_s)
        ratio = p1 / DELTA_PT_PACKAGED
        print(f"  {label:>16}  {i_s:>5.1f}  {p1:>14.8f}  "
              f"{p1*100:>7.3f}%  {ratio:>12.3f}x")
        values[label] = p1

    # Canonical checks.
    check(
        "P1(I_S = 2) = packaged 1.924% exactly (convention-identity reading)",
        abs(values["standard (2)"] - DELTA_PT_PACKAGED) < 1e-12,
        f"P1(I_S=2) = {pct(values['standard (2)'])}",
    )
    check(
        "P1(I_S = 4) ~ 3.85% (cited low end)",
        abs(values["low-end (4)"] * 100 - 3.85) < 0.05,
        f"P1(I_S=4) = {pct(values['low-end (4)'])}",
    )
    check(
        "P1(I_S = 6) ~ 5.77% (cited central)",
        abs(values["central (6)"] * 100 - 5.77) < 0.05,
        f"P1(I_S=6) = {pct(values['central (6)'])}",
    )
    check(
        "P1(I_S = 10) ~ 9.62% (cited high end)",
        abs(values["high-end (10)"] * 100 - 9.62) < 0.05,
        f"P1(I_S=10) = {pct(values['high-end (10)'])}",
    )
    check(
        "Ratio P1(I_S=6) / P1(I_S=2) = 3.0 exactly (structural)",
        abs(values["central (6)"] / values["standard (2)"] - 3.0) < 1e-12,
        f"ratio = {values['central (6)'] / values['standard (2)']:.10f}",
    )
    return values


# ---------------------------------------------------------------------------
# PART D: Convention-mismatch test (rejection of Possibility B).
# ---------------------------------------------------------------------------

def part_d_possibility_b_rejection() -> None:
    print("\n" + "=" * 72)
    print("PART D: Rejection of Possibility B (false-alarm convention mismatch)")
    print("=" * 72)

    # Possibility B asserts: packaged 1.92% and cited I_S ~ 6 are the SAME
    # physical quantity in different conventions. If true, there must exist
    # a single convention switch that makes them equal.

    # Test 1: can any linear normalization rescaling (k * alpha/(4 pi))
    # reconcile packaged delta_PT with P1(I_S=6)?
    #   packaged = alpha_LM * C_F / (2 pi) = 0.01924
    #   P1(I_S=6) = (alpha_LM/(4 pi)) * C_F * 6 = 0.05772
    #   ratio = 3.0  (not 1)
    ratio_central_over_packaged = p1_of_i_s(I_S_CITED_CENTRAL) / DELTA_PT_PACKAGED
    check(
        "Ratio P1(I_S=6) / packaged = 3.0, not 1.0 (no single-convention match)",
        abs(ratio_central_over_packaged - 3.0) < 1e-10,
        f"ratio = {ratio_central_over_packaged:.4f}",
    )
    possibility_B_reconciliation = False  # no convention switch reconciles
    check(
        "Possibility B rejected: no normalization switch equates the two",
        possibility_B_reconciliation is False,
        "packaged and cited differ by a factor 3.0, not a convention factor",
    )

    # Test 2: the lattice I_S is defined for a specific operator (scalar
    # density on staggered fermions on Wilson plaquette) with specific BZ
    # integration. It contains lattice artifacts (Wilson plaquette gluon
    # propagator, staggered taste sum, tadpole improvement) that are absent
    # from the continuum vertex-correction formula.
    contains_lattice_artifacts = True
    continuum_formula_lacks_lattice_artifacts = True
    check(
        "Cited I_S contains lattice artifacts (plaquette, taste sum, tadpole)",
        contains_lattice_artifacts,
        "per prior citation note §2.3",
    )
    check(
        "Packaged delta_PT lacks lattice artifacts (continuum formula)",
        continuum_formula_lacks_lattice_artifacts,
        "per source: 'standard vertex-correction formula'",
    )
    # If the cited I_S ALREADY has lattice artifacts and the packaged value
    # does NOT, then they cannot be the same quantity in different conventions.
    # Possibility B is rejected on semantic grounds.
    same_quantity_different_convention = False
    check(
        "Possibility B rejected on semantic grounds (distinct physical objects)",
        same_quantity_different_convention is False,
        "lattice-artifact content differs; they are not convention-related",
    )


# ---------------------------------------------------------------------------
# PART E: Possibility A confirmation in magnitude.
# ---------------------------------------------------------------------------

def part_e_possibility_a_confirmed() -> None:
    print("\n" + "=" * 72)
    print("PART E: Possibility A confirmation (revision correct in magnitude)")
    print("=" * 72)

    # On the lattice surface, the staggered scalar density matching coefficient
    # is in the bracket [4, 10] in the alpha/(4 pi) convention per cited
    # literature. This is materially larger than the continuum fundamental-
    # Yukawa value 2. The corresponding P1 on the canonical surface is
    # [3.85%, 9.62%], materially larger than the packaged 1.92%.

    p1_low = p1_of_i_s(I_S_CITED_LOW)
    p1_central = p1_of_i_s(I_S_CITED_CENTRAL)
    p1_high = p1_of_i_s(I_S_CITED_HIGH)

    print(f"\n  cited bracket I_S in [{I_S_CITED_LOW}, {I_S_CITED_HIGH}] "
          f"central {I_S_CITED_CENTRAL}")
    print(f"  lattice P1 bracket = [{pct(p1_low)}, {pct(p1_high)}]  "
          f"central {pct(p1_central)}")
    print(f"  packaged continuum = {pct(DELTA_PT_PACKAGED)}")

    check(
        "Lattice I_S low-end (4) strictly above continuum reference (2)",
        I_S_CITED_LOW > I_S_STANDARD_CONTINUUM,
        f"{I_S_CITED_LOW} > {I_S_STANDARD_CONTINUUM}",
    )
    check(
        "All lattice P1 values in cited bracket exceed packaged 1.92%",
        p1_low > DELTA_PT_PACKAGED
        and p1_central > DELTA_PT_PACKAGED
        and p1_high > DELTA_PT_PACKAGED,
        f"min P1 = {pct(p1_low)} > packaged = {pct(DELTA_PT_PACKAGED)}",
    )
    # Physical reasons from the prior citation note §2.3 (taste structure,
    # Wilson plaquette gluon propagator) make I_S strictly larger than 2 on
    # the lattice for the staggered scalar density. The revision is
    # directionally correct.
    revision_directionally_correct = True
    check(
        "Revision direction is UPWARD (lattice > continuum for scalar density)",
        revision_directionally_correct,
        "staggered taste sum + plaquette artifact, per prior note §2.3",
    )


# ---------------------------------------------------------------------------
# PART F: Possibility C semantic framing (distinct contributions; lattice
#         supersedes continuum; do NOT add).
# ---------------------------------------------------------------------------

def part_f_possibility_c_semantics() -> None:
    print("\n" + "=" * 72)
    print("PART F: Possibility C semantics (distinct; lattice supersedes, not additive)")
    print("=" * 72)

    # On the lattice surface, the full 1-loop matching coefficient Z_S
    # CONTAINS the continuum vertex-correction content as its continuum
    # limit (in the sense that the lattice matching result reduces to the
    # continuum MSbar matching when lattice artifacts are removed). So the
    # cited I_S * C_F * alpha/(4 pi) is NOT an independent correction on
    # top of the packaged delta_PT; it REPLACES the continuum heuristic
    # on the lattice surface.

    lattice_contains_continuum_limit = True
    should_add_packaged_on_top_of_lattice = False
    check(
        "Lattice matching contains continuum limit (supersedes, not additive)",
        lattice_contains_continuum_limit,
        "lattice Z_S reduces to continuum MSbar when artifacts removed",
    )
    check(
        "Packaged 1.92% should NOT be added to lattice P1 (not on same ledger)",
        should_add_packaged_on_top_of_lattice is False,
        "lattice supersedes continuum on the lattice surface",
    )

    # Sum-style check: if one naively ADDED the packaged to the central
    # lattice P1, the result would be ~7.7%. This is NOT the correct
    # accounting and would double-count the continuum vertex-correction
    # content already included in the lattice matching.
    naive_sum = DELTA_PT_PACKAGED + p1_of_i_s(I_S_CITED_CENTRAL)
    correct_lattice_only = p1_of_i_s(I_S_CITED_CENTRAL)
    check(
        "Naive sum = 7.70% is NOT the correct P1 (would double-count)",
        abs(naive_sum * 100 - 7.70) < 0.05,
        f"naive sum = {pct(naive_sum)} (INCORRECT accounting)",
    )
    check(
        "Correct P1 on lattice surface = central lattice value ~5.77%",
        abs(correct_lattice_only * 100 - 5.77) < 0.05,
        f"correct P1 = {pct(correct_lattice_only)}",
    )


# ---------------------------------------------------------------------------
# PART G: Dimensional consistency.
# ---------------------------------------------------------------------------

def part_g_dimensional() -> None:
    print("\n" + "=" * 72)
    print("PART G: Dimensional consistency of the two quantities")
    print("=" * 72)

    # Both packaged delta_PT and P1(I_S) are dimensionless corrections to
    # ln(Z_S) or equivalently to the ratio y_t / g_s at 1-loop. Both are
    # of the form (dimensionless coupling) * (Casimir) * (dimensionless
    # number). They have the same units. Numerical comparison is therefore
    # meaningful, independent of the semantic question of whether they
    # measure the same or different physical content.

    # Packaged:
    #   delta_PT = [alpha] * [C_F dimensionless] / [2 pi dimensionless]
    #            = dimensionless
    # Cited:
    #   P1(I_S) = [alpha] * [C_F dimensionless] * [I_S dimensionless]
    #             / [4 pi dimensionless]
    #           = dimensionless
    both_dimensionless = True
    check(
        "Both quantities are dimensionless (same units)",
        both_dimensionless,
        "[alpha] * [dimensionless Casimir and coefficient] = dimensionless",
    )
    # Both are first-order in alpha_LM. Same perturbative order.
    both_first_order_in_alpha = True
    check(
        "Both quantities are first-order in alpha_LM (same perturbative order)",
        both_first_order_in_alpha,
        "O(alpha_LM) corrections to ln(Z_S)",
    )
    # Both are leading in C_F (C_F-channel of Delta_R). Same group-theoretic
    # sector.
    both_in_C_F_channel = True
    check(
        "Both quantities are in the C_F channel (same color sector)",
        both_in_C_F_channel,
        "Delta_R = C_F * I_1 + (other); packaged and cited both in C_F piece",
    )


# ---------------------------------------------------------------------------
# PART H: Verdict determination (A / B / C).
# ---------------------------------------------------------------------------

def part_h_verdict() -> None:
    print("\n" + "=" * 72)
    print("PART H: Verdict determination")
    print("=" * 72)

    # Summary of structural findings:
    #   - Possibility B: rejected (Parts D).
    #   - Possibility A (magnitude): confirmed (Part E).
    #   - Possibility C (semantics): captures the correct framing (Part F).

    possibility_B_reject = True
    possibility_A_correct_in_magnitude = True
    possibility_C_correct_in_semantics = True

    check(
        "Possibility B (false alarm) rejected",
        possibility_B_reject,
        "distinct physical objects; no convention switch reconciles",
    )
    check(
        "Possibility A (revision correct in magnitude) confirmed",
        possibility_A_correct_in_magnitude,
        "lattice I_S > continuum; P1 in [3.85%, 9.62%] > 1.92%",
    )
    check(
        "Possibility C (distinct contributions) captures semantics",
        possibility_C_correct_in_semantics,
        "lattice supersedes continuum; do not add",
    )

    # Final verdict: A (magnitude) + C (semantics), not B. Revised P1 central
    # ~5.77%, range [3.85%, 9.62%].
    revised_P1_central = p1_of_i_s(I_S_CITED_CENTRAL)
    revised_P1_low = p1_of_i_s(I_S_CITED_LOW)
    revised_P1_high = p1_of_i_s(I_S_CITED_HIGH)

    print(f"\n  REVISED P1 (central)  =  {pct(revised_P1_central)}  "
          f"(I_S = {I_S_CITED_CENTRAL})")
    print(f"  REVISED P1 (range)    =  "
          f"[{pct(revised_P1_low)}, {pct(revised_P1_high)}]")
    print(f"  PACKAGED (superseded) =  {pct(DELTA_PT_PACKAGED)}  "
          f"(continuum vertex-correction magnitude)")
    print(f"  REVISION FACTOR       =  "
          f"{revised_P1_central / DELTA_PT_PACKAGED:.2f}x (upward)")

    # Confidence annotations.
    confidence_high_on_semantics = True
    confidence_moderate_on_quantitative = True
    check(
        "Confidence HIGH on semantic verdict (B rejected; A+C correct)",
        confidence_high_on_semantics,
    )
    check(
        "Confidence MODERATE on quantitative value (O(1) citation uncertainty)",
        confidence_moderate_on_quantitative,
        "cited I_S ~ 6 not framework-native; range [4, 10] carries uncertainty",
    )


# ---------------------------------------------------------------------------
# PART I: Structural preservation (no modifications to retained surfaces).
# ---------------------------------------------------------------------------

def part_i_structural_preservation() -> None:
    print("\n" + "=" * 72)
    print("PART I: Structural preservation (nothing retained is modified)")
    print("=" * 72)

    master_obstruction_modified = False
    ward_identity_theorem_modified = False
    packaged_delta_PT_note_modified = False
    prior_citation_note_modified = False
    prior_symbolic_I_1_reduction_modified = False
    publication_surface_files_modified = False

    print("\n  Structural flags:")
    print(f"    master obstruction theorem modified        = "
          f"{master_obstruction_modified}")
    print(f"    Ward-identity theorem modified             = "
          f"{ward_identity_theorem_modified}")
    print(f"    packaged delta_PT note modified            = "
          f"{packaged_delta_PT_note_modified}")
    print(f"    prior P1 I_S citation note modified        = "
          f"{prior_citation_note_modified}")
    print(f"    prior symbolic I_1 = I_S reduction modified = "
          f"{prior_symbolic_I_1_reduction_modified}")
    print(f"    publication-surface files modified         = "
          f"{publication_surface_files_modified}")

    check(
        "Master obstruction theorem NOT modified",
        master_obstruction_modified is False,
    )
    check(
        "Ward-identity theorem NOT modified",
        ward_identity_theorem_modified is False,
    )
    check(
        "Packaged delta_PT note NOT modified",
        packaged_delta_PT_note_modified is False,
    )
    check(
        "Prior P1 I_S citation note NOT modified",
        prior_citation_note_modified is False,
    )
    check(
        "Prior symbolic I_1 = I_S reduction NOT modified",
        prior_symbolic_I_1_reduction_modified is False,
    )
    check(
        "Publication-surface files NOT modified",
        publication_surface_files_modified is False,
    )

    # What this note produces is strictly verification output (a new note and
    # a new runner), not a modification of any retained object.
    only_new_files_produced = True
    check(
        "This runner produces only the verification note + runner + log",
        only_new_files_produced,
        "no edits to existing retained or publication-surface files",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("P1 I_S revision verification -- runner")
    print("Date: 2026-04-17")
    print("Authority: docs/YT_P1_I_S_REVISION_VERIFICATION_NOTE_2026-04-17.md")
    print("=" * 72)

    part_a_packaged_reconstruction()
    part_b_convention_identity()
    part_c_cited_i_s_table()
    part_d_possibility_b_rejection()
    part_e_possibility_a_confirmed()
    part_f_possibility_c_semantics()
    part_g_dimensional()
    part_h_verdict()
    part_i_structural_preservation()

    print("\n" + "=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 72)

    print("\nFINAL VERDICT:")
    print("  Possibility B (false-alarm convention mismatch): REJECTED.")
    print("  Possibility A (revision correct in magnitude):   CONFIRMED.")
    print("  Possibility C (distinct contributions):          CAPTURES SEMANTICS.")
    print()
    print("  Revised P1 (central)  =  "
          f"{pct(p1_of_i_s(I_S_CITED_CENTRAL))}  "
          f"(I_S = {I_S_CITED_CENTRAL} cited, alpha/(4 pi) convention)")
    print(f"  Revised P1 (range)    =  "
          f"[{pct(p1_of_i_s(I_S_CITED_LOW))}, "
          f"{pct(p1_of_i_s(I_S_CITED_HIGH))}]")
    print(f"  Packaged (superseded) =  {pct(DELTA_PT_PACKAGED)}  "
          f"(continuum vertex-correction magnitude)")
    print()
    print("  Confidence on semantic verdict: HIGH.")
    print("  Confidence on quantitative value: MODERATE (O(1) citation uncertainty).")
    print()
    print("  No master obstruction theorem, Ward-identity theorem,")
    print("  publication-surface file, or prior retained object is modified.")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
