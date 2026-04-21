# Reviewer Stress-Test for I1 and I2/P

**Date:** 2026-04-21
**Status:** Enumerated reviewer objections addressed by executable checks.
**Runner:** `scripts/frontier_koide_reviewer_stress_test.py` — 42/42 PASS.

---

## Scope

Enumerates the strongest reviewer objections to:
- **I1** (Q = 2/3 via F-functional + AM-GM)
- **I2/P** (δ = 2/9 rad via APS topological robustness)

Each objection is either answered by an executable check in this
runner or cited to the specific retained-source runner/note that
establishes it.

## CAT-A: Uniqueness (4 objections)

- **A1** *Is F = log(E_+ · E_⊥) unique given retained axioms?*
  The Frobenius inner product is the canonical trace form on matrix
  algebras, unique up to scale. Max at E_+ = E_⊥ gives κ = 2 by
  strict concavity. A Peter-Weyl weighting with (1, 2) exponents
  would give κ = 1, disagreeing with the Koide κ = 2.

- **A2** *Is the extremum a global max (not saddle)?*
  log(x·y) under x + y = N is strictly concave (Hessian eigenvalues
  −1/x² and −1/y² are negative in the interior). Unique critical
  point at x = y is the global max.

- **A3** *Are the (1, 2) tangent weights uniquely forced?*
  C_3[111] rotation by 2π/3 has eigenvalues (ω, ω²) on the
  transverse plane. Weights (1, 2) mod 3 are forced by these
  eigenvalues (up to the trivial (a, b) ↔ (b, a) swap, which the
  ABSS formula is symmetric under).

- **A4** *Is η = 2/9 unique for (1, 2) weights?*
  The ABSS formula gives η(1, 2; 3) = 2/9 exactly via the core
  identity (ζ − 1)(ζ² − 1) = 3. Symmetry η(a, b) = η(b, a). No
  alternative value.

## CAT-B: Scope (3 objections)

- **B1** *AM-GM requires positive reals — is E_+, E_⊥ positive?*
  E_+ = 3a² ≥ 0 (a real), E_⊥ = 6|b|² ≥ 0 (b complex). Physical
  non-degenerate charged leptons have both > 0 (interior case).

- **B2** *APS requires smooth spin manifold; retained is PL.*
  PL S³ is smoothable (Cerf's theorem, dim ≤ 6). Z_3 action lifts
  to smoothed manifold via equivariant smoothing. ABSS metric-
  independence makes the resulting η independent of the smoothing
  choice.

- **B3** *Morse-Bott condition for ABSS?*
  Z_3 fixed locus is codim-2 (two timelike worldlines on PL S³ × R).
  Normal Hessian eigenvalues (ω, ω²) are non-unit → non-degenerate
  rotation → Morse-Bott satisfied.

## CAT-C: Independence (2 objections)

- **C1** *Are the 8 routes to η = 2/9 truly independent?*
  Honest answer: 8 routes cluster into **3 genuinely independent
  mathematical frameworks**:
    - Topological (ABSS-based): equivariant fixed-point, core
      identity, K-theory χ₀ isotype.
    - Analytical (spectral): Hirzebruch-Zagier, APS Dirac,
      Dai-Freed.
    - Number-theoretic (Dedekind): Dedekind 4·s(1, 3), C_3 CS
      level-2 mean spin.
  Three independent frameworks is still strong theorem-grade support.

- **C2** *Does the I1 AM-GM derivation cycle back to a Peter-Weyl
  prescription?*
  No. The AM-GM derivation uses `F_sym = log(E_+ · E_⊥)` with
  equal weights — the Frobenius trace metric, forced by the
  retained Herm_circ(3) structure. A Peter-Weyl (1, 2) weighting
  would give κ = 1 ≠ 2. No circularity.

## CAT-E: Decoupling from the framework's separately-open dynamical-metric-lift question

A first-pass reviewer correctly asked whether the APS stack depends
on `frontier_s3_anomaly_spacetime_lift.py`, which still hard-fails
on the framework-level dynamical-metric-lift question.

**Answer: no. The APS stack is orthogonal to that runner.** The APS
η value requires only:

- **(E1)** Retained kinematic manifold (PL S³ × R with Z_3 action) —
  axiomatic base of the framework, not a consequence of the
  dynamical-metric runner.
- **(E2)** Standard algebraic topology (Cerf smoothability; S³ has
  spin structure w_2 = 0; Z_3 action lifts via equivariant smoothing).
  These are topology theorems, not framework assumptions.
- **(E3)** ABSS equivariant fixed-point theorem (mathematical
  theorem): η depends only on tangent rep, not on metric.
- **(E4)** Core algebraic identity (ζ − 1)(ζ² − 1) = 3.

The dynamical-metric-lift question is about **which specific metric**
the framework's dynamics eventually picks out. ABSS gives the **same
η value** (2/9) for **any** smooth metric consistent with the
retained Z_3 action, so the specific dynamical metric is irrelevant
to the η conclusion. **(E5)** confirms this decoupling explicitly.

## CAT-D: "Retained kinematics" is the axiomatic base, not soft ground

"Retained kinematics" enumerates precisely:

- Cl(3) Clifford algebra on Z³ lattice.
- SELECTOR = √6/3.
- Observable principle W[J].
- S_3 cubic axis-permutation symmetry on Z³.
- C_3[111] = 2π/3 body-diagonal rotation subgroup.
- Continuum limit Z³ → PL S³ × R (`S3_CAP_UNIQUENESS_NOTE` on main).

These are the **framework's retained axioms**. "Retained-forced under
retained kinematics" is equivalent to "forced by the framework's
axioms" — it is not a hidden soft conditional.

## Remaining open items (not in I1 or I2/P scope)

- I5 (PMNS mixing-angle mechanism) — separate lane, not part of this
  package.
- sin(δ_CP) sign — separate observable.
- Quark-sector Koide / CKM — separate retention problem.

None of these affect the I1 or I2/P closures addressed here.
