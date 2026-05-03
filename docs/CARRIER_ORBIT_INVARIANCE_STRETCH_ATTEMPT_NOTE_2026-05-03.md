# Carrier Orbit Invariance — Stretch Attempt with Partial Closing-Derivation

**Date:** 2026-05-03  
**Type:** stretch_attempt (output type c) with PARTIAL structural-insight  
**Claim scope:** documents a worked stretch attempt at closing the
cycle 17 named residual — the swap-reduction theorem's structural-
exhaustion premise that NO exact `E/T`-distinguishing operator exists
on the `K_R(q)` carrier. Cycle 22 of `retained-promotion-2026-05-02`
campaign continuation. Establishes a partial Z_2-equivariant operator
classification on the carrier, reducing the open-ended structural
premise to a single named meta-mathematical residual: closure of the
retained primitive registry. Audit-lane ratification required for any
retained-grade interpretation.

**Status:** stretch attempt with partial structural insight; the
residual gap (registry closure) is named precisely.

**Runner:** [`scripts/frontier_carrier_orbit_invariance.py`](../scripts/frontier_carrier_orbit_invariance.py)

**Authority role:** sharpens the residual named by cycle 17 (PR #445)
on the upstream swap-reduction theorem; converts an open-ended
structural exhaustion question into a finite registry-enumeration check
plus one named meta-premise.

**Cycle:** 22 of `retained-promotion-2026-05-02` campaign.

## A_min (minimal allowed premise set)

- (R1, retained) **Cl(3) on Z^3 axiom** — the single framework axiom.
- (R2, retained-bounded) `S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE`:
  carrier definition `K_R(q) = [[u_E, u_T], [delta_A1 u_E, delta_A1 u_T]]`.
- (R3, retained-bounded) `S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE`:
  `Theta_R^(0)(q) = (gamma_E, gamma_T)` is bounded, not exact.
- (R4, retained-bounded) `S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE`:
  `Xi_R^(0)` is bounded, not exact.
- (M1) **Maschke's theorem** for finite groups over R: every finite-
  dimensional R-representation of a finite group decomposes into a
  direct sum of isotypic components. (Admitted-context standard math.)
- (M2) **Schur's lemma** (admitted-context standard math).

## Forbidden imports

- **PDG values, neutrino masses, PMNS angles, m_top, sin²(theta_W),
  eta_obs**: NOT consumed.
- **Literature numerical comparators**: NOT consumed.
- **Fitted selectors**: NOT consumed.
- **Same-surface family arguments**: NOT used.
- **Cycle 17 retention routes A, B, C**: ADMITTED as prior-cycle
  inputs only, not load-bearing on the structural-exhaustion argument.
- **v_even values themselves**: NOT consumed (cycle 22 attacks the
  upstream structural premise, not the values).
- **Cohomological / sheaf-theoretic machinery**: rejected as overkill
  during route portfolio (Routes C, D in `ROUTE_PORTFOLIO.md`).

## Background

From the swap-reduction theorem
(`DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15`,
audited_conditional, td=47), the exact even-response law on the current
weak source carrier reduces to the swap quotient — provided that **no
exact E/T-distinguishing operator** acts on the carrier `K_R(q)`. This
"structural-exhaustion premise" is the load-bearing input.

Cycle 17 (PR #445) closed v_even three independent ways but identified
the precise residual:

> "the swap-reduction theorem's structural-exhaustion premise — 'no
> exact E/T-distinguishing operator on the K_R(q) carrier' — is
> established for specific operators (Theta_R^(0), Xi_R^(0) are
> bounded) but NOT exhaustively."

Cycle 22 attacks this exhaustion claim via Route B (group-theoretic
classification).

## Carrier representation under the Z_2 swap action

The carrier

```text
K_R(q) = [[u_E, u_T], [delta_A1 u_E, delta_A1 u_T]]
```

viewed as a 4-vector

```text
v = (u_E, u_T, delta_A1 u_E, delta_A1 u_T) ∈ V := R^4
```

carries an explicit `Z_2` action by right-multiplication of the
underlying 2x2 matrix by `P_ET = [[0,1],[1,0]]`:

```text
tau(u_E, u_T, delta u_E, delta u_T) = (u_T, u_E, delta u_T, delta u_E)
```

The action `tau` is an involution (`tau^2 = id`) and is well-defined as
a linear automorphism of `V`.

## Isotypic decomposition

By Maschke's theorem, the carrier `V = R^4` decomposes under `tau` into
isotypic components:

```text
V = V^+ ⊕ V^-
```

where:
- `V^+ = ker(tau - id)` is the symmetric (`+1`-eigenspace), dim 2,
  spanned by `(1, 1, 0, 0)` and `(0, 0, 1, 1)`.
- `V^- = ker(tau + id)` is the antisymmetric (`-1`-eigenspace), dim 2,
  spanned by `(1, -1, 0, 0)` and `(0, 0, 1, -1)`.

Concretely, in the parametrization `(u_E, u_T, delta u_E, delta u_T)`:

```text
V^+ = span{(u_E + u_T) basis vectors}
V^- = span{(u_E - u_T) basis vectors}
```

## Operator decomposition

Linear operators `L: V -> W` (for any `W`) decompose under the
induced `Z_2` action `L ↦ L ∘ tau`:

```text
Hom(V, W) = Hom(V, W)^+ ⊕ Hom(V, W)^-
```

where `Hom(V, W)^+` consists of operators `L` with `L ∘ tau = L`
(swap-invariant) and `Hom(V, W)^-` of operators with `L ∘ tau = -L`
(swap-antisymmetric).

For the case `W = R` (linear functionals), the decomposition is:

```text
V* = (V*)^+ ⊕ (V*)^-
dim(V*)^+ = 2, dim(V*)^- = 2
```

where `(V*)^+` is the space of **swap-invariant** functionals and
`(V*)^-` is the space of **swap-antisymmetric** functionals.

## Definition: E/T-distinguishing operator

A linear operator `L: V -> W` (for `W` non-trivial) **distinguishes**
the E and T orbits iff there exists `v ∈ V` with `L(v) ≠ L(tau v)`,
equivalently `L ≠ L ∘ tau`.

By the isotypic decomposition, this is equivalent to: `L` has nonzero
component in `Hom(V, W)^-`.

## Theorem (Carrier Operator Classification — partial)

**Statement.** Let `L: V -> W` be a linear operator built from the
current retained framework primitives. Then `L` has zero component in
`Hom(V, W)^-`.

**Proof structure (partial).**

(1) The current retained primitive registry on the carrier surface
consists of:
- `Theta_R^(0) = (gamma_E, gamma_T)`: explicitly **bounded**, not exact
  (per `S3_TIME_TENSOR_PRIMITIVE_PROTOTYPE_NOTE`).
- `Xi_R^(0) = d Theta_R^(0) / d delta_A1`: explicitly **bounded**, not
  exact (per `S3_TIME_CONSTRUCTED_SUPPORT_TENSOR_PRIMITIVE_NOTE`).

(2) Bounded operators do NOT supply an exact single-axiom readout
(per the swap-reduction theorem note, "Why this does not contradict the
old Route-2 staging tools"). They are staging tools, not theorem-grade
coefficient laws.

(3) The active Hermitian basis on the H-side source surface — the
operators (a, b, c, d, T_delta, T_rho) of cycle 16 / cycle 17 — acts
on the 3x3 H-side, not on the carrier directly. Their projection onto
the carrier action factors through `K_R = [1, delta_A1]^T [u_E, u_T]`,
and is column-symmetric on the (u_E, u_T) columns by construction.

(4) The framework axiom `Cl(3)` on `Z^3` does not include any operator
that intertwines the `E_x` irrep block with the `T1x` irrep block of
the support algebra. The vectors `E_x` and `T1x` are basis vectors in
distinct irreps of the cubic group `O_h` acting on the seven-site star
support: `E_x` lies in the `E` (2D) irrep and `T1x` in the `T1` (3D)
irrep. The `O_h`-equivariant primitive operators on the support algebra
are necessarily block-diagonal with respect to the (`E`, `T1`) irrep
decomposition.

(5) An operator with nonzero component in `Hom(V, W)^-` corresponds to
a primitive that distinguishes `(u_E, u_T)` columns by their irrep
label (E vs T1). Since the framework's retained primitive operators
are O_h-equivariant and block-diagonal with respect to the (E, T1)
decomposition, their action on the carrier columns is given by
multiplication by independent scalars `(c_E, c_T)`. The component in
`(V*)^-` corresponds to `c_E ≠ c_T`.

(6) **Registry enumeration.** Direct enumeration of currently retained
primitive operators acting on `(u_E, u_T)` confirms each acts
column-symmetrically (`c_E = c_T = c`) on the carrier columns: the
inner-product structure of `<E_x, q>` and `<T1x, q>` against any
retained primitive `O_h`-equivariant operator yields equal weight on
both columns (by `O_h` block-diagonality).

(7) Therefore: every retained-primitive operator `L` on the current
audited surface has `L ∘ tau = L`, i.e., zero component in
`Hom(V, W)^-`.

**Residual gap (named precisely).** Step (6) — registry enumeration —
is currently a finite check that PASSES on the audited surface. The
**closure** premise — "no future retained primitive can have nonzero
`(V*)^-` component" — is a meta-mathematical statement about the
framework registry, not a statement provable on the current axiomatic
surface. This is the residual obstruction that cycle 22 names
precisely.

## Counterfactual hypotheticals

To test the classification, four hypothetical antisymmetric operator
candidates were considered:

| candidate | swap-antisymmetric? | currently retained? | passes test? |
|---|---|---|---|
| `Z_diff_col = e_E^* - e_T^*` (column-difference) | YES | NO | YES (ruled out by registry) |
| `Z_diff_row = e_1^* - e_2^*` (row-difference) | NO (acts on rows) | NO | N/A (wrong axis) |
| `Theta_R^(0)` (gamma_E - gamma_T component) | bounded only | bounded, not exact | YES (already-bounded) |
| `Xi_R^(0)` (d(gamma_E - gamma_T)/d delta_A1) | bounded only | bounded, not exact | YES (already-bounded) |

All antisymmetric candidates are either NOT in the retained-exact
registry or are explicitly bounded (not exact). This confirms the
classification on the current audited surface.

## Counterfactual: what would falsify the classification?

A new retained primitive `Z_new` with the property
`Tr(Z_new · K_R) ≠ Tr(Z_new · K_R · P_ET)` for some carrier instance
would directly falsify the structural-exhaustion premise. The runner
verifies that the active Hermitian basis (a, b, c, d, T_delta, T_rho)
contains zero such `Z_new`: every basis element induces a column-
symmetric trace on `K_R`.

## What this closes

1. **Z_2-equivariant operator classification** on the carrier
   representation: the operator space decomposes into `(V*)^+ ⊕ (V*)^-`,
   with explicit dimension count `2 + 2`. The structural-exhaustion
   question reduces to: "does the retained primitive registry contain
   any `(V*)^-` element?"

2. **Registry enumeration on current audited surface**: passes — no
   retained primitive on the carrier has nonzero antisymmetric
   component. Counterfactual antisymmetric candidates are explicitly
   absent from the registry or already bounded.

3. **Sharpens cycle 17 named residual**: from a vague open-ended
   structural exhaustion claim to a single named meta-mathematical
   premise (registry closure).

4. **Routes C, D rejected as overkill**: the cohomological and sheaf-
   theoretic reformulations reduce to the same Z_2-isotypic
   decomposition without adding content.

## What this does not close

- **Absolute retention of the swap-reduction theorem to audited_clean**:
  blocked on the registry closure meta-premise. Future cycles can
  target this single named obstruction by either (a) auditing the
  retained primitive registry exhaustively, or (b) proving a closure
  property (e.g., that all framework-derived operators on the carrier
  factor through the swap quotient).

- **Absolute retention of v_even theorem**: downstream of swap-
  reduction; same blocker.

- **Composite-Higgs / leptogenesis closures**: out of scope.

## Audit-graph effect

If independent audit ratifies cycle 22:

1. Swap-reduction theorem residual sharpened from "no exact
   E/T-distinguishing operator" to "registry closure of antisymmetric
   primitives on `K_R(q)`."
2. Cycle 17 named residual is RETIRED as cycle 22 names the precise
   meta-premise.
3. New named residual: **registry closure** — a meta-mathematical
   audit task, not a single-cycle physics derivation.
4. Cycle 16 sub-B/sub-C and cycle 17 retention routes A/B/C remain
   single-lemma-away from retained, with the lemma now precisely
   identified.

## Honesty disclosures

- This is a **stretch attempt** (output type c) with partial
  structural-insight, not an absolute closing derivation.
- The Z_2-isotypic decomposition is rigorous (Maschke / Schur); the
  registry enumeration on the current audited surface is a finite
  check that PASSES.
- The closure ("no future retained primitive can break this") is a
  meta-statement about the framework registry, not a statement
  provable on the current axiomatic surface.
- Audit-lane ratification required for any retained-grade
  interpretation.
- Routes C and D were rejected during route portfolio (overkill);
  Route E (low-degree polynomial operator enumeration) was used as
  runner cross-check.

## Reproduction

```bash
python3 scripts/frontier_carrier_orbit_invariance.py
```

Expected output: `SUMMARY: PASS=N FAIL=0` with `N >= 15`. The runner
verifies:
- Z_2-isotypic decomposition of `V = R^4`.
- Operator decomposition `End(V) = End(V)^+ ⊕ End(V)^-`.
- Registry enumeration of currently retained primitives.
- Counterfactual antisymmetric candidate falsification.
- Carrier-level swap-symmetry check on the active Hermitian basis.
- Low-degree polynomial operator enumeration (Route E cross-check).
- Named obstructions on registry closure.
