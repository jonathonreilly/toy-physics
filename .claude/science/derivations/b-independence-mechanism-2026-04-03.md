# Derivation: Why gravity deflection is b-independent

## Date
2026-04-03

## Target Behavior
On all tested graph families, the gravity deflection does not decay
with impact parameter b. At y=7 and y=16 on a 2D mirror (yr=20),
gravity is +4.83 and +4.39 respectively (essentially equal at 5 SE).
The field f = 0.1/r DOES decay with distance, but the centroid shift
does not.

## Axioms Used
- Events are nodes with positions (x, y) or (x, y, z)
- Links have continuation weights: exp(i*k*S) * w / L
- S (action) depends on the field: S = dl - sqrt(dl² - L²) where dl = L*(1+f)
- The field f = 0.1/r decays as 1/distance from mass

## Minimal Example

Consider 3 layers: source → intermediate → detector.
Mass at (x_mass, y_mass) where y_mass = b (impact parameter).
Two intermediate nodes at (x_mid, y_1) and (x_mid, y_2).

Path 1: source → node_1 → detector_d
Path 2: source → node_2 → detector_d

The field at node_1 is f_1 = 0.1/r_1 where r_1 = |node_1 - mass|.
The field at node_2 is f_2 = 0.1/r_2.

The PHASE DIFFERENCE between the two paths reaching detector_d is:
  ΔΦ = k * (S_1 - S_2)

where S_1, S_2 are the actions along each path.

## Derivation

### Step 1: The field gradient determines the phase gradient

For paths at y-position y near the beam center (y ≈ 0), the field
from mass at y = b is:
  f(y) = 0.1 / sqrt(Δx² + (b - y)²)

The field GRADIENT in y is:
  ∂f/∂y = 0.1 * (b - y) / (Δx² + (b - y)²)^(3/2)

At the beam center (y = 0):
  ∂f/∂y|_{y=0} = 0.1 * b / (Δx² + b²)^(3/2)

For b >> Δx: ∂f/∂y ∝ 1/b² (decaying gradient).
For b << Δx: ∂f/∂y ∝ b/Δx³ (growing gradient).

So the LOCAL field gradient DOES decay as 1/b² in the far field.
The phase gradient should also decay. WHY DOESN'T THE DEFLECTION?

### Step 2: The deflection is NOT proportional to the local gradient

The centroid shift is:
  Δy = Σ_d |ψ_mass(d)|² * y_d / Σ_d |ψ_mass(d)|²
     - Σ_d |ψ_flat(d)|² * y_d / Σ_d |ψ_flat(d)|²

This is a RATIO of weighted sums. It depends on the NORMALIZED
detector distribution, not on the raw amplitude.

### Step 3: The normalization removes the b-dependence

Consider two regimes:

(a) Weak field (large b): f is small everywhere in the beam.
    All paths have nearly the same phase. The detector distribution
    is nearly the same as the flat-field case. SMALL deflection.
    This is what we EXPECT and what would give 1/b.

(b) Strong field (small b): f is large near the mass side.
    Paths on the mass side have significantly different phase.
    The detector distribution shifts toward mass. LARGE deflection.

The problem is regime (a). Let me check whether the field at the
beam IS actually small at large b.

### Step 4: The field is NOT small at the beam at large b

On a graph with y_range = 20 and mass at y = 16, the field at
the beam center (y ≈ 0) is:
  f(0) = 0.1 / sqrt(Δx² + 16²)

With Δx ≈ N_layers/3 ≈ 13 (distance from mass layer to beam):
  f(0) = 0.1 / sqrt(169 + 256) = 0.1 / 20.6 ≈ 0.005

BUT: the field at a node near the mass (y = 16):
  f(16) = 0.1 / sqrt(Δx² + 0) = 0.1 / 13 ≈ 0.008

So f(0)/f(16) ≈ 0.6. The field at the beam center is 60% of the
field at the mass itself! The 1/r decay is not steep enough to
create a strong gradient across the beam.

THIS is the mechanism: the field is a GLOBAL Laplacian solution
that extends everywhere on the graph. At b = 16, the field at
y = 0 is not much weaker than at y = 16 because the graph has
finite extent and the Laplacian field fills the whole graph.

