# Cl(3) Color Structure Theorem: SU(3)_c on the Symmetric Base + R_conn Derivation

**Date:** 2026-04-19 (originally); 2026-05-04 (audited_renaming scope-narrow)
**Status:** algebraic SU(3) embedding + Fierz channel-count theorem on the 3D symmetric base subspace of the taste cube. **The identification of this 3D base with physical SM color is a separate retained-bridge requirement, not part of this theorem's load-bearing scope.**
**Claim boundary authority:** this note
**Script:** `scripts/verify_cl3_sm_embedding.py` (sections H, I)

---

## Audit-driven scope narrowing (2026-05-04)

The 2026-05-04 audit verdict was `audited_renaming`: the algebraic checks are
ratified, but the load-bearing identification of the **3D symmetric base
subspace** with **physical SM color SU(3)_c** requires a separate retained
bridge theorem that this note does not provide. The narrowed scope below
keeps the verified algebraic content and explicitly defers the physical
identification.

The renaming criterion (from the audit): *"Re-audit after the claim is
narrowed to the algebraic embedding/channel-count result or after a retained
bridge derives physical color and R_conn from the selected symmetric-base
carrier."* This note now adopts the first option.

## Statement (scope-narrowed)

**Theorem (algebraic, scope-narrowed).** On the Z³ spatial lattice the
following are exact algebraic facts about the tensor-product carrier
`{0,1}² ⊗ {0,1}` and the 3D symmetric base subspace inside it:

1. The spatial dimension of `Z³` is 3, so the hw=1 orbit on the taste cube
   has size 3. We adopt the convention `N_c := dim(Z³) = 3` for the
   algebraic counting below. (The physical identification of `N_c` with the
   SM color count is the bridge requirement deferred below.)

2. SU(3) acts on the 3-dimensional symmetric base subspace of
   `{0,1}² ⊗ {0,1}` (the (b₁,b₂)-base ⊗ b₃-fiber decomposition), embedded as
   `M₃_sym ⊗ I₂` in the 8D taste space. This is an embedding theorem on the
   chosen carrier; reading this SU(3) as physical SM color requires a
   separate bridge (see "Physical-identification bridge" below).

3. `T_F = 1/2` (trace normalization), `dim(adjoint) = N_c² - 1 = 8`.

4. The embedded SU(3) commutes with the embedded SU(2)_weak and the
   embedded U(1)_Y on the same carrier: `[SU(3), SU(2)_weak] = 0` and
   `[SU(3), Y] = 0` by tensor product structure.

5. The Fierz identity for SU(3) gives:
   `∑_a T^a_{ij} T^a_{kl} = (1/2)δᵢₗδₖⱼ − (1/2N_c)δᵢⱼδₖₗ`

6. From the Fierz identity, the algebraic channel-count ratio on
   `End(ℂ^{N_c})` is:
   `R_conn = (N_c² − 1)/N_c² = 8/9`
   This is an **exact channel-count fraction on the 3D symmetric base
   carrier**. Reading it as a physical EW-color coupling factor requires
   the bridge below; the EW alpha-level factor is tracked as
   `K_EW(kappa_EW)=1/(8/9+kappa_EW/9)` with `sqrt(9/8)` the
   connected-trace specialization `kappa_EW=0`, not an unconditional
   consequence of this algebra alone.

## Physical-identification bridge (deferred to a separate theorem)

This note **does not derive** the identification

> "the 3D symmetric base subspace inside the taste cube **is** the physical
> SM color carrier SU(3)_c."

That identification is the load-bearing bridge gap flagged by the
2026-05-04 audit. To clean this lane, a separate retained theorem must
either:

- Derive the bridge from accepted upstream inputs (e.g., a representation
  match between the Z³ axis-selector orbit and the physical SU(3)_c rep
  carried by SM quark fields), or
- Cite an existing retained authority that supplies the bridge.

