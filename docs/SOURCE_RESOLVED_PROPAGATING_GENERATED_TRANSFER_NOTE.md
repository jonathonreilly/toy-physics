# Source-Resolved Propagating Generated Transfer Note

**Status:** bounded - bounded or caveated result note
This note freezes the generated-family test of the propagating Green pocket.

## Files

- [`scripts/source_resolved_propagating_generated_transfer.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_propagating_generated_transfer.py)
- [`logs/2026-04-05-source-resolved-propagating-generated-transfer.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-resolved-propagating-generated-transfer.txt)

## Question

Does the exact-lattice propagating Green pocket transfer one step to the retained
compact generated DAG family without tuning the family broadly?

## Gates

The transfer is only interesting if all of the following hold:

- exact zero-source reduction
- all-TOWARD on the weak-field ladder
- `F~M` in `[0.95, 1.05]`
- nontrivial amplitude relative to the instantaneous comparator

## Result

The generated-family propagating transfer fails the hard gates:

- exact zero-source reduction survives exactly
- the weak-field ladder is `0/4` TOWARD
- the fitted propagating exponent is `0.33`
- the instantaneous comparator is also not close to linear, with exponent `0.43`
- the mean `|prop/inst|` ratio is `2.119`

The propagating causal-memory step therefore does **not** rescue the generated
family. It is a sharper no-go than the static generated-family negative because
the exact zero-source reduction survives while the sign is still wrong on every
retained row.

## Bounded read

On this retained generated family, the propagating Green architecture is a
bounded negative:

- exact reduction is fine
- weak-field sign does not transfer
- linear mass scaling does not recover
- causal memory increases the mismatch rather than fixing it

This stays aligned with the broader generated-family conclusion: the exact
lattice supports the Green pocket, but the retained generated DAG family still
does not.
