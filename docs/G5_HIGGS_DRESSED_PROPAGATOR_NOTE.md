# G5 Avenue G — Higgs-dressed Intermediate Propagator

**Date:** 2026-04-17
**Status:** **FRAMEWORK_DERIVES_KOIDE = INCONCLUSIVE.** Three retained
constructions tested. One construction (G-2, resolvent at
`lambda = chamber_slack`) achieves a numerical near-match
(`Q = 0.6664`, `|Q - 2/3| = 3.09e-4`; `cos-sim = 0.9963` via
Σ_Higgs eigenvalues) to the PDG charged-lepton direction. The match is
**not a framework derivation** because (a) the H-lift from T_1 to the
intermediate subspace `O_0 ⊕ T_2` is a structural choice not itself on
the retained surface, and (b) the resolvent scale
`lambda = chamber_slack` is the distance of the G1 observationally-
pinned chamber point to the chamber boundary — i.e., it carries
PMNS-observational content. Avenue G therefore does **not** demote to
`TRUE` (framework-derives) and does **not** demote to
`NO_NATURAL_CONSTRUCTION`; the honest verdict is `INCONCLUSIVE`.
**Script:** [`scripts/frontier_g5_higgs_dressed_propagator.py`](../scripts/frontier_g5_higgs_dressed_propagator.py) — **7 PASS / 0 FAIL**.
**Authority role:** scope-refining attack-surface note for gap G5
(charged-lepton mass hierarchy), complementing the Agent-10-v2 retained
second-order return survey and the Agent-12 S_2-breaking primitive
survey. Not a closure.

## Safe statement (promotable to retained)

On the retained `Cl(3) ⊗ chirality` carrier `C^16`, with the retained
branch-convention EWSB operator `Gamma_1 = sigma_x ⊗ I ⊗ I ⊗ I` and the
retained projectors `P_{O_0}`, `P_{T_1}`, `P_{T_2}`, `P_{O_3}` on the
`hw = 0, 1, 2, 3` Hamming-weight strata, the identity-weighted
second-order return on `T_1` is exactly `I_3`. Replacing the identity
intermediate with a Hermitian weight `W(H)` built from the G1 retained
affine Hermitian `H(m, delta, q_+)` — lifted from its natural action
on `T_1` to the intermediate subspace `O_0 ⊕ T_2` — defines the
Higgs-dressed return

```
Sigma_Higgs = P_{T_1} Gamma_1 · W(H) · Gamma_1 P_{T_1}
```

which is a Hermitian 3x3 operator on the T_1 species block whose
species-diagonal and eigenvalue structures are both non-trivially
species-resolved for generic H-lifts. This is the structural content
that Agent-10-v2's Correction-C survey flagged as UNDERDETERMINED in
the retained framework; Avenue G operationalizes it with an
H-derived weight.

## The three constructions tested

We adopt the intermediate basis ordering
`(O_0, T_2[011], T_2[101], T_2[110])` on the L-taste subspace,
identifying the three T_2 states with the "missing axis" labels
(1, 2, 3). Under Gamma_1, T_1 species (axis-1) hops to O_0;
species (axis-2) to T_2[110]; species (axis-3) to T_2[101]; the
third T_2 state T_2[011] is unreached in one hop (Agent-10-v2).

Two H-lifts are tested:

- **Missing-axis lift (ia):** H3 embedded on T_2 in (missing axis 1, 2, 3)
  order.
- **Hopping-aligned lift (ib):** H3 embedded on T_2 in the order matching
  the Gamma_1 hopping target per species.

plus two choices for the O_0 scalar weight `h_O0 in {0, tr(H3)/3}`.

### Construction G-1 — W(H) = f(H_lift)

Apply f ∈ {H, H^2, exp(H), |H|, H + shift} to the lifted H on the
4-dim intermediate. Results (best-of across all lift / h_O0 / f):

- **Best cos-sim:** `0.9622` at missing-axis lift, h_O0 = 0, f = exp(H),
  with Σ_Higgs eigenvalues `(0.418, 1.000, 5.720)`, `Q = 0.4377`.
