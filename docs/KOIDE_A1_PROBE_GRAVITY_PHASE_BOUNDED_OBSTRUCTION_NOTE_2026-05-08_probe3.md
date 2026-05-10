# Koide A1 Probe — Gravity-as-Phase Matter-Sector Inner Product Bounded Obstruction

**Date:** 2026-05-08
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — gravity-as-phase probe
attempt for the A1 √2 equipartition admission on the charged-lepton
Koide lane. Companion to the negative closures Routes A, D, E, F.
**Status:** source-note proposal for a negative gravity-phase route
closure — shows that the retained gravity-as-phase content (lattice
Green function, wavefield propagation, self-gravity loops) cannot
induce a canonical inner product on the matter-sector hw=1 generation
triplet that forces `|b|²/a² = 1/2`. Five independent structural
barriers each block the proposed identification. The A1 admission
count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and
downstream status set only by the independent audit lane.
**Loop:** koide-a1-probe-gravity-phase-20260508
**Primary runner:** [`scripts/cl3_koide_a1_probe_gravity_phase_2026_05_08_probe3.py`](../scripts/cl3_koide_a1_probe_gravity_phase_2026_05_08_probe3.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_gravity_phase_2026_05_08_probe3.txt`](../logs/runner-cache/cl3_koide_a1_probe_gravity_phase_2026_05_08_probe3.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit lane
has full authority to retag, narrow, or reject the proposal.

## Question

`KOIDE_A1_DERIVATION_STATUS_NOTE.md`
plus its companion bounded-obstruction notes
([Route F](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md))
classify all four prior axiom-native A1 closure routes (A, D, E, F)
as structurally barred. The retained framework also contains
gravity-as-phase content (lattice `Z³` Green function, wave-equation
propagation, self-gravity loops). The probe question is whether that
content provides what the prior four routes lacked:

> Does the retained gravity-as-phase content induce a canonical
> inner product / scale on the matter-sector hw=1 generation triplet
> that forces `|b|²/a² = 1/2`?

The probe hypothesis is appealing because Newton's constant `G` (or
its lattice-units analog) is a *natural dimensional scale* and a
canonical inner-product induction would be a 2-for-1 path: it would
also advance the Planck-from-structure derivation (still an open
target with a no-go on the boundary character route per
[`PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md`](PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md)).

**Question:** Can the retained gravity-as-phase content be assembled
into a structural map that forces the matter-sector circulant
amplitude ratio `|b|²/a² = 1/2` — no empirical loading, no new
axioms, and crucially without an analog of the Routes A/D/E/F traps?

## Answer

**No.** The retained gravity-as-phase content cannot close A1 from
retained content alone. Five independent structural barriers each
independently block the proposed identification. The trap profile
shifts from the convention-/weight-class-/symmetry-import traps that
killed Routes A/D/E/F to a more fundamental category obstruction:
gravity content lives on the **spatial Z³ substrate** while the
amplitude ratio `|b|²/a²` lives on the **flavor (hw=1 BZ-corner
generation) sector**, and the audit ledger shows that no retained
gravity content speaks to the flavor sector.

The five barriers (each verified numerically and symbolically in the
paired runner):

1. **Substrate-vs-flavor sector orthogonality (G1).** Every retained
   gravity content row in the audit ledger acts on Z³-substrate
   wavefunctions / lattice Green functions / scalar wavefields.
   The Koide A1 amplitude ratio lives on the 3-dim hw=1 BZ-corner
   triplet `T_1 = span{X_1, X_2, X_3}` per
   [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md).
   These two sectors are tensor-product orthogonal: `H_full ≅ H_Z3 ⊗
   T_1`. No retained theorem maps a Laplacian Green function on `H_Z3`
   to a circulant amplitude ratio on `T_1`.

2. **Retained gravity content is overwhelmingly bounded (G2).** Of
   ~30 retained-grade gravity-related rows in the audit ledger, the
   vast majority are `retained_bounded` (not `retained`), and all of
   the bounded rows have explicit fragility caveats (control-only
   family, weak-effect regimes, sign-only certifications, no clean
   `1/r` radiation tail per
   [`WAVE_EQUATION_GRAVITY_NOTE.md`](WAVE_EQUATION_GRAVITY_NOTE.md)
   2026-05-01 narrowing). The four `retained` (full positive_theorem)
   rows are scalar wavefield static-direct probes
   ([`WAVE_STATIC_*`](WAVE_STATIC_DIRECT_PROBE_FINE_NOTE.md)) and
   the bipartition entropy probe
   ([`SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md`](SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md)) — none
   carries the structural strength to fix a flavor-sector amplitude
   ratio. `GRAVITY_CLEAN_DERIVATION_NOTE.md` itself is `unaudited`
   and explicitly conditional on `L^{-1} = G_0` self-consistency
   plus Born/test-mass mappings.

3. **C_3-equivariance vs Z³ point-group symmetry mismatch (G3).** The
   only retained "gravity-and-phase" content that touches anything
   resembling a discrete character action is
   [`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md):
   a Hadamard / `Z_2^3` character transform on the 8-corner BZ
   subspace `C^8 = (C^2)^{⊗3}`. The flavor-sector circulant amplitude
   `|b|²/a²` lives on hw=1, where the relevant character is `C_3 =
   Z/3Z` (cube-roots-of-unity). The retained intertwiner provides a
   `Z_2^3` character, NOT a `Z_3` character; the two character groups
   are orthogonal at the level of the framework's Plancherel
   decomposition. No retained content bridges them at the gravity-
   phase level.

