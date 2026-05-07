# Native Teleportation Transport Theory Note

**Date:** 2026-04-26
**Status:** planning / candidate transport theory; not retained framework
promotion
**Companion runner:** `scripts/frontier_teleportation_transport_invariants.py`

## Scope

This note develops a second theory layer for the native taste-qubit
teleportation lane. The prior axiom note made accounting obligations explicit.
This note proposes a more structural interpretation:

> Native teleportation is not transport of a particle or conserved support.
> It is trivialization of a discrete Pauli-frame connection on a retained
> taste-qubit fiber, enabled by a classical 3D+1 record section.

This is a candidate lane theory only. It does not promote teleportation beyond
planning status and does not claim matter teleportation, mass transfer, charge
transfer, energy transfer, object transport, or faster-than-light signaling.

## Geometric Object

Use a 3D+1 base `B` whose points are lattice events

```text
e = (x, y, z, t).
```

At selected spatial sites there is a retained taste-qubit fiber

```text
F_e = C^2
```

obtained from a Kogut-Susskind cell/taste factorization after a retained-axis
choice. Cells and spectator taste bits are the local environment unless they
are explicitly promoted to records.

The full local bookkeeping splits into two layers:

```text
base ledger:      site support, mass, charge, energy, apparatus records
retained fiber:   encoded taste-qubit state and Pauli frame
```

Teleportation acts on the retained fiber of Bob's already-present register. It
does not move the base ledger from Alice's site to Bob's site.

## New Candidate Axioms

### T1. Base-Fiber Separation

Every admissible native teleportation claim must factor its degrees of freedom
into:

```text
base/event ledger algebra L_B
retained taste-qubit fiber algebra A_F
```

Bob corrections and Bell-frame updates act in `A_F`. Conserved support,
charge, mass, energy, and apparatus records live in `L_B`. A teleportation
success is admissible only when the correction algebra commutes with the
ledger algebra:

```text
[C_B, L] = 0 for every retained ledger observable L.
```

This is stronger than a verbal no-transfer disclaimer. It requires the protocol
to exhibit the algebra that cannot transport the conserved ledgers.

### T2. Bell Resource As A Pauli Connection

A Bell resource between Alice's resource half and Bob's register is an oriented
edge carrying a `Z2 x Z2` connection value:

```text
h(e_A -> e_B) in Z2 x Z2.
```

The four Bell sectors are connection frames:

```text
Phi+ : (0, 0)
Phi- : (1, 0)
Psi+ : (0, 1)
Psi- : (1, 1)
```

Alice's Bell measurement gives another `Z2 x Z2` value `c`. Bob's required
fiber correction is the connection holonomy

```text
k = c xor h.
```

The positive `3D side=2` resource currently has `h=(0,1)` (`Psi+`). That is a
connection value, not a particle displacement.

### T3. Causal Record Section

The measurement value `c` is not available as an operation at Bob until there
is a classical section of the record sheaf over a 3D+1 future-cone path:

```text
gamma_c: e_A -> e_B,
t_B >= t_A + d_3D(e_A, e_B) / v.
```

Before the section reaches Bob, Bob has the connection edge but not the local
trivialization data. Operationally, this is the Pauli-twirled channel: Bob's
fiber state is independent of Alice's unknown input.

### T4. Flatness Or Recorded Holonomy

For a network of teleportation resources, connection values compose by xor
along paths. A closed loop has holonomy

```text
H(loop) = xor_edges h(edge).
```

There are only two admissible cases:

```text
H(loop) = (0, 0)                  flat calibrated loop
H(loop) != (0, 0) and recorded    calibrated logical Pauli defect
```

An unrecorded nonzero loop holonomy is an invalid deterministic protocol. It
is a hidden Pauli error, not a new transport effect.

### T5. Branch Records Are Gauge Data

Spectator taste branches, Bell-frame labels, and Bell outcomes are all
discrete gauge data. They may be traced only after proving irrelevance. If
they affect the retained fiber, they must become classical records and obey
T3. Otherwise they must be rejected.

For 3D raw `xi_5`, the hidden spectator sign is exactly such a branch datum:

```text
xi_5 | branch = +/- Z_r.
```

Without a branch record, deterministic `xi_5` retained-Z readout creates an
untracked Pauli sign channel. With a branch record, it becomes an ordinary
conditioned correction problem.

### T6. Preparation Curvature

A Poisson Hamiltonian path that creates a Bell resource is not just a way to
obtain a density matrix. It induces a connection frame and possible curvature
over the resource-parameter space:

```text
G, mass, boundary, retained axis, schedule -> h in Z2 x Z2.
```

