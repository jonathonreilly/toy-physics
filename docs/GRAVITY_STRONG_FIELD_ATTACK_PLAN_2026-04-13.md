# Strong-Field Gravity Attack Plan

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Purpose:** Codex-owned research plan for the strongest remaining gravity upside:
full nonlinear / strong-field closure beyond the retained weak-field surface,
now understood as a **3D shell/junction theorem plus a 3+1 spacetime lift**,
not a symmetric 4D lattice derivation.

## Current honest state

The repo already supports a strong weak-field gravity surface:

- Poisson / Newton chain
- weak-field WEP
- weak-field time dilation

It does **not** yet support full nonlinear GR closure.

The strongest currently defensible strong-field statement is narrower:

- within the current conformal spatial-metric ansatz and leading
  self-consistency closure, the lattice point-source fixed point remains
  spatially nondegenerate
- this is **not** the same thing as a fully derived strong-field spacetime
  metric

New exact foothold now extracted on this branch:

- for a rank-one additive attractive local potential,
  the strong-field enhancement factor used in the point-source note is an
  exact resolvent identity
- see `docs/STRONG_FIELD_RESOLVENT_CLOSURE_NOTE.md`
- this removes one heuristic from the current point-source closure, but it does
  **not** yet produce the full strong-field spacetime metric

New exact foothold extracted after that:

- the same resolvent program now extends beyond the rank-one source to a
  finite-support diagonal attractive source class
- the exact field can be written as `phi = G_0 P (I - V G_S)^-1 m`
- see `docs/DISTRIBUTED_SOURCE_SPACETIME_CLOSURE_NOTE.md`
- this removes the "point source only" limitation from the exact source-model
  foothold, but still does **not** derive the physical matter source class

New bounded bridge now extracted on this branch:

- for the standard static isotropic vacuum system, the spatial conformal factor
  `psi` and the combination `alpha psi` are both harmonic outside the source
- this fixes the isotropic Schwarzschild lapse once the spatial harmonic data
  are given
- see `docs/STATIC_ISOTROPIC_VACUUM_BRIDGE_NOTE.md`
- this is **not** a framework derivation of full GR; it sharpens the temporal
  sector target by showing what a common static vacuum closure would force

New bounded bridge sharpened after that:

- the finite-support source theorem now provides one common exterior harmonic
  field that can drive both `psi` and `alpha` through
  `psi = 1 + phi`, `alpha psi = 1 - phi`
- see `docs/DISTRIBUTED_SOURCE_SPACETIME_CLOSURE_NOTE.md`
- this is still **bounded**, because the static isotropic vacuum bridge itself
  has not yet been derived from the lattice closure rather than imported as
  the correct exterior target

New exact/bounded split extracted after that:

- the exact source-model foothold now extends further to a finite-rank
  positive-semidefinite support operator, not just a diagonal support source
- see `docs/FINITE_RANK_GRAVITY_RESIDUAL_NOTE.md`
- the direct common-source 4D metric candidate built from that exact field has
  a nonzero vacuum Einstein residual outside the source
- the monopole-projected isotropic candidate built from the same exact field
  reduces that residual by roughly `6.5e2`
- this pinpoints the remaining gap:
  the theorem-grade reduction from the exact finite-rank harmonic exterior
  field to the isotropic-vacuum surface

New exact/bounded asymptotic reduction extracted after that:

- for the exact cubic-symmetric finite-rank source class, the renormalized
  support source and the exact exterior field are both `O_h`-invariant
- the first non-monopole exterior correction is the unique cubic `l=4` mode
- the relative exterior anisotropy decays with a bounded slope consistent with
  quartic suppression, and is already `~1.6e-3` by radius `r = 6`
- see `docs/CUBIC_MONOPOLE_REDUCTION_NOTE.md`
- this means the asymptotic isotropic reduction is no longer ad hoc for that
  exact source class; the remaining gap is why the physical source lands in,
  or flows to, that cubic-symmetric sector strongly enough near the source

New exact/bounded local-source-class result extracted after that:

- the most general real symmetric local `O_h`-invariant source operator on the
  star support has an exact five-parameter commutant, and the corresponding
  invariant bare source vector has exact dimension two
- scanning that full exact local cubic source class materially lowers the
  direct 4D residual floor, but does **not** remove it
- see `docs/OH_SOURCE_CLASS_NOTE.md`
- this removes “wrong local cubic source family” as the main explanation for
  the remaining residual and pushes the live blocker onto near-source matching
  or the exterior metric law itself

New bounded same-source metric result extracted after that:

- allowing the direct metric closure to deform within the simplest nonlinear
  same-source quadratic family improves the 4D residual only marginally
- see `docs/SAME_SOURCE_METRIC_ANSATZ_SCAN_NOTE.md`
- this removes the easy hope that the remaining gravity gap is just a tiny
  low-order metric reparameterization of the same exact field

New bounded coarse-grained exterior-law result extracted after that:

- projecting the exact lattice exterior data onto the unique radial harmonic
  law `phi_eff = a/r` outside a finite matching radius gives a vacuum-close
  static isotropic exterior metric on both the exact local `O_h` source class
  and the broader exact finite-rank source class
