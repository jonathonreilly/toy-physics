# Koide A1 Eleven-Probe Campaign Synthesis Meta Note

**Date:** 2026-05-08
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion.
Source-note proposal; pipeline-derived status is set only after
independent audit review.
**Authority role:** records the eleven-probe state of the
A1-condition closure campaign and the precisely-localized missing
primitive that all eleven probes converge to. Companion to
[`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
and
[`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md).
**Primary runner:** [`scripts/frontier_a1_11_probe_campaign_synthesis.py`](../scripts/frontier_a1_11_probe_campaign_synthesis.py)
**Cache:** [`logs/runner-cache/frontier_a1_11_probe_campaign_synthesis.txt`](../logs/runner-cache/frontier_a1_11_probe_campaign_synthesis.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. This note does not write audit verdicts and does
not promote any downstream theorem. It records what the eleven-probe
campaign converged to; it does not, by itself, admit, derive, or close
the A1-condition.

**Same-batch follow-up (2026-05-09):** Probes 12 and 13 landed in the
same review-loop batch as this synthesis. They corroborate the same
missing-primitive locus and leave the A1 admission count unchanged.
This note remains the eleven-probe synthesis/index; the later probes
are linked below as targeted follow-up, not as theorem promotion.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- **"A1-condition"** = the Brannen-Rivero amplitude-ratio constraint
  `|b|²/a² = 1/2` for the `C_3`-equivariant Hermitian circulant
  `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`.

These are distinct objects despite the shared label. The eleven-probe
campaign concerns the A1-condition only; framework axiom A1 is
retained and untouched.

## Scope

The A1-condition is a load-bearing non-axiom step on the Brannen
circulant lane for the charged-lepton Koide cone (see
[`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)).
A self-organized eleven-probe campaign attacked it from independent
mathematical/physical angles between 2026-05-07 and 2026-05-09 to
determine whether the A1-condition can be derived from retained-grade
content alone, or whether a missing primitive is structurally required.

This note records the campaign's converged state and the precise
mathematical name of the missing primitive that every probe converges
to. It does **not** admit that primitive, derive the A1-condition,
modify any retained theorem, or add any axiom.

## The eleven-probe campaign

All eleven probes returned **STRUCTURAL OBSTRUCTION** (no positive
closure of the A1-condition from retained content). Each landed as a
bounded-theorem source-note + paired runner, with the obstruction
verified by independent algebraic counterexamples.

### Round 1 — within retained content

| # | Probe | Closure path | Outcome | PR | Source note |
|---|---|---|---|---|---|
| 1 | Route F | Yukawa Casimir-difference `T(T+1) − Y² = 1/2` | barred — `Y²` convention dependence (PDG vs SU(5)) | #727 | [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md) |
| 2 | Route E | Kostant Weyl-vector `\|ρ_{A_1}\|² = 1/2` | barred — Cartan-Killing `\|α\|²` normalization convention dependence | #730 | [`KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md`](KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md) |
| 3 | Route A | Koide-Nishiura U(3) quartic variational | barred — Wilson-coefficient circularity + squaring trap | #731 | [`KOIDE_A1_ROUTE_A_KOIDE_NISHIURA_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routea.md`](KOIDE_A1_ROUTE_A_KOIDE_NISHIURA_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routea.md) |
| 4 | Route D | Newton-Girard polynomial structure | barred — weight-class `(1,1)` vs `(1,2)` ambiguity | #732 | [`KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md`](KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md) |

### Round 2 — natural extensions

| # | Probe | Closure path | Outcome | PR | Source note |
|---|---|---|---|---|---|
| 5 | Probe 1 | RP/GNS canonical Frobenius pairing | barred — vacuum-state freedom + log-functional choice + reduction-map ambiguity | #735 | [`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md) |
| 6 | Probe 2 | Anomaly extension to flavor sector | barred — R3 functoriality failure + category mismatch (charges-to-coefficients) | #733 | [`KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md`](KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md) |
| 7 | Probe 3 | Gravity-phase canonical scale | barred — sector orthogonality + character mismatch + Born-map collapse | #736 | [`KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md`](KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md) |
| 8 | Probe 4 | Spectral-action principle (Connes) | barred — requires four named primitives; cutoff convention dependence | #734 | [`KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md`](KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md) |

### Round 3 — deep methodological

| # | Probe | Closure path | Outcome | PR | Source note |
|---|---|---|---|---|---|
| 9 | Probe 5 | RG-flow fixed-point candidate | barred — framework's standard SM RGE drives **away** from `1/2` | #738 | [`KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md`](KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md) |
| 10 | Probe 6 | Wrong-operator-class expansion (`Y†Y`) | barred — `Y†Y` collapses 6-DOF complex circulant back to 3-DOF Hermitian; the Brannen ansatz IS the right space | #737 | [`KOIDE_A1_PROBE_OPERATOR_CLASS_BOUNDED_NOTE_2026-05-08_probe6.md`](KOIDE_A1_PROBE_OPERATOR_CLASS_BOUNDED_NOTE_2026-05-08_probe6.md) |

### Round 4 — Survey-2-motivated

| # | Probe | Closure path | Outcome | PR | Source note |
|---|---|---|---|---|---|
| 11 | Probe 7 | `Z_2 × C_3 = Z_6` retained pairing | barred — no retained `Z_2` pairs with `C_3` to force `1/2`; **identifies the structural locus**: `1/2` is the `C_3`-multiplicity ratio `3 : 6 = dim(trivial-isotype) : dim(non-trivial-isotype)` on `M_3(ℂ)_Herm` | #740 | [`KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md`](KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md) |

**Aggregate result:** eleven independent attack vectors, all returning
bounded structural obstruction. The campaign has converged.

## The precisely-localized missing primitive

The §8 finding of Probe 7 (PR #740), corroborated
independently by Route D (PR #732, weight-class ambiguity) and Probe 1
(PR #735, Frobenius-pairing reduction-map ambiguity), names the
missing primitive precisely:

> **The canonical `(1,1)`-multiplicity-weighted Frobenius pairing on
> `M_3(ℂ)_Herm` under `C_3`-isotype decomposition.**

This phrase is mathematically precise and identifies a single
distinguished structure. The remainder of this note unpacks why this
specific phrase is the right characterization of what the eleven
probes converge to.

### Structural locus: the `3 : 6` multiplicity ratio on `M_3(ℂ)_Herm`

The 9-real-dimensional Hermitian algebra `M_3(ℂ)_Herm` decomposes
under the retained `C_3[111]` action on `hw=1` into three isotypic
components:

```
M_3(ℂ)_Herm  =  (3-dim trivial-character isotype)
              ⊕ (3-dim ω-character isotype)
              ⊕ (3-dim ω̄-character isotype)
```

The `C_3`-equivariant Hermitian circulant `H = aI + bC + b̄C²` lives
exactly in the trivial-character isotype's 3-dimensional fiber over
the `aI` axis (1-dim) plus the non-trivial-character isotype's
combined 6-dimensional fiber spanned by `(b, b̄)`-coefficients of
`(C, C²)`. Schematically:

```
trivial-isotype dimension    = 3
non-trivial-isotype dimension = 6 = 3 (ω) + 3 (ω̄)
ratio                          = 3 : 6 = 1 : 2
```

The A1-condition `|b|²/a² = 1/2` is **algebraically equivalent** to
the equality

```
3 · a²  =  6 · |b|²
```

i.e., the equality of the **multiplicity-weighted Frobenius norms** of
the two isotypic projections. The `1/2` IS the multiplicity ratio
`3 : 6` on the Hermitian algebra. This is independently observed by
Probe 7 §8 (Survey-2 reframing), Route D's weight-class analysis (the
`(1,1)` weighting choice IS the multiplicity weighting), and Probe 1's
Frobenius-reduction observation (the canonical pairing structure is
the missing piece).

### Why the existing retained content does not supply this primitive

The eleven probes establish, jointly, the following:

1. **Pure `C_3` representation theory does not single out `1/2`.**
   The `C_3` characters give arithmetic outputs `1/3, 2/3, 1/9,
   2/9, …` (powers of `1/3`); they do not single out `1/2`. (Survey 2
   observation, formalized in Probe 7.)

2. **No retained `Z_2` pairs with `C_3` on `hw=1` to give a
   `Z_6 = Z_2 × C_3` forcing.** Five candidate `Z_2`'s enumerated and
   each barred (Probe 7).

3. **Linear equivariance principles cannot single out a quadratic
   constraint.** The A1-condition `|b|² = a²/2` is a quadratic
   surface; linear involutions give linear cones, hence either no
   ratio or a continuum. (Probe 7 universal barrier; Route D
   weight-class observation.)

4. **The Frobenius-pairing structure is not canonical without a
   weighting principle.** Probe 1 found multiple admissible Frobenius
   pairings (vacuum-state freedom, log-functional choice,
   reduction-map ambiguity); the multiplicity-weighted one is
   distinguished by `C_3`-isotype geometry but is not retained.

5. **The right algebraic locus IS `M_3(ℂ)_Herm` under `C_3`-isotype
   decomposition.** Probe 6 (operator-class expansion) ruled out
   alternative operator spaces: `Y†Y` collapses back to `M_3(ℂ)_Herm`,
   so the campaign has the right space. The missing piece is the
   weighting principle ON that space.

6. **No external natural-units, RG-flow, gravity-phase, or
   spectral-action route imports the multiplicity weighting from
   retained content.** Routes E, F, A, and Probes 2, 3, 4, 5 each
   confirm one of these external imports fails.

The convergent finding: **the campaign has correctly localized the
missing input. It is not a missing route or a missing alternative
operator class; it is a specific named pairing structure on a known
space.**

## Why this characterization is the right one

The phrase "canonical `(1,1)`-multiplicity-weighted Frobenius pairing
on `M_3(ℂ)_Herm` under `C_3`-isotype decomposition" is the right
characterization for three independent reasons:

1. **Precise mathematical content.** It names a single distinguished
   inner product on a known finite-dimensional algebra:
   `⟨X, Y⟩_w = Σ_χ w_χ · Tr(P_χ X · P_χ Y)` with weights
   `w_χ = (mult of χ in M_3(ℂ)_Herm)`. The `(1,1)` label denotes
   weighting both factors by their isotypic multiplicity.

2. **Convergence target of three independent probes.** Probe 7 §8
   (`3 : 6` multiplicity ratio), Route D (weight-class `(1,1)` vs
   `(1,2)` ambiguity), and Probe 1 (Frobenius-pairing reduction-map
   ambiguity) each independently land on this pairing as the missing
   structure.

3. **Generic primitive type matches the gap.** The eleven probes ruled
   out gauge-Casimir, RG-fixed-point, anomaly-flavor, gravity-phase,
   spectral-action, RP/GNS, Newton-Girard, Koide-Nishiura, Kostant,
   `Z_2`-pairing, and operator-class expansions. The remaining gap is
   exactly a *normalization principle* on the isotypic decomposition,
   which is precisely the role a multiplicity-weighted pairing plays.

## Audit-honest options

This synthesis records the missing primitive precisely. Three options
remain audit-honestly open. **None is selected by this note.** The
audit lane and the user retain authority over which (if any) to take.

### Option (a): explicit user-approved admission of the primitive

**Form:** if, and only if, the user explicitly approves it, add to the
framework's named admissions a single line:
"the canonical `(1,1)`-multiplicity-weighted Frobenius pairing on
`M_3(ℂ)_Herm` under `C_3`-isotype decomposition." Under such a
user-approved admission, the A1-condition becomes a one-step algebraic
consequence (the multiplicity weighting `3 : 6` directly gives
`3a² = 6|b|²`).

**Cost:** adds a new named admission. By framework policy, this
requires explicit user authority. It is **not** load-bearing on the
retained `Cl(3)/Z³` axioms (A1+A2 still suffice for the existing
retained theorem stack); it would be a sector-specific normalization
admission for the charged-lepton Koide lane only.

**Status under this note:** **NOT TAKEN.** No admission is added by
this note.

### Option (b): further probes seeking to derive the primitive

**Direction examples** (none endorsed by this note):

- A retained random-matrix-measure (GOE/GUE) argument that derives
  the multiplicity-weighted Frobenius pairing from a max-entropy
  principle on isotypic decomposition.
- A 2nd-order phase-transition equipartition principle internal to
  the Cl(3)/Z³ stack (analogue of the classical equipartition
  theorem).
- A Schur-orthogonality + `Cl(3)` trace-form argument that lifts the
  multiplicity weighting to canonical status.

Each candidate remains a research target; none is currently retained
content.

**Status under this note:** **OPEN as research direction** for a
future probe round, if the user authorizes it. The campaign's
converged state means further probes should target this specific
primitive, not generic closure routes already covered by the bounded
patterns.

### Option (c): pivot to other bridge work

The A1-condition is one named target among multiple bridge-gap
admissions tracked by the repo's bridge-gap status notes (L3a
trace-surface, L3b overall scalar, C-iso `a_τ = a_s`, W1.exact
engineering frontier). The audit lane and the user may classify the
A1-condition as a parameter/readout target (per
[`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md))
and prioritize independent bridge work over A1-closure attempts.

**Status under this note:** **NEUTRAL.** The campaign's converged state
provides a sharp, well-localized bounded admission for any future
prioritization decision; the prioritization itself is out of scope.

## What this DOES NOT do

This note explicitly does **NOT**:

1. **Explicitly approve the primitive as a new named admission.** No
   mathematical axiom or admission is added here. A1+A2 still suffice
   on the retained stack.
2. **Derive the A1-condition.** The A1-condition remains an open
   bounded admission on the Brannen circulant lane.
3. **Modify any retained theorem.** The eleven bounded-obstruction
   theorems stand as algebra-layer mathematical results; this note
   synthesizes their joint converged state, not their individual
   content.
4. **Promote any specific Option (a/b/c).** Authority for the
   admission/derivation/pivot decision is reserved to the audit lane
   and the user.
5. **Load-bear PDG values into a derivation step.** The substep-4 AC
   narrowing rule
   ([`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
   continues to forbid PDG-input use; this note is upstream of any
   readout step.
6. **Claim closure of any sister bridge gap** (L3a, L3b, C-iso,
   W1.exact). This is an A1-condition synthesis only.
7. **Promote Survey 2 to retained authority.** Survey 2 is external
   scoping context that motivated the Round 4 framing; it is not
   load-bearing here.

## What this DOES do

This note records, as repo-language clarification:

1. **The eleven-probe campaign has converged.** All eleven independent
   closure-attempt probes returned bounded structural obstruction.
   Further closure attempts should target the precisely-named missing
   primitive, not new alternative routes.
2. **The missing primitive is named precisely.** "The canonical
   `(1,1)`-multiplicity-weighted Frobenius pairing on `M_3(ℂ)_Herm`
   under `C_3`-isotype decomposition." Three independent probes
   (Probe 7 §8, Route D, Probe 1) corroborate this characterization.
3. **The structural locus is the `3 : 6` multiplicity ratio on
   `M_3(ℂ)_Herm`.** This is a derivable arithmetic identity; what is
   missing is the canonical weighting principle that elevates it to
   the A1-condition.
4. **Three audit-honest options exist** (admit, derive, pivot). None
   is selected.
5. **No new axiom is added.** No retained theorem is modified. No
   downstream theorem is promoted. The audit lane retains full
   authority over each decision.

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Physical-lattice baseline interpretation: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Preserved-`C_3` interpretation: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained provenance of the C_3 / circulant structure

- BZ-corner forcing theorem: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Circulant character / eigenvalue spectrum: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Eleven-probe campaign source notes

Round 1 — within retained content (PRs #727, #730, #731, #732):

- Route F: [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- Route E: [`KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md`](KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md)
- Route A: [`KOIDE_A1_ROUTE_A_KOIDE_NISHIURA_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routea.md`](KOIDE_A1_ROUTE_A_KOIDE_NISHIURA_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routea.md)
- Route D: [`KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md`](KOIDE_A1_ROUTE_D_NEWTON_GIRARD_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routed.md)

Round 2 — natural extensions (PRs #735, #733, #736, #734):

- Probe 1 (RP/GNS): [`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md)
- Probe 2 (anomaly-flavor): [`KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md`](KOIDE_A1_PROBE_FLAVOR_ANOMALY_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe2.md)
- Probe 3 (gravity-phase): [`KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md`](KOIDE_A1_PROBE_GRAVITY_PHASE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe3.md)
- Probe 4 (spectral-action): [`KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md`](KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md)

Round 3 — deep methodological (PRs #738, #737):

- Probe 5 (RG fixed-point): [`KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md`](KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md)
- Probe 6 (operator class): [`KOIDE_A1_PROBE_OPERATOR_CLASS_BOUNDED_NOTE_2026-05-08_probe6.md`](KOIDE_A1_PROBE_OPERATOR_CLASS_BOUNDED_NOTE_2026-05-08_probe6.md)

Round 4 — Survey-2-motivated (PR #740):

- Probe 7 (`Z_2 × C_3 = Z_6`): [`KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md`](KOIDE_A1_PROBE_Z2_C3_PAIRING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe7.md)

Same-batch targeted follow-up (PRs #755, #763):

- Probe 12 (Plancherel/Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- Probe 13 (real structure / antilinear involution): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)

## Validation

Run:

```bash
python3 scripts/frontier_a1_11_probe_campaign_synthesis.py
```

The runner is a review-hygiene check, not a physics proof. It verifies
that this note:

1. Is classified as `meta` and does not declare pipeline status.
2. Cross-references all retained foundational notes (`MINIMAL_AXIOMS`,
   `PHYSICAL_LATTICE_FOUNDATIONAL`, `C3_SYMMETRY_PRESERVED`,
   `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW`).
3. Cross-references each of the ten on-main probe notes by filename
   and the open Probe 7 note by filename.
4. Cites all eleven PR numbers (#727, #730, #731, #732, #733, #734,
   #735, #736, #737, #738, #740).
5. States the missing primitive consistently with the precise phrase
   "canonical `(1,1)`-multiplicity-weighted Frobenius pairing on
   `M_3(ℂ)_Herm` under `C_3`-isotype decomposition."
6. States the `3 : 6` multiplicity ratio structural locus.
7. Does not claim A1-condition closure.
8. Does not add a new mathematical axiom.
9. Does not promote any downstream theorem or write an audit verdict.
10. Does not load-bear PDG numerical mass values as derivation input.

## Review-loop rule

When reviewing future branches that touch the A1-condition:

1. Treat the eleven-probe campaign as converged for generic-route
   search: do not propose a new
   closure route from a generic angle (gauge-Casimir, RG-fixed-point,
   anomaly-flavor, gravity-phase, spectral-action, RP/GNS,
   Newton-Girard, Koide-Nishiura, Kostant, `Z_2`-pairing, operator-
   class expansion) without first explaining why it is *not* an
   instance of one of the eleven already-bounded patterns.
2. Treat the canonical `(1,1)`-multiplicity-weighted Frobenius pairing
   on `M_3(ℂ)_Herm` under `C_3`-isotype decomposition as the named
   primitive at issue.
3. Treat any proposal to admit that primitive as a new named admission as
   requiring explicit user authority; do not let review-loop add it
   silently.
4. Treat any proposal to derive that primitive as a research target,
   not a completed derivation, until it has its own retained-grade
   theorem note + paired runner + audit closure.
5. The retained `Cl(3)/Z³` axioms (A1+A2) and the retained
   bounded-obstruction theorems for the eleven probes remain
   unchanged.
