# Mass and Mixing Subspace Disjointness on the hw=1 Triplet

**Date:** 2026-04-17
**Status:** exact structural theorem
**Runners:**
- `scripts/frontier_mass_mixing_disjointness_theorem.py` (9 PASS, 0 FAIL)
- `scripts/frontier_charged_lepton_via_neutrino_hermitian.py` (14 PASS, 0 FAIL)

## Safe statement

On the retained `hw=1` three-generation Hermitian algebra
`M_3(ℂ)_Herm`, the subspace encoding charged-lepton mass eigenvalues
has **trivial intersection** with the subspace encoding neutrino-
mixing parameters:
```
dim(V_H ∩ V_D)  =  rank(V_H) + rank(V_D) − rank(V_H + V_D)
                =  3 + 3 − 6
                =  0.
```
Charged-lepton mass eigenvalues cannot be expressed as linear
combinations of neutrino-mixing sources. The charged-lepton closure
and the neutrino-mixing closure are architecturally independent
observational pins covering disjoint (intersection-zero) subspaces
of the retained Hermitian algebra.

**Scope note — disjointness vs. orthogonality.** The theorem proves
`dim(V_H ∩ V_D) = 0`, which is **trivial intersection** (the
subspaces are linearly independent / in direct sum). It does NOT
prove that `V_H` and `V_D` are **orthogonal** with respect to any
Hermitian inner product on `M_3(ℂ)_Herm` (e.g., the Hilbert-Schmidt
inner product `⟨A, B⟩ = Tr(A^† B)`). Trivial-intersection is the
weaker, strictly algebraic statement; orthogonality is a
stronger, metric-dependent statement that is NOT established here.

This note uses "disjoint" throughout to refer to the trivial-
intersection / direct-sum property. Earlier formulations using
"orthogonal" were imprecise and have been revised.

## Retained inputs

- [DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md):
  `U_e = I_3` constraint — charged-lepton mass basis coincides with
  the generation axis basis on the retained surface.
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md):
  retained `hw=1` Hermitian algebra `M_3(ℂ)` (9 real dimensions).

## Construction

### The mixing tangent space V_H

The retained neutrino-mixing Hermitian chart on the `hw=1` triplet
is the affine family
```
H(m, δ, q_+)  =  H_base  +  m T_m  +  δ T_δ  +  q_+ T_q
```
where the generators are (in the generation-axis basis):
```
T_m = [[1, 0, 0], [0, 0, 1], [0, 1, 0]]          (axis-2 ↔ axis-3 swap plus diagonal)
T_δ = [[0, −1,  1], [−1, 1, 0], [ 1, 0, −1]]     (antisymmetric off-diagonal + diag trace)
T_q = [[0,  1,  1], [ 1, 0, 1], [ 1, 1,  0]]     (symmetric off-diagonal, no diag)
```
and `H_base` is a fixed Hermitian matrix carrying the retained
`γ = 1/2`, `E_1 = √(8/3)`, `E_2 = √8/3` amplitudes.

Define
```
V_H  ≡  span_ℝ {T_m, T_δ, T_q}   ⊂  M_3(ℂ)_Herm.
```
The three generators are linearly independent over ℝ; `rank(V_H) = 3`.

### The charged-lepton mass subspace V_D

By the retained Dirac-bridge theorem, the charged-lepton effective
mass operator on `T_1` is diagonal in the generation axis basis:
`U_e = I_3`. Its eigenvalues are the three charged-lepton masses,
which live on the species-diagonal subspace spanned by the three
rank-1 generation projectors:
```
D_1 = diag(1, 0, 0),   D_2 = diag(0, 1, 0),   D_3 = diag(0, 0, 1).
```
Define
```
V_D  ≡  span_ℝ {D_1, D_2, D_3}   ⊂  M_3(ℂ)_Herm.
```
`rank(V_D) = 3`.

## Theorem 3: subspace disjointness

**Theorem 3.** On the retained `hw=1` Hermitian algebra `M_3(ℂ)_Herm`:
```
rank(V_H + V_D)  =  6,
dim(V_H ∩ V_D)   =  3 + 3 − 6  =  0.
```

*Proof.* Construct the 6 × 9 real matrix `A` whose rows are
`vec(T_m), vec(T_δ), vec(T_q), vec(D_1), vec(D_2), vec(D_3)`.
Compute the rank (over ℝ) of `A`:

- `vec(D_i)` are the three unit-vectors on the diagonal entries of
  `M_3(ℂ)_Herm`.
- `vec(T_m)` contributes `(1, 0, 0; 0, 0, 1; 0, 1, 0)`. Its trace is 1
  (diagonal `(1, 0, 0)`), but its off-diagonal part
  `(0, 0, 1; 0, 1, 0)` is independent of the diagonal part of
  `V_D`.
- `vec(T_δ)` contributes
  `(0, −1, 1; −1, 1, 0; 1, 0, −1)`. Its trace is 0, diagonal part is
  `(0, 1, −1)` (a trace-zero diagonal combination), and off-diagonal
  part is antisymmetric.
