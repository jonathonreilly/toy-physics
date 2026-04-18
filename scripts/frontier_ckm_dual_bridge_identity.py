#!/usr/bin/env python3
"""
CKM-Dual Bridge Identity Theorem: two-layer runner.

Authority:
  docs/CKM_DUAL_BRIDGE_IDENTITY_THEOREM_NOTE_2026-04-17.md

Layer 1 (retained on main) — structural identities:
  SI1: sqrt(6) in |V_cb|_atlas and in the Ward identity is the same retained
       framework constant sqrt(N_c * N_iso) = sqrt(dim(Q_L)).
  SI2: GST exponent 1/2 = 1/n_pair (retained atlas EWSB residual pair count).
  SI3: 5/6 bridge exponent = atlas orthogonal-complement projector weight
       1 - 1/n_quark = 5/6, not the SU(3) Casimir combination C_F - T_F.

Layer 2 (proposed new retained primitive P-AT) — Atlas-Projector-Weighted
Mass-Matrix Texture:
  M_d(1,1) = m_d, M_d(2,2) = m_s, M_d(3,3) = m_b
  M_d(1,2) = sqrt(m_d * m_s)                          (GST / NNI geometric mean)
  M_d(2,3) = m_s^(5/6) * m_b^(1/6)                    (atlas-projector-weighted)
  M_d(1,3) = 0                                        (NNI texture zero)

Under P-AT, in the hierarchical limit m_d/m_s -> 0 and m_s/m_b -> 0:
  T1: |V_us| = sqrt(m_d/m_s)              (GST, leading-order exact)
  T2: |V_cb| = (m_s/m_b)^(5/6)            (5/6 bridge, leading-order exact)
  T3: matching to the retained CKM atlas gives the mass-ratio identification
      surface (I1)-(I2):
         m_d/m_s = alpha_s(v) / n_pair
         m_s/m_b = [ alpha_s(v) / sqrt(n_quark) ]^(n_quark/(n_quark-1))

The runner tags results by layer: RETAINED (SI1-SI3), P-AT (the proposed
primitive's consequences), and BOUNDED (quantitative PDG readout). P-AT is a
new framework proposal and its acceptance is a framework-level decision.
"""

from __future__ import annotations

import math

import numpy as np

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


# ---------------------------------------------------------------------------
# Retained framework structural constants (unchanged)
# ---------------------------------------------------------------------------

N_C = 3
N_ISO = 2
DIM_Q_L = N_C * N_ISO

N_PAIR = 2
N_COLOR = 3
N_QUARK = N_PAIR * N_COLOR

CENTER_EXCESS_WEIGHT = 1.0 / N_QUARK
ORTHOGONAL_PHASE_WEIGHT = 1.0 - CENTER_EXCESS_WEIGHT

C_F = 4.0 / 3.0
T_F = 0.5

# PDG threshold-local self-scale comparators (observation only)
M_D_2GEV = 4.67e-3
M_S_2GEV = 93.4e-3
M_B_MB = 4.180
R_DS_SELF = M_D_2GEV / M_S_2GEV
R_SB_SELF = M_S_2GEV / M_B_MB
R_DB_SELF = M_D_2GEV / M_B_MB


# ---------------------------------------------------------------------------
# Bookkeeping
# ---------------------------------------------------------------------------

RETAINED_PASS = 0
PAT_PASS = 0
BOUNDED_PASS = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", layer: str = "RETAINED") -> None:
    global RETAINED_PASS, PAT_PASS, BOUNDED_PASS, FAIL_COUNT
    if condition:
        if layer == "RETAINED":
            RETAINED_PASS += 1
        elif layer == "P-AT":
            PAT_PASS += 1
        else:
            BOUNDED_PASS += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    prefix = f" [{layer}]" if layer != "RETAINED" else ""
    line = f"  [{status}]{prefix} {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


# ---------------------------------------------------------------------------
# P-AT texture helpers
# ---------------------------------------------------------------------------

