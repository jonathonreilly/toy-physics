# Chiral Walk Synthesis Addendum

**Date:** 2026-04-10
**Status:** Overnight results retained in 1+1D and 2+1D, and retained at a specific 3+1D operating point, but the global 3+1D gravity claim is narrower than the 2026-04-09 synthesis stated.

This addendum folds the overnight `frontier/final-moonshots` work into the newer
3+1D recurrence and decoherence checks. It does not replace the overnight note.
It narrows the 3+1D interpretation where the newer like-for-like periodic sweep
shows a stronger limitation.

## What Still Stands From Overnight

- **1+1D chiral:** the wide-lattice result remains strong. Exact lattice
  Klein-Gordon in the low-k limit, Born-clean barrier behavior, U(1) gauge,
  exact light cone, and stable localized-source TOWARD deflection on the wide
  reflecting lattice are still retained. But a corrected carrier-k sweep at
  fixed `theta` does **not** support full achromaticity of the measured
  deflection.
- **2+1D chiral:** the closure-card operating point, approximate low-k
  Klein-Gordon behavior, and sub-percent superposition remain retained as
  overnight results.
- **3+1D chiral operating point:** the closure card at `n=21`, `L=16`,
  offset `3` remains a real positive result. It is not invalidated by the newer
  sweep; it is simply not enough to justify a universal 3+1D sign claim.
- **3+1D distance law script:** the overnight correction to the field-coupling
  convention was real. The sign must be `theta(r) = theta0 * (1 - f(r))`.
  The flipped convention `theta0 * (1 + gain * f)` produced spurious AWAY
  results and should not be used as evidence against the architecture.

## What The New 3+1D Sweep Changes

The new script [`scripts/frontier_chiral_3plus1d_decoherence_sweep.py`](../scripts/frontier_chiral_3plus1d_decoherence_sweep.py)
keeps the **same 3+1D periodic architecture** fixed and compares:

- coherent amplitudes
- exact classical probability propagation
- phase-kill after every layer

Across `n in {15, 21, 23, 25, 31}` and `L in {12, 14, 16, 18, 20, 28}`,
the sign windows do **not** disappear under classicalization. Broad AWAY windows
remain in the classical and phase-kill columns. That means the 3+1D sign problem
on the periodic architecture is not just coherent phase noise.

Representative AWAY windows from the sweep:

- coherent: `(15,16)`, `(21,12)`, `(23,12)`, `(25,14)`, `(31,16)`, `(31,20)`
- classical: `(15,14)`, `(21,18)`, `(21,20)`, `(23,18)`, `(23,20)`, `(25,20)`, `(31,28)`
- phase-kill: same broad windows as classical in this sweep

The older wide-lattice 1D decoherence script remains useful, but only as a
**1D reflecting-lattice fact**. It does not settle the 3+1D periodic case.

## Best Current 3+1D Framing

- **Retained:** there is a real TOWARD basin in 3+1D periodic chiral transport.
  The `n=17..23`, `L=14..20`, offset-`3` block contains a substantial all-TOWARD
  region, and the overnight closure card at `(21,16,3)` is a legitimate
  operating-point success.
- **Not retained:** a universal 3+1D gravity-sign law, monotone convergence with
  larger `n`, or the claim that AWAY windows are merely small coherent boundary
  artifacts that decoherence removes.
- **More accurate language:** 3+1D currently shows a **TOWARD basin with genuine
  periodic sign windows**, not an everywhere-attractive universal regime.

## What Organizes The Bad Windows

The newer notes
[`docs/CHIRAL_3PLUS1D_RECURRENCE_NOTE.md`](./CHIRAL_3PLUS1D_RECURRENCE_NOTE.md)
and
[`docs/CHIRAL_3PLUS1D_MIXING_PERIOD_NOTE.md`](./CHIRAL_3PLUS1D_MIXING_PERIOD_NOTE.md)
show that the best control variables are dimensionless:

- `delta = d / n` for source-mass offset relative to box size
- `lambda = L / n` for propagation depth relative to the box

The strongest AWAY bands cluster near half-wrap, late pre-recurrence, and
post-recurrence values of `lambda`. The flat mixing scale `pi / theta0` sets a
background timescale, but it does not by itself pin the bad windows. The field
shifts the local period only slightly; the periodic geometry is doing most of
the work.

## Implication

The overnight synthesis should now be read as:

- **1+1D:** retained
- **2+1D:** retained at the tested operating points
- **3+1D:** promising, with a real retained operating-point closure card and a
  real TOWARD basin, but not yet a universal sign-stable gravitational regime on
  the periodic architecture

That is a stronger and more defensible statement than either of the extremes:
"all dimensions validated" or "3+1D is pure chaos."

## Next Work

The next non-optional tests are:

1. compare periodic against reflecting or open boundaries at fixed `delta` and `lambda`
2. tie any geodesic-based gravity observable to the same retained 3+1D chiral transport law
3. sweep the 3+1D architecture in dimensionless coordinates first, not just by raw lattice size
