# Signed Gravitational Response Lane Backlog

**Date:** 2026-04-25
**Branch:** `codex/signed-gravity-response-backlog`
**Status:** working backlog for the high-risk signed gravitational response
sector; not a claim surface

This backlog extends
[`ANTIGRAVITY_SIGN_SELECTOR_BOUNDARY_NOTE.md`](ANTIGRAVITY_SIGN_SELECTOR_BOUNDARY_NOTE.md)
and records the next concrete work paths so the lane does not collapse back
into an undocumented sign toy.

Language boundary:

- "antigravity" is shorthand only.
- This lane is not a negative-mass, shielding, propulsion, or reactionless
  force claim.
- A physical sector requires a native or naturally hosted `chi_g = +/-1`,
  source/response locking, positive inertial mass, and two-body
  action-reaction closure.
- If the selector cannot be derived or naturally superselected, the lane
  remains a toy-control model.

## Current Baseline

Artifacts landed in the first pass:

- [`../scripts/gravity_signed_sector_harness.py`](../scripts/gravity_signed_sector_harness.py)
- [`../scripts/signed_gravity_two_body_action_reaction.py`](../scripts/signed_gravity_two_body_action_reaction.py)
- [`../scripts/staggered_antigravity_response_window.py`](../scripts/staggered_antigravity_response_window.py)
- [`../scripts/lensing_sign_phase_diagram.py`](../scripts/lensing_sign_phase_diagram.py)
- [`ANTIGRAVITY_SIGN_SELECTOR_BOUNDARY_NOTE.md`](ANTIGRAVITY_SIGN_SELECTOR_BOUNDARY_NOTE.md)

Current closure/blocker artifacts:

- [`../scripts/signed_gravity_cl3z3_source_character_derivation.py`](../scripts/signed_gravity_cl3z3_source_character_derivation.py)
- [`../scripts/signed_gravity_source_character_uniqueness_theorem.py`](../scripts/signed_gravity_source_character_uniqueness_theorem.py)
- [`../scripts/signed_gravity_nature_grade_closure_blockers.py`](../scripts/signed_gravity_nature_grade_closure_blockers.py)
- [`../scripts/signed_gravity_oriented_tensor_source_lift.py`](../scripts/signed_gravity_oriented_tensor_source_lift.py)
- [`../scripts/signed_gravity_tensor_source_transport_retention.py`](../scripts/signed_gravity_tensor_source_transport_retention.py)
- [`../scripts/signed_gravity_continuum_graded_einstein_localization.py`](../scripts/signed_gravity_continuum_graded_einstein_localization.py)
- [`../scripts/signed_gravity_remaining_closure_gates.py`](../scripts/signed_gravity_remaining_closure_gates.py)
- [`../scripts/signed_gravity_native_boundary_complex_containment.py`](../scripts/signed_gravity_native_boundary_complex_containment.py)
- [`../scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py`](../scripts/signed_gravity_staggered_dirac_boundary_eta_realization.py)
- [`../scripts/signed_gravity_naturally_hosted_orientation_line.py`](../scripts/signed_gravity_naturally_hosted_orientation_line.py)
- [`SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md`](SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md)
- [`SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md`](SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md)
- [`SIGNED_GRAVITY_NATURE_GRADE_CLOSURE_BLOCKER_AUDIT_NOTE.md`](SIGNED_GRAVITY_NATURE_GRADE_CLOSURE_BLOCKER_AUDIT_NOTE.md)
- [`SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_NOTE.md`](SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_NOTE.md)
- [`SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_NOTE.md`](SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_NOTE.md)
- [`SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_NOTE.md`](SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_NOTE.md)
- [`SIGNED_GRAVITY_REMAINING_CLOSURE_GATES_NOTE.md`](SIGNED_GRAVITY_REMAINING_CLOSURE_GATES_NOTE.md)
- [`SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_CONTAINMENT_NOTE.md`](SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_CONTAINMENT_NOTE.md)
- [`SIGNED_GRAVITY_STAGGERED_DIRAC_APS_BOUNDARY_REALIZATION_NOTE.md`](SIGNED_GRAVITY_STAGGERED_DIRAC_APS_BOUNDARY_REALIZATION_NOTE.md)
- [`SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md`](SIGNED_GRAVITY_NATURALLY_HOSTED_ORIENTATION_LINE_NOTE.md)

Current first-pass result:

- source-only and response-only signs are controls and fail mixed-pair
  momentum balance
- source/response-locked signs pass the four-pair table:
  `++` attract, `+-` repel, `-+` repel, `--` attract
- positive inertial mass is retained
- Born, norm, null-field, `F~M`, and analytic kernel portability controls pass
- a native conservation theorem for `chi_g` remains open only beyond the
  audited local/taste-cell route
- the first strict local/taste-cell selector scan now returns
  `NO_GO_STRICT_SELECTOR`: conserved neutral taste labels exist, but no scanned
  local Pauli-string involution both conserves the massive parity-scalar
  surface and pins scalar source sign
- the first source-primitive audit now returns
  `SOURCE_PRIMITIVE_BLOCKED_LOCAL`: the parity scalar coupling varies to
  `epsilon|psi|^2`, but that density is not branch-stable, not conserved by
  retained kinetic hopping, and washes out under refinement; inserted
  `chi_g|psi|^2` remains a control, not a derivation
- the first nonlocal/boundary batch found conserved or formal labels, but no
  native source/response-locked active gravitational sign:
  `BOUNDARY_CHI_SOURCE_NOT_LOCKED` for coframe and `Z2` flux,
  `APS_BOUNDARY_INDEX_PROBE_PASS_SOURCE_LOCKING_OPEN` for APS eta sign, and
  `NONLOCAL_PROJECTOR_FORMAL_CONTROL_ONLY` for projector-difference charge
- the APS/Wald/Gauss bridge audit now returns
  `APS_WALD_GAUSS_BRIDGE_NOT_DERIVED`: eta is source-neutral under
  gap-preserving variations, the retained Wald/Gauss scale is positive and
  unsigned, and the locked table appears only after inserting `chi_eta` into
  the source action
