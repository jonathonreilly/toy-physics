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
- the two-source taste-radial row production manifest as bounded run-control
  support only: it records exact no-resume chunk commands and a collision
  guard for future `C_sx/C_xx` rows, but it is not row data, pole evidence,
  canonical `O_H`, scalar LSZ normalization, or `y_t` closure.
- the two-source taste-radial row-wave launcher as bounded run-control support
  only: it records active occupancy and can start a capped no-resume wave, but
  active processes, logs, empty directories, and partial directories are not
  row data, pole evidence, canonical `O_H`, scalar LSZ normalization, or
  `y_t` closure.
- the two-source taste-radial chunk checkpoint runner as bounded schema
  infrastructure only: completed mode will validate real chunk JSON, while
  pending mode records only active PIDs and the absence of row JSON.  Pending
  checkpoints are not row data, pole evidence, canonical `O_H`, scalar LSZ
  normalization, or `y_t` closure.
- the completed two-source taste-radial chunks001-012 checkpoints as
  bounded row support only: they validate real chunk JSON, seed control,
  selected-mass-only FH/LSZ, and `C_sx/C_xx` timeseries, but not combined L12
  pole evidence, canonical `O_H`, scalar LSZ normalization, or `y_t` closure.
- the two-source taste-radial row-combiner gate as bounded aggregation support
  only: it records `ready=12/63` and refuses to write the combined measurement
  row packet until 63/63 chunks are schema-clean.  Partial diagnostics are not
  combined L12 pole evidence, canonical `O_H`, scalar LSZ normalization,
  `kappa_s`, or `y_t` closure.
- the Two-source taste-radial Schur-subblock witness as bounded row support
  only: chunks001-012 supply finite `C_ss/C_sx/C_xx` correlator subblocks for
  the certified `s/x` source chart with positive Gram determinants, but finite
  C_ss/C_sx/C_xx correlator subblocks are not strict K-prime pole rows, do not
  provide `A'`, `B'`, or `C'` pole derivatives, and do not identify `x` with
  canonical `O_H`.
- the taste-radial canonical-`O_H` selector gate as exact conditional support
  only: it proves the cyclic degree-one radial source is unique in
  `span{S0,S1,S2}`, but also proves current `Z3`/trace/source filters do not
  select it from the full trace-zero invariant taste algebra.
- the Degree-one Higgs-action premise gate as an exact current-surface
  boundary only: degree-one filtering selects the implemented taste-radial
  `E1` source, but degree is not proof selectors until a same-surface EW/Higgs
  action or canonical-operator theorem derives the degree-one premise.
- the FMS post-degree route rescore as route support only: FMS/lattice
  literature is route guidance only, not PR230 proof authority, and it does
  not supply the same-surface EW/Higgs action, canonical `O_H`, source-Higgs
  rows, or Gram-purity certificate.
- the FMS composite-`O_H` conditional theorem as exact route support only:
  given a future same-surface gauge-Higgs action with
  `Phi^dagger Phi=((v+h)^2+pi^2)/2`, it derives the linear `v h` component and
  pole-residue scaling `v^2 Z_h`, but it does not supply the action, `v`,
  `Z_h`, source-overlap row `C_sH`, `C_HH` pole rows, or Gram/FV/IR authority.
- the Higgs mass-source action bridge as conditional support only: if a future
  same-surface EW/Higgs action couples the scalar source to centered
  `Phi^dagger Phi`, then the source derivative is `dS/ds=sum O_H` and the
  degree-one coefficient is `v`; the current action, canonical `O_H`
  certificate, `v`, LSZ normalization, source-Higgs pole rows, and any
  `kappa_s=1` authority are absent.
- the refreshed same-source EW action certificate builder/gate as contract
  support only: it now requires a centered `Phi^dagger Phi` source coupling and
  the Higgs mass-source action bridge, but still reports the action certificate
  absent and supplies no W/Z rows, canonical `O_H`, source-Higgs rows, LSZ, or
  closure.
- the same-source EW/Higgs action ansatz gate as conditional action-extension
  support only: it specifies a concrete lattice `SU(2)xU(1)`/Higgs ansatz with
  the PR230 scalar source coupled to centered `Phi^dagger Phi`, and checks the
  source derivative plus local FMS expansion.  It is conditional
  action-extension support only, not an adopted current-surface action, does
  not write accepted future certificate paths, and supplies no canonical
  `O_H`, `C_sH/C_HH` rows, W/Z rows, LSZ, `kappa_s`, or closure.
  Exact stress phrases: conditional action-extension support only; does not write accepted future certificate paths.
- the Same-source EW action adoption attempt as an exact shortcut boundary:
  the ansatz supplies the action-form side, but ansatz-only action-adoption
  shortcut blocked remains the current status because the canonical-Higgs
  operator certificate, same-source sector-overlap theorem, W/Z correlator
  mass-fit path certificate, accepted action-certificate input, and current
  action gate are still absent.  It writes no accepted EW action certificate.
  Exact adoption stress phrases: ansatz-only action-adoption shortcut blocked; canonical-Higgs operator certificate; W/Z correlator mass-fit path certificate.
- the radial-spurion sector-overlap theorem as exact conditional support only:
  if a future adopted same-surface EW/Higgs action makes `s` a single
  canonical-Higgs radial spurion with no independent additive top bare-mass
  source, then `dv/ds` cancels in top/W and top/Z response ratios.  The current
  PR230 additive mass FH source is not that contract, and the theorem does not
  supply W/Z mass-fit rows, canonical `O_H`, `kappa_s`, or closure.
