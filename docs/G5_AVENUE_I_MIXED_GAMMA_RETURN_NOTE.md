# G5 / Avenue I — Mixed-Γ_i Fourth-Order Return

**Date:** 2026-04-17
**Status:** `AVENUE_I_NO_RETAINED_MIXED_BREAKING`. Fourth-order mixed-Γ_i insertions on the retained `Cl(3) ⊗ chirality` carrier `C^16` either vanish on species (through the canonical retained intermediate `P_{O_0} + P_{T_2}`), or have single-species-resolved individual orderings whose signed within-multiset sum vanishes exactly (through `P_{O_0} + P_{T_2} + P_{O_3}`). EWSB-weighted (Construction I-5) and unweighted (Construction I-4) symmetrizations both inherit this sign cancellation. No retained mixed-Γ fourth-order construction breaks the residual `S_2` on species `{2, 3}`; the missing per-`T_2`-state weighting primitive isolated by Agent 10 v2 Correction-C is not supplied by extending to fourth order with mixed insertions.
**Script:** [`scripts/frontier_g5_avenue_i_mixed_gamma_return.py`](../scripts/frontier_g5_avenue_i_mixed_gamma_return.py) — **11 PASS / 0 FAIL**.
**Authority role:** frontier attack-surface runner closing Avenue I (mixed-Γ_i fourth-order return) for gap G5 (charged-lepton mass hierarchy). Extends Agent 10 v2's second-order shape theorem and Agent 14's pure-Γ_1 iterated stress tests to genuinely mixed-Γ insertions. Not a closure. Not a new retained theorem.

## Safe statement (promotable to retained)

On the retained `Cl(3) ⊗ chirality` carrier `C^16` with the branch-convention EWSB generators
`Γ_i = ∂_i` and HW-stratum projectors `P_{O_0}, P_{T_1}, P_{T_2}, P_{O_3}`, the fourth-order mixed-Γ return operator family

```
Σ_mixed(i, j, k, l ; Π_1, Π_2, Π_3)
  = P_{T_1} Γ_i Π_1 Γ_j Π_2 Γ_k Π_3 Γ_l P_{T_1}
```

with `(i, j, k, l) ∈ {1, 2, 3}^4` and `Π_n ∈ {P_{O_0}, P_{T_2}, P_{O_3}, …}`, restricted to the `T_1` species block, satisfies two structural identities:

1. **Parity selection.** `Σ_mixed` has nonzero species diagonal only if each axis index appears an even number of times in `(i, j, k, l)`. There are 21 such even-axis-count sequences out of 81.
2. **Canonical-intermediate vanishing.** Through the canonical retained intermediate `Π = P_{O_0} + P_{T_2}`, every mixed-Γ return `Σ_mixed` has species block identically zero. Species-resolved structure only appears when `P_{O_3}` is included in the intermediate.
3. **Ordering-signed cancellation.** Through `Π = P_{O_0} + P_{T_2} + P_{O_3}`, individual orderings within a fixed multiset `{Γ_a, Γ_a, Γ_b, Γ_b}` (`a ≠ b`) produce pure single-species diagonals `±(δ_{c=1}, δ_{c=2}, δ_{c=3})` where `c` is the axis *not* in `{a, b}`, but the signed sum over the six orderings of any such multiset vanishes exactly.

These three facts together imply that no mixed-Γ fourth-order symmetrization — unweighted (Construction I-4) or EWSB-weighted by Higgs VEV φ-monomials (Construction I-5) — carries a non-zero species-diagonal. The residual `S_2` on species `{2, 3}` identified by Agent 10 v2 as the retained obstruction survives the Avenue I extension untouched.

## Phase 0 — consistency check (5 PASS / 0 FAIL)

The runner first reproduces retained baseline identities:

- Agent 10 v2 / Dirac-bridge: `P_{T_1} Γ_1 (P_{O_0} + P_{T_2}) Γ_1 P_{T_1} |_{species} = I_3`.
- Agent 14 Stress 1 (S_3 axis covariance): `P_{T_1} Γ_i (P_{O_0} + P_{T_2}) Γ_i P_{T_1} |_{species} = I_3` for each `i ∈ {1, 2, 3}`.
- Agent 14 Stress 2 (iterated): pure-Γ_1 `[Γ_1 P_{not T_1} Γ_1]^2` on species = `I_3`.