- see `docs/COARSE_GRAINED_EXTERIOR_LAW_NOTE.md`
- this means the remaining gravity problem is now much more explicitly the
  microscopic-to-macroscopic matching theorem, not the macroscopic exterior
  law itself

New bounded matching-window result extracted after that:

- the coarse-grained radial harmonic exterior law does not merely become good
  asymptotically; it becomes vacuum-close in a finite matching band around
  `R_match ~ 4.0 - 4.5` across both the exact local `O_h` family and the
  broader exact finite-rank source family
- see `docs/MATCHING_RADIUS_WINDOW_NOTE.md`
- this sharpens the remaining gravity target from “find some matching” to
  “derive why this finite matching window emerges from the exact lattice data”

New exact/bounded matching-decomposition result extracted after that:

- the exact exterior field now admits a lattice-native decomposition
  `phi = Q G_0 + h`, where `Q` is the conserved enclosed discrete charge,
  `G_0` is the unit point-source lattice Green function, and the remainder
  `h` carries zero monopole charge
- see `docs/FLUX_FIXED_MATCHING_DECOMPOSITION_NOTE.md`
- for the exact local `O_h` source family, the shell data are already exactly
  captured by `Q G_0` outside the source
- for the broader exact finite-rank source family, the shell-level mismatch is
  already at the percent level by `R_match ~ 3 - 4.5`
- this means the matching problem is no longer “find the monopole law”; it is
  now specifically the shell/angular coarse-graining of the zero-monopole
  remainder and the near-source sewing to the 4D metric

New exact/bounded shell-projector result extracted after that:

- for the seven-point star support
  `S = {0, ±e_x, ±e_y, ±e_z}`, the shell-mean profiles of the seven point-Green
  columns agree to machine precision on every tested shell
- by linearity, any exact source supported on `S` therefore has shell-averaged
  exterior field fixed exactly by total charge:
  `<phi>_shell = Q K_shell`
- see `docs/STAR_SUPPORT_SHELL_PROJECTOR_NOTE.md`
- this applies directly to both the exact local `O_h` family and the broader
  exact finite-rank family already on the branch
- this removes shell-level coarse-graining itself as the live blocker for the
  current star-supported source classes

New bounded sewing-band result extracted after that:

- once the exact shell projector is imposed, a smooth blend of
  `(psi, alpha psi)` between the microscopic interior and the charge-fixed
  radial harmonic exterior localizes the remaining nonvacuum content to a
  finite matching shell `3.0 < r < 5.0`
- outside that shell, the exterior residual is already `~1e-6` to `~3e-6`
  across both exact source families
- see `docs/LOCALIZED_SEWING_BAND_NOTE.md`
- this does not derive the sewing-shell dynamics, but it shows the remaining
  mismatch does not need to leak into the macroscopic exterior

New exact shell-kernel derivation extracted after that:

- the universal sewing-shell profile is now derived as the exact discrete
  Dirichlet-to-Neumann shell source of the centered point-Green exterior trace
- see `docs/DISCRETE_DTN_SHELL_KERNEL_NOTE.md`
- the normalized shell kernel agrees to machine precision across all seven
  star-support point-Green columns and matches the previously extracted
  universal shell profile of both the exact local `O_h` family and the broader
  exact finite-rank family
- this removes “derive the universal shell kernel itself” from the live
  blocker list and replaces it with the interpretation problem: what effective
  shell stress / sewing law this exact DtN kernel represents in the nonlinear
  4D closure

New exact/bounded orbit-channel reduction extracted after that:

- the anisotropic sewing-shell remainder is no longer an uncontrolled angular
  sector for the current exact source families
- its orbit-sum support is confined to four cubic orbit channels
  `(3,2,2)`, `(3,3,0)`, `(4,1,0)`, `(4,1,1)` with exact shellwise cancellation
- after normalizing by one anchor channel amplitude, both the orbit-sum vector
  and the shell-mean exterior response are identical across the exact local
  `O_h` family and the broader exact finite-rank family
- see `docs/ORBIT_CHANNEL_SHELL_REMAINDER_NOTE.md`
- the shell-mean anisotropic correction stays below `8.1%` of the radial-shell
  contribution outside the sewing band
- this removes “large uncontrolled anisotropic shell sector” from the live
  blocker list and narrows the remaining problem to deriving the amplitude and
  stress meaning of one universal cubic orbit-channel correction

New exact/bounded reduced-mode origin extracted after that:

- the universal anisotropic orbit-channel pattern is not just shared by the
  two current exact source families
- on the reduced orbit/shell-mean surface, it is already the unique exact DtN
  mode induced by the star-support point-Green columns
- see `docs/DTN_ORBIT_MODE_NOTE.md`
- this removes “family-coincidence only” from the live blocker list and
  leaves the amplitude / shell-stress interpretation as the next gravity step

New exact/bounded one-parameter shell-law result extracted after that:

- on the current star-supported exact source class, the reduced sewing-shell
  law is fixed entirely by total charge `Q`
- the exact reduced law has the form
  `sigma_red(Q) = Q * (k_rad + c_aniso * m_orb)`
  with:
  - exact radial DtN shell kernel `k_rad`
  - exact reduced anisotropic DtN mode `m_orb`
  - exact lattice constant `c_aniso = 0.081435402995901`
