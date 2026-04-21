# PMNS Angle-Triple Selector Attack Backlog

**Branch:** `afternoon-4-21`
**Gate:** the DM A-BCC / PMNS angle-triple gate. The physical pinned point
`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` is known on the
2-real source manifold `(δ, q_+)` (see
`PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17`).
What is missing: a **framework-native point-selection law** that picks
the physical point uniquely (beyond the positive-sheet law, which is
closed, and beyond the Z_3 center law, which leaves a family rather
than a unique point).

This backlog tracks the attack candidates for the loop on
`afternoon-4-21`.

---

## Iter log

| Iter | Attack | Status | Note |
|------|--------|--------|------|
| 1 | Doublet-block AM-GM on (E_sym, E_anti) | **negative** | `PMNS_SELECTOR_ITER1_DOUBLET_AMGM_NEGATIVE_NOTE_2026-04-21.md` |
| 2 | `W[J] = log|det H|` under scalar Casimir constraints {‖J‖_F², Tr(H²), Tr(H), Tr(H³)} | **negative** | `PMNS_SELECTOR_ITER2_WDET_CONSTRAINED_NEGATIVE_NOTE_2026-04-21.md` — best alignment at cos(θ)=0.69 with Tr(H²), still 46° off |
| 3 | Brannen-phase gate: 12 phase invariants vs retained I2/P values {2/9 rad, 2π/9, π−2/9, …} | **weak hint / negative at 1e-4** | `PMNS_SELECTOR_ITER3_BRANNEN_PHASE_WEAK_HINT_NOTE_2026-04-21.md` — best match \|dev\|=0.025 rad (1.4°), two clusters; chamber-blind `Im(a_*+b_*) = γ = 1/2` exactly |
| 4 | Operator-commutation + scalar-invariant scan (33 scalars × retained simple values) | **mixed — strong hint on `δ · q_+ ≈ 2/3 = Q`** (0.15% dev) | `PMNS_SELECTOR_ITER4_OPERATOR_COMMUTATION_MIXED_NOTE_2026-04-21.md` — operator-commutation class ruled out; scalar scan finds `δ·q_+ = 2/3` and `Σλ/Σ\|λ\| = 1/6` both at 0.001 deviation — likely iter-5 candidates |
| 5 | Precision-sharpen test of `δ · q_+ = Q = 2/3` hypothesis | **strong intermediate** | `PMNS_SELECTOR_ITER5_DELTA_QPLUS_EQ_Q_HYPOTHESIS_NOTE_2026-04-21.md` — at machine precision `\|dev\| = 1.04e-3` (NOT exact), BUT re-pin under exact constraint gives `sin²θ_23 = 0.5447` within 0.06% of PDG central 0.545 — inside 1σ NuFit NO. A genuine codim-1 cut compatible with all PMNS data. |
| 6 | Combined-cuts scan: walk `{δ·q_+ = 2/3, s13²=0.0218}` curve, find second retained cut | **second cut found: `det(H) = E2 = √8/3`** | `PMNS_SELECTOR_ITER6_SECOND_CUT_DET_H_EQ_E2_NOTE_2026-04-21.md` — two retained identities + s13² input gives PMNS within 1σ on s12² and essentially central on s23². E2 is a retained atlas constant. |
| 7 | Symbolic sympy expansion of det(H); derivation attempt of det(H)=E2 | **informative partial** | `PMNS_SELECTOR_ITER7_SYMBOLIC_DET_H_DERIVATION_NOTE_2026-04-21.md` — closure eq is irreducible cubic in m with ℤ[√2,√3,√6] coeffs; IS the retained content at polynomial level; no THIRD simple-value identity at closure point. |

---

## Candidate attacks (iter 2+)

Each candidate has a concrete executable form — not a vague direction.

### A2. Observable-principle functional with scale-fixing constraint

**Functional.** `W[J] = log |det(H_base + J)|`, where `J = m·T_m + δ·T_Δ + q_+·T_q`.
On the chamber `det(H_base + J) > 0`, `W[J]` is smooth and real. Without
a scale constraint `W[J]` diverges as `‖J‖ → ∞`, so we pair it with a
retained Frobenius constraint.

