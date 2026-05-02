# Hierarchy Matsubara Determinant — Narrow Algebraic Theorem

**Date:** 2026-05-02
**Type:** positive_theorem (proposed; audit-lane to ratify)
**Primary runner:** `scripts/frontier_hierarchy_matsubara_determinant_narrow.py`

## Claim scope (proposed)

> On the minimal spatial APBC block `L_s = 2` of the staggered Dirac
> operator on `Z⁴`, with the mean-field gauge factorization (admitted
> standard mean-field convention; cycle 7 setup), all spatial momenta
> are pinned at the Brillouin-zone corners (`sin²(k_i) = 1` for `i ∈
> {1,2,3}`). The full APBC determinant has the **exact closed form**:
> ```
> |det(D + m)|  =  ∏_ω  [m² + u_0² (3 + sin²ω)]⁴
> ```
> where the product runs over temporal APBC Matsubara momenta
> `ω_n = (2n+1)π/L_t` for `n = 0, 1, ..., L_t − 1`.

The narrow theorem **explicitly does NOT** claim:

- the physical electroweak order parameter (separate downstream);
- a Higgs-mass prediction or `m_H = v / (2 u_0)` derivation;
- the temporal-averaging selection that would identify the physical
  EWSB observable;
- the value of `u_0` (admitted external lattice mean-field input).

The result is a **pure determinant identity** on the staggered Dirac
operator at minimal block size with admitted mean-field factorization.

## Admitted dependencies

| Authority | Role |
|---|---|
| Cl(3) Clifford identity `D_taste² = d · I` | admitted standard staggered fermion algebra; gives the eigenvalue magnitudes per taste |
| Mean-field factorization `U_{ab} → u_0 δ_{ab}` | admitted standard mean-field convention; scales eigenvalues by `u_0` |
| `L_s = 2` minimal APBC block | admitted block-size choice; pins spatial momenta to BZ corners (`sin²(k_i) = 1`) |
| Standard staggered Dirac dispersion `λ²(k, ω) = u_0² Σ_μ sin²(k_μ)` | admitted standard staggered fermion algebra; gives the eigenvalue formula at general `(k, ω)` |

The deps are admitted standard staggered fermion algebra + the same
mean-field setup used in cycle 7 (PR #302). No external authority is
load-bearing for the algebraic identity itself.

## Load-bearing step (class A)

```text
Setup: staggered Dirac operator D on Z⁴ APBC (anti-periodic temporal)
       with mean-field gauge factorization U_{ab} → u_0 δ_{ab}.
       Spatial: L_s = 2 → spatial momenta k_i ∈ {π/2}, so sin²(k_i) = 1.
       Temporal: ω_n = (2n+1)π/L_t for n = 0, …, L_t − 1.

Standard staggered Dirac dispersion at mean field:
  λ²(k, ω) = u_0² · [Σ_i sin²(k_i) + sin²(ω)]
          = u_0² · [3 + sin²(ω)]      at L_s = 2

For each ω, the operator (D + m) has 4 taste-degenerate eigenvalues:
  λ_taste(k, ω) = m + i · sqrt[u_0² (3 + sin²ω)]   (4-fold degenerate)
  λ_taste-bar = m − i · sqrt[u_0² (3 + sin²ω)]    (4-fold degenerate)

|det(D + m) at fixed ω| = ∏_taste |λ_taste|² · |λ_taste-bar|²
                       = [m² + u_0²(3 + sin²ω)]⁴

Total APBC determinant:
  |det(D + m)|_full = ∏_ω [m² + u_0²(3 + sin²ω)]⁴.    ∎
```

This is class (A) — algebraic identity on admitted standard
staggered fermion eigenvalue structure.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_matsubara_determinant_narrow.py
```

Verifies, at exact rational precision via Python `Fraction` and `sympy`:

1. The dispersion `λ²(k, ω) = u_0² Σ sin²(k_μ)` reduces to
   `u_0² (3 + sin²ω)` at `L_s = 2`.
2. The 4-fold taste degeneracy gives `|det(D + m)|_per-ω =
   [m² + u_0²(3 + sin²ω)]⁴`.
3. Total APBC determinant matches the product over `L_t` Matsubara
   modes for `L_t ∈ {2, 3, 4}` (small cases tractable in exact arithmetic).
4. The closed form is exact (matches direct matrix evaluation at
   tested `(L_t, m, u_0)` values).

## Independent audit handoff

```yaml
proposed_claim_type: positive_theorem
proposed_claim_scope: |
  Pure algebraic determinant identity for the staggered Dirac operator
  on Z^4 APBC at L_s = 2 with mean-field gauge factorization:
  |det(D + m)| = prod_omega [m^2 + u_0^2 (3 + sin^2 omega)]^4. NO physical
  EWSB order-parameter identification, NO m_H prediction.
proposed_load_bearing_step_class: A
status_authority: independent audit lane only
```

The narrow theorem is class (A) algebraic on admitted-standard staggered
fermion algebra. The independent audit lane will evaluate the load-bearing
class and any later status.

## What this theorem closes

The exact algebraic determinant identity on the minimal block, freed
from the conditional physical-electroweak-order-parameter selection
identified in prior review of the parent row.

## What this theorem does NOT close

- Physical EWSB order-parameter identification (separate downstream).
- m_H = v / (2 u_0) Higgs mass derivation (separate; lattice→physical
  matching cluster obstruction).
- Choice of temporal averaging that identifies the physical observable
  (separate downstream).
- The value of `u_0` (admitted external lattice mean-field input).

## Cross-references

- `HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md` — parent; this narrow
  theorem carves out the algebraic determinant identity.
- Cycle 7 / PR #302 — sister narrow theorem on Higgs lattice eigenvalue
  ratio (related mean-field admission).
- Cycles 1-11 — sister narrow theorems / source-note edits / audit
  companions on different lanes.
