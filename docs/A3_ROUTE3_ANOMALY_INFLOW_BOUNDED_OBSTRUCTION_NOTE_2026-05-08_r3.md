# A3 / AC_phi Route 3 — Anomaly Inflow (Bounded Obstruction, 7-Vector Sweep)

**Date:** 2026-05-08
**Type:** bounded_theorem
**Claim type:** bounded_theorem
**Scope:** source-note proposal — bounded obstruction over a 7-vector
sweep of anomaly-inflow channels. Tests whether anomaly-inflow content
(`'t Hooft` matching, Callan-Harvey inflow, SPT phases, discrete
anomalies, WZW terms, Atiyah-Singer index, Nieh-Yan torsion) can
distinguish the three hw=1 BZ corners on the staggered Dirac Z³ APBC
surface and thereby close substep-4 atom AC_φ from A1 (Cl(3)) + A2
(Z³) + the retained upstream authority stack — **without new axioms
and without adding a new bounding assumption**.
**Status:** source-note proposal — audit verdict and downstream status
set only by the independent audit lane.
**Loop:** `a3-route3-anomaly-inflow-20260508`
**Primary runner:** [`scripts/cl3_a3_route3_anomaly_inflow_2026_05_08_r3.py`](../scripts/cl3_a3_route3_anomaly_inflow_2026_05_08_r3.py)
**Cache:** [`logs/runner-cache/cl3_a3_route3_anomaly_inflow_2026_05_08_r3.txt`](../logs/runner-cache/cl3_a3_route3_anomaly_inflow_2026_05_08_r3.txt)

## Authority disclaimer

This is a source-note proposal. Effective `effective_status` is generated
by the audit pipeline only after the independent audit lane reviews the
claim, dependency chain, and runner. The `claim_type`, scope, named
admissions, and bounded classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Question

