# Lane 2 S4 — Born-Trace Mass-Readout Extension Probe (higgsS4)

**Date:** 2026-05-10
**Type:** bounded_theorem (sharpened sub-issue inside Lane 2 step S4)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal. Extends the Probe G2 unified
position-density Born map (`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`)
from gravity-source readout to Higgs-mass operational readout, applied to
step S4 of `LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md`.
**Status:** source-note proposal. Verdict is SHARPENED, not CLOSED. The
operational mass-readout `m_H² = Tr(ρ̂ · Ô_{V''})` follows the same
trace-operator template as G2 once a mass-density observable is admitted,
but the load-bearing residual of S4 is the stationary-point matching
(symmetric-phase lattice curvature → post-EWSB physical curvature), which
the Born-trace template DOES NOT close. The trace template narrows S4
into an explicit state-selection sub-residual, but the conjunction
S4 ∧ S7 of the parent matching residual remains structurally open.
**Authority disclaimer:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** higgs-mass-s4-born-extension-20260510-higgsS4
**Primary runner:** [`scripts/cl3_higgs_mass_s4_born_extension_2026_05_10_higgsS4.py`](../scripts/cl3_higgs_mass_s4_born_extension_2026_05_10_higgsS4.py)
**Cache:** [`logs/runner-cache/cl3_higgs_mass_s4_born_extension_2026_05_10_higgsS4.txt`](../logs/runner-cache/cl3_higgs_mass_s4_born_extension_2026_05_10_higgsS4.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived `claim_type`,
`audit_status`, and `effective_status` are generated only after the
independent audit lane reviews the claim, dependency chain, and
runner. The audit lane has full authority to retag, narrow, or reject
the proposal.

## 0. Question

PR #884 (`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`)
established the unified position-density Born map as the canonical
operational readout for gravity sources:

```
ρ_grav(x) := ⟨x| ρ̂ |x⟩ = Tr(ρ̂ · M̂(x))   where  M̂(x) = |x⟩⟨x|
```

This map is canonical for both pure and mixed states (P1.1–P1.6 of G2).

PR #893 (`HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`) and PR #865
(`LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md`)
identified Lane 2 (Higgs mass from axiom) as **blocked** by step S4 of
the per-step matching decomposition:

> **S4** (load-bearing): tree-level mean-field readout
> `(m_H/v)² := |V''_lat| / N_taste = 1/(4 u_0²)` — asserted, not derived.

The brief proposes:

> Extend G2's unified Born map from gravity-sourcing to mass-readout. The
> same canonical operator-trace gives, for the Higgs:
> `m_H² = Tr(ρ̂_vacuum · ∂²V/∂φ²|_{φ_VEV})`.
>
> Hypothesis: this Born-trace identity matches lattice readout to
> physical mass, closing S4.

**Question:** Does the G2 unified Born-trace template extend to the
Lane 2 S4 mass-readout matching?

## 1. Answer

**SHARPENED, NOT CLOSED.**

The Born-trace template is **structurally extensible** to a
mass-readout operational form. For any Hermitian operator `Ô` on the
physical-lattice state space, the expectation value
`⟨Ô⟩ = Tr(ρ̂ · Ô)` follows the same trace-operator template as G2's
position-density map. Thus a candidate operational mass-readout is:

```
m_H² (operational) := Tr(ρ̂_phys · Ô_{m_H²})
```

where `Ô_{m_H²}` is the Hermitian operator whose expectation in the
physical Higgs single-particle state gives the squared mass.

**However**, three structural distinctions block direct closure of S4
by this extension:

- **(D1) Position vs. mass observables are different.** G2's
  `M̂(x) = |x⟩⟨x|` is a **rank-1 position projector**. The mass
  observable `Ô_{m_H²}` is the **second variational derivative of
  the effective potential**, evaluated at the post-EWSB minimum. These
  are structurally different operators on different parts of the
  Hilbert space. The Born-trace template gives the operational form
  but does not select between candidate `Ô_{m_H²}` operators.

- **(D2) Symmetric-point vs. post-EWSB stationary-point matching.**
  S4's load-bearing identification is `V''_lat(φ=0) ≡ V''_phys(φ=v)`,
  i.e. the lattice **symmetric-point** curvature is identified with
  the **post-EWSB-minimum** curvature. The Born-trace template does
  NOT bridge this stationary-point gap: it cannot derive the
  evaluation point φ* of the effective potential from the operator
  trace alone.

- **(D3) State-selection gap.** Even granting `Ô_{m_H²}`, the trace
  is `Tr(ρ̂ · Ô_{m_H²})` — and S4's identification implicitly fixes
  `ρ̂` to be the post-EWSB physical vacuum, not the lattice
  symmetric vacuum. The Born-trace template alone does not select
  ρ̂; this requires the EWSB stabilization that lies precisely in
  the open Lane 2 content (S7 gap-closure functional Δ²).

**Conclusion:** the Born-trace extension narrows S4 into an explicit
state-and-operator selection sub-residual, replacing the asserted
"tree-level mean-field readout" with the operational form
`m_H² = Tr(ρ̂_phys · Ô_{m_H²})` — but it does not derive the
state-and-operator pair `(ρ̂_phys, Ô_{m_H²})` from current retained
content. S4 remains the load-bearing residual, sharpened to a state-
selection sub-residual.

## 2. Setup

### Premises (this note's bounded-support lemma)

| ID | Statement | Class |
|---|---|---|
| BASE-CL3 | Physical `Cl(3)` local algebra | repo baseline; [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| BASE-Z3 | `Z^3` spatial substrate | repo baseline; same source |
| PhysLatBase | Physical `Cl(3)` on `Z^3` baseline (lattice is physical, not regulator) | repo-semantics meta: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md) |
| BornOp | Born-rule operationalism (Born rule as operational connection) | cited meta: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md) |
| G2-Born | Unified position-density Born map `ρ_grav(x) = Tr(ρ̂ · M̂(x))` | bounded_theorem proposal: [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md) |
| ParentS4 | Lane 2 S4 load-bearing residual: tree-level mean-field readout | bounded_theorem: [`LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md`](LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md) |
| ParentS7 | Lane 2 S7 +12% gap-closure functional Δ² | bounded_theorem: same as ParentS4 |
| HiggsTree | Tree-level mean-field formula `m_H_tree = v / (2 u_0) = 140.3 GeV` | [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) |
| BornDynVsMeas | Born rule is a MEASUREMENT postulate, not a DYNAMICS statement | cited: [`BORN_RULE_ANALYSIS_2026-04-11.md`](BORN_RULE_ANALYSIS_2026-04-11.md) |

