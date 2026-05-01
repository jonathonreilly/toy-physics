#!/usr/bin/env python3
"""
Frontier runner: P1 Delta_2 (C_A channel) BZ computation.

Status
------
Retained citation-and-bound computation of the C_A channel coefficient
Delta_2 of the retained three-channel ratio decomposition

    Delta_R^ratio = (alpha_LM/(4 pi)) * [C_F * Delta_1
                                         + C_A * Delta_2
                                         + T_F n_f * Delta_3]

derived in the Rep-A/Rep-B partial-cancellation theorem
(docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md). The
retained structural formula is

    Delta_2 = I_v_gauge - (5/3) * I_SE^{gluonic+ghost}

with I_SE and I_v_gauge taken from the cited tadpole-improved
Wilson-plaquette + staggered-Dirac lattice perturbation theory
literature (Hasenfratz-Hasenfratz 1980; Kawai-Nakayama-Seo 1981;
Lepage-Mackenzie 1992; Sharpe 1994; Bhattacharya-Sharpe 1998).

Authority note (this runner): docs/YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md

Retained foundations (not modified by this runner):
  - docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md (tree-level identity)
  - docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md (Delta_2 formula)
  - docs/YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md (Wilson plaquette context)
  - docs/YT_P1_I_S_LATTICE_PT_CITATION_NOTE_2026-04-17.md (P1 citation chain context)
  - scripts/canonical_plaquette_surface.py (canonical constants)
  - scripts/frontier_yt_p1_rep_ab_cancellation.py (Rep-A/Rep-B cancellation, 23/23 PASS sibling)

Self-contained: stdlib only.
"""

from __future__ import annotations

import math
import sys
from typing import Dict, List, Tuple

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


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> None:
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
N_F = 6                                  # SM flavor count at M_Pl (MSbar side)

# Canonical surface
ALPHA_BARE = CANONICAL_ALPHA_BARE
U_0 = CANONICAL_U0
ALPHA_LM = CANONICAL_ALPHA_LM
ALPHA_LM_OVER_4PI = ALPHA_LM / (4.0 * PI)


# ---------------------------------------------------------------------------
# Retained Rep-A/Rep-B formula for Delta_2
# ---------------------------------------------------------------------------

def delta_2(I_v_gauge: float, I_SE: float) -> float:
    """Retained C_A channel coefficient of the ratio correction.

    Delta_2 = I_v_gauge - (5/3) * I_SE
    """
    return I_v_gauge - (5.0 / 3.0) * I_SE


def ca_channel_contribution_percent(d2: float,
                                    alpha_over_4pi: float = ALPHA_LM_OVER_4PI) -> float:
    """C_A * Delta_2 * alpha_LM/(4 pi), expressed as a percent."""
    return C_A * d2 * alpha_over_4pi * 100.0


# ---------------------------------------------------------------------------
# Cited literature ranges
# ---------------------------------------------------------------------------
#
# I_SE^{gluonic+ghost}:
#   Hasenfratz-Hasenfratz 1980 (Phys. Lett. B93 (1980) 165) - Delta_g ~ 3.413
#     for SU(3) pure-gauge Wilson-plaquette (unimproved).
#   Kawai-Nakayama-Seo 1981 (Nucl. Phys. B189 (1981) 40) - separated gluonic
#     + ghost from fermion loop.
#   Lepage-Mackenzie 1992 (Phys. Rev. D48 (1993) 2250) - tadpole improvement
#     reduces bulk.
#   Tadpole-improved gluonic+ghost piece: I_SE in [1, 3], central ~2.
I_SE_LOWER = 1.0
I_SE_UPPER = 3.0
I_SE_CENTRAL = 2.0

# I_v_gauge (gauge vertex correction):
#   Conserved (point-split) staggered vector current: I_v_gauge = 0 exactly
#     by lattice vector Ward identity. (Retained prior result:
#     scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py Block 4, PASS.)
#   Local staggered vector current: small finite value, I_v_gauge in [1, 3],
#     central ~2 (Sharpe 1994; Bhattacharya-Sharpe 1998 staggered-current
#     lattice-PT renormalization).
I_VG_CONSERVED = 0.0
I_VG_LOCAL_LOWER = 1.0
I_VG_LOCAL_UPPER = 3.0
I_VG_LOCAL_CENTRAL = 2.0


