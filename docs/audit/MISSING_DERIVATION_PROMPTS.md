# Missing-Derivation Prompts

**Status:** human-actionable list. Each entry below is a self-contained
prompt to feed into the `physics-loop` skill in a fresh session. Each one
describes ONE row whose audit verdict says a real derivation is missing
(audited_renaming / audited_failed / audited_numerical_match / open_gate).

Sorted within each category by transitive descendants — top entries unblock
the most downstream rows when fixed.

Archived (`archive_unlanded/*`) rows are excluded — those are already retired.

Usage: pick a row, paste its prompt block into a fresh Claude Code session,
and start the physics-loop. The skill will iterate on the derivation; do not
over-prescribe approach in the prompt.

## audited_renaming

Auditor judged the load-bearing step as a renaming or definition rather than a derivation. The chain reduces to a definitional substitution. To close: write the actual derivation that produces the equality, or accept the renaming and reclassify as a decoration.

_34 rows in this category._

### `planck_primitive_clifford_majorana_edge_derivation_theorem_note_2026-04-30`

**Note:** [docs/PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md](docs/PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md)  |  **Descendants:** 435  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: F
- claim_scope: Audited whether the cited retained Cl(3)/SU(2) bivectors, graph-first SU(3) surface, anomaly-forced time axis, complex Hilbert packet, and rank-four Hamming-weight-one packet derive an invariant irreducible Cl_4(C)/two-mode CAR carrier on P_A H_cell.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner genuinely verifies an explicit matrix representation of Cl_4(C), its CAR pairing, and coefficient cross-checks, but it hard-wires the contested carrier by constructing gamma matrices directly on C^4 and setting rank(P_A)=4. That verifies consistency of the assigned carrier, not derivation of that carrier from the event-cell substrate. The cited no-go notes further show P_A is not uniquely forced because P_3 and other rank-four local equivariant projectors satisfy the same stated substrate tests.

Auditor-quoted load-bearing step:
The note identifies rank(P_A H_cell)=4 with the unique irreducible complex Cl_4(C) module and thereby assigns the displayed gamma generators to P_A H_cell.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `gauge_vacuum_plaquette_spatial_environment_character_measure_theorem_note`

**Note:** [docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md](docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md)  |  **Descendants:** 428  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: open_gate
- load_bearing_step_class: F
- claim_scope: The residual source-sector environment operator is identified with convolution by a normalized unmarked spatial Wilson boundary class function; explicit rho_(p,q)(6) data remain open.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: the load-bearing closure is an asserted identity between the residual operator and the newly constructed convolution operator. Why this blocks: the runner confirms algebraic consistency once a rho_env sequence is supplied, but it does not compute rho_(p,q)(6) from the unmarked spatial Wilson integral or independently verify that the residual operator spectrum equals those coefficients. Repair target: compute or independently verify the beta=6 boundary character coefficients from the unmarked spatial Wilson environment. Claim boundary until fixed: safe to cite this as an open-gate reformulation of the residual environment datum, not as a retained positive theorem.

Auditor-quoted load-bearing step:
The residual environment operator is asserted to have the same normalized coefficients rho_(p,q)(beta) as the boundary class function, so R_beta^env=C_(Z_beta^env).

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `gauge_vacuum_plaquette_residual_environment_identification_theorem_note`

**Note:** [docs/GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md](docs/GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md)  |  **Descendants:** 426  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: open_gate
- load_bearing_step_class: F
- claim_scope: The unresolved residual plaquette factor is identified as a compressed unmarked spatial environment operator R_beta^env; explicit rho_(p,q)(6) coefficients remain open.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: the load-bearing move is an asserted identification of the residual open datum as R_beta^env, not a derivation of its coefficients from the unmarked Wilson environment. Why this blocks: the runner verifies algebraic properties and factorized behavior for a generic positive symmetric witness, but it does not compute the actual residual environment. Repair target: compute rho_(p,q)(6) or Perron data directly from the unmarked spatial Wilson environment, or prove the stripped residual equals that compression without witness injection. Claim boundary until fixed: safe to cite this as an open-gate target naming the residual environment slot, not as a retained theorem.

Auditor-quoted load-bearing step:
After stripping the marked half-slice and local mixed-kernel factor, the remaining object is called and identified exactly with the compressed unmarked spatial Wilson environment operator R_beta^env.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `universal_qg_optional_textbook_comparison_note`

**Note:** [docs/UNIVERSAL_QG_OPTIONAL_TEXTBOOK_COMPARISON_NOTE.md](docs/UNIVERSAL_QG_OPTIONAL_TEXTBOOK_COMPARISON_NOTE.md)  |  **Descendants:** 342  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/UNIVERSAL_QG_OPTIONAL_TEXTBOOK_COMPARISON_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: meta
- load_bearing_step_class: E
- claim_scope: Audited only the note's self-declared packaging/scope boundary, not the underlying canonical textbook continuum closure.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step is a definitional scope statement, not a first-principles computation or algebraic theorem. The note explicitly disclaims being a theorem, claim, or new authority surface, so the audit cannot ratify the seeded positive-theorem hint. With no cited authorities or runner, the only closed item is the packaging boundary itself.

Auditor-quoted load-bearing step:
This note is packaging-only and is not a theorem, claim, or new authority surface.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `hypercharge_identification_note`

**Note:** [docs/HYPERCHARGE_IDENTIFICATION_NOTE.md](docs/HYPERCHARGE_IDENTIFICATION_NOTE.md)  |  **Descendants:** 324  |  **Class:** F

**Status:** _rewrite landed 2026-05-05_ (worktree `naughty-sutherland-f91d6e`).
Closure approach: load-bearing identification step removed from this note;
note retyped to `bounded_theorem` (chain claim) with one-hop authorities
[`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](../LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md)
(structural ratio +1:(-3)) and
[`LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md`](../LHCM_MATTER_ASSIGNMENT_FROM_SU3_REPRESENTATION_NOTE_2026-05-02.md)
(matter-sector identification under SM-definition convention). Absolute
normalization `α = 1/3` explicitly admitted as still-open LHCM repair item
(2). Runner relabeled with explicit STRUCTURAL / CHAIN-L2 / CHAIN-L3 /
CONSISTENCY tags; cache refreshed. Awaiting re-audit on the new note hash.

```
Use the physics-loop skill to close the missing derivation in docs/HYPERCHARGE_IDENTIFICATION_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: F
- claim_scope: Bounded left-handed-doublet identification: in C^8 with SU(2)_weak on factor 1 and SWAP_23 on factors 2 and 3, the unique traceless commutant U(1) has eigenvalue ratio 1:-3 and, after identifying the (2,3) and (2,1) sectors as Q_L and L_L with conventional normalization, reproduces their SM hypercharges and charges.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: the load-bearing step identifies the symmetric/antisymmetric commutant sectors with SM Q_L/L_L and names the unique traceless U(1) as hypercharge after choosing conventional normalization. Why this blocks: the runner verifies exact algebra and downstream consistency after that carrier identification, but it does not derive the SM fermion-sector map or hypercharge normalization from independent premises. Repair target: provide a retained theorem constructing the physical map from the C^8 taste sectors to SM left-handed fermion representations and deriving the allowed normalization/readout without importing the target labels. Claim boundary until fixed: the safe statement is that the commutant contains a unique traceless U(1) whose eigenvalue ratio matches the left-handed SM hypercharge ratio under the stated identification.

Auditor-quoted load-bearing step:
With conventional normalization a=1/3, the (2,3)=C^2 x Sym^2(C^2) subspace is identified with the left-handed quark doublet and the (2,1)=C^2 x Anti^2(C^2) subspace is identified with the left-handed lepton doublet, so the traceless commutant U(1) matches SM hypercharge on that surface.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `s3_time_bilinear_tensor_primitive_note`

**Note:** [docs/S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md](docs/S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md)  |  **Descendants:** 321  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: open_gate
- load_bearing_step_class: E
- claim_scope: Definition-only audit of the bilinear carrier K_R(q) from assumed named coordinates (delta_A1, u_E, u_T) and an assumed decoupling fact on the seven-site star support.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step introduces K_R by definition, and the runner checks algebraic consequences of that definition under an imported coordinate model. The source note explicitly narrows away the physical tensor-primitive claim and lists the upstream derivations still missing. The bounded projection check is endpoint-fixed from an older surface, not a first-principles derivation of the carrier's physical meaning.

Auditor-quoted load-bearing step:
Define the exact microscopic tensor carrier K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q) u_E(q), delta_A1(q) u_T(q)]].

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `yt_color_projection_correction_note`

**Note:** [docs/YT_COLOR_PROJECTION_CORRECTION_NOTE.md](docs/YT_COLOR_PROJECTION_CORRECTION_NOTE.md)  |  **Descendants:** 319  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/YT_COLOR_PROJECTION_CORRECTION_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: F
- claim_scope: Audited the in-scope algebraic/channel-counting claim that the SU(3) color projection gives R_conn = 8/9 and that this same factor supplies sqrt(8/9) to the physical Yukawa vertex.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner hard-codes R_CONN = (N_C**2 - 1)/N_C**2 and applies SQRT_R_CONN as the Yukawa correction; it does not derive the physical scalar Z_phi mapping from framework operators. The central step equates the singlet Yukawa projection with the connected/adjoint fraction, despite the note's own decomposition distinguishing singlet and adjoint pieces. The later mass, Higgs, alpha_s, and PDG comparisons are external comparator/readout checks and cannot close the in-scope derivation.

Auditor-quoted load-bearing step:
The physical Yukawa probes only the singlet channel, so y_t(physical)/y_t(Ward) = sqrt(Z_phi^{connected/total}) = sqrt((N_c^2 - 1)/N_c^2) = sqrt(8/9).

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `s3_time_bilinear_tensor_action_note`

**Note:** [docs/S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md](docs/S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md)  |  **Descendants:** 316  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/S3_TIME_BILINEAR_TENSOR_ACTION_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: open_gate
- load_bearing_step_class: E
- claim_scope: Definition-only tensorized action and spacetime carrier construction from the named inputs `I_R`, `K_R`, `Lambda_R`, and `u_*`; not the Einstein/Regge identification.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: the operative move is a definition of new constructed symbols, not a derivation of a tensor dynamics law. Why this blocks: the runner checks finiteness, imported Schur-generator behavior, and semigroup algebra, then records the GR bridge as blocked rather than proving it. Repair target: retained upstream certificates for the bilinear carrier and a theorem identifying the constructed action/carrier with physical Einstein/Regge dynamics. Claim boundary until fixed: a definition-only tensorized construction under named inputs.

Auditor-quoted load-bearing step:
The note defines `I_TB(f,a;j)=I_R(f;j)+1/2 ||a-vec K_R(q)||^2` and `Xi_TB(t;q)=vec K_R(q) \otimes exp(-t Lambda_R) u_*` from named upstream inputs.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `single_axiom_hilbert_note`

**Note:** [docs/SINGLE_AXIOM_HILBERT_NOTE.md](docs/SINGLE_AXIOM_HILBERT_NOTE.md)  |  **Descendants:** 304  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/SINGLE_AXIOM_HILBERT_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: E
- claim_scope: Audited whether the provided note and runner derive the finite graph plus unitary-evolution axioms from only a finite local tensor-product Hilbert space.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner numerically demonstrates consequences after constructing Hamiltonians with selected support, choosing Born-rule probabilities, and comparing unitary/Lindblad examples, but it does not derive those structures from the single Hilbert-space axiom. The conclusion mainly repackages several specifications into the phrase "local tensor product Hilbert space" and then reads graph/locality/unitarity back out of the added Hamiltonian data. This is a definitional compression rather than a first-principles derivation from the stated axiom.

