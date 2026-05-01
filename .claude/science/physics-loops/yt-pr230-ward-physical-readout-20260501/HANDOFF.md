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
- The stronger scalar pole-residue current-surface no-go shows that identical
  current-visible algebraic data can produce distinct physical `y_t/g_s`
  readouts when pole residue/dressing vary.
- A retained-closure route certificate now records the shortest honest closure
  routes.
- The direct measurement route now has a scale requirement: current scale gives
  `am_top = 81.423`, so a relativistic direct measurement needs roughly `81x`
  finer inverse lattice spacing for `am_top <= 1`, or an HQET/top-integrated
  route.

The scientific result is narrower than closure:

```text
Current PR #230 status: open / conditional-support.
The normalization 1/sqrt(6) is not the hard blocker.
The hard blockers are now sharply separated.  For retained closure, PR #230
needs either strict physical measurement evidence or a real scalar two-point
pole-residue/common-dressing theorem.  The normalization arithmetic, SSB
bookkeeping, and wording around the old Ward note are not enough.
```

Exact next action:

```text
Package this PR #230 update.  The remaining positive options are now:

1. strict direct physical measurement at a suitable top/heavy-quark scale;
2. scalar pole-residue/common-dressing theorem from retained dynamics;
3. a newly derived Planck stationarity selector.
```

Acceptance target for the next block:

1. Define the scalar-bilinear source functional.
2. Compute the scalar two-point residue / external-leg normalization or prove
   that the current data do not fix it.
3. Decide whether a clean scalar LSZ theorem can select `kappa_H`.
4. Keep the status open unless all source, carrier, chirality, LSZ, and common
   dressing imports are retired.
