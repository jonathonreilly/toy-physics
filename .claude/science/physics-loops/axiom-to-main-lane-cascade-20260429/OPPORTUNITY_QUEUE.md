# Opportunity Queue

**Slug:** axiom-to-main-lane-cascade-20260429
**Date:** 2026-04-29
**Refresh:** initial seed; refresh at every block closure

Ranked retained-positive science targets for the 12-hour campaign. Each row is
a self-contained science block that can attempt closure independently. Ranking
weights: retained-positive probability, lane-cascade leverage (rows unlocked),
runtime feasibility, independence from blocked lanes, deep-stretch suitability.

## Queue (initial)

### Q1: Koide Q canonical-descent closure (HIGHEST LEVERAGE)

- **Lane:** charged-lepton Koide bridge package (line 192) +
  Q23 surface theorem (KOIDE_EIGENVALUE_Q23_SURFACE_THEOREM_NOTE_2026-04-20)
- **Status before:** Q V7.3 lands "retained promotion theorem" with
  conditional Q closure corollary (commit 302cd9e3, runner PASS=56). Codex
  V5/V6 landing pattern matches.
- **Goal:** lift the conditional closure to full closure on the current axiom
  surface. Specifically, prove that source-domain canonical descent of the
  cyclic mass-amplitude line forces `(sum sqrt(m_l))^2 = (3/2) sum m_l`
  unconditionally, by deriving the source-free reduced-carrier selection
  from the `Cl(3)` + cubic graph axioms alone.
- **Cascade unlocked:** lines 158, 159, 160, 161, 162 (CKM Bernoulli /
  n/9 / cubic / Egyptian-fraction / consecutive-primes / S_3 supports);
  157 (cross-sector V_cb bridge); 166 (charged-lepton Koide); 167
  (Q OP source-domain); 168 (Q SO(2) phase erasure). Total 9 rows.
- **Hard residual:** physical source-domain/source-free reduced-carrier
  selection behind `Q = 2/3`.
- **First-principles routes available:**
  - R-Q1: Cl(3) automorphism-fixing of A_1 carrier line under cubic
    Z_3 source rotation.
  - R-Q2: Berry-phase orbit closure on the eigenvalue Q23 surface theorem.
  - R-Q3: source-free reduced-carrier selection from minimal Hilbert /
    locality / information axiom (cf. SINGLE_AXIOM_HILBERT_NOTE.md).
