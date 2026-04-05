# Source-Resolved Generated New Family V2 Note

**Date:** 2026-04-05  
**Status:** bounded bridge on the split-shell family, with a real but insufficient weak-field-law improvement over the first reopening

## Artifact chain

- [`scripts/source_resolved_generated_new_family_v2_probe.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_generated_new_family_v2_probe.py)
- [`logs/2026-04-05-source-resolved-generated-new-family-v2-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-generated-new-family-v2-probe.txt)

## Question

Does the broader-support split-shell family recover more of the weak-field
mass law if we remove the self-consistent source reweighting that may be
distorting the response?

This v2 probe stays narrow:

- retained compact bridge family as the baseline control
- the split-shell family from the first reopening
- static Green vs self-consistent wavefield vs fixed-weight wavefield
- exact zero-source reduction check
- detector effective support `N_eff`
- centroid sign counts and weak-field `F~M` fit

## Frozen result

Exact zero-source reduction survives all families and modes:

- `zero = 0.000e+00`

Aggregated over seeds `0..3`:

| family | mode | `TOWARD` | `F~M` | `N_eff` |
| --- | --- | ---: | ---: | ---: |
| bridge | static | `7/16` | `0.058` | `5.06` |
| bridge | wavefield | `6/16` | `0.098` | `5.14` |
| bridge | fixedwave | `5/16` | `0.230` | `4.94` |
| split-shell | static | `8/16` | `0.424` | `8.31` |
| split-shell | wavefield | `8/16` | `0.381` | `8.30` |
| split-shell | fixedwave | `8/16` | `0.500` | `8.26` |

## Safe read

The important result is that the broader-support family still helps, but not
enough to close the weak-field law:

- the split-shell geometry keeps the widened support from the first reopening
- the fixed-weight wavefield improves the law relative to the self-consistent
  wavefield on that same family
- the improvement is real, but it is still only partial:
  - split-shell `wavefield`: `F~M = 0.381`
  - split-shell `fixedwave`: `F~M = 0.500`
- that is better, but it is still far from the retained weak-field class
  and far from a clean Newtonian-style transfer

## Honest limitation

This is not generated-family closure.

- the weak-field mass law is still not cleanly linear
- the fixed-weight update helps, but the family remains bridge-level
- the split-shell geometry is broader, but the field rule still does not fully
  recover the retained weak-field behavior

## Branch verdict

Treat this as a **bounded bridge / partial improvement**, not a closure:

- the compact generated-family bridge remains closed
- the split-shell family is a genuinely different geometry rule
- the fixed-weight wavefield is the stronger law-first test
- it improves the weak-field fit relative to the self-consistent wavefield,
  but not enough to count as a full recovery

So the right read is:

- generated-family support widening is real
- removing the self-consistent source reweighting helps the law
- but the law is still too weak for generated-family closure

