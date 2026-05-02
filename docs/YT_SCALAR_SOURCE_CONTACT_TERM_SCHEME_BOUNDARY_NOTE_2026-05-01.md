# PR #230 Scalar Source Contact-Term Scheme Boundary

**Status:** exact negative boundary / scalar source contact-term scheme boundary
**Runner:** `scripts/frontier_yt_scalar_source_contact_term_scheme_boundary.py`
**Certificate:** `outputs/yt_scalar_source_contact_term_scheme_boundary_2026-05-01.json`

## Question

Can a source-curvature renormalization convention replace the same-source
scalar pole residue needed for `kappa_s`?

## Result

No.  Local source contact terms can shift analytic low-momentum curvature data
without fixing the isolated pole residue.  The runner uses:

```text
C(x) = Z / (x + m_H^2) + a + b x
```

and chooses `a,b` so that different pole residues `Z` share the same
low-momentum conditions:

```text
C(0) = 1
C'(0) = -0.25
```

The contact-normalized curvature surface is identical, but `dE/ds` and the
source overlap vary with `sqrt(Z)`.  The correct same-source readout stays
fixed only when the actual pole residue is included:

```text
dE/ds / sqrt(Res C_ss)
```

## Claim Boundary

```text
proposal_allowed: false
```

This blocks a shortcut only.  It does not add a source contact counterterm to
`A_min`, does not set `kappa_s = 1`, and does not use forbidden Ward, `H_unit`,
observed-value, alpha/plaquette, or reduced-pilot inputs.

## Exact Next Action

Use an isolated same-source pole-residue fit/theorem.  Do not use
contact-renormalized `C_ss(0)` or `C_ss'(0)` as the source-to-Higgs
normalization.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_scalar_source_contact_term_scheme_boundary.py
python3 scripts/frontier_yt_scalar_source_contact_term_scheme_boundary.py
# SUMMARY: PASS=10 FAIL=0
```
