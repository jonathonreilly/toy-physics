# Koide Q two-point spectral-triple no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_two_point_spectral_triple_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Promote the retained charged-lepton `C_3` center to a finite two-point geometry.
The hoped-for route was:

```text
two-point Dirac metric / finite spectral action
  -> equal center-label state
  -> K_TL = 0
  -> Q = 2/3.
```

## Executable result

The runner verifies the retained real carrier split:

```text
rank(P_plus) = 1
rank(P_perp) = 2
```

For the abstract two-label spectral triple,

```text
D = [[0,m],[m,0]]
spec(D) = {-m,m}
d(plus,perp) = 1/m.
```

The metric scale `m` fixes distance between labels.  It does not fix the
central source state

```text
rho(u) = u P_plus + (1-u) P_perp/2.
```

The lifted state remains `C_3`-invariant for every `u`, with probabilities

```text
(p_plus,p_perp) = (u,1-u).
```

The neutral source state is the special point

```text
u = 1/2.
```

The retained Hilbert/rank state is still admissible:

```text
(1/3,2/3) -> Q = 1, K_TL = 3/8.
```

The equal-label state lands on the Koide leaf:

```text
(1/2,1/2) -> Q = 2/3, K_TL = 0.
```

But finite metric data do not choose between those states.

## Exchange escape hatch

An abstract exchange of the two labels would force

```text
u = 1/2.
```

That is not retained by the charged-lepton carrier: a rank-1 projector cannot
be conjugated to a rank-2 projector by an orthogonal/unitary map on the real
carrier.

## Residual

```text
RESIDUAL_SCALAR = center_label_state_u_minus_one_half_equiv_K_TL
RESIDUAL_STATE = finite_geometry_does_not_select_center_label_state
```

## Why this is not closure

Finite geometry adds useful metric data, but it does not derive the missing
state law.  Closure would need a retained reason that the physical central
state is the equal-label state, not the Hilbert/rank state or another central
state.

## Falsifiers

- A retained finite-geometry theorem whose spectral action varies with `u` and
  has a unique stationary point at `u=1/2`.
- A retained lift of the two-label exchange symmetry to the real `C_3` carrier.
- A physical state-selection principle tying the finite Dirac metric to
  `rho(u)` and proving `u=1/2`.

## Boundaries

- Covers two-label Connes distance, a polynomial spectral-action check, and the
  lift back to the retained rank-1/rank-2 carrier.
- Does not exclude a future finite-geometry model with extra retained dynamics
  for the central state.

## Hostile reviewer objections answered

- **"The two-point geometry has a natural exchange."**  Only after discarding
  the retained rank-1/rank-2 carrier.  The physical carrier does not retain that
  exchange.
- **"The spectral action could select the state."**  The checked finite action
  depends on Dirac eigenvalues and multiplicities, not on the source-state
  parameter `u`.
- **"Equal-label state is natural."**  It is admissible, but admissibility is
  not a derivation.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_two_point_spectral_triple_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_TWO_POINT_SPECTRAL_TRIPLE_NO_GO=TRUE
Q_TWO_POINT_SPECTRAL_TRIPLE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=center_label_state_u_minus_one_half_equiv_K_TL
RESIDUAL_STATE=finite_geometry_does_not_select_center_label_state
```
