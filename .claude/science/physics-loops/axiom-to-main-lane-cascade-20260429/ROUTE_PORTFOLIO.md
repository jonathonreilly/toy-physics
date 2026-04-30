# Route Portfolio

**Slug:** axiom-to-main-lane-cascade-20260429
**Date:** 2026-04-29

For each opportunity, the routes that pass the dramatic-step gate. Scored on
claim-state upgrade, import retirement, review-blocker close, artifactability,
novelty, deep-stretch suitability, and overclaim risk (negative).

## Q1: Koide Q canonical-descent closure

### R-Q1: Cl(3) automorphism-fixing of A_1 carrier

- **Route type:** constructive theorem (axiom-cyclic-line)
- **Premise (A_min only):** under cubic Z_3 source rotation acting on the
  `Cl(3)` A_1 (trace-line) eigenspace, the Q23 surface theorem
  (KOIDE_EIGENVALUE_Q23_SURFACE_THEOREM_NOTE_2026-04-20) implies a unique
  source-free reduced carrier whose three eigenvalue ratios live in the
  cyclic-orbit of {Z_3 fixed}.
- **Conjecture:** the only Z_3-cyclic, source-free, irreducible reduced
  carrier on `Cl(3)` admitting non-degenerate eigenvalue triples is the
  one with `(Σ√x_i)^2 = (3/2) Σ x_i` (i.e., `Q = 2/3`).
- **Why it might land:** uses two retained surfaces (Q23 surface theorem,
  graph-first Z_3 source) plus only the A_min Cl(3) algebra; no observed
  mass enters.
- **Score:** state-upgrade 3, import-retirement 3, blocker-close 3,
  artifact 2, novelty 3, stretch 3, overclaim risk -1 → **16/18**.

### R-Q2: Berry-phase orbit closure on Q23 surface

- **Route type:** constructive theorem + symmetry argument
- **Premise:** Q23 surface theorem says the Q-surface in the 3-eigenvalue
  space is the cone (Σ√x_i)^2 / (Σ x_i) = const. Find the value of `const`
  forced by Berry-phase closure on the cyclic orbit of the source-free
  reduced carrier.
- **Why it might land:** Berry phase on a cyclic orbit is a well-defined
  geometric quantity; if the source-free carrier exists (R-Q1) the Berry
  closure gives a unique const without observed input.
- **Score:** state-upgrade 3, import-retirement 2, blocker-close 2,
  artifact 2, novelty 3, stretch 3, overclaim risk -1 → **14/18**.

### R-Q3: source-free reduced-carrier from one-axiom Hilbert/locality/info

- **Route type:** constructive theorem
- **Premise:** SINGLE_AXIOM_HILBERT_NOTE.md establishes that `Cl(3)` +
  Hilbert/locality/info uniquely fixes the local Hilbert space. Combine
  with the Z_3 cyclic constraint to fix the source-free reduced carrier.
- **Why it might land:** ties Q1 to the strongest minimal-axiom result on
  current main.
- **Score:** state-upgrade 3, import-retirement 3, blocker-close 3,
  artifact 2, novelty 2, stretch 2, overclaim risk -1 → **14/18**.

### Selected route for Block 1: R-Q1

R-Q1 has the cleanest direct construction: Q23 surface (retained) +
cubic Z_3 (retained) + Cl(3) automorphism. R-Q3 is the fallback if R-Q1
hits a residual carrier-selection ambiguity.

## Q2: Koide δ = 2/9 rad

### R-D1: Plancherel-decomposition of A_1 cyclic line

- **Route type:** constructive theorem (V1 attempt extended)
- **Premise:** retained Plancherel support; arg(b)=δ proven inside
  Brannen parameterization. Extend to derive the value δ = 2/9 from the
  cyclic Z_3 orbit on the A_1 line.
- **Why it might land:** V1 closed arg(b)=δ; remaining gap is the
  numerical value.
- **Score:** state-upgrade 3, import-retirement 2, blocker-close 2,
  artifact 2, novelty 2, stretch 3, overclaim risk -1 → **13/18**.

### R-D2: Berry-phase holonomy on cubic Z_3 source rotation

- **Route type:** constructive theorem + holonomy
- **Premise:** if R-Q1 closes, the source-free reduced carrier has a
  natural cyclic Z_3 orbit. The Berry holonomy around this orbit is a
  unique geometric phase; compute it and identify with δ.
- **Why it might land:** Berry holonomy = (2π/N) × (winding) = (2π/3) ×
  (1/3) = 2π/9 ≈ 0.698 rad — close to 2/9 in the Type-B period
  convention.
