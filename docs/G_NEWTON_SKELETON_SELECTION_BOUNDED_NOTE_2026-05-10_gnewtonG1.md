# Skeleton-Selection Bounded Theorem: `L = H` from Retained Hamiltonian Uniqueness

**Date:** 2026-05-10
**Type:** bounded_theorem
**Claim scope:** From A_min plus the retained reflection-positivity, retained
spectrum-condition, retained microcausality / Lieb-Robinson, and retained
single-clock codimension-1 unitary-evolution support theorems, plus the
retained physical-`Cl(3)`-on-`Z^3` baseline interpretation, the framework's
**primary spatial kinematic operator on the equal-time Cauchy slice is
unique and equals `H = -Δ_lat`**. Any candidate linear field operator `L`
in the static, zero-energy sector that is sourced by the framework's
retained dynamical content must reduce to `H` in that sector. Hence
`L = H`, and by the propagator's definition `G_0 := H^{-1}` the closure
identity `L^{-1} = G_0` follows definitionally. This narrows the
gravity-clean lane's previously-stipulated closure identity into a derived
consequence of retained dynamics, conditional on the physical-lattice
baseline.
**Status:** awaiting independent audit. Source-note status is not an audit
verdict. The bound is the physical-lattice baseline meta plus the upstream
audit status of the cited support theorems.
**Loop:** `g-newton-sharpened-admissions-2026-05-10`
**Cycle:** 1 (Probe P4 admission (a) of 3)
**Branch:** `claude/skeleton-selection-bounded-2026-05-10-gnewtonG1`
**Runner:** `scripts/cl3_g_newton_skeleton_selection_2026_05_10_gnewtonG1.py`
**Cache:** `logs/runner-cache/cl3_g_newton_skeleton_selection_2026_05_10_gnewtonG1.txt`

## Scope

