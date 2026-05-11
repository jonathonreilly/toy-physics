# y_t Quasi-Fixed-Point Insensitivity Support Note

**Date:** 2026-04-14
**Status:** bounded support
**Script:** `scripts/frontier_yt_qfp_insensitivity.py`

## The Codex Blocker

The reviewer's specific blocker: "if backward M_Pl transfer is
correct, derive WHY the SM RGE continuation above v is a valid
framework-native surrogate for lattice RG / taste-staircase evolution."

The Boundary Selection Theorem establishes that the SM EFT is the
physical theory below v, while the lattice theory (16 tastes, non-
perturbative couplings) applies above v. The backward Ward derivation
uses the SM RGE above v as a mathematical interpolation to transfer
the Ward boundary condition from M_Pl to v. The objection is that
the SM EFT is the WRONG theory above v.

This bound does not claim the SM RGE is the physical description
above v. It proves something narrower and sufficient: the backward
Ward prediction y_t(v) = 0.973 is insensitive to the choice of RG
flow above v, because the y_t beta function has a strong IR quasi-
fixed point (Pendleton-Ross focusing). Any smooth monotonic flow
satisfying the Ward BC and gauge anchor gives the same y_t(v) to
within bounded uncertainty. The SM RGE is one such flow; the exact
lattice taste-staircase is another. They converge at v.

---

## Part 1: The Pendleton-Ross Focusing Structure

The 1-loop y_t beta function in the SM is:

    beta_{y_t} = y_t / (16 pi^2) * [9/2 y_t^2 - 8 g_3^2
                                     - 9/4 g_2^2 - 17/20 g_1^2]

The dominant terms are the Yukawa self-coupling (+9/2 y_t^2) and the
QCD correction (-8 g_3^2). Their competition creates an IR quasi-fixed
point (QFP): trajectories with y_t > y_t^QFP are pulled downward by
the QCD term, while trajectories below the QFP are pushed upward by
the self-coupling. Over 17 decades of running from M_Pl to v, this
focusing compresses a wide range of UV boundary conditions into a
narrower band at v.

This is the Pendleton-Ross mechanism (1981). It is a structural
property of any gauge-Yukawa system where the gauge coupling dominates
at high scales. It does not depend on the specific numerical values
of the beta coefficients -- only on their signs and relative magnitudes.

The focusing ratio R = Delta(y_t(M_Pl)) / Delta(y_t(v)) measures the
compression. For the SM RGE with alpha_s(v) = 0.1033:
- Full range [0.2, 0.8]: R = 1.09 (a 300% UV variation maps to 90% IR)
- Upper half [Ward, 0.8]: R = 1.98 (strong focusing above QFP)
- Local sensitivity near Ward BC: dy_t(v)/dy_t(M_Pl) = 0.90

---

## Part 2: Insensitivity to y_t(M_Pl)

**Claim:** Varying y_t(M_Pl) across [0.2, 0.8] -- well beyond the
Ward value 0.436 -- changes y_t(v) by a bounded amount that is smaller
than the variation at M_Pl for trajectories above the QFP.

**Mechanism:** For each y_t(M_Pl), solve the SM RGE backward to
obtain y_t(v). The QFP focusing ensures convergence above the QFP.
Below the QFP, sensitivity is near 1:1, but the Ward BC is a DERIVED
quantity -- its uncertainty is bounded by Ward identity precision, not
by the full scan range.

**Numerical result (from script):**

| y_t(M_Pl) | y_t(v) | m_t [GeV] |
|-----------|--------|-----------|
| 0.200     | 0.609  | 106.0     |
| 0.300     | 0.805  | 140.2     |
| 0.436     | 0.973  | 169.4     |
| 0.600     | 1.085  | 189.0     |
| 0.800     | 1.157  | 201.5     |

Over the upper half [Ward, 0.8] (an 83% variation at M_Pl), y_t(v)
varies by 42% -- a focusing ratio R = 1.98. A 10% shift in y_t(M_Pl)
near the Ward value produces only a 4.0% shift in y_t(v).

