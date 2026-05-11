# Koide A1 Route D — Newton-Girard Polynomial Structure Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Route D closure attempt
for the A1 √2 equipartition admission on the charged-lepton Koide
lane.
**Status:** source-note proposal for a negative Route D closure —
shows that the candidate polynomial-coefficient identification
`p_2/e_1² = 2/3` (equivalently `e_1² = 6 e_2`, equivalently
`|b|²/a² = 1/2`) cannot be derived from retained Cl(3)/Z³ content
via Newton-Girard polynomial structure alone. Five independent
structural barriers each block the proposed derivation. The A1
admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-route-d-newton-girard-20260508
**Primary runner:** [`scripts/cl3_koide_a1_route_d_newton_girard_2026_05_08_routed.py`](../scripts/cl3_koide_a1_route_d_newton_girard_2026_05_08_routed.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_route_d_newton_girard_2026_05_08_routed.txt`](../logs/runner-cache/cl3_koide_a1_route_d_newton_girard_2026_05_08_routed.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit lane
has full authority to retag, narrow, or reject the proposal.

## Question

`KOIDE_A1_DERIVATION_STATUS_NOTE.md`
identifies **Route D** (Newton-Girard polynomial structure) as a
candidate closure route for the A1 √2 equipartition admission.
The proposed structural identification is

> `V(Φ)  =  [e_1²  −  6 e_2]²  =  0`  on Herm_circ(3),

equivalently the rational coefficient identity

> `p_2 / e_1²  =  2/3`

where `(p_k, e_k)` are the power sums and elementary symmetric
polynomials in the eigenvalues `λ_k` of the retained C_3-equivariant
Hermitian circulant
`H = aI + bC + b̄C^2` on hw=1. By Newton-Girard,
`p_2 = e_1² - 2 e_2`, so the two forms are equivalent.

This is **structurally distinct** from the Lie-algebraic norm routes
that closed Routes E and F negatively
([`KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md`](KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md),
[`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)).
Routes E and F failed because their candidate `1/2` values were
**convention-dependent under continuous root-length / hypercharge
normalization conventions**. Route D's `2/3` is by contrast a
**rational coefficient in a polynomial identity** — its trap profile,
if it has one, must be different.

**Question:** Can the structural identification
`p_2/e_1² = 2/3` (equivalently `e_1² = 6 e_2`, equivalently
`|b|²/a² = 1/2`) be derived from retained Cl(3)/Z³ content via
Newton-Girard polynomial structure alone — no empirical loading, no
new axioms, and crucially without falling into a structurally
analogous trap to Routes E/F?

## Answer

**No.** The identification cannot close from retained content alone.
Five independent structural barriers each independently block the
proposed derivation. The trap profile is **materially different** from
Routes E/F (discrete weight-class choice rather than continuous norm
convention), but it is **structurally analogous**: the value `2/3`
depends on a convention/weight-class choice the framework does not
make.

The five barriers (each verified numerically and symbolically in the
paired runner, 33/33 PASS):

1. **Newton-Girard is identity, not constraint (D1).** The
   Newton-Girard relation `p_2 = e_1² − 2 e_2` is a textbook bijection
   between power sums and elementary symmetric polynomials. It holds
   for any 3-tuple of (real or complex) numbers and imposes ZERO
   structural constraint. The runner verifies the identity holds
   exactly for 50/50 random triples and on 50/50 random circulants
   while the ratio `p_2/e_1²` ranges over `[0.336, 10.481]` — clearly
   not pinned at `2/3`. The Newton-Girard machinery alone therefore
   does not single out any specific value.

