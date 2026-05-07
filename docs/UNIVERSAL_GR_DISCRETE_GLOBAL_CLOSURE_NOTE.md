# Universal GR Discrete Global Closure on `PL S^3 x R`

**Status:** bounded structural assembly note. The bilinear-density and global
operator family `K_GR(D) = H_D ⊗ Lambda_R` are runner-verified at machine
precision (overlap covariance, chart-independent action, patched stationary
section). The note records that the **already-derived** local + signature-class
+ atlas-patching ingredients on the direct-universal route are mutually
compatible; it is **not** an axiom-first derivation of any of those imported
ingredients. (audit-prep refresh: 2026-05-06)
**Date:** 2026-04-14 (audit-prep refresh: 2026-05-06)
**Branch:** `codex/review-active`
**Role:** direct universal route / structural assembly summary
**Claim type:** `bounded_theorem` author hint; independent audit lane sets the
actual `claim_type`, `audit_status`, and pipeline-derived `effective_status`.
**Runner:** `scripts/frontier_universal_gr_discrete_global_closure.py`
(PASS=5 FAIL=0 on current source; verifies (i) the closure-stack source notes
exist, (ii) `K_GR` has no zero eigenvalues on the chosen Lorentzian
background, (iii) overlap covariance error < 1e-12, (iv) action mismatch
across the chart change < 1e-12, (v) stationary representatives patch with
mismatch < 1e-12).

## Audit boundary

The runner numerically certifies the four operator-level overlap properties
above on a single nondegenerate Lorentzian background `D0` and one explicit
chart change `S`. The note's structural-assembly statement (the eight bullets
under "What this means") is **conditional** on the prior closure-stack notes
being independently retained; it does not re-derive their content here.

**Admitted authority inputs (cited but not derived in this note):**
- `S3_ANOMALY_SPACETIME_LIFT_NOTE.md` — the discrete `3+1` lift `PL S^3 x R`
- `UNIVERSAL_GR_POSITIVE_BACKGROUND_LOCAL_CLOSURE_NOTE.md` — the exact local
  bilinear density `B_D(h,k) = -Tr(D^-1 h D^-1 k)` and the negative-definite
  Hessian `H_D` (sign character corrected 2026-05-01)
- `UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md` — extension of the
  exact local family from positive-symmetric to nondegenerate Lorentzian
  backgrounds
- `UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md` — finite-atlas
  congruence-covariance overlap compatibility
- the slice generator `Lambda_R` is taken as already-present on the branch
  (per the support-tier closure-stack chain)

This note does **not** re-prove the existence of `Lambda_R`, the global
patching theorem for stationary representatives across an arbitrary finite
atlas of `PL S^3 x R`, or any continuum/Lorentzian interpretation beyond the
explicit overlap data the runner exercises.

## Verdict (scope-bounded)

On the discrete-route ingredients listed above, the direct-universal route
**assembles** into a runner-verified compatibility certificate for an exact
global Lorentzian Einstein/Regge stationary action family on the discrete
`3+1` spacetime `PL S^3 x R`:

- the local bilinear `B_D` from the positive-background note,
- extended to Lorentzian signature by the signature-class note,
- glued by congruence-covariance overlaps from the global atlas note,
- on the discrete spacetime fixed by the spacetime-lift note,
- forms the global operator family `K_GR(D) = H_D ⊗ Lambda_R`.

The closure stack is:

- exact scalar observable generator
- exact `3+1` lift `PL S^3 x R` (`S3_ANOMALY_SPACETIME_LIFT_NOTE.md`)
- exact tensor-valued variational / quotient-kernel family
- exact canonical lapse / shift / trace / shear block structure
- exact isotropic glue and nonlinear completion
- exact positive-background extension and local closure
  (`UNIVERSAL_GR_POSITIVE_BACKGROUND_LOCAL_CLOSURE_NOTE.md`)
- exact Lorentzian signature-class extension
  (`UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md`)
- exact finite-atlas global patching
  (`UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`)

**Status authority disclaimer:** the words "exact" and "closed" in the bullet
list above refer to the runner-verified algebraic identities on the explicit
chart change `S` and background `D0` exercised by the runner, plus the cited
support-tier source notes. They are not a stand-alone first-principles
derivation; they are a structural-assembly statement conditional on those
inputs.

## What exactly is closed (assembly statement)

The exact local bilinear density

`B_D(h,k) = -Tr(D^-1 h D^-1 k)`

