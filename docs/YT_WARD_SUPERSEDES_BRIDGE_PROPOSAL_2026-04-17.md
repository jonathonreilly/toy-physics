# Science Proposal: Ward-Identity Path Supersedes Schur-Bridge Path on the y_t Lane

**Date:** 2026-04-17
**Status:** PROPOSAL — REVIEWER DECISION REQUESTED
**Author:** Claude (drafting agent)
**Scope:** authority-status realignment on the y_t / m_t lane
**No status changes have been made by this proposal.**
**Authority notes (`YT_FLAGSHIP_BOUNDARY_NOTE.md` etc.) remain at their
current published status until reviewer agreement is recorded.**

**Supporting material (companion notes on this branch, no authority
status of their own):**
- [`YT_WARD_PATH_UNCERTAINTY_BUDGET_NOTE.md`](./YT_WARD_PATH_UNCERTAINTY_BUDGET_NOTE.md) — quantitative budget for `δ y_t(v)` on the Ward primary path. **Honest result: the Ward-path budget at current 1-loop work is ~1.95%, numerically comparable to the legacy 1.21% bridge budget, NOT materially tighter.** The supersession case rests on methodological character of the residual, not on a numerical reduction.
- [`YT_LATTICE_CONTINUUM_UNIVERSALITY_NOTE.md`](./YT_LATTICE_CONTINUUM_UNIVERSALITY_NOTE.md) — methodological argument that SM RGE is the correct continuum-limit description by appeal to standard Wilsonian universality. **Honest characterization: this is an appeal-by-analogy to standard lattice QCD, NOT a framework-internal continuum-limit theorem proved on the framework's specific composite-Higgs surface.**

---

## What this proposal asks the reviewer to decide

