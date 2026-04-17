# Higher-Order Structural Theorems on the Charged-Lepton Sector

**Date:** 2026-04-17
**Status:** three exact structural theorems + one companion survey + observational-pin closure spec
**Runners (8):**
- `scripts/frontier_higgs_dressed_propagator_v1.py` (7 PASS)
- `scripts/frontier_higgs_dressed_propagator_transport_identity.py` (10 PASS)
- `scripts/frontier_koide_cone_variational_principle_survey.py` (20 PASS)
- `scripts/frontier_koide_cone_real_irrep_democracy.py` (22 PASS)
- `scripts/frontier_fourth_order_mixed_gamma_return.py` (11 PASS)
- `scripts/frontier_s2_breaking_primitive_survey.py` (31 PASS)
- `scripts/frontier_charged_lepton_observational_pin_closure.py` (32 PASS)

Total: 133 PASS, 0 FAIL.

## Purpose

This note develops three additional structural theorems on the
retained `Cl(3)/Z^3` surface that close the three natural
framework-derives-Koide routes, plus the `S_2`-breaking primitive
survey and the observational-pin closure specification. Each
theorem is a corollary of the retained authorities; none requires
additional axioms.

## Theorem 4: canonical intermediate-subspace-lift transport identity

For any weight operator `X` on the intermediate subspace
`O_0 ⊕ T_2` and any Cl(3)-covariant lift
`lift_{int}: M_3(ℂ) → M_4(ℂ)`:
```
diag(P_{T_1} Γ_1  ·  lift_{int}(X)  ·  Γ_1 P_{T_1})|_{species}  =  diag(X).
```

### Proof

The `Γ_1` hopping structure maps species `i ∈ {1, 2, 3}` to
intermediate state `I(i) ∈ {O_0, T_2(1,1,0), T_2(1,0,1)}` via the
table in Theorem 2. For any Cl(3)-covariant lift of `X` onto the
intermediate subspace, the diagonal matrix element at species `i` is
```
[Σ]_{ii}  =  ⟨X_i| Γ_1 lift_{int}(X) Γ_1 |X_i⟩
          =  ⟨I(i)| lift_{int}(X) |I(i)⟩
          =  [X]_{I(i), I(i)}.
```
The first equality uses `Γ_1 |X_i⟩ = |I(i)⟩` (the hopping table).
The second uses orthogonality of the intermediate basis. Hence the
species diagonal of `Σ` equals the intermediate diagonal of `X`
evaluated at the image of the hopping map, independent of the lift
mechanism. □

### Corollary

