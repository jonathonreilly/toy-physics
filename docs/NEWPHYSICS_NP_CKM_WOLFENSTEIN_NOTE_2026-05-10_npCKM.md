# NEWPHYSICS NP-CKM-Wolfenstein — P-Heavy-A Circulant Cabibbo No-Go

**Date:** 2026-05-10
**Probe:** NP-CKM-Wolfenstein
**Claim type:** no_go (source theorem)
**Status authority:** independent audit lane only; effective status is
pipeline-derived. This source note does not set or predict an audit outcome.

**Primary runner:**
[`scripts/cl3_newphysics_np_ckm_wolfenstein_2026_05_10_npCKM.py`](../scripts/cl3_newphysics_np_ckm_wolfenstein_2026_05_10_npCKM.py)
**Cached output:**
[`logs/runner-cache/cl3_newphysics_np_ckm_wolfenstein_2026_05_10_npCKM.txt`](../logs/runner-cache/cl3_newphysics_np_ckm_wolfenstein_2026_05_10_npCKM.txt)

## 0. Probe context

This probe tests whether the **P-Heavy-A primitive** introduced in
[`PRIMITIVE_P_HEAVYQ_SPECIES_PROPOSAL_NOTE_2026-05-10_pPheavyq.md`](PRIMITIVE_P_HEAVYQ_SPECIES_PROPOSAL_NOTE_2026-05-10_pPheavyq.md)
(PR #1044) — sector-dependent ρ-Koide Hermitian circulants on the retained
cyclic-three substrate C_3[111] — can produce the observed Wolfenstein CKM
structure (λ, A, ρ̄, η̄, J) through the canonical mass-eigenstate
diagonalization route

```text
V_CKM = U_up^dagger U_down
```

where `U_q` diagonalizes the Hermitian quark Yukawa matrix in sector
`q ∈ {up, down}`.

The headline result is a clean **negative source theorem** at structural
level: the P-Heavy-A primitive forecloses Cabibbo mixing entirely.
`V_CKM` is forced to be a permutation matrix; λ, A, ρ̄, η̄, J are forced to
`{0, 1}`-valued or zero. PDG `λ = 0.22500`, `A = 0.826`, `J ≈ 3.08 × 10⁻⁵`
are structurally unreachable on this primitive.

This probe does **not** claim a positive CKM derivation route. It is a
narrow no-go that prunes the P-Heavy-A admission's reach: P-Heavy-A may
remain viable for quark mass differentiation, but it does **not**
simultaneously close the CKM gap.

## 1. Existing framework context (cited, not promoted)

| Item | Content | Role here |
|---|---|---|
| Z1 | `N_gen = 3` retained (PR #952) | structural input |
| Z2 | `N_color = 3` retained (PR #954) | structural input |
| Z3 | C_3[111] cyclic structure on hw=1 generation triplet | structural input |
| Z4 | Hermitian circulants `H = aI + bC + b̄C²` on T_1 | structural input |
| Z5 | Circulant eigenvalues `λ_k = a + 2|b|cos(arg(b) + 2πk/3)` | structural input |
| Z6 | Z_3 Fourier basis diagonalizes C_3[111] (PR landing 2026-05-03) | structural input |
| Z7 | Z_3 generator C acts on H_{hw=1} (Z1 axis of Z^3) | structural input |
| Z8 | P-Heavy-A primitive: per-sector `(ρ_q, δ_q, v_0_q)` | candidate primitive under test |
| Z9 | Charged-lepton Brannen-Rivero context: `ρ_lep = √2`, `δ_lep = 2/9` | consistency surface |
| Z10 | `DM_NEUTRINO_CKM_TEXTURE_TRANSFER_NO_GO_NOTE_2026-04-15` | sister no-go (same-eigenbasis pattern, neutrino sector) |

The existing CKM structural-identity package
([`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md),
[`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md),
[`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md))
defines `λ²`, `A²`, `ρ`, `η` as algebraic structural identities over
`(n_pair, n_color, n_quark, α_s(v))`. That package does **not** derive
`V_CKM` from `U_up^† U_down` on the P-Heavy-A primitive. The present note
fills that exact gap with a negative finding.

## 2. Claim

On the P-Heavy-A admission surface (Z8) and the retained C_3[111]
substrate (Z3, Z4):

> **NP-CKM no-go.** Let `H_up = a_up I + b_up C + b̄_up C²` and
> `H_dn = a_dn I + b_dn C + b̄_dn C²` be the P-Heavy-A Hermitian circulants
> on H_{hw=1}, with `(ρ_q, δ_q, v_0_q)` admitted as sector-specific
> parameters. Then for every admissible
> `(ρ_up, δ_up, ρ_dn, δ_dn) ∈ (ℝ₊ × ℝ)²`:
>
> 1. `[H_up, H_dn] = 0` (commutator vanishes identically).
> 2. `H_up` and `H_dn` are simultaneously diagonalized by the Z_3 discrete
>    Fourier matrix `F`.
> 3. The CKM matrix `V_CKM = U_up^† U_down` is unitarily equivalent to a
>    permutation matrix; `|V_ij| ∈ {0, 1}` for every entry.
> 4. The Wolfenstein parameters obey `λ ∈ {0, 1}`, `A ∈ {0, 1}` (modulo
>    convention), `J = 0` exactly.
> 5. PDG Wolfenstein values `(λ, A, ρ̄, η̄, J) = (0.22500, 0.826, 0.159,
>    0.348, 3.08 × 10⁻⁵)` are structurally unreachable.

The no-go is **parameter-free**: it does not depend on any choice of
`(ρ_q, δ_q, v_0_q)`, on the canonical `α_s(v)`, on the retained `N_gen = 3`
or `N_color = 3` counts, or on any free parameter inside P-Heavy-A.

## 3. Cited inputs

| Input | Authority on `main` | Role |
|---|---|---|
| P-Heavy-A candidate primitive | [`PRIMITIVE_P_HEAVYQ_SPECIES_PROPOSAL_NOTE_2026-05-10_pPheavyq.md`](PRIMITIVE_P_HEAVYQ_SPECIES_PROPOSAL_NOTE_2026-05-10_pPheavyq.md) | candidate under test |
| C_3[111] cyclic substrate | [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) (Axiom 2, Z^3 substrate); existing 3-generation framework context | retained |
| Hermitian circulant family `H = aI + bC + b̄C²` | [`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md), and longer support chain | retained context |
| `N_gen = 3` | [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md) (PR #952 retention) | retained |
| `N_color = 3` | [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) (PR #954) | retained |
| PDG CKM observables (comparator only) | PDG 2024 CKM review | comparator (NOT derivation input) |

No PDG CKM matrix element, mass ratio, or fitted observable enters as a
derivation premise.

## 4. Derivation

### 4.1 Step 1 — Commutativity of circulants on a common cyclic group

The retained framework primitive is that `H_q` is a Hermitian element of
the algebra `ℂ[C_3] = span_ℂ{I, C, C²}` where `C` is the single Z_3
generator. Every element of `ℂ[C_3]` is a polynomial in `C`, and `C·C = C²`,
`C·C² = I`, so the algebra is commutative. In particular

```text
H_up · H_dn  =  (a_up I + b_up C + b̄_up C²) (a_dn I + b_dn C + b̄_dn C²)
              =  (a_dn I + b_dn C + b̄_dn C²) (a_up I + b_up C + b̄_up C²)
              =  H_dn · H_up.
```

So `[H_up, H_dn] = 0` for **every** admissible
`(a_q, b_q, b̄_q) ∈ ℝ × ℂ × ℂ`. This is verified numerically in **Test 7**
(`PASS=1, FAIL=0` over 30 random parameter pairs, max
`|[H_up, H_dn]| = 0` to machine precision).

### 4.2 Step 2 — Simultaneous diagonalization by the Z_3 Fourier matrix

Commuting normal operators are simultaneously diagonalizable (spectral
theorem, second form). Because `C` is unitary with spectrum
`{1, ω, ω²}` for `ω = e^(2πi/3)`, the orthonormal eigenbasis of `C` is the
Z_3 discrete Fourier matrix

```text
F  =  (1/√3) [ [1, 1,    1   ],
                [1, ω,    ω²  ],
                [1, ω²,   ω   ] ].
```

For every `(a, b, b̄)` in `ℂ[C_3]`,

```text
F^† H F  =  diag(λ_0, λ_1, λ_2)   with   λ_k = a + b ω^k + b̄ ω^{-k}
                                          = a + 2 Re(b ω^k)
                                          = a + 2 |b| cos(arg(b) + 2πk/3).
```

This recovers the framework's `λ_k = a + 2|b|cos(δ + 2πk/3)` formula
(retained context Z5). Both `H_up` and `H_dn` are diagonalized by the
**same** matrix `F`. **Test 1** verifies this on six representative
triples and **Test 8** confirms the same eigenbasis appears for the
charged-lepton Brannen-Rivero parameters `(ρ_lep, δ_lep) = (√2, 2/9)`.

### 4.3 Step 3 — V_CKM as a permutation matrix dressed by phases

`np.linalg.eigh` returns eigenvectors that span the eigenspaces of
`H_q` in some order, possibly with arbitrary unit phases. So

```text
U_up  =  F · P_up · D_up,        U_dn  =  F · P_dn · D_dn,
```

where `P_q ∈ S_3` is a permutation acting on the Fourier-index labels and
`D_q ∈ diag(U(1)³)` collects per-column phases. Then

```text
V_CKM  =  U_up^†  U_dn
       =  D_up^†  P_up^T  F^†  F  P_dn  D_dn
       =  D_up^†  P_up^T  P_dn  D_dn
       =  D_up^†  Π  D_dn,                    Π := P_up^T P_dn ∈ S_3.
```

Hence `V_CKM` is a permutation matrix dressed by overall column and row
phases. The magnitudes obey `|V_ij| ∈ {0, 1}` exactly. **Test 2**
verifies this on the P-Heavy-A fitted parameters
`(ρ_up, δ_up, ρ_dn, δ_dn) = (1.7600, 2.1729, 1.5450, 4.3022)`:

```text
|V_CKM|  =  [[ 7.36e-16   1.00      2.86e-16 ],
             [ 8.59e-18   2.85e-16  1.00     ],
             [ 1.00       8.35e-16  1.45e-16 ]].
```

**Test 5** confirms that the discrete permutation freedom yields exactly
6 distinct `|V_CKM|` patterns (the full symmetric group `S_3`), all with
0/1-valued magnitudes.

### 4.4 Step 4 — Random parameter sweep confirms parameter-free no-go

**Test 3** sweeps `(ρ_up, δ_up, ρ_dn, δ_dn)` over 25 random points in
`(0.1, 2.4) × (0, 2π) × (0.1, 2.4) × (0, 2π)` and confirms `V_CKM` is a
permutation to numerical precision (max deviation
`|V|² − round(|V|²)| < 10⁻⁸`). **Test 6** then performs a 12 × 12 × 12 × 12
grid sweep (20 736 parameter combinations) and reports `max |V[0, 1]|` is
either 0 or 1 to better than 10⁻⁸ — the off-diagonal magnitude in the
(generation-1, generation-2) block of the standard ordering — confirming
that the Cabibbo angle is not a continuous function of any P-Heavy-A
parameter.

### 4.5 Step 5 — Wolfenstein parameters are 0 or trivial

From the permutation structure:

```text
|V_us|  =  |V[0, 1]|  ∈  {0, 1}        →    λ = |V_us| ∈ {0, 1};
|V_cb|  =  |V[1, 2]|  ∈  {0, 1};
J       =  Im(V_us V_cb V_ub^* V_cs^*)  =  0   (one of the four factors is exactly 0).
```

**Test 4** numerically verifies these on the fitted P-Heavy-A parameters:
`|V_us|_pred = 1.000000`, `|V_cb|_pred = 1.000000`,
`|V_ub|_pred = 2.86 × 10⁻¹⁶`, `λ_pred = 1.000000`, `J_pred = 4.07 × 10⁻³²`,
all of which are far (relative) from PDG values
`(λ, |V_cb|, |V_ub|, J) = (0.22500, 0.04210, 0.00370, 3.08 × 10⁻⁵)`.

The density-of-rationals control test confirms that the PDG `λ = 0.22500`
is at distance ≥ 0.225 from the discrete admissible set `{0, 1}`, and
`|V_cb| = 0.04210` is at distance ≥ 0.0421. There is no parametric
relaxation of P-Heavy-A that closes this gap; the no-go is structural.

## 5. Why CP violation also dies

The Jarlskog invariant

```text
J  =  Im(V_us V_cb V_ub^* V_cs^*)
```

requires all four `V_ij` factors to be nonzero. Under the permutation
structure, at least one of `V_us, V_cb, V_ub, V_cs` is exactly zero
(at most one nonzero entry per row and per column). Therefore `J = 0`
exactly, independent of any phase choices in `D_up, D_dn`. The CP-plane
coordinates `(ρ̄, η̄) = (Re, −Im) (V_ud V_ub^* / V_cd V_cb^*)` also
vanish because either `V_ud V_ub^*` or `V_cd V_cb^*` involves a zero
factor.

This is consistent with the framework's prior `DM_NEUTRINO_CKM_TEXTURE_TRANSFER_NO_GO_NOTE_2026-04-15`
(2026-04-15), which foreclosed the analogous **lepton-sector** flavor
texture transfer on a different but structurally similar same-eigenbasis
argument.

## 6. What this rules out vs. what it permits

### 6.1 Ruled out (negative source theorem)

- Deriving Wolfenstein λ, A, ρ̄, η̄, J from V_CKM = U_up^† U_down with
  both `H_up, H_dn` Hermitian circulants on the SAME C_3[111] generator.
- Predicting the Cabibbo angle from the P-Heavy-A sector-specific `ρ_q`
  and `δ_q` parameters.
- A continuous family of CKM textures parameterized by `(ρ_q, δ_q)`.

### 6.2 Permitted by this no-go (i.e., not in conflict)

- The existing CKM atlas/axiom package
  (`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`, `WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`)
  remains an algebraic structural-identity package. It defines λ², A²,
  ρ, η as functions of `(n_pair, n_color, n_quark, α_s(v))` — not as
  outputs of a diagonalization. This note is orthogonal to that package.
- The P-Heavy-A primitive may still differentiate heavy-quark **mass
  ratios** (its original purpose), independent of CKM.
- A future CKM derivation could come from a primitive that breaks the
  shared-C_3[111] structure: for example, distinct cyclic generators on
  the two sectors (different `C_up`, `C_dn`), a non-cyclic flavor group
  on at least one sector, a left-right asymmetric basis with `U_L_q` and
  `U_R_q` separately fitted, or a unification step that couples
  generation indices to the isospin/color quantum number explicitly.
- The retained Z_3 cyclic structure itself is unaffected; the no-go
  only constrains the **two-circulant** form `V_CKM = U_up^† U_dn` with
  both `H_q` in `ℂ[C_3]`.

## 7. Test plan / runner result

| Test | What it checks | Numeric result |
|---|---|---|
| Test 1 | `F` diagonalizes 6 representative `H` triples | PASS=6, FAIL=0 |
| Test 2 | `V_CKM` is a permutation pattern on fitted P-Heavy-A params | PASS=5, FAIL=0 |
| Test 3 | Random sweep: `V_CKM` permutation to 10⁻⁸ | PASS=1, FAIL=0 |
| Test 4 | Wolfenstein λ, J far from PDG values; `J ≈ 0` | PASS=4, FAIL=0 |
| Test 5 | All 36 (`P_up`, `P_dn`) permutation pairs → 6 distinct `|V|` | PASS=2, FAIL=0 |
| Test 6 | Grid sweep 20 736 pts: `\max\|V[0,1]\| ∈ {0, 1}` | PASS=2, FAIL=0 |
| Test 7 | `[H_up, H_dn] = 0` over 30 random pairs | PASS=1, FAIL=0 |
| Test 8 | `F` diagonalizes charged-lepton Brannen-Rivero circulant | PASS=1, FAIL=0 |
| Density control | PDG λ, `|V_cb|` not in `{0, 1}` discrete set | PASS=2, FAIL=0 |
| **TOTAL** | | **PASS=24, FAIL=0** |

Reproduction:
```bash
python3 scripts/cl3_newphysics_np_ckm_wolfenstein_2026_05_10_npCKM.py
```

Expected output: `TOTAL: PASS=24, FAIL=0`.

## 8. Scope

This note claims:

- A no-go for CKM derivation from V_CKM = U_up^† U_down on the
  P-Heavy-A admission surface with both sectors on C_3[111].
- The Cabibbo angle, Wolfenstein A, CP-plane (ρ̄, η̄), and Jarlskog J
  are forced to discrete `{0, 1}`-valued or zero outputs by the shared-
  eigenbasis structure.
- The no-go is parameter-free and depends only on the retained
  primitives Z3–Z6.

This note does **not** claim:

- Any positive CKM derivation route.
- Refutation of P-Heavy-A as a quark-mass primitive (its original
  domain).
- Refutation of the existing CKM structural-identity package
  (algebraic-identity surface only; not a diagonalization claim).
- Any constraint on the up- and down-type Yukawa magnitudes beyond
  what's already in the framework.

## 9. Cross-references

- [`PRIMITIVE_P_HEAVYQ_SPECIES_PROPOSAL_NOTE_2026-05-10_pPheavyq.md`](PRIMITIVE_P_HEAVYQ_SPECIES_PROPOSAL_NOTE_2026-05-10_pPheavyq.md)
  — P-Heavy-A primitive under test.
- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
  — existing CKM structural-identity package (orthogonal to this note).
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  — algebraic Wolfenstein λ²/A² identities.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  — algebraic CP-plane identities `ρ = 1/6`, `η = √5/6`.
- [`DM_NEUTRINO_CKM_TEXTURE_TRANSFER_NO_GO_NOTE_2026-04-15.md`](DM_NEUTRINO_CKM_TEXTURE_TRANSFER_NO_GO_NOTE_2026-04-15.md)
  — sister no-go on the neutrino sector (same-eigenbasis pattern).
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
  — retained `N_gen = 3` source (PR #952).
- [`KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md`](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md)
  — Hermitian circulant family `H = aI + bC + b̄C²` (retained substrate).

## 10. Hostile-review tier classification

- **Would require explicit approval before promotion:** none. This is a
  source-only no-go that imports no new axiom and no new derivational
  primitive.
- **Context used by the diagnostic:** Hermitian circulant family on
  C_3[111] (retained); P-Heavy-A primitive (open-gate proposal, not
  promoted); discrete Z_3 Fourier basis.
- **Comparator only (NOT derivation input):** PDG 2024 CKM Wolfenstein
  values, used only to demonstrate the structural gap.
- **Cross-sector consistency:** matches the existing
  `DM_NEUTRINO_CKM_TEXTURE_TRANSFER_NO_GO_NOTE_2026-04-15` pattern.

## 11. Open follow-up (out of scope for this note)

If the framework eventually pursues a positive CKM derivation route, it
must break the shared-C_3[111] eigenbasis structure at one of the
following levels:

1. **Different cyclic generators per sector.** Replace the single Z_3
   on H_{hw=1} with two independent Z_3 actions whose generators are not
   simultaneously diagonalizable. Requires explaining why the generators
   differ (e.g., isospin-dependent boundary condition on the C_3 walk).
2. **Left-right asymmetric basis.** Treat `Y_q` as a general complex
   3×3 matrix `M_q` and use the polar decomposition `M_q = U_L_q H_q U_R_q^†`.
   Then `V_CKM = U_L_up^† U_L_dn` and `U_L_q` need not equal the
   eigenbasis of `H_q† H_q` if `M_q` has off-diagonal SVD structure.
3. **Off-cyclic flavor group.** Promote the flavor group from `Z_3` to
   a larger group (`S_3`, `A_4`, etc.) whose irreps mix the three
   generations in a non-circulant way.
4. **Generation-isospin coupling.** Treat the flavor index as joint
   `(g, T_3)` rather than per-sector `g`. This is the spirit of the
   `MOMENTUM_CHARGE_COMMUTE_THEOREM_NOTE_2026-05-02` and would require
   re-deriving the per-sector mass spectrum.

None of these directions is claimed or pursued here. The present note
only closes the negative direction for P-Heavy-A on the shared-C_3[111]
substrate.
