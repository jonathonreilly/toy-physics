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
- And finally closed on the lower-level active transport chain:
  [PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md](/Users/jonBridger/Toy%20Physics-neutrino-majorana/docs/PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md)

## Current Exact Endpoint
On the lower-level retained transport / response chain, the Dirac / PMNS lane
is closed. The historical last-mile reductions still matter because they show
what had to be fixed:

- `tau`
- `q`
- `xbar`
- `sigma`
- passive Hermitian moduli `(|a_1|, |a_2|, |a_3|)`
- active orbit-breaking coordinates `(xi_1, xi_2, rho_1, rho_2)`

The new point is that the active four-real source is no longer an extra open
object once the non-averaged lower-level active transport / response profile is
derived. It is exactly the centered non-averaged part of that active profile.

## What Is Closed
- Exact reduction from full microscopic `D` to `(D_0^trip, D_-^trip)`
- Exact downstream recovery of branch, sheet, `H_nu`, `H_e`, masses, and PMNS
- Exact elimination of passive phases
- Exact elimination of the passive moduli as an independent last-mile object
- Exact elimination of the active four-real source as an independent lower-level
  theorem target once the active transport / response profile is available

## What Is Not Yet Claimed
This packet does **not** claim full sole-axiom neutrino closure from
`Cl(3)` on `Z^3` alone. The remaining open object is the derivation of the
relevant lower-level active/passive transport or response profiles from the
sole axiom itself, rather than the extraction of PMNS data once those profiles
are available.

## Representative Runners
- [frontier_pmns_full_microscopic_operator_to_pair.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_full_microscopic_operator_to_pair.py)
- [frontier_pmns_lower_level_end_to_end_closure.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_lower_level_end_to_end_closure.py)
- [frontier_pmns_passive_monomial_phase_reduction.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_passive_monomial_phase_reduction.py)
- [frontier_pmns_microscopic_d_seven_real_last_mile.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_microscopic_d_seven_real_last_mile.py)
- [frontier_pmns_microscopic_d_four_real_last_mile.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_microscopic_d_four_real_last_mile.py)
- [frontier_pmns_active_four_real_source_from_transport.py](/Users/jonBridger/Toy%20Physics-neutrino-majorana/scripts/frontier_pmns_active_four_real_source_from_transport.py)
