# Teleportation Cross-Encoding Maps Note

**Date:** 2026-04-25
**Status:** planning / first cross-map artifact; not a manuscript claim surface
**Runner:** `scripts/frontier_teleportation_cross_encoding_maps.py`

## Scope

This note records the next bounded artifact for the native taste-qubit
teleportation lane: cross-encoding maps.  It extends the same-encoding
portability audit to Alice and Bob encoded taste qubits with different cells,
spectator taste assignments, and logical taste axes.

The audited surface is still the Kogut-Susskind cell/taste factorization:

```text
C^(side^dim) = C^((side/2)^dim cells) tensor C^(2^dim tastes)
```

Alice's unknown input register and Alice's Bell-resource half use one encoding.
Bob's already-present Bell-resource half may use a different encoding in the
same geometry.  The intended cross-encoding Bell resource pairs equal logical
coefficients:

```text
|Omega_AB> = (|0_A 0_B> + |1_A 1_B>) / sqrt(2)
```

Equivalently, the logical coefficient conversion is identity in the ordered
logical bases, while the site-basis map is the explicit partial isometry:

```text
C_{B<-A} = |0_B><0_A| + |1_B><1_A|
```

This remains ordinary quantum state teleportation only.  It does not claim
matter teleportation, mass transfer, charge transfer, energy transfer, or
faster-than-light signaling.

## Tested Surfaces

The runner compares four map surfaces.

```text
axis_adapted_cross_encoding:
  Alice Bell X = I_cells tensor sigma_x on Alice's selected logical axis
  Bob correction X = I_cells tensor sigma_x on Bob's selected logical axis
  intended resource conversion = identity logical coefficient map

current_fixed_pairhop_cross_encoding:
  Alice Bell X = current row-major pair-hop X
  Bob correction X = current row-major pair-hop X

axis_bell_bob_fixed_correction_control:
  Alice Bell measurement is axis-adapted and valid
  Bob deliberately keeps the current fixed pair-hop correction

wrong_bit_swap_resource_control:
  Alice/Bob operators are axis-adapted
  resource conversion is deliberately bit-swapped while the target map is identity
```

The fixed-pair-hop surfaces are controls.  They identify when the current
last-axis correction convention is insufficient rather than claiming a physical
failure of teleportation.

## Default Run

Command:

```bash
python3 scripts/frontier_teleportation_cross_encoding_maps.py
```

Default audit surface:

```text
dimensions: 1, 2, 3
side lengths: 2, 4
valid KS geometries: 6
encoding supports: 131
cross-encoding maps: 9637
random trials per cross map: 8
tolerance: 1e-12
```

Geometry counts:

```text
dim=1 side=2: 1 encodings, 1 maps
dim=1 side=4: 2 encodings, 4 maps
dim=2 side=2: 4 encodings, 16 maps
dim=2 side=4: 16 encodings, 256 maps
dim=3 side=2: 12 encodings, 144 maps
dim=3 side=4: 96 encodings, 9216 maps
```

Conversion-map classification:

```text
same support, no site conversion needed: 131
explicit nonidentity site maps needed: 9506
relocation only, same taste pair: 722
in-cell retaste only: 1248
relocation plus retaste: 7536
pairs with different cells: 8258
pairs with different taste supports: 8784
max partial-isometry error: 0.000e+00
```

## Numerical Results

Axis-adapted cross-encoding maps:

```text
teleportation/no-signaling pass: 9637/9637
minimum corrected-state fidelity: 0.9999999999999996
maximum infidelity: 6.661e-16
max branch probability error from 1/4: 2.220e-16
max total probability error from 1: 8.882e-16
max Bob trace distance to I/2 before Alice measurement: 4.441e-16
max Bob trace distance to I/2 after Alice measurement before message: 4.163e-16
max pairwise pre-message Bob-state distance across inputs: 5.551e-16
max corrected-state trace error: 4.441e-16
Bell outcomes seen: Phi+, Phi-, Psi+, Psi-
```

Current fixed-pair-hop cross-encoding maps:

```text
expected pass cases: 1113/9637
teleportation/no-signaling pass: 1113/1113 run
skipped before teleportation: 8524
failure causes:
  alice_bell_x_and_bob_correction_x_not_axis_adapted=4228
  alice_bell_x_not_axis_adapted=2148
  bob_correction_x_not_axis_adapted=2148
minimum corrected-state fidelity on accepted maps: 0.9999999999999996
maximum infidelity on accepted maps: 6.661e-16
```

Pass counts by geometry for the current fixed map:

```text
dim=1 side=2: 1/1
dim=1 side=4: 4/4
dim=2 side=2: 4/16
dim=2 side=4: 64/256
dim=3 side=2: 16/144
dim=3 side=4: 1024/9216
```

Axis-adapted Bell measurement with non-adapted Bob fixed correction:

```text
expected pass cases: 3261/9637
teleportation/no-signaling pass: 3261/9637
failure cause: bob_fixed_pairhop_not_logical_x=6376
minimum corrected-state fidelity: 0.0000000000000000
maximum infidelity: 1.000e+00
max corrected-state trace error: 1.000e+00
Bob pre-message input-independence still holds to 5.551e-16
```

Wrong bit-swap resource conversion control:

```text
expected pass cases: 0/9637
teleportation/no-signaling pass: 0/9637
failure cause: resource_conversion_map_not_identity_target=9637
minimum corrected-state fidelity: 0.0000000003471099
maximum infidelity: 1.000e+00
Bob pre-message input-independence still holds to 5.551e-16
```

The runner reported `PASS` for:

- axis-adapted cross maps;
- all four Bell outcomes represented;
- Bob pre-message input-independence for cross maps;
- current fixed-pair-hop boundary;
- non-adapted Bob correction failure control;
- wrong conversion failure control.

## Interpretation

The cross-map obstruction is not cell relocation or spectator taste assignment.
With axis-adapted logical `X` on Alice's Bell measurement and Bob's correction,
every surveyed Alice/Bob pair passes the Bell-outcome, random-state fidelity,
and Bob pre-message input-independence checks.

The current fixed pair-hop convention remains a last-axis convention.  It
passes cross-encoding maps only when both Alice's Bell-measurement logical axis
and Bob's correction logical axis are the last taste axis.  It fails for
non-last axes because the fixed pair-hop does not restrict to Bob's selected
logical `X`.

Explicit conversion maps are needed at the site-support level whenever Alice
and Bob supports differ.  In this first artifact the intended logical
coefficient conversion is identity, so no additional logical correction is
needed after the two-bit Bell record if the resource was prepared with the
matching site partial isometry.  The bit-swap control shows that a mismatched
resource conversion can preserve Bob pre-message no-signaling while still
failing post-message fidelity.

## Limitations

This is a finite algebraic audit over dimensions 1, 2, and 3 with side lengths
2 and 4 by default.  Larger even lattices can be requested but are not claimed
by the default run.  Odd side lengths remain outside the audited KS
cell/taste factorization.

Alice's input register and Alice's Bell-resource half use the same encoding in
this artifact.  The runner does not yet survey three independently chosen
encodings for input, Alice resource half, and Bob resource half.

The Bell resource, Bell measurement, conversion map, and Bob corrections are
ideal logical objects.  The runner does not derive a physical resource
preparation channel, measurement apparatus, durable record, Hamiltonian
transport, noise model, or readout model.

Only an unknown qubit state is reconstructed on Bob's already-present encoded
taste-qubit register after the classical Bell record is available.  No matter,
mass, charge, energy, or macroscopic object is transported, and no
faster-than-light signaling channel is introduced.