4. **Mass-density Born map is target-side, not source-side (G4).** All
   retained gravity loops use the Born map `ρ = |ψ|²` (mass density
   sourced by the wavefunction's modulus squared) per
   [`POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md`](POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md).
   This map operates AFTER the wavefunction `ψ` is given. It does not
   constrain how `ψ` decomposes into `(a, b)` flavor amplitudes — it
   reads the integrated probability density on the spatial substrate.
   A "gravity-induced inner product on matter" would have to act
   BEFORE the modulus square (selecting the canonical `(a, b)`
   normalization), which is mathematically incompatible with the
   `ρ = |ψ|²` step.

5. **Newton constant G is dimensional, not amplitude-fixing (G5). The
   target `|b|²/a²` is dimensionless** — it is a ratio of two
   complex amplitudes in the same Hermitian decomposition. Newton's
   constant `G` (or its lattice analog `G_0 = H^{-1}`) carries
   physical dimensions of `(length)^{D-1}/mass` (or, in lattice
   units, encodes the L → ∞ continuum gap per
   [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md)
   Step 3). To fix a dimensionless flavor ratio, one must form a
   dimensionless combination — but the only retained theorems that
   produce dimensionless gravity outputs (the Newton-power exponent
   `α = -1` per Step 6 of the clean-derivation note, the radiation
   tail `γ`, the mass scaling `β`) all live on the **spatial** sector
   and are independently characterized as `retained_bounded` with
   their own fragility caveats. There is no retained dimensionless
   gravity output that lifts to the flavor sector.

The combined picture: **the gravity-phase probe is structurally
barred**. The five barriers are not just analogs of Routes A/D/E/F
trap profiles — they are deeper, because they include a top-level
ledger check (G2) showing that no retained gravity content exists at
the structural strength required to load-bear a flavor-sector closure.
Closing A1 via this route would require either (a) packaging a new
retained primitive that maps the spatial-substrate gravity sector to
the flavor sector (not present in the audit ledger), (b) explicit
user-approved A3-class admission, or (c) an alternative structural
identity not based on gravity-as-phase.

## Setup

### Premises (A_min for gravity-phase probe attempt)

| ID | Statement | Class |
|---|---|---|
| A1 | Cl(3) local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | Z³ spatial substrate | framework axiom; same source |
| Embed | Cl⁺(3) ≅ ℍ → SU(2)_L; ω pseudoscalar → U(1)_Y | retained: [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| Circulant | C_3-equivariant Hermitian on hw=1 is `aI + bU + b̄U^{-1}` | retained: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| KoideAlg | Koide Q = 2/3 ⟺ a₀² = 2|z|² ⟺ \|b\|²/a² = 1/2 (algebraic) | retained: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |
| 3GenObs | hw=1 BZ-corner triplet has M_3(C) algebra; C_3[111] cycles corners | retained-bounded: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Substep4 | AC_φλ remains the explicit identification residual on hw=1 | retained-bounded: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md) |
| GravLawClean | Lattice Z³ Laplacian gives 1/r potential and 1/r² force on the controlled-distance/mass surface | retained-bounded: [`GRAVITY_LAW_CLEANUP_NOTE.md`](GRAVITY_LAW_CLEANUP_NOTE.md) |
| GravPhaseSite | Site-phase / cube-shift intertwiner on `C^8` is Hadamard / `Z_2^3` character transform | retained: [`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md) |
| GravBornMap | Self-gravity loops use `ρ = |ψ|²` Born map on the spatial substrate | retained-bounded: [`POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md`](POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md) |
| GravWaveStatic | Wave equation has Newton-recovery static limit on lattice substrate | retained-bounded: [`WAVE_EQUATION_GRAVITY_NOTE.md`](WAVE_EQUATION_GRAVITY_NOTE.md) |
| GravCleanCond | Conditional 1/r derivation chain (IF L⁻¹ = G_0 + Born + S = L(1−φ)) | unaudited: [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md) — **NOT retained-grade**; named here only for completeness/honest-status |

### Forbidden imports

- NO PDG observed mass values used as derivation input (anchor-only at
  end, clearly marked).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- **NO new axioms** (the gravity-phase probe's promise was axiom-
  native; any A3-class admission requires explicit user approval and
  is not proposed here)
- NO promotion of `unaudited`/`audited_conditional` gravity content
  to retained-grade for the purposes of this probe; the probe must
  honestly use only the retained gravity rows
- NO admitted SM Yukawa-coupling pattern as derivation input

## The structural identification at issue

**Proposed gravity-phase identification:**
```
|b|² / a²  =  ⟨v, v⟩_grav,(C_3 subspace) / ⟨v, v⟩_grav,(trivial subspace)
                                                                = 1/2
```
where the proposal is that gravity-as-phase content induces a canonical
inner product `⟨·,·⟩_grav` on the flavor sector that fixes the
ratio `|b|²/a² = 1/2` (and equivalently, the Brannen `c² = 2`,
Koide `Q = 2/3`).

The runner explicitly tests four classes of induction map:

  (i)   spatial-Laplacian Plancherel induction on hw=1
  (ii)  staggered-cube-shift `Z_2^3` character transform restricted to hw=1
  (iii) Born `ρ = |ψ|²` projection followed by gravity-loop iteration
  (iv)  wave-equation static-limit Newton kernel pulled back to flavor sector

For each, the runner produces explicit counterexamples or shows the
map is undefined / does not fix the target ratio.

## Theorem (gravity-phase probe bounded obstruction)

**Theorem.** On A1+A2 + retained CL3_SM_EMBEDDING + retained
gauge-selection + retained C_3-equivariance + retained KoideCone-
algebraic-equivalence + retained-bounded gravity content rows
(GravLawClean, GravPhaseSite, GravBornMap, GravWaveStatic, plus
self-gravity loop rows) + admissible standard math machinery:

```
The structural identification

  |b|² / a²  =  (gravity-induced canonical ratio)  =  1/2

cannot be derived from retained Cl(3)/Z³ content alone. Five
independent structural barriers each block the lemma:

  (G1) Substrate-vs-flavor sector orthogonality: gravity content
       lives on H_Z3, A1 ratio lives on T_1 (hw=1 BZ-corner triplet).
  (G2) Retained gravity content is overwhelmingly bounded; no
       retained-grade row carries the structural strength to fix a
       flavor amplitude ratio. The clean-derivation chain is
       `unaudited` and conditional.
  (G3) C_3 vs Z_2^3 character mismatch: the only retained gravity-
       phase character content (site-phase intertwiner) is Z_2^3
       (cube-shift), not Z_3 (flavor-sector character).
  (G4) Born map is target-side: ρ = |ψ|² acts AFTER ψ is given;
       cannot constrain (a, b) decomposition.
  (G5) Newton constant G is dimensional; the only dimensionless
       gravity outputs are spatial-sector exponents (α, β, γ),
       not flavor-amplitude ratios.

Therefore the gravity-phase A1 closure attempt is structurally
barred under the stated retained-content surface. The A1 admission
count is unchanged.
```

**Proof.** Each barrier is verified independently in the paired
runner; combining them establishes that no derivation chain from
retained content reaches the identification of `|b|²/a²` with any
gravity-induced canonical ratio.

### Barrier G1: Substrate-vs-flavor sector orthogonality

The retained framework decomposes the full Hilbert space (on the
hw=1 BZ-corner subspace) as a tensor product:

```
H_full  =  H_Z3  ⊗  T_1
```

where:
- `H_Z3` carries spatial-substrate Z³ wavefunctions (acted on by
  the lattice Laplacian `-Δ`, the Green function `G_0 = (-Δ)^{-1}`,
  the wave-equation field `Φ`, the Poisson source `ρ = |ψ|²`).
- `T_1 = span{X_1, X_2, X_3}` is the 3-dim hw=1 BZ-corner triplet
  (acted on by `M_3(C)` and the C_3[111] cycle that cycles corners),
  per [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md).

The C_3-circulant Hermitian operator `H_circ = aI + bU + b̄U^{-1}`
acts entirely on `T_1`. The flavor amplitude ratio `|b|²/a²` is a
ratio of operator coefficients in this `T_1`-only decomposition.

In contrast, every retained gravity content row acts on `H_Z3`. The
Laplacian `-Δ`, the Green function `G_0`, the wave equation operator
`d²/dt² − c²(L + μ²)`, the Born density `ρ = |ψ|²` (where `ψ`
is the spatial wavefunction whose squared modulus integrates to a
density on Z³) — all live on `H_Z3`.

A gravity-phase induction on `T_1` would require either:
- (a) a retained operator `M_grav` mapping `H_Z3 → T_1`, or
- (b) a tensor-factor extraction principle that reads `T_1` content
  from `H_full = H_Z3 ⊗ T_1` via gravity-phase data.

Neither (a) nor (b) appears in any retained ledger row. The runner
verifies (i) the absence of any such map in retained content and (ii)
that the natural candidates (spectral projection on `-Δ` reduced to
hw=1, restriction of wave field to BZ-corner, etc.) all fail to fix
`|b|²/a²` because they leave `(a, b)` free.

### Barrier G2: Retained gravity content is overwhelmingly bounded

Audit-ledger inventory (counted directly from
`docs/audit/data/audit_ledger.json` at the time of writing):

| Bin | Effective status | Count |
|---|---|---|
| Retained positive theorems | `retained` | 4 (scalar wavefield static probes + entropy probe) |
| Retained bounded theorems | `retained_bounded` | ~22 |
| Retained no-go's | `retained_no_go` | ~9 |
| Audited conditional | `audited_conditional` | ~7 |
| Audited renaming (failed) | `audited_renaming` | ~3 |
| Unaudited | `unaudited` | ~12 |

The four `retained` (full positive theorem) gravity-related rows are:
[`SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md`](SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md),
[`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md),
[`WAVE_STATIC_BOUNDARY_SENSITIVITY_NOTE.md`](WAVE_STATIC_BOUNDARY_SENSITIVITY_NOTE.md),
[`WAVE_STATIC_DIRECT_PROBE_FINE_NOTE.md`](WAVE_STATIC_DIRECT_PROBE_FINE_NOTE.md),
[`WAVE_STATIC_FIXED_BEAM_BOUNDARY_SENSITIVITY_NOTE.md`](WAVE_STATIC_FIXED_BEAM_BOUNDARY_SENSITIVITY_NOTE.md),
[`WAVE_STATIC_MATRIXFREE_FIXED_BEAM_BOUNDARY_NOTE.md`](WAVE_STATIC_MATRIXFREE_FIXED_BEAM_BOUNDARY_NOTE.md),
[`WAVE_STATIC_SINGLE_SOURCE_COMPARE_NOTE.md`](WAVE_STATIC_SINGLE_SOURCE_COMPARE_NOTE.md).

None of these states a flavor-sector identity. Each is a probe of
spatial wavefield boundary sensitivity, source comparison, or scalar
bipartition entropy on a single-particle state — all on `H_Z3`-like
Hilbert spaces.

`GRAVITY_CLEAN_DERIVATION_NOTE.md` is `unaudited` per the audit
ledger and is explicitly conditional on three named closures:
`L^{-1} = G_0` (self-consistency), `ρ = |ψ|²` (Born map), `S = L(1−φ)`
(test-mass response). None of these conditional closures has been
audited clean as of 2026-05-08, and the note's status line was
narrowed 2026-04-28 to "bounded conditional weak-field gravity chain"
explicitly because the IF-conditions are not registered as audit-clean.

The Planck-from-structure derivation has its own no-go on the
boundary character route
([`PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md`](PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md))
and the orientation-incidence route
([`PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30.md`](PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30.md)).
The "G-Newton-from-structure" lane is therefore not retained-grade
either; it has its own bounded/conditional/no-go layered status.

The runner enumerates the gravity content surface and verifies that
no `retained` (full) row contains a structural identity of the form
`(flavor amplitude ratio) = (gravity-induced quantity)`.

### Barrier G3: C_3 vs Z_2^3 character mismatch

The only retained gravity-related "phase" content involving a
discrete character action is
[`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md).
That note proves an exact intertwiner

```
Φ^† P_μ Φ  =  S_μ
```

between site-phase operators `P_μ` (multiplication by `(-1)^{x_μ}`)
on the BZ-corner subspace of even-periodic `Z_L^3` and cube-shifts
`S_μ` on the abstract taste cube `C^8 = (C^2)^{⊗3}`. The joint `P_μ`
eigensystem is the Hadamard / `Z_2^3` character transform.

The flavor-sector character `C_3 = Z/3Z` (cube-roots of unity ω, ω²)
is fundamentally different from `Z_2 = Z/2Z` (sign characters ±1):

- `Z_2^3` has `2^3 = 8` characters labeled by α ∈ {0,1}^3.
- `C_3` has `3` characters labeled by trivial / ω / ω̄.

The two character groups are **non-isomorphic**: there is no group
homomorphism `Z_2^3 → C_3` because `gcd(8, 3) = 1` (and conversely
no `C_3 → Z_2^3` injection because 3 ∤ 8). The runner verifies that
restriction of `Z_2^3`-character data to a 3-dim hw=1 subspace
(any of the 8 corners can be selected as one element of the C_3
triplet, but only 3 of 8 corners participate in any given hw=1
configuration) does not preserve the character structure.

Therefore the only retained "gravity-and-phase" character content in
the framework cannot supply a flavor-sector character bridge; the
character mismatch is a hard structural obstruction.

### Barrier G4: Mass-density Born map is target-side

The retained self-gravity loops
([`POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md`](POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md),
[`POISSON_SELF_GRAVITY_LOOP_NOTE.md`](POISSON_SELF_GRAVITY_LOOP_NOTE.md),
[`POISSON_SELF_GRAVITY_LOOP_V3_NOTE.md`](POISSON_SELF_GRAVITY_LOOP_V3_NOTE.md),
[`POISSON_SELF_GRAVITY_MECHANISM_NOTE.md`](POISSON_SELF_GRAVITY_MECHANISM_NOTE.md))
all use the Born map

```
ρ(x)  =  |ψ(x)|²
```

to source the gravitational potential. This map **operates after**
`ψ` is given. The gravity loop reads `|ψ(x)|²` at each spatial site
and produces a potential `φ(x) = G_0 ρ(x)`, then iterates.

Any flavor-sector structure of `ψ` (its decomposition into hw=1
generation amplitudes, or its `(a, b)` circulant content) is COLLAPSED
by the modulus-square. Concretely: if `ψ_full(x, σ) = ψ_spatial(x) ⊗
v(σ)` with `v = a₀ e_+ + z e_ω + z̄ e_{ω²}`, then

```
ρ(x)  =  |ψ_spatial(x)|² · ⟨v, v⟩  =  |ψ_spatial(x)|² (a₀² + 2|z|²)
```

— the Born density depends only on the **norm** of `v`, not on the
ratio `a₀² / |z|²`. The runner verifies this explicitly: two
different flavor-sector vectors with the same norm produce
identical Born densities, so identical gravity loops.

A gravity-induced inner product on matter that fixes `(a, b)` would
have to act BEFORE the Born step, but the only retained map that
takes `ψ` to a scalar gravity source IS the Born step. There is no
retained pre-Born map of the required shape.

### Barrier G5: Newton constant G is dimensional

The Koide A1-condition target `|b|²/a² = 1/2` is dimensionless.
Newton's constant `G` (or the lattice `G_0 = (-Δ)^{-1}` per
[`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md)
Step 2) carries dimensions: in the lattice setting, `G_0` is the
Green function, with `G_0(x, y) ~ 1/|x − y|` for large separation in
3D — units of `(length)^{-1}` in lattice spacing.

