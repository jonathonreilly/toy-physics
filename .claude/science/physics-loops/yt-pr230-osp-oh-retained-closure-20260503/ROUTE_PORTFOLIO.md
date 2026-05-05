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

Status: best next positive route, with the unratified-Gram shortcut now closed
negatively in
`docs/YT_SOURCE_HIGGS_UNRATIFIED_GRAM_SHORTCUT_NO_GO_NOTE_2026-05-05.md`.
Requires a real same-surface `O_H` operator identity and normalization
certificate before production rows can be audited as the canonical radial
observable.

Cycle-3 update: the current-primitives stretch attempt for that identity and
normalization certificate is also closed negatively in
`docs/YT_CANONICAL_OH_PREMISE_STRETCH_NO_GO_NOTE_2026-05-05.md`.  Source-Higgs
is no longer the best immediate non-chunk executable route unless a new
same-surface `O_H` surface appears.

Reason: perfect `C_ss/C_sH/C_HH` Gram purity against an unratified supplied
operator certifies only that supplied operator; it does not identify PR230
canonical `O_H`.

## R3: Same-Source W/Z Response

Measure a W/Z mass-response row under the same scalar source and use the
response ratio to cancel source normalization.

Status: current best positive non-chunk family only if real same-surface rows
or identity/covariance theorems appear.  Current harness lacks W/Z response
rows and sector-overlap identity certificates; static transport and
Goldstone-equivalence source-identity shortcuts are now closed negatively.

Cycle-4 update: the static-algebra source-coordinate transport shortcut is
closed negatively in
`docs/YT_WZ_SOURCE_COORDINATE_TRANSPORT_NO_GO_NOTE_2026-05-05.md`.  Static
`dM_W/dh` is not a PR230 same-source W row without a same-surface
source-to-Higgs Jacobian certificate.  W/Z remains viable only through real
same-source EW action plus transport and mass-fit rows, measured matched top/W
rows, or a strict same-surface covariance theorem.

Cycle-6 update: the Goldstone-equivalence source-identity shortcut is closed
negatively in
`docs/YT_WZ_GOLDSTONE_EQUIVALENCE_SOURCE_IDENTITY_NO_GO_NOTE_2026-05-05.md`.
Longitudinal-equivalence bookkeeping is not the PR230 source-coordinate
identity.

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
compares five non-chunk families and now records the W/Z
Goldstone-equivalence source-identity no-go as the latest selected shortcut
boundary.