- the exact local `O_h` and broader finite-rank source families satisfy that
  same one-parameter reduced shell law to machine precision
- see `docs/ONE_PARAMETER_REDUCED_SHELL_LAW_NOTE.md`
- this removes “free anisotropic shell amplitude” from the live blocker list
  and leaves the nonlinear shell-stress / junction interpretation as the next
  gravity step

New exact/bounded reduced-junction operator result extracted after that:

- on the current exact star-supported source class, the reduced sewing-shell
  law is already one exact rank-one operator
- the reduced-junction matrix factors as
  `J_red = v_red * (1,1,...,1)`, i.e. one fixed reduced junction vector
  composed with the total-charge functional
- the exact local `O_h` and broader finite-rank source families lie on that
  same reduced-junction image to machine precision
- see `docs/REDUCED_JUNCTION_OPERATOR_NOTE.md`
- this removes “unknown reduced junction operator” from the live blocker list
  and pushes the remaining gravity problem onto the lift from reduced
  shell/exterior data to the full nonlinear 4D closure

New exact/bounded discrete shell-action result extracted after that:

- the charge-normalized exact reduced junction vector now admits a discrete
  quadratic shell action `J(z) = 1/2 ||z - v_red||^2` whose stationary point
  is the exact reduced junction law
- on the exact local `O_h` class, zero orbit spread on `3 < r <= 5` lifts that
  reduced stationarity point to the exact pointwise shell law
- see `docs/OH_DISCRETE_SHELL_ACTION_NOTE.md`
- this removes the last "no variational interpretation" ambiguity, but it does
  **not** yet derive the shell action itself from the microscopic lattice
  Hamiltonian or a genuine simplicial Regge action

New broader-support result extracted after that:

- the exact bridge package now widens beyond compact finite support to
  noncompact source tails with sufficiently fast decay
- exponentially localized tails are truncation-stable on the current box
- steep algebraic tails remain compatible only while the low moments stay
  finite
- generic long-range power-law tails are obstructed:
  - `p <= 3` fails already at the monopole level
  - `3 < p <= 5` fails the finite-shell / quadrupole closure test
- see `docs/BROADER_SUPPORT_CLASS_GRAVITY_NOTE.md`
- this means the live blocker is no longer “compact vs noncompact” in the
  abstract; it is the exact low-moment decay threshold, and beyond that a
  genuinely nonlocal or tensorially broader bridge principle

New exact/bounded reduced shell-stress lift extracted after that:

- on the outer half of the sewing band `4 < r <= 5`, the reduced outer-shell
  source profile per unit charge and the reduced exterior potential profile per
  unit charge are exact and universal across the star-support point-Green
  columns
- under the static isotropic conformal bridge, this gives one exact
  charge-parameterized reduced shell-stress family:
  - `rho_Q(r) = Q k(r) / (2 pi (1 + Q u(r))^5)`
  - `S_Q(r) = 0.5 rho_Q(r) (1/alpha_Q(r) - 1)`
  - `alpha_Q(r) = (1 - Q u(r)) / (1 + Q u(r))`
- the exact local `O_h` and broader finite-rank source families satisfy that
  reduced outer-shell stress law to machine precision
- see `docs/REDUCED_OUTER_SHELL_STRESS_LAW_NOTE.md`
- this removes “reduced shell-stress lift on the DtN side of the shell” from
  the live blocker list and leaves the local whole-shell lift and the bridge
  derivation itself as the next targets

New exact/bounded reduced whole-shell stress lift extracted after that:

- on the full sewing band `3 < r <= 5`, the reduced radial source profile per
  unit charge and reduced exterior-projector potential profile per unit charge
  are exact and universal across the star-support point-Green columns
- on the inner half `3 < r <= 4`, the reduced exterior-projector potential
  vanishes exactly, while on the outer half `4 < r <= 5` it matches the
  previously derived DtN-side profile
- under the static isotropic conformal bridge, this gives one exact
  charge-parameterized reduced whole-shell stress family:
  - `rho_Q(r) = Q k(r) / (2 pi (1 + Q u(r))^5)`
  - `S_Q(r) = 0.5 rho_Q(r) (1/alpha_Q(r) - 1)`
  - `alpha_Q(r) = (1 - Q u(r)) / (1 + Q u(r))`
- the exact local `O_h` and broader finite-rank source families satisfy that
  same reduced whole-shell stress law to machine precision
- see `docs/REDUCED_WHOLE_SHELL_STRESS_LAW_NOTE.md`
- this removes “reduced whole-shell stress lift on the current bridge surface”
  from the live blocker list and leaves the local/angular lift and the bridge
  derivation itself as the next targets

New exact/bounded orbit-resolved whole-shell law extracted after that:

- on the full sewing band `3 < r <= 5`, the orbit-mean exterior-projector
  potential profile per unit charge and orbit-mean shell-source profile per
  unit charge are exact and universal across the exact local `O_h` and broader
  exact finite-rank source families
- for the exact local `O_h` family, that orbit-mean law is already pointwise
  exact on each orbit
