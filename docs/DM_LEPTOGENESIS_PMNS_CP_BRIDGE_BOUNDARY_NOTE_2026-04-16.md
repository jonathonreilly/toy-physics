# DM Leptogenesis PMNS/Mainline CP Bridge Boundary

**Date:** 2026-04-16
**Status:** support - structural or confirmatory support note
to the mainline post-canonical leptogenesis CP package
**Claim type:** bounded_theorem
**Script:** `scripts/frontier_dm_leptogenesis_pmns_cp_bridge_boundary.py`

## Inputs (cited authorities)

The runner imports `canonical_h`, `cp_formula`, `cp_pair_from_h`,
`h_from_breaking_triplet`, and `exact_package` from helper modules.
Each of those imported constructions is supplied by a one-hop
authority on the current dependency surface:

- `canonical_h`, `h_from_breaking_triplet`, breaking-triplet grammar:
  [`DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md)
  and
  [`DM_LEPTOGENESIS_PMNS_BREAKING_TRIPLET_SOURCE_LAW_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_BREAKING_TRIPLET_SOURCE_LAW_NOTE_2026-04-16.md);
- `cp_formula`, `cp_pair_from_h` (CP pair from breaking-triplet
  parameters): same projector-interface note above;
- `exact_package` (exact source-oriented mainline leptogenesis CP
  package with `gamma = 1/2`, `E1 = sqrt(8/3)`, `E2 = sqrt(8)/3`):
  [`DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md`](DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md)
  and
  [`DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md).

The note's contribution is the comparator: the runner shows that the
canonical PMNS near-closing sample produces the opposite CP sign
pattern from the source-oriented mainline package. The cited primitives
are not re-derived; the note's load-bearing claim is the sign-split
verdict conditional on those imported inputs.

## Question

Does the canonical near-closing PMNS-assisted `N_e` sample already realize the
same source-oriented CP package as the mainline exact leptogenesis branch?

## Bottom line

No.

The canonical off-seed `N_e` sample decomposes exactly on the same
breaking-triplet grammar used by the mainline CP theorem, but it lands on the
opposite CP orientation sheet.

On the canonical PMNS `N_e` sample:

- `gamma = 0.13047275751299414`
- `delta + rho = -0.6782032360883523`
- `A + b - c - d = -0.9742967639116479`

so the intrinsic CP pair is

- `cp1 = +0.0589913642444558`
- `cp2 = -0.08474612361569306`.

By contrast, the exact source-oriented mainline leptogenesis package fixes

- `gamma = 1/2`
- `E1 = sqrt(8/3)`
- `E2 = sqrt(8)/3`

and therefore

- `cp1 = -0.5443310539518174`
- `cp2 = +0.3142696805273545`.

So the PMNS canonical near-closing sample has the **opposite CP sign pattern**
from the exact source-oriented mainline package.

## Exact consequence

This sharpens the role of the PMNS lane.

The PMNS-assisted `N_e` route is still an exact and valuable comparator:

- it reduces the old one-flavor miss to `eta/eta_obs = 0.9895127046003488`
- it isolates the off-seed charged-sector `5`-real source law
- it reconstructs the full `D -> D_- -> dW_e^H -> H_e -> packet -> eta` chain

But it is **not yet** a constructive witness for the live mainline CP package,
because the canonical near-closing PMNS sample does not land on the same CP
sheet.

## Meaning for the remaining blocker

The remaining bridge is now sharper.

It is not enough to derive some off-seed charged-sector `5`-real law that
nearly closes transport. The missing constructive bridge is:

- a microscopic full-`D` / off-seed charged-sector value law that lands on the
  source-oriented post-canonical CP sheet of the live leptogenesis branch

or, failing that,

- a stronger exact incompatibility theorem showing that the current PMNS
  near-closing comparator cannot realize that sheet.

## Scope

This note does **not** prove that the PMNS route is useless.

It proves only that the current canonical near-closing PMNS comparator is not
yet the same object as the exact source-oriented mainline CP package.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_cp_bridge_boundary.py
```
