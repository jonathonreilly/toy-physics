# Lane 1 `sqrt(sigma)` B2 Static-Energy Bridge: Current-Surface No-Go

**Date:** 2026-04-30 (claim-type lock: 2026-05-16)
**Status:** support / current-surface **no-go**; no theorem or claim
promotion. This note states the elementary closure-gate derivation that
no current-surface static-energy or force-scale comparator can promote
the Lane 1 `sqrt(sigma)` row to retained while either of the two
load-bearing siblings is `retained_no_go`.
**Script:** `scripts/frontier_hadron_lane1_sqrt_sigma_b2_static_energy_bridge.py`
**Lane:** 1 - Hadron mass program, route 3E `sqrt(sigma)` retained
promotion.
**Claim type:** `no_go` (current surface), derived by gate-closure logic
from two retained no-go siblings; see Theorem 0 and Section 9.

**Repair history (2026-05-16):**
The audit lane previously classified this note `audited_conditional`
(verdicts 2026-05-05 and 2026-05-11) with the repair target
"supply a retained B5 framework-to-standard-QCD import theorem and a
declared unique force-scale or finite-window-tension observable with its
convention residual." That repair is materially unachievable on the
current surface because the requested B5 framework-link import is
itself `retained_no_go` (sibling
`hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30`,
`audited_clean`, `effective_status=retained_no_go`, `claim_type=no_go`,
2026-04-30) and the requested unique sigma scheme cannot exist while the
B2 dynamical-screening factor is `retained_no_go`
(sibling `hadron_lane1_b2_dynamical_screening_boundary_note_2026-04-29`,
`audited_clean`, `effective_status=retained_no_go`, `claim_type=no_go`).
The honest repair is therefore not to invent a retained import that the
graph has already ruled out, but to lock this row's `claim_type` to
`no_go` (current surface) by reading the closure gate against the two
retained no-go siblings. That derivation is the new Theorem 0 below; the
runner verifies it as a chain check (class A/B citation of retained
no-go siblings) and the prior external-comparator arithmetic is kept as
non-load-bearing diagnostic material.

---

## 0. Result

**Theorem 0 (current-surface no-go for Lane 1 sqrt(sigma) retained
promotion via B2 static-energy bridges).**

*Assumptions (all retained).*

A1. `hadron_lane1_b2_dynamical_screening_boundary_note_2026-04-29` is
`audited_clean` with `claim_type=no_go` and
`effective_status=retained_no_go`. It establishes that the rough x0.96
B2 dynamical screening factor is not closed by any current-surface
derivation: no unique sigma scheme is available on the current surface.

A2. `hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30` is
`audited_clean` with `claim_type=no_go` and
`effective_status=retained_no_go`. It establishes that the
framework-to-standard-QCD B5 import is not closed on the current
surface: structural `SU(3)` + `g_bare=1 -> beta=6` + `4^4` plaquette
check is not the required large-volume Wilson/Creutz/force-scale ladder
with declared uncertainty.

G. A B2 static-energy/force-scale comparator promotes the Lane 1
`sqrt(sigma)` row to retained only if all six closure-gate bits hold for
at least one bridge candidate: (g1) non-circular source, (g2) sea-quark
dynamics, (g3) defined observable, (g4) uncertainty budget, (g5)
**unique sigma scheme**, (g6) **framework-to-standard-QCD B5 link**.

*Claim.* No current-surface B2 static-energy or force-scale comparator
can satisfy gate G.

*Proof.* By A1, gate bit (g5) cannot be satisfied on the current
surface: the rough x0.96 factor is retained-no-go and the TUMQCD
`A_r0` vs `pi/12` convention split (about 3% on the available
finite-window sigma, see Section 1.1) is precisely the convention
ambiguity A1 records as not closable on the current surface. By A2,
gate bit (g6) cannot be satisfied on the current surface: the requested
framework-to-standard-QCD import is retained-no-go. Either bit alone
forces `closes=False`. Therefore for every candidate `c` in the gate
enumeration, `c.closes() = False` on the current surface. *QED.*

*Load-bearing step class.* B (derivation from cited retained-no-go
siblings + elementary boolean closure on the gate). Class D
external-comparator arithmetic is retained below as non-load-bearing
diagnostic material that quantifies the convention split A1 names.

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

Cycle 1 repaired the B2 gate. Cycle 2 narrows the live external bridge.
Cycle 3 (this revision, 2026-05-16) **locks the claim_type to `no_go`
(current surface)** via Theorem 0 above.

The Cycle 2 catalog stands:

- `r0`/`r1` force scales are the cleanest `N_f=2+1` observable;
- finite-window `sigma` is usable only with an explicit convention
  residual;
