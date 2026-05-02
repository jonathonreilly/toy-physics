# FH/LSZ Soft-Continuum Threshold No-Go

Status: exact negative boundary / FH-LSZ soft-continuum threshold no-go

Claim firewall:

```yaml
actual_current_surface_status: exact negative boundary / FH-LSZ soft-continuum threshold no-go
proposal_allowed: false
bare_retained_allowed: false
```

This block tests whether the existing color-singlet support can be promoted
into the missing FH/LSZ threshold premise.

Result:

- color-singlet `q=0` gauge-zero-mode cancellation is useful support;
- finite-`q` IR regularity is useful support;
- neither support statement certifies a positive continuum gap above the
  scalar pole;
- a zero-mode-removed massless kernel can be locally integrable while positive
  continuum spectral weight starts arbitrarily close to the pole.

The runner models a normalized soft continuum band with density proportional
to the zero-mode-removed finite-`q` measure.  As the lower edge approaches the
pole, all sampled shell contributions remain finite.  Therefore IR regularity
controls a divergence; it does not supply the pole-saturation / uniform
threshold premise required by the residue-interval gate.

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_soft_continuum_threshold_no_go.py
# SUMMARY: PASS=8 FAIL=0
```

Boundary:

This does not close PR #230 and does not authorize `retained` or
`proposed_retained`.  A real microscopic scalar-denominator theorem or
production acceptance certificate is still required before a finite-shell
same-source pole fit can become load-bearing.
