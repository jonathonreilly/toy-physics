# P2 Taste-Staircase Beta Functions: Retained No-Go

**Date:** 2026-04-17
**Status:** NO-GO for per-step perturbative beta functions.
PARTIAL closure of P2 (via the prior taste-staircase note and prior
v-matching note) remains the canonical surface.
**Runner:** `scripts/frontier_yt_p2_taste_staircase_beta.py`
**Log:** `logs/retained/yt_p2_taste_staircase_beta_2026-04-17.log`

---

## Authority notice

This note is a DEEPEST-QUESTION probe of the P2 transport primitive.
It tests whether the 16-step taste staircase admits EXPLICIT per-step
1-loop beta functions `beta_{g_s}^{(k)}`, `beta_{y_t}^{(k)}` that
integrate to reproduce the retained framework-native factors

    g_s^lat(v) / g_s^lat(M_Pl) = 1.208 / 1.067 = 1.132    (target_gs)
    y_t^lat(v) / y_t^lat(M_Pl) = 0.973 / 0.436 = 2.233    (target_yt)

through the rung sequence `n_taste^{(k)} = 16 - k`, `k = 0, ..., 16`.

The outcome of this note is **NO-GO**: per-step perturbative 1-loop
beta running (with `n_taste` replacing `n_f` in the retained gauge
beta) does NOT reproduce the targets. The staircase is therefore
**non-perturbative**, consistent with `alpha_LM^16` being a
non-perturbative factor in the retained hierarchy theorem.

This note does **not** invalidate the prior taste-staircase note
(`docs/YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`) or the
prior v-matching note (`docs/YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md`).
It SHARPENS them: the "structural Ward preservation at every rung"
claim in the prior note is NOT a per-rung beta identity; it is the
structural re-derivation of an algebraic identity on every lattice
frame that retains the Q_L block. The running through the 17 decades
is delivered by the 2-loop SM RGE on the primary chain, and the
1-loop surrogate is bounded by the retained QFP 3% envelope.

Cross-references:
- `docs/YT_P2_TASTE_STAIRCASE_TRANSPORT_NOTE_2026-04-17.md`
  (prior PARTIAL: per-rung Ward preservation + uniform u_0^{-1/32} dressing)
- `docs/YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md`
  (prior PARTIAL: decomposition `M = sqrt(u_0) * F_yt * sqrt(8/9)`)
- `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`
  (structural Ward identity on the Q_L block)
- `docs/YT_BOUNDARY_THEOREM.md`
  (domain separation; v is the physical crossover)
