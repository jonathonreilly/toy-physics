# Canonical-Higgs Repo Authority Audit

**Status:** exact negative boundary / repo-wide canonical-Higgs `O_H` authority audit
**Runner:** `scripts/frontier_yt_canonical_higgs_repo_authority_audit.py`
**Certificate:** `outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json`

## Purpose

PR #230 now needs one specific object: a same-surface canonical-Higgs radial
operator `O_H`, with identity and normalization certificates strong enough to
support `C_sH` and `C_HH` pole-residue rows.

This audit asks whether that proof already exists elsewhere in the repository
under Higgs, taste-scalar, Ward, source, or electroweak names.

## Result

No existing repo surface satisfies the PR #230 `O_H` certificate schema.

The Higgs/taste stack is useful support, but it does not close the PR230 source
identity:

- `HIGGS_MASS_DERIVED_NOTE.md` is a Higgs quantitative lane with inherited YT
  residuals, not a same-source operator certificate.
- `COMPLETE_PREDICTION_CHAIN_2026_04_15.md` is historical cascade packaging
  around the old Ward/H_unit route, not an independent PR230 source-operator
  proof.
- `CANONICAL_HARNESS_INDEX.md` indexes current note/runner pairs but is not
  proof authority.
- `TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md` proves an exact taste-block
  Coleman-Weinberg isotropy lemma, but it does not select the PR230 scalar
  source direction or LSZ normalization.
- `EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md` assumes a
  canonical Higgs doublet after it is supplied.
- `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md` selects the
  allowed one-Higgs Yukawa monomials but leaves Yukawa values free.
- `H_unit` is explicitly blocked by the audit and by the dedicated candidate
  gate unless pole-purity and canonical-normalization certificates are supplied.

So the auditor did not miss a clean retained `O_H` proof already sitting in the
repo.  The current positive target must be derived or measured directly.

## Next Derivation Target

The exact target is now:

```text
same-surface O_H identity + normalization certificate
```

or the observable equivalent:

```text
Res(C_sH)^2 = Res(C_ss) Res(C_HH)
```

at the isolated scalar pole, with `C_sH` and `C_HH` measured on the same
ensemble and source surface.

## Claim Boundary

This is not retained or `proposed_retained` top-Yukawa closure.  It does not
promote Higgs/taste support to `O_H` authority, does not treat `H_unit` as
`O_H`, and does not set `kappa_s = 1`, `cos(theta) = 1`, `c2 = 1`, or
`Z_match = 1`.

## Verification

```bash
python3 scripts/frontier_yt_canonical_higgs_repo_authority_audit.py
# SUMMARY: PASS=12 FAIL=0
```
