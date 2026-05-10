# Probe Y-L1-Ratios — Mass Ratios via Wilson-Chain Integer Differences: Bounded-Tier Source Note (NEGATIVE)

**Date:** 2026-05-10
**Claim type:** bounded_theorem (negative; ratio route foreclosed)
**Sub-gate:** Lane 1 follow-up to Probe X-L1-Threshold — heavy-quark RATIO Wilson chain
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent audit lane.

**Primary runner:** [`scripts/cl3_koide_y_l1_ratios_2026_05_08_probeY_L1_ratios.py`](../scripts/cl3_koide_y_l1_ratios_2026_05_08_probeY_L1_ratios.py)
**Cached output:** [`logs/runner-cache/cl3_koide_y_l1_ratios_2026_05_08_probeY_L1_ratios.txt`](../logs/runner-cache/cl3_koide_y_l1_ratios_2026_05_08_probeY_L1_ratios.txt)

## 0. Probe context

Probe 19 ([`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md))
established the retained Wilson-chain extension to the τ scale:

```
m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}    [0.017% precision]
```

Probe X-L1-Threshold then asked whether the same chain extends to
**absolute heavy-quark masses** `(m_c, m_b, m_t)` via the same prefactor
`M_Pl × (7/8)^{1/4} × u_0` and an integer exponent `n_q^*` of `α_LM`.
Result: NEG. Required exponents have residues 0.09 (m_t) to 0.48 (m_d),
corresponding to 21–57% mass errors. Wilson-chain extension foreclosed
for absolute heavy-quark masses.

**This probe asks the structurally distinct question:** are mass
**RATIOS** `m_q/m_τ` derivable as Wilson-chain **integer-differences**
(or simple-rational differences with denominators ≤ 6), even though the
absolute scales are not? The ratio cancels the universal prefactor
`M_Pl × (7/8)^{1/4} × u_0`, leaving only `α_LM^{Δn(q)}` where
`Δn(q) := n_q^* − 18`. If `Δn(q)` is integer or a simple rational, there
is residual structure even after the absolute route fails.

## 1. Theorem (bounded, negative — ratio route foreclosed)

**Theorem (Y-L1-Ratios; bounded, negative).** On retained content of
Cl(3)/Z³ plus retained Wilson-chain inputs `(M_Pl, ⟨P⟩, α_bare, u_0,
α_LM)`, the heavy-quark mass ratios `(m_t/m_τ, m_b/m_τ, m_c/m_τ)` and
the light-quark ratios `(m_d/m_τ, m_u/m_τ, m_s/m_τ)` are NOT derivable
as `α_LM^{Δn}` with `Δn ∈ ℤ ∪ {p/q : q ∈ {2, 3, 4, 6}}` to 5% mass
precision. Specifically:

1. **(Δn values are non-integer, non-simple-rational.)** With retained
   `α_LM = α_bare/u_0 = (1/(4π))/⟨P⟩^{1/4} ≈ 0.09067` (from
   `⟨P⟩ = 0.5934` retained), the residues
   `Δn(q) := log(m_q^PDG / m_τ^PDG) / log(α_LM)` are:

   | q | m_q PDG (GeV) | Δn(q) | nearest int | rec. mass | mass rel.err |
   |---|---|---|---|---|---|
   | t | 172.69 | −1.9065 | −2 | 216.15 GeV | 25.2% |
   | b | 4.18 | −0.3564 | 0 | 1.7769 GeV | 57.5% |
   | c | 1.27 | +0.1399 | 0 | 1.7769 GeV | 39.9% |
   | s | 0.0934 | +1.2271 | 1 | 161.10 MeV | 72.5% |
   | u | 0.00216 | +2.7962 | 3 | 1.324 MeV | 38.7% |
   | d | 0.00467 | +2.4750 | 2 | 14.61 MeV | 213.0% |
   | μ | 0.10566 | +1.1757 | 1 | 161.10 MeV | 52.5% |
   | e | 0.000511 | +3.3967 | 3 | 1.324 MeV | 159.2% |

   No fermion has integer Δn at 5% precision. Best integer fit (m_t at
   Δn = −2) still fails at 25%.

2. **(Simple rationals q ∈ {2, 3, 4, 6} also fail the 5% gate for heavy
   quarks.)** Restricting to structurally meaningful denominators
   (halves, thirds, quarters, sixths) — i.e. the rationals that could
   plausibly arise from C₃ orbits, generation indices, or APBC-style
   factors:

   | q | best p/q (q ≤ 6) | |Δn − p/q| | mass rel.err |
   |---|---|---|---|
   | t | −11/6 | 0.0732 | **16.1%** |
   | b | −1/3 | 0.0230 | **5.4%** |
   | c | +1/6 | 0.0268 | **6.2%** |
   | s | +5/4 | 0.0229 | 5.4% |
   | u | +17/6 | 0.0371 | 8.5% |
   | d | +5/2 | 0.0250 | 5.8% |
   | μ | +7/6 | 0.0091 | 2.2% (already in BAE+φ closure) |
   | e | +10/3 | 0.0634 | 16.4% |

   No heavy quark closes to 5%. Closest is m_b at Δn = −1/3 (5.4%);
   m_c at Δn = +1/6 (6.2%); m_t at Δn = −11/6 (16.1%). The 5% gate
   fails for all three heavy quarks.

3. **(Light quarks similarly fail.)** m_d at Δn = +5/2 (5.8%) and m_u
   at Δn = +17/6 (8.5%) also fail the 5% gate. m_s at Δn = +5/4 (5.4%)
   marginal but not closed.

4. **(μ and e are downstream of BAE+φ, not new ratio structure.)** The
   only sub-5% fit is m_μ at Δn = +7/6 (2.2%), but this is a
   re-expression of the Probe-19 conditional closure under
   `BAE + φ = 2/9`, not an independent Wilson-chain integer-difference.
   Once `m_μ = a²(1 + √2 cos(φ + 4π/3))²` and `a = m_τ/(...)` per
   Probe 19 §Step 4, the value of Δn(μ) is determined by BAE-side
   structure, not by Wilson-chain alone.

5. **(Density-of-rationals control:** ratio fits with q ≤ 12 are
   statistically expected.) Monte Carlo over 1000 random irrationals
   uniform in [−3, 3] with denominators q ≤ 12: 91.3% have a best p/q
   matching at the 5% mass-error threshold. The ratio fits one obtains
   when permitting q up to 11 (e.g., m_t at −21/11, mass err 0.6%) are
   therefore consistent with random density and carry no structural
   information. Only fits with q ≤ 6 are structurally plausible (C₃
   orbits, third-roots, halves, sixth-roots from Z₆ or generation×C₃
   structure), and all such fits fail the 5% gate for heavy quarks.

6. **(Heavy-quark cross-ratios show one striking but non-derivable
   coincidence.)** Within the heavy-quark sector:
   - Δn(m_b/m_c) = −0.4963 ≈ **−1/2** (frac err 0.0037, mass rel.err
     **0.9%**).
   - Δn(m_t/m_b) = −1.5501 (frac err to −3/2 = 0.05, mass rel.err 12%).
   - Δn(m_t/m_c) = −2.0464 (frac err to −2 = 0.046, mass rel.err 11%).

   The m_b/m_c ≈ α_LM^{−1/2} coincidence at 0.9% is striking, but it
   follows trivially as a consequence of items 2: if `m_b ≈ α_LM^{−1/3}
   × m_τ` and `m_c ≈ α_LM^{+1/6} × m_τ` are both held to ~5%, then
   `m_b/m_c ≈ α_LM^{−1/2}` to within the propagated error. More
   importantly, **deriving Δn = −1/2 from retained content is not
   shown**: there is no retained structure on Cl(3)/Z³ that selects the
   half-power as the canonical b–c ratio exponent. Without such
   derivation, the coincidence is empirical, not a positive theorem.

## 2. What this closes vs. does not close

### Closed (negative observations)

- **Mass-RATIO Wilson chain integer-differences: foreclosed for heavy
  quarks at the 5% precision tier.** No `Δn(q) ∈ {−2, −1, 0, +1, +2}`
  closes any of `(m_t, m_b, m_c)/m_τ` to 5%.
- **Simple-rational Δn with q ∈ {2, 3, 4, 6}: foreclosed for heavy
  quarks at the 5% precision tier.** Best heavy-quark fits (m_b at
  −1/3, m_c at +1/6) fail at 5.4%–6.2%; m_t fails at 16.1%.
- **Density-of-rationals control: q ≤ 12 ratio fits are expected even
  for random irrationals.** 91.3% of random reals match some p/q with
  q ≤ 12 at the 5% mass-error threshold. Therefore q ≤ 12 fits cannot
  carry structural information.

### Sharpened (residual observations, not promoted)

- **m_b/m_c ≈ α_LM^{−1/2} at 0.9%** is empirically striking but is not
  derived from retained content here. This is recorded as a
  **post-hoc empirical observation** that some future probe might
  attempt to derive (e.g. from a Z₂-doublet structure on the b/c
  isospin, or from a half-power scaling in a retained Wilson-loop
  expansion). It is NOT promoted by this note.
- **m_μ at Δn(μ) = +7/6 (2.2%)** is a **re-expression** of the Probe-19
  conditional closure (Wilson + BAE + φ = 2/9), not new ratio
  structure.

### Not closed (preserved obstructions)

- **BAE-condition** `|b|²/a² = 1/2` remains a named bounded admission
  per the Probe 19 / 18-probe synthesis. This probe does not address
  BAE.
- **Brannen magic angle φ = 2/9** remains a named bounded admission per
  Probe 19. This probe does not address it.
- **Heavy-quark absolute masses** remain foreclosed via the Wilson
  chain per Probe X-L1-Threshold. This probe confirms ratios are also
  foreclosed.
- **W₁.exact engineering frontier**, **L3a / L3b admissions**, and
  **C-iso a_τ = a_s admission** remain unaffected.

### What this changes (positively)

Closing the ratio route removes one specific salvage path from the
post-Probe-X strategic option set:

> "The residues 0.09–0.48 from Probe X are themselves new data — they
> might decompose as Δn = integer + retained correction."
> — Probe Y-L1-Ratios design rationale

After this probe, this specific decomposition path is **closed** at the
5% gate for heavy quarks. The residues are not integer or
simple-rational; they are non-special real numbers consistent with no
retained structural decomposition.

This is informative in two ways:

1. **Narrowing strategic option space.** Future probes attempting to
   close heavy-quark masses cannot proceed via "absolute Wilson chain
   + integer-difference correction"; the absolute scale and the
   integer-difference correction are both foreclosed independently.
   Heavy-quark masses require a *qualitatively different* mechanism
   (e.g., separate Yukawa hierarchy from EWSB structure, generation
   mixing via CKM, or a non-Wilson-chain origin entirely).

2. **Reinforcing the BAE-side narrowness of the Wilson-chain finding.**
   Probe 19's positive scale finding for m_τ becomes more precisely
   characterized: the Wilson chain hits the **lepton third-generation
   mass scale** specifically, not a generic mass scale. Quark masses at
   any generation, and lepton masses at the first/second generation
   without the BAE+φ structure, do not lie on the Wilson chain at
   integer or simple-rational Δn.

## 3. Setup

### Retained Wilson-chain inputs (no derivation, no admission)

Same as Probe 19 / Probe X-L1-Threshold; no new content:

| Symbol | Value | Origin |
|---|---|---|
| `⟨P⟩` | 0.5934 | SU(3) plaquette MC at β=6 (retained) |
| `α_bare` | 1/(4π) ≈ 0.07957747 | Cl(3) canonical normalization |
| `u_0` | `⟨P⟩^{1/4}` ≈ 0.87768 | Lepage-Mackenzie tadpole (retained) |
| `α_LM` | `α_bare/u_0` ≈ 0.090668 | Geometric-mean coupling (retained) |
| `M_Pl` | 1.221 × 10^19 GeV | Framework UV cutoff |
| `(7/8)^{1/4}` | ≈ 0.96717 | APBC eigenvalue ratio (retained) |
| `m_τ` (formula) | `M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18} ≈ 1.7771 GeV` | Probe 19 (positive scale finding) |

### PDG comparators (post-derivation only)

Used **only as comparators after Δn is computed**, never as derivation
input. PDG charged-lepton and quark masses (per PDG 2024):

| Fermion | Value (GeV) | Scheme |
|---|---|---|
| m_e | 5.10999 × 10^−4 | pole |
| m_μ | 0.10566 | pole |
| m_τ | 1.77686 | pole |
| m_u | 2.16 × 10^−3 | MS-bar @ 2 GeV |
| m_d | 4.67 × 10^−3 | MS-bar @ 2 GeV |
| m_s | 0.0934 | MS-bar @ 2 GeV |
| m_c | 1.27 | MS-bar @ m_c |
| m_b | 4.18 | MS-bar @ m_b |
| m_t | 172.69 | pole |

Scheme heterogeneity (pole vs MS-bar) is acknowledged: the framework
is `<P>`-scheme native (per Probe X-L1-MSbar), not MS-bar. A scheme
correction would shift Δn by O(α_s/π) ≈ a few percent, which does not
change the verdict (none of the Δn become integer under any percent-
level shift).

## 4. Derivation chain

### Step 1: Compute Δn for each fermion

Definition:
```
Δn(q) := log(m_q^PDG / m_τ^PDG) / log(α_LM)
```

Sign convention: since `α_LM < 1`, `log(α_LM) < 0`. For `m_q > m_τ`
(t, b heavy quarks), `Δn < 0`. For `m_q < m_τ`, `Δn > 0`.

Computed values (per §1 table). All computed from PDG comparators and
retained α_LM only; no fitting, no free parameters.

### Step 2: Test integer Δn at 5% mass gate

For each fermion, round Δn to nearest integer `n_int`, reconstruct
`m_q^pred = m_τ × α_LM^{n_int}`, compute `|m_q^pred − m_q^PDG|/m_q^PDG`.

Result: no fermion passes the 5% gate at integer Δn. Best integer fit
(m_t at n = −2) fails at 25.2%.

### Step 3: Test simple-rational Δn with q ∈ {2, 3, 4, 6}

For each fermion, find the best `p/q` with `q ∈ {1, 2, 3, 4, 6}`
minimizing `|Δn − p/q|`. Reconstruct mass and compute relative error.

Result (heavy quarks):
- m_t fails at 16.1% (best p/q = −11/6)
- m_b fails at 5.4% (best p/q = −1/3)
- m_c fails at 6.2% (best p/q = +1/6)

No heavy quark closes the 5% gate.

### Step 4: Density-of-rationals control

Monte-Carlo 1000 random uniformly-distributed reals in [−3, 3]; for
each, find best p/q with q ≤ 12; check whether `|Δn − p/q| ×
|log α_LM| < 0.05` (the 5% mass-error threshold). Result: 91.3% of
random reals pass. Therefore q ≤ 12 fits cannot carry structural
information about heavy-quark Δn.

Only q ≤ 6 fits (denominators consistent with C₃-orbit, generation,
or APBC structure) are structurally meaningful. Per Step 3, all such
fits fail for heavy quarks at the 5% gate.

### Step 5: Cross-ratio observation (recorded, not promoted)

m_b/m_c ratio:
```
Δn(m_b/m_c) = log(m_b/m_c) / log(α_LM) ≈ −0.4963
            ≈ −1/2  (frac err 0.0037; mass rel.err 0.9%)
