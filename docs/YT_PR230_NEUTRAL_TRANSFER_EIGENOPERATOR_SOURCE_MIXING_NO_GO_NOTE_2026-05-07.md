# PR230 Neutral Transfer/Eigenoperator Source-Mixing No-Go

**Status:** exact negative boundary / current same-surface Z3 eigenoperator
data do not certify a physical neutral scalar transfer or `O_H` bridge

**Runner:** `scripts/frontier_yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go.py`

**Certificate:** `outputs/yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go_2026-05-07.json`

## Load-Bearing Dependencies

- [Same-surface Z3 taste triplet artifact](YT_PR230_SAME_SURFACE_Z3_TASTE_TRIPLET_ARTIFACT_NOTE_2026-05-06.md)
- [Z3 triplet positive-cone support certificate](YT_PR230_Z3_TRIPLET_POSITIVE_CONE_SUPPORT_CERTIFICATE_NOTE_2026-05-06.md)
- [Z3 triplet conditional primitive-cone theorem](YT_PR230_Z3_TRIPLET_CONDITIONAL_PRIMITIVE_CONE_THEOREM_NOTE_2026-05-06.md)
- [Z3 lazy-transfer promotion attempt](YT_PR230_Z3_LAZY_TRANSFER_PROMOTION_ATTEMPT_NOTE_2026-05-06.md)
- [Z3 lazy selector no-go](YT_PR230_Z3_LAZY_SELECTOR_NO_GO_NOTE_2026-05-06.md)
- [Same-surface neutral multiplicity-one candidate attempt](YT_PR230_SAME_SURFACE_NEUTRAL_MULTIPLICITY_ONE_CANDIDATE_ATTEMPT_NOTE_2026-05-07.md)
- [Canonical Higgs operator certificate gate](YT_CANONICAL_HIGGS_OPERATOR_CERTIFICATE_GATE_NOTE_2026-05-03.md)
- [Source-Higgs pole-row acceptance contract](YT_PR230_SOURCE_HIGGS_POLE_ROW_ACCEPTANCE_CONTRACT_NOTE_2026-05-06.md)
- [OS transfer-kernel artifact gate](YT_PR230_OS_TRANSFER_KERNEL_ARTIFACT_GATE_NOTE_2026-05-07.md)

## Purpose

This block attacks the neutral transfer/eigenoperator primitive route directly.
The current PR230 surface has real same-surface algebra:

- a Z3 cyclic action on the taste triplet;
- equal-magnitude positive-cone support for `Q_i^+=(I+S_i)/2`;
- a conditional primitive theorem for the lazy triplet transfer;
- two-source taste-radial row support.

The missing question is whether those facts already force a physical neutral
transfer/action eigenoperator bridge from the PR230 source to canonical
`O_H` or to `C_sH/C_HH` pole rows.

They do not.

## Exact Obstruction

In the current symmetric taste-polynomial Z3-invariant neutral sector the
runner constructs the orthonormal basis

```text
E0 = I/sqrt(8)
E1 = (S0+S1+S2)/sqrt(24)
E2 = (S0S1+S1S2+S2S0)/sqrt(24)
E3 = S0S1S2/sqrt(8).
```

The tensor-cycle Z3 action fixes all four exhibited basis vectors.  In
particular the source identity `E0` and degree-one taste-radial axis `E1` are
orthogonal but live in the same trivial Z3 sector.  Therefore Z3/eigenoperator
data alone do not determine the off-diagonal source-radial action entry.

The runner exhibits two positive self-adjoint source-radial kernels compatible
with the same current symmetry data:

```text
K0 = [[2, 0],
      [0, 3]]

K1 = [[2, 1/2],
      [1/2, 3]].
```

`K0` keeps `E1` as an eigenoperator but has zero source-radial bridge entry.
`K1` has a nonzero bridge entry but `E1` is no longer an eigenoperator by
itself.  The bridge coefficient is independent transfer/action data, not a
consequence of current Z3 or taste-radial eigenoperator facts.

## Primitive-Transfer Boundary

The same issue appears in the primitive transfer language.  The lazy triplet
transfer `L=(I+P)/2` is primitive on the triplet because `L^2` is strictly
positive.  But extending it to the PR230 source plus triplet with the source
block isolated is reducible and not primitive.  A primitive full
source-plus-triplet transfer requires a new source-triplet coupling `eta`.
For example `eta=1/10` gives a primitive finite matrix, while `eta=0` does
not.

The current same-surface artifacts do not derive `eta`.  Choosing it by
positivity, entropy, spectral gap, Markov laziness, or notation would import
the missing physical transfer/action principle.

## Claim Boundary

This note is not retained or `proposed_retained` closure.  It does not
identify the taste-radial source `x` with canonical `O_H`, does not relabel
`C_sx/C_xx` as `C_sH/C_HH`, does not set `kappa_s`, `c2`, `Z_match`, or `g2`
to one, and does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0`.

## Exact Next Action

To reopen the route positively, supply one of:

- a same-surface neutral transfer/action row with the source-radial
  off-diagonal entry fixed;
- a strict off-diagonal neutral-generator certificate;
- a strict primitive-cone certificate on the full source-plus-neutral sector;
- canonical `O_H` plus `C_sH/C_HH` pole rows and Gram purity;
- a same-source W/Z physical-response packet with accepted action, covariance,
  strict non-observed `g2`, and orthogonal-scalar control.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go.py
python3 scripts/frontier_yt_pr230_neutral_transfer_eigenoperator_source_mixing_no_go.py
# SUMMARY: PASS=18 FAIL=0
```
