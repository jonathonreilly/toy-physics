# YT Color-Singlet Zero-Mode Cancellation Note

**Date:** 2026-05-01  
**Status:** exact-support / color-singlet gauge-zero-mode cancellation  
**Runner:** `scripts/frontier_yt_color_singlet_zero_mode_cancellation.py`  
**Certificate:** `outputs/yt_color_singlet_zero_mode_cancellation_2026-05-01.json`

## Purpose

The previous scalar-denominator blocks isolated the massless gauge zero mode as
a load-bearing obstruction.  This block checks the color algebra of that exact
mode in the scalar `q qbar` singlet channel.

## Theorem

A spatially constant gauge mode couples to total color charge.  For the
normalized singlet

```text
|S> = 1/sqrt(3) sum_i |i anti-i>,
```

the total color generator satisfies

```text
(T_q^a + T_qbar^a) |S> = 0
```

for every SU(3) generator.

Equivalently, the zero-mode self and exchange pieces cancel:

```text
<S| T_q^2 |S>       = C_F
<S| T_qbar^2 |S>    = C_F
2 <S| T_q T_qbar |S> = -2 C_F
sum = 0
```

## Runner Result

```text
python3 scripts/frontier_yt_color_singlet_zero_mode_cancellation.py
# SUMMARY: PASS=7 FAIL=0
```

The runner verifies SU(3) generator normalization, exact singlet charge
annihilation, cancellation of self plus exchange zero-mode pieces, and that an
octet state does not cancel in the same way.

## Claim Boundary

This is exact support, not retained closure.  It says an exchange-only finite
ladder that keeps the `q=0` gauge mode is not the correct color-neutral
singlet scalar denominator.  It does not derive the finite-`q` IR behavior,
the interacting scalar pole, the inverse-propagator derivative, projector /
source normalization, finite-`N_c=3` continuum control, or production FH/LSZ
evidence.
