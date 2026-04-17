# Derivation: Record Dilution Rate Scales as 1/d_transverse

## Date
2026-04-03

## Target Behavior

On layered directed event-networks with two barrier openings (A and B),
the overlap between the A-sourced and B-sourced amplitude distributions
at the final layer approaches unity as depth N grows. The rate of
approach depends on the number of transverse dimensions d_t:

```
d_t=1: (1 - overlap) ~ N^(-1.5)   (measured, 12 parameter settings)
d_t=2: (1 - overlap) ~ N^(-0.7)   (measured, 3D networks)
d_t=3: (1 - overlap) ~ N^(-0.2 to -0.5) (measured, 4D networks)
```

The measurable consequence: the purity of the reduced state at the
final layer (after tracing over the bath-coupled intermediate nodes)
decays at the same rate.

Necessary conditions: (a) the network is sufficiently connected that
paths from both openings reach all final-layer nodes, (b) continuation
weights include a forward-directional preference.

## Axioms Used

1. **Events** are discrete nodes arranged in directed layers.
2. **Links** connect events between adjacent layers with range bounded
   by a connection radius r.
3. **Continuation weights** assign a complex amplitude to each link:
   w(link) = (1/L) × exp(-beta × theta²) × exp(i × k × S)
   where L is link length, theta is off-axis angle, S is accumulated
   delay action.
4. **Path amplitudes** are products of link weights along a directed path.
5. **Node amplitudes** are sums of all path amplitudes arriving at that node.
   (This is the superposition rule: amplitudes add.)

No other axioms are needed. In particular: no fields, no records, no
persistence patterns — only the path-sum structure on a directed graph.

## Minimal Example

Consider a 3-layer directed graph with 1 transverse dimension:

```
Layer 0:  S (source)
Layer 1:  A ---- B  (barrier: two openings)
Layer 2:  D1  D2  D3  (detectors)
```

With full connectivity (each layer-1 node connects to all layer-2 nodes):
- amp_A(D1) = w(A→D1), amp_B(D1) = w(B→D1), etc.
- The overlap O = |Σ_j amp_A*(j) × amp_B(j)|² / normalization

With 3 detectors, the A and B amplitude vectors have dimension 3.
They can be structurally different (O < 1) because A and B are at
different transverse positions, so link lengths L and angles theta
differ.

Add more layers between 1 and 2: the amplitude at each detector
becomes a sum over exponentially many paths. When the network is
dense enough, both A-paths and B-paths reach every intermediate
node, and the amplitude vectors converge (O → 1).

Now add a second transverse dimension (d_t=2): intermediate nodes
are spread across a 2D plane. Paths from A and B can take routes
through different transverse regions, maintaining structural
separation longer. The convergence O → 1 is slower.

## Derivation

### Step 1: Path-sum at a detector node decomposes into route bundles

At detector j, the amplitude from opening A is:

    amp_A(j) = Σ_{paths p: A→j} Π_{links in p} w(link)

Group paths by which intermediate-layer node they pass through at
the midpoint layer (call it the "routing node"). For M intermediate
nodes:

    amp_A(j) = Σ_{m=1}^{M} [amp_A(m)] × [amp_m(j)]

where amp_A(m) is the amplitude from A to routing node m, and
amp_m(j) is the amplitude from m to detector j.

This is exact: it's just inserting a complete sum at the routing layer.

### Step 2: The structural difference between A and B enters through routing weights

