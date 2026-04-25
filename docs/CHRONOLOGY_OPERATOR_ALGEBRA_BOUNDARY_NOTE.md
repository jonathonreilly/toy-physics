# Chronology Operator-Algebra Boundary Note

**Date:** 2026-04-25
**Status:** finite operator-algebra hardening note; conditional boundary surface
**Probe:** `scripts/chronology_operator_algebra_no_past_signal_probe.py`
**Companions:**
[CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md](CHRONOLOGY_PROTECTION_OPERATIONAL_NO_PAST_SIGNALING_THEOREM_NOTE_2026-04-25.md),
[CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md](CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md),
[POSTSELECTION_NO_SIGNALING_AUDIT.md](POSTSELECTION_NO_SIGNALING_AUDIT.md)

## Role

This note states the chronology boundary in the language of local algebras and
trace-preserving operations.

The retained claim remains conditional:

> A later operation on degrees of freedom outside an earlier durable-record
> algebra cannot change the expectation values of that earlier record algebra
> on the retained single-clock local-data surface.

This is not a universal theorem about all time-nonlocal theories. It is the
operator-algebra version of the retained no-operational-past-signaling
boundary.

## Finite Theorem

Let the relevant finite closed state at a comparison slice be represented on

```text
H = H_R tensor H_L tensor H_E,
```

where:

- `R` is the durable-record carrier whose earlier value is being audited;
- `L` is the later accessible subsystem on which the agent acts;
- `E` is any untouched environment or additional record copy.

Let `A_R = B(H_R) tensor I_L tensor I_E` be the record algebra. Let the later
operation be a trace-preserving completely positive map on `L`:

```text
Phi = id_R tensor Phi_L tensor id_E.
```

Then for every record observable `O_R in A_R`,

```text
Tr[ O_R Phi(rho) ] = Tr[ O_R rho ].
```

Equivalently, in the Heisenberg picture:

```text
Phi^*(O_R tensor I_L tensor I_E)
  = O_R tensor Phi_L^*(I_L) tensor I_E
  = O_R tensor I_L tensor I_E,
```

because trace preservation is exactly `Phi_L^*(I_L) = I_L`.

So an operation localized to the later accessible algebra cannot change the
record marginal. To change the record marginal, the operation must either:

- act on the record algebra itself;
- use a non-trace-preserving selected branch and then renormalize;
- impose a final-boundary/fixed-point constraint;
- omit environment/record carriers from the state being audited.

All of those are already classified imports or future erasures, not retained
operational past signaling.

## Probe

The companion probe uses an exact finite probability table, which is the
diagonal subalgebra of the statement above.

It checks:

- a correlated `R-L` state can have strong record/later correlations;
- every stochastic trace-preserving map on `L` preserves the `R` marginal;
- the Heisenberg dual preserves the record observable because `Phi_L^*(1)=1`;
- a non-trace-preserving selected branch can shift the conditional `R`
  distribution only after renormalization;
- a map that acts directly on `R` can change `R`, but is classified as acting
  on the record carrier, not as a late operation outside the record algebra.

Run:

```bash
python3 -m py_compile scripts/chronology_operator_algebra_no_past_signal_probe.py
python3 scripts/chronology_operator_algebra_no_past_signal_probe.py
```

## Boundary

This finite theorem is deliberately modest.

- It does not derive durable-record formation.
- It does not prove that every physical environment factorization is exact.
- It does not cover nonlocal final-boundary maps, postselected dynamics, or
  CTC fixed-point maps as retained operations.
- It does not prohibit future erasure of a later copy of a record.

It does close one common loophole: ordinary later local dynamics, if
trace-preserving and outside the record algebra, cannot change the record
algebra's marginal or expectation values.

## Safe Language

Use:

- "local trace-preserving operations outside the record algebra preserve record
  expectations"
- "nonselective local operations do not alter the earlier durable-record
  marginal"
- "postselected branches are non-trace-preserving imports"

Avoid:

- "all possible operations preserve records"
- "records cannot be erased in the future"
- "operator algebra proves all time-travel theories impossible"
