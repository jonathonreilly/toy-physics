# Legacy Exploratory Drivers

**Date:** 2026-04-04  
**Status:** support - structural or confirmatory support note

This note exists so a new reader does not mistake older exploratory scripts
for the retained physics harnesses.

## Canonical entry points

Use these first:

- [`docs/START_HERE.md`](/Users/jonreilly/Projects/Physics/docs/START_HERE.md)
- [`docs/UNIFIED_PROGRAM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/UNIFIED_PROGRAM_NOTE.md)
- [`README.md`](/Users/jonreilly/Projects/Physics/README.md)

## Legacy exploratory drivers

These files are still useful as historical experiments, but they are not the
canonical retained harnesses:

- [`scripts/causal_field_full_test.py`](/Users/jonreilly/Projects/Physics/scripts/causal_field_full_test.py)
- [`scripts/continuum_limit_test.py`](/Users/jonreilly/Projects/Physics/scripts/continuum_limit_test.py)
- [`scripts/lorentz_symmetry_test.py`](/Users/jonreilly/Projects/Physics/scripts/lorentz_symmetry_test.py)
- [`scripts/three_d_joint_test.py`](/Users/jonreilly/Projects/Physics/scripts/three_d_joint_test.py)

## Read this way

- `*_test.py` in this area means “experiment driver,” not “current regression
  harness.”
- These scripts may still contain interesting historical prints, but the
  retained project state is described by the canonical notes linked from
  `START_HERE`.
- If a claim only appears in one of these drivers and not in a retained
  script/log/note chain, treat it as exploratory.
