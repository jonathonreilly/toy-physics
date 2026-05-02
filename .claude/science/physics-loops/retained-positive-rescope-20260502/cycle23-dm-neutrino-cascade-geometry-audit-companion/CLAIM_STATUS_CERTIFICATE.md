# Cycle 23 Claim Status Certificate — DM Neutrino Cascade Geometry Audit Companion (Pattern B)

**Block:** physics-loop/dm-neutrino-cascade-geometry-audit-companion-block23-20260502
**Runner:** scripts/audit_companion_dm_neutrino_cascade_geometry_exact.py (PASS=11/0)
**Target row:** dm_neutrino_cascade_geometry_note_2026-04-14 (claim_type=positive_theorem, audit_status=audited_conditional, td=153, load_bearing_step_class=A)

## Block type

**Pattern B — audit-acceleration runner.** This block does NOT introduce a new
claim row, a new source note, or a new positive theorem. It contributes a
focused exact-precision verification companion to the existing
`dm_neutrino_cascade_geometry_note_2026-04-14` row, providing audit-lane
evidence at sympy `Rational` exact precision (rather than numpy float).

The parent's load-bearing step is the operator-algebra identity on the C^8
taste cube. With `Gamma_1 = sigma_x (x) I_2 (x) I_2` and the projectors
onto `O_0`, `T_1`, `T_2`:

- `P_T1 Gamma_1 P_T1 = 0` (Gamma_1 doesn't act inside T_1 at one hop);
- `P_O0 Gamma_1 P_T1 = [1, 0, 0]` (rank 1 singlet channel);
- `P_T2 Gamma_1 P_T1` has rank 2 (T_2 channel);
- Second-order returns: `via O_0 = diag(1, 0, 0)`, `via T_2 = diag(0, 1, 1)`,
  total = `I_3` (1+2 cascade decomposition).

The companion verifies all of these at sympy exact precision via explicit
8x8 Kronecker product construction.

## Claim-Type Certificate (Pattern B)

```yaml
target_claim_type: meta  # audit-companion runner; not a claim row
proposed_load_bearing_step_class: A
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_audit_status: false  # audit-lane decides
audit_required_before_effective_retained: true  # parent row only; companion is meta
bare_retained_allowed: false
```

## 7-criteria check (adapted for Pattern B)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES (Pattern B audit-acceleration runner) |
| 2 | No new claim rows or new source notes introduced | YES (runner-only; provides class-A breakdown evidence) |
| 3 | No load-bearing observed/fitted/admitted in the companion | YES (purely symbolic linear algebra; no PDG/literature/fitted/admitted-convention input) |
| 4 | Parent row's deps unchanged by this block | YES (does not modify ledger row state; only adds runner artifact) |
| 5 | Runner verifies parent's load-bearing step at exact precision | YES (sympy `Matrix`, `Rational`, explicit Kronecker product, exact equality checks) |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact; audit-lane decides |
| 7 | PR body says audit-lane to ratify | YES (block proposes companion evidence only; does not assert any retained-status promotion) |

## What the companion verifies

1. **Gamma_1^2 = I_8** (sigma_x squared = I_2 lifted via Kronecker).
2. **One-hop closure off T_1:** `P_T1 Gamma_1 P_T1 = 0_{8x8}`.
3. **Rank-1 singlet channel:** `b0^T Gamma_1 b1 = [1, 0, 0]` exactly,
   rank = 1.
4. **Rank-2 T_2 channel:** `b2^T Gamma_1 b1` has rank 2.
5. **Second-order via O_0:** `b1^T Gamma_1 P_O0 Gamma_1 b1 = diag(1, 0, 0)`
   exactly.
6. **Second-order via T_2:** `b1^T Gamma_1 P_T2 Gamma_1 b1 = diag(0, 1, 1)`
   exactly.
7. **Total return = I_3** (completeness on T_1).
8. **1+2 cascade rank signature:** `diag(1,0,0)` rank 1, `diag(0,1,1)` rank 2.
9. **Parent row class-(A) ledger check.**

## Audit-graph effect

This companion is **meta** — it does not move the parent row by itself.
The parent's `audited_conditional` verdict identifies remaining open steps
in the C^8-to-C^16 chiral embedding, the operator-chain identification of
the physical Dirac Yukawa, and the neutrino-sector base normalization.
None of those gaps are addressed by this companion; the companion only
verifies that the local operator-algebra identities hold at exact
precision, useful when audit-lane reviewers revisit the conditional
verdict on the local-algebra portion of the row.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

The companion is pure symbolic linear algebra on the explicit Clifford
realization of the C^8 taste cube.

## What this proposes

A standalone audit-companion runner that complements the existing primary
runner by providing exact symbolic verification of the cascade-geometry
operator algebra. The block proposes nothing about any retained-status
change; the audit lane is the authority for that.