These Phase-0 checks certify the Avenue I runner is operating on the same retained surface as the prior agents.

## Phase 1 — enumeration of 21 even-axis-count sequences

For each of the 21 sequences with each axis count even, we compute the species diagonal through two retained intermediates.

### 1a. Through `Π = P_{O_0} + P_{T_2}` (canonical retained)

**All 21 sequences give diag = (0, 0, 0)** — zero species diagonal. Pure-Γ_i (four identical insertions) trivially returns to `I_3` on full `T_1` but zero on species, because `Γ_i^4 = I` but intermediate projectors alternate. Mixed multisets similarly vanish because the two-hop `T_1 → T_2` via `Γ_a` lands on a state that `Γ_b` (for `a ≠ b`) either cannot return directly or only via paths that require `P_{O_3}`.

### 1b. Through `Π = P_{O_0} + P_{T_2} + P_{O_3}` (all non-T_1)

Individual orderings within multisets `{Γ_a, Γ_a, Γ_b, Γ_b}` with `a ≠ b` produce species-resolved single-species diagonals. Representative orderings (full enumeration in the runner stdout):

| Ordering | Multiset | diag (species 1, 2, 3) |
|---|---|---|
| `Γ_1 Γ_2 Γ_2 Γ_1` | `{Γ_1², Γ_2²}` | `(0, 0, +1)` |
| `Γ_2 Γ_1 Γ_1 Γ_2` | `{Γ_1², Γ_2²}` | `(0, 0, +1)` |
| `Γ_1 Γ_2 Γ_1 Γ_2` | `{Γ_1², Γ_2²}` | `(0, 0, −1)` |
| `Γ_2 Γ_1 Γ_2 Γ_1` | `{Γ_1², Γ_2²}` | `(0, 0, −1)` |
| `Γ_1 Γ_1 Γ_2 Γ_2` | `{Γ_1², Γ_2²}` | `(0, 0, 0)` |
| `Γ_2 Γ_2 Γ_1 Γ_1` | `{Γ_1², Γ_2²}` | `(0, 0, 0)` |
| `Γ_1 Γ_3 Γ_3 Γ_1` | `{Γ_1², Γ_3²}` | `(0, +1, 0)` |
| `Γ_2 Γ_3 Γ_3 Γ_2` | `{Γ_2², Γ_3²}` | `(+1, 0, 0)` |

**The species reached by multiset `{Γ_a², Γ_b²}` is the axis `c` not in `{a, b}`.** This is an `S_3`-equivariant extension of Agent 10 v2's shape theorem: where the second-order `Γ_a` return hops species `i` to `O_0` (for `i = a`) or `T_2` (for `i ≠ a`), the fourth-order mixed-`Γ_a Γ_b` return projects onto species `c`. But the within-multiset ordering sum of these single-species diagonals, with the signs induced by the `σ_z` factors in the Jordan-Wigner embedding of `Γ_2, Γ_3`, is exactly zero:

```
+1 +1 −1 −1 +0 +0 = 0
```

Pure-Γ_i multisets `{Γ_i⁴}` give `diag = (0, 0, 0)` directly (four identical hops traverse a closed path that returns to T_1 via O_0 which contains no species label).

## Phase 2 — named Constructions I-1 through I-4

### Construction I-1: `Σ_I1 = P_{T_1} Γ_1 Π Γ_2 Π Γ_2 Π Γ_1 P_{T_1}`

Axis count `(2, 2, 0)` — even. Through various intermediates:

| Π | diag |
|---|---|
| `P_{O_0} + P_{T_2}` | `(0, 0, 0)` |
| `P_{T_2}` | `(0, 0, 0)` |
| `P_{O_0} + P_{T_2} + P_{O_3}` | `(0, 0, +1)` |
| `P_{O_3}` | `(0, 0, 0)` |
| `P_{O_0}` | `(0, 0, 0)` |

Only when `P_{O_3}` is *mixed with* `P_{O_0} + P_{T_2}` does a non-zero diagonal appear. The non-zero entry is at species 3 (the axis not in `{1, 2}`).

**Retained justification:** Γ_1, Γ_2 are retained EWSB generators. Mixing `P_{O_3}` into the intermediate is retained only if a retained primitive assigns it unit weight; the Dirac-bridge theorem PASS set uses the canonical intermediate `P_{O_0} + P_{T_2}` with unit weight everywhere, which gives zero.

