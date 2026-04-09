# Derivation: Geometric vs Dispersive Deflection

## Date
2026-04-09

## Target Behavior
When a persistent pattern (mass source) alters the local delay
landscape, does the deflection of a test pattern depend on the
test pattern's continuation-weight wavenumber k?

Observed: the deflection oscillates between TOWARD and AWAY as k
varies (k-sweep on retained 2+1D and 3+1D lattices). Spectral
averaging over k gives net AWAY on the retained harness.

Question: does the axiom chain PREDICT this k-dependence, or does
it predict k-independent (geometric) deflection?

## Axioms Used

- Axiom 1: Reality is an evolving network of events and links.
- Axiom 3: Space is inferred from signal-delay structure.
- Axiom 4: Duration is local update count.
- Axiom 6: Free systems follow the locally simplest continuation.
- Axiom 7: Inertia is undisturbed natural continuation.
- Axiom 8: Gravity is natural continuation in a DISTORTED
           continuation structure.

## Minimal Example

Consider a 5-node network:

    A ---1--- B ---1--- D
               \       /
                1     1
                 \   /
                  C
                  |
                  M (persistent pattern = mass)

Nodes A, B, C, D are events. M is a persistent pattern that
alters the delay on link B-C (increases it to 1+f where f > 0).

Two paths from A to D:
  Path 1: A → B → D (total delay = 2, no field)
  Path 2: A → B → C → D (total delay = 2 + f, passes near mass)

## Derivation

### Step 1: Axiom 8 says gravity IS the continuation structure

Axiom 8 does NOT say "gravity is the phase-weighted deflection
of a wave pattern." It says gravity is "natural continuation in a
distorted continuation structure." The continuation structure is
the DELAY LANDSCAPE — the set of delays on all links.

The persistent pattern M distorts the delay on link B-C from 1 to
1+f. This distortion IS the gravitational effect, by axiom.

### Step 2: The continuation structure is k-independent

The delay landscape {delay(link)} is a property of the NETWORK,
not of any test pattern propagating through it. The delay on link
B-C is 1+f regardless of what passes through it. Any pattern
following the "locally simplest admissible continuation" (Axiom 6)
through this landscape encounters the same delays.

Therefore: the distorted continuation structure is k-independent.
If gravity IS this structure (Axiom 8), then gravity is
k-independent.

### Step 3: Where does k-dependence enter?

The model's implementation adds a SEPARATE mechanism on top of the
continuation structure: a path-sum with amplitude weights:

  amplitude(path) = product of exp(i*k*S_edge) * w(theta) / L^p

The wavenumber k determines the PHASE ACCUMULATION per unit action.
Different k values accumulate different phases along the same path,
leading to different interference patterns at the detector.

This phase accumulation is NOT part of the continuation structure.
It is a wave-propagation mechanism layered on top of the structure.
The continuation structure (delays, topology) is the same for all k.

### Step 4: The model conflates two mechanisms

The current implementation conflates:

(a) The CONTINUATION STRUCTURE: delays, topology, connectivity.
    This is k-independent. Axiom 8 says this IS gravity.

(b) The WAVE PROPAGATION: phase accumulation, interference, Born
    rule. This is k-dependent. This is the path-sum mechanism.

The deflection measured in all experiments is the WAVE deflection —
the centroid of |sum_paths amplitude(path)|^2 at the detector.
This is k-dependent because it involves interference.

But the GEOMETRIC deflection — the shift in the minimum-delay path
(geodesic) — is k-independent because it depends only on the
continuation structure.

### Step 5: What the axioms predict

From the axioms alone:

- Axiom 8 predicts k-INDEPENDENT deflection (gravity is the
  continuation structure, which doesn't involve k).

- The path-sum implementation adds k-DEPENDENT wave corrections
  on top of the geometric baseline.

The k-dependent resonance is REAL but it is NOT gravity in the
sense of Axiom 8. It is a wave-interference effect in a path-sum
propagating through a gravitationally distorted network.

### Step 6: The geometric baseline exists but was never measured

The minimum-delay path (geodesic) through the distorted network
curves toward the mass source because delays are longer near mass
(f > 0 → delay = L*(1+f) > L). By Axiom 6, the "locally simplest
continuation" avoids the high-delay region — but the GRADIENT of
the delay field creates a net transverse deflection.

Wait — this needs careful analysis. If delays are LONGER near mass,
the shortest path AVOIDS mass. This gives geodesic deflection AWAY
from mass, not toward it.

In the model's implementation, the valley-linear action S = L*(1-f)
DECREASES action near mass, creating a phase valley that deflects
the WAVE toward mass. But the DELAY landscape has delays that
INCREASE near mass, deflecting GEODESICS away from mass.

This is a fundamental tension:
  - Geodesics (delay-based): AWAY from mass (delays increase near mass)
  - Wave deflection (phase-based): TOWARD mass in attractive k-window
    (action decreases near mass)

### Step 7: Resolution — what does Axiom 8 actually mean?

Axiom 8 says gravity is "path selection through a locally altered
delay/load landscape." The word "delay" suggests the geodesic
(delay-based) mechanism. But the word "load" is more ambiguous —
it could include action-like quantities.

If "continuation structure" means the DELAY landscape:
  → Geodesics bend AWAY from mass (longer delays near mass)
  → This is NOT gravitational attraction
  → The TOWARD deflection at k=5 is a wave resonance, not gravity

If "continuation structure" means the ACTION landscape:
  → The action S = L(1-f) is SMALLER near mass
  → Geodesics of the action (minimum-action paths) bend TOWARD mass
  → But action-geodesics are phase-dependent (the stationary-phase
    condition involves k), so they are NOT k-independent

Neither interpretation gives k-independent TOWARD deflection.

## Novel Prediction

IF the derivation in Step 6 is correct (geodesics bend AWAY from
mass on the delay landscape), then:

**Prediction: The arrival-time gradient at the detector should point
AWAY from mass, not toward it.**

Specifically: on the retained 3D lattice with a mass source at z=3,
the Dijkstra shortest-path arrival time at detector position z=4
should be LATER (not earlier) than at z=2. The mass makes the
near-mass region slower, pushing the shortest path away.

This is testable with the existing infer_arrival_times function.

If confirmed: the model's "gravity" is purely a wave-resonance
effect with no geometric (geodesic) basis. The TOWARD deflection
exists only for specific k values, is dispersive, and the geometric
baseline is AWAY.

If falsified (geodesics bend TOWARD): there is a mechanism in the
delay landscape that I'm missing, and the geometric gravity
interpretation may be salvageable.

## Weakest Link

Step 6: the claim that longer delays near mass push geodesics AWAY.
This assumes the shortest path minimizes total delay. On a lattice
with discrete topology, the shortest path might curve toward mass
if the mass region has HIGHER CONNECTIVITY (more edges, shorter
alternative paths) despite longer individual delays.

The test: compute Dijkstra arrival times with and without mass on
the retained 3D lattice and check the transverse gradient.

## Status
PROPOSED — the arrival-time gradient test is the decisive experiment.
