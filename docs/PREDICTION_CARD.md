# Prediction & Falsification Card

**Date:** 2026-04-01
**Purpose:** State what would falsify the model's claims and what
toy-level signatures distinguish this architecture from simpler baselines.

## What the model predicts

### P1. Gravity is a pure phase effect
**Prediction:** gravitational deflection vanishes exactly at k=0.
**Test:** set k=0 and measure centroid shift.
**Status:** CONFIRMED — delta = 0.000000e+00 at k=0 across all
tested dimensions (2D, 3D, 4D) and graph families.

### P2. Mass scaling increases with spatial dimension
**Prediction:** higher spatial dimension → stronger mass dependence.
**Test:** measure alpha (shift ~ M^alpha) at matched parameters across d=1,2,3.
**Status:** CONFIRMED in 3D (alpha converges to ~0.58). 4D shows
positive mass scaling but doesn't converge to a universal exponent.

### P3. Decoherence requires slit distinguishability in the bath
**Prediction:** CL bath decoherence scales with bin-resolved contrast S_norm.
If S_norm → 0, decoherence vanishes regardless of coupling strength lambda.
**Test:** measure S_norm vs N. If S_norm stays bounded, decoherence persists.
**Status:** CONFIRMED in 3D (S_norm bounded 0.07-0.30 through N=100).

### P4. Born rule holds for linear path-sum with chokepoint barrier
**Prediction:** I_3/P = 0 to machine precision when no paths bypass the barrier.
**Test:** three-slit Sorkin test on chokepoint DAGs.
**Status:** CONFIRMED (I_3/P = 3e-16).

### P5. Cross-family gravity
**Prediction:** gravity works on any sufficiently connected causal DAG,
not just modular. The corrected propagator is the mechanism, not the topology.
**Test:** measure gravity on hierarchical, uniform, and preferential DAGs.
**Status:** CONFIRMED on 4 of 5 families. Preferential attachment fails
(hub concentration disrupts amplitude distribution).

## What would falsify the model

### F1. Gravity at k=0
If gravitational deflection appeared at k=0 (no phase), the mechanism
would not be a phase effect — it would be a trivial amplitude bias.
This was tested and passed, but any future architecture modification
must re-check k=0.

### F2. Born rule violation on chokepoint graphs
If I_3/P > 1e-6 on a graph where all paths pass through the barrier,
the linear path-sum model would have genuine higher-order interference.
This has never been observed and would require revising the propagator.

### F3. Decoherence without mass/environment
If CL bath purity dropped below 1.0 on a flat field (no mass nodes),
the decoherence would be a graph geometry artifact, not a mass-mediated
environment effect. This has never been observed.

### F4. Gravity reversal at large N
If the sign of gravitational deflection flipped from attraction to
repulsion at large N (without changing k or the propagator), the phase
valley mechanism would be unstable. The current data shows stable
attraction through N=100 on 3D modular DAGs.

### F5. Mass scaling reversal with dimension
If adding spatial dimensions reduced alpha (weaker mass scaling), the
dimensional progression would be broken. Currently alpha increases
monotonically: ~0 (2D) → ~0.58 (3D) → positive but parameter-sensitive (4D).

## What distinguishes this model from simpler baselines

### D1. Phase valley vs amplitude routing
The k=0 diagnostic separates phase-mediated gravity from trivial
conductance bias. Edge reweighting (1+alpha*f)^gamma gives 1/b
distance falloff BUT the same falloff appears at k=0 — proving it's
amplitude routing, not gravity. The phase valley mechanism produces
b-independent gravity that requires k > 0.

### D2. CL bath vs structural decoherence
The CL bath decoherence is genuine environment-mediated (partial trace
over bin-resolved bath). A simpler model (e.g., dephasing from random
phases) would not show the bin-structure dependence or the scaling
with lambda. The CL bath specifically requires S_norm > 0 (slit
distinguishability in the spatial bins).

### D3. Emergent gap vs imposed gap
The adaptive quantile pruning creates emergent gap structure from
uniform DAGs, improving decoherence by 5pp at N=30 and sustaining
through N=60. A simpler model with no self-regulation would not
show this dynamic gap formation.

### D4. Dimensional dependence
The mass scaling exponent depends on spatial dimension (0 → 0.58 → positive).
A simpler model (e.g., random phase accumulation without geometric structure)
would not show this dimensional progression.

