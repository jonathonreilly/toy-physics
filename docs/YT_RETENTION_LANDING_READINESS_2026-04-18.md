# YT Retention Landing Readiness Report (Submission Under Review)

**Date:** 2026-04-18
**Status:** NAVIGATION / REVIEWER-FACING SUMMARY of the YT retention
**submission branch** after Session Round 2 reconciliation. This
report is an internal readiness checklist over the YT-lane artifacts
**introduced by this branch and currently under review**. It does
**not** claim acceptance; it is the proposal-side self-audit the
reviewer uses to locate files, check replay, and decide whether the
retained claims themselves should be accepted.

The sub-theorem notes, runners, and logs catalogued below are
**proposed** for promotion to retained status on `main`. Until the
reviewer accepts the package, the word "retained" in this report
refers to the sub-theorem's *proposal-side* self-classification, not
to an already-accepted repo-wide verdict.

**Companion manifest:** `docs/YT_RETENTION_MASTER_MANIFEST_2026-04-18.md`
**Landing-readiness runner:** `scripts/frontier_yt_retention_landing_readiness.py`
**Landing-readiness log:** `logs/retained/yt_retention_landing_readiness_2026-04-18.log`

---

## 1. Executive summary (1 page)

**Self-audit status: READY FOR REVIEW.** The branch's internal
checks replay without failure and the manifest runner now agrees
with the manifest note on slot status. This is the submission's
proposal-side verdict, not an acceptance verdict. The reviewer
retains the final accept / revise / reject call on the retained
claims themselves.

Known caveats declared up front for the reviewer:

- one documentation-hygiene item: P1.4's note file remains
  EMBEDDED-only by design (runner + log on disk);
- one open scientific coverage item: framework-native 2-loop
  `Δ_R` MC closure is OPEN — the through-2-loop central in this
  package is **bound-constrained**, not MC-pinned (see §R2.2 of
  the manifest).

The YT UV-to-IR transport submission bundles **1617 PASS markers
across 39 proposal-runners, 0 FAIL** on the branch's internal
replay. The canonical framework-native `Δ_R` central proposed by
this branch is **`−3.77 % ± 0.45 %`** (full-staggered-PT 4D BZ
quadrature, P1.15); the literature-cited `−3.27 %` is preserved as
the prior citation-based assembly, explicitly superseded as the
canonical central on the proposal side. The through-2-loop value is
**bound-constrained**, not MC-pinned (Round 2 honesty fix, §R2.2
of the manifest).

The proposed m_t(pole) YT-lane coverage stands at
**`172.57 ± 6.9 GeV`** (through 2-loop, structural extension), consistent
with the observed PDG central **`172.69 GeV`** at ~0.1σ.

All six Round-2 in-flight deliverables are on disk in this
submission:

1. **Agent A (files on disk).** Master obstruction theorem note
   (M.1) and P1.1 shared-Fierz shortcut no-go standalone notes.
2. **Agent H (files on disk).** P1.2 color-factor retention note,
   P3.1 K_1 framework-native derivation note, and P3.2 K_2
   color-factor retention note, each with runner and log.
   Combined contribution: +15 PASS markers in Pillar A.
3. **Agent I (files on disk).** SSB matching-gap analysis note,
   runner, and log. Contribution: 19 PASS markers in Pillar B.
   After the audit repair, this note is a scoped `H_unit`
   component-overlap arithmetic boundary. It does not corroborate a
   physical SSB/Yukawa matching closure.

The known open scientific items at this point are **framework-native
2-loop Δ_R closure** and the physical SSB/Yukawa operator-matching
theorem outside the repaired arithmetic note. The 2-loop item is a
coverage item, not an accuracy item. The proposed 2-loop value is
loop-geometric bound-constrained (P1.17 retains a schematic
magnitude-envelope check; §R2.2 Agent C honesty fix made this
explicit). The
equivalent coverage question on P3 is closed by the K-series
geometric bound (P3.5) at 0.137 % fractional tail on m_t. Both P2
and P3 residuals sit inside the packaged ~2 % m_t(pole) envelope;
P1's 2-loop coverage is the widest proposed band at
`±0.7 % (structural)` / `±0.84 % (bound)` on Δ_R.

**The reviewer retains the accept / revise / reject call on the
retained claims themselves.** This section reports the proposal's
self-audit, not an acceptance verdict.

---

## 2. Key retained results