Auditor-quoted load-bearing step:
A finite-dimensional Hilbert space with local tensor product structure is claimed to encode graph topology, locality, unitarity, and the Born rule as one axiom.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dark_energy_eos_note`

**Note:** [docs/DARK_ENERGY_EOS_NOTE.md](docs/DARK_ENERGY_EOS_NOTE.md)  |  **Descendants:** 295  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/DARK_ENERGY_EOS_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: F
- claim_scope: Audited whether the note derives w = -1 for dark energy from the asserted fixed S^3 spectral-gap identification within the restricted packet.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing move is an asserted identity between physical dark energy/Lambda and a graph spectral gap, followed by standard cosmological algebra. The runner mostly prints and checks consequences of that premise; its numerical S^3 graph calculation does not derive the physical identification and its own finite-grid corrections do not match the claimed -1/4 coefficient. DESI comparisons are external comparator context, not framework-internal closure.

Auditor-quoted load-bearing step:
Dark energy is identified with the fixed S^3 graph-Laplacian spectral gap, Lambda = lambda_1(S^3) = 3/R^2, with R fixed thereafter.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `graviton_mass_derived_note`

**Note:** [docs/GRAVITON_MASS_DERIVED_NOTE.md](docs/GRAVITON_MASS_DERIVED_NOTE.md)  |  **Descendants:** 295  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/GRAVITON_MASS_DERIVED_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: F
- claim_scope: Audited the conditional derivation of m_g = sqrt(6) hbar H_0 / c^2 from the stated S^3 TT spectrum, the radius input R = c/H_0, and the runner source/output supplied in the packet.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner computes the stated arithmetic, bounds ratios, Higuchi ratio, Compton wavelength, and Lambda relation, but it does not instantiate the underlying framework operators or derive the mass identification from first principles. The load-bearing move is the asserted identity between the lowest TT eigenvalue and physical graviton mass-squared, which is a renaming/definition-like bridge in the restricted packet. The result also depends numerically on the imported H_0 radius choice, but the primary failure of theorem closure is the unproved eigenvalue-to-mass identification.

Auditor-quoted load-bearing step:
The effective graviton mass is identified with the lowest S^3 TT Lichnerowicz eigenvalue: m_g^2 c^2 / hbar^2 = lambda_2^TT = 6/R^2, with R = c/H_0.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `rconn_derived_note`

**Note:** [docs/RCONN_DERIVED_NOTE.md](docs/RCONN_DERIVED_NOTE.md)  |  **Descendants:** 288  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/RCONN_DERIVED_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: F
- claim_scope: Audited the claimed derivation of R_conn = (N_c^2 - 1)/N_c^2 + O(1/N_c^4) for the SU(N_c) quark-antiquark connected color trace ratio, specialized to 8/9 at N_c = 3.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner performs a Monte Carlo comparison against the expected 8/9 value, but the code also computes that value explicitly as the check target and does not derive the contested dynamical identification from first principles. The source note's decisive step is the assertion that the connected/adjoint propagator fraction equals the representation dimension fraction, which is an open bridge between a group-theory decomposition and a dynamical lattice observable. The provided Fierz authority supports the exact 8/9 channel-counting ratio, not the physical connected-trace matching claimed here.

Auditor-quoted load-bearing step:
The note identifies the dynamical connected trace fraction with the adjoint Hilbert-space dimension fraction by assuming planar dynamics populates all color channels according to dimensionality, giving Pi_adjoint/Pi_total = (N_c^2 - 1)/N_c^2.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `universal_gr_tensor_action_blocker_note`

**Note:** [docs/UNIVERSAL_GR_TENSOR_ACTION_BLOCKER_NOTE.md](docs/UNIVERSAL_GR_TENSOR_ACTION_BLOCKER_NOTE.md)  |  **Descendants:** 287  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/UNIVERSAL_GR_TENSOR_ACTION_BLOCKER_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: E
- claim_scope: Audited the note's bounded blocker claim that the direct universal GR route remains incomplete until a tensor localization/projector primitive identifies the scalar-generator Hessian with full Einstein/Regge metric dynamics.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
No runner, cited authority, or derivation is provided, so the audit must judge from the note text alone. The load-bearing move introduces and names the missing primitive Pi_curv/projector bundle and uses that definition to classify the route as blocked. This is an honest bounded blocker statement, but it is not a first-principles computation or algebraic closure from retained inputs.

Auditor-quoted load-bearing step:
The route lacks a covariant 3+1 polarization-frame/projector bundle with distinguished connection and induced curvature-localization map Pi_curv identifying the Hessian kernel with Einstein/Regge dynamics.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `restricted_strong_field_closure_note`

**Note:** [docs/RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](docs/RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md)  |  **Descendants:** 286  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: E
- claim_scope: Audited whether the provided note alone closes the claimed exact restricted strong-field closure for the local O_h shell source class without cited authorities or runner evidence.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
No cited authorities or runner source/stdout are available, so the audit must judge the note text alone. The local 3+1 equations partly follow by substituting the definitions of rho and S once the bridge and shell source are assumed, but the core closure package is introduced as an exact status assertion rather than derived. That makes the load-bearing step a definitional/package declaration, not a first-principles computation or genuine algebraic closure over independent retained inputs.

Auditor-quoted load-bearing step:
The note asserts that on the exact local O_h class, the shell law, same-charge bridge, local 3+1 lift, and Schur boundary action form one exact restricted strong-field closure package.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `gravity_full_self_consistency_note`

**Note:** [docs/GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md](docs/GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md)  |  **Descendants:** 285  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: F
- claim_scope: Audited whether the note derives Poisson on Z^3 with no operator-class restriction from Cl(3) on Z^3 plus the asserted self-consistency identity L^{-1}=G_0.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing move identifies the field Green's function L^{-1} with the propagator Green's function G_0. Once that identity is stipulated, L=G_0^{-1}=H is an algebraic consequence, but the identity itself is not independently derived in the packet. No runner source or stdout is available to upgrade the claim to first-principles computation, and the note's numerical checks as described only verify the stipulated closure and its inversion.

Auditor-quoted load-bearing step:
Self-consistency requires L^{-1} = G_0, so L = G_0^{-1} = H = -Delta_lat.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `s3_time_constructed_support_tensor_primitive_note`

**Note:** [docs/S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md](docs/S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md)  |  **Descendants:** 285  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: E
- claim_scope: Audited the note's claim that Xi_R^(0), defined as the response Jacobian of the bounded prototype with respect to delta_A1, is a nonzero bounded tensor primitive compatible with Theta_R^(0).

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step is a definition of a new symbol as a derivative of an already named bounded prototype with respect to an already named support scalar. No runner or cited authority is provided, and the note does not perform a first-principles computation or an algebraic closure from independent retained inputs. The affine compatibility and nonzero-direction claims rely on imported structure and endpoint context absent from the restricted packet, so the presented chain does not close as a derivation.

Auditor-quoted load-bearing step:
Define the bounded support-response tensor primitive candidate Xi_R^(0) := d Theta_R^(0) / d delta_A1 on the microscopic support block A1 x {E_x, T1x}.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `s3_time_tensor_primitive_prototype_note`

**Note:** [docs/S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md](docs/S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md)  |  **Descendants:** 285  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: E
- claim_scope: Audited the note's bounded definition of the Route-2 tensor primitive prototype Theta_R^(0) on A1 x {E_x, T1x}, including its asserted endpoint coefficients and affine support-law role.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step is a new definition of Theta_R^(0) as the pair of already-named coefficients gamma_E and gamma_T, so the audited chain is definitional rather than a first-principles derivation. No runner source or stdout is available, and no cited authorities are provided, so the numerical endpoint values and affine support-law claims cannot be independently verified inside the restricted packet. Because the note explicitly frames the object as bounded staging rather than exact theorem-grade closure, the clean theorem burden is not met.

Auditor-quoted load-bearing step:
For a scalar A1 background q, define Theta_R^(0)(q) := (gamma_E(q), gamma_T(q)) after normalizing by the exact reduced anisotropic shell amplitude.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_leptogenesis_pmns_observable_relative_action_law_note_2026-04-16`

**Note:** [docs/DM_LEPTOGENESIS_PMNS_OBSERVABLE_RELATIVE_ACTION_LAW_NOTE_2026-04-16.md](docs/DM_LEPTOGENESIS_PMNS_OBSERVABLE_RELATIVE_ACTION_LAW_NOTE_2026-04-16.md)  |  **Descendants:** 284  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/DM_LEPTOGENESIS_PMNS_OBSERVABLE_RELATIVE_ACTION_LAW_NOTE_2026-04-16.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: open_gate
- load_bearing_step_class: E
- claim_scope: Audited whether the observable-relative-action minimization law and reported off-seed PMNS closure selector are derived from the restricted packet rather than introduced as an additional selector premise.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing move is the introduction of a new selector law: minimize the relative bosonic action under exact closure on the favored column. The supplied runner performs a real constrained numerical optimization once that law, seed surface, transport machinery, and normalizations are supplied, but it does not prove that the law follows from the sole axiom. Because the decisive premise is definitional rather than derived, the audited chain does not close as a positive theorem.

Auditor-quoted load-bearing step:
Among all positive off-seed sources on the same seed surface satisfying eta_{i_*} / eta_obs = 1, choose the one minimizing S_rel(H_e || H_seed).

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_leptogenesis_exact_kernel_closure_note_2026-04-15`

**Note:** [docs/DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md](docs/DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md)  |  **Descendants:** 283  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/DM_LEPTOGENESIS_EXACT_KERNEL_CLOSURE_NOTE_2026-04-15.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: E
- claim_scope: Audited the narrowed claim that the exact source/CP package plus K00=2 gives epsilon_1 / epsilon_DI ≈ 0.928 and eta/eta_obs ≈ 0.558 on the retained benchmark, with percent-level eta closure no longer claimed.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Although the runner labels six checks as class C, its source code hard-codes the claimed exact package values rather than deriving them from the axiom. The epsilon and eta calculations are downstream numerical arithmetic once those values and retained benchmark constants are accepted. The audit therefore cannot ratify the source-package closure as a first-principles theorem from the restricted packet.

Auditor-quoted load-bearing step:
The refreshed branch fixes gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3, and K00 = 2, yielding the exact CP tensor channels and the epsilon_1 / epsilon_DI = 0.9276209209 kernel result.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_neutrino_k00_bosonic_normalization_theorem_note_2026-04-15`

**Note:** [docs/DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md](docs/DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md)  |  **Descendants:** 283  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/DM_NEUTRINO_K00_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: F
- claim_scope: Audited whether the provided note and runner derive the heavy-basis diagonal normalization K00 = 2 from the restricted packet alone.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner verifies several linear-algebra facts about J3/3 and (1/2)J2, but those are class A checks over matrices already introduced in the note. The load-bearing identification of the target K00 normalization with twice the source amplitude is not independently computed; it is imposed as the coefficient law. The final value K00 = 2 also depends on hard-coded tau_E = tau_T = 1/2, with no derivation or retained cited authority in the restricted packet.

Auditor-quoted load-bearing step:
Since F00 is isospectral to (1/2)J2, the unique additive CPT-even bosonic observable fixes the coefficient law K00 = 2 tau_+.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `pmns_sole_axiom_hw1_source_transfer_boundary_note`

**Note:** [docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md](docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md)  |  **Descendants:** 283  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/PMNS_SOLE_AXIOM_HW1_SOURCE_TRANSFER_BOUNDARY_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: E
- claim_scope: Audited only the restricted claim that the canonical hw=1 source/transfer construction, as implemented, produces basis-source columns, a cycle support frame, and is rejected by the retained PMNS closure stack.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The provided runner performs mostly algebraic consistency checks after defining the canonical pack with active_block = I3 and passive_block = I3. It does not instantiate the Clifford/lattice axiom or compute the identity resolvent result from first principles, and key support/closure functions are imported without their sources. The bounded conclusion is true for the defined trivial pack, but the load-bearing claim that this pack is derived from the sole axiom is not closed by the restricted packet.

Auditor-quoted load-bearing step:
The sole-axiom active/passive blocks are therefore exactly (I3, I3), so source insertion and graph-first transfer only produce the trivial free pack.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_leptogenesis_pmns_minimum_information_source_law_note_2026-04-16`

**Note:** [docs/DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md](docs/DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md)  |  **Descendants:** 282  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: E
- claim_scope: Audited the asserted minimum-information selector law and its reported closure source for the PMNS-assisted N_e branch using only the note, runner output, and runner source provided.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step is a definition of a new selector principle: minimize I_seed subject to exact closure on the favored column. The runner appears to perform a real constrained optimization, but the selection criterion itself is not derived from the axiom and several imported framework components are not available in the restricted packet. Therefore the note can document the consequences of adopting this invented law, but it does not audit as a first-principles theorem.

Auditor-quoted load-bearing step:
Among all positive off-seed sources on the same seed surface satisfying eta_{i_*}/eta_obs = 1, choose the one minimizing I_seed.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `koide_mru_weight_class_obstruction_theorem_note_2026-04-19`

**Note:** [docs/KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md](docs/KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)  |  **Descendants:** 282  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: E
- claim_scope: Audited the claimed conversion of the unreduced determinant obstruction into an MRU-resolving two-slot real-isotype quotient for the d=3 cyclic carrier, using only the note and runner source/output provided.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner verifies correct algebraic consequences once the reduced carrier is accepted, including the unreduced (1,2) determinant weight and the equal-weight reduced determinant. It does not independently derive the physical or structural necessity of replacing the real doublet plane by a single scalar slot; that step is encoded as a definition/quotient choice. Therefore the presented positive resolution is not a first-principles closure from the restricted packet.

Auditor-quoted load-bearing step:
The scalar lane quotients the internal SO(2) frame of the real doublet and therefore retains only the doublet radius, giving the two-slot carrier (rho_+, rho_perp).

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `pmns_commutant_eigenoperator_selector_note`

**Note:** [docs/PMNS_COMMUTANT_EIGENOPERATOR_SELECTOR_NOTE.md](docs/PMNS_COMMUTANT_EIGENOPERATOR_SELECTOR_NOTE.md)  |  **Descendants:** 282  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/PMNS_COMMUTANT_EIGENOPERATOR_SELECTOR_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: F
- claim_scope: Audited the bounded claim that a non-Cl(3) projected commutant eigenoperator on the hw=1 triplet yields a native even/odd C3 selector law for the passive offset and orientation labels, while not closing the active 5-real PMNS source.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: the computed C3 Fourier modes are renamed as passive-offset and branch/orientation selectors without an internal theorem deriving that readout. Why this blocks: the finite linear-algebra computation establishes a nonzero corner-distinguishing profile, but the selector interpretation and the specific tau/q extraction are asserted by definition-level code. Repair target: prove a bridge theorem that the relevant PMNS selector observables are exactly these even/odd Fourier invariants with the stated normalization and q/tau maps. Claim boundary until fixed: the packet supports a projected-commutant corner-profile decomposition, not an axiom-native PMNS selector value law.

Auditor-quoted load-bearing step:
The C3-even Fourier mode of the lifted projected commutant generator fixes the passive offset class, and the C3-odd Fourier mode fixes the branch/orientation selector.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `single_axiom_information_note`

**Note:** [docs/SINGLE_AXIOM_INFORMATION_NOTE.md](docs/SINGLE_AXIOM_INFORMATION_NOTE.md)  |  **Descendants:** 282  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/SINGLE_AXIOM_INFORMATION_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: meta
- load_bearing_step_class: F
- claim_scope: Audited whether the note derives graph substrate and unitary dynamics as inseparable consequences of a single conserved-information-flow axiom from the restricted packet.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The numerical checks are mostly algebraic or model-demonstration checks after H has already been chosen as sparse and Hermitian. They do not derive the graph-unitary object from the single verbal axiom; they rename the original graph-plus-unitary package as conserved information flow and show familiar properties of that representation. Test 2 and Test 3 add self-consistency claims about locality and unitarity, but these rely on chosen graph models and imposed dissipative factors rather than closing a first-principles derivation.

Auditor-quoted load-bearing step:
The mathematical realization is taken to be a sparse Hermitian operator H whose nonzero entries define the graph and whose exponentiation exp(iHt) defines unitary dynamics.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_leptogenesis_transport_decomposition_theorem_note_2026-04-16`

