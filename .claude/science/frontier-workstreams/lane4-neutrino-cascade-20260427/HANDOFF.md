# Handoff

## Loop 3 Checkpoint 2026-04-29T04:27Z

Supervisor loop 3 continued Lane 5 `(C1)` after the A4 parity-gate boundary.
The selected route was the direct `P_A` module-morphism / Boolean-coframe
restriction attempt.

### Claim-State Movement This Checkpoint

Added a new exact negative boundary:

- `docs/HUBBLE_LANE5_C1_A5_BOOLEAN_COFRAME_RESTRICTION_OBSTRUCTION_NOTE_2026-04-29.md`
- `scripts/frontier_hubble_lane5_c1_a5_boolean_coframe_restriction_obstruction.py`
- `logs/2026-04-29-hubble-lane5-c1-a5-boolean-coframe-restriction-obstruction.txt`

Verified result: the natural full-cell Boolean/Jordan-Wigner odd coframe
generators obey `Cl_4` on `H_cell=(C^2)^4`, but they change Hamming weight.
The Hamming-weight-one `P_A` packet is therefore not a reducing submodule:

```text
P_A Gamma_i P_A = 0,
[P_A, Gamma_i] != 0.
```

Direct compression cannot supply the active-block metric-compatible coframe
response. The intrinsic active-block `Cl_4` response remains possible, but it
must be derived by a different theorem or kept conditional.

### Verification

- `PYTHONPATH=scripts python3 scripts/frontier_hubble_lane5_c1_a5_boolean_coframe_restriction_obstruction.py`
  -> `PASS=9 FAIL=0`
- `python3 -m py_compile scripts/frontier_hubble_lane5_c1_a5_boolean_coframe_restriction_obstruction.py`
  -> pass
- `PYTHONPATH=scripts python3 scripts/frontier_planck_target3_clifford_phase_bridge.py`
  -> `PASS=34 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_planck_primitive_coframe_boundary_carrier.py`
  -> `PASS=14 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_planck_finite_response_nogo.py`
  -> `7/7 checks passed`
- `bash docs/audit/scripts/run_pipeline.sh`
  -> complete
- `python3 docs/audit/scripts/audit_lint.py --strict`
  -> OK, known graph-cycle warning only
- `git diff --check`
  -> pass
- Audit row:
  `hubble_lane5_c1_a5_boolean_coframe_restriction_obstruction_note_2026-04-29`
  seeded as `proposed_retained` / `unaudited`.

### Review-Loop Emulation

- Code/runner: PASS. The runner checks the load-bearing direct restriction
  shortcut and distinguishes it from an intrinsic active-block response.
- Physics boundary: exact negative boundary for direct full-cell odd coframe
  restriction only. The Target 3 Clifford bridge remains conditional positive.
- Imports: disclosed in `ASSUMPTIONS_AND_IMPORTS.md`; no observed or SI
  action value is used.
- Repo governance: no repo-wide authority weaving performed. Audit generated
  surfaces were refreshed for parseability only.

### Next Exact Action

Assess a number-preserving bilinear / quotient route that might select an
intrinsic `Cl_4` basis on the one-particle `P_A` sector. If that route fails,
write the minimal carrier/metrology axiom audit and mark Lane 5 `(C1)` as
blocked by human science judgment before pivoting.

## Loop 3 Checkpoint 2026-04-29T04:20Z

Supervisor loop 3 continued Lane 5 `(C1)` after the A2 action-unit
metrology obstruction. The selected route was the A4 parity-gate-to-CAR
stretch attempt.

### Claim-State Movement This Loop

Added a new exact support/boundary theorem:

- `docs/HUBBLE_LANE5_C1_A4_PARITY_GATE_CAR_BOUNDARY_NOTE_2026-04-29.md`
- `scripts/frontier_hubble_lane5_c1_a4_parity_gate_car_boundary.py`
- `logs/2026-04-29-hubble-lane5-c1-a4-parity-gate-car-boundary.txt`

Verified result: the primitive residual `Z_2` parity gate supplies the exact
self-dual half-zone selector and preserves the conditional positive chain

