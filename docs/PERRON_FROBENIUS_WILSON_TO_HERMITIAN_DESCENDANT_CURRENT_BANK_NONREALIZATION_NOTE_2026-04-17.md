# Perron-Frobenius Wilson-to-Hermitian Descendant Current-Bank Nonrealization

**Date:** 2026-04-17  
**Status:** exact science-only current-bank nonrealization theorem for the missing step-2A bridge  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_wilson_to_hermitian_descendant_current_bank_nonrealization_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

After the PF lane reduced step 2A to the charged-sector chain

`Wilson -> D_- -> dW_e^H -> H_e`,

does the **current exact bank already contain that missing bridge under another
name**?

## Bottom line

No.

The current bank contains:

1. an exact Wilson parent object with canonical plaquette and `theta`
   descendants;
2. an exact scalar observable backbone on determinant source-response data;
3. exact support intertwiners on the taste-cube / BZ-corner side;
4. exact PMNS and DM microscopic reduction theorems **once microscopic `D` is
   supplied**;
5. exact PMNS-side nonselection / nonforcing theorems showing that the current
   selector and support bank still lacks the needed inter-sector bridge.

But none of those objects is already an exact descendant/intertwiner law from
the Wilson parent surface into the charged-sector microscopic chain
`D_- -> dW_e^H -> H_e`.

So the current bank does **not** already realize the missing step-2A bridge.

## What was checked

### 1. The Wilson parent object stays on the gauge surface

From
[GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md):

- the exact Wilson parent object already has canonical plaquette and `theta`
  descendants;
- that theorem explicitly stops before PMNS provenance.

So the current positive parent theorem is real, but gauge-side only.

### 2. The observable principle is still scalar

From
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):

- the exact current observable generator is

  `W[J] = log|det(D+J)| - log|det D|`;

- its exact derivatives are scalar source responses built from traces of
  resolvent insertions.

So the present observable backbone is exact and important, but it is not yet a
matrix-valued charged-sector descendant law into `D_-` or `dW_e^H`.

### 3. The support intertwiners stay support-side

From [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md):

- the full taste-cube operator algebra and the lattice BZ-corner support are
  exactly intertwined on restricted support;
- the note explicitly says its safe role is support transport only.

So the current exact support intertwiner does not yet carry Wilson parent data
into the charged Hermitian source-response chain.

### 4. The PMNS / DM microscopic chain starts only after `D` is supplied

From
[DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md)
and
[DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md):

- the exact microscopic chain is

  `D -> D_- -> dW_e^H -> H_e -> packet -> eta`;

- `dW_e^H = Schur_{E_e}(D_-)`;
- `dW_e^H` reconstructs `H_e` exactly;
- those notes explicitly do **not** yet evaluate `D_-` or `dW_e^H` from the
  sole axiom.

So the current PMNS-side exactness begins at supplied microscopic `D`, not at a
Wilson descendant theorem.

### 5. The current PMNS selector/support bank still lacks the inter-sector bridge

From
[PMNS_SELECTOR_BANK_NONREALIZATION_NOTE.md](./PMNS_SELECTOR_BANK_NONREALIZATION_NOTE.md)
and
[PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md](./PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md):

- the current exact selector bank acts on other domains;
- no retained bridge theorem maps those selector outputs into the PMNS branch
  datum;
- no retained sector-sensitive inter-sector bridge theorem is currently
  present.

So even the PMNS-side selector bank already proves the relevant negative fact:
the needed bridge is not hiding elsewhere in the current exact toolkit.

## Theorem 1: current-bank nonrealization of the Wilson-to-Hermitian descendant

Assume the current exact PF stack, the exact Wilson parent/compression theorem,
the exact observable-principle theorem, the exact site-phase / cube-shift
support intertwiner, the exact PMNS / DM microscopic reduction notes, and the
exact PMNS selector-bank nonrealization / sector-exchange nonforcing theorems.
Then:

1. the current bank already realizes one Wilson parent object, but only with
   gauge-surface plaquette and `theta` descendants;
2. the current bank already realizes an exact scalar observable backbone, but
   not a charged-sector matrix-valued descendant law;
3. the current bank already realizes exact support intertwiners, but only on
   the support-side taste-cube / BZ-corner bridge;
4. the current PMNS / DM microscopic chain is exact only once microscopic `D`
   is supplied;
5. the current selector/support bank still contains no retained inter-sector
   bridge theorem carrying data into the PMNS branch datum.

Therefore the current exact bank does **not** already contain the missing
Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem under another name.

## Corollary 1: step 2A is not blocked by hidden bank redundancy

The step-2A problem is therefore no longer:

- scan the current exact bank for another renamed bridge candidate.

It is:

- derive a genuinely new Wilson-to-`D_-` / Wilson-to-`dW_e^H`
  descendant/intertwiner law.

## Corollary 2: the admissible next moves are now narrower

The next honest science moves are exactly:

1. derive a new Wilson-to-`D_-` law;
2. derive a new Wilson-to-`dW_e^H` law directly;
3. derive an equivalent nontrivial sole-axiom PMNS transfer construction strong
   enough to play that role.

Not admissible anymore:

- more bank-scanning for a hidden existing bridge,
- more support-only PMNS exactness as if it solved provenance,
- more plaquette-side PF formalism as if it closed the PMNS descendant gap.

## What this closes

- the hidden-bridge loophole on step 2A;
- one exact distinction between existing Wilson, observable, support, and PMNS
  tools versus the still-missing cross-sector descendant law;
- one sharper theorem order for the next PF work.

## What this does not close

- a positive Wilson-to-`D_-` theorem;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive global PF selector;
- explicit plaquette `beta = 6` operator closure.

## Why this matters

This note is the hard-review-safe negative companion to the step-2A reduction
note.

It says not only:

- what the missing bridge theorem should look like,

but also:

- that the current exact bank does not already contain it.

So the PF lane no longer has to spend time defending against the review
question:

> maybe the cross-sector bridge is already present somewhere in the current
> bank under a different label.

Answer: no.

## Atlas inputs used

- [GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md](./SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
- [DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md)
- [PMNS_SELECTOR_BANK_NONREALIZATION_NOTE.md](./PMNS_SELECTOR_BANK_NONREALIZATION_NOTE.md)
- [PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md](./PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_wilson_to_hermitian_descendant_current_bank_nonrealization_2026_04_17.py
```
