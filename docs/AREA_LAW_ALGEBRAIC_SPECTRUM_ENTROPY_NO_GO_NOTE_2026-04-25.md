# Area-Law Algebraic-Spectrum Entropy No-Go Note

**Date:** 2026-04-25
**Status:** bounded - bounded or caveated result note
**Runner:** `scripts/frontier_area_law_algebraic_spectrum_entropy_no_go.py`

## Purpose

The primitive-edge no-go shows that the direct finite-cell entropy
constructions from the `16`-state primitive cell do not give `1/4`. This note
adds a stronger number-theoretic obstruction: an exact finite-dimensional
gapped edge carrier with algebraic Schmidt spectrum cannot have nonzero von
Neumann entropy exactly equal to the algebraic number `1/4`.

This matters because exact finite `Cl(3)`/projector constructions naturally
produce rational or algebraic spectra. If Target 2 is to be closed by an
ordinary von Neumann entanglement carrier with coefficient `1/4`, the carrier
must introduce a transcendental Schmidt-spectrum selector or use a different
operational entropy functional.

## The lemma

Let a primitive edge have a finite Schmidt spectrum

```text
lambda = (lambda_1, ..., lambda_n),
lambda_i >= 0,
sum_i lambda_i = 1,
```

with every nonzero `lambda_i` algebraic. Its von Neumann entropy is

```text
S(lambda) = - sum_i lambda_i log(lambda_i).
```

By Baker's theorem on linear forms in logarithms of algebraic numbers, any
nonzero linear form in logarithms of algebraic numbers with algebraic
coefficients cannot be algebraic. Since `S(lambda)` is such a linear form and
`S(lambda)>0` for a non-product spectrum, `S(lambda)` is transcendental.

Therefore:

```text
S(lambda) = 1/4
```

is impossible for any nonzero algebraic finite Schmidt spectrum, because
`1/4` is algebraic.

The zero-entropy product spectrum is algebraic, but gives `S=0`, not `1/4`.

## Consequences

1. **Finite projector/rank spectra.** Flat rank spectra give `S=log r`, and
   rational block spectra give rational linear combinations of `log` of
   rationals. These are either zero or transcendental, never `1/4`.

2. **Exact algebraic gapped Hamiltonians.** A finite local Hamiltonian with
   algebraic entries has algebraic spectral data after solving its finite
   characteristic equations. If the resulting reduced density spectrum is
   algebraic, the exact entropy cannot be `1/4` unless it is zero.

3. **The tuned two-level edge parameter is necessarily non-algebraic.** The
   primitive-edge no-go identified the unique `p_* in (0,1/2)` with
   `H_binary(p_*)=1/4`. This lemma shows that `p_*` cannot be algebraic. It is
   an analytic selector, not a finite `Cl(3)` rank datum.

4. **The Planck trace is not rescued by algebraic Schmidt spectra.** The exact
   primitive coefficient `4/16` is algebraic because it is a trace/rank
   fraction. Ordinary finite-cell von Neumann entropy from algebraic spectra
   lives in a different number class.

## What remains open

A positive Target 2 theorem must now do one of the following:

- derive the required transcendental Schmidt-spectrum selector from a retained
  physical principle;
- derive a multipocket Widom selector instead of a finite gapped-edge spectrum;
- or define and justify a non-von-Neumann primitive-boundary entropy functional
  for which the trace `Tr((I_16/16)P_A)` is operationally the entropy.

Without one of those steps, exact `1/4` remains an action/counting coefficient,
not a derived entanglement-entropy coefficient.

## Relation to previous Target 2 branches

This note is compatible with:

- the retained single-carrier Widom no-go (`c_Widom=1/6`);
- the simple-fiber broader Widom no-go (`c_Widom<=1/6`);
- the multipocket selector no-go (quarter requires an extra crossing-measure
  selector);
- the primitive-edge entropy selector no-go (canonical finite-cell entropies
  from `(16,4)` miss `1/4`).

It strengthens the last item by showing that the obstruction is not just the
handful of tested spectra: the whole algebraic finite-spectrum class misses
`1/4`.

## Literature anchor

The number-theoretic input is Baker's theorem on linear forms in logarithms of
algebraic numbers, beginning with:

- Alan Baker, "Linear forms in the logarithms of algebraic numbers,"
  Mathematika 13, 204-216 (1966), and follow-up papers.

The relevant consequence used here is that a non-vanishing linear form, with
algebraic coefficients, in logarithms of algebraic numbers cannot be algebraic.

## Package wording

Safe wording:

> Any exact finite-dimensional primitive-edge von Neumann entropy carrier with
> algebraic Schmidt spectrum has entropy either zero or transcendental by
> Baker's theorem. Since `1/4` is algebraic, such a carrier cannot deliver the
> Bekenstein-Hawking coefficient exactly. A positive gapped Target 2 result
> must derive a transcendental Schmidt-spectrum selector or use a justified
> non-von-Neumann primitive entropy.

Unsafe wording:

> No finite or gapped entanglement carrier can ever give `1/4`.

## Verification

Run:

```bash
python3 scripts/frontier_area_law_algebraic_spectrum_entropy_no_go.py
```

The runner checks representative algebraic spectra, the Baker-theorem
certificate conditions, the tuned two-level selector, and the separation
between algebraic primitive traces and von Neumann entropy values.

Current output:

```text
SUMMARY: PASS=38  FAIL=0
```