**Note:** [docs/DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md](docs/DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md)  |  **Descendants:** 281  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/DM_LEPTOGENESIS_TRANSPORT_DECOMPOSITION_THEOREM_NOTE_2026-04-16.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: E
- claim_scope: Audited whether the supplied note and runner derive the stated transport decomposition and comparator demotion from the axiom-only packet.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing equation introduces kappa_axiom[H] as the remaining transport object rather than computing it. The runner verifies imported constants and hard-coded benchmark numbers, but the claimed theorem-native closure is represented by definitional statements and unconditional checks. This is not a first-principles computation from the axiom and does not establish the asserted authority-path demotion as a derived result.

Auditor-quoted load-bearing step:
eta[H] = (s/n_gamma) * C_sph * d_N * epsilon_1 * kappa_axiom[H], with kappa_axiom[H] declared to be the direct transport functional and kappa_fit(K) demoted to a comparator.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `pmns_corner_transport_active_block_note`

**Note:** [docs/PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md](docs/PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md)  |  **Descendants:** 281  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: E
- claim_scope: Audited the bounded claim that orbit-averaged direct hw=1 corner transport recovers the active seed pair on the aligned patch, reads a branch bit from the imaginary C3-odd asymmetry, and remains blind to the five-real corner-breaking source.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner performs real algebraic checks on the provided transport matrix and its orbit averages, including the branch-bit sign flip and the nontrivial kernel example. However, it does not derive the direct corner-to-corner transport matrix from the axiom; it defines that operator form in code and verifies consequences. With no cited upstream authority closing the operator construction, the load-bearing step is a definition rather than a first-principles native theorem.

Auditor-quoted load-bearing step:
For the active hw=1 triplet, the direct corner-to-corner transport matrix is T_act = diag(x_1, x_2, x_3) + diag(y_1, y_2, y_3 e^{i delta}) C.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `pmns_transfer_operator_dominant_mode_note`

**Note:** [docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md](docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md)  |  **Descendants:** 281  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: bounded_theorem
- load_bearing_step_class: E
- claim_scope: Audited the claimed bounded law that the aligned hw=1 native transfer-operator spectrum recovers the active PMNS seed pair and weak-axis seed patch while remaining blind to the 5-real zero-sum off-seed breaking carrier.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: The note names T_seed = xbar I + ybar(C + C^2) as the native positive transfer kernel and then recovers the same seed coefficients by eigenvalue inversion; the runner likewise constructs the kernel from supplied xbar and ybar, including a separate 2*xbar normalization in the active-block shadow. Why this blocks: This establishes an exact algebraic reparameterization of an already supplied C3 circulant kernel, not a native dynamical law that recovers PMNS microscopic data from independent transport. Repair target: Derive the hw=1 transfer kernel and its active-block normalization from primitive corner-to-corner dynamics without inserting the target seed coefficients, and make the runner construct that object from those primitive inputs. Claim boundary until fixed: The result may be cited as the exact spectral identity for an already specified positive aligned C3 transfer kernel, plus its blindness to zero-sum off-seed breaking, but not as a native recovery law for the PMNS seed data.

Auditor-quoted load-bearing step:
On the aligned hw=1 active patch, the native positive transfer kernel T_seed = xbar I + ybar(C + C^2) has one dominant symmetric mode and one doubly-degenerate orthogonal mode, and those two eigenvalues reconstruct (xbar, ybar).

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_conclusion_boundary_note`

**Note:** [docs/TELEPORTATION_CONCLUSION_BOUNDARY_NOTE.md](docs/TELEPORTATION_CONCLUSION_BOUNDARY_NOTE.md)  |  **Descendants:** 281  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_CONCLUSION_BOUNDARY_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: open_gate
- load_bearing_step_class: E
- claim_scope: Audited only the boundary claim that the teleportation lane remains a conditional planning artifact with selector, scaling, and hardware obligations still open, and no matter/FTL transport claim.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner does not derive the boundary from the axiom or recompute the cited physics; it mostly encodes fixed selector, scaling, and hardware status values, then checks booleans against them. That is adequate for a planning/status boundary, but under the rubric the load-bearing step is a definition/status assignment rather than class C derivation or independent algebraic closure. The verdict therefore cannot be audited_clean even though the note is appropriately conservative and does not overclaim unconditional closure.

Auditor-quoted load-bearing step:
The lane is closed as a conditional planning artifact with precise remaining obligations, but is not closed as unconditional nature-grade theory.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `universal_gr_casimir_block_localization_note`

**Note:** [docs/UNIVERSAL_GR_CASIMIR_BLOCK_LOCALIZATION_NOTE.md](docs/UNIVERSAL_GR_CASIMIR_BLOCK_LOCALIZATION_NOTE.md)  |  **Descendants:** 281  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/UNIVERSAL_GR_CASIMIR_BLOCK_LOCALIZATION_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: E
- claim_scope: Audited whether the note proves an exact canonical lapse/shift/trace/shear block localization for the universal GR route from the restricted packet alone.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The note asserts the projector, complement representation, Casimir spectrum, and physical block labels, but the restricted packet provides no upstream inputs or runner source/output to verify those assertions. The load-bearing step functions as an introduced classification/definition within the note rather than a derivation from provided axioms or retained inputs. Because no actual computation or algebraic closure is present, the claimed positive theorem is not audited clean.

Auditor-quoted load-bearing step:
On the 8D complement of Pi_A1, the universal SO(3) generators define C = G_x^2 + G_y^2 + G_z^2 with spectrum -2 of multiplicity 3 and -6 of multiplicity 5, giving the j=1 shift and j=2 shear blocks.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `universal_gr_supermetric_normal_form_note`

**Note:** [docs/UNIVERSAL_GR_SUPERMETRIC_NORMAL_FORM_NOTE.md](docs/UNIVERSAL_GR_SUPERMETRIC_NORMAL_FORM_NOTE.md)  |  **Descendants:** 281  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/UNIVERSAL_GR_SUPERMETRIC_NORMAL_FORM_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: F
- claim_scope: Audited the asserted identification of the universal Hessian on the SO(3)-invariant lifted background with the inverse-metric supermetric normal form.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step is an asserted identity between the existing object called the universal Hessian and the inverse-metric pairing, not a first-principles computation or algebraic closure over provided retained inputs. No upstream authorities or runner evidence are available in the packet. Therefore the theorem-level conclusion does not close from the restricted inputs and reduces to an unsupported identification/substitution.

Auditor-quoted load-bearing step:
For symmetric perturbations h,k on D = diag(a,b,b,b), the universal Hessian is B(h,k) = -Tr(D^-1 h D^-1 k), exactly the inverse-metric contraction pairing.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `gauge_vacuum_plaquette_full_slice_rim_lift_integral_boundary_science_only_note_2026-04-17`

**Note:** [docs/GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md](docs/GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md)  |  **Descendants:** 12  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: E
- claim_scope: Audited whether the note derives the full-slice rim lift B_beta(W) and eta_beta(W)=P_cls B_beta(W) as exact local Wilson/Haar boundary objects from the restricted packet.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing move is a definition-style identification of B_beta(W) with a named local Wilson/Haar rim integral, followed by eta_beta(W)=P_cls B_beta(W). The supplied runner does not verify this theorem: it computes a separate first-three-sample positive-cone obstruction and only string-checks that the rim-lift note says explicit B_6 remains open. With no cited upstream authority and no first-principles derivation in the restricted packet, the theorem-grade conclusion reduces to introducing a symbol for the proposed boundary integral.

Auditor-quoted load-bearing step:
The full-slice local rim lift is declared to be the exact slice-space boundary function B_beta(W)(U) = integral_(Omega^rim(U)) dmu_H(Xi^rim) exp[(beta / 3) A^rim(U, Xi^rim; W)].

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `lattice_nn_light_cone_note`

**Note:** [docs/LATTICE_NN_LIGHT_CONE_NOTE.md](docs/LATTICE_NN_LIGHT_CONE_NOTE.md)  |  **Descendants:** 0  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/LATTICE_NN_LIGHT_CONE_NOTE.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: F
- claim_scope: Administrative branch-freeze: the NN/DAG light-cone branch is frozen as a topological forward-reachability statement (influence confined to the forward causal neighborhood in the graph/DAG sense). Explicit retraction of any emergent-relativity, Lorentz-invariance, physical-spacetime light-cone, or universal-speed-law reading. Excludes any independent retained light-cone theorem; the cited fixed-mass verification log is missing and the causal-field script is marked retracted for distance-law purposes.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Re-audit confirms the original renaming verdict: the residual claim is a graph-reachability label, not a derived physical light-cone law. Scope narrowed to the administrative branch-freeze with explicit emergent-relativity retraction.

Auditor-quoted load-bearing step:
The NN light-cone branch is frozen as a topological causal-bound statement: influence is confined to the relevant forward causal neighborhood in the graph/DAG sense, with no emergent-relativity or physical spacetime light-cone claim retained.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `yt_ssb_matching_gap_analysis_note_2026-04-18`

**Note:** [docs/YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md](docs/YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md)  |  **Descendants:** 0  |  **Class:** F

```
Use the physics-loop skill to close the missing derivation in docs/YT_SSB_MATCHING_GAP_ANALYSIS_NOTE_2026-04-18.md.

Current audit state:
- audit_status: audited_renaming
- claim_type: positive_theorem
- load_bearing_step_class: F
- claim_scope: Bounded H_unit normalization arithmetic: two quantities defined as the same H_unit component overlap each evaluate to 1/sqrt(6). Excludes any retained matching theorem for the physical Yukawa trilinear; the SSB matching gap is not closed by identifying the Ward 4-fermion matrix element with the Qbar_L-H-u_R trilinear coefficient via a shared 1/sqrt(6) normalization without deriving HS/source normalization, SSB VEV division, chirality projection, LSZ/external-state normalization, and absence of extra factors.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Re-audit confirms the original renaming verdict: shared H_unit normalization is asserted, not derived from a tree-level operator-matching theorem. Scope narrowed from the migration backfill to the bounded H_unit arithmetic.

Auditor-quoted load-bearing step:
The Ward 4-fermion channel and the physical trilinear are both matrix elements of H_unit; they share the 1/sqrt(6) coefficient by construction.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


## audited_failed

Auditor judged that the chain doesn't close even on its own terms — the note's claimed conclusion doesn't follow from the cited inputs as written. To close: identify the broken step, rewrite the chain, or scope the claim down to what actually closes.

_16 rows in this category._

### `shapiro_static_discriminator_note`

**Note:** [docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md](docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md)  |  **Descendants:** 307  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md.

Current audit state:
- audit_status: audited_failed
- claim_type: bounded_theorem
- load_bearing_step_class: A
- claim_scope: Audited the restricted claim that, in the provided Shapiro discriminator runner, the static cone-shape field matches the causal c-dependent detector-line phase curve and the static scheduling proxy does not.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The exact static-cone mimic is supported only because the runner's causal and static-cone field builders are algebraically identical; no independent causal propagation delay is actually computed in the causal branch. The note's broader boundary claim also requires the static scheduling curve to be near-flat, but the cached runner timed out with no results. On its own terms, the runner therefore does not establish the claimed causal-vs-static discriminator result as a first-principles or completed computational theorem.

