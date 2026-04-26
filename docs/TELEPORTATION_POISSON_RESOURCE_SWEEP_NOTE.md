# Teleportation Poisson-Resource Sweep: Bounded Hardening

Status: planning / first artifact. This note records a bounded parameter sweep
of the Poisson-derived encoded two-qubit resource audited in
`scripts/frontier_teleportation_resource_from_poisson.py`.

The scope is ordinary quantum state teleportation only. It does not claim
matter teleportation, charge transfer, mass transfer, energy transfer, or
faster-than-light transport.

## Script

New runner:

```bash
python3 scripts/frontier_teleportation_poisson_resource_sweep.py
```

The runner reuses the existing Poisson/CHSH ground-state construction and the
same deterministic extraction:

1. build the two-species Poisson-coupled ground state;
2. keep the last Kogut-Susskind taste bit of each species as the logical qubit;
3. trace over cells and spectator taste bits;
4. measure best Bell overlap, `Phi+` overlap, exact fixed-protocol average
   teleportation fidelity, full-state CHSH, logical-resource CHSH, purity, and
   negativity;
5. scan fixed-environment postselected branches only as diagnostics.

The fixed-protocol average fidelity is reported from the `Phi+` overlap:

```text
F_avg = (1 + 2 * <Phi+|rho|Phi+>) / 3
```

This keeps the deterministic teleportation claim separate from the best Bell
label and from postselected branches.

## Default Sweep

Command:

```bash
python3 scripts/frontier_teleportation_poisson_resource_sweep.py
```

Default grid:

- surfaces: `1d_N8`, `2d_4x4`
- masses: `0`, `0.1`, `0.5`, `1`
- Poisson couplings: `0`, `1`, `10`, `50`, `100`, `500`, `1000`
- random sampled teleportation probes per row: `64`

Thresholds:

- best Bell overlap: `>= 0.900`
- exact fixed-protocol average fidelity: `>= 0.900`
- CHSH violation counted as `S > 2.001`
- negativity counted as `> 1e-10`

Protocol sanity check against the ideal `Phi+` resource:

- sampled mean fidelity: `0.9999999999999996`
- sampled minimum fidelity: `0.9999999999999991`
- maximum trace error: `5.551e-16`

## Threshold Summary

The table reports the first `G` value in the default grid where each threshold
is met. `none` means the threshold was not met on that surface and mass.

| surface | mass | Bell* >= 0.9 | F_avg >= 0.9 | F_avg > 2/3 | full CHSH > 2.001 | logical CHSH > 2.001 | neg > 0 | high-resource pass |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `1d_N8` | `0.00` | `500` | `100` | `10` | `50` | `50` | `10` | `500` |
| `1d_N8` | `0.10` | none | none | `10` | `50` | `50` | `10` | none |
| `1d_N8` | `0.50` | none | none | `10` | `500` | `500` | `10` | none |
| `1d_N8` | `1.00` | none | none | `10` | none | none | `10` | none |
| `2d_4x4` | `0.00` | `500` | `500` | `50` | `500` | `50` | `1` | `500` |
| `2d_4x4` | `0.10` | `1000` | `500` | `50` | `500` | `50` | `1` | `1000` |
| `2d_4x4` | `0.50` | none | none | `50` | `500` | `100` | `10` | none |
| `2d_4x4` | `1.00` | none | none | `50` | none | none | `50` | none |

Here `high-resource pass` means:

- best Bell label is `Phi+`;
- best Bell overlap is at least `0.900`;
- exact fixed-protocol `F_avg` is at least `0.900`;
- negativity is above `1e-10`.

## High-Resource Rows

The deterministic high-resource threshold passed on `5/48` non-null rows:

| surface | mass | G | best Bell overlap | F_avg | full CHSH | logical CHSH | negativity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `1d_N8` | `0.00` | `500` | `0.991988` | `0.994659` | `2.805789` | `2.805789` | `0.491988` |
| `1d_N8` | `0.00` | `1000` | `0.997963` | `0.998642` | `2.822668` | `2.822668` | `0.497963` |
| `2d_4x4` | `0.00` | `500` | `0.905991` | `0.937327` | `2.381922` | `2.576287` | `0.405991` |
| `2d_4x4` | `0.00` | `1000` | `0.970283` | `0.980189` | `2.668376` | `2.745662` | `0.470283` |
| `2d_4x4` | `0.10` | `1000` | `0.937343` | `0.958229` | `2.576927` | `2.651253` | `0.437343` |

Other non-null sweep counts:

- exact fixed-protocol `F_avg > 2/3`: `36/48`
- full-state CHSH violation: `16/48`
- logical-resource CHSH violation: `21/48`
- negativity-positive rows: `41/48`

Best observed values over non-null rows:

- best Bell overlap: `0.997963` at `1d_N8`, `m=0`, `G=1000`
- best fixed-protocol `F_avg`: `0.998642` at `1d_N8`, `m=0`, `G=1000`
- best full-state CHSH: `2.822668` at `1d_N8`, `m=0`, `G=1000`
- best logical-resource CHSH: `2.822668` at `1d_N8`, `m=0`, `G=1000`
- best negativity: `0.497963` at `1d_N8`, `m=0`, `G=1000`
- weakest high-resource pass by `F_avg`: `0.937327` at `2d_4x4`,
  `m=0`, `G=500`

## Null Controls

The `G=0` controls remain clean across all eight surface/mass rows:

- max full-state CHSH: `2.000000`
- max logical CHSH: `2.000000`
- max best Bell overlap: `0.500000`
- max exact fixed-protocol `F_avg`: `0.666667`
- max negativity: `5.210380e-16`
- high-resource passes: `0`
- CHSH violations above margin: `0`
- negativity hits above threshold: `0`

## Interpretation

The positive Poisson-resource result survives this bounded sweep as a
parameter-window result: high coupling and low mass produce deterministic
high-fidelity encoded Bell resources on the audited `1D N=8` and `2D 4x4`
surfaces.

It is not uniform. Higher mass and weaker coupling often fail the
high-resource threshold, even when the resource can still beat the classical
average-fidelity benchmark or show positive negativity. Full-state CHSH,
logical-resource CHSH, Bell overlap, and teleportation fidelity also do not
turn on at identical grid points, so CHSH alone is still not promoted as a
teleportation-resource derivation.

Postselected fixed-environment branches can have very high Bell overlap at
small probability in rows where the deterministic traced resource fails. Those
branches remain diagnostics only in this artifact.

## Limitation Status

The claim boundary remains strict:

- planning / first artifact;
- small bounded `1D/2D` parameter sweep only;
- deterministic traced encoded resource only;
- ordinary quantum state teleportation only;
- no matter, mass, charge, energy, or faster-than-light transport claim.

Within that boundary, the earlier positive Poisson-resource result survives
the bounded sweep as a non-uniform but real parameter window.
