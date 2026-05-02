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
- The large-`N_c` pole-dominance block shows asymptotic pole dominance is not
  enough at physical `N_c=3`.  A natural `1/N_c^2` continuum allowance shifts
  the canonical Yukawa proxy by more than five percent.
- The production resource projection converts the existing `12^3 x 24`
  numba mass-bracket benchmark into a concrete strict-campaign estimate:
  the requested three-volume, three-mass protocol projects to about
  `228.48` single-worker hours.  This keeps the direct route actionable as a
  planned production job, but it is not production evidence and cannot make the
  strict runner pass.
- The Feynman-Hellmann scalar-response block opens a distinct observable route:
  top-energy slopes with respect to a uniform scalar source cancel additive
  rest-mass shifts.  The route still does not close PR #230 because the slope
  is with respect to a chosen lattice source; converting it to `dE/dh` requires
  scalar source-to-Higgs normalization, scalar LSZ residue, and production
  response data.
- The mass-response bracket certificate extracts the same idea from existing
  reduced `12^3 x 24` correlator data: fitted energies are monotone in
  `m_bare` and give positive local `dE/dm_bare` slopes.  This is useful
  lightweight evidence for the observable design, but it is reduced-scope and
  bare-source only.
- The source-reparametrization gauge block formalizes the hard boundary:
  source curvature, same-1PI products, and Feynman-Hellmann slopes are
  covariant under scalar source rescaling.  They cannot produce a physical
  Yukawa readout unless a canonical scalar normalization / LSZ residue is
  derived or directly measured.
- The canonical scalar-normalization import audit checks the strongest existing
  EW/Higgs candidates.  They do not hide the missing theorem: the EW gauge-mass
  note assumes canonical `|D H|^2`, the SM one-Higgs note leaves Yukawa values
  free, observable-principle remains audited conditional, and `R_conn`/EW color
  projection do not derive scalar LSZ.
- The explicit source-to-Higgs / LSZ closure attempt lists every allowed
  premise that could fix `kappa_s`.  None does.  The named open theorem is now
  precise: derive an isolated scalar pole, its residue / inverse-propagator
  derivative, and the match to the canonical kinetic normalization used by
  `v`, without forbidden imports.
- The scalar-source response harness extension now makes the
  Feynman-Hellmann route executable inside the production harness:
  `--scalar-source-shifts` emits `scalar_source_response_analysis` and a
  finite reduced-smoke `dE/ds` slope.  This is bounded support only.  It does
  not derive `dE/dh`, and `kappa_s = 1` remains forbidden until scalar
  LSZ/canonical normalization is derived.
- The Feynman-Hellmann production protocol is now specified: measure symmetric
  source shifts on the same saved gauge configurations, fit correlated
  `dE_top/ds`, and separately measure/derive `kappa_s` from the same-source
  scalar two-point LSZ/canonical-normalization problem.
- The same-source scalar two-point measurement primitive now computes
  `C_ss(q)=Tr[S V_q S V_-q]` and `Gamma_ss(q)=1/C_ss(q)` for the additive
  source used in `dE_top/ds`.  It identifies the LSZ measurement object, but
  the reduced cold primitive has no controlled scalar pole and does not fix
  `kappa_s`.
- The scalar Bethe-Salpeter kernel/residue degeneracy block shows that even if
  an isolated scalar pole is granted, finite same-source Euclidean samples do
  not fix the pole derivative.  Analytic denominator deformations can preserve
  every measured `Gamma_ss(q)` value and the pole location while moving
  `dGamma/dp^2`; natural `1/N_c^2` remainders at `N_c=3` move the `kappa_s`
  proxy by more than five percent.
- The production harness now has a stochastic same-source scalar two-point
  estimator.  `--scalar-two-point-modes` plus `--scalar-two-point-noises`
  emits `C_ss(q)`, `Gamma_ss(q)`, and a finite-difference residue proxy for the
  same additive scalar source used by `dE_top/ds`.  This is production-facing
  measurement support, not closure: reduced smoke output is not production
  evidence and no controlled pole/canonical-Higgs normalization is derived.