Auditor-quoted load-bearing step:
The frozen cone-shape proxy reproduces the full c-dependent causal phase curve to numerical precision, while the frozen activation-delay proxy stays near-flat.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_neutrino_weak_vector_theorem_note_2026-04-15`

**Note:** [docs/DM_NEUTRINO_WEAK_VECTOR_THEOREM_NOTE_2026-04-15.md](docs/DM_NEUTRINO_WEAK_VECTOR_THEOREM_NOTE_2026-04-15.md)  |  **Descendants:** 293  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/DM_NEUTRINO_WEAK_VECTOR_THEOREM_NOTE_2026-04-15.md.

Current audit state:
- audit_status: audited_failed
- claim_type: positive_theorem
- load_bearing_step_class: A
- claim_scope: Audited the claimed exact weak-vector covariance, spin-1 Casimir, and trace orthogonality of the direct chiral bridge family from the definitions stated in the note only.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step is an algebraic identity claim, not a renaming or numerical match. However, with no cited authorities, no runner stdout, and no runner source, the restricted packet contains only the theorem statement and a description of checks, not the checks themselves. Because the relevant operator algebra is not fully specified in the packet, the claimed exact weak-vector theorem does not close on its own terms in this audit.

Auditor-quoted load-bearing step:
The chiral bridge family Y_i = P_R Gamma_i P_L obeys [B_a, Y_b] = i eps_{abc} Y_c under the derived weak bivectors.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `persistent_object_multistage_floor_sweep_note_2026-04-16`

**Note:** [docs/PERSISTENT_OBJECT_MULTISTAGE_FLOOR_SWEEP_NOTE_2026-04-16.md](docs/PERSISTENT_OBJECT_MULTISTAGE_FLOOR_SWEEP_NOTE_2026-04-16.md)  |  **Descendants:** 282  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/PERSISTENT_OBJECT_MULTISTAGE_FLOOR_SWEEP_NOTE_2026-04-16.md.

Current audit state:
- audit_status: audited_failed
- claim_type: bounded_theorem
- load_bearing_step_class: C
- claim_scope: Audited the bounded exact-lattice multistage floor claim that, under the frozen h=0.25, blend=0.25, three-update/three-segment setup and five stable widened rows, top4 is the first retained object width passing the stated persistence, carry, direction, alpha, and kappa-drift gates.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The top3 completed output supports the negative part of the floor comparison: top3 fails 0/5 under the stated gates. However, the claim’s conclusion requires completed top4 evidence showing 5/5 admissibility and preferably top5/top6 corroboration; those outputs are not included in the restricted packet. Since no cited authorities are provided and the note’s asserted top4 rows cannot be verified from the available stdout alone, the chain does not close on its own terms.

Auditor-quoted load-bearing step:
Multistage-admissible totals on the stable widened-regime rows are top3: 0/5, top4: 5/5, top5: 5/5, top6: 5/5, so top4 is the first self-maintaining floor.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `ckm_schur_complement_theorem`

**Note:** [docs/CKM_SCHUR_COMPLEMENT_THEOREM.md](docs/CKM_SCHUR_COMPLEMENT_THEOREM.md)  |  **Descendants:** 281  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/CKM_SCHUR_COMPLEMENT_THEOREM.md.

Current audit state:
- audit_status: audited_failed
- claim_type: bounded_theorem
- load_bearing_step_class: A
- claim_scope: Audited the algebraic Schur-complement identity c_13^eff = c_12*c_23 for the stipulated NNI matrix, plus the note's broader CKM magnitude claims using the provided runner output and source.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The central identity c_13^eff = c_12*c_23 is a valid class-A algebraic Schur-complement calculation, not a first-principles computation. The runner relies on PDG masses/CKM values, fitted NNI coefficients, and heuristic overlap or cascade inputs, and several bounded checks fail on its own output: |V_ub| is high by about 6x, J by about 4.7x, lambda and A miss their stated tolerances, and the Schur c_13/c_23 ratio is 1480x from the scan optimum. Therefore the broad CKM theorem does not close even conditionally within the supplied packet.

Auditor-quoted load-bearing step:
The Schur complement of the generation-2 block gives (M_eff)_13 = -a*b/m_2 = -c_12*c_23*sqrt(m_1*m_3), hence c_13^eff = c_12*c_23 in NNI normalization.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `equivalence_principle_note`

**Note:** [docs/EQUIVALENCE_PRINCIPLE_NOTE.md](docs/EQUIVALENCE_PRINCIPLE_NOTE.md)  |  **Descendants:** 281  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/EQUIVALENCE_PRINCIPLE_NOTE.md.

Current audit state:
- audit_status: audited_failed
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited only the bounded statement that a lattice uniform-field beam sweep reportedly gives near-linear force-response exponents and does not derive equality of inertial and gravitational mass.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The note explicitly avoids the strong equivalence-principle conclusion and correctly states that the missing force observable, mass-extraction theorem, source-normalization theorem, and action-coupling derivation prevent that chain from closing. However, even the bounded positive content relies on reported numerical exponents without the underlying runner, source code, fit tables, or upstream authority. With no cited authorities and no runner source available, the restricted packet cannot verify the measured sweep that carries the bounded claim.

Auditor-quoted load-bearing step:
A uniform-field deflection sweep on the lattice produces force responses that scale near-linearly with field strength and source strength, with exponents 1.008 and 0.998, while layer scaling is sub-quadratic at 1.14.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `gauge_vacuum_plaquette_first_sector_minimal_bulk_completion_principle_theorem_note_2026-04-19`

**Note:** [docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_PRINCIPLE_THEOREM_NOTE_2026-04-19.md](docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_PRINCIPLE_THEOREM_NOTE_2026-04-19.md)  |  **Descendants:** 281  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_MINIMAL_BULK_COMPLETION_PRINCIPLE_THEOREM_NOTE_2026-04-19.md.

Current audit state:
- audit_status: audited_failed
- claim_type: bounded_theorem
- load_bearing_step_class: A
- claim_scope: Audited only the order-minimality and positive-tail monotonicity claim inside the canonical Wilson factorized cone described in the note and runner.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner imports three upstream notes by substring checks even though no cited authorities are supplied in the restricted packet, so those imported premises cannot count as closed inputs. Its universal monotonicity and uniqueness claims are not proved by the finite witness checks on tails A and B. The coefficient-order zero-extension result is valid on its own terms, but the claimed equivalence to unique Loewner-minimality for all admissible extensions is not established by the provided note and code.

Auditor-quoted load-bearing step:
Among all full nonnegative conjugation-symmetric extensions of rho_ret, the minimal-support zero extension is the unique least element in the coefficient order and therefore uniquely minimizes every positive bulk-tail functional.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `koide_delta_lattice_wilson_selected_eigenline_no_go_note_2026-04-24`

**Note:** [docs/KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO_NOTE_2026-04-24.md](docs/KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO_NOTE_2026-04-24.md)  |  **Descendants:** 281  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO_NOTE_2026-04-24.md.

Current audit state:
- audit_status: audited_failed
- claim_type: no_go
- load_bearing_step_class: C
- claim_scope: As-written finite L=3 Wilson selected-eigenline no-go, including both the rank-two character-sector obstruction and the claimed ambient eta-proxy residual.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: the as-written note's ambient residual and expected closeout are stale relative to the included runner/source, which returns one failed check and `KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO=FALSE`. Why this blocks: the full source-note claim does not close on its own verification packet, even though the rank-two selected-eigenline obstruction appears locally supported. Repair target: split or correct the ambient eta-proxy assertion and rerun the closeout so the retained claim is only the computed rank-two selected-line no-go unless a real eta mismatch is derived. Claim boundary until fixed: finite Wilson data support non-canonical rank-one selection inside a multiplicity-two character sector, not the false ambient eta mismatch residual.

Auditor-quoted load-bearing step:
The note asserts that the finite Wilson data leave a rank-two same-character zero-mode sector, so they select a spectral projector/eigenspace rather than a unique rank-one eigenline.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `koide_frobenius_isotype_split_uniqueness_note_2026-04-21`

**Note:** [docs/KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md](docs/KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md)  |  **Descendants:** 281  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md.

Current audit state:
- audit_status: audited_failed
- claim_type: positive_theorem
- load_bearing_step_class: A
- claim_scope: Audited the internal algebraic AM-GM route from the admitted Herm_circ(3) scalar/traceless Frobenius energy split to kappa = 2 and Q = 2/3, not the physical/source-law bridge.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner verifies many algebraic identities for the chosen trace/Frobenius split and one PDG interior positivity check. But the note's stronger claim that the building blocks are structurally fixed is not established: the uniqueness argument for the Frobenius inner product is incomplete, since checking that (tr A)(tr B) alone is degenerate does not exclude positive combinations with Tr(AB). Therefore the presented chain does not close on its own terms as a uniqueness theorem, although the conditional AM-GM calculation is algebraically correct.

Auditor-quoted load-bearing step:
Given E_+ + E_perp = Tr(M^2) = N, AM-GM uniquely maximizes log(E_+ E_perp) at E_+ = E_perp = N/2, hence kappa = 2 and Q = 2/3.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `koide_hostile_review_guard_note_2026-04-24`

**Note:** [docs/KOIDE_HOSTILE_REVIEW_GUARD_NOTE_2026-04-24.md](docs/KOIDE_HOSTILE_REVIEW_GUARD_NOTE_2026-04-24.md)  |  **Descendants:** 281  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/KOIDE_HOSTILE_REVIEW_GUARD_NOTE_2026-04-24.md.

Current audit state:
- audit_status: audited_failed
- claim_type: meta
- load_bearing_step_class: A
- claim_scope: Whether the hostile-review guard actually substantiates its stated mechanical hygiene checks for Koide no-go packet drift and only emits negative Q/delta closure flags.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: The note claims the guard verifies that every no-go script prints explicit negative CLOSES flags and residual labels. Why this blocks: the runner only performs source-text substring checks, so comments, dead strings, or unrelated FALSE/RESIDUAL occurrences could satisfy the guard without the claimed printed outputs existing. Repair target: execute the target scripts or parse their AST/print paths to verify the actual emitted closeout and residual labels, then rerun the guard. Claim boundary until fixed: the artifact supports only a shallow packet-hygiene source scan and its own negative HOSTILE_REVIEW_GUARD_CLOSES_Q/DELTA flags, not the stronger print-verification claim.

Auditor-quoted load-bearing step:
The runner scans the Koide no-go notes, objection-review packet, and no-go scripts, and verifies the eight listed hygiene checks while emitting negative Q and delta closure flags.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `nonlinear_born_gravity_note`

**Note:** [docs/NONLINEAR_BORN_GRAVITY_NOTE.md](docs/NONLINEAR_BORN_GRAVITY_NOTE.md)  |  **Descendants:** 281  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/NONLINEAR_BORN_GRAVITY_NOTE.md.

Current audit state:
- audit_status: audited_failed
- claim_type: positive_theorem
- load_bearing_step_class: G
- claim_scope: Audited whether the provided note and runner establish, without other inputs, that nonlinear path-sum propagators generically break both Sorkin I_3 and attractive Newtonian gravity.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The numerical runner is not a first-principles derivation from the stated framework axiom; it is a toy simulation at chosen lattice sizes, propagation kernels, nonlinearities, normalizations, and field coupling. Its stdout also overstates the mass-law claim: beta remains near 1 for the nonlinear cases, while the asserted gravity failure is mainly the selected sign response. The source note’s universal conclusion does not follow from the restricted packet even if the reported runner values are accepted.

Auditor-quoted load-bearing step:
The Born rule and attractive Newtonian gravity are both consequences of linear amplitude superposition, so nonlinear propagators that give I_3 != 0 also flip the gravitational force sign.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `radial_scaling_protected_angle_narrow_theorem_note_2026-05-02`

**Note:** [docs/RADIAL_SCALING_PROTECTED_ANGLE_NARROW_THEOREM_NOTE_2026-05-02.md](docs/RADIAL_SCALING_PROTECTED_ANGLE_NARROW_THEOREM_NOTE_2026-05-02.md)  |  **Descendants:** 281  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/RADIAL_SCALING_PROTECTED_ANGLE_NARROW_THEOREM_NOTE_2026-05-02.md.

Current audit state:
- audit_status: audited_failed
- claim_type: positive_theorem
- load_bearing_step_class: A
- claim_scope: Pure Euclidean radial scaling of a first-quadrant point: slope and origin angle are preserved, doubled-angle functions are preserved, radius scales by mu, and the (1,0)-based tangent is generically not preserved.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing radial-scaling identity is a genuine class-A algebraic identity with no cited dependencies or forbidden imports. However, the note's T4 universal claim is not stated with the needed domain exclusions for the tangent denominators, so the full theorem as written does not close on its own terms. The runner source performs real symbolic checks for T1-T3 and a concrete T4 counterexample, but it does not verify the overbroad universal T4 statement.

Auditor-quoted load-bearing step:
eta_bar / rho_bar = (mu eta) / (mu rho) = eta / rho, since mu > 0 cancels.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_acceptance_suite_note`

**Note:** [docs/TELEPORTATION_ACCEPTANCE_SUITE_NOTE.md](docs/TELEPORTATION_ACCEPTANCE_SUITE_NOTE.md)  |  **Descendants:** 281  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_ACCEPTANCE_SUITE_NOTE.md.