### Forbidden imports

- NO PDG observed values used as derivation input.
- NO new repo-wide axioms.
- NO promotion of unaudited content to retained.
- NO empirical fits.
- NO same-surface family arguments.
- NO new physics inputs beyond G2's bounded support + standard QM
  expectation-value formalism + cited baseline/meta inputs above.

## 3. Theorem (bounded support, sharpened sub-issue inside S4)

**Theorem (Born-trace mass-readout extension; bounded support).**

Under the physical-lattice repo baseline + cited Born-rule
operationalism + G2's unified position-density Born map (bounded
support), the **Born-trace mass-readout operational form**

```
m_H² = Tr(ρ̂_phys · Ô_{m_H²})        (M-OP)
```

— where `ρ̂_phys` is the physical post-EWSB vacuum and `Ô_{m_H²}` is
the Hermitian Higgs-mass-squared operator on the physical Hilbert
space — is the **operational form for the physical Higgs mass-readout**.
This operational form satisfies:

- **(M1.1) Same trace-operator template as G2.** Both `ρ_grav(x)` and
  `m_H²` are expectation values of Hermitian operators in physical
  states: `⟨Ô⟩ = Tr(ρ̂ · Ô)`. The template `Tr(ρ̂ · Ô)` is canonical
  for any Hermitian observable `Ô` and any density operator `ρ̂` per
  Born-rule operationalism.

