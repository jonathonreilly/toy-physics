# PR230 Holonomic Source-Response Feasibility Gate

Date: 2026-05-05

Status: exact negative boundary / PR541-style holonomic source-response route
is relevant but blocked by missing current-surface `O_H` and `h` source.

Runner:
`scripts/frontier_yt_pr230_holonomic_source_response_feasibility_gate.py`

Certificate:
`outputs/yt_pr230_holonomic_source_response_feasibility_gate_2026-05-05.json`

## Question

PR #541 found a useful mathematical pattern in the plaquette lane: define a
finite-volume generating functional first, then compute target rows as
derivatives using Picard-Fuchs, holonomic, creative-telescoping, or tensor
contraction methods.

This note tests whether the same pattern immediately helps PR #230.  The
candidate target is:

```text
Z_PR230(beta, s, h)
  = integral exp(-S_Cl3Z3 + s O_s + h O_H) dmu
```

with rows:

```text
C_ss = d_s d_s log Z
C_sH = d_s d_h log Z
C_HH = d_h d_h log Z
```

at `s=h=0`.

## Result

The PR541 method is relevant, but not yet a closure route on the current PR230
surface.

The current PR230 surface has useful source-only support: an LSZ/source
functional object can describe `Z(s,0)` and `C_ss`.  But the current surface
does not contain the second source coordinate `h`, a same-surface canonical
Higgs operator `O_H`, or production `C_sH/C_HH` rows.  Without those objects,
holonomic or tensor methods have no physical two-source functional to compute.

This is a compute-method boundary, not a physics closure.

## Source-Only Counterfamily

The runner includes a minimal normalized pole counterfamily:

```text
log Z(s,h) = 1/2 (C_ss s^2 + 2 C_sH s h + C_HH h^2)
```

with `C_ss=C_HH=1` and varying `C_sH=rho`.  Every member has the same
source-only functional:

```text
log Z(s,0) = 1/2 s^2
```

but the source-Higgs overlap and Gram determinant change:

```text
Delta = C_ss C_HH - C_sH^2 = 1 - rho^2
```

So exact knowledge of `Z(s,0)` does not determine `C_sH`, `C_HH`, or the
source-Higgs purity condition.  The missing `h/O_H` object is structural, not
just numerical.

## What Transfers From PR541

The usable transfer is the discipline:

1. Define the finite-volume functional on the same current surface.
2. Name all source operators before computing.
3. Compute rows as derivatives of `log Z`.
4. Use Picard-Fuchs, D-module, tensor-network, character, or creative
   telescoping methods only after the row-generating object exists.
5. Keep observed target values and fitted selectors out of the proof.

This would be a strong route after a current-surface `O_H/h` artifact lands.

## Exact Next Action

Make the PR541-style route positive by first supplying one of:

- a same-source EW/Higgs action certificate tied to the PR230 Cl(3)/Z3 scalar
  source coordinate;
- a canonical `O_H` identity and normalization theorem on the same current
  surface;
- production `C_sH/C_HH` rows with a real `O_H` operator and Gram-purity
  certificate.

Then build `Z(beta,s,h)` and apply finite-volume tensor contraction or
holonomic creative telescoping to compute the defined rows.

## Non-Claims

This note does not claim retained or proposed-retained top-Yukawa closure.  It
does not compute `y_t` or `m_t`, does not define `y_t_bare`, does not use
`H_unit` or `yt_ward_identity`, does not use PR541 plaquette values as Yukawa
inputs, and does not identify source-only `O_s` with canonical `O_H`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_holonomic_source_response_feasibility_gate.py
# SUMMARY: PASS=17 FAIL=0
```
