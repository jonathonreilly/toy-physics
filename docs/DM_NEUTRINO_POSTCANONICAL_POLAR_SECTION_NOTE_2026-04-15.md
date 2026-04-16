# DM Neutrino Post-Canonical Positive Polar Section

**Date:** 2026-04-15  
**Status:** exact generic positive-section theorem on the intrinsic DM
post-canonical bridge  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_postcanonical_polar_section.py`

## Question

After the exact post-canonical extension-class theorem, the exact slot-support
class theorem, and the exact raw right-frame obstruction, is the remaining DM
bridge still only an orbit-dependent extension target?

Or does the generic full-rank right orbit already admit a canonical
representative that makes the bridge intrinsic from

`H = Y Y^dag`

alone?

## Bottom line

Yes, on the generic full-rank patch.

The raw right-frame obstruction only ruled out the stronger claim that the
bridge data on an **arbitrary** orbit representative are already intrinsic.
That is false.

But for any full-rank Yukawa matrix `Y`, the exact right orbit still carries
the unique positive polar representative

`Y_+(H) = H^(1/2)`.

For that representative,

`K_+(H) = Y_+(H)^dag Y_+(H) = H`.

So the remaining post-canonical singlet-doublet bridge is already read
intrinsically from `H` through

`K_Z3(H) = U_Z3^dag H U_Z3`.

If we denote

- `a(H) = (K_Z3(H))_01`
- `b(H) = (K_Z3(H))_02`

then after the exact real Majorana doublet rotation

`K_mass(H) = R^T K_Z3(H) R`

the physical entries are exactly

- `(K_mass(H))_01 = (a(H) - b(H))/sqrt(2)`
- `(K_mass(H))_02 = (a(H) + b(H))/sqrt(2)`

and the physical leptogenesis tensor becomes

- `Im[(K_mass(H))_01^2] = Im[(a(H)-b(H))^2 / 2]`
- `Im[(K_mass(H))_02^2] = Im[(a(H)+b(H))^2 / 2]`

So the generic full-rank right orbit already has a canonical intrinsic DM
bridge from `H`.

## Inputs

This note sharpens and reuses:

- [DM_NEUTRINO_POSTCANONICAL_EXTENSION_CLASS_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_EXTENSION_CLASS_NOTE_2026-04-15.md)
- [DM_NEUTRINO_POSTCANONICAL_SLOT_SUPPORT_CLASS_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_SLOT_SUPPORT_CLASS_NOTE_2026-04-15.md)
- [DM_NEUTRINO_POSTCANONICAL_RIGHT_FRAME_OBSTRUCTION_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_RIGHT_FRAME_OBSTRUCTION_NOTE_2026-04-15.md)
- [DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_SINGLET_DOUBLET_CP_SLOT_TOOL_NOTE_2026-04-15.md)
- [PMNS_RIGHT_POLAR_SECTION_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_RIGHT_POLAR_SECTION_NOTE.md:1)

The PMNS note gives the structural template. This note transfers that exact
positive-section logic onto the live DM denominator object.

## Exact positive-section theorem

### 1. The generic full-rank right orbit has a unique positive representative

If `Y` is full rank and

`H = Y Y^dag`,

then the left polar decomposition gives

`Y = H^(1/2) U_R`

with `U_R in U(3)` and a unique positive Hermitian factor `H^(1/2)`.

So the generic full-rank right orbit already carries the canonical intrinsic
representative

`Y_+(H) = H^(1/2)`.

### 2. The post-canonical bridge is read directly from `H`

For the positive representative,

`K_+(H) = Y_+(H)^dag Y_+(H) = H`.

Therefore the exact remaining bridge data live directly in the transformed
Hermitian kernel

`K_Z3(H) = U_Z3^dag H U_Z3`.

The post-canonical singlet-doublet slot pair is therefore intrinsic:

- `a(H) = (K_Z3(H))_01`
- `b(H) = (K_Z3(H))_02`

and the physical heavy-neutrino-basis entries are

- `(K_mass(H))_01 = (a(H)-b(H))/sqrt(2)`
- `(K_mass(H))_02 = (a(H)+b(H))/sqrt(2)`.

So the physical CP carrier is already a function of `H` alone on this patch.

### 3. The generic full-rank `H` patch is not CP-empty

The runner checks explicit branch samples and generic random canonical samples.
On those full-rank `H` data, the positive-section CP tensor is generically
nonzero.

So the positive-section route is not merely formal. It is the first exact
constructive intrinsicization of the remaining DM bridge on the generic patch.

## The theorem-level statement

**Theorem (Generic positive polar section for the DM post-canonical bridge).**
Assume the exact post-canonical DM extension-class theorem, the exact
slot-support-class theorem, and the exact raw right-frame obstruction theorem.
Then on the generic full-rank patch:

1. every right orbit `Y -> Y U_R^dag` admits the unique positive intrinsic
   representative `Y_+(H) = H^(1/2)`
2. on that representative, `K_+(H) = H`
3. the remaining singlet-doublet bridge is therefore read intrinsically from
   `H` through the slot pair
   `a(H) = (U_Z3^dag H U_Z3)_01`,
   `b(H) = (U_Z3^dag H U_Z3)_02`
4. the physical heavy-neutrino-basis CP tensor is an exact function of that
   intrinsic slot pair

So the raw right-frame obstruction is not the final endpoint. On the generic
full-rank patch, the current stack already carries a canonical intrinsic DM
bridge from `H`.

## What this closes

This closes the old blocker wording

> derive a genuinely new right-frame-fixing theorem or right-sensitive
> observable principle

as the universal next step.

That is no longer the honest generic endpoint.

It is now exact that:

- the raw right-frame obstruction is **not** a total no-section theorem
- the generic full-rank right orbit already has a canonical intrinsic section
  `Y_+(H) = H^(1/2)`
- the remaining DM bridge is intrinsically readable from `H` on that patch

## What this does not close

This note does **not** prove that the branch’s actual `H`-law lands on a
CP-supporting patch.

That remaining question moves to the Hermitian-data side:

- what `H` does the active neutrino lane actually derive?
- does it sit on the CP-empty residual-`Z_2` aligned core, or beyond it?

That sharper boundary is handled next by the aligned-core no-go.

## Command

```bash
python3 scripts/frontier_dm_neutrino_postcanonical_polar_section.py
```
