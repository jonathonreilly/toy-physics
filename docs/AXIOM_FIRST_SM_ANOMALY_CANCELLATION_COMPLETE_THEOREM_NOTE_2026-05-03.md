# Axiom-First SM Anomaly Cancellation Complete on Cl(3)/Z³ Left-Handed Surface

**Date:** 2026-05-03
**Type:** positive_theorem
**Claim type:** synthesis-aggregator anomaly-cancellation theorem (assembles four exact gauge-anomaly trace identities plus the nonperturbative SU(2) Witten Z_2 parity into a single closure statement on the retained Cl(3)/Z³ left-handed-frame matter content)
**Claim scope:** the four perturbative gauge-anomaly traces `(SU(3)^3, SU(2)^2 U(1)_Y, grav^2 U(1)_Y, U(1)_Y^3)` and the nonperturbative `SU(2)` Witten Z_2 parity all vanish exactly on the retained Cl(3)/Z³ left-handed-frame Standard-Model fermion content with the retained `N_c = 3` graph-first colour, retained native `SU(2)_L` gauge structure, retained three-generation structure, retained left-handed `Q_L`, `L_L` content, and retained one-generation right-handed completion (`u_R`, `d_R`, `e_R`, `nu_R`). All five cancellations are exact-Fraction or integer-parity statements; none uses an observed mass, mixing angle, or cross-section.
**Status:** awaiting independent audit. Under the scope-aware classification framework, ratified status is computed by the audit pipeline from audit-lane data; no author-side retained tier is asserted in source.
**Loop:** `anomaly-cancellation-full-closure-2026-05-03`
**Cycle:** 1 (Block 01)
**Branch:** `claude/anomaly-cancellation-full-closure-iter1-2026-05-03`
**Primary runner:** `scripts/axiom_first_sm_anomaly_cancellation_complete_check.py`

## 0. Synthesis Statement

**Theorem (SM anomaly cancellation complete on Cl(3)/Z³ LH-frame surface).**
On the retained Cl(3)/Z³ left-handed-frame Standard-Model fermion content (one
generation replicated three times),

| Field | `SU(3)` | `SU(2)` | colour | weak | LH count | `Y` |
|---|---:|---:|---:|---:|---:|---:|
| `Q_L`     | `3`    | `2` | `3` | `2` | `6` | `+1/3` |
| `L_L`     | `1`    | `2` | `1` | `2` | `2` | `-1`  |
| `u_R^c`   | `3bar` | `1` | `3` | `1` | `3` | `-4/3`|
| `d_R^c`   | `3bar` | `1` | `3` | `1` | `3` | `+2/3`|
| `e_R^c`   | `1`    | `1` | `1` | `1` | `1` | `+2`  |
| `nu_R^c`  | `1`    | `1` | `1` | `1` | `1` | `0`   |

with the doubled-hypercharge convention `Q = T_3 + Y/2`, every gauge-anomaly
constraint required for a quantum-consistent gauge theory cancels:

```text
  (A1)  Tr[SU(3)^3]                     = 0          (cubic colour anomaly)
  (A2)  Tr[SU(2)^2 U(1)_Y]              = 0          (mixed weak^2-hypercharge)
  (A3)  Tr[grav^2 U(1)_Y]   ≡ Tr[Y]     = 0          (gravitational^2 hypercharge)
  (A4)  Tr[U(1)_Y^3]                    = 0          (cubic hypercharge)
  (A5)  N_D(SU(2) Witten Z_2) mod 2     = 0          (nonperturbative SU(2) parity)
```

Each cancellation is an exact rational/integer statement; (A1)–(A4) are
exact `Fraction` equalities and (A5) is an integer parity equality.

The pure `SU(2)^3` cubic gauge anomaly vanishes group-theoretically because
the symmetric `d^{abc}` tensor for `SU(2)` is identically zero; this is not a
matter-content condition and is included for completeness as `(A0)`.

## 1. Retained inputs

| Ingredient | Authority |
|---|---|
| Cl(3)/Z³ native cubic SU(2) gauge structure | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) |
| Graph-first SU(3) integration with `N_c = 3` colour count | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |
| Three-generation observable structure | [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md), [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) |
| Retained left-handed `Q_L`, `L_L` content with `Y(Q_L) = +1/3`, `Y(L_L) = -1` | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md) |
| Retained one-generation RH completion `(u_R, d_R, e_R, nu_R)` | [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) |
| Retained RH hypercharges `(+4/3, -2/3, -2, 0)` | [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) |
| Standard ABJ trace formulae and Dynkin indices `T(3) = T(2) = 1/2` | textbook QFT input |
| Witten (1982) homotopy fact `pi_4(SU(2)) = Z_2` | textbook nonperturbative-anomaly input |
| Standard SU(3) cubic anomaly indices `A(3) = +1, A(3bar) = -1` | textbook Lie-algebra input |

