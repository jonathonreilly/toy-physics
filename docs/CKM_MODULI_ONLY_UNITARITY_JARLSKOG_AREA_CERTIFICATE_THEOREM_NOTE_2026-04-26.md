# CKM Moduli-Only Unitarity and Jarlskog Area Certificate Theorem

**Date:** 2026-04-26
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** (1) staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`); (2) g_bare = 1 derivation target (canonical parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md)).

**Status:** proposed_retained - explicit strong derivation claim pending audit
model-independent algebraic certificate that converts a 3x3 CKM squared-
magnitude table into its unitarity-triangle area and Jarlskog magnitude,
using only the moduli. It does not modify, promote, or close any retained CKM
atlas, Wolfenstein, alpha_s, Koide, PMNS, dark-sector, or cosmology lane.

**Primary runner:**
`scripts/frontier_ckm_moduli_only_unitarity_jarlskog_area_certificate.py`

## 1. Claim

For a 3x3 unitary matrix `V`, the squared moduli

```text
B_ai = |V_ai|^2
```

already determine the absolute Jarlskog invariant. For each pair of rows
`a != b`, form the three side-squares

```text
x_i^(ab) = B_ai B_bi,        i = 1, 2, 3,
```

and the Heron radicand

```text
R_ab = 2(x_1 x_2 + x_2 x_3 + x_3 x_1) - (x_1^2 + x_2^2 + x_3^2).
```

For each pair of columns `i != j`, form similarly

```text
y_a^(ij) = B_ai B_aj,        a = 1, 2, 3,

C_ij = 2(y_1 y_2 + y_2 y_3 + y_3 y_1) - (y_1^2 + y_2^2 + y_3^2).
```

Then every row and column certificate is the same invariant:

```text
R_12 = R_13 = R_23 = C_12 = C_13 = C_23 = 4 J^2.
```

Consequently every CKM unitarity triangle has area

```text
Area = |J| / 2 = sqrt(R_ab) / 4 = sqrt(C_ij) / 4,
```

independent of which row-pair or column-pair triangle is used.

The converse is also constructive in the 3x3 case. If a strictly positive
3x3 bistochastic matrix `B` has one row-pair side triple
`sqrt(B_ai B_bi)` satisfying the triangle inequalities, then `B` is
unistochastic: there exists a unitary `V` with `|V_ai|^2 = B_ai`.
For a non-degenerate triangle, the two lifts are complex conjugates up to
row and column rephasings, and their Jarlskog invariants have opposite signs
but the same magnitude

```text
|J| = sqrt(R_ab) / 2.
```

This is the exact three-generation CP-area guardrail: moduli fix the CP
area, while the remaining freedom is the orientation sign.

## 2. Why This Moves the Program Forward

The current CKM notes contain several atlas and NLO area formulas. This note
adds the missing model-independent bridge:

- any proposed CKM magnitude surface can be checked for unitary consistency
  before a phase convention or Wolfenstein expansion is chosen;
- the absolute Jarlskog invariant is a moduli-only quantity in 3x3, not an
  additional hidden phase datum once the moduli are unitary;
- a failed equality among the six Heron certificates is a hard algebraic
  rejection of a candidate CKM table, independent of the framework's
  preferred alpha_s or atlas inputs;
- a positive common radicand places the table in the CP-violating
  unistochastic interior, while a zero radicand is the CP-conserving
  boundary.

No numerical CKM value, PDG comparator, or new alpha_s input is used below.

## 3. Definitions

Let `B` be a real 3x3 matrix with nonnegative entries. It is **bistochastic**
if

```text
sum_i B_ai = 1       for each row a,
sum_a B_ai = 1       for each column i.
```

It is **unistochastic** if there is a unitary `V` such that

```text
B_ai = |V_ai|^2.
```

For a row pair `(a,b)`, define complex edge vectors

```text
z_i = V_ai V_bi^*.
```

Row orthogonality says

```text
z_1 + z_2 + z_3 = 0,
```

so the three numbers `z_i` are the directed sides of a unitarity triangle.
Their side lengths are

```text
|z_i| = sqrt(B_ai B_bi).
```

The column-pair construction is identical, with

```text
w_a = V_ai V_aj^*
```

and column orthogonality

```text
w_1 + w_2 + w_3 = 0.
```

## 4. Necessity: Unitarity Forces the Common Certificate

Assume `V` is unitary.

### 4.1 Row-pair triangles

Fix two rows `a != b`. Let

```text
z_i = V_ai V_bi^*.
```

The row orthogonality relation gives `z_1 + z_2 + z_3 = 0`, hence the
three complex numbers close into a triangle. The squared side lengths are

```text
|z_i|^2 = |V_ai|^2 |V_bi|^2 = B_ai B_bi = x_i.
```

For any triangle with side-squares `(x_1, x_2, x_3)`, Heron's formula in
side-square form is

```text
16 Area^2 = 2(x_1 x_2 + x_2 x_3 + x_3 x_1)
            - (x_1^2 + x_2^2 + x_3^2).