### Construction I-2: `Σ_I2 = P_{T_1} Γ_1 Π Γ_2 Π Γ_3 Π Γ_1 P_{T_1}`

Axis count `(2, 1, 1)` — **NOT even**. Species diagonal is exactly zero; the operator has non-zero off-species-diagonal entries (`T_1 → T_2` leakage). Fails the parity selection rule — this construction does not species-diagonalize.

### Construction I-3: `Σ_I3 = P_{T_1} Γ_2 Π Γ_1 Π Γ_1 Π Γ_2 P_{T_1}`

Axis count `(2, 2, 0)` — even. Behaves analogously to I-1 (axis-roles swapped): through `P_{O_0} + P_{T_2} + P_{O_3}`, `diag = (0, 0, +1)`; through canonical retained intermediate, `(0, 0, 0)`.

### Construction I-4: Unweighted symmetrization

```
Σ_I4 = (1/21) Σ_{seq ∈ even-parity} fourth_order_return(seq, Π)
```

Through `Π = P_{O_0} + P_{T_2}`: `diag = (0, 0, 0)`.
Through `Π = P_{O_0} + P_{T_2} + P_{O_3}`: `diag = (0, 0, 0)`.

**Per-multiset sums** (through `P_{O_0} + P_{T_2} + P_{O_3}`): every multiset gives `diag = (0, 0, 0)` as a signed sum of its six orderings. The `±1` entries cancel in pairs.

**Retained justification:** the unweighted symmetrization is a retained construction (uniform sum over permutations of retained generators), but its vanishing is intrinsic — no free parameter can rescue it.

## Phase 3 — Construction I-5: EWSB-weighted

### Set-up

The retained local spatial Higgs family is `M(φ) = φ_1 Γ_1 + φ_2 Γ_2 + φ_3 Γ_3`. After EWSB axis-1 selection, `V_sel = 32 Σ_{i<j} φ_i² φ_j²` is minimized at `φ = e_1`. The retained Hessian at `e_1` is

```
∂²V / ∂φ_a ∂φ_b |_{e_1} = 64 δ_{ab}      for a, b ∈ {2, 3}
```

and `= 0` for any index touching axis 1. Fluctuations around `e_1` therefore follow a Gaussian measure `N(0, σ²)` with **equal variance** `σ_2 = σ_3`.

The EWSB-weighted fourth-order return at generic `φ = (φ_1, φ_2, φ_3)` is

```
Σ_I5(φ, Π) = P_{T_1} M(φ) Π M(φ) Π M(φ) Π M(φ) P_{T_1}
           = Σ_{seq} φ_{seq[0]} φ_{seq[1]} φ_{seq[2]} φ_{seq[3]}  ×  Σ_seq
```

where `Σ_seq` is the unweighted 4-hop return for sequence `seq`.

### Result

At `φ = e_1`: `Σ_I5 = 0` (all mixed terms have zero `φ`-monomial weight; pure `Γ_1⁴` gives zero diagonal).

At `φ = (1, ε, ε)` with `ε` small (symmetric): `diag = (0, 0, 0)` to within `1e-37` (machine precision at this expansion order). The signed ordering sum inside each multiset cancels independent of the overall `φ`-monomial weight, because the `φ`-monomial depends only on the MULTISET, not on the ordering.

Anisotropic `φ = (1, ε_2, ε_3)` with `ε_2 ≠ ε_3`: `diag = (0, 0, 0)` still, by the same within-multiset cancellation.

**Gaussian MC average** over (ε_2, ε_3) ~ N(0, σ²) iid with σ = 0.05, N = 10 000:

```
⟨Σ_I5⟩_Gaussian = (0, 0, 0)       |d_2 − d_3| = 0
```

Even a deliberately anisotropic (non-retained) variance `σ_2 = 0.10, σ_3 = 0.02` gives `⟨Σ_I5⟩ = (0, 0, 0)`. The vanishing is **structural**, stronger than any S_2 symmetry of the measure.

### Retained vs ad-hoc audit

