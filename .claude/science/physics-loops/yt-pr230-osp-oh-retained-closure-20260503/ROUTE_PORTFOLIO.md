# Route Portfolio

## R1: Source-Only O_sp/O_H Identity

Try to derive `O_sp = O_H` from the Legendre source functional, taste support,
EW Higgs notes, and one-Higgs monomial selection.

Status: closed negatively in
`docs/YT_OSP_OH_IDENTITY_STRETCH_ATTEMPT_NOTE_2026-05-03.md`.

Reason: a counterfamily keeps `O_sp` normalized and the same-source top
readout fixed while changing the canonical-Higgs overlap.

## R2: Source-Higgs Gram Purity

Measure `C_sH` and `C_HH` pole residues, using `O_sp` as the normalized source
side, and check

```text
Res(C_sH)^2 = Res(C_ss) Res(C_HH).
```

Status: best next positive route.  Requires a real same-surface `O_H` operator
or a production row that can be audited as the canonical radial observable.

## R3: Same-Source W/Z Response

Measure a W/Z mass-response row under the same scalar source and use the
response ratio to cancel source normalization.

Status: fallback physical-observable route.  Current harness lacks W/Z
response rows and sector-overlap identity certificates.

## R4: Dynamical Rank-One Neutral Scalar Theorem

Prove the neutral scalar response space is rank one so `O_sp` cannot contain
an orthogonal neutral scalar.

Status: currently blocked by commutant, dynamical-rank, and tomography
countermodels.

## R5: Production FH/LSZ Completion

Continue seed-controlled chunks and postprocessing.

Status: useful source-pole evidence only.  Cannot by itself close physical
`y_t` while `O_sp/O_H` remains open.

## R6: Scalar-LSZ Polynomial Contact Repair

Test whether finite polynomial contact subtraction can convert the current
polefit8x8 finite-shell `C_ss` proxy into scalar-LSZ Stieltjes authority.

Status: closed negatively in
`docs/YT_FH_LSZ_POLYNOMIAL_CONTACT_REPAIR_NO_GO_NOTE_2026-05-05.md`.

Reason: low-degree polynomial contacts leave robust higher divided-difference
violations invariant, while degree-seven finite interpolation can manufacture
distinct Stieltjes-looking residuals without identifying the physical contact.
This is an exact negative boundary, not global closure.  A positive scalar
route still needs a same-surface contact-subtraction certificate, microscopic
scalar-denominator theorem, or strict moment-threshold-FV certificate.

Route-family audit: `docs/YT_PR230_NONCHUNK_ROUTE_FAMILY_IMPORT_AUDIT_NOTE_2026-05-05.md`
compared five non-chunk families and selected this block only because it was
the best current executable no-go test.
