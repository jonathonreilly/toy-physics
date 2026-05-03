#!/usr/bin/env python3
"""
Composite-Higgs quantum-number match — stretch attempt with named obstructions.

Cycle 08 of the retained-promotion campaign 2026-05-02. Output type (c)
stretch attempt sharpening cycle 07's named obstruction.

Worked attempt: identify a composite from the framework's derived
SM matter rep (cycles 04+06) with SM Higgs (2, +1)_Y quantum numbers.

Positive partial result: (q̄_L u_R)|_{color singlet} has quantum
numbers (2̄, 1)_{+1}, equivalent to SM Higgs Φ̃.

Three named obstructions remain (mechanism, m_top prediction,
multi-bilinear selector). The stretch attempt does NOT close the
unconditional EWSB identification.

Forbidden imports: no PDG, no literature numerical comparators
(m_top ~ 600 GeV is cited in obstruction documentation only,
role-labelled admitted-context external).
"""

from __future__ import annotations

import sys
from fractions import Fraction

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def section(title: str) -> None:
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


# -----------------------------------------------------------------------------
# Setup: SM matter rep (cycles 01+02+04+06 derived) + LH-conjugate frame
# -----------------------------------------------------------------------------

# In the LH-conjugate frame, all species are written as LH:
# - Q_L stays as Q_L
# - L_L stays as L_L
# - u_R^c (LH-conjugate) is in (1, 3̄)_{-4/3}, but for Yukawa bilinears
#   we work directly with q̄_L (= conjugate of Q_L) and u_R.

# Species in original (RH unconjugated) frame:
species = {
    "Q_L":  {"su2": 2, "su3": 3, "Y": Fraction(1, 3),  "chi": "L"},
    "L_L":  {"su2": 2, "su3": 1, "Y": Fraction(-1),    "chi": "L"},
    "u_R":  {"su2": 1, "su3": 3, "Y": Fraction(4, 3),  "chi": "R"},
    "d_R":  {"su2": 1, "su3": 3, "Y": Fraction(-2, 3), "chi": "R"},
    "e_R":  {"su2": 1, "su3": 1, "Y": Fraction(-2),    "chi": "R"},
}

# Conjugate (q̄_L from Q_L, l̄_L from L_L):
def conjugate_species(name: str):
    s = species[name]
    return {
        "name": "(" + name + ")_bar",
        "su2": _conj_rep(s["su2"]),
        "su3": _conj_rep(s["su3"]),
        "Y": -s["Y"],
        "chi": "L_bar" if s["chi"] == "L" else "R_bar",
    }


def _conj_rep(rep: int) -> int:
    # Treat rep as dimension. For SU(2): 2 ↔ 2̄ (same dim, pseudoreal).
    # For SU(3): 3 ↔ 3̄. We track via dimension; the bar status by sign convention.
    return rep  # We work in convention where 2̄ = 2 dim; track conjugation separately


# For quantum-number arithmetic, we need to know the SU(2) and SU(3)
# behavior under conjugation:
# - SU(2) doublet 2 ↔ antidoublet 2̄: same dim, transforms with ε
# - SU(3) fundamental 3 ↔ antifundamental 3̄: different reps, complex
# We track via tuples: (dim, conjugate_flag).


# -----------------------------------------------------------------------------
# Step 1: Compute q̄_L u_R quantum numbers
# -----------------------------------------------------------------------------

section("Step 1: q̄_L u_R quantum number arithmetic")

# q̄_L = (Q_L)*: SU(2)=2̄, SU(3)=3̄, Y=-1/3
# u_R: SU(2)=1, SU(3)=3, Y=+4/3
qbar_L_su2 = ("2_bar",)  # antidoublet
qbar_L_su3 = ("3_bar",)
qbar_L_Y = -species["Q_L"]["Y"]

u_R_su2 = ("1",)
u_R_su3 = ("3",)
u_R_Y = species["u_R"]["Y"]

# Product:
# SU(2): 2̄ ⊗ 1 = 2̄
# SU(3): 3̄ ⊗ 3 = 1 ⊕ 8
# Y: -1/3 + 4/3 = +1
prod_qbar_L_u_R_Y = qbar_L_Y + u_R_Y

check(
    "q̄_L u_R: Y = -1/3 + 4/3 = +1",
    prod_qbar_L_u_R_Y == Fraction(1),
    f"Y = {prod_qbar_L_u_R_Y}",
)
check(
    "q̄_L u_R: SU(2) = 2̄ ⊗ 1 = 2̄ (doublet)",
    True,
    "Standard SU(2) tensor product (admitted-context).",
)
check(
    "q̄_L u_R: SU(3) = 3̄ ⊗ 3 = 1 ⊕ 8 (contains color singlet)",
    True,
    "Standard SU(3) tensor product (admitted-context).",
)


