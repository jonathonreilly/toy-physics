# PR #230 Neutral-Scalar Burnside Irreducibility Attempt

**Status:** exact negative boundary / Burnside neutral irreducibility attempt
blocked by non-full current generator algebra
**Runner:** `scripts/frontier_yt_neutral_scalar_burnside_irreducibility_attempt.py`
**Certificate:** `outputs/yt_neutral_scalar_burnside_irreducibility_attempt_2026-05-05.json`

This block tests a distinct outside-math version of the neutral-sector route:
can Burnside's theorem or the double-commutant criterion certify that the
neutral scalar sector is irreducible on the current PR #230 surface?

The attempt does not close.  The current certified neutral generator set is
source-only: identity, a source projector, and a block-diagonal source-only
transfer in a source/orthogonal neutral completion.  Its generated algebra has
dimension `2`, not the full `M_2` dimension `4`, and its commutant has
dimension `2`, not the scalar-only dimension `1`.  The associated transfer
graph is not strongly connected and has no positive primitive power.

The runner also records an acceptance-shape example.  If a future same-surface
off-diagonal neutral transfer generator were supplied, the generated algebra
could become full `M_2` and the transfer could be primitive.  That example is
only a contract witness; it is not PR #230 evidence because the required
source/orthogonal mixing generator is not currently derived or measured.

Burnside/double-commutant methods are therefore admissible only as a future
certificate engine.  They do not turn source-only `C_ss` rows, symmetry labels,
or exact method names into `O_H`, `C_sH/C_HH`, a primitive-cone certificate, or
`kappa_s`.

## Claim Boundary

This note does not claim retained or proposed-retained PR #230 closure.  It
does not write a neutral irreducibility certificate, does not set `kappa_s`,
`c2`, or `Z_match` to one, and does not use `H_unit`, `yt_ward_identity`,
observed targets, `alpha_LM`/plaquette/`u0`, reduced pilots, or PSLQ/value
recognition as proof input.

## Next Action

To make this route positive, supply a same-surface neutral scalar generator set
with source/orthogonal mixing and prove that its generated algebra is full
`M_n`, or supply an equivalent primitive-cone certificate.  Otherwise return to
certified `O_H/C_sH/C_HH` pole rows, same-source W/Z response rows with
identity/covariance/`g2` authority, Schur `A/B/C` rows, or strict scalar-LSZ
moment/threshold/FV authority.

## Verification

```bash
python3 scripts/frontier_yt_neutral_scalar_burnside_irreducibility_attempt.py
```