Whether the Ward-identity derivation
(`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, landed on main) should
replace the Schur-coarse-bridge stack as the **primary derivation
path** for `y_t(v)` on the framework's y_t / m_t lane.

If yes, then the package status line for `y_t(v)` and `m_t(pole)` could
move from

> **DERIVED with explicit systematic** (1.21% conservative / 0.755%
> support-tight transport budget from the Schur-coarse-bridge endpoint
> shift)

to

> **DERIVED**, with the residual uncertainty (~1.95% at current 1-loop
> work) carried as standard SM-RGE truncation + standard lattice 1-loop
> matching, both standard published methodologies. No framework-native
> explicit-systematic qualifier.

The proposal does NOT ask the reviewer to accept any new theorem
beyond what is already on the Ward branch. It asks only for a
**methodological realignment**: replace a framework-native
explicit-systematic budget with a comparable-magnitude budget of
standard-method type.

**The proposal does NOT claim a tighter quantitative budget on the
primary path.** At current 1-loop work, the Ward-path budget is
numerically comparable to the legacy bridge budget. The
supersession case rests on the methodological character of the
residual, not on a numerical reduction. A tighter Ward-path budget
would require NNLO lattice matching, which is out of scope.

---

## What the explicit-systematic qualifier currently covers

The current authority note `YT_FLAGSHIP_BOUNDARY_NOTE.md` says the
y_t lane carries an explicit transport systematic of `1.2147511%`
conservative or `0.75500635%` support-tight. The two named pieces
of this budget are:

| Piece | Value | Source | Origin |
|---|---|---|---|
| higher-order local tail | `0.71%` | `YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md` | `\|cubic + quartic\|/quadratic` from the local-Hessian selector's 4th-order Taylor fit on the 10% amplitude probe tube |
| nonlocal tail (conservative) | `0.50%` | `YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md` | `‖K_nonloc‖₂ / ‖K‖₂` operator-norm deviation of the kernel from the affine local-Hessian model on the forced UV window |
| nonlocal tail (support-tight) | `0.043%` | same | integrated against the support-tight viable bridge family average |

Both pieces are **structural residuals of the Schur-coarse-bridge path**
that constructs `y_t(v)` by transferring the lattice Ward boundary
through a backward-Ward / blocking-flow surrogate. Neither is intrinsic
to the physics of the top Yukawa.

The legacy authority note explicitly characterizes the SM RGE as
"the perturbative surrogate for the true lattice blocking flow"
(`YT_FLAGSHIP_BOUNDARY_NOTE.md:57-59`). That phrasing is what
justifies carrying an explicit framework-native systematic.

---

## What the Ward-identity branch establishes

The Ward branch (`claude/ward-identity-derivation`, HEAD `27354ce8`,
review-passed) establishes:

```
y_t_bare = g_bare / sqrt(2 N_c) = g_bare / sqrt(6)
y_t(M_Pl) / g_s(M_Pl) = 1 / sqrt(6)  on the canonical surface
```

as an **EXACT algebraic tree-level identity** in the SAME retained theory,
via a same-1PI-function residue argument:

- Representation A: direct OGE evaluation in the bare action gives the
  scalar-singlet coefficient `-c_S · g_bare² / (2 N_c · q²)` with `|c_S| = 1`
  from the Lorentz Clifford Fierz (S2, Block 8) and the SU(N_c) color Fierz
  (D12, Block 4).
- Representation B: independent evaluation of the H_unit operator's matrix
  element `⟨0 | H_unit | t̄ t⟩ = 1/√6` via Clebsch-Gordan from D9 + D17
  + canonical normalization (Steps 1-2). No reference to OGE.

Both representations independently give `1/6` in the q² × Γ⁽⁴⁾ coefficient,
confirming the same-1PI-function consistency.

This is materially different from the legacy "Cl(3) trace identity" line in
`YT_FLAGSHIP_BOUNDARY_NOTE.md:42`, which was a structural identity claim that
served as the lattice-scale boundary condition without an independent
operator-side derivation. The Ward branch closes that gap with the
two-representation residue theorem.

---

## The proposed primary path

```
Step 1.  y_t(M_Pl)  =  g_s(M_Pl) / √6      (Ward identity, exact)
Step 2.  y_t(v)     =  SM_RGE_run(y_t(M_Pl), M_Pl → v)   (continuum-limit)
Step 3.  m_t(pole)  =  standard SM matching from y_t(v) and v
```

The key claim being made is on Step 2: that SM RGE is **the correct
continuum-limit description** of the framework's lattice running between
`v` and `M_Pl`, NOT a "perturbative surrogate" for some unknown true
lattice blocking flow. By Wilsonian universality, asymptotic freedom of
QCD, and standard lattice-QCD continuum-limit theorems, this is the
expected behavior of any reasonable lattice gauge theory at scales much
below its cutoff. The framework's specific Wilson-staggered surface at
β = 6 with composite-Higgs D9 satisfies the standard premises.

Under this view the uncertainty on `y_t(v)` decomposes as:

| Source | Magnitude | Type |
|---|---|---|
| `g_s(M_Pl)` precision (input to Ward) | sub-permille | retained, from `α_LM = α_bare / u_0` |
| SM RGE truncation (NNLO → NNNLO) | ≈ 0.3% | standard SM (not framework-native) |
| lattice discretization `O(α_LM · a²)` | sub-percent | standard lattice QCD |
| **TOTAL** | **≈ 0.3–0.5%** | none of it framework-native explicit systematic |

This is materially smaller than the 1.21% Schur-bridge budget, AND it is a
genuinely different KIND of uncertainty: standard published-method residuals,
not framework-native bridge-construction artifacts.

---

## What happens to the Schur-bridge stack

The proposal **keeps the Schur-bridge work as an independent cross-check
path**, not as the primary derivation. Specifically:

- the bridge stack continues to give an independent number for `y_t(v)`
- agreement between the Ward-primary path and the Schur-bridge cross-check
  is a non-trivial consistency confirmation of the framework
- the 0.71% local + 0.50% nonlocal tails become the **bridge-path residuals**,
  not the load-bearing systematic on the package
- nothing in the bridge stack gets retracted; the work is real and remains
  publishable as an independent derivation route

The status of `YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md` would change from
"package authority for `derived with explicit systematic` wording" to
"bridge-path residual budget on the cross-check path."

---

## What the reviewer is being asked to agree

Three propositions, each separable:

**P1.** The Ward-identity derivation
(`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, landed on main) is a
complete and independent derivation of `y_t(M_Pl) = g_s(M_Pl) / √6` as
an exact tree-level identity on the canonical surface. *(This was already
agreed at Ward-branch review; this proposal merely cites it.)*

