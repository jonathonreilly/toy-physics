# Koide Q source-fibre identity/preparation no-go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_source_fibre_identity_preparation_no_go.py`  
**Status:** executable no-go; not Q closure

## Theorem attempt

After the extremal-objective audit showed that zero-centered objectives select
`rho=0` only by supplying the zero center, the next stronger route was a
physical identity law: perhaps retained source composition or neutral
preparation makes the hidden source-fibre identity equal to `rho=0`.

The audit rejects that as retained-only closure.  A compositional source fibre
without a retained origin is an affine torsor.  For any identity value `e`,

```text
rho1 *_e rho2 = rho1 + rho2 - e
```

is associative, commutative, and has identity `e`.  Translation of the affine
coordinate sends the `e=0` law to the `e=c` law, so identity structure alone
does not distinguish the closing origin.

## Exact counteridentity

```text
e = 0
  Q = 2/3
  K_TL = 0
  closes conditionally

e = 1
  Q = 1
  K_TL = 3/8
  full-determinant counteridentity
```

Both values lie in the retained source-positive region `rho > -1`.  The
nonclosing `e=1` model has the same exact unit algebra:

```text
rho *_1 1 = rho = 1 *_1 rho.
```

## Probe/background distinction

Writing a relative source coordinate

```text
eta = rho - e
```

makes the chosen background identity look like zero.  But the zero-probe
condition `eta=0` gives only `rho=e`; it does not derive `e=0`.  Thus
renormalized subtraction and neutral-probe expansions cannot close Q unless
the retained origin law has already been proven.

## Hostile review

This no-go does **not** use:

- PDG charged-lepton masses;
- an observational `H_*` pin;
- `K_TL=0` as a theorem input;
- `K=0`;
- `P_Q=1/2`;
- `Q=2/3` as a theorem input;
- `delta=2/9`.

It treats `e=0` and `e=1` symmetrically as source-fibre identity choices.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_source_fibre_origin_identity_e_equals_zero
RESIDUAL_SOURCE = affine_source_torsor_identity_e_remains_free
COUNTERIDENTITY = e_1_full_determinant_Q_1_K_TL_3_over_8
```

## Consequence

The live Q route is now one notch sharper: a positive closure cannot merely
say "use the neutral source identity" or "expand at zero probe."  It must
derive why the retained physical source-fibre origin is the specific hidden
coordinate value `rho=0`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_source_fibre_identity_preparation_no_go.py
python3 scripts/frontier_koide_q_current_retained_source_class_exhaustion_no_go.py
python3 scripts/frontier_koide_q_residual_scalar_unification_no_go.py
```

Expected closeout:

```text
KOIDE_Q_SOURCE_FIBRE_IDENTITY_PREPARATION_NO_GO=TRUE
Q_SOURCE_FIBRE_IDENTITY_PREPARATION_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_SOURCE_FIBRE_ORIGIN_E_EQUALS_ZERO=TRUE
RESIDUAL_SCALAR=derive_retained_source_fibre_origin_identity_e_equals_zero
RESIDUAL_SOURCE=affine_source_torsor_identity_e_remains_free
COUNTERIDENTITY=e_1_full_determinant_Q_1_K_TL_3_over_8
```
