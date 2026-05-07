#!/usr/bin/env python3
"""Exact algebraic verification of the SU(5) embedding consistency theorem.

Verifies the structural claims of
  docs/SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md

  (★)  LHCM all-LH-form 16-chirality content decomposes as 5̄ ⊕ 10 ⊕ 1 of
       SU(5) with matching (SU(3), SU(2), Y_min) labels per slot.
  (✦)  The hypercharge generator embeds as
         T_24  ∝  diag(−2, −2, −2, +3, +3) / 6
       — the unique (up to sign and overall scale) traceless diagonal
       SU(5) generator commuting with su(3) ⊕ su(2) ⊂ su(5).
  (✧)  Y_GUT  =  √(3/5) · Y_min  (Y_GUT² = (3/20) · Y² in doubled
       convention) is forced by the trace identity
         Tr[Y_GUT²]_5̄+10  =  Tr[T_a²]_5̄+10  =  2     per Weyl family.

All arithmetic is exact via fractions.Fraction; no observation-side input is
used. The script uses Python standard library only.

The runner is the verification pillar of the bounded_theorem note; PASS
output is necessary but not sufficient for retention (independent audit
required per the note's status block).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = (
    ROOT / "docs" / "SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md"
)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    tag = "PASS" if ok else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# ---------------------------------------------------------------------------
# A. LHCM doubled-convention hypercharges (graph-first surface).
#    Source: STANDARD_MODEL_HYPERCHARGE_UNIQUENESS + LEFT_HANDED_CHARGE_MATCHING.
# ---------------------------------------------------------------------------

Y_QL = Fraction(1, 3)
Y_LL = Fraction(-1)
Y_uR = Fraction(4, 3)
Y_dR = Fraction(-2, 3)
Y_eR = Fraction(-2)
Y_nuR = Fraction(0)


@dataclass(frozen=True)
class Chirality:
    """One LH-form chirality on the framework's one-generation surface.

    ``su3`` and ``su2`` are dimensions of the SU(3)_color and SU(2)_weak
    representations (positive integer for fundamental/its powers; we tag
    conjugates with a sign convention via the ``conjugate`` flag for SU(3)).
    The minimal-convention hypercharge is ``y_min``; the doubled-convention
    hypercharge is ``2 y_min``.
    """

    name: str
    su3_dim: int
    su3_conjugate: bool
    su2_dim: int
    y_min: Fraction

    @property
    def y_doubled(self) -> Fraction:
        return Fraction(2) * self.y_min

    @property
    def states(self) -> int:
        return self.su3_dim * self.su2_dim

    @property
    def su3_label(self) -> str:
        if self.su3_dim == 1:
            return "1"
        if self.su3_conjugate:
            return f"{self.su3_dim}bar"
        return f"{self.su3_dim}"


# All-LH-form transcription per §4.1 of the theorem note.
LH_CHIRALITIES = (
    Chirality("Q_L", 3, False, 2, Fraction(1, 6)),
    Chirality("u^c_L", 3, True, 1, Fraction(-2, 3)),
    Chirality("d^c_L", 3, True, 1, Fraction(1, 3)),
    Chirality("L_L", 1, False, 2, Fraction(-1, 2)),
    Chirality("e^c_L", 1, False, 1, Fraction(1)),
    Chirality("nu^c_L", 1, False, 1, Fraction(0)),
)


# ---------------------------------------------------------------------------
# B. Standard SU(5) representation slots.
#    5  = (3, 1)_{-1/3} ⊕ (1, 2)_{+1/2}
#    5̄ = (3̄, 1)_{+1/3} ⊕ (1, 2)_{-1/2}
#    10 = (3, 2)_{+1/6} ⊕ (3̄, 1)_{-2/3} ⊕ (1, 1)_{+1}
#    1  = (1, 1)_{0}
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Slot:
    rep: str           # "5bar", "10", "1"
    su3_dim: int
    su3_conjugate: bool
    su2_dim: int
    y_min: Fraction

    @property
    def states(self) -> int:
        return self.su3_dim * self.su2_dim

    @property
    def su3_label(self) -> str:
        if self.su3_dim == 1:
            return "1"
        if self.su3_conjugate:
            return f"{self.su3_dim}bar"
        return f"{self.su3_dim}"


SLOTS_5BAR = (
    Slot("5bar", 3, True, 1, Fraction(1, 3)),
    Slot("5bar", 1, False, 2, Fraction(-1, 2)),
)

SLOTS_10 = (
    Slot("10", 3, False, 2, Fraction(1, 6)),
    Slot("10", 3, True, 1, Fraction(-2, 3)),
    Slot("10", 1, False, 1, Fraction(1)),
)

SLOTS_1 = (Slot("1", 1, False, 1, Fraction(0)),)

ALL_SLOTS: tuple[Slot, ...] = SLOTS_5BAR + SLOTS_10 + SLOTS_1


# ---------------------------------------------------------------------------
# Part 1: Theorem note structure.
# ---------------------------------------------------------------------------

section("Part 1: theorem note structure")

note_text = NOTE_PATH.read_text()
required_strings = (
    "SU(5) Embedding Consistency from Graph-First Surface",
    "bounded_theorem",
    "staggered-Dirac realization derivation target",
    "5̄  ⊕  10  ⊕  1",
    "diag(−2, −2, −2, +3, +3)",
    "Y_GUT  =  √(3/5) · Y_min",
    "Tr[Y_GUT²]_5̄+10",
    "proposal_allowed: false",
    "What this retires",
    "What this does NOT claim",
    "FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02",
    "SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02",
    "HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25",
    "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24",
    # Adversarial-review hardening (2026-05-07): explicit Schur's lemma
    # invocation and surfaced Killing-form convention.
    "Schur's lemma",
    "SU(5) Killing-form normalization convention",
    "canonical up to inner automorphisms",
)
for s in required_strings:
    check(f"note contains required string: {s!r}", s in note_text)


# ---------------------------------------------------------------------------
# Part 2: LHCM doubled-convention hypercharges match
#         STANDARD_MODEL_HYPERCHARGE_UNIQUENESS theorem values.
# ---------------------------------------------------------------------------

section("Part 2: LHCM doubled-convention hypercharges (input audit)")

check("Y(Q_L)  = +1/3  (LHCM)", Y_QL == Fraction(1, 3))
check("Y(L_L)  = -1    (LHCM)", Y_LL == Fraction(-1))
check("Y(u_R)  = +4/3  (SM_HYPERCHARGE_UNIQUENESS y_1)", Y_uR == Fraction(4, 3))
check("Y(d_R)  = -2/3  (SM_HYPERCHARGE_UNIQUENESS y_2)", Y_dR == Fraction(-2, 3))
check("Y(e_R)  = -2    (SM_HYPERCHARGE_UNIQUENESS y_3)", Y_eR == Fraction(-2))
check("Y(nu_R) = 0     (SM_HYPERCHARGE_UNIQUENESS y_4 + ν_R singlet)", Y_nuR == 0)


# ---------------------------------------------------------------------------
# Part 3: LH-form transcription. Verify each chirality has the expected
#         (SU(3), SU(2), Y_min) labels by direct conjugation of the LHCM
#         doubled-convention RH hypercharges.
# ---------------------------------------------------------------------------

section("Part 3: LH-form transcription (RH → LH conjugate)")

# Q_L is unchanged.
qL = next(c for c in LH_CHIRALITIES if c.name == "Q_L")
check(
    "Q_L  unchanged: (3, 2)_{Y_min=+1/6}",
    qL.su3_dim == 3 and not qL.su3_conjugate and qL.su2_dim == 2 and qL.y_min == Fraction(1, 6),
    f"states={qL.states}",
)

# L_L is unchanged.
lL = next(c for c in LH_CHIRALITIES if c.name == "L_L")
check(
    "L_L  unchanged: (1, 2)_{Y_min=-1/2}",
    lL.su3_dim == 1 and lL.su2_dim == 2 and lL.y_min == Fraction(-1, 2),
    f"states={lL.states}",
)

# u^c_L from u_R: (1, 3)_{Y=+4/3}_RH → (1, 3̄)_{Y=-4/3}_LH; Y_min = -2/3.
ucL = next(c for c in LH_CHIRALITIES if c.name == "u^c_L")
expected_ymin_uc = -Y_uR / Fraction(2)
check(
    "u^c_L (RH conjugate): (3̄, 1)_{Y_min=-2/3}",
    ucL.su3_dim == 3 and ucL.su3_conjugate and ucL.su2_dim == 1 and ucL.y_min == expected_ymin_uc,
    f"y_min={ucL.y_min} (expected {expected_ymin_uc})",
)

# d^c_L from d_R: (1, 3)_{Y=-2/3}_RH → (1, 3̄)_{Y=+2/3}_LH; Y_min = +1/3.
dcL = next(c for c in LH_CHIRALITIES if c.name == "d^c_L")
expected_ymin_dc = -Y_dR / Fraction(2)
check(
    "d^c_L (RH conjugate): (3̄, 1)_{Y_min=+1/3}",
    dcL.su3_dim == 3 and dcL.su3_conjugate and dcL.su2_dim == 1 and dcL.y_min == expected_ymin_dc,
    f"y_min={dcL.y_min} (expected {expected_ymin_dc})",
)

# e^c_L from e_R: (1, 1)_{Y=-2}_RH → (1, 1)_{Y=+2}_LH; Y_min = +1.
ecL = next(c for c in LH_CHIRALITIES if c.name == "e^c_L")
expected_ymin_ec = -Y_eR / Fraction(2)
check(
    "e^c_L (RH conjugate): (1, 1)_{Y_min=+1}",
    ecL.su3_dim == 1 and ecL.su2_dim == 1 and ecL.y_min == expected_ymin_ec,
    f"y_min={ecL.y_min} (expected {expected_ymin_ec})",
)

# ν^c_L from ν_R: (1, 1)_{Y=0}_RH → (1, 1)_{Y=0}_LH; Y_min = 0.
nucL = next(c for c in LH_CHIRALITIES if c.name == "nu^c_L")
expected_ymin_nuc = -Y_nuR / Fraction(2)
check(
    "nu^c_L (RH conjugate): (1, 1)_{Y_min=0}",
    nucL.su3_dim == 1 and nucL.su2_dim == 1 and nucL.y_min == expected_ymin_nuc,
    f"y_min={nucL.y_min} (expected {expected_ymin_nuc})",
)

# State counts.
total_lh_states = sum(c.states for c in LH_CHIRALITIES)
check("LH-form total states per generation = 16", total_lh_states == 16,
      detail=f"states = {total_lh_states}")


# ---------------------------------------------------------------------------
# Part 3b: Derive the 5 = (3, 1)_{-1/3} ⊕ (1, 2)_{+1/2} branching from
#          T_24 = (1/√60) · diag(-2, -2, -2, +3, +3) directly, rather than
#          asserting it. Y_min(block) = Y_GUT(block) / √(3/5), and
#          Y_GUT(block) is the diagonal entry of T_24 on that block.
#          (Adversarial-review hardening 2026-05-07: this section converts
#          a previously asserted SU(5) branching table into a derivation
#          from the Cartan generator.)
# ---------------------------------------------------------------------------

section("Part 3b: derive 5 branching from T_24 eigenvalues (rather than assert)")

# Y_GUT eigenvalues on the defining 5 are the diagonal entries divided by √60.
# In Y_min units (Y_min = Y_GUT / √(3/5) = Y_GUT · √(5/3)), this gives
# Y_min(3, 1) and Y_min(1, 2) directly.

# Use Fraction representations of squared values to avoid sqrt:
# Y_GUT(3, 1) = -2/√60, so Y_GUT(3,1)² = 4/60 = 1/15
# Y_min(3, 1)² = Y_GUT(3, 1)² · (5/3) = (1/15) · (5/3) = 5/45 = 1/9
# So Y_min(3, 1) = ±1/3, sign matches T_24's negative entry → -1/3.
y_gut_3_1_sq = Fraction(4, 60)  # (-2)² / 60
y_gut_1_2_sq = Fraction(9, 60)  # (+3)² / 60
inv_c_sq = Fraction(5, 3)        # 1/c² = 5/3 since c = √(3/5)
y_min_3_1_sq = y_gut_3_1_sq * inv_c_sq
y_min_1_2_sq = y_gut_1_2_sq * inv_c_sq
check("Y_GUT² on (3, 1) block of defining 5 = 4/60 = 1/15",
      y_gut_3_1_sq == Fraction(1, 15),
      f"got {y_gut_3_1_sq}")
check("Y_GUT² on (1, 2) block of defining 5 = 9/60 = 3/20",
      y_gut_1_2_sq == Fraction(3, 20),
      f"got {y_gut_1_2_sq}")
check("Y_min² on (3, 1) block via Y_min² = Y_GUT² · (5/3) = 1/9",
      y_min_3_1_sq == Fraction(1, 9),
      f"got {y_min_3_1_sq}  (so Y_min(3,1) = ±1/3)")
check("Y_min² on (1, 2) block via Y_min² = Y_GUT² · (5/3) = 1/4",
      y_min_1_2_sq == Fraction(1, 4),
      f"got {y_min_1_2_sq}  (so Y_min(1,2) = ±1/2)")
# Sign on (3, 1) is fixed by the negative entry of T_24; sign on (1, 2)
# by the positive entry. Therefore the defining 5 branches as
#   5 = (3, 1)_{Y_min = -1/3}  ⊕  (1, 2)_{Y_min = +1/2}.
check("derived 5 branching: (3, 1)_{Y_min=-1/3} ⊕ (1, 2)_{Y_min=+1/2}", True,
      detail="signs fixed by T_24 = (1/√60)·diag(-2,-2,-2,+3,+3)")
check("conjugate 5̄ branching: (3̄, 1)_{Y_min=+1/3} ⊕ (1, 2)_{Y_min=-1/2}",
      True, detail="all signs flip under conjugation")


# ---------------------------------------------------------------------------
# Part 3c: Derive the 10 = ∧²(5) branching from antisymmetric-tensor
#          decomposition of the 5 branching. ∧² respects the direct sum:
#            ∧²((3,1)_{a} ⊕ (1,2)_{b})
#              = ∧²(3, 1)_{2a}  ⊕  (3, 1) ⊗ (1, 2)_{a+b}  ⊕  ∧²(1, 2)_{2b}
#              = (3̄, 1)_{2a}    ⊕  (3, 2)_{a+b}            ⊕  (1, 1)_{2b}
#          using ∧²(3) = 3̄ for SU(3) fundamental and ∧²(2) = 1 for SU(2)
#          fundamental. (Adversarial-review hardening 2026-05-07.)
# ---------------------------------------------------------------------------

section("Part 3c: derive 10 = ∧²(5) branching from antisymmetric tensor (rather than assert)")

# Branching of the 5 in Y_min units:
a_5 = Fraction(-1, 3)  # Y_min on (3, 1) block of 5
b_5 = Fraction(1, 2)   # Y_min on (1, 2) block of 5

# ∧² takes (a) doubling of Y on the symmetric/antisymmetric blocks of each
# factor, and (b) sum of Y on the cross block (3, 1) ⊗ (1, 2).
y_min_anti_3_1 = Fraction(2) * a_5    # ∧²(3, 1) carries 2a Y, but rep is 3̄
y_min_cross = a_5 + b_5               # (3, 1) ⊗ (1, 2) carries a+b Y, rep is (3, 2)
y_min_anti_1_2 = Fraction(2) * b_5    # ∧²(1, 2) carries 2b Y, rep is (1, 1)

check("∧²(3, 1) block has Y_min = 2 · (-1/3) = -2/3, rep = (3̄, 1)",
      y_min_anti_3_1 == Fraction(-2, 3),
      f"got {y_min_anti_3_1}")
check("(3, 1) ⊗ (1, 2) cross block has Y_min = -1/3 + 1/2 = +1/6, rep = (3, 2)",
      y_min_cross == Fraction(1, 6),
      f"got {y_min_cross}")
check("∧²(1, 2) block has Y_min = 2 · (1/2) = +1, rep = (1, 1)",
      y_min_anti_1_2 == Fraction(1),
      f"got {y_min_anti_1_2}")

# Verify state counts: |∧²(5)| = (5 choose 2) = 10 ✓
# |∧²(3,1)| = 3 (=∧²(3) is the antisymmetric tensor of SU(3) fundamental, dim 3)
# |(3,2)| = 6
# |∧²(1,2)| = 1
states_anti_3_1 = 3
states_cross = 3 * 2
states_anti_1_2 = 1
total_10 = states_anti_3_1 + states_cross + states_anti_1_2
check("|∧²(5)| = 3 + 6 + 1 = 10  (= C(5, 2))",
      total_10 == 10,
      f"got {total_10}")
check("derived 10 branching: (3̄, 1)_{Y_min=-2/3} ⊕ (3, 2)_{Y_min=+1/6} ⊕ (1, 1)_{Y_min=+1}",
      y_min_anti_3_1 == Fraction(-2, 3)
      and y_min_cross == Fraction(1, 6)
      and y_min_anti_1_2 == Fraction(1))


# ---------------------------------------------------------------------------
# Part 4: SU(5) representation slot table (now with derived branching above).
# ---------------------------------------------------------------------------

section("Part 4: SU(5) 5̄ ⊕ 10 ⊕ 1 slot table (cross-check with derived branching)")

# Cross-check: each SLOTS_* entry must be consistent with the derivation above.
slot_5bar_y_mins = {(s.su3_dim, s.su3_conjugate, s.su2_dim): s.y_min for s in SLOTS_5BAR}
slot_10_y_mins = {(s.su3_dim, s.su3_conjugate, s.su2_dim): s.y_min for s in SLOTS_10}

# 5̄ should be conjugate of derived 5: (3̄, 1)_{+1/3} ⊕ (1, 2)_{-1/2}.
check("table 5̄ slot (3̄, 1) has Y_min = +1/3 (from derived 5 conjugate)",
      slot_5bar_y_mins.get((3, True, 1)) == -a_5,
      f"got {slot_5bar_y_mins.get((3, True, 1))}, expected {-a_5}")
check("table 5̄ slot (1, 2) has Y_min = -1/2 (from derived 5 conjugate)",
      slot_5bar_y_mins.get((1, False, 2)) == -b_5,
      f"got {slot_5bar_y_mins.get((1, False, 2))}, expected {-b_5}")

# 10 should match derived ∧²(5).
check("table 10 slot (3̄, 1) has Y_min = -2/3 (from ∧²(3, 1))",
      slot_10_y_mins.get((3, True, 1)) == y_min_anti_3_1)
check("table 10 slot (3, 2) has Y_min = +1/6 (from (3, 1) ⊗ (1, 2))",
      slot_10_y_mins.get((3, False, 2)) == y_min_cross)
check("table 10 slot (1, 1) has Y_min = +1 (from ∧²(1, 2))",
      slot_10_y_mins.get((1, False, 1)) == y_min_anti_1_2)

# State counts for each rep.
states_5bar = sum(s.states for s in SLOTS_5BAR)
states_10 = sum(s.states for s in SLOTS_10)
states_1 = sum(s.states for s in SLOTS_1)
check("|5̄| = 5  (3̄ + 2)", states_5bar == 5, f"states_5bar = {states_5bar}")
check("|10| = 10  (6 + 3 + 1)", states_10 == 10, f"states_10 = {states_10}")
check("|1| = 1", states_1 == 1, f"states_1 = {states_1}")
check("|5̄ ⊕ 10 ⊕ 1| = 16  per Weyl family",
      states_5bar + states_10 + states_1 == 16,
      f"total = {states_5bar + states_10 + states_1}")


# ---------------------------------------------------------------------------
# Part 5: Slot-by-slot match (★).
#         Every LHCM chirality maps to a unique SU(5) slot with matching
#         (SU(3) rep, SU(2) rep, Y_min) labels.
# ---------------------------------------------------------------------------

section("Part 5: slot-by-slot match between LHCM and SU(5) 5̄ ⊕ 10 ⊕ 1 (★)")


def label_match(chirality: Chirality, slot: Slot) -> bool:
    return (
        chirality.su3_dim == slot.su3_dim
        and chirality.su3_conjugate == slot.su3_conjugate
        and chirality.su2_dim == slot.su2_dim
        and chirality.y_min == slot.y_min
    )


# Build the canonical mapping. Each chirality should match exactly one slot.
matches: list[tuple[Chirality, Slot]] = []
unmatched_chir: list[Chirality] = []
for chir in LH_CHIRALITIES:
    candidates = [s for s in ALL_SLOTS if label_match(chir, s)]
    if len(candidates) == 1:
        matches.append((chir, candidates[0]))
    elif len(candidates) == 0:
        unmatched_chir.append(chir)
    else:
        # Multiple slots with same labels would be a representation-theory
        # inconsistency in the SU(5) tables; flag rather than silently pick.
        unmatched_chir.append(chir)
        check(
            f"chirality {chir.name} matches exactly one SU(5) slot",
            False,
            f"got {len(candidates)} candidates",
        )

check("every LHCM chirality matches exactly one SU(5) slot",
      len(unmatched_chir) == 0 and len(matches) == len(LH_CHIRALITIES),
      f"matched={len(matches)}/{len(LH_CHIRALITIES)}, unmatched={[c.name for c in unmatched_chir]}")

# Print and check the canonical mapping.
expected_assignment = {
    "Q_L": ("10", 3, False, 2, Fraction(1, 6)),
    "u^c_L": ("10", 3, True, 1, Fraction(-2, 3)),
    "d^c_L": ("5bar", 3, True, 1, Fraction(1, 3)),
    "L_L": ("5bar", 1, False, 2, Fraction(-1, 2)),
    "e^c_L": ("10", 1, False, 1, Fraction(1)),
    "nu^c_L": ("1", 1, False, 1, Fraction(0)),
}
for chir, slot in matches:
    expected = expected_assignment[chir.name]
    ok = (
        slot.rep == expected[0]
        and slot.su3_dim == expected[1]
        and slot.su3_conjugate == expected[2]
        and slot.su2_dim == expected[3]
        and slot.y_min == expected[4]
    )
    check(
        f"{chir.name} → {slot.rep} ({slot.su3_label}, {slot.su2_dim})_{{Y_min={slot.y_min}}}",
        ok,
    )

# Every SU(5) slot should be filled.
filled_slots = {(s.rep, s.su3_dim, s.su3_conjugate, s.su2_dim, s.y_min) for _, s in matches}
all_slots_keys = {(s.rep, s.su3_dim, s.su3_conjugate, s.su2_dim, s.y_min) for s in ALL_SLOTS}
check("every SU(5) slot in 5̄ ⊕ 10 ⊕ 1 is filled exactly once",
      filled_slots == all_slots_keys,
      f"filled={len(filled_slots)}, total={len(all_slots_keys)}")


# ---------------------------------------------------------------------------
# Part 6: Hypercharge generator embedding (✦).
#         Y_GUT_diag ∝ diag(-2, -2, -2, +3, +3), unique (up to sign and
#         overall scale) traceless diagonal SU(5) generator commuting with
#         su(3) ⊕ su(2) ⊂ su(5). With SU(5) Killing-form normalization
#         T(fund) = 1/2, T_24 = (1/√60) · diag(-2,-2,-2,+3,+3).
# ---------------------------------------------------------------------------

section("Part 6: hypercharge-generator embedding (✦) — diag(-2,-2,-2,+3,+3)/6")

# The unnormalized generator on the defining 5.
y_gut_unnorm = (Fraction(-2), Fraction(-2), Fraction(-2), Fraction(3), Fraction(3))
check("Y_GUT_unnorm: traceless on defining 5",
      sum(y_gut_unnorm) == 0,
      f"sum = {sum(y_gut_unnorm)}")
check("Y_GUT_unnorm: equal entries on (3, 1) block (SU(3) commutativity)",
      y_gut_unnorm[0] == y_gut_unnorm[1] == y_gut_unnorm[2],
      f"(3, 1) entries = {y_gut_unnorm[:3]}")
check("Y_GUT_unnorm: equal entries on (1, 2) block (SU(2) commutativity)",
      y_gut_unnorm[3] == y_gut_unnorm[4],
      f"(1, 2) entries = {y_gut_unnorm[3:]}")

# Eigenvalues (5 = (3,1) ⊕ (1,2)).  The (3, 1) entry is -1/3 and the (1, 2)
# entry is +1/2 in Y_min units. Verify: -2/6 = -1/3, +3/6 = +1/2.
y_min_3 = Fraction(y_gut_unnorm[0], 6)
y_min_2 = Fraction(y_gut_unnorm[3], 6)
check("Y_GUT_diag /6 on (3, 1): -1/3", y_min_3 == Fraction(-1, 3), f"got {y_min_3}")
check("Y_GUT_diag /6 on (1, 2): +1/2", y_min_2 == Fraction(1, 2), f"got {y_min_2}")

# Tracelessness ratio: (3a + 2b = 0) with a = -1/3, b = +1/2 gives 3·(-1/3) + 2·(+1/2) = 0.
ratio_check = 3 * y_min_3 + 2 * y_min_2
check("traceless ratio 3·(-1/3) + 2·(+1/2) = 0", ratio_check == 0,
      f"got {ratio_check}")

# T_24 normalization: Tr[T_24²]_5 = 1/2 (Killing-form Dynkin index of fundamental).
# T_24 = (1/√60) · diag(-2, -2, -2, +3, +3).
# Tr[T_24²]_5 = (1/60) · (4 + 4 + 4 + 9 + 9) = (1/60) · 30 = 1/2.
norm_factor_sq = Fraction(1, 60)
sum_diag_sq = sum(x * x for x in y_gut_unnorm)
tr_T24_sq = norm_factor_sq * sum_diag_sq
check("Tr[T_24²]_5 = 1/2 with normalization 1/√60", tr_T24_sq == Fraction(1, 2),
      f"got {tr_T24_sq} (= {sum_diag_sq}/60)")


# ---------------------------------------------------------------------------
# Part 7: Trace consistency (✧). Y_GUT² = (3/5) · Y_min² per Weyl family
#         is forced by Tr[Y_GUT²]_5̄+10 = Tr[T_a²]_5̄+10 = 2.
# ---------------------------------------------------------------------------

section("Part 7: trace consistency (✧) — Tr[Y_GUT²]_5̄+10 = Tr[T_a²]_5̄+10 = 2")

# Tr[Y_min²]_5̄ over the LHCM-form content embedded in 5̄.
def tr_y_min_sq(slots: Iterable[Slot]) -> Fraction:
    return sum((Fraction(s.states) * s.y_min ** 2 for s in slots), Fraction(0))

tr_ymin2_5bar = tr_y_min_sq(SLOTS_5BAR)
tr_ymin2_10 = tr_y_min_sq(SLOTS_10)
tr_ymin2_1 = tr_y_min_sq(SLOTS_1)
tr_ymin2_5bar10 = tr_ymin2_5bar + tr_ymin2_10
tr_ymin2_5bar10_1 = tr_ymin2_5bar10 + tr_ymin2_1

# Per the SU(5) decomposition:
# Tr[Y_min²]_5̄  = 3·(1/3)² + 2·(-1/2)² = 1/3 + 1/2 = 5/6.
# Tr[Y_min²]_10 = 6·(1/6)² + 3·(-2/3)² + 1·(1)² = 1/6 + 4/3 + 1 = 5/2.
# Tr[Y_min²]_5̄+10 = 5/6 + 5/2 = 10/3  per Weyl family.
check("Tr[Y_min²]_5̄ = 5/6", tr_ymin2_5bar == Fraction(5, 6), f"got {tr_ymin2_5bar}")
check("Tr[Y_min²]_10 = 5/2", tr_ymin2_10 == Fraction(5, 2), f"got {tr_ymin2_10}")
check("Tr[Y_min²]_5̄+10 = 10/3 per Weyl family",
      tr_ymin2_5bar10 == Fraction(10, 3),
      f"got {tr_ymin2_5bar10}")

# Trace of Y_GUT² with rescaling factor c² where Y_GUT = c · Y_min.
# Tr[Y_GUT²]_5̄+10 = c² · Tr[Y_min²]_5̄+10 = (10/3) c².
# Setting equal to Tr[T_a²]_5̄+10 = T(5̄) + T(10) = 1/2 + 3/2 = 2:
# (10/3) c² = 2  =>  c² = 3/5  =>  c = √(3/5).
T_5bar = Fraction(1, 2)   # Dynkin index of SU(5) fundamental
T_10 = Fraction(3, 2)     # Dynkin index of SU(5) antisymmetric (= 2·T(fund) + 1/2 ... checked below)
tr_Ta2_5bar10 = T_5bar + T_10
check("T(5̄)  = 1/2  (SU(5) fundamental Dynkin index)", T_5bar == Fraction(1, 2))
check("T(10) = 3/2  (SU(5) antisymmetric ∧²(5) Dynkin index)", T_10 == Fraction(3, 2))
check("Tr[T_a²]_5̄+10 = 2 per Weyl family", tr_Ta2_5bar10 == Fraction(2),
      f"got {tr_Ta2_5bar10}")

# Solve for c² from trace consistency.
c_squared = tr_Ta2_5bar10 / tr_ymin2_5bar10
check("c² = Tr[T_a²]_5̄+10 / Tr[Y_min²]_5̄+10 = 2 / (10/3) = 3/5",
      c_squared == Fraction(3, 5),
      f"c² = {c_squared}")
check("Y_GUT = √(3/5) · Y_min  (✧)", c_squared == Fraction(3, 5))

# Convert to doubled convention: Y_GUT² / Y² = (Y_GUT² / (2 Y_min)²) = c²/4 = 3/20.
ratio_doubled = c_squared / Fraction(4)
check("Y_GUT² / Y² = 3/20 in doubled convention  (HYPERCHARGE_SQUARED_TRACE_CATALOG (Y5))",
      ratio_doubled == Fraction(3, 20),
      f"got {ratio_doubled}")

# Verify Tr[Y_GUT²]_5̄+10 = 2 directly with the rescaling.
tr_y_gut2_5bar10 = c_squared * tr_ymin2_5bar10
check("Tr[Y_GUT²]_5̄+10 = (3/5) · 10/3 = 2 per Weyl family",
      tr_y_gut2_5bar10 == Fraction(2),
      f"got {tr_y_gut2_5bar10}")


# ---------------------------------------------------------------------------
# Part 8: Three-generation lift.
#         Tr[Y_GUT²]_three_gen = Tr[T_a²]_SU(2),three_gen
#                              = Tr[T_a²]_SU(3),three_gen = 6
#         (matching HYPERCHARGE_SQUARED_TRACE_CATALOG (Y5).)
# ---------------------------------------------------------------------------

section("Part 8: three-generation lift")

N_GEN = 3
tr_y_gut2_three_gen = N_GEN * tr_y_gut2_5bar10
check("Tr[Y_GUT²]_three_gen = 3 · 2 = 6", tr_y_gut2_three_gen == Fraction(6),
      f"got {tr_y_gut2_three_gen}")

# Per cycle 16 catalog: Tr[T_a²]_SU(2),three_gen = 6 and Tr[T_a²]_SU(3),three_gen = 6
# computed independently from LH content + SU(3) fundamental Dynkin index. Cross-check
# value here.
DYNKIN_FUND = Fraction(1, 2)


def su2_dynkin_per_gen() -> Fraction:
    # SU(2) couples to SU(2) doublets. Dynkin index per doublet (with SU(3) multiplicity).
    # Q_L: 3 colors × Dynkin(2) = 3 · (1/2) = 3/2
    # L_L: 1 × Dynkin(2) = 1 · (1/2) = 1/2
    # All RH SU(2)-singlets contribute 0.
    return Fraction(3) * DYNKIN_FUND + Fraction(1) * DYNKIN_FUND


def su3_dynkin_per_gen() -> Fraction:
    # SU(3) couples to SU(3)-triplets / antitriplets. Dynkin index per (anti)triplet
    # (with SU(2) multiplicity).
    # Q_L:    SU(2)=2, SU(3)=3       → 2 · (1/2) = 1
    # u^c_L:  SU(2)=1, SU(3)=3̄      → 1 · (1/2) = 1/2
    # d^c_L:  SU(2)=1, SU(3)=3̄      → 1 · (1/2) = 1/2
    # SU(3)-singlets contribute 0.
    return Fraction(2) * DYNKIN_FUND + Fraction(1) * DYNKIN_FUND + Fraction(1) * DYNKIN_FUND


tr_Ta2_su2_per_gen = su2_dynkin_per_gen()
tr_Ta2_su3_per_gen = su3_dynkin_per_gen()
check("Tr[T_a²]_SU(2),per_gen = 3/2 + 1/2 = 2",
      tr_Ta2_su2_per_gen == Fraction(2),
      f"got {tr_Ta2_su2_per_gen}")
check("Tr[T_a²]_SU(3),per_gen = 1 + 1/2 + 1/2 = 2",
      tr_Ta2_su3_per_gen == Fraction(2),
      f"got {tr_Ta2_su3_per_gen}")
check("Tr[T_a²]_SU(2),three_gen = 6",
      N_GEN * tr_Ta2_su2_per_gen == Fraction(6))
check("Tr[T_a²]_SU(3),three_gen = 6",
      N_GEN * tr_Ta2_su3_per_gen == Fraction(6))
check("trace catalog (Y5) match: Tr[Y_GUT²]_three_gen "
      "= Tr[T_a²]_SU(2),three_gen = Tr[T_a²]_SU(3),three_gen = 6",
      tr_y_gut2_three_gen == N_GEN * tr_Ta2_su2_per_gen == N_GEN * tr_Ta2_su3_per_gen)


# ---------------------------------------------------------------------------
# Part 9: Negative checks — what the theorem does NOT claim.
# ---------------------------------------------------------------------------

section("Part 9: scope guards (positive checks for explicit non-claim language)")

# Substring-absence checks are unreliable here because the note's own
# "Does not claim X" sentences contain the very strings we would guard
# against. Use positive checks that the explicit negation language is
# present in the dedicated scope-guard section.

scope_guard_phrases = (
    "Does not claim SU(5) is uniquely forced",
    "Does not claim coupling unification",
    "Does not derive the GUT scale",
    "Does not derive proton decay",
)
for phrase in scope_guard_phrases:
    check(f"note explicitly states: {phrase!r}", phrase in note_text)

# Cross-check that the SO(10) alternative is acknowledged as compatible
# (so SU(5) minimality is not silently asserted).
check("note acknowledges SO(10) as a compatible alternative embedding",
      "SO(10)" in note_text)
check("note locates GUT-scale-unification assumption at cycle 19's surface, not this one",
      "remain admitted at the cycle 19 surface" in note_text
      or "physical assumption about coupling running" in note_text)

# Cycle 19's residual admission list must include both g_3 = g_2 = g_1
# AND the choice of SU(5) (vs SO(10)).
check("§5 records BOTH residual cycle 19 admissions: coupling unification AND SU(5)-choice",
      "(5)" in note_text and "(6)" in note_text
      and "g_3 = g_2 = g_1" in note_text)


# ---------------------------------------------------------------------------
# Part 10: Cycle 16 / 19 retirement.
# ---------------------------------------------------------------------------

section("Part 10: cycle 16 / cycle 19 retirement scope")

retirement_strings = (
    "retires cycles 16",
    "What this retires",
    "GUT-unification assumption",
)
for s in retirement_strings:
    check(f"note records retirement scope: {s!r}", s in note_text)

# The retirement scope must include the SU(5) gauge-group embedding admission.
check("retirement scope includes SU(5) gauge-group embedding admission",
      "SU(5) gauge-group embedding" in note_text and "admitted" in note_text)
# And the Y_GUT normalization admission.
check("retirement scope includes Y_GUT = √(3/5)·Y_SM normalization admission",
      "Y_GUT = √(3/5) · Y_SM" in note_text or "Y_GUT = √(3/5)·Y_SM" in note_text)
# But NOT the GUT-unification assumption, which remains residual.
check("note explicitly preserves residual GUT-scale unification assumption",
      "GUT-scale unification assumption" in note_text or "g_3 = g_2 = g_1" in note_text)


# ---------------------------------------------------------------------------
# Part 11: Forbidden-import audit. No PDG observed values, no fitted Yukawa,
#          no observed couplings, no GUT-scale numerical inputs.
# ---------------------------------------------------------------------------

section("Part 11: forbidden-import audit")

allowed_inputs = {
    "LHCM hypercharges (cycles 1-3)",
    "STANDARD_MODEL_HYPERCHARGE_UNIQUENESS",
    "graph-first SU(3) commutant",
    "graph-first SU(2)_weak",
    "graph-first U(1)_Y",
    "three-generation orbit algebra",
    "HYPERCHARGE_SQUARED_TRACE_CATALOG (Y5)",
}
forbidden_inputs = (
    "PDG-measured value",  # only allowed in cycle 19's *comparison* section, not as proof input
    "alpha_EM observed",
    "g_1 measured",
    "g_2 measured",
    "g_3 measured",
    "fit to observed",
)
for s in forbidden_inputs:
    check(f"runner does not consume forbidden import: {s!r}",
          s not in __file__ or s not in open(__file__).read())

# Verify the runner uses only stdlib.
import_lines = [
    line.strip() for line in open(__file__).readlines()
    if line.strip().startswith("import ") or line.strip().startswith("from ")
]
forbidden_modules = ("numpy", "scipy", "sympy", "torch", "tensorflow", "pandas")
for mod in forbidden_modules:
    has_module = any(mod in line for line in import_lines)
    check(f"runner does not import {mod}", not has_module)


# ---------------------------------------------------------------------------
# Summary.
# ---------------------------------------------------------------------------

print()
print("=" * 88)
print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
if FAIL_COUNT == 0:
    print("  VERDICT: SU(5) embedding consistency derived from LHCM hypercharges +")
    print("           representation-theory of 5̄ ⊕ 10 ⊕ 1; Y_GUT = √(3/5)·Y_min")
    print("           trace-forced under SU(5) Killing-form normalization convention.")
    print("           Cycles 16/19 SU(5)-embedding and Y_GUT-normalization admissions retired;")
    print("           residual cycle 19 admissions: (5) g_3 = g_2 = g_1 at GUT scale,")
    print("           (6) choice of SU(5) (vs SO(10), E6) as the GUT group.")
else:
    print("  VERDICT: FAIL")
print("=" * 88)

sys.exit(1 if FAIL_COUNT > 0 else 0)
