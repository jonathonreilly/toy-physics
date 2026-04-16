# Review: `codex/p-derivation-package`

## Verdict

Not promotable as a full analytic plaquette-closure package.

The branch contains one real upgrade:

- an exact local `SU(3)` one-plaquette block with an independent Weyl-angle
  cross-check

But it does **not** yet justify rewiring the live package from

- same-surface evaluated plaquette

to

- exact analytic plaquette derivation

because the crucial lift from the local block to the physical 4D vacuum value
is still not theorem-grade on the current repo surface.

## Main blockers

### 1. The `beta -> beta_eff` lift is not currently closed

The note claims

`beta_eff = beta * (3/2) * (2/sqrt(3))^(1/4)`

as an exact gauge-vacuum closure.

The `3/2` coordination factor is fine as a combinatorial incidence factor.

The problem is the `(2/sqrt(3))^(1/4)` factor. On current `main`, that factor
comes from the hierarchy/effective-potential endpoint story, and that story is
still explicitly marked as **not fully closed** as a physical insertion theorem.

So the branch is currently upgrading an open diagnostic/surface into an exact
gauge-vacuum theorem without closing the missing argument.

### 2. The runner validates the local integral, not the full closure

The runner does correctly validate:

- the exact Bessel-determinant one-plaquette block
- the independent Weyl-angle group-integral cross-check

Those are good and should be kept.

But the current “combined closure value” check is effectively tautological:

- it computes `p_full` from the same coded lift formula
- then checks it against the hardcoded number produced by that same formula

That is not evidence that the lift itself has been derived.

### 3. The note overstates what has been shown

The current branch note says:

- exact analytic plaquette value
- exact gauge-vacuum closure
- analytic replacement for the previous computed input

That is too strong for the current support stack.

The exact local one-plaquette block is real.
The full-vacuum lift is still a proposal unless you close the missing theorem.

### 4. Small packaging bug

The command block still points to the wrong machine/path:

- `/Users/jonBridger/Toy Physics`

Fix that before any further review.

## What would make this promotable

You need one of these two outcomes:

### Option A. Actually close the lift theorem

Derive the lift

`beta -> beta * (3/2) * (2/sqrt(3))^(1/4)`

on a gauge-side theorem surface, not by importing the current hierarchy-side
dimensional-compression diagnostic.

That means proving, not assuming:

1. why the local one-plaquette exact block should be evaluated at a lifted
   inverse coupling rather than only at bare `beta`
2. why the `3/2` incidence factor enters multiplicatively at the effective
   inverse-coupling level
3. why the dimension-4 endpoint ratio is the correct physical insertion for the
   gauge vacuum, rather than a hierarchy-side suggestive normalization factor

If you can prove those, then this becomes a real repo-wide upgrade.

### Option B. Demote the branch and keep the valid part

If you cannot yet close the lift theorem, then reposition this as:

- exact local `SU(3)` one-plaquette block
- exact local plaquette expectation formula
- exact Weyl-angle cross-check
- suggestive but not yet theorem-grade full-vacuum lift

That version would be promotable as a support tool, but **not** as a repo-wide
replacement for canonical `<P>`.

## What I would keep even in the demoted version

- the one-plaquette Toeplitz/Bessel determinant
- the derivative formula for `P_1plaq(beta_loc)`
- the Weyl-angle integration cross-check
- the clean numerical outputs showing:
  - `P_1plaq(6) = 0.422531739649983`
  - the proposed lifted value lands near the existing canonical `0.5934`

That is useful science even if the full closure is not yet landed.

## What I would not do yet

Do **not**:

- rewire canonical `P`
- rewire `u_0`
- rewire `alpha_s(v)`
- rewrite the paper or front door to call the plaquette analytic

until the lift theorem itself is actually closed.

## Bottom line

This branch is promising, and it may become important.

If the lift theorem closes, it materially strengthens the project because it
would upgrade the whole

`<P> -> u_0 -> alpha_s(v)`

stack.

But right now the branch only cleanly closes the **local** exact block, not the
full physical vacuum plaquette.