- the rough x0.96 factor is a consistency placeholder that happens to
  agree with one TUMQCD fit convention.

But the load-bearing claim is now negative and derived, not an external
gate assessment:

> Conditional on the two retained no-go siblings (B2 dynamical-screening
> boundary and B5 framework-link audit) remaining in effect, **no**
> current-surface B2 static-energy or force-scale comparator can promote
> the Lane 1 `sqrt(sigma)` row to retained. A future retained-with-budget
> upgrade would require lifting at least one of the two retained no-gos:
> either by deriving a unique sigma scheme that closes A1 or by landing
> the large-volume framework-side Wilson/Creutz/force-scale ladder that
> closes A2. Neither is attempted in this note.

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
PASS=21 FAIL=0
```

The 2026-05-16 revision adds Part 5 (Theorem 0 chain check, 9 new
checks) that loads the two retained no-go sibling notes and verifies
their stated adjudication content plus the elementary derivation that
no current-surface bridge candidate can satisfy gate G. Earlier audit
cycles (2026-05-05 and 2026-05-11) recorded `PASS=12` against the
previous runner that contained only Parts 1-4; the new Part 5 raises
the count to 21. The prior `PASS=14` figure cited in an even earlier
draft was stale.

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
the cheapest path to a stronger audit verdict named in the previous
audit cycle was to "supply a retained B5 framework-to-standard-QCD
import theorem and a declared unique force-scale or finite-window-tension
observable with its convention residual."

Both halves of that request are blocked on the current surface:

- the requested B5 framework-to-standard-QCD import is itself the
  subject of a retained no-go
  (`hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30`,
  `audited_clean`, `effective_status=retained_no_go`); and
- the requested unique sigma scheme is exactly the object the B2
  dynamical-screening retained no-go forbids
  (`hadron_lane1_b2_dynamical_screening_boundary_note_2026-04-29`,
  `audited_clean`, `effective_status=retained_no_go`).

The honest repair is therefore not to invent an import the graph has
already adjudicated as non-existent on the current surface, but to lock
this row's `claim_type` to `no_go` (current surface) via Theorem 0 and
let the runner derive the conclusion from the two retained no-go
siblings rather than from external comparator arithmetic. That is the
2026-05-16 change.

## 9. Claim-type lock summary

This section is the formal record of the 2026-05-16 demotion from
`positive_theorem` (migration_hint) to `no_go` (derived, current
surface). It does not promote the row; it correctly narrows the
`claim_type` to what the load-bearing step actually establishes.

| Field | Pre-2026-05-16 | Post-2026-05-16 |
|---|---|---|
| `claim_type` (provenance) | `positive_theorem` (`migration_hint`) | `no_go` (derived) |
| `claim_scope` | scout-note conclusion that quoted TUMQCD/CLS values do not promote Lane 1 sqrt(sigma) | derived current-surface no-go that no B2 static-energy or force-scale comparator can promote Lane 1 sqrt(sigma) while siblings A1/A2 remain retained no-go |
| `load_bearing_step_class` | D (external comparator arithmetic) | B (citation of retained no-go siblings + elementary boolean closure on the gate) |
| `effective_status` target | `retained_no_go` | `retained_no_go` |
| `chain_closes` target | true | true (closure on the negative claim) |

The `claim_type=no_go` is mirrored on the sister B5 framework-link audit
row (`audited_clean`, class B, `retained_no_go`); the present row uses
the same template applied to the static-energy bridge surface.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [hadron_lane1_sqrt_sigma_b2_gate_repair_audit_note_2026-04-30](HADRON_LANE1_SQRT_SIGMA_B2_GATE_REPAIR_AUDIT_NOTE_2026-04-30.md)
- [hadron_lane1_sqrt_sigma_b5_ladder_budget_note_2026-04-30](HADRON_LANE1_SQRT_SIGMA_B5_LADDER_BUDGET_NOTE_2026-04-30.md)
- [hadron_lane1_sqrt_sigma_retention_gate_audit_support_note_2026-04-27](HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27.md)

## Retained no-go sibling links (Theorem 0 chain)

This section is load-bearing: the two siblings cited here are the
retained no-go premises in Theorem 0 (Section 0).

- [hadron_lane1_b2_dynamical_screening_boundary_note_2026-04-29](HADRON_LANE1_B2_DYNAMICAL_SCREENING_BOUNDARY_NOTE_2026-04-29.md) (A1)
- [hadron_lane1_sqrt_sigma_b5_framework_link_audit_note_2026-04-30](HADRON_LANE1_SQRT_SIGMA_B5_FRAMEWORK_LINK_AUDIT_NOTE_2026-04-30.md) (A2)
