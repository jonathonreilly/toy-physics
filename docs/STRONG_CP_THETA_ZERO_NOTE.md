# Strong CP / θ = 0 Conditional Action-Surface Closure

**Date:** 2026-04-16 (status line narrowed 2026-04-28 per audit-lane verdict)
**Status:** bounded conditional `θ_eff = 0` closure on the **explicitly θ-free Wilson-plus-staggered scalar-mass surface** that the runner restricts to. The decisive step is action-surface selection (no bare θ slot, real positive mass orientation), not a derived dynamical θ = 0 result. Not a tier-ratifiable strong-CP solution beyond that selected surface.
**Script:** `scripts/frontier_strong_cp_theta_zero.py`

## Theorem

**Theorem (retained-framework action-surface `θ_eff = 0` closure).**
On the retained Wilson-plus-staggered action surface of the `Cl(3)/Z^3`
framework,

    θ_eff = θ_QCD + arg det(M_u M_d) = 0

with no surviving loophole from:

1. fermion determinant / exact fermion-effective-action phase,
2. admissible axial or chiral basis rephasing inside the retained action class,
3. strong-sector phase generation when the fermions are integrated out, or
4. positive-weight topological-sector weighting away from `θ = 0`.

This is a **retained-action-surface** closure theorem. It is not a claim about
every continuum formulation, every regulator, or axion-model exclusion beyond
that retained surface.

## The Standard Strong CP Problem

In the Standard Model, the effective QCD vacuum angle is

    θ_eff = θ_QCD + arg det(M_u M_d)

where `θ_QCD` is the bare vacuum angle in the gluon action and
`arg det(M_u M_d)` is the phase of the quark-mass determinant. Both are
independent free parameters, generically `O(1)`, while experiment requires

    |θ_eff| < 10^-10

from the neutron electric dipole moment bound.

The question here is narrower and sharper: on the retained
Wilson-plus-staggered `Cl(3)/Z^3` action surface, does any strong-sector CP
phase survive at all?

## Four Closure Legs

### Leg A: Fermion phase closure

The staggered Dirac operator `D[U]` on the retained lattice surface is
anti-Hermitian:

    D† = -D.

For real mass `m > 0`, the eigenvalues of `D+mI` occur as conjugate pairs
`m ± i λ`, so

    det(D+mI) = Π_k (m^2 + λ_k^2) > 0.

This already removes the usual fermion-determinant phase. The retained package
now closes the fermion side more strongly than before:

1. the `3+1` APBC staggered operator remains anti-Hermitian on sampled
   retained `SU(3)` configurations,
2. `det(D+mI)` remains real positive there,
3. the exact fermion effective action is Gaussian,

       Γ_f = -Tr ln(D+m),

   so there are no higher fermion loops beyond that determinant, and
4. the sublattice generator `ε(x)=(-1)^{Σx}` gives `εD + Dε = 0`, forcing
   exact `±λ` pairing of the eigenvalues of `iD`, hence

       Im Γ_f = -Σ_k arctan(λ_k / m) = 0.

So the fermion phase is not merely small or sampled away. On the retained
surface it closes exactly, with the `3+1` APBC spectral audit serving as the
explicit verification layer.

### Leg B: Axial / chiral non-generation

The usual continuum loophole is an axial rotation that shifts phase between the
mass term and `θ_QCD`. On the retained staggered surface, the candidate axial
generator is the sublattice operator `ε`, and the admissible unitary transform
is

    U_α = exp(i α ε / 2).

Because `εD + Dε = 0`, the kinetic operator is invariant:

    U_α D U_α = D.

But the mass term rotates as

    U_α (mI) U_α = m (cos α I + i sin α ε).

Therefore:

1. only `α ∈ πZ` preserves a real mass operator,
2. any nontrivial continuous axial rotation introduces an imaginary
   pseudoscalar mass component,
