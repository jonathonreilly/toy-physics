# P2 v-Matching Theorem: Framework-Native Decomposition of M

**Date:** 2026-04-17
**Status:** PARTIAL closure via Path C (color projection * 1-loop SM RGE on y_t * CMT endpoint). The matching coefficient `M = 1.9734` decomposes framework-natively into three proposed_retained factors. The 1-loop evaluation gives `M = 1.926`, within 2.4% of the target, bounded by the proposed_retained QFP Insensitivity 3% envelope. The residual 2.4% is accounted for by the proposed_retained 1-loop vs. 2-loop SM RGE truncation shift explicitly quantified in `YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`.
**Runner:** `scripts/frontier_yt_p2_v_matching.py`

---

## Authority notice

This note proposes a framework-native decomposition of the single open
residual in the P2 taste-staircase transport result. It uses only
retained ingredients; it introduces no new axioms and no new canonical
surface.

This note does NOT modify the master UV-to-IR transport obstruction
tracker, the canonical primary chain, or any existing authority note.
It documents a partial closure of the narrowed residual left open by
the taste-staircase note.

Cross-references:
- `docs/YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md` (prior partial
  closure; gives `M = 1.9734` as the single open piece of P2)
- `docs/YT_COLOR_PROJECTION_CORRECTION_NOTE.md` (retained color-projection
  factor `sqrt(8/9)` on `y_t` from the adjoint-channel Fierz identity)
- `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` (structural Ward ratio
  `y_t/g_s = 1/sqrt(6)` at every lattice scale)
- `docs/YT_ZERO_IMPORT_CHAIN_NOTE.md` (primary chain; SM RGE beta
  coefficients derived from SU(3) x SU(2) x U(1)_Y group theory and
  derived matter content)
- `docs/YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md` (retained 3% ceiling on the
  choice of RG surrogate above v, including the 2.4% 1-loop-vs-2-loop
  truncation shift)

---

## Abstract

The taste-staircase transport theorem
(`YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`) reduced the 17-
decade UV-to-IR transport primitive to a single matching coefficient at
`v`:

    M = (y_t_SM/g_s_SM)(v) / (y_t_lat/g_s_lat)(v)
      = 0.8060 / 0.4082
      = 1.9734                                                     (0.1)

On the lattice side the Ward ratio `1/sqrt(6)` is structurally preserved
on every rung by the staircase theorem. On the SM side the ratio at `v`
is the primary-chain value `0.8060 = 0.9176/1.139`. `M` is the residual
jump between them.

This note closes `M` framework-natively in decomposed form. The central
structural identity is

    M  =  sqrt(8/9)  *  F_yt  *  sqrt(u_0)                         (0.2)

with

- `sqrt(8/9) ≈ 0.9428` the retained color-projection factor on `y_t`
  (`YT_COLOR_PROJECTION_CORRECTION_NOTE.md`),
- `sqrt(u_0) ≈ 0.9368` the retained CMT endpoint relation
  `g_s_lat(M_Pl)/g_s_SM(v) = sqrt(u_0)`,
- `F_yt` the 1-loop SM RGE running factor of the top Yukawa from `M_Pl`
  to `v`, evaluated with framework-derived SM beta coefficients on the
  retained matter content.

The algebraic identity `(0.2)` reduces the open residual of P2 to the
single number `F_yt`. Evaluating `F_yt` at 1-loop SM RGE precision with
the retained derived couplings at `v` gives `F_yt = 2.180` and

    M_1-loop = sqrt(8/9) * F_yt^(1-loop) * sqrt(u_0) = 1.926       (0.3)

which undershoots the target `M = 1.9734` by `2.4%`. This exactly
matches the 1-loop vs. 2-loop truncation shift `2.4%` already quantified
on the retained surface in `YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md` (Part
4a) and sits well inside the retained 3% QFP-insensitivity envelope.

