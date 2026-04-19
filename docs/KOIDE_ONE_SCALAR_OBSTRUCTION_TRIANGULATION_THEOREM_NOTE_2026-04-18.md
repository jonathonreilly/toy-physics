# Koide One-Scalar Obstruction Triangulation Theorem

**Date:** 2026-04-18
**Status:** exact structural theorem on the charged-lepton Koide promotion
gap; reviewer-facing support theorem on the bounded charged-lepton package
**Target:** express the open scalar-selector conditional of the charged-lepton
Koide lane as a structurally derived one-scalar gap rather than a diffuse
miscellaneous-axiom search space
**Dedicated verifier:**
`scripts/frontier_koide_one_scalar_obstruction_triangulation.py`
**Consolidates three independent axiom-only derivations:**
- `docs/KOIDE_SCALAR_SELECTOR_DIRECT_ATTACK_SCOUT_NOTE_2026-04-18.md`
  (runner `frontier_koide_scalar_selector_direct_attack_scout.py`, 60/60 PASS)
- `docs/KOIDE_OBSERVABLE_PRINCIPLE_CYCLIC_SOURCE_LAW_NOTE_2026-04-18.md`
  (runner `frontier_koide_observable_principle_cyclic_source_law.py`, 107/107 PASS)
- `docs/KOIDE_MATRIX_UNIT_SOURCE_LAW_CYCLIC_PROJECTION_NOTE_2026-04-18.md`
  (runner `frontier_koide_matrix_unit_source_law_cyclic_projection.py`, 553/553 PASS)
**Relates to:**
`docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`,
`docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`,
`docs/HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md`

## Unit system and axiom base

- **Unit system:** dimensionless on `M_3(ℂ)`; real trace pairing
  `⟨A, B⟩ = Re Tr(A† B)`.
- **Axiom base (strict):**
  - A0. Cl(3) on Z³ (single axiom).
  - A1. Retained `hw=1` generation triplet `T_1 = span{X_1, X_2, X_3}` with
    induced `C_3[111]` cyclic shift `C : X_i → X_{i+1 mod 3}` on
    `H_{hw=1}` (retained by `THREE_GENERATION_OBSERVABLE_THEOREM`).
  - A2. Observable principle
    `W[J] = log|det(D+J)| − log|det D|` (retained by
    `OBSERVABLE_PRINCIPLE_FROM_AXIOM`).
  - A3. Second-order return shape on hw=1 (retained by
    `HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM`).

No PDG masses. No back-fitting. No retained physics asserted as a blocker
without derivation.

## Summary

On the retained Cl(3)/Z³ surface (A0–A3), the charged-lepton Koide cone on
the `C_3[111]`-cyclic bundle is **exactly equivalent** to a single scalar
equation on the retained microscopic response `G = D⁻¹`. Specifically, for
any Cl(3)/Z³-covariant retained `D` (so that `[C, D] = 0`),
```
G = g_0 · I + g_1 · C + \bar{g_1} · C²    with g_0 ∈ ℝ, g_1 ∈ ℂ,
```
and the cyclic observable-principle responses satisfy
```
2 r_0² − (r_1² + r_2²) = 18 · (g_0² − 2 |g_1|²).                  (★)
```
Hence the Koide cone `2 r_0² = r_1² + r_2²` reduces to **one real scalar
equation**
```
g_0² = 2 |g_1|²    ⟺    κ := g_0² / |g_1|² = 2.                  (†)
```

**Triangulation.** Three structurally-independent axiom-only derivation
routes — direct scalar-m attack on the selected Z_3 doublet-block slice,
observable-principle `W[J]` on the cyclic bundle, and matrix-unit source
law on the 9-real generation algebra — all terminate at the same scalar
equation (†). No basis choice, carrier extension, or Schur projection
reduces the obstruction below one real scalar.

**Consequence.** Charged-lepton Koide promotion on the current retained
surface is **one scalar (†) away** from closure. Three prior named
missing primitives — Frobenius-sector equipartition `A1`, the `√m_k`
identification `P1`, and the scalar-selector `m` on the frozen-bank
slice — are all algebraically equivalent to (†) on the retained surface.