Current audit state:
- audit_status: audited_failed
- claim_type: meta
- load_bearing_step_class: A
- claim_scope: Audited whether the note accurately documents the bounded acceptance-suite harness behavior and meaning of PASS for scripts/frontier_teleportation_acceptance_suite.py.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: the note's strict-lane profile is stale relative to the provided runner source. Why this blocks: a note whose load-bearing claim is to document the acceptance suite cannot be retained as accurate when one documented profile omits present runner probes. Repair target: sync docs/TELEPORTATION_ACCEPTANCE_SUITE_NOTE.md with the full --strict-lane --list-probes surface or split the audited claim to default-only harness behavior. Claim boundary until fixed: the cached default run supports only bounded default/optional harness telemetry, not the full documented strict-lane profile.

Auditor-quoted load-bearing step:
The suite runs existing teleportation artifacts as child processes and reports coarse PASS/FAIL/SKIP categories, including the documented default, optional, and strict-lane probe surfaces.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `mesoscopic_surrogate_threshold_2d_note`

**Note:** [docs/MESOSCOPIC_SURROGATE_THRESHOLD_2D_NOTE.md](docs/MESOSCOPIC_SURROGATE_THRESHOLD_2D_NOTE.md)  |  **Descendants:** 35  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/MESOSCOPIC_SURROGATE_THRESHOLD_2D_NOTE.md.

Current audit state:
- audit_status: audited_failed
- claim_type: bounded_theorem
- load_bearing_step_class: C
- claim_scope: A bounded finite 2D ordered-lattice support sweep over the listed topN values found no sharp collapse of the two-stage sourced-response stability criterion.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The note makes a bounded and appropriately scoped claim, not a persistent-mass or inertial-response theorem. However, its load-bearing evidence is the asserted support sweep, and that evidence is not included in the restricted packet except as prose summary. With no cited authority, no stdout, no runner source, and no log contents, the audit cannot verify that the finite sweep was actually computed or satisfied the thresholds.

Auditor-quoted load-bearing step:
Every scanned topN value stayed stable, with stage-1 and stage-2 sourced-response ratios equal to printed precision and support carry 1.000 across the scan.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `higher_symmetry_gravity_probe_note`

**Note:** [docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md](docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md)  |  **Descendants:** 11  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md.

Current audit state:
- audit_status: audited_failed
- claim_type: bounded_theorem
- load_bearing_step_class: C
- claim_scope: Audited only the fit-window-restricted gravity-side positive bump claim for dense Z2 x Z2, using the provided note, runner stdout, and runner source.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner source appears to perform an actual framework computation rather than merely printing constants, so the intended load-bearing step is class C. However, the completed runner output provided in the restricted packet is not the output for the claim as written and directly conflicts with the note's parameter setup and tabulated results. Because the claimed N=80,100,120 dense-extension mass-window and distance-sweep values are not supported by the supplied completed runner record, the chain does not close on its own terms.

Auditor-quoted load-bearing step:
Within the fit window M ∈ {2,3,5,8} the dense Z2 x Z2 extension shows a positive mass-bump fit with high R^2 at N = 80 and degrading but still positive bump-fits at N = 100, 120.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `lattice_nn_deterministic_rescale_note`

**Note:** [docs/LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md](docs/LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md)  |  **Descendants:** 3  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/LATTICE_NN_DETERMINISTIC_RESCALE_NOTE.md.

Current audit state:
- audit_status: audited_failed
- claim_type: bounded_theorem
- load_bearing_step_class: C
- claim_scope: Audited only the bounded claim that a deterministic geometry-only rescale schedule gives Born-clean NN lattice refinement through h = 0.0625 with the tabulated observables.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The note is framed as a bounded computational result, but the restricted packet contains only the reported results and no executable or textual evidence that the table was produced from the stated deterministic schedule. With no cited authorities and no runner source or output, the claimed first-principles computation cannot be verified from the provided inputs. This is not a timeout or compute-budget case in the packet; the artifact needed for audit is absent.

Auditor-quoted load-bearing step:
The canonical rows assert that the fixed geometry-only rescale schedule remains Born-clean and extends the NN lattice through h = 0.0625.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `gauge_vacuum_plaquette_first_sector_completed_triple_current_transfer_family_boundary_note_2026-04-19`

**Note:** [docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_COMPLETED_TRIPLE_CURRENT_TRANSFER_FAMILY_BOUNDARY_NOTE_2026-04-19.md](docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_COMPLETED_TRIPLE_CURRENT_TRANSFER_FAMILY_BOUNDARY_NOTE_2026-04-19.md)  |  **Descendants:** 0  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SECTOR_COMPLETED_TRIPLE_CURRENT_TRANSFER_FAMILY_BOUNDARY_NOTE_2026-04-19.md.

Current audit state:
- audit_status: audited_failed
- claim_type: no_go
- load_bearing_step_class: C
- claim_scope: Audited only the current explicit beta=6 spatial_pair witness family on the stated 1440-point dense grid over tau_transfer, tau_boundary, asym_decay, and linear_decay, with optimal scalar fitting inside gap_at as implemented by the supplied runner.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The supplied runner source does perform an actual first-principles-style computation through the imported recurrence/family machinery and sweeps the advertised 1440 grid points, rather than merely printing constants. However, the note's stronger no-realization conclusion over the audited parameter box is not established by a finite dense grid alone, and the note itself admits the dense grid is not a symbolic or interval-arithmetic global certificate. Therefore the chain does not close for the continuous-family no-go claim, though it does support a narrower empirical sampled-grid claim.

Auditor-quoted load-bearing step:
A dense 6×6×5×8 grid over the audited parameter box has minimum gap 7.791551e-03 at the stated boundary corner, so no sampled point realizes the completed triple exactly.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


## audited_numerical_match

Auditor judged the load-bearing step as a numerical fit to a tuned input scale rather than a first-principles compute. To close: derive the value from the framework's axiom rather than fitting, or accept the tuning and reclassify as a calibrated derived value.

_22 rows in this category._

### `born_scattering_comparison_note`

**Note:** [docs/BORN_SCATTERING_COMPARISON_NOTE.md](docs/BORN_SCATTERING_COMPARISON_NOTE.md)  |  **Descendants:** 439  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/BORN_SCATTERING_COMPARISON_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: positive_theorem
- load_bearing_step_class: G
- claim_scope: Audited the restricted-packet claim that the plane-wave finite-path eikonal slope is -1.28 and is closer to the stated lattice slope -1.43 than the provided 2D Gaussian beam correction.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner genuinely computes the finite-path eikonal and Gaussian-beam slopes from chosen parameter values L=15, x_src=5, beta=0.8, and b in {3..6}; it is not merely printing constants. However, the scientific conclusion is a comparison to an imported lattice slope and chosen lattice configuration, not a first-principles closure from the stated axioms. The cited dispersion authority is itself audited_conditional/open_gate, and the packet does not close the 3D beam correction or L-independence explanation.

Auditor-quoted load-bearing step:
The finite-path plane-wave eikonal formula at L=15, x_src=5 gives a power-law slope of about -1.28 on b in {3..6}, closer to the imported lattice slope -1.43 than the tested beam-averaged corrections.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `yt_constructive_uv_bridge_note`

**Note:** [docs/YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md](docs/YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)  |  **Descendants:** 326  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited the bounded claim that three chosen endpoint-preserving UV-localized bridge families can be tuned within the scanned window to reproduce y_t(v)=0.9176 with small cross-family spread.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The code performs a real numerical scan, but the scan objective is explicitly the imported target y_t(v)=0.9176 and the best rows are selected by minimizing deviation from that target. The result therefore establishes a tuned numerical match within a chosen profile class, not a first-principles computation from the stated axiom. The note itself acknowledges that deriving why the exact interacting lattice bridge belongs to this UV-localized class remains open.

Auditor-quoted load-bearing step:
Each bridge family scans the UV-localized window and selects its best fit to the accepted endpoint y_t(v)=0.9176, after which the best fits are compared for stability.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `yt_bridge_nonlocal_corrections_note`

**Note:** [docs/YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md](docs/YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md)  |  **Descendants:** 324  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Bounded numerical control of a residual endpoint-response kernel on the forced UV window for three searched bridge-profile families in the supplied runner.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner is not merely printing constants; it numerically integrates RG-like equations, fits an affine kernel on the UV window, searches profile parameters, and reproduces the note's numbers. However, the calculation depends on hard-coded external physical inputs and a target y_t viability filter, then reports small residuals for best rows selected from a chosen family grid. Because no cited retained authority or first-principles axiom derivation is provided for those inputs and modeling choices, the load-bearing step is best classified as a numerical match within a calibrated/tuned setup rather than a closed derivation.

Auditor-quoted load-bearing step:
After subtracting the affine local-Hessian model on x >= 0.95, the nonlocal residual has L2/operator-norm ratio 5.024e-3 and integrated effects at or below about 1.03e-3 on the selected viable bridge families.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `quark_cp_carrier_completion_note_2026-04-18`

**Note:** [docs/QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md](docs/QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md)  |  **Descendants:** 304  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited the bounded numerical existence claim that sector-specific complex 1-3 carriers can fit m_u/m_c, m_c/m_t, |V_us|, |V_cb|, |V_ub|, and J while keeping arg det(M_u M_d) numerically zero.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step is an optimized numerical completion using explicit solved carrier coefficients and imported comparator targets. The runner is not a trivial printout: it builds Hermitian mass matrices, diagonalizes them, computes CKM observables, and checks the determinant phase. However, the parameters xi_u and xi_d are tuned degrees of freedom rather than derived from the stated axiom, and the success criteria are external observation/atlas matches, so this is class G rather than first-principles class C.

Auditor-quoted load-bearing step:
Adding one independent complex determinant-neutral 1-3 carrier in each sector, with xi_u and xi_d solved numerically, closes the full quark mass-ratio plus CKM CP target surface.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_leptogenesis_ne_charged_source_response_reduction_note_2026-04-16`

**Note:** [docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md](docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md)  |  **Descendants:** 287  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/DM_LEPTOGENESIS_NE_CHARGED_SOURCE_RESPONSE_REDUCTION_NOTE_2026-04-16.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: positive_theorem
- load_bearing_step_class: G
- claim_scope: Audited the asserted conditional reduction from a supplied charged-lepton Hermitian source law dW_e^H to the PMNS-assisted selected-column eta value and residual 1.0106x miss.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The algebraic Schur-factorization and Hermitian-response reconstruction checks are valid as finite-dimensional identities, but the numerical near-closure is obtained after choosing canonical_h inputs and building D_- to realize that target. The source code also hard-codes the old one-flavor ratio and checks the PMNS miss against a fixed expected value, so it is not a first-principles compute from the stated axiom. The note itself concedes that evaluating D_- or dW_e^H from the sole axiom remains open.

Auditor-quoted load-bearing step:
Once dW_e^H is supplied, it reconstructs H_e, determines the N_e transport packet, and the exact selector gives eta/eta_obs = 0.989512704600.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `ckm_down_type_scale_convention_support_note_2026-04-22`

**Note:** [docs/CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md](docs/CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md)  |  **Descendants:** 286  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited the support-level numerical scale-convention identity relating threshold-local and common-scale down-type mass-ratio comparisons, conditional on the imported α_s(v), 5/6 bridge, PDG mass inputs, and QCD transport factor.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner mostly verifies arithmetic over imported constants and external PDG-style inputs, and it hard-codes the decisive full-loop transport factor as 1.14747 after noting its own one-loop computation gives a different value. The note is candid that the 5/6 bridge and the threshold-local scale choice are not theorem-grade closures. The load-bearing support is therefore a numerical match at a selected comparator scale, not a first-principles derivation or clean algebraic closure from retained inputs.

Auditor-quoted load-bearing step:
The framework prediction R_pred = (α_s(v)/√6)^(6/5) matches the threshold-local PDG ratio m_s(2 GeV)/m_b(m_b) at +0.20%, while the common-scale mismatch is explained by the imported transport factor.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `work_history.ckm.ckm_mass_basis_nni_note`

**Note:** [docs/work_history/ckm/CKM_MASS_BASIS_NNI_NOTE.md](docs/work_history/ckm/CKM_MASS_BASIS_NNI_NOTE.md)  |  **Descendants:** 286  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/work_history/ckm/CKM_MASS_BASIS_NNI_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited the bounded claim that applying mass-eigenvalue NNI normalization to Schur-complement c13 suppresses the geometric-mean |V_ub| overshoot to about 1.14 times the quoted PDG value.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner performs real matrix and ratio computations, but those computations are over hard-coded external quark masses, PDG comparator values, and fitted geometric coefficients. The quoted 1.14x |V_ub| agreement is therefore a numerical match after importing calibrated inputs, not a first-principles closure from the axiom. The runner source does not instantiate the claimed framework operators or derive the mass hierarchy internally, despite the note saying the mass ratios are framework-derived.

Auditor-quoted load-bearing step:
The conversion c_ij^phys = c_ij^geom * sqrt(m_i/m_j) for i < j applies the quark mass-ratio suppression that brings |V_ub| near PDG.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `yt_bridge_action_invariant_note`

**Note:** [docs/YT_BRIDGE_ACTION_INVARIANT_NOTE.md](docs/YT_BRIDGE_ACTION_INVARIANT_NOTE.md)  |  **Descendants:** 282  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/YT_BRIDGE_ACTION_INVARIANT_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited the bounded numerical claim that scanned UV-localized bridge profiles retained near the target endpoint show endpoint deviation dominated by the normalized gauge-surplus action I2 and a tight UV centroid.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner performs a real numerical scan rather than merely printing constants, and its stdout supports the stated bounded correlation claims within the scanned families. However, the load-bearing result depends on hard-coded physical inputs, a selected constructive bridge ansatz, a target endpoint, and finite profile-family scans rather than a first-principles derivation from the stated axiom. The note itself frames the exact interacting bridge selection of the action invariant and UV centroid as remaining theorem work, so the audited claim is a numerical reduction, not closure.

Auditor-quoted load-bearing step:
Inside the viable UV-localized class, the low-energy endpoint is controlled almost entirely by the normalized gauge-surplus action I2.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `yt_bridge_moment_closure_note`

**Note:** [docs/YT_BRIDGE_MOMENT_CLOSURE_NOTE.md](docs/YT_BRIDGE_MOMENT_CLOSURE_NOTE.md)  |  **Descendants:** 282  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/YT_BRIDGE_MOMENT_CLOSURE_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited the bounded proxy claim that the hard-coded accepted UV-localized bridge family has a nearly affine endpoint-response kernel and a narrow response-weighted moment band J_aff among near-target rows.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner performs real computation rather than merely printing constants, but it is a calibrated proxy scan with hard-coded physical inputs, target value, accepted logistic bridge, UV window, and pass thresholds. It does not instantiate the claimed microscopic axiom system to derive the moment-selection band from first principles. The note's honest boundary correctly limits the result to bounded support, but the audited load-bearing step remains a numerical proxy match on selected inputs rather than a closed theorem.

Auditor-quoted load-bearing step:
On the accepted branch bridge, the endpoint-response kernel from the rearrangement derivation is nearly affine on the viable UV-localized window, reducing the endpoint response to the two moments I2 and c2.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `yt_ew_coupling_bridge_note`

**Note:** [docs/YT_EW_COUPLING_BRIDGE_NOTE.md](docs/YT_EW_COUPLING_BRIDGE_NOTE.md)  |  **Descendants:** 282  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/YT_EW_COUPLING_BRIDGE_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited whether the EW/y_t bridge note closes a framework-native derivation of the EW coupling bridge and SM-RGE surrogate used for the y_t prediction from the restricted packet alone.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner computes a taste-threshold scan, but the decisive parameter taste_weight is selected by minimizing error against the observed sin^2(theta_W)(M_Z), which makes the load-bearing bridge class (G). Several PASS checks are comparator checks against observed sin^2, alpha_EM, and alpha_s, while other PASS checks are assertions that constants are framework-derived rather than independent computations in the shown code. The source note itself acknowledges remaining imported or open pieces, including g_2(v), lambda(v), kappa_EW, and a rigorous surrogate theorem, so the advertised closure is not clean from the restricted packet.

Auditor-quoted load-bearing step:
The SM RGE is the perturbative approximation of the framework's own RG flow, and QFP insensitivity bounds the error from using it instead of the exact lattice taste-staircase at O(3%).

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_leptogenesis_full_microscopic_reduction_note_2026-04-16`

