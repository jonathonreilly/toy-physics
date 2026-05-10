# A3 Option C - Brannen-Rivero / Physical-Lattice Baseline Bounded Decomposition

**Date:** 2026-05-08
**Type:** bounded_theorem (bounded decomposition / obstruction)
**Claim type:** bounded_theorem
**Status:** source-note proposal; audit verdict and downstream status are
set only by the independent audit lane.
**Authority role:** source note for the Option C closure attempt. It
restores physical `Cl(3)` on `Z^3` as baseline semantics and then names
the remaining non-retained inputs.
**Primary runner:** [`scripts/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.py`](../scripts/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.py)
**Cache:** [`logs/runner-cache/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.txt`](../logs/runner-cache/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.txt)

## Authority disclaimer

This is a source-note proposal. Effective `effective_status` is generated
by the audit pipeline only after the independent audit lane reviews the
claim, dependency chain, and runner. The baseline physical-lattice reading
is not a new axiom or admitted input. Any extra selector, species
identification, empirical match, or readout bridge remains separately
auditable.

## Question

Option C asks whether the Brannen-Rivero / Fourier-basis route can close
the A3/AC residual once the repo's baseline physical `Cl(3)` on `Z^3`
semantics are restored.

The candidate chain is:

```text
physical Cl(3) on Z^3 baseline
  -> C_3-equivariant circulant structure on hw=1
  -> Brannen-Rivero eigenvalue spectrum
  -> charged-lepton numerical match
  -> physical species identification
```

Does this close the AC residual from retained content alone?

## Answer

No. Restoring the physical-lattice baseline removes one spurious
"admission" from the analysis, but it does not close the full chain.
The Option C route remains bounded by four separate non-retained inputs:

| # | Input | Role | Review status |
|---|---|---|---|
| 1 | `A1` sqrt(2) equipartition | charged-lepton-specific amplitude constraint | not retained here |
| 2 | `P1` sqrt(m) identification | mass/readout map | not retained here |
| 3 | delta/radian unit bridge | maps `2/dim_R(M_3(C)_Herm) = 2/9` into the phase unit | not retained here |
| 4 | `v_0` scale derivation | absolute lepton-sector scale | heuristic / not retained here |

The physical `Cl(3)` on `Z^3` baseline is not in this table because it is
already the framework semantics. It should not be counted as a new axiom
or a new admitted premise.

## Bounded Claim

Under the baseline physical `Cl(3)` on `Z^3` reading, Option C provides a
bounded decomposition of the remaining AC/species-identification problem:

1. The `C_3`-equivariant Hermitian operators on the hw=1 three-state
   sector have the circulant form
   `H = a I + b C + conjugate(b) C^2`.
2. Their eigenvalues have the Brannen-Rivero form
   `lambda_k = a + 2 |b| cos(arg(b) + 2 pi k / 3)`.
3. Moving from corner basis to Fourier/eigenbasis relocates, but does not
   eliminate, the physical species-identification step.
4. The charged-lepton numerical match is a strong falsifiability anchor,
   but it cannot be used as derivational input in a retained theorem.
5. Full closure still requires the four inputs listed above to be derived,
   retained, or otherwise explicitly admitted under the repo process.

This note does not close A3, does not reduce any bridge-gap count by
itself, and does not promote a parent theorem/status surface. It makes the
remaining work more discoverable by separating the restored baseline from
the actual open scientific inputs.

## What Is Salvaged

The durable science is the bounded Option C decomposition:

- Fourier-basis re-identification is a real alternative to corner-basis
  phrasing, but it still requires a physical labeling/readout bridge.
- The Brannen-Rivero/circulant spectrum is the right finite-dimensional
  structural object to audit for this route.
- The prior "physical lattice" item was a vocabulary/process error, not a
  scientific admission.
- The remaining four gates are concrete and separately attackable.

## Empirical Anchor

The runner records the charged-lepton numerical match only as a
falsifiability and prioritization anchor. PDG charged-lepton masses are not
used as derivational premises.

At the documented benchmark (`delta = 2/9`, `A1 + P1`, and
`v_0 = (sum sqrt(m_k))/3`) the match is very sharp, but that sharpness
does not by itself turn the readout/scale assumptions into retained
theorems.

## Status

```yaml
actual_current_surface_status: bounded_decomposition
proposed_claim_type: bounded_theorem
audit_review_points: |
  Independent audit should check:
   (a) physical Cl(3) on Z^3 is treated as baseline repo semantics, not
       as a new admission;
   (b) the Fourier-basis route relocates rather than eliminates the
       species-identification/readout step;
   (c) the four remaining inputs are correctly classified as not retained
       by this note;
   (d) PDG values are used only as numerical/falsifiability anchors.
admitted_context_inputs:
  - A1_sqrt2_equipartition
  - P1_sqrtm_identification
  - delta_rad_unit_bridge
  - v_0_scale_derivation
independent_audit_required_before_any_effective_status_change: true
bare_retained_allowed: false
forbidden_imports_used_as_derivation: false
```

## Cross-references

- Baseline semantics:
  [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Minimal framework:
  `MINIMAL_AXIOMS_2026-05-03.md`
- Parent AC boundary:
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- R1 hostile review:
  [`A3_R1_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r1hr.md`](A3_R1_HOSTILE_REVIEW_CONFIRMS_OBSTRUCTION_NOTE_2026-05-08_r1hr.md)
- Koide circulant source note:
  [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Physical-lattice narrowed no-go:
  [`PHYSICAL_LATTICE_NECESSITY_NOTE.md`](PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- Three-generation observable:
  [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)

## Validation

Run:

```bash
python3 scripts/cl3_a3_option_c_brannen_rivero_2026_05_08_optC.py
```

The runner checks the circulant/eigenvalue algebra, the Fourier-basis
relocation boundary, the four-input decomposition, and the empirical-match
anchor without using the empirical values as derivational premises.
