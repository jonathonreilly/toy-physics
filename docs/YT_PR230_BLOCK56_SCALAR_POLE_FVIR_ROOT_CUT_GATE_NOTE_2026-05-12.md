# PR230 Block56 Scalar-Pole/FVIR Root Cut Gate

**Status:** exact-support / current scalar/FH-LSZ artifacts do not close scalar pole/model-class/FV/IR authority
**Runner:** `scripts/frontier_yt_pr230_block56_scalar_pole_fvir_root_cut_gate.py`
**Certificate:** `outputs/yt_pr230_block56_scalar_pole_fvir_root_cut_gate_2026-05-12.json`

## Claim

Block54 reduced physical readout authorization to two roots:

1. scalar pole/model-class/FV/IR authority;
2. canonical-Higgs identity or an equivalent same-surface neutral-transfer
   bridge.

Block55 cut the second root.  This note cuts the first root on the current
PR230 surface: the existing FH-LSZ, Stieltjes/Pade, contact-subtraction,
holonomic, finite-volume, and source-Higgs row artifacts do not supply strict
scalar pole/model-class/FV/IR authority.

This is not a permanent no-go against scalar LSZ.  It is a current-surface
boundary.  A future proof can still close the root by deriving a same-surface
scalar denominator/contact theorem with threshold and FV/IR control, or by
bypassing scalar-source normalization through strict physical rows.

## Current-Surface Cut

The runner verifies the following current-surface facts together:

- The Block54 scalar/FVIR root still survives, and Block55 does not close it.
- The raw two-source taste-radial `C_ss` proxy is not a strict scalar-LSZ
  Stieltjes object: it violates the required non-increasing behavior and has no
  multivolume FV/IR, isolated-pole, or threshold authority.
- The model-class, Stieltjes moment, Pade-Stieltjes, and complete-Bernstein
  certificates do not pass as strict scalar authority.
- Finite-shell holonomic continuation is ambiguous: the same finite samples
  admit different pole residues without a same-surface denominator and boundary
  theorem.
- Finite Stieltjes prefixes are not determinacy certificates: positive
  measures can share the checked finite prefix while changing the pole atom and
  higher tail.
- Contact subtraction is not identified by the current rows.  Affine
  monotonicity repair and polynomial contact repair are both blocked as
  scalar-LSZ authority.
- Pole saturation, threshold, and FV/IR authority remain absent; finite-volume
  discreteness alone is not a pole-saturation theorem.
- The strict source-Higgs bypass is not available because accepted `O_H` and
  production `C_ss/C_sH/C_HH` pole rows are absent.

The certificate records `PASS=18 FAIL=0`,
`scalar_pole_fvir_root_closed=false`, and `proposal_allowed=false`.

## Remaining Obligations

The scalar root can move positively only with one of these artifacts:

1. a same-surface scalar denominator/contact/subtraction theorem;
2. a strict positive Stieltjes or exact-denominator certificate with all-order
   or certified-tail control;
3. an isolated scalar pole with a tight positive residue interval;
4. continuum threshold/gap plus multivolume FV/IR limiting-order authority;
5. a canonical `O_H`/source-overlap bridge with strict rows, or a physical
   W/Z/source-Higgs bypass.

## Non-Claims

This note does not claim retained or `proposed_retained` top-Yukawa closure.
It does not define `y_t` through a matrix element or `y_t_bare`.  It does not
use `H_unit`, `yt_ward_identity`, `alpha_LM`, plaquette/`u0`, observed targets,
`kappa_s=1`, `c2=1`, or `Z_match=1`.

It also does not claim scalar LSZ is impossible.  It only rejects the current
shortcuts: finite-shell fits, raw `C_ss`, holonomic interpolation, contact
repair, finite-volume discreteness, and source-Higgs contracts are not strict
physical scalar-pole authority.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_block56_scalar_pole_fvir_root_cut_gate.py
python3 scripts/frontier_yt_pr230_block56_scalar_pole_fvir_root_cut_gate.py
# SUMMARY: PASS=18 FAIL=0
```

