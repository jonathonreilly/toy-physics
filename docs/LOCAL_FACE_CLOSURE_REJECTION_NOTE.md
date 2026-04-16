# Minimal Local Face-Closure Candidate Rejection at `beta = 6`

**Date:** 2026-04-16  
**Status:** bounded rejection of the weakest local closure axiom  
**Script:** `scripts/frontier_local_face_closure_rejection.py`

## Question

Once the exact local directed-cell and root-face launch theorems are known, does
the weakest possible local closure axiom already close analytic `P(6)`?

## Closure candidate

The weakest local candidate is:

1. keep the exact local block
   - `p = P_1plaq(6)`
2. keep only the exact local face launch sectors
3. factor the remaining outgoing frontier faces through one generic face
   dressing factor `G`

That gives the minimal local closure system

`G = 1 + 3 p^4 G^5 + p^14 G^15`

and then

`H = 1 + 4 p^4 G^5 + 4 p^14 G^15`,
`P(6) = p H`.

## Bounded answer

No.

Using a strict lower bound on the exact local block

`p_low = 0.42253173964998 < P_1plaq(6)`,

define

`g(G) = 1 + 3 p_low^4 G^5 + p_low^14 G^15 - G`.

Then:

- `g(0) > 0`
- `g''(G) > 0` for `G > 0`
- so `g` has a unique global minimum on the positive branch
- that minimum occurs near `G_* = 1.202246940360351...`
- and
  `g(G_*) = 0.0380192306425637... > 0`

Therefore `g(G) > 0` for every `G > 0`.

So the generic fixed-point equation has no positive real solution even for the
strict lower bound `p_low`, hence also no positive solution for the exact local
block.

## Corollary

The weakest local face-closure axiom is rejected at `beta = 6`.

So the exact local theorems are real, but they still do not by themselves
produce a physically admissible analytic plaquette closure.

The remaining closure has to retain more than:

- one generic frontier-face amplitude
- the local one-cell / three-cell launch sectors

In particular, it has to retain nontrivial correlations among outgoing frontier
faces beyond this minimal local factorization.

The next stronger exact obstruction is now recorded in
`docs/ONE_SHELL_FACE_STATE_TRANSFER_NO_GO_NOTE.md`: even the full multiset of
exact one-shell local boundary-face states is still not enough to determine the
next rooted continuation count.

## Honest status

This note does **not** derive analytic `P(6)`.

It closes a narrower but important decision:

> the weakest explicit local closure axiom is now tested and rejected.

That is better than leaving the closure line implicit, because the branch now
records one concrete local closure attempt and its failure.

## Commands run

```bash
python3 scripts/frontier_local_face_closure_rejection.py
```

Output summary:

- strict lower bound on `P_1plaq(6)`
- unique positive critical point of the closure residual
- strictly positive minimum residual
- rejection of the minimal local face-closure candidate
