# Perron-Frobenius Step-2 Microscopic Channel Target

**Date:** 2026-04-17  
**Status:** exact science-only target-reduction theorem for the remaining step-2A constructive object  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_microscopic_channel_target_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

After the PF lane has already proved:

- the first honest step-2A codomain is `Wilson -> D_- -> dW_e^H -> H_e`,
- the missing Wilson-side charged embedding cannot be supplied by support
  pullback,

what is the **actual next constructive target**?

## Bottom line

The next constructive target is a genuinely new **Wilson-to-charged
microscopic channel**.

More sharply:

1. `E_e` is already fixed;
2. `dW_e^H = Schur_{E_e}(D_-)` is already exact once `D_-` is supplied;
3. `dW_e^H` reconstructs `H_e`;
4. once the Hermitian pair is supplied, the PMNS projector packet is automatic.

So the remaining unresolved content is not:

- support labeling,
- projector readout,
- or downstream Hermitian packet algebra.

It is:

- how Wilson parent operator data produce the charged microscopic object
  `D_-`, or equivalently a direct operator law with the same charged
  microscopic content.

## What is already exact

### 1. The upstream/downstream split is already fixed

From
[PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md):

- any future positive step-2 completion must begin with one upstream
  Wilson-to-Hermitian descendant law;
- only after that, if needed, does the residual PMNS bridge amplitude appear.

So the current search target is the upstream channel, not the downstream PMNS
last mile.

### 2. The charged microscopic codomain is already functorially organized

From
[DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md):

- `dW_e^H = Schur_{E_e}(D_-)`;
- `dW_e^H` reconstructs `H_e`;
- once the charged microscopic block is supplied, the rest of the charged
  Hermitian chain is algorithmic.

So the unresolved content sits upstream of the Schur pushforward.

### 3. The projector packet is already downstream automatic

From
[DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md):

- once the Hermitian pair is supplied, the flavored transport projector packet
  is automatic.

So the open object is not another projector theorem.

### 4. Support pullback is already excluded

From
[PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md):

- the current support bank cannot obtain the missing charged embedding /
  compression object by pure pullback of `E_e`.

So the open object must carry genuinely new cross-sector microscopic content.

## Theorem 1: exact reduction of the live step-2A target to a microscopic channel

Assume the exact step-2 minimal positive-completion theorem, the exact charged
source-response reduction theorem, the exact PMNS projector-interface theorem,
and the exact charged-support pullback boundary theorem. Then:

1. step 2A is upstream of any residual PMNS selector amplitude;
2. the charged codomain data `E_e`, `dW_e^H`, `H_e`, and the projector packet
   are all downstream once the charged microscopic law is supplied;
3. the current support bank cannot supply that law by pure support pullback.

Therefore the live unresolved step-2A object is exactly a new
Wilson-to-charged microscopic channel, with the cleanest target being a
Wilson-to-`D_-` law and the direct Wilson-to-`dW_e^H` law only a compressed
alternative form.

## Corollary 1: the first positive proof attempt should target `D_-`

Because the Schur pushforward and Hermitian reconstruction are already exact,
the strongest constructive target is:

- `Wilson -> D_-`.

After that:

- `dW_e^H = Schur_{E_e}(D_-)`,
- `H_e`,
- and the projector packet

are already downstream.

## Corollary 2: step 2A is no longer a search over downstream PMNS algebra

The branch should not spend step-2A effort on:

- projector formulas,
- PMNS packet readout,
- support relabeling,
- or generic Hermitian bookkeeping.

Those objects are already downstream of the real missing microscopic channel.

## What this closes

- one exact identification of the remaining constructive content on step 2A;
- one sharper preference for `Wilson -> D_-` as the cleanest target form;
- one clearer separation between microscopic channel content and downstream
  PMNS/Hermitian readout.

## What this does not close

- a positive Wilson-to-`D_-` theorem;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive global PF selector.

## Why this matters

This note keeps the next step honest and efficient.

The branch no longer has to say merely:

- “the bridge is missing.”

It can now say:

- the missing content is exactly a new Wilson-to-charged microscopic channel,
  with `Wilson -> D_-` the cleanest target.

## Atlas inputs used

- [PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_MINIMAL_POSITIVE_COMPLETION_CLASS_NOTE_2026-04-17.md)
- [DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_PROJECTOR_INTERFACE_NOTE_2026-04-16.md)
- [PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_SUPPORT_PULLBACK_BOUNDARY_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_microscopic_channel_target_2026_04_17.py
```