**Constraint candidates.**
- `‖J‖_F² = ‖J_*‖_F²` (fix perturbation scale to the pinned value)
- `Tr(H²) = Tr(H_base²) + c` for framework `c`
- `det(H) = det(H_base)` (determinant-preserving slice)

**Test.** Compute critical points of `W[J]` under each constraint.
If any coincide with the pinned point, the selector is `W[J]` under that
constraint, and the constraint itself becomes the retained input.

### A3. Koide-like AM-GM on eigenvalues of H

**Functional.** Let `λ_1 ≥ λ_2 ≥ λ_3` be the eigenvalues of
`H(m, δ, q_+)`. Define a "Koide-Q-like" functional
`Q_H(m, δ, q_+) = (Σ λ_i) / (Σ |λ_i|^½)²`
or, under `σ_hier = (2, 1, 0)` already retained, work with ordered
pairs. Test whether the pinned point is a critical point of a
Koide-cone-like functional on the `H`-spectrum.

**Rationale.** The framework has I1 Koide closure at Q = 2/3. Maybe the
PMNS selector is an ANALOGOUS Koide-style functional on the chamber
`H`-eigenvalues, with a fixed-Frobenius constraint.

### A4. Brannen-phase gate on H

**Functional.** Let `G = H^2` (or `H · H^†`, same for Hermitian). The
Brannen phase `δ_B` of `H` is given by the APS η-invariant of some
associated Z_3 orbifold construction. If `H(m, δ, q_+)` has a
well-defined Brannen phase `δ_B(m, δ, q_+)`, test whether requiring
`δ_B = 2/9` (the retained I2/P value) forces the pinned point.

**Test.** Compute `δ_B` at a grid of chamber points; check whether the
level set `δ_B = 2/9` intersects the pinned point.

### A5. A-BCC axiomatic derivation (structural closure)

**Goal.** Derive A-BCC (baseline-connected-component) from
`Cl(3)` on `Z³` rather than importing it observationally from T2K.

**Approach.** The A-BCC condition is currently `sign(det H) > 0`. This
is equivalent to a no-go theorem on the caustic. If we can show the
retained `Z_3` action on the Cl(3) support lattice forces
`sign(det H_physical) > 0` via a retained index-theoretic invariant
(e.g., spectral flow through the caustic is odd and wraps to the same
sheet), we'd have A-BCC retained rather than imposed.

**Connection to iter 1.** If A-BCC is retained, then the admissible
basin is unique (only Basin 1 at `σ_hier = (2, 1, 0)`), and the
doublet-block family collapses. Combined with any functional (possibly
even the iter 1 F_d with constraint), this MIGHT pin the point.

### A6. C_3 center-lift to a non-abelian sub-gate

**Rationale.** User flagged "tested Z_3 center law is too weak".
Replace or augment `Z_3` with `S_3 = Z_3 ⋊ Z_2` (adding the parity
swap) or with a non-abelian sub-lift that distinguishes the
chamber's two sheets differently.

**Test.** Identify the `S_3` action on the affine chart. Compute
`S_3`-invariant observables (beyond the frozen `K_01, K_02`). Check
whether an additional `S_3`-invariant fixes the 2-real family to a
unique point.

### A7. Wilson-line cyclic-bundle observable

**Functional.** The observable principle `W[J]` applied on the full
retained cyclic bundle `{I, C + C², i(C − C²)}` — not just `log|det|`
of `H` but the more specific cyclic-bundle version. Specific form:

```
W_cyclic[J] = Σ_{B ∈ bundle} log |det(H_base + B · J)|
```

**Test.** Check critical points on the chamber.

### A8. A-BCC × I2/P cross-sector pin

