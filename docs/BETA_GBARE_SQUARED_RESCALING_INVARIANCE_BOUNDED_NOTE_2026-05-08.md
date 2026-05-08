# β·g_bare² = 2 N_c Rescaling-Invariance Bounded Identity Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Proposal allowed:** false
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_beta_gbare_squared_rescaling_invariance.py`](../scripts/frontier_beta_gbare_squared_rescaling_invariance.py)
**Runner cache:** [`logs/runner-cache/frontier_beta_gbare_squared_rescaling_invariance.txt`](../logs/runner-cache/frontier_beta_gbare_squared_rescaling_invariance.txt)

## Claim

The dimensionless identity

```text
β · g_bare² = 2 N_c
```

is a direct algebraic consequence of the Wilson small-`a` matching
relation `β = 2 N_c / g_bare²` carried by
[`G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`](G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md).
Under the generator-basis rescaling `T_a → c · T_a` (equivalently
`A → c · A`) established by
[`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md),
which sends `β → c² · β`, holding the product `β · g_bare² = 2 N_c`
fixed forces the companion mapping `g_bare² → g_bare² / c²`. The product

```text
β'(c) · g_bare'²(c) = (c² β) · (g_bare² / c²) = β · g_bare² = 2 N_c
```

is therefore invariant under the rescaling. Verified at exact rational
precision for `c ∈ {1/2, 1, 2, 3}`.

This note is a bounded arithmetic identity. It does not introduce a new
axiom, does not modify the retained theorem family, and does not promote
any status row.

## Imported Authorities

| Authority | Role |
|---|---|
| [`G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`](G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md) | supplies the Wilson small-`a` matching relation `β = 2 N_c / g_bare²` used as input here |
| [`G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md`](G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md) | supplies the `T_a → c · T_a` (equivalently `A → c · A`) generator-basis rescaling and the `β → c² · β` mapping used as input here |

Both are imported authorities for a bounded arithmetic identity. The row
remains unaudited until the independent audit lane reviews this note,
its dependencies, and the runner.

## Arithmetic Identity Table

For `N_c = 3`, the imported Wilson small-`a` matching gives
`β · g_bare² = 2 · 3 = 6`. With the imported generator-basis rescaling
mapping `β → c² · β`, the companion mapping that holds the product
fixed is `g_bare² → g_bare² / c²`. The single-row arithmetic table:

| `c` | `β'(c) = c² · β` | `g_bare'²(c) = g_bare² / c²` | product `β'(c) · g_bare'²(c)` |
|---|---|---|---|
| `1/2` | `β / 4` | `4 · g_bare²` | `2 N_c` |
| `1`   | `β`     | `g_bare²`     | `2 N_c` |
| `2`   | `4 · β` | `g_bare² / 4` | `2 N_c` |
| `3`   | `9 · β` | `g_bare² / 9` | `2 N_c` |

The runner verifies each row at exact rational precision using
`fractions.Fraction`, with the representative substitution
`β = 2 N_c / g_bare² = 6` at the canonical `g_bare² = 1` value carried
by `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`. The product equals
`2 N_c = 6` exactly for every row.

## Boundaries

This is a **bounded arithmetic identity only**. In particular, this
note does not establish, and does not claim to establish:

- a continuum-limit statement about `β` or `g_bare` at `a → 0`;
- any retention or promotion of `g_bare = 1` or any other `g_bare` lane;
- any modification of the imported Wilson small-`a` matching relation;
- any modification of the imported generator-basis rescaling theorem;
- any new claim about the action form (Wilson plaquette vs Symanzik vs
  improved actions remain outside this scope);
- any new claim about the canonical Cl(3) connection normalization
  `Tr(T_a T_b) = δ_ab / 2` itself;
- any parent theorem/status promotion.

The single load-bearing step is class (A) algebraic substitution
verified at exact rational precision for the four enumerated `c`
values.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_beta_gbare_squared_rescaling_invariance.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: bounded arithmetic identity passes; β · g_bare² = 2 N_c is
invariant under the imported generator-basis rescaling for c ∈ {1/2, 1,
2, 3} at exact rational precision.
```
