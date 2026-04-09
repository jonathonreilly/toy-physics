# Derivation: Asymmetric deflection on Z₂-symmetric graphs

## Date
2026-04-03

## Target Behavior
The S4 mirror family (explicit edge mirroring) produces gravity at
+3.96 SE (N=60) while Z₂×Z₂ (implicit radius-based connectivity on
symmetric node positions) produces only +0.98 SE (N=60).

Both have Z₂ symmetry in node positions. Both use the same propagator
and the same asymmetric mass placement (y > 0 only). Why does explicit
edge mirroring preserve gravity while implicit connectivity doesn't?

## Axioms Used
- Links connect events with directed influence (axiom 1)
- Continuation weights govern path selection (axiom 6)
- Gravity is natural continuation in a distorted continuation structure (axiom 8)

## Minimal Example

Consider 4 nodes per layer, 2 layers post-barrier:

```
Explicit mirror (S4):
  Node A (y=+5) connects to: C (y=+3), D (y=-3)   ← radius check
  Node B (y=-5) connects to: D (y=-3), C (y=+3)   ← FORCED mirror of A's edges

  Result: A→C and B→D are the "same-side" edges.
          A→D and B→C are the "cross-side" edges.
          Every edge has an exact mirror partner.

Implicit radius (Z₂×Z₂):
  Node A (y=+5) connects to: C (y=+3)               ← within radius
  Node B (y=-5) connects to: D (y=-3)               ← within radius
  A does NOT connect to D (too far if |y_A - y_D| > radius)
  B does NOT connect to C (too far)

  Result: NO cross-side edges. Channels are disconnected.
```

The critical difference: **explicit mirroring creates cross-channel
edges that the radius check alone does not.**

## Derivation

### Step 1: The field breaks the graph's Z₂ symmetry

Mass at y > 0 creates a field f(node) that is NOT y-symmetric.
Nodes near the mass have higher field values.
The distorted delay dl = L * (1 + f) is larger near mass.
The spent-delay action S = dl - sqrt(dl² - L²) is larger near mass.

Wait — larger action means MORE phase, not less. Let me re-check.

Actually: for small f, S ≈ L*f + O(f²). So S increases with f.
The propagation kernel is exp(i*k*S). Higher S = faster phase rotation.

The deflection arises because paths near mass accumulate DIFFERENT
phase than paths far from mass. When summed at the detector, the
phase differences create constructive interference toward mass
(where phases align) and destructive interference away from mass.

### Step 2: Explicit mirroring preserves path-pair structure

On the S4 mirror graph, every path from source to detector through
the upper channel has an EXACT mirror path through the lower channel.
These mirror paths have different actions (one passes near mass, one
doesn't) but the SAME geometric structure (same edge lengths, same
angles, just y-reflected).

When the field is applied asymmetrically (mass at y > 0):
- Upper-channel paths: action modified by field → phase shifted
- Lower-channel mirror paths: action NOT modified → reference phase

The detector amplitude is the sum of ALL paths. The field creates a
phase DIFFERENCE between upper and lower channel paths. This phase
difference deflects the amplitude toward the mass side.

The key: the mirror pairing ensures that for every path contributing
to the "toward mass" signal, there is a reference path with the
baseline phase. The difference is purely from the field, not from
random geometric fluctuations.

### Step 3: Implicit radius connectivity breaks path-pair structure

On the Z₂×Z₂ graph, edges are determined by radius, not by mirroring.
Two consequences:

(a) Cross-channel edges may be ABSENT if the radius doesn't reach
    across the y=0 plane. This means upper and lower channels are
    effectively disconnected — amplitude from the source reaches
    different detector nodes depending on which slit it entered.

(b) The edge SET is different for upper and lower nodes even at
    the same distance from y=0. Node A at (x, +5, +3) may connect
    to different previous-layer nodes than node B at (x, -5, +3)
    because the specific random positions of previous-layer nodes
    create different neighborhoods.

Result: the path ensemble from slit A and slit B have different
geometric structure (different edge lengths, different angles) in
ADDITION to different field values. The geometric differences create
random phase variations that mask the field-induced deflection.

### Step 4: The gravity signal is a field-minus-geometry difference

On the S4 mirror graph:
  Gravity signal = (field-induced phase shift) only
  Geometric noise = 0 (mirror paths have identical geometry)

On the Z₂×Z₂ graph:
  Gravity signal = (field-induced phase shift)
  Geometric noise = (random phase from different path geometries)
  Signal-to-noise = gravity / geometric_noise → weak

### Step 5: Therefore, explicit edge mirroring preserves gravity

The S4 mirror family has strong gravity because the mirror pairing
eliminates geometric noise from the deflection measurement. The
Z₂×Z₂ family has weak gravity because the radius-based connectivity
creates geometric asymmetry that adds noise to the phase signal.

## Novel Prediction

**Prediction:** If we add explicit edge mirroring to the Z₂×Z₂
generator (so that every edge (i,j) has a mirror partner
(mirror(i), mirror(j)) for BOTH y and z reflections), the gravity
signal should increase from ~1 SE to ~3+ SE while decoherence
remains at the Z₂×Z₂ level.

**Quantitative:** Z₂×Z₂ with explicit edge mirroring at N=60 should
give gravity > 2.0 SE AND pur_cl < 0.75.

**Second prediction:** The ratio gravity(S4) / gravity(Z₂×Z₂) should
correlate with the ratio of cross-channel edges. S4 has forced
cross-channel edges; Z₂×Z₂ may have few or none. Measuring
cross-channel edge fraction should predict gravity strength.

## Weakest Link

Step 3(b): the claim that radius-based connectivity creates
"geometric noise" that masks the field signal. This could be
tested by computing the variance of path-length differences
between mirror-paired paths on S4 vs Z₂×Z₂. On S4, this variance
should be exactly zero. On Z₂×Z₂, it should be positive and
correlate with gravity weakness.

## Status
PROPOSED — test the novel prediction by implementing Z₂×Z₂ with
explicit edge mirroring.
