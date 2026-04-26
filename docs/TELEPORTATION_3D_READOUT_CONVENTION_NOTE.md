# Teleportation 3D Readout Convention Audit

**Date:** 2026-04-26
**Status:** planning / first artifact; not a promotion claim
**Runner:** `scripts/frontier_teleportation_3d_readout_convention_audit.py`

## Scope

This note records a focused 3D audit of retained-axis logical `Z_r` versus raw
sublattice parity

```text
xi_5 = Z_x Z_y Z_z.
```

For a retained taste axis `r`, the traced operational readout lane requires

```text
Z_traced = Z_r tensor I_spectator,
```

with cells and the two other taste axes in the traced environment. Raw `xi_5`
instead equals

```text
xi_5 = Z_r * product_{a != r} Z_a.
```

It is therefore a signed logical `Z_r` only after fixing spectator taste bits.
It is not the traced retained-bit `Z` operator.

This remains ordinary quantum state teleportation planning only. It does not
claim matter teleportation, mass transfer, charge transfer, energy transfer,
object transport, or faster-than-light signaling.

## Command

```bash
python3 -m py_compile scripts/frontier_teleportation_3d_readout_convention_audit.py
python3 scripts/frontier_teleportation_3d_readout_convention_audit.py
```

Both commands completed successfully.

Default settings:

```text
dim = 3
sides = 2,4
retained axes = x,y,z
tolerance = 1e-12
```

## Operator Summary

The audit factors each single-register operator against
`O_logical tensor I_env`, where `env = cells + spectator taste bits`.

| surface | retained axis | envs | `Z_r` | `X_r` | raw `xi_5` as traced `Z` | raw `xi_5` rel residual | raw `xi_5` expected error | fixed-branch max error | retained Bell4 | raw-`xi_5` Bell4 | raw Bell max rel |
| --- | ---: | ---: | --- | --- | --- | ---: | ---: | ---: | --- | --- | ---: |
| `3D side=2` | x | 4 | PASS | PASS | FAIL | `1.000000` | `1.000000` | `0` | PASS | FAIL | `0.707107` |
| `3D side=2` | y | 4 | PASS | PASS | FAIL | `1.000000` | `1.000000` | `0` | PASS | FAIL | `0.707107` |
| `3D side=2` | z | 4 | PASS | PASS | FAIL | `1.000000` | `1.000000` | `0` | PASS | FAIL | `0.707107` |
| `3D side=4` | x | 32 | PASS | PASS | FAIL | `1.000000` | `1.000000` | `0` | PASS | FAIL | `0.707107` |
| `3D side=4` | y | 32 | PASS | PASS | FAIL | `1.000000` | `1.000000` | `0` | PASS | FAIL | `0.707107` |
| `3D side=4` | z | 32 | PASS | PASS | FAIL | `1.000000` | `1.000000` | `0` | PASS | FAIL | `0.707107` |

Interpretation:

- every retained-axis `Z_r` factors exactly as logical `Z tensor I_env`;
- every retained-axis `X_r` factors exactly as logical `X tensor I_env`;
- raw `xi_5` fails traced retained-axis `Z` factorization for all retained
  axes, with relative residual `1.000000`;
- the averaged logical candidate for raw `xi_5` differs from retained `Z` by
  expected error `1.000000`;
- fixed-branch restrictions of raw `xi_5` have zero error once spectator bits
  are fixed.

## Fixed-Branch Sign Table

For each retained axis, the spectator sign is

```text
s_branch = (-1)^(sum spectator bits).
```

Thus

```text
xi_5 | fixed spectators = s_branch * Z_r.
```

The sign table is the same for side 2 and side 4. Side 2 has one cell/env per
spectator sector; side 4 has eight cell/env labels per spectator sector.

| retained axis | spectator axes | spectator bits | sign | side=2 envs | side=4 envs | max error |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| x | yz | 00 | `+1` | 1 | 8 | `0` |
| x | yz | 01 | `-1` | 1 | 8 | `0` |
| x | yz | 10 | `-1` | 1 | 8 | `0` |
| x | yz | 11 | `+1` | 1 | 8 | `0` |
| y | xz | 00 | `+1` | 1 | 8 | `0` |
| y | xz | 01 | `-1` | 1 | 8 | `0` |
| y | xz | 10 | `-1` | 1 | 8 | `0` |
| y | xz | 11 | `+1` | 1 | 8 | `0` |
| z | xy | 00 | `+1` | 1 | 8 | `0` |
| z | xy | 01 | `-1` | 1 | 8 | `0` |
| z | xy | 10 | `-1` | 1 | 8 | `0` |
| z | xy | 11 | `+1` | 1 | 8 | `0` |

This is the valid fixed-branch Pauli statement. It is not a traced-operator
statement unless the spectator branch is explicitly measured, retained, and
fed into branch-conditioned corrections.

## Bell Projector Consequence

For every audited side and retained axis:

```text
Bell projectors from retained-axis Z_r/X_r:
  4/4 PASS
  max relative residual = 0
  max expected error = 0

Bell projectors with raw xi_5 substituted for Z_r:
  4/4 FAIL
  max relative residual = 0.707107
  max expected error = 0.250000
```

The raw-`xi_5` Bell control fails because the `ZZ` and `ZX tensor ZX` terms
retain spectator signs. A traced Bell measurement must be built from
retained-axis `Z_r` and retained-axis `X_r`, or else the script must explicitly
model spectator measurement/heralding and branch-conditioned correction.

## Acceptance Gates

The default run reports `PASS` for:

- 3D side 2 and side 4 surfaces audited;
- all retained-axis `Z_r` operators factor as `O_logical tensor I_env`;
- all retained-axis `X_r` operators factor as `O_logical tensor I_env`;
- raw `xi_5` fixed-branch restrictions are signed logical `Z`;
- raw `xi_5` fails traced retained-axis `Z` factorization in 3D;
- retained-axis Bell projectors pass as traced Bell measurements;
- raw `xi_5` Bell projectors fail as traced Bell measurements.

## Recommended Guard Language

Future 3D teleportation scripts should keep these labels separate:

```text
fixed_branch_z:
  raw xi_5 restricted to an explicit spectator branch; track the branch sign.

traced_operator_z:
  retained-axis Z_r tensor I_spectator for 3D readout/correction.

native_xi5_as_traced_z:
  reject in 3D unless an environment measurement/heralding workflow and
  branch-conditioned correction rule are supplied.

bell_projectors:
  build traced Bell measurements from retained-axis Z_r and X_r.
```

Suggested pass/fail wording:

```text
PASS fixed-branch Z restriction: xi_5 -> +/- Z_r on this spectator branch.
PASS traced retained-axis Z: Z_r factors as O_logical tensor I_env.
FAIL raw xi_5 as traced Z in 3D: spectator taste signs remain.
FAIL raw xi_5 Bell projector as traced Bell measurement: spectator signs remain.
```

## Limitations

- This is a finite side 2 / side 4 operator audit, not a continuum result.
- It is not a hardware readout design, pulse sequence, noise model, or
  fault-tolerant measurement primitive.
- It does not provide a 3D Poisson resource or a 3D end-to-end teleportation
  resource result.
- Raw `xi_5` remains valid for explicitly fixed spectator-branch algebra when
  the branch sign is carried as data.
- A deterministic traced raw-`xi_5` workflow would need an explicit
  environment measurement/heralding model, branch-conditioned operations, and
  a postselection or success-probability accounting.
