# Koide Frobenius-Uniformity Axiom Candidate -- SUPERSEDED by MRU Theorem

**Date:** 2026-04-19
**Status:** SUPERSEDED (cycle 10A). Originally proposed as an axiom
candidate ("AXIOM D") closing the Koide kappa = 2 gap through block-
democratic Frobenius stationarity on the cyclic-compression image. Now
**demoted** to the d = 3 specialization of the retained **Moment-Ratio
Uniformity (MRU) theorem** on Cl(d)/Z_d. AXIOM D is no longer an
axiom; its content (kappa = 2) follows from MRU + retained d = 3.

**Primary reference:** `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`.

---

## 1. What changed between cycle 1-4 and cycle 10

### Cycle 1-4 state

AXIOM D was proposed as the minimal new axiom closing the Koide
kappa = 2 gate:

> Retained Frobenius uniformity on the cyclic-compression image: within
> each Z_3-isotype of Herm_circ(3), the Frobenius-weighted cyclic-
> response sum is uniform.

At d = 3 this forces `a^2 = 2 |b|^2`, i.e. kappa = 2.

Cost: one new axiom (AXIOM D) supplemental to A0-A3.

### Cycle 10A state (this update)

AXIOM D has been reduced to a **theorem** via the Moment-Ratio
Uniformity (MRU) principle on Cl(d)/Z_d, a **dim-parametric** principle
defined at arbitrary d >= 2:

    M(I) = M(I')  for all isotypes I, I' in Iso(d),

with `M(I) := (1/w(I)) sum_{j in J(I)} r_j^2` the isotype moment and
w(I) the common per-basis-element Frobenius norm squared of isotype I.

MRU's per-d structure is genuinely non-trivial (it gives 1, 1, 2, 2, 3
scalar equations at d = 2, 3, 4, 5, 6 respectively). At d = 3 MRU
collapses to the single equation `a^2 / 3 = |b|^2 / 6`, i.e. **kappa =
2 = AXIOM D**.

Uniqueness: MRU has a single non-trivial singlet-vs-doublet selector
iff Iso(d) has exactly one singlet and one complex doublet, which holds
iff d = 3.

Cost: zero new axioms. MRU is a theorem (pre-conditions are all retained
on main). AXIOM D has dropped from the axiom list.

---

## 2. Current axiom status

AXIOM D is **not an axiom anymore**. The content kappa = 2 is now a
corollary of MRU + retained d = 3.

This note is retained as historical context showing the route:

- Cycle 1-2: open scalar in the Koide kappa lane.
- Cycle 3: AXIOM D proposed (block-democratic Frobenius stationarity;
  cycle 3 no-go suite passes 32/32).
- Cycle 4: AXIOM D holds; axiom cost confirmed as 1.
- Cycle 10A: AXIOM D demoted to theorem via MRU.

The Frobenius-uniformity language survives in MRU as the Frobenius-
metric weighting choice; the cyclic-compression retained image is
unchanged; the 7 no-gos pass (inherited).

---

## 3. Runner status

The old runner `scripts/frontier_koide_frobenius_uniformity_axiom_candidate.py`
is NOT included in this branch (the axiom is superseded). Its
functional content is absorbed into the MRU runner
`scripts/frontier_koide_moment_ratio_uniformity_theorem.py` (PASS=65
FAIL=0).

---

## 4. Cross-references

- `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md` (cycle 10A, primary)
- `docs/KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md` (cycle 2, orbit-dim sharpening)
- `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md` (cycle 1, shared isotype decomposition)
- `docs/CYCLE_1_TO_10_SYNTHESIS_NOTE_2026-04-19.md` (reading order)