**Note:** [docs/DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md](docs/DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md)  |  **Descendants:** 281  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/DM_LEPTOGENESIS_FULL_MICROSCOPIC_REDUCTION_NOTE_2026-04-16.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited the bounded claim that, once a full charge-preserving microscopic operator D is supplied, the PMNS-assisted DM route algorithmically reduces through D_- and H_e to the near-closing eta value.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The code does perform algebraic Schur-complement and response checks, but the decisive equality L_e = H_e is engineered by build_full_charge_preserving_operator(target_le), which receives the canonical H_e target as input. The eta value and miss factors then follow from this constructed target and hard-coded numerical expectations, not from a first-principles computation of D. The note is honest that D remains open, but the presented runner does not close the claimed microscopic reduction from the sole axiom.

Auditor-quoted load-bearing step:
dW_e^H factors exactly through the Schur value L_e = Schur_{E_e}(D_-), and L_e reproduces the canonical charged-lepton Hermitian block H_e.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_leptogenesis_transport_integral_theorem_note_2026-04-16`

**Note:** [docs/DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md](docs/DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md)  |  **Descendants:** 281  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/DM_LEPTOGENESIS_TRANSPORT_INTEGRAL_THEOREM_NOTE_2026-04-16.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: positive_theorem
- load_bearing_step_class: G
- claim_scope: Audited only the restricted claim that the stated Boltzmann transport equations, with imported reference inputs E_H(z)=1 and K_H=47.23597962989828, yield the quoted kappa and eta ratios and supersede the old fit on that branch.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner performs useful numerical checks that the direct solve and formal integral agree and that the old fit is larger on the stated branch. However, its load-bearing computation is anchored to a specific imported K_H value and imported common-module constants/functions, while the restricted packet supplies no derivation of those inputs from the axiom. That makes the claim a numerical match or branch-specific consistency check, not a first-principles theorem-native closure.

Auditor-quoted load-bearing step:
On the diagnostic radiation branch E_H(z)=1 with K_H = 47.23597962989828, the direct transport solve gives kappa_axiom,ref = 0.004829545290766509 and the formal integral reproduces it.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_pmns_chamber_spectral_completeness_theorem_note_2026-04-20`

**Note:** [docs/DM_PMNS_CHAMBER_SPECTRAL_COMPLETENESS_THEOREM_NOTE_2026-04-20.md](docs/DM_PMNS_CHAMBER_SPECTRAL_COMPLETENESS_THEOREM_NOTE_2026-04-20.md)  |  **Descendants:** 281  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/DM_PMNS_CHAMBER_SPECTRAL_COMPLETENESS_THEOREM_NOTE_2026-04-20.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: positive_theorem
- load_bearing_step_class: G
- claim_scope: Audited the compact active-chamber enumeration claim for the fixed PMNS target triple on the stated affine DM Hermitian family, excluding any upstream asymptotic no-go or full I11 closure.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: The load-bearing computation is a numerical multistart match at the fixed PMNS target and includes hard-coded expected basin coordinates/seeds, not a certified global derivation. Why this blocks: residual checks and convergence from sampled seeds show the listed roots are real candidates, but they do not prove there are no additional real ordered roots or chamber roots. Repair target: provide a symbolic elimination, Sturm/interval, Krawczyk, or equivalent exhaustive root-count certificate from the displayed equations and inequalities. Claim boundary until fixed: the packet supports numerical reproduction of the listed roots, not an exact chamber-completeness theorem.

Auditor-quoted load-bearing step:
The reduced real ordered-eigenvalue system has exactly four real roots on each of the two electron-axis-3 branches, and the independent all-permutation chamber solve finds no other chamber chi^2 = 0 roots.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_pmns_ne_seed_surface_exact_source_manifold_theorem_note_2026-04-20`

**Note:** [docs/DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md](docs/DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md)  |  **Descendants:** 281  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: positive_theorem
- load_bearing_step_class: G
- claim_scope: Audited the restricted claim that a numerically searched fixed N_e seed surface contains multiple regular preimages of the embedded physical PMNS angle triple and that listed current selector-family points miss that target.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner does perform nontrivial numerical work: it maps chart coordinates through imported PMNS machinery, uses least_squares to hit the target, computes finite-difference ranks, and evaluates selector misses. However, the decisive target is embedded as an observed physical triple, and the source representatives are obtained by polishing hard-coded starts against that target. With no cited authorities and with the imported framework routines unavailable in the packet, the claim does not close as class C first-principles compute.

Auditor-quoted load-bearing step:
The verifier exhibits multiple distinct source points on the fixed native N_e seed surface whose PMNS angle map equals the physical target triple, with rank dF_Ne = 3 at those points.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `hierarchy_dimensional_compression_note`

**Note:** [docs/HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md](docs/HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md)  |  **Descendants:** 281  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited the bounded numerical diagnostic that a chosen Lt condensate-density residual, when compressed as a dimension-4 density, is closer to the observed v_obs/v_pred prefactor than a direct sixteenth-root scale correction.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner genuinely computes the condensate-density ratio from its finite lattice Dirac operator and then performs the advertised root comparisons. However, the load-bearing conclusion is a numerical closeness claim at chosen parameters and against the imported observed prefactor C_obs, not a first-principles closure of the physical determinant-to-VEV map. The note itself caveats that the sign, placement, order parameter derivation, and full determinant-to-VEV theorem remain open.

Auditor-quoted load-bearing step:
Using the same residual ratio R, the dimension-4 effective-potential-like inverse fourth root R^(-1/4) ~= 0.96468 is in the right few-percent range, while the inverse sixteenth root R^(-1/16) ~= 0.99105 is too small.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `monopole_derived_note`

**Note:** [docs/MONOPOLE_DERIVED_NOTE.md](docs/MONOPOLE_DERIVED_NOTE.md)  |  **Descendants:** 281  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/MONOPOLE_DERIVED_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited the presented derivation of the headline monopole mass M_mono ~ 1.43 M_Planck and its stated overclosure implication from the provided note and runner packet.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing mass value is obtained by inserting a specific externally calibrated running coupling, alpha_EM^{-1}(M_Pl) ~ 72.1, into c*beta*M_Pl. That makes the headline prefactor a chosen-scale numerical result, not a closed first-principles computation from the stated lattice axiom alone. The runner contains some genuine lattice computations, but the direct numerical self-energy section visibly disagrees with the analytic headline by orders of magnitude.

Auditor-quoted load-bearing step:
M_mono = c * beta * M_Planck with c = G_lat(0) = 0.2527 and beta = 1/(4*pi*alpha_EM(M_Pl)) using alpha_EM^{-1}(M_Pl) ~ 72.1 from one-loop SM RG running.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `quark_e_channel_endpoint_quotient_law_note_2026-04-19`

**Note:** [docs/QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md](docs/QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md)  |  **Descendants:** 281  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/QUARK_E_CHANNEL_ENDPOINT_QUOTIENT_LAW_NOTE_2026-04-19.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited the bounded endpoint-rationalization claim that the live E-channel quotient near 1.876246 selects 15/8 in a numerator<=96, denominator<=32 rational scan, yielding r_E=21/4 and conditionally D_E=21/8.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner does compute the rational scan and the downstream algebra, but its central step is selecting 15/8 because it is close to the imported live endpoint quotient within a chosen low-rational class. The endpoint values, anchored solve, and shell/intercept ratio are imported from other modules not included as retained authorities in the packet. The note itself correctly says this is bounded and not a theorem; it does not close the missing derivation of 15/8 from exact tensor machinery.

Auditor-quoted load-bearing step:
Inside the controlled low-rational endpoint class, the live E-channel shell/center quotient is best rationalized by 15/8, implying r_E = 21/4 and D_E = 21/8 under the shell-multiplicity bridge.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `quark_endpoint_ratio_chain_law_note_2026-04-19`

**Note:** [docs/QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md](docs/QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md)  |  **Descendants:** 281  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/QUARK_ENDPOINT_RATIO_CHAIN_LAW_NOTE_2026-04-19.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: G
- claim_scope: Audited whether the provided note and runner derive the endpoint ratio chain {5/6, -2, -8/9} and its consequences 15/8, r_E = 21/4, and D_E = 21/8 from the restricted packet.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner verifies an exact algebraic identity and then scans a bounded small-rational class against endpoint ratios obtained from imported functions. The contested step is not a first-principles computation from the stated axiom; it is a numerical match to live endpoint data with proximity thresholds. The downstream 15/8, r_E = 21/4, and D_E = 21/8 consequences follow only after accepting the selected rational candidates.

Auditor-quoted load-bearing step:
On the live endpoint data, gamma_T(center)/gamma_T(shell), gamma_T(shell)/gamma_E(shell), and gamma_T(center)/gamma_E(center) are nearest to the small rational candidates 5/6, -2, and -8/9.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `mirror_chokepoint_boundary_fit_note`

**Note:** [docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md](docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md)  |  **Descendants:** 16  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/MIRROR_CHOKEPOINT_BOUNDARY_FIT_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: positive_theorem
- load_bearing_step_class: G
- claim_scope: Bounded finite-window report of the boundary-mirror N=40..100 pocket: Born-clean, gravity-positive, decohering through N=100 with weak descriptive exponent fit alpha = -0.245 (R^2 = 0.126) and a gravity wall at N=120. Excludes any retained mirror family theorem or asymptotic law; the audit row carries no registered runner/log artifacts.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Re-audit confirms the original numerical-match verdict: a finite parameter-pocket fit with weak R^2, not a derived asymptotic. Scope narrowed from the migration backfill to a bounded finite-window report.

Auditor-quoted load-bearing step:
The boundary mirror family is a Born-clean, gravity-positive, decohering pocket through N=100, with canonical exponent fit alpha=-0.245 but no bounded asymptotic claim.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `lattice_distance_law_note`

**Note:** [docs/LATTICE_DISTANCE_LAW_NOTE.md](docs/LATTICE_DISTANCE_LAW_NOTE.md)  |  **Descendants:** 10  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/LATTICE_DISTANCE_LAW_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: positive_theorem
- load_bearing_step_class: G
- claim_scope: Audited only the note's claim that the specified no-barrier ordered 2D lattice harness exhibits an approximate |delta| ~ 1/b distance-magnitude fit over b >= 7.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step is a numerical power-law fit on a selected far-field window and fixed harness parameters, not a first-principles derivation from the axiom in the restricted packet. No cited authorities or runner artifacts are available to independently close the computation. The note may document an interesting empirical lattice fit, but the presented chain does not establish a clean theorem-level distance law from provided inputs alone.

Auditor-quoted load-bearing step:
The ordered lattice gives a clean distance-dependent magnitude law on the far-field window b >= 7: |delta| ~= 23.5071 * b^(-1.052), R^2 = 0.9850.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `wave_direct_dm_h025_seed0_crossfamily_note`

**Note:** [docs/WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_NOTE.md](docs/WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_NOTE.md)  |  **Descendants:** 8  |  **Class:** G

```
Use the physics-loop skill to close the missing derivation in docs/WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: positive_theorem
- load_bearing_step_class: G
- claim_scope: Bounded observation: at H=0.25 with seed 0, two selected control rows from Fam1 and Fam2 share negative sign, common ordering, and weak-field control on the seed-0 fine-H surface. Excludes any structural theorem, stable amplitude law, or portability claim beyond the listed two rows; the source rows and runner/log artifacts are not registered as audit dependencies.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Re-audit confirms the original numerical-match verdict: two-row compression, not a family theorem. Scope narrowed from the migration backfill to the bounded two-row observation.

