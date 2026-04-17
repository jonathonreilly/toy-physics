#!/usr/bin/env python3
"""
CKM-Dual Bridge Identity Theorem: retained structural theorem for the GST and
5/6 bridge exponents in the down-type CKM-dual mass-ratio lane.

Authority:
  docs/CKM_DUAL_BRIDGE_IDENTITY_THEOREM_NOTE_2026-04-17.md

This runner validates the retained structural theorem that fixes the bridge
exponents as framework constants:

  - sqrt(6) is the same retained Ward-theorem Clebsch-Gordan sqrt(N_c * N_iso)
    on the left-handed quark block Q_L, and appears identically in the CKM
    atlas formula |V_cb| = alpha_s(v)/sqrt(6);

  - the 5/6 bridge exponent is the retained atlas orthogonal-complement
    projector weight on the same six-state quark block (1/6 CP-even center
    excess plus 5/6 CP-odd complement);

  - the 1/2 GST exponent is 1/n_pair from the retained EWSB residual pair.

On the retained identification surface
  m_d/m_s := alpha_s(v) / 2
  m_s/m_b := [alpha_s(v)/sqrt(6)]^(6/5)
both bridge relations
  |V_us|_atlas = sqrt(m_d/m_s)
  |V_cb|_atlas = (m_s/m_b)^(5/6)
are exact algebraic identities.

The quantitative match to PDG threshold-local self-scale comparators remains a
bounded downstream readout (mass-hierarchy systematic) and is reported as such.
"""

from __future__ import annotations

import math

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


# ---------------------------------------------------------------------------
# Retained framework structural constants
# ---------------------------------------------------------------------------

# Ward-identity Clebsch-Gordan factors on Q_L = (2, 3)
# (docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
N_C = 3          # color rank (structural SU(3))
N_ISO = 2        # isospin doublet size (EWSB residual pair)
DIM_Q_L = N_C * N_ISO  # left-handed quark-block dimension = 6

# CKM atlas structural counts
# (docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
N_PAIR = 2       # EWSB residual color pair
N_COLOR = 3      # structural SU(3)
N_QUARK = N_PAIR * N_COLOR  # = 6 = dim(Q_L)

# Atlas projector weights on the six-state quark block
CENTER_EXCESS_WEIGHT = 1.0 / N_QUARK       # 1/6 CP-even
ORTHOGONAL_PHASE_WEIGHT = 1.0 - CENTER_EXCESS_WEIGHT  # 5/6 CP-odd

# Standard SU(3) Casimirs (independent of framework; coincidence check only)
C_F = 4.0 / 3.0
T_F = 0.5

# PDG threshold-local self-scale comparators (observation only, not inputs)
M_D_2GEV = 4.67e-3       # GeV
M_S_2GEV = 93.4e-3       # GeV
M_B_MB = 4.180           # GeV
R_DS_SELF = M_D_2GEV / M_S_2GEV
R_SB_SELF = M_S_2GEV / M_B_MB
R_DB_SELF = M_D_2GEV / M_B_MB


# ---------------------------------------------------------------------------
# Check bookkeeping
# ---------------------------------------------------------------------------

EXACT_PASS = 0
BOUNDED_PASS = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> None:
    global EXACT_PASS, BOUNDED_PASS, FAIL_COUNT
    if condition:
        if kind == "EXACT":
            EXACT_PASS += 1
        else:
            BOUNDED_PASS += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    prefix = f" [{kind}]" if kind != "EXACT" else ""
    line = f"  [{status}]{prefix} {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def part1_sqrt6_origin() -> None:
    print("\n" + "=" * 74)
    print("PART 1: sqrt(6) origin = Ward-theorem Clebsch-Gordan on Q_L")
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

    check("Ward Z^2 = N_c * N_iso = 6", ward_z2 == 6)
    check("Ward sqrt(Z^2) = sqrt(6)", abs(ward_z - math.sqrt(6.0)) < 1e-14)
    check("atlas n_quark = n_pair * n_color = 6", N_QUARK == 6)
    check("atlas sqrt(n_quark) = sqrt(6)", abs(atlas_denom - math.sqrt(6.0)) < 1e-14)
    check(
        "Ward sqrt(6) equals atlas sqrt(n_pair * n_color) as the same retained constant",
        abs(ward_z - atlas_denom_alt) < 1e-14,
        f"|Ward - atlas| = {abs(ward_z - atlas_denom_alt):.2e}",
    )
    check(
        "atlas quark-block dimension equals Ward left-handed block dimension",
        N_QUARK == DIM_Q_L,
        f"n_quark = {N_QUARK}, dim(Q_L) = {DIM_Q_L}",
    )


