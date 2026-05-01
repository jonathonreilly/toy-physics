# Handoff

Block 1 completed the Ward-route triage for PR #230.

What changed:

- The repo-wide YT audit found no hidden retained top-Yukawa proof.
- The Ward physical-readout repair target is now executable and explicit.
- The tree-level normalization arithmetic was isolated in a conditional
  operator-matching candidate.
- The SSB VEV-division substep was reduced: for a canonical Higgs doublet,
  `sqrt(2) m/v` recovers the doublet coefficient with no extra factor.
- `kappa_H = 1` was ruled out as a consequence of counts plus SSB alone.
  It requires a scalar two-point residue / LSZ theorem.
- `R_conn = 8/9` was separated from the scalar LSZ pole residue: the channel
  ratio does not by itself fix the external-leg factor.
- The chirality/right-handed selector was reduced to gauge arithmetic:
  `Qbar_L H_tilde u_R` and `Qbar_L H d_R` are the unique invariant one-Higgs
  terms, conditional on non-clean matter/hypercharge parents.
- Common scalar/gauge dressing was shown to be an extra theorem: the current
  Ward/gauge identities do not force `Z_scalar = Z_gauge`.

The scientific result is narrower than closure:

```text
Current PR #230 status: open / conditional-support.
The normalization 1/sqrt(6) is not the hard blocker.
The hard blockers are now sharply separated: scalar pole-residue normalization,
scalar carrier identification, non-clean parent repair for chirality, and
common dressing.  The normalization arithmetic and SSB bookkeeping are not the
hard part.
```

Exact next action:

```text
Package this PR #230 update.  The remaining positive options are now either a
real scalar pole-residue/common-dressing theorem or the direct production MC
measurement route.
```

Acceptance target for the next block:

1. Define the scalar-bilinear source functional.
2. Compute the scalar two-point residue / external-leg normalization or prove
   that the current data do not fix it.
3. Decide whether a clean scalar LSZ theorem can select `kappa_H`.
4. Keep the status open unless all source, carrier, chirality, LSZ, and common
   dressing imports are retired.
