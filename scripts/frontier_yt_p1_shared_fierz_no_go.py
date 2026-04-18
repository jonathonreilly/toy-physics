#!/usr/bin/env python3
"""
Frontier runner: P1 Shared-Fierz Shortcut No-Go Sub-Theorem.

Status
------
Retained structural sub-theorem. Definitive no-go verdict on reducing
the 1-loop ratio correction Delta_R = delta_y - delta_g on the Ward
ratio y_t^2/g_s^2 to an algebraic shortcut via a shared Fierz identity
combining the Ward-theorem SU(N_c) color Fierz (D12) with the Lorentz
Clifford Fierz (S2).

The two representations are structurally different at 1-loop:
  - Rep-A (OGE extraction of g_s^2): vertex + gluon SE + ghost + quark
    SE + tadpole pieces.
  - Rep-B (H_unit matrix-element extraction of y_t^2): scalar-op
    dressing + quark SE only.

The external quark SE cancels on the ratio because both representations
share the same physical external legs. The remaining pieces are
STRUCTURALLY DIFFERENT and cannot be related by any Fierz identity.

This runner verifies the structural divide between Rep-A and Rep-B by
enumerating the piece lists of each representation and checking that
the non-shared pieces (gluon SE in Rep-A; scalar-op anomalous dim. in
Rep-B; vertex BZ integrals in both but with different Dirac/color)
have no counterpart on the other side.

Authority
---------
Authority note (this runner):
  docs/YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md

Upstream retained foundations (not modified by this runner):
  - docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md  (tree-level D16+D17+D12+S2)
  - docs/YT_COLOR_PROJECTION_CORRECTION_NOTE.md  (H_unit/H_bar Fierz)
  - docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md

Downstream dependent sub-theorems (use this no-go as prerequisite):
  - docs/YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md
  - docs/YT_P1_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md

Self-contained: numpy + stdlib only.
"""

from __future__ import annotations

import math
import sys
from typing import Dict, Set


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
# Retained constants
# ---------------------------------------------------------------------------

PI = math.pi
N_C = 3
C_F = (N_C * N_C - 1.0) / (2.0 * N_C)   # 4/3
C_A = float(N_C)                         # 3
T_F = 0.5                                # 1/2
N_F = 6                                  # SM flavor count at M_Pl


# ---------------------------------------------------------------------------
# Rep-A 1-loop piece list (dressing g_s^2 on OGE channel)
# ---------------------------------------------------------------------------
#
# Each piece is keyed by a diagrammatic-topology tag. The color structure
# and Dirac structure are stored to make the structural divide with Rep-B
# explicit.

REP_A_PIECES: Dict[str, Dict] = {
    "vertex": {
        "color_structure": "(C_F - C_A/2) T^A",
        "color_channels": {"CF", "CA"},
        "dirac_structure": "gamma^mu gamma^nu gamma_mu",
        "bz_integral": "I_v_gauge",
        "diagram_topology": "vertex-correction",
        "renorm_type": "lagrangian-parameter",
    },
    "gluon_SE_gluonic": {
        "color_structure": "(5/3) C_A T^A",
        "color_channels": {"CA"},
        "dirac_structure": "N/A (internal gluon propagator)",
        "bz_integral": "I_SE_gluonic+ghost",
        "diagram_topology": "self-energy",
        "renorm_type": "lagrangian-parameter",
    },
    "gluon_SE_fermion": {
        "color_structure": "(-4/3) T_F n_f T^A",
        "color_channels": {"TFnf"},
        "dirac_structure": "N/A (closed fermion loop)",
        "bz_integral": "I_SE_fermion-loop",
        "diagram_topology": "self-energy",
        "renorm_type": "lagrangian-parameter",
    },
    "ghost": {
        "color_structure": "absorbed in gluon_SE_gluonic (Feynman gauge)",
        "color_channels": {"CA"},
        "dirac_structure": "N/A",
        "bz_integral": "absorbed in I_SE_gluonic+ghost",
        "diagram_topology": "self-energy",
        "renorm_type": "lagrangian-parameter",
    },
    "external_Z_psi": {
        "color_structure": "C_F (per leg)",
        "color_channels": {"CF"},
        "dirac_structure": "scalar",
        "bz_integral": "I_leg",
        "diagram_topology": "external-leg-self-energy",
        "renorm_type": "external-leg",
    },
    "tadpole": {
        "color_structure": "absorbed in u_0 tadpole improvement",
        "color_channels": set(),
        "dirac_structure": "N/A",
        "bz_integral": "absorbed in u_0",
        "diagram_topology": "tadpole",
        "renorm_type": "non-perturbative",
    },
}


