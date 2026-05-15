# DM Neutrino Hermitian Bridge Carrier

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_neutrino_hermitian_bridge_carrier.py`

## Question

Now that the denominator is expressed on the active Hermitian PMNS lane, what
is the exact DM-side carrier object?

Does DM still need a new local carrier, or does the local neutrino lane already
fix it?

## Bottom line

The local neutrino lane already fixes the exact DM-side carrier.

The minimal continuous carrier is

`B_H,min = (A, B, u, v, delta, rho, gamma)`,

where:

- `(A, B)` is the weak-axis seed pair
- `(u, v)` is the aligned deformation pair
- `(delta, rho, gamma)` is the breaking-triplet complement

If the selector leg is included too, the exact unified carrier is

`U_min = (A, B, u, v, delta, rho, gamma, a_sel, e)`,

with:

- `a_sel` the reduced selector amplitude slot
- `e in {0,1}` the optional seed-edge selector bit

So the denominator is no longer blocked on "finding a local carrier."
That carrier is already fixed. The live problem is populating it with a
positive axiom-side value law.

## Exact DM-side reconstruction

On the canonical active Hermitian branch,

`H = H_core + B(delta,rho,gamma)`,

with

`H_core = [[a,b,b],[b,c,d],[b,d,c]]`

and

`B(delta,rho,gamma) = [[0,rho,-rho-i gamma],[rho,delta,0],[-rho+i gamma,0,-delta]]`.

The aligned core is reconstructed exactly from the four-real bridge data
`(A,B,u,v)`, and the breaking leg is reconstructed exactly from
`(delta,rho,gamma)`.

So the full active Hermitian grammar is exactly a `4 + 3` package:

- rank `4` aligned core
- rank `3` breaking-source complement

That is the exact DM-side meaning of the local neutrino-lane bridge package.

## Unified carrier

If the selector primitive is included, the exact unified bundle is

`U_min = (A, B, u, v, delta, rho, gamma, a_sel, e)`.

This does not replace `B_H,min`. It extends it.

So the safe reading is:

- `B_H,min` is the exact Hermitian bridge carrier for the DM denominator
- `U_min` is the smallest exact unified carrier if the selector leg must be
  carried alongside the Hermitian bridge

## What this closes

This closes the carrier question.

It is now exact that the DM denominator is **not** blocked on:

- inventing a new local CP carrier
- inventing a smaller hidden Hermitian bridge
- rephrasing the triplet in older raw slot coordinates

The exact carrier is already known.

## What this does not close

This note does **not** derive:

- the values of `(A,B,u,v,delta,rho,gamma)`
- the selector amplitude `a_sel`
- the seed-edge bit `e`
- any cross-sector law that populates `gamma`

So this is a carrier transplant theorem, not a positive denominator closure
theorem.

## Command

```bash
python3 scripts/frontier_dm_neutrino_hermitian_bridge_carrier.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [dm_neutrino_exact_h_source_surface_theorem_note_2026-04-16](DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16.md)
- [pmns_active_four_real_source_from_transport_note](PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md)
- [dm_neutrino_dirac_bridge_theorem_note_2026-04-15](DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
- `DM_NEUTRINO_SOURCE_SURFACE_CARRIER_SIDE_CONCLUSION_NOTE_2026-04-18.md` <!-- cycle-break 2026-05-15: forward reference (this 04-15 carrier note is upstream of the 04-18 side-conclusion); link backticked to break 49 dep cycles via dm_neutrino_source_surface_carrier_normal_form_theorem_note_2026-04-16 -->
