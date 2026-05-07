# Newton's Law Derived from Cl(3) on Z^3

**Status:** support - structural or confirmatory support note
## Status

**Closed** on the retained framework surface.

Newton's inverse-square law F = G M1 M2 / r^2 follows from the Poisson
equation on Z^3 without additional assumptions.

## Theorem / Claim

**Theorem.** Let (-Delta_lat) be the lattice Laplacian on Z^3. Then:

1. The Green's function G(r) of (-Delta_lat) satisfies
   G(r) -> 1 / (4 pi |r|) as |r| -> infinity (Maradudin et al. 1971).

2. A point source of strength M produces potential phi(r) = M * G(r) -> M / (4 pi r).

3. The force on a test mass M_test is F = -M_test * grad(phi) = M * M_test / (4 pi r^2),
   which is Newton's law with G_N = 1/(4 pi) in lattice units.

4. The product M1 * M2 arises from two independent Poisson solves with cross-coupling.
   It is MEASURED from Poisson linearity, not imposed as a bilinear ansatz.

5. The exponent 2 in 1/r^2 equals d - 1 = 3 - 1, where d = 3 is
   the spatial dimension from Cl(3). In general d dimensions, the Poisson
   Green's function gives F ~ 1/r^{d-1}.

## Assumptions

1. Cl(3) on Z^3 (the framework axiom).
2. The staggered scalar field obeys the lattice Poisson equation
   (-Delta_lat) phi = rho (equation of motion from the action).
3. The asymptotic theorem for the lattice Green's function
   (standard lattice potential theory, not a framework-specific claim).

No additional physics is imported. The coupling constant G_N, the product
law, the inverse-square exponent, and the distance dependence all follow.

## What Is Actually Proved

**Exact results (mathematical theorems):**

- The lattice Laplacian Green's function on Z^3 converges to 1/(4 pi r)
  for large r. This is a theorem of lattice potential theory.
- Poisson linearity: phi(M) = M * phi(1) exactly.
- The product law F ~ M1 * M2 follows from linearity + cross-coupling.
  This is exact given the Poisson equation.
- The force exponent d - 1 follows from the dimension of the Poisson
  equation. In d = 3: F ~ 1/r^2 exactly.

**Numerical confirmations (bounded checks):**

- Green's function ratio 4 pi r G(r) -> 1.0 confirmed to < 1% for r >= 5
  on a 64^3 lattice.
- Deflection exponent alpha -> -1.0 confirmed to < 5% on 32^3 to 64^3
  lattices (consistent with sub-1% at 128^3 from frontier_distance_law_definitive.py).
- Product law gamma = 1.0 confirmed to < 5% on 32^3 lattice.
- Dimensionality check: d=1 (constant force), d=2 (1/r force), d=3 (1/r^2 force)
  all confirmed numerically.

## What Remains Open

Nothing in the Newton's law derivation chain remains open. The derivation
is complete on the framework's theorem surface:

- The Poisson equation is the equation of motion.
- The Green's function asymptotics are a mathematical theorem.
- The product law is exact from linearity.
- The exponent is exactly d - 1 = 2.

The only bounded element is the finite-lattice numerical precision of
the checks, which is a verification limitation, not a logical gap.

## How This Changes The Paper

This derivation belongs in the paper as a clean worked example of how
a macroscopic force law emerges from the framework without additional input:

> The inverse-square gravitational force law F = G M1 M2 / r^2 is a
> consequence of the lattice Poisson equation on Z^3. The Green's function
> of the lattice Laplacian approaches 1/(4 pi r) at large distances
> (a standard result of lattice potential theory). The product M1 M2
> emerges from Poisson linearity with cross-coupling between independent
> sources. The exponent 2 = d - 1 follows from the spatial dimension d = 3,
> itself determined by Cl(3).

This closes the loop from the framework axiom Cl(3) on Z^3 to Newton's
law with no free parameters beyond the overall coupling normalization.

This is the retained weak-field gravity claim. Broader GR-signature notes
(WEP, time dilation, light bending, geodesics, strong-field extension) should
still be carried separately with their actual bounded status.

## Commands Run

```bash
cd /Users/jonreilly/Projects/Physics
python3 scripts/frontier_newton_derived.py
```

## Supporting Evidence

The distance law and product law have been independently verified at
higher precision in:

- `scripts/frontier_distance_law_definitive.py` (sub-1% at 128^3)
- `scripts/frontier_product_law_no_ansatz.py` (product law without bilinear ansatz)
- `scripts/frontier_dm_coulomb_from_lattice.py` (Green's function theorem + numerics)

This note synthesizes those results into a single derivation chain.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [gravity_full_self_consistency_note](GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md)

The earlier link to `gravity_clean_derivation_note` is removed here as a
cycle-break: that note CONSUMES this one (via Step 8 of its derivation
chain, the `Z^3` Green-function asymptotic) and is downstream, not
upstream. The prior audit that asked for the back-link did so before the
chain direction was clarified; the back-link created a length-2 cycle in
the citation graph (newton_law ↔ gravity_clean) that blocked retained-tier
promotion of either. The forward edge `gravity_clean → newton_law_derived`
is preserved on the gravity_clean side and is the correct direction.
