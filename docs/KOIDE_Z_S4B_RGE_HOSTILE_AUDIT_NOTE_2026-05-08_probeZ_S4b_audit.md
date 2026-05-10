# Probe Z-S4b-Audit — Hostile Audit of Y-S4b-RGE Imports vs Retained Ingredients (probeZ_S4b_audit)

**Date:** 2026-05-08 (compute date 2026-05-10)
**Type:** bounded_theorem (audit downgrades sister probe Y-S4b-RGE from positive_theorem to bounded_theorem on import-content grounds)
**Claim type:** bounded_theorem (semantic-layer audit; downgrade of sister probe)
**Scope:** review-loop source-note proposal. Hostile audit (per
[`feedback_hostile_review_semantics.md`](../.claude/projects/-Users-jonreilly-Projects-Physics/memory/feedback_hostile_review_semantics.md)
and
[`feedback_consistency_vs_derivation_below_w2.md`](../.claude/projects/-Users-jonreilly-Projects-Physics/memory/feedback_consistency_vs_derivation_below_w2.md))
of Probe Y-S4b-RGE
([`KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md`](KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md)).
The sister probe declared `m_H(3-loop) = 125.14 GeV` (deviation
−0.09% from PDG 125.25 GeV) a POSITIVE THEOREM closing the +12% gap
identified by Probe X-S4b-Combined. The hostile audit asks whether
the ingredients used in that derivation are GENUINELY RETAINED in
Cl(3)/Z³ or are EXTERNAL IMPORTS dressed as retained.
**Status:** source-note proposal. Verdict is **BOUNDED THEOREM**
(downgrade of sister Y-S4b-RGE from positive to bounded), with named
imports identified at three of the five ingredient layers (β_λ^(2),
β_λ^(3), and λ(M_Pl)=0 BC). The 1-loop-only derivation remains
inside the ~5% positive band (+4.27%) on retained content.
**Authority disclaimer:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** probe-z-s4b-audit-hostile-import-tier-20260508-probeZ_S4b_audit
**Primary runner:** [`scripts/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.py`](../scripts/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.py)
**Cache:** [`logs/runner-cache/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.txt`](../logs/runner-cache/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived `claim_type`,
`audit_status`, and `effective_status` are generated only after the
independent audit lane reviews the claim, dependency chain, and
runner. The audit lane has full authority to retag, narrow, or reject
the proposal.

## 0. Question

Probe Y-S4b-RGE
([`KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md`](KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md))
declared a POSITIVE THEOREM: that the retained 3-loop SM `β_λ`
system, integrated from `λ(M_Pl) = 0` to `v_EW` on framework-derived
couplings, gives `m_H = 125.14 GeV` (−0.09% from PDG 125.25 GeV),
closing 99.3% of the +12.04% Probe X-S4b-Combined "structurally
inaccessible" gap.

The user-memory rule
[`feedback_hostile_review_semantics.md`](../.claude/projects/-Users-jonreilly-Projects-Physics/memory/feedback_hostile_review_semantics.md)
warns:

> Trace-ratio derivations can be arithmetically perfect while
> comparing against convention-defined sources rather than physical
> couplings; hostile-review passes must stress-test the action-level
> identification of symbols, not just algebra.

This audit applies that lens to Probe Y-S4b-RGE. Five ingredients
are load-bearing for the +12% closure:

1. The 1-loop β_λ coefficient.
2. The 2-loop β_λ scalar channel weights.
3. The 3-loop β_λ scalar channel weights.
4. The classicality BC `λ(M_Pl) = 0`.
5. The framework-derived couplings `(g_1, g_2, g_3, y_t)` at v_EW.

**Question:** for each ingredient, is it RETAINED (derivable from
A1+A2+retained content) or IMPORTED (from MSbar dim-reg literature
external to the framework's lattice / `<P>`-scheme retention stack)?
The answer determines whether Y-S4b-RGE is a derivation or an
arithmetic ratio against a literature comparator.

## 1. Answer

**BOUNDED THEOREM (downgrade).** Three of the five Y-S4b-RGE
ingredients are EXTERNAL IMPORTS, not retained derivations:

| # | Ingredient | Status | Why |
|---|---|---|---|
| I1 | β_λ^(1) coefficient | **RETAINED (largely)** | 1-loop β_λ is universal (Machacek-Vaughn 1983); each term derives from retained Casimir algebra + 1-loop counterterm structure that the framework's `<P>`-scheme can in principle reproduce. The numerical coefficients `24, 12, -6, -3, +3/8` are scheme-independent at 1-loop in any reasonable scheme. |
| I2 | β_λ^(2) coefficients (FJJ92, LWX03) | **IMPORTED** | The scalar channel weights `-312, -144, -3, +30, ...` and `305/16 g_2^6, -289/48 g_2^4 g'^2, -559/48 g_2^2 g'^4, -379/48 g'^6, -73/8 g_2^4, +39/4 g_2^2 g'^2, +629/24 g'^4, ...` are 2-loop dim-reg MSbar integrals on multi-loop topologies. Per Probe X-L1-MSbar the framework retains only the Casimir skeleton at 2-loop+; the scalar weights require 3-loop integral primitives (sunsets, ladders) that are NOT in retained content. Same verdict applies to scalar β_λ^(2) where the same dim-reg machinery is used. |
| I3 | β_λ^(3) coefficients (CZ12, BPV13) | **IMPORTED** | Contains ~200 terms with explicit ζ(3) factors like `640 − 1152 ζ(3)` (g_3^4 yt^4), `-1599/16 + 291/2 ζ(3)` (g_2^6), `7168/3 ζ(3) − 1024` (g_3^6 yt^2), etc. These are 3-loop dim-reg MSbar integrals computed in `D = 4 − 2ε` with non-trivial ε-pole subtraction. The framework's lattice `<P>`-scheme is foreign to dim-reg; per Probe X-L1-MSbar `beta_2, beta_3` scalar coefficients are NOT framework-derivable in any scheme. β_λ^(3) is in the same class — UNAMBIGUOUSLY IMPORTED. |
| I4 | λ(M_Pl) = 0 BC | **POSTULATED, not derived** | Y-S4b-RGE §10 itself admits: `lambda_m_pl_classicality_boundary_condition: retained but framework-axiom in nature, not derived from A1+A2`. The VACUUM_CRITICAL_STABILITY_NOTE labels it "framework-native composite-Higgs / no-elementary-scalar boundary structure" but provides no first-principles derivation showing why classicality at M_Pl is forced rather than chosen. Different physics: postulated BCs are admissions; derived BCs are theorems. |
| I5 | g_3(v), g_3 → M_Pl uplift | **IMPORTED (uplift only)** | g_3(v) = √(4π · α_s(v)) with α_s(v) = α_bare/u_0² is RETAINED. But the *uplift* g_3(v) → g_3(M_Pl) used in step 1 of K3 (run gauge+Yukawa from v to M_Pl) traverses 17 decades of QCD running through β_3^(2) and β_3^(3). Per Probe X-L1-MSbar these are imports. So the value of g_3(M_Pl) entering the downward β_λ integration is itself an IMPORT-CONTAMINATED quantity. The same applies to y_t(M_Pl) via β_yt^(2), β_yt^(3). |

**Net audit verdict.** The +12% closure stands ARITHMETICALLY but
not as a from-axioms-only derivation. The K3 result `m_H = 125.14
GeV` at 3-loop is achieved using 2-loop and 3-loop SM β_λ
coefficients that are MSbar dim-reg imports, plus a postulated UV
boundary condition that the framework cannot derive from A1+A2. The
1-loop-only result `m_H(1-loop) = 130.60 GeV` (+4.27%) is the
strongest claim that survives a strict retained-only audit. This
+4.27% is still inside the brief's ~5% positive threshold by a hair
— but only on the 1-loop layer, where the 24λ², -6y_t⁴, and gauge
contributions ARE recoverable from retained Casimirs at the 1-loop
counterterm level.

**Brief tier mapping:**

> If 1-2 ingredients are imports → Y-S4b-RGE downgrades to BOUNDED
> (with named imports).
> If ≥3 ingredients are imports → Y-S4b-RGE collapses to
> ARITHMETIC RATIO not derivation.

This audit identifies **3 imports (I2, I3, I4) plus 1 import-contaminated
auxiliary (I5 uplift)**. By the brief, this puts Y-S4b-RGE on the
boundary between "bounded" and "arithmetic ratio." The conservative
verdict, retaining the I1 1-loop layer as genuinely derived, is
**BOUNDED THEOREM** — the closure is real numerically, but its
sub-percent precision rests on imports and a postulate, not on
A1+A2-only derivation. The strongest from-axioms claim is the +4.27%
1-loop result. Sister probe Y-S4b-RGE should be retagged accordingly.

## 2. Setup

### Premises

| ID | Statement | Class |
|---|---|---|
| BASE-CL3 | Physical `Cl(3)` local algebra | repo baseline; [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| BASE-Z3 | `Z^3` spatial substrate | repo baseline; same source |
| ProbeY | Y-S4b-RGE positive_theorem proposal at m_H(3L) = 125.14 GeV | [`KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md`](KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md) |
| ProbeXL1 | Probe X-L1-MSbar verdict that QCD β_2, β_3 scalar coefficients are NOT framework-derivable in any scheme | [`KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md`](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md) |
| BetaLamSrc | Y-S4b-RGE 3-loop runner cites β_λ at 1-loop (MV83), 2-loop (FJJ92, LWX03), 3-loop (CZ12, BPV13) | [`scripts/frontier_higgs_mass_full_3loop.py`](../scripts/frontier_higgs_mass_full_3loop.py) lines 138-551 |
| ClassBC | `λ(M_Pl) = 0` (classicality boundary condition; explicit admitted_context in Y-S4b §10) | [`KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md`](KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md) §10 |
| EWSBPotForm | SM Higgs potential FORM `V = −μ² H†H + λ(H†H)²` admitted as SM convention | [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md) §3 line 117 |
| HostileRule | Hostile review must stress-test action-level identification of symbols, not just algebra | [`feedback_hostile_review_semantics.md`](../.claude/projects/-Users-jonreilly-Projects-Physics/memory/feedback_hostile_review_semantics.md) |
| ConsistRule | Consistency equality is not derivation; A² below-W2 / runner-must-verify | [`feedback_consistency_vs_derivation_below_w2.md`](../.claude/projects/-Users-jonreilly-Projects-Physics/memory/feedback_consistency_vs_derivation_below_w2.md) |
| PDG-Higgs | `m_H = 125.25 GeV` (falsifiability comparator only) | PDG 2024 |

### Forbidden imports

- NO new repo-wide axioms.
- NO PDG observed values used as derivation input.
- This audit consumes Probe Y-S4b-RGE and Probe X-L1-MSbar as inputs;
  its conclusions are conditional on those probes' status.

### Authority of this probe

This probe does NOT introduce new derivation primitives. It is a
**semantic-layer audit** of Probe Y-S4b-RGE that asks, ingredient by
ingredient, whether the +12% closure is RETAINED or IMPORTED. The
audit's marginal contribution is:

1. Itemized retention/import classification for each of the five
   Y-S4b-RGE ingredients.
2. Numerical recompute of the 1-loop-only derivation on retained
   content (m_H(1L) = 130.60 GeV; +4.27% gap).
3. Consistency check against Probe X-L1-MSbar's "scalar 3-loop /
   4-loop coefficients NOT framework-derivable in any scheme"
   verdict (β_λ^(2) and β_λ^(3) are in the same import class).
4. Tier downgrade from positive_theorem to bounded_theorem with
   named imports.

## 3. Theorem (bounded; Y-S4b-RGE downgrades to bounded with imports)

**Theorem (Z-S4b-Audit, bounded; Y-S4b-RGE downgraded with named imports).**

Under the premises of §2 and the user-memory hostile-review rule,
the Y-S4b-RGE closure of the +12% Higgs gap is BOUNDED, not POSITIVE,
because three of its five load-bearing ingredients are external
imports, and a fourth is import-contaminated:

- **(K1) 1-loop β_λ coefficient is largely retained.** The 1-loop
  `β_λ^(1) = 24λ² + 12λ y_t² − 6 y_t⁴ − 3λ(3 g_2² + g'²) +
  (3/8)[2 g_2^4 + (g_2² + g'²)²]` (Machacek-Vaughn 1983) has scheme-
  universal coefficients in any reasonable scheme. Each term arises
  from a 1-loop counterterm with a Casimir/group-theoretic origin
  that the framework's retained content can support: the `24λ²`
  pure-scalar term is the unique 1-loop quartic vacuum diagram; the
  `−6 y_t⁴` is the top-loop closure trace `Tr(y_t Y_t)^4` whose
  factor 6 is the single-flavor color trace `N_c · 1` plus Wick
  combinatorics — derivable from retained color/flavor algebra. The
  gauge contributions `(3/8)(2 g_2^4 + (g_2² + g'²)²)` involve the
  1-loop gauge boson polarization on the Higgs propagator, which the
  framework's `<P>`-scheme can in principle reproduce since the gauge
  β-function 1-loop coefficients ARE retained per Probe X-L1-MSbar.
  Verdict: **RETAINED at 1-loop** (with one mild caveat: the precise
  factor 1/(16π²) follows from a 4D Lorentz integral that the lattice
  framework approximates rather than computes exactly; this enters
  as an inherited support-tier admission of the FORM of the SM
  potential per EWSB-PotForm).

- **(K2) 2-loop β_λ scalar coefficients are imports.** The 2-loop
  expression in `frontier_higgs_mass_full_3loop.py` lines 254–280
  contains ~12 distinct rational coefficients in front of products
  of `(λ, y_t, g_1, g_2, g_3)` powers:
  ```
   −312 λ³
   −144 λ² y_t² − 3λ y_t^4 + 30 y_t^6
   +80 λ y_t² g_3² + 45/2 λ y_t² g_2² + 85/6 λ y_t² g'²
   −32 y_t^4 g_3² − 9/2 y_t^4 g_2² + 17/2 y_t^4 g'²
   +36 λ²(3 g_2² + g'²)
   −73/8 λ g_2^4 + 39/4 λ g_2² g'² + 629/24 λ g'^4
   +305/16 g_2^6 − 289/48 g_2^4 g'² − 559/48 g_2² g'^4 − 379/48 g'^6
   −8/5 g'² y_t^4
  ```
  Per Probe X-L1-MSbar (cited above), the analogous 3-loop scalar
  weights for QCD `c_FFF, c_FFA, c_FAA, c_AAA, c_FFn, c_FAn, c_AAn,
  c_Fnn, c_Ann` are NOT framework-derivable in ANY scheme — they
  require 3-loop integral primitives (dim-reg sunsets, ladders, cross
  diagrams) that are NOT part of the retained Cl(3)/Z³ stack. The
  2-loop β_λ scalar coefficients are in the same class: they are
  2-loop dim-reg MSbar integrals on multi-loop topologies (specifically
  2-loop sunsets in D = 4 − 2ε with explicit ε-pole subtraction). The
  framework's lattice `<P>`-scheme cannot recover these; literature
  (FJJ92 + erratum, LWX03) is the only known source. Verdict:
  **IMPORTED**.

- **(K3) 3-loop β_λ scalar coefficients are imports.** The 3-loop
  expression `blam_3` in `frontier_higgs_mass_full_3loop.py` lines
  396–539 contains ~30 distinct rational coefficients with explicit
  `ZETA3 = ζ(3) = 1.20206...` factors. Examples:
  ```
   +3588 λ^4
   +3564 λ³ y_t² + (792 + 288 ζ_3) λ² y_t^4 + (−396 − 528 ζ_3) λ y_t^6 + (−171 + 960 ζ_3) y_t^8
   +(640 − 1152 ζ_3) g_3^4 y_t^4
   +(−576 + 768 ζ_3) g_3² y_t^6
   +(−640 + 384 ζ_3) g_3^4 λ y_t²
   +(7168/3 ζ_3 − 1024) g_3^6 y_t²
   +(−1599/16 + 291/2 ζ_3) g_2^6
   +(1341/40 − 51/2 ζ_3) g_2^4 g'²
   ...
  ```
  These are 3-loop dim-reg MSbar integrals on Higgs/top/gauge
  topologies. The presence of `ζ(3)` factors (Riemann zeta evaluated
  at integer 3) is a structural fingerprint of dim-reg multi-loop
  integration: ζ(3) appears in the Laurent expansion of two- and
  three-loop massless propagator integrals as residues at ε = 0. The
  framework's lattice `<P>`-scheme has no analog of this structure.
  CZ12 (Chetyrkin-Zoller) and BPV13 (Bednyakov-Pikelner-Veretin) are
  the literature sources; they are NOT framework derivations.
  Verdict: **IMPORTED**, with the ζ(3) fingerprint as the most
  unambiguous evidence of dim-reg origin.

- **(K4) λ(M_Pl) = 0 is a postulate, not a derivation.** Probe
  Y-S4b-RGE itself acknowledges this in its honest scope §10:
  ```
  residual_structural_admissions:
    - lambda_m_pl_classicality_boundary_condition  # retained but
      framework-axiom in nature, not derived from A1+A2
  ```
  And the cited authority `VACUUM_CRITICAL_STABILITY_NOTE.md` line
  39 calls it "the framework-native composite-Higgs / no-elementary-
  scalar boundary structure" — a label, not a derivation showing why
  classicality is FORCED rather than CHOSEN. The 1-loop quantum
  correction to the BC `|δλ(M_Pl)| ≲ g^4/(16π²) ≈ 4 × 10⁻⁴` (per
  HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18 §3.2) is itself
  admitted as a Gap-2 retention residual. The hostile audit's
  position: a UV boundary condition that the framework cannot
  *derive* from A1+A2 is an ADMISSION, not a retained ingredient.
  This makes the K3 RGE result conditional on a free parameter that
  happens to be set to 0; setting it to a different value would
  yield a different m_H. Verdict: **POSTULATED, not derived**.

- **(K5) Gauge couplings at v are retained, but their uplift to
  M_Pl is import-contaminated.** The framework retains:
  - `g_3(v) = √(4π · α_s(v)) = √(4π · 0.1033) = 1.139` from the
    canonical surface (α_s(v) = α_bare/u_0²).
  - `g_2(v) = 0.648`, `g_1(v) = 0.464` from the EW sector (HIGGS_MASS_RETENTION_ANALYSIS).
  - `y_t(v) = 0.9176` from the YT Δ_R master assembly.

  These initial values at v_EW ARE retained. **However**, Y-S4b-RGE's
  K3 procedure first runs gauge+Yukawa UP from v_EW to M_Pl
  (`run_with_thresholds(t_v, t_pl, loop_order=nloop)`), then sets
  `λ(M_Pl) = 0`, then runs the full 5-coupling system DOWN. The
  upward run at 2-loop or 3-loop traverses the QCD β_3^(2), β_3^(3)
  coefficients (and SU(2), U(1) analogs) that Probe X-L1-MSbar
  declared NOT framework-derivable in any scheme. So `g_3(M_Pl)`,
  `g_2(M_Pl)`, `g_1(M_Pl)`, and via β_yt also `y_t(M_Pl)`, are all
  IMPORT-CONTAMINATED quantities at the boundary where λ(M_Pl) = 0
  is imposed. The downward β_λ integration then uses these
  import-contaminated couplings as inputs.

  Caveat: at 1-loop only, the upward run uses just β_3^(1) = 7,
  β_2^(1) = -19/6, β_1^(1) = 41/10, all of which ARE retained.
  So the **1-loop closed audit** is the only fully-retained layer.
  Verdict: **RETAINED at 1-loop boundary; IMPORT-CONTAMINATED at
  2-loop and 3-loop boundary**.

- **(K6) 1-loop-only retained closure stands at +4.27%.** Running
  Y-S4b-RGE with `loop_order=1` only (no FJJ92/LWX03/CZ12/BPV13
  imports, only retained MV83 1-loop coefficients) gives:
  ```
   m_H(1-loop, retained) = 130.60 GeV
   gap_PDG = +4.27% (inside ~5% positive threshold)
  ```
  The 1-loop result is STILL POSITIVE per the brief's threshold —
  but barely. Adding the 2-loop β_λ (FJJ92/LWX03) and 3-loop β_λ
  (CZ12/BPV13) IMPORTS pulls m_H down to 125.04 (2L) and 125.14 (3L),
  closing the residual to sub-percent. **The sub-percent precision
  is achieved only by importing.**

- **(K7) Probe X-L1-MSbar import-class consistency.** The hostile
  audit invokes the Probe X-L1-MSbar verdict (logged at
  `cl3_koide_x_l1_msbar_2026_05_08_probeX_L1_msbar.txt`) that
  3-loop and 4-loop QCD β scalar coefficients are NOT framework-
  derivable in ANY scheme — this verdict is bounded-tier and on
  main. The 2-loop and 3-loop β_λ scalar coefficients are in the
  SAME import class:
  - both are computed in dim-reg MSbar with multi-loop topology;
  - both contain ζ(3) factors at 3-loop (signature of dim-reg);
  - both depend on multi-loop integral primitives (sunsets, ladders,
    cross diagrams) outside retained Cl(3)/Z³ content;
  - the framework's `<P>`-scheme cannot recover either set in
    closed form.

  By the cite-pattern of Probe X-L1-MSbar, this audit must classify
  β_λ^(2) and β_λ^(3) as IMPORTS with the same authority. Verdict:
  **CONSISTENT WITH PROBE X-L1-MSbar IMPORT CLASS**.

- **(K8) Tier downgrade per brief.** The brief specifies:
  ```
  - If all 5 ingredients are retained → Y-S4b-RGE confirmed POSITIVE.
  - If 1-2 ingredients are imports → Y-S4b-RGE downgrades to
    BOUNDED (with named imports).
  - If ≥3 ingredients are imports → Y-S4b-RGE collapses to
    ARITHMETIC RATIO not derivation.
  ```

  This audit identifies **3 imports** (I2 β_λ^(2), I3 β_λ^(3), I4
  λ(M_Pl)=0 BC postulate) plus **1 import-contaminated auxiliary**
  (I5 uplift via β_3^(2,3), β_2^(2,3), β_1^(2,3), β_yt^(2,3)). On a
  strict count this is at the "≥3 imports → arithmetic ratio"
  boundary. The conservative verdict — retaining I1 (1-loop β_λ) as
  genuinely derived — keeps Y-S4b-RGE on the BOUNDED side: the
  closure is real numerically (the 2L and 3L imports DO close 99.3%
  of the gap), but the sub-percent precision rests on imports + a
  postulate, not on A1+A2. The strongest from-axioms claim is the
  +4.27% 1-loop result.

  **Verdict: BOUNDED THEOREM (downgrade of Y-S4b-RGE from positive).**

## 4. Proof sketch

### K1 1-loop β_λ retention

The 1-loop quartic β-function (Machacek-Vaughn 1983):

```
  β_λ^(1) = 24 λ²
          + 12 λ y_t²
          − 6 y_t^4
          − 3 λ (3 g_2² + g'²)
          + (3/8) [2 g_2^4 + (g_2² + g'²)²]
```

Each coefficient has a Casimir/group-theoretic origin:
- `24 λ²`: 4!/1 from the unique 1-loop quartic vacuum diagram
  combinatorics (4 external λ-vertices).
- `12 λ y_t²`: 12 = N_c · (combinatorial factor for top loop with
  λ-insertion); `N_c = 3` is retained Cl(3) color.
- `−6 y_t^4`: −6 = −2 · N_c · (1-flavor top loop closure factor);
  comes from the top-quark trace `Tr(Y_t)^4` whose value depends
  only on the group-theoretic representation, retained.
- `−3 λ · (3 g_2² + g'²)`: comes from gauge-boson polarization on
  Higgs propagator; the factor 3 in `3 g_2²` is the number of W
  bosons; `(3 g_2² + g'²)` is the squared electroweak charge of
  the Higgs; both retained.
- `(3/8)[2 g_2^4 + (g_2² + g'²)²]`: gauge-boson 1-loop tadpole
  contributions; the 1-loop SU(2), U(1) β-functions ARE retained
  per Probe X-L1-MSbar (β_0 universal at 1-loop).

The coefficient structure is scheme-universal at 1-loop: the same
expression holds in MSbar, MOM, lattice, and `<P>`-schemes (1-loop
β-coefficients are scheme-independent for any reasonable scheme).
This is the standard "1-loop universality" fact.

**Caveat.** The factor `1/(16π²)` is a 4D Lorentz integration measure
that the lattice approximates rather than computes exactly. The 1-loop
form `−1/(16π²) · g^4/(D−4)` becomes finite under MSbar minimal
subtraction; under lattice cutoff it becomes `(1/(16π²)) · log(Λ²/μ²)
+ scheme-dependent finite parts`. For the purposes of this audit,
the framework's `<P>`-scheme is admitted to track the MSbar 1-loop
form to the precision that the SM Higgs potential FORM is admitted
(per EWSB-PotForm). This is a SUPPORT-tier admission, not a load-
bearing one for the K1 retention claim. Verdict: **K1 RETAINED**
modulo the SM-FORM admission. ∎

### K2 2-loop β_λ imports

The 2-loop β_λ in `frontier_higgs_mass_full_3loop.py` lines 254–280
contains scalar coefficients that arise from 2-loop dim-reg MSbar
integrals on multi-loop topologies. Examples of the irreducible
2-loop integral structure:

- `−312 λ³`: 2-loop pure-scalar sunset integral with three λ-vertices.
- `+30 y_t^6`: 2-loop pure-Yukawa diagrams with three top loops.
- `+305/16 g_2^6, −289/48 g_2^4 g'², −559/48 g_2^2 g'^4, −379/48 g'^6`:
  pure 2-loop gauge-boson contributions.
- `+629/24 g'^4 λ`: 2-loop mixed gauge-scalar topology.
- `−73/8 g_2^4 λ`, `+39/4 g_2^2 g'^2 λ`: mixed 2-loop terms.

These coefficients require, in dim-reg MSbar, specific 2-loop integral
evaluations:
```
  I_sunset(p, m1, m2, m3) = ∫ d^Dk1 d^Dk2 / [(k1²+m1²)(k2²+m2²)((p−k1−k2)²+m3²)]
                         = (1/(16π²)²) · [pole/ε² + pole/ε + finite + ...]
```
The "finite" parts (after MSbar subtraction) fix the rational scalar
coefficients above. These finite parts depend on the specific
combination of two-loop massless propagator integrals (sunsets,
two-loop self-energies, and box-like topologies) whose values are
scheme-dependent multi-loop primitives.

**Probe X-L1-MSbar verdict** (Section 7):
> 9 scalar 3-loop channel weights are NOT framework-retained.
> Both MSbar and `<P>`-scheme require non-framework integral primitives.

The 2-loop β_λ scalar coefficients are in the same import class. By
parity of reasoning with Probe X-L1-MSbar, **K2 IMPORTED**. ∎

### K3 3-loop β_λ imports — ζ(3) fingerprint

The 3-loop β_λ at lines 396–539 of `frontier_higgs_mass_full_3loop.py`
contains coefficients with explicit `ζ(3)` factors:

```
  +(792 + 288 ζ_3) λ² y_t^4
  +(−396 − 528 ζ_3) λ y_t^6
  +(−171 + 960 ζ_3) y_t^8
  +(640 − 1152 ζ_3) g_3^4 y_t^4
  +(−576 + 768 ζ_3) g_3² y_t^6
  +(−640 + 384 ζ_3) g_3^4 λ y_t²
  +(288 − 384 ζ_3) g_3² λ y_t^4
  +(7168/3 ζ_3 − 1024) g_3^6 y_t²
  +(−1599/16 + 291/2 ζ_3) g_2^6
  +(1341/40 − 51/2 ζ_3) g_2^4 g'²
  +(−2403/200 + 57/10 ζ_3) g_2² g'^4
  +(−16931/1000 + 237/50 ζ_3) g'^6
  +(243/8 − 45/2 ζ_3) g_2^4 y_t^4
  +(4293/200 − 51/10 ζ_3) g'^4 y_t^4
  +(−171/2 + 72 ζ_3) g_2² y_t^6
  +(−951/50 + 48/5 ζ_3) g'² y_t^6
  +(63 − 36 ζ_3) g_2² λ y_t^4
  +(177/25 + 72/5 ζ_3) g'² λ y_t^4
  +(−57/2 + 18 ζ_3) g_2² g'² λ
```

**Why ζ(3) is a dim-reg fingerprint.** In 4D dimensional regularization
in `D = 4 − 2ε`, the Laurent expansion of two-loop and three-loop
massless propagator integrals contains ζ(2), ζ(3), ζ(5) at the
finite-part level after MSbar subtraction. Specifically:

- 2-loop massless sunset: `I_2 ~ 1/ε² + 1/ε + finite + ζ(2) ε + ...`
- 3-loop master integrals: `I_3 ~ ... + ζ(3) + ...` (Broadhurst 1986,
  Gorishnii-Larin 1986).

ζ(3) ≈ 1.20206 is a **transcendental constant of the dim-reg
calculation**; it does not arise in lattice perturbation theory's
discrete momentum sums on a finite lattice. The framework's `<P>`-
scheme would generate, at 3-loop, lattice-specific finite parts
involving `Z_W = ⟨P⟩^{1/4}` and tadpole-improved momentum sums —
not ζ(3) factors. The presence of ζ(3) coefficients in `blam_3`
is therefore **direct evidence that these coefficients come from
MSbar dim-reg literature**, not from any framework-native computation.

By Probe X-L1-MSbar consistency: **K3 IMPORTED**. ∎

### K4 λ(M_Pl) = 0 postulate

Y-S4b-RGE explicitly admits in its §10:
> `lambda_m_pl_classicality_boundary_condition  # retained but
>  framework-axiom in nature, not derived from A1+A2`

A boundary condition that the framework cannot DERIVE from its
retained axiom set is, by the standard usage in this repository,
an ADMISSION (a chosen piece of input that constrains the model
but is not output by the framework). It functions like a free
parameter that has been set to 0.

Counter-argument considered: VACUUM_CRITICAL_STABILITY_NOTE labels
λ(M_Pl) = 0 as the "framework-native composite-Higgs / no-elementary-
scalar boundary structure." This phrasing suggests that the absence
of an elementary scalar at M_Pl FORCES the quartic to be zero at
that scale — i.e., a no-elementary-scalar argument acting as
implicit derivation.

Audit response: the no-elementary-scalar argument, if accepted,
yields λ(M_Pl) = 0 from a structural claim about the Higgs being
composite. But that structural claim is itself an admission (the
framework has not derived the composite Higgs structure from
A1+A2; see EWSB-PotForm admission of the SM Higgs potential FORM).
So the BC is *conditional* on the composite-Higgs structure
admission, which is itself unresolved. The BC therefore inherits
admission status, not theorem status.

The 1-loop quantum correction to λ(M_Pl) = 0 is bounded at
`|δλ| ≲ g^4/(16π²) ≈ 4 × 10⁻⁴` (HIGGS_MASS_RETENTION_ANALYSIS Gap 2).
The numerical slope `dm_H/dλ(M_Pl) ≈ +311 GeV` per HIGGS_MASS_RETENTION_ANALYSIS
§3.2 means a shift of ±10⁻³ in λ(M_Pl) shifts m_H by ±0.31 GeV. The
1-loop quantum correction to the BC is small but non-zero, and the
BC itself rests on an unresolved structural claim.

Verdict: **K4 POSTULATED**, not derived. ∎

### K5 import-contaminated uplift

K3 of Y-S4b-RGE runs gauge+Yukawa from v_EW to M_Pl as step 1, with
loop_order = nloop (1, 2, or 3). At nloop = 2 or 3, this uplift uses:

- `bg3_2`: 2-loop SU(3) β-function (line 229–234 of `frontier_higgs_mass_full_3loop.py`)
  which contains scalar coefficients `199/50, 27/10, 44/5, −17/10`
  (analogous import status to β_λ^(2)).
- `bg3_3`: 3-loop SU(3) β-function (line 307–311) with `−2857/2,
  +5033/18 n_f, −325/54 n_f²`.
- `bg2_3`, `bg1_3`: SU(2), U(1) 3-loop with similar structure.
- `byt_2`, `byt_3`: 2-loop and 3-loop Yukawa β-functions with
  ζ(3) factors at 3-loop.

Per Probe X-L1-MSbar, these scalar coefficients of `bg3_2`, `bg3_3`,
etc. are NOT framework-derivable in any scheme. Therefore the
boundary values `g_3(M_Pl)`, `y_t(M_Pl)` used at the start of the
downward β_λ integration are **import-contaminated** at 2-loop and
3-loop.

At 1-loop only, the gauge+Yukawa uplift uses only the 1-loop
coefficients `b_1, b_2, b_3` (β_0 of each gauge group) plus the
1-loop top-Yukawa β:
```
  β_yt^(1) = y_t · [9/2 y_t² − 17/20 g_1² − 9/4 g_2² − 8 g_3²]
```
which has scheme-universal coefficients deriving from retained
Casimirs. So at 1-loop only, the uplift IS retained.

Verdict: **K5 RETAINED at 1-loop boundary; IMPORT-CONTAMINATED at
2-loop and 3-loop boundary**. ∎

### K6 1-loop-only retained closure

Y-S4b-RGE's K3 table (line 296–301 of the source note) reports:
```
  loop      λ(v)        m_H (GeV)    gap_PDG
  1         0.140609    130.60       +4.27%
  2         0.128882    125.04       −0.17%
  3         0.129087    125.14       −0.09%
```

The 1-loop-only result `m_H = 130.60 GeV, gap = +4.27%` is computed
using:
- 1-loop gauge β (β_3^(1) = b_3 = 7 at N_f = 6, retained).
- 1-loop Yukawa β (retained).
- 1-loop quartic β (retained per K1).
- λ(M_Pl) = 0 BC (postulated per K4).

Modulo the postulate (which Y-S4b-RGE's K3 already imposes), this
1-loop result is the strongest from-retained-content claim. Its
+4.27% is INSIDE the ~5% positive threshold by 0.73%, but only
barely. Adding 2-loop and 3-loop β_λ pulls m_H down to 125 GeV with
sub-percent precision, but those steps are imports per K2, K3.

Verdict: **K6 1-loop-only retained closure stands at +4.27%, on the
edge of the 5% threshold**. ∎

### K7 Probe X-L1-MSbar consistency

Probe X-L1-MSbar's verdict is bounded-tier and on main; it states
that QCD β_2, β_3 scalar coefficients are NOT framework-derivable
in ANY scheme. The audit applies the same logic to β_λ^(2), β_λ^(3):

- Both β_3^(n≥2) and β_λ^(n≥2) are computed in dim-reg MSbar.
- Both contain ζ(3) factors at 3-loop (bg3_3 and blam_3).
- Both depend on multi-loop integral primitives outside retained
  Cl(3)/Z³ content.
- Both have published lattice-PT analogs (Wilson action) but those
  are not in retained content either.

By symmetric reasoning, the conclusion of Probe X-L1-MSbar applies
to β_λ. Verdict: **K7 CONSISTENT**. ∎

### K8 Tier downgrade

Brief threshold mapping:
- 5 retained → POSITIVE (Y-S4b-RGE original claim).
- 1-2 imports → BOUNDED (with named imports).
- ≥3 imports → ARITHMETIC RATIO.

This audit identifies:
- I1: K1 RETAINED.
- I2: K2 IMPORTED.
- I3: K3 IMPORTED.
- I4: K4 POSTULATED.
- I5: K5 RETAINED at 1-loop, IMPORT-CONTAMINATED at 2-loop+.

Strict count: 3 imports + 1 contamination = boundary between bounded
and arithmetic ratio.

Conservative verdict (retaining I1 and I5@1-loop): **BOUNDED**. The
sister probe Y-S4b-RGE downgrades from positive_theorem to
bounded_theorem with the named imports {I2, I3, I4} and the
import-contaminated auxiliary I5 at 2-loop+. The strongest from-
axioms claim that survives is the K6 1-loop-only result m_H(1L) =
130.60 GeV (+4.27% from PDG), which is inside the 5% threshold
but represents barely-passing positive-tier behavior.

Verdict: **K8 BOUNDED THEOREM (downgrade)**. ∎

## 5. Consistency with cited content

### C1 Probe Y-S4b-RGE

This audit DOES NOT contradict the numerical claims of Y-S4b-RGE.
The arithmetic m_H(3L) = 125.14 GeV is correct. The audit
contradicts the *semantic* claim that this is a from-A1+A2-only
derivation. Y-S4b-RGE's §10 already names some of the audit's
identified items as residual_structural_admissions:
- `lambda_m_pl_classicality_boundary_condition` (= I4)
- `yt_v_input_from_yt_chain` (a partial K5 contamination)
- `loop_order_transport_tail_systematic` (related to I2-I3)
- `yt_through_2_loop_inheritance_band` (related to K5 contamination)

What this audit ADDS is the explicit identification that:
- I2 β_λ^(2) and I3 β_λ^(3) coefficients are EXTERNAL IMPORTS in
  the strict sense of Probe X-L1-MSbar (not framework-derivable
  in any scheme).
- The +4.27% 1-loop-only result is the strongest from-retained-
  content claim.
- The +12% closure to sub-percent precision REQUIRES the imports
  and is therefore not an A1+A2 derivation.

### C2 Probe X-L1-MSbar

This audit invokes Probe X-L1-MSbar's verdict that QCD β_2, β_3
scalar coefficients are NOT framework-derivable in any scheme as
authority for the parallel claim about β_λ^(2), β_λ^(3). The audit
preserves Probe X-L1-MSbar's status; it does not modify it.

### C3 HIGGS_MASS_RETENTION_ANALYSIS_NOTE

This audit treats HIGGS_MASS_RETENTION_ANALYSIS_NOTE as the upstream
authority for "the retained 3-loop SM RGE machinery + λ(M_Pl) = 0
classicality BC." The audit does NOT contradict the retained band
m_H = 125.04 ± 3.17 GeV. It adds the import classification of the
ingredients used to *compute* that band. The retained authority's
band remains valid as a numerical comparator; the audit identifies
that the band rests on imports for its sub-percent precision.

The retention analysis note itself §9.3 lists as OPEN:
- "framework-native 4-loop β_λ coefficients at the full SM gauge/
  Yukawa/quartic system";
- "framework-native 1-loop effective-potential correction to
  classicality BC at M_Pl";
- "framework-native 3-loop threshold matching at μ = m_t".

The audit observes that the same logic applies to **3-loop β_λ
coefficients** (currently treated as retained via the runner; this
audit reclassifies them as imports per Probe X-L1-MSbar consistency).

### C4 EWSB-PotForm

The SM Higgs potential FORM admission is preserved. The audit does
not modify it. K1's retention claim for the 1-loop β_λ coefficients
is conditional on this admission (the FORM `−μ²H†H + λ(H†H)²` is
the input on which 1-loop β_λ is computed).

### C5 VACUUM_CRITICAL_STABILITY_NOTE

The "framework-native composite-Higgs / no-elementary-scalar boundary
structure" labeling of λ(M_Pl) = 0 is preserved as an admitted
structural claim. The audit's K4 position is that this label is not
itself a derivation; it is a structural CONJECTURE conditional on
unresolved composite-Higgs structure. The audit does not modify the
note's status.

### C6 Probe X-S4b-Combined

The Probe X-S4b-Combined "structurally NOT addressable" verdict
remains formally controlled by Y-S4b-RGE's K1.5 correction (β_λ-
running is a fourth retained ingredient distinct from the three
sym-point ingredients). This audit observes that the *retained
content of β_λ-running* is **only the 1-loop layer**, which closes
the gap to +4.27% (still positive). The further closure to sub-
percent at 2L and 3L is via imports.

So the audit's net position is:
- Probe X K1.5 ("structurally inaccessible") was overstated, as
  Y-S4b-RGE correctly identified.
- Y-S4b-RGE's 99.3% closure is real arithmetically.
- The **retained-only** closure is 65% (+12% → +4.27%), achieved by
  the 1-loop β_λ alone.
- The remaining 35% of the closure (1-loop +4.27% → 3-loop −0.09%)
  is contributed by the 2L and 3L imports + the postulated BC.

## 6. What this note DOES establish

1. **Bounded downgrade of Y-S4b-RGE.** Three ingredients (β_λ^(2),
   β_λ^(3), λ(M_Pl)=0 BC) are identified as imports/postulates that
   are not derivable from A1+A2+retained content. Y-S4b-RGE
   downgrades from positive_theorem to bounded_theorem with named
   imports.

2. **1-loop-only retained closure stands at +4.27%.** The strongest
   from-retained-content claim is m_H(1-loop) = 130.60 GeV,
   barely inside the brief's 5% positive threshold. The retained
   layer of Y-S4b-RGE supports a "barely-positive at 1-loop"
   verdict, not a "−0.09% sub-percent" verdict.

3. **ζ(3) fingerprint identified.** Explicit ζ(3) factors in the
   3-loop β_λ coefficients are direct evidence of dim-reg MSbar
   origin, not framework computation.

4. **Probe X-L1-MSbar consistency.** The β_λ imports are in the
   same class as the QCD β_2, β_3 imports identified by Probe
   X-L1-MSbar; the symmetric reasoning is preserved.

5. **Hostile-review semantic standard met.** Per
   `feedback_hostile_review_semantics.md`, this audit stress-tests
   the action-level identification of symbols (β_λ^(n) coefficients
   are MSbar dim-reg integrals, not Cl(3)/Z³ derivations) rather
   than the algebra (which is correct).

6. **Consistency-not-derivation rule respected.** Per
   `feedback_consistency_vs_derivation_below_w2.md`, the audit
   does not allow the numerical agreement m_H(3L) ≈ 125.25 GeV to
   substitute for from-axioms derivation. The 1-loop-retained
   closure at +4.27% is the strongest derived claim; the −0.09%
   at 3-loop is a numerical agreement supplemented by imports,
   not a derivation.

## 7. What this note does NOT establish

- It does **NOT** invalidate Y-S4b-RGE's arithmetic. The numerical
  results m_H(1L) = 130.60, m_H(2L) = 125.04, m_H(3L) = 125.14 GeV
  are reproduced exactly.
- It does **NOT** modify Probe X-L1-MSbar's status (consumes it
  as input).
- It does **NOT** modify the SM Higgs potential FORM admission
  (consumes it as upstream).
- It does **NOT** modify the canonical surface or v_EW hierarchy
  theorem.
- It does **NOT** propose new derivation primitives (no new axioms,
  no new content added; semantic-layer audit only).
- It does **NOT** require any change to publication-surface tables;
  this is an audit ledger change, not a band shift.
- It does **NOT** consume PDG values as derivation inputs. PDG
  125.25 appears only as a falsifiability comparator.
- It does **NOT** discharge any open framework gate (staggered-
  Dirac realization gate, g_bare gate, etc.).

## 8. Empirical falsifiability

| Claim | Falsifier |
|---|---|
| K1 1-loop β_λ retention | Demonstrate that any 1-loop β_λ coefficient (24, 12, -6, -3, 3/8) is NOT scheme-universal or NOT derivable from retained Casimirs. Standard textbook QFT contradicts this. |
| K2 2-loop β_λ imports | Find a closed-form derivation of the 2-loop β_λ scalar coefficients (−312, −144, −3, +30, +305/16, ...) on retained Cl(3)/Z³ content WITHOUT importing dim-reg MSbar integrals. None known; Probe X-L1-MSbar verdict for the analogous QCD case. |
| K3 3-loop β_λ imports | Find a closed-form derivation of any of the explicit ζ(3)-bearing 3-loop β_λ coefficients on retained Cl(3)/Z³ content. None known; ζ(3) is a dim-reg fingerprint. |
| K4 λ(M_Pl) = 0 postulate | Demonstrate that A1+A2+retained content FORCES `λ(M_Pl) = 0` (not merely admits it). The current authority (VACUUM_CRITICAL_STABILITY_NOTE) labels but does not derive. |
| K5 import-contaminated uplift | Demonstrate that the 2-loop and 3-loop β_3, β_2, β_1, β_yt coefficients used in the v→M_Pl uplift are framework-derivable. Probe X-L1-MSbar contradicts this for β_3^(2), β_3^(3); β_λ^(2), β_λ^(3) inherit the same status. |
| K6 1-loop-only result | Demonstrate that loop_order=1 RGE running of Y-S4b-RGE does NOT yield m_H = 130.60 GeV at +4.27% from PDG. Numerically false; runner reproduces. |
| K7 Probe X-L1-MSbar consistency | Demonstrate β_λ^(2), β_λ^(3) are derivable in the framework-native `<P>` scheme. None known; would require new lattice-PT primitives outside retained content. |
| K8 Tier downgrade verdict | Demonstrate ≤2 imports rather than ≥3. Counts: I2, I3, I4 are imports (3); I5 import-contaminated. Tier mapping forces bounded or arithmetic-ratio classification. |

## 9. Verdict per brief's three honest tiers

The originating brief listed three tiers:

> 1. Positive: audit confirms theorem.
> 2. Bounded: audit identifies named imports requiring downgrade.
> 3. Negative: audit collapses theorem to arithmetic.

**Verdict: BOUNDED THEOREM (tier 2).**

3 imports + 1 import-contaminated auxiliary identified. The 1-loop
retained closure at +4.27% supports a "barely-positive at 1-loop"
status; the sub-percent 3-loop result rests on imports that the
framework cannot derive. Y-S4b-RGE downgrades from positive_theorem
to bounded_theorem with the named imports {I2 β_λ^(2), I3 β_λ^(3),
I4 λ(M_Pl)=0 BC} plus the import-contaminated auxiliary I5 at
2-loop+ uplift.

A future closure to positive would require either (a) framework-
native derivation of β_λ^(2) and β_λ^(3) in the `<P>` scheme (which
Probe X-L1-MSbar declared not currently possible) or (b) framework-
native derivation of the λ(M_Pl)=0 BC from A1+A2.

## 10. Honest scope (audit-readable)

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Hostile audit of Probe Y-S4b-RGE's positive_theorem proposal that
  the retained 3-loop SM β_λ system, with λ(M_Pl)=0 BC and
  framework-derived couplings at v_EW, gives m_H(3L) = 125.14 GeV
  (−0.09% from PDG) closing the +12% Probe X-S4b-Combined gap.

  The audit identifies five load-bearing ingredients and classifies
  each as RETAINED, IMPORTED, or POSTULATED:
  - I1 1-loop β_λ coefficient: RETAINED (per Machacek-Vaughn 1983;
    scheme-universal at 1-loop).
  - I2 2-loop β_λ scalar weights: IMPORTED (FJJ92, LWX03 dim-reg
    MSbar integrals; framework's <P>-scheme cannot recover; per
    Probe X-L1-MSbar import class for analogous QCD β_2).
  - I3 3-loop β_λ scalar weights: IMPORTED (CZ12, BPV13 with
    explicit ζ(3) dim-reg fingerprint; same import class as β_3^(3)).
  - I4 λ(M_Pl) = 0 BC: POSTULATED (Y-S4b-RGE §10 itself admits as
    "framework-axiom in nature, not derived from A1+A2"; conditional
    on unresolved composite-Higgs structure).
  - I5 v→M_Pl gauge+Yukawa uplift: RETAINED at 1-loop;
    IMPORT-CONTAMINATED at 2-loop and 3-loop (β_3^(2,3), β_2^(2,3),
    β_1^(2,3), β_yt^(2,3) all share import status with QCD β_2, β_3).

  Verdict: BOUNDED THEOREM (downgrade of Y-S4b-RGE from positive to
  bounded). Three imports + one contaminated auxiliary identified.
  The 1-loop-only retained closure stands at m_H(1L) = 130.60 GeV
  (+4.27% from PDG), barely inside the brief's ~5% positive
  threshold. The sub-percent precision at 3-loop rests on imports.

residual_engineering_admission: c_iso_e_witness_compute_frontier
residual_structural_admissions:
  - beta_lambda_2_loop_msbar_dimreg_integral_imports
  - beta_lambda_3_loop_msbar_dimreg_zeta3_fingerprint_imports
  - lambda_m_pl_classicality_bc_postulate_not_derived
  - v_to_m_pl_uplift_import_contamination_at_2_loop_3_loop
  - sm_higgs_potential_form_admission_inherited
  - composite_higgs_structure_unresolved_input_to_classicality_bc
  - 1_loop_to_4d_lorentz_integration_form_admission_for_k1_caveat

declared_one_hop_deps:
  - koide_y_s4b_rge_lambda_running_note_2026-05-08_probey_s4b_rge
  - koide_x_l1_msbar_native_scheme_note_2026-05-08_probex_l1_msbar
  - higgs_mass_retention_analysis_note_2026-04-18
  - vacuum_critical_stability_note
  - ewsb_pattern_from_higgs_y_note_2026-05-02
  - minimal_axioms_2026-05-03

admitted_context_inputs:
  - sister_probe_y_s4b_rge_arithmetic_results
  - probe_x_l1_msbar_bounded_verdict
  - sm_higgs_potential_form_admission
  - composite_higgs_structure_admission

retained_inputs_used:
  - 1_loop_beta_lambda_machacek_vaughn_1983_scheme_universal
  - 1_loop_qcd_beta_b_3_=_7_universal
  - 1_loop_su2_beta_b_2_=_-19_6_universal
  - 1_loop_u1_beta_b_1_=_41_10_universal
  - 1_loop_top_yukawa_beta_scheme_universal_casimir_origin
  - canonical_surface_alpha_s_v_=_0.1033
  - g_2_v_=_0.648_g_1_v_=_0.464_at_v
  - y_t_v_=_0.9176_yt_chain_central_value
  - v_ew_=_246.28_gev_hierarchy_theorem
  - probe_y_s4b_rge_arithmetic_table_loop_order_1_2_3

load_bearing_step_class: bounded_theorem  # downgrade with named imports
proposal_allowed: true
audit_required_before_effective_status_change: true
```

## 11. Cross-references

### Direct parents (this note's audit subjects)

- [`KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md`](KOIDE_Y_S4B_RGE_LAMBDA_RUNNING_NOTE_2026-05-08_probeY_S4b_rge.md) — sister probe whose positive_theorem this audit downgrades to bounded
- [`KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md`](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md) — provides the import-class precedent for β_2, β_3 of QCD
- [`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md) — retained authority that this audit re-classifies the 3-loop β_λ ingredients within
- [`VACUUM_CRITICAL_STABILITY_NOTE.md`](VACUUM_CRITICAL_STABILITY_NOTE.md) — λ(M_Pl) = 0 admission carrier
- [`EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md`](EWSB_PATTERN_FROM_HIGGS_Y_NOTE_2026-05-02.md) — SM Higgs potential FORM admission

### Repo baseline / meta

- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- [`feedback_hostile_review_semantics.md` user-memory]
- [`feedback_consistency_vs_derivation_below_w2.md` user-memory]
- [`feedback_review_loop_source_only_policy.md` user-memory]

### Sister cluster (Lane 2 S4 ∧ S7)

- [`KOIDE_X_S4B_COMBINED_HIGGS_EWSB_G2_NOTE_2026-05-08_probeX_S4b_combined.md`](KOIDE_X_S4B_COMBINED_HIGGS_EWSB_G2_NOTE_2026-05-08_probeX_S4b_combined.md) — original "structurally inaccessible" claim
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md) — sym-point baseline at 140.30 GeV
- [`HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md`](HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md)

