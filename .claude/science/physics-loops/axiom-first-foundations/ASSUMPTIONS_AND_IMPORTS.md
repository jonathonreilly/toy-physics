# ASSUMPTIONS_AND_IMPORTS — axiom-first-foundations block01

## A_min (current package boundary, verbatim from `docs/MINIMAL_AXIOMS_2026-04-11.md`)

| ID | Statement |
|----|-----------|
| A1 | Local algebra: the physical local algebra is `Cl(3)`. |
| A2 | Spatial substrate: the physical spatial substrate is the cubic lattice `Z^3`. |
| A3 | Microscopic dynamics: finite local Grassmann / staggered-Dirac partition together with the lattice operators built on that surface. |
| A4 | Canonical normalization: `g_bare = 1` together with the accepted plaquette / `u_0` surface and the minimal APBC hierarchy block. |

`A4` is itself carried by two retained structural routes
(operator-algebra: `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`
+ `G_BARE_RIGIDITY_THEOREM_NOTE.md`; 1PI: `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`
+ Rep-B independence + same-1PI pinning) plus the dynamical-fixation obstruction.
Any derivation in this loop that uses `g_bare = 1` cites those theorems.

## Mathematical infrastructure permitted (post-A_min, ordinary tools)

- finite-dimensional linear algebra over `R` and `C`
- finite Grassmann calculus (Berezin integrals, Pfaffian/determinant identities)
- finite group / finite Clifford algebra representation theory
- transfer-matrix construction on a finite lattice
- standard discrete Fourier on `Z^3` with periodic / APBC boundary
- spectral theory of finite Hermitian and unitary operators
- standard counting / combinatorial bookkeeping on the cubic lattice

These are *not* axioms. They do not promote a bounded claim to retained on
their own.

## Forbidden imports (anti-list for this loop)

1. Any observed numerical value as a step in a derivation. Comparators may
   appear only as sanity checks at the end of a runner, never as a hidden
   pivot inside the chain.
2. Continuum-QFT axiom systems (Wightman, Osterwalder–Schrader,
   Haag–Kastler) imported as black boxes. We may *parallel* those statements
   on the lattice; we do not import them as primitive.
3. Lorentz invariance, full Poincaré, or continuum CPT as a primitive.
   Any lattice analogue must be stated as a discrete symmetry of the
   `A_min` action and proved.
4. Spin-statistics, reflection positivity, cluster decomposition, or CPT
   as primitives. These are precisely the targets of this loop; they may
   not appear as imports for one route while being claimed as theorems on
   another.
5. Fitted selectors or tuned parameters of any kind.
6. Numerical-fit curves used as functional-form premises.

## Imports the loop deliberately retires (one per route)

| Route | Import retired | Replacement (theorem to prove) |
|-------|---------------|--------------------------------|
| R1 | spin-statistics asserted on `Cl(3)` Grassmann fields | finite-Grassmann + Cl(3) ⇒ fermionic anticommutation theorem |
| R2 | reflection positivity asserted for the canonical staggered-Dirac action | `A_min` ⇒ RP for the canonical staggered + Wilson plaquette action on the temporal-reflection surface |
| R3 | cluster decomposition asserted at long range | `A_min` + finite-range Hamiltonian ⇒ exponential clustering theorem (Lieb–Robinson-style on Cl(3) tensor product) |
| R4 (stretch) | CPT-evenness asserted (e.g. in `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`) | `A_min` ⇒ a discrete CPT symmetry of the Cl(3) staggered Grassmann action |