To produce a dimensionless target from gravity content, one must
form a ratio. The retained dimensionless gravity outputs from the
audit ledger are:

| Output | Source | Status |
|---|---|---|
| Newton power-law exponent `α ≈ -1` | static-limit Poisson | retained_bounded (control-only family) |
| Wavefield mass exponent `β` | wave equation steady-state | retained_bounded (β ≈ 1.21 ≈ 1.0 ± 21%) |
| Wave radiation tail `γ` | oscillating source | bounded_failed (`γ ≈ -0.58` ≠ -1; runner FAIL on Test 4a) |
| Bipartition entropy `S(A)` | self-gravity entropy | retained (single-particle, bounded by ln 2) |

None of these dimensionless gravity outputs is `1/2`. The closest
numerical match (`α ≈ -1`, `β ≈ 1.21`) are spatial-substrate quantities
on Z³, with their own caveats. The runner verifies that no retained
dimensionless gravity output equals the A1 target `1/2`, and that no
two retained gravity outputs combine into a dimensionless ratio that
equals `1/2` without empirical input.

## Why the gravity-phase probe is even less load-bearing than Routes A/D/E/F

| Route | What was wrong | What was right |
|---|---|---|
| Route A (Koide-Nishiura) | Required U(3) flavor symmetry not in framework | Polynomial form V(Φ) is dimensionally consistent |
| Route D (Newton-Girard) | Newton-Girard is identity, not constraint | Polynomial structure on hw=1 is well-defined |
| Route E (Kostant Weyl) | Cartan-Killing convention dependence | A_1 root system is in retained content (SU(2)_L) |
| Route F (Casimir difference) | Hypercharge convention dependence | Numerical match is striking and unique within SM |
| **Gravity-phase (this note)** | **Five compounding structural barriers G1-G5** | **The retained gravity-as-phase chain DOES exist on Z³** |

