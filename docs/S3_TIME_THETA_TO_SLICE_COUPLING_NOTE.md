# Route 2 Readout to Slice Coupling

**Status:** open_gate route survey — exact conditional readout-to-slice
coupling family obtained by composing cited upstream authorities, with the
unique-exact `Theta_R -> Lambda_R` coupling theorem **not** closed because
the underlying readout-map endpoint triple is not yet derived.
**Date:** 2026-04-19 (audit-narrowing refresh: 2026-05-10)
**Purpose:** state the current exact status of the Route-2 (s3-time)
`Theta_R -> Lambda_R` coupling problem after the exact bilinear carrier and
the audited Route-2 readout / time-coupling notes.
**Type:** open_gate
**Status authority:** independent audit lane only.
**Authority role:** records, but does not close, the s3-time arm of the
Route-2 readout-to-slice coupling family. Names the missing readout-map
endpoint triple as the single open theorem target for this row.

## Audit boundary

This note assembles a conditional Route-2 coupling family on the s3-time
arm by importing four upstream authorities and combining them
algebraically. It is **not** a derivation of the underlying carrier,
slice backbone, or readout map.

**Cited authorities (one-hop deps; cited but not closed in this note):**

- [`QUARK_ROUTE2_EXACT_TIME_COUPLING_NOTE_2026-04-19.md`](QUARK_ROUTE2_EXACT_TIME_COUPLING_NOTE_2026-04-19.md)
  (`claim_type: bounded_theorem`, `audit_status: audited_clean`) —
  canonical Route-2 slice backbone authority. Supplies the exact slice
  generator `Lambda_R` (SPD), the transfer matrix `T_R = exp(-Lambda_R)`,
  the seed law `V_R(t) = exp(-t Lambda_R) u_*`, and the conditional
  coupling family `Xi_P(t ; c) = (P_R c) ⊗ V_R(t)` once an admissible
  readout map `P_R` is supplied. Imported as the slice-backbone authority
  for this s3-time arm.
- [`QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md`](QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md)
  (`claim_type: no_go`, `audit_status: audited_clean`) — canonical
  Route-2 readout-map authority. Establishes the exact bilinear carrier
  `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`, the restricted
  bright readout class
  `gamma_E = alpha_E u_E + beta_E delta_A1 u_E`,
  `gamma_T = alpha_T u_T + beta_T delta_A1 u_T`, and the
  **audited-clean no-go** that the endpoint dimensionless triple
  `(beta_T / alpha_T, alpha_T / alpha_E, beta_E / alpha_E) = (-1, -2, 21/4)`
  is not derived by the current exact stack. Imported as the readout-class
  authority and as the canonical statement of the open obstruction this
  row inherits.
- [`QUARK_ROUTE2_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md`](QUARK_ROUTE2_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md)
  (`claim_type: no_go`, `audit_status: audited_conditional` as of the
  2026-05-10 fresh audit; previously `audited_clean`) — companion
  source-domain bridge no-go on the same Route-2 arm; cited for
  cross-confirmation that the readout-map blocker is not bypassed by a
  source-domain detour, with the source-domain typed-edge inventory now
  flagged as configured (hard-coded in the runner) rather than derived.
  This row inherits that conditional status; it does not bypass it.

**Admitted-context derivation gap (real, not import-redirect):**

The unique exact `Theta_R -> Lambda_R` coupling theorem on this s3-time
arm requires the readout-map endpoint triple to be derived. The cited
[`QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md`](QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md)
records this as an **audited-clean no-go**: the exact endpoint triple is
not derived by the current exact stack on `main`. This row inherits that
no-go and does not bypass it.

## Verdict (scope-bounded)

Conditional on the cited upstream authorities, this row records:

- exact slice backbone `Lambda_R`, `T_R = exp(-Lambda_R)`,
  `V_R(t) = exp(-t Lambda_R) u_*` — imported from the Route-2 time-coupling
  authority;
- exact bilinear carrier `K_R(q)` and restricted bright readout class —
  imported from the Route-2 readout-map authority;
- exact conditional coupling family
  `Xi_P(t ; c) = (P_R c) ⊗ V_R(t)`
  obtained algebraically once an admissible readout map `P_R` is supplied;
- explicit absence, on `main`, of any retained-grade derivation of the
  readout-map endpoint triple, and therefore explicit absence of any
  unique exact `Theta_R -> Lambda_R` coupling theorem on this arm.

So the honest endpoint is:

> exact conditional coupling family obtained by composing cited Route-2
> authorities; exact induced obstruction to uniqueness inherited from the
> Route-2 readout-map no-go.

## Exact ingredients already available

### Carrier

- `K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`

### Readout class

- restricted bright form
  `gamma_E = alpha_E u_E + beta_E delta_A1 u_E`
  `gamma_T = alpha_T u_T + beta_T delta_A1 u_T`

### Slice backbone

- exact `Lambda_R`
- exact `T_R = exp(-Lambda_R)`
- exact seed law `V_R(t) = exp(-t Lambda_R) u_*`

## Exact conditional coupling family

Once an admissible readout map `P_R` is chosen, the current branch supports
the exact family

```text
Xi_P(t ; c) = (P_R c) ⊗ V_R(t)
```

for every restricted carrier column `c`.

This is exact because:

1. `c` is exact,
2. `P_R` is algebraic once specified,
3. `V_R(t)` is exact.

So the route does not lack a carrier-to-slice construction anymore.

## Why the unique theorem is still blocked

The cited
[`QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md`](QUARK_ROUTE2_EXACT_READOUT_MAP_NOTE_2026-04-19.md)
records as an audited-clean no-go that the endpoint triple

```text
beta_T / alpha_T = -1
alpha_T / alpha_E = -2
beta_E / alpha_E = 21/4
```

is **not** derived by the current exact stack on `main`. Therefore the
readout map remains non-unique on the restricted class, and the unique
exact `Theta_R -> Lambda_R` coupling theorem is **not** closed on this
s3-time arm.

The cited Route-2 readout-map note documents the obstruction directly:

- distinct exact admissible maps agree at shell normalization,
- but produce different center `E` source factors,
- so they produce different exact spacetime tensors on the same slice
  backbone.

The ambiguity is therefore localized to the unresolved readout-map
endpoint triple — not to `Lambda_R` (audited_clean) and not to the
carrier `K_R` (audited_clean). This row imports that localization and
does **not** bypass it.

## Current blocker

The blocker is now very precise:

> unresolved readout exactness blocks a unique exact `Theta_R -> Lambda_R`
> coupling law on the current carrier.

This is sharper than the older “missing tensor observable” statement, because
the carrier and the slice semigroup are already exact.

## Bottom line

Conditional on the cited upstream authorities, this row records:

- exact carrier (imported from Route-2 readout-map authority),
- exact slice backbone (imported from Route-2 time-coupling authority),
- exact conditional readout-to-slice family obtained algebraically from
  the imports,
- no unique exact `Theta_R -> Lambda_R` coupling theorem on this arm,
  because the readout-map endpoint triple is not derived (no-go inherited
  from the cited Route-2 readout-map authority).

The next theorem target is the missing readout-map endpoint triple. That
target lives on the upstream readout-map row, not on this row. This row
remains `open_gate` until that target closes upstream.
