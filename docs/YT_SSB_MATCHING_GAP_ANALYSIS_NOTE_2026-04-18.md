# Yukawa SSB Matching-Gap Arithmetic Boundary Note

**Date:** 2026-04-18
**Repair date:** 2026-05-06
**Type:** positive_theorem, scoped to exact algebraic identity
**Claim scope:** bounded `H_unit` normalization arithmetic. Given the
unit-normalized scalar-singlet component

```text
H_unit = (1 / sqrt(N_iso * N_c)) * sum_{alpha,a} E_{alpha,a}
```

on the canonical orthonormal pair basis, each single component overlap is
`1 / sqrt(N_iso * N_c)`. For the framework values `(N_iso, N_c) = (2, 3)`,
that value is `1 / sqrt(6)`. If two labels are both explicitly defined to be
this same `H_unit` component overlap, both labels evaluate to `1 / sqrt(6)`.

**Boundary:** this note does not close a retained matching theorem for the
physical Standard Model Yukawa trilinear. In particular, it does not identify
the Ward four-fermion matrix element with the `Qbar_L-H-u_R` trilinear
coefficient. That stronger matching statement would require a separate
tree-level operator-matching theorem deriving the HS/source normalization,
SSB VEV division, chirality projection, LSZ/external-state normalization, and
absence of extra factors from the retained action. Those steps are not derived
here.

**Status authority:** this source note does not set its own audit outcome.
Independent audit must decide the final audit status for the scoped
finite-dimensional theorem.
**Primary runner:** `scripts/frontier_yt_ssb_matching_gap.py`
**Log:** `logs/retained/yt_ssb_matching_gap_2026-04-18.log`

---

## 1. Repair Summary

The earlier version of this note overclaimed that the SSB matching gap was
closed by a Hubbard-Stratonovich / effective-action route and a direct
identical-operator route. The audit correctly objected that this equated two
different readout structures by naming both of them `H_unit`.

This repaired note keeps only the part that is actually proved by the local
algebra:

```text
<alpha_0,a_0 | H_unit | alpha_0,a_0>
  = 1 / sqrt(N_iso * N_c).
```

At `(N_iso, N_c) = (2, 3)`, the result is `1 / sqrt(6)`. This is exact
finite-dimensional arithmetic. It is not a physical SSB matching theorem.

---

## 2. Definitions

Let

```text
D = N_iso * N_c
```

with `N_iso, N_c` positive integers. Let the pair Hilbert space have
orthonormal basis

```text
|alpha,a>,  1 <= alpha <= N_iso,  1 <= a <= N_c.
```

Let `E_{alpha,a}` be the diagonal Wick-contractor / matrix-unit operator that
acts as the identity on the basis pair `|alpha,a>` and as zero on all other
basis pairs:

```text
<beta,b | E_{alpha,a} | beta,b> =
  1, if (beta,b) = (alpha,a),
  0, otherwise.
```

The scoped operator in this note is

```text
H_unit = (1 / sqrt(D)) * sum_{alpha=1..N_iso} sum_{a=1..N_c} E_{alpha,a}.
```

Equivalently, in this basis,

```text
H_unit = (1 / sqrt(D)) * I_D.
```

For the framework instance used in the original note,

```text
N_iso = 2,  N_c = 3,  D = 6,
H_unit = (1 / sqrt(6)) * I_6.
```

---

## 3. Theorem

For any basis pair `|alpha_0,a_0>`,

```text
F(alpha_0,a_0)
  := <alpha_0,a_0 | H_unit | alpha_0,a_0>
   = 1 / sqrt(N_iso * N_c).                                      (T1)
```

For `(N_iso, N_c) = (2, 3)`,

```text
F(alpha_0,a_0) = 1 / sqrt(6).                                    (T2)
```

If two quantities are defined as aliases of this same component overlap,
for example

```text
A := F(alpha_0,a_0),
B := F(alpha_0,a_0),
```

then

```text
A = B = 1 / sqrt(6)
```

in the framework instance. This last equality is only an alias equality inside
the finite-dimensional `H_unit` arithmetic. It carries no independent
operator-matching content.

---

## 4. Proof

By definition,

```text
<alpha_0,a_0 | H_unit | alpha_0,a_0>
  = <alpha_0,a_0 |
      (1 / sqrt(D)) * sum_{alpha,a} E_{alpha,a}
    | alpha_0,a_0>
```

Linearity gives

```text
= (1 / sqrt(D)) *
  sum_{alpha,a}
  <alpha_0,a_0 | E_{alpha,a} | alpha_0,a_0>.
```

All summands vanish except the one with `(alpha,a) = (alpha_0,a_0)`, and that
summand equals `1` by the canonical basis-pair normalization. Therefore

