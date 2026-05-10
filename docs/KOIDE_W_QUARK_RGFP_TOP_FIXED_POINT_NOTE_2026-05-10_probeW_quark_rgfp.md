# Probe W-Quark-RGFP — Top-Quark Mass via QFP Attractor (Dynamical Route): Bounded-Tier Source Note (NEGATIVE)

**Date:** 2026-05-10
**Claim type:** bounded_theorem (negative; dynamical RGE-attractor route foreclosed for top-quark mass)
**Sub-gate:** Lane 1 follow-up to Probe X-L1-Threshold (PR #933),
Probe Y-L1-Ratios (PR #946), and Probe Z-Quark-QCD-Chain
(commit 18d247acb) — the **dynamical** (RGE-attractor) alternative to
the three foreclosed **algebraic-chain** routes for heavy-quark masses.
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent audit
lane.

**Primary runner:** [`scripts/cl3_koide_w_quark_rgfp_2026_05_10_probeW_quark_rgfp.py`](../scripts/cl3_koide_w_quark_rgfp_2026_05_10_probeW_quark_rgfp.py)
**Cached output:** [`logs/runner-cache/cl3_koide_w_quark_rgfp_2026_05_10_probeW_quark_rgfp.txt`](../logs/runner-cache/cl3_koide_w_quark_rgfp_2026_05_10_probeW_quark_rgfp.txt)

## 0. Probe context

Three prior probes have foreclosed single-mechanism routes for
heavy-quark masses on the EW Wilson chain `m_τ = M_Pl × (7/8)^(1/4) × u_0
× α_LM^18`:

- **Probe X-L1-Threshold** (PR #933): heavy-quark **absolute** masses
  via Wilson chain — NEGATIVE.
- **Probe Y-L1-Ratios** (PR #946): heavy-quark mass **ratios** via
  Wilson chain integer differences — NEGATIVE.
- **Probe Z-Quark-QCD-Chain** (commit 18d247acb): parallel QCD-confinement
  chain `m_q = Λ_QCD × C × α_s^(n_q)` — NEGATIVE.

Collective conclusion: the three **single-chain algebraic** routes
(EW absolute, EW ratios, QCD parallel) all foreclose. Each assumed
quarks reach via the *same algebraic mechanism* as `m_τ`.

**This probe asks the structurally distinct question:** what if that
assumption is wrong? `m_τ` is *passive* (Yukawa small, RGE running
negligible). Heavy quarks (especially top) are *RGE-active*: large
Yukawas, dynamical mass via RGE flow. The top Yukawa is the canonical
case. From a wide range of UV BCs `y_t(M_Pl) ∈ [0.5, 5]`, 2-loop
SM RGE in the SM-physical-α_s case drives `y_t(M_Z) → 0.95-0.99` — the
**Pendleton-Ross IR quasi-fixed point (QFP) attractor**. Then
`m_t = y_t(v) × v / √2` gives `m_t ≈ 173 GeV` regardless of UV BC.

This probe tests whether the QFP attractor mechanism — using the
framework's RETAINED 1-loop `β_yt` and RETAINED gauge couplings — closes
`m_t` to ~5% under generic UV BCs at `M_Pl`, *without* invoking the
lattice Ward identity `y_t(M_Pl) = g_lattice/√6 = 0.4358`.

## 1. Theorem (bounded, negative — QFP-attractor route foreclosed for top-quark mass)

**Theorem (W-Quark-RGFP; bounded, negative).** On retained content of
Cl(3)/Z³ plus retained 1-loop SM RGEs (β_yt^(1), β_g_i^(1) — RETAINED via
SU(N_c=3)×SU(2)×U(1) Casimirs; per Z-S4b-Audit row I1 pattern), with
framework gauge couplings `g_3(v) = √(4π·α_bare/u_0²) = 1.139`,
`g_2(v) = 0.646`, `g_1(v) = 0.464` evolved up to `M_Pl` via 1-loop SM
RGE (n_f = 6), and a wide generic UV grid `y_t(M_Pl) ∈ [0.5, 5.0]` with
NO Ward-identity input:

```
The IR QFP-attractor value of y_t under the framework's retained
1-loop β_yt is

   y_t(v)|attractor ≈ 1.26    (corresponding to m_t|attractor ≈ 218 GeV)

NOT the SM-physical attractor value y_t(v) ≈ 0.95 (m_t ≈ 173 GeV).

The structural reason: the framework's α_s(v) = α_bare/u_0² = 0.1033
is ~12.5% LOWER than the SM-physical α_s(M_Z) = 0.1181 (PDG). The QFP
fixed-point value of y_t solves
   9/2 y² = 8 g_3²(v) + 9/4 g_2²(v) + 17/20 g_1²(v),
giving y_t^QFP(v) = 1.60 directly (mt^QFP = 278 GeV, +61% from PDG)
in the bare bracket sense, while the dynamical attractor under 17
decades of running converges to y_t(v) ≈ 1.25 (m_t ≈ 218 GeV, +26%).

Numerical evidence (1-loop, retained content, this runner):

| y_t(M_Pl) | y_t(v)   | m_t [GeV] | Δ from PDG 172.69 |
|-----------|----------|-----------|-------------------|
| 0.4       | 0.9137   | 159.12    | -7.86%            |
| 0.5       | 1.0029   | 174.66    | +1.14%            |
| 0.7       | 1.1065   | 192.69    | +11.58%           |
| 1.0       | 1.1764   | 204.87    | +18.64%           |
| 2.0       | 1.2359   | 215.23    | +24.64%           |
| 5.0       | 1.2543   | 218.43    | +26.49%           |
| 10.0      | 1.2570   | 218.90    | +26.76%           |

The attractor is at y_t(v) ≈ 1.257, m_t ≈ 218.9 GeV. UV BCs in
[1, 10] all converge to the attractor band [+18%, +27%] from PDG.

Therefore the QFP-attractor route for m_t is FORECLOSED at the 5%
mass-precision tier: the dynamical IR fixed point of the framework's
retained RGE does NOT sit at the PDG m_t = 172.7 GeV.

The Ward-BC result m_t = 169.4 GeV (-1.9%, from
YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md) is a TRANSIENT — y_t(M_Pl) =
0.4358 sits on the LOWER side of the QFP basin and the trajectory
rises toward the attractor without finishing in 17 decades, leaving
y_t(v) ≈ 0.95. This is a UV-IR transient property, not an attractor
property. It depends on the specific Ward BC value 0.4358; it does
NOT represent a structural attractor closure.

Specifically:

1. (QFP structure exists.) The 1-loop β_yt has the Pendleton-Ross
   sign structure: at y_t = 1, the QCD term -8 g_3²(v) = -10.39
   dominates the Yukawa self-coupling +9/2 y² = +4.5. A QFP DOES
   exist at the framework's retained gauge couplings.

2. (Focusing exists.) The focusing ratio over UV scan
   y_t(M_Pl) ∈ [0.5, 5] is R ≈ 17.9 (UV factor 10× compresses to
   IR factor 1.25×). Strong focusing — but not enough to compress
   the full UV range to the PDG band.

3. (Attractor mislocation.) The IR attractor sits at y_t(v) ≈ 1.257
   instead of the SM-physical 0.95. Structural reason: framework
   α_s(v) = 0.1033 < SM-physical α_s(M_Z) = 0.1181, weakening the
   -8 g_3² QCD pull-down term in β_yt and raising the QFP location.

4. (Single point coincidence at 5%.) y_t(M_Pl) = 0.5 happens to
   give m_t = 174.66 GeV (+1.14%). This is one accidental UV BC,
   not a structural attractor — and 0.5 is NOT a retained-derivable
   value in the framework.

5. (Ward-BC transient ≠ attractor.) Ward BC y_t(M_Pl) = 0.4358 lies
   below the attractor; the running trajectory rises toward y_t ≈
   1.26 but is captured at y_t(v) ≈ 0.95 because 17 decades is not
   enough time to reach the attractor. The Ward-BC result is a
   trajectory-truncation effect, not an IR fixed-point property.
```

**Proof sketch.** Each numbered claim is verified independently in
the paired runner; their conjunction gives the negative closure. ∎

## 2. What this closes vs. does not close

### Closed (negative observations)

- **QFP-attractor route for `m_t` foreclosed at the 5% precision
  tier on retained content.** The IR attractor of the framework's
  retained 1-loop SM RGE sits at y_t(v) ≈ 1.26, m_t ≈ 218 GeV — far
  from the PDG 172.7 GeV.
- **The Ward-BC result m_t = 169.4 GeV is a transient, not an
  attractor.** It depends on the specific Ward BC value 0.4358 lying
  below the attractor; it does not represent a structural fixed-point
  property of the RGE flow.
- **The brief's hypothesis "wide UV → m_t ≈ 173 GeV via QFP" is FALSE
  on retained content.** The Pendleton-Ross folklore "any UV BC gives
  m_t ≈ 173 GeV" relies on SM-physical α_s ≈ 0.118; the framework's
  retained α_s(v) = 0.1033 places the QFP attractor at the wrong
  value.
- **Together with X/Y/Z, four single-mechanism routes for heavy-quark
  masses are now closed:**
  | Route | Mechanism | Status |
  |---|---|---|
  | X-L1-Threshold | EW Wilson chain (absolute) | NEGATIVE (PR #933) |
  | Y-L1-Ratios | EW Wilson chain (ratios) | NEGATIVE (PR #946) |
  | Z-Quark-QCD-Chain | Parallel QCD chain | NEGATIVE (commit 18d247acb) |
  | **W-Quark-RGFP (this)** | RGE QFP attractor (dynamical) | **NEGATIVE** |

### Sharpened (residual observations, not promoted)

- **y_t(M_Pl) = 0.5 single-point coincidence at +1.14%.** With UV BC
  `y_t(M_Pl) = 0.5`, m_t = 174.66 GeV, a 1.14% match to PDG. But
  `0.5` is NOT a retained-derivable value (it is not the Ward BC
  0.4358, not √(1/4), not 1/2 derived from any retained source). It
  is a numerical coincidence, recorded as not promoted.
- **Ward-BC lower-side trajectory.** The Ward BC sits 0.0642 below
  the QFP attractor (0.5 - 0.4358 = 0.064). It would require
  significantly longer running (more than 17 decades) for the
  trajectory to reach the attractor. The 17-decade truncation is
  what gives the Ward-BC its "good" m_t answer; it is a UV-IR
  artifact, not a fixed point.

### Not closed (preserved obstructions)

- **EW Wilson chain heavy-quark absolute masses** remain foreclosed.
- **EW Wilson chain heavy-quark ratios** remain foreclosed.
- **Parallel QCD chain heavy-quark masses** remain foreclosed.
- **Charged-lepton Koide A1 admission** is unaffected by this probe
  (lepton sector has no Pendleton-Ross structure regardless; see
  KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08
  Barrier RG2).
- **W₁.exact engineering frontier**, **L3a/L3b admissions**, and
  **C-iso a_τ = a_s admission** remain unaffected.

### What this changes (positively)

Closing the dynamical route narrows the strategic option space:

> "The four foreclosed single-mechanism routes (EW absolute, EW
> ratio, QCD chain, RGE attractor) now exhaust the natural surface
> of single-mechanism heavy-quark mass closures. Heavy-quark mass
> derivation requires either:
> (a) a QUALITATIVELY NEW mechanism not on this list (e.g.,
>     non-trivial UV BC derivation from retained content,
>     multi-mechanism interaction between chain + RGE, or new
>     structural primitive),
> (b) a multi-coupling-chain construction with structurally derived
>     UV BCs at lattice scale per quark, OR
> (c) acceptance that heavy-quark masses are framework-bounded
>     (admissions, not theorems)."

## 3. Setup

### Premises (A_min for Probe W-Quark-RGFP closure attempt)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Plaquette | `<P> = 0.5934` from SU(3) lattice MC at `β = 6` | retained: [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md) |
| α_s(v) | `α_s(v) = α_bare/u_0² = 0.1033` derived from plaquette | retained: same source (Coupling Map Theorem) |
| Hierarchy | `v_EW = M_Pl·(7/8)^(1/4)·α_LM^16 = 246.28 GeV` | retained: same source (Hierarchy Theorem) |
| g_bare | `g_bare = 1` from HS rigidity given `N_F = 1/2` | retained: [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md) |
| 1-loop β_yt | `β_yt^(1) = y_t/(16π²)·[9/2 y² - 8 g_3² - 9/4 g_2² - 17/20 g_1²]` | retained: derivable from SU(N_c=3)×SU(2)×U(1) Casimirs at 1-loop counterterm level (Machacek-Vaughn 1983 universal); per Z-S4b-Audit row I1 pattern (sister case for β_λ^(1)). |
| 1-loop β_g_i | `β_g_i^(1) = b_i g_i³` with `b_1=41/10, b_2=-19/6, b_3=-(11-2N_F/3)` | retained: 1-loop universal; `b_3 = -7` at retained `N_F = 6` |
| QFP existence | β_yt has Pendleton-Ross IR fixed point at retained framework α_s | retained: existence is structural (sign analysis of β_yt at framework α_s(v)) |
| Ward BC | `y_t(M_Pl)_Ward = √(4π α_LM)/√6 = 0.4358` | retained but NOT used as input here (the whole point is to test whether QFP attractor closes m_t WITHOUT Ward BC) |

### Forbidden imports (for the load-bearing layer)

- NO PDG `m_t` value used as derivation input (anchor-only at end).
- NO 2-loop or higher β-function coefficients in the load-bearing layer
  (Part 4 uses 2-loop only as cross-check, marked IMPORTED).
- NO fitted matching coefficients.
- NO UV BC derived from a particular Ward identity (the test is
  generic UV grid, not Ward-anchored).
- **NO new axioms** (the probe tests existing retained content under
  a generic UV BC scan).

## 4. The hypothesis at issue

**Hypothesis (W-Quark-RGFP):**
> The dynamical IR Pendleton-Ross quasi-fixed-point attractor of the
> retained 1-loop SM `β_yt`, evaluated with framework gauge couplings,
> closes `m_t` to ~5% mass precision under generic UV BCs at `M_Pl`,
> WITHOUT requiring the lattice Ward identity `y_t(M_Pl) = g_lattice/√6`
> as input.

If true, "deriving m_t" means showing the framework's retained dynamics
have an IR attractor at the PDG m_t — and the previous foreclosed
chain probes (X/Y/Z) were testing the wrong mechanism.

This hypothesis is motivated by:
- The framework HAS retained dynamical content acting on `y_t`
  (Pendleton-Ross IR QFP per
  [`YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)).
- The y_t QFP is an existence proof that the framework has at least one
  matter-sector dynamical fixed point.
- The retained content includes the colored-Yukawa β_yt with the `-8 g_3²`
  pull-down term (the Pendleton-Ross focusing driver).
- The natural extension: ask whether the IR attractor *value* matches
  the PDG m_t — testing whether the dynamical mechanism alone closes m_t.

## 5. The five structural barriers (and the confirmed barrier finding)

The runner verifies five facts that combine into the negative closure:

### 5.1 (RGFP1) QFP structure exists at framework α_s

**Verified (PASS in runner).** At `α_s(v) = 0.1033`, the 1-loop β_yt has

```
beta_yt = yt/(16 pi^2) * [9/2 yt^2 - 8 g_3^2(v) - 9/4 g_2^2(v) - 17/20 g_1^2(v)]
        = yt/(16 pi^2) * [9/2 yt^2 - 10.385 - 1.123 - ...]
```

For yt < y_t^QFP, beta_yt > 0 (yt grows under IR running); for
yt > y_t^QFP, beta_yt < 0 (yt shrinks). A Pendleton-Ross IR quasi-
fixed point DOES exist on retained content.

### 5.2 (RGFP2) Focusing ratio is strong (R ≈ 18)

**Verified (PASS in runner).** Over a wide UV scan
`y_t(M_Pl) ∈ [0.5, 5.0]` (factor 10×), the IR span at `v` is
`y_t(v) ∈ [1.003, 1.254]` (factor 1.25×). Focusing ratio
`R = 17.9`. The QFP is structurally a strong attractor.

### 5.3 (RGFP3) BUT the attractor mislocation: y_t(v)|attractor ≈ 1.257, NOT 0.95

**Verified (FAIL in runner — STRUCTURAL FINDING).** Running from large
UV BCs (y_t(M_Pl) ≥ 1) lands at y_t(v) ≈ 1.25, giving m_t ≈ 218 GeV
(+26% from PDG). The IR attractor of the framework's retained RGE
does not sit at the PDG m_t.

**Structural reason:** The QFP fixed-point condition (β_yt = 0) gives

```
y_t^QFP(v) = sqrt( (8 g_3^2(v) + 9/4 g_2^2(v) + 17/20 g_1^2(v)) / (9/2) )
```

With framework `α_s(v) = 0.1033 < 0.1181 = α_s(M_Z)_phys`, the QCD term
is weaker, the QFP value is HIGHER, and the attractor mislocates.

### 5.4 (RGFP4) Single-point coincidence at y_t(M_Pl) = 0.5 is not retained-derivable

**Verified (FAIL in runner — coincidence).** At y_t(M_Pl) = 0.5,
m_t = 174.66 GeV (+1.14%, within 5%). But `y_t(M_Pl) = 0.5` is NOT
a framework-derivable value:

- Not the Ward BC (which is 0.4358).
- Not √(1/4) from any retained Casimir.
- Not 1/2 derived from a retained two-form.
- Not √2/(2√α_LM) or any α_LM expression.

It is a numerical coincidence inside the QFP basin. The probe records
it as a coincidence, not a closure.

### 5.5 (RGFP5) Ward-BC m_t = 169.4 GeV closure is a transient, not an attractor

**Verified (FAIL in runner — sharpening).** The Ward BC y_t(M_Pl) =
0.4358 lies BELOW the QFP attractor at y_t(v) ≈ 1.26. Under 17 decades
of running:

```
y_t(M_Pl) = 0.4358  →  y_t(v) = 0.949  (m_t = 165 GeV, -4%)
```

The trajectory is RISING toward the QFP but is captured at
y_t(v) ≈ 0.95 because 17 decades is not enough running time to reach
the attractor at 1.26. This is a UV-IR transient effect — a
trajectory-truncation property — not a fixed-point closure.

The "Ward-BC m_t = 169.4 GeV" result therefore depends on:
(a) The specific Ward BC value 0.4358 lying below the attractor.
(b) The specific 17-decade running window between M_Pl and v.

Neither (a) nor (b) is a structural attractor property. The Ward-BC
result is a TRANSIENT, not an attractor — and depends on the input
value, not the dynamical fixed-point structure.

## 6. Hostile-review ingredient tier audit

Per Z-S4b-Audit (PR #956) pattern, each ingredient classified
RETAINED / IMPORTED / POSTULATED:

| # | Ingredient | Tier | Why |
|---|---|---|---|
| W1 | `g_3(v) = √(4π α_bare/u_0²)` | RETAINED | Coupling Map Theorem on retained `<P>` |
| W2 | `v_EW = M_Pl · (7/8)^(1/4) · α_LM^16` | RETAINED | Hierarchy Theorem |
| W3 | `β_yt^(1) = yt·[9/2 y² - 8 g_3² - 9/4 g_2² - 17/20 g_1²]/(16π²)` | RETAINED | Universal at 1-loop counterterm level (Machacek-Vaughn 1983); each coefficient derives from retained Casimirs (C_F=4/3 from SU(N_c=3); SU(2) and U(1)_Y group factors). Per Z-S4b-Audit row I1 pattern (sister case for β_λ^(1)). |
| W4 | `β_g3^(1) = -(11 - 2N_F/3) g_3³` | RETAINED | b_3 = -7 derived from group-theoretic 1-loop counterterm at retained N_F = 6. |
| W5 | `β_g1^(1), β_g2^(1)` | RETAINED | b_1 = 41/10, b_2 = -19/6 universal at 1-loop. |
| W6 | `y_t(M_Pl)` UV BC | POSTULATED (test grid) | This probe scans a wide grid `[0.5, 5.0]`; the Ward BC is referenced but explicitly NOT used as input. |
| W7 | `β_yt^(2)` (2-loop) | IMPORTED | Per Z-S4b-Audit row I2 pattern: 2-loop scalar weights are MSbar dim-reg imports. Used only for cross-check (Part 4); load-bearing layer is 1-loop. |
| W8 | `β_g3^(2)` (2-loop) | IMPORTED | Per Z-S4b-Audit row I5: gauge 2-loop is dim-reg-imported. Used only for cross-check. |
| W9 | `g_1(v), g_2(v)` from M_Z 1-loop matching | IMPORTED (subdominant) | EW couplings at v derived via 1-loop SM running from M_Z standard values. Subdominant in β_yt (coefficients 17/20 and 9/4 vs. 8 for g_3); contributes <5% to m_t per QFP_INSENSITIVITY Part 3. |
| W10 | Threshold matching at m_t/m_b/m_c | IMPORTED (cross-check only) | Affects only v→M_Z transfer, not v-scale m_t prediction. |

**Tier mapping (per Z-S4b-Audit policy):**
- 0 imports in load-bearing layer → POSITIVE
- 1-2 imports → BOUNDED with named imports
- ≥3 imports → ARITHMETIC RATIO not derivation

**Load-bearing layer (this probe):** 1-loop forward QFP attractor with
RETAINED gauge inputs uses NO load-bearing imports. The 2-loop
comparison (W7, W8) and EW-coupling matching (W9) and threshold
matching (W10) are cross-check / subdominant only.

**The probe's negative closure is therefore on RETAINED CONTENT.** The
QFP attractor mislocation is a real structural finding, not an
import-contamination artifact.

## 7. Why the framework's existing dynamical content is NOT enough

The framework HAS retained dynamical content acting on `y_t`:

- 1-loop β_yt with the Pendleton-Ross `-8 g_3²` driver (RETAINED).
- IR QFP existence at framework α_s (verified PASS in this runner).
- Strong focusing ratio R ≈ 18 (verified PASS).

But the IR attractor *value* is wrong: y_t(v)|attractor ≈ 1.257
(m_t ≈ 218 GeV) vs the PDG `m_t = 172.69 GeV`. Structural reason:
framework α_s(v) = 0.1033 is 12.5% lower than SM-physical α_s(M_Z) =
0.1181.

To extend retained content to a CORRECT QFP attractor at PDG m_t
would require either:
- A new RETAINED primitive supplying a different α_s(v) that places the
  QFP at y_t(v) ≈ 0.95 (but α_s(v) is determined by the retained
  Coupling Map Theorem on the plaquette — fully fixed).
- A new RETAINED β_yt structural correction (but the 1-loop coefficients
  are universal at the counterterm level — not adjustable).
- C_3-breaking dynamics (forbidden — all retained dynamics is C_3-symmetric
  per Coleman/Wilson).
- A 2-loop+ correction whose load-bearing weight is large enough to
  shift the attractor by 25% (but per Z-S4b-Audit pattern, 2-loop+ is
  IMPORTED, not retained — and even with 2-loop the attractor shifts
  to y_t(v) ≈ 1.29, m_t ≈ 224 GeV — making the gap WORSE, not better).

None of these extensions is supplied by retained content.

## 8. Comparison to prior work

| Prior closure attempt | Status | Comment |
|---|---|---|
| Probe X-L1-Threshold | bounded obstruction (NEGATIVE) | EW Wilson chain absolute masses miss heavy quarks (21–57% errors). |
| Probe Y-L1-Ratios | bounded obstruction (NEGATIVE) | EW Wilson chain ratios miss at 5–16% with simple-rational exponents. |
| Probe Z-Quark-QCD-Chain | bounded obstruction (NEGATIVE) | Parallel QCD chain `m_q = Λ_QCD·C·α_s^n_q` miss heavy-quark triplet at 5%. |
| **Probe W-Quark-RGFP — THIS NOTE** | **bounded obstruction (NEGATIVE)** | **QFP attractor sits at +26% from PDG; Ward-BC closure is transient, not attractor.** |
| YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md | bounded support (Ward-anchored) | The Ward-BC closure m_t = 169.4 GeV is a UV-IR transient that depends on the specific Ward BC value, NOT a structural attractor closure. This probe sharpens that understanding. |

This note **complements** prior probes by establishing that the
DYNAMICAL alternative to the foreclosed algebraic chain routes also
fails on retained content. Together with X/Y/Z, the four single-
mechanism routes for heavy-quark masses are now exhausted.

## 9. What this closes

- **Probe W negative closure (bounded obstruction).** Five structural
  facts (QFP exists, focusing exists, attractor mislocation, single-point
  coincidence non-derivable, Ward-BC transient) verified independently.
- **Sharpens the four-route exhaustion**: prior 3 probes (X/Y/Z) tested
  algebraic-chain mechanisms; this probe tested the natural dynamical
  alternative. All four close negatively on retained content.
- **Verified RG-flow numerical experiments**: the SM 1-loop RGE on the
  framework's retained gauge couplings produces an IR attractor at
  y_t(v) ≈ 1.26, NOT at the SM-physical 0.95. This is a falsifiable
  numerical claim.
- **Structural reason for the no-go**: framework α_s(v) = 0.1033 < SM
  physical α_s(M_Z) = 0.1181, weakening the -8 g_3² pull-down term and
  raising the QFP value.
- **Sharpens the Ward-BC closure interpretation**: the Ward-BC m_t =
  169.4 GeV is a UV-IR transient, not a structural attractor. It
  depends on the specific Ward BC value 0.4358 lying below the
  attractor, and on the 17-decade running window. This is a
  trajectory property, not a fixed-point property.
- **Audit-defensibility**: all five claims verified by paired runner
  with explicit numerical evidence.

## 10. What this does NOT close

- A1 admission count is unchanged. A1 remains a load-bearing
  non-axiom step on the Brannen circulant lane.
- Charged-lepton Koide closure remains a bounded observational-pin
  package (status from
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  unchanged).
- The framework's retained dynamical content (plaquette, EW staircase,
  y_t QFP existence) is unaffected.
- AC_φλ residual (substep 4) is unaffected.
- L3a/L3b admissions and C-iso a_τ = a_s admission remain unaffected.
- The Ward-BC closure m_t = 169.4 GeV (-1.9%) per
  YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md remains as a TRANSIENT-tier
  result. It is sharpened (shown to be a trajectory property, not an
  attractor property) but its bounded-tier status is not affected.

## 11. Empirical falsifiability

| Claim | Falsifier |
|---|---|
| RGFP1 (QFP structure exists) | Show β_yt has no zero crossing at framework α_s — refutes RGFP1. |
| RGFP2 (focusing R > 5) | Compute R < 5 over a wider physically-relevant UV grid — refutes RGFP2. |
| RGFP3 (attractor mislocation) | Identify a retained-derivable correction to β_yt or α_s(v) that places the QFP at y_t(v) ≈ 0.95 — refutes RGFP3. |
| RGFP4 (single-point coincidence) | Identify a retained derivation of `y_t(M_Pl) = 0.5` from A1+A2+retained content — promotes the single-point coincidence to a closure. |
| RGFP5 (Ward-BC transient ≠ attractor) | Show the Ward BC y_t(M_Pl) = 0.4358 sits AT the QFP attractor (not below it), making the m_t = 169.4 GeV result an attractor property — refutes RGFP5. |
| Numerical evidence | Falsified if alpha_s(v) = α_bare/u_0² no longer evaluates to 0.1033, or if β_yt^(1) coefficients change. |

## 12. Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative Probe W boundary: the
QFP-attractor route for `m_t` is blocked because the IR attractor value
of the framework's retained 1-loop SM RGE sits at +26% from PDG, not
at PDG.

No new admissions are proposed. No retained-tier promotions implied.
The independent audit lane may retag, narrow, or reject this proposal.

## 13. Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "single-mechanism heavy-quark" methodological gap is closed: prior 3 probes (X/Y/Z) tested algebraic chains; this probe tests the natural dynamical alternative. All four close negatively. |
| V2 | New derivation? | The QFP-attractor mislocation finding is new structural content with explicit numerical RG-flow integration of the framework's retained 1-loop RGE. The Ward-BC-as-transient interpretation sharpens prior YT_QFP_INSENSITIVITY work. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) RGFP1 β_yt sign analysis, (ii) RGFP2 numerical focusing measurement, (iii) RGFP3 attractor location vs PDG, (iv) RGFP4 single-point coincidence non-derivability, (v) RGFP5 Ward-BC trajectory truncation analysis. |
| V4 | Marginal content non-trivial? | Yes — the explicit numerical demonstration that the QFP attractor sits at y_t(v) ≈ 1.26 (not the SM-folklore 0.95) is non-obvious and definitively refutes the dynamical-route hypothesis under retained α_s. |
| V5 | One-step variant? | No — the dynamical-route argument (RGE attractor) is structurally distinct from the algebraic-chain arguments in X/Y/Z. The five-fact structure (QFP exists, focusing exists, attractor mislocates, single-point coincidence, Ward-BC transient) is not a relabel of any prior obstruction. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## 14. Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule is
to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of prior heavy-quark probes (X/Y/Z were algebraic
  chains; this is the dynamical RGE attractor — structurally
  distinct).
- Tests a NEW STRUCTURAL HYPOTHESIS (the dynamical-attractor
  alternative) explicitly motivated by the brief and not addressed in
  prior probes.
- Provides explicit numerical RG-flow integration with multiple UV BCs
  — these were not present in prior probes for heavy-quark masses.
- Sharpens the existing YT_QFP_INSENSITIVITY note's interpretation
  (Ward-BC closure is a transient, not an attractor — a non-trivial
  structural distinction).

## 15. Cross-references

- Sister probe X-L1-Threshold: PR #933 (heavy-quark Wilson chain absolute masses)
- Sister probe Y-L1-Ratios: PR #946 (heavy-quark Wilson chain ratios)
- Sister probe Z-Quark-QCD-Chain: commit 18d247acb / [`KOIDE_Z_QUARK_QCD_CHAIN_NOTE_2026-05-08_probeZ_quark_qcd_chain.md`](KOIDE_Z_QUARK_QCD_CHAIN_NOTE_2026-05-08_probeZ_quark_qcd_chain.md)
- Hostile-review template (audit pattern): [`KOIDE_Z_S4B_RGE_HOSTILE_AUDIT_NOTE_2026-05-08_probeZ_S4b_audit.md`](KOIDE_Z_S4B_RGE_HOSTILE_AUDIT_NOTE_2026-05-08_probeZ_S4b_audit.md)
- Retained dynamical chain: [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- y_t QFP existence support: [`YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md`](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
- Ward identity boundary theorem: [`YT_BOUNDARY_THEOREM.md`](YT_BOUNDARY_THEOREM.md)
- A1 RG fixed-point (related lepton-sector negative): [`KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md`](KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md)
- MINIMAL_AXIOMS: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## 16. Validation

```bash
python3 scripts/cl3_koide_w_quark_rgfp_2026_05_10_probeW_quark_rgfp.py
```

Expected output: structural verification of (i) QFP structure exists at
framework α_s, (ii) focusing ratio R ≈ 18, (iii) attractor mislocation
at y_t(v) ≈ 1.26 → m_t ≈ 218 GeV (NOT PDG 173 GeV), (iv) single-point
coincidence at y_t(M_Pl) = 0.5 (not retained-derivable), (v) Ward-BC
trajectory analysis (transient, not attractor), (vi) hostile-review
ingredient tier audit (load-bearing layer 0 imports, retained-only),
(vii) negative verdict.

Total: 4 PASS / 7 FAIL. The FAILs encode the negative-tier structural
findings (attractor mislocation, single-point non-derivability, Ward-BC
transient). The PASSes confirm the QFP structure and focusing exist
but converge to the wrong value.

Cached: [`logs/runner-cache/cl3_koide_w_quark_rgfp_2026_05_10_probeW_quark_rgfp.txt`](../logs/runner-cache/cl3_koide_w_quark_rgfp_2026_05_10_probeW_quark_rgfp.txt)

## 17. User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note specifically
  applies the "consistency equality is not derivation" rule. The numerical
  match `y_t(M_Pl) = 0.5 → m_t = 174.66 GeV (+1.14%)` is a coincidence
  inside the QFP basin, not a structural derivation, and the proposed
  hypothesis cannot load-bear m_t closure on this basis.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "the framework's retained dynamics produce m_t at
  the QFP attractor" by showing that (a) the QFP attractor exists
  structurally but (b) it sits at the WRONG value because framework α_s
  differs from SM-physical α_s. The Z-S4b-Audit ingredient tier audit is
  applied (Section 6).
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; A1 admission
  remains at its prior bounded status. No retained-tier promotion
  implied.
- `feedback_physics_loop_corollary_churn.md`: the dynamical-attractor
  argument with explicit numerical RG-flow integration and attractor
  location analysis is substantive new structural content, not a relabel
  of prior algebraic-chain probes.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (retained α_s correction, β_yt structural correction, multi-mechanism
  closures) are characterized in terms of WHAT additional content would
  be needed, not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages a
  multi-fact attack (five independent structural facts: QFP exists,
  focusing exists, attractor mislocates, single-point non-derivable,
  Ward-BC transient) on a single load-bearing dynamical hypothesis, with
  sharp PASS/FAIL deliverables in the runner.
- `feedback_primitives_means_derivations.md`: no new axioms or imports
  are proposed. The probe tests existing retained content under generic
  UV BCs.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named
by the source-note above. It does not promote this note or change the
audited claim scope.

- [koide_z_quark_qcd_chain_note_2026-05-08_probeZ_quark_qcd_chain](KOIDE_Z_QUARK_QCD_CHAIN_NOTE_2026-05-08_probeZ_quark_qcd_chain.md)
- [koide_z_s4b_rge_hostile_audit_note_2026-05-08_probeZ_S4b_audit](KOIDE_Z_S4B_RGE_HOSTILE_AUDIT_NOTE_2026-05-08_probeZ_S4b_audit.md)
- [yt_qfp_insensitivity_support_note](YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md)
- [yt_boundary_theorem](YT_BOUNDARY_THEOREM.md)
- [complete_prediction_chain_2026_04_15](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- [koide_a1_probe_rg_fixed_point_bounded_obstruction_note_2026-05-08_probe5](KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md)
- [g_bare_hilbert_schmidt_rigidity_theorem_note_2026-05-07](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)
- [charged_lepton_mass_hierarchy_review_note_2026-04-17](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