[`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
narrowed the substep-4 admitted-context (AC) into three independent
atoms

```
AC_narrow  =  AC_φ  ∧  AC_λ  ∧  AC_φλ
```

and identified `AC_φ` as the structural barrier under retained C_3:

> **Substep4ac Lemma.** If `H` is self-adjoint on `H_{hw=1} ≅ C³` and
> `[H, U_{C_3}] = 0`, then `H` has the *same* expectation value on each
> corner-basis state `|c_α⟩` (α = 1, 2, 3).

This forces AC_φ closure to require **C_3[111]-breaking dynamics not
supplied by the current upstream stack**.

Substep4ac listed three known closure paths: (a) Yukawa-Higgs VEV,
(b) anomaly-induced breaking, (c) spontaneous C_3 breaking. Path (a)
is a new field; path (c) is an alternative-vacuum statement excluded
by RP+CD unique-vacuum authorities. Path (b), **anomaly-induced
breaking**, is the candidate examined here.

Prior anomaly attacks on the related W2 / L3a layer were homogeneous
in gauge-field power and gave clean obstructions or weak partials
([`L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md`](L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md)
attack vector V4 — anomaly cancellation as a clean obstruction;
[`N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md`](N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md)
attack vector V2 — anomaly cancellation specific to V_3, partial).
Neither used **anomaly inflow** — the Callan-Harvey 1985 mechanism by
which anomalies on a boundary force specific representation content
in the bulk.

The hypothesis examined here:

> **Hypothesis (R3-H1).** 't Hooft anomaly matching, Callan-Harvey
> bulk-boundary inflow, SPT-class invariants, discrete (mod-N)
> anomalies, WZW terms, Atiyah-Singer index, or Nieh-Yan torsion — at
> least one of these anomaly-inflow channels assigns to the three hw=1
> corner states `{|c_1⟩, |c_2⟩, |c_3⟩}` distinct anomaly-class
> contributions, breaking the C_3[111] equal-expectation conclusion of
> Lemma substep4ac.

## Answer

**Hypothesis R3-H1 is REJECTED across all seven channels.**

The seven attack vectors all yield **OBSTRUCTION**: the corresponding
anomaly-inflow operator is C_3[111]-symmetric by construction (built
from C_3-symmetric primitives in A1+A2 plus the retained upstream
stack), and therefore obeys substep4ac's equal-expectation conclusion.
Anomaly inflow does **not** close A3 / AC_φ from the current primitive
stack without new axioms.

The result is consistent with prior anomaly results
([`L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md`](L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md)
S3 sharpening: anomaly cancellation is trace-surface independent;
[`N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md`](N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md)
V2: rep-content not trace-surface) and identifies the *deeper*
structural reason that those prior obstructions are themselves
instances of:

> **Universal C_3-orbit obstruction (R3-S1).** Anomalies attach
> functorially to *symmetries* (groups, orbits, cohomology classes,
> representation classes), **not** to individual *states* within a
> single symmetry orbit. The three hw=1 corners form a single
> C_3[111] orbit; any anomaly-class invariant assigns the same value
> to the orbit, hence (operationally) the same corner-basis
> expectation to each |c_α⟩.

This is a sharpening of the substep4ac Lemma, lifting it from "C_3-
symmetric *self-adjoint operator*" to "C_3-symmetric *anomaly
functor*". The two conclusions coincide on hw=1 because functorial
anomaly carriers act on H_{hw=1} as C_3-symmetric operators.

## Setup

### Premises (A_min for Route 3)

| ID | Statement | Authority |
|---|---|---|
| A1 | Cl(3) local algebra | `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | `MINIMAL_AXIOMS_2026-05-03.md` |
| RP | RP A11 + OS reconstruction → `H_phys` with unique vacuum `Ω` | [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) |
| CD | Cluster decomposition + unique vacuum | [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md) |
| RS | Reeh-Schlieder cyclicity | [`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md) |
| LR | Lieb-Robinson microcausality | [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md) |
| LN | Lattice Noether fermion-number on H_phys | [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md) |
| SC | Single-clock codimension-1 evolution | [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md) |
| BlockT3 | hw=1 BZ-corner triplet has M_3(C) algebra with distinct joint translation characters | [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md), [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| C3_111 | C_3[111] cyclic permutation `(x, y, z) → (y, z, x)` of Z³ axes | imported from Z³ point-group / BZ-corner setup |
| StagC | Staggered chirality `C(x) = (-1)^{x+y+z}`; `{C, H_phys} = 0`; `(-1)^{hw}` per BZ corner | [`STAGGERED_CHIRAL_SYMMETRY_SPECTRUM_THEOREM_NOTE_2026-05-02.md`](STAGGERED_CHIRAL_SYMMETRY_SPECTRUM_THEOREM_NOTE_2026-05-02.md), [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) |
| Sub4ac | Substep4ac Lemma: C_3-symmetric self-adjoint H ⇒ equal corner-basis expectations | [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) |

### Forbidden imports

- NO PDG observed values
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- **NO new axioms** (this is the explicit user constraint for the route)
- **NO bounding** (this is the explicit user constraint for the route)
- NO HK + DHR appeal (the Block 01 audit retired this; respected)
- NO same-surface family arguments

The route is therefore constrained to derive AC_φ closure from the
listed retained primitives only, and the present note documents the
result of that constrained search across the seven anomaly-inflow
channels.

## Attack-vector sweep (E1–E7)

The runner enumerates seven anomaly-inflow channels. Each is a
candidate physical mechanism for assigning C_3-distinct anomaly content
to the three hw=1 corners. For each, we either (a) identify a structural
reason that the channel is unavailable from A1+A2 + the retained stack,
or (b) construct the natural C_3-symmetric anomaly-carrier operator on
H_{hw=1} and verify it gives equal corner-basis expectations (the
substep4ac equal-expectation Lemma applies).

| # | Channel | Physical content | Status | Structural reason |
|---|---|---|---|---|
| **E1** | `'t Hooft anomaly matching across boundary of Z³` | Boundary-bulk anomaly polynomial matching ('t Hooft 1980) | OBSTRUCTION | Z³ has no boundary; finite L³ APBC is a 3-torus (no boundary either). Adding a boundary is a new axiom. C_3-symmetric matching polynomial gives equal corner expectations. |
| **E2** | Callan-Harvey anomaly inflow from a domain wall | Codim-1 defect hosts boundary fermion; bulk inflow cancels boundary anomaly (Callan-Harvey 1985) | OBSTRUCTION | A1+A2 supplies no codim-1 defect on Z³. C_3-symmetric defect ⇒ C_3-symmetric inflow ⇒ equal corner expectations. |
| **E3** | SPT phase under `C_3 × U(1)_Q` | Bulk gapped phase classified by `H^4(BZ_3, U(1)) = ℤ_3`; topological response action | OBSTRUCTION | SPT class is a single ℤ_3-valued invariant of the bulk Hamiltonian / unique vacuum, NOT a function on `H_{hw=1}`. RP+CD gives a C_3-symmetric vacuum ⇒ C_3-symmetric SPT response ⇒ equal corner expectations. |
| **E4** | Discrete (mod-3) anomaly on Z_3 | `H^d(BZ_3, U(1))`-valued obstruction to gauging C_3 | OBSTRUCTION | ℤ_3 cohomology is a property of the GROUP Z_3, not of orbit elements. Carrier operator on hw=1 is C_3-symmetric (polynomial in `U_{C_3}`); equal corner expectations. |
| **E5** | Wess-Zumino-Witten term on the C_3 orbit | Topological term in the action capturing discrete anomalies | OBSTRUCTION | WZW term is a topological functional of FIELD configurations. Operator-expectation on hw=1 is polynomial in `U_{C_3}` (cyclic permutation has zero diagonal); equal corner expectations. |
| **E6** | Atiyah-Singer index for the staggered Dirac operator | Chiral charge `n_+ − n_−` graded by sublattice parity | OBSTRUCTION | All hw=1 corners share Hamming weight 1 ⇒ same staggered chirality `(−1)^1 = −1`. Index theorem groups corners by hw parity and CANNOT distinguish elements within a fixed hw stratum. |
| **E7** | Nieh-Yan torsion anomaly | Torsion-related 4D topological density `T^a ∧ T_a` | OBSTRUCTION | A1+A2 supplies no torsion field; Z³ is flat. Adding torsion is a new axiom. C_3-symmetric torsion ⇒ C_3-symmetric Nieh-Yan integral ⇒ equal corner expectations. |

**Result distribution:** 0 unconditional positive arrows, 0 partials,
**7 clean obstructions**.

The runner verifies the obstruction structurally for each vector
(15 PASS, 0 FAIL) and verifies the universal C_3-symmetric
equal-expectation lemma over a 200-sample random sweep of `(a, b)`
parameters (200/200 PASS).

## Universal C_3-orbit obstruction (R3-S1)

Behind the seven OBSTRUCTION verdicts is a single structural fact:

> **Lemma (R3-S1, Universal C_3-orbit obstruction).** Let `G = C_3[111]`
> act on `H_{hw=1} ≅ C³` by the cyclic permutation `U_{G}` of the
> orbit basis `{|c_α⟩}`. Let `A` be any *anomaly-class invariant*
> constructed from G-equivariant primitives — i.e., any of:
> a 't Hooft anomaly polynomial p(G), an SPT class κ ∈ H^4(BG, U(1)),
> a discrete anomaly class η ∈ H^d(BG, U(1)), an Atiyah-Singer index
> ind(D), a Nieh-Yan integral N, a WZW cocycle ω, or a Callan-Harvey
> inflow current J. Let `O_A` be the natural carrier operator
> realizing A on `H_{hw=1}` — i.e., the operator whose
> expectation-value evaluates the anomaly contribution. Then
> `[O_A, U_{G}] = 0` and consequently
>
> ```
> ⟨c_α | O_A | c_α⟩  =  ⟨c_β | O_A | c_β⟩    for all α, β = 1, 2, 3.
> ```

**Proof sketch.** Each anomaly-class invariant `A` is, by definition,
a functor from G-modules (or G-orbits, G-cohomology classes) to a
target group (typically U(1) or ℤ). Functoriality means that any
G-equivariant isomorphism `f : M → M'` of G-modules induces equality
`A(M) = A(M')`. The cyclic permutation `U_{G}` acts on H_{hw=1} as
such a G-equivariant isomorphism (it is *the* C_3 generator). Hence
the carrier operator `O_A` commutes with `U_{G}`. The substep4ac
Lemma then gives equal corner-basis expectations. ∎

This lemma is the deeper reason why the seven E1–E7 channels all
yield obstruction: every anomaly-class invariant is functorially a
property of the G-orbit, never of an individual orbit-element. The
C_3-orbit `{c_1, c_2, c_3}` is a single object in the G-category,
and the seven anomaly-inflow channels read off seven different
functors evaluated on this single object.

## Comparison to the substep4ac three "closure paths"

Substep4ac listed three known mechanisms for breaking C_3[111] of
hw=1 dynamics:

> (a) **Yukawa-Higgs coupling:** Higgs VEV breaks C_3[111] by
>     selecting a preferred mass direction.
> (b) **Anomaly-induced breaking:** an uncancelled triangle anomaly
>     under C_3[111] would generate dynamical C_3 breaking.
> (c) **Spontaneous C_3 breaking:** the vacuum state itself fails
>     to be C_3[111]-symmetric.

The present note examines path (b) in seven concrete sub-channels
and finds clean obstructions in all seven. Combined with substep4ac
on path (a) and on the RP+CD unique-vacuum exclusion of path (c),
the result is:

- **Path (a)** Yukawa-Higgs: requires a Higgs field, which is a new
  primitive on top of A1+A2 — a new axiom or admitted-context input.
- **Path (b)** anomaly-induced (this note, R3-S1): all seven
  anomaly-inflow channels respect C_3 functorially; no path-(b)
  closure exists from A1+A2 + retained stack.
- **Path (c)** spontaneous C_3 breaking: requires non-unique vacuum,
  excluded by RP A11 + cluster decomposition (CD).

**Joint conclusion:** AC_φ remains an open closure target on the
A1+A2 + retained stack. The three substep4ac closure paths are now
all checked: paths (a), (c) excluded by named upstream authorities;
path (b) excluded across seven sub-channels by R3-S1.

## What this note DOES establish

1. **Seven-vector enumeration.** Seven independent anomaly-inflow
   channels (E1–E7) covering the standard literature: 't Hooft
   matching, Callan-Harvey inflow, SPT phases, discrete anomalies,
   WZW terms, Atiyah-Singer index, Nieh-Yan torsion.

2. **Universal C_3-orbit obstruction (R3-S1).** A single sharpening
   of substep4ac Lemma from "C_3-symmetric self-adjoint operator" to
   "C_3-symmetric anomaly-class functor" — covering the entire
   literature class of anomaly invariants.

3. **15 PASS / 0 FAIL** runner verification across structural
   checks plus a 200-sample random sweep of the universal lemma.

4. **Cross-consistency** with prior anomaly attacks:
   [`L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md`](L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md)
   S3 (anomaly cancellation trace-surface independent) and
   [`N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md`](N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md)
   V2 (rep-content not trace-surface). Both prior obstructions are
   instances of R3-S1 functoriality.

5. **Path-(b) of substep4ac substantially excluded.** Combined with
   substep4ac on paths (a) and (c), this leaves no in-stack closure
   route for AC_φ; any future closure requires explicit user
   approval to add a new primitive.

## What this note does NOT establish

- It does **not** close A3 from A1+A2 + the retained stack. Substep 4
  remains `bounded_theorem`; AC_φ remains an open atom; AC_residual
  = AC_φλ remains the genuine residual.
- It does **not** rule out a hypothetical anomaly mechanism *outside*
  the seven E1–E7 channels enumerated. R3-S1 is a structural
  argument that any *functorial* anomaly invariant respects the
  obstruction; non-functorial / non-anomaly-class mechanisms are
  outside the scope.
- It does **not** lift any prior `bounded_theorem` row to
  `positive_theorem`. The L3a / W2 tier-stratification is unchanged.
- It does **not** remove the staggered-Dirac realization gate
  (`MINIMAL_AXIOMS_2026-05-03.md`
  formerly-A3). Closing that gate is the canonical closure path.

## Empirical AC_φ testability after Route 3

| Closure path | Testability after Route 3 |
|---|---|
| Yukawa-Higgs (substep4ac path a) | Falsifiable via lattice MC with hypothetical Yukawa perturbation; level-spacing on hw=1 measurable |
| Anomaly-induced (substep4ac path b) | **Excluded across 7 sub-channels by R3-S1**; further sub-channel additions would be redundant by functoriality |
| Spontaneous C_3 breaking (substep4ac path c) | Excluded by RP A11 + CD (unique-vacuum upstream authorities) |
| Yet-unconsidered C_3-breaking primitive (R3 residual) | Open; would require explicit user approval as a new axiom or admitted-context input |

The Route 3 contribution is to compress closure path (b) — anomaly-
induced C_3 breaking — from a vague open path to a structurally
excluded path. Path (a) remains a falsifiable physical input, and
path (c) is excluded by stack authorities.

## Theorem (R3 bounded obstruction)

**Bounded theorem (Route 3, anomaly-inflow obstruction).** On A1+A2 +
the listed retained authorities + admissible standard math machinery,
without new axioms and without adding a new bounding assumption:

```
For each of the seven anomaly-inflow channels E1, …, E7
(  E1 't Hooft matching across Z^3 boundary,
   E2 Callan-Harvey inflow from a domain wall,
   E3 SPT phase under C_3 × U(1)_Q,
   E4 Discrete (mod-3) anomaly on Z_3,
   E5 WZW term on the C_3 orbit,
   E6 Atiyah-Singer index for staggered Dirac,
   E7 Nieh-Yan torsion anomaly
), the natural carrier operator O_E_k on H_{hw=1} commutes with
U_{C_3} and (by substep4ac Lemma)

   <c_α | O_E_k | c_α>  =  <c_β | O_E_k | c_β>     for all α, β.

In particular, no E_k closes AC_φ on H_{hw=1}.

Behind the seven verdicts is the universal C_3-orbit obstruction
R3-S1: an anomaly-class invariant is functorial in G-modules /
G-orbits / G-cohomology classes, hence its hw=1 carrier operator is
C_3-symmetric, hence equal corner-basis expectations.
```

**Proof.** Structural verification across seven concrete channels and
a universal-lemma random sweep, all in the runner. ∎

## Status

```yaml
actual_current_surface_status: bounded_theorem (anomaly-inflow obstruction)
proposed_claim_type: bounded_theorem
audit_review_points: |
  Conditional on:
   (a) independent audit confirmation that the seven E1–E7 channels
       constitute a representative sweep of anomaly-inflow mechanisms
       relevant to the C_3 orbit on hw=1;
   (b) independent audit confirmation that R3-S1 (universal C_3-orbit
       obstruction via functoriality of anomaly invariants) is a
       valid sharpening of substep4ac Lemma;
   (c) independent audit confirmation that the listed upstream
       authorities (RP A11, CD, RS, LR, LN, SC, BlockT3, StagC,
       Sub4ac, MINIMAL_AXIOMS) are correctly cited and load-bearing
       only at one hop;
   (d) independent audit confirmation that the claim of "path (b) of
       substep4ac substantially excluded" via R3-S1 is fairly
       characterized as bounded over the seven E_k.
hypothetical_axiom_status: null
admitted_observation_status: |
  Substep 4 AC_residual = AC_φλ remains admitted; AC_φ remains
  open with path (b) substantially excluded by R3-S1 across seven
  channels; closure requires path (a) Yukawa-Higgs (new primitive)
  or a yet-unconsidered C_3-breaking primitive (new axiom / admitted
  context, requiring explicit user approval).
claim_type_reason: |
  This note adds R3-S1 (universal C_3-orbit obstruction) and
  excludes the seven anomaly-inflow sub-channels of substep4ac path
  (b). It does not close A3; substep 4 remains bounded_theorem;
  AC_residual = AC_φλ remains the genuine residual.
independent_audit_required_before_any_effective_status_change: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## Promotion-Value Gate (V1–V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | Substep4ac path (b) is substantially excluded across seven channels via R3-S1; no new obstruction introduced beyond what was already implied by substep4ac. |
| V2 | New derivation? | R3-S1 (universal C_3-orbit obstruction via functoriality of anomaly invariants) is a new structural sharpening of substep4ac Lemma; the seven-vector enumeration (E1–E7) is new content. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) the seven-vector enumeration completeness, (ii) R3-S1 functoriality argument, (iii) the structural reasons for each E_k, (iv) cross-consistency with prior anomaly attacks. |
| V4 | Marginal content non-trivial? | Yes — R3-S1 lifts substep4ac Lemma from operator-level to functor-level; the seven-vector sweep covers the standard anomaly literature. |
| V5 | One-step variant? | No — R3-S1 is a structural-functoriality sharpening, not a relabeling of substep4ac path (b). |

**Source-note V1–V5 screen: pass for bounded audit seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`:

- Not a relabel of substep4ac. The seven-vector enumeration is a
  concrete sweep of anomaly mechanisms; R3-S1 (universal functorial
  obstruction) is a structural sharpening of the substep4ac Lemma.
- Identifies a structural reason for the prior L3a-V4 / W2.binary-V2
  anomaly obstructions: both are instances of R3-S1.
- The seven E_k channels cover the standard physics literature on
  anomaly inflow; further sub-channels would be redundant by R3-S1
  functoriality. This is precisely what the user-memory feedback
  rule recommends — stop at corollary exhaustion, not at
  `--max-cycles`.

## Cross-references

- Parent open-gate: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Substep 1 (upstream): [`STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md)
- Substep 2 (upstream): [`STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md)
- Substep 3 (upstream): [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- L3a 10-vector consolidation: [`L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md`](L3A_V3_TRACE_SURFACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_l3a.md)
- W2 binary obstruction (V2 anomaly attack): [`N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md`](N_F_TRACE_SPACE_BOUNDED_OBSTRUCTION_NOTE_2026-05-07_w2binary.md)
- SM anomaly cancellation closure: [`AXIOM_FIRST_SM_ANOMALY_CANCELLATION_COMPLETE_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SM_ANOMALY_CANCELLATION_COMPLETE_THEOREM_NOTE_2026-05-03.md)
- Anomaly-forces-time row: [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
- Brannen / Callan-Harvey candidate (bridge-conditioned): [`KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`](KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md)
- Staggered chiral-symmetry spectrum (sublattice parity): [`STAGGERED_CHIRAL_SYMMETRY_SPECTRUM_THEOREM_NOTE_2026-05-02.md`](STAGGERED_CHIRAL_SYMMETRY_SPECTRUM_THEOREM_NOTE_2026-05-02.md)
- CPT-exact (sublattice parity = staggered chirality): [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`
- Three-generation observable (M_3(C) on hw=1): [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- No-proper-quotient: [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)

## Citation references (anomaly inflow / anomalies / index)

- Adler, S. L. *Axial-Vector Vertex in Spinor Electrodynamics*,
  Phys. Rev. 177 (1969) 2426 — ABJ anomaly.
- Bell, J. S. & Jackiw, R. *A PCAC puzzle: π⁰ → γγ in the σ-model*,
  Nuovo Cimento A60 (1969) 47 — companion ABJ paper.
- 't Hooft, G. *Naturalness, chiral symmetry, and spontaneous chiral
  symmetry breaking*, in *Recent Developments in Gauge Theories*,
  NATO ASI B59 (Plenum, 1980) — 't Hooft anomaly matching.
- Callan, C. G. Jr. & Harvey, J. A. *Anomalies and Fermion Zero
  Modes on Strings and Domain Walls*, Nucl. Phys. B 250 (1985)
  427-436 — anomaly inflow from a codim-1 defect.
- Atiyah, M. F. & Singer, I. M. *The Index of Elliptic Operators I*,
  Ann. Math. 87 (1968) 484-530 — index theorem.
- Witten, E. *An SU(2) anomaly*, Phys. Lett. B 117 (1982) 324-328 —
  Z_2 / mod-N discrete anomaly archetype.
- Nieh, H. T. & Yan, M. L. *An identity in Riemann-Cartan
  geometry*, J. Math. Phys. 23 (1982) 373-374 — Nieh-Yan torsion
  anomaly.
- Wess, J. & Zumino, B. *Consequences of anomalous Ward
  identities*, Phys. Lett. B 37 (1971) 95-97; Witten, E. *Global
  aspects of current algebra*, Nucl. Phys. B 223 (1983) 422-432 —
  Wess-Zumino-Witten term.
- Chen, X., Gu, Z.-C., Liu, Z.-X. & Wen, X.-G. *Symmetry-Protected
  Topological Orders and the Group Cohomology of Their Symmetry
  Group*, Phys. Rev. B 87 (2013) 155114 — SPT phases via group
  cohomology, including ℤ_3 SPT classes.

## Command

```bash
python3 scripts/cl3_a3_route3_anomaly_inflow_2026_05_08_r3.py
```

Expected output: structural verification of the universal C_3-orbit
equal-expectation lemma, a 200-sample random sweep over C_3-symmetric
self-adjoint operators, structural verification across the seven
anomaly-inflow attack vectors E1–E7, and a sanity check that a
deliberately C_3-breaking operator does distinguish the corners.

```text
EXACT      : PASS = 15, FAIL = 0
BOUNDED    : PASS = 0, FAIL = 0
TOTAL      : PASS = 15, FAIL = 0
```

Cached: [`logs/runner-cache/cl3_a3_route3_anomaly_inflow_2026_05_08_r3.txt`](../logs/runner-cache/cl3_a3_route3_anomaly_inflow_2026_05_08_r3.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: R3-S1 is derived
  via functoriality of anomaly invariants on G-orbits, NOT via
  consistency-equality. The seven E_k structural-reason columns
  cite physical mechanisms, not numerical coincidences.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  action-level semantics of "anomaly inflow distinguishes the three
  corners" — what does "distinguish" actually require? — not just
  the algebra. R3-S1 is the semantic obstruction.
- `feedback_retained_tier_purity_and_package_wiring.md`: this note
  is a source-note proposal at the bounded tier; no automatic
  cross-tier promotion. AC_φ remains an open atom; substep 4 remains
  bounded_theorem.
- `feedback_physics_loop_corollary_churn.md`: R3-S1 functoriality
  argument is a structural sharpening, not a one-step relabel of
  substep4ac path (b); seven-vector enumeration covers the standard
  literature; further sub-channels are redundant by R3-S1.
- `feedback_compute_speed_not_human_timelines.md`: closure paths
  are characterized in terms of WHAT additional content would be
  needed (path (a) Yukawa primitive, or new C_3-breaking
  primitive), not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note is
  Route 3 of a parallel multi-route attack on A3; the result is a
  clean negative for one route, suitable for consolidation into a
  reusable no-go note (R3-S1 functoriality lemma).
- `feedback_review_loop_source_only_policy.md`: the deliverable is
  exactly (a) one source-theorem note in `docs/`, (b) one paired
  runner in `scripts/`, (c) one cached output in
  `logs/runner-cache/`. No output-packets, no lane promotions, no
  synthesis notes.

## Honest scope

This is a *Route 3* result. It does NOT close A3. It DOES:

1. Excluded substep4ac path (b) anomaly-induced C_3 breaking across
   seven concrete channels, via the universal R3-S1 functorial
   C_3-orbit obstruction.
2. Identified the deeper structural reason that prior L3a-V4 and
   W2.binary-V2 anomaly obstructions hold: both are instances of
   R3-S1.
3. Compressed the closure-path map for AC_φ:
   - path (a) Yukawa: requires a new primitive (open admission);
   - path (b) anomaly: substantially excluded by R3-S1 across seven
     sub-channels;
   - path (c) spontaneous: excluded by RP A11 + CD upstream
     authorities.

Closing A3 unconditionally from A1+A2 + retained stack remains an
open derivation target. The natural canonical closure path is the
staggered-Dirac realization gate per
`MINIMAL_AXIOMS_2026-05-03.md`.