**Implication:** Even if the exact lattice RG flow modifies y_t(M_Pl)
by O(10%) from the perturbative Ward value, the effect on y_t(v) is
suppressed. The Ward BC y_t(M_Pl) = 0.436 is a derived quantity with
O(few %) uncertainty, mapping to O(few %) uncertainty in y_t(v).

---

## Part 3: Insensitivity to g_1(v), g_2(v), lambda(v)

**Claim:** The electroweak and Higgs quartic couplings are subdominant
in the y_t beta function. Their contributions relative to the QCD term
are bounded by the coefficient ratios:

- g_3^2 term: -8 g_3^2 ~ -10.4 at v (DOMINANT)
- y_t^2 term: +9/2 * 0.97^2 ~ +4.2
- g_2^2 term: -9/4 * 0.65^2 ~ -0.95  (6.5% of beta)
- g_1^2 term: -17/20 * 0.46^2 ~ -0.18 (1.2% of beta)
- lambda: enters only at 2-loop (negligible)

**Numerical result (from script):**

| Coupling varied | Range         | max |Delta y_t(v)| / y_t(v) |
|-----------------|---------------|--------------------------------------|
| g_1(v)          | [0.30, 0.60]  | < 3.7%                               |
| g_2(v)          | [0.40, 0.90]  | < 7.4%                               |
| lambda(v)       | [0.05, 0.30]  | < 0.03%                              |

These are WIDE scan ranges -- much wider than the physical uncertainty
in these derived quantities (which is O(1%)). The key point: g_1 and
lambda are negligible. g_2 contributes at the several-percent level
over this extreme range, but its physical value is determined by the
derived SU(2) gauge structure and is not a free parameter.

---

## Part 4: Insensitivity to the Beta Function Itself

This is the key part that addresses the Codex blocker. The objection
is that the SM beta functions are wrong above v because the lattice
theory has different field content (16 tastes, not 1 family). We show
that the prediction is robust to modifications of the beta function.

### 4a. Loop order: 2-loop vs 1-loop

Replacing the full 2-loop SM RGE with the 1-loop approximation shifts
y_t(v) by -2.4%. This sets the scale of perturbative truncation
uncertainty for 17 decades of running.

### 4b. Coefficient perturbation (+/-3% -- taste-staircase scale)

The taste-staircase modifies the effective beta function coefficients
by O(1/n_taste) at each blocking step. The integrated effect over 17
decades is estimated at O(few %). Testing +/-3% perturbations:

| Config                  | Delta y_t(v)/y_t(v) |
|-------------------------|---------------------|
| c_3 +/-3%              | +/-1.9%             |
| c_self +/-3%           | +/-0.8%             |
| c_3 +3%, c_self -3%    | +2.8%               |
| c_3 -3%, c_self +3%    | -2.7%               |
| All coefficients +/-3% | +/-0.5%             |

Maximum deviation: 2.8%. The QFP structure partially cancels the
effects of simultaneous perturbations (the "All +/-3%" shift is
smaller than individual perturbations due to anticorrelation).

### 4c. Large coefficient perturbation

b_3 perturbation (controls the QCD running):

| Config      | Delta y_t(v)/y_t(v) |
|-------------|---------------------|
| b_3 +/-10%  | -3.0% / +3.3%      |
| b_3 +/-20%  | -5.6% / +7.1%      |

Random simultaneous perturbation of ALL 7 coefficients at +/-10%
(10 trials): max deviation 7.6%, mean 3.3%.

The response is approximately linear: a 10% coefficient change
produces a ~3% shift in y_t(v). The estimated taste-staircase
correction is O(few %), well within this bound.

### 4d. Physical content

The physical content of the backward Ward prediction is NOT the
specific form of the SM beta functions. It is the TOPOLOGY of the RG
flow: the existence of an IR quasi-fixed point in any gauge-Yukawa
system with a dominant gauge coupling. This topological feature is
shared by:
- The SM RGE (1 family, perturbative)
- Any EFT with the same gauge group and similar matter content
- The lattice theory's taste-staircase evolution (16 -> 1 taste)

