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

## Next up (iter 5)

**Candidate**: precision-sharpen test of `δ · q_+ = Q = 2/3`. The
strongest signal from iter 4 by far. Iter 5 settles whether this is
an exact retained identity or a 0.15%-level near-miss.

Concrete plan:
- Solve the chamber inversion at HIGH PRECISION (mpmath or symbolic
  sympy), re-pinning `(m, δ, q_+)` to the PDG 2024 central values
  `(sin²θ_12, sin²θ_13, sin²θ_23) = (0.307, 0.0218, 0.545)`.
- At that high-precision pinned point, compute `δ · q_+` to 10+
  digits. If it equals `2/3` to 10+ digits → retained identity
  confirmed.
- If confirmed: also test `Σλ / Σ|λ| = 1/6` at high precision (the
  other iter 4 near-hit).
- Additionally: re-pin under the CONSTRAINT `δ · q_+ = 2/3` exactly
  (imposing this as one of the three equations), and check whether
  the resulting PMNS angles are within PDG 3σ of central — this is
  the predictive falsifiability test.
- If both (retained exactness AND PDG-compatibility) hold, the gate
  closes via cross-sector I1 → I5 linkage and iter 6 moves to
  axiomatic derivation.
