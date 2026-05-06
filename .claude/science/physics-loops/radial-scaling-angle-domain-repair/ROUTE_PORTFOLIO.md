# Route Portfolio

## R1: Finite-Tangent Domain Repair

Status: executed.

Repair T4 by explicitly restricting the `(1,0)`-based tangent equality to the
finite-tangent subdomain `rho != 1` and `mu*rho != 1`, then prove

```text
tan(beta_bar) - tan(beta)
  = eta*(mu - 1)/((1 - mu*rho)*(1 - rho)).
```

This closes the auditor-identified gap without changing T1-T3 or importing any
CKM-specific data.

## R2: Demote T4 To Example Only

Status: rejected.

This would avoid the overbroad universal statement but would lose a useful
exact counter-protection theorem. R1 is stronger and still zero-input.

## R3: Drop The `(1,0)` Angle Entirely

Status: rejected.

The audit did not object to the counter-protection idea; it objected to the
missing denominator domain. Dropping T4 would be unnecessary.