```text
primitive Clifford/CAR coframe response
  => primitive-CAR edge carrier
  + parity gate
  => c_Widom = c_cell = 1/4.
```

But the gate does **not** derive that CAR/coframe response. Its finite gate
algebra is only `span{I, Q_+}` and remains compatible with non-CAR rank-four
semantics. A4 therefore blocks the shortcut:

```text
primitive parity gate + rank(P_A)=4
  => metric-compatible Clifford/CAR coframe response on P_A H_cell.
```

This does not demote the primitive parity-gate carrier theorem, the
primitive-CAR edge theorem, the native-CAR tightening theorem, or the Target 3
Clifford bridge. It only exposes the missing orientation/statistics lift from
the even parity gate to odd Clifford/CAR coframe generators.

### Verification

- `PYTHONPATH=scripts python3 scripts/frontier_hubble_lane5_c1_a4_parity_gate_car_boundary.py`
  -> `PASS=13 FAIL=0`
- `python3 -m py_compile scripts/frontier_hubble_lane5_c1_a4_parity_gate_car_boundary.py`
  -> pass
- `PYTHONPATH=scripts python3 scripts/frontier_area_law_primitive_parity_gate_carrier.py`
  -> `PASS=40 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_area_law_primitive_car_edge_identification.py`
  -> `PASS=36 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_area_law_native_car_semantics_tightening.py`
  -> `PASS=23 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_planck_target3_clifford_phase_bridge.py`
  -> `PASS=34 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_planck_target3_phase_unit_edge_statistics.py`
  -> `27/27 checks passed`
- `bash docs/audit/scripts/run_pipeline.sh`
  -> complete
- `python3 docs/audit/scripts/audit_lint.py --strict`
  -> OK, known graph-cycle warning only
- `git diff --check`
  -> pass
- Audit row:
  `hubble_lane5_c1_a4_parity_gate_car_boundary_note_2026-04-29`
  seeded as `proposed_retained` / `unaudited`.

### Review-Loop Emulation

- Code/runner: PASS. The runner tests the load-bearing A4 shortcut and not
  only the already-known parity-gate coefficient.
- Physics boundary: exact support/boundary. Conditional positive parity-gate
  support is preserved; no `(C1)` or `H_0` closure is claimed.
- Imports: disclosed in `ASSUMPTIONS_AND_IMPORTS.md`; no observed or SI
  action value is used.
- Repo governance: no repo-wide authority weaving performed. Audit generated
  surfaces were refreshed for parseability only.

### Next Exact Action

Continue Lane 5 `(C1)` with a direct `P_A` module-morphism / metric-compatible
coframe theorem attempt, or write the minimal carrier/metrology axiom audit
that records the remaining human-judgment boundary. A4 does not justify
`STOP_ALL_LANES_REQUESTED` by itself.

Fetch note: `origin/main` remains ahead with a broad review batch at
`207760ce`. This loop did not merge it because A4 only needed local Planck /
area-law authorities already present on the cascade branch, and merging would
pull broad unrelated audit-review changes into the science branch.

## Loop 2 Checkpoint 2026-04-29T04:08Z

Supervisor loop 2 continued Lane 5 `(C1)` after the A1 obstruction from loop
1. The selected route was the A2 action-unit metrology stretch attempt.

### Claim-State Movement This Loop

Added a new exact negative boundary:

- `docs/HUBBLE_LANE5_C1_A2_ACTION_UNIT_METROLOGY_OBSTRUCTION_NOTE_2026-04-29.md`
- `scripts/frontier_hubble_lane5_c1_a2_action_unit_metrology_obstruction.py`
- `logs/2026-04-29-hubble-lane5-c1-a2-action-unit-metrology-obstruction.txt`

Verified result: retained `g_bare = 1`, `beta = 6`, plaquette/`u_0`, APBC
hierarchy data, and `c_cell = 1/4` remain dimensionless normalization/support
inputs. They do not choose an absolute dimensional action quantum `kappa` on
`P_A H_cell`; the Target 3 `(S,kappa)` rescaling degeneracy survives.

