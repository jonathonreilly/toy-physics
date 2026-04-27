# Artifact Plan

## Cycle 1 Artifact

Create a retained-objective no-go theorem that blocks a false direct route:

```text
docs/CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md
scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py
```

**Status:** complete.

## Required Checks

The runner must check:

- hypercharge selection for `bar L_L H e_R`;
- rejection of `bar L_L tilde H e_R`;
- arbitrary diagonal and off-diagonal entries of `Y_e` remain gauge invariant;
- generation-basis rotations change entries while preserving gauge invariance;
- no scalar-singlet normalization on the charged-lepton monomial produces the
  top Ward factor `1/sqrt(6)`;
- observed/comparator values, if printed, are not used in any proof check.

## Safe Status

Actual status: exact negative boundary / retained-objective no-go.

The note must not claim charged-lepton mass closure. It should say the
retained objective remains open and is narrowed to an additional primitive:
a generation-selection/loop/source law beyond one-Higgs gauge selection and
direct top-Ward analogy.

## Verification

```text
python3 scripts/frontier_charged_lepton_direct_ward_free_yukawa_no_go.py
TOTAL: PASS=26, FAIL=0
```

## Cycle 2 Candidate

Audit whether `y_tau = alpha_LM/(4pi)` can be promoted from support-only to a
retained absolute-scale theorem. Required focus:

- loop diagram completeness;
- normalization of the `4pi` denominator;
- source of the tau-generation selector;
- firewall against using observed charged-lepton masses as hidden inputs.

**Status:** complete as a support firewall, not a promotion.

```text
docs/CHARGED_LEPTON_RADIATIVE_TAU_SELECTOR_FIREWALL_NOTE_2026-04-26.md
scripts/frontier_charged_lepton_radiative_tau_selector_firewall.py
```

Verification:

```text
python3 scripts/frontier_charged_lepton_radiative_tau_selector_firewall.py
TOTAL: PASS=17, FAIL=0
```

## Cycle 3 Candidate

Attack the remaining retained ratio/source problem:

- Koide `Q = 2/3` source-domain closure;
- Brannen/selected-line phase provenance;
- proof that the charged-lepton eigenvalue vector is selected without PDG
  masses;
- exact firewall against reusing killed `Z_3`-only, APBC-only, or
  universal-Koide routes.

**Status:** complete as a ratio/source selector firewall, not a promotion.

```text
docs/CHARGED_LEPTON_KOIDE_RATIO_SOURCE_SELECTOR_FIREWALL_NOTE_2026-04-27.md
scripts/frontier_charged_lepton_koide_ratio_source_selector_firewall.py
```

Verification:

```text
python3 scripts/frontier_charged_lepton_koide_ratio_source_selector_firewall.py
TOTAL: PASS=35, FAIL=0
```

Safe status: exact negative boundary / support firewall. The artifact closes
only the standalone-selector route:

```text
Koide Q support + Brannen/selected-line phase support
  does not imply retained generation/tau-scale selection.
```

## Cycle 4 Candidate

Only proceed if a genuinely new physical premise is named. Candidate targets:

- derive or refute the physical source law
  `strict-onsite + C3-fixed undeformed charged-lepton scalar source`;
- derive or refute a based selected-line endpoint/radian readout law;
- derive a non-observational generation/tau-scale label tying the ratio vector
  to the radiative scale support.

Do not produce another `Q = 2/3` or `delta = 2/9` value-match packet without a
new source, endpoint, or generation-selection premise.

**Status:** complete as a selected-line/generation-selector no-go, not a
promotion.

```text
docs/CHARGED_LEPTON_SELECTED_LINE_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md
scripts/frontier_charged_lepton_selected_line_generation_selector_no_go.py
```

Verification:

```text
python3 scripts/frontier_charged_lepton_selected_line_generation_selector_no_go.py
TOTAL: PASS=38, FAIL=0
```

Safe status: exact negative boundary. Granting the current non-PDG `Q` and
selected-line support values still leaves the physical generation selector
open because unbased free `C3` orbit data have no invariant single-label
selector.

## Cycle 5 Candidate

Audit the strongest named new ratio/source premise now available:

```text
OP-local strict-onsite + C3-fixed undeformed source
  => z=0
  => Q=2/3.
```

Combine that granted premise with the selected-line/Brannen phase support and
test whether it supplies a retained physical generation selector without PDG
charged-lepton masses.

**Status:** complete as an exact negative boundary, not a promotion.

```text
docs/CHARGED_LEPTON_OP_LOCAL_SOURCE_SELECTED_LINE_SELECTOR_NO_GO_NOTE_2026-04-27.md
scripts/frontier_charged_lepton_op_local_source_selected_line_selector_no_go.py
```

Verification:

```text
python3 scripts/frontier_charged_lepton_op_local_source_selected_line_selector_no_go.py
TOTAL: PASS=48, FAIL=0
```

Safe status: exact negative boundary. The OP-local source support erases the
`Q` source coordinate, but the source is a common scalar and does not base the
selected-line orbit or label the tau generation.

## Cycle 6 Candidate

Audit the strongest Brannen-side scalar premise left on the ratio/source side:

```text
P_RADIAN:
  Type-B rational 2/9 is physically read as delta = 2/9 rad.
```

Combine that granted premise with OP-local `z=0 => Q=2/3` support and test
whether scalar readout plus source support supplies a retained physical
generation selector without PDG charged-lepton masses.

**Status:** complete as an exact negative boundary, not a promotion.

```text
docs/CHARGED_LEPTON_TYPEB_RADIAN_READOUT_GENERATION_SELECTOR_NO_GO_NOTE_2026-04-27.md
scripts/frontier_charged_lepton_typeb_radian_readout_generation_selector_no_go.py
outputs/frontier_charged_lepton_typeb_radian_readout_generation_selector_no_go_2026-04-27.txt
```

Verification:

```text
python3 scripts/frontier_charged_lepton_typeb_radian_readout_generation_selector_no_go.py
TOTAL: PASS=43, FAIL=0
```

Safe status: exact negative boundary. A scalar Type-B-to-radian readout narrows
the unit problem but still does not choose a selected-line basepoint or label
the tau generation.
