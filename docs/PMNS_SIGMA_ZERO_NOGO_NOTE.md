# PMNS Sigma-Zero No-Go

**Status:** bounded - bounded or caveated result note
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

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [pmns_active_four_real_source_from_transport_note](PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md)
- [pmns_c3_nontrivial_current_boundary_note](PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md)
- [pmns_oriented_cycle_channel_value_law_note](PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md)
- [pmns_oriented_cycle_reduced_channel_nonselection_note](PMNS_ORIENTED_CYCLE_REDUCED_CHANNEL_NONSELECTION_NOTE.md)
- [pmns_sole_axiom_hw1_source_transfer_boundary_note](PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)
- [pmns_uniform_scalar_deformation_boundary_note](PMNS_UNIFORM_SCALAR_DEFORMATION_BOUNDARY_NOTE.md)
