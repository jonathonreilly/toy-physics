# PMNS Graph-First Residual Antiunitary on the Oriented Cycle Channel — Narrow Bridge Theorem

**Date:** 2026-05-16
**Claim type:** positive_theorem (narrow algebraic bridge)
**Status:** unaudited candidate. This note is graph-visible only so the
independent audit lane can decide whether the candidate is retained.
**Primary runner:** [`scripts/frontier_pmns_graph_first_residual_antiunitary_2026-05-16.py`](../scripts/frontier_pmns_graph_first_residual_antiunitary_2026-05-16.py)
**Cached output:** [`logs/runner-cache/frontier_pmns_graph_first_residual_antiunitary_2026-05-16.txt`](../logs/runner-cache/frontier_pmns_graph_first_residual_antiunitary_2026-05-16.txt)
**Source-note proposal:** audit verdict and downstream status set only by
the independent audit lane.

## Audit context

This note is filed to address the `missing_bridge_theorem` repair target
named by the 2026-05-05 / 2026-05-11 audit verdicts on
`pmns_oriented_cycle_selection_structure_note`:

> `missing_bridge_theorem: add a retained bridge proving the graph-first
> residual antiunitary condition and the sole-axiom free-point identity
> block within the restricted dependency chain.`

This note addresses the first clause only: the graph-first residual
antiunitary condition on the oriented forward-cycle channel. The
free-point identity-block clause is addressed by the sibling note
[`PMNS_SOLE_AXIOM_FREE_POINT_IDENTITY_BLOCK_NARROW_THEOREM_NOTE_2026-05-16.md`](PMNS_SOLE_AXIOM_FREE_POINT_IDENTITY_BLOCK_NARROW_THEOREM_NOTE_2026-05-16.md).

The downstream note
[`PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md`](PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md)
imports the residual antiunitary condition
`A_fwd = P_23 A_fwd^dagger P_23` on the graph-first selected-axis route
as a premise. The present narrow bridge theorem closes the algebraic
content of that premise from already-cited one-hop authorities:

- [`PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md`](PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md)
  supplies the graph-first residual `Z_2` axis stabilizer acting on the
  active triplet as `P_23` (swap of axes `1` and `2`).
- [`Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md`](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md)
  supplies the canonical residual-`Z_2`-invariant Hermitian normal form
  on the `hw=1` triplet.

What is added here is the explicit algebraic step from "residual
`Z_2`-invariance of the active Hermitian core under `P_23 H P_23 = H`"
to the **antiunitary** condition
`A_fwd = P_23 A_fwd^dagger P_23` restricted to the oriented forward-cycle
channel `A_fwd = c_1 E_12 + c_2 E_23 + c_3 E_31`. The conjugate-transpose
arises because the oriented forward-cycle channel sits as the strictly
off-diagonal anti-Hermitian-pair-projection of a Hermitian operator, and
the residual swap acts antiunitarily on that projection by exactly the
swap-of-orientation `(c_1, c_2, c_3) -> (\bar c_3, \bar c_2, \bar c_1)`.

## Safe statement

Let `P_23` denote the residual `Z_2` swap of axes `2` and `3`:

```text
P_23 = [[1, 0, 0],
        [0, 0, 1],
        [0, 1, 0]].
```

(Note: the present note adopts the same axis-labelling convention used
by the runner of
[`PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md`](PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md),
in which the residual `Z_2` stabilizer of the graph-first selected axis
acts on the `hw=1` triplet as the matrix `P_23` above.)

Let the oriented forward-cycle channel be

```text
A_fwd(c_1, c_2, c_3) = c_1 E_12 + c_2 E_23 + c_3 E_31,
```

with `E_{ij}` the standard matrix units on `C^3`.

Define the **graph-first residual antiunitary map** on the oriented
forward-cycle channel by

```text
R[A] := P_23 @ A^dagger @ P_23.
```

**Theorem (graph-first residual antiunitary action on the oriented
cycle channel).**

1. **Channel preservation.** `R` carries the forward-cycle channel into
   itself: for every `(c_1, c_2, c_3) in C^3`,

   ```text
   R[A_fwd(c_1, c_2, c_3)] = A_fwd(c_1', c_2', c_3')
   ```

   with explicit coordinate action

   ```text
   (c_1, c_2, c_3) -> (conj(c_3), conj(c_2), conj(c_1)).
   ```

2. **Antiunitarity.** `R` is conjugate-linear in `A_fwd`:

   ```text
   R[A_fwd(alpha * c)] = conj(alpha) * R[A_fwd(c)]    for all alpha in C.
   ```

3. **Involution.** `R` is an involution on the oriented cycle channel:

   ```text
   R[R[A_fwd(c)]] = A_fwd(c).
   ```

4. **Fixed locus.** The fixed locus
   `{ A_fwd(c) :  R[A_fwd(c)] = A_fwd(c) }`
   is exactly the real-3-parameter subfamily

   ```text
   c_1 = conj(c_3),    c_2 real,
   ```

   i.e. the strictly real-parameter family
   `(Re c_1, Im c_1, c_2)` of cardinality `3`.

