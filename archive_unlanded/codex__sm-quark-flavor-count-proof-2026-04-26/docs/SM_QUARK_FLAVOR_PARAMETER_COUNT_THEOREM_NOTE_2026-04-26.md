# Standard Model Quark Flavor Parameter-Count Theorem

**Date:** 2026-04-26

**Status:** standalone positive Standard Model flavor theorem. This note proves
that the generic active one-Higgs Standard Model quark Yukawa sector contains
exactly ten physical real parameters: six quark masses, three CKM mixing
angles, and one CKM CP-odd phase. It is a structural guardrail for the
retained Yukawa and CKM notes. It does not derive any numerical mass, CKM
entry, Wolfenstein parameter, CP phase value, rare-decay rate, baryogenesis
asymmetry, time-travel, teleportation, or antigravity claim.

**Primary runner:** `scripts/frontier_sm_quark_flavor_parameter_count.py`

## 1. Claim

Work on the active one-Higgs Standard Model quark sector with three
generations and canonical kinetic terms. The retained one-Higgs Yukawa
selection theorem supplies two arbitrary complex `3 x 3` Yukawa matrices,

```text
Y_u, Y_d.
```

At a generic full-rank point with nondegenerate singular values and no
accidental flavor stabilizer beyond baryon number, the physical quark-flavor
parameter space has real dimension

```text
10.
```

Equivalently, the generic quark sector is coordinatized by

```text
6 positive quark masses
+ 3 CKM mixing angles
+ 1 CKM CP-odd phase.
```

The theorem is a parameter-count theorem, not a numerical prediction theorem.

## 2. Scope and Guardrails

The word "generic" is load-bearing. If quark masses are exactly degenerate,
if a Yukawa matrix loses rank, or if additional flavor symmetries are imposed,
the stabilizer of the Yukawa pair grows and the quotient has lower effective
dimension. Those special strata are physically important boundaries, but they
are not the generic Standard Model flavor surface.

The theorem also does not assert that the CKM parameters are determined by
the Standard Model gauge representation alone. It proves the opposite
guardrail: after all allowed basis redundancies are removed, ten independent
quark-flavor inputs remain.

## 3. Input Surface

The quark Yukawa Lagrangian has the form

```text
L_Y^q = - bar Q_L Y_d H d_R - bar Q_L Y_u tilde H u_R + h.c.
```

After electroweak symmetry breaking, the mass matrices are proportional to
the same Yukawa matrices:

```text
M_u = v Y_u / sqrt(2),
M_d = v Y_d / sqrt(2).
```

The proportional factor `v/sqrt(2)` does not affect the flavor parameter
count. The count is therefore the count of two arbitrary complex `3 x 3`
matrices modulo the flavor-basis transformations that preserve canonical
kinetic terms.

Before Yukawas are specified, the quark kinetic terms have the generation
flavor symmetry

```text
G_flavor = U(3)_Q x U(3)_u x U(3)_d.
```

The transformations act as

```text
Q_L -> U_Q Q_L,
u_R -> U_u u_R,
d_R -> U_d d_R,
```

and hence

```text
Y_u -> U_Q^dagger Y_u U_u,
Y_d -> U_Q^dagger Y_d U_d.
```

## 4. Quotient Count

Each complex `3 x 3` matrix carries

```text
2 * 3^2 = 18
```

real parameters. The pair `(Y_u,Y_d)` therefore carries

```text
36
```

real parameters before quotienting.

The flavor group has dimension

```text
dim U(3)_Q + dim U(3)_u + dim U(3)_d
  = 3^2 + 3^2 + 3^2
  = 27.
```

At a generic Yukawa pair the only continuous transformation that leaves both
matrices unchanged is common quark-number phase rotation,

```text
U_Q = U_u = U_d = e^(i alpha) I_3.
```

This is baryon number. It has real dimension `1`. Therefore the generic
flavor orbit has dimension

```text
27 - 1 = 26.
```

The physical quotient dimension is

```text
36 - 26 = 10.
```

This proves the ten-parameter quotient count.

One way to see why the generic stabilizer is only this one phase is to move
to a basis where `Y_u = D_u` is positive diagonal with nondegenerate entries.
The equation `U_Q^dagger D_u U_u = D_u` then forces `U_Q` and `U_u` to be
the same diagonal phase matrix. Applying the same reasoning to `Y_d` leaves a
diagonal rephasing freedom acting on the CKM matrix:

```text
V_ab -> e^(-i alpha_a) V_ab e^(i beta_b).
```

