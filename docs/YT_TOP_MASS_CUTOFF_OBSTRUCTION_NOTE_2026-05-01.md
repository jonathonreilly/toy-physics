# YT Top-Mass Cutoff Obstruction Note

**Date:** 2026-05-01
**Status:** bounded cutoff obstruction / pilot compute evidence
**Runner:** `scripts/frontier_yt_top_mass_cutoff_obstruction.py`
**Certificate:** `outputs/yt_top_mass_cutoff_obstruction_2026-05-01.json`

```yaml
actual_current_surface_status: bounded cutoff obstruction / pilot compute evidence
conditional_surface_status: "A direct top-correlator route may reopen with a much finer scale, a heavy-quark effective treatment, or a different retained selector."
hypothetical_axiom_status: null
admitted_observation_status: "PDG top mass is used as an external target for cutoff assessment only."
proposal_allowed: false
proposal_allowed_reason: "The mass-bracketing pilot indicates cutoff obstruction, not production-ready retained closure."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Question

Is the direct staggered top-correlator production route close enough to the
physical top mass to justify scaling immediately to the full three-volume
production campaign?

## Pilot Bracket Result

No.

At the current Sommer-scale conversion in the harness,

```text
1 lattice mass unit = 2.119291769496 GeV
```

The physical top target `172.56 GeV` would require

```text
a m_t ~= 81.423428
```

The mass-bracketing pilot scanned bare masses `1, 2, 4, 8, 16` on `12^3 x 24`
with `50` thermalization sweeps, `25` saved configurations, and separation
`5`.  It found:

| `m_bare` | fitted `m_lat` | `chi^2/dof` | proxy GeV |
|---:|---:|---:|---:|
| 1 | 2.238868 | 0.256191 | 4.744814 |
| 2 | 3.124670 | 0.075137 | 6.622087 |
| 4 | 4.270790 | 0.021292 | 9.051050 |
| 8 | 5.575509 | 0.000000 | 11.816131 |
| 16 | 6.939225 | 0.000000 | 14.706242 |

The scan is monotone, but strongly sublinear.  The highest scanned point is
only `8.52%` of the physical top target and is more than a factor of `11`
below the required lattice mass.

## Interpretation

This is not a numerical failure of the pilot harness.  The gauge update,
staggered Dirac build, CG solve, correlator measurement, and fitter all ran.
CG residuals remained below `1e-8`.

The problem is scale.  With the current `a ~= 0.093 fm` anchor, a relativistic
direct top correlator would require `a m_t >> 1`.  That is a cutoff-obstructed
regime for this direct production plan.

## Consequence For PR #230

The full production campaign should not be treated as the next automatic step
at the current scale.  The live options are:

- introduce a much finer scale-setting path and re-benchmark;
- switch to an explicitly heavy-quark effective/top-integrated treatment;
- keep the direct correlator lane as a measurement-gate artifact, not retained
  closure;
- pursue a non-MC selector route, while preserving the already recorded
  stationarity and assumption-boundary no-gos.

## Verification

```bash
python3 scripts/frontier_yt_top_mass_cutoff_obstruction.py
# SUMMARY: PASS=8 FAIL=0
```
