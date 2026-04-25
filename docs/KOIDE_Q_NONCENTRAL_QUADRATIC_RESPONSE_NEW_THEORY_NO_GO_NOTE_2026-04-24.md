# Koide Q Noncentral Quadratic-Response New-Theory No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_noncentral_quadratic_response_new_theory_no_go.py`  
**Status:** conditional support theorem; executable no-go for retained closure

## Theorem Attempt

Try to replace central source bookkeeping with a live noncentral response law.
Let `A` be an off-block response operator between the charged-lepton plus block
and perp block.  The symmetrized positive response

```text
R(A) = A^T A + A A^T
```

has equal total plus/perp block trace for every off-block `A`.  If retained
charged-lepton physics made this the exclusive physical Q source generator,
then

```text
E_+ = E_perp
K_TL = 0
Q = 2/3
```

would follow without importing the Koide target.

## Exact Positive Support

For a real off-block response

```text
A = [[0, r1, r2],
     [l1, 0,  0 ],
     [l2, 0,  0 ]]
```

the runner verifies

```text
Tr_+(A^T A + A A^T) = l1^2+l2^2+r1^2+r2^2
Tr_perp(A^T A + A A^T) = l1^2+l2^2+r1^2+r2^2.
```

So the symmetrized noncentral quadratic response is exactly block-democratic.
This is a genuine support mechanism, not a restatement of `Q=2/3`.

## Retained Obstruction

The retained `C3` split is trivial plus real-standard perp.  The audit verifies:

```text
Hom_C3(plus,perp) = 0.
```

Equivalently, the retained `C3` commutant has no plus/perp cross block.  A
nonzero off-block `A` transforms as a source, not as a retained invariant
operator.

The second obstruction is exclusivity.  Even if `R(A)` is allowed, the old
central rank-visible determinant source remains algebraically admissible:

```text
W_full = log(1+k_plus)+2log(1+k_perp)
dW_full|0=(1,2)
K_TL=3/8
Q=1.
```

So the new mechanism closes Q only if retained physics also proves that central
rank-visible source language is inadmissible.

## Musk Simplification Pass

1. The positive mechanism is one trace identity:
   `Tr_+(R(A)) = Tr_perp(R(A))`.
2. The missing requirement is exclusive source admissibility, not another
   determinant formula.
3. A future proof must either retain the transforming off-block source law or
   derive it from the first-live `Gamma_1` carrier.
4. It must also forbid `W_full`; merely adding `R(A)` is insufficient.
5. The executable countertest is whether the central full determinant remains
   physical.

## Hostile Review

This is not a Koide closure.  It gives a promising new support theorem, but the
retained-status and exclusivity bridge is still missing.

The exact residual is:

```text
derive_exclusive_noncentral_quadratic_response_source_law
```

## Verdict

```text
KOIDE_Q_NONCENTRAL_QUADRATIC_RESPONSE_NEW_THEORY_NO_GO=TRUE
Q_NONCENTRAL_QUADRATIC_RESPONSE_NEW_THEORY_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_EXCLUSIVE_NONCENTRAL_QUADRATIC_SOURCE=TRUE
RESIDUAL_SCALAR=derive_exclusive_noncentral_quadratic_response_source_law
RESIDUAL_SOURCE=central_rank_visible_full_determinant_not_excluded
COUNTERSTATE=central_full_determinant_ratio_2_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_noncentral_quadratic_response_new_theory_no_go.py
python3 -m py_compile scripts/frontier_koide_q_noncentral_quadratic_response_new_theory_no_go.py
```
