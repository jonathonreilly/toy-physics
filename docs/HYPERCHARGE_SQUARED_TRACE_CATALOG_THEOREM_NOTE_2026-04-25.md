# Hypercharge Squared Trace Catalog Theorem

**Date:** 2026-04-25

**Status:** Retained structural-identity subtheorem of the promoted
[`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
and
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md).
This note names and regression-tests the squared-hypercharge trace
identities already implicit in those parent surfaces. The single line
`Tr[Y^2] = 8/3` in
[`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
section 5 is extracted into a complete left-handed / right-handed /
one-generation / three-generation / GUT-consistency catalog.

This is a companion to the recent linear and cubic anomaly trace
catalogs: it does not expand the parent uniqueness theorem's scope and
does not introduce a new gauge group, anomaly, or representation.

**Primary runner:** `scripts/frontier_hypercharge_squared_trace_catalog.py`

## Statement

In the doubled-hypercharge convention used throughout the retained
anomaly notes (`Q = T_3 + Y/2`, with
`Y(Q_L) = +1/3`, `Y(L_L) = -1`,
`Y(u_R) = +4/3`, `Y(d_R) = -2/3`,
`Y(e_R) = -2`, `Y(nu_R) = 0`),
the squared hypercharge traces over the retained one-generation Standard
Model content satisfy

```text
(Y1)  Tr[Y^2]_LH         = 8/3,
(Y2)  Tr[Y^2]_RH         = 32/3,
(Y3)  Tr[Y^2]_one_gen    = 40/3,
(Y4)  Tr[Y^2]_three_gen  = 40,
(Y5)  Tr[Y_GUT^2]_three_gen
                          = (3/20) * Tr[Y^2]_three_gen
                          = 6
                          = Tr[T_a^2]_SU(2),three_gen
                          = Tr[T_a^2]_SU(3),three_gen.
```

Identity (Y5) is the structural content of the standard "5/3 ratio"
in the SU(5) embedding, expressed in the doubled convention.

## Retained Inputs

| Input | Authority |
| --- | --- |
| LH content `Q_L : (2,3)_{+1/3}`, `L_L : (2,1)_{-1}` | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) |
| RH completion `u_R, d_R, e_R, nu_R` with Standard Model hypercharges | [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) |
| Hypercharge identification on the retained left-handed surface | [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) |
| Three-generation orbit count | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) |
| SU(2), SU(3) Dynkin index `T(fund) = 1/2` convention | retained anomaly notes |

No observed coupling, mass, or running scale enters the catalog. The
SU(5) GUT comparison in (Y5) is a structural normalization statement,
not an observation-side claim about coupling unification.

## Derivation

### LH content (Y1)

The left-handed retained content has 8 states with weights and
multiplicities

| Block | SU(2) mult | SU(3) mult | states | `Y` | `Y^2` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `Q_L` | 2 | 3 | 6 | `+1/3` | `1/9` |
| `L_L` | 2 | 1 | 2 | `-1`   | `1`   |

Summing the squared-hypercharge weight over all 8 states,

```text
Tr[Y^2]_LH = 6 * (1/3)^2 + 2 * (-1)^2
           = 6/9 + 2
           = 2/3 + 2
           = 8/3.
```

This is the line stated implicitly in
[`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
section 5.

### RH content (Y2)

The right-handed completion required by anomaly cancellation has 8
states:

| Block | SU(2) mult | SU(3) mult | states | `Y` | `Y^2` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `u_R` | 1 | 3 | 3 | `+4/3` | `16/9` |
| `d_R` | 1 | 3 | 3 | `-2/3` | `4/9`  |
| `e_R` | 1 | 1 | 1 | `-2`   | `4`    |
| `nu_R`| 1 | 1 | 1 | `0`    | `0`    |

Summing,

```text
Tr[Y^2]_RH = 3 * (4/3)^2 + 3 * (-2/3)^2 + 1 * (-2)^2 + 1 * 0^2
           = 48/9 + 12/9 + 4 + 0
           = 16/3 + 4/3 + 12/3
           = 32/3.
```

The eight-eight LH-RH split mirrors the
`8 + 8 = 16`-state one-generation count carried by
[`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md).

### One-generation total (Y3)

```text
Tr[Y^2]_one_gen = Tr[Y^2]_LH + Tr[Y^2]_RH
                = 8/3 + 32/3
                = 40/3.
```

### Three generations (Y4)

The retained orbit algebra
`8 = 1 + 1 + 3 + 3` carries three full generations
([`KOIDE_THREE_GAP_CLOSURE_NOTE_2026-04-22.md`](KOIDE_THREE_GAP_CLOSURE_NOTE_2026-04-22.md))
with identical hypercharges per generation. So