This does **not** demote the `g_bare` closure, the plaquette support surface,
the APBC/`u_0` hierarchy support theorem, the Target 3 phase-unit boundary, or
the conditional Planck packet. It only blocks the direct A2 shortcut:

```text
g_bare=1 + plaquette/u0 + APBC + c_cell=1/4
  => action-unit metrology on P_A H_cell.
```

### Verification

- `PYTHONPATH=scripts python3 scripts/frontier_hubble_lane5_c1_a2_action_unit_metrology_obstruction.py`
  -> `PASS=8 FAIL=0`
- `python3 -m py_compile scripts/frontier_hubble_lane5_c1_a2_action_unit_metrology_obstruction.py`
  -> pass
- `PYTHONPATH=scripts python3 scripts/frontier_planck_target3_phase_unit_edge_statistics.py`
  -> `PASS=27 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_planck_source_unit_normalization_support_theorem.py`
  -> `PASS=14 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_g_bare_two_ward_closure.py`
  -> `PASS=18 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_hierarchy_spatial_bc_and_u0_scaling.py`
  -> `PASS=8 FAIL=0` with numpy determinant overflow/divide warnings during
  direct determinant stress rows.
- `bash docs/audit/scripts/run_pipeline.sh`
  -> complete
- `python3 docs/audit/scripts/audit_lint.py --strict`
  -> OK, known graph-cycle warning only
- `git diff --check`
  -> pass
- Audit row:
  `hubble_lane5_c1_a2_action_unit_metrology_obstruction_note_2026-04-29`
  seeded as `proposed_retained` / `unaudited`.

### Review-Loop Emulation

- Code/runner: PASS. The new runner checks the load-bearing claim rather than
  only printing constants.
- Physics boundary: exact negative boundary for A2 only. No `(C1)` closure or
  `hbar`/Planck-scale closure is claimed.
- Imports: disclosed in `ASSUMPTIONS_AND_IMPORTS.md`; no observed or SI action
  value is used.
- Repo governance: no repo-wide authority weaving performed.

### Next Exact Action

Continue Lane 5 `(C1)` with **A4 parity-gate-to-CAR audit**. Test whether the
primitive parity-gate carrier route supplies a stronger bridge to native
CAR/coframe response on `P_A H_cell`. If A4 blocks, either attempt a direct
`P_A` module-morphism/coframe theorem or checkpoint Lane 5 as blocked on
human science judgment.

Fetch note: `origin/main` advanced during this loop to `207760ce`. It now
contains the reviewed Hubble `(C1)` residual-premise attack audit; this loop
checked that audit from `origin/main` before finalizing A2. The branch was not
merged with current `origin/main` in this checkpoint because that would pull a
broad unrelated review batch into the cascade branch. Next loop should decide
whether to merge current `origin/main` before A4.

Do **not** create `STOP_ALL_LANES_REQUESTED` yet. A4 remains viable.

## Loop 1 Checkpoint 2026-04-29T03:54Z

This cascade was resumed under the user's 12-hour deadline
`2026-04-29T15:48:24Z`. The branch first merged current `origin/main`
cleanly so the route assessment used the landed Lane 4 physics-loop closeout
and current audit surfaces.

### Claim-State Movement This Loop

1. **Lane 4F Sigma m_nu structural functional form integrated and verified.**
   The unmerged `frontier/neutrino-sigma-mnu-cosmology-20260428` block was
   cherry-picked onto this cascade branch. It adds:
   - `docs/NEUTRINO_LANE4_4F_SIGMA_M_NU_THEOREM_PLAN_NOTE_2026-04-28.md`
   - `docs/NEUTRINO_LANE4_4F_SIGMA_M_NU_FUNCTIONAL_FORM_THEOREM_NOTE_2026-04-28.md`
   - `scripts/frontier_neutrino_lane4_4f_sigma_m_nu_functional_form.py`
   - `docs/NEUTRINO_LANE4_4F_PHASE2_ATTACK_FRAME_FANOUT_NOTE_2026-04-28.md`

   Verified result: structural identity
   `Sigma m_nu = (1 - L - R - Omega_b - Omega_DM) * C_nu * h^2` on the
   retained cosmology bounded surface plus admitted matter-budget/CMB-neutrino
   convention. The runner passes `PASS=4 FAIL=0`. This is not numerical
   retained Sigma m_nu closure because `h`, `Omega_b`, and `Omega_DM` remain
   open/admitted.

