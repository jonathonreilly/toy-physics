# Koide Matrix-Unit Source Law + Cyclic Projection (Route 2, axiom-only)

**Date:** 2026-04-18
**Status:** PARTIAL — full 9-real `dW(E_ij)` structure pinned up to **one real
scalar** by Cl(3)/Z³ axioms on the retained surface; the cyclic projection
then forces the law `2 r_0^2 = r_1^2 + r_2^2` only after a **named open
primitive** fixes that scalar.
**Runner:** `scripts/frontier_koide_matrix_unit_source_law_cyclic_projection.py`

## Unit system

Lattice / Cl(3) internal units throughout. All operators on the retained
`hw=1` triplet are dimensionless endomorphisms of `C^3`. Real trace pairing
`⟨A, B⟩ := Re Tr(A^† B)` used without further rescaling.

## Axiom base

Only the retained package axioms used below:

1. **Cl(3) on Z³** — spatial lattice action with the induced `C_3[111]`
   corner-cycle.
2. **Retained triplet** — `T_1 = hw=1 = span{X_1, X_2, X_3}`, with the
   three elementary translations acting as
   `T_x = diag(-1,+1,+1), T_y = diag(+1,-1,+1), T_z = diag(+1,+1,-1)`
   and the induced `C = C_3[111]` permuting `X_1 → X_2 → X_3 → X_1`
   ([THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)).
3. **Observable principle** — the unique additive CPT-even scalar generator
   on the exact Grassmann partition amplitude is
   `W[J] = log|det(D + J)| − log|det D|`
   ([OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)).
4. **Retained second-order return shape** — the effective operator on `T_1`
   at second order in `Γ_1` is
   `diag(w_{O_0}, w_a, w_b)` on the species basis, with the fourth slot
   `w_c` irrelevant
   ([HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md](./HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md)).
5. **Schur inheritance** — if the larger carrier is `C_3[111]`-covariant and
   the reduction is the equivariant Schur complement, the reduced operator on
   `T_1` is circulant
   ([KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md](./KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18.md)).

No PDG masses, no fitted flavor input, no CKM / Jarlskog anywhere.

## Retained matrix units

Let `C` be the retained `C_3[111]` forward cycle on `T_1`, `P_i = |X_i⟩⟨X_i|`
the translation-character projectors. Then the 9 operators
```
E_ij = P_i C^{k(i,j)} P_j,    with k(i,j) the unique k in {0,1,2}
                               such that C^k X_j = X_i.
```
span `M_3(C)` on `T_1` (Three-Generation Observable Theorem), and their
Hermitian closure spans `Herm(3)`. Under `C_3`-conjugation,
```
C E_ij C^{-1} = E_{(i+1),(j+1)}  (indices mod 3),
```
so the 9-real Hermitian closure decomposes as `Herm(3) = V_0 ⊕ V_1 ⊕ V_{-1}`
under the `C_3`-cycling, where `V_0` is the 3-real **circulant** subspace
(trivial isotypic) and `V_{±1}` each carry 3 real dimensions of
non-circulant content.

## Step 1 — The observable principle forces a linear Hermitian response

From the observable principle and `D` on `T_1`:
```
dW(X) = (d/dt)|_{t=0} log|det(D + tX)| = Re Tr(X · D^{-1})  =: Re Tr(X · G),
```
with `G := D^{-1}` the retained Hermitian response operator on `T_1`
(Hermitian whenever `D` is Hermitian, which follows on the CPT-even scalar
generator). So **`dW` is a real-linear functional on Herm(3)**, determined by
one element `G ∈ Herm(3)` via the real trace pairing:
```
dW(E_ij) = Re(G_{ji}),   i,j ∈ {1,2,3}.
```
The 9-real response tuple is therefore
```
R_ij := dW(E_ij) = Re G_{ji}.
```
This is 9 real numbers a priori — but the axioms below cut it down.

## Step 2 — Cl(3)/Z³-covariance forces `G` circulant

