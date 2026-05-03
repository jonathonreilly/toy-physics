# DM PMNS `Z_3` Doublet-Block Center Positive-Sheet No-Go Theorem

**Date:** 2026-04-20 (originally); 2026-05-03 (audit-driven runner repair via PR #485)
**Lane:** DM A-BCC / remaining open import `I5`
**Status:** honest no-go on the current theorem stack; runner PASS=12/0 after PR #485 register-check repair
**Primary runner:**
`scripts/frontier_dm_pmns_z3_doublet_block_center_positive_sheet_no_go_2026_04_20.py`

## Audit-driven repair (2026-05-03)

The 2026-05-03 audit (codex-current-fresh-context) recorded the runner
at PASS=11/1: the geometric no-go content (PARTS 1–3) passed cleanly,
but PART 4's register-consistency check looked for a `| I5 |` row plus
`point-selection law` and `retained observational input` strings in
`SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md`. That register
has since been refactored to focus on Koide-related imports and no
longer enumerates an explicit I5 row.

The 2026-05-03 runner repair (landed in PR #485, commit `46d9fda67`)
points the PART 4 check at the current authoritative I5 status note
(`DM_PMNS_LOCAL_SELECTOR_FAMILY_NO_GO_THEOREM_NOTE_2026-04-20.md`),
which carries the literal `I5 is still open positively` line. Runner
now PASS=12/0. The no-go geometry was already ratified correct in
the audit; this clears the brittle string-match block, so re-audit
can now ratify the full row as `retained_no_go` via the proper
`claim_type=no_go + audited_clean` path.

The substantive content of the no-go (positive-sheet center locus has
many distinct exact solutions; PMNS angle triple varies macroscopically
across it; center law is conditional on the exact PMNS target, not a
native I5 closure) is unchanged by this repair.

## Summary

The recently proposed coefficient-free `Z_3` doublet-block center law

```text
delta_db(H) = 1,
q_+(H)      = 0
```

is structurally meaningful, but on the charged-lepton-side fixed native `N_e`
seed surface it does **not** close `I5` by itself, even after adding the
already-closed sheet law

```text
I_src(H) > 0.
```

The reason is geometric and explicit:

1. on the fixed `N_e` seed surface, the positive-sheet center system

   ```text
   delta_db(H) = 1,
   q_+(H)      = 0,
   I_src(H)    > 0
   ```

   still has many distinct exact source solutions;
2. at retained representatives, the Jacobian of the center pair
   `(delta_db, q_+)` has rank `2`, so the center locus is locally a `3`-real
   manifold inside the `5`-real seed surface;
3. the PMNS angle triple varies macroscopically along that positive center
   locus.

So the center law plus the `I12` sign law does **not** derive the PMNS angle
triple. It leaves a large positive-sheet family.

What the center law *does* give honestly is a useful conditional reduction:
once the exact PMNS target manifold is imposed, the center equations cut that
manifold to a two-sheet pair, and the already-closed `I12` law selects the
physical sheet. That is a real structural observation, but it is not a native
closure of `I5` because the PMNS target manifold itself is still observational.

## 1. Setup

On the fixed native `N_e` seed surface from
`DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md`,
define the center coordinates by the retained right-sensitive `Z_3`
doublet-block readout

```text
delta_db(H) = (Im K_12(H) + 4 sqrt(2) / 3) / sqrt(3),
q_+(H)      = 2 sqrt(2) / 9 - Re(K_11(H) + K_22(H)) / 2.
```

The proposed closeout system was

```text
delta_db(H) = 1,
q_+(H)      = 0,
I_src(H)    > 0.
```

The question is whether this already forces the physical PMNS angle triple

```text
(sin^2 theta_12, sin^2 theta_13, sin^2 theta_23)
  = (0.307, 0.0218, 0.545)
```

without separately imposing that target.

## 2. Theorem

**Theorem (`Z_3` doublet-block center positive-sheet no-go).** On the fixed
native `N_e` seed surface:

1. the positive-sheet center system

   ```text
   delta_db(H) = 1,
   q_+(H)      = 0,
   I_src(H)    > 0
   ```

   has multiple distinct exact source solutions;
2. at retained representative points, the Jacobian of the center pair
   `(delta_db, q_+)` has rank `2`;
3. hence the center system defines, on the verified patch, a local `3`-real
   positive-sheet center locus;
4. the PMNS angle triple varies macroscopically along that locus.

Therefore the current center law plus the already-closed `I12` sign law does
**not** close `I5`.

## 3. Retained positive-sheet center representatives

The verifier finds many exact positive-sheet center points. Representative
examples include

```text
(0.243800, 0.075946, 0.808903),
(0.943631, 0.030502, 0.124926),
(0.621613, 0.597343, 0.995705)
```

for the PMNS triple

```text
(sin^2 theta_12, sin^2 theta_13, sin^2 theta_23),
```

all with

```text
delta_db(H) = 1,
q_+(H)      = 0,
I_src(H)    > 0.
```

These triples are visibly different from one another, so the positive-sheet
center law is not a point selector.

## 4. Why the geometric conclusion is unavoidable

The fixed `N_e` seed surface is `5`-real dimensional. The center law supplies
two real equations. On the retained representative points the verifier finds

```text
rank d(delta_db, q_+) = 2.
```

So the center equations cut the seed surface to a local `3`-real locus.
Adding the already-closed sign condition `I_src > 0` selects one sheet of that
locus, but does not reduce its local dimension.

Since the PMNS angle triple varies along the resulting positive-sheet center
locus, the current center proposal cannot derive the PMNS target on its own.

## 5. Honest conditional value of the center law

The center law is still useful, just not as a full closure.

If one first imposes the exact PMNS target manifold from the exact-manifold
theorem, then the center equations cut that target manifold to a two-sheet
pair, and the already-closed `I12` law `I_src > 0` selects the physical sheet.

So the valid conclusion is:

```text
exact PMNS manifold + center law + I12  ->  unique physical sheet,
```

not

```text
center law + I12  ->  PMNS target.
```

That distinction is exactly the difference between a useful conditional
reduction and a native closure of `I5`.

## 6. Consequence for `I5`

`I5` remains open on this branch.

After the exact-source-manifold theorem and the present no-go, the remaining
live object is sharper:

```text
derive the additional selector on the positive-sheet center locus
```

or equivalently

```text
derive the point-selection law on the exact PMNS source manifold that is
stronger than the current center law delta_db = 1, q_+ = 0.
```

So the current center theorem should be read as a conditional reduction tool,
not as the closeout of `I5`.

## 7. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_z3_doublet_block_center_positive_sheet_no_go_2026_04_20.py
```

Expected:

```text
PASS=12 FAIL=0
```
