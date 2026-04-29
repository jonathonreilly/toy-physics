# Lane 3 — Quark Masses Retention

**Date:** 2026-04-26
**Status:** ACCEPTED CRITICAL OPEN SCIENCE LANE on `main`; no theorem or claim
promotion
**Science priority:** HIGHEST. CKM closing in α_s + rationals does NOT satisfy
"quark masses derived."
**Approachability:** Tier B-C (4–8 months for full closure; first sub-targets
landable in 4–8 weeks)
**Primary closure targets:** retained `m_u`, `m_d`, `m_s`, `m_c`, and `m_b`
from framework-native amplitudes and threshold-local retention.
**First parallel-worker target:** separate the bounded companion matches from
actual load-bearing theorem targets, then attack one up-type and one down-type
sub-target.
**Non-claim boundary:** the top mass is retained; the remaining five quark
masses are not.

## 2026-04-27 Dependency Firewall

The [Quark Lane 3 bounded-companion retention firewall](../../QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md)
records the current no-go boundary for this lane. The top mass is retained,
but CKM closure, bounded down-type ratios, and bounded up-type extensions do
not by themselves retain `m_u`, `m_d`, `m_s`, `m_c`, or `m_b`.

The firewall blocks any five-mass closure unless a branch supplies theorem-core
down-type bridges and scale selection, a retained up-type partition or scalar
amplitude law, and a species-differentiated Yukawa Ward or equivalent absolute
scale primitive for non-top quarks.

## 1. Missing-science framing

The CKM atlas/axiom package closes many mixing identities, but the framework
still needs direct answers to:

> "Wait — what about m_u, m_d, m_s, m_c, m_b? You closed CKM without using
> quark masses, but where are the quark masses themselves?"

The answer in the current package is "bounded companion" — meaning the
threshold-local self-scale comparison gives sub-percent matches but the
comparison uses PDG values, not framework-derived ones. The 5/6 = C_F − T_F
exponent for V_cb is a structural identity but its non-perturbative proof at
lattice scale remains open. The up-type sector has a candidate scalar law
shortlist (7/9, √(3/5), atan(√5)−√5/6, ...) but no derivation principle picks
one.

**Result: 5 of 6 quark masses are effectively pinned to PDG values via the
bounded companion lane. This is a central missing-science issue for
the framework's TOE claim after Koide.** Closing CKM structurally without
closing the quark mass values themselves is a partial result, not a full
flavor-sector closure.

## 2. Current state of repo content

### Retained

- m_t (pole) = 172.57 GeV at 0.07% (2-loop) — the only retained quark mass
- y_t(M_Pl)/g_s(M_Pl) = 1/√6 (exact lattice-scale Ward identity)
- Full CKM structural closure (every entry + B_s + Thales + NLO γ̄ + Jarlskog NLO
  + barred apex/circumradius/orthocenter — all in α_s and rationals)

### Bounded companion

- Down-type CKM-dual mass-ratio lane:
  - m_d/m_s = 0.05165 (+3.3% from threshold-local self-scale comparator)
  - m_s/m_b = 0.02239 (+0.2%)
  - m_d/m_b = 0.001156 (+3.5%)
- Up-type bounded extension with one interior partition (f_12, f_23)
- 5/6 bridge (V_cb = (m_s/m_b)^(5/6)) — perturbative QCD shifts give Δp ~ 0.01,
  full shift requires non-perturbative dynamics at g=1
- Up-type amplitude scalar law shortlist:
  - 7/9 (strongest small-rational refit)
  - √(3/5) (strongest small-radical anchored)
  - atan(√5) − √5/6 (best one-step native projector/support law)
  - √(5/6) · (1 − 1/√42) (best anchored projector law)
- Quark taste-staircase support
- (Approximately 10 structural support notes in
  [QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md](../../QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md))

### Absent

- Direct retention of m_d, m_s, m_b, m_u, m_c (only ratios bounded;
  absolute scales would chain off m_t retained)
- Full non-perturbative proof of the 5/6 exponent
- Up-type scalar amplitude law (which of the shortlist candidates is correct)
- Generation-stratified Yukawa Ward identities (analog of y_t Ward for u, d,
  s, c, b)

## 3. Derivation targets

### 3A. Down-type 5/6 exponent NP proof

**Target:** prove the V_cb = (m_s/m_b)^(5/6) bridge non-perturbatively at the
lattice scale, beyond perturbative QCD shifts.