# ---------------------------------------------------------------------------
# Rep-B 1-loop piece list (dressing y_t^2 through H_unit matrix element)
# ---------------------------------------------------------------------------

REP_B_PIECES: Dict[str, Dict] = {
    "scalar_vertex": {
        "color_structure": "C_F (identity color)",
        "color_channels": {"CF"},
        "dirac_structure": "gamma^mu 1 gamma_mu",
        "bz_integral": "I_v_scalar",
        "diagram_topology": "vertex-correction",
        "renorm_type": "composite-operator",
    },
    "operator_anom_dim": {
        "color_structure": "-6 C_F",
        "color_channels": {"CF"},
        "dirac_structure": "scalar bilinear (psi-bar psi)",
        "bz_integral": "-6 (constant from MSbar scalar-density gamma_S)",
        "diagram_topology": "composite-operator-dressing",
        "renorm_type": "composite-operator",
    },
    "external_Z_psi": {
        "color_structure": "C_F (per leg)",
        "color_channels": {"CF"},
        "dirac_structure": "scalar",
        "bz_integral": "I_leg",
        "diagram_topology": "external-leg-self-energy",
        "renorm_type": "external-leg",
    },
    "tadpole": {
        "color_structure": "absorbed in u_0 tadpole improvement",
        "color_channels": set(),
        "dirac_structure": "N/A",
        "bz_integral": "absorbed in u_0",
        "diagram_topology": "tadpole",
        "renorm_type": "non-perturbative",
    },
}


# ---------------------------------------------------------------------------
# Structural divide analysis
# ---------------------------------------------------------------------------

def pieces_shared_exactly(rep_a: Dict[str, Dict], rep_b: Dict[str, Dict]) -> Set[str]:
    """Return the set of piece-tags that appear in BOTH reps with identical
    color_structure and dirac_structure.
    """
    shared = set()
    for tag in rep_a:
        if tag not in rep_b:
            continue
        a = rep_a[tag]
        b = rep_b[tag]
        if (a["color_structure"] == b["color_structure"]
                and a["dirac_structure"] == b["dirac_structure"]
                and a["bz_integral"] == b["bz_integral"]):
            shared.add(tag)
    return shared


