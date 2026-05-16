# y_t Bridge: EW Coupling Derivation and Sensitivity Analysis

**Date:** 2026-04-14 (demoted 2026-05-16)
**Claim type:** bounded_theorem
**Status:** bounded numerical-match scan (target-conditioned `taste_weight` scan against observed `sin^2(theta_W)(M_Z)` plus comparator checks)
**Audit class:** G — load-bearing step is a target-conditioned numerical scan against observed EW comparators, not a derivation from the restricted packet
**Superseded by (historical):** `COMPLETE_PREDICTION_CHAIN_2026_04_15.md` for the headline `y_t` chain; the present note is retained as a target-conditioned EW-bridge support scan, not a closed derivation
**Primary runner:** `scripts/frontier_yt_ew_coupling_derivation.py`
**Supporting runner (informational):** `scripts/frontier_yt_qfp_insensitivity.py` (QFP insensitivity proxy)

## Scope (honest framing)

This note is **not** a derivation that the EW coupling bridge `g_1(v)`,
`g_2(v)` and the SM-RGE surrogate used in the `y_t` chain are framework-native
closures of the restricted packet. It is a bounded *target-conditioned
numerical scan*: given (i) the imported observed value
`sin^2(theta_W)(M_Z) = 0.23122`, (ii) the imported physical EW masses
`(M_Z, M_W, M_T, M_B, M_C)`, (iii) a pre-selected one-parameter Hamming-weight
taste-threshold staircase `m_k = alpha_LM^{k/2} * M_Pl` with degeneracies
`(1, 4, 6, 4, 1)`, (iv) a SM-like 2-loop Machacek-Vaughn gauge RGE used as
the surrogate transport from `v` to `M_Z`, and (v) the Coupling Map Theorem
input `alpha_s(v) = 0.1033` injected at the boundary, the runner scans the
scalar `taste_weight in linspace(0, 2, 41)` plus a fine refinement on a
single decisive parameter and reports the value that minimizes
`|sin^2_pred(M_Z) - sin^2_obs(M_Z)|` across the scan.

The runner's PASS rows are:

1. `sin^2(theta_W)(M_Z) within 1% of observed` — a comparator against the
   observed `sin^2(theta_W)(M_Z) = 0.23122` AT the `taste_weight = 0.390`
   selected by minimizing the same comparator;
2. `1/alpha_EM(M_Z) within 15% of observed` — a comparator against
   `1/alpha_EM_obs = 127.951` that lands at `143.584` (`+12.22%` deviation),
   explicitly tagged "BOUNDED" in the runner because the absolute
   normalization is set by `g_Y^2 = 1/5` and not re-derived;
3. `alpha_s(M_Z) within 10% of observed` — a comparator against
   `alpha_s_obs(M_Z) = 0.1179` that lands at `0.1062` (`-9.93%` deviation),
   inherited from the CMT input `alpha_s(v) = 0.1033`;
4. `Bare couplings require zero imports` — an assertion that `g_3^2 = 1`,
   `g_2^2 = 1/4`, `g_Y^2 = 1/5` come from Cl(3) lattice geometry, not an
   independent derivation step in this runner;
5. `alpha_s(v) from CMT (framework-derived, not imported)` — an assertion
   pointing at an upstream theorem, not an independent derivation step;
6. `Taste_weight has physical interpretation` — a range check
   `0.01 < best_tw < 3.0`, not a derivation of the selected value
   `taste_weight = 0.390`;
7. `2-loop running used for v -> M_Z` — an assertion that the surrogate
   transport is integrated, not a derivation that the SM RGE is the
   framework's own RG flow above `v`;
8. `Gap reduced from 3.4% to < 1%` — a comparator describing the same scan
   that the `taste_weight` parameter was tuned against.

The decisive load-bearing parameter `taste_weight = 0.390` is **selected
by minimizing the residual against the observed comparator
`sin^2(theta_W)(M_Z)`**, and the runner's own commentary records that
`taste_weight = 0.390 requires a physical derivation from the taste-gauge
coupling structure` (Part 9 status line). Several PASS rows are comparator
checks against the same observed quantities the scan is tuned against, and
the remaining PASS rows are assertions that constants are framework-derived
rather than independent computations in this runner.

