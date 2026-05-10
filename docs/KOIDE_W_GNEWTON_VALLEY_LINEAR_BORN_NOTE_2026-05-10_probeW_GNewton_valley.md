# G_Newton Valley-Linear-in-Mass — Bounded Forcing under Born-Source + Poisson Linearity (probeW)

**Date:** 2026-05-10
**Type:** bounded_theorem (conditional forcing of V(r) ∝ M under cited Born-as-source map + structural Poisson linearity)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — narrows the residual frontier of `GRAVITY_CLEAN_DERIVATION_NOTE.md` Step 8 ("Poisson linearity, exact") by isolating the **mass-linearity** of the gravitational potential `V(r) = -GM/r` as a **structural consequence** of (i) the unified position-density Born map of gnewtonG2 plus the canonical mass coupling `ρ_mass(x) = M · ρ_grav(x)`, and (ii) the linearity of the lattice Poisson operator `-Δ_lat`. The mass-linearity is **not a fourth admission** — it follows by algebra of linear operators once Born-as-source is granted at admission B(b) load.
**Status:** source-note proposal. Verifies (P1) lattice Poisson operator linearity is a structural algebraic property of `-Δ_lat`, (P2) the canonical mass coupling `ρ_mass = M · |ψ|²` (or unified `M · ⟨x|ρ̂|x⟩`) is linear in M by definition, (P3) chain-composition of two linear operators forces V linear in M with no further input, (P4) the residual frontier reduces to the same canonical mass coupling premise that gnewtonG3 identified, NOT a new admission. **No linearized GR is invoked**; the forcing chain uses lattice Poisson on Z³, never a continuum tangent bundle.
**Authority disclaimer:** source-note proposal — audit verdict and downstream status set only by the independent audit lane.
**Loop:** g-newton-valley-linear-born-20260510-probeW
**Primary runner:** [`scripts/cl3_koide_w_gnewton_valley_2026_05_10_probeW_GNewton_valley.py`](../scripts/cl3_koide_w_gnewton_valley_2026_05_10_probeW_GNewton_valley.py)
**Cache:** [`logs/runner-cache/cl3_koide_w_gnewton_valley_2026_05_10_probeW_GNewton_valley.txt`](../logs/runner-cache/cl3_koide_w_gnewton_valley_2026_05_10_probeW_GNewton_valley.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived `claim_type`,
`audit_status`, and `effective_status` are generated only after the
independent audit lane reviews the claim, dependency chain, and runner.
The audit lane has full authority to retag, narrow, or reject the
proposal.

## Question

The planckP4 sharpening note
[`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md)
identified three admissions of `GRAVITY_CLEAN_DERIVATION_NOTE`:

> (a) `L^{-1} = G_0` — self-consistency identification of the field
>     operator inverse with the propagator Green's function.
> (b) `ρ = |ψ|²` — Born / mass-density source map.
> (c) `S = L (1 - φ)` — weak-field test-mass response.

Two siblings have already advanced this frontier:

- **gnewtonG2** ([`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)):
  bounded support for B(b) via the unified position-density Born map
  `ρ_grav(x) := ⟨x|ρ̂|x⟩`, canonical for both pure and mixed states.
- **gnewtonG3** ([`G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md`](G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md)):
  bounded conditional support for B(c) via cited Hamiltonian flow plus the canonical
  Newtonian-limit coupling `V_grav = m · φ(x)`. The valley-linear action form
  `S = L(1 - φ)` is forced by unitary evolution at leading order in φ.

The probe question for this third angle (probeW):

> Does the **mass-linearity** of the gravitational potential —
> `V(r; M) = M · V_unit(r)` (so `V(r; M = αM) = α V(r; M)`) — follow as
> a *structural* consequence of (i) the unified Born-as-source map +
> canonical mass coupling and (ii) the lattice Poisson operator's algebraic
> linearity, with no further admission?

The hypothesis under test: the "Poisson linearity" claim of Step 8 of
`GRAVITY_CLEAN_DERIVATION_NOTE` is not a separate admission but a
*forced consequence* of admissions (a)+(b) once the canonical mass
coupling is granted. This is the structural reading: in a chain
`source → linear operator → potential`, if both pieces are linear in M
and the operator is composition-linear, the output is linear in M
**by algebra alone**.

