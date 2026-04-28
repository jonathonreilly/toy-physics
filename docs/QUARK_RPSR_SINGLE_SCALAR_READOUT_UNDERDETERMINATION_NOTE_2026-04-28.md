# Quark RPSR Single-Scalar Readout Underdetermination Note

**Date:** 2026-04-28

**Status:** exact no-go / boundary theorem for Lane 3 target 3B. This
block-11 artifact sharpens the block-10 RPSR support result by testing whether
one exact reduced up-amplitude scalar can determine the two independent
up-type Yukawa ratios. It does not claim retained `m_u`, `m_c`, `m_u/m_c`, or
`m_c/m_t`.

**Primary runner:**
`scripts/frontier_quark_rpsr_single_scalar_readout_underdetermination.py`

## 1. Question

Block 10 established exact retained support for the reduced RPSR up-amplitude

```text
a_u = sqrt(5/6) * (1 - 48/(49 sqrt(42))).
```

The remaining 3B mass-retention question is sharper:

```text
Can this single reduced scalar, together with the top Ward anchor, determine
both physical up-type ratios y_u/y_c and y_c/y_t without adding an independent
readout law?
```

## 2. Minimal Premise Set

Allowed premises:

1. the exact RPSR reduced amplitude `a_u` from the block-10 theorem;
2. positivity and generation ordering for an up-type Yukawa triple after a
   top-scale normalization;
3. scale covariance: changing the absolute top anchor rescales the whole
   triple but does not change the two ratios;
4. no observed quark masses, no fitted Yukawa entries, and no CKM singular
   values treated as mass inputs.

Forbidden proof inputs:

1. a hidden exponent or functional readout law selected from observed ratios;
2. a hidden generation label assigning the RPSR scalar to one particular
   singular-value gap;
3. species-uniform reuse of the top Ward normalization for non-top masses;
4. endpoint-distance or nearest-rational selection not supplied as a theorem.

## 3. Exact Readout Test Class

After the top scale is factored out, a positive ordered up-type triple has two
dimensionless ratios:

```text
r_uc = y_u/y_c,
r_ct = y_c/y_t.
```

A single reduced scalar `a_u` can only become a mass-ratio prediction after a
readout theorem specifies how the two ratio functions are built from it. The
minimal scale-covariant power readout class already exposes the issue:

```text
R_{p,q}(a_u; y_t) = y_t * (a_u^(p+q), a_u^q, 1),
```

with `p > 0` and `q > 0`. It obeys positivity, ordering, and scale covariance
for `0 < a_u < 1`, and it gives

```text
y_u/y_c = a_u^p,
y_c/y_t = a_u^q.
```

The exact RPSR amplitude fixes `a_u`; it does not fix `p` or `q`.

## 4. Lemma: Continuum Of Ratio Readouts

For fixed `a_u` in `(0, 1)`, the family `R_{p,q}` contains a continuum of
ordered, scale-covariant triples with the same RPSR scalar and different
ratio pairs. For example:

```text
R_{1,1}: (a_u^2, a_u, 1),
R_{2,1}: (a_u^3, a_u, 1),
R_{1,2}: (a_u^3, a_u^2, 1).
```

All three use the same exact RPSR scalar. They disagree on at least one of
`y_u/y_c` or `y_c/y_t`.

## 5. Lemma: Fit-Capacity Is Not Prediction

The same power class can represent any synthetic ordered ratio pair in
`(0, 1) x (0, 1)`:

```text
p = log(r_uc) / log(a_u),
q = log(r_ct) / log(a_u).
```

Because `0 < a_u < 1`, positive `r_uc` and `r_ct` below one give positive
`p` and `q`. This is useful as a readout grammar test, but it is not a
prediction. Selecting `p` and `q` is exactly the missing readout theorem.

## 6. Theorem

**Theorem (RPSR single-scalar readout underdetermination).** The exact
STRC/RPSR reduced amplitude

```text
a_u = sqrt(5/6) * (1 - 48/(49 sqrt(42)))
```

does not, together with top-scale normalization and scale covariance, determine
the two independent physical up-type Yukawa ratios. Within the admissible
scale-covariant power readout class, the same `a_u` supports a continuum of
ordered ratio pairs. Therefore any promotion from RPSR reduced amplitude to
retained `m_u/m_c` and `m_c/m_t` must add a retained readout law fixing the
two ratio functions or their equivalent exponents, plus a sector/scale bridge
to the top Ward anchor.

## 7. What This Retires

This retires the stronger shortcut:

```text
RPSR reduced amplitude a_u
+ top Ward scale
=> retained up-type ratio pair.
```

The block-10 amplitude theorem remains valuable exact support. The block-11
result proves that a single-scalar readout is underdetermined unless the
readout functions themselves are derived.

## 8. What Remains Open

Lane 3 remains open. A future 3B route can still move the claim state by
supplying:

1. a retained readout theorem that fixes `p` and `q` or replaces the power
   grammar with an equally explicit two-ratio map;
2. a generation/source theorem assigning the two readout functions to the
   physical `u,c,t` singular-value gaps;
3. a top-compatible sector/scale bridge;
4. a proof that the readout is compatible with the existing 3C and CKM
   boundary notes.

## 9. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_rpsr_single_scalar_readout_underdetermination.py
```

Expected result:

```text
TOTAL: PASS=80, FAIL=0
VERDICT: exact RPSR scalar support remains underdetermined as a two-ratio
up-type Yukawa readout without a new readout theorem.
```
