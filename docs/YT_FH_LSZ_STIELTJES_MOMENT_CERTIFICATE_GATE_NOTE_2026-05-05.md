# PR #230 FH/LSZ Stieltjes Moment-Certificate Gate

**Status:** exact-support / FH-LSZ Stieltjes moment-certificate gate; strict positive certificate absent
**Runner:** `scripts/frontier_yt_fh_lsz_stieltjes_moment_certificate_gate.py`
**Certificate:** `outputs/yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json`

## Claim

The scalar-LSZ route now has a strict positive-certificate contract.  A finite
Euclidean shell fit or pole-fit postprocessor row is not enough to identify the
scalar LSZ residue.  A future positive route must supply a Stieltjes moment
certificate for the scalar two-point function, plus pole-saturation,
threshold-gap, FV/IR, and semantic-firewall checks.

For a positive Stieltjes representation

```text
C(q^2) = int dmu(s) / (q^2 + s),        dmu(s) >= 0,
```

the moments `m_n` obey positive-semidefinite Hankel constraints:

```text
H_ij = m_{i+j} >= 0,        H'_ij = m_{i+j+1} >= 0.
```

The runner constructs a positive discrete spectral witness that satisfies the
Hankel and shifted-Hankel checks, and a finite-shell-like moment witness whose
`2 x 2` Hankel determinant is negative.  This makes the acceptance criterion
mathematical rather than a self-declared model-class label.

## Acceptance Contract

A future certificate at
`outputs/yt_fh_lsz_stieltjes_moment_certificate_2026-05-05.json` must include:

- same-surface `Cl(3)/Z^3` provenance and source coordinate;
- declared zero-source limit;
- scalar-channel moments passing Hankel PSD through order 3 and shifted Hankel
  PSD through order 2;
- certified pole location and positive pole residue;
- positive lower bound and relative width <= 2% for the pole-residue interval;
- threshold-gap and FV/IR control;
- analytic-continuation or microscopic scalar-denominator authority;
- firewall checks excluding observed-target selectors, `H_unit`, Ward
  authority, `alpha_LM`, plaquette/u0, and unit shortcuts.

## Boundary

This is not scalar-LSZ closure.  It does not define `y_t_bare`, does not use
`yt_ward_identity`, and does not turn the current chunk or pole-fit outputs
into `y_t` evidence.  It gives the strict positive gate that future production
data or a stronger scalar-denominator theorem must satisfy.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_stieltjes_moment_certificate_gate.py
python3 scripts/frontier_yt_fh_lsz_stieltjes_moment_certificate_gate.py
# SUMMARY: PASS=10 FAIL=0
```
