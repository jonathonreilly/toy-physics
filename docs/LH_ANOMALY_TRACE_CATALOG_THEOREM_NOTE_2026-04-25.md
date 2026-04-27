# Left-Handed-Content Anomaly Trace Catalog Theorem

**Date:** 2026-04-25

**Status:** proposed_retained structural-arithmetic subtheorem on the proposed_retained
left-handed matter surface. Catalogues, names, and regression-tests the
five specific anomaly-trace identities on the retained left-handed
content `Q_L + L_L` already used in the body of
[`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md).
The numerical values are the explicit inputs to the right-handed
hypercharge solve packaged by
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md).

**Primary runner:** `scripts/frontier_lh_anomaly_trace_catalog.py`

## Statement

On the retained left-handed content

```text
Q_L : (2, 3)_{+1/3},     6 LH Weyl states (3 colors x 2 weak),
L_L : (2, 1)_{-1},       2 LH Weyl states (1 color x 2 weak),
```

with the doubled-hypercharge convention `Q = T_3 + Y/2`, the four
perturbative anomaly traces and the SU(2) Witten doublet count compute to
the exact rational/integer values

```text
(C1)  Tr[Y]_LH                = 0,
(C2)  Tr[Y^3]_LH              = -16/9,
(C3)  Tr[SU(3)^2 Y]_LH        = 1/3,
(C4)  Tr[SU(2)^2 Y]_LH        = 0,
(C5)  N_D(Witten, LH)          = 4.
```

The Dynkin factors `T(3) = 1/2` for the SU(3) fundamental and
`T(2) = 1/2` for the SU(2) fundamental are retained as the standard
choice; (C3) is reported with the `T(3)` factor included so the value
matches the value catalogued in the body of `ANOMALY_FORCES_TIME_THEOREM`.

These five rational/integer values are the explicit retained-LH input data
to the SM hypercharge uniqueness solve. They are not new derivations of the
left-handed content; they audit that the retained content carries the
specific rational fingerprints already used in adjacent retained theorems.

## Retained Inputs

| Input | Authority |
| --- | --- |
| Retained left-handed `Q_L`, `L_L` content | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) |
| Retained `N_c = 3` color count | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| Retained `SU(2)_L` weak-doublet structure | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) |
| Standard ABJ anomaly-trace formulae | textbook |
| Retained anomaly-cancellation usage | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) |

No observed mass, charge, or cross-section enters the catalog.

## Derivation

Using retained multiplicities and hypercharges:

| Field | LH count | Hypercharge `Y` |
| --- | ---: | ---: |
| `Q_L` | `2 N_c = 6` | `+1/3` |
| `L_L` | `2` | `-1` |

### (C1) Linear hypercharge trace

```text
Tr[Y]_LH  =  6 (1/3) + 2 (-1)
          =  2 - 2
          =  0.
```

### (C2) Cubic hypercharge trace

```text
Tr[Y^3]_LH  =  6 (1/3)^3 + 2 (-1)^3
            =  6/27 - 2
            =  2/9 - 18/9
            =  -16/9.
```

### (C3) Mixed `SU(3)^2 U(1)_Y` trace

Only `Q_L` (SU(3) fundamental, weak doublet) contributes:

```text
Tr[SU(3)^2 Y]_LH  =  T(3) * (weak multiplicity) * Y(Q_L)
                  =  (1/2) * 2 * (1/3)
                  =  1/3.
```

### (C4) Mixed `SU(2)^2 U(1)_Y` trace

`Q_L` and `L_L` are both SU(2) doublets. Color multiplicities enter:

```text
Tr[SU(2)^2 Y]_LH  =  T(2) * (color multiplicity) * Y of doublet
                  =  (1/2) * [3 * (1/3) + 1 * (-1)]
                  =  (1/2) * (1 - 1)
                  =  0.
```

### (C5) Witten SU(2) Z_2 doublet count

The retained left-handed content provides

```text
N_D(Witten, LH)  =  N_c (Q_L color copies of one weak doublet) + 1 (L_L)
                 =  3 + 1
                 =  4.
```

The Witten Z_2 cancellation condition is `N_D mod 2 = 0`, which is
verified in
[`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md);
this catalog only records the LH-only contribution `4`.

## Role In The Anomaly System

The right-handed solve packaged in
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
sets the (LH + RH) traces (C1)-(C4) to zero and solves for the four RH
hypercharges. The catalog values

```text
LH side: (Tr[Y], Tr[Y^3], Tr[SU(3)^2 Y]) = (0, -16/9, 1/3)
```

are the rational right-hand-side targets of the RH-side cancellation
equations:

```text
3 (y_1 + y_2) + y_3 + y_4         = 0,           cancels Tr[Y]_LH = 0,
3 (y_1^3 + y_2^3) + y_3^3 + y_4^3 = -16/9,       cancels Tr[Y^3]_LH = -16/9,
y_1 + y_2                          = 2/3,         cancels Tr[SU(3)^2 Y]_LH = 1/3,
                                                  (the (1/2) Dynkin factor cancels.)
```

Imposing `y_4 = 0` (neutral-singlet input) and `y_1 > 0` (electric-charge
labeling) then yields the unique SM RH hypercharges
`(y_1, y_2, y_3, y_4) = (4/3, -2/3, -2, 0)`. This catalog records the
left-hand-side input arithmetic; the solve and uniqueness statement live
in the hypercharge-uniqueness companion.

## Scope

This note claims:

- the exact rational values (C1)-(C4) for the four perturbative anomaly
  traces on the retained LH content;
- the integer Witten doublet count (C5) on the retained LH content;
- consistency with the LH-only entries in the anomaly table of
  [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md).

This note does not claim:

- the right-handed completion (handled in the SM hypercharge uniqueness
  theorem);
- the Witten cancellation (handled in the SU(2) Witten Z_2 theorem);
- the SU(3)^3 cubic gauge cancellation (handled in the SU(3)^3 theorem);
- the B-L anomaly closure (handled in the B-L anomaly-freedom theorem);
- a native-axiom derivation of the LH content itself;
- any beyond-Standard-Model trace identity.

## Reproduction

```bash
python3 scripts/frontier_lh_anomaly_trace_catalog.py
```

Expected result:

```text
TOTAL: PASS=26, FAIL=0
```

The runner uses the Python standard library only and operates entirely on
exact `fractions.Fraction` arithmetic.

## Cross-References

- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  - parent theorem citing these LH trace values inline.
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  - companion solving the RH hypercharges using these LH inputs.
- [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
  - companion verifying the Witten cancellation across the full content.
- [`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`](SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md)
  - companion handling the cubic SU(3) gauge anomaly.
- [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md)
  - companion handling the B-L gauge-extension anomaly closure.
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  - retained left-handed content authority.
- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  - retained `Y(Q_L) = 1/3`, `Y(L_L) = -1` identification.