For a generic CKM matrix with all entries nonzero, invariance of every entry
requires `alpha_a = beta_b` for all `a,b`, hence one common phase. Degenerate
masses, zero CKM entries, or extra texture constraints are precisely the
non-generic cases where this stabilizer can grow.

## 5. Mass-Basis Identification

The quotient count becomes physically transparent by using singular-value
decompositions:

```text
U_uL^dagger Y_u U_uR = D_u,
U_dL^dagger Y_d U_dR = D_d,
```

where `D_u` and `D_d` are real nonnegative diagonal matrices. At a generic
full-rank nondegenerate point they contain six positive singular values:

```text
m_u, m_c, m_t, m_d, m_s, m_b.
```

The mismatch between the two left-handed diagonalizations is

```text
V_CKM = U_uL^dagger U_dL.
```

The right-handed rotations do not enter the charged weak current. Thus the
remaining flavor information after the six masses is the unitary `3 x 3`
matrix `V_CKM`, modulo mass-eigenstate field rephasings.

## 6. CKM Rephasing Count

A unitary `3 x 3` matrix has real dimension

```text
dim U(3) = 9.
```

The six mass-eigenstate quark fields may be rephased:

```text
u_a -> e^(i alpha_a) u_a,
d_b -> e^(i beta_b) d_b.
```

Under these rephasings,

```text
V_ab -> e^(-i alpha_a) V_ab e^(i beta_b).
```

The common choice

```text
alpha_1 = alpha_2 = alpha_3 = beta_1 = beta_2 = beta_3
```

leaves `V` unchanged. Therefore only

```text
6 - 1 = 5
```

phase directions act effectively on `V`. The physical CKM space has dimension

```text
9 - 5 = 4.
```

The real orthogonal submanifold `SO(3)` has dimension

```text
3 * (3 - 1) / 2 = 3.
```

Those are the three mixing angles. The remaining physical dimension is

```text
4 - 3 = 1,
```

the single CP-odd CKM phase.

Combining with the six singular values gives

```text
6 + 3 + 1 = 10,
```

matching the quotient count from Section 4.

## 7. General-N Cross-Check

The same argument for `N` generations gives:

```text
two Yukawa matrices:              4 N^2 real parameters,
flavor group:                     3 N^2 dimensions,
generic baryon stabilizer:        1 dimension,
generic physical quark count:     N^2 + 1.
```

The physical coordinates split as

```text
2N masses,
N(N-1)/2 mixing angles,
(N-1)(N-2)/2 CP-odd phases.
```

The sum is

```text
2N + N(N-1)/2 + (N-1)(N-2)/2
  = N^2 + 1.
```

For `N=1`, there is no mixing angle and no CP phase. For `N=2`, there is one
mixing angle and no CP phase. For `N=3`, there are three mixing angles and
one CP phase. Thus the existence of a physical CKM CP phase is a genuinely
three-generation feature of the generic one-Higgs quark flavor sector.

## 8. Theorem Proof

The raw quark Yukawa data are the two complex matrices `(Y_u,Y_d)`, so the
unquotiented dimension is `36`. Canonical kinetic terms permit the unitary
flavor-basis group `U(3)_Q x U(3)_u x U(3)_d`, dimension `27`, to act on this
pair. At a generic full-rank nondegenerate point, the only continuous element
that fixes both matrices is common baryon number, dimension `1`. Therefore
the physical quotient has dimension `36 - (27 - 1) = 10`.

Singular-value decompositions show that six of those ten parameters can be
chosen as positive quark masses. The residual left-handed mismatch is the
unitary CKM matrix. Rephasing the six mass eigenfields removes five effective
phases from this unitary matrix, leaving a four-dimensional physical CKM
space. Its real orthogonal subspace accounts for three mixing angles, and
the one remaining dimension is the CP-odd phase.

Therefore the generic active one-Higgs Standard Model quark sector has
exactly six masses, three mixing angles, and one CP-odd CKM phase. This
proves the theorem.

## 9. Program Consequences

This theorem gives a sharp review-facing boundary:

- any proposed CKM derivation must account for four physical CKM parameters,
  not an arbitrary nine-entry unitary matrix;
- the one-Higgs Yukawa theorem correctly leaves ten quark-flavor inputs open;
- CP violation in the quark sector is structurally possible only from three
  generations onward;
- no numerical CKM, Koide, PMNS, dark-sector, baryogenesis, time-travel,
  teleportation, or antigravity claim is promoted by this count.
