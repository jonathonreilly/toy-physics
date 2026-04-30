# Direct Lattice-Correlator Top-Yukawa Measurement Gate

**Date:** 2026-04-30
**Status:** proposed_retained measurement route, pending production-scale staggered-correlator data and audit
**Primary runner:** `scripts/frontier_yt_direct_lattice_correlator.py`
**Production harness:** `scripts/yt_direct_lattice_correlator_production.py`

## Theorem Statement

Candidate theorem under test:

On the `Cl(3)/Z^3` Wilson-staggered substrate with `g_bare = 1`, the top-sector
mass is measured from the long-distance decay of a staggered-fermion top
correlator,

```text
C_t(tau) = sum_x < psi_t(x,tau) psi_t^dagger(0) >,
```

and the electroweak Yukawa readout is then computed by the Standard Model mass
relation

```text
y_t(v) = sqrt(2) m_t(v) / v.
```

The value of `v` is an explicit substrate input from the existing electroweak
VEV chain.  This note does not claim that the `v = 246 GeV` chain is repaired
or independently audit-cleaned here.

A production certificate is expected to give, after scale setting and the
standard SM/QCD running bridge,

```text
y_t(v) ~= 0.917 +/- total_lattice_matching_uncertainty
m_t(pole) ~= 172.56 GeV +/- total_lattice_matching_uncertainty
```

with the strict comparator set to the current PDG 2025 listing average
`m_t = 172.56 +/- 0.31 GeV`.  The older `172.69 GeV` ATLAS-combination value is
listed by PDG as superseded by the 2024 ATLAS+CMS combination, so it is kept
only as a historical cross-check target, not as the strict comparator.

This branch contains reduced-scope and pilot MC/correlator certificates for
infrastructure evidence only.  They are not production numerical results.  The
strict runner reads the default reduced certificate and rejects it until the
production volumes, statistics, independent `g_s` ratio evidence, and physical
comparator checks are supplied.

## Five-Step Methodology

### 1. Staggered-Fermion Action Setup

Use the graph-first `SU(3)` gauge sector from
[GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) and
the canonical `g_bare = 1` substrate declaration from
[MINIMAL_AXIOMS_2026-04-11.md](MINIMAL_AXIOMS_2026-04-11.md).  The production
calculation must use the Wilson gauge action plus staggered fermions, with:

- spatial volumes including `12^3`, `16^3`, and `24^3`;
- enough scale-control information to separate finite-volume, finite-spacing,
  and Sommer-scale uncertainties;
- periodic gauge boundary conditions and antiperiodic temporal fermion
  boundary conditions;
- HMC/RHMC or Cabibbo-Marinari heat-bath plus overrelaxation updates for the
  Wilson-staggered ensemble;
- a scan or tuning record for the heavy top-sector bare mass parameter.

The heavy mass parameter is a lattice action parameter to be tuned and
measured through observables.  It is not a Yukawa definition.

### 2. Top-Correlator Measurement

Measure a top-sector staggered correlator over multiple Euclidean time
separations.  The production certificate must state whether the colored
top-sector two-point function is made gauge-defined by a fixed gauge, by an
explicit gauge transporter, or by another documented framework-native dressing.
The observable route is a correlator mass extraction, not a scalar-composite
matrix-element identification.

The expected large-time form is

```text
C_t(tau) = A_0 exp(-m_t tau) + A_1 exp(-m'_t tau) + ...
```

with the staggered parity/oscillating contribution modelled or bounded where
it is visible.

### 3. Mass Extraction

Extract the mass from the effective-mass plateau,

```text
m_eff(tau) = log(C_t(tau) / C_t(tau + 1)),
```

and from correlated single-state and excited-state fits on the plateau window.
The certificate must report:

- the selected plateau window and `chi^2/dof`;
- bootstrap or jackknife statistical uncertainty;
- finite-volume and finite-spacing residuals;
- heavy-mass tuning uncertainty;
- an excited-state contamination bound.

### 4. Yukawa Computation And Scale Setting

