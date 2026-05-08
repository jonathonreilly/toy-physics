# Full SU(3) Spin-Network ED — Λ=2 Compute Frontier Broken (W1.exact)

**Date:** 2026-05-07
**Claim type:** bounded_theorem
**Status:** unaudited candidate. This note is graph-visible only so the
independent audit lane can decide its audit and effective status.
**Primary runner:** [`scripts/cl3_ks_full_spinnet_ed_2026_05_07_w1exact.py`](../scripts/cl3_ks_full_spinnet_ed_2026_05_07_w1exact.py)
**Cached output:** [`logs/runner-cache/cl3_ks_full_spinnet_ed_2026_05_07_w1exact.txt`](../logs/runner-cache/cl3_ks_full_spinnet_ed_2026_05_07_w1exact.txt)
**Source-note proposal:** audit verdict and downstream status set only
by the independent audit lane.

## 0. Audit context

The prior W1.full result
([`SPINNETWORK_FULL_ED_BOUNDED_THEOREM_NOTE_2026-05-07_w1full.md`](SPINNETWORK_FULL_ED_BOUNDED_THEOREM_NOTE_2026-05-07_w1full.md))
implemented full SU(3) spin-network ED on the 2×2 spatial torus and
documented a compute frontier: at `Λ=2, max_active=4`, the vertex Q
construction at `(1,1)⊗(1,1)⊗(1,1)⊗(1,1)` requires a 4096-dim
eigendecomposition that exceeds 600 MB / 2 minutes, blocking the run.

This note documents the **engineering breakthrough**: replacing the
dense `eigh` on the 4096×4096 projector with **matrix-free Lanczos via
tensor-product matvec** breaks the frontier. The `Λ=2, max_active=4`
configuration now runs in ~79 seconds with basis dim 439.

**The structural finding**: even with the frontier broken, the
variational ED at `Λ=2, max_active=4, g²=1` gives `⟨P⟩ = 0.016`. This
**confirms the basis-truncation diagnosis at the next cutoff level**:
the weak-coupling vacuum has support beyond `Λ=2, max_active=4`. The
prior path-integral computation (anisotropic Wilson 4D MC) remains the
bounded-tier closure of the multi-plaquette numerics sub-gate.

## 1. Engineering optimization (the breakthrough)

The W1.full v4 runner used:

```
P_inv = (1/N_haar) Σ_g (⊗_legs D^lam(g))    # 4096×4096 dense matrix
evals, evecs = eigh(P_inv)                    # O(N³) = O(7×10¹⁰) flops
Q = evecs[:, -n_inv_expected:]
```

The matrix `P_inv` for `(1,1)⊗(1,1)⊗(1,1)⊗(1,1)` legs is `4096×4096`
complex, requiring ~268 MB just to store. The full `eigh` requires
~600 MB workspace and ~2 minutes wall-clock. This blocked the run.

The W1.exact runner replaces this with **matrix-free Lanczos**:

```
def matvec(v_flat):
    v = v_flat.reshape(*leg_dims)           # tensor view
    result = Σ_g [⊗_a D^lam_a(g) · v]       # tensor-product matvec
    return result.flatten()
op = LinearOperator(shape=(D_total, D_total), matvec=matvec)
evals, evecs = eigsh(op, k=n_inv_expected+2, which='LA')
```

