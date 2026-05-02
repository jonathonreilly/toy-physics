# SM Hypercharge Uniqueness Without ν_R Input — Anomaly Cancellation Alone

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the **derivation** that, on the cited framework
left-handed content (Q_L, L_L) plus minimal SU(2)-singlet right-handed
completion **without ν_R**, the right-handed hypercharges
`(y_1, y_2, y_3) = Y(u_R, d_R, e_R)` are uniquely fixed at
`(+4/3, -2/3, -2)` (the SM values, doubled-Y convention) by **anomaly
cancellation alone**, with **no neutral-singlet input**. The 4-unknown
parent system (`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`)
imports `Y(ν_R) = 0` from `HYPERCHARGE_IDENTIFICATION_NOTE.md` to break
the residual freedom; the 3-unknown system on the no-ν_R sector closes
without that input.
The ν_R species is then optional add-on, consistent with the framework
but not anomaly-required.
**Status:** independent audit required. This is a candidate derivation
that removes the load-bearing dependency on
`HYPERCHARGE_IDENTIFICATION_NOTE.md` from the parent's hypercharge
uniqueness chain. Under the scope-aware classification framework,
ratified status is computed by the audit pipeline; no author-side tier
is asserted in source.
**Runner:** [`scripts/frontier_sm_hypercharge_no_nu_r_derivation.py`](./../scripts/frontier_sm_hypercharge_no_nu_r_derivation.py)
**Authority role:** closing derivation that decouples
`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md` from
the neutral-singlet input.

## Parent input avoided by this derivation

From `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`
§5 ("What this theorem does and does not claim"):

> Does NOT claim a native-axiom derivation of `Y(ν_R) = 0`; the
> neutral-singlet identification is treated here as an input

That input is imported from `HYPERCHARGE_IDENTIFICATION_NOTE.md`,
which remains a separate normalization/readout authority. This note does
not close that separate task. Instead, it **removes the dependency**:
the SM hypercharge uniqueness theorem can be stated and proved without
`Y(ν_R) = 0`, and hence without depending on
`HYPERCHARGE_IDENTIFICATION_NOTE`.

## Statement

Let:

- (P1) `Q_L : (2, 3)_{+1/3}` from
  `LEFT_HANDED_CHARGE_MATCHING_NOTE.md`.
- (P2) `L_L : (2, 1)_{-1}` from
  `ONE_GENERATION_MATTER_CLOSURE_NOTE.md`.
- (P3) The framework requires an anomaly-cancelling
  SU(2)-singlet right-handed completion
  (`ANOMALY_FORCES_TIME_THEOREM.md` Step 2). The **minimal** completion
  consists of three colored/uncolored SU(2)-singlet RH species:
  `u_R : (1, 3)_{y_1}, d_R : (1, 3)_{y_2}, e_R : (1, 1)_{y_3}`.
  No ν_R is included in the minimal completion.
- (P4, admitted-context external) Standard ABJ anomaly cancellation
  requirement (Adler 1969; Bell-Jackiw 1969):

  ```text
  Tr[Y]            = 0    (mixed gauge-gravitational + linear)
  Tr[SU(3)² Y]     = 0    (mixed SU(3)²-U(1))
  Tr[Y³]           = 0    (cubic U(1)³)
  ```

  (The mixed `Tr[SU(2)² Y]` = 0 is automatic on the cited LH
  doublet content and adds no constraint on the RH singlet
  hypercharges; gravitational `Tr[Y]` coincides with the linear
  trace.)
- (P5, convention) `Q = T_3 + Y/2` doubled-Y convention with
  `Q(u_R) > 0` labelling (`u_R` is the up-type quark singlet, by
  convention).

**Conclusion (T1) (closing derivation: SM hypercharges from anomaly
alone, no ν_R input).** Under P1–P5 with the no-ν_R minimal RH
completion (P3), the right-handed hypercharges are **uniquely
forced** to be

