PR230 Block102 checkpoint: Z3 heat-kernel neutral-transfer attempt.

What landed:

- Added `scripts/frontier_yt_pr230_z3_heat_kernel_neutral_transfer_attempt.py`.
- Added `outputs/yt_pr230_z3_heat_kernel_neutral_transfer_attempt_2026-05-15.json`.
- Added `docs/YT_PR230_Z3_HEAT_KERNEL_NEUTRAL_TRANSFER_ATTEMPT_NOTE_2026-05-15.md`.
- Wired the certificate into retained-route, campaign-status, full-assembly,
  completion-audit, and assumption/import stress gates.
- Updated the PR230 loop pack state, handoff, claim status, no-go ledger,
  assumptions, opportunity queue, artifact plan, and review history.

Physics result:

- The C3/Z3 Dirichlet form `Delta=2I-P-P^T` gives a genuine primitive finite
  heat kernel `exp(-t Delta)` for every `t>0`.
- This is exact mathematical support only. The current PR230 surface does not
  identify the heat kernel as the physical neutral transfer, does not derive
  the heat time/scale from the action, and does not supply H4
  source/canonical-Higgs coupling.

Validation:

```text
Z3 heat-kernel attempt PASS=16 FAIL=0
```

Claim boundary:

No retained or `proposed_retained` closure is claimed. The PR remains draft/open.
The next genuine artifact must be accepted `O_H`/action plus strict
`C_ss/C_sH/C_HH` pole rows, strict W/Z response with an allowed absolute pin,
strict Schur/scalar-LSZ pole authority, or a same-surface physical H3/H4
neutral-transfer certificate.