2. **Block-counting weight ambiguity (1,1) vs (1,2) (D2).** The
   polynomial form `V_{(1,1)} = e_1² - 6 e_2` (which vanishes at A1)
   corresponds to the **multiplicity-weight** extremum on Herm_circ(3)
   (one scalar slot per real isotype: trivial = 1, doublet = 1).
   The equally-natural **dimensional-weight** extremum (real-dim
   weighting: trivial = 1, doublet = 2) gives a different polynomial
   structure and lands at `kappa = 1` (NOT A1). This is **exactly the
   same `(1,1)`-vs-`(1,2)` weight ambiguity flagged as a "minor
   structural residue" by the retained
   [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
   §4 ("Residue"). Route D's "specific 6 coefficient" reproduces this
   weight-class choice in polynomial-coefficient clothing; it does not
   escape it.

3. **Brannen ansatz + extra input required (D3).** On a generic
   Hermitian 3×3 operator outside Herm_circ(3) (i.e., not C_3-equivariant),
   `p_2/e_1²` ranges widely. Even on the retained Brannen circulant
   ansatz `λ_k = a + 2|b|cos(arg b + 2πk/3)`, the ratio is
   `p_2/e_1² = 1/3 + (2/3)(|b|/a)²`, a continuous function of `|b|/a`.
   The retained content (R1+R2 from
   [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md))
   forces the Brannen form, but the SPECIFIC value `|b|/a = 1/√2`
   requires a separate principle.

4. **Polynomial-coefficient circularity (D4).** Substituting Brannen
   parameters into the polynomial form gives the symbolic identity

   ```
   e_1² − 6 e_2 = 9 (2|b|² − a²),

   V(Φ) = [e_1² − 6 e_2]² = 81 (a² − 2|b|²)².
   ```

   So `V(Φ) = 0 ⟺ a² = 2|b|²` (Frobenius equipartition). The
   polynomial form is **algebraically equivalent** to the open A1
   admission, written in different coordinates. The polynomial
   coefficient `6` is exactly the Frobenius factor `n(n−1) = 3·2`
   counting off-diagonal entries — it is the Frobenius admission, not
   a derivation of it.

5. **No symmetric-polynomial-only extremization picks A1 (D5).** A
   scan over candidate symmetric-polynomial functionals on
   `(e_1, e_2, e_3)` of Herm_circ(3) confirms that none has a critical
   point at A1 without additional input:

   - **Discriminant** of the characteristic polynomial: nonzero at A1
     (eigenvalues remain non-degenerate); `d(Disc)/dr ≠ 0` at A1.
   - **Tschirnhaus depressed cubic** coefficient `p = e_2 − e_1²/3`:
     equals `−3 r²` at A1 (free parameter, no special vanishing).
   - **Ratio `e_1²/e_2`**: equals 6 at A1 (by construction, `6 = n(n-1)`
     Frobenius factor); but `d/dr [e_1²/e_2] ≠ 0` at A1 (NOT
     extremized).

   The "selection" of A1 must come from external input (block-counting
   weights, Frobenius equipartition, irrep-multiplicity counting), not
   from polynomial extremization alone.

The combined picture: **Route D is structurally barred** in a way
that is materially different from Routes E and F, but ultimately
falls to a structurally analogous trap. Routes E/F: continuous
norm-convention dependence. Route D: discrete weight-class choice.
All three: the value depends on a convention the framework does not
make.

Closing A1 via this route would require either (a) a new retained
primitive selecting between multiplicity weighting (1,1) and
dimensional weighting (1,2) — equivalent to the open
SO(2)-quotient / weight-class residue flagged by the retained MRU
demotion note; (b) explicit user-approved A3-class admission; or
(c) an alternative polynomial route not based on the
elementary-symmetric / Newton-Girard machinery.

## Setup

### Premises (A_min for Route D closure attempt)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Embed | Cl⁺(3) ≅ ℍ → SU(2)_L; ω pseudoscalar → U(1)_Y; Y_L, Y_H fixed | retained: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| GS | One-Higgs gauge selection: Y_e is arbitrary 3×3 complex matrix | retained: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md) |
| WardFree | No direct Ward lift forces y_τ; Y_e remains free 3×3 | retained: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md) |
| R1 (Circulant) | C_3-equivariant Hermitian on hw=1 is `aI + bU + b̄U^{-1}` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| R2 (Spectrum) | Eigenvalues `λ_k = a + 2|b|cos(arg b + 2πk/3)` | retained: same source R2 |
| C3Pres | C_3[111] is preserved (not broken) on hw=1 in retained content | retained: [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md) |
| 3GenObs | hw=1 BZ-corner triplet has M_3(C) algebra; C_3[111] cycles corners | retained-bounded: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Substep4 | AC_φλ remains the explicit identification residual on hw=1 | retained-bounded: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) |
| KoideAlg | Koide Q = 2/3 ⟺ a₀² = 2|z|² ⟺ \|b\|²/a² = 1/2 ⟺ p_2/e_1² = 2/3 | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| Bridge | Spectrum-operator bridge: a_0² − 2\|z\|² = 3(a² − 2\|b\|²) | retained: [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md) |
| BTF | Block-total Frobenius theorem: (1,1) multiplicity weights yield κ=2 | retained: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md) |
| MRUDemo | MRU SO(2)-quotient is supplementary, not load-bearing | retained: [`KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`](KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md) |
| RouteD_Form | `V(Φ) = [e_1² − 6 e_2]²` is the candidate Newton-Girard form for A1 | route-status note: `KOIDE_A1_DERIVATION_STATUS_NOTE.md` §"Route D" |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end, clearly marked per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms** (Route D's promise is axiom-native; any A3-class
  admission requires explicit user approval and is not proposed here)