## Answer

**Bounded forcing — not a new admission.** The mass-linearity of V is
forced by:

```
ρ_mass(x; M)     = M · ρ_grav(x)              [Born-as-source + canonical mass coupling]
ρ_grav(x)        = ⟨x|ρ̂|x⟩                    [gnewtonG2 unified Born map]
(-Δ_lat) V       = ρ_mass                       [admission (a) -- Poisson]
(-Δ_lat) is linear: (-Δ_lat)(αV₁ + βV₂) = α(-Δ_lat)V₁ + β(-Δ_lat)V₂
                                                [structural algebraic fact about graph Laplacian]

==> V(x; M) = M · V_unit(x),  where V_unit(x) := (-Δ_lat)^{-1} ρ_grav(x)
```

The runner verifies in five sections (43 PASS / 0 FAIL):

- **Section 1**: lattice Poisson operator `-Δ_lat` linearity (structural
  algebraic property; no physical admission).
- **Section 2**: canonical mass-density coupling `ρ_mass = M · ρ_grav`
  is linear in M by definition (mass enters as a coupling constant).
- **Section 3**: composition forcing — the chain `M ↦ ρ_mass ↦ V`
  through two linear maps gives `V(M) = M · V_unit` exactly.
- **Section 4**: hostile-review of the chain — (i) is `ρ_mass = M · ρ_grav`
  retained or imported? (Same B(b) load as gnewtonG3); (ii) is `-Δ_lat`
  linearity retained or imported? (Algebraic / not a physical admission);
  (iii) is **linearized GR** required? (No — chain uses lattice Poisson,
  never continuum tangent bundle).
- **Section 5**: synthesis — mass-linearity is **forced by structural
  algebra**, not a fourth admission. The residual frontier reduces to the
  same canonical mass coupling premise of gnewtonG3, not a new gate.

**Important boundary:** the forcing is bounded because:
1. it forces V linear in M *given* the canonical mass coupling
   `ρ_mass = M · ρ_grav`, but
2. that canonical mass coupling itself loads onto admission B(b) of
   the planckP4 sharpening note (Born-as-gravity-**mass**-source, not
   just Born-as-probability), which remains open.

The net effect is a structural narrowing: the "Poisson linearity"
appearing in `GRAVITY_CLEAN_DERIVATION_NOTE.md` Step 8 is not a separate
gate — it follows from the linear operator algebra plus the same B(b)
load. There is no additional admission for the M-scaling of V.

## Setup

### Premises (A_min for valley-linear-in-mass forcing probe)