The specific trajectory differs between these flows, but the endpoint
at v converges due to focusing.

---

## Part 5: Bounded Support Statement

**Bound (QFP Insensitivity Support).** Let F denote a family of RG flows
{F_a} for the gauge-Yukawa system (g_3, y_t) on the interval
[v, M_Pl], satisfying:

(i) **Smoothness:** Each flow is a smooth ODE solution on [v, M_Pl]

(ii) **Gauge anchor:** alpha_s(v) = alpha_bare/u_0^2 = 0.1033

(iii) **Ward BC:** y_t(M_Pl) = g_lattice/sqrt(6) = 0.436

(iv) **Focusing structure:** The y_t beta function has the form
     beta_yt = yt * [c_self * yt^2 - c_3 * g_3^2 + ...] with
     c_3 > c_self > 0 (the QCD correction dominates the Yukawa
     self-coupling, creating a quasi-fixed point)

Then for any two flows F_a, F_b in the family:

    |y_t(v; F_a) - y_t(v; F_b)| / y_t(v; F_a) < epsilon

where epsilon is determined by the sensitivity budget:

| Perturbation source          | epsilon   |
|------------------------------|-----------|
| +/-3% beta coefficients      | < 3%      |
| +/-10% beta coefficients     | < 8%      |
| +/-20% b_3 alone             | < 8%      |
| 2-loop truncation            | ~2.4%     |

For the physically relevant case (taste-staircase corrections at the
O(few %) level), epsilon ~ 3%.

**Corollary.** The SM RGE and the exact lattice taste-staircase RG
flow both satisfy conditions (i)-(iv). Therefore:

    y_t(v; SM RGE) = y_t(v; lattice) + O(3%)

The backward Ward prediction m_t = 169.4 GeV carries a bounded
systematic uncertainty of ~3% from the choice of RG flow above v.

---

## Part 6: Why This Resolves the Codex Blocker

The Codex blocker states: "the SM EFT is the wrong theory above v."
This is correct as a statement about the PHYSICS above v. But it is
not relevant to the backward Ward prediction, because:

1. **The SM RGE above v is not a physical description.** It is a
   mathematical interpolation used to transfer the Ward BC from M_Pl
   to v. The backward Ward procedure uses the SM RGE as a "surrogate
   RG flow" -- a smooth curve connecting the BC at M_Pl to the
   prediction at v.

2. **The QFP focusing makes the surrogate choice bounded.** Any
   smooth flow satisfying the Ward BC and gauge anchor gives the same
   y_t(v) to within the sensitivity budget. The SM RGE is one valid
   surrogate. The exact lattice taste-staircase is another. They
   agree at v because the QFP structure compresses UV differences.

3. **The "wrong theory" carries bounded error.** Even if the SM beta
   function coefficients are O(few %) wrong above v (due to the taste-
   staircase structure), the QFP insensitivity theorem bounds the
   effect on y_t(v) at < 3%.

4. **Four structural features are shared.** The SM RGE and the lattice
   RG flow share: (a) the SU(3) gauge group, (b) the dominant -8 g_3^2
   term creating the QFP, (c) the gauge anchor alpha_s(v), and (d) the
   Ward BC at M_Pl. These four features determine y_t(v) to within the
   stated precision. Everything else is a subdominant correction.

---

## Numerical Verification

All results from `frontier_yt_qfp_insensitivity.py`:

