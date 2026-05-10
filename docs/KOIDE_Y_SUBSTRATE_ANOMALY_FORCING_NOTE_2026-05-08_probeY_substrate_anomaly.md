# Probe Y-Substrate-Anomaly — Anomaly Cancellation as Substrate-to-Carrier Forcing: Bounded Mostly-Negative Probe

**Date:** 2026-05-10
**Claim type:** bounded_theorem (mostly negative; positive retentions on
already-closed sub-rows)
**Status authority:** independent audit lane only; effective status is
pipeline-derived. This is a source-note proposal; the audit lane has full
authority to retag, narrow, or reject the proposed bounded label.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent audit
lane. The author does NOT propose retained / positive_theorem promotion.

**Primary runner:** [`scripts/cl3_koide_y_substrate_anomaly_2026_05_08_probeY_substrate_anomaly.py`](../scripts/cl3_koide_y_substrate_anomaly_2026_05_08_probeY_substrate_anomaly.py)
**Cached output:** [`logs/runner-cache/cl3_koide_y_substrate_anomaly_2026_05_08_probeY_substrate_anomaly.txt`](../logs/runner-cache/cl3_koide_y_substrate_anomaly_2026_05_08_probeY_substrate_anomaly.txt)

## 0. Probe context

The substrate-to-carrier forcing direction of the Cl(3)/Z^3 framework asks
whether the substrate (`Cl(3)` local algebra + `Z^3` spatial substrate) is
sufficient to FORCE the Standard Model carrier sector content (quark colour
multiplicity `N_c = 3`, lepton/quark partitioning of left-handed doublets,
three generations, the hypercharge assignments
`(Q_L : +1/3, L_L : -1, u_R^c : -4/3, d_R^c : +2/3, e_R^c : +2, nu_R^c : 0)`).
The "hidden-character delta = 0" admission, in the substrate-to-carrier sense,
is the claim that the carrier sector inherits the substrate's hidden character
without external choice.

Earlier substrate-to-carrier probes attacked this directly:
- Symmetry decomposition ([SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md](SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md))
  found 17 rank-four equivariant projector classes — symmetry alone insufficient.
- Variational/orientation principles
  ([PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md](PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md))
  give a positive route conditional on staggered-Dirac action source.
- Reflection-positivity OS Cauchy-Schwarz
  ([PLANCK_SUBSTRATE_TO_CARRIER_FORCING_BOUNDED_NOTE_2026-05-10_planckP1.md](PLANCK_SUBSTRATE_TO_CARRIER_FORCING_BOUNDED_NOTE_2026-05-10_planckP1.md))
  selects `P_A` uniquely under cited RP.

The Planck-side hidden-character `delta = 0` admission was closed positively in
[`PLANCK_HIDDEN_CHARACTER_DELTA_ZERO_POSITIVE_THEOREM_NOTE_2026-05-10_planckP2.md`](PLANCK_HIDDEN_CHARACTER_DELTA_ZERO_POSITIVE_THEOREM_NOTE_2026-05-10_planckP2.md)
via the source-free state mechanism — but that closes the *Planck normalization*
delta, not the broader carrier-sector hidden character.

This probe asks the *separate* question:

> **Question (Probe Y).** Can **gauge anomaly cancellation** (perturbative
> ABJ anomalies plus the nonperturbative SU(2) Witten Z_2 parity), applied
> as a structural constraint on the framework's potential carrier sector,
> FORCE the SM carrier content from substrate alone? Specifically: does
> anomaly cancellation alone fix `N_c = 3`, the three-generation count,
> the LH/RH partitioning into `Q_L, L_L, u_R, d_R, e_R, nu_R`, and the
> SM hypercharge assignments?

The hypothesis under test is that anomaly cancellation is a structural
sufficient condition that converts the carrier sector inputs from "retained
admissions" into "derived outputs," closing the substrate-to-carrier
hidden-character bundle.

## 1. Theorem (bounded, mostly negative; positive retentions on
already-closed sub-rows)