`GRAVITY_CLEAN_DERIVATION_NOTE.md` (Step 3) and
`GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md` (hypothesis A2) currently treat the
**closure identity** `L^{-1} = G_0` as a stipulated physical closure
condition rather than a derived consequence of A_min. The gravity-clean
auditor verdict (`audited_conditional`, 2026-04-28) explicitly flagged
this as one of three named admissions blocking retained-positive closure
on the `G_Newton` lane. Probe P4 (PR #875) sharpened the admission list to
three:

- **(a) skeleton-selection** `L^{-1} = G_0` — operator-class selection;
- **(b) Born-as-source** `ρ = |ψ|²` — source-density identification;
- **(c) test-mass response** `S = L(1 - φ)` — valley-linear coupling.

This note targets **(a)** only. It does not address (b) or (c).

The new angle: under the framework's already-retained single-clock
codimension-1 unitary-evolution theorem, there is **exactly one**
primary time generator `H`, and the equal-time local algebra on each
codimension-1 slice `Σ_t` is the mutually-commuting tensor product
`⊗_x Cl(3)_x`. The static, zero-energy sector of the dynamics is then
spanned by a single primary spatial kinematic operator. That operator,
on the canonical surface, is `H = -Δ_lat`.

Any candidate field operator `L` for the static linear field equation
`Lφ = -κρ` must arise from the framework's retained dynamical content
(physical-lattice baseline). The candidate skeletons historically
considered in the repo — Hamiltonian, lattice d'Alembertian, complex-
action / Euclidean — all collapse to the same primary spatial operator
`H = -Δ_lat` in the static sector. Hence the skeleton selection
`L = H` is **forced** under retained Hamiltonian uniqueness plus the
physical-lattice baseline; by `G_0 := H^{-1}` the closure identity
`L^{-1} = G_0` follows definitionally.

## A_min objects in use

- **A1 — local algebra `Cl(3)`.** Used only via the retained Cl(3)
  per-site algebra structure: each lattice site `x ∈ Z^3` carries an
  independent copy of the 8-dim Cl(3) algebra.
- **A2 — substrate `Z^3`.** Used as the spatial slice
  `Σ_t = {t} × (Z/L_s Z)^3` of the canonical block
  `Λ = (Z/L_τ Z) × (Z/L_s Z)^3`, and as the lattice graph metric.

No fitted parameters. No observed values used as proof inputs.

## Retained inputs

- **(R-RP) Reflection positivity.** From the
  `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`:
  the canonical staggered + Wilson action on `Λ` is RP under temporal
  link reflection, and the reconstructed transfer matrix
  `T : H_phys → H_phys` is positive Hermitian with `||T||_op ≤ 1`.

- **(R-SC) Spectrum condition.** From the
  `AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`:
  `H := -(1/a_τ) log(T)` is self-adjoint and bounded below on
  `H_phys`.

- **(R-LR) Microcausality / Lieb-Robinson.** From the
  `AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`:
  (M1) `[O_x, O_y] = 0` strictly for `x ≠ y` at equal time, and
  (M2) Heisenberg-evolved commutators are exponentially bounded outside
  the lattice lightcone with `v_LR = 2 e r J`.

- **(R-SCC) Single-clock codimension-1 unitary evolution.** From the
  `AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`:
  (S1) `H` is the **unique** generator of a strongly-continuous
  one-parameter unitary group `U(t) = exp(-itH)` on `H_phys`,
  (S2) each `Σ_t` is a codimension-1 Cauchy hypersurface with
  mutually-commuting equal-time local algebra
  `A(Σ_t) = ⊗_{x ∈ Σ_t} Cl(3)_x`, (S3) the temporal direction is the
  **unique** RP-admissible reflection axis (no "second clock").

- **(R-PL) Physical-lattice baseline.** From the
  `PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`
  (retained meta clarification): `Cl(3)` on `Z^3` is the framework's
  **physical** local algebra and spatial substrate, not a regulator or
  formal bookkeeping device. Therefore the framework's retained
  dynamical content (in particular the reconstructed Hamiltonian `H`)
  is the **physical** kinematic content, not auxiliary.

These five inputs together fix the framework's primary kinematic
content on the canonical surface.

## Statement

**(K1) Single primary spatial kinematic operator.** Let `Λ`, `H_phys`,
`T`, and `H = -(1/a_τ) log(T)` be as in (R-RP)+(R-SC)+(R-SCC). On the
equal-time slice `Σ_t` and on the static, zero-energy sector
(`E = 0` eigenspace of `H`, equivalently the kernel of `H` after
vacuum subtraction or the resolvent at zero energy on the orthogonal
complement), the framework's only primary linear spatial operator on
`Σ_t` consistent with retained dynamics is

```text
    H_spatial  :=  H |_{static sector}  =  -Δ_lat                    (1)
```

where `Δ_lat` is the `Z^3` graph Laplacian
`(Δ_lat ψ)(x) = sum_{|y - x| = 1} (ψ(y) - ψ(x))`.

Equivalently: the Kawamoto-Smit staggered construction at
`A1+A2+A3+A4` realises the single-time Hamiltonian on `Σ_t` as
`H = -Δ_lat` in the scalar (squared-Dirac) sector
(`GRAVITY_CLEAN_DERIVATION_NOTE.md` Step 1).

**(K2) Reduction of all retained skeletons to `H_spatial`.** Any
candidate field operator `L` for the static linear field equation
`Lφ = -κρ` that is sourced by retained dynamical content of the
framework reduces to `H_spatial` in the static, zero-energy sector.
Three retained skeleton families are exhaustive on the canonical
surface:

  (i) **Hamiltonian skeleton.** `L_H := H`. Static restriction
  `L_H |_{Σ_t} = H = -Δ_lat = H_spatial`.

  (ii) **Lattice-d'Alembertian skeleton.** `L_□ := ∂_t² - Δ_lat`
  (lattice second-order temporal + spatial Laplacian, the canonical
  Lorentzian wave operator on `Λ`). On the static, zero-energy
  sector, `∂_t² → 0` (no temporal variation), so
  `L_□ |_{static} = -Δ_lat = H_spatial`.

  (iii) **Euclidean / complex-action skeleton.** From (R-RP), the
  Euclidean transfer matrix `T = exp(-a_τ H)` Wick-rotates to the
  Lorentzian unitary group `U(t) = exp(-itH)`. The Euclidean field
  equation in the static sector reduces to the resolvent equation
  `(H + iε)^{-1} → H^{-1} = G_0` as `ε → 0^+`, i.e., the static
  Euclidean field operator is again `H`. So
  `L_S |_{static} = H = -Δ_lat = H_spatial`.

In all three cases, `L |_{static} = -Δ_lat = H_spatial`. Hence

```text
    L  =  H  =  -Δ_lat                                                (2)
```

is forced by retained Hamiltonian uniqueness in the static sector.

**(K3) Closure identity is definitional.** Define the propagator
Green's function as `G_0 := H^{-1}` (the standard resolvent at zero
energy on the orthogonal complement of `ker(H)`; on a finite block
with vacuum subtracted, this is well-defined by (R-SC)). Then by (K2),

