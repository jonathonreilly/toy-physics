# PR230 Top-Yukawa Retained-Closure Route Certificate

**Date:** 2026-05-01  
**Status:** open / closure not yet reached  
**Runner:** `scripts/frontier_yt_retained_closure_route_certificate.py`  
**Certificate:** `outputs/yt_retained_closure_route_certificate_2026-05-01.json`

## Purpose

This note answers the practical closure question for PR #230: what is the
shortest honest path from the current branch state to retained top-Yukawa
closure?

The answer is not another small pilot run and not another rewording of the old
Ward theorem.  The remaining closure routes are now sharply separated.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=82 FAIL=0
```

The runner verifies:

| Check | Result |
|---|---|
| required route certificates present | pass |
| hidden retained `y_t` proof exists | no |
| strict production direct-correlator certificate exists | no |
| Ward physical-readout repair is closed | no |
| scalar pole residue is derived on current analytic surface | no |
| key-blocker closure attempt found retained authority | no |
| LSZ source-normalization cancellation is closure | no |
| Feshbach response preservation proves common dressing | no |
| same-source FH/LSZ invariant readout is production evidence | no |
| scalar ladder derivative limiting order is derived | no |
| scalar ladder pole-tuned residue envelope is an LSZ bound | no |
| Ward/gauge identities fix `K'(x_pole)` | no |
| zero-mode / IR / finite-volume limiting order is selected | no |
| hidden repo authority supplies zero-mode prescription | no |
| compact action selects trivial flat toron sector | no |
| flat-toron thermodynamic washout closes scalar LSZ | no |
| color-singlet gauge zero-mode cancellation closes scalar LSZ | no |
| color-singlet finite-`q` IR regularity closes scalar LSZ | no |
| color-singlet zero-mode-removed finite ladder pole search closes scalar LSZ | no |
| taste-corner finite ladder pole witness closes scalar LSZ | no |
| hidden taste-corner scalar-carrier authority exists | no |
| normalized taste-singlet source keeps finite crossings | no |
| unit taste-singlet algebra fixes the physical scalar carrier and pole derivative | no |
| unit-projector finite ladder crosses at retained kernel strength | no |
| hidden scalar-kernel enhancement authority exists | no |
| fitted scalar-kernel multiplier derives a retained LSZ residue | no |
| Cl(3)/Z3 source unit fixes `kappa_s` | no |
| canonical Higgs kinetic renormalization fixes the source overlap | no |
| source contact-term curvature scheme fixes the pole residue | no |
| short-distance/OPE operator normalization fixes the IR source-pole residue | no |
| finite effective-mass plateau window fixes the source-pole residue | no |
| single finite source-shift radius certifies the zero-source FH derivative | no |
| BRST/ST/Nielsen identities fix the source pole as canonical Higgs | no |
| finite Cl(3)/Z3 automorphism/orbit data fix continuous LSZ source overlap | no |
| same-source pole-data sufficiency gate is passed | no |
| joint FH/LSZ production manifest is evidence | no |
| joint FH/LSZ production postprocess gate is ready | no |
| current FH/LSZ resume support makes 12h foreground production launch safe | no |
| chunked L12 production manifest is complete production evidence | no |
| chunk-combiner gate has complete ready L12 chunks | no |
| four-mode scalar-LSZ kinematics determine the isolated pole derivative | no |
| pole-fit postprocessor has combined production input | no |
| pole-fit mode/noise budget is production evidence | no |
| same-source sector-overlap identity is derived | no |
| source pole is certified as canonical Higgs radial mode | no |
| joint FH/LSZ route is foreground-sized | no |
| interacting kinetic route has ensemble/matching evidence | no |
| Planck beta-stationarity route is derived | no |
| prior non-MC queue is exhausted | yes |

## Shortest Honest Closure Routes

### Route 1: Direct Or Joint Physical Measurement

Run the strict production correlator route or the joint Feynman-Hellmann /
scalar-LSZ production route on a physically suitable scale or heavy-quark
treatment, produce production certificates, derive the scalar pole derivative
and any matching bridge, and pass a retained-proposal gate such as:

```text
scripts/frontier_yt_direct_lattice_correlator.py
```

This route bypasses the Ward/H-unit definition trap.  The joint manifest now
gives exact launch commands, and the postprocess gate now states the exact
acceptance boundary.  It is not evidence until the production run, pole/LSZ
analysis, finite-volume/IR control, and retained-proposal audit gate complete.

