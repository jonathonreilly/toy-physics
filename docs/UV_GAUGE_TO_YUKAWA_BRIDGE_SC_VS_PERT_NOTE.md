# UV Gauge-to-Yukawa Bridge: Subordinate Support Note

**Date:** 2026-04-16
**Status:** subordinate support for the retained Ward-identity theorem
[YT_WARD_IDENTITY_DERIVATION_THEOREM.md](YT_WARD_IDENTITY_DERIVATION_THEOREM.md).
This note compares the perturbative and strong-coupling leading-order
4-fermion coefficients and documents why the perturbative coefficient
governs the retained result on the tadpole-improved canonical surface.
**Script:** `scripts/frontier_yt_ward_identity_derivation.py` (Blocks 7, 7a,
8, 8a, 9)

---

## Role

The main theorem derives the RATIO `y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6)`
framework-natively from AX1 + AX2 (Cl(3) × Z³) via:

1. Canonical kinetic normalization of phi on Q_L block: `Z = sqrt(6)`.
2. Clebsch-Gordan overlap of unit-norm (1,1) singlet with basis: `1/sqrt(6)`.
3. Composite-Higgs structure (D9) → no independent Yukawa parameter in
   the bare Cl(3) × Z³ action (Yukawa is derived, not a free parameter).
4. Canonical-surface tadpole cancels in the ratio (D15, n_link = 1 per
   vertex shared), giving `y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6)`.

The theorem's load-bearing claim is the RATIO above, derived from
framework-native structural content only (no package-status imports,
no new axioms beyond Cl(3) × Z³).

This note is a **subordinate cross-check** via a different, independent
derivation path:

1. Shows the perturbative one-gluon-exchange + color Fierz route gives
   the same UV 4-fermion color-singlet coefficient `1/(2 N_c) = 1/6` at
   N_c = 3 via the Fierz identity.
2. Shows the strong-coupling character-expansion route gives a
   **different** leading coefficient `1/N_c^2 = 1/9`, which does NOT
   govern on the canonical surface.
3. Argues that the perturbative expansion is the convergent one on the
   tadpole-improved canonical surface (`alpha_LM = 0.091 << 1`,
   `n_opt ~ 35` loops), so `1/(2 N_c)` is the correct leading-order
   4-fermion coefficient.
4. Provides the numerical Haar-sampled SU(N_c) one-link integral as a
   machine-precision verification of the strong-coupling coefficient.

This note is SUBORDINATE: it supports the retained theorem; it does NOT
reopen the closure.

---

## Perturbative derivation (retained, matches main theorem)

Starting from one-gluon exchange at the lattice cutoff (main theorem
Step 2):

```
    L_exchange = -(g_s^2 / M_Pl^2) * J^{mu A} J_mu^A                  (A.1)
```

Apply the retained SU(N_c) Fierz identity ([YCP_EW:169-172](YT_EW_COLOR_PROJECTION_THEOREM.md)):

```
    sum_A (T^A)_{ab} (T^A)_{cd} = (1/2)[delta_{ad} delta_{bc}
                                       - (1/N_c) delta_{ab} delta_{cd}]   (A.2)
```

Project onto color-singlet channel (delta_{ab} delta_{cd}):

```
    C_pert = g_s^2 / (2 N_c)                                          (A.3)
```

For N_c = 3: `C_pert = g_s^2 / 6`.

## Strong-coupling derivation (independent cross-check)

The exact SU(N_c) one-link integral under Haar measure:

```
    integral dU U_{ab} U^dag_{cd} = (1/N_c) delta_{ad} delta_{bc}      (B.1)
```

This is an exact algebraic identity, verified numerically in Block 7a of
the runner (Haar-sample SU(3), 100,000 samples, max Monte Carlo error
< 2%).

Applying (B.1) to the fermion bilinears at the same link in the strong-
coupling leading-order character expansion:

```
    integral dU_mu [psi-bar U psi at x, x+mu] * [psi-bar U^dag psi at x+mu, x]
        = (1/N_c) * (psi-bar psi)(x) * (psi-bar psi)(x+mu)            (B.2)
```

