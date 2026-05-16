# Opportunity Queue

**Date:** 2026-05-16
**Loop:** koide-l5-spectral-triple-20260516
**Refreshed:** 2026-05-16T07:15Z

## Ranked candidates for the 12h campaign

| Rank | Opportunity | Retained-positive prob | Effort | Independent of prior? | Notes |
|---|---|---|---|---|---|
| 1 | R2 — Connes-Lott Spectral Triple | medium-high | medium | yes | Standard NCG; off-diagonal Yukawa Dirac; most natural |
| 2 | R1 — Schur Complement / Alt γ | medium | medium | yes | 2-component chirality; project to 3-gen |
| 3 | R5 — Twisted Z_3 Spectral Triple | medium | medium | YES (orthogonal) | Modular; may give sibling chain not extension |
| 4 | R3 — Chamseddine-Connes (infinite-dim) | medium | high | yes | Spectral action; broader scope |
| 5 | R4 — Complex 4-dim Hermitian H | low-medium | low | yes | Extends search space; may not add primitive |
| 6 | NG-2 sharpening — zero eigenvalue must be lepton-orthogonal | high (narrow corollary, may be churn) | low | NO (corollary of L4) | Skip — likely corollary churn |
| 7 | No-go theorem on R1-R5 collectively | medium | high | YES | If R1-R5 all fail, this becomes Exit (b) |
| 8 | Staggered Dirac taste cube (NG-3 re-open) | low | high | yes | Research-level open; deferred |

## Cycle plan (initial)

**Cycle 0:** Build loop pack (this cycle — completing now).

**Cycle 1:** Special-forces 5-agent fan-out on R1-R5 in parallel.
Synthesis after all 5 return. Each agent has ~hourly compute budget.

**Cycle 2:** Execute the highest-yield route from Cycle 1 synthesis.
Produce theorem note + runner + cache. Run review-loop.

**Cycle 3:** If Cycle 2 succeeded → open review PR. Else → pivot to
next-ranked route, OR begin no-go consolidation (option 7).

**Cycle 4-N:** Continue until:
- Exit (a) — positive existence proof retained
- Exit (b) — rigorous no-go proven
- Exit (c) — corollary exhaustion
- Exit (d) — 12h runtime exhausted

## Promotion Value Gate (V1-V5) — applied at each PR-open decision

Per skill workflow §7. Before opening any PR:

- **V1:** What SPECIFIC verdict-identified obstruction does this PR close?
  - For R1-R5 spectral-triple routes: closes §5 of L4 note ("the existence of a specific framework-derived H of the required form")
- **V2:** What NEW derivation does this PR contain that the audit lane doesn't already have?
  - For R1-R5: a specific spectral-triple construction with h derived from framework primitives
- **V3:** Could the audit lane already complete this from existing retained primitives + standard math?
  - For R1-R5: NO — the spectral triple construction is non-trivial and not a textbook computation from L4 alone
- **V4:** Is the marginal content non-trivial?
  - YES — building a specific (A, H, D, γ, J) on Cl(3)/Z³ is substantive
- **V5:** Is this a one-step variant of an already-landed cycle?
  - NO — L4 characterizes the 2-dim family abstractly; this constructs a specific element of that family from primitives

## Corollary-Churn Guard

The retained Level 4 theorem already establishes:
- Anti-commuting → LCC implication
- 2-dim characterization (h ∈ R³, Σh = 0)
- Spectrum {−λ, 0, +λ}

Any cycle whose output is a one-step relabeling of this MUST be rejected
as churn. Specifically, anti-patterns to avoid:

- "Take h = (1, −1, 0); compute Koide eigenvector; verify it works"
  — this is just checking an example; not new content.
- "Apply Pattern A narrow rescope to L4's algebra"
  — creates audit row, no new derivation.
- "Sympy-exact verification of the existing primary runner's identities"
  — already done.

The legitimate science delta is FRAMEWORK DERIVATION of h, not abstract
re-characterization.
