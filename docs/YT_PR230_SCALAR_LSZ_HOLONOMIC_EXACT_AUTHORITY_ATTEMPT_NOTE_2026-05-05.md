# PR230 Scalar-LSZ Holonomic Exact-Authority Attempt

**Status:** exact negative boundary / scalar-LSZ holonomic exact authority not
derivable from current finite-shell PR230 data
**Runner:** `scripts/frontier_yt_pr230_scalar_lsz_holonomic_exact_authority_attempt.py`
**Certificate:** `outputs/yt_pr230_scalar_lsz_holonomic_exact_authority_attempt_2026-05-05.json`

## Purpose

This block tests the strict scalar-LSZ outside-math route: whether
holonomic/Picard-Fuchs/WZ, exact tensor/PEPS, PSLQ/value recognition, or
finite-shell exact interpolation can turn current scalar data into the missing
pole-residue, threshold, and FV/IR authority.

## Result

The attempt does not close.  The runner records a rational-holonomic
counterfamily: two rational continuations agree on every sampled shell but
carry different residues at the same isolated pole.  Therefore finite shell
values, exact interpolation, a PSLQ hit, or the existence of some holonomic
continuation do not identify the physical scalar denominator or LSZ residue.

Current blockers loaded by the runner:

- strict Stieltjes moment and Pade/Stieltjes certificates are absent;
- the current polefit8x8 `C_ss` proxy fails a necessary Stieltjes monotonicity
  check;
- contact subtraction and polynomial-contact repair shortcuts are blocked;
- threshold and FV/IR pole-saturation authority is not certified;
- no same-surface scalar denominator theorem is present.

## Future Positive Contract

A positive scalar-LSZ exact-math certificate must provide:

- same-surface exact scalar two-point or denominator object;
- derived Picard-Fuchs/WZ/D-module/tensor denominator authority with boundary
  data from the PR230 path integral;
- contact/subtraction and source-scheme certificate;
- Stieltjes moment positivity;
- threshold gap plus finite-volume/IR limiting-order authority;
- positive tight pole-residue interval;
- firewall rejecting observed selectors, `H_unit`/Ward authority,
  `alpha_LM`/plaquette/`u0`, unit `kappa_s/c2/Z_match`, and PSLQ selectors.

## Boundary

No retained or `proposed_retained` PR230 closure is claimed.  This block does
not write a strict Stieltjes, Pade, scalar-denominator, or contact-subtraction
certificate, and does not set `kappa_s`, `c2`, or `Z_match` to one.

## Verification

```bash
python3 scripts/frontier_yt_pr230_scalar_lsz_holonomic_exact_authority_attempt.py
# SUMMARY: PASS=15 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=21 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=77 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=225 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=255 FAIL=0
```
