# C-iso Numerical Convergence Bounded Support Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Scope:** bounded numerical support for the Convention C-iso engineering
frontier at the epsilon-witness scale. The result is conditional on the
imported finite-volume ensemble summaries listed below, the cited C-iso
source notes, and the paired runner's Weyl-integration and refit arithmetic.
It is not a raw-MC regeneration theorem and does not promote any parent
surface.
**Status authority:** independent audit lane only; effective status is
pipeline-derived.

**Primary runner:** [`scripts/cl3_c_iso_numerical_convergence_2026_05_10_numconv.py`](../scripts/cl3_c_iso_numerical_convergence_2026_05_10_numconv.py)
**Cached output:** [`logs/runner-cache/cl3_c_iso_numerical_convergence_2026_05_10_numconv.txt`](../logs/runner-cache/cl3_c_iso_numerical_convergence_2026_05_10_numconv.txt)
**Runner artifact:** [`outputs/action_first_principles_2026_05_10/c_iso_numerical_convergence/results_mode-analytic.json`](../outputs/action_first_principles_2026_05_10/c_iso_numerical_convergence/results_mode-analytic.json)

## Question

The path-integral epsilon-witness source note
[`EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness.md`](EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness.md)
left the C-iso contribution at xi=4 as a large engineering systematic. The
SU(3) single-plaquette correction note
[`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)
gave analytic and numerical control of the single-plaquette Wilson/heat-kernel
ratio.

The bounded question here is narrower:

> given the cited L=3,4,6 ensemble summaries and the additional L=8,10
> summary measurements recorded in this branch, does applying the numerical
> Weyl single-plaquette correction and refitting the xi=4 finite-volume scan
> reduce the combined C-iso budget to the epsilon-witness scale?

## Answer

Yes, as bounded numerical support. The runner performs three load-bearing
checks:

- numerical Weyl integration over the SU(3) Cartan torus recovers the
  Wilson single-plaquette asymptotic coefficient `c_2 = -1` to about 0.2%;
- a weighted fit of the imported xi=4 volume scan
  `L = {3, 4, 6, 8, 10}` to
  `P(L) = P_inf + a/L^2 + b/L^4` gives
  `P_inf = 0.44044 +/- 0.00026`;
- applying the Weyl-truth single-plaquette correction gives
  `<P>_KS_combined(xi=4, L->infinity) = 0.41092 +/- 0.00026`, with the
  residual budget below `epsilon_witness = 3e-4`.

The same runner also applies the correction to xi=8 and xi=16 finite-volume
inputs. The corrected values spread by about 35%, so a single-plaquette C-iso
correction does not explain the deep large-xi regime. That is useful negative
science: it identifies a multi-plaquette obstruction away from the xi=4
operating point.

## Imported Values And Support

The runner is an arithmetic and quadrature verifier, not a raw ensemble
generator in its default mode. Its load-bearing imported values are:

| L | geometry | `<P_sigma>(xi=4)` | source |
|---:|:--|---:|:--|
| 3 | `3^3 x 12` | `0.44545 +/- 0.00034` | [`EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness.md`](EXACT_TIER_EWITNESS_BOUNDED_NOTE_2026-05-07_ewitness.md) |
| 4 | `4^3 x 16` | `0.44329 +/- 0.00016` | same source |
| 6 | `6^3 x 24` | `0.44207 +/- 0.00022` | same source |
| 8 | `8^3 x 32` | `0.44099 +/- 0.00026` | imported branch summary value |
| 10 | `10^3 x 40` | `0.44090 +/- 0.00023` | imported branch summary value |

The L=8 and L=10 values are valuable because they materially tighten the
finite-volume refit, but they are summary inputs. Independent audit should
check their provenance or require raw time-series regeneration before using
this row as anything stronger than bounded support.

Other dependencies:

- [`C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md`](C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md)
  for the Convention C-iso temporal-step boundary.
- [`C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md`](C_ISO_SU3_NLO_CLOSURE_BOUNDED_NOTE_2026-05-08_su3nlo.md)
  for the SU(3) Wilson/heat-kernel single-plaquette correction machinery.
- [`EXACT_TIER_PATH_INTEGRAL_BOUNDED_NOTE_2026-05-07_exact.md`](EXACT_TIER_PATH_INTEGRAL_BOUNDED_NOTE_2026-05-07_exact.md)
  for the prior bounded W1 path-integral surface.
- [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
  for `g_bare = 1`.

Standard lattice-gauge references used for method context include
Cabibbo-Marinari, Drouffe-Zuber, Menotti-Onofri, Karsch, Klassen,
Kennedy-Pendleton, and the listed SU(3) thermodynamics benchmark papers.
They are method context, not repo-derived premises.

## Boundaries

This note does not claim:

- retained status, parent promotion, or C-iso theorem closure;
- a proof from the physical Cl(3) local algebra and Z^3 spatial substrate
  alone;
- raw reproduction of the L=8 and L=10 ensemble means;
- cross-xi universality of the combined estimator;
- direct Hamilton-form ED agreement.

The scientifically durable payload is the bounded arithmetic bridge:
given the imported volume-scan summaries and the cited C-iso correction
machinery, the xi=4 Weyl-truth corrected budget lands at
`2.6e-4`, while the xi=8 and xi=16 checks identify a multi-plaquette
large-xi obstruction.

## Audit Scope

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Bounded numerical support for C-iso engineering convergence at xi=4,
  conditional on imported finite-volume ensemble summaries and the cited
  C-iso source dependencies.
new_axiom_admission: false
audit_status_authority: independent audit lane only
effective_status_authority: pipeline-derived
raw_mc_regeneration_in_default_runner: false
```

## Falsifiers

- Recomputing the L=8 or L=10 ensembles from raw samples gives means outside
  the stated error bars.
- The SU(3) Weyl quadrature fails to stabilize under grid refinement at the
  beta values used here.
- A retained upstream result changes the C-iso correction machinery or the
  xi=4 operating point.
- A multi-plaquette correction at xi=4 is shown to be comparable to the
  declared `2.6e-4` budget.