- **(M1.2) Position observables vs. mass observables (D1).**
  G2 instantiates the template with `Ô = M̂(x) = |x⟩⟨x|` (rank-1
  position projector). M-OP instantiates the template with
  `Ô = Ô_{m_H²}` (Higgs-mass-squared operator, not a rank-1 projector).
  The two instantiations share the trace-operator template but are
  distinct observables. The Born-trace template alone does not select
  `Ô_{m_H²}`.

- **(M1.3) State-selection gap (D2 + D3).** The trace
  `Tr(ρ̂_phys · Ô_{m_H²})` requires `ρ̂_phys` to be the post-EWSB
  physical vacuum. The lattice surface (HiggsTree) computes
  `V''_lat(0) = -4/u_0²` at the **symmetric point** (m=0, φ=0), which
  is **structurally distinct** from the post-EWSB vacuum
  `ρ̂_phys` ≈ |Ω_v⟩⟨Ω_v|. The Born-trace template does not derive
  the EWSB stabilization required to identify ρ̂_phys; this content
  is exactly the open Lane 2 S7 gap-closure functional Δ².

- **(M1.4) Born-rule layer separation (BornDynVsMeas).** Per
  `BORN_RULE_ANALYSIS_2026-04-11`, the Born rule is a **measurement
  postulate**, distinct from dynamics. S4's matching is a
  **dynamics-level** identification (effective potential curvature
  matching), not a measurement-level identification. The Born-trace
  template applies at the measurement-readout layer; it does not
  resolve the dynamics-level stationary-point matching gap.

- **(M1.5) Tree-level mean-field shortcut is not a Born-trace
  derivation.** The parent note `HIGGS_MASS_FROM_AXIOM_NOTE.md`
  Step 5(b) identifies `(m_H_tree/v)² = curvature/N_taste` at the
  symmetric point. This is the **tree-level mean-field
  Klein-Gordon readout** in the symmetric phase, NOT a Born-trace
  evaluation in the post-EWSB physical vacuum. The Born-trace
  extension explicitly highlights that the tree-level shortcut is a
  state-and-evaluation-point approximation, not a Born-trace
  identity.

- **(M1.6) Sharpened S4 residual.** The matching residual S4
  decomposes into:
  ```
  S4 ≡ S4a (operational form) ∧ S4b (state-and-operator selection)
  ```
  where S4a (operational form `m_H² = Tr(ρ̂_phys · Ô_{m_H²})`) is
  bounded-supported by the Born-trace template extension, while S4b
  (selection of the post-EWSB ρ̂_phys and the Higgs-mass operator
  `Ô_{m_H²}` from current retained content) remains the
  load-bearing residual. S4b composes with S7 (gap-closure
  functional Δ²) to recover the parent matching residual.

## 4. Proof sketch

### M1.1 Trace-operator template generality

For any density operator `ρ̂` and any Hermitian operator `Ô` on a
common Hilbert space, the expectation value is
```
⟨Ô⟩ = Tr(ρ̂ · Ô).
```
This is the standard QM expectation-value formalism (cited via
`BornOp` and `G2-Born`). Setting `Ô = M̂(x) = |x⟩⟨x|` recovers
`ρ_grav(x)` (G2's case). Setting `Ô = Ô_{m_H²}` (the squared
mass operator, defined as the second variation of the effective
potential at the post-EWSB minimum, projected onto the
physical Higgs single-particle channel) gives M-OP.

The shared template `Tr(ρ̂ · Ô)` is canonical for both
instantiations. ∎

### M1.2 Distinct observables

`M̂(x) = |x⟩⟨x|` is a rank-1 idempotent projector. The
Higgs-mass-squared operator `Ô_{m_H²}` is, in standard QFT,
the curvature of the effective action at the post-EWSB
minimum projected onto the physical Higgs channel. This is
**not** a rank-1 projector, **not** idempotent, and **not**
located in the position basis on `Z³`. The two operators
differ in rank, support, and physical interpretation.

The Born-trace template does not select between candidate
Hermitian operators. The runner verifies numerically that
even on a 4-site toy lattice, the position observable
`M̂(x=2)` and a mass-curvature observable
`Ô = -∂² V_lat / ∂m²|_{m=0}` (sketched as a Hermitian
matrix on the same Hilbert space) give different
expectation values in the same density operator, confirming
they are structurally different observables sharing only the
trace template. ∎