2. **Lane 2 reassessed and skipped for lack of a fresh premise.** Current main
   still points to the 2026-04-27 Rydberg dependency firewall. No new retained
   `m_e`, `alpha(0)`/QED-running bridge, or physical-unit nonrelativistic
   limit was found, so Lane 2 remains blocked without a new theorem route in
   this loop.

3. **Lane 5 `(C1)` A1 stretch attempt executed.** Added:
   - `docs/HUBBLE_LANE5_C1_A1_GRASSMANN_BOUNDARY_CAR_OBSTRUCTION_NOTE_2026-04-29.md`
   - `scripts/frontier_hubble_lane5_c1_a1_grassmann_boundary_car_obstruction.py`

   Verified result: exact negative boundary for the direct A1 shortcut. Bulk
   Grassmann/CAR structure plus rank-four support does not force CAR semantics
   on `P_A H_cell`; the descent works only when `P_A` is a reducing
   Clifford/CAR module morphism for the selected modes. The runner passes
   `PASS=5 FAIL=0`.

### Verification

- `PYTHONPATH=scripts python3 scripts/frontier_neutrino_lane4_4f_sigma_m_nu_functional_form.py`
  -> `PASS=4 FAIL=0`
- `python3 -m py_compile scripts/frontier_neutrino_lane4_4f_sigma_m_nu_functional_form.py`
  -> pass
- `PYTHONPATH=scripts python3 scripts/frontier_neutrino_retained_observable_bounds.py`
  -> `PASS=35 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_cosmology_open_number_reduction.py`
  -> `PASS=5 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_hubble_lane5_c1_a1_grassmann_boundary_car_obstruction.py`
  -> `PASS=5 FAIL=0`
- `python3 -m py_compile scripts/frontier_hubble_lane5_c1_a1_grassmann_boundary_car_obstruction.py scripts/frontier_neutrino_lane4_4f_sigma_m_nu_functional_form.py`
  -> pass
- `PYTHONPATH=scripts python3 scripts/frontier_area_law_native_car_semantics_tightening.py`
  -> `PASS=23 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_planck_target3_phase_unit_edge_statistics.py`
  -> `PASS=27 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_planck_target3_clifford_phase_bridge.py`
  -> `PASS=34 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_area_law_primitive_car_edge_identification.py`
  -> `PASS=36 FAIL=0`
- `bash docs/audit/scripts/run_pipeline.sh`
  -> complete
- `python3 docs/audit/scripts/audit_lint.py --strict`
  -> OK, known graph-cycle warning only
- `git diff --check`
  -> pass

### Review-Loop Emulation

- Lane 4F: PASS with boundary note. Structural functional form retained only
  at the algebraic/formal level; numerical `Sigma m_nu` still depends on
  Lane 5 `h` and admitted matter-budget inputs.
- Lane 2: no new route. Keep the 2026-04-27 dependency firewall as the active
  stop boundary until a fresh electron-mass, QED-running, or NR-limit premise
  lands.
- Lane 5 A1: PASS as negative-boundary artifact. The direct A1 route is not
  closed positively; it exposes a sharper import (`P_A` module morphism).
  Conditional Planck/area-law positive packets remain intact.

### Next Exact Action

Continue Lane 5 `(C1)` rather than stopping the cascade. Execute **A2 stretch
attempt**: test whether retained `g_bare = 1` plus the accepted plaquette /
`u_0` surface and minimal APBC hierarchy block projects to action-unit
metrology on `P_A H_cell`. If A2 is blocked, pivot to A4
parity-gate-to-CAR audit or A5 minimal-carrier-axiom audit.

Do **not** create `STOP_ALL_LANES_REQUESTED` yet. Lane 5 still has viable
follow-up after the A1 negative boundary.

## Resume Directive 2026-04-29

