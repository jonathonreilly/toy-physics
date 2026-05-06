# PR230 Two-Source Taste-Radial Chart Certificate

**Status:** exact-support / same-surface two-source taste-radial chart;
canonical `O_H` and production rows absent

**Runner:** `scripts/frontier_yt_pr230_two_source_taste_radial_chart_certificate.py`
**Certificate:** `outputs/yt_pr230_two_source_taste_radial_chart_certificate_2026-05-06.json`

## Purpose

The one-source source-coordinate route is blocked: the PR230 source line is
the uniform additive mass source `m_bare + s`, with taste insertion `I_8`, and
no same-surface reparametrization maps that tangent into a trace-zero
Higgs/taste axis.

This block records the next honest positive artifact for that contract.  It
does not pretend the second source already existed.  It asks whether the same
`Cl(3)/Z^3` taste algebra supplies an exact two-source chart if a future
production action explicitly turns on a second source coordinate.

## Exact Chart

On `C^8 = (C^2)^{otimes 3}`, let

```text
S0 = sigma_x I I
S1 = I sigma_x I
S2 = I I sigma_x
```

and define the Hilbert-Schmidt normalized source and taste-radial directions

```text
s_hat = I_8 / sqrt(8)
h_taste = (S0 + S1 + S2) / sqrt(24).
```

The runner verifies:

- the `S_i` form an orthonormal Hilbert-Schmidt taste-axis frame after
  normalization;
- `<s_hat, h_taste> = 0`;
- `||s_hat|| = ||h_taste|| = 1`;
- `Tr(h_taste) = 0`, while `Tr(I_8) = 8`;
- the cyclic tensor permutation fixes both `I_8` and the radial sum
  `S0 + S1 + S2`;
- the normalized two-source chart has Gram matrix `diag(1,1)`.

This supplies an exact same-surface algebraic target for future two-source
rows.  It retires only the absence of a named taste-radial chart.

## Boundary

This is not top-Yukawa closure.  The new `h_taste` coordinate is a second
source-axis extension until a same-surface production action or measurement-row
certificate turns it on.  It is not canonical `O_H` by itself.

Still absent:

- same-source EW/Higgs or two-source production action;
- canonical `O_H` identity and normalization;
- production `C_sx/C_xx` or `C_sH/C_HH` pole rows;
- proof that the taste-radial pole is the canonical Higgs pole;
- retained-route or campaign authorization for `proposed_retained`.

## Non-Claims

No retained or `proposed_retained` PR230 closure is claimed.  This block does
not use `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`, plaquette,
`u0`, or unit assignments for `kappa_s`, `c2`, or `Z_match`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_two_source_taste_radial_chart_certificate.py
# SUMMARY: PASS=21 FAIL=0
```

## Next Action

If pursuing the source-coordinate route, implement a genuine two-source
production/action row for `h_taste` and measure `C_sx/C_xx`, then separately
prove or reject whether that `x` is canonical `O_H`.  Otherwise pivot to W/Z
response, Schur `A/B/C`, neutral primitive, or strict scalar-LSZ authority.