**Existing scaffolding:**
- C_F − T_F = 4/3 − 1/2 = 5/6 (exact group-theory rationals)
- Lattice anomalous dimension support (L=4-12 noisy; needs L≥16)
- Taste-staircase support landed 2026-04-25

**Approachability:** Tier B-C. Substantial NP-QCD work but the structural
target is sharp.

### 3B. Up-type amplitude scalar law derivation

**Target:** identify which of the shortlist candidates (or a new clean form)
is the correct up-type amplitude scalar law that closes m_u/m_c retention.

**Existing scaffolding:**
- The candidate shortlist itself
- The widened native-affine-support no-go (rules out one-step affine-projector
  laws)
- Up-amplitude candidate scan + restricted native-expression scan

**Approachability:** Tier B (4–8 weeks). Small candidate set; structural
grammar well-mapped.

### 3C. Generation-stratified Yukawa Ward identities

**Target:** derive y_d/y_t, y_s/y_t, y_b/y_t, y_u/y_t, y_c/y_t as Ward-identity
ratios analogous to the retained y_t(M_Pl)/g_s(M_Pl) = 1/√6.

**Existing scaffolding:**
- The y_t Ward derivation (template)
- The hw=1 triplet structure with 3 generations explicitly
- Generation-color and EW A4 bridges (recent landing 4cc6d474)

**Approachability:** Tier B. Extends existing retained Ward content.

### 3D. Absolute quark-mass scales via m_t retained

**Target:** chain absolute mass scales for all 5 down-type and up-type quarks
off the retained m_t = 172.57 GeV.

**What the framework needs:** generation-stratified Ward (3C) + retained mass
ratios (3A + 3B) → absolute masses by simple chain.

**Approachability:** Tier A-B. Automatic once 3A, 3B, 3C land.

### 3E. CKM-mass cross-validation

**Target:** verify the now-retained quark masses correctly reproduce the
already-retained CKM atlas/axiom structural identities.

**Approachability:** Tier A. Internal consistency check after 3A-3D.

## 4. Existing scaffolding to build on

- [QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md](../../QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md)
- [QUARK_MASS_RATIO_FULL_SOLVE_NOTE_2026-04-18.md](../../QUARK_MASS_RATIO_FULL_SOLVE_NOTE_2026-04-18.md)
- [QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25.md](../../QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT_NOTE_2026-04-25.md)
- [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](../../DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md)
- [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
- The full retained CKM atlas/axiom package
- Generation-color and EW A4 bridges on current `main`
- α_LM geometric-mean identity

## 5. Recommended attack approach

**Phase 1 (parallel):**

1. **3B: Up-type amplitude law.** Small candidate shortlist; weeks of focused
   work could land. Tier B.
2. **3C: Generation-stratified Yukawa Ward.** Template (y_t Ward) is retained;
   lift to other generations. Tier B.

**Phase 2 (after Phase 1):**

3. **3A: Down-type 5/6 NP proof.** Substantial; benefits from the taste-staircase
   support already landed. Tier B-C.
4. **3D: Absolute scales via m_t.** Automatic after Phase 1. Tier A.

**Phase 3:**

5. **3E: CKM-mass cross-validation.** Internal consistency check. Tier A.

## 6. Out of scope / will not claim

- This lane does NOT propose to derive m_t separately (already retained).
- This lane does NOT propose to address heavy-quark expansions (HQET, NRQCD)
  in initial scope.
- This lane does NOT address quark mass running at all scales — focus is
  retained values at canonical lattice / threshold scales.

## 7. Cross-references

- Depends on: Koide closure (for the Q-side of the cross-sector V_cb bridge,
  which provides additional constraint on quark masses via Q_ℓ · α_s² = 4|V_cb|²)
- Enables: Lane 1 (hadron masses depend on quark masses; Lane 1 now
  identifies combined `m_u + m_d` retention as the shortest quark-mass
  dependency for the GMOR pion route)
- Enables: Lane 4 (neutrino sector consistency checks via flavor-universal
  Yukawa structure)
- Cross-validates: existing CKM atlas/axiom package (CKM was closed without
  quark inputs; closing quark masses retention provides independent verification)

## 8. Reviewer questions

1. Should up-type amplitude law (3B) be the entry point, or down-type 5/6
   proof (3A)?
2. Is the generation-stratified Yukawa Ward identity (3C) approach the right
   route, or is there a cleaner taste-staircase route?
3. What precision target should "retained" mean for quark mass ratios —
   sub-percent? PDG precision?
4. Should the 5/6 NP proof be considered a single theorem target or a
   research program with multiple sub-theorems?
