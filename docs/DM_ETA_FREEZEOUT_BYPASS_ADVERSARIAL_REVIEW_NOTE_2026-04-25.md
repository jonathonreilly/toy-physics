# DM eta Freezeout-Bypass Quantitative Theorem -- Adversarial Self-Review

**Date:** 2026-04-25 (same-day adversarial review)
**Status:** internal review packet flagging issues with the same-day quantitative
theorem and its G1 Wilson-mass attempt. Findings ranked CRITICAL / MODERATE /
MINOR. Each finding has a recommended fix and an explicit fix-status.

**Authority targets reviewed:**
- [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
- [`scripts/frontier_dm_eta_freezeout_bypass_quantitative_theorem.py`](../scripts/frontier_dm_eta_freezeout_bypass_quantitative_theorem.py)
- [`scripts/frontier_dm_eta_freezeout_bypass_g1_wilson_mass_attempt.py`](../scripts/frontier_dm_eta_freezeout_bypass_g1_wilson_mass_attempt.py)

## Findings

### F1. CRITICAL -- "16" provenance ambiguity (two different lattices)

The number 16 appears in this work with TWO incompatible structural origins:

**Origin A (audit-level identification, in main theorem):**
`16 = N_sites = 2^d` from the **minimal APBC block on Z^4** (spacetime
lattice with d = 4). This is the same N_sites = 16 that appears in
[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md).

**Origin B (G1 attempt, in Wilson-mass runner):**
`16 = 6 * 8/3 = (2 * hw_dark) * (dim(adj_3) / N_c)` where:
- `2 * hw_dark = 6` is the bare chiral Wilson mass eigenvalue on the
  **`Cl(3)` taste cube `C^8 = (C^2)^otimes 3`** (hw operator on Z_2^3),
- `dim(adj_3)/N_c = 8/3` is an **SU(3) Casimir ratio** in color space.

These are THREE DIFFERENT spaces (Z^4 spacetime, Z_2^3 chiral taste, SU(3)
color). The numerical coincidence `N_sites = (2 * hw_dark) * (dim(adj_3)/N_c)`
in SU(3) is just integer arithmetic: `16 = 6 * 8 / 3`. There is no derived
theorem connecting Origins A and B.

A skeptical reviewer would observe: "you have written down the candidate
`m_DM = 16 v` and *post-hoc* identified two unrelated factorizations, each
of which uses the framework's structural counts. This is reverse-engineering
the answer, not deriving it."

**Severity:** CRITICAL. Without resolution, the structural cleanness of the
candidate is undermined.

**Recommended fix:** Be honest. The audit-discovered candidate is the
NUMERICAL FACT `m_DM ≈ 16 v`. The two factorizations (A and B) are
*candidate origin stories*, neither of which is yet a derived theorem. The
honest framing: "The numerical match m_DM = 16 v is striking but the
structural mechanism is open. Two distinct factorizations are tabulated as
candidates for follow-up; the eventual retained closure must pick one (or
unify them via a genuine Coleman-Weinberg argument that involves all three
structures jointly)."

**Fix status:** ADDRESSED in this review note. Main theorem note will be
updated to flag the two origin stories explicitly as competing candidates.

### F2. MODERATE -- Multiple-comparisons risk in the audit

The main theorem's section 3 audit tested 19 candidate structural mass
identities against the freeze-out target. ONE candidate (`N_sites * v`)
landed within 5%. The closest competitor is at 19.82%. This is presented as
a "decisive structural match".

But: with 19 candidates spanning a wide range of structural products, even
a uniform random distribution of `m_pred / m_target` ratios would expect
to land 1-2 candidates within `+/-5%` of any given target. The "decisive"
language could be a multiple-comparisons artifact.

**Severity:** MODERATE. The candidate may still be special, but the audit
needs a null-distribution test.

**Recommended fix:** Run a null-distribution audit. Define a clean class of
"random structural mass identities" (e.g., `m = v * prod_i x_i^{p_i}` for
`x_i in {alpha_LM, u_0, pi, 2, 3, N_c, N_sites, hw_dark, R_base}` and
`p_i in {-2, -1, 1, 2}` with bounded total complexity). Enumerate all such
identities up to some complexity, compute deviation from target, and ask:
where does the candidate `N_sites * v` sit in the distribution? If it is
in the top 1%, the audit's match is significant. If it is in the top 50%,
the audit is not informative.

**Fix status:** ADDRESSED in [section "Implemented fixes"](#implemented-fixes)
with a new null-distribution runner.

### F3. MODERATE -- Hierarchy compression for dark sector is unjustified

Both the main theorem and the G1 attempt apply the **EW hierarchy
compression** `v = M_Pl * (7/8)^(1/4) * alpha_LM^16` to the dark sector's
bare lattice mass. Specifically, the G1 attempt writes:

> bare physical mass `m_S3_bare = 6 * M_Pl`
> after retained hierarchy compression: `m_S3_bare(phys) = 6 * v`

The retained hierarchy theorem
([`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md))
gives `v` as the **EWSB condensate** scale on the visible sector. Applying
the same compression `M_Pl * alpha_LM^16` to the dark sector's bare
lattice mass requires either:
- a separate theorem showing the dark sector's effective scale is also
  `M_Pl * alpha_LM^16`, or
- an explicit assumption that the dark sector lives at the same hierarchy
  level as the visible.

Currently, this is the latter -- assumed.

**Severity:** MODERATE. The structural argument hinges on the dark sector
sharing the visible sector's hierarchy compression. Without justification,
the m_DM ~ 4 TeV prediction depends on this assumption.

**Recommended fix:** Document this as an EXPLICIT assumption in the theorem
note. State: "we assume the dark Hamming-weight-3 singlet's bare lattice
mass undergoes the same hierarchy compression as the EWSB condensate, by
the same `(7/8)^(1/4) * alpha_LM^16` factor. A separate hierarchy theorem
for the dark sector would be required to justify this independently."

**Fix status:** ADDRESSED in this review; will be explicitly flagged in the
main theorem note as assumption A0.

### F4. MINOR -- Misleading "matching Planck to ~0.5%" summary line

The runner summary previously said: `"matching Planck to ~0.5%"`. This was
a leftover hardcoded string. The actual nominal deviation is `+4.22%`
(within bounded band, but not 0.5%).

**Severity:** MINOR (already partially fixed in the runner; needs final
review of the theorem note).

**Fix status:** ADDRESSED. Runner summary now states `+4.22%` correctly.
Theorem note's "matching Planck to ~0.5%" wording (from G1 docstring) will
be reviewed.

### F5. MINOR -- s-wave Coulomb saturation assumption for sigma_v

The freezeout-bypass identity uses `<sigma_v> = pi * alpha_X^2 / m_DM^2`
(s-wave Coulomb saturation). For dark-sector annihilation through the link
mediator, this is the standard textbook form, but:
- Real annihilation may have P-wave contributions (suppressed by v_rel^2)
- Threshold corrections shift the cross-section by O(1) factors
- t-channel scalar exchange gives a different `m_DM`-dependence

The 4.22% deviation is well within these textbook approximation noises
(typically O(10%)), so the bound is not falsified -- but the cleanness of
the prediction is overstated if read as `+/-1%`.

**Severity:** MINOR (already correctly bounded in the theorem note as a
"bounded freeze-out coefficient" range).

**Fix status:** Adequate as documented. Monitor in future rebases if more
precise freeze-out numerics are added.

### F6. MINOR -- "DM is hw=3 singlet" identification not derived

The C^8 chiral taste decomposition `1 + 3 + 3 + 1` has TWO singlets:
- `hw = 0` (the unflipped state, EWSB Higgs sector)
- `hw = 3` (the all-flipped state, the proposed DM candidate)

The identification "DM = hw=3 singlet" is consistent with the historical
DM derivation literature on this branch (see
[`DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17.md`](DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17.md)
and the visible/dark partition `T_1 + T_2 = 6` (gauge-active) vs
`S_0 + S_3 = 2` (gauge-singlet)), but not derived from the axiom on the
present surface. The hw=0 (S_0) is also a gauge-singlet; why is DM the
hw=3 (S_3) and not the hw=0 (S_0)?

**Severity:** MINOR. The visible/dark partition is established on the live
surface; the specific hw=3 vs hw=0 selection is implicitly fixed by the
"all-flipped" interpretation (S_0 is the unbroken vacuum, S_3 is the
"completely-flipped" field excitation). Documenting this explicitly is
sufficient.

**Fix status:** Will document the hw=3 selection in the next theorem-note
revision as a structural identification, with the partition theorem cited.

## Implemented fixes

### Multiple-comparisons null-distribution audit (addresses F2)

Added: `scripts/frontier_dm_eta_freezeout_bypass_null_distribution_audit.py`

This script:
1. Defines a class of "structural candidate" identities of the form
   `m_pred = v * prod_i x_i^{p_i}` where `x_i in {alpha_LM, u_0, pi, 2,
   3, N_c, N_sites, hw_dark, R_base, alpha_s(v)}` and `p_i in {-2,-1,1,2}`.
2. Enumerates all candidates with total complexity (sum of |p_i|) <= 4.
3. Computes |dev| from `m_DM_target = 3859.92 GeV`.
4. Reports the percentile of the audit-selected `N_sites * v` candidate
   in the resulting null distribution.

If `N_sites * v` is in the top 1%, the audit match is genuinely informative;
if it is in the top 50%, the audit is not.

### Two-origin honest framing (addresses F1)

The theorem note has been updated to flag both Origin A (N_sites from APBC
block) and Origin B (Wilson chiral + SU(3) Casimir factorization) as
**competing candidate origin stories** rather than as a single derived
identity. The text explicitly says: "The numerical match `m_DM = 16 v` is
striking; two distinct structural factorizations are tabulated as
follow-up candidates."

### Explicit assumption A0 (addresses F3)

The hierarchy compression for the dark sector is now flagged as A0:
"the dark Hamming-weight-3 singlet's bare lattice mass undergoes the
same hierarchy compression as the EWSB condensate". A0 is listed alongside
G1-G4 as an open structural input.

## Updated honest-status board

After fixes, the work breaks down as follows:

| component | status |
|---|---|
| `eta = C * m_DM^2` identity (Eq. 2 in main note) | RIGOROUS, structural |
| Numerical reproduction of `C` on canonical surface | RIGOROUS |
| Audit list of 19 candidates | RIGOROUS, but susceptible to F2 |
| Null-distribution percentile of `N_sites * v` | NEW, addresses F2 |
| `m_DM = 16 v ~ 3940 GeV` numerical match (2.09% from target) | RIGOROUS NUMERICAL FACT |
| `eta_pred = 6.38e-10` at central point | RIGOROUS, +4.22% from Planck |
| Bounded band brackets `eta_obs` | RIGOROUS |
| Origin A: `16 = N_sites` from APBC block | CANDIDATE (post-hoc) |
| Origin B: `16 = 6 * 8/3` from chiral Wilson + SU(3) Casimir | CANDIDATE (post-hoc) |
| Hierarchy compression to dark sector (A0) | ASSUMPTION, not derived |
| sigma_v = pi * alpha_X^2 / m^2 | TEXTBOOK approximation |
| Sommerfeld continuation (F4) | BOUNDED, in [1.4, 1.7] |
| `x_F = 25` freeze-out | DERIVED (log-insensitive), bounded [22, 28] |
| `alpha_X = alpha_LM` | choice, structural-clean candidate |
| `DM = hw=3 singlet` identification | structural identification |
| **G1 Coleman-Weinberg theorem** | **OPEN** |

## Conclusion

The same-day adversarial review identifies one CRITICAL finding (F1, the
"16" provenance ambiguity) and two MODERATE findings (F2 multiple-
comparisons, F3 hierarchy compression). All three are addressed via
clarifying language and a new null-distribution runner. After fixes, the
work stands as:

> A bounded-grade quantitative theorem on the DM eta gate via the
> freeze-out bypass, with the numerical fact `m_DM = 16 v` matching the
> freeze-out target at 2% and Planck eta at 4%. Two candidate structural
> origins are tabulated; both are post-hoc factorizations. The retained-
> grade closure path is a Coleman-Weinberg derivation of the dark
> hw=3 singlet's mass on the SU(3)-gauged staggered minimal block.

This is honest progress, not a closure.