- NO admitted SM Yukawa-coupling pattern as derivation input
- NO SO(2)-quotient postulate (per retained MRU demotion)

## The structural identification at issue

**Proposed identification (Route D):**

```
p_2 / e_1²  =  2/3      on circulant Hermitian on hw=1 ≅ ℂ³
```

equivalently `e_1² = 6 e_2`, equivalently
`V(Φ) = [e_1² − 6 e_2]² = 0`, equivalently `|b|²/a² = 1/2` (A1).

Where, for eigenvalues `(λ_0, λ_1, λ_2)` of `H = aI + bC + b̄C^2`:

- `p_k = λ_0^k + λ_1^k + λ_2^k`  (k-th power sum)
- `e_1 = λ_0 + λ_1 + λ_2`  (1st elementary symmetric)
- `e_2 = λ_0 λ_1 + λ_0 λ_2 + λ_1 λ_2`  (2nd elementary symmetric)
- `e_3 = λ_0 λ_1 λ_2`  (3rd elementary symmetric)

The Newton-Girard identity (textbook):

```
p_2  =  e_1²  −  2 e_2.
```

Substituting the Brannen R2 spectrum:

- `p_1 = e_1 = 3a` (cosine sum vanishes at n=3)
- `p_2 = 3a² + 6|b|²` (cosine-squared sum is 3/2 at n=3)
- `e_2 = (e_1² − p_2)/2 = (9a² − 3a² − 6|b|²)/2 = 3a² − 3|b|²`

Therefore A1 (`a² = 2|b|²`) is equivalent to `e_1² = 6 e_2`:

```
A1: a² = 2|b|²
⟺ 9a² = 6 (3a² − 3|b|²) = 18 a² − 18|b|²
⟺ 18|b|² = 9 a²
⟺ a² = 2|b|² ✓
```

Equivalently `p_2/e_1² = (3a² + 6|b|²)/9a² = 1/3 + (2/3)(|b|/a)² = 2/3`
when `(|b|/a)² = 1/2` (A1).

This is mathematically clean and convention-independent at the
identity level (the trigonometric identities involved — `Σcos = 0`,
`Σcos² = 3/2` at n=3 — are pure trigonometry, no Lie-algebraic
normalization). However, the SPECIFIC VALUE `2/3` (or equivalently the
coefficient `6` in `e_1² = 6 e_2`) is **NOT forced** by Newton-Girard
alone. The runner verifies this in five independent ways.

## Theorem (Route D bounded obstruction)

**Theorem.** On A1+A2 + retained CL3_SM_EMBEDDING + retained
gauge-selection + retained C_3-equivariance + retained
Koide-cone algebraic equivalence + retained C_3-preservation +
admissible standard math machinery (elementary symmetric polynomials,
Newton-Girard, discriminant theory):

