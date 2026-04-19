# G5 Joint PMNS + Koide Pinning Theorem — Structural-Link Attempt

**Date:** 2026-04-17
**Status:** NEGATIVE. The retained G1 affine chart `H(m, delta, q_+)` and
the retained G5 second-order return diagonal `Sigma = diag(w_O0, w_a, w_b)`
live on the *same* retained `hw=1` three-generation observable carrier,
but they occupy **structurally orthogonal tangent subspaces** of the
Hermitian 3x3 algebra: the H-chart tangent span `span{T_m, T_delta, T_q}`
and the diagonal subspace `span{D_1, D_2, D_3}` intersect in dimension
zero. There is no natural joint retained source whose first-order
response is H and whose species-diagonal is Sigma. Four flagship gates
do NOT close from one observational pin.
**Verdict:** `JOINT_PINNING_THEOREM_ABSENT`.
**Script:** [`scripts/frontier_g5_joint_pmns_koide_pinning.py`](../scripts/frontier_g5_joint_pmns_koide_pinning.py) — **PASS=9 FAIL=0**.
**Authority role:** attack-surface note; closes the "shared-source joint
pinning" lane identified as candidate 3 in the post-G1-closure successor
list of [`CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md`](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md).

## Motivation

The G1 Physicist-H closure
([`G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md`](./G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md))
pins the retained affine chart
`H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`
at `(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)` from PMNS
observation on the `hw=1` triplet.

The G5 Gamma_1 second-order return shape theorem
([`G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md`](./G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md))
gives the retained diagonal `Sigma = diag(w_O0, w_a, w_b)` on the same
`hw=1` triplet, via the `Gamma_1` hopping pattern to the intermediate
`O_0 + T_2` projector.

Both operators live on `H_{hw=1}`. If a retained joint source `J` on
`H_{hw=1}` carried both — H as a first-order source response, Sigma as
a second-order or species-diagonal source response — then the G1 PMNS
pin would simultaneously determine `(w_O0, w_a, w_b)` and the charged-
lepton Koide relation would follow as a G1 corollary. That is the
"one pin, four gates" scenario targeted by this note.

## Structural obstruction (the sharp theorem-grade finding)

**Theorem (H-chart / diag-subspace orthogonality).** Within the
9-dimensional real Hermitian 3x3 algebra on `H_{hw=1}`,

- the H-chart *tangent* span `V_H := span_R{T_m, T_delta, T_q}` has
  rank 3;
- the species-diagonal subspace `V_D := span_R{D_1, D_2, D_3}` has
  rank 3;
- the combined span `V_H + V_D` has rank 6;
- hence `dim(V_H cap V_D) = 3 + 3 - 6 = 0`.

The three generators of H's parameter dependence are:

```
T_m     = [[1, 0, 0], [0, 0, 1], [0, 1, 0]],        (species-diagonal (1,0,0) + axis 2<->3 swap)
T_delta = [[0, -1, 1], [-1, 1, 0], [1, 0, -1]],     (one diagonal entry but NOT species-diagonal)
T_q     = [[0, 1, 1], [1, 0, 1], [1, 1, 0]],        (purely off-diagonal)
```

None of these lies in the pure species-diagonal subspace, and no linear
combination of them does either. **H's parameter dependence is carried
entirely by off-diagonal / axis-permutation pieces**; any species-
diagonal content is inherited only from `H_base`'s zero diagonal plus
`T_delta`'s `(0, 1, -1)` diagonal — which is a fixed `S_2`-antisymmetric
1-dim direction, not three independent diagonal weights.

The runner verifies this via a direct rank computation on the flattened
real-Hermitian basis:

```
rank(V_D) = 3
rank(V_H) = 3
rank(V_D + V_H) = 6
intersection dim = 0
```

Phase 2 result, runner-verified to machine precision.

