# Inputs And Qualifiers

**Date:** 2026-04-15
**Purpose:** one canonical public note for the explicit inputs, derived
constants, bridge-conditioned rows, bounded rows, and live gates on the
current paper surface.

This note is the shortest package-level answer to:

> what is actually taken as input, what is same-surface derived, and what
> still depends on bridge layers or open gates?

## 1. Framework statement

The accepted package statement is:

> We take `Cl(3)` on `Z^3` as the physical theory.

The operational memo
[MINIMAL_AXIOMS_2026-04-11.md](../../MINIMAL_AXIOMS_2026-04-11.md)
records the accepted implementation boundary used to audit the current package.

The one-axiom notes

- [SINGLE_AXIOM_INFORMATION_NOTE.md](../../SINGLE_AXIOM_INFORMATION_NOTE.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](../../SINGLE_AXIOM_HILBERT_NOTE.md)

are optional reduction/support context for framework compression and
physical-lattice scoping. They are not the load-bearing input ledger for the
current paper surface.

## 2. Explicit external inputs on the current paper surface

Current cosmology-facing rows are conditioned on:

- `T_CMB = 2.7255 K`
- `H_0 = 67.4 km/s/Mpc`

These are not inputs to the retained structural core. They are explicit
boundary data for the bounded cosmology lane. The FRW kinematic reduction
adds no new point input; `q_0`, `z_*`, `z_{mLambda}`, and asymptotic `H_inf`
remain functions of the same open `H_inf/H_0` ratio, with listed cosmology
numbers used only as comparators.

The matter-radiation equality identity adds no new native density derivation:
`1 + z_mr = Omega_m,0/Omega_r,0` is exact on the admitted FRW/EOS surface, but
the readout `z_mr ~= 3423` uses supplied `Omega_m,0` and observational
`Omega_r,0` from `T_CMB` plus relativistic-species bookkeeping.

The `N_eff` support theorem connects the retained three-generation matter
content to the active-neutrino count `N_active = 3`. The public value
`N_eff = 3.046` still includes the standard external `0.046` thermal-history
correction and uses observational photon-temperature data when converted into
`Omega_r,0`.

The dark-matter/cosmology cascade also uses the exact support identity
`R_base = 31/9`, which depends on the admitted Georgi-Glashow/GUT
normalization factor `3/5`. That identity is now packaged separately, but it
does not derive the Sommerfeld correction, the full `Omega_DM/Omega_b` value,
or the downstream `Omega_Lambda` numerics.

The charged-lepton bounded package is additionally conditioned on
an explicit three-real observational pin:

- PDG charged-lepton masses `(m_e, m_μ, m_τ)`

Those are not inputs to the retained structural core either. They are the
explicit observational pin behind the charged-lepton bounded row.

## 3. Same-surface derived constants used across the package

These are not experimental fit parameters or hidden free knobs. They are the
current canonical same-surface evaluated constants on `main`.

Current absolute-scale package rule:

- on the accepted physical-lattice reading, the package currently carries
  `a^(-1) = M_Pl` as an explicit Planck-scale pin
- that pin is not yet derived from the minimal accepted theorem stack
- the 2026-04-24 conditional-completion packet derives `c_cell = 1/4` and
  the unique additive finite-boundary density extension, then gives
  `a/l_P = 1` after the primitive boundary count is accepted as the
  gravitational boundary/action carrier; that carrier identification is still
  the explicit Planck-lane condition
- the finite-automorphism-only response route is closed negatively; finite
  primitive-cell automorphisms have no infinitesimal metric/coframe response
  tangent and cannot replace the realified response surface
- the carrier-only parent-source scalar route is closed negatively; carrier
  data alone leave an affine hidden character `delta`, so scalar equality
  requires a separate no-hidden-character law
- authority:
  [PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md](../../PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md),
  [PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md](../../PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md),
  [PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md](../../PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md),
  [PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md](../../PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md),
  [PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md](../../PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md)