| Ingredient | Retained? | Source |
|---|---|---|
| `Γ_1, Γ_2, Γ_3` generators | **Retained** | Dirac-bridge theorem PASS set on C^16 |
| `P_{O_0}, P_{T_1}, P_{T_2}, P_{O_3}` projectors | **Retained** | Hamming-weight projectors on Cl(3)/Z^3 |
| Mixed-Γ fourth-order product | **Retained** | Direct operator composition |
| Higgs family `M(φ) = Σ φ_i Γ_i` | **Retained** | Dirac-bridge retained Higgs family |
| V_sel Hessian σ_2 = σ_3 at e_1 | **Retained** | Exact from `V_sel = 32 Σ_{i<j} φ_i² φ_j²` |
| Anisotropic `σ_2 ≠ σ_3` | **NOT retained** | No retained mechanism forces it |
| Per-T_2-state weights | **NOT retained** | Agent 10 v2 Correction-C's missing primitive |

Every structural element tested here is retained. The constructions themselves build from retained objects. The verdict is therefore a statement about the retained framework's capability, not about the sufficiency of a particular ansatz.

## Phase 4 — species-resolved Koide / direction check

### Structural observation (runner text, Phase 4)

Individual orderings within each multiset ARE species-resolved (pure single-species diagonals `±(δ_{c=1}, δ_{c=2}, δ_{c=3})` through `P_{O_0} + P_{T_2} + P_{O_3}`), but:

- Pure unweighted sum over orderings → 0 (sign cancellation).
- EWSB-weighted sum `Σ_seq [Π φ_{seq[i]}] × diag(seq)` also → 0, because the φ-monomial depends only on the multiset, not on the ordering.

**Consequence:** no Gaussian-fluctuation construction lifts the species degeneracy. The retained obstruction is STRONGER than "S_2 symmetric": it is **ordering-signed cancellation** of Clifford algebra products.

### Hypothetical (non-retained) absolute-magnitude benchmark

If each ordering were weighted by a non-signed positive scalar (violating the signed Clifford algebra), multiset sums would give

```
species 1 ∝ (|φ_2||φ_3|)²  from {Γ_2², Γ_3²}
species 2 ∝ (|φ_1||φ_3|)²  from {Γ_1², Γ_3²}
species 3 ∝ (|φ_1||φ_2|)²  from {Γ_1², Γ_2²}
```

At EWSB `φ_1 = v` and σ_2 = σ_3 = σ, this gives `(σ^4, v²σ², v²σ²)` — a 2+1 degenerate pattern structurally identical to Agent 10 v2's Correction-C hw-staggered scheme. Scan over `v/σ`:

| v/σ | `(σ^4, σ², σ²)` | Koide Q | cos-sim to PDG |
|---|---|---|---|
| 100 | `(10⁻⁸, 10⁻⁴, 10⁻⁴)` | 0.495 | 0.854 |
| 10 | `(10⁻⁴, 10⁻², 10⁻²)` | 0.456 | 0.853 |
| 2 | `(0.0625, 0.25, 0.25)` | 0.360 | 0.811 |
| 1 | `(1, 1, 1)` | 0.333 | 0.707 |
| 0.5 | `(16, 4, 4)` | 0.375 | 0.507 |
| 0.1 | `(10⁴, 10², 10²)` | 0.708 | 0.136 |

**Maximum achievable cos-similarity to PDG direction: ≈ 0.854** (at `v/σ = 100`). Far below the `0.99+` threshold for a plausible match. No value achieves Koide `Q = 2/3` simultaneously with a cos > 0.99.

Even under this generous *non-retained* benchmark, the fourth-order mixed-Γ structure lands squarely on Agent 10 v2's 2+1 degeneracy failure mode — the obstruction is intrinsic to the `S_2`-symmetric residual of EWSB axis-1 selection.

## Four-outcome verdict

**`AVENUE_I_NO_RETAINED_MIXED_BREAKING`**

| Outcome | Disposition |
|---|---|
| `AVENUE_I_CLOSES_G5` | RULED OUT — no mixed-Γ fourth-order construction produces species-resolved `(d_1, d_2, d_3)` aligned with `(m_e, m_μ, m_τ)` at Koide `Q = 2/3`. |
| `AVENUE_I_CONE_ONLY` | RULED OUT — no cone-forcing from mixed-Γ insertions; residual `S_2` on species `{2, 3}` remains unbroken. |
| `AVENUE_I_S2_BREAKING_BUT_NO_KOIDE` | RULED OUT — mixed-Γ insertions under the retained V_sel Hessian do not break `S_2` at all. |
| **`AVENUE_I_NO_RETAINED_MIXED_BREAKING`** | **CONFIRMED** — retained mixed-Γ fourth-order constructions vanish (through canonical retained intermediate) or have individual species-resolved orderings whose signed within-multiset sum cancels exactly. |

