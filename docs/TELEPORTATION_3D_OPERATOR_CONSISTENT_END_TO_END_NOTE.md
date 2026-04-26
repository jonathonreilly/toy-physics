# 3D Operator-Consistent End-To-End Teleportation Audit

**Date:** 2026-04-26
**Status:** planning / first artifact; not a promotion claim
**Runner:** `scripts/frontier_teleportation_3d_operator_consistent_end_to_end.py`

## Scope

This note records the first 3D retained-axis operator-consistent end-to-end
audit for the Poisson-backed taste-qubit teleportation lane.

The audited convention is unchanged from the 1D/2D operator-consistent runner:

```text
3D single-particle site Hilbert space
  -> retained logical qubit = last KS taste bit
  -> environment = cells + spectator taste bits
  -> allowed traced logical operators factor as O_logical tensor I_env
```

The runner uses retained-axis logical `Z/X` for traced readout, Bell
measurement, and Bob correction. Raw sublattice parity `Z=xi_5` is included
only as a 3D rejection control.

This remains ordinary quantum state teleportation planning only. It does not
claim matter teleportation, mass transfer, charge transfer, energy transfer,
object transport, or faster-than-light signaling.

## Command

```bash
python3 -m py_compile scripts/frontier_teleportation_3d_operator_consistent_end_to_end.py
python3 scripts/frontier_teleportation_3d_operator_consistent_end_to_end.py
```

Both commands completed successfully.

Default settings:

```text
3D side = 2 (N=8 sites, dense N^2=64 two-particle Hamiltonian)
mass = 0
candidate non-null coupling G = 1000
input probes = 134 states (six Pauli-axis probes + 128 random, seed=20260425)
fidelity threshold = 0.900
protocol tolerance = 1e-10
operator tolerance = 1e-12
```

## Operator-Consistency Guards

| surface | retained axis | sites | envs | retained-axis `Z` | retained-axis `X` | retained-axis Bell projectors | raw `xi_5` as `Z` | raw-`Z` Bell projectors |
| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| `3D side=2` | 2 | 8 | 4 | PASS | PASS | PASS | FAIL | FAIL |

Raw-control residuals:

| control | relative residual | expected error |
| --- | ---: | ---: |
| raw `xi_5` as retained-bit `Z` | `1.000000` | `1.000000` |
| raw-`Z`/fixed-`X` Bell projectors | `0.707107` max | `0.250000` max |

Interpretation: retained-axis logical `Z/X` satisfy the traced
`O_logical tensor I_env` condition in this 3D case. Raw `xi_5` is rejected as
a traced retained-bit `Z`, including inside Bell projectors.

## End-To-End Rows

The default 3D positive Poisson case lands in the `Psi+` Bell frame. The fixed
`Phi+` protocol row is therefore an honest failure. A known Bob-side retained
logical `X` frame, followed by the standard retained-axis `Z^z X^x`
feed-forward correction, maps the resource to the `Phi+` frame and passes.

| case | frame | raw best Bell | framed best Bell | `Phi+` overlap | exact `F_avg` | sampled min fidelity | min conditional branch fidelity | Bob pre-record pairwise distance | outcomes | pass |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `3d_side2_null` | fixed `Phi+` | `0.500000` (`Psi+`) | `0.500000` (`Psi+`) | `0.500000` | `0.666667` | `0.500000` | `0.006062` | `2.776e-16` | 4 | no |
| `3d_side2_poisson_G1000_m0` | fixed `Phi+` | `0.997724` (`Psi+`) | `0.997724` (`Psi+`) | `0.002276` | `0.334850` | `0.002276` | `0.000017` | `2.498e-16` | 4 | no |
| `3d_side2_poisson_G1000_m0` | `Psi+ -> Phi+` | `0.997724` (`Psi+`) | `0.997724` (`Phi+`) | `0.997724` | `0.998483` | `0.997724` | `0.997719` | `2.498e-16` | 4 | yes |

Additional resource diagnostics for the non-null `G=1000` case:

```text
ground energy = -114.870237352
full-state CHSH = 2.809224
logical CHSH = 2.821998
negativity = 0.497724
Bob marginal bias from I/2 = 4.764e-02
```

## No-Signaling And Causal Record Checks

Bob pre-message input-independence remained clean for all runnable rows:

```text
3d_side2_null fixed Phi+: distance to resource marginal = 4.475e-16, pairwise input distance = 2.776e-16
3d_side2_poisson_G1000_m0 fixed Phi+: distance to resource marginal = 4.163e-16, pairwise input distance = 2.498e-16
3d_side2_poisson_G1000_m0 Psi+->Phi+: distance to resource marginal = 4.163e-16, pairwise input distance = 2.498e-16
```

All four Bell outcomes were represented in every runnable row:

```text
Phi+, Phi-, Psi+, Psi-
```

The passing 3D framed row kept the directed classical record clean:

```text
delivered record = Psi+
early delivery blocked = True
delivered once = True
delivered-branch fidelity = 0.998841
```

## Acceptance Gates

The default run reported `PASS` for:

- 3D retained-axis operator guard passes;
- 3D raw `xi_5` as traced retained-bit `Z` rejects;
- 3D raw `xi_5` Bell controls reject;
- 3D null rows do not pass the high-fidelity protocol;
- 3D non-null retained-axis resource has a passing row;
- fixed `Phi+` frame failures are reported when the resource lands elsewhere;
- Bob pre-message input-independence is clean for runnable rows;
- all four Bell outcomes are represented for runnable rows;
- causal two-bit record remains clean for passing rows.

## Limitations

- The default 3D resource is the dense-diagonalized `side=2` case only
  (`N=8`, two-particle dimension `64`). Larger 3D surfaces are not promoted by
  this artifact.
- The positive `G=1000` resource is high fidelity only after accounting for
  its known `Psi+` Bell frame with a Bob-side retained-axis `X` frame. The
  fixed `Phi+` row fails and is intentionally kept in the table.
- Bell measurement, feed-forward, and Bob correction are ideal retained-logical
  operations, not a physical apparatus derivation.
- Raw `xi_5` rejection is an operator-factorization control. It is not a
  detector, pulse sequence, or hardware readout model.
- No matter, charge, mass, energy, or object is teleported. Only an unknown
  quantum state on Bob's already-present encoded taste qubit is reconstructed
  after Bob receives Alice's classical Bell record.
