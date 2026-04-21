# Koide Loop Iteration 12 — Honest Revision of Iter 11 Near-TM1 Claim

**Date:** 2026-04-21 (iter 12)
**Type:** HONEST REVISION iteration (like earlier "unconditional closure" downgrade)
**Status:** Iter 11's "near-TM1 soft" physical interpretation WITHDRAWN
**Runner:** `scripts/frontier_koide_pmns_iter11_revision.py` (14/14 PASS)

---

## What was wrong with iter 11

Iter 11 claimed that V_conj is a "near-TM1" deformation of V_TBM based on:

> "Right-mult decomposition `R_right = V_TBM^T · V_conj` has axis 0.970
>  aligned with V_TBM col_1 = (2,-1,-1)/√6."

**This comparison was basis-confused.** 

- `R_right` is a rotation in the **mass basis** (its axis is a linear combination of ν_1, ν_2, ν_3).
- `V_TBM col_1 = (2,-1,-1)/√6` is a **flavor-basis** vector (expressing ν_1 in flavor coordinates).
- **Comparing these two is not physically meaningful** — they live in different basis spaces.

The 0.970 overlap was a **coincidental numerical alignment** with a specific
(not-natural) linear combination of mass basis vectors, not a physical
"near-TM1" structural claim.

## What's correct

The TRUE mass-basis analysis:

| Mass basis direction | Overlap with axis_mass |
|---|---|
| ν_1 (= (1,0,0) in mass basis) | **0.859** (86%) |
| ν_2 (= (0,1,0) in mass basis) | 0.480 (48%) |
| ν_3 (= (0,0,1) in mass basis) | 0.177 (18%) |

The rotation axis has **significant** components along all three mass basis
directions. It is NOT cleanly aligned with any single mass eigenstate.

## Revised numerical fit quality

**Best true-TM1 approximation** (rotation around mass-basis ν_1 = (1,0,0)
with best-fit angle): dist = **0.122** to V_conj.

**Comparison to other single-rotation best-fits**:

| Mechanism | Axis basis | Best dist | Gap reduction |
|---|---|---|---|
| Baseline (V_TBM vs V_conj) | — | 0.238 | 0% |
| Iter 5 (flavor single-rot) | flavor | 0.109 | 54% |
| **True mass-basis TM1** | mass, ν_1 axis | **0.122** | 49% |
| Iter 11 spurious ansatz | mixed (wrong) | 0.058 | 76% |

True mass-basis TM1 approximation is **similar quality** to iter 5's flavor
rotation (~50% gap reduction), NOT significantly better.

## What this iter 12 revision does

1. **Corrects** iter 11's physical interpretation.
2. **Preserves** iter 11's runner as a numerical-fit exercise (19/19 PASS
   technically valid; the physical claim is what's revised).
3. **Documents** the error pattern (basis confusion) for future iteration
   discipline.
4. **Restores** iter 5's conclusion: no clean single-rotation mechanism.

## Status update

| Gap | Post-iter-10 | Post-iter-11 (stale) | Post-iter-12 (correct) |
|---|---|---|---|
| I1 (Q=2/3) | RETAINED-FORCED | RETAINED-FORCED | RETAINED-FORCED |
| I2/P (δ=2/9) | RETAINED-FORCED | RETAINED-FORCED | RETAINED-FORCED |
| I5 mechanism | composite (iter 5) | "soft-TM1" (WRONG) | composite (restored) |

**Good news**: I1 and I2/P closure status is unaffected by this revision.

**Accurate I5 status**: mechanism is genuinely composite. No clean single
rotation in either flavor basis (iter 5) or mass basis (iter 12 correction)
decomposes iter 4 V_conj cleanly. Composite mechanism search continues.

## Discipline reflection

The pattern of error:
- Iter 11 computed a numerical overlap (0.969)
- Interpreted it physically as "near-TM1"
- Didn't rigorously check basis compatibility

This is similar to the earlier "unconditional closure" error corrected
in the pre-loop history. The loop's honesty discipline caught it within
one iteration — iter 12 catches iter 11's error.

This IS a kind of progress: demonstrating that the loop's self-correcting
discipline is working. A reviewer-quality review would have caught this
too, so better to catch it internally.

## Iter 13+ targets

**I5 mechanism attacks** (updated after iter 12 correction):

1. Return to composite-rotation search with CORRECT basis awareness.
   Specifically: parametrize R_right = exp(-θ · [combination of basis axes])
   in mass basis, with coefficients from (Q, δ).

2. Try the 86-48-18 axis structure directly — can this be written as
   a natural (Q, δ)-combination of (ν_1, ν_2, ν_3) mass axes?
   Guess: axis = (-√(3/4), +1/2, +1/6)/norm? or some (Q, δ) function?
   Actual components: (-0.859, 0.480, 0.177). Not obvious.

3. Pursue chirality-forced orientation (iter 8 follow-up) or quark-sector
   parallel as alternative entry points.