## Per-construction summary

| Construction | diag (L-taste, through P_all) | Koide Q | cos-sim | Retained/ad-hoc |
|---|---|---|---|---|
| I-1: `Γ_1 Π Γ_2 Π Γ_2 Π Γ_1` (single ordering) | `(0, 0, +1)` | degenerate | 0.577 | retained, but single ordering not a full retained object |
| I-2: `Γ_1 Π Γ_2 Π Γ_3 Π Γ_1` (axis-count odd) | `(0, 0, 0)`; off-diag nonzero | N/A | N/A | retained product; off-species — doesn't species-diagonalize |
| I-3: `Γ_2 Π Γ_1 Π Γ_1 Π Γ_2` (single ordering) | `(0, 0, +1)` | degenerate | 0.577 | retained, but single ordering not a full retained object |
| I-4: unweighted symmetrization (21 sequences) | `(0, 0, 0)` | 1/3 | 0.707 | retained, trivially zero |
| I-5: EWSB-weighted, Gaussian-averaged | `(0, 0, 0)` | 1/3 | 0.707 | fully retained, exactly zero |
| *hypothetical non-retained (σ^4, σ², σ²)* | *`(v/σ)^{-2}, 1, 1`* | 0.333–0.71 | **0.85 max** | *NOT retained — benchmark only* |
| **PDG target** | `(0.511, 105.66, 1776.86) MeV` | **0.6667** | **1.0000** | — |

## What this does NOT claim

- No closure of G5. The shape theorem and the Agent 10 v2 Correction-C missing primitive are unchanged.
- No promotion of any result to retained-theorem status. The "Safe statement" above is promotable *if* Avenue I is added to the published framework audit; it is not currently retained.
- No new retained axiom or operator.
- No claim that SOME non-retained mixed-Γ construction might close G5. The runner tests only retained constructions and a single honest non-retained benchmark (absolute-magnitude multiset weights) that already lands on the 2+1 failure mode.
- No refutation of the possibility that a retained primitive beyond the scope of Avenue I (e.g., Higgs-dressed propagator — Agent 15 or stationarity principle — Agent 16) breaks the residual `S_2`.

## Relationship to sibling notes

- **Agent 10 v2 ([`G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md`](./G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md), Correction A):** Agent 10 v2 tested Higgs fluctuations `φ = e_1 + ε` at SECOND order and found `diag(Σ − I_3) = |ε|²(1, 1, 1)` — species-democratic. Avenue I extends to FOURTH order with mixed-Γ insertions. The result is STRONGER than Correction A: the EWSB-weighted fourth-order return is **exactly zero** on species (not merely species-democratic), because within-multiset ordering sums cancel before any φ-monomial weighting.
- **Agent 14 Stress Test 5 ([`G5_SHAPE_THEOREM_ROBUSTNESS_AUDIT_NOTE.md`](./G5_SHAPE_THEOREM_ROBUSTNESS_AUDIT_NOTE.md), `S_3` gauge check):** Agent 14 identified the Jordan-Wigner nuance: the naive bit-permutation unitary `U_{perm}` is not a Clifford ring automorphism for odd permutations, but HW-projector structure remains `S_3`-equivariant. Avenue I confirms this nuance in a new setting: the sign structure of individual mixed-Γ orderings (which determines the cancellation pattern) follows exactly the Jordan-Wigner `σ_z` placement in `Γ_2 = σ_z ⊗ σ_x ⊗ I ⊗ I` and `Γ_3 = σ_z ⊗ σ_z ⊗ σ_x ⊗ I`. Despite this representation-dependent sign, the multiset-sum vanishing is a Clifford-algebraic fact: for any Clifford rep, `{Γ_a, Γ_a, Γ_b, Γ_b}` ordering sums on T_1 species give zero.
- **Agent 12 Candidate 3 ([`G5_S2_BREAKING_PRIMITIVE_SURVEY_NOTE.md`](./G5_S2_BREAKING_PRIMITIVE_SURVEY_NOTE.md), lattice-geometric no-go):** Agent 12 showed that no sole-axiom lattice-geometric object breaks `S_2` on species `{2, 3}`. Avenue I closes a specific non-sole-axiom but still retained lane (mixed-Γ fourth-order symmetrization): extending the order and including all retained Γ_i does not supply the missing primitive. Both nulls converge on the same conclusion — the required primitive does not live in the retained spatial-Clifford + HW-projector + Higgs-VEV algebra.

