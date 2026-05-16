# Newtonian Mass Scaling from Four Principles (bounded family-law note)

**Date:** 2026-04-04 (scope-documentation refresh 2026-05-16)
**Status:** open_gate. Additivity strengthens Principle 3 on the retained ordered-lattice family, and the 2026-05-07 multistage compact-object bridge operationally satisfies the *self-sourcing* half of Principle 3 on the audit-clean `top4` family; the residual gate is the *external-field* generator-invariant inertial-mass step on a persistent compact-object family. See the new "Open Gate Scope" section below for the precise audit boundary.

## The Claim

The strongest bounded claim currently supported is:

on the retained ordered-lattice family, Newtonian mass scaling is selected when
all of the following hold together:

1. Linear amplitude propagation (Born rule)
2. Phase valley (gravitational attraction)
3. Additive one-parameter mass (`m ∝ s` under the same composition law)
4. Momentum conservation (action-reaction symmetry)

This is a family-level statement only. It does **not** claim architecture-
independent uniqueness, and it does **not** claim that the action is uniquely
forced by the axioms on arbitrary graphs or lattices.

The open step is still whether Principle 3 can be made real for persistent
patterns rather than only for the current test-particle/composition harnesses.

## The Argument

### Principle 1: Linear propagator → Born rule

The amplitude at node j is a linear sum of contributions from
connected nodes: ψ_j = Σ K(i→j) ψ_i. This gives the Sorkin test
I₃ = 0 (Born rule) for ANY action formula. Born does not constrain
the action.

Verified: I₃/P < 5e-15 for all tested actions (p=0.5 to p=2.0).

### Principle 2: Phase valley → TOWARD gravity

The action S = L × g(f) with g'(0) < 0 creates a phase deficit
near mass. This produces constructive interference on the mass side,
shifting the centroid TOWARD the mass.

