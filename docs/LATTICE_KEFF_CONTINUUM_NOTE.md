# k_eff = k*h Continuum Limit — Bounded Negative

**Date:** 2026-04-09
**Status:** retained NEGATIVE — the dense `k_eff = k*h` scheme does not rescue the continuum limit. After fixing a spacing bug in the first wrapper draft, the lane now runs cleanly through `h=0.5` and then collapses at `h=0.25`: free and mass detector probabilities are exactly zero while the maximum amplitude stays pinned at the source (`max|A| = 1`). So this is not an overflow lane. It is a **signal-collapse lane**. The simple `k -> k*h` renormalization does not preserve a nontrivial detector readout at fine spacing.

## Artifact chain

- [`scripts/lattice_keff_continuum.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_keff_continuum.py)
- [`logs/2026-04-09-lattice-keff-continuum.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-09-lattice-keff-continuum.txt)
- baseline comparison:
  - [`scripts/lattice_continuum_limit.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_continuum_limit.py)
  - [`docs/CONTINUUM_LIMIT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/CONTINUUM_LIMIT_NOTE.md)

## Scheme

This was the remaining open dense-continuum candidate after:

- Approach 1: nearest-neighbor only
- Approach 3: fan-out normalization

The modification is intentionally narrow. Keep the dense baseline kernel

```text
exp(i k act) * w / L * h^2
```

but replace the phase coupling with

```text
k_eff = k * h
```

so the transfer becomes

```text
exp(i (k*h) act) * w / L * h^2
```

The goal was to reduce fine-grid phase accumulation without reopening the
overflow/underflow pathologies that killed the other dense candidates.

## Result

| h | nodes | gravity | k=0 | MI | 1-pur | d_TV | read |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2.0 | 441 | -1.6910 | 0 | 0.3923 | 0.2804 | 0.6200 | works |
| 1.0 | 1681 | +0.1374 | 0 | 0.4942 | 0.4186 | 0.7588 | works |
| 0.5 | 6561 | +0.5821 | 0 | 0.3814 | 0.4598 | 0.6406 | works |
| 0.25 | 25921 | — | — | — | — | — | **fails** |

Failure diagnostics at `h=0.25`:

- `P_det, free = 0`
- `P_det, mass = 0`
- `max|A|, free = 1`
- `max|A|, mass = 1`

So the fine-grid failure is not:

- amplitude blowup
- unstable phase explosion
- large but noisy detector probability

It is a complete collapse of detector signal.

## Interpretation

The first wrapper draft incorrectly reported `FAIL` at every `h` because it
computed `spacing` from two same-layer nodes (`pos[1][0] - pos[0][0] = 0`).
After fixing that bug, the actual lane is clear:

- coarse and medium spacings do produce nonzero readings
- the fine spacing does not

That is enough to reject the simple scheme as a continuum-limit answer.

The likely structural reason is straightforward: the dense baseline already
has an `h^2` measure suppressing each edge transfer, and with `L ~ h` the
edge magnitude scales roughly like `h`. Replacing `k` by `k*h` weakens the
phase accumulation while leaving that amplitude suppression in place. By
`h=0.25`, the propagator is too weak to deliver any detector probability at
all on the retained geometry.

The observed behavior matches that picture:

- no blowup
- no oscillatory instability
- just loss of transport to the detector

## What this rules out

- the naive dense `k_eff = k*h` renormalization as a continuum unlock
- the idea that weakening the phase coupling alone is enough to keep the
  dense kernel both stable and nontrivial at fine `h`

## Candidate pool update

After this run, the dense candidate pool is:

- Approach 1 (nearest-neighbor only): retained through `h=0.25`, runtime-blocked finer
- Approach 2 (`k_eff = k*h`): **negative**
- Approach 3 (fan-out normalization): **negative**

So the dense-continuum rescue program is effectively closed in its current
simple form. The only surviving refinement path is the nearest-neighbor
branch, and that branch is already known to be narrow and runtime-limited.

## Bottom line

> "The dense `k_eff = k*h` continuum scheme is not a rescue. After fixing
> the initial wrapper bug, it runs through `h = 0.5` but collapses at
> `h = 0.25`: both free and mass detector probabilities are exactly zero
> while the maximum amplitude remains 1 at the source. This is not an
> overflow lane; it is a signal-collapse lane. Weakening the phase coupling
> alone does not preserve a nontrivial dense continuum readout. Approach 2
> joins fan-out normalization as a negative dense-continuum candidate."
