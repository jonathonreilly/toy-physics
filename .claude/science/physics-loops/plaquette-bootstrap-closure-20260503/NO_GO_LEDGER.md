# NO-GO LEDGER — Plaquette Bootstrap Closure

**Date:** 2026-05-03

## Inherited from prior campaign (`vev-v-singlet-derivation-20260502`)

| # | No-go | Implication |
|---|---|---|
| N1 | Naive U → u_0·I mean-field has no positive saddle without Haar entropy | Prior campaign block 03 (PR [#410](https://github.com/jonathonreilly/cl3-lattice-framework/pull/410)). The bootstrap approach uses positivity constraints, not mean-field saddle, so this no-go does not directly apply. But it confirms that direct mean-field is insufficient for ⟨P⟩(β=6). |
| N2 | Toy SU(3) Haar entropy gives wrong magnitude | Prior campaign block 03. Confirms true SU(3) Haar entropy is non-trivial and needs more sophisticated treatment. |
| N3 | The minimal-block-equals-bulk gap on V-invariant subspace = framework-point underdetermination | Bootstrap approach also lives on the minimal block; same gap may apply. Need to address explicitly in block 01. |

## Constraints from existing framework infrastructure

| # | Constraint | Source |
|---|---|---|
| F1 | CVXPY install blocked by PEP 668 (system Python externally-managed); no industrial SDP solver | Preflight 2026-05-03; no `--user` workaround works; `--break-system-packages` not used (risky). |
| F2 | The framework's RP theorem (A11) is `support` tier (audit-pending), not retained. | `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`. Bootstrap built on A11 inherits the A11 conditional status. |
| F3 | Migdal-Makeenko / loop equations are NOT explicitly derived on the framework's surface. | Standard lattice gauge result, but not framework-internal. Must be admitted as bridge BB2 if used. |

## Routes NOT to re-explore

- Naive mean-field saddle (covered by N1, N2, prior block 03 / PR [#410](https://github.com/jonathonreilly/cl3-lattice-framework/pull/410))
- Single-plaquette strong-coupling expansion as a "bound" — it's an expansion, not a bound
- Same-surface family arguments (per memory `consistency_vs_derivation_below_w2`)
- Hard-coding bootstrap brackets from literature