The three load-bearing **previously-existing source theorems** providing the
component cancellations are:

1. [`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`](SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md)
   — cancels `(A1)` exactly on retained `Q_L + u_R^c + d_R^c`.
2. [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
   — supplies the LH-only trace values that appear as the rational
   right-hand-side targets of the RH-side cancellation equations for `(A2)`,
   `(A3)`, `(A4)`.
3. [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
   — cancels `(A5)` parity-exactly on retained three-generation content.

The full perturbative `(A2)+(A3)+(A4)` closure on the LH+RH content with the
SM RH hypercharges is independently packaged in:

4. [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
   — solves the RH hypercharge system from anomaly cancellation, with the
   resulting `(y_1, y_2, y_3, y_4) = (+4/3, -2/3, -2, 0)`.

5. [`RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md`](RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md)
   — explicit Fraction-equality verification of `(A2)`, `(A3)`, `(A4)` over
   the full LH+RH content using the SM RH hypercharges.

The synthesis here cites these as load-bearing inputs and verifies that the
five anomaly-closure statements `(A1)–(A5)` are simultaneously consistent on
**one** matter-content surface (the retained Cl(3)/Z³ LH-frame SM
one-generation content × n_gen = 3).

No observed mass, charge, mixing angle, cross-section, or proton-decay datum
enters the synthesis. All arithmetic uses standard-library `fractions.Fraction`.

## 2. Proof On The Retained Cl(3)/Z³ LH-Frame Surface

### 2.1 (A1) SU(3)^3 cubic gauge anomaly

Only `Q_L`, `u_R^c`, `d_R^c` are SU(3)-charged. Working in the LH-conjugate
frame so that all chirality signs are absorbed into the LH/anti-fundamental
labelling,

```text
A_SU3^3
  = (Q_L weak mult) * A(3) + (u_R^c)*A(3bar) + (d_R^c)*A(3bar)
  = 2 * (+1) + 1 * (-1) + 1 * (-1)
  = +2 - 1 - 1
  = 0.
```

This is the result of [`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`](SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md);
it relies on retained `N_c = 3` colour count and on the retained right-handed
colour-anti-triplet completion `u_R^c, d_R^c`.

### 2.2 (A2) Mixed SU(2)^2 × U(1)_Y anomaly

Only `Q_L` and `L_L` are SU(2) doublets. With `T(2) = 1/2`,

```text
A_SU2^2*Y
  = T(2) * sum over SU(2) doublets of (colour mult * Y of doublet)
  = (1/2) * [3 * (+1/3) + 1 * (-1)]
  = (1/2) * (1 - 1)
  = 0.
```

This is the LH-only `(C4)` value from [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md);
since RH fields are SU(2) singlets and contribute zero to `A_SU2^2*Y`, the
LH-only cancellation immediately closes the trace on the full LH+RH content.

### 2.3 (A3) Gravitational² × U(1)_Y anomaly ≡ Tr[Y] = 0

The `grav^2 U(1)_Y` anomaly reduces to the linear hypercharge sum:

```text
Tr[Y]_one-gen
  = 6 * (+1/3) + 2 * (-1)            # LH side: Q_L (3 col x 2 weak) + L_L (1 x 2)
  + 3 * (-4/3) + 3 * (+2/3) + 1 * (+2) + 1 * (0)   # RH side: u_R^c, d_R^c, e_R^c, nu_R^c
  = 2 - 2 - 4 + 2 + 2 + 0
  = 0.
```

Equivalently in the LH+RH form used by [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md):

```text
LH side: Tr[Y]_LH = 0  (from LH_ANOMALY_TRACE_CATALOG (C1))
RH side: 3 (y_1 + y_2) + y_3 + y_4 = 3 (4/3 - 2/3) + (-2) + 0
         = 3 * 2/3 - 2 = 2 - 2 = 0.
Total:   Tr[Y] = Tr[Y]_LH + Tr[Y]_RH = 0 + 0 = 0.
```

(In the LH-conjugate frame both sides combine with chirality signs absorbed
into the conjugate hypercharges of the RH content, e.g. `Y(u_R^c) = -4/3`.)

### 2.4 (A4) Cubic U(1)_Y³ anomaly

```text
Tr[Y^3]_one-gen
  = 6 (1/3)^3 + 2 (-1)^3              # LH:  6*(1/27) + 2*(-1) = 2/9 - 2 = -16/9
  + 3 (-4/3)^3 + 3 (2/3)^3 + 1 (2)^3 + 1 (0)^3   # RH (in LH-conjugate frame)
  = -16/9 + 3*(-64/27) + 3*(8/27) + 8 + 0
  = -16/9 - 192/27 + 24/27 + 8
  = -16/9 + (-168/27) + 8
  = -16/9 - 56/9 + 72/9
  = (-16 - 56 + 72)/9
  = 0/9
  = 0.
```

Equivalently:

```text
LH side: Tr[Y^3]_LH = -16/9  (from LH_ANOMALY_TRACE_CATALOG (C2))
RH side: 3(y_1^3 + y_2^3) + y_3^3 + y_4^3
       = 3((4/3)^3 + (-2/3)^3) + (-2)^3 + 0
       = 3*(64/27 - 8/27) + (-8)
       = 3 * 56/27 - 8
       = 168/27 - 216/27
       = -48/27
       = -16/9.
Total:   Tr[Y^3] = -16/9 + 16/9 = 0.
```

This matches both the (C2) LH-only catalog value and the RH-side solve in
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md).

### 2.5 (A5) SU(2) Witten Z_2 nonperturbative parity

Witten's `pi_4(SU(2)) = Z_2` global anomaly counts SU(2) Weyl doublets:

```text
N_D(per generation) = N_c (Q_L colour copies) + 1 (L_L)
                    = 3 + 1 = 4.
N_D(three generations) = n_gen * 4 = 3 * 4 = 12.
N_D(total) mod 2 = 0.
```

This is the result of [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md);
it depends on the retained `N_c = 3` colour count and the retained
three-generation structure.

### 2.6 (A0) Pure SU(2)^3 cubic gauge anomaly

The symmetric `d^{abc}` tensor for SU(2) vanishes identically (no rank-3
symmetric invariant exists for SU(2) acting on a fundamental representation;
equivalently, all SU(2) representations are real or pseudoreal so the cubic
trace `Tr[T^a {T^b, T^c}]` vanishes group-theoretically). Hence:

```text
A_SU2^3 = 0  identically,
```

regardless of matter content. This is recorded for completeness, not as a
matter-content cancellation.

### 2.7 Closure on the synthesis surface

The five cancellations `(A1)–(A5)` plus the group-theoretic `(A0)` exhaust
the gauge-anomaly conditions for a quantum-consistent
`SU(3) × SU(2) × U(1)_Y` gauge theory coupled to gravity:

| Anomaly slot | Conditional on | Value | Cancels |
|---|---|---|---|
| `(A0)` SU(2)^3 | group theory | `0` identically | yes (group-theoretic) |
| `(A1)` SU(3)^3 | `Q_L + u_R^c + d_R^c` content | `+2 - 1 - 1 = 0` exact | yes (matter-content) |
| `(A2)` SU(2)^2 Y | LH-doublet trace-free | `(1/2)(1-1) = 0` exact | yes (LH only) |
| `(A3)` grav^2 Y | LH+RH `Y` sum | `0` exact | yes (LH+RH) |
| `(A4)` Y^3 | LH+RH `Y^3` sum | `-16/9 + 16/9 = 0` exact | yes (LH+RH) |
| `(A5)` SU(2) Witten Z_2 | LH-doublet parity | `N_D mod 2 = 0` integer | yes (parity) |

All six slots simultaneously hold on **one and the same** retained Cl(3)/Z³
LH-frame matter content. This is the synthesis statement.

## 3. What This Synthesis Does Not Claim

This synthesis does **not** claim:

- **a native-axiom derivation of the LH content itself** (`Q_L`, `L_L` and
  their `+1/3`, `-1` hypercharges) — that is upstream input from
  [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) and
  [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md);
- **a native-axiom derivation of `N_c = 3`** — that is upstream input from
  the graph-first SU(3) integration;
- **a native-axiom derivation of the three-generation count** — upstream
  input from the three-generation observable / structure notes;
- **a native-axiom derivation of the standard ABJ trace formula or
  Dynkin-index normalization** — admitted-context QFT input;
- **a native-axiom derivation of Witten's `pi_4(SU(2)) = Z_2`** —
  admitted-context topology input;
- **a derivation of the absolute U(1)_Y normalization** — that is
  convention-fixed by the lepton-doublet `-1` normalization upstream;
- **a uniqueness-of-completion statement** — vectorlike or B-L-extended
  matter content can also pass these tests, as recorded in the individual
  scope sections of each component theorem.

The synthesis is a **closure aggregator**: given retained inputs, all five
anomaly conditions cancel simultaneously on one surface. It does not promote
the Cl(3)/Z³ LH-content surface to retained on its own.

## 4. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/axiom_first_sm_anomaly_cancellation_complete_check.py
```

Expected result:

```text
TOTAL: PASS=N FAIL=0
```

The runner verifies, classified by anomaly slot:

- `(A0)` SU(2)^3 cubic identically zero by group theory;
- `(A1)` SU(3)^3 cubic = `+2 - 1 - 1 = 0` exact Fraction equality on the
  retained content; nonzero `d^{abc}` for SU(3);
- `(A2)` SU(2)^2 Y = `(1/2)(3*(1/3) + 1*(-1)) = 0` exact LH-only;
- `(A3)` grav^2 Y ≡ Tr[Y]_one-gen = `2 - 2 - 4 + 2 + 2 + 0 = 0` exact LH+RH;
- `(A4)` Y^3 = `-16/9 + 16/9 = 0` exact LH+RH;
- `(A5)` SU(2) Witten N_D = `12`, `mod 2 = 0`.

The runner uses the Python standard library only and operates entirely on
exact `fractions.Fraction` arithmetic.

## 5. Cross-references

- [`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`](SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md)
  — load-bearing input theorem for `(A1)`.
- [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
  — load-bearing input catalog for `(A2)`, `(A3)`, `(A4)` LH-side traces.
- [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
  — load-bearing input theorem for `(A5)`.
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  — companion solving the RH hypercharges from `(A2)`, `(A3)`, `(A4)`.
- [`RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md`](RH_SECTOR_ANOMALY_CANCELLATION_IDENTITIES_NOTE_2026-05-02.md)
  — companion verifying `(A2)`, `(A3)`, `(A4)` over LH+RH at exact-Fraction
  precision.
- [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md)
  — companion `B-L` gaugeability theorem; orthogonal to this synthesis.
- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  — parent framework using these anomaly identities upstream.
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md)
  — retained native cubic SU(2) gauge structure on Cl(3)/Z³.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  — retained SU(3) integration with `N_c = 3`.
- [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
  — retained three-generation structure.
- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
  — retained one-generation completion.

## 6. Honest claim-status

```yaml
proposed_claim_type: positive_theorem
status_authority: independent audit lane only
audit_required_before_effective_retained: true
actual_current_surface_status: synthesis-aggregator anomaly-cancellation theorem assembling four exact gauge-anomaly trace identities plus the SU(2) Witten Z_2 parity into a single closure statement on the retained Cl(3)/Z³ LH-frame matter content
conditional_surface_status: full SM gauge-anomaly closure (A1)-(A5) holds simultaneously on one retained matter-content surface; conditional on retained-grade upstreams (NATIVE_GAUGE_CLOSURE, GRAPH_FIRST_SU3_INTEGRATION, three-generation structure, LEFT_HANDED_CHARGE_MATCHING, HYPERCHARGE_IDENTIFICATION, ONE_GENERATION_MATTER_CLOSURE, SM hypercharge uniqueness) and on the three component anomaly theorems (SU(3)^3, LH trace catalog, SU(2) Witten Z_2)
hypothetical_axiom_status: null
admitted_observation_status: "Standard ABJ anomaly-trace formulae, Dynkin-index normalization T(3) = T(2) = 1/2, standard SU(3) cubic anomaly indices A(3) = +1, A(3bar) = -1, Witten (1982) homotopy fact pi_4(SU(2)) = Z_2 admitted as universal QFT/topology input."
proposal_allowed: false
proposal_allowed_reason: "Source note records the synthesis closure theorem. Effective retained tier is set by the independent audit lane based on retained-grade upstream availability of the three component anomaly theorems (already audit-pending under their own status fields) plus the listed retained-grade gauge-structure and matter-content notes; not asserted by author."
bare_retained_allowed: false
```
