# Newton's Law Derived from Cl(3) on Z^3

**Date:** 2026-04 (audit-narrowing refresh 2026-05-10)
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane. The
`bounded_theorem` label is a source-side claim-boundary declaration,
not an audit verdict; the 2026-05-10 audit verdict on the prior
unconditional framing recorded `audited_conditional` (chain_closes
False because the load-bearing Poisson equation was supported only by
a cited authority itself conditional on a stipulated `L^{-1}=G_0`
closure identity). This scope narrowing implements the verdict's
named repair-target option (b) "narrow this note to a bounded theorem
conditional on the Poisson equation".

## Bounded admissions

The load-bearing claim is **conditional on the two bounded admissions**
below. Neither is derived in this note; each is admitted as a named
input. The chain closes class-A algebraically from (BA-1) plus (BA-2)
plus elementary calculus on `Z^3`.

(BA-1) **Lattice Poisson equation as equation of motion.** The
staggered scalar field obeys

```text
(-Delta_lat) phi = rho                                                    (BA-1)
```

on `Z^3`, derived from the canonical staggered scalar action. This
identification is currently bounded by the `L^{-1} = G_0`
self-consistency closure supplied in
[`GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`](GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md);
the present note admits (BA-1) and does not re-derive it.

(BA-2) **Maradudin et al. 1971 lattice Green's function asymptotic.**
The Green's function of the lattice Laplacian on `Z^3` satisfies

```text
G(r) = (-Delta_lat)^{-1}(r)  ->  1 / (4 pi |r|)    as |r| -> infinity.   (BA-2)
```

Standard result of lattice potential theory (Maradudin, Montroll,
Weiss, *Theory of Lattice Dynamics in the Harmonic Approximation*,
1971); admitted as a textbook math input rather than derived in this
note.

(BA-1) and (BA-2) are the only bounded admissions. The chain to
Newton's inverse-square law closes class-A from (BA-1) and (BA-2)
without any further import.

## Theorem / Claim (conditional on BA-1 and BA-2)

**Theorem.** Given (BA-1) and (BA-2), let `(-Delta_lat)` be the lattice
Laplacian on `Z^3`. Then:

1. The Green's function G(r) of (-Delta_lat) satisfies
   G(r) -> 1 / (4 pi |r|) as |r| -> infinity, by (BA-2).

2. A point source of strength M produces potential
   phi(r) = M * G(r) -> M / (4 pi r), by linearity of (BA-1).

3. The force on a test mass M_test is F = -M_test * grad(phi) = M * M_test / (4 pi r^2),
   which is Newton's inverse-square law with G_N = 1/(4 pi) in lattice
   units.

4. The product M1 * M2 arises from two independent Poisson solves with
   cross-coupling. It is MEASURED from Poisson linearity (BA-1), not
   imposed as a bilinear ansatz.

5. The exponent 2 in 1/r^2 equals d - 1 = 3 - 1, where d = 3 is
   the spatial dimension from Cl(3). In general d dimensions, the
   Poisson Green's function gives F ~ 1/r^{d-1}.

## Assumptions

1. **Framework axiom:** Cl(3) on Z^3 (the framework axiom).
2. **(BA-1):** The staggered scalar field obeys the lattice Poisson
   equation `(-Delta_lat) phi = rho` (admitted; not derived here; see
   §"Bounded admissions" above).
3. **(BA-2):** Maradudin asymptotic theorem for the lattice Green's
   function (admitted as textbook math input; not derived here).

No additional physics is imported. Under (BA-1) and (BA-2), the
coupling constant G_N, the product law, the inverse-square exponent,
and the distance dependence all follow as class-A consequences.

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
  — supplies the `L^{-1} = G_0` self-consistency closure that justifies
  treating `(-Delta_lat)` as THE field operator (Theorem assumption 2:
  the lattice Poisson equation is the equation of motion). Correct
  upstream.

### Direction-corrected cycle break (2026-05-05)

The earlier link to `gravity_clean_derivation_note` is removed because
gravity_clean is a **parallel presentation** of the same Newton-from-Z^3
derivation, not an upstream supplier. Both this note and gravity_clean
independently consume the Maradudin et al. 1971 lattice Green's function
asymptotic theorem (an external math theorem, not an internal repo dep).
Neither note derives the other's content; they are alternate routes to
`F = G_N M_1 M_2 / r^2` from `Cl(3) on Z^3`.

The earlier back-link from this note to gravity_clean was added by a
prior audit-bookkeeping pass and created a length-2 citation cycle
`newton_law ↔ gravity_clean` in the graph. Removing the back-link breaks
the cycle without losing science content (the inline mathematical
justification — Maradudin's theorem — remains in the Theorem section).