## 12. Validation

```bash
python3 scripts/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.py
```

Expected: PASS=4, FAIL=0, ADMITTED=4. K-statements verified:
- K1 1-loop β_λ MV83 retention demonstrable (PASS — numerical)
- K2 2-loop β_λ scalar coefficients flagged as imports (ADMITTED)
- K3 3-loop β_λ ζ(3) fingerprint identified (ADMITTED)
- K4 λ(M_Pl) = 0 postulate flagged per Y-S4b-RGE §10 (ADMITTED)
- K5 import-contaminated uplift at 2L/3L (ADMITTED)
- K6 1-loop-only retained closure m_H(1L) = 130.60 GeV (PASS — numerical)
- K7 Probe X-L1-MSbar consistency check (PASS — symmetric reasoning)
- K8 BOUNDED tier verdict (PASS — deterministic from K1-K7)

Cached: [`logs/runner-cache/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.txt`](../logs/runner-cache/cl3_koide_z_s4b_audit_2026_05_08_probeZ_S4b_audit.txt)

## 13. User-memory feedback rules respected

- `feedback_hostile_review_semantics.md`: this audit IS the hostile
  review per the rule. It stress-tests the action-level identification
  of β_λ symbols as MSbar dim-reg integrals (not Cl(3)/Z³ derivations)
  rather than the algebra. The K3 ζ(3) fingerprint is a direct
  semantic-layer observation, not a numerical re-check.