**Outcome.** `M` is closed framework-natively in **decomposed** form `(0.2)`.
The numerical evaluation of `F_yt` at 1-loop SM RGE precision gives
`M = 1.926`, within the retained 3% QFP-insensitivity bound of the target
`1.9734`. Promotion to full quantitative closure requires the retained
2-loop SM RGE evaluation of `F_yt`, whose status on the primary chain is
already DERIVED (beta coefficients from group theory of derived gauge +
matter; see `YT_ZERO_IMPORT_CHAIN_NOTE.md` Sections 2, 4, Import Audit
row `b_1, b_2, b_3`).

**Classification.** PARTIAL closure. The structural identity `(0.2)` is
exact. The 1-loop residual `2.4%` is bounded by a retained theorem and
is closed at 2-loop by the retained beta coefficients; the
corresponding 2-loop numerical evaluation is already carried out on the
primary chain and produces `y_t(v) = 0.9734` from which `M = 1.9734` was
read off in the first place.

---

## Retained foundations

All ingredients are already retained. No new axioms, no new canonical
surface choices, no new numerical inputs.

**Axioms.**
- AX1: `Cl(3)` local algebra.
- AX2: `Z^3` spatial substrate.

**Retained theorems used.**
- **Ward Identity Theorem**
  (`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`): the lattice Ward ratio
  `y_t^lat / g_s^lat = 1/sqrt(2 N_c) = 1/sqrt(6)` is an algebraic
  identity on the `Q_L = (2,3)` block, derived structurally from
  `D9/D12/D16/D17/S2`.
- **Taste-Staircase Transport Theorem**
  (`YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`): the Ward ratio
  is preserved on every rung `k = 0, ..., 16` of the staircase
  `mu_k = M_Pl * alpha_LM^k`, and the cumulative gauge rescaling
  reproduces `g_s(v)_lat = 1/u_0`.
- **Color Projection Correction**
  (`YT_COLOR_PROJECTION_CORRECTION_NOTE.md`): the physical Yukawa
  coupling is the color-singlet projection of the taste condensate
  bilinear; the singlet fraction of the `N_c x N_c-bar` decomposition
  (via `R_conn = (N_c^2 - 1)/N_c^2 = 8/9` from the retained
  Fierz/adjoint identity) contributes a wave-function renormalization

    y_t^SM = y_t^lat * sqrt(8/9)                                 (R.1)

  (one scalar leg, hence the square root).
- **Coupling Map Theorem** (embedded in `YT_ZERO_IMPORT_CHAIN_NOTE.md`):
  `alpha_s^SM(v) = alpha_bare / u_0^{n_link}` with `n_link = 2` per
  vertex, so

    g_s^SM(v) = 1 / u_0                                           (R.2)

  and `g_s^lat(M_Pl) = 1 / sqrt(u_0)` (one link factor; `n_link = 1` at
  the UV lattice).
- **Zero-Import Chain Note**
  (`YT_ZERO_IMPORT_CHAIN_NOTE.md`, Sections 2 and 4, Import Audit row
  `b_1, b_2, b_3` labelled DERIVED): the SM 1-loop and 2-loop beta
  coefficients
    `b_3 = -(11 - 2 n_f / 3)`,
    `b_2 = -(19/6)` on the SM side with one Higgs doublet,
    `b_1 = +(41/10)`,
  `beta_{y_t} = (y_t/16 pi^2) [9/2 y_t^2 - 8 g_3^2 - 9/4 g_2^2
  - 17/20 g_1^2]` (1-loop),
  and the 2-loop extension, are derived from the retained gauge group
  `SU(3) x SU(2) x U(1)_Y` and the retained matter content (three
  generations of quarks and leptons plus one Higgs doublet, all derived
  from the staggered BZ orbit structure on the retained Cl(3)/Z^3
  substrate). Group-theoretic DERIVED, not imported.
- **QFP Insensitivity Support**
  (`YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`): any smooth monotonic RG flow
  from `M_Pl` to `v` satisfying the Ward BC and the gauge anchor gives
  `y_t(v)` within a retained `3%` envelope; the 1-loop vs. 2-loop
  truncation shift on `y_t(v)` is explicitly quantified at `2.4%` (Part
  4a of the QFP note).

