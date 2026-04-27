# Chronology Import Classification Note

**Date:** 2026-04-25
**Status:** chronology-protection companion note; boundary classifier only
**Companions:**
[FRONTIER_EXTENSION_LANE_OPENING_NOTE_2026-04-25.md](FRONTIER_EXTENSION_LANE_OPENING_NOTE_2026-04-25.md),
[CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md](CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md),
[U_MINUS_T_VS_PAST_SIGNALING_NOTE.md](U_MINUS_T_VS_PAST_SIGNALING_NOTE.md)

## Role

This note classifies apparent time-travel constructions by the extra structure
they import beyond the retained `Cl(3)/Z^3` chronology surface.

This is not a time-machine lane. It is a retained-surface boundary classifier.
The safe claim remains:

> On the retained single-clock, local-data framework surface, the theory admits
> reversible reconstruction but no operational signaling to an earlier durable
> record.

The purpose is to keep later chronology work from turning equation-level
reversibility, global consistency, postselection, advanced Green functions,
multi-time constraints, or Loschmidt echoes into an overclaim.

## Retained Surface

The classifier uses the same hypotheses as the operational no-past-signaling
support note:

1. one strongly continuous Hamiltonian clock `U(t) = exp(-itH)`;
2. arbitrary admissible local data on one codimension-1 slice;
3. directed acyclic causal order, or retarded support semantics compatible
   with that order;
4. no extra final-boundary condition, postselection rule, or nonlocal
   fixed-point condition;
5. durable records are physical degrees of freedom, including apparatus and
   environmental copies when those copies exist.

The load-bearing framework hook is not CPT. It is the single-clock,
codimension-1 Cauchy surface recorded in
[ANOMALY_FORCES_TIME_THEOREM.md](ANOMALY_FORCES_TIME_THEOREM.md), together with
the retarded / causal-support discipline used by the existing causal-field and
light-cone notes.

## Classification Principle

If a construction makes an earlier variable `R(t0)` depend on a later
controllable choice `a(t1)` with `t1 > t0`, then on the retained surface that
dependence cannot be a local past-directed channel. It must be classified as
one of the following imports:

- a directed causal cycle or fixed-point equation;
- a CTC global consistency condition;
- a postselection or final-boundary constraint;
- advanced-field future-boundary data;
- multi-time nonlocal support constraints;
- a full Loschmidt reversal of records, environment, and apparatus.

This is a smallest-import classification. Some constructions import more than
one item. For example, a closed timelike curve often presents as both a directed
cycle and a global consistency rule. The classifier should name the strongest
structure actually doing the work.

## Import Table

| apparent construction | extra imported structure | retained-surface classification | barred claim |
|---|---|---|---|
| late-to-early graph edge | directed causal cycle, or a fixed-point solve after the DAG fails | not a retarded channel; either ill-ordered or converted into a global equation system | "a local operation at `t1` sent a signal to `t0`" |
| closed timelike curve | global consistency condition on a loop of events | constrained history surface, not arbitrary local Cauchy evolution | "paradox-free CTC consistency gives controllable past editing" |
| postselected teleportation / P-CTC / final-state projection | later outcome or final state imposed as an admissibility filter | conditional subensemble or nonunitary/nonlinear theory surface | "discarded runs were changed" or "postselection rewrote the past" |
| advanced Green function / absorber term | future source data included in the boundary-value problem | future-boundary import, not retained retarded support | "advanced fields are local backward signals" |
| multi-time wave equation or extra temporal dimensions | nonlocal support restrictions replacing arbitrary codimension-1 data | different constrained multi-time theory | "extra time dimensions preserve the same local Cauchy semantics" |
| `U(-t)` / Loschmidt echo | inverse map applied to the full closed state, including records and environment | reversible reconstruction or global un-writing of the later state | "selective erasure of an earlier durable record while the later lab remains intact" |

## Class 1: Directed Causal Cycle Or Fixed Point

A retained directed causal presentation evaluates local data along a partial
order. A later-to-earlier edge breaks that partial order. There are only two
honest readings:

1. **Retarded-channel reading:** the edge is inadmissible because it violates
   clock orientation and destroys topological order.
2. **Equation-system reading:** the variables are solved simultaneously as a
   fixed point. Earlier variables may then depend on later source terms, but
   only because the later source terms were included in the global equation
   system.

The second reading is useful as a boundary witness. It is not a retained
local-data channel.