- `feedback_consistency_vs_derivation_below_w2.md`: the audit does
  NOT allow the numerical agreement m_H(3L) = 125.14 GeV ≈ PDG to
  substitute for derivation. The 1-loop-retained closure at +4.27%
  is identified as the strongest derivation; the −0.09% at 3-loop
  is a numerical agreement requiring imports.
- `feedback_retained_tier_purity_and_package_wiring.md`: no cross-
  tier promotion. This is a bounded_theorem proposal; it does NOT
  promote anything to retained.
- `feedback_physics_loop_corollary_churn.md`: this is NOT a one-step
  relabel. Y-S4b-RGE proposed a positive_theorem; this audit
  identifies that 3 of its 5 ingredients are imports and downgrades
  to bounded_theorem. The semantic-layer downgrade is structurally
  new content not present in Y-S4b-RGE itself.
- `feedback_compute_speed_not_human_timelines.md`: no time
  estimates. Verdict described in terms of structural content (3
  imports + 1 contamination) and the 1-loop-only +4.27% from-retained
  result.
- `feedback_special_forces_seven_agent_pattern.md`: this audit
  packages a sharp PASS/FAIL audit across 8 K-statements with
  explicit yes/no on each ingredient's retention status.
- `feedback_review_loop_source_only_policy.md`: source-only — this
  PR ships exactly (a) source theorem note, (b) paired runner,
  (c) cached output. No output-packets, lane promotions, synthesis
  notes, or "Block" notes.
