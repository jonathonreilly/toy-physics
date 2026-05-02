# Teleportation Unconditional-Closure Attack Note

**Date:** 2026-04-26
**Status:** planning / theorem-premise sharpening; not promoted
**Runner:** `scripts/frontier_teleportation_unconditional_closure_attack.py`

## Scope

This artifact attacks the remaining nature-grade blockers after the open-item
pass:

- derive the bridge principles from the original sole axiom;
- turn the finite side `4,6,8,10` resource fit into a theorem;
- replace pulse/detector proxies with material or continuum implementations.

The result is deliberately mixed. It sharpens the theorem premises, but it does
not close the lane unconditionally.

The scope remains ordinary quantum state teleportation only. No matter, mass,
charge, energy, object, or faster-than-light transport is claimed.

## Bare One-Axiom Underdetermination

The single-axiom framework surface gives local Hilbert structure and
local-Hermitian conserved flow. That is enough to host the protocol, but it is
not enough to select a unique apparatus or amplitude law.

The runner exhibits a finite witness family:

```text
transducers = 8
carriers = 4
equivalent_pairs = 32
selection_entropy_bits = 5.000000
```

All witnesses are treated as local Hermitian flows and share the audited
protocol observables. Therefore the original bare one-axiom surface remains
underdetermined for this lane. A selector must either be derived from a stronger
retained framework theorem or retained as an added variational completion.

## Minimal Variational Completion

The minimal completion that selects the current bridge principles is:

```text
1. retarded causal-positive orientation;
2. minimal generator/action norm over equivalent Bell-record writers;
3. no-dwell cubic-covariant nearest-neighbor carrier.
```

Default result:

```text
selected_winding = 0
angle = 1.570796
action_gap = 19.739209
selected_center = 0.000
neighbor_weight = 0.408248
dwell_gap = 0.015625
extra_completion_required = True
```

This is not a derivation from the bare single axiom. It is a minimal sufficient
completion candidate.

## Conditional Sparse-Resource Theorem

The side `4,6,8,10` signed sparse rows satisfy a conservative finite certificate:

```text
side=4:  gap*L^2 = 0.390440, Bell*=0.999702
side=6:  gap*L^2 = 0.434225, Bell*=0.999709
side=8:  gap*L^2 = 0.450979, Bell*=0.999711
side=10: gap*L^2 = 0.459031, Bell*=0.999711
```

The theorem schema is:

```text
If for all even L >= 4:
  gap(L) >= 0.380 / L^2
  Bell*(L) >= 0.999702
then adiabatic/cooling preparation has polynomial bounds:
  T_ad(L, eps) <= L^4 / 0.380^2 * log(1/eps)
  beta(L, eps) <= L^2 / 0.380 * log((L^6 - 1)/eps)
```

The audited side-10 bounds at `eps=1e-3` are:

```text
side10_Tadiabatic_bound = 4.784e+05
side10_beta_bound = 5.453e+03
```

This turns the finite fit into a precise conditional theorem. The missing
piece is the asymptotic proof of the gap floor and Bell-overlap floor.

## Pulse Threshold Class

The record code has length `8`, minimum Hamming distance `5`, and corrects up to
two arbitrary slot flips. For the correlated pulse model from the previous
artifact:

```text
max_slot_error = 5.631e-04
union_word_failure_bound = 9.978e-09
exact_worst_observed = 1.449e-11
target = 1.000e-06
slot_threshold = 2.622e-03
```

The union-bound theorem is weaker than the exact decoder result, but it is a
controller-independent threshold class: any hardware whose worst conditional
slot error is below `2.622e-03` passes the `1e-6` word-failure target under the
bounded-flip model.

## Thermodynamic Ising Detector Class

The finite detector proxy is promoted to a thermodynamic class. For odd domain
side `L`, each record slot is a 3D Ising majority domain with `L^3` spins.
Below the flip threshold `p < 1/2`, the majority failure is bounded by a KL
large-deviation tail:

```text
P_majority <= exp(-L^3 D(1/2 || p)).
```

At the audited point:

```text
domain_side = 5
spins_per_slot = 125
p_spin = 2.006e-03
KL_majority_bound = 9.373e-132
word_failure_bound = 7.498e-131
log10_overlap_bound = -655.141
arrhenius_wall = 1.929e-22
decay = word~exp(-Theta(L^3)), wall~exp(-Theta(L^2))
```

This is a continuum/thermodynamic detector class, not a named laboratory
material.

## Retained Status

The remaining blockers are now more precise:

- bare one-axiom derivation is blocked by an explicit underdetermination
  witness unless the variational completion is derived or retained;
- sparse-resource asymptotics reduce to proving `gap(L) >= 0.380/L^2` and
  `Bell*(L) >= 0.999702` for the signed branch;
- hardware closure reduces to realizing the pulse slot-threshold class and the
  Ising-domain detector class in an actual material/controller model.

The lane remains planning / conditional theory, not unconditional nature-grade
closure.