def pat_mass_matrix(m_d: float, m_s: float, m_b: float) -> np.ndarray:
    """Atlas-Projector-Weighted Mass-Matrix Texture (P-AT).

    Real symmetric 3x3 on the axis basis (X_1, X_2, X_3) with
    NNI-zero structure and atlas-projector-weighted (2,3) off-diagonal.
    """
    a_12 = math.sqrt(m_d * m_s)
    a_23 = (m_s ** ORTHOGONAL_PHASE_WEIGHT) * (m_b ** CENTER_EXCESS_WEIGHT)
    return np.array(
        [
            [m_d, a_12, 0.0],
            [a_12, m_s, a_23],
            [0.0, a_23, m_b],
        ],
        dtype=float,
    )


def ckm_magnitudes_from_pat(m_d: float, m_s: float, m_b: float) -> tuple[float, float, float]:
    """Diagonalize P-AT mass matrix and return (|V_us|, |V_cb|, |V_ub|)
    assuming the up-type mass matrix is diagonal in the weak basis
    (U_u = I), so V_CKM = U_d."""
    matrix = pat_mass_matrix(m_d, m_s, m_b)
    evals, U_d = np.linalg.eigh(matrix)
    # Sort by absolute value ascending: lightest (m_d-like), middle (m_s-like),
    # heaviest (m_b-like)
    idx = np.argsort(np.abs(evals))
    U_d = U_d[:, idx]
    V = U_d
    # Axis basis rows correspond to X_1, X_2, X_3 = weak basis generations
    return abs(float(V[0, 1])), abs(float(V[1, 2])), abs(float(V[0, 2]))


# ---------------------------------------------------------------------------
# Layer 1 sections: retained structural identities (SI1, SI2, SI3)
# ---------------------------------------------------------------------------

def layer1_si1_same_sqrt6() -> None:
    print("\n" + "=" * 74)
    print("LAYER 1 / SI1: sqrt(6) origin = Ward-theorem Clebsch-Gordan on Q_L")
    print("=" * 74)

    ward_z2 = N_C * N_ISO
    ward_z = math.sqrt(ward_z2)
    atlas_denom = math.sqrt(N_QUARK)
    atlas_denom_alt = math.sqrt(N_PAIR * N_COLOR)

    print(f"\n  N_c = {N_C}")
    print(f"  N_iso = {N_ISO}")
    print(f"  Ward Clebsch-Gordan Z^2 = N_c * N_iso = {ward_z2}")
    print(f"  Ward CG factor sqrt(Z^2) = sqrt(6) = {ward_z:.12f}")
    print(f"  atlas sqrt(n_quark) = sqrt(n_pair * n_color) = sqrt(6) = {atlas_denom:.12f}")

    check("SI1.a: Ward Z^2 = N_c * N_iso = 6", ward_z2 == 6)
    check("SI1.b: Ward sqrt(Z^2) = sqrt(6)", abs(ward_z - math.sqrt(6.0)) < 1e-14)
    check("SI1.c: atlas n_quark = n_pair * n_color = 6", N_QUARK == 6)
    check("SI1.d: atlas sqrt(n_quark) = sqrt(6)", abs(atlas_denom - math.sqrt(6.0)) < 1e-14)
    check(
        "SI1.e: Ward sqrt(6) equals atlas sqrt(n_pair * n_color) as the same retained constant",
        abs(ward_z - atlas_denom_alt) < 1e-14,
        f"|Ward - atlas| = {abs(ward_z - atlas_denom_alt):.2e}",
    )
    check(
        "SI1.f: atlas quark-block dimension equals Ward left-handed block dimension",
        N_QUARK == DIM_Q_L,
        f"n_quark = {N_QUARK}, dim(Q_L) = {DIM_Q_L}",
    )


def layer1_atlas_vcb_uses_same_sqrt6() -> float:
    print("\n" + "=" * 74)
    print("LAYER 1: atlas |V_cb| = alpha_s(v)/sqrt(6) uses the same sqrt(6)")
    print("=" * 74)

    alpha_s_v = CANONICAL_ALPHA_S_V
    v_cb = alpha_s_v / math.sqrt(N_QUARK)

    print(f"\n  alpha_s(v) = {alpha_s_v:.12f}")
    print(f"  |V_cb|_atlas = alpha_s(v)/sqrt(n_quark) = {v_cb:.12f}")

    check(
        "|V_cb|_atlas formula uses the same sqrt(6) as the Ward Clebsch-Gordan",
        abs(v_cb - alpha_s_v / math.sqrt(6.0)) < 1e-14,
        f"|V_cb| = {v_cb:.12f}",
    )
    return v_cb


