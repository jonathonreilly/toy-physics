# Lane 5 `(C1)` Cl_4(C)-Conditional Derivation Chain Construction Note

**Date:** 2026-04-30
**Status (actual current surface):** support / explicit-construction note on
`main` for the conditional `(G1) → (C1)` chain. Conditional on adopting
**Axiom\*** (the irreducible Cl_4(C) module on `P_A H_cell`); does **NOT**
adopt Axiom\* and does **NOT** retire `(G1)`/`(C1)` on the current `A_min`
surface. Bare `retained` / `promoted` is NOT used.
**Runner:** `scripts/frontier_hubble_lane5_c1_cl4c_conditional_derivation_chain_construction.py`
**Lane:** 5 — Hubble constant derivation, `(C1)` absolute-scale gate.

**Cited authorities (one-hop deps):**
- [AXIOM_STACK_MINIMALITY_CL4C_NO_GO_THEOREM_NOTE_2026-04-29.md](AXIOM_STACK_MINIMALITY_CL4C_NO_GO_THEOREM_NOTE_2026-04-29.md)
  — V1 minimality no-go: Cl_4(C) on `P_A H_cell` is non-derivable from
  `A_min`; Axiom\* is the unique minimal extension that closes `(G1)`.
- [HUBBLE_LANE5_C1_A6_BILINEAR_ACTIVE_BLOCK_SUPPORT_BOUNDARY_NOTE_2026-04-29.md](HUBBLE_LANE5_C1_A6_BILINEAR_ACTIVE_BLOCK_SUPPORT_BOUNDARY_NOTE_2026-04-29.md)
  — A6 bilinear support: number-preserving bilinears on `P_A H_cell` realize
  `M_4(C)` as a host algebra (existence, not selection).
- [HUBBLE_LANE5_C1_A2_ACTION_UNIT_METROLOGY_OBSTRUCTION_NOTE_2026-04-29.md](HUBBLE_LANE5_C1_A2_ACTION_UNIT_METROLOGY_OBSTRUCTION_NOTE_2026-04-29.md)
  — A2 metrology obstruction: dimensionless lattice inputs do not pin κ.
- [HUBBLE_LANE5_C1_CARRIER_METROLOGY_AXIOM_AUDIT_NOTE_2026-04-29.md](HUBBLE_LANE5_C1_CARRIER_METROLOGY_AXIOM_AUDIT_NOTE_2026-04-29.md)
  — Carrier/metrology axiom audit: minimal premise statement.
- [PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md](PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md)
  — Conditional Clifford phase bridge that this construction discharges in
  the Axiom\* extension.
- [PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md)
  — Source-unit normalization theorem providing `λ = 1`, `G_Newton,lat = 1`,
  `a/l_P = 1`.
- [HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md](HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md)
  — Two-gate dependency firewall: numerical `H_0` requires `(C1) ∧ ((C2) ∨ (C3))`.
- [CL4C_CARRIER_AXIOM_CONSEQUENCE_MAP_NOTE_2026-04-28.md](CL4C_CARRIER_AXIOM_CONSEQUENCE_MAP_NOTE_2026-04-28.md)
  — Cross-lane consequence map under Axiom\*.

---

## 0. Headline

V1 closes the question of whether Cl_4(C) is derivable from `A_min`:
**no.** Adopting Axiom\* — the irreducible Cl_4(C) module on `P_A H_cell` —
is the unique minimal extension that opens the `(G1)/(C1)` lane. That
adoption is a science-level decision and is **not** taken here.

This note assumes the user's hypothetical: *what if Axiom\* is adopted?*
It then constructs the four-arrow derivation chain explicitly:

```text
Axiom*  ⟹  metric-compatible primitive Clifford/CAR coframe response on P_A H_cell
        ⟹  (G1) closure
        ⟹  (C1) absolute-scale gate (a/l_P = 1, a^{-1} = M_Pl in natural units)
        ⟹  H_0  [BLOCKED — needs independent (C2) or (C3)].
```

