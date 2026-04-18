# Perron-Frobenius Step-2 Wilson Hermitian Source-Packet Realization

**Date:** 2026-04-17  
**Status:** exact science-only theorem reducing theorem-grade Wilson support
realization to one finite `9`-element Hermitian source packet with explicit
matrix-unit reconstruction identities, while carrying the matching
current-bank no-go  
**Script:** `scripts/frontier_perron_frobenius_step2_wilson_hermitian_source_packet_realization_2026_04_17.py`

## Question

After the Wilson front has already been sharpened to:

- rank-`3` Wilson matrix-source embedding `Phi_e`,
- weaker Hermitian restriction `Psi_e`,
- one invariant compressed-resolvent block law,
- and then one post-support spectral packet,

can theorem-grade support realization itself be posed as one finite explicit
Wilson source packet rather than as an abstract embedding statement?

## Bottom line

Yes.

Fix the standard Hermitian basis of `Herm(3)`:

- `B_1 = E_11`,
- `B_2 = E_22`,
- `B_3 = E_33`,
- `B_4 = E_12 + E_21`,
- `B_5 = -i E_12 + i E_21`,
- `B_6 = E_13 + E_31`,
- `B_7 = -i E_13 + i E_31`,
- `B_8 = E_23 + E_32`,
- `B_9 = -i E_23 + i E_32`.

Then theorem-grade Wilson support realization is exactly equivalent to one
finite Hermitian Wilson source packet

`S_a = Psi_e(B_a)`, `a = 1, ..., 9`,

such that the reconstructed operators

- `F_11 = S_1`,
- `F_22 = S_2`,
- `F_33 = S_3`,
- `F_12 = (S_4 + i S_5)/2`,
- `F_21 = (S_4 - i S_5)/2`,
- `F_13 = (S_6 + i S_7)/2`,
- `F_31 = (S_6 - i S_7)/2`,
- `F_23 = (S_8 + i S_9)/2`,
- `F_32 = (S_8 - i S_9)/2`

satisfy the exact matrix-unit relations and

`P_e = F_11 + F_22 + F_33`

is rank `3`.

So the Wilson support problem is now finite in the sharpest explicit sense yet:

- realize one `9`-packet of Hermitian Wilson operators,
- satisfying one explicit finite polynomial identity table.

This is cleaner than abstract embedding rhetoric and sharper than saying only
that the image of `Psi_e` is a `9`-dimensional Hermitian plane.

The current exact bank still does **not** realize even this finite packet.

## What is already exact

### 1. `Phi_e` and `Psi_e` are already the right Wilson-side objects

From
[PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_WILSON_MATRIX_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md):

- theorem-grade `I_e / P_e` is exactly equivalent to theorem-grade
  rank-`3` Wilson matrix-source embedding `Phi_e : Mat_3(C) -> End(H_W)`.

From
[PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md):

- the compressed theorem only uses the Hermitian restriction
  `Psi_e := Phi_e |_(Herm(3))`,
- whose image is a real `9`-dimensional Hermitian source plane.

So the Wilson front already knows both the stronger algebra object and the
weaker Hermitian object.

### 2. Matrix units already reconstruct the full source algebra

From the Wilson matrix-source embedding theorem:

- theorem-grade `Phi_e` is equivalent to one embedded rank-`3` matrix-unit
  system `F_ij`.

So any finite packet that reconstructs those `F_ij` exactly is already enough
to recover `Phi_e`, hence `I_e / P_e`.

### 3. The current bank still lacks even theorem-grade `Psi_e`

From
[PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_HERMITIAN_SOURCE_EMBEDDING_TARGET_NOTE_2026-04-17.md)
and
[PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md](./PERRON_FROBENIUS_STEP2_CHARGED_EMBEDDING_BOUNDARY_NOTE_2026-04-17.md):

- the current bank still does **not** realize theorem-grade
  `I_e / P_e / Phi_e / Psi_e`.

So this finite packet is not already hidden on the current bank either.

## Theorem 1: theorem-grade `Psi_e` is exactly equivalent to one finite `9`-packet with explicit matrix-unit reconstruction

