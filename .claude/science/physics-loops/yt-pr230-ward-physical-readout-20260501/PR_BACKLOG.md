# PR Backlog

The block is being added to PR #230 because the user requested the routes be
combined into that draft PR rather than split into separate physics-loop PRs.

Suggested PR body update:

```text
Adds a Ward physical-readout repair block:
- global YT proof inventory: no hidden retained y_t proof found;
- Ward repair audit: old Ward route remains open at source/HS, chirality,
  scalar-carrier, LSZ, and dressing bridges;
- operator-matching candidate: independent tree-level normalizations meet at
  1/sqrt(6), but this is conditional support, not retained closure.

PR #230 remains draft.  Next block attacks the source-to-Higgs Legendre/SSB
bridge.
```

Latest checkpoint text for PR #230:

```text
Adds a scalar-source response harness checkpoint:
- production harness now accepts `--scalar-source-shifts` and emits
  `scalar_source_response_analysis`;
- reduced smoke validator passes `PASS=8 FAIL=0`;
- campaign status now consumes 33 route certificates and reports
  `PASS=29 FAIL=0`;
- this is bounded support for Feynman-Hellmann `dE/ds`, not physical `dE/dh`;
- `kappa_s = 1` remains forbidden unless derived by scalar LSZ/canonical
  normalization.
```

Latest protocol checkpoint text for PR #230:

```text
Adds a Feynman-Hellmann production protocol certificate:
- common-ensemble symmetric source shifts and correlated `dE_top/ds` fits are
  now specified for the strict PR230 volumes;
- validator passes `PASS=9 FAIL=0`; campaign status now consumes 34 route
  certificates and reports `PASS=30 FAIL=0`;
- the protocol identifies the required `kappa_s` fixer: same-source scalar
  two-point LSZ/canonical-normalization measurement;
- still no retained closure and no physical `dE/dh` without derived `kappa_s`.
```

Latest scalar-LSZ measurement checkpoint text for PR #230:

```text
Adds a same-source scalar two-point LSZ measurement primitive:
- computes `C_ss(q)=Tr[S V_q S V_-q]` and `Gamma_ss(q)=1/C_ss(q)` for the
  same additive scalar source used in `dE_top/ds`;
- validator passes `PASS=8 FAIL=0`; campaign status now consumes 35 route
  certificates and reports `PASS=31 FAIL=0`;
- this identifies the measurement object needed to fix `kappa_s`, but the
  reduced cold primitive has no controlled scalar pole/continuum limit and
  does not authorize physical `dE/dh` or retained closure.
```

Latest scalar Bethe-Salpeter residue checkpoint text for PR #230:

```text
Adds a scalar Bethe-Salpeter kernel/residue degeneracy certificate:
- preserves all currently measured same-source `Gamma_ss(q)` finite-mode
  values and a granted scalar pole while moving `dGamma/dp^2` at the pole;
- validator passes `PASS=6 FAIL=0`; campaign status now consumes 36 route
  certificates and reports `PASS=32 FAIL=0`;
- natural `1/N_c^2` denominator remainders at `N_c=3` move the `kappa_s`
  proxy without changing the finite samples;
- still no retained closure: the interacting denominator, finite-volume/IR
  limit, and pole-residue derivative remain open.
```

Latest scalar two-point harness checkpoint text for PR #230:

```text
Adds a scalar two-point production-harness extension:
- `yt_direct_lattice_correlator_production.py` now accepts
  `--scalar-two-point-modes` and `--scalar-two-point-noises`;
- smoke output emits stochastic estimates of same-source `C_ss(q)` and
  `Gamma_ss(q)` plus a finite-difference residue proxy;
- validator passes `PASS=9 FAIL=0`; campaign status now consumes 37 route
  certificates and reports `PASS=33 FAIL=0`;
- this is production-facing support for the `kappa_s` measurement, not
  retained closure; production data, controlled pole/IR limits, and canonical
  Higgs normalization remain open.
```

Latest joint FH/LSZ harness checkpoint text for PR #230:

```text
Adds a joint Feynman-Hellmann / scalar-LSZ harness certificate:
- one reduced smoke run now emits both `dE_top/ds` and same-source
  `C_ss(q)`/`Gamma_ss(q)`;
- validator passes `PASS=10 FAIL=0`; campaign status now consumes 38 route
  certificates and reports `PASS=34 FAIL=0`;
- this defines the exact production observable bundle for the physical-response
  route;
- still no retained closure: production statistics, controlled scalar-pole
  isolation, `dGamma/dp^2`, and canonical-Higgs `kappa_s` remain open.
```

Latest joint FH/LSZ resource checkpoint text for PR #230:

```text
Adds a joint Feynman-Hellmann / scalar-LSZ resource projection:
- modest scalar-LSZ plan: 4 momentum modes and 16 noise vectors/configuration;
- projected solve budget is `15.8889x` the existing three-mass direct
  projection;
- validator passes `PASS=7 FAIL=0`; campaign status now consumes 39 route
  certificates and reports `PASS=35 FAIL=0`;
- projected mass-scaled foreground cost is about `3630` single-worker hours,
  so this is exact next-action planning, not retained closure.
```

Latest FH/LSZ invariant-readout checkpoint text for PR #230:

```text
Adds a Feynman-Hellmann / scalar-LSZ invariant readout theorem:
- proves the same-source formula
  `y_proxy=(dE_top/ds)*sqrt(dGamma_ss/dp^2 at pole)=dE_top/ds/sqrt(Res[C_ss])`;
- validator passes `PASS=7 FAIL=0`; campaign status now consumes 40 route
  certificates and reports `PASS=36 FAIL=0`;
- this removes the need for any `kappa_s = 1` shortcut: `kappa_s` is measured
  by the same-source pole overlap;
- still no retained closure because production response, isolated pole,
  pole derivative, and canonical-Higgs matching remain open.
```

Latest scalar pole determinant-gate checkpoint text for PR #230:

```text
Adds a scalar pole determinant gate:
- isolates the denominator condition `D(x)=1-K(x)Pi(x)` and pole condition
  `D(x_pole)=0`;
- shows pole location fixes `K(x_pole)` but not `K'(x_pole)`, which controls
  the LSZ residue through `D'(x_pole)`;
- validator passes `PASS=7 FAIL=0`; campaign status now consumes 41 route
  certificates and reports `PASS=37 FAIL=0`;
- still no retained closure: interacting `K(x)`, finite-volume/IR control, or
  production pole-derivative data remain open.
```

Latest scalar ladder eigen-derivative checkpoint text for PR #230:

```text
Adds a scalar ladder eigen-derivative gate:
- matrix Bethe-Salpeter pole condition `lambda_max=1` is only a crossing
  witness;
- holding the crossing fixed while varying `dK/dp^2` moves
  `d lambda_max/dp^2`, the LSZ residue proxy, and the FH/LSZ readout factor;
- validator passes `PASS=7 FAIL=0`; campaign status now consumes 42 route
  certificates and reports `PASS=38 FAIL=0`;
- still no retained closure: total-momentum kernel derivative or production
  pole-derivative data remain open.
```

Latest scalar ladder total-momentum derivative checkpoint text for PR #230:

```text
Adds a scalar ladder total-momentum derivative scout:
- computes finite-difference `d lambda_max/dp^2` in a Wilson-exchange scalar
  ladder by shifting the fermion bubble with total momentum;
- validator passes `PASS=9 FAIL=0`; campaign status now consumes 43 route
  certificates and reports `PASS=39 FAIL=0`;
- derivative is finite and negative on the 108-point scan, but its magnitude
  varies by about `3903.98x` across projector, zero-mode, IR, mass, and volume
  choices;
- still no retained closure: the limiting prescription, scalar pole
  derivative, canonical-Higgs normalization, or production pole data remain
  open.
```

Latest scalar ladder derivative limiting-order checkpoint text for PR #230:

```text
Adds a scalar ladder derivative limiting-order obstruction:
- tests the total-momentum derivative as `mu_IR^2` is lowered with the gauge
  zero mode included versus removed;
- validator passes `PASS=8 FAIL=0`; campaign status now consumes 44 route
  certificates and reports `PASS=40 FAIL=0`;
- included zero mode makes the derivative grow by `13.882x` to `24.0129x`,
  while zero-mode-removed stays within about `1.11x`;
- pole crossing occurs only in the zero-mode-included prescription;
- still no retained closure: the zero-mode/IR limiting theorem or production
  pole derivative remains load-bearing.