- for the broader exact finite-rank family, the remaining within-orbit
  correction stays small:
  - `u` below about `1.4%`
  - `k` below about `1.7%`
  - bridge-side `rho` below about `1.4%`
  - bridge-side `S` below about `2.7%`
- the universal orbit-mean profiles already predict the finite-rank orbit-mean
  bridge stress law with tiny absolute error
- see `docs/ORBIT_MEAN_WHOLE_SHELL_STRESS_LAW_NOTE.md`
- this removes “generic local/angular shell freedom” from the live blocker list
  and leaves the bridge derivation itself plus the final pointwise 4D lift as
  the remaining targets

New exact/bounded same-charge bridge closure extracted after that:

- for an exact exterior field `phi_ext` with shell source `sigma_R` and total
  shell charge `Q`, any common-harmonic bridge family
  `psi_c = 1 + c phi_ext`, `chi_c = 1 - c phi_ext` carries shell charges
  `+cQ` and `-cQ`
- exact same-source / same-charge inheritance therefore fixes `c = 1`
- the unique same-charge common-harmonic bridge on the current exact source
  classes is:
  - `psi = 1 + phi_ext`
  - `chi = alpha psi = 1 - phi_ext`
- both are exact exterior harmonic functions outside the sewing shell
- off-diagonal coefficient mismatch in the natural two-parameter common-
  harmonic metric family worsens the exterior 4D vacuum residual by more than
  an order of magnitude on both current exact source families
- see `docs/NATIVE_STATIC_BRIDGE_CLOSURE_NOTE.md`
- this removes “bridge derivation itself” from the live blocker list and
  leaves the final pointwise 4D Einstein/Regge lift as the remaining target

New exact/bounded pointwise shell closure extracted after that:

- on the exact local `O_h` source class, the whole-shell exterior-projector
  profile and shell-source profile are already pointwise exact on each cubic
  orbit across `3 < r <= 5`
- with the same-charge bridge fixed, the induced whole-shell bridge density
  `rho` and stress-trace `S` are also pointwise exact on each orbit
- on the broader exact finite-rank family, the remaining within-orbit
  correction stays small:
  - `u` below about `1.4%`
  - `k` below about `1.7%`
  - `rho` below about `1.4%`
  - `S` below about `2.7%`
- see `docs/OH_POINTWISE_SHELL_CLOSURE_NOTE.md`
- this removes “local/angular shell freedom on the symmetric source class”
  from the live blocker list and leaves the final Einstein/Regge lift beyond
  the current bridge surface as the main remaining gravity target

New exact/bounded perturbative junction-stability result extracted after that:

- on the exact local `O_h` source class, the whole-shell bridge law is
  pointwise exact on each orbit
- on the broader exact finite-rank family, the non-`O_h` departure is a small
  within-orbit perturbation rather than a new shell law:
  - `u` and bridge-side `rho` spread below about `1.3905%`
  - `k` spread below about `1.6747%`
  - bridge-side `S` spread below about `2.6295%`
- after subtracting the orbit-mean base law, the first-order Taylor correction
  leaves only a second-order remainder:
  - relative residual in `rho` about `2.18e-5`
  - relative residual in `S` about `3.54e-5`
- see `docs/PERTURBATIVE_JUNCTION_STABILITY_NOTE.md`
- this means the broader finite-rank non-`O_h` family is a controlled
  perturbation of the exact `O_h` junction law, not a separate closure
  branch

New exact/bounded projected-correction result extracted after that:

- on the active sewing-band orbit quotient, the non-`O_h` correction is an
  exact projected DtN / Schur-complement operator built directly from the
  microscopic lattice solve
- the projected operator has exact pairwise antisymmetry between
  `(3,2,2) <-> (4,1,0)` and `(3,3,0) <-> (4,1,1)`, so the active correction
  factors through the two pair channels
- its leading output mode aligns with the universal active orbit pattern
  already extracted from the exact local `O_h` and finite-rank families
- see `docs/FINITE_RANK_DTN_CORRECTION_OPERATOR_NOTE.md`
- this removes “the correction is only a post hoc fit” from the live blocker
  list and narrows the remaining problem to the scalar amplitude on the active
  pair quotient and its promotion to the full 4D closure

New exact support-amplitude result extracted after that:

- on the current star-supported source class, the microscopic map from the
  renormalized support vector `q_eff = (I - W G_S)^-1 m` to the active shell
  correction is already rank one
- the exact support-to-active response operator factors as
  `A_active = m_active * 1^T`
  so the active non-`O_h` shell correction obeys
  `delta_sigma_active = Q_eff * m_active`
  with `Q_eff = 1^T q_eff`
- the same scalar-amplitude law holds on the reduced active pair quotient
- the exact local `O_h` and broader finite-rank source families satisfy that
  support-renormalized amplitude law exactly
- see `docs/SUPPORT_RENORMALIZED_ACTIVE_AMPLITUDE_NOTE.md`
- this removes “derive the scalar amplitude on the active pair quotient” from
  the live blocker list and leaves the final nonlinear 4D lift as the main
  remaining gravity problem on the current source class

## Do not retread these solved or near-solved substeps