Existing probe:

```bash
python3 scripts/chronology_cycle_insertion_probe.py
```

Expected classification:

```text
late-to-early edge -> DAG failure or fixed-point/final-boundary import
```

## Class 2: CTC Global Consistency

A closed timelike curve is stronger than a single inserted edge. The usual
paradox-free version imposes a condition like:

```text
state entering loop = state produced after traversing loop
```

That is a loop-wide consistency constraint. It can remove paradoxes by
removing inconsistent histories, but this is precisely the import. The allowed
histories are no longer generated from arbitrary local codimension-1 data by
retained forward evolution.

Operationally:

- if a later choice is inconsistent with the loop, the history is absent or
  has zero admissible weight;
- if the loop has a unique fixed point, the apparent "message" is fixed by the
  global solution, not freely chosen at `t1`;
- if the loop has several fixed points, an extra selection rule is still
  needed to say which fixed point is realized.

Retained classification:

```text
CTC -> global consistency / fixed-point import
```

This note does not claim that every mathematically definable CTC spacetime is
inconsistent. It says that CTC global consistency is not the retained
single-clock local Cauchy surface.

## Class 3: Postselection And Final-Boundary Constraints

Postselection and final-state boundary proposals make earlier statistics depend
on later conditions by conditioning the ensemble, or by declaring a later state
to be part of the definition of the history.

The retained distinction is:

```text
P(past | later outcome) can change
P(past record physically realized in an individual run) does not get edited
```

If postselection is ordinary conditioning, discarded runs were not changed. If
postselection is promoted to a deterministic dynamical rule, the theory has
imported a final boundary and generally becomes nonunitary, nonlinear, or
nonlocal relative to the retained surface.

Retained classification:

```text
postselection -> conditional subensemble or final-boundary import
```

The safe language is "later conditioning changes the selected ensemble," not
"the later choice changed what happened in the run."

## Class 4: Advanced-Field Future-Boundary Import

Retarded support has the retained local-data form:

```text
field(t, x) depends on source(t', x') with t' <= t
```

An advanced Green-function solve has the future-boundary form:

```text
field(t, x) depends on source(t', x') with t' >= t
```

The earlier field can change when a later source is toggled only because the
later source has been supplied to the earlier boundary-value problem. That is
not a local operation propagating backward inside retained retarded semantics.

Existing probe:

```bash
python3 scripts/advanced_vs_retarded_field_probe.py
```

Expected classification:

```text
advanced dependence -> future-boundary import
```

## Class 5: Multi-Time Nonlocal Support Constraints

The retained framework uses one Hamiltonian clock and one codimension-1
initial surface. Multi-time or `d_t > 1` theories do not preserve that same
well-posedness condition for arbitrary local data. The relevant obstruction is
not a slogan about "extra time is weird"; it is the support constraint.

For ultrahyperbolic / multi-time systems, well-posed evolution requires
nonlocal restrictions on the allowed initial data, often expressible as a
Fourier-space support condition. A local perturbation on the slice generally
does not remain inside the admissible support class.

Retained classification:

```text
multi-time construction -> constrained nonlocal support surface
```

A constrained multi-time theory may be studied as a different theory. It is
not the retained graph-local Cauchy surface with arbitrary admissible local
slice data.

## Class 6: Full Loschmidt Reversal Of Records And Environment

`U(-t)` exists for a closed unitary history:

```text
psi(t0) = U(-(t1 - t0)) psi(t1)
```

That is inverse reconstruction. It is not a late local operation that changes
an already-realized durable record.

A Loschmidt echo can return a finite closed system toward an earlier state
only to the extent that the whole closed state is reversed. Once a record has
copied into an apparatus, environment, scattered radiation, or substrate mark,
those degrees of freedom are part of the state. Partial reversal leaves a
witness. Full reversal also erases the later lab state and any memory that the
echo operation was performed.

Existing probe:

```bash
python3 scripts/loschmidt_echo_record_probe.py
```

Expected classification:

```text
record erasure -> full closed-state reversal, not selective past editing
```

## Probe Inventory

The three existing chronology probes cover the first retained checks:

| script | current role |
|---|---|
| `scripts/chronology_cycle_insertion_probe.py` | distinguishes a retained DAG from a late-to-early fixed-point import |
| `scripts/advanced_vs_retarded_field_probe.py` | distinguishes retarded support from advanced future-boundary import |
| `scripts/loschmidt_echo_record_probe.py` | distinguishes inverse reconstruction from selective durable-record editing |

