# G5 / Γ_1 Second-Order Return — Hierarchy-Breaking Correction Survey

**Date:** 2026-04-17
**Status:** EXACT symbolic construction of the retained second-order return on `T_1` plus four independent hierarchy-breaking correction candidates. Verdict: **GAMMA_1_SECOND_ORDER_UNDERDETERMINED**. The retained `Cl(3)` + chirality carrier admits exactly one structural mechanism (Correction-C: per-intermediate-state weighted propagator) that can in principle lift the leading `I_3` degeneracy, but the retained framework does not currently carry a primitive that assigns the three required distinct weights, and the closest retained approximation (hw-staggered propagator) is structurally 2+1 degenerate and cannot match the observed `(m_e, m_μ, m_τ)` direction. Corrections A, B, D are structurally species-blind on the retained `hw=1` triplet.
**Script:** [`scripts/frontier_g5_gamma_1_second_order_return.py`](../scripts/frontier_g5_gamma_1_second_order_return.py) — **20 PASS / 0 FAIL**.
**Authority role:** scope-refining attack-surface note for gap G5 (charged-lepton mass hierarchy). Extends the reconnaissance note [`G5_GAMMA_1_RECONNAISSANCE_NOTE_2026-04-17.md`](./G5_GAMMA_1_RECONNAISSANCE_NOTE_2026-04-17.md) and the eight-agent consolidated status note [`CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md`](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md) from a structural-primitive view to a constructive-perturbation view on the exact Dirac-bridge `T_1` second-order return. Not a closure.

## Safe statement (promotable to retained)

On the retained `Cl(3) ⊗ chirality` carrier `C^16`, with the retained
branch-convention EWSB operator `Γ_1 = σ_x ⊗ I ⊗ I ⊗ I` and the retained
projectors `P_{O_0}, P_{T_1}, P_{T_2}, P_{O_3}` on the `hw = 0, 1, 2, 3`
Hamming-weight strata, the second-order effective charged-lepton mass
operator on the `hw=1` generation triplet is identity:

```
Σ(I) = P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} = I_3
```

(first-order vanishing `P_{T_1} Γ_1 P_{T_1} = 0` and second-order return
on `O_0 + T_2` are both PASS-verified by
`frontier_dm_neutrino_dirac_bridge_theorem.py` on live `main`, and
re-verified independently by this runner). This is the canonical
consistency check.

Under the retained `Γ_1` hopping structure, the three `T_1` species
connect to the following intermediate states:

| `T_1` species | Spatial label | `Γ_1`-reached intermediate |
|---|---|---|
| 1 | `(1,0,0)` | `(0,0,0)` = `O_0` |
| 2 | `(0,1,0)` | `(1,1,0)` ∈ `T_2` |
| 3 | `(0,0,1)` | `(1,0,1)` ∈ `T_2` |

So the second-order species-diagonal mass operator, under an arbitrary
weight assignment `w_O0` on `O_0` and per-T_2-state weights `w_a, w_b, w_c`
for `T_2 = {(1,1,0), (1,0,1), (0,1,1)}`, is exactly

```
diag(Σ) = (w_O0, w_a, w_b)
```

(the third `T_2` state `(0,1,1)` is unreachable from `T_1` in one `Γ_1`
hop and does not contribute at this order).

**Safe theorem:** the retained second-order return on `T_1`, as a linear
functional of the intermediate projector, is an affine species-diagonal
map `w ↦ diag(w_O0, w_a, w_b)` with the first `T_2` state irrelevant.
This is a structural identity, verified by the runner to PASS.

## Phase 1 — exact consistency check (PASS 9 / 9)

- `Γ_1` Hermitian, `Γ_1² = I_16`, `{Γ_1, γ_5} = 0`, `P_L Γ_1 P_L = P_R Γ_1 P_R = 0`.
- `P_{T_1} Γ_1 P_{T_1} = 0` (first-order vanishing).
- `P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} = I_6` on the full taste-doubled `T_1`.
- Restricted to the `L`-taste species basis: exactly `I_3`.
- `O_3` contributes nothing: `P_{T_1} Γ_1 (P_{O_0} + P_{T_2} + P_{O_3}) Γ_1 P_{T_1} = P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1}`.

This matches the Dirac-bridge theorem exactly; the runner is re-deriving,
not re-asserting, its content.

