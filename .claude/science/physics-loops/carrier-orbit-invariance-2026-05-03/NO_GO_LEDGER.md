# No-Go Ledger — Cycle 22

## Routes rejected before execution

- **Route C (cohomological):** rejected because for a Z_2 action on a
  finite-dimensional carrier, H^1(BZ_2; V^-) reduces algebraically to
  the same Z_2-isotypic decomposition that Route B uses directly. The
  cohomological framing adds no content beyond the rep-theoretic
  argument.
- **Route D (sheaf-theoretic):** rejected for the same content vs.
  machinery tradeoff. Sheaves on a finite base are equivalent to the
  rep-theoretic argument.

## Premises NOT proved

- **Closure of retained primitive registry**: cycle 22 does NOT prove
  that the audited registry is exhaustive. Future retained primitives
  could in principle have nontrivial antisymmetric component. This is
  a meta-mathematical premise about the registry itself, not a
  statement provable on the current axiomatic surface.

## Counterfactual hypotheticals tested

- **What if a future retained primitive Z were antisymmetric?** Cycle
  22 tests this hypothetically: such a Z would yield Tr(Z · K_R) ≠
  Tr(Z · K_R · P_ET) for some carrier instance, and would directly
  break the swap-reduction. The runner verifies that NO currently
  retained primitive has this property by enumeration of the active
  Hermitian basis (a, b, c, d, T_delta, T_rho).

## Falsified candidates

- **Naive antisymmetric candidates:**
  - Z_diff = diag(1, -1) on the carrier: this is the carrier-row
    (top-row vs bottom-row distinction), NOT the column distinction.
    It distinguishes the delta_A1 weight, not E vs T.
  - Z_col_diff = "column 1 - column 2": this IS antisymmetric, but it
    is not a retained framework primitive — it is the very
    swap-asymmetric operator the registry is being checked against. As
    such it appears in NEITHER Theta_R^(0) NOR Xi_R^(0) NOR the active
    Hermitian basis (a, b, c, d, T_delta, T_rho).

These tests confirm: any candidate antisymmetric operator on the
carrier corresponds to a primitive that is NOT currently retained.

## Hard residuals from prior cycles

This cycle does NOT attempt to close:
- Cycle 08 obstructions (composite-Higgs mechanism, m_top, multi-bilinear)
- Cycle 09 obstructions (K_H, thermal scattering, branch selector)
- Cycle 12 O3 (M_i scales)
- Cycle 15 R1, R2, R3 (v-scale running residuals)

These are scoped to other lanes/cycles.
