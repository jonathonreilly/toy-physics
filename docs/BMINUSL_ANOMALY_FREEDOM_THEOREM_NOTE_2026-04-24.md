# B-L Anomaly-Freedom Theorem With Retained nu_R

**Date:** 2026-04-24
**Type:** positive_theorem
**Claim scope:** the exact rational arithmetic of all six anomaly traces
`(G1)-(G6)` for `U(1)_{B-L}` on the retained one-generation matter
content, evaluated via standard SM `B`/`L` charge assignments. The
**gaugeability conclusion** ("`U(1)_{B-L}` is gauge-anomaly-consistent on
the retained content") follows from the arithmetic plus the standard
quantum-consistency criterion. The **upstream supply** of the
one-generation matter content (including `nu_R`), the doubled-hypercharge
convention, the anomaly-cancellation-as-quantum-consistency principle,
and the standard SM `B`/`L` bookkeeping are explicitly **out of scope**
here and live in separate authority notes (admitted-context to this
note).
**Status:** audit pending. Under the scope-aware classification framework,
`effective_status` is computed by the audit pipeline from `audit_status` +
`claim_type` + dependency chain; no author-side tier is asserted in source.
The current ledger state is `unaudited` and audit-lane ratification is
required before any retained-grade status applies.

**Primary runner:** `scripts/frontier_bminusl_anomaly_freedom.py`

---

## 1. Statement

On the retained one-generation matter surface including `nu_R`, write all
fermions as left-handed Weyl fields. Right-handed species are represented by
their charge-conjugate left-handed fields, so their abelian charges are
sign-flipped.

Using the doubled-hypercharge convention of the retained notes
`Q = T3 + Y/2`, the left-handed-frame content is:

| Field | `SU(3)` | `SU(2)` | multiplicity | `Y` | `B-L` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `Q_L` | `3` | `2` | `6` | `1/3` | `1/3` |
| `L_L` | `1` | `2` | `2` | `-1` | `-1` |
| `u_R^c` | `3bar` | `1` | `3` | `-4/3` | `-1/3` |
| `d_R^c` | `3bar` | `1` | `3` | `2/3` | `-1/3` |
| `e_R^c` | `1` | `1` | `1` | `2` | `1` |
| `nu_R^c` | `1` | `1` | `1` | `0` | `1` |

Then the complete anomaly set for gauging `U(1)_{B-L}` on the retained
`SU(3) x SU(2) x U(1)_Y` matter content vanishes exactly:

```text
(G1)  grav^2 U(1)_{B-L}              Tr[B-L]          = 0
(G2)  U(1)_{B-L}^3                   Tr[(B-L)^3]      = 0
(G3)  SU(3)^2 U(1)_{B-L}                                = 0
(G4)  SU(2)^2 U(1)_{B-L}                                = 0
(G5)  U(1)_Y^2 U(1)_{B-L}            Tr[Y^2(B-L)]     = 0
(G6)  U(1)_Y U(1)_{B-L}^2            Tr[Y(B-L)^2]     = 0
```

The `nu_R^c` field is load-bearing for (G1) and (G2). Removing it changes both
traces from `0` to `-1`. It is inert for (G3)-(G6), because it is an
`SU(3) x SU(2)` singlet and has `Y = 0`.

## 2. Retained Inputs

| Ingredient | Authority |
| --- | --- |
| One-generation matter content including `nu_R` | [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) |
| Hypercharge convention and retained singlet `Y(nu_R)=0` | [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) |
| Anomaly-cancellation as a quantum-consistency condition | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) |
| `B` and `L` bookkeeping charges | standard SM baryon/lepton-number assignment |

No observed mass, mixing angle, proton-decay datum, `nu_R` mass, or Majorana
phase is used.

## 3. Exact Anomaly Arithmetic

### 3.1 Linear and Cubic B-L Traces

In the left-handed frame,

```text
Tr[B-L]
  = 6(1/3) + 2(-1) + 3(-1/3) + 3(-1/3) + 1 + 1
  = 2 - 2 - 1 - 1 + 1 + 1
  = 0.
```

The cubic trace is

```text
Tr[(B-L)^3]
  = 6(1/3)^3 + 2(-1)^3 + 3(-1/3)^3 + 3(-1/3)^3 + 1^3 + 1^3
  = 2/9 - 2 - 1/9 - 1/9 + 1 + 1
  = 0.
```

Without `nu_R^c`, both traces are `-1`. Thus the retained neutral singlet is
not cosmetic for B-L: it closes both the gravitational and cubic abelian
anomalies.

### 3.2 Nonabelian Mixed Traces

For `SU(3)^2 U(1)_{B-L}`, the common Dynkin index is irrelevant to
cancellation:

```text
2(1/3) + (-1/3) + (-1/3) = 0.
```

For `SU(2)^2 U(1)_{B-L}`,