## Phase 2 — four hierarchy-breaking correction candidates

### Correction-A — Higgs fluctuations `φ = e_1 + ε` around the EWSB axis

Replace `Γ_1` with `M(φ) = Γ_1 + ε_2 Γ_2 + ε_3 Γ_3` and compute the
perturbed second-order return. Result:

```
diag(Σ(e_1 + ε) − I_3) = (ε²_1 + ε²_2 + ε²_3) × (1, 1, 1)  (to all tested orders)
```

The correction is a **global scalar** — every diagonal entry receives the
same increment. `std(diag) = 0` to machine precision at `ε = (0, 0.1, 0.1)`,
`ε = (0, 0.001, 0.001)`, and every intermediate scale. At `O(ε)`:
`P_{T_1} (ε Γ_2) (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} + h.c. = 0`, so the cross
term vanishes identically. At `O(ε²)`, the diagonal shift is
`|ε|² I_3`. **Verdict: REJECT.** The `V_sel = 32 Σ_{i<j} φ_i² φ_j²` Hessian
at `e_1` is species-democratic between `φ_2, φ_3`, consistent with the
all-species-equal correction.

### Correction-B — iterated higher-order returns

Compute `P_{T_1} [Γ_1 (P_{O_0} + P_{T_2}) Γ_1]^n P_{T_1}` for `n = 1, 2, 3, 4`
and also the variant with `P_{O_0} + P_{T_2} + P_{O_3}` intermediate.
Result: every iterated return is exactly `I_3`, with `std(diag) = 0` to
machine precision at every `n`. The iterated operator `K = Γ_1 P_{not T_1} Γ_1`
has the structural property `P_{T_1} K P_{T_1} = I_3`, so `[K P_{T_1}]^n = I_3`.
**Verdict: REJECT.** Higher-order returns carry no new species information.

### Correction-C — weighted intermediate propagator

Parametrize the retained intermediate as
`P_mid(w) = w_O0 P_{O_0} + Σ_j w_{T_2,j} P_{T_2,j}` and compute
`P_{T_1} Γ_1 P_mid(w) Γ_1 P_{T_1}`. Verified numerically:

```
diag(Σ) = (w_O0, w_{T_2,(1,1,0)}, w_{T_2,(1,0,1)})
```

at arbitrary weights (test at `(0.37, 1.19, 2.31, 0.73)` reproduced
exactly). This mechanism **structurally can** lift `I_3` to any
desired diagonal — including `(m_e, m_μ, m_τ)` — by setting the
three weights proportional to the target masses.

However: **no retained primitive on `main` assigns per-T_2-state
weights**. The retained framework's closest available scheme is the
hw-staggered propagator
`w(hw) = 1 / (m_0 + hw · Δ)` — on-site mass `m_0` at `hw=0` and a
common `hw=2` weight. That gives `diag(Σ) = (w_0, w_2, w_2)`, which is
**2+1 degenerate** and cannot match the observed non-degenerate direction
`(0.0165, 0.2369, 0.9713)`. Scan over `(w_0, w_2) ∈ [10⁻⁴, 10] × [10⁻⁴, 10]`
gives best cos-similarity `0.8545`, well below the `0.99` threshold for a
plausible match.

**Verdict: UNDERDETERMINED.** Unconstrained per-T_2 weights match any
target (they are the target, by construction); the retained staggered
weights cannot match. Closing G5 on this lane requires identifying a
retained `C^16` operator that assigns the three `T_2` states
`(1,1,0), (1,0,1), (0,1,1)` to three distinct scalar weights.

### Correction-D — retained mass insertion on `T_1`

Insert a retained Cl(3) bilinear between `(P_{O_0} + P_{T_2})` and the
second `Γ_1`:
```
P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) M_insert Γ_1 P_{T_1} + h.c.
```
Tested `M_insert ∈ { γ_5, Ξ_5, Γ_1 Γ_2 Γ_3, Γ_2 Γ_3 }`: every retained
bilinear insertion gives species block `= 0`. Direct species-block
restriction of all retained Cl(3) generators (`Γ_i, γ_5, Ξ_5, Γ_i Γ_j,
Γ_1 Γ_2 Γ_3`): zero diagonal on `T_1` for all (with occasional off-diagonal
entries from `Γ_1 Γ_2`, which do not contribute to the species-diagonal
mass). **Verdict: REJECT.** The retained spatial Clifford carries the
species label via the **HW-basis projectors**, not via any algebraic
operator — consistent with the "taste ⊗ species carrier orthogonality"
theorem established by Agents 7 and 8.

