# REVIEW HISTORY — axiom-first-foundations block01

Branch-local review notes after each major artifact. Live active review
queue (`docs/repo/ACTIVE_REVIEW_QUEUE.md`) is **not** updated during the
science run; proposed weaving lives in `HANDOFF.md`.

## Cycle 1 — R1: spin-statistics (in-loop self-review)

**Artifacts.**
- `docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
- `scripts/axiom_first_spin_statistics_check.py`
- `outputs/axiom_first_spin_statistics_check_2026-04-29.txt`

**Runner result.** PASSED 4/4 exhibits (E1–E4). Sign-flip exhibited
non-trivially in E4 (|±0.5|, sum exactly 0).

**In-loop review findings.**

1. *Mid-cycle correction.* The first draft of Step 2 used a "bosonic
   Gaussian divergence" argument. That argument is wrong for the
   canonical staggered Dirac–Wilson `M` at `g_bare = 1` with mass term
   and Wilson term: `H(M) = (M+M†)/2` is in fact positive definite
   (runner E2 context print: min eigval `+0.30`, max `+6.30`,
   `#neg/zero/pos = 0/0/8` on `L=2, dim=3`). The corrected Step 2
   uses the per-site Hilbert space dimension argument: `[a,a^†] = I`
   has no finite-dimensional realisation (trace argument: `tr([a,a^†]) =
   0` always, while `tr(I) = K`), so a bosonic implementation forces
   per-site Hilbert dim `ℵ_0`, contradicting `A1`'s finite-dim Cl(3)
   spinor module. Note explicitly records the corrected argument and
   why the original textbook intuition fails on this surface.
2. *Hypothesis set audit.* The proof uses A1 (only finite-dim Cl(3)
   irrep), A2 (only finite block), A3 (Grassmann partition, quadratic
   action), A4 (only to fix the canonical `M`). No literature theorem,
   no observed value, no fitted parameter, no continuum Lorentz axiom.
   Forbidden-imports list respected.
3. *Status.* Branch-local theorem. Not promoted to retained or
   Nature-grade. Promotion would require external review-loop
   backpressure and integration through the derivation atlas, which
   are out of scope for this run per skill rule 12.
4. *Reuse.* C1–C4 corollaries are written so DM/leptogenesis, Yukawa,
   CKM, and observable-principle lanes can quote the result directly.

**Disposition.** Accept artifact as branch-local theorem. Continue to
Cycle 2 (R2: reflection positivity).

## Cycle 2 — R2: reflection positivity (in-loop self-review)

**Artifacts.**
- `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
- `scripts/axiom_first_reflection_positivity_check.py`
- `outputs/axiom_first_reflection_positivity_check_2026-04-29.txt`

**Runner result.** PASSED 4/4 exhibits (E1–E4). E1 free staggered
transfer matrix is Hermitian (||T-T†|| = 1e-15) and positive
(spectrum strictly > 0). E2 single-plaquette U(1) gauge transfer
matrix likewise. E3 RP inequality `<Θ(F) F> ≥ 0` verified on 40
single-mode and pair-mode observable insertions across 4 time
separations — all real and non-negative. E4 half-action Gram matrix
positive semi-definite.

**In-loop review findings.**

1. *Mid-cycle correction.* The first draft of E1 asserted `T ≤ 1` in
   operator norm. That is true *only* after ground-state /
   zero-point subtraction `H_phys = H_lat - E_0`. The runner uses the
   unsubtracted `H_lat`, whose spectrum is symmetric about zero, so
   `T = exp(-a_τ H_lat)` has `max(T) ≈ 8` on the test setup. RP
   *requires* `T ≥ 0` (positivity), not `T ≤ 1` (the latter is a
   normalisation choice). The check now reports `T ≥ 0` and notes the
   subtraction caveat in the output.
2. *E2 scope.* The original E2 attempted a 2×2 spatial torus (8 links,
   dim ≈ 5.7M with ±3 truncation) and was correctly skipped. Replaced
   with a single-plaquette 4-link system (dim 2401), which is the
   smallest non-trivial gauge-plaquette transfer-matrix exhibit in
   the abelian sector. Since the standard RP proof factorises
   plaquette-by-plaquette, single-plaquette suffices for the
   structural exhibit.
3. *Hypothesis set audit.* Step 1 (gauge half) uses A4 only via
   compactness of SU(3), Haar invariance, and `β > 0`. Step 2
   (fermion half) uses A1 via the Cl(3) C-matrix and staggered phases,
   A3 via the canonical staggered + Wilson + mass action. Step 3
   (combined) uses the standard `γ_5`-Hermiticity already supported
   by the strong-CP retention. No imports from the forbidden list;
   the only "imports" are theorem-grade lattice references
   (Osterwalder-Seiler 1978; Sharatchandra-Thun-Weisz 1981; Menotti-
   Pelissetto 1987; Lüscher 1977).
4. *Status.* Branch-local theorem. Promotion would require external
   review-loop backpressure and integration outside this run.
5. *Reuse.* C1 (Hermitian transfer matrix), C2 (`H_phys`
   reconstruction), C3 (spectrum-condition lattice analogue), C4
   (compatibility with `θ_eff = 0` retention) are written for direct
   citation by mass-gap, confinement, transfer-matrix, and CPT lanes.
6. *Linkage.* This theorem retroactively cleans the implicit RP
   premise used in Cycle 1's per-site Hilbert-space argument: the
   transfer matrix construction underlying the Cl(3) finite-dim
   per-site Hilbert space is now an axiom-first theorem, not an
   assumption. Cycle 1 + Cycle 2 form a coherent foundational pair.

**Disposition.** Accept artifact as branch-local theorem. Continue to
Cycle 3 (R3: cluster decomposition / Lieb–Robinson).

## Cycle 3 — R3: cluster decomposition / Lieb–Robinson (in-loop self-review)

**Artifacts.**
- `docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
- `scripts/axiom_first_cluster_decomposition_check.py`
- `outputs/axiom_first_cluster_decomposition_check_2026-04-29.txt`

