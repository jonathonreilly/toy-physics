# Koide Q RG fixed-point/source-origin no-go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_rg_fixed_point_origin_no_go.py`  
**Status:** no-go; Q not closed

## Theorem attempt

Try to derive the charged-lepton Q source law from retained
renormalization-group structure.  On the live normalized source fibre, write

```text
x = log(1 + rho).
```

The route asks whether Callan-Symanzik stationarity, an RG fixed point, or
anomalous-dimension stability can force the absolute source origin `x = 0`,
hence `rho = 0`, without importing `K_TL = 0` or `Q = 2/3`.

## Brainstormed routes

The runner tests:

1. Callan-Symanzik stationarity might force the absolute log-source origin;
2. an attractive RG fixed point `beta = 0` might select `x = 0`;
3. anomalous-dimension stability might distinguish the no-source section;
4. RG-invariant effective action might minimize only at the origin;
5. UV/IR endpoint behavior might identify the absolute subtraction scale;
6. wrong-assumption inversion: the same fixed-point law accepts `mu = log(2)`.

The strongest decisive route is translation-covariant fixed-point algebra.

## Result

The retained RG equations live on the source torsor.  They are equations in
the relative coordinate

```text
s = x - mu.
```

For the standard stable source beta function

```text
beta = -gamma (x - mu),
```

the fixed-point equation gives

```text
beta = 0 <=> x = mu.
```

The exact flow is

```text
x(t) = mu + (x0 - mu) exp(-gamma t),
```

so it converges to the supplied subtraction point `mu`, not to an absolute
retained origin.

More general translation-covariant beta functions behave the same way.  If

```text
beta(s) = s (s - r),
```

then the fixed roots are `s = 0` and `s = r`, hence

```text
x = mu
x = mu + r.
```

The roots are relative displacements.  They do not derive `mu = 0`.

## Countersection

The conditional closing case remains:

```text
mu = 0 -> rho = 0 -> K_TL = 0 -> Q = 2/3.
```

But the same exact retained fixed-point law also admits

```text
mu = log(2) -> rho = 1 -> K_TL = 3/8 -> Q = 1.
```

Therefore RG fixedness is not a retained Q closure theorem.

## Hostile review

- No Koide target is assumed.  The closing and counterclosing fixed lines are
  audited symmetrically.
- No PDG masses, observational `H_*` pin, `delta=2/9`, or Brannen-phase input
  appears.
- No new selector primitive is renamed as a theorem.  The missing theorem is
  named directly.
- Callan-Symanzik invariance protects relative source data; it does not
  choose the absolute subtraction point.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_rg_fixed_point_absolute_origin_mu_equals_zero
RESIDUAL_SOURCE = translation_covariant_rg_fixed_points_leave_mu_free
COUNTERSECTION = mu_log2_rg_fixed_line_rho_1_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 -m py_compile scripts/frontier_koide_q_rg_fixed_point_origin_no_go.py
python3 scripts/frontier_koide_q_rg_fixed_point_origin_no_go.py
```

Expected result:

```text
KOIDE_Q_RG_FIXED_POINT_ORIGIN_NO_GO=TRUE
Q_RG_FIXED_POINT_ORIGIN_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_RG_SUBTRACTION_POINT_MU_EQUALS_ZERO=TRUE
RESIDUAL_SCALAR=derive_retained_rg_fixed_point_absolute_origin_mu_equals_zero
```
