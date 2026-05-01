# Route Portfolio

## R1. Source-to-Higgs Legendre/SSB Theorem

Score: 14/18. Hard-residual pressure: 3.

Construct the generating functional with a scalar-bilinear source, perform the
Legendre transform, expand around the VEV, and compute the third functional
derivative that defines the physical trilinear vertex.  This is the cleanest
repair target because it attacks the exact audit objection rather than adding
more arithmetic.

Current status: partially reduced.  The SSB VEV-division algebra is closed as
an exact subderivation; the source-to-canonical-Higgs normalization `kappa_H`
remains open.

## R2. Ward Operator-Matching Candidate

Score: 11/18. Hard-residual pressure: 2.

Compute the independent tree-level factors: scalar singlet, physical trilinear
component, HS residue, chirality factor, and SSB convention.  This now exists
as `scripts/frontier_yt_ward_operator_matching_candidate.py`.

Outcome: conditional-support.  It narrows the blocker but does not close it.

## R3. Scalar LSZ / Connected Trace Bridge

Score: 10/18. Hard-residual pressure: 3.

Repair the `Z_phi` bridge by proving that the connected color trace is the
physical scalar LSZ residue, not only a hard-coded channel ratio.  This would
retire one of the open imports but still depends on R1.

Current status: exact negative boundary for deriving LSZ from `R_conn` alone.
The full scalar pole-residue theorem remains open.

## R6. Source-Higgs `kappa_H` Residue Theorem

Score: 13/18. Hard-residual pressure: 3.

Compute the scalar source two-point residue and decide whether the canonical
Higgs normalization factor `kappa_H` is forced to one.  This is now the narrow
successor to R1 after the SSB bookkeeping reduction.

Current status: exact negative boundary for counts+SSB selection.  The route
proved `kappa_H` requires a two-point residue / LSZ theorem.

## R7. Scalar LSZ / Two-Point Residue Theorem

Score: 12/18. Hard-residual pressure: 3.

Derive the scalar source pole residue and show whether it fixes the canonical
field normalization.  This is now the direct successor to R6.

Current status: open.

## R4. Chirality and Right-Handed Selector Theorem

Score: 9/18. Hard-residual pressure: 2.

Use retained hypercharge and one-generation matter closure to force the
`Q_L(up) -> u_R` and `Q_L(down) -> d_R` selector without using the old
matrix-element identification.

Current status: conditional-support.  The selector arithmetic is complete over
the four one-Higgs hypercharge candidates, but parent statuses are non-clean.

## R5. Direct MC Production

Score: 5/18. Hard-residual pressure: 4.

Run production gauge + staggered-fermion correlator measurement.  This remains
the cleanest empirical route but is too large for the current foreground loop
and does not repair the Ward proof.

Current status: parked as production evidence route, not PR #230 closure today.
