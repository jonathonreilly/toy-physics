PR230 Block103 checkpoint: Z3 heat-kernel scale-selector no-go.

What landed:

- Added `scripts/frontier_yt_pr230_z3_heat_kernel_scale_selector_no_go.py`.
- Added `outputs/yt_pr230_z3_heat_kernel_scale_selector_no_go_2026-05-15.json`.
- Added `docs/YT_PR230_Z3_HEAT_KERNEL_SCALE_SELECTOR_NO_GO_NOTE_2026-05-15.md`.
- Wired the certificate into retained-route, campaign-status, full-assembly,
  completion-audit, and assumption/import stress gates.
- Updated the PR230 loop pack state, handoff, claim status, no-go ledger,
  assumptions, opportunity queue, artifact plan, and review history.

Physics result:

- The C3/Z3 heat-kernel family `K_tau = exp(-tau Delta)` remains a genuine
  primitive mathematical semigroup for every `tau > 0`.
- Symmetry, cone, semigroup, reversibility, entropy, and spectral-gap criteria
  do not select a finite physical heat time or diffusion scale on the current
  PR230 surface.
- The obstruction is a scale/time reparametrization: `Delta -> lambda Delta`
  is equivalent to `tau -> lambda tau` unless a same-surface action supplies
  the scale.

Validation:

```text
Z3 heat-kernel scale-selector no-go PASS=13 FAIL=0
retained route PASS=324 FAIL=0
campaign status PASS=426 FAIL=0
full positive assembly PASS=199 FAIL=0
positive completion audit PASS=78 FAIL=0
assumption/import stress PASS=110 FAIL=0
```

Claim boundary:

No retained or `proposed_retained` closure is claimed. The PR remains
draft/open. The neutral route now needs a same-surface physical action,
transfer operator, or off-diagonal generator that fixes the heat
time/diffusion scale plus H4 source/canonical-Higgs coupling; otherwise the
clean closure targets remain accepted `O_H`/action with strict
`C_ss/C_sH/C_HH` pole rows, strict W/Z response with an allowed absolute pin,
or strict Schur/scalar-LSZ pole authority.