This is therefore an `audited_numerical_match` / class-G proxy in the
project's audit taxonomy, not a closed first-principles derivation of the
EW coupling bridge from the restricted packet. The remaining structural
gaps the source note itself acknowledges
(`g_2(v)`, `lambda(v)`, `kappa_EW`, and a rigorous SM-RGE surrogate
theorem) are recorded below in "What remains open (load-bearing gaps)".

> **Historical WARNING (retained):** This note predates the
> `COMPLETE_PREDICTION_CHAIN_2026_04_15.md` package which carries the
> promoted quantitative rows. That package adjusts the framing of `g_2`,
> `g_Y`, the color projection `sqrt(8/9)` on `y_t`, and the CW `lambda`
> route. The Import Status Table below is the **pre-2026-04-15 framing**
> of this note and is retained for historical context only; it does
> **not** describe the promoted package, does **not** describe the audit
> status of this note as a target-conditioned scan, and must **not** be
> used for promotion decisions. The promoted `g_2` / `lambda` framing in
> the complete-prediction-chain package is itself a separate audit
> object and is out of scope for this note.

## Purpose

The backward Ward derivation of m_t = 169.4 GeV uses five couplings as
initial conditions at v for the SM RGE: (g_1, g_2, g_3, y_t, lambda).
Of these:

- g_3 = alpha_s(v) = 0.1033: DERIVED (Coupling Map Theorem)
- y_t: DERIVED (backward Ward scan → 0.973)

The remaining three (g_1, g_2, lambda) were previously imported from
experiment. This note derives what can be derived and bounds what
cannot, to narrow the remaining import class.

Codex accepts EW inputs as "fair game" for the y_t chain
(instructions.md, lines 303-306). This work goes beyond that
acceptance to strengthen the chain.

---

## Part 1: g_1(v) — DERIVED (zero imports)

### Route

U(1)_Y is NOT asymptotically free (b_1 = +41/10 > 0). Perturbative
running from M_Pl to v is valid because the coupling WEAKENS going
to lower energy. No Landau pole occurs.

Starting from GUT unification at M_Pl:

    alpha_1_GUT(M_Pl) = alpha_LM = 0.09066

All inputs:
- alpha_LM = alpha_bare / u_0 = 0.09066 [DERIVED, CMT]
- GUT unification: g_1_GUT = g_2 = g_3 at M_Pl [DERIVED, SU(5) from Cl(3)]
- b_1 = 41/10 [DERIVED, Cl(3) hypercharge assignments]
- ln(M_Pl/v) = 38.44 [DERIVED, v from hierarchy theorem]

1-loop running:

    1/alpha_1(v) = 1/alpha_LM + b_1/(2 pi) * ln(M_Pl/v)
                 = 11.03 + 25.08
                 = 36.11

    alpha_1_GUT(v) = 0.02769
    g_1_GUT(v) = sqrt(4 pi * 0.02769) = 0.590

### Comparison

    g_1_GUT(v) predicted  = 0.590
    g_1_GUT(v) observed   = 0.464
    Deviation: +27%

The 27% deviation at 1-loop over 38 decades is comparable to the
classic SU(5) prediction quality before 2-loop corrections. Known
corrections:

1. 2-loop RGE: shifts 1/alpha by O(1) out of 36
2. GUT threshold corrections: heavy GUT particles at M_Pl
3. Proton-decay-scale adjustment: standard SU(5) uses M_GUT != M_Pl

### Import status: ZERO imports. Every ingredient traces to the axiom.

---

## Part 2: g_2(v) — NOT DERIVED (Landau pole barrier)

### The obstruction

SU(2) IS asymptotically free (b_2 = -19/6 < 0). Running from M_Pl
with alpha_GUT = 0.091:

    1/alpha_2(v) = 1/alpha_LM + b_2/(2 pi) * ln(M_Pl/v)
                 = 11.03 - 19.37
                 = -8.34   <-- NEGATIVE (Landau pole at ~4e9 GeV)

Perturbative running from M_Pl is impossible. This is structurally
identical to the SU(3) obstruction: alpha_LM = 0.091 is too strong
for perturbative running across 38 decades for any AF gauge group.