The attack should **not** spend time redoing the following:

- weak-field Poisson / Newton derivation
- weak-field WEP or weak-field time dilation
- broad eikonal discussion as if that by itself gives strong-field closure
- old Schwarzschild-at-`r = R_S + l_P` arguments

Those are not the live blocker.

## Exact load-bearing blocker

The live blocker is:

> The repo does not yet derive a nonlinear **3+1 spacetime lift** tying the
> already-sharp spatial shell/junction law to the temporal sector and matter
> backreaction in one self-consistent strong-field equation.

Concretely, the current strong-field branch still relies on two load-bearing
extensions that are not yet theorem-grade:

1. the weak-field conformal spatial form `g_ij = (1 - phi)^2 delta_ij` is
   extended into the strong-field regime
2. the backreaction law used in the fixed-point solve is inserted as a
   self-consistency ansatz rather than derived from the exact lattice
   propagator / Hamiltonian

At the current Codex state, the live gravity gap is even narrower in practice:

3. the zero-monopole harmonic remainder must be shown to decouple under the
   shell/angular coarse-graining that defines the macroscopic exterior metric
4. the near-source region must be sewn to that monopole-dominated exterior in
   one common nonlinear 4D closure

After the DtN-kernel and orbit-channel results, this can be tightened
again:

3. shell-level coarse-graining is no longer the blocker for the current
   star-supported exact source classes
4. the reduced shell/exterior junction law itself is no longer the blocker on
   the current exact source class
5. the live blocker is now the full local lift across the whole sewing band
   and the derivation of the static isotropic bridge from the lattice closure
   itself
6. after that, the resulting exterior-plus-band construction still has to be
   promoted to a theorem-grade nonlinear **3+1** closure

More concretely now:

7. the spatial side is no longer the vague part of the problem:
   on the current star-supported source class, the shell kernel, reduced
   junction operator, anisotropic correction mode, and support-renormalized
   amplitude law are already solved natively on the **3D** lattice
8. the remaining theorem is therefore not “derive symmetric 4D gravity from
   scratch,” but:
   - identify the exact local **3D shell/junction functional**
   - prove its temporal / lapse lift
   - promote that pair to the final nonlinear **3+1** Einstein-Regge closure

Until those are replaced by a genuine nonlinear closure, the following stay
bounded or conditional:

- full strong-field metric
- no-horizon as a physics claim
- no-echo as a theorem-grade consequence
- any “full GR derived” wording

## Best derivation route already latent in the repo

The shortest credible route is **not** another phenomenology note. It is a
propagator-based **3D-to-3+1** metric reconstruction program:

1. start from the exact **spatial** lattice propagator / DtN / shell data in
   background field form, not from Schwarzschild
2. derive the strong-field **3D shell/junction law** from that propagator data
   without importing the continuum metric interpretation by hand
3. derive the strong-field **temporal** component from the same background,
   i.e. as a lift of the same solved spatial object rather than as an
   independent sector
4. combine them into a single **3+1** metric / junction candidate
5. compute Ricci / Einstein residuals or a Regge-lattice analog and test
   whether a closed nonlinear vacuum equation is actually satisfied

This route stays on the framework’s strongest native surface:

- path-sum action
- propagator-defined geometry
- self-consistency closure
- already-retained weak-field gravity

It also matches the actual structure of the current branch:

- all exact strong-field objects extracted so far are fundamentally **spatial**
  (`G_0`, shell source, DtN kernel, orbit channels, reduced junction operator,
  support-renormalized amplitude law)
- the temporal sector is a derived **lift** from those spatial objects
- so the final gravity theorem should be framed as:
  **exact 3D shell/junction closure -> exact 3+1 spacetime lift**

## Specific files to reuse

These are the strongest starting points already in the repo:

- `docs/GRAVITY_CLEAN_DERIVATION_NOTE.md`
- `docs/BROAD_GRAVITY_DERIVATION_NOTE.md`
- `docs/SPATIAL_METRIC_DERIVATION_NOTE.md`
- `docs/STRONG_FIELD_METRIC_NOTE.md`
- `docs/STRONG_FIELD_RESOLVENT_CLOSURE_NOTE.md`
- `docs/LATTICE_NO_HORIZON_NOTE.md`
- `scripts/frontier_broad_gravity.py`
- `scripts/frontier_strong_field_metric.py`
- `scripts/frontier_strong_field_resolvent_closure.py`
- `scripts/frontier_strong_field_extension.py`
- `scripts/frontier_lattice_no_horizon.py`

Use them as inputs. Do **not** assume their strongest status labels are already
paper-safe.

## Concrete attack sequence

### Attack 1: replace the strong-field self-consistency ansatz with a derived nonlinear equation

Current gap:

- the point-source fixed-point equation is elegant, but the backreaction law is
  not yet derived from the exact lattice propagator

Current status update:

- the rank-one local-source version of that enhancement law is now exact
- the same exact closure now extends to a finite-support diagonal attractive
  source class
- the same exact closure now extends again to a finite-rank correlated support
  operator
- the remaining issue is upgrading that exact source class to the actual
  physical matter source / strong-field Hamiltonian

Required outcome:

- derive the effective nonlinear source term directly from the Hamiltonian /
  resolvent / path-sum structure
- show that the strong-field fixed-point equation is not just a motivated ansatz

This is the highest-leverage step.

### Attack 2: derive the 3+1 lift from the already-solved spatial object

Current gap:

- the spatial shell/junction side is much sharper than the temporal side
- no full spacetime statement is possible until the temporal/lapse sector is
  proved to be the lift of that same spatial object

Current bridge result:

- on the static isotropic vacuum surface, `g_tt` is not an arbitrary extra
  function once the harmonic spatial data are fixed
- so the real unresolved issue is no longer “guess a lapse,” but “derive why
  the lattice strong-field closure reduces to this common harmonic system”
- the finite-support source theorem now provides one exact exterior harmonic
  object that both sectors can share, but the reduction to the static isotropic
  vacuum bridge is still a bounded step
- the new finite-rank residual test sharpens that further:
  the direct common-source candidate is not yet vacuum-closed, while the
  monopole/isotropic projection of the same exact field is nearly vacuum
- the new cubic-monopole reduction result sharpens it again:
  for the exact `O_h`-symmetric source class, the isotropic reduction is
  asymptotically justified and the first anisotropic correction is controlled
- the new exact local-source-class scan sharpens it once more:
  even the full exact local `O_h` family does not close the direct metric,
  so the remaining gap is not source-family freedom by itself
- the new same-source ansatz scan sharpens it again:
  small nonlinear same-source metric deformations do not remove the residual,
  so the remaining gap is not just the linear closure choice
- the new coarse-grained exterior-law result sharpens it again:
  after harmonic coarse-graining, the exterior law is already vacuum-close, so
  the live blocker is the matching from the exact lattice field to that
  coarse-grained exterior representative
- the new matching-window result sharpens it once more:
  the matching is not infinitely vague; it appears in a finite radial band
  around `R ~ 4 - 4.5`, so the theorem target is now the mechanism for that
  crossover
- the new sewing-shell source result sharpens it again:
  the sewing shell is no longer only a bounded blend region; for the current
  exact source families it is represented exactly by a lattice shell source
  `sigma_R = H_0 (Pi_R^ext phi)` supported in the same finite band
  `3 < r <= 5`
  - see `docs/SEWING_SHELL_SOURCE_THEOREM_NOTE.md`
  - this removes “does an exact sewing shell exist?” as the blocker and
    replaces it with the narrower problem of interpreting that exact shell
    source as the effective stress / matching law of the 4D closure
- the new radial-shell result sharpens it once more:
  the exact shell source already collapses strongly onto a purely radial shell
  law carrying the full total charge, with a zero-monopole anisotropic
  remainder
  - see `docs/RADIAL_SHELL_MATCHING_LAW_NOTE.md`
  - this reduces the remaining target further: derive the radial shell profile
    and control the anisotropic remainder, rather than derive an arbitrary
    shell law from scratch
- the new universal-shell-profile result sharpens it again:
  for the current exact source families, the normalized radial shell profile
  is identical to machine precision
  - see `docs/UNIVERSAL_SHELL_PROFILE_NOTE.md`
  - this removes family-dependence of the radial shell law as a blocker and
    leaves the real target as the microscopic derivation and effective-stress
    interpretation of one universal shell kernel

Required outcome:

- derive the temporal redshift factor from the exact same spatial shell /
  junction closure that now drives the strong-field exterior law, in a way
  stronger than the current bounded static-isotropic bridge
- remove the current mismatch where the exact **3D** branch is stronger than
  the temporal / 3+1 lift
- derive the microscopic-to-macroscopic matching rule that sends the exact
  lattice field to the coarse-grained radial harmonic exterior law
- or derive the effective source/coarse-graining theorem that forces that
  projection from the lattice dynamics itself
- more sharply now:
  derive the continuum / effective-stress meaning of the exact shell source
  `sigma_R` and show that it generates the correct nonlinear sewing law
- more sharply still:
  derive the radial shell profile from the microscopic lattice dynamics and
  show the zero-monopole shell anisotropy is a controlled subleading stress
- more sharply still:
  derive the universal shell kernel itself from the microscopic lattice
  dynamics and promote it to the shell stress / matching law of the nonlinear
  closure
- and, before the full 3+1 lift, derive the perturbative correction operator
  that controls the finite-rank non-`O_h` junction deviation with a bounded
  `O(\epsilon^2)` remainder

New exact/bounded local shell-to-`3+1` lift extracted after that:

- on the current bridge surface, the exact shell source `sigma_R = H_0 phi_ext`
  and the unique same-charge bridge
  `psi = 1 + phi_ext`, `chi = 1 - phi_ext = alpha psi`
  admit an exact local static conformal constraint lift
- the pointwise shell density and stress-trace are fixed by
  `rho = sigma_R / (2 pi psi^5)` and
  `S = 0.5 rho (1/alpha - 1)`, and satisfy
  `H_0 psi = 2 pi psi^5 rho`,
  `H_0 chi = -2 pi alpha psi^5 (rho + 2S)` identically
