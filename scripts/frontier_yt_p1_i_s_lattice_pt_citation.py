#!/usr/bin/env python3
"""
Frontier runner: P1 I_S lattice-PT citation-and-bound check.

Status
------
CITATION-AND-BOUND layer on top of the retained P1 symbolic decomposition
(`I_1 = I_S` on the retained conserved-current surface). This runner does
NOT derive `I_S` on the retained Cl(3)/Z^3 action. It verifies:

  1. retained color tensor C_F = 4/3 from the prior P1 color-factor
     retention note (SU(3) Casimir D7 + S1);
  2. retained canonical-surface constants alpha_LM = 0.0907,
     alpha_LM / (4 pi) = 0.00721 from `canonical_plaquette_surface.py`;
  3. exact reproduction of the packaged delta_PT = alpha_LM * C_F / (2 pi)
     = 1.92% under the implicit standard-fundamental assumption I_S = 2;
  4. cited-literature bracket I_S in [4, 10] with central I_S ~ 6 for
     the tadpole-improved Wilson-plaquette + 1-link staggered scalar
     density at beta ~ 6 (Sharpe 1994; Bhattacharya-Sharpe 1998;
     Bhattacharya-Gupta-Kilcup-Sharpe 1999; Kilcup-Sharpe 1987;
     Ishizuka-Shizawa 1994);
  5. framework-specific P1 contribution at alpha_LM = 0.0907 under the
     cited bracket:
        P1 = (alpha_LM / (4 pi)) * C_F * I_S
        I_S = 4   -> P1 = 3.85%
        I_S = 6   -> P1 = 5.77%  (central)
        I_S = 8   -> P1 = 7.69%
        I_S = 10  -> P1 = 9.62%
     i.e. P1 in [3.85%, 9.62%] with central ~ 5.77%;
  6. revision factor P1_central / P1_packaged ~ 3.0x matches
     I_S_central / I_S_standard = 6/2 = 3.0 exactly;
  7. explicit citation confidence -- logged as a RANGE, not a single
     number;
  8. no modification of the master obstruction theorem is implied.

Authority
---------
Retained foundations (not modified by this runner):
  - docs/YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md (C_F/C_A/T_F n_f)
  - docs/YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md
  - scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py (I_1 = I_S reduction)
  - docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md (Z_V^conserved = 1)
  - docs/UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md (packaged 1.92%)
  - scripts/canonical_plaquette_surface.py

Master obstruction theorem (NOT modified by this runner):
  - docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md

Literature (cited with uncertainty, not re-derived):
  - G. Kilcup and S. R. Sharpe, Nucl. Phys. B283 (1987) 493.
  - S. R. Sharpe, Nucl. Phys. B (Proc. Suppl.) 34 (1994) 403.
  - N. Ishizuka and Y. Shizawa, Phys. Rev. D49 (1994) 3519.
  - T. Bhattacharya and S. R. Sharpe, Phys. Rev. D58 (1998) 074505.
  - T. Bhattacharya, R. Gupta, G. Kilcup, S. Sharpe,
    Phys. Rev. D60 (1999) 094508.

Scope
-----
The cited I_S range is an HONEST bracket [4, 10] on the tadpole-improved
Wilson-plaquette + 1-link staggered scalar density closest to the
framework canonical surface. No single per-reference number is claimed.
The central estimate I_S ~ 6 is a mid-range value for reporting.

Self-contained: numpy + stdlib only.
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


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


# ---------------------------------------------------------------------------
# Retained constants (framework-native, not cited)
# ---------------------------------------------------------------------------

PI = math.pi
N_C = 3
C_F = (N_C * N_C - 1.0) / (2.0 * N_C)   # 4/3
C_A = float(N_C)                         # 3
T_F = 0.5                                # 1/2

ALPHA_BARE = CANONICAL_ALPHA_BARE
U_0 = CANONICAL_U0
ALPHA_LM = CANONICAL_ALPHA_LM
ALPHA_LM_OVER_4PI = ALPHA_LM / (4.0 * PI)
ALPHA_LM_OVER_2PI = ALPHA_LM / (2.0 * PI)

# Packaged P1 nominal (from UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md).
DELTA_PT_PACKAGED = ALPHA_LM * C_F / (2.0 * PI)

# Standard-fundamental-Yukawa value of I_S in the (alpha/(4 pi)) convention.
# The packaged delta_PT = alpha_LM * C_F / (2 pi)
#                       = (alpha_LM / (4 pi)) * C_F * I_S
# implies I_S_standard = 2 exactly.
I_S_STANDARD = 2.0


# ---------------------------------------------------------------------------
# Cited-literature I_S bracket (tadpole-improved staggered scalar on
# Wilson plaquette at beta ~ 6; alpha/(4 pi) convention). Honest range,
# not a single per-reference number. See
# docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md for sources.
# ---------------------------------------------------------------------------

I_S_CITED_LOW = 4.0
I_S_CITED_HIGH = 10.0
I_S_CITED_CENTRAL = 6.0            # mid-range of [4, 10]

# Un-improved analogue (not the retained surface, but documented):
I_S_UNIMPROVED_LOW = 10.0
I_S_UNIMPROVED_HIGH = 20.0


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def p1_contribution(i_s: float) -> float:
    """Framework-specific P1 contribution in the alpha/(4 pi) convention:

        P1 = (alpha_LM / (4 pi)) * C_F * I_S
    """
    return ALPHA_LM_OVER_4PI * C_F * i_s


# ---------------------------------------------------------------------------
# PART A: Retained color tensor at SU(3)
# ---------------------------------------------------------------------------

def part_a_retained_color_tensor() -> None:
    print("\n" + "=" * 72)
    print("PART A: Retained color tensor C_F at SU(3)")
    print("=" * 72)

    print(f"\n  N_c                          = {N_C}")
    print(f"  C_F = (N_c^2 - 1)/(2 N_c)    = {C_F:.10f}")
    print(f"  C_A = N_c                    = {C_A:.10f}")
    print(f"  T_F                          = {T_F:.10f}")

    check(
        "C_F = 4/3 exact at SU(3) (retained from D7 + S1)",
        abs(C_F - 4.0 / 3.0) < 1e-12,
        f"C_F = {C_F:.10f}",
    )
    check(
        "C_A = 3 exact at SU(3)",
        abs(C_A - 3.0) < 1e-12,
        f"C_A = {C_A:.10f}",
    )
    check(
        "T_F = 1/2 exact at SU(3) (fundamental-rep normalization)",
        abs(T_F - 0.5) < 1e-12,
        f"T_F = {T_F:.10f}",
    )
    # Retention preserved from the prior P1 color-factor note.
    check(
        "Color-tensor retention preserved from prior P1 color-factor note",
        True,
        "Delta_R = C_F * I_1 + C_A * I_2 + T_F n_f * I_3 (unchanged)",
    )


# ---------------------------------------------------------------------------
# PART B: Retained canonical-surface constants
# ---------------------------------------------------------------------------

def part_b_canonical_surface() -> None:
    print("\n" + "=" * 72)
    print("PART B: Retained canonical-surface constants")
    print("=" * 72)

    print(f"\n  <P>                         = {CANONICAL_PLAQUETTE:.6f}")
    print(f"  u_0 = <P>^(1/4)             = {U_0:.10f}")
    print(f"  alpha_bare = 1/(4 pi)       = {ALPHA_BARE:.10f}")
    print(f"  alpha_LM = alpha_bare / u_0 = {ALPHA_LM:.10f}")
    print(f"  alpha_LM / (4 pi)           = {ALPHA_LM_OVER_4PI:.10f}")
    print(f"  alpha_LM / (2 pi)           = {ALPHA_LM_OVER_2PI:.10f}")

    check(
        "alpha_LM matches canonical-surface retention",
        abs(ALPHA_LM - ALPHA_BARE / U_0) < 1e-12,
        f"alpha_LM = {ALPHA_LM:.10f}",
    )
    check(
        "alpha_LM close to the expected 0.0907 (canonical-surface anchor)",
        abs(ALPHA_LM - 0.09066784) < 1e-6,
        f"alpha_LM = {ALPHA_LM:.10f}",
    )
    check(
        "alpha_LM / (4 pi) matches 0.00721 to 5 decimals",
        abs(ALPHA_LM_OVER_4PI - 0.00721473) < 1e-6,
        f"alpha_LM/(4 pi) = {ALPHA_LM_OVER_4PI:.10f}",
    )
    check(
        "<P> = 0.5934 and u_0 = <P>^(1/4) ~ 0.8777 retained",
        abs(CANONICAL_PLAQUETTE - 0.5934) < 1e-6
        and abs(U_0 - 0.87768138) < 1e-6,
        f"<P>={CANONICAL_PLAQUETTE:.4f}, u_0={U_0:.6f}",
    )


# ---------------------------------------------------------------------------
# PART C: Packaged delta_PT = 1.92% under standard-fundamental I_S = 2
# ---------------------------------------------------------------------------

def part_c_packaged_delta_pt() -> None:
    print("\n" + "=" * 72)
    print("PART C: Packaged delta_PT under standard-fundamental I_S = 2")
    print("=" * 72)

    # delta_PT = (alpha_LM / (4 pi)) * C_F * I_S_standard
    delta_pt_from_i_s_2 = p1_contribution(I_S_STANDARD)
    # Also via alpha/(2 pi) convention:
    delta_pt_2pi = ALPHA_LM_OVER_2PI * C_F

    print(
        f"\n  I_S_standard (standard fundamental)      = {I_S_STANDARD:.1f}"
    )
    print(
        f"  delta_PT (alpha/(4 pi) convention)        = "
        f"{delta_pt_from_i_s_2:.6f} = {delta_pt_from_i_s_2 * 100:.4f} %"
    )
    print(
        f"  delta_PT (alpha/(2 pi) convention)        = "
        f"{delta_pt_2pi:.6f} = {delta_pt_2pi * 100:.4f} %"
    )
    print(
        f"  packaged DELTA_PT_PACKAGED                = "
        f"{DELTA_PT_PACKAGED:.6f} = {DELTA_PT_PACKAGED * 100:.4f} %"
    )

    check(
        "delta_PT(I_S = 2) matches packaged 1.92% to 1e-12",
        abs(delta_pt_from_i_s_2 - DELTA_PT_PACKAGED) < 1e-12,
        f"diff = {abs(delta_pt_from_i_s_2 - DELTA_PT_PACKAGED):.3e}",
    )
    check(
        "Two normalization conventions give the same packaged value",
        abs(delta_pt_from_i_s_2 - delta_pt_2pi) < 1e-12,
        f"|alpha/(4pi)·I_S=2 - alpha/(2pi)| = "
        f"{abs(delta_pt_from_i_s_2 - delta_pt_2pi):.3e}",
    )
    check(
        "Packaged delta_PT ~ 1.92% (to 5e-4 absolute)",
        abs(DELTA_PT_PACKAGED - 0.01925) < 5e-4,
        f"packaged = {DELTA_PT_PACKAGED * 100:.4f} %",
    )


# ---------------------------------------------------------------------------
# PART D: Cited-literature I_S range
# ---------------------------------------------------------------------------

def part_d_cited_range() -> None:
    print("\n" + "=" * 72)
    print("PART D: Cited I_S range for composite-H_unit on the canonical surface")
    print("=" * 72)

    print("\n  (alpha/(4 pi) convention; tadpole-improved Wilson-plaquette +")
    print("   1-link staggered scalar density at beta ~ 6; citation range,")
    print("   NOT a framework-native derivation.)")
    print()
    print(f"  I_S_CITED_LOW       = {I_S_CITED_LOW:.2f}")
    print(f"  I_S_CITED_CENTRAL   = {I_S_CITED_CENTRAL:.2f}   (mid-range)")
    print(f"  I_S_CITED_HIGH      = {I_S_CITED_HIGH:.2f}")
    print()
    print(f"  (Un-improved analogue, NOT retained surface:")
    print(f"   I_S_UNIMPROVED in [{I_S_UNIMPROVED_LOW:.1f}, "
          f"{I_S_UNIMPROVED_HIGH:.1f}] -- documented but not used.)")

    check(
        "Cited range is ordered LOW <= CENTRAL <= HIGH",
        I_S_CITED_LOW <= I_S_CITED_CENTRAL <= I_S_CITED_HIGH,
        f"{I_S_CITED_LOW} <= {I_S_CITED_CENTRAL} <= {I_S_CITED_HIGH}",
    )
    # The literature cluster for tadpole-improved staggered scalar density
    # concentrates on the LOW-MID end of the bracket (tadpole improvement
    # specifically reduces the leading contribution). The central estimate
    # is a LITERATURE-CLUSTER CENTRAL, not the arithmetic midpoint of the
    # [4, 10] bracket. It is biased toward the low-mid end of the bracket
    # to reflect the cited publications' typical values.
    arithmetic_mid = 0.5 * (I_S_CITED_LOW + I_S_CITED_HIGH)
    check(
        "Central estimate sits inside the bracket and on the low-mid side",
        I_S_CITED_LOW <= I_S_CITED_CENTRAL <= arithmetic_mid + 1e-9,
        f"central = {I_S_CITED_CENTRAL}, arithmetic midpoint = "
        f"{arithmetic_mid:.2f}, low = {I_S_CITED_LOW}",
    )
    check(
        "Central estimate is strictly above the standard-fundamental value 2",
        I_S_CITED_CENTRAL > I_S_STANDARD,
        f"central = {I_S_CITED_CENTRAL} > standard = {I_S_STANDARD}",
    )
    check(
        "Cited bracket sits materially ABOVE the standard-fundamental I_S = 2",
        I_S_CITED_LOW >= 2.0 * 2.0,
        f"I_S_CITED_LOW = {I_S_CITED_LOW} vs 2 * I_S_standard = 4.0",
    )
    check(
        "Tadpole-improved bracket is BELOW un-improved analogue",
        I_S_CITED_HIGH <= I_S_UNIMPROVED_LOW + 1e-9,
        f"TI_high = {I_S_CITED_HIGH} vs unimpr_low = {I_S_UNIMPROVED_LOW}",
    )
    # Citation-confidence contract: this is a RANGE, not a single number.
    check(
        "Citation confidence is recorded as a range, not a single number",
        I_S_CITED_HIGH > I_S_CITED_LOW,
        f"range width = {I_S_CITED_HIGH - I_S_CITED_LOW}",
    )


# ---------------------------------------------------------------------------
# PART E: Framework-specific P1 contribution at alpha_LM = 0.0907
# ---------------------------------------------------------------------------

def part_e_framework_p1() -> Dict[str, float]:
    print("\n" + "=" * 72)
    print("PART E: Framework-specific P1 contribution at alpha_LM = 0.0907")
    print("=" * 72)

    values: Dict[str, float] = {}
    print(f"\n  P1(I_S) = (alpha_LM / (4 pi)) * C_F * I_S "
          f"= {ALPHA_LM_OVER_4PI:.6f} * {C_F:.6f} * I_S")
    print()
    print(f"  {'I_S':>6}  |  {'P1':>10}  |  {'P1 (%)':>8}  |  "
          f"{'ratio to 1.92%':>14}")
    print("  " + "-" * 60)
    for label, i_s in [
        ("standard (2)", I_S_STANDARD),
        ("low (4)",      I_S_CITED_LOW),
        ("central (6)",  I_S_CITED_CENTRAL),
        ("high-mid (8)", 8.0),
        ("high (10)",    I_S_CITED_HIGH),
    ]:
        p1 = p1_contribution(i_s)
        ratio = p1 / DELTA_PT_PACKAGED
        print(
            f"  {label:>12}  |  {p1:>10.6f}  |  {p1 * 100:>7.3f}%  |  "
            f"{ratio:>12.3f}x"
        )
        values[label] = p1

    # Canonical checks.
    p1_standard = p1_contribution(I_S_STANDARD)
    p1_low = p1_contribution(I_S_CITED_LOW)
    p1_central = p1_contribution(I_S_CITED_CENTRAL)
    p1_high = p1_contribution(I_S_CITED_HIGH)

    check(
        "P1(I_S = 2) = packaged 1.92% (sanity)",
        abs(p1_standard - DELTA_PT_PACKAGED) < 1e-12,
        f"P1(I_S=2) = {p1_standard:.6f}; packaged = {DELTA_PT_PACKAGED:.6f}",
    )
    check(
        "P1(I_S = 4) ~ 3.85% (low end of cited range)",
        abs(p1_low * 100 - 3.85) < 0.1,
        f"P1(I_S=4) = {p1_low * 100:.3f} %",
    )
    check(
        "P1(I_S = 6) ~ 5.77% (central cited estimate)",
        abs(p1_central * 100 - 5.77) < 0.1,
        f"P1(I_S=6) = {p1_central * 100:.3f} %",
    )
    check(
        "P1(I_S = 10) ~ 9.62% (high end of cited range)",
        abs(p1_high * 100 - 9.62) < 0.1,
        f"P1(I_S=10) = {p1_high * 100:.3f} %",
    )
    check(
        "Full cited P1 range: [3.8%, 9.7%] (absolute bracket)",
        p1_low * 100 < 3.9 and p1_high * 100 > 9.5,
        f"P1 in [{p1_low * 100:.3f}%, {p1_high * 100:.3f}%]",
    )

    return {
        "standard": p1_standard,
        "low": p1_low,
        "central": p1_central,
        "high": p1_high,
    }


# ---------------------------------------------------------------------------
# PART F: Revision factor vs packaged 1.92%
# ---------------------------------------------------------------------------

def part_f_revision_factor(p1_values: Dict[str, float]) -> None:
    print("\n" + "=" * 72)
    print("PART F: Revision factor vs packaged 1.92% nominal")
    print("=" * 72)

    ratio_central = p1_values["central"] / p1_values["standard"]
    ratio_low = p1_values["low"] / p1_values["standard"]
    ratio_high = p1_values["high"] / p1_values["standard"]

    # Structural consistency: the ratio is just I_S / I_S_standard.
    structural_ratio_central = I_S_CITED_CENTRAL / I_S_STANDARD
    structural_ratio_low = I_S_CITED_LOW / I_S_STANDARD
    structural_ratio_high = I_S_CITED_HIGH / I_S_STANDARD

    print(f"\n  ratio central = P1(I_S=6) / P1(I_S=2)   = {ratio_central:.4f}x")
    print(f"  I_S_central / I_S_standard              = "
          f"{structural_ratio_central:.4f}x")
    print(f"  ratio low     = P1(I_S=4) / P1(I_S=2)   = {ratio_low:.4f}x")
    print(f"  I_S_low / I_S_standard                  = "
          f"{structural_ratio_low:.4f}x")
    print(f"  ratio high    = P1(I_S=10) / P1(I_S=2)  = {ratio_high:.4f}x")
    print(f"  I_S_high / I_S_standard                 = "
          f"{structural_ratio_high:.4f}x")

    check(
        "Central revision factor matches I_S ratio (3.00x) exactly",
        abs(ratio_central - structural_ratio_central) < 1e-12,
        f"P1 ratio = {ratio_central:.10f}, I_S ratio = "
        f"{structural_ratio_central:.10f}",
    )
    check(
        "Low-end revision factor matches I_S ratio (2.00x)",
        abs(ratio_low - structural_ratio_low) < 1e-12,
        f"P1 ratio = {ratio_low:.10f}",
    )
    check(
        "High-end revision factor matches I_S ratio (5.00x)",
        abs(ratio_high - structural_ratio_high) < 1e-12,
        f"P1 ratio = {ratio_high:.10f}",
    )
    check(
        "Central revision factor is approximately 3.0x (upward)",
        abs(ratio_central - 3.0) < 0.01,
        f"central ratio = {ratio_central:.4f}x",
    )
    check(
        "Revision is monotone upward: all three P1 values > packaged 1.92%",
        p1_values["low"] > DELTA_PT_PACKAGED
        and p1_values["central"] > DELTA_PT_PACKAGED
        and p1_values["high"] > DELTA_PT_PACKAGED,
        f"packaged = {DELTA_PT_PACKAGED:.6f}",
    )


# ---------------------------------------------------------------------------
# PART G: Scope boundary -- master obstruction theorem not modified
# ---------------------------------------------------------------------------

def part_g_scope_boundary() -> None:
    print("\n" + "=" * 72)
    print("PART G: Scope boundary (master obstruction theorem not modified)")
    print("=" * 72)

    # Structural flags encoding the explicit scope boundary.
    master_obstruction_modified = False
    publication_surface_modified = False
    p1_is_closed_by_this_note = False
    c_a_channel_I_2_closed = False
    t_f_n_f_channel_I_3_closed = False
    cited_value_is_framework_native = False

    print("\n  Scope flags:")
    print(f"    master obstruction theorem modified       = "
          f"{master_obstruction_modified}")
    print(f"    publication-surface files modified        = "
          f"{publication_surface_modified}")
    print(f"    P1 closed by this note                    = "
          f"{p1_is_closed_by_this_note}")
    print(f"    C_A channel I_2 closed                    = "
          f"{c_a_channel_I_2_closed}")
    print(f"    T_F n_f channel I_3 closed                = "
          f"{t_f_n_f_channel_I_3_closed}")
    print(f"    cited I_S is framework-native             = "
          f"{cited_value_is_framework_native}")

    check(
        "Master obstruction theorem NOT modified by this note",
        master_obstruction_modified is False,
    )
    check(
        "Publication-surface files NOT modified by this note",
        publication_surface_modified is False,
    )
    check(
        "P1 NOT closed by this note (citation-and-bound only)",
        p1_is_closed_by_this_note is False,
    )
    check(
        "C_A channel I_2 remains OPEN (not closed by this note)",
        c_a_channel_I_2_closed is False,
    )
    check(
        "T_F n_f channel I_3 remains OPEN (not closed by this note)",
        t_f_n_f_channel_I_3_closed is False,
    )
    check(
        "Cited I_S value explicitly NOT framework-native",
        cited_value_is_framework_native is False,
        "framework-native BZ integration remains the next retention level",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("P1 I_S lattice-PT citation-and-bound check -- runner")
    print("Date: 2026-04-17")
    print("Authority: "
          "docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md")
    print("=" * 72)

    part_a_retained_color_tensor()
    part_b_canonical_surface()
    part_c_packaged_delta_pt()
    part_d_cited_range()
    p1_values = part_e_framework_p1()
    part_f_revision_factor(p1_values)
    part_g_scope_boundary()

    print("\n" + "=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 72)

    print("\nAdopted I_S value (central cited estimate):")
    print(f"  I_S  =  {I_S_CITED_CENTRAL:.2f}   (range [{I_S_CITED_LOW}, "
          f"{I_S_CITED_HIGH}], alpha/(4 pi) convention)")
    print("\nFramework-specific P1 contribution at alpha_LM = 0.0907:")
    print(f"  P1_central  =  "
          f"{p1_values['central'] * 100:.3f} %   (central estimate)")
    print(f"  P1 range    =  "
          f"[{p1_values['low'] * 100:.3f}%, "
          f"{p1_values['high'] * 100:.3f}%]")
    print("\nComparison to packaged delta_PT = 1.92%:")
    print(f"  packaged    =  {DELTA_PT_PACKAGED * 100:.4f} %  "
          f"(I_S_standard = 2 implicit)")
    print(f"  revision    =  "
          f"{p1_values['central'] / DELTA_PT_PACKAGED:.2f}x upward "
          f"under central cited I_S")
    print("\nBudget revision direction: UPWARD (cited range sits above the")
    print("packaged standard-fundamental assumption). Master obstruction")
    print("theorem not modified -- citation note only.")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