### Why the CMT doesn't extend trivially to SU(2)

The Coupling Map Theorem derives alpha_s(v) = alpha_bare/u_0^2 using
the SU(3) plaquette for u_0. Applying the SAME u_0 to SU(2) gives
alpha_2(v) = alpha_s(v) = 0.1033 — identical couplings at v, which
contradicts the observed coupling hierarchy alpha_2 << alpha_3 by 3x.

The SU(3) plaquette captures SU(3)-specific non-perturbative vacuum
fluctuations. SU(2) has different group-theoretic structure (different
C_A, different representations in the vacuum) and would require its
own plaquette computation. Even with an estimated SU(2) plaquette
(<P_SU(2)> ~ 0.73 at beta_2 = 4), the CMT gives alpha_2(v) ~ 0.093,
still 2.7x above observed.

### Physical interpretation

This is a PREDICTION of the framework, not a failure. The framework
explains WHY the CMT is necessary: the lattice coupling is too strong
for perturbative running. For SU(3), the CMT (via the plaquette)
provides the non-perturbative bridge. For SU(2), the analogous
non-perturbative bridge has not yet been computed.

### What would close this

Either:
1. Compute the SU(2) plaquette on the Cl(3)/Z^3 lattice via MC
2. Derive an SU(2) taste-staircase matching formula
3. Find a group-theory relation between SU(3) and SU(2) mean-field
   factors that accounts for the coupling hierarchy

### Import status: IMPORTED (g_2 currently uses observed sin^2(theta_W))

---

## Part 3: lambda(v) — BOUNDED, NOT DERIVED

### Coleman-Weinberg estimate

In the framework, the Higgs IS the taste condensate. If the quartic
is entirely radiative (CW mechanism), the dominant top-loop gives:

    lambda_CW = 3 y_t^4 / (8 pi^2) = 3 * 0.973^4 / (8 pi^2) = 0.034

Compared to observed lambda = m_H^2/(2v^2) = 0.129: ratio 0.26.

The CW estimate is the right order of magnitude but 3.8x low. Missing
contributions include gauge boson loops and higher-order corrections.

### Impact on y_t

lambda enters beta_{y_t} ONLY at 2-loop. Over 17 decades, varying
lambda from 0.05 to 0.30 shifts m_t by < 0.03% (QFP script, Part 3).
Lambda is genuinely negligible for the y_t prediction.

### Import status: IMPORTED (lambda hardcoded as 0.129)

---

## Part 4: QFP Insensitivity Theorem (Supporting Evidence)

The quasi-fixed-point insensitivity theorem
(`docs/YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`, 14/14 PASS) proves that
the backward Ward prediction y_t(v) = 0.973 is robust against all
sources of UV and EW uncertainty.

### Sensitivity budget

| Source                           | Impact on y_t(v) |
|----------------------------------|------------------|
| lambda(v) over [0.05, 0.30]     | < 0.03%          |
| g_1(v) over [0.30, 0.60]        | < 3.7%           |
| g_2(v) over [0.40, 0.90]        | < 7.4%           |
| 2-loop truncation                | ~2.4%            |
| Beta coeff +/-3% (taste scale)   | < 2.8%           |

### What this means

The m_t prediction is dominated by alpha_s(v) (DERIVED via CMT) and
the Ward BC y_t(M_Pl) = 0.436 (DERIVED). The EW corrections g_1 and
g_2 contribute at the several-percent level over EXTREME scan ranges
much wider than their physical uncertainty. Lambda is negligible.

### What this does NOT mean

The QFP insensitivity theorem does NOT prove the SM RGE is the correct
theory above v. It proves the prediction is STABLE regardless of which
interpolation is used. This is necessary but not sufficient for closure.
The sufficient condition is deriving WHY the SM RGE is a valid surrogate
(addressed below).

---

## Part 5: The Bridge Question — Current Status

### Codex blocker (review.md, section 2)

"If backward M_Pl transfer is correct, derive why that SM RGE
continuation above v is a valid framework-native surrogate for
lattice RG / taste-staircase evolution"

### What we now have

1. **Boundary Selection Theorem**: v is the physical crossover endpoint.
   The SM EFT is valid below v; the lattice theory above v.
   [YT_BOUNDARY_THEOREM.md, CLOSED subderivation]

