# Perron-Frobenius Step-2 Charged-Support Pullback Boundary

**Date:** 2026-04-17  
**Status:** exact science-only boundary theorem excluding support-pullback realization of the missing charged embedding  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_charged_support_pullback_boundary_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

Can the missing Wilson-side charged embedding / compression object

- `I_e`, or
- `P_e`,

be obtained just by **pulling back** the already-fixed charged support label
`E_e` through the current exact support bank?

## Bottom line

No.

The current exact support bank does **not** supply a Wilson-side charged
embedding / compression object by pure support pullback.

What is already exact:

1. the PMNS / DM lane fixes the charged support label `E_e`;
2. the charged Hermitian codomain is exactly
   `dW_e^H = Schur_{E_e}(D_-)`;
3. the site-phase / cube-shift intertwiner exactly transports taste-cube /
   BZ-corner support and explicitly declares its safe role to be support
   transport only.

So the current support bank knows:

- where the charged support lives on the PMNS side,
- and how to move statements between taste-cube and BZ-corner support.

But it does **not** know:

- how to pull Wilson parent data onto the charged microscopic support `E_e`.

Therefore the missing Wilson-side charged embedding / compression object is
not a hidden support-pullback corollary of the current bank.

## What is already exact

### 1. The PMNS side fixes `E_e`, but only on the charged microscopic codomain

From
[DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md):

- the lepton supports `E_nu` and `E_e` are fixed;
- once the Hermitian pair is supplied, the projector packet is automatic.

From
[DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md):

- `dW_e^H = Schur_{E_e}(D_-)`;
- the charged support sits inside the charged microscopic class.

So `E_e` is a fixed support label, but it is fixed on the charged PMNS / DM
codomain side, not yet on the Wilson parent space.

### 2. The current exact support intertwiner is narrower

From
[SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md):

- the full taste-cube operator algebra and the lattice BZ-corner support are
  exactly intertwined;
- the note states its safe role is support transport only.

So the current support bank transports support statements between:

- the taste cube,
- and the BZ-corner lattice support.

It does not yet transport Wilson parent transfer data into the charged support
`E_e`.

### 3. The current PF lane already excludes support-only bridge candidates

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md):

- another support-only intertwiner cannot honestly be the missing charged
  bridge;
- the future bridge must be more than support transport.

And from
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md):

- the current support bank still does not realize the missing cross-sector
  descendant law.

So the PF lane has already excluded the support-only class abstractly. The
present note sharpens that exclusion at the concrete charged-support object
level.

## Theorem 1: exact support-pullback boundary for the missing charged embedding

Assume the exact PMNS projector-interface theorem, the exact charged
source-response reduction theorem, the exact site-phase / cube-shift support
intertwiner, the exact step-2 bridge-candidate-shape boundary theorem, and the
exact current-bank nonrealization theorem. Then:

1. the charged support label `E_e` is fixed only on the PMNS / charged
   microscopic side;
2. the current support intertwiner moves statements only between taste-cube
   and BZ-corner support;
3. the current PF lane already excludes support-only constructions as honest
   charged-bridge candidates;
4. the current bank still contains no cross-sector descendant law realizing
   the Wilson-to-charged bridge.

Therefore the missing Wilson-side charged embedding / compression object cannot
be obtained as a pure pullback of `E_e` through the current exact support bank.

## Corollary 1: support-bank searches can stop

The next constructive step should not be:

- search for another taste-cube / BZ-corner support pullback,
- restate the site-phase intertwiner with PMNS labels attached,
- treat `E_e` itself as if it were already a Wilson-side subspace theorem.

Those routes are now closed.

## Corollary 2: the missing object must carry new cross-sector microscopic content

Any future explicit Wilson-side charged embedding / compression object
`I_e` or `P_e` must carry genuinely new content beyond support transport.

It has to specify how Wilson parent operator data land in the charged
microscopic sector, not just how support bases are relabeled.

## What this closes

- one exact exclusion of the support-pullback shortcut for the missing charged
  embedding;
- one clearer separation between PMNS-side support labels and Wilson-side
  embedding data;
- one sharper statement that the next positive step must be microscopic and
  cross-sector, not support-only.

## What this does not close

- an explicit Wilson-side charged embedding / compression object;
- a positive Wilson-to-`D_-` theorem;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive global PF selector.

## Why this matters

This note prevents a subtle but likely review drift:

> maybe the missing charged embedding is already implicit once `E_e` and the
> support intertwiners are known.

Answer: no.

The current support bank does not yet reach that object. So the remaining PF
step-2A target is not another support theorem. It is a genuinely new
cross-sector operator law.

## Atlas inputs used

- [DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md)
- [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_BRIDGE_CANDIDATE_SHAPE_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_charged_support_pullback_boundary_2026_04_17.py
```