Fix the standard Hermitian basis `B_1, ..., B_9` above.

Then the following are equivalent:

1. a theorem-grade rank-`3` Wilson matrix-source embedding `Phi_e`, equivalently
   its Hermitian restriction `Psi_e = Phi_e |_(Herm(3))`;
2. a `9`-tuple of Hermitian Wilson operators `S_1, ..., S_9` such that the
   reconstructed operators `F_ij` defined above satisfy:
   - `F_ij F_kl = delta_jk F_il`,
   - `F_ij^* = F_ji`,
   - `rank(F_11 + F_22 + F_33) = 3`.

### Proof

`(1) => (2)`.

Given `Phi_e`, define

`S_a := Psi_e(B_a) = Phi_e(B_a)`.

Because each `B_a` is Hermitian and `Phi_e` is `*`-preserving, each `S_a` is
Hermitian.

Now reconstruct the `F_ij` from the displayed formulas. Since

- `B_1 = E_11`, `B_2 = E_22`, `B_3 = E_33`,
- `B_4 + i B_5 = 2 E_12`,
- `B_6 + i B_7 = 2 E_13`,
- `B_8 + i B_9 = 2 E_23`,

one gets exactly

`F_ij = Phi_e(E_ij)`.

So the `F_ij` obey the matrix-unit relations, and

`F_11 + F_22 + F_33 = Phi_e(1_3)`

has rank `3`.

`(2) => (1)`.

Assume a `9`-packet with the stated reconstruction property.
Define `Phi_e(E_ij) := F_ij` on the matrix units and extend complex-linearly to
all of `Mat_3(C)`.

Because the `F_ij` satisfy the exact matrix-unit relations, `Phi_e` is a
unital `*`-monomorphism. Its support projector is

`P_e := Phi_e(1_3) = F_11 + F_22 + F_33`,

which has rank `3` by assumption.

Restricting `Phi_e` to `Herm(3)` gives `Psi_e`, and by construction

`Psi_e(B_a) = S_a`.

So the finite `9`-packet is exactly equivalent to theorem-grade Wilson support
realization.

## Corollary 1: the Wilson support problem is now a finite polynomial-identity problem

The next honest positive Wilson-support theorem may now be stated as:

- produce `9` Hermitian Wilson operators `S_1, ..., S_9`,
- verify the explicit reconstructed `F_ij` satisfy the matrix-unit table,
- verify `rank(F_11 + F_22 + F_33) = 3`.

That is finite and explicit.

## Corollary 2: once the packet lands, the later Wilson theorems follow canonically

As soon as the `9`-packet is realized:

- `Phi_e` follows canonically,
- `Psi_e` follows canonically,
- the invariant compressed-resolvent block law is the next theorem,
- and after support realization the post-support verification shrinks further to
  the three scalar spectral identities.

So this packet is the sharp finite gateway into the whole Wilson compressed
route.

## Theorem 2: the current bank still does not realize even that finite packet

Assume the exact Wilson matrix-source embedding target theorem, the exact
Hermitian source-embedding target theorem, and the exact charged-embedding
boundary theorem. Then the current exact bank still does **not** realize:

1. theorem-grade `Phi_e`,
2. theorem-grade `Psi_e`,
3. therefore any `9`-packet whose reconstructed operators satisfy the exact
   matrix-unit table at theorem grade.

So the current bank still does **not** reach even this sharp finite packet
stage.

## What this closes

- exact reduction of Wilson support realization to one finite `9`-element
  Hermitian source packet
- exact reconstruction formulas from that packet to the embedded matrix units
- exact statement that the current bank still does not realize even this
  finite packet

## What this does not close

- a positive realization of that packet
- a positive Wilson support theorem
- a positive Wilson-to-`dW_e^H` theorem
- a positive global PF selector

## Why this matters

This is the sharpest explicit Wilson-support reduction yet on the branch.

The frontier is no longer just:

- “realize `P_e` somehow.”

It is now:

- realize one finite `9`-packet of Hermitian Wilson sources with one explicit
  matrix-unit reconstruction table.
