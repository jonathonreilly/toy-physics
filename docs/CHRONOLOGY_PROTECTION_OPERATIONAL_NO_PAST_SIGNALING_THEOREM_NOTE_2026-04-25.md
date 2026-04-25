# Chronology Protection: Operational No-Past-Signaling Theorem

**Date:** 2026-04-25
**Status:** frontier theorem note; advances the chronology-protection lane but
does not close it
**Scope:** single-clock Hilbert/local-data surface with durable records treated
as physical degrees of freedom

## Claim

On the retained single-clock framework surface, an operation chosen at clock
time `t_1` cannot alter the operational probability law of a record or boundary
datum at an earlier clock time `t_0 < t_1`.

The proof is an exact trace-preservation theorem. It does not use informal
"time travel is impossible" language, and it does not lean on the free-field
CPT theorem as its load-bearing step.

Safe wording:

> The framework admits reversible reconstruction and future Loschmidt echoes,
> but no operation at `t_1` sends a controllable signal to an earlier durable
> record at `t_0 < t_1` unless one adds postselection, a final-boundary
> constraint, a directed causal cycle, or abandons the single-clock local-data
> surface.

## Existing imports

This note uses only already-opened framework structure:

- one strongly continuous Hamiltonian clock `U(t,s)`, as used in
  [ANOMALY_FORCES_TIME_THEOREM.md](ANOMALY_FORCES_TIME_THEOREM.md)
- Hilbert/tensor-product and information-flow semantics from
  [SINGLE_AXIOM_HILBERT_NOTE.md](SINGLE_AXIOM_HILBERT_NOTE.md) and
  [SINGLE_AXIOM_INFORMATION_NOTE.md](SINGLE_AXIOM_INFORMATION_NOTE.md)
- retarded/local causal framing from
  [LIGHT_CONE_FRAMING_NOTE.md](LIGHT_CONE_FRAMING_NOTE.md) and
  [CAUSAL_FIELD_CANONICAL_CHAIN_NOTE.md](CAUSAL_FIELD_CANONICAL_CHAIN_NOTE.md)
- the boundary that free-lattice CPT is exact but not an interacting
  chronology proof, from [CPT_EXACT_NOTE.md](CPT_EXACT_NOTE.md)

## Formal model

Fix two clock times `t_0 < t_1`.

1. `rho_0` is an arbitrary admissible state on the slice immediately before
   the record event at `t_0`.
2. A record event at `t_0` is a quantum instrument
   `{M_a}`. Each `M_a` is completely positive and
   `sum_a M_a` is trace preserving. The label `a` is the durable record value.
3. Single-clock evolution from `t_0` to `t_1` is the unitary channel
   `U_10(X) = U(t_1,t_0) X U(t_1,t_0)^dagger`.
4. A later choice made at `t_1` is an arbitrary completely positive
   trace-preserving channel `E_x` on the full slice, including apparatus,
   environment, and any future copies of the record. A later measurement with
   outcomes is a family `{E_{x,b}}` whose nonselective sum
   `E_x = sum_b E_{x,b}` is trace preserving.

An operational past signal is a dependence of the earlier record law
`P(a | x)` on the later freely chosen setting `x`, without conditioning on a
future outcome `b`.

This definition intentionally allows destructive future operations on memory
systems. Erasing or overwriting a record copy after `t_1` is an ordinary future
causal action. It is not a change to the event law on the earlier slice
`t_0`.

## Theorem

For every admissible `rho_0`, every record instrument `{M_a}` at `t_0`, every
later setting `x`, and every later trace-preserving operation `E_x` at or after
`t_1`,

```text
P_x(a) = Tr[ E_x( U_10( M_a(rho_0) ) ) ]
       = Tr[ U_10( M_a(rho_0) ) ]
       = Tr[ M_a(rho_0) ].
```

Therefore `P_x(a)` is independent of `x`. No operation chosen at `t_1` sends an
operational signal to the earlier record at `t_0`.

The same statement holds for any finite sequence of later operations, because
the composition of trace-preserving channels is trace preserving.

## Proof

The proof is three lines, but each hypothesis matters.

First, single-clock chronology gives an ordered circuit. A choice made at
`t_1` can only appear after the record instrument at `t_0` and after the
evolution channel `U_10`. The unnormalized branch state associated with the
earlier record value `a` at time `t_1` is

```text
sigma_a = U_10( M_a(rho_0) ).
```

Second, every admissible later nonselective operation is trace preserving.
Hence

```text
Tr[ E_x(sigma_a) ] = Tr[ sigma_a ]
```

for every `x` and every positive trace-class branch state `sigma_a`.

Third, unitary evolution preserves trace:

```text
Tr[ sigma_a ] = Tr[ U_10( M_a(rho_0) ) ] = Tr[ M_a(rho_0) ].
```

