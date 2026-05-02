# Electromagnetic Coupling e = g sin(θ_W) = g' cos(θ_W) from EWSB Pattern

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on cycle 18 (EWSB
pattern Q = T_3 + Y/2). NOT proposed_retained.
**Primary runner:** `scripts/frontier_em_coupling_from_ewsb.py`

## 0. Statement

**Theorem.** Given:
1. EWSB pattern Q = T_3 + Y/2 (cycle 18, PR #281);
2. Photon-fermion coupling form `e Q ψ̄γ^μψ A_μ` (admitted SM convention);
3. EW gauge-boson mixing parameterized by Weinberg angle θ_W:
   - A_μ = sin(θ_W) W_μ^3 + cos(θ_W) B_μ
   - Z_μ = cos(θ_W) W_μ^3 − sin(θ_W) B_μ;

then the electromagnetic coupling satisfies:

```text
e  =  g sin(θ_W)  =  g' cos(θ_W),
```

equivalently `tan(θ_W) = g'/g`.

**Proof.** The fermion-gauge coupling from D_μ = ∂_μ − i g T^a W_μ^a − i g' (Y/2) B_μ
yields:
```text
−i (g T_3 W_μ^3 + g' (Y/2) B_μ)
```

Substituting W_μ^3 = sin(θ_W) A_μ + cos(θ_W) Z_μ and B_μ = cos(θ_W) A_μ − sin(θ_W) Z_μ:
```text
A_μ coefficient:  g T_3 sin(θ_W) + g' (Y/2) cos(θ_W)
Z_μ coefficient:  g T_3 cos(θ_W) − g' (Y/2) sin(θ_W)
```

For the A_μ coefficient to equal `e Q = e (T_3 + Y/2)`:
```text
g sin(θ_W)  =  e        (matching T_3 coefficient)
g' cos(θ_W) =  e        (matching Y/2 coefficient)
```

So `e = g sin(θ_W) = g' cos(θ_W)`. ∎

Equivalently: tan(θ_W) = g'/g (consistent with cycle 19 sin²θ_W^GUT = 3/8 and cycle 21 cos²θ_W = M_W²/M_Z²).

## 1. Z-coupling structure

The Z-coupling from the same calculation:
```text
g_Z  =  g cos(θ_W) − g' sin(θ_W)·(Y/2 / T_3)  ...
```
After grouping, the standard result is:
```text
Z_μ coupling  =  (g/cos(θ_W)) (T_3 − Q sin²(θ_W))
```

This is the SM-standard Z-coupling form, derivable from cycle 18 + admitted SM gauge structure.

## 2. Status

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on cycle 18 (EWSB) + admitted SM gauge-boson mixing
  parameterization + admitted photon-fermion coupling form.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 3. What this closes

- **e = g sin(θ_W) = g' cos(θ_W)** from cycle 18 + admitted SM gauge structure
- **Z-coupling form Z_μ ∝ (T_3 − Q sin²θ_W)** as immediate consequence

## 4. Cross-references

- Cycle 18 / PR #281 — EWSB pattern Q = T_3 + Y/2
- Cycle 19 / PR #282 — sin²θ_W^GUT = 3/8 (sister)
- Cycle 21 / PR #284 — M_W²/M_Z² = cos²θ_W (sister)
