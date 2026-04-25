# Koide Q Witten-index pairing no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_witten_index_pairing_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Test whether a hidden supersymmetric pairing between the retained `C_3`
singlet and real doublet blocks forces equal block totals, deriving `K_TL=0`.

## Executable theorem

The retained block dimensions are

```text
dim(P_plus) = 1
dim(P_perp) = 2.
```

The graded/Witten index is therefore

```text
Str(I) = dim(P_plus) - dim(P_perp) = -1.
```

Any odd map between the blocks has rank at most `1`, so one real doublet
direction remains unpaired.  The same obstruction appears whether the odd map
goes singlet-to-doublet or doublet-to-singlet.

## Residual

```text
RESIDUAL_SCALAR = dim_plus_minus_dim_perp_nonzero_equiv_K_TL
RESIDUAL_INDEX = dim_plus_minus_dim_perp_nonzero_equiv_K_TL
```

Equal block totals land on the Koide/source-neutral leaf, but they would
require cancelling the nonzero retained index.  Zero index would need one
auxiliary singlet/ghost dimension, which changes the carrier.

## Why this is not closure

Supersymmetric pairing does not remove the rank mismatch.  It makes the
obstruction sharper: the retained carrier has a nonzero index, so complete
pairing is impossible without adding new structure.

## Falsifiers

- A retained auxiliary field/source that cancels the index and is already part
  of the charged-lepton second-order carrier.
- A physical theorem showing the unpaired doublet direction decouples from the
  normalized Q source.
- A nonstandard grading where the retained blocks have equal effective index
  without changing the carrier.

## Boundaries

- The runner covers finite-dimensional odd pairings between the rank-1 singlet
  and rank-2 real doublet blocks.
- It does not exclude a future theory with additional retained auxiliary
  degrees of freedom; it shows such degrees are not currently present.

## Hostile reviewer objections answered

- **"A supercharge could pair the blocks."**  It can pair at most one doublet
  direction with the singlet; one doublet direction remains.
- **"Could a ghost cancel it?"**  Yes, but that is a new retained degree of
  freedom.
- **"Does this disprove equal-block support?"**  No.  It rejects only the
  stronger claim that supersymmetric pairing derives equal blocks from the
  retained carrier.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_witten_index_pairing_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_Q_WITTEN_INDEX_PAIRING_NO_GO=TRUE
Q_WITTEN_INDEX_PAIRING_CLOSES_Q=FALSE
RESIDUAL_SCALAR=dim_plus_minus_dim_perp_nonzero_equiv_K_TL
RESIDUAL_INDEX=dim_plus_minus_dim_perp_nonzero_equiv_K_TL
```