```text
Tr[Y^2]_three_gen = 3 * 40/3 = 40.
```

### GUT consistency (Y5)

The SU(2) and SU(3) Dynkin sums over one generation evaluate to

```text
Tr[T_a^2]_SU(2),one_gen
   = (3 colors)(1 species)(1/2)   [Q_L]
   + (1)(1)(1/2)                   [L_L]
   = 3/2 + 1/2 = 2.

Tr[T_a^2]_SU(3),one_gen
   = (1 SU(3) fund)(2 SU(2))(1/2)  [Q_L]
   + (1 SU(3) fund)(1)(1/2)        [u_R]
   + (1 SU(3) fund)(1)(1/2)        [d_R]
   = 1 + 1/2 + 1/2 = 2.
```

Three generations give `Tr[T_a^2]_SU(2),three_gen = Tr[T_a^2]_SU(3),three_gen = 6`.

GUT normalization fixes the ratio between the abelian and nonabelian
quadratic Casimir traces by requiring
`Tr[Y_GUT^2] = Tr[T_a^2]_simple`. Setting

```text
Y_GUT^2 = (3/20) * Y^2     (doubled convention, (Y5)),
```

equivalently `Y_GUT = sqrt(3/5) * Y_min` in the conventional minimal
hypercharge `Y_min = Y/2`, gives

```text
Tr[Y_GUT^2]_three_gen = (3/20) * 40 = 6,
```

matching the SU(2) and SU(3) Dynkin sums. This is the doubled-convention
restatement of the standard `g_1^2 = (5/3) g_Y^2` SU(5) embedding.

## Catalog

| Identity | Trace | Value |
| --- | --- | ---: |
| (Y1) | `Tr[Y^2]_LH` | `8/3` |
| (Y2) | `Tr[Y^2]_RH` | `32/3` |
| (Y3) | `Tr[Y^2]_one_gen` | `40/3` |
| (Y4) | `Tr[Y^2]_three_gen` | `40` |
| (Y5) | `Tr[Y_GUT^2]_three_gen` | `6` |

Bookkeeping companions:

| Companion | Trace | Value |
| --- | --- | ---: |
| SU(2) Dynkin | `Tr[T_a^2]_SU(2),three_gen` | `6` |
| SU(3) Dynkin | `Tr[T_a^2]_SU(3),three_gen` | `6` |
| GUT factor | `Y_GUT^2 / Y^2` | `3/20` |
| GUT factor (minimal) | `Y_GUT^2 / Y_min^2` | `3/5` |

## Cross-Checks Against Existing Catalogs

- (Y1) reproduces the inline statement
  `Tr[Y^2] = 8/3` in
  [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  section 5 with full multiplicity bookkeeping.
- (Y3) is consistent with the LH-only `Tr[Y^3] = -16/9` and
  RH cancellation pattern catalogued in
  [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  Step 1 -- both rely on the same multiplicity table.
- (Y5) is the structural origin of the `5/3` factor that appears in
  one-loop coupling unification arguments. This note does not promote
  any unification claim; it only names the ratio of squared traces.

## Scope

This note claims:

- exact rational values of `Tr[Y^2]` over the retained LH content (`8/3`),
  RH completion (`32/3`), one generation (`40/3`), and three
  generations (`40`);
- the GUT-consistency identity `Tr[Y_GUT^2]_three_gen = 6` matching the
  SU(2) and SU(3) Dynkin sums on the same content, with conversion
  factor `Y_GUT^2 / Y^2 = 3/20` in the doubled convention.

This note does not claim:

- a new derivation of the SU(5) embedding or any GUT-scale physics;
- any one-loop running, threshold matching, or coupling-unification
  prediction;
- any new neutral singlet or right-handed-content claim beyond the
  parent uniqueness theorem;
- any BSM hypercharge assignment, dark-photon mixing, or hidden U(1)
  identification.

## Reproduction

```bash
python3 scripts/frontier_hypercharge_squared_trace_catalog.py
```

Expected result:

```text
TOTAL: PASS=35, FAIL=0
```

The runner uses the Python standard library only.

## Cross-References

- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  -- parent inline statement of `Tr[Y^2] = 8/3`.
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  -- parent uniqueness theorem fixing the RH hypercharge values.
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  -- retained left-handed quark and lepton doublet content.
- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  -- companion linear and cubic trace catalog.
- [`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`](SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md)
  -- companion cubic SU(3) trace cancellation.
- [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
  -- companion SU(2) global anomaly count.
- [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md)
  -- companion B-L anomaly freedom catalog.