- on the exact local `O_h` source class, this lift is pointwise exact at orbit
  resolution across the whole sewing band `3 < r <= 5`
- see `docs/OH_STATIC_CONSTRAINT_LIFT_NOTE.md`
- this removes the shell-to-`3+1` lift itself from the live blocker list on
  the current bridge surface

New exact/bounded microscopic shell-action result extracted after that:

- on the exterior domain with inner trace `Gamma_R`, the shell boundary energy
  is the exact Schur complement of the lattice Laplacian
- its gradient equals the microscopic shell trace flux exactly
- on both the exact local `O_h` class and the broader finite-rank class, the
  exact shell trace is the stationary point of the same microscopic sourced
  boundary action
- see `docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md`
- this removes the microscopic shell-action gap on the current source classes

New exact/bounded microscopic Dirichlet-principle result extracted after that:

- the sourced Schur boundary action is strictly convex on the current bridge
  surface
- the exact shell trace is the unique global minimizer of that microscopic
  boundary energy
- the native same-charge bridge is therefore the unique minimum-energy
  discrete Dirichlet extension of the exact shell data on the current
  star-supported class
- see `docs/MICROSCOPIC_DIRICHLET_BRIDGE_PRINCIPLE_NOTE.md`
- this removes the last "ansatz vs principle" ambiguity on the current bridge
  surface

## Current promotable gravity statement

At this point the branch supports a real **restricted strong-field closure**
statement:

- on the exact local `O_h` star-supported source class, the framework has
  exact shell source, exact same-charge bridge, exact local shell-to-`3+1`
  static conformal lift, exact microscopic Schur boundary action, and exact
  minimum-energy discrete Dirichlet bridge principle
- on the broader finite-rank family, the same closure package persists with
  only the already-controlled small within-orbit deformation

See `docs/RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md`.

New exact/bounded source-class extension extracted after that:

- on the current bridge surface, the exact shell source, same-charge bridge,
  local static conformal constraints, and microscopic Schur boundary action do
  not depend on the benchmark `O_h` family alone
- they extend exactly to the full star-supported finite-rank source class
- see `docs/STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md`
- this removes source-class dependence within the current star-supported
  finite-rank sector from the live blocker list

New exact/bounded support-class widening extracted after that:

- the same exact Schur boundary action and static conformal lift are not
  confined to the star-supported benchmark geometry
- on generic finite-support positive-semidefinite source operators inside the
  same Dirichlet box, the exact finite-rank resolvent field still feeds the
  same shell source, same-charge bridge, local static conformal constraints,
  and microscopic boundary action
- see `docs/GENERIC_FINITE_SUPPORT_SCHUR_BRIDGE_NOTE.md`
- this removes the remaining star-specific geometry objection from the live
  blocker list

New exact/bounded local-bridge uniqueness extracted after that:

- on the current star-supported finite-rank class, any local scalar bridge
  channel that remains exterior harmonic on the exact shell exterior must be
  affine in `phi_ext`
- same-charge inheritance and the attractive temporal branch then fix the
  native bridge `psi = 1 + phi_ext`, `chi = 1 - phi_ext`
- see `docs/LOCAL_BRIDGE_UNIQUENESS_NOTE.md`
- this removes local scalar bridge reparameterization freedom from the live
  blocker list on the current class

New exact/bounded generic-support bridge-uniqueness extension extracted after
that:

- on the broader generic finite-support bridge class, the affine bridge channel
  still remains exactly exterior harmonic, while quadratic local scalar
  deformations immediately fail both bulk harmonicity and the discrete
  mean-value / Jensen test on realized exterior neighbor data
- see `docs/GENERIC_LOCAL_BRIDGE_UNIQUENESS_NOTE.md`
- this removes the most obvious “hidden nonlinear local scalar bridge” escape
  hatch from the broader finite-support class as well

New bounded full-generality obstruction extracted after that:

- the branch now has a credible route to a coarse-grained scalar exterior law
  with sharply reduced residuals on the exact local `O_h` and finite-rank
  source families, but this does **not** close full nonlinear GR
- the remaining missing principle is now localized as a tensorial matching /
  completion theorem from the microscopic source data to the full 4D metric,
  including non-spherical and time-dependent sectors
- see `docs/FULL_GENERALITY_NONLINEAR_GR_NOTE.md`
- this means the remaining gap is not “slightly better shell fitting”; it is
  the absence of a theorem deriving the full lapse-shift-spatial metric from
  the current scalar/static bridge machinery

New exact/bounded bridge-variational result extracted after that:

- the exact microscopic Schur boundary action admits a strict positive-definite
  completion of the square around the native bridge trace
- for both the exact local `O_h` family and the broader finite-rank family,
  random shell-trace perturbations raise the exact boundary action by a
  strictly positive amount
- see `docs/MICROSCOPIC_DIRICHLET_BRIDGE_PRINCIPLE_NOTE.md`
- this turns the current bridge from a well-motivated static conformal ansatz
  into the unique minimum-energy discrete Dirichlet extension on the current
  source classes

New bounded first-tensor correction extracted after that:

- the universal zero-monopole DtN anisotropic shell mode is a real first
  tensor correction to the scalar bridge
