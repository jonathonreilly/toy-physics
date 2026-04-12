# Gate 2: Generation Physicality

**Status:** Bounded -- exact algebra retained, physical interpretation conditional  
**Codex objection:** "still open" -- Wilson entanglement test does not prove physicality  
**Script:** `frontier_generations_rigorous.py` (20/20), `frontier_generation_physicality.py` (20/20)

---

## What is proven

1. **Exact orbit algebra.** The 8 = 2^3 taste states of staggered fermions in
   d = 3 decompose under the Z_3 cyclic permutation sigma: (s1,s2,s3) ->
   (s2,s3,s1) into exactly 4 orbits: two singlets (Hamming weight 0 and 3)
   and two triplets (Hamming weight 1 and 2). The partition 8 = 1 + 3 + 3 + 1
   is verified by explicit enumeration and confirmed by Burnside's lemma:
   |Fix(e)| = 8, |Fix(sigma)| = 2, |Fix(sigma^2)| = 2, giving
   (8 + 2 + 2)/3 = 4 orbits.

2. **The 1+3+3+1 pattern is a combinatorial identity of d = 3.** The binomial
   coefficients C(3,k) = 1, 3, 3, 1 give the orbit sizes by Hamming weight.
   This is dimension-locked: for d = 2 one gets 1+2+1 (two generations), for
   d = 4 one gets 1+4+6+4+1 (no clean triplet structure). The number 3 in
   "three generations" is the spatial dimension.

3. **The orbits are algebraically distinct.** The three states within each
   triplet orbit differ in their Brillouin-zone momentum assignments and
   carry distinct O(a^2) taste-breaking corrections. These are not copies of
   the same state -- they are distinguishable by lattice-scale observables.

## What is dropped

The Wilson entanglement test (argument 6 in the 20/20 script) does not prove
what the earlier notes claimed. The entanglement entropy of Wilson-deformed
states shows that taste structure is fragile under deformation, but fragility
is not the same as physicality. This argument is withdrawn from the closure
claim.

## What remains bounded

The physical interpretation of taste orbits as fermion generations requires one
structural assumption: **taste-physicality** -- that the lattice spacing a is a
physical minimum (a = l_Planck) and there is no continuum limit in which taste
splittings vanish.

The two strongest arguments for this assumption are:

1. **No continuum limit.** In lattice QCD (d = 4), taste splitting scales as
   a^2 and vanishes as a -> 0 (the fourth-root trick removes doublers). In
   this framework, a = l_Planck is the physical UV cutoff. There is no a -> 0
   limit. Taste-breaking mass splittings of order 1/a are permanent physical
   mass differences, not discretization artifacts.

2. **C(3,k) is dimension-locked.** The orbit count follows from the
   combinatorial identity C(d,k) applied to d = 3. This is not a property of
   a particular lattice size L -- it holds for any Z^3 lattice and is
   independent of the continuum limit question. The triplet structure is exact
   at all scales.

However, taste-physicality is not itself a theorem derived from the axiom. It
is a structural consequence of interpreting the lattice as fundamental rather
than as a regulator. This interpretation is physically motivated but is an
additional commitment beyond the algebra.

## Paper-safe claim

> The exact orbit algebra 8 = 1 + 3 + 3 + 1 under Z_3 cyclic permutation is
> retained as a proven algebraic result of the d = 3 staggered construction.
> The physical interpretation of the two triplet orbits as three fermion
> generations is bounded by the taste-physicality argument: no continuum limit
> exists when a = l_Planck, so taste splittings are permanent. This is a
> well-motivated structural argument but not yet a theorem.
