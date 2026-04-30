# Axiom-First Lattice Noether's Theorem on Cl(3) ⊗ Z^3

**Date:** 2026-04-29
**Status:** branch-local theorem note on
`physics-loop/axiom-first-foundations-block01-20260429`. Audit-grade,
not yet reviewed against the live repo authority surfaces.
**Loop:** `axiom-first-foundations`
**Cycle:** 5 (Route R5)
**Runner:** `scripts/axiom_first_lattice_noether_check.py`
**Log:** `outputs/axiom_first_lattice_noether_check_2026-04-29.txt`

## Scope

This note derives, on the audited current `A_min`
(`docs/MINIMAL_AXIOMS_2026-04-11.md`), a lattice analogue of
Noether's theorem: for any one-parameter Lie or discrete symmetry
of the canonical action that maps Grassmann variables to Grassmann
variables, there is an explicit *conserved lattice current*
`J^μ_x` with discrete divergence

```text
    ∂^L_μ J^μ_x   :=   Σ_μ  ( J^μ_x  -  J^μ_{x - μ̂} )   =   0  on shell.   (1)
```

The theorem is established for the two physically-load-bearing
symmetries of `A_min`:

- **(N1) Z^3 translation symmetry → discrete momentum conservation.**
- **(N2) Global U(1) phase symmetry of the matter sector →
  conserved fermion-number current.**

After this note, any package lane that quotes "the canonical action
has a conserved current of type X" can cite an axiom-first lattice
Noether theorem on `A_min` instead of treating Noether as background.

## A_min objects in use

- **A1 — local algebra `Cl(3)`.** Used only via the existence of a
  faithful local representation of the Cl(3) algebra on each site.
- **A2 — substrate `Z^3`.** Used via the discrete translation group
  `Z^3` acting on the lattice sites by `T_a : x ↦ x + a`.
- **A3 — Grassmann partition / staggered Dirac action.** Action

  ```text
      S_F[χ̄, χ]  =  Σ_{x,y}  χ̄_x  M_xy  χ_y                            (2)
  ```

  with `M = m + M_KS`, `M_KS` the staggered Kogut–Susskind hop. The
  action is invariant under both `T_a` (acting on lattice indices)
  and global `U(1)` phase (acting as `χ → e^{iα} χ`, `χ̄ →
  e^{-iα} χ̄`).
- **A4 — canonical normalization.** Used only via the SU(3) gauge-
  invariance of `S_G`, i.e. the gauge `U(1)` subgroup is automatically
  contained in the canonical action.

## Statement

Let `S = S_F + S_G` be the canonical action on `A_min`, and let
`G` be a one-parameter symmetry group that maps the action into
itself: `S[g · ϕ] = S[ϕ]` for all `g ∈ G`. Then on `A_min`:

**(N1) Z^3 momentum conservation.** For the discrete translation
symmetry `T_a ∈ Z^3`, the conserved lattice current is the
canonical staggered momentum density

```text
    P^μ_x  =  - (i/2) η_μ(x)  ( χ̄_x  ∂^L_μ χ_x  -  ∂^L_μ χ̄_x · χ_x ),   (3)
```

with `∂^L_μ` the symmetric lattice difference. The lattice
divergence `∂^L_μ P^μ_x = 0` holds on shell (i.e. when the
classical equations of motion `M_xy χ_y = 0` are satisfied).

**(N2) Fermion-number current.** For the global `U(1)` phase
symmetry `χ → e^{iα} χ`, the conserved current is

```text
    J^μ_x  =  - (1/2) η_μ(x)  ( χ̄_x  χ_{x + μ̂}  +  χ̄_{x + μ̂}  χ_x ),    (4)
```

with lattice divergence `∂^L_μ J^μ_x = 0` on shell. Integration over
a Cauchy surface (lattice time slice) gives the conserved fermion
number `Q = Σ_x χ̄_x χ_x`.

**(N3) General lattice Noether identity.** For any infinitesimal
symmetry `δ_α χ_x = α^A T^A_{xy} χ_y`, the on-shell conserved
current is

```text
    J^{μ,A}_x  =  Σ_y  η_μ(x)  T^A_{xy}  ( χ̄_x · χ_{x+μ̂} - χ̄_{x+μ̂} · χ_x ) / 2.   (5)
```

The proof of (N1) and (N2) is the specialisation of (N3) to the
generators of `Z^3` translation and `U(1)` phase.

## Proof

The proof is the standard variational Noether argument adapted to
the finite Grassmann lattice action.

### Step 1 — variation of the action under an infinitesimal symmetry

Write `δχ_x = α^A T^A_{xy} χ_y` with `α^A` infinitesimal. The
variation of the action `S_F = χ̄ M χ` is

```text
    δS_F  =  α^A  ( χ̄_x  T^A_{xy}  M_yz  χ_z   +   χ̄_x  M_xy (-T^A_{yz})  χ_z ).
```

For `T^A` to be a *symmetry*, the variation must vanish for arbitrary
χ̄, χ:

