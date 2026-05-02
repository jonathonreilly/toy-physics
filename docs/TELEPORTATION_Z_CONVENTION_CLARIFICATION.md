# Teleportation Logical Z Convention Clarification

**Date:** 2026-04-25
**Status:** claim-boundary clarification; not a new protocol result

## Scope

This note clarifies a narrow convention issue in the native taste-qubit
teleportation lane: when the raw sublattice parity operator

```text
Z_raw = xi_5
```

can be read as a logical `Z`, and when the traced operational readout lane must
instead use the retained-axis logical `Z`.

The distinction is between:

- fixed-branch or fixed-encoding restrictions, where a cell and spectator
  taste sector are selected before restricting the operator; and
- traced operational readout/correction, where cells and spectator tastes have
  been traced out and the implemented operator must act only on the retained
  logical bit.

This is ordinary encoded quantum-state teleportation bookkeeping. It does not
claim matter teleportation, mass transfer, charge transfer, energy transfer,
object transport, or faster-than-light signaling.

## Conventions

For a `dim`-dimensional Kogut-Susskind cell/taste decomposition,

```text
C^N = C^(N_cells) tensor C^(2^dim)
```

the native sublattice parity is taste-diagonal:

```text
Z_raw = I_cells tensor xi_5
```

In taste-bit notation, `xi_5` is the product of all taste-axis `Z` signs. If
the retained logical axis is `r`, then

```text
xi_5 = Z_r * product_{a != r} Z_a
```

where the axes `a != r` are spectator taste axes.

The retained-axis logical operator is instead

```text
Z_retained = I_cells tensor Z_r tensor I_spectator
```

after ordering the taste Hilbert space as retained logical bit plus spectator
taste bits. This is the `Z` operator supported by the traced operational
readout/operator model in dimensions greater than one.

## Fixed-Branch Statement

On a fixed cell and fixed spectator taste sector, every spectator sign is a
known scalar. Therefore the restricted raw parity operator is

```text
Z_raw | fixed spectators = s_branch * Z_retained
```

with `s_branch = +/-1`.

This is a valid fixed-branch logical-Pauli statement. It does not weaken the
earlier fixed-cell and fixed-spectator artifacts:

- a fixed branch may use `Z_raw` as logical `Z`, up to the known spectator
  sign;
- same-encoding Bell stabilizers can cancel a shared fixed sign;
- a Pauli correction can absorb a known sign as a convention or branch
  relabeling;
- algebraic portability checks may report that the restricted `Z_raw` is a
  signed logical Pauli on each surveyed encoding.

Those are restriction statements about selected branches. They are not by
themselves operational statements about a traced apparatus that ignores the
branch labels.

## Traced-Operator Statement

After cells and spectator tastes are traced out, a readout, Bell measurement,
or correction is taste-only for the retained logical qubit only if its full
operator factors as

```text
O_full = O_logical tensor I_env
```

where `env` contains all traced cells and spectator tastes.

In `dim > 1`, `Z_raw = xi_5` includes the spectator factor
`product_{a != r} Z_a`. It is diagonal and cell-blind, but it is not identity
on spectator tastes. A `Z_raw` readout therefore distinguishes, weights, or
conditions on spectator sectors unless an extra branch model is supplied. It
is not the retained-bit-only `Z` needed by traced retained-bit
readout/correction.

The operational traced lane must therefore use

```text
Z_retained = I_cells tensor Z_r tensor I_spectator
```

for retained-bit computational readout, `ZZ` stabilizers, Bell projectors, and
Bob corrections. In the retained-last-axis lane, the fixed pair-hop `X` remains
acceptable only because the operator-model audit finds it equal to the
retained-last-axis logical `X`; this does not turn `Z_raw` into a traced
retained-bit `Z` in `dim > 1`.

## Why `dim = 1` Is Special

For `dim = 1`, there are no spectator taste axes. The product over spectators
is empty, so

```text
xi_5 = Z_r
```

up to the chosen one-dimensional convention. Because `Z_raw` is also
`I_cells tensor xi_5`, it is identity on cells and has no spectator dependence.
Thus raw sublattice parity and retained-axis logical `Z` coincide for the
traced retained-bit criterion in `dim = 1`.