Routes A/D/E/F all had at least a structurally well-defined candidate
identity (a polynomial, a Lie-algebra norm, a Casimir scalar) on the
flavor sector with a single trap (convention or weight-class
ambiguity). The gravity-phase probe has a DIFFERENT failure profile:
the candidate identity isn't well-defined in the first place because
gravity content lives on the wrong sector (G1) and is mostly
non-retained (G2). Even if one tried to construct a flavor-sector
gravity-phase ratio, the natural candidates fail by character
mismatch (G3), Born-map ordering (G4), and dimensional analysis (G5).

So the gravity-phase probe is **strictly worse** as a closure path
than Routes A/D/E/F: its failure is multi-mode and structural at the
sector-identification level, not just at the convention-fix level.

## Comparison to prior work

| Prior closure attempt | Status | Comment |
|---|---|---|
| Route A (Koide-Nishiura U(3) quartic) | bounded obstruction, 4 barriers | trace-based 4th-order; needs U(3) import |
| Route D (Newton-Girard) | bounded obstruction, 5 barriers | weight-class choice |
| Route E (A_1 Weyl-vector / Kostant) | bounded obstruction, 5 barriers | normalization convention |
| Route F (Yukawa Casimir-difference) | bounded obstruction, 4 barriers | hypercharge convention |
| **Gravity-phase probe (this note)** | **bounded obstruction, 5 barriers** | **sector orthogonality + retained-grade absence** |

