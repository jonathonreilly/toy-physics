# G5 / S_2-Breaking Primitive Survey on T_2 Subspace

**Date:** 2026-04-17
**Status:** Systematic survey of retained objects on `main` for S_2-breaking matrix elements on the T_2 states `(1,1,0)` and `(1,0,1)`. Verdict: **`S2_BREAKING_PRIMITIVE_AMBIGUOUS`** — only candidate 6 (G1's retained `H(m, δ, q_+)`) carries any S_2-breaking shape on the lifted T_2 basis, and that breaking (i) is G1-observational (pinned from neutrino PMNS, not a retained-theorem statement), (ii) does not match observed charged-lepton ratios (best cos-sim `0.74 < 0.99`), and (iii) relies on a post-hoc T_1 → T_2 species-index lift that is not itself a retained theorem. Every other retained object tested is S_2-symmetric on axes `{2, 3}` (either equal diagonal entries or zero T_2 diagonal with purely off-diagonal S_2-odd coupling). The survey rigorously confirms Agent 10 v2's structural-shape conclusion: G5 closure via the `Γ_1` second-order return requires a genuinely new retained primitive on `main` (or an observational pin analogous to G1's).
**Script:** [`scripts/frontier_g5_s2_breaking_primitive_survey.py`](../scripts/frontier_g5_s2_breaking_primitive_survey.py) — **31 PASS / 0 FAIL**.
**Authority role:** scope-refining attack-surface note for gap G5 (charged-lepton mass hierarchy). Extends [`G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md`](./G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE.md) and [`CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md`](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md) by systematically closing eight candidate channels for S_2-breaking primitives. Not a closure.

## Target

Agent 10 v2's structural-shape theorem: on the retained `Cl(3) ⊗ chirality` carrier `C^16`, the second-order `Γ_1` return on `T_1` has diagonal

```
diag(Σ) = (w_O0, w_a, w_b)
```

where `w_a` is the weight on T_2-state `(1, 1, 0)` and `w_b` is the weight on T_2-state `(1, 0, 1)`. The residual `S_2` symmetry on axes `{2, 3}` (left unbroken after EWSB axis-1 selection by `V_sel`) exchanges these two states, structurally forcing `w_a = w_b` in every retained propagator scheme tested so far.

This survey asks: does any retained object on `main` have distinct matrix elements between `(1,1,0)` and `(1,0,1)` that are NOT related by the `S_2` exchange?

For each candidate the runner computes, over the taste-doubled lattice subspace,

```
w_a   = Tr[ P_{(1,1,0)} O P_{(1,1,0)} ]
w_b   = Tr[ P_{(1,0,1)} O P_{(1,0,1)} ]
w_c   = Tr[ P_{(0,1,1)} O P_{(0,1,1)} ]  (the unreachable T_2 state, for context)
off   = |⟨(1,1,0)| O |(1,0,1)⟩| over the taste doublet
δ     = w_a − w_b
```

and flags the candidate as **TRUE (S_2 broken)** if `|δ| > 10⁻¹⁰` or `off > 10⁻¹⁰` AND the induced `(w_a, w_b)` weights satisfy the observed charged-lepton ratios `m_e/m_μ = 0.00484`, `m_μ/m_τ = 0.0594` within a cosine-similarity threshold of `0.99`.

## Candidate survey

### Candidate 1 — Anomaly substructure (individual traces)

Agent 8 showed the total anomaly-forced 3+1 structure is species-blind on `hw=1`. Here we test whether each INDIVIDUAL anomaly-coefficient contribution carries S_2-breaking matrix elements on T_2 before cancellation.

| Trace | `w_a, w_b, w_c` | `δ = w_a − w_b` | S_2 broken? |
|---|---|---|---|
| `Tr[Y]` (LH charged-lepton `Y = −1`) | `−2, −2, −2` | `0` | FALSE |
| `Tr[Y³]` | `−2, −2, −2` | `0` | FALSE |
| `Tr[SU(3)² Y]` (leptons singlet) | `0, 0, 0` | `0` | FALSE |
| `Tr[SU(2)² Y]` | `−2, −2, −2` | `0` | FALSE |
| Witten `SU(2)` | `0, 0, 0` | `0` | FALSE |

Each anomaly trace is proportional to identity on species (consistent with Agent 8's species-blind conclusion); no individual anomaly subcomponent breaks S_2. **Verdict: FALSE.**

### Candidate 2 — Higher-order retained Higgs potential invariants

Test 6th-order totally-symmetric Higgs invariants: `Σ φ_i⁶`, `(Σ φ_i²)³`, `Σ_{i<j} φ_i⁴ φ_j²`, `φ_1² φ_2² φ_3²`. At `φ = e_1` each Hessian gives `H_22 = H_33` and `H_23 = 0` exactly (verified symbolically with sympy). Theoretical closure: any retained `S_3`-invariant `V` has `Hess V|_{e_1}` fixed by `(2 ↔ 3)`, forcing `H_22 = H_33`.

**Verdict: FALSE.** No retained `S_3`-invariant Higgs potential can break S_2 at the Hessian level — S_2 survives as a residual of `S_3` that stabilizes `e_1`.

### Candidate 3 — Lattice-geometric operators on Z³

| Operator | `(w_a, w_b)` | `off(a,b)` | S_2-status |
|---|---|---|---|
| `Γ_1 + Γ_2 + Γ_3` (body-diagonal) | `0, 0` | `0` | S_2-symmetric |
| `Γ_1 − Γ_2 + Γ_3` (anti-diagonal) | `0, 0` | `0` | sign not retained |
| `Γ_2 + Γ_3` (face-diagonal `{2,3}`) | `0, 0` | `0` | S_2-symmetric |
| `Γ_1 Γ_2 Γ_3` (cube-corner) | `0, 0` | `0` | S_2-odd in algebra, zero T_2 diag |
| `Γ_2 Γ_3` (face bilinear) | `0, 0` | `1.41` | S_2-odd, pure off-diag |

The only S_2-odd object with nonzero T_2 coupling (`Γ_2 Γ_3`) generates purely off-diagonal `(1,1,0) ↔ (1,0,1)` matrix elements, not asymmetric diagonal weights, and was already tested as Correction-D in Agent 10 v2 to give zero T_1 species-diagonal contribution. A sign choice on axis 2 would break S_2 but is a post-axiom primitive, not retained.

**Verdict: FALSE.**

### Candidate 4 — Chirality-variant operators

All retained chirality operators — `γ_5, P_L, P_R, Ξ_5, γ_5 Ξ_5, P_L − P_R` — give `w_a = w_b` exactly (either both zero or both equal nonzero). Chirality sits in the taste slot and commutes with spatial projectors, so the T_2 diagonal is species-blind by construction. Consistent with the taste ⊗ species carrier orthogonality theorem (Agent 7).

**Verdict: FALSE.**

### Candidate 5 — Cl(3) bilinears on T_2 diagonals

Every retained Cl(3) generator and bilinear (`Γ_i`, `γ_5`, `Ξ_5`, `Γ_i Γ_j`, `Γ_1 Γ_2 Γ_3`, `Γ_i γ_5`) has `w_a = w_b = w_c = 0` on T_2 diagonals. The S_2-odd bilinears `Γ_2 Γ_3` and `Γ_1 Γ_2 Γ_3`-style objects have nonzero `(1,1,0) ↔ (1,0,1)` off-diagonal coupling (already tested by Correction-D in Agent 10 v2, giving zero T_1 species-diagonal contribution).

**Verdict: FALSE.**

### Candidate 6 — G1's retained `H(m, δ, q_+)` on lifted T_2

G1's retained Hermitian 3×3 `H(m, δ, q_+) = H_base + m T_m + δ T_δ + q_+ T_q` lives on the T_1 species basis. At the G1 chamber pin `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`, its diagonal is

```
diag H = m_* · (1, 0, 0) + δ_* · (0, 1, −1) + q_+* · (0, 0, 0)
       = (0.657061, 0.933806, −0.933806).
```

Lifted to T_2 via the species-index map `(1,1,0) ↔ species-3, (1,0,1) ↔ species-2, (0,1,1) ↔ species-1`, the T_2 diagonal is

```
(H_aa, H_bb, H_cc) = (−0.933806, +0.933806, +0.657061).
```

**Signed:** `δ_ab = −1.868` — S_2 BROKEN by a factor of `−1`. But physical masses are positive, and taking `|H|`-diag gives `(0.934, 0.934, 0.657)` — `w_a = w_b` exactly (because `T_δ`'s diagonal `(0, 1, −1)` is sign-flip-symmetric on entries 1 and 3, restoring S_2 under absolute value).

**Charged-lepton ratio match:** treating `|H|`-diag as propagator weights, best permutation cos-similarity to the PDG direction `(0.0165, 0.2369, 0.9713)` is `0.7432`, well below the `0.99` threshold — no match. Eigenvalue readings (`|λ|`, `λ²`) reproduce Agent 9's `NO_NATURAL_MATCH`.

**Retained-theorem status:** `H`'s structural shape is retained (from `T_m, T_δ, T_q` basis tensors) but the specific `(m, δ, q_+)` values are G1-observational (pinned by neutrino PMNS). Using `H`'s lifted T_2 diagonal as a charged-lepton propagator weight is a POST-HOC identification, not a retained theorem. `H` acts on T_1 species, not on T_2 propagator weights.

**Verdict: AMBIGUOUS.** Signed `H` diag breaks S_2 but doesn't match observation and requires a non-retained lift; `|H|`-diag restores S_2 accidentally.

### Candidate 7 — Anomaly-forced time direction

`Γ_0` sits in the taste slot and has `w_a = w_b = w_c = 0` on T_2 diagonals. Products `Γ_0 Γ_i` change Hamming weight by one and do not have T_2 diagonal matrix elements (either zero diagonal with pure off-diagonal, or zero entirely). The retained 3+1 anomaly-forces-time theorem carries no S_2-breaking info on T_2 diagonals.

**Verdict: FALSE.**

### Candidate 8 — Retained Schur-cascade structure from CKM atlas

A generic retained Schur cascade `D_n = Σ_k c_k (P_{C_3})^k` is a `C_3`-class function on the three-generation triplet. Class functions on `C_3` have equal diagonal entries in the axis basis by `C_3` invariance, so `w_a = w_b = w_c` exactly. Verified numerically: cascade with `(c_0, c_1, c_2) = (1.0, 0.3, 0.1)` gives T_2 diagonal `(1.0, 1.0, 1.0)`. Breaking this to `1+1+1` requires an auxiliary non-`C_3` source — the same missing primitive already named.

**Verdict: FALSE.**

## Summary table

| Candidate | Breaks S_2 on T_2 diagonals? | Matches charged-lepton ratios? |
|---|---|---|
| 1. Anomaly substructure (Tr Y, Tr Y³, mixed, Witten) | FALSE | — |
| 2. Higher-order Higgs invariants (6th order) | FALSE | — |
| 3. Lattice-geometric ops (body/face diag, corners) | FALSE | — |
| 4. Chirality operators (γ_5, P_L, P_R, Ξ_5) | FALSE | — |
| 5. Cl(3) bilinears on T_2 diagonals | FALSE | — |
| 6. G1's `H(m, δ, q_+)` lifted to T_2 | AMBIGUOUS (signed yes, |.|-symmetric no) | NO (cos-sim 0.74) |
| 7. Anomaly-forced time direction `Γ_0` | FALSE | — |
| 8. Retained Schur cascade from CKM atlas | FALSE | — |

## Final verdict

**`S2_BREAKING_PRIMITIVE_AMBIGUOUS`**

No retained object on `main` breaks S_2 on T_2 diagonals with weights matching observed charged-lepton ratios. Candidate 6 (G1's `H` lifted to T_2) carries AMBIGUOUS S_2-breaking shape but (i) the lift from T_1 species to T_2 propagator weights is a post-hoc identification rather than a retained theorem, (ii) the signed diagonal matches neither charged-lepton magnitudes nor Koide `Q = 2/3`, and (iii) the `|H|`-diagonal is accidentally S_2-symmetric due to `T_δ`'s `(0, 1, −1)` structure.

This rigorously confirms Agent 10 v2's structural-shape conclusion. G5 closure via the `Γ_1` second-order return requires one of:

1. A genuinely new retained primitive that distinguishes `(1,1,0)` from `(1,0,1)` in both sign and magnitude.
2. A retained LIFTING theorem that promotes G1's `H` (or an analog) from T_1 species to T_2 propagator weights — turning candidate 6 from AMBIGUOUS to TRUE.
3. An observational pin analogous to G1's PMNS pin, promoting Koide `Q_ℓ = 2/3` to retained-via-observational-promotion.

## Honest interpretation

All eight candidate channels either respect S_2 on axes `{2, 3}` exactly, or have zero T_2 diagonal weights (their S_2-odd coupling lives purely off-diagonal and contributes zero to the retained `T_1` second-order return, as Agent 10 v2's Correction-D already established). The only ambiguous case — candidate 6 — depends on a T_1 → T_2 species-index lift that is not presently retained on `main` and whose signed diagonal fails the charged-lepton direction match anyway (cos-sim `0.74 < 0.99`). The convergent architectural fact is sharp: within the retained `Cl(3)/Z³` framework surface, every symmetry-compatible object on the taste-doubled lattice either commutes with the `S_2` that exchanges `(1,1,0) ↔ (1,0,1)` or couples them purely off-diagonally; none supplies the distinct-magnitude diagonal weights the Agent 10 v2 shape theorem requires. This is a rigorously valuable negative: G5 does not close on any retained primitive currently on `main`, and the follow-up target is now sharply specified — either a T_1 → T_2 lifting theorem for G1's `H`, or a new axis-specific primitive, or an observational-pin promotion.

## Dependency contract

Retained authorities validated on live `main`:

- `frontier_dm_neutrino_dirac_bridge_theorem.py` (28 PASS / 0 FAIL) — defines `Γ_1`, first-order vanishing, `I_3` second-order return.
- `frontier_g1_physicist_h_pmns_as_f_h.py` — defines `H(m, δ, q_+)` used in candidate 6.
- `frontier_koide_anomaly_forced_cross_species.py` (42 PASS / 0 FAIL) — Agent 8's individual-anomaly-trace species-blindness context for candidate 1.
- `frontier_g5_gamma_1_second_order_return.py` (20 PASS / 0 FAIL) — Agent 10 v2's shape theorem that motivates this survey.

Framework-native objects used only: `Cl(3)` generators `Γ_0, Γ_1, Γ_2, Γ_3`, chirality projectors `P_L, P_R`, `γ_5`, `Ξ_5`, retained anomaly-coefficient hypercharges, retained Higgs potential `V_sel = 32 Σ_{i<j} φ_i² φ_j²`, G1's `H_base, T_m, T_δ, T_q`, `C_3` cyclic permutation for Schur cascade. PDG charged-lepton masses used only in the final cos-similarity check.

## What this does NOT claim

- No closure of G5. The `S_2`-breaking primitive remains ABSENT on retained `main` (candidate 6 is ambiguous, not a closure).
- No promotion of Koide `Q_ℓ = 2/3` to retained framework theorem.
- No claim that the eight candidates are exhaustive — they are the concrete channels enumerated by the task brief. Future agents may identify additional retained channels.
- No overlap with Agent 11 (observational-pin), Agent 13 (joint pinning), or Agent 14 (robustness audit) — this survey is structural-primitive-enumeration only.

## Atlas status

Proposed row for [`DERIVATION_ATLAS.md`](./publication/ci3_z3/DERIVATION_ATLAS.md) Section F (Flavor / CKM portfolio) and [`FULL_CLAIM_LEDGER.md`](./publication/ci3_z3/FULL_CLAIM_LEDGER.md) Section 3:

| Tool | Authority | Status |
|---|---|---|
| `frontier_g5_s2_breaking_primitive_survey.py` | This note | **`S2_BREAKING_PRIMITIVE_AMBIGUOUS`**; 31 PASS / 0 FAIL; eight candidate channels surveyed; candidate 6 (G1's H lifted) alone has S_2-breaking shape but does not match charged-lepton ratios and depends on a non-retained lift. Rigorously confirms Agent 10 v2's shape-theorem conclusion. |

## Status

**`S2_BREAKING_PRIMITIVE_AMBIGUOUS` open-lane attack surface note.** Not a closure. The value is the systematic closure of seven candidate channels (1-5, 7, 8) as rigorously S_2-symmetric on T_2 diagonals, and the isolation of candidate 6 (G1 `H` lift) as the unique ambiguous case whose full resolution depends on whether a T_1 → T_2 lifting theorem can be retained. Future G5 attacks should either target that specific lifting theorem, target Agent 11's observational-pin lane, or accept Koide as an unretained observational fact.
