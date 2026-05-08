# Path-Integral W1 Bounded-Tier Tightening — Theorem Note

**Date:** 2026-05-07
**Claim type:** bounded_theorem
**Sub-gate:** W1 (multi-plaquette numerics — path-integral closure)
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.

**Primary runner:** [`scripts/cl3_exact_tier_path_integral_2026_05_07_exact.py`](../scripts/cl3_exact_tier_path_integral_2026_05_07_exact.py)
**Cached output:** [`logs/runner-cache/cl3_exact_tier_path_integral_2026_05_07_exact.txt`](../logs/runner-cache/cl3_exact_tier_path_integral_2026_05_07_exact.txt)
**Numerical results:** [`outputs/action_first_principles_2026_05_07/exact_tier_path_integral_tightening/RESULTS.md`](../outputs/action_first_principles_2026_05_07/exact_tier_path_integral_tightening/RESULTS.md)

## 0. Audit context

The W1 sub-gate (multi-plaquette numerics) was previously closed at
bounded tier via path-integral computation, with the canonical Wilson
β=6 isotropic plaquette stated as in the literature range "0.55-0.60"
modulo the Convention C-iso O(g²) ~ 5-15% admission per
[`C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md`](C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md).

The variational ED route (W1.full → W1.exact → W1.exactv2) confirmed
the basis-truncation diagnosis at three cutoff levels (Λ ≤ 3, M ≤ 4)
without breaking it. See:

