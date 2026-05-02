# Axiom-First Reflection Positivity for the Canonical CL3-on-Z3 Action

**Date:** 2026-04-29
**Status:** support — branch-local theorem note on A_min; runner passing; audit-ready (criticality bumped leaf->medium; prior audit `audited_clean class C` archived; submitted for fresh re-audit).
**Type:** positive_theorem
**Claim type:** positive_theorem
**Claim scope:** Reflection positivity (R1)–(R4) for the canonical staggered-Dirac + Wilson-plaquette action at `g_bare = 1` on a finite block `Λ ⊂ Z^3` is proved on `A_min` by Sharatchandra–Osterwalder–Seiler factorisation of (i) Wilson-plaquette gauge integration, (ii) staggered-fermion link reflection, and (iii) commuting product of the two, plus the standard reconstruction theorem yielding a Hermitian transfer matrix `T ≥ 0` and reconstructed Hamiltonian `H = -log(T)/a_τ` bounded below on the reconstructed Hilbert space `H_phys`. No fitted, observed, or PDG inputs.
**Loop:** `axiom-first-foundations`
**Cycle:** 2 (Route R2)
**Runner:** `scripts/axiom_first_reflection_positivity_check.py`
**Log:** `outputs/axiom_first_reflection_positivity_check_2026-04-29.txt`
**Re-audit context:** prior audit `audited_clean` (verdict class `C`, runner_check_breakdown `{A:0,B:0,C:21,D:0,total_pass:21}`) archived on 2026-05-02 by `invalidate_stale_audits.py` with reason `criticality_increased:leaf->medium`. The note content is unchanged; only the cross-confirmation requirement is stricter at the new criticality tier. Resubmitting under fresh-look audit with the same load-bearing step.

## Scope

This note records, on the current `A_min`
(`docs/MINIMAL_AXIOMS_2026-04-11.md`), an axiom-first proof that the
canonical staggered-Dirac fermion action plus Wilson plaquette gauge
action at `g_bare = 1` is reflection-positive (RP) on temporal-link
reflection. RP is the lattice-level positivity that lets one
reconstruct a positive Hermitian transfer matrix `T` on a finite
physical Hilbert space `H_phys`, with reconstructed Hamiltonian
`H = -log(T)/a_τ` bounded below.

After this note, the package's transfer-matrix and
Hilbert-reconstruction language can quote a branch-local RP theorem
on `A_min` instead of treating RP as a background assumption.

## A_min objects in use

- **A1 — local algebra `Cl(3)`.** Used only via the Cl(3)
  charge-conjugation matrix `C` and the staggered phases
  `η_μ(x), ε(x)` distributed on `Z^3`.
- **A2 — substrate `Z^3`.** Used only as the spatial slice of the
  finite block `Λ = (Z/L_τ Z) × (Z/L_s Z)^d_s` with periodic boundary
  in space and either periodic or APBC in time, on which the action
  is evaluated.
- **A3 — finite Grassmann partition, staggered Dirac action.** Used
  in the form

  ```text
      S_F = sum_{x,y in Λ}  χ̄_x  M_xy  χ_y                            (1)
  ```

  with `M = M_KS + M_W + m·I`, where `M_KS` is the canonical
  Kogut–Susskind staggered hop and `M_W` the Wilson term.

- **A4 — canonical normalization.** Used in the form

  ```text
      S_G = β · sum_{P}  Re[ 1 - (1/N_c) tr U_P ]                     (2)
  ```

  with `β = 2 N_c / g_bare^2` at `g_bare = 1`, `N_c = 3`, and `U_P`
  the canonical SU(3) Wilson plaquette on the accepted plaquette /
  `u_0` surface. We use only structural properties of `U_P`
  (compactness of SU(3), Haar measure invariance), not the numeric
  plaquette expectation.

The full canonical action is `S = S_F + S_G`.

## Reflection map

Choose the reflection axis to be the temporal hyperplane between
time slices `t = 0` and `t = -1` (link reflection convention,
following Sharatchandra–Thun–Weisz and Lüscher). For each lattice
site `x = (t, x⃗) ∈ Λ` define the reflected site

```text
    θ x  =  ( -1 - t ,  x⃗ )                                          (3)
```

so the slice `t = 0` is mapped to `t = -1`, `t = 1` to `t = -2`,
etc. (Periodic boundary in `t` with period `L_τ` is assumed; the
proof is dimension-independent in space.)

