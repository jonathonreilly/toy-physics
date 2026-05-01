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

Update: direct key-blocker closure attempt checked the existing Ward, color,
SSB, LSZ, common-dressing, one-Higgs, EW-Higgs, taste-scalar, and neutrino
two-point analogue authorities.  None supplies the top-sector scalar pole
residue and relative scalar/gauge dressing.  A new theorem or measurement is
required.

Campaign stretch update: the scalar source two-point curvature is now derived
as an exact logdet fermion bubble.  The free Wilson-staggered residue proxy is
not stable enough to select `kappa_H = 1`.  The fan-out selected the HS/RPA
pole route, but the contact version needs an extra scalar-channel coupling.
The constructive successor is the full scalar-channel Bethe-Salpeter ladder
kernel theorem.

Projector update: the full-staggered PT formula layer supplies exact
staggered/Wilson kinematics, including a shared scalar/gauge point-split factor,
but the ladder pole criterion changes under scalar source/projector
normalization.  Therefore R7 still needs a scalar LSZ/source-normalization
theorem before R8 can be load-bearing.

Legendre update: the source Legendre transform does not remove the
normalization freedom.  `W_k(J)=W(kJ)` preserves the Legendre relation while
scaling the curvature and `y_readout`; the positive target is specifically a
momentum-dependent pole residue or canonical kinetic normalization theorem.

Free two-point update: the finite Wilson-staggered logdet bubble is positive
and finite with no inverse-curvature zero on the scanned surfaces.  The route
therefore needs an interacting scalar denominator, not only the free source
curvature.

## R8. Scalar-Channel Bethe-Salpeter Kernel Theorem

Score: 10/18. Hard-residual pressure: 4.

Derive the exact scalar-channel Wilson-staggered ladder kernel, scalar
projector, IR/finite-volume limit, eigenvalue crossing, and pole-residue
derivative.  A finite scout exists and shows the machinery, but also shows
strong dependence on mass and IR/projector choices.

Current status: bounded support / scout only, with an exact negative boundary
against treating point-split/gauge kinematic equality as physical LSZ readout.

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

Update: the HQET/static shortcut was checked.  It can remove the numerical
`am_top >> 1` cutoff in the correlator, but only by rephasing away the absolute
heavy rest mass.  Absolute `m_t` and `y_t` then require static additive-mass and
lattice-HQET-to-SM matching.  This is a production strategy, not a current
closure route.

Static matching update: the residual-mass decomposition `am0 + delta_m` is
nonunique after static rephasing.  The same subtracted correlator supports
different absolute top masses and therefore different `y_t` values until a
separate matching condition fixes the physical sum.
