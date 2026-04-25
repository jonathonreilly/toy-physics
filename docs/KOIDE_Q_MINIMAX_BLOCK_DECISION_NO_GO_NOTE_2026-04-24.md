# Koide Q minimax block-decision no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_minimax_block_decision_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Test whether a decision-theoretic minimax/proper-scoring principle over the
retained singlet/doublet quotient forces equal block totals, thereby deriving
`K_TL=0`.

## Executable theorem

Minimax log-loss over the two coarse block labels equalizes active losses:

```text
-log(p_plus) = -log(p_perp)
```

so

```text
p_plus = p_perp = 1/2.
```

That lands on the Koide/source-neutral leaf.  But this works only because the
loss counts the two central labels equally.

If the same minimax principle is applied to the retained real micro-dimensions,
there is one singlet dimension and two real-doublet dimensions:

```text
micro probabilities = (1/3, 1/3, 1/3)
block totals = (1/3, 2/3).
```

That rank-weighted law gives `Q=1` and nonzero `K_TL`.

More generally, weighted minimax gives

```text
p_plus = 1/(1+c)
p_perp/p_plus = c.
```

The desired point is `c=1`; retained real dimension/fusion counting gives
`c=2`.

## Residual

```text
RESIDUAL_COARSEGRAINING = loss_weight_c_equals_1_equiv_K_TL
```

## Why this is not closure

The result depends on a loss/coarse-graining primitive.  Equal block labels,
real dimensions, and other retained-compatible losses give different exact
values.  The minimax argument closes Q only after choosing the non-monoidal
equal-label loss.

## Falsifiers

- A retained physical decision principle proving the loss weight `c=1` for the
  charged-lepton second-order carrier.
- A theorem showing real dimensions/fusion weights are not the relevant
  outcomes for this physical measurement.
- A proper-scoring derivation whose minimax solution is equal blocks and whose
  loss is fixed by retained `Cl(3)/Z^3` structure.

## Boundaries

- The runner covers log-loss minimax on coarse labels, real micro-dimensions,
  and a symbolic weighted-loss family.
- It does not exclude a future physical coarse-graining theorem; it isolates
  exactly what such a theorem must prove.

## Hostile reviewer objections answered

- **"Minimax naturally gives uniform."**  Uniform over what?  Coarse block
  labels give `1:1`; retained real dimensions give `1:2`.
- **"The two central idempotents are the physical outcomes."**  That is the
  needed coarse-graining primitive.  It is not forced by fusion or rank data.
- **"Does this support Q?"**  It supports the location of the missing
  principle.  It does not derive that principle.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_minimax_block_decision_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_Q_MINIMAX_BLOCK_DECISION_NO_GO=TRUE
Q_MINIMAX_BLOCK_DECISION_CLOSES_Q=FALSE
RESIDUAL_COARSEGRAINING=loss_weight_c_equals_1_equiv_K_TL
```