This note **complements** the four prior route notes by removing
gravity-as-phase from the list of "remaining open candidates." The
gravity-phase probe was not in the original status note's enumerated
routes, but the user-prompt question is whether it could be a
2-for-1 bridge to Planck-from-structure as well. The answer is no:
the same retained-grade absence that bars A1 closure also bars the
hoped-for Planck-from-structure 2-for-1.

## What this closes

- **Gravity-phase route negative closure** (bounded obstruction).
  Five independent structural barriers verified.
- **Sharpens the "if gravity were retained" hypothesis**: prior
  user-prompt formulation framed gravity content as potentially
  load-bearing for matter-sector normalization. This note
  demonstrates that even the retained-grade gravity content is
  structurally incompatible with the matter-sector amplitude ratio,
  for reasons orthogonal to the retained-grade limitation. Even if
  `GRAVITY_CLEAN_DERIVATION_NOTE` were to clear its audit and become
  retained, barriers G1, G3, G4, G5 still apply.
- **2-for-1 Planck hypothesis boundary**: the user-prompt
  hypothesized that closing G-Newton self-consistency would
  simultaneously advance Planck-from-structure and A1. This note
  shows that even a fully-retained `GRAVITY_CLEAN_DERIVATION` would
  not by itself close A1 (sector-orthogonality argument is independent of
  retained-grade). So the 2-for-1 path does not exist; A1 closure
  must come from a different mechanism than gravity-phase.