Nature-grade closure therefore needs more than high fidelity at one point. It
needs a calibration law for how the Bell frame changes under native parameter
variation, and a proof that any changes are either continuous within a sector,
cross a diagnosed gap/degeneracy event, or become explicit records.

## Derived Results

### Theorem A: Missing-Record Twirl

Assume T2 and T3. If Bob has the resource connection `h` but not Alice's
Bell-record value `c`, Bob must average over `c`. The four possible Pauli
corrections form the single-qubit Pauli twirl:

```text
rho -> 1/4 sum_k P_k rho P_k = I/2.
```

For an imperfect resource the Bob marginal may be biased, but the unknown
input still cannot be recovered before the causal section arrives.

### Theorem B: Multi-Hop Composition

A chain of native teleportation links has total correction

```text
k_total = xor_i c_i xor_i h_i.
```

Thus a multi-hop chain is equivalent, on the retained fiber, to one Pauli-frame
connection with total holonomy `k_total`. This gives a sharp scaling target:
larger protocols must track xor-composed frame data, not only endpoint
fidelity.

### Theorem C: Ledger No-Transfer

Assume T1. Since every Bob correction is `I_base tensor P_fiber`, it commutes
with every retained base-ledger observable `L_base tensor I_fiber`. Therefore
teleportation cannot move or rewrite the mass, charge, energy, or support
ledger. Only the retained fiber state on Bob's already-present register is
changed.

### Theorem D: Hidden Branch Dephasing

Assume T5. If a branch sign controls whether the retained operation is `I` or
`Z` and the branch is not recorded, the effective channel is

```text
rho -> 1/2 (rho + Z rho Z).
```

For an equatorial input this destroys phase coherence. Therefore hidden
spectator branches are experimentally visible as dephasing/fidelity loss; they
cannot be swept into notation.

### Theorem E: Holonomy Defect Bound

A nonzero unrecorded loop holonomy in `Z2 x Z2` is a deterministic logical
Pauli defect. It can be corrected only by a recorded frame update. If no such
record exists, the protocol is not closed even if local edge fidelities are
high.

## Why This Is A New Theory Step

The earlier artifacts already show ordinary teleportation on encoded
taste-qubit registers. This note adds a candidate native mechanism vocabulary:

- Bell resources are not just useful states; they are connection edges.
- Bell outcomes are not just two classical bits; they are local holonomy
  measurements.
- Bob correction is not just feed-forward; it is connection trivialization.
- 3D+1 causality is not just a latency check; it is the domain condition for a
  record section.
- The no-transfer boundary is not only a warning; it is an algebraic
  superselection requirement against the base ledger.

These are creative additions, but they remain conditional lane theory until
the native Hamiltonian, measurement, record, apparatus, and conservation
stories are derived.

## Nature-Grade Review Consequences

This theory raises the closure bar. A future nature-grade package would need:

1. a retained base/fiber algebra decomposition for the actual apparatus;
2. a derivation of Bell-resource connection values from native Poisson
   dynamics, including calibration across parameters;
3. a derivation of durable Bell-record sections in 3D+1;
4. a proof that Bob corrections commute with all relevant conservation ledgers;
5. a loop/holonomy audit for any multi-link or extended-resource protocol;
6. a hidden-branch dephasing audit for every spectator or environment label.

Until those exist, the lane remains planning / candidate theory, even when the
small-surface teleportation fidelity is high.

## Coordinated Algebraic Closure (2026-05-07)

The algebraic content of T1 (base/fiber separation) and T2 (Bell connection)
now has bounded theorem support via the Retained-Axis Operator Algebra (RALA)
theorem. Independent audit owns any effective-status change. Specifically:

  - T1 base/fiber separation is realized exactly by RALA(a): every
    correction commutes with every base-ledger observable on the same site
    (T6 of the closure note).
  - T2 Bell connection is realized exactly by the four axis Bell projectors
    P_zx^axis, which form a partition of unity, project to the four
    logical Bell states, and compose via XOR up to phase (T3 + T7 of the
    closure note).

See [`TELEPORTATION_RETAINED_AXIS_OPERATOR_ALGEBRA_CLOSURE_NOTE.md`](TELEPORTATION_RETAINED_AXIS_OPERATOR_ALGEBRA_CLOSURE_NOTE.md)
(runner `scripts/frontier_teleportation_retained_axis_operator_algebra_closure.py`)
for the proof.

T3 (causal record section), T4 (loop holonomy bookkeeping), T5 (branch
records as gauge data), and T6 (preparation curvature) of this note
require physical content beyond the RALA algebra and are *not* resolved by
the RALA theorem; they remain open in their own gates.
