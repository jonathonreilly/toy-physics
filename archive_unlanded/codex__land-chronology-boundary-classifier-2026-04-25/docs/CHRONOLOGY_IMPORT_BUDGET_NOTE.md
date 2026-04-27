# Chronology Import Budget Note

**Date:** 2026-04-25
**Status:** import classifier companion; counted/weighted budget only
**Companions:**
[CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md](CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md),
[CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md](CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md)

## Role

This note turns the chronology import classifier into a small counted and
weighted budget. The budget is a bookkeeping device for review. It is not a
proof against every logically definable theory with closed timelike curves,
postselection, advanced boundary conditions, multi-time constraints, or exact
Loschmidt reversals.

The retained zero-budget surface is still:

```text
single Hamiltonian clock + arbitrary admissible local slice data
+ directed/retarded support + no final-boundary or nonlocal fixed-point import
```

Positive budget means that the apparent late-to-early dependence has been
classified as imported structure outside that retained surface. It does not
mean the imported theory is mathematically inconsistent.

## Budget Rule

For a construction `C`, let `imports(C)` be the smallest explicit set of import
types needed to make the claimed late-to-early dependence work.

```text
counted_budget(C) = number of import types in imports(C)
weighted_budget(C) = sum(weight(import_type) for import_type in imports(C))
```

The weights are review weights, not probabilities and not theorem strength.
They only make the classifier harder to blur:

- weight `2`: the construction replaces retained retarded evaluation by a
  global equation, future-boundary solve, or full closed-state reversal;
- weight `3`: the construction imposes a loop-wide consistency rule,
  final-boundary admissibility filter, or nonlocal support constraint.

Zero budget is reserved for retained retarded evolution.

## Import Types

| id | import type | weight | definition | retained classification |
|---|---|---:|---|---|
| `causal_cycle_fixed_point` | causal cycle / fixed point | 2 | a late-to-early edge breaks DAG order, or the variables are solved as one simultaneous fixed-point system | not a local retarded channel |
| `ctc_consistency` | CTC consistency | 3 | histories on a closed timelike loop are admitted only if they satisfy a loop-wide consistency condition | constrained history surface, not arbitrary local Cauchy evolution |
| `postselection_final_boundary` | postselection / final-boundary | 3 | a later outcome, accepted branch, or final state is used as an admissibility condition | conditional subensemble or final-boundary theory |
| `advanced_future_boundary_support` | advanced future-boundary support | 2 | later source degrees are supplied to an earlier field solve through advanced or absorber-style support | future-boundary import, not retarded signaling |
| `multi_time_nonlocal_support_constraint` | multi-time nonlocal support constraint | 3 | extra time variables are made well posed by nonlocal restrictions on admissible support data | different constrained multi-time surface |
| `full_closed_state_record_reversal` | full closed-state record reversal | 2 | inverse evolution is applied to the entire closed state, including records, apparatus, environment, and memories | reversible reconstruction, not selective past editing |

Some constructions legitimately receive more than one tag. A CTC presented as
a directed loop with a consistency equation may use both
`causal_cycle_fixed_point` and `ctc_consistency`. A pure algebraic fixed-point
toy model need only use `causal_cycle_fixed_point`.

## Named Construction Budget

| construction | imports | counted | weighted | classification |
|---|---|---:|---:|---|
| retained retarded evolution | none | 0 | 0 | retained zero-budget surface |
| advanced field | `advanced_future_boundary_support` | 1 | 2 | future-boundary import, not past signaling |
| postselection | `postselection_final_boundary` | 1 | 3 | conditional/final-boundary import, not same-run past editing |
| CTC / fixed-point construction | `causal_cycle_fixed_point`, `ctc_consistency` | 2 | 5 | global fixed-point and loop-consistency import |
| multi-time support construction | `multi_time_nonlocal_support_constraint` | 1 | 3 | constrained support surface outside retained single-clock semantics |
| full Loschmidt reversal | `full_closed_state_record_reversal` | 1 | 2 | reconstruction/global un-writing, not operational past signaling |

The Loschmidt row is intentionally positive-budget. The import is not
"backward signaling"; it is the requirement that the whole closed
record/environment/apparatus state be reversed. A partial reversal has
remaining witnesses. A full reversal also erases the later lab state and the
memory that the operation was performed.

## PASS/FAIL Artifact

The executable checker is:

```bash
python3 scripts/chronology_import_budget.py
```

It must keep these boundary checks true:

- retained retarded evolution has counted and weighted budget `0`;
- advanced field has positive budget;
- postselection has positive budget;
- CTC / fixed-point construction has positive budget;
- full Loschmidt reversal has positive budget and is classified as
  reconstruction, not past signaling.

## Safe Language

Use:

- "counted/weighted import budget"
- "positive budget means imported structure outside the retained surface"
- "classifier, not a proof against all theories"
- "reconstruction, not operational past signaling"

Avoid:

- "positive budget proves the construction impossible"
- "advanced support is a local backward signal"
- "postselection changed discarded runs"
- "Loschmidt reversal selectively edits the past"