### Step 5: On a FINITE graph, the Laplacian field is nearly uniform

The field f = 0.1/r is computed by summing 1/distance from each
mass node. On a finite graph with y_range = 20, the field ranges
from f_max ≈ 0.1/(0.1) = 1.0 (at mass) to f_min ≈ 0.1/28 ≈ 0.004
(at the far corner). The RELATIVE variation across the beam width
(say, from y = -3 to y = +3) is:

  Δf_beam = f(beam_near_mass) - f(beam_far_from_mass)
           ≈ 0.1/sqrt(Δx² + (b-3)²) - 0.1/sqrt(Δx² + (b+3)²)

For b = 16, Δx = 13:
  f(y=-3) = 0.1/sqrt(169 + 361) = 0.1/23.0 = 0.00435
  f(y=+3) = 0.1/sqrt(169 + 169) = 0.1/18.4 = 0.00544
  Δf = 0.00109

For b = 7, Δx = 13:
  f(y=-3) = 0.1/sqrt(169 + 100) = 0.1/16.4 = 0.00610
  f(y=+3) = 0.1/sqrt(169 + 16) = 0.1/13.6 = 0.00735
  Δf = 0.00125

Δf(b=16)/Δf(b=7) ≈ 0.87. The field gradient only drops 13%
when b doubles from 7 to 16. This is because the Laplacian
1/r field is shallow — it varies slowly over the beam width.

### Step 6: The deflection is set by the TOTAL accumulated phase contrast

The beam passes through ~N/3 layers between barrier and detector.
At each layer, it accumulates a phase contrast ΔΦ_layer ≈ k * Δf * L.
The total phase contrast is:
  ΔΦ_total ≈ k * Δf * L * N_post_barrier

Since Δf barely changes with b (step 5), and N_post_barrier and L
are graph properties independent of b, the total phase contrast
is nearly b-independent.

### Step 7: Therefore the deflection saturates

The centroid shift is a function of ΔΦ_total:
  Δy ≈ Δy_sat * tanh(C * ΔΦ_total)

Since ΔΦ_total barely changes with b, Δy barely changes with b.
The deflection is b-independent because:
  (a) The 1/r field has weak gradient variation across the beam
  (b) The phase contrast accumulates over many layers
  (c) The cumulative contrast saturates the tanh response

## Novel Prediction

**To get 1/b falloff, the field gradient across the beam must decay
as 1/b.** This requires either:

1. A STEEPER field: f ~ 1/r^n with n > 1. If n = 2 (Newtonian 3D),
   the gradient would be ∂f/∂y ~ 1/b³, and the beam-averaged gradient
   would scale as ~1/b². On a finite graph, this would create enough
   gradient variation for the deflection to decay.

   **Prediction:** If we replace f = 0.1/r with f = 0.1/r² in the
   field computation, the deflection should show 1/b or steeper falloff.

2. A NARROWER beam: if the beam width w << b, the gradient across
   the beam is ∂f/∂y * w, which decays as 1/b² * w. Currently
   w ~ y_range (the beam fills the whole graph). A narrower beam
   (from stronger directional measure β) would see less field variation.

   **Prediction:** Increasing β from 0.8 to 5.0 should narrow the
   beam and create distance-dependent deflection.

3. A LOCALIZED field: if the field has finite range (not global
   Laplacian), distant masses don't affect the beam. An exponentially
   decaying field f ~ exp(-r/r0) would give the deflection a natural
   distance scale.

   **Prediction:** Replacing f = 0.1/r with f = 0.1*exp(-r/r0)
   where r0 ~ beam_width should give 1/b-like falloff for b > r0.

## Weakest Link

Step 5 assumes that the field gradient ratio Δf(b=16)/Δf(b=7) ≈ 0.87
based on analytic 1/r. The actual field on the discrete graph includes
connectivity effects that could change this ratio. Test: compute the
actual field gradient at the beam center for multiple b values on the
2D mirror graph and compare to the analytic prediction.

## Status
PROPOSED — test all three predictions (steeper field, narrower beam,
localized field).