```

Therefore

```text
16 Area_ab^2 = R_ab.
```

The same area is also half the absolute two-dimensional cross product of
any two directed sides:

```text
2 Area_ab = |Im(z_p z_q^*)|,        p != q.
```

But

```text
z_p z_q^*
  = V_ap V_bp^* V_aq^* V_bq
  = V_ap V_bq V_aq^* V_bp^*,
```

so `Im(z_p z_q^*)` is precisely a Jarlskog quartet for the chosen two rows
and two columns. Hence

```text
Area_ab = |J_ab;pq| / 2,
R_ab = 4 J_ab;pq^2.
```

### 4.2 One magnitude for all column choices in a fixed row pair

Let `{i,j,k} = {1,2,3}`. Since `z_i + z_j + z_k = 0`,

```text
z_k = -z_i - z_j.
```

Then

```text
Im(z_j z_k^*) = Im(z_j(-z_i^* - z_j^*))
              = -Im(z_j z_i^*)
              =  Im(z_i z_j^*),
```

and similarly

```text
Im(z_k z_i^*) = Im(z_i z_j^*).
```

Thus the three Jarlskog quartets obtained from the same row pair have the
same signed area up to the orientation convention. In particular, their
absolute values are identical.

### 4.3 One magnitude for all row choices in a fixed column pair

Now fix two columns `i != j` and define

```text
w_a = V_ai V_aj^*.
```

Column orthogonality gives `w_1 + w_2 + w_3 = 0`. The same argument as in
Section 4.2 gives a common absolute value for all row-pair quartets in this
column pair:

```text
|Im(w_a w_b^*)| = constant for a != b.
```

Since

```text
w_a w_b^*
  = V_ai V_aj^* V_bi^* V_bj
  = V_ai V_bj V_aj^* V_bi^*,
```

this is the same Jarlskog quartet family.

Combining the row-pair and column-pair arguments, every nontrivial 3x3
Jarlskog quartet has one common magnitude. Call it `|J|`. Therefore

```text
R_12 = R_13 = R_23 = C_12 = C_13 = C_23 = 4 J^2.
```

This proves the necessity direction.

## 5. Sufficiency: One Closing Row Triangle Builds the Unitary

Now let `B` be a strictly positive 3x3 bistochastic matrix. Suppose one
row pair satisfies the triangle inequalities. By permuting rows, take that
pair to be rows `1` and `2`.

Write

```text
a_i = B_1i,
b_i = B_2i,
c_i = B_3i = 1 - a_i - b_i.
```

Bistochasticity gives

```text
sum_i a_i = 1,
sum_i b_i = 1,
sum_i c_i = 1.
```

The assumed triangle inequalities for the side lengths

```text
s_i = sqrt(a_i b_i)
```

are exactly the condition that phases `theta_i` can be chosen with

```text
sum_i sqrt(a_i b_i) exp(-i theta_i) = 0.
```

Define two row vectors

```text
r_i = sqrt(a_i),
s_i = sqrt(b_i) exp(i theta_i).
```

Then

```text
<r,r> = 1,
<s,s> = 1,
<r,s> = sum_i r_i s_i^*
      = sum_i sqrt(a_i b_i) exp(-i theta_i)
      = 0.
```

So `r` and `s` are orthonormal.

Let `t` be the normalized Hermitian cross product completing the two rows:

```text
t_i^* = epsilon_ijk r_j s_k,
```

with the usual summation over the two indices not equal to `i`. Since `r`
and `s` are orthonormal, the Lagrange identity gives `||t|| = 1`, and the
antisymmetry of `epsilon_ijk` gives

```text
<r,t> = 0,
<s,t> = 0.
```

Thus the matrix with rows `r`, `s`, `t` is unitary. It remains only to prove
that the third row has the desired squared moduli.

For the first component,

```text
|t_1|^2 = |r_2 s_3 - r_3 s_2|^2
        = a_2 b_3 + a_3 b_2
          - 2 sqrt(a_2 b_2 a_3 b_3) cos(theta_3 - theta_2).
```

The closure relation says

```text
sqrt(a_1 b_1) exp(-i theta_1)
  = -sqrt(a_2 b_2) exp(-i theta_2)
    -sqrt(a_3 b_3) exp(-i theta_3).
```

Taking squared moduli gives

```text
a_1 b_1
  = a_2 b_2 + a_3 b_3
    + 2 sqrt(a_2 b_2 a_3 b_3) cos(theta_3 - theta_2).
```

Substitute this into `|t_1|^2`:

```text
|t_1|^2
  = a_2 b_3 + a_3 b_2 - (a_1 b_1 - a_2 b_2 - a_3 b_3)
  = (a_2 + a_3)(b_2 + b_3) - a_1 b_1
  = (1 - a_1)(1 - b_1) - a_1 b_1
  = 1 - a_1 - b_1
  = c_1.