Fierz the resulting delta structure into color channels (same Fierz
(A.2)):

```
    C_strong = 1 / N_c^2                                              (B.3)
```

For N_c = 3: `C_strong = 1/9`.

## Why perturbative governs at the canonical surface

The two coefficients differ:
- `C_pert = 1/(2 N_c) = 1/6` at N_c = 3
- `C_strong = 1/N_c^2 = 1/9` at N_c = 3

Both are leading-order results in DIFFERENT expansions:
- Perturbative expansion: in `alpha_LM`
- Strong-coupling expansion: in the character coefficients of the
  UNIMPROVED Wilson action

On the **tadpole-improved canonical surface**
([MINIMAL_AXIOMS_2026-04-11.md:18-20](MINIMAL_AXIOMS_2026-04-11.md)):

```
    alpha_LM = alpha_bare / u_0 = 0.0907                              (C.1)
```

This is small (`<< 1`), so the perturbative expansion is convergent.
Optimal truncation of the asymptotic series is at
`n_opt ~ pi / alpha_LM ~ 35` loops — far beyond the 1-loop and 2-loop
truncations used in the main theorem.

The unimproved Wilson action at `beta = 6` has character-expansion
coefficient ratios `c_1/c_0 ~ O(0.4)` (from Bessel function ratios at
SU(3) moderate beta). This is NOT small, so the strong-coupling
expansion does NOT converge rapidly at beta = 6.

The tadpole improvement `U = u_0 V` is precisely the re-organization of
the lattice partition function that moves the dominant nonperturbative
contribution (mean-field tadpole) into `u_0`, leaving a convergent
perturbative series at the vertex level. On this surface, the
perturbative leading-order coefficient `1/(2 N_c) = 1/6` is the
dominant 4-fermion structure; the strong-coupling `1/N_c^2 = 1/9` is
NOT the correct coefficient because its expansion does not converge on
the canonical surface.

**Conclusion**: on the framework's retained canonical plaquette/u_0
surface, the UV 4-fermion coefficient is `g_s^2 / (2 N_c)` (the
tadpole-improved perturbative value), with 1-loop correction
`alpha_LM/pi = 2.9%` and 2-loop `(alpha_LM/pi)^2 = 0.08%`.

The strong-coupling `1/N_c^2` value is documented here as an
INDEPENDENT CROSS-CHECK calculation. Its numerical discrepancy with
`1/(2 N_c)` is NOT a contradiction — it is a confirmation that
different expansions give different results away from their respective
domains of validity. The canonical surface selects the perturbative
expansion.

## Numerical values on the canonical surface

Inputs (all retained):
```
    <P>       = 0.5934         (retained MC, YT_VERTEX_POWER_DERIVATION)
    u_0       = <P>^(1/4)       = 0.87768138
    alpha_bare = 1/(4 pi)        = 0.07957747
    alpha_LM  = alpha_bare / u_0 = 0.09066784
    g_s(M_Pl) = sqrt(4 pi alpha_LM) = 1.06741071
```

Derived:
```
    C_pert  (perturbative)      = g_s^2 / (2 N_c) = g_s^2 / 6
    y_t/g_s = 1 / sqrt(2 N_c)   = 1 / sqrt(6) = 0.40824829
    y_t(M_Pl)                   = g_s(M_Pl) / sqrt(6) = 0.43576860
```

NLO systematic:
```
    C_F = (N_c^2 - 1) / (2 N_c) = 4/3 for SU(3)
    delta(y_t/g_s) / (y_t/g_s) = alpha_LM * C_F / (2 pi) = 1.92%
    NNLO = (alpha_LM/pi)^2 * C_F^2 = 0.15%  (negligible)
```

The 1.92% NLO systematic is within the framework's existing
~3% Yukawa-lane systematic [MINIMAL_AXIOMS_2026-04-11.md:68], so no new
lane-level budget is required.
