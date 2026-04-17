# PMNS Selector Unique Amplitude Slot

**Date:** 2026-04-15  
**Status:** exact reduced-form theorem on the microscopic bridge amplitude
slot  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_selector_unique_amplitude_slot.py`

## Question

Once the reduced PMNS selector class is unique up to scale, what microscopic
datum still remains to be derived at the reduced class quotient?

## Bottom line

Exactly one real amplitude slot remains.

Let

`S_cls = chi_N_nu - chi_N_e`

be the unique reduced selector class on the branch-class quotient

`X_red = {U_1, U_2, N_nu, N_e}`.

Then any future microscopic realization, after reduction to `X_red`, has the
form

`B_red = a_sel S_cls`

for one real amplitude

`a_sel in R`.

So the microscopic realization problem is no longer a family-search over
reduced selector classes. It is the activation law for one real amplitude.

## Atlas and package inputs

This theorem reuses:

- `PMNS selector class-space uniqueness`

And, as structural framing from the Majorana lane:

- `Majorana unique source slot`

That import is not a dynamics import. It is a safe structural reuse: once the
admissible reduced class space is one-dimensional, the remaining microscopic
unknown is one amplitude coordinate on that class.

## Why this is stronger than class-space uniqueness

The class-space uniqueness theorem says the reduced selector class is unique up
to scale.

This note goes one step further. It translates that uniqueness into the exact
microscopic reduced-form statement:

- one reduced selector class
- one real amplitude slot on that class

So the remaining bridge question is not “which reduced selector shape?” It is
“what turns on `a_sel`?”

## Theorem-level statement

**Theorem (Unique reduced amplitude slot for the PMNS selector bridge).**
Assume the exact PMNS selector class-space uniqueness theorem. Then every
future microscopic bridge functional, after reduction to the branch-class
quotient `X_red`, is of the form

`B_red = a_sel S_cls`

with

`S_cls = chi_N_nu - chi_N_e`

and one real scalar amplitude `a_sel`.

Therefore the reduced microscopic selector problem carries one real amplitude
slot and no further reduced class-level freedom.

## What this closes

This closes the reduced-form microscopic bookkeeping.

It is now exact that the remaining bridge problem is not:

- a search over multiple reduced selector classes
- a search over multiple reduced selector amplitudes
- a search over reduced selector phases

It is one real amplitude law on one unique reduced class.

## What this does not close

This note does **not** prove:

- that the microscopic bridge exists
- that `a_sel` is nonzero
- that the current retained stack already realizes it
- which microscopic observable grammar carries that amplitude

It is a reduced-form theorem only.

## Command

```bash
python3 scripts/frontier_pmns_selector_unique_amplitude_slot.py
```
