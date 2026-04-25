# Koide Q No-New-Axiom Separation No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_no_new_axiom_separation_no_go.py`  
**Status:** no-go under current retained constraints; sharp next search criterion

## Theorem Attempt

Under the user's no-new-axioms constraint, try to derive the Q source law from
only the currently audited retained Cl(3)/Z3 charged-lepton carrier,
source-response, symmetry, Morita, gauge, anomaly, RG, and no-observational-pin
constraints.

## Exact Separation

The runner exhibits a one-parameter source-response family:

```text
W_rho = log(1+k_plus) + (1+rho) log(1+k_perp).
```

The hidden quotient-kernel source charge is `rho`.  Two exact models satisfy
the same audited retained constraints:

```text
M_close:   rho = 0, reduced/quotient source response, Q = 2/3, K_TL = 0
M_counter: rho = 1, full rank-visible determinant response, Q = 1, K_TL = 3/8
```

The audited retained equality constraints have zero Jacobian rank in `rho`.
The source-positivity inequalities, C3/gauge invariance, tensor repetition,
and zero anomaly/RG equations accept both models.

## Consequence

Any theorem from the currently audited retained constraints must hold in
`M_counter`.  Since `M_counter` has `K_TL = 3/8` and `Q = 1`, those constraints
do not entail the desired source law.

This is not a license to add a new axiom.  It gives the exact no-new-axiom
search criterion:

```text
find an already-retained source-side equality with Jacobian rank 1 in rho.
```

Without that existing retained equation, the current audited retained package
cannot force `rho = 0`.

## Hostile Review

This note does not claim closure and does not assume:

- `K_TL = 0`;
- `K = 0`;
- `P_Q = 1/2`;
- `Q = 2/3`;
- `delta = 2/9`;
- PDG mass matching;
- an observational `H_*` pin;
- a renamed source-selector primitive.

The values `Q = 2/3` and `Q = 1` are consequences of two symbolic source
models, not inputs to the theorem.

## Residual

```text
RESIDUAL_SCALAR = find_existing_retained_equation_setting_hidden_kernel_charge_rho_to_zero
RESIDUAL_SOURCE = audited_retained_constraints_have_zero_rank_on_rho
COUNTERMODEL_PAIR = M_close_rho_0_and_M_counter_rho_1
NEXT_SEARCH_CRITERION = existing_retained_source_equality_with_jacobian_rank_1_in_rho
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_no_new_axiom_separation_no_go.py
python3 -m py_compile scripts/frontier_koide_q_no_new_axiom_separation_no_go.py
python3 scripts/frontier_koide_q_current_retained_source_class_exhaustion_no_go.py
python3 scripts/frontier_koide_q_residual_scalar_unification_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_NO_NEW_AXIOM_SEPARATION_NO_GO=TRUE
Q_NO_NEW_AXIOM_SEPARATION_CLOSES_Q_RETAINED_ONLY=FALSE
COUNTERMODEL_PAIR=M_close_rho_0_and_M_counter_rho_1
RESIDUAL_SCALAR=find_existing_retained_equation_setting_hidden_kernel_charge_rho_to_zero
NEXT_SEARCH_CRITERION=existing_retained_source_equality_with_jacobian_rank_1_in_rho
```