```

Latest Cl(3)/Z3 source-unit checkpoint text for PR #230:

```text
Adds a Cl(3)/Z3 source-unit normalization no-go:
- checks unit lattice spacing, unit Clifford generators, additive source
  coefficient, `g_bare=1`, and source functional derivative definitions;
- validator passes `PASS=8 FAIL=0`; campaign status now consumes 45 route
  certificates and reports `PASS=41 FAIL=0`;
- same-source invariant readouts are source-rescaling safe, but `dE/dh` and
  canonical curvature still change with `kappa_s`;
- still no retained closure: `kappa_s=1` is not derived from substrate unit
  conventions and still needs scalar pole/kinetic normalization or production
  LSZ data.
```

Latest joint FH/LSZ production-manifest checkpoint text for PR #230:

```text
Adds a joint Feynman-Hellmann / scalar-LSZ production manifest:
- exact three-volume launch commands now exist for `12x24`, `16x32`, and
  `24x48` with `--production-targets`, `--resume`, common-ensemble source
  shifts, and same-source scalar two-point modes;
- validator passes `PASS=9 FAIL=0`; campaign status now consumes 46 route
  certificates and reports `PASS=42 FAIL=0`;
- projected joint cost remains about `3630.28` single-worker hours before
  pole-fit and autocorrelation tuning;
- still no retained closure: this is launch planning, not production evidence,
  and `kappa_s`/pole-derivative control remains open.
```

Latest retained-closure route refresh checkpoint text for PR #230:

```text
Refreshes the retained-closure route certificate:
- now includes same-source invariant readout, scalar ladder derivative-limit,
  Cl(3)/Z3 source-unit, production-manifest, and joint resource blockers;
- validator passes `PASS=17 FAIL=0`; campaign status now consumes 47 route
  certificates and reports `PASS=43 FAIL=0`;
- still no retained/proposed-retained closure: remaining routes are strict
  production physical-response data or a scalar pole/common-dressing theorem.
```

Latest scalar ladder residue-envelope checkpoint text for PR #230:

```text
Adds a scalar ladder pole-tuned residue-envelope obstruction:
- tunes each finite Wilson-exchange ladder surface to its own pole, so the
  check no longer confuses pole location with LSZ residue;
- validator passes `PASS=9 FAIL=0`; retained-route gate reports
  `PASS=18 FAIL=0`; campaign status now consumes 48 route certificates and
  reports `PASS=44 FAIL=0`;
- the pole-tuned residue proxy still has a `7.08739x` envelope spread, with
  zero-mode, projector, and finite-volume choices changing the result;
- still no retained/proposed-retained closure: a real interacting
  denominator/zero-mode/IR/finite-volume theorem or production pole data is
  required.
```

Latest scalar-kernel Ward-identity checkpoint text for PR #230:

```text
Adds a scalar-kernel Ward-identity obstruction:
- verifies the old `yt_ward_identity` surface is audited-renaming, not current
  authority;
- shows exact Feshbach response preservation and gauge/Ward identities do not
  fix `K'(x_pole)` or common scalar/gauge dressing;
- validator passes `PASS=9 FAIL=0`; retained-route gate reports
  `PASS=19 FAIL=0`; campaign status now consumes 49 route certificates and
  reports `PASS=45 FAIL=0`;
- still no retained/proposed-retained closure: the interacting scalar
  denominator derivative or production pole data remains load-bearing.
```

Latest scalar zero-mode limit-order checkpoint text for PR #230:

```text
Adds a scalar zero-mode limit-order theorem:
- proves the retained gauge zero mode adds an exact positive diagonal ladder
  term `(4/3) w_i/(V mu_IR^2)`;
- validator passes `PASS=8 FAIL=0`; retained-route gate reports
  `PASS=20 FAIL=0`; campaign status now consumes 50 route certificates and
  reports `PASS=46 FAIL=0`;
- fixed-volume IR, volume-first, and box-scaled regulator paths give different
  scalar denominator behavior;
- still no retained/proposed-retained closure: the gauge-fixing, zero-mode,
  IR, and finite-volume prescription or production pole data remains
  load-bearing.
```

Latest zero-mode prescription import-audit checkpoint text for PR #230:

```text
Adds a zero-mode prescription import audit:
- checks the strongest current PT, continuum-identification, FH/LSZ manifest,
  and scalar-ladder certificate surfaces for a hidden prescription;