Until that bridge is on the retained surface, the corollary "`R_conn = 8/9`
is the physical color-trace ratio" must be read as **conditional on the
bridge**, not as a direct consequence of this note's algebra.

The bridge is currently flagged as a discrete retained-elsewhere
dependency; the closure path is documented in
`NATIVE_GAUGE_CLOSURE_NOTE.md` (graph-first axis selector) and in the
representation-match work on the residual axis swap.

---

## Proof

### A. N_c = 3 from Z³

The spatial substrate is Z³ with 3 independent coordinate axes. Staggered-fermion
doubling maps each axis to one taste direction. The Hamming-weight-1 sector has
exactly 3 states: `{e₁=(1,0,0), e₂=(0,1,0), e₃=(0,0,1)}`, one per spatial axis.

`N_c = |hw=1 states| = dim(Z³) = 3`

This is not an input; it is the algebraic image of the spatial dimension.

### B. SU(3)_c on Symmetric Base

The 8D taste space decomposes as `ℂ⁴_base ⊗ ℂ²_fiber` where:
- **base**: `{(b₁,b₂) ∈ {0,1}²}` = 4D space with basis `{|00⟩, |01⟩, |10⟩, |11⟩}`
- **fiber**: `{b₃ ∈ {0,1}}` = 2D weak-doublet space

The base further decomposes under b₁↔b₂ reflection:
- **symmetric subspace** (3D): `{|00⟩, |01⟩+|10⟩, |11⟩}` — carries color
- **antisymmetric subspace** (1D): `{|01⟩−|10⟩}` — lepton singlet

The unitary `U_base` mapping `{|00⟩,|01⟩,|10⟩,|11⟩}` to
`{|sym₁⟩,|sym₂⟩,|sym₃⟩,|antisym⟩}` block-diagonalizes the base.

The 8 Gell-Mann generators `T^a` (Hermitian, `Tr[T^a T^b] = (1/2)δ^{ab}`) are
embedded as:

```
T^a_{8D} = (U_base† · diag(T^a, 0₁) · U_base) ⊗ I₂
```

where `diag(T^a, 0₁)` is T^a acting on the 3D symmetric block, extended by 0 on
the antisymmetric 1D block.

### C. Gauge Group Commutativity

By the tensor product structure:
- `T^a_{8D} = M_base ⊗ I_fiber` acts on the base only
- `Jf_i = I_base ⊗ σᵢ/2` acts on the fiber only
- Operators on different tensor factors commute: `[A⊗I, I⊗B] = 0` for any A, B.
  Explicitly: `(M_base⊗I_fiber)(I_base⊗(σᵢ/2)) = M_base⊗(σᵢ/2) = (I_base⊗(σᵢ/2))(M_base⊗I_fiber)`.
- Therefore `[T^a_{8D}, Jf_i] = 0`.

`Y = P_symm · (1/3) + P_antisymm · (−1)` also acts on the base symmetry sectors,
so `[T^a_{8D}, Y] = 0` by the same structure.

The Standard Model gauge group structure `SU(3)_c × SU(2)_L × U(1)_Y` emerges
algebraically from the tensor product decomposition of the taste cube.

### D. R_conn from the SU(N_c) Algebra

The Fierz completeness relation for SU(N_c) with `T_F = 1/2` (summing over the
`N_c²-1` traceless generators):

```
∑_{a=1}^{N_c²-1} (T^a)_{ij} (T^a)_{kl} = (1/2)δᵢₗδₖⱼ − (1/(2N_c))δᵢⱼδₖₗ
```

Including the identity channel `T^0 = I/√N_c` with weight `(1/(2N_c))δᵢⱼδₖₗ`,
the full completeness relation on `End(ℂ^{N_c})` is:

```
singlet channel:  weight = 1/N_c²  of the N_c²-dimensional matrix algebra
adjoint channel:  weight = (N_c²−1)/N_c²
```

