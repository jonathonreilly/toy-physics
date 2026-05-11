# DM Wilson Direct-Descendant Canonical-Fiber Mixed Spectral / Branch-Weight No-Go

**Date:** 2026-04-19  
**Status:** exact follow-on no-go on the DM source-fiber lane. The canonical
**Claim type:** no_go
transport-column theorem and the canonical-fiber entropy note already reduced
the live object to a local scalar law on the positive source fiber over the
canonical favored column orbit. This note tests the next natural same-carrier
family:

**Audit-conditional perimeter (2026-04-30):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, `claim_type =
no_go`, `independence = cross_family`, and load-bearing step class
`B`. The audit chain-closure explanation is exact: "No. One-hop
dependencies are not all retained
(`dm_wilson_direct_descendant_canonical_transport_column_fiber_theorem_note_2026-04-19=audited_conditional`,
`dm_wilson_direct_descendant_canonical_fiber_schur_entropy_candidate_no_go_note_2026-04-19=audited_conditional`,
`dm_wilson_direct_descendant_local_schur_branch_discriminant_theorem_note_2026-04-19=audited_conditional`),
so the chain does not close under the leaf audit rule." The
audit-stated repair target (`notes_for_re_audit_if_any`) is exact:
"dependency_not_retained: audit or repair the listed dependency
rows to retained / equivalent closure, then re-audit this claim."
The generated audit ledger remains the authority for any terminal status. This is a **leaf
no-go** on the dm_wilson direct-descendant lane: it is a sibling
of `dm_wilson_direct_descendant_constructive_positive_closure_manifold_theorem_note_2026-04-18`
(currently `audited_conditional`) and it depends on the four named
canonical-fiber upstream rows registered in the audit
`dep_effective_status` block (canonical transport-column theorem,
canonical-fiber Schur-entropy candidate no-go, local Schur
branch-discriminant theorem, local observable-coordinate theorem).
All four upstream rows are themselves `audited_conditional` at the
2026-04-30 leaf-resweep, so the chain does not close even though
this row's three Theorems (Theorem 1: `alpha = 0` and `alpha = 1`
select different exact positive-fiber sources; Theorem 2: spectral
isotropy ↔ branch margin tradeoff; Theorem 3: both sampled members
miss the constructive path lane via aligned-seed `E1 < 0`) are
verified by the runner `PASS=9 FAIL=0`. The conditional perimeter
is therefore the audit-graph leaf-rule pending closure of the four
upstream canonical-fiber rows, not the runner-replay outcome.
Nothing in this edit promotes audit status; the note remains a
**conditional no-go** within the canonical-fiber chain. See
"Citation chain and audit-stated repair path (2026-05-10)" below.

```text
F_alpha(H_e)
  = H_Shannon(normalized Schur spectrum of H_e)
    + alpha log Delta_src(H_e),
```

where

```text
Delta_src(H_e) = det(H_e(L_e))
```