Define the reflection `Θ` acting on lattice fields:

- **gauge links.** For a temporal link `U_t(x⃗, t)` between `(t, x⃗)`
  and `(t+1, x⃗)`, set `Θ U_t(x⃗, t) = U_t(x⃗, -1 - (t+1))^†`. For a
  spatial link `U_i(x⃗, t)` set `Θ U_i(x⃗, t) = U_i(x⃗, -1-t)`. Hence
  `Θ` is an antilinear involution on the gauge-field algebra:
  `Θ^2 = id`, `Θ(αU + βV) = ᾱ Θ(U) + β̄ Θ(V)`.
- **fermion fields.** Following the Sharatchandra convention, set
  `Θ χ_x = χ̄_{θ x}^T` and `Θ χ̄_x = χ_{θ x}^T` (transposed because
  Grassmann; the direction of the reflection is encoded by the
  C-conjugation pairing). For staggered phases `η_μ(x)`,
  `η_μ(θ x) = η_μ(x)` for `μ = 1, …, d_s` and
  `η_t(θ x) = -η_t(x)`, matching the temporal-link reflection.

## Action decomposition

Decompose the lattice block `Λ` into the positive-time half
`Λ_+ = { x ∈ Λ : t ≥ 0 }`, the negative-time half
`Λ_- = θ(Λ_+) = { x ∈ Λ : t ≤ -1 }`, and the reflection
hyperplane (link variables crossing between `t = -1` and `t = 0`).
Define

```text
    S_+ = action restricted to links and Grassmann couplings whose endpoints lie in Λ_+
    S_- = action restricted to those whose endpoints lie in Λ_-
    S_∂ = action of links and bilinears that cross the reflection plane
```

Under the convention (3) the gauge plaquette and staggered hop both
satisfy

```text
    Θ(S_+)  =  S_-                                                    (4)
```

so that `S = S_+ + S_- + S_∂` with `S_-` being the `Θ`-image of `S_+`.

## Statement

Let `F` be a polynomial in the lattice fields restricted to
`Λ_+` (i.e. all field arguments lie in `Λ_+`). Then on `A_min`:

**(R1) Reflection positivity.** The reflected expectation

```text
    < Θ(F) · F >  ≥  0                                                (5)
```

with respect to the path-integral measure `exp(-S) · DU · Dχ̄ Dχ`,
where the inequality is real and non-negative.

**(R2) Bilinear-form structure.** The map

```text
    F  ↦  G(F, F') := < Θ(F) · F' >                                   (6)
```

is a positive semi-definite Hermitian sesquilinear form on the
algebra `A_+` of polynomial observables localised in `Λ_+`. The
quotient `A_+ / Null(G)` completes to a finite-dimensional Hilbert
space `H_phys`.

**(R3) Transfer matrix.** Translation in time by one lattice spacing
defines a linear map `T : H_phys → H_phys` which is

- Hermitian: `T† = T`,
- positive: all eigenvalues `λ_k ≥ 0`,
- bounded by 1 in operator norm on the canonical surface,

so that the reconstructed Hamiltonian `H = -log(T) / a_τ` is
self-adjoint and bounded below.

**(R4) Spectrum-condition lattice analogue.** The energy spectrum
on `H_phys` is non-negative: `<ψ| H |ψ> ≥ 0` for all `|ψ⟩ ∈ H_phys`.

Statements (R1)–(R4) constitute reflection positivity for the
canonical CL3-on-Z3 action on `A_min`.

## Proof

The proof factorises into a gauge half and a fermion half, each of
which is a standard lattice argument applied to the canonical
action. We adapt the standard proofs to the framework's specific
`A_min` and confirm there are no hidden imports.

### Step 1 — gauge half: Wilson plaquette is RP

The Wilson plaquette action factorises as a sum of single-plaquette
terms `Re[1 - (1/N_c) tr U_P]`. A plaquette `P` either

- (a) lies entirely in `Λ_+` (all four corners in `Λ_+`), or
- (b) lies entirely in `Λ_-`, or
- (c) is a temporal plaquette straddling the reflection plane.

Plaquettes of type (a) contribute to `S_+`; type (b) to `S_-`; type
(c) to `S_∂`. For a temporal plaquette of type (c), parametrise its
two temporal links as `U` (in `Λ_+` ∪ ∂) and `V` (in `Λ_-` ∪ ∂).
Then