- **Score:** retained-positive 2/3, cascade 3/3, runtime 2/3, independence
  3/3, stretch 3/3 → **13/15** (rank #1).

### Q2: Koide δ = 2/9 rad analytical derivation

- **Lane:** charged-lepton Koide bridge (line 192). Type-B `2/9` readout,
  period-`1 rad` vs `2π rad` convention, downstream `m_*/(w/v)` chain.
- **Status before:** V1 rejected by Codex; V2 (commit 7d9b2018) attempts
  closure via OP local-source protocol. Subagent review #4 APPROVED.
- **Goal:** derive `δ = 2/9` analytically from a Berry-phase / cyclic
  source-line argument on the retained Q23 surface, with the period
  convention forced by the source-free reduced carrier (R-Q1 result if Q1
  closes).
- **Cascade unlocked:** completes the Q+δ Koide closure pair; activates
  line 158 fully (no more "no Koide closure" qualifier).
- **Hard residual:** based-endpoint and period-convention selection.
- **First-principles routes available:**
  - R-D1: Plancherel-decomposition of A_1 cyclic line (V1 attempt
    extended).
  - R-D2: Berry-phase holonomy on cubic Z_3 source rotation orbit.
  - R-D3: SO(2) phase-erasure → 2/9 = 2/(3·3) = (2/N_color)/N_color
    structural identity.
- **Score:** retained-positive 2/3 (depends on Q1), cascade 2/3, runtime
  2/3, independence 1/3, stretch 3/3 → **10/15** (rank #2 if Q1 lands;
  drops to 8/15 if Q1 blocks).

### Q3: Quark mass-ratio first-principles endpoint chain

- **Lane:** Quark mass-ratio support stack (line 164); Down-type CKM-dual
  (line 163).
- **Status before:** bounded; threshold-local self-scale comparators give
  `0.05000`, `0.02234`, `0.001117`; common-scale `m_s(m_b)/m_b(m_b)`
  stays `+15.0%` away.
- **Goal:** derive an exact endpoint ratio chain (or readout map) from the
  taste-staircase mass mechanism that closes the +15% gap structurally
  without observed-mass input.
- **Cascade unlocked:** lines 163, 164. Promotes the CKM down-type
  inversion to an audit-ratifiable retained corollary.
- **Hard residual:** common-scale matching and time-coupling law for the
  taste-staircase mechanism.
- **First-principles routes available:**
  - R-M1: derive the running-coupling time-scale identification from the
    Wilson reduction-existence + susceptibility-flow theorems (gauge
    vacuum plaquette stack).
  - R-M2: structural readout map from the Cl(3) mass operator on the
    canonical eigenline.
- **Score:** retained-positive 2/3, cascade 1/3, runtime 1/3,
  independence 2/3, stretch 3/3 → **9/15** (rank #3).

### Q4: Cl_4(C) module axiom (Axiom*) derivation or no-go

- **Lane:** Hubble C1 (G1) closure gate; CL4C consequence map shows
  Axiom* + (C2) closes Lane 5 + Lane 1 Target 2 + Planck Targets 1-3 +
  (Σm_ν conditional retention).
- **Status before:** Axiom* itself NOT adopted; consequence map landed
  conditional cascade; both A1/A2/A4/A5 of (G1) closed negatively.
- **Goal:** EITHER derive the Cl_4(C) module structure on `P_A H_cell` from
  `Cl(3)` + `Z^3` + finite Grassmann axioms (retiring Axiom* as a
  separate input), OR prove an exact no-go that any axiom strictly
  contained in `{Cl(3), Z^3, Grassmann, g_bare=1}` cannot close (G1).
  The no-go would force adoption of Axiom* as the minimal extension.
- **Cascade unlocked:** Hubble C1 (Lane 5), Lane 1 Target 2, Planck
  Targets 1-3, Σm_ν h-retained conditional. Total 5+ rows.
- **Hard residual:** the carrier algebra extension from `Cl(3)` (3 real
  Pauli generators) to `Cl_4(C)` (4 complex Dirac generators) on the
  primitive event cell.
- **First-principles routes available:**
  - R-A1: extend the cubic + time generator to a 4D Clifford action by
    invoking the retained anomaly-forced 3+1 theorem.
  - R-A2: derive `P_A H_cell` projector dimension from the Hamming-weight-1
    primitive coframe boundary carrier theorem (PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25).
  - R-A3: prove that no integer linear combination of existing minimal
    axioms generates an irreducible Cl_4(C) module — exact no-go.
- **Score:** retained-positive 1/3 (axiom-level is hard), cascade 3/3,
  runtime 1/3, independence 3/3, stretch 3/3 → **11/15** (rank #2).

### Q5: BH 1/4 carrier from framework Wald-Noether charge

- **Lane:** Bekenstein-Hawking entropy (line 179); BH area law target.
- **Status before:** Planck Pin retained Nature-grade with structural BH
  derivation from framework's Wald-Noether charge on retained discrete
  GR action; framework's `c_cell = 1/4` IS the BH coefficient via
  `S_Wald = A·c_cell ↔ S_BH = A/(4G)`. Codex probability ~90-95%
  (per user memory 2026-04-26).
- **Goal:** lift the proposed_retained Wald-Noether BH theorem to a
  retained-grade artifact by independently verifying the
  Wald formula on the discrete GR action surface (already retained:
  UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE) and tightening the Wald
  formula's axiom-acceptance status.
- **Cascade unlocked:** line 179 (BH area law). One row but it is a
  publication-headline target.
- **Hard residual:** Wald formula universality on the retained discrete
  3+1 GR action (currently a literature-input universal physics
  statement on equal footing with Newton).
- **First-principles routes available:**
  - R-B1: derive Wald-Noether charge from the retained Universal QG
    canonical refinement net + Lorentzian global atlas closure
    (UNIVERSAL_QG_*; UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE).
  - R-B2: prove `c_cell = 1/4` boundary-density extension uniqueness on
    the framework's primitive coframe surface (already retained).
- **Score:** retained-positive 2/3, cascade 1/3, runtime 2/3,
  independence 3/3, stretch 2/3 → **10/15** (rank #2 tied).

### Q6: DM η freeze-out-bypass closure attempt

- **Lane:** DM η freeze-out-bypass support lane (line 125).
- **Status before:** bounded; m_DM = N_sites · v candidate; G1 SU(3)
  lane open (per user memory 2026-04-25).
- **Goal:** close the `m_DM = N_sites · v` candidate by deriving N_sites
  from the cubic `Z^3` + Cl(3) lattice automorphism count, OR demote to
  no-go on a named structural obstruction.
- **Cascade unlocked:** line 125 (DM lane); contributes to Σm_ν
  cross-bound (sigma-mnu-f3 work).
- **Hard residual:** N_sites combinatorial count + v-scale matching.
- **First-principles routes available:**
  - R-DM1: derive N_sites from the retained generation count (3) and
    cubic automorphism Oh order.
  - R-DM2: derive m_DM directly from the retained EW v scale via the
    matter-content count.
- **Score:** retained-positive 1/3, cascade 1/3, runtime 2/3,
  independence 2/3, stretch 2/3 → **8/15** (rank #5).

### Q7: Plaquette β=6 explicit Perron / boundary closure

- **Lane:** plaquette `<P>` value support stack (line 33 USABLE INDEX).
- **Status before:** exact local Wilson marked-link factor and exact
  normalized mixed-kernel local compression are explicit; remaining open
  object is the explicit `β=6` tensor-transfer Perron / boundary data
  generating boundary character data of `Z_6^env`.
- **Goal:** explicitly compute the `β=6` Perron eigenvector and
  boundary character data using the retained transfer-operator /
  character-recurrence theorem (GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE),
  closing the last open object in the plaquette analytic chain.
- **Cascade unlocked:** repo-wide plaquette numeric migration to the
  analytic value `P_cand(6) = 0.593530679977098`. Affects EW v, alpha_s,
  YT, all downstream.
- **Hard residual:** explicit Perron solve of `exp(3J) D_6^loc C_(Z_6^env) exp(3J)`.
- **First-principles routes available:**
  - R-P1: numerical Perron eigenvector solve on small `Z_6^env`
    representation.
  - R-P2: structural analytic identification of the Perron state via
    spatial-environment tensor-transfer theorem.
- **Score:** retained-positive 1/3 (numerical Perron is research-grade),
  cascade 3/3, runtime 1/3, independence 3/3, stretch 3/3 → **11/15**
  (rank #2 tied — but mostly a stretch-attempt route).

## Initial selection

**Block 1 = Q1 (Koide Q canonical-descent closure)** — highest cascade
leverage and best stretch suitability. Run first.

**Block 2 candidates (after Block 1 outcome):**
- if Q1 closes: Block 2 = Q2 (Koide δ analytical derivation, builds on Q1).
- if Q1 blocks: Block 2 = Q4 (Cl_4(C) axiom derivation/no-go, independent
  axiom-level lever).

**Block 3 candidates:** Q3 (quark mass ratios) or Q5 (BH 1/4 carrier),
chosen by remaining runtime and Block 2 outcome.

**Block 4+:** Q5, Q6, Q7 in remaining runtime, plus newly identified
opportunities from refresh.

## Refresh trigger

Refresh this queue:
- after each block closure (success, no-go, or honest stop);
- after every two cycles of audit-grade output (force a stretch route);
- after any review-loop demote/block disposition.