```
The structural identification

  p_2 / e_1²  =  2/3   on Herm_circ(3)

(equivalently e_1² = 6 e_2, equivalently |b|²/a² = 1/2, equivalently A1)

cannot be derived from retained Cl(3)/Z³ content alone via
Newton-Girard polynomial structure. Five independent structural
barriers each block the derivation:

  (D1) Newton-Girard is identity, not constraint: p_2 = e_1² − 2 e_2
       holds for any 3-tuple of eigenvalues; imposes zero structural
       constraint; cannot single out the value 2/3.

  (D2) Block-counting weight ambiguity: V_{(1,1)} = e_1² − 6 e_2
       (multiplicity weights, kappa = 2 = A1) is one natural form;
       the (1, 2) dimensional-weight form gives a different
       polynomial structure landing at kappa = 1 (NOT A1). The
       framework does not select between (1,1) and (1,2) weights.
       This is the same residue flagged by the retained
       BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM and the MRU_DEMOTION_NOTE.

  (D3) Brannen ansatz + extra input required: on a generic Hermitian
       3×3 operator p_2/e_1² ranges widely; even on the retained
       Brannen ansatz, the ratio is a continuous function of |b|/a
       and is not pinned by the ansatz alone. The SPECIFIC value
       |b|/a = 1/√2 requires a separate selection principle.

  (D4) Polynomial-coefficient circularity: substituting Brannen
       parameters gives V(Φ) = [e_1² − 6 e_2]² = 81 (a² − 2|b|²)².
       The polynomial form is algebraically equivalent to the
       Frobenius equipartition condition (the open A1 admission)
       in different coordinates — same admission, not a derivation.
       The polynomial coefficient '6' is the Frobenius factor
       n(n-1) = 3·2 in disguise.

  (D5) No symmetric-polynomial-only extremization picks A1: a scan
       over candidate functionals (discriminant, Tschirnhaus
       depressed-cubic coefficients, e_k^a/e_l^b ratios) confirms
       none has a critical point at A1 without additional input.
       The Discriminant, p_depressed = e_2 - e_1²/3, and e_1²/e_2 all
       fail to extremize at A1.

Therefore Route D closure of A1 is structurally barred under the
stated retained-content surface. The A1 admission count is unchanged.
```

**Proof.** Each barrier is verified independently in the paired runner;
combining them establishes that no derivation chain from retained
content reaches `p_2/e_1² = 2/3` via Newton-Girard polynomial structure.

### Barrier D1: Newton-Girard is identity, not constraint

The Newton-Girard relation `p_2 = e_1² − 2 e_2` is a textbook
elementary-symmetric-polynomial bijection. It holds for ANY 3-tuple
of (real or complex) numbers and imposes ZERO structural constraint.

The runner verifies this in three ways:

- 50/50 random eigenvalue triples satisfy `p_2 = e_1² − 2 e_2`
  exactly to numerical tolerance.
- 50/50 random Brannen-form circulants give `p_2/e_1²` ranging from
  ≈0.336 to ≈10.481 — clearly not pinned at 2/3.
- Explicit counterexamples `(a, b) = (1, 0.3)`, `(1, 0.7+0.4i)`,
  `(1, 1)`, `(1, 0.5+0.5i = A1)` all satisfy Newton-Girard but only
  one (the last) satisfies A1.

The Newton-Girard machinery is a tool for INTER-CONVERTING (p_k) and
(e_k); it is not a constraint that picks out A1.

### Barrier D2: Block-counting weight ambiguity

