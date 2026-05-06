# PR #230 Same-Source EW Action Gate

```yaml
actual_current_surface_status: exact negative boundary / same-source EW action not defined on PR230 surface
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_wz_same_source_ew_action_gate.py`  
**Certificate:** `outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json`

## Purpose

This note closes the first W/Z implementation work unit from the PR #230 W/Z
response plan: does the current repo already define a same-source electroweak
gauge/Higgs production action that can measure `dM_W/ds` or `dM_Z/ds` under the
same scalar source used by the top FH/LSZ run?

It does not.  The current top production harness is an `SU(3)` QCD
Wilson-staggered top-correlator harness with scalar source shifts.  It has an
explicit W/Z absent guard and no W/Z correlator mass-fit path.  The current
EW/Higgs notes give tree-level dictionaries such as `M_W = g_2 v / 2` after a
canonical Higgs field has already been supplied; they are not a lattice EW
action and not a `dM_W/ds` measurement.

## Action Contract

A future W/Z action certificate must provide all of the following:

- dynamical `SU(2)_L` and `U(1)_Y` gauge fields with update or ensemble
  semantics;
- a scalar source `s` coupled to centered `Phi^dagger Phi`, with the Higgs
  mass-source action bridge attached, not to `H_unit`;
- a same-source-coordinate certificate tying the top `dE_top/ds` source to the
  W/Z `dM/ds` source;
- W/Z two-point correlators and mass fits under source shifts;
- a firewall excluding observed masses/couplings, static EW algebra, `H_unit`,
  `yt_ward_identity`, `alpha_LM`, plaquette, and `u0` authority.

## Validation

```text
python3 scripts/frontier_yt_wz_same_source_ew_action_gate.py
# SUMMARY: PASS=22 FAIL=0
```

## Boundary

This is an exact negative boundary for the current PR230 surface, not a physics
closure.  It writes no W/Z measurement rows, defines no retained or
`proposed_retained` claim, and does not modify the running QCD production
campaign.

Next action: implement a genuine same-source EW gauge/Higgs production action
and W/Z correlator mass-fit harness, or pivot back to source-Higgs pole rows,
Schur rows, neutral-sector irreducibility, or FH/LSZ production evidence.