The construction is **face-equivariant**, not face-unique: spatial Z³
isotropy + time-locking pin the Cl_4 module up to an active U(1)³ × S₃
gauge orbit. All Lane-5 structural invariants (`c_Widom = c_cell = 1/4`,
`λ = 1`, `G_Newton,lat = 1`, `a/l_P = 1`) are gauge-invariant on the orbit;
the face-unique selection is therefore not load-bearing for `(C1)`.

The construction reaches `(C1)` cleanly. It does **not** reach `H_0`: the
`(C2)` eta-retirement gate is structurally orthogonal to Axiom\* and is not
discharged by Cl_4(C) presence. Numerical `H_0` retention requires
Axiom\* **and** an independent `(C2)` (or `(C3)`) closure — exactly as the
two-gate dependency firewall already records.

---

## 1. Setup and conditional premise

Time-locked primitive event cell:

```text
H_cell ≅ C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z ≅ C^16,
P_A = P_{|S|=1},  rank(P_A) = 4,  c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4.
```

Hamming-weight-1 basis on `P_A H_cell`:

```text
|t⟩ = |1000⟩,  |x⟩ = |0100⟩,  |y⟩ = |0010⟩,  |z⟩ = |0001⟩.
```

**Conditional premise (Axiom\*).** `End(P_A H_cell)` carries an irreducible
Cl_4(C) module action: there exist four Hermitian operators
`Γ_1, …, Γ_4` on `K = P_A H_cell` with

```text
{Γ_a, Γ_b} = 2 δ_ab I_K.
```

Per V1, this is **not** derivable from `A_min`. It is a separate carrier
axiom. This note proceeds *as if* it has been adopted, and traces the
chain.

No measured value of `G`, `ℏ`, `M_Pl`, `H_0`, or any cosmological
observable enters this construction.

---

## 2. Arrow 1 — Cl_4(C) ⟹ metric-compatible coframe response on `P_A H_cell`

### 2.1 Explicit Pauli construction

Identify `K ≅ C^2 ⊗ C^2` via the 2⊗2 split labeled `(face-pair, tangent-pair)`:

```text
|t⟩ ↔ |0⟩ ⊗ |0⟩,  |n⟩ ↔ |1⟩ ⊗ |0⟩,  |τ_1⟩ ↔ |0⟩ ⊗ |1⟩,  |τ_2⟩ ↔ |1⟩ ⊗ |1⟩.
```

Define four Hermitian generators by Pauli matrices:

```text
Γ_t   = σ_x ⊗ I,
Γ_n   = σ_y ⊗ I,
Γ_τ1  = σ_z ⊗ σ_x,
Γ_τ2  = σ_z ⊗ σ_y.
```

These satisfy `{Γ_a, Γ_b} = 2 δ_ab I_K` mechanically (Pauli identities;
verified by the runner).

### 2.2 Linear extension to a coframe response

Extend linearly to `D : E_C → End(K)` by

```text
D(α t + β n + γ τ_1 + δ τ_2) = α Γ_t + β Γ_n + γ Γ_τ1 + δ Γ_τ2.
```

Polarization gives, for any orthonormal coframe vector `v`,

```text
D(v)^2 = ‖v‖^2 I_K
```

(verified by the runner on a sweep of test vectors).

### 2.3 Spatial-isotropy gauge equivalence

The "selected oriented face" with normal `n ∈ {x, y, z}` is one of three
choices. Spatial Z³ isotropy of `A_min` is a symmetry of the construction:
for any rotation `R ∈ S₃ ⊂ SO(3)` permuting `(x, y, z)`, there exists a
unitary `U_R` on `K` such that the rotated face's Cl_4 generators are
`U_R Γ_a U_R^†`. The active basis additionally admits a continuous
`U(1)^3` phase rescaling on `(|x⟩, |y⟩, |z⟩)` that conjugates the Cl_4
presentation without changing its algebra (per A6 witnesses 6–7).

The face is therefore a **coset representative**, not a derivation residue.
Structural invariants of the Cl_4 module — irreducibility, the
anticommutator algebra, oriented Majorana → CAR pairings — are
gauge-invariant on the `U(1)^3 × S_3` orbit.

### 2.4 Two-mode CAR pairing

