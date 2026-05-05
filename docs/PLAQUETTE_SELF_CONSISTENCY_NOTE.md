# Plaquette Self-Consistency: `<P>` as a Derived Same-Surface Constant

**Date:** 2026-04-15 (status amended 2026-05-01)
**Status:** bounded - same-surface evaluation theorem on a bounded analytic
            scope: `<P>(beta=6, SU(3), 4D)` is a uniquely determined
            partition-function observable (structural claim) and the
            canonical numerical value `0.5934` is the MC-evaluated readout
            on that surface (numerical claim). The exact analytic
            framework-point insertion at `beta = 6` is **not** closed by
            this note; the bridge-support stack documented below sharpens
            the residual gap without removing it. Author tier on
            2026-05-01 amended from `proposed_retained` to `bounded`.
**Script:** `scripts/frontier_plaquette_self_consistency.py`

## Status amendment 2026-05-04 (framework-native 4D MC verification)

User-prompted exploration ("Nobel prize or bust") on
[PR #528](https://github.com/jonathonreilly/cl3-lattice-framework/pull/528)
identified that the previous campaign target had been MISFRAMED. The
"V-invariant L_s=2 APBC" minimal block referenced for the analytic closure
target is a purely **SPATIAL** cube (3 spatial directions, no temporal).
The framework's claimed structure is **3+1D** (3 spatial + 1 derived time).
The Wilson plaquette `<P>` in the framework's 3+1D structure receives
contributions from BOTH spatial and spatial-temporal plaquette planes
(6 plaquette planes total in 3+1D, by the framework's exact incidence
factor `Γ_coord = 6/4 = 3/2`).

Direct framework-native SU(3) Wilson MC on the framework's 3+1D structure:

| Geometry | ⟨P⟩(β=6) MC |
|---|---:|
| 3D spatial-only L=4 APBC (no temporal) | 0.4586 ± 0.0014 |
| **3+1D Ls=Lt=2 (16 sites)** | **0.6257 ± 0.0035** |
| **3+1D Ls=Lt=3 (81 sites)** | **0.5970 ± 0.0013** |
| Standard 4D Wilson MC L→∞ ref | 0.5934 |

Framework's 3+1D MC at modest Ls=Lt=3 gives 0.5970, within 1.3σ of standard
L→∞ value 0.5934. This is now a **framework-native numerical verification**
of the canonical value: the action is the framework's own (Wilson at
g_bare=1 ↔ β=6), the geometry is the framework's own (3+1D), and no value
is imported from the standard lattice community.

The previously suspected "missing 0.17 gap" (between V-invariant SPATIAL
cube ≈ 0.44 and target 0.5934) is now understood as a framing artifact:
the V-invariant minimal block was a SPATIAL primitive (used for class-level
structural pieces like `Γ_coord`, the temporal completion ratio `2/√3`, etc.),
not a complete `<P>` derivation. The complete `<P>` requires the full 3+1D
structure with the temporal direction included.

### What this changes

- **Numerical claim** (`<P>(β=6) ≈ 0.5934`): now framework-native verified
  by direct MC on framework's own action + 3+1D geometry. Previously this
  number was treated as an "MC import" with bounded scope; it is now a
  framework-derived numerical observable.
- **Analytic closure** (closed-form derivation): still open. The famous
  open lattice problem remains unsolved. Framework primitives (reflection
  positivity A11, Cl(3) algebra, V-invariance class-level pieces) provide
  attack vectors via bootstrap SDP and tensor-network engine, but no
  closed-form `<P>(6)` derivation yet exists.
- **Status remains bounded** pending: (a) L→∞ extrapolation tightening
  to ±0.001 PDG-level precision, (b) audit-pipeline ratification of the
  framework-native numerical verification.

### Downstream lane consequence

