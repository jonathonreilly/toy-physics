# Simple Nonlinear Same-Source Metric Closure Does Not Remove the Strong-Field Residual

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_same_source_metric_ansatz_scan.py`  
**Status:** Bounded negative result; not a GR closure

## Purpose

After the exact local `O_h` source-class scan, one cheap remaining excuse was:

> maybe the metric only fails because the direct closure
> `psi = 1 + phi`, `alpha psi = 1 - phi`
> is too rigid, and a small nonlinear same-source correction would close it

This note tests that directly.

## Ansatz family

Keep the same exact lattice field `phi(x)` and the same weak-field linear
limit, but allow the simplest quadratic strong-field deformation:

- `psi(phi) = 1 + phi + a_2 phi^2`
- `alpha psi(phi) = 1 - phi + b_2 phi^2`

This preserves the retained weak-field surface while letting the strong-field
closure move in the simplest nonlinear way.

## What the script finds

Using the best exact local `O_h` source law from
`OH_SOURCE_CLASS_NOTE.md`:

- baseline direct same-source residual:

  `max |G_{mu nu}| = 2.978e-2`

- best quadratic same-source residual over `121` admissible `(a_2, b_2)`
  choices:

  `max |G_{mu nu}| = 2.852e-2`

- best point in the scan:
  - `a_2 = 1.0`
  - `b_2 = -1.0`

So the quadratic same-source deformation improves the residual only
slightly, by about `4%`.

## Interpretation

This is a useful bounded negative result:

- the remaining strong-field gap is **not** just the too-rigid linear
  direct closure
- a simple nonlinear reparameterization of the same exact field does not
  drive the candidate anywhere near vacuum closure

So the live blocker is deeper than a low-order ansatz tweak. It is more likely
to be one of:

1. a missing near-source matching theorem
2. a missing coarse-grained / effective physical source law
3. the need for a genuinely different nonlinear exterior metric law

## What this closes

This closes another weak escape route:

> “maybe a small quadratic same-source correction already fixes the strong-field metric”

It does not.

## What this does not close

This note does **not** close:

1. the theorem-grade spacetime metric
2. the nonlinear vacuum field equation
3. full nonlinear GR

## Practical next step

The next gravity move should therefore not be:

- another tiny same-source ansatz tweak

It should instead be:

1. derive a stronger effective source law / coarse-graining statement
2. or derive the correct nonlinear exterior metric law from the exact
   harmonic field itself
