# Gauge-Scalar Bridge 3+1 Native Tube Staging Gate

**Date:** 2026-05-03
**Claim type:** open_gate
**Status:** open staging gate for the L_s=2 APBC spatial-cube
tensor-transfer Perron solve. This note records reproducible
K-plaquette tube Perron data and names the remaining cube-geometry
calculation; it does not establish a new lower-bound theorem, parent
promotion, or audit-ratified effective status.
**Primary runner:** `scripts/frontier_gauge_scalar_bridge_3plus1_native_tube_staging.py`
**Gate target:** the observable-level residual isolated by
[`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md)
and the stretch attempt
[`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md).

## 0. Headline

The runner computes a controlled tube-family probe for the native
3+1 gauge-scalar bridge program. It does four useful things:

1. Reproduces the two existing reference Perron solves on the
   V-invariant minimal block:
   `P_delta(6) = 0.4225317396` and `P_rho=1(6) = 0.4524071590`.
2. Computes the K-plaquette tube family at `beta_env = 6` for `k = 0..6`.
3. Verifies NMAX convergence for the `k = 1` tube value with drift
   `1.329e-9` between `NMAX = 6` and `NMAX = 7`.
4. Names the exact remaining closure target: the L_s=2 APBC spatial-cube
   boundary character measure `rho_(p,q)(6)` for the actual five
   unmarked plaquettes, not a tube ansatz.

The tube values are staging data. They are not a strict lower bound for
the physical cube because the cube has a specific finite geometry and
need not equal or dominate any tube member.

## 1. Dependencies And Inputs

This gate uses only framework-internal or already named support inputs:

- [`GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md):
  source-sector factorization
  `T_src(6) = exp(3J) D_6^loc C_(Z_6^env) exp(3J)`.
- [`GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md):
  reference solves for `rho = delta` and `rho = 1`, plus the obstruction
  that the Wilson coefficients and SU(3) intertwiners alone do not
  determine the physical `rho_(p,q)(6)`.
- [`GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md):
  identifies the spatial-environment boundary data as the Perron state
  of a finite positive tensor-transfer operator, with the full beta=6
  evaluation explicitly out of scope there.
- [`GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md):
  supplies the bridge-support upper candidate `0.593530679977098`; this
  note does not rederive that value.
- [`GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md`](GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md):
  consumer context for the observable bridge; this note does not change
  its status.

Forbidden imports remain excluded: no PDG plaquette value, no lattice-MC
plaquette value as a derivation input, no fitted `beta_eff`, no
perturbative beta-function bridge as derivation, and no same-surface
family argument.

## 2. Runner Results

### 2.1 Reference Solves

| reference | environment | P(6) |
|---|---|---:|
| B | `rho = delta` | `0.4225317396` |
| A | `rho = 1` | `0.4524071590` |

The strict native floor remains the existing `rho = delta` reference.
The tube family does not replace it.

### 2.2 K-Plaquette Tube Probe

For

```text
rho_k(p,q) = (c_(p,q)(6) / c_(0,0)(6))^k
```

the runner obtains:

| k | P(6) | Perron eigenvalue |
|---:|---:|---:|
| 0 | `0.4524071590` | `3.812630` |
| 1 | `0.4594237929` | `3.915306` |
| 2 | `0.4678430800` | `4.047790` |
| 3 | `0.4777615094` | `4.219099` |
| 4 | `0.4891802187` | `4.441077` |
| 5 | `0.5019552672` | `4.729211` |
| 6 | `0.5157590249` | `5.103608` |

Tube span over `k = 0..6`: `0.0633518659`.

### 2.3 NMAX Convergence

For `k = 1`:

| NMAX | P(6) |
|---:|---:|
| 3 | `0.459032827025` |
| 4 | `0.459414804723` |
| 5 | `0.459423660967` |
| 6 | `0.459423791566` |
| 7 | `0.459423792895` |

The drift from `NMAX = 6` to `NMAX = 7` is `1.329e-9`.

## 3. What This Gate Does Not Establish

- No new strict lower bound above `0.4225317396`.
- No theorem that the L_s=2 APBC spatial cube lies inside the tube range.
- No parent theorem promotion or status change.
- No quantitative bypass of the no-go witness.
- No use of the rejected K-Z external-lift PR as a dependency or authority.

The existing support envelope from the reference floor and bridge-support
upper candidate is

```text
[0.4225317396, 0.5935306800]
```

with width approximately `0.170999`. That is far wider than the no-go
witness scale `epsilon_witness ~= 3.03e-4`, so this staging gate does
not close the observable bridge.

## 4. Closure Target

The next required computation is exact and finite:

```text
Compute rho_(p,q)(6) for the unmarked 3D Wilson environment on the
L_s = 2 APBC spatial cube with one marked plaquette and five unmarked
plaquettes in their actual geometry.
```

The ingredients are already named: Wilson character coefficients from
Bessel determinants, SU(3) fusion/intertwiner data, and the explicit
cube link/plaquette incidence pattern. The current runner intentionally
does not perform that cube solve.

## 5. Audit Handling

This note should seed an `open_gate` claim row. The independent audit
lane owns any verdict and effective status. Review-loop has only checked
that the staging data are reproducible, scoped, dependency-linked, and
not promoted into theorem authority.

## 6. Command

```bash
python3 scripts/frontier_gauge_scalar_bridge_3plus1_native_tube_staging.py
```

Expected summary:

```text
SUMMARY: STAGING PASS=4 SUPPORT=1 FAIL=0
```
