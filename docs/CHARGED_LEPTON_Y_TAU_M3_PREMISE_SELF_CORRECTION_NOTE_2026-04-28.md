# `y_τ` Cycle 4 Fan-out M3 Premise — Self-Correction

**Date:** 2026-04-28
**Status:** retained branch-local **self-correction** note on
`frontier/charged-lepton-pickup-20260428`. Cycle 5 of the charged-
lepton loop: the Cycle 4 stuck-fan-out (M3 candidate, "EW A_4 flavor-
symmetry anchor") rests on a **misreading of the lane file's
"Generation-color and EW A4 bridges (recent landing 2026-04-25)"
phrase.** Reading the actual bridge notes shows:
- `CKM_EW_LATTICE_A4_BRIDGE_RETAINED_IDENTITY_NOTE_2026-04-25.md`
  packages `sin²(θ_W)|_lattice = A^4 = 4/9` where `A^4 = (Wolfenstein
  A)^4` — this is **gauge-coupling normalization**, not the
  alternating group `A_4`. The note explicitly closes with
  `KOIDE_CLOSURE=FALSE`.
- `CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`
  packages `N_gen = N_color = 3` — an **integer-counting identity**.
  The note explicitly disclaims "this is numerical agreement of two
  target-class readouts, not a charged-lepton Koide theorem."

There is **no `A_4` (alternating-group) flavor symmetry** in the
framework's retained content. M3 as Cycle 4 framed it does not
exist. **Result: M3 closed (false premise). Reassess M5 backup.**
**Lane:** 6 — Charged-lepton mass retention (Phase-1 6B)
**Loop:** `charged-lepton-pickup-20260428`

---

## 0. What Cycle 4 said vs. what the bridges actually say

### 0.1 Cycle 4 M3 framing (mistaken)

> M3 — Generation-flavor-symmetry anchor (using retained EW A4 bridges).
> Premise: the recent (2026-04-25) retained "Generation-color and EW
> A4 bridges" landings may provide a generation-flavor-symmetry
> constraint that anchors the τ-Yukawa via the alternating group
> A_4 (the standard three-generation flavor symmetry candidate).
> Mechanism: A_4 representation theory on the lepton-doublet
> generation triplet… A_4 has a 3-dimensional irreducible
> representation; if the retained EW A4 bridge places L_L
> generations in this rep, the A_4 Clebsch-Gordan structure
> constrains the Yukawa coefficient ratios.

This is a **fabrication** of A_4 flavor-symmetry content not present
in the retained bridges.

### 0.2 What the actual EW A4 bridge says

`CKM_EW_LATTICE_A4_BRIDGE_RETAINED_IDENTITY_NOTE_2026-04-25.md`:

```text
sin^2(theta_W)|_lattice = A^4 = 4/9
```

where `A` is the Wolfenstein parameter (CKM matrix structure) and
the identity is

```text
sin^2(theta_W)|_lattice
  = g_Y^2 / (g_Y^2 + g_2^2)
  = (1/(d+2)) / (1/(d+2) + 1/(d+1))
  = (d+1)/(2d+3) = 4/9       (with d = 3)
```

This is a **CKM-EW lattice-scale gauge-coupling normalization
identity**. It does not introduce any alternating-group A_4
representation, does not assign lepton-doublet generations to any
flavor-symmetry rep, and does not constrain Yukawa coefficient
ratios. The note's own closeout explicitly states:

```text
KOIDE_CLOSURE=FALSE
```

### 0.3 What the actual cross-sector Z_3 closure says

`CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`:

```text
(R1)  N_gen = 3       [retained, THREE_GENERATION_STRUCTURE_NOTE]
(R2)  N_color = 3     [retained, CKM_MAGNITUDES_STRUCTURAL_COUNTS]
(R3)  N_gen = N_color = 3       (direct retained equality)
```

This is a **numerical integer equality** between two retained
counts. The note's auxiliary reading (numerical coincidence
`(N_gen - 1)/N_gen² = (N_color - 1)/N_color² = 2/9`) is explicitly
flagged:

> This is **numerical agreement** of two target-class readouts,
> not a charged-lepton Koide theorem and not a structural
> unification.