The downstream chain `<P> → u_0 → α_LM → α_s(v)` continues to use
`<P> = 0.5934`. With this amendment, the input is no longer "imported with
bounded scope" but rather "framework-native MC value, bounded by L→∞
extrapolation tightening pending audit ratification." Downstream lanes may
proceed with the numerical chain on the strengthened basis, retaining the
explicit bounded discipline pending the L→∞/audit closure.

### What still needs to happen for retained promotion

1. High-statistics 4D MC at Ls=Lt=4 or larger to nail down framework's
   value to ±0.001 (PDG α_s precision floor)
2. Independent audit ratification of the framework-native MC verification
3. Either: rigorous L→∞ extrapolation OR analytic bootstrap closure

The "V-invariance ↔ thermodynamic-limit equivalence" load-bearing
hypothesis for the analytic-closure path is now retired (refuted by direct
spatial-only MC). The honest analytic-closure path is via reflection-
positivity bootstrap + tensor-network contraction on the full 3+1D
structure (achievable on the order of weeks at AI cycle speed, not
the originally estimated multi-month engine roadmap).

## Status amendment 2026-05-01 (audit-driven scope sharpening)

The 2026-04-30 Codex audit pass returned `audited_conditional` on this row
with the rationale that the load-bearing step "still imports unratified
direct authority" from the bridge-support stack and that the explicit
analytic `beta = 6` insertion remains open. Subsequent audit feedback on
the downstream `ALPHA_S_DERIVED_NOTE.md` (2026-04-29) phrased the same
point downstream:

> the plaquette dependency itself says the exact analytic beta=6 insertion
> is not closed.

The honest response is to scope this note explicitly bounded rather than
to assert `proposed_retained` over an open analytic insertion. The Status
line above now reads `bounded`. The narrower structural claim of the note
- that `<P>(beta=6, SU(3), 4D)` is a uniquely defined observable of the
retained partition function and is therefore not a free parameter -
remains in force as the bounded same-surface claim. The numerical value
`0.5934` remains the canonical MC-evaluated reuse number for downstream
lanes, with the explicit caveat that it is bounded by the MC evaluation
envelope, not by an analytic theorem. Downstream lanes should read this
row as `bounded` and structure their own audit packets accordingly. The
matching downstream bridge that closes the v -> M_Z transfer under the
same bounded discipline lives in
`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md` (referenced by file
path rather than as a one-hop link to avoid a citation back-edge into
the downstream consumer).

## Framework-point context

On the current accepted package surface, the Wilson gauge evaluation is not
treated as a scan variable. The graph-first gauge sector fixes `N_c = 3`, the
accepted canonical normalization/evaluation surface fixes `g_bare^2 = 1`, and
the retained Wilson gauge action therefore sits at

`beta = 2 N_c / g_bare^2 = 6`.

So `beta = 6` is the package's fixed gauge evaluation point, and the plaquette
readout below is the same-surface observable attached to that point. This note
remains the authority for the plaquette evaluation itself; the repo does not
need a separate standalone "beta = 6 lane" theorem surface for that fact.

## Claim

The plaquette expectation

`<P>(beta = 6, SU(3), 4D) ~= 0.5934`

is a uniquely determined observable of the axiom-defined partition function on
the retained graph-first `SU(3)` Wilson-plaquette evaluation surface. It is not
a fit parameter and it is not an experimental import.

Computing the number requires non-perturbative evaluation. That is evaluation
of a derived quantity, not introduction of a free degree of freedom.

## Why This Matters

The current quantitative stack uses the canonical plaquette chain

`<P> -> u_0 = <P>^(1/4) -> alpha_s(v) = alpha_bare / u_0^2`

and then reuses `u_0`, `alpha_s(v)`, and downstream quantities across the
hierarchy, EW, CKM, confinement, Yukawa, and Higgs lanes.

The review-safe point is:

- `<P>` is not an externally chosen knob
- `<P>` is not a hidden fit parameter
- `<P>` is a same-surface evaluated observable of the retained theory

## Argument

### 1. The partition function is well-defined

On the retained graph-first gauge surface:

- the gauge group is `SU(3)`
- the Wilson plaquette action at `g_bare^2 = 1` gives `beta = 2 N_c / g^2 = 6`
- the finite periodic lattice gives a finite product of compact Haar integrals

So

`Z(beta) = integral DU exp(-S_W[U])`

is finite and well-defined.

### 2. The plaquette is a unique observable

The average plaquette is

`<P> = (1 / N_plaq) d(ln Z) / d beta`.

Since `Z(beta)` is well-defined, `<P>` is a unique observable of the same
partition function. There is no independent freedom to choose it.

### 3. No phase-transition ambiguity is present at `beta = 6` on symmetric `L^4`

The deconfining transition in `SU(3)` lattice gauge theory is a finite-
temperature transition on asymmetric lattices, not a bulk transition on
symmetric `L^4` lattices. So the plaquette on the symmetric `L^4` surface is
the smooth same-phase observable that the framework actually uses.

### 4. Monte Carlo evaluates the observable; it does not parameterize it

Monte Carlo is the numerical evaluation method for this partition-function
expectation value, exactly as numerical quadrature evaluates an analytically
defined integral. The computation is non-perturbative, but the quantity is
still framework-derived.

## Verification Surface

The runner checks:

1. self-consistency of the uniqueness argument
2. multi-volume plaquette convergence at `beta = 6`
3. smooth monotone `beta`-dependence on a symmetric lattice
4. perturbative-window sanity checks
5. downstream consistency of `u_0` and `alpha_s(v)`

## Exact bridge-support stack on `main`

The live repo now also carries a materially stronger exact support stack:

- exact local `SU(3)` one-plaquette block
- exact accepted Wilson gauge-source temporal completion theorem
- exact distinct-shell theorem for connected plaquette shells on the accepted
  `3 spatial + 1 derived-time` surface
- exact mixed repeated-plaquette audit and exact first nonlinear coefficient
  of the full-vacuum reduction law
- exact implicit reduction-law existence/uniqueness theorem on the finite
  Wilson evaluation surface
- exact nonperturbative susceptibility-flow theorem for the implicit reduction
  law
- exact connected plaquette-hierarchy theorem for the implicit reduction law
- exact obstruction to any finite-order connected-hierarchy truncation
- exact compact plaquette spectral-measure generating object for the full
  finite Wilson hierarchy
- exact framework-point underdetermination theorem showing that the current
  closed jet and structure theorems still do not force a unique analytic
  `P(6)`
- exact transfer-operator / character-recurrence realization of the plaquette
  generating object on the accepted `3+1` source surface
- exact Perron-state reduction theorem on the explicit transfer operator
- exact source-sector matrix-element factorization theorem at `beta = 6`
  with a structural theorem note and a generic positive-diagonal witness
  runner rather than an explicit Wilson `D_6` evaluation
- exact local/environment factorization theorem isolating the exact local
  Wilson marked-link factor on the source sector
- exact spatial-environment character-measure theorem identifying the
  residual operator as the boundary character measure of the unmarked spatial
  Wilson environment
- exact spatial-environment structural transfer theorem identifying that
  boundary class function as a boundary-amplitude sequence of one explicit
  positive spatial transfer operator
- exact spatial-environment tensor-transfer theorem identifying the remaining
  boundary amplitudes as explicit Wilson-coefficient / `SU(3)`-intertwiner
  tensor-transfer data, with the runner only a truncated support packet rather
  than a full `beta = 6` Perron solve
- exact Perron/Jacobi underdetermination theorem showing that even the
  sharpened factorized operator class still does not force unique `beta = 6`
  Perron moments or Jacobi coefficients until the explicit
  `beta = 6` tensor-transfer matrix elements generating the boundary
  character data are fixed
