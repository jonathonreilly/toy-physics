# Koide Q Markov-category terminal-state no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_markov_terminal_state_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use categorical classical-process structure to force the center source:

```text
copy/delete + discard + terminality
  -> canonical center-label preparation
  -> K_TL = 0.
```

## Executable theorem

In the finite classical Markov category, discarding is unique:

```text
discard = (1, 1).
```

Preparations from the terminal object to the two-label center are all
probability distributions:

```text
* -> (u, 1-u).
```

The runner verifies:

```text
discard * prep = 1
copy * prep = (u, 0, 0, 1-u).
```

## Obstruction

Terminality gives a unique effect from labels to the terminal object.  It does
not give a unique state from the terminal object to labels.

Closing and non-closing preparations are all valid:

```text
u = 1/3 -> Q = 1,   K_TL = 3/8
u = 1/2 -> Q = 2/3, K_TL = 0
u = 2/3 -> Q = 1/2, K_TL = -3/8.
```

Convex operational closure does not remove the ambiguity.  The mixture of the
rank preparation and equal-label preparation is still a valid normalized
Markov preparation:

```text
(1-lambda)(1/3,2/3) + lambda(1/2,1/2).
```

## Naturality escape hatch

Naturality under an abstract label swap would force:

```text
u = 1/2.
```

But the retained real C3 carrier has:

```text
rank(P_plus) = 1
rank(P_perp) = 2.
```

The swap is not a retained physical automorphism.

## Residual

```text
RESIDUAL_SCALAR = center_label_preparation_u_minus_one_half_equiv_K_TL
RESIDUAL_PREPARATION = terminality_does_not_choose_uniform_center_state
```

## Why this is not closure

Markov-category structure is the right language for classical center labels,
but it does not select a physical preparation.  The uniform center state still
requires a retained source law.

## Falsifiers

- A retained Markov-natural automorphism exchanging the two center labels.
- A theorem making the uniform state the unique physical preparation, not just
  a valid preparation.
- A causal or operational source rule excluding the rank-state preparation.

## Boundaries

- Covers finite classical Markov copy/delete/discard structure for the two
  center labels.
- Does not refute a stronger physical preparation theorem.

## Hostile reviewer objections answered

- **"The terminal map is unique."**  The unique terminal map is discard, not a
  unique preparation.
- **"Classical labels should be copied."**  Copying preserves every classical
  distribution.
- **"Use naturality."**  Naturality under swap adds the non-retained exchange
  symmetry.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_markov_terminal_state_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_MARKOV_TERMINAL_STATE_NO_GO=TRUE
Q_MARKOV_TERMINAL_STATE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=center_label_preparation_u_minus_one_half_equiv_K_TL
RESIDUAL_PREPARATION=terminality_does_not_choose_uniform_center_state
```
