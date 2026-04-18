# Review Note: `claude/angry-chatelet-2dc78c`

## Status (revised 2026-04-17 after new-science-path commit)

- Original verdict (4e517dae): **do not merge as-is** — the branch promoted
  a still-open identification surface as if it were a retained theorem
  output.
- New-science-path response: separated the claim into three layers
  (Layer 1 retained structural identities + Layer 2 proposed new
  retained primitive P-AT + Layer 3 bounded quantitative readout), and
  introduced an explicit new framework primitive that, if accepted,
  derives the bridges at leading order from retained atlas projector
  weights. **P-AT is labeled transparently as a new framework proposal
  with review pending**, not as a derivation from pre-existing retained
  primitives.

## Response To The Original Review Blockers

### P1.a — "Bridge theorem promotes an open identification surface as retained output"

Fixed by restructuring the authority note into Layer 1 + Layer 2 + Layer 3.

- **Layer 1 (retained on `main`, unconditional)** is narrowly the
  structural identities SI1-SI3:
  - SI1: `sqrt(6)` in `|V_{cb}|_{atlas}` = retained Ward Clebsch-Gordan
    `sqrt(N_c · N_{iso})` on `Q_L`.
  - SI2: GST exponent `1/2 = 1/n_{pair}`.
  - SI3: `5/6` bridge exponent = retained atlas `1+5`
    orthogonal-complement projector weight on the six-state `Q_L` block
    (not the SU(3) Casimir combination).
- **Layer 2 (proposed new retained primitive P-AT, framework-level review
  pending)** is what *does* the bridge-forcing work: the down-type `hw=1`
  NNI mass matrix has atlas-projector-weighted `(2,3)` off-diagonal
  `M_d(2,3) = m_s^(5/6) · m_b^(1/6)`. Under P-AT, GST and the `5/6`
  bridge are leading-order exact hierarchical identities, and combining
  with the retained CKM atlas gives the identification surface
  `m_d/m_s = \alpha_s(v)/n_{pair}`, `m_s/m_b = [\alpha_s(v)/\sqrt{n_{quark}}]^{6/5}`
  as framework output. **P-AT is explicitly labeled a new framework
  proposal, not a derivation from pre-existing retained primitives.**
- **Layer 3 (bounded quantitative readout)** is unchanged.

The original overpromotion was conflating Layer 1 (which is retained) and
Layer 2 (which is a framework-level proposal that needs review). The
revised note separates them explicitly.

### P1.b — "Primary runner certifies the conditional algebra, not the still-open forcing step"

Fixed by restructuring the runner into three labeled layers
(`RETAINED`, `P-AT`, `BOUNDED`) that match the authority note:

- `RETAINED PASS` checks certify SI1-SI3 (Layer 1) on structural
  constants alone — no mass-matrix assumptions.
- `P-AT PASS` checks numerically diagonalize the proposed atlas-projector-
  weighted texture at a sequence of epsilon-scaled hierarchies
  `(m_d/m_s, m_s/m_b) = (\epsilon, \epsilon)` for
  `\epsilon \in \{10^{-1}, ..., 10^{-6}\}`, confirming:
  - `|V_{us}|/\sqrt{m_d/m_s} \to 1` as `\epsilon \to 0` (T1: GST
    leading-order exact under P-AT);
  - `|V_{cb}|/(m_s/m_b)^{5/6} \to 1` as `\epsilon \to 0` (T2: `5/6`
    bridge leading-order exact under P-AT);
  - convergence is monotone in `\epsilon`.
  These checks certify the **hierarchical-limit exactness of the bridges
  under the proposed primitive**, explicitly separate from the retained
  Layer 1 content.
- `BOUNDED PASS` checks the quantitative mass-ratio readout against PDG
  threshold-local self-scale.

Current result: `RETAINED PASS=16`, `P-AT PASS=9`, `BOUNDED PASS=3`,
`FAIL=0`.

### P2 — "Package truth surface propagates the same overpromotion"

Fixed by updating all publication-surface rows to advertise the three-
layer status explicitly:

- **Retained** (structural identities SI1-SI3, unconditional on `main`).
- **Proposed new retained primitive** (P-AT, framework-level review
  pending; derives bridges at leading order).