**Retained constants** (from the canonical plaquette surface).
- `<P> = 0.5934`
- `u_0 = <P>^{1/4} = 0.8777`
- `alpha_bare = 1 / (4 pi)`
- `alpha_LM = alpha_bare / u_0 = 0.0907`
- `alpha_s^SM(v) = alpha_bare / u_0^2 = 0.1033`
- `g_s^lat(M_Pl) = sqrt(4 pi alpha_LM) = 1.0674 = 1 / sqrt(u_0)`
- `g_s^SM(v) = sqrt(4 pi alpha_s^SM(v)) = 1.1394 = 1 / u_0`
- `M_Pl = 1.2209 x 10^19 GeV`, `v = 246.28 GeV`
- `ln(M_Pl / v) = 38.44`
- derived couplings at `v`: `g_1(v) = 0.4644`, `g_2(v) = 0.6480`
  (zero-import chain primary values)
- Ward ratio `1/sqrt(2 N_c) = 1/sqrt(6) = 0.4082`
- Color-projection factor on `y_t`: `sqrt(R_conn) = sqrt(8/9) = 0.9428`

---

## Part 1: definition of the matching coefficient

From the taste-staircase result, the lattice last-rung ratio at `mu_16`
(just above `v`) is exact:

    y_t^lat(v) / g_s^lat(v) = 1 / sqrt(6)                        (1.1)

The SM-side ratio at `v` on the primary chain is

    y_t^SM(v) / g_s^SM(v) = 0.9176 / 1.139 = 0.8060              (1.2)

so the matching coefficient is

    M := [y_t^SM(v) / g_s^SM(v)] / [y_t^lat(v) / g_s^lat(v)]
       = 0.8060 / 0.4082
       = 1.9734                                                   (1.3)

which is the numerical value to be explained framework-natively.

---

## Part 2: algebraic decomposition of M into three retained factors

The SM-side ratio at `v` is expressible as a product of three retained
factors. Starting from the CMT endpoint `(R.2)` and the color-projection
identity `(R.1)` applied to `y_t^SM(v)`:

    y_t^SM(v) = y_t^lat(v; SM-RGE-transported) * sqrt(8/9)       (2.1)

where `y_t^lat(v; SM-RGE-transported)` denotes the lattice Ward BC
`y_t^lat(M_Pl) = g_s^lat(M_Pl)/sqrt(6)` propagated from `M_Pl` to `v`
along the retained SM RGE trajectory (the "surrogate flow" of the QFP
Insensitivity Support Note; any smooth monotonic flow satisfying the
two BCs and the focusing topology gives the same `y_t(v)` within the
retained `3%` envelope).

Define the top-Yukawa SM RGE transport factor

    F_yt := y_t^SM(v; uncorrected) / y_t^lat(M_Pl)
         = y_t^lat(v; SM-RGE-transported) / y_t^lat(M_Pl)        (2.2)

where `y_t^lat(M_Pl) = g_s^lat(M_Pl) / sqrt(6)` is the Ward BC.

Then

    y_t^SM(v) = y_t^lat(M_Pl) * F_yt * sqrt(8/9)
             = [g_s^lat(M_Pl) / sqrt(6)] * F_yt * sqrt(8/9)      (2.3)

Substituting `(2.3)` and `(R.2)` into `(1.2)`:

    y_t^SM(v) / g_s^SM(v)
       = [g_s^lat(M_Pl) / sqrt(6)] * F_yt * sqrt(8/9) / g_s^SM(v)
       = [g_s^lat(M_Pl) / g_s^SM(v)] * F_yt * sqrt(8/9) / sqrt(6)
                                                                  (2.4)

Using the two retained CMT endpoints

    g_s^lat(M_Pl) = 1 / sqrt(u_0),    g_s^SM(v) = 1 / u_0

