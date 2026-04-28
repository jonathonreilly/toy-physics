# 3D Kernel Transfer-Norm Probe

**Date:** 2026-04-04 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** bounded local discrimination probe; not a branch-promotion claim and not a continuum-limit theorem.

This note freezes a small local probe of the exploratory 3D kernel lane.
It is intentionally narrower than the heavy `h=0.25` / 4D work Claude is
running elsewhere.

## Script

[`scripts/lattice_kernel_transfer_norm_probe.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_kernel_transfer_norm_probe.py)

## Log

[`logs/2026-04-04-lattice-kernel-transfer-norm-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-lattice-kernel-transfer-norm-probe.txt)

## What the probe measures

The probe computes a local outgoing transfer norm on a representative 3D
ordered-lattice neighborhood:

- kernel power `p` in `1/L^p`
- refinement `h`
- measure-corrected norm `h^2 × Σ exp(-β θ²) / L^p`

It is a discrimination harness, not a proof of the continuum limit.

## Retained local read

Using the measured norm with `h^2` normalization, the closest-to-marginal
power in the tested sweep is:

- `p = 1.5` is closest to stable across `h = 1.0, 0.5, 0.25, 0.125`
- `p = 2.0` is next, but still drifts with refinement
- `p = 2.5` and `p = 3.0` drift more strongly away from marginality

The fitted measured-norm slopes from the probe are:

| p | measured slope | read |
|---|---:|---|
| 1.5 | `+0.102` | closest to marginal |
| 2.0 | `-0.204` | still scales with `h` |
| 2.5 | `-0.598` | clearly non-marginal |
| 3.0 | `-1.046` | strongly non-marginal |

## Review-safe interpretation

- This does **not** prove the final 3D kernel power.
- It does **not** replace the same-harness propagation audits.
- It does **not** settle the branch-level promotion question.

What it does give us is a bounded local discriminator:

- the simple local transfer norm does not currently single out `p = 2.0`
- the probe points to a shallower effective marginality near `p = 1.5`
- that result should be treated as a review-safe warning, not a promoted law

This note should also not be collapsed into the later exploratory
[`scripts/transfer_norm_and_born.py`](/Users/jonreilly/Projects/Physics/scripts/transfer_norm_and_born.py)
branch story. They are different observables, and the transfer-norm selection
story remains under reconciliation on `main`.

## Why this matters

The probe is useful because it separates three questions that should not be
blurred together:

1. sign persistence under refinement
2. distance-tail steepening
3. finite-magnitude transfer control

Only the third question is tested here, and only in a local kernel-only way.
The full 3D branch still needs same-harness propagation and artifact-chain
closure before any promotion.

## Audit boundary (2026-04-28)

The earlier Status line ("bounded discrimination probe, not a
`proposed_promoted` branch claim") tripped the audit-lane parser, which
classified the row as `proposed_promoted` solely because the literal
token appeared in the Status string — even though the note's intent was
the negation. The Status line has been rephrased to remove the parser
collision while keeping the same intent.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: the audit target is classified as `proposed_promoted`, but the
> source note states that this is a bounded discrimination probe and not
> a `proposed_promoted` branch claim. Why this blocks: a local outgoing
> transfer norm over four `h` values can warn that `p=2.0` is not
> singled out, but it does not establish a promoted 3D kernel branch, a
> continuum limit, or same-harness propagation behavior; treating this
> note as a promoted branch would contradict the note's own scope.

> Claim boundary until fixed: it is safe to claim only the finite local
> discriminator: with `h^2` normalization and `h = {1.0, 0.5, 0.25,
> 0.125}`, `p = 1.5` has measured slope `+0.102`, `p = 2.0` has
> `−0.204`, `p = 2.5` has `−0.598`, and `p = 3.0` has `−1.046`; this is
> a warning signal, not a promoted law.

## What this note does NOT claim

- A promoted 3D kernel branch.
- A continuum-limit theorem on the lattice kernel.
- Same-harness propagation behavior of any selected `p`.
- A first-principles selection of the kernel power.

## What would close this lane (Path A future work)

A future worker pursuing branch promotion would need a separate note
with a registered primary runner that establishes:

1. The selected kernel power on same-harness propagation across the
   four `h` values.
2. Born/controls passing on the selected kernel power.
3. Refinement-stable behavior across at least three `h` values.
4. A continuum-limit argument tying the lattice probe to a target
   3D-kernel theorem.
