# PMNS Oriented Cycle Selection Structure

**Date:** 2026-04-16  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_pmns_oriented_cycle_selection_structure.py`

## Question

Once the oriented forward cycle channel has an exact native observable/value
law, what exact selection structure remains on that channel?

## Answer

Three exact statements survive:

- exact `C_3` covariance collapses the cycle channel to one complex slot
  `sigma C`
- at the sole-axiom free point, `sigma = 0`, so the sole axiom selects only the
  trivial cycle law on that exact `C_3`-covariant locus
- on the graph-first selected-axis route, the residual antiunitary symmetry
  reduces the cycle channel to the `3`-real subfamily
  `c_1 = conjugate(c_3)`, `c_2 real`

So the carrier and observable law are closed, and the remaining gap is only a
value-selection law on that reduced channel.

## Exact chain

### 1. Exact `C_3` covariance

Write the oriented forward-cycle block as

`A_fwd = c_1 E_12 + c_2 E_23 + c_3 E_31`.

Conjugation by the projected cycle operator `C` permutes the coefficients
cyclically:

`(c_1, c_2, c_3) -> (c_2, c_3, c_1)`.

Therefore the exact `C_3`-fixed locus is

`c_1 = c_2 = c_3 = sigma`,

equivalently

`A_fwd = sigma C`.

### 2. Sole-axiom free point

At the sole-axiom free point, the active block is the identity block `I_3`.
Its oriented-cycle coefficients vanish exactly, so

`sigma = 0`.

Therefore the sole axiom by itself does not select a nontrivial cycle value on
the exact `C_3`-covariant locus.

### 3. Graph-first selected-axis route

On the graph-first route, the strongest exact residual antiunitary reduction on
the cycle channel is

`A_fwd = P_23 A_fwd^dagger P_23`.

Its fixed locus is

- `c_1 = conjugate(c_3)`
- `c_2` real

So the graph-first selected-axis route reduces the cycle channel from three
complex coefficients to three real parameters:

- `Re c_1`
- `Im c_1`
- `c_2`

## Consequence

This is not a full value-selection law. It does not yet derive the values from
`Cl(3)` on `Z^3` alone.

What it does prove is that the remaining positive target is no longer vague:

> any future nontrivial retained PMNS law must select values on the reduced
> oriented-cycle channel, and on the graph-first route that channel is already
> only `3` real dimensional.

## Boundary

This is a selection-structure theorem, not a closure theorem.

It closes:

- the exact `C_3`-covariant cycle slot
- the exact sole-axiom free-point value on that slot
- the exact graph-first residual symmetry reduction

It does **not** yet derive a nontrivial cycle-value selection law from the sole
axiom.

## Command

```bash
python3 scripts/frontier_pmns_oriented_cycle_selection_structure.py
```
