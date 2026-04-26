# Taste-Qubit Encoding Portability Note

**Date:** 2026-04-25
**Status:** planning audit; not a manuscript claim surface
**Runner:** `scripts/frontier_teleportation_encoding_portability.py`

## Scope

This note records a finite portability audit for the encoded taste-qubit
teleportation artifact.  It uses the same Kogut-Susskind cell/taste surface as
`scripts/frontier_teleportation_protocol.py` and
`scripts/frontier_bell_inequality.py`:

```text
C^(side^dim) = C^((side/2)^dim cells) tensor C^(2^dim tastes)
```

Only even side lengths in dimensions 1, 2, and 3 are audited.  The audit checks
every available cell, every spectator taste assignment, and every logical taste
axis for the requested geometries.

This remains ordinary quantum state teleportation on ideal encoded taste-qubit
registers.  It is not matter teleportation, mass transfer, charge transfer, or
faster-than-light transport.

## Operator Sets

The runner compares two operator sets.

```text
current_fixed_x:
  Z = sublattice parity = I_cells tensor xi_5
  X = row-major pair-hop = I_cells tensor sigma_x on the last taste axis

axis_adapted_x:
  Z = sublattice parity
  X = I_cells tensor sigma_x on the selected logical taste axis
```

The second set is a control: it shows what works if the taste `X` operator is
retargeted to the selected logical axis.  It is not a claim that the current
fixed pair-hop gate already implements every logical axis.

## Default Run

Command:

```bash
python3 scripts/frontier_teleportation_encoding_portability.py
```

Default audit surface:

```text
dimensions: 1, 2, 3
side lengths: 2, 4, 6, 8
valid KS geometries: 12
skipped geometries: 0
cell sets across geometries: 140
encoding cases: 1330
random teleportation trials per accepted encoding: 8
tolerance: 1e-12
```

Pass counts by dimension and logical axis:

```text
dim axis  current_fixed_x  axis_adapted_x
1   0     10/10            10/10
2   0     0/60             60/60
2   1     60/60            60/60
3   0     0/400            400/400
3   1     0/400            400/400
3   2     400/400          400/400
```

Aggregate results:

```text
current_fixed_x:
  logical Pauli pass: 470/1330
  Bell-projector gate pass: 470/1330
  teleportation/no-signaling pass: 470/470 run
  skipped before teleportation: 860
  failure cause: current_pair_hop_x_flips_last_axis_not_logical_axis=860
  zero X-restriction failures: 860
  max failed-case X leakage: 1.414e+00
  max failed-case Bell-projector idempotence/orthogonality error: 2.500e-01
  minimum corrected-state fidelity on accepted encodings: 0.9999999999999996
  maximum infidelity on accepted encodings: 8.882e-16
  max Bob pre-message pairwise trace distance: 4.441e-16

axis_adapted_x:
  logical Pauli pass: 1330/1330
  Bell-projector gate pass: 1330/1330
  teleportation/no-signaling pass: 1330/1330
  failure causes: none
  max Z leakage: 0.000e+00
  max X leakage: 0.000e+00
  minimum corrected-state fidelity: 0.9999999999999996
  maximum infidelity: 8.882e-16
  max Bob pre-message pairwise trace distance: 4.996e-16
```

The restricted `Z` operator is a signed logical Pauli on all surveyed
encodings.  The sign depends on spectator parity:

```text
Z sign counts across all cases: -1=660, +1=670
```

That sign does not break the same-encoding teleportation gates because it
cancels in the two-register Bell stabilizers and contributes at most a global
phase to the corresponding Pauli correction.

## Interpretation

The current fixed-cell encoding generalizes in these bounded senses:

- the fixed 3D side-4 cell `(0,0,0)` case extends to every surveyed cell;
- spectator taste bits need not be fixed to zero;
- the same fixed pair-hop `X` works in each surveyed dimension and side length
  when the logical taste axis is the last axis;
- the accepted encodings pass logical-Pauli restrictions, Bell-projector
  gates, corrected-state teleportation, and Bob pre-message no-signaling gates
  to numerical precision.

The current fixed-cell encoding fails in this bounded sense:

- in dimensions 2 and 3, selecting a non-last logical taste axis while keeping
  the current row-major pair-hop `X` does not produce a logical `X`;
- the pair-hop flips the last taste bit instead of the selected logical bit;
- for those 860 cases, the `X` restriction to the selected two-dimensional
  encoded subspace is zero and the operator leaks out of the subspace with
  norm `sqrt(2)`;
- the resulting Bell-projector candidates are not valid projectors, with
  worst idempotence and orthogonality errors `2.500e-01`.

The axis-adapted control shows that this is an operator-targeting failure, not
a cell or spectator obstruction: using `I_cells tensor sigma_x` on the selected
logical taste axis passes all 1330 surveyed encodings.

## Limitations

This is a finite algebraic audit.  It does not cover odd side lengths, because
the audited KS cell/taste factorization requires even side length.

The default run covers only dimensions 1, 2, and 3 and side lengths 2, 4, 6,
and 8.  Larger even lattices are not claimed by this run.

Each test uses the same encoding for Alice's input register, Alice's Bell-half
register, and Bob's Bell-half register.  The audit does not test cross-cell,
cross-axis, or cross-spectator teleportation maps.

The Bell resource, Bell measurement, and correction gates are ideal logical
objects.  The audit does not derive a physical measurement apparatus, durable
record channel, resource-preparation channel, Hamiltonian transport, noise
model, or readout error model.

No matter, mass, charge, energy, or object is teleported.  Only an unknown
quantum state on Bob's already-present encoded taste-qubit register is
reconstructed after the classical Bell record is available.