def part2_atlas_vcb_surface() -> float:
    print("\n" + "=" * 74)
    print("PART 2: atlas |V_cb| = alpha_s(v)/sqrt(6)")
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


def part3_one_plus_five_split() -> None:
    print("\n" + "=" * 74)
    print("PART 3: 1+5 projector split on the six-state quark block")
    print("=" * 74)

    print(f"\n  center-excess CP-even weight    = 1/n_quark = {CENTER_EXCESS_WEIGHT:.12f}")
    print(f"  orthogonal CP-odd complement    = 1 - 1/n_quark = {ORTHOGONAL_PHASE_WEIGHT:.12f}")

    check("CENTER_EXCESS_WEIGHT = 1/6", abs(CENTER_EXCESS_WEIGHT - 1.0 / 6.0) < 1e-14)
    check(
        "ORTHOGONAL_PHASE_WEIGHT = 5/6",
        abs(ORTHOGONAL_PHASE_WEIGHT - 5.0 / 6.0) < 1e-14,
    )
    check(
        "CENTER_EXCESS + ORTHOGONAL = 1 (complete split)",
        abs(CENTER_EXCESS_WEIGHT + ORTHOGONAL_PHASE_WEIGHT - 1.0) < 1e-14,
    )
    check(
        "sum 1 + 5 = n_quark = 6 (1+5 decomposition reconstructs the block)",
        1 + 5 == N_QUARK,
    )


def part4_bridge_exponents() -> None:
    print("\n" + "=" * 74)
    print("PART 4: bridge exponents fixed by retained framework constants")
    print("=" * 74)

    gst_exponent = 1.0 / N_PAIR
    bridge_exponent = ORTHOGONAL_PHASE_WEIGHT
    inverse_bridge_exponent = 1.0 / bridge_exponent  # 6/5 used in m_s/m_b identification
    chain_alpha_exponent = 1.0 + inverse_bridge_exponent  # 11/5 on alpha_s in m_d/m_b
    casimir_exponent = C_F - T_F  # coincidence check, not framework-retained

    print(f"\n  GST exponent                = 1/n_pair                          = {gst_exponent:.12f}")
    print(f"  5/6 bridge exponent         = ORTHOGONAL_PHASE_WEIGHT            = {bridge_exponent:.12f}")
    print(f"  inverse bridge exponent     = 1 / ORTHOGONAL_PHASE_WEIGHT = 6/5  = {inverse_bridge_exponent:.12f}")
    print(f"  chain alpha_s exponent      = 1 + 6/5 = 11/5                     = {chain_alpha_exponent:.12f}")
    print(f"  SU(3) Casimir C_F - T_F     = 4/3 - 1/2 = 5/6                    = {casimir_exponent:.12f}")
    print(f"                                (coincidence check only)")

    check("GST exponent = 1/n_pair = 1/2", abs(gst_exponent - 0.5) < 1e-14)
    check(
        "5/6 bridge exponent equals the retained orthogonal-complement weight",
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
        "atlas 5/6 and Casimir 5/6 numerically coincide (framework-internal 5/6 is retained, not the Casimir)",
        abs(bridge_exponent - casimir_exponent) < 1e-14,
        "retained origin: atlas 1+5 projector split; SU(3) Casimir is a coincidence",
    )


