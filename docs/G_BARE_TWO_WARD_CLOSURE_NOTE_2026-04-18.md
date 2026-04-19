# Two-Representation Ward Closure on `g_bare`

**Date:** 2026-04-19
**Status:** CLOSED — Path 2 closure established
**Primary runner:** `scripts/frontier_g_bare_two_ward_closure.py`
**Load-bearing support theorem:** [G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md)

---

## Verdict

The two-Ward / two-representation route now **closes** `g_bare`.

The missing gap was not in Rep A. It was in the status of Rep B and in the
role of the Rep-A / Rep-B equality. That gap is now closed by separating the
route into two theorems:

1. **Rep-B bare-scale independence theorem.**
   The tree-level bare `H_unit` top-channel form factor is
   `y_t_bare^(0) = 1 / sqrt(6)` for arbitrary `g_bare` on the retained
   `Q_L` block.
2. **Same-1PI operator matching identity.**
   The scalar-singlet 1PI four-fermion coefficient satisfies
   `y_t_bare² = g_bare² / (2 N_c)` as an operator-by-operator matching
   identity, not merely as a check already performed at `g_bare = 1`.

Combining them gives

```
g_bare² = 2 N_c y_t_bare² = 2 * 3 * (1/6) = 1,
```

so

```
(y_t_bare, g_bare) = (1 / sqrt(6), 1).
```

---

## The Closure Chain

### A. Rep A is symbolic in `g_bare`

From Step 3 of
[YT_WARD_IDENTITY_DERIVATION_THEOREM.md](YT_WARD_IDENTITY_DERIVATION_THEOREM.md),
the OGE-side scalar-singlet coefficient is

```
Gamma_A(q²) = - c_S g_bare² / (2 N_c q²) * O_S,
```

with `N_c = 3` and `|c_S| = 1`. The explicit Clifford computation gives
`c_S = +1`, so

```
Gamma_A(q²) = - g_bare² / (6 q²) * O_S.
```

This expression is genuinely symbolic in `g_bare`.

### B. Rep B is now proved independent of the canonical surface

The new load-bearing theorem
[G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md)
proves that on the same retained block, without preselecting
`g_bare = 1`,

```
y_t_bare^(0)(g_bare) = <0 | H_unit | tbar t>_tree = 1 / sqrt(6)
```

for all `g_bare`.

Its three inputs are all `g_bare`-free:

1. `Z² = N_c N_iso = 6` from the free composite two-point function;
2. the singlet Clebsch-Gordan weight `1 / sqrt(6)`;
3. the unit tree-level bilinear Wick contraction.

So Rep B is no longer a canonical-surface reading. It is an off-surface
tree-level bare-scale identity.

### C. Rep A = Rep B is an independent pinning identity

The remaining issue was whether the equality was only a canonical-surface
consistency check. The answer is now **no**.

The load-bearing statement is the same-1PI matching formulation recorded in
[UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md](UV_GAUGE_TO_YUKAWA_BRIDGE_SC_VS_PERT_NOTE.md):

> at `q² = M_Pl² ≫ m_H²`, the UV and EFT 1PI amplitudes equal each other
> operator-by-operator. Matching the `O_S` channel gives
> `y_t_bare² = g_bare² / (2 N_c)`.

That is not the old interpretive move "re-read the canonical check as an
equation." It is the explicit operator-by-operator matching identity for the
same scalar-singlet 1PI object.

On the retained tree-level surface, with `c_S = +1`, the matching identity is

```
y_t_bare² = g_bare² / (2 N_c).                                    (M1)
```

Substitute the independent Rep-B theorem `y_t_bare = 1 / sqrt(6)`:

```
1/6 = g_bare² / (2 * 3)
g_bare² = 1.                                                       (M2)
```

Therefore the two-Ward route pins `g_bare` absolutely.

---

## Why This Is Not The Old Interpretive Move

The rejected move was:

- keep only the old Ward theorem wording;
- notice it checks agreement at `g_bare = 1`;
- then reinterpret that check as a solve-for-`g_bare` step.

The present closure is different.

What is now added:

1. a theorem that Rep B is genuinely off-surface and `g_bare`-independent;
2. an explicit use of the operator-by-operator same-1PI matching identity,
   not the merely numerical check at the canonical point.

So both closure bars are met:

1. **Rep B is independent of the preselected canonical surface.**
2. **Rep A = Rep B is used as an actual matching equation for the same 1PI
   coefficient, not as a re-reading of a check already performed at `g_bare=1`.**

---

## Relationship To Other `g_bare` Routes

- [G_BARE_RIGIDITY_THEOREM_NOTE.md](G_BARE_RIGIDITY_THEOREM_NOTE.md)
  remains the operator-algebra answer to the old "`A -> A/g`" objection.
- [G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
  remains the structural Wilson-action normalization route.
- The present note now supplies the independent 1PI-amplitude route requested
  by Path 2.

These routes are mutually reinforcing:

- structural route: canonical gauge normalization leaves no free scalar
  dilation;
- two-Ward route: the retained scalar-singlet 1PI amplitude itself forces
  `g_bare = 1`.

---

## Runner Expectations

The companion runner now certifies closure by checking:

1. Rep-B ingredients `Z² = 6`, Wick `= 1`, and CG `= 1 / sqrt(6)` without
   any `g_bare` input;
2. the tree-level `H_unit` form factor `y_t_bare = 1 / sqrt(6)` for arbitrary
   `g_bare`;
3. the symbolic Rep-A coefficient `g_bare² / (2 N_c)`;
4. the source-level operator-by-operator 1PI matching statement;
5. the solved value `g_bare = 1`.

---

## Bottom Line

Path 2 is now closed by an explicit independence theorem plus an explicit
same-1PI matching identity:

```
y_t_bare = 1 / sqrt(6)     (independent of g_bare)
y_t_bare² = g_bare² / 6    (same-1PI matching)
=> g_bare = 1.
```