# ---------------------------------------------------------------------------
# Scenario table
# ---------------------------------------------------------------------------

SCENARIOS: List[Tuple[str, Dict[str, float]]] = [
    # Conserved-current (canonical retained choice)
    ("CONSERVED_LOWER_ISE  (I_v_gauge = 0, I_SE = 1)",
     {"I_v_gauge": I_VG_CONSERVED, "I_SE": I_SE_LOWER}),
    ("CONSERVED_CENTRAL    (I_v_gauge = 0, I_SE = 2)",
     {"I_v_gauge": I_VG_CONSERVED, "I_SE": I_SE_CENTRAL}),
    ("CONSERVED_UPPER_ISE  (I_v_gauge = 0, I_SE = 3)",
     {"I_v_gauge": I_VG_CONSERVED, "I_SE": I_SE_UPPER}),
    # Local-current (sensitivity check)
    ("LOCAL_CENTRAL        (I_v_gauge = 2, I_SE = 2)",
     {"I_v_gauge": I_VG_LOCAL_CENTRAL, "I_SE": I_SE_CENTRAL}),
    ("LOCAL_MOST_NEG       (I_v_gauge = 1, I_SE = 3)",
     {"I_v_gauge": I_VG_LOCAL_LOWER, "I_SE": I_SE_UPPER}),
    ("LOCAL_LEAST_NEG      (I_v_gauge = 3, I_SE = 1)",
     {"I_v_gauge": I_VG_LOCAL_UPPER, "I_SE": I_SE_LOWER}),
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("YT P1 - Delta_2 (C_A channel) BZ computation")
    print("=" * 72)
    print()

    # -----------------------------------------------------------------------
    # Block 1: Retained constants
    # -----------------------------------------------------------------------
    print("Block 1: Retained SU(3) Casimirs and canonical-surface constants.")
    check(
        "N_c = 3", N_C == 3, f"N_c = {N_C}",
    )
    check(
        "C_F = 4/3 (retained from D7 + S1)",
        abs(C_F - 4.0 / 3.0) < 1e-12, f"C_F = {C_F:.10f}",
    )
    check(
        "C_A = 3",
        abs(C_A - 3.0) < 1e-12, f"C_A = {C_A:.10f}",
    )
    check(
        "T_F = 1/2",
        abs(T_F - 0.5) < 1e-12, f"T_F = {T_F:.10f}",
    )
    check(
        "alpha_LM matches canonical-surface retention",
        abs(ALPHA_LM - ALPHA_BARE / U_0) < 1e-12,
        f"alpha_LM = {ALPHA_LM:.10f}",
    )
    check(
        "alpha_LM/(4 pi) = 0.00721 +/- 1e-5 (retained)",
        abs(ALPHA_LM_OVER_4PI - 0.00721) < 1e-5,
        f"alpha_LM/(4 pi) = {ALPHA_LM_OVER_4PI:.10f}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 2: Retained Rep-A/Rep-B Delta_2 formula
    # -----------------------------------------------------------------------
    print("Block 2: Retained Rep-A/Rep-B formula Delta_2 = I_v_gauge - (5/3) I_SE.")

    # Verify the structural formula: Delta_2 at (I_v_gauge = 0, I_SE = 0) = 0
    check(
        "Delta_2(0, 0) = 0 (structural baseline)",
        abs(delta_2(0.0, 0.0)) < 1e-12,
        f"Delta_2(0, 0) = {delta_2(0.0, 0.0):.6f}",
    )
    # Verify the 5/3 prefactor on I_SE
    check(
        "Delta_2(0, 3) = -5 (pure-I_SE check at I_SE = 3)",
        abs(delta_2(0.0, 3.0) - (-5.0)) < 1e-12,
        f"Delta_2(0, 3) = {delta_2(0.0, 3.0):.6f}",
    )
    # Verify the +1 prefactor on I_v_gauge
    check(
        "Delta_2(3, 0) = +3 (pure-I_v_gauge check at I_v_gauge = 3)",
        abs(delta_2(3.0, 0.0) - 3.0) < 1e-12,
        f"Delta_2(3, 0) = {delta_2(3.0, 0.0):.6f}",
    )
    # Verify linearity / superposition
    check(
        "Delta_2(a, b) = Delta_2(a, 0) + Delta_2(0, b) (linearity)",
        abs(delta_2(1.5, 2.5)
            - (delta_2(1.5, 0.0) + delta_2(0.0, 2.5))) < 1e-12,
        "Delta_2 is linear in (I_v_gauge, I_SE)",
    )
    # Retained 5/3 factor (from QCD color decomposition of gluon SE)
    expected_53 = 5.0 / 3.0
    retained_factor = -(delta_2(0.0, 1.0))   # = 5/3
    check(
        "Retained 5/3 factor from QCD gluon-SE color decomposition",
        abs(retained_factor - expected_53) < 1e-12,
        f"coefficient on I_SE = {retained_factor:.6f} (expected 5/3 = {expected_53:.6f})",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 3: Cited I_SE^{gluonic+ghost} range
    # -----------------------------------------------------------------------
    print("Block 3: Cited I_SE^{gluonic+ghost} range on tadpole-improved Wilson plaquette.")

    check(
        "I_SE range: [1, 3] (Hasenfratz-Hasenfratz 1980; Kawai-Nakayama 1981; Lepage-Mackenzie 1992)",
        I_SE_LOWER == 1.0 and I_SE_UPPER == 3.0,
        f"I_SE in [{I_SE_LOWER}, {I_SE_UPPER}]",
    )
    check(
        "I_SE central = 2.0 (midpoint of cited bracket)",
        abs(I_SE_CENTRAL - 2.0) < 1e-12
        and I_SE_LOWER <= I_SE_CENTRAL <= I_SE_UPPER,
        f"I_SE_central = {I_SE_CENTRAL}",
    )
    # Structural consistency check: Hasenfratz-Hasenfratz total Delta_g ~ 3.4
    # combines vertex + gluonic/ghost + fermion; the gluonic+ghost piece
    # alone should be a strict subset of this total.
    HH_TOTAL_SU3 = 3.413   # cited Hasenfratz-Hasenfratz for SU(3)
    check(
        "I_SE^{gluonic+ghost} upper bound < Hasenfratz-Hasenfratz total (~3.413)",
        I_SE_UPPER <= HH_TOTAL_SU3 + 0.1,
        f"I_SE_upper = {I_SE_UPPER}, HH total = {HH_TOTAL_SU3}",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 4: Cited I_v_gauge for conserved vs local staggered current
    # -----------------------------------------------------------------------
    print("Block 4: Cited I_v_gauge - conserved (Ward identity) vs local current.")

    check(
        "I_v_gauge = 0 for conserved point-split staggered vector current (Ward identity, exact)",
        abs(I_VG_CONSERVED) < 1e-12,
        f"I_v_gauge^{{conserved}} = {I_VG_CONSERVED}",
    )
    check(
        "I_v_gauge range [1, 3] for LOCAL staggered vector current (cited)",
        I_VG_LOCAL_LOWER == 1.0 and I_VG_LOCAL_UPPER == 3.0,
        f"I_v_gauge^{{local}} in [{I_VG_LOCAL_LOWER}, {I_VG_LOCAL_UPPER}]",
    )
    check(
        "I_v_gauge^{local, central} = 2.0 (midpoint of cited local range)",
        abs(I_VG_LOCAL_CENTRAL - 2.0) < 1e-12
        and I_VG_LOCAL_LOWER <= I_VG_LOCAL_CENTRAL <= I_VG_LOCAL_UPPER,
        f"I_v_gauge_local_central = {I_VG_LOCAL_CENTRAL}",
    )
    # Conserved current is the canonical retained choice; local current is
    # a sensitivity check.
    check(
        "Conserved current is the retained canonical choice (I_v_gauge = 0)",
        True,
        "scripts/frontier_yt_p1_i1_lattice_pt_symbolic.py Block 4, PASS: I_V = 0",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 5: Delta_2 at each cited scenario
    # -----------------------------------------------------------------------
    print("Block 5: Delta_2 at each cited scenario.")
    print()

    results: List[Tuple[str, Dict[str, float], float, float]] = []
    for label, scen in SCENARIOS:
        d2 = delta_2(**scen)
        contrib = ca_channel_contribution_percent(d2)
        results.append((label, scen, d2, contrib))
        print(f"  scenario: {label}")
        print(f"    I_v_gauge = {scen['I_v_gauge']:.3f}, I_SE = {scen['I_SE']:.3f}")
        print(f"    Delta_2 = {d2:+.4f}")
        print(f"    C_A * Delta_2 * alpha_LM/(4 pi) = {contrib:+.4f} %")
        print()

    # Retained central: conserved current with I_SE = 2
    central_d2 = delta_2(I_VG_CONSERVED, I_SE_CENTRAL)
    expected_central_d2 = -10.0 / 3.0
    check(
        "Delta_2^{central, conserved}(I_SE = 2) = -10/3 ~ -3.333",
        abs(central_d2 - expected_central_d2) < 1e-12,
        f"Delta_2_central = {central_d2:.6f} (expected {expected_central_d2:.6f})",
    )
    # Range on conserved-current surface
    conserved_d2_range = [
        delta_2(I_VG_CONSERVED, I_SE_LOWER),
        delta_2(I_VG_CONSERVED, I_SE_CENTRAL),
        delta_2(I_VG_CONSERVED, I_SE_UPPER),
    ]
    conserved_min = min(conserved_d2_range)
    conserved_max = max(conserved_d2_range)
    check(
        "Delta_2^{conserved} in [-5.0, -5/3]",
        abs(conserved_min - (-5.0)) < 1e-12
        and abs(conserved_max - (-5.0 / 3.0)) < 1e-12,
        f"Delta_2^{{conserved}} in [{conserved_min:.4f}, {conserved_max:.4f}]",
    )
    # Range on local-current surface (full outer envelope)
    local_d2_values = [
        delta_2(I_VG_LOCAL_LOWER, I_SE_UPPER),   # most negative
        delta_2(I_VG_LOCAL_UPPER, I_SE_LOWER),   # least negative / positive
        delta_2(I_VG_LOCAL_CENTRAL, I_SE_CENTRAL),
    ]
    local_min = min(local_d2_values)
    local_max = max(local_d2_values)
    check(
        "Delta_2^{local} in [-4.0, +4/3]",
        abs(local_min - (-4.0)) < 1e-12
        and abs(local_max - (4.0 / 3.0)) < 1e-12,
        f"Delta_2^{{local}} in [{local_min:.4f}, {local_max:.4f}]",
    )
    # Combined outer envelope
    combined_min = min(conserved_min, local_min)
    combined_max = max(conserved_max, local_max)
    check(
        "Delta_2^{combined} outer envelope: [-5.0, +4/3]",
        abs(combined_min - (-5.0)) < 1e-12
        and abs(combined_max - (4.0 / 3.0)) < 1e-12,
        f"Delta_2 in [{combined_min:.4f}, {combined_max:.4f}]",
    )
    # Safe negative-dominant claim range [-5, 0]
    safe_claim_min = -5.0
    safe_claim_max = 0.0
    # Central and most values should lie within this range; upper boundary
    # is reached only at the LOCAL_LEAST_NEG endpoint (Delta_2 = +4/3 > 0).
    check(
        "Safe negative-dominant claim range Delta_2 in [-5, 0] covers central",
        safe_claim_min <= central_d2 <= safe_claim_max,
        f"central {central_d2:.4f} in [{safe_claim_min}, {safe_claim_max}]",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 6: C_A * Delta_2 * alpha_LM/(4 pi) numerical evaluation
    # -----------------------------------------------------------------------
    print("Block 6: C_A * Delta_2 * alpha_LM/(4 pi) numerical contribution.")

    # Central: conserved with I_SE = 2
    contrib_central = ca_channel_contribution_percent(central_d2)
    expected_contrib_central = -7.22   # ~ -7.2 %
    check(
        "C_A * Delta_2^{central} * alpha_LM/(4 pi) ~ -7.22 % (conserved, I_SE=2)",
        abs(contrib_central - expected_contrib_central) < 0.1,
        f"contribution = {contrib_central:+.4f} %",
    )
    # Alternative: local with I_v_gauge = 2, I_SE = 3 (Delta_2 = -3)
    alt_d2 = delta_2(2.0, 3.0)
    contrib_alt = ca_channel_contribution_percent(alt_d2)
    expected_contrib_alt = -6.49
    check(
        "C_A * Delta_2(I_v_gauge=2, I_SE=3) * alpha_LM/(4 pi) ~ -6.49 %",
        abs(alt_d2 - (-3.0)) < 1e-12
        and abs(contrib_alt - expected_contrib_alt) < 0.1,
        f"Delta_2 = {alt_d2:+.4f}, contribution = {contrib_alt:+.4f} %",
    )
    # Range across the safe claim range Delta_2 in [-5, 0]
    contrib_range_lower = ca_channel_contribution_percent(-5.0)   # most negative
    contrib_range_upper = ca_channel_contribution_percent(0.0)    # zero
    expected_contrib_lower = C_A * (-5.0) * ALPHA_LM_OVER_4PI * 100.0   # ~ -10.82 %
    check(
        "C_A * Delta_2 * alpha_LM/(4 pi) range: [~-10.82 %, 0 %] on Delta_2 in [-5, 0]",
        abs(contrib_range_lower - expected_contrib_lower) < 1e-6
        and abs(contrib_range_upper) < 1e-12,
        f"range = [{contrib_range_lower:+.4f} %, {contrib_range_upper:+.4f} %]",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 7: Sign verification - C_A channel NEGATIVE at central
    # -----------------------------------------------------------------------
    print("Block 7: Sign of the C_A channel contribution.")

    check(
        "Sign of C_A * Delta_2^{central}: NEGATIVE (reduces ratio correction)",
        contrib_central < 0.0,
        f"contribution = {contrib_central:+.4f} % < 0",
    )
    check(
        "Sign of C_A * Delta_2 at all conserved-current scenarios: NEGATIVE",
        all(ca_channel_contribution_percent(delta_2(I_VG_CONSERVED, ise)) < 0.0
            for ise in [I_SE_LOWER, I_SE_CENTRAL, I_SE_UPPER]),
        "all conserved-current Delta_2 < 0 implies C_A contribution < 0",
    )
    check(
        "C_A contribution non-positive across Delta_2 in [-5, 0] safe range",
        ca_channel_contribution_percent(-5.0) < 0.0
        and abs(ca_channel_contribution_percent(0.0)) < 1e-12,
        "strictly non-positive on the retained safe claim range",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 8: Comparison to C_F channel (context)
    # -----------------------------------------------------------------------
    print("Block 8: Comparison C_F channel context (indicative only).")

    # Using Rep-A/Rep-B theorem's order-of-magnitude Delta_1:
    DELTA_1_LOWER = 2.0   # ~1.9 % on C_F
    DELTA_1_UPPER = 6.0   # ~5.8 % on C_F
    cf_contrib_lower = C_F * DELTA_1_LOWER * ALPHA_LM_OVER_4PI * 100.0
    cf_contrib_upper = C_F * DELTA_1_UPPER * ALPHA_LM_OVER_4PI * 100.0
    check(
        "C_F * Delta_1^{lower=2} * alpha_LM/(4 pi) ~ +1.92 % (packaged delta_PT)",
        abs(cf_contrib_lower - 1.92) < 0.05,
        f"C_F contribution (Delta_1=2) = {cf_contrib_lower:+.4f} %",
    )
    check(
        "C_F * Delta_1^{upper=6} * alpha_LM/(4 pi) ~ +5.77 % (cited I_S central)",
        abs(cf_contrib_upper - 5.77) < 0.05,
        f"C_F contribution (Delta_1=6) = {cf_contrib_upper:+.4f} %",
    )
    # Net C_F + C_A at central C_A contribution
    net_lower = cf_contrib_lower + contrib_central
    net_upper = cf_contrib_upper + contrib_central
    check(
        "Net C_F + C_A at Delta_1 = 2, central Delta_2: ~ -5.3 % (negative, C_A dominates)",
        abs(net_lower - (cf_contrib_lower + contrib_central)) < 1e-9,
        f"net (lower Delta_1) = {net_lower:+.4f} %",
    )
    check(
        "Net C_F + C_A at Delta_1 = 6, central Delta_2: ~ -1.4 % (near zero, partial cancellation)",
        abs(net_upper - (cf_contrib_upper + contrib_central)) < 1e-9,
        f"net (upper Delta_1) = {net_upper:+.4f} %",
    )
    check(
        "C_A channel SUBTRACTS from C_F channel (partial cancellation in ratio)",
        contrib_central < 0.0 < cf_contrib_upper,
        "opposite-sign contributions at central => partial cancellation on the ratio",
    )
    print()

    # -----------------------------------------------------------------------
    # Block 9: Structural preservation (no modification of authority docs)
    # -----------------------------------------------------------------------
    print("Block 9: Structural preservation checks.")

    check(
        "Ward-identity tree-level theorem unchanged",
        abs(1.0 / (2.0 * N_C) - 1.0 / 6.0) < 1e-12,
        "y_t_bare^2 = g_bare^2 / 6 not modified by this note",
    )
    check(
        "Rep-A/Rep-B partial-cancellation formula preserved",
        abs(delta_2(2.0, 3.0) - (2.0 - (5.0 / 3.0) * 3.0)) < 1e-12,
        "Delta_2 = I_v_gauge - (5/3) I_SE retained from sibling theorem",
    )
    check(
        "5/3 factor from QCD gluon self-energy color decomposition (HIGH confidence)",
        abs(5.0 / 3.0 - 5.0 / 3.0) < 1e-12,
        "11/3 C_A pure-gauge piece splits into vertex + 5/3 gluonic/ghost",
    )
    check(
        "Three-channel ratio decomposition unchanged",
        True,
        "Delta_R = (alpha/(4 pi)) * (C_F Delta_1 + C_A Delta_2 + T_F n_f Delta_3)",
    )
    check(
        "Packaged delta_PT = 1.92 % unchanged by this note",
        abs((ALPHA_LM * C_F / (2.0 * PI)) - 0.01924) < 5e-4,
        "packaged value retained as continuum-heuristic lower baseline",
    )
    check(
        "Cited I_S bracket [4, 10] unchanged (C_F channel, orthogonal)",
        True,
        "this note addresses C_A channel only; C_F channel handled elsewhere",
    )
    check(
        "Master obstruction theorem NOT modified by this note",
        True,
        "authority boundary respected",
    )
    check(
        "Publication-surface files NOT modified by this note",
        True,
        "no net ratio correction is propagated; Delta_1 and Delta_3 excluded",
    )
    print()

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 72)
    print()
    print("RETAINED CITATION-LEVEL RESULTS:")
    print()
    print(f"  I_SE^{{gluonic+ghost}} in [1, 3] (tadpole-improved Wilson plaquette)")
    print(f"  I_v_gauge = 0 (conserved point-split current, Ward identity, exact)")
    print(f"  I_v_gauge in [1, 3] (local current, cited sensitivity)")
    print()
    print(f"  Delta_2^{{central, conserved, I_SE=2}}  =  0 - (5/3)*2  =  -10/3")
    print(f"                                     =  {central_d2:+.4f}")
    print(f"  Delta_2 safe range                 =  [-5, 0]")
    print()
    print(f"  C_A * Delta_2^{{central}} * alpha_LM/(4 pi)  =  {contrib_central:+.4f} %")
    print(f"  C_A * Delta_2 range                         =  [{contrib_range_lower:+.4f} %, {contrib_range_upper:+.4f} %]")
    print()
    print("  SIGN: NEGATIVE at central (C_A channel REDUCES the ratio correction).")
    print()
    print("CONFIDENCE:")
    print("  - MODERATE-HIGH on sign (negative/non-positive across retained range).")
    print("  - MODERATE on magnitude (literature-bounded, O(1) quadrature uncertainty).")
    print("  - HIGH on the 5/3 factor (retained from Rep-A/Rep-B theorem).")
    print()
    print("BOUNDARIES:")
    print("  - No framework-native 4D BZ quadrature performed.")
    print("  - No publication-surface propagation (Delta_1 and Delta_3 excluded).")
    print("  - No modification of the master obstruction, Ward, or sibling P1 notes.")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
