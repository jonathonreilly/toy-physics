# Broken-Graph Action-Power Robustness Note

**Date:** 2026-04-04  
**Status:** bounded graph-damage replay on the retained 3D ordered-lattice
family

## Artifact chain

- Script: [`scripts/broken_graph_action_power_robustness.py`](/Users/jonreilly/Projects/Physics/scripts/broken_graph_action_power_robustness.py)
- Log: [`logs/2026-04-04-broken-graph-action-power-robustness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-broken-graph-action-power-robustness.txt)

This note tests a narrow claim:

- under bounded graph damage, is the weak-field-linear phase valley
  (`p = 1`) structurally more robust than neighboring action powers?

The retained family is the same 3D ordered-lattice valley-linear setup used by
the other bounded action probes:

- `h = 0.5`
- `W = 8`
- `L = 12`
- kernel `1/L^2` with `h^2` measure

The damage ladder is intentionally small:

- baseline
- 30% offset deletion
- 50% offset deletion
- 70% offset deletion
- asymmetric connectivity
- jittered positions at `0.5h`
- sparse NN connectivity

The action powers compared are:

- `p = 0.5`
- `p = 1.0`
- `p = 2.0`

## Frozen result

Frozen result is recorded in the log file linked above.

The frozen rows say:

- baseline: all three actions stay TOWARD and Born is machine-clean
- 30% deletion: all three actions still stay TOWARD
- 50% and 70% deletion: `p = 0.5` and `p = 1.0` flip AWAY on the fixed probe,
  while `p = 2.0` stays marginally TOWARD
- asymmetric connectivity: the same split persists
- jittered positions at `0.5h`: all three actions remain TOWARD
- sparse NN connectivity: all three actions remain TOWARD, but the Born
  control becomes too thin to read as a strong universal positive

The summary row is the key comparison:

- `p = 0.5`: TOWARD on `3/6` damaged cases, mean `|F~M - p| = 0.004`
- `p = 1.0`: TOWARD on `3/6` damaged cases, mean `|F~M - p| = 0.000`
- `p = 2.0`: TOWARD on `5/6` damaged cases, mean `|F~M - p| = 0.057`

## Safe interpretation

The honest interpretation is:

- the bounded damage ladder does **not** crown `p = 1` as the most robust
  action power on this family
- `p = 1` is the cleanest on the exponent side when it survives, but `p = 2`
  survives more of the signed damage ladder
- so the stronger robustness claim weakens on this family
- what remains is a bounded statement that graph damage mostly changes
  retention and precision, not the existence of the phase-mediated effect

This note is intentionally narrower than the earlier inverse-problem memo:

- it does not claim a universal graph theorem
- it does not claim all graphs give the same physics
- it only tests a bounded robustness ordering on one retained family

## Relation to the inverse-problem note

Read this with:

- [`docs/INVERSE_PROBLEM_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/INVERSE_PROBLEM_NOTE.md)
- [`docs/ACTION_UNIQUENESS_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ACTION_UNIQUENESS_NOTE.md)
- [`docs/ACTION_POWER_SCALING_SWEEP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/ACTION_POWER_SCALING_SWEEP_NOTE.md)

The inverse-problem note asks whether the graph is necessary for gravity to
exist.
This note asks whether `p = 1` is the most robust force law once the graph is
damaged.

Those are related but not identical questions.

## Best next move

- keep the inverse-problem claim as a precision/retention statement, not a
  structural uniqueness statement
- if we keep exploring, the next move should be a different graph family or a
  more explicit perturbation model, not another attempt to promote `p = 1` as
  the uniquely robust answer on this retained family
