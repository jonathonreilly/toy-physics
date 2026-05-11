# Complex Action: Kernel-Generic vs Gravity-Specific

**Date:** 2026-04-06
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/kernel-gravity-conflation-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/kernel-gravity-conflation-2026-04-30/` (the directory name encodes the failure reason: kernel/gravity conflation in the separation observable).
- **Audit verdict_rationale (quoted verbatim from `docs/audit/data/audit_ledger.json`):**

  > Issue: the source conflates link-level imaginary-action damping with the detector escape observable. The factor exp(-k gamma L f) is below 1 for f > 0 and gamma > 0, but the runner's detector escape ratios are still above 1 for UNIFORM f=0.005 at gamma=0.1 and 0.2, UNIFORM f=0.01 at gamma=0.1 and 0.2, and GRAVITY at gamma=0.1 and 0.2. Why this blocks: the retained separation claim says kernel-generic absorption occurs under any nonzero field at gamma > 0, but the measured observable used by the note only shows suppression at sufficiently large gamma in this setup. Repair target: distinguish local per-link attenuation from total detector escape, or add a theorem/runner proving a thresholded escape-suppression criterion across gamma and field families. Claim boundary until fixed: safely claim only that gamma=0.5 suppresses detector escape for the tested nonzero fields, and that the 1/r gravity field uniquely shows the tested TOWARD -> AWAY centroid crossover by gamma=0.2.

- **Do not cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Artifact chain

- [`scripts/complex_action_kernel_vs_gravity.py`](../scripts/complex_action_kernel_vs_gravity.py)
- [`logs/2026-04-06-kernel-vs-gravity.txt`](../logs/2026-04-06-kernel-vs-gravity.txt)

## Question

The complex action S = L(1-f) + i*gamma*L*f produces both absorption
(escape < 1) and deflection direction change (TOWARD → AWAY). Are these
the same phenomenon, or two distinct effects?

## Result

They are distinct:

### Kernel-generic: absorption under ANY nonzero field

| Field | gamma=0 escape | gamma=0.5 escape |
| --- | ---: | ---: |
| ZERO | 1.000 | 1.000 |
| UNIFORM (f=0.005) | 1.204 | 0.789 |
| UNIFORM (f=0.01) | 1.450 | 0.623 |
| GRAVITY (s=0.004) | 1.030 | 0.961 |

Mechanism: exp(-k*gamma*L*f) < 1 whenever f > 0 and gamma > 0.
No spatial structure required. Any constant field triggers absorption.

### Gravity-specific: localized deflection crossover

| Field | gamma=0 direction | gamma=0.2 direction |
| --- | --- | --- |
| ZERO | — | — |
| UNIFORM | random (1/2) | random (1/2) |
| GRAVITY | **TOWARD (2/2)** | **AWAY (0/2)** |

Mechanism: the 1/r field gradient couples to the beam centroid.
Only the spatially structured (localized) field produces directional bias.

## Claim boundary

The complex action produces two separable effects:
1. **Kernel-generic absorption**: any f > 0 with gamma > 0 suppresses amplitude
2. **Gravity-specific crossover**: only 1/r field produces TOWARD → AWAY transition

These are NOT the same phenomenon. The absorption is trivial (exponential
decay from imaginary action). The crossover is non-trivial (requires field
gradient and beam-field coupling).
