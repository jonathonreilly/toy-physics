# Plaquette V=1 Picard-Fuchs ODE Note

**Date:** 2026-05-05
**Claim type:** bounded_theorem
**Status:** bounded support theorem, unaudited.
**Primary runner:** `scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py`

**All-order proof companion (added 2026-05-09):**
`PLAQUETTE_V1_PICARD_FUCHS_ODE_ALL_ORDER_PROOF_NOTE_2026-05-09.md`
upgrades the truncated-series substitution and finite ODE-vs-Weyl
agreement below to an all-order proof that `L · J(β) = 0` identically
in `Q[[β]]` and that `J(β)` IS the analytic Frobenius branch at
`β = 0`. That note's runner uses the Bostan-Salvy-Schost
finite-window-suffices theorem combined with the runner-internal
D-finite parameter bounds `(R, D) = (3, 2)`. The independent audit
lane decides whether that companion closes the all-order gap.
(Backticked to break five nested length-2/3/4 citation cycles in the
plaquette V=1 Picard-Fuchs cluster; citation graph direction is
*all_order_proof → this_note*, since the all-order proof companion
consumes this V=1 ODE statement as its target while this bounded
ODE note's truncated-series claim does not consume the downstream
all-order proof as an input. This single demotion cascades to break
the four longer cycles through `bounded_synthesis_note_2026-05-06`,
`minimality_proof_note_2026-05-06`,
`koutschan_minimality_note_2026-05-06`, and
`rank_bound_citation_note_2026-05-06`, since each runs through the
same `this_note → all_order_proof` back-edge.)

## Claim

For the single-plaquette SU(3) Wilson integral

```text
J(beta) = integral_SU(3) exp(beta Re Tr U / 3) dU,
```

the runner verifies the third-order Picard-Fuchs equation

```text
6 beta^2 J'''(beta)
+ beta(60 - beta) J''(beta)
+ (-4 beta^2 - 2 beta + 120) J'(beta)
- beta(beta + 10) J(beta) = 0.
```

The analytic Frobenius solution at beta = 0 gives the physical
single-plaquette integral. Numerical integration of the ODE agrees with
direct Weyl integration at beta in {2, 4, 6, 8, 10}. At beta = 6,

```text
<P>_V=1(beta=6) = J'(6) / J(6) = 0.422531739650.
```

## Scope

This is a bounded single-plaquette result. It does not compute the
thermodynamic-limit Wilson plaquette value and does not promote any
plaquette, bridge, or downstream coupling status. The comparison to
larger-volume values remains outside this note.

The two broader exploratory notes from PR #541 are not landed here:
their `research_finding` claim type is not canonical for the audit lane,
and they referenced retained plaquette status that current main does not
grant. This note salvages only the runner-backed V=1 Picard-Fuchs result.

## Audit Consequence

```yaml
claim_id: plaquette_v1_picard_fuchs_ode_note_2026-05-05
note_path: docs/PLAQUETTE_V1_PICARD_FUCHS_ODE_NOTE_2026-05-05.md
runner_path: scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py
claim_type: bounded_theorem
intrinsic_status: unaudited
deps: []
audit_authority: independent audit lane only
```

## Command

```bash
python3 scripts/frontier_su3_v1_picard_fuchs_ode_2026_05_05.py
```

Expected summary:

```text
SUMMARY: THEOREM PASS=4 FAIL=0
```
