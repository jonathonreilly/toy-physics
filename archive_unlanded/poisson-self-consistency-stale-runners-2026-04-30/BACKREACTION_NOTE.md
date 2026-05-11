# Self-Consistent Back-Reaction: Horizons from Geometry

**Date:** 2026-04-05
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/poisson-self-consistency-stale-runners-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/poisson-self-consistency-stale-runners-2026-04-30/` (the directory name encodes the failure reason: stale Poisson self-consistency runners)
- **Audit verdict_rationale (verbatim from [audit_ledger.json](../../docs/audit/data/audit_ledger.json) under claim_id `backreaction_note`):**

> Issue: the source note's quantitative absorption-threshold claim is stale against the live Poisson/self-consistency runners; the current Poisson output gives escape 1.0498 at G=0.005, 1.0502 at G=0.010, 0.9631 at G=0.050, and 0.7547 at G=0.100, not the note's 1.025, 1.002, 0.751, and 0.486 trend with G_crit ~ 0.011. Why this blocks: a hostile physicist cannot retain a claimed horizon-like threshold at G_crit ~ 0.011 or a smooth table-driven collapse transition when the current computation places the first listed sub-unity escape much later and shows unstable/away behavior at larger G. Repair target: restore the exact runner/version and sweep grid that generated the note, or update the note with a live asserted sweep including G=0.011, 0.012, 0.020, the field-strength-dependence rows, convergence gates, escape monotonicity checks, and Born checks on the same converged field. Claim boundary until fixed: it is safe to claim only that the current Poisson runner shows TOWARD deflection for G <= 0.1, escape below one by G=0.050 at s_ext=0.004, and a linear fixed-field Born check of 2.45e-16 in the separate self-consistency script; it is not safe to retain the note's G_crit ~ 0.011 gravitational-collapse threshold or its exact table.

- **Do NOT cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a 'closed no-go'.

## Artifact chain

- [`scripts/backreaction_poisson.py`](../scripts/backreaction_poisson.py)
- [`scripts/backreaction_selfconsistent.py`](../scripts/backreaction_selfconsistent.py)
- [`scripts/backreaction_emergent_gamma.py`](../scripts/backreaction_emergent_gamma.py) (bounded negative)

## The idea

In GR: matter curves spacetime, spacetime guides matter. Here:
1. Propagate on fixed field -> amplitude distribution |psi|^2
2. |psi|^2 generates additional field: f_self = G * sum |psi(x)|^2 / |y-x|
3. Re-propagate on updated field
4. Iterate to self-consistency

Born rule holds at each step (linear propagator on fixed field).
The field evolves between steps.

## Results

### Critical G for absorption

| G | deflection | direction | escape |
| ---: | ---: | --- | ---: |
| 0.005 | +1.10e-02 | TOWARD | 1.025 |
| 0.010 | +1.11e-02 | TOWARD | 1.002 |
| **0.011** | — | — | **~1.000** |
| 0.012 | +1.12e-02 | TOWARD | 0.992 |
| 0.020 | +1.15e-02 | TOWARD | 0.949 |
| 0.050 | +1.07e-02 | TOWARD | 0.751 |
| 0.100 | +1.60e-02 | TOWARD | 0.486 |

### Key properties of the threshold

- **Gravity preserved**: deflection is TOWARD at ALL G values
- **Smooth transition**: escape decreases monotonically from 1.03 to 0.49
- **Field-strength dependence**: stronger external field resists absorption
  (s=0.001: escape=0.92, s=0.016: escape=1.09 at G=0.02)

### Born rule

Born |I3|/P = 8.4e-16 on the converged field at G=0.1. The self-consistent
field is fixed after convergence, so the propagator is linear.

### Bounded negatives

1. **Edge addition**: extra edges at high-amplitude nodes absorbs amplitude
   even without field. The absorption is from topology change, not physics.
2. **Direct epsilon-gamma mapping**: back-reaction and complex action produce
   qualitatively similar physics but don't map quantitatively.

## What this means

The Poisson self-gravity produces a **gravitational collapse threshold**:
below G_crit ~ 0.011, the beam passes through with mild amplification.
Above G_crit, the beam is partially absorbed — a horizon-like effect.

This is the discrete analog of the Schrodinger-Newton equation.
The self-consistent field converges to a stable solution where:
- The beam curves toward the mass (gravity)
- Some amplitude is lost to the self-focused field (horizon)
- Born rule holds (linear propagation on converged field)

The complex action S = L(1-f) + i*gamma*L*f is the **effective theory**
of this back-reaction. It captures the qualitative physics (gravity +
absorption) in a single kernel, but gamma is not a simple function of G.
