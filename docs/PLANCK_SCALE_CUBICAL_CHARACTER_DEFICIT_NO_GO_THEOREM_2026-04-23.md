# Planck-Scale Cubical Character-Deficit No-Go Theorem

**Date:** 2026-04-23  
**Status:** science-only conditional no-go on the canonical gauge-invariant
same-defect holonomy class  
**Audit runner:** `scripts/frontier_planck_cubical_character_deficit_nogo.py`

## Question

After ruling out exact `a = l_P` on the **linear resolved-weight**
same-defect `Spin(3)` class, the next obvious local holonomy route is the
canonical gauge-invariant scalar built from the same curvature loop:

`q_j(eps) = 1 - chi_j(eps) / (2j+1)`,

where `chi_j` is the `Spin(3) ~ SU(2)` character in spin-`j`.

Can that canonical character-deficit scalar force exact Planck on the minimal
cubical defect?

## Bottom line

No.

On the physical cubic lattice, the smallest positive local Regge defect is

`eps_min = pi / 2`.

For that defect, the exact Planck reduction gives

`a^2 / l_P^2 = 8 pi q_j(eps_min) / eps_min = 16 q_j(pi/2)`.

But for every `j in (1/2) Z_(>0)`,

`q_j(pi/2) >= 1 - sqrt(2)/2`,

with equality at the minimal spinor `j = 1/2`.

Therefore

`a^2 / l_P^2 >= 16 (1 - sqrt(2)/2) = 16 - 8 sqrt(2) ~= 4.6862915 > 1`.

So the canonical gauge-invariant same-defect character-deficit class cannot
force exact conventional `a = l_P`.

## Why this is the right class to test

If one rejects a resolved-weight phase as too basis-dependent, the next most
natural same-process scalar is the normalized character itself:

- it is conjugation-invariant;
- it lives on the same local holonomy;
- it is the standard finite-dimensional gauge-invariant scalar built from the
  loop.

So if exact Planck were hiding in a local holonomy scalar, this is one of the
first places it should show up.

## Setup

Use three already-isolated facts:

1. the elementary Planck reduction

   `a^2 / l_P^2 = 8 pi q_* / eps_*`;

2. the cubic Regge bookkeeping already used elsewhere on the branch:
   flat edges have zero deficit, and positive cubical defects come in multiples
   of `pi/2`;
3. the `SU(2)` / `Spin(3)` character formula

   `chi_j(eps) = sin((2j+1) eps / 2) / sin(eps / 2)`.

For the minimal positive cubical defect,

`eps = pi/2`,

the normalized character is

`chi_j(pi/2) / (2j+1) = sqrt(2) * sin((2j+1) pi/4) / (2j+1)`.

So the character-deficit scalar is

`q_j(pi/2) = 1 - sqrt(2) * sin((2j+1) pi/4) / (2j+1)`.

## Exact lower bound

Since

`sin((2j+1) pi/4) <= 1`

and

`2j+1 >= 2`,

we get

`chi_j(pi/2) / (2j+1) <= sqrt(2) / 2`.

Therefore

`q_j(pi/2) >= 1 - sqrt(2)/2`.

Equality is attained at `j = 1/2`, because then

`chi_(1/2)(pi/2) / 2 = cos(pi/4) = sqrt(2)/2`.

So the minimal deficit scalar on this whole class is exactly

`q_min = 1 - sqrt(2)/2`.

## Consequence for Planck

Insert that minimum into the Planck reduction:

`a^2 / l_P^2 = 16 q_min = 16 (1 - sqrt(2)/2) = 16 - 8 sqrt(2)`.

Numerically,

`16 - 8 sqrt(2) ~= 4.686291501`.

This is already well above `1`.

Hence exact conventional `a = l_P` is impossible on the canonical
character-deficit class.

## Comparison with the linear same-defect class

The earlier resolved-weight linear-holonomy classification gave the minimal
spinorial coefficient

`a^2 / l_P^2 = 4 pi ~= 12.566`.

This character-deficit class is more economical, but it still misses exact
Planck:

`16 - 8 sqrt(2) ~= 4.686 < 4 pi`,

yet still

`16 - 8 sqrt(2) > 1`.

So even after switching from a resolved weight to the canonical
gauge-invariant character-deficit scalar, the local same-defect holonomy route
still does not land exact `a = l_P`.

## What this closes

This closes the most natural **gauge-invariant nonlinear** local-holonomy
class on the minimal cubical defect.

Together with the resolved-weight linear classification theorem, we now know:

- the obvious linear same-defect holonomy laws miss exact Planck;
- the obvious canonical character-deficit same-defect holonomy law also misses
  exact Planck.

That makes it much less likely that exact conventional `a = l_P` is hiding in
an elementary local `Spin(3)` holonomy scalar at all.

## What survives

This note still does **not** kill every remaining first-principles route.

What survives is narrower again:

- a more exotic nonlinear holonomy functional than the normalized character
  deficit;
- a nonlocal or boundary-density gravitational carrier;
- an information/action theorem not reducible to a local holonomy scalar.

## The theorem-level statement

**Theorem (minimal cubical character-deficit no-go).**
Assume:

1. the elementary Planck reduction

   `a^2 / l_P^2 = 8 pi q_* / eps_*`;
2. the same elementary curvature process is read by the canonical
   gauge-invariant `Spin(3)` character-deficit scalar

   `q_j(eps) = 1 - chi_j(eps)/(2j+1)`;
3. the local positive cubical defect is the minimal one

   `eps = pi/2`.

Then

`a^2 / l_P^2 >= 16 - 8 sqrt(2) > 1`,

with equality at `j = 1/2`.

Consequently exact conventional `a = l_P` is impossible on this canonical
same-defect character-deficit class.

## Safe wording

**Can claim**

- the canonical gauge-invariant same-defect character-deficit class is now
  ruled out for exact conventional `a = l_P`;
- its best possible cubical coefficient is exactly
  `16 - 8 sqrt(2) ~= 4.68629`;
- the local-holonomy search space is narrower again.

**Cannot claim**

- that every nonlinear holonomy functional is dead;
- that no boundary-density or information/action route can ever work;
- that exact conventional `a = l_P` has been derived.
