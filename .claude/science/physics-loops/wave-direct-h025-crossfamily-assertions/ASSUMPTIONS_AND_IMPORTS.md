# Assumptions And Imports

## Local Inputs

- `logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`
- `logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt`

These logs are treated as frozen source artifacts for this bounded check.  The branch does not rerun the expensive fine-`H` controls.

## Imports

- The control-log values are imported from prior generated artifacts.
- The assertion runner verifies consistency between those logs and the cross-family note.
- No external physics or literature value is imported.
- No new axiom, selector, or family-portability premise is introduced.

## Open Imports

- A later audit may still require auditing the underlying Fam1/Fam2 control notes and their heavy runners.
- Fam3 remains unclaimed.
- A stable amplitude law remains unclaimed.