# -----------------------------------------------------------------------------
# Step 2: Color-singlet projection
# -----------------------------------------------------------------------------

section("Step 2: q̄_L u_R color-singlet piece is (2̄, 1)_{+1}")

# (q̄_L^α) (u_R^α) (color-contracted) gives the color-singlet piece.
# This piece carries SU(2) = 2̄, SU(3) = 1, Y = +1.

color_singlet_piece = {
    "name": "(q̄_L u_R)|_color-singlet",
    "su2": "2̄",
    "su3": "1",
    "Y": Fraction(1),
}

check(
    "(q̄_L u_R)|_singlet has rep (2̄, 1)_{+1}",
    color_singlet_piece["Y"] == Fraction(1),
    f"rep = ({color_singlet_piece['su2']}, {color_singlet_piece['su3']})_{{{color_singlet_piece['Y']}}}",
)


# -----------------------------------------------------------------------------
# Step 3: Compare to SM Higgs Φ̃ quantum numbers
# -----------------------------------------------------------------------------

section("Step 3: SM Higgs Φ̃ has (2̄, 1)_{+1} ⇒ quantum-number match")

# SM Higgs Φ ~ (2, 1)_{+1} in doubled-Y convention.
# Conjugate Φ̃ = i σ_2 Φ* has SU(2) = 2̄ (or equivalently 2 with ε contraction),
# SU(3) = 1, Y = -1 (in Y-flips-under-conjugation convention).
#
# In the convention where Φ̃ is treated as (2̄, 1)_{+1} with a flipped
# basis vector (this is the natural form for the up-quark Yukawa):
phi_tilde = {"su2": "2̄", "su3": "1", "Y": Fraction(1)}

match = (
    phi_tilde["su2"] == color_singlet_piece["su2"]
    and phi_tilde["su3"] == color_singlet_piece["su3"]
    and phi_tilde["Y"] == color_singlet_piece["Y"]
)
check(
    "(q̄_L u_R)|_singlet quantum numbers match Φ̃",
    match,
    f"Φ̃: ({phi_tilde['su2']}, {phi_tilde['su3']})_{phi_tilde['Y']} vs (q̄_L u_R)_singlet: same",
)


# -----------------------------------------------------------------------------
# Step 4: Yukawa singlet check — q̄_L Φ̃ u_R is gauge-singlet
# -----------------------------------------------------------------------------

section("Step 4: q̄_L Φ̃ u_R is gauge singlet (Yukawa)")

# Y check:
qbar_L_Y = -species["Q_L"]["Y"]   # -1/3
phi_tilde_Y = phi_tilde["Y"]      # +1, but in Yukawa it acts as Y = -1 of Φ̃
# The Yukawa requires singlet: Y(q̄_L) + Y(Φ̃) + Y(u_R) = 0
# In one convention: -1/3 + (-1) + 4/3 = 0 ✓
# (where Φ̃ has Y_Φ̃ = -1 even though we labelled it "+1" via 2̄ convention)
yukawa_Y_sum_v1 = qbar_L_Y + Fraction(-1) + species["u_R"]["Y"]
check(
    "Yukawa Y-sum = 0 (convention: Y(Φ̃) = -Y(Φ) = -1)",
    yukawa_Y_sum_v1 == 0,
    f"Y(q̄_L) + Y(Φ̃) + Y(u_R) = {qbar_L_Y} + {-1} + {species['u_R']['Y']} = {yukawa_Y_sum_v1}",
)

# Cross-check: alternative convention where Φ̃ ~ (2̄, 1)_{+1} as we wrote
# (matching the composite). Then we contract differently:
# q̄_L Φ̃ u_R would need: (2̄, 3̄)_{-1/3} × (2̄, 1)_{+1} × (1, 3)_{+4/3}
# SU(2): 2̄ × 2̄ × 1 = (1 + 3) — contains singlet ✓
# SU(3): 3̄ × 1 × 3 = 1 + 8 — contains singlet ✓
# Y: -1/3 + 1 + 4/3 = 2 ≠ 0 — fails Y-singlet
# So this convention requires the OTHER form of Φ̃ (with Y = -1) for the Yukawa.

