# G5 / Avenue G — Higgs-Dressed Intermediate Propagator

**Date:** 2026-04-17
**Status:** NEGATIVE. A systematic survey of four retained constructions for
a Higgs-dressed intermediate weight operator `W(H)` on the `(O_0 ⊕ T_2)`
subspace — derived from G1's retained affine Hermitian `H(m, δ, q_+)` at
the G1 chamber pin `(m_*, δ_*, q_+*) = (0.657, 0.934, 0.715)` — produces
no variant reproducing the observed charged-lepton direction or Koide
`Q = 2/3`. Best cos-similarity across 27 variants is `0.919` (G-4b);
best `|Q − 2/3|` is `0.239`. The retained "Higgs-as-propagator-dressing"
lane is therefore **not** the missing G5 primitive.
**Verdict:** `AVENUE_G_NO_MATCH`.
**Script:** [`scripts/frontier_g5_avenue_g_higgs_dressed_propagator.py`](../scripts/frontier_g5_avenue_g_higgs_dressed_propagator.py) — **10 PASS / 0 FAIL**.
**Authority role:** attack-surface note closing the "Avenue G" lane (Higgs-
dressed intermediate propagator) identified by Agent 15 as structurally
distinct from Agents 9, 12, 13's lanes. Not a closure; not a demotion of
any retained object. The valuable content is the rigorous negative: H as
a propagator dressing on C^16 does not carry the S_2-breaking,
three-level shape that Agent 10 v2's shape theorem requires.
**Framework convention:** "axiom" means only the single framework axiom
`Cl(3)` on `Z^3`.

## One-sentence state

Inserting the retained `H(m_*, δ_*, q_+*)` as a species-diagonal or
species-off-diagonal weight operator `W(H)` on the intermediate
`(O_0 ⊕ T_2)` subspace of `C^16`, via the natural `Γ_1`-induced
species-to-intermediate-state transport, does not produce a species-
resolved second-order return diagonal matching the observed charged-
lepton direction at any tested shift, power, or retained linear
combination — so the Higgs-as-propagator-dressing construction is not
the missing G5 primitive.

## Safe statement

On the retained `Cl(3) ⊗ chirality` carrier `C^16`, with the retained
`Γ_1 = σ_x ⊗ I ⊗ I ⊗ I` branch-convention operator and the retained
projectors `P_{O_0}, P_{T_1}, P_{T_2}, P_{O_3}`, there is a canonical
bijection induced by `Γ_1` between the three `T_1` species and the three
`Γ_1`-reachable intermediate states:

```
species 1 (electron) <--> O_0 = (0,0,0)
species 2 (muon)     <--> (1,1,0) in T_2
species 3 (tau)      <--> (1,0,1) in T_2
```

Using this bijection, any 3×3 operator `X` on the `T_1` species basis
admits a canonical lift `X^{int}` to the 3-dimensional intermediate
subspace reachable from `T_1` in one `Γ_1` hop. The runner verifies that
the second-order return on `T_1` through this lifted weight reduces to a
species block whose diagonal is the diagonal of `X`:

```
P_{T_1} Γ_1 (lift_int X) Γ_1 P_{T_1} |_{T_1 species} = diag(X)
```

provided `Γ_1` acts on each species as a single axis flip (which is its
retained structure). This is a structural identity. The question is
whether any retained choice of `X = f(H)` places `diag(X)` in
correspondence with the observed `(m_e, m_μ, m_τ)` direction and Koide
`Q = 2/3`. Twenty-seven variants tested, none matches.

## Construction map

The runner surveys four construction families. Each is built from
retained-on-`main` objects only; no new axiom, no post-axiom primitive.

### Construction G-1 — natural Higgs-lift via `Γ_1` hopping

Lift `f(H)` into the intermediate subspace via the canonical species-to-
intermediate bijection. Six variants:

| Variant | `f(H)` | diag(Σ) at G1 pin | Koide Q | cos-sim PDG (best perm) |
|---|---|---|---|---|
| G-1a | `diag(eigvals ascending)` | `(−1.309, −0.320, +2.287)` | `0.377` | `0.8839` |
| G-1b | `diag(|eigvals|)` | `(+1.309, +0.320, +2.287)` | `0.377` | `0.8839` |
| G-1c | `H` itself (full, off-diag retained) | `(+0.657, +0.934, −0.934)` | `0.335` | `0.7432` |
| G-1d | `H²` | `(+2.682, +3.056, +1.307)` | `0.343` | `0.7931` |
| G-1e | `|H| = √(HH†)` | `(+1.378, +1.504, +1.034)` | `0.335` | `0.7510` |
| G-1f | species-diagonal of `H` | `(+0.657, +0.934, −0.934)` | `0.335` | `0.7432` |