For a chosen face, define oriented pairs

```text
c_N = (Γ_t + i Γ_n) / 2,    c_T = (Γ_τ1 + i Γ_τ2) / 2.
```

These satisfy the two-mode CAR relations

```text
{c_i, c_j} = 0,    {c_i, c_j^†} = δ_ij I_K,
```

so `K ≅ F(C^2)`. This is the equivalence (a) ⇔ (b) of the A5 audit. The
pairing labels depend on the face; the algebra does not.

---

## 3. Arrow 2 — coframe response ⟹ `(G1)` closure (in natural phase units)

`(G1)` *is* the metric-compatible primitive Clifford/CAR coframe response
on `P_A H_cell`. Arrow 1's construction produces it explicitly.

**Native phase unit.** Bivectors `Γ_a Γ_b` (`a ≠ b`) generate the local
spin lift. A `2π` vector rotation acts on the spinor module `K` as the
central element `−I_K`; a `4π` rotation returns to `I_K`. The native
phase periodicity is therefore `4π` (verified by the runner via direct
exponentiation of `Γ_t Γ_n / 2`).

**Boundary against A2.** The dimensional action quantum `κ` is **not**
fixed by Arrow 2. The `(S_dim, κ) → (λ S_dim, λ κ)` rescaling leaves all
Hilbert phases invariant ([HUBBLE_LANE5_C1_A2_ACTION_UNIT_METROLOGY_OBSTRUCTION_NOTE_2026-04-29.md](HUBBLE_LANE5_C1_A2_ACTION_UNIT_METROLOGY_OBSTRUCTION_NOTE_2026-04-29.md)).
Arrow 2 therefore closes `(G1)` in **natural phase units only**, leaving
the SI metrology of `ℏ` undetermined. This is exactly the boundary in
the conditional Clifford phase bridge theorem.

---

## 4. Arrow 3 — `(G1)` ⟹ `(C1)` absolute-scale gate (in natural lattice units)

In natural lattice units (`a = 1`, native phase unit `4π`):

1. **Widom-Gioev-Klich coefficient.** The two CAR modes are a normal
   crossing mode (two cut-normal Fermi crossings) and a tangent response
   mode (one half-zone Fermi crossing). The all-tangent half-period
   involution on the primitive transverse Laplacian gives
   `⟨N_x⟩ = 2 + 2·(1/2) = 3`. Hence

   ```text
   c_Widom = ⟨N_x⟩ / 12 = 3/12 = 1/4.
   ```

2. **Carrier-trace match.** This equals the Planck primitive trace on the
   same active block:

   ```text
   c_Widom = c_cell = 1/4.
   ```

3. **Source-unit normalization.** Per
   [PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md),
   `c_cell = λ/4 = 1/4 ⟹ λ = 1`. The physical Newton coefficient is

   ```text
   G_Newton,lat = (4π) G_kernel = 4π · 1/(4π) = 1.
   ```

4. **Planck-length identity.** With `G_Newton,lat = 1`, `ℏ = 1`, `c = 1`
   in lattice-natural units,

   ```text
   l_P = √(ℏ G c^{-3}) = 1,    a / l_P = 1,    a^{-1} = M_Pl.
   ```

The runner verifies items 2–4 numerically.

`(C1)` closes as a **structural numerical identity in natural units**,
gauge-equivariantly. SI decimal of `ℏ` or `M_Pl` is metrology, not
derivation, and remains separate.

---

## 5. Arrow 4 — `(C1)` ⟹ `H_0` [BLOCKED]

From `(C1)` plus the retained admitted `Λ ≈ 1.1 × 10^{-52} m^{-2}`:

```text
R_Λ = √(3/Λ)         (numerically retainable, modulo admitted Λ),
H_inf = c / R_Λ      (closed in the Axiom* extension).
```

But

```text
H_0 = H_inf / √L,    L := Ω_Λ,0 = (H_inf / H_0)^2.
```

`(C1)` closes the absolute scale `H_inf` without closing `L`. Per the
two-gate dependency firewall ([HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md](HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md)),
numerical `H_0` requires `(C1) ∧ ((C2) ∨ (C3))`.