**Hypothesis.** The user's headline explicitly names "DM A-BCC / PMNS
angle-triple gate". The attack: identify the retained Cl(3) operator
that ties the DM A-BCC observable `sign(det H) > 0` to the PMNS
`δ_*, q_+*` specifically — a cross-sector coupling that forces a
unique point on the doublet manifold.

**Concrete candidate.** The retained `Y_l = U_e · diag(m_e, m_μ, m_τ) · V_e^†`
on `H_hw=1` has frozen `U_e = I` via the Z_3-trichotomy. Maybe the
A-BCC condition `det H > 0` combined with the retained relation
`Y_l^† Y_l = ` specific Koide-cone form pins the point directly.

### A9. Chamber-boundary distance variational

**Functional.** `F_boundary(m, δ, q_+) = − log(q_+ − (√(8/3) − δ))`
(distance to the chamber caustic). At the caustic `det H = 0`.
Minimizing this pushes toward the boundary; combined with any
energetic functional, a trade-off could pin a specific point.

**Test.** `F_full = λ · F_boundary + (1 − λ) · F_energetic` for
various `λ` and choices of energetic functional. Look for a specific
`λ` such that the critical point is the pinned point.

### A10. Symplectic / fiber-bundle structure on the 2-real manifold

**Rationale.** The 2-real manifold might carry a natural symplectic
form (tied to the Z_3 equivariance). A Hamiltonian vector field
associated to a retained Hamiltonian could have its unique zero at
the pinned point.

**Test.** Construct the symplectic form (candidates: `dδ ∧ dq_+` or
something Z_3-equivariant). Identify a retained Hamiltonian. Look
for its critical point.

---

## Loop discipline

1. **Each iteration**: pick ONE attack from the backlog. Execute to
   completion (runner with concrete PASS/FAIL; companion note).
   Commit + push to `origin/afternoon-4-21`.
2. **If no good idea**: use that turn as a brainstorm turn. Add new
   candidates to this backlog with specific executable forms.
3. **Honest labeling**: negative results are as valuable as positive.
   Report them cleanly with what they RULE OUT.
4. **Composite attempts allowed**: if iter N shows attack X alone is
   insufficient, iter N+1 may combine X with Y from this list.
5. **Stop when**: the PMNS angle-triple selector is verified
   retained-forced (i.e., a specific framework-native functional has
   its critical point at the pinned chamber point, and the functional
   itself is theorem-grade retained), OR the backlog is genuinely
   exhausted.

---

## Next up (iter 8)

Iter 7 verified the closure equation `det(H) = E2 | δ·q+ = 2/3` is an
irreducible cubic in m with ℤ[√2, √3, √6] coefficients. It IS the
retained content at the polynomial level — but does not reduce to a
simpler one-scalar-equals-one-simple-value form. No third simple-value
scalar identity exists at the closure point within the broad class
tested.

Iter 8 primary direction: **variational on the 1-D curve**. On the
1-parameter curve `{δ · q_+ = 2/3, det(H) = E2}` (parameterized by m
or δ), search for a retained functional `F(m, δ, q_+)` whose
extremum along the curve is the physical point `(m_*, δ_*, q_+*)`.

Concrete candidates for the variational functional:

- `F = Tr(H^2) / Tr(H)^2` (dimensionless Koide-like ratio of H-spectrum
  invariants)
- `F = log |λ_max / λ_min|` (spread of eigenvalues)
- `F = Jarlskog(U_PMNS(H))` (CP-violation invariant, natural physical
  quantity)
- `F = Σ (arg K_ij)` (Z_3 phase sum on K-basis)
- `F = W[J]` restricted to the 1-D curve (observable principle on the
  reduced manifold)

Iter 8 plan:
1. Parametrize the 1-D curve by `m` (so δ = f(m), q_+ = g(m) solve
   δ·q_+ = 2/3 and det(H) = E2 simultaneously).
2. Compute each candidate F(m) along the curve.
3. Find extrema (zeros of dF/dm).
4. Check whether any extremum coincides with `m_*`.
5. If yes, that F is the third retained cut. Verify it's
   framework-native.

This would complete the selector gate with THREE retained identities.
