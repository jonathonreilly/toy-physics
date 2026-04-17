# Framework Point `beta = 6` Lane Note

**Date:** 2026-04-17
**Status:** synthesis / authority note on the canonical `beta = 6` framework
point. No new theorems are claimed; this note consolidates existing retained
ingredients into one reviewer-facing surface and isolates the single remaining
analytic object.
**Atlas role:** canonical authority surface for the `beta = 6` framework-point
claim and for the `beta = 6` plaquette theorem stack

## Purpose

The number `beta = 6` appears across the retained quantitative package in so
many places that it has become the de facto framework point, but it is not yet
surfaced as such. This note does three things:

1. states the `beta = 6` derivation theorem explicitly as a synthesis of
   existing retained ingredients;
2. consolidates the ~19 existing `beta = 6` plaquette theorem notes into one
   factorization chain and isolates the last-mile analytic object;
3. reframes the quantitative spine of the package as a sequence of
   `beta = 6` readouts.

Nothing in this note is newly proved. The content is already carried by
retained notes cited below; the contribution is synthesis.

## 1. The `beta = 6` derivation

### 1.1 Safe statement

On the axiom-determined Wilson-plus-staggered gauge surface:

> The Wilson gauge coupling
> `beta = 2 N_c / g_bare^2`
> is fixed to `beta = 6` as the unique framework-point evaluation, because
> `N_c = 3` is forced by the graph-first structural `SU(3)` closure and
> `g_bare = 1` is the canonical coordinate on the already-derived operator
> algebra. It is not a tuning parameter, not a fitted number, and not a knob
> to match a physical scale.

### 1.2 Load-bearing ingredients (already retained)

- `N_c = 3` is forced:
  - [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](./GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  - the Cl(3) bivector commutant on the canonical cube-shift graph closes
    exactly to `su(3) + u(1)` after the weak-axis selector
- `g_bare = 1` is forced as a coordinate choice on the derived algebra:
  - [G_BARE_RIGIDITY_THEOREM_NOTE.md](./G_BARE_RIGIDITY_THEOREM_NOTE.md)
  - once `su(3)` appears as a compact semisimple commutant in `End(V)` with
    the framework Hilbert inner product, there is no independent scalar
    gauge-normalization freedom left
  - [G_BARE_DERIVATION_NOTE.md](./G_BARE_DERIVATION_NOTE.md) carries the older
    bounded normalization argument consistent with the same conclusion
- The Wilson action is the retained gauge-sector action:
  - [STRONG_CP_THETA_ZERO_NOTE.md](./STRONG_CP_THETA_ZERO_NOTE.md) uses the
    CP-even Wilson plaquette action as the retained surface
  - [CONFINEMENT_STRING_TENSION_NOTE.md](./CONFINEMENT_STRING_TENSION_NOTE.md)
    evaluates confinement at `g_bare^2 = 1`, `beta = 6.0`
- The fixed-surface rigidity is exact:
  - [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
    states that the accepted framework is pinned to one canonical
    `g_bare = 1`, `beta = 6`, same-surface plaquette/hierarchy chain

### 1.3 Framework-point claim

Combining the three retained facts:

- `N_c = 3` forced
- `g_bare = 1` forced
- Wilson gauge action retained

gives a single framework-point value:

> `beta = 2 * 3 / 1 = 6`.

This is the unique evaluation point at which the retained package computes
its quantitative stack. The lattice spacing `a` falls out as a *consequence*
of the framework-point evaluation, not as a tuning parameter. This is the
inversion of standard lattice QCD practice, where `beta` is a knob tuned to
set `a` against a physical observable.

## 2. Why `beta = 6` appears everywhere

Every dimensionful prediction carried by the retained package passes through
`beta = 6`. The catalog below is a reading aid; each entry is already in an
authority note.

| Row | Uses `beta = 6` via | Authority |
|---|---|---|
| plaquette `<P>` | direct same-surface evaluation | [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](./PLAQUETTE_SELF_CONSISTENCY_NOTE.md) |
| tadpole `u_0` | `u_0 = <P>^(1/4)` at `beta = 6` | [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](./PLAQUETTE_SELF_CONSISTENCY_NOTE.md) |
| `alpha_LM` | `alpha_bare / u_0^2` at `beta = 6` | [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md) |
| `alpha_s(v)` | coupling map at `beta = 6` | [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md) |
| EW hierarchy `v` | `v = M_Pl (7/8)^(1/4) alpha_LM^16`; `alpha_LM` at `beta = 6` | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) |
| `alpha_s(M_Z)`, `sin^2 theta_W`, `g_1(v)`, `g_2(v)` | run from `alpha_s(v)` at `beta = 6` | [YT_EW_COLOR_PROJECTION_THEOREM.md](./YT_EW_COLOR_PROJECTION_THEOREM.md), [RCONN_DERIVED_NOTE.md](./RCONN_DERIVED_NOTE.md) |
| CKM `|V_us|`, `|V_cb|`, `|V_ub|`, `delta`, `J` | algebraic in `alpha_s(v)` from `beta = 6` | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| down-type mass ratios | CKM dual in `alpha_s(v)` from `beta = 6` | [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](./DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md) |
| `y_t(v)`, `m_t`, `m_H` | downstream of the same `beta = 6` chain | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md), [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](./HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md) |
| confinement `sqrt(sigma)` | Wilson `beta = 6.0` + retained `alpha_s` | [CONFINEMENT_STRING_TENSION_NOTE.md](./CONFINEMENT_STRING_TENSION_NOTE.md) |
| strong CP `theta_eff = 0` | retained Wilson-plus-staggered action at `beta = 6` | [STRONG_CP_THETA_ZERO_NOTE.md](./STRONG_CP_THETA_ZERO_NOTE.md) |

