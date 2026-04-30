# DM Neutrino Source-Surface Microscopic Positive-Probe Representation Theorem

**Date:** 2026-04-17  
**Status:** bounded - bounded or caveated result note
microscopic positive-probe grammar; not flagship closure  
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem.py`

## Question

Can the positive-probe candidate stack be compressed into one cleaner
representation theorem before any more recovered-carrier search?

## Bottom line

Yes.

On one common positive comparison window

`A_mu(H) = H + mu I > 0`,

let the exact singleton microscopic responses on

`dW_e^H = Schur_Ee(D_-)`

be

`w_P(H; mu) = W(A_mu(H); P)`

for trace-one rank-one positive probes `P = v v^*`.

Then:

1. if a family scalarization `S_F(H; mu)` preserves the exact family threshold
   witness event

   `S_F(H; mu) >= tau  <=>  exists P in F with w_P(H; mu) >= tau`

   for every threshold `tau`, it is forced pointwise to be

   `S_F(H; mu) = max_{P in F} w_P(H; mu)`;
2. if threshold units are intrinsic only up to strict monotone recalibration,
   then every admissible scalarization factors as

   `g(max_{P in F} w_P(H; mu))`

   with `g` strictly increasing;
3. passing to the full canonical family of all trace-one rank-one positive
   probes gives the exact extremal law

   `sup_P W(A_mu(H); P) = log(1 + 1 / lambda_min(A_mu(H)))`;
4. on the current recovered exact carrier, every lift has one negative soft
   mode, so this specializes to a strict monotone of

   `Lambda_+(H) = max(0, -lambda_min(H))`.

So the selector-class problem is now cleaner than the earlier candidate stack
made it look:

- the open item is no longer “which probe family / which weights / which
  scalarization?”;
- the open item is now:
  whether the true last-mile microscopic law is exhausted by this exact
  positive-probe threshold grammar, together with the separate exact-carrier
  completeness problem.

## Exact theorem shape

### 1. Family-threshold semantics force the pointwise maximum

Fix a finite family `F` of trace-one rank-one positive probes and one common
positive comparison window `A_mu(H)`.

For each threshold `tau`, the exact family witness event is

`exists P in F with w_P(H; mu) >= tau`.

If a scalar family score `S_F(H; mu)` is required to preserve those witness
events exactly, then the set of witnessed thresholds is the half-line

`(-infinity, max_{P in F} w_P(H; mu)]`,

so its endpoint is forced:

`S_F(H; mu) = max_{P in F} w_P(H; mu)`.

This is the top-down compression step that removes arbitrary weighted sums and
other list-dependent scalarizations from the theorem surface.

### 2. Monotone threshold recalibration leaves only reparameterization freedom

If threshold units are physically intrinsic only up to strict monotone
recalibration, then the only remaining scalar freedom is

`S_F(H; mu) = g(max_{P in F} w_P(H; mu))`

with `g` strictly increasing.

So once the exact witness semantics are fixed, there is no residual freedom in
the scalar selector beyond monotone reparameterization.

### 3. The canonical family collapses exactly to the soft mode

For the full canonical family

`F_can = {P = v v^* : ||v|| = 1}`,

the exact singleton response obeys the determinant-lemma / Rayleigh identity

`W(A_mu(H); v v^*) = log(1 + v^* A_mu(H)^(-1) v)`.

Therefore

`sup_P W(A_mu(H); P)`

is attained by the spectral projector onto the least eigendirection of
`A_mu(H)`, and the extremal score is

`log(1 + 1 / lambda_min(A_mu(H)))`.

So the canonical selector-class representative is not a fitted finite-family
sum.  It is the exact soft-mode extremal score of the full positive-probe
family.

### 4. Current recovered-carrier specialization

On the current recovered exact carrier, every lift still has one negative soft
mode, so

`lambda_min(A_mu(H)) = mu - Lambda_+(H)`.

Hence on that carrier the canonical extremal score is exactly

`log(1 + 1 / (mu - Lambda_+(H)))`,

which is a strict monotone of `Lambda_+`.

That is why the canonical extremal score, the least positive shift, and the
current preferred recovered point all already line up on the rebuilt branch.

## What this closes

This note closes the **selector-class representation** question at the right
level of abstraction.

The branch no longer needs to lead with:

- fitted finite probe families,
- arbitrary weight vectors,
- or competing scalarizations on the same exact positive-probe grammar.

Those routes become corollaries or discarded presentations of the same
selector-class law.

## What remains open

Two items remain open and should now be kept sharply separate:

1. **Observable-grammar exhaustion / intrinsic-family descent**
   whether the true last-mile selector on `dW_e^H = Schur_Ee(D_-)` is in fact
   exhausted by the exact positive-probe threshold grammar;
2. **Exact-carrier completeness / global dominance**
   whether the current recovered preferred point already dominates the full
   exact carrier, not merely the recovered carrier.

So the next theorem attack should not be “search more probe families.”
It should be:

- first, prove or obstruct observable-grammar exhaustion;
- second, prove or obstruct exact-carrier completeness / global dominance.

## Canonical validation

- [frontier_dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem.py](../scripts/frontier_dm_neutrino_source_surface_microscopic_positive_probe_representation_theorem.py)
- [DM_NEUTRINO_SOURCE_SURFACE_OBSERVABLE_GRAMMAR_EXHAUSTION_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_OBSERVABLE_GRAMMAR_EXHAUSTION_OBSTRUCTION_NOTE_2026-04-17.md)
- [DM_NEUTRINO_SOURCE_SURFACE_GLOBAL_DOMINANCE_COMPLETENESS_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_GLOBAL_DOMINANCE_COMPLETENESS_OBSTRUCTION_NOTE_2026-04-17.md)
