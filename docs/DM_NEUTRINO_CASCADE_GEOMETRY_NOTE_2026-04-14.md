# DM Neutrino Cascade Geometry Note

**Date:** 2026-04-14  
**Branch:** `codex/dm-across-the-line`  
**Script:** `scripts/frontier_dm_neutrino_cascade_geometry.py`

---

## Status

**EXACT operator geometry / BOUNDED physics interpretation**

This note isolates the exact weak-axis Clifford geometry behind the newer
neutrino-Yukawa candidate story.

The clean exact result is:

1. the weak-axis Yukawa insertion `Gamma_1` does **not** act inside `T_1`
2. at one hop, it splits `T_1` into:
   - one singlet channel `O_0`
   - one residual two-state channel into `T_2`
3. at second order, the return operator on `T_1` decomposes exactly as

   `diag(1,0,0)` from `O_0` plus `diag(0,1,1)` from `T_2`

So the branch now has exact operator support for the statement that the
weak-axis insertion naturally creates a `1 + 2` cascade surface.

---

## Exact Matrices

In the site basis

- `T_1 = {(1,0,0), (0,1,0), (0,0,1)}`
- `T_2 = {(1,1,0), (1,0,1), (0,1,1)}`
- `O_0 = {(0,0,0)}`

the weak-direction Clifford generator satisfies:

- `P_T1 Gamma_1 P_T1 = 0`
- `P_O0 Gamma_1 P_T1 = [1 0 0]`
- `P_T2 Gamma_1 P_T1` has rank `2`

and the second-order return operators are exactly:

- via `O_0`: `diag(1,0,0)`
- via `T_2`: `diag(0,1,1)`
- total: `I_3`

That is a much cleaner operator statement than the old heuristic
"one state couples directly, two couple radiatively."

---

## Why This Matters For The Neutrino Blocker

This exact geometry does **not** derive the neutrino Dirac Yukawa. What it does
show is that the second-order cascade candidate is not arbitrary.

There is now a precise operator reason to focus on a second-order surface:

- one hop does not close inside `T_1`
- the first exact closed return structure is second order
- that second-order structure is already split into a `1 + 2` pattern

This is the best exact operator support currently available for the bounded
claim that the neutrino Yukawa might arise from a second-order EWSB cascade.

---

## Why This Still Falls Short Of A Theorem

Three physics steps remain open:

1. connect this `C^8` weak-axis geometry to the full `C^16` chiral/right-handed
   neutrino embedding
2. identify which operator chain actually generates the physical Dirac Yukawa
3. fix the neutrino-sector base normalization

Until those steps are derived, the correct claim remains:

> exact operator geometry supports the second-order cascade as the right place
> to look, but the neutrino Yukawa theorem itself is still open.