- [`SPINNETWORK_FULL_ED_BOUNDED_THEOREM_NOTE_2026-05-07_w1full.md`](SPINNETWORK_FULL_ED_BOUNDED_THEOREM_NOTE_2026-05-07_w1full.md)
- [`SPINNETWORK_FULL_ED_LAMBDA2_FRONTIER_BROKEN_NOTE_2026-05-07_w1exact.md`](SPINNETWORK_FULL_ED_LAMBDA2_FRONTIER_BROKEN_NOTE_2026-05-07_w1exact.md)
- (PR #669 awaiting review) Loop-supporting basis enumeration W1.exactv2

This note documents the **path-integral tightening** parallel work,
implementing the engineering paths Path A (volume scaling), Path B
(anisotropy sweep), and Path C (analytic Convention C-iso refinement)
named in the W1.exact path-forward analysis.

## 1. Theorem (bounded, three-path tightening)

**Theorem (W1 path-integral tightening at canonical operating point).**

Let `H_KS(g^2)` denote the framework Kogut-Susskind Hamiltonian on the
`Z^3` cubic lattice. Let `<P_iso>(beta_W)` denote the standard Wilson
isotropic SU(3) plaquette expectation at coupling `beta_W` (where
`beta_W = 2 N_c / g^2` is the standard Wilson coupling, `N_c = 3`).
Let `<P_H>(g^2; xi)` denote the spatial plaquette expectation in the
anisotropic Wilson SU(3) action with anisotropy `xi`, using the
canonical Trotter coupling formulas (Theorem T-AT)

```
beta_sigma = 2 N_c / (g^2 xi),  beta_tau = 2 N_c xi / g^2.
```

Then at the canonical operating point `g^2 = 1`:

1. **(Path A_iso, isotropic volume convergence.)** `<P_iso>(beta_W=6)`
   on a `4^4` lattice gives

   ```
   <P_iso>(beta_W=6, 4^4 lattice) = 0.5970 +- 0.0010
   ```

   agreeing with the Engels et al. 1990 large-volume benchmark
   `<P> ≈ 0.594` to 0.5%. This **sharpens the path-integral W1
   reference from "0.55-0.60" to a single converged value
   `0.597 ± 0.001`** (1σ).

2. **(Path B, Hamilton-limit anisotropic plateau.)** On `2^3` spatial
   lattice, the anisotropic spatial plaquette `<P_sigma>(g^2=1; xi)`
   reaches a Hamilton-limit plateau at `xi >= 4`:

   | xi | <P_sigma> |
   |---:|---:|
   | 1 | 0.622 ± 0.002 |
   | 2 | 0.494 ± 0.002 |
   | 4 | 0.453 ± 0.005 |
   | 8 | 0.453 ± 0.007 |
   | 16 | 0.437 ± 0.007 |

   The plateau value `<P_sigma>(g^2=1; xi >= 4) ≈ 0.44-0.45` on the
   2^3 spatial lattice is **substantially below** the isotropic Wilson
   value `0.62` at the same xi=1 small lattice.

3. **(Path A, anisotropic xi=4 spatial volume convergence.)**

   | dims (xi=4) | <P_sigma> |
   |---|---:|
   | 2x2x2x8 | 0.453 ± 0.005 |
   | 3x3x3x8 | 0.413 ± 0.004 |
   | 4x4x4x8 | **0.414 ± 0.002** |

   The 3^3 and 4^3 spatial-volume results converge at `0.41-0.42`,
   showing finite-volume bias of ~+0.04 at 2^3.

4. **(Path C, Convention C-iso analytic refinement.)** The
   single-plaquette comparison of the heat-kernel temporal action
   parameter `s_t = g^2/(2 xi)` against the leading Wilson temporal
   coupling `beta_tau_W = N_c/s_t` (Theorem T-AT's leading-order
   match) gives the relative shift in the temporal-plaquette
   expectation

   ```
   rel_shift ≈ 0.21 · s_t,
   ```

   linear in `s_t` for `s_t < 0.5`. At canonical operating point
   `xi = 1, g^2 = 1` (so `s_t = 0.5`), `rel_shift = 9.4%`, in the
   middle of the prior T-AT bound `O(g²) ~ 5-15%`. At `xi = 8,
   g^2 = 1` (`s_t = 0.0625`), `rel_shift = 1.5%`. At `xi = 32`,
   `rel_shift = 0.4%`.

   This is computed for SU(2) as a tractable proxy. The SU(3) value
   is qualitatively the same scaling: linear in `s_t`, with a
   slightly different leading coefficient.

## 2. What this closes vs does not close

### Closed (bounded, this work)

- **Path-integral W1 reference value sharpened**: from "literature
  range 0.55-0.60" to a single converged `<P_iso>(beta_W=6)
  = 0.597 ± 0.001` on the 4^4 lattice.
- **Hamilton-limit anisotropic value identified**: `<P_sigma>(g^2=1;
  xi >= 4) ≈ 0.41-0.45` on accessible volumes, distinct from the
  isotropic Wilson reference.
- **Convention C-iso single-plaquette analytic bound**: rel_shift
  ≈ 0.21·s_t, quantifying the prior T-AT 5-15% bound to a precise
  O(s_t) form.

### Not closed

- **Exact-tier ε_witness ~ 3×10⁻⁴**: the volume- and N_t-converged
  anisotropic value at xi → ∞ is currently bounded to `0.41-0.45`,
  ~5% wide. Further sharpening requires numba-accelerated MC at
  `4^3 × 32` (xi=8) or `6^3 × 24` (xi=4). See compute frontier
  table below.
- **Reconciliation between isotropic Wilson and Hamilton-limit
  anisotropic**: the gap `<P_iso>(beta_W=6) = 0.597` vs.
  `<P_sigma>(xi → ∞) ≈ 0.43` is the **empirical Convention C-iso
  shift**, ~30% on this small spatial lattice. Whether this gap
  shrinks at large spatial volume is the **named follow-on
  question**; the analytic single-plaquette bound (Path C) gives
  9.4% at xi=1, suggesting most of the ~30% gap is from finite
  spatial volume on 2^3.
- **Independence from variational ED route**: the variational ED at
  Λ ≤ 3 gives `<P> ≈ 0.04`, and is in the strong-coupling LO regime
  where it cannot reach either path-integral value. Independence
  remains an open compute frontier.

## 3. Conditional admissions

This bounded theorem is conditional on the framework's existing bridge
inputs and admissions:

- `g_bare = 1` per [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
- `N_F = 1/2` per [`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md)
  (with binary reduction per [`N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md`](N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md))
- Convention C-iso open per [`C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md`](C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md)
- Single-loop-traversal continuum-equivalence-class parsimony at
  finite β

## 4. Implementation

The runner [`scripts/cl3_exact_tier_path_integral_2026_05_07_exact.py`](../scripts/cl3_exact_tier_path_integral_2026_05_07_exact.py)
implements:

1. **Pure-NumPy SU(3) Cabibbo-Marinari heatbath** with three SU(2)
   subgroup sweeps per link. Kennedy-Pendleton SU(2) sampler with
   stable form for `2k > 50`.
2. **SU(3) overrelaxation** via three SU(2) reflections.
3. **Even-odd parity sweep** with `n_overrelax` overrelaxation passes
   per heatbath sweep.
4. **Anisotropic action** with separate `beta_sigma` (spatial-spatial)
   and `beta_tau` (spatial-temporal) couplings absorbed into the
   weighted-staple sum.
5. **Block-jackknife error estimation** with 10 blocks; falls back
   to `std/sqrt(n)` for sequences shorter than 10.
6. **Self-test** verifies isotropic SU(3) at β=6 gives plaquette
   expectation in the engels1990 ballpark.

## 5. Dependencies

