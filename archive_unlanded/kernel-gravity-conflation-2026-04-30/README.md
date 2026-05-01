# Archive: kernel vs gravity — conflation of link-level damping with detector escape

**Archived:** 2026-04-30 (README added 2026-05-01)
**Audit verdict:** audited_failed (terminal; ACCEPT)

## Why this is here

`KERNEL_VS_GRAVITY_NOTE.md` claimed a clean separation of two distinct
effects:

> kernel-generic absorption occurs under any nonzero field for gamma > 0,
> while only the localized 1/r gravity field produces the TOWARD → AWAY
> deflection crossover.

The audit found a load-bearing conflation between two different
observables:

- **Link-level imaginary-action damping**: the per-link factor
  `exp(-k gamma L f)` is below 1 for any `f > 0`, `gamma > 0`. This is a
  trivial algebraic statement.
- **Detector escape** (the actual observable used): a path-summed
  ratio that is **not** monotone-suppressed by an arbitrarily small
  gamma. The runner's data show escape ratios STILL ABOVE 1 for:
  - UNIFORM `f = 0.005` at gamma = 0.1, 0.2
  - UNIFORM `f = 0.01`  at gamma = 0.1, 0.2
  - GRAVITY            at gamma = 0.1, 0.2

So the note's "kernel-generic absorption under any nonzero field"
claim does not hold for the detector-escape observable as measured.
The link-level damping is real; the detector-escape suppression
requires sufficiently large gamma (≥ ~0.5) and is not generic.

The safe-claim boundary (per the audit) is:
- gamma = 0.5 suppresses detector escape for the tested nonzero fields.
- The 1/r gravity field uniquely shows the tested TOWARD → AWAY
  centroid crossover by gamma = 0.2.

The stronger "any nonzero field at any positive gamma" version of the
separation is NOT retained.

The repair target is to either distinguish local per-link attenuation
from total detector escape in the note, or add a theorem/runner
proving a thresholded escape-suppression criterion across gamma and
field families. That repair has not been done.

## Status

Archived as a terminal-failed historical record. The audit row
`kernel_vs_gravity_note` will remain `audited_failed` until the repair
above is completed.