- The joint Feynman-Hellmann/scalar-LSZ harness certificate now shows the
  production harness can emit both required observables in one run:
  `dE_top/ds` from symmetric source shifts and same-source `C_ss(q)` /
  `Gamma_ss(q)` for `kappa_s`.  This defines the exact production measurement
  bundle; it remains bounded support until production data and a controlled
  scalar-pole/canonical-LSZ normalization exist.
- The joint FH/LSZ resource projection converts that bundle into a compute
  estimate.  With four scalar-LSZ momentum modes and sixteen noise vectors per
  configuration, the solve budget is about `15.8889x` the existing three-mass
  direct projection, or about `3630.28` single-worker hours before extra
  autocorrelation and pole-fit tuning.
- The Feynman-Hellmann/scalar-LSZ invariant readout theorem proves the
  same-source response formula:
  `y_proxy = (dE_top/ds) * sqrt(dGamma_ss/dp^2 at the pole) =
  dE_top/ds / sqrt(Res[C_ss])`.  This retires the `kappa_s = 1` shortcut as
  unnecessary and forbidden: `kappa_s` is measured by the pole overlap.  It is
  exact support only, because the same-source production pole data are absent.
- The scalar pole determinant gate localizes the remaining theorem to the
  interacting denominator.  In one-channel notation, `D(x)=1-K(x)Pi(x)` and a
  pole needs `D(x_pole)=0`, but the LSZ derivative contains
  `K'(x_pole)`.  Holding the pole location fixed while changing `K'(x_pole)`
  changes the residue, so pole naming is not enough.
- The scalar ladder eigen-derivative gate gives the matrix version: a finite
  `lambda_max(pole)=1` witness is only a pole-location condition.  The residue
  and FH/LSZ readout need `d lambda_max/dp^2`, which varies with the
  momentum-dependent ladder kernel even when the pole eigenvalue is fixed.
- The scalar ladder total-momentum derivative scout computes that derivative
  in a finite Wilson-exchange model.  The derivative is finite and negative
  across the scan, but its magnitude is strongly sensitive to projector,
  zero-mode, IR regulator, mass, and volume choices.  This is constructive
  machinery, not a limiting theorem.
- The scalar ladder derivative limiting-order obstruction shows why that
  finite derivative cannot yet be used as LSZ input: retaining the gauge zero
  mode makes the derivative grow as the IR regulator is lowered and changes
  the pole crossing, while removing the zero mode gives a different stable
  surface.
- The Cl(3)/Z3 source-unit normalization no-go checks the substrate-level
  premise directly.  Unit lattice spacing, unit Clifford generators, `g_bare=1`,
  and the additive source coefficient define the source coordinate `s`, not
  the canonical Higgs field metric.  `kappa_s=1` remains forbidden without a
  pole/kinetic theorem.
- The joint FH/LSZ production manifest now gives exact three-volume,
  production-targeted, resumable commands for the production route.  It is a
  launch surface only: no production output, pole fit, or retained proposal
  certificate exists.
- The FH/LSZ production postprocess gate now blocks manifest or partial-output
  evidence claims.  It requires production-phase output, same-source
  `dE/ds`, same-source `Gamma_ss(q)`, an isolated scalar-pole derivative,
  FV/IR/zero-mode control, and a retained-proposal certificate before any
  physical `y_t` wording is allowed.
- The FH/LSZ production checkpoint-granularity gate shows the current harness
  resumes only completed per-volume artifacts.  The smallest projected joint
  shard is `180.069` hours, so a 12-hour foreground launch is not safely
  checkpointed production evidence.
- The FH/LSZ chunked production manifest gives a foreground-sized L12
  scheduling surface: 63 production-targeted chunks of 16 saved
  configurations, estimated at `11.3186` hours each.  This is not production
  evidence and does not cover L16/L24 or scalar pole postprocessing.