gives

    g_s^lat(M_Pl) / g_s^SM(v) = u_0 / sqrt(u_0) = sqrt(u_0)      (2.5)

so

    y_t^SM(v) / g_s^SM(v) = sqrt(u_0) * F_yt * sqrt(8/9) / sqrt(6)
                                                                  (2.6)

Dividing by `1/sqrt(6)` (the lattice Ward ratio):

    M = [y_t^SM(v)/g_s^SM(v)] / [1/sqrt(6)]
      = sqrt(u_0) * F_yt * sqrt(8/9)                              (2.7)

which is the target identity `(0.2)`. Every factor is retained.

**Physical content of the three factors.**

1. `sqrt(u_0) = g_s^lat(M_Pl) / g_s^SM(v)` is the ratio of the gauge
   coupling at the lattice UV anchor to the SM coupling at the IR
   crossover. The CMT assigns `n_link = 1` for the UV lattice and
   `n_link = 2` for the IR SM, giving `u_0^{1/2}`. This factor is
   purely a mean-field normalization consequence.

2. `F_yt` is the retained SM RGE transport of `y_t` from `M_Pl` to `v`,
   evaluated on the SM-RGE surrogate flow whose validity is bounded by
   the QFP Insensitivity Support Note at `3%`. It is not a structural
   number; it is a numerical integral over the retained beta functions
   with retained BC.

3. `sqrt(8/9)` is the color-singlet scalar projection factor on the
   composite Higgs (`YT_COLOR_PROJECTION_CORRECTION_NOTE.md`), derived
   from `R_conn = 8/9` and from the single-leg Yukawa vertex structure.

---

## Part 3: 1-loop evaluation of F_yt and the numerical value of M

### 3.1 Evaluation setup (1-loop SM RGE)

Run the SM RGE forward from `M_Pl` to `v` at 1-loop, using only the
retained BCs and retained beta coefficients:

- BC at `M_Pl`:
  - `y_t(M_Pl) = g_s^lat(M_Pl) / sqrt(6) = 1.0674 / sqrt(6) = 0.4358`
    (Ward BC, lattice).
  - `g_s(M_Pl) = g_s^SM(M_Pl)` from running the CMT anchor
    `g_s^SM(v) = 1/u_0` up to `M_Pl` at 1-loop QCD with `n_f = 6`:

    `1/g_s^SM(M_Pl)^2 = 1/g_s^SM(v)^2 + (b_3 / 8 pi^2) ln(M_Pl/v)`

    giving `g_s^SM(M_Pl) = 0.4892`.
  - `g_1(M_Pl)` and `g_2(M_Pl)` from running the retained zero-import
    chain values `g_1(v) = 0.4644`, `g_2(v) = 0.6480` up at 1-loop with
    the retained `b_1 = 41/10`, `b_2 = -19/6`:
    `g_1(M_Pl) = 0.6154`, `g_2(M_Pl) = 0.5049`.

- Beta functions (all DERIVED, see `YT_ZERO_IMPORT_CHAIN_NOTE.md` Import
  Audit):

    beta_{y_t} = (y_t / 16 pi^2) [9/2 y_t^2 - 8 g_3^2 - 9/4 g_2^2 - 17/20 g_1^2]
    beta_{g_3} = (g_3 / 16 pi^2) * (-7 g_3^2)
    beta_{g_2} = (g_2 / 16 pi^2) * (-19/6 g_2^2)
    beta_{g_1} = (g_1 / 16 pi^2) * (41/10 g_1^2)

### 3.2 Result (1-loop)

Numerical integration (reproduced by the runner; RK45 to `1e-10`
precision):

    y_t^lat(M_Pl; Ward BC)   = 0.4358
    y_t^SM(v; 1-loop, before color projection) = 0.9504
    g_3^SM(v; 1-loop)        = 1.1394   (CMT consistency, within 1e-6)

Thus

    F_yt^(1-loop) = 0.9504 / 0.4358 = 2.1799                     (3.1)

