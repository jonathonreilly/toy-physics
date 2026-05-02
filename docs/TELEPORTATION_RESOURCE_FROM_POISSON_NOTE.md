# Teleportation Resource From Poisson/CHSH: First Audit

Status: planning / first artifact. This note records a narrow audit of whether
the existing Poisson-driven CHSH lane already yields an encoded two-qubit Bell
resource for ordinary quantum state teleportation.

It does not claim matter teleportation, charge transfer, mass transfer, or
faster-than-light transport. The only audited object is a quantum state
teleportation resource extracted from the two-species ground state used by
`scripts/frontier_bell_inequality.py`.

## Script

New runner:

```bash
python3 scripts/frontier_teleportation_resource_from_poisson.py
```

The runner imports the existing Poisson/CHSH machinery, builds the small
ground-state cases, and then extracts a candidate resource as follows:

1. Use the Kogut-Susskind cell/taste factorization already used in the CHSH
   lane.
2. Keep the last taste bit of each species as the logical qubit.
3. Trace over cells and spectator taste bits to get a deterministic two-qubit
   logical resource.
4. Separately scan fixed-environment postselected branches as diagnostics only.
5. Measure Bell overlap, two-qubit CHSH, purity, negativity, and standard
   teleportation fidelity for random input states.

The script also checks the Bell teleportation convention against an ideal
`Phi+` resource before running the Poisson cases.

## Default Run Results

Command:

```bash
python3 scripts/frontier_teleportation_resource_from_poisson.py
```

Protocol sanity:

- Ideal `Phi+` resource mean fidelity: `0.9999999999999996`
- Ideal `Phi+` resource minimum fidelity: `0.9999999999999991`
- Maximum output trace error: `5.551e-16`

| case | full CHSH | traced Bell overlap | traced CHSH | negativity | standard teleportation fidelity | deterministic high-fidelity resource |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `1d_null`, `G=0` | `2.000000` | `0.500000` (`Psi+`) | `2.000000` | `0.000000` | mean `0.669817`, min `0.500038`, max `0.987949` | no |
| `1d_poisson_chsh`, `G=1000` | `2.822668` | `0.997963` (`Phi+`) | `2.822668` | `0.497963` | mean `0.998621`, min `0.997964`, max `0.999470` | yes |
| `2d_poisson_chsh`, `G=1000` | `2.668376` | `0.970283` (`Phi+`) | `2.745662` | `0.470283` | mean `0.979360`, min `0.970287`, max `0.999810` | yes |

Postselected diagnostic branches:

| case | best branch Bell overlap | probability | branch CHSH | branch negativity |
| --- | ---: | ---: | ---: | ---: |
| `1d_null` | `0.500000` (`Psi+`) | `6.250000e-02` | `2.000000` | `0.000000` |
| `1d_poisson_chsh` | `0.998981` (`Phi+`) | `2.497454e-01` | `2.825546` | `0.498981` |
| `2d_poisson_chsh` | `0.999428` (`Psi+`) | `5.854540e-08` | `2.826809` | `0.499428` |

## Interpretation

The `G=0` null case does not produce an entangled Bell resource under this
extraction: the best Bell overlap is `0.500000` and negativity is zero.

The two audited Poisson/CHSH cases are positive on the deterministic traced
logical resource: both exceed the script's `0.90` Bell-overlap threshold and
both give high standard teleportation fidelity in the ideal Bell-measurement
protocol. This is stronger than merely observing a full-state CHSH violation.

The postselected branches are not promoted as resources here. They are useful
diagnostics, but a postselection scan is not a deterministic resource
preparation protocol.

## Limitation Status

The limitation has moved, but it is not closed.

Previous limitation: no Poisson-resource derivation artifact for teleportation.

Current status: small-surface positive first artifact. The existing Poisson/CHSH
ground-state machinery can yield a high-fidelity encoded two-qubit resource on
the audited `1D N=8` and `2D 4x4` cases after tracing to the last taste bit per
species.

Still open before promotion:

- Harden beyond the two small default surfaces.
- Check mass, coupling, dimension, boundary, and degeneracy sensitivity.
- Add a native preparation/readout story for the logical resource, not only an
  offline ground-state extraction.
- Separate deterministic traced extraction from diagnostic postselection.
- Keep the claim restricted to quantum state teleportation.