### M1.3 State-selection gap

The lattice symmetric-point vacuum `Ω_lat`(m=0) is
**not** the post-EWSB physical vacuum `Ω_v` (φ=v=246.22 GeV).
On the lattice mean-field surface, the symmetric-point
curvature is `V''_lat(0) = -4/u_0²`, which is **negative**
(tachyonic) and signals instability of the symmetric point.
The post-EWSB stable curvature is positive and located at
φ=v. The two vacua are different states.

The Born-trace template instantiated with `ρ̂ = Ω_lat`(m=0)
gives the symmetric-point curvature expectation, not the
physical Higgs mass squared. To get the physical Higgs
mass via the Born-trace template, one must instantiate
with `ρ̂ = Ω_v`, but `Ω_v` is the post-EWSB physical
vacuum that the Lane 2 S7 closure is precisely about
(Δ² gap-closure functional via CW + RGE + lattice flow +
Wilson taste-breaking).

The Born-trace template does not derive `Ω_v` from
`Ω_lat`. ∎

### M1.4 Layer separation

Per `BORN_RULE_ANALYSIS_2026-04-11.md`:

> The Born rule is a MEASUREMENT postulate (interface
> between quantum state and classical observables).
> Gravitational self-consistency is a DYNAMICS statement
> (how ψ and Φ co-evolve). These are different levels
> of the theoretical stack.

By analogous structure: the matching theorem residual S4
is a **dynamics-level** identification — it asserts that
the lattice effective-potential curvature equals the
physical Higgs mass squared. This is NOT a measurement
question. It is a question of how the effective action
on the lattice surface composes with EWSB stabilization
to produce a post-EWSB minimum and its curvature.

The Born-trace template applies at the measurement
readout layer (operational form for the mass observable
in a fixed state). It does not extend to the dynamics
layer (deriving the post-EWSB stationary state from the
symmetric-phase action). ∎

### M1.5 Tree-level mean-field shortcut framed via Born trace

The parent `HIGGS_MASS_FROM_AXIOM_NOTE.md` Step 5(b) is
explicit:

> The note's tree-level shortcut is: identify the per-channel
> curvature at the symmetric point `(4/u_0²)/N_taste` with
> `(m_H_tree/v)²` directly, treating the symmetric-point
> curvature as a proxy for the post-EWSB mass at the natural
> EWSB scale v. This is the standard mean-field estimate that
> becomes exact in the limit where (i) all N_taste taste
> channels degenerate, (ii) gauge corrections vanish, and (iii)
> the EWSB saddle aligns with the symmetric-point curvature.
> None of (i)-(iii) is exactly true — the +12% gap is precisely
> the magnitude of the correction.

Translating into Born-trace language:
- The operational form is `m_H² = Tr(Ω_v · Ô_{m_H²})`.
- The lattice surface gives
  `V''_lat(0) ≡ Tr(Ω_lat(0) · Ô_{V''})_{at φ=0}`.
- The shortcut **identifies** these two traces, with
  `(Ω_lat(0), Ô_{V''})` ≈ `(Ω_v, Ô_{m_H²})` "in a mean-field
  limit". This identification is precisely the +12% gap.

The Born-trace template makes the shortcut's structure
explicit (state-and-operator approximation), confirming that
S4 is a state-and-operator-pair selection issue, not a
matter of trace-template uniqueness. ∎

### M1.6 Sharpened decomposition

The parent matching residual is `M ≡ S4 ∧ S7` (T6 of the
parent match note). With the Born-trace extension:

```
S4 ≡ S4a ∧ S4b
S4a := operational form m_H² = Tr(ρ̂_phys · Ô_{m_H²})       [bounded support via G2 template]
S4b := selection of (ρ̂_phys, Ô_{m_H²}) from retained content  [open]
```

S4a is the trivial Born-rule expectation-value form for any
Hermitian observable; it follows directly from BornOp +
G2-Born. S4b is the genuinely load-bearing content — and it
composes with S7 to recover the parent matching residual:

```
S4 ∧ S7 ≡ S4a ∧ S4b ∧ S7
       ≡ [operational form, supported]
       ∧ [state-and-operator selection ∧ Δ² gap-closure functional, OPEN]
```