- **Bounded quantitative** (mass-ratio readout).

Surfaces updated:
`PUBLICATION_MATRIX.md`, `CLAIMS_TABLE.md`, `DERIVATION_ATLAS.md`,
`DERIVATION_VALIDATION_MAP.md`, `FULL_CLAIM_LEDGER.md`,
`QUANTITATIVE_SUMMARY_TABLE.md`, `RESULTS_INDEX.md`,
`PREDICTION_SURFACE_2026-04-15.md`, `INPUTS_AND_QUALIFIERS_NOTE.md`,
`EXTERNAL_REVIEWER_GUIDE.md`, `ARXIV_DRAFT.md`, package `README.md`,
repo `README.md`. Downstream authority notes (`DOWN_TYPE_...`,
`CKM_FIVE_SIXTHS_...`, `CKM_FROM_MASS_HIERARCHY_...`) similarly
three-layer the status and cross-reference the P-AT proposal.

## The New-Science Content

The new primitive P-AT is sharp and testable:

**P-AT (Atlas-Projector-Weighted Mass-Matrix Texture).** On the retained
`hw=1` down-type mass matrix in the axis basis `(X_1, X_2, X_3)`, the
real symmetric mass matrix has the NNI-zero + atlas-projector-weighted
`(2,3)` texture

```
M_d(1,1) = m_d
M_d(2,2) = m_s
M_d(3,3) = m_b
M_d(1,2) = sqrt(m_d · m_s)                [NNI geometric mean]
M_d(2,3) = m_s^(5/6) · m_b^(1/6)          [atlas-projector-weighted]
M_d(1,3) = 0                              [NNI texture zero]
```

The new content is specifically the `(2,3)` off-diagonal: it weights the
**lighter** generation `m_s` by the retained CP-odd `5/6` atlas projector
weight and the **heavier** generation `m_b` by the retained CP-even `1/6`
atlas projector weight. The `(1,2)` and `(1,3)` entries are standard NNI
content and are not novel.

**Motivation (structural, not a pre-existing derivation):** the atlas
bilinear tensor carrier `K_R` on `Q_L` decomposes into a CP-even singlet
(weight `1/6`) and CP-odd orthogonal complement (weight `5/6`). P-AT
asserts that the bridge-inducing `(2,3)` mass-matrix element inherits
the same atlas-projector weighting, lighter-generation on CP-odd and
heavier-generation on CP-even.

**Mergeability:** this is a framework-level proposal with transparent
labeling and a numerically-verified hierarchical limit. It does not
claim P-AT is already retained; it proposes P-AT and derives the
leading-order bridges under P-AT. Acceptance of P-AT as retained is a
framework-level decision outside this commit's scope.

## Named Open Work

- **Operator-theoretic derivation of P-AT from `K_R`.** An explicit
  framework-internal derivation of the atlas-projector-weighted `(2,3)`
  off-diagonal texture from an operator argument on the atlas bilinear
  tensor carrier `K_R` on `Q_L` would upgrade P-AT from proposed to
  retained. Currently P-AT is structurally motivated but not derived.
- **Sub-leading-order corrections under P-AT.** The bridges are exact
  only at leading order in the hierarchical limit; the next-to-leading
  corrections are `O(m_d/m_s)` for GST and `O(m_s/m_b)` for the `5/6`
  bridge. A systematic NLO program is named open.
- **Scale-selection theorem for the threshold-local comparator.**
  Unchanged from the original review.

## Bottom Line

The original review correctly identified an overpromotion. The revised
branch addresses it by separating retained structural identities (Layer
1) from the proposed new retained primitive P-AT (Layer 2) that actually
carries the bridge-forcing step. P-AT is labeled transparently as a new
framework-level proposal with review pending, not as a derivation from
pre-existing retained primitives. The runner, authority note, and all
publication surfaces reflect the three-layer status consistently.

The lane is now reviewable as **retained structural identities + a
clearly-labeled new framework proposal** rather than as an unconditional
retained bridge theorem. That is the honest new-science path: propose
the missing primitive, derive the consequences, label it as new, and
open it for framework-level review.
