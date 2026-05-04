# Neutrino Dirac / PMNS Retained Lane Packet (2026-04-16)

**Primary runner:** [`scripts/frontier_lepton_single_higgs_pmns_triviality.py`](../scripts/frontier_lepton_single_higgs_pmns_triviality.py) (PASS=32/0)

## Scope

This packet covers the retained Dirac / PMNS side of the neutrino lane on the
current `main` package.

## Exact Surviving Chain

- lower-level PMNS closure once the retained source/transfer pack is supplied:
  [PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md](./PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md)
- exact lower-level active source recovery and current-bank value-selection
  no-go:
  [PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md](./PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md),
  [PMNS_CURRENT_BANK_VALUE_SELECTION_NOGO_NOTE.md](./PMNS_CURRENT_BANK_VALUE_SELECTION_NOGO_NOTE.md)
- exact negative closure of the full single-Higgs lepton route:
  [LEPTON_SINGLE_HIGGS_PMNS_TRIVIALITY_NOTE.md](./LEPTON_SINGLE_HIGGS_PMNS_TRIVIALITY_NOTE.md)
- exact minimal surviving neutrino-side two-Higgs branch:
  [NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md](./NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md)
- exact native nontrivial-character current boundary and selector reduction
  stack:
  [PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md](./PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md),
  [PMNS_SECTOR_ORIENTATION_ORBIT_NOTE.md](./PMNS_SECTOR_ORIENTATION_ORBIT_NOTE.md),
  [PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md](./PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md),
  [PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md](./PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md),
  [PMNS_SELECTOR_SECTOR_ODD_REDUCTION_NOTE.md](./PMNS_SELECTOR_SECTOR_ODD_REDUCTION_NOTE.md),
  [PMNS_SELECTOR_NONUNIVERSAL_SUPPORT_REDUCTION_NOTE.md](./PMNS_SELECTOR_NONUNIVERSAL_SUPPORT_REDUCTION_NOTE.md),
  [PMNS_SELECTOR_CLASS_SPACE_UNIQUENESS_NOTE.md](./PMNS_SELECTOR_CLASS_SPACE_UNIQUENESS_NOTE.md),
  [PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md](./PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md),
  [PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md](./PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md),
  [PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md](./PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md),
  [PMNS_BRANCH_CONDITIONED_QUADRATIC_SHEET_CLOSURE_NOTE.md](./PMNS_BRANCH_CONDITIONED_QUADRATIC_SHEET_CLOSURE_NOTE.md),
  [PMNS_RIGHT_POLAR_SECTION_NOTE.md](./PMNS_RIGHT_POLAR_SECTION_NOTE.md)

## Current Exact Endpoint

On the retained sole-axiom bank:

- the lower-level downstream closure machinery is exact once the right
  source/transfer pack is supplied
- the sole axiom itself does not produce a positive retained PMNS realization
- the exact missing PMNS object is one complex native nontrivial-character
  current `J_chi`
- the current retained sole-axiom, source-transfer, and scalar routes all set
  `J_chi = 0`

So the current live status is:

- positive downstream closure machinery
- negative sole-axiom closeout
- exact selector and branch-reduction toolkit on the surviving one-sided
  surface

## What Is Closed

- the single-Higgs lepton PMNS route is closed negatively
- the minimal surviving neutrino-side two-Higgs branch is reduced to one
  canonical seven-real class
- the one-sided selector problem is reduced to one unique reduced class with
  one real amplitude slot `a_sel`
- the current retained bank sets `a_sel,current = 0`
- any future nonzero sign of `a_sel` hands off directly to the
  branch-conditioned coefficient problem

## What Is Not Claimed

- no positive PMNS value-selection law on the retained bank
- no positive sole-axiom PMNS closure
- no flagship neutrino promotion

## Representative Runners

- [frontier_lepton_single_higgs_pmns_triviality.py](../scripts/frontier_lepton_single_higgs_pmns_triviality.py)
- [frontier_neutrino_dirac_two_higgs_canonical_reduction.py](../scripts/frontier_neutrino_dirac_two_higgs_canonical_reduction.py)
- [frontier_pmns_c3_nontrivial_current_boundary.py](../scripts/frontier_pmns_c3_nontrivial_current_boundary.py)
- [frontier_pmns_selector_current_stack_zero_law.py](../scripts/frontier_pmns_selector_current_stack_zero_law.py)
- [frontier_pmns_branch_conditioned_quadratic_sheet_closure.py](../scripts/frontier_pmns_branch_conditioned_quadratic_sheet_closure.py)
- [frontier_pmns_right_polar_section.py](../scripts/frontier_pmns_right_polar_section.py)
