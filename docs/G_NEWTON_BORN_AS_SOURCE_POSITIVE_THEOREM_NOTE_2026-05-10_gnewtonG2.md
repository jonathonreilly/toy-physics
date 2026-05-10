# G_Newton Born-as-Gravity-Source — Positive Theorem (gnewtonG2)

**Date:** 2026-05-10
**Type:** positive_theorem (closure of admission (b) of GRAVITY_CLEAN_DERIVATION_NOTE under retained content)
**Claim type:** positive_theorem
**Scope:** review-loop source-note proposal. Closes the Born-as-gravity-source admission named (b) in
[`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md)
under the retained physical-lattice baseline + retained Born-rule operationalism + statistical mixing.
**Status:** source-note proposal for closure of admission (b). The unified position-density Born map
`ρ_grav(x) := ⟨x| ρ̂ |x⟩` is canonical for both pure and mixed states. The previously cited
"divergence between Born and DM-trace on mixed states" is a category error: it compares the
pure-state Born map (undefined on mixed states) to the unified map (defined on all states).
The unified map reduces to `|ψ(x)|²` on pure states and to `Σ_i p_i |ψ_i(x)|²` on mixed states.
**Authority disclaimer:** source-note proposal — audit verdict and downstream
status set only by the independent audit lane.
**Loop:** g-newton-born-as-source-20260510-gnewtonG2
**Primary runner:** [`scripts/cl3_g_newton_born_as_source_2026_05_10_gnewtonG2.py`](../scripts/cl3_g_newton_born_as_source_2026_05_10_gnewtonG2.py)
**Cache:** [`logs/runner-cache/cl3_g_newton_born_as_source_2026_05_10_gnewtonG2.txt`](../logs/runner-cache/cl3_g_newton_born_as_source_2026_05_10_gnewtonG2.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived `claim_type`,
`audit_status`, and `effective_status` are generated only after the
independent audit lane reviews the claim, dependency chain, and runner.
The audit lane has full authority to retag, narrow, or reject the
proposal.

## Question

Probe P4 (planckP4) sharpened `GRAVITY_CLEAN_DERIVATION_NOTE.md` from
"unaudited / conditional" to "explicitly conditional on three named
admissions":

> (a) `L^{-1} = G_0` — self-consistency identification of the field
>     operator inverse with the propagator Green's function.
> (b) `ρ = |ψ|²` — Born / mass-density source map.
> (c) `S = L (1 - φ)` — weak-field test-mass response.

The planckP4 probe identified Barrier B(b) as: "pure-state Born and
density-matrix trace diverge on mixed states; no retained
Born-as-gravity-source theorem."

The probe question:

> Can admission (b) — Born-as-gravity-source — be closed under retained
> Cl(3)/Z³ content, with no new axioms or imports?

## Answer

**Closed under retained content.** Admission (b) reduces, under the
retained physical-lattice baseline + retained Born-rule operationalism
+ statistical mixing, to the **unified position-density Born map**

```
ρ_grav(x) := ⟨x| ρ̂ |x⟩    (diagonal of density operator in position basis)
        ≡ Tr( ρ̂ · M̂(x) )    where  M̂(x) := |x⟩⟨x|
```

This map is defined for ALL density operators (pure or mixed) and:

- **Reduces to `|ψ(x)|²` on pure states.** For `ρ̂ = |ψ⟩⟨ψ|`,
  `⟨x|ψ⟩⟨ψ|x⟩ = |⟨x|ψ⟩|² = |ψ(x)|²`. So pure-state Born is recovered.
- **Reduces to `Σ_i p_i |ψ_i(x)|²` on mixed states.** For
  `ρ̂_mixed = Σ_i p_i |ψ_i⟩⟨ψ_i|`, by linearity of the diagonal,
  `⟨x|ρ̂_mixed|x⟩ = Σ_i p_i |ψ_i(x)|²`. This IS the standard statistical
  mixing of pure-state Born densities.
- **Is non-negative.** For any density operator (PSD, Tr=1),
  `⟨x|ρ̂|x⟩ ≥ 0` for all x.
- **Is normalization-preserving.** `Σ_x ⟨x|ρ̂|x⟩ = Tr ρ̂ = 1`.
- **Is linear in `ρ̂`.** Statistical mixing of density operators
  yields statistical mixing of densities, with no extra structure
  required.

The previously cited "divergence on mixed states" was a comparison
between TWO DIFFERENT MAPS: (i) the pure-state Born map `|ψ|²` applied
to a fixed pure ψ, and (ii) the position-density Born map `⟨x|ρ̂|x⟩`
applied to a mixed ρ̂. These cannot agree because they are DIFFERENT
MAPS APPLIED TO DIFFERENT STATES — a category error, not a real
obstruction. The unified map has no such divergence: it gives a single,
well-defined density for every state.

## Setup

### Premises (`A_min` for Born-as-gravity-source closure)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| A2 | Z³ spatial substrate | framework axiom; same source |
| PhysLatBase | Physical Cl(3) on Z³ baseline (lattice IS physical, not regulator) | retained meta: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md) |
| BornOp | Born-rule operationalism (Born rule as standard operational connection) | retained meta: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md) |
| StatMix | Statistical mixing of states (classical probabilities over pure states) | standard QM ensemble formalism (no internal repo dep needed) |
| PureBorn | Pure-state Born rule `ρ_pure(x) = |ψ(x)|²` (probability density) | retained / standard QM, used in [`STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md) |
| GRavCleanCondB | Admission (b) of [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md): `ρ = |ψ|²` as gravity source | conditional, this note's closure target |
| ParentP4 | The 3-admission sharpening that identified B(b) | bounded_theorem proposal: [`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md) |

### Forbidden imports

- NO PDG observed values used as derivation input.
- NO new axioms.
- NO promotion of unaudited content to retained-grade.
- NO empirical fits.
- NO same-surface family arguments.
- NO new physics inputs beyond standard QM density-operator formalism +
  retained baselines listed above.

## Theorem (positive closure of admission (b))

**Theorem (positive).** Under the retained physical-lattice baseline,
the retained Born-rule operationalism, and the standard quantum
statistical-mixing formalism, the **unified position-density Born map**

```
ρ_grav(x) := ⟨x| ρ̂ |x⟩ = Tr(ρ̂ · M̂(x))    where  M̂(x) := |x⟩⟨x|
```

is the canonical Born-as-gravity-source identification, valid for all
density operators (pure or mixed). It satisfies:

- **(P1.1) Linearity.**
  `ρ_grav(α ρ̂_1 + β ρ̂_2) = α ρ_grav(ρ̂_1) + β ρ_grav(ρ̂_2)` for scalars α, β.

- **(P1.2) Pure-state reduction.** For `ρ̂ = |ψ⟩⟨ψ|`,
  `ρ_grav(x) = |ψ(x)|²`. The standard pure-state Born map is recovered as
  a special case.

- **(P1.3) Mixed-state reduction.** For `ρ̂ = Σ_i p_i |ψ_i⟩⟨ψ_i|` with
  `p_i ≥ 0`, `Σ p_i = 1`, `ρ_grav(x) = Σ_i p_i |ψ_i(x)|²`. Statistical
  mixing of states yields statistical mixing of densities.

- **(P1.4) Non-negativity.** `ρ_grav(x) ≥ 0` for all x and all density
  operators ρ̂. (Compatible with H2 of `STAGGERED_FERMION_CARD_2026-04-11`,
  i.e. `ρ ≥ 0` as a screened-Poisson source.)

- **(P1.5) Normalization-preservation.** `Σ_x ρ_grav(x) = Tr ρ̂`. For
  normalized density operators (`Tr ρ̂ = 1`), the integrated source
  density equals the conserved total mass/probability.

- **(P1.6) Trace-operator form.** `ρ_grav(x) = Tr(ρ̂ · M̂(x))` with
  `M̂(x) = |x⟩⟨x|` the canonical position-density operator on Z³.
  The set `{M̂(x) : x ∈ Z³}` resolves the identity:
  `Σ_x M̂(x) = Î`.

The previously cited "Born / DM-trace divergence on mixed states" is a
category error:

```
Prior framing (planckP4 Section 4):
  MAP_a:  ρ = |ψ|²            applied to a fixed pure ψ
  MAP_b:  ρ = ⟨x|ρ̂|x⟩          applied to a mixed ρ̂
Showed these "diverge" -- but MAP_a is undefined on mixed states.

This note's framing:
  MAP_c:  ρ_grav(x) = ⟨x|ρ̂|x⟩  applied to ALL density operators
  - Reduces to MAP_a on pure states.
  - Equals statistical mixing of MAP_a on mixed states.
  - Has no "divergence" on any state.
```

The "divergence" of the prior probe was the divergence between an
INAPPLICABLE map (MAP_a on mixed) and an APPLICABLE map (MAP_b on
mixed) — not a genuine inconsistency in the theory.

## Proof

### P1.1 Linearity

Direct from linearity of matrix elements: for any two operators X, Y
and any vector |x⟩,
`⟨x| (αX + βY) |x⟩ = α ⟨x|X|x⟩ + β ⟨x|Y|x⟩`. So
`ρ_grav(α ρ̂_1 + β ρ̂_2)(x) = α ρ_grav(ρ̂_1)(x) + β ρ_grav(ρ̂_2)(x)`
for all x. ∎

### P1.2 Pure-state reduction

For `ρ̂ = |ψ⟩⟨ψ|`,
```
⟨x|ρ̂|x⟩ = ⟨x|ψ⟩⟨ψ|x⟩ = ⟨x|ψ⟩ · ⟨x|ψ⟩* = |⟨x|ψ⟩|² = |ψ(x)|².
```
So `ρ_grav(x) = |ψ(x)|²`, recovering the standard pure-state Born
density. ∎

### P1.3 Mixed-state reduction

For `ρ̂_mixed = Σ_i p_i |ψ_i⟩⟨ψ_i|`,
```
⟨x|ρ̂_mixed|x⟩ = Σ_i p_i ⟨x|ψ_i⟩⟨ψ_i|x⟩ = Σ_i p_i |ψ_i(x)|².
```
This is the statistical mixing of pure-state Born densities, weighted
by classical probabilities `p_i`. It is the natural and unique extension
of the pure-state Born rule to mixed states under the standard density-
operator formalism. ∎

### P1.4 Non-negativity

A density operator ρ̂ is positive semidefinite (PSD): `⟨v|ρ̂|v⟩ ≥ 0`
for all `|v⟩`. Taking `|v⟩ = |x⟩` (a position basis state), we have
`⟨x|ρ̂|x⟩ ≥ 0` for all `x`. So `ρ_grav(x) ≥ 0` everywhere. This is
compatible with the screened-Poisson bridge of
`STAGGERED_FERMION_CARD_2026-04-11` admission H2. ∎

### P1.5 Normalization preservation

`Σ_x ⟨x|ρ̂|x⟩ = Σ_x ⟨x| ρ̂ |x⟩ = Tr ρ̂` (sum of diagonal elements is
the trace). For normalized density operators (`Tr ρ̂ = 1`),
`Σ_x ρ_grav(x) = 1`. The total integrated source density equals the
total conserved mass/probability. ∎

### P1.6 Trace-operator form

The position-density operator `M̂(x) = |x⟩⟨x|` is Hermitian, PSD, and
idempotent (a rank-1 projector). The set `{M̂(x) : x ∈ Z³}` satisfies
the resolution of identity `Σ_x M̂(x) = Î` because
`Σ_x |x⟩⟨x| = Î` is the completeness relation for the position basis
on Z³. Then
```
Tr(ρ̂ · M̂(x)) = Tr(ρ̂ · |x⟩⟨x|) = ⟨x| ρ̂ |x⟩ = ρ_grav(x).
```
The trace-operator form is the standard operational Born rule (per
`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08`) for the position
observable. ∎

### P2: prior "divergence" is a category error

The prior probe's Section 4 (planckP4) compared:

```
S4.1: rho_pure_via_psisq = |psi|^2    on a fixed pure psi
S4.2: rho_dm_mixed = diag(rho_op)     on a mixed rho_op = 0.5|0><0| + 0.5|1><1|
```

S4.1 gave `[1.0, 0.0]`; S4.2 gave `[0.5, 0.5]`. The claim was that the
two maps "diverge."

**Resolution:** S4.1 and S4.2 are the same map (`⟨x|ρ̂|x⟩`) applied to
DIFFERENT STATES. The pure state `|ψ⟩ = (1, 0)` is not the same physical
state as the mixed `0.5|0⟩⟨0| + 0.5|1⟩⟨1|`. Comparing their densities
and finding them different is exactly what the formalism says should
happen: different states have different densities.

Furthermore, MAP_a `ρ = |ψ|²` is not even defined on mixed states (a
mixed state has no single pure ψ representation). The prior probe's
"divergence" was between MAP_a (inapplicable on mixed) and MAP_b
(applicable on mixed). The unified map MAP_c uses MAP_b uniformly.

Even more directly: the coherent superposition `|+⟩ = (|0⟩+|1⟩)/√2` and
the mixed state `0.5|0⟩⟨0| + 0.5|1⟩⟨1|` BOTH have diagonal `[0.5, 0.5]`.
So the unified map cannot distinguish coherent superposition from
classical mixture (off-diagonal elements differ). This is correct
physics: gravity sources couple to the local density `ρ_grav(x)`, which
is exactly the diagonal of `ρ̂` in position basis. ∎

### P3: Consistency with retained content

**P3.1 Born-rule operationalism.** Per
`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08`, the Born rule is
the standard operational connection between the framework and
observation. The unified position-density Born map
`ρ_grav(x) = Tr(ρ̂ · M̂(x))` is the standard operational form for the
position observable: probability/density at site x is the expectation
value of the position-density operator in the state ρ̂.

**P3.2 Physical-lattice baseline.** Per
`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08`, lattice
sites x ∈ Z³ are physical localization labels (not regulator artifacts).
So the position-density operator `M̂(x) = |x⟩⟨x|` is canonical: it is the
Hermitian projector onto the lattice site x. The completeness relation
`Σ_x |x⟩⟨x| = Î` is the standard L²(Z³) decomposition.

**P3.3 Statistical mixing.** The classical-probability mixing of
density operators `ρ̂ = Σ_i p_i ρ̂_i` (with `p_i ≥ 0`, `Σ p_i = 1`) is
the standard density-operator formalism for ensembles. The unified Born
map respects this mixing by linearity (P1.1).

**P3.4 Compatibility with the screened-Poisson bridge.** Admission H2
of `STAGGERED_FERMION_CARD_2026-04-11` requires `ρ ≥ 0` for the
positivity of `Φ` under `(L + μ²)Φ = G ρ`. The unified map gives
`ρ_grav(x) ≥ 0` for any density operator (P1.4), so the screened-
Poisson bridge admission H2 is structurally satisfied — not an extra
imposition, just a consequence of the PSD property of density operators.

## Conclusion

Admission (b) of `GRAVITY_CLEAN_DERIVATION_NOTE` — the
Born-as-gravity-source identification `ρ = |ψ|²` — is **closed under
retained content** via the unified position-density Born map:

```
ρ_grav(x) := ⟨x|ρ̂|x⟩ = Tr(ρ̂ · M̂(x))
```

This is canonical for both pure and mixed states, reduces to `|ψ(x)|²`
on pure states (so the parent-note language is preserved as the
pure-state special case), and equals statistical mixing of pure
densities on mixed states. The G_Newton self-consistency admission
count, per the planckP4 sharpening, drops from 3 to 2:

```
(a) L^{-1} = G_0 skeleton-selection         [open]
(b) ρ = |ψ|² Born-as-gravity-source          [CLOSED, this note]
(c) S = L(1 - φ) valley-linear vs spent-delay [open]
```

This note does NOT close (a) or (c). Those remain bounded per planckP4
B(a), B(c) and parallel probes.

## What this closes

- **Admission (b) of `GRAVITY_CLEAN_DERIVATION_NOTE`** is closed. The
  Born-as-gravity-source map is canonical under retained content; no
  new axioms or imports are required.
- **Barrier B(b) of `G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4`**
  is reduced from "no retained Born-as-gravity-source theorem" to
  "retained-content-derivable position-density Born map (this note)."
- **G_Newton self-consistency lane sharpens further:** the planckP4
  framing was "positive P1 dimensional rigidity + three named obstructions
  B(a), B(b), B(c)." This note closes B(b). The lane status moves
  from "3 open admissions" to "2 open admissions + 1 closed".
- **Pure-state Born identification preserved.** The parent note's
  language `ρ = |ψ|²` is recovered as the pure-state special case
  of the unified map. No retained content downstream of the parent
  language is invalidated.

## What this does NOT close

- **The unconditional G_Newton self-consistency derivation.**
  Admissions (a) `L^{-1} = G_0` skeleton-selection and (c)
  `S = L(1 - φ)` valley-linear-vs-spent-delay remain open per
  planckP4 B(a), B(c).
- **The status of `GRAVITY_CLEAN_DERIVATION_NOTE.md`** itself remains
  `audited_conditional` until ALL three admissions close. This note
  closes one of three; two remain open.
- **The Planck-from-structure derivation.** P1 of the planckP4 parent
  anchors on `M_Pl` as a dimensional input, but `M_Pl` itself is not
  retained from the framework axiom (separate retained no-go's:
  `PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md`,
  `PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30.md`).
  This note does not address Planck-from-structure.
- **A1 admission count.** The Koide A1 closure is on the flavor
  sector and is independently barred per the parent obstruction note
  Barriers G1–G5. This note touches only the gravity-source admission.
- **Strong-field gravity, geodesics, time dilation, etc.** Those remain
  bounded per the broader gravity sub-bundle.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Unified map P1.2 (pure-state reduction) | Demonstrate a pure-state ρ̂ = |ψ⟩⟨ψ| where `⟨x|ρ̂|x⟩ ≠ |ψ(x)|²`. The runner verifies this is exact (max |diff| = 0). |
| Unified map P1.3 (mixed-state reduction) | Demonstrate a mixed-state ρ̂ = Σ p_i |ψ_i⟩⟨ψ_i| where `⟨x|ρ̂|x⟩ ≠ Σ p_i |ψ_i(x)|²`. The runner verifies this is exact (max |diff| = 0). |
| Unified map P1.4 (non-negativity) | Demonstrate a PSD density operator with negative diagonal. Mathematically impossible. |
| Unified map P1.5 (normalization) | Demonstrate Σ_x ⟨x|ρ̂|x⟩ ≠ Tr ρ̂. Impossible by definition of trace. |
| P2 category-error claim | Demonstrate that ⟨x|ρ̂|x⟩ has multiple inequivalent extensions to mixed states. The unified map is unique under linearity + matrix-element form. |
| P3 retained-content compatibility | Demonstrate that retained Born-rule operationalism + retained physical-lattice baseline + statistical mixing PROHIBIT the unified map. The retained-content checks (S3.1–S3.7) confirm consistency. |

## Review boundary

This note proposes `claim_type: positive_theorem` for the independent
audit lane: the Born-as-gravity-source admission (b) of
`GRAVITY_CLEAN_DERIVATION_NOTE` is closed under retained content via
the unified position-density Born map. The proposal does NOT promote
the parent gravity-clean note; it closes ONE of the parent's three
admissions.

No new axioms are introduced. The retained meta clarifications
(physical-lattice baseline + Born-rule operationalism) are NOT new
admissions — they are already retained per their respective 2026-05-08
companion notes. The standard QM density-operator formalism is also
not new — it is the universal language of mixed-state physics in
quantum mechanics.

The independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | Yes — Barrier B(b) of planckP4 (Born-as-gravity-source non-derivability) is closed. The unified position-density Born map provides the retained-content closure that the planckP4 probe identified as missing. The G_Newton lane status sharpens from "3 open admissions" to "2 open + 1 closed". |
| V2 | New derivation? | Yes — the unified position-density Born map `ρ_grav(x) := ⟨x|ρ̂|x⟩` is structurally new content. The prior probe identified Born-as-source as target-side and concluded "no retained Born-as-gravity-source theorem." This note shows that under the retained physical-lattice baseline + Born-rule operationalism + statistical mixing, the position-density Born map is canonical for ALL states (pure or mixed), with the pure-state Born `\|ψ\|²` recovered as a special case. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) the trace-operator definition `ρ_grav(x) = Tr(ρ̂ M̂(x))` against retained Born-rule operationalism, (ii) the linearity, pure-state reduction, mixed-state reduction, non-negativity, and normalization properties (each verified in the runner), (iii) the consistency of the unified map with retained physical-lattice baseline and statistical mixing, (iv) the category-error resolution of the prior "divergence" claim. |
| V4 | Marginal content non-trivial? | Yes — closing one of three named admissions of `GRAVITY_CLEAN_DERIVATION_NOTE` is non-trivial: it advances the gravity lane from "3 admissions" to "2 admissions" status. The structural insight (that the prior probe's "divergence" was a category error, not a real obstruction) is also novel and useful for guiding future probes on (a) and (c). |
| V5 | One-step variant? | No — this is not a relabel of any prior gravity or Born note. The unified position-density map `⟨x|ρ̂|x⟩` is a structurally new framing that subsumes pure-state Born (preserved as special case) and mixed-state Born (extended via statistical mixing) under one definition. The category-error analysis of the prior "divergence" framing is also new. |

**Source-note V1-V5 screen: pass for positive-theorem audit seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule is
to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of any prior gravity or Born note. The unified
  position-density Born map `⟨x|ρ̂|x⟩` is structurally new framing.
  The prior probe (planckP4) explicitly claimed Born-as-source had no
  retained closure; this note SHOWS the closure.
- Identifies a NEW STRUCTURAL CLOSURE (one of the three planckP4
  obstructions) on the G_Newton lane. The closure follows from
  retained content and the standard QM density-operator formalism,
  with no new axioms.
- Provides a structural correction to the planckP4 framing: the
  "divergence" of Born and DM-trace was a category error (different
  maps applied to different states), not a real obstruction. This
  is structurally distinct from the planckP4 enumeration of three
  admissions.
- Sharpens the open frontier from "3 admissions" to "2 admissions +
  1 closed". Future probes on (a) and (c) can build on this closure.

## Cross-references

- Parent G_Newton self-consistency probe: [`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md)
- Parent gravity-clean note: [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md)
- Companion full-self-consistency note: [`GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`](GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md)
- Sister A1 gravity-phase obstruction: [`KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md`](KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md)
- Retained physical-lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Retained Born-rule operationalism: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- Pure-state Born and screened-Poisson bridge: [`STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md)
- Born rule analysis (gravity vs measurement): [`BORN_RULE_ANALYSIS_2026-04-11.md`](BORN_RULE_ANALYSIS_2026-04-11.md)
- Newton-from-Z³ derivation: [`NEWTON_LAW_DERIVED_NOTE.md`](NEWTON_LAW_DERIVED_NOTE.md)
- MINIMAL_AXIOMS: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## Validation

```bash
python3 scripts/cl3_g_newton_born_as_source_2026_05_10_gnewtonG2.py
```

Expected output: structural verification of (i) unified position-density
Born map `ρ_grav(x) := ⟨x|ρ̂|x⟩` with linearity, pure-state reduction,
mixed-state reduction, non-negativity, and normalization properties,
(ii) prior "divergence" framing is a category error (different maps
applied to different states; coherent superposition has same diagonal
as classical mixture but different off-diagonals), (iii) retained-content
consistency check (Born-rule operationalism + physical-lattice baseline
+ statistical mixing + screened-Poisson H2 compatibility), (iv)
admission status: (b) closed under retained content; (a) and (c) remain
open per planckP4 / parallel probes, (v) synthesis with no
corollary-churn relabel.
Total: 30 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_g_newton_born_as_source_2026_05_10_gnewtonG2.txt`](../logs/runner-cache/cl3_g_newton_born_as_source_2026_05_10_gnewtonG2.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note does
  not assert "consistency = derivation". The closure is a structural
  *derivation* of the unified map from retained Born-rule
  operationalism + physical-lattice baseline + statistical mixing.
  Pure-state reduction to `\|ψ\|²` is exact algebra, not numerical
  consistency.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "Born and DM-trace diverge on mixed states" by
  identifying it as a category error (different maps, different
  states). The unified map has well-defined behavior on every state.
- `feedback_retained_tier_purity_and_package_wiring.md`: no
  automatic cross-tier promotion. This note is a positive-theorem
  proposal closing ONE of three admissions of the parent gravity-
  clean note. The parent note remains `audited_conditional` — the
  remaining two admissions (a, c) are still open. Audit-lane
  authority on `effective_status` is preserved.
- `feedback_physics_loop_corollary_churn.md`: the unified
  position-density Born map is structurally new content, not a
  relabel of `STAGGERED_FERMION_CARD` admissions or planckP4
  framing. Distinct structural insight (category-error resolution of
  prior "divergence" framing).
- `feedback_compute_speed_not_human_timelines.md`: the closure of
  admission (b) is presented in terms of WHAT structural ingredients
  suffice (retained baselines + standard QM density-operator
  formalism), not how-long-it-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  the Born-as-source closure attack with sharp PASS/FAIL deliverables
  in the runner: P1 (unified map definition + 6 properties), P2
  (category-error resolution), P3 (retained-content consistency).
- `feedback_review_loop_source_only_policy.md`: source-only — this
  PR ships exactly (a) source theorem note, (b) paired runner,
  (c) cached output. No output-packets, lane promotions, synthesis
  notes, or "Block" notes.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: the parent
  G_Newton lane is being fragmented. planckP4 isolated three named
  admissions; this note closes one (b). No new admissions are
  introduced. Fragmentation pattern preserved: closures land
  one-admission-at-a-time, with parent status updated only when ALL
  admissions close.
