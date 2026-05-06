# Assumptions And Imports

## Scope

The claim is a bounded finite computation over the listed `topN` support sizes
in the existing 2D ordered-lattice harness.

## Imports

- No observational, PDG, cosmological, fitted, or literature values are used.
- Numerical parameters are harness inputs: `h=0.5`, `W=12`, `L=20`,
  `source_y=5.0`, `sigma=1.25`, and source strength `5e-5`.
- The runner imports the existing 2D lattice generator and helper functions
  from the companion two-stage harness. The claim should be read as a finite
  result on that code-defined harness, not as a new theorem about all possible
  ordered lattices.

## Load-Bearing Checks

The branch-local decisive checks are in
`scripts/mesoscopic_surrogate_threshold_2d.py` and cached at
`logs/runner-cache/mesoscopic_surrogate_threshold_2d.txt`:

- every listed `topN` is scanned;
- every scanned row satisfies the stated stability gate;
- maximum stage-ratio relative error is `0.0066069 <= 0.01`;
- minimum support carry is `1 >= 0.99`;
- first stable support is `topN=1`, so no sharp collapse appears in the
  scanned range.
