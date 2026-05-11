# Lane 1 `sqrt(sigma)` B2 Static-Energy Bridge Scout

**Date:** 2026-04-30
**Status:** support / bridge scout; no theorem or claim promotion. This
note tests whether modern full-QCD static-energy or force-scale
literature can replace the rough x0.96 `(B2)` screening factor in the
Lane 1 `sqrt(sigma)` gate.
**Script:** `scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py`
**Lane:** 1 - Hadron mass program, route 3E `sqrt(sigma)` retained
promotion.

**Status authority and audit hygiene (2026-05-10):**
The audit lane has classified this note `audited_conditional` (verdict
2026-05-05). The runner's PASS=12 arithmetic and consistency checks on
embedded TUMQCD/CLS values are sound, and the scout conclusion -- "modern
full-QCD static-energy data strengthen the B2 bridge but do not promote
the Lane 1 `sqrt(sigma)` row" -- is properly bounded and open by
construction. The audit-conditional verdict reflects exactly what this
note already says: the load-bearing scientific step is an external
comparator/gate assessment, not a first-principles derivation from the
axiom, and both the `sigma` convention/window and the B5
framework-to-standard-QCD link remain open. This rigorization edit makes
that conditional perimeter explicit; nothing here promotes audit_status.

---

## 0. Result

Modern full-QCD static-energy results are useful B2 bridge material, but
they do **not promote** the repo's `sqrt(sigma)` row from bounded to
retained.

The reason is precise:

- the clean `N_f=2+1` object is a static-force scale such as `r0` or
  `r1`, not an asymptotic full-QCD string tension;
- the available finite-window static-energy `sigma` value is convention
  dependent at the few-percent level;
- the framework-to-standard-QCD `(B5)` link remains open.

So Cycle 2 keeps B2 live but upgrades the next route from "invent a
screening factor" to a concrete bridge table:

```text
B2a: choose static-force scale or finite-window effective tension.
B2b: import that value with its uncertainty and convention split.
B5: declare the framework-to-standard-QCD residual.
```

## 1. Source Values

### 1.1 `N_f=2+1+1` static-energy fit-window sigma

The TUMQCD static-energy analysis reports, in its continuum section:

```text
r0 = 0.4547 +/- 0.0064 fm
r0/r1 = 1.4968 +/- 0.0069
r0 sqrt(sigma) = 1.077 +/- 0.016  (A = A_r0)
r0 sqrt(sigma) = 1.110 +/- 0.016  (A = pi/12)
```

Converted using `hbar c = 197.327 MeV fm`:

```text
sqrt(sigma) = 467.39 +/- 9.57 MeV  (A = A_r0)
sqrt(sigma) = 481.71 +/- 9.70 MeV  (A = pi/12)
```

The two static-potential convention choices differ by about 14.3 MeV,
or 3.0 percent. That is larger than a sub-percent retention target and
must remain a bridge residual.

Interpretation:

- the `A = A_r0` value is close to the repo's rough x0.96 value
  (`464.75 MeV`);
- the `A = pi/12` value is close to the repo's quenched Method 2 value
  (`484.11 MeV`);
- therefore the literature does not define one unique dynamical
  screening factor.

### 1.2 `N_f=2+1` force scales

The 2025 CLS `N_f=2+1` potential-scale determination reports:

```text
r0 = 0.4729(57)(48) fm
r1 = 0.3127(24)(32) fm
r0/r1 = 1.532(12)
```

These are clean static-force scales. They avoid the asymptotic
string-tension problem because they are defined by `r^2 F(r) = c_i`.
But by themselves they do not provide a unique `sqrt(sigma)` value.

As a diagnostic only, applying the TUMQCD dimensionless
`r0 sqrt(sigma)` values to the CLS `r0` scale gives:

```text
sqrt(sigma) ~= 449.52 MeV  (A = A_r0 diagnostic)
sqrt(sigma) ~= 463.30 MeV  (A = pi/12 diagnostic)
```

This bracket straddles the repo's rough 465 MeV value, but it mixes
sources and is not a closure.

## 2. Gate Assessment

| Candidate | Non-circular | Sea-quark dynamics | Observable defined | Uncertainty | Unique sigma scheme | B5 link | Closes? |
|---|---:|---:|---:|---:|---:|---:|---:|
| CLS 2025 force scales | yes | yes | yes | yes | no | no | no |
| TUMQCD 2023 fit-window sigma | yes | yes | yes | yes | no | no | no |
| repo rough x0.96 | yes | no | no | no | no | no | no |