The note explicitly does **not** close any charged-lepton mass
identity. Its boundary section says:

> Does NOT promote any prior Koide-bridge support-tier branch to
> retained Koide closure.

### 0.4 The misreading

The lane file's phrase

> "Generation-color and EW A4 bridges (recent landing 2026-04-25)"

cited in
`docs/lanes/open_science/06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md`
contains the substring "A4" which I (in Cycle 4) interpreted as the
alternating group `A_4`. The actual content is `A^4 = (Wolfenstein
A)^4 = 4/9`. The two are unrelated.

## 1. Honest reassessment of the six Cycle 4 candidates

| Candidate | Cycle 4 promise | After audit | Why |
|---|---|---|---|
| M1 Koide-structural | medium | medium (unchanged) | Q + δ closure required (in flight on flagship) |
| M2 SU(2)×U(1) combined | medium | low (depends on unestablished D17-prime) | unchanged |
| **M3 EW A4 flavor-symmetry** | **high** | **CLOSED** | **false premise: no A_4 flavor symmetry exists in retained content** |
| M4 Anomaly-cancellation | low | low (speculative) | unchanged |
| M5 Cross-sector y_τ/y_t | medium-high | needs sharper audit (this cycle) | y_t identity uses color Fierz; lepton has no color |
| M6 Direct Cl(3) three-gen | low | low (speculative) | unchanged |

So the Cycle 4 fan-out's headline ("M3 strongest") is wrong. **The
remaining single-cycle backup is M5.**

## 2. M5 audit: cross-sector `y_τ / y_t` ratio

### 2.1 Premise

If a structural identity gave `y_τ / y_t = const` at lattice scale,
then `y_τ` retains via retained `y_t = g_s / sqrt(6)`.

### 2.2 What such an identity would have to do

The retained YT-lane chain D1-D17 produces

```text
y_t_bare = g_s_bare / sqrt(2 N_c) = g_s_bare / sqrt(6)              (YT-T1)
```

with the load-bearing factor `1/sqrt(2 N_c) = 1/sqrt(6)` from the
SU(N_c) **color Fierz identity D12** on the `Q_L = (2, 3)` block.
Combined with retained 1-loop running (or lattice-scale evaluation),
`y_t` retains.

A `y_τ / y_t = const` cross-sector identity would have to deliver,
on the lepton (2, 1) block:

- A structural numerator with a known sqrt-rational factor (analog
  of the YT Block 4 / Block 5 structural primitives), AND
- A way to factor out the difference between (2, 3) and (2, 1)
  blocks — i.e., the color-Fierz factor `sqrt(2 N_c)` itself.

### 2.3 Why this fails on retained content

The cross-sector Z_3 closure
(`CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`)
closes `N_gen = N_color = 3` as **integer-counting equality**, not
as a Yukawa-coefficient identity. Per its own boundary statement:

> Does NOT derive A² = Q_l = 2/3 cross-sector identification (W2
> retains A² = 2/3 independently; Koide Q_l = 2/3 is empirical
> input outside the retained framework derivation chain on main).
> Does NOT promote any prior Koide-bridge support-tier branch to
> retained Koide closure.

So a Yukawa-coefficient cross-sector identity `y_τ / y_t = const`
is **NOT** a consequence of the retained Z_3 closure or of the
EW A^4 = 4/9 bridge.

To establish such an identity from retained content alone would
require:

- A structural primitive on the (2, 1) block analogous to YT-lane
  D17 (composite-Higgs scalar uniqueness on Q_L) — currently
  unestablished for the lepton block (Cycle 2 finding).
- A Fierz-analog factor on the (2, 1) block — currently does not
  exist (Cycles 2 + 3 combined no-go).

Both of these were closed in Cycles 2 + 3. So **M5 reduces to the
same load-bearing structural primitives that Cycles 2 + 3
excluded**: the cross-sector ratio doesn't add a new derivation
chain, it inherits the closed gauge-anchor obstruction.

**Status:** M5 closed on current retained surface. Same root
cause as SA-A and SA-B: no Fierz-analog for the colorless lepton
block, no D17-analog verified for the (2, 1) block.

