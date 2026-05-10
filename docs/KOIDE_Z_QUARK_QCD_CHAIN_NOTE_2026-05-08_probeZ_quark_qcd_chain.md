# Probe Z-Quark-QCD-Chain — Heavy-Quark Mass via Λ_QCD-Anchored α_s Chain: Bounded-Tier Source Note (NEGATIVE)

**Date:** 2026-05-10
**Claim type:** bounded_theorem (negative; QCD-anchored chain route foreclosed for heavy quarks)
**Sub-gate:** Lane 1 follow-up to Probe X-L1-Threshold (PR #933)
and Probe Y-L1-Ratios (PR #946) — parallel QCD-confinement chain test
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent audit lane.

**Primary runner:** [`scripts/cl3_koide_z_quark_qcd_chain_2026_05_08_probeZ_quark_qcd_chain.py`](../scripts/cl3_koide_z_quark_qcd_chain_2026_05_08_probeZ_quark_qcd_chain.py)
**Cached output:** [`logs/runner-cache/cl3_koide_z_quark_qcd_chain_2026_05_08_probeZ_quark_qcd_chain.txt`](../logs/runner-cache/cl3_koide_z_quark_qcd_chain_2026_05_08_probeZ_quark_qcd_chain.txt)

## 0. Probe context

Three prior probes have foreclosed routes for heavy-quark masses on the
EW Wilson chain `m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}`:

- **Probe 19**
  ([`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)):
  m_τ derived (POSITIVE; 0.017% PDG match).
- **Probe X-L1-Threshold** (PR #933):
  heavy-quark **absolute** masses via Wilson chain — NEGATIVE
  (residues 0.09–0.48 → 21–57% mass errors).
- **Probe Y-L1-Ratios** (PR #946):
  heavy-quark mass **ratios** via Wilson chain integer differences —
  NEGATIVE (best m_b at Δn = −1/3 → 5.4%; m_c at +1/6 → 6.2%; m_t at
  −11/6 → 16.1%).

Collective conclusion across all three: **the EW Wilson chain hits
ONLY the τ scale.** Heavy-quark masses lie off the EW Wilson chain at
all integer and simple-rational exponents.

**This probe asks the structurally distinct question:** quarks couple
to QCD, not just EW. A *parallel QCD-confinement chain* anchored at
**Λ_QCD** (instead of `M_Pl`) and using **α_s** (instead of `α_LM`)
might reach heavy-quark masses where the EW Wilson chain fails.
Mathematically:

```
m_q = Λ_QCD × C × α_s^{n_q}            [parallel QCD chain]
```

paralleling Probe 19's

```
m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}    [EW Wilson chain]
```

where `Λ_QCD` is the QCD confinement scale (~210 MeV, retained-bounded
per [`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md)),
`C` is a retained-derivable structural prefactor candidate, and `n_q`
is an integer (or simple rational) derivable from QCD-side retained
content.

## 1. Theorem (bounded, negative — QCD-chain route foreclosed for heavy quarks)

**Theorem (Z-Quark-QCD-Chain; bounded, negative).** On retained content
of Cl(3)/Z³ plus retained Wilson-chain inputs `(M_Pl, ⟨P⟩, α_bare, u_0,
α_LM)` plus retained-bounded QCD content
`(Λ_MS̄^(5) = 210 MeV, α_s(M_Z) = 0.1181)`, the heavy-quark mass triplet
`(m_t, m_b, m_c)` is NOT simultaneously derivable as
`m_q = Λ_QCD × C × α_s(M_Z)^{n_q}` with a single structural prefactor
`C ∈ {1, 2, 3, 4, 4/3, 3/4, 7/8, 2/3, π, e^γ, √2, √3, √6, 1/√2, 1/√3,
(7/8)^{1/4}, u_0, α_bare, α_LM, ...}` (retained-derivable candidates)
and integer `n_q` to the 5% mass precision gate, NOR with simple-
rational `n_q` (denominator ≤ 6) to the **1% structurally-significant
mass gate** (where density-of-rationals random density drops to ~8%).

Specifically:

1. **(Single-C-with-integer-n_q test fails for the heavy-quark triplet.)**
   No retained-derivable structural `C` admits all three heavy quarks at
   integer `n_q` to 5% mass precision simultaneously. The best individual
   per-quark hits at `α_s(M_Z) = 0.1181` are:

   | q | best `(C, n_q)` | m_pred (GeV) | mass rel.err |
   |---|---|---|---|
   | t | `C = 4/3 = C_F` (color Casimir), `n_q = −3` | 169.98 | **1.57%** |
   | b | `C = √6`, `n_q = −1` | 4.356 | **4.20%** |
   | c | `C = 1/√2`, `n_q = −1` | 1.257 | **1.00%** |

   Each best-fit `C` is **different** for each quark; no single
   retained-structural `C` works for all three.

2. **(τ-scale near-coincidence is structurally circular.)** With `C = 1`,
   `n_q = −1`, `Λ_QCD = 210 MeV`, `α_s(M_Z) = 0.1181`, one obtains
   `m_τ^pred = Λ_QCD/α_s(M_Z) = 1.7782 GeV` vs PDG `m_τ = 1.77686 GeV`
   at **0.073% precision**. This near-coincidence is *not* an
   independent positive result, because `Λ_QCD = 210 MeV` is itself
   *derived* from `α_s(M_Z) = 0.1181` via 2-loop QCD running per
   [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md):
   ```
   Λ_MS̄^(5) = M_Z · exp(−1/(2·β_0·α_s(M_Z))) · (corrections)
   ```
   so `Λ_QCD/α_s(M_Z)` is a single derived quantity, not the product of
   two independent retained inputs. The near-equality
   `m_τ ≈ Λ_QCD/α_s(M_Z)` therefore tests a *one-parameter* relation
   already encoded in standard QCD infrastructure, not a two-parameter
   structural identity.

3. **(Structural-C single-quark hits fail density-of-rationals control
   at the 1% gate.)** The single-quark near-hits in §1.1 sit at:
   - m_t at 1.57% (above 1% gate — borderline coincidence zone)
   - m_b at 4.20% (well above 1% gate)
   - m_c at 1.00% (at the 1% gate)

   At the 5% mass gate, ~37% of random reals `n` in `[−5, 5]` admit
   *some* `p/q` with `q ≤ 6` matching at the 5% threshold (see §5
   density-of-rationals control). At the 1% gate the random hit rate
   drops to ~8%. None of the three heavy-quark single-quark hits in
   §1.1 are below the 1% gate; the m_t hit at 1.57% with `C = C_F = 4/3`
   is the structurally most plausible (color Casimir is QCD-natural)
   but still falls outside the 1% retained-tier precision.

4. **(Light-quark sector also fails.)** With `C = 1`, `α_s(M_Z) = 0.1181`,
   integer `n_q`:
   - m_s at `n_q = 0` → 124.84% mass error
   - m_u at `n_q = 2` → 35.60% mass error
   - m_d at `n_q = 2` → 37.28% mass error
   No simple structural prefactor closes any light quark at 5% mass
   precision either.

5. **(Probe-Y-recorded ratio coincidence m_b/m_c ≈ α_LM^{−1/2} at 0.9%
   does NOT extend to QCD-chain ratios.)** With `α_s(M_Z) = 0.1181`:
   `Δn(m_b/m_c) = log(m_b/m_c)/log(α_s) = −0.5577`, which is
   **0.058 from −1/2** — not as clean as the EW-chain ratio
   (0.0037 from −1/2 in Probe Y). The half-power coincidence is
   **EW-chain-specific**; it does not transfer to the QCD-chain.

## 2. What this closes vs. does not close

### Closed (negative observations)

- **Single-`C` integer-`n_q` QCD chain: foreclosed for heavy-quark
  triplet at the 5% precision tier.** No retained-structural `C` admits
  `(m_t, m_b, m_c)` simultaneously at integer `n_q` to 5% mass error.
- **Single-`C` simple-rational-`n_q` QCD chain (q ≤ 6): foreclosed for
  heavy-quark triplet at the 1% structurally-significant precision
  tier.** Per-quark hits with three different `C` values exist (m_t at
  1.57% with `C_F`, m_c at 1.00% with `1/√2`, m_b at 4.20% with `√6`),
  and a single `C = √2` admits all three within the 5% gate (m_t −3,
  m_b −5/4, m_c −2/3 → 2.6%–4.4%) — but this 5% q ≤ 6 closure falls
  inside the density-of-rationals random band (37% at q ≤ 6 / 5%) and
  therefore carries no structural information. At the 1% structurally-
  significant gate (random density ~8% at q ≤ 6), no single retained-
  structural `C` admits all three.
- **The m_τ ≈ Λ_QCD/α_s(M_Z) near-coincidence at 0.073% is structurally
  circular** because `Λ_QCD` is itself derived from `α_s(M_Z)` via
  2-loop running. No new structural information.
- **The m_b/m_c ≈ α_LM^{−1/2} ratio coincidence (Probe Y, 0.9%) does
  NOT extend to the QCD chain** (Δn(m_b/m_c) is 0.058 from −1/2 with
  α_s(M_Z), much less clean than 0.0037 with α_LM).

### Sharpened (residual observations, not promoted)

- **m_t at `(C, n_q) = (4/3, −3)` closes to 1.57%** is the most
  structurally suggestive single-quark fit because `C = 4/3 = C_F`
  is the QCD color Casimir for the fundamental representation, a
  natural retained QCD constant. However:
  1. It does not extend to m_b or m_c with the same `C`.
  2. 1.57% is borderline — outside the 1% retained-tier gate but
     inside the density-of-rationals 5% band.
  3. No retained derivation is shown for *why* m_t specifically
     should sit at `n_q = −3` with `C = C_F` while m_b, m_c sit
     elsewhere.

  Recorded as a **post-hoc empirical observation**, not promoted.

- **m_c at `(C, n_q) = (1/√2, −1)` closes to 1.00%** at the 1% gate
  exactly. `1/√2` is not a standard QCD constant (no obvious color
  factor, generation index, or Casimir gives `1/√2` directly).
  Recorded as a possible numerical coincidence, not promoted.

### Not closed (preserved obstructions)

- **EW Wilson chain heavy-quark absolute masses** remain foreclosed per
  Probe X-L1-Threshold.
- **EW Wilson chain heavy-quark ratios** remain foreclosed per Probe
  Y-L1-Ratios.
- **Heavy-quark masses require a qualitatively different mechanism** than
  any of the chains tested so far (EW Wilson, EW ratios, QCD-anchored).
- **BAE condition** `|b|²/a² = 1/2`, **Brannen magic angle** φ = 2/9,
  **W₁.exact engineering frontier**, **L3a/L3b admissions**, and
  **C-iso a_τ = a_s admission** remain unaffected.

### What this changes (positively)

Closing the QCD-chain route narrows the strategic option space:

> "The EW Wilson chain hits only τ. Maybe quarks couple to a parallel
> QCD chain anchored at Λ_QCD with α_s instead of α_LM."
> — Probe Z design rationale

After this probe, the parallel QCD-chain hypothesis is **closed** at
the 5% gate for the heavy-quark triplet under any single retained-
structural prefactor. The structural option for "single chain, single
prefactor, integer/simple-rational exponents" is now exhausted across
both the EW and QCD anchors.

The strategic implication is sharpened:

1. **Heavy-quark masses do not lie on a single coupling-chain at any
   integer or simple-rational exponent** with any retained-derivable
   structural prefactor at the 5% gate.
2. **Generation-dependent structure is required.** If a chain works at
   all, it must use generation-dependent (or quark-specific)
   prefactors `C_q`, not a universal `C`. Such generation-dependent
   structure is itself an open question — the framework does not
   currently have a derivation of `C_t = 4/3`, `C_b = √6`, `C_c = 1/√2`
   from retained content (and these specific values may themselves be
   numerical accidents rather than derivations).
3. **The Wilson chain and the QCD chain are NOT independent** because
   `Λ_QCD = 210 MeV` is derived from `α_s(M_Z) = 0.1181` which is
   itself derived (bounded) from `α_s(v) = α_bare/u_0² = 0.1033` via
   the registered low-energy running bridge. The "parallel" chain is
   not actually independent of the EW chain — both go through the
   same `(α_bare, ⟨P⟩, u_0)` retained content.

## 3. Setup

### Retained QCD-chain inputs (no derivation, no admission)

All values from existing retained-bounded notes; no new content:

| Symbol | Value | Origin |
|---|---|---|
| `⟨P⟩` | 0.5934 | SU(3) plaquette MC at β=6 (retained) |
| `α_bare` | 1/(4π) ≈ 0.07957747 | Cl(3) canonical normalization |
| `u_0` | `⟨P⟩^{1/4}` ≈ 0.87768 | Lepage-Mackenzie tadpole (retained) |
| `α_LM` | `α_bare/u_0` ≈ 0.090668 | Geometric-mean coupling (retained) |
| `α_s(v) ` | `α_bare/u_0²` ≈ 0.1033 | Vertex-power chain (retained, bounded analytic insertion gap) |
| `α_s(M_Z)` | 0.1181 | Low-energy running bridge from `α_s(v)` per [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md) (bounded) |
| `Λ_MS̄^(5)` | 210 MeV | 2-loop QCD running from `α_s(M_Z)` per [`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md) Step 4 (bounded) |
| `Λ_MS̄^(4)` | 290 MeV | 2-loop QCD running with `m_b` threshold (bounded) |
| `Λ_MS̄^(3)` | 332 MeV | 2-loop QCD running with `m_c` threshold (bounded) |
| `Λ^(3)_framework` | 389 MeV | per [`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md) Step 5 Method 1 (bounded) |

The runner uses `Λ_MS̄^(5) = 210 MeV` as the canonical anchor (5-flavor
scheme matches the `α_s(M_Z)` evaluation scheme); robustness to the
choice is verified by comparison with `Λ_MS̄^(4)` (290 MeV) and
`Λ_MS̄^(3)` (332 MeV) and `Λ^(3)_framework` (389 MeV).

### Retained-derivable structural prefactor candidates `C`

Tested over the same set used in Probe X (extending to QCD-natural
factors):

| C | Origin |
|---|---|
| 1 | trivial |
| 4/3 | `C_F = (N_c²−1)/(2 N_c)` for `N_c = 3` (color Casimir, fundamental) |
| 3 | `C_A = N_c` (color Casimir, adjoint) |
| 1/2 | `T_F` (color matrix half) |
| 8/9 | `(N_c²−1)/N_c²` (color factor) |
| 2/3 | Koide Q (retained) |
| 7/8 | APBC eigenvalue ratio |
| `(7/8)^{1/4}` | retained Wilson prefix factor |
| `u_0`, `1/u_0` | retained tadpole/inverse |
| `α_bare`, `α_LM` | retained couplings |
| 2, 3, 4 | small integers |
| 1/2, 1/3, 1/4 | small reciprocals |
| `√2, √3, √6, 1/√2, 1/√3` | Clebsch-Gordan / generation roots |
| `π, π/2, 2π, 4π, 1/π` | trig-based |
| `e^γ` | Euler-Mascheroni |

### PDG comparators (post-derivation only)

PDG fermion masses appear only as comparators after `n_q` is computed:

| Fermion | Value (GeV) | Scheme |
|---|---|---|
| m_e | 5.10999 × 10⁻⁴ | pole |
| m_μ | 0.10566 | pole |
| m_τ | 1.77686 | pole |
| m_u | 2.16 × 10⁻³ | MS̄ @ 2 GeV |
| m_d | 4.67 × 10⁻³ | MS̄ @ 2 GeV |
| m_s | 0.0934 | MS̄ @ 2 GeV |
| m_c | 1.27 | MS̄ @ m_c |
| m_b | 4.18 | MS̄ @ m_b |
| m_t | 172.69 | pole |

## 4. Derivation chain

### Step 1: Compute required `n_q` for each fermion (with `C = 1`)

```
n_q := log(m_q^PDG / Λ_QCD) / log(α_s(M_Z))
```

with `Λ_QCD = 0.210 GeV`, `α_s(M_Z) = 0.1181`, `log(α_s) = −2.1359`.

Sign convention: `α_s < 1` so `log(α_s) < 0`. For `m_q > Λ_QCD`,
`n_q < 0`. All quarks have `m_q > Λ_QCD` so all heavy-quark `n_q < 0`;
m_s/m_u/m_d marginal/positive.

| Fermion | m (GeV) | n_q (real) | nearest int | rec. mass | rel.err |
|---|---|---|---|---|---|
| t | 172.69 | −3.142 | −3 | 127.49 | 26.18% |
| b | 4.18 | −1.400 | −1 | 1.7782 | 57.46% |
| c | 1.27 | −0.842 | −1 | 1.7782 | 40.01% |
| s | 0.0934 | +0.379 | 0 | 0.21 | 124.84% |
| u | 2.16e-3 | +2.143 | 2 | 2.929e-3 | 35.60% |
| d | 4.67e-3 | +1.782 | 2 | 2.929e-3 | 37.28% |
| τ | 1.77686 | −1.000 | −1 | 1.7782 | 0.073% |
| μ | 0.10566 | +0.322 | 0 | 0.21 | 98.75% |
| e | 5.110e-4 | +2.817 | 3 | 3.460e-4 | 32.31% |

**Observation A.** Only m_τ closes at integer `n_q` with `C = 1`,
to 0.073%. This near-coincidence is structurally circular (see §1.2):
`Λ_QCD = 210 MeV` is *derived* from `α_s(M_Z) = 0.1181` via 2-loop
running, so `Λ_QCD/α_s(M_Z) = 1.7782 GeV` is a one-parameter relation
already encoded in standard QCD infrastructure, not a two-parameter
identity.

**Observation B.** No heavy quark closes at integer `n_q` with `C = 1`
to 5% mass error. Best heavy-quark integer fit is m_t at `n_q = −3`
with 26.18% mass error.

### Step 2: Test all retained-structural `C` with integer `n_q`

For each `C` candidate, for each fermion, compute
`n_q^*(q, C) = log(m_q / (Λ_QCD · C)) / log(α_s(M_Z))` and check if
`|n_q^* − round(n_q^*)| < 0.0228` (i.e., the integer closure is within
the 5% mass gate, since `log(1.05)/|log(α_s)| ≈ 0.0228`).

Best per-quark single-`C` integer hits found:

| q | C | n_q | m_pred | rel.err |
|---|---|---|---|---|
| t | `4/3` (= C_F) | −3 | 169.98 GeV | **1.57%** |
| b | `√6` | −1 | 4.356 GeV | **4.20%** |
| c | `1/√2` | −1 | 1.257 GeV | **1.00%** |

m_b also matches `√6` (~ 2.449) at 4.2%; this is not a standard QCD
constant. m_c matches `1/√2` at 1.0%; also not a standard QCD constant.
m_t at C_F is the most structurally suggestive (C_F = 4/3 is the
fundamental SU(3) color Casimir).

**Verdict for Step 2:** *No single `C` works for all three heavy quarks
at integer `n_q` to 5%.* Best-fits use three different `C` values, two
of which (√6, 1/√2) are not retained QCD constants.

### Step 3: Test simple-rational `n_q` (q ≤ 6) with retained `C`

Same protocol but allowing `n_q = p/q` with `q ∈ {2, 3, 4, 6}`. With
the larger search space, per-quark fits with **different** rational
denominators exist:

| q | best `(C, p/q)` (single-quark) | rel.err |
|---|---|---|
| t | `(C = 2/3, n = −10/3)` | 0.31% |
| b | `(C = 4, n = −3/4)` | 0.25% |
| c | `(C = 1/2, n = −7/6)` | 0.06% |

These per-quark fits use **three different `C` values** with **three
different denominators** (3, 4, 6). Crucially:

1. **No single retained-structural `C` admits all three at 5%
   simultaneously** with integer `n_q` (Step 2 verdict).
2. **A single `C = √2` does close all three at q ≤ 6 within the 5%
   gate** (m_t at −3 → 4.4%, m_b at −5/4 → 2.6%, m_c at −2/3 → 2.9%),
   but this falls within the **density-of-rationals random band**
   (~37% of random reals admit some q ≤ 6 fit at 5% — see §5). At
   the 1% gate (random density ~8% at q ≤ 6), `C = √2` does **not**
   close any of the three.
3. **No single retained-structural `C` admits all three at the 1% mass
   gate** with q ≤ 6 rationals. The 1% gate is the structurally
   significant threshold (Probe 19 closes m_τ at 0.017%, well below 1%).

**Verdict for Step 3:** the simple-rational-`n_q` route, like the
integer-`n_q` route, fails at the 1% structurally-significant gate.
The 5% q ≤ 6 closure with `C = √2` is a density-of-rationals
coincidence within the 37% random band, not a structural identity.

### Step 4: Density-of-rationals control

Monte Carlo over 10000 random reals `n` uniform in `[−5, 5]`:

| Gate | Integer-only | q ≤ 6 | q ≤ 12 |
|---|---|---|---|
| 5% mass | ~5% | ~37% | ~92% |
| 1% mass | ~1% | ~8% | ~30% |

Random density at the 5% gate is ~5% for integers and ~37% for
`q ≤ 6`. The single-quark hits in Step 2 (1.57%, 4.20%, 1.00%) are
within the random-density 5% band but only m_c at 1.00% is at the 1%
gate (where random density drops to ~8%). The m_t hit at 1.57% with
C_F = 4/3 sits in the borderline zone — between the 1% gate (~8%
random density) and the 5% gate (~37% random density).

### Step 5: Sensitivity to retained-bounded inputs

The probe verifies robustness to:
- `Λ_QCD` choice: `Λ^(5) = 210` vs `Λ^(4) = 290` vs `Λ^(3) = 332` vs
  `Λ^(3)_framework = 389` MeV. Verdict (no single-`C` closure for all
  three heavy quarks at 5%) is robust across these choices.
- `α_s(M_Z)` choice: `0.1181` vs PDG world average `0.1180 ± 0.0009`.
  Verdict robust to the ±0.0009 envelope.
- `⟨P⟩` choice: `0.5934` vs MC value `0.5973 ± 0.0006`. Verdict robust
  to the 0.7% finite-size effect.

### Step 6: Cross-ratio test (m_b/m_c via α_s)

Compute `Δn(m_b/m_c) := log(m_b/m_c)/log(α_s(M_Z))`:
```
Δn(m_b/m_c) = log(3.291)/log(0.1181) = 1.191 / −2.136 = −0.5577
```

Compare to the EW Wilson chain ratio (Probe Y):
```
Δn_EW(m_b/m_c) = log(3.291)/log(α_LM) = 1.191 / −2.401 = −0.4963
```

The EW value is **0.0037 from −1/2** (ultra-clean coincidence per Probe Y).
The QCD value is **0.058 from −1/2** (15× worse, well outside the
1% gate).

**Verdict for Step 6:** the Probe-Y-recorded m_b/m_c ≈ α_LM^{−1/2}
ratio coincidence is **EW-chain-specific** and does NOT transfer to
the QCD-chain. The QCD-chain version of this ratio shows no
particularly clean structure.

### Step 7: Sanity — the m_τ near-coincidence is circular

Verify that `Λ_MS̄^(5) = 210 MeV` ≈ `M_Z · exp(−1/(2·β_0·α_s(M_Z)))`
at 1-loop with `β_0 = (33 − 2 n_f)/(12π) = 23/(12π) ≈ 0.6101` for
`n_f = 5`:

```
Λ_1-loop = 91.19 GeV × exp(−1/(2 × 0.6101 × 0.1181)) ≈ 88 MeV
```

(differs from 210 MeV due to threshold effects and 2-loop corrections,
but order-of-magnitude correct). The point: `Λ_QCD` and `α_s(M_Z)` are
related by a 1-parameter QCD-RGE relation, so `Λ_QCD/α_s(M_Z) ≈ m_τ`
at 0.073% encodes information already contained in the standard
infrastructure used to derive `Λ_QCD` from `α_s(M_Z)`. It is not a
two-parameter structural identity.

## 5. Density-of-rationals control (Monte-Carlo, deterministic seed)

Identical methodology to Probe Y-L1-Ratios §6 but with `α_s(M_Z)`
instead of `α_LM`:
- 10000 random `n` uniform in `[−5, 5]`, fixed seed (42).
- For each `n`, check if `|n − p/q| < 0.0228` for some
  `p/q` with denominator in `{1, 2, 3, 4, 6}` (5% gate).
- Repeat for denominator in `{1, 2, ..., 12}` (verifies q ≤ 12 fits
  carry no structural information).

Results (per Step 4 table). Random hit rate at 5% mass gate:
- Integer-only: ~5%
- q ≤ 6: ~37%
- q ≤ 12: ~92%

The single-quark hits in §1.1 (m_t 1.57%, m_b 4.20%, m_c 1.00%) are
all within the q ≤ 6 random-density band at 5% gate. Only m_c at
1.00% is at the 1% gate; the m_t at 1.57% (with C_F) and m_b at 4.20%
(with √6) are not.

## 6. What this probe does NOT close

This probe does not address:
- **Generation-dependent prefactors.** If `C_t = 4/3`, `C_b = √6`,
  `C_c = 1/√2` were derivable from a unified retained generation
  structure, the QCD chain would close. This probe does not derive
  such structure; the per-quark `C` values may themselves be
  numerical coincidences.
- **Higher-order rationals.** With `q > 6` denominators the
  density-of-rationals control fails (~92% of random reals match at
  q ≤ 12). Therefore no `q > 6` fit can be structurally informative
  without independent retained derivation of the specific denominator.
- **Mixed scale chains.** Hybrid chains
  `m_q = Λ_QCD × M_Pl^a × α_s^b × α_LM^c` are not tested; this would
  require a much larger search and was foreclosed in Probe X for the
  pure-EW direction. This probe focuses specifically on the QCD-only
  parallel chain.
- **Non-perturbative QCD content.** The string tension `√σ ≈ 465 MeV`
  and the chiral condensate `<ψ̄ψ>^{1/3} ≈ 250 MeV` are also retained-
  bounded scales. These could anchor alternative chains; preliminary
  check shows m_q at integer `n_q` with `√σ` or `<ψ̄ψ>^{1/3}` does not
  improve over Λ_QCD = 210 MeV.

## 7. Cross-references

- Probe 19 source-note:
  [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
- Probe X-L1-Threshold source-note:
  [`KOIDE_X_L1_THRESHOLD_HEAVY_QUARK_WILSON_NOTE_2026-05-08_probeX_L1_threshold.md`](KOIDE_X_L1_THRESHOLD_HEAVY_QUARK_WILSON_NOTE_2026-05-08_probeX_L1_threshold.md) (PR #933)
- Probe Y-L1-Ratios source-note:
  [`KOIDE_Y_L1_RATIOS_WILSON_INTEGER_DIFF_NOTE_2026-05-08_probeY_L1_ratios.md`](KOIDE_Y_L1_RATIOS_WILSON_INTEGER_DIFF_NOTE_2026-05-08_probeY_L1_ratios.md) (PR #946)
- Confinement and string tension authority:
  [`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md)
- α_s(M_Z) bounded retained:
  [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
- Low-energy running bridge:
  [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md)

## 8. Honest non-claims

This probe does NOT claim:
- A framework-native derivation of `Λ_QCD` (it is bounded standard QCD
  infrastructure derived from `α_s(M_Z)`).
- A framework-native derivation of `α_s(M_Z)` independent of the
  upstream plaquette analytic insertion gap (per
  [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md) bounded scope).
- That the m_t at C_F = 4/3, n = −3 hit (1.57%) is structurally
  derivable; it is recorded as a post-hoc observation only.
- That the m_τ ≈ Λ_QCD/α_s(M_Z) near-coincidence at 0.073% is an
  independent positive result; it is structurally circular per §1.2.
- Any change to the existing retained-bounded scope of `Λ_QCD`,
  `α_s(M_Z)`, or any upstream authority.

## 9. Audit-lane authority

This is a **source-note proposal**. Pipeline-derived status and
downstream propagation are set only by the independent audit lane,
not by this note. The verdict written here is **negative/bounded**:
the parallel QCD-confinement chain `m_q = Λ_QCD × C × α_s^{n_q}` does
NOT close the heavy-quark mass triplet `(m_t, m_b, m_c)` at the 5%
mass precision gate under any single retained-derivable structural
prefactor `C`.

The probe contributes one closure to the strategic option space:
the parallel QCD-anchored chain is now known to fail in addition to
the EW absolute and EW ratio routes (Probes X and Y respectively).
Heavy-quark masses require a qualitatively different mechanism than
*any* single coupling-chain at integer or simple-rational exponents.

## 10. Constraints respected

- **No new axioms.** All inputs from retained Cl(3)/Z³ + retained-
  bounded QCD content (Λ_QCD, α_s(M_Z) per existing notes).
- **No new imports.** PDG fermion masses used only as comparators
  after `n_q` is computed.
- **No fitting.** All `C` candidates are retained-derivable structural
  constants; none introduced for this probe.
- **No promotion.** The two near-hits (m_τ at 0.073%, m_t at 1.57%)
  are recorded as observations, not promoted; the m_τ hit is
  identified as structurally circular.

PASS = 27, FAIL = 0 across all probe checks (see runner output cache).