Auditor-quoted load-bearing step:
The seed-0 fine-H surface is consistent across families in sign, ordering, and weak-field control, but it still does not define a stable amplitude law or a portability claim beyond Fam1/Fam2.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `source_resolved_exact_green_self_consistent_note`

**Note:** [docs/SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_NOTE.md](docs/SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_NOTE.md)  |  **Descendants:** 0  |  **Class:** D

```
Use the physics-loop skill to close the missing derivation in docs/SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_NOTE.md.

Current audit state:
- audit_status: audited_numerical_match
- claim_type: bounded_theorem
- load_bearing_step_class: D
- claim_scope: Bounded finite-run statement for the specified h=0.25, W=3, L=6 lattice, source cluster, kernel, source strengths, calibration gain, and single self-consistency update.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Issue: the load-bearing positive is established by a calibrated finite numerical run, with the gain chosen so max |f| reaches the target cap at s=0.008. Why this blocks: the runner output supports the bounded table and sign/scaling readout, but has no explicit PASS/FAIL assertion wrapper and the comparator amplitude is calibration-dependent. Repair target: add explicit assertions for zero-source exactness, TOWARD sign, exponent tolerances, and declare the calibrated gain as an input rather than evidence of independent physical amplitude. Claim boundary until fixed: acceptable only as a narrow refinement-positive numerical pocket for the frozen setup, not as a full self-consistent field theory.

Auditor-quoted load-bearing step:
A compact exact h=0.25 lattice with a boundary-clipped 4-node source cluster preserves zero-source reduction, TOWARD sign in 4/4 rows, linear F~M scaling, and nontrivial self-consistent Green deflections after one reweighting update.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


## open_gate

Author explicitly labeled the row as open work. The audit confirmed the labeling is honest. To close: complete the missing derivation that the gate is tracking, then have it re-audited as a theorem.

_19 rows in this category._

### `staggered_dirac_realization_gate_note_2026-05-03`

**Note:** [docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md](docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)  |  **Descendants:** 567  |  **Class:** E

```
Use the physics-loop skill to close the missing derivation in docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: E
- claim_scope: Canonical open-gate parent identity for the unresolved staggered-Dirac realization derivation from A1 (Cl(3)) plus A2 (Z^3), including Grassmann realization, staggered kinetic structure, BZ-corner doublers, and the three-generation physical-species bridge.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The note is clean only under the open_gate scope: it defines a canonical parent object for an unresolved derivation target and repeatedly states that the substantive A1+A2-to-staggered-Dirac chain is not closed. There is no hidden theorem promotion, no runner-bearing numerical match, and no decoration claim. Residual risk is governance-only: a future theorem audit must not cite this clean open-gate verdict as proof of the staggered-Dirac realization itself.

Auditor-quoted load-bearing step:
This note's load-bearing content is identity assignment only.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_selector_first_shoulder_exit_threshold_support_note_2026-04-21`

**Note:** [docs/DM_SELECTOR_FIRST_SHOULDER_EXIT_THRESHOLD_SUPPORT_NOTE_2026-04-21.md](docs/DM_SELECTOR_FIRST_SHOULDER_EXIT_THRESHOLD_SUPPORT_NOTE_2026-04-21.md)  |  **Descendants:** 283  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/DM_SELECTOR_FIRST_SHOULDER_EXIT_THRESHOLD_SUPPORT_NOTE_2026-04-21.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: A
- claim_scope: The exact threshold-volume family contains a unique earliest middle-branch breakpoint tau_b,min at recovered lift 0, this breakpoint lies inside the prior stabilization window, and evaluating the field there selects lift 0; no physical threshold law is claimed.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step is an algebraic check over existing recovered-bank inputs: compute tau_b = log(1+b), verify its unique minimum at lift 0, compare it with the stabilization-window endpoints, and evaluate V_tau there. The cached runner completes with PASS=11 FAIL=0 and its substantive checks match the note's reported tau_b values and selector values. The runner does not derive a physical law, but the source note does not claim one; it states the remaining selector-side burden explicitly. Residual risk is dependency-grade rather than scope failure, but under the audited open-gate scope the chain closes.

Auditor-quoted load-bearing step:
For each recovered lift, tau_b(i) = log(1 + b_i); on the recovered bank the minimum is unique, belongs to lift 0, lies inside the stabilization window, and V_tau at that breakpoint makes lift 0 the unique minimizer.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `dm_wilson_direct_descendant_schur_feshbach_boundary_variational_theorem_note_2026-04-25`

**Note:** [docs/DM_WILSON_DIRECT_DESCENDANT_SCHUR_FESHBACH_BOUNDARY_VARIATIONAL_THEOREM_NOTE_2026-04-25.md](docs/DM_WILSON_DIRECT_DESCENDANT_SCHUR_FESHBACH_BOUNDARY_VARIATIONAL_THEOREM_NOTE_2026-04-25.md)  |  **Descendants:** 281  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/DM_WILSON_DIRECT_DESCENDANT_SCHUR_FESHBACH_BOUNDARY_VARIATIONAL_THEOREM_NOTE_2026-04-25.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: A
- claim_scope: Finite-dimensional Schur-Feshbach boundary theorem for L_e=Schur_{E_e}(D_-) under stated invertibility and positive-Hermitian hypotheses, excluding evaluation of D_-, Wilson-native support construction, and final DM selector closure.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing step is a standard Schur-complement/Feshbach identity and positive-definite quadratic completion, not a renamed physical observable or tuned numerical comparator. The runner cache completed successfully with 42/42 passes and checks the relevant block algebra, determinant response, elimination equation, positive variational principle, trial-map certificate, and monotonicity; its document-wiring checks are hygiene rather than physics closure. No hidden DM closure is imported because the audited scope explicitly stops at the boundary object once D_- is supplied.

Auditor-quoted load-bearing step:
The exact block factorization of D_- with middle block diag(L_e,F), where L_e=A-BF^(-1)C, gives I_e^* D_-^(-1) I_e=L_e^(-1); under D_-=D_-^*>0, completing the square gives u^*L_eu=min_v [u;v]^*D_-[u;v].

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `newton_derivation_note`

**Note:** [docs/NEWTON_DERIVATION_NOTE.md](docs/NEWTON_DERIVATION_NOTE.md)  |  **Descendants:** 24  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/NEWTON_DERIVATION_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: A
- claim_scope: Audited the Newtonian mass-scaling note as an open gate: on the retained ordered-lattice family, the algebra selects p=1 only conditional on a phase valley, linear propagation, momentum conservation, and an as-yet-unclosed persistent-pattern inertial mass parameter extensive under the same composition law as the source parameter s.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The row should be clean only as an open gate, not as a retained Newtonian derivation. The one-hop dependency, docs/EQUIVALENCE_PRINCIPLE_HARNESS_NOTE.md, is retained_bounded and supports only amplitude-scaling invariance plus packet-shape dependence on a fixed test-particle family; it does not close the persistent-pattern inertial-mass bridge. The source note preserves that boundary and states the missing theorem explicitly, so the audited object is a valid open gate blocking retained propagation.

Auditor-quoted load-bearing step:
If the inertial quantity of a persistent pattern is an extensive quantity attached to the same composition law as the field-source parameter s, then m proportional to s.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `gauge_wilson_isotropy_boundary_note_2026-05-04`

**Note:** [docs/GAUGE_WILSON_ISOTROPY_BOUNDARY_NOTE_2026-05-04.md](docs/GAUGE_WILSON_ISOTROPY_BOUNDARY_NOTE_2026-05-04.md)  |  **Descendants:** 18  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/GAUGE_WILSON_ISOTROPY_BOUNDARY_NOTE_2026-05-04.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: A
- claim_scope: Audited the boundary claim that two proposed PR #528 mechanisms do not force a new anisotropic Wilson gauge action, leaving the accepted isotropic Wilson surface scoped and unchanged.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The claim is correctly scoped as an open gate and narrow boundary record, not as retained theorem propagation. The algebraic Clifford checks and staggered eta-product checks close from the supplied runner and do not import an unapproved physical bridge. The cited retained_bounded Wilson grammar supports the statement that no new anisotropic action is added here, while the note explicitly leaves broader spacetime-emergence routes open.

Auditor-quoted load-bearing step:
The Cl(3) pseudoscalar is central rather than a fourth anticommuting generator, and the staggered eta plaquette products are identical across all six orientations, so these two routes do not derive a spatial/temporal gauge-coupling split.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `gauge_scalar_temporal_observable_bridge_stretch_note_2026-05-02`

**Note:** [docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md](docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md)  |  **Descendants:** 7  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: A
- claim_scope: Open-gate claim that the full interacting Wilson plaquette expectation to completed local one-plaquette response bridge is not derived from A_min/current retained Wilson inputs; positive bridge promotion remains blocked pending a new exact nonperturbative primitive.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The audited claim is not a positive derivation of <P>_full = R_O(beta_eff); it is the open-gate/named-obstruction statement that this bridge is not closed by A_min. The one-hop dependencies are retained-grade for this scope: the temporal completion theorem is retained_bounded at kernel level, and the no-go theorem is retained_no_go for the bridge from the current Wilson packet. The runner completes and checks the note structurally, with PASS=33 and FAIL=0, but does not compute a positive bridge; that is consistent with the open_gate scope.

Auditor-quoted load-bearing step:
The bridge <P>_full = R_O(beta_eff) cannot be derived analytically from A_min alone, so the observable-level bridge remains open rather than promoted as a positive plaquette derivation.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `lattice_nn_continuum_note`

**Note:** [docs/LATTICE_NN_CONTINUUM_NOTE.md](docs/LATTICE_NN_CONTINUUM_NOTE.md)  |  **Descendants:** 4  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/LATTICE_NN_CONTINUUM_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: C
- claim_scope: Raw nearest-neighbor lattice refinement is Born-clean through h = 0.25, with h = 0.125 unresolved and the continuum question left open.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The scoped claim is deliberately bounded: it asserts the retained finite-spacing window and explicitly leaves the continuum limit unresolved. The current runner output matches the note's numerical rows through h = 0.25 and cleanly reports failure at h = 0.125, so the open gate is supported on its own terms. Residual risk is confined to any future continuum or finer-spacing claim, which this note explicitly does not make.

Auditor-quoted load-bearing step:
The nearest-neighbor lattice shows a Born-clean positive refinement trend through h = 0.25, while h = 0.125 remains unresolved and no full continuum theorem is claimed.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `lattice_nn_high_precision_note`

**Note:** [docs/LATTICE_NN_HIGH_PRECISION_NOTE.md](docs/LATTICE_NN_HIGH_PRECISION_NOTE.md)  |  **Descendants:** 2  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/LATTICE_NN_HIGH_PRECISION_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: C
- claim_scope: The raw nearest-neighbor high-precision h = 0.125 continuation remains open; no canonical Born-clean h = 0.125 extension is promoted.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The seeded positive_theorem label is not the note's actual scoped claim. The note explicitly says the h = 0.125 attempt did not complete, produced no retained numerical result, and should not be promoted as a canonical Born-clean extension. Under the timeout/noncompletion policy, this is a clean open gate rather than a failed or conditional theorem.

Auditor-quoted load-bearing step:
The h = 0.125 continuation did not complete in a practical runtime window and did not produce a retained numerical result.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_taste_readout_operator_model_note`

**Note:** [docs/TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE.md](docs/TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE.md)  |  **Descendants:** 2  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_TASTE_READOUT_OPERATOR_MODEL_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: A
- claim_scope: Finite-dimensional operator-factorization audit for dims 1-3 and sides 2,4 of retained-last-KS-taste-bit readout, correction, Bell-projector, and no-record separation checks.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The load-bearing classification is a finite algebraic operator-factorization check, not a renaming or tuned numerical comparison. The runner source constructs the lattice/taste operators and Frobenius projections directly, then uses expected pass/fail rules only as consistency checks after computing residuals. The note's conclusion is appropriately bounded: retained-axis logical operators factor, native parity Z fails in dim > 1, and physical apparatus claims remain open rather than asserted.

Auditor-quoted load-bearing step:
Native sublattice parity Z is the product of all taste Z signs, so in 2D and 3D it changes across spectator taste sectors and fails to factor as O_logical tensor I_env for the retained last taste bit.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_bell_measurement_circuit_note`

