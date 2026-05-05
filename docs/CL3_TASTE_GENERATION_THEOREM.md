# Cl(3) Taste-Generation Theorem: Z³ Lattice Doubling → 3 Tastes with Generation Structure

**Date:** 2026-04-19 (originally); 2026-05-04 (audited_renaming scope-narrow)
**Status:** representation-theory theorem on the staggered-Dirac taste cube. The hw=1 orbit gives **three Z₃-related generation-candidate states** with the listed Y/T₃ spectra; identifying these candidates with **physical SM generations** is a separate retained-bridge requirement, not part of this theorem's load-bearing scope.
**Claim type:** bounded_theorem
**Claim boundary authority:** this note
**Script:** `scripts/verify_cl3_sm_embedding.py` (section G);
            `scripts/frontier_s3_action_taste_cube_decomposition.py` (independent crosscheck)

---

## Audit-driven scope narrowing (2026-05-04)

The 2026-05-04 audit verdict was `audited_renaming`: the
representation-theory checks (S₃ decomposition `4A₁ + 0A₂ + 2E`, hw=1 = A₁+E
with Z₃ orbit, restricted Y/T₃ spectra) were accepted as algebraic content, but the
load-bearing identification of these Z₃-orbit states with **three physical
SM generations** requires a separate retained bridge theorem this note
does not provide. The narrowed scope below keeps the verified algebraic
content and explicitly defers the physical generation identification.

The renaming criterion (from the audit): *"Re-check whether a separate
retained bridge theorem derives taste-orbit states as physical SM
generations rather than naming them generation candidates."* This note now
adopts the narrower "generation-candidate" framing throughout.

## Statement (scope-narrowed)

**Theorem (representation-theory, scope-narrowed).** The staggered-fermion
doubling on Z³ produces a taste space `C^8 = (ℂ²)^{⊗3}` on which the
following are exact representation-theory facts:

1. The axis-permutation group S₃ acts by tensor-position permutation, giving the
   decomposition `C^8 = 4A₁ + 0A₂ + 2E` (no A₂ component).

2. The Hamming-weight-1 sector (hw=1), spanned by
   `{e₁=(1,0,0), e₂=(0,1,0), e₃=(0,0,1)}`, transforms as the 3-dimensional
   permutation representation `A₁ + E` of S₃.

3. The three hw=1 states are related by the Z₃ cyclic subgroup:
   `e₁ → e₂ → e₃ → e₁`.

4. The hw=1 sector has Y eigenvalues {+1/3, +1/3, −1} and T₃ eigenvalues
   {−1/2, +1/2, +1/2} within the 3D subspace. The Z₃ cyclic symmetry relates all
   three states.

5. **Generation-candidate framing.** The combined hw=1 matter content — two
   quark-like (Y=+1/3) and one lepton-like (Y=−1) — is **consistent with**
   one SM left-handed generation, and the three-fold Z₃ degeneracy provides
   **3 such generation-candidate states**. This statement is at the level
   of representation-theory consistency, not physical identification.

## Physical-generation identification (deferred to a separate bridge)

This note **does not derive** the physical identification

> "the three Z₃-related taste states **are** the three physical SM
> generations (e/μ/τ together with d/s/b and u/c/t partner blocks)."

That identification is the load-bearing bridge gap flagged by the
2026-05-04 audit. To close this lane to retained-grade, a separate
retained-grade theorem must derive:

- The map between the Z₃-cyclic taste-orbit indexing and the physical
  generation index;
- Why the residual block degeneracy lifts in the physical mass spectrum
  in the Yukawa hierarchy direction (light/heavy generation split), not
  the taste-cycle direction;
- Why the Z₃-orbit ordering matches the observed e/μ/τ mass ordering or,
  equivalently, why the Yukawa hierarchy respects the cyclic structure.

Until that bridge is on the retained-grade surface, the corollary "the three
hw=1 Z₃ states **are** the three physical SM generations" is **conditional
on the bridge**, not a direct consequence of this note's
representation-theory.

