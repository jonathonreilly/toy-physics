# PMNS Unified Bridge: Full-Closure Consequences

**Date:** 2026-04-15  
**Status:** exact consequence theorem after promoting the unified PMNS bridge
carrier to a new derived completion object  
**Script:** `scripts/frontier_pmns_unified_bridge_full_closure_consequence.py`

## Question

If the minimal unified PMNS bridge object

`U_min = (A, B, u, v, delta, rho, gamma, a_sel, e)`

is promoted to a new derived completion carrier, what exactly closes?

Does that already give **full** neutrino closure, or is there still a smaller
honest object beyond `U_min` that must be admitted?

## Bottom line

Promoting `U_min` is enough to close the selector/Hermitian side, but not yet
the full coefficient side.

What follows exactly is:

1. if `a_sel != 0`, then `sign(a_sel)` selects the active minimal PMNS branch
2. `(A, B, u, v, delta, rho, gamma)` reconstruct the selected active
   Hermitian law exactly
3. one additional global sheet bit `s in Z_2` reconstructs the selected
   two-Higgs coefficients exactly
4. on the charged-lepton-side branch, full neutrino closure additionally
   requires the passive neutrino monomial mass triple `(m_1, m_2, m_3)`

So the honest minimal full-closing object is **piecewise**:

- neutrino-side branch:
  `U_full^nu = (A, B, u, v, delta, rho, gamma, a_sel, s)`
- charged-lepton-side branch:
  `U_full^e = (A, B, u, v, delta, rho, gamma, a_sel, s, m_1, m_2, m_3)`

This is the exact full-closure consequence of promoting `U_min`. It is no
longer a vague “missing bridge” story.

## Exact consequence of `U_min`

The existing unified bridge theorem already identified

`U_min = (A, B, u, v, delta, rho, gamma, a_sel, e)`

as the smallest exact carrier simultaneously accounting for:

- the active Hermitian bridge package
- the breaking-source coordinates
- the reduced selector primitive

The new point is what happens once that carrier is treated as a derived
object rather than merely a minimal missing object.

### Selector and branch

The reduced selector piece is

`B_red = a_sel (chi_N_nu - chi_N_e)`.

So:

- `a_sel > 0` selects the neutrino-side branch
- `a_sel < 0` selects the charged-lepton-side branch
- `a_sel = 0` does not close the branch

Thus full closure requires `a_sel != 0`.

### Active Hermitian law

The Hermitian bridge piece is

`B_H,min = (A, B, u, v, delta, rho, gamma)`.

It reconstructs the selected active Hermitian matrix exactly through

`H = H_core(A, B, u, v) + B(delta, rho, gamma)`.

So once `a_sel != 0`, the selected active Hermitian law is closed exactly.

## One extra generic sheet bit

The branch-conditioned quadratic-sheet theorem already proves that selected
Hermitian data do not determine a unique two-Higgs canonical coefficient
matrix. They determine exactly two coefficient sheets with the same
Hermitian matrix.

Therefore `U_min` is still short by one discrete coefficient datum.

Call that datum

`s in Z_2`.

Then:

- `U_min + s` fixes the selected two-Higgs coefficient sheet exactly
- no `H`-based object can absorb `s`
- on the weak-axis seed patch, the old boundary edge selector is just the
  restriction of `s` to the seed boundary

So the earlier seed-edge bit `e` is not a second independent discrete datum.
It is the boundary manifestation of the global coefficient-sheet bit.

## Charged-lepton-side extra data

If the active PMNS branch is the charged-lepton branch, then full neutrino
closure still contains the passive monomial neutrino sector.

That passive sector is not encoded in the active Hermitian bridge. It is the
exact triple of positive monomial Dirac masses:

`(m_1, m_2, m_3)`.

So:

- on the neutrino-side branch, `U_min + s` closes full neutrino data
- on the charged-lepton-side branch, `U_min + s` is still short by the passive
  monomial neutrino mass triple

This matches the exact earlier last-mile count: `7` versus `3 + 7`.

## Theorem-level statement

**Theorem (Full-closure consequence of the unified PMNS bridge carrier).**
Assume the unified bridge carrier

`U_min = (A, B, u, v, delta, rho, gamma, a_sel, e)`

is promoted to a new derived completion object, together with the exact sign-to-branch
reduction, the exact branch-conditioned quadratic-sheet closure, the exact
sheet nonforcing theorem, the exact weak-axis seed coefficient-closure theorem,
and the exact last-mile branch-conditioned count theorem. Then:

1. if `a_sel != 0`, `sign(a_sel)` selects the active minimal PMNS branch
2. `(A, B, u, v, delta, rho, gamma)` reconstruct the selected active
   Hermitian law exactly
3. one additional global sheet bit `s in Z_2` reconstructs the selected
   two-Higgs coefficient sheet exactly
4. the seed-boundary bit is the restriction of `s` on the weak-axis boundary
5. on the charged-lepton-side branch, full neutrino closure additionally
   requires the passive monomial neutrino mass triple `(m_1, m_2, m_3)`

Therefore the exact minimal full-closing object is piecewise:

- `U_full^nu = (A, B, u, v, delta, rho, gamma, a_sel, s)`
- `U_full^e  = (A, B, u, v, delta, rho, gamma, a_sel, s, m_1, m_2, m_3)`

## What this closes

This closes the ambiguity about what is actually left after promoting the
unified bridge carrier.

It is now exact that the remaining full-closing object is **not**:

- another hidden continuous Hermitian bridge
- another hidden selector family
- another independent seed-edge selector

The remaining object is exactly:

- one global two-Higgs coefficient-sheet bit
- plus, on the charged-lepton-side branch only, the passive neutrino monomial
  mass triple

## What this does not claim

This note does **not** claim that the retained bank itself derives
`U_min`, `s`, or `(m_1, m_2, m_3)`.

It claims something narrower and exact:

- **if** `U_min` is elevated to a new derived completion object,
- **then** the smallest honest full-closing augmentation is the piecewise
  object above.

So this is an exact promoted-carrier consequence theorem, not a retained-bank
closure theorem.

## Command

```bash
python3 scripts/frontier_pmns_unified_bridge_full_closure_consequence.py
```
