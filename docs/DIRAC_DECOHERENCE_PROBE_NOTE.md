# Dirac Decoherence / Record Probe

**Date:** 2026-04-10  
**Scope:** test whether the 4-component Dirac walk's decoherence / purity failures are a bad harness match or a real architecture problem.

## Geometry

The probe uses a compact Dirac double-slit setup:

- localized +x-moving Gaussian packet
- barrier plane at fixed `x`
- two slits in the barrier plane
- detector plane one step beyond the barrier

The carrier and geometry were chosen to match the actual transport speed of the current 4-component Dirac walk. A more distant detector plane produced empty outputs and was not diagnostic.

## Channels Tested

1. **Coherent double-slit propagation**
2. **Naive random phase kicks** each layer
3. **Which-path record model**: propagate each slit branch separately and sum probabilities incoherently

## Measured Results

### `n=17`, `steps=16`

- clean detector visibility: `0.5800`
- clean detector proxy: `0.0705`
- phase-kick visibility: `0.5668 +/- 0.0522`
- phase-kick proxy: `0.0678`
- record-model visibility: `0.5663`
- record-model proxy: `0.0707`
- clean vs record L1 residual: `0.9084`
- slit weights `(A,B)`: `(0.017664, 0.017063)`
- slit distinguishability `D`: `0.0173`
- record-mixture purity: `0.5001`
- proxy gap vs mixture purity: `0.4295`
- norms `(clean/noise/record)`: `0.658659 / 0.626148 / 1.207968`

### `n=21`, `steps=20`

- clean detector visibility: `0.5158`
- clean detector proxy: `0.0638`
- phase-kick visibility: `0.5128 +/- 0.0470`
- phase-kick proxy: `0.0575`
- record-model visibility: `0.5411`
- record-model proxy: `0.0638`
- clean vs record L1 residual: `0.9413`
- slit weights `(A,B)`: `(0.012349, 0.011898)`
- slit distinguishability `D`: `0.0186`
- record-mixture purity: `0.5002`
- proxy gap vs mixture purity: `0.4364`
- norms `(clean/noise/record)`: `0.657205 / 0.607673 / 1.207786`

## Interpretation

The important mismatch is between the current-style detector proxy and the actual record-mixture purity:

- the detector proxy stays near `0.06-0.07` across clean, noisy, and record channels
- the record-mixture purity sits at `~0.500`
- the clean-vs-record profile residual is large (`~0.91-0.94`)

That means the existing closure-card "purity" style row is not measuring the same thing as a Dirac which-path record channel. The probe does **not** show a strong architecture-level decoherence failure. It shows that the harness is using a weak proxy that barely moves even when the actual record-mixture purity is exactly what it should be.

The random phase channel is also not a clean discriminator here: the visibility changes only mildly in this compact geometry and is not monotone with phase strength, which is another sign that visibility alone is too crude as the main Dirac decoherence readout.

## Conclusion

For the 4-component Dirac walk, the current closure-card decoherence / purity rows should be redesigned.

Recommended replacement reads:

- use a Dirac-appropriate slit geometry with explicit which-path branches
- report a record-mixture purity or reduced path purity, not just a detector concentration proxy
- keep a separate interference-residual metric to show whether the coherent and incoherent profiles diverge

This probe supports a **harness mismatch** diagnosis, not a clear Dirac architecture failure.