**Theorem (Y-Substrate-Anomaly; bounded).** On retained Cl(3)/Z^3 content,
gauge anomaly cancellation alone does NOT force the full SM carrier sector
content from substrate-only structure. Anomaly cancellation forces:

1. **(Y-Pos-1) RH hypercharges from LH content (already-positive).** Given
   the retained LH content `Q_L : (3, 2)_{1/3} + L_L : (1, 2)_{-1}`, the
   SU(2)-singlet right-handed completion `u_R^c, d_R^c, e_R^c, nu_R^c`
   is uniquely fixed at `(-4/3, +2/3, -2, 0)` by perturbative anomaly
   cancellation `Tr[Y] = Tr[SU(3)^2 Y] = Tr[Y^3] = 0` plus the neutrality
   input `Y(nu_R^c) = 0`. **This is the existing positive theorem
   `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24`.**
   Probe Y does not strengthen this row; it cites it as the positive
   anomaly-forcing already on the retained surface.
2. **(Y-Pos-2) RH SU(3) representation from Q_L (already-positive).** The
   anomaly-cancelling RH (anti-)quark content is forced to be exactly two
   LH-Weyl 3̄ singlets by SU(3)^3 cubic anomaly cancellation against
   `Q_L` (which contributes `+2`); see
   [`SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md`](SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md).
   Probe Y cites this as a second positive anomaly-forcing.
3. **(Y-Pos-3) 3+1 spacetime signature (conditional, already-bounded).**
   Anomaly cancellation conditionally forces 3+1 spacetime signature on
   the cited Cl(3) chiral-gauge structure, per
   [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md).
   Probe Y cites this as the third positive anomaly-forcing on the
   retained surface.

Anomaly cancellation does NOT force, on the retained Cl(3)/Z^3 substrate
alone:

4. **(Y-Neg-A) `N_c = 3` quark colour multiplicity.** Anomaly cancellation
   constraints are agnostic to the choice `N_c`: any `N_c ≥ 2` with
   appropriately rescaled charges admits an anomaly-free assignment.
   Specifically, the linear (gravitational), mixed (`Tr[SU(3)^2 Y]`),
   and cubic (`Tr[Y^3]`) anomaly traces depend on `N_c` polynomially
   but admit cancelling solutions for any `N_c ≥ 2`. The choice
   `N_c = 3` is forced not by anomaly cancellation but by the
   GRAPH_FIRST_SU3_INTEGRATION decomposition of the bipartite-cube
   selected-axis `gl(3) ⊕ gl(1)` commutant ([`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)).
5. **(Y-Neg-B) Three-generation count.** Anomaly cancellation is linear
   in generation count: if one generation is anomaly-free, then `n_gen`
   generations are anomaly-free for any positive integer `n_gen`. The
   SU(2) Witten Z_2 parity constraint requires only `n_gen × N_D ≡ 0
   mod 2` where `N_D = 4` per generation (3 colours of `Q_L` + 1 `L_L`),
   so any `n_gen ∈ Z_{≥1}` satisfies the parity. The choice `n_gen = 3`
   is forced not by anomaly cancellation but by the THREE_GENERATION
   `hw=1 ≅ C^3` exact orbit structure ([`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)).
6. **(Y-Neg-C) LH content choice (Q_L, L_L vs alternatives).** Anomaly
   cancellation is satisfied by infinitely many LH content choices, not
   only by `Q_L + L_L`. Vectorlike pairs `(R + R̄)` of any SU(2)/SU(3)
   irreps cancel all anomalies trivially; chiral content like
   B-L extensions, fourth families with full RH completion, and SU(5)
   GUT 5̄+10 also cancel. The LH choice is forced not by anomaly
   cancellation but by the LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO
   structural ratio plus the LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION
   chain.
