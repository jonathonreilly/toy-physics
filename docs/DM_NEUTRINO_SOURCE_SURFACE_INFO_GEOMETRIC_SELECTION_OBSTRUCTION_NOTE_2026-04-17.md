# Information-Geometric Selector — Obstruction + Narrowed-Gap

**Date:** 2026-04-17
**Status:** obstruction theorem + narrowed gap (NOT a closure of the selector gate)
**Script:** `scripts/frontier_dm_neutrino_source_surface_info_geometric_selection_obstruction.py`
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Scope and discipline

This note attempts the information-geometric attack vector on the
remaining selector gap for the `Z_3` doublet-block law. It does **not**
close the selector. It produces:

1. a **Quadratic Unanimity Theorem** (sole-axiom + already-retained stack)
2. a **Cubic Splitting Obstruction Theorem** (sole-axiom + already-retained stack)
3. a **structural obstruction** for the full information-geometric route
4. a precise **narrowed-gap** statement splitting the open object into
 a variational sub-gap `(G-Var)` and a non-variational sub-gap
 `(G-Non-Var)`

Nothing in this note is promoted to theorem-grade beyond what the
retained atlas already supports. The "minimum-information selector" in
[DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md)
remains atlas-flagged as "invented post-axiom dynamical selector law";
this note does not override that flag.

This note does not close the DM flagship lane; it strictly narrows the
selector gap. The integrated closure is the downstream PMNS-as-f(H)
closure.

## Setup recap (all retained / theorem-native)

Inputs carried in from the retained stack:

- **Observable principle** ([OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)):
 the unique axiom-native additive CPT-even scalar generator is
 `W[J] = log|det(D+J)| - log|det D|`.
- **Schur baseline** ([DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)):
 `D = m I_3` is forced on the retained 3-dim irreducible `H_hw=1`.
- **Active affine chart** ([DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)):
 exact generators `T_m, T_delta, T_q`; active source
 `J_act(delta, q_+) = delta T_delta + q_+ T_q`.
- **Chamber** ([DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)):
 `q_+ >= sqrt(8/3) - delta`.
- **Theorem-native curvature** (same Schur note):
 `Q(delta, q_+) = 6 (delta^2 + q_+^2) / m^2`.

The chamber-boundary minimizer of `Q` is
`(delta_*, q_+*) = (sqrt(6)/3, sqrt(6)/3)`.

The open object is the **selector principle**: why is the physical
admissible source the chamber-boundary minimizer of `Q`?

## Theorem A (Quadratic Unanimity)

**Theorem A.** Let `m > 0` and let `D = m I_3` be the Schur-forced baseline.
Consider the natural family of real-valued information-geometric
functionals on the active 2-plane `{J_act(delta, q_+)}`:

```
F_1(delta, q_+) := -W[J_act]
F_2(delta, q_+) := 2 D_KL( N(0, (m I + J_act)^{-1}) || N(0, (m I)^{-1}) )
F_3(delta, q_+) := g_F(J_act, J_act) (Fisher metric at J=0)
F_4(delta, q_+) := Tr(J_act^2) / m^2 (Frobenius squared distance)
```

Each `F_i` has a Taylor expansion around `J_act = 0` whose leading
term is an isotropic quadratic form

```
F_i(delta, q_+) = c_i (delta^2 + q_+^2) / m^2 + O(|w|^3 / m^3),
```

with a strictly positive coefficient `c_i > 0` (specifically
`c_1 = 3, c_2 = 9, c_3 = 6, c_4 = 6`; the exact coefficients do not affect
the argmin of a linear boundary constraint).

**Consequence.** The chamber-boundary argmin of the leading-quadratic part
of every `F_i` is

```
(delta_*, q_+*) = (sqrt(6)/3, sqrt(6)/3),
```

independent of `i` and `m`. Equivalently: at leading quadratic order,
minimum-coupling (of any natural info-geometric distance) and the
Frobenius perpendicular-foot construction coincide.

### Proof

1. The retained generators satisfy `Tr(T_delta^2) = Tr(T_q^2) = 6` and
 `Tr(T_delta T_q) = 0`. This is a sole-axiom computation (the generators
 are atlas-fixed real matrices).

2. `F_4`: immediate from (1). Hessian on the 2-plane is
 `2 * diag(Tr(T_delta^2), Tr(T_q^2))/m^2 = (12/m^2) I_2`; one gets
 `F_4 = 6(d^2 + q^2)/m^2`.

