# Assumptions And Imports

## Minimal Inputs

- Local algebra: `Cl(3)`, instantiated in the runner by Pauli generators and
  checked by the Clifford anticommutator relation.
- Spatial substrate/readout: the `Z^3` `hw=1` character triplet
  `(-1,+1,+1)`, `(+1,-1,+1)`, `(+1,+1,-1)`.
- Lower-level PMNS response conventions: active response uses
  `(I - lambda_act (D - I))^-1`; passive response uses
  `(I - lambda_pass D)^-1`.

## Retired Import

- The identity active/passive blocks are no longer inserted as constants.
  They are computed as `sum_i P_i I_hw1 P_i = I3` from joint spectral
  projectors of the `Z^3` translation involutions.

## Remaining Imports

- The live retained PMNS closure stack is still invoked as a consistency
  check. The runner now also includes a local support-mask rejection showing
  that both derived blocks are monomial/diagonal and neither has active
  `I + C` support.
- Independent re-audit is required before this branch-local bounded-support
  repair can become effective retained/bounded-retained status.
