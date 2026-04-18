# Perron-Frobenius Review Status

**Date:** 2026-04-18  
**Status:** science-only reviewer summary of what the PF program now proves on
the review branch and what it does not prove  
**Primary verifier:** `scripts/frontier_perron_frobenius_selection_axiom_boundary.py`

## Review question

What is the clean reviewer-facing status of the Perron-Frobenius program on
this branch?

## Short answer

The branch now supports a strong **negative current-bank closure** result.

It does **not** support a positive theorem that the sole axiom already derives
one common global Perron-Frobenius physical-state selector.

That is not because the PF program failed. It is because the PF program has now
been reduced far enough to show exactly where the present exact bank stops.

## What is exact on this branch

1. **Sector-local PF science is real.**
   - Plaquette Perron reduction is exact on explicit positive finite operators.
   - Strong-CP positivity selection is exact at `theta = 0`.
   - PMNS dominant-mode/readout theorems are exact on their explicit transfer
     kernels.

2. **The current bank is fully closed negatively for a positive global
   sole-axiom PF selector.**
   - Wilson current-bank reopening route: negatively closed.
   - PMNS-native production route: negatively closed.
   - Plaquette non-Wilson first constructive route: negatively closed.

3. **The frontier is now reviewably small.**
   The sharpest current frontier certificates are:
   - Wilson: one local nilpotent-chain `1 + 1` certificate,
   - PMNS-native: one fixed-slice scalar production discriminant,
   - Plaquette: one first Hankel + `K` certificate.

## What is not exact on this branch

1. There is still **no** theorem-grade nontrivial sole-axiom PMNS
   source/transfer pack.
2. There is still **no** theorem-grade Wilson-to-PMNS descendant/projection
   theorem.
3. There is still **no** unique framework-point plaquette `beta = 6` PF object
   derived from the present bank.
4. Therefore there is still **no** positive global sole-axiom PF selector
   theorem on the present bank.

## Correct reviewer reading

The right reading is:

- PF is a successful exact-theorem program inside the repo.
- PF does not currently deliver the stronger global selector claim.
- The present bank is now sharply bounded.
- Any future positive reopening would require genuinely new science.

## Wilson and reopening

Wilson remains important, but only in the right sense.

On the **present bank**, the Wilson route is already negatively closed at its
sharpest local level.

Under **stronger future science**, Wilson remains the main plausible reopening
lever, because the strongest candidate positive route would still run through a
stronger Wilson constructive law.

That distinction matters for review:

- **current-bank status:** closed negatively,
- **future-theory status:** Wilson is still the main plausible reopening lever.

## Implication for the repo

This branch should be reviewed as a **science-only boundary result**.

It is suitable for review because it now gives:

- one exact statement of what PF already proves,
- one exact statement of what PF does not yet prove,
- one exact statement of where stronger future science would have to enter.

It should **not** be reviewed as a branch claiming that the sole axiom already
derives a positive global PF selector.

## Main supporting notes

- [PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md)
- [PERRON_FROBENIUS_CURRENT_BANK_FULL_FRONTIER_CLOSURE_NOTE_2026-04-18.md](./PERRON_FROBENIUS_CURRENT_BANK_FULL_FRONTIER_CLOSURE_NOTE_2026-04-18.md)
- [PERRON_FROBENIUS_WILSON_CURRENT_BANK_COMPLETE_CLOSURE_NOTE_2026-04-18.md](./PERRON_FROBENIUS_WILSON_CURRENT_BANK_COMPLETE_CLOSURE_NOTE_2026-04-18.md)
- [PMNS_GRAPH_FIRST_FIXED_SLICE_SCALAR_PRODUCTION_DISCRIMINANT_NOTE_2026-04-18.md](./PMNS_GRAPH_FIRST_FIXED_SLICE_SCALAR_PRODUCTION_DISCRIMINANT_NOTE_2026-04-18.md)
- [GAUGE_VACUUM_PLAQUETTE_BETA6_FIRST_HANKEL_CERTIFICATE_NOTE_2026-04-18.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_FIRST_HANKEL_CERTIFICATE_NOTE_2026-04-18.md)

## Verification

```bash
python3 scripts/frontier_perron_frobenius_selection_axiom_boundary.py
```

Expected review-branch result:

- `PASS = 127`
- `FAIL = 0`
- `SUPPORT = 64`
