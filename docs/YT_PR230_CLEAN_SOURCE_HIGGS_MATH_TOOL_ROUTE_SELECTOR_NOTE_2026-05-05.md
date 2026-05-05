# PR230 Clean Source-Higgs Math-Tool Route Selector

**Status:** exact support / clean source-Higgs outside-math route selector;
positive closure still open
**Runner:** `scripts/frontier_yt_pr230_clean_source_higgs_math_tool_route_selector.py`
**Certificate:** `outputs/yt_pr230_clean_source_higgs_math_tool_route_selector_2026-05-05.json`

## Purpose

The cleanest PR230 closure is the direct source-to-canonical-Higgs route:
derive a same-surface canonical `O_H` identity and normalization certificate,
then produce `C_ss/C_sH/C_HH` pole rows and run the Gram-purity plus scalar-LSZ
aggregate gates.

This note classifies outside-math tools as possible certificate-producing
methods, not as proof authority by name.

## Ranking

1. `O_H/C_sH/C_HH` source-Higgs pole rows.
   Use invariant-ring, commutant, primitive-cone, GNS, moment, or exact tensor
   tools only if they emit the same-surface `O_H` certificate and pole rows.
2. Neutral primitive-cone or irreducibility certificate.
   This is the theorem variant of the clean route if it proves the neutral
   top-coupled scalar sector has no orthogonal component.
3. Strict scalar-LSZ moment/threshold/FV authority.
   Necessary for physical readout, but not by itself an overlap proof.
4. Schur `A/B/C` kernel rows.
   Useful denominator/orthogonal-sector authority, but source-only compressed
   denominator data is already blocked.
5. Genuine same-source W/Z response rows.
   Strong fallback, but less clean because it adds EW action, `g2`, covariance,
   and orthogonal-correction obligations.

## Outside-Math Boundary

Allowed uses:

- invariant-ring or commutant analysis to prove a same-surface
  multiplicity-one or primitive-cone certificate;
- GNS / flat-extension / truncated moment methods to certify rank-one
  source-Higgs pole purity once `C_sH/C_HH` rows exist;
- exact tensor/PEPS contraction to compute same-surface rows after the
  operator and action are defined;
- holonomic, Picard-Fuchs, WZ, or related analytic-continuation methods to
  certify scalar-LSZ moment/threshold/FV authority;
- PSLQ, motivic, MZV, or free-probability recognition only after a
  same-surface quantity has already been produced independently.

Forbidden uses:

- using PSLQ or exact constants as selectors for `O_H`, `y_t`, `g2`,
  `kappa_s`, `c2`, or `Z_match`;
- using Schur's lemma, large-N, free probability, or tensor exactness without
  the PR230 same-surface representation/action data;
- treating source-only `C_ss` rows or rows against an unratified operator as
  canonical-Higgs evidence.

## Result

No closure is claimed.  The current surface still lacks:

- `outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json`;
- `outputs/yt_source_higgs_cross_correlator_measurement_rows_2026-05-03.json`;
- neutral irreducibility or primitive-cone certificates;
- Schur kernel rows;
- strict scalar-LSZ moment/threshold/FV certificates.

The selected clean next action is:

```text
derive a same-surface invariant-ring/commutant/primitive-cone O_H identity
and normalization certificate; only after that, produce C_ss/C_sH/C_HH rows
and run GNS/Gram-purity plus scalar-LSZ aggregate gates.
```

## Verification

```bash
python3 scripts/frontier_yt_pr230_clean_source_higgs_math_tool_route_selector.py
# SUMMARY: PASS=14 FAIL=0
```
