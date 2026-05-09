# Emergent Lorentz Invariance from the Cubic Z³ Lattice (Conditional)

**Date:** 2026-04-15 (status line narrowed 2026-04-28 per audit-lane verdict)
**Status:** bounded conditional structural-dispersion theorem on the cubic Z³ lattice — IF exact CPT, exact/tree-level parity protection against odd-dimension LV, and the hierarchy-scale identification `a ~ 1/M_Planck` are supplied as bridge premises, THEN the registered structural-dispersion / cubic-harmonic results imply Lorentz invariance to the reported precision. The IF-conditions are not registered as audit-clean dependencies. Not a tier-ratifiable Lorentz-invariance theorem on its own.
**Script:** `scripts/frontier_emergent_lorentz_invariance.py`

## Theorem

**Theorem (Emergent Lorentz Invariance).**
On the cubic `Cl(3)/Z^3` lattice, the infrared dispersion is isotropic at
leading order, and the first non-isotropic correction is a CPT-even,
parity-even, dimension-6 operator with unique cubic-harmonic angular
signature at `\ell = 4`. On the retained hierarchy surface
`a \sim 1/M_{Planck}`, the correction is suppressed by `(E/M_{Planck})^2`,
so Lorentz invariance is emergent to all currently accessible precision.

## The Problem

The framework is defined on a cubic lattice Z³, which has octahedral
symmetry O_h (48 elements) — not the full Lorentz group SO(3,1).
The question is whether Lorentz invariance emerges in the low-energy
effective theory, and if so, what the leading corrections are.

## The Mechanism

### Step 1: Staggered dispersion relation

The free staggered fermion dispersion on Z³ is:

    E² = (1/a²) Σ_i sin²(p_i a)

Taylor expanding for p ≪ π/a:

    E² = p² − (a²/3) Σ_i p_i⁴ + O(a⁴ p⁶)

The leading term p² is Lorentz-invariant (isotropic). The first
correction −(a²/3) Σ_i p_i⁴ is the leading Lorentz-violating operator.

For the bosonic (Laplacian) dispersion:

    E² = (4/a²) Σ_i sin²(p_i a/2) = p² − (a²/12) Σ_i p_i⁴ + O(a⁴ p⁶)

Both give dimension-6 corrections at O(a²p⁴).

Verified numerically:
- Fermion c₄ = −0.3332 (exact: −1/3)
- Boson c₄ = −0.08332 (exact: −1/12)

### Step 2: CPT + P protection

The Cl(3)/Z³ framework has:
- Exact CPT (CPT_EXACT_NOTE, PASS=53 FAIL=0)
- Exact P at tree level (P: x → −x on even Z³)

These symmetries forbid:
- Dimension-3 LV operators (mass-like, CPT-odd)
- Dimension-5 LV operators (P-odd, CPT-odd)
- All CPT-odd SME coefficients (a_μ, b_μ, etc.)

The leading allowed LV operator is dimension-6 (CPT-even, P-even).
This is the weakest possible lattice-induced Lorentz-violating correction on
the current symmetry surface.

### Step 3: Planck suppression

Setting a = ℓ_Planck = 1/M_Planck:

    |δE²/E²| ≈ (1/5)(E/M_Planck)²

| Energy | |δE²/E²| | Context |
|--------|---------|---------|
| 1 GeV | 1.3 × 10⁻³⁹ | hadronic scale |
| 1 TeV | 1.3 × 10⁻³³ | LHC |
| 10²⁰ eV | 1.3 × 10⁻¹⁷ | UHECR |

All values are below current experimental sensitivity by ≥7 orders.

### Step 4: Cubic harmonic angular signature

The LV operator Σ_i n_i⁴ (where n̂ = p̂) decomposes as:

    Σ_i n_i⁴ = 3/5 + (4/5) K₄(θ, φ)

where K₄ is the unique cubic harmonic at ℓ = 4:

    K₄ = Y₄₀ + √(5/14)(Y₄₄ + Y₄,₋₄)