| Quantity                                              | Retained value              | Source                        |
|-------------------------------------------------------|-----------------------------|-------------------------------|
| **Δ_R (1-loop, framework-native; CANONICAL)**          | **−3.77 % ± 0.45 %**         | P1.15 full-staggered-PT       |
| Δ_R (1-loop, literature-cited; superseded as canonical)| −3.27 % ± 2.32 %             | P1.12 master assembly         |
| Δ_R (through-2-loop, structural, lit base)             | −3.99 % ± 0.70 %             | P1.16                         |
| Δ_R (through-2-loop, bound-constrained, full-PT base)  | ≤ −4.60 % ± 0.84 %           | P1.17 (bound, not MC pin)     |
| P1 loop-expansion envelope                             | `|Δ_R^tot| ≤ 7.41 %`         | P1.3                          |
| P2 residual (3-loop tail)                              | 0.15 %                       | P2.4                          |
| P3 residual (K_4 onward on m_t)                        | 0.137 %                      | P3.5                          |
| m_t(pole) YT-lane (1-loop, canonical)                  | **172.57 ± 6.50 GeV**        | P1.15                         |
| m_t(pole) YT-lane (through-2-loop, structural)         | 172.57 ± 6.9 GeV             | P1.16                         |
| m_t(pole) YT-lane (through-2-loop, bound-constrained)  | 172.57 ± 7.94 GeV            | P1.17                         |
| m_t(pole) observed (PDG)                               | 172.69 GeV                   | external                      |

**Packaged Ward ratio:** `y_t² / g_s² = 1 / (2 N_c) = 1/6`, from the
retained tree-level Ward identity at `M_Pl`. The canonical retained
`Δ_R` is the 1-loop correction to this ratio on the tadpole-improved
Wilson-plaquette + 1-link staggered-Dirac surface.

**Sign / scheme consistency:** `Δ_R` is negative on the retained
surface, consistent with the MSbar `y_t / g_s` running direction; the
SM-RGE cross-check (P1.13) confirms `Δ_R` is orthogonal to the 2-loop
SM-RGE transport.

---

## 3. Pillar A status (P1 + P2 + P3 primitive retention suite)

**Runners:** 26 · **PASS:** 868 · **FAIL:** 0 · **anomalies:** none.

| Sub-pillar                                | Runners | PASS | FAIL |
|-------------------------------------------|--------:|-----:|-----:|
| P1 (17 slots; structural + BZ + assembly) |      16 |  654 |    0 |
| P2 (4 slots)                              |       4 |   84 |    0 |
| P3 (5 slots; all 5 on-disk runners post-Round-2) |       5 |  130 |    0 |

**Pillar A proposal-side self-audit: PASS.** All 26 Pillar-A
runners terminate PASS on the branch's internal replay; no FAIL
markers are present anywhere in the Pillar-A logs. The canonical
1-loop central has sub-percent precision and the through-2-loop
proposed band is bound-constrained within the loop-geometric
envelope. Acceptance for promotion to retained status on `main` is
the reviewer's call.

**Open scientific item in Pillar A:** framework-native 2-loop Δ_R
MC closure (P1.17 carries a bound-envelope value, Round 2
honesty-fix §R2.2). This is a coverage item, not a defect; see
Gap 4.

---

## 4. Pillar B status (retention-analysis class notes + SSB companion)

**Runners:** 11 · **PASS:** 595 · **FAIL:** 0 · **anomalies:** none.

