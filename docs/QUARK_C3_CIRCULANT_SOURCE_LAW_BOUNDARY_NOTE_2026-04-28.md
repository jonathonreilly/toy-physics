# Quark `C3` Circulant Source-Law Boundary Note

**Date:** 2026-04-28

**Status:** exact support/boundary theorem for Lane 3 target 3C. This
block-07 artifact audits whether the existing `C3[111]` circulant
generation-hierarchy mechanism can be imported as retained non-top quark
Yukawa Ward identities. It does not claim retained `m_u`, `m_d`, `m_s`,
`m_c`, or `m_b`.

**Primary runner:**
`scripts/frontier_quark_c3_circulant_source_law_boundary.py`

## 1. Question

Block 06 proved the exact local `C3` Ward normal form on the retained `hw=1`
generation triplet:

```text
H = a I + q C + conjugate(q) C^2,
```

with `a in R` and `q in C`. Older retained-analysis notes already record the
important correction that this circulant family has distinct Fourier-basis
eigenvalues and is therefore a real hierarchy carrier. They also identify the
non-retained inputs that would make the charged-lepton Koide route predictive:

```text
A1: |q|^2 / a^2 = 1/2     (Frobenius/equal-block-energy selection)
P1: eigenvalues of H are one-leg amplitudes sqrt(m), not masses themselves
```

This block asks the quark-specific question:

```text
Can the C3 circulant mechanism plus A1/P1 be treated as retained quark Ward
source law for y_u/y_t, y_c/y_t, y_d/y_t, y_s/y_t, y_b/y_t?
```

## 2. Minimal Premise Set

Allowed premises:

1. retained `hw=1` generation triplet;
2. exact induced `C3[111]` cycle on that triplet;
3. exact Hermitian circulant normal form;
4. inherited `C3` Fourier-basis hierarchy support from
   `YT_GENERATION_HIERARCHY_PRIMITIVE_ANALYSIS_NOTE_2026-04-18.md` and
   `YT_CLASS_6_C3_BREAKING_OPERATOR_NOTE_2026-04-18.md`;
5. inherited Koide circulant bridge facts only as support, with A1 and P1
   kept as open primitives.

Forbidden proof inputs:

1. observed quark masses;
2. fitted Yukawa entries;
3. CKM mixing data treated as mass-eigenvalue input;
4. importing charged-lepton Koide phase/scale/readout into quarks as if it
   were species-universal retained structure;
5. treating A1 or P1 as already retained for Lane 3.

## 3. Exact Circulant Degrees Of Freedom

The eigenvalues of

```text
H(a,q) = a I + q C + conjugate(q) C^2
```

are

```text
lambda_k = a + 2 |q| cos(arg(q) + 2 pi k / 3),  k = 0,1,2.
```

This map is not predictive by itself. For every real eigenvalue triple
`(lambda_0, lambda_1, lambda_2)` there is a unique Hermitian circulant with
that spectrum:

```text
a = (lambda_0 + lambda_1 + lambda_2)/3,
q = Fourier_1(lambda)/3.
```

So the exact `C3` circulant family is a carrier, not a source law. It can
represent an arbitrary real generation spectrum unless an additional
selection theorem constrains `a` and `q`.

## 4. What A1 Adds And Does Not Add

A1 imposes the equal-block-energy / Frobenius ratio

```text
3 a^2 = 6 |q|^2.
```

If the eigenvalues are read as square-root amplitudes, this implies

```text
Q = sum(lambda_k^2) / (sum(lambda_k))^2 = 2/3,
```

independently of the phase `arg(q)`. Therefore A1 is a real and useful
one-relation source candidate, but it still leaves:

1. the overall scale `a`;
2. the phase `arg(q)`, which controls the ordered hierarchy;
3. the P1 readout identifying eigenvalues with one-leg amplitudes;
4. the species map for up-type versus down-type quark Ward channels.

These are exactly the quantities Lane 3 needs for non-top quark masses.

## 5. Quark-Sector Boundary

For Lane 3 target 3C, a retained quark Ward source law would need to explain
at least:

```text
up sector:    y_u/y_t, y_c/y_t
down sector:  y_d/y_t, y_s/y_t, y_b/y_t
```

The `C3` circulant carrier by itself is species-blind. If the same normalized
circulant spectrum is used for every species, then all species inherit the
same normalized generation hierarchy. If separate phases/scales are allowed
for up and down sectors, those phases/scales are new species source data.

Thus the exact boundary is:

```text
C3 circulant support + A1/P1 does not become retained quark Ward closure
until a quark-specific source/readout theorem supplies the species phases,
relative scales, and amplitude-vs-Yukawa dictionary.
```

## 6. Theorem

**Theorem (`C3` circulant source-law boundary).** On the retained Lane 3
`hw=1` generation surface, the exact `C3[111]` Hermitian circulant family is a
valid Fourier-basis hierarchy carrier. Without A1/P1 or an equivalent
source/readout theorem, it is three-real-dimensional and can fit any real
generation spectrum, so it is not predictive. With A1 and P1, it supplies the
Koide-style relation `Q=2/3` for an amplitude triple but still leaves the
scale, phase, species assignment, and quark Yukawa readout open. Therefore the
existing `C3` circulant mechanism is exact support for a future 3C theorem,
not retained non-top quark mass closure.

## 7. What This Retires

This retires the direct promotion:

```text
retained C3 circulant hierarchy support
=> retained quark generation-stratified Ward identities.
```

The support is real, but Lane 3 still needs a quark-specific source/readout
theorem.

## 8. What Remains Open

Lane 3 remains open. The next 3C theorem target is one of:

1. derive A1 or an equivalent ratio for the quark Ward source;
2. derive a P1-style positive parent/readout for quark Yukawa amplitudes;
3. derive sector-specific phases and relative scales for up/down quarks;
4. prove a stronger no-go showing that the `C3` circulant route cannot supply
   quark Ward identities under any admissible source/readout primitive.

## 9. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_c3_circulant_source_law_boundary.py
```

Expected result:

```text
TOTAL: PASS=43, FAIL=0
VERDICT: C3 circulants are exact hierarchy carriers, but A1/P1 plus
quark-specific species source/readout laws remain load-bearing.
```
