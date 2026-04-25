# Koide Q Observable/Morita Orbit-Invisibility No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_observable_morita_orbit_invisibility_no_go.py`  
**Status:** executable no-go for deriving orbit invisibility from current retained structure

## Theorem Attempt

Prove the requested theorem:

```text
the retained C3 orbit type {0} versus {1,2} is not source-visible after
observable/Morita reduction.
```

If true, the stabilized center exchange is physical, the center state is
`lambda=1/2`, and the Q chain closes.

## Exact Audit

After observable/Morita reduction, the center still contains:

```text
P_plus, P_perp
```

and the retained label coordinate:

```text
Z = P_plus - P_perp.
```

The runner verifies:

```text
Z P_plus = P_plus
Z P_perp = -P_perp
Z^2 = I.
```

Morita normalization removes matrix amplification rank, and the reduced
observable one-slot jets are identical.  But neither operation sets:

```text
Z = 0.
```

## Counterfunctional

The source functional:

```text
rho -> tr(Z rho)
```

is stable, central, and `C3`-invariant.  It separates the two retained orbit
types:

```text
tr(Z P_plus) = 1
tr(Z P_perp) = -1.
```

Therefore the current retained package does not prove orbit invisibility.

## Residual

The missing theorem is:

```text
derive_observable_Morita_source_domain_forgets_C3_orbit_type.
```

Equivalently, prove that physical source preparation factors through the
anonymous observable-jet/Morita quotient and not through retained `C3` orbit
labels.

## Verdict

```text
KOIDE_Q_OBSERVABLE_MORITA_ORBIT_INVISIBILITY_NO_GO=TRUE
Q_OBSERVABLE_MORITA_ORBIT_INVISIBILITY_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_ORBIT_TYPE_IS_SOURCE_INVISIBLE=TRUE
RESIDUAL_SCALAR=derive_observable_Morita_source_domain_forgets_C3_orbit_type
RESIDUAL_SOURCE=stable_C3_invariant_label_functional_tr_Z_rho_not_excluded
COUNTERSTATE=rank_K0_center_state_lambda_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_observable_morita_orbit_invisibility_no_go.py
python3 -m py_compile scripts/frontier_koide_q_observable_morita_orbit_invisibility_no_go.py
```