`R_conn` is the fraction of a quark bilinear propagated by the adjoint (non-singlet,
color-connected) channel:

```
R_conn = (N_c²−1)/N_c²  [leading order in 1/N_c]
```

For `N_c = 3`: `R_conn = 8/9`. Subleading topology corrections are
`O(1/N_c^4) ~ 1.2%` at `N_c=3` (bounded in `RCONN_DERIVED_NOTE.md`).

**EW-color coefficient boundary:**

The Ward-identity derivation of `y_t = g_bare/√(2N_c)` produces a ratio of EW
and color traces. The SU(N_c) algebra fixes the channel fraction, but the EW
normalization lane now carries the explicit coefficient
`K_EW(kappa_EW)=1/(8/9+kappa_EW/9)`. The coupling factor `sqrt(9/8)` is the
connected-trace specialization `kappa_EW=0`, not a consequence of this
algebraic support note by itself.

---

## Numerical Verification

| Check | Result |
|-------|--------|
| `Tr[T^a T^b] = (1/2)δ^{ab}` (T_F = 1/2) | exact |
| Jacobi identity `[[T^a,T^b],T^c] + cyc = 0` | max err < 10⁻¹⁵ |
| `[T^a,T^b] = i f^{abc} T^c` in 8D | max err < 10⁻¹⁶ |
| `[SU(3)_c, SU(2)_weak] = 0` | max err < 10⁻¹⁶ |
| `[SU(3)_c, Y] = 0` | max err < 10⁻¹⁷ |
| `N_c = 3`, adjoint dim = 8 | exact |
| Fierz identity | max err < 10⁻¹⁶ |
| `F_adj = 8/9` | exact Fierz/channel-count fraction |
| `K_EW(0)=9/8` | conditional connected-trace specialization |

---

## Relation to Existing Framework Results

### NATIVE_GAUGE_CLOSURE_NOTE.md

This theorem provides the algebraic underpinning for the SU(3)_c structure already
retained there. The graph-first chain:
- Z₃ axis selector → selected axis defines fiber/base split
- Residual axis swap → 3⊕1 split of base
- Commutant = gl(3)⊕gl(1) → compact semisimple = su(3)

is now grounded in the explicit Gell-Mann embedding verified here.

### YT_EW_COLOR_PROJECTION_THEOREM.md

The exact `8/9` channel fraction used there is confirmed here via the SU(3)
Fierz identity. The EW physical readout coefficient is separately bounded by
`EW_CURRENT_MATCHING_RULE_OPEN_GATE_NOTE_2026-05-03.md`.

### RCONN_DERIVED_NOTE.md

`R_conn = 8/9 = (N_c²−1)/N_c²` is confirmed as following from SU(3) structure
constants alone, with `N_c = 3` forced by the spatial dimension of Z³.

---

## What This Theorem Sharpens

- **R_conn = 8/9 blocker**: algebraic origin — adjoint fraction of SU(N_c) matrix algebra;
  leading-order value exact, O(1/N_c^4) corrections bounded in `RCONN_DERIVED_NOTE.md`
- **EW-color correction**: reduced to `K_EW(kappa_EW)`; the `sqrt(9/8)`
  coupling factor is only the `kappa_EW=0` specialization
- **[SU(3), SU(2)] = 0**: exact from tensor product structure of taste cube
- **N_c = 3 forced**: from dim(Z³) = 3 spatial axes

## What Remains Bounded

- The connection between the abstract taste-cube SU(3) and the continuum color
  gauge field requires the lattice-to-continuum matching prescription
- The running of `α_s` from lattice scale to M_Z inherits the bridge budget from
  `ALPHA_S_DERIVED_NOTE.md`

## Reading Rule

This note is the claim boundary for this reviewed color-structure support packet.
It sharpens the existing color / EW support stack on current `main`, but it does
not by itself upgrade the accepted minimal-input surface.