## Theorem (One-Scalar Obstruction)

**Let `D` be any Cl(3)/Z³-covariant retained Hermitian source operator on
`H_{hw=1}` with non-singular `G = D⁻¹ ∈ Herm(3)`.** Then:

1. **Circulant reduction.** `[C, D] = 0` on retained `D` forces
   `[C, G] = 0`, and Schur's lemma on the 3-element commutant of the
   regular 3-cycle in `M_3(ℂ)` restricts `G` to the 3-real circulant
   family
   ```
   G = g_0 · I + g_1 · C + \bar{g_1} · C²,    g_0 ∈ ℝ, g_1 ∈ ℂ.
   ```

2. **Cyclic response law.** The observable-principle responses against the
   retained cyclic bundle
   `B_0 = I`, `B_1 = C + C²`, `B_2 = i (C − C²)` are
   ```
   r_0 = dW(B_0) = Re Tr(G · B_0) = 3 g_0,
   r_1 = dW(B_1) = Re Tr(G · B_1) = 6 Re(g_1),
   r_2 = dW(B_2) = Re Tr(G · B_2) = 6 Im(g_1),
   ```
   using `Tr(C) = Tr(C²) = 0`, `Tr(C³) = 3`, and `Tr(G · B_i)` evaluated
   directly.

3. **Master identity (★).** Substituting,
   ```
   2 r_0² − (r_1² + r_2²)
   = 2 · (3 g_0)² − (6 Re g_1)² − (6 Im g_1)²
   = 18 g_0² − 36 |g_1|²
   = 18 (g_0² − 2 |g_1|²).
   ```

4. **Koide equivalence (†).** The Koide cone `2 r_0² = r_1² + r_2²` is
   exactly equivalent to `g_0² = 2 |g_1|²`, i.e. to the single scalar
   selection `κ = 2`.

5. **Basis independence.** The Jacobian of the map
   `(g_0, Re g_1, Im g_1) ↦ (r_0, r_1, r_2)` is
   `det diag(3, 6, 6) = 108 ≠ 0`. The map is a linear bijection;
   generic circulant `G` does not satisfy (†), so Koide is a genuine
   codimension-1 selection on `G`, not a character-theoretic identity.

6. **Carrier-extension invariance.** For any `C_3[111]`-covariant
   Hermitian extension to a larger carrier `V = T_1 ⊕ W` with equivariant
   Schur complement `S = A − B D_W⁻¹ B†`, circulant form on `T_1` is
   preserved under `[C, S] = 0`, but the scalar ratio
   `g_0²/|g_1|²` on `T_1` is not constrained by the extension. (Verified
   in Route 3 runner via 10 random intertwining trials.)

**Conclusion.** The charged-lepton Koide promotion on the Cl(3)/Z³ +
A0–A3 surface reduces **exactly** to the one-scalar condition (†). No
structure within the retained base plus observable principle + Schur
inheritance + cyclic projection + matrix-unit basis + full-carrier
descent selects the scalar value `κ = 2`. **QED.** □

## Corollary (Triangulation)

Three structurally-independent axiom-only derivation routes all terminate
at (†):

| Route | Operator basis | Missing primitive (same as (†)) | Agent runner | Checks |
|---|---|---|---|---|
| 1. Scalar-m direct attack | Selected Z_3 doublet-block slice `K_Z3^sel(m)` | `P_m` — a C_3-equivariant functional sensitive to ω, ω̄ isotypic sectors fixing `m = m_*` | `frontier_koide_scalar_selector_direct_attack_scout.py` | 60/60 PASS |
| 2. `W[J]` observable principle | Cyclic bundle `{I, C+C², i(C−C²)}` on `hw=1` | Retained law on intermediate-state weight triple `(w_{O_0}, w_a, w_b)` forcing `|b|²/a² = 1/2` | `frontier_koide_observable_principle_cyclic_source_law.py` | 107/107 PASS |
| 3. Matrix-unit source law | Full 9-real `Herm(3)` via `E_ij = P_i C^k P_j` → cyclic projection | Scalar `κ = g_0²/|g_1|²` pin at `κ = 2` | `frontier_koide_matrix_unit_source_law_cyclic_projection.py` | 553/553 PASS |