is the exact local branch-discriminant scalar. The result is still nonclosure:
`alpha` is load-bearing. Different exact members of this natural family select
different positive-fiber sources, and both sampled members still miss the
constructive path lane because their aligned-seed exact roots have `E1 < 0`.

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_canonical_fiber_mixed_spectral_branch_weight_no_go_2026_04_19.py`

## Question

After the canonical-fiber Schur-entropy note, the cleanest next positive idea
was:

1. keep the exact Shannon normalized-spectrum law as the shape term;
2. add the exact local branch scalar already derived from `L_e`,
   namely `log Delta_src`;
3. ask whether the natural mixed law

   ```text
   F_alpha = H_Shannon + alpha log Delta_src
   ```

   is now enough to fix the source without any further ambiguity.

This is a real test because the two ingredients are not imported from outside
the lane:

- `H_Shannon` is the strongest conditional spectral-shape candidate already
  isolated on the canonical fiber;
- `Delta_src = det(H_e(L_e))` is the exact local branch-discriminant scalar
  already proved on the descended Schur block.

Does the current branch now force a unique `alpha`?

## Bottom line

No.

The runner certifies two exact positive-fiber selectors from the same family:

- `alpha = 0` gives the Shannon point `S_0`;
- `alpha = 1` gives a distinct mixed-law point `S_1`.

Both satisfy the exact canonical orbit constraints and the retained positive
pack conditions

```text
gamma > 0, E1 > 0, E2 > 0, Delta_src > 0.
```

But they are genuinely different:

- `S_0` beats `S_1` on the `alpha = 0` law;
- `S_1` beats `S_0` on the `alpha = 1` law;
- the selected sources and observable packs are materially separated.

So `alpha` is not bookkeeping. It is a real missing selector datum.

The mixed family does sharpen the remaining gap. Turning on `alpha`

- raises the raw branch margin `Delta_src`,
- lowers the normalized spectral-isotropy score,
- and moves the right-sensitive even-response pair `(E1, E2)`.

So the current branch now knows the remaining source-fiber issue more sharply
than before:

> the missing object is not merely “some microscopic law on `L_e`”, but the
> unique weighting theorem between normalized spectral shape and raw branch
> margin, or a deeper theorem that bypasses this family entirely.

There is also one important downstream check:

- both sampled laws still produce aligned-seed exact `eta_1 = 1` roots with
  `E1 < 0`;
- so even this mixed family does not yet recover the constructive path lane.

## The natural mixed family

The previous same-day notes already isolated the two load-bearing scalar
ingredients on the canonical fiber:

1. **normalized Schur spectral shape**

   ```text
   p(H_e) = lambda(H_e) / Tr(H_e),
   H_Shannon(p) = -sum_i p_i log p_i;
   ```

2. **local branch margin**

   ```text
   Delta_src(H_e) = det(H_e(L_e)),
   log Delta_src.
   ```

Both are exact same-carrier scalars on the local descended block.

So the mixed family

```text
F_alpha = H_Shannon + alpha log Delta_src
```

is the most natural next family to test once one wants both:

- a spectral-shape term,
- and a right-sensitive branch-margin term.

If the current branch already fixed how these should be weighted, `alpha`
would not matter.

The runner shows that it does.

## Theorem 1: `alpha = 0` and `alpha = 1` select different exact positive-fiber sources

Write:

- `S_0` for the exact positive-fiber maximizer of `F_0 = H_Shannon`;
- `S_1` for the exact positive-fiber maximizer of
  `F_1 = H_Shannon + log Delta_src`.

The runner certifies:

- both `S_0` and `S_1` satisfy the exact canonical orbit constraints;
- both satisfy

  ```text
  gamma > 0, E1 > 0, E2 > 0, Delta_src > 0;
  ```

- but

  ```text
  F_0(S_0) > F_0(S_1),
  F_1(S_1) > F_1(S_0).
  ```

So the family is not secretly coefficient-free. The weight really changes the
selected source.

## Theorem 2: the family trades spectral isotropy against branch margin

The same comparison certifies:

- `Delta_src(S_1) > Delta_src(S_0)`;
- `H_Shannon(S_0) > H_Shannon(S_1)`;
- the even-response channels move:

  ```text
  E1(S_1) < E1(S_0),
  E2(S_1) < E2(S_0).
  ```

So the family is doing exactly what one would expect physically:

- higher `alpha` rewards larger raw local branch margin,
- at the cost of some normalized spectral isotropy,
- and that tradeoff is visible in the right-sensitive local observables.

That is why the coefficient cannot be ignored.

## Theorem 3: this family still misses the constructive path lane

For both sampled choices `alpha = 0` and `alpha = 1`, the runner also checks
the aligned-seed affine segment to the selected source.

In both cases:

- there is a unique exact `eta_1 = 1` crossing;
- but the crossing pack has

  ```text
  E1 < 0.
  ```

So even though the family is a real source-fiber law family, it does not yet
repair the downstream constructive path lane.

## Why this matters

This is the sharpest same-day narrowing after the entropy-only note.

Before this note, one could still say:

> maybe Shannon plus the exact local branch scalar already closes the fiber.

After this note, the honest statement is sharper:

> no; the combined family still carries one free real weight, and the
> currently sampled members do not recover the constructive downstream root.

So the remaining source-fiber object is no longer vague. It is one of:

1. a theorem fixing the mixed weight `alpha`;
2. a deeper exact local law on `L_e` that replaces this family;
3. or a bridge theorem showing why some other descended observable is the
   correct coefficient-free scalar.

That is a more precise scientific target than the older generic “microscopic
law on the fiber” wording.

## Cross-references

- [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_FIBER_SCHUR_ENTROPY_CANDIDATE_NO_GO_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_FIBER_SCHUR_ENTROPY_CANDIDATE_NO_GO_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md)

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_canonical_fiber_mixed_spectral_branch_weight_no_go_2026_04_19.py
```

Expected:

- `PASS=9 FAIL=0`

## Citation chain and audit-stated repair path (2026-05-10)

The audit verdict (2026-04-30 leaf-resweep, see top of note) flags
that the four named canonical-fiber upstream rows are themselves
`audited_conditional` and therefore the leaf-audit chain does not
close on this row. The cited authority chain is registered explicitly
below so the audit-graph one-hop edges from the source note to the
upstream canonical-fiber rows are visible.

