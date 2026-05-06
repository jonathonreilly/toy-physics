# Assumptions And Imports

## Zero-Input / Structural

- The guard's claim is a meta hygiene claim about repo artifacts, not a
  physics theorem.
- The target no-go scripts are the scripts found by the guard's existing
  `SCRIPT_GLOBS`.
- Emitted labels are read from captured stdout after executing each target
  script with the current Python interpreter from the repo root.

## Tooling Assumptions

- `subprocess.run(..., capture_output=True, text=True)` captures the labels
  that the auditor asked to verify.
- A target no-go script may exit nonzero and still provide useful negative
  closeout and residual labels. The guard audits emitted label hygiene, not
  the target script's theorem status.

## Imports Not Used

- No PDG values, measured constants, fitted selectors, literature values, or
  physical boundary conventions are imported.
- No new physics premise is introduced.
