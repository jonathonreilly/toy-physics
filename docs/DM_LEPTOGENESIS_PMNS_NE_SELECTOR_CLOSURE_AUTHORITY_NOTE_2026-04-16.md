# DM Leptogenesis PMNS `N_e` Selector Closure Authority

**Date:** 2026-04-16  
**Status:** canonical authority surface for the exact reduced-domain
PMNS-assisted `N_e` selector lane on the current branch  
**Scope:** freeze the live selector claim boundary without touching the atlas

## Question

What is the strongest exact branch claim we should now treat as the live
authority surface for the PMNS-assisted charged-lepton-active `N_e` selector
lane?

## Bottom line

The live authority claim is now:

> on the exact reduced `N_e` domain, the PMNS-assisted selector lane has an
> exact real-slice reduction, anchor-free reduced-chart stationary recovery,
> selector coincidence, and a strict-real-slice intrinsic-class certificate.
> The physical branch is the unique low-action / maximum-dominance-gap /
> minimum-spill branch on the current exact reduced stationary set.

This is materially stronger than the earlier "support-only" wording.

What is still not claimed here:

- a pure-retained neutrino closure on this lane
- an observation-free normalization/value law removing the closure condition
  `eta / eta_obs = 1`
- a fully validated interval-arithmetic proof over every point of the reduced
  closure manifold

So the live residual issue is now certification style, not unresolved PMNS
branch physics.

## Authority stack

This authority surface is the conjunction of six exact pieces.

### 1. Exact reduced domain

The admissible PMNS-assisted closure problem already factors exactly through
the fixed native `N_e` seed surface. There is no separate physical component
outside that reduced domain for this selector problem.

Authority:

- [DM_LEPTOGENESIS_PMNS_REDUCTION_EXHAUSTION_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_REDUCTION_EXHAUSTION_THEOREM_NOTE_2026-04-16.md)
- [frontier_dm_leptogenesis_pmns_reduction_exhaustion_theorem.py](../scripts/frontier_dm_leptogenesis_pmns_reduction_exhaustion_theorem.py)

### 2. Exact analytic stationary reduction

On that exact reduced domain, the charged Hermitian block is explicit, the
selector problem is even under `delta -> -delta`, and the stationary
classification reduces to the real slice as an exact KKT problem.

Authority:

- [DM_LEPTOGENESIS_PMNS_ANALYTIC_STATIONARY_CLASSIFICATION_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_ANALYTIC_STATIONARY_CLASSIFICATION_THEOREM_NOTE_2026-04-16.md)
- [frontier_dm_leptogenesis_pmns_analytic_stationary_classification_theorem.py](../scripts/frontier_dm_leptogenesis_pmns_analytic_stationary_classification_theorem.py)

### 3. Exact phase competition reduction

At fixed positive reduced coordinates, the observable-relative action is
strictly decreasing in `cos(delta)`. So the physically relevant competition is
forced onto the real slice `delta = 0`.

Authority:

- [DM_LEPTOGENESIS_PMNS_ACTION_PHASE_REDUCTION_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_ACTION_PHASE_REDUCTION_THEOREM_NOTE_2026-04-16.md)
- [frontier_dm_leptogenesis_pmns_action_phase_reduction_theorem.py](../scripts/frontier_dm_leptogenesis_pmns_action_phase_reduction_theorem.py)

### 4. Anchor-free reduced-chart branch recovery

On the strict reduced chart, an anchor-free compact-cover search plus local
polishing recovers the same three stationary closure branches with the same
low branch, the same finite gap `Delta S = 0.001812373907`, and the same
positive tangent Hessian at the low branch.

Authority:

- [DM_LEPTOGENESIS_PMNS_REDUCED_SURFACE_SELECTOR_SUPPORT_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_REDUCED_SURFACE_SELECTOR_SUPPORT_NOTE_2026-04-16.md)
- [frontier_dm_leptogenesis_pmns_reduced_surface_selector_support.py](../scripts/frontier_dm_leptogenesis_pmns_reduced_surface_selector_support.py)

### 5. Exact selector coincidence

On the exact reduced stationary set, the observable-relative-action selector
and the packet-level physical selector coincide:

- observable selector: low branch
- maximum-dominance-gap selector: low branch
- minimum-spill selector: low branch

So branch identity is no longer ambiguous on the recovered stationary set.

Authority:

- [DM_LEPTOGENESIS_PMNS_SELECTOR_COINCIDENCE_THEOREM_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_SELECTOR_COINCIDENCE_THEOREM_NOTE_2026-04-16.md)
- [frontier_dm_leptogenesis_pmns_selector_coincidence_theorem.py](../scripts/frontier_dm_leptogenesis_pmns_selector_coincidence_theorem.py)

### 6. Strict-real-slice intrinsic classes

On the strict real slice:

- `low` and `high` are locally stable interval classes
- the nearby `mid` chart is not its own strict-real class and collapses back
  into `low` under local real-slice probing

So the real reduced chart does not carry a diffuse family of equally live
physical branches.

Authority:

- [DM_LEPTOGENESIS_PMNS_REAL_SLICE_INTRINSIC_CLASS_CERTIFICATE_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_REAL_SLICE_INTRINSIC_CLASS_CERTIFICATE_NOTE_2026-04-16.md)
- [frontier_dm_leptogenesis_pmns_real_slice_intrinsic_class_certificate.py](../scripts/frontier_dm_leptogenesis_pmns_real_slice_intrinsic_class_certificate.py)

## Exact live claim boundary

This authority surface does claim:

- the reduced `N_e` selector problem has one exact admissible domain
- the physical competition reduces exactly to the real slice
- the same low branch is recovered by the internal effective-action selector
  and the external packet selector
- the nearby middle branch is not an equally live strict-real competitor

This authority surface does not yet claim:

- a symbolic elimination of every closure point over the full reduced manifold
  without any computational certification layer
- an observation-free normalization/value law replacing the closure condition
  `eta / eta_obs = 1`

So the safe current branch wording is:

> exact reduced-domain PMNS-assisted `N_e` selector closure with real-slice
> phase reduction, anchor-free reduced-chart branch recovery, selector
> coincidence, and strict-real-slice intrinsic-class certification.

## Verification bundle

The canonical verification bundle for this authority surface is:

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_reduction_exhaustion_theorem.py
python3 scripts/frontier_dm_leptogenesis_pmns_analytic_stationary_classification_theorem.py
python3 scripts/frontier_dm_leptogenesis_pmns_action_phase_reduction_theorem.py
python3 scripts/frontier_dm_leptogenesis_pmns_reduced_surface_selector_support.py
python3 scripts/frontier_dm_leptogenesis_pmns_selector_coincidence_theorem.py
python3 scripts/frontier_dm_leptogenesis_pmns_real_slice_intrinsic_class_certificate.py
```

On the current branch, all six runners pass.

## Consequence

This note supersedes older branch wording that described the PMNS-assisted
selector lane as merely "support" or "not yet promoted" in a general sense.

What remains open is narrower:

- the observation-free normalization/value law
- the final style upgrade from current exact real-slice / reduced-chart
  certification to a fully validated interval-global certificate
