# Perron-Frobenius Step-2 Active Five-Real Current-Bank Nonrealization

**Date:** 2026-04-17  
**Status:** exact science-only nonrealization theorem for the smallest live step-2A packet on the current bank  
**Atlas front door:** `docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_perron_frobenius_step2_active_five_real_current_bank_nonrealization_2026_04_17.py`  
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Question

After the PF lane has reduced step 2A to the active off-seed `5`-real source

`(xi_1, xi_2, eta_1, eta_2, delta)`,

does the **current exact bank** already determine that packet?

## Bottom line

No.

The current exact bank still does **not** realize the active off-seed
`5`-real packet on the charged-lepton branch.

What the bank already fixes:

- branch / orientation structure,
- aligned seed averages,
- active-block transport locality,
- aligned dominant-mode law,
- charged Hermitian codomain / projector readout once microscopic data are
  supplied.

What it still does **not** fix:

- the off-seed active `5`-real source packet
  `(xi_1, xi_2, eta_1, eta_2, delta)`.

So the next missing constructive object is now exact and singular: this one
packet.

## What is already exact

### 1. PMNS internal exactness stops before the off-seed packet

From
[PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md](./PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md):

- the aligned transfer law fixes the aligned seed pair exactly;
- it does **not** determine the generic `5`-real corner-breaking source.

So PMNS internal dominant-mode exactness still stops before the live off-seed
packet.

### 2. One-sided PMNS reduction already says the live remaining object is the active five-real source

From
[DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md):

- the one-sided transport object reduces to the active block;
- after branch/orientation and seed averages are imported, the remaining
  object is exactly the active five-real source.

From
[DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md):

- the remaining `D`-level object is only the active off-seed `5`-real
  breaking source.

So the PMNS / DM bank already identifies the packet, but does not derive it.

### 3. The Wilson-side PF bank still does not realize the corresponding upstream route

From
[PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md):

- the current exact bank does **not** already contain the missing
  Wilson-to-`D_-` / Wilson-to-`dW_e^H` descendant theorem under another name.

So the Wilson-side exact bank does not yet realize the packet upstream either.

## Theorem 1: exact current-bank nonrealization of the active off-seed five-real packet

Assume the exact PMNS transfer dominant-mode theorem, the exact PMNS
active-projector reduction theorem, the exact PMNS microscopic `D` last-mile
reduction theorem, and the exact Wilson-to-Hermitian current-bank
nonrealization theorem. Then:

1. the current PMNS transfer law fixes only the aligned seed pair, not the
   generic off-seed `5`-real packet;
2. the one-sided PMNS / DM reduction stack already identifies that packet as
   the smallest live remaining object;
3. the Wilson-side PF bank does not yet realize the corresponding upstream
   descendant theorem.

Therefore the current exact bank still does **not** determine the active
off-seed `5`-real source
`(xi_1, xi_2, eta_1, eta_2, delta)`.

## Corollary 1: the next missing construction is one exact packet, not a family

The remaining constructive target is now fully isolated:

- one active off-seed `5`-real packet on the charged-lepton branch.

## Corollary 2: current-bank global PF nonclosure really sits on this packet

On the PMNS side, after all current reductions, the missing global PF closure
content is no longer vague provenance rhetoric. It includes this exact missing
packet.

## What this closes

- one exact nonrealization statement for the smallest live PMNS-side step-2A
  packet;
- one sharper handoff from reduction theorems to positive construction;
- one clearer statement of where current-bank global PF nonclosure still lives
  on the PMNS branch.

## What this does not close

- a positive Wilson-to-`D_-` theorem;
- a positive Wilson-to-`dW_e^H` theorem;
- a positive global PF selector.

## Why this matters

This note eliminates the last remaining “maybe the packet is already fixed”
drift.

The branch can now say exactly:

- the live PMNS-side obstruction is one explicit off-seed `5`-real packet,
- and the current exact bank does not yet determine it.

## Atlas inputs used

- [PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md](./PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md)
- [DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_ACTIVE_PROJECTOR_REDUCTION_NOTE_2026-04-16.md)
- [DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MICROSCOPIC_D_LAST_MILE_NOTE_2026-04-16.md)
- [PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md](./PERRON_FROBENIUS_WILSON_TO_HERMITIAN_DESCENDANT_CURRENT_BANK_NONREALIZATION_NOTE_2026-04-17.md)

## Command

```bash
python3 scripts/frontier_perron_frobenius_step2_active_five_real_current_bank_nonrealization_2026_04_17.py
```
