# Reproduction Audit Note

**Date:** 2026-04-04  
**Status:** skeptical-reader reproduction entry point

This note explains how to reproduce the current retained frontier without
mistaking exploratory drivers for canonical harnesses.

## Recommended entry point

Run:

[`scripts/reproduction_audit_harness.py`](/Users/jonreilly/Projects/Physics/scripts/reproduction_audit_harness.py)

Default behavior:

1. run the bounded canonical regression gate
2. run one bounded cross-family retained comparison
3. print a short canonical-vs-exploratory inventory

Optional:

- `--full-cross-family` adds the heavier 3D family sweep from the exploratory
  robustness lane

## What the harness actually checks

The default audit checks are intentionally modest:

- mirror / lattice / structured-bridge retained scripts still pass the cheap
  regression gate
- exact 2D mirror and structured chokepoint bridge still provide machine-clean
  Born-safe retained rows
- the two retained families are distinct but both still satisfy their own
  review-safe control logic

The default cross-family comparison is:

- exact 2D mirror validation
- structured chokepoint bridge

That is enough to tell a skeptical reader that the project is not a one-script
story, without turning the audit into a broad search.

## What it does not certify

This harness does **not** prove:

- the full physics program
- the `1/L^(d-1)` propagator fork as a theorem
- the continuum / RG bridge as complete
- the exploratory 3D/4D kernel claims as canonical
- the open dynamics problem as solved

Those need their own script / log / note chains and should be promoted only if
the evidence chain stays fixed on disk.

## Practical reading

Use this note together with:

- [`docs/CANONICAL_HARNESS_INDEX.md`](/Users/jonreilly/Projects/Physics/docs/CANONICAL_HARNESS_INDEX.md)
- [`docs/START_HERE.md`](/Users/jonreilly/Projects/Physics/docs/START_HERE.md)
- [`docs/LEGACY_EXPLORATORY_DRIVERS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LEGACY_EXPLORATORY_DRIVERS_NOTE.md)

The point is to make it obvious which scripts are retained harnesses and which
ones are still exploratory drivers.