```text
<alpha_0,a_0 | H_unit | alpha_0,a_0>
  = (1 / sqrt(D)) * 1
  = 1 / sqrt(D)
  = 1 / sqrt(N_iso * N_c).
```

Substituting `(N_iso, N_c) = (2, 3)` gives `D = 6` and hence
`1 / sqrt(6)`.

No gauge coupling, source normalization, SSB VEV, LSZ residue, chirality
projector, or physical Yukawa readout map appears in this proof. The theorem
is exactly the component-overlap arithmetic of the stated operator.

---

## 5. What This Claims

- The finite-dimensional identity `(T1)` for any positive `N_iso, N_c`.
- The framework arithmetic instance `(N_iso, N_c) = (2, 3)` gives
  `1 / sqrt(6)`.
- Two labels defined as the same `H_unit` component overlap evaluate to the
  same number.
- The scoped overlap expression contains no gauge-coupling parameter and no
  SSB/readout normalization symbol.

---

## 6. What This Does Not Claim

- Does not derive the physical Yukawa trilinear coefficient.
- Does not close the SSB matching gap.
- Does not prove a Hubbard-Stratonovich normalization theorem.
- Does not divide by or derive an EWSB VEV normalization.
- Does not perform a chirality projection from the scalar-singlet bilinear to
  the `Qbar_L-H-u_R` Standard Model monomial.
- Does not derive LSZ or external-state normalization factors.
- Does not prove that no additional finite, sign, color, chirality, source, or
  field-normalization factors enter the physical trilinear readout.
- Does not use observed masses, PDG values, fitted selectors, or admitted unit
  conventions.

The physical matching problem remains open until those ingredients are
derived by a separate retained action-level operator-matching theorem.

---

## 7. Relation To The Ward And Class 5 Notes

`docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` is the parent authority for the
framework's `H_unit` definition and for its Ward-side use. This note does not
rederive that parent theorem; it isolates the local arithmetic consequence of
the normalized operator once the definition is stated.

`docs/YT_CLASS_5_NON_QL_YUKAWA_VERTEX_NOTE_2026-04-18.md` discusses
non-`Q_L` Yukawa trilinear Clebsch-Gordan factors. This note does not certify
that the Class 5 trilinear coefficient is the same Green-function object as the
Ward four-fermion coefficient. It only records that the same numerical
`1 / sqrt(6)` appears when a readout is explicitly defined to be the same
`H_unit` component overlap.

---

## 8. Audit Repair Mapping

Auditor objection:

```text
The Ward 4-fermion channel and the physical trilinear are both matrix
elements of H_unit; they share the 1/sqrt(6) coefficient by construction.
```

Repair:

1. The theorem statement now removes the physical trilinear from the claimed
   result.
2. The proof derives only the diagonal matrix element of
   `H_unit = I_D / sqrt(D)` on an orthonormal pair basis.
3. Any two-name equality is explicitly identified as alias arithmetic, not as
   physical operator matching.
4. The missing physical steps named by the audit are listed as open boundary
   conditions rather than silently passed.

The intended re-audit scope is therefore:

```text
Given H_unit = I_(N_iso*N_c) / sqrt(N_iso*N_c), the diagonal component
overlap equals 1 / sqrt(N_iso*N_c); at (2,3) it equals 1 / sqrt(6).
```

---

## 9. Validation

Primary runner: `scripts/frontier_yt_ssb_matching_gap.py`.

The repaired runner verifies:

1. positive integer dimensions and `D = N_iso * N_c`;
2. the framework instance `D = 6`;
3. explicit matrix form `H_unit = I_6 / sqrt(6)`;
4. diagonal component overlaps are all `1 / sqrt(6)`;
5. off-diagonal overlaps are zero;
6. two labels defined as the same component overlap are numerically equal;
7. alternative dimensions `(3,4)` give `1 / sqrt(12)`;
8. the degenerate dimension `(1,1)` gives `1`;
9. the proof expression contains no `g_bare`, `y_t_phys`, `V_EWSB`,
   `Z_LSZ`, `P_chiral`, or HS source-normalization symbol;
10. the runner outcome explicitly says the SSB matching theorem remains open.

The runner is intentionally an arithmetic verifier, not a physical matching
verifier.

---

## 10. Cross-References

- `docs/YT_WARD_IDENTITY_DERIVATION_THEOREM.md` - parent Ward/H_unit note.
- `docs/YT_CLASS_5_NON_QL_YUKAWA_VERTEX_NOTE_2026-04-18.md` - separate
  trilinear Clebsch-Gordan discussion, not certified by this note.
- `docs/UNIT_SINGLET_OVERLAP_NARROW_THEOREM_NOTE_2026-05-02.md` - sibling
  narrow arithmetic theorem with the same finite-dimensional overlap core.