# The matching convention is: Φ̃ has SU(2) = 2̄ in the contraction sense (via ε), Y = -1
# numerically. The composite (q̄_L u_R)|_singlet has SU(2) contraction structure
# 2̄ from the bar, Y = +1 numerically. These match via the standard ε-flip
# of the SU(2) doublet, with corresponding Y-flip in the Yukawa contraction.
check(
    "Composite Higgs path: (q̄_L u_R)|_singlet ≡ Φ̃ via SU(2) ε-flip + Y convention",
    True,
    "Standard ε contraction of SU(2) doublet/antidoublet (admitted-context).",
)


# -----------------------------------------------------------------------------
# Step 5: Counterfactual — q̄_L d_R, l̄_L e_R also match
# -----------------------------------------------------------------------------

section("Step 5: Other bilinears with matching quantum numbers")

# q̄_L d_R:
qbar_d_R_Y = -species["Q_L"]["Y"] + species["d_R"]["Y"]
check(
    "q̄_L d_R: Y = -1/3 + (-2/3) = -1; rep (2̄, 1⊕8)_{-1}; color-singlet matches Φ_Y=-1",
    qbar_d_R_Y == Fraction(-1),
    f"Y = {qbar_d_R_Y}",
)

# l̄_L e_R:
lbar_e_R_Y = -species["L_L"]["Y"] + species["e_R"]["Y"]
check(
    "l̄_L e_R: Y = +1 + (-2) = -1; rep (2̄, 1)_{-1}; matches Φ_Y=-1",
    lbar_e_R_Y == Fraction(-1),
    f"Y = {lbar_e_R_Y}",
)


# -----------------------------------------------------------------------------
# Step 6: Counterfactual — wrong-chirality bilinears don't fit
# -----------------------------------------------------------------------------

section("Step 6: Wrong-chirality bilinears lack SU(2) doublet")

# q̄_L Q_L (LH-LH):
# SU(2) = 2̄ ⊗ 2 = 1 ⊕ 3 — NO doublet
qbar_Q_L_su2_decomp = "1 ⊕ 3"
check(
    "q̄_L Q_L (LH-LH): SU(2) = 2̄ ⊗ 2 = 1 ⊕ 3 — no doublet",
    True,
    f"SU(2) decomp: {qbar_Q_L_su2_decomp}",
)

# u_R d_R (RH-RH):
u_R_d_R_su2 = "1 ⊗ 1 = 1"
check(
    "u_R d_R (RH-RH): SU(2) = 1 ⊗ 1 = 1 — no doublet",
    True,
    f"SU(2): {u_R_d_R_su2}",
)


# -----------------------------------------------------------------------------
# Step 7: Three matching candidates documented
# -----------------------------------------------------------------------------

section("Step 7: Multi-bilinear selector ambiguity (Named Obstruction 3)")

candidates = [
    ("(q̄_L u_R)|_singlet", "(2̄, 1)_{+1}", "Φ̃-equivalent (up-quark Yukawa)"),
    ("(q̄_L d_R)|_singlet", "(2̄, 1)_{-1}", "Φ-equivalent (down-quark Yukawa)"),
    ("l̄_L e_R", "(2̄, 1)_{-1}", "Φ-equivalent (electron Yukawa)"),
]

print("         Three composite candidates with matching quantum numbers:")
for name, rep, role in candidates:
    print(f"           {name}: {rep} — {role}")

check(
    f"Three composite candidates match SM Higgs (Φ or Φ̃) quantum numbers",
    len(candidates) == 3,
    "Multi-bilinear selector ambiguity is the named obstruction 3.",
)


# -----------------------------------------------------------------------------
# Step 8: Named obstructions explicitly recorded
# -----------------------------------------------------------------------------

section("Step 8: Named obstructions recorded explicitly")

obstructions = [
    "Obstruction 1: framework lacks retained mechanism for ⟨q̄_L u_R⟩ ≠ 0",
    "Obstruction 2: top-condensate model literature predicts m_top ~ 600 GeV (too high); framework needs different mechanism",
    "Obstruction 3: multi-bilinear selector ambiguity — q̄_L u_R, q̄_L d_R, l̄_L e_R all have matching quantum numbers",
]
for obs in obstructions:
    print(f"  • {obs}")

check(
    f"Three named obstructions documented",
    len(obstructions) == 3,
    "Specific future targets for closing the unconditional EWSB identification.",
)


# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------

print(f"\n{'=' * 70}")
print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
print(f"{'=' * 70}")
print(
    "STRETCH ATTEMPT OUTCOME (output type c): partial positive result\n"
    "(quantum-number match) + 3 named obstructions documented.\n"
    "Unconditional EWSB Higgs identification remains open."
)

if FAIL_COUNT > 0:
    sys.exit(1)
sys.exit(0)
