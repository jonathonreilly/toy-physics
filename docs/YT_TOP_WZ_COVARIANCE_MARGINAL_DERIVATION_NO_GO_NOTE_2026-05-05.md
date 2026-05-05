# YT Top/W Covariance Marginal-Derivation No-Go

Status: exact negative boundary / covariance derivation shortcut rejected;
proposal_allowed=false.

This note records the derivation-first test for the matched top/W covariance
input in PR #230.  The attempted shortcut was:

```text
top-response marginal support + W-response marginal or static EW response
  -> derive cov_dE_top_dM_W
```

That shortcut fails.  The matched covariance is a joint observable.  It is not
determined by the separate top and W response marginals.

## Runner

```text
scripts/frontier_yt_top_wz_covariance_marginal_derivation_no_go.py
```

Output:

```text
outputs/yt_top_wz_covariance_marginal_derivation_no_go_2026-05-05.json
```

## Witness

The runner constructs two matched ensembles with the same top-response
marginal and the same W-response marginal.  The two ensembles therefore have
the same top mean, W mean, top variance, W variance, and response ranges.

The only change is the pairing between top and W rows.  One pairing gives
positive `cov_dE_top_dM_W`; the reversed pairing gives negative
`cov_dE_top_dM_W`.

Therefore a covariance certificate cannot be derived from marginal response
support alone.  A valid route needs one of:

- measured matched top/W response rows on the same configuration set;
- a same-surface factorization or independence theorem fixing the covariance;
- a deterministic W-response theorem plus a validated finite-sample covariance
  rule against the top response.

## Current PR230 Boundary

The current surface has:

- bounded top-response support;
- exact support for the same-source W-response algebra;
- W/Z row contracts and adapters;
- no production matched top/W rows;
- no W/Z correlator mass-fit rows;
- no same-source EW action certificate;
- no factorization theorem fixing `cov_dE_top_dM_W`.

This note does not create production rows, does not claim top-Yukawa closure,
and does not use observed W/Z/top/`y_t`/`g_2` selectors, `H_unit`,
`yt_ward_identity`, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`, or
`Z_match=1`.

## Next Action

If we want to avoid new W/Z compute, the next derivation target is not the
covariance itself from marginals.  It is a real same-surface
factorization/independence theorem for the joint top/W source response.