- **Score:** state-upgrade 3, import-retirement 3, blocker-close 2,
  artifact 2, novelty 3, stretch 3, overclaim risk -1 → **15/18**.

### R-D3: SO(2) phase erasure structural identity

- **Route type:** structural identity
- **Premise:** Q SO(2) phase-erasure support note
  (KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25) establishes the
  phase-erasure mechanism. Evaluate the residual phase as
  δ = (2/N_color)/N_color = 2/9.
- **Why it might land:** if the SO(2) erasure surface is retained, the
  residual phase is a compact algebraic identity.
- **Score:** state-upgrade 3, import-retirement 3, blocker-close 2,
  artifact 2, novelty 2, stretch 2, overclaim risk -1 → **13/18**.

### Selected route for Block 2 (if Q1 lands): R-D2

Berry holonomy is the cleanest and most natural route after Q1. R-D3 is
fallback (ties to retained SO(2) erasure surface).

## Q3: Quark mass-ratio first-principles endpoint chain

### R-M1: derive running-coupling time-scale from gauge-vacuum plaquette

- **Route type:** constructive theorem (atlas reuse)
- **Premise:** retained Wilson reduction-existence + susceptibility-flow +
  connected-hierarchy + spectral-measure theorems. Identify the
  taste-staircase mass time-scale with the Wilson reduction surface.
- **Why it might land:** uses 6+ retained Wilson theorems on the same
  surface; if the time-scale identification is forced, the +15% gap
  closes structurally.
- **Score:** state-upgrade 2, import-retirement 2, blocker-close 1,
  artifact 1, novelty 2, stretch 3, overclaim risk -1 → **10/18**.

### R-M2: structural readout map from Cl(3) mass operator

- **Route type:** constructive theorem
- **Premise:** retained Cl(3) eigenline + source-domain canonical descent
  (Koide V7.3). Apply the same structural readout map to the down-type
  quark mass eigenline.
- **Why it might land:** ties Q3 to Q1 closure; if the readout map is
  universal across mass eigenlines, the same Q-structure governs both.
- **Score:** state-upgrade 3, import-retirement 2, blocker-close 1,
  artifact 1, novelty 3, stretch 2, overclaim risk -1 → **11/18**.

### Selected route for Block 3 (depends on Q1+Q2): R-M2

R-M2 leverages Q1 closure for cross-sector universality. R-M1 fallback.

## Q4: Cl_4(C) module derivation (Axiom* → A_min consequence)

### R-A1: extend cubic + time generator using anomaly-forced 3+1

- **Route type:** constructive theorem
- **Premise:** retained anomaly-forced 3+1 spacetime + retained 3
  cubic generators of `Cl(3)`. Show that the natural extension to time
  forces a 4th anti-commuting generator, which together with `i` from
  Hilbert structure (PHYSICAL_LATTICE_NECESSITY) produces an irreducible
  `Cl_4(C)` module on `P_A H_cell`.
- **Why it might land:** retained 3+1 + retained Cl(3) + retained Hilbert
  i — if these three forces give Cl_4(C), Axiom* is retired.
- **Score:** state-upgrade 3, import-retirement 3, blocker-close 3,
  artifact 2, novelty 3, stretch 3, overclaim risk -1 → **16/18**.

### R-A2: derive `P_A H_cell` from primitive coframe boundary carrier

- **Route type:** constructive theorem (atlas reuse)
- **Premise:** retained PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM
  selects the Hamming-weight-1 packet as `P_A`. Combine with retained
  generation count (3) to fix `H_cell` dimension.
- **Why it might land:** if `H_cell` dimension is structurally fixed by
  retained primitives, the Cl_4(C) module structure is forced.
- **Score:** state-upgrade 3, import-retirement 3, blocker-close 2,
  artifact 2, novelty 2, stretch 2, overclaim risk -1 → **13/18**.

### R-A3: prove no-go that A_min cannot generate Cl_4(C) — minimality theorem

- **Route type:** no-go/obstruction
- **Premise:** if R-A1 and R-A2 both fail, prove explicitly that no
  combination of A_min (Cl(3), Z^3, Grassmann, g_bare=1) generates
  irreducible Cl_4(C) on any quotient. This forces Axiom* adoption as
  the unique minimal extension.
- **Why it might land:** falsifier-grade; gives the Hubble C1 lane an
  exact theorem-grade dependency, even if Axiom* itself remains a
  science decision.
- **Score:** state-upgrade 2, import-retirement 1, blocker-close 3,
  artifact 2, novelty 2, stretch 3, overclaim risk 0 → **13/18**.