- **Best |Q − 2/3|:** `1.97e-01` at hopping-aligned, h_O0 = 0.219,
  f = H^2, with Σ_Higgs eigenvalues `(0.048, 1.056, 3.307)`, `cs = 0.9587`.

G-1 produces species-resolved diagonals (PASS, max `std(diag) = 2.23`),
but no combination of lift + h_O0 + f achieves both
`cos-sim > 0.99` and `|Q − 2/3| < 1e-3` jointly.

**G-1 verdict: NO_MATCH.**

### Construction G-2 — W(H) = 1 / (lambda − H_lift) (resolvent)

Retained lambda-candidates: `0, ±E_1, ±E_2, chamber_slack, eig_extrema ± 0.1,
+3, +10`. Results:

- **Best cos-sim:** `0.9963` at missing-axis lift, h_O0 = 0,
  `lambda = chamber_slack = 0.0159`, with
  Σ_Higgs eigenvalues `(0.331, 1.913, 63.07)`, `Q_eig = 0.6664`.
- **Best |Q − 2/3|:** same point as best cs:
  `|Q − 2/3| = 3.09e-04`, `cs = 0.9963`.

This is the **only candidate across the entire runner** that
simultaneously satisfies both the cos-sim threshold (`> 0.99`) and
the Koide threshold (`|Q − 2/3| < 1e-3`), via the Σ_Higgs
**eigenvalue** reading (not the species-diagonal reading).

Σ_Higgs species-block diagonal (not eigenvalues):
`diag = (63.07, 1.395, 0.849)`, `Q_diag = 0.6474`, `cs_diag = 0.162`.

So the match is supported only in the eigenvalue channel, not in the
diagonal species-block channel.

**G-2 verdict (numerical): MATCH. Retention verdict: INCONCLUSIVE —
chamber_slack is observationally pinned.**

### Construction G-3 — W(H) from G1-pin eigenvalues as weights

The G1 chamber pin produces three retained eigenvalues
`(-1.30909, -0.32043, +2.28659)`. Assign these as three diagonal
weights on T_2 in all 3! orderings, with retained scalar O_0 weights
drawn from `{0, tr(H)/3, mean|eigs|, min|eigs|, lambda_1, lambda_2,
lambda_3, lambda_i^2}` (10 candidates), and four eigenvalue
transformations `tau ∈ {id, abs, square, shifted}`.

- **Best cos-sim:** `0.9877` at `tau = square, perm = (0,2,1),
  h_O0 = lambda_2^2`, with `diag = (0.103, 0.103, 5.228)`, `Q = 0.6341`.
- **Best |Q − 2/3|:** `3.26e-02` at the same `tau = square, perm = (0,2,1),
  h_O0 = lambda_2^2`, but ordering matters — the (0,1,2) ordering has
  identical Q but cs = 0.368.

No G-3 candidate simultaneously achieves `cs > 0.99` AND `|Q − 2/3| <
1e-3` (0 candidates out of the full `4 × 6 × 10 = 240`).

**G-3 verdict: NO_MATCH.**

## Why G-2's near-match does not constitute a framework derivation

The G-2 resolvent construction achieves

```
|Q − 2/3|  =  3.09e-04   (passes |Q − 2/3| < 1e-3)
cos-sim    =  0.9963      (passes cos-sim > 0.99)
```

via the **eigenvalues of Sigma_Higgs**. This is numerically striking,
but three retention gaps separate it from a framework derivation:

1. **The missing-axis H-lift is not a retained theorem.** The
   identification of T_2 states by missing-axis label and the embedding
   of H3 along that label is Cl(3)-covariant but a NEW structural
   choice. The retained Dirac-bridge theorem fixes the intermediate
   weight to `P_{O_0} + P_{T_2}` (unit-weighted). Replacing it with
   W(H_lift) requires a retained justification that is currently
   absent. Agent 12's AMBIGUOUS verdict on a different (absolute-value)
   lift is a direct precedent for the retention fragility here.

