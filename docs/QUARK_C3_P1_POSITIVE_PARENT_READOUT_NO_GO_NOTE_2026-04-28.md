# Quark `C3` P1 Positive-Parent Readout No-Go Note

**Date:** 2026-04-28

**Status:** exact current-bank no-go / support-boundary theorem for Lane 3
target 3C. This block-09 artifact audits whether the repo's existing
positive-parent square-root dictionary can be promoted into a retained quark
Yukawa readout theorem. It does not claim retained `m_u`, `m_d`, `m_s`,
`m_c`, or `m_b`.

**Primary runner:**
`scripts/frontier_quark_c3_p1_positive_parent_readout_no_go.py`

## 1. Question

Blocks 07 and 08 separated two load-bearing imports for the `C3` circulant
source-law route:

```text
A1: |q|^2/a^2 = 1/2 or an equivalent source ratio.
P1: eigenvalues of the C3 circulant source are one-leg Yukawa amplitudes,
    not arbitrary mass, mass-squared, or support coordinates.
```

The Koide square-root note already gives a strong exact dictionary:

```text
positive C3-covariant parent M
=> principal square root Y = M^(1/2)
=> eig(Y) = sqrt(eig(M)).
```

This block asks the Lane 3 version:

```text
Does the current support bank already supply a positive quark C3 parent M and
a retained readout theorem identifying eig(M^(1/2)) with physical quark
Yukawa amplitudes?
```

## 2. Minimal Premise Set

Allowed premises:

1. retained `hw=1` generation triplet;
2. exact induced `C3[111]` cycle on the generation triplet;
3. exact Hermitian `C3` circulant algebra;
4. exact finite-dimensional positive square-root theorem;
5. existing Koide P1 support as a square-root dictionary;
6. one-Higgs Yukawa gauge selection as a boundary on allowed Yukawa terms.

Forbidden proof inputs:

1. observed quark masses;
2. fitted Yukawa entries;
3. CKM mixing data treated as mass-eigenvalue input;
4. charged-lepton positive parent imported as species-universal;
5. a hidden assertion that the physical quark Yukawa operator is already the
   principal square root of a retained positive `C3` parent.

## 3. Exact Square-Root Algebra

If `M` is a positive Hermitian parent and `[M,C]=0`, then finite-dimensional
functional calculus gives a unique positive square root:

```text
Y = M^(1/2),
Y^2 = M,
[Y,C] = 0,
eig(Y) = sqrt(eig(M)).
```

This is exact and useful. It supplies the right mathematical form for a P1
theorem if a physical parent `M` has already been derived.

However, this algebra is not a source law. For every positive amplitude triple
`s = (s_0,s_1,s_2)`, there is a positive `C3` parent

```text
M = F diag(s_0^2,s_1^2,s_2^2) F^*
```

whose square root has eigenvalues `s`. Therefore the positive-parent
dictionary can represent any positive generation-amplitude spectrum unless a
separate theorem derives the parent or the readout.

## 4. Current-Bank Boundary

The current support bank contains:

| Surface | What it supplies | What it does not supply |
|---|---|---|
| positive square-root dictionary | `M -> M^(1/2)` once `M` is positive | physical quark parent `M` |
| `C3` circulant carrier | Fourier-basis hierarchy carrier | amplitude-vs-Yukawa readout |
| one-Higgs gauge selection | allowed Dirac Yukawa monomials | generation eigenvalues or parent positivity |
| Koide P1 support | charged-lepton square-root route narrowing | species-universal quark readout |

Two typed edges remain missing:

```text
quark Yukawa source domain
=> positive C3-covariant parent M_quark

eig(M_quark^(1/2))
=> physical quark Yukawa amplitudes.
```

Without both edges, P1 is support-only for Lane 3.

## 5. Theorem

**Theorem (`C3` P1 positive-parent readout no-go).** In the current Lane 3
support bank, the positive-parent square-root dictionary is exact: a positive
`C3`-covariant parent has a positive `C3`-covariant square root with
square-root eigenvalues. But the current bank does not derive a physical quark
positive parent and does not identify the square-root spectrum with quark
Yukawa amplitudes. Since the dictionary can represent arbitrary positive
generation-amplitude triples once a parent is supplied, it is not predictive by
itself. Therefore P1 cannot be promoted to retained quark Ward closure in this
block.

## 6. What This Retires

This retires the direct promotion:

```text
repo square-root dictionary
=> retained quark P1 readout
=> retained quark generation Ward identities.
```

The dictionary is exact support; the quark parent and readout theorem remain
new source/readout content.

## 7. What Remains Open

Lane 3 remains open. A future route can reopen P1 by supplying:

1. a retained positive `C3` parent for quark Yukawa amplitudes;
2. a readout theorem identifying `eig(M^(1/2))` with physical quark Yukawa
   amplitudes;
3. sector-specific phase and relative-scale laws for up/down quarks;
4. an alternate readout route that bypasses P1;
5. a full no-go showing no admissible positive-parent quark readout can exist
   under the current primitive set.

## 8. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_c3_p1_positive_parent_readout_no_go.py
```

Expected result:

```text
TOTAL: PASS=54, FAIL=0
VERDICT: square-root algebra is exact support, but quark P1 parent/readout
requires new theorem content.
```
