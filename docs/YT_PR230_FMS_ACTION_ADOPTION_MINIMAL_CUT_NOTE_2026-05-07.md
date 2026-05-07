# PR230 FMS Action-Adoption Minimal Cut

Date: 2026-05-07

Status: exact-support / FMS action-adoption minimal cut; current PR230 surface does not close.

Runner:
`scripts/frontier_yt_pr230_fms_action_adoption_minimal_cut.py`

Certificate:
`outputs/yt_pr230_fms_action_adoption_minimal_cut_2026-05-07.json`

## Result

The FMS route remains the cleanest physics route, but only as a strict future
action-adoption path.  The current branch has real support:

- `O_sp`, the same-source LSZ-normalized source-pole operator;
- the degree-one taste-radial axis theorem under a future action premise;
- an explicit FMS `O_H` candidate/action packet;
- the exact future residue readout formula
  `kappa_sH = Res(C_sH)/sqrt(Res(C_ss) Res(C_HH))`;
- a non-colliding source-Higgs time-kernel production manifest.

Those supports do not adopt the action.  The minimal adoption cut still needs:

- a same-surface Cl(3)/Z3 derivation or accepted EW/Higgs action extension;
- dynamic `Phi` and gauge-covariant Higgs kinetic/update semantics;
- canonical radial `h`, radial background `v`, and LSZ metric authority;
- canonical `O_H = Phi^dagger Phi - <Phi^dagger Phi>` provenance and
  normalization;
- `dS/ds = sum_x O_H(x)` with no independent additive top bare-mass source;
- production `C_ss/C_sH/C_HH` pole rows with covariance, FV/IR, zero-mode, and
  model-class authority;
- aggregate assembly, retained-route, and campaign gates.

## Boundary

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not identify `O_sp` or the taste-radial second source with canonical
`O_H`, does not relabel `C_sx/C_xx` as `C_sH/C_HH`, and does not set
`kappa_s`, `c2`, `Z_match`, or `g2` to one.  FMS literature and the action
ansatz remain route context, not proof authority.

## Validation

```bash
python3 -m py_compile scripts/frontier_yt_pr230_fms_action_adoption_minimal_cut.py
python3 scripts/frontier_yt_pr230_fms_action_adoption_minimal_cut.py
# SUMMARY: PASS=11 FAIL=0
```
