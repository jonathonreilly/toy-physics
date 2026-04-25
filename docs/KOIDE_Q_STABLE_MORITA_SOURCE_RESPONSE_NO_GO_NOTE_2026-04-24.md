# Koide Q Stable Morita Source-Response No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_stable_morita_source_response_no_go.py`  
**Status:** conditional support theorem; executable no-go for retained closure

## Theorem Attempt

Try to promote the Morita-normalized determinant from arithmetic support to a
physical source-response uniqueness theorem.  If the charged-lepton source
generator is invariant under stable matrix amplification, then a rank-two
matrix block is dummy Morita amplification, not a physical source multiplicity:

```text
a(2) = a(1).
```

With scalar normalization `a(1)=1`, this gives:

```text
dW|0 = (1,1)
K_TL = 0
Q = 2/3.
```

## Brainstormed Variants

1. Stable Morita source-response: matrix amplification is dummy.
2. Full equivariant rank source: matrix rank is physical multiplicity.
3. What if stable Morita invariance is a retained physical law?  Then Q closes.
4. What if rank/orbit type remains source-visible?  The full determinant is an exact counterstate.
5. Coefficient-ratio formulation: `K_TL=0` iff `a2=a1`.

## Exact Audit

The generic determinant-source generator is:

```text
W = a1 log(1+k_plus) + a2 log(1+k_perp).
```

Therefore:

```text
dW|0 = (a1,a2)
weights = (a1/(a1+a2), a2/(a1+a2)).
```

The runner verifies:

```text
K_TL=0 <=> a2=a1.
```

The stable Morita law supplies the closing specialization:

```text
a1=a2=1 -> weights=(1/2,1/2) -> Q=2/3.
```

But the retained equivariant-rank source remains:

```text
a1=1, a2=2 -> weights=(1/3,2/3) -> Q=1, K_TL=3/8.
```

## Hostile Review

This does not close Q from retained data.  It names the exact law still
missing:

```text
derive_stable_Morita_source_response_over_equivariant_rank_source.
```

Without that theorem, the rank-two block can still be read as physical
source-visible multiplicity.

## Verdict

```text
KOIDE_Q_STABLE_MORITA_SOURCE_RESPONSE_NO_GO=TRUE
Q_STABLE_MORITA_SOURCE_RESPONSE_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_STABLE_MORITA_SOURCE_RESPONSE_IS_PHYSICAL=TRUE
RESIDUAL_SCALAR=derive_stable_Morita_source_response_over_equivariant_rank_source
RESIDUAL_Q=equivariant_rank_full_determinant_counterstate_not_excluded
COUNTERSTATE=equivariant_rank_logdet_w_plus_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_stable_morita_source_response_no_go.py
python3 -m py_compile scripts/frontier_koide_q_stable_morita_source_response_no_go.py
```
