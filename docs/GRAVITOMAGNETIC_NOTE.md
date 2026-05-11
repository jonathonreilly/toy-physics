# Velocity-Dependent Phase Shift on the Imposed-Source Layered DAG

**Date:** 2026-04-06 (audit-status note added 2026-05-10)
**Status:** bounded computational diagnostic — monotonic velocity-dependent
phase shift on the configured imposed-source layered-DAG family. The
small-`|v|` data is consistent with antisymmetry within stated tolerance
on the configured probe; the large-`|v|` data is **not** antisymmetric
(see audit-status note). No gravitomagnetic / Shapiro bridge is derived
inside this packet.

## Audit-status note (2026-05-10)

The 2026-05-05 audit verdict (`audited_failed`, `chain_closes=false`)
flagged that the original note over-promoted the configured numerical
table to an antisymmetric gravitomagnetic / Shapiro observable, but the
table itself fails strict antisymmetry at `|v|=0.5`, and no cited
authority derives the Shapiro / gravitomagnetic bridge from the
imposed-source runner.

> "the table itself fails strict antisymmetry at |v|=0.5 and no cited
> authority derives the Shapiro/gravitomagnetic observable bridge from
> the imposed-source runner ... the reported deltas are not
> antisymmetric over the stated velocity set: mean delta(+0.5)=+0.0056
> while mean delta(-0.5)=-0.0080, leaving a large even component."

Admitted-context inputs (carrier framework, not derived in this note):

- the imposed source trajectory `z_src(layer) = z0 + v_z * (layer - gl) * H`
  on the layered DAG (not a self-consistent moving solution)
- the propagator `prop_moving` with phase `k * L * (1 - lf)` and
  conical weight `exp(-BETA * theta^2)` over a finite `c_field` cone
- the field amplitude `s/r` with regulator `+0.1` and reach
  `c_field * dt * H + 0.1`
- the layered DAG geometry `grow(seed, drift, restore)` over three
  configured families `(0.20, 0.70)`, `(0.05, 0.30)`, `(0.50, 0.90)`

Configured probe parameters (proxy thresholds, not derived):

- `BETA = 0.8`, `K = 5.0`, `MAX_D_PHYS = 3`, `H = 0.5`, `NL = 30`,
  `PW = 8`, `MASS_Z = 3.0`, `S = 0.004`, `C_FIELD = 0.5`
- `V_VALUES = [-0.5, -0.2, 0.0, +0.2, +0.5]` and `SEEDS = [0, 1]`

Bounded retained diagnostic: under the configured probe parameters,
the mean phase delta from the static `v=0` baseline is monotonic in
`v_z` and the small-`|v|` rows agree with antisymmetry within the
configured tolerance:

| `|v|` | mean delta(+) | mean delta(-) | even component | antisymmetric? |
| ---: | ---: | ---: | ---: | --- |
| `0.2` | `+0.0032` | `-0.0035` | `~0.00015` (< 5%) | yes (within tol) |
| `0.5` | `+0.0056` | `-0.0080` | `~0.0012` (~ 18%) | **no** |

Honest revision: the small-`|v|` row is consistent with antisymmetry on
the configured probe, but the `|v|=0.5` row carries a large even
component (`(delta(+0.5) + delta(-0.5))/2 ~ -0.0012`, comparable to
half the antisymmetric signal), so the antisymmetry claim does not hold
across the full velocity set on this probe. The original
"antisymmetric in v, portable across 3 families" framing is retracted
to a bounded small-`|v|` consistency observation; no
gravitomagnetic-frame-dragging analog claim is preserved inside this
packet.

Blocked-on: this row stays `audited_failed` until either the runner is
extended to a self-consistent moving source (so the imposed trajectory
is no longer an admitted input), or a retained Shapiro /
gravitomagnetic bridge theorem is supplied that derives the
phase-versus-`v_z` observable from a graph-native field action with
controlled antisymmetric / even decomposition. The bounded computational
diagnostic — phase is monotonic in `v_z` and small-`|v|` deltas are
antisymmetric within configured tolerance across the three configured
grown families — is unaffected by this status note.

## Artifact chain

- [`scripts/gravitomagnetic_portable.py`](../scripts/gravitomagnetic_portable.py)
- [`logs/2026-04-06-gravitomagnetic-portable.txt`](../logs/2026-04-06-gravitomagnetic-portable.txt)
- This note

## Question (configured probe)

On the configured imposed-source layered-DAG family with parameters
listed in the audit-status note above, how does the phase observable
recorded by the propagator depend on the imposed source velocity `v_z`?

## Result

Phase lag at c=0.5, s=0.004, z0=3.0 (2 seeds per family):

| v_z | Fam 1 phase | Fam 2 phase | Fam 3 phase |
| ---: | ---: | ---: | ---: |
| -0.5 | +0.0542 | +0.0548 | +0.0538 |
| -0.2 | +0.0589 | +0.0590 | +0.0586 |
| 0.0 | +0.0623 | +0.0624 | +0.0621 |
| +0.2 | +0.0655 | +0.0654 | +0.0655 |
| +0.5 | +0.0680 | +0.0678 | +0.0680 |

Delta from static (v=0):

| v_z | Fam 1 | Fam 2 | Fam 3 | Mean |
| ---: | ---: | ---: | ---: | ---: |
| -0.5 | -0.0081 | -0.0076 | -0.0083 | -0.0080 |
| -0.2 | -0.0035 | -0.0034 | -0.0036 | -0.0035 |
| +0.2 | +0.0032 | +0.0030 | +0.0034 | +0.0032 |
| +0.5 | +0.0056 | +0.0054 | +0.0059 | +0.0056 |

## Properties (configured probe)

1. **Monotonic in `v_z` and in `|v|`**: phase increases monotonically
   from `v=-0.5` through `v=0` to `v=+0.5`, and `|delta|` increases
   with `|v|` on every family.
2. **Small-`|v|` antisymmetry within tolerance**: at `|v|=0.2`,
   delta(+0.2) ~ +0.0032 and delta(-0.2) ~ -0.0035 leave an even
   component below 5% of the signal, consistent with antisymmetry on
   the configured probe.
3. **Large-`|v|` antisymmetry fails**: at `|v|=0.5`, delta(+0.5) ~
   +0.0056 and delta(-0.5) ~ -0.0080 leave an even component near
   `-0.0012`, comparable to half the antisymmetric signal. This is the
   audit blocker; the original "antisymmetric in v" claim is retracted
   to small-`|v|` only.
4. **Portable across the three configured families**: the per-family
   spread on the delta column at any fixed `v` stays within ~12%, but
   this is a configured-probe portability statement, not a portability
   law.

## Claim boundary

This row records a bounded computational diagnostic on a configured
imposed-source layered-DAG probe with the parameters listed above. It
does NOT claim:

- equivalence to GR gravitomagnetic frame-dragging (no tensor field is
  derived);
- antisymmetry of the phase observable across the full velocity set
  (the `|v|=0.5` row fails antisymmetry by ~18% even component);
- a Shapiro / gravitomagnetic observable bridge from the imposed-source
  runner to a graph-native field action;
- self-consistency of the moving source (the trajectory is imposed).