So the parent residual is unchanged; the Born-trace extension
narrows S4 into a sharpened state-and-operator-selection
sub-residual that is structurally fused with S7. ∎

## 5. Consistency with cited content

### C1 G2 unified Born map (G2-Born)

G2 establishes `ρ_grav(x) = Tr(ρ̂ · M̂(x))` is canonical for
all density operators. The trace template `Tr(ρ̂ · Ô)` for
arbitrary Hermitian `Ô` is the standard generalization. The
Born-trace mass-readout extension uses the same template
with `Ô = Ô_{m_H²}` instead of `Ô = M̂(x)`. No new framework
content is added; the extension uses existing trace-template
generality.

### C2 Born-rule operationalism (BornOp)

Per `CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`,
the Born rule is the operational connection between the
framework and observation. For the Higgs single-particle
state in the post-EWSB vacuum, the squared mass observable
expectation is the standard operational mass-readout. The
Born-trace template gives the operational form
`m_H² = Tr(ρ̂_Higgs · Ĥ²)` for a free Higgs at rest, or
equivalently `m_H² = ⟨Ω_v|Ô_{m_H²}|Ω_v⟩` for the vacuum
state. Both are instances of the trace template.

### C3 Physical-lattice baseline (PhysLatBase)

The lattice on `Z³` is physical. So `M̂(x) = |x⟩⟨x|` is
canonical (G2). The lattice effective potential `V_lat(φ)`
is also physical content (computed on the lattice
partition function). However, the **post-EWSB
stationary point** φ* and the curvature at φ* depend on
the **dynamics** of the lattice action under EWSB
stabilization, which is the Lane 2 S7 content. The
physical-lattice baseline supports the lattice surface but
does not derive the post-EWSB minimum.

### C4 Born rule layer separation (BornDynVsMeas)

`BORN_RULE_ANALYSIS_2026-04-11.md` is explicit that the
Born rule is at the measurement-readout layer, distinct
from dynamics. The Born-trace template extension respects
this separation: it provides the operational form for
mass-readout (measurement layer) but does not bridge the
dynamics-layer EWSB stabilization gap.

### C5 Tree-level mean-field shortcut (HiggsTree)

`HIGGS_MASS_FROM_AXIOM_NOTE.md` Step 5(b) explicitly
identifies `(m_H_tree/v)² = (4/u_0²)/N_taste` at the
symmetric point as a **tree-level mean-field
identification**, not a derivation of post-EWSB physical
mass. The +12% gap is the explicit measure of the
mean-field-identification error. The Born-trace extension
confirms this framing (M1.5 above): the shortcut is a
state-and-operator approximation, with S4b sharpening
the residual.

## 6. What this DOES establish

1. **Operational form for mass-readout.** The Born-trace
   template `m_H² = Tr(ρ̂_phys · Ô_{m_H²})` is the canonical
   operational form for the physical Higgs mass, derived
   from G2's unified Born map by replacing `M̂(x)` with
   `Ô_{m_H²}`. No new framework content; same template.

2. **Sharpened S4 decomposition.** The S4 residual splits
   into S4a (operational form, supported) and S4b (state-
   and-operator selection, open and structurally fused
   with S7).

3. **Layer separation made explicit.** The Born-trace
   template applies at the measurement-readout layer; the
   dynamics-level EWSB stabilization gap is not addressable
   by the Born-trace template alone.

4. **Mean-field shortcut framing.** The parent note's
   tree-level mean-field identification is recast in
   Born-trace language as a state-and-operator
   approximation: `(Ω_lat(0), Ô_{V''})` ≈ `(Ω_v, Ô_{m_H²})`.
   The +12% gap is the magnitude of this approximation
   error.

## 7. What this does NOT establish

- It does **NOT** close S4. The load-bearing state-and-
  operator selection (S4b) and the +12% gap-closure
  functional Δ² (S7) remain open.
- It does **NOT** unblock Lane 2 (Higgs mass from axiom).
  The parent matching residual `M ≡ S4 ∧ S7` is
  unchanged in scope.