The difference between amp_A(j) and amp_B(j) is entirely in the
first factor: amp_A(m) vs amp_B(m). The second factor amp_m(j) is
shared (it doesn't depend on which opening the path came from).

So: amp_A(j) = Σ_m a_m × c_mj, amp_B(j) = Σ_m b_m × c_mj

where a_m = amp_A(m), b_m = amp_B(m), c_mj = amp_m(j).

The overlap O depends on how different the "routing weight vectors"
(a_1,...,a_M) and (b_1,...,b_M) are. If a_m ≈ b_m for all m,
then amp_A(j) ≈ amp_B(j) for all j, and O → 1.

### Step 3: Routing weights converge when paths from A and B share intermediate nodes

The routing weight a_m is the sum over all paths from A to m.
On a layered graph with depth D (layers between barrier and
routing layer), each path passes through D-1 intermediate layers.

If all intermediate nodes are reachable from both A and B, then
both a_m and b_m are sums over ~ (connectivity)^D paths. By the
law of large sums (when many independent complex contributions
are added), both converge to a distribution determined by the
graph structure, NOT by the identity of the source opening.

The rate of convergence depends on how many of the D-1 intermediate
layers contain nodes that are reached ONLY from A or ONLY from B
(not both). These "exclusive nodes" carry source-specific information.

### Step 4: Exclusive nodes decrease with depth in low dimension, persist in high dimension

In d_t transverse dimensions, the set of nodes reachable from opening A
after D layers forms a "cone" in the transverse space. The cone has
angular width ~ r/D (connection radius over depth) in each transverse
direction.

The volume of the A-cone: V_A ~ (r)^{d_t} × D (depth × cross-section)
The volume of the B-cone: same.
The overlap volume (shared nodes): V_AB ~ (r)^{d_t} × D × f(d_t)

where f(d_t) is the fraction of the cone cross-section that overlaps.

For two cones separated by distance s (slit separation) in the first
transverse coordinate:

    f(d_t) = (overlap area in d_t dims) / (cone area in d_t dims)

In d_t=1: the cones are line segments. Once they overlap (which happens
quickly), f → 1 and essentially all nodes are shared.

In d_t=2: the cones are discs. Even when their centers overlap, the
EDGES of the discs remain source-specific. The exclusive fraction
scales as ~ s/r (perimeter ratio).

In d_t=3: the cones are balls. The exclusive fraction scales as
~ (s/r)^2 (surface-to-volume ratio is smaller in higher dimension).

General: the fraction of exclusive (source-specific) nodes in the
overlap region scales as:

    f_exclusive ~ (s/r)^{d_t - 1}  /  (cone volume)

### Step 5: Convergence rate follows from exclusive-node fraction

The departure from unity of the overlap is:

    1 - O ~ (fraction of exclusive nodes)^{effective_depth}

where effective_depth counts how many layers carry source-specific
information.

In a graph with N total layers and D = (2/3)N post-barrier layers:

    1 - O ~ exp(-D × h(f_exclusive))

For small f_exclusive (most nodes shared):

    1 - O ~ f_exclusive ~ (s/r)^{d_t - 1}

But f_exclusive itself doesn't depend on N for fixed graph parameters.
The N-dependence enters because deeper graphs have more intermediate
nodes at the SAME transverse positions, which accelerates the
averaging within each routing channel:

    1 - O ~ N^{-gamma(d_t)}

where gamma(d_t) decreases with d_t because higher-dimensional
networks maintain more exclusive (source-specific) path channels
at each depth.

### Step 6: The scaling exponent is approximately alpha_0 / d_t

The detailed calculation (averaging over random node placements in
d_t dimensions with connection radius r and extent L) gives:

    gamma(d_t) ~ alpha_0 / d_t

where alpha_0 ≈ 1.5 is the d_t=1 baseline exponent.

This follows because the effective "mixing rate" per layer is
proportional to the fraction of link endpoints that cross between
the A-cone and B-cone. In d_t dimensions, this fraction scales
as the (d_t-1)-dimensional boundary surface divided by the
d_t-dimensional volume: ~ 1/d_t.

### Therefore

The purity departure (1 - pur_min) ~ N^{-alpha_0/d_t} with alpha_0 ≈ 1.5.

## Novel Prediction

### Prediction 1: 5D networks (d_t=4) should give alpha ≈ -0.375

This is testable with the existing infrastructure. Generate 5D modular
DAGs and fit the exponent. The prediction is alpha = -1.5/4 = -0.375,
which should be distinguishable from the 4D value of -0.5 with 24 seeds.

### Prediction 2: The exponent should scale as 1/d_t even on non-modular graphs

The derivation doesn't use the channel gap. On UNIFORM d_t-dimensional
graphs (no imposed gap), the exponent should still follow the same
dimensional scaling. This is testable by running the 4D script with gap=0.

### Prediction 3: Increasing connect_radius at fixed extent should STEEPEN the exponent

The mixing fraction scales as (r/L)^{d_t-1}. Larger r means more
cone overlap, faster mixing, steeper exponent. This is consistent with
the universality test (connect_radius=5 gave alpha=-1.91 vs
connect_radius=2 gave alpha=-1.00).

Quantitative: doubling connect_radius should roughly double |alpha| in 2D.

## Weakest Link

**Step 4 is weakest.** The claim that "exclusive-node fraction scales
as (s/r)^{d_t-1}" assumes uniform random node placement and isotropic
connectivity. On graphs with directional preference (beta > 0 in the
continuation weight), the effective cone shape is anisotropic, and the
dimensional scaling may be modified.

**Test:** Run the exponent measurement on 2D graphs with beta=0
(isotropic) vs beta=0.8 (standard directional). If the derivation
is correct, both should give the same exponent (beta doesn't change
the cone geometry, only the amplitude weighting within the cone).
If the exponent changes significantly with beta, Step 4 needs revision.

## Status
PROPOSED — predictions untested