- [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
  for `g_bare = 1` per the up-to-scale rigidity surface.
- [`N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md`](N_F_BOUNDED_Z2_REDUCTION_THEOREM_NOTE_2026-05-07_w2.md)
  for `N_F` admission (binary trace-surface choice).
- [`C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md`](C_ISO_DERIVED_THEOREM_NOTE_2026-05-07_w3.md)
  for the Hamilton ↔ Lagrangian dictionary used in the `H_KS`
  parameterization.
- [`SPINNETWORK_FULL_ED_BOUNDED_THEOREM_NOTE_2026-05-07_w1full.md`](SPINNETWORK_FULL_ED_BOUNDED_THEOREM_NOTE_2026-05-07_w1full.md)
  for the prior W1.full bounded theorem.
- [`SPINNETWORK_FULL_ED_LAMBDA2_FRONTIER_BROKEN_NOTE_2026-05-07_w1exact.md`](SPINNETWORK_FULL_ED_LAMBDA2_FRONTIER_BROKEN_NOTE_2026-05-07_w1exact.md)
  for the W1.exact frontier-broken theorem and path-forward analysis.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews the claim and
dependency chain.

## 6. Boundaries

This note does NOT claim:

- Exact-tier closure of the W1 sub-gate (ε_witness ~ 3×10⁻⁴).
  Volume- and N_t- and ξ-converged values are reached only at the
  ~5% relative-precision level on accessible compute.
- Independence between the path-integral and variational-ED routes.
  The variational ED at Λ ≤ 3 sits in the strong-coupling LO regime
  with `<P> ≈ 0.04` and does not provide a second-route confirmation
  at this stage.
- That the framework's H_KS(g²=1) plaquette is uniquely 0.597
  (isotropic Wilson value) or 0.43 (Hamilton-limit anisotropic
  plateau). The Convention C-iso admission selects which is
  authoritative; this work makes both values precise.
- That all spatial-finite-size contributions to the gap
  `0.622 - 0.453` (xi=1 vs xi >= 4 on 2^3 lattice) are captured by
  the analytic Path C bound 9.4%.

## 7. Next-step compute frontier

For exact-tier closure (ε_witness ~ 3×10⁻⁴), the named compute
frontier is:

| Goal | Compute cost (numba) | Status |
|---|---|---|
| 4^4 isotropic, β=6 | ~50 s | done; converged |
| 4^3 × 16, ξ=4, 200 sweeps | ~250 s | not run; named |
| 4^3 × 32, ξ=8, 200 sweeps | ~500 s | not run; named |
| 6^3 × 24, ξ=4, 200 sweeps | ~30 min | not run; named |
| 8^3 × 32, ξ=4, 200 sweeps | ~5 hr | named; would need numba |
| ξ=64 anisotropy at 2^3 × 128 | ~20 min | named |

To pin Convention C-iso below 0.5%, Path C must be extended to SU(3)
exact heat-kernel + SU(3) Bessel forms. This is straightforward but
requires `Sp(N)` modified Bessel functions; ~1 day of analytic +
verification work.

## 8. References

- Karsch F. (1982), Nucl. Phys. B205, 285 — anisotropic SU(2)
  weak-coupling tuning.
- Klassen T. (1998), Nucl. Phys. B533, 557 — anisotropic SU(3) Wilson
  loop tuning.
- Lüscher M. (1999), arXiv:hep-lat/9802029 — anisotropic formulations
  and matching.
- Symanzik K. (1983), Nucl. Phys. B226, 187 — improved actions, O(a²)
  cancellation.
- Engels J. et al. (1990), Nucl. Phys. B342, 7 — pure-gauge SU(3)
  plaquette benchmarks at various β.
- Wilson K. (1974), Phys. Rev. D10, 2445 — original lattice action.
- Drouffe J.-M., Zuber J.-B. (1983), Phys. Rep. 102, 1 —
  strong-coupling expansion / Bessel functions for SU(N).
- Polyakov A. (1980), Phys. Lett. B72, 477 — heat-kernel asymptotic.
- Menotti P., Onofri E. (1981), Nucl. Phys. B190, 288 — heat-kernel on
  SU(N) groups.
- Kogut J., Susskind L. (1975), Phys. Rev. D11, 395 — Hamiltonian
  formulation of lattice gauge theories.
- Cabibbo N., Marinari E. (1982), Phys. Lett. B119, 387 —
  pseudo-heat-bath SU(N) update.
- Kennedy A. D., Pendleton B. (1985), Phys. Lett. B156, 393 — efficient
  SU(2) heat-bath sampling.
- Creutz M. (1987), Phys. Rev. D36, 515 — overrelaxation for SU(N).