Phase HILL (g'(0) > 0) gives AWAY (repulsion). Zero coupling gives
no gravity. The phase valley is the unique mechanism for attraction.

### Principle 3: Additivity / one-parameter mass

The weakest step is still the identification of the field-source parameter
with the inertial quantity that weights momentum.

What is now frozen:

- the dedicated equivalence harness shows that global amplitude scaling cancels
  exactly in the centroid ratio on the linear test-particle family
- but localized packet shape still changes the response strongly
- the dedicated composite-source harness shows that, on the same weak-field
  test-particle family, valley-linear source composition is additive while
  spent-delay is not
- a second-family 2D ordered-lattice probe now shows the same bounded
  valley-linear additivity story while spent-delay remains strongly
  non-additive

Artifact chains:

- [`scripts/equivalence_principle_harness.py`](/Users/jonreilly/Projects/Physics/scripts/equivalence_principle_harness.py)
- [`logs/2026-04-04-equivalence-principle-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-equivalence-principle-harness.txt)
- [`docs/EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md)
- [`scripts/composite_source_additivity_harness.py`](/Users/jonreilly/Projects/Physics/scripts/composite_source_additivity_harness.py)
- [`logs/2026-04-04-composite-source-additivity-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-composite-source-additivity-harness.txt)
- `docs/COMPOSITE_SOURCE_ADDITIVITY_NOTE.md` (sibling artifact in same lane; cross-reference only — not a one-hop dep of this note)
- [`scripts/composite_source_additivity_2d_cross_family.py`](/Users/jonreilly/Projects/Physics/scripts/composite_source_additivity_2d_cross_family.py)
- [`logs/2026-04-04-composite-source-additivity-2d-cross-family.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-composite-source-additivity-2d-cross-family.txt)
- `docs/COMPOSITE_SOURCE_ADDITIVITY_2D_NOTE.md` (sibling artifact in same
  lane; cross-reference only — not a one-hop dep of this note)

This is enough for a stronger bounded statement:

- if the inertial quantity of a persistent pattern is an extensive quantity
  attached to the same composition law as the field-source parameter `s`,
  then `m ∝ s`

What is still missing is a persistent-pattern or quasi-persistent localized
state whose inertial response can actually be measured on the lattice.

So Principle 3 is **stronger than a bare assumption**, but it is still **not
closed** by the current code.

### Principle 4: Momentum conservation → p = 1

With action S = L(1-f^p), the deflection of a test particle in
field f ∝ s/r scales as s^p (the F∝M = p universality law).

Two particles A (coupling s_A) and B (coupling s_B) at separation r:
- Deflection of A by B's field: ∝ s_B^p
- Deflection of B by A's field: ∝ s_A^p

Define momentum: p = m × v_centroid, with `m ∝ s` under Principle 3.
- p_A = s_A × s_B^p × g(r)
- p_B = s_B × s_A^p × g(r)

Momentum conservation: p_A + p_B = 0 requires
  s_A × s_B^p = s_B × s_A^p
  (s_A/s_B)^(p-1) = 1

This holds for ALL mass ratios s_A/s_B only if **p = 1**.

### Conclusion

With p = 1: F ∝ s_A × s_B / r^(d-2) on a d-dimensional lattice.
In 3+1D (d=3): F ∝ M₁M₂/r on the retained ordered-lattice family.
This is the Newtonian mass-scaling law on that family; the persistent-pattern
version of the argument remains open.

## Numerical Evidence

| Test | Result |
|------|--------|
| F∝M = p (5 powers) | Exact: 0.50, 0.75, 1.00, 1.50, 2.00 |
| Born (all actions) | < 5e-15 |
| Two-body momentum (`m ∝ s`) | Valley-linear conserved to `0.0-0.1%`; spent-delay violated by `42-55%` at unequal masses |
| Distance tail (p=1) | b^(-1.07), near Newtonian |
| Amplitude-level equivalence | Exact under global amplitude rescaling |
| Packet-shape independence | Fails on the bounded localized-packet probe |
| Valley same-site / disjoint additivity | Exact to printed precision on the weak-field test-particle family |
| Valley additivity on second retained family | `<= 0.08%` on the 2D ordered-lattice cross-check |
| Spent-delay same-site / disjoint additivity | Violated by 24-29% on the same family |

## Persistent-Pattern Control

The smallest viable persistent-pattern check was run and did not close the gap:

- the packet re-identification control stayed visually stable, but that only
  supports a bounded re-identification diagnostic
- the stricter persistent inertial-object probe found no admissible class that
  met the capture / carry / shift thresholds
- the leading row was still a broad surrogate, not a persistent-pattern
  inertial object

So the review branch still lacks a localized state whose inertial response can
be measured as a closed one-parameter mass. Principle 3 is stronger than a bare
assumption, but it is not closed for persistent patterns.

### Multistage compact-object bridge (2026-05-07)

Since the original control sweeps, the audit-clean
`persistent_object_top4_multistage_transfer_sweep_note_2026-04-16` has
registered a multistage compact-object floor that survives 11/13 widened-
pocket cases at `top_keep = 4` with `stage_mean_overlap >= 0.90`,
`stage_alpha in [0.95, 1.05]`, and `max_kappa_drift = 0.000%` on the
admissible rows. A new bridge note documents how this changes the local
picture without promoting the gate:

- [`docs/NEWTON_DERIVATION_TOP4_BRIDGE_NOTE.md`](NEWTON_DERIVATION_TOP4_BRIDGE_NOTE.md)
  — bounded conditional bridge note; the same scalar `s` controls
  source strength, linear response (`alpha = 1`), and persistence on
  the audit-clean multistage compact-object family.
- [`scripts/newton_derivation_top4_bridge_runner.py`](../scripts/newton_derivation_top4_bridge_runner.py)
  — primary runner for the bridge note.

The bridge does **not** close `newton_derivation_note`. It narrows the
residual to a concrete experimental target: does the same multistage
compact-object family exhibit generator-invariant response under an
*external* field (i.e. under a field sourced by a different compact
object), or does the equivalence-principle no-go from
`matter_inertial_closure_note` recur on the multistage object as well?

## What This Does NOT Prove

1. It does not derive the dimension d of spacetime
2. It does not derive the lattice geometry (still imposed)
3. It does not derive the specific form of g(f) — only that g must
   be linear in f at weak field
4. Principle 3 is stronger than before because additivity now supports
   `m ∝ s` on the weak-field test-particle family, but it is still not a
   derived persistent-pattern theorem
5. The current equivalence and additivity harnesses only close the
   test-particle response statement; they do not yet produce a
   persistent-pattern inertial mass

## Promotion Guidance

Do **not** promote the stronger theorem framing:

- “valley-linear is uniquely forced by the axioms”
- “Newtonian mass scaling is architecture-independent”
- “the action is uniquely determined on arbitrary graphs”

## The Strongest Safe Statement

"On the retained ordered-lattice family, if the propagator is linear, the
action creates a phase valley, the inertial quantity is extensive under the
same composition law as the field-source parameter, and momentum is conserved,
then `p = 1` is selected and the Newtonian mass-scaling law follows on that
family. The open step in the current project is still the persistent-pattern
version of that extensive one-parameter mass principle, so this remains a
hold rather than a mainline closure."

## Open Gate Scope (scope-documentation, 2026-05-16)

This note is scoped as an `open_gate` row. The intent of this section is to
fix the precise scope of the open step so that re-audit can re-confirm the
gate at the same boundary or recognise a narrower residual.

### What is closed inside this note

| Sub-claim | Status | Authority |
|---|---|---|
| Principle 1 (linear propagator → Born `I_3 = 0`) | closed on all tested actions `p in [0.5, 2.0]` to `< 5e-15` | this note, Numerical Evidence table |
| Principle 2 (phase valley → attraction; hill → repulsion; zero coupling → no gravity) | closed on the retained ordered-lattice family | this note, Principle 2 section |
| Principle 3a (amplitude-scaling invariance on test-particle family) | retained_bounded | [`EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md`](EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md) |
| Principle 3b (valley-linear additivity of source composition on weak-field test-particle family, 3D and 2D ordered-lattice cross-check) | retained_bounded | this note, Numerical Evidence table; sibling additivity notes |
| Principle 3c (operational extensivity of `s` on the audit-clean `top4` multistage compact-object family under self-sourcing: persistence, `alpha = 1`, stage-stable `kappa`) | bounded conditional bridge, support tier | [`NEWTON_DERIVATION_TOP4_BRIDGE_NOTE.md`](NEWTON_DERIVATION_TOP4_BRIDGE_NOTE.md), [`scripts/newton_derivation_top4_bridge_runner.py`](../scripts/newton_derivation_top4_bridge_runner.py) |
| Principle 4 (momentum conservation forces `p = 1` *given* Principle 3) | closed algebraically | this note, Principle 4 section |

### What remains open (the gate)

The gate guarding promotion of this note to retained Newtonian-derivation
status is the **external-field generator-invariant inertial-mass step on a
persistent compact-object family**. Concretely, the missing theorem has the
form:

> Let `O` be a persistent compact pattern admitted by the audit-clean
> `top4` multistage floor. Let `f_ext` be a weak field sourced by a
> *different* persistent compact pattern `O'` on the same retained
> ordered-lattice family. Then the linear response of `O` to `f_ext`,
> measured as the centroid shift per unit source strength, is invariant
> under change of `O`'s internal width within the admissible compact-object
> band `{top3, top4, top5}`.

This is exactly the "persistent-pattern inertial mass equal to source
charge" step that Principle 3 needs as a *physical* (not test-particle)
theorem. Until this step is registered, the chain
"Born + valley + linearity + momentum conservation `→ F ∝ M_1 M_2 / r^(d-2)`"
cannot be promoted from "bounded conditional on the retained ordered-lattice
family" to "retained Newtonian derivation".

### Why the gate is still open after the existing bridge

The 2026-05-07 bridge note operationally satisfies Principle 3 on the
multistage compact-object family, but only under *self-sourcing* — the same
object both sources and responds to the field. The bridge therefore
discharges the "extensivity of the response coefficient in `s`" half of
Principle 3, but not the "generator-invariance of inertial mass across
different persistent patterns" half. The two halves are independent:
self-source extensivity is consistent with the response coefficient depending
on the internal width of the responder, which would violate the
equivalence-principle reading required for two-body Newtonian momentum
conservation in Principle 4.

The negative authority that fixes the residual is
[`MATTER_INERTIAL_CLOSURE_NOTE.md`](MATTER_INERTIAL_CLOSURE_NOTE.md): on
Gaussian persistent packets under a uniform linear field, equivalence-
principle slopes differ by 123% across packet widths. The open question is
whether the audit-clean multistage compact-object family escapes that
no-go (because its persistence band is much tighter than free Gaussian
packets) or whether the same wave-mechanical dispersion mechanism recurs.

### Smallest experiment that would close the gate

A future closure attempt should:

1. Build the external-field probe by sourcing `f_ext` from a separate
   `top4` multistage compact-object placement at a fixed offset.
2. Sweep the responder's internal width over `{top3, top4, top5}` on the
   same admissibility floor.
3. Measure the response slope (centroid shift per unit `s_source`) at
   each width.
4. PASS criterion: response slope is invariant across `{top3, top4, top5}`
   to within the same `ALPHA_BAND = [0.95, 1.05]` and within the same
   `OVERLAP_THRESHOLD = 0.90` already used by the audit-clean floor.

Until such a probe exists and either PASSes the equivalence-principle gate
or fails it cleanly, this note must remain within `open_gate` scope and
must not be cited as a closed Newtonian derivation. A FAIL is informative:
it would extend `matter_inertial_closure_note`'s no-go from free Gaussian
packets to the multistage compact-object family, and would force the
closure path to one of the structural alternatives listed in that note
(soliton-like persistent objects, modified action, or geometry-independent
coupling).

### Audit boundary statement

The audited scope of this note is therefore:

> On the retained ordered-lattice family, the algebra of Principles 1, 2,
> 3a, 3b, 3c (self-sourcing), and 4 selects `p = 1` and the Newtonian
> mass-scaling law as a *bounded conditional theorem*. The open gate is the
> external-field generator-invariant inertial-mass step on a persistent
> compact-object family, specifically the response-slope-invariance test
> across `{top3, top4, top5}` under a field sourced by a separate
> `top4` multistage compact object. The negative authority
> `matter_inertial_closure_note` fixes the residual at the
> equivalence-principle level for free Gaussian packets; this note's open
> step is whether that no-go also recurs on the multistage compact-object
> family.