- validator passes `PASS=8 FAIL=0`; retained-route gate reports
  `PASS=21 FAIL=0`; campaign status now consumes 51 route certificates and
  reports `PASS=47 FAIL=0`;
- no current surface selects the PR #230 scalar zero-mode/IR/finite-volume
  denominator prescription;
- still no retained/proposed-retained closure: a new prescription theorem or
  production same-source pole data is required.
```

Latest flat-toron scalar-denominator checkpoint text for PR #230:

```text
Adds a flat-toron scalar-denominator obstruction:
- constant commuting Cartan links have zero plaquette action but distinct
  Polyakov phases;
- validator passes `PASS=7 FAIL=0`; retained-route gate reports
  `PASS=22 FAIL=0`; campaign status now consumes 52 route certificates and
  reports `PASS=48 FAIL=0`;
- scalar bubble and inverse-denominator proxies change across those flat
  sectors, so the compact action does not select the trivial zero mode;
- still no retained/proposed-retained closure: the toron/zero-mode sector
  prescription or production pole data remains load-bearing.
```

Latest flat-toron thermodynamic washout checkpoint text for PR #230:

```text
Adds flat-toron thermodynamic washout support:
- proves fixed physical holonomy corresponds to link angle `theta=phi/N`, so
  the local massive scalar bubble is a shifted periodic Riemann sum with the
  same thermodynamic limit as the trivial sector;
- validator passes `PASS=6 FAIL=0`; retained-route gate reports
  `PASS=23 FAIL=0`; campaign status now consumes 53 route certificates and
  reports `PASS=49 FAIL=0`;
- for `N >= 20`, relative bubble and inverse-denominator shifts are below
  `1e-4` on the scan;
- still no retained/proposed-retained closure: the interacting scalar pole,
  massless gauge-zero-mode/IR prescription, LSZ derivative, and production
  evidence remain open.
```

Latest color-singlet zero-mode cancellation checkpoint text for PR #230:

```text
Adds color-singlet gauge-zero-mode cancellation support:
- proves `(T_q^a + T_qbar^a)|S>=0` for the `q qbar` singlet;
- validator passes `PASS=7 FAIL=0`; retained-route gate reports
  `PASS=24 FAIL=0`; campaign status now consumes 54 route certificates and
  reports `PASS=50 FAIL=0`;
- the q=0 self and exchange pieces cancel as `C_F + C_F - 2 C_F = 0`, so an
  exchange-only finite ladder with the q=0 mode kept is not the color-neutral
  scalar denominator;
- still no retained/proposed-retained closure: finite-q IR behavior,
  interacting pole derivative, source/projector normalization, and production
  FH/LSZ evidence remain open.
```

Latest color-singlet finite-q IR regularity checkpoint text for PR #230:

```text
Adds color-singlet finite-q IR regularity support:
- after exact q=0 cancellation, proves the remaining massless kernel is
  locally integrable in four dimensions (`d^4q/q^2 ~ q dq`);
- validator passes `PASS=6 FAIL=0`; retained-route gate reports
  `PASS=25 FAIL=0`; campaign status now consumes 55 route certificates and
  reports `PASS=51 FAIL=0`;
- zero-mode-removed lattice kernel has a stable `mu_IR -> 0` limit and stable
  large-volume sequence on the scan;
- still no retained/proposed-retained closure: interacting scalar pole
  location, inverse-propagator derivative, finite-`N_c` residue, and
  production FH/LSZ evidence remain open.
```

Latest color-singlet zero-mode-removed ladder pole-search checkpoint text for
PR #230:

```text
Adds a color-singlet zero-mode-removed ladder pole-search block:
- after q=0 cancellation and finite-q IR regularity, scans the finite
  zero-mode-removed Wilson-exchange ladder at `mu_IR^2=0`;
- validator passes `PASS=9 FAIL=0`; retained-route gate reports
  `PASS=26 FAIL=0`; campaign status now consumes 56 route certificates and
  reports `PASS=52 FAIL=0`;
- four small-mass finite `lambda_max >= 1` witnesses exist, but they are
  volume, projector, taste-corner, and derivative sensitive;