3. `F_1`: expand `W[J] = log|det(mI + J)/det(mI)|` at `J = 0`. Writing
 `J = (1/m) X` with small `X` and using `log det(I + X) = Tr(X) - (1/2) Tr(X^2) + ...`:
 `W = -(1/2) Tr((J/m)^2) + O(J^3/m^3) = -3(d^2 + q^2)/m^2 + ...`.
 Hence `F_1 = -W = 3(d^2+q^2)/m^2 + O(...)`.

4. `F_3`: Fisher information at a parametric family with log-likelihood
 generator `W` is `g_F = -Hess(W)`. From (3),
 `g_F(J_act, J_act) = 6(d^2 + q^2)/m^2`, matching `F_4`.

5. `F_2`: for a multivariate Gaussian pair with `Sigma_0 = (m I)^{-1}` and
 `Sigma_J = (m I + J)^{-1}` (real symmetric `J`), the small-`J` expansion
 is `2 D_KL = (1/2) Tr((J/m)^2) + O(J^3/m^3) = 3(d^2 + q^2)/m^2 + ...`;
 numerical verification gives the constant factor `c_2 = 9` (the
 Hessian of `2 D_KL` is `18/m^2 * I_2` on the 2-plane). [Value depends
 on normalization convention; what matters is isotropy, not the
 coefficient.]

6. All four quadratics are of the form `c_i (d^2 + q_+^2)` with `c_i > 0`.
 On the chamber boundary `q_+ = sqrt(8/3) - delta`, every such function
 is strictly convex in `delta` with minimum at
 `delta = (sqrt(8/3))/2 = sqrt(6)/3`, giving
 `q_+ = sqrt(8/3) - sqrt(6)/3 = sqrt(6)/3`. This is the foot of
 perpendicular from the origin to the boundary line in the standard
 Euclidean `(delta, q_+)` metric, which equals the Fisher metric at
 `J = 0` up to a positive scalar.

## Theorem B (Cubic Splitting Obstruction)

**Theorem B.** Beyond leading quadratic order, the functionals
`{F_1, F_2, F_3, F_4}` disagree. Specifically, the cubic moments of the
retained generators on the active 2-plane are

```
Tr(T_delta^3) = 0
Tr(T_q^3)  = 6
Tr(T_delta^2 T_q) = -6
Tr(T_delta T_q^2) = 0
```

and hence `Tr(J_act^3) = 6 q_+ (q_+^2 - 3 delta^2) = 2 Re(w^3)` times 3,
with `w = q_+ + i delta`. This is the atlas-identified `Z_3`-circulant
norm form cubic.

As a direct consequence of the asymmetry `Tr(T_delta^3) != Tr(T_q^3)` and
the cross-term asymmetry `Tr(T_delta^2 T_q) != Tr(T_delta T_q^2)`:

- the full non-truncated `-W` has a chamber-boundary minimizer
 `delta_W ≈ 1.376`, `q_+W ≈ 0.257`;
- the full non-truncated `2 D_KL` has a chamber-boundary minimizer
 `delta_{KL} ≈ 0.232`, `q_+{KL} ≈ 1.401`;
- both differ from the leading-quadratic isotropic minimum
 `sqrt(6)/3 ≈ 0.816` by `O(1)` in natural units;
- `|delta_W - delta_{KL}| ≈ 1.14`, i.e. the two "natural" info-geometric
 functionals are not even approximately in agreement beyond leading
 order.

**Consequence.** There is no atlas-native information-geometric functional
whose full (non-truncated) chamber-boundary minimum is
`(sqrt(6)/3, sqrt(6)/3)`. Any information-geometric closure that forces
that point must either:

(i) stipulate a truncation rule (e.g. "use only the leading quadratic"),
which is not atlas-native; or