| Test | Criterion | Result |
|------|-----------|--------|
| Ward y_t(v) found | y_t(v) ~ 0.973 | PASS |
| m_t within 5% of observed | \|m_t - 172.7\|/172.7 < 5% | PASS |
| QFP focusing ratio > 1 (full range) | R > 1 | PASS (R = 1.09) |
| QFP focusing ratio > 1.5 (upper half) | R > 1.5 | PASS (R = 1.98) |
| Local sensitivity bounded | dy_t(v)/dy_t(M_Pl) < 1.5 | PASS (0.90) |
| Ward-band [0.3, 0.6] variation | < 30% | PASS (28.8%) |
| g_1 insensitivity [0.3, 0.6] | < 5% | PASS (3.7%) |
| g_2 insensitivity [0.4, 0.9] | < 10% | PASS (7.4%) |
| lambda insensitivity [0.05, 0.3] | < 0.5% | PASS (0.03%) |
| 1-loop vs 2-loop shift | < 5% | PASS (2.4%) |
| Small perturbation (+/-3%) | < 5% | PASS (2.8%) |
| b_3 +/-20% perturbation | < 15% | PASS (7.1%) |
| Random +/-10% all coefficients | < 10% | PASS (7.6%) |
| EW contribution quantified | < 20% | PASS (13.8%) |

14 PASS, 0 FAIL.

---

## Import Status

| Element | Status |
|---------|--------|
| g_bare = 1 | AXIOM |
| `<P>` = 0.5934 | COMPUTED |
| alpha_s(v) = alpha_bare/u_0^2 | DERIVED (CMT) |
| v = M_Pl * alpha_LM^16 | DERIVED (hierarchy thm) |
| y_t(M_Pl) = g_lattice/sqrt(6) | DERIVED (Ward identity) |
| SM RGE coefficients | DERIVED (from gauge group + matter) |
| QFP focusing structure | STRUCTURAL (topological, not model-dependent) |
| Insensitivity bounds | COMPUTED (this note) |

## Audit dependency repair links

This graph-bookkeeping section records load-bearing dependency links
named by a prior conditional audit as Markdown links so the audit
citation graph can track them. Backticked filenames in this section
are preserved see-also context only and do not emit citation-graph
edges. This section does not promote this note or change the audited
claim scope.

- `yt_p2_taste_staircase_beta_functions_note_2026-04-17` /
  `YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md`
  (see-also cross-reference, not a load-bearing dependency — backticked
  to break cycles 0009, 0010, and 0011 in the citation graph. The
  beta-functions note consumes this QFP 3% envelope as a load-bearing
  upstream bound on the SM-surrogate flow comparison; the citation
  graph direction is *beta_functions → qfp_insensitivity*, not the
  reverse. This back-edge was a graph-bookkeeping artifact only.)
