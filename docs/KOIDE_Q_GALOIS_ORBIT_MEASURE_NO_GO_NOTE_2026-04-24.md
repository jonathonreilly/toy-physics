# Koide Q Galois-orbit measure no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_galois_orbit_measure_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use the real/Galois orbit structure of the complex `C_3` characters to derive
equal real-block weights.

The complex characters are

```text
0, 1, 2.
```

Complex conjugation gives two real orbits:

```text
{0}, {1,2}.
```

Counting those two orbits equally would give equal real blocks and hence
`K_TL=0`.

## Executable theorem

Two natural Galois-invariant measures disagree:

```text
push-forward of uniform complex-character measure: (1/3, 2/3)
uniform measure on the orbit set:                 (1/2, 1/2)
```

The push-forward measure is rank/character-count weighting and gives `Q=1`,
nonzero `K_TL`.  The uniform orbit-label measure lands on the Koide leaf, but
it is an extra measure choice.

A size-exponent family makes the residual explicit:

```text
weights({0},{1,2}) proportional to (1^s, 2^s)
R(s) = 2^s.
```

Equal real blocks require

```text
s = 0.
```

The character push-forward is `s=1`.

## Residual

```text
RESIDUAL_SCALAR = size_exponent_s_equals_0_equiv_K_TL
RESIDUAL_ORBIT_MEASURE = size_exponent_s_equals_0_equiv_K_TL
```

## Why this is not closure

Galois invariance identifies the two nontrivial complex characters as one real
orbit.  It does not decide whether physics counts orbit labels equally or
pushes forward the uniform measure on complex characters.  The former closes
Q; the latter is retained rank/fusion-compatible and does not.

## Falsifiers

- A retained theorem proving the charged-lepton source measures real Galois
  orbit labels with exponent `s=0`.
- A physical argument rejecting character-count push-forward despite retained
  rank/fusion data.
- A source theorem where the Galois quotient itself supplies a normalized
  measure, not merely an orbit set.

## Boundaries

- The runner covers complex `C_3` character orbits under real conjugation,
  push-forward character measure, uniform orbit measure, and the orbit-size
  exponent family.
- It does not exclude a future physical orbit-measure postulate; it isolates
  that postulate as the residual.

## Hostile reviewer objections answered

- **"There are two real orbits, so use half and half."**  That is one valid
  orbit measure, but not the push-forward of the retained complex character
  measure.
- **"Galois invariance should be enough."**  Both measures are Galois
  invariant.  Invariance alone does not select `s=0`.
- **"Does orbit counting support Q?"**  Yes as a candidate primitive.  It is
  not a derivation without the physical orbit-measure theorem.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_galois_orbit_measure_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_Q_GALOIS_ORBIT_MEASURE_NO_GO=TRUE
Q_GALOIS_ORBIT_MEASURE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=size_exponent_s_equals_0_equiv_K_TL
RESIDUAL_ORBIT_MEASURE=size_exponent_s_equals_0_equiv_K_TL
```
