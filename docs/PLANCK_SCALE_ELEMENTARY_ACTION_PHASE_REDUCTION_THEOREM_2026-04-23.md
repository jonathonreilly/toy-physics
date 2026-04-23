# Planck-Scale Elementary Action-Phase Reduction Theorem

**Date:** 2026-04-23  
**Status:** science-only first-principles reduction theorem  
**Audit runner:** `scripts/frontier_planck_elementary_action_phase_reduction.py`

## Question

If we stop leaning on the current repo packaging and ask the bare first-
principles question

> what about `Cl(3)` on `Z^3` could ever force the lattice spacing to be
> Planck?

what is the strongest honest answer?

## Bottom line

The strongest honest answer is:

> `Cl(3)` on `Z^3` forces the **right kind of elementary carrier** for a
> Planck derivation, but not yet the exact Planck coefficient.

More precisely:

1. `Z^3` gives a minimal nondegenerate oriented 2-cell: the elementary square
   plaquette of area `a^2`.
2. `Cl(3)` gives the local spinorial rotation algebra through its bivectors.
3. Unitarity says a closed elementary process is read out only through an
   action phase `exp(i S / hbar)`.
4. Einstein/Regge gravity assigns to an elementary curvature hinge the
   dimensionless phase

   `S_h / hbar = (A_h eps_h) / (8 pi l_P^2)`,

   where `l_P^2 = G hbar / c^3`.

Therefore any exact Planck derivation from bare `Cl(3)` on `Z^3` must come
from one new theorem of the following form:

> the elementary `Cl(3)`/`Z^3` curvature process has one exact nonzero action
> quantum `q_* = S_* / hbar` and one exact geometric defect quantum `eps_*`,
> on the same elementary plaquette/hinge.

That theorem would force

`a^2 / l_P^2 = 8 pi q_* / eps_*`.

So `Cl(3)` on `Z^3` by itself can already force **Planck-order** scaling, but
it does **not** yet force the exact coefficient `a = l_P` until the ratio
`q_* / eps_*` is itself derived exactly.

## What bare `Cl(3)` on `Z^3` really gives

The first-principles gains are real:

- **discreteness:** `Z^3` provides a minimal length step `a`;
- **minimal area:** the elementary oriented square gives a minimal 2-cell of
  area `a^2`;
- **local rotation algebra:** bivectors in `Cl(3)` generate local spinorial
  rotations/holonomies;
- **quantum readout:** unitarity makes closed local evolution visible only
  through a phase `S / hbar`.

That is already enough to say what the Planck theorem must look like.

It is **not** enough to fix the exact numerical coefficient.

## The reduction

### 1. Minimal geometric carrier

On `Z^3`, the smallest nondegenerate closed oriented spatial loop is the
elementary square plaquette. So the natural elementary curvature carrier has

`A_* = a^2`.

If gravity on the physical lattice is truly geometric rather than a mere
continuum regulator, this is the first place a local curvature defect can live.

### 2. Minimal quantum carrier

On a unitary theory, an elementary closed process contributes only through

`U_* = exp(i S_* / hbar)`.

So any elementary geometric forcing law must be a statement about an exact
dimensionless action phase

`q_* := S_* / hbar`.

### 3. Einstein/Regge matching

For a discrete curvature hinge, the Einstein/Regge action has the form

`S_h = (c^3 / (8 pi G)) A_h eps_h`,

so

`S_h / hbar = (A_h eps_h) / (8 pi l_P^2)`.

On the elementary hinge/plaquette:

`q_* = S_* / hbar = (a^2 eps_*) / (8 pi l_P^2)`.

Therefore

`a^2 / l_P^2 = 8 pi q_* / eps_*`.

That is the exact first-principles reduction.

### 4. What follows immediately

If both `q_*` and `eps_*` are exact nonzero order-one quantities, then

`a^2 ~ l_P^2`

up to an exact order-one coefficient.

So a bare discrete spinorial lattice does naturally point to a **Planck-scale
cell**, not to an arbitrarily separated UV length.

### 5. What does **not** follow immediately

Exact `a = l_P` requires

`8 pi q_* / eps_* = 1`.

That is a highly nontrivial coefficient identity.

Bare `Cl(3)` on `Z^3` does not yet supply it.

## First-principles examples

This reduction also explains why several tempting arguments fail to give an
exact result:

- **Compton = Schwarzschild self-completion** only fixes a threshold up to an
  order-one convention for what counts as "one cell" or "one localized mode."
- **spinorial sign under `2 pi` rotation** gives a nontrivial phase quantum,
  but by itself does not fix the associated curvature defect coefficient.
- **minimal nonzero cubical deficit** may be geometrically quantized, but by
  itself does not fix the action quantum.

Each gives one side of the formula, not both.

## The theorem-level statement

**Theorem (elementary action-phase reduction).**
Assume only:

1. the physical substrate is `Z^3` with elementary step `a`;
2. local geometry/holonomy is carried by `Cl(3)` bivector rotations;
3. physical closed elementary processes are read out by the unitary phase
   `exp(i S / hbar)`;
4. the gravitational curvature sector, when written on the same elementary
   carrier, is Einstein/Regge with hinge action
   `S_h = (c^3 / (8 pi G)) A_h eps_h`.

Then any no-import Planck derivation from bare `Cl(3)` on `Z^3` reduces to an
exact coefficient theorem on one elementary plaquette/hinge:

`a^2 / l_P^2 = 8 pi q_* / eps_*`,

where

- `q_* = S_* / hbar` is the exact elementary action phase quantum, and
- `eps_*` is the exact elementary geometric defect quantum.

Consequently:

- if `q_*` and `eps_*` are only known up to order-one size, then the lattice
  is forced only to be Planck-order;
- exact `a = l_P` is forced only if the ratio `q_* / eps_*` is itself derived
  exactly.

## What this closes

This closes the very broad question

> what kind of thing could make bare `Cl(3)` on `Z^3` force Planck at all?

Answer:

- not a generic spectral identity,
- not a generic bulk action identity,
- but an **elementary curvature/action quantum theorem** on the minimal
  plaquette/hinge carrier.

That is a real reduction in search space.

## What this does not close

This theorem does **not** prove:

- that `q_*` is already known;
- that `eps_*` is already known;
- that `a = l_P` is already derived;
- that the surviving theorem must come from spinorial `2 pi` sign alone;
- that the boundary-density route is dead.

It proves only the sharper first-principles reduction:

- exact Planck from bare `Cl(3)` on `Z^3` lives or dies on one elementary
  action/defect coefficient theorem.

## Safe wording

**Can claim**

- bare `Cl(3)` on `Z^3` naturally points to a Planck-order elementary cell if
  gravity is carried by elementary curvature/action quanta;
- exact Planck reduces to an elementary coefficient identity
  `a^2 / l_P^2 = 8 pi q_* / eps_*`;
- the right first-principles target is an elementary action-phase/defect
  theorem, not another large-scale continuum matching.

**Cannot claim**

- that `Cl(3)` on `Z^3` already forces `a = l_P` with no further theorem;
- that the coefficient identity is already in hand.
