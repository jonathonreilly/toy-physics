# Off-Surface Same-1PI Pinning Theorem for the Two-Ward `g_bare` Route

**Date:** 2026-04-19
**Status:** DERIVED — load-bearing Path-2 theorem
**Role:** upgrades the final Path-2 step from a canonical-surface agreement
check to an off-surface coefficient identity on the same retained block

---

## Theorem

Fix the retained Wilson-plaquette + staggered-Dirac bare action on the
`Q_L = (2,3)` block, but leave the bare gauge scale `g_bare` arbitrary.

Let

```
Gamma_S^(4)(q^2; g_bare)
```

denote the amputated tree-level four-fermion Green's function projected onto
the unique color-singlet x iso-singlet x Dirac-scalar operator

```
O_S = (psibar psi)_(1,1) (psibar psi)_(1,1)
```

on `Q_L`.

Then the same retained Green's function has two complete tree-level
representations:

```
Gamma_S^(4)(q^2; g_bare)
  = - c_S g_bare^2 / (2 N_c q^2) * O_S                           (A)
  = - F_Htt^(0)(g_bare)^2 / q^2 * O_S                           (B)
```

with `|c_S| = 1` and `F_Htt^(0)(g_bare) = <0|H_unit|tbar t>_tree`.

Therefore the scalar-singlet coefficient identity

```
F_Htt^(0)(g_bare)^2 = g_bare^2 / (2 N_c)                        (P1)
```

holds for arbitrary `g_bare` on the retained block.

Combining (P1) with
[G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md),
which proves

```
F_Htt^(0)(g_bare) = 1 / sqrt(6)
```

for all `g_bare`, gives

```
g_bare^2 = 2 N_c * (1/6) = 1.
```

So the unique positive solution is

```
g_bare = 1.
```

---

## Proof

### 1. There is only one retained scalar-singlet coefficient on `Q_L`

By D17, the unique unit-normalized scalar-singlet composite on `Q_L` is

```
H_unit = (1 / sqrt(N_c N_iso)) sum_{alpha,a} psibar_{alpha,a} psi_{alpha,a}
       = (1 / sqrt(6)) (psibar psi)_(1,1).
```

So the projected channel `O_S` has one retained scalar-singlet coefficient to
be matched. There is no second independent scalar-singlet operator on this
block with the same normalization.

### 2. Representation A is valid for arbitrary `g_bare`

The retained bare action contains only the Wilson plaquette and the staggered
Dirac operator. Changing `g_bare` rescales the gauge vertex coefficient but
does not change the field content of the action.

Therefore D16 remains the same statement off the canonical surface: at tree
order on the scalar-singlet channel, the only contributing diagram is
single-gluon exchange. Applying the exact SU(`N_c`) color Fierz coefficient
`-1/(2 N_c)` and the exact Lorentz-Clifford scalar coefficient `c_S` gives

```
Gamma_S^(4)(q^2; g_bare)
  = - c_S g_bare^2 / (2 N_c q^2) * O_S.
```

This is the complete tree-level coefficient from the bare action for arbitrary
`g_bare`.

### 3. Representation B is valid for arbitrary `g_bare`

The companion Rep-B theorem proves that the tree-level matrix element

```
F_Htt^(0)(g_bare) := <0|H_unit|tbar t>_tree
```

exists on the same retained block and is independent of `g_bare`:

```
F_Htt^(0)(g_bare) = 1 / sqrt(6).
```

Using that same matrix element on both scalar insertions gives the tree-level
`H_unit` representation of the same projected Green's function:

```
Gamma_S^(4)(q^2; g_bare)
  = - F_Htt^(0)(g_bare)^2 / q^2 * O_S.
```

No canonical-surface input enters this step: the operator `H_unit`, the
external top-channel state, and the tree-level Wick contraction are all
defined on the retained block itself.

### 4. Why the equality is mathematically unavoidable

This is not a UV-vs-EFT matching move and not a support-layer reinterpretation.
It is the same-theory identity already isolated in Step 3 of
[YT_WARD_IDENTITY_DERIVATION_THEOREM.md](YT_WARD_IDENTITY_DERIVATION_THEOREM.md):
the scalar-singlet four-fermion coefficient is one amputated Green's function
`Gamma_S^(4)` computed two algebraically equivalent ways in the same retained
theory.

On the present off-surface family:

- Representation A is the complete tree-level coefficient from bare-action
  Feynman rules.
- Representation B is the complete tree-level coefficient from the unique
  scalar-singlet composite residue on the same block.

Because D17 leaves only one retained scalar-singlet coefficient on `Q_L`,
these two formulas cannot represent different quantities. They are two
representations of the same coefficient of the same projected Green's
function. Their coefficients must therefore agree for every `g_bare` in the
family.

Equating (A) and (B) gives

```
F_Htt^(0)(g_bare)^2 = c_S g_bare^2 / (2 N_c).
```

The explicit Clifford trace gives `c_S = +1`, so

```
F_Htt^(0)(g_bare)^2 = g_bare^2 / (2 N_c),
```

which is (P1).

### 5. Solve the coefficient identity

Substitute the Rep-B theorem

```
F_Htt^(0)(g_bare) = 1 / sqrt(6)
```

into (P1):

```
1/6 = g_bare^2 / (2 * 3)
g_bare^2 = 1.
```

On the positive bare-coupling branch,

```
g_bare = 1.
```

This proves the theorem.

---

## What This Fixes

The rejected version of Path 2 depended on a subordinate support note to read
`Rep A = Rep B` as a pinning equation. This theorem removes that dependence.

The decisive step is now internal to the retained Ward route itself:

1. Rep B is proved off-surface.
2. The same projected `Gamma^(4)` coefficient is proved off-surface.
3. The resulting identity pins `g_bare` directly.

So the final Path-2 solve-for-`g_bare` step is no longer a reinterpretation of
a canonical-surface consistency check.

---

## Current audit-lane disposition (informational)

This row was audited on 2026-04-30 by
`codex-audit-loop-critical-sweep-20260430` and returned `audited_conditional`.
The chain-closure rationale recorded in the ledger is:

> *The local step cannot be promoted because direct upstream authorities
> remain unaudited, support/open/unknown, or terminal non-clean:
> `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`,
> `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`.*

The two declared upstream authorities now sit at:

| Upstream authority | Effective status (current) |
|---|---|
| [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md) | `retained_bounded` (cross-confirmed `audited_clean`) |
| [`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md) | `unaudited` |

The Rep-B-independence dep has reached retained-grade audit status since the
2026-04-30 verdict snapshot, but the `yt_ward_identity_derivation_theorem`
dep remains `unaudited`. This row therefore stays at `audited_conditional`
until the second dep is audited; the local class-(A) algebra and the proof
in §§1–5 are unchanged.

Downstream cross-reference (informational only, not a load-bearing
dependency of this pinning theorem): the Ward-route upgrade theorem
`G_BARE_FORCED_BY_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-05-09.md`
explicitly cites this row as one of its two one-hop deps and acknowledges
its current `audited_conditional` status. The conditional upgrade landed
there closes immediately under both retained-grade authorities; until this
row is itself ratified, the Ward upgrade inherits the same conditional
verdict.