```text
    L^{-1}  =  H^{-1}  =  G_0                                         (3)
```

i.e., the closure identity `L^{-1} = G_0` previously stipulated in
`GRAVITY_CLEAN_DERIVATION_NOTE.md` Step 3 follows definitionally
from (K2) and the propagator definition.

Statements (K1)–(K3) constitute the **skeleton-selection bounded
theorem on A_min plus retained inputs**.

## Proof

The proof has four steps. Step 1 records that under (R-SCC) the
generator `H` is unique. Step 2 records that under (R-RP)+(R-SC) the
Wick rotation between Euclidean and Lorentzian sectors is faithful, so
the Euclidean / complex-action skeleton reduces to `H` in the static
sector. Step 3 records that the lattice d'Alembertian skeleton
reduces to `H` in the static sector. Step 4 concludes (K2)+(K3).

### Step 1 — Hamiltonian uniqueness on the equal-time slice

By (R-SCC) S1, the reconstructed `H` from the canonical action via
the (R-RP) factorisation is the **unique** generator of a
strongly-continuous one-parameter unitary group on `H_phys`. By
(R-SCC) S3, the temporal direction is the unique RP-admissible
reflection axis on the staggered-Dirac action, so there is no second
clock and no alternative `H'` arising from a different RP factorisation.

By (R-SCC) S2, the equal-time local algebra on `Σ_t` is the
mutually-commuting tensor product `A(Σ_t) = ⊗_{x ∈ Σ_t} Cl(3)_x`. The
spatial part of `H` (after restriction to the static sector) acts
within `A(Σ_t)` and is uniquely fixed by the canonical action's
spatial hops, which the Kawamoto-Smit construction realises as
`-Δ_lat` (`GRAVITY_CLEAN_DERIVATION_NOTE.md` Step 1).

Hence the framework's primary spatial kinematic operator on `Σ_t` is

```text
    H_spatial  =  H |_{static}  =  -Δ_lat                             (4)
```

with no operator-family freedom remaining.

This proves (K1).

### Step 2 — Euclidean / complex-action skeleton reduces to `H`

By (R-RP), the canonical Euclidean transfer matrix
`T : H_phys → H_phys` is positive Hermitian with `||T||_op ≤ 1`. By
(R-SC), `H := -(1/a_τ) log(T)` is self-adjoint and bounded below.
The Wick-rotation correspondence
`T^n = exp(-n a_τ H) ↔ U(t) = exp(-itH)` is faithful on the finite-dim
`H_phys` (`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`
Step 1).

Consider the Euclidean / complex-action skeleton. The full Euclidean
field equation arising from a quadratic action `S_E[φ] =
(1/2) ⟨φ, K_E φ⟩ + ⟨ρ, φ⟩` has equation of motion `K_E φ = -ρ`. On
the canonical surface (R-RP) factorisation gives `K_E = ∂_τ² + H` in
the temporal-spatial split. In the **static** (zero-frequency) sector
`∂_τ² → 0`, so `K_E |_{static} = H`. The Euclidean propagator is the
resolvent