5. **Genericity.** A generic point in `C^3` is not fixed: for almost
   every `(c_1, c_2, c_3) in C^3`,
   `R[A_fwd(c_1, c_2, c_3)] != A_fwd(c_1, c_2, c_3)`.

## Proof

For (1)–(2), expand explicitly. The matrix units satisfy

```text
P_23 E_12^dagger P_23 = P_23 E_21 P_23,
P_23 E_23^dagger P_23 = P_23 E_32 P_23,
P_23 E_31^dagger P_23 = P_23 E_13 P_23,
```

and `P_23 = P_23^dagger`. Direct multiplication gives the swap action
on the matrix-unit labels: with `P_23` swapping `2` and `3`,

```text
P_23 E_21 P_23 = E_31,
P_23 E_32 P_23 = E_23,
P_23 E_13 P_23 = E_12,
```

(this is the elementary fact that conjugation of `E_{ij}` by a permutation
matrix `P_pi` gives `E_{pi(i), pi(j)}`, with the swap `pi = (2 3)`).

Therefore for `A = c_1 E_12 + c_2 E_23 + c_3 E_31`,

```text
A^dagger = conj(c_1) E_21 + conj(c_2) E_32 + conj(c_3) E_13,

P_23 A^dagger P_23
    = conj(c_1) E_31 + conj(c_2) E_23 + conj(c_3) E_12,
```

which is exactly `A_fwd(c_1', c_2', c_3')` with
`(c_1', c_2', c_3') = (conj(c_3), conj(c_2), conj(c_1))`. This proves
both (1) and (2).

For (3), apply the involution twice:

```text
(c_1, c_2, c_3) -> (conj(c_3), conj(c_2), conj(c_1))
              -> (conj(conj(c_1)), conj(conj(c_2)), conj(conj(c_3)))
              = (c_1, c_2, c_3).
```

For (4), the fixed-point equation
`(conj(c_3), conj(c_2), conj(c_1)) = (c_1, c_2, c_3)`
is equivalent to `c_1 = conj(c_3)` together with `c_2 = conj(c_2)` and
the redundant `c_3 = conj(c_1)`; the first equation fixes `c_3` in
terms of `c_1`, the second says `c_2` is real. So the fixed locus is
exactly `c_1 = conj(c_3)`, `c_2 real`, a 3-real-parameter family.

For (5), choose any `(c_1, c_2, c_3)` violating either
`c_1 = conj(c_3)` or `c_2 = conj(c_2)`. Such triples form an open
dense subset of `C^3 ~= R^6`, of full Lebesgue measure. Their images
under `R` differ from themselves.

## Boundary

This bridge theorem closes only the algebraic content of the
graph-first residual antiunitary condition on the oriented cycle
channel from one-hop authorities. It does not:

- derive the graph-first selector itself from `Cl(3)` on `Z^3` (that is
  the role of
  [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)),
- derive the `Z_2` axis stabilizer as `P_23` (that is the role of
  [`PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md`](PMNS_GRAPH_FIRST_AXIS_ALIGNMENT_NOTE.md)),
- select a point in the resulting 3-real-parameter cycle subfamily.

What it does close, on its own terms, is the load-bearing step in
[`PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md`](PMNS_ORIENTED_CYCLE_SELECTION_STRUCTURE_NOTE.md)
that asserts "on the graph-first selected-axis route the residual
antiunitary condition `A_fwd = P_23 A_fwd^dagger P_23` fixes
`c_1 = conjugate(c_3)`, `c_2` real."

## Runner check breakdown

The paired runner exercises class A finite-dimensional algebra only:

- explicit matrix-unit conjugation under `P_23` (3 equalities),
- explicit coordinate action
  `(c_1, c_2, c_3) -> (conj(c_3), conj(c_2), conj(c_1))` on six sample
  triples (including a generic triple, a fixed-locus triple, and three
  matrix-unit-supported triples),
- antiunitarity check: `R[alpha * A] = conj(alpha) * R[A]` for two
  scalars,
- involution check `R o R = id` at six sample triples,
- explicit fixed-locus characterization `c_1 = conj(c_3)`, `c_2` real,
- negative control: generic triple is moved by `R`.

Expected counts: `runner_check_breakdown = {A: N, B: 0, C: 0, D: 0,
total_pass: N}` where `N` is the printed `PASS` count in the cache.

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_graph_first_residual_antiunitary_2026-05-16.py
```

## Honest auditor read

The runner performs explicit class A matrix algebra. It treats the
matrix `P_23` defined above and the channel
`A_fwd = c_1 E_12 + c_2 E_23 + c_3 E_31` from the downstream note as
imports, and proves the antiunitary action and its fixed locus
explicitly. The carrier identification (active `hw=1` triplet) and the
axis-stabilizer-equals-`P_23` step are imported from the cited one-hop
authorities and not re-derived here. Effective status remains
`unaudited` until the independent audit lane assigns one.

## Scope of this rigorization

This note is a narrow class A bridge theorem registered specifically to
close one of the two `missing_bridge_theorem` clauses named by the
audit verdict on `pmns_oriented_cycle_selection_structure_note`. It
adds a new source note, a paired runner, and a cached runner output.
No audit-data files are modified by this PR; no `audit_status`
promotions are claimed. The downstream selection-structure note is not
edited by this PR.