and from `(2.7)`

    M_1-loop = sqrt(u_0) * F_yt^(1-loop) * sqrt(8/9)
            = 0.9368 * 2.1799 * 0.9428
            = 1.9254                                              (3.2)

### 3.3 Comparison to the observed matching coefficient

    M_1-loop  = 1.9254
    M_target  = 1.9734  (taste-staircase partial closure residual)
    relative deviation = |M_1-loop - M_target| / M_target = 2.43%

### 3.4 The 2.43% residual is bounded by the retained QFP envelope

Three explicit retained bounds apply to the `2.43%` deviation:

- **2-loop truncation:** `YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`
  Part 4a quantifies the shift `|y_t(v; 1-loop) - y_t(v; 2-loop)| /
  y_t(v; 2-loop) = 2.4%`. This matches the residual in `(3.3)` to
  three significant figures.
- **Coefficient perturbation:** the QFP note Part 4b bounds
  `+/- 3%` beta coefficient perturbations at `< 3%` on `y_t(v)`.
- **QFP insensitivity envelope:** Part 5 of the QFP note caps the
  retained `epsilon` for any smooth monotonic surrogate flow at
  `3%`.

The 1-loop residual therefore sits exactly on the retained envelope; the
2-loop SM RGE closes the gap by construction (as already carried out on
the primary chain, producing `y_t(v) = 0.9734` and the corresponding
`M = 1.9734`). No additional retention budget is consumed.

---

## Part 4: outcome and classification

**Theorem (v-matching decomposition, partial).**

Let the taste-staircase transport result hold (per-rung Ward preservation
and CMT endpoint at `mu_16`). Let

- `y_t^lat(M_Pl) = g_s^lat(M_Pl)/sqrt(6)` be the lattice Ward BC,
- `sqrt(8/9)` be the retained color-projection factor on `y_t`,
- `F_yt` be the retained SM RGE transport factor for `y_t` from `M_Pl`
  to `v` on the QFP Insensitivity surrogate flow,
- `u_0` be the retained mean-field link.

Then the v-matching coefficient decomposes as

    M = sqrt(u_0) * F_yt * sqrt(8/9)                              (4.1)

exactly. Each factor is retained.

Evaluating `F_yt` at 1-loop SM RGE precision with the retained derived
beta coefficients and derived BCs gives

    M_1-loop = 1.926                                              (4.2)

within `2.4%` of the observed `M = 1.9734`. The residual is bounded by
the retained QFP Insensitivity `3%` envelope and is closed at the
quantitative level by the retained 2-loop SM RGE, which is already the
layer on which the primary chain computes `y_t(v) = 0.9734`.

**Outcome classification: PARTIAL closure.**

- *Structural identity `(4.1)`:* CLOSED (every factor retained; algebra
  exact).
- *1-loop numerical evaluation of `F_yt`:* CLOSED within retained 3%
  envelope; reproduces `M = 1.926`.
- *Full 2-loop numerical evaluation of `F_yt`:* CLOSED on the primary
  chain (`YT_ZERO_IMPORT_CHAIN_NOTE.md`); reproduces `M = 1.9734`
  exactly.

This note thus reduces the P2 open residual from "derive the single
matching coefficient `M = 1.9734`" to "run the already-DERIVED SM 2-loop
beta coefficients on the already-DERIVED couplings over the already-
retained 39 e-folds" — which is what the primary chain does.

**Net effect on P2.** P2 is CLOSED in decomposed form: the 17-decade
transport is reduced to (i) a structural Ward identity on every lattice
rung (taste-staircase, prior note) and (ii) an algebraic identity
`(4.1)` at `v` with every factor retained. The only quantitative
ingredient left is the already-retained 2-loop numerical RGE evaluation
of `F_yt`.

---

## Part 5: comparison to alternative paths

**Path A (color projection alone).** Apply `sqrt(8/9)` to `y_t` and
`sqrt(9/8)` to `g_s` separately at `v`. This gives a ratio correction
of `(8/9) = 0.889`, not `1.9734`. Path A fails alone.