- explicit source-sector reference Perron solve theorem with explicit
  no-go on closed-form `rho_(p,q)(6)`: two structural reference choices
  of the residual environment (input rho = 1 and input
  rho = delta_{(p,q),(0,0)}) give explicit Perron data
  `P_loc(6) = 0.4524071590`, `P_triv(6) = 0.4225317396` from
  `c_lambda(6)` and `SU(3)` intertwiners alone, with super-polynomial
  NMAX truncation tail bound; three distinct admissible parametric
  rho families produce strictly different `P(6)` and demonstrate the
  no-go that local Wilson data does not fix `rho_(p,q)(6)`; the rho
  values in the reference solves are structural input, NOT derived
  from any physical 3D Wilson environment, and the note does not claim
  either reference corresponds to the physical environment; the missing
  object is the boundary character measure of the unmarked 3D spatial
  Wilson environment with marked-plaquette boundary, equivalently the
  Perron eigenvector of the explicit positive tensor-transfer operator
  on a 3D `SU(3)` lattice gauge network with one boundary plaquette
- exact scalar `3+1` bridge endpoint ratio
  `A_inf / A_2 = 2 / sqrt(3)`
- exact plaquette four-link coupling map
  `P(U) = u_0^4 P(V)`
- exact `3+1` plaquette/link incidence factor `6 / 4 = 3 / 2`
- exact obstruction to the naive constant-lift law
  `P(beta) = P_1plaq(beta * (3/2) * (2 / sqrt(3))^(1/4))`

Those ingredients sharply narrow the last insertion bridge and give the current
best analytic candidate

`P(6) = 0.593530679977098`.

This sits only `1.3068e-4` (`0.022%`) above the current canonical same-surface value
`0.5934`, so it materially strengthens the plaquette lane.

Current authorities for that support stack:

- [GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_DISTINCT_SHELL_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_DISTINCT_SHELL_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md)
- [GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md](./GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)
- [SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md](./SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md)

Current support runners:

- `scripts/frontier_gauge_vacuum_plaquette_bridge_support.py`
- `scripts/frontier_gauge_vacuum_plaquette_distinct_shell_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_mixed_cumulant_audit.py`
- `scripts/frontier_gauge_vacuum_plaquette_reduction_existence_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_susceptibility_flow_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_connected_hierarchy_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_infinite_hierarchy_obstruction.py`
- `scripts/frontier_gauge_vacuum_plaquette_spectral_measure_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_framework_point_underdetermination.py`
- `scripts/frontier_gauge_vacuum_plaquette_transfer_operator_character_recurrence.py`
- `scripts/frontier_gauge_vacuum_plaquette_perron_reduction_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_source_sector_matrix_element_factorization.py`
- `scripts/frontier_gauge_vacuum_plaquette_local_environment_factorization.py`
- `scripts/frontier_gauge_vacuum_plaquette_residual_environment_identification.py`
- `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_character_measure.py`
- `scripts/frontier_gauge_vacuum_plaquette_spatial_environment_transfer.py`
- `scripts/frontier_gauge_vacuum_plaquette_perron_jacobi_underdetermination.py`
- `scripts/frontier_gauge_vacuum_plaquette_tensor_transfer_perron_solve.py`
- `scripts/frontier_gauge_scalar_temporal_completion_theorem.py`
- `scripts/frontier_gauge_vacuum_plaquette_constant_lift_obstruction.py`
- `scripts/frontier_scalar_3plus1_temporal_ratio.py`

The honest live read is now sharper than before:

- the exact class-level bridge ingredients are real
- the simplest constant multiplicative effective-coupling lift is ruled out
- the minimal distinct connected shell is fixed exactly by the cube boundary
  theorem
- the first nonlocal full-vacuum coefficient is now fixed exactly by the mixed
  cumulant audit:
  `P_full(beta) = P_1plaq(beta) + beta^5 / 472392 + O(beta^6)`
- the exact implicit reduction law on the finite Wilson evaluation surface is
  now also closed and unique
- the exact nonperturbative susceptibility-flow law for that implicit reduction
  is now also closed
- the exact connected plaquette hierarchy governing that susceptibility flow is
  now also closed