After the mass is measured, compute

```text
y_t(v) = sqrt(2) m_t(v) / v.
```

Here `m_t(v)` is the measured mass after the stated matching/running bridge to
the electroweak scale, and `v` is the explicit VEV substrate input.  The strict
runner checks this arithmetic from the certificate fields and rejects any
certificate that supplies the Yukawa value from a prior Ward or matrix-element
route.

Scale setting must use the Sommer scale or an equivalent explicit physical
length anchor.  That physical anchor remains an external matching input and is
not closed by this theorem.

### 5. Running To The Physical Scale

Run the measured lattice mass and computed Yukawa through the standard SM/QCD
bridge, including continuum scheme conversion and threshold matching.  The
bridge may be implemented at four or five loops, but the certificate must
state the loop order, matching scheme, thresholds, and truncation uncertainty.

The strict certificate is expected to compare:

```text
m_t(pole)            against PDG 2025: 172.56 +/- 0.31 GeV
y_t(v)               against the chosen SM running comparator near 0.917
y_t/g_s at the lattice scale against 1/sqrt(6)
```

The last comparison is a measured ratio check using independently measured
`y_t` and `g_s`.  It is not an identity used to obtain `y_t`.

## Explicit Avoidance Of The Prior Trap

The audit ledger currently records
`yt_ward_identity_derivation_theorem` as `audited_renaming`.  Its load-bearing
failure mode is that the top-Yukawa readout is introduced by declaring the
unit-normalized `H_unit`-to-top matrix element to be the physical Yukawa
quantity, after which the runner checks algebraic consistency of that
identification.

This route avoids that failure by construction:

- it does not use the `H_unit`-to-top matrix element as input;
- it does not use the prior Ward-identity theorem as a dependency;
- it does not use the `alpha_LM` or plaquette/tadpole coupling chain;
- it measures `m_t` from the staggered-fermion correlator;
- it computes `y_t` only after the mass measurement, via `sqrt(2) m_t/v`;
- it treats `v` as a declared substrate input whose own audit status remains
  separate.

The strict runner enforces this boundary by rejecting production certificates
that contain prior Ward, matrix-element, `H_unit`, or coupling-definition
authority fields.

## Numerical Result And Uncertainty Budget

This PR update adds a resumable Wilson-staggered production harness and records
one reduced-scope feasibility run.  The reduced run validates the implemented
path but is not theorem evidence:

| Field | Reduced-scope value |
|---|---:|
| Certificate phase | `reduced_scope` |
| Volumes | `2^3 x 4`, `3^3 x 6` |
| Thermalization | 2 sweeps |
| Saved configurations | 3 per volume |
| Separation | 1 sweep |
| Bare-mass scan | `0.45`, `0.75`, `1.05` |
| `m_t` proxy | `2.662884 GeV` |
| `y_t(v)` proxy | `0.01529483` |
| Total `m_t` proxy uncertainty | `1.194967 GeV` |
| Total `y_t` proxy uncertainty | `0.00686354` |
| Ratio evidence | `g_s_source = not_measured_reduced_scope` |

The output files are
`outputs/yt_direct_lattice_correlator_certificate_2026-04-30.json` and the
archived reduced-run copy under `outputs/yt_direct_lattice_correlator/`.  The
reported mass and Yukawa are proxy values from the reduced infrastructure run;
they are far from the physical comparators and deliberately do not pass strict
mode.

This PR also records a bounded `12^3 x 24` pilot lane.  The pilot is a
manageable unit of execution for PR #230 and is explicitly non-retained:

| Field | Pilot value |
|---|---:|
| Certificate phase | `pilot` |
| Volume | `12^3 x 24` |
| Thermalization | 10 sweeps |
| Saved configurations | 3 |
| Separation | 2 sweeps |
| Overrelaxation | 2 sweeps per heat-bath |
| Bare-mass scan | `0.45`, `0.75`, `1.05` |
| `m_t` proxy | `4.121892 GeV` |
| `y_t(v)` proxy | `0.02367494` |
| Total `m_t` proxy uncertainty | `1.201741 GeV` |
| Total `y_t` proxy uncertainty | `0.00690245` |
| Ratio evidence | `g_s_source = not_measured_pilot` |