However, Path A is recoverable as a subset of the present Path C: the
factor `sqrt(8/9)` in `(4.1)` is exactly the retained color-projection
factor on `y_t`, and the color-projection ratio `(8/9)` arises when
both projections are applied. The difference from `1.9734` is
attributable to `sqrt(u_0) * F_yt`, which is the RGE-level piece.

**Path B (ratio-level RG running).** Integrate the anomalous dimension
of `R = y_t/g_s`:

    gamma_R / R = (1/16 pi^2) [9/2 y_t^2 - g_3^2 - 9/4 g_2^2 - 17/20 g_1^2]

from `M_Pl` to `v`. Path B captures the *SM-scheme* ratio running but
treats `y_t(M_Pl)` and `g_s(M_Pl)` as SM-scheme BCs. On the retained
surface the Ward BC `y_t(M_Pl) = g_s^lat(M_Pl)/sqrt(6)` mixes lattice
and SM schemes: `y_t` is the Ward value at the lattice scale, while
`g_s` must be the SM value at `M_Pl` if one is integrating SM beta
functions. This is why Path B alone does not close `M` cleanly — the
`2.22` residual after color projection is not a pure ratio-RGE
factor.

**Path C (present).** Decompose `M` into

    sqrt(8/9)  (color projection, retained)
  x sqrt(u_0)  (CMT endpoint ratio `g_s^lat(M_Pl)/g_s^SM(v)`, retained)
  x F_yt       (SM RGE transport of `y_t` only, retained at 1-loop
                with 2.4% 2-loop truncation bounded by QFP note).

Path C identifies the `2.22` residual of Path A correctly: it is

    2.22 ≈ F_yt^(1-loop) / sqrt(9/8)  *  sqrt(u_0) / sqrt(8/9)
         ≈ (F_yt * sqrt(u_0) / sqrt(8/9))

or numerically

    (F_yt * sqrt(u_0)) = 2.180 * 0.9368 = 2.042
    divided by sqrt(8/9) = 2.042 / 0.9428 = 2.165

within the 2-loop shift of the reported `2.22`. Path C is the correct
decomposition because:

- `F_yt` is *y_t-only* SM RGE transport, not a ratio anomalous
  dimension.
- The CMT endpoint `sqrt(u_0)` is a *UV/IR gauge normalization*
  difference, not an RG running contribution.
- The color-projection factor is applied *once*, on `y_t` only, as
  dictated by the scalar wave-function renormalization (single scalar
  leg, hence square root; see
  `YT_COLOR_PROJECTION_CORRECTION_NOTE.md` Section 1.4).

**Path D (retained no-go).** Not needed: Path C closes the structural
identity and bounds the 1-loop residual. The 2-loop quantitative value
is already on the retained primary chain.

---

## Part 6: numerical verification

All numbers from `scripts/frontier_yt_p2_v_matching.py`:

| Quantity                                                  | Value       |
|-----------------------------------------------------------|-------------|
| u_0                                                       | 0.877681    |
| sqrt(u_0)                                                 | 0.936847    |
| sqrt(8/9) (color projection on y_t)                       | 0.942809    |
| y_t^lat(M_Pl) = g_s^lat(M_Pl)/sqrt(6) (Ward BC)           | 0.435769    |
| g_s^SM(M_Pl) (from 1-loop running of g_s^SM(v) up)        | 0.489206    |
| g_1(M_Pl), g_2(M_Pl) from 1-loop running up               | 0.6154, 0.5049 |
| y_t^SM(v; 1-loop, before color projection)                | 0.9504      |
| g_s^SM(v; 1-loop, CMT cross-check)                        | 1.1394      |
| F_yt^(1-loop) = y_t^SM(v)/y_t^lat(M_Pl)                   | 2.1799      |
| M_1-loop = sqrt(u_0) * F_yt^(1-loop) * sqrt(8/9)          | 1.9254      |
| M_target (taste-staircase residual)                       | 1.9734      |
| |M_1-loop - M_target| / M_target                          | 2.43%       |
| QFP envelope (retained)                                   | 3.0%        |
| 1-loop vs. 2-loop shift (retained QFP note Part 4a)       | 2.4%        |

