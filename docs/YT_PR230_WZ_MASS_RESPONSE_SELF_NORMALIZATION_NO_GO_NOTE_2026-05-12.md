# PR230 W/Z Mass-Response Self-Normalization No-Go

**Status:** support / exact negative boundary for W/Z mass-plus-response self-normalization

**Runner:** `scripts/frontier_yt_pr230_wz_mass_response_self_normalization_no_go.py`

**Certificate:**
`outputs/yt_pr230_wz_mass_response_self_normalization_no_go_2026-05-12.json`

```yaml
actual_current_surface_status: exact negative boundary / WZ top-W-Z mass-plus-response self-normalization does not fix absolute y_t on the current PR230 surface
conditional_surface_status: conditional-support if a future strict non-observed g2 certificate, absolute v authority accepted as a substrate input, or another absolute EW normalization theorem is supplied
proposal_allowed: false
bare_retained_allowed: false
```

## Question

After the Block38 neutral-rank bypass failed, the strongest W/Z shortcut left
to test was whether adding same-surface top/W/Z mass rows to same-source W/Z
response rows could remove the need for the strict `g2` certificate.  If true,
the W/Z physical-response route would no longer need an external absolute EW
normalization.

## Result

It cannot.  The full mass-plus-response dictionary

```text
m_t       = y_t v / sqrt(2)
M_W       = g2 v / 2
M_Z       = sqrt(g2^2 + gY^2) v / 2
dm_t/ds   = y_t (dv/ds) / sqrt(2)
dM_W/ds   = g2 (dv/ds) / 2
dM_Z/ds   = sqrt(g2^2 + gY^2) (dv/ds) / 2
```

is invariant under

```text
(v, dv/ds) -> lambda (v, dv/ds)
(y_t, g2, gY) -> (y_t, g2, gY) / lambda.
```

Thus even ideal mass rows plus ideal same-source response rows determine
ratios such as `y_t/g2`, `gY/g2`, `m_t/M_W`, and `dM_W/ds / dM_Z/ds`.  They do
not determine the absolute `y_t`, `g2`, or `v` normalization.

## Boundary

This is not a no-go against future W/Z closure.  It only blocks the
self-normalization shortcut.  The W/Z physical-response route can reopen if a
future artifact supplies one of:

1. a strict non-observed `g2` certificate from allowed authority;
2. an explicitly admitted `v` substrate input for the readout, with that
   dependency kept visible;
3. another absolute EW normalization theorem outside the top/W/Z
   mass-response rows.

## Non-Claims

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not use observed top/W/Z/`y_t`/`g2` values, `H_unit`,
`yt_ward_identity`, `y_t_bare`, `alpha_LM`, plaquette, `u0`, static EW algebra
as response evidence, scout/smoke rows as production evidence, or unit
settings for `v`, `g2`, `c2`, `Z_match`, or `kappa_s`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_wz_mass_response_self_normalization_no_go.py
python3 scripts/frontier_yt_pr230_wz_mass_response_self_normalization_no_go.py
# SUMMARY: PASS=15 FAIL=0
```