- a minimal APS-locked source action proposal is now explicit:
  `S_int = - chi_eta M_phys <|psi|^2, Phi>`, with final tag
  `APS_LOCKED_SOURCE_ACTION_CONDITIONAL_CANDIDATE`; it passes variation,
  locked-table, positive-inertia, Born, norm, null, and source-unit controls,
  but it is a new source-action premise until derived from retained
  APS/Wald/Gauss structure
- the origin/superselection/stability audit now returns
  `APS_LOCKED_ACTION_CONDITIONAL_NOT_RETAINED`: the proposed action requires a
  new `chi_eta rho Phi` cross term, eta superselection is conditional on a
  protected boundary gap, and the locked positive-mass law avoids the
  negative-mass runaway control while retaining the ordinary short-distance
  gravity boundedness problem
- the retained boundary source-principle audit now returns
  `RETAINED_BOUNDARY_SOURCE_PRINCIPLE_NO_GO`: positive Born/Gauss source plus
  APS spectator plus positive Wald area cannot span the orientation-odd signed
  source, and APS gap protection requires a new hard constraint or dynamical
  zero-crossing exclusion theorem
- the explicit new-axiom pass now returns
  `APS_LOCKED_AXIOM_EXTENSION_CONTROLLED_CANDIDATE`: an eta-polarized source
  line plus hard gapped-sector admissibility coherently supplies the locked
  source/response sign, positive inertial mass, null-sector quarantine,
  momentum balance, Born/norm controls, and first refinement sanity checks; it
  is an axiomatic extension, not a retained theorem or physical claim
- the source-line origin pass now returns
  `ETA_SOURCE_LINE_ORIGIN_CONDITIONAL_A1_TENSOR_LIFT`: if compact active
  sources are local sections of the real APS determinant-orientation line,
  then locality, orientation covariance, real-action discipline, null
  quarantine, and refinement invariance force the coefficient to `chi_eta`;
  the same line has a clean invariant `A1` lapse/trace lift, while full
  tensor/Einstein localization requires the separate oriented tensor-source
  lift now tracked below
- the source-character uniqueness theorem now returns
  `ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL`: within the
  determinant-orientation source-character grammar, exhaustive finite
  enumeration and the algebraic refinement argument force the unique
  normalized local real character to be `sign(eta)=chi_eta`; the same 3+1
  covariance audit proves the source line is tensorially maximal at invariant
  `A1` and has no nonzero canonical complement vector
- the original-stack derivation pass now returns
  `CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE`: on the finite
  `Cl(3)`/`Z^3` Grassmann/staggered-Dirac determinant-line surface, `log|det|`
  supplies the positive scalar magnitude while the determinant-line package
  hosts the local orientation character used by the source-character grammar;
  the later hosted-line audit narrows this to a real `Z2` torsor/flat local
  system, not a canonical active signed-source selector
- the nature-grade blocker audit now returns
  `SIGNED_GRAVITY_NATURE_GRADE_HARD_BLOCKERS_REDUCED_CONDITIONALS_REMAIN`:
  continuum determinant-line lift, retained graph-family APS realization,
  sector dynamics/preparation, UV/core stability, and tensor localization now
  reduce to conditional finite gates; the scalar determinant source character
  remains `A1`-maximal, but an orientation-line twist can coherently sign an
  ordinary retained tensor source bundle
- the oriented tensor-source lift now returns
  `SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_FINITE_CONDITIONAL`: scalar
  `chi_eta rho` cannot manufacture non-`A1` tensor components, but the derived
  orientation line can twist an ordinary tensor source bundle
  `T_g = chi_eta T_plus`, preserving canonical projectors, linear
  Ward/conservation constraints, locked tensor response signs, and the
  non-claim gate
- the tensor-source transport/retention pass now returns
  `SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_FINITE_CONDITIONAL`: the
  retained gravity stack has a rank-two ordinary tensor source carrier on the
  audited exact local `O_h` and finite-rank classes, the `chi_eta` twist
  commutes with finite family/refinement transport, and cylindrical tensor
  response observables are projectively stable; naive nonlinear `h -> -h`
  closure is blocked by even nonlinear jets and must be replaced by a graded
  nonlinear Einstein localization theorem
- the continuum graded localization pass now returns
  `SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FORMAL_THEOREM`:
  on the chosen canonical continuum GR target, the APS orientation line is a
  flat local system, signed tensor sources commute with Schur/projective
  transport, and nonlinear localization closes as a formal odd/even Einstein
  jet `H_chi(eps)=eps chi h_1+eps^2 h_2+eps^3 chi h_3+...`; global nonlinear
  PDE existence and physical sector preparation are not claimed
- the remaining-gates pass now returns
  `SIGNED_GRAVITY_REMAINING_GATES_REDUCED_TO_PRECISE_CONDITIONALS`: finite
  Galerkin small-data nonlinear contraction passes, raw graph Hodge APS
  boundaries are eta-neutral, fixed sectors are superselected but
  opposite-sector preparation remains boundary-data/defect preparation, and
  pair softening bounds fixed `N` while failing thermodynamic/Ruelle stability
  by itself
- the native boundary-complex containment pass now returns
  `SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED`: the raw
  retained cochain/Hodge boundary complex has cochain-parity-paired spectrum
  and `eta=0`; edge/face orientation reversal is a relabeling control; the
  previous orientation-line APS carrier requires an added one-dimensional line
  plus Hodge zero-mode quarantine unless a future retained boundary theorem
  derives that line
- the staggered-Dirac boundary realization pass now returns
  `SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED`:
  retained-compatible staggered boundary operators are gapped but
  eta-neutral; odd open faces can produce an unpaired eta, but that sign
  flips under staggering-origin shift and disappears under even refinement;
  Pfaffian signs are determinant-line orientation metadata, not invariant
  branch labels
- the naturally-hosted orientation-line pass now returns
  `SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED`:
  the finite Grassmann determinant-line functor naturally hosts a real
  orientation line as a `Z2` torsor/flat local system, but the host does not
  canonically select `chi_eta`, does not put an unpaired APS mode into the raw
  Hodge or retained-compatible staggered boundary operators, and does not
  force the `chi_eta rho Phi` source term