The best G-1 variant is G-1a/G-1b (eigenvalue lift, cos-sim `0.8839`).
All six fall far short of the `0.99` direction threshold and `Q = 2/3` to
1% precision.

**Note.** G-1a/b reproduce exactly Agent 9's `|λ_i|` and `λ_i`
readings — but here applied as *intermediate propagator weights* rather
than as direct charged-lepton masses, via the retained `Γ_1` species-to-
intermediate transport. The fact that cos-sim and Koide do not change is
a structural consequence: the identity
`diag(Σ) = diag(X)` means the propagator-dressing lift re-expresses
Agent 9's direct reading without introducing any new information. This
is the new structural finding.

### Construction G-2 — Higgs resolvent `(H + shift)^{-1}`

Five shifts tested (0.5, 2, 10, `λ_max + 0.1`, `2λ_max`). Resolvent
smears the eigenvalue triple onto the intermediate subspace via the
same `Γ_1` transport. Best G-2 variant is G-2a (shift 2), cos-sim
`0.8236`. All G-2 variants give Koide Q between `0.334` and `0.345`,
far from `2/3`.

| Variant | Shift | diag(Σ) | Koide Q | cos-sim |
|---|---|---|---|---|
| G-2a | 2 | `(+0.592, +0.519, +1.165)` | `0.345` | `0.8236` |
| G-2b | 10 | `(+0.096, +0.093, +0.111)` | `0.334` | `0.7336` |
| G-2c | 0.5 | `(+0.468, +0.419, +0.834)` | `0.342` | `0.8078` |
| G-2d | `λ_max+ε` | `(+0.446, +0.401, +0.779)` | `0.341` | `0.8046` |
| G-2e | `2λ_max` | `(+0.209, +0.197, +0.281)` | `0.335` | `0.7610` |

**Interpretation.** The resolvent dresses the eigenvalue structure
smoothly; as `shift → ∞` the resolvent becomes `(1/shift) · I` and the
return is democratic. As `shift → 0` it approaches the bare `H⁻¹`
singularity without acquiring the Koide-two-thirds structure.

### Construction G-3 — Higgs-projected weight via the retained Higgs family `M(φ)`

The retained Higgs family is `M(φ) = φ₁ Γ₁ + φ₂ Γ₂ + φ₃ Γ₃`, the
branch-convention EWSB source family. At the retained EWSB axis-1 point
`φ = e_1`, `M = Γ_1` and `|M|² = I`, reproducing the unit-weight
baseline `I_3`. Four variants tested:

| Variant | Structure | diag(Σ) | Koide Q | cos-sim |
|---|---|---|---|---|
| G-3a | `|M(e_1)|² = I` | `(1, 1, 1)` | `0.333` | `0.7071` |
| G-3b | `|M(1, ε, ε)|²` | `(1.020, 1.020, 1.020)` | `0.333` | `0.7071` |
| G-3c | `M(e_1) H^{lift} M(e_1)` (symmetrized) | zero | n/a | n/a |
| G-3d | `H^{lift} + (|M|²−I) pert` | `(+0.657, +0.934, −0.934)` | `0.335` | `0.7432` |

**Interpretation.** G-3 variants confirm Agent 10 v2's Correction-A
finding (species-democratic at every tested order) and show that
symmetrizing the `H`-lift through the retained Higgs family either
re-democratizes (G-3a/b) or collapses to zero (G-3c) or reduces to the
G-1c shape (G-3d). The retained Higgs family carries no extra S_2-
breaking shape beyond what is already in `H`.

### Construction G-4 — lifts of `T_m`, `T_δ`, `T_q` to the intermediate subspace

The retained G1 tangent generators `T_m, T_δ, T_q` span the H-chart
tangent. Eight combinations tested, both in "species-diag-only" form and
"full-lift" form:

| Variant | diag(Σ) | Koide Q | cos-sim |
|---|---|---|---|
| G-4a `I + m_* T_m` | `(+1.657, +1.000, +1.000)` | `0.338` | `0.7864` |
| **G-4b `I + δ_* T_δ`** | `(+1.000, +1.934, +0.066)` | **`0.428`** | **`0.9191`** |
| G-4c `I + q_* T_q` | `(+1.000, +1.000, +1.000)` | `0.333` | `0.7071` |
| G-4d `T_m + T_δ` | `(+1, +1, −1)` | `0.333` | `0.7071` |
| G-4e `T_m + T_q` | `(+1, 0, 0)` | n/a | n/a |
| G-4f `T_δ + T_q` | `(0, +1, −1)` | n/a | n/a |
| G-4g `T_m + T_δ + T_q` | `(+1, +1, −1)` | `0.333` | `0.7071` |
| G-4h `m_* T_m + δ_* T_δ + q_* T_q` | `(+0.657, +0.934, −0.934)` | `0.335` | `0.7432` |

