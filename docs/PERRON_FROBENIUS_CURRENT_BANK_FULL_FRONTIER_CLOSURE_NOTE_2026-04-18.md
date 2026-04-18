# Perron-Frobenius Current-Bank Full Frontier Closure

**Date:** 2026-04-18  
**Status:** exact science-only theorem that all three current-bank PF frontier
certificates are now negatively closed on the present exact bank  
**Script:** `scripts/frontier_perron_frobenius_current_bank_full_frontier_closure_2026_04_18.py`

## Question

After the Wilson lane has been completely closed on the current bank at the
sharpest local `1 + 1` level, what is the exact branch-wide current-bank
status of the three frontier certificates?

## Answer

All three frontier certificates are now negatively closed on the current bank:

1. **Wilson**:
   the sharpest current Wilson reopening route is one local nilpotent-chain
   `1 + 1` certificate, and the current bank still does **not** realize even
   the first generator layer;
2. **PMNS-native**:
   the sharpest current PMNS-native route is one fixed-slice scalar production
   discriminant, and the current bank still forces that scalar to vanish;
3. **Plaquette non-Wilson**:
   the sharpest current first-layer plaquette route is one first Hankel + `K`
   certificate, and the current bank already fails at that first Hankel layer.

Therefore the present exact bank has no remaining positive PF route left open.

That is a current-bank closure theorem, not an impossibility theorem against
future strengthening.

## Setup

From
[PERRON_FROBENIUS_WILSON_CURRENT_BANK_COMPLETE_CLOSURE_NOTE_2026-04-18.md](./PERRON_FROBENIUS_WILSON_CURRENT_BANK_COMPLETE_CLOSURE_NOTE_2026-04-18.md):

- the Wilson lane is completely closed on the current bank.

From
[PMNS_GRAPH_FIRST_FIXED_SLICE_SCALAR_PRODUCTION_DISCRIMINANT_NOTE_2026-04-18.md](./PMNS_GRAPH_FIRST_FIXED_SLICE_SCALAR_PRODUCTION_DISCRIMINANT_NOTE_2026-04-18.md):

- the PMNS-native lane is now one scalar production-discriminant certificate,
  and the current bank still does **not** realize it.

From
[GAUGE_VACUUM_PLAQUETTE_BETA6_FIRST_HANKEL_CERTIFICATE_NOTE_2026-04-18.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_FIRST_HANKEL_CERTIFICATE_NOTE_2026-04-18.md):

- the plaquette first constructive blocker is now one first Hankel + `K`
  certificate,
  and the current bank already fails there.

## Theorem 1: all three current-bank frontier certificates are negatively closed

Assume the three exact current-bank frontier closure/boundary theorems above.

Then:

1. the Wilson frontier is closed negatively on the current bank;
2. the PMNS-native frontier is closed negatively on the current bank;
3. the plaquette first-layer non-Wilson frontier is closed negatively on the
   current bank.

Therefore the present exact bank has no live positive PF route remaining.

## Corollary 1: current-bank global PF is fully closed negatively

Because all three current-bank frontier certificates are negatively closed, the
current bank is fully closed negatively for a positive global sole-axiom PF
selector theorem.

## Corollary 2: future reopening now requires genuinely new science on at least one frontier

Any future positive reopening must therefore come from genuinely new input on
at least one frontier:

- stronger Wilson constructive science,
- stronger PMNS-native production science,
- or stronger plaquette operator-side science.

## What this closes

- exact branch-wide current-bank closure at the sharpest current frontier level
- exact statement that no positive PF route remains open on the present bank

## What this does not close

- an impossibility theorem against future strengthening
- a positive global PF selector from a stronger future bank

## Why this matters

This is the strongest honest current-bank reading now available on the branch.

The branch can now distinguish sharply between:

- **current-bank status**: fully closed negatively;
- **future-theory status**: Wilson remains the main plausible reopening lever
  under stronger science.

## Command

```bash
python3 scripts/frontier_perron_frobenius_current_bank_full_frontier_closure_2026_04_18.py
```
