# Teleportation Three-Register Cross-Encoding Note

**Date:** 2026-04-25
**Status:** planning / first three-register cross-map artifact; not a manuscript claim surface
**Runner:** `scripts/frontier_teleportation_three_register_cross_encoding.py`

## Scope

This note records the next bounded artifact for the native taste-qubit
teleportation lane: three independently chosen encodings for the input,
Alice's Bell-resource half, and Bob's Bell-resource half.

```text
A = Alice unknown input encoding
R = Alice Bell-resource-half encoding
B = Bob Bell-resource-half encoding
```

The audited surface remains the Kogut-Susskind cell/taste factorization:

```text
C^(side^dim) = C^((side/2)^dim cells) tensor C^(2^dim tastes)
```

This remains ordinary quantum state teleportation only.  It does not claim
matter teleportation, mass transfer, charge transfer, energy transfer, object
transport, or faster-than-light signaling.

## Map Requirements

The two-register cross-encoding artifact assumed Alice's input register and
Alice's resource half used the same encoding.  This runner removes that
assumption and classifies three requirements for each surveyed `(A, R, B)`
triple.

```text
A->R map:
  Needed when Alice's input support differs from Alice's resource-half support.
  The site-basis partial isometry is |0_R><0_A| + |1_R><1_A|.

Adapted Bell measurement:
  Needed when A/R require cross-register Bell pairing or when either A or R
  does not admit the current fixed last-axis pair-hop X as logical X.

R->B resource map:
  Needed when Alice's resource-half support differs from Bob's resource-half
  support.  The intended first-artifact logical coefficient map is identity;
  the site-basis partial isometry is |0_B><0_R| + |1_B><1_R|.
```

The intended surface uses canonical logical Pauli operators in each ordered
logical basis, an explicit A/R Bell pairing, an identity logical resource map,
and axis-adapted Bob corrections.  The failure controls remove one requirement
at a time.

## Default Run

Command:

```bash
python3 scripts/frontier_teleportation_three_register_cross_encoding.py
```

Default audit surface:

```text
dimensions: 1, 2, 3
side lengths: 2, 4
valid KS geometries: 6
encoding supports: 131
possible A/R/B triples: 890633
surveyed A/R/B triples: 1609
random trials per surveyed triple: 4
max triples per geometry: 512
tolerance: 1e-12
```

Geometry counts:

```text
dim=1 side=2: 1 encodings, 1/1 triples surveyed
dim=1 side=4: 2 encodings, 8/8 triples surveyed
dim=2 side=2: 4 encodings, 64/64 triples surveyed
dim=2 side=4: 16 encodings, 512/4096 triples surveyed
dim=3 side=2: 12 encodings, 512/1728 triples surveyed
dim=3 side=4: 96 encodings, 512/884736 triples surveyed
```

Requirement classification over the surveyed triples:

```text
A input -> R Alice-resource-half:
  no site conversion needed: 330
  explicit A->R site maps needed: 1279
  in-cell retaste: 809
  relocation plus retaste: 391
  relocation only, same taste pair: 79

R Alice-resource-half -> B Bob-resource-half:
  no site conversion needed: 321
  explicit R->B resource site maps needed: 1288
  in-cell retaste: 807
  relocation plus retaste: 387
  relocation only, same taste pair: 94

Bell-measurement adaptation:
  cross-register A/R Bell pairing required: 1279
  axis-adapted Bell X required: 1267
  adapted Bell measurement required by either condition: 1485
  fixed last-axis Bell X sufficient: 342

Combined site maps:
  no A->R or R->B site maps needed: 131
  both A->R and R->B site maps needed: 1089
  max partial-isometry error: 0.000e+00
```

## Numerical Results

Axis-adapted three-register maps:

```text
teleportation/no-signaling pass: 1609/1609
minimum corrected-state fidelity: 0.9999999999999996
maximum infidelity: 6.661e-16
max branch probability error from 1/4: 2.220e-16
max total probability error from 1: 8.882e-16
max Bob trace distance to I/2 before Alice measurement: 4.441e-16
max Bob trace distance to I/2 after Alice measurement before message: 4.163e-16
max pairwise pre-message Bob-state distance across inputs: 4.718e-16
max corrected-state trace error: 2.220e-16
Bell outcomes seen: Phi+, Phi-, Psi+, Psi-
```

Missing A->R conversion control:

```text
expected pass cases: 330/1609
teleportation/no-signaling pass: 330/330 run
skipped before teleportation: 1279
failure cause: missing_explicit_a_to_r_site_conversion=1279
minimum corrected-state fidelity on runnable cases: 0.9999999999999998
maximum infidelity on runnable cases: 6.661e-16
```

Non-adapted Bell-measurement control:

```text
expected pass cases: 342/1609
teleportation/no-signaling pass: 342/342 run
skipped before teleportation: 1267
failure causes:
  a_and_r_bell_x_not_axis_adapted=673
  a_bell_x_not_axis_adapted=282
  r_bell_x_not_axis_adapted=312
minimum corrected-state fidelity on runnable cases: 0.9999999999999996
maximum infidelity on runnable cases: 6.661e-16
```

Non-adapted Bob-correction control:

```text
expected pass cases: 642/1609
teleportation/no-signaling pass: 642/1609
failure cause: bob_fixed_pairhop_x_zero_on_encoding=967
minimum corrected-state fidelity: 0.0000000000000000
maximum infidelity: 1.000e+00
max corrected-state trace error: 1.000e+00
Bob pre-message input-independence still holds to 5.274e-16
```

Wrong B resource-conversion control:

```text
expected pass cases: 0/1609
teleportation/no-signaling pass: 0/1609
failure cause: wrong_b_resource_conversion_map=1609
minimum corrected-state fidelity: 0.0000000134850124
maximum infidelity: 1.000e+00
max corrected-state trace error: 2.220e-16
Bob pre-message input-independence still holds to 4.996e-16
```

The runner reported `PASS` for:

- axis-adapted three-register maps;
- all four Bell outcomes represented;
- Bob pre-message reduced-state input-independence;
- missing A->R conversion control;
- non-adapted Bell-measurement boundary;
- non-adapted Bob-correction control;
- wrong B resource-conversion control.

## Interpretation

Within the bounded default survey, the obstruction is not three-register
cross-encoding itself.  The intended logical protocol passes when the A/R Bell
measurement is explicitly adapted to the two Alice-side encodings and Bob's
corrections are adapted to Bob's chosen encoding.

The first new requirement is A->R Bell pairing.  If Alice's unknown input and
Alice's resource half occupy different encoded site supports, the Bell
measurement needs an explicit site partial isometry to define which ordered
logical basis states are paired.

The second requirement is Bell-measurement adaptation.  The current fixed
pair-hop X remains a last-axis convention.  It is sufficient only when both A
and R use encodings where the fixed pair-hop restricts to logical X.

The third requirement is the R->B resource map.  If R and B differ, the Bell
resource must be prepared with the matching site partial isometry.  The wrong
B-side bit-swap control shows that Bob can still see an input-independent
pre-message state while post-message fidelity fails.

## Limitations

This is a finite algebraic audit over dimensions 1, 2, and 3 with side lengths
2 and 4 by default.  The three-register product is capped at 512 triples per
geometry, so the default run is a deterministic bounded survey, not an
exhaustive survey of all 890633 possible default triples.  Use
`--max-triples-per-geometry 0` for exhaustive triples when the requested
geometry set is small enough.

Odd side lengths remain outside the audited KS cell/taste factorization.
Larger even lattices can be requested but are not claimed by the default run.

The Bell resource, Bell measurement, conversion maps, and Bob corrections are
ideal logical objects.  The runner does not derive a physical resource
preparation channel, measurement apparatus, durable record, Hamiltonian
transport, noise model, or readout model.