```text
y_1 = Y(u_R) = +4/3,
y_2 = Y(d_R) = -2/3,
y_3 = Y(e_R) = -2,
```

i.e., the Standard Model values. The Q(u_R) > 0 convention breaks the
residual u_R ↔ d_R relabelling. **No neutral-singlet hypercharge
input is needed.**

**Conclusion (T2) (counterfactual: adding ν_R reopens the family).**
If a fourth SU(2)-singlet RH species `ν_R : (1, 1)_{y_4}` is added
without imposing `y_4 = 0`, the resulting 4-unknown × 3-equation
system has a 1-parameter family of solutions. The neutrality input
`y_4 = 0` IS load-bearing for uniqueness when ν_R is included; it is
NOT needed when ν_R is omitted.

**Conclusion (T3) (decoupling).** The chain
`SM hypercharge uniqueness ⇐ anomaly cancellation`
on the no-ν_R sector does NOT depend on
`HYPERCHARGE_IDENTIFICATION_NOTE.md`.
The parent row
`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`'s
hypercharge uniqueness statement can be evaluated without load-bearing
dependency on that neutral-singlet input.

## Proof

### Step 1: Anomaly traces on the no-ν_R sector

Sum over chiralities (LH with `+`, RH with `−`, in the LH-conjugate
frame summing all as `+`):

**Tr[Y]** (LH contribution + RH contribution):

```text
Tr[Y] = (LH) - (RH)
      = [6 · (1/3) + 2 · (-1)] - [3·y_1 + 3·y_2 + y_3]
      = (2 - 2) - 3(y_1 + y_2) - y_3
      = -3(y_1 + y_2) - y_3.                                    (E1)
```

**Tr[SU(3)² Y]** (only colored contributions, with SU(3) Dynkin index
T(3) = 1/2):

```text
Tr[SU(3)² Y] = (1/2) · [2 · (1/3)·3 - y_1·3 - y_2·3] / 3
             = (1/2) · [2 · (1/3) - y_1 - y_2]
             = (1/2) · [(2/3) - (y_1 + y_2)].                   (E2)
```

(The factor 2 in the LH sum is the SU(2)-doublet multiplicity per
quark color; the factor 3 from SU(3) multiplicity cancels between
trace and Dynkin normalization in the standard conventions.)

**Tr[Y³]** (cubic over chirality-signed fermions):

```text
Tr[Y³] = [6 · (1/3)³ + 2 · (-1)³] - [3·y_1³ + 3·y_2³ + y_3³]
       = [(6/27) - 2] - 3(y_1³ + y_2³) - y_3³
       = (2/9 - 2) - 3(y_1³ + y_2³) - y_3³
       = -16/9 - 3(y_1³ + y_2³) - y_3³.                         (E3)
```

### Step 2: Anomaly-cancellation system

Setting (E1), (E2), (E3) to zero:

```text
(A1)  3(y_1 + y_2) + y_3            = 0
(A2)  y_1 + y_2                     = 2/3
(A3)  3(y_1³ + y_2³) + y_3³         = -16/9
```

Three equations in three unknowns.

### Step 3: Reduction

From (A2) into (A1):

```text
3 · (2/3) + y_3 = 0  ⇒  y_3 = -2.                              (S1)
```

Substituting into (A3):

```text
3(y_1³ + y_2³) + (-2)³ = -16/9
3(y_1³ + y_2³) - 8     = -16/9
3(y_1³ + y_2³)         = 8 - 16/9 = (72 - 16)/9 = 56/9
y_1³ + y_2³            = 56/27.                                (S2)
```

### Step 4: Closed-form solve of (y_1, y_2)

Using `(y_1 + y_2)³ = y_1³ + y_2³ + 3 y_1 y_2 (y_1 + y_2)`:

```text
(2/3)³ = 56/27 + 3 y_1 y_2 (2/3)
8/27   = 56/27 + 2 y_1 y_2
2 y_1 y_2 = -48/27 = -16/9
y_1 y_2 = -8/9.                                                (S3)
```