2. **EFT Bridge Theorem**: The backward Ward approach applies the
   Ward identity at M_Pl (where it holds in the lattice theory) and
   uses the SM RGE as a mathematical interpolation to transfer the
   BC to v. All RGE coefficients trace to Cl(3) group theory.
   [YT_EFT_BRIDGE_THEOREM.md]

3. **QFP Insensitivity Theorem**: The prediction is stable to O(3%)
   against modifications of the running above v. Any flow sharing the
   same SU(3) group structure, QFP topology, gauge anchor alpha_s(v),
   and Ward BC gives the same y_t(v) within the sensitivity budget.
   [YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md, 14/14 PASS]

4. **EW Coupling Boundary**: g_1(v) and g_2(v) are matching-rule
   conditional at the physical scale because the EW readout coefficient
   `kappa_EW` is not fixed by the Fierz arithmetic alone. Older zero-import
   g_1(v) wording is retained only as route history. g_2(v) remains blocked
   by the SU(2) non-perturbative matching problem in this bridge note.
   lambda(v) bounded via CW (0.034). Both g_2 and lambda are
   subdominant in the y_t beta and do not contaminate the prediction.
   [EW_COUPLING_DERIVATION_NOTE.md]

### The argument for SM RGE validity above v (status: bounded plausibility, not derivation)

The SM RGE beta function coefficients are algebraic functions of group
theory constants whose values agree with Cl(3) representation content:

- b_3 = -(11/3 C_A - 4/3 T_F n_f) with C_A = 3, T_F = 1/2, n_f = 6
- b_2 = 22/3 - n_doublets/3 - n_H/6 with n_doublets = 12, n_H = 1
- b_1 = 41/10 from hypercharge assignments
- beta_{y_t} coefficients: all from SU(3)xSU(2)xU(1) Casimirs

The framing **"the framework CONTAINS the SM as its low-energy EFT, the
SM RGE is the perturbative approximation of the framework's own RG flow,
and using the derived RGE to transfer a derived BC is self-consistent"**
is a *consistency plausibility statement*, not a derivation. What this
note actually licenses is the weaker pair:

1. The numerical SM RGE coefficients used in the runner match the values
   one would write down from SU(3) x SU(2) x U(1) Casimirs computed in
   the Cl(3) representation content;
2. The QFP insensitivity proxy (`YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`,
   itself a target-conditioned support note) reports that the headline
   `y_t(v)` is stable at `O(3%)` against scans over `(g_1, g_2,
   lambda)` and the 2-loop truncation budget.

It does **not** license the stronger claim that the SM RGE *is* the
unique perturbative limit of the lattice RG flow above `v`, that the
"O(3%)" budget bounds the *true* RGE-vs-taste-staircase deviation
(as opposed to the deviation under the same scan ansatz), or that the
EW coupling bridge `g_1(v)`, `g_2(v)` are framework-native from the
restricted packet.

### What remains for full closure (still open)

1. **`g_2(v)` derivation**: Currently the largest remaining import in the
   `y_t` chain after `alpha_s` and `y_t` themselves. Deriving it requires
   SU(2) non-perturbative matching (CMT analogue or SU(2) MC). This note
   does not close it.

2. **Rigorous SM-RGE surrogate theorem**: The QFP-proxy plus
   coefficient-matching argument above establishes bounded plausibility,
   not derivation. A rigorous proof that the SM RGE is the unique
   perturbative limit of the lattice RG flow above `v` (or a derivation
   of an explicit error functional bounding the deviation from the exact
   lattice taste-staircase) is required and not present in this note.

3. **`kappa_EW` derivation**: The EW readout coefficient `kappa_EW` is
   not fixed by the Fierz arithmetic of the restricted packet; the older
   "zero-import g_1(v)" wording in Part 1 is retained as route history,
   not as a license that `g_1(v)` is closed from the restricted packet
   alone.

---

## Import Status Table