The retained `D` arises from `Γ_1`-type hops on the Cl(3)/Z³ carrier (HW1
second-order return shape theorem) and, after the full-lattice Schur descent
(Schur Inheritance Theorem), from any `C_3[111]`-covariant parent. In both
cases,
```
C D C^{-1} = D,
```
so `C G C^{-1} = G` on `T_1`. Hence `G` is **circulant Hermitian**:
```
G = g_0 I + g_1 C + g_1^* C^2,    g_0 ∈ R, g_1 ∈ C.
```
So the exact retained `G` has only **3 real parameters** `(g_0, α, β)` where
`g_1 = α + i β`. This collapses the 9-real `R_ij` tuple as follows.

### Step 2a — closed form for `R_ij`

Since `(C^k)_{ji} = δ_{j, i+k \bmod 3}`, and writing `s(i,j) := (j - i) \bmod 3`:
```
G_{ji} = g_0 δ_{ij} + g_1 δ_{j, i+1} + g_1^* δ_{j, i+2}      (mod 3).
```
Hence
```
R_ij = Re G_{ji} =
   { g_0                    if s(i,j) = 0,
   { α                      if s(i,j) ≡ 1  (mod 3),
   { α                      if s(i,j) ≡ 2  (mod 3).
```
Only **one real number (`g_0`) on the diagonal** and **one real number (`α`)
on both off-diagonals** survives in the 9-real Hermitian tuple. The imaginary
part `β` is invisible to `dW` on bare `E_ij`'s with `i ≠ j`, because the
matrix unit `E_ij` has a single `1` at position `(i,j)`, whose trace with `G`
picks up `G_{ji}`, and `Re G_{ji}` is the same on `s ≡ 1` and `s ≡ 2`.

To expose `β`, use the **antisymmetric combinations**
```
Y_ij := i(E_ij − E_ji)  ∈ Herm(3),
```
which are the standard antisymmetric Hermitian off-diagonals. Then
```
dW(Y_ij) = Re Tr(i(E_ij − E_ji) G) = Re[i G_{ji} − i G_{ij}]
         = −Im G_{ji} + Im G_{ij}.
```
By the circulant form of `G`, with `g_1 = α + iβ`:
- `s(i,j) ≡ 1`: `G_{ji} = g_1` so `Im G_{ji} = β`, and `G_{ij} = g_1^*` so
  `Im G_{ij} = −β`. Hence `dW(Y_ij) = −β + (−β) = −2β`.
- `s(i,j) ≡ 2`: `G_{ji} = g_1^*`, `G_{ij} = g_1`, so
  `dW(Y_ij) = +β + β = +2β`.

So the symmetric / antisymmetric off-diagonal split gives exactly:
```
dW(E_ij + E_ji) = 2 α       for every adjacent pair,   (symmetric sector)
dW(Y_12) = dW(Y_23) = −2 β      (these are s=1 pairs)
dW(Y_13)            = +2 β      (this is an s=2 pair)
```
This is a 3-real law `(g_0, α, β)` saturating the full 9-real Hermitian
matrix-unit response.

## Step 3 — Cyclic projection

The canonical cyclic projector
`P_cyc(X) = (1/3) ∑_{k=0}^2 C^k X C^{-k}`
has image exactly `span_R{B_0, B_1, B_2}` with
```
B_0 = I,    B_1 = C + C^2,    B_2 = i(C − C^2).
```
The basis-level projection (verified numerically in the runner) is:
```
P_cyc(D_i) = B_0 / 3              (diagonals)
P_cyc(X_ij) = B_1 / 3              (symmetric off-diagonals, all three pairs)
P_cyc(Y_12) = P_cyc(Y_23) = − B_2 / 3,
P_cyc(Y_13)               = + B_2 / 3.
```
(The DWEH Compression Theorem uses an opposite sign convention on Y_ij or
reversed cycle direction — the algebraic statement is identical up to that
overall sign; our conventions are internally consistent and numerically
verified.)