7. **(Y-Neg-D) Hypercharge absolute scale.** Anomaly cancellation closes
   only the **ratio** structure. The absolute normalization `Y(L_L) = -1`
   (or equivalently `α = +1/3` in `Y_α = α(P_sym − 3 P_anti)`) is fixed
   by an explicit labelling convention, not derived from anomaly
   cancellation; see [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
   and [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md).
   Anomaly cancellation alone preserves the convention freedom.
8. **(Y-Neg-E) Generation-flavor structure on hw=1.** Even with `N_c = 3`
   and `n_gen = 3` retained, anomaly cancellation does not constrain
   operator-coefficient ratios on the C_3-circulant Yukawa structure on
   `hw = 1 ≅ C^3` (the A1-condition `|b|²/a² = 1/2`); see
   [`KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md`](KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md).
   Anomaly is a constraint on REPRESENTATION LABELS; A1 is a constraint
   on OPERATOR COEFFICIENTS; categories disjoint.

The bounded label records the positive sub-rows (Y-Pos-1, Y-Pos-2, Y-Pos-3
already on the retained surface) plus the negative obstructions
(Y-Neg-A through Y-Neg-E unforced by anomaly alone).

## 2. Honest scope and named admissions

**Bounded admissions (records of negative findings, not new admissions to
the framework):**

- **B-Neg-A.** `N_c = 3` is **outside** the anomaly-forcing chain. The
  GRAPH_FIRST_SU3 substrate selector is the load-bearing input.
- **B-Neg-B.** `n_gen = 3` is **outside** the anomaly-forcing chain. The
  THREE_GENERATION orbit-counting theorem is the load-bearing input.
- **B-Neg-C.** LH content choice is **outside** the anomaly-forcing chain.
  The LH_DOUBLET ratio + LHCM matter assignment chain is the load-bearing
  input.
- **B-Neg-D.** Hypercharge absolute normalization is **convention-fixed**,
  not anomaly-forced; this is recorded honestly in the existing LEFT_HANDED
  and HYPERCHARGE_IDENTIFICATION notes.
- **B-Neg-E.** A1-condition `|b|²/a² = 1/2` is **outside** the anomaly-
  forcing chain; reaffirms PR #733 (probe 2) result.

**Positive sub-rows already retained (cited, not strengthened):**

- **Y-Pos-1.** RH hypercharges `(-4/3, +2/3, -2, 0)` — already retained
  positive theorem.
- **Y-Pos-2.** RH SU(3) reps as `2 × 3̄` — already retained positive
  theorem.
- **Y-Pos-3.** 3+1 spacetime signature — bounded conditional positive
  theorem on retained chiral-gauge content.

The probe's contribution is the **explicit identification** of which
substrate-to-carrier admissions anomaly cancellation reaches and which
it does not, in a single bounded source note. This sharpens the prior
bundled "substrate-to-carrier" gap into named negative obstructions plus
named already-closed positive rows.

This note does NOT use:
- PDG observed masses, charges, mixing angles
- New repo-wide axioms
- Lattice MC empirical measurements
- Fitted matching coefficients
- HK + DHR appeal (Block 01 audit retired this; respected)
- Same-surface family arguments

## 3. Setup

### 3.1 Retained inputs (Cl(3)/Z^3 baseline + cited theorems)

| Ingredient | Authority |
|---|---|
| Cl(3)/Z^3 native primitive structure | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| Cl(3)/Z^3 native cubic SU(2) gauge structure | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) |
| Graph-first SU(3) integration with `N_c = 3` | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| Three-generation observable structure | [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Retained left-handed `Q_L`, `L_L` content | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) |
| SM hypercharge uniqueness (RH solve) | [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) |
| SU(3)^3 anomaly-forced 3̄ completion | [`SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md`](SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md) |
| Anomaly forces 3+1 (bounded) | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) |
| SM anomaly cancellation complete (synthesis) | [`AXIOM_FIRST_SM_ANOMALY_CANCELLATION_COMPLETE_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SM_ANOMALY_CANCELLATION_COMPLETE_THEOREM_NOTE_2026-05-03.md) |
| Standard ABJ trace formulae and Dynkin indices | textbook QFT input |
| Witten (1982) homotopy `pi_4(SU(2)) = Z_2` | textbook nonperturbative-anomaly input |

### 3.2 Anomaly slots considered

| Slot | Form | Constraint type |
|---|---|---|
| (A0) | `Tr[SU(2)^3]` | identically 0 by group theory (no constraint on matter) |
| (A1) | `Tr[SU(3)^3]` | matter-content cubic on quark sector |
| (A2) | `Tr[SU(2)^2 Y]` | LH-doublet weighted hypercharge sum |
| (A3) | `Tr[Y]` (grav) | linear hypercharge sum |
| (A4) | `Tr[Y^3]` | cubic hypercharge sum |
| (A5) | `n_D mod 2` (Witten Z_2) | nonperturbative SU(2) doublet count parity |

These six slots are exhaustive for `SU(3) × SU(2) × U(1)_Y` coupled to gravity.

## 4. Probe construction (anomaly forcing test on substrate-only carrier
candidates)

### 4.1 Positive row Y-Pos-1: RH hypercharges from LH content

Given LH content `Q_L : (3, 2)_{+1/3} + L_L : (1, 2)_{-1}`, the system
`(A2), (A3), (A4)` plus neutrality `Y(nu_R^c) = 0` uniquely determines

```
y_1 = Y(u_R^c) = -4/3,  y_2 = Y(d_R^c) = +2/3,
y_3 = Y(e_R^c) = -2,    y_4 = Y(nu_R^c) = 0.
```

(The runner verifies this solving path explicitly; this row is already
retained per [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md).)

### 4.2 Positive row Y-Pos-2: RH SU(3) rep from Q_L

The SU(3)^3 cubic anomaly index satisfies `A(3) = +1, A(3̄) = -1`. With
`Q_L` contributing `2 × A(3) = +2` (SU(2) doublet), the RH content must
contribute `-2` for cancellation. The minimal solution is two LH-Weyl
3̄ singlets, identified as `u_R^c, d_R^c`. (Runner verifies; row already
retained per [`SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md`](SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md).)

### 4.3 Positive row Y-Pos-3: 3+1 signature (bounded)

The chiral gauge content `SU(2) × U(1)_Y` requires a chirality grading
on the spinor representation of `Cl(d_s, d_t)`. The standard physics
convention `γ_5 = i^{d_t(d_t+1)/2} · ω` (with `ω = e_1 ... e_n` the volume
element, `n = d_s + d_t`) gives a Z_2 chirality grading exactly when
`n` is even, with `(γ_5)^2 = +1` after the `i`-prefactor adjustment.
Combined with two retained substrate constraints:
- the `Z^3` spatial substrate per [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  forces `d_s = 3`;
- the single-clock codim-1 evolution per
  [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
  forces `d_t = 1`,

the unique signature accepting chiral gauge anomaly cancellation is
`(3, 1)`. Bounded on the still-open ABJ admission (i) per
`ANOMALY_FORCES_TIME_THEOREM`.

### 4.4 Negative obstruction Y-Neg-A: anomaly does not force `N_c`

The candidate generalisation `Q_L : (N_c, 2)_{a/N_c}` for arbitrary
`N_c ≥ 2` and rational `a` (with the same SU(2) doublet structure)
admits anomaly cancellation against an `N_c`-dependent RH completion.
The runner constructs the system for `N_c ∈ {2, 3, 4, 5, 6}` and verifies
that anomaly cancellation closes for each `N_c`, with hypercharges
`(y_1, y_2, y_3, y_4)` shifting accordingly. Anomaly cancellation alone
does not select `N_c = 3`; the GRAPH_FIRST_SU3 substrate selector does.

### 4.5 Negative obstruction Y-Neg-B: anomaly does not force `n_gen`

Anomaly cancellation traces are LINEAR in the number of generations: if
the one-generation traces vanish, then `n_gen` generations also have
vanishing traces for any `n_gen ≥ 1`. The Witten Z_2 parity requires
`n_gen × n_D mod 2 = 0` where `n_D = 4` per generation (3 quark colours
+ 1 lepton doublet); since `n_D = 4` is even, ANY `n_gen` satisfies the
parity. The runner verifies this for `n_gen ∈ {1, 2, 3, 4, 5}`. Anomaly
cancellation alone does not select `n_gen = 3`; the THREE_GENERATION
orbit-counting theorem does.

### 4.6 Negative obstruction Y-Neg-C: anomaly does not force LH partition

The runner enumerates alternative LH content surfaces:
1. **Vectorlike content** `R + R̄` for any SU(3) × SU(2) representation
   — anomaly-free for any `R`.
2. **Pati-Salam** `(4, 2, 1) + (\bar{4}, 1, 2)` — anomaly-free under the
   PS gauge group.
3. **Trinification** `(3, \bar{3}, 1) + (1, 3, \bar{3}) + (\bar{3}, 1, 3)`
   — anomaly-free under SU(3)^3.
4. **Fourth-family `Q_L^{IV} + L_L^{IV} + ν_R^{IV}`** — anomaly-free under
   the SM gauge group, just adds another generation.
5. **B-L extension** with extra RH neutrinos — anomaly-free per
   [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md).
6. **SU(5) GUT** `5̄ + 10` — anomaly-free under SU(5).
The runner verifies each of these is anomaly-free. Anomaly cancellation
alone does not select the SM-frame `Q_L + L_L` LH content; the substrate
LH_DOUBLET ratio + LHCM matter assignment chain does.

### 4.7 Negative obstruction Y-Neg-D: anomaly does not force absolute Y scale

The one-parameter family `Y_α = α (3 P_sym − 3 P_anti)` (in the LH-doublet
sector) preserves all anomaly trace ratios for any `α ≠ 0`; the absolute
scale `α = +1/3` is fixed by the convention `Y(L_L) = -1`. The runner
verifies that for `α ∈ {1/3, 1, 2, π}` the anomaly traces all vanish (with
appropriately rescaled RH hypercharges). The convention boundary is
honestly recorded in [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md).

### 4.8 Negative obstruction Y-Neg-E: anomaly does not force A1-condition

The A1-condition `|b|²/a² = 1/2` lives on the C_3-equivariant Hermitian
circulant `H = aI + bC + b̄C²` on `hw = 1 ≅ C^3` (operator coefficients).
Anomaly cancellation lives on representation labels (charges, multiplicities).
There is no retained map from representation labels to operator coefficients
in this sector; this is the structural P2-S1 lemma of probe 2 (PR #733).
The runner re-verifies this category mismatch explicitly.

## 5. Why this is bounded (mostly negative)

Following the user-memory feedback rule
[`feedback_consistency_vs_derivation_below_w2.md`](../docs/) (consistency
equality is not derivation): the existing positive-theorem chain
`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS` and `SU3_ANOMALY_FORCED_3BAR_COMPLETION`
are positive ON THE RETAINED LH CONTENT SURFACE. They derive RH content
from LH content; they do not derive LH content from substrate. Probe Y
respects this boundary and explicitly identifies the inputs anomaly
cancellation reaches and the inputs it doesn't.

Per [`feedback_primitives_means_derivations.md`](../docs/): the probe is
restricted to retained Cl(3)/Z^3 + standard anomaly cancellation (group
theory of retained Cl(3) generators). No new axioms, no imports beyond
retained content.

Per [`feedback_physics_loop_corollary_churn.md`](../docs/): probe Y is NOT
a relabel of an already-landed anomaly-forcing cycle. It is a **new
synthesis** that explicitly identifies the boundary between what anomaly
cancellation forces and what it does not, in a single source note. The
prior anomaly-forcing notes (SU3_3̄, SM_HYPERCHARGE_UNIQUENESS, ANOMALY_FORCES_TIME)
each closed one positive sub-row; this probe closes the *negative
boundary* — what is OUTSIDE the anomaly-forcing surface — for `N_c`,
`n_gen`, LH partition, absolute Y scale, and A1.

Per [`feedback_special_forces_seven_agent_pattern.md`](../docs/) (when
attacking a load-bearing brick): the probe is single-shot, not a 7-agent
dispatch. The bounded result is the appropriate verdict given the existing
positive-theorem chain.

## 6. Cross-references

- **Sister positive theorems (cited, not strengthened):**
  - [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  - [`SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md`](SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02.md)
  - [`AXIOM_FIRST_SM_ANOMALY_CANCELLATION_COMPLETE_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SM_ANOMALY_CANCELLATION_COMPLETE_THEOREM_NOTE_2026-05-03.md)
  - [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  - [`SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md`](SM_HYPERCHARGE_UNIQUENESS_WITHOUT_NU_R_INPUT_THEOREM_NOTE_2026-05-02.md)
- **Sister substrate-to-carrier probes (this round):**
  - [`PLANCK_SUBSTRATE_TO_CARRIER_FORCING_BOUNDED_NOTE_2026-05-10_planckP1.md`](PLANCK_SUBSTRATE_TO_CARRIER_FORCING_BOUNDED_NOTE_2026-05-10_planckP1.md)
    (P1 — RP route on `P_A`)
  - [`PLANCK_HIDDEN_CHARACTER_DELTA_ZERO_POSITIVE_THEOREM_NOTE_2026-05-10_planckP2.md`](PLANCK_HIDDEN_CHARACTER_DELTA_ZERO_POSITIVE_THEOREM_NOTE_2026-05-10_planckP2.md)
    (P2 — Planck-side delta closure via source-free state)
- **Substrate carrier obstructions:**
  - [`SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`](SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
- **A1 anomaly probe (negative result, sister probe):**
  - [`KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md`](KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md)
- **Substrate retained inputs:**
  - [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  - [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  - [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
  - [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  - [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
- **B-L freedom:**
  - [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md)

## 7. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/cl3_koide_y_substrate_anomaly_2026_05_08_probeY_substrate_anomaly.py
```

The runner verifies:

1. **Section 1 (Y-Pos-1).** RH hypercharges `(-4/3, +2/3, -2, 0)` solve
   the `(A2)+(A3)+(A4)` system on retained LH content, exact Fraction
   arithmetic.
2. **Section 2 (Y-Pos-2).** RH SU(3) rep `2 × 3̄` is the unique 2-field
   anomaly-cancelling completion against `Q_L : (3, 2)`, exact Fraction
   arithmetic.
3. **Section 3 (Y-Pos-3).** 3+1 signature accepts chiral-gauge anomaly
   cancellation; alternatives `(d_s, d_t) ∈ {(2,2), (4,0), (5,1)}` either
   fail single-clock codim-1 or fail Clifford volume-element chirality
   grading.
4. **Section 4 (Y-Neg-A).** For `N_c ∈ {2, 3, 4, 5, 6}`, anomaly
   cancellation closes with `N_c`-dependent rescaled hypercharges.
   Anomaly does not select `N_c = 3`.
5. **Section 5 (Y-Neg-B).** For `n_gen ∈ {1, 2, 3, 4, 5}`, all six
   anomaly slots vanish. Anomaly does not select `n_gen = 3`.
6. **Section 6 (Y-Neg-C).** Six alternative LH content surfaces (vector-
   like, Pati-Salam, trinification, fourth-family, B-L, SU(5) 5̄+10)
   are anomaly-free. Anomaly does not select the SM `Q_L + L_L`
   partition.
7. **Section 7 (Y-Neg-D).** For `α ∈ {1/3, 1, 2, π}`, anomaly traces
   all vanish under appropriately rescaled hypercharges. Anomaly does
   not fix the absolute Y scale.
8. **Section 8 (Y-Neg-E).** Anomaly traces and operator-coefficient
   ratios are in disjoint mathematical categories; no retained map
   exists. Cross-references probe 2 (PR #733).
9. **Section 9.** Honest scope and tier classification.

Expected output:

```
=== TOTAL: PASS=N, FAIL=0 ===
```

with all positive sub-rows (Y-Pos-1, Y-Pos-2, Y-Pos-3) confirmed and
all negative obstructions (Y-Neg-A through Y-Neg-E) explicitly verified.

## 8. Status

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Anomaly cancellation forces RH content (hypercharges, SU(3) reps) given
  LH content, and conditionally forces 3+1 spacetime signature, but does
  NOT force the substrate-side carrier choices N_c=3, n_gen=3, LH
  partition, absolute Y scale, or A1-condition operator coefficients.
  The substrate-to-carrier hidden-character bundle is therefore PARTIALLY
  but not FULLY closed by anomaly cancellation alone.
proposed_load_bearing_step_class: B (bounded; positive sub-rows already
  retained, negative boundary explicitly identified)
declared_one_hop_deps:
  - axiom_first_sm_anomaly_cancellation_complete_theorem_note_2026-05-03
  - standard_model_hypercharge_uniqueness_theorem_note_2026-04-24
  - su3_anomaly_forced_3bar_completion_theorem_note_2026-05-02
  - anomaly_forces_time_theorem
  - graph_first_su3_integration_note
  - three_generation_observable_theorem_note
  - left_handed_charge_matching_note
  - hypercharge_identification_note
  - koide_a1_probe_flavor_anomaly_bounded_obstruction_note_2026-05-08_probe2
  - bminusl_anomaly_freedom_theorem_note_2026-04-24
independent_audit_required_before_effective_status_change: true
forbidden_imports_used: false
hypothetical_axiom_status: null
admitted_observation_status: |
  Standard ABJ trace formulae, Dynkin indices T(3) = T(2) = 1/2,
  SU(3) cubic anomaly indices A(3) = +1 / A(3bar) = -1, Witten (1982)
  pi_4(SU(2)) = Z_2 admitted as universal QFT/topology input. The
  ANOMALY_FORCES_TIME admission (i) (ABJ on the lattice) remains a bare
  external admission per the parent note.
```

## 9. What this probe closes / does not close

**Closes:**
- The structural-boundary question: which substrate-to-carrier admissions
  anomaly cancellation forces (RH content, 3+1 signature) and which it
  does not (`N_c`, `n_gen`, LH partition, abs Y, A1).
- A unified bounded source note for the negative boundary.

**Does NOT close:**
- The substrate-to-carrier hidden-character bundle in full — anomaly
  cancellation closes only sub-rows.
- Any new positive theorem; existing positive sub-rows are cited, not
  strengthened.
- The Planck-from-structure cascade — that requires P1 (RP-route),
  P2 (delta=0), P3 (orientation), and P4 (G_Newton) per the
  path-opening synthesis.

## 10. Honest verdict summary

The probe Y hypothesis ("anomaly cancellation forces full SM carrier
content from substrate alone") is **NOT supported**. Anomaly cancellation
is a powerful constraint on RH content given LH content, and a conditional
forcing on spacetime signature, but it leaves the substrate carrier
inputs (`N_c`, `n_gen`, LH partition, abs Y, A1) unforced. The closure
of those inputs requires substrate-side machinery (GRAPH_FIRST_SU3,
THREE_GENERATION orbit theorem, LH_DOUBLET ratio, conventional
labelling) that lives outside the anomaly-cancellation surface.

The probe contributes:
1. A clean negative boundary identification for `N_c`, `n_gen`, LH
   partition, abs Y, A1.
2. A unified bounded source note that consolidates the prior scattered
   anomaly-forcing positives (RH content, 3+1) with the new negatives.
3. A cross-reference into the probe 2 / R3-functoriality / P2-S1 chain
   for the A1 boundary.