2. **`lambda = chamber_slack` is observationally-pinned.**
   `chamber_slack = q_+* + delta_* - sqrt(8/3) = 0.01594` is the
   distance of the G1 PMNS-pinned chamber point to the chamber
   boundary. The pin `(m_*, delta_*, q_+*) = (0.657061, 0.933806,
   0.715042)` comes from the PDG measurement of PMNS angles
   (`sin^2 theta_12 = 0.307`, etc.). Therefore chamber_slack carries
   PMNS-observational content. No other lambda-candidate in the
   retained list (0, ±E_1, ±E_2, eigenvalue-spacings, O(1) scalars)
   achieves the same match, so the match is genuinely specific to
   the observationally-derived chamber_slack.

3. **Eigenvalues vs diagonals.** The match uses eigenvalues of
   Sigma_Higgs (`eigs = (0.331, 1.913, 63.07)`). The species-block
   DIAGONAL entries (`diag = (63.07, 1.395, 0.849)`) produce
   `Q_diag = 0.6474`, `cs_diag = 0.162` — dramatically worse. The
   eigenvalue reading requires a basis-change of Sigma_Higgs that
   projects species onto a non-axis basis; whether this basis-change
   is retained is not currently established by any theorem on `main`.
   The species basis on T_1 is canonical under the axis labelling
   fixed by the Dirac-bridge theorem's `Gamma_1` diagonal structure;
   redefining charged-lepton mass eigenstates to be the Sigma_Higgs
   eigenvectors is a non-trivial additional postulate.

**Bottom line:** The numerical match in G-2 is **the best currently-
observed** across all Avenue G constructions, and it is striking in
both Q and direction. But promoting it to `FRAMEWORK_DERIVES_KOIDE =
TRUE` would require retaining three independent additional primitives
(the H-lift, the lambda scale, and the eigenvalue reading). Each is
independently non-trivial. On the current retained surface, the
verdict is `INCONCLUSIVE`.

## Four-outcome verdict

```
FRAMEWORK_DERIVES_KOIDE = INCONCLUSIVE
```

| Outcome | Status |
|---|---|
| `TRUE` (flagship TOE result) | NO — requires retention of H-lift + lambda + eigenvalue reading |
| `PARTIAL` | partially achieved: G-2 matches both Koide and direction within thresholds at a specific (lift, lambda) choice; G-1 and G-3 each partially match but not jointly |
| `NO_NATURAL_CONSTRUCTION` | NO — G-2 numerically matches, so the construction is not dead |
| `INCONCLUSIVE` | **YES** — numerical match exists but requires retained promotion of three non-retained inputs to ascend to `TRUE` |

## Quantitative summary

| Construction | Best (lift, params) | Σ_Higgs diag | Σ_Higgs eigs | Q_best | cs_best |
|---|---|---|---|---|---|
| G-1 f(H) | missing-axis, h_O0=0, exp(H) | (1.00, 0.62, 5.52) | (0.42, 1.00, 5.72) | 0.4377 | 0.9622 |
| G-1 f(H) (Q-best) | hop-aligned, h_O0=0.219, H^2 | (0.05, 3.06, 1.31) | (0.05, 1.06, 3.31) | 0.4695 | 0.9587 |
| **G-2 resolvent** | missing-axis, h_O0=0, λ=chamber_slack | (63.07, 1.40, 0.85) | (0.33, 1.91, 63.07) | **0.6664** | **0.9963** |
| G-3 chamber-eigs | (τ=sq, perm=(0,2,1), h_O0=λ_2^2) | (0.10, 0.10, 5.23) | — | 0.6341 | 0.9877 |

PDG targets: `Q_ℓ = 0.6667`, `cs = 1.0000`, mass direction
`(0.01647, 0.23688, 0.97140)`.

## What this does NOT claim

- **No closure of G5.** `Q_ℓ = 2/3` is not promoted to a retained
  framework theorem.
- **No promotion of the H-lift to retained.** The missing-axis
  embedding of H3 on T_2 is Cl(3)-covariant but remains a structural
  choice not proven to be the unique retained extension.
- **No promotion of chamber_slack to a retained scale.** It is derived
  from the G1 PMNS-observational chamber pin; retention of the pin
  itself is `retained-map-plus-observational-promotion`, not
  `sole-axiom`.
