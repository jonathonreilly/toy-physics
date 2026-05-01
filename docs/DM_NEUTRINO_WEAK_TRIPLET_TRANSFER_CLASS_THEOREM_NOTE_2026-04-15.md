# DM Neutrino Weak-Triplet Transfer-Class Theorem

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_neutrino_weak_triplet_transfer_class_theorem.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

Once the current exact source-side data are reduced to:

- one selector amplitude slot `a_sel`
- one two-channel weak tensor-slot pair `(tau_E, tau_T)`

what is the exact remaining transfer class into the DM triplet endpoint

- odd source `gamma`
- even responses `E1 = delta + rho`, `E2 = A + b - c - d`?

## Bottom line

The transfer class is no longer vague.

Any linear transfer law compatible with the exact odd/even source-target split
is forced into block form:

- `gamma = c_odd a_sel`
- `[E1, E2]^T = M_even [tau_E, tau_T]^T`

with:

- one real odd coefficient `c_odd`
- one real `2 x 2` even response matrix `M_even`

So the missing DM law is no longer an arbitrary `3 x 3` cross-sector map. It
is a `1 + 4` coefficient problem.

## Exact source bundle

The current stack already supplies the right-dimensional source data:

- the neutrino selector lane gives one exact real amplitude slot `a_sel`
- the strong-CP / CKM tensor-slot lane gives one exact two-channel weak tensor
  carrier

The theorem does not need the final microscopic realization of the tensor pair.
It only uses the exact fact that the current weak-side source bundle is a
`1 + 2` package.

## Exact target bundle

The DM branch already fixed the target decomposition:

- odd slot: `gamma`
- even pair: `E1 = delta + rho`, `E2 = A + b - c - d`

So the target is also a `1 + 2` package.

## Transfer-class statement

Let the source involution act as:

- `a_sel -> -a_sel`
- `(tau_E, tau_T)` fixed

and let the target involution act as:

- `gamma -> -gamma`
- `(E1, E2)` fixed

Then any linear transfer map intertwining these involutions is exactly of the
form

`L = [[c_odd, 0, 0], [0, m_11, m_12], [0, m_21, m_22]]`.

Equivalently:

- `gamma = c_odd a_sel`
- `E1 = m_11 tau_E + m_12 tau_T`
- `E2 = m_21 tau_E + m_22 tau_T`

No cross-parity terms survive.

## Why this matters

This closes the transfer-class question.

The branch no longer has to say only:

- “some cross-sector law must populate `(gamma,E1,E2)`”

It can now say exactly:

- the odd triplet source must come from the single selector amplitude leg
- the even response pair must come from the two-channel weak tensor leg
- the downstream coefficient problem splits cleanly into an odd normalization
  leg and an even response leg

So the remaining denominator gap is no longer “invent the transfer map.”
It is “derive the transfer coefficients on this exact `1 + 2 -> 1 + 2`
bundle.”

## What this does not close

This note does **not** derive:

- the value of `c_odd` itself inside this note
- the entries of `M_even`
- the microscopic tensor realization `(tau_E, tau_T)` on the neutrino branch

So this is an exact transfer-class theorem, not full coefficient closure.
The downstream odd-normalization theorem now closes `c_odd`; the live
remaining coefficient blocker is `M_even`.

## Command

```bash
python3 scripts/frontier_dm_neutrino_weak_triplet_transfer_class_theorem.py
```
