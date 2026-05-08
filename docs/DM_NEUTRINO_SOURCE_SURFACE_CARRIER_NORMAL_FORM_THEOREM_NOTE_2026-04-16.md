# DM Neutrino Source-Surface Carrier Normal-Form Theorem

**Date:** 2026-04-16  
**Status:** exact blocker-reduction theorem on the mainline post-canonical gate  
**Script:** `scripts/frontier_dm_neutrino_source_surface_carrier_normal_form.py`

## Question

On the live source-oriented sheet of the exact `H`-side source surface, what is
the smallest carrier-side normal form for the remaining mainline inverse-image
problem?

## Bottom line

After quotienting by the exact common diagonal-shift tangent, the live
source-oriented sheet factors through the minimal Hermitian bridge carrier

- `B_H,min = (Lambda_+, Lambda_odd, u, v, delta, rho, gamma)`

and the exact source surface becomes the three-equation normal form

- `gamma = 1/2`
- `delta + rho = sqrt(8/3)`
- `sigma sin(2v) = 8/9`

with

- `sigma = -Lambda_+ + Lambda_odd + u`

So the remaining mainline object is no longer a generic `7`-real `H`-grammar
law. It is a shift-quotiented carrier-side inverse-image law on the live
source-oriented sheet.

## Exact carrier formula

On the carrier core,

- `A + b - c - d = 3 sqrt(2) sigma sin(2v) / 4`

So the third source-surface condition `A + b - c - d = sqrt(8)/3` is
equivalent to

- `sigma sin(2v) = 8/9`

That is the exact even-response carrier constraint on the sharp
source-oriented branch.

## Shift quotient

The exact common diagonal-shift tangent acts by

- `Lambda_+ -> Lambda_+ + lambda`
- `Lambda_odd -> Lambda_odd + lambda`

while leaving

- `u`
- `v`
- `delta`
- `rho`
- `gamma`
- `sigma`

unchanged.

So the exact source-surface normal form is already naturally shift-quotiented.

## Exact consequence

The honest mainline blocker is now smaller still on the live source-oriented
sheet:

- derive the post-canonical mixed-bridge law that populates the carrier normal
  form `gamma = 1/2`, `delta + rho = sqrt(8/3)`, `sigma sin(2v) = 8/9`

equivalently

- derive the residual `3`-real even-response law on the carrier side

instead of reopening a generic `H`-grammar search.

## Command

```bash
python3 scripts/frontier_dm_neutrino_source_surface_carrier_normal_form.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [dm_neutrino_exact_h_source_surface_preimage_bundle_theorem_note_2026-04-16](DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_PREIMAGE_BUNDLE_THEOREM_NOTE_2026-04-16.md)
- [dm_neutrino_hermitian_bridge_carrier_note_2026-04-15](DM_NEUTRINO_HERMITIAN_BRIDGE_CARRIER_NOTE_2026-04-15.md)
- [dm_neutrino_positive_polar_h_cp_theorem_note_2026-04-15](DM_NEUTRINO_POSITIVE_POLAR_H_CP_THEOREM_NOTE_2026-04-15.md)
- [dm_neutrino_breaking_triplet_cp_theorem_note_2026-04-15](DM_NEUTRINO_BREAKING_TRIPLET_CP_THEOREM_NOTE_2026-04-15.md)
