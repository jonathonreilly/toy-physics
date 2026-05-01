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
- A direct key-blocker closure attempt checked all plausible repo authorities
  for scalar pole-residue/common-dressing closure.  None closes it; the exact
  required theorem is now named.
- The scalar source two-point stretch derives the exact logdet curvature as a
  fermion bubble and proves the free residue proxy is not universal.
- The stuck fan-out rejects the finite-volume near-match to `1/sqrt(6)` and
  selects the HS/RPA pole equation as the constructive successor.
- The contact HS/RPA route is blocked unless a scalar-channel coupling/kernel
  theorem is derived from Wilson gauge exchange.
- A finite scalar-channel ladder scout now exists.  It shows the eigenvalue
  machinery but also shows mass/IR/projector sensitivity.
- The full-staggered PT formula layer has been audited for PR #230 reuse:
  `D_psi`, `D_gluon`, and the scalar/gauge kinematic form factor are usable as
  formulas, while alpha/plaquette/`H_unit` surfaces remain forbidden proof
  inputs.
- The scalar ladder projector-normalization obstruction is now explicit:
  source rescaling changes `lambda_max` quadratically, and raw versus
  zero-momentum-normalized point-split projectors can flip the scout pole
  criterion.
- The HQET/static direct-route shortcut is now bounded: it removes the
  numerical `am_top >> 1` problem by rephasing away the absolute heavy rest
  mass, so absolute `m_t` and `y_t` still need a static additive-mass and
  lattice-HQET-to-SM matching theorem.
- The formal static matching obstruction is now explicit: `am0 + delta_m` is
  nonunique after rephasing, and the same subtracted correlator supports
  different absolute top masses.
- The Legendre/source route is now bounded at the normalization level:
  source/field rescaling preserves the Legendre transform while changing
  curvature and `y_readout`, so `kappa_H` needs a pole-residue or canonical
  kinetic theorem.
- The free momentum-dependent scalar source bubble is also bounded: it is
  finite and positive with no inverse-curvature zero, so an isolated scalar pole
  requires an interacting denominator or production evidence.
- The same-1PI route is also bounded: a fixed four-fermion coefficient controls
  `y^2 D_phi`, not `y` and scalar LSZ normalization separately, and the existing
  same-1PI notes still depend on H_unit/Rep-B matrix-element data.

The scientific result is narrower than closure:

```text
Current PR #230 status: open / conditional-support.
The normalization 1/sqrt(6) is not the hard blocker.
The hard blockers are now sharply separated.  For retained closure, PR #230
needs either strict physical measurement evidence with a valid heavy-mass
matching bridge or a real interacting scalar-channel
Bethe-Salpeter/projector/pole-residue theorem.  The normalization arithmetic,
SSB bookkeeping, free source bubble, source Legendre transform, kinematic
scalar/gauge factorization, static rephasing, same-1PI coefficient equality,
contact HS rewrite, and wording around the old Ward note are not enough.
```

Exact next action:

```text
Package this PR #230 update.  The remaining positive options are now:

1. strict direct physical measurement at a suitable top/heavy-quark scale with
   additive-mass/matching control supplied by an independent observable or
   theorem;
2. scalar projector/pole-residue/common-dressing theorem from retained
   dynamics;
3. a newly derived Planck stationarity selector.
```

Acceptance target for the next block:

1. Derive the exact scalar-channel Wilson-staggered scalar projector/source
   normalization.
2. Derive the scalar ladder kernel with controlled IR and finite-volume limits.
3. Prove or disprove eigenvalue crossing on the current authority surface.
4. If crossing is proven, compute the pole residue from the eigenvalue
   derivative and re-run the Ward physical-readout repair audit.