### F6. Lattice gravity reversal under refinement (2026-04-04)
If the 3D 1/L^2 gravitational TOWARD flipped back to AWAY at h < 0.125,
the convergence claim would be falsified. Current data: TOWARD at h=0.5,
0.25, 0.125, strengthening at each step. A reversal below h=0.125 would
indicate the TOWARD was another (finer) lattice artifact.

### F7. Distance exponent stops steepening (2026-04-04)
If the distance-law tail exponent plateaus (e.g., stays at -0.53
at h=0.125 and h=0.0625), the model does NOT produce Newtonian gravity
in the continuum limit. Currently: -0.35 (h=0.5) → -0.53 (h=0.25).
If it flattens, the asymptotic exponent is not -2.

### F8. 4D 1/L^3 gravity fails at longer lattice (2026-04-04)
At L=15 on 4D, 1/L^3 gives +0.034 (TOWARD, strengthening). If at
L=20 or L=25 it flips to AWAY, the dimension-dependent kernel pattern
breaks for d=4. Currently the pattern holds for d=2,3,4.

## What distinguishes this model from simpler baselines

### D1. Phase valley vs amplitude routing
The k=0 diagnostic separates phase-mediated gravity from trivial
conductance bias. Edge reweighting (1+alpha*f)^gamma gives 1/b
distance falloff BUT the same falloff appears at k=0 — proving it's
amplitude routing, not gravity. The phase valley mechanism produces
b-independent gravity that requires k > 0.

### D2. CL bath vs structural decoherence
The CL bath decoherence is genuine environment-mediated (partial trace
over bin-resolved bath). A simpler model (e.g., dephasing from random
phases) would not show the bin-structure dependence or the scaling
with lambda. The CL bath specifically requires S_norm > 0 (slit
distinguishability in the spatial bins).

### D3. Emergent gap vs imposed gap
The adaptive quantile pruning creates emergent gap structure from
uniform DAGs, improving decoherence by 5pp at N=30 and sustaining
through N=60. A simpler model with no self-regulation would not
show this dynamic gap formation.

### D4. Dimensional dependence
The mass scaling exponent depends on spatial dimension (0 → 0.58 → positive).
A simpler model (e.g., random phase accumulation without geometric structure)
would not show this dimensional progression.

### D5. Kernel dimension-dependence (2026-04-04)
The unique persistent kernel power p=d-1 across 2D/3D/4D is a
non-trivial pattern. A simpler model (fixed kernel independent of
dimension) would not show this. The transfer norm analysis reveals
p=d-1 is the logarithmically marginal boundary — not an arbitrary
choice but the unique admissible scaling.

## Open predictions (untested)

### O1. 4D continuum limit
If 4D alpha converges at higher density (npl > 80), it should settle
between 0.7 and 1.2 based on the current trajectory. If it diverges,
the 4D mass scaling is not well-defined.

### O2. Hub-disruption threshold
Preferential attachment breaks gravity when hub_boost > some threshold.
Prediction: the threshold depends on the ratio of hub degree to mean
degree. If hub_degree / mean_degree > ~5, gravity should fail.

### O3. Decoherence on preferential DAGs
The cross-family test showed decoherence works on preferential DAGs
even when gravity fails. Prediction: decoherence is more robust than
gravity across graph families because it depends on slit distinguishability
(geometric), not phase valley coherence (interference).

### O4. 5D kernel prediction (2026-04-04)
On a 5D lattice (4 transverse dims), the correct kernel should be
1/L^4. Prediction: 1/L^3 will be TOWARD but weakening with L on 5D,
while 1/L^4 will strengthen. Born should hold at machine precision.

### O5. Distance exponent convergence rate (2026-04-04)
On the 3D 1/L^2 lattice, the distance tail exponent at h=0.125 should
be between -0.60 and -0.75 (extrapolating the -0.35 → -0.53 trend).
If it is shallower than -0.45 or steeper than -1.0, the convergence
rate model is wrong.

### O6. RG exponent universality (2026-04-04)
The RG scaling s ~ h^0.92 was measured on the 3D lattice. On the 4D
lattice, a different RG exponent is expected (the per-layer amplitude
transfer scales differently). Prediction: 4D RG exponent > 0.92.
