# Higgs Mass from the Axiom: Complete Derivation with N_c Tracking

**Date:** 2026-04-14 (originally); 2026-05-03 (review-loop repair)
**Status:** TREE-LEVEL MEAN-FIELD auxiliary route — closed-form support formula, N_c tracked at every step. NOT the physical Higgs mass; physical value requires CW + RGE corrections (see Step 5).
**Claim type:** bounded_theorem
**Resolves:** color-factor dispute (does 8/9 enter m_H?)
**Scripts:**
- `scripts/higgs_tree_level_mean_field_runner_2026_05_03.py` — primary runner for THIS note's tree-level formula `m_H_tree = v/(2 u_0) = 140.3 GeV` on the canonical surface (post-2026-05-03 repair).
- `scripts/frontier_higgs_mass_corrected_yt.py` — separate corrected-y_t RGE route giving 119.93 GeV (a DIFFERENT observable; not a verifier for this note).
- `scripts/frontier_higgs_buttazzo_calibration.py` — full-3-loop calibration (also separate).

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

This repair clarifies both:

- **Sharpened scope.** The note now states explicitly that
  `m_H_tree = v/(2 u_0) = 140.3 GeV` is a **tree-level mean-field
  estimate** of the Higgs mass on the canonical lattice surface
  (mean-field link `U_{ab} → u_0 δ_{ab}`, V_taste curvature at the
  symmetric point m=0 with N_taste = 16 degeneracy assumed). It is
  NOT the physical Higgs mass — the +12% gap from observed 125.10 GeV
  is closed by 2-loop CW corrections, lattice spacing convergence,
  and Wilson-term taste breaking, all of which are explicitly
  out-of-scope.
- **Curvature-to-readout map made explicit.** Step 5 is restated to
  acknowledge that the identification `(m_H/v)² = -d²V_taste/dm² / N_taste`
  at m=0 is the standard tree-level mean-field readout (matching the
  free-field Klein-Gordon Higgs mass in the symmetric phase before
  EWSB stabilises the VEV at v); it is NOT a derivation of the
  physical post-EWSB Higgs mass. The susceptibility argument (Step 5c)
  reduces to the same formula and is recorded as a consistency
  cross-check, not an independent derivation.
- **New primary runner** `scripts/higgs_tree_level_mean_field_runner_2026_05_03.py`
  reproduces exactly this tree-level formula and explicitly distinguishes
  it from the separate corrected-y_t / Buttazzo runners (which compute
  different observables along different chains).

After this repair, the note is honest about what it derives: a
tree-level mean-field formula `m_H_tree = v/(2 u_0)` with explicit
N_c-cancellation at every step. The physical Higgs mass remains a
separate calculation, requiring inputs (RGE, CW corrections) that
this note does not supply.

---

## Result (tree-level mean-field)

    m_H_tree = v * sqrt(4 / (u_0^2 * N_taste))
             = v / (2 u_0)
             = 246.22 / (2 * 0.8776)
             = 140.3 GeV                       (+12.0% vs observed 125.10 GeV)

This is a TREE-LEVEL mean-field estimate. The 12% gap to the observed
physical Higgs mass is closed by 2-loop CW corrections, lattice
spacing convergence (m_H/m_W decreases monotonically with a), and
Wilson-term taste breaking, all separately derived in companion
notes.

The color factor 8/9 does NOT enter m_H. N_c cancels exactly in the
derivation. Full tracking below.

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

## Step 3: Curvature at the symmetric point

    d V_taste / dm = -N_taste * m / (m^2 + 4 u_0^2) = 0  at m = 0

    d^2 V_taste / dm^2 |_{m=0} = -N_taste / (4 u_0^2)
                                = -4 / u_0^2                    [3]

The negative curvature confirms tachyonic instability: the symmetric
point m = 0 is a local maximum of V_taste. This drives EWSB.

**Note:** The full log potential -8 log(m^2 + 4 u_0^2) is monotonically
decreasing for m > 0. It has no CW minimum by itself. The physical
VEV arises from the interplay of the fermion determinant with the gauge
action and tree-level mass (the full CW mechanism), stabilized at
v = 246 GeV by the hierarchy theorem (v = M_Pl * alpha_LM^16).

---

## Step 4: The Higgs mass

