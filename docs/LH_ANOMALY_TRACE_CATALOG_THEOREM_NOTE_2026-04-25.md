# Left-Handed-Content Anomaly Trace Catalog Theorem

**Date:** 2026-04-25

**Status:** bounded_theorem on the assumed left-handed matter surface. The
five exact rational identities (C1)-(C5) are arithmetic consequences of
the LH content `Q_L : (2, 3)_{1/3}` and `L_L : (2, 1)_{-1}` and the
standard ABJ trace formulae. The LH content itself is admitted as
external input from `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` (currently
`decoration_under_lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`,
retained) and `HYPERCHARGE_IDENTIFICATION_NOTE.md` (currently
`audited_renaming`); this catalog does not derive the LH content. Given
the premise, the rational/integer values are exact via
`fractions.Fraction` arithmetic.

**Type:** bounded_theorem (algebraic-identity catalog on the assumed
LH content surface; see `## Scope` for the explicit not-claimed
boundary).

**Claim type:** bounded_theorem

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
| Retained anomaly-cancellation usage | `ANOMALY_FORCES_TIME_THEOREM.md` |

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

The Witten Z_2 cancellation condition is `N_D mod 2 = 0`, which is a
companion claim handled by
`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md` (sibling theorem,
not a load-bearing input here);
this catalog only records the LH-only contribution `4`.

## Role In The Anomaly System

The right-handed solve packaged in
`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`
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

### What this bounded theorem claims

Given the LH-content premise

```text
Q_L : (2, 3)_{1/3} with weak multiplicity 2 and color multiplicity 3,
L_L : (2, 1)_{-1} with weak multiplicity 2 and color multiplicity 1,
```

(and the standard Dynkin factors `T(3) = T(2) = 1/2`), this catalog
proves the exact rational/integer identities (C1)-(C5):

```text
(C1) Tr[Y]_LH         = 6*(1/3) + 2*(-1) = 0.
(C2) Tr[Y^3]_LH       = 6*(1/27) + 2*(-1) = -16/9.
(C3) Tr[SU(3)^2 Y]_LH = (1/2)*2*(1/3) = 1/3.
(C4) Tr[SU(2)^2 Y]_LH = (1/2)*[3*(1/3) + 1*(-1)] = 0.
(C5) N_D(Witten, LH)  = 3 + 1 = 4.
```

These are pure algebraic-identity (class A) checks: each value is a
finite rational expression of the LH content fields' multiplicities
and hypercharges, computed exactly via `fractions.Fraction` and tested
for equality with the catalogued rational. The class-B authority
existence checks are auxiliary (verifying that the parent and sibling
notes that *use* these values are present on main); they are not the
load-bearing content.

### What this theorem does NOT claim

- It does not derive the LH content `Q_L : (2, 3)_{1/3}`,
  `L_L : (2, 1)_{-1}` itself; that input is admitted from
  `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` and
  `HYPERCHARGE_IDENTIFICATION_NOTE.md`.
- It does not solve for the right-handed hypercharges (handled in
  `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`).
- It does not assert full anomaly cancellation across LH+RH; cancellation
  is the claim of the upstream solve, not this catalog.
- It does not assert the Witten Z_2 cancellation (handled in
  `SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`); only the
  LH-only contribution `4` is reported here.
- It does not assert SU(3)^3 cubic cancellation (handled in
  `SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`).
- It does not assert B-L anomaly closure (handled in
  `BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`).
- It does not introduce BSM matter content or any other trace identity
  outside (C1)-(C5).

### Audit-readiness boundary

The catalog is audit-ready as `bounded_theorem` -> `retained_bounded`:
the load-bearing checks are exact `fractions.Fraction` arithmetic
identities (class A) on the named LH content. The runner's cross-note
authority checks (class B) are scoped as auxiliary existence checks,
not as load-bearing arithmetic. The 26 PASS lines decompose as:

| class | count | meaning |
| --- | ---: | --- |
| A    | 19   | exact `fractions.Fraction` identity checks (C1-C5 + algebraic decompositions + status-boundary safety asserts) |
| B    | 7    | parent/sibling note existence + retained-LH content authority |

This catalog therefore presents as A-dominant rather than B-dominant
once the runner's content vs. authority lines are separated.

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

### Load-bearing inputs (cited as authority)

- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  - retained left-handed content authority (currently
    `decoration_under_lh_doublet_traceless_abelian_eigenvalue_ratio_narrow_theorem_note_2026-05-02`,
    retained).
- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  - retained `Y(Q_L) = 1/3`, `Y(L_L) = -1` identification (currently
    `audited_renaming`).
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  - retained `N_c = 3` color count.
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md)
  - retained `SU(2)_L` weak-doublet structure.

### Logical siblings (NOT load-bearing inputs)

These notes share the same anomaly cancellation backbone but are
independent companion theorems; this catalog does not import their
results, and they do not import this catalog's results. They are
referenced here as cross-readers for the broader anomaly system and
for the human reader, not as upstream authority.

- `ANOMALY_FORCES_TIME_THEOREM.md` (parent theorem citing these LH
  trace values inline; the values here are the inputs the parent
  uses, but the parent's claim — that anomaly cancellation forces
  d_t = 1 — is not imported here).
- `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`
  (companion solving the RH hypercharges using these LH inputs).
- `SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`
  (companion verifying the Witten Z_2 cancellation across the full
  content; this catalog only computes the LH-only contribution
  `N_D = 4`).
- `SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`
  (companion handling the SU(3)^3 cubic gauge anomaly cancellation
  on the LH+RH content; this catalog only computes the LH-only
  C3 trace `1/3`).
- `BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`
  (companion handling the B-L gauge-extension anomaly closure).