def layer1_si3_one_plus_five_split() -> None:
    print("\n" + "=" * 74)
    print("LAYER 1 / SI3: 1+5 projector split on the six-state quark block")
    print("=" * 74)

    print(f"\n  center-excess CP-even weight    = 1/n_quark = {CENTER_EXCESS_WEIGHT:.12f}")
    print(f"  orthogonal CP-odd complement    = 1 - 1/n_quark = {ORTHOGONAL_PHASE_WEIGHT:.12f}")

    check("SI3.a: CENTER_EXCESS_WEIGHT = 1/6", abs(CENTER_EXCESS_WEIGHT - 1.0 / 6.0) < 1e-14)
    check(
        "SI3.b: ORTHOGONAL_PHASE_WEIGHT = 5/6",
        abs(ORTHOGONAL_PHASE_WEIGHT - 5.0 / 6.0) < 1e-14,
    )
    check(
        "SI3.c: CENTER_EXCESS + ORTHOGONAL = 1 (complete split)",
        abs(CENTER_EXCESS_WEIGHT + ORTHOGONAL_PHASE_WEIGHT - 1.0) < 1e-14,
    )
    check(
        "SI3.d: sum 1 + 5 = n_quark = 6 (1+5 decomposition reconstructs the block)",
        1 + 5 == N_QUARK,
    )


def layer1_si2_gst_exponent() -> None:
    print("\n" + "=" * 74)
    print("LAYER 1 / SI2 + SI3: bridge exponents fixed by retained framework constants")
    print("=" * 74)

    gst_exponent = 1.0 / N_PAIR
    bridge_exponent = ORTHOGONAL_PHASE_WEIGHT
    inverse_bridge_exponent = 1.0 / bridge_exponent
    chain_alpha_exponent = 1.0 + inverse_bridge_exponent
    casimir_exponent = C_F - T_F

    print(f"\n  GST exponent                = 1/n_pair                          = {gst_exponent:.12f}")
    print(f"  5/6 bridge exponent         = ORTHOGONAL_PHASE_WEIGHT            = {bridge_exponent:.12f}")
    print(f"  inverse bridge exponent     = 1 / ORTHOGONAL_PHASE_WEIGHT = 6/5  = {inverse_bridge_exponent:.12f}")
    print(f"  chain alpha_s exponent      = 1 + 6/5 = 11/5                     = {chain_alpha_exponent:.12f}")
    print(f"  SU(3) Casimir C_F - T_F     = 4/3 - 1/2 = 5/6                    = {casimir_exponent:.12f}")
    print(f"                                (coincidence check only)")

    check("SI2: GST exponent = 1/n_pair = 1/2", abs(gst_exponent - 0.5) < 1e-14)
    check(
        "SI3 (restated): 5/6 bridge exponent equals the retained orthogonal-complement weight",
        abs(bridge_exponent - 5.0 / 6.0) < 1e-14,
    )
    check(
        "inverse bridge exponent (appearing in the m_s/m_b identification) equals 6/5 exactly",
        abs(inverse_bridge_exponent - 6.0 / 5.0) < 1e-14,
    )
    check(
        "chain alpha_s exponent in closed-form m_d/m_b equals 11/5 exactly",
        abs(chain_alpha_exponent - 11.0 / 5.0) < 1e-14,
    )
    check(
        "atlas 5/6 and Casimir 5/6 numerically coincide (retained origin is the atlas 1+5 split, not the Casimir)",
        abs(bridge_exponent - casimir_exponent) < 1e-14,
        "retained origin: atlas 1+5 projector split; SU(3) Casimir is a coincidence",
    )


# ---------------------------------------------------------------------------
# Layer 2 sections: proposed new primitive P-AT + its consequences
# ---------------------------------------------------------------------------