**Runner result.** PASSED 4/4 exhibits. E1 LR exponential envelope
exhibited on a 1D free fermion lattice (24 sites): log₁₀ |U(t)_{0,d}|
table covers (d, t) ∈ [0, 12] × [0, 4], with clear exponential decay
in d outside the light cone (slope -2.48 at t=1.0, decay length 0.4).
E2 connected `<n_0 n_d>` ground-state correlator decays from 8.4e-2
at d=1 to 1.8e-5 at d=10, log-linear slope ≈ -0.86 (exponential due
to the staggered mass gap). E3 100% of spacelike cells satisfy
|U| < 0.05. E4 effective front velocity v_eff = 1.17, far below the
LR-1972 conservative bound v_LR = 10.87 — exactly the expected
ordering (LR is conservative; tighter Hastings 2010 / Bravyi-Hastings
2011 bounds are not needed for the structural exhibit).

**In-loop review findings.**

1. *Hypothesis set audit.* Proof uses A1 (Cl(3) op-norm bound), A2
   (lattice graph distance, Z_lat = 6, finite-range), A3 (Hermitian
   Hamiltonian + finite per-site algebra), A4 (O(1) bound on J). No
   imports from forbidden list. The Lieb-Robinson 1972 technique is
   an elementary finite-lattice manipulation; standard external
   references cited as theorem-grade lattice literature.
2. *LR bound is conservative; runner shows this honestly.* The
   LR-1972 constants give v_LR ≈ 10.87 for J=0.5, R=1, Z=2 in 1D;
   the actual propagation front velocity for free fermions is
   v_eff ≈ 1.17 (group velocity ≤ 2J for nearest-neighbour). The
   theorem as stated provides the conservative envelope; the runner
   reports both the predicted bound and the empirical front velocity,
   and confirms v_eff < v_LR. This is the correct ordering: the
   theorem provides an upper bound, not an equality.
3. *Status.* Branch-local theorem. Promotion would require external
   review-loop backpressure and integration outside this run.
4. *Reuse.* C1 (mass-gap exponential decay), C2 (confinement
   area-law lane support), C3 (microcausality on A_min), C4
   (compatibility with R2 / RP). Confinement / area-law lanes that
   silently assume exponential clustering can now cite this theorem.
5. *Linkage.* Cycle 1 (spin-statistics) + Cycle 2 (RP) + Cycle 3
   (LR/clustering) form the lattice analogue of the Wightman
   axiom triple "spin-statistics + positivity-of-energy +
   cluster-decomposition" — discharged as branch-local theorems on
   A_min instead of imported as primitives.

**Disposition.** Accept artifact as branch-local theorem. Proceed to
stretch attempt (Cycle 4 / R4: CPT theorem).

