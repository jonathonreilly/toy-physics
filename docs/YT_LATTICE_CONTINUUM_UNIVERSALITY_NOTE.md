# Lattice → Continuum Universality on the Canonical Wilson-Staggered Surface

**Date:** 2026-04-17
**Status:** SUPPORT NOTE for `YT_WARD_SUPERSEDES_BRIDGE_PROPOSAL_2026-04-17.md`
**Scope:** justify treating SM RGE as the correct continuum-limit
description (NOT a "perturbative surrogate") of the framework's lattice
running between scales `v ≪ M_Pl`.

This note carries no authority status of its own. It is the supporting
methodological argument for **P2** of the supersedes-bridge proposal.

---

## What this note settles

The legacy authority note `YT_FLAGSHIP_BOUNDARY_NOTE.md:57-59` describes
SM RGE as

> "the perturbative surrogate for the true lattice blocking flow over the
> full v → M_Pl interval"

That phrasing carries an implicit framework-native systematic. The ~1.21%
Schur-coarse-bridge endpoint budget is the bound on the gap between SM
RGE and "the true lattice blocking flow."

This note argues that SM RGE is not a SURROGATE for an unknown true
flow; rather, by standard Wilsonian universality applied to the
framework's specific surface, **SM RGE IS the correct continuum-limit
description** of the lattice flow at scales much below the cutoff.

If accepted, this changes the methodological status (not the equations).
The SM RGE running step in the y_t lane stops carrying a framework-
native systematic, and the lane uncertainty reduces to standard SM
(NNLO truncation) + standard lattice-QCD (`O(α_LM · a²)`) residuals
both quantified in the companion note
`YT_WARD_PATH_UNCERTAINTY_BUDGET_NOTE.md`.

---

## The standard universality result (textbook material)

For an asymptotically-free SU(N_c) gauge theory regulated on a Wilson
or Wilson-staggered lattice, with bare coupling `g_bare(a)` running
toward zero as `a → 0` according to the asymptotic-freedom relation,
the LOW-ENERGY physics — at scales `μ` such that `μ · a → 0` in the
continuum limit — is described by:

1. The standard continuum action of the gauge theory in the same gauge
   group, fermion content, and matter representations.
2. Continuum running of the gauge coupling and other physical couplings
   via the standard continuum β-functions.
3. Lattice-discretization corrections of `O(α_lattice · (μ · a)²)` (for
   tadpole-improved Wilson) or `O((μ · a)²)` (standard Wilson), all
   vanishing as `μ · a → 0`.

This is **standard lattice-QCD textbook material** (e.g., Lepage
1993, Symanzik improvement program, Wilsonian renormalization group
on a lattice). It applies to ANY lattice gauge theory satisfying:

- asymptotically free gauge sector
- fixed regulator (single lattice spacing)
- Wilsonian-block compatibility (renormalization group makes sense)

Below the cutoff `1/a = M_Pl`, the lattice theory is described by the
continuum theory with matched bare → renormalized couplings.

---

## How the framework's specific surface satisfies these premises

The framework's canonical Wilson-staggered lattice at `β = 2 N_c / g_bare² = 6`:

| Premise | Framework's surface |
|---|---|
| Asymptotically free SU(N_c) | YES: SU(3)_c is asymptotically free in the framework's matter content (LEFT_HANDED_CHARGE_MATCHING + retained generation count) |
| Fixed single regulator | YES: canonical surface specifies `β = 6` as the fixed package evaluation point (`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`, recently re-emphasized on main) |
| Wilsonian-block compatibility | YES: tadpole-improved Lepage-Mackenzie surface with `α_LM = 0.0907 ≪ 1` is in the perturbative regime where Wilsonian RG is well-defined (cf. Block 9 of `frontier_yt_ward_identity_derivation.py`: `n_opt = π/α_LM ≈ 35` loops to optimal truncation) |
| Composite-Higgs D9 | YES: composite-Higgs structure (no fundamental scalar in the bare action) is consistent with a Wilsonian RG flow that matches onto the SM EFT below the cutoff via the operator-decomposition done in the Ward derivation Steps 3A-3D |
| Matter content matches SM at low energy | YES: derived in `LEFT_HANDED_CHARGE_MATCHING_NOTE.md` (Q_L = (2,3) block, etc.); composite-Higgs gives the SM Higgs doublet at the EWSB scale |