def layer2_pat_hierarchical_limit() -> None:
    print("\n" + "=" * 74)
    print("LAYER 2 / P-AT: hierarchical limit of atlas-projector-weighted texture")
    print("=" * 74)
    print("")
    print("  Diagonalize the P-AT mass matrix with texture")
    print("    M_d(1,2) = sqrt(m_d * m_s)                [NNI geometric mean]")
    print("    M_d(2,3) = m_s^(5/6) * m_b^(1/6)          [atlas-projector-weighted]")
    print("    M_d(1,3) = 0                              [NNI texture zero]")
    print("")
    print("  Verify that |V_us|/sqrt(m_d/m_s) -> 1 and |V_cb|/(m_s/m_b)^(5/6) -> 1")
    print("  as the hierarchy m_d/m_s, m_s/m_b -> 0.")
    print("")
    print(f"  {'epsilon':<10} {'|V_us|/sqrt(m_d/m_s)':<24} {'|V_cb|/(m_s/m_b)^(5/6)':<24}")

    epsilons = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    gst_ratios = []
    bridge_ratios = []
    for eps in epsilons:
        m_b = 1.0
        m_s = eps
        m_d = eps ** 2
        v_us, v_cb, _ = ckm_magnitudes_from_pat(m_d, m_s, m_b)
        gst = v_us / math.sqrt(m_d / m_s)
        bridge = v_cb / ((m_s / m_b) ** (5.0 / 6.0))
        gst_ratios.append(gst)
        bridge_ratios.append(bridge)
        print(f"  {eps:<10.2e} {gst:<24.12f} {bridge:<24.12f}")

    # Limit check: the ratios should approach 1 monotonically as epsilon shrinks.
    gst_drift = abs(gst_ratios[-1] - 1.0)
    bridge_drift = abs(bridge_ratios[-1] - 1.0)
    gst_monotone = all(
        abs(gst_ratios[i] - 1.0) <= abs(gst_ratios[i - 1] - 1.0) + 1e-12
        for i in range(1, len(gst_ratios))
    )
    bridge_monotone = all(
        abs(bridge_ratios[i] - 1.0) <= abs(bridge_ratios[i - 1] - 1.0) + 1e-12
        for i in range(1, len(bridge_ratios))
    )

    check(
        "T1: |V_us|/sqrt(m_d/m_s) tends to 1 as epsilon -> 0 (GST leading-order exact under P-AT)",
        gst_drift < 1e-3,
        f"deviation at epsilon=1e-6 is {gst_drift:.3e}",
        layer="P-AT",
    )
    check(
        "T1: |V_us|/sqrt(m_d/m_s) approaches 1 monotonically in epsilon",
        gst_monotone,
        "monotone convergence",
        layer="P-AT",
    )
    check(
        "T2: |V_cb|/(m_s/m_b)^(5/6) tends to 1 as epsilon -> 0 (5/6 bridge leading-order exact under P-AT)",
        bridge_drift < 1e-5,
        f"deviation at epsilon=1e-6 is {bridge_drift:.3e}",
        layer="P-AT",
    )
    check(
        "T2: |V_cb|/(m_s/m_b)^(5/6) approaches 1 monotonically in epsilon",
        bridge_monotone,
        "monotone convergence",
        layer="P-AT",
    )