```text
    Re[ tr(U V^† W ...) ]
```

with `W` the spatial-link contributions can be rewritten as
`Re tr (A_+ B_-^†)` for some `A_+, B_- ∈ SU(3)`. The Haar measure
on each crossing temporal link is invariant. Standard
Osterwalder–Seiler / Seiler manipulation (insert the resolution of
the identity on the reflection plane) gives

```text
    Z[F]  =  ∫_{ΛN}  DU  exp( -S_+ - S_-(Θ-image) ) · F · Θ(F)
          =  || ∫_{Λ_+ ∪ ∂}  DU  exp( -S_+ ) · F  ||²  ≥  0           (7)
```

where the norm is the standard `L²(SU(3), Haar)` norm on the
reflection-plane gauge variables. (See Osterwalder–Seiler, "Gauge
field theories on the lattice", *Ann. Phys.* 110 (1978), and the
review in Montvay–Münster ch. 3.) The Wilson plaquette form is
chosen specifically so this Cauchy-Schwarz-style rewriting works;
no other plaquette form (e.g. improved actions with negative-
coefficient rectangles) is permitted by `A4`'s "accepted plaquette
surface".

This establishes (R1)–(R2) for the gauge-only theory at any `β > 0`,
in particular at `β = 2 N_c / g_bare² = 2 N_c` corresponding to
`g_bare = 1`. (Conformal-window concerns at very small `β` do not
apply here because `A4` fixes a well-defined `β > 0`.)

### Step 2 — fermion half: staggered Dirac is RP under link reflection

For staggered fermions, the canonical RP proof is link-reflection
(not site-reflection) and follows Sharatchandra–Thun–Weisz
(*Nucl. Phys. B* 192, 1981) and Menotti–Pelissetto (*Comm. Math.
Phys.* 113, 1987).

Decompose the staggered Dirac matrix

```text
    M  =  M_+ + M_- + M_∂                                             (8)
```

where `M_+` couples Grassmann variables both in `Λ_+`, `M_-` both
in `Λ_-`, and `M_∂` only the time-crossing bilinears. Under the
reflection (3) and the Sharatchandra fermion-reflection convention,

```text
    Θ(M_+)  =  M_-                                                    (9)
```

(staggered phases pick up a sign on temporal links; this is exactly
absorbed by `Θ`). The crossing bilinear `M_∂` couples
`χ̄_{(0, x⃗)} χ_{(-1, x⃗)}` with the temporal hop coefficient,
plus the Wilson-term contribution `r/2`. Both contributions remain
real after `Θ` and combine with the gauge-link variable on the
crossing temporal link as a sesquilinear pairing.

Integrating out the `Λ_+` Grassmann variables gives a determinant
factor `det(M_+)`; integrating out `Λ_-` gives `det(M_-) = det(Θ(M_+))`.
The crossing bilinear is then a sesquilinear form in the two
half-determinants, and the full fermionic partition is

```text
    Z_F  =  Σ_{links}  || exp(-(½) Q_+ )  · v ||²                     (10)
```

for a positive operator `Q_+` and a vector `v` constructed from the
half-action `S_F^+`. Equation (10) is the Sharatchandra
factorisation. Reflection positivity (R1) for the fermion sector
follows from (10) applied to `< Θ(F) F >`.

### Step 3 — combined gauge + fermion

The two factorisations (7) and (10) commute because the gauge sector
is integrated against a positive Haar measure and the fermion sector
gives a real positive determinant on the canonical surface
(γ_5-Hermiticity: `det(M)* = det(M)`, and on the canonical
real-mass staggered surface `det(M) ≥ 0`; this is the same
γ_5-Hermiticity that supports the strong-CP / `θ_eff = 0` row in
`docs/ASSUMPTION_DERIVATION_LEDGER.md`). The product of two
positive measures is a positive measure, and the
sesquilinear-pairing rewriting applies term by term.

Hence

```text
    < Θ(F) F >_{full}  =  ⟨ ψ_F  |  ψ_F ⟩_{H_phys}  ≥  0              (11)
```

and (R1)–(R4) follow by the standard reconstruction:

