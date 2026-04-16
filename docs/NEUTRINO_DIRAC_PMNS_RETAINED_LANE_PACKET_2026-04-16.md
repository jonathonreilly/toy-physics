# Neutrino Dirac / PMNS Retained Lane Packet (2026-04-16)

## Scope
This packet covers the retained Dirac / PMNS lane on the fixed lepton-support
surface derived from the sole axiom `Cl(3)` on `Z^3`.

## Exact Surviving Chain
- Fixed supports `E_nu`, `E_e` and charge-sector Schur localization:
  [PMNS_LEPTON_CHARGE_SCHUR_LOCALIZATION_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_LEPTON_CHARGE_SCHUR_LOCALIZATION_NOTE.md)
- Full microscopic operator to PMNS-relevant pair:
  [PMNS_FULL_MICROSCOPIC_OPERATOR_TO_PAIR_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_FULL_MICROSCOPIC_OPERATOR_TO_PAIR_NOTE.md)
- Lower-level end-to-end closure once the microscopic pair is supplied:
  [PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md)
- Passive phase reduction:
  [PMNS_PASSIVE_MONOMIAL_PHASE_REDUCTION_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_PASSIVE_MONOMIAL_PHASE_REDUCTION_NOTE.md)
- PMNS-relevant microscopic `D` reduced first to a seven-real last mile:
  [PMNS_MICROSCOPIC_D_SEVEN_REAL_LAST_MILE_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_MICROSCOPIC_D_SEVEN_REAL_LAST_MILE_NOTE.md)
- Then reduced further to a four-real active orbit-breaking last mile:
  [PMNS_MICROSCOPIC_D_FOUR_REAL_LAST_MILE_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_MICROSCOPIC_D_FOUR_REAL_LAST_MILE_NOTE.md)

## Current Exact Endpoint
The retained Dirac / PMNS lane is not a generic matrix search anymore.

Already fixed natively:
- `tau`
- `q`
- `xbar`
- `sigma`
- the passive Hermitian moduli `(|a_1|, |a_2|, |a_3|)`

The only unreduced PMNS-relevant microscopic data left are:

`(xi_1, xi_2, rho_1, rho_2)`

These are the active orbit-breaking coordinates around the already derived
active means.

## What Is Closed
- Exact reduction from full microscopic `D` to `(D_0^trip, D_-^trip)`
- Exact downstream recovery of branch, sheet, `H_nu`, `H_e`, masses, and PMNS
- Exact elimination of passive phases
- Exact elimination of the passive moduli as an independent last-mile object

## What Is Not Yet Claimed
This packet does **not** claim full sole-axiom neutrino closure from
`Cl(3)` on `Z^3` alone. The remaining open object is the four-real active
orbit-breaking source.

## Representative Runners
- [frontier_pmns_full_microscopic_operator_to_pair.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_full_microscopic_operator_to_pair.py)
- [frontier_pmns_lower_level_end_to_end_closure.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_lower_level_end_to_end_closure.py)
- [frontier_pmns_passive_monomial_phase_reduction.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_passive_monomial_phase_reduction.py)
- [frontier_pmns_microscopic_d_seven_real_last_mile.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_microscopic_d_seven_real_last_mile.py)
- [frontier_pmns_microscopic_d_four_real_last_mile.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_microscopic_d_four_real_last_mile.py)