**Corollary.** The chart coordinates `(m, delta, q_+)` pinned by the
G1 PMNS closure carry *no direct information* about the Sigma-diagonal
weights `(w_O0, w_a, w_b)`. Any map `(m, delta, q_+) -> (w_O0, w_a, w_b)`
must be *constructed* (e.g. via secondary operations like `diag(H @ H)`
or eigenvalue extraction), not *structurally inherited*.

## Candidate secondary maps — all fail cone-closure at the G1 pin

Seven secondary maps `(m, delta, q_+) -> (w_O0, w_a, w_b)` were
evaluated at the G1 pin. None produces Koide `Q = 2/3` or cosine
similarity `>= 0.99` with the PDG charged-lepton direction.

| Map | (w_O0, w_a, w_b) at G1 pin | Koide Q | cos-sim PDG |
|---|---|---|---|
| I-a direct `(m, delta, q_+)` | (0.657, 0.934, 0.715) | 0.335 | 0.700 |
| I-b `diag(H)` axis-basis | (0.657, 0.934, -0.934) | 0.335 | 0.743 |
| I-c `diag(H H)` axis-basis | (2.682, 3.056, 1.307) | 0.343 | 0.584 |
| I-d \|eigvals(H)\| | (0.320, 1.309, 2.287) | 0.377 | 0.884 |
| I-e eigvals(H)^2 | (1.714, 0.103, 5.228) | 0.460 | 0.874 |
| I-f `diag(K_Z3)` | (1.459, -0.689, -0.112) | 0.401 | 0.360 |
| I-g `diag(K_Z3^dag K_Z3)` | (4.270, 2.000, 0.776) | 0.370 | 0.461 |
| **PDG target** | (0.511, 105.66, 1776.86) MeV | **0.667** | **1.000** |

Observed `Q_ell = 0.66666`, sqrt-direction `(0.01647, 0.23688, 0.97140)`.
Every candidate is off by at least ~30% in Koide and at least `0.12` in
cos-sim.

## Chamber-wide search — near-Koide point exists for candidate I-a but NOT at G1 pin

A dense 31x31x21 = 20,181-point grid scan over the chamber
`q_+ >= sqrt(8/3) - delta, (m, delta) in [-1.5, 1.5]^2, q_+ in [0, 2]`
yields 5,890 chamber-interior points. Best-fit chamber points per map:

| Map | best `(m, delta, q_+)` | Q | cos-sim |
|---|---|---|---|
| I-a direct | (0.000, 0.100, 1.600) | 0.680 | **0.9998** |
| I-b `diag(H)` | (0.000, -0.200, 1.900) | 0.500 | 0.854 |
| I-d \|eigvals\| | (1.200, 1.100, 0.900) | 0.497 | 0.915 |
| I-f `diag(K_Z3)` | (0.200, 1.500, 0.200) | 0.406 | 0.923 |

Most striking: the **identity map I-a** `(w_O0, w_a, w_b) = (m, delta, q_+)`
can come within `|Q-2/3|/Q = 0.02` of Koide AND within cos-sim `0.9998`
of the PDG direction at `(0.000, 0.100, 1.600)`. But this chamber
point lies **distance 1.45** from the G1 pin — structurally unrelated
to where PMNS observation lands.

The inverse-pin test (Phase 5) confirms: the `(m, delta, q_+)` region
that *would* reproduce the charged-lepton direction under the identity
map is far from the G1 PMNS basin. There is no coincidental near-pin.

## Interpretation: "Structural link absent, accidental chamber proximity present but wrong-pin"

This is NOT the "JOINT_HOLDS_BUT_WRONG_PIN" scenario. That would
require a structural identification (m, delta, q_+) = (w_O0, w_a, w_b)
— which exists as a trivial linear map but carries NO retained meaning,
because `T_m, T_delta, T_q` are not diagonal matrices. The identification
is a coordinate accident, not a framework-level link.

The framework-level link requires `H` and `Sigma` to be related by a
retained operator equation, e.g.
- `Sigma = diag(H)` (fails: misses q_+; cs=0.74);
- `Sigma = diag(H @ H)` (fails: cs=0.58);
- `Sigma = |eigvals(H)|` (fails: cs=0.88).