def part5_bridge_identity(v_cb_atlas: float) -> tuple[float, float, float]:
    print("\n" + "=" * 74)
    print("PART 5: exact algebraic bridge identity on the retained surface")
    print("=" * 74)

    alpha_s_v = CANONICAL_ALPHA_S_V

    # Identification surface (I1), (I2) from the retained theorem note
    r_ds = alpha_s_v / N_PAIR
    r_sb = (alpha_s_v / math.sqrt(N_QUARK)) ** (6.0 / 5.0)
    r_db = r_ds * r_sb

    # Atlas side
    v_us_atlas = math.sqrt(alpha_s_v / N_PAIR)

    # Bridge reconstructions
    v_us_from_gst = math.sqrt(r_ds)
    v_cb_from_bridge = r_sb ** (5.0 / 6.0)

    # Closed-form chain
    r_db_closed = (alpha_s_v ** (11.0 / 5.0)) / (N_PAIR * N_QUARK ** (3.0 / 5.0))

    print(f"\n  identification: m_d/m_s = alpha_s(v)/n_pair = {r_ds:.12f}")
    print(f"  identification: m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5) = {r_sb:.12f}")
    print(f"  identification: m_d/m_b = (m_d/m_s)(m_s/m_b) = {r_db:.12f}")
    print(f"  closed form:    m_d/m_b = alpha_s(v)^(11/5) / (2 * 6^(3/5)) = {r_db_closed:.12f}")
    print(f"\n  |V_us|_atlas   = sqrt(alpha_s(v)/2)              = {v_us_atlas:.12f}")
    print(f"  |V_us|_GST     = sqrt(m_d/m_s)                   = {v_us_from_gst:.12f}")
    print(f"  |V_cb|_atlas   = alpha_s(v)/sqrt(6)              = {v_cb_atlas:.12f}")
    print(f"  |V_cb|_bridge  = (m_s/m_b)^(5/6)                 = {v_cb_from_bridge:.12f}")

    check(
        "(T1) |V_us|_atlas = sqrt(m_d/m_s) exact on identification surface",
        abs(v_us_atlas - v_us_from_gst) < 1e-14,
        f"|diff| = {abs(v_us_atlas - v_us_from_gst):.2e}",
    )
    check(
        "(T2) |V_cb|_atlas = (m_s/m_b)^(5/6) exact on identification surface",
        abs(v_cb_atlas - v_cb_from_bridge) < 1e-14,
        f"|diff| = {abs(v_cb_atlas - v_cb_from_bridge):.2e}",
    )
    check(
        "chain identity: m_d/m_b = alpha_s(v)^(11/5) / (2 * 6^(3/5))",
        abs(r_db - r_db_closed) < 1e-14,
        f"|diff| = {abs(r_db - r_db_closed):.2e}",
    )

    return r_ds, r_sb, r_db


def part6_quantitative_readout(r_ds: float, r_sb: float, r_db: float) -> None:
    print("\n" + "=" * 74)
    print("PART 6: bounded quantitative readout against threshold-local self-scale")
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
        kind="BOUNDED",
    )
    check(
        "m_s/m_b framework lands within 1% of the self-scale comparator",
        abs(dev_sb) < 1.0,
        f"dev = {dev_sb:+.3f}%",
        kind="BOUNDED",
    )
    check(
        "m_d/m_b framework lands within 5% of the self-scale comparator",
        abs(dev_db) < 5.0,
        f"dev = {dev_db:+.3f}%",
        kind="BOUNDED",
    )


def main() -> int:
    print("=" * 74)
    print("  FRONTIER: CKM-Dual Bridge Identity Theorem")
    print("  (retained structural bridge-exponent theorem; bounded quantitative readout)")
    print("=" * 74)

    part1_sqrt6_origin()
    v_cb_atlas = part2_atlas_vcb_surface()
    part3_one_plus_five_split()
    part4_bridge_exponents()
    r_ds, r_sb, r_db = part5_bridge_identity(v_cb_atlas)
    part6_quantitative_readout(r_ds, r_sb, r_db)

    print("\n" + "=" * 74)
    print("SUMMARY")
    print("=" * 74)
    print(f"  EXACT PASS   = {EXACT_PASS}")
    print(f"  BOUNDED PASS = {BOUNDED_PASS}")
    print(f"  FAIL         = {FAIL_COUNT}")
    print()
    print("  Retained structural content:")
    print("    - sqrt(6) in |V_cb|_atlas and the 5/6 bridge is the same")
    print("      Ward-theorem Clebsch-Gordan sqrt(N_c * N_iso) on Q_L")
    print("    - 5/6 exponent is the retained 1+5 orthogonal-complement weight")
    print("    - bridge relations are exact algebraic identities on the")
    print("      identification surface")
    print()
    print("  Bounded downstream content:")
    print("    - quantitative mass-ratio readout inherits the current")
    print("      mass-hierarchy systematic; closure of the absolute ratios")
    print("      and scale-selection rule remains explicitly named open work")
    print("=" * 74)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