**The best variant across all 27 tested** is G-4b (`I + δ_* T_δ`):
cos-sim `0.9191`, Koide `Q = 0.4288` — still `36%` off the target
`2/3` and below the `0.99` direction threshold. `T_δ` is the unique
retained tangent generator with nonzero diagonal entries `(0, 1, −1)`;
adding `δ_*` times `T_δ` to `I` produces the `(1, 1+δ_*, 1−δ_*)` shape
that happens to be closest to the observed direction among all lifts
tested, but falls well short of a match.

## Evidence of the negative result — specific quantitative outputs

The twenty-seven variants collectively span the natural retained
constructions of `W(H)`. Summary statistics:

- Best cos-similarity across all variants: **`0.919117`** (G-4b).
- Best `|Q − 2/3|`: **`0.2388`** (G-4b, i.e., `Q = 0.4279`).
- Number of variants achieving cos-sim `≥ 0.99`: **0**.
- Number of variants achieving `|Q − 2/3| < 0.01`: **0**.
- Number of variants producing three genuinely distinct diagonal
  entries: **14 / 27** (so non-degeneracy is not the obstruction;
  matching is).

PDG target: `direction = (0.01647, 0.23688, 0.97140)`,
`Q_PDG = 0.66666`.

## Four-outcome verdict

**`AVENUE_G_NO_MATCH`**

No retained `W(H)` construction in the tested family matches the observed
charged-lepton direction and Koide `Q = 2/3` simultaneously. The best
direction cos-similarity is `0.919 < 0.99`; the best Koide deviation is
`|Q − 2/3| = 0.239`, an order of magnitude above a `1%` partial-match
threshold.

### Why this is not `PARTIAL_MATCH`

`PARTIAL_MATCH` in the task brief requires three distinct weights AND
Koide `Q ≈ 2/3` with a direction miss `> 1%`. Best Koide is `0.428`,
which is `36%` off `2/3`, not a `1%` miss. No variant clears the
partial-match bar.

### Why this is not `UNDERDETERMINED`

`UNDERDETERMINED` in the task brief requires at least one `W(H)` that
matches observation but requires an added retained assumption. No
variant matches observation, so the underdetermined pattern does not
apply. This is the sharp-negative outcome: no ambiguity, no match.

### Why this is not `CLOSES_G5`

No variant comes within `1%` in direction or Koide.

## Retained / ad-hoc audit — per-construction retained provenance

All constructions use only:

- `Γ_0, Γ_1, Γ_2, Γ_3` — retained `Cl(3)` generators on `C^16`
  ([DIRAC_CORE_CARD_NOTE.md](./DIRAC_CORE_CARD_NOTE.md)).
- `P_{O_0}, P_{T_1}, P_{T_2}, P_{O_3}` — retained HW-stratum projectors
  ([DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)).
- `H(m, δ, q_+) = H_{base} + m T_m + δ T_δ + q_+ T_q` — retained affine
  Hermitian on the `hw=1` triplet
  ([G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md](./G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md)).
- G1 chamber pin `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` —
  observational from PDG PMNS angles (same as G1 closure uses; no new
  input).
- `M(φ)` Higgs family from retained EWSB source — axis-1 point is
  retained.
- PDG charged-lepton masses used ONLY in the final cos-similarity /
  Koide comparison, never as inputs to any construction.

Per-construction retention classification:

| Construction | Retained inputs only? | New assumption? |
|---|---|---|
| G-1 (H-lift) | Yes | No. Uses G1's `H` at G1's pin, canonical `Γ_1` transport to intermediate subspace. |
| G-2 (resolvent) | Yes at the shift scale + `H` | The `shift` parameter is a free scalar; its five values are probes, not retained pins. Any *particular* shift is a new parameter. |
| G-3 (Higgs-projected) | Yes | No. Uses retained `M(φ)` at retained axis-1 point. |
| G-4 (T-generator lifts) | Yes | No. Uses G1's retained tangent generators `T_m, T_δ, T_q` at G1's pin coordinates. |

Even when all constructions are purely retained (G-1, G-3, G-4), none
matches observation. G-2 introduces a free shift that could in principle
be fixed observationally; the test shows it still cannot match.