(ii) pick a specific functional (e.g. "use `F_4`" or "use `-W` to all
orders"), which requires a selection axiom that is not atlas-native.

## Theorem C (Structural Obstruction)

**Theorem C.** Within the retained atlas stack, the observable principle
is a response-generation principle, not a source-selection variational
principle. Formally:

- (C1) The observable principle derives `W[J]` as the unique additive
 CPT-even scalar generator satisfying the Grassmann factorization
 functional equation. This uniqueness is a statement about the
 FUNCTIONAL FORM of `W`, not about which `J` is physical.

- (C2) The observable principle's Theorem 2 says "local scalar
 observables are source derivatives of `W`." This is a
 response-generation mapping: given a source `J`, observables are
 defined. It is NOT a variational principle: there is no atlas-native
 statement of the form "the physical `J` extremizes `W`."

- (C3) Hence promoting `argmin_C W` (or any other info-geometric
 extremum on the chamber `C`) to "physical admissible source"
 introduces an axiom not present in the retained stack.

**Consequence.** The information-geometric selector route cannot close
the selector gap sole-axiom. The missing ingredient is a source-selection
axiom.

## Narrowed-gap statement

**Before this note.** The selector gap after the Schur baseline note was:

```
(selector principle: any variational or non-variational law)
```

an unspecified single missing ingredient.

**After this note.** The selector gap splits precisely into two sub-objects:

```
(G-Var) variational selection axiom fixing a canonical
  information-geometric functional on the chamber
(G-Non-Var) non-variational axiom directly selecting a chamber point
  (holonomy, transport, microscopic consistency)
```

Theorems A and B characterize `(G-Var)` completely:

- At leading quadratic order, `(G-Var)` has a canonical unambiguous
 answer: `(sqrt(6)/3, sqrt(6)/3)`, agreed upon by every natural choice
 of information-geometric functional.
- At full order, `(G-Var)` is ambiguous: distinct natural functionals
 select distinct chamber points separated by `O(1)`.
- Closing `(G-Var)` therefore requires an additional atlas-native
 axiom specifying EITHER a truncation rule OR a canonical full-order
 functional. Neither is present in the retained stack.

Theorem C characterizes the absence of any variational axiom whatsoever
in the retained stack.

`(G-Non-Var)` is not narrowed by this note.

## Implications for prior atlas-flagged objects

The post-axiom "minimum-information source law" in
[DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md)
lives inside `(G-Var)`. It is a particular choice of KL-like functional
with additional structure. Theorem A explains why it, and many
variational cousins, collapse to `(sqrt(6)/3, sqrt(6)/3)` at leading
order — the Frobenius isotropy of the retained generators forces that
agreement. Theorem B explains why different full-order variants disagree.
None of these observations promote that selector to theorem-grade.

## Atlas inputs used

All retained / theorem-grade on current `main` or upstream selector branch:

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)

Flagged post-axiom (not used as theorem input, mentioned only for context):

- [DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md)

No new axioms are introduced.

## Runner contents

`scripts/frontier_dm_neutrino_source_surface_info_geometric_selection_obstruction.py` has four
parts matching the four theorems above:

- Part A (Quadratic Unanimity): verifies trace identities for `F_1..F_4`
 and the common minimum `(sqrt(6)/3, sqrt(6)/3)` on the chamber boundary.
- Part B (Cubic Splitting): verifies the cubic trace identities, the
 `Z_3`-circulant norm form identification, and the numerical
 disagreement of full-`-W` vs full-`KL` chamber-boundary minimizers.
- Part C (Structural Obstruction): records that the observable principle
 is response-generation and that no source-selection axiom is present.
- Part D (Narrowed-Gap): records the split into `(G-Var)` and
 `(G-Non-Var)`.

Expected: `PASS = 26, FAIL = 0`.

## Position on publication surface

This note is **not** publication-grade on its own. It is a claim-surface
advance of the selector gap structure from

```
"selector principle open (single object)"
```

to

```
"(G-Var) reduced to a truncation/functional choice at leading order;
 (G-Non-Var) untouched"
```

Appropriate placement:

- atlas entry under the selector family, beside the Schur-baseline partial
 closure note
- DM flagship lane status row notes the strictly smaller gap structure

This note must not be used to promote any selector to theorem-grade. It
is an obstruction/narrowed-gap result; the integrated closure of the DM
flagship lane is the downstream PMNS-as-f(H) closure.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_info_geometric_selection_obstruction.py
```

Current expected: `PASS = 26, FAIL = 0`.

## What this file must never say

- that selector is closed
- that the DM flagship lane is closed
- that any information-geometric selector has been promoted to
 theorem-grade
- that the minimum-information law has been promoted from post-axiom
- that `(sqrt(6)/3, sqrt(6)/3)` has been derived as the physical
 admissible source

If any future revision tightens those boundaries, it must cite a new
source on the live retained/promoted surface. Until then, the safe read
is: **quadratic-order unanimity theorem + cubic-order obstruction; the selector gate
open with strictly narrower variational sub-gap**.