- still no retained/proposed-retained closure: a continuum/taste/projector
  theorem for the interacting scalar pole and LSZ derivative, or production
  FH/LSZ pole data, remains required.
```

Latest taste-corner ladder pole-witness checkpoint text for PR #230:

```text
Adds a taste-corner ladder pole-witness obstruction:
- checks the four finite zero-mode-removed ladder crossings against
  corner-only, non-origin-corner-only, physical-origin-only, and no-corner
  policies;
- validator passes `PASS=8 FAIL=0`; retained-route gate reports
  `PASS=27 FAIL=0`; campaign status now consumes 57 route certificates and
  reports `PASS=53 FAIL=0`;
- non-origin taste corners supply `70.4828%` to `92.2308%` of the full crossing
  scale, and physical-origin-only filtering removes every crossing;
- still no retained/proposed-retained closure: a taste/scalar-carrier theorem
  plus continuum/projector/pole-derivative control, or production FH/LSZ pole
  data, remains required.
```

Latest taste-corner scalar-carrier import-audit checkpoint text for PR #230:

```text
Adds a taste-corner scalar-carrier import audit:
- checks CL3 taste generation, taste-scalar isotropy, full staggered PT, scalar
  ladder input audit, and the taste-corner obstruction for a hidden authority;
- validator passes `PASS=8 FAIL=0`; retained-route gate reports
  `PASS=28 FAIL=0`; campaign status now consumes 58 route certificates and
  reports `PASS=54 FAIL=0`;
- no retained/audit-clean authority admits non-origin BZ corners as the
  physical scalar carrier for PR #230;
- still no retained/proposed-retained closure: a taste/scalar-carrier theorem,
  continuum projector, pole derivative, or production FH/LSZ pole data remains
  required.
```

Latest taste-singlet ladder normalization-boundary checkpoint text for PR #230:

```text
Adds a taste-singlet ladder normalization boundary:
- checks the four finite zero-mode-removed ladder crossings under normalized
  singlet weighting over the 16 BZ corners;
- validator passes `PASS=6 FAIL=0`; retained-route gate reports
  `PASS=29 FAIL=0`; campaign status now consumes 59 route certificates and
  reports `PASS=55 FAIL=0`;
- normalized source weighting rescales every witness by `1/16`, giving
  normalized `lambda_max` range `0.0914604870307` to `0.442298920672`, so every
  finite crossing disappears;
- still no retained/proposed-retained closure: the scalar taste/projector
  normalization, continuum pole derivative, or production FH/LSZ pole data
  remains required.
```

Latest scalar taste-projector normalization-attempt checkpoint text for PR #230:

```text
Adds a scalar taste-projector normalization theorem attempt:
- derives the unit taste-singlet projector algebra over the 16 BZ corners,
  `O_singlet=(1/sqrt(16)) sum_t O_t`;
- validator passes `PASS=8 FAIL=0`; retained-route gate reports
  `PASS=30 FAIL=0`; campaign status now consumes 60 route certificates and
  reports `PASS=56 FAIL=0`;
- the unnormalized local corner sum has norm squared `16`, and the source term
  can absorb this factor as `s O_local = (sqrt(16) s) O_singlet`;
- still no retained/proposed-retained closure: the physical scalar carrier,
  source-to-Higgs normalization, and interacting pole derivative `K'(x_pole)`
  remain open, or must be measured in production same-source FH/LSZ data.
```

Latest unit-projector pole-threshold checkpoint text for PR #230:

```text
Adds a unit-projector pole-threshold obstruction:
- applies the unit taste-projector normalization to the finite ladder witnesses;
- validator passes `PASS=6 FAIL=0`; retained-route gate reports
  `PASS=31 FAIL=0`; campaign status now consumes 61 route certificates and
  reports `PASS=57 FAIL=0`;
- all unit-projector eigenvalues are below `lambda_max=1`; the best row is
  `0.442298920672` and needs an underived scalar-kernel multiplier
  `2.26091440260` to cross;
- still no retained/proposed-retained closure: a real interacting kernel
  theorem deriving the pole and `K'(x_pole)`, or production same-source FH/LSZ
  pole data, remains required.
```

Latest scalar-kernel enhancement import-audit checkpoint text for PR #230:

```text
Adds a scalar-kernel enhancement import audit:
- checks HS/RPA contact coupling, scalar ladder input formulae, same-1PI, and
  Ward/Feshbach response identities for the unit-projector pole multiplier;
