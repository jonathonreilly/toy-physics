# Teleportation Preparation/Readout Probe

Status: bounded diagnostic. This note separates the offline Poisson-derived
teleportation resource extraction documented in
[`TELEPORTATION_RESOURCE_FROM_POISSON_NOTE.md`](TELEPORTATION_RESOURCE_FROM_POISSON_NOTE.md)
from a plausible preparation/readout protocol.
It does not claim dynamic cooling, adiabatic preparation, deterministic branch
selection, matter transfer, charge transfer, mass transfer, or faster-than-light
transport.

## Script

Runner:

```bash
python3 scripts/frontier_teleportation_preparation_readout_probe.py
```

The runner reuses
[`TELEPORTATION_RESOURCE_FROM_POISSON_NOTE.md`](TELEPORTATION_RESOURCE_FROM_POISSON_NOTE.md)
and `scripts/frontier_teleportation_resource_from_poisson.py` as context and
adds preparation/readout-facing diagnostics:

1. Fully diagonalize each small default Hamiltonian and report ground-state
   multiplicity and gap to the next distinct eigenvalue.
2. Report simple ground-manifold projection probabilities from an origin-pair
   state, a uniform pair state, and the best localized site-pair.
3. Keep the previous deterministic traced logical resource extraction: keep the
   last Kogut-Susskind taste bit per species and trace cells/spectator tastes.
4. Separately scan fixed-environment postselected branches and report success
   probabilities, expected attempts, and branch quality.
5. Emit an explicit verdict that preparation/readout is not demonstrated.

## Commands Run

```bash
python3 -m py_compile scripts/frontier_teleportation_preparation_readout_probe.py
python3 scripts/frontier_teleportation_preparation_readout_probe.py
```

Both commands completed successfully.

Protocol sanity check for an ideal `Phi+` resource:

- mean fidelity: `0.9999999999999996`
- minimum fidelity: `0.9999999999999991`
- maximum trace error: `5.551e-16`

## Spectral And Projection Diagnostics

| case | ground multiplicity | gap to next distinct | origin-pair ground projection | uniform-pair ground projection | best localized site-pair projection |
| --- | ---: | ---: | ---: | ---: | ---: |
| `1d_null`, `G=0` | `1` | `5.857864e-01` | `0.015625` | `1.000000` | `0.015625` |
| `1d_poisson_chsh`, `G=1000` | `1` | `1.868323e-02` | `1.645024e-18` | `0.141330` | `0.124745` |
| `2d_poisson_chsh`, `G=1000` | `1` | `2.463780e-01` | `1.675112e-11` | `0.145230` | `0.058802` |

The default small cases are nondegenerate under the script tolerance. That is
helpful but not a preparation protocol: the projection numbers only quantify
overlap with the offline ground subspace from simple reference states.

## Deterministic Traced Resource

| case | full-state CHSH | traced Bell overlap | traced CHSH | negativity | teleportation mean fidelity | offline traced resource |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `1d_null` | `2.000000` | `0.500000` (`Psi+`) | `2.000000` | `0.000000` | `0.669817` | no |
| `1d_poisson_chsh` | `2.822668` | `0.997963` (`Phi+`) | `2.822668` | `0.497963` | `0.998621` | yes |
| `2d_poisson_chsh` | `2.668376` | `0.970283` (`Phi+`) | `2.745662` | `0.470283` | `0.979360` | yes |

The Poisson cases remain positive as offline traced-resource diagnostics. The
deterministic trace has mathematical success probability `1`, but this is not a
readout primitive by itself. It assumes the logical taste qubits can be
addressed while the environment is ignored.

## Fixed-Environment Postselection

| case | best-fidelity branch | best branch probability | expected attempts | most-likely branch | most-likely probability | high-fidelity branch mass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `1d_null` | `0.500000` (`Psi+`) | `0.062500` | `16` | `0.500000` (`Psi+`) | `0.062500` | `0` |
| `1d_poisson_chsh` | `0.999984` (`Psi+`) | `2.056839e-13` | `4.86183e+12` | `0.998981` (`Phi+`) | `0.249745` | `0.998982` |
| `2d_poisson_chsh` | `0.999428` (`Psi+`) | `5.854540e-08` | `1.70808e+07` | `0.984720` (`Phi+`) | `0.119428` | `1.000000` |

The postselected branches are diagnostics only. The best-fidelity branch can be
very rare, and even large aggregate high-fidelity branch mass does not specify a
physical environment measurement, heralding workflow, or post-measurement
logical operation.

## Remaining Preparation/Readout Limitations

- No dynamic cooling, adiabatic path, or schedule is constructed.
- A finite spectral gap is reported, but no runtime, control Hamiltonian, or
  robustness estimate follows from the probe.
- Ground-manifold projection probabilities are overlaps from simple references,
  not implemented projective preparation.
- The deterministic traced resource is a reduced density matrix, not a physical
  extraction/readout operation.
- Fixed-environment postselection needs an explicit environment measurement and
  heralding cost model before it can be promoted.
- The encoded Bell measurement, classical feed-forward, and Bob correction on
  the logical taste qubit remain assumed ideal operations.
- The result is still small-surface only and needs mass, coupling, boundary,
  dimension, and scaling hardening.

Bottom line: the offline Poisson-derived resource survives this diagnostic on
the default Poisson cases, but preparation/readout remains open.