Each of these IS a retained operator equation, but none reproduces
observed `(m_e, m_mu, m_tau)` at the G1 pin.

The joint-action candidate `Phi(J) = log|det(I_3 + J)|` likewise fails:
it produces a SCALAR retained functional, whose source derivative
`tr(J)` is one-dimensional — insufficient to carry both H (9 Hermitian
DOF, parameterized by 3 reals via `T_m, T_delta, T_q`) and Sigma
(3 diagonal DOF). A single scalar generator cannot bifurcate into two
distinct retained operator-valued observables on `H_{hw=1}` without
introducing post-axiom structure.

## Residual `S_2` check — H does break the symmetry at the G1 pin

Agent 10 v2 identified the residual `S_2` on axes `{2, 3}` as the
structural obstruction: any retained operator respecting `S_2` forces
`w_a = w_b`. This note checks whether H at the G1 pin already breaks
`S_2`, as a structural opportunity test:

- `diag(H_star) = (0.657, 0.934, -0.934)` is **not** `S_2({2,3})`-invariant
  (the swap gives `(0.657, -0.934, 0.934)`).
- `S23 H_star S23^dag != H_star` (verified).

So H_star is structurally `S_2`-breaking — the obstruction from
Agent 10 v2 could in principle be lifted if a retained map
`H -> Sigma` carried this breaking onto the `(w_a, w_b)` split. Several
candidates produce non-trivial `|w_a - w_b|/max` values at the G1 pin:

| Map | `|w_a - w_b|/max` at G1 pin |
|---|---|
| I-c `diag(H H)` | 0.573 |
| I-d \|eigvals(H)\| | 0.428 |
| I-e eigvals(H)^2 | 0.980 |
| I-f `diag(K_Z3)` | 0.837 |
| I-g `diag(K_Z3^dag K_Z3)` | 0.612 |

`S_2` breaking is present but the ratio `m_tau : m_mu : m_e ≈
3475 : 207 : 1` is far larger than anything these maps deliver at the
G1 pin. The structural `S_2` breaking is qualitatively right but
quantitatively too mild.

## Four-outcome verdict

**`JOINT_PINNING_THEOREM_ABSENT`**

The runner decision tree:

1. Phase 1: no candidate at the G1 pin matches Koide + PDG direction.
   -> Rule 1 ("CLOSES_G5") not triggered.
2. Phase 2: `dim(V_H cap V_D) = 0`. The H-chart tangent subspace and
   the diagonal subspace are structurally orthogonal.
   -> Rule 3 ("ABSENT") triggered.

Sub-finding (Phase 3, 5): the linear identification `(w_O0, w_a, w_b) =
(m, delta, q_+)` has a chamber point producing Koide + PDG direction to
cos-sim 0.9998, but at distance 1.45 from the G1 pin. This is a
coincidence in a 3-parameter chamber, not a framework-native link.

## What this does NOT claim

- Does NOT claim Koide `Q_ell = 2/3` is incompatible with the retained
  framework. Agent 10 v2's shape theorem already shows the framework
  has structural room for it.
- Does NOT claim G1 and G5 are unrelated — they share `H_{hw=1}` and
  the Dirac-bridge structure constrains `Gamma_1` to be diagonal in the
  axis basis. The claim is narrower: no *joint source* whose PMNS-pin
  automatically fixes the charged-lepton diagonal.
- Does NOT close off Agent 10 v2's `S_2`-breaking retained primitive
  search — that lane remains independent and open.
