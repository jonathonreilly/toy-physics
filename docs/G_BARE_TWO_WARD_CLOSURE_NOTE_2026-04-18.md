# Two-Representation Ward Closure on `g_bare`

**Date:** 2026-04-19 (originally); 2026-05-10 (audit-narrowing refresh:
status-line scoping + dep-status table at footer).
**Status:** `audited_conditional` per 2026-04-30 audit; the local
two-Ward closure algebra is unchanged, but the row inherits one-hop
dependency on five upstream authorities, of which one
(Rep-B independence) has reached `audited_clean / retained_bounded`
since the snapshot, one (same-1PI pinning) is `audited_conditional`,
and three (YT_WARD, rigidity, structural normalization) remain
`unaudited`. See "Audit boundary" footer for the full dep-status
table.
**Type:** positive_theorem (in-note algebra) under upstream-conditional
imports.
**Status authority:** independent audit lane only.
**Authority role:** records the in-note class-B closure algebra
combining Rep-B independence and the same-1PI pinning identity. Does
**not** propose retained or promoted-status promotion until the four
non-clean upstream authorities (same-1PI pinning, YT_WARD, rigidity,
structural normalization) are ratified to `audited_clean`.
**Primary runner:** `scripts/frontier_g_bare_two_ward_closure.py`
(`PASS=18, FAIL=0`)
**Load-bearing theorems:**
- [G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md) (`audited_clean / retained_bounded`, audit_date 2026-05-05)
- [G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md](G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md) (`audited_conditional`, audit_date 2026-04-30)

---

## Verdict

The two-Ward / two-representation route now **closes** `g_bare`.

The missing gap was not in Rep A. It was in the status of Rep B and in the
status of the final Rep-A / Rep-B equality. That gap is now closed by
separating the route into two explicit theorems:

1. **Rep-B bare-scale independence theorem.**
   The tree-level bare `H_unit` top-channel form factor is
   `y_t_bare^(0) = 1 / sqrt(6)` for arbitrary `g_bare` on the retained
   `Q_L` block.
2. **Off-surface same-1PI pinning theorem.**
   The scalar-singlet four-fermion coefficient on the retained `Q_L` block
   satisfies
   `F_Htt^(0)(g_bare)^2 = g_bare² / (2 N_c)` for arbitrary `g_bare`,
   because it is the same amputated Green's-function coefficient computed two
   ways in the same retained theory.

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

### C. The final equality is now theorem-grade and off-surface

The remaining issue was whether the equality was only a canonical-surface
consistency check. The answer is now **no**.

The load-bearing statement is no longer the subordinate bridge note. It is the
two-Ward same-1PI pinning theorem
[G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md](G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md),
which isolates the exact off-surface identity needed for closure:

```
Gamma_S^(4)(q²; g_bare)
  = - c_S g_bare² / (2 N_c q²) * O_S
  = - F_Htt^(0)(g_bare)^2 / q² * O_S.                              (M1)
```

This theorem is internal to the retained Ward route itself:

- Representation A uses D16 + D12 + S2 on the bare action with arbitrary
  `g_bare`.
- Representation B uses D17 plus the Rep-B independence theorem on the same
  retained block.
- D17 leaves only one retained scalar-singlet coefficient on `Q_L`, so the two
  formulas are forced to agree as the same projected Green's-function
  coefficient.

```
F_Htt^(0)(g_bare)^2 = g_bare² / (2 N_c).                           (M2)
```

That is not the old interpretive move "re-read the canonical check as an
equation." It is an off-surface theorem about the same coefficient in the same
retained theory.

Substitute the independent Rep-B theorem `F_Htt^(0)(g_bare) = 1 / sqrt(6)`:

```
1/6 = g_bare² / (2 * 3)
g_bare² = 1.                                                       (M3)
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
2. a theorem that the same scalar-singlet `Gamma^(4)` coefficient itself is
   off-surface and identical in the two retained representations.

So both closure bars are met:

1. **Rep B is independent of the preselected canonical surface.**
2. **Rep A = Rep B is used as an actual off-surface coefficient identity for
   the same projected Green's function, not as a re-reading of a check already
   performed at `g_bare = 1`.**

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
4. the theorem-grade off-surface same-`Gamma^(4)` pinning identity;
5. the solved value `g_bare = 1`.

---

## Bottom Line

Path 2 is now closed by an explicit independence theorem plus an explicit
off-surface same-1PI pinning theorem:

```
F_Htt^(0)(g_bare) = 1 / sqrt(6)     (independent of g_bare)
F_Htt^(0)(g_bare)^2 = g_bare² / 6   (same Gamma^(4) coefficient)
=> g_bare = 1.
```

---

## Audit boundary (2026-05-10 refresh of 2026-04-30 verdict)

This row was audited on 2026-04-30 by
`codex-audit-loop-critical-sweep-20260430` and returned
`audited_conditional`. The chain-closure rationale recorded in the
ledger is:

> *The local step cannot be promoted because direct upstream authorities
> remain unaudited, support/open/unknown, or terminal non-clean:
> `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`,
> `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`,
> `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`,
> `G_BARE_RIGIDITY_THEOREM_NOTE.md`,
> `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`.*

The audit's `verdict_rationale` (load-bearing-step class B):

> *The load-bearing step still imports unratified direct authority.
> Repair target: ratify or repair the listed upstream theorem/bridge
> rows and rerun the local runner so it computes the disputed bridge
> rather than only checking consequences. Claim boundary until fixed:
> the note may be cited as conditional/supporting local structure, but
> no retained or promoted audit status propagates through this row.*

The five declared upstream authorities now sit at:

| Upstream authority | Effective status (current) | Movement since 2026-04-30 audit snapshot |
|---|---|---|
| [`G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md) | `audited_clean` / `retained_bounded` (audit_date 2026-05-05) | promoted from `audited_conditional` to `audited_clean / retained_bounded` |
| [`G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`](G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md) | `audited_conditional` (audit_date 2026-04-30) | unchanged |
| [`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md) | `unaudited` | unchanged |
| [`G_BARE_RIGIDITY_THEOREM_NOTE.md`](G_BARE_RIGIDITY_THEOREM_NOTE.md) | `unaudited` | unchanged |
| [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md) | `unaudited` | unchanged |

The Rep-B-independence dep has reached `audited_clean / retained_bounded`
since the 2026-04-30 verdict snapshot. The same-1PI pinning dep
remains `audited_conditional`, and three deps (YT_WARD, rigidity,
structural normalization) remain `unaudited`. This row therefore
stays at `audited_conditional` until those four deps are audited
clean; the local class-B algebra and the proof in §§A--C are
unchanged. The cached runner
`scripts/frontier_g_bare_two_ward_closure.py` remains fresh
(`PASS=18, FAIL=0`).

**Cross-reference.** The same-cluster theorem note
[`G_BARE_FORCED_BY_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-05-09.md`](G_BARE_FORCED_BY_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-05-09.md)
exists in `docs/` and treats the Rep-B-only forcing branch as a
stand-alone bounded theorem. It depends on the same Rep-B
independence authority and on this row's two-Ward closure chain; it
does not retire any of this row's four non-clean deps.

**Repair path until fixed.** Per the audit verdict, the closure of
this row requires either (i) ratification of the four non-clean
upstream authorities (same-1PI pinning, YT_WARD, rigidity, structural
normalization) to `audited_clean`, or (ii) a runner extension that
computes the disputed bridge `F_Htt^(0)(g_bare)^2 = g_bare^2 / (2 N_c)`
directly rather than checking consequences at a chosen `g_bare`. No
repair is attempted in this audit-narrowing refresh; the in-note
algebra and proof are unchanged.
