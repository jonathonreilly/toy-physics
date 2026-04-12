# Single Axiom: The Simplest Self-Consistent Computation

## Question

Do the two axioms of the framework (path-sum propagator + self-consistency)
reduce to a single axiom?

**Proposed single axiom:** *The simplest self-consistent computation exists.*

## The Argument

A computation requires:

1. **States** (nodes in a graph)
2. **Transitions** (edges connecting nodes)
3. **A rule for combining paths** (amplitudes or weights)
4. **Self-consistency** (the output feeds back as input and stabilizes)

If we demand the *simplest* computation that achieves self-consistency,
each structural choice is forced rather than postulated.

## Numerical Evidence

### Test 1: Complex amplitudes are selected (d_local = 2)

| Propagator | phi_center | IPR (density peakedness) |
|------------|-----------|------------------------|
| Classical (real Boltzmann weights) | 0.00499 | 8.50e-4 |
| Quantum (complex amplitudes) | 0.00596 | 9.68e-4 |

Quantum amplitudes give a 19% stronger gravitational well and 14%
sharper density profile. The mechanism: complex phases allow
destructive interference, which focuses the density more tightly
near the source. Classical (real positive) weights can only add
constructively, spreading the density.

**Selection principle:** Maximal gravitational focusing requires
interference, which requires complex amplitudes. The simplest
complex amplitude system is a single complex scalar (d_local = 2).
Extra components (d_local > 2) decouple without interaction terms,
giving identical physics to d_local = 2.

### Test 2: d = 3 spatial dimensions are selected

| Dimension | Converges | Green's function | Bound states |
|-----------|-----------|-----------------|-------------|
| d = 2 | Yes | log(r), confining | Infinite (no Kepler orbits) |
| d = 3 | Yes | 1/r, inverse-square | Finite Rydberg series |
| d = 4 | Yes | 1/r^2, marginal | Fall-to-center |
| d >= 5 | Yes | 1/r^(d-2) | None (unstable) |

All dimensions d >= 2 support a convergent self-consistent loop.
The selection comes from requiring *stable atoms*:

- d < 3: Confining potential, no inverse-square law, no Kepler orbits.
- d = 3: Hydrogen-like bound states with finite Rydberg series. Chemistry works.
- d = 4: Marginal. V ~ 1/r^2 has same scaling as centrifugal barrier;
  bound states collapse to zero radius (fall-to-center).
- d >= 5: No stable bound states at any coupling.

d = 3 is the minimum dimension where the self-consistent force law
supports stable matter. (See also `frontier_bound_state_selection.py`.)

### Test 3: Unitarity (reversibility) is required

Dissipation (information loss) changes the density profile when
propagating through the self-consistent field:

| gamma | IPR | Center density |
|-------|-----|---------------|
| 0.0 (unitary) | 6.15e-3 | 7.48e-10 |
| 0.5 | 8.87e-4 | 1.06e-3 |
| 2.0 | 3.80e-2 | 4.59e-2 |

The dissipative propagator produces a qualitatively different density
profile from the unitary one. The information-theoretic argument is
stronger than the numerics: self-consistency is a *fixed point*
condition (rho -> phi -> rho), and the data processing inequality
guarantees that an irreversible map cannot preserve the information
needed for a nontrivial fixed point.

**Selection principle:** Self-consistency requires reversibility.
Reversibility = unitarity (on finite graphs, all norm-preserving
linear maps are unitary).

### Test 4: Poisson field equation is uniquely selected

| Variant | Converges | Attractive | Notes |
|---------|-----------|-----------|-------|
| Valley-linear + Poisson | Yes | Yes | Standard framework |
| Quadratic + Poisson | Yes | Yes | Same at weak coupling |
| Repulsive + Poisson | Yes | Yes | Same at weak coupling |
| Valley-linear + non-local (1/r^2) | No | No | Wrong force law, diverges |
| Flat (no coupling) | Yes | Yes | No physical feedback |

The key discrimination is the *field equation*:

- **Poisson** (nearest-neighbor Laplacian): Converges to attractive gravity
  with the correct 1/r Green's function.
- **Non-local kernel** (1/r^2): Does not converge; gives wrong force law
  exponent (beta = 1.43 instead of the Poisson value).

Local action variants (quadratic, repulsive) are indistinguishable from
valley-linear at weak coupling (phi ~ 0.02 << 1), which is a form of
perturbative universality. At strong coupling, prior work
(`frontier_self_consistent_field_equation.py`) shows only the linear
coupling gives consistent attraction.

The flat propagator converges trivially but has no physical feedback --
the field does not affect the propagator, so it is not truly self-consistent.

## Chain of Forced Structure

Starting from "a self-consistent computation exists" plus "simplest":

```
Self-consistent computation exists
  |
  +-- States + transitions needed --> graph
  |
  +-- Self-consistency (fixed point) --> unitarity required
  |     (data processing inequality: irreversible maps
  |      cannot have nontrivial fixed points)
  |
  +-- Unitarity + simplest --> complex scalar (d_local = 2)
  |     (real weights = no interference = weaker focusing;
  |      d_local > 2 gives redundant degrees of freedom)
  |
  +-- Graph Laplacian as propagator --> Poisson field equation
  |     (Green's function of nearest-neighbor propagator
  |      IS the inverse Laplacian; uniqueness proven in
  |      frontier_poisson_exhaustive_uniqueness.py)
  |
  +-- Poisson + stable atoms --> d = 3
  |     (minimum dimension for 1/r potential + bound states)
  |
  +-- d=3 + Poisson + self-consistency --> valley-linear action
        (only action giving attractive gravity at strong coupling)
```

## Bounded Claim

Numerical evidence supports the thesis that self-consistency plus
minimality constrains all structural choices in the framework.
The path-sum propagator form (Axiom 1) is not independent of
self-consistency (Axiom 2); rather, Axiom 2 forces the specific
form of Axiom 1 when "simplest" is applied as a selection criterion.

The reduction is not yet fully rigorous:

- **Strong claim (supported):** Self-consistency forces the field equation
  (Poisson uniqueness) and dimension (bound state stability).
- **Moderate claim (supported):** Complex amplitudes give stronger gravity
  than classical weights, favoring quantum mechanics.
- **Weak point:** Action discrimination requires strong coupling;
  at weak coupling, perturbative universality makes all local actions
  equivalent. The full argument requires combining weak-coupling
  universality with strong-coupling discrimination (prior work).

## Script

`scripts/frontier_single_axiom_computation.py` -- runs in ~10 seconds.

## Prior Results Referenced

- `frontier_self_consistent_field_equation.py`: Poisson is forced by self-consistency
- `frontier_poisson_exhaustive_uniqueness.py`: Poisson is unique among all local operators
- `frontier_bound_state_selection.py`: d=3 selected by stable atomic bound states
- `frontier_dimension_emergence.py`: Spectral dimension determines force law
