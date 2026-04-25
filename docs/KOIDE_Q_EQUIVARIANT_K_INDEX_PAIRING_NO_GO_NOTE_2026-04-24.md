# Koide Q equivariant K-index pairing no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_equivariant_k_index_pairing_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use an equivariant `K`-theory or index pairing on the retained real `C_3`
carrier to force the label-counting center source:

```text
equivariant index -> equal center labels -> K_TL = 0.
```

## Executable theorem

An additive positive `K_0` pairing on the two central sectors has weights:

```text
(a,b).
```

The source-neutral leaf is:

```text
a = b.
```

Additivity alone supplies no equation selecting that subcone.

If the index pairing is strengthened to respect the retained real fusion rule,
then the doublet dimension `d` must obey:

```text
D tensor D = 2*1 + D
d^2 = d + 2.
```

The positive solution is:

```text
d = 2.
```

That is the rank/Hilbert dimension.  The label-count value `d=1` violates the
fusion equation.

## Consequence

Fusion/index dimension gives:

```text
weights = (1,2)
Q = 1
K_TL = 3/8.
```

Label counting gives:

```text
weights = (1,1)
Q = 2/3
K_TL = 0.
```

But label counting is not the retained monoidal/fusion index dimension.

## Residual

```text
RESIDUAL_SCALAR = label_counting_index_weight_minus_rank_fusion_weight
RESIDUAL_INDEX_PAIRING = additive_pairing_does_not_select_a_equals_b
```

## Why this is not closure

The `K`-theory/index route splits:

- additive index pairings leave the sector ratio free;
- fusion-compatible dimensions force rank weighting, not label weighting.

So the route does not derive the missing source law.

## Falsifiers

- A retained equivariant index pairing that is positive, physically coupled to
  the source carrier, and uniquely gives `(1,1)`.
- A theorem showing monoidal/fusion compatibility is not the relevant physical
  naturality condition for the charged-lepton source.
- A quotient-index theorem that discards rank while remaining independently
  forced by the retained structure.

## Boundaries

- Covers additive `K_0` pairings and fusion-compatible dimension characters.
- Does not exclude a future nonstandard quotient index with a separate physical
  derivation.

## Hostile reviewer objections answered

- **"Index theory could count sectors."**  It can, but additive sector counting
  is a choice among positive pairings.
- **"Fusion is too strong."**  If used, it selects rank dimension and moves away
  from the Koide leaf.
- **"Use quotient labels."**  That is again the missing physical source law.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_equivariant_k_index_pairing_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_EQUIVARIANT_K_INDEX_PAIRING_NO_GO=TRUE
Q_EQUIVARIANT_K_INDEX_PAIRING_CLOSES_Q=FALSE
RESIDUAL_SCALAR=label_counting_index_weight_minus_rank_fusion_weight
RESIDUAL_INDEX_PAIRING=additive_pairing_does_not_select_a_equals_b
```
