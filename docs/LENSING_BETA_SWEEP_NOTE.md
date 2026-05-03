## Lane M — BETA sweep of the lensing slope

**Status:** bounded conditional negative (status line narrowed 2026-04-28 per audit-lane verdict). The reported coarse-grid `beta = 5` recovery of canonical `1/b` lensing is described in this note as an isolated coarse-resolution spike that is unstable under nearby `beta = 7, 10` and under H-refinement at `H = 0.35`. The runner is not registered in the audit ledger; the result is scoped to Fam1 `b = {3, 4, 5, 6}`; the adjoint-kernel authority used for interpretation is not registered. Not a tier-ratifiable negative theorem.

### Artifact chain

- [`/Users/jonreilly/Projects/Physics/scripts/lensing_beta_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/lensing_beta_sweep.py)
- [`/Users/jonreilly/Projects/Physics/logs/2026-04-08-lensing-beta-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-08-lensing-beta-sweep.txt)

### Question

After the finite-path/ray explanation failed, the next clean mechanism test was:

> Does the `≈ -1.43` slope come from the propagator's broad angular
> distribution, and if so, does forcing a narrow angular window recover a
> ray-like `1/b` law?

The relevant control knob is the per-edge angular weight

`exp(-beta * theta^2)`,

where larger `beta` suppresses off-axis paths more strongly.

If `beta=5` were a genuine geometric-optics limit, two things should happen:

1. nearby large-`beta` values should stay near slope `-1`
2. the result should survive refinement

### Harness

The sweep uses the same asymptotic subset as Lane L+:

- `b in {3, 4, 5, 6}`
- Fam1 geometry (`seed=0`, `drift=0.20`, `restore=0.70`)
- `kubo_true(b)` from the first-order Kubo coefficient

Two checks were run:

1. coarse `H=0.5` scan at `beta in {0.8, 5, 7, 10}`
2. refinement check at `H=0.35`, `beta=5`

### Results

#### Coarse scan (`H=0.5`)

| `beta` | `kubo_true(b=3..6)` | slope | `R^2` | sign pattern | `1/b` shape spread |
|---|---|---:|---:|---:|---:|
| `0.8` | `[7.0619, 5.6136, 3.6639, 3.0176]` | `-1.2811` | `0.9711` | `++++` | `14.54%` |
| `5.0` | `[0.0189, 0.0139, 0.0112, 0.0094]` | `-1.0114` | `0.9995` | `++++` | `1.69%` |
| `7.0` | `[-0.0035, -0.0024, -0.0018, -0.0013]` | `-1.3922` | `0.9971` | `----` | `24.00%` |
| `10.0` | `[-0.0004, -0.0003, -0.0002, -0.0002]` | `-1.2690` | `0.9989` | `----` | `17.12%` |

At `H=0.5`, `beta=5` looks special: slope `-1.0114`, near-perfect `1/b` shape,
all-positive sign pattern.

But the nearby large-`beta` points do **not** cluster there:

- `beta=7` changes sign and steepens to `-1.3922`
- `beta=10` stays negative and lands at `-1.2690`

So `beta=5` is not an asymptotic ray-optics branch. It is a localized spike in
parameter space.

#### Refinement check (`H=0.35`, `beta=5`)

| `H` | `beta` | `kubo_true(b=3..6)` | slope | `R^2` | sign pattern | `1/b` shape spread |
|---|---:|---|---:|---:|---:|---:|
| `0.35` | `5.0` | `[-0.034338, -0.02764, -0.023081, -0.01981]` | `-0.7930` | `0.9994` | `----` | `15.38%` |

This kills the coarse `beta=5` moonshot directly:

- the sign flips from `++++` to `----`
- the slope moves from `-1.0114` to `-0.7930`
- the coarse `1/b` shape does not survive refinement

### What survives

Only the narrower statement survives:

- the lensing slope is sensitive to `beta`
- changing `beta` changes both amplitude and sign structure

That is consistent with the adjoint-kernel result in
`/Users/jonreilly/Projects/Physics/docs/LENSING_ADJOINT_KERNEL_NOTE.md` (downstream consumer in same lane; cross-reference only — not a one-hop dep of this note):
the observable is a broad detector-weighted wave response, so it should depend
on the propagator's angular weighting.

### What is falsified

This lane falsifies the stronger rescue:

> "Make the beam narrow enough and the model cleanly recovers canonical
> `1/b` lensing."

That claim is not retainable. The only clean near-`-1` point found so far is a
single coarse-resolution coincidence at `beta=5`.

### Current honest state of the lensing program

- The strongest retained positive is still the exact adjoint-kernel identity:
  the literal first-order observable is a broad detector-weighted edge sum.
- The strongest retained empirical fact on the slope is still:
  default `beta=0.8`, `H=0.25`, `b in {3,4,5,6}` gives a clean power law near
  `-1.43`.
- The mechanism remains open.
- The simple narrow-beam / ray-optics rescue is now closed.

### Best next move

The next high-value mechanism test is no longer "push beta larger." It is:

1. fan out the exact adjoint kernel over `b in {3,4,5,6}` at default `beta`
2. compare normalized kernel shapes across `b`
3. only then test whether kernel width/skew, rather than raw `beta`, tracks the
   `-1.43` exponent

### Bottom line

> "The `beta=5` near-`1/b` result was not a real narrow-beam limit. It is an
> isolated coarse-grid spike. Nearby large-`beta` values already leave it, and
> the `H=0.35` refinement check flips sign and lands at slope `-0.7930`. The
> lensing mechanism is still open, but the simple ray-optics rescue is closed."

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, high criticality, 124 transitive
descendants):

> Issue: the proposed_retained negative rests on a beta sweep and
> H-refinement numerical battery, but the audit ledger registers no
> primary runner/output, and the source note's artifacts are
> absolute local paths outside the audit packet. Why this blocks: a
> hostile auditor cannot reproduce the key `beta = 5` coarse slope,
> the `beta = 7 / 10` sign/shape departures, or the `H = 0.35` sign
> flip / slope `-0.7930` from registered evidence; the result is
> also scoped to Fam1 `b = {3, 4, 5, 6}` and does not register the
> adjoint-kernel authority it uses for interpretation.

## What this note does NOT claim

- A framework-level negative theorem about narrow-beam recovery
  beyond the single Fam1 sweep.
- That the adjoint-kernel interpretation is supported by registered
  authority; that authority is not registered as a one-hop
  dependency.
- Reproducibility from the audit packet alone; the runner and log
  use absolute local paths.

## What would close this lane (Path A future work)

Promoting from bounded conditional to retained would require:

1. Registering `scripts/lensing_beta_sweep.py` and its deterministic
   output as the primary runner with PASS thresholds.
2. Registering the adjoint-kernel authority used for interpretation.
3. Replacing absolute-path artifact links with relative paths inside
   the audit packet.
4. Extending or explicitly bounding the family / `b` coverage.