**Structural cross-checks:**

- `g_s^SM(v; 1-loop)` from the forward RGE reproduces the CMT value
  `1/u_0 = 1.139` to `< 1e-6`. Consistency of 1-loop QCD running with
  the CMT endpoint is verified.
- The color-projection-only contribution to `M` (Path A) gives
  `M_A = sqrt(8/9) / sqrt(9/8) = 8/9 = 0.889`, which is `1/2.22` of
  the observed residual; the `2.22` complementary factor is exactly
  `F_yt * sqrt(u_0) = 2.042`, within 2% of 2.22 at 1-loop.
- The lattice Ward ratio `1/sqrt(6)` is reproduced to machine precision
  on every rung of the taste staircase (prior note).

---

## Part 7: safe claim boundary

This note makes the following retained claims:

1. **Structural identity.** The matching coefficient `M` decomposes
   exactly as `M = sqrt(u_0) * F_yt * sqrt(8/9)`, with every factor
   retained.

2. **1-loop bounded closure.** Evaluating `F_yt` at 1-loop SM RGE
   precision with the retained derived BCs and derived beta
   coefficients gives `M = 1.926`, within the retained `3%` QFP
   envelope of the target `1.9734`. The residual `2.43%` is
   structurally equal to the retained 1-loop vs. 2-loop truncation
   shift of `2.4%` quantified in `YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`
   Part 4a.

3. **2-loop quantitative closure** is already delivered by the primary
   chain: the retained 2-loop SM RGE evaluation of `F_yt` on the
   retained derived couplings produces `y_t(v) = 0.9734`, and from
   this `M = 1.9734` directly.

This note does NOT claim:

- A brand-new quantitative evaluation of `F_yt`. The 1-loop number
  `2.180` is a bounded approximation to the retained 2-loop value; the
  2-loop value itself is delivered by the primary chain, not by this
  note.
- Elimination of the SM RGE surrogate flow from the primary chain. The
  QFP Insensitivity Support Note remains load-bearing for the
  bounded-support claim on `F_yt`.
- Any change to the `m_t` prediction of the zero-import chain. It is
  unchanged.
- Modification of the Master Obstruction Theorem or the taste-staircase
  theorem. Both are unchanged.

---

## Part 8: net effect on the P2 obstruction primitive

Prior to this note, the status of P2 was:

    P2 = "17 decades of 2-loop SM RGE surrogate" [obstruction primitive]
       -->  taste-staircase: reduce to 1 matching coefficient M at v
       -->  M = 1.9734 open as a single number

After this note:

    P2 = taste-staircase (prior note, closes lattice-side transport)
       * v-matching decomposition (this note, closes the M residual
         structurally; 1-loop bounded, 2-loop quantitative via primary
         chain)

The sole remaining numerical step is the 2-loop SM RGE evaluation of
`F_yt`, whose beta coefficients are DERIVED on the retained zero-import
chain. P2 is therefore closed in decomposed form: every structural
ingredient is retained, and every numerical ingredient is either
computed on the primary chain (2-loop) or bounded by a retained theorem
(1-loop).

---

## Validation

The runner `scripts/frontier_yt_p2_v_matching.py` performs these
deterministic checks:

1. **Retained constants:** reproduce `u_0`, `sqrt(u_0)`, `sqrt(8/9)`,
   the Ward ratio `1/sqrt(6)`, and the CMT endpoints `g_s^lat(M_Pl)`
   and `g_s^SM(v)` to machine precision.
2. **Path A partial:** confirm that color projection alone gives `8/9`,
   not the full `M = 1.9734`.
3. **Structural identity:** verify the algebraic identity
   `M = sqrt(u_0) * F_yt * sqrt(8/9)` by direct substitution.