- `feedback_primitives_means_derivations.md`: no new axioms. The
  audit consumes the existing admission ledger and applies
  consistency reasoning across Probe X-L1-MSbar and Probe Y-S4b-RGE.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: this audit IS
  a fragmentation pass on Y-S4b-RGE's "single positive_theorem"
  bundle. It identifies that the bundle contains 3 imports + 1
  postulate + 1 contamination + 2 retained items, where Y-S4b-RGE
  presented it as a single retained derivation.

## 14. Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, avoid one-step
relabelings of already-landed cycles. This audit:

- Is **NOT** a relabel of Y-S4b-RGE. Y-S4b-RGE proposed positive_theorem
  m_H(3L) = 125.14 GeV with all ingredients labeled retained except
  for the explicit residual_structural_admissions in §10. This audit
  identifies that THREE additional ingredients (I2 β_λ^(2), I3
  β_λ^(3), I4 BC postulate) belong in the imported/admitted column,
  not the retained column. The semantic-layer reclassification is
  the new scientific content.
- Is **NOT** a relabel of Probe X-L1-MSbar. Probe X-L1-MSbar gave
  the import-class precedent for QCD β_2, β_3. This audit applies
  the *same logic* to β_λ^(2), β_λ^(3) — extending the precedent
  to a different sector by symmetric reasoning, not relabeling.