The user explicitly requested that the disconnected physics/frontier loop be
picked back up for the next 12 hours. Treat this as human direction to resume
the unattended cascade despite the prior all-lane stop marker. Preserve the
prior stop record as historical context, but run at least one fresh route
assessment before creating a new all-lane stop marker.

**Branch:** `frontier/lane4-neutrino-cascade-20260427`
**Updated:** 2026-04-27T12:57:24Z
**Current lane:** Lane 1 hadron mass program
**Current status:** cycle 5 verified and pushed; all-lane stop marker present

## What Changed

Cycle 1 added a Lane 4 no-go/fork guardrail:

- current-stack `mu_current = 0`;
- diagonal seesaw atmospheric benchmark requires nonzero invertible `M_R`;
- direct one-Higgs Dirac use of `y_nu^eff` gives GeV-scale mass, not meV;
- therefore no hidden global retained closure follows from combining those
  ingredients.

A narrow compatibility fix was also made in
`scripts/frontier_neutrino_majorana_current_stack_zero_law.py`: after the
fast-forward to current `origin/main`, the atlas includes Pfaffian/Nambu
no-forcing and beyond-stack source-principle rows. The runner now verifies
those rows are scoped by the current-atlas non-realization boundary instead of
failing on the mere presence of the word `Pfaffian`.

## Lane 4 Verification

- `PYTHONPATH=scripts python3 scripts/frontier_neutrino_lane4_dirac_seesaw_fork_no_go.py`
  -> `PASS=10 FAIL=0`
- `python3 -m py_compile scripts/frontier_neutrino_lane4_dirac_seesaw_fork_no_go.py scripts/frontier_neutrino_majorana_current_stack_zero_law.py`
  -> pass
- `PYTHONPATH=scripts python3 scripts/frontier_neutrino_majorana_current_stack_zero_law.py`
  -> `PASS=13 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_neutrino_mass_derived.py`
  -> `PASS=19 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_neutrino_retained_observable_bounds.py`
  -> `PASS=35 FAIL=0`
- `bash docs/audit/scripts/run_pipeline.sh`
  -> complete
- `python3 docs/audit/scripts/audit_lint.py --strict`
  -> OK, known graph-cycle warning only
- `git diff --check`
  -> pass

## Lane 2 Cycle 2

Added an atomic Rydberg dependency firewall:

- direct use of retained `alpha_EM(M_Z)=1/127.67` in the Bohr formula gives
  `E_1=-15.68 eV`, about `+15.21%` off the textbook Rydberg scale;
- `m_e` remains a separate linear scale input;
- a retained `alpha(0)` or QED-running bridge and a physical-unit
  nonrelativistic limit are still required.

Verification:

- `PYTHONPATH=scripts python3 scripts/frontier_atomic_rydberg_dependency_firewall.py`
  -> `PASS=12 FAIL=0`
- `python3 -m py_compile scripts/frontier_atomic_rydberg_dependency_firewall.py`
  -> pass
- `PYTHONPATH=scripts python3 scripts/frontier_atomic_hydrogen_helium_probe.py`
  -> bounded scaffold output reproduced
- `bash docs/audit/scripts/run_pipeline.sh`
  -> complete
- `python3 docs/audit/scripts/audit_lint.py --strict`
  -> OK, known graph-cycle warning only
- `git diff --check`
  -> pass

## Lane 5 Cycle 3

Added a Hubble two-gate dependency firewall:

- `H_0 = H_inf / sqrt(L)` keeps both the absolute-scale gate `(C1)` and
  the dimensionless cosmic-history gate `(C2)`/`(C3)` load-bearing;
- `(C1)` alone leaves a one-parameter family over `L`;
- `(C2)` or `(C3)` alone leaves a one-parameter family over `H_inf`;
- the late-time structural lock fixes `H(a)/H_0`, not the scalar `H_0`;
- current `(C3)` remains empty, so the practical path is `(C1) + (C2)`.

Verification:

- `PYTHONPATH=scripts python3 scripts/frontier_hubble_lane5_two_gate_dependency_firewall.py`
  -> `PASS=18 FAIL=0`
