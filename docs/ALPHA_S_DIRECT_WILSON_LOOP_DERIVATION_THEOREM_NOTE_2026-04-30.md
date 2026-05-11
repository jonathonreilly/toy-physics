# Direct Wilson-Loop `alpha_s(M_Z)` Derivation Gate

**Date:** 2026-04-30
**Type:** bounded_theorem
**Claim scope:** the lattice Wilson-loop certificate on the
`Cl(3)/Z^3 graph-first SU(3)` Wilson gauge surface at `g_bare = 1`,
`beta = 6` — i.e., the static-potential extraction from rectangular
Wilson-loop expectation values, evaluated by the strict-passing
production runner. The **bridge to `alpha_s(M_Z)`** depends on four
external/admitted-context items: external Sommer scale setting,
standard QCD running, threshold matching, and a sea-quark / full-QCD
bridge. These are explicitly **out of scope** of this note's
load-bearing claim. The PDG comparator
`alpha_s(M_Z) = 0.1180 +/- 0.0009` is **never** consumed as a
derivation input; it appears only in the audit-comparator role.
**Status:** independent audit required. Under the scope-aware classification
framework, ratified status is computed by the audit pipeline from audit lane
data and the dependency chain; no author-side tier is asserted in source.
**Primary runner:** `scripts/frontier_alpha_s_direct_wilson_loop.py`

**Audit-conditional perimeter (2026-05-05):**
The audit lane has classified this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and load-bearing
step class `B`. The audit chain-closure explanation is exact: "the
in-packet runner validates a JSON certificate and comparator gates
rather than recomputing the production Wilson loops, static-potential
fit, scheme conversion, and running bridge from raw retained inputs.
The full alpha_s(M_Z) claim also explicitly depends on external
Sommer scale setting, QCD running, threshold matching, and the
sea-quark/full-QCD bridge." The audit-stated repair target is:
"dependency_not_retained: replace the superseded minimal-axioms
citation with the current canonical framework-baseline memo and
provide a retained-grade bridge theorem or independently auditable
certificate derivation for Sommer scale setting, QCD running,
threshold matching, and the sea-quark/full-QCD bridge." This
rigorization edit only sharpens the boundary of the conditional
perimeter; nothing here promotes audit status, and the runner sha256
remains `0bfcc76b4b64a087157b0644db297c2c1def1d2878c918c338d96b94d0affa0f`.

## Theorem Statement

Candidate theorem under test:

On the Cl(3)/Z^3 graph-first `SU(3)` Wilson gauge surface with `g_bare = 1`
and Wilson `beta = 2 N_c / g_bare^2 = 6`, the renormalized strong coupling
extracted directly from rectangular Wilson-loop expectation values,
the static potential, the Sommer scale, and the standard QCD running bridge
to `M_Z` should give

```text
alpha_s(M_Z) = 0.1181 +/- total_direct_Wilson_loop_uncertainty.
```

This note records a strict-passing production certificate for the direct
Wilson-loop/static-potential route.  It remains `proposed_retained`: the audit
ledger, not this note, decides whether the theorem is ratified.

The current comparator is the PDG 2025 world average
`alpha_s(M_Z) = 0.1180 +/- 0.0009`; PDG also reports a restricted combination
giving `0.1179 +/- 0.0008`.  The target `0.1181` is inside that current
one-sigma band.

## Methodology

The audit-candidate route is deliberately the standard Wilson-loop/static-
potential route, not the existing coupling-definition chain.

