# FH/LSZ Uniform-Gap Self-Certification No-Go

Status: exact negative boundary / FH-LSZ uniform-gap self-certification no-go

Claim firewall:

```yaml
actual_current_surface_status: exact negative boundary / FH-LSZ uniform-gap self-certification no-go
proposal_allowed: false
bare_retained_allowed: false
```

The pole-saturation threshold gate identified a possible repair: provide a
uniform continuum gap or microscopic scalar-denominator theorem so finite-shell
same-source `Gamma_ss(p^2)` rows can be used for an isolated pole residue.

This block checks whether the finite shell rows can certify that gap by
themselves.  They cannot.

The runner constructs shell data from a deliberately gapped positive Stieltjes
model with continuum threshold `m^2 = 1.0` and pole residue `1`.  When fit in
the true gapped model class, the pole-residue interval is tight.  But the same
finite shell values are also fit by a positive near-pole continuum model with
threshold `m^2 = 0.251`, and in that model class the allowed pole-residue lower
bound is zero.

Therefore finite Euclidean shell rows do not self-certify the uniform gap.  The
gap must come from one of:

- an independent scalar-denominator theorem;
- a continuum-threshold / pole-saturation certificate;
- a production postprocess acceptance analysis with model-class control.

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_uniform_gap_self_certification_no_go.py
# SUMMARY: PASS=7 FAIL=0
```

Boundary:

This does not close PR #230 and does not authorize `retained` or
`proposed_retained`.  It narrows the analytic target: the next positive theorem
must derive the microscopic scalar denominator / threshold support, not infer a
gap from finite shell samples.
