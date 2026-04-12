# Self-Consistency Poisson Preference -- Bounded Companion Note

**Date:** 2026-04-12
**Status:** bounded companion to `SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`
**Branch:** `claude/youthful-neumann`
**Script:** `scripts/frontier_self_consistent_field_equation.py`

## Bounded Claim

Among 21 tested operators on the 3D cubic lattice (N=20 and N=24,
Dirichlet BC), the graph Laplacian (unscreened Poisson) best matches
Newtonian gravity in self-consistent iteration:

| Operator             | Converges? | Attractive? | beta | Physical? |
|----------------------|-----------|-------------|------|-----------|
| Poisson (nabla^2)    | Yes       | Yes         | 1.28 | Yes       |
| Biharmonic (nabla^4) | Yes       | No          | 0.87 | No        |
| 1/r^2 kernel         | No        | No          | 1.03 | No        |
| Local (phi = G*rho)  | Yes       | No          | 8.64 | No        |
| Random PD kernel     | Yes       | No          | 4.19 | No        |

The discriminator is the decay exponent beta: only unscreened Poisson
gives beta approaching 1.0 (the Newtonian target). Screened variants
converge and produce attractive fields, but with beta >> 1 (Yukawa
decay), which does not match the 1/r Newtonian potential.

## What Is NOT Claimed

1. **No uniqueness proof.** This is operator preference among the tested
   set, not a proof that Poisson is the unique self-consistent equation.
2. **No exclusion of screened Poisson on convergence grounds.** Screened
   Poisson also converges with attractive fields. Discrimination is via
   beta, not convergence failure or sign reversal.
3. **No claim beyond cubic lattice.** Extension to grown, random, or
   irregular graphs requires separate verification.
4. **No exclusion of non-local operators.** Only local/short-range
   operators tested. Tuned non-local kernels are not excluded.

## What IS Retained

- Unscreened Poisson is the unique tested operator that produces an
  attractive, monotonically decaying potential with beta closest to 1.0.
- Screened sweep (mu^2 = 0, 0.1, 1.0, 2.0): beta increases with
  screening mass; only mu^2 = 0 gives the Newtonian exponent.
- Propagator susceptibility correlates (r = 0.93) with Poisson Green's
  function, confirming structural compatibility.
- Sign discriminator excludes biharmonic, local, random-PD, and
  wrong-kernel operators outright (all repulsive).

## Caveats

- beta = 1.28 at N=20 exceeds target 1.0 (Dirichlet BC on small
  lattices). Distance-law closure extrapolates beta -> 1.0 at 96^3.

## References

- Script: `scripts/frontier_self_consistent_field_equation.py`
- Parent note: `docs/SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`
- Codex review: `docs/OVERNIGHT_CLAUDE_AUDIT_2026-04-12.md`