Current blocker: existing certificates are reduced-scope, pilot, or planning
manifests.  The new postprocess gate confirms the three production outputs are
absent and no isolated-pole `dGamma_ss/dp^2` certificate exists.  The joint
FH/LSZ route projects to about `3630.28` single-worker hours before pole-fit
and autocorrelation tuning.  The checkpoint-granularity gate also shows the
current `--resume` support is whole-volume only, while the smallest projected
joint shard is `180.069` single-worker hours.  A 12-hour foreground launch
would not create a safely checkpointed production certificate.
The chunked manifest provides an L12 scheduling route with 63 production-targeted
chunks of 16 saved configurations, estimated at `11.3186` hours each, but it
is launch planning only and leaves L16/L24 and pole postprocessing open.
The chunk-combiner gate now requires all 63 L12 chunks to be production phase
with seed/command run-control provenance, same-source `dE/ds`, and same-source
`C_ss(q)` before L12 combination.  It currently finds zero present chunks, and
L12-only remains non-retained even when complete.  Chunk commands now use
chunk-local production artifact directories plus per-chunk resume, so
per-volume artifacts cannot collide across independent chunks.
The scalar-pole kinematics gate adds that the current four scalar modes contain
only one nonzero `p_hat^2` shell.  Completed four-mode chunks are therefore
finite-difference support, not the isolated-pole `dGamma_ss/dp^2` needed for
retained closure.
The pole-fit postprocessor scaffold now gives a concrete future fit path after
chunk combination, but the combined production input is absent/nonready, so it
is not evidence.
The mode/noise budget gives a constructive next launch class: eight scalar
modes with eight noises keep the current foreground L12 chunk estimate, but
that is planning only and requires a variance gate before use.
The eight-mode noise variance gate now rejects the current evidence surface:
the reduced smoke has the wrong phase, volume, modes, noises, and statistics,
and the current chunk surface is absent or four-mode/x16 rather than an
eight-mode/x8 calibration.
The harness now emits noise-subsample stability diagnostics needed by a future
paired x8/x16 calibration, but the current diagnostic smokes remain
reduced-scope instrumentation support only.
The paired x8/x16 variance calibration manifest now fixes matched launch
controls, but no completed calibration output exists.
The gauge-VEV source-overlap no-go blocks another analytic shortcut: canonical
`v` and gauge-boson masses fix the metric of an already identified Higgs field,
not the overlap between the substrate source `s` and canonical `h`.
The scalar renormalization-condition source-overlap no-go blocks the remaining
kinetic-normalization shortcut: `Z_h=1` fixes the canonical Higgs field
residue, not the source operator matrix element `<0|O_s|h>`.
The source contact-term scheme boundary blocks using contact-renormalized
low-momentum curvature as the LSZ bridge: `C_ss(0)` and `C_ss'(0)` can be fixed
by source contact terms while the isolated pole residue remains different.
The finite source-shift derivative no-go blocks treating the current
single-radius source response as the zero-source FH derivative: `E(-delta)`,
`E(0)`, `E(+delta)`, and the finite slope can remain fixed while `dE/ds|_0`
changes through odd nonlinear response.  Future source-response evidence needs
multiple source radii, a finite-source-linearity gate, or a retained analytic
response-bound theorem.

### Route 2: Analytic Scalar Residue And Common Dressing

Derive from retained dynamics:

1. the scalar source two-point pole residue;
2. the scalar carrier map;
3. the scalar LSZ external-leg factor;
4. the common scalar/gauge dressing ratio.

Then re-run the Ward physical-readout repair audit.  This is the direct
analytic repair of the audit's physical-readout objection.

