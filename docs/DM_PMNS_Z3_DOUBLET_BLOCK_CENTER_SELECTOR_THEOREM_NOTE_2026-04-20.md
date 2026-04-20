# DM PMNS `Z_3` Doublet-Block Center Selector Theorem

**Date:** 2026-04-20  
**Lane:** DM A-BCC sigma-chain / remaining open import `I5`  
**Status:** closes `I5` on this branch on the current theorem stack  
**Primary runner:**  
`scripts/frontier_dm_pmns_z3_doublet_block_center_selector_theorem_2026_04_20.py`

## 0. Question

After the exact `N_e` PMNS-manifold theorem and the `I12` sheet closure, is
there now a retained coefficient-free law that selects the physical PMNS angle
pin on the charged-lepton-side branch?

## 1. Bottom line

Yes.

The remaining `I5` object after
[DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md](./DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md)
was a point-selection law on the exact PMNS source manifold inside the fixed
native `N_e` seed surface. That point-selection law is now explicit.

Write the right-sensitive `Z_3` doublet-block target coordinates as

```text
delta_db(H) = (Im K_12(H) + 4 sqrt(2) / 3) / sqrt(3),
q_+(H)      = 2 sqrt(2) / 9 - Re(K_11(H) + K_22(H)) / 2,
```

where `K(H)` is the retained `Z_3` doublet block already used on the active
source-bank lane.

Then on the exact charged-lepton-side PMNS source manifold the coefficient-free
center law

```text
delta_db(H) = 1,
q_+(H)      = 0
```

cuts that manifold to exactly one two-sheet pair:

```text
(x_*, y_*, +delta_*), (x_*, y_*, -delta_*).
```

The pair shares the same `x` and `y` data and differs only by the sheet flip

```text
delta_src -> -delta_src,
gamma     -> -gamma,
I_src     -> -I_src.
```

The already-closed `I12` law `I_src(H) > 0` then selects the physical sheet
uniquely.

So `I5` is closed on this branch by the small complete retained system

```text
delta_db(H) = 1,
q_+(H)      = 0,
I_src(H)    > 0.
```

The first two laws are the new coefficient-free center law on the exact PMNS
manifold; the third law is the already-closed `I12` sheet selector.

## 2. Theorem

**Theorem (exact `Z_3` doublet-block center selector on the charged-lepton-side
PMNS manifold).** Let

```text
M_PMNS
  = F_Ne^(-1)(0.307, 0.0218, 0.545)
```

be the exact PMNS source manifold on the fixed native `N_e` seed surface from
the exact-manifold theorem. Then:

1. the exact system

   ```text
   F_Ne(x, y, delta_src) = (0.307, 0.0218, 0.545),
   delta_db(H_e)         = 1,
   q_+(H_e)              = 0
   ```

   has exactly two source solutions on the seed surface;
2. the two solutions have the same `x` and `y` data and opposite source phase
   `delta_src = ± delta_*`;
3. they therefore share the same aligned Hermitian core and differ only by the
   odd sheet data:

   ```text
   gamma -> -gamma,
   I_src -> -I_src,
   (cp1, cp2) -> -(cp1, cp2);
   ```

4. exactly one of the two center solutions satisfies `I_src(H) > 0`;
5. by the already-closed `I12` theorem, that positive-source-cubic sheet is
   the physical one.

Hence the retained system

```text
delta_db(H) = 1,
q_+(H)      = 0,
I_src(H)    > 0
```

selects a unique exact PMNS source on the charged-lepton-side branch. This
closes `I5` on the current theorem stack.

## 3. Exact selected source

The verifier finds the exact center pair

```text
x_* = (0.31922000..., 0.68397847..., 0.68680154...),
y_* = (0.41273682..., 0.09707923..., 0.41018395...),
delta_* = 0.728938949196...
```

with the two sheets

```text
(x_*, y_*, +delta_*),
(x_*, y_*, -delta_*).
```

Both reproduce

```text
(sin^2 theta_12, sin^2 theta_13, sin^2 theta_23)
  = (0.307, 0.0218, 0.545)
```

exactly to verifier tolerance, and both satisfy

```text
delta_db(H_e) = 1,
q_+(H_e)      = 0.
```

On the positive sheet:

```text
I_src(H_e) > 0,
(cp1, cp2) < 0.
```

On the negative sheet:

```text
I_src(H_e) < 0,
(cp1, cp2) > 0.
```

So the center law itself selects a unique two-sheet pair, and the existing
`I12` source-cubic law picks the physical member of that pair.

## 4. Why this closes `I5`

Before this note, the honest state of `I5` on this branch was:

- the PMNS CP-sign / `sigma_hier` half was already closed by `I12`;
- the physical PMNS angle triple was already known to lie on an exact regular
  `2`-real source manifold inside the fixed native `N_e` seed surface;
- what remained was exactly the missing point-selection law on that manifold.

This note supplies that law.

It does **not** replace the exact-manifold theorem. It completes it:

- the exact-manifold theorem gives the exact physical PMNS target manifold;
- the new center theorem gives a coefficient-free two-real selector on that
  manifold;
- the already-closed `I12` theorem resolves the residual sheet pair.

That is the whole remaining `I5` object on the current branch, so `I5` is now
closed.

## 5. Consequence for the register

The open-imports register entry for `I5` should now read:

```text
closed on this branch
```

with the exact reason:

```text
the exact PMNS source manifold is cut to an exact two-sheet center pair by the
coefficient-free Z_3 doublet-block center law delta_db = 1, q_+ = 0, and the
already-closed I12 source-cubic law I_src > 0 selects the physical sheet.
```

## 6. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_z3_doublet_block_center_selector_theorem_2026_04_20.py
```

Expected:

```text
PASS=15 FAIL=0
```