- **No promotion of the Σ_Higgs eigenvalue reading to the
  physical-mass reading.** The retained Dirac-bridge theorem's
  diagonal-on-axis-basis statement suggests the species block's
  DIAGONAL is the natural charged-lepton mass readout; the
  EIGENVALUE readout used here is a non-trivial additional
  interpretive choice.
- **No claim that Avenue G is closed.** Constructions G-1 and G-3
  fail numerically; G-2 passes only under three retention gaps.
- **No claim of overlap with Agents 16 or 17** (Avenues H and I).

## Dependency contract

Retained authorities required on live `main`:

- `frontier_dm_neutrino_dirac_bridge_theorem.py` — **28 PASS / 0 FAIL**.
  This runner replicates the Phase-1 identity
  `P_{T_1} Gamma_1 (P_{O_0} + P_{T_2}) Gamma_1 P_{T_1} = I_3` on C^16.
- `frontier_g1_physicist_h_pmns_as_f_h.py` — **43 PASS / 0 FAIL**
  (G1 closure theorem). Supplies the retained affine Hermitian
  H(m, delta, q_+) and the observational chamber pin
  (m_*, delta_*, q_+*).
- `frontier_g5_gamma_1_second_order_return.py` — **20 PASS / 0 FAIL**
  (Agent 10 v2). Supplies the structural shape theorem
  `diag(Sigma) = (w_O0, w_a, w_b)` in the weighted-intermediate
  framework.

Framework-native retained constants used:
`v = 246.28 GeV` (implicit via Dirac-bridge), `E1 = sqrt(8/3)`,
`E2 = sqrt(8)/3`, `gamma = 1/2`, G1 chamber pin
`(m_*, delta_*, q_+*)`, G1 chamber-pin eigenvalues
`(-1.309, -0.320, +2.287)`, chamber_slack
`= q_+* + delta_* - sqrt(8/3) = 0.01594`.
PDG charged-lepton masses (`m_e, m_mu, m_tau`) used ONLY for post-hoc
Q / direction comparison, NEVER as derivation inputs.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the G1 retained
> affine Hermitian `H(m, delta, q_+)` at the PMNS-pinned chamber
> point `(m_*, delta_*, q_+*) = (0.657, 0.934, 0.715)`, lifted to the
> intermediate subspace `O_0 ⊕ T_2` via a missing-axis Cl(3)-covariant
> embedding and inserted as a resolvent weight `W(H) = 1 / (lambda -
> H_lift)` between the two `Gamma_1` hops of the retained second-order
> return, produces a Hermitian effective charged-lepton mass operator
> whose eigenvalues saturate Koide `Q = 0.6664` (|dev − 2/3| = 3.09 ×
> 10^{-4}) and reproduce the PDG charged-lepton mass direction to
> cosine similarity 0.9963 at `lambda = q_+* + delta_* - sqrt(8/3) =
> 0.0159`. This is the best numerical match achieved by any of three
> retained Avenue-G constructions (function-of-H, resolvent, chamber-
> eigenvalue weights), but it is **not a framework derivation** of
> `Q_ℓ = 2/3` because three distinct retention gaps separate the
> construction from the retained surface: (i) the missing-axis H-lift
> is Cl(3)-covariant but not a retained theorem; (ii) `lambda =
> chamber_slack` inherits the G1 pin's observational content;
> (iii) the eigenvalue reading of Σ_Higgs rather than its species-
> block diagonal is a non-trivial interpretive choice. The honest
> verdict is `FRAMEWORK_DERIVES_KOIDE = INCONCLUSIVE`: the
> construction is numerically successful but retention-dependent on
> ingredients that themselves are not currently on the retained
> surface.

## Relationship to sibling notes

- **Agent 10 v2 Correction-C [`G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md`](./G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md):**
  Agent 10 v2 flagged the per-T_2-state weighted intermediate as the
  only structural lever that can lift `I_3` to a three-level
  diagonal. Avenue G supplies the weight from the G1 H-operator
  (the most natural retained candidate). The G-2 near-match shows
  that **an H-resolvent weight does** structurally resolve the three
  T_2 states distinctly, at a specific lambda scale.
