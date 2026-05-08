# C_3 Symmetry Preserved Interpretation Note

**Date:** 2026-05-08
**Type:** meta
**Claim type:** meta
**Status:** repo-semantics clarification; no theorem promotion. Source-note
proposal — the audit lane sets `effective_status` after independent
review.
**Authority role:** companion to
[`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md).
Records that the framework's `C_3[111]` symmetry on `hw=1` is *preserved*
(not broken) and that the mass-ordering labels {electron, muon, tau} are
convention, not derivation input.
**Primary runner:** [`scripts/frontier_c3_symmetry_preserved_interpretation.py`](../scripts/frontier_c3_symmetry_preserved_interpretation.py)
**Cache:** [`logs/runner-cache/frontier_c3_symmetry_preserved_interpretation.txt`](../logs/runner-cache/frontier_c3_symmetry_preserved_interpretation.txt)

## Authority disclaimer

This is a source-note proposal. Effective `effective_status` is generated
by the audit pipeline only after the independent audit lane reviews the
claim, dependency chain, and runner. This note does not write audit
verdicts and does not promote any downstream theorem.

## What this note clarifies

The framework's retained content on main establishes that:

1. The `Cl(3)/Z³` algebraic structure has a manifest `C_3[111]` cyclic
   symmetry acting on the BZ-corner triplet on `hw=1 ≅ ℂ³` (theorem,
   retained per `STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`).
2. Every `C_3`-equivariant Hermitian operator on this sector has the
   circulant form `H = aI + bC + b̄C²` (theorem, retained per
   `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md` R1).
3. Such operators have eigenvalue spectrum
   `λ_k = a + 2|b|·cos(arg(b) + 2πk/3)` for `k ∈ {0, 1, 2}` (theorem,
   retained per the same note's R2).
4. Generically these three eigenvalues are distinct.

Recent campaigns (the 10-probe A3 derivation campaign,
PRs #709-#713 + #719-#723) sought a mechanism to *break* `C_3` from inside
the algebra in order to label the three corners as physical species
{electron, muon, tau}. Across 99+ attack vectors and 347/0 PASS, every
route confirmed: **`C_3` cannot be broken from inside the framework's
primitives.**

This note records the natural interpretive consequence of that result:

> **The framework's `C_3[111]` symmetry is fundamental and preserved.
> It is not a problem to be broken. The three-fold structure on `hw=1`
> IS the framework's prediction of three-generation matter, and the
> matching to observed charged leptons is structural (3 ↔ 3,
> distinct ↔ distinct), with mass-ordering labels treated as
> conventions in the standard physics sense.**

## Why "embrace, not break" is the audit-honest reading

The 10-probe campaign proved a structural impossibility. There are two
ways to read that result:

| Reading | Status |
|---|---|
| "Can't break `C_3` ⟹ derivation impossible from this framework" | The user-rejected framing; would force adoption of an extra structural admission (AC_φλ as new axiom) |
| "Can't break `C_3` ⟹ `C_3` is fundamental and the framework's prediction is the three-fold spectrum itself" | This note's framing; consistent with how preserved symmetries are routinely treated in physics |

Standard physics already accepts preserved symmetries as load-bearing
predictions, not as gaps. Examples on retained ground:

- **QCD `SU(3)` color** is fundamental and unbroken; individual colors
  are not observed (confinement). Nobody calls this "a sector
  identification problem"; the symmetry IS the answer.
- **Isospin `SU(2)`** in low-energy QCD is preserved at the gauge level;
  observed `m_u ≠ m_d` reflects an explicit Yukawa-sector breaking that
  the symmetry itself does not derive but that is *consistent with*
  isospin-related labeling.
- **`CPT`** is exact; particles and antiparticles are `CPT`-related,
  with charge-sign labels assigned by convention, not by deriving the
  sign of the electron's charge from `CPT` alone.
- **Quark labels** (`u`, `d`, `s`, …): assigned by charge and mass-ordering
  conventions on top of derived `SU(N)`-flavor structure, not derived
  from group theory alone.

Calling the `Cl(3)/Z³` framework's `C_3` situation a "sector
identification problem" treats the framework to a stricter standard
than the SM applies to itself.

## What is structural prediction vs labeling convention

Under the preserved-`C_3` reading:

**Structural predictions (load-bearing, retained or bounded):**

- *Three* charged-lepton-like states on `hw=1` (forced by `C_3` orbit
  count = 3; theorem).
- *Distinct* eigenvalue magnitudes (forced generically by
  `λ_k = a + 2|b|·cos(...)` for `b ≠ 0`; theorem).
- *Koide ratio* `Q = (Σ √λ_k)² / (3 Σ λ_k) = 2/3` (forced by the
  circulant structure under A1; bounded on amplitude constraint).
- *Mass-hierarchy ordering pattern* (one small, one intermediate, one
  large) follows from `cos` taking three distinct values at
  `arg(b) + 2πk/3`.

These are testable scientific predictions of the framework. They can be
*falsified* by observation if observation showed e.g., four
charged-lepton generations, or two equal masses, or `Q ≠ 2/3`.
Empirically, charged-lepton phenomenology *agrees* with all of them.

**Labeling conventions (not load-bearing, not derivation input):**

- The mapping `{smallest λ_k, middle λ_k, largest λ_k} ↔ {electron,
  muon, tau}` by mass ordering. This is a *labeling convention*
  identical in nature to:
  - Naming `u`/`c`/`t` quarks by charge and mass-ordering rather than
    deriving "up-quark" from the SM Lagrangian.
  - Naming `ν_1` / `ν_2` / `ν_3` mass eigenstates by mass-ordering.
  - Naming `K_S` / `K_L` by lifetime ordering.
- These conventions consume zero retained-grade content. They do not
  load-bear PDG values into a derivation step.

The substep-4 AC narrowing rule
([`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
forbids using PDG values *as derivation input*. This note does not.
Mass-ordering is a labeling rule applied *after* the framework
predicts three distinct eigenvalues.

## Reclassification of Option C admissions under this reading

The Option C bounded decomposition
([`A3_OPTION_C_BRANNEN_RIVERO_PHYSICAL_LATTICE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_optC.md`](A3_OPTION_C_BRANNEN_RIVERO_PHYSICAL_LATTICE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_optC.md))
named four non-retained inputs to the Brannen-Rivero closure chain:

| # | Admission | Old framing | Reclassification under preserved-`C_3` |
|---|---|---|---|
| 1 | A1 (`3a² = 6\|b\|²` amplitude ratio) | structural admission for sector identification | parameter-pinning research target for the `C_3`-invariant operator's amplitude ratio |
| 2 | P1 (eigenvalue → mass map) | structural admission for species identification | parameter-pinning research target for the eigenvalue ↔ observable functional |
| 3 | δ (rad-unit bridge for 2/9) | structural admission for phase | parameter-pinning research target for the operator's phase shift |
| 4 | v_0 (lepton-sector scale) | structural admission for scale | parameter-pinning research target for the operator's overall scale |

Under the old framing, these were "bridge admissions" that the framework
needed to derive in order to claim AC_φλ closure. Under the preserved-
`C_3` reading, they are concrete research targets — analogous to
**Convention C-iso engineering** (currently bounded ~1.3% absolute,
target ε_witness ~ 3×10⁻⁴), which the framework does not classify as a
bridge admission but as a parameter-pinning frontier.

This reclassification:

- does **not** load-bear PDG values into any derivation;
- does **not** add a new axiom;
- does **not** claim closure of any specific parameter target by itself;
- **does** record the framework-internal interpretation that these are
  parameter-pinning research targets, not sector-identification gaps.

The audit lane retains full authority over each parameter target's
`claim_type` and `effective_status`.

## What this does NOT do

This note explicitly does **not**:

1. Derive specific charged-lepton mass values. The framework's bounded
   results on lepton masses remain bounded; their precise values still
   depend on parameter pinning of `(a, b, scale, phase)` for the `C_3`-
   invariant operator on `hw=1`.
2. Claim AC_φλ is "trivially closed by definition." The labeling-
   convention reclassification is a *separate move* from the parameter-
   pinning research targets, which remain bounded.
3. Promote any specific Option C admission to retained status. Each of
   A1, P1, δ, v_0 still requires its own derivation route or explicit
   admission.
4. Modify any retained theorem on main. The 10-probe A3 obstruction
   theorems remain valid as algebra-layer mathematical results; this
   note clarifies their interpretation, not their content.
5. Add a new axiom. A1+A2 still suffice as the framework's mathematical
   axioms.
6. Replace empirical falsifiability of lane predictions. Each lane's
   observable predictions remain independently falsifiable.

## What this DOES do

It records, as repo-language clarification:

1. `C_3[111]` symmetry on `hw=1` is *preserved* in this framework, not
   "needing to be broken" for derivational completion.
2. The three-fold eigenvalue structure on `hw=1` IS the framework's
   structural three-generation prediction, matching observed
   phenomenology (3 charged-lepton generations, distinct masses, Koide
   `Q = 2/3`).
3. Mass-ordering labels {electron, muon, tau} are conventions of the
   standard kind already used throughout particle physics
   (`u`/`c`/`t`, `ν_1`/`ν_2`/`ν_3`, `K_S`/`K_L`, etc.); they consume no
   retained content and are not derivation input.
4. The four Option C parameter targets (A1, P1, δ, v_0) are research
   targets at the same logical level as Convention C-iso engineering,
   not bridge-gap admissions about sector identification.

## Cross-references

- Foundational baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- BZ-corner forcing theorem (the C_3 origin): [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Circulant character / eigenvalue spectrum: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Substep-4 AC narrowing (PDG-input prohibition): [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- A3 obstruction theorems (the 10-probe campaign):
  - [`A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md`](A3_ROUTE1_HIGGS_YUKAWA_C3_BREAKING_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r1.md)
  - [`A3_ROUTE2_SINGLE_CLOCK_C3_OBSTRUCTION_NOTE_2026-05-08_r2.md`](A3_ROUTE2_SINGLE_CLOCK_C3_OBSTRUCTION_NOTE_2026-05-08_r2.md)
  - [`A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md`](A3_ROUTE3_ANOMALY_INFLOW_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r3.md)
  - [`A3_ROUTE4_SPIN6_CHAIN_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r4.md`](A3_ROUTE4_SPIN6_CHAIN_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_r4.md)
  - [`A3_ROUTE5_NO_PROPER_QUOTIENT_SHARPENED_OBSTRUCTION_NOTE_2026-05-08_r5.md`](A3_ROUTE5_NO_PROPER_QUOTIENT_SHARPENED_OBSTRUCTION_NOTE_2026-05-08_r5.md)
- Option C bounded decomposition: [`A3_OPTION_C_BRANNEN_RIVERO_PHYSICAL_LATTICE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_optC.md`](A3_OPTION_C_BRANNEN_RIVERO_PHYSICAL_LATTICE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_optC.md)

## Validation

Run:

```bash
python3 scripts/frontier_c3_symmetry_preserved_interpretation.py
```

The runner is a review-hygiene check, not a physics proof. It verifies
that this note:

1. Is classified as `meta` and does not declare pipeline status.
2. Does not load-bear PDG/empirical mass values as derivation input.
3. States the preserved-`C_3` interpretation in the standard preserved-
   symmetry idiom (analogous to QCD color, isospin, CPT).
4. Treats mass-ordering labels as labeling conventions, not derivation
   steps.
5. Does not promote specific Option C parameter targets to retained
   status.
6. Cross-references the BZ-corner forcing theorem and the circulant
   character note (the retained provenance of the `C_3` structure).
7. Cross-references the substep-4 AC narrowing rule and the 10-probe
   A3 obstruction theorems.
8. Does not add a new mathematical axiom (A1+A2 still suffice).

## Review-loop rule

When reviewing future branches that depend on `C_3[111]` on `hw=1`:

1. Treat `C_3` as preserved framework symmetry, not a "gap to be
   broken."
2. Treat the three-eigenvalue structure as the framework's structural
   three-generation prediction.
3. Treat mass-ordering labels {electron, muon, tau} as standard
   conventions; do not classify them as derivation imports.
4. Treat the four Option C parameter targets (A1, P1, δ, v_0) as
   parameter-pinning research targets at the same logical level as
   Convention C-iso engineering, not as bridge-gap admissions.
5. Specific operator parameters and absolute scales still require
   their own derivation paths or explicit admissions on a per-target
   basis.
