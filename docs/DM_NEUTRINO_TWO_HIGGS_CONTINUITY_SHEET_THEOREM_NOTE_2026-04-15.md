# DM Neutrino Two-Higgs Continuity Sheet Theorem

**Date:** 2026-04-15  
**Status:** exact DM-side sheet-fixing theorem on the circulant two-Higgs
subcone  
**Script:** `scripts/frontier_dm_neutrino_two_higgs_continuity_sheet_theorem.py`

## Question

Once the DM odd-circulant right-Gram target lands on the canonical local
two-Higgs neutrino lane, does the residual local `x <-> y` sheet remain
physically open?

## Bottom line

No, not on the DM lane.

The earlier two-Higgs right-Gram bridge theorem already proved that on the
CP-admissible circulant subcone `d >= 2 r`, the realization is forced onto the
symmetric local slice

- `x_1 = x_2 = x_3 = x`
- `y_1 = y_2 = y_3 = y`

with

- `d = x^2 + y^2`
- `r = x y`

So the only remaining local ambiguity is the swap

`(x,y) <-> (y,x)`.

But the retained DM branch already has one exact local anchor: the universal
Dirac bridge `Y = y_0 I`.

On the two symmetric sheets:

```text
x_+^2 = (d + sqrt(d^2 - 4 r^2))/2
y_+^2 = (d - sqrt(d^2 - 4 r^2))/2

x_- = y_+
y_- = x_+
```

As `r -> 0` with `d > 0` fixed:

- the `+` sheet tends to `sqrt(d) I`
- the `-` sheet tends to a pure cycle-supported monomial class

So continuity to the retained universal bridge picks the `+` sheet uniquely.

## Inputs

This theorem combines:

- the DM two-Higgs right-Gram bridge theorem
- the retained universal Dirac bridge on the DM denominator lane

The point is to remove the residual local sheet ambiguity without importing an
extra admitted PMNS-side right-Gram scalar.

## Exact two-sheet law

On the circulant target

`K_can(d,r,delta)`,

the symmetric two-Higgs realization gives

- `d = x^2 + y^2`
- `r = x y`

Therefore the roots are

```text
x^2, y^2 = (d +- sqrt(d^2 - 4 r^2))/2
```

so the local ambiguity is exactly the swap `x <-> y`.

There is no larger residual family left on this DM subcone.

## Why continuity fixes the sheet

At vanishing deformation `r -> 0`, the DM lane already has the retained local
identity-supported bridge `Y = y_0 I`.

The two symmetric sheets behave differently:

- `x_+ -> sqrt(d)`, `y_+ -> 0`
- `x_- -> 0`, `y_- -> sqrt(d)`

So only the `+` sheet is continuous to the retained universal bridge.

The swapped sheet instead approaches a pure cycle-supported monomial limit,
which is not the retained DM identity-supported bridge.

## Theorem-level statement

**Theorem (DM continuity fixes the residual two-Higgs sheet on the circulant
subcone).** Assume the exact DM two-Higgs right-Gram bridge and the retained
universal Dirac bridge `Y = y_0 I`. Then on the CP-admissible circulant
subcone `d >= 2 r`:

1. the canonical local two-Higgs realization is forced onto the symmetric slice
2. the residual ambiguity is exactly the swap `x <-> y`
3. only the sheet with
   `x^2 = (d + sqrt(d^2 - 4 r^2))/2`,
   `y^2 = (d - sqrt(d^2 - 4 r^2))/2`
   tends continuously to the retained universal bridge as `r -> 0`

Therefore the DM lane fixes the residual local two-Higgs sheet intrinsically by
continuity to the retained universal bridge.

## What this closes

This closes the second live DM-side local ambiguity on the circulant route.

The branch no longer needs to say:

- "the sheet is still open"
- "we still need an admitted right-Gram modulus just to pick the two-Higgs
  sheet"

on this DM circulant subcone.

## What this does not close

This note does **not** derive:

- the two-Higgs extension from the bare axiom
- the values of `d`, `r`, or `delta`
- the odd-circulant coefficient law itself

So it does not close the whole denominator. It closes the local sheet.

## Safe wording

**Can claim**

- on the DM circulant subcone, the local two-Higgs sheet is fixed by continuity
  to the retained universal bridge
- the physical symmetric-sheet coefficients are explicit

**Cannot claim**

- the branch already derives the circulant subcone parameters from the bare
  axiom
- the whole two-Higgs local data law is fully closed

## Command

```bash
python3 scripts/frontier_dm_neutrino_two_higgs_continuity_sheet_theorem.py
```