**Note:** [docs/TELEPORTATION_BELL_MEASUREMENT_CIRCUIT_NOTE.md](docs/TELEPORTATION_BELL_MEASUREMENT_CIRCUIT_NOTE.md)  |  **Descendants:** 1  |  **Class:** B

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_BELL_MEASUREMENT_CIRCUIT_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: B
- claim_scope: An ideal logical/taste Bell-measurement decomposition is verified algebraically, but the native physical gate/readout/apparatus implementation remains an explicit open dependency.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The packet supports the bounded logical decomposition with exact matrix identities up to numerical precision, and all acceptance gates pass. It does not claim a physical native schedule, apparatus Hamiltonian, decoherence model, or durable measurement-record derivation. Because that physical mechanism is explicitly left open, the correct retained object is a clean open gate rather than a theorem about implementable teleportation hardware.

Auditor-quoted load-bearing step:
The Bell-measurement limitation is narrowed from an undecomposed ideal Bell projector to an ideal logical/taste stabilizer or CNOT-H circuit measurement, while physical implementation of those logical primitives remains open.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_encoding_portability_note`

**Note:** [docs/TELEPORTATION_ENCODING_PORTABILITY_NOTE.md](docs/TELEPORTATION_ENCODING_PORTABILITY_NOTE.md)  |  **Descendants:** 1  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_ENCODING_PORTABILITY_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: C
- claim_scope: Finite algebraic audit of ideal encoded taste-qubit teleportation over even side lengths 2, 4, 6, and 8 in dimensions 1, 2, and 3, showing current_fixed_x works only for last-axis encodings while axis_adapted_x works for all surveyed encodings.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The correct scoped object is a clean open_gate: it identifies a standalone operator-targeting gap in the current fixed pair-hop X, not a retained broad teleportation theorem. The runner confirms the bounded failure for all non-last logical axes in dimensions 2 and 3 and confirms that retargeting X removes the obstruction across the surveyed cases. The note also preserves the finite, idealized boundary and does not overclaim physical teleportation, matter transfer, or larger lattices.

Auditor-quoted load-bearing step:
Keeping the current row-major pair-hop X while selecting a non-last logical taste axis fails because X flips the last taste bit rather than the selected logical bit.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_logical_readout_audit`

**Note:** [docs/TELEPORTATION_LOGICAL_READOUT_AUDIT.md](docs/TELEPORTATION_LOGICAL_READOUT_AUDIT.md)  |  **Descendants:** 1  |  **Class:** B

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_LOGICAL_READOUT_AUDIT.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: B
- claim_scope: The audit validates reduced logical trace extraction for taste-only observables in the audited Poisson/CHSH cases, while identifying operational retained-taste readout/control as still unestablished.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
This row is best treated as a clean open_gate rather than a theorem claim. The note does establish the mathematical reduced-density diagnostic for taste-only observables, but its citeable load-bearing content is the blocker: trace extraction alone is not an operational logical readout primitive. The runner output directly supports that distinction and does not rely on one-hop cited authorities.

Auditor-quoted load-bearing step:
Cells and spectators can be ignored only if preparation, Bell measurement, correction, and readout are proven to factor as logical taste operators tensor identity on the environment, or an explicit blind/heralded environment workflow is supplied.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_resource_fidelity_note`

**Note:** [docs/TELEPORTATION_RESOURCE_FIDELITY_NOTE.md](docs/TELEPORTATION_RESOURCE_FIDELITY_NOTE.md)  |  **Descendants:** 1  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_RESOURCE_FIDELITY_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: C
- claim_scope: Bounded open-gate harness for ordinary single-qubit state teleportation using a supplied two-qubit resource density matrix with ideal Bell measurement, two-bit classical record, and Bob-side Pauli correction.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The note is explicitly scoped to a fixed density-matrix teleportation protocol and keeps the physical boundary narrow. The runner does not merely hard-code the threshold: it computes the corrected channel and Choi average fidelity independently of the Bell-overlap prediction, then checks the formula error, isotropic bracket, no-pre-message Bob input-independence, trace preservation, and resource physicality. Current runner output matches the note and all acceptance gates pass. Residual risk is only scope risk: this clean verdict makes the bounded open-gate harness citeable, not the broader teleportation lane retained.

Auditor-quoted load-bearing step:
For this fixed Bell-basis measurement and fixed Pauli-correction convention, the exact average fidelity obeys F_avg = (1 + 2 * <Phi+|rho|Phi+>) / 3, so the fixed-protocol threshold is <Phi+|rho|Phi+> > 1/2.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `carrier_orbit_invariance_stretch_attempt_note_2026-05-03`

**Note:** [docs/CARRIER_ORBIT_INVARIANCE_STRETCH_ATTEMPT_NOTE_2026-05-03.md](docs/CARRIER_ORBIT_INVARIANCE_STRETCH_ATTEMPT_NOTE_2026-05-03.md)  |  **Descendants:** 0  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/CARRIER_ORBIT_INVARIANCE_STRETCH_ATTEMPT_NOTE_2026-05-03.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: A
- claim_scope: Audited the narrow open-gate claim that the carrier swap problem admits a Z_2 isotypic decomposition and that the remaining obstruction is registry closure of antisymmetric carrier primitives, not closure of the upstream swap-reduction theorem.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The runner completed with SUMMARY: PASS=52 FAIL=0 and checks the Z_2 carrier action, isotypic/operator decompositions, current-surface bounded-primitive/textual registry checks, and explicit naming of registry closure. The audited scope is an open gate: it cleanly narrows the residual to registry closure, while explicitly refusing to claim absolute structural exhaustion. Residual risk is that parts of the registry enumeration are textual/current-surface checks, so this verdict must not be read as proving no future retained primitive can add an antisymmetric component.

Auditor-quoted load-bearing step:
The structural-exhaustion question reduces to: does the retained primitive registry contain any (V*)^- element, with registry closure named as the remaining meta-mathematical residual.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_3d1_causal_record_channel_note`

**Note:** [docs/TELEPORTATION_3D1_CAUSAL_RECORD_CHANNEL_NOTE.md](docs/TELEPORTATION_3D1_CAUSAL_RECORD_CHANNEL_NOTE.md)  |  **Descendants:** 0  |  **Class:** A

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_3D1_CAUSAL_RECORD_CHANNEL_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: A
- claim_scope: 3D+1 discrete planning harness for causal classical Bell-record propagation in ordinary qubit teleportation, explicitly bounded to exclude derivation of the Bell record, Bell resource, measurement dynamics, matter transfer, and faster-than-light signaling.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
Clean only as an open-gate/planning-boundary claim. The runner checks consistency of an explicit classical Bell-record channel on a discrete 3D+1 lattice and the note clearly says the Bell record, Bell resource, and measurement dynamics are supplied rather than derived. No retained physics theorem beyond that bounded channel claim is established or implied.

Auditor-quoted load-bearing step:
The channel schedules and delivers the record inside the configured 3D+1 light cone, while explicitly not deriving the Bell bits, Bell resource, or measurement dynamics.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_3d_initial_ramp_probe_note`

**Note:** [docs/TELEPORTATION_3D_INITIAL_RAMP_PROBE_NOTE.md](docs/TELEPORTATION_3D_INITIAL_RAMP_PROBE_NOTE.md)  |  **Descendants:** 0  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_3D_INITIAL_RAMP_PROBE_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: C
- claim_scope: Exact side=2/N=8 3D Poisson ramp diagnostic under the listed runner: null control, high best-Bell resource candidate, and a native-basis G=0 preparation blocker; no scalability, robustness, readout, or non-teleportation transport claim.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The audited claim is a planning boundary, not a resource theorem. The source note and runner output agree on the load-bearing facts: the null control is clean, the side-2 Poisson endpoint and finite-time ramp meet the stated Bell/overlap thresholds, and the G=0 initial state remains maximally delocalized in the native basis. Because the note explicitly limits the conclusion to a side-2 resource candidate with unresolved preparation/scaling/readout gaps, it cleanly establishes a citeable open gate.

Auditor-quoted load-bearing step:
Combined preparation verdict: unresolved gap; the side-2 ramp is a useful 3D resource candidate, but the required G=0 initial state is maximally delocalized in the native basis and no scalable preparation, control, noise, or readout proof is supplied.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_initial_state_preparation_probe_note`

**Note:** [docs/TELEPORTATION_INITIAL_STATE_PREPARATION_PROBE_NOTE.md](docs/TELEPORTATION_INITIAL_STATE_PREPARATION_PROBE_NOTE.md)  |  **Descendants:** 0  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_INITIAL_STATE_PREPARATION_PROBE_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: C
- claim_scope: For the default 1D N=8 and 2D 4x4 G=0 teleportation probes, the initial state is unique, separable, exactly an H1-ground tensor product, and maximally native-site delocalized; operational preparation beyond that finite diagnostic remains open.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The scoped open gate closes cleanly: the note records finite diagnostic facts and a bounded operational gap, not a claimed physical implementation. The runner verifies the load-bearing properties on both default small G=0 surfaces, including uniqueness, exact product structure, separability, and failure of native-basis localization by the stated threshold. Residual risk is explicit in the claim boundary: scaling, noise, cooling/control, and readout remain unaudited open work.

Auditor-quoted load-bearing step:
The assumed G=0 state is a unique separable H1-ground tensor product on the default small surfaces, but it is fully delocalized in the native site basis and the artifact supplies no cooling/control/readout protocol, noise model, or scaling proof.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_native_transport_theory_note`

**Note:** [docs/TELEPORTATION_NATIVE_TRANSPORT_THEORY_NOTE.md](docs/TELEPORTATION_NATIVE_TRANSPORT_THEORY_NOTE.md)  |  **Descendants:** 0  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_NATIVE_TRANSPORT_THEORY_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: C
- claim_scope: Open-gate transport theory note: assuming the stated base/fiber split, Pauli-frame connection, causal record section, branch-record, and holonomy bookkeeping axioms, the listed algebraic invariants hold, while nature-grade native teleportation remains explicitly unclosed pending native physical derivations.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The source note explicitly withholds promotion and states that the transport vocabulary is candidate lane theory. The runner checks only the algebraic consequences of the assumed Pauli-frame/record formalism and explicitly reports nature-grade unconditional closure as HOLD. Because the audited object is the open-gate articulation rather than a positive physical derivation, there is no hidden physical identification being ratified as closed physics; the missing Bell resource, measurement, record carrier, apparatus, noise model, and conservation-ledger derivations are preserved as the blocker.

Auditor-quoted load-bearing step:
The note's retained claim is not native teleportation closure, but the open-gate boundary that Pauli-frame transport invariants are only conditional formal structure until Bell-resource preparation, durable Bell records, record carriers, apparatus/noise, and conservation ledgers are derived from native dynamics.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```


### `teleportation_three_register_cross_encoding_note`

**Note:** [docs/TELEPORTATION_THREE_REGISTER_CROSS_ENCODING_NOTE.md](docs/TELEPORTATION_THREE_REGISTER_CROSS_ENCODING_NOTE.md)  |  **Descendants:** 0  |  **Class:** C

```
Use the physics-loop skill to close the missing derivation in docs/TELEPORTATION_THREE_REGISTER_CROSS_ENCODING_NOTE.md.

Current audit state:
- audit_status: audited_clean
- claim_type: open_gate
- load_bearing_step_class: C
- claim_scope: Bounded finite numerical audit showing that, for the default surveyed KS taste-qubit geometries and sampled A/R/B encoding triples, ideal three-register teleportation passes with axis-adapted Bell measurement, identity logical resource map, and axis-adapted Bob corrections, while the stated controls fail only on their expected boundaries.

Auditor's verdict_rationale (why this isn't yet a closed derivation):
The clean verdict applies only to the open-gate artifact: a bounded finite-survey planning result over ideal encoded taste qubits. The runner does not merely restate the conclusion; it builds the surveyed encodings, logical operators, Bell projectors, teleportation trials, no-signaling metrics, and negative controls, and the current output matches the source note. The note explicitly excludes apparatus dynamics, physical resource preparation, durable records, Hamiltonian transport, noise, matter/object transfer, and faster-than-light signaling, so those missing physical bridges do not block the scoped artifact. Residual risk is limited to the finite sampling boundary: dim 2 side 4, dim 3 side 2, and dim 3 side 4 are capped at 512 triples per geometry rather than exhaustive over all possible triples.

Auditor-quoted load-bearing step:
Within the bounded default survey, the obstruction is not three-register cross-encoding itself; the intended logical protocol passes when the A/R Bell measurement is explicitly adapted to the two Alice-side encodings and Bob's corrections are adapted to Bob's chosen encoding.

Goal: close the chain so a re-audit of this same note can land
audited_clean at retained-grade. Use the physics-loop skill to iterate.
Do not over-prescribe approach — explore the framework, let the skill
drive.
```

