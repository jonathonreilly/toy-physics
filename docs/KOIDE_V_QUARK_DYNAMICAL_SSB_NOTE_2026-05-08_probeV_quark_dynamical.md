# Probe V-Quark-Dynamical — Heavy-Quark Masses via Dynamical Chiral SSB + Retained Yukawa Flow: Bounded-Tier Source Note (NEGATIVE)

**Date:** 2026-05-10
**Claim type:** no_go (negative for the heavy-quark closure
gate; the chiral-SSB structural argument does NOT bridge the heavy-quark
Yukawa-BC gap)
**Sub-gate:** Lane 1 follow-up to Probes X-L1-Threshold (PR #933),
Y-L1-Ratios (PR #946), Z-Quark-QCD-Chain (PR #958) — alternative-mechanism
test for heavy quarks
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.

**Primary runner:** [`scripts/cl3_koide_v_quark_dynamical_2026_05_08_probeV_quark_dynamical.py`](../scripts/cl3_koide_v_quark_dynamical_2026_05_08_probeV_quark_dynamical.py)
**Cached output:** [`logs/runner-cache/cl3_koide_v_quark_dynamical_2026_05_08_probeV_quark_dynamical.txt`](../logs/runner-cache/cl3_koide_v_quark_dynamical_2026_05_08_probeV_quark_dynamical.txt)

## 0. Probe context

Three single-chain probes have foreclosed routes for heavy-quark masses
on a single coupling-chain anchor:

- **Probe X-L1-Threshold** (PR #933): EW Wilson chain ABSOLUTE heavy-
  quark masses — NEGATIVE (residues 0.09–0.48 → 21–57% mass errors).
- **Probe Y-L1-Ratios** (PR #946): EW Wilson chain heavy-quark mass-
  RATIO integer-differences — NEGATIVE (best m_b at Δn = −1/3 → 5.4%;
  m_c at +1/6 → 6.2%; m_t at −11/6 → 16.1%).
- **Probe Z-Quark-QCD-Chain** (PR #958): parallel QCD-anchored chain
  `m_q = Λ_QCD × C × α_s^{n_q}` — NEGATIVE (per-quark single-`C` hits
  use three different `C` values; no retained single-`C` closes triplet
  at 1% gate).

All three probes assumed **heavy quarks must be reached by the SAME
chain mechanism that closes m_τ at 0.017% precision** (Probe 19).

This probe asks the structurally distinct question:

> *What if heavy quarks DO NOT use a chain mechanism at all?*

**Physical motivation.** m_τ is "passive": Yukawa small (`y_τ ~ 0.01`),
RGE running negligible from M_Pl to v, chain identification works.
Heavy quarks (c, b, t) are RGE-ACTIVE: large Yukawas (`y_t ~ 1`,
`y_b ~ 0.024`, `y_c ~ 0.007`), QCD condensate `<q̄q> ~ Λ_QCD³`,
dynamical mass generation via chiral spontaneous symmetry breaking
(chiral SSB).

The actual physics decomposes a quark mass as:

```
m_q = m_q^current + m_q^chiral
```

where:
- `m_q^current = y_q(v_EW) × v_EW / √2` — Higgs-Yukawa contribution
- `m_q^chiral ~ Σ^{1/3} ~ Λ_QCD` — chiral SSB constituent shift

For LIGHT quarks (u, d, s): chiral SSB dominates (constituent ~330 MeV
vs current few MeV). For HEAVY quarks (c, b, t): Yukawa dominates;
chiral SSB correction `~ Λ_QCD³ / m_q²` is small. m_b and m_c sit in
a transition regime where both contribute.

**Goal.** Test whether the physical `Cl(3)` local algebra + `Z^3`
spatial substrate content plus chiral SSB
structural argument + retained Yukawa flow gives `m_b`, `m_c` (and
possibly `m_t` separately) within ~5% of PDG.

**Pre-computed reference points.**
- Retained `m_t = 169.51 GeV (-1.84%)` via species-PRIVILEGED Ward BC
  per [`YT_ZERO_IMPORT_CHAIN_NOTE.md`](YT_ZERO_IMPORT_CHAIN_NOTE.md).
  This chain treats `y_b(v)`, `y_c(v)` as INFRASTRUCTURE inputs (held
  at observed values) and does NOT derive their absolute scales.
- Species-UNIFORM Ward BC `y_t(M_Pl) = y_b(M_Pl) = g_lattice/√6` +
  2L SM RGE per [`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md):
  `m_b(m_b) ≈ 140 GeV` (33× overshoot of PDG 4.18 GeV); `m_t ≈ 99 GeV`
  (43% undershoot). FALSIFIED.

## 1. Theorem (bounded, negative — chiral SSB does NOT bridge heavy-quark Yukawa gap)

**Theorem (V-Quark-Dynamical; bounded no-go).** On physical
`Cl(3)` local algebra + `Z^3` spatial substrate content plus retained Wilson-chain inputs `(M_Pl, ⟨P⟩,
α_bare, u_0, α_LM, v_EW)` plus retained-bounded QCD content
`(Λ_QCD, α_s(M_Z))` plus the **IMPORTED chiral SSB constituent shift
`Σ^{1/3} ~ 330 MeV`** (Banks-Casher / ChPT phenomenology, NOT retained
per [`HADRON_LANE1_CHIRAL_CONDENSATE_BANKS_CASHER_SCOPING_SUPPORT_NOTE_2026-04-27.md`](HADRON_LANE1_CHIRAL_CONDENSATE_BANKS_CASHER_SCOPING_SUPPORT_NOTE_2026-04-27.md)),
the heavy-quark masses `m_b` and `m_c` are NOT derivable to the 5%
precision gate via:

```
m_q = m_q^current + m_q^chiral                 [V-Quark-Dynamical]
m_q^current = y_q(v_EW) × v_EW / √2            [Higgs-Yukawa]
m_q^chiral ~ Σ_constituent ≈ 330 MeV           [chiral SSB shift]
```

with **any retained-derivable boundary condition for `y_q(M_Pl)`** that
respects the physical `Cl(3)` local algebra + `Z^3` spatial substrate
baseline plus the retained Ward identity.

Specifically:

1. **(Species-UNIFORM Ward BC + 1L SM Yukawa RGE FALSIFIED for m_b, m_c.)**
   Setting `y_t(M_Pl) = y_b(M_Pl) = y_c(M_Pl) = g_lattice/√6 = 0.4358`
   (Block 6 species-uniform Clebsch-Gordan extension of the retained
   Ward identity to all Q_L species) and forward-running the 1L SM
   coupled `(y_t, y_b, g_3)` system from `M_Pl` to `v_EW` converges
   at the 1L coupled fixed-point to `(y_t, y_b)(v) ≈ (0.755, 0.755)`.
   This gives:
   - `m_t ≈ 131.4 GeV` (24% undershoot of PDG 172.69 GeV)
   - `m_b(v) ≈ 131.4 GeV`; `m_b(m_b) ≈ 190.5 GeV` after standard QCD
     running (`v → m_b`) — **45.6× overshoot of PDG 4.18 GeV**.

   1L is more severe than the YT_BOTTOM 2L result (~140 GeV) due to
   coupled fixed-point back-reaction on `g_3`. The species-uniform BC
   is FALSIFIED in both cases.

2. **(Chiral SSB additive correction bridges <1% of the gap.)** With
   chiral SSB constituent shift `Σ_constituent ≈ 330 MeV` (IMPORTED
   from ChPT phenomenology), the closure attempt
   `m_b ≈ y_b(v) × v/√2 + Σ_constituent` shifts the species-uniform
   1L forecast from `190.5 GeV` to `190.8 GeV`. The gap to PDG `4.18 GeV`
   is `186 GeV`; the chiral SSB correction bridges `0.330/186 = 0.18%`
   of this gap. **Chiral SSB cannot rescue the species-uniform Yukawa
   forecast.**

3. **(Heavy-quark chiral SSB is structurally sub-dominant.)** Σ as a
   fraction of PDG:
   - `Σ/m_t = 0.19%` (negligible)
   - `Σ/m_b = 7.89%` (sub-dominant)
   - `Σ/m_c = 25.98%` (significant but cannot bridge a 100%-scale gap
     additively)

   Chiral SSB is structurally a LIGHT-quark constituent-mass mechanism,
   not a HEAVY-quark Yukawa-hierarchy mechanism. For light quarks
   (u, d, s) the additive `m_q = m_q^current + Σ` reproduces the
   constituent-mass benchmark within 15% (u: −1.1%, d: −1.6%,
   s: −12.9%) — but the LIGHT-quark `m_q^current` is itself NOT
   retained from the physical `Cl(3)` local algebra + `Z^3` spatial
   substrate content (same species-differentiation obstruction).

4. **(Species-PRIVILEGED top-only chain reproduces retained m_t but
   does not derive m_b, m_c.)** The retained YT_ZERO_IMPORT chain
   uses `y_t(M_Pl) = g_lattice/√6` as the species-privileged BC and
   holds `y_b(v) ≈ 0.016`, `y_c(v) ≈ 0.007` as INFRASTRUCTURE inputs
   (observed values, used only for v→M_Z cross-check). This chain
   delivers `m_t = 169.47 GeV (-1.86% from PDG)`. It is RETAINED for
   m_t but **does NOT derive `m_b` or `m_c` absolute scales**.

5. **(Retained CKM-dual ratio is consistent but does not close
   absolute scale.)** The bounded down-type CKM-dual lane gives
   `m_s/m_b = (α_s(v)/√6)^{6/5} = 0.02239` vs threshold-local PDG
   `m_s(2 GeV)/m_b(m_b) = 0.02234` (+0.20%). This is RETAINED-BOUNDED
   for the ratio but `DOWN_TYPE_MASS_RATIO_CKM_DUAL §6` explicitly
   disclaims absolute m_b closure.

## 2. Hostile-review tier classification (per Z-S4b-Audit pattern)

Following [`feedback_hostile_review_semantics.md`](../.claude/projects/-Users-jonreilly-Projects-Physics/memory/feedback_hostile_review_semantics.md)
and the Z-S4b-Audit hostile-review pattern (PR #956), the five
load-bearing ingredients are tiered:

| Ingredient | Tier | Detail |
|---|---|---|
| **I1** 1L SM Yukawa β-function (gauge + Yukawa-self) | **RETAINED** | Universal Casimir piece (`-8 g_3²` etc.) is scheme-independent at 1L; structural per S1 + Casimir algebra. Same retention status as 1L β_λ in Z-S4b-Audit. |
| **I2** 2L+ SM Yukawa β-function scalar weights | **IMPORTED** | FJJ92, LWX03, Machacek-Vaughn dim-reg MSbar fingerprint; same import class as Z-S4b-Audit I3 (3L β_λ) and Probe X-L1-MSbar (β_2/β_3 QCD). |
| **I3** y_t(M_Pl) Ward BC `= g_lattice/√6` | **RETAINED** | YT_WARD_IDENTITY_DERIVATION_THEOREM (species-privileged); Block 6 algebra is exact at 1PI level. |
| **I4** y_b(M_Pl), y_c(M_Pl) species-DIFFERENTIATED BC | **NOT RETAINED** | Species-uniform extension is FALSIFIED (33× overshoot per YT_BOTTOM). Koide circulant `ρ_down ≈ 1.536`, `ρ_up ≈ 1.754` candidate; but Koide equipartition + Brannen `√m` identification are admitted non-retained primitives per YT_BOTTOM §5.2. |
| **I5** Chiral SSB constituent shift `Σ ~ Λ_QCD³` | **IMPORTED** scope | HADRON_LANE1_CHIRAL_CONDENSATE_BANKS_CASHER_SCOPING audit verdict: `Σ = π ρ_Dirac(0)` requires L≥12-16 dynamical lattice run NOT on retained surface, OR new structural identity. ChPT-model ~330 MeV is phenomenological. |

**Audit semantics.** Two ingredients are RETAINED (I1, I3); three are
ADMITTED (I2, I4, I5). The probe's claimed "retained Yukawa flow gives
m_b, m_c" rests entirely on I4 (species-differentiated y_q BC), which
is NOT retained. I5 (chiral SSB) is a separate IMPORTED mechanism that
even if admitted bridges <1% of the I4 gap. The probe FAILS at I4.

## 3. What this closes vs. does not close

### Closed (negative observations)

- **Dynamical chiral SSB + retained Yukawa flow as a closure mechanism
  for m_b, m_c at the 5% gate.** The species-uniform Ward BC + 1L SM
  RGE gives `m_b(m_b) ≈ 190 GeV` (45× overshoot); chiral SSB ~330 MeV
  bridges 0.18% of the 186 GeV gap. No combination of the retained
  ingredients + chiral SSB closes m_b or m_c at 5%.
- **Heavy-quark masses are NOT derivable from the union of retained
  physical `Cl(3)` local algebra + `Z^3` spatial substrate content +
  chiral SSB structural argument + retained 1L
  Yukawa flow.** The species-differentiation primitive on `y_q(M_Pl)`
  (I4) is the load-bearing missing piece, and chiral SSB does not
  substitute for it.

### Sharpened (residual observations, not promoted)

- **Chiral SSB is structurally a LIGHT-quark mechanism.** Adding
  `Σ_constituent ≈ 330 MeV` to `m_q^current` reproduces u, d
  constituent-mass benchmarks within 2%, and m_s within 13% (the s
  quark sits in a transition regime). But the light-quark
  `m_q^current` itself is NOT retained from physical `Cl(3)` local
  algebra + `Z^3` spatial substrate content; the
  species-differentiation problem appears at light AND heavy scales.
  Recorded as a structural observation, not promoted.

- **Species-uniform Ward BC + 1L (this work) is more severe than the
  YT_BOTTOM 2L result.** 1L gives `m_b(m_b) ≈ 190 GeV` vs 2L `≈ 140 GeV`,
  due to coupled `(y_t, y_b, g_3)` 1L fixed-point back-reaction. The
  conclusion (FALSIFIED) is the same; the 1L number is recorded for
  completeness.

### Not closed (preserved obstructions)

- **Species-privileged retained `m_t = 169.5 GeV` chain
  (YT_ZERO_IMPORT_CHAIN_NOTE) is unaffected.** This probe addresses a
  DIFFERENT chain (species-uniform with chiral SSB extension) and
  does not modify the top-only retained result.
- **Retained CKM-dual `m_s/m_b` ratio (+0.2% threshold-local) is
  unaffected.** This probe addresses absolute scales; the ratio
  remains retained-bounded.
- **Koide circulant Fourier-basis candidate mechanism** for
  species-differentiation (per YT_BOTTOM §5.2) remains the open
  positive-mechanism candidate, conditional on Koide equipartition +
  Brannen `√m` admissions.
- **W₁.exact engineering frontier**, **L3a/L3b admissions**, and
  **C-iso a_τ = a_s admission** remain unaffected.

### What this changes (positively)

Closing the dynamical-SSB route narrows the strategic option space:

> "The EW Wilson chain hits only τ. Maybe quarks couple to a parallel
> QCD chain (Z); maybe heavy quarks need a fundamentally different
> mechanism — Yukawa-dominated current mass plus chiral SSB
> contribution." — V-Quark-Dynamical design rationale

After this probe, the parallel-chain hypothesis (X, Y, Z) AND the
Yukawa+chiral-SSB hypothesis (V) are both **closed** at the 5% gate
for `m_b` and `m_c` under any single retained-derivable mechanism.

The strategic implication is sharpened:

1. **Heavy-quark masses are NOT closable by chain mechanisms (X, Y, Z)
   OR by a Yukawa-dominated mass with chiral SSB correction (V).**
2. **A species-DIFFERENTIATION primitive on `y_q(M_Pl)` is required.**
   This primitive must produce `y_b(M_Pl)` suppressed by ~1/35 relative
   to `y_t(M_Pl)` (and `y_c(M_Pl)` suppressed by ~1/130). The Koide
   circulant Fourier-basis spectrum with sector-dependent
   `ρ = 2|b|/a` is the leading candidate (per YT_BOTTOM §5.2), but
   `Koide equipartition` and `Brannen √m identification` are admitted
   non-retained primitives.
3. **Chiral SSB is NOT the species-differentiation primitive.** It is
   structurally a constituent-mass mechanism for LIGHT quarks
   (`Σ ~ 330 MeV` dominates over current few-MeV scales) and adds
   negligible-to-modest fractional corrections to heavy-quark masses
   (`<8%` for m_b, `<26%` for m_c, `<0.2%` for m_t).

## 4. Setup

### Retained inputs (no derivation, no admission)

All values from existing retained-bounded notes; no new content:

| Symbol | Value | Origin |
|---|---|---|
| `⟨P⟩` | 0.5934 | SU(3) plaquette MC at β=6 (retained) |
| `α_bare` | `1/(4π)` ≈ 0.07957747 | Cl(3) canonical normalization |
| `u_0` | `⟨P⟩^{1/4}` ≈ 0.87768 | Lepage-Mackenzie tadpole (retained) |
| `α_LM` | `α_bare/u_0` ≈ 0.090668 | Geometric-mean coupling (retained) |
| `α_s(v)` | `α_bare/u_0²` ≈ 0.10330 | Vertex-power chain (retained, bounded analytic insertion gap) |
| `g_lattice` | `√(4π α_LM)` ≈ 1.06741 | Lattice gauge coupling at the cutoff |
| `Ward BC y_t(M_Pl)` | `g_lattice/√6` ≈ 0.43577 | YT_WARD_IDENTITY_DERIVATION_THEOREM (RETAINED) |
| `M_Pl` | 1.221 × 10¹⁹ GeV | Framework UV cutoff (axiom) |
| `v_EW` | 246.22 GeV | Hierarchy theorem `v = M_Pl × (7/8)^{1/4} × α_LM^{16}` |
| `Λ_QCD` (5-flavor) | 210 MeV | bounded retained per `CONFINEMENT_STRING_TENSION_NOTE` |
| `C_F, C_A, T_F` | 4/3, 3, 1/2 | SU(3) Casimirs (retained per S1) |

### Imported inputs (admitted, with controlled provenance)

| Symbol | Value | Origin |
|---|---|---|
| 2L+ SM Yukawa β-functions | scalar weights | FJJ92 / Machacek-Vaughn dim-reg MSbar (Z-S4b-Audit import class) |
| `Σ_constituent` | ≈ 330 MeV | ChPT phenomenology; Banks-Casher requires L≥12-16 lattice run NOT on retained surface |
| Species-uniform interpretation of Block 6 algebra | structural extension | algebraic (1PI Block 6 species-uniform Clebsch-Gordan extends to ALL Q_L species), but PHYSICAL species identification is what's tested |

### PDG comparators (post-derivation only)

PDG fermion masses appear only as comparators after numerical
predictions are computed:

| Fermion | PDG Value (GeV) | Scheme |
|---|---|---|
| m_u | 2.16 × 10⁻³ | MS̄ @ 2 GeV |
| m_d | 4.67 × 10⁻³ | MS̄ @ 2 GeV |
| m_s | 0.0934 | MS̄ @ 2 GeV |
| m_c | 1.27 | MS̄ @ m_c |
| m_b | 4.18 | MS̄ @ m_b |
| m_t | 172.69 | pole |
| m_τ | 1.77686 | pole |

Constituent comparators (light-quark phenomenology):
- m_u^constituent ~ 336 MeV
- m_d^constituent ~ 340 MeV
- m_s^constituent ~ 486 MeV

## 5. Derivation chain

### Step 1: Species-uniform Ward BC + 1L SM Yukawa RGE (forward M_Pl → v_EW)

**RGE system** (1L SM Yukawa, QCD-dominant truncation; EW gauge
contributions are sub-dominant for QCD-active heavy-quark Yukawa flow):

```
d y_t / dt = y_t / (16π²) × [3 y_t² + 3 y_b² + (3/2)(y_t² − y_b²) − 8 g_3²]
d y_b / dt = y_b / (16π²) × [3 y_t² + 3 y_b² + (3/2)(y_b² − y_t²) − 8 g_3²]
d g_3 / dt = −7 g_3³ / (16π²)
```

**Boundary conditions:**
- UV at `t_M = ln(M_Pl)`: `y_t(M_Pl) = y_b(M_Pl) = WARD_BC = 0.4358`
  (species-uniform Ward extension)
- IR at `t_v = ln(v_EW)`: `g_3(v) = √(4π × α_s(v)) = √(4π × 0.1033) ≈ 1.139`
  → backward-run g_3 to M_Pl gives `g_3(M_Pl) ≈ 0.489`.

**Forward integration** (`t_M = 43.95 → t_v = 5.51`, 20000 steps):

```
y_t(v) ≈ 0.755
y_b(v) ≈ 0.755          [coupled 1L fixed-point reached]
g_3(v) ≈ 1.139
```

**Predictions:**
```
m_t = y_t(v) × v_EW / √2 ≈ 0.755 × 246.22 / √2 ≈ 131.4 GeV    (PDG 172.69)
m_b(v) = y_b(v) × v_EW / √2 ≈ 131.4 GeV
m_b(m_b) = m_b(v) / 0.69 ≈ 190.5 GeV                         (PDG 4.18)
```

**Errors:** m_t undershoots by 24%; m_b(m_b) overshoots by **45.6×**.
Both predictions FAIL the 5% gate. The species-uniform interpretation
of the Ward identity is FALSIFIED for both heavy quarks at 1L (and
also at 2L per YT_BOTTOM `≈ 140 GeV`).

### Step 2: Chiral SSB additive correction

Apply `m_q^total = m_q^current + Σ_constituent`:

```
m_b^total = 190.5 GeV + 0.330 GeV = 190.8 GeV    (PDG 4.18)
gap to PDG: 186.3 GeV
chiral SSB bridges 0.330 / 186.3 = 0.177% of gap
```

Verdict for Step 2: chiral SSB cannot rescue the species-uniform
Yukawa overshoot. The structural `Σ ~ Λ_QCD` scale is three orders of
magnitude smaller than the gap.

### Step 3: Light-quark structural decomposition cross-check

For the LIGHT quarks where chiral SSB IS dominant:

| Quark | m_q^current (MeV) | + Σ_constituent (MeV) | constituent target (MeV) | err |
|---|---|---|---|---|
| u | 2.2 | 332 | 336 | −1.1% |
| d | 4.7 | 335 | 340 | −1.6% |
| s | 93.4 | 423 | 486 | −12.9% |

Chiral SSB additive recovers the constituent benchmarks for u, d at
~2%; s at ~13% (s quark is in a transition regime where chiral SSB
and current mass are comparable).

**However**: the LIGHT-quark `m_q^current` (e.g. m_u = 2.16 MeV) is
itself NOT retained from physical `Cl(3)` local algebra + `Z^3`
spatial substrate content. The same species-differentiation
primitive is needed for light quarks too. The light-quark check is a
structural plausibility argument, not a closure.

### Step 4: Cross-mechanism closure gate

For both `m_b` and `m_c`, no V-mechanism combination closes at 5%:

| Closure attempt | m_b pred (GeV) | err vs PDG | within 5%? |
|---|---|---|---|
| Species-uniform Ward + 1L RGE (no chiral) | 190.6 | 4460% | NO |
| Species-uniform Ward + 1L RGE + chiral SSB | 190.9 | 4468% | NO |
| Chiral SSB alone (m_b = Σ) | 0.33 | −92% | NO |

| Closure attempt | m_c pred (GeV) | err vs PDG | within 5%? |
|---|---|---|---|
| Species-uniform Ward + 1L RGE (no chiral) | 190.6 | 14908% | NO |
| Chiral SSB alone (m_c = Σ) | 0.33 | −74% | NO |

**Verdict:** the V mechanism FAILS at the 5% closure gate for both
m_b and m_c under all retained-or-IMPORTED ingredient combinations.

### Step 5: Retained ratio cross-check (DOWN_TYPE_MASS_RATIO_CKM_DUAL)

`m_s/m_b = (α_s(v)/√6)^{6/5} ≈ 0.02239` vs threshold-local PDG
`m_s(2 GeV)/m_b(m_b) = 0.02234` (+0.20%). This RATIO is retained-
bounded, but the absolute m_b scale is NOT closed (per
DOWN_TYPE_MASS_RATIO_CKM_DUAL §6 explicit disclaimer).

## 6. Constraints respected

- **No new axioms.** All inputs from physical `Cl(3)` local algebra +
  `Z^3` spatial substrate content (S1+Casimir+
  plaquette-self-consistency) + retained-bounded scales (Λ_QCD, v_EW,
  M_Pl, α_LM) + IMPORTED 2L+ β + IMPORTED chiral SSB scope.
- **No PDG masses used as derivation input.** PDG values appear only
  as comparators after `m_q^pred` is computed.
- **No fitting.** Chiral SSB is fixed at `Σ ≈ 330 MeV` from ChPT
  phenomenology (IMPORTED, declared).
- **No promotion.** The retained m_t = 169.5 GeV chain is not modified.
  The retained CKM-dual ratio is not modified. No new theorem-grade
  claim is made; the verdict is no-go / bounded negative.
- **Hostile-review tier classification applied** per Z-S4b-Audit
  pattern; all five load-bearing ingredients tiered.
- **Source-only PR** per `feedback_review_loop_source_only_policy`:
  1 source-note + 1 paired runner + 1 cached output. No support docs,
  no audit-ledger edits, no synthesis notes.

## 7. Cross-references

- Probe X-L1-Threshold (PR #933):
  EW Wilson chain heavy-quark absolute masses foreclosed.
- Probe Y-L1-Ratios (PR #946):
  EW Wilson chain heavy-quark mass-ratio integer-difference foreclosed.
- Probe Z-Quark-QCD-Chain (PR #958, this branch):
  parallel QCD-anchored chain heavy-quark masses foreclosed.
- Probe Y-S4b-RGE (PR #948) downgraded to bounded by Probe Z-S4b-Audit
  (PR #956): same hostile-review pattern applied here.
- [`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md):
  species-uniform Ward BC for y_b → m_b ≈ 140 GeV at 2L; the same
  forecast at 1L (this probe) gives ≈ 190 GeV.
- [`YT_ZERO_IMPORT_CHAIN_NOTE.md`](YT_ZERO_IMPORT_CHAIN_NOTE.md):
  retained species-PRIVILEGED top-only chain; m_t = 169.5 GeV
  (-1.84%); UNAFFECTED by this probe.
- [`YT_WARD_IDENTITY_DERIVATION_THEOREM.md`](YT_WARD_IDENTITY_DERIVATION_THEOREM.md):
  source of the Ward BC `y_t(M_Pl) = g_lattice/√6`.
- [`HADRON_LANE1_CHIRAL_CONDENSATE_BANKS_CASHER_SCOPING_SUPPORT_NOTE_2026-04-27.md`](HADRON_LANE1_CHIRAL_CONDENSATE_BANKS_CASHER_SCOPING_SUPPORT_NOTE_2026-04-27.md):
  chiral condensate Σ NOT retained on current surface; same scope
  obstruction inherited here.
- [`DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`](DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md):
  retained `m_s/m_b` ratio (bounded); §6 disclaims absolute m_b closure.

## 8. Honest non-claims

This probe does NOT claim:
- A framework-native derivation of `y_b(M_Pl)` or `y_c(M_Pl)`. The
  species-uniform extension is FALSIFIED; the species-differentiated
  candidate (Koide circulant) is NOT retained.
- A framework-native derivation of `Σ_constituent` or `<q̄q>`. The
  Banks-Casher route is foreclosed at retained-surface scope per
  HADRON_LANE1_CHIRAL_CONDENSATE_BANKS_CASHER_SCOPING audit.
- That the species-uniform Ward + 2L result `~140 GeV` of YT_BOTTOM
  was wrong; this probe REPRODUCES the same negative direction at 1L
  with `~190 GeV`.
- That the retained species-PRIVILEGED top-only `m_t = 169.5 GeV`
  chain is wrong; that chain is unaffected.
- Any change to the existing retained-bounded scope of α_s(v), α_LM,
  Λ_QCD, v_EW, or any upstream authority.
- Any promotion of the chiral-SSB structural argument as a derivation
  primitive.

## 9. Audit-lane authority

This is a **source-note proposal**. Pipeline-derived status and
downstream propagation are set only by the independent audit lane,
not by this note. The verdict written here is **negative/bounded**:
the dynamical chiral SSB + retained Yukawa flow mechanism does NOT
close `m_b`, `m_c` to the 5% precision gate. The chiral SSB
contribution is structurally a light-quark constituent-mass shift
(~330 MeV) that bridges <1% of the species-uniform Yukawa-BC
overshoot for heavy quarks.

The probe contributes ONE closure to the strategic option space:
combined with X (#933), Y (#946), Z (#958), the structural option
for "heavy-quark masses from {single coupling chain, Yukawa+SSB}"
is now exhausted at the 5% gate. The species-DIFFERENTIATION
primitive on `y_q(M_Pl)` (candidates: Koide circulant Fourier-basis
spectrum with `ρ_down ≈ 1.536`, `ρ_up ≈ 1.754`; Koide/Brannen admissions)
remains the open gap.

## 10. Validation

PASS = 21, FAIL = 0, ADMITTED = 12 across all probe checks (see
runner output cache). The runner verifies:
1. Retained-anchor sanity (α_bare, u_0, α_LM, α_s(v), g_lattice,
   Ward BC, Casimirs).
2. Hostile-review tier classification (5 ingredients: 2 RETAINED, 3
   ADMITTED).
3. Species-uniform Ward + 1L SM RGE forecast (m_t undershoot, m_b
   overshoot ≥20×).
4. Species-PRIVILEGED top-only retained reference (m_t ≈ 169 GeV
   within 5%).
5. Chiral SSB structural decomposition (light-quark recovery within
   15%; heavy-quark Σ-fraction; <1% gap-bridge for m_b).
6. Retained CKM-dual ratio (m_s/m_b within 5% threshold-local).
7. Cross-mechanism closure gate (NO V-mechanism attempt closes m_b
   or m_c at 5%).
8. Structural verdict (combined X+Y+Z+V option-space exhaustion).
9. Constraints respected (no axioms, no PDG inputs, hostile-review
   pattern, source-only PR).
