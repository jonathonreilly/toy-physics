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
# SUMMARY: PASS=32 FAIL=0
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
| joint FH/LSZ production manifest is evidence | no |
| joint FH/LSZ production postprocess gate is ready | no |
| current FH/LSZ resume support makes 12h foreground production launch safe | no |
| chunked L12 production manifest is complete production evidence | no |
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
scalar two-point residue/common-dressing theorem.  More small pilot MC runs do
not close PR #230.
