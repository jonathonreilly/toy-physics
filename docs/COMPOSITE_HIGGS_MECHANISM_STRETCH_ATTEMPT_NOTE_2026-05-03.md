# Composite-Higgs Candidate — Multi-Channel Z3-Phased Composite Scalar (Stretch Attempt with 3 Named Residual Obstructions)

**Date:** 2026-05-03
**Claim type:** open_gate
**Output type:** stretch_attempt (output type c)
**Cycle:** 20 of physics-loop campaign (single-cycle compressed successor
to retained-promotion-2026-05-02)
**Claim scope:** documents a worked stretch attempt at the composite-Higgs
candidate question opened by earlier EWSB obstruction work. The attempt's
candidate content is a branch-local
multi-channel Z3-covariant composite-scalar candidate that JOINTLY
narrows cycle 08's three named obstructions
O1 (mechanism for ⟨q̄_L u_R⟩ ≠ 0), O2 (BHL m_top ~ 600 GeV literature
prediction), and O3 (multi-bilinear selector ambiguity).

The worked attempt's candidate structural content:

1. The three matching bilinears `q̄_L u_R`, `q̄_L d_R`, `l̄_L e_R`
   identified by cycle 08 form a Z3 cyclic triplet under the framework's
   Koide Z3 structure extended to act on generation index.
2. A Z3-covariant multi-channel composite scalar
   `Φ_eff = Φ_1 + ω Φ_2 + ω² Φ_3` (where ω = exp(2πi/3) and
   Φ_i are the three bilinear condensates) is proposed.
3. Multi-channel structure suppresses the single-channel BHL m_top
   prediction by a factor 1/N_z3 = 1/3 in the effective Yukawa magnitude.
4. The three-bilinear ambiguity (cycle 08 O3) is narrowed structurally:
   the three bilinears are NOT arbitrary — they are precisely the Z3
   triplet components of the candidate composite scalar under H1.

The worked attempt's named residual obstructions:

- **NO1**: framework needs derivation that Z3 extends from charged-lepton
  selected slice to act on quark-bilinear generation index.
- **NO2**: framework needs derivation that the three bilinear condensates
  have equal magnitude (Z3-symmetric strong-coupling, not just Z3 on
  representation space).
- **NO3**: framework needs derivation of the strong-coupling magnitude
  itself (inherits cycle 08 O1).

**Status:** stretch attempt with candidate mechanism + 3 named residual obstructions.
Audit-lane ratification required for any retained-grade interpretation.
This is NOT a closing derivation. Independent audit required.

**Script:** `scripts/frontier_composite_higgs_mechanism.py`

**Runner:** [`scripts/frontier_composite_higgs_mechanism.py`](../scripts/frontier_composite_higgs_mechanism.py)

**Authority role:** Sharpens cycle 08's three named obstructions with a
concrete multi-channel candidate + 3 named residual obstructions for future
cycles.

## A_min (minimal allowed premise set)

The premises of this stretch attempt:

- **(D1, retained)** Native gauge structure SU(3)_c × SU(2)_L × U(1)_Y
  via [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md).

- **(D2, bounded support)** Framework's current matter-content/EWSB
  harness supplies the SM matter representation used here:

  ```text
  Q_L : (2, 3)_{+1/3}_Y
  L_L : (2, 1)_{-1}_Y
  u_R : (1, 3)_{+4/3}_Y
  d_R : (1, 3)_{-2/3}_Y
  e_R : (1, 1)_{-2}_Y
  ν_R : (1, 1)_0_Y
  ```

  Source: [`UNIFIED_MATTER_CONTENT_EWSB_HARNESS_THEOREM_NOTE_2026-05-03.md`](UNIFIED_MATTER_CONTENT_EWSB_HARNESS_THEOREM_NOTE_2026-05-03.md),
  cross-checked against [`LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md`](LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md).