1. **Wilson action setup.**  Use the graph-first `SU(3)` gauge sector from
   [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
   and the `g_bare = 1` canonical-normalization input.  As of 2026-05-03 the
   current canonical framework-baseline memo is
   [MINIMAL_AXIOMS_2026-05-03.md](MINIMAL_AXIOMS_2026-05-03.md), which
   explicitly supersedes the 2026-04-11 file (the 2026-04-15 rewrite that
   added staggered-Dirac, physical-lattice, and `g_bare = 1 / u_0 / APBC`
   as additional axioms has been backed out, and `g_bare = 1` is now an open
   gate, not part of the physical `Cl(3)` local algebra / `Z^3` spatial
   substrate baseline).  The earlier
   [MINIMAL_AXIOMS_2026-04-11.md](MINIMAL_AXIOMS_2026-04-11.md) citation is
   retained here only as the historical anchor consistent with the
   2026-04-30 production certificate; the live framework-language anchor is
   the 2026-05-03 successor.  This fixes the Wilson gauge action at `beta = 6`.
   A production run must include at
   least three lattice volumes and enough scale-control information to separate
   finite-volume, finite-spacing, and scale-setting uncertainties.

2. **Wilson-loop measurement.**  Measure rectangular loops `W(R,T)` over
   multiple `R` and `T`, with enough statistics that loop means and errors are
   stable.  The runner requires explicit loop means, standard errors, and
   configuration counts.

3. **Static-potential extraction.**  Extract
   `V(R) = -lim_{T -> infinity} (1/T) log W(R,T)` using plateau fits.  The
   certificate must carry plateau pass/fail fields and `chi^2/dof` diagnostics.
   Large-distance data should fit the confinement form
   `V(R) = sigma R + e/R + V_0 + ...`; short-distance data support the force
   coupling.

4. **Running-coupling extraction.**  Extract the force-scheme coupling from
   the static force,
   `alpha_qq(1/R) = (R^2 / C_F) dV/dR`, with `C_F = 4/3`, at multiple
   physical scales.  The sign convention is fixed by
   `F(R) = dV/dR > 0` for an attractive short-distance potential
   `V(R) ~ -C_F alpha_s/R`.

5. **Scale setting.**  Use the Sommer scale defined by
   `R^2 dV/dR = 1.65` at `R = r_0`.  The physical value of `r_0` is an
   external matching number.  This is not an axiom-only route.

6. **Running to `M_Z`.**  Convert the extracted short-distance coupling to the
   chosen continuum scheme and run to `M_Z` using the standard high-loop QCD
   beta function and threshold matching.  This is the retained running bridge,
   not a framework-native identity.

Standard references for this route include Sommer's scale-setting definition
from the static force, the FLAG lattice-QCD alpha_s review machinery, and the
PDG QCD review world-average treatment:

- R. Sommer, "A New Way to Set the Energy Scale in Lattice Gauge Theories...",
  arXiv:hep-lat/9310022.
- FLAG Review 2021, Eur. Phys. J. C 82, 869 (2022).
- PDG 2025 QCD review, Section 9.4.

## Decoration-Trap Avoidance

The older `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24`
route is not authority for this note because its load-bearing step is
algebra from the definitions `alpha_LM = alpha_bare/u_0` and
`alpha_s(v) = alpha_bare/u_0^2`.

The older `alpha_s_derived_note` route is also not authority here because
the `0.1181` value is reproducible only after supplying the plaquette
dependency and an unsupplied low-energy running bridge.

This route avoids that trap by construction:

- it does not define `alpha_s(v)` as `alpha_bare/u_0^2`;
- it does not use `alpha_LM = alpha_bare/u_0` as authority;
- it does not use `<P>` or `u_0` as a running-coupling input;
- it extracts the coupling from Wilson-loop static-potential data;
- it treats the existing `alpha_LM/u_0` value only as a numerical
  consistency cross-check after the direct result is already obtained.

The runner enforces this by requiring a certificate whose metadata sets:

```text
uses_alpha_lm_chain = false
uses_alpha_bare_over_u0_squared = false
uses_plaquette_as_running_coupling_input = false
```

and by rejecting forbidden authority keys such as `u0`, `alpha_lm`,
and `alpha_bare_over_u0_squared`.

## Numerical Result And Uncertainty Budget

The 2026-05-01 replacement production run uses unsmeared rectangular Wilson
loops on three already-thermalized `beta = 6`, `g_bare = 1` Wilson ensembles.
An APE-smeared pilot was rejected because its `R >= 2` long-`T` tails were
less stable in this backend; the strict-passing certificate therefore uses raw
Wilson loops, which are the direct static-potential observable.

Certificate:

```text
outputs/alpha_s_direct_wilson_loop_certificate_2026-04-30.json
```

Strict runner result:

```text
PASS=18  FAIL=0
```

Direct result:

```text
alpha_s(M_Z) = 0.1179962733 +/- 0.0067923686
```

This is inside the runner's one-PDG-sigma central-value window around
`0.1180 +/- 0.0009`, but the direct uncertainty is still dominated by
fixed-substrate scale-setting residuals.  No ratified source status is
claimed.

Production inputs used by the certificate:

| Volume | Saved Wilson-loop configurations | Measurement cadence | Notes |
|---|---:|---:|---|
| `12^3 x 24` | 500 | separation 6, 4 overrelaxation sweeps / heat-bath sweep | unsmeared `R <= 4`, `T <= 6` |
| `16^3 x 32` | 500 | separation 6, 4 overrelaxation sweeps / heat-bath sweep | unsmeared `R <= 4`, `T <= 6` |
| `24^3 x 48` | 500 | separation 1, 4 overrelaxation sweeps / heat-bath sweep | unsmeared `R <= 4`, `T <= 6` |

The certificate builder uses blocked jackknife errors with block size `11`
for the saved Wilson-loop configurations.

Per-volume static-potential plateaus:

| Volume | `V(1)` | `V(2)` | `V(3)` | `V(4)` | Plateau passes |
|---|---:|---:|---:|---:|---:|
| `12^3 x 24` | 0.413395 | 0.609563 | 0.713650 | 0.781118 | 4/4 |
| `16^3 x 32` | 0.413410 | 0.609443 | 0.714788 | 0.793395 | 4/4 |
| `24^3 x 48` | 0.412744 | 0.607600 | 0.711605 | 0.793594 | 4/4 |

The scale setting uses a fixed-`g_bare` global Sommer fit with volume-specific
additive constants and common Cornell `sigma` and Coulomb coefficient:

| Quantity | Value |
|---|---:|
| global `r0/a` | 5.0056762542 |
| global `a` from `r0 = 0.5 fm` | 0.0998866036 fm |
| Cornell `sigma` | 0.0544856367 |
| Cornell Coulomb coefficient `e` | 0.2847645839 |

Per-volume independent `r0/a` values are kept as diagnostics and feed the
finite-spacing/fixed-substrate residual:

```text
12^3 x 24: 5.3255995278
16^3 x 32: 4.9090949907
24^3 x 48: 4.8293276704
```

The running analysis excludes on-axis `R/a < 2` points as cutoff-dominated
diagnostics and averages the global Cornell force-scheme values over
`R/a in [2.0, 3.5]` before applying the four-loop `N_f = 5` bridge to `M_Z`.

Uncertainty budget:

| Component | Value |
|---|---:|
| Statistical / scaling-window stderr | 0.0009356182 |
| Finite volume | 0.0005000000 |
| Finite spacing / fixed-substrate residual | 0.0062624069 |
| Scale setting | 0.0023599255 |
| Running bridge | 0.0004731818 |
| Total | 0.0067923686 |

The scale-setting component is the builder's conservative `2% * alpha_s(M_Z)`
allowance for the physical `r_0` anchor, not an independent phenomenological
error analysis of `r_0`.

The existing `alpha_LM/u_0` route gives `0.1181` and is recorded only as a
consistency diagnostic.  The direct result differs from that value by
`0.0001037267`.

## Phase 2 Production Infrastructure

On 2026-04-30, Phase 2 was scoped against the existing framework MC
infrastructure.  The repository currently has small-volume pure-gauge
Metropolis code paths:

- `scripts/frontier_alpha_s_direct_wilson_loop.py` scout mode;
- `scripts/frontier_plaquette_self_consistency.py`;
- `scripts/frontier_g_bare_critical_feature_scan.py`;
- `scripts/frontier_confinement_string_tension.py`.

These are useful for scout/qualitative checks, but they are not a production
Cabibbo-Marinari heat-bath / overrelaxation Wilson-loop pipeline with smearing,
autocorrelation control, and static-potential plateau analysis.

Follow-up inspection found `scripts/frontier_color_projection_mc.py`, which
contains a Cabibbo-Marinari-style heat-bath routine for a `4^4`
color-projection support calculation. That path is also a pure-Python
site/link loop, is symmetric-`L^4` only, has no overrelaxation sweep, and has
no Wilson-loop/static-potential analysis stack. It benchmarks at roughly
`180 us/link`, slower than the Metropolis benchmark below, so it is not the
requested production replacement.

A benchmark on the requested first production volume used the array-backed
Wilson Metropolis implementation:

```text
12^3x24: 14.181 s/sweep, links=165888, 85.49 us/link, acc=0.152
```

Using the requested protocol

```text
1000 thermalization sweeps + 1000 measurements * 20 separated sweeps
```

gives the following sweep-only estimate:

| Volume | Estimated seconds / sweep | Estimated sweep-only wall time |
|---|---:|---:|
| `12^3 x 24` | 14.2 | 3.4 days |
| `16^3 x 32` | 44.8 | 10.9 days |
| `24^3 x 48` | 226.9 | 55.1 days |
| Total | - | 69.4 days |

This excludes the expensive measurement pass for all Wilson loops
`R,T in {1,...,8}`, APE/HYP smearing, jackknife/bootstrap analysis, plateau
fitting, and any reruns needed for autocorrelation or failed plateaus.

The first environment check found no `numba`, `cupy`, `Cython`, `pybind11`, or
`meson`; only `cffi` and `clang` were available.  A follow-up production
attempt installed `numba` and added a compiled backend in
`scripts/alpha_s_numba_wilson_loop_mc.py` with `@njit` kernels for the SU(3)
matrix helpers, Cabibbo-Marinari SU(2)-subgroup heat-bath update,
overrelaxation update, staple sums, APE spatial smearing, plaquette
diagnostics, and rectangular Wilson-loop measurement.

The first compiled benchmark exposed a real bug: the SU(2) subgroup projection
used the raw `2x2` determinant rather than the quaternionic SU(2) component
that controls the local `Re Tr(R W)` action.  After replacing that projection,
rewriting the staple builder to use scratch buffers, and adding
checkerboard-parallel sweeps plus a parallel Wilson-loop measurement kernel,
the compiled backend passes the local speed and stability checks.

| Compiled benchmark | Timing | Speedup vs pure-Python heat-bath | Gate |
|---|---:|---:|---|
| `12^3 x 24`, heat-bath only | `0.941 us/link` | `194.01x` | PASS |
| `16^3 x 32`, heat-bath only | `1.421 us/link` | `128.39x` | PASS |
| `24^3 x 48`, heat-bath only | `1.198 us/link` | `152.35x` | PASS |
| `8^4`, heat-bath plus 4 overrelaxation sweeps | `3.506 us/link` | `52.06x` | PASS |
| `8^3 x 16`, heat-bath plus 4 overrelaxation sweeps | `3.505 us/link` | `52.07x` | PASS |
| `12^3 x 24`, heat-bath plus 3 overrelaxation sweeps | `3.074 us/link` | `59.38x` | PASS |

The full larger-volume heat-bath-plus-three-overrelaxation benchmarks are
stable but do not clear `50x` when the deliberately extra microcanonical
sweeps are included in the denominator:

```text
16^3 x 32, OR=3: 4.963 us/link, 36.77x
24^3 x 48, OR=3: 4.018 us/link, 45.42x
```

The heat-bath kernel itself clears the `50x` gate on those geometries.  The
remaining blocker is not compiled inner-loop availability; it is the wall
clock for the full three-volume production campaign.

Using `OR=3`, `400` saved configurations per volume, and full `R,T <= 8`
Wilson-loop measurements, the current estimate is:

| Volume | Update wall time | Measurement wall time | Total estimate |
|---|---:|---:|---:|
| `12^3 x 24` | 2.97 h | 0.35 h | 3.33 h |
| `16^3 x 32` | 15.18 h | 1.11 h | 16.29 h |
| `24^3 x 48` | 62.21 h | 5.61 h | 67.83 h |
| Total | 80.37 h | 7.07 h | 87.44 h |

A follow-up `12^3 x 24` autocorrelation pilot measured the slowest tracked
observable at `tau_int = 1.0697` sweeps and recommends
`separation = ceil(5 tau_int) = 6` rather than the conservative fixed
separation `50`.  With `500` saved configurations per volume, which satisfies
the strict runner's `n_cfg >= 500` loop-statistics threshold, the revised
valid-production estimate is:

| Volume | Update wall time | Measurement wall time | Total estimate |
|---|---:|---:|---:|
| `12^3 x 24` | 0.51 h | 0.45 h | 0.96 h |
| `16^3 x 32` | 2.89 h | 1.43 h | 4.32 h |
| `24^3 x 48` | 11.85 h | 7.26 h | 19.11 h |
| Sequential total | 15.25 h | 9.15 h | 24.39 h |

The production run must still recompute autocorrelation and use blocked
jackknife/bootstrap on the actual saved ensembles.

The earlier production-planning blocker is recorded in:

```text
outputs/alpha_s_wilson_loop_production/PHASE2_BLOCKER_REPORT_2026-04-30.md
outputs/alpha_s_wilson_loop_production/phase2_blocker_report_2026-04-30.json
outputs/alpha_s_wilson_loop_production/COMPILED_MC_NUMBA_BENCHMARK_REPORT_2026-04-30.md
```

The first APE-smeared production certificate existed but failed the strict
static-potential and running-coupling checks: its long-`T` tails for `R > 1`
were too noisy and produced `SUMMARY: PASS=8 FAIL=6`.  That failed certificate
was not promoted.  The current certificate replaces it with the unsmeared
Wilson-loop production data summarized above and passes strict mode.

Required uncertainty budget carried by a passing certificate:

| Component | Required content |
|---|---|
| Statistical | Wilson-loop and static-potential fit uncertainty |
| Finite volume | multi-volume extrapolation or bounded residual |
| Finite spacing | scale-control/continuum or fixed-substrate discretization residual |
| Scale setting | uncertainty from the physical `r_0` anchor |
| Running bridge | scheme conversion, beta-function truncation, and threshold matching |

The success window for the final certificate is:

```text
abs(alpha_s(M_Z) - 0.1180) <= 0.0009
```

with an internal target consistency check against `0.1181`.

## Cross-Validation Against The Existing Chain

The existing `ALPHA_S_DERIVED_NOTE.md` chain gives

```text
alpha_s(M_Z) = 0.1181
```

using the plaquette / `u_0` surface and the running bridge.  For this new
route that number is a cross-check only.  It is not allowed to enter the
Wilson-loop static-potential extraction, the Sommer-scale fit, or the final
`alpha_s(M_Z)` value.

The runner requires the direct Wilson-loop result and the existing-chain
cross-check to agree within the stated comparison tolerance, while separately
requiring `used_as_authority = false` for the existing chain.

## Explicit Non-Claims

This note does not claim:

- a fresh derivation of `<P> = 0.5934`;
- a fresh derivation of `g_bare = 1`;
- an axiom-only determination of physical units;
- a bypass of the Sommer-scale physical anchor;
- a bypass of the QCD running / threshold bridge to `M_Z`;
- a direct promotion of CKM, EW, YT/top, or hierarchy downstream rows;
- audit retention before the audit ledger ratifies the row.

It also does not claim that a pure-gauge quenched calculation alone is
automatically identical to full physical `N_f = 5` QCD at `M_Z`.  Any
certificate must state how the continuum scheme, sea-quark content,
thresholds, and running bridge are handled.

## Current Runner State

Run:

```bash
python3 scripts/frontier_alpha_s_direct_wilson_loop.py
```

Expected current outcome:

```text
SUMMARY: PASS=18  FAIL=0
Strict gate passed: direct Wilson-loop alpha_s route is ready for audit.
```

The passing result uses the certificate at:

```text
outputs/alpha_s_direct_wilson_loop_certificate_2026-04-30.json
```

or a supplied `--certificate` path with the same schema whose static-potential,
Sommer-scale, running-coupling, and final `alpha_s(M_Z)` checks pass.

For infrastructure smoke only, run:

```bash
python3 scripts/frontier_alpha_s_direct_wilson_loop.py --scout --scout-volumes 2,3
```

The scout mode generates tiny low-stat `SU(3)` Wilson configurations and
Wilson-loop values on multiple volumes.  It is useful for checking that the
local Monte Carlo machinery runs, but it is not a static-potential production
measurement and cannot certify `alpha_s(M_Z)`.

## Claim Boundary Pending Audit

Safe current claim:

The framework now has an audit-visible direct Wilson-loop production
certificate (the lattice static-potential extraction at `beta = 6` on the
`Cl(3)/Z^3 SU(3)` surface) and strict gate passing without using the known
`alpha_LM/u_0` decoration route as authority.

Unsafe current claim:

That the theorem is ratified at the `alpha_s(M_Z)` level. Independent
audit is required, and the four external/admitted-context items must be
resolved or explicitly accepted by the audit lane before the repository
can treat the full `alpha_s(M_Z)` bridge as closed.

## Cited authority chain (audit-conditional perimeter register)

The audit lane's `notes_for_re_audit_if_any` field names the conditional
perimeter precisely. The table below registers each cited authority and its
current ledger status, so the conditional perimeter is explicit.

| Cited authority | Note | Effective status (2026-05-10) | Conditional on |
|---|---|---|---|
| Graph-first `SU(3)` gauge surface | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | `retained_bounded` | none in this row's perimeter |
| Physical `Cl(3)` local algebra and `Z^3` spatial substrate baseline | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | `meta` | canonical framework-baseline memo; this row does not turn the meta note into a retained-grade dependency |
| Earlier (superseded) baseline memo | [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) | `meta` (superseded by 2026-05-03) | not retained-grade authority; cited as historical anchor only |
| Wilson action at `beta = 6` and `g_bare = 1` | inline in this note | conditional on the audit-flagged `g_bare` open-gate status (2026-05-03 minimal-axioms restoration moved `g_bare = 1` from axiom-like language to open gate) | `g_bare` open-gate closure |
| Sommer scale `r_0 = 0.5 fm` | external (Sommer 1993, FLAG 2021) | external admitted-context | retained bridge theorem from the framework's lattice scale to physical units |
| 4-loop QCD beta function for `N_f = 5` | external (PDG 2025 QCD review section 9.4) | external admitted-context | retained bridge theorem from short-distance lattice coupling to continuum scheme + running |
| PDG-style threshold matching across `m_c`, `m_b` | external (PDG 2025) | external admitted-context | retained bridge theorem for `N_f = 4 -> 5` matching |
| Sea-quark / full-QCD bridge | not in current packet | not yet packaged | retained bridge theorem from pure-gauge Wilson surface to dynamical-quark physical alpha_s at `M_Z` |
| `<P>` analytic insertion at `beta = 6` (cross-check only) | [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md) | `audited_conditional` | only enters as a cross-check, not as authority on this row |

The audit-conditional perimeter of this row is therefore precisely the
last four rows of the table plus the `g_bare` open-gate dependency: the
in-runner certificate validation does not itself recompute Sommer scale
setting, QCD running, threshold matching, or the sea-quark bridge, and
each remains an external admitted-context item that the audit verdict
flags as not yet retained-grade in-framework. The Wilson-loop /
static-potential measurement at `beta = 6` and the local certificate
checks (plateau pass/fail, Cornell fit, multi-volume residual,
uncertainty budget) are not part of the conditional perimeter at the
stated scope.

## Audit-aware repair path

Per `audit_ledger.json`, `notes_for_re_audit_if_any` for this row, the
audit-stated repair path is two-pronged:

1. **Replace the superseded minimal-axioms citation.** Update internal
   references so the live canonical framework-baseline anchor is
   [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md). This
   rigorization edit performs that update in the methodology section
   while preserving the historical 2026-04-11 anchor as a cross-reference
   for the 2026-04-30 certificate. The successor minimal-axioms note
   continues to carry `claim_type: meta` and is the canonical
   baseline-language memo.
2. **Provide retained bridge theorems for the four external items.**
   Land retained-grade audited bridge notes for:
   - Sommer scale setting from the framework's lattice surface to the
     physical `r_0` anchor;
   - QCD running from the short-distance lattice coupling to `M_Z`;
   - threshold matching across `m_c`, `m_b`;
   - the sea-quark / full-QCD bridge from pure-gauge Wilson to
     `N_f = 5` physical `alpha_s(M_Z)`.

   Until each of those four bridges is retained-grade in-framework,
   they continue to enter as admitted external authorities, and this
   row's effective status caps at `audited_conditional` regardless of
   the in-packet certificate's strict pass/fail state.

Either repair narrows the conditional perimeter; this rigorization edit
only sharpens the boundary register and refreshes the methodology's
baseline-memo citation, without changing audit status.

## Out of scope (admitted-context to this note)

The following items are explicitly **NOT** load-bearing claims of this
note. They depend on external authorities / open derivations and enter
only as admitted-context:

1. **External Sommer scale setting.** The Sommer parameter `r_0`
   provides the lattice-to-physical length-scale calibration. This
   note treats the Sommer-scale calibration as an external admitted
   input.

2. **Standard QCD running.** The running of `alpha_s` from the lattice
   short-distance scale to `M_Z` follows standard 4-loop QCD
   beta-function machinery. This note treats the running machinery as
   admitted external authority, not as a load-bearing internal
   derivation.

3. **Threshold matching.** Matching across heavy-quark mass thresholds
   (charm, bottom) is admitted from standard PDG-style threshold-matching
   formulas, not derived here.

4. **Sea-quark / full-QCD bridge.** The bridge from the framework's
   pure-gauge Wilson surface to full-QCD physics including dynamical
   sea quarks is **not** closed by the cited authorities or
   constructed by the runner.

5. **PDG comparator `alpha_s(M_Z) = 0.1180 +/- 0.0009`.** The PDG 2025
   world average appears only in the audit-comparator role. It is
   **never** consumed as a derivation input; the framework target
   `0.1181` is computed from the lattice Wilson-loop chain plus the
   four admitted bridges above, then compared to PDG for posture.

The **in-scope content** of this note is the Wilson-loop certificate
itself (the strict-passing static-potential extraction at `beta = 6` on
the `Cl(3)/Z^3 SU(3)` surface). The full `alpha_s(M_Z)` claim depends on
the four admitted external bridges above and is therefore out of scope
of the in-scope load-bearing content.