```text
    G_E(0)  =  K_E^{-1} |_{static}  =  H^{-1}  =  G_0                 (5)
```

i.e., the static Euclidean field operator coincides with `H`, and the
static Euclidean propagator coincides with `G_0`. The
complex-action skeleton therefore selects `L = H` in the static
sector — no operator-family freedom remains.

This is the standard Wick-rotation static-limit identity, valid because
`H_phys` is finite-dim on a finite block by (R-RP) reconstruction and
the spectral expansion `T^n = sum_k λ_k^n |k⟩⟨k|`,
`H = sum_k E_k |k⟩⟨k|` is exact (`AXIOM_FIRST_SINGLE_CLOCK_*` Step 1
eq. (2)–(4)).

### Step 3 — Lattice-d'Alembertian skeleton reduces to `H`

The lattice d'Alembertian on the canonical block `Λ` is
`L_□ := ∂_t²_lat - Δ_lat`, where `∂_t²_lat` is the second-order
finite difference in the temporal direction. By (R-SCC) S2, each
`Σ_t` is a codimension-1 Cauchy hypersurface with the equal-time
local algebra `A(Σ_t)`. The static sector is the zero-frequency
sector in the temporal direction:

```text
    static sector :  ∂_t |φ⟩ = 0   ⟺   φ  is t-independent on Σ_t.    (6)
```

In this sector `∂_t²_lat |_{static} = 0`, so

```text
    L_□ |_{static}  =  - Δ_lat  =  H_spatial.                         (7)
```

The d'Alembertian skeleton therefore selects `L = H` in the static
sector — no operator-family freedom remains.

This is consistent with the (R-LR) Lieb-Robinson microcausality bound:
in the static sector, the lightcone constraint `d ≤ v_LR |t|`
becomes vacuous (`|t| = 0` in the static sector reduces the constraint
to `d ≤ 0`, i.e., equal-site only — but the kinematics is still
generated by spatial hops via `H_spatial = -Δ_lat`).

### Step 4 — Conclusion

By Step 1, the Hamiltonian skeleton selects `L = H = -Δ_lat`. By
Step 2, the Euclidean / complex-action skeleton selects the same
operator. By Step 3, the lattice-d'Alembertian skeleton selects the
same operator. Hence under retained Hamiltonian uniqueness plus
(R-PL) physical-lattice baseline,

```text
    L  =  H  =  -Δ_lat                                                (8)
```

is forced. By the propagator definition `G_0 := H^{-1}`,

```text
    L^{-1}  =  H^{-1}  =  G_0                                         (9)
```

definitionally. The closure identity `L^{-1} = G_0` previously
stipulated in `GRAVITY_CLEAN_DERIVATION_NOTE.md` Step 3 is therefore
a derived consequence of A_min + (R-RP) + (R-SC) + (R-LR) + (R-SCC) +
(R-PL). QED.

## Hypothesis set used

- A1 (Cl(3) per-site local algebra), A2 (Z^3 spatial substrate).
- (R-RP) retained reflection-positivity support theorem.
- (R-SC) retained spectrum-condition support theorem.
- (R-LR) retained microcausality / Lieb-Robinson support theorem.
- (R-SCC) retained single-clock codimension-1 unitary-evolution
  support theorem.
- (R-PL) retained physical-`Cl(3)`-on-`Z^3` baseline meta
  clarification.

No fitted parameters. No observed values used as proof inputs.

Standard external references (theorem-grade, no numerical input):
Stone (1932) one-parameter unitary group theorem; Streater-Wightman
(1964) chapter 3; Osterwalder-Schrader (1973) Wick rotation for
finite-dim transfer matrices; Wald (1994) chapter 14 (lattice
transfer-matrix Wick rotation); Sharatchandra-Thun-Weisz (1981)
staggered RP; Kawamoto-Smit (1981) staggered Cl(3) construction;
Maradudin et al. (1971) lattice Green's-function asymptotic on `Z^3`.

