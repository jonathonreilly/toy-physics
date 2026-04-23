# Planck-Scale Native Stop Conditions Audit

**Date:** 2026-04-23  
**Status:** branch-local failure-mode audit  
**Audit runner:** `scripts/frontier_planck_native_stop_conditions_audit.py`

## Question

What exactly would stop the direct Planck route from becoming genuinely native?

## Bottom line

The route now fails only if one of three things is denied.

### Stop condition 1

Deny that the exact time-locked factorized cell

`H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z`

is the right native primitive local object.

If this is denied, the whole direct state-law route loses its object.

### Stop condition 2

Deny that a **source-free** local state is the default state datum of the bare
primitive cell when no extra local preparation/source is supplied.

If this is denied, the state can remain an arbitrary unknown prepared state and
no unique source-free law follows.

### Stop condition 3

Deny that the default datum of the bare primitive cell must be free of hidden
presentation-dependent or information-bearing one-cell structure.

If this is denied, a nontracial hidden-datum state is still allowed.

## Consequence

If all three denials are rejected, the route closes:

`default source-free cell state = I_16/16`
`-> c_cell = Tr((I_16/16) P_A) = 1/4`
`-> a^2 = l_P^2`
`-> a = l_P`.

## Honest read

This means the route is now genuinely narrow.

It is no longer vulnerable to broad objections like:

- "the coefficient was guessed,"
- "the packet was arbitrary,"
- "the factor of 2 was imported,"
- "pressure was chosen by hand."

The only real remaining issue is whether the package wants to accept the
source-free default-datum semantics on the primitive cell.