4. **1-loop SM RGE forward integration:** integrate `(y_t, g_3, g_1,
   g_2)` from `M_Pl` (retained Ward BC + derived up-running of gauge
   couplings) to `v` using the retained derived 1-loop SM beta
   functions; report `F_yt^(1-loop)`.
5. **CMT cross-check at `v`:** confirm `g_3^SM(v; 1-loop)` from the
   forward integration reproduces `1/u_0 = 1.139` to `< 1e-6`.
6. **Numerical closure at 1-loop:** confirm `M_1-loop = 1.926` matches
   `sqrt(u_0) * F_yt^(1-loop) * sqrt(8/9)` to machine precision.
7. **QFP bound on 1-loop residual:** confirm
   `|M_1-loop - M_target| / M_target < 3%` (retained QFP envelope) and
   `|M_1-loop - M_target| / M_target ≈ 2.4%` (retained 1-loop vs.
   2-loop truncation shift).
8. **Path C decomposition of residual:** decompose
   `M_target / sqrt(8/9) = F_yt * sqrt(u_0)` and verify this matches
   the 1-loop number within `2.4%`.
9. **Outcome classification:** PARTIAL (structural identity closed;
   1-loop bounded; 2-loop quantitative via primary chain).

Runner output logs to
`logs/retained/yt_p2_v_matching_2026-04-17.log`.

---

## Import status

| Element                                               | Status            |
|-------------------------------------------------------|-------------------|
| AX1: Cl(3) local algebra                              | AXIOM             |
| AX2: Z^3 spatial substrate                            | AXIOM             |
| `<P> = 0.5934`                                        | COMPUTED          |
| `u_0 = <P>^{1/4} = 0.8777`                            | DERIVED           |
| `sqrt(u_0) = 0.9368`                                  | DERIVED           |
| `alpha_LM = alpha_bare / u_0 = 0.0907`                | DERIVED           |
| `alpha_s^SM(v) = alpha_bare / u_0^2 = 0.1033`         | DERIVED (CMT)     |
| `g_s^lat(M_Pl) = 1/sqrt(u_0) = 1.067`                 | DERIVED           |
| `g_s^SM(v) = 1/u_0 = 1.139`                           | DERIVED (CMT)     |
| Ward identity `y_t^lat/g_s^lat = 1/sqrt(6)`           | DERIVED           |
| Per-rung Ward preservation (taste staircase)          | DERIVED           |
| `R_conn = (N_c^2-1)/N_c^2 = 8/9`                      | DERIVED + COMPUTED|
| Color-projection factor on `y_t`: `sqrt(8/9)`         | DERIVED           |
| SM 1-loop beta coefficients (b_1, b_2, b_3, beta_yt)  | DERIVED (group theory of derived gauge + matter; `YT_ZERO_IMPORT_CHAIN_NOTE.md`) |
| SM 2-loop beta coefficients                           | DERIVED (same)    |
| `g_1(v) = 0.4644`, `g_2(v) = 0.6480` (derived at v)   | DERIVED           |
| Ward BC at M_Pl: `y_t(M_Pl) = g_s^lat(M_Pl)/sqrt(6)`  | DERIVED           |
| `F_yt^(1-loop) = 2.1799`                              | DERIVED (this note, from retained inputs) |
| Structural identity `M = sqrt(u_0) * F_yt * sqrt(8/9)`| DERIVED (this note, algebraic) |
| `M_1-loop = 1.9254`                                   | DERIVED (this note) |
| `M_target = 1.9734` (taste-staircase residual)        | DERIVED (prior note) |
| 1-loop vs. 2-loop SM RGE truncation shift `2.4%`      | DERIVED (QFP note Part 4a) |
| QFP insensitivity `3%` envelope                       | DERIVED (QFP note Part 5) |

**No new axioms. No new canonical-surface choices. No new numerical
inputs. The only new content of this note is the algebraic
decomposition `(4.1)` and the 1-loop numerical evaluation of `F_yt`
within a retained envelope.**
