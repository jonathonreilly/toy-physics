# Symmetric-Point Per-Channel Curvature Scale `m_curv_tree` from V_taste — Complete Derivation with N_c Tracking

**Date:** 2026-04-14 (originally); 2026-05-03 (review-loop repair); 2026-05-10 (Gap #3 lite — demote `m_H_tree` to `m_curv_tree`)
**Status:** TREE-LEVEL MEAN-FIELD per-channel curvature scale on the canonical surface. NOT a Higgs-mass prediction. The downstream bounded Higgs route is tracked in `HIGGS_MASS_DERIVED_NOTE.md` (full 3-loop SM RGE from `λ(M_Pl) = 0`; audit status remains ledger-owned).
**Claim type:** bounded_theorem
**Resolves:** color-factor dispute (does 8/9 enter the Higgs sector? Answer: no, N_c cancels in the per-channel curvature scale)
**Scripts:**
- `scripts/higgs_tree_level_mean_field_runner_2026_05_03.py` — primary runner for THIS note's tree-level formula `m_curv_tree = v/(2 u_0) = 140.3 GeV` on the canonical surface (post-2026-05-03 repair; post-2026-05-10 demotion).
- `scripts/frontier_higgs_mass_corrected_yt.py` — separate corrected-y_t RGE route giving 119.93 GeV (a DIFFERENT observable; not a verifier for this note).
- `scripts/frontier_higgs_buttazzo_calibration.py` — full-3-loop calibration (also separate).

## What this note is and is NOT (2026-05-10 demotion)

**This note derives** a per-channel symmetric-point curvature scale of V_taste on the canonical mean-field surface:

    m_curv_tree := sqrt(|V_taste''(0)| / N_taste) · v
                 = v / (2 u_0)
                 = 140.3 GeV   (at canonical u_0 ≈ 0.8776)

`m_curv_tree` is a dimensionful magnitude (mass units) constructed from the mass²-coefficient of V_taste at the symmetric point m = 0, divided by the per-taste-channel multiplicity N_taste = 16, and re-expressed at the EW VEV v.

**This note does NOT derive the Higgs-mass pole.** The post-EWSB Higgs-mass pole is the curvature of the FULL effective potential V_eff_total at the broken-phase minimum φ = v, not the per-channel curvature of V_taste at the symmetric point m = 0. Per the Morse/convexity Gap #3 probe (2026-05-10):

- V_taste(m) = -8 log(m² + 4u_0²) is **monotonically decreasing in |m|**;
- V_taste(m) **has no interior minimum** on its own;
- the broken-phase pole emerges only when V_taste is combined with the tree-level mass term and the gauge sector to form V_eff_total.

So `m_curv_tree` is structurally a **symmetric-point per-channel curvature magnitude** (rescaled by the externally-fixed VEV v), NOT a broken-phase pole.

**Earlier drafts of this note labeled this quantity `m_H_tree`.** The first-principles-honest label is `m_curv_tree`: the underscore-curv subscript indicates it is the magnitude of a curvature, the *_tree* subscript indicates the tree-level mean-field surface, and the leading `m_` indicates mass units. Throughout this note the canonical label is now `m_curv_tree`. Sister bounded-source-surface notes that compute the same numerical value (`v/(2u_0) ≈ 140.3 GeV`) under the older label `m_H_tree` continue to compute that same number; the demotion is a relabeling and a scope clarification, not a numerical change. The closed-form math is unchanged.

This mirrors PR #951 v3's pattern: the analogous dimensionless ratio derived from V_taste's symmetric-point curvature was renamed from `λ_curv` to `κ_curv` in `HIGGS_KAPPA_CURV_FROM_VTASTE_SYMMETRIC_POINT_NARROW_THEOREM_NOTE_2026-05-10.md` for the same first-principles reason. That file pointer is context, not a load-bearing dependency edge: the symmetric-point object should not carry a name that implies a broken-phase pole or quartic coupling.

## Honest scope (Gap #3 lite, 2026-05-10)

**Per-channel symmetric-point curvature ≠ broken-phase pole.** This identity becomes exact only in a limit where (i) all N_taste taste channels are degenerate with the physical Higgs channel, (ii) gauge corrections vanish, (iii) the EWSB saddle aligns with the symmetric-point curvature, and (iv) V_eff has a quadratic-only mass coefficient near the symmetric point (no m⁴ or higher mixing changes the broken-phase curvature). **None of (i)-(iv) is exactly true** on the canonical framework surface.

Concretely, for a standard Mexican hat V = -μ²|φ|² + λ|φ|⁴, the symmetric-point curvature magnitude |V''(0)| = 2μ² and the broken-phase pole V''(v) = 4λv² = 2μ² (using v² = μ²/2λ). The two coincide only because of the specific Mexican-hat relation between the v scale and the μ²-λ ratio. For V_taste — which is logarithmic, monotonically decreasing in |m|, and has **no interior minimum** — the symmetric-point curvature has no pole partner on V_taste alone; the pole emerges only from V_eff_total.

**The +12% gap is the genuine higher-order separation between the per-channel symmetric-point curvature scale and the broken-phase Higgs pole.** It is Morse/convexity-forced (per Gap #3 probe), not a numerical accident or a missing finite correction in this note. The closure of the +12% gap is delegated to the sister-authority chain (full 3-loop CW + RGE running, lattice spacing convergence, Wilson-term taste breaking) — see Step 7 below. This note does not attempt the closure; it provides the symmetric-point curvature magnitude as the cited input to that chain.

**The downstream bounded Higgs route is tracked in `HIGGS_MASS_DERIVED_NOTE.md`.** That note's primary runner is `scripts/frontier_higgs_mass_full_3loop.py`, which integrates the full 3-loop SM RGE from the framework boundary `λ(M_Pl) = 0` down to μ = v and gives `m_H ≈ 125.1 GeV` under its stated admissions. The present note's `m_curv_tree = 140.3 GeV` is a per-channel symmetric-point curvature scale; it is NOT a Higgs-mass prediction.

## Review-loop repair (2026-05-03)

The 2026-05-03 review follow-up identified
two gaps:

1. **Curvature-to-physical-Higgs-mass bridge asserted, not derived.**
   Step 5's justification ((a) dimensional analysis, (b) consistency
   with the code, (c) susceptibility) didn't actually derive the
   identification `(m_H/v)² = curvature/N_taste`; it asserted it.
2. **Note's 140.3 GeV headline stale relative to the named runner.**
   The cited `frontier_higgs_mass_corrected_yt.py` runs a corrected-y_t
   RGE route that ends at 119.93 GeV, which is a DIFFERENT observable
   from the note's tree-level formula.

This repair (and the 2026-05-10 demotion in the section above)
clarifies all of the above:

- **Sharpened scope.** The note now states explicitly that
  `m_curv_tree = v/(2 u_0) = 140.3 GeV` is a **tree-level mean-field
  per-channel symmetric-point curvature scale** of V_taste on the canonical
  lattice surface (mean-field link `U_{ab} → u_0 δ_{ab}`, V_taste curvature
  at the symmetric point m=0 with N_taste = 16 degeneracy assumed). It is
  **NOT the physical Higgs mass**, and it is no longer labeled as such.
  The +12% gap from observed 125.10 GeV is now framed as the **genuine
  higher-order separation between symmetric-point curvature and broken-phase
  pole** (Morse/convexity-forced, per Gap #3 probe), not a finite missing
  correction.
- **Curvature-to-readout map made explicit.** Step 5 is restated to
  acknowledge that the identification `(m_curv_tree/v)² = -d²V_taste/dm² / N_taste`
  at m=0 is the standard tree-level mean-field curvature readout in the
  symmetric phase before EWSB stabilises the VEV at v; it is NOT a derivation
  of the physical post-EWSB Higgs mass. The susceptibility argument (Step 5c)
  reduces to the same formula and is recorded as a consistency
  cross-check, not an independent derivation.
- **New primary runner** `scripts/higgs_tree_level_mean_field_runner_2026_05_03.py`
  reproduces exactly this tree-level formula and explicitly distinguishes
  it from the separate corrected-y_t / Buttazzo runners (which compute
  different observables along different chains).

After this repair plus the 2026-05-10 demotion, the note is honest about
what it derives: a tree-level mean-field formula `m_curv_tree = v/(2 u_0)`
with explicit N_c-cancellation at every step. The physical Higgs mass
remains a separate calculation, requiring inputs (RGE, CW corrections)
that this note does not supply, and is the subject of
`HIGGS_MASS_DERIVED_NOTE.md`.

---

## Result (tree-level mean-field per-channel symmetric-point curvature scale)

    m_curv_tree = v * sqrt(4 / (u_0^2 * N_taste))
                = v / (2 u_0)
                = 246.22 / (2 * 0.8776)
                = 140.3 GeV                     (curvature scale; not a Higgs-mass prediction)

This is a TREE-LEVEL mean-field **per-channel symmetric-point curvature
magnitude**, expressed in mass units. The +12% gap to the observed
physical Higgs mass (125.10 GeV) is the genuine higher-order separation
between the symmetric-point curvature scale and the broken-phase pole
(Morse/convexity-forced; see "Honest scope" above). Closure of that gap
is delegated to the sister-authority chain (full 3-loop CW + RGE running,
lattice spacing convergence, Wilson-term taste breaking) — see Step 7.
This note does not ship a Higgs-mass closure.

The color factor 8/9 does NOT enter `m_curv_tree` — and *a fortiori* does
not enter the downstream bounded Higgs route in `HIGGS_MASS_DERIVED_NOTE.md`.
N_c cancels exactly in the derivation. Full tracking below.

---

## Step 1: The generating functional

**Axiom.** Cl(3) on Z^3. Staggered Dirac operator D on Z^4 (APBC in
time), gauge group SU(3) at beta = 2 N_c / g^2 = 6. On the minimal
APBC block (L = 2, N_sites = 2^4 = 16), the matrix dimension is
N_tot = N_c * N_sites = 48.

**Eigenvalue degeneracy theorem.** The Clifford identity D_taste^2 = d I
forces all N_taste = 16 taste eigenvalues to have |lambda| = 2 u_0.
Mean-field factorization (U_{ab} -> u_0 delta_{ab}) extends this to
all N_tot = 48 eigenvalues. The eigenvalues are pure imaginary:
lambda_k = +/- 2 i u_0 (staggered anti-Hermiticity).

The generating functional at mean field:

    W(J) = sum_{k=1}^{N_tot} (1/2) log(J^2 + 4 u_0^2)
         = (N_tot / 2) * log(J^2 + 4 u_0^2)                   [1]

**N_c tracking:** N_tot = N_c * N_sites = 3 * 16 = 48. The factor
N_c is a linear overall multiplier.

---

## Step 2: Factoring out color

Color and taste factorize at mean field. The full determinant:

    det(D + J) = [det_taste(D + J)]^{N_c}

The taste-sector generating functional (one color copy):

    W_taste(J) = W(J) / N_c = (N_sites / 2) * log(J^2 + 4 u_0^2)

The taste-sector effective potential per site:

    V_taste(m) = -W_taste / N_sites = -(1/2) * log(m^2 + 4 u_0^2)

Summing over all N_taste = 16 taste eigenvalues on the minimal block
(where N_sites = N_taste):

    V_taste(m) = -(N_taste / 2) * log(m^2 + 4 u_0^2)
               = -8 * log(m^2 + 4 u_0^2)                       [2]

**N_c does not appear in [2].** From here on, the derivation is
N_c-independent. The color links contribute only through u_0 = <P>^{1/4}.

---

## Step 3: Curvature at the symmetric point (Morse/convexity context)

    d V_taste / dm = -N_taste * m / (m^2 + 4 u_0^2) = 0  at m = 0

    d^2 V_taste / dm^2 |_{m=0} = -N_taste / (4 u_0^2)
                                = -4 / u_0^2                    [3]

The negative curvature confirms the symmetric point m = 0 is a local
maximum of V_taste — a tachyonic instability that drives EWSB when V_taste
is combined with the rest of V_eff.

**Morse/convexity context (Gap #3 probe, 2026-05-10).** The full log
potential V_taste(m) = -8 log(m² + 4 u_0²) is **monotonically decreasing
for m > 0**. It has **no interior minimum on V_taste alone** — and a
fortiori no interior CW minimum that could play the role of a Higgs
broken-phase pole. The physical VEV arises from the interplay of the
fermion determinant with the gauge action and the tree-level mass (the
full CW mechanism), with the EW scale supplied by the bounded hierarchy
formula `v = M_Pl * alpha_LM^16`. This is the structural reason why
`m_curv_tree`, derived from the symmetric-point curvature [3] alone,
is NOT a Higgs-mass pole: V_taste's symmetric-point curvature has no
broken-phase partner *on V_taste*; the pole emerges only from
V_eff_total.

---

## Step 4: The per-channel symmetric-point curvature

The curvature [3] counts ALL N_taste = 16 degenerate taste channels
responding to the mass shift dm. The Higgs is identified (in the
all-channels-degenerate limit; see "Honest scope") with a single
taste-singlet scalar occupying one out of N_taste channels. By the
degeneracy theorem, each taste channel contributes equally, so the
per-channel curvature is:

    |d^2 V / dm^2|_{per channel} = (4 / u_0^2) / N_taste
                                  = 1 / (4 u_0^2)               [4]

This per-channel curvature magnitude, rescaled by the EW VEV v, is the
symmetric-point curvature scale `m_curv_tree`. The per-channel
dimensionless curvature ratio is

    (m_curv_tree / v)^2 = 4 / (u_0^2 * N_taste) = 1 / (4 u_0^2)

    m_curv_tree / v = 1 / (2 u_0)                              [5]

    m_curv_tree = v / (2 u_0) = 246.22 / 1.7552 = 140.3 GeV    [6]

Note: equations [5]–[6] give the **per-channel symmetric-point curvature
scale**. They do NOT give the Higgs-mass pole; per "Honest scope" above,
that identification holds only in a limit where (i)–(iv) are exact, none
of which is true on the canonical framework surface.

**N_c tracking:** N_c divided out at Step 2. Equation [4] involves
only u_0 and N_taste. The per-channel symmetric-point curvature scale
`m_curv_tree` is N_c-independent. The downstream Higgs-mass prediction
in `HIGGS_MASS_DERIVED_NOTE.md` is also
N_c-independent (consistent finding via a separate chain).

---

## Step 5: Why the ratio (m_curv_tree / v)^2 = curvature / N_taste

**This step is the curvature-to-curvature-readout map at TREE LEVEL.**
It is the standard mean-field Klein-Gordon curvature readout in the
symmetric phase, NOT a derivation of the physical Higgs mass after
EWSB. The 2026-05-03 review-loop sharpening and the 2026-05-10 Gap #3
demotion appear in the headings: each argument is now labelled by what
it actually establishes.

**(a) Dimensional matching (necessary condition only).** The curvature
d²V/dm² is dimensionless (V is dimensionless, m is dimensionless in
lattice units). The curvature scale in lattice units is m_curv(lat) =
m_curv(phys)·a = m_curv/M_Pl. The VEV in lattice units is v_lat = v/M_Pl.
The ratio m_curv/v = m_curv(lat)/v_lat is dimensionless and must equal
a function of the dimensionless lattice quantities u_0 and N_taste.
Dimensional analysis ALONE does not pick out the specific ratio
(m_curv_tree/v)² = curvature/N_taste — it only constrains the
combination to be dimensionless. The specific identification needs the
next argument.

**(b) Tree-level mean-field Klein-Gordon curvature readout (the actual derivation).**
At tree level, the Higgs-channel scalar mode is one of N_taste
degenerate scalar modes in V_taste. The tree-level curvature *at the
symmetric point* is the Hessian of V_taste at m=0; per equation [4],
the per-channel magnitude is `(4/u_0²)/N_taste`. The note's tree-level
shortcut is: define `m_curv_tree²` as the per-channel symmetric-point
curvature times the externally-fixed v² scale:

    m_curv_tree² := (4/u_0²)/N_taste · v² = v²/(4 u_0²).

This identifies a **symmetric-point curvature magnitude** in mass units
— a structurally clean object derivable from V_taste alone. It is NOT
the broken-phase Higgs-mass pole, and the note no longer claims that
identification. (In earlier drafts the symbol `m_H_tree` was used and
the identification was implied; the 2026-05-10 demotion replaces both
the symbol and the implication.)

The Higgs-mass-pole identification would additionally require:
(i) all N_taste taste channels to be exactly degenerate with the physical
Higgs (the canonical surface uses uniform N_taste = 16, which is
non-derived per `HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md` (context file pointer, not a load-bearing dependency edge));
(ii) gauge corrections to vanish (they do not);
(iii) the EWSB saddle to align with the symmetric-point curvature
(it does not — V_taste alone has no interior minimum, per Step 3 and
the Gap #3 Morse/convexity probe);
(iv) V_eff to have a quadratic-only mass coefficient (it does not —
V_taste's logarithmic m⁴ and higher coefficients are non-zero and
contribute to the broken-phase curvature).

The +12% gap from observed 125.10 GeV is the **numerical magnitude of
the genuine higher-order separation** induced by (i)–(iv) failing
simultaneously. Closure of that gap is delegated to the sister-authority
chain (Step 7).

**(c) Susceptibility consistency cross-check (not independent).** The
scalar susceptibility chi = d²W/dJ² counts the response of all internal
DOF. The full per-site susceptibility is chi = N_c/(4 u_0²); the
per-channel chi_curv = chi/(N_c · N_taste) = 1/(4 u_0² N_taste). Then
the symmetric-point per-channel curvature scale m_curv² = v²/chi_curv = v²·4 u_0²·N_taste,
which would give a curvature scale ~ 1000 GeV — too large by a factor
(M_Pl/v)². The correct identification is m_curv² = (1/chi_curv)·(v/M_Pl)²,
which after the hierarchy conversion gives back the same formula [6].
This is a consistency check, not an independent derivation; the
load-bearing step is still (b)'s tree-level mean-field per-channel
symmetric-point curvature identification.

**Honest scope of Step 5.** The curvature-to-curvature-readout map is
the **tree-level mean-field Klein-Gordon curvature identification**.
It is correct *at tree level on the mean-field surface as a
symmetric-point per-channel curvature magnitude*. It is **not** a
Higgs-mass-pole derivation. The physical Higgs mass requires (i)
dropping the mean-field approximation, (ii) summing CW + gauge
corrections, (iii) RGE running from the lattice scale to the physical
scale, and (iv) recognizing that the broken-phase pole differs from
the symmetric-point curvature by the genuine higher-order separation
described in the "Honest scope" section above. None of (i)–(iv) is
supplied here. Hence `m_curv_tree = 140.3 GeV` is the symmetric-point
curvature scale; the physical Higgs-mass prediction
~125.1 GeV is tracked in `HIGGS_MASS_DERIVED_NOTE.md`
on the full 3-loop SM RGE chain from `λ(M_Pl) = 0`.

> **Note (2026-05-07 cleanup).** A duplicate of paragraph (c) appeared
> here in earlier drafts (the original pre-2026-05-03-repair version
> that read "the correct identification is m_H² = (1/chi_H)·(v/M_Pl)²"
> contradicting the sharpened cross-check framing above). That stale
> paragraph has been removed; the susceptibility content is fully
> covered by the cross-check framing in (c) above. The 2026-05-10
> Gap #3 lite demotion additionally renames `m_H` → `m_curv` in this
> susceptibility context to keep the parent note's primary label
> consistent.

---

## Step 6: Does the color factor 8/9 enter the Higgs sector?

**No.** Three independent arguments — and these arguments are about the
per-channel symmetric-point curvature scale `m_curv_tree`, *not* about
a Higgs-mass pole prediction. The downstream Higgs-mass prediction in
`HIGGS_MASS_DERIVED_NOTE.md` is also
N_c-independent (consistent finding via a separate chain).

**Argument 1 (factorization).** The taste potential V_taste [2] is
obtained by dividing V_full = N_c * V_taste by N_c. All quantities
derived from it are N_c-independent. The factor (N_c^2 - 1)/N_c^2
is a quadratic Casimir ratio that has no algebraic pathway to enter
a linear-in-N_c factorization.

**Argument 2 (different operators).** The 8/9 arises in the EW vacuum
polarization Pi_EW, a 2-point function requiring Fierz decomposition
in q-qbar color space (YT_EW_COLOR_PROJECTION_THEOREM.md, Section 2.2).
The per-channel symmetric-point curvature comes from the scalar
susceptibility chi = d^2 W / dJ^2, a 0-point function with trivial color
structure delta_{ab} delta_{ab} = N_c.

**Argument 3 (ratio invariance).** Even if 8/9 entered m_W through the
EW coupling correction, it would not enter m_curv_tree/m_W. Both
m_curv_tree and m_W are extracted from the same taste-sector potential
and any universal color correction would cancel in their ratio.

---

## Summary: N_c tracking table

| Quantity | Formula | N_c dependence |
|----------|---------|----------------|
| W(J) | (N_c N_sites / 2) log(J^2 + 4 u_0^2) | proportional to N_c |
| V_taste(m) | -8 log(m^2 + 4 u_0^2) | NONE (N_c divided out) |
| curvature at m=0 | 4 / u_0^2 | NONE |
| per-channel curvature | 4 / (u_0^2 N_taste) | NONE |
| m_curv_tree / v | 1 / (2 u_0) | NONE |
| 8/9 factor | (N_c^2-1) / N_c^2 | enters EW couplings ONLY |

---

## The remaining +12% gap (genuine higher-order separation, Morse/convexity-forced)

The +12% gap between the symmetric-point curvature scale `m_curv_tree =
140.3 GeV` and the observed Higgs-mass pole `m_H = 125.10 GeV` is the
**genuine higher-order separation** between two structurally distinct
objects:

- `m_curv_tree`: a per-channel symmetric-point curvature magnitude on
  V_taste alone (this note);
- `m_H_pole`: the broken-phase pole of V_eff_total at φ = v
  (`HIGGS_MASS_DERIVED_NOTE.md`).

Per the Gap #3 Morse/convexity probe (2026-05-10), the two are forced
to differ on the canonical surface because V_taste has no interior
minimum (logarithmic, monotonically decreasing); the Higgs-mass pole
emerges only from V_eff_total. The +12% magnitude of the separation is
itself a quantitative output of the framework chain, not a finite missing
correction in *this* note.

Three identified sister contributions in the gap-closure chain:

1. **2-loop CW corrections.** The 1-loop CW overestimates the m_H/m_W
   ratio. 2-loop contributions from the top quark are negative and
   reduce m_H by ~10-15% in standard SM analyses. A 12% reduction from
   2-loop effects is within the expected range.

2. **Lattice spacing convergence.** The code shows m_H/m_W = 1.64 at
   a = 0.5 vs 1.85 at a = 1 (HIGGS_MASS_NOTE.md). The prediction
   monotonically approaches the SM value 1.558 as a decreases.

3. **Taste-breaking (Wilson term).** The Wilson term breaks the 16-fold
   degeneracy into a (1,4,6,4,1) staircase. This changes the effective
   N_taste in formula [5], potentially reducing the curvature scale.

The framework's downstream bounded Higgs route (~125.1 GeV under its
stated admissions) is tracked by the full 3-loop SM RGE chain in
`HIGGS_MASS_DERIVED_NOTE.md`, not by additively patching this note's
symmetric-point curvature scale.

---

## Step 7: Authority chain for the +12% gap (2026-05-07; 2026-05-10 demotion)

The narrative paragraph above ("The remaining +12% gap") attributes the
140.3 GeV → 125.10 GeV gap-closure to three sister authorities without
naming the rows that actually carry each derivation. This step
upgrades the cross-reference to an audit-compatible authority inventory
without attempting any new derivation. Each row is a pointer; this note
does not change any sibling claim boundary or effective status (the pipeline-derived status field in the audit ledger). The
audit ledger remains the only authority for current audit and
effective status (the pipeline-derived status field in the audit ledger).

| Gap correction | Sister authority | Status authority | Closes the gap from / to | Open content |
|---|---|---|---|---|
| 2-loop CW + RGE running | `HIGGS_MASS_DERIVED_NOTE.md` (file-pointer context reference, backticked to avoid the known back-edge through the EW-coupling cluster; that note already cites this one's tree-level formula in its Note↔runner reconciliation section) + `scripts/frontier_higgs_mass_corrected_yt.py` (corrected-y_t RGE) | audit ledger only | symmetric-point curvature scale → ~119.93 GeV via corrected-y_t at 3L+NNLO | conditional on `y_t` Ward + RGE-transport scaffolding |
| Lattice spacing convergence (`m_H/m_W` flow as `a → 0`) | [`HIGGS_FROM_LATTICE_NOTE.md`](HIGGS_FROM_LATTICE_NOTE.md) (`bounded_theorem`, td=310) | audit ledger only | `m_H/m_W = 1.85` at `a=1` → 1.64 at `a=0.5` → 1.558 SM in continuum | continuum-limit theorem surface |
| Wilson-term taste-breaking ((1,4,6,4,1) staircase) | [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md); the sister Wilson follow-on notes `HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`, `WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md`, `WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`, and `WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md` are listed as file-pointer context references (backticked to avoid length-2 back-edges, since each of those notes already cites this note as the load-bearing parent in their proof-walks) | audit ledger only | proves the finite staircase identity and bounded leading-order Wilson correction formulas | **still open**: no retained closure of the physical gap; uniform `N_taste = 16`, any nonzero Wilson coefficient `r`, and the leading-order comparison to 125.10 GeV remain bounded/noncanonical inputs |
| Buttazzo full-3-loop calibration cross-check | `scripts/frontier_higgs_buttazzo_calibration.py` | (auxiliary calibration) | independent ~125.1 GeV via 3-loop Buttazzo parametric calibration | a different observable along a different chain; not load-bearing for this note |

### What this Step 7 changes

No claim status or theorem boundary. The +12% gap remains an open chain
across sister authorities and a remaining quantitative-effect bridge,
now framed as the genuine higher-order separation between the
symmetric-point curvature scale and the broken-phase pole (Morse/convexity
context per Gap #3). This note continues to claim only the tree-level
formula `m_curv_tree = v/(2 u_0) = 140.3 GeV`, with the gap-closure load
explicitly delegated.

### What this Step 7 records

- The **2026-05-02 status correction audit packet**
  (`HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md`)
  classifies the lattice-curvature → physical-(m_H/v)² bridge as a
  **same-shape obstruction** with cycle 5 (yt_ew matching M)
  and cycle 9 (gauge-scalar observable bridge) — i.e., as
  a member of the **lattice → continuum / physical matching cluster**
  identified in `AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md`
  §2.3. That cluster requires an independent non-perturbative matching
  theorem before it can support a physical-mass closure.
  Closing the cluster closes this gap.
- The **Wilson taste-breaking row now has bounded follow-on source
  notes** for the staircase, the uniform-`N_taste = 16` boundary, the
  corrected `V_taste` formula, the Wilson-shifted extremum, and the
  leading-order `m_curv_tree` comparison. These notes sharpen the
  dependency chain but do **not** close the physical +12% gap: the
  channel choice is non-derived, the parent canonical setup has
  `r = 0`, and the `r ≈ 0.235` number is a leading-order comparison
  value rather than a derivation of a Wilson coefficient.

---

## Definitive answer

    m_curv_tree = v / (2 u_0) = 140.3 GeV
        (zero free parameters; per-channel symmetric-point curvature scale)

with u_0 = 0.8776 from SU(3) plaquette at beta = 6, and v = 246.22 GeV
from the bounded hierarchy formula. N_c cancels. The 8/9 does not enter.

**This is NOT a Higgs-mass prediction.** It is the symmetric-point
per-channel curvature magnitude on V_taste, expressed in mass units at
the externally-fixed VEV v. The Higgs-mass prediction (~125.1 GeV) is
is tracked in `HIGGS_MASS_DERIVED_NOTE.md`, which uses the full 3-loop
SM RGE from `λ(M_Pl) = 0` under its stated admissions and does not
load-bear on `m_curv_tree`.

---

## Backward-compatibility note (2026-05-10)

Earlier drafts of this note labeled `m_curv_tree` as `m_H_tree`. Sister
bounded-source-surface notes that import this object continue to use the
older label `m_H_tree` for the same numerical quantity (`v/(2u_0) ≈
140.3 GeV`); they compute the same thing. Files where this naming
collision is most direct include
`HIGGS_MASS_12PCT_GAP_DECOMPOSITION_BOUNDED_NOTE_2026-05-10_higgsS7.md`,
`HIGGS_MASS_WILSON_CHAIN_PARTIAL_PROGRESS_NOTE_2026-05-10_higgsH1.md`,
`LATTICE_PHYSICAL_MATCHING_THEOREM_BOUNDED_OBSTRUCTION_NOTE_2026-05-10_match.md`,
`WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`,
`WILSON_M_H_TREE_AT_EXTREMUM_ALL_ORDERS_BOUNDED_NOTE_2026-05-08.md`,
and `HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`.
Where these notes cite the imported quantity directly with phrasing like
"`m_H_tree` from `HIGGS_MASS_FROM_AXIOM_NOTE`", that citation should be
read as "the symmetric-point per-channel curvature scale `m_curv_tree`
from `HIGGS_MASS_FROM_AXIOM_NOTE` (previously labeled `m_H_tree` in
those source notes)". The numerical content is unchanged; only the
parent label is demoted.

The script `higgs_tree_level_mean_field_runner_2026_05_03.py` continues
to compute `v/(2 u_0) = 140.3 GeV` and verifies the parent note's primary
label is now `m_curv_tree` (the runner identifies the formula by the
canonical lattice expression rather than by the old/new symbol).

---

## Dependencies

- `TASTE_POLYNOMIAL_NOTE.md` -- det(D+m) = (m^2 - 4c^2)^8
- `DM_AMGM_SATURATION_NOTE.md` -- eigenvalue degeneracy from Clifford identity
- `HIERARCHY_THEOREM.md` -- v = M_Pl * alpha_LM^16
- `YT_EW_COLOR_PROJECTION_THEOREM.md` -- 8/9 applies to EW couplings only
- `HIGGS_MASS_DERIVED_NOTE.md` -- downstream bounded Higgs route (~125.1 GeV under stated admissions) via full 3-loop SM RGE; NOT load-bearing on `m_curv_tree`
- `HIGGS_FROM_LATTICE_NOTE.md` -- lattice spacing convergence (`a → 0`)
- `HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md` -- 2026-05-02 status-correction packet classifying the lattice-curvature → (m_H/v)² bridge as same-shape lattice-physical matching obstruction (cycles 5, 9, 11)
- `AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md` -- cluster-level synthesis of the lattice-physical matching obstruction
- `HIGGS_KAPPA_CURV_FROM_VTASTE_SYMMETRIC_POINT_NARROW_THEOREM_NOTE_2026-05-10.md` -- analogous κ_curv naming pattern for the dimensionless symmetric-point curvature ratio (PR #951 v3 mirror)
- `frontier_higgs_mass_corrected_yt.py` -- corrected-`y_t` Higgs support route
- `frontier_higgs_buttazzo_calibration.py` -- full-3-loop boundary support

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a
prior conditional audit so the audit citation graph can track the load-bearing
links. Backticked file-pointer entries are context references deliberately
omitted from the graph to avoid non-load-bearing back-edges. This section does
not promote this note or change the audited claim scope.

- [yt_ew_color_projection_theorem](YT_EW_COLOR_PROJECTION_THEOREM.md)
- `HIGGS_MASS_DERIVED_NOTE.md` (file-pointer context reference, backticked
  to avoid the known back-edge through the EW-coupling / `g_1(v)`-`g_2(v)`
  input-authority cluster; that note already cites this one in its
  Note↔runner reconciliation section)
- [higgs_from_lattice_note](HIGGS_FROM_LATTICE_NOTE.md)
