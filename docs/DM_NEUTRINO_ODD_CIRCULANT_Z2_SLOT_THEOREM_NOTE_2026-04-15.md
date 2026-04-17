# DM Neutrino Odd-Circulant Residual-`Z_2` Slot Theorem

**Date:** 2026-04-15  
**Status:** exact local structural theorem on the DM circulant coefficient space  
**Script:** `scripts/frontier_dm_neutrino_odd_circulant_z2_slot_theorem.py`

## Question

On the DM Hermitian circulant right-Gram family, what exact local coefficient
slot carries the CP-supporting deformation?

## Bottom line

There is exactly one residual-`Z_2`-odd slot.

Writing the Hermitian circulant kernel as

`K = d I + c_even (S + S^2) + i c_odd (S - S^2)`,

the exchange `P_23` swaps `S <-> S^2`, leaves `I` and `S + S^2` invariant, and
flips the sign of `i(S - S^2)`. So:

- `d` is residual-`Z_2` even
- `c_even` is residual-`Z_2` even
- `c_odd` is residual-`Z_2` odd

Moreover, the standard leptogenesis CP kernel on this family is

`Im[(K_01)^2] = 2 c_even c_odd`,

so `c_odd` is exactly the local slot that must be activated away from zero.

## Exact weak-axis input

The exact weak-axis `1+2` split already gives a positive local result:

- the bridged local Dirac surface fills the even circulant slot
- its Hermitian kernel has `c_odd = 0` exactly

So the branch now knows something sharper than “some CP phase is missing.”
It knows the exact local slot that is missing.

## Theorem-level statement

**Theorem (Unique residual-`Z_2`-odd slot on the DM Hermitian circulant
family).** On the Hermitian circulant family

`K = d I + c_even (S + S^2) + i c_odd (S - S^2)`,

with `P_23 S P_23 = S^2`, the coefficient `c_odd` is the unique
residual-`Z_2`-odd local slot. The standard leptogenesis CP tensor on this
family is proportional to `c_even c_odd`. The exact weak-axis `1+2` bridge
fills only the even slot and gives `c_odd = 0`.

Therefore the remaining local coefficient problem on the DM denominator lane is
exactly the activation law for one residual-`Z_2`-odd slot.

## What this closes

This closes the last vague part of the local coefficient space.

The branch no longer needs to say:

- “some phase-like thing is missing”
- “some generic flavor coefficient is missing”

The missing local object is now exact: the odd circulant coefficient `c_odd`.

## What this does not close

This note does **not** derive a nonzero activation law for `c_odd`.

It identifies the slot exactly, but it does not yet turn it on.

## Command

```bash
python3 scripts/frontier_dm_neutrino_odd_circulant_z2_slot_theorem.py
```