Combining the three equalities gives the theorem. Nothing in the result depends
on a special lattice size, a special state, or a special representation of
`Cl(3)`.

For a later measurement with outcomes `{b}`, the operationally relevant
unconditioned probability is

```text
P_x(a) = sum_b Tr[ E_{x,b}(sigma_a) ]
       = Tr[ (sum_b E_{x,b})(sigma_a) ]
       = Tr[ E_x(sigma_a) ]
       = Tr[ sigma_a ].
```

Conditioning on a future outcome `b` can change `P(a | x,b)`. That is
postselection, not a controllable signal to the past.

## Boundary-data version

If the earlier datum is not a measurement record but an effect `F_a` or a
classical boundary component on `Sigma_{t_0}`, the same proof is the Heisenberg
dual statement.

The adjoint of a trace-preserving channel is unital:

```text
E_x^*(I) = I.
```

Thus a later nonselective operation contributes only an identity effect when
one computes the earlier marginal. Future settings can change later
correlations, but they cannot change the earlier marginal datum.

## Why `U(-t)` is not past signaling

The inverse unitary `U(t_0,t_1)` is a reconstruction map between two complete
closed-system slices. It is not an operation inserted into the already ordered
history before `t_0`.

If an agent at `t_1` physically implements a Hamiltonian that realizes
`U(t_0,t_1)` for a duration, the clock still advances to a later slice. The
result is a Loschmidt echo in the future:

```text
t_1 -> t_2,    rho(t_2) = U(t_0,t_1) rho(t_1) U(t_0,t_1)^dagger.
```

It may reproduce an earlier microstate as a new future state if the agent has
coherent control of the complete closed system. It does not alter the record
event that already occurred on `Sigma_{t_0}`.

To make the record on `Sigma_{t_0}` differ, one must do at least one of the
following:

- choose different initial data before `t_0`
- impose a final-boundary or fixed-point constraint
- postselect on a later outcome and discuss only the selected subensemble
- introduce a causal cycle so that the operation is no longer later in the
  partial order

All four are outside the retained single-clock local-data surface.

## Why CPT and T do not create a channel to the past

The free-lattice CPT theorem says the free staggered Hamiltonian is invariant
under a combined transformation. That is a symmetry statement about complete
solutions. It is not a device that lets a later local agent change an earlier
record.

Time reversal has the same boundary. Reversing a full closed history also
reverses momenta, apparatus states, record carriers, and environment degrees of
freedom. A partial future operation that leaves the earlier record fixed is
just an ordinary future operation, and the trace-preservation theorem applies.

## Reviewer-pressure checks

### Delayed choice and quantum eraser

Delayed-choice and eraser experiments change which future correlations are
available. Their unconditioned earlier detection statistics are unchanged.
They realize the conditional `P(a | x,b)` loophole, not a change in `P(a | x)`.

### Future erasure of a memory

A later operation may erase a memory register or overwrite a durable record
copy. That changes the future state of the memory. It does not change the
earlier event law `Tr[M_a(rho_0)]`.

### Nonunitary postselection

A trace-decreasing selected branch can bias the apparent past ensemble after
conditioning. The branch probability itself is the price paid for that
selection. Without communicating the later selected outcome forward to the
reader, there is no controllable message in the earlier marginal.

### Advanced fields

An advanced Green-function calculation imports future boundary data. It is a
two-boundary or final-condition problem, not an operation chosen on one
single-clock Cauchy slice after the earlier record has been fixed.

### Closed timelike curves

A CTC or Deutsch-style fixed-point model adds a directed causal cycle or a
nonlocal consistency constraint. That is exactly one of the exits listed in
the lane-opening note. It is not a counterexample inside the retained
single-clock local-data framework.

## What this advances

This note supplies the theorem-grade core of the chronology-protection lane:

```text
single-clock ordered composition
  + trace-preserving later operations
  + no future postselection/final-boundary import
  => no operational signaling to an earlier record.
```

It does not close the lane. Remaining useful artifacts are still:

- an explicit cycle-insertion probe showing loss of partial-order semantics
- a Loschmidt-record probe separating future echoes from earlier-record
  alteration
- an advanced-vs-retarded field note classifying future-boundary imports
- an interacting extension boundary for CPT/T language, if that language is
  later used anywhere near chronology claims

## Claim boundary

What is proved:

- exact no-past-signaling on the retained single-clock Hilbert/local-data
  surface
- exact separation between future inverse evolution and alteration of an
  earlier durable record
- exact identification of the needed escape hatches: postselection,
  final-boundary constraints, causal cycles, or abandoning single-clock
  Cauchy evolution

What is not proved:

- no theorem about arbitrary non-framework multi-time theories
- no interacting CPT theorem
- no final measurement ontology
- no blanket statement about all possible CTC toy models
- no manuscript promotion or lane closure
