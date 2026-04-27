# Charged-Lepton OP-Local Source / Selected-Line Selector No-Go

**Date:** 2026-04-27
**Status:** exact negative boundary for charged-lepton mass retirement; not
retained charged-lepton mass closure
**Primary runner:**
`scripts/frontier_charged_lepton_op_local_source_selected_line_selector_no_go.py`

## Purpose

This note audits the remaining ratio/source side under the strongest new
non-PDG premise currently available on this branch:

```text
P_SOURCE:
  the undeformed charged-lepton scalar source is strict-onsite and C3-fixed.
```

The OP-locality support note proves the conditional chain

```text
P_SOURCE => J = s I => z = 0 => Q = 2/3.
```

This cycle grants that conditional `Q` support and also grants the current
selected-line/Brannen phase support value. The question tested here is narrower:

```text
OP-local C3-fixed Q source support
  + selected-line/Brannen phase support
  ?=> retained physical generation selector without PDG masses.
```

The answer is no. The `P_SOURCE` premise erases the `Q` source coordinate, but
it is generation-symmetric. It does not base the selected-line orbit and does
not attach the heavy/middle/light ratio profile to the physical `e`, `mu`,
`tau` generation labels.

## Inputs Audited

The runner reads the current support/no-go surfaces:

- `CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md`
- `CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md`
- `KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md`
- `KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`
- `KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md`
- `KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`
- `KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md`
- `KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`
- `KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md`
- `KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md`
- `CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md`

PDG charged-lepton masses are used only in a comparator block.

## Result 1: The Granted Source Premise Is C3-Trivial

On the three-generation orbit, a strict-onsite scalar source has the form

```text
J = diag(j_1, j_2, j_3).
```

The `C3`-fixed condition forces

```text
j_1 = j_2 = j_3,
```

so the source is a common scalar:

```text
J = s I.
```

Projection to the two `C3` isotype channels gives equal coefficients

```text
K_+ = K_perp = s,
```

hence the reduced trace-zero coordinate is

```text
z = (K_+ - K_perp) / 2 = 0.
```

On the admitted criterion carrier this gives

```text
Q(z=0) = 2/3.
```

This is real conditional support for the `Q` side. It is not a generation
selector, because `J = sI` is invariant under every cyclic relabeling and
carries no distinguished generation slot.

## Result 2: The Selected-Line Orbit Remains Unbased

Grant the current selected-line support data:

```text
sqrt(m_k) = V0 (1 + sqrt(2) cos(delta + 2 pi k / 3)),
delta = 2/9.
```

Cyclic relabelings preserve `Q = 2/3` and preserve the unordered
heavy/middle/light ratio profile, but they move the heaviest slot through all
three labels. The C3-fixed source premise does not change this, since the
source is the same scalar after every relabeling.

Therefore the combined data determine at most an unbased ratio orbit. They do
not identify which physical charged-lepton generation/source slot should carry
the tau-scale support.

## Result 3: No C3-Natural Single-Label Selector Exists

A selector from unbased quotient data to one generation label would have to
return a label fixed by the `C3` action. But the `C3` action on the three
generation labels is free:

```text
0 -> 1 -> 2 -> 0.
```

No single label is fixed. The only nonempty invariant subset is the full
generation orbit `{0, 1, 2}`.

Based equivariant selectors do exist, but there are three of them, one for each
choice of basepoint. Choosing one basepoint is exactly the missing physical
endpoint/source/generation law. It is not supplied by `Q`, by `delta = 2/9`, by
the C3-fixed source premise, or by the radiative scale support.

## Comparator Firewall

The runner prints a comparator-only PDG Koide check. The proof inputs are only:

- `C3` fixed onsite-source algebra;
- the `z = 0` source-erasure criterion;
- Brannen carrier support at `c^2 = 2`;
- selected-line phase support `delta = 2/9`;
- the free `C3` action on generation labels;
- prior support/no-go closeout flags.

The runner does not use observed charged-lepton masses, the observed tau label,
or a PDG hierarchy selector as derivation input.

## What Lands

This artifact lands a narrow workstream movement:

1. Granting `P_SOURCE => Q = 2/3` still does not produce a retained
   generation-selection primitive.
2. The remaining selected-line obstruction is basedness, not another numerical
   `Q` or `delta` calculation.
3. The charged-lepton mass-retirement target remains open.

## What Does Not Land

This note does not prove:

1. retained native `Q = 2/3` closure;
2. retained selected-line `delta = 2/9` radian closure;
3. a retained tau-generation selector;
4. absolute charged-lepton masses;
5. retirement of the 3-real PDG charged-lepton mass pin.

It also does not kill future based endpoint/source/generation laws. It only
blocks the promotion of the current OP-local source support plus the current
selected-line support into a retained generation selector.

## Closeout Flags

```text
CHARGED_LEPTON_OP_LOCAL_SOURCE_SELECTED_LINE_SELECTOR_NO_GO=TRUE
OP_LOCAL_SOURCE_PLUS_SELECTED_LINE_SELECTS_GENERATION=FALSE
BASED_ENDPOINT_SOURCE_OR_TAU_SCALE_SELECTOR_REQUIRED=TRUE
PDG_MASSES_USED_AS_COMPARATORS_ONLY=TRUE
CHARGED_LEPTON_MASS_RETENTION=FALSE
RESIDUAL_Q=derive_physical_charged_lepton_source_selection_strict_onsite_C3_fixed
RESIDUAL_DELTA=derive_based_selected_line_endpoint_and_Type_B_radian_readout
RESIDUAL_GENERATION=derive_based_endpoint_source_or_tau_scale_selector
```

## Verification

Run:

```bash
python3 scripts/frontier_charged_lepton_op_local_source_selected_line_selector_no_go.py
```

Expected final line:

```text
TOTAL: PASS=48, FAIL=0
```