### Selected route for Block 4: R-A1

R-A1 has highest expected leverage if the anomaly-forced 3+1 + Cl(3) +
Hilbert i identification works. R-A3 fallback after first stretch.

## Q5: BH 1/4 carrier from framework Wald-Noether charge

### R-B1: derive Wald-Noether charge from retained Universal QG stack

- **Route type:** constructive theorem (atlas reuse)
- **Premise:** retained UNIVERSAL_QG_PL_FIELD_INTERFACE,
  UNIVERSAL_QG_PL_WEAK_FORM, UNIVERSAL_QG_LORENTZIAN_GLOBAL_ATLAS_CLOSURE.
  Show that on this canonical Lorentzian action surface, the Wald-Noether
  charge for a Killing horizon evaluates to `A · c_cell` where `c_cell`
  is the framework's primitive coframe boundary carrier
  (PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM with `c_cell = 1/4`).
- **Why it might land:** the entire chain is on retained surfaces.
- **Score:** state-upgrade 3, import-retirement 2, blocker-close 1,
  artifact 2, novelty 3, stretch 3, overclaim risk -1 → **13/18**.

### R-B2: tighten `c_cell = 1/4` boundary uniqueness on framework primitives

- **Route type:** constructive theorem (atlas reuse)
- **Premise:** retained PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM
  + retained PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM. Show
  `c_cell = 1/4` is forced uniquely by these two theorems together.
- **Why it might land:** mostly atlas-reuse; tight result.
- **Score:** state-upgrade 2, import-retirement 1, blocker-close 1,
  artifact 2, novelty 1, stretch 2, overclaim risk 0 → **9/18**.

### Selected route for Block 5: R-B1

R-B1 has higher cascade leverage. R-B2 tightens existing chain.

## Q6: DM η freezeout-bypass

### R-DM1: derive N_sites from retained generation/Oh order

- **Route type:** constructive theorem
- **Premise:** retained 3-generation count + retained cubic Oh
  automorphism order |Oh| = 48. Test `m_DM = N_sites · v` with N_sites
  from explicit retained graph automorphism counts.
- **Score:** state-upgrade 2, import-retirement 2, blocker-close 1,
  artifact 1, novelty 2, stretch 2, overclaim risk -1 → **9/18**.

### R-DM2: derive m_DM from retained EW v + matter-content count

- **Route type:** constructive theorem
- **Premise:** retained EW v scale + retained matter-content (Q_L + L_L
  catalog). Test direct identification.
- **Score:** state-upgrade 2, import-retirement 2, blocker-close 1,
  artifact 1, novelty 1, stretch 2, overclaim risk -1 → **8/18**.

### Selected route for Block 6: R-DM1

R-DM1 has slightly higher novelty.

## Q7: Plaquette β=6 explicit Perron / boundary

### R-P1: numerical Perron solve on small Z_6^env

- **Route type:** exact runner
- **Premise:** retained transfer-operator / character-recurrence theorem.
  Implement Perron eigenvector solve on small Z_6^env representation.
- **Score:** state-upgrade 2, import-retirement 3, blocker-close 1,
  artifact 3, novelty 1, stretch 2, overclaim risk 0 → **12/18**.

### R-P2: structural analytic identification of Perron state

- **Route type:** constructive theorem (atlas reuse)
- **Premise:** retained spatial-environment tensor-transfer theorem.
  Identify Perron state via Wilson coefficient + SU(3) intertwiner data.
- **Score:** state-upgrade 3, import-retirement 3, blocker-close 1,
  artifact 2, novelty 3, stretch 3, overclaim risk -1 → **14/18**.

### Selected route for Block 7 (if reached): R-P2

R-P2 has higher novelty + atlas reuse strength.

## Stuck fan-out plan

If a route hits a wall, fan out to 3-5 orthogonal premises before declaring
no-go. For each block:

- **Block 1 (Q1):** if R-Q1 walls → fan out to R-Q2, R-Q3, plus orthogonal
  attempts: (a) Cl(3) Pauli triple cyclic permutation invariant;
  (b) `SU(2) ⊂ Cl(3)` rotation-invariant ratio.
- **Block 2 (Q2):** if R-D2 walls → R-D1, R-D3, plus (a) cyclic Wilson
  loop closure; (b) Z_3 character-table residue.
- **Block 4 (Q4):** if R-A1 walls → R-A2, R-A3, plus (a) graph-first
  selector + cubic time edge; (b) anomaly trace catalog forced
  representation.