- validator passes `PASS=7 FAIL=0`; retained-route gate reports
  `PASS=32 FAIL=0`; campaign status now consumes 62 route certificates and
  reports `PASS=58 FAIL=0`;
- no current retained/audit-clean authority derives the extra
  scalar-channel enhancement or `K'(x_pole)`;
- still no retained/proposed-retained closure: a new interacting kernel theorem
  or production same-source FH/LSZ pole data remains required.
```

Latest FH/LSZ production-manifest preflight checkpoint text for PR #230:

```text
Fixes the joint FH/LSZ production manifest preflight:
- adds `--production-targets` and `--resume` to every strict three-volume launch
  command so successful future runs emit production-targeted certificates
  rather than reduced-scope certificates;
- manifest validator now passes `PASS=9 FAIL=0`; retained-route gate remains
  `PASS=32 FAIL=0`; campaign status remains 62 certificates and
  `PASS=58 FAIL=0`;
- still no retained/proposed-retained closure: the manifest is launch planning,
  not production measurements, pole fits, or scalar LSZ evidence.
```

Latest FH/LSZ production-postprocess gate checkpoint text for PR #230:

```text
Adds an FH/LSZ production postprocess gate:
- validates the production manifest as a launch surface, not evidence;
- requires production-phase outputs, same-source `dE/ds`, same-source
  `Gamma_ss(q)`, isolated scalar-pole `dGamma_ss/dp^2`, FV/IR/zero-mode
  control, no forbidden normalization imports, and a retained-proposal
  certificate before physical `y_t` wording;
- validator passes `PASS=9 FAIL=0`; retained-route gate reports
  `PASS=33 FAIL=0`; campaign status now consumes 63 route certificates and
  reports `PASS=59 FAIL=0`;
- still no retained/proposed-retained closure: the expected production outputs
  and pole-fit certificate are absent.
```

Latest fitted-kernel residue selector no-go checkpoint text for PR #230:

```text
Adds a fitted scalar-kernel residue selector no-go:
- tests the shortcut of choosing `g_eff = 1/lambda_unit` to force a
  unit-projected finite ladder pole;
- validator passes `PASS=8 FAIL=0`; retained-route gate reports
  `PASS=34 FAIL=0`; campaign status now consumes 64 route certificates and
  reports `PASS=60 FAIL=0`;
- the fitted multiplier range is `2.26091440260` to `10.9336833038`, and the
  fitted residue proxy spread is `2.00925585041`;
- still no retained/proposed-retained closure: fitting `g_eff` imports the
  missing scalar-kernel normalization and does not derive `K'(x_pole)`.
```

Latest FH/LSZ production checkpoint-granularity checkpoint text for PR #230:

```text
Adds an FH/LSZ production checkpoint-granularity gate:
- audits the production manifest, resource projection, and current harness
  resume semantics;
- validator passes `PASS=9 FAIL=0`; retained-route gate reports
  `PASS=35 FAIL=0`; campaign status now consumes 65 route certificates and
  reports `PASS=61 FAIL=0`;
- current `--resume` loads completed per-volume artifacts only, and
  `write_volume_artifact` runs after `run_volume` returns;
- the smallest projected joint shard is `180.069` hours, so a 12-hour
  foreground launch would not produce safely checkpointed production evidence;
- still no retained/proposed-retained closure: production needs chunk-level
  checkpointing, an external scheduler that can finish at least L12_T24, or a
  new analytic scalar-denominator theorem.
```

Latest FH/LSZ chunked-production manifest checkpoint text for PR #230:

```text
Adds an FH/LSZ chunked production manifest:
- derives foreground-sized L12_T24 launch chunks from the resource projection
  and checkpoint-granularity gate;
- validator passes `PASS=8 FAIL=0`; retained-route gate reports
  `PASS=36 FAIL=0`; campaign status now consumes 66 route certificates and
  reports `PASS=62 FAIL=0`;
- L12 can be scheduled as 63 production-targeted chunks of 16 saved
  configurations, conservatively estimated at `11.3186` hours each;
- still no retained/proposed-retained closure: the chunk manifest is launch
  planning only, L16/L24 still need scheduler/checkpoint support, and no
  scalar pole postprocess certificate exists.