3. that rotated mass operator is no longer a real scalar mass term, so it
   exits the retained Wilson-plus-staggered action class.

This closes the chiral/basis loophole on the retained surface. The framework
does not have a continuous admissible axial freedom that can move phase between
the mass term and a strong-sector `θ`.

### Leg C: Gauge-sector radiative non-generation

The retained action surface is fixed by the accepted package boundary:

1. `Cl(3)` local algebra,
2. `Z^3` spatial substrate,
3. finite Grassmann / staggered-Dirac partition,
4. physical-lattice reading,
5. canonical normalization.

Canonical normalization fixes the Wilson gauge coupling at

    β = 6.

So the retained action class is exactly:

    S_ret[U, ψ, ψ̄] = S_Wilson[U] + ψ̄(D[U] + m)ψ

with no bare `θ` slot.

Integrating out the fermions is exact on this surface:

    Z = ∫ DU det(D[U] + m) e^{-S_Wilson[U]}
      = ∫ DU exp(-S_eff[U]),

where

    S_eff[U] = S_Wilson[U] - ln det(D[U] + m).

Leg A already gives `det(D[U]+m) > 0`, so `ln det(D[U]+m)` is real. The
Wilson action is real and CP-even. Therefore `S_eff[U]` remains real and
strong-sector CP-even on the retained action surface.

The runner now checks this directly on sampled retained `3+1` configurations:

- `S_Wilson[U]` is real,
- the exact fermion effective action is real,
- the full retained effective action is real,
- linkwise complex conjugation preserves the full retained effective action.

This is the retained-framework version of radiative non-generation: exact
fermion integration does not generate a CP-odd strong-sector phase inside the
retained Wilson-plus-staggered action class.

### Leg D: Topological-sector positivity and the `θ = 0` minimum

The topological charge exists on the retained `3+1` surface, and the retained
partition function can be written formally as

    Z = Σ_Q Z_Q

with sector weights

    Z_Q = ∫_{Q[U]=Q} DU det(D[U] + m) e^{-S_Wilson[U]}.

Leg A and Leg C imply every retained integrand factor is real and positive, so

    Z_Q >= 0.

The `θ`-deformed partition is therefore

    Z(θ) = Σ_Q Z_Q e^{i θ Q}.

By the triangle inequality,

    |Z(θ)| <= Σ_Q Z_Q = Z(0),

so the retained free energy

    F(θ) = -ln |Z(θ)|

is minimized at `θ = 0`.

This is the exact topological closure needed here. It does **not** require a
closed-form first-principles expression for the detailed lattice measure
`Z_Q`. Positivity of the sector weights is enough.

The runner mirrors this mechanism with a sampled retained `3+1`
positive-weight `Q`-weighted family rather than a literal computed exact
sector decomposition:

- sampled retained positive weights are strictly positive,
- the sampled `θ`-sum obeys `|Z(θ)| <= Z(0)`,
- the sampled free energy is minimized at `θ = 0`.

## Relation to CKM CP Violation

The framework does contain CP violation, but only in the weak sector. The
`Z_3` source acts through the electroweak `1+2` split and produces the CKM
phase

    δ_std = arctan(√5) = 65.905°.

The color `SU(3)` is the graph-first commutant of the selected weak `SU(2)`.
The `Z_3` source does not provide a continuous strong-sector `θ`; it remains a
discrete weak-sector source. The runner keeps the exact finite checks:

- selected-axis `su(2)` closure,
- joint commutant dimension `10 = gl(3) ⊕ gl(1)`,
- `Z_3` eigenvalues are discrete cube roots of unity,
- `|det V_CKM| = 1`,
- explicit positive-mass `arg det(M_u M_d) = 0`.

So CKM CP remains weak-sector only and does not leak into `θ_eff`.

## Combined Result

The four legs now close together:

1. no fermion phase survives,
2. no admissible axial rephasing can move phase into a strong-sector `θ`,
3. exact fermion integration leaves the retained effective action real and
   CP-even,