## Why bounded_theorem and not positive_theorem

The bound is twofold:

(B1) **Audit-status propagation.** All five retained inputs (R-RP,
R-SC, R-LR, R-SCC, R-PL) are either `unaudited` or
`audited_conditional` on the current authority surface — they are
"retained" by the source-note conventions of the physics-loop, but
the audit lane has not yet ratified them as `audited_clean`. By the
project's own retained-tier purity rule
(`feedback_retained_tier_purity_and_package_wiring`), a derivation
that consumes retained-but-unaudited support cannot itself promote to
`positive_theorem` until each cited input ratifies clean.

(B2) **Physical-lattice baseline meta.** (R-PL) is a meta
clarification (not itself a positive theorem) restoring repo baseline
semantics. The argument's "any candidate field operator must arise
from retained dynamical content" step inherits the meta status of
(R-PL): it says, in particular, that no out-of-framework operator
class (e.g., a fictitious finite-range smoothed Laplacian, a
nonlocal pseudodifferential operator outside the lattice's hopping
algebra, etc.) is admissible as a "primary" framework field
operator. That assertion follows from the physical-lattice baseline,
not from a class-A algebraic theorem.

Both bounds are explicitly named here. Neither bound is a hidden
admission; both are downstream-visible inputs that the audit lane can
audit independently.

The argument's algebraic core (Steps 1–4) is class-A under the cited
inputs. Promotion to `positive_theorem` becomes available once
(R-RP), (R-SC), (R-LR), (R-SCC) each promote to `audited_clean` on
the audit surface.

## Honest status

**Branch-local bounded theorem on A_min plus 5 retained-grade
support inputs and 1 retained meta clarification.** The algebraic
chain (K1)–(K3) is exact under the cited support theorems and the
physical-lattice baseline. The runner verifies, on a finite block,
the structural content of each step:

  (i) `H = -Δ_lat` on the canonical staggered-Dirac scalar sector
  (KS algebraic identity, machine-precision check),

  (ii) Euclidean / Lorentzian Wick-rotation correspondence via
  `T = exp(-a_τ H)` and `U(t) = exp(-itH)` on a finite-dim
  `H_phys` (spectral identity),

  (iii) Static-sector reduction `L_□ |_{static} = H_spatial` for
  the lattice d'Alembertian (zero-frequency restriction),

  (iv) Static-sector reduction `L_E |_{static} = H_spatial` for
  the Euclidean / complex-action skeleton (resolvent at zero
  energy),

  (v) Closure identity `L^{-1} = G_0` is definitional once
  `L = H` is fixed (matrix-inversion check on a finite block).

**Honest claim-status fields (audit-lane handoff):**

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  From A_min + retained reflection-positivity + retained spectrum
  condition + retained microcausality / Lieb-Robinson + retained
  single-clock codimension-1 unitary evolution + retained
  physical-`Cl(3)`-on-`Z^3` baseline meta clarification, the
  framework's primary spatial kinematic operator on the equal-time
  Cauchy slice in the static, zero-energy sector is unique and
  equals `H_spatial = -Δ_lat`. Any candidate field operator `L`
  for the static linear field equation `Lφ = -κρ` that is sourced
  by retained dynamical content reduces to `H_spatial` in that
  sector. Hence `L = H = -Δ_lat`, and the closure identity
  `L^{-1} = H^{-1} = G_0` follows definitionally from the
  propagator's definition. The bound is the audit-status
  propagation of the cited support theorems plus the physical-
  lattice baseline meta clarification, both named explicitly.
proposed_load_bearing_step_class: A (algebraic implication on the
  retained inputs; no external admissions beyond the cited support
  theorems)