- plaquette surface:
  - `<P> = 0.5934`
  - authority:
    [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](../../PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
- mean link:
  - `u_0 = <P>^(1/4)`
- strong-coupling chain:
  - `alpha_LM`
  - `alpha_s(v)`
  - authority:
    [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md)
- electroweak hierarchy:
  - `v = 246.282818290129 GeV`
  - authority:
    [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- color normalization support:
  - `R_conn = 8/9 + O(1/N_c^4)`
  - authority:
    [RCONN_DERIVED_NOTE.md](../../RCONN_DERIVED_NOTE.md)

## 4. Chosen-target qualifiers

The gravity/QG chain is exact on:

- the discrete project route;
- one chosen canonical textbook continuum target.

It is not currently claimed as a theorem about every possible continuum
packaging. Use:

- [CONTINUUM_IDENTIFICATION_NOTE.md](../../CONTINUUM_IDENTIFICATION_NOTE.md)

## 5. Bridge-conditioned rows

These rows are still on the paper surface, but their interpretation uses a
bridge layer beyond the exact structural core.

- `alpha_s(M_Z)` and the `M_Z` EW rows:
  - same-surface derived framework values plus the retained running bridge
- bounded string tension readout:
  - exact confinement theorem plus low-energy EFT bridge
- CKM-only neutron-EDM corollary + bounded continuation:
  - retained strong-CP closure package + promoted CKM package
  - exact corollary `d_n(QCD) = 0` on the retained surface; EFT bridge only
    for the bounded `d_n(CKM)` number
- universal theta-induced EDM response:
  - retained strong-CP closure package + source-decomposition bookkeeping
  - exact corollary for theta-sourced EDM components only; independent CKM,
    qCEDM, Weinberg, CP-odd four-fermion, and BSM source directions are not
    set to zero by this theorem
- down-type CKM-dual mass ratios:
  - promoted CKM atlas/axiom package + GST + bounded `5/6` mass-ratio bridge; no observed
    masses as derivation inputs
  - current live comparison surface:
    threshold-local self-scale comparator `m_s(2 GeV)/m_b(m_b)`
  - theorem-grade closure of the exact `5/6` bridge and exact scale-selection
    rule remains open
- proton lifetime:
  - exact operator content + imported dimension-6 EFT decay-rate bridge
- cosmology windows:
  - fixed-gap vacuum/topology route plus the still-open matter bridge
  - FRW kinematic identities are structural support only until that bridge
    fixes `H_inf/H_0`

## 6. Bounded rows

These are already publication-captured, but not promoted to the retained
theorem core.

- charged-lepton bounded observational-pin package
  (explicit three-real PDG pin; no spare forecast beyond the pin)
- retained YT/top transport lane
- derived Higgs/vacuum lane with retention-decomposed budget
- cosmology lanes
- bounded secondary prediction surface:
  - proton lifetime
  - down-type CKM-dual mass ratios
  - neutrino absolute-mass observable bounds
  - vacuum critical stability
  - taste-scalar near-degeneracy
  - benchmark gravitational decoherence
  - monopole mass
  - Bekenstein-Hawking entropy comparison
- dual-status corollary surface:
  - CKM-only neutron EDM with bounded `d_n(CKM)` continuation
  - universal theta-induced EDM response vanishing, with no new bounded
    numerical EDM estimate and no independent CP-odd EFT operator-zero claim

## 7. Remaining bridge package

The remaining flagship bridge package is:

- charged-lepton Koide support package
  - April 24 native dimensionless review/no-go packet sharpens but does not
    close the lane; physical background-zero / `Z`-erasure, selected-line
    local boundary source, and based endpoint remain theorem targets

That is the current missing flagship prediction bridge. It does not erase the
rest of the retained or bounded prediction surface.

## 8. Reading rule

When someone asks “is this exact, derived, bounded, or bridge-conditioned?”
the answer should come from this note together with:

- [CLAIMS_TABLE.md](./CLAIMS_TABLE.md)
- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [PREDICTION_SURFACE_2026-04-15.md](./PREDICTION_SURFACE_2026-04-15.md)
