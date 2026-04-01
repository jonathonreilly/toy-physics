---
name: b-independence derivation
date: 2026-04-01
status: DERIVED
---

# Why Gravity is b-Independent: The Extended Field Argument

## The phenomenon

On all tested graph architectures (random DAGs, locality-shell DAGs,
regular lattices), the gravitational deflection force is approximately
independent of the impact parameter b (distance between mass and source
axis). This holds across all propagator powers, node densities, and
spatial dimensions.

## The mechanism: Laplacian field extends the phase valley everywhere

### Step 1: Field structure

The gravitational field f is computed by Laplacian relaxation from
mass sources. On any connected graph, this produces f > 0 at every
reachable node, not just near the mass. The field decays with graph
distance but never reaches zero.

On a graph with mean path length L_graph, the field at distance r
from the mass decays as:
  f(r) ~ 1/r^alpha  (for small r)
  f(r) ~ f_floor > 0  (for r comparable to L_graph)

The "floor" f_floor is set by the graph's connectivity: more connected
graphs have higher floors because the Laplacian averages more quickly.

### Step 2: Phase perturbation per path

A path of N edges accumulates total phase perturbation:
  δΦ_path = k × Σ_edges δS_e

where δS_e ≈ L_e × f_e is the spent-delay change at edge e, and
f_e is the average field along the edge.

For a path that visits nodes at various transverse positions y_1, ..., y_N,
the total perturbation is:
  δΦ_path = k × Σ_i L_i × f(y_i, z_i; b)

where f(y, z; b) is the field at position (y, z) from mass at (x_m, b, z_m).

### Step 3: The averaging argument

The deflection is proportional to the y-derivative of the average
phase perturbation:
  shift ~ d/dy [<δΦ>_paths_to_detector_d]

The average phase perturbation over paths is dominated by the
integral of f along the typical path length:
  <δΦ> ~ k × N_edges × <f>_graph

where <f>_graph is the graph-average of the field. Because the
Laplacian relaxation averages f over the entire graph, <f>_graph
depends on the TOTAL mass (how many source nodes), not on WHERE
the mass is located.

### Step 4: Why b doesn't matter

The deflection comes from the GRADIENT of the phase perturbation
in the y-direction. This gradient is:
  d<δΦ>/dy ~ k × N × d<f>_graph/dy

But <f>_graph is the graph-averaged field, which varies only weakly
with the y-position of the mass. Moving the mass from b=2 to b=8
changes <f>_graph by at most O(1/N_nodes) because the field is
averaged over all N_nodes.

The y-GRADIENT of <f>_graph points toward the mass regardless of b,
but its MAGNITUDE is set by the ratio f_near/f_far, which is bounded
by the graph's mean path length, not by b.

### Step 5: What would break b-independence

b-dependent gravity requires:
  1. Sharply localized field (f → 0 far from mass), OR
  2. Paths that are geometrically constrained to a narrow y-band, AND
  3. The path-to-detector mapping preserves this constraint

Condition 1 fails because the phase valley requires an extended field
for constructive interference. Sharply localized fields produce weak,
noisy gravity (verified: Gaussian sigma=1, sharp field).

Condition 2 holds on the lattice (paths do preserve y-position), but
condition 3 fails because the detector centroid integrates over all
detectors, averaging out any local b-dependence.

## Verified predictions

1. **Paths preserve transverse position**: <y_det> tracks y_src on
   random DAGs. b-independence is NOT from path scrambling.

2. **Localized fields weaken gravity without introducing 1/b**:
   Sharp field gives near-zero signal. Gaussian sigma=2 gives a weak
   hint of b-dependence but mostly noise.

3. **The Laplacian field is the b-independence engine**: its graph-wide
   extent makes <f>_graph insensitive to mass position.

## Implication

b-independence is intrinsic to the phase valley + Laplacian field
architecture. Getting 1/b would require either:
- A field propagation mechanism that maintains 1/r^d_spatial decay
  without Laplacian averaging (e.g., retarded Green's function)
- A non-linear propagation that couples the field to the amplitude
  in a way that breaks the averaging
- A fundamentally different gravity mechanism (metric emergence)