The external bridge is materially stronger than the rough x0.96 factor:
it has actual dynamical-sea ensembles, defined observables, and quoted
uncertainties. It still does not close retained B2 because the sigma
scheme/window and B5 framework link are not closed.

## 3. Claim-State Movement

Cycle 1 repaired the B2 gate. Cycle 2 narrows the live external bridge:

- `r0`/`r1` force scales are the cleanest `N_f=2+1` observable;
- finite-window `sigma` is usable only with an explicit convention
  residual;
- the rough x0.96 factor is now demoted to a consistency placeholder
  that happens to agree with one TUMQCD fit convention.

Safe statement:

> The B2 bridge can be made much more explicit using modern static-energy
> data, but it remains bounded. A retained-with-budget upgrade would need
> a declared force-scale or finite-window-tension observable, the
> convention split as an uncertainty, and a B5 framework-to-standard-QCD
> residual.

## 4. Literature Sources

- TUMQCD, "Static Energy in (2+1+1)-Flavor Lattice QCD: Scale Setting
  and Charm Effects", arXiv:2206.03156:
  <https://arxiv.org/abs/2206.03156>
- M. Bruno et al., "The determination of potential scales in 2+1 flavor
  QCD", EPJC 85, 673 (2025):
  <https://link.springer.com/article/10.1140/epjc/s10052-025-14339-y>

## 5. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py
```

Expected result:

```text
PASS=12 FAIL=0
```

(matches `runner_check_breakdown.total_pass = 12` recorded in the
2026-05-05 audit ledger entry; an earlier "PASS=14" figure cited in this
section's prior text was stale and has been corrected.)

## 6. Next Exact Action

Either:

1. write a retained-with-budget draft that explicitly chooses `r0`/`r1`
   as the Lane 1 force-scale observable and demotes `sqrt(sigma)` to a
   derived bounded comparator; or
2. run a B5 large-volume framework-to-standard-QCD check so external
   static-energy inputs can be imported with a smaller residual.

The first is editorial/claim-boundary work. The second is the stronger
science route.

## 7. Cited Lane 1 sibling status (audit-explicit)

The audit identifies the open dependency as the Lane 1 `sqrt(sigma)`
B2/B5 chain rather than this scout's own arithmetic. Current ledger
statuses for the cited siblings are:

| Sibling row | `audit_status` | `effective_status` | `claim_type` |
|---|---|---|---|
| `hadron_lane1_b2_dynamical_screening_boundary_note_2026-04-29` | audited_clean | retained_no_go | no_go |
| `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` | audited_clean | retained_no_go | no_go |
| `hadron_lane1_sqrt_sigma_b2_gate_repair_audit_note_2026-04-30` | unaudited | unaudited | open_gate |
| `hadron_lane1_sqrt_sigma_b5_ladder_budget_note_2026-04-30` | unaudited | unaudited | positive_theorem |
| `hadron_lane1_sqrt_sigma_retention_gate_audit_support_note_2026-04-27` | unaudited | unaudited | open_gate |

The retained-no-go siblings (B2 dynamical-screening boundary and B5
framework-link audit) are the load-bearing closures behind the present
scout's "scout, not promotion" stance: B2 has a retained no-go on the
rough x0.96 screening factor and B5 has a retained no-go on the
framework-to-standard-QCD link. The unaudited siblings (gate repair,
ladder budget, retention gate audit) are the open repair surfaces; this
scout cites their existence but does not depend on their content.

## 8. Audit-aware repair path

Per `audit_ledger.json`, `notes_for_re_audit_if_any` for
`hadron_lane1_sqrt_sigma_b2_static_energy_bridge_scout_note_2026-04-30`:
the cheapest path to a stronger audit verdict is to "supply a retained
B5 framework-to-standard-QCD import theorem and a declared unique
force-scale or finite-window-tension observable with its convention
residual." That repair path is exactly the second option in section 6
above and would close the missing bridge theorem the audit names. It is
not attempted in this scout note; this note remains a bounded scout that
catalogs the available external static-energy/force-scale literature
without promoting the Lane 1 `sqrt(sigma)` row.