`(C2)` is the eta-retirement gate on the right-sensitive 2-real Z₃
doublet-block point-selection law for `dW_e^H = Schur_{E_e}(D_-)`. This
lives on the Yukawa / Wilson-to-`dW_e^H` lane, not on the boundary
primitive carrier `P_A H_cell`. Axiom\* operates on `P_A H_cell`
edge-statistics; it does **not** touch the Yukawa-side Schur point
selection.

`(C3)` (direct cosmic-`L` derivation) currently has no active route per
[HUBBLE_LANE5_C3_VACUUM_TOPOLOGY_NO_ACTIVE_ROUTE_NOTE_2026-04-27.md](HUBBLE_LANE5_C3_VACUUM_TOPOLOGY_NO_ACTIVE_ROUTE_NOTE_2026-04-27.md).

**Honest verdict.** Cl_4(C) presence on `P_A H_cell` ⟹ `(C1)` does **not**
yield `H_0`. The chain reaches `H_inf` but stalls at the structurally
orthogonal `(C2)` residual. This is *not* a defect of the Cl_4
construction; it is the cosmic-history-ratio necessity already isolated
on the surface.

---

## 6. Chain summary table

| Arrow | Status under "Axiom\* adopted" | Residual import |
|---|---|---|
| 1: Cl_4(C) → metric-compatible coframe `D` | **constructible, face-equivariant** (gauge: `U(1)^3 × S_3`) | face-unique selection (not load-bearing) |
| 2: coframe `D` → (G1) | **closed in natural phase units** | A2: dimensional `κ` SI metrology |
| 3: (G1) → (C1) absolute-scale | **closed** as `c_Widom = c_cell = 1/4`, `λ = 1`, `G_Newton,lat = 1`, `a/l_P = 1` | SI `ℏ` / `M_Pl` decimal (metrology) |
| 4: (C1) → `H_0` | **blocked** — reaches `H_inf` only | `(C2)` eta-retirement gate (or `(C3)`); structurally orthogonal |

---

## 7. What this note closes

1. An **explicit Pauli construction** of `D : E_C → End(K)` realizing the
   metric-compatible coframe response on `P_A H_cell`, conditional on
   Axiom\*.
2. A face-equivariance witness: spatial-rotation gauge + active-basis
   phase gauge leave the structural invariants `{c_Widom, c_cell, λ,
   G_Newton,lat, a/l_P}` invariant.
3. Source-unit normalization step verifying `λ = 1`, `G_Newton,lat = 1`,
   `a/l_P = 1` on the construction.
4. An explicit `(C2)`-orthogonality witness: the Cl_4 module on
   `P_A H_cell` is silent on `dW_e^H = Schur_{E_e}(D_-)` point selection,
   confirming the Yukawa-side residual is not discharged.

## 8. What this note does NOT close

1. **Adoption of Axiom\*.** Per V1 corollary, this is a science-level
   decision; the note is conditional only.
2. **`(G1)` and `(C1)` in current `A_min`.** They remain open, exactly as
   V1 records.
3. **Numerical `H_0`.** Blocked by `(C2)` independently of any Axiom\*
   decision.
4. **SI decimal of `ℏ` or `M_Pl`.** Remains metrology.
5. **Face-unique Cl_4 selection.** Remains a gauge — not load-bearing
   for any Lane-5 structural invariant.

---

## 9. Status firewall fields

```yaml
actual_current_surface_status: support
conditional_surface_status: closed_in_axiom_star_extension_for_arrows_1_3
hypothetical_axiom_status: axiom_star_assumed_not_adopted
admitted_observation_status: null
proposal_allowed: true
proposal_allowed_reason: |
  Walks the conditional consequence chain of the V1 minimality no-go's
  option (i) without adopting Axiom*. Pure construction; no observed
  value enters; no theorem is promoted on the actual current surface.
audit_required_before_effective_retained: false
bare_retained_allowed: false
g1_lane_status_under_axiom_star: closed_face_equivariantly
c1_lane_status_under_axiom_star: closed_in_natural_lattice_units
h0_lane_status_under_axiom_star: blocked_by_C2_orthogonal_residual
```