Current blocker: the current algebraic surface underdetermines the pole
residue and dressing.  Source-normalization covariance, exact Feshbach response
preservation, same-source invariant readout, and Cl(3)/Z3 source-unit checks
are now controlled, but none derives the microscopic interacting scalar
denominator, zero-mode/IR limiting order, pole residue, or scalar/gauge
equality.  The pole-tuned finite-ladder residue envelope remains
zero-mode/projector/volume dependent, so it is not a scalar-LSZ bound either.
The current Ward/gauge/Feshbach surfaces likewise do not determine
`K'(x_pole)`.  The exact zero-mode theorem now shows why this is
not a numerical nuisance: retaining the gauge zero mode adds a positive
`1/(V mu_IR^2)` diagonal term, so different IR/volume paths give different
scalar denominators until a prescription is derived.  The import audit checks
the strongest current PT, continuum-identification, manifest, and scalar
ladder surfaces and finds no hidden authority that selects that prescription.
The flat-toron check further shows constant commuting gauge zero modes have
zero plaquette action but change scalar-denominator proxies, so selecting the
trivial sector is itself a finite-volume theorem/prescription.  The new
thermodynamic washout support removes that ambiguity for the local massive
bubble at fixed physical holonomy, but it does not derive the interacting pole
denominator, finite-`q` massless IR prescription, or LSZ derivative.  The
color-singlet zero-mode theorem removes the exact `q=0` exchange-only
divergence by total-color-charge cancellation, but the finite-`q` kernel and
pole derivative remain open.  The finite-`q` IR regularity theorem then shows
the zero-mode-removed massless kernel is locally integrable in four
dimensions, leaving the pole derivative and production evidence as the active
blockers.  The zero-mode-removed ladder pole search finds finite small-mass
`lambda_max >= 1` witnesses, but they are volume, projector, taste-corner, and
derivative sensitive, so they are not the retained interacting pole/LSZ
theorem.  Filtering non-origin Brillouin-zone taste corners removes every
finite crossing, so a taste/scalar-carrier theorem is load-bearing.  The
taste-carrier import audit finds no current retained authority that supplies
that theorem.  Normalized taste-singlet source weighting over the 16 corners
rescales the same finite witnesses by `1/16` and removes every finite crossing,
so unnormalized taste multiplicity is load-bearing too.  A unit taste singlet
can be constructed algebraically, but the source functional still permits
source-coordinate rescaling and the current surface does not identify the
physical scalar carrier or derive `K'(x_pole)`.
With that unit projector, the finite ladder has no crossing at the retained
scout kernel strength; the best row would require an underived scalar-channel
kernel multiplier of `2.26091440260`.
The scalar-kernel enhancement import audit checks HS/RPA, ladder formulae,
same-1PI, and Ward/Feshbach surfaces and finds no retained authority for that
factor.
The fitted-kernel residue selector no-go closes the next shortcut: forcing a
finite pole with `g_eff = 1/lambda_unit` imports the missing scalar-channel
normalization and leaves the residue proxy
`lambda_raw / |d lambda_raw / dp^2|` finite-row dependent.

### Route 3: New Selector Theorem

Derive `beta_lambda(M_Pl)=0`, or another selector, from the `Cl(3)/Z^3`
substrate.

Current blocker: all current stationarity shortcuts are no-go or conditional.
Adding the selector as a premise may be useful, but it is not retained closure
under the current claim posture.

## Actual Current Status

```text
open / retained closure not yet reached
```

No route currently satisfies retained-proposal conditions.  The next useful
action is either launching/scheduling the strict production physical-response
manifest and then passing the postprocess pole/LSZ gate, or deriving a real
scalar two-point residue/common-dressing theorem.  A finite-shell
analytic-continuation gate is also required before any Euclidean
`Gamma_ss(p^2)` pole fit can be load-bearing: finite shell rows can share the
same sampled values and pole while changing `dGamma_ss/dp^2`.  The executable
model-class gate now enforces that boundary and remains open.  Replacement
chunk001 has completed under `numba_gauge_seed_v1` and is the first ready
chunk in the combiner.  Historical chunk002 remains seed-invalid until its
replacement completes.  The current set is still only `1/63` ready L12 chunks,
with no combined L12, L16/L24, pole-derivative, model-class, or FV/IR
certificate.  Positive
Stieltjes/spectral form alone also does not close the
model-class gate because positive continuum freedom can preserve finite shell
values and the pole while changing the residue.  The pole-saturation threshold
gate now converts that requirement into a concrete residue-interval check, and
the current interval is not tight.  The threshold-authority import audit finds
no hidden current artifact that supplies the missing premise.  The finite-volume
pole-saturation obstruction also blocks using finite-L discreteness as a
uniform continuum-gap theorem.  The combiner gate now also rejects chunks
without auditable numba gauge seeding or with duplicate gauge signatures across
distinct metadata seeds.  The uniform-gap self-certification no-go also blocks
inferring that theorem from finite shell rows: a gapped positive model's shell
values can be reproduced by a near-pole positive continuum model with zero pole
residue lower bound.  The scalar-denominator theorem closure attempt then
checks the full dependency stack and remains blocked on zero-mode prescription,
scalar carrier/projector, `K'(pole)`, model class, threshold, and
seed-controlled production.  The soft-continuum threshold no-go also blocks
promoting color-singlet q=0 cancellation plus finite-q IR regularity into that
threshold premise: IR integrability does not exclude positive continuum
spectral weight arbitrarily close to the pole.  The reflection-positivity
LSZ shortcut no-go blocks the broader OS positivity repair as well: positive
reflection-positive spectral families can preserve finite same-source shell
rows while moving the pole residue.  The scalar carrier/projector
closure attempt confirms that the taste/projector side is still open:
color-singlet support and unit taste-singlet algebra do not admit the physical
carrier, preserve unit-projector finite crossings, or derive `K'(pole)`.  The
`K'(pole)` closure attempt then confirms the derivative itself is named but
unclosed: finite derivative scouts remain blocked by limiting order, residue
envelope dependence, Ward/Feshbach non-identification, carrier/projector
choice, fitted-kernel imports, and missing threshold control.  If
the FH/LSZ same-source invariant formula is used, it still needs the
canonical-Higgs pole identity gate: source-coordinate scaling cancels, but the
measured scalar source pole is not certified as the canonical Higgs radial mode
used by `v`.  Production pole derivative data and the source-to-Higgs identity
remain open.  A same-source gauge-normalized response ratio could also cancel
`kappa_s` using a W/Z mass slope, but the W/Z response observable and shared
Higgs identity certificate are absent.  The gauge-mass observable-gap gate
confirms that the present production harness is QCD top-only and does not
produce `dM_W/ds` or `dM_Z/ds`.  The same-source sector-overlap identity
obstruction also blocks treating a common source coordinate as proof that
`k_top = k_gauge`; without that theorem or a direct measurement, the
gauge-normalized ratio reads `y_t * k_top/k_gauge`.  If
the source-pole FH/LSZ readout is used instead, the pole itself must be proved
to be the canonical Higgs radial mode; a mixed source pole would read out
`y_t * cos(theta)` rather than `y_t`.  If
the eight-mode/x8
foreground option is used, it first needs same-source x8/x16 variance
calibration with noise-subsample diagnostics.  More small pilot MC runs do not
close PR #230.