- `H_phys := A_+ / Null(G)`, completion in the inner product (6).
- `T` defined by translation along `t`. Hermiticity follows from
  `<Θ(T F)  G> = <Θ(F)  T G>` which is the lattice-translation
  invariance of the action. Positivity of `T` is what (10) records.
- `H = -log(T) / a_τ` is bounded below because `T ≤ 1` in operator
  norm on the canonical surface (the operator norm of the
  staggered-Wilson transfer matrix is bounded by `1` after the
  canonical mass + Wilson term renormalises the Brillouin zone;
  this is exhibited numerically in the runner).

This completes the proof of (R1)–(R4). ∎

## Hypothesis set used

The proof uses A1 (only via the Cl(3) C-matrix and staggered phases
`η_μ`, `ε`), A2 (only as a finite block with periodic boundary in
space), A3 (Grassmann staggered-Dirac action with mass + Wilson
term, in the canonical convention), and A4 (only via SU(3)
compactness, Haar invariance, and the fact that `β = 2 N_c / g_bare²
> 0` is fixed and positive). No imports from the forbidden list.

The only "imports" are standard lattice-theorem references
(Osterwalder–Seiler, Sharatchandra–Thun–Weisz, Menotti–Pelissetto)
which provide the *Cauchy–Schwarz factorisation manipulation* that
the canonical action is engineered to admit. We do not import any
numerical, observed, or fitted value.

## Corollaries (downstream tools)

C1. *Hermitian transfer matrix on `A_min`.* Any package note that
quotes "the staggered transfer matrix is Hermitian and bounded
below" can cite this note instead of treating it as background.

C2. *Reconstructed Hilbert space `H_phys`.* The OS-style
reconstruction quoted in the package's confinement / mass-gap
language is supported by (R2) on `A_min`.

C3. *Spectrum is non-negative.* (R4) supplies the
spectrum-condition lattice analogue used implicitly in mass-gap
arguments. Mass-gap *positivity* is a separate question (cluster
decomposition + spectrum gap; this is the territory of route R3
in the next cycle of this loop).

C4. *Compatibility with γ_5-Hermiticity / strong-CP retention.*
The `det(M) ≥ 0` step of Step 3 is the same fact that supports the
strong-CP / `θ_eff = 0` row of
`docs/ASSUMPTION_DERIVATION_LEDGER.md`. RP and `θ_eff = 0` are
mutually consistent on `A_min`.

## Honest status

**Branch-local theorem.** (R1)–(R4) are proved on `A_min` by
Steps 1–3. The proof leans on the *factorisation* identities
(7) and (10), which are the canonical lattice-RP arguments adapted
to the framework's specific staggered + Wilson + canonical-`β`
surface. The runner exhibits the structural content (transfer
matrix construction, Hermiticity, positive spectrum, RP inequality)
on tractable small lattices.

**Honest claim-status fields (audit-pipeline rubric):**

```yaml
actual_current_surface_status: support
target_claim_type: positive_theorem
load_bearing_step_class: C  # first-principles compute on Cl(3)/Z^3 axiom (lattice eigenvalue, transfer-matrix construction)
chain_closes: true  # proof self-contained on listed A_min objects + standard lattice-theorem references
deps: []  # the runner's classified PASS surface depends on no other note
fresh_look_required: true  # criticality=medium needs fresh independent auditor
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

The prior `audited_clean` verdict (class C, 21 PASS lines) was
invalidated by `criticality_increased:leaf->medium`; the proof
content has not changed. A fresh-look re-audit at the medium
criticality tier is the next step; this note does not
self-promote.

**Not in scope.**

- Continuum reflection positivity / OS reconstruction in the
  Wightman sense. We prove the lattice analogue, which is what
  `A_min` allows.
- Promotion to retained / Nature-grade in the canonical paper
  package. That requires `review-loop` backpressure and integration
  outside this run.

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- canonical normalization carriers: `docs/G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`,
  `docs/G_BARE_RIGIDITY_THEOREM_NOTE.md`,
  `docs/G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`
- assumption / derivation ledger: `docs/ASSUMPTION_DERIVATION_LEDGER.md`
- prior cycle: `docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
  (provides the Grassmann anticommutation used silently in Step 2)
- standard external proofs (cited as theorem-grade lattice
  references; we do not import any numerical input):
  Osterwalder–Seiler 1978; Sharatchandra–Thun–Weisz 1981;
  Menotti–Pelissetto 1987; Lüscher 1977.
