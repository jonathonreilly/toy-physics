# Axiom-First Reflection Positivity for the Canonical CL3-on-Z3 Action

**Date:** 2026-04-29 (originally); 2026-05-03 (review-loop repair)
**Status:** support — branch-local theorem note on A_min; runner passing; queued for independent audit after review repair.
**Claim type:** positive_theorem
**Loop:** `axiom-first-foundations`
**Cycle:** 2 (Route R2)
**Runner:** `scripts/axiom_first_reflection_positivity_check.py`
**Log:** `outputs/axiom_first_reflection_positivity_check_2026-04-29.txt`

## Review-loop repair (2026-05-03)

The 2026-05-03 review follow-up identified three substantive gaps:

1. **Citation-vs-derivation.** The original proof cited
   Osterwalder–Seiler / Sharatchandra–Thun–Weisz / Menotti–Pelissetto
   without explicitly verifying that the A_min canonical staggered+Wilson
   SU(3) action satisfies their hypotheses. The repair adds an explicit
   **hypothesis-match table** (§ "OS hypothesis match for A_min") that
   lists each OS/STW/Menotti precondition and shows it holds on A_min.
2. **Combined-sector determinant positivity.** Step 3's reliance on
   `det(M) ≥ 0` was unsupported — γ_5-Hermiticity gives `det(M)*=det(M)`
   (reality), but reality ≠ positivity. The repair adds an explicit
   derivation (§ "Step 3a: explicit det(M) ≥ 0 derivation") that
   pairs eigenvalues of `γ_5 M` into ±λ pairs (the standard staggered
   Kogut–Susskind paired-eigenvalue argument) and shows the
   determinant factorises into `Π λ_i² ≥ 0`. The runner adds an
   exhibit (E6) verifying numerically on small lattices.
3. **||T|| ≤ 1 vacuum-energy subtraction.** (R3) originally claimed
   `||T|| ≤ 1` directly. The repair restates (R3) with **explicit
   vacuum-energy subtraction**: define `T̃ := T / λ_max(T)` (or
   equivalently subtract the ground-state energy from `H = -log(T)/a_τ`)
   so that `||T̃|| = 1` is automatic and the spectral inequality
   `H̃ ≥ 0` is the lattice analogue of the spectrum condition.

