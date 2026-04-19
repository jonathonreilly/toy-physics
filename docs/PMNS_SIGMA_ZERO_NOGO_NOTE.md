# PMNS Sigma-Zero No-Go

**Date:** 2026-04-16  
**Script:** `scripts/frontier_pmns_sigma_zero_no_go.py`

## Question
On the current pure-retained sole-axiom PMNS bank, can the retained native
sources, readouts, or selectors force nonzero `sigma`?

## Answer
No.

The exact remaining positive PMNS source had already been sharpened to the
native cycle/transport mean `sigma`, with nonzero `sigma` giving a concrete
route to nonzero `J_chi` on the `C_3`-covariant slice.

But on the current pure-retained bank:

- the free route has `sigma = 0`
- the canonical sole-axiom `hw=1` source/transfer route still has `sigma = 0`
- the retained scalar route has `sigma = 0`
- the only current native selector without an extra PMNS constraint surface,
  the unconstrained effective action on the canonical positive lift, is still
  minimized at the seed and so also stays at `sigma = 0`

Therefore the current pure-retained PMNS bank does **not** force nonzero
`sigma`.

## Exact Content

The theorem packages four exact points:

1. `sigma` is already a native PMNS observable: the cycle mean and transport
   mean agree exactly.
2. On the `C_3`-covariant fixed-`sigma` point, `J_chi = sigma`, so `sigma`
   is a genuine positive PMNS candidate source.
3. Every currently retained PMNS source route still lands at `sigma = 0`.
4. The current unconstrained native selector also stays at the seed rather
   than lifting `sigma` away from zero.

## Consequence

The PMNS retained lane is now closed more sharply than the earlier generic
value-selection no-go:

- the current pure-retained bank sets `sigma = 0`
- hence its retained PMNS current samples all have `J_chi = 0`
- any nonzero `sigma` requires a genuinely new pure-PMNS source law or a
  genuinely new admitted constraint surface beyond the current retained bank

## Verification

```bash
python3 scripts/frontier_pmns_sigma_zero_no_go.py
```
