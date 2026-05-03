# Assumptions and Imports — Cycle 22

## Retained framework primitives (LOAD-BEARING)

- (R1, retained) **Cl(3) on Z^3 axiom**: the single framework axiom.
- (R2, retained, td=126) `DM_NEUTRINO_WEAK_VECTOR_THEOREM`: the bridge
  family Y_i = P_R Gamma_i P_L is exactly an SU(2) weak vector with
  Tr(Y_i^dag Y_j) = 8 delta_ij. Column-ordering independent.
- (R3, retained-bounded) `S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE`:
  carrier definition K_R(q) = [[u_E, u_T], [delta_A1 u_E, delta_A1 u_T]].
- (R4, retained-bounded) `S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE`:
  Theta_R^(0)(q) = (gamma_E(q), gamma_T(q)) is bounded, not exact.
- (R5, retained-bounded) `S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE`:
  Xi_R^(0) = d Theta_R^(0) / d delta_A1 is bounded, not exact.
- (R6, retained, td=45) `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM`:
  positive-Hermitian witness on the source surface forces v_even =
  (sqrt(8/3), sqrt(8)/3). (Cycle 17 admitted-context.)

## Admitted-context standard math (NOT load-bearing on novelty claim)

- (M1) **Schur's lemma** (finite-dimensional intertwiner argument).
- (M2) **Representation theory of finite groups** — specifically the
  Z_2 isotypic decomposition of a representation V = V^+ ⊕ V^- where
  V^+ is the +1 eigenspace and V^- is the -1 eigenspace of the action.
- (M3) **Multilinear algebra** on tensor product spaces — symmetric and
  antisymmetric components of V ⊗ V under swap.
- (M4) **Polynomial algebra** in carrier coordinates — degree-bounded
  invariant theory under Z_2.
- (M5) **Burnside / Maschke** — finite group representations over R
  decompose into isotypic components.

## Prior-cycle admitted inputs (NOT load-bearing on novelty)

- (P1, prior-cycle) **Cycle 16 Frobenius dual results**: v_even =
  (sqrt(8/3), sqrt(8)/3) values; not used as load-bearing input here.
  Cycle 22 attacks the structural premise upstream of v_even.
- (P2, prior-cycle) **Cycle 17 retention routes A, B, C**: convergent
  v_even retention. Cycle 22 sharpens the residual NAMED in cycle 17.

## Forbidden imports

- **PDG** values for any physical observable: NOT consumed.
- **Literature numerical comparators**: NOT consumed.
- **Fitted selectors**: NOT consumed.
- **m_top, sin^2(theta_W), eta_obs, neutrino masses, PMNS angles**: NOT
  consumed.
- **Standard QFT machinery beyond finite-group rep theory**: NOT
  consumed.
- **Same-surface family arguments**: NOT used.

## Meta-mathematical premise (named, NOT proved)

- (Meta-1) **Retained primitive registry closure**: the set of
  retained framework primitives that act on K_R(q) is exhaustively
  characterized by the audited surface; specifically, the set
  {Theta_R^(0), Xi_R^(0)} (both bounded) is the complete set of
  retained candidate E/T-distinguishing operators on the current
  surface.

This is the residual gap that cycle 22 names precisely. It is a
meta-statement about the audited registry, not a statement provable on
the current axiomatic surface. Future cycles can target this single
named premise.

## Imports retired by cycle 22

- The vague phrasing "no exact E/T-distinguishing operator on the
  carrier" is replaced with the precise phrasing "no antisymmetric
  isotypic operator in the Z_2-equivariant operator space on K_R(q)."
- The check is reduced from an open-ended structural claim to a
  registry-enumeration check + a meta-mathematical closure premise.