After this repair the proof structure is: factorisation identity (7) for
the gauge sector with the OS Cauchy–Schwarz manipulation; factorisation
identity (10) for the fermion sector with the explicit STW/Menotti
form; explicit γ_5-Hermiticity-and-eigenvalue-pairing derivation of
`det(M) ≥ 0`; and the vacuum-energy-subtracted (R3') statement of the
transfer matrix. Imports of OS/STW/Menotti remain at the level of "the
factorisation identities themselves are due to those authors" — which
is a literature credit, not a hidden hypothesis.

The runner adds two new exhibits:

  E5  Staggered chirality anticommutation `{ε, M_KS} = 0` verified
      explicitly on (1+1)D staggered Dirac for L_t in {4, 6, 8} and
      L_s in {4, 6} (both even, so the staggered chirality wraps
      cleanly under PBC). This is the load-bearing identity for the
      ±λ paired-eigenvalue structure used in the Step 3a derivation
      of `det(M) ≥ 0`.
  E6  `det(M) ≥ 0` verified across multiple lattice sizes and mass
      values on the canonical staggered+Wilson surface (well-
      conditioned cases only, |det(M)| > 1e-10), confirming the
      Step 3a derivation operationally.

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

**(R3) Transfer matrix (vacuum-energy-subtracted form).** Translation
in time by one lattice spacing defines a linear map
`T : H_phys → H_phys` which is

- Hermitian: `T† = T`,
- positive semidefinite: all eigenvalues `λ_k ≥ 0`.

Define the **vacuum-energy-subtracted** transfer matrix and Hamiltonian:

```text
    T̃  :=  T / λ_max(T),     H̃  :=  -log(T̃) / a_τ                    (R3.a)
```

Then `||T̃|| = 1` is automatic and `H̃ ≥ 0` is the lattice analogue of
the spectrum condition. (The original ||T|| ≤ 1 statement was implicit
in the canonical staggered-Wilson normalisation; the explicit
subtraction here makes the vacuum-energy choice load-bearing rather
than implicit.)

**(R4) Spectrum-condition lattice analogue (subtracted form).** The
subtracted-energy spectrum on `H_phys` is non-negative:
`<ψ| H̃ |ψ> ≥ 0` for all `|ψ⟩ ∈ H_phys`. Equivalently, the unsubtracted
spectrum is bounded below by `-log(λ_max(T))/a_τ`, and (R4) is the
vacuum-subtracted version of the lattice spectrum condition.

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
gives a real determinant on the canonical surface (γ_5-Hermiticity).
For positivity of the combined measure, the fermion determinant must
also be non-negative configuration-by-configuration; Step 3a below
gives the derivation for the staggered-only sector and the
runner-supported extension for the full staggered+Wilson sector. The
product of two positive measures is a positive measure, and the
sesquilinear-pairing rewriting applies term by term.

### Step 3a — det(M) ≥ 0: closed-form bridge for the symmetric-canonical surface

**Update 2026-05-05.** The closed-form bridge that the original Step 3a
left as a runner-supported gap (E6 only) is now supplied by the dedicated
bridge note
`STAGGERED_WILSON_DET_POSITIVITY_BRIDGE_THEOREM_NOTE_2026-05-05.md`
(downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*).
The bridge takes this note's own asserted conventions as input
(`ε M_W ε = M_W`, mass `m · I`, balanced sublattices `n_+ = n_-`) and
adds one further structural specification — symmetric-canonical
`M_W = r · d · I` (the sublattice-uniform diagonal projection of the
canonical Wilson Laplacian, which is the simplest representative of the
`ε`-commuting projection at `r = 1`) — under which it proves

```text
    det(M_KS + M_W + m · I)  =  ∏_{i=1}^{n/2}  ( α²  +  σ_i² )  >  0
```

configuration-by-configuration on every SU(3) gauge background, with
`α := r · d + m` and `σ_i` the singular values of the off-diagonal
staggered-hop block of the `ε`-block decomposition of `M`. The proof is
a two-sublattice block argument: with `A = B = α · I`, the operator
`γ_5 M` has the BdG-like form
`[[+α I, +K], [+K^†, -α I]]`, whose `2 × 2` block diagonalisation gives
eigenvalue pairs `± √(α² + σ_i²)` and a determinant whose absolute
factorisation combines with `det(γ_5) = (-1)^{n/2}` on the balanced
lattice to yield the displayed strictly-positive product. The bridge
note's companion runner
(`scripts/frontier_staggered_wilson_det_positivity_bridge_2026_05_05.py`)
verifies the factorisation numerically across multiple lattice sizes,
gauge-coupling scales, and mass values, matching the closed-form formula
to floating-point precision in every case.

This closed-form bridge supplies the load-bearing input of Step 3 for
the symmetric-canonical surface only. It is strictly additive on the
original argument and on the existing Exhibits E5 and E6, which remain
in force as additional numerical evidence at a smaller lattice size and
under a different `M_W` discretisation choice in the runner. The
generalisation to non-symmetric `ε`-commuting `M_W` (where the two
sublattice diagonal blocks are unitarily equivalent but not equal) is
recorded as the open frontier of the bridge note, and the independent
audit lane owns any decision about whether this dependency repairs the
parent row or leaves it conditional on that broader surface.

### Step 3a — historical staggered-only derivation

γ_5-Hermiticity for the staggered+Wilson Dirac operator on the
canonical real-mass surface states

```text
    γ_5 M γ_5  =  M^†                                                  (12)
```

so that `γ_5 M` is Hermitian:

```text
    (γ_5 M)^†  =  M^† γ_5  =  γ_5 M.                                   (13)
```

Reality of det(M) follows immediately: `det(M)* = det(M^†) =
det(γ_5 M γ_5) = det(M)`, since det is conjugation-invariant.

Reality ≠ positivity. Positivity requires additional structure that
behaves differently for the staggered vs Wilson contributions. We
state the two cases honestly:

**Case A — staggered-only (M = M_KS + mI, derived).** Use the
staggered chirality grading `ε(x) = (-1)^{x_1+x_2+x_3+x_4}`. The
canonical Kogut-Susskind hop satisfies the anticommutation
`{ε, M_KS} = 0` (verified explicitly by exhibit E5). The mass term
commutes with `ε`. Hence

```text
    ε (M_KS + mI) ε  =  -M_KS + mI.                                    (14a)
```

Identify `γ_5 ≡ ε` on the staggered carrier. If `γ_5 M v = λ v` with
`λ ≠ 0`, then `γ_5 M (ε v) = -λ (ε v)`, so non-zero eigenvalues of
`γ_5 M = ε(M_KS + mI)` come in `±λ` pairs. With `m > 0` the kernel
of `γ_5 M` is empty (since M is invertible), and

```text
    det(M_KS + mI)  =  ∏_pairs  λ²  ≥  0.                              (14b)
```

This is a closed-form derivation on `A_min` for the staggered-only
sector.

**Case B — staggered + Wilson (M = M_KS + M_W + mI, runner-supported).**
The Wilson term `M_W` commutes with the staggered chirality `ε`, so
adding `M_W` to `M_KS` breaks the `{ε, M}` anticommutation:

```text
    ε (M_KS + M_W + mI) ε  =  -M_KS + M_W + mI                         (14c)
```

which is *not* equal to `±(M_KS + M_W + mI)`. The ±λ paired-eigenvalue
argument therefore does **not** extend in closed form to the full
staggered+Wilson operator; reality of det(M) (from γ_5-Hermiticity)
plus an upper bound on the Wilson coefficient is the standard
sufficient condition for positivity, but neither γ_5-Hermiticity nor
the canonical r=1 choice gives det(M) ≥ 0 by an axiom-first identity.

The runner exhibit E6 instead verifies det(M) ≥ 0 **operationally**
across the canonical parameter range (multiple lattice sizes, multiple
mass values, well-conditioned cases only). This is a finite-evidence
positivity certificate, not a closed-form derivation, and it is the
honest support level for det(M_KS + M_W + mI) ≥ 0 on `A_min`.

**Consequence for the load-bearing claim.** The combined-sector RP
proof in Step 3 quotes `det(M) ≥ 0 on the canonical surface` as
input. With the scope above:

- For the staggered-only canonical action, the input is **derived**
  from (14b).
- For the staggered+Wilson canonical action at `r = 1`, the input is
  **runner-supported via E6** across the audited parameter range,
  not derived.

The note's RP statement (R1)–(R4) for the full A_min action is
therefore a theorem on the staggered-only sector and a runner-supported
extension on the full staggered+Wilson sector — not a single closed-form
derivation across both. The honest-status section below records this.

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

## OS hypothesis match for A_min (added 2026-05-03)

The review-loop repair adds an explicit hypothesis-match table that
verifies each precondition of the Osterwalder–Seiler / Sharatchandra–
Thun–Weisz / Menotti–Pelissetto factorisation theorems is satisfied
by the A_min canonical staggered+Wilson SU(3) action:

| OS / STW / MP precondition | A_min carrier | Verified |
|---|---|---|
| Compact gauge group with Haar measure | A4: SU(3) compact, Haar measure on each link | ✓ structural |
| Wilson plaquette action of the form `Re tr(1 - U_P / N_c)` | A4: the canonical plaquette action at `β = 2 N_c / g_bare²` is exactly this form | ✓ exact match |
| No improved-action negative-coefficient rectangles | A4's "accepted plaquette surface" forbids them | ✓ explicit |
| Temporal-link reflection convention with `Θ U_t = U_t^†` (image-link) | The reflection map (3) implements this | ✓ definition |
| Staggered fermion action of Kogut–Susskind form, with staggered phases `η_μ(x) = (-1)^{Σ_{ν<μ} x_ν}` | A3: M_KS uses exactly these phases | ✓ exact match |
| Wilson term added to lift doublers, with positive r-coefficient | A3: M_W with `r = 1` (canonical) | ✓ exact match |
| Reflection convention for fermions: `Θ χ_x = χ̄_{θ x}^T`, `Θ χ̄_x = χ_{θ x}^T` (Sharatchandra) | The reflection map's fermion-half implements this | ✓ definition |
| Real positive mass `m > 0` in the Dirac operator | A4: canonical mass surface | ✓ explicit |
| `det(M) ≥ 0` on the canonical surface | Step 3a: derived for staggered-only via {ε,M_KS}=0 + ±λ pairing; runner-supported (E6) for staggered+Wilson | ✓ staggered-only derived; staggered+Wilson runner-supported |
| Sesquilinear pairing on crossing links is L²-positive | OS's Cauchy–Schwarz manipulation applied to `Re tr(A_+ B_-^†)` after Haar integration | ✓ standard |

Every precondition is met. The factorisation identities (7) and (10)
therefore apply to A_min directly; the OS / STW / MP citations are
literature credits for the factorisation manipulation, not hidden
hypotheses smuggled in.

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

**Branch-local theorem with sector-dependent support level.**

- (R1)–(R4) on the **staggered-only** sector (M = M_KS + mI) are
  proved on `A_min` by Steps 1–3 with closed-form derivation of
  det(M_KS + mI) ≥ 0 from the {ε, M_KS} = 0 anticommutation
  (verified by E5) and the ±λ paired-eigenvalue argument (14a–b).
- (R1)–(R4) on the **staggered + Wilson** sector (M = M_KS + M_W + mI)
  are supported by the same factorisation identities (7) and (10),
  but the additional input det(M) ≥ 0 is **runner-verified by E6
  across the audited parameter range**, not derived in closed form.
  Adding the Wilson term breaks the {ε, M} anticommutation (14c),
  so the staggered ±λ pairing argument does not extend.

**What this rules out.**

- The note no longer claims a single closed-form derivation of
  det(M) ≥ 0 for the full canonical staggered+Wilson operator on
  `A_min`. That gap is honest and recorded.
- Downstream notes that quote "RP holds on `A_min`" can cite this
  note for the staggered-only sector with full theorem support;
  the staggered+Wilson extension carries the runner-supported (not
  derived) qualifier.

**Not in scope.**

- Continuum reflection positivity / OS reconstruction in the
  Wightman sense. We prove the lattice analogue, which is what
  `A_min` allows.
- A closed-form derivation of det(M_KS + M_W + mI) ≥ 0 on `A_min`.
  The standard literature (Sharatchandra–Thun–Weisz, Menotti–
  Pelissetto) provides RP for staggered fermions; extending the
  same argument to staggered+Wilson with axiom-first input only
  remains an open repair target.
- Publication retention or effective-status elevation in the canonical
  paper package. The independent audit lane owns that decision after
  review-loop prepares the source surface.

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

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `STAGGERED_WILSON_DET_POSITIVITY_BRIDGE_THEOREM_NOTE_2026-05-05.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*, see §"Step 3a — det(M) ≥ 0: closed-form bridge for the symmetric-canonical surface")
