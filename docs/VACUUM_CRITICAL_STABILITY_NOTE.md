# Vacuum Critical Stability Companion

**Date:** 2026-04-15 (Gap #7 update 2026-05-10)
**Status:** bounded companion prediction on `main`
**Primary runner:** `scripts/frontier_higgs_mass_full_3loop.py` ([scripts/frontier_higgs_mass_full_3loop.py](../scripts/frontier_higgs_mass_full_3loop.py))
**Additional primary runner:** `scripts/frontier_yt_color_projection_correction.py`
**Boundary-support runner:** `scripts/frontier_direct_yt_extraction.py`

## Authority Role

This note is the standalone authority for the bounded vacuum-critical-stability
readout extracted from the current Higgs / vacuum package.

It is separate from:

- the retained hierarchy / `v` lane
- the broader Higgs / vacuum explicit-systematic package note
- the Yukawa / top lane that still controls the quantitative systematic

## Safe Statement (revised, Gap #7 2026-05-10)

The framework's high-scale Higgs boundary condition is **OPEN**.

Three candidate routes for forcing the high-scale quartic coupling exist in
the literature:

1. **Asymptotic safety** (Wetterich, Eichhorn, Reuter — UV fixed point of
   gravity-matter system can drive `lambda(M_Pl) -> 0`).
2. **Multiple-Point Principle** (Froggatt-Nielsen 1996 — degenerate vacua
   force `lambda(M_Pl) ~= 0` and `beta_lambda(M_Pl) ~= 0`).
3. **pNGB compositeness with shift symmetry** (Contino-Pomarol 2003 —
   pseudo-Nambu-Goldstone Higgs has a tree-level shift symmetry that
   protects the quartic at tree level).

**None of these is currently derived in the framework.** The framework's
existing `m_H` prediction routes (full 3-loop running from observed inputs;
lattice mean-field tree-level + corrections) do **not** load-bear on the
boundary condition: they consume `lambda(M_Pl) = 0` as an *admitted-context*
input, exactly as the Buttazzo / Degrassi SM analyses do.

This note therefore reframes the prior `lambda(M_Pl) = 0` claim as a
literature-standard input choice, not a framework-derived theorem. The
companion vacuum-stability readout produced by the runners remains a useful
*sensitivity surface* for Higgs / `y_t` precision work, but it is no longer
asserted as a framework-native consequence.

## Why The Prior Claim Was Retired (Gap #7 / PR #937)

The earlier "framework-native composite-Higgs / no-elementary-scalar boundary
structure" wording for `lambda(M_Pl) = 0` was a heuristic slogan, not a
theorem. PR #937 retired the slogan as a named obstruction (NJL-style
composite-scalar models give a *nonzero* tree-level quartic via four-fermion
auxiliary-field bosonization — Bardeen-Hill-Lindner 1990 BHL, Hill 1991).

The Gap #7 literature probe confirmed: across BHL top-condensate models,
walking technicolor, asymptotic safety, and holographic compositeness, the
**only theorem-grade route from compositeness to `lambda_tree = 0`** is the
pNGB / shift-symmetry route of Contino-Pomarol 2003 — and even there the
protection is at *tree* level only. The framework does not currently carry
a pNGB shift-symmetry derivation for its taste-condensate identification of
the Higgs scalar, so the Contino-Pomarol route is not available either.

The cleanest fix is therefore to **drop the asserted boundary-condition
claim** rather than reframe it as pNGB. The companion vacuum readout still
exists as a calculable function of `lambda(M_Pl)`, but the choice of
`lambda(M_Pl) = 0` is now flagged as a literature-standard admitted-context
input on equal footing with the SM analyses.

## First-Principles Status (Gap #7 audit, 2026-05-10)

### Counterfactual Pass (cap 250 words)

**Assumptions in the prior claim:**

1. The framework's taste-condensate identification of the Higgs is *equivalent
   to* a composite-Higgs picture in the pNGB sense.
2. "No elementary scalar" automatically forces `lambda_tree = 0`.
3. Choice (a) — drop the claim — is cleaner than choice (b) — pNGB reframing.

**Negate (1).** If the taste condensate is NJL-like rather than pNGB-like,
auxiliary-field bosonization gives `lambda_tree != 0` at the matching scale
(BHL, Hill). The framework has no current derivation distinguishing pNGB
vs NJL behavior on the retained taste block. So (1) is not safe.

**Negate (2).** A theory with no fundamental scalar can still have a
*nonzero* induced tree-level quartic via fermion-bilinear bosonization. This
is exactly what BHL constructs: the auxiliary scalar `H ~ (psi-bar psi)`
has both a tree-level mass term and a tree-level quartic at the matching
scale. So "no elementary scalar" does not in itself force vanishing
quartic.

**Negate (3).** What if pNGB framing is genuinely available? It would
require a derived shift symmetry of the form `H -> H + c` on the framework's
taste-condensate field at the matching scale. The framework has no such
derivation: the taste-block isotropy theorem
(`TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md`) shows isotropy of the one-loop
fermion CW Hessian, not a tree-level shift symmetry. Pursuing (b) without
that derivation would just relocate the unjustified-claim problem from
"composite => lambda=0" to "shift-symmetric pNGB => lambda=0". So (3) holds:
(a) is cleaner.