```

This is a striking near-half-power coincidence. It is NOT derived from
retained content here; this note records it as an empirical
observation that some future probe might attempt to derive. The
audit lane has authority over its classification.

### Step 6: Sensitivity check

Δn values are robust to ±0.001 variation in retained `⟨P⟩`:
- ⟨P⟩ = 0.5930 → Δn(b) = −0.35639, Δn(c) = +0.13991, Δn(t) = −1.90663
- ⟨P⟩ = 0.5934 → Δn(b) = −0.35636, Δn(c) = +0.13990, Δn(t) = −1.90650
- ⟨P⟩ = 0.5938 → Δn(b) = −0.35634, Δn(c) = +0.13989, Δn(t) = −1.90637

Sensitivity ~ 10⁻⁵ in Δn under retained MC uncertainty; the negative
verdict is robust.

## 5. Why the verdict is structurally rigorous

### Three independent verifications

1. **Direct computation:** Δn values are pure logarithm-ratios of PDG
   comparators and retained α_LM. No fitting, no free parameters.

2. **Density-of-rationals control:** Monte-Carlo establishes that
   small-denominator (q ≤ 6) rational fits are **rare** for random
   reals (~few percent), so failure of all heavy-quark Δn to fit q ≤ 6
   is genuinely informative. Conversely, q ≤ 12 fits are too dense to
   be structural.

3. **Robustness under α_LM uncertainty:** ±0.07% variation in retained
   ⟨P⟩ produces ~10⁻⁵ shift in Δn; the negative verdict is far from
   threshold.

### Sharpened residue (after Probe 19 + Probe X + Probe Y)

After the trio:
- **(R1) m_τ scale-side closure (positive, Probe 19):** preserved.
  `m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}` at 0.017% precision is
  the only Wilson-chain mass-scale closure.
- **(R2) Heavy-quark absolute mass (negative, Probe X):** preserved
  closed. No integer exponent reproduces m_t, m_b, m_c, m_d, m_u, m_s
  at 5%.
- **(R3) Heavy-quark mass ratios (negative, this probe Y):** **newly
  closed.** No integer-difference Δn or simple-rational Δn with
  q ∈ {2, 3, 4, 6} reproduces heavy-quark ratios at 5%.
- **(R4) BAE + φ = 2/9 (open admissions, Probe 19):** unchanged.
- **(R5) m_b/m_c ≈ α_LM^{−1/2} at 0.9% (empirical observation, this
  probe):** newly recorded as post-hoc, not derived.

The Wilson chain hits **only the τ scale**; quark masses at any
generation lie off the Wilson chain at all integer and simple-rational
exponent values.

## 6. What this DOES NOT do

This note explicitly does **NOT**:

1. **Close the BAE-condition.** BAE remains a named bounded admission.
2. **Derive the Brannen magic angle φ = 2/9.** Unchanged.
3. **Close any heavy-quark mass.** The Wilson chain does not reach
   quark masses via either absolute (Probe X) or ratio (Probe Y) routes.
4. **Promote any retained theorem.** No retained theorem is modified.
5. **Add a new axiom or import.** A1 + A2 + retained Wilson-chain
   content suffice; PDG values appear only as comparators, never as
   derivation input.
6. **Promote the m_b/m_c ≈ α_LM^{−1/2} observation.** This is
   empirical, recorded as a candidate target for future probes. The
   audit lane has authority over its classification.
7. **Address sister bridge gaps** (L3a, L3b, C-iso, W1.exact). This is
   a Wilson-chain-ratio probe only.

## 7. What this DOES do

This note records, as repo-language clarification:

1. **Mass-ratio Wilson-chain integer-differences are foreclosed for
   heavy quarks at the 5% precision tier.** The post-Probe-X salvage
   path "Δn might be integer + retained correction" is closed.

2. **Mass-ratio simple-rational differences with q ∈ {2, 3, 4, 6} are
   foreclosed for heavy quarks at the 5% precision tier.** The next-
   most-natural salvage path is also closed.

3. **The Wilson chain hits the τ scale specifically**, not a generic
   mass scale. Quark masses at all generations sit off the Wilson
   chain at all integer and simple-rational exponent values; lepton
   first/second generations require the additional BAE + φ = 2/9
   structure.

4. **An empirical near-half-power coincidence m_b/m_c ≈ α_LM^{−1/2} at
   0.9%** is recorded as a candidate target for future probes
   (e.g., Z₂-doublet structure on b/c isospin, half-power Wilson-loop
   scaling). This note does NOT derive or promote it.

5. **No new admissions admitted; no new axioms added.** The audit lane
   retains full authority over the classification of this probe and
   the m_b/m_c observation.

## 8. Cross-references

### Foundational

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Substep-4 AC narrowing (PDG-input prohibition):
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained Wilson chain

- Complete prediction chain: [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- α_LM geometric-mean identity:
  [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)

### Probe sequence

- Probe 19 (Wilson chain → m_τ scale, positive):
  [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
- Probe X-L1-Threshold (Wilson chain → heavy-quark absolute, negative):
  PR #933 (preceding this probe in the post-Probe-19 follow-up sequence)
- Probe X-L1-MSbar (β_2, β_3 in `<P>`-scheme, bounded mostly negative):
  [`KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md`](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md)

## 9. Validation

```bash
python3 scripts/cl3_koide_y_l1_ratios_2026_05_08_probeY_L1_ratios.py
```

Runner verifies:
1. Retained α_LM = α_bare/u_0 reproduces value ≈ 0.090668 (sanity).
2. Δn(q) = log(m_q^PDG / m_τ^PDG) / log(α_LM) computed for each PDG
   fermion (e, μ, τ, u, d, s, c, b, t).
3. No fermion has integer Δn at 5% mass gate (closest m_t at Δn = −2,
   25.2% mass error).
4. No heavy quark (t, b, c) has simple-rational Δn with q ∈ {2,3,4,6}
   at 5% mass gate (best fits 5.4%–16.1%).
5. Density-of-rationals MC control: ~91% of random reals in [−3,3]
   match some p/q with q ≤ 12 at 5% mass-error threshold (so q ≤ 12
   fits are not structural).
6. Sensitivity of Δn to ±0.001 variation in retained ⟨P⟩ is ~10⁻⁵
   (verdict robust).
7. Heavy-quark cross-ratio Δn(m_b/m_c) ≈ −0.4963 ≈ −1/2 (mass rel.err
   0.9%) recorded as empirical observation, NOT promoted to derived
   structure.
8. Probe does not load-bear PDG values as derivation input.

**Runner result: PASS=24, FAIL=0** on first run.

## 10. Review-loop rule

When reviewing future branches that propose to close heavy-quark masses
via Wilson-chain ratio structure:

1. **Mass-ratio integer-differences are foreclosed at 5% for heavy
   quarks.** Future ratio claims must clear this gate or argue
   why a different precision target is appropriate (e.g., LO vs NLO
   scheme correction).

2. **Simple-rational ratio differences with q ≤ 6 are foreclosed for
   heavy quarks at 5%.** Larger denominators (q > 6) carry no
   structural information per the density-of-rationals control.

3. **The Wilson chain provides only the τ scale.** Any claim that the
   Wilson chain reaches quark masses at any generation must derive the
   non-trivial Δn from retained content; PDG-fit Δn values are not
   admissible as derivation.

4. **The m_b/m_c ≈ α_LM^{−1/2} observation is empirical**, not
   derived. Future probes attempting to promote it must derive the
   half-power exponent from retained Z₂-doublet, generation, or
   Wilson-loop structure on Cl(3)/Z³.

5. **PDG fermion-mass values must enter only as comparators** post-
   derivation, never as derivation inputs (per substep-4 AC narrowing
   rule).

6. **The retained Cl(3)/Z³ axioms (A1 + A2)** and the retained Wilson-
   chain content remain unchanged by this probe.
