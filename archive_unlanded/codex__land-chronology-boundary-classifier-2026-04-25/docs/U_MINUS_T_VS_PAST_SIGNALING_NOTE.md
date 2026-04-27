# U(-t) Versus Operational Past Signaling

**Date:** 2026-04-25
**Status:** chronology-protection companion note; boundary clarification only
**Companion:** [CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md](CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md)

## Purpose

This note isolates the common confusion:

```text
U(-t) exists
```

does not imply

```text
a late operation can send a controllable signal to an earlier durable record.
```

The first statement is equation-level reversibility. The second is an
operational past-signal claim. They are different claims.

## Reversibility Statement

On the retained single-clock surface,

```text
U(t) = exp(-itH),
U(-t) = U(t)^dagger.
```

For a closed state known exactly at `t_1`, one may reconstruct the earlier
closed state by

```text
psi(t_0) = U(-(t_1 - t_0)) psi(t_1).
```

This is a statement about the same closed history represented from two time
slices. It does not supply an operation localized at `t_1` whose output is an
already-realized slice at `t_0`.

## Why This Is Not A Past-Signal Channel

An operational channel has a controllable input and an output in its future
domain of dependence. A late local operation has the schematic form

```text
psi(t_1^+) = M_local psi(t_1^-),
psi(t_2) = U(t_2 - t_1) psi(t_1^+),  t_2 > t_1.
```

Nothing in that expression changes the earlier state `psi(t_0)`. One can
mathematically infer which `psi(t_0)` would evolve into a later state, but that
is retrodiction, not intervention.

In Heisenberg language, a future measurement effect can be pulled back to an
operator on an earlier slice. That pulled-back operator computes conditional
probabilities for inference. It is not a control knob acting on the past.

## CPT And T

The exact free-lattice result in [CPT_EXACT_NOTE.md](CPT_EXACT_NOTE.md) is a
structural symmetry statement:

- `T` maps a solution to a time-reversed solution;
- `CPT` preserves the free staggered Hamiltonian on the stated even periodic
  lattices;
- the interacting extension remains broader than that note.

None of these statements says that an agent inside one solution can choose at
`t_1` to alter a durable record at `t_0 < t_1`. A symmetry-related solution is
not a controllable same-history past edit.

## Loschmidt Echo Boundary

A Loschmidt echo reverses dynamics only to the extent that the full closed
state is reversed. If a measurement record has copied into an environment,
then the environment is part of the state.

The two relevant cases are:

| case | result |
|---|---|
| reverse only the selected subsystem | record/environment copies remain |
| reverse record plus environment plus apparatus plus perturbation | current state returns to a pre-record configuration |

The second case is not a message to the earlier record. It is a new later
configuration produced by globally undoing the closed evolution, including the
degrees of freedom that carried the fact that the record existed.

`scripts/loschmidt_echo_record_probe.py` implements this as a reversible
record-copy toy model. `scripts/partial_loschmidt_record_lower_bound.py`
extends the same point by exhausting partial reversals over multiple
environment copies and showing that unreversed durable copy carriers remain as
witnesses.

## Retrodiction And Postselection

Retrodiction asks:

```text
given later data, what earlier data are compatible with it?
```

Postselection asks:

```text
condition on this later outcome; what is the earlier subensemble?
```

Neither operation changes runs outside the selected subensemble, and neither
changes the physical record that already existed in an individual run. A
postselected theory with a nonlocal final boundary is a different theory
surface from the retained local Cauchy-data framework.

## Advanced Fields

Retarded support has the local-data form:

```text
field(t, x) depends on source(t', x') with t' <= t.
```

Advanced support has the future-boundary form:

```text
field(t, x) depends on source(t', x') with t' >= t.
```

If an earlier field changes when a later source is toggled, the calculation has
imported future source data into the earlier boundary-value problem. That is a
classification statement, not an operational past-signal theorem.

`scripts/advanced_vs_retarded_field_probe.py` makes this distinction explicit.

## Safe Language

Use:

> The framework admits reversible reconstruction of closed histories, but no
> operational past signaling to earlier durable records on the retained
> single-clock local-data surface.

Do not use:

- "time machine"
- "send information backward in time"
- "CPT allows time travel"
- "Loschmidt echo changes the past"
- "advanced fields are local backward signals"

## Command

```bash
python3 scripts/loschmidt_echo_record_probe.py
python3 scripts/partial_loschmidt_record_lower_bound.py
```
