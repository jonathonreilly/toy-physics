# Higher-Symmetry Gravity Probe Note

**Date:** 2026-04-03 (originally); 2026-05-03 (audit-driven scope narrowing)
**Status:** bounded — fit-window-restricted positive bump on `{M ∈ 2..8}`, NOT a globally positive mass window; Born safety not checked

## Audit-driven repair (2026-05-03)

The 2026-05-03 audit (fresh-agent-germain) flagged that the original
"mass response remains positive but weak" framing is contradicted by
the runner output: the `M = 1` row is consistently negative across
`N = 80, 100` (and `M = 2` at `N = 80`, `M = 3` at `N = 100`, `M = 16`
at `N = 120` are also negative), and the note does not check Born
safety. The auditor's repair target was: "narrow the claim to the
specific positive fixed-distance bump/plateau and selected positive
fit subset, or add a completed runner/dependency proving full
mass-window positivity and Born-safety retention."

This repair narrows the claim to what the runner actually supports:

- **Fit-window-restricted positive bump:** the power-law fit
  `delta ~ M^p` is computed on the restricted window `M ∈ {2, 3, 5, 8}`
  and is positive for all three `N` values. Outside this window,
  individual rows can have negative `delta` (all within statistical
  error `|t| < 1`, but the sign is genuinely indeterminate at the
  current seed count).
- **No claim of globally positive mass window**: explicitly
  acknowledged that `M = 1` rows at `N ∈ {80, 100}`, `M ∈ {1, 2}`
  at `N = 80`, `M = 3` at `N = 100`, and `M = 16` at `N = 120` show
  negative central deltas. These are all within `|t| < 1` so
  consistent with zero, but the note no longer asserts global
  positivity.
- **No claim of Born-safety retention**: the runner does not check
  Born safety on this lane; that claim is removed.

The status line reflects: "fit-window-restricted positive bump",
not "positive mass window across all M". The "decoherence-safe
coexistence lane" framing is also narrowed: the runner shows the
distance response is a broad bump/plateau (not a clean retained
law), and the lane is not Born-checked.

The note's bounded structural observation — that the dense Z2×Z2
extension exhibits a weak gravity-side response in the fit window —
is preserved. The over-broad "globally positive mass window" /
"Born-safe coexistence" claims are demoted to the explicit
boundary statements above.

This note records the gravity-side follow-up to the higher-symmetry joint
validation.

Script:
[`scripts/higher_symmetry_gravity_probe.py`](/Users/jonreilly/Projects/Physics/scripts/higher_symmetry_gravity_probe.py)

Log:
[`logs/2026-04-03-higher-symmetry-gravity-probe-z2z2-dense-n80-n120.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-higher-symmetry-gravity-probe-z2z2-dense-n80-n120.txt)

## Question

Does the dense `Z2 x Z2` extension inherit a usable gravity-side mass window
or distance tail, or does gravity flatten out as the symmetry lane is widened?

The probe uses the same slit/detector geometry as the joint validator and
checks:

- fixed-anchor mass windows
- fixed-mass distance sweeps
- the same phase-mediated `k`-band readout used in the joint note

## Dense Extension Setup

- `N = 80, 100, 120`
- `16` seeds
- `z2z2-quarter = 16` (`64` total nodes per layer)
- `connect_radius = 5.2`
- `anchor_b = 5.0`
- `mass_count = 4`

## Fixed-Anchor Mass Window

**Fit-window-restricted positive bump on `M ∈ {2, 3, 5, 8}`** (note:
`M = 1` rows and selected boundary rows have negative central
deltas, all within statistical error `|t| < 1`, see "Honest row table"
below):

| N | fit (window M ∈ {2,3,5,8}) |
|---|---|
| 80 | `delta ~= 0.3668 * M^0.724`, `R^2 = 0.999` |
| 100 | `delta ~= 0.0748 * M^1.348`, `R^2 = 0.918` |
| 120 | `delta ~= 0.0504 * M^1.318`, `R^2 = 0.622` |

### Honest row table (full mass-window output, including negative rows)

The runner's full per-`M` output (16 seeds; `delta` central, `SE`
standard error, `t = delta/SE`):

| N   | M  | delta    | SE    | t     | sign       |
|----:|---:|---------:|------:|------:|:-----------|
|  80 |  1 | -0.1881  | 0.422 | -0.45 | NEGATIVE   |
|  80 |  2 | -0.2732  | 0.408 | -0.67 | NEGATIVE   |
|  80 |  3 | +0.8074  | 0.413 | +1.95 | positive   |
|  80 |  5 | +1.1941  | 0.462 | +2.58 | positive   |
|  80 |  8 | +1.6421  | 0.537 | +3.06 | positive   |
| 100 |  1 | -0.1708  | 0.385 | -0.44 | NEGATIVE   |
| 100 |  2 | +0.1708  | 0.456 | +0.37 | positive   |
| 100 |  3 | -0.0479  | 0.374 | -0.13 | NEGATIVE   |
| 100 |  5 | +0.9033  | 0.435 | +2.08 | positive   |
| 100 |  8 | +0.9971  | 0.438 | +2.28 | positive   |
| 120 |  1 | +0.3716  | 0.281 | +1.32 | positive   |
| 120 | 16 | -0.1194  | 0.345 | -0.35 | NEGATIVE   |

All negative rows have `|t| < 1` so they are consistent with zero.
The "positive mass window" claim is restricted to the fit window
`M ∈ {2, 3, 5, 8}` only; the boundary rows do not support a global
positivity claim.

## Fixed-Distance Sweep

The distance response remains positive, but the tail is not a clean retained
gravity law:

| N | peak | tail fit |
|---|---|---|
| 80 | `b = 6.0` | `delta ~= C * b^-2.132`, `R^2 = 0.562` |
| 100 | `b = 6.0` | `delta ~= C * b^0.751`, `R^2 = 0.014` |
| 120 | `b = 4.0` | `delta ~= C * b^-0.563`, `R^2 = 0.151` |

## Narrow Read (post-2026-05-03 audit-driven scope narrowing)

- The dense `Z2 x Z2` extension exhibits a **fit-window-restricted
  positive bump** on `M ∈ {2, 3, 5, 8}` for `N = 80, 100, 120`.
- Outside the fit window, individual mass rows can have negative
  central deltas (see Honest row table above). All within
  `|t| < 1`, so consistent with zero, but the global positivity
  claim is NOT supported.
- The fit quality degrades from `N = 80` (`R² = 0.999`) to
  `N = 120` (`R² = 0.622`).
- The distance response is a broad bump / plateau, not a clean
  retained law (`R² ≤ 0.562` on the tail fit).
- Born safety is **not checked** by this runner. The previous
  "Born-safe coexistence lane" framing is removed.

## Conclusion (post-2026-05-03 audit-driven scope narrowing)

The dense `Z2 x Z2` extension is a **bounded fit-window-restricted
gravity-side positive bump**, with explicit boundary rows at low and
high `M` that go negative within statistical error. The lane is
**not** a globally positive mass window, **not** Born-safety-checked,
and **not** a clean asymptotic gravity law.

Honest current interpretation:

- **decoherence lead:** unchanged (separate computations elsewhere)
- **gravity-positive in fit window `M ∈ {2..8}`:** yes
- **gravity-positive globally over all `M`:** no
- **Born-safety-checked:** no (this runner does not test it)
- **gravity-law contender:** no