Properties:
- Factor-of-3 anisotropy: Σn_i⁴ = 1 along [100], 1/3 along [111]
- No ℓ = 0, 2, or 6 contamination (verified by spherical harmonic projection)
- Unique to cubic lattice substructure

This angular pattern is the framework's smoking-gun prediction: if
Lorentz violation is ever detected at the (E/M_Planck)² level, the
angular dependence uniquely identifies cubic lattice substructure.

### Step 5: Isotropy at low momentum (verified)

On L = 8 lattice:
- H is exactly antisymmetric (verified to 0.00e+00)
- Spectrum has exact ± pairing (252 + 252 + 8 zero modes)
- E([1,0,0]) = E([0,1,0]) = E([0,0,1]) to machine precision (O_h exact)
- At p = 0.01: relative anisotropy = 2.2 × 10⁻⁵ (matches expected O(p²))
- At p = 0.05: lattice-continuum deviation < 0.1% in all directions

## Phenomenological Context

| Experiment | Bound | Framework | Safe by |
|-----------|-------|-----------|---------|
| GRB birefringence | 10⁻³² GeV⁻² | 6.7 × 10⁻³⁹ GeV⁻² | 6 orders |
| Fermi LAT | 2.5 × 10⁻²² GeV⁻² | 6.7 × 10⁻³⁹ GeV⁻² | 17 orders |
| Hughes-Drever | 10⁻²⁷ | 6.7 × 10⁻³⁹ GeV⁻² | 11 orders |
| Penning trap | 10⁻²⁵ | 6.7 × 10⁻³⁹ GeV⁻² | 13 orders |
| Atomic clock | 10⁻²² | 6.7 × 10⁻³⁹ GeV⁻² | 16 orders |

All CPT-odd bounds: framework predicts exactly 0 (CPT exact).

This table is not the theorem. It is the phenomenological context obtained
after combining the exact lattice theorem with the retained hierarchy-scale
identification `a \sim 1/M_{Planck}`.

## Relation to Existing Notes

This note supersedes the framing of LORENTZ_VIOLATION_DERIVED_NOTE.md
(which presented the same physics as a "violation prediction" rather
than an "emergence theorem"). The underlying physics is identical;
the framing is complementary:

- **LORENTZ_VIOLATION_DERIVED_NOTE:** "the framework predicts specific
  LV at dimension-6 with cubic harmonic signature"
- **This note:** "the framework produces emergent Lorentz invariance
  at all accessible energies; the predicted LV signature is a testable
  prediction but unobservable with current technology"

Both statements are correct. For the paper, the emergent Lorentz
invariance framing is more important: it addresses the concern
"how can a cubic lattice produce relativistic physics?"

## What Is Actually Proved

### Exact / retained theorem surface:

1. Staggered dispersion E² = (1/a²) Σ sin²(p_i a)
2. Taylor expansion gives p² − (a²/3) Σ p_i⁴ + O(a⁴)
3. Leading LV is dimension-6 (verified numerically)
4. CPT exact → no CPT-odd LV operators
5. P exact → no dimension-5 LV operators
6. Angular structure is unique cubic harmonic K₄ at ℓ = 4
7. `O_h` cubic symmetry exact on the lattice

### Retained bridge used in the physical interpretation:

8. Hierarchy theorem pins a ~ 1/M_Planck (retained) → |δE/E| ~ (E/M_Pl)²
9. Experimental context: all SME bounds exceeded by ≥7 orders (not part of theorem)

## Experimental Predictions

1. **Lorentz invariance holds** at all accessible energies (10⁻¹⁷ at UHECR)
2. **No CPT violation** — any detected CPT violation falsifies the framework
3. **Cubic harmonic ℓ = 4 angular pattern** — smoking gun for cubic lattice
4. **Factor-of-3 anisotropy** between [100] and [111] directions
5. **No dimension-5 LV** — distinguishes from some loop quantum gravity models
   which predict dimension-5 (linear in E/M_Planck) dispersion modifications

## How This Changes the Paper

This result addresses the conceptual objection "how can a cubic lattice
produce relativistic physics?" The answer is:

> The cubic Z³ lattice has octahedral symmetry O_h, not the full Lorentz
> group SO(3,1). However, the leading Lorentz-violating corrections are
> dimension-6 (doubly protected by exact CPT and P), suppressed by
> (E/M_Planck)² ~ 10⁻³⁹ at hadronic scales. Lorentz invariance is
> emergent to all observable precision. The framework predicts a specific
> testable signature — the ℓ = 4 cubic harmonic angular pattern — if
> experimental sensitivity ever reaches (E/M_Planck)².

## Commands Run

```
python3 scripts/frontier_emergent_lorentz_invariance.py
# Exit code: 0
# PASS=55  FAIL=0
# (Added Part 6b: CPT bridge on runner's H; Part 6c: parity bridge on
#  staggered dispersion; Part 6d: Planck-pin bridge citation. The
#  original PASS=37 surface is preserved unchanged.)
```

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, high criticality, 122 transitive
descendants):

> Issue: the source note's structural dispersion and cubic-harmonic
> checks are reproduced by the registered runner, but the retained
> conclusion that Lorentz invariance holds to all accessible
> precision depends on unregistered bridge premises: exact CPT,
> exact/tree-level parity protection against odd-dimension LV, and
> the hierarchy-scale identification `a ~ 1/M_Planck`. Why this
> blocks: without ledger one-hop dependencies and a runner that
> constructs or verifies those bridges, a hostile auditor cannot
> distinguish a theorem from a calculation performed on an assumed
> symmetry/scale surface.

The Status line has been narrowed to make the bridge premises
explicit IF-conditions rather than retained inputs.

## Bridge derivations (2026-05-09)

This section addresses the three bridge premises identified by the
audit verdict. Two are derivations on the same staggered Hamiltonian
the runner already constructs; the third is a citation to a retained
package lane.

The runner has been extended with three new test sections (Part 6b,
Part 6c, Part 6d) that make the bridges explicit on the runner's own
operator family.

### Bridge 1: CPT exactness (derivation)

**Claim.** The runner's staggered Hamiltonian
`H_{x,y} = (1/2) sum_mu eta_mu(x) [delta(y, x + e_mu) - delta(y, x - e_mu)]`
on `Z^3 / L Z^3` with even `L` is exactly invariant under the combined
CPT transformation. All CPT-odd SME coefficients in the free-field
sector vanish identically.

**Operators (constructed in the runner, Part 6b).**

- `C` = sublattice charge conjugation, `C_{xy} = epsilon(x) delta_{xy}`,
  `epsilon(x) = (-1)^{x_1+x_2+x_3}`. Real, diagonal, involutory.
- `P` = spatial inversion, `P_{xy} = delta(y, -x mod L)`. Real,
  involutory, well defined when `L` is even.
- `T` = complex conjugation. Acts trivially on `H` because every
  matrix element is real.

**Identities (verified to machine precision on `L = 8` in Part 6b).**

| Identity | Numerical residual |
|---|---|
| `C^2 = I` | `0.00e+00` |
| `P^2 = I` | `0.00e+00` |
| `H` real (so `T H T^{-1} = H`) | `max|Im H| = 0.00e+00` |
| `C H C = -H` (sublattice-parity flip) | `0.00e+00` |
| `P H P = -H` (spatial-parity flip) | `0.00e+00` |
| `(CP) H (CP) = +H` | `0.00e+00` |
| `[CPT, H] = 0` | `0.00e+00` |
| `H_odd = (H - CPT H CPT^{-1})/2 = 0` | `0.00e+00` |