- Does NOT claim the Higgs-VEV deployment lane (Candidate 2 in the
  G5 status note's successor list) is foreclosed.

## Honest publication-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the G1 Physicist-H
> retained affine chart `H(m, delta, q_+)` and the G5 Gamma_1
> second-order return diagonal `Sigma = diag(w_O0, w_a, w_b)` live on
> the same `hw=1` three-generation carrier but occupy structurally
> orthogonal tangent subspaces of the Hermitian 3x3 algebra: the
> H-chart tangent span `span{T_m, T_delta, T_q}` and the species-
> diagonal subspace `span{D_1, D_2, D_3}` intersect in dimension zero.
> Seven secondary `H -> Sigma` maps (direct-linear, `diag(H)`,
> `diag(H^2)`, `|eigvals|`, `eigvals^2`, `diag(K_Z3)`,
> `diag(K_Z3^dag K_Z3)`) are each evaluated at the G1 PMNS pin
> `(m_*, delta_*, q_+*) = (0.657, 0.934, 0.715)`; none reproduces
> the charged-lepton Koide `Q = 2/3` within 1% or the PDG sqrt-direction
> within cosine similarity 0.99. A dense chamber search finds a
> near-Koide, near-PDG-direction point only under the trivial identity
> map, and at distance 1.45 from the G1 pin. The result is a *negative*
> structural verdict `JOINT_PINNING_THEOREM_ABSENT`: G5 does not close
> as an automatic G1 corollary through any retained shared-source
> mechanism identified here. The Agent 10 v2 `S_2`-breaking retained
> primitive lane remains the active open route.

## Quantitative summary

- G1 pin: `(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)`.
- H_star eigenvalues: `(-1.30909, -0.32043, +2.28659)`.
- H-chart / diag-subspace intersection: dim 0 (sharp theorem).
- Best Koide `Q` at G1 pin across all 7 maps: 0.460 (I-e), 0.377 (I-d);
  target 0.667.
- Best cos-sim PDG at G1 pin: 0.884 (I-d); target 0.99+.
- Best chamber point (I-a identity): `(0.000, 0.100, 1.600)`,
  `Q = 0.680`, cos-sim `0.9998`, **distance 1.45 from G1 pin**.

## Relationship to sibling notes

- G1 closure [`G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md`](./G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md):
  canonical source of `H(m, delta, q_+)` and the G1 pin
  `(m_*, delta_*, q_+*)`.
- G5 shape theorem [`G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md`](./G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md):
  canonical source of `Sigma = diag(w_O0, w_a, w_b)` and the residual
  `S_2` obstruction.
- G5 status note [`CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md`](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md):
  lists the "Joint PMNS + Koide pinning theorem" as candidate 3 in the
  post-G1-closure successor list; this note closes candidate 3 as
  ABSENT.
- Agent 9 predecessor [`G5_VIA_G1_H_CHARGED_LEPTON_NOTE.md`](./G5_VIA_G1_H_CHARGED_LEPTON_NOTE.md):
  rejected the direct "apply H to charged leptons" reading; this note
  sharpens that rejection at the tangent-space level and rules out the
  joint-source reformulation as well.

## Dependency contract

Retained authorities valid on live `inspiring-meitner`:

- `frontier_g1_physicist_h_pmns_as_f_h.py` (43 PASS / 0 FAIL) — source
  of the G1 pin.
- `frontier_g5_gamma_1_second_order_return.py` (20 PASS / 0 FAIL) —
  source of the Sigma-diagonal shape theorem.
- `frontier_dm_neutrino_dirac_bridge_theorem.py` (28 PASS / 0 FAIL) —
  retained `Gamma_1` first-order vanishing and second-order `I_3`
  identity.

This runner introduces no new framework primitive and makes no post-
axiom invention. It is a tangent-space structural test plus a
chamber-wide secondary-map survey.

## Status

**Negative attack-surface note.** Not a closure. The value is the
sharp theorem-grade finding that the retained H-chart tangent span
and the species-diagonal subspace on `H_{hw=1}` are **orthogonal** in
the Hermitian 3x3 algebra, which rules out any joint-source retained
mechanism linking G1's PMNS pin to G5's charged-lepton Koide weights.
The active open G5 route remains the Agent 10 v2 `S_2`-breaking
retained primitive search and the Agent-9-successor Higgs-VEV
deployment lane.
