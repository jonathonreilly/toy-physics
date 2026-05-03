# GOAL — Composite-Higgs Mechanism (Cycle 20 / 2026-05-03)

## Lane

EWSB Higgs identification — what plays the Higgs in the framework? This is
an open EWSB question, opened by cycle 07's conditional
`Q = T_3 + Y/2` derivation and sharpened by cycle 08's three named
obstructions:

- **Obstruction 1**: framework lacks retained mechanism for `⟨q̄_L u_R⟩ ≠ 0`
  with EW-symmetry-breaking direction.
- **Obstruction 2**: top-condensate models predict `m_top ~ 600 GeV` (BHL
  1990) — too high; framework needs a different mechanism.
- **Obstruction 3**: multi-bilinear selector ambiguity — `q̄_L u_R`,
  `q̄_L d_R`, `l̄_L e_R` all have matching `(2̄, 1)_{±1}` quantum numbers.

## Target status

`best-honest-status` (per SKILL.md). Expected output type **(c) STRETCH
ATTEMPT**: produce one major cycle's worth of structural analysis on the
composite-Higgs candidate, sharpening cycle 08's obstructions with
branch-local candidate content and explicit named residual obstructions for
what remains.

A closing derivation (output type a) is NOT honestly expected and would
indicate either (i) a missed import, (ii) a numerical coincidence, or
(iii) a real breakthrough requiring separate audit. Treat the campaign
as a multi-route stretch attempt; the route-portfolio + selected-route
execution is the genuine /physics-loop contribution.

## Constraints

### Forbidden imports (hard)

- No PDG values for `m_top`, `m_H`, `v_EW`, `m_W`, `m_Z` as derivation inputs.
- No literature numerical comparators (BHL `m_top ~ 600 GeV`, Hill 1991
  walking technicolor, Holdom 1985, Yamawaki et al. 1986) cited as
  derivation comparators — only as admitted-context external.
- No fitted selectors (no Koide-style fitting).
- No same-surface family arguments.

### Admitted-context external (allowed; not load-bearing on retention)

- Standard QFT machinery (Peskin-Schroeder ch. 20, Weinberg vol. 2).
- SU(N) representation theory.
- SM Yukawa structural form (Halzen-Martin).

### Retained inputs (load-bearing; cited at one hop)

- Derived SM matter and conditional EWSB harness — `UNIFIED_MATTER_CONTENT_EWSB_HARNESS_THEOREM_NOTE_2026-05-03.md`.
- Doubled-Y normalization and `Q = T_3 + Y/2` convention — `LHCM_Y_NORMALIZATION_FROM_ANOMALY_AND_CONVENTION_NOTE_2026-05-02.md`.
- One-Higgs Yukawa gauge-selection boundary — `SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`.
- Higgs `Y_H=+1` from LHCM plus admitted Yukawa structure — `HIGGS_Y_FROM_LHCM_AND_YUKAWA_STRUCTURE_NOTE_2026-05-02.md`.
- Cycle 15 lattice-scale `g_2² = 1/(d+1) = 1/4` — `YT_EW_COLOR_PROJECTION_THEOREM_NOTE.md`.
- Koide Z3 scalar potential — `KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`.
- EW Fierz channel decomposition — `EW_CURRENT_FIERZ_CHANNEL_DECOMPOSITION_NOTE_2026-05-01.md`.

## V1-V5 PROMOTION VALUE GATE (must be answered in cert before PR)

| # | Question |
|---|---|
| V1 | What specific cycle 08 obstruction(s) does this PR sharpen? |
| V2 | What branch-local candidate derivation does this PR contain beyond cycles 07/08/15/16? |
| V3 | Could the audit lane synthesize this from existing retained primitives + textbook QFT? |
| V4 | Is the marginal content non-trivial (not relabeling cycle 08's quantum-number match)? |
| V5 | Is this distinct from cycles 11 (synthesis), 17 (Carrier Orbit), 18 (Z3 origin)? |

All five must answer "yes / explicit / specific" or the cycle is churn and
must NOT be opened as a PR. Honest answer "no" → discard cycle.