- the post-FMS source-overlap necessity gate as exact current-surface boundary
  only: it proves current source-only rows, FMS `C_HH` support, and
  taste-radial `C_sx/C_xx` chunks do not infer `Res C_sH` or exclude an
  orthogonal neutral top coupling.  It does not close PR230; it names the
  missing row/theorem more sharply.
- the source-Higgs overlap/kappa contract as exact support only: it derives
  the future measured overlap
  `kappa_spH = Res(C_sH)/sqrt(Res(C_ss) Res(C_HH))` and proves source-scale
  invariance, but the current surface has no certified `O_H` row packet and
  does not set `kappa_s = 1`.
- the Z3-triplet positive-cone H2 support certificate as exact algebraic
  support only: the projectors `Q_i^+=(I+S_i)/2` are PSD, nonzero,
  equal-rank/equal-norm, and cycled by the same Z3 operator.  This supplies
  H2 for the conditional primitive route, but it is not a physical neutral
  transfer, primitive irreducibility theorem, source-Higgs coupling, scalar
  LSZ normalization, `kappa_s`, or `y_t` closure.

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
- FMS composite `Phi^dagger Phi` expansion is not a proof selector until the
  same-surface EW/Higgs action and source-Higgs pole rows exist on PR230.
- Higgs mass-source action bridge is not a proof selector until a same-surface
  EW/Higgs action, canonical `O_H` certificate, nonzero `v` authority, LSZ
  normalization, and source-Higgs pole rows exist on PR230.
- Same-source EW action contract refresh is not a proof selector until a real
  same-surface EW/Higgs action candidate satisfies that refreshed contract and
  the downstream W/Z or source-Higgs row gates pass.
- Same-source EW/Higgs action ansatz is not a proof selector until a
  same-surface adoption theorem accepts it as actual PR230 action authority and
  the downstream canonical `O_H`, source-Higgs row, W/Z row, Gram/LSZ/FV/IR,
  and retained-route gates pass.
- Radial-spurion sector-overlap algebra is not a proof selector until the
  PR230 action is actually adopted as a no-independent-top-source canonical
  radial-spurion action or equivalent production rows measure/subtract the
  additive top-source component.
- Post-FMS `C_HH` support is not a source-overlap proof selector until a
  same-surface `Res C_sH` row, Gram-purity theorem, or physical-response
  bypass exists on PR230.
- Source-Higgs overlap/kappa formula rows are not proof selectors until a
  same-surface certified `O_H/C_sH/C_HH` pole-row packet exists and passes
  Gram/FV/IR/model-class and retained-route gates.
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
- Z3 positive-cone H2 support is not a proof selector until the PR230 surface
  supplies the physical transfer/action or off-diagonal generator (H3) and the
  source/canonical-Higgs coupling authority (H4).
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
- Two-source taste-radial row production manifest is not proof selectors until the planned chunks are actually run, combined, pole-tested, and bridged to canonical O_H or physical response.
- Two-source taste-radial row-wave launcher status is not proof selectors until
  completed chunk JSON exists and passes per-chunk schema gates; active
  workers and partial directories are explicitly non-evidence.
- Two-source taste-radial active-pending chunk checkpoints are not proof
  selectors; they explicitly certify that completed row JSON is absent.
- Completed two-source taste-radial chunks001-012 are not proof selectors
  until combined row evidence, pole/FV/IR authority, and canonical
  `O_H`/source-overlap or physical-response authority exist.
- Source-Higgs schema field names in completed two-source taste-radial chunks
  are not proof selectors; the readiness gate now treats them as explicit
  `C_sx/C_xx` second-source aliases unless a real canonical `O_H` identity,
  pole-residue row packet, and physical-readout certificate are present.
- Partial two-source taste-radial row-combiner diagnostics are not proof
  selectors; the combined row packet is intentionally absent until 63/63
  manifest chunks are present and schema-clean, and even a complete packet
  still requires pole/FV/IR authority plus canonical `O_H`/source-overlap or
  physical-response authority.
- Finite-mode `rho_sx` and `Delta_sx` diagnostics in the partial combiner are
  not proof selectors; they are not isolated-pole residues and do not certify
  Gram purity, scalar LSZ normalization, canonical `C_sH/C_HH`, or `y_t`.
- Two-source taste-radial Schur-subblock witness rows are not proof selectors;
  finite C_ss/C_sx/C_xx correlator subblocks are not strict K-prime pole rows,
  do not provide pole derivatives or FV/IR authority, and do not turn
  taste-radial `x` into canonical `O_H`.
- Taste-radial degree-one uniqueness is not a proof selector until a
  same-surface EW/Higgs action or canonical-operator theorem derives the
  degree-one Higgs-action premise.
- Degree-one Higgs-action premise is not proof selectors until a same-surface EW/Higgs action or canonical-operator theorem derives the degree-one premise.
- FMS/lattice literature is route guidance only, not PR230 proof authority.
- FMS post-degree route rescore is not proof selectors until a same-surface
  EW/Higgs action, canonical `O_H` certificate, source-Higgs rows, and
  Gram-purity certificate exist.
- source-coordinate transport from the PR230 uniform mass source to a canonical
  taste-axis Higgs source;
- same-surface canonical `O_H` identity and normalization;
- production `C_sH/C_HH` pole residues;
- future source-Higgs production rows must attach
  `outputs/yt_pr230_genuine_source_pole_artifact_intake_2026-05-06.json` and
  must preserve its support-only status;
- future source-Higgs production rows must also attach
  `outputs/yt_pr230_source_higgs_overlap_kappa_contract_2026-05-06.json` and
  report `kappa_spH = Res(C_sH)/sqrt(Res(C_ss) Res(C_HH))` as a measured
  overlap field; this is not permission to set `kappa_s = 1`;
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
