# PMNS Lower-Level End-to-End Closure

**Status:** support - structural or confirmatory support note
**Primary runner:** [`scripts/frontier_pmns_lower_level_end_to_end_closure.py`](../scripts/frontier_pmns_lower_level_end_to_end_closure.py) (PASS=26/0)
Starting from lower-level observable packs only:

- active/passive response columns on the retained lepton supports

the lane reconstructs:

- `tau`
- `q`
- passive block and `a_i`
- active block and full active coordinates
- `(D_0^trip, D_-^trip)`
- branch
- sheet
- `H_nu`, `H_e`
- masses
- PMNS

The runner contains a circularity guard: no target PMNS objects appear as
inputs.