No premise of the standard universality argument is violated by the
framework's specific surface.

---

## Why the legacy "surrogate" framing was conservative, not load-bearing

The Schur-bridge stack was constructed BEFORE the Ward identity at M_Pl
had a clean independent derivation (i.e., before the Ward branch). At
that time, the scalar-singlet boundary condition `y_t/g_s = 1/√6` was
quoted as a "Cl(3) trace identity" without an operator-side derivation
matching the OGE-side Feynman-rule computation.

In that historical context, the cautious move was to treat the entire
`v → M_Pl` flow as needing an independently retained transport theorem,
because the boundary condition itself was structurally weaker. The
backward-Ward / Schur-coarse-bridge construction was the framework's
attempt to provide that transport theorem directly, with explicit
endpoint-budget control.

Now that the Ward branch closes the boundary-condition derivation
(operator-side via H_unit matrix element + OGE-side via D12 + S2,
verified consistent in Block 11 of the Ward runner), the historical
need for a framework-native transport theorem has been discharged.
The "true lattice blocking flow" between `v` and `M_Pl` reduces to
standard continuum SM RGE at scales below the cutoff, by the standard
universality argument above.

The Schur-bridge stack remains a perfectly valid INDEPENDENT derivation
that reaches the same `y_t(v)` value through different machinery; its
0.71% local + 0.50% nonlocal residuals are now the cross-check budget,
not the load-bearing systematic on the package.

---

## What the reviewer is asked to evaluate

For the universality argument to be accepted (P2 of the proposal):

1. The standard lattice-QCD universality result for asymptotically free
   gauge theories at scales much below the cutoff is well-established
   textbook material; the reviewer should accept it on those grounds.
2. The framework's specific surface satisfies the standard premises (table
   above). The reviewer should evaluate this case-by-case if any premise
   is contested.
3. No framework-specific obstruction has been identified. If the
   reviewer believes a framework-specific obstruction exists, the
   proposal asks them to name it explicitly so it can be addressed.

The argument does not require any new theorem proved here. It only
requires accepting that standard universality applies to the framework's
specific surface.

---

## Honest limitations

- **Not a new theorem.** This note appeals to standard lattice-QCD
  universality, not to a framework-internal continuum-limit theorem.
  A reviewer who insists on a fully framework-internal derivation of
  the universality argument would need that work done separately.
- **Composite-Higgs D9 + universality.** The standard universality
  argument is best-established for elementary-Higgs SM (or pure gauge
  + matter). Extending it to composite-Higgs frameworks is standard
  in the technicolor / NJL / BHL literature, but the reviewer may
  want the framework's specific composite-Higgs structure cross-checked
  against a published universality argument for composite-Higgs lattice
  models. The composite-Higgs literature (e.g., Bardeen-Hill-Lindner
  Phys. Rev. D 41, 1647 (1990)) supports this extension.
- **`O(α_LM · a²)` lattice-discretization.** Estimated from standard
  power counting; not separately measured on this surface. Sub-percent
  on standard lattice-QCD experience, but the reviewer may want this
  measured directly for the framework's surface (sweep of `β` values
  or comparable lattice-spacing variation).

---

## Bottom line

If P2 is accepted:

> The continuum limit of the framework's canonical Wilson-staggered
> surface at `β = 6` with composite-Higgs D9 is described, at scales
> `v ≪ M_Pl`, by the standard SM continuum action with matched
> renormalized couplings. SM RGE running between any two such scales
> is the correct continuum description (not a surrogate). Residual
> uncertainties are standard SM-RGE truncation + standard lattice-
> discretization corrections, both quantified in the companion budget
> note as sub-percent.

This is the methodological move that retires the legacy 1.21% bridge
budget as the load-bearing systematic on the package primary path.