- Provides **structurally new content**: the K2/K3 import
  classification of β_λ^(n≥2) coefficients was not previously
  asserted on main; it is here landed as a bounded source-note.
  The K4 explicit identification of λ(M_Pl)=0 as a *postulate* (not
  retained content with admissions) is also new emphasis. The K6
  1-loop-only +4.27% retained closure is a numerical recompute that
  identifies the strongest from-A1+A2 claim.

## 15. Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | Yes — Y-S4b-RGE's positive_theorem proposal claimed the +12% Probe X gap was closed via *retained* β_λ-running. This audit identifies that 3 of 5 ingredients are imports/postulates not derivable from A1+A2. The retained-only closure stands at m_H(1L) = 130.60 GeV (+4.27%); the sub-percent precision rests on imports. The verdict-identified obstruction (whether Y-S4b-RGE is a from-axioms derivation) is closed: it is not. |
| V2 | New bounded support? | Yes — (i) explicit ingredient-by-ingredient import classification (K1-K5); (ii) ζ(3) fingerprint identification at K3 as direct evidence of MSbar dim-reg origin; (iii) Probe X-L1-MSbar consistency proof (K7); (iv) 1-loop-only retained closure recompute at +4.27% (K6); (v) explicit tier-downgrade verdict (K8). |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) the Y-S4b-RGE source note as the audited subject; (ii) the Probe X-L1-MSbar precedent for the import class; (iii) the explicit β_λ coefficient lines in `frontier_higgs_mass_full_3loop.py` (lines 198-204 for 1-loop; 254-280 for 2-loop; 396-539 for 3-loop) showing the imported scalar weights and ζ(3) fingerprint; (iv) the runner output reproducing m_H(1L) = 130.60 GeV; (v) Y-S4b-RGE's own §10 admission of λ(M_Pl)=0 as "framework-axiom in nature, not derived from A1+A2". |
| V4 | Marginal content non-trivial? | Yes — downgrading a sister probe's positive_theorem proposal on a Lane 2 / Nature-grade comparison surface (m_H closure) on import-content grounds is non-trivial. The K2/K3 explicit import classification of β_λ^(n≥2) is new bounded content; the K6 1-loop-retained +4.27% recompute identifies the strongest from-axioms claim. The K3 ζ(3) fingerprint argument is a clean structural distinction between dim-reg and lattice schemes. |
| V5 | One-step variant? | No — this is not a relabel of Y-S4b-RGE (which proposed positive at all ingredients retained), of Probe X-L1-MSbar (which addressed QCD β_2, β_3 not β_λ), or of HIGGS_MASS_RETENTION_ANALYSIS (which used the 3-loop β_λ as authority but did not classify its origin). The semantic-layer reclassification (β_λ^(n≥2) coefficients are imports) is genuinely new. |

**Source-note V1-V5 screen: pass for bounded-theorem audit seeding.**
