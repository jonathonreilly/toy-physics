# Koide Q Refinement-Naturality Source No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_refinement_naturality_source_no_go.py`  
**Status:** conditional support theorem; executable no-go for retained closure

## Theorem Attempt

Try to derive the intensive source law from a naturality principle:
independent dummy refinements inside a center component should not change the
physical source weight of that component.  If the retained rank difference
`1:2` is only dummy refinement, this forces the source convention exponent to
zero and gives

```text
w_plus = w_perp = 1/2
K_TL = 0
Q = 2/3.
```

## Brainstormed Variants

1. Treat internal rank as dummy Morita refinement: independent block
   amplification must not affect source weights.
2. Treat internal rank as physical rank-one refinement: uniform refined atoms
   give rank weights.
3. What if only common amplification is dummy?  Then every rank exponent
   survives, since common scaling preserves ratios.
4. What if independent amplification is allowed only after quotienting the
   source language?  Then this reduces to the prior quotient-language
   factorization no-go.
5. What if additivity and dummy-invariance are both imposed?  They conflict
   unless one first classifies which refinements are physical source atoms.

Ranking:

```text
1. independent dummy-refinement invariance: strongest conditional closure
2. quotient-language factorization: already audited as conditional
3. common-amplification invariance: too weak
4. physical rank-one additivity: exact retained counterstate
5. arbitrary exponent prior: only repackages the residual scalar
```

## Exact Scalar

The runner uses the rank-exponent family

```text
w_perp / w_plus = 2^alpha.
```

Then

```text
alpha = 0 -> w=(1/2,1/2), K_TL=0, Q=2/3
alpha = 1 -> w=(1/3,2/3), K_TL=3/8, Q=1.
```

Because `2^alpha` is positive,

```text
K_TL = 0 <=> 2^alpha = 1 <=> alpha = 0.
```

## Two Naturalities

Rank-one refinement additivity says each retained rank-one refined atom has
equal measure.  With ranks `(1,2)`, this gives

```text
w=(1/3,2/3)
K_TL=3/8
Q=1.
```

Independent dummy-refinement invariance says amplifying only the plus block by
two should not change the component source ratio.  In the exponent family:

```text
base ratio = 2^alpha
amplified ratio = 1^alpha
invariance => alpha = 0.
```

Thus the positive route is real but conditional: it assumes the rank/orbit-size
difference is source-blind dummy refinement.

## Musk Simplification Pass

1. Make requirements less wrong: the issue is not a new Koide identity; it is
   whether rank refinement is physical or dummy for sources.
2. Delete: all structure reduces to the rank pair `(1,2)` plus one exponent
   `alpha`.
3. Simplify: one scalar identity `2^alpha=1` is the entire closing condition.
4. Accelerate: test independent dummy amplification against rank-one
   additivity directly.
5. Automate: add the refinement residual to the common residual atlas.

## Hostile Review

This is not a retained closure.  The current retained package contains the
rank/orbit-size distinction and the rank-additive state.  The proof closes Q
only after declaring that distinction source-blind for physical preparation.
That declaration is the missing primitive:

```text
derive_rank_refinement_source_blindness_over_rank_additivity.
```

## Verdict

```text
KOIDE_Q_REFINEMENT_NATURALITY_SOURCE_NO_GO=TRUE
Q_REFINEMENT_NATURALITY_SOURCE_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_RANK_REFINEMENT_IS_SOURCE_BLIND=TRUE
RESIDUAL_SCALAR=derive_rank_refinement_source_blindness_over_rank_additivity
RESIDUAL_Q=rank_additive_source_state_not_excluded
COUNTERSTATE=rank_refinement_alpha_1_w_plus_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_refinement_naturality_source_no_go.py
python3 -m py_compile scripts/frontier_koide_q_refinement_naturality_source_no_go.py
```