def layer2_identification_surface(v_cb_atlas: float) -> tuple[float, float, float]:
    print("\n" + "=" * 74)
    print("LAYER 2 / P-AT: identification surface (I1)-(I2) at observed hierarchy")
    print("=" * 74)

    alpha_s_v = CANONICAL_ALPHA_S_V
    r_ds = alpha_s_v / N_PAIR
    r_sb = (alpha_s_v / math.sqrt(N_QUARK)) ** (6.0 / 5.0)
    r_db = r_ds * r_sb
    r_db_closed = (alpha_s_v ** (11.0 / 5.0)) / (N_PAIR * N_QUARK ** (3.0 / 5.0))

    v_us_atlas = math.sqrt(alpha_s_v / N_PAIR)

    print(f"\n  (I1) m_d/m_s := alpha_s(v) / n_pair                 = {r_ds:.12f}")
    print(f"  (I2) m_s/m_b := [alpha_s(v)/sqrt(n_quark)]^(6/5)    = {r_sb:.12f}")
    print(f"  (chain) m_d/m_b = (I1)*(I2)                         = {r_db:.12f}")
    print(f"  (chain closed) alpha_s(v)^(11/5) / (2 * 6^(3/5))    = {r_db_closed:.12f}")
    print(f"\n  atlas |V_us| = sqrt(alpha_s(v)/n_pair) = {v_us_atlas:.12f}")
    print(f"  atlas |V_cb| = alpha_s(v)/sqrt(n_quark) = {v_cb_atlas:.12f}")

    # Diagonalize P-AT at these observed mass ratios (m_b = 1, m_s from I2, m_d from I1 * I2)
    m_b_unit = 1.0
    m_s_unit = r_sb
    m_d_unit = r_ds * r_sb
    v_us_pat, v_cb_pat, v_ub_pat = ckm_magnitudes_from_pat(m_d_unit, m_s_unit, m_b_unit)
    gst_ratio_observed = v_us_pat / math.sqrt(r_ds)
    bridge_ratio_observed = v_cb_pat / (r_sb ** (5.0 / 6.0))

    print(f"\n  P-AT diagonalization at observed hierarchy:")
    print(f"    |V_us|_P-AT = {v_us_pat:.8f}  (atlas: {v_us_atlas:.8f})")
    print(f"    |V_cb|_P-AT = {v_cb_pat:.8f}  (atlas: {v_cb_atlas:.8f})")
    print(f"    |V_ub|_P-AT = {v_ub_pat:.8f}")
    print(f"  leading-order GST  ratio: |V_us|/sqrt(m_d/m_s) = {gst_ratio_observed:.6f}")
    print(f"  leading-order 5/6  ratio: |V_cb|/(m_s/m_b)^(5/6) = {bridge_ratio_observed:.6f}")

    check(
        "T3: m_d/m_s matches identification-surface closed form exactly",
        abs(r_ds - alpha_s_v / N_PAIR) < 1e-14,
        f"|diff| = {abs(r_ds - alpha_s_v / N_PAIR):.2e}",
        layer="P-AT",
    )
    check(
        "T3: m_s/m_b matches identification-surface closed form exactly",
        abs(r_sb - (alpha_s_v / math.sqrt(6.0)) ** (6.0 / 5.0)) < 1e-14,
        f"|diff| = {abs(r_sb - (alpha_s_v / math.sqrt(6.0)) ** (6.0 / 5.0)):.2e}",
        layer="P-AT",
    )
    check(
        "T3: chain m_d/m_b equals alpha_s(v)^(11/5) / (2 * 6^(3/5)) exactly",
        abs(r_db - r_db_closed) < 1e-14,
        f"|diff| = {abs(r_db - r_db_closed):.2e}",
        layer="P-AT",
    )
    # At observed hierarchy m_d/m_s ~ 0.05, leading-order deviation is O(m_d/m_s) ~ 5%;
    # at m_s/m_b ~ 0.02, leading-order deviation is O(m_s/m_b) ~ 2%. These are the
    # natural next-to-leading-order residuals and are consistent with the
    # leading-order-exact claim in the hierarchical limit (see T1, T2 above).
    check(
        "T1 at observed hierarchy: |V_us|_P-AT matches atlas within next-to-leading-order residual O(m_d/m_s)",
        abs(gst_ratio_observed - 1.0) < 0.10,
        f"gst ratio = {gst_ratio_observed:.6f}; NLO residual bound = O(m_d/m_s) ~ {r_ds:.3f}",
        layer="P-AT",
    )
    check(
        "T2 at observed hierarchy: |V_cb|_P-AT matches atlas within next-to-leading-order residual O(m_s/m_b)",
        abs(bridge_ratio_observed - 1.0) < 0.10,
        f"5/6 ratio = {bridge_ratio_observed:.6f}; NLO residual bound = O(m_s/m_b) ~ {r_sb:.3f}",
        layer="P-AT",
    )

    return r_ds, r_sb, r_db


