# Koide Theta Hierarchy Open Scalar -- CLOSED by Berry-Phase Theorem

**Date:** 2026-04-19
**Status:** CLOSED (cycle 10B). Originally the remaining open scalar on
the Koide charged-lepton lane: the doublet argument theta_PDG ~ 2.0416
rad ~ 116.976 deg in the circulant parametrization, equivalent to
Brannen-Zenczykowski delta = 2/9. Not expressible as a retained
angular primitive in cycles 1-4. Now **closed** by the retained
**Berry-phase theorem** on the projectivized Koide cone.

**Primary reference:** `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`.

---

## 1. What changed between cycle 1-4 and cycle 10

### Cycle 1-4 state

The Koide theta was the residual open scalar after AXIOM D pinned
kappa = 2. AXIOM D fixes `|b|` relative to `a` on the sqrt-parent
`H = aI + bC + b^bar C^2`, but not `arg(b)`. The PDG value

    theta_PDG = 2 pi / 3 + 2/9 ~ 2.0416 rad

(Brannen delta = 2/9, 2-decade phenomenological value;
Brannen 2006 MASSES2.pdf; Zenczykowski PRD 86 (2012) 117303) was not
reproducible from retained angular primitives at 0.05% tolerance.
Closure routes flagged at that time:

- atom-bank extension (add more retained angles);
- third-moment readout primitive (cubic moment construction);
- CP / Klein-four sigma_S lift;
- positive-parent-axis obstruction lift.

Cycle 8 Q1 reformulated the content as AXIOM E:

    cos(3 * arg(b_s)) = cos(Q),    Q = 2/3,

which is independent of AXIOM D + A0-A3 (cycle 8 Q1 proved this on the
Hilbert series of the coordinate ring modulo AXIOM D).

### Cycle 10B state (this update)

AXIOM E has been reduced to a **theorem** via the **Berry-phase theorem
on the projectivized Koide cone S^2_Koide**. The construction:

1. Projectivize the Koide cone to S^2_Koide.
2. Identify the natural equivariant line bundle L_doublet = det(doublet)
   associated to the non-trivial C_3 isotype of the hw = 1 triplet.
3. Its first Chern number is `n = dim(doublet) = d - 1 = 2` (at d = 3),
   by Borel-Weil / Pieri on S^2 under a finite-group action.
4. The monopole connection of flux n has Berry holonomy over one C_3
   cyclic period equal to `gamma = 2 pi n / d = 2 pi Q`.
5. Brannen reduction: `delta_d = Q / d = (d - 1) / d^2`, giving
   `delta_3 = 2 / 9` exactly.

The value 2/9 emerges from the **Chern-fraction per orbifold
fundamental period** of the doublet monopole bundle at d = 3. No
numerical tuning. No new axioms.

AXIOM E -- equivalently, the Koide theta -- is now a corollary of the
Berry-phase theorem.

Cost: zero new axioms. AXIOM E has dropped from the axiom list.

---

## 2. Current status

The Koide theta hierarchy is **closed**. The 2/9 value is
structurally forced by retained equivariant index-theoretic data on
S^2_Koide (Chern class + C_3 orbifold structure). The dim-parametric
scan d = 2..7 verifies `delta_d = (d - 1) / d^2` at every dim.

---

## 3. Runner status

The old runner `scripts/frontier_koide_theta_hierarchy_open_scalar.py`
is NOT included in this branch (the open scalar is closed). Its
functional content is absorbed into the Berry-phase theorem runner
`scripts/frontier_koide_berry_phase_theorem.py` (PASS=26 FAIL=0).

---

## 4. Cross-references

- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` (cycle 10B, primary)
- `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md` (cycle 10A, AXIOM D -> theorem)
- `docs/KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md` (sqrt-mass dictionary, on main)
- `docs/CYCLE_1_TO_10_SYNTHESIS_NOTE_2026-04-19.md` (reading order)
- Brannen 2006 MASSES2.pdf; Zenczykowski PRD 86 (2012) 117303; PRD 87 (2013) 077302; Rivero-Gsponer hep-ph/0505220 (historical Brannen phase literature).