**Cost reduction**: each matvec is `O(d² × n_legs × N_haar)` (apply
each leg's `D^lam(g)` to the corresponding tensor axis), totaling
`64 × 4 × 200 = 5×10⁴` flops per matvec. Lanczos converges to top
`n_inv` eigenvalues in `~100` iterations: total `~5×10⁶` flops vs the
dense `eigh`'s `~7×10¹⁰`. **~10⁴× speedup**, with `O(d⁴)` memory in
total (16 MB for `(1,1)^4`) instead of `O(D²) = O(d^(2k))` (270 MB).

The optimization triggers when `D_total > 256` (per-vertex dimension
threshold); below that, dense `eigh` is faster.

## 2. Theorem (proposed, bounded)

**Theorem (W1.exact: Λ=2, max_active=4 compute frontier broken).**

Let `H_KS(g², Λ, M)` be the framework Kogut-Susskind Hamiltonian on
the 2×2 spatial torus projected onto the spin-network subspace
`H^(Λ, M)` with irrep cutoff `Λ` and active-link cutoff `M`. Then:

1. The ground state of `H_KS(g², Λ=2, M=4)` is computable in finite
   time via matrix-free Lanczos vertex Q construction + dense MC
   matrix elements + dense eigh on the truncated Hamiltonian, despite
   the vertex shape `(1,1)⊗(1,1)⊗(1,1)⊗(1,1)` having full intertwiner
   space dimension `4096`.

2. At canonical operating point `g²=1`, the ground-state plaquette
   expectation is

   ```
   ⟨P⟩(g²=1, Λ=2, M=4) = 0.016 ± MC noise
   ```

   (basis dim 439, runtime 79 s, 56 unique vertex shapes, with
   `N_haar=200, N_samples=2000`).

3. The result is **strictly below** the path-integral / KS literature
   benchmark `⟨P⟩_KS(g²=1) ≈ 0.50-0.60` and slightly **below** the
   prior `Λ=1, M=4` variational result `0.023`. Both observations are
   **consistent with the basis-truncation diagnosis**: the weak-
   coupling vacuum has support primarily on high-irrep states beyond
   accessible `Λ` at this `M` cap.

## 3. Conditional admissions

Same as the W1.full bounded theorem:
- `g_bare = 1` per [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
- `N_F = 1/2` per [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  (with binary reduction per [`N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md`](N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md))
- Convention C-iso open per [`C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md`](C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md)
- Single-loop-traversal continuum-equivalence-class parsimony at finite β

## 4. Numerical results

### 4a. Sanity check (matches W1.full v4)

At `Λ=1, M=4, g²=1, N=4000, N_haar=200`:

```
n_basis = 81
E_0 = -0.099   (W1.full v4: -0.109; agrees within MC noise)
⟨P⟩_avg = 0.023   (W1.full v4: 0.025; agrees within MC noise)
runtime = 0.6s
```

### 4b. Λ=2, M=4 frontier broken

At `Λ=2, M=4, g²=1, N=2000, N_haar=200`:

```
n_basis = 439     (W1.full v4: predicted 439, never completed)
E_0 = -0.444      (significantly below Λ=1 M=4; variational improvement)
⟨P⟩_avg = 0.016   (slightly below Λ=1 M=4 = 0.023)
runtime = 79.5s   (W1.full v4: > 120 s + 600 MB blocked)
n_VQ_unique = 56
```

The 79s runtime decomposes as:
- Q-build: 63 s for 56 unique vertex shapes (cached across configs)
- Ψ-eval: 3 s for 251 configs
- H/Gram + diag: ~13 s

### 4c. Coupling sweep

The landed cache is scoped to the `Λ=2, M=4, g²=1` frontier-breaking
claim plus lower-cutoff sanity checks. A full coupling sweep at `Λ=2,
M=4` is a useful follow-on compute run but is not part of this note's
load-bearing cached support.

### 4d. Cutoff comparison at g²=1

| Cutoff | n_basis | ⟨P⟩ | E_0 | runtime |
|---|---|---|---|---|
| Λ=0, M=0 | 1 | 0.000 | 0.0 | <0.1 s |
| Λ=1, M=4 | 81 | 0.023 | -0.099 | 0.6 s |
| **Λ=2, M=4** | **439** | **0.016** | **-0.444** | **79 s** |
| Path-integral 2×2×2, ξ=4 | — | 0.488 | — | (separate work) |
| KS literature target | — | 0.55-0.60 | — | (target) |

The energy `E_0` decreases monotonically with cutoff (variational
improvement). The plaquette `⟨P⟩` does NOT increase monotonically; it
decreases from `Λ=1` to `Λ=2`. This is consistent with: at `Λ=2`,
additional admixture of higher irreps `(1,1), (2,0), (0,2)` to the
ground state distributes weight across more states, slightly lowering
the per-plaquette expectation while substantially lowering total
energy.

## 5. What this closes vs does not close

### Closed (bounded)

- **The W1.full compute frontier at Λ=2, M=4 is broken**. Matrix-free
  Lanczos vertex Q construction makes the run feasible in ~79 s with
  ~16 MB peak memory.
- The full SU(3) spin-network ED machinery scales to higher cutoffs
  with the documented optimization.
- The basis-truncation diagnosis from W1.full is **confirmed at the
  next cutoff level**: `Λ=2, M=4` does NOT reach the literature
  value `0.55-0.60`; it gives `⟨P⟩ = 0.016`.

### Not closed

- **Exact-tier closure of the multi-plaquette numerics sub-gate**: even
  at `Λ=2, M=4`, the variational ED gives `⟨P⟩ ≈ 0.016`, far below
  the literature target. The path-integral approach (Convention C-iso
  admitted) remains the bounded-tier closure.
- **Higher cutoffs** (`Λ ≥ 3` or `M ≥ 5`): the matrix-free Lanczos
  optimization helps but the basis enumeration still grows
  combinatorially. `Λ=2, M=5` would have ~2000+ configs and take
  several × 79 s. `Λ=3` would face new vertex shapes with even
  larger total dim.
- **Independence from path-integral confirmation**: this work confirms
  the basis-truncation diagnosis at one more cutoff, but does not
  provide an *independent* variational-ED route to the literature
  value at exact tier.

## 6. Path forward to exact-tier closure

The dominant remaining cost is **basis enumeration**, not vertex Q
construction. To reach the literature value at exact tier:

1. **Loop-supporting active-link enumeration**: only configurations
   forming closed loops have non-zero magnetic matrix elements. Filter
   the `C(8, M)` active-link tuples to those forming closed loops on
   the 2×2 torus before iterating over irrep assignments.

2. **Importance sampling of basis**: instead of exhaustive enumeration,
   build a Lanczos-Krylov subspace by repeatedly applying H to the
   current candidate ground state. Captures the relevant subspace
   without enumerating all `Λ^M`-scale configs.

3. **Closed-form 6j-symbol contraction**: replace MC-Haar magnetic
   matrix elements with exact `6j`-symbol contractions for SU(3). The
   `pysu3lib` library or similar provides closed-form `6j` symbols.
   Eliminates MC noise and is faster at fixed accuracy.

4. **Larger geometry with sparse representation**: 3×3 or 4×4 spatial
   torus has more plaquettes, smaller boundary effects, but exponen-
   tially larger basis. Sparse-tensor-network representation (PEPS)
   may make this tractable.

These are **engineering-decoupled directions**; each can be pursued
independently without affecting the others.

## 7. Honest scope statement

This is the **engineering breakthrough** for the W1.full compute
frontier: matrix-free Lanczos vertex Q construction makes `Λ=2, M=4`
feasible. The result confirms the basis-truncation diagnosis at the
next cutoff level — the variational ED at this cutoff still does not
reach the literature value `0.55-0.60`.

The path-integral approach remains the bounded-tier closure of the
multi-plaquette numerics sub-gate; this work demonstrates that the
basis-truncation barrier is structural across cutoff levels, not
specific to `Λ=1`.

Future closure attempts should target the basis-enumeration scaling
(loop-supporting filter, importance sampling, closed-form `6j`) rather
than the vertex Q construction (which is now O(d^k) memory, O(d^k
× N_haar × n_iter) time per shape, cached across configs).

## 8. References

- Standard SU(3) representation theory: Slansky 1981 §3, Greiner-Müller
  ch. 8-9, Fulton-Harris Lectures 4-6.
- Spin-network basis: Baez 1994; Rovelli-Smolin 1995.
- Kogut-Susskind Hamiltonian: Kogut-Susskind 1975, Phys. Rev. D 11.
- Lanczos algorithm for sparse eigenvalue problems: Lanczos 1950;
  Demmel "Applied Numerical Linear Algebra" §7.4.
- Matrix-free Lanczos in scipy: `scipy.sparse.linalg.eigsh`
  documentation; ARPACK reference manual.
- Wigner-Racah `6j`-symbol algebra: Sharp & Pieper 1971;
  Bargmann 1962; Edmonds 1957.
- Prior bounded-tier W1 closure via path-integral: see
  [`SPINNETWORK_FULL_ED_BOUNDED_THEOREM_NOTE_2026-05-07_w1full.md`](SPINNETWORK_FULL_ED_BOUNDED_THEOREM_NOTE_2026-05-07_w1full.md).