The no-orthogonal-top-coupling import audit now closes another shortcut.  The
existing Class #3 SUSY/2HDM authority excludes a retained fundamental second
scalar, retained 2HDM species split, and second D17 `Q_L` scalar, but it does
not derive LSZ source-pole purity.  It cannot be used to set an orthogonal top
coupling to zero or to identify the measured source pole with the canonical
Higgs radial mode.  The retained-route certificate is refreshed at
`PASS=69 FAIL=0` and still authorizes no retained/proposed-retained wording.

The D17 source-pole identity closure attempt then checks the strongest
carrier-uniqueness upgrade directly.  D17 fixes a single scalar carrier/irrep
statement, but it does not fix source operator overlap, source two-point pole
residue, inverse-propagator derivative, or the canonical kinetic metric used
by `v`.  The retained-route certificate is refreshed at `PASS=70 FAIL=0` and
still authorizes no retained/proposed-retained wording.

The source-overlap spectral sum-rule no-go closes the finite-moment shortcut.
Positive pole-plus-continuum spectral measures can keep the first four
same-source moments fixed while changing pole residue by a factor of ten.
The retained-route certificate is refreshed at `PASS=71 FAIL=0` and still
authorizes no retained/proposed-retained wording.

The latest Higgs-pole identity blocker certificate consolidates the remaining
source-pole identity failure after D17, source-pole mixing, no-orthogonal
top-coupling, source-overlap, sector-overlap, denominator, and `K'(pole)`
checks.  The same source-pole top readout can stay fixed while the physical
canonical-Higgs Yukawa varies, so the route still needs a real Higgs-pole
identity theorem or production pole data with an independent identity
certificate.  The retained-route certificate is refreshed at `PASS=72 FAIL=0`
and still authorizes no retained/proposed-retained wording.

The confinement-gap threshold import audit closes another scalar-denominator
shortcut.  Generic substrate confinement or mass-gap statements are qualitative
sector constraints, not a same-source scalar continuum-threshold theorem and
not a pole-residue bound.  The retained-route certificate is refreshed at
`PASS=73 FAIL=0` and still authorizes no retained/proposed-retained wording.

The same-source W/Z gauge-mass response manifest records a concrete physical
response observable that could cancel `kappa_s`, but it is not evidence.  The
current harness has top `dE/ds` support only; no W/Z response path or identity
certificate exists.  The retained-route certificate is refreshed at
`PASS=74 FAIL=0` and still authorizes no retained/proposed-retained wording.

The reflection-positivity LSZ shortcut no-go closes another analytic shortcut.
OS positivity gives a positive spectral representation, but the positive
pole-plus-continuum family can be realized by reflection-positive Euclidean
time correlators while finite same-source shell rows stay fixed and the pole
residue changes.  The retained-route certificate is refreshed at
`PASS=75 FAIL=0` and still authorizes no retained/proposed-retained wording.

Chunks005-006 are now included in the seed-controlled FH/LSZ ready set.  The
combiner reports ready indices `[1, 2, 3, 4, 5, 6]`, or `6/63` L12 chunks.  This improves
production support only: response stability still fails and the route still
lacks combined L12, L16/L24 scaling, scalar-pole derivative/model-class,
FV/IR, and canonical-Higgs identity gates.

The effective-potential Hessian source-overlap no-go closes the radial-
curvature shortcut.  Canonical VEV, W/Z masses, scalar Hessian eigenvalues,
and canonical top Yukawa can remain fixed while the PR #230 source operator
direction rotates in scalar field space.  The retained-route certificate is
refreshed at `PASS=76 FAIL=0` and still authorizes no retained/proposed-retained
wording.