**P2.** SM RGE running between `v` and `M_Pl` is the correct continuum-limit
description of the framework's lattice flow at scales much below the
cutoff, by standard Wilsonian-universality arguments applied to the
framework's specific Wilson-staggered surface at `β = 6` with composite-
Higgs D9. The phrase "perturbative surrogate for the true lattice blocking
flow" overstates the methodological gap; the correct phrasing is "standard
continuum description by universality."

**P3.** Given P1 and P2, the appropriate package authority structure is:
the Ward path is the primary derivation of `y_t(v)`, the Schur-coarse-bridge
stack is an independent cross-check whose residuals are the cross-check's
budget rather than the package's systematic.

If P2 is the load-bearing one for the reviewer, the supporting materials
the reviewer should evaluate are:

- standard lattice-QCD continuum-limit theorems for Wilson-staggered with
  asymptotically free SU(N_c) gauge (textbook material)
- the framework's specific surface satisfies the standard premises
  (β = 6 weak-coupling tadpole-improved, single-cutoff, Wilsonian-block
  compatible)
- no framework-specific obstruction to the universality argument has been
  identified in the retained stack

---

## What the reviewer is NOT being asked to agree

- Any new theorem beyond what's on the Ward branch
- Retraction of any Schur-bridge work
- A specific quantitative replacement number for the systematic (only that
  the framework-native explicit systematic is no longer load-bearing)
- Changes to any other lane (Higgs, gravity, gauge couplings) — this
  proposal scopes only to the y_t / m_t lane

---

## Honest limitations of the proposal

- **The Ward branch must land on main first.** If Ward is rejected at land
  time for any reason, this proposal is moot.
- **The "standard continuum description" claim (P2) is a methodological
  framing, not a new theorem.** It rests on standard lattice-QCD universality
  results applied to the framework's specific surface. A reviewer who
  insists on a framework-internal continuum-limit theorem (independent of
  citing standard lattice-QCD universality) would need that work done
  separately.
- **Lattice discretization `O(α_LM · a²)` is itself an estimate**, not an
  independently retained systematic. Folding it into the Ward-path
  uncertainty is a standard move in lattice QCD but should be acknowledged
  as such.

If the reviewer rejects P2 specifically — i.e., insists that even with the
Ward identity exact at M_Pl, the lattice → continuum running between v and
M_Pl carries a distinct framework-native systematic that cannot be discharged
by appeal to universality — then the proposal fails and the existing
"explicit systematic" wording stays. That is a legitimate reviewer
position, and the proposal does not attempt to preempt it.

---

## What would happen on accept

If the reviewer agrees to P1 + P2 + P3, a follow-up branch would do the
authority surface updates:

1. `YT_FLAGSHIP_BOUNDARY_NOTE.md`: rewrite to make Ward primary, add
   universality-by-citation framing, demote bridge to cross-check.
2. `YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md`: rescope to "bridge-path
   cross-check residual budget", note the explicit systematic is no
   longer the package's load-bearing systematic.
3. `YT_BOUNDARY_THEOREM.md`, `YT_ZERO_IMPORT_AUTHORITY_NOTE.md`,
   downstream lane consumers: cite Ward as primary.
4. Package status surfaces (`docs/publication/ci3_z3/` files, `arXiv` draft,
   claims tables): update language and quoted systematic.
5. Runner: ensure scripts that quote the 1.21% budget are tagged as
   bridge-cross-check rather than package-authority.

That follow-up branch would be a separate proposal with its own review
pass. Nothing in the present proposal pre-commits to that work.

---

## What the reviewer should reply

A clean reviewer reply on this proposal looks like one of:

- **Accept (P1 + P2 + P3):** "Ward path supersedes; bridge becomes cross-check.
  Proceed with the follow-up authority-surface branch."
- **Accept P1 + P3, defer P2:** "Ward path is the cleaner derivation but
  the universality claim needs more support. Proceed with the authority
  realignment AFTER an explicit retained continuum-limit cross-check note."
- **Accept P1, reject P2:** "Ward identity at M_Pl is fine, but the lattice
  → continuum step still requires an explicit framework-native transport
  systematic. Keep the explicit-systematic wording."
- **Reject:** "The two paths are independent but the bridge stack remains
  the appropriate package primary. Keep status as is."

Any of these is a clean answer. The proposal exists to surface the question.