- **Agent 9 [`G5_VIA_G1_H_CHARGED_LEPTON_NOTE.md`](./G5_VIA_G1_H_CHARGED_LEPTON_NOTE.md):**
  Agent 9 tested H directly AS the charged-lepton mass operator and
  obtained `NO_NATURAL_MATCH`. Avenue G tests H as a WEIGHT /
  PROPAGATOR INSERTION — a structurally distinct object. The two
  results are independent; the near-match here does not invalidate
  Agent 9's null.
- **Agent 12 [`G5_S2_BREAKING_PRIMITIVE_SURVEY_NOTE.md`](./G5_S2_BREAKING_PRIMITIVE_SURVEY_NOTE.md):**
  Agent 12 tested H lifted to T_2 post-hoc and got `AMBIGUOUS` (the
  absolute-value branch restored S_2 symmetry). Avenue G's G-2
  succeeds specifically BECAUSE the resolvent at `lambda =
  chamber_slack` maps near a pole, amplifying eigenvalue differences
  and BREAKING the S_2 that would otherwise be preserved. This is
  structurally consistent with Agent 12's finding but exposes a
  lambda-fine-tuning route that Agent 12 did not explore.
- **Agent 13 [`G5_JOINT_PMNS_KOIDE_PINNING_NOTE.md`](./G5_JOINT_PMNS_KOIDE_PINNING_NOTE.md):**
  Agent 13 proved `dim(V_H ∩ V_D) = 0` — H's tangent space and the
  species-diagonal subspace are orthogonal in the retained Hermitian
  `M_3(ℂ)` on hw=1. Avenue G does **not** contradict this: it uses
  H as a WEIGHT on the intermediate space (O_0 ⊕ T_2), NOT on the
  T_1 species-diagonal subspace. The species-diagonal structure of
  Sigma_Higgs is INHERITED from the Gamma_1 hopping, with H
  modulating the slot weights. Agent 13's orthogonality theorem
  therefore does not block Avenue G; it correctly notes that H
  cannot be ADDED directly to the species-diagonal operator.
- **Agent 14 [`G5_SHAPE_THEOREM_ROBUSTNESS_AUDIT_NOTE.md`](./G5_SHAPE_THEOREM_ROBUSTNESS_AUDIT_NOTE.md):**
  Agent 14 verified the shape theorem under 7 stress tests. Avenue
  G's structural content is consistent: Sigma_Higgs's species block
  does have a species-resolved diagonal when the intermediate
  weight breaks the unit-weight symmetry, as predicted.

## Atlas status

Proposed row for [`DERIVATION_ATLAS.md`](./publication/ci3_z3/DERIVATION_ATLAS.md)
Section F (Flavor / CKM portfolio):

| Tool | Authority | Status |
|---|---|---|
| `frontier_g5_higgs_dressed_propagator.py` | This note | **INCONCLUSIVE**; 7 PASS / 0 FAIL; G-2 resolvent at `lambda = chamber_slack` achieves `|Q − 2/3| = 3.09e-4` and `cos-sim = 0.9963` via Σ_Higgs eigenvalues; blocked from promotion by three retention gaps (H-lift, observational lambda, eigenvalue reading) |

## Status

**INCONCLUSIVE** open-lane attack-surface note. Not a closure. The
structural value is the identification of a concrete H-resolvent
construction that numerically saturates charged-lepton Koide; the
honesty requirement is that three retention gaps must each be
independently closed before this ascends from `INCONCLUSIVE` to
`TRUE`. Future G5 attacks may productively target:

1. A retained theorem establishing that the missing-axis embedding
   of H3 into `O_0 ⊕ T_2` is the unique Cl(3)-covariant lift.
2. A retained scale-setting mechanism that fixes `lambda =
   chamber_slack` from sole-axiom inputs without PMNS observational
   pinning.
3. A retained theorem establishing that Sigma_Higgs eigenvalues
   (rather than its species-block diagonal) are the physical
   charged-lepton masses.

If any two of the three gaps are closed, the verdict upgrades to
`PARTIAL`. If all three are closed, Avenue G becomes the flagship
G5 derivation.