- `vec(T_q)` contributes
  `(0, 1, 1; 1, 0, 1; 1, 1, 0)`. Its trace is 0, diagonal part is
  zero, and off-diagonal part is symmetric.

Linear independence check: the 6 rows of `A` are linearly
independent in the 9-dimensional ambient Hermitian space, hence
`rank(A) = 6`. By dimension counting,
`dim(V_H ∩ V_D) = 3 + 3 − 6 = 0`. □

**Direct verification.** Suppose `α T_m + β T_δ + γ T_q = a D_1 + b D_2 + c D_3`
for some real coefficients. Examining the off-diagonal entries:
- `(1,2)` entry: `−β + γ = 0`, so `β = γ`.
- `(1,3)` entry: `β + γ = 0`, so `β = −γ`.
Combining: `β = γ = 0`. Then the remaining constraint
`α T_m = a D_1 + b D_2 + c D_3` requires the off-diagonal part of
`α T_m` to vanish, which needs `α = 0`. Hence the only solution is
trivial, and the intersection is `{0}`. □

## Corollary: charged-lepton closure and neutrino-mixing closure are
architecturally independent

Since `V_H ∩ V_D = {0}` on the retained Hermitian algebra (trivial
intersection, not orthogonality in any metric sense), the charged-
lepton mass eigenvalues (which live in `V_D` by `U_e = I_3`) cannot
be expressed as linear combinations of neutrino-mixing sources.
Equivalently: observational pinning of the neutrino-mixing chart
`H(m, δ, q_+)` does NOT fix the charged-lepton mass eigenvalues. The
charged-lepton hierarchy is not derivable as a corollary of the
neutrino-mixing closure.

**Architectural decomposition.** The retained `M_3(ℂ)_Herm` (9 real
dimensions) admits a direct-sum decomposition (as ℝ-vector spaces,
not necessarily orthogonal under any particular inner product)
```
M_3(ℂ)_Herm  =  V_H  ⊕  V_D  ⊕  V_{complement}
```
with `dim(V_H) = dim(V_D) = 3` and
`dim(V_{complement}) = 9 − 6 = 3`, where `V_{complement}` is a
choice of linear complement to `V_H + V_D`. The neutrino-mixing closure pins
`V_H` via observational PMNS angles; the charged-lepton closure
pins `V_D` via observed charged-lepton masses. The 3-real
complementary subspace (containing Hermitian modes not in `V_H + V_D`)
is not observationally pinned by either closure.

## Numerical cross-check

At the neutrino-mixing observational pin
`(m_*, δ_*, q_+*) = (0.657, 0.934, 0.715)`, the retained Hermitian
`H(m_*, δ_*, q_+*)` has eigenvalue triple
`(−1.309, −0.320, +2.287)`. Cosine similarity to the observed
charged-lepton mass-square-root direction
`(√m_e, √m_μ, √m_τ)/||·|| = (0.0165, 0.2369, 0.9713)`:
- Eigenvalue reading (`m_i = |λ_i|`): 0.884
- Eigenvalue-squared reading (`m_i = λ_i²`): 0.956
Neither reaches the 0.99 threshold for a structural match. An
80-restart Nelder-Mead chamber search confirms no interior pin
`(m, δ, q_+)` reproduces the charged-lepton direction AND saturates
Koide simultaneously.

This is the numerical manifestation of Theorem 3: the neutrino-mixing
chart and the charged-lepton mass subspace are structurally
decoupled.

## What this does not claim

- Theorem 3 does NOT claim the charged-lepton closure is unreachable
  by any means. It claims only that the charged-lepton mass
  hierarchy is not a corollary of the neutrino-mixing closure. The
  charged-lepton closure proceeds via its own observational pin on
  `V_D` (Theorem 7 in
  [CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md](./CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)).
- The 3-real complementary subspace is not characterized
  here; it may contain structure relevant to future framework-derives
  attempts.
- Theorem 3 establishes **disjointness** (trivial intersection /
  direct sum as ℝ-vector spaces), NOT **orthogonality**. No metric
  or Hermitian inner product is invoked. Earlier wording of this
  note that called the subspaces "orthogonal" was imprecise and
  has been revised.

## Paper-safe wording

> On the retained `hw=1` three-generation Hermitian algebra, the
> neutrino-mixing tangent subspace `V_H = span{T_m, T_δ, T_q}` and
> the charged-lepton mass subspace `V_D = span{D_1, D_2, D_3}`
> satisfy `rank(V_H + V_D) = 6`, hence `dim(V_H ∩ V_D) = 0`. The two
> sector closures are structurally independent observational pins
> on disjoint subspaces of the retained Hermitian algebra.
> Disjointness here means trivial intersection (direct sum as
> ℝ-vector spaces); it is strictly weaker than orthogonality under
> any particular Hermitian inner product, which is not claimed.

## Dependency contract

- `scripts/frontier_three_generation_observable_theorem.py` PASS on
  live `main`.
- `scripts/frontier_dm_neutrino_dirac_bridge_theorem.py` PASS on
  live `main`.

## Status

**REVIEW.**