4. positive topological-sector weights force the free-energy minimum to
   `θ = 0`.

Therefore, on the retained Wilson-plus-staggered action surface,

    θ_bare = 0,
    arg det(M_u M_d) = 0,
    θ_eff = 0.

This is now a **retained action-surface strong-CP closure package**.

## What Is Actually Proved

### Exact theorem-grade statements

1. the retained action class has 5 accepted inputs,
2. canonical normalization fixes the Wilson gauge coupling at `β = 6`,
3. `ε^2 = I`,
4. `U_α = exp(i α ε/2)` is unitary,
5. `U_α D U_α = D`,
6. `U_α (mI) U_α = m(cos α I + i sin α ε)`,
7. only `α ∈ πZ` preserves a real mass operator on the retained action class,
8. the selected-axis weak `su(2)` closes exactly,
9. the joint commutant has dimension `10 = gl(3) ⊕ gl(1)`,
10. the `Z_3` weak-sector source does not commute with the selected-axis
    `SU(2)`,
11. `Z_3` has only discrete cube-root eigenvalues,
12. `|det V_CKM| = 1`,
13. positive retained sector weights imply `|Z(θ)| <= Z(0)`, hence
    `F(θ)` is minimized at `θ = 0`.

### Accepted-surface definitions used by the closure

1. no bare `θ` slot appears in the retained Wilson-plus-staggered action
   class,
2. therefore `θ_bare = 0` on that retained action surface.

These are part of the accepted action-surface definition. They are load-bearing
for the closure claim, but the runner counts them as support/definition items
rather than standalone theorem passes.

### Retained-surface compute checks

1. free-field and gauged `Z^3` staggered determinant positivity,
2. `3+1` APBC determinant positivity on sampled retained `SU(3)` configurations,
3. sampled nontrivial topological charge without determinant phase generation,
4. `εD + Dε = 0` on the retained `3+1` APBC surface,
5. sampled exact `±λ` pairing of `iD`,
6. sampled `Im Γ_f = 0`,
7. sampled agreement between the spectral phase and the determinant phase,
8. sampled axial-grid audit matches the exact statement that only `α ∈ πZ`
   preserves a real mass operator,
9. explicit nontrivial axial rotation exits the retained scalar-mass action
   class,
10. the only admissible retained-surface axial endpoints keep zero determinant
    phase,
11. explicit positive-mass quark-surface audit gives `arg det(M_u M_d)=0`,
12. sampled retained effective action is real,
13. linkwise complex conjugation preserves the full retained effective action,
14. sampled retained positive-weight `Q`-weighted family obeys
    `|Z(θ)| <= Z(0)`,
15. the sampled retained free energy is minimized at `θ = 0`.

### Support only

1. Vafa-Witten sign-discipline consistency,
2. the statement that a detailed closed-form `Z_Q` measure is unnecessary for
   the retained `θ = 0` minimum theorem.

These support items are not counted as theorem-grade closure.

## What Is Not Claimed

1. **Unrestricted all-formulations closure.**
   The theorem is only about the retained Wilson-plus-staggered
   `Cl(3)/Z^3` action surface.

2. **Closed-form `Z_Q` measure on the physical `S^3` lattice.**
   The closure uses positivity and the `θ`-sum bound, not a closed-form
   instanton measure.

3. **Axion exclusion beyond the retained action surface.**
   The theorem says the retained action surface already closes strong CP.
   Broader axion-model exclusion is a separate question.

4. **Observable neutron-EDM matrix elements.**
   The surviving observable lane is the separate CKM neutron-EDM corollary /
   bounded-prediction note: the exact corollary `d_n(QCD) = 0` and
   CKM-only structure follow from this theorem plus the promoted CKM
   atlas/axiom package, while
   the numerical `d_n(CKM)` scale remains EFT-bridged.

## How This Changes The Paper

