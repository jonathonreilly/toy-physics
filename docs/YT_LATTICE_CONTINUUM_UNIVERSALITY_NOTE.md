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

## Status of the universality argument on this specific surface

The Schur-bridge stack was constructed BEFORE the Ward identity at M_Pl
had a clean independent derivation. In that historical context, the
backward-Ward / Schur-coarse-bridge construction was the framework's
attempt to provide a retained transport theorem directly, with explicit
endpoint-budget control.

Now that the Ward branch closes the boundary-condition derivation, the
question is whether the standard universality argument above can be
appealed to for the v → M_Pl transport instead of carrying a framework-
native transport theorem.

**Honest characterization.** The argument that the framework's specific
canonical surface satisfies the standard universality premises (table
above) is a **proposal asking the reviewer to accept by analogy**, not
a framework-internal continuum-limit theorem proved on this surface.

What is actually shown in this note:

- ✓ The standard Wilsonian-universality result is textbook material for
  asymptotically free lattice gauge theories.
- ✓ The framework's specific surface satisfies the listed standard
  premises (asymptotic freedom, fixed regulator, Wilsonian-block
  compatibility, etc.).
- ✗ The application to this specific composite-Higgs surface is NOT
  proved here; it is an appeal to the general universality result.
- ✗ No framework-internal continuum-limit theorem on the canonical
  Wilson-staggered surface at β = 6 with composite-Higgs D9 is provided
  by this note.

**What this means for the proposal.** The case for P2 is therefore that
the standard universality argument applies to this surface BY ANALOGY
WITH STANDARD LATTICE QCD, not because a framework-internal
continuum-limit theorem has been proved.

If the reviewer accepts this — i.e., accepts the standard universality
argument as background methodology for any reasonable asymptotically-
free lattice gauge theory satisfying the listed premises — then P2
holds and the supersession proposal proceeds.

If the reviewer requires a framework-internal continuum-limit theorem
on this specific surface (e.g., a Symanzik-improvement-style explicit
analysis on the composite-Higgs Wilson-staggered surface), then this
note does NOT provide that, the methodological gap is NOT discharged
on this branch, and the supersession case stalls pending that work.

The Schur-bridge stack remains a perfectly valid INDEPENDENT derivation
that reaches `y_t(v)` through different machinery, regardless of which
way the reviewer rules on P2. Its 0.71% local + 0.50% nonlocal
residuals stay valid as bridge-path residuals; the question is only
whether they remain the package's load-bearing systematic.

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

## Bottom line (honest)

If the reviewer accepts P2 as a standard-methodology appeal:

> The continuum limit of the framework's canonical Wilson-staggered
> surface at `β = 6` with composite-Higgs D9 is described, at scales
> `v ≪ M_Pl`, by the standard SM continuum action with matched
> renormalized couplings — by appeal to the standard Wilsonian
> universality result for asymptotically free lattice gauge theories
> satisfying the listed premises. The application to this specific
> composite-Higgs surface is by analogy with standard lattice QCD,
> not from a framework-internal continuum-limit theorem proved here.
> Residual uncertainties on the Ward primary path are quantified in
> the companion budget note as ~1.95% (1-loop matching + RGE),
> numerically comparable to the legacy bridge budget.

This is the methodological move the proposal asks the reviewer to
make. It retires the framework-native explicit-systematic wording in
favor of standard SM perturbative-residual wording. It does NOT claim
a tighter quantitative budget (the companion note shows the budget is
comparable, not smaller). It does NOT prove a framework-internal
continuum-limit theorem on this surface.

If the reviewer rejects this appeal — i.e., requires that the
framework prove its own continuum-limit theorem before any standard
universality argument can be cited for this surface — then the
proposal fails on P2 and the existing wording stays. That is a
legitimate reviewer position and the proposal does not attempt to
preempt it.
