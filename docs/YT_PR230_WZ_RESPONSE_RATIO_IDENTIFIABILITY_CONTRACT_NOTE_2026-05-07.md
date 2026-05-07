# PR #230 W/Z Response-Ratio Identifiability Contract

**Status:** exact-support / response-ratio contract only; current rows and strict `g2` authority absent
**Runner:** `scripts/frontier_yt_pr230_wz_response_ratio_identifiability_contract.py`
**Certificate:** `outputs/yt_pr230_wz_response_ratio_identifiability_contract_2026-05-07.json`

## Claim

The clean physical-response bypass has a narrow exact form.  If one accepted
same-source EW/Higgs action makes the PR230 source `s` move a single Higgs
radial branch `v(s)`, and if there is no independent additive `s * tbar t`
top source, then

```text
dm_top/ds = y_t dv/ds / sqrt(2)
dM_W/ds   = g2 dv/ds / 2
dM_Z/ds   = sqrt(g2^2 + gY^2) dv/ds / 2
```

so the unknown source normalization cancels:

```text
y_t = (g2 / sqrt(2)) * (dm_top/ds) / (dM_W/ds)
y_t = (sqrt(g2^2 + gY^2) / sqrt(2)) * (dm_top/ds) / (dM_Z/ds)
```

The runner also records the required matched covariance/error contract.  For
the top/W readout it uses the exact delta-method gradient for

```text
y_t(T,W,g2) = g2 T / (sqrt(2) W)
```

with `T=dE_top/ds`, `W=dM_W/ds`, and a covariance matrix containing at least
`var(T)`, `var(W)`, `cov(T,W)`, and `var(g2)`.

## Boundary

This is not a current closure.  The runner writes a future acceptance schema
and checks the current blockers:

- no accepted same-source EW/Higgs action certificate;
- no production W/Z response-ratio row packet;
- no same-source top-response certificate under that action;
- no matched top/W or top/Z covariance certificate;
- no strict non-observed `g2` certificate;
- the current radial-spurion action contract is support only and is not
  satisfied on the current surface.

Two counterfamilies are explicit.  If an independent additive top source is
allowed, fixed measured top/W slopes can be represented by different `y_t`
values with different additive top slopes.  If `g2` is not fixed by a strict
non-observed certificate, the same top/W response ratio gives different
absolute `y_t` values.

No retained or proposed-retained closure is authorized.  The contract does not
use `H_unit`, `yt_ward_identity`, observed masses or couplings, `alpha_LM`,
plaquette/`u0`, reduced pilots, or fiat settings of `kappa_s`, `c2`,
`Z_match`, `g2`, or `delta_perp`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_wz_response_ratio_identifiability_contract.py
python3 scripts/frontier_yt_pr230_wz_response_ratio_identifiability_contract.py
# SUMMARY: PASS=18 FAIL=0
```