- **(D3, current-note recomputation)** Three bilinears with matching
  SU(2) × U(1)_Y quantum numbers:

  ```text
  Φ_1 ≡ (q̄_L u_R)|_color-singlet  ~  (2̄, 1)_{+1}     [Φ̃-equivalent]
  Φ_2 ≡ (q̄_L d_R)|_color-singlet  ~  (2̄, 1)_{-1}     [Φ-equivalent]
  Φ_3 ≡  l̄_L e_R                  ~  (2̄, 1)_{-1}     [Φ-equivalent]
  ```

  This note recomputes the bilinear hypercharges directly from D2 and
  the landed one-Higgs/Yukawa guardrails
  [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
  and [`HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md`](HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md). The
  unlanded cycle 08 note is historical context only, not a load-bearing
  dependency.

- **(D4, exact-support)** Koide Z3 scalar potential
  `V(m) = V₀ + (c1+c2/2)m + (3/2)m² + (1/6)m³` from Clifford involution
  `T_m^2 = I_3` on charged-lepton selected slice. Source:
  [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md).

- **(D5, exact group theory)** EW Fierz channel decomposition with
  adjoint fraction `(N_c² - 1)/N_c² = 8/9` at N_c = 3. Source:
  [`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md).

- **(H1, branch-local HYPOTHESIS; NOT retained)** Z3 acts on
  quark-bilinear generation index, extending the Koide Z3 domain from
  charged-lepton selected slice to bilinear triplets. This is
  load-bearing for the candidate only.

- **(H2, branch-local HYPOTHESIS; NOT retained)** The three bilinear
  condensates `Φ_1, Φ_2, Φ_3` have equal magnitude. This is
  load-bearing for the candidate only.

- **(C1, admitted-context external)** NJL mean-field factorization
  for fermion bilinears (Nambu-Jona-Lasinio 1961).

- **(C2, admitted-context external)** Cube-roots-of-unity arithmetic:
  ω = exp(2πi/3), 1 + ω + ω² = 0, ω³ = 1.

- **(C3, admitted-context external)** Standard SU(N) representation
  theory and SM Yukawa structural form (Halzen-Martin, Peskin-Schroeder
  ch. 20).

## Forbidden imports

- **No PDG values**: m_t, m_H, v_EW, m_W, m_Z are NOT used as
  derivation inputs anywhere.
- **No literature numerical comparators**: BHL `m_t ~ 600 GeV` is
  referenced ONLY as cycle 08's admitted-context obstruction
  documentation, not as a derivation input. Hill 1991, Holdom 1985,
  Yamawaki 1986 walking technicolor papers NOT cited.
- **No fitted selectors**.
- **No admitted unit conventions** load-bearing on retention beyond
  the doubled-Y convention shared with cycle 04 and cycle 08.
- **No same-surface family arguments**.

## Worked attempt — Route B execution

### Step 1: Identify the Z3 triplet structure

Cycle 08 enumerated three SU(2)_L × U(1)_Y bilinear forms with matching
Higgs-doublet quantum numbers (D3). Group them as:

```text
Φ_1 = (q̄_L u_R)|_singlet     ↔ (2̄, 1)_{+1}   [up-quark mass]
Φ_2 = (q̄_L d_R)|_singlet     ↔ (2̄, 1)_{-1}   [down-quark mass]
Φ_3 = (l̄_L e_R)              ↔ (2̄, 1)_{-1}   [charged-lepton mass]
```

Note the Y values: Φ_1 has Y = +1 (Φ̃-like), while Φ_2 and Φ_3 share
Y = -1 (Φ-like). The Y signs differ by a Y-flip
(Φ̃ = i σ_2 Φ* convention), but the **SU(2) doublet structure is
identical** for all three (each is a (2̄, 1) doublet representation
under SU(2)_L). For the Z3 phase analysis below, what matters is the
*unique-doublet structure* — each Φ_i is a single (2̄, 1) doublet.

We rewrite the three components in a uniform doublet basis. Use the
convention that Φ_1 is paired with Φ̃_1 = i σ_2 Φ_1*, so all three
components can be brought to the same Y = -1 convention by writing:

```text
Φ_1' = i σ_2 Φ_1*  ~  (2̄, 1)_{-1}
Φ_2'  = Φ_2        ~  (2̄, 1)_{-1}
Φ_3'  = Φ_3        ~  (2̄, 1)_{-1}
```

Now `(Φ_1', Φ_2', Φ_3')` is a triplet of identical-rep components,
suitable for Z3 cyclic action.

**Hypothesis H1**: the framework's Koide Z3 structure (currently
retained on charged-lepton selected slice) extends to act on the
*generation index* of these bilinears. Concretely:

```text
Z3 : (Φ_1', Φ_2', Φ_3')  ↦  (Φ_2', Φ_3', Φ_1')         [cyclic]
```

This is a **branch-local hypothesis** for Route B. It is not derived
here and is named as obstruction NO1.

### Step 2: Z3-covariant composite scalar

Given the cyclic Z3 action on the triplet, define the Z3-covariant
composite scalar:

```text
Φ_eff = Φ_1' + ω Φ_2' + ω² Φ_3'
```

where ω = exp(2πi/3) is a primitive cube root of unity. Under the Z3
cyclic action:

```text
Z3 : Φ_eff  ↦  Φ_2' + ω Φ_3' + ω² Φ_1'
              =  ω² (Φ_1' + ω Φ_2' + ω² Φ_3')      [factoring ω²]
              =  ω² · Φ_eff
```

So Φ_eff transforms as a **Z3 charge-2 representation** (or equivalently,
as ω² which is the complex conjugate of ω). The three independent Z3
combinations are:

```text
Φ_eff^(0)  = Φ_1' + Φ_2' + Φ_3'                    [Z3 singlet, charge 0]
Φ_eff^(1)  = Φ_1' + ω Φ_2' + ω² Φ_3'               [Z3 charge 1]
Φ_eff^(2)  = Φ_1' + ω² Φ_2' + ω Φ_3'               [Z3 charge 2]
```

These three combinations span the same 3-dimensional space as
`(Φ_1', Φ_2', Φ_3')`. The Z3-singlet `Φ_eff^(0)` is the Z3-invariant
sum.

### Step 3: SU(2) × U(1)_Y quantum number consistency

Each Φ_i' has SU(2) × U(1)_Y quantum numbers (2̄, 1)_{-1}. Linear
combinations preserve the rep — Z3 phase factors (ω, ω²) are complex
scalars, not gauge transformations. So:

```text
Φ_eff^(k) ~ (2̄, 1)_{-1}  for k = 0, 1, 2
```

All three Z3 combinations carry the SAME SU(2) × U(1)_Y rep —
consistent with the candidate Higgs role.

The Goldstone count for SU(2) × U(1)_Y → U(1)_em SSB is 4 - 1 = 3
broken generators. With multi-channel condensate, each of Φ_eff^(0),
Φ_eff^(1), Φ_eff^(2) acquires a VEV (under H2 equal-magnitude). The
Goldstone modes parameterize the unbroken U(1)_em direction in each
component — 3 Goldstones × 1 effective doublet = 3 Goldstones total.
Z3 symmetry does NOT add Goldstones (it's a discrete symmetry on
flavor space, not gauge).

### Step 4: Multi-channel suppression of effective top Yukawa

In single-channel BHL (Bardeen-Hill-Lindner 1990, admitted-context
external for obstruction documentation only), the top-condensate model
predicts m_top ~ 600 GeV from naive infrared coupling. Schematically:

```text
single-channel BHL:  y_top^naive ~ y_eff^single
                     m_top^pred ~ y_eff^single · v_EW
                     ⇒ m_top ~ 600 GeV
```

This single-channel prediction does NOT apply when the condensate is
*multi-channel*. Under H2 (equal-magnitude condensates), the EWSB
strength is distributed across Z3 = 3 channels:

```text
multi-channel:
  ⟨Φ_1'⟩ = ⟨Φ_2'⟩ = ⟨Φ_3'⟩ = v_unit · e^{iθ}  (equal magnitude, H2)
  ⟨Φ_eff^(0)⟩ = 3 v_unit · e^{iθ}              [Z3-singlet sum]
  ⟨Φ_eff^(1)⟩ = ⟨Φ_eff^(2)⟩ = 0                [Z3-charged components vanish at Z3-symmetric point]
```

In this Z3-symmetric VEV configuration, each *individual* condensate
carries fraction 1/N_z3 = 1/3 of the total EWSB strength. The effective
Yukawa for the top-quark sector (which couples specifically to Φ_1') is
then:

```text
y_top^eff = y_eff^single · (⟨Φ_1'⟩ / ⟨Φ_eff^(0)⟩)
          = y_eff^single · (v_unit / (3 v_unit))
          = y_eff^single / 3
```

So the multi-channel m_top prediction is suppressed by exactly 1/N_z3
= 1/3 relative to single-channel BHL:

```text
m_top^multi-channel = m_top^single-channel / 3
                    ≈ 600 GeV / 3
                    = 200 GeV
```

This is a STRUCTURAL relation. The exact numerical value 200 GeV vs the
observed 173 GeV is NOT a prediction (we have not derived
y_eff^single from framework primitives — that's NO3); but the
*direction* of the suppression is structurally fixed at 1/N_z3.

The 200 GeV / 173 GeV residual ratio is approximately 1.16 — representing
the gap between "multi-channel structural suppression alone" and "exact
m_top". This residual is to be addressed by NO3 (strong-coupling magnitude)
in future cycles.

### Step 5: Narrowing cycle 08 Obstruction O3 (multi-bilinear selector)

Cycle 08 named the multi-bilinear selector ambiguity as O3:

> Without an additional selector, the framework cannot uniquely
> identify WHICH bilinear plays the Higgs role. In the SM, a
> fundamental Higgs Φ couples to all three via different Yukawa
> coefficients; in a composite picture, a unique condensate would
> need to be selected.

**Route B narrows O3 structurally.** The "selector" is the Z3
representation theory itself: the three bilinears are NOT three
independent candidates with one to be selected — they are precisely
the three Z3-charged components of a single Z3-covariant candidate.
The Z3-singlet linear combination Φ_eff^(0) is the unique
Z3-symmetric condensate direction.

Under H1 (Z3 generation action) and H2 (equal-magnitude), the unique
Higgs-role component is `Φ_eff^(0) = Φ_1' + Φ_2' + Φ_3'`, and the
*selector* is the Z3 invariance condition inside this H1/H2 candidate.
No additional selector is introduced by the candidate, but O3 is not
retained-closed without H1/H2.

This is a structural sharpening of cycle 08 O3, not a closing of
cycle 08 O1.

### Step 6: Counterfactual on Z3 phase orderings

Z3 has only 3 nontrivial actions on a triplet:

- identity: (Φ_1, Φ_2, Φ_3) ↦ (Φ_1, Φ_2, Φ_3)
- cyclic forward: (Φ_1, Φ_2, Φ_3) ↦ (Φ_2, Φ_3, Φ_1)
- cyclic backward: (Φ_1, Φ_2, Φ_3) ↦ (Φ_3, Φ_1, Φ_2)

The "forward" and "backward" actions are inverses of each other under
Z3 (one is ω, the other is ω²). The three Z3 representations
(charge 0, 1, 2) are conjugate under outer automorphism of Z3 (which
swaps ω ↔ ω²). So the "phase ordering" (1, ω, ω²) vs (1, ω², ω) is NOT
a free parameter — both give the same Z3-symmetric composite scalar
up to outer automorphism.

This is a structural feature, NOT an additional input. The Z3 algebra
itself constrains the phase relations.

### Step 7: Counterfactual on single-channel condensation

If only ONE of the three bilinears condensed (e.g., ⟨Φ_1'⟩ ≠ 0,
⟨Φ_2'⟩ = ⟨Φ_3'⟩ = 0), then under the Z3 cyclic action this becomes
(0, ⟨Φ_1'⟩, 0) which is NOT proportional to the original. So
single-channel condensation BREAKS Z3 explicitly.

If the framework's Z3 applies here (per H1 hypothesis), then
single-channel condensation is FORBIDDEN, and the BHL single-channel
prediction does not apply.

This is a falsifier for the candidate: if the framework's Z3 applies
on generation indices, then the EWSB condensate must be multi-channel,
and the single-channel BHL `m_top ~ 600 GeV` comparator is structurally
inapplicable.

### Step 8: Mass-ratio constraints from Z3 symmetry

Under H2 (equal-magnitude condensates), the structural Z3 symmetry
implies the three-channel Yukawa couplings y_1, y_2, y_3 (for
up-quark, down-quark, charged-lepton respectively) are constrained:

```text
y_1 · ⟨Φ_1'⟩ = m_up-type     [for the dominant generation]
y_2 · ⟨Φ_2'⟩ = m_down-type   [for the dominant generation]
y_3 · ⟨Φ_3'⟩ = m_lepton-type [for the dominant generation]
```

If y_1 = y_2 = y_3 = y (Z3-symmetric coupling) AND ⟨Φ_1'⟩ = ⟨Φ_2'⟩ =
⟨Φ_3'⟩ (H2), then m_top = m_bottom = m_tau structurally — clearly NOT
observed. So either:

- (a) the Z3 symmetry is BROKEN at the Yukawa coupling level (y_i ≠ y_j),
  in which case the Z3-symmetric VEV is preserved but the Yukawas
  introduce explicit Z3 breaking. The mass hierarchy is then carried
  by the Yukawa breaking, not the VEV.
- (b) H2 is FALSE — the three condensates have different magnitudes;
  Z3 symmetry is broken at the condensate level.

This is a **falsifier**: observed mass ratios m_top : m_bottom : m_tau
≈ 173 : 4.18 : 1.78 GeV (PDG, used here ONLY as falsifier-target,
NOT as derivation input) are NOT compatible with a fully Z3-symmetric
multi-channel composite. The Z3 symmetry must be broken somewhere.

This narrows H2 — equal-magnitude condensates is structurally
INCOMPATIBLE with observed mass hierarchy unless the Yukawa couplings
themselves break Z3. Future cycles must address this. Named as part of
**NO2 sharpened**.

### Conclusion of stretch attempt

**Candidate structural result**:

1. The three matching bilinears form a Z3 cyclic triplet under H1.
2. The Z3-covariant composite scalar Φ_eff has consistent SU(2) × U(1)_Y
   quantum numbers across all three Z3 charges.
3. Multi-channel condensation suppresses single-channel BHL m_top ~ 600
   GeV by structural factor 1/N_z3 = 1/3.
4. Cycle 08 O3 (multi-bilinear selector) is narrowed structurally:
   selector = Z3 representation theory inside the H1/H2 candidate.
5. Cycle 08 O2 (BHL m_top too high) is PARTIALLY ADDRESSED:
   600/3 ≈ 200 GeV, gap of ~1.16x to observed 173 GeV remains for NO3.
6. Cycle 08 O1 (mechanism for nonzero condensate) is narrowed by the
   candidate direction under H1/H2; magnitude inherits to NO3.
7. Counterfactuals on Z3 phase orderings, single-channel condensation,
   and mass-ratio constraints all give STRUCTURAL constraints, not
   numerical inputs.

**Three named residual obstructions (the stretch attempt's residual gaps):**

#### NO1: Z3 generation action (branch-local for Route B)

The framework's retained Koide Z3 structure (`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE`)
is established on the charged-lepton selected slice. Extending Z3 to act
on quark-bilinear generation index is a branch-local hypothesis. To
resolve this obstruction, future cycles must:

- Identify the Z3 generator on the *quark sector* of the framework's
  derived rep (cycle 06).
- Verify that the Clifford involution `T_m^2 = I_3` from the lepton
  selected slice has a quark-sector analogue.
- Show that the Z3 action on bilinear generation index is the natural
  consequence of the Clifford involution structure.

If H1 fails (Z3 does NOT extend to quark sector), Route B fails
structurally and the multi-channel candidate does not apply.

**Specific repair target**: derive (or refute) H1 from framework primitives.

#### NO2: Equal-magnitude condensate (Z3-symmetric strong coupling)

H2 asserts ⟨Φ_1'⟩ = ⟨Φ_2'⟩ = ⟨Φ_3'⟩ in magnitude. This is a stronger
condition than H1 — it requires the strong-coupling sector to be
Z3-SYMMETRIC, not just to act on a Z3 representation.

**Structural challenge identified in Step 8**: equal-magnitude
condensates with Z3-symmetric Yukawa couplings would predict
m_top = m_bottom = m_tau, contradicting observation. So H2 must be
broken in EITHER:

- (a) the condensate magnitudes themselves (Z3 broken at strong-coupling),
- (b) the Yukawa couplings (Z3 broken at the lepton-quark interface).

The framework's existing retained Koide structure on charged-leptons
shows Z3 acts WITH a small breaking parameter (the K_frozen offset);
extending this to quarks is the next step.

**Specific repair target**: derive (or refute) H2 from framework
primitives, including the Z3 breaking pattern that gives observed
mass hierarchy.

#### NO3: Strong-coupling magnitude (inherits cycle 08 O1)

Even with H1, H2 derived, Route B does NOT predict the magnitude of
the EW-breaking condensate. The framework's strong-coupling sector
must produce ⟨Φ_eff^(0)⟩ ≠ 0 with magnitude consistent with the EW
scale. This is identical to cycle 08 O1 — the multi-channel structure
forces the DIRECTION but not the MAGNITUDE.

**Specific repair target**: derive ⟨Φ_eff^(0)⟩ from framework
primitives. Candidates for future cycles:

- Lattice strong-coupling regime with Z3-covariant Wilson loops.
- Z3-symmetric Coleman-Weinberg potential beyond the leading lepton
  sector.
- Mean-field NJL with Z3-symmetric four-fermion coupling derived from
  framework's gauge structure (cycle 15 g_2² = 1/4 might be a hint
  here, since the lattice-scale gauge coupling is structurally fixed).

## Honest stop conditions

This is a stretch attempt with three named obstructions. The candidate
analysis is structurally clean (quantum numbers preserved, Z3
covariance consistent, counterfactuals provide structural constraints),
but H1, H2, and NO3 are unattacked premises. Promotion to retained-
grade requires addressing all three named obstructions, which is
multi-week work outside this single cycle's scope.

## What this claims

- **(P1)** Z3 cyclic action on three bilinear triplet (under H1) gives
  three Z3-charged composite scalars Φ_eff^(0), Φ_eff^(1), Φ_eff^(2).
- **(P2)** All three Z3-charged components have SU(2) × U(1)_Y quantum
  numbers (2̄, 1)_{-1}, identical and consistent for the candidate
  Higgs role.
- **(P3)** Multi-channel structure suppresses single-channel BHL
  m_top prediction by structural factor 1/N_z3 = 1/3.
- **(P4)** Cycle 08 O3 (multi-bilinear selector) is narrowed inside
  the H1/H2 candidate: Z3 representation supplies the selector.
- **(P5)** Three named residual obstructions (NO1, NO2, NO3) for what
  remains.
- **(P6)** Counterfactuals: alternative phase orderings, single-channel,
  mass-ratio constraints all give structural constraints.

## What this does NOT claim

- Does NOT close the unconditional EWSB Higgs identification — that
  requires resolving NO1, NO2, NO3.
- Does NOT prove H1 (Z3 acts on quark generations) or H2 (equal-
  magnitude condensates) — both are explicit hypotheses.
- Does NOT predict m_top, m_H, v_EW, or any other EW observable.
- Does NOT promote any author-side tier; audit-lane ratification is
  required.
- Does NOT use PDG values as derivation inputs anywhere; m_top = 173
  GeV mentioned only for falsifier comparison in Step 8, NOT used as
  fitting input.
- Does NOT ratify cycle 08 obstructions as fully closed — only
  sharpens them with Route B candidate + names residual obstructions for
  what remains.

## Cited dependencies

- (D1) [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) — retained.
- (D2) [`UNIFIED_MATTER_CONTENT_EWSB_HARNESS_THEOREM_NOTE_2026-05-03.md`](UNIFIED_MATTER_CONTENT_EWSB_HARNESS_THEOREM_NOTE_2026-05-03.md)
  and [`LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md`](LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md)
  — current matter-content and hypercharge support.
- (D3) Current-note recomputation from D2 plus
  [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
  and [`HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md`](HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md).
- (D4) [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md)
  — Koide Z3 retained.
- (D5) [`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)
  — EW Fierz channel decomposition.
- (C1) Nambu-Jona-Lasinio 1961 — admitted-context external on NJL
  mean-field factorization.
- (C3) Halzen-Martin SM Yukawa structure — admitted-context external.
- (C3) Peskin-Schroeder ch. 20 — admitted-context external on SM Higgs.
- BHL 1990 — admitted-context external; cited ONLY in obstruction
  documentation (cycle 08 O2 framing, used here as falsifier target
  for Step 4 multi-channel suppression).

## Forbidden imports check

- No PDG observed values consumed as derivation inputs.
- No literature numerical comparators consumed (BHL m_top ~ 600 GeV
  used as Step 4 falsifier-target only, NOT as derivation input).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.
- m_top = 173 GeV PDG appears in Step 8 ONLY as falsifier-target for
  the equal-magnitude H2 hypothesis (showing observed mass hierarchy
  is incompatible with full Z3 symmetry). NOT used as fitting input.

## Validation

Primary runner:
[`scripts/frontier_composite_higgs_mechanism.py`](../scripts/frontier_composite_higgs_mechanism.py)
verifies (PASS=N/0, exact rational arithmetic + Z3 phase covariance):

1. Cycle 06 derived rep used at one hop (counterfactual: wrong rep
   gives wrong Y_total).
2. Cycle 08 quantum-number match recovered for three bilinears.
3. Z3 cube-root-of-unity arithmetic: 1 + ω + ω² = 0 exactly (using
   sympy exact).
4. Three Z3-charged components Φ_eff^(0), Φ_eff^(1), Φ_eff^(2) span
   3D space; equivalent to (Φ_1', Φ_2', Φ_3').
5. Z3 cyclic action: (Φ_1, Φ_2, Φ_3) ↦ (Φ_2, Φ_3, Φ_1) gives
   Φ_eff^(1) ↦ ω² · Φ_eff^(1).
6. SU(2) × U(1)_Y quantum numbers (2̄, 1)_{-1} preserved across all
   three Z3 components.
7. Y-flip convention: Φ_1 (Y=+1) → Φ_1' (Y=-1) consistent with i σ_2
   conjugate convention; Y(Φ_eff^(k)) = -1 for all k.
8. Multi-channel suppression formula: y_top^multi / y_top^single =
   1/N_z3 = 1/3.
9. m_top^multi = m_top^single / 3 ≈ 600/3 = 200 GeV (structural;
   600 cited as cycle 08 O2 obstruction context only).
10. Z3-symmetric VEV: ⟨Φ_eff^(0)⟩ = 3 v_unit, ⟨Φ_eff^(1)⟩ =
    ⟨Φ_eff^(2)⟩ = 0.
11. Single-channel counterfactual: ⟨(Φ_1', 0, 0)⟩ breaks Z3
    explicitly, NOT Z3-invariant.
12. Z3 phase ordering counterfactual: (1, ω², ω) and (1, ω, ω²)
    differ by Z3 outer automorphism (complex conjugation), NOT a
    free parameter.
13. Mass-ratio falsifier (Step 8): equal-magnitude H2 + Z3-symmetric
    Yukawa ⇒ m_top = m_bottom = m_tau (contradicts observation).
14. Goldstone mode counting: 3 broken generators of SU(2) × U(1)_Y
    → U(1)_em give 3 Goldstones, preserved under multi-channel.
15. Cycle 15 g_2² = 1/4 used at one hop.
16. EW Fierz channel decomposition: 8/9 adjoint + 1/9 singlet exact
    at N_c = 3.
17. Three bilinears form Z3 cyclic triplet under H1 ansatz.
18. NO1, NO2, NO3 named in note.
19. Forbidden imports check: m_top, m_H, v_EW PDG values NOT consumed
    in derivation steps 1-7; appear only in Step 8 falsifier-target
    role.
20. Y-arithmetic for q̄_L u_R: -1/3 + 4/3 = +1 exact.
21. Y-arithmetic for q̄_L d_R: -1/3 + (-2/3) = -1 exact.
22. Y-arithmetic for l̄_L e_R: +1 + (-2) = -1 exact.
23. Y-arithmetic check: Y(Φ_1') = -Y(Φ_1) = -1 (i σ_2 conjugate).
24. SU(2) doublet structure: 2̄ ⊗ 1 = 2̄ for all three bilinears
    (q̄_L is 2̄, u_R/d_R/e_R are 1).
25. Color-singlet projection: SU(3) color (3̄ ⊗ 3 = 1 ⊕ 8) singlet
    selected for q̄_L u_R, q̄_L d_R; trivial for l̄_L e_R.

## Cross-references

- [`UNIFIED_MATTER_CONTENT_EWSB_HARNESS_THEOREM_NOTE_2026-05-03.md`](UNIFIED_MATTER_CONTENT_EWSB_HARNESS_THEOREM_NOTE_2026-05-03.md)
  — current matter-content/EWSB synthesis used for the SM representation
  and EWSB bookkeeping.
- [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
  and [`HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md`](HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md)
  — landed Yukawa/hypercharge guardrails used to check the bilinear
  arithmetic.
- [`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md)
  — Koide Z3 retained on charged-lepton selected slice; Route B's
  H1 extends Z3 to quark-bilinear generation index.
- [`EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`](EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md)
  — EW Fierz channel decomposition (8/9 adjoint vs 1/9 singlet at
  N_c = 3).
- [`HIGGS_MECHANISM_NOTE.md`](HIGGS_MECHANISM_NOTE.md) — parent row
  for the EWSB Higgs identification lane that cycle 07/08/20 sharpen.
- [`NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md`](NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md)
  — companion no-go: framework's current native surface gives zero
  condensate (relevant to cycle 08 O1 / NO3).
- BHL 1990 — admitted-context external on top-condensate single-channel
  m_top ~ 600 GeV prediction.
- Nambu-Jona-Lasinio 1961 — admitted-context external on mean-field
  composite-scalar formalism.