### 2.4 What M5 would need (research-level, not single-cycle)

For M5 to land, one of the following would have to be established
as new structural content:

- (M5-a) D17-prime: composite-Higgs scalar uniqueness on the (2, 1)
  lepton-doublet block (analog of YT D17 on the (2, 3) quark-doublet
  block). Currently unverified.
- (M5-b) A non-Fierz Yukawa-coefficient identity that exploits the
  combined SU(2) × U(1) representation structure on the lepton
  block plus the Z_3 generation-color identity to produce a
  sqrt-rational factor. Currently no candidate construction.
- (M5-c) Koide-flagship-anchored cross-sector identity: with
  Q = 2/3 retained, `(m_τ / Σ m_ℓ)` is structurally pinned on the
  lepton mass-square-root direction, providing a "lepton-side"
  structural anchor that could be tied to retained `y_t` via the
  Z_3 generation-color closure. **Depends on Koide flagship
  closing first.**

None of (M5-a), (M5-b), (M5-c) are single-cycle attemptable on the
current retained surface.

## 3. Combined no-go: extends through M3 + M5

Cycles 2, 3, and now Cycle 5 (M3 false-premise + M5 audit) together
extend the combined no-go:

**Theorem (charged-lepton structural y_τ Ward identity, current
retained surface).** On the retained `Cl(3)/Z^3` framework with:
- YT-lane chain D1-D17 retained for the (2, 3) Q_L block,
- Cycle 2 finding (no SU(2) Fierz analog on the (2, 1) lepton block),
- Cycle 3 finding (no abelian Fierz analog for U(1)_Y),
- Cycle 5 finding (no A_4 alternating-group flavor symmetry in
  retained content; M3 false premise),
- Cycle 5 audit (M5 reduces to closed gauge-anchor obstruction),

no `y_τ` Ward identity of the form `y_τ_bare = (retained content) ×
(structural sqrt-rational constant)` is constructible on the
current retained surface.

**Surviving research-level routes (not single-cycle attemptable):**

- **(M1)** Koide-structural anchor (depends on Koide flagship
  Q + δ closure landing). Closest to attemptable; depends on a
  parallel-lane closure.
- **(M5-c)** Koide-anchored cross-sector y_τ ↔ y_t (depends on
  Koide flagship + new cross-sector derivation chain).
- **(M5-a)** D17-prime on (2, 1) block (open structural problem
  with no current candidate).

## 4. Implications for Lane 6 closure pathway

After Cycle 5:

- **All single-cycle attemptable y_τ Ward identity routes on the
  current retained surface are CLOSED.** Six candidate mechanisms
  audited; none have a single-cycle path on the retained surface.
- **Lane 6 6B is research-level distant.** Closure within the loop
  budget is not feasible without parallel-lane progress (Koide
  flagship Q + δ closure, then M1 or M5-c attemptable).
- **Honest stop is now warranted.** Both Deep Work Rules
  requirements are satisfied (≥1 stretch attempt: Cycles 2, 3;
  ≥1 stuck fan-out: Cycle 4; falsified misreading caught in
  Cycle 5).

This is the same pattern as the neutrino loop's Cycle 10 finding
on 4A `m_lightest`: structurally distant from `A_min`, requires
parallel-lane progress (there: Lorentz-onset / Pfaffian-extension;
here: Koide flagship + new structural content).

## 5. Cycle 4 status correction

`CHARGED_LEPTON_Y_TAU_MECHANISM_STUCK_FANOUT_NOTE_2026-04-28.md`
remains valid as a stuck-fan-out artifact (six orthogonal candidates
generated, synthesis attempted), but its **headline conclusion
("M3 strongest single-cycle continuation") is superseded by this
note's finding** that M3 rests on a misreading. The corrected
ranking is:

| Candidate | Status after Cycle 5 |
|---|---|
| M1 Koide-structural | research-level; depends on Koide flagship |
| M2 SU(2)×U(1) combined | low (unestablished primitive) |
| M3 EW A4 flavor-symmetry | **CLOSED — false premise** |
| M4 Anomaly-cancellation | low (speculative) |
| M5 Cross-sector y_τ/y_t | closed on current surface; M5-c research-level conditional |
| M6 Direct Cl(3) three-gen | low (speculative) |