```

Latest FH/LSZ chunk-combiner gate checkpoint text for PR #230:

```text
Adds an FH/LSZ chunk combiner gate:
- adds `metadata.run_control` provenance to future production-harness
  certificates, including seed and command settings;
- reconstructs the 63 expected L12 chunk outputs and requires production
  phase, same-source `dE/ds`, same-source `C_ss(q)`, and run-control
  provenance before L12 combination;
- validator passes `PASS=7 FAIL=0`; retained-route gate reports
  `PASS=37 FAIL=0`; campaign status now consumes 67 route certificates and
  reports `PASS=63 FAIL=0`;
- still no retained/proposed-retained closure: zero chunks are present, L12
  alone is not closure, and L16/L24 plus isolated-pole/FV/IR postprocess remain
  open.
```

Latest FH/LSZ chunk command-isolation checkpoint text for PR #230:

```text
Tightens the FH/LSZ L12 chunk launch preflight:
- each chunk command now uses a chunk-local `--production-output-dir` and
  `--resume`, preventing completed per-volume artifacts from colliding across
  independent chunks;
- the combiner gate now verifies 63 unique chunk artifact directories and
  requires future chunk certificates to record the matching run-control path;
- chunked-manifest validator passes `PASS=10 FAIL=0`; combiner gate passes
  `PASS=8 FAIL=0`; retained-route gate remains `PASS=37 FAIL=0`; campaign
  status remains `PASS=63 FAIL=0`;
- still no retained/proposed-retained closure: zero chunks are present, and
  production pole/FV/IR plus L16/L24 remain open.
```

Latest FH/LSZ negative scalar-source CLI preflight checkpoint text for PR #230:

```text
Fixes FH/LSZ production command syntax:
- first chunk launch failed immediately because `--scalar-source-shifts
  -0.01,0.0,0.01` is parsed as a missing argument by `argparse`;
- production and chunk manifest emitters now use
  `--scalar-source-shifts=-0.01,0.0,0.01`;
- production manifest remains `PASS=9 FAIL=0`, chunked manifest remains
  `PASS=10 FAIL=0`, postprocess gate remains `PASS=9 FAIL=0`, combiner gate
  remains `PASS=8 FAIL=0`;
- still no retained/proposed-retained closure: this only makes the next
  non-evidence chunk launch syntactically executable.
```

Latest FH/LSZ pole-fit kinematics checkpoint text for PR #230:

```text
Adds an FH/LSZ scalar-pole kinematics gate:
- parses the production and chunk manifest scalar-LSZ modes;
- verifies the current mode set has only one nonzero `p_hat^2` shell;
- validator passes `PASS=7 FAIL=0`; retained-route gate reports
  `PASS=38 FAIL=0`; campaign status now consumes 68 certificates and reports
  `PASS=64 FAIL=0`;
- still no retained/proposed-retained closure: four-mode chunks are finite
  positive-momentum secant support, not an isolated scalar-pole derivative.
```

Latest FH/LSZ pole-fit mode/noise budget checkpoint text for PR #230:

```text
Adds an FH/LSZ pole-fit mode/noise budget:
- eight modes with sixteen noises are pole-fit kinematics ready but estimate
  to `21.45` hours for an L12 chunk;
- eight modes with eight noises keep the current `11.3186` hour foreground
  estimate and give enough momentum shells;
- validator passes `PASS=8 FAIL=0`; retained-route gate reports
  `PASS=39 FAIL=0`; campaign status consumes 69 certificates and reports
  `PASS=65 FAIL=0`;
- still no retained/proposed-retained closure: this is launch planning only
  until a variance gate, production data, FV/IR control, and retained-proposal
  audit exist.
```

Latest FH/LSZ eight-mode noise variance checkpoint text for PR #230:

```text
Adds an FH/LSZ eight-mode noise variance gate:
- verifies the eight-mode/eight-noise L12 option is pole-fit-kinematics ready
  and fits the current foreground estimate;
- blocks using it as evidence because x8 raises scalar-LSZ noise-only stderr
  by sqrt(2) versus x16 and no same-source production x8/x16 calibration or
  theorem exists;
- disqualifies the reduced smoke as wrong phase, volume, modes, noises, and
  statistics; chunk001 is absent until complete and is four-mode/x16 rather
  than the needed x8 calibration;