Every quantitative row in the retained package is therefore a same-surface
evaluation on one framework point.

## 3. The unified `6` across the package

The number `6` itself also appears in several distinct algebraic positions. On
the retained surface these are the same `6`, not separate coincidences:

| Appearance | Expression | Algebraic source |
|---|---|---|
| Wilson coupling | `beta = 2 N_c / g_bare^2 = 6` | `N_c = 3`, `g_bare = 1` |
| CKM projector | `1/6` on the atlas tensor-slot surface | `SU(3)` tensor structure |
| `|V_cb|` | `alpha_s(v) / sqrt(6)` | same atlas projector |
| `|V_ub|` | `alpha_s(v)^(3/2) / (6 sqrt(2))` | same atlas projector |
| generation permutation group | `|S_3| = 3! = 6` | three retained `hw=1` sectors |
| `SU(3)` Casimir combination | `C_F - T_F = 4/3 - 1/2 = 5/6` | `SU(3)` group constants |

Each `6` traces back to `N_c = 3` plus the retained `hw=1` generation triplet
and its permutation structure. The coincidence of the number `6` in the gauge
coupling and in the CKM / flavor algebra is the same algebraic object read in
different positions.

## 4. The hierarchy cascade from `beta = 6`

Read the retained chain in the direction of energy flow:

1. `beta = 6` is the **UV framework point at the Planck scale**. `g_bare = 1`
   is the canonical coordinate on the derived operator algebra, which is
   consistent with an O(1) gauge coupling at a scale where the graviton sector
   is also O(1).
2. The plaquette same-surface evaluation at `beta = 6` gives
   `<P> ~= 0.5934`, `u_0 = <P>^(1/4)`, and
   `alpha_LM = alpha_bare / u_0^2`.
3. The retained hierarchy theorem gives
   `v = M_Pl * (7/8)^(1/4) * alpha_LM^16 = 246.282818290129 GeV`.
   With `alpha_LM ~= 0.09`, the factor `alpha_LM^16 ~= 2.5 * 10^(-17)`
   reproduces `v / M_Pl`.
4. The coupling map then gives `alpha_s(v) ~= 0.1033`, and the retained
   running bridge gives `alpha_s(M_Z) = 0.1181`.
5. All downstream rows (EW normalization, CKM, down-type mass ratios,
   `y_t`, `m_t`, `m_H`, `sqrt(sigma)`) are algebraic in `alpha_s(v)`
   plus `SU(3)` group constants.

The retained reading is therefore:

> The framework is O(1)-coupled at the UV framework point `beta = 6`. The
> logarithmic amplification `alpha_LM^16` on the retained minimal hierarchy
> block fixes the EW/Planck hierarchy. Every downstream dimensionful row is
> an algebraic readout of the same `beta = 6` evaluation.

This is not a new claim. It is the retained hierarchy chain read as a
framework-point statement.