### The propagator-dressing identity is the essential obstruction

A structural finding sharpens the negative: under the canonical
intermediate-subspace lift of a 3×3 operator `X`, the second-order
return satisfies

```
diag(P_{T_1} Γ_1 (lift_int X) Γ_1 P_{T_1}) |_species = diag(X)
```

exactly (verified numerically for all six G-1 variants, off-diagonal
parts contribute only to the off-diagonal of the species block). So the
"Higgs-dressed propagator" construction transports the species-diagonal
content of `X = f(H)` directly into `diag(Σ)`. This means Avenue G is
structurally equivalent to asking "is `diag(f(H))` in the direction of
`(m_e, m_μ, m_τ)` for some retained `f`?" — and this is exactly the
question Agents 9 and 12 already investigated, only now in the
intermediate-subspace-lift framing.

The propagator-dressing framing is structurally distinct from Agents 9,
12, 13 in its *construction mechanism* — it tests a genuinely new
operator (a weight on `(O_0 ⊕ T_2)`) rather than a direct mass
assignment on `T_1` — but the `Γ_1` transport identity reveals that the
diagonal information content is the same. This is itself a useful
structural theorem: "the `Γ_1`-second-order-return species-diagonal is a
transport invariant — diag of any species-indexed intermediate weight."

## What this does NOT claim

- No closure of G5. Koide `Q_ℓ = 2/3` remains UNRETAINED.
- No demotion of G1's closure. G1's `H(m, δ, q_+)` is used exactly as
  retained; the negative result is about charged-lepton Koide, not about
  G1's PMNS map.
- No claim that `H` plays no role at all in charged-lepton structure.
  Only that the specific Higgs-dressed-propagator construction with G1's
  `H` at G1's pin does not reproduce the charged-lepton direction or
  Koide.
- No claim that all possible retained `W(H)` were tested. Twenty-seven
  variants covering four structurally distinct families were tested.
  Future agents may construct further retained variants; any such
  variant must still pass the transport identity
  `diag(Σ) = diag(X)`, so is subject to the same obstruction.
- No overlap with Agent 16 (retained stationarity principle) or Agent 17
  (fourth-order mixed-`Γ` return).
- No new retained axiom or operator introduced.

## Relationship to Agents 9, 12, 13 — lane distinctness

- **Agent 9 (`G5_VIA_G1_H_CHARGED_LEPTON_NOTE.md`)** tested H directly as
  the charged-lepton mass operator on `T_1` (eigenvalues / squared
  eigenvalues as masses). Verdict `NO_NATURAL_MATCH`. This lane is
  **construction** on `T_1` itself.
- **Agent 12 (`G5_S2_BREAKING_PRIMITIVE_SURVEY_NOTE.md`)** tested `H`
  lifted POST-HOC to `T_2` diagonal weights. Verdict `AMBIGUOUS` (signed
  diagonal breaks S_2, `|H|`-diagonal restores it). This lane is
  **observation** on `T_2` diagonal weights.
- **Agent 13 (`G5_JOINT_PMNS_KOIDE_PINNING_NOTE.md`)** proved
  `dim(V_H ∩ V_D) = 0` on the hw=1 Hermitian 3×3 algebra. This is a
  **structural** statement about tangent overlap.
- **This note (Agent 15, Avenue G)** tests `W(H)` as a PROPAGATOR
  DRESSING inside the second-order Γ_1 return on `C^16`. The construction
  differs in that the weight operator lives on `(O_0 ⊕ T_2)` and is
  pulled back from `T_1` via the retained `Γ_1` transport — genuinely
  new as a **mechanism**. The sharp new structural finding is the
  transport identity `diag(Σ) = diag(X)`, which reveals that the
  diagonal information content of Avenue G reduces to Agent 9's /
  Agent 12's reading even though the mechanism is new.

The four lanes are:

| Lane | Agent | Mechanism | Verdict |
|---|---|---|---|
| H as CL mass on T_1 | 9 | direct | NO_NATURAL_MATCH |
| H lifted to T_2 diag | 12 | post-hoc | AMBIGUOUS |
| V_H ∩ V_D structure | 13 | orthogonality theorem | dim = 0 |
| **H as propagator dressing on C^16** | **15 (this note)** | **transport via Γ_1** | **NO_MATCH** |

## Dependency contract

Retained authorities validated on live `main` (or the inspiring-meitner
worktree) before this runner is valid:

- `frontier_dm_neutrino_dirac_bridge_theorem.py` — **28 PASS / 0 FAIL** —
  defines `Γ_1`, first-order vanishing, `I_3` second-order return.
- `frontier_g1_physicist_h_pmns_as_f_h.py` — **43 PASS / 0 FAIL** —
  defines `H(m, δ, q_+)` used in every construction.
- `frontier_g5_gamma_1_second_order_return.py` — **20 PASS / 0 FAIL** —
  Agent 10 v2's shape theorem, which identifies `(w_{O_0}, w_a, w_b)`
  as the three weight slots this runner attempts to fill.
- `frontier_g5_s2_breaking_primitive_survey.py` — **31 PASS / 0 FAIL** —
  Agent 12's survey, which this runner does not duplicate.
- `frontier_g5_joint_pmns_koide_pinning.py` — **9 PASS / 0 FAIL** —
  Agent 13's `dim(V_H ∩ V_D) = 0` theorem.
- `frontier_g5_via_g1_h_charged_lepton.py` — **14 PASS / 0 FAIL** —
  Agent 9's direct reading.

Framework-native retained constants used (none as fit parameters):
`E_1 = √(8/3)`, `E_2 = √8 / 3`, `γ_H = 1/2`, G1 chamber pin
`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`. PDG masses used
only for comparison.

## Paper-safe wording

> Within the retained `Cl(3)/Z³` framework on the chirality-doubled
> lattice `C^16`, the natural Higgs-dressed intermediate propagator
> construction — replacing the unit-weight intermediate projector
> `P_{O_0} + P_{T_2}` in the retained second-order `Γ_1` return by a
> weight operator `W(H)` built from G1's retained affine Hermitian
> `H(m, δ, q_+)` at the G1 observational chamber pin — does not
> reproduce the observed charged-lepton mass direction or Koide
> `Q = 2/3`. Twenty-seven variants across four construction families
> (natural `Γ_1`-transport lift of `f(H)`, Higgs resolvent
> `(H + shift)^{-1}`, retained Higgs-family-projected weight at EWSB
> axis 1, and lifted combinations of the `T_m, T_δ, T_q` tangent
> generators) were tested. Best direction cos-similarity is
> `0.919 < 0.99`; best Koide deviation is `|Q − 2/3| = 0.239`. The
> retained second-order return satisfies the structural transport
> identity
> `diag(P_{T_1} Γ_1 (lift_{int} X) Γ_1 P_{T_1})|_{species} = diag(X)`,
> reducing the diagonal content of Avenue G to the species-diagonal
> content of `f(H)` — a sharp structural reason why Avenue G cannot
> succeed beyond the limits already found in Agent 9's direct reading.
> Avenue G is therefore closed as `AVENUE_G_NO_MATCH`; G5 closure
> cannot be forced via Higgs propagator dressing on `C^16` alone.

## Open successor directions (not claimed here)

The runner confirms the transport identity
`diag(Σ) = diag(X)` for the lift
`lift_int X = B_{int} X B_{int}^†`. Any successor retained construction
must therefore introduce EITHER

1. a weight operator `W` whose species-block is NOT the lift of a 3×3
   operator via the canonical `Γ_1` transport (e.g., `W` couples chirality
   tastes or uses higher HW strata in a way the canonical lift cannot
   reproduce), OR
2. a higher-order `Γ_1` return (fourth-order or mixed with other `Γ_a`)
   where the transport identity fails, OR
3. a retained observational pin on the charged-lepton side analogous to
   G1's PMNS pin (Option 2 in
   [CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md)).

The first two routes are Agent 17's lane (fourth-order mixed-Γ) and
possibly a taste-resolved variant; the third is Agent 11's observational-
pin lane.

## Atlas status

Proposed row for [`DERIVATION_ATLAS.md`](./publication/ci3_z3/DERIVATION_ATLAS.md)
Section F (Flavor / CKM portfolio):

| Tool | Authority | Status |
|---|---|---|
| `frontier_g5_avenue_g_higgs_dressed_propagator.py` | This note | **`AVENUE_G_NO_MATCH`**; 10 PASS / 0 FAIL; 27 variants across 4 construction families; best cos-sim `0.919`, best `|Q−2/3| = 0.239`; transport identity `diag(Σ) = diag(X)` established as structural obstruction. |

## Status

**`AVENUE_G_NO_MATCH` open-lane closure note.** Not a G5 closure; a
rigorously-tested negative for the Higgs-dressed propagator lane. The
value is the explicit structural transport identity reducing Avenue G's
diagonal content to Agent 9's question, and the quantitative closure of
all four natural retained construction families without a match.
