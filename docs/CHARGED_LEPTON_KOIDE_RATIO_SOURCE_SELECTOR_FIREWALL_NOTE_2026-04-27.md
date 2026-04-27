# Charged-Lepton Koide Ratio/Source Selector Firewall

**Date:** 2026-04-27  
**Status:** proposed_retained exact negative boundary / support firewall for
charged-lepton mass retirement

This is not retained charged-lepton mass closure.
**Primary runner:**
`scripts/frontier_charged_lepton_koide_ratio_source_selector_firewall.py`

## Purpose

This note audits the remaining ratio/source side of the charged-lepton mass
retirement workstream:

```text
Koide Q support + Brannen/selected-line phase support
  ?=> retained generation-selection primitive without PDG masses.
```

The answer is no on the current repo surface. The support stack is useful and
sharper than the old bounded mass pin, but it does not yet supply a retained
primitive that selects all of:

1. the physical source-free `Q` representative;
2. the physical selected-line Brannen endpoint/readout;
3. a non-observational charged-lepton generation or tau-scale label.

PDG charged-lepton masses are comparator-only in the runner.

## Inputs Audited

The runner reads the current support/no-go surfaces:

- `KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`
- `KOIDE_Q_OP_LOCALITY_C3_FIXED_SOURCE_SUPPORT_NOTE_2026-04-27.md`
- `KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md`
- `KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`
- `KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`
- `KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md`
- `KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO_NOTE_2026-04-24.md`
- `CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`
- `CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md`

It deliberately does not update publication matrices, lane registries, or
repo-wide authority surfaces.

## Result 1: `Q` Erases the Selected-Line Phase

On the Brannen square-root carrier,

```text
sqrt(m_k) = V0 (1 + c cos(delta + 2 pi k / 3)),   k = 0,1,2,
```

the exact `C3` trigonometric identities give

```text
sum_k sqrt(m_k) = 3 V0,
sum_k m_k = (3 V0^2 / 2)(2 + c^2),
Q = (c^2 + 2) / 6.
```

Therefore

```text
dQ/d(delta) = 0,
dQ/dV0 = 0,
Q = 2/3 <=> c^2 = 2.
```

This is support for the `Q` side, not a phase selector. Once `c^2=2` is
imposed or conditionally derived, there is still a positive continuum of
distinct selected-line phases with the same `Q = 2/3`.

## Result 2: Current `Q` Source Support Is Conditional

The OP-locality / `C3`-fixed source note gives a useful conditional route:

```text
strict onsite source + C3-fixed undeformed-source premise
  => J = s I
  => z = 0
  => Q = 2/3
```

But the load-bearing physical premise is still open:

```text
retained charged-lepton physical readout
  => undeformed scalar source must be strict onsite and C3-fixed.
```

Moreover, the premise is generation-symmetric. A `C3`-fixed onsite scalar
source is a common scalar background, not a tau/electron/muon selector.

## Result 3: Current Brannen Endpoint Support Is Conditional

The retained ABSS/APS arithmetic gives the closed value

```text
eta_APS = 2/9.
```

But the open selected-line endpoint coordinate still has a free transition:

```text
eta_APS = delta_open + tau,
tau = 2/9 - delta_open.
```

Thus setting the physical Brannen phase equal to the closed `eta_APS` value
requires the still-open selected-line boundary-source, based endpoint, and
Type-B rational-to-radian readout laws. The current note does not derive them.

## Result 4: Ratio Data Still Do Not Label the Tau Scale

At the Brannen phase `2/9`, cyclic relabelings of the three square-root
components keep `Q` and the unordered ratio vector fixed while moving which
slot is the largest component. The ratio package can describe a sorted
heavy/middle/light spectrum after a phase is supplied, but it does not by
itself attach the radiative scale support to the physical tau eigenvalue
without an additional non-observational generation or scale-selector law.

This is the same firewall exposed by the earlier scale-side artifacts:

- one-Higgs gauge selection leaves the charged-lepton Yukawa matrix free;
- the radiative `alpha_LM/(4pi)` scale is generation-blind and cannot be a
  standalone tau selector.

## Comparator Firewall

The runner prints a comparator-only check that the PDG charged-lepton masses
lie near the Koide relation. Those values are not used in any proof step. The
proof inputs are only:

- `C3` trigonometry;
- conditional Brannen-carrier amplitude algebra;
- conditional `C3`-fixed onsite-source algebra;
- ABSS/APS arithmetic;
- cyclic relabeling algebra;
- prior support/no-go closeout flags.

## What Lands

This artifact lands a narrow workstream movement:

1. `Q = 2/3` support and `delta = 2/9` support remain useful.
2. Their combination does not supply a retained generation-selection primitive.
3. The charged-lepton mass-retirement target remains open.
4. The next theorem target is no longer another value match. It is a physical
   source/endpoint/generation law.

## What Does Not Land

This note does not prove:

1. retained native `Q = 2/3` closure;
2. retained selected-line `delta = 2/9` radian closure;
3. a retained tau-generation selector;
4. absolute charged-lepton masses;
5. retirement of the 3-real PDG charged-lepton mass pin.

## Closeout Flags

```text
CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL=TRUE
KOIDE_Q_PLUS_BRANNEN_PHASE_GENERATION_SELECTOR=FALSE
PDG_MASSES_USED_AS_COMPARATORS_ONLY=TRUE
CHARGED_LEPTON_MASS_RETENTION=FALSE
RESIDUAL_Q=derive_physical_charged_lepton_source_selection_strict_onsite_C3_fixed
RESIDUAL_DELTA=derive_selected_line_boundary_source_based_endpoint_and_Type_B_radian_readout
RESIDUAL_GENERATION=derive_nonobservational_generation_label_or_tau_scale_selector
```

## Verification

Run:

```bash
python3 scripts/frontier_charged_lepton_koide_ratio_source_selector_firewall.py
```

Expected final line:

```text
TOTAL: PASS=35, FAIL=0
```
