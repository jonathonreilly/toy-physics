# Assumptions And Imports

## Claim Scope

Exact restricted scalar/static-conformal closure on the exact local `O_h`
star-supported source object realized in the current finite-box source
generator.

## Allowed Inputs

| Input | Classification | Role |
|---|---|---|
| `H_0` nearest-neighbor lattice Laplacian on the `15^3` box | framework-derived finite-box operator | defines shell source, Dirichlet solve, and Schur complement |
| `G_0 = H_0^{-1}` on the zero-boundary sector | framework-derived finite-box inverse | reconstructs `phi_ext` from `sigma_R` |
| seven-point star support `{0, +/-e_x, +/-e_y, +/-e_z}` | restricted source-class definition | defines the local source class |
| `O_h`-commutant source parameters in the note | restricted source-class definition | fixes the exact local `O_h` source object; not derived from the single axiom |
| cutoff `R = 4` and exterior projector `Pi_R^ext` | admitted finite-box boundary choice | defines the sewing shell for this restricted theorem |
| static conformal constraint pair | restricted bridge law under proof | determines `rho` and `S` once bridge/source are fixed |
| Schur complement `Lambda_R` | derived from `H_0` block elimination | supplies boundary action and unique minimizer |

## Imported Values

No observational, literature, PDG, cosmological, or fitted target values are
used. The source parameters define the restricted source class; they are not
fit to the closure residuals being proved.

## Open Boundaries

- No derivation of the numerical local `O_h` source parameters from the single
  axiom alone.
- No full nonlinear GR theorem.
- No tensorial Einstein/Regge completion beyond the scalar/static-conformal
  bridge.
- No fully general non-`O_h` strong-field theorem.
