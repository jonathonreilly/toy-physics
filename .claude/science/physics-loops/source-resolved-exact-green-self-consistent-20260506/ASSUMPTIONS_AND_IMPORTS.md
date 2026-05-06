# Assumptions And Imports

## Current Surface Inputs

- Fixed compact exact lattice: `h=0.25`, `W=3`, `L=6`.
- Boundary-clipped cross5 source cluster, leaving four in-bounds source nodes.
- Source strengths: `0.001`, `0.002`, `0.004`, `0.008`.
- Kernel: `exp(-0.08 r)/(r+0.5)`.
- Calibration gain input: `1.7578903308081324`.
- One source-cluster reweighting update from propagated amplitudes.

## No Hidden Promotion Inputs

- The calibrated gain is admitted as a setup input.
- The `green/inst` amplitude ratio is comparator- and calibration-dependent.
- No uncalibrated physical amplitude theorem is claimed.
- No continuum, large-lattice, generated-family, or fully converged
  self-consistent field theory is imported.