- mechanism-separation and non-claim gates are now landed; current locked-chi
  rows remain `CLAIM_SURFACE_BLOCKED` until selector/source locking passes

## Agent Workstreams

Exploration agents were launched on these independent paths:

| path | agent | immediate question |
|---|---|---|
| selector theorem / no-go | Ampere | Is there a native `Z2` branch operator that can host `chi_g`? |
| signed source density | Jason | Can a signed gravitational source be a scalar bilinear while inertial mass stays positive? |
| superselection / mixing | Anscombe | Is `chi_g` conserved under retained dynamics and deformations? |
| full two-packet dynamics | Godel | Does the locked sign survive real packet evolution, not just algebraic force balance? |
| family portability | Gibbs | Does the four-pair locked table survive actual retained graph/lattice families? |
| lensing / complex-action quarantine | Archimedes | Which AWAY regimes must be quarantined from signed-gravity claims? |

The sections below are the branch backlog. Agent findings should be folded into
the same sections rather than creating competing lane notes.

## P0: Selector Theorem Or No-Go

**Goal:** decide whether `chi_g` can be native or naturally hosted, rather than
inserted as a free phenomenological sign.

Candidate target:

```text
Q_chi^2 = 1
[Q_chi, H_retained] = 0 or controlled superselection residual
Q_chi maps the gravitational scalar source branch as chi_g = +/-1
```

Proposed artifacts:

- `scripts/frontier_signed_gravity_chi_selector_algebra.py`
- `docs/SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md`

First result:

- [`../scripts/frontier_signed_gravity_chi_selector_algebra.py`](../scripts/frontier_signed_gravity_chi_selector_algebra.py)
  scans all non-identity local Pauli-string involutions on the 8D KS taste
  cell
- `SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md` (sibling artifact;
  cross-reference only — not a one-hop dep of this note)
  records the first local/taste-cell no-go
- strict selector candidates found: `0`
- conserved neutral taste labels found: `IXY`, `XYI`, `XZY`
- scalar-sign-pinning `epsilon = ZZZ` is kinetic-broken
- `i Omega` is kinetic-conserved but broken by the parity-scalar mass/coupling

Initial scan set:

- site parity `epsilon(x)`
- staggered taste parity / even-odd taste projectors
- `Cl(3)` grade involution
- central pseudoscalar orientation
- CP and CPT-related involutions from the free staggered theorem
- residual `Z2` stabilizers already used in the matter-source lanes

Acceptance gates:

- finds a nontrivial involution with eigenvalues `+/-1`
- prints Hermiticity/unitarity, `Q_chi^2 = I`, sector dimensions, and
  projectors `P_+`, `P_-`
- branch is not just a relabeling of ordinary positive density
- candidate commutes with the retained free Hamiltonian, or the noncommuting
  part is exactly identified as the sector-breaking term
- projector leakage `||P_- U(t) P_+||` is exactly zero on the retained free
  surface, or the script prints `NO_GO`
- candidate has a clean CPT transform law on even periodic lattices
- candidate has a scalar-density transform law that can lock source and
  response signs as one label
- candidate naturally couples to the parity-correct scalar response channel
- no negative inertial mass is introduced

No-go condition:

- every candidate either fails conservation, fails to source a sign, collapses
  to gauge/relabeling freedom, or breaks the retained scalar coupling surface
- positive-source no-go: variational sourcing remains forced to
  `rho = |psi|^2 >= 0`
- parity/taste relabel no-go: the candidate is only a basis or gauge/taste
  relabeling, not a superselected physical branch
- CPT no-go: the sign is CPT-odd in a way that breaks exact retained CPT or
  requires odd-lattice/parity failure
- scalar-only overreach no-go: a scalar signed response cannot be promoted to
  full tensor gravity; cite
  [`SCALAR_TRACE_TENSOR_NO_GO_NOTE.md`](SCALAR_TRACE_TENSOR_NO_GO_NOTE.md)

## P0: Signed Source-Density Audit

**Goal:** test whether a signed gravitational source can exist without
abandoning positive Born density or positive inertial mass.

Proposed artifacts:

- `scripts/gravity_chi_source_density_audit.py`
- `scripts/frontier_signed_gravity_source_variational_audit.py`
- `scripts/signed_source_unit_normalization_audit.py`
- `scripts/neutral_pair_farfield_audit.py`
- `docs/GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md`

First result:

- [`../scripts/frontier_signed_gravity_source_variational_audit.py`](../scripts/frontier_signed_gravity_source_variational_audit.py)
  identifies the scalar-coupling variational source:
  `delta E / delta Phi = response_sign * epsilon|psi|^2`
- `GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md` (downstream consumer
  artifact derived from this backlog; cross-reference only — that note
  cites `chi_selector` as its predecessor, not vice versa)
  records the local source-primitive block
- positive Born/inertial density remains clean, with normalized packet Born
  charge `1.000000`
- the parity scalar source is signed, but a one-site translation flips it:
  at `sigma = 0.65`, the scalar charges are `+6.841826e-01` and
  `-6.841826e-01`
- the parity scalar source is not conserved by retained free evolution:
  `+4.233389e-02 -> +5.457125e-02`, with norm drift `2.354e-14`
- the parity scalar monopole washes out under refinement:
  `+4.953538e-01`, `+7.762077e-03`, `+4.537555e-10`,
  `-4.163336e-17` for `h = 1.0, 0.5, 0.25, 0.125`
- conserved neutral taste labels `IXY`, `XYI`, and `XZY` have
  `epsilon` spectrum `[-1,+1]` with mean `0` in both branches, so they do not
  pin scalar source sign
- `epsilon = ZZZ` pins scalar sign but is not conserved
- source-unit normalization can represent an already supplied sign through
  `q_bare = 4 pi chi_g M_phys`, with `F~M` slope `1.000000`, null source
  zero, and same-point inserted `+/-` cancellation, but it does not derive
  `chi_g`

Candidate source forms to audit:

```text
rho_g = chi_g * m * |psi|^2
rho_g = m * <psi | Q_chi | psi>
rho_g = m * (|P_+ psi|^2 - |P_- psi|^2)
rho_inertial = m * <psi | psi>
```

