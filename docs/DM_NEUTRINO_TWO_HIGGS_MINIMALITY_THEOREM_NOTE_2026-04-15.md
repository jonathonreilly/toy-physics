# DM Neutrino Two-Higgs Minimality Theorem

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
**Script:** `scripts/frontier_dm_neutrino_two_higgs_minimality_theorem.py`

## Question

After the universal-Yukawa no-go and the odd-circulant CP tool, what is the
smallest exact local `Z_3` extension that can possibly supply the non-diagonal
Hermitian kernel the DM leptogenesis denominator now needs?

## Bottom line

A neutrino two-Higgs lane with **distinct Higgs charges**.

More sharply:

- every fixed-charge single-Higgs lane is monomial, so `Y^dag Y` is diagonal
- a two-Higgs lane with repeated charge is still effectively single-Higgs
- two distinct charges are the first exact local escape
- every distinct-charge pair is support-equivalent to one canonical class
  `A + B C`
- on that class, the DM odd-circulant CP-supporting right-Gram target already
  lives on the exact admissible subcone `d >= 2 r`

So once nonzero local DM CP support is required, the canonical distinct-charge
two-Higgs lane is the **unique minimal exact local escape** on the current
stack.

## Inputs

This theorem combines:

- the single-Higgs monomial obstruction
- the two-Higgs neutrino escape theorem from the local neutrino lane
- the universal-Yukawa leptogenesis no-go
- the DM odd-circulant CP tool
- the DM two-Higgs right-Gram bridge theorem

The point is to turn those separate facts into one DM-side route-selection
statement.

## Single-Higgs and repeated-charge lanes are too small

For any fixed Higgs charge,

`Y = D P_q`

with `P_q` one of the three exact support permutations. Therefore

`Y^dag Y = P_q^dag D^dag D P_q`

is diagonal.

So every fixed-charge single-Higgs lane is exactly CP-empty at the level of the
Hermitian kernel used by leptogenesis.

The same is true for a two-Higgs lane with repeated charge:

`Y = D_a P_q + D_b P_q = (D_a + D_b) P_q`,

so it is still effectively one Higgs and still gives diagonal `Y^dag Y`.

## Two distinct Higgs charges are the first local escape

If two distinct Higgs charges are active,

`Y = D_a P_a + D_b P_b`

with `P_a != P_b`.

Then generically:

- the support has six entries rather than three
- the texture is no longer monomial
- the right-Gram kernel `Y^dag Y` becomes non-diagonal

So two distinct charges are the first exact local class that can carry the kind
of kernel DM now needs.

## The charge-pair label is not a real remaining ambiguity

There are only three unordered distinct-charge pairs:

- `(0,1)`
- `(0,2)`
- `(1,2)`

For each pair, right-multiplying by the first support and conjugating by a
generation relabeling reduces the relative support to the same forward cycle
`C`.

So every distinct-charge pair reduces to one canonical class

`Y = A + B C`.

The local two-Higgs escape is therefore canonical up to relabeling.

## Connection to the DM CP-supporting target

The DM odd-circulant CP tool identified the exact algebraic target

`mu I + nu (S + S^2) + i eta (S - S^2)`.

The DM two-Higgs right-Gram bridge then proved that the induced Hermitian
circulant kernel is realized on the canonical two-Higgs lane exactly on the
subcone

`d >= 2 r`.

So the DM target is not just compatible with the two-Higgs lane in some loose
sense. It already sits on that unique minimal local escape.

## Theorem-level statement

**Theorem (DM-side minimality of the canonical distinct-charge two-Higgs
neutrino lane).** On the current exact local `Z_3` neutrino flavor stack:

1. every fixed-charge single-Higgs lane gives diagonal `Y^dag Y`
2. every repeated-charge two-Higgs lane reduces to the same diagonal class
3. every distinct-charge two-Higgs lane is support-equivalent up to relabeling
   to the canonical class `A + B C`
4. the DM odd-circulant CP-supporting right-Gram family is realized on that
   canonical class on the exact admissible subcone `d >= 2 r`

Therefore, once nonzero local DM CP support is required, the canonical
distinct-charge two-Higgs neutrino lane is the **unique minimal exact local
escape** on the current stack.

## What this closes

This closes the planning ambiguity around the local neutrino extension.

The branch no longer needs to ask:

- whether one Higgs can still somehow work
- whether repeating the same Higgs charge might help
- whether some smaller exact local extension than the two-Higgs class remains
  untested

Those routes are closed.

## What this does not close

This note does **not** yet derive:

- the two-Higgs extension from the bare axiom alone
- the seven canonical two-Higgs quantities
- the right-sensitive sheet datum
- the exact odd-circulant coefficient law

So it is a route-selection theorem, not full two-Higgs closure.

## Safe wording

**Can claim**

- the canonical distinct-charge two-Higgs neutrino lane is the unique minimal
  exact local escape once nonzero local DM CP support is required
- no smaller exact local neutrino extension remains on the current stack

**Cannot claim**

- the bare axiom already forces two Higgs with no bridge condition
- the local two-Higgs coefficients are already derived

## Command

```bash
python3 scripts/frontier_dm_neutrino_two_higgs_minimality_theorem.py
```

