# Koide delta Z3 Wilson d2-power quantization no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_z3_wilson_d2_power_quantization_no_go.py`  
**Status:** executable no-go; Route-3 Wilson power law remains an explicit primitive

## Theorem Attempt

Derive the Route-3 law

```text
W_Z3^(d^2) = exp(2i) 1,  d = 3,
```

so that the selected endpoint phase is `2/d^2 = 2/9`.

## Result

Negative.  The retained finite `C3` generator satisfies

```text
C^3 = 1,  C^9 = 1.
```

A phase-twisted generator `W(phi)=exp(i phi) C` has

```text
W^3 = exp(3 i phi),  W^9 = exp(9 i phi).
```

If it is still the retained finite `C3` action, `W^3=1`, so `W^9=1`, not
`exp(2i)`.  If instead `W^9=exp(2i)` is imposed, then `phi=2/9` modulo the
orbit convention and `W^3=exp(2i/3)`, so the construction has introduced a new
`U(1)` Wilson holonomy.

## Projective And Spin-Lift Checks

The spin lift gives a cubic sign and hence `W^9=-1`, also not `exp(2i)`.
Projective generator phases are rephasable:

```text
W -> exp(i alpha) W.
```

Thus the central cubic phase is not a retained invariant unit.  Choosing
`exp(2i/3)` is the missing endpoint/radian law.

## Residual

```text
RESIDUAL_PRIMITIVE = retained_U1_Wilson_radian_unit_on_selected_endpoint
COUNTERSTATE = finite_C3_or_spin_lift_W9_not_exp_2i
NEXT_ATTACK = lattice_propagator_radian_quantum_or_hw1_baryon_Wilson_holonomy
```

## Hostile Review

This does not close delta.  It shows that the Route-3 Wilson power law is not
a consequence of retained finite `C3`, spin-lift, or projective-representation
data.  A positive closure still needs a physical theorem selecting the
`U(1)` Wilson action/radian unit before the `2/9` endpoint is read out.

## Verification

```bash
python3 scripts/frontier_koide_delta_z3_wilson_d2_power_quantization_no_go.py
python3 -m py_compile scripts/frontier_koide_delta_z3_wilson_d2_power_quantization_no_go.py
```