The pilot certificate is
`outputs/yt_direct_lattice_correlator_pilot_certificate_2026-04-30.json`, with
the per-volume artifact at
`outputs/yt_direct_lattice_correlator_pilot/L12xT24/ensemble_measurement.json`.
When pointed at the pilot certificate, strict mode rejects it as expected: it is
`phase = pilot`, has only the `12^3 x 24` volume, has pilot statistics, has no
independent `g_s`, and does not match physical comparators.

## Production-Scale Engineering Status

The requested production campaign was benchmarked on the actual `12^3 x 24`
path rather than certified from reduced data.  The original Python gauge path
was too slow, so this PR now includes a Numba-backed gauge-update engine selected
by `--engine auto` when Numba is available.  The benchmark command is:

```bash
python3 scripts/yt_direct_lattice_correlator_production.py --benchmark-production --engine numba --profile-heatbath
```

It wrote a non-certificate optimized benchmark artifact at
`outputs/yt_direct_lattice_correlator_production/L12xT24/production_scale_benchmark_numba_2026-04-30.json`
and a Numba profile note at
`outputs/yt_direct_lattice_correlator_production/L12xT24/heatbath_profile_numba.txt`.
The original Python reference benchmark remains at
`outputs/yt_direct_lattice_correlator_production/L12xT24/production_scale_benchmark_2026-04-30.json`.

Measured `12^3 x 24` component timings after the Numba gauge-engine fix:

| Component | Seconds |
|---|---:|
| One heat-bath sweep | `1.633316` |
| One overrelaxation sweep | `1.105756` |
| One plaquette pass | `0.158155` |
| One APE smearing step | `12.563164` |
| One staggered-Dirac build | `3.492021` |
| One CG solve | `1.244262` |
| One one-mass, three-source correlator measurement | `5.182000` |

With the requested protocol of 1000 thermalization sweeps, 1000 saved
configurations, 20 separation sweeps, four overrelaxation sweeps per heat-bath
sweep, and three mass points, the linear volume extrapolation from the measured
optimized `12^3 x 24` timings is:

| Volume | Estimated wall time |
|---|---:|
| `12^3 x 24` | `1.80 days` |
| `16^3 x 32` | `5.69 days` |
| `24^3 x 48` | `28.82 days` |
| Total | `36.31 days` |

The Python reference path estimated `518.67 days`, so the compiled gauge path
removes the first-order blocker by roughly a factor of 14 in the end-to-end
campaign estimate.  The campaign is still not completed inside this PR update:
the `24^3 x 48` volume dominates the remaining wall time, APE smearing is still
Python-side, and the current fermion solve forms `D^dagger D` explicitly, which
remains a memory-risk path at the largest volume.

For long-running execution, production-targeted runs now write per-volume
artifacts under `outputs/yt_direct_lattice_correlator_production/L{L}xT{T}/`
and support `--resume` to reuse completed volume artifacts instead of restarting
the full campaign.

No production certificate replaces the reduced-scope certificate in this PR
update.  Strict mode therefore remains a real failure until the optimized engine
or an external compute campaign supplies the full three-volume production data.

A future passing production certificate must supply this budget:

| Component | Required content |
|---|---|
| Statistical | jackknife/bootstrap correlator and fit uncertainty |
| Heavy-mass tuning | interpolation/extrapolation in the top mass parameter |
| Finite volume | comparison across `12^3`, `16^3`, and `24^3` volumes |
| Finite spacing | Sommer-scale or equivalent scale-control residual |
| Scale setting | physical length-anchor uncertainty |
| Matching | lattice-to-continuum mass/coupling scheme conversion |
| Running bridge | SM/QCD RGE truncation and threshold matching |
| VEV input | propagated uncertainty from the substrate `v` input |