### Elon First-Principles (cap 250 words)

**Strip framework. Standard QFT.** Under what conditions can a composite-scalar
theory force `lambda_tree(Lambda) = 0` at some scale `Lambda`?

**Candidate mechanisms from QFT primitives:**

- **Symmetry-protected tree-level vanishing.** A continuous shift symmetry
  `H -> H + c` forbids any polynomial potential including the quartic. This
  is the pNGB mechanism (Contino-Pomarol). It requires the scalar to be a
  pseudo-Goldstone of an approximate global symmetry that is spontaneously
  broken at a higher scale `f >> Lambda_EW`. The shift symmetry is exact at
  tree level and only broken by explicit symmetry-breaking spurions
  (typically Yukawa and gauge couplings).

- **Fixed-point flow at high scale.** If the `beta_lambda` flow has a UV
  fixed point at `lambda* = 0`, and the theory is asymptotically safe,
  trajectories ending at that fixed point have `lambda(M_Pl) -> 0`. This
  requires a non-trivial UV completion (gravity-matter asymptotic safety,
  Wetterich; or Bank-Zaks-like fixed point in a specific gauge sector).

- **Multiple-Point Principle / fine-tuned matching.** Demanding the EW
  vacuum be degenerate with a Planck-scale vacuum imposes both
  `lambda(M_Pl) = 0` and `beta_lambda(M_Pl) = 0` (Froggatt-Nielsen). This
  is a non-derivative principle, not a symmetry consequence.

**Mere compositeness — auxiliary-field bosonization of `(psi-bar psi)` —
does NOT in general force vanishing tree-level quartic.** BHL explicitly
gets a non-zero matching-scale quartic. Walking TC and holographic models
likewise do not generically force vanishing.

**Conclusion:** without a derived shift symmetry, fixed-point flow, or MPP,
no QFT-primitive route from "composite scalar" to `lambda_tree = Lambda) = 0`
exists. Drop the claim.

## What Is Exact On The Current Surface (revised)

- the existence of a direct framework-side full 3-loop Higgs/vacuum runner on
  `main` that *consumes* `lambda(M_Pl) = 0` as admitted-context input and
  produces a vacuum-stability readout
- the existence of a separate corrected-`y_t` 2-loop / 3L+NNLO support route
  that produces a complementary `m_H` readout

## What Is Still Bounded / Open

- the high-scale boundary condition `lambda(M_Pl) = 0` is **OPEN**: no
  framework-native derivation is available. The runners use it as an
  admitted-context input, not as a framework consequence.
- the quantitative vacuum readout still inherits the explicit-systematic
  Yukawa / top lane (precision caveat on `y_t`)
- the package does not promote vacuum critical stability as an independent
  retained theorem separate from the bounded Higgs package

## Current Readout (with revised provenance)

The companion runners still produce numerical readouts when supplied with
the admitted-context `lambda(M_Pl) = 0` input:

- `m_H(2-loop support route) = 119.8 GeV`
- `m_H(full 3-loop framework-side route) = 125.1 GeV`
- vacuum readout: critical / non-metastable side **conditional on**
  `lambda(M_Pl) = 0`
- comparator: the usual SM observed-input route is commonly read as
  metastable

These readouts are now flagged as *conditional on the same admitted-context
boundary input that the SM analyses use*, not as framework consequences of
a derived boundary structure.

## Falsification Surface

If precision measurements of `m_t`, `m_H`, and the associated running inputs
force the vacuum deep into the metastable region in a way incompatible with
the current bounded framework-side `y_t` band — *under the same admitted
boundary input* — this companion readout is in tension with the framework
route.

This falsifier remains valid: it tests the framework's `y_t` precision
prediction *given* the admitted boundary, exactly as the SM falsifier does.
What the falsifier no longer tests is a (now-retired) framework derivation
of the boundary itself.

## Supporting Notes

- [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](./HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md)
- [HIGGS_MASS_DERIVED_NOTE.md](./HIGGS_MASS_DERIVED_NOTE.md)
- [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](./YT_COLOR_PROJECTION_CORRECTION_NOTE.md)
- [COMPOSITE_HIGGS_MECHANISM_STRETCH_ATTEMPT_NOTE_2026-05-03.md](./COMPOSITE_HIGGS_MECHANISM_STRETCH_ATTEMPT_NOTE_2026-05-03.md) — companion stretch attempt at composite-Higgs identification, with three named residual obstructions; relevant context for any future attempt to derive the high-scale boundary

## Validation Snapshot

- current package boundary-condition input: `lambda(M_Pl) = 0` (admitted-context, literature-standard; no framework-native derivation)
- full 3-loop framework-side Higgs runner exists and is live on `main`,
  consuming the admitted-context boundary input
- vacuum stability remains bounded through the same explicit-systematic Yukawa / top route that
  controls the current Higgs package
- pursuit of a framework-native derivation of the boundary is logged as an
  open-gate item; candidate routes (asymptotic safety, MPP, pNGB) are
  flagged but none is closed

Primary reruns:

- `frontier_higgs_mass_full_3loop.py`
- `frontier_yt_color_projection_correction.py`
- `frontier_direct_yt_extraction.py`
