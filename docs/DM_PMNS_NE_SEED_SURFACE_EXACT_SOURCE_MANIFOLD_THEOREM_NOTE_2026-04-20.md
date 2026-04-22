# DM PMNS Fixed `N_e` Seed-Surface Exact Source-Manifold Theorem

**Date:** 2026-04-20  
**Lane:** PMNS / `I5` remaining angle-pin task  
**Status:** theorem-grade reduction on the charged-lepton-side branch; not a
full positive `I5` closure  
**Does not close:** a framework-native point-selection law on the exact PMNS
source manifold  
**Dedicated verifier:**  
`scripts/frontier_dm_pmns_ne_seed_surface_exact_source_manifold_theorem_2026_04_20.py`

## Summary

The current `I5` gap is now sharper than “derive three PMNS angles somehow.”

On the fixed native `N_e` seed surface

```text
S_Ne
  = { (x,y,delta) :
      x_i > 0, y_i > 0,
      (x_1+x_2+x_3)/3 = Xbar_Ne,
      (y_1+y_2+y_3)/3 = Ybar_Ne } ,
```

with

```text
Xbar_Ne = 0.5633333333333334,
Ybar_Ne = 0.30666666666666664,
```

the physical PMNS angle triple

```text
(sin^2 theta_12, sin^2 theta_13, sin^2 theta_23)
  = (0.307, 0.0218, 0.545)
```

is already realized exactly.

But it is **not** realized as an isolated selected point on the current exact
stack. On the verified exact points, the PMNS-angle Jacobian on `S_Ne` has
rank `3`, so the exact preimage is a local `2`-real regular source manifold.
Current exact nonlocal seed-surface selector families miss that manifold by
macroscopic `chi^2`.

So `I5` is reduced to one much sharper remaining object:

> a new `2`-real point-selection law on the exact PMNS source manifold inside
> the fixed native `N_e` seed surface.

## 1. Setup

On the charged-lepton-side minimal PMNS branch, the canonical active block is

```text
Y_e = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C,
H_e = Y_e Y_e^dagger.
```

On the one-sided `N_e` branch, the PMNS packet is already the active packet

```text
|U_PMNS|^2 = |U_act(H_e)|^2^T.
```

So on `S_Ne` the PMNS angle map is the explicit exact map

```text
F_Ne(x,y,delta)
  = (sin^2 theta_12(H_e), sin^2 theta_13(H_e), sin^2 theta_23(H_e))
  in R^3.
```

The current theorem asks:

1. does `F_Ne` already hit the physical target triple exactly?
2. if yes, does the present exact selector stack on `S_Ne` already choose that
   point?

## 2. Theorem statement

**Theorem (exact PMNS manifold on the fixed native `N_e` seed surface, with
current nonlocal selector no-go).** On the fixed native `N_e` seed surface:

1. the physical PMNS angle triple lies in the image of `F_Ne`;
2. the verifier exhibits multiple distinct exact source points
   `p in S_Ne` with

   ```text
   F_Ne(p) = (0.307, 0.0218, 0.545)
   ```

   to numerical precision;
3. at each retained exact point, the Jacobian `dF_Ne` has rank `3`;
4. therefore, on the verified regular patch, the exact preimage

   ```text
   F_Ne^(-1)(0.307, 0.0218, 0.545)
   ```

   is a local `2`-real source manifold inside the `5`-real seed surface;
5. current exact nonlocal seed-surface selector-family points

   - aligned seed,
   - low-action stationary branch,
   - high-action stationary branch,
   - constructive `eta = 1` closure point,
   - constructive witness,

   all miss the target triple by macroscopic `chi^2 > 0.03`;
6. current selector observables vary along the exact PMNS manifold itself:
   the seed-relative relative action, transport outputs, and source cubic are
   not constant there.

Hence the current exact nonlocal selector stack does **not** close `I5` on the
charged-lepton-side branch. What remains is a genuinely new `2`-real
point-selection law on the exact PMNS source manifold.

## 3. Exact source representatives

The verifier certifies several exact source points. Three representative ones
are:

| rep | `x` | `y` | `delta` | `S_rel(H_e || H_seed)` | `eta / eta_obs` | source cubic |
|---|---|---|---:|---:|---:|---:|
| A | `(0.060928, 0.750228, 0.878844)` | `(0.498479, 0.245209, 0.176312)` | `-1.533871` | `4.302174` | `(0.777873, 0.700284, 0.827267)` | `-8.65e-4` |
| B | `(0.172810, 0.702009, 0.815181)` | `(0.453865, 0.263544, 0.202591)` | `0.789612` | `1.938594` | `(0.775999, 0.699960, 0.827260)` | `+1.70e-3` |
| C | `(0.284724, 0.657377, 0.747899)` | `(0.396580, 0.281713, 0.241707)` | `-0.635221` | `0.905124` | `(0.769934, 0.698837, 0.827234)` | `-2.24e-3` |

All three reproduce

```text
(sin^2 theta_12, sin^2 theta_13, sin^2 theta_23)
  = (0.307, 0.0218, 0.545)
```

to the verifier tolerance.

The important point is not the specific coordinates. It is that these points
are **distinct**, yet all live on the same exact PMNS target fiber.

## 4. Regular-manifold consequence

The seed surface `S_Ne` is `5`-real dimensional. The verifier computes the
finite-difference Jacobian of

```text
F_Ne : S_Ne -> R^3
```

at the retained exact points and finds

```text
rank dF_Ne = 3.
```

So on that regular patch, the implicit-function heuristic is the correct one:
the exact physical PMNS target is not an isolated source. It is a local
`2`-real manifold.

This is the sharp new reduction:

- existence of exact PMNS points is no longer the live issue;
- branch isolation is no longer the live issue on this patch;
- the live issue is selecting one point on that exact source manifold.

## 5. Current selector-family miss

The verifier checks the current exact nonlocal selector-family points already
on branch:

| selector-family point | PMNS triple | `chi^2` to target |
|---|---|---:|
| aligned seed | `(0.200000, 0.166667, 0.600000)` | `0.035460` |
| low-action stationary | `(0.921382, 0.546423, 0.003479)` | `0.945939` |
| high-action stationary | `(0.950756, 0.094768, 0.962175)` | `0.593782` |
| constructive `eta=1` closure | `(0.701614, 0.911995, 0.865291)` | `1.050754` |
| constructive witness | `(0.737048, 0.951639, 0.878470)` | `1.160744` |

So the current exact seed-surface selector families do **not** land on the
physical PMNS manifold. This is the nonlocal analogue of the later Schur-line
no-go:

- local selector families miss the PMNS target on the active DM source sheet;
- current nonlocal seed-surface selector families miss the PMNS target on the
  charged-lepton-side fixed-seed sheet.

## 6. Why this is stronger than “still open”

Before this theorem, “`I5` is still open” still left two qualitatively
different possibilities:

1. maybe the physical PMNS point is not even present on the exact retained
   charged-lepton-side seed surface;
2. maybe it is present, but the retained selector stack still does not choose
   it.

This theorem closes the first possibility positively and the second
negatively.

So the sharpened honest state is:

- the physical PMNS angle triple is already exact on the fixed native `N_e`
  seed surface;
- the current exact nonlocal selector stack does not pick it;
- the remaining `I5` target is a new `2`-real point-selection law on that
  exact manifold.

## 7. Consequence for `I5`

`I5` is not closed by this note.

But it is reduced substantially.

The old phrasing

```text
derive the PMNS angle triple
```

can now be sharpened on the charged-lepton-side branch to

```text
derive a point-selection law on the exact 2-real PMNS source manifold
inside the fixed native N_e seed surface.
```

Equivalently:

- the seed pair is already exact,
- the branch-local carrier already contains the physical PMNS triple,
- the remaining science is no longer existence or branch hunting,
- it is the missing point-selection law on the exact source manifold.

That is the correct `I5` reduction to cite after this theorem.

## 8. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_ne_seed_surface_exact_source_manifold_theorem_2026_04_20.py
```

Expected:

```text
PASS=12 FAIL=0
```