```

The same cyclic calculation gives

```text
|t_i|^2 = c_i        for i = 1, 2, 3.
```

Therefore the constructed unitary matrix satisfies

```text
|V_ai|^2 = B_ai
```

for every row and column. This proves that `B` is unistochastic.

If the row triangle is non-degenerate, the phase solution is unique up to a
common rotation and complex conjugation. A common rotation is absorbed by
row or column rephasing; complex conjugation reverses the sign of every
Jarlskog quartet. Therefore the moduli fix `|J|` and leave only the CP
orientation sign:

```text
|J| = sqrt(R_12) / 2.
```

Degenerate triangles are the boundary case `R_12 = 0`, hence `J = 0`.
The construction still gives a unitary lift by using collinear phases, but
the lift lies on the CP-conserving boundary rather than in the CP-violating
interior.

## 6. Operational Certificate

For a proposed strictly positive 3x3 CKM squared-magnitude table:

1. Check bistochasticity.
2. Pick any row pair and compute

```text
R_ab = 2(x_1 x_2 + x_2 x_3 + x_3 x_1) - (x_1^2 + x_2^2 + x_3^2),
      x_i = B_ai B_bi.
```

3. If `R_ab < 0`, the table is not unistochastic.
4. If `R_ab >= 0`, the positive side triple satisfies the triangle
   inequalities, the row-pair triangle closes, and a 3x3 unitary lift exists.
5. For any valid lift,

```text
Area = sqrt(R_ab) / 4,
|J|  = sqrt(R_ab) / 2.
```

6. The remaining five row/column Heron certificates must equal the same
   `R_ab` for the lifted unitary table. If an independently proposed CKM
   table gives unequal certificates, it is algebraically inconsistent with
   exact 3x3 unitarity.

This is a finite-dimensional exact theorem, not an approximation, expansion,
or fit.

Boundary tables with zero entries are handled by the same proof after deleting
zero sides, or by continuity from the strictly positive interior. CKM
applications are in the strictly positive case.

## 7. Scope and Guardrails

This note claims:

- the exact equality of all row and column Heron certificates for any 3x3
  unitary matrix;
- the moduli-only formula `|J| = sqrt(R)/2`;
- the exact area formula `Area = sqrt(R)/4`;
- the constructive 3x3 converse: one closing row-pair triangle in a strictly
  positive bistochastic table builds a unitary lift;
- the orientation statement that non-degenerate lifts differ by CP-conjugate
  sign after rephasing.

This note does not claim:

- any new numerical CKM prediction;
- any new value of `alpha_s(v)`, `lambda`, `A`, `rho`, `eta`, or barred
  Wolfenstein coordinates;
- any all-orders extension of the retained atlas or NLO CKM surface;
- a 4x4 or higher-generation analogue;
- a PMNS, Majorana, BSM, dark-sector, cosmology, time-travel, teleportation,
  or antigravity statement.

## 8. Relationship to Existing CKM Notes

This theorem is compatible with the retained CKM area statements:

- `CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md` names the
  atlas CP-plane coordinates and atlas Jarlskog-area factor.
- `CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md` proves the
  exact right-angle identity on the rescaled atlas triangle.
- `CKM_JARLSKOG_EXACT_NLO_CLOSED_FORM_THEOREM_NOTE_2026-04-25.md` packages
  the NLO protected-gamma-bar Jarlskog closed form.

The present note supplies the independent algebraic certificate underneath
all such uses of triangle area: in three generations, the common unitarity
triangle area and `|J|` are already fixed by the squared magnitudes whenever
the moduli table is genuinely unitary.

## 9. Reproduction

```bash
python3 scripts/frontier_ckm_moduli_only_unitarity_jarlskog_area_certificate.py
```

Expected:

```text
TOTAL: PASS=14, FAIL=0
```

The runner verifies the exact Fourier-unitary case, the symbolic Heron
side-square identity, the symbolic third-row modulus recovery in the
constructive 3x3 converse, a nondegenerate numeric bistochastic lift, and the
scope/status guardrails above.


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on **both** open gates:

1. **Staggered-Dirac realization derivation target** — canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`); in-flight supporting work: `PHYSICAL_LATTICE_NECESSITY_NOTE.md`, `THREE_GENERATION_STRUCTURE_NOTE.md`, `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`, `scripts/frontier_generation_rooting_undefined.py`, `GENERATION_AXIOM_BOUNDARY_NOTE.md`.
2. **`g_bare = 1` derivation target** — canonical parent: [`G_BARE_DERIVATION_NOTE.md`](G_BARE_DERIVATION_NOTE.md) (`claim_type: positive_theorem`, `audit_status: audited_conditional`); in-flight supporting work: `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`, `G_BARE_RIGIDITY_THEOREM_NOTE.md`, `G_BARE_TWO_WARD_CLOSURE_NOTE_2026-04-18.md`, `G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md`, `G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md`, `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`, `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`.

The note produces (or directly supports) a quantitative gauge prediction (Wilson plaquette content, `α_s`, `v`, `sin²θ_W`, `m_t`, `m_H`, `g_1`, `g_2`, `β = 6`, CKM/quark/hadron mass hierarchy, action-unit metrology, etc.) by fixing `g_bare = 1` without independently deriving it — therefore both gates must close for the lane to upgrade.

Therefore `claim_type: bounded_theorem` until both gates close. When both gates close, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