The Cycle 4 fan-out artifact is not removed; it remains in the
loop's audit trail with this self-correction supersedence-note.

## 6. What this cycle closes and does not close

**Closes:**

- M3 candidate (false premise — no A_4 alternating-group flavor
  symmetry in framework's retained content; "EW A4" = `A^4 = 4/9`
  Wolfenstein gauge-coupling identity, unrelated).
- M5 candidate on current retained surface (reduces to closed
  gauge-anchor obstruction from Cycles 2 + 3).
- The combined no-go extension: no single-cycle y_τ Ward identity
  route remains on the current retained surface.
- Honest stop justification for Lane 6 charged-lepton block within
  this loop's runtime budget.

**Does not close:**

- Lane 6 6B `y_τ` Ward identity.
- M1 Koide-structural (research-level conditional on flagship).
- M5-c Koide-anchored cross-sector (research-level conditional).
- M5-a D17-prime on (2, 1) block (open structural problem).

## 7. Falsifiers

This cycle's findings are falsified by:

- A retained-tier note showing that the framework's accepted
  surface includes an `A_4` (alternating group) flavor-symmetry
  representation assignment for the lepton-doublet generations
  (would resurrect M3).
- A worked Yukawa-coefficient cross-sector identity `y_τ / y_t =
  const` derivable from the retained Z_3 generation-color closure
  alone (would resurrect M5 on current surface).
- Closure of the Koide flagship Q + δ identities, which would
  unblock M1 and M5-c (would shift Lane 6 6B from research-level
  to single-cycle attemptable).

## 8. Cross-references

- Cycle 1 theorem plan:
  `docs/CHARGED_LEPTON_LANE6_THEOREM_PLAN_NOTE_2026-04-28.md`.
- Cycle 2 SA-A SU(2) anchor exclusion:
  `docs/CHARGED_LEPTON_Y_TAU_WARD_IDENTITY_SU2_ANCHOR_STRETCH_ATTEMPT_NOTE_2026-04-28.md`.
- Cycle 3 SA-B U(1)_Y anchor exclusion:
  `docs/CHARGED_LEPTON_Y_TAU_WARD_IDENTITY_U1_ANCHOR_STRETCH_ATTEMPT_NOTE_2026-04-28.md`.
- Cycle 4 stuck fan-out (superseded headline):
  `docs/CHARGED_LEPTON_Y_TAU_MECHANISM_STUCK_FANOUT_NOTE_2026-04-28.md`.
- Actual EW A4 bridge content (mistakenly cited as A_4 flavor sym):
  `docs/CKM_EW_LATTICE_A4_BRIDGE_RETAINED_IDENTITY_NOTE_2026-04-25.md`.
- Actual cross-sector Z_3 closure content:
  `docs/CKM_KOIDE_CROSS_SECTOR_Z3_CLOSURE_THEOREM_NOTE_2026-04-25.md`.
- Lane 6 lane file (citation context):
  `docs/lanes/open_science/06_CHARGED_LEPTON_MASS_RETENTION_OPEN_LANE_2026-04-26.md`.
- YT-lane analog template:
  `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`.
- Cross-lane analog (neutrino 4A m_lightest):
  `docs/NEUTRINO_LANE4_4A_M_LIGHTEST_WARD_IDENTITY_STRETCH_ATTEMPT_NOTE_2026-04-28.md`.
- Loop pack:
  `.claude/science/physics-loops/charged-lepton-pickup-20260428/`.

## 9. Boundary

This is a self-correction artifact. It catches a misreading in
Cycle 4's stuck-fan-out (M3 candidate fabricated an A_4 flavor
symmetry not present in retained content), audits the M5 backup,
and extends the combined no-go through both. The honest finding
is that **all single-cycle attemptable y_τ Ward identity routes on
the current retained surface are closed**; Lane 6 6B is research-
level distant and requires parallel-lane progress (Koide flagship
or new structural content).

A runner is not authored.
