# Shapiro Diamond Frequency Bridge Note

**Date:** 2026-04-06  
**Status:** RETRACTED 2026-04-30 — audit failed; this note is archived under `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. See `## Retraction` section.

## Retraction

- **Date archived:** 2026-04-30
- **Archive directory:** `archive_unlanded/shapiro-static-renderers-and-failed-bridges-2026-04-30/` (the directory name encodes the failure reason: static renderers and failed bridges).
- **Audit verdict_rationale (quoted verbatim from `docs/audit/data/audit_ledger.json`):**

  > Issue: The frequency bridge depends on a conditional Shapiro-delay result, a failed Shapiro-diamond bridge, and unaudited/conditional diamond phase-ramp and signal-budget notes, with no runner constructing phi, k-scaling, or normalized phase-ramp quantities. Why this blocks: translating an unratified proxy scaling into lab-facing X/Y/phi language does not establish a retained frequency-sensitive diamond/NV prediction or a calibrated comparison surface. Repair target: audit or repair SHAPIRO_DELAY_NOTE and SHAPIRO_DIAMOND_BRIDGE_NOTE, audit the diamond phase-ramp and signal-budget notes, and add a runner that varies k at fixed geometry and verifies phi/k and slope/k collapse from generated data. Claim boundary until fixed: it is safe to say this note proposes a proxy-level frequency-bridge test to run; it is not safe to claim retained k-linear diamond/NV phase-ramp behavior.

- **Do not cite warning:** Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

## Artifact Chain

- [`docs/SHAPIRO_DELAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DELAY_NOTE.md)
- [`docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md)
- [`docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_PHASE_RAMP_BRIDGE_CARD_NOTE.md)
- [`docs/DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_NV_PHASE_RAMP_SIGNAL_BUDGET_NOTE.md)
- [`docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_SENSOR_PROTOCOL_NOTE.md)
- [`docs/DIAMOND_SENSOR_PREDICTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DIAMOND_SENSOR_PREDICTION_NOTE.md)
- retained scaling result anchor:
  - commit `1730b52` (`feat(shapiro): phase scales as s^1.000 (linear in mass), proportional to k`)

## Question

How do we translate the retained `k`-proportional Shapiro scaling into the
diamond/NV bridge language without turning the proxy result into an absolute
lab claim?

## Retained Scaling Result

The Shapiro delay is not just a phase lag.
It scales as a phase observable:

- phase `~ s^1.000` in source strength / mass proxy
- phase decreases with impact parameter `b`
- phase `~ k`, i.e. the delay is chromatic / frequency sensitive

The important part for the bridge is the last one:

- at fixed geometry, the lag grows with the drive wavenumber/frequency scale
- equivalently, the normalized phase response is the cleanest proxy quantity

## Bridge Translation

The diamond bridge card already uses the right language:

- `X`: in-phase channel
- `Y`: quadrature channel
- `phi = atan2(Y, X)`: phase lag
- phase-ramp slope: spatial accumulation of the lag

The Shapiro scaling adds one more dimension to that language:

- the phase lag itself should scale with the drive frequency scale `k`
- the phase-ramp slope should scale with `k` in the same proxy sense
- after dividing out the drive scale, the proxy phase response should collapse

So the clean lab-facing translation is:

- hold geometry fixed
- vary drive frequency / wavenumber
- look for a quadrature / phase-ramp response that scales linearly with `k`
- check whether `phi / k` and the normalized phase-ramp slope stay roughly
  constant across the retained proxy sweep

That is the frequency-sensitive analog of the existing phase-ramp bridge card.

## Why This Is Useful

This is a better lab-facing discriminator than raw amplitude alone because:

- absolute amplitude still needs external calibration
- phase and quadrature are naturally normalized observables
- the retained Shapiro result already says the lag is monotone in slower
  propagation and proportional to `k`

So the frequency bridge turns the Shapiro result into a lab-friendly proxy
prediction:

- higher drive frequency should produce a proportionally larger phase lag
- the same geometry should preserve the sign and ordering of the lag
- the normalized phase response should be cleaner than the raw amplitude

## What Can Be Claimed In-Repo

The repo can defensibly say:

- the Shapiro delay is portable across the retained grown families
- the delay is seed-stable and exact-null safe
- the delay is proportional to `k`
- the delay is expressible in the same `X / Y / phi` and phase-ramp language
  used by the diamond bridge card

The repo cannot yet say:

- the absolute NV-unit mapping for frequency or phase
- the lab-specific detectability threshold
- a calibrated conversion from proxy `k` to microscope readout units

## Narrow Prediction

If a diamond/NV setup is driven at multiple frequencies while holding the
geometry fixed, the clean proxy prediction is:

- `phi` grows approximately linearly with `k`
- the phase-ramp slope grows approximately linearly with `k`
- the normalized ratios `phi / k` and slope / `k` are the cleaner quantities
  to compare across runs

That is the proxy-level frequency bridge.

## Final Verdict

**the retained Shapiro delay is frequency-sensitive in the same phase-language
as the diamond bridge card: `X / Y / phi` and phase-ramp slope should scale
with `k`, but the absolute NV calibration remains external**
