# Koide Scalar-Selector Direct Attack — Axiom-Only Scout Note

**Date:** 2026-04-18
**Status:** SCOUT — attempted axiom-only derivation of the charged-lepton
selected-slice scalar `m`. Verdict: **DEAD on the retained surface; MISS-STRUCTURE
at the pure-axiom level.** Names the missing primitive explicitly.
**Runner:** `scripts/frontier_koide_scalar_selector_direct_attack_scout.py`

## Unit system

All equations are dimensionless in the retained `Cl(3)` Hermitian grammar on
the `hw=1` triplet. `m, δ, q_+` are the three real affine coordinates of the
live source-oriented chart (source-surface affine basis of the April-16
`ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY` note). Sign conventions match the
frozen-bank decomposition note.

## Axiom base

This attack uses **only**:

1. **A0.** Cl(3) on `Z^3` with the retained `hw=1` triplet `H_hw=1 = span{X_1,X_2,X_3}`.
2. **A1.** The retained `C_3[111]` induced cyclic shift `C : X_i -> X_{i+1}`.
3. **A2.** The retained lattice-translation characters that separate the
   triplet sectors (THREE_GENERATION_OBSERVABLE_THEOREM_NOTE).
4. **A3.** The observable principle `W[J] = log|det(D+J)| - log|det D|`
   (OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE) derived from Grassmann factorization
   + CPT-even scalar additivity.
5. **A4.** The exact retained Hermitian source-surface affine chart
   `H(m,δ,q_+) = H_base + m T_m + δ T_δ + q_+ T_q` (affine-boundary note).
6. **A5.** The parity-compatible observable selector slice `δ = q_+ = √6/3`
   (parity-compatible-observable-selector theorem).
7. **A6.** The frozen-bank decomposition
   `K_Z3^sel(m) = K_frozen + m T_m^(K)` (frozen-bank-decomposition note).

The retained source-surface package
`(γ = 1/2, E_1 = √(8/3), E_2 = √8/3)`, intrinsic slots `(a_*,b_*)`, and
intrinsic CP pair `(cp1,cp2)` are all consequences of A0–A5.

## Target

Derive the real scalar `m` on the selected slice from A0–A6 alone.

Four equivalent forms:
- `m = Re K_12 + 2·cp2  =  Re K_12 − 4√2/9`
- `m = K_00 + 2·cp2 + 3·cp1  =  K_00 − 4√2/9 + 6√6/9`
- `m = Tr K_Z3^sel`
- `m =` coefficient of `T_m^(K)` in `K_Z3^sel`

---

## Step 1 (exact, retained). The selected-slice decomposition is verified.

From A5+A6, substituting `δ = q_+ = √6/3` into the doublet-block point-selection
formulas gives
```
K_11 = 3 cp1/2 + cp2 − 1/(2√3)
K_22 = 3 cp1/2 + cp2 + 1/(2√3)
Im K_12 = −3 cp2/2
K_00 = m − 2 cp2 − 3 cp1
Re K_12 = m − 2 cp2
```
and therefore `K_Z3^sel(m) = K_frozen + m T_m^(K)` exactly, with
`T_m^(K) = E_00 + E_12 + E_21`.

**Numerical verification** (scout runner, Step 1 block): all six identities
hold to machine precision. Step 1 is a tautological re-derivation of the
frozen-bank note; it establishes the affine target.

## Step 2 (exact, retained). `T_m^(K)` lifts back to `T_m` in the H-basis.

Applying the Fourier unitary `U_Z3 = (1/√3) · DFT_3` and computing
`T_m^(H) := U_Z3 T_m^(K) U_Z3^†`, one obtains **exactly**
```
T_m^(H) = E_00 + E_12 + E_21  =  T_m   (from the affine-boundary note).
```

So the H-basis affine generator and the Z_3-basis direction agree identically.
This is consistent with the frozen-bank theorem and the active-affine theorem,
and confirms the two charts are the same affine target seen from two bases.

**Numerical verification** (scout runner, Step 2 block): `||T_m^(H) - T_m|| < 10^{-14}`.

## Step 3 (exact, retained). C_3[111] isotypic decomposition of `T_m`.

Under conjugation action of `C` on `M_3(C)` with trivial / ω / ω̄ isotypic
projectors,
```
P_triv(X) = (X + C X C^{-1} + C^2 X C^{-2}) / 3
P_ω(X)    = (X + ω̄ C X C^{-1} + ω C^2 X C^{-2}) / 3
P_ω̄(X)   = (X + ω  C X C^{-1} + ω̄ C^2 X C^{-2}) / 3
```
direct computation (Step 3 runner block) gives
```
P_triv(T_m) = (1/3)(I + C + C^2)  = (1/3)(B_0 + B_1)  ∈ span{B_0,B_1,B_2}
P_ω(T_m)    ≠ 0                    ∉ span{B_0,B_1,B_2}
P_ω̄(T_m)   ≠ 0                    ∉ span{B_0,B_1,B_2}
```
with explicit entries
```
[P_triv T_m]_{ij} = 1/3  (for all i,j)
[P_ω T_m]_{00}    = 1/3  ;  [P_ω T_m]_{12} = 1/3   (etc., full matrix computed)
```
and `P_triv(T_m) + P_ω(T_m) + P_ω̄(T_m) = T_m` (partition of unity).