- The retained-closure route certificate has been refreshed against the new
  source-unit, derivative-limit, production-manifest, postprocess-gate, and
  checkpoint-granularity and chunked-manifest
  blocks.  It still reports `proposal_allowed=false`; the remaining positive routes are
  production evidence or a scalar pole/common-dressing theorem.
- The scalar ladder residue-envelope obstruction normalizes away pole-location
  ambiguity by tuning each finite ladder to its own pole.  Even then, the
  residue proxy remains zero-mode, source-projector, and finite-volume
  dependent.  A finite ladder envelope is not a scalar-LSZ/canonical-Higgs
  theorem.
- The scalar-kernel Ward-identity obstruction checks the next possible
  shortcut.  Current Ward/gauge/Feshbach surfaces fix neither `K'(x_pole)` nor
  common scalar/gauge dressing.  A same-pole kernel family changes the scalar
  LSZ readout factor while preserving `D(x_pole)=0`.

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

Exact next action after the residue-envelope checkpoint:

```text
Continue the campaign from the remaining positive options:

1. strict direct physical measurement at a suitable top/heavy-quark scale with
   additive-mass/interacting-kinetic/matching control supplied by an
   independent observable or theorem; current single-worker projection is
   multi-day, not 12-hour foreground closure;
2. interacting scalar denominator/pole-residue/common-dressing theorem from
   retained dynamics, including zero-mode/IR/finite-volume control and a
   finite-`N_c=3` pole-residue bound;
3. Feynman-Hellmann scalar-response production measurement plus a derived
   scalar-source normalization bridge;
4. a newly derived Planck stationarity selector.
```

Acceptance target for the next heavy-kinetic block:

1. Implement a nonzero-momentum correlator scout that extracts `E(p)-E(0)`.
2. If pursuing closure rather than engineering, derive the interacting kinetic
   coefficient and lattice-HQET/NRQCD-to-SM matching import.
3. Otherwise pivot back to the scalar LSZ/pole-residue theorem.

Acceptance target for the next scalar-response block:

1. Design the production `dE/ds` source-response protocol using the new
   `--scalar-source-shifts` harness path.
2. Derive or measure the scalar source-to-canonical-Higgs normalization
   `kappa_s`; do not set `kappa_s = 1`.
3. Keep reduced source-response runs as scouts only until production and
   matching certificates exist.