Acceptance gates:

- `rho_inertial > 0` for both branches
- signed source is computed from a local scalar/taste-parity bilinear or
  projector expectation, not passed as a free multiplier
- source-check `delta E / delta Phi` identifies whether the parity-correct
  scalar coupling actually sources the signed bilinear
- same-branch source sign is stable under normalization and phase changes
- neutral same-point `+/-` source cancellation works
- neutral or near-neutral far-field audit cancels the monopole while keeping
  positive additive inertial mass/norm
- null-field and zero-branch controls reduce exactly
- self-source does not create an unbounded negative-energy runaway
- source law is linear in branch population in the weak-field regime
- source-unit normalization remains compatible with
  [`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md):
  bare kernel normalization and physical source units must not be conflated

Failure modes to explicitly record:

- signed density is only a hand-inserted external charge
- branch-projected density is not conserved
- the sign also flips inertial mass
- mixed branch superpositions make source sign basis-dependent
- source-unit normalization regresses to labeling `G_kernel = 1/(4 pi)` as the
  physical `G_Newton`
- neutral signed pairs leave an unphysical residual monopole

## P0: Nonlocal / Boundary `chi_g` Targets

**Goal:** after the local/taste-cell and source-primitive blocks, test whether
`chi_g` can be hosted by a boundary, index, holonomy, or global projector
sector rather than by a local Pauli/taste label.

Artifacts:

- `SIGNED_GRAVITY_NONLOCAL_BOUNDARY_CHI_TARGET_NOTE.md` (downstream consumer
  artifact derived from this backlog; cross-reference only — that probe
  cites this backlog and `chi_selector` as its predecessors, not vice versa)
- [`../scripts/signed_gravity_boundary_coframe_chi_probe.py`](../scripts/signed_gravity_boundary_coframe_chi_probe.py)
- [`SIGNED_GRAVITY_BOUNDARY_COFRAME_CHI_PROBE_NOTE.md`](SIGNED_GRAVITY_BOUNDARY_COFRAME_CHI_PROBE_NOTE.md)
- [`../scripts/signed_gravity_aps_boundary_index_probe.py`](../scripts/signed_gravity_aps_boundary_index_probe.py)
- `SIGNED_GRAVITY_APS_BOUNDARY_INDEX_CHI_PROBE_NOTE.md` (downstream consumer
  artifact derived from this backlog; cross-reference only — that probe
  cites this backlog and `chi_selector` as its predecessors, not vice versa)
- [`../scripts/signed_gravity_aps_wald_gauss_bridge_audit.py`](../scripts/signed_gravity_aps_wald_gauss_bridge_audit.py)
- `SIGNED_GRAVITY_APS_WALD_GAUSS_BRIDGE_AUDIT_NOTE.md` (downstream consumer
  audit derived from this backlog; cross-reference only — that audit cites
  this backlog as its source target, not vice versa)
- [`../scripts/signed_gravity_aps_locked_source_action_proposal.py`](../scripts/signed_gravity_aps_locked_source_action_proposal.py)
- `SIGNED_GRAVITY_APS_LOCKED_SOURCE_ACTION_PROPOSAL_NOTE.md` (downstream
  consumer artifact derived from this backlog; cross-reference only — that
  proposal cites the bridge audit as its predecessor, not vice versa)
- [`../scripts/signed_gravity_aps_action_origin_superselection_stability_audit.py`](../scripts/signed_gravity_aps_action_origin_superselection_stability_audit.py)
- `SIGNED_GRAVITY_APS_ACTION_ORIGIN_SUPERSELECTION_STABILITY_NOTE.md`
  (downstream consumer artifact derived from this backlog; cross-reference
  only — that audit cites the locked-source-action proposal as its
  predecessor, not vice versa)
- [`../scripts/signed_gravity_retained_boundary_source_principle_nogo.py`](../scripts/signed_gravity_retained_boundary_source_principle_nogo.py)
- `SIGNED_GRAVITY_RETAINED_BOUNDARY_SOURCE_PRINCIPLE_NO_GO_NOTE.md`
  (downstream consumer artifact derived from this backlog; cross-reference
  only — that no-go cites the action-origin audit as its predecessor, not
  vice versa)
- [`../scripts/signed_gravity_aps_locked_axiom_extension_audit.py`](../scripts/signed_gravity_aps_locked_axiom_extension_audit.py)
- `SIGNED_GRAVITY_APS_LOCKED_AXIOM_EXTENSION_NOTE.md` (downstream consumer
  artifact derived from this backlog; cross-reference only — that extension
  cites the boundary-principle no-go as its predecessor, not vice versa)
- [`../scripts/signed_gravity_source_line_origin_tensor_lift_audit.py`](../scripts/signed_gravity_source_line_origin_tensor_lift_audit.py)
- [`SIGNED_GRAVITY_SOURCE_LINE_ORIGIN_TENSOR_LIFT_NOTE.md`](SIGNED_GRAVITY_SOURCE_LINE_ORIGIN_TENSOR_LIFT_NOTE.md)
- [`../scripts/signed_gravity_source_character_uniqueness_theorem.py`](../scripts/signed_gravity_source_character_uniqueness_theorem.py)
- [`SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md`](SIGNED_GRAVITY_SOURCE_CHARACTER_UNIQUENESS_THEOREM_NOTE.md)
- [`../scripts/signed_gravity_cl3z3_source_character_derivation.py`](../scripts/signed_gravity_cl3z3_source_character_derivation.py)
- [`SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md`](SIGNED_GRAVITY_CL3Z3_SOURCE_CHARACTER_DERIVATION_NOTE.md)
- [`../scripts/signed_gravity_nature_grade_closure_blockers.py`](../scripts/signed_gravity_nature_grade_closure_blockers.py)
- [`SIGNED_GRAVITY_NATURE_GRADE_CLOSURE_BLOCKER_AUDIT_NOTE.md`](SIGNED_GRAVITY_NATURE_GRADE_CLOSURE_BLOCKER_AUDIT_NOTE.md)
- [`../scripts/signed_gravity_boundary_z2_flux_probe.py`](../scripts/signed_gravity_boundary_z2_flux_probe.py)
- [`SIGNED_GRAVITY_BOUNDARY_Z2_FLUX_CHI_PROBE_NOTE.md`](SIGNED_GRAVITY_BOUNDARY_Z2_FLUX_CHI_PROBE_NOTE.md)
- [`../scripts/signed_gravity_nonlocal_projector_charge_probe.py`](../scripts/signed_gravity_nonlocal_projector_charge_probe.py)
- `SIGNED_GRAVITY_NONLOCAL_PROJECTOR_CHARGE_CHI_PROBE_NOTE.md` (downstream
  consumer artifact derived from this backlog; cross-reference only — that
  probe cites `chi_selector` and the boundary-target as its predecessors,
  not vice versa)
- [`SIGNED_GRAVITY_SOURCE_ACTION_ESCAPE_HATCH_NOTE.md`](SIGNED_GRAVITY_SOURCE_ACTION_ESCAPE_HATCH_NOTE.md)

First result table:

| candidate | result tag | what survives | blocker |
|---|---|---|---|
| primitive boundary coframe orientation | `BOUNDARY_CHI_SOURCE_NOT_LOCKED` | conserved boundary `Z2` chirality on even coframe dynamics; positive inertial mass, Born, norm, null, and source-unit controls pass | no boundary action/Gauss identity tying `Q_chi` to both exterior active monopole and response sign |
| APS / spectral-asymmetry boundary index | `APS_WALD_GAUSS_BRIDGE_NOT_DERIVED` | eta-sign is basis-invariant, gap-stable, and changes only at zero crossing in the finite probe | eta is source-neutral under gap-preserving variations; retained Wald/Gauss source scale is positive and unsigned; locked table only passes as inserted source action |
| boundary `Z2` holonomy / flux | `BOUNDARY_CHI_SOURCE_NOT_LOCKED` | conditional conserved label on restricted holonomy-preserving local algebra; topology and sector-breaking controls fail loudly | native Wilson-loop flux is source-neutral; source locking only works as inserted charge |
| nonlocal projector-difference charge | `NONLOCAL_PROJECTOR_FORMAL_CONTROL_ONLY` | imposed global sectors pass formal conservation, leakage, Born, norm, null, source-unit, and locked-consequence controls | scalar-source pinning fails; signed source appears only after adding a projector-source action; mixed/basis-rotated states are ambiguous |

Source-action escape-hatch result:

- retained Poisson/Born source remains stable, positive, and unsigned
- parity scalar variational source is signed and native, but blocked by branch
  instability and nonconservation
- inserted signed charge remains a useful control only
- no escape hatch is immediately viable without a genuinely new action that
  derives conserved branch-fixed `chi_g`, keeps inertial mass positive, and
  locks source and response

APS bridge audit:

- [`../scripts/signed_gravity_aps_wald_gauss_bridge_audit.py`](../scripts/signed_gravity_aps_wald_gauss_bridge_audit.py)
  returns `FINAL_TAG: APS_WALD_GAUSS_BRIDGE_NOT_DERIVED`
- gap-preserving `Phi` deformation leaves eta source-neutral:
  `d_eta/dPhi = 0`
- eta changes sign only through an explicit zero-crossing boundary defect
- the primitive Wald/Gauss/source-unit scale remains positive:
  `c_cell = 1/4`, `lambda = 1`, `C_abs = M_phys`
- putting `chi` into the Wald coefficient is rejected because the `chi=-1`
  branch would have a negative area coefficient
- retained positive source gives all-pair attraction; APS spectator gives zero
  active source; source-only and response-only insertions fail mixed-pair
  balance; only locked insertion gives the desired four-pair table

APS-locked source action proposal:

- [`../scripts/signed_gravity_aps_locked_source_action_proposal.py`](../scripts/signed_gravity_aps_locked_source_action_proposal.py)
  and
  [`SIGNED_GRAVITY_APS_LOCKED_SOURCE_ACTION_PROPOSAL_NOTE.md`](SIGNED_GRAVITY_APS_LOCKED_SOURCE_ACTION_PROPOSAL_NOTE.md)
  define the smallest action that would close the APS source/response gap:

  ```text
  S_int[Phi,psi,Y] = - chi_eta(Y) M_phys sum_x |psi_x|^2 Phi_x
  chi_eta(Y) = sign eta_delta(D_Y)
  ```

- variation gives the desired active source:
  `rho_active = chi_eta M_phys |psi|^2`
- the positive Wald/area carrier remains unsigned:
  `c_cell = +1/4`, `lambda = 1`
- source-unit normalization consumes the proposed sign:
  `q_bare = 4 pi chi_eta M_phys`
- the locked four-pair table passes:
  `++` and `--` attract; `+-` and `-+` repel
- Born, norm, null, and positive inertial mass controls pass in the finite
  harness
- status is conditional only: this is a new source-action premise unless a
  separate APS/Wald/Gauss derivation is supplied

Origin / superselection / stability audit:

- [`../scripts/signed_gravity_aps_action_origin_superselection_stability_audit.py`](../scripts/signed_gravity_aps_action_origin_superselection_stability_audit.py)
  returns `FINAL_TAG: APS_LOCKED_ACTION_CONDITIONAL_NOT_RETAINED`
- retained separable APS/Wald/Gauss terms span positive source
  `[+1,+1]` plus source-neutral terms; they cannot produce the signed source
  `[+1,-1]` without adding the `chi_eta rho Phi` cross term
- adding the proposed cross term solves the finite source basis exactly, so the
  action is a precise target but not retained
- eta is stable under sampled gap-preserving perturbations, but flips through
  an explicit zero-crossing defect if the gap is not protected
- locked positive-inertial-mass signs avoid the negative-mass runaway control
  and keep two-body force balance; ordinary same-sector short-distance
  gravitational collapse remains a UV/core or constraint issue

Retained boundary source-principle audit:

- [`../scripts/signed_gravity_retained_boundary_source_principle_nogo.py`](../scripts/signed_gravity_retained_boundary_source_principle_nogo.py)
  returns `FINAL_TAG: RETAINED_BOUNDARY_SOURCE_PRINCIPLE_NO_GO`
- retained source-current basis over eta sectors:
  `[+1,+1]` from positive Born/Gauss source and `[0,0]` from APS spectator /
  positive Wald terms
- target signed source is `[+1,-1]`; least-squares residual in the retained
  basis is `1.414e+00`
- adding the `chi_eta rho Phi` cross term spans the target exactly, so that
  term is a new orientation-odd coupling
- continuous APS paths between eta sectors cross the zero mode; finite gap
  penalties are not superselection, and a hard gap rule is a new admissibility
  constraint

Current read:

- the APS boundary-index route remains the cleanest boundary label, but its
  current source-response bridge is now audited negative on the retained
  Wald/Gauss stack
- the proposed APS-locked action is the cleanest concrete target, but not a
  retained theorem
- coframe and `Z2` flux are useful boundary labels but are presently blocked at
  source locking
- projector-difference charge is a formal control unless an independent
  boundary/global constraint fixes the projectors and derives the source action
- the only useful APS continuation is now to derive or no-go the proposed
  action term, not another source-unit or phenomenology sweep
- after the origin audit, the target is narrower still: derive the new cross
  term from a retained boundary source principle, or classify the lane as a
  no-go/control packet
- the retained boundary source-principle audit lands the latter for the current
  stack: no retained derivation of `chi_eta rho Phi` or APS gap protection is
  in hand

## P0: Superselection And Mixing

**Goal:** determine whether `chi_g` is a conserved branch label or an unstable
basis choice.

Proposed artifacts:

- `scripts/gravity_chi_superselection_probe.py`
- `scripts/chi_g_selector_conservation_probe.py`
- `scripts/frontier_signed_gravity_interacting_conservation.py`
- `docs/GRAVITY_CHI_SUPERSELECTION_BOUNDARY_NOTE.md`

Tests:

- free staggered evolution: measure leakage between `Q_chi` sectors
- free commutator: classify `[H_free, Q_chi] = 0`, exact anticommutation, or
  spectral-flip cases rather than hiding them in a scalar residual
- parity-correct scalar coupling: verify whether the sector is preserved by
  `H_diag = (m + Phi) epsilon(x)`
- external weak-field perturbations: identify branch-preserving versus
  branch-mixing perturbations
- graph deformation: test whether the label survives open cubic, periodic
  cubic, irregular, layered, and grown families
- graph defects: odd cycles, parity-wrap defects, dense shortcuts, and
  high-degree contamination should fail loudly as structural breaks if the
  branch depends on bipartite/taste parity
- interaction insertion: identify whether gauge or mass terms break the branch
- interaction mixing: test matrix elements `<chi=-|V_int|chi=+>` for
  taste-isotropic scalar, gauge-only, CKM-like complex phases, and generic
  taste off-diagonal terms

Acceptance gates:

- leakage is zero or parametrically controlled on the retained surface
- any allowed sector-breaking term is already known and bounded
- branch conservation is independent of packet shape and global phase
- branch label does not depend on an arbitrary basis choice
- external fields can alter trajectories but cannot induce `P_+ <-> P_-`
  transitions unless they contain an explicitly sector-breaking operator
- graph defects are classified as `Q_chi UNDEFINED` or `STRUCTURAL BREAK`, not
  as silent portability positives

No-go condition:

- generic retained dynamics mixes `+` and `-` at leading order
- the protected class is only free/scalar and fails once admissible retained
  interactions are included

## P1: Full Two-Packet Dynamics

**Goal:** replace the algebraic pair table with real branch-labeled packet
dynamics in a shared signed Poisson field.

Proposed artifacts:

- `scripts/signed_gravity_two_packet_dynamics.py`
- `scripts/signed_gravity_center_of_mass_control.py`
- `scripts/signed_two_packet_action_reaction_dynamics.py`
- `scripts/signed_midplane_flux_balance.py`
- `scripts/signed_scattering_deflection.py`
- `scripts/signed_finite_size_dt_sigma_sweep.py`
- `docs/SIGNED_GRAVITY_TWO_PACKET_DYNAMICS_NOTE.md`

Minimum model:

```text
(L + mu^2 I) Phi = sum_a chi_a m_a |psi_a|^2
H_a = H0 + scalar_response(chi_a Phi_partner)
```

Acceptance gates:

- `++` and `--` packets move inward relative to self-only controls
- `+-` and `-+` packets move outward relative to self-only controls
- center-of-mass or momentum proxy is conserved in the locked sector
- integrated partner impulses `I_A = integral F_A dt` and
  `I_B = integral F_B dt` satisfy an action-reaction residual below `1e-3`
  on the first pass, with a tighter target if numerics permit
- source-only and response-only controls fail or are explicitly rejected
- norm drift stays at numerical precision
- positive kinetic/inertial mass proxy is unchanged by branch sign
- no runaway appears over the short-time weak-field window
- mass slopes are near `1.00 +/- 0.05` with `R^2 > 0.98`
- distance exponent is near `-2.0 +/- 0.2` on calibrated open bulk rows
- center-of-mass drift remains below `1%` of the relative displacement
- results are stable under A/B swap, left/right reflection, parity placement,
  finite-size growth, and `dt` refinement

Observables:

- exact partner-force where available
- integrated impulses `I_A`, `I_B`
- midplane flux or stress-balance proxy
- blocked centroid/envelope shift on staggered lattices
- momentum proxy `m * delta_centroid`
- total center-of-mass drift
- field energy proxy and source-response work sign
- solver residual, energy drift, and branch leakage

## P1: Actual-Family Portability

**Goal:** move beyond analytic kernel portability and test the locked four-pair
table on existing retained surfaces.

Proposed artifacts:

- `scripts/signed_gravity_family_portability_sweep.py`
- `scripts/signed_gravity_graph_portability.py`
- `scripts/signed_gravity_graph_portability_stress.py`
- `scripts/signed_gravity_irregular_core_packet_gate.py`
- `scripts/signed_gravity_architecture_portability_sweep.py`
- `scripts/signed_gravity_electrostatics_comparator.py`
- `docs/SIGNED_GRAVITY_FAMILY_PORTABILITY_NOTE.md`
- `docs/SIGNED_GRAVITY_GRAPH_PORTABILITY_NOTE.md`
- `docs/SIGNED_GRAVITY_GRAPH_PORTABILITY_STRESS_NOTE.md`
- `docs/SIGNED_GRAVITY_IRREGULAR_CORE_PACKET_GATE_NOTE.md`
- `docs/SIGNED_GRAVITY_ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md`
- `docs/SIGNED_GRAVITY_ELECTROSTATICS_COMPARATOR_NOTE.md`

Target families:

- open 3D staggered cubic
- periodic staggered cubic
- bipartite random-geometric irregular graph
- bipartite growing graph
- layered bipartite DAG-compatible graph
- graph stress families from the retained staggered graph-portability stress
  surface
- irregular core-packet gate families at `G = 5, 10` and
  `mu2 = 0.1, 0.001`
- architecture rows from the existing architecture-portability sweep
- retained grown row from the electrostatics sign-law lane
- one architecture-portability holdout if runtime is acceptable

Acceptance gates:

- locked signs preserve the four-pair orientation table on each passing family
- source-only and response-only remain controls
- null-field, neutral same-point cancellation, and `F~M` checks pass
- graph baseline: positive inertial mass, norm `< 1e-10`, `F~M R^2 > 0.9`,
  achromatic/equivalence coefficient of variation below the existing family
  thresholds where those readouts exist
- irregular core-packet replay: at least `80%` positive separation at both
  screening levels, with ball1, ball2, and depth margins agreeing
- architecture sweep: signed direction table correct on every architecture
  where direction is meaningful; Born `I3 < 1e-6` where measured
- electrostatics comparator: zero-source cancellation, neutral same-point
  cancellation, plus/minus antisymmetry, unit weak-field slope, and locked
  action-reaction
- family failures are classified by observable failure, graph topology, or
  branch non-portability rather than hidden sign convention

Known blockers:

- current portability is only analytic-kernel portability, not actual graph or
  architecture portability
- current signed harness has no graph-native signed source primitive
- irregular graph directional observables are proxy-sensitive
- lensing and complex-action AWAY regimes are not conservative sign sectors
- raw staggered centroids can alias sublattice beating
- electrostatics starts with signed source charge by construction; gravity
  still needs a signed scalar-density source primitive

## P1: Lensing And Complex-Action Quarantine

**Goal:** prevent phase-interference and absorptive AWAY results from being
mistaken for signed gravitational response.

Proposed artifacts:

- `docs/SIGNED_GRAVITY_MECHANISM_SEPARATION_NOTE.md`
- `docs/SIGNED_GRAVITY_NON_CLAIM_GATE_NOTE.md`
- `docs/SIGNED_GRAVITY_LENSING_PHASE_QUARANTINE_NOTE.md`
- `docs/SIGNED_GRAVITY_COMPLEX_ACTION_QUARANTINE_NOTE.md`
- `scripts/signed_gravity_mechanism_separator.py`
- `scripts/lensing_phase_quarantine_audit.py`
- `scripts/complex_action_absorptive_quarantine_audit.py`
- optional `scripts/signed_gravity_quarantine_regression.py`

First result:

- `SIGNED_GRAVITY_MECHANISM_SEPARATION_NOTE.md` (downstream consumer artifact
  derived from this backlog; cross-reference only — that note cites
  `chi_selector` as its predecessor, not vice versa)
  and [`SIGNED_GRAVITY_NON_CLAIM_GATE_NOTE.md`](SIGNED_GRAVITY_NON_CLAIM_GATE_NOTE.md)
  are landed
- [`../scripts/signed_gravity_mechanism_separator.py`](../scripts/signed_gravity_mechanism_separator.py)
  classifies rows as `locked_chi_response`, `lensing_phase_flip`,
  `complex_absorptive_away`, `boundary/proxy`, or `inserted_control_no_go`
- current locked-chi rows are `CLAIM_SURFACE_BLOCKED` because
  `NO_GO_STRICT_SELECTOR` and `SOURCE_PRIMITIVE_BLOCKED_LOCAL` still stand
- lensing AWAY is `LENSING_PHASE_ONLY`
- complex-action AWAY is `COMPLEX_ABSORPTIVE_ONLY`
- inserted signs are `CONTROL_NO_GO`

Lensing boundary:

- lensing sign flips depend on `k*h` and phase windows
- sign-clean rows may exist, but they are not selector evidence
- a `chi_g` claim must use conservative source/response locking and
  action-reaction gates, not lensing centroid sign alone

Complex-action boundary:

- AWAY behavior at large `gamma` is absorptive path selection
- nonunitary/absorptive escape changes are not conservative repulsive gravity
- Born can remain clean for linear nonunitary propagation, so Born cleanliness
  alone does not identify a physical signed-gravity sector

Acceptance gates:

- separation notes cite the actual phase/complex-action scripts
- every future AWAY row declares one mechanism bucket before interpretation:
  `locked_chi_response`, `lensing_phase_flip`, `complex_absorptive_away`,
  `boundary/proxy`, or `control_no_go`
- each AWAY mechanism is classified as conservative, absorptive, interference,
  boundary, or proxy artifact
- signed-response promotion requires locked two-body closure, not one-body
  deflection
- scripts print regression tags such as `SIGNED_RESPONSE_CANDIDATE`,
  `LENSING_PHASE_ONLY`, `COMPLEX_ABSORPTIVE_ONLY`, `CONTROL_NO_GO`, or
  `CLAIM_SURFACE_BLOCKED`
- no signed-gravity claim may cite
  [`LENSING_K_SWEEP_NOTE.md`](LENSING_K_SWEEP_NOTE.md),
  [`../scripts/lensing_sign_phase_diagram.py`](../scripts/lensing_sign_phase_diagram.py),
  or [`COMPLEX_ACTION_NOTE.md`](COMPLEX_ACTION_NOTE.md) as positive `chi_g`
  evidence before a native selector theorem passes

## P2: Continuum And Renormalization Sanity

**Goal:** test whether the branch survives refinement as more than a finite-grid
parameter artifact.

Proposed artifacts:

- `scripts/signed_gravity_refinement_sweep.py`
- `docs/SIGNED_GRAVITY_REFINEMENT_SANITY_NOTE.md`

Acceptance gates:

- sign table is invariant across `h`
- magnitude approaches the expected kernel law under refinement
- branch leakage does not grow under refinement
- weak-field `F~M` remains near one
- null-field and neutral controls remain exact or improve

## P2: Claim-Surface Guardrails

**Goal:** keep the discovery lane from leaking into the manuscript package as a
claim before the selector theorem is settled.

Proposed artifact:

- update the science map or frontier lane note only after P0 closes
- optionally add `docs/CHI_G_NATIVE_SELECTOR_THEOREM_TARGET_NOTE.md` as a
  target statement before any theorem/no-go result is promoted

Promotion checklist:

- native `chi_g` origin
- `chi_g` conservation or protected superselection
- source/response locking by one label
- two-body action-reaction in algebraic and dynamical harnesses
- positive inertial mass
- Born, norm, null-field, and `F~M` controls
- continuum/refinement and actual-family portability
- explicit quarantine from lensing and complex-action AWAY rows

Allowed wording before P0 closes:

> The framework has a coherent signed-response consequence harness if a native
> locked branch label exists.

Forbidden wording before P0 closes:

> The framework predicts antigravity.

> Negative gravitational mass exists.

> Gravity can be shielded, switched, or used for propulsion.

## Immediate Next Moves

1. Treat the local/taste-cell selector route as provisionally blocked by
   `NO_GO_STRICT_SELECTOR`.
2. Treat the local source-primitive route as provisionally blocked by
   `SOURCE_PRIMITIVE_BLOCKED_LOCAL`.
3. Treat primitive coframe and boundary `Z2` flux as conserved-label positives
   but source-locking blocks, both tagged `BOUNDARY_CHI_SOURCE_NOT_LOCKED`.
4. Treat nonlocal projector charge as `FORMAL_CONTROL_ONLY` unless an
   independent boundary/global constraint fixes the projectors and derives the
   source action.
5. Treat the APS boundary-index route as the best boundary label but not a
   signed active-source theorem: the first APS/Wald/Gauss bridge audit returns
   `APS_WALD_GAUSS_BRIDGE_NOT_DERIVED`.
6. Keep the mechanism-separation and non-claim gates mandatory for every AWAY
   row; current claim surface remains blocked.
7. Treat the APS-locked action
   `S_int = -chi_eta M_phys <|psi|^2,Phi>` as the current conditional target:
   it passes the finite proposal harness but is not derived.
8. Treat the origin/superselection/stability audit as a conditional no-go for
   the current retained stack: the action requires a new `chi_eta rho Phi`
   cross term and a protected APS gap.
9. Continue to defer broad family portability and phenomenology until an active
   source/response-locked `chi_g` theorem candidate exists.
10. Treat the current retained boundary source-principle route as blocked by
    `RETAINED_BOUNDARY_SOURCE_PRINCIPLE_NO_GO`.
11. Treat the eta-polarized source-line package as the current genuinely new
    axiom candidate: `APS_LOCKED_AXIOM_EXTENSION_CONTROLLED_CANDIDATE`.
12. Treat the determinant-orientation source-line pass as the current origin
    theorem target: `ETA_SOURCE_LINE_ORIGIN_CONDITIONAL_A1_TENSOR_LIFT`.
13. Treat the source-character uniqueness theorem as the strongest current
    breakthrough result:
    `ETA_SOURCE_CHARACTER_UNIQUENESS_THEOREM_A1_MAXIMAL`.
14. Treat the finite original-stack determinant-line result as a strong host
    result, not a canonical selector theorem:
    `CL3Z3_DETERMINANT_SOURCE_CHARACTER_DERIVED_FINITE`.
15. Treat the nature-grade blocker audit as the current closure boundary:
    `SIGNED_GRAVITY_NATURE_GRADE_HARD_BLOCKERS_REDUCED_CONDITIONALS_REMAIN`.
16. Treat the oriented tensor-source lift as the finite conditional resolution
    of the `A1` tensor blocker:
    `SIGNED_GRAVITY_ORIENTED_TENSOR_SOURCE_LIFT_FINITE_CONDITIONAL`.
17. Treat tensor-source transport/retention as finite-positive but nonlinear
    gated:
    `SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_FINITE_CONDITIONAL`.
18. Treat chosen-continuum transport plus graded nonlinear localization as a
    formal local theorem:
    `SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FORMAL_THEOREM`.
    The remaining tensor-side escalation is global nonlinear PDE
    existence/uniqueness only if the lane needs global dynamics.
19. Treat the remaining nature-grade blockers as precise conditionals:
    `SIGNED_GRAVITY_REMAINING_GATES_REDUCED_TO_PRECISE_CONDITIONALS`.
    The next true blockers are retained orientation-line APS extraction on
    graph families, physical sector preparation or demotion, and a real global
    stability mechanism beyond pair softening.
20. Treat native raw boundary-complex containment as negative:
    `SIGNED_GRAVITY_NATIVE_BOUNDARY_COMPLEX_APS_LINE_NOT_CONTAINED`.
    The determinant-orientation grammar remains finite/conditional at the
    functor level, but the actual raw cochain/Hodge boundary complex does not
    contain the orientation-line APS source character.
21. Treat retained-compatible staggered-Dirac boundary realization as
    negative:
    `SIGNED_GRAVITY_STAGGERED_DIRAC_APS_REALIZATION_NOT_CONTAINED`.
    Odd open-face eta and Pfaffian signs are controls, not admissible
    selectors.
22. Treat determinant-line orientation hosting as real but not a selector:
    `SIGNED_GRAVITY_ORIENTATION_LINE_NATURALLY_HOSTED_NOT_CANONICALLY_SELECTED`.
    Future promotion requires a retained canonical section/source theorem;
    otherwise the source-line package stays a controlled extension or no-go
    boundary package.
23. Keep this lane away from any physical signed-gravity claim unless the
    finite derivation is lifted to a continuum determinant-line theorem,
    realized on the actual retained graph/lattice gravity families, extended
    through a retained tensor-source theorem, and hardened by
    dynamics/sector-preparation plus ordinary UV/core stability arguments.