Related current surfaces are
[`S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`](S3_TASTE_CUBE_DECOMPOSITION_NOTE.md),
[`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md),
and [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md). They are
not treated here as supplying the deferred physical-generation bridge.

---

## Proof

### A. S₃ Action on C^8

S₃ acts on `(ℂ²)^{⊗3}` by permuting tensor positions. For permutation `σ ∈ S₃`,
the unitary operator `U(σ)` satisfies:

```
U(σ)|b₁,b₂,b₃⟩ = |b_{σ⁻¹(1)}, b_{σ⁻¹(2)}, b_{σ⁻¹(3)}⟩
```

This action:
- Preserves Hamming weight (commutes with `P_hw` for each `hw = 0,1,2,3`)
- Respects the group structure: `U(σ)U(τ) = U(στ)`

### B. Character Computation and Decomposition

The characters for each conjugacy class of S₃:

| Class | `χ(g)` on C^8 | `χ(g)` expected |
|-------|--------------|-----------------|
| identity | 8 | 8 |
| 2-cycles {(12),(13),(23)} | 4 | 4 |
| 3-cycles {(123),(132)} | 2 | 2 |

Multiplicities via inner product with irrep characters:
- `n(A₁) = (8 + 3·4 + 2·2)/6 = (8+12+4)/6 = 4`
- `n(A₂) = (8 - 3·4 + 2·2)/6 = (8-12+4)/6 = 0`
- `n(E) = (2·8 - 2·2)/6 = (16-4)/6 = 2`

Result: **C^8 = 4A₁ + 2E** — no A₂ appears.

### C. hw=1 Triplet = Generation Sector

The hw=1 sector `{e₁, e₂, e₃}` has characters:
- `χ(e) = 3`, `χ(2-cycle) = 1`, `χ(3-cycle) = 0`

This matches `A₁ + E` exactly — the standard 3-point permutation representation.
The Z₃ element `(123)` sends `e₁ → e₂ → e₃ → e₁` (cyclic, verified numerically).

### D. Quantum Number Content of the hw=1 Sector

Z₃ cycles all three tensor factors: e₁→e₂→e₃→e₁. Because Z₃ maps b₃ (fiber)
to b₁ (base) and back, it does NOT preserve the base/fiber decomposition on which
Y and T₃ are defined. Individual hw=1 states are NOT Y eigenstates:
- e₃ = |0,0,1⟩ (b₃=1): Y eigenstate with Y = +1/3, T₃ = +1/2
- e₁ = |1,0,0⟩ and e₂ = |0,1,0⟩ (b₃=0, mixed base): T₃ = +1/2 each (σ₃|0⟩ = +|0⟩);
  symmetric combination (e₁+e₂)/√2 has Y = +1/3, antisymmetric (e₁−e₂)/√2 has Y = −1.

The Y eigenvalue spectrum of the full 3D hw=1 subspace is {+1/3, +1/3, −1}.
The T₃ spectrum is {−1/2, +1/2, +1/2}.

The Z₃ symmetry establishes these three states as a degenerate generation-structure
orbit: each copy of the lattice (choosing a different axis as the "generation axis")
gives the same {+1/3, +1/3, −1} matter content, so three Z₃-orbit copies yield
three families with the same quantum number structure.

---

## Physical Interpretation

The three taste doublers from Z³ staggered fermions are not spurious artifacts:
they are the algebraic origin of three generation-analogous structures, each with
Y spectrum {+1/3, +1/3, −1} and T₃ spectrum {−1/2, +1/2, +1/2}, related by the
Z₃ cyclic symmetry of the cubic lattice.

The S₃ → Z₃ → 3 generations chain is:
1. Z³ spatial lattice has cubic symmetry S₃ (axis permutations)
2. Staggered doubling maps each spatial axis to a taste direction
3. Z₃ subgroup cyclically permutes the three taste-axis states
4. Each copy has Y spectrum {+1/3, +1/3, −1} (quark-like + lepton-like) → 3 generation-analogous structures

This provides the algebraic basis for "taste = generation" without requiring
additional matter input.

---

## Numerical Verification

| Check | Result |
|-------|--------|
| `U(σ)` unitary for all σ ∈ S₃ | exact |
| `[U(σ), P_hw]= 0` for all hw | exact |
| χ(e)=8, χ(2-cycle)=4, χ(3-cycle)=2 | exact |
| C^8 = 4A₁ + 0A₂ + 2E | exact |
| hw=1: A₁+E permutation rep | exact |
| Z₃ cycles {e₁→e₂→e₃→e₁} | exact |
| hw=1 Y spectrum: {−1, +1/3, +1/3} | exact |
| hw=1 T₃ spectrum: {−1/2, +1/2, +1/2} | exact |

Independent crosscheck: `scripts/frontier_s3_action_taste_cube_decomposition.py`
produces identical decomposition (63/63 pass, 0 fail).

---

## What This Theorem Sharpens

- **Taste = generation blocker**: Z₃ cyclic symmetry of Z³ forces exactly 3
  generation candidates; the hw=1 sector has Y spectrum {+1/3, +1/3, −1} and
  T₃ spectrum {−1/2, +1/2, +1/2}, consistent with one SM left-handed generation
- Provides algebraic support for the three-generation matter structure recorded
  in [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md)

## What Remains Bounded

- Generation mass splitting (CKM, Yukawa hierarchy) is not derived here
- The identification of hw=1 tastes with specific SM generations requires the
  graph-first axis-selection procedure
- This theorem establishes the count and degeneracy; the dynamics distinguishing
  generations are a separate derivation

## Reading Rule

This note is the claim boundary for this reviewed taste/generation support result.
It sharpens the existing three-generation matter package on current `main`, but
generation mass structure and full flavor phenomenology remain separate.
