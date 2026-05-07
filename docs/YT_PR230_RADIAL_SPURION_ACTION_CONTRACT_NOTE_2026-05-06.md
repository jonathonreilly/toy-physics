# PR230 Radial-Spurion Action Contract

**Status:** exact-support / no-independent-top-source radial-spurion action
contract; current additive-source action not adopted
**Runner:** `scripts/frontier_yt_pr230_radial_spurion_action_contract.py`
**Certificate:** `outputs/yt_pr230_radial_spurion_action_contract_2026-05-06.json`

This block turns the radial-spurion sector-overlap theorem into a concrete
future action contract.  The clean W/Z physical-response route is not merely
"use the same source name."  It requires an accepted same-surface EW/Higgs
action in which the scalar source moves one canonical-Higgs radial branch
`v(s)` and does not also add an independent top bare-mass source.

The required mass branches are:

```text
m_t(s) = y_t v(s) / sqrt(2)
M_W(s) = g2 v(s) / 2
M_Z(s) = sqrt(g2^2 + gY^2) v(s) / 2
```

Then the common source overlap `dv/ds` cancels in the response ratios:

```text
y_t = g2 (dm_t/ds) / (sqrt(2) dM_W/ds)
y_t = sqrt(g2^2 + gY^2) (dm_t/ds) / (sqrt(2) dM_Z/ds)
```

The runner also checks the failure mode.  If an independent additive top
source contributes `a_top` to `dm_t/ds`, the inferred value changes with
`a_top`.  That is the current PR230 risk surface: the existing FH/LSZ top
source is additive, and the same-source EW/Higgs ansatz is not adopted as a
current action authority.

This contract is support only.  It does not write the accepted EW action
certificate, does not provide W/Z rows, does not supply strict `g2`, does not
identify canonical `O_H`, does not create `C_sH/C_HH` pole rows, and does not
authorize retained/proposed_retained language.

```bash
python3 scripts/frontier_yt_pr230_radial_spurion_action_contract.py
# SUMMARY: PASS=13 FAIL=0
```