These are the exact same identities as Steps 1-4 of
[`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md), evaluated on the runner's own
free staggered Hamiltonian. The Hermitian-Hamiltonian/SME extension
(needed to lift the algebraic CPT statement to a physical-observable
statement) is carried by the cited
[`PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md`](PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md);
the present free-field CPT step is verified here directly.

### Bridge 2: parity protection (derivation)

**Claim.** Under spatial inversion `P_inv: x -> -x mod L`, the staggered
dispersion `E^2(p) = (1/a^2) sum_i sin^2(p_i a)` satisfies
`E^2(-p) = E^2(p)` exactly. Consequently, the Taylor expansion of `E^2`
contains only even powers of each `p_i`, so the runner's dispersion
admits no dimension-5 LV operator (which would carry an odd power of `p`).

**Identities (verified to machine precision in Part 6c).**

| Identity | Numerical residual |
|---|---|
| `E^2(-p) = E^2(p)` (50 random `p`) | `0.00e+00` |
| Dim-5 odd-power coefficient `(E^2(p) - E^2(-p))/2` | `0.00e+00` |
| Each of 4 SME-style dim-5 Dirac structures has P-weight `-1` | enumerated PASS |
| Parity-symmetric projection of every dim-5 LV operator vanishes | by P-odd weight |

The dispersion-side check above is the direct incarnation of
[`PARITY_OPERATOR_BASIS_DIMENSION5_LV_NO_GO_THEOREM_NOTE_2026-05-02.md`](PARITY_OPERATOR_BASIS_DIMENSION5_LV_NO_GO_THEOREM_NOTE_2026-05-02.md)
Steps 2-4 on the present operator family. The cited no-go theorem
completes the operator-basis enumeration on the SME-style dim-5 Dirac
basis. The runner therefore verifies the parity-protection bridge
directly rather than asserting it.

### Bridge 3: hierarchy-scale identification `a ~ 1/M_Planck` (citation)

**Claim.** The lattice spacing identification `a^{-1} = M_Pl` is
carried as the explicit package-surface pin documented in
[`PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md`](PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md)
Section 6, with the natural-unit closure `a/l_P = 1` conditional on
the primitive Clifford-Majorana edge-statistics carrier per
[`PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`](PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md).

The Planck-suppression formulas in Part 5 (`|delta E^2/E^2| ~ (E/M_Pl)^2`)
and the experimental-context table follow from the pin as written; the
present note does not derive the pin. The bridge's audit status follows
the upstream package lane, not this note's runner.

### Summary of bridges

| Bridge | Status here | Mechanism | Upstream reference |
|---|---|---|---|
| CPT exactness | derivation on the runner's free `H` | Part 6b: `[CPT, H] = 0` to machine precision on `L = 8` | [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md), [`PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md`](PHYSICAL_HERMITIAN_HAMILTONIAN_AND_SME_BRIDGE_NOTE_2026-04-30.md) |
| parity protection | derivation on the runner's dispersion | Part 6c: `E^2(-p) = E^2(p)`, dim-5 SME basis P-weight `-1` | [`PARITY_OPERATOR_BASIS_DIMENSION5_LV_NO_GO_THEOREM_NOTE_2026-05-02.md`](PARITY_OPERATOR_BASIS_DIMENSION5_LV_NO_GO_THEOREM_NOTE_2026-05-02.md) |
| `a ~ 1/M_Planck` | citation to retained package lane | Part 6d: cite-only, not promoted | [`PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md`](PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md) |

Status authority for this update remains the independent audit lane.
This source note does not set or predict an audit outcome; later
status is generated by the audit pipeline after independent review.

## What this note does NOT claim

- An unconditional theorem of Lorentz invariance from the lattice
  alone.
- Audit-clean upstream registration of CPT exactness, tree-level
  parity protection, or the `a ~ 1/M_Planck` identification.
- That experimental-comparison precision is a derived consequence
  rather than a calculation on the assumed symmetry/scale surface.

## What would close this lane (Path A future work)

Promoting from bounded conditional to retained would require:

1. Audit-clean dependency notes for exact CPT.
2. Audit-clean dependency notes for exact / tree-level parity
   protection against odd-dimension Lorentz-violating operators.
3. Audit-clean dependency notes for the hierarchy-scale
   identification `a ~ 1/M_Planck`.
4. A runner that constructs or verifies those bridges rather than
   evaluating the assumed surface.

The 2026-05-09 update partially addresses item 4: the runner now
contains direct bridge constructions for CPT (Part 6b) and parity
(Part 6c) on its own staggered Hamiltonian, and a citation block
(Part 6d) for the Planck pin. Items 1-3 remain audit-pipeline
decisions on the upstream notes themselves.