The protocol block completed item 1.  The same-source two-point block reduces
item 2 to the controlled-pole/residue theorem, and the harness extension makes
that measurement executable on future production ensembles.  The joint harness
block verifies the combined command path.  Items 2 and 3 remain active.
The resource projection says the exact next action is a scheduled production
job or a scalar pole theorem, not more reduced foreground smoke.
The invariant-readout theorem says the exact scalar theorem target is now the
existence/control of the same-source scalar pole and derivative, not a separate
source naming convention.
The determinant-gate block says the exact analytic object is now the
interacting scalar-channel kernel `K(x)` and its derivative at the pole.
The eigen-derivative block says the same in matrix language: derive or measure
the total-momentum derivative of the scalar Bethe-Salpeter kernel.
The total-momentum derivative scout says this derivative is computable in a
finite model, but the current route still needs the retained prescription and
limit theorem or production pole data.
The derivative limiting-order obstruction makes the missing theorem explicit:
the zero-mode/IR prescription must be derived before the derivative can carry
scalar LSZ normalization.
The source-unit no-go makes the parallel functional point explicit: Cl(3)/Z3
unit conventions alone do not turn the additive source coordinate into the
canonical Higgs field.
The production-manifest block makes the empirical route resumable; running it
is a multi-day compute action, not a foreground proof.
The refreshed retained-closure gate is the current claim firewall: no retained
or proposed-retained wording is allowed until production or theorem evidence
changes that certificate.  The residue-envelope block says the next analytic
move must be the actual interacting denominator/zero-mode/IR/finite-volume
limit theorem, not another finite ladder witness.  The Ward-kernel block says
the old Ward/Feshbach surfaces cannot substitute for that theorem.  The
zero-mode limit-order block makes the limiting theorem concrete: retaining the
gauge zero mode adds an exact `1/(V mu_IR^2)` diagonal term, so taking the IR
limit first, volume first, or a box-scaled regulator path gives different
scalar denominators unless a prescription is derived.  The zero-mode
prescription import audit checks the strongest current PT,
continuum-identification, manifest, and scalar-ladder surfaces; none supplies
that prescription.  The flat-toron block shows why trivial-sector selection is
not automatic: constant commuting Cartan links have zero plaquette action but
change scalar denominator proxies through Polyakov phases.  The flat-toron
thermodynamic washout block gives positive support: fixed-holonomy flat-sector
dependence vanishes for the local massive scalar bubble as `N -> infinity`.
The remaining denominator blocker is therefore the interacting scalar pole and
massless gauge-zero-mode/IR prescription, not this finite-volume toron artifact
by itself.  The color-singlet zero-mode cancellation block then removes the
exact `q=0` gauge mode from the singlet denominator: total color charge
annihilates the scalar singlet, and self plus exchange pieces cancel.  The
live analytic blocker is now finite-`q` IR behavior and the interacting pole
derivative in that color-singlet kernel.  The finite-`q` IR regularity block
then removes the remaining massless IR divergence concern: after `q=0`
cancellation, `d^4q/q^2` is locally integrable.  The live blocker is now the
interacting color-singlet scalar pole location and inverse-propagator
derivative, or production FH/LSZ data.  The zero-mode-removed ladder pole
search checks that narrowed surface directly: finite small-mass pole witnesses
exist, but they are volume, projector, taste-corner, and derivative sensitive.
The live blocker is now a continuum/taste/projector theorem for the
interacting color-singlet scalar denominator and LSZ derivative, or production
pole data.  The taste-corner obstruction sharpens that further: the finite
crossings are dominated by non-origin Brillouin-zone corners and disappear
under a physical-origin-only filter, so a taste/scalar-carrier theorem is
load-bearing before any finite crossing can be used.  The taste-carrier import
audit checks the current ledger candidates and finds no retained authority:
CL3 taste generation is a physical-identification boundary, taste-scalar
isotropy is conditional for scalar-spectrum consequences, full staggered PT is
conditional and imports non-clean normalization surfaces, and the ladder input
audit still lists the scalar color/taste/spin projector as missing.  The
taste-singlet normalization boundary then checks the constructive singlet
normalization: applying normalized source weight over the 16 BZ corners divides
each finite witness by `16` and removes every crossing.  The live blocker is
therefore a retained scalar taste/projector normalization theorem plus the
interacting pole derivative, or production same-source FH/LSZ pole data.  The
scalar taste/projector theorem attempt now separates the algebraic and
physical parts: the unit taste singlet `O_singlet=(1/sqrt(16)) sum_t O_t` is
available, but the source term can absorb the same factor into the source
coordinate and no current retained authority identifies the physical scalar
carrier or derives `K'(x_pole)`.  The unit-projector pole-threshold block then
shows the normalized finite ladder has no crossing at retained scout strength:
the best row has `lambda_max=0.442298920672` and would need an underived
scalar-kernel multiplier `2.26091440260` to reach `lambda_max=1`.  The
scalar-kernel enhancement audit checks HS/RPA contact coupling, ladder input
formulae, same-1PI, and Ward/Feshbach response identities; none supplies that
multiplier or `K'(x_pole)` on the retained current surface.
The fitted-kernel residue selector no-go closes the next possible shortcut:
choosing `g_eff = 1/lambda_unit` to force a finite pole imports the missing
scalar normalization, and the resulting residue proxy remains finite-row
dependent.