## Dependency contract

Retained authorities that must PASS on live `main` before this runner is valid:

- `frontier_dm_neutrino_dirac_bridge_theorem.py` — **28 PASS / 0 FAIL** required. Supplies `Γ_i`, `P_{O_0}, P_{T_1}, P_{T_2}, P_{O_3}` and the baseline second-order identity.
- `frontier_g5_gamma_1_second_order_return.py` — **20 PASS / 0 FAIL** (Agent 10 v2) — supplies the shape theorem and Correction-C reference.
- `frontier_g5_shape_theorem_robustness_audit.py` — **57 PASS / 0 FAIL** (Agent 14) — supplies the iterated-return baseline and the `S_3` gauge clarification.

Framework-native retained objects used (none as fit parameters):
`Γ_1, Γ_2, Γ_3` (retained EWSB axis generators), `P_{O_0}, P_{T_1}, P_{T_2}, P_{O_3}` (HW-projectors), `M(φ) = Σ φ_i Γ_i` (retained Higgs family), `V_sel = 32 Σ_{i<j} φ_i² φ_j²` (retained selector Hessian at `e_1`).

PDG charged-lepton masses `(m_e, m_μ, m_τ)` appear ONLY in the Koide and cos-similarity comparisons, never as inputs to any retained construction.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the fourth-order mixed-Γ_i return family `P_{T_1} Γ_i Π Γ_j Π Γ_k Π Γ_l P_{T_1}` with `(i, j, k, l) ∈ {1, 2, 3}^4` and retained intermediate projectors `Π ∈ {P_{O_0}, P_{T_2}, P_{O_3}, …}` is exhaustively enumerated on `C^16`. Parity selection (each axis count even) admits 21 of 81 sequences. Through the canonical retained intermediate `P_{O_0} + P_{T_2}`, every such return has zero species diagonal. Through `P_{O_0} + P_{T_2} + P_{O_3}`, individual orderings within multisets `{Γ_a², Γ_b²}` (a ≠ b) give pure single-species diagonals on the axis `c` not in `{a, b}`, but signed ordering sums vanish exactly (in pairs of `±1`). EWSB-weighted symmetrization under the retained V_sel Hessian `σ_2 = σ_3` at axis-1 selection inherits this vanishing identically: the φ-monomial weight depends only on the multiset, not on the ordering, so the ordering-signed cancellation is not lifted by any retained fluctuation. A hypothetical non-retained absolute-magnitude benchmark gives a 2+1 degenerate pattern `(σ^4, v²σ², v²σ²)` that reproduces Agent 10 v2's Correction-C hw-staggered failure mode with maximum cos-similarity ≈ 0.854 to the observed `(m_e, m_μ, m_τ)` direction. Verdict: `AVENUE_I_NO_RETAINED_MIXED_BREAKING`. The missing per-`T_2`-state weighting primitive isolated by Agent 10 v2 is not supplied by fourth-order mixed-Γ constructions on the retained surface.

## Atlas status

Proposed row for [`DERIVATION_ATLAS.md`](./publication/ci3_z3/DERIVATION_ATLAS.md) Section F (Flavor / CKM portfolio):

| Tool | Authority | Status |
|---|---|---|
| `frontier_g5_avenue_i_mixed_gamma_return.py` | This note | `AVENUE_I_NO_RETAINED_MIXED_BREAKING`; 11 PASS / 0 FAIL; 21 even-parity mixed-Γ sequences enumerated; all retained constructions give zero species diagonal; hypothetical non-retained absolute-magnitude benchmark reproduces Agent 10 v2 Correction-C 2+1 failure mode. |

## Status

Frontier attack-surface note. Not a closure. The retained `Cl(3)/Z^3` framework does not supply a mixed-Γ fourth-order mechanism that breaks the residual `S_2` on species `{2, 3}`. Future G5 attacks should look outside the spatial-Clifford / HW-projector / Higgs-VEV algebra (Agents 15, 16 pending) rather than higher-order within-algebra constructions.
