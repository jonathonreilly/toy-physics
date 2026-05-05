# YT Same-Source Top-Response Identity Certificate Builder Note

Status: open / top-response identity contract; proposal_allowed=false.

This note records the identity object required before the PR #230 same-source
top response can be consumed by the W/Z response route.  A same-source label
and a stable `dE_top/ds` slope are not enough: the route needs an explicit
certificate that the source response is tied to the canonical Higgs/top sector,
with sector-overlap and canonical-Higgs pole identity gates closed.

## Runner

```text
scripts/frontier_yt_same_source_top_response_identity_certificate_builder.py
```

Default status output:

```text
outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json
```

Scout identity certificate:

```text
outputs/yt_same_source_top_response_identity_certificate_builder_scout_certificate_2026-05-04.json
```

Strict production identity certificate:

```text
outputs/yt_same_source_top_response_identity_certificate_2026-05-04.json
```

## Strict Requirements

Strict mode emits the production identity certificate only when all of these
conditions are satisfied:

- same-source sector-overlap identity passed;
- canonical-Higgs pole identity passed;
- at least one accepted identity route passed: direct Higgs-pole identity,
  source-Higgs Gram purity, neutral-scalar rank-one purity, or same-source W/Z
  response;
- retained-route or retained-proposal gate passed;
- forbidden-import firewalls remain clean.

## Current Result

Scout mode passes and writes only scout-named output:

```text
python3 scripts/frontier_yt_same_source_top_response_identity_certificate_builder.py --scout
```

Default/current mode passes as an honest open status and does not write
`outputs/yt_same_source_top_response_identity_certificate_2026-05-04.json`.
Strict mode intentionally fails until the identity premises close.

The current positive checks that fail are:

```text
same_source_sector_overlap_identity_passed
canonical_higgs_pole_identity_passed
source_pole_canonical_identity_passed
no_orthogonal_top_coupling_or_measured_component_passed
source_higgs_gram_purity_passed
neutral_scalar_rank_one_purity_passed
same_source_wz_response_certificate_passed
retained_route_or_proposal_gate_passed
```

## Non-Claims

This note does not claim retained or proposed_retained top-Yukawa closure.  It
does not set `kappa_s=1`, `cos(theta)=1`, or `k_top/k_gauge=1` by fiat, and it
does not use `H_unit`, `yt_ward_identity`, observed top/`y_t`/W/Z selectors,
`alpha_LM`, plaquette, or u0.

## Next Action

Close one accepted identity route.  The cleanest candidates are:

- source-Higgs Gram purity with `C_sH/C_HH` pole residues;
- same-source W/Z response certificate with sector-overlap identity;
- neutral-scalar rank-one theorem;
- direct canonical-Higgs pole identity.

Then rerun this builder in strict mode to emit the production identity
certificate consumed by the same-source top-response certificate builder.
