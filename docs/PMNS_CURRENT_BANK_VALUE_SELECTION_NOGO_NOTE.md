# PMNS Current Bank Value-Selection No-Go

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Script:** `scripts/frontier_pmns_current_bank_value_selection_nogo.py`

## Question
Does the current exact bank contain a positive value-selection law for the
retained PMNS lane?

## Answer
No.

The current exact bank now closes the retained PMNS lane negatively:

- the sole axiom `Cl(3)` on `Z^3` gives only the trivial free lower-level
  response profiles on the retained lepton triplets
- the retained scalar deformation routes stay diagonal/scalar and are rejected
  by the one-sided PMNS closure stack
- the only surviving positive carrier is the graph-first reduced oriented
  forward-cycle channel
- that reduced channel has an exact native observable law
- every point of that reduced channel is realized exactly on the lower-level
  active response chain

Therefore the current exact bank does **not** contain a positive
value-selection law on that reduced channel.

## Exact Content

Let

\[
A_{\mathrm{fwd}}(u,v,w)
= (u + i v) E_{12} + w E_{23} + (u - i v) E_{31}.
\]

The current exact bank proves:

1. The sole axiom gives only the trivial free response profiles.
2. The retained local scalar routes never leave the diagonal/scalar sector.
3. The graph-first selected-axis route reduces the surviving positive carrier
   to the reduced `3`-real oriented-cycle family above.
4. The native oriented-cycle observable law reads `(u,v,w)` exactly.
5. Every point of that reduced family is realized on the lower-level active
   response chain.

So the current exact bank fixes:

- the carrier,
- the observable law,
- and the exact residual symmetry,

but not a unique value.

## Consequence

The retained PMNS lane is now closed at the current-bank boundary.

Any further positive value-selection law would require:

- genuinely new dynamics, or
- a further admitted extension.

## Verification

```bash
python3 scripts/frontier_pmns_current_bank_value_selection_nogo.py
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [pmns_lower_level_end_to_end_closure_note](PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md)
- [pmns_oriented_cycle_channel_value_law_note](PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md)
- [pmns_oriented_cycle_reduced_channel_nonselection_note](PMNS_ORIENTED_CYCLE_REDUCED_CHANNEL_NONSELECTION_NOTE.md)
- [pmns_uniform_scalar_deformation_boundary_note](PMNS_UNIFORM_SCALAR_DEFORMATION_BOUNDARY_NOTE.md)