**Key fact:** Of the 9 real degrees of freedom in `T_m`, only **2** land in
the cyclic bundle `span{B_0, B_1, B_2}` (equivalently the `C_3`-trivial-isotypic
Hermitian circulants). The other 6 real degrees of freedom, including the
off-diagonal signature `E_12 + E_21`, sit in the non-trivial ω and ω̄ isotypic
sectors.

## Step 4. Direct attack route 1 — observable principle on the cyclic bundle.

Following KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE and the positive-paths
Approach 1, compute
```
r_i = dW(B_i) |_{H = H_sel(m)}
```
at linear order in the source-surface Hermitian:
```
r_0 = Re Tr[H_sel(m) B_0] = Re Tr[H_sel(m)]
r_1 = Re Tr[H_sel(m) B_1] = Re Tr[H_sel(m) (C+C^2)]
r_2 = Re Tr[H_sel(m) B_2] = Re Tr[H_sel(m) · i(C-C^2)]
```

**Arithmetic** (scout runner, Step 4 linear block):
- `H_base` has zero diagonal, so `Tr H_base = 0`.
- `Tr T_m = 1`, `Tr T_δ = 0`, `Tr T_q = 0` → `r_0(m) = m`.
- `Tr(H_base B_1) = −2√8/3` (direct computation from the explicit `H_base`).
  Combined with `Tr(T_m B_1) = 2`, `Tr(T_δ B_1) = 0`, `Tr(T_q B_1) = 6`, on the
  selected slice:
  `r_1(m) = −2√8/3 + 2m + 6·(√6/3) = 2m + 2√6 − 2√8/3`.
- `r_2 = Re Tr(H_sel · i(C-C^2)) = −1` on the selected slice
  (independent of m — comes from the frozen antisymmetric part of
  `H_base + q_+ T_q + δ T_δ`).

Testing the cyclic selector `2 r_0^2 − r_1^2 − r_2^2 = 0`:

Substituting the explicit linear formulas above gives a quadratic in `m`
whose zero at `m ≈ −1.003` is **numerical** and does **not** reproduce the
Koide charged-lepton point `m_* ≈ −1.16047` from the closure note (which in
turn is set by the imported `H_*` witness ratio, not by any axiom-only
equation).

**Reason for failure:** the linear observable-principle on the cyclic bundle
projects `T_m` onto its trivial isotypic part. It therefore sees only
`(1/3)(B_0 + B_1)` of the affine direction, and misses the 6 non-trivial
isotypic real parameters that distinguish the Koide `T_m` from a generic
circulant. The selector equation on the trivially-projected bundle is not
the selected-slice Koide equation.

**Verdict on attack 1:** MISS-STRUCTURE. The retained cyclic bundle is
fundamentally smaller than the object `T_m` lives in. Pushing to higher
orders in `J` does not repair this, because the ω and ω̄ isotypic sectors of
`T_m` remain orthogonal to all products of cyclic-bundle sources `B_i · B_j`
(they stay in the same isotypic class under convolution).

## Step 5. Direct attack route 2 — full retained matrix units.

The three-generation observable theorem proves that the retained operator
algebra on `hw=1` is the **full** matrix algebra `M_3(C)`, generated by
`E_ij = P_i C^k P_j`.

So **9 real retained responses** `r_{ij} = dW(E_ij) = Re Tr[(D+J)^{-1} E_ij]`
exist. They determine every matrix entry of `(D+J)^{-1}`.

But this is just the statement that `H` itself is retained as a 9-real-parameter
Hermitian operator. It does **not** select a value of any one of those 9
parameters — it merely confirms all 9 are observable.

The only retained quadratic invariant candidates that might pin `m` are:

1. **The Koide selector `2 r_0^2 = r_1^2 + r_2^2`** — already shown above to
   be the cyclic-bundle projection, hence blind to the non-trivial isotypic
   components of `T_m`.
2. **The block democracy / real-irrep equipartition principle A1** (Frobenius
   `3a² = 6|b|²` on the circulant eigenvalue triple, per
   `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`) — applies to
   the circulant sector only; `T_m` has a 6-real non-circulant piece.
