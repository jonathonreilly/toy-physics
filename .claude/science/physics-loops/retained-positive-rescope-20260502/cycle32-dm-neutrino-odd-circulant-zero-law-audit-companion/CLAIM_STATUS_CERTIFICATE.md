# Cycle 32 Claim Status Certificate — DM Neutrino Odd-Circulant Current-Stack Zero Law Audit Companion (Pattern B)

**Block:** physics-loop/dm-neutrino-odd-circulant-zero-law-audit-companion-block32-20260502
**Runner:** scripts/audit_companion_dm_neutrino_odd_circulant_zero_law_exact.py (PASS=17/0)
**Target row:** dm_neutrino_odd_circulant_current_stack_zero_law_note_2026-04-15 (claim_type=positive_theorem, load_bearing_step_class=C)

## Block type

**Pattern B — audit-acceleration runner.** This block does NOT introduce a new
claim row, a new source note, or a new positive theorem. It contributes a
focused exact-precision verification companion to the existing
`dm_neutrino_odd_circulant_current_stack_zero_law_note_2026-04-15` row,
providing audit-lane evidence at sympy `Rational` exact precision (rather
than numpy float at 1e-12 tolerance) for the residual-Z_2 parity-preservation
argument and the `c_odd = 0` conclusion.

## Claim-Type Certificate (Pattern B)

```yaml
proposed_claim_type: meta  # companion runner; not a claim row
proposed_load_bearing_step_class: C
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_status: false
status_authority: independent_audit_lane
source_sets_audit_outcome: false
```

## 7-criteria check (adapted for Pattern B)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES (Pattern B audit-acceleration runner) |
| 2 | No new claim rows or new source notes introduced | YES (runner-only; provides class-C breakdown evidence on existing row) |
| 3 | No load-bearing observed/fitted/admitted in the companion | YES (purely symbolic linear algebra on Z_3 cube-root-of-unity expressions; no PDG/literature/fitted/admitted-convention input) |
| 4 | Parent row's deps unchanged by this block | YES (does not modify ledger row state; only adds runner artifact) |
| 5 | Runner verifies parent's load-bearing step at exact precision | YES (sympy `Matrix`, `Rational`, exact `omega = exp(2 pi i / 3)` cube-root-of-unity, exact parity / odd-coefficient checks via `rewrite(cos).expand(complex=True)`) |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact; audit-lane decides |
| 7 | PR body says audit-lane to ratify | YES (block proposes companion evidence only; does not assert any retained-status promotion) |

## What the companion verifies

1. **Generators.** `S^3 = I`, `P_{23}^2 = I`, and `U_Z3` unitary (cube-root-of-unity check via sympy `cos`-rewrite + complex expand).
2. **Weak-axis split parity.** `P_{23} d P_{23}^T = d` for `d = diag(a, b, b)` (symbolic in `a, b`).
3. **Bridged Dirac surface parity.** At concrete rational `a = 7/5`, `b = 4/5`, `Y_even = U_Z3^dag d U_Z3` is residual-Z_2 even.
4. **Hermitian kernel parity and zero odd coefficient.** `H_even = Y_even^dag Y_even` is residual-Z_2 even and `Im(H_even[0, 1]) = 0` exact.
5. **Equivariant functionals preserve parity.** Three test functionals (`Y^dag Y`, `Y + Y^dag`, quadratic combination) all give Z_2-even output with `c_odd = 0`.
6. **Circulant from even data.** `c_even = mu I + nu(S + S^2)` has `c_odd = Im(K[0,1]) = 0` symbolically; the perturbation `+ i r (S - S^2)` gives `c_odd = r != 0` and breaks Z_2 evenness.
7. **Parent row class-(C) ledger check.**

## Audit-graph effect

This companion is **meta** — it does not move the parent row by itself.
The upstream weak-axis split / Z_3 bridge / DM-circulant authorities are
outside this companion's scope. The companion only verifies that
the parent's local class-(C) parity-preservation step holds at exact
symbolic precision, including the cube-root-of-unity reductions in the
Z_3 bridge.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on the claim.
- No same-surface family arguments.

The companion is pure symbolic linear algebra on the standard 3x3
matrices `S, S^2, P_{23}, U_Z3` over `Z[i]` (with `omega` reduced via
`cos`-rewrite + complex expand).

## What this proposes

A standalone audit-companion runner that complements the existing primary
runner by providing exact symbolic verification of the residual-Z_2
parity-preservation argument with the cube-root-of-unity Z_3 bridge
reduced symbolically (rather than at 1e-12 float tolerance). The block
proposes nothing about any parent status change; the independent audit
lane is the authority for that.
