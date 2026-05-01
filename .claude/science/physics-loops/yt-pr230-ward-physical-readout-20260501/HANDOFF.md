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
- The campaign status certificate now collects the current PR #230 route
  certificates and verifies that none authorizes retained-proposal wording.
  The live status is still open; the remaining routes are production evidence,
  a new scalar LSZ/canonical-normalization theorem, or a new heavy-matching
  observable/theorem.
- The scalar ladder IR/zero-mode obstruction now shows that even holding the
  scalar source fixed, the finite Wilson-exchange ladder pole test can flip
  under the open gauge-zero-mode, IR-regulator, and finite-volume prescription.
  A finite `lambda_max >= 1` witness is therefore not load-bearing until a
  limiting theorem fixes those choices.
- The heavy kinetic-mass scout supplies the constructive route around the
  static additive-mass obstruction: use nonzero-momentum energy differences
  `E(p)-E(0)` to extract `M_kin`.  This cancels the additive shift, but pure
  static correlators have no kinetic splitting and a top-like heavy mass needs
  very high energy-splitting precision plus a matching theorem.
- The nonzero-momentum correlator scout now reuses the production harness
  Dirac/CG primitives and constructs cos-projected momentum correlators on a
  tiny cold gauge field.  The extracted energy splittings are ordered and give
  finite kinetic-mass proxies, so the next engineering step is production
  support for momentum projection plus matching.
- The production harness now has optional `--momentum-modes` support and emits
  `momentum_analysis` certificate fields.  A reduced-scope `4^3 x 8` smoke run
  produced finite kinetic-mass proxies, but the validation runner explicitly
  keeps this at bounded-support status.
- The heavy kinetic matching obstruction shows why the kinetic route is not
  retained closure yet: a measured `E(p)-E(0)` fixes a kinetic combination, and
  changing `c2` or the lattice-to-SM matching factor changes the inferred SM
  top mass without changing the measured splitting.
- A bounded small-volume momentum pilot now exists through `8^3 x 16`.  It
  emits finite kinetic proxies, but the full `p_min` proxy has relative spread
  `0.950562`, so reduced cold-gauge pilots are exhausted as closure evidence.
- The assumptions/import exercise has been refreshed and made executable.  It
  explicitly forbids `H_unit`, observed target values, alpha/plaquette/u0,
  reduced pilots, and undeclared `c2`/`Z_match` shortcuts.
- The free Wilson-staggered kinetic coefficient is now exact support:
  `M_kin^free = m sqrt(1+m^2)`.  This is a positive route movement, but it
  leaves interacting kinetic renormalization and SM matching open.
- The interacting kinetic background sensitivity block shows that the
  nonzero-momentum kinetic proxy changes across small fixed SU(3) gauge
  backgrounds.  Therefore the free kinetic coefficient cannot be used as a
  zero-import interacting `c2` replacement; this route needs ensemble evidence
  or a retained interacting kinetic/matching theorem.
- The scalar LSZ normalization-cancellation block shows a constructive repair
  to the source-scaling obstruction: in a covariant scalar channel,
  `O -> c O` scales the bubble, vertex, and inverse-residue so that the
  canonical `vertex/sqrt(Z_inverse)` proxy is invariant.  This removes source
  naming as the final blocker but leaves the interacting denominator, pole
  location, finite-volume/IR limit, and residue derivative open.
- The Feshbach operator-response block shows exact low-energy projection
  preserves both scalar and gauge responses when operators are transformed
  consistently.  This rules out crossover distortion as the main blocker, but
  it does not derive equality of the underlying scalar and gauge microscopic
  residues.
- The retained-closure route certificate has been refreshed to include the
  newer LSZ covariance, Feshbach response, and interacting kinetic sensitivity
  checks.  It now passes `PASS=12 FAIL=0` and still authorizes no retained
  proposal wording.
- The axiom-first / constructive UV bridge stack has been audited as the main
  possible missed proof.  It is not PR230 closure: it is bounded transport
  support, imports accepted `y_t(v)` or accepted plaquette/`u_0` surfaces, and
  its ledger rows are bounded, unaudited, or audited conditional.
- The scalar spectral-saturation block shows positivity and fixed low-order
  source-curvature data do not determine the isolated scalar pole residue.
  Multiple positive pole-plus-continuum models share `C(0)` and `C'(0)` while
  changing the canonical Yukawa proxy.

The scientific result is narrower than closure:

```text
Current PR #230 status: open / conditional-support.
The normalization 1/sqrt(6) is not the hard blocker.
The hard blockers are now sharply separated.  For retained closure, PR #230
needs either strict physical measurement evidence with a valid heavy-mass
matching bridge or a real interacting scalar-channel
Bethe-Salpeter/projector/pole-residue theorem with controlled zero-mode and
IR/finite-volume limits.  The normalization arithmetic, SSB bookkeeping, free
source bubble, source Legendre transform, kinematic scalar/gauge factorization,
static rephasing, same-1PI coefficient equality, finite ladder eigenvalue
scouts, contact HS rewrite, and wording around the old Ward note are not enough.
```

Exact next action:

```text
Package this PR #230 update.  The remaining positive options are now:

1. strict direct physical measurement at a suitable top/heavy-quark scale with
   additive-mass/interacting-kinetic/matching control supplied by an
   independent observable or theorem;
2. interacting scalar denominator/pole-residue/common-dressing theorem from
   retained dynamics;
3. a newly derived Planck stationarity selector.
```

Acceptance target for the next heavy-kinetic block:

1. Implement a nonzero-momentum correlator scout that extracts `E(p)-E(0)`.
2. If pursuing closure rather than engineering, derive the interacting kinetic
   coefficient and lattice-HQET/NRQCD-to-SM matching import.
3. Otherwise pivot back to the scalar LSZ/pole-residue theorem.
