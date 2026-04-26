# Planck Primitive Coframe Boundary-Carrier Theorem

**Date:** 2026-04-25
**Status:** positive support theorem for the Planck boundary/action carrier;
not a standalone minimal-stack derivation of `a^(-1) = M_Pl`
**Scope:** first-order coframe/worldtube boundary carrier on the time-locked
primitive event cell
**Runner:** `scripts/frontier_planck_primitive_coframe_boundary_carrier.py`

## Purpose

The current Planck packet already has the exact primitive trace

```text
c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4,
```

and the finite-boundary extension theorem shows that this coefficient extends
uniquely to finite face-union patches once the primitive boundary count is
accepted as the microscopic gravitational boundary/action carrier.

The remaining carrier-identification question is sharper:

```text
why should the Hamming-weight-one packet P_A be the primitive
boundary/action carrier?
```

This note proves the positive theorem available on the coframe surface:

> On the time-locked primitive event cell, the unique source-free, additive,
> coframe-slot symmetric first-order coframe boundary/worldtube carrier is
> exactly the Hamming-weight-one packet `P_A`.

This moves the Planck lane forward because the `1/4` coefficient is no longer
only a rank choice. It is the coefficient of the unique first-order coframe
boundary variation. The theorem still does not prove that gravitational
boundary/action density must be identified with that first-order coframe
carrier; that physical identification remains the explicit bridge premise.

## Primitive event algebra

Let the primitive time-locked coframe axes be

```text
E = {t, x, y, z}.
```

The primitive event cell is the Boolean coframe register

```text
H_cell = tensor_{a in E} C^2_a ~= C^16.
```

Use the orthonormal basis `|S>` indexed by subsets

```text
S subset E.
```

Here `S` records which primitive coframe slots are active in a cell event. Let

```text
P_S = |S><S|
```

and define the Hamming-weight packets

```text
P_k = sum_{|S|=k} P_S,       k = 0,1,2,3,4.
```

The Planck packet's active primitive boundary packet is

```text
P_A = P_1 = sum_{a in E} P_{ {a} }.
```

The source-free primitive state is

```text
rho_cell = I_16/16.
```

## Coframe response polynomial

Introduce formal coframe activation variables

```text
u_t, u_x, u_y, u_z.
```

The source-free local coframe response generating polynomial is

```text
G(u) = product_{a in E} (1 + u_a)
     = sum_{S subset E} u_S,
```

where

```text
u_S = product_{a in S} u_a.
```

The dictionary from the response polynomial to the event-cell Hilbert
decomposition sends

```text
u_S  <->  P_S.
```

This is just the Boolean tensor-product expansion of the primitive cell. It
does not introduce an entropy law or a Planck normalization.

## Theorem 1: first-order boundary carrier is `P_A`

Let

```text
G_1(u) = sum_{a in E} u_a
```

be the first homogeneous component of `G(u)`. Under the monomial/projector
dictionary above, `G_1` maps exactly to

```text
B_1 = sum_{a in E} P_{ {a} } = P_A.
```

Thus the first-order coframe boundary/worldtube carrier is exactly the
Hamming-weight-one packet.

### Proof

Expanding the product gives

```text
G(u)
  = 1
    + (u_t + u_x + u_y + u_z)
    + (degree 2 terms)
    + (degree 3 terms)
    + u_t u_x u_y u_z.
```

The first homogeneous component is therefore

```text
G_1(u) = u_t + u_x + u_y + u_z.
```

The dictionary sends each one-axis monomial to the corresponding one-axis
projector:

```text
u_a <-> P_{ {a} }.
```

Therefore

```text
G_1 <-> sum_{a in E} P_{ {a} } = P_1 = P_A.
```

QED.

## Theorem 2: uniqueness from first-order locality and symmetry

Let `B` be a diagonal source-free primitive boundary carrier on `H_cell`.
Assume:

1. **First-order coframe locality.** `B` is supported only on basis states
   with exactly one active coframe axis:

   ```text
   B = P_1 B P_1.
   ```

2. **Axis additivity.** The four one-axis events contribute independently,
   so

   ```text
   B = sum_{a in E} b_a P_{ {a} }.
   ```

3. **Time-locked coframe-slot symmetry.** The source-free primitive register
   does not distinguish the four primitive coframe slots on this carrier
   surface:

   ```text
   b_t = b_x = b_y = b_z.
   ```

4. **Unit primitive response normalization.** A single activated coframe axis
   carries unit first-order boundary count:

   ```text
   b_a = 1.
   ```

Then

```text
B = P_A.
```

### Proof

By first-order locality and axis additivity,

```text
B = b_t P_{ {t} } + b_x P_{ {x} } + b_y P_{ {y} } + b_z P_{ {z} }.
```

Coframe-slot symmetry gives one common coefficient `b`. Unit primitive
response normalization gives `b=1`. Hence

```text
B = P_{ {t} } + P_{ {x} } + P_{ {y} } + P_{ {z} } = P_A.
```

QED.

## Theorem 3: primitive coefficient