```text
3(1/3) + (-1) = 0.
```

The `nu_R` slot does not enter either trace.

### 3.3 Mixed Abelian Traces

The two mixed abelian traces must also vanish if `B-L` is gauged while the
retained hypercharge gauge factor remains present.

For `U(1)_Y^2 U(1)_{B-L}`:

```text
Tr[Y^2(B-L)]
  = 6(1/3)^2(1/3) + 2(-1)^2(-1)
    + 3(-4/3)^2(-1/3) + 3(2/3)^2(-1/3) + (2)^2(1) + 0
  = 2/9 - 2 - 16/9 - 4/9 + 4
  = 0.
```

For `U(1)_Y U(1)_{B-L}^2`:

```text
Tr[Y(B-L)^2]
  = 6(1/3)(1/3)^2 + 2(-1)(-1)^2
    + 3(-4/3)(-1/3)^2 + 3(2/3)(-1/3)^2 + 2(1)^2 + 0
  = 2/9 - 2 - 4/9 + 2/9 + 2
  = 0.
```

Again `nu_R^c` is inert here because `Y(nu_R^c)=0`.

## 4. Consequences

- `U(1)_{B-L}` is anomaly-consistent and gaugeable on the retained
  one-generation content without adding fermions.
- This does not mean the retained framework gauges `B-L`; it only says the
  extension is quantum-consistent on the retained matter spectrum.
- The retained `nu_R` slot has two independent structural witnesses:
  the neutral-singlet slot in the hypercharge uniqueness theorem and the
  load-bearing `B-L` contribution to (G1) and (G2).
- The proton-lifetime companion may cite B-L anomaly freedom through the new
  six-trace theorem rather than through the older linear-only check.

## 5. Scope Boundary

This theorem claims:

- exact cancellation of (G1)-(G6) using rational arithmetic;
- gaugeability of `U(1)_{B-L}` on the retained content;
- `nu_R` load-bearing status for the linear and cubic B-L traces.

This theorem does not claim:

- that `U(1)_{B-L}` is part of the retained gauge group;
- a `Z'_{B-L}` mass, coupling, kinetic-mixing law, or breaking scale;
- a Majorana mass or Majorana phase for `nu_R`;
- a derivation of baryon number, lepton number, or `B-L` from the minimal
  `Cl(3)/Z^3` axiom;
- exact physical B-L conservation after adding explicit B-L-breaking dynamics.

## 6. Proton-Decay and Falsifiability Posture

The theorem itself is an internal anomaly-arithmetic theorem. It is not a
new proton-lifetime prediction.

For the proton-lifetime companion, the relevant bookkeeping is:

```text
p -> e+ pi0:  initial B-L = 1, final B-L = 1, so Delta(B-L)=0.
p -> e- pi+:  initial B-L = 1, final B-L = -1, so Delta(B-L)=-2.
```

Thus B-L-preserving proton-decay channels are compatible with the retained
companion story, while B-L-violating channels would falsify any promoted
gauged-B-L or exact-B-L-conservation extension. They would not falsify the
mathematical anomaly-cancellation identity by themselves.

## 7. Reproduction

```bash
python3 scripts/frontier_bminusl_anomaly_freedom.py
```

Expected result:

```text
TOTAL: PASS=36, FAIL=0
```

The runner uses `fractions.Fraction` throughout, so all anomaly equalities are
exact rational identities rather than floating-point comparisons.

## 8. Out of scope (admitted-context to this note)

The following items are explicitly **NOT** load-bearing claims of this
note. They depend on separate authority rows and enter only as
admitted-context:

1. **One-generation matter content** including `nu_R`. Supplied by
   [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md).
   This note does not derive the matter content; it consumes the
   spectrum as an input.

2. **Hypercharge convention and `Y(nu_R) = 0`.** Supplied by
   [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md).
   The doubled-hypercharge convention `Q = T_3 + Y/2` is admitted-context.

3. **Anomaly-cancellation-as-quantum-consistency principle.** Supplied by
   [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md).
   The general principle that gauge-anomaly traces must vanish for the
   gauged group is admitted external authority.

4. **Standard SM `B` and `L` bookkeeping.** Quark `B = 1/3`, lepton
   `L = 1` is the standard SM assignment, admitted as conventional
   bookkeeping. This note does not derive `B` and `L` from any
   underlying axiom.

The **in-scope content** of this note is the exact rational anomaly
arithmetic itself: the six trace evaluations `Tr[B-L]`, `Tr[(B-L)^3]`,
`Tr[F_a^2 (B-L)]`, etc., conditional on the matter content and charge
conventions above. The gaugeability conclusion follows from the
arithmetic plus the admitted quantum-consistency principle.

## 9. Cross-References

- [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
- `PROTON_LIFETIME_DERIVED_NOTE.md`
