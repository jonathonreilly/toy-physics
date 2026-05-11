# Planck Primitive Coframe Boundary-Carrier Theorem

**Date:** 2026-04-25
**Status:** conditional positive support theorem for the Planck
boundary/action carrier; audit status is owned by the independent audit
lane, and this is not a standalone minimal-stack derivation of `a^(-1) = M_Pl`
**Scope:** first-order coframe/worldtube boundary carrier on the time-locked
primitive event cell
**Runner:** `scripts/frontier_planck_primitive_coframe_boundary_carrier.py`

## Cited authorities (one-hop deps)

This note records explicit one-hop authority citations for the two premises
identified as load-bearing in Theorem 2 (first-order locality and unit
primitive response normalization). The citations make the provenance of those
premises explicit, while the gravitational boundary/action-density bridge
from §5 remains the named open premise.

- [`PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`](PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
  — unaudited candidate authority that supplies the conditional route for
  the first-order locality premise from the named microscopic action
  surface. The theorem there argues that the
  algebraic differential of the link-local staggered-Dirac / Grassmann
  action with respect to its fundamental local link variables has support
  on exactly the Hamming-weight-one packet `P_1`, and that the Hodge-dual
  `P_3` is excluded as a fundamental first variation because it
  corresponds to a third-link composite source rather than a one-link
  source. That theorem supplies the action-native provenance for the
  "first-order coframe locality" assumption used in Theorem 2 below.
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  — current framework memo restoring the repo-wide axioms to physical
  `Cl(3)` on `Z^3` and recategorizing the staggered-Dirac / Grassmann
  realization as an open gate rather than a framework axiom. The
  link-local first-variation route is therefore a conditional action-surface
  route, not a new repo-wide axiom and not retained by this note.
- [`AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_LATTICE_NOETHER_THEOREM_NOTE_2026-04-29.md)
  — conditional theorem on the same Grassmann staggered-Dirac action route,
  recording explicitly that the conserved-current carriers are one-link
  bilinears (eqs (3)–(5) in that note). This is consilience evidence for the
  same first-order locality route: the action's natural carriers are
  link-local one-form structures, not three-form composites.
- [`FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md`](FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md)
  — exact negative boundary clarifying that pure substrate symmetries
  alone do *not* force first-order over Hodge-dual third-order. This is
  why the link-local first-variation route is needed: symmetry-only
  reasoning cannot select `P_1` from `P_3`. The action-route provenance
  above is the additional conditional structure that breaks the Hodge
  degeneracy if that route survives audit.

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

## Premise provenance

Prior review of this row identifies two premises in Theorem 2 as
load-bearing rather than trivial: **first-order locality**
(`B = P_1 B P_1`) and **unit primitive response normalization** (`b_a = 1`).
This section records the provenance of each premise explicitly so the
theorem statement is honest about what it derives versus what it accepts as
input.

### Premise 1: first-order coframe locality (conditional provenance; not assumed silently)

First-order locality is *not* left as an uncited structural assumption on
this note's surface. It is sourced to the algebraic first variation of the
named link-local action route, as argued in the cited
[`PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM`](PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md).
The chain is:

```text
A_min / action-surface route
  = finite Grassmann / staggered-Dirac partition
  + lattice operators built from one-link nearest-neighbor hops
  on Z^3 + anomaly-forced time axis.

local action on the primitive (t,x,y,z) star
  = sum_{a in E} u_a J_a    with support(J_a) = {a}.

algebraic first variation
  dS_link / du_a = J_a.

support of the first variation
  = span({t},{x},{y},{z}) = P_1 H_cell.
```

Equivalently: on the named `A_min` action surface, the fundamental
local source variables `u_a` are one-link / one-axis variables, by
construction. The first variation `dS_link / du_a` carries Hamming weight
exactly one. The Hodge-dual `P_3` packet remains a valid flux/face
representation, but it corresponds to a third-link composite source — it
is not an automorphism of the link-local source domain that the action route
exposes. Hence first-order locality is explicitly conditional on that cited
action structure, not adopted silently as an independent assumption on this
note's surface.

This derivation respects the negative boundary recorded in the cited
[`FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM`](FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md):
substrate symmetries alone do *not* force first-order over Hodge-dual
third-order. The link-local first-variation theorem changes the premise
surface (it adds the action source domain as additional structure beyond pure
symmetries), and on that enlarged surface the Hodge ambiguity is broken
because Hodge duality maps a one-link source to a three-link composite and is
therefore not an automorphism of the fundamental source domain.

Audit caveat: the link-local first-variation theorem is currently unaudited
on the audit graph; this note records the provenance citation explicitly but
does not ratify it. If that upstream theorem later audits clean, the present
premise would inherit stronger derivational footing. If it fails audit, this
note's first-order locality premise reverts to the abstract assumption form
already identified as load-bearing. Either way, no claim of unconditional
retention is made here.

### Premise 2: unit primitive response normalization (honest scheme/normalization choice)

Unit primitive response normalization (`b_a = 1`) is *not* a derived
fact. It is recorded here as an honest scheme/normalization choice with
explicit physical content:

```text
(N)  one activated coframe axis carries unit first-order boundary count.
```

(N) is the canonical normalization of the primitive boundary-count
operator on the source-free cell state. Concretely:

- The boundary-count operator `B` is defined to count the first-order
  active coframe slots in a primitive event. (N) sets the unit of that
  count to be one count per active slot.
- Any other choice `b_a = c` for some real `c > 0` rescales the primitive
  trace linearly: `Tr((I_16/16) (c P_A)) = c/4`. The choice `c = 1` is
  the choice that makes "one active coframe slot" carry "one boundary
  count," which is the natural canonical normalization for any
  count-valued boundary operator.
- This scheme convention is fully analogous to the standard physics
  convention that fixes the unit of fermion number to one per particle:
  it does not derive a constant; it fixes a unit so that downstream
  coefficients are dimensionless ratios rather than scheme-dependent
  rescalings.
- Coframe-slot symmetry (premise 3 of Theorem 2) then forces the same
  unit choice on each of the four primitive slots.

What this is and is not:

- (N) is **not** a hidden assumption about gravitational normalization.
  The bridge to gravitational boundary/action density is the *separate*
  named open premise (BP) carried over from §5: that the first-order
  coframe carrier `P_A` is the microscopic gravitational boundary/action
  density carrier. (N) is upstream of that bridge and concerns only the
  count-operator normalization on the Boolean event cell.
- (N) is **not** a tunable parameter. It is the canonical unit choice
  for a count operator. Rescaling `b_a` linearly rescales `c_cell`
  linearly, so it is *exactly* the normalization gauge of the
  bookkeeping; it does not move the lane forward or backward, only
  rescales numbers in lock-step.
- The downstream Wald-Noether composition cited in
  `BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`
  (downstream consumer; backticked to avoid length-2 cycle — citation
  graph direction is *downstream → upstream*)
  uses this canonical normalization to match `c_cell = 1/4` to
  `1/(4G_Newton,lat)`, forcing `G_Newton,lat = 1` in framework lattice
  units. Any rescaling of (N) by a factor `c` would absorb into a
  matching rescaling of `G_Newton,lat`; the physical content of the
  match is preserved, only the unit convention changes.

Honest premise label: `unit_primitive_response_normalization` is recorded
as an explicit scheme/normalization choice. It is not derived from
`A_min` and this note does not claim to derive it. Future work that
derives a canonical count-operator normalization from independent
substrate dynamics (rather than scheme convention) would close this
remaining bookkeeping freedom.

### Closure status after this provenance pass

```text
first-order coframe locality
  : sourced to the link-local first variation route
    (cited authority: PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM)
  ; conditional pending upstream audit of that theorem.

unit primitive response normalization
  : honest scheme/normalization choice; canonical count-operator unit
  ; not derived from A_min on this note's surface.

coframe-slot symmetry, axis additivity
  : time-locked Boolean event-cell symmetry assumptions used by this note.

gravitational boundary/action density identification
  : open named bridge premise (§5);
    NOT derived; NOT closed by this PR.
```

The review-blocker form — "P_A is forced only after assuming first-order
locality and unit primitive response normalization" — is now narrowed:
first-order locality has a cited conditional route through the link-local
first-variation theorem, and unit primitive response normalization is recorded
as an explicit scheme/normalization choice. The remaining open premise is the
gravitational boundary/action-density bridge in §5, which this note does not
claim to derive.

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
TOTAL: PASS=18, FAIL=0
```

The four added checks verify the new premise-provenance content:

1. The cited link-local first-variation authority exists and is
   load-bearing for the first-order locality premise.
2. The current minimal-framework memo exists and is cited, keeping the
   action-surface route conditional rather than axiomatic.
3. The cited Hodge-degeneracy negative boundary authority exists.
4. Unit primitive response normalization is recorded as a canonical
   scheme/normalization choice and rescaling it linearly rescales
   `c_cell` linearly (so unit choice is not a hidden tunable parameter,
   only a bookkeeping gauge).

## Closeout flags

```text
PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER=TRUE
FIRST_ORDER_COFRAME_CARRIER_EQUALS_P_A=TRUE
PRIMITIVE_COEFFICIENT_FROM_COFRAME_CARRIER=1/4
FINITE_BOUNDARY_EXTENSION_COMPATIBLE=TRUE
FIRST_ORDER_LOCALITY_PROVENANCE=conditional_link_local_first_variation_route
UNIT_PRIMITIVE_RESPONSE_NORMALIZATION_PROVENANCE=canonical_scheme_choice
PLANCK_MINIMAL_STACK_CLOSURE=FALSE
RESIDUAL_PLANCK=derive_gravitational_boundary_action_density_as_first_order_coframe_carrier
```