Per the retained
[`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
§4 ("Residue, minor, single-named"), there are two natural retained
log-laws on Herm_circ(3):

- **Block-total log-law** with multiplicity weights `(μ, ν) = (1, 1)`:
  extremum at `E_+ = E_perp`, equivalently `kappa = 2`, equivalently
  A1. Polynomial form: `V_{(1,1)} = e_1² − 6 e_2`, vanishes at A1.
- **Det log-law** with dimensional weights `(μ, ν) = (1, 2)`
  (rank P_+ = 1, rank P_perp = 2): extremum at `E_perp = 2 E_+`,
  equivalently `kappa = 1`, NOT A1. Polynomial form lands at a
  different leaf.

The runner verifies that `V_{(1,1)} = e_1² − 6 e_2` vanishes at A1
(target value `9·a²/2` is replaced by 0 there), while the dimensional-
weight form `V_{(1,2)} = e_1² − 3 e_2` does NOT vanish at A1
(`V_{(1,2)} |_A1 = 9a²/2 ≠ 0`). And the (1,2) Lagrangian extremum
(at `r=a`, i.e., `kappa = 1`) gives `e_2 = 0` (a degenerate
manifold), illustrating that polynomial coefficient zeros and
Lagrangian-extremum points are not in 1-1 correspondence.

**The framework does not select between (1,1) and (1,2) weighting.**
This is the same convention residue identified by the retained MRU
demotion note as "minor structural residue" — the SO(2)-quotient
postulate that closes the (1,1) weighting is not derivable from
retained content alone (per
[`KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`](KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md)).

Route D's polynomial-coefficient framing **reproduces this exact
ambiguity** — the "specific 6 coefficient" is the (1,1) weight in
disguise; the framework's failure to select it remains.

### Barrier D3: Brannen ansatz + extra input required

The runner confirms two scopes:

- **Generic Hermitian 3×3** (NOT cyclic-equivariant): random sampling
  gives `p_2/e_1²` ranging from ≈0.795 to ≈1652.704. Newton-Girard
  imposes zero constraint.
- **Brannen circulant** (R1+R2 retained): `p_2/e_1² = 1/3 + (2/3)(r/a)²`
  is a continuous function of `r/a`, taking values in [1/3, ∞).
  Specific values: 1/3 at b=0 (degenerate), 2/3 at A1, 3 at r=2a.

The retained R1+R2 narrows the operator class to circulants but does
not pin the SPECIFIC value `r/a = 1/√2`. A separate principle is
required, which is exactly the open A1 admission.

### Barrier D4: Polynomial-coefficient circularity

The runner verifies symbolically:

```
e_1² − 6 e_2  =  9 (2 r² − a²)   on Brannen ansatz
V(Φ) = [e_1² − 6 e_2]²  =  81 (a² − 2 r²)²  =  81 (a² − 2|b|²)²
```

The polynomial form is **algebraically equivalent** to the Frobenius
equipartition condition `a² = 2|b|²`, which is exactly A1. The
polynomial coefficient `6` is the Frobenius factor `n(n−1) = 3·2`
in disguise — the count of off-diagonal entries on the n×n cyclic
matrix algebra.

So "deriving 2/3 via polynomial structure" reduces to "deriving
`a² = 2|b|²` via Frobenius structure" — but that is exactly the
A1 admission this route was supposed to close. The polynomial framing
is **not a new derivation**; it is the same admission in different
coordinates.

### Barrier D5: No symmetric-polynomial-only extremization picks A1

The runner scans candidate symmetric-polynomial functionals on
`(e_1, e_2, e_3)`:

- **Discriminant** `Δ = 18 e_1 e_2 e_3 − 4 e_1³ e_3 + e_1² e_2² − 4 e_2³ − 27 e_3²`:
  Nonzero at A1 (eigenvalues remain non-degenerate). At
  `(a=1, δ=2/9)`, `Δ ≠ 0` and `dΔ/dr |_A1 ≈ 43.80` (not extremized).
- **Tschirnhaus depressed cubic** `p = e_2 − e_1²/3`: At A1,
  `p = −3a²/2` (free parameter, no special vanishing).
- **Ratio `e_1²/e_2`**: equals 6 at A1 (BY CONSTRUCTION — this IS the
  polynomial form of A1); but `d/dr [e_1²/e_2] |_A1 ≈ 16.97` (not
  extremized).

None of these natural symmetric-polynomial functionals has its
critical point at A1. The "selection" of `e_1² = 6 e_2` must come
from **external input** (block-counting weights, irrep-multiplicity,
Frobenius equipartition) — exactly the input that retained content
does not provide.

## Why the 2/3 = 2/3 numerical match is not a derivation

Within the retained R1+R2 structure, the Brannen circulant ansatz
holds, and the cosine-sum / cosine-squared-sum identities give
`p_1 = 3a` and `p_2 = 3a² + 6|b|²` exactly. The "6" coefficient in
`p_2 = 3a² + 6|b|²` IS structural (it's `n(n-1)` for n=3). But A1's
value `2/3` for the ratio `p_2/e_1²` requires the additional condition
`6|b|² = 3a²`, which is the Frobenius equipartition itself — the open
admission.

So the pattern is:
- LHS = `p_2/e_1²` ranges freely in [1/3, ∞) under R1+R2.
- A1 condition forces this to 2/3 — which IS the value Koide observes
  in PDG charged-lepton masses.
- Both LHS and RHS evaluate to 2/3 BECAUSE A1 is imposed; not because
  Newton-Girard derives A1.

This is a Type-I admission per
`feedback_consistency_vs_derivation_below_w2.md`: "consistency
equality is not derivation."

## Counterfactual: alternative coefficient choices

The runner verifies that other coefficient choices in the polynomial
form correspond to different `kappa` values:

- `e_1² = 6 e_2` (multiplicity weights (1,1)) ⟺ `kappa = 2` ⟺ A1
- `e_1² = 3 e_2` (dimensional weights (1,2)) ⟺ `kappa = 1` ⟺ NOT A1
- `e_1² = C e_2` for general C: extremum equation has different leaves

The framework does not select C. Without a selection principle,
Route D's "specific 6 coefficient" is one choice among an infinite
family of natural polynomial coefficients — not a derivation.

## Comparison to Routes E and F (trap-profile contrast)

The runner explicitly verifies the comparison:

| Route | Trap value | Convention dependence | Profile |
|---|---|---|---|
| **E (Kostant Weyl-vector)** | `\|ρ_{A_1}\|²` | continuous: {1/4, 1/2, 1} under {\|α\|²=1, 2, 4} root-length conventions | continuous norm convention |
| **F (Casimir difference)** | `T(T+1) − Y²` | binary: {1/2, -1/4} under {Y_PDG, Y_SU5} hypercharge conventions | binary hypercharge convention |
| **D (Newton-Girard)** | `e_1² / e_2` | binary discrete: {6, 3} under {(1,1), (1,2)} weight choices | discrete weight-class convention |

**Materially different:** Routes E/F's conventions are CONTINUOUS
NORM CONVENTIONS (root-length / hypercharge); Route D's convention
is a DISCRETE WEIGHT-CLASS CHOICE (multiplicity vs dimensional).

**Structurally analogous:** All three failures share the same
underlying pattern — *the value depends on a choice the framework
does not make*. Routes E/F: framework does not select a Cartan-Killing
normalization. Route D: framework does not select between multiplicity
and dimensional weighting. None of the three is a derivation from
retained content.

This is the new structural finding of this note: **polynomial-
coefficient routes are NOT immune to the convention-dependence trap
that closed Routes E and F.** They face a different VARIANT of the
same trap.

## What this closes

- **Route D negative closure** (bounded obstruction). Five independent
  structural barriers verified, each independently blocking the
  proposed derivation.
- **Sharpens the "candidate" status**: prior status from
  `KOIDE_A1_DERIVATION_STATUS_NOTE.md` was "structurally suggestive,
  not closing." This note demonstrates the polynomial-coefficient
  derivation cannot close from retained content. Future re-attempts
  must supply at least one of:
  - a structural principle selecting between (1,1) multiplicity and
    (1,2) dimensional weighting (equivalent to closing the SO(2)-
    quotient residue from the MRU demotion);
  - a convention-invariant reformulation of the polynomial coefficient
    that does not depend on the weight class;
  - an extremization principle on a symmetric-polynomial functional
    whose critical point uniquely lands at A1.
- **Sister-route implications**: confirms Routes A (Koide-Nishiura
  quartic) and B (Clifford torus) remain the open structurally-distinct
  candidates. Routes C, E, F, and now D are closed negatively. Route A
  is OUTSIDE Theorem 6 (4th-order Clifford cancellation) since V is
  trace-based, so it remains open in a different way than Route D.
- **Audit-defensibility**: explicit numerical counterexamples and
  symbolic identities, removing Route D from the "axiom-native A1"
  candidate list at retained-grade.

## What this does NOT close

- A1 admission count is unchanged. A1 remains a load-bearing
  non-axiom step on the Brannen circulant lane.
- Route A (Koide-Nishiura quartic) remains the strongest open
  candidate (outside Theorem 6's cancellation).
- Charged-lepton Koide closure remains a bounded observational-pin
  package (status from
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  unchanged).
- The retained spectrum-operator bridge theorem
  ([`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md))
  retains its primary status — operator-side `kappa = 2` follows from
  spectrum-side `Q = 2/3` with zero residue. This note does NOT
  retract that — it only addresses the question of whether
  Newton-Girard polynomial structure can derive the spectrum-side
  Koide condition itself, which it cannot.