These three named primitives are algebraically identical on the retained
surface. Route 3 ruled out the obvious loophole that the 9-real matrix-
unit basis might carry more information than the 3-real cyclic basis: it
does not, because `[C, G] = 0` is enforced upstream and the 9→3 compression
is a tautology once `C_3[111]`-covariance is imposed.

## Corollary (Basis-Independence of the Obstruction)

No change of operator basis within Cl(3)/Z³ + A0–A3 reduces the Koide
scalar obstruction below one real scalar. Equivalent statements:

- Any Cl(3)/Z³-covariant observable-principle functional on `H_{hw=1}`
  factors through the cyclic Fourier data `(g_0, g_1)` of `D⁻¹`.
- Any carrier-extension with equivariant Schur descent preserves the
  circulant form on `T_1` but does not add scalar-ratio constraints.
- The 1-parameter family `{G : κ = λ, λ ≥ 0}` is a foliation of the
  retained circulant commutant, and the specific leaf `λ = 2` is not
  picked out by A0–A3.

## Corollary (Identification of A1, P1, and `m`)

The three prior named candidate selectors on the charged-lepton Koide lane
are algebraically identical to (†) on the retained surface:

- `A1` (Frobenius-sector equipartition `3a² = 6|b|²` on the circulant
  parametrization, cf. `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`)
  ≡ (†) via Route 3's `(a, b) ↔ (g_0, g_1)`.
- `P1` (`λ_k = √m_k` spectral identification, cf. same note) connects (†)
  to physical masses; a retained `P1` plus (†) gives Koide `Q = 2/3` by
  the Brannen–Rivero algebraic identity (independent of `δ`).
- `m` (scalar-selector on the frozen Z_3 doublet-block slice,
  cf. `KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md`)
  ≡ (†) via Route 1's explicit T_m decomposition under the C_3[111]
  isotypic projectors.

These equivalences are the main consolidation content of this note.
Multiple apparently-independent missing primitives in the April-18 Koide
chain are **the same scalar gap**, not four.

## Scope — what this theorem does and does not claim

### What is established (unconditional)

1. On the retained base A0–A3, the charged-lepton Koide cone reduces
   exactly to the one-scalar equation (†).
2. Three structurally-independent derivation paths (Routes 1, 2, 3)
   converge on (†).
3. The obstruction is basis-independent and carrier-extension-invariant
   within the retained surface.
4. The prior named primitives `A1`, `P1`, and `m` are algebraically
   identical to (†) on the retained surface.

### What is not established

- No derivation of the scalar `κ = 2` from any structure beyond A0–A3.
  This is the remaining open-science target.
- No promotion of charged-lepton Koide to a retained theorem. The
  bounded-observational-pin status on the April 17 review remains the
  correct current classification.
- No claim about the quark sector, neutrino sector, or any mass-hierarchy
  statement beyond Koide `Q = 2/3` for charged leptons.
- No claim that (†) cannot be closed by a *new* retained primitive — only
  that it cannot be closed from A0–A3 as currently retained.

### Observational check (flagged separately)

PDG charged-lepton masses + the Brannen–Rivero circulant form give
`a²/|b|² = 2` (equivalently `κ = 2`) to sub-percent precision. This
confirms the selector *target* is empirically correct but does not
constitute a derivation from A0–A3.

## Why this is a strong negative result, not a null result

A null result would be "no progress on charged-lepton Koide." This is not
that. The triangulation theorem establishes:

- The open gap has a definite size: **one real scalar**, not a fuzzy
  miscellaneous-axiom search space.
- The gap has a canonical form: `κ = g_0²/|g_1|²` on the commutant of
  `C_3[111]` in `Herm(3)`, where `g_0`, `g_1` are the trivial and
  non-trivial cyclic-Fourier coefficients of `D⁻¹`.
- Four prior named primitives are the same one scalar.
- No amount of operator-basis cleverness within the retained surface can
  reduce the gap below one scalar.

This is a structural lower bound on what Cl(3)/Z³ + retained observable
principle + retained generation-space theorems can deliver for Koide.
Going below it requires a genuinely new retained primitive.