3. **The square-root / P1 readout** (`λ_k = √m_k`) — not a retained theorem;
   still a named-missing primitive in the positive-paths note.

No fourth retained quadratic invariant sensitive to the ω/ω̄ isotypic part
of `T_m` is on the science stack.

**Verdict on attack 2:** DEAD. The retained M_3(C) algebra is available, but
no retained scalar functional on it distinguishes m from any other value.

## Step 6. Direct attack route 3 — m-spectator theorem as blocker.

The `DM_NEUTRINO_SOURCE_SURFACE_M_SPECTATOR_THEOREM_NOTE_2026-04-16` is
explicit:

> the intrinsic slot pair `(a_*, b_*)`, intrinsic CP pair `(cp1, cp2)`, exact
> source package, and slot-torsion are all **constant along the m-direction**.

The frozen-bank decomposition extends this to the selected slice: every
exact retained scalar built from `H` via the current bank has zero derivative
in `m`.

Therefore **no retained scalar functional of H can fix m on the selected slice**.
This is a theorem, not a claim.

Any axiom-only derivation of `m` must therefore rely on a primitive that is
**strictly outside** the current retained bank. The positive-paths note
names the three candidate extensions (A1 equipartition, P1 square-root
readout, and the positive parent). None are retained today.

## Verdict

**DEAD** on the retained surface; **MISS-STRUCTURE** at the pure Cl(3)/Z^3
axiom level.

Precisely:

- Every step from A0–A6 to `K_Z3^sel(m) = K_frozen + m T_m^(K)` is exact and
  retained.
- `T_m` has essential weight (6/9 of its real degrees of freedom) in the ω/ω̄
  isotypic sectors of the C_3[111] action.
- The retained cyclic bundle `{B_0, B_1, B_2}` and its observable-principle
  readouts see only the trivial-isotypic projection of `T_m`. They are blind
  to the selector coordinate.
- The m-spectator theorem proves the **whole** current retained bank is
  blind to `m`.
- The three named extension primitives in the positive-paths note (A1, P1,
  positive parent) are each non-retained; any of them would be a **new axiom
  outside Cl(3)/Z^3**.

## Named missing primitive

**P_m (isotypic response readout).** A retained scalar functional
`S : Herm(3) → R` on the `hw=1` triplet that
- is C_3[111]-equivariant (hence descends to a function of the three
  isotypic projections),
- is not a pure function of the trivial-isotypic circulant sector, and
- derivably vanishes (or takes a derivable constant value) on the selected
  slice `δ = q_+ = √6/3`, thereby pinning `m = m_*`.

Equivalent formulations of P_m:

- A retained scalar `S : Herm(3) → R` sensitive to the Hermitian ω-isotypic
  component `P_ω(H) + P_ω̄(H)` whose stationarity in `m` on the selected
  slice fixes `m_*`.
- A derivation of the `√m_k` (P1) readout, which upgrades the cyclic-bundle
  selector to act directly on the physical mass-square-root spectrum and
  thereby pins `m` via the Koide cone.
- A derivation of the `H_*` witness ratio
  `κ_* = √3 r_2 / (2 r_0 − r_1) ≈ −0.6079` as a sole-axiom cyclic-response
  law (cyclic-response bridge note).

Any one of these, once retained, closes the gap.

## Observational check (NOT a derivation)

Observed charged-lepton masses (PDG 2024) give Koide `Q = 2/3` to `5·10^{-5}`
and `δ ≈ 2/9 rad` to `4·10^{-4}`. On the selected-line closure route, the
corresponding scalar value is `m_* ≈ −1.16047` (matching
`κ_* ≈ −0.6079`). This is observational verification of the target, not a
derivation.

## Consequence for the promotion gate

Charged-lepton Koide promotion remains **bounded observational-pin only** on
the current retained surface.

The frozen-bank decomposition has successfully compressed the promotion gap
to a single real scalar, but a direct Cl(3)/Z^3-only derivation of that
scalar is structurally obstructed by the m-spectator theorem. One additional
retained primitive (P_m above) is required. The positive-paths note still
correctly names the three strongest candidate routes, all of which are
extensions, not fresh axiom consequences.

## Relation to Codex P1 finding

First-round reviewer finding P1 (Ward/blockers) objected that the circulant
derivation uses non-retained equipartition (A1) and spectral identification
(`λ_k = √m_k`). The present scout note strengthens that objection: even
**before** A1 and `λ_k = √m_k` are invoked, the scalar `m` itself is
already unreachable from the retained surface by an m-spectator obstruction.
A1 and P1 are therefore not optional add-ons that the circulant derivation
happened to use; they are **exactly** the kind of extension primitive P_m
that would close the gap.

## Reproduction

```
PYTHONPATH=scripts python3 scripts/frontier_koide_scalar_selector_direct_attack_scout.py
```