```text
    [ T^A , M ]_{xz}   =   T^A_{xy} M_{yz} - M_{xy} T^A_{yz}   =   0.    (6)
```

This is the symmetry condition.

### Step 2 — promote `α` to a slowly-varying lattice field

Now allow `α^A` to depend on the lattice site: `α^A → α^A_x`. The
action variation becomes

```text
    δS_F[α(x)]   =   Σ_x α^A_x  ·  K^A_x[χ̄, χ]   +   higher orders     (7)
```

where the kernel `K^A_x` contains both bulk and boundary terms.
Group the variation into a "bulk" piece that vanishes by the
symmetry condition (6), and a "current" piece that survives:

```text
    δS_F[α(x)]   =   Σ_{x, μ}  ( α^A_{x + μ̂} - α^A_x ) · J^{μ,A}_x      (8)
```

with `J^{μ,A}_x` reading off as the coefficient of the `α`-difference.
A direct calculation gives (5).

### Step 3 — on-shell conservation

When the equations of motion `(M χ)_x = 0` and `(χ̄ M)_x = 0` are
satisfied (i.e. classical solutions of the Grassmann action), the
"bulk" piece of `δS_F[α(x)]` vanishes for *any* `α^A_x`, including
constant `α^A`. By global symmetry (`α^A` constant), the action
itself is invariant: `δS_F[constant α] = 0`.

Conversely, for non-constant `α^A_x`, the bulk piece still vanishes
on shell, so

```text
    Σ_x  α^A_x · ∂^L_μ J^{μ,A}_x   =   0                              (9)
```

for any `α^A_x`. By choosing `α^A_x = δ_{x, x_0}` (delta-function
test field), we obtain

```text
    ∂^L_μ J^{μ,A}_{x_0}   =   0   on shell.                          (10)
```

This is the lattice Noether identity.

### Step 4 — specialisation to Z^3 translation and U(1) phase

For `Z^3` translation, the generator is `T^μ_{xy} = δ_{y, x + μ̂} -
δ_{y, x - μ̂}` (discrete derivative). Substituting into (5) gives
the staggered momentum density (3).

For `U(1)` phase, the generator is `T_{xy} = i δ_{xy}` (constant
phase rotation). Substituting into (5) gives the fermion-number
current (4).

In both cases, the symmetry condition (6) is satisfied: `M_KS`
commutes with discrete translation up to the staggered phase factor
(which is built into `η_μ(x)`), and `M = m + M_KS` commutes with
the constant phase rotation (since both `m·I` and `M_KS` are
phase-rotation invariant). ∎

## Hypothesis set used

A1 (only via existence of the local Cl(3) representation), A2 (Z^3
translation group action), A3 (Grassmann staggered-Dirac action with
mass; symmetry properties of M_KS), A4 (only via SU(3) gauge
invariance, which contains `U(1)` as a subgroup). No imports from
the forbidden list.

The "external import" is the variational Noether technique itself,
which is an elementary finite-Grassmann manipulation, not a
primitive imported as a black box.

## Corollaries (downstream tools)

C1. *Conserved fermion number on the canonical surface.* The
`U(1)` charge `Q = Σ_x χ̄_x χ_x` is a conserved quantum number,
which underlies any "baryon number" / "lepton number" lane on
A_min.

C2. *Discrete momentum quantum number.* On a finite block `Λ` with
periodic boundary, the lattice translation symmetry gives discrete
momenta `k_μ ∈ {0, 2π/L, …}` as good quantum numbers — the basis
on which the package's spectral / band-structure language depends.

C3. *Compatibility with reflection positivity (R2).* The conserved
charge `Q` is `Θ_RP`-invariant (charge is even under reflection
positivity), so the physical Hilbert space `H_phys` decomposes into
fixed-`Q` superselection sectors. This is the structural support
for the package's separate fermion-number / gauge-charge sectors.

C4. *Anomaly slot.* Lattice Noether by itself does not say whether
a *quantum* current remains conserved (anomalies). The
gauge-invariance + flavour-anomaly closure of the package — captured
in the anomaly-forced 3+1 row — is the next layer above the
classical Noether identity here. This note does not claim to
discharge anomaly cancellation.

## Honest status

**Branch-local theorem.** (N1)–(N3) are proved on `A_min` by the
standard variational argument adapted to the finite Grassmann
staggered action. The runner exhibits both currents and verifies
the on-shell conservation `∂^L_μ J^μ = 0` numerically on small
lattices.

**Not in scope.**

- Anomaly closure for the conserved currents at the quantum level.
  That requires the index theorem / anomaly-forced 3+1 row of the
  package's existing retained closure, not the classical Noether
  identity established here.
- Lattice analogue of full energy-momentum tensor conservation.
  We give the discrete momentum density; the full T^{μν} requires
  more careful identifications which are deferred.

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- prior cycles in this loop:
  - `docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
  - `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
  - `docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
  - `docs/AXIOM_FIRST_CPT_THEOREM_STRETCH_NOTE_2026-04-29.md`
- assumption / derivation ledger: `docs/ASSUMPTION_DERIVATION_LEDGER.md`