- promoted as the minimal traceless spatial shear, it lowers the 4D Einstein
  residual on both the exact local `O_h` and broader finite-rank classes, but
  does not close the gap
- see `docs/TENSORIAL_BRIDGE_PRINCIPLE_NOTE.md`
- this means the remaining freedom is not “no tensor correction exists”; it is
  that the first tensor correction is insufficient

New sharp tensorial-completion obstruction extracted after that:

- keeping the exact scalar bridge fixed while turning on explicit shift and
  traceless spatial tensor perturbations leaves the scalar Schur boundary
  action unchanged but generates independent `G_{0i}` and traceless
  `G_{ij}` residual channels
- see `docs/TENSORIAL_EINSTEIN_REGGE_COMPLETION_NOTE.md`
- this localizes the remaining gap: the current restricted `3+1` lift is
  scalar-complete on the bridge surface, but it is not a full tensorial
  completion theorem

New exact/bounded scalar-completion no-go extracted after that:

- the current microscopic boundary functional depends only on the scalar shell
  trace / Schur data
- explicit vector, traceless-shear, and mixed perturbations keep that scalar
  data fixed while producing different tensorial Einstein channels
- see `docs/SCALAR_TRACE_TENSOR_NO_GO_NOTE.md`
- therefore no completion principle factoring only through the current scalar
  shell trace / Schur data can determine the full `3+1` metric on this branch
- this removes the last scalar-only escape hatch and forces any positive next
  step to be a genuinely tensor-valued matching law

New exact/bounded tensor-matching localization extracted after that:

- on the retained restricted family, the missing tensor completion is now
  localized to the smallest non-scalar shell data compatible with the current
  probes:
  - one shift-like tensor boundary coordinate
  - one traceless-shear boundary coordinate
- see `docs/TENSOR_MATCHING_COMPLETION_THEOREM_NOTE.md`
- on the current audited family, the mixed probe is locally additive in those
  two channels, so they are not just necessary; they are also the smallest
  locally sufficient tensor extension currently visible on the branch
- this means the only honest positive route left is to derive:
  - the microscopic source-to-tensor-channel map `eta`
  - the symmetric positive-definite tensor boundary kernel `K_tensor`
- see `docs/TENSOR_COMPLETION_NO_GO_OR_EXTENSION_NOTE.md`

New exact/bounded universal-kernel obstruction and selector-normalized
narrowing extracted after that:

- the raw family-universal positive `K_tensor` theorem fails on the current
  audited restricted class
- see `docs/TENSOR_UNIVERSAL_KERNEL_OBSTRUCTION_NOTE.md`
- but that failure is no longer structureless:
  - after normalizing by the dominant traceless-shear response `eta_11`, the
    tensor-kernel shape mismatch drops from `2.62e-01` to `4.26e-02`
  - the normalized source-map mismatch drops to `4.55e-02`
  - the scalar-derived tensor-drive coefficient
    `c_eta = eta_floor_tf / |I_scalar|` differs by only `7.18e-02`
  - one common selector-normalized candidate predicts both families within
    about `5% - 7%`
- see `docs/TENSOR_SELECTOR_NORMALIZED_KERNEL_NOTE.md`
- this means the missing gravity principle is now best understood as:
  - a selector / coarse-graining / microscopic source law that fixes the
    normalization of the tensor channels
  - not a wholly different tensor-kernel shape on each family

### Attack 3: only after metric closure, revisit horizon / echo claims

Current gap:

- no-horizon is still conditional on the strong-field metric
- no-echo is separately weaker still

Required outcome:

- once the metric is fixed, re-evaluate horizon formation
- treat echo phenomenology as a downstream consequence, not the place where the
  gravity theorem is decided

## What not to overclaim

Even if the next step lands, keep these distinctions explicit:

- broad weak-field GR signatures are not the same as full nonlinear GR
- a bounded hard floor / no-singularity statement is not the same as no horizon
- no-horizon is not the same as no-echo

## Research success criteria

This lane is worth promoting only if all of the following hold:

1. the nonlinear closure is derived from the exact lattice framework, not
   inserted as a closure ansatz
2. the exact **3D** shell/junction law is derived natively from the lattice
   and not merely extracted as a fitted or bounded effective law
3. `g_tt` and `g_ij` come from the same strong-field derivation, i.e. one
   common **3+1** lift of that 3D shell/junction law
4. the resulting metric satisfies a real nonlinear field equation or Regge
   analog with controlled residuals
5. downstream no-horizon / strong-field claims are reclassified against that
   derived metric, not inherited from older notes

## Practical conclusion

The gravity upside is still real, but the branch should stop acting as if the
main task is “derive more GR signatures” or “derive symmetric 4D lattice
gravity.” The actual task is:

> derive one exact **3D shell/junction theorem** and its nonlinear **3+1**
> spacetime lift, replacing the remaining strong-field ansatzes with a genuine
> lattice theorem.

With the latest support-class widening, that theorem is now best phrased for
generic finite-support sources on the current box rather than only the
star-supported benchmark geometry. The remaining freedom is now best understood
as genuinely beyond the current static conformal local-scalar bridge class and
ultimately as a missing tensorial completion principle for full 4D gravity.
