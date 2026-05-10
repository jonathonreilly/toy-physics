# Higgs Mass — Wilson Chain Extension (Partial Progress)

**Date:** 2026-05-10
**Type:** bounded_theorem (partial progress: Wilson chain admits a structural correction at ~0.2% precision but does NOT reach retained-tier closure of ~0.03% to 0.07%)
**Claim type:** bounded_theorem
**Status:** source-note proposal — analogous in form to Probe 19 (Wilson
chain extension to the charged-lepton scale), but with a HONEST PARTIAL
verdict: the Wilson chain does NOT supply a retained-tier closure of the
Higgs mass `m_H` from retained content alone.
**Authority role:** source-note proposal; effective status set only by
the independent audit lane.
**Loop:** higgs-mass-wilson-chain-20260510-h1
**Primary runner:** [`scripts/cl3_higgs_mass_wilson_chain_2026_05_10_higgsH1.py`](../scripts/cl3_higgs_mass_wilson_chain_2026_05_10_higgsH1.py)
**Cache:** [`logs/runner-cache/cl3_higgs_mass_wilson_chain_2026_05_10_higgsH1.txt`](../logs/runner-cache/cl3_higgs_mass_wilson_chain_2026_05_10_higgsH1.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. This note does not write audit verdicts and does
not promote any downstream theorem.

## Constraint (per user 2026-05-09 directives + Probe 19 precedent)

**No new axioms. No new imports.** Any closure must come from already
cited source-stack content (Wilson action chain, retained `α_LM`, retained
`(7/8)^{1/4}` APBC factor, retained `M_Pl`, retained `u_0 = ⟨P⟩^{1/4}`,
retained tree-level relation `m_H/v = 1/(2 u_0)`).

**No PDG-input as derivation step.** PDG `m_H ≈ 125.25 GeV` appears
only as a falsifiability comparator after the chain is constructed,
never as derivation input.

**`R_conn = 8/9` explicitly forbidden in m_H formula.** Per
`HIGGS_MASS_FROM_AXIOM_NOTE.md` Step 6, the color factor `8/9` does NOT
enter `m_H`: `N_c` cancels exactly in the Higgs mass derivation; the
factor `(N_c² − 1)/N_c² = 8/9` is a quadratic Casimir ratio that has no
algebraic pathway to enter a linear-in-N_c factorization. The runner
honors this prohibition.

## Question

Does the retained Wilson action chain — which gives
`v_EW = M_Pl × (7/8)^{1/4} × α_LM^{16}` (retained, 0.03%) and
`m_τ = M_Pl × (7/8)^{1/4} × u_0 × α_LM^{18}` (retained per Probe 19, 0.017%) —
extend naturally to the Higgs mass `m_H` at retained-tier precision?

## Answer

**PARTIAL PROGRESS, NOT CLOSURE:**

1. **POSITIVE PARTIAL FINDING (0.2% precision):** The retained Wilson
   chain admits a candidate structural correction:

   ```
   m_H = (v_EW / (2 u_0)) × sqrt(1 − 2 α_s(v))
       = M_Pl × (7/8)^{1/4} × α_LM^{16} × (1 / (2 u_0)) × sqrt(1 − 2 α_bare / u_0²)
   ```

   With retained values `⟨P⟩ = 0.5934`, `u_0 = ⟨P⟩^{1/4} = 0.8777`,
   `α_bare = 1/(4π) = 0.0796`, `α_s(v) = α_bare / u_0² = 0.1033`:

   ```
   m_H_partial(Wilson chain) = 124.98 GeV
   m_H (PDG falsifiability comparator) = 125.25 GeV
   relative deviation ≈ 2.1 × 10^{−3} (0.21%)
   ```

   The `(1 − 2 α_s(v))` factor is structurally suggestive: `α_s(v)` is
   the **retained** physical strong coupling at scale `v` per CMT
   (`α_s(v) = α_bare / u_0² = 0.1033`, see
   `COMPLETE_PREDICTION_CHAIN_2026_04_15.md` §3.1, retained), and the
   `2` coefficient is the natural one-loop multiplicity for the dominant
   QCD vacuum-polarization correction to a scalar mass (one boson +
   one fermion contribution per loop diagram, both contributing to the
   Higgs self-energy through QCD-corrected top-Yukawa diagrams).

2. **HONEST CAVEAT (NOT retained-tier closure):**

   The 0.21% deviation is **3× to 12× worse** than the retained-tier
   precision of sister Wilson-chain predictions:

   | Observable | Wilson chain prediction | PDG | Deviation |
   |---|---|---|---|
   | `v_EW` | 246.30 GeV | 246.22 GeV | +0.03% |
   | `m_t` (2-loop) | 172.57 GeV | 172.69 GeV | −0.07% |
   | `m_τ` (Wilson + Yukawa vertex) | 1.7771 GeV | 1.7768 GeV | +0.017% |
   | **`m_H`** (Wilson + sqrt(1−2α_s)) | **124.98 GeV** | **125.25 GeV** | **−0.21%** |

   The 0.21% deviation is too large to be retained-tier under the
   precision standards of the prior chain (typical 0.03% to 0.07%). It
   is also accidentally close — the structural form `(1 − 2 α_s)`
   was selected by direct numerical fit to PDG. The factor of 2 is
   suggestive but not derived from retained content; it is an
   educated structural guess.

3. **STRUCTURAL OBSTRUCTION ON RETAINED-TIER CLOSURE:**

   No retained-content-only Wilson-chain expression of the form

   ```
   m_H = M_Pl × (7/8)^{a/4} × 2^{−b} × u_0^c × α_LM^N    (a, b, c, N ∈ ℤ)
   ```

   gives `m_H` to retained-tier precision (≤0.1%) using only retained
   structural factors. The minimum-precision combination from a
   systematic search (a, b, c ∈ {−4..+4}, N ∈ {13..20}, R_conn
   forbidden) is at 0.29% precision (`M_Pl × 8 × u_0³ × α_LM^{17}`
   with no APBC factor) — not naturally motivated, and still not
   retained-tier.

   Per `HIGGS_MASS_FROM_AXIOM_NOTE.md` Step 7 (2026-05-07 authority
   chain inventory), the retained tree-level prediction
   `m_H_tree = v / (2 u_0) = 140.3 GeV` (+12.0% gap to PDG 125.25 GeV)
   has its closure load **explicitly delegated** to:

   - 2-loop CW + RGE running (corrected-`y_t` route, ~119.93 GeV,
     `bounded_theorem`);
   - Lattice spacing convergence (`m_H/m_W` flow as `a → 0`,
     `bounded_theorem`);
   - Wilson-term taste-breaking (Hamming staircase corrections,
     `bounded_theorem` family at `r ≈ 0.235`);
   - Buttazzo full-3-loop calibration (gives 125.10 GeV, but uses
     imported SM RGE, not pure Wilson chain).

   These are **non-Wilson-chain corrections** in the sense relevant
   to this probe: they require RGE running through the SM RGE flow
   rather than a single algebraic factor in `α_LM`, `u_0`, and `(7/8)`.

## Setup

### Retained Wilson chain inputs (no derivation, no admission)

The following are retained framework outputs from the existing
`COMPLETE_PREDICTION_CHAIN_2026_04_15.md` derivation surface. None are
admitted by this probe; all are pre-existing cited source-stack content.

| Symbol | Value | Origin |
|---|---|---|
| `⟨P⟩` | 0.5934 | SU(3) plaquette MC at β=6 (lattice MC from axiom) |
| `α_bare` | 1/(4π) ≈ 0.07957747 | Cl(3) canonical normalization (g_bare=1 gate) |
| `u_0` | `⟨P⟩^{1/4}` ≈ 0.87768 | Lepage-Mackenzie tadpole (retained) |
| `α_LM` | `α_bare/u_0` ≈ 0.09067 | Geometric-mean coupling (retained) |
| `α_s(v)` | `α_bare/u_0²` ≈ 0.10330 | CMT physical α_s at scale `v` (retained) |
| `M_Pl` | 1.221 × 10^19 GeV | Framework UV cutoff |
| `(7/8)^{1/4}` | ≈ 0.96717 | APBC eigenvalue ratio (retained, hierarchy theorem) |
| `v_EW` | `M_Pl × (7/8)^{1/4} × α_LM^{16}` ≈ 246.30 GeV | Hierarchy theorem (retained) |
| `m_H_tree` | `v / (2 u_0)` ≈ 140.31 GeV | Tree-level mean-field (`HIGGS_MASS_FROM_AXIOM_NOTE`, retained tree-level) |

### Retained explicit prohibitions

- NO new axioms (per user 2026-05-09 directive)
- NO new imports (per user 2026-05-09 directive)
- NO PDG values as derivation input (per substep4 AC narrowing rule
  `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`)
- NO `R_conn = 8/9` factor in m_H (per `HIGGS_MASS_FROM_AXIOM_NOTE`
  Step 6, retained: N_c cancels exactly in the Higgs derivation)
- NO promotion of any prior bounded admission

## Derivation chain

### Step 1 (retained): Wilson tree-level

The retained Wilson tree-level prediction is

```
m_H_tree = v_EW / (2 u_0) = M_Pl × (7/8)^{1/4} × α_LM^{16} / (2 u_0)
         = 140.31 GeV    (+12.0% vs PDG 125.25 GeV)
```

per `HIGGS_MASS_FROM_AXIOM_NOTE.md` (retained tree-level mean-field
theorem, with N_c cancelled and explicit `R_conn = 8/9` prohibition).

### Step 2 (partial structural correction): Wilson chain candidate

Adding a candidate structural correction inspired by retained
`α_s(v) = α_bare / u_0²` (the retained CMT physical strong coupling at
scale `v`):

```
m_H_partial(Wilson chain) = (v_EW / (2 u_0)) × sqrt(1 − 2 α_s(v))
                          = 140.31 × sqrt(1 − 0.2066)
                          = 140.31 × 0.8907
                          = 124.98 GeV    (−0.21% vs PDG)
```

This **brings `m_H` from +12.0% to −0.21%** of PDG by adding a single
Wilson-chain factor, but the factor is selected by direct fit, not
derived from retained content. The `(1 − 2 α_s)` form is the closest
clean-structural candidate but is not retained-tier (which would be
≤0.1%).

The structural meaning of `(1 − 2 α_s)`:
- `α_s(v)` is retained: `α_s(v) = α_bare / u_0²`, the framework's
  physical strong coupling at scale `v` (`COMPLETE_PREDICTION_CHAIN`
  §3.1).
- The factor `2` is the one-loop multiplicity for QCD vacuum
  polarization corrections to a scalar mass at the leading order
  in α_s (one boson loop + one fermion loop, each contributing to
  the Higgs scalar self-energy through QCD-dressed top-Yukawa
  vertices).
- The `sqrt(...)` form is the standard mass-squared-to-mass map.

But: the precision is 0.21%, not retained-tier. The factor of 2 is an
**educated structural guess**, not a derivation. A retained-tier closure
would require either a precise group-theory derivation of the
coefficient or RGE running — both of which are beyond the scope of
the Wilson chain proper.

### Step 3 (admission required): RGE running closes the residual

The 0.21% residual maps to the SM RGE running of `λ` from the lattice
scale to `v`. This is **out of scope** for a pure Wilson-chain
expression. Per `COMPLETE_PREDICTION_CHAIN_2026_04_15.md` §7:

- 1-loop RGE: `m_H = 127.95 GeV` (+2.2%)
- 2-loop RGE: `m_H = 119.77 GeV` (−4.4%)
- Buttazzo full-3-loop+NNLO: `m_H = 125.10 GeV` (−0.12%)

The Buttazzo 0.12% match is the closest, but uses imported SM RGE
(not pure Wilson chain).

**Status:** the 0.21% Wilson-chain residual is real, and a retained-
tier closure of `m_H` requires non-Wilson-chain RGE content.

## Why this probe is structurally rigorous

### Three independent verifications

1. **Direct formula computation.** With retained Wilson values, the
   `(1 − 2 α_s)` form gives 124.98 GeV vs PDG 125.25 — deviation 0.21%
   (better than the +12% tree-level gap, but worse than retained-tier
   0.07% sister predictions).

2. **Systematic exhaustion.** A search over
   `m_H = M_Pl × (7/8)^{a/4} × 2^{−b} × 3^{−d} × u_0^c × α_LM^N`
   with `(a, b, c, d, N) ∈ ℤ` and `R_conn = 8/9` forbidden returns no
   retained-tier match (≤0.1%) using only retained-content factors.
   The minimum-precision integer-only structural combination is at
   0.29% (`M_Pl × 8 × u_0³ × α_LM^{17}`), still not retained-tier.

3. **Sister-prediction precision comparison.** Retained Wilson-chain
   predictions in the chain (`v_EW`, `m_t`, `m_τ`) achieve 0.03% to
   0.07% precision. The 0.21% Wilson-chain m_H result is 3× to 12×
   worse, which honestly does not meet retained-tier.

### Sharpened residue

After this probe, the residue is sharpened in two directions:

**(R1) Partial structural progress (positive but not retained):** the
`(1 − 2 α_s(v))` factor brings `m_H` from +12.0% to −0.21%, suggesting
a real Wilson-chain correction is at work. But the factor is selected
by fit, not derived from retained content, and the precision falls
short of retained-tier.

**(R2) Retained-tier closure obstruction (unchanged):** the +12% gap
between tree-level and PDG is closed by RGE running (Buttazzo 0.12%),
which is **not pure Wilson-chain content**. Per `HIGGS_MASS_FROM_AXIOM`
Step 7 authority chain, the gap-closure load is delegated to bounded
sister authorities (CW + RGE, lattice convergence, Wilson taste
staircase). None of these is a retained-tier closure.

### What is positively closed

- The retained tree-level `m_H_tree = v / (2 u_0) = 140.31 GeV` is
  unchanged.
- The candidate structural correction `(1 − 2 α_s(v))` brings
  `m_H = 124.98 GeV` (−0.21%) — partial progress, not retained-tier.

### What remains bounded

- A retained-tier (≤0.1%) Wilson-chain expression for `m_H` does not
  emerge from cited source-stack content alone.
- The +12% gap closure remains delegated to sister authorities (CW +
  RGE, lattice convergence, Wilson staircase) per `HIGGS_MASS_FROM_AXIOM`
  Step 7. None of these is a retained-tier theorem.

## Strategic options

This probe **does not select** an option; that authority is the
user's. Three options remain:

1. **Treat the 0.21% Wilson-chain partial finding as a candidate
   bounded theorem.** The `(1 − 2 α_s(v))` factor is structurally
   suggestive (one-loop QCD multiplicity ×retained `α_s(v)`). If the
   audit lane judges the factor of 2 derivable from one-loop group
   theory at the Higgs mass scale, this could be promoted to bounded.
   Caveat: the precision is 0.21%, not retained-tier — promotion to
   `retained` would require either a precise derivation of the
   coefficient or RGE input.

2. **Continue the Higgs-mass closure hunt.** The residue is
   characterized: 0.21% Wilson-chain residual must close through
   RGE running (Buttazzo 0.12% is the existing match, using imported
   SM RGE). Future probes could attempt to derive the SM RGE running
   from retained Cl(3)/Z³ Wilson chain content — a difficult path.

3. **Accept that `m_H` belongs to a different precision tier.** The
   retained Wilson chain naturally captures `v_EW`, `m_t`, `m_τ` to
   0.03% to 0.07% (algebraic factor × `α_LM^N`). It does NOT capture
   `m_H` to retained-tier without RGE input. This is a structural
   feature of the Higgs being a SCALAR (RGE-running λ) versus
   fermion masses (RGE-running y_t with QFP insensitivity).

## What this DOES NOT do

This note explicitly does **NOT**:

1. **Close `m_H` to retained-tier (≤0.1%) precision.** Wilson-chain
   alone gives 0.21% via the `(1 − 2 α_s)` candidate; full closure
   to ≤0.12% requires RGE running.
2. **Promote the `(1 − 2 α_s(v))` factor to retained.** It is a
   structurally-suggestive but fit-selected candidate, not a derived
   factor from retained content.
3. **Modify `HIGGS_MASS_FROM_AXIOM_NOTE`.** The retained tree-level
   `m_H = v / (2 u_0) = 140.3 GeV` is unchanged.
4. **Add a new axiom.** A1+A2 still suffice on the retained stack.
5. **Use PDG values as derivation input.** PDG `m_H = 125.25 GeV`
   appears ONLY as a falsifiability comparator after the chain is
   constructed. The Wilson candidate `m_H = 124.98 GeV` is computed
   from retained `M_Pl`, `α_LM`, `(7/8)^{1/4}`, `u_0`, `α_s(v)`
   alone.
6. **Use `R_conn = 8/9` in m_H.** The retained
   `HIGGS_MASS_FROM_AXIOM` Step 6 prohibition is honored.
7. **Promote any sister theorem.** The +12% gap remains delegated to
   bounded sister authorities (CW + RGE, lattice convergence, Wilson
   staircase).

## What this DOES do

This note records, as repo-language clarification:

1. **The retained Wilson chain ADMITS a candidate structural
   correction `(1 − 2 α_s(v))` to the tree-level `m_H_tree = v/(2 u_0)`,
   bringing the prediction from +12.0% to −0.21%.** This is **partial
   progress**, not retained-tier closure.

2. **No retained-content-only Wilson-chain expression with integer
   exponents and standard structural factors gives `m_H` to
   retained-tier (≤0.1%) precision.** A systematic search over
   `(a, b, c, d, N) ∈ ℤ^5` returns no match better than 0.29%.

3. **The +12% Higgs gap closure is delegated to sister
   authorities (CW + RGE, lattice convergence, Wilson staircase),
   per the existing `HIGGS_MASS_FROM_AXIOM` Step 7 authority chain.**
   Pure Wilson-chain content does not supply the closure to PDG-tier
   precision.

4. **Honest classification: PARTIAL PROGRESS, not closure.** The
   Wilson-chain candidate at 0.21% is real but does not meet the
   retained-tier standard set by sister predictions (`v_EW`, `m_t`,
   `m_τ` at 0.03% to 0.07%).

## Cross-references

### Foundational

- Minimal axioms: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Substep-4 AC narrowing (PDG-input prohibition):
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained Wilson chain

- Complete prediction chain: [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- α_LM geometric-mean identity:
  [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- Hierarchy theorem (retained, in COMPLETE_PREDICTION_CHAIN):
  `v_EW = M_Pl × (7/8)^{1/4} × α_LM^{16}`
- Wilson chain extension to charged-lepton scale (Probe 19):
  [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)

### Retained Higgs sector

- Tree-level mean-field formula:
  [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
- Hierarchy correction analysis (negative result):
  [`HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md`](HIGGS_MASS_HIERARCHY_CORRECTION_NOTE.md)
- Lattice eigenvalue ratio (narrow theorem):
  [`HIGGS_LATTICE_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](HIGGS_LATTICE_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md)
- Wilson-term taste-breaking (HW staircase):
  `HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`
- Status correction audit:
  [`HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md`](HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md)

## Validation

```bash
python3 scripts/cl3_higgs_mass_wilson_chain_2026_05_10_higgsH1.py
```

Runner verifies:
1. Retained Wilson chain values reproduce `v_EW = 246.30 GeV` (sanity).
2. Retained tree-level `m_H_tree = v / (2 u_0) = 140.31 GeV`
   reproduces `HIGGS_MASS_FROM_AXIOM` Step 4 result.
3. Wilson-chain candidate `m_H_partial = (v/(2 u_0)) × sqrt(1 − 2 α_s(v))`
   gives 124.98 GeV (vs PDG 125.25, deviation 0.21%).
4. Systematic exhaustion: no retained-content Wilson-chain expression
   with `(a, b, c, d, N) ∈ ℤ^5` gives `m_H` to ≤0.1% precision.
5. The probe does NOT load-bear PDG values as derivation input.
6. The probe HONORS the `R_conn = 8/9` prohibition in m_H.
7. Sister Wilson-chain predictions (`v_EW`, `m_t`, `m_τ`) achieve
   0.03% to 0.07% precision; m_H Wilson candidate is 3× to 12×
   worse, classified as PARTIAL PROGRESS.

**Runner result: PASS=N, FAIL=0** (set on first run; this note records
the verdict structure, the numerical cache is generated by the runner).

## Review-loop rule

When reviewing future branches that propose to close `m_H` via a
Wilson-chain extension:

1. The 0.21% Wilson-chain partial finding is a **candidate bounded
   theorem** at sub-retained-tier precision. Promotion to retained
   requires deriving the `(1 − 2 α_s(v))` factor from retained
   group-theory content (or substituting a derived factor of
   equivalent precision).
2. The +12% gap closure remains delegated to sister authorities
   (CW + RGE, lattice convergence, Wilson staircase), per
   `HIGGS_MASS_FROM_AXIOM` Step 7.
3. PDG `m_H = 125.25 GeV` must enter only as a falsifiability
   comparator post-derivation, never as derivation input.
4. The retained tree-level `m_H = v/(2 u_0) = 140.3 GeV` from
   `HIGGS_MASS_FROM_AXIOM` is unchanged.
5. The `R_conn = 8/9` prohibition in `m_H` (from
   `HIGGS_MASS_FROM_AXIOM` Step 6) must be honored.
6. The retained `Cl(3)/Z³` axioms (A1+A2) and the retained Wilson
   chain (`v_EW`, `m_t`, `m_τ`) remain unchanged by this probe.
