# Wilson Normalization / Comparison Reconciliation

**Date:** 2026-04-11  
**Status:** support - methodological control note
**Claim type:** meta
**Scope:** late-2026-04-11 Wilson Newton-strengthening batch

**Review repair perimeter (2026-05-05 generated-audit context):**
Generated-audit context identified this chain-closure blocker: "The methodological
inference is valid in form, but the restricted packet does not
provide the runner contents or independent evidence that the listed
Wilson runners are internally coherent or that older runners
differed in the named ways." The generated rationale notes that
the note is "a support/meta control note, not a first-principles
derivation from the axiom" and that "the safe negative caution
about over-attributing discrepancies is reasonable as a
methodological rule, but the concrete same-convention and
mixed-runner claims remain conditional on unprovided runner
verification." This rigorization edit only sharpens the boundary
of the repair perimeter; nothing here promotes audit status.
The note's claim type is `meta` (methodological control), and its
explicit purpose is to prevent over-attribution of mixed-runner
discrepancies to the `4*pi` factor — that purpose is already
correctly bounded by the existing `What Is Not Proven` and
`Reading Rule` sections. The four cited Wilson runners and their
shared convention are registered in "Cited authority chain
(2026-05-10)" below so the audit-graph edges from this support
note to its load-bearing inputs are explicit.

## Purpose

Prevent future summaries from collapsing several different Wilson runners into a
single story like:

> “the bad exponent came from a `4*pi` normalization mistake.”

That statement is too strong for the current evidence.

## What Is Actually True

The late Wilson batch is internally coherent **within one shared convention**:

- open 3D cubic Wilson surface
- complex Wilson hopping
- Poisson solve with `-4*pi*G*rho`
- low-screening regime `mu^2 = 0.001`

Within that convention, the following are all consistent with each other:

- [`scripts/frontier_newton_systematic.py`](../scripts/frontier_newton_systematic.py)
- [`scripts/frontier_test_mass_limit.py`](../scripts/frontier_test_mass_limit.py)
- [`scripts/frontier_perturbative_mass_law.py`](../scripts/frontier_perturbative_mass_law.py)
- [`scripts/frontier_continuum_limit.py`](../scripts/frontier_continuum_limit.py)

The safe conclusion is:

> within this same-convention open-Wilson lane, the weak-field test-mass and
> continuum companions support Newton-compatible scaling.

## What Is Not Proven

The current repo does **not** prove that `4*pi` alone caused every earlier
Wilson discrepancy.

Why not:

- older runners differed in more than Poisson source convention
- some also differed in:
  - screening regime
  - observable definition
  - geometry / boundary conditions
  - hopping convention
  - strong- vs weak-field operating point

So cross-runner disagreements cannot be attributed to the `4*pi` factor alone
unless all other differences are controlled simultaneously.

## Valid And Invalid Comparisons

### Valid

- compare the late Wilson batch **to itself**
- compare weak-field vs stronger-field behavior on the same open-Wilson surface
- compare screened vs low-screening exponents on the same observable family

### Invalid without further controls

- treating a mixed-runner exponent mismatch as a pure normalization diagnosis
- using the test-mass or perturbative runner as if it independently closes the
  both-masses Hartree lane
- reading the bounded Wilson companion as an architecture-wide Newton closure

## Reading Rule

If a Wilson summary uses one of:

- `frontier_test_mass_limit.py`
- `frontier_perturbative_mass_law.py`
- `frontier_continuum_limit.py`
- `frontier_newton_systematic.py`

then it must also preserve this sentence or an equivalent one:

> This is a same-convention open-Wilson calibration result, not a global
> normalization verdict across mixed Wilson runners.

## Cited authority chain (2026-05-10)

The generated-audit context cited at top flagged that the
restricted packet "does not provide the runner contents or
independent evidence that the listed Wilson runners are internally
coherent or that older runners differed in the named ways." Because
this is a methodological `meta` control note rather than a
first-principles derivation, the cited-authority chain serves to
register the four Wilson runners that share the late-2026-04-11
convention plus the cache contract that lets the audit lane verify
their shared convention without re-importing each runner's source.

| Cited authority | File | Provenance role |
|---|---|---|
| Same-convention runner #1 | [`scripts/frontier_test_mass_limit.py`](../scripts/frontier_test_mass_limit.py) | open 3D cubic Wilson surface, complex Wilson hopping, Poisson solve with `-4*pi*G*rho`, low-screening regime `mu^2 = 0.001`; one of the four internally-coherent runners |
| Same-convention runner #2 | [`scripts/frontier_perturbative_mass_law.py`](../scripts/frontier_perturbative_mass_law.py) | same convention as runner #1; one of the four |
| Same-convention runner #3 | [`scripts/frontier_continuum_limit.py`](../scripts/frontier_continuum_limit.py) | same convention as runner #1; one of the four |
| Same-convention runner #4 | [`scripts/frontier_newton_systematic.py`](../scripts/frontier_newton_systematic.py) | same convention as runner #1; one of the four |
| Cache contract | [`scripts/runner_cache.py`](../scripts/runner_cache.py) | declares the SHA-pinned cache header and the per-runner `AUDIT_TIMEOUT_SEC` declaration mechanism that the audit-lane precompute uses to record stdout/status for the four runners; long runners still need a declared longer budget or split runner before their caches can be completed. |

The review repair perimeter is exactly the absence of completed
stdout / runner-contents in the restricted audit packet. Because this
note is a methodological `meta` rule rather than a numerical claim,
the conditional rests only on the four cited runners actually
sharing the named convention; the audit-graph one-hop edges are
to the four runner sources above. A review-loop cache refresh recorded
`status: ok` for `frontier_test_mass_limit.py` and
`frontier_perturbative_mass_law.py`; `frontier_continuum_limit.py` and
`frontier_newton_systematic.py` still hit the default 120 s timeout,
so their caches are diagnostic freshness records rather than completed
stdout. The `Reading Rule` already
enforces the methodological boundary: any downstream Wilson summary
that cites these runners must explicitly preserve the
"same-convention open-Wilson calibration result, not a global
normalization verdict across mixed Wilson runners" sentence.

This rigorization edit only sharpens the conditional perimeter and
registers the cited authority chain; it does not set audit status,
hand-author audit JSON, claim that the four runners' shared
convention has been independently verified, or extend the
methodological scope beyond the existing `Valid` / `Invalid` table.
