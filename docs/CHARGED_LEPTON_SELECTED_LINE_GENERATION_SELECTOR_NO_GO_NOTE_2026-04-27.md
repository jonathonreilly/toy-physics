# Charged-Lepton Selected-Line Generation-Selector No-Go

**Date:** 2026-04-27  
**Status:** support / exact negative boundary for the selected-line/generation-label
side of charged-lepton mass retirement; not retained charged-lepton mass
closure  
**Primary runner:**
`scripts/frontier_charged_lepton_selected_line_generation_selector_no_go.py`

## Purpose

This note follows the ratio/source audit from
`CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md` and
isolates the sharpest remaining selected-line question:

```text
Koide Q support + selected-line/Brannen phase support
  ?=> retained physical generation or tau-scale label without PDG masses.
```

The answer is no on the current repo surface. The obstruction is not another
numerical mismatch. Even if the current support values are granted, unbased
`C3` orbit data cannot select one charged-lepton generation label in a
`C3`-natural way. A selector exists only after a based endpoint, source, or
generation-label law is supplied.

## Inputs Audited

The runner reads these current support/no-go surfaces:

- `CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md`
- `KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`
- `KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md`
- `KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`
- `KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`
- `KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md`
- `KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md`
- `CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md`

PDG charged-lepton masses are used only in a final comparator block.

## Result

Grant the non-PDG support data:

```text
sqrt(m_k) = V0 (1 + sqrt(2) cos(delta + 2 pi k / 3)),
delta = 2/9,
Q = 2/3.
```

Cyclic relabeling of the three components preserves `Q` and the unordered
ratio vector, but moves the largest slot through all three labels. Therefore
the support data determine at most a sorted heavy/middle/light ratio profile
on an unbased orbit. They do not identify which physical charged-lepton
generation/source slot carries the tau-scale support.

Formally, the quotient of a free `C3` orbit has one unbased point. A natural
single-label selector from that quotient to the label set `{0,1,2}` would need
to return a label fixed by all `C3` relabelings. The `C3` action on labels is
free, so no such label exists. The only nonempty invariant subset is the full
generation orbit `{0,1,2}`.

Based equivariant selectors do exist. There are three of them, corresponding
to the three possible choices of basepoint label. That is exactly the point:
the basepoint is additional physical data. It is not supplied by Koide `Q`,
the selected-line phase value, the current `C3`-fixed onsite-source support,
or the radiative `alpha_LM/(4pi)` scale support.

## Consequence

This lands a narrow no-go:

```text
unbased selected-line orbit data
  + current Koide Q support
  + current Brannen/selected-line phase support
  does not imply a retained physical generation selector.
```

The remaining theorem target is still one of:

1. a retained based selected-line endpoint/source law;
2. a retained Type-B rational-to-radian readout law with its physical
   basepoint;
3. a non-observational generation/tau-scale selector tying the ratio vector to
   the radiative scale support.

## What Does Not Land

This note does not prove:

1. retained native `Q = 2/3` closure;
2. retained selected-line `delta = 2/9` radian closure;
3. a retained tau-generation selector;
4. absolute charged-lepton masses;
5. retirement of the 3-real PDG charged-lepton mass pin.

It also does not kill future based-endpoint or source-law routes. It only
blocks the current unbased selected-line support data from being promoted into
a generation selector.

## Closeout Flags

```text
CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO=TRUE
UNBASED_C3_ORBIT_SELECTS_SINGLE_GENERATION_LABEL=FALSE
BASED_ENDPOINT_OR_SOURCE_LAW_REQUIRED=TRUE
PDG_MASSES_USED_AS_COMPARATORS_ONLY=TRUE
CHARGED_LEPTON_MASS_RETENTION=FALSE
RESIDUAL_SELECTED_LINE=derive_based_endpoint_or_source_law
RESIDUAL_GENERATION=derive_nonobservational_generation_label_or_tau_scale_selector
```

## Verification

Run:

```bash
python3 scripts/frontier_charged_lepton_selected_line_generation_selector_no_go.py
```

Expected final line:

```text
TOTAL: PASS=38, FAIL=0
```