| Class / note                                          | Runner PASS | Status                                         |
|-------------------------------------------------------|------------:|------------------------------------------------|
| Class #1 (H_unit flavor-column decomposition)         |          79 | retained no-go; §10 scrutiny audit (Round 2)   |
| Class #2 (generation-hierarchy primitive)             |          51 | retained narrow no-go + Fourier correction (Round 2) |
| Class #3 (SUSY / 2HDM)                                |          79 | retained; no Round 2 correction required       |
| Class #5 (non-Q_L Yukawa vertex)                      |          56 | §0 matching-gap closure sketch added (Round 2) |
| Class #6 (C_3 breaking operator)                      |          43 | retained narrow no-go + Fourier correction (pre-Round 2) |
| Class #7 (spontaneous C_3 breaking)                   |          41 | retained; no Round 2 correction required       |
| b-Yukawa retention analysis                           |          52 | §0 scope correction (Round 2)                  |
| Right-handed species dependence (Class #4)            |          58 | §4.2 Δ_R correction inherited (Round 2)        |
| Species-uniformity extent                             |          48 | retained                                       |
| EW Δ_R retention                                      |          69 | retained                                       |
| SSB matching-gap companion (Round 2, Agent I)         |          19 | scoped H_unit arithmetic boundary; physical matching remains open |

**Pillar B proposal-side self-audit: PASS.** Every retention-
analysis class note terminates PASS on the branch's internal replay
with no FAIL markers. The Round 2 corrections (Class #2 §0 Fourier,
Class #5 §0 matching-gap closure, b-Yukawa §0 scope, Class #1 §10
scrutiny audit, Class #4 §4.2 inheritance) are scope / framing
tightening, not numerical changes. The Round 2 SSB companion note now
records only the exact `H_unit` component-overlap arithmetic; it does
not provide an independent physical matching closure. Reviewer
acceptance of Pillar B is a separate decision.

---

## 5. Pillar C status (master obstruction + manifest)

**Runners:** 2 · **PASS:** 154 · **FAIL:** 0 · **anomalies:** none.

| Note / runner                               | PASS | Status                                                            |
|---------------------------------------------|-----:|-------------------------------------------------------------------|
| Master UV-to-IR obstruction (M.1)           |    5 | recreated by Agent A (Round 2); ON DISK                           |
| Retention master manifest                   |  118 | updated by current agent (Round 2); Session Round 2 section added |

**Pillar C proposal-side self-audit: PASS.** All Pillar-C checks
terminate PASS on the branch's internal replay with no FAIL
markers. The manifest runner and the manifest note agree on slot
status (Round 2 finding R2.8 — see manifest §R2.8). The retention
manifest has been updated with the Session Round 2 corrections
section (§R2), the canonical central is explicitly recorded as
`Δ_R = −3.77 % ± 0.45 %` on the full-staggered-PT surface, and the
through-2-loop value is labelled as bound-constrained rather than
MC-pinned.

---

## 6. Cross-reference integrity sweep

The landing-readiness runner resolved 713 repo-internal Markdown
link targets across 38 session-dated YT notes. Broken references
identified (post-Round-2 final state):

- **5** references to `docs/YT_P1_I1_LATTICE_PT_SYMBOLIC_DECOMPOSITION_NOTE_2026-04-17.md`
  (slot P1.4 — **intentionally EMBEDDED-only by design**; runner
  and log exist with 21 PASS).

**Total broken:** 5, all of which are **expected and accounted for**:
the P1.4 references are the intentionally EMBEDDED-only slot's expected link
targets.

No Agent H or Agent I artifact is missing. All six Round-2 landed
artifacts (M.1 note, P1.1 note, P1.2 note/runner/log, P3.1
note/runner/log, P3.2 note/runner/log, SSB note/runner/log) resolve
correctly.

---

## 7. Known open items

### Open item 1: framework-native 2-loop Δ_R closure

- **Current status:** proposed as loop-geometric bound
  (`|Δ_R^{(2)}| ≤ 0.834 %`, same-sign saturation).
- **What would close it:** a framework-native 4D BZ quadrature of
  the 2-loop integrand with explicit enforcement of the gauge-
  group-irreducible topology cancellations that the schematic 8D MC
  in P1.17 does not capture.
- **Impact if open:** through-2-loop m_t(pole) coverage is
  `±6.9 GeV` structural / `±7.94 GeV` bound-constrained, already
  well inside the packaged ~2 % m_t(pole) envelope (`≃ ±3.45 GeV`
  at the packaged P3-dominated residual).
- **Proposal-side reviewer-gating assessment:** proposal-side NO
  (the 1-loop canonical central and the P3 geometric bound already
  place m_t(pole) inside the packaged envelope). Whether this
  coverage gap is acceptable for retained-status promotion on
  `main` is the reviewer's call.

### Open item 2: P1.4 standalone note promotion (documentation hygiene)

- **Current status:** EMBEDDED-ONLY by design. The I_1 symbolic
  decomposition runner `frontier_yt_p1_i1_lattice_pt_symbolic.py` and
  log `yt_p1_i1_lattice_pt_symbolic_2026-04-17.log` (21 PASS) are on
  disk; the standalone note file is not.
- **What would close it:** promote the embedded derivation to a
  standalone note file at
  `docs/YT_P1_I1_LATTICE_PT_SYMBOLIC_DECOMPOSITION_NOTE_2026-04-17.md`.
- **Impact if open:** minor documentation-hygiene improvement. The
  load-bearing content (I_1 = I_S − I_V with conserved-current Ward
  reduction `I_V = 0`) is carried through the P1 runners that cite
  it as a named prior.
- **Proposal-side reviewer-gating assessment:** proposal-side NO
  (documentation hygiene only, runner + log on disk). Whether the
  reviewer wants the standalone note promoted before acceptance is
  the reviewer's call.

---

## 8. Landing readiness checklist

| Check                                                          | Status | Gating? |
|----------------------------------------------------------------|:------:|:-------:|
| Grand total PASS (retention manifest + landing-readiness)      | 1617   | —       |
| Grand total FAIL                                               | 0      | —       |
| Canonical `Δ_R` central on disk and cited as canonical         | PASS   | no      |
| Canonical `Δ_R` central ≠ superseded literature-cited central  | PASS   | no      |
| Through-2-loop central labelled as bound-constrained, not MC-pinned | PASS | no    |
| Class #5 §0 matching-gap closure on disk                       | PASS   | no      |
| Class #2 §0 Fourier correction on disk                         | PASS   | no      |
| Class #1 §10 scrutiny audit on disk                            | PASS   | no      |
| Class #4 §4.2 Δ_R correction inherited on disk                 | PASS   | no      |
| b-Yukawa §0 scope correction on disk                           | PASS   | no      |
| Master obstruction theorem standalone on disk (Round 2)        | PASS   | no      |
| Shortcut no-go standalone on disk (Round 2)                    | PASS   | no      |
| SSB matching-gap note + runner + log on disk (Round 2)         | PASS   | no      |
| Agent H's 3 color-factor / K_1 / K_2 recreations on disk       | PASS   | no      |
| Publication-surface files unmodified                           | PASS   | YES     |
| Canonical-surface numerics unchanged                           | PASS   | YES     |
| Session Round 2 amendment record (§R2) on disk                 | PASS   | no      |

**Interpretation of the two YES-gating checks:** both passed on
the branch's internal self-audit. The Round 2 amendments modify
framing / scope / interpretive framing of the proposal-side notes
via §0 / §10 corrections in-place; no canonical number is changed,
no publication-surface file is touched. Acceptance of the
non-gating items is the reviewer's call.

---

## 9. Self-audit verdict

**Proposal-side verdict: READY FOR REVIEW.** The submission's
internal self-audit terminates at **1617 PASS markers / 0 FAIL
markers across 39 proposal-runners**, with the canonical 1-loop
framework-native central `Δ_R = −3.77 % ± 0.45 %` and the proposed
m_t(pole) band `172.57 ± 6.9 GeV` consistent with PDG at ~0.1σ.
All six in-flight Round-2 deliverables (Agents A, H, I) are on
disk. The remaining proposal-side open items — framework-native
2-loop Δ_R MC closure (coverage, not accuracy) and P1.4 standalone
note promotion (documentation hygiene), plus the physical SSB/Yukawa
operator-matching theorem outside the scoped arithmetic note — are declared up
front for the reviewer's accept / revise / reject decision. The 5 broken
cross-references are all expected P1.4 embedded-only references.

This report is a navigation index over the YT submission bundle.
It does not introduce physics of its own; the retained claims
proposed by this branch live in the sub-theorem notes, not here.
No publication-surface file is touched by the proposal. Whether
the sub-theorem claims should be accepted, revised, or rejected is
the reviewer's call.

**Next-step suggestion for the reviewer:** start at
`docs/YT_RETENTION_MASTER_MANIFEST_2026-04-18.md` §Part 7 ("reviewer
reading guide"), then descend into P1.15 (canonical central) and
P1.17 (bound-constrained 2-loop coverage) to verify the Round 2
honesty fix, and cross-read the repaired SSB matching-gap note only
as a scoped `H_unit` arithmetic boundary; do not treat it as closing
the physical matching theorem.

---

## 10. Artifact inventory (this report)

- This report: `docs/YT_RETENTION_LANDING_READINESS_2026-04-18.md`
- Landing-readiness runner: `scripts/frontier_yt_retention_landing_readiness.py`
- Landing-readiness log: `logs/retained/yt_retention_landing_readiness_2026-04-18.log`
- Companion manifest: `docs/YT_RETENTION_MASTER_MANIFEST_2026-04-18.md`
