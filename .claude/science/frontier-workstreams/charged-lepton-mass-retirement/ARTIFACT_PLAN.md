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