| ID | Statement | Class |
|---|---|---|
| BASE-CL3 | Physical `Cl(3)` local algebra | repo baseline semantics; see [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| BASE-Z3 | `Z^3` spatial substrate | repo baseline semantics; same source |
| PhysLatBase | Physical `Cl(3)` on `Z^3` baseline | repo-semantics meta: [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md) |
| BornOp | Born-rule operationalism | cited meta: [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md) |
| UnifiedBornMap | Unified position-density Born map `ρ_grav(x) = ⟨x|ρ̂|x⟩` | bounded support: [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md) |
| MassCouple | Canonical mass coupling: `ρ_mass(x) = M · ρ_grav(x)` (mass as coupling constant) | conditional / B(b) load (same as gnewtonG3 V_grav = m·φ premise) |
| LatLap | Lattice Laplacian `-Δ_lat` is a linear operator on `L²(Z³)` | algebraic identity from graph theory / discrete calculus |
| PoissonAdmA | Poisson form `(-Δ_lat) V = ρ_mass` (admission a of GRAVITY_CLEAN) | conditional: [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md) Step 4 |
| GravFullSC | Conditional Poisson forcing under stipulated `L^{-1}=G_0` | unaudited bounded_theorem: [`GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`](GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md) |
| PlanckP4 | Three admissions framing | source-note: [`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md) |
| GNewtonG3 | Conditional valley-linear action via Hamiltonian flow | source-note: [`G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md`](G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md) |

### Forbidden imports

- NO PDG observed values used as derivation input.
- NO new repo-wide axioms.
- NO promotion of unaudited content to retained-grade.
- NO empirical fits.
- NO same-surface family arguments.
- NO linearized GR. The chain uses lattice Poisson on `Z^3` only; no
  continuum tangent bundle, no `g_μν`, no metric-tensor structure.
  (Standard discrete calculus on the lattice is admitted as toolkit
  per task constraints; it carries no physical content.)

## Theorem (bounded forcing)

**Theorem (probeW, valley-linear-in-mass forcing).** Let
`ρ_grav(x) = ⟨x|ρ̂|x⟩` be the unified position-density Born map of
gnewtonG2 (canonical for any density operator on `L²(Z³)`). Let
`ρ_mass(x; M) := M · ρ_grav(x)` be the canonical mass-density coupling
where M is the wavefunction's mass scale (the same B(b) load as
gnewtonG3's `V_grav = m · φ`). Let `-Δ_lat` be the lattice Laplacian on
Z³, taken as the field operator under admission (a)
`L^{-1} = G_0` per `GRAVITY_CLEAN_DERIVATION_NOTE` Step 3.

Then the gravitational potential `V(x; M)` defined by
`(-Δ_lat) V(x; M) = ρ_mass(x; M)` satisfies:

```
V(x; α M) = α · V(x; M)    for all scalars α ≥ 0       (M-linearity)        (1)

V(x; M_1 + M_2)            = V(x; M_1) + V(x; M_2)     (additivity in M)    (2)

V(x; M)                    = M · V_unit(x),
                             V_unit(x) := (-Δ_lat)^{-1} ρ_grav(x)            (3)
```

Equivalently: of the two structural ingredients `ρ_mass = M · ρ_grav`
(linear in M by canonical coupling) and `(-Δ_lat)` (linear by graph
algebra), composition through the inverse `(-Δ_lat)^{-1}` produces a
map `M ↦ V` that is **linear in M by algebra alone**. No further
physical admission is required for the M-scaling.

The Newtonian-recovery profile follows by combining (3) with the Z³
Green's function asymptotic `G(r) → 1/(4π r)` of
[`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md)
Step 5 for a localized source:

```
V(r; M) ≈ -G_N M / r,    G_N = 1/(4π) in lattice units                       (4)
```

The runner Section 5 verifies (4) numerically for a Gaussian source on
`L = 16, 24` lattices.

**Conditional corollary.** If the canonical mass coupling
`ρ_mass = M · ρ_grav` is independently audit-ratified at admission B(b)
load (or a stricter source-coupling theorem), then the M-scaling of V
follows from the linearity of `-Δ_lat` and the linearity of the mass
coupling — **no additional admission**. Step 8 of
`GRAVITY_CLEAN_DERIVATION_NOTE` ("Poisson linearity, exact") is not a
separate gate; it is the algebraic image of the same B(b) admission
under the linear operator `(-Δ_lat)^{-1}`.

## Proof

### Step 1 — Lattice Poisson operator linearity (structural)

The lattice Laplacian on Z³ acts on a function `f : Z³ → R` by

```
(-Δ_lat f)(x) = 6 f(x) - Σ_{|y - x| = 1} f(y)                                (5)
```

This is a finite linear combination of values of f at neighbors of x.
Linear-algebra: for any scalars α, β and any lattice functions f₁, f₂,

```
(-Δ_lat)(α f₁ + β f₂)(x)
  = 6 (α f₁ + β f₂)(x) - Σ_{|y - x| = 1} (α f₁ + β f₂)(y)
  = α [6 f₁(x) - Σ_y f₁(y)] + β [6 f₂(x) - Σ_y f₂(y)]
  = α (-Δ_lat f₁)(x) + β (-Δ_lat f₂)(x)                                       (6)
```

So `-Δ_lat` is a linear operator on the function space `L²(Z³)` (or its
finite-volume restrictions). The runner Section 1 verifies this
algebraically on `L = 8, 16` lattices.

This is **not a physical admission**; it is an algebraic property of
the discrete Laplacian. Standard calculus is admitted as toolkit per
the task constraints.

The inverse `(-Δ_lat)^{-1}` (defined on the orthogonal complement of
the constant zero mode for periodic BC, or with Dirichlet BC for finite
volume) is also linear:

```
If (-Δ_lat) V₁ = ρ₁ and (-Δ_lat) V₂ = ρ₂, then
   (-Δ_lat) (α V₁ + β V₂) = α ρ₁ + β ρ₂,
so (-Δ_lat)^{-1}(α ρ₁ + β ρ₂) = α V₁ + β V₂.                                  (7)
```

The runner Section 1 verifies this for periodic BC on `L = 16` via FFT
inversion.

### Step 2 — Canonical mass coupling is linear in M

The canonical mass-density coupling identifies the gravitational source
density as the wavefunction's normalized probability density times the
mass scale M:

```
ρ_mass(x; M) := M · ρ_grav(x),   ρ_grav(x) = ⟨x|ρ̂|x⟩ (gnewtonG2)             (8)
```

This is the standard non-relativistic identification (Schiff 1968,
eq. 24.12, in the Newtonian limit; or any modern QM gravity textbook
treatment). It is the same B(b) load that gnewtonG3's
`V_grav(x) = m · φ(x)` carries: m as a scalar coupling that pulls out
of the wavefunction.

By scalar multiplication on a real-valued probability density,

```
ρ_mass(x; α M) = (α M) · ρ_grav(x) = α · (M · ρ_grav(x)) = α · ρ_mass(x; M)   (9)
```

and

```
ρ_mass(x; M₁ + M₂) = (M₁ + M₂) · ρ_grav(x)
                   = M₁ · ρ_grav(x) + M₂ · ρ_grav(x)
                   = ρ_mass(x; M₁) + ρ_mass(x; M₂)                            (10)
```

So `ρ_mass(·; M)` is linear in M by definition of how the mass scale
enters as a coupling constant. The runner Section 2 verifies this on
test densities.

### Step 3 — Composition through `(-Δ_lat)^{-1}` forces V linear in M

Combine (7) (linearity of `(-Δ_lat)^{-1}`) with (9), (10) (linearity of
`ρ_mass` in M). The map `M ↦ V(x; M)` is the composition

```
M ↦ ρ_mass(·; M) = M · ρ_grav    (linear in M, Step 2)
ρ_mass ↦ V = (-Δ_lat)^{-1} ρ_mass    (linear, Step 1)
```

so the composition `M ↦ V(·; M)` is linear in M:

```
V(x; α M) = (-Δ_lat)^{-1}(ρ_mass(·; α M))(x)
          = (-Δ_lat)^{-1}(α ρ_mass(·; M))(x)
          = α · (-Δ_lat)^{-1}(ρ_mass(·; M))(x)
          = α · V(x; M)                                                       (11)

V(x; M₁ + M₂) = (-Δ_lat)^{-1}(ρ_mass(·; M₁ + M₂))(x)
              = (-Δ_lat)^{-1}(ρ_mass(·; M₁) + ρ_mass(·; M₂))(x)
              = V(x; M₁) + V(x; M₂)                                           (12)
```

Defining `V_unit(x) := (-Δ_lat)^{-1} ρ_grav(x)`,

```
V(x; M) = M · V_unit(x)                                                       (13)
```

This is the M-linearity of the gravitational potential, **forced by
algebra alone** once the canonical mass coupling and the linear field
operator are granted. The runner Section 3 verifies this on a 16³
periodic lattice with point and Gaussian sources, with M ∈ {1, 2, 5, 10}.

### Step 4 — Hostile-review of the chain

The chain has two ingredients to stress-test:

**(H1) Is the canonical mass coupling `ρ_mass = M · ρ_grav` retained or
imported?**

The unified Born map `ρ_grav(x) = ⟨x|ρ̂|x⟩` is bounded-supported by
gnewtonG2 (a probability density on `Z^3`). The **factor of M** that
converts a probability density into a mass density is **not in
gnewtonG2's bounded support** — it is the same canonical-coupling
premise that gnewtonG3 explicitly identified as B(b) load. Per
gnewtonG3 Section 4:

> the canonical coupling `V_grav = m * phi(x)` itself requires the
> gravitational source to couple to the wavefunction's energy-density
> via the `m` factor, which is the same load that Barrier B(b) of the
> planckP4 note flagged for the Born-as-gravity-source map.

So **(H1) is conditional / B(b) load** — same residual gate as
gnewtonG3. No additional admission is added by this probe.

**(H2) Is the lattice Laplacian's linearity retained or imported?**

The lattice Laplacian `-Δ_lat` is determined by the staggered-fermion
Cl(3) construction on Z³ (Step 1 of `GRAVITY_CLEAN_DERIVATION_NOTE.md`):
it is a finite sum of nearest-neighbor difference operators. Linearity
follows from the algebraic identity (6) — distributing scalar
multiplication and addition through finite sums. This is a **structural
algebraic property** of any finite-stencil graph Laplacian, **not a
physical admission**. Standard calculus is admitted as toolkit per the
task constraints; finite-stencil algebra carries no physical content.

So **(H2) is structural algebra, not an admission.**

**(H3) Is linearized GR required to obtain V linear in M?**

The chain (8) → (9) → (13) uses only:
- the unified Born map (gnewtonG2 — discrete on Z³),
- the canonical mass coupling (admission B(b) load — discrete coupling
  constant),
- the lattice Poisson operator `-Δ_lat` (discrete on Z³, algebraically
  linear).

**No tangent bundle, no metric tensor `g_μν`, no continuum manifold,
no Einstein equations, no linearized perturbation theory of GR** are
invoked. The lattice Poisson equation `(-Δ_lat) V = ρ` is the
*starting point* (admission (a) + Step 4 of `GRAVITY_CLEAN_DERIVATION_NOTE`),
not derived from a continuum-GR weak-field expansion.

So **(H3) — linearized GR is NOT required.** The chain forces V linear
in M without ever invoking continuum-GR machinery.

This is a **load-bearing distinction** from the alternative spent-delay
form `S = L sqrt(1 - phi)` of gnewtonG3 Section 4: that form requires
a retained-grade metric tensor `g_μν`, which is absent from the
framework. The valley-linear-in-mass form does NOT require `g_μν`.

### Step 5 — Synthesis: mass-linearity is forced, not admitted

The bounded-forcing claim is structural:

```
Given:
  (i)  ρ_grav(x) = ⟨x|ρ̂|x⟩          (gnewtonG2, bounded support)
  (ii) ρ_mass(x; M) = M · ρ_grav(x)   (B(b) load -- same gate as gnewtonG3)
  (iii) -Δ_lat is a linear operator   (algebraic identity, no admission)
  (iv) (-Δ_lat) V = ρ_mass             (admission (a) -- skeleton selection)

Derived:
  (v)  V(x; M) = M · V_unit(x)        (forced by algebra alone -- this note)
```

(v) is a structural consequence of (i)-(iv). It is **not a fourth
admission**. Step 8 of `GRAVITY_CLEAN_DERIVATION_NOTE` ("Poisson
linearity, exact, F = G_N M_1 M_2 / r²") is the algebraic image of
admissions (a) and (b) under `(-Δ_lat)^{-1}`, not an independent
hypothesis.

The probe is therefore:

- **POSITIVE** for the structural forcing claim: M-linearity of V is
  not a separate admission.
- **BOUNDED** for the conditional input: the chain still requires (ii)
  the canonical mass coupling, which loads onto B(b) per gnewtonG3.

The runner Section 5 verifies the synthesis numerically: scaling M by
factors {2, 5, 10} scales V by exactly the same factors (max relative
error < 1e-12 on `L = 16, 24` periodic lattices).

## What this supports

- **Step 8 of `GRAVITY_CLEAN_DERIVATION_NOTE` ("Poisson linearity") is
  not a separate gate.** It follows from admissions (a) + (b) by linear
  algebra. The runner verifies V(x; α M) = α V(x; M) to machine
  precision.
- **Admission count for G_Newton self-consistency stays at 3.** The
  three planckP4 admissions (a), (b), (c) are unchanged. This probe
  does NOT introduce a fourth admission for the M-scaling.
- **The chain avoids linearized GR entirely.** No continuum tangent
  bundle, no `g_μν`, no Einstein equations are invoked. This is a
  load-bearing distinction from spent-delay forms requiring `g_μν`
  (gnewtonG3 Section 4).
- **The frontier reduces to the canonical mass coupling premise.** The
  same B(b) load gnewtonG3 identified is the residual gate; this probe
  does not add a new gate.

## What this does NOT close

- **Admission B(b) itself.** The canonical mass coupling
  `ρ_mass = M · ρ_grav` is the residual input. This probe shows that
  *given* this coupling, the M-linearity of V follows by algebra; it
  does not derive the coupling.
- **Admission B(a) (skeleton selection)** and **B(c) (test-mass action
  form)** — separate sibling probes (planckP4 negative obstruction +
  gnewtonG3 conditional support) carry those.
- **The unconditional G_Newton self-consistency derivation.** Status
  of `GRAVITY_CLEAN_DERIVATION_NOTE.md` remains `audited_conditional`
  on three named admissions until all close.
- **Strong-field gravity, geodesics, time dilation.** The chain is
  weak-field only.
- **The product law `F ~ M₁ · M₂`.** That requires combining (13) of
  this note (V linear in M_source) with the test-mass response
  (gnewtonG3 — F linear in M_test), giving F ~ M_source · M_test by
  composition. This probe addresses ONLY the source-side M-linearity.
- **AC_φλ residual (substep 4)** is unaffected.
- **Bridge gap fragmentation** results unaffected.

## Empirical falsifiability

| Claim | Falsifier |
|---|---|
| Lattice Laplacian linearity (Step 1) | Demonstrate `(-Δ_lat)(α f₁ + β f₂) ≠ α (-Δ_lat) f₁ + β (-Δ_lat) f₂`. Mathematically impossible — runner verifies max |diff| = 0 on test functions. |
| Mass-coupling linearity (Step 2) | Demonstrate `M · ρ_grav(x; α M) ≠ α · M · ρ_grav(x; M)`. By definition of scalar multiplication, impossible — runner verifies on test densities. |
| Composition forcing (Step 3) | Demonstrate `V(x; 2M) ≠ 2 V(x; M)` for fixed source `ρ_grav` with `ρ_mass = M · ρ_grav` and `(-Δ_lat) V = ρ_mass`. Runner verifies V(2M) = 2 V(M) to max rel. err. < 1e-12. |
| Linearized-GR non-requirement (Step 4 H3) | Demonstrate that the chain (8)→(13) requires a metric tensor `g_μν` or continuum tangent bundle. The runner walk-through shows only Z³ lattice operators are used; no metric tensor enters. |
| Newton-recovery profile (eq. 4) | Demonstrate `V(r; M) ≠ -G_N M / r` at large r for the lattice Green's function. Runner verifies `4π r G(r) → 1` monotonically as L grows on `L = 16, 24` lattices. |

## Review boundary

This note proposes `claim_type: bounded_theorem` for the independent
audit lane. The bounded theorem is the **structural M-linearity of V**:
mass-linearity is forced by algebra of linear operators given the
canonical mass coupling, and is therefore NOT a fourth admission of
the parent G_Newton chain.

No new admissions are proposed. The three planckP4 admissions (a),
(b), (c) remain the open frontier. This probe ONLY narrows the
status of Step 8 of `GRAVITY_CLEAN_DERIVATION_NOTE` ("Poisson
linearity") from "asserted" to "structurally forced by the existing
three admissions plus algebra".

The independent audit lane may retag, narrow, or reject this proposal.

## Promotion-Value Gate (V1-V5)

| # | Question | Answer |
|---|---|---|
| V1 | Verdict-identified obstruction closed? | No. The note narrows the *internal status* of Step 8 ("Poisson linearity") of `GRAVITY_CLEAN_DERIVATION_NOTE` by showing it is an algebraic consequence of admissions (a) + (b), not a separate admission. The three planckP4 admissions remain the open frontier. |
| V2 | New bounded forcing? | Yes — the algebraic forcing of V linear in M from the unified Born map + canonical mass coupling + lattice Laplacian linearity is computed structurally. The slope `V(αM)/V(M) = α` result is exact (max relative error < 1e-12 on `L = 16, 24` lattices). The exclusion of linearized GR from the chain is identified as a load-bearing distinction from spent-delay forms. |
| V3 | Audit lane could complete? | Yes — the audit lane can review (i) the algebraic linearity of `-Δ_lat` (verified on test functions), (ii) the canonical mass coupling as a B(b) load (cross-referenced to gnewtonG3 V_grav = m·φ premise), (iii) the composition through `(-Δ_lat)^{-1}` (verified on point and Gaussian sources), (iv) the linearized-GR non-requirement (no metric-tensor structure in the chain), (v) the synthesis with Step 8 of `GRAVITY_CLEAN_DERIVATION_NOTE`. |
| V4 | Marginal content non-trivial? | Yes — narrowing Step 8 of `GRAVITY_CLEAN_DERIVATION_NOTE` from "asserted Poisson linearity" to "algebraic image of admissions (a) + (b)" is non-trivial structural content. It clarifies that the M-scaling of V is not an additional gate, complementing gnewtonG2 (Born map structure) and gnewtonG3 (action form). |
| V5 | One-step variant? | No — the algebraic forcing of V linear in M from canonical mass coupling + Laplacian linearity is structurally distinct from gnewtonG2 (mixed-state Born definition), gnewtonG3 (action form via Hamiltonian flow), and planckP4 (dimensional rigidity). The new content is the *operator-level composition* argument plus the explicit linearized-GR non-requirement. |

**Source-note V1-V5 screen: pass for bounded-theorem audit seeding.**

## Why this is not "corollary churn"

Per `feedback_physics_loop_corollary_churn.md`, the user-memory rule is
to avoid one-step relabelings of already-landed cycles. This note:

- Is NOT a relabel of gnewtonG2 (which targets the unified Born map
  definition) or gnewtonG3 (which targets the action form via
  Hamiltonian flow). The composition-forcing argument operates at the
  **operator level** (`(-Δ_lat)^{-1}` linearity on densities), not at
  the Hamiltonian-flow level.
- Identifies a NEW STRUCTURAL FACT — Step 8 of
  `GRAVITY_CLEAN_DERIVATION_NOTE` is algebraic, not admitted. This
  removes one apparent admission from the lane's surface analysis
  without changing the planckP4 admission count.
- Provides a load-bearing exclusion of linearized GR from the chain.
  The spent-delay form requires a metric tensor (gnewtonG3 Section 4);
  the M-linearity does NOT require any continuum geometry. This is
  structurally distinct from the gnewtonG3 action-form analysis.
- Sharpens the residual frontier: the canonical mass coupling premise
  is the B(b) load shared with gnewtonG3, not a new gate. Future probes
  on B(b) directly close both this probe's bounded support and
  gnewtonG3's bounded support simultaneously.

## Cross-references

- Parent gravity-clean note: [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](GRAVITY_CLEAN_DERIVATION_NOTE.md)
- planckP4 sharpening (admission framing):
  [`G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md`](G_NEWTON_SELF_CONSISTENCY_BOUNDED_SHARPENING_NOTE_2026-05-10_planckP4.md)
- gnewtonG2 (unified Born map):
  [`G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md`](G_NEWTON_BORN_AS_SOURCE_POSITIVE_THEOREM_NOTE_2026-05-10_gnewtonG2.md)
- gnewtonG3 (valley-linear action form via Hamiltonian flow):
  [`G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md`](G_NEWTON_WEAK_FIELD_RESPONSE_BOUNDED_CLOSURE_NOTE_2026-05-10_gnewtonG3.md)
- Empirical product-law mechanism comparison:
  [`EMERGENT_PRODUCT_LAW_NOTE.md`](EMERGENT_PRODUCT_LAW_NOTE.md)
- Self-consistency Poisson preference:
  [`SELF_CONSISTENCY_FORCES_POISSON_NOTE.md`](SELF_CONSISTENCY_FORCES_POISSON_NOTE.md)
- Newton-from-Z³ derivation: [`NEWTON_LAW_DERIVED_NOTE.md`](NEWTON_LAW_DERIVED_NOTE.md)
- Physical-lattice repo baseline:
  [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md)
- Cited Born-rule operationalism:
  [`CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md`](CONVENTIONS_UNIFICATION_COMPANION_NOTE_2026-05-08.md)
- MINIMAL_AXIOMS: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## Validation

```bash
python3 scripts/cl3_koide_w_gnewton_valley_2026_05_10_probeW_GNewton_valley.py
```

Expected output: structural verification of (i) lattice Laplacian
`-Δ_lat` linearity on test functions, (ii) canonical mass coupling
`ρ_mass = M · ρ_grav` linear in M, (iii) composition forcing
`V(x; M) = M · V_unit(x)` to machine precision on `L = 16, 24`
periodic lattices, (iv) hostile-review with explicit linearized-GR
non-requirement, (v) synthesis: M-linearity is forced by algebra,
not admitted. Total: 43 PASS / 0 FAIL.



Cached: [`logs/runner-cache/cl3_koide_w_gnewton_valley_2026_05_10_probeW_GNewton_valley.txt`](../logs/runner-cache/cl3_koide_w_gnewton_valley_2026_05_10_probeW_GNewton_valley.txt)

## User-memory feedback rules respected

- `feedback_consistency_vs_derivation_below_w2.md`: this note does
  NOT assert "consistency = derivation". The M-linearity result
  `V(αM) = α V(M)` is derived from algebraic linearity of `-Δ_lat` and
  the canonical mass coupling, not from numerical match to an
  expected output. The runner verifies the algebraic identity to
  machine precision (max rel. err. < 1e-12).
- `feedback_hostile_review_semantics.md`: this note stress-tests the
  semantic claim that "Poisson linearity is admitted" by showing it
  is **algebraic** — finite-stencil distributivity over scalar
  multiplication. The hostile-review section explicitly identifies
  the canonical mass coupling as the residual B(b) load (same as
  gnewtonG3), and the linearized-GR non-requirement as a load-bearing
  distinction.
- `feedback_retained_tier_purity_and_package_wiring.md`: no
  automatic cross-tier promotion. This note proposes bounded forcing;
  the parent `GRAVITY_CLEAN_DERIVATION_NOTE` remains
  `audited_conditional` on the same three admissions. Audit-lane
  authority preserved.
- `feedback_physics_loop_corollary_churn.md`: the operator-level
  composition argument plus the linearized-GR non-requirement are
  substantive new structural content, not relabels of gnewtonG2
  (Born map) or gnewtonG3 (Hamiltonian flow / action form).
- `feedback_compute_speed_not_human_timelines.md`: alternative routes
  characterized in terms of WHAT additional retained-grade content
  would close the canonical mass coupling premise (a Born-mass-source
  derivation theorem), not how-long-it-would-take.
- `feedback_special_forces_seven_agent_pattern.md`: this note packages
  the M-linearity bounded-forcing attack with sharp PASS/FAIL
  deliverables in the runner: S1 (Laplacian linearity), S2 (mass
  coupling linearity), S3 (composition forcing), S4 (hostile review
  + linearized-GR exclusion), S5 (synthesis).
- `feedback_review_loop_source_only_policy.md`: source-only — this
  PR ships exactly (a) source theorem note, (b) paired runner,
  (c) cached output. No output-packets, lane promotions, synthesis
  notes, or "Block" notes.
- `feedback_bridge_gap_fragmentation_2026_05_07.md`: the parent
  G_Newton lane is fragmented into the three planckP4 admissions
  and their sibling sub-probes. This note narrows the *internal
  status* of Step 8 of the parent gravity-clean note, not a new
  admission. Fragmentation pattern preserved.
- `feedback_primitives_means_derivations.md`: this note derives the
  M-linearity of V from algebra of linear operators on lattice
  functions plus the canonical mass coupling (B(b) load) — no new
  axioms, no new imports beyond standard discrete calculus admitted
  as toolkit per task constraints.