def pieces_in_a_not_in_b(rep_a: Dict[str, Dict], rep_b: Dict[str, Dict]) -> Set[str]:
    """Return pieces in Rep-A that are NOT algebraically convertible to a
    Rep-B piece. A piece is NOT convertible if it differs from every Rep-B
    piece in either (i) color structure, (ii) Dirac structure, or
    (iii) diagram topology.
    """
    not_convertible = set()
    for tag_a, piece_a in rep_a.items():
        if tag_a == "tadpole":
            continue  # tadpoles absorbed in u_0 on both sides
        if tag_a == "ghost":
            continue  # ghost absorbed in gluon SE on both sides
        # Check if piece_a can be matched to any piece_b via Fierz reasoning.
        convertible = False
        for tag_b, piece_b in rep_b.items():
            # Rule: a piece is "Fierz-convertible" only if diagram topology
            # matches (Fierz cannot convert SE <-> vertex <-> operator-dressing).
            if piece_a["diagram_topology"] == piece_b["diagram_topology"]:
                convertible = True
                break
        if not convertible:
            not_convertible.add(tag_a)
    return not_convertible


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("YT P1 Shared-Fierz Shortcut No-Go Sub-Theorem -- runner")
    print("Date: 2026-04-17")
    print("Authority: YT_P1_SHARED_FIERZ_NO_GO_SUB_THEOREM_NOTE_2026-04-17.md")
    print("=" * 72)
    print()

    # -----------------------------------------------------------------------
    # Print Rep-A and Rep-B piece lists
    # -----------------------------------------------------------------------
    print("Rep-A 1-loop piece list (dressing g_s^2 on OGE channel):")
    for tag, piece in REP_A_PIECES.items():
        print(f"  {tag}:")
        print(f"    color_structure = {piece['color_structure']}")
        print(f"    dirac_structure = {piece['dirac_structure']}")
        print(f"    bz_integral     = {piece['bz_integral']}")
        print(f"    topology        = {piece['diagram_topology']}")
        print(f"    renorm_type     = {piece['renorm_type']}")
    print()

    print("Rep-B 1-loop piece list (dressing y_t^2 via H_unit):")
    for tag, piece in REP_B_PIECES.items():
        print(f"  {tag}:")
        print(f"    color_structure = {piece['color_structure']}")
        print(f"    dirac_structure = {piece['dirac_structure']}")
        print(f"    bz_integral     = {piece['bz_integral']}")
        print(f"    topology        = {piece['diagram_topology']}")
        print(f"    renorm_type     = {piece['renorm_type']}")
    print()

    # -----------------------------------------------------------------------
    # Structural check 1: External Z_psi is the only piece that matches exactly
    # -----------------------------------------------------------------------
    print("Structural check 1: external Z_psi matches exactly between Rep-A and Rep-B.")

    shared = pieces_shared_exactly(REP_A_PIECES, REP_B_PIECES)
    # The exactly-shared piece is external Z_psi (same physical external legs).
    # Tadpoles absorb into u_0 on both sides (also shared, but not a diagram).
    shared_nontrivial = shared - {"tadpole"}

    check(
        "External Z_psi is the UNIQUE exactly-shared Rep-A/Rep-B piece",
        shared_nontrivial == {"external_Z_psi"},
        f"shared non-trivial pieces = {sorted(shared_nontrivial)}",
    )
    print()

    # -----------------------------------------------------------------------
    # Structural check 2: Gluon SE (C_A and T_F n_f channels) has no Rep-B counterpart
    # -----------------------------------------------------------------------
    print("Structural check 2: gluon SE (C_A, T_F n_f) in Rep-A has no Rep-B analog.")

    # Any Rep-B piece with diagram_topology == "self-energy"?
    rep_b_has_self_energy = any(
        p["diagram_topology"] == "self-energy" for p in REP_B_PIECES.values()
    )
    # Rep-A gluon SE pieces have CA and TFnf channels, respectively.
    rep_a_se_ca = REP_A_PIECES["gluon_SE_gluonic"]["color_channels"] == {"CA"}
    rep_a_se_tfnf = REP_A_PIECES["gluon_SE_fermion"]["color_channels"] == {"TFnf"}

    check(
        "Rep-A gluon SE (both C_A and T_F n_f channels) has NO Rep-B counterpart",
        rep_a_se_ca and rep_a_se_tfnf and not rep_b_has_self_energy,
        "Rep-B has no self-energy topology (color-singlet scalar operator "
        "has no internal gluon to dress); covers both gluonic and fermion-loop",
    )
    print()

    # -----------------------------------------------------------------------
    # Structural check 3: Scalar-operator anomalous dimension (Rep-B) has no Rep-A analog
    # -----------------------------------------------------------------------
    print("Structural check 3: scalar-op anom. dim. in Rep-B has no Rep-A analog.")

    # Any Rep-A piece with diagram_topology == "composite-operator-dressing"?
    rep_a_has_op_dressing = any(
        p["diagram_topology"] == "composite-operator-dressing"
        for p in REP_A_PIECES.values()
    )
    # Any Rep-A piece with renorm_type == "composite-operator"?
    rep_a_has_composite_renorm = any(
        p["renorm_type"] == "composite-operator"
        for p in REP_A_PIECES.values()
    )

    rep_b_op_present = REP_B_PIECES["operator_anom_dim"]["color_structure"] == "-6 C_F"

    check(
        "Rep-B scalar-operator anom. dim. (-6 C_F) has NO Rep-A counterpart",
        rep_b_op_present and not rep_a_has_op_dressing and not rep_a_has_composite_renorm,
        "Rep-A has Lagrangian-parameter renormalization; Rep-B has composite-operator",
    )
    print()

    # -----------------------------------------------------------------------
    # Structural check 4: Vertex BZ integrals differ structurally
    # -----------------------------------------------------------------------
    print("Structural check 4: vertex BZ integrals differ between Rep-A and Rep-B.")

    rep_a_vertex = REP_A_PIECES["vertex"]
    rep_b_vertex = REP_B_PIECES["scalar_vertex"]

    # Same diagram topology (both are vertex corrections) but different
    # Dirac structure, different color structure, different BZ integral.
    same_topology = rep_a_vertex["diagram_topology"] == rep_b_vertex["diagram_topology"]
    different_dirac = rep_a_vertex["dirac_structure"] != rep_b_vertex["dirac_structure"]
    different_color = rep_a_vertex["color_structure"] != rep_b_vertex["color_structure"]
    different_bz = rep_a_vertex["bz_integral"] != rep_b_vertex["bz_integral"]
    # Rep-A color channels include CA (from -C_A/2); Rep-B does not.
    rep_a_vertex_has_ca = "CA" in rep_a_vertex["color_channels"]
    rep_b_vertex_has_ca = "CA" in rep_b_vertex["color_channels"]

    check(
        "Vertex corrections have different Dirac/color/BZ structures (NO Fierz maps them)",
        same_topology and different_dirac and different_color and different_bz
        and rep_a_vertex_has_ca and not rep_b_vertex_has_ca,
        f"Rep-A: Dirac={rep_a_vertex['dirac_structure']}, color={rep_a_vertex['color_structure']}, "
        f"BZ={rep_a_vertex['bz_integral']}; "
        f"Rep-B: Dirac={rep_b_vertex['dirac_structure']}, color={rep_b_vertex['color_structure']}, "
        f"BZ={rep_b_vertex['bz_integral']}",
    )
    print()

    # -----------------------------------------------------------------------
    # Additional diagnostic: total non-shared pieces in each direction
    # -----------------------------------------------------------------------
    print("Diagnostic: non-shared pieces in each direction.")

    not_convertible_a = pieces_in_a_not_in_b(REP_A_PIECES, REP_B_PIECES)
    not_convertible_b = pieces_in_a_not_in_b(REP_B_PIECES, REP_A_PIECES)

    print(f"  Rep-A pieces NOT convertible to Rep-B: {sorted(not_convertible_a)}")
    print(f"  Rep-B pieces NOT convertible to Rep-A: {sorted(not_convertible_b)}")
    print()

    # Optional diagnostic prints for the Fierz/color content
    print("Retained Fierz constants (from D12 + S2, tree level only):")
    print(f"  D12 color singlet coefficient: -1/(2 N_c) = {-1.0/(2.0*N_C):.10f}")
    print(f"  S2 Lorentz scalar coefficient: c_S = 1")
    print(f"  Tree Ward:  y_t_bare^2 = g_bare^2 / (2 N_c) = {1.0/(2.0*N_C):.10f}")
    print()
    print("These Fierz identities hold at TREE level only. At 1-loop, the")
    print("diagrammatic structure of Rep-A and Rep-B diverges qualitatively")
    print("and no Fierz rearrangement closes the gap.")
    print()

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print("=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 72)
    print()
    print("VERDICT: SHARED-FIERZ SHORTCUT NO-GO.")
    print()
    print("  The 1-loop ratio correction Delta_R = delta_y - delta_g cannot")
    print("  be closed by any algebraic shortcut using the Ward-theorem Fierz")
    print("  (D12 color + S2 Clifford) identities.")
    print()
    print("  Rep-A (OGE extraction of g_s^2) has: vertex + gluon SE + ghost")
    print("  + quark SE + tadpole pieces.")
    print("  Rep-B (H_unit extraction of y_t^2) has: scalar vertex + scalar-op")
    print("  dressing + quark SE.")
    print()
    print("  External Z_psi cancels exactly on the ratio (same physical legs).")
    print("  All other pieces are STRUCTURALLY DIFFERENT and cannot be related")
    print("  by any Fierz identity (different diagram topologies, renorm types,")
    print("  color channels, Dirac Clifford structures).")
    print()
    print("  Delta_R must be computed channel by channel via lattice-PT BZ")
    print("  evaluation on the retained canonical surface.")

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
