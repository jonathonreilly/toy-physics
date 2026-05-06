# PR230 Source-Sector Pattern Transfer Gate

**Date:** 2026-05-05  
**Status:** bounded-support / SU(3) source-sector pattern is relevant to PR230 as a bridge-computation method, not as source-only `y_t` closure  
**Runner:** `scripts/frontier_yt_pr230_source_sector_pattern_transfer_gate.py`  
**Certificate:** `outputs/yt_pr230_source_sector_pattern_transfer_gate_2026-05-05.json`

## Question

The SU(3) plaquette campaign found a useful pattern: define a finite compact
source sector, derive the observable as a derivative or source response, and
then attack the residual by character, Schwinger-Dyson, holonomic, or tensor
methods.

This note asks whether that approach is relevant to PR #230's top-Yukawa
problem.

## Verdict

Yes, but only as a method for the missing bridge.

The transfer is not:

```text
SU3 plaquette exponent shift -> y_t value
```

and it is not:

```text
source-only C_ss -> canonical Higgs coupling
```

The valid transfer is:

```text
define same-surface Z(beta, s, h)
-> compute C_ss, C_sH, C_HH by exact source-sector methods
-> certify source-Higgs purity and scalar LSZ normalization
-> then compute the physical Yukawa readout
```

or the theorem variant:

```text
derive a neutral scalar primitive/rank-one theorem
-> prove the source pole is the unique canonical Higgs radial pole
-> source-only rows become sufficient
```

## Why The Plaquette Move Does Not Directly Close PR230

The plaquette is an action source already living in the compact gauge sector.
Once the source-sector weight is derived, the plaquette observable is the
physical derivative of the same action.

In PR #230, the current source coordinate is not yet certified as the canonical
Higgs radial coordinate used by `v`.  Exact knowledge of `Z(s,0)` or `C_ss`
does not determine the missing cross rows.  A two-operator pole model with

```text
log Z(s,h) = 1/2 (C_ss s^2 + 2 C_sH s h + C_HH h^2)
```

can keep `C_ss = C_HH = 1` and the same source-only functional
`log Z(s,0)=s^2/2` while varying `C_sH`.  The source-Higgs Gram determinant
`C_ss C_HH - C_sH^2` then changes, so source-only data cannot fix purity.

## What Does Transfer

- The finite-source discipline transfers.  Define `Z` first; compute rows as
  derivatives of `log Z`; do not select operators by observed target values.
- Holonomic, Picard-Fuchs, D-module, Schwinger-Dyson, character, and exact
  tensor methods are useful after the same-surface operator/action exists.
- The exponent-shift idea suggests a legitimate PR230 target: derive the
  source-coordinate normalization or scalar pole residue from the same
  finite-source equations.  It is not a proof until it supplies an invariant
  overlap row or canonical normalization.
- The strongest derivation route is still the neutral-scalar primitive/rank-one
  bridge.  If all neutral top-coupled scalar probes couple to one unique
  lowest pole, source-only measurements could become physical.

## Current Blocker

The current surface still lacks all positive bridge artifacts:

- same-surface canonical `O_H/h` certificate;
- source-Higgs `C_sH/C_HH` pole rows;
- same-source W/Z response rows;
- neutral primitive-cone or rank-one certificate.

Therefore the source-sector approach is relevant but not a retained or
proposed-retained `y_t` derivation.

## Non-Claims

This note does not work the SU(3) plaquette SD problem, does not import the
plaquette value or exponent shift into `y_t`, does not define `y_t_bare`, does
not use `H_unit` or `yt_ward_identity`, does not identify source-only `O_s`
with canonical `O_H`, and does not set `kappa_s = 1`.

## Exact Next Action

Use the transferred method only after building a current-surface bridge object:
canonical `O_H/h` plus `C_sH/C_HH` rows, same-source W/Z response rows, or a
neutral primitive-cone/rank-one theorem.  Do not spend PR230 effort deriving
SU(3) plaquette constants unless they directly produce one of those bridge
objects.

## Verification

```bash
python3 scripts/frontier_yt_pr230_source_sector_pattern_transfer_gate.py
# SUMMARY: PASS=11 FAIL=0
```