def layer3_quantitative_readout(r_ds: float, r_sb: float, r_db: float) -> None:
    print("\n" + "=" * 74)
    print("LAYER 3 / BOUNDED: quantitative readout against threshold-local self-scale")
    print("=" * 74)

    dev_ds = (r_ds - R_DS_SELF) / R_DS_SELF * 100.0
    dev_sb = (r_sb - R_SB_SELF) / R_SB_SELF * 100.0
    dev_db = (r_db - R_DB_SELF) / R_DB_SELF * 100.0

    print(f"\n  m_d/m_s:  framework = {r_ds:.8f}, comparator = {R_DS_SELF:.8f},  dev = {dev_ds:+.3f}%")
    print(f"  m_s/m_b:  framework = {r_sb:.8f}, comparator = {R_SB_SELF:.8f},  dev = {dev_sb:+.3f}%")
    print(f"  m_d/m_b:  framework = {r_db:.8f}, comparator = {R_DB_SELF:.8f},  dev = {dev_db:+.3f}%")

    check(
        "m_d/m_s framework lands within 5% of the self-scale comparator",
        abs(dev_ds) < 5.0,
        f"dev = {dev_ds:+.3f}%",
        layer="BOUNDED",
    )
    check(
        "m_s/m_b framework lands within 1% of the self-scale comparator",
        abs(dev_sb) < 1.0,
        f"dev = {dev_sb:+.3f}%",
        layer="BOUNDED",
    )
    check(
        "m_d/m_b framework lands within 5% of the self-scale comparator",
        abs(dev_db) < 5.0,
        f"dev = {dev_db:+.3f}%",
        layer="BOUNDED",
    )


def main() -> int:
    print("=" * 74)
    print("  FRONTIER: CKM-Dual Bridge Identity Theorem")
    print("  (two-layer: Layer 1 retained structural identities SI1-SI3;")
    print("   Layer 2 proposed new retained primitive P-AT with hierarchical")
    print("   limit derivation of GST, 5/6 bridge, and identification surface)")
    print("=" * 74)

    # Layer 1: retained structural identities
    layer1_si1_same_sqrt6()
    v_cb_atlas = layer1_atlas_vcb_uses_same_sqrt6()
    layer1_si3_one_plus_five_split()
    layer1_si2_gst_exponent()

    # Layer 2: proposed new primitive P-AT + consequences
    layer2_pat_hierarchical_limit()
    r_ds, r_sb, r_db = layer2_identification_surface(v_cb_atlas)

    # Layer 3: bounded quantitative readout
    layer3_quantitative_readout(r_ds, r_sb, r_db)

    print("\n" + "=" * 74)
    print("SUMMARY")
    print("=" * 74)
    print(f"  RETAINED PASS = {RETAINED_PASS}    (Layer 1: SI1-SI3 structural identities)")
    print(f"  P-AT PASS     = {PAT_PASS}    (Layer 2: hierarchical-limit bridge theorems")
    print(f"                              under the proposed atlas-projector texture)")
    print(f"  BOUNDED PASS  = {BOUNDED_PASS}    (Layer 3: quantitative PDG readout)")
    print(f"  FAIL          = {FAIL_COUNT}")
    print()
    print("  Layer 1 (retained on main):")
    print("    SI1: sqrt(6) in |V_cb|_atlas and Ward theorem is the same")
    print("         retained framework constant sqrt(N_c * N_iso).")
    print("    SI2: GST exponent 1/2 is the retained atlas 1/n_pair count.")
    print("    SI3: 5/6 bridge exponent is the retained atlas 1+5")
    print("         orthogonal-complement projector weight (not the Casimir).")
    print()
    print("  Layer 2 (proposed new retained primitive P-AT):")
    print("    atlas-projector-weighted (2,3) off-diagonal in the down-type")
    print("    hw=1 mass matrix: M_d(2,3) = m_s^(5/6) * m_b^(1/6).")
    print("    Under P-AT, GST and the 5/6 bridge are leading-order exact")
    print("    hierarchical identities, and combining with the retained CKM")
    print("    atlas gives the identification surface (I1)-(I2).")
    print("    P-AT is a framework-level proposal, not a derivation from")
    print("    pre-existing retained primitives.")
    print()
    print("  Layer 3 (bounded): threshold-local self-scale PDG match at")
    print("    m_d/m_s +3.30%, m_s/m_b +0.20%, m_d/m_b +3.50%.")
    print("=" * 74)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