- validator passes `PASS=10 FAIL=0`; retained-route gate reports
  `PASS=40 FAIL=0`; campaign status consumes 70 certificates and reports
  `PASS=66 FAIL=0`;
- still no retained/proposed-retained closure: this is launch control only,
  not production pole data or a scalar LSZ/canonical-Higgs theorem.
```

Latest FH/LSZ noise-subsample diagnostics checkpoint text for PR #230:

```text
Adds scalar-LSZ noise-subsample diagnostics to the production harness:
- each scalar two-point mode row and top-level LSZ analysis now emits
  `noise_subsample_stability` fields for split-noise stability checks;
- scalar-only and joint FH/LSZ smokes were rerun and validate the diagnostic
  shape, but remain reduced-scope two-mode/two-noise instrumentation outputs;
- diagnostics validator passes `PASS=9 FAIL=0`; retained-route gate reports
  `PASS=41 FAIL=0`; campaign status consumes 71 certificates and reports
  `PASS=67 FAIL=0`;
- still no retained/proposed-retained closure: diagnostics are future
  calibration plumbing, not production pole data or scalar LSZ normalization.
```

Latest FH/LSZ variance calibration manifest checkpoint text for PR #230:

```text
Adds a paired x8/x16 FH/LSZ variance calibration manifest:
- emits exact L12 commands with matched mass, source shifts, eight scalar-LSZ
  modes, seed, therm/measurement schedule, and separate artifact dirs;
- x8 and x16 differ only by scalar-LSZ noise count and output paths;
- manifest validator passes `PASS=9 FAIL=0`; retained-route gate reports
  `PASS=42 FAIL=0`; campaign status consumes 72 certificates and reports
  `PASS=68 FAIL=0`;
- still no retained/proposed-retained closure: this is launch planning only;
  no completed calibration, pole derivative, FV/IR control, or retained gate
  exists.
```

Latest gauge-VEV source-overlap checkpoint text for PR #230:

```text
Adds a gauge-VEV source-overlap no-go:
- constructs countermodels with identical canonical `v`, gauge coupling, and
  `m_W`, but different `h = kappa_s s` source overlap;
- shows setting `kappa_s=1` changes the inferred physical `dE/dh`;
- runner passes `PASS=8 FAIL=0`; retained-route gate reports
  `PASS=43 FAIL=0`; campaign status consumes 73 certificates and reports
  `PASS=69 FAIL=0`;
- still no retained/proposed-retained closure: electroweak `v` and gauge
  masses do not replace scalar LSZ residue or same-source production pole data.
```

Latest scalar renormalization-condition source-overlap checkpoint text for PR #230:

```text
Adds a scalar renormalization-condition source-overlap no-go:
- constructs countermodels with identical canonical Higgs `Z_h=1`, pole mass,
  `v`, and canonical `y_h`, but different source operator overlap
  `<0|O_s|h>`;
- shows `dE/ds` changes unless the same-source pole residue `Res C_ss` is
  measured or derived; the invariant readout `dE/ds / sqrt(Res C_ss)` stays
  fixed only when that residue is included;
- runner passes `PASS=11 FAIL=0`; retained-route gate reports
  `PASS=44 FAIL=0`; campaign status consumes 74 certificates and reports
  `PASS=70 FAIL=0`;
- still no retained/proposed-retained closure: canonical kinetic
  normalization does not replace scalar LSZ residue or same-source production
  pole data.
```

Latest scalar source contact-term scheme checkpoint text for PR #230:

```text
Adds a scalar source contact-term scheme boundary:
- uses C(x)=Z/(x+m_H^2)+a+b*x and chooses local source contact terms a,b so
  that pole residues Z={0.25,1,4} share the same low-q C(0)=1 and C'(0)=-0.25
  convention;
- shows contact-normalized readouts vary while the same-source pole-residue
  readout dE/ds/sqrt(Res C_ss) stays fixed;
- runner passes `PASS=10 FAIL=0`; retained-route gate reports
  `PASS=45 FAIL=0`; campaign status consumes 75 certificates and reports
  `PASS=71 FAIL=0`;
- still no retained/proposed-retained closure: source contact-term schemes do
  not replace scalar LSZ residue or same-source production pole data.
```