The strict runner requires the total uncertainty to be finite and sub-percent,
and it requires the final `m_t(pole)` and `y_t(v)` values to agree with their
comparators within the stated one-sigma window.

## Cross-Validation Against External Comparators

The production comparator set is:

- PDG 2025 top-quark listing: `m_t = 172.56 +/- 0.31 GeV` current average;
- PDG listing historical/superseded ATLAS combination: `172.69 +/- 0.25 +/-
  0.41 GeV`, kept only as a cross-check target;
- SM running-Yukawa target near `y_t(v) = 0.917`, with the certificate required
  to state the scheme and scale used for this comparator.

Standard methodology references for the measurement route include:

- R. Sommer, "A New Way to Set the Energy Scale in Lattice Gauge Theories...",
  arXiv:hep-lat/9310022, for the Sommer scale;
- FLAG Review 2021, Eur. Phys. J. C 82, 869 (2022), for lattice-QCD
  systematic-review conventions and staggered-fermion context;
- PDG 2025, top-quark listing and QCD/SM review material, for the external
  mass comparator and running conventions.

## Measured `y_t/g_s = 1/sqrt(6)` Verification

The strict production certificate must include a ratio block:

```text
ratio_check:
  y_t_lattice: measured from m_t and v
  g_s_lattice: independently measured strong coupling on the same substrate
  ratio: y_t_lattice / g_s_lattice
  uncertainty: ...
  used_as_definition: false
```

The strict runner checks that the reported ratio agrees with `1/sqrt(6)` within
the supplied uncertainty.  That check is a posterior cross-validation.  It is
not allowed to feed into the mass extraction or Yukawa computation.

## Current Runner State

Strict mode:

```bash
python3 scripts/frontier_yt_direct_lattice_correlator.py
```

Current reduced-scope outcome:

```text
RESULT: FAIL
```

The failure is expected: the certificate is explicitly `reduced_scope`, uses
`2^3` and `3^3` test volumes rather than `12^3`, `16^3`, and `24^3`, has only
three saved configurations per volume, lacks an independently measured `g_s`
ratio, and does not match the top-mass/Yukawa comparators.

Reduced production-harness command:

```bash
python3 scripts/yt_direct_lattice_correlator_production.py
```

Pilot command:

```bash
python3 scripts/yt_direct_lattice_correlator_production.py --pilot-targets --engine numba --resume
```

Full production target command, not run in this PR update:

```bash
python3 scripts/yt_direct_lattice_correlator_production.py --production-targets --engine auto --resume
```

Scout mode:

```bash
python3 scripts/frontier_yt_direct_lattice_correlator.py --scout
```

The scout uses tiny lattices, minimal update sweeps, a gauge-dressed heavy
staggered-correlator smoke construction, and a single-exponential fitter.  It
checks that the infrastructure path runs.  It does not produce a retained
top-Yukawa value.

## Explicit Non-Claims

This note does not claim:

- audit retention before the audit ledger ratifies it;
- that production-scale top-correlator data already exist;
- a repair of the `v = 246 GeV` derivation chain;
- a repair of the `g_bare = 1` substrate input;
- a derivation of the Sommer-scale physical anchor;
- a bypass of the SM/QCD running and matching bridge;
- a direct promotion of EW, top, Higgs, CKM, or `g_bare` downstream rows;
- that the prior Ward-identity theorem is audit-clean;
- that the scout, reduced, or pilot numerical masses are physical evidence.

Safe current claim:

> The branch adds a proposed-retained direct staggered-correlator measurement
> gate for `m_t -> y_t`, with scout-mode infrastructure evidence, reduced-scope
> and pilot MC/correlator certificates, a Numba production engine with resume
> artifacts, and a strict production-certificate gate that blocks prior
> Ward/matrix-element authority.

Unsafe current claim:

> The framework has already retained a direct lattice derivation of
> `y_t(v) = 0.917`.

That stronger statement belongs only after production correlator data exist and
the audit ledger ratifies the row.
