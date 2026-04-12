# Single Axiom Reduction: Local Tensor Product Hilbert Space

**Date:** 2026-04-12
**Status:** PASS -- all four tests support axiom unification
**Runner:** `scripts/frontier_single_axiom_hilbert.py`

## Question

Can the two axioms (finite graph + unitary evolution) be reduced to one?

**Candidate single axiom:** A finite Hilbert space with local tensor product
structure, H = H_1 (x) H_2 (x) ... (x) H_N.

This single mathematical object encodes the nodes (the factors H_i), locality
(only neighboring factors interact via the Hamiltonian), unitarity (automatic
for Hermitian generators on a Hilbert space), and the Born rule (automatic
from the inner product).

## Tests and Results

### Test 1: Graph emerges from Hamiltonian support

Built random local Hamiltonians on 5-qubit systems with random interaction
graphs (3--10 edges per trial). Extracted the interaction graph by decomposing
H into a product operator basis and checking for non-trivial 2-site
components.

| Trial | Input edges | Recovered edges | Match |
|-------|------------|-----------------|-------|
| 1     | 3          | 3               | yes   |
| 2     | 8          | 8               | yes   |
| 3     | 4          | 4               | yes   |
| 4     | 8          | 8               | yes   |
| 5     | 5          | 5               | yes   |

Recovery rate: 100%. The graph is not assumed -- it is the support of the
Hamiltonian on the tensor factors.

### Test 2: Born rule is automatic (I_3 = 0)

Third-order interference I_3 computed for 200 random state pairs in
dimension-8 Hilbert space.

| Framework         | mean |I_3|   | max |I_3|    |
|-------------------|--------------|---------------|
| Hilbert (p=2)     | 1.3 x 10^-17 | 2.6 x 10^-16 |
| p-norm p=1.5      | 7.0 x 10^-3  | 5.3 x 10^-2  |
| p-norm p=3.0      | 2.0 x 10^-3  | 2.9 x 10^-2  |
| p-norm p=4.0      | 1.0 x 10^-3  | 3.6 x 10^-2  |

In Hilbert space, I_3 = 0 to machine precision. Any p != 2 norm gives I_3 != 0.
The Hilbert space inner product forces the Born rule.

### Test 3: Unitarity is automatic; Lindblad breaks gravity

8-site chain with 1/r gravitational potential. Unitary evolution concentrates
probability at the gravitational center. Lindblad (non-unitary) evolution with
increasing dephasing rate gamma:

| gamma | Center excess | Behavior                        |
|-------|---------------|---------------------------------|
| 0.0   | +0.104        | Probability at center (gravity) |
| 0.1   | +0.078        | Weakened attraction              |
| 0.5   | -0.005        | Attraction destroyed             |
| 1.0   | -0.078        | Stuck near source                |
| 2.0   | -0.167        | Localized at source              |

Unitarity is automatic from the Hermitian Hamiltonian. Non-unitary evolution
(open systems, Lindblad channels) destroys gravitational attraction -- particles
freeze at their source instead of migrating toward the potential minimum.

### Test 4: Tensor product structure is essential

Compared a 6-qubit chain (tensor product, local Hamiltonian) to a random
64x64 Hamiltonian (same dimension, no factorization).

| Metric               | Tensor product | Unfactored |
|----------------------|---------------|------------|
| Participation ratio  | 1.0 / 6 sites | 30.2 / 64 states |
| Distance dependence  | Yes (decay with graph distance) | No (uniform spread) |
| Spread ratio         | 29x more localized | baseline |

Without tensor product factorization there is no notion of locality, distance,
or spatial structure. The propagator spreads uniformly rather than respecting
any geometry. Gravity requires locality; locality requires the tensor product.

## Conclusion

The two axioms reduce to one. The single axiom is:

**A finite-dimensional Hilbert space with local tensor product structure.**

From this one object:
- The **graph** emerges as the interaction support of the Hamiltonian (Test 1)
- The **Born rule** is automatic from the inner product norm (Test 2)
- **Unitarity** is automatic from the Hermitian generator (Test 3)
- **Locality and spatial structure** are the tensor product factorization (Test 4)

What remains specified beyond the axiom: the local dimension d and the
Hamiltonian H (which encodes dynamics and implicitly defines the graph
topology). But the framework -- the arena in which physics plays out --
is fully captured by this single axiom.

## Caveats

1. The Hamiltonian is additional data on top of the tensor product space. One
   could argue this is a second specification (though not a second axiom about
   the framework).

2. The "local" qualifier (interactions couple only neighboring factors) is
   doing real work. A tensor product space with all-to-all interactions would
   not give spatial locality. The restriction to local H is part of the axiom.

3. These are small-system demonstrations (5--8 sites). The argument is
   structural and holds at any scale, but large-scale gravitational physics
   tests (distance law, etc.) use the 3D lattice infrastructure in other
   frontier scripts.