## 5. Synthesis of the existing `beta = 6` plaquette theorem stack

The repo currently carries ~19 exact theorems on the `beta = 6` plaquette /
transfer-operator surface. Read in order they form one factorization chain:

1. [GAUGE_VACUUM_PLAQUETTE_DISTINCT_SHELL_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_DISTINCT_SHELL_THEOREM_NOTE.md)
   — minimal distinct connected shell fixed exactly by the cube boundary
2. [GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md)
   — exact first nonlinear coefficient:
   `P_full(beta) = P_1plaq(beta) + beta^5 / 472392 + O(beta^6)`
3. [GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)
   — naive constant multiplicative effective-coupling lift is ruled out
4. [GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md)
   — exact implicit reduction law on the finite Wilson evaluation surface
5. [GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md)
   — exact nonperturbative susceptibility-flow law
6. [GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md)
   — exact connected plaquette hierarchy
7. [GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md)
   — no exact finite-order truncation closes the object
8. [GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md)
   — exact equivalent compact plaquette spectral measure
9. [GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md)
   — exact jet/structure theorems do not yet force unique analytic `P(6)`
10. [GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md)
    — exact transfer-operator / character-recurrence realization of the
    generating object
11. [GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md)
    — exact unique strictly positive Perron state of the transfer operator
12. [GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md)
    — explicit factorization at `beta = 6`:
    `T_src(6) = exp(3 J) D_6 exp(3 J)`
13. [GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md)
    — exact isolation of the local Wilson marked-link factor:
    `D_6 = D_6^loc * E_6` with
    `D_6^loc chi_(p,q) = a_(p,q)(6)^4 chi_(p,q)`
14. [GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md)
    — factorized operator class still does not force unique `beta = 6`
    Perron moments or Jacobi coefficients without `E_6`
15. [GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md)
    — identification surface for `E_6`
16. [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md)
    — spatial environment transfer structure
17. [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md)
    — tensor-transfer refinement
18. [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md)
    — character-measure form of the environment sector
19. [GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md)
    — bridge-support synthesis across the stack

The current best analytic candidate from this stack is
`P(6) = 0.593530679977098`, which is `1.31 * 10^(-4)` (`0.022%`) above the
canonical same-surface value `<P> = 0.5934`.

## 6. The single remaining analytic object: `E_6`

After this stack, the remaining object is a single named structure:

> **`E_6`**: the residual environment-response sequence in the factorization
> `D_6 = D_6^loc * E_6`, equivalently the exact Perron state of the
> factorized `beta = 6` source-sector transfer operator after the local
> Wilson marked-link factor has been stripped off.

What is ruled out already:

- the old constant-lift ansatz;
- the onset coefficient alone;
- reduction-law existence, transport, or hierarchy identification;
- generating-object existence or operator realization;
- broad operator-level underdetermination.

What remains:

- explicit identification of `E_6`.

Closing `E_6` is sufficient to promote the plaquette lane from "canonical
same-surface evaluation" to "framework-point analytic closure," and it is
necessary — the Perron/Jacobi underdetermination theorem (note 14 above)
rules out closure without it.

## 7. Reviewer FAQ

> **Why `beta = 6`? Why not `beta = 5.7` or `beta = 6.2`?**
>
> `beta = 6` is not selected, it is derived. `N_c = 3` is forced by the
> graph-first `SU(3)` commutant closure on the canonical cube-shift graph
> with the weak-axis selector. `g_bare = 1` is forced as the canonical
> coordinate on the derived `su(3)` operator algebra inside `End(V)`: once
> the compact semisimple commutant is fixed together with the framework
> Hilbert inner product, no independent scalar gauge-normalization freedom
> remains. Therefore `beta = 2 N_c / g_bare^2 = 6` uniquely. The lattice
> spacing `a` is a consequence of this framework-point evaluation, not a
> knob tuned to match physical observables. This is the inversion of
> standard lattice QCD practice.

## 8. Framing the remaining TOE gap around `beta = 6`

Reading the current open gate list through this lane:

- G1 (`Z_3` doublet-block selector law), G2 (plaquette `E_6`),
  G5 (charged-lepton universality selector), and G8 (PMNS value law) are
  all underdetermination problems on transfer-operator projections at the
  same framework point.
- G2 is the direct `E_6` problem on the plaquette source sector.
- G1, G5, G8 are selection problems on *other* sectors that share the
  same underlying transfer operator structure.

