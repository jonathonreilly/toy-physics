# DM Neutrino Odd-Circulant Current-Stack Zero Law

**Date:** 2026-04-15  
**Status:** exact current-stack theorem on the last local DM coefficient slot  
**Script:** `scripts/frontier_dm_neutrino_odd_circulant_current_stack_zero_law.py`

## Question

Given the exact local odd-slot theorem on the DM circulant family, what
activation law does the stack currently retained today assign to that slot?

## Bottom line

The current-stack law is the zero law:

`c_odd,current = 0`.

The reason is structural.

The current local DM bank is built from residual-`Z_2`-even data:

- the exact weak-axis `1+2` split `diag(a,b,b)`
- the even circulant bridge it induces
- Hermitian/scalar/equivariant functionals of that same even data

Any residual-`Z_2`-equivariant functional of a residual-`Z_2`-even input is
again residual-`Z_2` even, so its projection onto the unique odd circulant slot
vanishes.

Therefore the exact present-tense local coefficient law on the retained stack
is not “unknown.” It is the zero law.

## Theorem-level statement

**Theorem (Current-stack zero law for the odd circulant coefficient).** Assume
the exact weak-axis `1+2` local split, the exact even circulant bridge it
induces, and the retained support/Hermitian/scalar DM bank built as
residual-`Z_2`-equivariant functionals of that even data. Then the unique odd
circulant coefficient on the DM Hermitian kernel obeys

`c_odd,current = 0`.

Therefore any future positive DM coefficient law must introduce a genuinely new
residual-`Z_2`-odd bridge or activator.

## What this closes

This closes the present-tense activation question on the current stack.

The branch no longer needs to say:

- “the odd coefficient might already be hiding in the current bank”
- “maybe one more scalar/Hermitian functional turns it on”

Those routes are closed on the current retained stack.

## What this does not close

This note does **not** prove that no future extension can realize
`c_odd != 0`.

It proves that the present retained stack does not.

## Command

```bash
python3 scripts/frontier_dm_neutrino_odd_circulant_current_stack_zero_law.py
```
