# Koide Q OP-Locality / C3-Fixed Source Support Note

**Date:** 2026-04-27
**Status:** conditional support note for the charged-lepton `Q` source-selection
lane; not retained Koide closure
**Primary runner:**
`scripts/frontier_koide_q_op_locality_c3_fixed_source_support.py`

## 1. Purpose

This note salvages the useful algebra from the `monday-koide` V7.3 branch
without promoting the open physical-source premise to retained theorem status.

The branch correctly isolates a sharp route:

```text
OP-local onsite source + C3-fixed undeformed physical source
  => J = s I on the three-generation orbit
  => equal (P_+, P_perp) channel source
  => reduced trace-zero source coordinate z = 0
  => Q = 2/3 on the admitted CRIT carrier.
```

The branch did **not** prove the load-bearing physical theorem:

```text
retained charged-lepton physical readout
  => undeformed scalar source must be strict onsite and C3-fixed.
```

That remains the live charged-lepton `Q` residual. This note therefore lands
only the conditional algebra and the sharpened open target.

## 2. Status boundary

This is a support note. It does not claim that `Q = 2/3` is retained.

The current retained/support surface remains:

- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` gives local scalar sources of the
  form `J = sum_x j_x P_x`.
- `THREE_GENERATION_STRUCTURE_NOTE.md` gives the retained three-generation
  matter structure.
- `KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md` proves
  the exact canonical descent from the projected `C3` commutant to strict
  onsite scalar functions, but labels itself support/criterion.
- `KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`
  proves the exact `z = 0 <=> Q = 2/3` criterion on the admitted carrier, but
  labels itself support/criterion.

The additional conditional premise used here is:

```text
P_SOURCE:
  the physical undeformed charged-lepton scalar source on the three-generation
  orbit is both strict-onsite and C3-fixed.
```

This note proves what follows from `P_SOURCE`; it does not prove `P_SOURCE`.

## 3. Local onsite source algebra

On the three-generation orbit, write the site-local projectors as

```text
P_1 = diag(1,0,0),  P_2 = diag(0,1,0),  P_3 = diag(0,0,1).
```

The OP-local scalar source form is

```text
J = j_1 P_1 + j_2 P_2 + j_3 P_3 = diag(j_1, j_2, j_3).
```

This gives the strict onsite source domain

```text
D = span_R{P_1, P_2, P_3}.
```

The cyclic generation action `C` sends `P_1 -> P_2 -> P_3 -> P_1`. The
conditional undeformed-source premise `P_SOURCE` imposes

```text
C J C^{-1} = J.
```

For onsite diagonal `J`, this is equivalent to

```text
j_1 = j_2 = j_3 =: s,
```

so the C3-fixed onsite source is

```text
J = s I,
D^C3 = span{I}.
```

This is the first useful output: if the physical undeformed source is required
to be onsite and C3-fixed, the only allowed source direction is the common
scalar/background direction.

## 4. Projection to the two isotype channels

Let

```text
P_+    = (I + C + C^2) / 3,
P_perp = I - P_+.
```

These are the trivial and two-dimensional nontrivial `C3` isotype projectors.
Project the scalar source `J = sI` into these two channels with the
trace-Frobenius inner product:

```text
K_+(J)    = Tr(J P_+) / Tr(P_+^2),
K_perp(J) = Tr(J P_perp) / Tr(P_perp^2).
```

Since

```text
Tr(P_+) = Tr(P_+^2) = 1,
Tr(P_perp) = Tr(P_perp^2) = 2,
```

we get

```text
K_+(sI)    = s,
K_perp(sI) = s.
```

Therefore the reduced two-block source is

```text
K(sI) = diag(s, s) = s I_2.
```

In the trace-zero parameterization

```text
K = s_par I_2 + z Z,       Z = diag(1,-1),
z = (K_+ - K_perp)/2,
```

the scalar source has

```text
z = 0.
```

So `P_SOURCE` implies reduced source `Z`-erasure.

## 5. Connection to existing criterion notes

The existing canonical descent support theorem gives the equivalent statement
from the projected commutant side. For a projected source

```text
K = s I + z Z,
```

the unique trace-preserving strict-onsite descent is

```text
E_loc(K) = (Tr K / 3) I = (s - z/3) I,
```

which kills the reduced trace-zero coordinate modulo the common scalar.

The existing background-zero / `Z`-erasure criterion theorem then gives, on
the admitted normalized reduced two-block carrier,

```text
z = 0  <=>  Y = I_2  <=>  Q = 2/3.
```

The salvage result is therefore:

```text
P_SOURCE  =>  z = 0  =>  Q = 2/3.
```

## 6. What this note lands

This note lands:

1. the exact C3-fixed onsite-source algebra `D^C3 = span{I}`;
2. the exact Frobenius projection of `J = sI` to equal `(P_+, P_perp)`
   source channels;
3. the exact conditional implication from a C3-fixed onsite undeformed source
   to reduced `z = 0`;
4. the precise remaining source-selection theorem needed to promote the
   support/criterion package.

## 7. What remains open

This note does **not** prove:

1. that the physical charged-lepton readout must use a strict onsite scalar
   source rather than a broader projected source grammar;
2. that the physical undeformed charged-lepton source must be C3-fixed;
3. that the admitted reduced two-block carrier is forced as the physical
   charged-lepton carrier;
4. retained native `Q = 2/3` closure;
5. retained `delta = 2/9` radian closure;
6. absolute charged-lepton masses.

Those remain active charged-lepton Koide / mass-retention lane targets.

## 8. Closeout flags

```text
KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT=TRUE
CONDITIONAL_C3_FIXED_ONSITE_SOURCE_IMPLIES_Z_ZERO=TRUE
CONDITIONAL_Z_ZERO_IMPLIES_Q_TWO_THIRDS=TRUE
CD_PHYSICAL_PREMISE_DERIVED_FROM_R1_PLUS_R2=FALSE
CRIT_PHYSICAL_PREMISE_DERIVED_FROM_R1_PLUS_R2=FALSE
KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE
KOIDE_DELTA_RETAINED_NATIVE_CLOSURE=FALSE
CHARGED_LEPTON_MASS_RETENTION=FALSE
RESIDUAL_Q=derive_physical_charged_lepton_source_selection_strict_onsite_C3_fixed
```

## 9. Reproduction

```bash
python3 scripts/frontier_koide_q_op_locality_c3_fixed_source_support.py
```

Expected final line:

```text
TOTAL: PASS=44 FAIL=0
```

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_q_source_domain_canonical_descent_theorem_note_2026-04-25](KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md)
- [koide_q_background_zero_z_erasure_criterion_theorem_note_2026-04-25](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md)