The FH/LSZ chunk-combiner gate now closes the procedural gap left by the L12
chunk manifest.  Future L12 chunks must expose `metadata.run_control` seed and
command provenance, production phase, same-source `dE/ds`, and same-source
`C_ss(q)` before the branch can construct even an L12 combined summary.  The
current gate finds `0` present / `0` ready chunks.  L12-only remains
non-retained because L16/L24 scaling, isolated scalar-pole inverse derivative,
FV/IR/zero-mode control, and retained-proposal certification are still open.
The chunk launch commands have also been tightened: each command now uses a
chunk-local `--production-output-dir` and `--resume`, so future
`ensemble_measurement.json` artifacts cannot collide across chunks.
The first chunk launch also exposed a pure CLI preflight bug: negative scalar
source shifts must be passed with equals syntax.  The production and chunk
manifest emitters now use `--scalar-source-shifts=-0.01,0.0,0.01`, so the next
exact action can relaunch chunk001 under the non-evidence combiner gate.
Chunk001 has been relaunched as non-evidence.  In parallel, the FH/LSZ pole-fit
kinematics gate shows the current scalar modes provide only one nonzero
momentum shell; they are not sufficient to determine an isolated scalar-pole
inverse derivative without richer pole-fit kinematics or a theorem.
The pole-fit mode/noise budget gives a concrete next production design:
eight modes with eight noises keep the current L12 foreground estimate while
adding enough shells for pole-fit kinematics.  It is still planning support
and needs a variance gate before launch.

The eight-mode noise variance gate now blocks using that x8 option as
production-facing evidence on the current surface.  Dropping from sixteen to
eight stochastic vectors raises the scalar-LSZ noise-only stderr by `sqrt(2)`,
and no same-source production x8/x16 calibration is present.  The reduced
smoke output is wrong phase, wrong volume, two modes, two noises, and one
configuration.  Chunk001 is absent until completion and, by construction, is
four-mode/x16 rather than an eight-mode/x8 calibration.

The production harness now emits `noise_subsample_stability` diagnostics in
the scalar-LSZ analysis and each mode row.  The scalar-only and joint smokes
were rerun to validate the field shape.  This is instrumentation support for a
future paired x8/x16 calibration, not a production variance result.
The paired variance calibration manifest now gives exact x8 and x16 L12
commands with matched seed, source shifts, eight scalar-LSZ modes, and separate
artifact directories.  This is still launch planning; no calibration output is
present.

The gauge-VEV source-overlap no-go now closes the shortcut of using electroweak
`v` or gauge-boson masses to set `kappa_s=1`.  Those surfaces fix the metric of
an already identified canonical Higgs field; they do not derive the overlap
`h = kappa_s s` for the Cl(3)/Z3 scalar source.

The scalar renormalization-condition source-overlap no-go closes the adjacent
kinetic-normalization shortcut.  Canonical `Z_h=1` fixes the `h`-field pole
residue but not the source operator matrix element `<0|O_s|h>`.  The same
canonical Higgs sector can support different source responses unless the
same-source pole residue is measured or derived.

The scalar source contact-term scheme boundary closes the low-momentum
curvature-renormalization shortcut.  Source contact terms can enforce the same
`C_ss(0)` and `C_ss'(0)` convention for different pole residues, so
contact-normalized curvature is not a source-to-Higgs normalization.

The FH/LSZ scalar-pole fit postprocessor scaffold now gives future combined
production output a concrete fit path.  It requires zero plus at least three
positive momentum shells and an isolated negative-`p_hat^2` pole before using
`dGamma_ss/dp^2`; the current combined input is absent/nonready.

Next exact action: keep chunk001 running under the non-evidence combiner gate.
If it finishes, run the chunk combiner and write a partial-chunk checkpoint.
If it remains running, continue analytic scalar denominator/residue work or
schedule the paired x8/x16 calibration if compute is available.