status_authority: independent audit lane only
actual_current_surface_status: support
conditional_surface_status: derived bounded theorem on A_min + 4
  retained support theorems + 1 retained meta clarification
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: true
proposal_allowed_reason: |
  All cited inputs are retained on the current authority surface or
  are explicit retained meta clarifications. The proof proceeds via
  finite-dim spectral theory (Stone), the Wick-rotation
  correspondence on `H_phys`, and the standard static-sector
  zero-frequency reduction. No new axiom, no new fitted parameter,
  no new observed value, no new convention is introduced. The
  bound (R-PL meta + audit-status propagation of R-RP, R-SC, R-LR,
  R-SCC) is named explicitly. Promotion to `positive_theorem`
  becomes available when the four support theorems ratify
  `audited_clean`.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Not in scope.**

- Probe P4 admissions (b) `ρ = |ψ|²` and (c) `S = L(1 - φ)`. This
  note targets only (a). Those two admissions remain open and require
  separate source-theorem-notes.

- Continuum-limit identification of the lattice Green's function
  asymptotic `G(r) → 1/(4πr)`. That is `GRAVITY_CLEAN_DERIVATION_NOTE.md`
  Step 5 (theorem-grade lattice potential theory, Maradudin et al.
  1971) — already a theorem, not an admission.

- Promotion of `GRAVITY_CLEAN_DERIVATION_NOTE.md` to `audited_clean`.
  This note discharges admission (a) only; admissions (b) and (c)
  remain blocking the parent note's audit re-verdict.

## Relation to the gravity-clean lane

This note narrows the gravity-clean lane's previously-stipulated
closure identity `L^{-1} = G_0` (`GRAVITY_CLEAN_DERIVATION_NOTE.md`
Step 3, currently classified DERIVED via "framework's own closure
condition" but flagged by the auditor as not derived from A1) into
a **derived bounded consequence** of retained dynamical content.

After this note + an audit-clean ratification, the gravity-clean
chain has:

- Step 1 [DERIVED] `H = -Δ_lat` (KS, retained).
- Step 2 [DEFINITION] `G_0 := H^{-1}`.
- Step 3 [DERIVED] `L = H`, hence `L^{-1} = G_0` (this note, bounded
  conditional on the cited support theorems audit status).
- Step 4 [DERIVED] `(-Δ) φ = ρ` Poisson equation (from Step 3 + (b)).

Admission (a) is downgraded from "stipulated closure" to "derived
bounded conditional on retained Hamiltonian uniqueness." The
remaining two admissions (b) and (c) are unaffected by this note.

## Citations

- A_min: `MINIMAL_AXIOMS_2026-05-03.md`
- (R-RP) `AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
- (R-SC) `AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`
- (R-LR) `AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`
- (R-SCC) `AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`
- (R-PL) `PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`
- parent gravity-clean lane: `GRAVITY_CLEAN_DERIVATION_NOTE.md`
- parent self-consistency note: `GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`
- Probe P4 sharpening: PR #875 (G_NEWTON sharpened to 3 admissions)
- standard external references (theorem-grade, no numerical input):
  Stone, M. H. (1932), *Ann. Math.* 33, 643;
  Streater, R. F. & Wightman, A. S. (1964), *PCT, Spin and Statistics,
  and All That*, Benjamin (Wightman reconstruction);
  Osterwalder, K. & Schrader, R. (1973), *Comm. Math. Phys.* 31, 83;
  Sharatchandra, H. S., Thun, H. J., Weisz, P. (1981), *Nucl. Phys. B*
  192, 205;
  Kawamoto, N. & Smit, J. (1981), *Nucl. Phys. B* 192, 100;
  Wald, R. M. (1994), *Quantum Field Theory in Curved Spacetime and
  Black Hole Thermodynamics*, Univ. Chicago Press, ch. 14;
  Maradudin, A. A., Montroll, E. W., Weiss, G. H. & Ipatova, I. P.
  (1971), *Theory of Lattice Dynamics in the Harmonic Approximation*,
  Academic Press.
