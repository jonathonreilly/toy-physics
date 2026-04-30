# Direct Wilson-Loop `alpha_s(M_Z)` Derivation Gate

**Date:** 2026-04-30
**Status:** proposed_retained measurement route, pending production Wilson-loop data and audit
**Primary runner:** `scripts/frontier_alpha_s_direct_wilson_loop.py`

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

This note does not yet claim that the candidate theorem has landed.  The
strict runner currently requires a production Wilson-loop/static-potential
certificate and fails if that certificate is absent.  That failure is the
correct audit behavior until the measurement exists.

The current comparator is the PDG 2025 world average
`alpha_s(M_Z) = 0.1180 +/- 0.0009`; PDG also reports a restricted combination
giving `0.1179 +/- 0.0008`.  The target `0.1181` is inside that current
one-sigma band.

## Methodology

The retained-grade route is deliberately the standard Wilson-loop/static-
potential route, not the existing coupling-definition chain.

1. **Wilson action setup.**  Use the graph-first `SU(3)` gauge sector from
   [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
   and the `g_bare = 1` canonical-normalization input from
   [MINIMAL_AXIOMS_2026-04-11.md](MINIMAL_AXIOMS_2026-04-11.md).  This fixes
   the Wilson gauge action at `beta = 6`.  A production run must include at
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

The audit ledger flags
`alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` as
`audited_decoration` because the load-bearing step is algebra from the
definitions `alpha_LM = alpha_bare/u_0` and
`alpha_s(v) = alpha_bare/u_0^2`.

The ledger also flags `alpha_s_derived_note` as `audited_conditional` because
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

No retained direct Wilson-loop numerical result is currently present in this
branch.  The strict gate is therefore blocked, not promoted.

## Phase 2 Production Attempt: Blocked, No Certificate

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

The environment check also found no `numba`, `cupy`, `Cython`, `pybind11`, or
`meson`; only `cffi` and `clang` are available for a future compiled kernel.

The production evidence therefore remains absent.  The branch records the
blocker in:

```text
outputs/alpha_s_wilson_loop_production/PHASE2_BLOCKER_REPORT_2026-04-30.md
outputs/alpha_s_wilson_loop_production/phase2_blocker_report_2026-04-30.json
```

No production certificate was generated, no direct `alpha_s(M_Z)` value is
claimed, and the strict runner must continue to fail until real production
Wilson-loop/static-potential data exist.

Required uncertainty budget for a future passing certificate:

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
STRICT GATE BLOCKED
missing production Wilson-loop/static-potential certificate
```

This is intentional.  A passing result requires production data at:

```text
outputs/alpha_s_direct_wilson_loop_certificate_2026-04-30.json
```

or a supplied `--certificate` path with the same schema.

For infrastructure smoke only, run:

```bash
python3 scripts/frontier_alpha_s_direct_wilson_loop.py --scout --scout-volumes 2,3
```

The scout mode generates tiny low-stat `SU(3)` Wilson configurations and
Wilson-loop values on multiple volumes.  It is useful for checking that the
local Monte Carlo machinery runs, but it is not a static-potential production
measurement and cannot certify `alpha_s(M_Z)`.

## Claim Boundary Until Data Exist

Safe current claim:

The framework now has an audit-visible direct Wilson-loop alpha_s retention
gate that blocks the known `alpha_LM/u_0` decoration route from serving as
authority.

Unsafe current claim:

That `alpha_s(M_Z) = 0.1181` has already been directly measured from
framework Wilson loops at retained grade.