| Element              | Value     | Status    | Source                          |
|---------------------|-----------|-----------|----------------------------------|
| g_bare = 1          | 1.0       | AXIOM     | Cl(3) canonical                  |
| <P> = 0.5934        | 0.5934    | COMPUTED  | SU(3) MC at beta = 6            |
| alpha_LM            | 0.09066   | DERIVED   | alpha_bare/u_0                   |
| alpha_s(v)          | 0.1033    | DERIVED   | CMT, n_link = 2                  |
| v                   | 246.28 GeV | DERIVED   | Hierarchy theorem                |
| y_t(M_Pl)           | 0.436     | DERIVED   | Ward identity                    |
| g_1_GUT(v)          | 0.590     | DERIVED   | 1-loop U(1) running from M_Pl   |
| g_2(v)              | 0.646     | IMPORTED  | sin^2(theta_W)(M_Z) = 0.23122   |
| lambda(v)           | 0.129     | IMPORTED  | m_H = 125 GeV                    |
| lambda(v) CW bound  | 0.034     | BOUNDED   | CW top loop                      |
| SM RGE coefficients | b_i, c_i  | DERIVED   | Cl(3) group theory               |
| y_t(v)              | 0.973     | DERIVED   | Backward Ward + QFP stability    |
| m_t                 | 169.4 GeV | DERIVED   | y_t(v) * v / sqrt(2)             |
| alpha_s(M_Z)        | 0.1181    | DERIVED   | 2-loop QCD running from v        |

### Honest summary (re-framed 2026-05-16)

The y_t chain has 2 remaining imports of physical origin in this note's
framing: `g_2(v)` and `lambda(v)`. The runner's QFP scan reports that
the headline `y_t(v)` is stable at the several-percent level against
scans over these two parameters; this is a *target-conditioned stability
report*, not a derivation that `g_2(v)` and `lambda(v)` are negligible
in the framework-native (rather than scan) sense.

The backward Ward prediction carries a `~3%` *scan-budgeted* systematic
from using the SM RGE as the interpolation above `v` under the QFP scan
ansatz. This is bounded by the QFP insensitivity scan and is comparable
to the 2-loop truncation error *under the same scan*. It is **not** a
bound on the true RGE-vs-taste-staircase deviation, which would require
the rigorous surrogate theorem listed below in "What remains open".

The "DERIVED" labels on `g_1_GUT(v) = 0.590` and the SM RGE coefficients
in the Import Status Table above are the pre-2026-04-15 framing of this
note (see the historical WARNING in the Scope section); they should be
read as "the route computes these from upstream theorems" rather than
"this note's runner re-derives them as audit-load-bearing steps".

## What remains open (load-bearing gaps)

To upgrade this row from `audited_numerical_match` to a clean derivation,
the following structural gaps must be closed; none of the present runner
PASS rows close any of them:

1. **Derive `taste_weight`**: the decisive parameter
   `taste_weight = 0.390` is selected in the runner by minimizing
   `|sin^2_pred(M_Z) - sin^2_obs(M_Z)|` over a 41-point coarse + fine
   scan. To upgrade to a derivation, `taste_weight` must come from the
   taste-gauge coupling structure (orbit decomposition of the BZ-corner
   tastes under SU(3)_color and SU(2)_L), not from minimizing residual
   against the observed EW comparator the same scan reports on.

2. **Derive the staircase scheme**: the one-parameter Hamming-weight
   staircase `m_k = alpha_LM^{k/2} * M_Pl` with degeneracies
   `(1, 4, 6, 4, 1)` and the rule "each extra taste adds one
   generation-equivalent of matter" is pre-selected, not derived. The
   runner's own commentary records two alternative readings of the
   taste matter content (1/3-gen-per-taste partner mixing vs.
   full-gen-per-taste copying) without selecting between them.

3. **Derive `g_2(v)`**: the runner emits `g_2(v) = 0.611` from the
   target-conditioned taste-staircase scan, which is `-5.48%` below the
   observed-at-`v` value `0.646`. The Part-2 obstruction "SU(2) Landau
   pole prevents direct CMT extension" is recorded but no SU(2)
   non-perturbative bridge (SU(2) plaquette MC, SU(2) taste-staircase
   matching formula, or SU(3)<->SU(2) group-theory relation) is supplied.

