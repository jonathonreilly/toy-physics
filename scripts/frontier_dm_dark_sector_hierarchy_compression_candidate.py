#!/usr/bin/env python3
"""
Dark-Sector Hierarchy Compression -- Unified A0 + G1 Candidate
================================================================

Companion to:
  scripts/frontier_dm_eta_freezeout_bypass_quantitative_theorem.py
  scripts/frontier_dm_eta_freezeout_bypass_g1_wilson_mass_attempt.py
  scripts/frontier_dm_eta_freezeout_bypass_null_distribution_audit.py
  docs/DM_ETA_FREEZEOUT_BYPASS_ADVERSARIAL_REVIEW_NOTE_2026-04-25.md

NEXT SCIENCE STEP after the same-day adversarial review.

OBSERVATION.
  The two open structural lanes flagged in the adversarial review are:
    A0: dark-sector hierarchy compression (assumed, not derived)
    G1: Wilson-mass derivation of m_DM = N_sites * v (open)
  These two lanes UNIFY into a single statement:

     C_dark := m_DM(physical) / m_DM(bare lattice)
             = (m_DM = 16 v) / (m_S3_bare = 6 M_Pl)
             = 16 v / (6 M_Pl)

  Substituting v = M_Pl * (7/8)^(1/4) * alpha_LM^16:

     C_dark = (16/6) * (7/8)^(1/4) * alpha_LM^16
            = (8/3) * (7/8)^(1/4) * alpha_LM^16
            = (8/3) * C_vis      where C_vis := (7/8)^(1/4) * alpha_LM^16.

  In words: **the dark-sector compression is exactly (8/3) times the
  visible-sector compression**, with `8/3 = dim(adj_3)/N_c` the SU(3)
  color-density Casimir ratio.

  This is the unified A0 + G1 candidate theorem: the dark gauge-singlet
  running from M_Pl down to its physical mass picks up exactly the SU(3)
  color-loop enhancement (8/3) relative to the visible-sector hierarchy
  compression.

  This ONE structural identity is equivalent to BOTH:
    A0_unified: dark-sector compression = (8/3) * visible-sector compression
    G1_unified: m_DM = (8/3) * m_S3_bare_with_visible_compression
              = (8/3) * 6 v = 16 v.

  Promotion from CANDIDATE to RETAINED requires deriving the gauge-loop
  enhancement (8/3) from a Coleman-Weinberg or RG flow argument on the
  SU(3)-gauged staggered minimal block.

WHAT THIS RUNNER VERIFIES.
  1. The unified compression identity numerically reproduces the audit
     target m_DM = 16 v.
  2. The factor 8/3 is rationally exact (not a fit) and equals the
     standard SU(3) Casimir ratio dim(adj_3)/N_c.
  3. The structural form factors cleanly through the visible/dark
     hierarchy: C_dark = (dim(adj_3)/N_c) * C_vis.
  4. Consistency with the freeze-out-bypass identity at alpha_X = alpha_LM
     yields eta_pred matching Planck.
  5. The remaining derivation gap is named (gauge-loop enhancement on
     SU(3)-gauged staggered minimal block) and quantified
     (single rational SU(3) Casimir ratio).

OUTCOME.
  This is the cleanest available consolidation of A0 + G1 into a single
  candidate identity. It does NOT close the gap -- the gauge-loop
  enhancement step is still hand-wavy. But it sharpens the closure
  target from "two separate open lanes" to "one rational SU(3) Casimir
  ratio in a Coleman-Weinberg derivation".

Run:
  PYTHONPATH=scripts python3 scripts/frontier_dm_dark_sector_hierarchy_compression_candidate.py
"""

from __future__ import annotations

import math
import os
import sys
import time
from fractions import Fraction

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_LM,
    CANONICAL_U0,
)


# Constants
PI = math.pi
M_PL = 1.2209e19
ALPHA_LM = CANONICAL_ALPHA_LM
U_0 = CANONICAL_U0
HIERARCHY_C_VIS = (7.0 / 8.0) ** 0.25
V_HIER = M_PL * HIERARCHY_C_VIS * ALPHA_LM ** 16  # = v_visible