For `dim > 1`, there is at least one spectator taste sign. Fixed branches still
have a signed restriction, but traced operational readout sees the branch
dependence unless it uses `Z_retained` or supplies an explicit environment
measurement/heralding model.

## When Cells and Spectators May Be Ignored

Cells and spectator tastes may be ignored only under one of the following
conditions:

1. Every preparation, readout, Bell-measurement, and correction operator used
   by the protocol is proved to factor as `O_logical tensor I_env`.
2. The apparatus/control model is proved readout-blind to the ignored labels
   within the protocol tolerance and does not condition on them.
3. Branch variation over ignored labels is bounded below the protocol error
   budget for every logical observable used.
4. An explicit environment measurement, heralding rule, and branch-conditioned
   operation set is supplied, including the success probability or
   postselection cost.
5. The claim is explicitly a fixed-branch claim: the cell and spectator sector
   are selected, retained throughout the calculation, and all logical signs
   are tracked as branch data.

Condition 5 is enough for fixed-branch algebra. It is not enough for a traced
deterministic retained-bit readout/correction claim.

## Recommended Language

Future protocol notes should use language like:

```text
On a fixed cell and fixed spectator taste branch, raw sublattice parity
Z_raw = xi_5 restricts to a signed logical Z on the retained taste bit. This
supports the fixed-branch algebraic Pauli checks.

For traced retained-bit readout/correction, the implemented Z must be the
retained-axis operator Z_retained = I_cells tensor Z_r tensor I_spectator.
In dim > 1, raw xi_5 contains spectator taste signs and is not a retained-bit
operator unless an explicit branch measurement/heralding model is supplied.
```

Future scripts should label these cases separately:

```text
fixed_branch_z: raw xi_5 restricted to selected cell/spectator branch;
traced_operator_z: retained-axis Z_r tensor identity on traced environment;
native_xi5_as_traced_z: allowed only when dim == 1, or when an explicit
environment branch workflow is being tested.
```

Suggested pass/fail wording:

```text
PASS fixed-branch Z restriction: xi_5 -> +/- Z_L on this branch.
PASS traced retained-axis Z: Z_r factors as O_logical tensor I_env.
FAIL native xi_5 as traced Z in dim>1: spectator taste signs remain.
```

## Related Notes

This clarification is meant to scope, not replace, the existing artifacts:

- [`TELEPORTATION_PROTOCOL_NOTE.md`](TELEPORTATION_PROTOCOL_NOTE.md) records
  the original fixed-cell retained-last-axis protocol surface and the later
  operational gate summaries.
- [`TELEPORTATION_ENCODING_PORTABILITY_NOTE.md`](TELEPORTATION_ENCODING_PORTABILITY_NOTE.md)
  reports that restricted `Z_raw` is a signed logical Pauli on surveyed
  fixed encodings.
- [`TELEPORTATION_LOGICAL_READOUT_AUDIT.md`](TELEPORTATION_LOGICAL_READOUT_AUDIT.md)
  separates valid traced logical extraction from an operational readout
  primitive.
- [`TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE.md`](TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE.md)
  applies the `O_logical tensor I_env` criterion and rules out raw `xi_5` as
  traced retained-bit `Z` in `dim > 1`.
- [`TELEPORTATION_BELL_MEASUREMENT_CIRCUIT_NOTE.md`](TELEPORTATION_BELL_MEASUREMENT_CIRCUIT_NOTE.md)
  decomposes the ideal Bell measurement, assuming the logical `Z` readout
  supplied to the circuit is the correctly scoped retained-bit operator.

## Claim Boundary

The safe summary is:

```text
Raw sublattice parity Z=xi_5 can restrict to a signed logical Z on a fixed
cell/spectator branch. In traced operational retained-bit readout or
correction for dim>1, the logical Z must be the retained-axis Z operator,
not raw xi_5, unless an explicit environment measurement/heralding and
branch-conditioned correction workflow is supplied.
```

This preserves the fixed-branch artifacts while keeping the operational traced
readout claim strict.