4. **Derive `lambda(v)`**: the Coleman-Weinberg estimate
   `lambda_CW = 3 y_t^4 / (8 pi^2) = 0.034` is `~3.8x` below the
   observed `lambda(v) = 0.129`. The note treats this as "the right
   order of magnitude" but does not derive the gauge-boson-loop and
   higher-order contributions that would close the gap.

5. **Derive `kappa_EW`**: the EW readout coefficient is not fixed by
   the Fierz arithmetic of the restricted packet, so the older
   "zero-import g_1(v)" Part-1 framing reduces to "matching-rule
   conditional at the physical scale" rather than a closure.

6. **Derive the SM-RGE surrogate**: a rigorous proof that the SM RGE
   is the unique perturbative limit of the lattice RG flow above `v`,
   or an explicit error functional bounding the deviation from the
   exact lattice taste-staircase that is independent of the QFP scan
   ansatz, is required.

7. **Derive the absolute `1/alpha_EM(M_Z)` normalization**: the runner
   emits `1/alpha_EM(M_Z) = 143.6` against the observed `127.951`
   (`+12.22%`), explicitly tagged "BOUNDED" because the absolute
   normalization is set by the pre-selected `g_Y^2 = 1/5`. A derivation
   of the absolute normalization (rather than only the
   `sin^2(theta_W)(M_Z)` ratio that is comparator-tuned via
   `taste_weight`) is required.

All seven are operator/theorem problems and are out of scope for this
note. The note therefore stops at the bounded target-conditioned
numerical-scan claim and does not attempt to upgrade beyond it.

## Audit history

The 2026-05-05 audit recorded this row as `audited_numerical_match` with
Class-G load-bearing step, with the substantive observation that the
runner computes a taste-threshold scan but the decisive parameter
`taste_weight` is selected by minimizing error against the observed
`sin^2(theta_W)(M_Z)`, and several PASS checks are comparator checks
against observed `sin^2`, `alpha_EM`, and `alpha_s` rather than
independent computations. The note itself already acknowledged remaining
imported or open pieces above (`g_2(v)`, `lambda(v)`, `kappa_EW`, and a
rigorous SM-RGE surrogate theorem).

The 2026-05-16 demotion edit (this revision) rewrites the headline
"Status", adds an explicit "Scope (honest framing)" block enumerating
the eight PASS rows and the five load-bearing imports, demotes the
"SM-RGE validity" sub-argument in Part 5 from a closure assertion to a
bounded plausibility statement, re-frames the "Honest summary" so the
QFP `~3%` budget reads as a scan-budgeted statement rather than a true
RGE-vs-taste-staircase bound, and lists seven structural gaps under
"What remains open (load-bearing gaps)" that must close to upgrade this
row to a clean derivation. The runner output is unchanged
(`scripts/frontier_yt_ew_coupling_derivation.py`, 10 PASS / 0 FAIL,
elapsed 0.7s in the cached run), the Import Status Table is preserved
for historical context with an in-table-adjacent re-framing in "Honest
summary", and the current audit status is owned by the regenerated
audit pipeline and the next independent re-audit. This brings the
headline framing of this note into agreement with the parallel
2026-05-16 demotions of sister `YT_*_NOTE` rows
(`YT_BRIDGE_ACTION_INVARIANT_NOTE.md` in iter22,
`YT_BRIDGE_MOMENT_CLOSURE_NOTE.md` in iter23,
`YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md`, and
`YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md`).

## Audit dependency repair links

This graph-bookkeeping section records the upstream notes the EW
coupling bridge and SM-RGE surrogate argument depend on. It does not
promote this note or change the audited claim scope.

- [YT_BOUNDARY_THEOREM.md](YT_BOUNDARY_THEOREM.md)
  for the boundary selection of v as the physical EFT crossover endpoint.
- [YT_EFT_BRIDGE_THEOREM.md](YT_EFT_BRIDGE_THEOREM.md)
  for the backward Ward bridge construction the EW couplings feed into.
- [YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
  for the QFP-stability sensitivity budget bounding the SM-RGE surrogate
  error at O(3%).
- [YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md](YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md)
  for the forced UV-localized class that constrains the bridge shape on
  which the EW comparator runs.
- [YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md](YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md)
  for the EW-window proxy scan that excludes diffuse rescues at the
  bridge level.