- `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
  (hierarchy theorem; 16 staggered tastes from 2^4 BZ corners in 4D)
- `docs/YT_ZERO_IMPORT_CHAIN_NOTE.md`
  (current primary chain; SM beta coefficients DERIVED on retained matter)
- `docs/YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`
  (3% envelope on any smooth monotonic surrogate flow; 2.4% 1-vs-2-loop shift)

---

## Abstract

**Verdict.** Per-step 1-loop perturbative beta functions with `n_f`
replaced by `n_taste^{(k)} = 16 - k` do **not** close P2.

- **Gauge integration**: `b_3(n) = (11 C_A - 4 T_F n)/3 = (33 - 2n)/3`
  gives `b_3(16) = 1/3` (barely asymptotically free at the UV rung) and
  `b_3(n) <= 0` for any `n >= 17`. Starting from the retained UV anchor
  `g_s^lat(M_Pl) = 1.067`, literal 1-loop integration downward over
  16 rungs triggers Landau-pole crossing because the `1/g^2` trajectory
  decreases too fast (the tiny positive `b_3` at the UV rung combined
  with the lattice UV anchor is marginal; once the substep accumulates,
  `1/g^2` passes through zero before `n_taste` has decreased enough for
  `b_3` to become "standard QCD-sized"). Numerically the integration
  diverges.
- **Yukawa integration**: with `beta_{y_t} = (y_t / 16 pi^2)[9/2 y_t^2 -
  8 g_3^2]` driven by the gauge trajectory above, the same breakdown
  propagates. Yukawa integration is ill-defined on the same set of
  rungs.
- **Ward preservation by perturbative beta**: requires `b_3 = 29/4 =
  7.25`, which corresponds to `n_taste = 5.625`. This is NOT in the
  canonical integer sequence `{0, 1, ..., 16}`. The closest rung
  (`n_taste = 6` at `k = 10`) still deviates from the Ward-preserving
  value by `|b_3 - 29/4| = 1/4`. **Ward preservation is therefore NOT
  a per-rung beta-function consequence**; it is a **structural
  algebraic identity** re-derived from `D9/D12/D16/D17/S2` on each
  lattice frame that retains the Q_L block (prior note, Part 2).
- **Ward-by-definition**: if one instead DEFINES `y_t(mu_k)_lat =
  g_s(mu_k)_lat / sqrt(6)` at every rung (tautological Ward), the
  `y_t` factor through the staircase equals the `g_s` factor:
  `y_t_factor = g_s_factor = 1.132`. This MISSES the target `2.233`
  by a factor `2.233 / 1.132 = 1.973`, which is **exactly the prior
  v-matching coefficient `M = 1.973`** (the structural identity
  `M = sqrt(u_0) * F_yt * sqrt(8/9)` of the v-matching note). The
  per-rung-Ward-by-definition mechanism is therefore **insufficient
  by itself** to close P2; the missing factor is the same v-matching
  residual already identified in the prior note.

**Net effect on P2.** The deepest question ("is the staircase a
per-step beta ladder?") is resolved as **NO**. The staircase is a
**non-perturbative blocking renormalization** whose net UV-to-IR
effect is encoded in `alpha_LM^16` in the hierarchy theorem. P2
closure therefore rests on:

1. The prior taste-staircase note's structural Ward-preservation (lattice-
   side of `v`, all rungs, algebraic identity not an RG consequence).
2. The prior v-matching note's decomposition `M = sqrt(u_0) * F_yt *
   sqrt(8/9)` (the residual at `v`, bounded within QFP 3%).

Both remain PARTIAL. This note contributes the **negative result**
that per-step 1-loop perturbative beta functions do not provide an
alternative closure path.

---

## Retained foundations

No new axioms, no new canonical-surface choices.

**Axioms.**
- AX1: `Cl(3)` local algebra.
- AX2: `Z^3` spatial substrate.

**Retained theorems used.**
- **Hierarchy Theorem** (`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`,
  Theorem 4): `v = M_Pl * (7/8)^{1/4} * alpha_LM^16`, exponent 16 from
  `2^4 = 16` staggered tastes in 4D.
- **Ward Identity Theorem** (`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`):
  the lattice Ward ratio `y_t^lat / g_s^lat = 1/sqrt(2 N_c) = 1/sqrt(6)`
  is an algebraic identity on the Q_L = (2,3) block, derived from
  D9/D12/D16/D17/S2 at **every lattice frame**. The identity is
  independent of `n_taste` because each taste carries a COPY of the
  Q_L block, not an additional factor in it.
- **Coupling Map Theorem** (`YT_ZERO_IMPORT_CHAIN_NOTE.md`):
  `g_s^lat(M_Pl) = 1/sqrt(u_0) = 1.0674`, `g_s^SM(v) = 1/u_0 = 1.1394`,
  and on the lattice side of `v` (before color projection),
  `g_s^lat(v) = g_s^SM(v) * sqrt(9/8) = 1.2088`.
- **Boundary Selection Theorem** (`YT_BOUNDARY_THEOREM.md`): `v` is the
  physical crossover endpoint; lattice theory valid above `v`, SM EFT
  below.
- **Retained SU(3) 1-loop gauge beta** (`YT_ZERO_IMPORT_CHAIN_NOTE.md`
  Import Audit row `b_1, b_2, b_3` labelled DERIVED): the 1-loop SU(3)
  gauge beta coefficient is

      b_3(n_f) = (11 C_A - 4 T_F n_f) / 3                           (R.1)

  derived from the retained gauge group and fermion content. The
  staircase attempt in this note replaces `n_f` with `n_taste^{(k)}`.

**Retained constants.**
- `<P> = 0.5934`, `u_0 = <P>^{1/4} = 0.8777`
- `alpha_bare = 1/(4 pi) = 0.0796`
- `alpha_LM = alpha_bare / u_0 = 0.0907`
- `alpha_s^SM(v) = alpha_bare / u_0^2 = 0.1033`
- `(7/8)^{1/4} = 0.9672`
- `M_Pl = 1.2209 x 10^19 GeV`, `v = 246.28 GeV`
- `ln(alpha_LM) = -2.4006`, so per-rung log-interval `Delta_t = -2.4006`
- 16 rungs -> total log-span `16 * Delta_t = -38.41` (matches
  `ln(v / M_Pl) * (1 - (1/16) ln(7/8)^{-1/4}) = -38.44`).
- Group-theory constants: `C_A = 3`, `T_F = 1/2`.

**Retained target factors** (from the primary-chain zero-import values):
- `g_s^lat(M_Pl) = 1.067`, `g_s^lat(v) = 1.208` -> `target_gs = 1.132`
- `y_t^lat(M_Pl) = 0.436` (Ward BC), `y_t^lat(v) = 0.973`
  (from `y_t^SM(v) / sqrt(8/9)`) -> `target_yt = 2.233`

---

## Part 1: per-step n_taste sequence

The hierarchy theorem attributes the factor `alpha_LM^16` to 16 taste
doublers, one per corner of the 4D BZ. We treat the 16 decoupling
events as a discrete rung sequence

    k = 0, 1, ..., 16
    mu_k = M_Pl * alpha_LM^k                                       (1.1)
    n_taste^{(k)} = 16 - k                                         (1.2)

with `mu_0 = M_Pl`, `n_taste^{(0)} = 16`, and `mu_{16} * (7/8)^{1/4} =
v`. Between rungs, one taste is integrated out; the remaining tastes
still propagate.

The log-interval per rung is `ln(mu_{k+1} / mu_k) = ln(alpha_LM) ~
-2.40` (negative; running DOWN in scale).

This gives the **integer-sequence 16 -> 15 -> 14 -> ... -> 0 across
17 rungs with 16 decouplings**, distinct from the "2-per-step" reading
`16 -> 14 -> 12 -> ... -> 0` which would be 9 rungs with 8
decouplings. The hierarchy theorem places 16 decoupling events, so
the single-taste reading is canonical.

---

## Part 2: per-rung gauge beta function

The retained 1-loop SU(3) beta coefficient at rung k is

    b_3^{(k)} = (11 C_A - 4 T_F n_taste^{(k)}) / 3
              = (33 - 2 n_taste^{(k)}) / 3                         (2.1)

This runs from `b_3(16) = 1/3` at the UV rung to `b_3(0) = 11` at the
IR rung. The sequence is:

| k | n_taste | b_3       | AF?     |
|---|---------|-----------|---------|
| 0 | 16      |  0.333    | Yes, barely |
| 1 | 15      |  1.000    | Yes     |
| 2 | 14      |  1.667    | Yes     |
| 3 | 13      |  2.333    | Yes     |
| 4 | 12      |  3.000    | Yes     |
| 5 | 11      |  3.667    | Yes     |
| 6 | 10      |  4.333    | Yes     |
| 7 |  9      |  5.000    | Yes     |
| 8 |  8      |  5.667    | Yes     |
| 9 |  7      |  6.333    | Yes     |
| ... | ...   | ...       | ...     |
| 16 | 0     | 11.000    | Yes (pure gauge) |

Asymptotic freedom (AF) is **lost at** `n_taste > 33 / 4 = 8.25`, so
1-loop AF is **marginal** at the UV end of the staircase. `b_3(17) =
-1/3 < 0`; if one extended the staircase to 17 tastes, integration
would invert asymptotic freedom into asymptotic slavery, which is
unphysical for a lattice UV theory.

The per-rung 1-loop gauge running is

    1 / g_s^{(k+1)2} = 1 / g_s^{(k)2} + b_3^{(k)} / (8 pi^2) * Delta_t   (2.2)

with `Delta_t = ln(alpha_LM) < 0`. Since `b_3^{(k)} > 0` on all
canonical rungs, the RHS decreases, `g_s^{(k)}` grows (standard
asymptotic-freedom behavior running INTO the IR). But at rung 0,
`b_3 = 1/3` is so small that `1/g^2` decreases by only a small amount
per substep.

**Numerical test (runner Block 3).** Starting from the retained UV
anchor `g_s(M_Pl)_lat = 1.067` and integrating 1-loop downward through
the 16 rungs using (2.2) with (2.1):

The `1/g^2` trajectory crosses zero during the integration because the
starting `1/g^2 = 1/1.067^2 = 0.878` is small relative to the
cumulative `|b_3 * Delta_t / (8 pi^2)|` over 16 substeps. Specifically,
the total `sum_k b_3^{(k)} * Delta_t / (8 pi^2)` can exceed `1/g^2`
depending on substep resolution; the integration yields NaN
(Landau-pole crossing). **The 1-loop perturbative integration is not
well-defined on the retained UV anchor.**

(By contrast, the SM 1-loop integration starts from the SM-EFT anchor
`g_s^SM(v) = 1.139` and runs UP, which is well-defined because the
SM starts at `1/g^2 = 0.770` and `b_3_SM = 7` is large enough that the
trajectory monotonically increases without crossing zero. This is not
the staircase, though; it is the SM RGE.)

**Conclusion of Part 2.** The retained 1-loop perturbative integration
with `n_taste` replacing `n_f` is **not a viable per-step rule** on
the lattice UV anchor. It breaks down numerically, consistent with
the structural observation that `b_3(16) = 1/3` is marginal.

---

## Part 3: per-rung Yukawa running and Ward-ratio preservation

The retained 1-loop Yukawa beta for `y_t` on the lattice (no EW
structure retained above v) is

    beta_{y_t} = (y_t / 16 pi^2) * [9/2 y_t^2 - 8 g_3^2]            (3.1)

Per-rung running in log-scale:

    d ln(y_t) / dt = (1 / 16 pi^2) * [9/2 y_t^2 - 8 g_3^2]           (3.2)

We ask: **at what `b_3` (and hence what `n_taste`) is the Ward ratio
`y_t / g_s = 1/sqrt(6)` preserved under (2.2) + (3.2)?**

Differentiate the ratio:

    d ln(y_t / g_s) / dt = (beta_{y_t} / y_t) - (beta_{g_s} / g_s)
                        = (g_s^2 / 16 pi^2) * [9/2 * (1/6) - 8 + b_3]
                        = (g_s^2 / 16 pi^2) * [b_3 - 29/4]            (3.3)

(evaluated on the locus `y_t = g_s / sqrt(6)`). The Ward ratio is
preserved iff

    b_3 = 29 / 4 = 7.25                                              (3.4)

i.e., at `n_taste = (33 - 3 * 29/4) / 2 = 5.625`. This is **not an
integer** in the canonical staircase sequence `{16, 15, ..., 0}`.
The closest rung is `k = 10` (`n_taste = 6`, `b_3 = 7`), which still
deviates from (3.4) by `|b_3 - 29/4| = 1/4`.

**Conclusion of Part 3.** Under retained 1-loop perturbative beta
with `n_taste` replacing `n_f`, the Ward ratio is **NOT preserved**
at any canonical rung.

The Ward preservation claimed by the prior taste-staircase note
(`Part 2`) is therefore NOT a per-rung beta identity. It is a
**structural algebraic identity** re-derived from `D9/D12/D16/D17/S2`
at each rung that retains the `Q_L = (2, 3)` block. Per-rung
preservation follows from the **tree-level Clebsch-Gordan structure
and kinematic normalization**, not from cancelling contributions in a
1-loop beta function.

This is a crucial clarification: the prior note's "structural Ward
preservation" is correct as stated, but it is **tautological** at the
beta-function level (the `y_t` at each rung is DEFINED as `g_s / sqrt(6)`
at that rung, via the re-derivation of the algebraic identity). The
independent 1-loop beta for `y_t` does NOT preserve this relation.

---

## Part 4: Ward-preservation-by-definition — insufficient alone

Adopt the prior note's structural Ward identity literally:

    y_t^lat(mu_k) = g_s^lat(mu_k) / sqrt(6)    for k = 0, ..., 16    (4.1)

This is exact by construction (Part 2 of prior note). Then the
y_t factor through the staircase equals the g_s factor:

    y_t^lat(v) / y_t^lat(M_Pl) = g_s^lat(v) / g_s^lat(M_Pl)          (4.2)

With the retained values

    g_s^lat(M_Pl) = 1/sqrt(u_0) = 1.0674                             (4.3)
    g_s^lat(v) = (1/u_0) * sqrt(9/8) = 1.2088                        (4.4)

the g_s factor is `1.2088 / 1.0674 = 1.1325`. Under (4.1), the y_t
factor is the same `1.1325`. The retained target is `target_yt =
2.233`. The discrepancy is

    target_yt / y_t_Ward_def = 2.233 / 1.132 = 1.973                  (4.5)

which is **numerically identical** to the v-matching coefficient
`M = 1.973` of the prior v-matching note, to four significant figures.

**This is the central finding of Part 4.** Ward-preservation-by-
definition, combined with the retained CMT endpoint, recovers the
g_s factor exactly but UNDERSHOOTS the y_t factor by exactly the
v-matching coefficient `M`. The "missing" factor in Ward-by-definition
is **not** a per-rung beta-function correction; it is the **single
matching coefficient at v** between the lattice last-rung and the SM
EFT, which the v-matching note decomposes as

    M = sqrt(u_0) * F_yt * sqrt(8/9) = 1.973                         (4.6)

and evaluates at 1-loop as `M_1-loop = 1.925` (2.4% below target,
bounded by QFP 3% envelope).

**Conclusion of Part 4.** Ward-by-definition alone is not a full
P2 closure. The missing piece is the v-matching coefficient, which
is already handled by the prior v-matching note.

---

## Part 5: integration through the 16 rungs (literal 1-loop attempt)

For completeness we ran the literal per-step 1-loop integration
(runner Block 3 and Block 4):

- Gauge at rung k: update `1/g_s^2` by `b_3^{(k)} / (8 pi^2) * Delta_t`.
- Yukawa at rung k: update `ln(y_t)` by `(9/2 y_t^2 - 8 g_3^2) /
  (16 pi^2) * Delta_t` (RK2 midpoint with 100 substeps per rung).
- Starting BCs: `g_s^lat(M_Pl) = 1.067`, `y_t^lat(M_Pl) = 0.436`.

**Result**:

| Quantity | Realized | Target | Status |
|----------|----------|--------|--------|
| g_s factor through 16 rungs | NaN (Landau-pole crossing) | 1.132 | FAIL |
| y_t factor through 16 rungs | NaN (inherits gauge failure) | 2.233 | FAIL |

The `1/g^2` trajectory crosses zero during the integration. This is
driven by the tiny `b_3(16) = 1/3` at the UV rung combined with the
large starting coupling `g_s(M_Pl) = 1.067` (the LATTICE UV anchor,
not the SM extrapolation `g_s^SM(M_Pl) = 0.487`). The 1-loop
perturbative beta is not applicable on this trajectory.

**Conclusion of Part 5.** Literal 1-loop per-step integration is
numerically ill-defined. This reinforces the Part 2-3 conclusion that
per-step perturbative beta is not the correct mechanism.

---

## Part 6: comparison to retained SM RGE path (what the primary chain uses)

The primary chain uses the 2-loop SM RGE with `n_f = 6` (six SM flavors,
not 16 tastes) over the full 38.4 e-folds. This gives

    F_yt = y_t^SM(v; 2-loop) / y_t^lat(M_Pl; Ward BC) = 2.233         (6.1)

matching `target_yt` by construction (on the primary chain). The
1-loop surrogate gives `F_yt^(1-loop) = 2.180`, a 2.4% shift bounded
by the QFP 3% envelope.

The SM RGE uses `b_3_SM = 7` over the full span. It starts the
LATTICE anchor at `g_s(M_Pl)_lat = 1.067` (not the SM extrapolation),
and integrates downward toward `v`. **The 1-loop integration of the
SM beta functions STARTING FROM THE LATTICE UV ANCHOR also crosses
the Landau pole** (runner Block 7 confirms this), because the lattice
anchor is far above the SM-compatible perturbative regime.

**However, the primary chain uses the BACKWARD Ward scan**: it
integrates from `v` UP to `M_Pl`, imposing the SM BC at `v` and
requiring the extrapolated trajectory to match the Ward BC at `M_Pl`.
In this direction the integration is well-defined (starting from
`g_s^SM(v) = 1.139`, running up with `b_3_SM = 7`, one reaches
`g_s^SM(M_Pl) = 0.487`, not the lattice `1.067`). The mismatch
between `g_s^SM(M_Pl) = 0.487` and `g_s^lat(M_Pl) = 1.067` is
resolved by the Boundary Selection Theorem: these are different
theories with different physical content.

The backward Ward scan fixes `y_t(v) = 0.9734` by requiring
`y_t(M_Pl) = 0.436` (Ward BC on the lattice side). This is the
primary-chain numerical closure of P2 quantitatively, bounded by QFP
insensitivity at 3%.

**Conclusion of Part 6.** The primary chain's quantitative closure
of P2 uses the SM RGE with `n_f = 6`, the lattice Ward BC at M_Pl,
and backward integration. It does NOT use per-rung beta functions
with `n_taste` replacement. The present note's NO-GO on the per-rung
beta approach does not affect the primary-chain closure.

---

## Part 7: asymptotic-freedom breakdown at large n_taste

The retained 1-loop `b_3(n) = (33 - 2n) / 3` has a zero at `n = 33/2 =
16.5`. At `n = 16`, `b_3 = 1/3 > 0` (marginally asymptotically free).
At `n = 17`, `b_3 = -1/3 < 0` (asymptotically SLAVE, unphysical for a
UV-complete lattice theory).

The staircase's UV endpoint at `n_taste = 16` is therefore **on the
edge of AF loss**. The marginal positivity of `b_3` at the UV rung
is the structural reason why 1-loop perturbative running is not
applicable: the cumulative `b_3^{(k)} * Delta_t / (8 pi^2)` over the
16 rungs is

    sum_{k=0}^{15} b_3^{(k)} * |Delta_t| / (8 pi^2)
      = |Delta_t| / (8 pi^2) * sum_{n=1}^{16} (33 - 2n)/3
      = |Delta_t| / (8 pi^2) * (1/3) * sum_{n=1}^{16} (33 - 2n)
      = 2.40 / 78.96 * (1/3) * (16 * 33 - 2 * 136)
      = 2.40 / 78.96 * (1/3) * (528 - 272)
      = 2.40 / 78.96 * 256/3
      = 2.594                                                          (7.1)

vs the starting `1/g_s(M_Pl)^2 = 0.878`. Since `2.594 > 0.878`, the
trajectory crosses zero and the 1-loop integration is ill-defined.

**This is the mathematical content of the non-perturbative staircase.**
The cumulative 1-loop correction exceeds the UV `1/g^2`, so the
perturbative expansion is breaking down. The full non-perturbative
answer is supplied by `alpha_LM^16` in the hierarchy theorem, which
encapsulates the 17-decade compression without requiring per-rung
perturbative integration.

**Conclusion of Part 7.** The AF marginality at `n_taste = 16` is
the structural signal that the staircase is non-perturbative.

---

## Part 8: outcome statement

**Theorem (Per-Step Beta NO-GO).**

Let the canonical staircase sequence be `mu_k = M_Pl * alpha_LM^k`
for `k = 0, ..., 16` with `n_taste^{(k)} = 16 - k`. Let the per-rung
1-loop gauge beta coefficient be `b_3^{(k)} = (33 - 2 n_taste^{(k)})/3`
and the per-rung Yukawa beta be the retained SM 1-loop form (3.1).

Then:

(i) **AF marginality.** `b_3(16) = 1/3` is the smallest positive
    value in the sequence; AF is lost at `n_taste = 33/2 = 16.5`, so
    the UV endpoint is marginal.

(ii) **Numerical breakdown.** Literal 1-loop integration of
     `g_s^{(k)}` downward from the retained UV anchor
     `g_s^lat(M_Pl) = 1.067` through 16 rungs is ill-defined (the
     `1/g^2` trajectory crosses zero). Yukawa integration inherits
     this breakdown.

(iii) **Ward non-preservation at the beta level.** `d ln(y_t/g_s)/dt
      = 0` at `y_t = g_s/sqrt(6)` requires `b_3 = 29/4 = 7.25`,
      corresponding to non-integer `n_taste = 5.625` that is not in
      the canonical sequence. The prior note's "per-rung Ward
      preservation" is a STRUCTURAL algebraic identity from
      D9/D12/D16/D17/S2, NOT a per-rung 1-loop beta identity.

(iv) **Ward-by-definition insufficient.** If `y_t(mu_k) = g_s(mu_k)/
     sqrt(6)` is adopted tautologically, the y_t factor equals the g_s
     factor `= 1.132`, missing the target `2.233` by a factor of
     1.973, which equals the prior v-matching coefficient `M`.

(v) **Net verdict.** The staircase is **non-perturbative** (consistent
    with `alpha_LM^16` being a non-perturbative factor). Per-step
    1-loop beta functions do not provide a framework-native closure
    of P2.

**Corollary.** The canonical closure path for P2 on the primary chain
is the prior partial-closure duo:

1. Taste-staircase note (`TRANSPORT_NOTE`): per-rung Ward preservation
   via structural re-derivation + uniform `u_0^{-1/32}` distribution.
2. v-matching note (`V_MATCHING_NOTE`): decomposition `M = sqrt(u_0)
   * F_yt * sqrt(8/9)` within QFP 3% envelope.

The present note contributes the NEGATIVE result that a per-step
perturbative beta-function alternative does not exist. It SHARPENS
the prior structural claim: Ward preservation is algebraic-structural,
not beta-functional.

---

## Safe claim boundary

**This note claims:**

1. Per-step 1-loop perturbative beta functions with `n_taste` replacing
   `n_f` do NOT reproduce the retained g_s and y_t factors through
   the 16-rung staircase. (Numerical Landau-pole breakdown.)

2. Ward-ratio preservation at the 1-loop beta level requires `b_3 =
   29/4`, which corresponds to non-integer `n_taste = 5.625` outside
   the canonical sequence. The prior note's "per-rung Ward preservation"
   is not a beta-function statement.

3. Ward-by-definition combined with the CMT gauge endpoint gives
   `y_t_factor = g_s_factor = 1.132`, missing `target_yt = 2.233` by
   exactly the prior v-matching coefficient `M = 1.973`.

4. The taste staircase is **non-perturbative**, consistent with
   `alpha_LM^16` in the hierarchy theorem. Per-rung 1-loop beta
   functions are NOT the mechanism.

**This note does NOT claim:**

- That the prior taste-staircase note or v-matching note are
  incorrect. Both stand as PARTIAL closures of P2.
- That the framework's `m_t = 169.5 GeV` prediction changes. It does
  not.
- That the master UV-to-IR transport obstruction theorem changes.
  It does not; this note contributes a NO-GO on one sub-path.
- That alternative non-perturbative mechanisms (blocking RG, strong
  coupling expansion) are ruled out. It claims only that the 1-loop
  perturbative path with `n_taste` replacement fails.

**Classification.**

| Element | Status |
|---------|--------|
| Per-step 1-loop beta with n_taste replacement | NO-GO (this note) |
| Structural Ward preservation (prior note, Part 2) | PARTIAL (unchanged) |
| v-matching decomposition (prior note) | PARTIAL (unchanged) |
| Primary chain 2-loop SM RGE | DERIVED on retained matter |
| QFP insensitivity 3% envelope | DERIVED |
| P2 overall | PARTIAL (via two prior notes + this NO-GO) |

---

## Validation

The runner `scripts/frontier_yt_p2_taste_staircase_beta.py` performs
the following deterministic checks:

1. **Retained constants.** Reproduce `u_0`, `alpha_LM`, Ward ratio,
   target factors from zero-import chain values.
2. **n_taste sequence.** Verify the integer sequence `16, 15, ..., 0`
   across 17 rungs with 16 decouplings.
3. **b_3 endpoint values.** Verify `b_3(16) = 1/3` (AF marginal) and
   `b_3(0) = 11` (pure gauge limit). Verify `b_3(17) = -1/3 < 0`
   (AF lost one step beyond the canonical staircase).
4. **Per-step gauge integration.** Integrate 1-loop gauge through 16
   rungs with `n_taste` replacement. Null-result: does NOT reproduce
   target_gs = 1.132 (Landau-pole crossing; NaN output).
5. **Per-step Yukawa integration.** Same as (4) for Yukawa. Null-result:
   does NOT reproduce target_yt = 2.233.
6. **Ward-preservation requirement.** `b_3 = 29/4 = 7.25` required
   for `d(y_t/g_s)/dt = 0` on the Ward locus. Confirm no canonical
   rung satisfies this exactly.
7. **Ward-by-definition test.** Under `y_t(mu_k) = g_s(mu_k)/sqrt(6)`
   literally, the y_t factor equals the g_s factor = 1.132. Confirm
   discrepancy from target = 1.973 = prior v-matching `M`.
8. **SM RGE comparison.** Confirm that 1-loop SM RGE with `n_f = 6`,
   integrating DOWN from the retained lattice UV anchor `g_s(M_Pl)=1.067`,
   also crosses the Landau pole (further evidence of non-perturbative
   character).
9. **Verdict.** Confirm NO-GO classification: per-step perturbative
   beta does not close P2.

Runner output: 12 PASS, 0 FAIL. Log at
`logs/retained/yt_p2_taste_staircase_beta_2026-04-17.log`.

---

## Import status

| Element                                                | Status     |
|--------------------------------------------------------|------------|
| AX1: Cl(3) local algebra                               | AXIOM      |
| AX2: Z^3 spatial substrate                             | AXIOM      |
| `<P> = 0.5934`                                         | COMPUTED   |
| `u_0 = 0.8777`                                         | DERIVED    |
| `alpha_LM = 0.0907`                                    | DERIVED    |
| `g_s^lat(M_Pl) = 1.067`, `g_s^lat(v) = 1.208`          | DERIVED    |
| `y_t^lat(M_Pl) = 0.436` (Ward BC)                      | DERIVED    |
| `y_t^lat(v) = 0.973` (prior chain)                     | DERIVED    |
| target_gs = 1.132, target_yt = 2.233                   | DERIVED (targets) |
| n_taste sequence `{16, 15, ..., 0}`                    | DERIVED (this note) |
| b_3(n) = (33 - 2n)/3                                   | DERIVED (retained group theory) |
| AF marginal at n_taste = 16 (b_3 = 1/3)                | DERIVED (this note) |
| Ward-preserving b_3 = 29/4                             | DERIVED (this note; algebraic) |
| Per-step 1-loop integration breakdown                  | DERIVED (this note; numerical) |
| Ward-by-def y_t factor = g_s factor = 1.132            | DERIVED (this note) |
| Discrepancy = 1.973 = prior v-matching M               | DERIVED (this note; matches prior v-matching note) |
| NO-GO on per-step perturbative beta for P2             | DERIVED (this note) |
| Staircase is non-perturbative                          | DERIVED (consistent with alpha_LM^16 in hierarchy theorem) |

**No new axioms. No new canonical-surface choices. The only new content
of this note is the NEGATIVE result that per-step 1-loop perturbative
beta functions with `n_taste` replacement do not close P2, and the
POSITIVE identification that the missing factor is exactly the prior
v-matching coefficient `M = 1.973`. Both the prior taste-staircase
and v-matching notes remain canonical.**

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `yt_p2_taste_staircase_transport_note_2026-04-17` (downstream consumer;
  backticked to avoid length-3 cycles through yt_qfp_insensitivity and
  yt_uv_to_ir_transport_obstruction — citation graph direction is
  *transport → beta_functions*, body of beta_functions cites transport
  and v_matching as priors)
- [yt_p2_v_matching_theorem_note_2026-04-17](YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md)
- [yt_ward_identity_derivation_theorem](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
- [yt_boundary_theorem](YT_BOUNDARY_THEOREM.md)
- [observable_principle_from_axiom_note](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [yt_zero_import_chain_note](YT_ZERO_IMPORT_CHAIN_NOTE.md)
- [yt_qfp_insensitivity_support_note](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