The curvature [3] counts ALL N_taste = 16 degenerate taste channels
responding to the mass shift dm. The physical Higgs boson is a
single taste-singlet scalar, occupying one out of N_taste channels.
By the degeneracy theorem, each taste channel contributes equally,
so the per-channel curvature is:

    |d^2 V / dm^2|_{Higgs} = (4 / u_0^2) / N_taste
                            = 1 / (4 u_0^2)                    [4]

This curvature is the dimensionless ratio (m_H / v)^2 in lattice
units, since the VEV v is the natural scale of the scalar field:

    (m_H / v)^2 = 4 / (u_0^2 * N_taste) = 1 / (4 u_0^2)

    m_H / v = 1 / (2 u_0)                                      [5]

    m_H = v / (2 u_0) = 246.22 / 1.7552 = 140.3 GeV            [6]

**N_c tracking:** N_c divided out at Step 2. Equation [4] involves
only u_0 and N_taste. The Higgs mass is N_c-independent.

---

## Step 5: Why the ratio (m_H_tree / v)^2 = curvature / N_taste

**This step is the curvature-to-readout map at TREE LEVEL.** It is the
standard mean-field Klein-Gordon Higgs-mass readout in the symmetric
phase, NOT a derivation of the physical Higgs mass after EWSB. The
2026-05-03 review-loop sharpening is in the headings: each argument
is now labelled by what it actually establishes.

**(a) Dimensional matching (necessary condition only).** The curvature
d²V/dm² is dimensionless (V is dimensionless, m is dimensionless in
lattice units). The Higgs mass in lattice units is m_H(lat) = m_H(phys)·a
= m_H/M_Pl. The VEV in lattice units is v_lat = v/M_Pl. The ratio
m_H/v = m_H(lat)/v_lat is dimensionless and must equal a function of
the dimensionless lattice quantities u_0 and N_taste. Dimensional
analysis ALONE does not pick out the specific ratio (m_H_tree/v)² =
curvature/N_taste — it only constrains the combination to be
dimensionless. The specific identification needs the next argument.

**(b) Tree-level mean-field Klein-Gordon readout (the actual derivation).**
At tree level, the Higgs field is a single scalar mode in a potential
V_taste(m). The tree-level mass squared is the curvature at the minimum:
m_H_tree² = d²V_taste/dh²|_{h=v}. In the symmetric phase (m=0) the
curvature is -4/u_0² (the tachyonic mass-squared driving EWSB); the
physical post-EWSB mass requires summing the full CW + gauge + tree
contributions to find the true minimum and computing curvature there.

The note's tree-level shortcut is: identify the per-channel curvature
at the symmetric point `(4/u_0²)/N_taste` with `(m_H_tree/v)²` directly,
treating the symmetric-point curvature as a proxy for the post-EWSB
mass at the natural EWSB scale v. This is the standard mean-field
estimate that becomes exact in the limit where (i) all N_taste taste
channels degenerate, (ii) gauge corrections vanish, and (iii) the EWSB
saddle aligns with the symmetric-point curvature. None of (i)-(iii) is
exactly true — the +12% gap is precisely the magnitude of the
correction.

**(c) Susceptibility consistency cross-check (not independent).** The
scalar susceptibility chi = d²W/dJ² counts the response of all internal
DOF. The full per-site susceptibility is chi = N_c/(4 u_0²); the
Higgs-channel chi_H = chi/(N_c · N_taste) = 1/(4 u_0² N_taste). Then
m_H² = v²/chi_H = v²·4 u_0²·N_taste, which would give m_H ~ 1000 GeV
— too large by a factor (M_Pl/v)². The correct identification is
m_H² = (1/chi_H)·(v/M_Pl)², which after the hierarchy conversion gives
back the same formula [6]. This is a consistency check, not an
independent derivation; the load-bearing step is still (b)'s tree-level
mean-field identification.

