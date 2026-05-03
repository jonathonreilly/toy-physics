# Closed PR Science Salvage Sweep 2026-05-03

Purpose: record the review-loop sweep over closed unmerged PRs from PR #1
forward, excluding PR #230 as requested. This is a review-history surface,
not a physics source note.

## Scope

- Closed PRs scanned: 411, through PR #412.
- Closed merged PRs: 327; treated as already landed on main.
- Closed unmerged PRs reviewed for missed science: 84.
- PR #230 was not touched.

## Salvaged Into Source Rows

These PRs had runner-backed source lemmas worth preserving. The salvage PR
keeps them as source-only notes with independent audit authority and no
author-side audit verdicts.

- PRs #286, #287, #288, #289: bounded charge-arithmetic lemmas for nucleons,
  baryons, mesons, and charged leptons.
- PRs #348, #351, #357, #364, #369, #374: standalone Pattern A algebra
  narrowings. Parent-status checks and non-load-bearing parent links were
  removed so audit can classify them independently, including as decoration
  if appropriate.
- PRs #352, #354, #361, #363, #366, #368, #371, #373, #375, #376, #377,
  #379, #381: exact support lemmas for SU(3), translations, Pauli/Fock
  structure, fermion parity, and hopping bilinears.
- PR #403: the parity dimension-5 Lorentz-violation no-go was salvaged.
  The separate hierarchy `a = ell_Pl` item was not salvaged because it
  reuses an admitted carrier-scale premise rather than adding an independent
  source lemma.
- PR #406: the CMT channel-blindness result was salvaged as a no-go against
  the naive M-residual interpretation.

## Not Salvaged

These PRs were reviewed and intentionally not imported into source rows.

- Audit/control-plane or companion-only material with no source lemma to
  preserve: #99, #175, #179, #213, #222, #291, #349, #353, #358, #362,
  #365, #370, #378, #387, #389, #393, #396.
- Source files already exist on current main or the closed branch is stale
  status/hygiene over an existing source surface: #82, #83, #85, #93, #95,
  #97, #172, #191, #192, #199, #238, #245, #367, #385, #388, #391, #394,
  #397, #398, #400, #401, #404.
- Missing or divergent science was not audit-ready as a source row because
  it is historical, superseded, comparator-heavy, overclaimed, dependent on
  unlanded siblings, or only a named-obstruction/stretch packet: #31, #86,
  #87, #113, #180, #195, #198, #383, #386, #392, #395, #399, #402, #405,
  #407, #408, #409, #410, #411, #412.

## Rejection Notes

- PR #402's Wess-Zumino/Fujikawa source overreaches into broad anomaly and
  counterterm claims; it should be rewritten narrowly before any source
  submission.
- PRs #405 and #407 depend on unlanded sibling derivations and duplicate or
  overclaim existing electroweak source surfaces.
- PRs #408 through #412 are useful work history and obstruction sharpening,
  but they carry admitted baselines, external comparators, or numerical
  stretch-attempt framing rather than a clean audit-ready lemma.
- PRs #31, #86, #87, #113, #180, and #195 belong to older or comparator-heavy
  lanes and should stay historical unless rewritten as narrow source claims.