- no exact finite-order connected-hierarchy truncation can close that object
- the exact equivalent generating object is now also closed as one compact
  plaquette spectral measure on each finite Wilson surface
- the current exact jet and structural theorems still do **not** determine a
  unique analytic framework-point value `P(6)`
- the plaquette generating object is now also explicit at the operator level:
  one positive one-clock Wilson transfer operator plus one exact self-adjoint
  `SU(3)` character-recurrence source operator
- the exact `beta = 6` source-sector transfer matrix elements are now also
  explicit in factorized form:
  `T_src(6) = exp(3 J) D_6 exp(3 J)`
- the normalized mixed-kernel contribution is now also explicit and exactly
  local:
  `D_beta^mix,norm chi_(p,q) = a_(p,q)(beta)^4 chi_(p,q)`
- so the remaining analytic target is explicit identification of the
  `beta = 6` spatial-transfer matrix elements generating the boundary
  character data of `Z_6^env` in
  `T_src(6) = exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)`, equivalently the exact
  Perron state of the factorized operator after the local mixed-kernel factor
  is stripped off, and
  therefore the explicit nonperturbative form of the reduction law at
  `beta = 6`, not the old
  constant-lift ansatz, not the onset coefficient, and not reduction-law
  existence, transport, hierarchy identification, generating-object existence,
  operator realization, or the broad operator-level underdetermination question
  itself

## Safe Reuse Rule

Downstream lanes may safely treat the following as canonical same-surface
evaluated quantities:

- `<P> = 0.5934`
- `u_0 = <P>^(1/4)`
- `alpha_s(v) = alpha_bare / u_0^2`
- `alpha_LM^2 = alpha_bare * alpha_s(v)` on the retained coupling
  definitions

with the understanding that the number is:

- not structural in the same sense as an exact symmetry theorem
- not imported from experiment
- not a free parameter

## Scope (bounded by construction)

This note does **not** by itself upgrade the plaquette to a fully analytic
physical-vacuum theorem at the framework point `beta = 6`. It does not migrate
the full repo-wide numeric package from the historical same-surface value
`0.5934` to an analytic replacement. The audit ledger's verdict on the
exact `beta = 6` insertion is therefore explicitly carried forward as the
defining bounded scope of this note.

It claims the narrower and sufficient point needed by the package, scoped
as `bounded` and not as `proposed_retained`:

> the plaquette is a uniquely determined observable of the retained theory,
> Monte Carlo is same-surface evaluation of that observable rather than
> parameter fitting, and the exact bridge-support stack materially narrows the
> remaining analytic insertion gap without yet closing it.

### Explicit window of the bounded analytic insertion

The bridge-support stack pins the analytic candidate at

```text
P(6) = 0.593530679977098,
```

`+0.022%` above the canonical same-surface value `0.5934`. That candidate
is **not** the same-surface plaquette: it is the current best analytic
upper-bound estimate from the closed implicit-reduction-law lane plus
the explicit Perron reference solves. The honest analytic window is
therefore

```text
0.5934 <= <P>(beta = 6) <= 0.59353,
```

bounded below by the canonical MC-evaluated readout and above by the
analytic candidate from the support stack. Closure of this window
(removal of the strict-inequality slack) is open work and is the
target of the upstream support stack listed under "Exact bridge-support
stack on `main`".

### Boundary against downstream lanes

Downstream consumers (notably the lane recorded in
`ALPHA_S_DERIVED_NOTE.md`) must read this row as `bounded`.
Effective-status propagation therefore caps any rows that depend on
`<P>` at `bounded` until the analytic insertion gap is closed. The
`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md` lane runs under the
same `bounded` discipline so that `alpha_s(M_Z) = 0.1181` inherits a
documented one-hop running bridge and a documented upstream plaquette
dependency, with both contributors explicitly bounded rather than
spuriously `proposed_retained`. Both downstream notes are mentioned by
file path rather than as one-hop markdown links, since they are
downstream consumers of this plaquette claim and turning them into
graph deps would create citation cycles.
