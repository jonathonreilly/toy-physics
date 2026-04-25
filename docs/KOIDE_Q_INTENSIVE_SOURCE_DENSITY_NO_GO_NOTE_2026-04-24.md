# Koide Q Intensive Source-Density No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_intensive_source_density_no_go.py`  
**Status:** conditional support theorem; executable no-go for retained closure

## Theorem Attempt

Maybe the physical charged-lepton source is intensive on the normalized
quotient components, not extensive over retained Hilbert rank.  If the source
assigns one density unit per quotient atom, then

```text
w_plus = w_perp = 1/2
K_TL = 0
Q = 2/3.
```

This would give the desired source-neutral law without using PDG masses,
observational pins, or a direct `Q=2/3` assumption.

## Brainstormed Variants

1. Source density is intensive per quotient component, so ranks `(1,2)` do not
   enter the source measure.
2. Source density is extensive per Hilbert microdimension, so ranks `(1,2)`
   produce weights `(1/3,2/3)`.
3. What if rank is only a carrier multiplicity, not a physical source
   observable?  Then the route collapses to the prior quotient-language
   invisibility theorem.
4. What if rank is physical source data?  Then the retained Hilbert/rank state
   is an exact countermodel.
5. What if intensivity is a variational principle?  The existing entropy,
   minimax, and Markov routes already leave the same center-weight scalar free
   unless a source law selects the quotient-label state.

Ranking:

```text
1. intensive quotient-component source: strongest conditional closure
2. rank invisibility / quotient-language factorization: already audited no-go
3. variational intensivity: already reduces to center prior choice
4. Hilbert rank-extensive source: retained counterstate
5. arbitrary density ratio: exposes the residual scalar only
```

## Exact Audit

Let `rho_plus,rho_perp` be source densities per quotient component.  The
normalized component weights are

```text
w_plus = rho_plus / (rho_plus + rho_perp)
w_perp = rho_perp / (rho_plus + rho_perp).
```

The runner verifies exactly:

```text
K_TL = 0 <=> rho_plus = rho_perp.
```

Under equal intensive density,

```text
w = (1/2, 1/2)
K_TL = 0
Q = 2/3.
```

This is a valid conditional theorem.

## Retained Counterstate

The retained package also contains the Hilbert ranks

```text
rank(P_plus) = 1
rank(P_perp) = 2.
```

Equal density per Hilbert microdimension gives the rank-extensive state

```text
w = (1/3, 2/3)
Q = 1
K_TL = 3/8.
```

More generally, for extensive densities `sigma_plus,sigma_perp`,

```text
w_plus = sigma_plus / (sigma_plus + 2 sigma_perp)
w_perp = 2 sigma_perp / (sigma_plus + 2 sigma_perp)
K_TL = 0 <=> sigma_plus = 2 sigma_perp.
```

So closure requires the inverse-rank density choice, not an equation already
supplied by the retained structure.

## Musk Simplification Pass

1. Make requirements less wrong: the issue is not `Q`; it is the source
   dimension convention.
2. Delete: all higher carrier machinery reduces here to the rank pair `(1,2)`.
3. Simplify: one convention scalar interpolates label-counting and rank
   weighting.
4. Accelerate: the decisive test is whether retained equations set that scalar
   to the intensive endpoint.
5. Automate: add the scalar to the residual atlas and source-class exhaustion
   runner.

## Hostile Review

This route must be rejected as a retained closure.  The intensive law is not
derived from retained `Cl(3)/Z3` data; it selects the equal quotient-label
source state over the retained Hilbert/rank-extensive state.  Promoting it
would rename the missing primitive:

```text
derive_intensive_component_source_over_rank_extensive_source.
```

No forbidden input is used, but no positive Koide closure is obtained.

## Verdict

```text
KOIDE_Q_INTENSIVE_SOURCE_DENSITY_NO_GO=TRUE
Q_INTENSIVE_SOURCE_DENSITY_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_INTENSIVE_COMPONENT_SOURCE=TRUE
RESIDUAL_SCALAR=derive_intensive_component_source_over_rank_extensive_source
RESIDUAL_Q=rank_extensive_source_state_not_excluded
COUNTERSTATE=rank_extensive_w_plus_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_intensive_source_density_no_go.py
python3 -m py_compile scripts/frontier_koide_q_intensive_source_density_no_go.py
```
