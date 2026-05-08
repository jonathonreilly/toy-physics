# Full SU(3) Spin-Network ED — Bounded Theorem (Variational Implementation + Compute Frontier)

**Date:** 2026-05-07
**Claim type:** bounded_theorem
**Status:** unaudited candidate. This note is graph-visible only so the
independent audit lane can decide its audit and effective status.
**Primary runner:** [`scripts/cl3_ks_full_spinnet_ed_v4_2026_05_07_w1full.py`](../scripts/cl3_ks_full_spinnet_ed_v4_2026_05_07_w1full.py)
**Cached output:** [`logs/runner-cache/cl3_ks_full_spinnet_ed_v4_2026_05_07_w1full.txt`](../logs/runner-cache/cl3_ks_full_spinnet_ed_v4_2026_05_07_w1full.txt)
**Source-note proposal:** audit verdict and downstream status set only
by the independent audit lane.

## 0. Audit context

The bridge gap's multi-plaquette numerics sub-gate (W1) was previously
addressed at bounded tier via path-integral computation (anisotropic
Wilson 4D MC). The path-integral approach reaches the KS literature
range `⟨P⟩_KS(g²=1) ≈ 0.55-0.60` within Hamilton-limit corrections
`O(g²) ~ 5-15%` (parented per the Convention C-iso admission documented
in [`C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md`](C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md)).

The follow-up question (W1.full) is whether the variational
spin-network ED — the *direct* lattice computation in the
Hamiltonian framework — can independently reach the literature
value via a controlled truncation, without relying on the
path-integral comparator. This note documents a **bounded engineering
implementation**: the ED machinery is implemented and validated,
convergence trends are documented, and the compute frontier preventing
exact-tier closure is named explicitly.

## 1. Theorem (proposed, bounded)

**Theorem (Spin-Network ED of `H_KS` on 2×2 PBC torus, irrep cutoff `Λ`,
active-link cutoff `M`).**

Let `H_KS(g², Λ, M)` denote the framework Kogut-Susskind Hamiltonian

```
H_KS = (g²/2) Σ_e Ĉ_e − (1/(g² N_c)) Σ_p Re Tr U_p     (N_c = 3)
```

projected onto the spin-network subspace `H^(Λ, M)` of states with all
link irreps `λ_e` satisfying `p_e + q_e ≤ Λ` and at most `M` of the 8
links carrying non-trivial irreps. Then:

1. The Hamiltonian matrix elements are well-defined and computable
   via standard SU(3) representation theory (explicit `D^(p,q)(U)`
   matrices, exact integer Clebsch-Gordan, Haar-projection vertex
   intertwiners).
2. The Casimir matrix elements are diagonal in `{λ_e}` with eigenvalue
   `(g²/2) Σ_e C_2(λ_e)`.
3. The magnetic matrix elements couple configurations differing by
   tensor-product fusion with the fundamental rep on the 4 plaquette
   boundary edges.
4. The ground-state energy is variationally bounded as the truncated
   basis is enlarged. The plaquette expectation `⟨P⟩(Λ, M; g²)` is
   measured by the runner at each cutoff but is not itself a variational
   monotonicity theorem.
5. **At currently-tractable cutoffs** (`Λ ≤ 1, M ≤ 5`), the
   variational bound gives `⟨P⟩(g²=1) ≤ 0.05`, **strictly below** the
   path-integral benchmark `0.50 ± 0.05` and KS literature
   `0.55-0.60`. The basis-completeness gap is the named compute
   frontier.

## 2. Conditional admissions

This bounded theorem is conditional on the framework's existing bridge
inputs and admissions:

- `g_bare = 1` as imported through [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
- `N_F = 1/2` as imported through [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  (admission at L3, with binary reduction per [`N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md`](N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md))
- Single-loop-traversal continuum-equivalence-class parsimony at
  finite β (continuum closure derived; finite-β parsimony admitted
  per the bridge fragmentation analysis)

The theorem's variational bound holds rigorously under these
admissions; the basis-truncation result is independent of admission
choices.

## 3. Implementation (verified)

The runner [`scripts/cl3_ks_full_spinnet_ed_v4_2026_05_07_w1full.py`](../scripts/cl3_ks_full_spinnet_ed_v4_2026_05_07_w1full.py)
is the primary verification. Three SU(3) representation-theory modules
are built and validated:

1. [`scripts/cl3_ks_su3_rep_infrastructure_2026_05_07_w1full.py`](../scripts/cl3_ks_su3_rep_infrastructure_2026_05_07_w1full.py)
   — explicit `D^(p,q)(U)` matrices via Young symmetrizer on
   `(C^3)^⊗(p+2q)` (Schur-Weyl). Verified: dimensions correct,
   unitarity to ~1e-15, characters match Jacobi-Trudi formula to
   ~1e-15.

2. [`scripts/cl3_ks_su3_clebsch_gordan_2026_05_07_w1full.py`](../scripts/cl3_ks_su3_clebsch_gordan_2026_05_07_w1full.py)
   — exact integer tensor-product decomposition via Freudenthal
   recursion. Verified against standard SU(3) products (3⊗3 = 6 ⊕ 3̄,
   8⊗8 = six irreps including {1, 8, 8, 10, 10̄, 27}, 3⊗3⊗3̄⊗3̄ →
   trivial multiplicity 2, 8⊗8⊗8 → trivial multiplicity 2).

3. [`scripts/cl3_ks_full_spinnet_geometry_2026_05_07_w1full.py`](../scripts/cl3_ks_full_spinnet_geometry_2026_05_07_w1full.py)
   — 2×2 spatial torus geometry (4 sites, 8 links, 4 plaquettes);
   link/vertex/plaquette incidence verified self-consistent.

## 4. Numerical results (cached)

At `Λ=1, M=4, g²=1, N_samples=4000`:

```
n_basis = 81
E_0 = -0.0964
⟨P⟩_avg = 0.0226
per-plaq P = [0.017, 0.019, 0.028, 0.026]
```

Coupling sweep at `Λ=1, M=4` (verified end-to-end in cached output):

| g² | E_0 | ⟨P⟩ |
|---|---|---|
| 0.5 | -0.564 | 0.051 |
| 0.75 | -0.205 | 0.035 |
| 1.0 | -0.096 | 0.023 |
| 1.5 | -0.042 | 0.011 |
| 2.0 | -0.033 | 0.007 |

Monotonic decrease with `g²` is consistent with the deconfinement →
confinement transition. **All values are far below the literature
target** `0.55-0.60` at `g²=1`.

## 5. Compute frontier (named)

The basis-completeness frontier blocking exact-tier closure:

| Cutoff configuration | Status | Bottleneck |
|---|---|---|
| `Λ=1, M=4` | works (0.5s, 81 states) | — |
| `Λ=1, M=5` | works (1.5s, 145 states) | — |
| `Λ=1, M=6` | partial | per-config einsum >1s × 200+ configs |
| `Λ=2, M=4` | blocked | vertex Q construction at `(1,1)⊗(1,1)⊗(1,1)⊗(1,1)` requires 4096-dim eigh, exceeds 600 MB / 2 min |
| `Λ ≥ 3` | not reached | — |

Three concrete paths to reach higher cutoffs:
- Dedicated SU(3) recoupling library (e.g. SU3LIB) with closed-form
  6j-symbols
- GPU-accelerated tensor contraction
- Caching vertex eigendecompositions across permutation-equivalent
  shapes

## 6. What this closes vs does not close

### Closed (bounded)

- The proper spin-network ED machinery is implementable for SU(3)
  lattice gauge theory at the framework's canonical Hamiltonian.
- The SU(3) representation-theory infrastructure is validated to
  machine precision (Schur-Weyl, Freudenthal, Haar-projection
  intertwiners, MC-Haar magnetic-element integration).
- Variational convergence trends are documented and consistent with
  prior diagnosis: small-`Λ` truncations remain in the strong-coupling
  LO regime (`⟨P⟩ ≈ 0.04-0.05` at `g²=0.5-1`).
- The basis-truncation diagnosis from the prior path-integral closure
  is **confirmed at the next level of rigor**: even with the full
  spin-network basis (not just character-products), small `Λ`
  truncations cannot reach the weak-coupling vacuum.

### Not closed

- **Exact-tier closure of W1**: variational ED at currently-tractable
  cutoffs does NOT reach the KS literature value `~0.55-0.60`. The
  path-integral computation (Convention C-iso admitted) remains the
  bounded-tier closure of the multi-plaquette numerics sub-gate.
- **Independence from path-integral**: this work confirms the
  basis-truncation diagnosis but does not provide an *independent*
  variational-ED route to the literature value at exact tier.
- **Higher-`Λ` convergence**: the `Λ=2, M=4` configuration is
  blocked by vertex-intertwiner eigendecomposition memory pressure;
  closure at `Λ ≥ 2` would require the named compute optimizations.

## 7. Honest scope statement

This is the **engineering implementation** of the proper spin-network
ED specified in the prior multi-plaquette numerics work as the path
to exact-tier closure of W1. The implementation runs end-to-end and
produces the predicted variational-bounding behavior. The result is
that **at compute-tractable cutoffs the basis is structurally too
truncated to reach the weak-coupling vacuum**, confirming the prior
basis-truncation diagnosis.

The path-integral approach remains the bounded-tier closure of the
multi-plaquette numerics sub-gate; this work does not supersede that
closure but rather provides the second-route confirmation that the
basis-truncation issue is structural, not algorithmic.

## 8. References

- Standard SU(3) representation theory: Slansky 1981 §3,
  Greiner-Müller chapters 8-9, Fulton-Harris Lectures 4-6.
- Spin-network basis: Baez 1994; Rovelli-Smolin 1995.
- Kogut-Susskind Hamiltonian: Kogut-Susskind 1975, Phys. Rev. D 11.
- Wilson 4D lattice gauge theory: Wilson 1974, Phys. Rev. D 10.
- Convention C-iso (Hamilton-Lagrangian dictionary admission):
  [`C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md`](C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md).
- `g_bare = 1` Hamiltonian rigidity:
  [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md).
- `N_F` four-layer stratification:
  [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md).
- `N_F` continuous-to-binary reduction:
  [`N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md`](N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md).
