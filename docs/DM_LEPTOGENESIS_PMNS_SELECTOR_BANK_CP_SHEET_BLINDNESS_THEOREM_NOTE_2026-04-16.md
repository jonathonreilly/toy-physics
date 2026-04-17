# DM Leptogenesis PMNS Selector-Bank CP-Sheet Blindness Theorem

**Date:** 2026-04-16  
**Status:** exact negative theorem on the current PMNS-side selector-law bank  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_selector_bank_cp_sheet_blindness_theorem.py`

## Question

Do any of the current PMNS-side selector laws or positive closure candidates on
this branch already fix the constructive mainline CP sheet?

## Bottom line

No.

The current PMNS-side selector bank is already **transport-constructive** but
still **CP-sheet blind**.

The reason is structural:

1. every current PMNS-side selector objective on this branch is even under
   `delta -> -delta`
2. the baryogenesis source channel

   `gamma = x_1 y_3 sin(delta)`

   is odd under `delta -> -delta`
3. the interference channels `E1` and `E2` are even
4. therefore every current selected source or candidate comes with an equally
   selected opposite-CP partner

So none of the current PMNS-side selector laws yet gives a constructive
source-oriented mainline baryogenesis witness.

## What current laws are covered

This theorem covers the current PMNS-side selector bank on the branch:

- the minimum-information exact closure law
- the observable-relative-action exact closure law
- the transport-extremal overshooting source candidate
- the exact `eta = 1` continuity closure point generated from that candidate

## Exact consequences

### 1. The exact closure laws are CP-sheet blind

The minimum-information closure law and the observable-relative-action closure
law both reach exact `eta = 1` on the fixed native seed surface.

But in both cases:

- closure is unchanged under `delta -> -delta`
- the selector objective is unchanged under `delta -> -delta`
- `E1` and `E2` are unchanged
- `gamma`, `cp1`, and `cp2` flip sign

So their displayed representatives are not constructive CP witnesses. They are
only one member of an equally selected opposite-CP pair.

### 2. Even the positive transport-side overshoot/closure candidates are still CP-sheet blind

The transport-extremal candidate already overshoots:

- `eta/eta_obs = 1.0522203130495849`

and the exact continuity construction already gives a closure point with

- `eta/eta_obs = 1`.

So the PMNS side has already solved **transport existence** on the fixed native
seed surface.

But the same parity problem remains:

- the transport objective is unchanged under `delta -> -delta`
- the overshooting source has an equally transport-extremal opposite-CP partner
- the exact closure point has an equally selected opposite-CP partner

In the displayed representative, the exact closure point lands at

- `gamma < 0`
- `E1 > 0`
- `E2 < 0`

so its CP pair is

- `cp1 > 0`
- `cp2 > 0`

not the mainline source-oriented pattern `(-,+)`.

## What this closes

This closes the natural objection:

> didn’t the DM lane already construct closure candidates?

Yes, it did.

But those current selector laws and closure candidates do **not** yet close the
baryogenesis-side CP problem, because they do not fix the CP sheet.

So the remaining PMNS-side baryogenesis issue is no longer:

- existence of an off-seed source
- existence of `eta = 1` closure
- existence of `eta > 1` overshoot

It is specifically:

- a microscopic `D_- / dW_e^H` sign-law problem that must break the current
  `delta -> -delta` blindness and land on the constructive mainline sheet

## Consequence for the live target

The live PMNS comparator target is now sharp:

- derive a `D_- / dW_e^H` law that fixes the projected-source signs
  `gamma > 0`, `E1 > 0`, `E2 > 0`

or else

- prove that no such law exists on the current PMNS branch.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_selector_bank_cp_sheet_blindness_theorem.py
```