- **Sister-route implications**: confirms Routes A, D, E, F all
  remain individually closed-negatively, with gravity-phase joining
  them as a fifth structurally-barred axiom-native closure attempt.
- **Audit-defensibility**: explicit numerical counterexamples to
  each candidate gravity-phase induction map (Plancherel,
  cube-shift, Born-loop, wave-static).

## What this does NOT close

- A1 admission count is unchanged. A1 remains a load-bearing
  non-axiom step on the Brannen circulant lane.
- The retained gravity content rows themselves remain at their
  current statuses (no retraction implied here).
- Charged-lepton Koide closure remains a bounded observational-pin
  package (status from
  [`CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md`](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
  unchanged).
- Existing gravity runners (Poisson, wave, self-gravity loops)
  retain their PASS/FAIL fingerprints. This note does NOT reanalyze
  any of those — it analyzes the **structural reach** of gravity
  content into the flavor sector.
- AC_φλ residual (substep 4) is unaffected.
- L3a trace-surface bounded obstruction status unchanged.
- The Planck-from-structure derivation lane is unaffected; this note
  only rules out one specific 2-for-1 hypothesis.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Substrate-vs-flavor sector orthogonality (G1) | Demonstrate a retained operator `M_grav: H_Z3 → T_1` mapping a gravity quantity to a flavor amplitude — refutes G1. |
| Retained gravity content is bounded (G2) | If `GRAVITY_CLEAN_DERIVATION_NOTE` clears audit clean and (independently) supplies a flavor-sector identity, refutes G2's structural claim. (Status update alone is insufficient; structural map also required.) |
| Character mismatch (G3) | Demonstrate a retained gravity-phase content with `Z_3` (rather than `Z_2^3`) character action — refutes G3. |
| Born-map ordering (G4) | Demonstrate a retained pre-Born map taking `ψ` to a flavor-sensitive scalar before the modulus square — refutes G4. |
| Newton-G is dimensional (G5) | Demonstrate a retained dimensionless combination of gravity outputs equal to `1/2` without empirical input — refutes G5. |
| Numerical anchor (A1 target) | Falsified if charged-lepton Koide Q deviates significantly from 2/3 in updated PDG; representative anchor values give Q = 0.666661 (sub-0.001%). |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the negative gravity-phase route
boundary: the gravity-as-phase induction of matter-sector normalization
is blocked by sector orthogonality, retained-grade insufficiency,
character mismatch, Born ordering, and dimensional incompatibility,
unless a new gravity-flavor bridge primitive is supplied.

No new admissions are proposed. A1 remains unchanged at its prior
load-bearing non-axiom status on the Brannen circulant lane. The
independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | The "gravity-phase 2-for-1 hypothesis" is sharpened from "open user-prompt question" to "structurally barred under retained content; needs explicit gravity-flavor bridge primitive." |
| V2 | New derivation? | The five-barrier obstruction argument applied to gravity-as-phase is new structural content. The status note enumerated Routes A/D/E/F but did not address gravity content's structural reach into the flavor sector. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) sector orthogonality, (ii) retained-grade ledger inventory, (iii) character mismatch, (iv) Born ordering, (v) dimensional incompatibility, (vi) the five-barrier conjunction. |
| V4 | Marginal content non-trivial? | Yes — the audit-ledger-inventory finding (G2: ~22 retained_bounded vs ~4 retained, with explicit fragility caveats on each) is non-obvious from prior notes and directly challenges the gravity-phase 2-for-1 hypothesis. |
| V5 | One-step variant? | No — the five-barrier argument is structural across multiple sectors (substrate, flavor, character, Born, dimensional), not a relabel of any prior Koide route or any prior gravity note. |

**Source-note V1-V5 screen: pass for bounded-obstruction audit
seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule
is to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of prior Koide routes. The five-barrier
  obstruction argument applied to gravity-as-phase is new structural
  content with explicit ledger inventory and character-group analysis.
- Identifies a NEW STRUCTURAL CLASS OF OBSTRUCTION (Barrier G2 =
  retained-grade absence, Barrier G3 = `Z_2^3` vs `C_3` mismatch,
  Barrier G4 = Born-map ordering) not present in any prior Koide
  route note.
- Sharpens the user-prompt 2-for-1 hypothesis from open to closed-
  negatively, with a clear list of what would be required to reopen.
- Provides explicit ledger-derived counterexamples that demonstrate
  the retained gravity content's structural inability to load-bear
  flavor-sector closure — these were not present in any prior
  obstruction-note treatment.

## Cross-references

- A1 derivation status (parent): `KOIDE_A1_DERIVATION_STATUS_NOTE.md`
- Sister Route F note: [`KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)
- Gravity content key rows (retained_bounded):
  - [`GRAVITY_LAW_CLEANUP_NOTE.md`](GRAVITY_LAW_CLEANUP_NOTE.md)
  - [`POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md`](POISSON_SELF_GRAVITY_BORN_AUDIT_NOTE.md)
  - [`POISSON_SELF_GRAVITY_LOOP_NOTE.md`](POISSON_SELF_GRAVITY_LOOP_NOTE.md)
  - [`POISSON_SELF_GRAVITY_MECHANISM_NOTE.md`](POISSON_SELF_GRAVITY_MECHANISM_NOTE.md)
  - [`WAVE_EQUATION_GRAVITY_NOTE.md`](WAVE_EQUATION_GRAVITY_NOTE.md)
  - [`WAVE_EQUATION_SELF_FIELD_NOTE.md`](WAVE_EQUATION_SELF_FIELD_NOTE.md)
- Gravity content key rows (retained):
  - [`SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md`](SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md)
  - [`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
- Gravity content (unaudited / conditional): [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md)
- Planck-from-structure no-go's:
  - [`PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md`](PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md)
  - [`PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30.md`](PLANCK_BOUNDARY_ORIENTATION_INCIDENCE_NO_GO_NOTE_2026-04-30.md)
- Charged-lepton Koide-cone algebraic equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Substep 4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)
- Physical lattice baseline: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- MINIMAL_AXIOMS: `MINIMAL_AXIOMS_2026-05-03.md`

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_gravity_phase_2026_05_08_probe3.py
```

Expected output: structural verification of (i) sector tensor-product
decomposition + circulant amplitude ratio sits on `T_1` only, (ii)
ledger-derived inventory of retained gravity content, (iii) `Z_2^3`
vs `C_3` character non-isomorphism with explicit homomorphism check,
(iv) Born map collapses flavor amplitude ratios via norm-only
dependence, (v) dimensional analysis of retained gravity outputs and
explicit non-match to `1/2`, (vi) compounding-five-barrier theorem
statement, (vii) falsifiability anchor (PDG values, anchor-only).
Total: 29 PASS / 0 FAIL.

Cached: [`logs/runner-cache/cl3_koide_a1_probe_gravity_phase_2026_05_08_probe3.txt`](../logs/runner-cache/cl3_koide_a1_probe_gravity_phase_2026_05_08_probe3.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note
  applies the "consistency equality is not derivation" rule. Even
  if some retained gravity output equals `1/2` numerically, that
  would be consistency, not derivation. The structural barriers
  G1-G5 establish that no derivation chain reaches the target.
- `feedback_hostile_review_semantics.md`: this note stress-tests
  the semantic claim that "gravity-as-phase induces matter
  normalization" by showing that the action-level sector
  identification (operator coefficient ratio on `T_1` = gravity
  output on `H_Z3`) is not derivable — it requires a bridge
  primitive that retained content does not supply.
- `feedback_retained_tier_purity_and_package_wiring.md`: no
  automatic cross-tier promotion. This note is a bounded
  obstruction; the parent A1 admission remains at its prior
  bounded status. No retained-tier promotion of any gravity
  content is implied or proposed.
- `feedback_physics_loop_corollary_churn.md`: the five-barrier
  argument with explicit ledger inventory and character-group
  analysis is substantive new structural content, not a relabel of
  prior Koide routes or prior gravity notes.
- `feedback_compute_speed_not_human_timelines.md`: alternative
  routes characterized in terms of WHAT additional content would
  be needed (gravity-flavor bridge primitive, pre-Born map,
  dimensionless flavor output), not how-long-they-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note
  packages a multi-angle attack (five independent barriers across
  sector / ledger / character / Born / dimensional levels) on a
  single load-bearing structural identification, with sharp
  PASS/FAIL deliverables in the runner.
- `feedback_review_loop_source_only_policy.md`: source-only — this
  PR ships exactly (a) source theorem note, (b) paired runner,
  (c) cached output. No output-packets, lane promotions, synthesis
  notes, or "Block" notes.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: closing one
  named admission attempt at a time (here: gravity-phase
  hypothesis); the parent A1 admission remains explicitly named
  and unclosed, with the obstruction profile sharpened.