- It does **NOT** introduce new repo-wide axioms or new
  derivation primitives.
- It does **NOT** consume PDG values as derivation inputs.
- It does **NOT** discharge the staggered-Dirac
  realization gate, the g_bare = 1 gate, or any other
  open framework gate.
- It does **NOT** derive the post-EWSB vacuum `Ω_v` from
  the symmetric-phase lattice surface. That is the open
  S7 content.

## 8. Empirical falsifiability

| Claim | Falsifier |
|---|---|
| M1.1 trace-template generality | Demonstrate a Hermitian observable `Ô` and density operator `ρ̂` for which `Tr(ρ̂ · Ô) ≠ ⟨Ô⟩`. Mathematically impossible. |
| M1.2 distinct observables | Demonstrate that `M̂(x) = |x⟩⟨x|` and `Ô_{m_H²}` are the same operator. Trivially false; ranks differ. |
| M1.3 state-selection gap | Demonstrate that the lattice symmetric-point vacuum `Ω_lat(0)` and the post-EWSB physical vacuum `Ω_v` are the same state. Trivially false; one has tachyonic curvature, the other has positive curvature. |
| M1.4 layer separation | Demonstrate that the Born rule applies at the dynamics layer (e.g., that Born-trace expectations alone determine post-EWSB stationary points). Contradicts `BORN_RULE_ANALYSIS_2026-04-11.md`. |
| M1.5 tree-level shortcut framing | Demonstrate that `(Ω_lat(0), Ô_{V''})` and `(Ω_v, Ô_{m_H²})` give the same Born-trace value. Trivially false; the +12% gap is the explicit measure of the discrepancy. |
| M1.6 S4 decomposition | Demonstrate a closure of S4 from current retained content alone (no S4a/S4b split needed). Contradicts the parent matching note's T3 obstruction. |

## 9. Verdict per brief's three honest outcomes

The originating brief listed three honest outcomes:

> 1. **CLOSURE**: G2 extends naturally to mass-readout; S4 closes; Lane 2 unblocked.
> 2. **STRUCTURAL OBSTRUCTION**: extension doesn't apply.
> 3. **SHARPENED**: partial extension.

**Verdict: SHARPENED (option 3).**

The G2 trace template DOES extend to a mass-readout operational
form `m_H² = Tr(ρ̂_phys · Ô_{m_H²})`. But three structural
distinctions (D1 distinct observables; D2 stationary-point
matching; D3 state-selection gap) prevent direct closure of S4.
The extension narrows S4 into a state-and-operator selection
sub-residual S4b that is structurally fused with S7. The parent
matching residual M ≡ S4 ∧ S7 ≡ S4a ∧ S4b ∧ S7 has S4a
bounded-supported, S4b ∧ S7 still open.

This sharpens the Lane 2 obstruction without closing it. Honest:
the Born-trace template is the right operational form for the
mass-readout, but it cannot bridge the dynamics-layer EWSB
stabilization that S4b ∧ S7 demands.

## 10. Honest scope (audit-readable)

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Sharpened sub-issue inside Lane 2 step S4 of the lattice-curvature
  → physical (m_H/v)² matching residual. Extends the G2 unified
  position-density Born map to a mass-readout operational form
  m_H² = Tr(rho_phys * O_{m_H^2}) by replacing the position-density
  observable M_hat(x) = |x><x| with a mass-curvature observable
  O_{m_H^2}. Trace template is shared (canonical Born expectation);
  observables are distinct in rank/support/physical interpretation.
  The extension narrows S4 into S4a (operational form, supported via
  G2 template extension) ∧ S4b (state-and-operator selection from
  retained content, open). S4b composes with S7 to recover the
  parent matching residual; Lane 2 remains blocked.

residual_engineering_admission: c_iso_e_witness_compute_frontier  # named, but does NOT bridge S4
residual_structural_admissions:
  - lattice_curvature_to_physical_m_h_v_squared_matching_theorem  # parent residual
  - tree_level_mean_field_readout_to_post_ewsb_mass_identification  # S4 (load-bearing, only S4a sharpened here)
  - state_and_operator_selection_for_born_trace_mass_readout  # S4b (this note's sharpening)
  - twelve_percent_gap_closure_functional_delta_squared  # S7 (load-bearing, unchanged)
  - n_taste_16_uniform_channel
  - g_bare_canonical_normalization
  - staggered_dirac_realization_gate