For the unique first-order coframe boundary carrier,

```text
c_cell = Tr(rho_cell P_A) = 1/4.
```

### Proof

There are four one-axis subsets of the four-axis set `E`, so

```text
rank(P_A) = binom(4,1) = 4.
```

With `rho_cell = I_16/16`,

```text
Tr(rho_cell P_A)
  = Tr(P_A)/16
  = rank(P_A)/16
  = 4/16
  = 1/4.
```

QED.

## Relation to finite boundary patches

The finite-boundary density extension theorem starts from the primitive face
coefficient and proves the unique additive finite-patch law

```text
N_A(P) = c_cell A(P)/a^2.
```

This note supplies the missing local coframe content behind that primitive
coefficient:

```text
first-order coframe boundary variation
  -> P_A
  -> Tr((I_16/16) P_A) = 1/4.
```

Combining the two theorems gives a positive conditional chain:

```text
first-order coframe boundary carrier
  -> c_cell = 1/4
  -> unique finite-boundary density extension.
```

## Relation to the Clifford coframe bridge

The Target 3 Clifford phase bridge assumes a metric-compatible active
coframe response on `P_A H_cell`. This note identifies the preceding carrier
projection:

```text
first-order coframe/worldtube variation selects P_A.
```

The two notes are complementary:

- this note selects the primitive boundary/action carrier subspace `P_A`;
- the Clifford bridge supplies a sufficient active-block response structure on
  `P_A H_cell`, forcing the irreducible `Cl_4(C)` / two-mode CAR carrier.

Together they sharpen the positive Planck route without claiming that the
older finite automorphism stack alone derives the absolute scale.

## Why this is positive but not lane closure

What this proves:

- `P_A` is the unique first-order coframe boundary/worldtube carrier on the
  primitive time-locked Boolean event cell;
- the primitive coefficient `4/16 = 1/4` is the trace of that carrier in the
  source-free cell state;
- the coefficient is therefore tied to a first-order boundary variation, not
  just to an arbitrary rank-four label.

What this still does not prove:

- that the physical gravitational boundary/action density must be identified
  with the first-order coframe carrier;
- the SI decimal value of `G`, `hbar`, `l_P`, or `M_Pl`;
- a minimal finite-automorphism derivation of Planck scale;
- a replacement for the source-unit normalization theorem;
- any claim about charged-lepton Koide or the excluded frontier-extension
  lanes.

The exact remaining physical theorem target is now:

```text
derive_gravitational_boundary_action_density_as_first_order_coframe_carrier
```

rather than the broader phrase "derive the primitive boundary count."

## Reviewer-pressure checks

### Is this only restating the rank computation?

No. The rank computation is Theorem 3. The new content is Theorem 1 and
Theorem 2: `P_A` is selected by the first homogeneous coframe variation and is
unique under first-order locality, additivity, symmetry, and unit response.

### Does this assume the Planck coefficient?

No. The coefficient is computed after the carrier is selected:

```text
first-order coframe carrier = P_A,
rank(P_A)=4,
Tr((I_16/16)P_A)=1/4.
```

### Does coframe-slot symmetry really include the time slot?

On this theorem's surface the primitive cell is time-locked: the local
worldtube boundary carrier counts one active coframe axis in the four-axis
event cell `(t,x,y,z)`. The theorem is not claiming an independent Euclidean
spacetime symmetry or ordinary cubic spatial symmetry acting on time. It uses
the source-free coframe-slot symmetry of the Boolean event register before a
macroscopic face/normal is selected. Once a face normal is selected, the later
Target 2/3 notes split the active block into normal and tangent response
channels.

### Could a higher-order packet also have coefficient `1/4`?

Yes. On the source-free uniform state for four axes,

```text
Tr(rho_cell P_3) = binom(4,3)/16 = 1/4.
```

This is why first-order locality is load-bearing. The theorem selects `P_1`,
not merely a rank-four subspace. The Hodge-dual third-order packet is the
complementary codimension-one carrier, and treating it as primary would be a
different physical boundary convention. The current Planck packet uses the
one-step worldtube/boundary count, which is the first-order coframe carrier.

### Does this close the Planck lane?

No. It proves the exact carrier available once the gravitational boundary
object is read as a first-order coframe/worldtube variation. It does not prove
that this is the physical gravitational boundary/action readout of the older
minimal stack.

## Verification

Run:

```bash
python3 scripts/frontier_planck_primitive_coframe_boundary_carrier.py
```

Expected result:

```text
TOTAL: PASS=14, FAIL=0
```

## Closeout flags

```text
PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER=TRUE
FIRST_ORDER_COFRAME_CARRIER_EQUALS_P_A=TRUE
PRIMITIVE_COEFFICIENT_FROM_COFRAME_CARRIER=1/4
FINITE_BOUNDARY_EXTENSION_COMPATIBLE=TRUE
PLANCK_MINIMAL_STACK_CLOSURE=FALSE
RESIDUAL_PLANCK=derive_gravitational_boundary_action_density_as_first_order_coframe_carrier
```