Any retained Higgs-dressed-propagator construction of the form
`Σ(W) = P_{T_1} Γ_1 · W · Γ_1 P_{T_1}` cannot generate
species-resolved diagonal content beyond what the diagonal of `W`
itself supplies. In the physically-relevant diagonal-in-axis-basis
channel (Dirac-bridge theorem's `U_e = I_3`), this reduces the
problem of finding a charged-lepton-matching weight operator to the
problem of finding an intermediate-state diagonal matching the
observed species mass ratios — which is exactly the observational
pin.

### Numerical artifact in the eigenvalue channel

A striking but structurally artificial near-match: the resolvent
construction
```
W(H)  =  1 / (λ − H_{lift})
```
with `H_{lift}` a Cl(3)-covariant lift of the retained neutrino-
mixing Hermitian and
`λ = 0.01594` (the distance of the neutrino observational pin from
the retained chamber boundary) gives
```
Q_{eig}  =  0.6664,
cos-similarity(eigenvalue triple, observed √m direction)  =  0.9963.
```
In the **eigenvalue** channel of `Σ(W)`. However, the Dirac-bridge
theorem's `U_e = I_3` constraint excludes the eigenvalue channel
from the physical charged-lepton mass readout — physical masses are
the diagonal entries in the axis basis, not the eigenvalues of a
non-diagonal matrix. In the physical diagonal channel, the best
cos-similarity across 27 tested `W(H)` variants is 0.919, well below
the 0.99 threshold for a structural match. The eigenvalue-channel
near-match is a structural artifact of the Cl(3)-covariant-lift
transport, not a signal.

Runners:
- `scripts/frontier_higgs_dressed_propagator_v1.py`
- `scripts/frontier_higgs_dressed_propagator_transport_identity.py`

## Theorem 5: no retained C_3-invariant variational principle forces the Koide cone

Six candidate variational principles tested for selecting the Koide
cone `a_0² = 2|z|²` as a stationary point on the retained `hw=1`
triplet. All six close negatively.

### Candidate survey

| # | Principle | Retained? | Stationary on Koide cone? | Fixes cone point? |
|---|---|---|---|---|
| H-1 | Cauchy-Schwarz midpoint `(Q − 1/3)(1 − Q)` | AD-HOC | YES by construction | NO (whole cone is a degenerate critical set) |
| H-2 | Max-entropy with `C_3` character constraint | AD-HOC (the "char constraint" IS Koide — circular) | — | — |
| H-3 | `log|det(D + J)|` partition extremum | RETAINED | NO (stationary at full degeneracy `Q = 1/3`; Hessian triply-degenerate and strictly negative) | NO |
| H-4 | Fisher-Rao geodesic midpoint (uniform → corner) | AD-HOC | NO (`Q ≈ 0.4226`) | NO |
| H-5 | `C_3` norm extremum `α|v_∥|² + β|v_⊥|²` | AD-HOC | NO (reduces to the Candidate-B `α = β` no-go of §5.3 in [STRUCTURAL_NO_GO_SURVEY_NOTE.md](./STRUCTURAL_NO_GO_SURVEY_NOTE.md)) | NO |
| H-6 | Retained Matsubara `K_{ii}` shape theorem | RETAINED (from Theorem 2) | NO (stationary at full degeneracy or 2+1 split; observed hierarchy not selected) | NO |

Retained-and-cone-forcing intersection: **empty**.

### Deep reason

Retained `C_3`-invariant kernel `K` implies `C_3`-invariant
variational functional `F[v]` implies stationary points of `F`
respect the `C_3` action. The observed charged-lepton cone point has
no residual `S_2` symmetry on the axes `{2, 3}` (the observed
pinned triple has `w_a ≠ w_b`), so no retained `C_3`-invariant
principle can select it without first breaking `C_3`. This matches
the "missing `S_2`-breaking primitive" diagnosis of the shape
theorem: the retained framework's stationary points are at
fully-symmetric or 2+1 degenerate configurations.

Runner: `scripts/frontier_koide_cone_variational_principle_survey.py`.

### Real-irrep-block democracy (candidate primitive)

A sharp structural observation: the Koide cone `a_0² = 2|z|²` IS
the unique negative-definite maximum of the **unweighted**
block-log-volume
```
S  =  log(a_0²)  +  log(2|z|²)
```
at fixed `|v|²`, verified symbolically with negative-definite
Hessian. In information-theoretic terms:
```
σ  ≡  a_0² / (a_0² + 2|z|²),
Koide Q = 2/3  ⟺  σ = 1/2   (the `[0, 1]` midpoint).
```

However, the retained `log|det(D)|` generator is **dimension-
weighted** (one log-term per complex irrep, weighted by multiplicity).
The two-dimensional nontrivial-character subspace
`E_ω ⊕ E_{ω²}` contributes two log terms (one per complex irrep),
versus the one-dimensional trivial-character subspace `E_+`
contributing one log term. The dimension-weighted stationary point
is at
```
σ_{retained}  =  1/3  ≠  1/2  =  σ_{Koide}.
```
The gap is a single factor-of-2 weighting on the 2D nontrivial-
character block.

**Real-irrep-block democracy** is the named candidate primitive:
treating the 1D trivial character block and the 2D nontrivial
character block on **equal** footing — one log term per real-irrep
block, independent of complex-irrep multiplicity. If retained on
a future framework extension, this primitive would derive Koide
uniquely as the unique negative-definite maximum.

The real-irrep-democracy principle is NOT currently retained on
`main`. It is identified here as a sharply-posed construction
target for future retention work.

Runner: `scripts/frontier_koide_cone_real_irrep_democracy.py`.

## Theorem 6: fourth-order signed Clifford ordering cancellation

**Theorem.** For any even-parity fourth-order product of spatial
Clifford generators `Γ_{i_1} Π Γ_{i_2} Π Γ_{i_3} Π Γ_{i_4}` with
intermediate projector `Π` returning to `T_1`:

1. Individual orderings of each mixed-Γ multiset `{Γ_a², Γ_b²}`
   (with `a ≠ b`) produce species-resolved single-species diagonals
   through `O_3` participation — a new structural observation that
   mixed-`Γ` can reach the `T_2(0, 1, 1)` state via `O_3`.

2. Signed ordering sums within each multiset vanish pairwise:
   ```
   Σ_orderings (−1)^{σ(ordering)} diag(Γ_ordering)  =  0
   ```
   identically, because the `φ`-monomial weight from the EWSB
   expansion depends only on the multiset, not on the ordering.

3. The cancellation is **stronger** than the residual `S_2`
   obstruction and is **independent** of any retained or
   non-retained `φ`-reweighting scheme.

4. Parity selection restricts species-diagonalizing orderings to
   21 of the 81 possible length-4 sequences `(Γ_{i_1}, …, Γ_{i_4})`
   (even axis counts); the others either do not species-diagonalize
   on `T_1` or reduce to reachability-violating sequences.

*Proof sketch.* Enumerate the 21 even-parity species-diagonalizing
sequences. For each multiset `{Γ_a², Γ_b²}` (a ≠ b), the orderings
split into pairs related by axis-swaps `a ↔ b`. Each pair
contributes species-diagonal entries of the form `(±δ_c, 0, 0)` or
`(0, ±δ_c, 0)` etc., where `c` is the axis not in `{a, b}`. Summing
signed contributions within each multiset gives
`+1 + 1 − 1 − 1 + 0 + 0 = 0`. The `φ`-monomial weight factors out
of the multiset sum (because it is a symmetric function of
`(φ_{i_1}, …, φ_{i_4})`), so no reweighting can lift the
cancellation. □

*Consequence.* The fourth-order retained spatial-Clifford +
EWSB-weighted Higgs family is ruled out as a Koide-forcing
mechanism.

Runner: `scripts/frontier_fourth_order_mixed_gamma_return.py`.

## Theorem 6 companion: Eight-channel S_2-breaking primitive survey

Eight independent retained channels surveyed for breaking the
residual `S_2` symmetry on axes `{2, 3}`:

1. Anomaly-trace subcomponents (`Tr[Y], Tr[Y^3]`, …)
2. Higher-order Higgs invariants (six-point `V_{sel}` extensions)
3. Lattice-geometric operators (body-diagonal `Γ_1 Γ_2 Γ_3`,
   face-diagonals, cube-corner products)
4. Chirality-specific operators (`γ_5`, `P_L`, `P_R`, `Ξ_5`,
   `γ_5 Ξ_5`)
5. Cl(3) bilinears (12 independent bilinears)
6. Neutrino-mixing Hermitian `H(m_*, δ_*, q_+*)` lifted to `T_2`
7. Time-direction operators (`Γ_0, Γ_0 Γ_i, Γ_0 Γ_2 Γ_3`)
8. Retained Schur cascade `c_0 I + c_1 P_{C_3} + c_2 P_{C_3}²`

Seven channels close as exactly `S_2`-symmetric on `T_2` diagonals.
The single ambiguous case (channel 6, neutrino-mixing Hermitian
lifted to `T_2`) has a signed diagonal `(−0.934, +0.934, +0.657)`
that breaks `S_2` via the `T_δ`-tensor's `(0, 1, −1)` structure;
however, the absolute-value interpretation required for physical
mass readout restores `w_a = w_b` by accident of the same
antisymmetry, best cos-similarity to the observed direction is
0.74, and the `T_1 → T_2` lift is post-hoc rather than retained.

No retained sole-axiom `S_2`-breaking primitive is present on the
current framework surface.

Runner: `scripts/frontier_s2_breaking_primitive_survey.py`.

## Theorem 7: charged-lepton observational-pin closure

Let
```
(w_{O_0}, w_a, w_b)  =  (m_e, m_μ, m_τ) / m_τ
                     =  (2.71 × 10^{−4}, 5.61 × 10^{−2}, 9.44 × 10^{−1}).
```

**Claim.**
1. The triple lies strictly inside the retained chamber defined
   by constraints R1 (positivity), R2 (`Γ_1` reachability), R3
   (chiral-off-diagonal), R4 (scale freedom), R5 (`S_2`-broken,
   supplied by the pin).
2. The triple is unique **as a set** up to overall scale. A residual
   `S_2` labeling ambiguity on `w_a ↔ w_b` persists on the retained
   surface (no retained operator breaks axis-{2, 3} exchange), but
   Koide `Q` and the `Σ` spectrum are `S_2`-invariant, so the
   closure verdict is unaffected.
3. Koide `Q_{pin} = 0.6666605` matches `2/3` to
   `|Q − 2/3| = 6.15 × 10^{−6}` (PDG precision). This match is a
   tautological algebraic consequence of the pin equaling the
   observed triple, which satisfies Koide to PDG precision.

**Closure class:** retained-map-plus-observational-promotion,
identical to the retained neutrino-mixing closure's class. Not
sole-axiom.

**Strict-review verdict:** `TRUE_NO_PREDICTION`. The map
`(w_{O_0}, w_a, w_b) ↦ diag(m_e, m_μ, m_τ)` is 3→3 and produces no
spare observable analogous to the neutrino 3→4 map (which produces
`δ_CP ≈ −81°` as a retained forecast).

Four structural consequences of the shape theorem are testable but
SM-consistent:
- Lepton-flavor-violation zeros at leading order (SM-allowed but
  far below current MEG-II / Belle-II bounds).
- No charged-lepton EDM beyond SM (SM CL EDMs are already below
  observable thresholds).
- Electron-isolation hopping-ratio asymmetry `12.30` — equals the
  PDG ratio-of-ratios `(m_μ/m_e) / (m_τ/m_μ)` tautologically.
- Combined neutrino/charged-lepton consistency tests at DUNE /
  Hyper-K.

None is a genuinely new numerical prediction beyond SM baseline.

Runner: `scripts/frontier_charged_lepton_observational_pin_closure.py`.

## Three named missing primitives

Each theorem identifies a sharply-posed candidate primitive that,
if retained on a future framework extension, would derive the
charged-lepton hierarchy + Koide sole-axiom:

- **Primitive A** (Theorem 4). Non-Cl(3)-covariant retained lift of
  the intermediate propagator `O_0 ⊕ T_2` that carries species-
  resolved diagonal information not inherited from its source
  weight via the transport identity.

- **Primitive B** (Theorem 5). Real-irrep-block democracy in the
  variational weighting of `log|det(D)|`: one log-term per
  real-irrep block, independent of complex-irrep multiplicity.

- **Primitive C** (Theorem 6). A mechanism breaking the signed
  Clifford ordering cancellation within each multiset `{Γ_a², Γ_b²}`
  at fourth order: a retained ordering-sensitive weight depending
  on sequence, not only on multiset.

Each primitive is a specific construction target for future
retention work.

## What this note does not claim

- The three higher-order theorems do NOT close the charged-lepton
  mass hierarchy problem. They close three specific framework-
  derives routes and name three candidate primitives whose future
  retention would close the problem.
- The observational-pin closure of Theorem 7 is `TRUE_NO_PREDICTION`
  on strict review. It does not supply a new numerical forecast
  beyond SM baseline.

## Paper-safe wording

> Three higher-order structural theorems close the three natural
> framework-derives-Koide routes. The transport identity
> (Theorem 4) proves that retained Higgs-dressed propagator
> constructions inherit their species diagonal trivially from the
> weight's intermediate diagonal. The variational-principle survey
> (Theorem 5) establishes that no retained `C_3`-invariant
> variational principle on the current surface selects the Koide
> cone; the sharp real-irrep-block democracy principle is a
> candidate primitive that would derive Koide if retained.
> The fourth-order mixed-Γ cancellation theorem (Theorem 6) rules
> out the fourth-order retained spatial-Clifford + EWSB-weighted
> Higgs family via signed ordering cancellation. Charged-lepton
> closure at the retained-map-plus-observational-promotion class
> follows from a three-real observational pin on the shape-theorem
> weight triple (Theorem 7), with strict-review verdict
> `TRUE_NO_PREDICTION`.

## Status

**REVIEW.**