Because `dW` is real-linear and `C`-invariant (since `G` is circulant), it
factors through `P_cyc`:
```
dW(X) = dW(P_cyc(X))    ∀ X ∈ Herm(3).
```
Applying `dW` directly to each compressed basis element:

- `r_0 := dW(B_0) = dW(I) = Re Tr(G) = 3 g_0`.
- `r_1 := dW(B_1) = dW(C + C^2) = Re[Tr(CG) + Tr(C^2 G)]`.
  From the circulant form, `Tr(CG) = 3 g_1^*` and `Tr(C^2 G) = 3 g_1`, so
  `r_1 = Re(3 g_1^* + 3 g_1) = 6 α`.
- `r_2 := dW(B_2) = dW(i(C − C^2)) = Re[i(Tr(CG) − Tr(C^2 G))]
        = Re[i(3 g_1^* − 3 g_1)] = Re[−3i · 2i Im g_1] = 6 β`.

So the **three cyclic channels land at**
```
r_0 = 3 g_0,     r_1 = 6 α,     r_2 = 6 β.
```

This is the exact 3-real cyclic response law from the retained Cl(3)/Z³
data, with all algebra shown.

### Cross-check via the antisymmetric-sector Y-sum

Using the signs of Step 2a together with the Y-sum formula that is tied to
the sign convention of `P_cyc(Y_ij)`:
```
dW(Y_12) + dW(Y_23) − dW(Y_13)
   = (−2β) + (−2β) − (+2β) = −6β = −r_2.
```
The Y-sum reconstructs `−r_2` in this convention (equivalently `+r_2` in
the DWEH note's convention). Both statements carry the same information;
only the overall sign is convention-dependent.

## Step 4 — Is the Koide circle law `2 r_0^2 = r_1^2 + r_2^2` forced?

Substituting:
```
2 r_0^2 − (r_1^2 + r_2^2) = 2·9 g_0^2 − (36 α^2 + 36 β^2)
                          = 18 (g_0^2 − 2 α^2 − 2 β^2)
                          = 18 (g_0^2 − 2 |g_1|^2).
```
So the Koide relation is **equivalent to the single scalar selector**
```
g_0^2 = 2 |g_1|^2                       (circulant response-circle)
```
on the retained 3-real circulant response `G = g_0 I + g_1 C + g_1^* C^2`.

This is identical — coefficient-for-coefficient — to the **one-scalar
selector** named in
[KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md](./KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md).
Route 2 does not remove that scalar — it lands on it from a different
direction.

### What Cl(3)/Z³ does pin

1. The 9-real response tuple `R_ij = Re G_{ji}` collapses to 3-real
   `(g_0, α, β)` by `C_3[111]`-covariance. **Full pin, axiom-only.**
2. Antisymmetric sector exposes `β` exactly. **Full pin, axiom-only.**
3. The cyclic-projection formulas `r_0 = 3 g_0, r_1 = 6 α, r_2 = 6 β`.
   **Full pin, axiom-only.**

### What Cl(3)/Z³ does not pin

The scalar ratio `g_0 / |g_1|`. `Cl(3)/Z³` plus the observable principle
plus Schur equivariance gives `G ∈ {g_0 I + g_1 C + g_1^* C^2}`; it **does
not** force the specific scalar `g_0^2 = 2 |g_1|^2`.

This is exactly the charged-lepton microscopic scalar selector named
already on the selected slice:
```
g_0 ↔ (Tr G)/3,  
|g_1|^2 ↔ nonzero off-diagonal magnitude of G.
```
with the one-real remaining selector coefficient `m` on the selected slice
being in bijection with the Koide-determining ratio `g_0^2 / |g_1|^2`.

## Step 5 — Does the full-lattice Schur projection force `2 r_0^2 = r_1^2 + r_2^2`?

No — and here is the exact statement. The Schur Inheritance Theorem
(KOIDE_FULL_LATTICE_SCHUR_INHERITANCE_NOTE_2026-04-18) proves only that
the reduced operator on `T_1` is **circulant**. It says nothing about the
ratio of the 3 retained real parameters `(g_0, α, β)`. In fact the proof
explicitly lists among the escape hatches:
> "3. a new readout primitive replacing the current axis-diagonal `U_e = I_3`
> evaluation;"
> "2. a non-Schur or non-`C_3`-equivariant reduction map..."
i.e., the obstruction *includes* the blindness of the reduction class to the
circle condition.

So the Schur descent **does not** by itself close the Koide circle; it only
ensures the projected operator lives on the 3-real circulant target where
the circle condition *can* be imposed.

## Exit classification

**PARTIAL.** Named open primitive:

> **one microscopic scalar selector law** — the retained scalar
> `κ := g_0^2 / |g_1|^2` on the circulant response `G`.
>
> Equivalently, on the Z₃ selected slice coordinate `m` of the charged
> kernel `K_Z3^sel(m) = K_frozen + m T_m^{(K)}`, the one real coefficient
> named in
> [KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md](./KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md).

The Koide target `2 r_0^2 = r_1^2 + r_2^2` reduces, on the matrix-unit
basis with full Schur-equivariant reduction, to **exactly one real equation
`κ = 2`** on that scalar. Everything else — the 9→3 matrix-unit compression,
the identification of `(r_0, r_1, r_2)` as `(3 g_0, 6 α, 6 β)`, the closure
of antisymmetric content — is derived axiom-only on the retained Cl(3)/Z³
surface.

## What this note does close

- The **full 9-real `dW(E_ij)` law** on the retained matrix-unit basis is
  derived from the axioms up to the three-real circulant response `G`.
- The **Schur projection onto the cyclic bundle** is identified with
  `C_3[111]`-averaging and produces the exact formulas
  `r_0 = 3 g_0, r_1 = 6 α, r_2 = 6 β`.
- The **Koide circle `2 r_0^2 = r_1^2 + r_2^2`** is shown to be equivalent,
  on this retained surface, to the single scalar relation
  `g_0^2 = 2 |g_1|^2` on `G = D^{-1}`.

## What this note does not close

- The scalar selector itself. Route 2 lands precisely on the same one-scalar
  gap already named by the April 18 scalar-selector target note and the
  frozen-bank decomposition. It does not supply a new axiom-only primitive
  that forces that scalar.
- Consequently Route 2 is **not** the final promotion pathway; it is a
  clean re-derivation of the same bottleneck from the larger 9-real
  matrix-unit basis. The larger basis contributes no new constraint
  because Cl(3)/Z³ commutation already forces `G` circulant before any
  projection.

## Relation to Route 1 (`W[J]` on the cyclic bundle)

Route 1 (observable-principle `W[J]` on `B_0, B_1, B_2`) is algebraically
the **same calculation** carried out in the 3-real cyclic coordinates from
the start. Route 2 confirms that starting larger and projecting yields no
new information: the Cl(3)/Z³ commutant already enforces circulant form
upstream, so the cyclic projection is a tautology once `G` is circulant.

Therefore Route 1 and Route 2 share the same open primitive. The
charged-lepton Koide gap is genuinely one microscopic scalar, and neither
the 9-real nor the 3-real basis changes that.

## Bottom line

The retained Cl(3)/Z³ surface derives:

- `dW(E_ij) = Re G_{ji}` on the 9-real matrix-unit basis;
- `G` circulant with 3 real parameters `(g_0, α, β)`;
- cyclic projection `r_0 = 3 g_0, r_1 = 6 α, r_2 = 6 β`;
- Koide circle `2 r_0^2 = r_1^2 + r_2^2 ⇔ g_0^2 = 2 |g_1|^2`.

It does **not** derive the last scalar. The named open primitive is
`κ := g_0^2 / |g_1|^2 = 2`, equivalently the `m`-coefficient on the
selected Z₃ slice.

**Classification: PARTIAL.** One named open primitive.