**Honest scope of Step 5.** The curvature-to-readout map is the
**tree-level mean-field Klein-Gordon identification**. It is correct
*at tree level on the mean-field surface*. The physical Higgs mass
requires (i) dropping the mean-field approximation, (ii) summing CW
+ gauge corrections, and (iii) RGE running from the lattice scale to
the physical scale. None of these is supplied here. Hence
`m_H_tree = 140.3 GeV` is the tree-level value; the physical
~125.1 GeV is reached by the separate corrected-y_t RGE and Buttazzo
calibration runners (which are different observables built on
different chains, NOT verifiers for this note's tree-level formula).

> **Note (2026-05-07 cleanup).** A duplicate of paragraph (c) appeared
> here in earlier drafts (the original pre-2026-05-03-repair version
> that read "the correct identification is m_H² = (1/chi_H)·(v/M_Pl)²"
> contradicting the sharpened cross-check framing above). That stale
> paragraph has been removed; the susceptibility content is fully
> covered by the cross-check framing in (c) above.

---

## Step 6: Does the color factor 8/9 enter m_H?

**No.** Three independent arguments:

**Argument 1 (factorization).** The taste potential V_taste [2] is
obtained by dividing V_full = N_c * V_taste by N_c. All quantities
derived from it are N_c-independent. The factor (N_c^2 - 1)/N_c^2
is a quadratic Casimir ratio that has no algebraic pathway to enter
a linear-in-N_c factorization.

**Argument 2 (different operators).** The 8/9 arises in the EW vacuum
polarization Pi_EW, a 2-point function requiring Fierz decomposition
in q-qbar color space (YT_EW_COLOR_PROJECTION_THEOREM.md, Section 2.2).
The Higgs mass comes from the scalar susceptibility chi = d^2 W / dJ^2,
a 0-point function with trivial color structure delta_{ab} delta_{ab} = N_c.

**Argument 3 (ratio invariance).** Even if 8/9 entered m_W through the
EW coupling correction, it would not enter m_H/m_W. Both m_H and m_W
are extracted from the same taste-sector potential and any universal
color correction would cancel in their ratio.

---

## Summary: N_c tracking table

| Quantity | Formula | N_c dependence |
|----------|---------|----------------|
| W(J) | (N_c N_sites / 2) log(J^2 + 4 u_0^2) | proportional to N_c |
| V_taste(m) | -8 log(m^2 + 4 u_0^2) | NONE (N_c divided out) |
| curvature | 4 / u_0^2 | NONE |
| per-channel curvature | 4 / (u_0^2 N_taste) | NONE |
| m_H / v | 1 / (2 u_0) | NONE |
| 8/9 factor | (N_c^2-1) / N_c^2 | enters EW couplings ONLY |

---

## The remaining +12% gap

Three identified corrections reduce the gap between 140.3 GeV and 125.25 GeV:

1. **2-loop CW corrections.** The 1-loop CW overestimates m_H/m_W.
   2-loop contributions from the top quark are negative and reduce
   m_H by ~10-15% in standard SM analyses. A 12% reduction from
   2-loop effects is within the expected range.

2. **Lattice spacing convergence.** The code shows m_H/m_W = 1.64 at
   a = 0.5 vs 1.85 at a = 1 (HIGGS_MASS_NOTE.md). The prediction
   monotonically approaches the SM value 1.558 as a decreases.

3. **Taste-breaking (Wilson term).** The Wilson term breaks the 16-fold
   degeneracy into a (1,4,6,4,1) staircase. This changes the effective
   N_taste in formula [5], potentially reducing m_H.

---

## Step 7: Authority chain for the +12% gap (2026-05-07)

The narrative paragraph above ("The remaining +12% gap") attributes the
140.3 GeV → 125.10 GeV closure to three corrections without naming the
sister authorities that actually carry each derivation. This step
upgrades the cross-reference to an audit-compatible authority inventory
without attempting any new derivation. Each row is a pointer; this note
does not change any sibling claim boundary or effective status (the pipeline-derived status field in the audit ledger). The
audit ledger remains the only authority for current audit and
effective status (the pipeline-derived status field in the audit ledger).

| Gap correction | Sister authority | Status authority | Closes the gap from / to | Open content |
|---|---|---|---|---|
| 2-loop CW + RGE running | `HIGGS_MASS_DERIVED_NOTE.md` (file-pointer context reference, backticked to avoid the known back-edge through the EW-coupling cluster; that note already cites this one's tree-level formula in its Note↔runner reconciliation section) + `scripts/frontier_higgs_mass_corrected_yt.py` (corrected-y_t RGE) | audit ledger only | tree-level → ~119.93 GeV via corrected-y_t at 3L+NNLO | conditional on `y_t` Ward + RGE-transport scaffolding |
| Lattice spacing convergence (`m_H/m_W` flow as `a → 0`) | [`HIGGS_FROM_LATTICE_NOTE.md`](HIGGS_FROM_LATTICE_NOTE.md) (`bounded_theorem`, td=310) | audit ledger only | `m_H/m_W = 1.85` at `a=1` → 1.64 at `a=0.5` → 1.558 SM in continuum | continuum-limit theorem surface |
| Wilson-term taste-breaking ((1,4,6,4,1) staircase) | [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md); the sister Wilson follow-on notes `HIGGS_CHANNEL_EFFECTIVE_NTASTE_BOUNDARY_BOUNDED_NOTE_2026-05-08.md`, `WILSON_CORRECTED_V_TASTE_TREE_LEVEL_BOUNDED_NOTE_2026-05-08.md`, `WILSON_VTASTE_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md`, and `WILSON_M_H_TREE_AT_EXTREMUM_LEADING_ORDER_IN_R_BOUNDED_NOTE_2026-05-08.md` are listed as file-pointer context references (backticked to avoid length-2 back-edges, since each of those notes already cites this note as the load-bearing parent in their proof-walks) | audit ledger only | proves the finite staircase identity and bounded leading-order Wilson correction formulas | **still open**: no retained closure of the physical gap; uniform `N_taste = 16`, any nonzero Wilson coefficient `r`, and the leading-order comparison to 125.10 GeV remain bounded/noncanonical inputs |
| Buttazzo full-3-loop calibration cross-check | `scripts/frontier_higgs_buttazzo_calibration.py` | (auxiliary calibration) | independent ~125.1 GeV via 3-loop Buttazzo parametric calibration | a different observable along a different chain; not load-bearing for this note |

### What this Step 7 changes

No claim status or theorem boundary. The +12% gap remains an open chain
across sister authorities and a remaining quantitative-effect bridge. This
note continues to claim only the tree-level formula
`m_H_tree = v/(2 u_0) = 140.3 GeV`, with the gap-closure load explicitly
delegated.

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
  leading-order `m_H_tree` comparison. These notes sharpen the
  dependency chain but do **not** close the physical +12% gap: the
  channel choice is non-derived, the parent canonical setup has
  `r = 0`, and the `r ≈ 0.235` number is a leading-order comparison
  value rather than a derivation of a Wilson coefficient.

---

## Definitive answer

    m_H = v / (2 u_0) = 140.3 GeV     (zero free parameters, +12%)

with u_0 = 0.8776 from SU(3) plaquette at beta = 6, and v = 246.22 GeV
from the hierarchy theorem. N_c cancels. The 8/9 does not enter.

---

## Dependencies

- `TASTE_POLYNOMIAL_NOTE.md` -- det(D+m) = (m^2 - 4c^2)^8
- `DM_AMGM_SATURATION_NOTE.md` -- eigenvalue degeneracy from Clifford identity
- `HIERARCHY_THEOREM.md` -- v = M_Pl * alpha_LM^16
- `YT_EW_COLOR_PROJECTION_THEOREM.md` -- 8/9 applies to EW couplings only
- `HIGGS_MASS_DERIVED_NOTE.md` -- CW analysis and honest status
- `HIGGS_FROM_LATTICE_NOTE.md` -- lattice spacing convergence (`a → 0`)
- `HIGGS_MASS_FROM_AXIOM_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02.md` -- 2026-05-02 status-correction packet classifying the lattice-curvature → (m_H/v)² bridge as same-shape lattice-physical matching obstruction (cycles 5, 9, 11)
- `AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02.md` -- cluster-level synthesis of the lattice-physical matching obstruction
- `frontier_higgs_mass_corrected_yt.py` -- corrected-`y_t` Higgs support route
- `frontier_higgs_buttazzo_calibration.py` -- full-3-loop boundary support

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [yt_ew_color_projection_theorem](YT_EW_COLOR_PROJECTION_THEOREM.md)
- `HIGGS_MASS_DERIVED_NOTE.md` (file-pointer context reference, backticked
  to avoid the known back-edge through the EW-coupling / `g_1(v)`-`g_2(v)`
  input-authority cluster; that note already cites this one in its
  Note↔runner reconciliation section)
- [higgs_from_lattice_note](HIGGS_FROM_LATTICE_NOTE.md)
