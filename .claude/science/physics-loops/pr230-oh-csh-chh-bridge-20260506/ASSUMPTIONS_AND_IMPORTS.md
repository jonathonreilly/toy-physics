# Assumptions And Imports

Forbidden proof inputs:

- `H_unit` matrix-element readout;
- `yt_ward_identity` as top-Yukawa authority;
- observed top mass or observed `y_t` as selectors;
- `alpha_LM`, plaquette, or `u0` as Yukawa proof input;
- setting `kappa_s`, `cos(theta)`, `c2`, or `Z_match` to one by convention.

Allowed context:

- the exact algebra of the taste-shift operators in
  `TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md`;
- the PR230 production harness source coordinate, which is the uniform additive
  scalar mass shift `m_bare + s`;
- existing source-Higgs gates as acceptance surfaces.
- the May 6 genuine `O_sp` intake artifact as source-side support only, not as
  canonical-Higgs identity or physical `y_t` closure.
- the `origin/main` composite-Higgs stretch packet as cross-lane action-first
  context only, not as PR230 `O_H`, source-transport, or `C_sH/C_HH`
  authority.
- the `origin/main` EW M-residual CMT packet as context only.  Its Fierz
  singlet/adjoint channel bookkeeping may inform future W/Z work, but it is
  not PR230 same-source EW action, W/Z response, canonical `O_H`, or
  source-Higgs pole-row authority.
- Origin-main EW M-residual CMT packet is a context-only intake guard, not
  a PR230 closure artifact.
- the exact lazy-Z3 primitive matrix theorem as conditional mathematics only:
  if a same-surface PR230 action supplies a positive lazy cyclic transfer on
  the triplet, Perron-Frobenius gives rank-one triplet support.
- the H1 Z3 generation-action lift attempt as an exact current-surface
  boundary: Koide/lepton Z3 can be held fixed while quark-bilinear generation
  action is trivial or cyclic, and current PR230 source/action data do not
  select between them.
- the Z3 lazy-transfer promotion attempt as an exact current-surface boundary:
  the same-surface artifact supplies the cyclic symmetry `P`, and
  `L=(I+P)/2` is primitive as mathematics, but current PR230 artifacts do not
  instantiate `L` as physical dynamics.
- the two-source taste-radial chart certificate as exact source-coordinate
  support only: `I_8/sqrt(8)` and `(S0+S1+S2)/sqrt(24)` form an orthonormal
  same-surface chart, but the second coordinate is not a production action,
  canonical `O_H`, or a measured source-Higgs row.
- the two-source taste-radial action source vertex as exact harness support
  only: the blocked-hypercube source `X=(X_1+X_2+X_3)/sqrt(3)` is now a
  gauge-covariant source vertex, but it is not a canonical `O_H` identity,
  scalar LSZ normalization, or measured production row.
- the two-source taste-radial `C_sx/C_xx` row contract as bounded harness
  support only: the schema now names second-source rows explicitly, but the
  current artifact is not production evidence, pole residue extraction,
  canonical `O_H`, scalar LSZ normalization, or `y_t` closure.

Open imports after this block:

- Taste-condensate O_H bridge is a checked shortcut, not an authority row.
- uniform mass source is orthogonal to taste-axis Higgs operators in the
  exact taste-block Hilbert-Schmidt algebra.
- Higgs/taste-stack theorem names are not proof selectors until source-coordinate transport or C_sH/C_HH rows exist.
- Cross-lane composite-Higgs stretch packets are not PR230 proof selectors
  until same-source `O_H`, action, transport, or `C_sH/C_HH` rows exist on the
  PR230 surface.
- CMT/u0/Fierz channel bookkeeping is not proof selectors until an explicit
  same-surface EW Wilson-line action/current and W/Z response rows exist with
  strict `g2`, covariance, and `delta_perp` authority.
- Source-coordinate transport to O_H is not proof selectors until a same-surface transport certificate exists.
- Source-coordinate transport completion is a current-surface boundary, not a
  global theorem against future transport.
- unit-preserving/trace-preserving/taste-equivariant maps cannot send I_8 to trace-zero S_i.
- source-coordinate transport is not proof selectors until source-to-taste-axis certificate, canonical O_H rows, or neutral rank-one theorem exists.
- Action-first O_H/C_sH/C_HH route completion is a current-surface boundary,
  not a global theorem against the future FMS route.
- action-first O_H/C_sH/C_HH is not proof selectors until same-source EW/Higgs action, canonical O_H, source-Higgs rows, and Gram-purity certificate exist.
- W/Z same-source response route completion is a current-surface boundary, not
  a global theorem against the future physical-response bypass.
- W/Z same-source response is not proof selectors until same-source EW action, W/Z response rows, matched covariance, strict g2, and delta_perp control exist.
- Schur A/B/C route completion is a current-surface boundary, not a global
  theorem against future neutral-kernel row derivation.
- Schur A/B/C route completion is not proof selectors until neutral kernel basis plus Schur A/B/C rows or equivalent row theorem exists.
- Neutral primitive/rank-one route completion is a current-surface boundary,
  not a global theorem against future primitive neutral transfer derivation.
- Neutral primitive/rank-one route completion is not proof selectors until same-surface primitive transfer, off-diagonal generator, or irreducibility certificate exists.
- The conditional lazy-Z3 theorem is not a proof selector until the PR230
  surface supplies the positive transfer/action, off-diagonal neutral
  generator, or strict primitive-cone certificate.
- Koide/lepton Z3 is not a quark-bilinear generation-action proof selector
  until a same-surface H1 certificate selects the cyclic action and ties it to
  the PR230 source/action surface.
- Z3 lazy-transfer promotion attempt is not proof selectors until a
  same-surface neutral transfer/action or off-diagonal generator instantiates
  the lazy transfer.
- Two-source taste-radial chart is not proof selectors until a same-surface
  production/action row turns on the second source and separate authority
  identifies it with canonical `O_H` or supplies measured `C_sx/C_xx` rows.
- Two-source taste-radial action source vertex is not proof selectors until
  measured `C_sx/C_xx` rows and canonical `O_H`/source-overlap or
  physical-response authority exist.
- Two-source taste-radial action source vertex is not proof selectors until
  measured C_sx/C_xx rows and canonical O_H/source-overlap or
  physical-response authority exist.
- Two-source taste-radial action source vertex is not proof selectors until measured C_sx/C_xx rows and canonical O_H/source-overlap or physical-response authority exist.
- Two-source taste-radial row contract is not proof selectors until production C_sx/C_xx rows, pole/FV/IR authority, and canonical O_H/source-overlap or physical-response authority exist.
- source-coordinate transport from the PR230 uniform mass source to a canonical
  taste-axis Higgs source;
- same-surface canonical `O_H` identity and normalization;
- production `C_sH/C_HH` pole residues;
- future source-Higgs production rows must attach
  `outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json` and
  must preserve its support-only status;
- W/Z response rows with strict non-observed `g2`, matched covariance, and
  `delta_perp` authority;
- Schur `A/B/C` rows from a real neutral scalar kernel basis;
- neutral primitive-cone / off-diagonal-generator theorem;
- same-surface lazy positive Z3/triplet transfer if the conditional primitive
  theorem is to become load-bearing;
- same-surface H1 quark-bilinear Z3 action certificate, if the origin/main
  composite-Higgs packet is to become load-bearing;
- scalar-LSZ, FV/IR, and matching gates.

Negative-route interpretation:

- current negative artifacts block shortcuts on the current surface;
- they do not block first-principles derivation after a named same-surface row,
  certificate, or theorem is supplied.