---

## 10. Verification

```bash
python3 scripts/frontier_hubble_lane5_c1_cl4c_conditional_derivation_chain_construction.py
```

The runner mechanically checks the four arrows:

**Arrow 1 (8 checks):**
1. `rank(P_A) = 4`, `c_cell = 1/4`.
2. Pauli generators `Γ_t, Γ_n, Γ_τ1, Γ_τ2` are Hermitian and unitary.
3. Cl_4 anticommutator `{Γ_a, Γ_b} = 2 δ_ab I_K` exact.
4. Linear coframe response `D(v)^2 = ‖v‖^2 I` on a sweep of test vectors.
5. Face-rotation gauge: a face permutation `(x↔y)` lifts to a unitary
   that conjugates Cl_4 into a unitarily-equivalent presentation.
6. Active-basis phase gauge: `U(1)^3` rescaling of `(|x⟩, |y⟩, |z⟩)`
   conjugates Cl_4 without changing the algebra.
7. CAR pairing: `c_N, c_T` satisfy two-mode CAR relations.
8. `K ≅ F(C^2)`: the four basis vectors of `K` are `|0_N 0_T⟩`,
   `|1_N 0_T⟩`, `|0_N 1_T⟩`, `|1_N 1_T⟩` of the two-mode Fock space.

**Arrow 2 (3 checks):**
9. Spin-lift periodicity: `exp(π Γ_t Γ_n) = −I_K`,
   `exp(2π Γ_t Γ_n) = +I_K`.
10. Action-unit invariance witness (A2 boundary): `(S, κ) → (λ S, λ κ)`
    leaves `exp(i S/κ)` invariant for sweep `λ ∈ {0.5, 1.0, 2.0, 8.0}`.
11. Native phase unit `4π` recovered from full vector rotation.

**Arrow 3 (4 checks):**
12. `c_Widom = ⟨N_x⟩ / 12 = 3/12 = 1/4` from `⟨N_x⟩ = 3`.
13. `c_Widom = c_cell = 1/4`.
14. `λ = 4 c_cell = 1`, `G_Newton,lat = 4π · 1/(4π) = 1`.
15. `a / l_P = 1` in lattice-natural units.

**Arrow 4 (3 checks — orthogonality witness):**
16. The Cl_4 generators `Γ_a` commute with a model `Z_3` doublet-block
    point-selection projector on a 2-real subspace (no overlap).
17. The carrier `K = P_A H_cell` and the Yukawa-side `dW_e^H` algebra act
    on disjoint factors of the framework Hilbert package.
18. Therefore: Cl_4(C) on `P_A H_cell` does not affect the
    `Schur_{E_e}(D_-)` point selection — `(C2)` residual confirmed
    structurally orthogonal.

**Section: forbidden-import guard (6 checks).** The runner checks that no
observed value of `H_0`, `H_inf`, `Λ`, `M_Pl`, `ℏ`, `G` enters as a proof
input.

Expected: `PASS = 24, FAIL = 0`.

---

## 11. Honest residual

After this note lands as `support`:

- `(G1)`/`(C1)` still **open** in current `A_min` posture (V1 governs).
- Adoption of Axiom\* still a **science-level decision** for the user
  (V1 corollary governs).
- Numerical `H_0` still **blocked** by the structurally orthogonal
  `(C2)` residual, regardless of any Axiom\* decision.
- The construction here makes the `Axiom\* ⟹ (C1)` arrow concrete: it
  is no longer a sentence ("the Clifford phase bridge would close"); it
  is an explicit Pauli realization with verified anticommutators, gauge
  equivariance, and source-unit normalization.

What this note adds to the surface: **a concrete realization** of the
conditional Axiom\* consequence chain that the existing
[CL4C_CARRIER_AXIOM_CONSEQUENCE_MAP_NOTE_2026-04-28.md](CL4C_CARRIER_AXIOM_CONSEQUENCE_MAP_NOTE_2026-04-28.md)
lists abstractly, with the `(C2)` orthogonality residual confirmed in
the same construction.