So `y_1, y_2` are roots of the quadratic

```text
t² - (y_1 + y_2) t + y_1 y_2 = 0
t² - (2/3) t - 8/9 = 0.
```

Multiply by 9:

```text
9 t² - 6 t - 8 = 0
t = [6 ± √(36 + 288)] / 18 = [6 ± 18] / 18
t = 4/3   or   t = -2/3.
```

So `(y_1, y_2) ∈ {(4/3, -2/3), (-2/3, 4/3)}`. The two solutions are
related by the u_R ↔ d_R relabelling.

### Step 5: Q-labelling fixes the discrete swap

By P5 (`Q(u_R) > 0`, `Q = Y/2` for SU(2) singlets), `y_1 > 0`, so
`y_1 = +4/3`, `y_2 = -2/3`. ∎

### Step 6: Counterfactual — adding ν_R reopens the family

Add `ν_R : (1, 1)_{y_4}` (4th SU(2)-singlet species) with free `y_4`.
The anomaly traces become:

```text
(A1')  3(y_1 + y_2) + y_3 + y_4         = 0
(A2')  y_1 + y_2                        = 2/3   (unchanged: ν_R is
                                                  uncolored)
(A3')  3(y_1³ + y_2³) + y_3³ + y_4³    = -16/9
```

3 equations in 4 unknowns. From (A1') and (A2'):

```text
y_3 = -2 - y_4.
```

