# Quark `C3` A1 Source-Domain Bridge No-Go Note

**Date:** 2026-04-28

**Status:** exact current-bank no-go / support-boundary theorem for Lane 3
target 3C. This block-08 artifact audits whether existing Koide A1 support
can be typed into the quark `C3` circulant source ratio. It does not claim
retained `m_u`, `m_d`, `m_s`, `m_c`, or `m_b`.

**Primary runner:**
`scripts/frontier_quark_c3_a1_source_domain_bridge_no_go.py`

## 1. Question

Block 07 isolated the next `C3` source-law residual:

```text
derive A1 or an equivalent quark Ward source ratio for
H(a,q) = a I + q C + conjugate(q) C^2.
```

The inherited Koide lane already has strong A1 support. Several exact faces
collapse to the same scalar:

```text
P_Q = |q|^2 / a^2 = 1/2.
```

Those faces include equal cyclic block power, real-irrep-block democracy,
the `SU(2)_L` fundamental-weight norm, a Clifford spinor/even-Clifford
dimension ratio, and the charged-lepton Koide `Q = 2/3` bridge.

This block asks the quark-specific source-domain question:

```text
Does the current repo support bank already contain a typed bridge from those
A1 support scalars to the quark C3 Ward source ratio |q_quark|^2/a_quark^2
= 1/2?
```

## 2. Minimal Premise Set

Allowed premises:

1. retained `hw=1` generation triplet;
2. exact induced `C3[111]` cycle on the generation triplet;
3. exact Hermitian circulant algebra;
4. exact Koide/A1 scalar identities as support faces;
5. one-Higgs Yukawa gauge-selection theorem as a boundary on allowed Yukawa
   terms.

Forbidden proof inputs:

1. observed quark masses;
2. fitted Yukawa entries;
3. CKM mixing data treated as mass-eigenvalue input;
4. charged-lepton A1 physical bridge imported as if species-universal;
5. a hidden assertion that the quark Ward source extremizes the charged-lepton
   block-total Frobenius functional.

## 3. Exact A1 Algebra

For the `C3` Hermitian circulant family, write `r = |q|`. The eigenvalue
triple has invariant

```text
Q = (sum lambda_k^2) / (sum lambda_k)^2
  = 1/3 + 2 r^2/(3 a^2).
```

Thus A1 is exactly:

```text
r^2/a^2 = 1/2
<=> Q = 2/3.
```

Equivalently, with cyclic block powers

```text
E_plus = 3 a^2,
E_perp = 6 r^2,
```

A1 is exactly `E_plus = E_perp`. This is the same algebra used in the Koide
support lane.

## 4. Source-Domain Inventory

The current support bank contains exact internal A1 faces:

| Source face | Exact scalar | Current domain |
|---|---:|---|
| cyclic block power / real-irrep-block democracy | `1/2` | Koide/charged-lepton circulant support |
| `dim(spinor) / dim(Cl^+(3))` | `1/2` | Clifford / electroweak support face |
| `|omega_SU(2),fund|^2` | `1/2` | Lie-theoretic support face |
| charged-lepton `P_Q` | `1/2` | charged-lepton amplitude carrier |

The current bank also contains exact quark-side facts:

| Quark-side item | Current domain |
|---|---|
| retained `hw=1` generation triplet and `C3[111]` cycle | generation carrier |
| Hermitian `C3` circulant normal form | Ward/source carrier |
| one-Higgs Yukawa gauge selection | allowed Yukawa skeleton |

What is missing is a typed bridge:

```text
A1 support scalar 1/2
=> physical quark Ward source ratio |q_quark|^2/a_quark^2 = 1/2.
```

Without that edge, the equality of numbers is only a support coincidence. It
does not identify the physical source domain.

## 5. Theorem

**Theorem (`C3` A1 source-domain bridge no-go).** In the current Lane 3
support bank, the Koide A1 scalar `1/2` is exactly represented by several
internal support faces, and the quark `C3` circulant carrier has an exact A1
target ratio `|q|^2/a^2 = 1/2`. However, there is no typed existing edge from
the support scalar to the physical quark Ward source ratio. Adding such an
edge would create the desired A1 quark source law, so that edge is new theorem
content rather than latent support. Therefore Koide A1 support cannot be
promoted to retained quark Ward closure in this block.

## 6. What This Retires

This retires the direct promotion:

```text
Koide A1 support scalar = 1/2
=> quark C3 source ratio |q_quark|^2/a_quark^2 = 1/2
=> retained quark generation Ward identities.
```

The scalar match is exact support, not a retained quark source theorem.

## 7. What Remains Open

Lane 3 remains open. A future route can reopen this target only by supplying
one of:

1. a physical theorem that the quark Ward source extremizes the same
   block-total Frobenius functional;
2. a quark-specific Clifford/electroweak source-domain map from the `1/2`
   support scalar to `|q_quark|^2/a_quark^2`;
3. an alternate source ratio replacing A1;
4. a P1-style positive parent/readout theorem plus sector phase and scale
   laws that make A1 unnecessary.

## 8. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_c3_a1_source_domain_bridge_no_go.py
```

Expected result:

```text
TOTAL: PASS=50, FAIL=0
VERDICT: current A1 support has no typed bridge to the quark C3 source ratio.
```