The unifying reframing is:

> Every remaining selection / underdetermination gate in the package is a
> statement about Perron states of projections of the one `beta = 6`
> framework-point transfer-operator family. The open TOE problem reduces
> to: identify the Perron data on each retained projection.

Whether this unification is *formal* — i.e., whether the sector Perron
states are projections of a common parent Perron state under canonical
projectors — is itself an open structural question and is tracked under
the Perron-Frobenius cross-sector consistency program. See
[.claude/science/derivations/pf-selection-from-axiom-2026-04-17.md](../.claude/science/derivations/pf-selection-from-axiom-2026-04-17.md)
and related working files for the current state of that investigation.

This lane note does not assert that unification is formally proven. It
records that the open gates share a common algebraic location at the same
framework point.

## 9. What this lane does and does not claim

This lane claims:

- `beta = 6` is the unique framework-point evaluation of the retained
  axiom-determined Wilson-plus-staggered surface;
- the `beta = 6` claim is a synthesis of existing retained theorems
  (`N_c = 3` forced, `g_bare = 1` forced, Wilson action retained,
  fixed-surface rigidity);
- every dimensionful row in the retained quantitative package is a
  same-surface evaluation at `beta = 6`;
- the ~19 existing plaquette theorem notes form one factorization chain
  whose single remaining analytic object is `E_6`;
- the several distinct occurrences of the number `6` across the package
  trace back to the same `N_c = 3` + `hw=1` generation triplet algebra.

This lane does **not** claim:

- closure of `E_6` or promotion of the plaquette lane beyond
  canonical same-surface evaluation;
- formal cross-sector Perron consistency (that is a separate open
  investigation);
- promotion of `beta = 6` to manuscript-headline status beyond the
  existing retained claim surface;
- any new theorem beyond synthesis of already-retained ingredients.

## 10. Authorities and primary runners

Upstream framework-point authorities:

- [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](./GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
- [G_BARE_RIGIDITY_THEOREM_NOTE.md](./G_BARE_RIGIDITY_THEOREM_NOTE.md)
- [G_BARE_DERIVATION_NOTE.md](./G_BARE_DERIVATION_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [STRONG_CP_THETA_ZERO_NOTE.md](./STRONG_CP_THETA_ZERO_NOTE.md)
- [CONFINEMENT_STRING_TENSION_NOTE.md](./CONFINEMENT_STRING_TENSION_NOTE.md)

Plaquette stack authorities (see Section 5 for the ordered list):

- [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](./PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
- 19 `GAUGE_VACUUM_PLAQUETTE_*_NOTE.md` entries

Downstream quantitative authorities:

- [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [RCONN_DERIVED_NOTE.md](./RCONN_DERIVED_NOTE.md)
- [YT_EW_COLOR_PROJECTION_THEOREM.md](./YT_EW_COLOR_PROJECTION_THEOREM.md)
- [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](./DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](./HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md)

Primary runner for the plaquette same-surface evaluation:

- [../scripts/frontier_plaquette_self_consistency.py](../scripts/frontier_plaquette_self_consistency.py)

This lane is a synthesis note and does not introduce a new runner. The
runners for each cited sub-theorem are the canonical validation surfaces.

## 11. Paper-safe wording

> On the retained axiom-determined Wilson-plus-staggered surface, `N_c = 3`
> is forced by the graph-first `SU(3)` commutant closure and `g_bare = 1`
> is forced as the canonical coordinate on the derived operator algebra, so
> the Wilson gauge coupling is fixed to the unique framework-point value
> `beta = 2 N_c / g_bare^2 = 6`. Every dimensionful row in the retained
> quantitative package (`<P>`, `u_0`, `alpha_LM`, `alpha_s(v)`, `v`,
> `alpha_s(M_Z)`, the EW normalization package, the CKM atlas/axiom
> closure, the down-type mass-ratio dual, `y_t`, `m_t`, `m_H`, and the
> bounded `sqrt(sigma)` confinement readout) is a same-surface evaluation
> at this framework point. The residual analytic object on the plaquette
> lane is the `beta = 6` Perron state of the factorized source-sector
> transfer operator after the local Wilson marked-link factor is stripped,
> denoted `E_6`; promoting the plaquette lane to framework-point analytic
> closure is equivalent to identifying `E_6`.