Substitute into (A3'):

```text
3(y_1³ + y_2³) + (-2 - y_4)³ + y_4³ = -16/9.
```

Expand `(-2 - y_4)³ = -(2 + y_4)³ = -(8 + 12 y_4 + 6 y_4² + y_4³)`:

```text
3(y_1³ + y_2³) - 8 - 12 y_4 - 6 y_4² - y_4³ + y_4³ = -16/9
3(y_1³ + y_2³) = 8 + 12 y_4 + 6 y_4² - 16/9
                = 56/9 + 12 y_4 + 6 y_4².
```

Combined with `y_1 + y_2 = 2/3` (from A2'), the system has a
**1-parameter family** of solutions parametrized by `y_4`.

Setting `y_4 = 0` recovers the previous SM solution (matches parent
note). Other choices give consistent but non-SM hypercharge
assignments — for example, `y_4 = 1/2` gives a different `y_3` and
shifted (y_1, y_2). The neutrality input `y_4 = 0` IS load-bearing
when ν_R is included.

### Step 7: Decoupling consequence

The minimal-no-ν_R derivation (Steps 1–5) does NOT consume `Y(ν_R) = 0`
at any step. Therefore the chain

```text
SM hypercharge values
    ⇐ anomaly cancellation (P4)
    + cited LH content (P1, P2)
    + minimal RH completion existence (P3)
    + Q-labelling convention (P5)
```

is independent of `HYPERCHARGE_IDENTIFICATION_NOTE.md`. ∎

## What this claims

- `(T1)` SM hypercharge values for u_R, d_R, e_R forced uniquely by
  anomaly cancellation on the no-ν_R RH completion.
- `(T2)` Counterfactual: adding ν_R with free y_4 reopens a
  1-parameter family; neutrality y_4=0 IS needed for uniqueness only
  if ν_R is included.
- `(T3)` Decoupling: parent's hypercharge uniqueness chain is
  independent of `HYPERCHARGE_IDENTIFICATION_NOTE`.

## What this does NOT claim

- Does NOT claim ν_R is forbidden by the framework. ν_R is optional;
  if included, it requires `y_4 = 0` for uniqueness.
- Does NOT close the separate `HYPERCHARGE_IDENTIFICATION_NOTE`
  normalization/readout task.
- Does NOT derive the LH content (Q_L, L_L) — cited from upstream.
- Does NOT derive the existence of the RH-singlet completion — cited
  from `ANOMALY_FORCES_TIME_THEOREM` Step 2.
- Does NOT derive the ABJ anomaly cancellation requirement —
  admitted-context external (Adler 1969; Bell-Jackiw 1969).
- Does NOT promote any author-side tier; independent audit is required.

## Cited dependencies

- (P1) [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) —
  supplies Q_L:(2,3)_{+1/3}.
- (P2) [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) —
  supplies L_L:(2,1)_{-1}.
- (P3) [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) —
  supplies the anomaly-cancelling SU(2)-singlet RH completion premise.
- (P4) Adler 1969; Bell-Jackiw 1969 — admitted-context external
  ABJ anomaly cancellation requirement.
- (P5) Doubled-Y convention `Q = T_3 + Y/2` shared with parent
  hypercharge uniqueness note.

**Decoupled (not cited as a load-bearing input):**

- `HYPERCHARGE_IDENTIFICATION_NOTE.md`. Removed as a dependency by the
  no-ν_R variant.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (Adler 1969,
  Bell-Jackiw 1969 are admitted-context external mathematical
  authorities, role-labelled).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention beyond the
  doubled-Y convention shared with parent.
- No same-surface family arguments.
- **No load-bearing dependency on `HYPERCHARGE_IDENTIFICATION_NOTE`.**
  (Key value proposition.)

## Validation

Primary runner: [`scripts/frontier_sm_hypercharge_no_nu_r_derivation.py`](./../scripts/frontier_sm_hypercharge_no_nu_r_derivation.py)
verifies (PASS=22/0, exact rational arithmetic throughout):

1. Anomaly trace (E1) Tr[Y] on no-ν_R sector.
2. Anomaly trace (E2) Tr[SU(3)²Y] on no-ν_R sector.
3. Anomaly trace (E3) Tr[Y³] on no-ν_R sector.
4. Reduction (S1): y_3 = -2 from (A1) + (A2).
5. Reduction (S2): y_1³ + y_2³ = 56/27 from (A3) + (S1).
6. Reduction (S3): y_1 y_2 = -8/9 via the cubic-symmetric identity.
7. Quadratic solve: y_1, y_2 ∈ {4/3, -2/3} with discriminant 324 = 18²
   (perfect square ⇒ rational solutions).
8. Q(u_R) > 0 labelling fixes y_1 = +4/3.
9. Final SM values: (y_1, y_2, y_3) = (+4/3, -2/3, -2) in doubled-Y
   convention.
10. Counterfactual: with ν_R as 4th unknown, system has a 1-parameter
    family — three explicit (y_4 ≠ 0) examples that satisfy the
    anomaly conditions but give non-SM hypercharges.
11. Decoupling check: derivation Steps 1–5 use no `Y(ν_R)` value —
    explicit static check that no `y_4` symbol appears in the
    minimal-no-ν_R closed-form.
12. Independence verification: explicit verification that the parent
    note's `y_4=0` substitution gives the same (y_1, y_2, y_3)
    triple as our no-ν_R variant.
13. Electric-charge spectrum on no-ν_R SM matter: Q ∈ {±1/3, ±2/3, 0,
    ±1} with denominators in {1, 3} (same as parent).

## Cross-references

These are contextual references, not load-bearing dependencies for this row,
so they are intentionally not markdown links:

- `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24` —
  parent row whose load-bearing dependency on
  `HYPERCHARGE_IDENTIFICATION_NOTE` is decoupled by this derivation.
- `SU3_ANOMALY_FORCED_3BAR_COMPLETION_THEOREM_NOTE_2026-05-02` —
  related SU(3)^3 anomaly derivation for the right-handed quark sector.
- `HYPERCHARGE_IDENTIFICATION_NOTE` — separate normalization/readout
  authority that this derivation no longer depends on.
- Adler 1969, Bell-Jackiw 1969 — original ABJ anomaly cancellation.