The strong-CP lane is no longer merely an exact structural theorem plus a
fermion-side support stack. It is now a retained-framework full closure package
on the retained action surface:

- fermion phase closure,
- axial/chiral non-generation,
- gauge-sector radiative non-generation inside the retained action class,
- topological-sector positivity with the `θ = 0` minimum.

The safe paper sentence is:

> On the retained Wilson-plus-staggered `Cl(3)/Z^3` action surface, strong CP
> closes completely: no bare `θ` appears, no admissible axial rephasing
> survives inside the retained action class, exact fermion integration does not
> generate a strong-sector CP phase, and positive topological-sector weights
> force the free-energy minimum to `θ = 0`.

## Experimental Predictions

1. **`θ_eff = 0` exactly on the retained action surface.**
2. **`d_n(QCD) = 0` on that retained surface.**
   The surviving observable neutron-EDM estimate is the separate CKM-only
   corollary / bounded quantitative lane, currently
   `d_n(CKM) ~ 8 x 10^-33 e cm`.
3. **Any observed strong-sector CP phase requires structure beyond the retained
   action surface.**

## References

- Vafa, C. and Witten, E. (1984). *Restrictions on Symmetry Breaking in
  Vector-Like Gauge Theories*, PRL 53, 535.
- Leutwyler, H. and Smilga, A. (1992). *Spectrum of Dirac operator and role of
  winding number in QCD*, PRD 46, 5607.
- Witten, E. (1979). *Current algebra theorems for the U(1) Goldstone boson*,
  Nucl. Phys. B 156, 269.
- Veneziano, G. (1979). *U(1) without instantons*, Nucl. Phys. B 159, 213.

## Commands Run

```bash
python3 scripts/frontier_strong_cp_theta_zero.py
# Exit code: 0
# THEOREM PASS=13  FAIL=0
# RETAINED-SURFACE COMPUTE PASS=30  FAIL=0
# SUPPORT=4
```

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, high criticality, 124 transitive
descendants):

> Issue: the decisive step is not a computed strong-CP cancellation
> but the retained-action-surface selection: the runner/support text
> takes 'no bare θ slot' and `θ_bare = 0` from the action-class
> definition, and it uses an explicit positive real quark-mass
> surface for `arg det(M_u M_d) = 0`. Why this blocks: the 13
> theorem and 30 retained-surface compute passes show internal
> consistency of that restricted θ-free Wilson-plus-staggered
> scalar-mass surface, but they do not derive from the provided
> audit packet that the physical Cl(3)/Z^3 action forbids an
> allowed CP-odd F̃F term, fixes the real-mass orientation, or
> dynamically selects θ = 0 rather than merely evaluating the
> θ-free surface.

> Claim boundary until fixed: it is safe to claim that on the
> explicitly θ-free Wilson-plus-staggered scalar-mass surface, the
> implemented determinant, axial-grid, effective-action, and sampled
> positive-weight checks find no generated strong-sector phase; it
> is not yet an audited solution of strong CP beyond that selected
> action surface.

## What this note does NOT claim

- A derivation that the Cl(3)/Z^3 action forbids the CP-odd `F̃F`
  term.
- A derivation of the positive real quark-mass orientation
  (`arg det(M_u M_d) = 0`) from the framework primitives.
- A dynamical selection of θ = 0; the runner evaluates a θ-free
  surface and finds no generated phase, but does not derive the
  surface's exclusion of CP-odd terms.

## What would close this lane (Path A future work)

Promoting from bounded conditional to retained would require:

1. A retained operator-basis / action-surface theorem deriving from
   Cl(3)/Z^3 primitives and canonical normalization that no
   gauge-invariant CP-odd θ term is an admissible slot.
2. A registered positive real quark-mass orientation /
   `arg det(M_u M_d) = 0` theorem as a dependency.
3. An updated runner that constructs the allowed action basis and
   fails if an `F̃F` term or complex mass phase is admitted.
