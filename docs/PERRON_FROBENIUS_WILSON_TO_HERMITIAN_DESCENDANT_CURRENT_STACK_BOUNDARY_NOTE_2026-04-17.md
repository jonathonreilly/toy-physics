# Perron-Frobenius Wilson-to-Hermitian Descendant Current-Stack Boundary

**Date:** 2026-04-17  
**Status:** exact science-only boundary theorem for step 2A on the current stack  
**Script:** `scripts/frontier_perron_frobenius_wilson_to_hermitian_descendant_current_stack_boundary_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

After reducing the first honest PMNS-side descendant target to

- `Wilson -> D_- -> dW_e^H -> H_e`,

what exactly is still missing on the current stack?

## Answer

The missing object is now completely sharp.

The repo already has:

1. the Wilson parent object and its exact plaquette / `theta` descendants;
2. the full microscopic PMNS-assisted chain
   `D -> D_- -> dW_e^H -> H_e -> packet -> eta`
   once `D` is supplied;
3. exact constructive and selector reductions directly on the projected source
   pack `dW_e^H`.

What the repo still does **not** have is:

- a theorem carrying the Wilson parent structure into the microscopic PMNS
  operator chain,
- in particular, no Wilson-to-`D_-` law and no Wilson-to-`dW_e^H` law.

So step 2A is no longer blocked by codomain ambiguity.
It is blocked exactly by the missing **Wilson-to-Hermitian descendant map**.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md):

- the Wilson parent object is exact on the gauge surface,
- plaquette and `theta` descendants are exact,
- PMNS is not yet shown to be a canonical descendant.

From
[DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md):

- once full microscopic `D` is supplied, the chain
  `D -> D_- -> dW_e^H -> H_e -> packet -> eta`
  is already exact and algorithmic.

From
[DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_PROJECTED_SOURCE_SELECTOR_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_PROJECTED_SOURCE_SELECTOR_THEOREM_NOTE_2026-04-16.md):

- the constructive projected-source sign chamber is already nonempty on
  `dW_e^H`.

From
[DM_LEPTOGENESIS_PMNS_MINIMAL_A13_SHEET_SELECTOR_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MINIMAL_A13_SHEET_SELECTOR_THEOREM_NOTE_2026-04-16.md):

- the residual sheet selector is already reduced to the sign of `A13` on
  `dW_e^H`.

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md):

- the first honest step-2A codomain is exactly
  `D_- / dW_e^H / H_e`.

## Theorem 1: exact current-stack boundary on step 2A

On the current exact stack:

1. the PMNS-side Hermitian codomain is already exact once microscopic `D` is
   supplied;
2. constructive existence and minimal sheet-selection reduction are already
   exact directly on `dW_e^H`;
3. but the Wilson parent/compression theorem still does not identify either
   `D_-` or `dW_e^H` as a canonical descendant of the Wilson parent object.

Therefore the exact remaining step-2A blocker is:

- a **Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem**.

## Corollary 1: step 2A is not blocked by downstream transport or selector design

The branch no longer needs:

- a new packet theorem,
- a new constructive-existence theorem on `dW_e^H`,
- or a new minimal selector-reduction theorem on `dW_e^H`.

Those are already present.

So the missing work is upstream provenance, not downstream PMNS bookkeeping.

## Corollary 2: once step 2A lands, step 2B is already sharply posed

If the Wilson descendant law reaches `dW_e^H`, then the remaining PMNS-side
object is already known:

- the right-sensitive selector on `dW_e^H`,
- equivalently the residual odd/current datum.

So step 2A and step 2B are now separated cleanly.

## What this closes

- one exact current-stack boundary for the first PMNS-side descendant lane
- one exact statement that the missing step-2A object is upstream provenance,
  not downstream Hermitian transport structure
- one exact separation between the codomain chain already known and the Wilson
  map still missing

## What this does not close

- the Wilson-to-`D_-` theorem itself
- the Wilson-to-`dW_e^H` theorem itself
- the residual right-sensitive PMNS selector law
- global PF compatibility

## Atlas inputs used

- [GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md)
- [DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_PROJECTED_SOURCE_SELECTOR_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_PROJECTED_SOURCE_SELECTOR_THEOREM_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_PMNS_MINIMAL_A13_SHEET_SELECTOR_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MINIMAL_A13_SHEET_SELECTOR_THEOREM_NOTE_2026-04-16.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_REDUCTION_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_wilson_to_hermitian_descendant_current_stack_boundary_2026_04_17.py
```