## Phase 3 — Koide / direction / ratio comparison

| Correction | diag(Σ) | Koide Q | cos-sim to PDG | Status |
|---|---|---|---|---|
| A (Higgs fluctuation) | `(1, 1, 1)` | 0.3333 | 0.7071 | degenerate |
| B (iterated returns) | `(1, 1, 1)` | 0.3333 | 0.7071 | degenerate |
| C (hw-staggered retained) best | `(0.00010, 0.15085, 0.15085)` | 0.4875 | 0.8545 | 2+1 degenerate |
| D (mass insertion) | `(1, 1, 1)` | 0.3333 | 0.7071 | degenerate |
| **PDG target** | `(0.511, 105.66, 1776.86)` MeV | **0.6667** | **1.0000** | — |

Observed charged-lepton Koide: `Q_ℓ = 0.66666` (PDG, `|dev − 2/3| < 0.001%`),
sqrt-direction `(0.01647, 0.23688, 0.97140)`. None of the retained
corrections matches at either Koide or direction level.

## Four-outcome verdict

**`GAMMA_1_SECOND_ORDER_UNDERDETERMINED`**

The retained `Γ_1` second-order return on `T_1` is identically `I_3`,
and four independent retained correction mechanisms on the retained
`C^16` carrier are:

- Correction-A (Higgs axis fluctuation): **REJECT**, species-democratic at every order.
- Correction-B (iterated returns): **REJECT**, proportional to `I_3` at every iteration.
- Correction-C (weighted intermediate): **UNDERDETERMINED**, mechanism exists but the per-T_2-state weighting primitive is absent from retained `main`; the closest retained scheme is structurally 2+1 degenerate.
- Correction-D (algebraic mass insertion): **REJECT**, no retained Cl(3) bilinear carries a non-trivial species-diagonal block on `T_1`.

The convergent architectural conclusion: **the retained `Γ_1` algebra on
`hw=1` admits Koide-compatible hierarchies, but does not uniquely fix
one**. Closing G5 through this route requires a new retained primitive —
specifically, an operator on `C^16` that resolves the three individual
`T_2` states into three distinct scalar weights aligned with the physical
`(m_e, m_μ, m_τ)` direction.

## What this does NOT claim

- No closure of G5. `Q_ℓ = 2/3` remains UNRETAINED at the theorem level.
- No promotion of any result to retained-theorem status.
- No new retained framework axiom or operator.
- No claim that Correction-C is the *only* route to G5 closure outside
  retained `main`; only that it is the only one of the four structural
  candidates surveyed here that is not dead.
- No quantitative prediction for `(m_e, m_μ, m_τ)`.

## Relationship to sibling notes

