# Koide Q KMS/modular-state no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_kms_modular_state_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use a finite KMS/modular equilibrium principle on the retained `C_3` sectors to
select the equal center-label state:

```text
KMS/modular equilibrium -> p_plus = p_perp -> K_TL = 0.
```

## Executable theorem

The retained sector multiplicities are:

```text
n_plus = 1
n_perp = 2.
```

A finite KMS state over the two sectors has weights

```text
p_i proportional to n_i exp(-beta E_i).
```

Writing

```text
x = exp(-beta (E_perp - E_plus)),
```

the runner verifies:

```text
p_plus = 1/(1+2x)
p_perp = 2x/(1+2x).
```

The source-neutral equal-label state occurs only at

```text
x = 1/2.
```

Equivalently:

```text
beta (E_perp - E_plus) = log(2).
```

## Obstruction

The degenerate or infinite-temperature KMS state has `x=1`, hence

```text
(p_plus,p_perp) = (1/3,2/3)
Q = 1
K_TL = 3/8.
```

So the most symmetric KMS state is the Hilbert/rank state, not the equal-label
state.  Equal labels require a new log-2 sector-gap equation.

## Residual

```text
RESIDUAL_SCALAR = beta_deltaE_minus_log2_equiv_center_label_state
RESIDUAL_MODULAR_GAP = beta_Eperp_minus_Eplus_minus_log2
```

## Why this is not closure

KMS/detailed-balance form constrains the shape of the state, but it does not
derive the required sector energy gap or temperature.  Choosing the gap to make
`x=1/2` is exactly the missing source-state law in thermal language.

## Falsifiers

- A retained charged-lepton sector Hamiltonian proving
  `beta(E_perp-E_plus)=log(2)`.
- A modular flow fixed by `Cl(3)/Z^3` whose unique KMS state is the equal-label
  state rather than the rank state.
- A physical reason that multiplicity is excluded from the KMS trace while
  preserving the retained real carrier.

## Boundaries

- Covers finite sector KMS states with multiplicities `1` and `2`.
- Does not exclude a future retained Hamiltonian or modular-flow theory that
  independently proves the log-2 gap.

## Hostile reviewer objections answered

- **"Thermal equilibrium is natural."**  With retained multiplicities and no
  sector gap, it gives the rank state.
- **"`log(2)` comes from the dimension ratio."**  Yes, but turning that into an
  energy-temperature equation is extra dynamics.
- **"Set the energies so equal labels result."**  That fits the residual; it
  does not derive it.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_kms_modular_state_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_KMS_MODULAR_STATE_NO_GO=TRUE
Q_KMS_MODULAR_STATE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=beta_deltaE_minus_log2_equiv_center_label_state
RESIDUAL_MODULAR_GAP=beta_Eperp_minus_Eplus_minus_log2
```