- `python3 -m py_compile scripts/frontier_hubble_lane5_two_gate_dependency_firewall.py`
  -> pass
- `PYTHONPATH=scripts python3 scripts/frontier_cosmology_open_number_reduction.py`
  -> `PASS=5 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_hubble_tension_structural_lock.py`
  -> `PASS=5 FAIL=0`
- `bash docs/audit/scripts/run_pipeline.sh`
  -> complete
- `python3 docs/audit/scripts/audit_lint.py --strict`
  -> OK, known graph-cycle warning only

## Lane 3 Cycle 4

Added a quark bounded-companion retention firewall:

- the top mass remains the only retained quark mass;
- down-type CKM-dual ratios are bounded support, not absolute `m_d`, `m_s`,
  `m_b` retention;
- up-type support remains partition/scalar-law bounded;
- species-uniform physical reuse of the top Ward identity overshoots `m_b` by
  about `35x`, so a species-differentiated primitive is required;
- CKM closure is a mixing theorem, not a five-mass closure theorem.

Verification:

- `PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py`
  -> `PASS=17 FAIL=0`
- `python3 -m py_compile scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py`
  -> pass
- `PYTHONPATH=scripts python3 scripts/frontier_quark_mass_ratio_review.py`
  -> `PASS=46 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_yt_bottom_yukawa_retention.py`
  -> `PASS=52 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_yt_ward_identity_derivation.py`
  -> `PASS=45 FAIL=0`
- `bash docs/audit/scripts/run_pipeline.sh`
  -> complete
- `python3 docs/audit/scripts/audit_lint.py --strict`
  -> OK, known graph-cycle warning only

## Lane 1 Cycle 5

Added a hadron confinement-to-mass firewall:

- retained confinement and bounded `sqrt(sigma)` are prerequisites, not
  `m_pi`, `m_p`, `m_n`, or spectrum closure;
- a single bounded scale leaves unretained dimensionless spectral coefficients
  `c_H = m_H / sqrt(sigma)`;
- GMOR still requires retained `m_u`, `m_d`, `Sigma`, and `f_pi`;
- proton/neutron masses require light-quark masses, hadronic-scale matching,
  and correlator/spectral-coefficient extraction.

Verification:

- `PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_confinement_to_mass_firewall.py`
  -> `PASS=16 FAIL=0`
- `python3 -m py_compile scripts/frontier_hadron_lane1_confinement_to_mass_firewall.py`
  -> pass
- `PYTHONPATH=scripts python3 scripts/frontier_confinement_string_tension.py`
  -> `PASS=30 FAIL=0`
- `bash docs/audit/scripts/run_pipeline.sh`
  -> complete
- `python3 docs/audit/scripts/audit_lint.py --strict`
  -> OK, known graph-cycle warning only

## Next Exact Action

Stop this cascade. The branch has been pushed with the Lane 1 checkpoint and
`STOP_ALL_LANES_REQUESTED`. Do not continue to Lane 6 unless a new
charged-lepton premise is actually discovered.

## Stop Condition

All-lane stopping is justified now, not because Lane 4 closed, but because the
full requested viable queue has been processed:

- Lane 4 remains blocked on nonzero Majorana activation or a tiny Dirac
  activation law.
- Lane 2 remains blocked on retained `m_e`, `alpha(0)`/QED running, and the
  physical-unit nonrelativistic limit.
- Lane 5 remains blocked on `(C1)` plus `(C2)` or a fresh `(C3)`.
- Lane 3 remains blocked on the `5/6` bridge/scale-selection proof, up-type
  scalar/partition law, and species-differentiated Ward identities.
- Lane 1 remains blocked on light-quark masses, chiral inputs, hadronic-scale
  matching, and correlator/spectrum extraction.
- Lane 6 has no newly discovered premise; treat it as recently exhausted at
  `origin/frontier/charged-lepton-mass-retirement-20260426`.

The marker
`.claude/science/frontier-workstreams/lane4-neutrino-cascade-20260427/STOP_ALL_LANES_REQUESTED`
is present for the supervisor.
