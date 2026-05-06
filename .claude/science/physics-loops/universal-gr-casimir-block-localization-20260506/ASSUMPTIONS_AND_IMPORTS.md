# Assumptions And Imports

## Local Inputs Fixed By This Block

- Coordinate order `(t, x, y, z)`.
- Frobenius inner product on real symmetric `4 x 4` perturbations.
- Orthonormal 10D polarization basis listed in the note and runner.
- Spatial action `rho(R) h = R^T h R` for `R = diag(1, R_3)`.
- Embedded infinitesimal `SO(3)` generators `A_x,A_y,A_z`.

## Upstream Authorities Cited

- `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
- `docs/S3_ANOMALY_SPACETIME_LIFT_NOTE.md`
- `docs/UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md`
- `docs/UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md`
- `docs/UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md`

## Import Boundary

The runner does not import physical observed values, fitted selectors, or
external comparator targets. It computes the representation algebra from the
displayed basis and the displayed `SO(3)` action.