- The retained block-total Frobenius measure theorem
  ([`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md))
  retains its independent-second-route status. This note's Barrier D2
  is consistent with that note's §4 "minor structural residue"
  finding; it does not change the residue's status.
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Newton-Girard identity (D1) | Demonstrate a 3-tuple of eigenvalues for which `p_2 ≠ e_1² − 2 e_2` (mathematically impossible — refutes any framework using NG). |
| Block-counting weight ambiguity (D2) | Derive a retained selection between (1,1) multiplicity and (1,2) dimensional weighting from existing axioms; that closes the open SO(2)-quotient / weight-class residue and would discharge D2. |
| Brannen ansatz + extra input (D3) | Derive a retained constraint pinning `\|b\|/a = 1/√2` from R1+R2 alone (gauge-only, no extra input); refutes D3. |
| Polynomial circularity (D4) | Find a polynomial expression in `(e_1, e_2, e_3)` that is NOT algebraically equivalent to `a² = 2\|b\|²` and STILL vanishes at A1; refutes D4. |
| No extremization (D5) | Construct a natural symmetric-polynomial functional whose critical point uniquely lands at A1 without external input; refutes D5. |
| Numerical match (anchor) | Falsified if charged-lepton Koide Q deviates significantly from 2/3 in updated PDG; representative anchor values give `Q = 0.666661`, `Q_lin = 0.500005` (sub-0.001% match). |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative Route D boundary: the
Newton-Girard polynomial-coefficient identification is blocked by
identity-not-constraint, weight-class ambiguity, Brannen-ansatz
requirement, polynomial circularity, and absence of extremization
unless a new structural principle (selecting weight class, providing
extremization, or supplying convention-invariant polynomial form) is
supplied.

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "Route D Newton-Girard polynomial structure is structurally suggestive" claim is sharpened from "structurally suggestive, not closing" to "structurally barred under retained content; needs explicit weight-class selection or extremization principle." |
| V2 | New derivation? | The five-barrier obstruction argument applied to Route D is new structural content. Prior status note enumerated the candidate but did not prove the obstruction. The explicit identification with the (1,1)-vs-(1,2) weight-class residue is new. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) Newton-Girard identity universality, (ii) weight-class polynomial forms, (iii) Brannen-ansatz scope, (iv) polynomial-coefficient circularity, (v) extremization scan, and (vi) the five-barrier conjunction, plus (vii) the trap-profile comparison with Routes E and F. |
| V4 | Marginal content non-trivial? | Yes — the explicit identification of the polynomial coefficient `6` as the Frobenius factor `n(n-1)` and the recognition that polynomial-coefficient routes face the same weight-class trap as the MRU obstruction is non-obvious from prior notes. |
| V5 | One-step variant? | No — the five-barrier argument is structural across multiple polynomial-theoretic angles (NG identity, weight class, Brannen ansatz, polynomial circularity, no extremization), not a relabel of any prior Koide route. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of prior Koide routes. The five-barrier obstruction
  argument applied to Route D is new structural content with explicit
  symbolic identities and numerical extremization scans.
- Identifies a NEW STRUCTURAL CONNECTION (Barrier D2 = the
  polynomial-coefficient form of the (1,1)-vs-(1,2) weight-class
  residue from MRU demotion) not present in the prior
  `KOIDE_A1_DERIVATION_STATUS_NOTE` treatment of Route D.
- Sharpens the "structurally suggestive" claim from open-but-unscoped
  to closed-negatively, with a clear list of what would be required
  to reopen it.
- Provides explicit numerical and symbolic counterexamples that
  demonstrate the freedom of `p_2/e_1²` under R1+R2.
- Establishes the trap-profile contrast with Routes E and F: while
  E/F failed to continuous norm conventions, Route D fails to
  discrete weight-class choice — a *materially different* trap.

## Cross-references

- A1 derivation status (parent): `KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- Sister-route bounded obstructions:
  - Route F (Casimir difference): [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
  - Route E (Kostant Weyl-vector): see commit b38cccbb9 (filename `KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md`)
- Spectrum-operator bridge (retained): [`KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md)
- Block-total Frobenius (retained, weight-class residue): [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- MRU demotion (related residue): [`KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`](KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md)
- Circulant character derivation: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- CL3 SM embedding: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
- One-Higgs gauge selection: [`SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md`](SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md)
- Direct Ward-free Yukawa no-go: [`CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`](CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Physical lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Higher-order structural theorems: [`HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md`](HIGHER_ORDER_STRUCTURAL_THEOREMS_NOTE.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`
- Brocard fingerprint analog (different lane): [`CKM_BROCARD_POLYNOMIAL_VIETA_STRUCTURAL_INTEGERS_THEOREM_NOTE_2026-04-25.md`](CKM_BROCARD_POLYNOMIAL_VIETA_STRUCTURAL_INTEGERS_THEOREM_NOTE_2026-04-25.md) — uses Newton-Girard structural integer fingerprint `p_2 = 2 e_1²` for N_pair = 2 in the CKM lane; analogous machinery, different content; NOT directly transferable to Koide A1.

## Validation

```bash
python3 scripts/cl3_koide_a1_route_d_newton_girard_2026_05_08_routed.py
```

Expected output: structural verification of (i) Newton-Girard identity
universality (any 3-tuple of eigenvalues), (ii) Barrier D1 (NG is
identity, not constraint), (iii) Barrier D2 ((1,1)-vs-(1,2) weight
ambiguity), (iv) Barrier D3 (Brannen ansatz + extra input required),
(v) Barrier D4 (polynomial-coefficient circularity), (vi) Barrier D5
(no symmetric-polynomial-only extremization picks A1), (vii) Routes
E/F trap-profile comparison, (viii) falsifiability anchor
(PDG values, anchor-only), (ix) bounded-obstruction theorem statement.
Total: 33 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_koide_a1_route_d_newton_girard_2026_05_08_routed.txt`](../logs/runner-cache/cl3_koide_a1_route_d_newton_girard_2026_05_08_routed.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  specifically applies the "consistency equality is not derivation"
  rule. The numerical match `2/3 = 2/3` is a consistency equality,
  not a structural Newton-Girard identity, and the proposed
  identification cannot load-bear A1 closure on this basis.
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "the polynomial coefficient `6` is structurally
  forced" by showing that the action-level identification (polynomial
  coefficient = (1,1) multiplicity weight = Frobenius factor) is not
  a derivable identity — it requires either a weight-class selection
  or a convention-invariant reformulation that retained content does
  not supply.
- `feedback_retained_tier_purity_and_package_wiring.md`: no automatic
  cross-tier promotion. This note is a bounded obstruction; the
  parent A1 admission remains at its prior bounded status. No
  retained-tier promotion implied.
- `feedback_physics_loop_corollary_churn.md`: the five-barrier
  argument with explicit symbolic identities, numerical
  counterexamples, and the explicit identification of Barrier D2 as
  the polynomial-coefficient form of the MRU demotion's weight-class
  residue is substantive new structural content, not a relabel of
  prior Koide routes.
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  (A primarily) characterized in terms of WHAT additional content
  would be needed (weight-class selection or extremization principle),
  not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  a multi-angle attack (five independent barriers) on a single
  load-bearing structural lemma, with sharp PASS/FAIL deliverables in
  the runner.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: Route D's failure
  identifies that "polynomial-coefficient" candidates — like the
  Casimir-difference / Weyl-vector candidates — are not free of
  convention-dependence traps; they face their own variant. This
  fragments the bridge gap into more honestly-named pieces.