is defined on every nondegenerate Lorentzian background in the route (per the
positive-background and signature-class notes; sign character is
**negative-definite** as a quadratic form, see the positive-background note's
sign-correction history).

The exact slice generator `Lambda_R` is already present on the branch (cited
input, not derived here).

Therefore, on the discrete route, the global operator family

`K_GR(D) = H_D ⊗ Lambda_R`

is assembled on each finite atlas chart, and the runner exhibits one
explicit overlap pair `(D0, D1 = S^T D0 S)` for which:

- each local Lorentzian chart has an exact nondegenerate stationary problem
  (runner check 2: min |eig K_GR| > 1e-8);
- congruence covariance gives exact overlap compatibility (runner check 3:
  max overlap error < 1e-12);
- compatible local stationary representatives patch to the same stationary
  section (runner check 5: mismatch < 1e-12).

That is the runner-verified structural-assembly statement on the project's
discrete `3+1` route. Extension of this single-overlap certificate to "every
finite atlas of `PL S^3 x R`" is a separate closure that lives in the cited
atlas note (and is itself currently `audited_conditional`).

## What this means for "full GR" (scope clarification)

If by "full GR" we mean:

> the **runner-verified single-overlap structural-assembly statement** for
> a discrete `3+1` Einstein/Regge gravity law on the project's spacetime
> setting `PL S^3 x R`, conditional on the cited support-tier closure-stack
> notes,

then the direct-universal route is closed at this bounded scope.

If by "full GR" one means:

- a stronger continuum/Lorentzian interpretation beyond the project's exact
  discrete route, or
- an axiom-first derivation of the imported `Lambda_R`, slice generator, or
  global atlas patching theorem from `A_min`,

that is a further interpretation/derivation theorem, not provided here.

So the disciplined summary is:

- **runner-verified single-overlap discrete `3+1` GR assembly on the route,
  conditional on cited authorities:** YES
- **further continuum interpretation beyond that route:** separate question
- **axiom-first derivation of the imported ingredients:** separate question

## Prior audit history

The audit lane previously recorded `audit_status=audited_conditional` for
`universal_gr_discrete_global_closure_note` (commit `4f5a6b5b3`,
auditor `codex-cli-gpt-5.5`, independence `cross_family`). The auditor's
explicit finding was:

> The note asserts the global closure stack but cites no authorities and
> provides no runner or proof. Its conclusion depends on imported structural
> premises: the exact slice generator, tensor family, congruence covariance,
> and a global patching theorem for stationary representatives. Those are not
> closed inside the restricted packet, so the positive theorem cannot be
> audited cleanly from the supplied inputs.

This audit-prep refresh:

1. Adds the missing `**Status:**`, `**Claim type:**`, and `**Runner:**`
   header lines so the bounded scope, the support-tier authority, and the
   runner pointer are visible at the top of the file.
2. Names the `admitted_context_inputs` (the four cited support-tier notes
   plus `Lambda_R` as branch-given) explicitly, since the prior version
   used qualitative phrasing ("exact ... already present") that read as
   asserted rather than cited.
3. Tightens the verdict from "the strongest disciplined gravity theorem
   currently supported by the branch" / "capstone of the direct-universal
   branch" to a **scope-bounded structural-assembly statement**. The earlier
   "capstone" framing was an authority claim incompatible with the audit
   finding; the runner certifies an overlap-compatibility identity on one
   explicit chart pair, not a stand-alone first-principles closure.
4. Reframes "**full discrete `3+1` GR on the project's route:** YES" as a
   **conditional** YES (conditional on the cited closure-stack inputs and
   on the single-overlap runner check, not on a global atlas-exhaustion
   theorem).
5. Re-queues the changed source for independent audit authority.

The runner output (PASS=5 FAIL=0) is unchanged by this refresh; only the
note text was scope-tightened. Runner-verified algebraic content is
identical to the pre-refresh state.

## Honest status

This note is a **structural-assembly summary** of the direct-universal
branch, runner-verified at machine precision on one explicit chart pair,
conditional on the cited support-tier closure-stack notes.

It is **not** a stand-alone theorem; the words "capstone" and "strongest
disciplined gravity theorem" used in the prior version were authority claims
the audit lane explicitly declined to support. The substantive runner
identities (overlap covariance, action invariance, stationary patching) are
preserved and reproducible from `scripts/frontier_universal_gr_discrete_
global_closure.py`.

Anything stricter than the bounded scope above is a question of how far one
wants to identify this single-overlap structural-assembly statement with
other formulations of GR beyond the current project setting.