| Cited authority | File / log | Audit-graph status (2026-05-10) | Role on this row |
|---|---|---|---|
| Active runner | [`scripts/frontier_dm_wilson_direct_descendant_canonical_fiber_mixed_spectral_branch_weight_no_go_2026_04_19.py`](../scripts/frontier_dm_wilson_direct_descendant_canonical_fiber_mixed_spectral_branch_weight_no_go_2026_04_19.py) | runner-replay verified `PASS=9 FAIL=0` | computes Theorems 1-3: certifies `S_0` (Shannon) and `S_1` (Shannon + log Δ_src) as different positive-fiber maximizers under the natural mixed family `F_alpha = H_Shannon + alpha log Delta_src`, the spectral-isotropy ↔ branch-margin tradeoff, and the aligned-seed `E1 < 0` miss for both sampled `alpha` values |
| Audit-lane runner cache | [`logs/runner-cache/frontier_dm_wilson_direct_descendant_canonical_fiber_mixed_spectral_branch_weight_no_go_2026_04_19.txt`](../logs/runner-cache/frontier_dm_wilson_direct_descendant_canonical_fiber_mixed_spectral_branch_weight_no_go_2026_04_19.txt) | runner-cache copy under `scripts/runner_cache.py` | runner-cache replay verifying `PASS=9 FAIL=0` |
| Upstream one-hop dep — canonical transport-column fiber theorem | [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md) | `audited_conditional` | reduces the live object to a local scalar law on the positive source fiber over the canonical favored column orbit (cited at top of note) |
| Upstream one-hop dep — canonical-fiber Schur-entropy candidate no-go | [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_FIBER_SCHUR_ENTROPY_CANDIDATE_NO_GO_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_FIBER_SCHUR_ENTROPY_CANDIDATE_NO_GO_NOTE_2026-04-19.md) | `audited_conditional` | establishes that Shannon-only (`alpha = 0`) is not the closure (cited as motivation for the mixed family in §"The natural mixed family") |
| Upstream one-hop dep — local Schur branch-discriminant theorem | [`docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_LOCAL_SCHUR_BRANCH_DISCRIMINANT_THEOREM_NOTE_2026-04-19.md) | `audited_conditional` | supplies the exact local branch-discriminant scalar `Delta_src(H_e) = det(H_e(L_e))` used as the second ingredient in the mixed family |
| Upstream one-hop dep — local observable-coordinate theorem | [`docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md) | `audited_conditional` | supplies the right-sensitive even-response observables `(E1, E2)` used in Theorems 2-3 |
| Sibling no-go — constructive positive closure manifold theorem | [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MANIFOLD_THEOREM_NOTE_2026-04-18.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_POSITIVE_CLOSURE_MANIFOLD_THEOREM_NOTE_2026-04-18.md) | `audited_conditional` (PR #718 landing) | sibling on the dm_wilson direct-descendant lane; same pattern of leaf no-go conditional on upstream canonical-fiber retention |
| Repo baseline anchor | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) | `unaudited` / `meta` | repo-baseline terminology anchor for the dm_wilson direct-descendant lane |

The audit-stated repair path (verbatim from the audit
`notes_for_re_audit_if_any`) is to **audit or repair the listed
dependency rows to retained / equivalent closure, then re-audit
this claim**. The four upstream rows are all leaf-resweep
`audited_conditional` at 2026-04-30; promotion of any one of them
would not by itself satisfy the leaf-audit closure rule, which
requires *all* one-hop dependencies to be retained or equivalent.
Until that upstream cluster lands as retained / retained_bounded,
the regenerated ledger leaves this row for independent audit, and the
safe read is the runner-replay-verified Theorems 1-3 conditional on the upstream
canonical-fiber chain. The acknowledged residual is the absence of
upstream-row retention; everything else (the mixed-family
no-closure structure, the spectral-isotropy ↔ branch-margin
tradeoff, the aligned-seed `E1 < 0` constructive-path miss, the
runner `PASS=9 FAIL=0`) is supported by the runner and the listed
cited authorities.

This rigorization edit only sharpens the conditional perimeter and
registers the cited authority chain; it does not promote audit
status, hand-author audit JSON, modify the runner, or change the
no-go conclusion. The §Verdict and §"Why this matters" boundaries
continue to apply: the canonical-fiber mixed family is a real
no-closure on this row, but its retained closure is conditional
on the four upstream canonical-fiber rows landing as retained.
