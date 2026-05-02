# Taste-Scalar Fermion Coleman-Weinberg Isotropy — Narrow Theorem

**Date:** 2026-05-02
**Type:** positive_theorem (proposed; audit-lane to ratify)
**Primary runner:** `scripts/frontier_taste_scalar_fermion_cw_isotropy_narrow.py`

## Claim scope (proposed)

> On `ℂ⁸ = (ℂ²)^{⊗3}` with commuting taste-shift involutions `S_i = σ_x ⊗ I ⊗ I, I ⊗ σ_x ⊗ I, I ⊗ I ⊗ σ_x` and the linear taste Hamiltonian
> `H(φ) = Σ_i φ_i S_i`, the one-loop fermion Coleman-Weinberg Hessian
> at the axis-aligned electroweak minimum `φ = (v, 0, 0)` (with `v ≠ 0`) is
> exactly isotropic:
> ```
> ∂²V_f / ∂φ_i ∂φ_j  =  δ_{ij} · C(v)
> ```
> for any smooth `f` such that `V_f(φ) = Σ_s f(λ_s(φ)²)`.

The narrow scope is **purely the fermion Coleman-Weinberg isotropy
identity** at the retained taste block. The audit row's previously-named
"claim boundary until fixed" was: *"the exact isotropy theorem closes for
the fermion Coleman-Weinberg block."* This narrow theorem is that exact
safe scope.

The narrow theorem **does not** claim:

- gauge-loop or scalar-loop contributions to the Hessian (these use
  separate split models that are bounded — out of scope here);
- electroweak phase-transition consequences (separate downstream);
- Higgs-mass splitting from any non-fermionic source (separate);
- a Standard-Model Higgs-sector prediction.

## Retained / admitted dependencies

| Authority | Effective status | Role |
|---|---|---|
| (none, formally) | — | The theorem is purely algebraic on the binary product space `ℂ⁸ = (ℂ²)^{⊗3}` with `σ_x` shift operators — no external authority is load-bearing. |

The note operates on the abstract Cl(3)/Z³ taste-cube structure. While
this structure is the framework's setup, the load-bearing step does not
depend on any specific cited authority — it's an algebraic identity on
binary products of σ_x operators.

## Load-bearing step (class A)

```text
Setup: C^8 = (C^2)^{⊗3}, basis |s_1, s_2, s_3⟩ with s_i ∈ {0, 1}.
Operators: S_i = σ_x acting on tensor factor i.
Eigenvalue: S_i |s⟩ = (-1)^{s_i} |s⟩ in the σ_z eigenbasis.
            (i.e., we use the eigenbasis where S_i is diagonal — by
             commuting σ_z with σ_x via the basis rotation, but the
             formal identity holds in any basis.)

H(φ) = Σ_i φ_i S_i  →  λ_s(φ) = Σ_i φ_i (-1)^{s_i}    [exact eigenvalue]

At φ = (v, 0, 0):  λ_s(v, 0, 0) = v · (-1)^{s_1}, so |λ_s| = v ∀s.
                   Therefore  f(λ_s²) = f(v²)  ∀s.

Hessian:
    ∂²V_f / ∂φ_i ∂φ_j |_{φ=(v,0,0)}
       = Σ_s [ 2 f'(λ_s²) (∂λ_s/∂φ_i)(∂λ_s/∂φ_j)
              + 2 λ_s f''(λ_s²) λ_s (∂λ_s/∂φ_i)(∂λ_s/∂φ_j) ... ]
         simplified at λ_s² = v² uniform:
       = [coeff in v] · Σ_s (-1)^{s_i} · (-1)^{s_j}

Binary orthogonality sum:
    Σ_{s ∈ {0,1}^3} (-1)^{s_i} · (-1)^{s_j}
       = (Σ_{s_i ∈ {0,1}} (-1)^{2 s_i}) · (Σ_{s_j ≠ i} 1) · 4   if i = j
       = 8 · δ_{ij}                                           [exact]

Therefore Hessian = δ_{ij} · C(v) where C(v) absorbs the 8 and the
f-derivatives.   ∎
```

This is class (A) — algebraic identity on binary product structure.
No external authority is load-bearing.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_taste_scalar_fermion_cw_isotropy_narrow.py
```

Verifies, at exact rational precision via Python `Fraction`:

1. Binary orthogonality sum `Σ_s (-1)^{s_i}(-1)^{s_j} = 8 δ_{ij}` for all
   pairs `(i, j) ∈ {1, 2, 3}²`.
2. Eigenvalue `λ_s(φ) = Σ_i φ_i (-1)^{s_i}` is exact for any φ.
3. At `φ = (v, 0, 0)`: `λ_s² = v²` uniformly across all 8 basis states
   (verified for `v ∈ {1, 2, -3, 7/11}`).
4. Hessian off-diagonal `∂²/∂φ_i ∂φ_j` for `i ≠ j` evaluates to 0 at
   the axis-aligned minimum (concrete numerical test for several `f`
   choices: `f(x) = x`, `f(x) = x²`, `f(x) = log(1 + x)`).
5. Hessian diagonal `∂²/∂φ_i ∂φ_i` evaluates to a nonzero common value.

## Audit-lane disposition (proposed)

```yaml
target_claim_type: positive_theorem
proposed_claim_scope: |
  Pure algebraic isotropy identity for one-loop fermion Coleman-Weinberg
  Hessian on Cl(3)/Z³ taste block at axis-aligned electroweak minimum.
  Gauge-loop, scalar-loop, EW-phase-transition, and Higgs-sector
  consequences explicitly out of scope.
proposed_load_bearing_step_class: A
audit_required_before_effective_retained: true
```

If ratified, `effective_status = retained` (positive_theorem +
audited_clean + no upstream chain — the load-bearing identity is
self-contained algebra on binary products).

## What this theorem closes

The exact fermion Coleman-Weinberg isotropy half of the parent
`TASTE_SCALAR_ISOTROPY_THEOREM_NOTE` (`audit_status: audited_conditional`,
td=291). The parent's audit verdict named exactly this safe scope.

## What this theorem does NOT close

- Gauge-loop Hessian contributions (separate bounded model).
- Scalar-loop Hessian contributions (separate bounded model).
- Electroweak phase transition or thermal scalar-cubic (separate bounded).
- The full Higgs-sector spectrum (separate).

## Cross-references

- `TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md` — parent
  (`audit_status: audited_conditional`, td=291); this narrow theorem
  carves out the fermion CW isotropy half cleanly.
- Cycles 1-7 (PRs #292-302) — sister narrow theorems on different lanes.