- **Reconnaissance note [`G5_GAMMA_1_RECONNAISSANCE_NOTE_2026-04-17.md`](./G5_GAMMA_1_RECONNAISSANCE_NOTE_2026-04-17.md):** this note executes the exact resumed Agent-10 brief, Phases 1-4. The Phase-1 consistency check is the quantitative realization of the reconnaissance note's "Outstanding question 1".
- **Dirac-bridge theorem [`DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md`](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md):** canonical authority for `Γ_1`, the first-order vanishing, and the second-order `I_3` identity; the runner here re-derives those PASS items as Phase 1.
- **G1 closure [`G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md`](./G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md):** G1's retained `H(m, δ, q_+)` acts on the **neutrino** hw=1 structure. G1's `U_e = I_3` bridge condition forces the charged-lepton effective operator to be diagonal in the axis basis. This note confirms that the eigenvalues of that diagonal operator — the physical `(m_e, m_μ, m_τ)` — are inputs to the G1 bridge, not outputs, and identifies which retained correction channel could in principle supply them (Correction-C).
- **G5 consolidated status note [`CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md`](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md):** this runner operationalizes the "post-G1-closure open question 1" (application of G1's retained H to the charged-lepton sector) in the sharpened second-order-return form. The UNDERDETERMINED verdict here is consistent with the convergent eight-agent architectural conclusion that "every retained operator on `hw=1` built from retained algebraic or anomaly structure is species-diagonal unless it involves a Higgs/Yukawa VEV insertion", and refines it: even the Higgs/Yukawa route (Correction-A) fails when the intermediate is the canonical retained `P_{O_0} + P_{T_2}`.

## What the eight-agent attack surface looked like before, and what this adds

Agents 1-8 closed six species-blindness null hypotheses on the retained
`hw=1` block-level source-response kernel. This runner is the first to
operationalize the **Dirac-bridge second-order structure** directly on
`C^16`, and the first to isolate the per-`T_2`-state weighting primitive
as the unique remaining retained structural lever. The Correction-C
lever is not a new algebraic null — it is a named concrete successor
primitive whose presence or absence on retained `main` is a well-posed
question for the next agent to answer.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the charged-lepton
> effective second-order return
> `P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1}` on the `hw=1` generation
> triplet is identically `I_3`, re-derived here from the exact Cl(3)
> Clifford structure on `C^16`. Four independent hierarchy-breaking
> corrections — Higgs-axis fluctuation, higher-order iterated return,
> per-intermediate-state weighted propagator, and retained algebraic
> mass insertion — are examined. Three of the four are species-democratic
> on the retained `hw=1` triplet at every order tested. The fourth
> (per-`T_2`-state weighted propagator) structurally can lift the `I_3`
> degeneracy into the required three-level diagonal, but the retained
> framework does not currently supply the per-`T_2`-state weighting
> primitive, and the closest retained approximation (hw-staggered
> propagator weight `1 / (m_0 + hw · Δ)`) is 2+1 degenerate and cannot
> match the observed direction (best cos-sim `0.85 < 0.99`). The result
> is filed as `GAMMA_1_SECOND_ORDER_UNDERDETERMINED`: closing G5 via the
> retained `Γ_1` second-order return requires a new retained `C^16`
> operator that resolves the three individual `T_2` states into three
> distinct scalar weights aligned with the physical charged-lepton
> direction.

## Dependency contract

Retained authorities that must PASS on live `main` before this runner is
valid:

- `frontier_dm_neutrino_dirac_bridge_theorem.py` — **28 PASS / 0 FAIL** required. This runner replicates its key identity (`P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} = I_3`) as Phase 1.
- `frontier_g1_physicist_h_pmns_as_f_h.py` — G1 closure runner; establishes the `U_e = I_3` bridge structure.
- `frontier_g5_via_g1_h_charged_lepton.py` — Agent 9 scope-predecessor, `G5_CLOSES_VIA_G1_H = NO_NATURAL_MATCH`.

Framework-native retained constants used (none as fit parameters):
`v = 246.28 GeV`, `α_LM`, `u_0`, `⟨P⟩`, SU(3) Casimirs `(C_F, T_F, C_A)`,
SU(2) Casimirs `(C_F^{(2)}, T_F^{(2)}, C_A^{(2)})`, `Cl(3)` generators
`Γ_1, Γ_2, Γ_3, γ_5, Ξ_5` — none of which appears on the diagonal of any
tested correction at species-resolved weight. PDG charged-lepton masses
used only for the Koide / direction / ratio comparison.

## Atlas status

Proposed row for [`DERIVATION_ATLAS.md`](./publication/ci3_z3/DERIVATION_ATLAS.md) Section F (Flavor / CKM portfolio) and for [`FULL_CLAIM_LEDGER.md`](./publication/ci3_z3/FULL_CLAIM_LEDGER.md) Section 3:

| Tool | Authority | Status |
|---|---|---|
| `frontier_g5_gamma_1_second_order_return.py` | This note | **UNDERDETERMINED**; 20 PASS / 0 FAIL; Dirac-bridge consistency check PASS; four retained corrections surveyed; per-T_2-state weighting identified as missing retained primitive. |

## Status

**UNDERDETERMINED open-lane attack surface note.** Not a closure. The
value is the structural isolation of the missing retained primitive —
an operator on `C^16` that distinguishes the three `T_2` states `(1,1,0),
(1,0,1), (0,1,1)` with three distinct scalar weights aligned with the
observed `(m_e, m_μ, m_τ)` direction. Future G5 attacks should look for
this specific object rather than continuing to survey species-democratic
retained candidates.