declared_one_hop_deps:
  - g_newton_born_as_source_positive_theorem_note_2026-05-10_gnewtong2
  - lattice_physical_matching_theorem_bounded_obstruction_note_2026-05-10_match
  - higgs_mass_from_axiom_note
  - higgs_mass_hierarchy_correction_note
  - born_rule_analysis_2026-04-11
  - physical_lattice_foundational_interpretation_note_2026-05-08
  - conventions_unification_companion_note_2026-05-08
  - minimal_axioms_2026-05-03

admitted_context_inputs:
  - tree_level_mean_field_readout_to_post_ewsb_mass_identification
  - state_and_operator_selection_for_born_trace_mass_readout
  - twelve_percent_gap_closure_functional_delta_squared
  - n_taste_16_uniform_channel
  - g_bare_canonical_normalization
  - staggered_dirac_realization_gate

load_bearing_step_class: bounded_theorem  # operational form supported; selection open
proposal_allowed: true
audit_required_before_effective_status_change: true
```

## 11. Cross-references

### Direct parents (this note's analysis subjects)

- [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md) — G2 unified Born map (template source)
- [`LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md`](LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md) — parent S4 ∧ S7 framing
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) — tree-level mean-field formula `m_H/v = 1/(2 u_0)`
- [`HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`](HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md) — proves L_t hierarchy correction does NOT close +12% gap
- [`BORN_RULE_ANALYSIS_2026-04-11.md`](BORN_RULE_ANALYSIS_2026-04-11.md) — Born rule layer separation (measurement vs dynamics)

### Repo baseline / meta

- [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

### Sister cluster (Lane 2 S4 ∧ S7 pieces)

- [`HIGGS_MASS_DERIVED_NOTE.md`](HIGGS_MASS_DERIVED_NOTE.md)
- [`HIGGS_FROM_LATTICE_NOTE.md`](HIGGS_FROM_LATTICE_NOTE.md)
- [`WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`](WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md)
- [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

## 12. Validation

```bash
python3 scripts/cl3_higgs_mass_s4_born_extension_2026_05_10_higgsS4.py
```

Expected: structural verification of (i) trace-template generality
(M1.1), (ii) distinct observables (M1.2: position vs mass; ranks
differ; expectations differ on the same state), (iii) state-selection
gap (M1.3: lattice symmetric vacuum ≠ post-EWSB vacuum; tachyonic vs
positive curvature), (iv) layer separation (M1.4: Born rule is
measurement, S4 matching is dynamics), (v) tree-level shortcut framing
(M1.5: numerical evidence of the +12% gap as state-and-operator
approximation error), (vi) sharpened S4 decomposition (M1.6: S4 ≡
S4a ∧ S4b; S4a supported; S4b ∧ S7 open). Total: PASS=42, FAIL=0.

Cached: [`logs/runner-cache/cl3_higgs_mass_s4_born_extension_2026_05_10_higgsS4.txt`](../logs/runner-cache/cl3_higgs_mass_s4_born_extension_2026_05_10_higgsS4.txt)

## 13. User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note does
  not assert "consistency = derivation". The Born-trace template
  extension is a structural derivation of the operational form
  from cited content (G2 + Born-rule operationalism). The S4 closure
  itself is NOT claimed; the verdict is honest sharpening.
- `feedback_hostile_review_semantics.md`: this note stress-tests
  the brief's hypothesis and identifies three structural
  distinctions (D1, D2, D3) that block direct closure. The
  brief's "extend G2 to mass-readout" is honored at the operational
  template layer but not at the load-bearing dynamics layer.
- `feedback_retained_tier_purity_and_package_wiring.md`: no
  automatic cross-tier promotion. This note is a bounded-theorem
  proposal sharpening one sub-issue inside Lane 2 step S4. Audit-
  lane authority on `effective_status` is preserved.
- `feedback_physics_loop_corollary_churn.md`: this is structurally
  new content. The Born-trace template extension to mass-readout
  is not a relabel of G2 (which addresses gravity-source readout)
  or of the parent matching note (which decomposes S4 by step
  classification). The new structural insight is the
  **state-and-operator-pair selection gap** (D2 + D3) revealed by
  the template extension, distinct from the prior framings.
- `feedback_compute_speed_not_human_timelines.md`: no time
  estimates. The verdict is described in terms of structural
  obstructions (D1, D2, D3) and what content suffices vs what
  remains open.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  packages the Born-trace mass-readout attack with sharp PASS/FAIL
  deliverables in the runner: M1.1 trace template, M1.2 distinct
  observables, M1.3 state-selection, M1.4 layer separation,
  M1.5 mean-field framing, M1.6 sharpened S4.
- `feedback_review_loop_source_only_policy.md`: source-only — this
  PR ships exactly (a) source theorem note, (b) paired runner,
  (c) cached output. No output-packets, lane promotions, synthesis
  notes, or "Block" notes.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: the parent
  Lane 2 S4 ∧ S7 residual is being fragmented further. This note
  isolates the operational-form sub-piece (S4a) as supported, and
  fuses the residual selection (S4b) with S7 into a single open
  block. No new framework premises; admissions named explicitly.

## 14. Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, avoid one-step
relabelings of already-landed cycles. This note:

- Is **NOT** a relabel of G2 (which is about gravity-source
  readout in position basis). The Born-trace mass-readout
  extension uses the same template but for a different
  observable (Higgs mass squared) on a different physical state
  (post-EWSB vacuum), with three structural distinctions (D1,
  D2, D3) requiring explicit identification.
- Is **NOT** a relabel of the parent matching note (which
  decomposes S4 by classification). The Born-trace extension
  introduces a new sub-decomposition S4 ≡ S4a ∧ S4b at the
  operational/selection layer.
- Is **NOT** a relabel of the parent tree-level note (which
  gives `m_H_tree = v/(2 u_0)` directly). The Born-trace
  framing recasts the tree-level shortcut as a state-and-
  operator approximation, making the +12% gap explicit as the
  approximation error.
- Provides **structurally new content**: the state-and-operator-
  pair selection gap revealed by the template extension. This
  is distinct from prior framings of S4 (asserted/derived
  binary) and S7 (gap-closure functional Δ²).

## 15. Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | No — the load-bearing S4 residual is sharpened but not closed. S4a (operational form) is bounded-supported via the G2 template; S4b (state-and-operator selection) and S7 (Δ² gap-closure) remain open. |
| V2 | New bounded support? | Yes — the Born-trace mass-readout operational form `m_H² = Tr(ρ̂_phys · Ô_{m_H²})` is structurally new support, derived from G2's template by changing the observable from `M̂(x)` to `Ô_{m_H²}`. The three structural distinctions (D1, D2, D3) and the S4a/S4b decomposition are also new content. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) the trace-template generality (M1.1), (ii) the distinctness of position vs mass observables (M1.2, verified numerically), (iii) the state-selection gap (M1.3, with tachyonic vs positive curvature numerical evidence), (iv) the layer separation (M1.4, citing Born rule analysis), (v) the tree-level shortcut framing (M1.5, with +12% gap as approximation error), (vi) the sharpened S4 decomposition (M1.6). |
| V4 | Marginal content non-trivial? | Yes — sharpening one sub-issue (S4a) inside a load-bearing residual (S4) of a Nature-grade matching theorem (Lane 2) is non-trivial while leaving the parent block open. The structural insight about state-and-operator selection gap is useful for guiding future probes on S4b ∧ S7. |
| V5 | One-step variant? | No — this is not a relabel of G2 or the parent matching note. The Born-trace mass-readout extension introduces structurally new content: the trace template applied to a different observable (mass squared, not position projector), the distinct-observable verification (M1.2), the state-selection gap (M1.3), the layer-separation invocation of `BORN_RULE_ANALYSIS_2026-04-11.md` (M1.4), and the S4a/S4b decomposition (M1.6). |

**Source-note V1-V5 screen: pass for bounded-theorem audit seeding.**
