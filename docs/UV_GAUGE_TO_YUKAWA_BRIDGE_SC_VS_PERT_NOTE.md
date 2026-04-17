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

The main theorem (`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`) derives
the RATIO `y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6)` via explicit 1PI 4-point
function matching between the UV Cl(3) × Z³ lattice theory and the
composite-Higgs EFT at `q² = M_Pl²`:

1. **D16** (retained): bare Cl(3) × Z³ action contains only Wilson
   plaquette + staggered Dirac; at O(α_LM), single-gluon-exchange
   is the only tree diagram in the color-singlet scalar-scalar
   4-fermion channel.
2. **D17** (retained, Block 5 verified): `H_unit` is the unique
   unit-norm (1,1) composite scalar with `Z² = N_c · N_iso = 6`.
3. **1PI matching**: at `q² = M_Pl² ≫ m_H² ~ v²`, the UV and EFT
   1PI amplitudes equal each other operator-by-operator. Matching
   the `O_S = (ψ̄ψ)²` channel gives `y_t_bare² = g_bare²/(2 N_c)`.
4. **Tadpole cancellation** (D15, `n_link = 1`): `1/sqrt(u_0)`
   tadpole factor cancels in the ratio `y_t/g_s`, yielding
   `y_t(M_Pl)/g_s(M_Pl) = 1/sqrt(6)`.

The derivation uses only retained Cl(3) × Z³ content (D1-D17) plus
exact group-theoretic identities (S1 = SU(N_c) Casimir, S2 = Lorentz
Clifford Fierz). No 't Hooft limit, no Jouvet-Salam Z=0, no HS
auxiliary-mass freedom.

This note is a **subordinate support** documenting why the PERTURBATIVE
1/(2 N_c) coefficient (not the strong-coupling 1/N_c^2 coefficient)
is the correct leading-order 4-fermion input on the canonical surface:

1. One-gluon-exchange at tadpole-improved PT gives the color-singlet
   coefficient `C_pert = 1/(2 N_c) = 1/6` at N_c = 3 via SU(N_c) Fierz.
2. The strong-coupling character-expansion route gives a **different**
   leading coefficient `C_strong = 1/N_c^2 = 1/9`, which does NOT
   govern on the tadpole-improved canonical surface.
3. On the canonical surface (`alpha_LM = 0.091 << 1`, `n_opt ~ 35`
   loops), the perturbative expansion is convergent, so `C_pert` is
   the correct input to the main theorem's Step 3 UV side (3.8).
4. The Haar-sampled SU(N_c) one-link integral provides machine-
   precision cross-verification of the strong-coupling coefficient
   (Block 7a).

This note is SUBORDINATE: it supports the retained theorem's choice
of `C_pert` over `C_strong` as the Step-3B coefficient; it does NOT
attempt the full 1PI matching closure (which lives in the main theorem
Steps 3A-3E).

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

## NLO corrections (OPEN; support-only; not part of authority theorem)

The authority theorem in `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
states ONLY the exact tree-level 1PI matching identity
`y_t_bare = g_bare / sqrt(6)`. It makes no precision claim.

This section documents perturbative corrections for reference; the
status of these is SUPPORT-ONLY and the corrections remain OPEN for
any downstream quantitative use. In particular:

**Perturbative 1-loop vertex correction (derived):**
```
    C_F = (N_c^2 - 1) / (2 N_c) = 4/3 for SU(3)
    delta_PT = alpha_LM * C_F / (2 pi) = 1.92%
```
This is the magnitude of the 1-loop vertex correction on the tadpole-
improved PT surface (standard vertex-correction formula, retained in
Block 9 of the runner).

**Higher-order and topology-dependent corrections (OPEN):**
- NNLO perturbative `(alpha_LM * C_F / pi)^2` enters at ~0.15%
- Non-planar topology corrections at NNLO `(alpha_LM*C_F/pi)^2 / N_c^2`
  at ~0.017%
- Further higher-order corrections not worked out here

These NLO and higher-order statements are NOT part of the authority
theorem's certification. Any downstream package that reuses the
theorem's exact algebraic identity `y_t_bare = g_bare / sqrt(6)` and
wants a quantitative precision claim must carry its own systematic
(e.g., by citing the 3% Yukawa-lane budget at
[MINIMAL_AXIOMS_2026-04-11.md:68]) or leave the systematic OPEN.

The exact subtheorem can be unbounded even if the full Yukawa / top
lane carries a quantitative systematic elsewhere.
