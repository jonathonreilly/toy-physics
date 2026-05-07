# Block B — Cl(3)-Derived Kogut-Susskind Hamiltonian (3+1 Picture)

**Date:** 2026-05-07
**Type:** working block-derivation note (intermediate); superseded for
synthesis purposes by [`UNIFIED_BRIDGE_STATUS_2026_05_07.md`](UNIFIED_BRIDGE_STATUS_2026_05_07.md)
and [`LANE_UNLOCK_CONSOLIDATION_2026_05_07.md`](LANE_UNLOCK_CONSOLIDATION_2026_05_07.md).
**Authority role:** source-note proposal. Audit verdict and downstream
status are set only by the independent audit lane.

## B.1 General form forced by primitives

A local Hamiltonian on Z³ with Cl(3) at each site, demanding:
- **Tr-form invariance** (`Tr(T_a T_b) = δ_ab/2`)
- **Reflection positivity** in emergent time
- **Locality** (terms supported on bounded subcomplexes)
- **Single-clock dynamics** (Lieb-Robinson causal structure)
- **SU(3) gauge invariance** on the 3D symmetric base (derived)

must take the form

```
H  =  c_E · Σ_e   Ĉ_2(e)              "electric" / link-Casimir
    + c_M · Σ_p   M̂(U_p)              "magnetic" / spatial-plaquette
    + (higher-locality terms)
```

where `e` runs over spatial links of Z³, `p` over spatial plaquettes, and
the higher-locality terms are at minimum 6-link (cube). The ellipsis is
NOT a wildcard — Lieb-Robinson + canonical Tr-form bound the coefficients
of higher-locality terms to be irrelevant in the long-wavelength limit
(this is the standard relevance argument; valid here because Tr-form
fixes the dimension of operators).

## B.2 What is forced

| Coefficient / Form | Status | Reason |
|---|---|---|
| `Ĉ_2(e)` is the unique link operator | **forced** | Tr-form gives a unique quadratic invariant on each link |
| `c_E ≥ 0` | **forced** | RP / spectrum-bounded-below |
| `c_M ≥ 0` | **forced** | RP / hermiticity of magnetic term |
| Single coupling `g²` controlling both | **forced under canonical Tr-form (open gate g_bare=1)** | If `c_E = g²/(2a)` and `c_M = 1/(g² a)`, the canonical Tr-form fixes `g² = 1` modulo the open `g_bare` gate |
| Sum-over-plaquettes locality | **forced** | locality + RP |

## B.3 What is NOT forced — the residual freedom

The class function `M̂(U_p)` on SU(3) is not pinned by Cl(3) primitives.
Class functions on SU(3) are spanned by characters `{χ_λ}`. Hermitian
class functions are real linear combinations:

```
M̂(U_p)  =  Σ_λ  m_λ  Re χ_λ(U_p),    m_λ ∈ ℝ.
```

The framework's primitives constrain `{m_λ}` only via:
- M̂(I) ≥ M̂(U) for all U (positive semi-definiteness around identity)
- Hermiticity (`m_λ = m_{λ*}`, i.e., `m_(p,q) = m_(q,p)`)
- Continuum limit `(1/2g²) Tr F²` matching at lowest order in `X = log U`

The continuum-limit constraint pins **only the leading combination**:
`Σ_λ m_λ d_λ C_2(λ) = (1/g²) · k`

for some constant `k` from the spatial volume normalization. This is
**one linear constraint on infinitely many `{m_λ}`**.

## B.4 The natural Cl(3)-canonical choice

The **Cl(3)-Tr-form-canonical** simplest M̂ is obtained by demanding:
1. M̂ vanishes at identity (zero curvature → zero energy)
2. M̂ involves only the lowest non-trivial irrep
3. M̂ is real (combine `χ_λ` with `χ_{λ*}`)

This gives a **two-parameter** family on the lowest non-trivial irreps:

```
M̂(U_p)  =  α  ·  [N_c  −  Re χ_(1,0)(U_p)]
       +  β  ·  [d_(1,1)  −  χ_(1,1)(U_p)]   (next-to-leading)
       +  ...
```

with `α + β·d_(1,1)·C_2(1,1)/C_2(1,0)·... = 1` from continuum matching.

The **single-irrep choice α = 1, β = 0, ...** is a NATURAL but not
forced first cut. It's mathematically equivalent to "Wilson at the
Hamiltonian level" — but with a crucial difference:

- 4D Lagrangian Wilson is `S = β·Σ_{all plaquettes} Re Tr U_p`
- 3+1 Hamiltonian "Wilson" is `M̂ = (1/N_c) Re Tr U_p` ONLY on **spatial**
  plaquettes; temporal Trotter weights are induced, not chosen.

## B.5 The first-principles claim

**Proposition (Block B claim).** Under A1+A2 + canonical Tr-form +
RP + locality + the open `g_bare = 1` gate, the framework forces the
**electric sector** of `H` exactly (link Casimir, single coupling), and
the **magnetic sector** to be supported on closed-loop class functions
of SU(3) constrained by one linear continuum-matching equation. The
single-irrep choice (`α=1, β=0, ...`) is the most parsimonious
representative; it gives the standard Kogut-Susskind Hamiltonian:

```
H_KS,Cl(3)  =  (1/(2 a))  Σ_e   Ĉ_2(e)
           −  (1/a)  Σ_p   (1/N_c) Re Tr U_p
```

at canonical `g² = 1, N_c = 3`.

This is **substantially more constrained than the 4D Lagrangian
ambiguity**:
- 4D Wilson / Heat-kernel / Manton differ at finite β by 5-10%.
- 3+1 Hamiltonian: the differences correspond to operator-ordering
  / Trotter choices, which **vanish in ground-state observables**.

## B.6 The single physical observable

The spatial plaquette ground-state expectation:

```
⟨P⟩_KS  ≡  ⟨0_KS | (1/N_c) Re Tr U_p | 0_KS⟩
```

is computed with `H_KS,Cl(3)` at `g² = 1`. **This is a single number
with no convention freedom, modulo the residual `α, β, ...` choice.**

Block C computes this number for the canonical (`α=1, β=0`) choice on
the smallest non-trivial volume, then extrapolates.
