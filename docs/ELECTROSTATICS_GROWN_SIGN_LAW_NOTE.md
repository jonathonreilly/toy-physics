# Electrostatics Grown Sign-Law Note

**Date:** 2026-04-05 (status line narrowed 2026-04-28 per audit-lane verdict)
**Status:** bounded narrow grown-geometry sign-law companion — frozen numerical results for one fixed grown geometry row; the runner is not registered in the audit ledger and the artifact links use absolute local paths outside the audit packet.

## Artifact chain

- [`scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py`](/Users/jonreilly/Projects/Physics/scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py)
- [`logs/2026-04-05-electrostatics-grown-sign-law.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-electrostatics-grown-sign-law.txt)

## Question

Can the retained scalar sign-law family survive on the retained grown row
without becoming a geometry-generic claim?

This check is intentionally narrow:

- retained grown geometry row only: `drift = 0.2`, `restore = 0.7`
- fixed-field, no graph update
- one source layer, one final-layer detector centroid
- source sign in `{-1, +1}` plus simple multi-source superposition cases
- exact same-point neutral cancellation guardrail
- linearity check via `+1` versus `+2`

## Frozen Result

On the retained grown row, the sign law survives cleanly:

| case | source(s) | delta_z mean | sign | read |
| --- | ---: | ---: | ---: | --- |
| single `+1` | `+1@3.0` | `-1.882286e-04` | `AWAY` | `repel` |
| single `-1` | `-1@3.0` | `+1.882349e-04` | `TOWARD` | `attract` |
| neutral same-point `+1/-1` | `+1@3.0 + -1@3.0` | `+0.000000e+00` | `ZERO` | `null` |
| like pair `+1/+1` | `+1@2.0 + +1@4.0` | `-2.556525e-04` | `AWAY` | `repel` |
| dipole `+1/-1` | `+1@2.0 + -1@4.0` | `+3.137392e-05` | `TOWARD` | `partial-cancel` |
| double `+2` | `+2@3.0` | `-3.764509e-04` | `AWAY` | `linear` |

Reduction / linearity checks:

- neutral same-point pair mean delta: `+0.000000e+00`
- single `+1` vs double `+2` charge exponent: `1.000`
- single `-1` mean delta: `+1.882349e-04`
- dipole mean delta: `+3.137392e-05`

## Safe Read

The narrow, review-safe statement is:

- the same sign-coupled propagator still supports like/unlike sign response on the retained grown row
- neutral same-point `+/-` sources cancel to printed precision
- the response is approximately linear in source charge on this grown geometry
- this narrows the exact-to-grown transfer gap for the scalar sign-law family

## What this is not

- It is not full electromagnetism.
- It is not a Maxwell or radiation derivation.
- It is not a geometry-generic theorem.

## Final Verdict

**retained narrow grown-geometry sign-law companion**

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, high criticality, 123 transitive
descendants):

> Issue: the retained sign-law companion rests on frozen numerical
> results for one fixed grown geometry row, but the audit ledger
> registers no primary runner or output, and the note's artifact
> links are absolute local paths outside the audit packet. Why this
> blocks: a hostile auditor cannot reproduce the printed `delta_z`
> signs, neutral cancellation, dipole partial cancellation, or
> +1/+2 linearity threshold from registered evidence; moreover the
> note explicitly limits the result to fixed-field, no graph update,
> one source layer, and one final-layer centroid on a single grown
> row.

## What this note does NOT claim

- A grown-geometry sign-law theorem beyond the one fixed grown row.
- That the printed `delta_z` signs, neutral cancellation, dipole
  partial cancellation, or +1/+2 linearity threshold are
  reproducible from registered evidence; the runner is not
  registered.
- Coverage beyond fixed-field, no graph update, one source layer, and
  one final-layer centroid.

## What would close this lane (Path A future work)

Promoting from bounded conditional to retained would require:

1. Registering `scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py` as the
   claim runner with deterministic output and explicit PASS
   thresholds for sign, cancellation, and charge-linearity.
2. Replacing the absolute-path artifact links with proper relative
   paths inside the audit packet.
3. Either keeping the note scoped to the single grown row (current
   stance) or extending the runner to a family of grown geometries
   with hard PASS gates.