Compilation and current probe run:

```bash
python3 -m py_compile \
  scripts/chronology_cycle_insertion_probe.py \
  scripts/advanced_vs_retarded_field_probe.py \
  scripts/loschmidt_echo_record_probe.py
python3 scripts/chronology_cycle_insertion_probe.py
python3 scripts/advanced_vs_retarded_field_probe.py
python3 scripts/loschmidt_echo_record_probe.py
```

The following extension probes sharpen the classifier into a review packet:

| script | classification target | witness |
|---|---|---|
| `scripts/causal_cycle_fixed_point_dimension_probe.py` | cycles versus arbitrary local Cauchy data | acyclic systems solve forward; nonsingular cycles solve only as global fixed points; singular identity cycles impose source constraints and fixed-point freedom |
| `scripts/postselection_ctc_nonlinearity_probe.py` | postselection / P-CTC-style final-boundary maps | unnormalized success branch is linear, but normalized accepted-state map fails convex-linearity exactly |
| `scripts/future_boundary_import_index.py` | advanced and symmetric field solves | retarded earlier-event import index is zero; advanced and symmetric solves have positive future-source import index |
| `scripts/partial_loschmidt_record_lower_bound.py` | partial Loschmidt reversal versus durable records | remaining witnesses equal unreversed durable copy carriers; zero witness occurs only for full closed-state reversal |
| `scripts/chronology_import_budget.py` | import-budget registry | retained retarded evolution has zero budget; advanced, postselected, CTC, multi-time, and full-Loschmidt constructions have positive import budgets |
| `scripts/ctc_fixed_point_taxonomy_probe.py` | CTC loop consistency | no fixed point means inconsistent history; unique fixed point removes controllability; multiple fixed points require a selector |
| `scripts/postselection_no_signaling_audit.py` | postselection ensemble bookkeeping | `P(past | future selected)` shifts while unconditioned earlier records and discarded runs remain unchanged |
| `scripts/multi_time_support_constraint_probe.py` | multi-time support import | delta-local slice data activate forbidden modes and require a nonlocal support projection |
| `scripts/chronology_operator_algebra_no_past_signal_probe.py` | finite record-algebra no-signaling | trace-preserving maps outside the record algebra preserve the record marginal and record-observable expectations |
| `scripts/durable_record_formation_boundary_probe.py` | sufficient finite durable-record carrier model | redundant carriers survive bounded damage; partial erasure leaves witnesses |

Review-packet commands:

```bash
python3 scripts/chronology_protection_suite.py
```

## Loopholes And Non-Claims

This classifier is intentionally conditional.

- It does not rule out every mathematical spacetime with CTCs. It says that
  CTC global consistency is an imported constraint, not retained single-clock
  local Cauchy evolution.
- It does not disprove postselected quantum models. It classifies them as
  conditional-subensemble or final-boundary theories unless they supply a
  retained local mechanism.
- It does not deny time-symmetric or absorber-style field formalisms. It says
  that advanced dependence is future-boundary import unless rederived as a
  retained retarded operation.
- It does not use practical irreversibility as the theorem. A perfect finite
  Loschmidt reversal may exist in principle. The boundary is that it reverses
  the full closed record/environment/apparatus state, not only the inconvenient
  past record.
- It does not finish the measurement problem or durable-record derivation. It
  only states that once records are treated as physical degrees of freedom,
  they cannot be omitted from the state being reversed.
- It does not claim that CPT, T symmetry, or `U(-t)` are false. They are
  equation-level symmetries or inverse maps, not same-history control knobs
  acting on an already-existing past record.

## Safe Language

Use:

- "retained-surface boundary classifier"
- "future-boundary import"
- "global consistency constraint"
- "conditional subensemble"
- "nonlocal support constraint"
- "full closed-state reversal"
- "reversible reconstruction, not operational past signaling"

Avoid:

- "time machine"
- "send information backward in time"
- "CPT permits time travel"
- "advanced fields are local backward signals"
- "postselection changed the discarded runs"
- "Loschmidt echo changes the past while preserving the later lab"

## Retained Conclusion

Every apparent time-travel construction in this classification gets its
late-to-early dependence by importing structure outside the retained
single-clock local-data surface. The retained chronology lane should therefore
remain a boundary-protection lane: it classifies imports and preserves the
strict no-operational-past-signaling claim.
