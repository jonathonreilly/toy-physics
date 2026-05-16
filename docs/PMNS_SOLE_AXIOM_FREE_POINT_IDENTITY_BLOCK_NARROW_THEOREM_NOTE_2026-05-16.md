# PMNS Sole-Axiom Free-Point Identity-Block — Narrow Bridge Theorem

**Date:** 2026-05-16
**Claim type:** positive_theorem (narrow algebraic bridge)
**Status:** unaudited candidate. This note is graph-visible only so the
independent audit lane can decide whether the candidate is retained.
**Primary runner:** [`scripts/frontier_pmns_sole_axiom_free_point_identity_block_2026-05-16.py`](../scripts/frontier_pmns_sole_axiom_free_point_identity_block_2026-05-16.py)
**Cached output:** [`logs/runner-cache/frontier_pmns_sole_axiom_free_point_identity_block_2026-05-16.txt`](../logs/runner-cache/frontier_pmns_sole_axiom_free_point_identity_block_2026-05-16.txt)
**Source-note proposal:** audit verdict and downstream status set only by
the independent audit lane.

## Audit context

This note is filed to address the `missing_bridge_theorem` repair target
named by the 2026-05-05 / 2026-05-11 audit verdicts on
`pmns_oriented_cycle_selection_structure_note`:

> `missing_bridge_theorem: add a retained bridge proving the graph-first
> residual antiunitary condition and the sole-axiom free-point identity
> block within the restricted dependency chain.`

This note addresses the second clause only: the sole-axiom free-point
identity-block claim. The graph-first residual antiunitary clause is
addressed by the sibling note
`PMNS_GRAPH_FIRST_RESIDUAL_ANTIUNITARY_NARROW_THEOREM_NOTE_2026-05-16.md`.

The downstream note
`PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md`
imports the active-block identification `A = I_3` at the sole-axiom free
point as a premise. That import is exactly what the present narrow
bridge theorem closes from the active-operator construction supplied by
the sibling utility `scripts/pmns_lower_level_utils.py` (function
`active_operator(x, y, delta)`).

## Safe statement

Let the active operator on the `hw=1` triplet be the construction used
throughout the PMNS active-block stack:

```text
A_act(x, y, delta) = diag(x_1, x_2, x_3)
                   + diag(y_1, y_2, y_3 * exp(i * delta)) @ C
```

where `x_i, y_i in R` are the active diagonal and active forward-cycle
weights, `delta in R` is the active CP phase, and
`C = [[0,1,0],[0,0,1],[1,0,0]]` is the canonical forward-cycle matrix.

Define the **sole-axiom free point** of this construction as the
parameter point at which the active deformation away from the trivial
identity carrier vanishes:

```text
x = (1, 1, 1),    y = (0, 0, 0),    delta arbitrary in R.
```

**Theorem (sole-axiom free-point identity block).**

At the sole-axiom free point of the active-operator construction, the
active block is exactly the `3 x 3` identity matrix:

```text
A_act((1,1,1), (0,0,0), delta) = I_3   for all delta in R.
```

Therefore the oriented forward-cycle coefficients
`(c_1, c_2, c_3) = diag(A_act @ C^dagger)` vanish:

```text
c_1 = c_2 = c_3 = 0,
```

and the C3-fixed-locus scalar `sigma = (c_1 + c_2 + c_3) / 3` is exactly
`0`.

## Proof

Substitute `x = (1, 1, 1)` and `y = (0, 0, 0)` into the active-operator
construction:

```text
A_act((1,1,1), (0,0,0), delta)
  = diag(1, 1, 1) + diag(0, 0, 0 * exp(i * delta)) @ C
  = I_3           + 0_{3x3} @ C
  = I_3.
```

The second term vanishes because `diag(0, 0, 0)` is the zero matrix
independent of the multiplicative phase `exp(i * delta)` applied to its
third entry. The result is independent of `delta` for the same reason.

The oriented forward-cycle coefficient law (see
[`PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md`](PMNS_ORIENTED_CYCLE_CHANNEL_VALUE_LAW_NOTE.md))
is

```text
c_i = (A_act @ C^dagger)_{i, i}.
```

For `A_act = I_3` we have `A_act @ C^dagger = C^dagger`, and the diagonal
entries of `C^dagger` are all zero because `C` is a strict permutation
matrix with no fixed points (it sends index `i` to index `i+1 mod 3`).
Hence `c_1 = c_2 = c_3 = 0`, and `sigma = 0`.

## Boundary

This bridge theorem closes only the algebraic identification of the
active block as `I_3` at the sole-axiom free point of the active-operator
construction. It does not:

- pick out the active-operator construction as the unique sole-axiom
  active carrier (that is the role of the upstream retained authority
  chain on the `hw=1` triplet),
- derive the active-operator construction itself from `Cl(3)` on `Z^3`
  (that remains a separate carrier-derivation lane), or
- select a nontrivial value of `(x, y, delta)` away from the free point.

What it does close, on its own terms, is the load-bearing step in
`PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md` that asserts
"`A = I_3` at the sole-axiom free point, hence `sigma = 0` on the
C3-covariant locus."

## Runner check breakdown

The paired runner exercises class A finite-dimensional algebra only:

- explicit construction of `A_act((1,1,1), (0,0,0), delta)` at six
  sample values of `delta`,
- explicit identity `A_act((1,1,1), (0,0,0), delta) == I_3`,
- explicit `diag(A_act @ C^dagger) == (0, 0, 0)` at each sample,
- explicit `sigma == 0` at each sample,
- non-vanishing of `A_act((1,1,1), (0.3, -0.2, 0.1), 0.4) - I_3` as a
  negative control (the free-point identification is special, not
  vacuous).

Expected counts: `runner_check_breakdown = {A: N, B: 0, C: 0, D: 0,
total_pass: N}` where `N` is the printed `PASS` count in the cache.

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_sole_axiom_free_point_identity_block_2026-05-16.py
```

## Honest auditor read

The runner performs explicit class A matrix algebra against the same
active-operator construction `active_operator(x, y, delta)` already used
by the rest of the PMNS stack via `scripts/pmns_lower_level_utils.py`.
It does not derive that construction from the sole axiom; the carrier
derivation is the role of the upstream retained `hw=1` authority chain.
Within those imports, the algebraic identity
`A_act((1,1,1), (0,0,0), delta) = I_3` and the resulting
`(c_1, c_2, c_3) = (0, 0, 0)` are exact finite-dimensional facts.
Effective status remains `unaudited` until the independent audit lane
assigns one.

## Scope of this rigorization

This note is a narrow class A bridge theorem registered specifically to
close one of the two `missing_bridge_theorem` clauses named by the
audit verdict on `pmns_oriented_cycle_selection_structure_note`. It
adds a new source note, a paired runner, and a cached runner output.
No audit-data files are modified by this PR; no `audit_status`
promotions are claimed. The downstream selection-structure note is not
edited by this PR.
