# Conventions Unification Companion Note

**Date:** 2026-05-08
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion. Source-note
proposal; pipeline-derived status is set only after independent audit
review.
**Authority role:** companion to
[`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
and
[`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md).
Records that *labeling conventions* (mass-ordering names) and *unit
conventions* (meter, second, kilogram) are the same kind of operation
applied at different layers of the framework's prediction stack.
**Primary runner:** [`scripts/frontier_conventions_unification.py`](../scripts/frontier_conventions_unification.py)
**Cache:** [`logs/runner-cache/frontier_conventions_unification.txt`](../logs/runner-cache/frontier_conventions_unification.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated only
after the independent audit lane reviews the claim, dependency chain, and
runner. This note does not write audit verdicts and does not promote any
downstream theorem.

## What this note clarifies

Two recently-landed companion notes establish:

1. [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md):
   the physical `Cl(3)` on `Z³` reading is repo baseline, not a new
   axiom. Convention bookkeeping is a separate audit row from the
   physics derivation.
2. [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md):
   `C_3[111]` on `hw=1` is preserved framework symmetry, not a "gap to
   be broken." Mass-ordering labels {electron, muon, tau} are
   labeling conventions on top of the structural three-fold spectrum
   prediction, not derivation input.

This note records the audit-honest observation that **labeling
conventions and unit conventions are the same kind of operation** —
both apply naming choices on top of structural predictions, and neither
constitutes a physical import.

## The unification

Two layers of "convention bookkeeping" appear in the framework's
prediction stack:

| Layer | What's predicted (structural) | What's named (convention) |
|---|---|---|
| Mass-ordering | three distinct eigenvalues with Koide structure (under A1) | `{electron, muon, tau}` ← labels by mass ordering |
| Unit conversion | dimensionless ratios e.g. `λ_k / λ_ref`, `l / l_ref` | `meters`, `seconds`, `kilograms` ← human unit choice |
| Particle naming | specific charge / mass / spin states | `u`, `d`, `s`, `c`, `b`, `t` ← labels by quantum numbers |
| Eigenstate naming | specific eigenstates of mass operator | `ν_1`, `ν_2`, `ν_3` ← labels by mass ordering |

In every row:

- The **physics is in the structural prediction** (left column). The
  framework derives or admits these on its retained surface.
- The **names and units are convention** (right column). Choosing what
  to *call* the predicted objects does not consume retained content
  and does not load-bear PDG values into a derivation step.

This unification matches the reviewer's existing review-loop rule for
the physical-lattice baseline: vocabulary corrections back to the
baseline are appropriate review-loop fixes, while extra physical
identifications and readout bridges remain separate audit rows.

## Why this matters for SM-derivation imports

The standard practice in SM-derivation programs is to require **at
least one absolute scale anchor** (a physical pin: lattice spacing in
QCD, GUT scale in GUTs, string scale in string theory, etc.). This is
dimensionally forced: dimensionless math alone cannot fix absolute
sizes. Without a scale anchor, you can predict ratios but not
quantities.

There is one structural escape: if a framework derives a fundamental
scale (Planck length, Planck time, Planck mass) from its own primitive
content, then:

- The fundamental scale is *structural*, not imported.
- Every physical scale becomes a *dimensionless ratio* to the
  fundamental scale (e.g., `m_e / m_P`).
- Conversion to human units (meter, second, kilogram) is *unit
  convention only*, not physical content.

Under that condition, the framework's import surface reduces to:

1. **Structural derivations** (axioms + theorems) — no import beyond
   the foundational mathematical framework choice.
2. **Labeling conventions** (which eigenvalue is "electron", what the
   meter is called, etc.) — pure convention, identical in nature to
   `{u, d, s, ...}` naming or `{ν_1, ν_2, ν_3}` mass-ordering.

Specifically: the absolute scale anchor that other SM-derivation
programs require as a physical pin would, in this framework,
become a dimensionless ratio derivable from algebra plus a
unit-convention choice for what to call it.

## Conditional, not promoted

This note is explicit that the import-elimination story above is
**conditional**. It is not a closure claim. Specifically:

- **Planck-from-structure** is itself a research target. It is not
  retained on main as a closed derivation. Whether the framework's
  primitive layer (`Cl(3)/Z³` + 3+1 single-clock + Lieb-Robinson +
  retained gravitational-phase content) forces a unique fundamental
  length is open; the audit-lane status of relevant notes (e.g.,
  `PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30`)
  is currently `audited_renaming` rather than retained.
- **Dimensionless ratio derivations** for charged-lepton masses (the
  Option C parameter targets A1, P1, δ, v_0) are open research
  targets, not retained closures. Their reclassification under
  preserved-`C_3` (per the C_3 preserved interpretation note) tracks
  them as parameter-pinning frontiers.

**On the EW–Planck hierarchy**: the framework retains the structural
derivation `v_EW = M_Pl × (7/8)^(1/4) × α_LM^16 = 246.28 GeV` per
`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`. Under that retained
derivation, `v_EW / M_Pl` is *not* a separate import; it is a
structural consequence of the taste-determinant exponent and α_LM. This
note does not opine on which dimensionless ratios across physics
generally are "hard"; it tracks only what the audit ledger marks as
retained, bounded, or open on the framework's own surface.

## Application to ongoing review

The review lane has landed, in close sequence:

- The `PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE` (physical
  lattice as baseline, vocabulary correction).
- The `C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE` (preserved-`C_3`,
  three-state carrier vs species/readout).
- The `KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE`
  (Route F structurally barred for the A1 amplitude-ratio target).

This companion note slots in alongside the first two as a unification
between the two convention layers (labeling and unit). It does not
modify any retained theorem. It does not promote any downstream lane.
It records a vocabulary clarification: when the audit lane evaluates
the bridge gap, scale anchors and labeling conventions should be tracked
in the same way — as conventions on top of structural predictions, not
as physical admissions.

## What this does NOT do

This note explicitly does **not**:

1. Claim the framework derives Planck length from retained content. The
   relevant gravity / geometry / discreteness work is in flight; this
   note is conditional on it.
2. Claim the framework derives any dimensionless ratio for charged-
   lepton, quark, Higgs, or gauge-coupling values. The Option C
   parameter targets remain bounded research frontiers.
3. Promote any specific lane to retained status. Lane-specific
   classification, audit verdict, and pipeline-derived status remain
   audit-lane authority.
4. Add a new mathematical axiom. A1+A2 still suffice. The
   `MINIMAL_AXIOMS_2026-05-03.md` note is unchanged.
5. Replace the substep-4 AC narrowing rule. PDG values are still not
   load-bearing as derivation input.
6. Claim the bridge-gap admission count drops to a specific number.
   Audit-lane authority on per-row classifications is preserved.

## What this DOES do

It records, as repo-language clarification:

1. Mass-ordering labels (e, μ, τ) and unit conventions (m, s, kg) are
   the **same kind** of bookkeeping operation: naming on top of
   structural prediction.
2. The minimum import surface for any SM-derivation program is
   ordinarily one absolute scale anchor — but this can in principle be
   eliminated if a fundamental scale (Planck) is structurally derived.
3. Under the conditional preserved-`C_3` + Planck-from-structure
   framing, the four Option C parameter targets (A1, P1, δ, v_0) are
   tracked as **dimensionless-ratio research targets**, not as
   scale-anchor admissions.
4. Whether this conditional path closes or not, the unification of
   labeling and unit conventions stands as a vocabulary clarification:
   conventions of either kind don't count as physical imports.

## Cross-references

- Foundational baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Preserved-`C_3` companion: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Option C parameter targets: [`A3_OPTION_C_BRANNEN_RIVERO_PHYSICAL_LATTICE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_optC.md`](A3_OPTION_C_BRANNEN_RIVERO_PHYSICAL_LATTICE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_optC.md)
- Route F obstruction: [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- Physical-lattice narrowed no-go: [`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](PHYSICAL_LATTICE_NECESSITY_NOTE.md)

## Validation

Run:

```bash
python3 scripts/frontier_conventions_unification.py
```

The runner is a review-hygiene check, not a physics proof. It verifies:

1. The note is classified as `meta` and does not declare pipeline status.
2. The unification of labeling and unit conventions is stated explicitly
   and cited to standard physics analogues (`{u, c, t}`, `{ν_1, ν_2, ν_3}`,
   `K_S/K_L`).
3. The Planck-from-structure escape from scale-anchor imports is stated
   *conditionally*, not as a closure claim.
4. The note does not load PDG values as derivation input.
5. The note does not promote any specific Option C parameter target to
   retained status.
6. The note does not claim the bridge-gap admission count drops to any
   specific number.
7. Cross-references to the recently-landed companion notes are present.
8. The note does not add a new mathematical axiom.

## Review-loop rule

When reviewing future branches that mix scale anchors and labeling
choices:

1. Track labeling conventions (mass-ordering names, particle
   tags) and unit conventions (meter, second, kilogram) the same way:
   as conventions on top of structural predictions, not as physical
   imports.
2. Treat absolute scale anchors as **conditional imports**: required
   in standard SM-derivation programs, but in principle eliminable if
   a fundamental scale is structurally derived.
3. Do not promote any conditional dimensionless-ratio-derivation path
   to retained status without independent audit-grade derivation work.
4. Do not let convention bookkeeping silently promote downstream
   science on claim-classification or pipeline-derived status rows.
