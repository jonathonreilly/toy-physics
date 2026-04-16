# PMNS Hidden Principle Attempt Note

**Date:** 2026-04-15  
**Status:** exact obstruction theorem for simple hidden-principle candidates  
**Script:** `scripts/frontier_pmns_hidden_principle_attempt.py`

## Question

The current exact bank has reduced the remaining PMNS gap to three named
objects:

- the branch Hermitian-data law itself
- the breaking triplet `(delta, rho, gamma)`
- the restricted Higgs-offset selector on the canonical `(0,1)` seed pair

Is there one simple hidden principle, stationarity law, minimality law, or
continuity law that forces them from the retained bank?

## Bottom line

No simple principle of that kind closes the gap.

The tested exact candidates all fail in the same way:

- weak-axis continuation gives two continuous sheets, not a unique selector
- minimal source norm selects the zero amplitude, not a positive bridge
- residual-symmetry selection annihilates the breaking triplet instead of
  deriving it
- edge continuity distinguishes the monomial boundary but does not choose the
  edge bit
- any principle built only from `H` or from right-conjugacy-invariant data of
  `K = Y^dag Y` remains blind to the residual sheet

So the current bank does **not** hide a one-line stationarity/minimality law
that would force the missing objects.

## Exact candidate tests

### 1. Weak-axis continuation

On the compatible weak-axis seed patch, the canonical active coefficients
have two continuous sheets:

- `Y_+ = x_+ I + y_+ C`
- `Y_- = y_+ I + x_+ C`

At `A = B`, these limit to the two monomial edges

- `sqrt(A) I`
- `sqrt(A) C`

So continuation exists, but it is two-sheeted. Continuity alone does not pick
the sheet.

### 2. Minimal source norm

On the reduced selector class

`S_cls = chi_N_nu - chi_N_e`,

the smallest exact amplitude norm is `a_sel = 0`.

So a minimality principle on the retained bank picks the current zero law,
not a positive selector realization.

### 3. Residual-symmetry selection

The global active Hermitian law splits exactly as

`H = H_core + B(delta, rho, gamma)`.

Residual `P_23` symmetry selects the aligned core by forcing

`delta = rho = gamma = 0`.

That is useful structure, but it does not derive nonzero breaking values.

### 4. Edge continuity

At the weak-axis boundary `A = B`, the two exact monomial edges are

- `sqrt(A) I`
- `sqrt(A) C`

They have the same Hermitian data and the same source norm, so continuity
does not select the Higgs-offset bit.

### 5. Mixed-bridge candidate

The smallest surviving positive object is still the exact one-dimensional
reduced bridge

`B_red = a_sel (chi_N_nu - chi_N_e)`.

That object is sector-odd, inter-sector, non-additive over the lepton direct
sum, and supported only on the non-universal locus.

This is the right shape for the missing principle, but the current retained
bank does not derive its amplitude or the branch Hermitian-data values.

## Strongest exact theorem

**Theorem (No simple hidden principle closes the current PMNS gap).** Assume
the exact weak-axis seed theorem, the exact seed coefficient-closure theorem,
the exact breaking-triplet package, the exact selector reductions, and the
exact right-conjugacy no-go results already on the branch. Then:

1. weak-axis continuation is two-sheeted and does not fix the selector
2. minimal source norm fixes the zero amplitude, not a positive bridge
3. residual symmetry fixes the aligned core but not the breaking values
4. edge continuity identifies the monomial boundary but not the offset bit
5. any principle depending only on `H` or on right-conjugacy-invariant data
   of `K = Y^dag Y` remains blind to the residual sheet

Therefore the current bank does not contain a simple hidden
stationarity/minimality law that forces the missing PMNS objects.

The minimal surviving positive completion must be a genuinely new
non-additive, sector-sensitive mixed bridge supported only on the
non-universal locus, with one real reduced amplitude slot on
`chi_N_nu - chi_N_e`.

For the Hermitian side, the corresponding minimal bridge class is the exact
`2 + 2 + 3` package

`(A, B, u, v, delta, rho, gamma)`.

## What this closes

This closes the search for a simple hidden-principle shortcut.

It is now exact that:

- the missing objects are not forced by a simple continuation law
- the missing objects are not forced by a source-norm minimization law
- the missing objects are not forced by residual symmetry alone
- the missing objects are not forced by edge continuity alone

## What this does not close

This note does **not** derive the missing objects positively.

It only characterizes the shape any successful principle must have:

- sector-odd
- inter-sector
- non-additive
- supported only on the non-universal locus
- one real reduced amplitude slot for the selector
- `2 + 2 + 3` Hermitian bridge structure for the branch data

## Command

```bash
python3 scripts/frontier_pmns_hidden_principle_attempt.py
```