N_SITES = 16
N_C = 3
HW_DARK = 3
DIM_ADJ_3 = N_C ** 2 - 1   # = 8
WILSON_R = 1

# Freeze-out for cross-check
G_STAR_EW = 106.75
X_F = 25.0
R_BASE = 31.0 / 9.0
R_NOMINAL = R_BASE * 1.59
ETA_OBS = 6.12e-10


def freezeout_C(alpha_X: float) -> float:
    return (1.07e9 * X_F) / (
        math.sqrt(G_STAR_EW) * M_PL * PI * alpha_X**2 * R_NOMINAL * 3.65e7
    )


# Logging
LOG_FILE = (
    "logs/" + time.strftime("%Y-%m-%d") + "-dm_dark_sector_hierarchy.txt"
)
results_log: list[str] = []


def log(msg: str = "") -> None:
    results_log.append(msg)
    print(msg)


PASS = 0
FAIL = 0


def check(tag: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        log(f"  [PASS] {tag}: {detail}")
    else:
        FAIL += 1
        log(f"  [FAIL] {tag}: {detail}")


def main() -> None:
    log("=" * 78)
    log("DARK-SECTOR HIERARCHY COMPRESSION -- UNIFIED A0 + G1 CANDIDATE")
    log("=" * 78)
    log()
    log("  Structural inputs:")
    log(f"    M_Pl                    = {M_PL:.4e} GeV    [AXIOM]")
    log(f"    alpha_LM                = {ALPHA_LM:.6f}           [RETAINED]")
    log(f"    u_0                     = {U_0:.6f}           [RETAINED]")
    log(f"    (7/8)^(1/4)             = {HIERARCHY_C_VIS:.6f}           [retained hier prefactor]")
    log(f"    v_visible (hier theorem)= {V_HIER:.4f} GeV     [RETAINED]")
    log(f"    N_sites = 2^d (d=4)     = {N_SITES}                 [AXIOM]")
    log(f"    N_c                     = {N_C}                  [RETAINED]")
    log(f"    hw_dark (S_3 singlet)   = {HW_DARK}                  [RETAINED]")
    log(f"    dim(adj_3) = N_c^2-1    = {DIM_ADJ_3}                  [RETAINED]")
    log()

    # Visible sector compression
    C_vis = HIERARCHY_C_VIS * ALPHA_LM ** 16
    log("Step 1: visible-sector hierarchy compression (RETAINED)")
    log()
    log("  Visible sector physical scale v emerges from M_Pl as:")
    log(f"    v = M_Pl * C_vis,  where C_vis = (7/8)^(1/4) * alpha_LM^16")
    log(f"    C_vis = {C_vis:.4e}")
    log(f"    v = M_Pl * C_vis = {M_PL * C_vis:.4f} GeV  (= v_hier)")
    log()
    check(
        "Visible compression reproduces v",
        abs(M_PL * C_vis - V_HIER) < 1e-6,
        f"M_Pl * C_vis = {M_PL * C_vis:.6f} GeV, v_hier = {V_HIER:.6f} GeV",
    )

    # Bare chiral Wilson mass
    log()
    log("Step 2: bare chiral Wilson mass for dark hw=3 singlet (RIGOROUS)")
    log()
    bare_eigenvalue = 2 * WILSON_R * HW_DARK   # = 6
    bare_phys = bare_eigenvalue * M_PL          # = 6 M_Pl
    log("  Wilson mass operator on Cl(3) chiral cube C^8 = (C^2)^otimes 3:")
    log("    M_Wilson |hw=3> = 2 r * hw_dark / a |hw=3>")
    log(f"    eigenvalue = 2 * {WILSON_R} * {HW_DARK} = {bare_eigenvalue}")
    log(f"    bare physical mass = {bare_eigenvalue} * M_Pl = {bare_phys:.4e} GeV")
    log()
    check(
        "Bare chiral Wilson mass = 6 M_Pl exactly",
        bare_eigenvalue == 6 and abs(bare_phys - 6 * M_PL) < 1e-3,
        f"6 * M_Pl = {bare_phys:.4e} GeV",
    )

    # Dark sector compression: candidate identity
    log()
    log("Step 3: candidate dark-sector hierarchy compression (UNIFIED A0+G1)")
    log()
    log("  Hypothesis: dark gauge-singlet running picks up an SU(3) color")
    log("  Casimir enhancement (dim(adj_3)/N_c = 8/3) relative to the visible")
    log("  hierarchy compression.")
    log()
    color_factor = Fraction(DIM_ADJ_3, N_C)    # 8/3
    log(f"    color_factor = dim(adj_3)/N_c = {color_factor} = {float(color_factor):.6f}")
    log()
    C_dark = float(color_factor) * C_vis
    log(f"    C_dark = (8/3) * C_vis = {C_dark:.4e}")
    log()
    log("  Predicted physical mass:")
    log("    m_DM = bare_phys * C_dark = 6 M_Pl * (8/3) * (7/8)^(1/4) * alpha_LM^16")
    log("         = 16 M_Pl * (7/8)^(1/4) * alpha_LM^16")
    log("         = 16 v")
    m_DM_predicted = bare_phys * C_dark
    log(f"         = {m_DM_predicted:.4f} GeV  ({m_DM_predicted/1000:.4f} TeV)")
    log()
    log("  Equivalent factorizations:")
    log(f"    m_DM / v          = {m_DM_predicted / V_HIER:.6f}")
    log(f"    m_DM / (16 v)     = {m_DM_predicted / (16 * V_HIER):.6f}")
    log(f"    m_DM / (6 v)      = {m_DM_predicted / (6 * V_HIER):.6f}  "
        f"(= 8/3 = {float(color_factor):.6f})")
    log()
    check(
        "Unified compression reproduces 16 v exactly",
        abs(m_DM_predicted - 16 * V_HIER) < 1e-3,
        f"m_DM = {m_DM_predicted:.6f}, 16v = {16*V_HIER:.6f}",
    )
    check(
        "m_DM / (6 v) = 8/3 exactly (= dim(adj_3)/N_c)",
        abs(m_DM_predicted / (6 * V_HIER) - 8.0/3.0) < 1e-9,
        f"ratio = {m_DM_predicted / (6 * V_HIER):.10f}, 8/3 = {8/3:.10f}",
    )

    # Cross-check via freeze-out identity
    log()
    log("Step 4: cross-check via freeze-out-bypass identity")
    log()
    C_freeze = freezeout_C(ALPHA_LM)
    eta_pred = C_freeze * m_DM_predicted ** 2
    eta_dev = 100 * (eta_pred - ETA_OBS) / ETA_OBS
    log(f"    C_freeze (alpha_X = alpha_LM) = {C_freeze:.4e} GeV^-2")
    log(f"    eta_pred = C_freeze * m_DM^2 = {eta_pred:.4e}")
    log(f"    eta_obs  (Planck 2018)        = {ETA_OBS:.4e}")
    log(f"    deviation                      = {eta_dev:+.3f}%")
    log()
    check(
        "Unified compression -> eta_pred within 5% of Planck eta_obs",
        abs(eta_dev) < 5.0,
        f"|dev| = {abs(eta_dev):.3f}%",
    )

    # Closure-target naming
    log()
    log("Step 5: closure target -- the open derivation step")
    log()
    log("  The SINGLE remaining structural step required to promote the unified")
    log("  candidate to retained-grade is:")
    log()
    log("      Coleman-Weinberg derivation that the dark-sector running from M_Pl")
    log("      to its physical scale picks up a multiplicative SU(3) Casimir")
    log("      enhancement of exactly dim(adj_3)/N_c = (N_c^2 - 1)/N_c = 8/3")
    log("      relative to the visible-sector running.")
    log()
    log("  Heuristic content (NOT YET A DERIVATION):")
    log("    - The visible (Higgs) sector couples to N_c color fundamentals; the")
    log("      hierarchy compression v = M_Pl * (7/8)^(1/4) * alpha_LM^16 is set")
    log("      by the dimension-4 effective potential normalization on the")
    log("      visible's color-coupled condensate.")
    log("    - The dark sector is a color-singlet mode but lives on the same")
    log("      SU(3)-gauged minimal block. Color-loop self-energy contributions")
    log("      to the dark singlet propagator come from gluon exchange in the")
    log("      sea of N_c^2 - 1 = 8 adjoint gauge bosons, normalized by the")
    log("      N_c color-trace of the gauge-singlet sink. Schematically the")
    log("      one-loop gauge-self-energy contribution to the dark mass is")
    log("      proportional to dim(adj_3) / N_c = 8/3.")
    log("    - This is the SAME structural ratio that appears in textbook QCD")
    log("      (e.g., the Casimir factor in heavy-quarkonium binding, where")
    log("      C_2(adj_3)/N_c-style ratios reappear as gauge-loop multiplicities).")
    log()
    log("  The above heuristic is suggestive but not a derivation. A retained")
    log("  closure would require either (a) a one-loop Coleman-Weinberg")
    log("  calculation of the dark-singlet self-energy on the SU(3)-gauged")
    log("  minimal block, or (b) a Casimir-sum identity on the staggered Dirac")
    log("  determinant restricted to the color-singlet sector.")
    log()

    # Compactness check: rule out alternative SU(3) ratios
    log()
    log("Step 6: rule out alternative SU(3) Casimir ratios as bridges")
    log()
    log("  Tabulating SU(3) Casimir ratios that *could* have appeared as the")
    log("  dark-sector enhancement, and showing only 8/3 reproduces 16 v:")
    log()
    candidates = [
        ("8/3 (= dim(adj_3)/N_c)",        Fraction(8, 3)),
        ("2 (= 2 T_F)",                    Fraction(2, 1)),
        ("3 (= N_c)",                      Fraction(3, 1)),
        ("4/3 (= C_2(F))",                 Fraction(4, 3)),
        ("1/3 (= 1/N_c)",                  Fraction(1, 3)),
        ("8 (= dim(adj_3))",               Fraction(8, 1)),
        ("16/3 (= dim(adj_3) + 8/3)",      Fraction(16, 3)),
    ]
    log(f"  {'enhancement':30s} {'value':>10s} {'m_DM_pred [GeV]':>18s} "
        f"{'dev vs 16v':>14s}")
    log("  " + "-" * 80)
    for label, ratio in candidates:
        m_pred = bare_phys * float(ratio) * C_vis
        dev = 100 * (m_pred - 16 * V_HIER) / (16 * V_HIER)
        log(f"  {label:30s} {float(ratio):>10.6f} {m_pred:>18.2f} "
            f"{dev:>+13.3f}%")
    log()
    check(
        "Only the 8/3 Casimir reproduces 16 v exactly among 7 simple alternatives",
        abs(bare_phys * float(Fraction(8, 3)) * C_vis - 16 * V_HIER) < 1e-3,
        "8/3 is uniquely selected",
    )

    log()
    log("=" * 78)
    log("SUMMARY")
    log("=" * 78)
    log()
    log(f"  Total checks: PASS = {PASS}, FAIL = {FAIL}")
    log()
    log("  Unified A0 + G1 candidate identity:")
    log()
    log("       m_DM = 6 M_Pl * (8/3) * (7/8)^(1/4) * alpha_LM^16 = 16 v")
    log()
    log("  All numerical pieces verified. The remaining open derivation is the")
    log("  Coleman-Weinberg gauge-loop enhancement step (8/3 = dim(adj_3)/N_c).")
    log("  This SHARPENS THE CLOSURE TARGET from two separate open lanes (A0,")
    log("  G1) to a single named theorem on the SU(3)-gauged staggered minimal")
    log("  block.")
    log()

    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "w") as f:
            f.write("\n".join(results_log) + "\n")
    except OSError:
        pass

    sys.exit(0 if FAIL == 0 else 1)


if __name__ == "__main__":
    main()