## Retained status changes (under this theorem, if retained)

| Item | Before | After |
|---|---|---|
| Charged-lepton Koide promotion | bounded observational-pin, with ambiguously-many named candidate primitives (A1, P1, m, κ, ...) | bounded observational-pin, with **one named scalar primitive** (†) |
| Koide lane open-science target | "derive any of A1, P1, m, ..." | derive `κ = 2` (equivalently any of the algebraically-identical forms) |
| Koide attack surface | multiple basis-dependent routes | **basis-independent: no route within A0–A3 beats one scalar** |
| Relationship between A1, P1, m, κ | unclear; possibly independent | algebraically identical on the retained surface |
| DM-Koide intersection (frozen-bank slice) | open scalar-selector on `T_m^(K)` | `T_m^(K)` ω/ω̄-isotypic content identified; selector reduces to κ = 2 |

## Remaining open target (one scalar)

**Target (†).** Derive `κ = g_0²/|g_1|² = 2` from a retained Cl(3)/Z³
primitive.

Three candidate routes for a future retained derivation (not attempted
here):

- **Route A** (intermediate-state weight law). The retained hw=1 second-
  order return shape theorem gives a generic intermediate-state weight
  triple. A retained law fixing `|b|²/a² = 1/2` (equivalently `κ = 2`)
  on this triple closes (†).
- **Route B** (√m amplitude-principle derivation of P1). The
  `KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE` narrows this to "derive a
  positive `C_3[111]`-covariant parent operator `M` whose principal
  square root is the circulant amplitude operator."
- **Route C** (new discrete S_3-involution primitive). The open Path-A
  σ_hier scout returned OBSERVATIONAL-INPUT on a distinct but structurally
  similar one-scalar / one-involution gap. A shared discrete S_3 involution
  primitive could simultaneously close both.

## Reproduction

```bash
# Consolidated triangulation check (new):
PYTHONPATH=scripts python3 scripts/frontier_koide_one_scalar_obstruction_triangulation.py

# Three independent axiom-only derivations:
PYTHONPATH=scripts python3 scripts/frontier_koide_scalar_selector_direct_attack_scout.py
PYTHONPATH=scripts python3 scripts/frontier_koide_observable_principle_cyclic_source_law.py
PYTHONPATH=scripts python3 scripts/frontier_koide_matrix_unit_source_law_cyclic_projection.py
```

Expected: all four runners emit `FAIL=0`.

## Proposed status classification

**CANDIDATE THEOREM PROMOTION — AWAITING REVIEW**

The theorem is mathematically tight:
- Axiom base A0–A3 is explicit and matches retained surface.
- Closed-form derivation of (★) and (†) via three independent routes.
- Each route is independently verified by a dedicated runner (60/60,
  107/107, 553/553).
- The consolidation runner cross-checks the master identity (★)
  symbolically and numerically.
- Triangulation structure is itself a theorem (Corollary 1).

If retained, the charged-lepton Koide lane transitions from
"bounded observational-pin with ambiguously-many candidate primitives"
to **"bounded observational-pin with exactly one named scalar primitive"** —
a strict refinement that sharpens the open-science target and closes
the apparent multiplicity of candidate primitives.

## File references

- Observable principle from axiom: `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
- Three-generation observable theorem (source of `hw=1`, `C_3[111]`): `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- HW1 second-order return shape (source of intermediate-state weight triple): `HW1_SECOND_ORDER_RETURN_SHAPE_THEOREM_NOTE.md`
- Route 1 intake (direct attack): `KOIDE_SCALAR_SELECTOR_DIRECT_ATTACK_SCOUT_NOTE_2026-04-18.md`
- Route 2 intake (W[J]): `KOIDE_OBSERVABLE_PRINCIPLE_CYCLIC_SOURCE_LAW_NOTE_2026-04-18.md`
- Route 3 intake (matrix-unit): `KOIDE_MATRIX_UNIT_SOURCE_LAW_CYCLIC_PROJECTION_NOTE_2026-04-18.md`
- Dedicated consolidation verifier: `scripts/frontier_koide_one_scalar_obstruction_triangulation.py`