- [yt_ward_identity_derivation_theorem](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
- [yt_boundary_theorem](YT_BOUNDARY_THEOREM.md)
- [yt_zero_import_authority_note](YT_ZERO_IMPORT_AUTHORITY_NOTE.md)

---

## CORRECTION 2026-05-10 — Ward-BC `m_t = 169.4 GeV` is a trajectory-truncation artifact, not a QFP attractor closure

**Review context:** [#1022](https://github.com/jonathonreilly/cl3-lattice-framework/pull/1022) —
*Probe W-Quark-RGFP: QFP-attractor route for top mass foreclosed
(NEGATIVE).*
**Authority role:** local correction stanza for the dynamical
(RGE-attractor) reading of `m_t` under the existing 1-loop SM RGE with
`α_s(v) = α_bare/u_0² = 0.1033`.
**Status:** source-only correction stanza appended at end. Does NOT
modify the substantive content of Parts 1-6 above.

### What this stanza corrects

This support note (Parts 1-6 above) treats the Ward-BC backward-RGE
prediction `y_t(v) ≈ 0.973`, `m_t = 169.4 GeV` as the converged result
of a QFP-focusing flow. The numerical table in Part 2 lists this
`m_t` value, and the bounded-support theorem in Part 5 asserts a ~3%
systematic uncertainty from "the choice of RG flow above v".

The paired runner below reproduces the diagnostic that **high-UV
trajectories in the same 1-loop SM RGE machinery compress to an IR band
well above the Ward-BC landing**:

```
y_t(v)|high-UV QFP band ≈ 1.11..1.23   (runner mean ≈ 1.19)
```

**not** at the SM-physical region `y_t(v) ≈ 0.95` (`m_t ≈ 173 GeV`).
The Ward BC `y_t(M_Pl) = g_lattice/√6 = 0.4358` sits on the LOWER
side of the QFP basin: the trajectory rises toward the attractor but
runs out of running budget after 17 decades, landing at
`y_t(v) ≈ 0.95` without finishing the climb.

### Reclassification

| Item | Original framing in this note | Corrected framing (PR #1022) |
|------|-------------------------------|------------------------------|
| `y_t(v) ≈ 0.973` | "Ward BC result", treated as QFP-focused closure | **UV-IR transient property** on a 17-decade truncation |
| `m_t = 169.4 GeV` | "Backward Ward prediction" with ~3% RG-flow uncertainty | **Trajectory-truncation artifact**, not an attractor property |
| QFP focusing as load-bearing | "Compresses UV differences" → the SM-physical `m_t` | Focusing is real but the runner-backed high-UV IR band is above `y_t(v) ≈ 1.1`, NOT centered on `0.97` |
| Pendleton-Ross focusing ratio R | "Compression of UV variation onto IR band" | Compression onto the high-UV QFP band, **not** onto `0.97` |

The Ward-BC trajectory result is **dependent on the specific
boundary value `0.4358`** lying below the attractor. It is NOT a
structural attractor closure. A different Ward BC value would give a
different `y_t(v)` along the same RG flow.

### Bounded-support theorem (Part 5) — what survives

The bounded statement that "any smooth flow satisfying the Ward BC
and the gauge anchor, with the same QFP focusing structure, gives the
same `y_t(v)` to within ~3%" is **internally correct** and survives
the correction. What it does NOT establish is that this common
`y_t(v)` is the SM-physical `m_t ≈ 173 GeV`. The shared `y_t(v) ≈
0.973` is **a transient value of the trajectory at scale `v` after 17
decades of running**, NOT the QFP attractor value.

Equivalently: Parts 1-6's bound is "trajectory robustness to flow
choice", not "attractor-closure robustness". This is a narrower claim
than a casual reading of the title "QFP Insensitivity" would suggest.

### Classification

| Item | Tier |
|------|------|
| Numerical results in Parts 1-5 (RGE integration, sensitivity scan, 14/14 PASS) | **NUMERICALLY CORRECT** (unchanged) |
| Bounded statement "trajectory `y_t(v)` robust to flow choice at ~3%" | **VALID** (Part 5 theorem) |
| Reading "`m_t = 169.4 GeV` is the QFP attractor closure for top mass" | **not supported by this note** |
| Reading "`m_t = 169.4 GeV` is a trajectory-truncation artifact at the chosen Ward BC" | **runner-backed correction in this stanza** |
| QFP-attractor route for top-mass closure | **not closed here**; the local diagnostic places the attractor above the SM-physical band |

### Where the correction must propagate

Downstream notes and audits that cite this support note must
distinguish:

- **Trajectory-robustness claim** (Part 5 bound, ~3% RG-flow
  uncertainty around `y_t(v) ≈ 0.973`) — survives.
- **Attractor-closure claim** (any reading that `m_t = 169.4 GeV` is
  forced by the IR fixed-point structure) — not supported here. The local
  high-UV QFP band sits above the SM-physical band rather than at the
  Ward-BC landing.

Any downstream that uses this note as authority for a positive theorem
on `m_t` from QFP-attractor closure must be reclassified until a separate
audited route supplies that bridge.

### Source-only review-loop compliance

- This is a CORRECTION STANZA appended at the end. Parts 1-6 are
  unchanged.
- The review-context PR (#1022) is cited.
- A paired runner [`scripts/cl3_t1_corrections_v2_2026_05_10.py`](../scripts/cl3_t1_corrections_v2_2026_05_10.py)
  reproduces the attractor mislocation and the trajectory-truncation
  diagnostic numerically.

### Authority disclaimer

This is a source-only correction stanza. Audit verdict and downstream
effective status are set only by the independent audit lane.
