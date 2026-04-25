# Koide Q One-Clock Semigroup Value-Law No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_one_clock_semigroup_value_law_no_go.py`  
**Status:** executable no-go for closing `Q` from the positive one-clock
semigroup law alone

## Theorem Attempt

The strongest available positive semigroup route says: after the retained
full-cube / second-order charged-lepton carrier is reduced to positive
three-slot projective data, the physical one-clock repeated-step law should
force an exponential family and perhaps thereby force the source-neutral
Koide point.  The attempted theorem is that positive repeated-clock structure
alone derives `K_TL = 0`, hence `Y = I_2`, `E_+ = E_perp`, `kappa = 2`, and
`Q = 2/3`.

The audit rejects that theorem.  A positive one-clock semigroup forces
exponential form, but not the spectral clock gap.  Even under the stronger
reciprocal one-gap reduction, Koide is equivalent to the missing scalar law

```text
beta * spectral_gap = log((5 + sqrt(21))/2).
```

That law is not supplied by the semigroup axioms.

## Brainstormed Routes And Ranking

1. **One-clock semigroup value law without `H_*`:** strongest novelty and
   direct relevance.  Audit whether exponential repeated-step structure
   fixes the Koide point without observational pins.
2. **Reciprocal generator / determinant-one sharpening:** impose the most
   favorable trace-normalized one-gap spectral shape and test whether Koide
   becomes automatic.
3. **What if the free datum is not the source but the clock?** invert the
   assumption by treating `K_TL = 0` as an emergent endpoint condition and
   ask whether clock continuity selects the endpoint.
4. **What if the branch selector is wrong?** test whether the large branch or
   inverse orientation supplies a retained law instead of a charged-lepton
   fit.
5. **What if full positivity is too strong?** weaken from positive Hermitian
   semigroup to real projective semigroup and check whether the free scalar
   disappears.
6. **Delta pivot only if Q remains blocked:** attempt a Brannen-phase /
   ambient-APS equality derivation without assuming the equality.

Route 1 dominates because it directly attacks the strongest unresolved
positive lane while avoiding resolved no-gos: source-free assumption,
block-exchange, retained source-bank, gauge/Casimir, quartic coefficient,
effective-action tilt, minimal selector, eigenvalue-channel readout,
selected-line radius dependency, entropy prior, Lie/Clifford radius map,
controlled `C3` breaking, non-Schur metric, and full-taste neutrality.

## Exact Reduction

A diagonal positive semigroup has

```text
X_beta = exp(beta diag(g1,g2,g3)).
```

After the irrelevant common scale is removed, the projective three-slot
carrier is

```text
(x, 1, y)
  = (exp(beta(g1-g2)), 1, exp(beta(g3-g2))).
```

The Koide equation on this carrier is

```text
3(x^2 + 1 + y^2) = 2(x + 1 + y)^2,
```

or equivalently

```text
x^2 - 4xy - 4x + y^2 - 4y + 1 = 0.
```

That is a cone equation in two free positive projective gaps.  It is not a
semigroup identity.

## Stronger Reciprocal Audit

Even if the route is strengthened to the determinant-one / reciprocal
one-gap form

```text
(z, 1, z^-1),
```

with `z = exp(beta * spectral_gap)`, the Koide condition becomes:

```text
t = z + z^-1,
Q(t) = (t - 1)/(t + 1),
Q = 2/3  <=>  (t - 5)(t + 1) = 0.
```

For positive `z`, this means

```text
t = 5,
z = (5 +/- sqrt(21))/2.
```

Equivalently:

```text
beta * spectral_gap = log((5 + sqrt(21))/2)
```

up to inverse orientation.  The semigroup law gives
`z(beta+gamma)=z(beta)z(gamma)` once `z(1)` is supplied, but it does not
derive this value of `z(1)`.

## Hostile Review

This no-go does **not** use:

- PDG charged-lepton masses;
- the observational `H_*` pin;
- `K_TL = 0`;
- `K = 0`;
- `P_Q = 1/2`;
- `Q = 2/3` as an input to closure;
- `delta = 2/9`.

The Koide equation is used only as a diagnostic to name the residual scalar
that would be required for closure.  The result therefore cannot be promoted
as a closure theorem.

## Musk Simplification Pass

This is the third failed route in the current corrected loop after:

1. all-axis / pre-EWSB averaging;
2. O3 fourth-order source-balance;
3. one-clock semigroup value law.

The simplification pass leaves the target cleaner:

1. **Make requirements less wrong:** the problem is not "find a positive
   family"; it is "derive one exact source/clock scalar."
2. **Delete:** full-cube averaging, O3 sign-erasure, branch witness matching,
   and observational `H_*` can be removed from the closure proof.
3. **Simplify:** the strongest remaining Q form is a one-scalar identity:
   either `K_TL = 0` on the normalized carrier or an equivalent retained law
   fixing `beta * spectral_gap = log((5 + sqrt(21))/2)`.
4. **Accelerate:** future runners should test whether a proposed retained
   law fixes that scalar exactly, rather than re-auditing broad carrier
   classes.
5. **Automate:** the recurring hostile-review checklist should reject any
   proof whose "derived" scalar is actually one of the forbidden target
   imports.

## Executable Result

```text
PASSED: 14/14

KOIDE_Q_ONE_CLOCK_SEMIGROUP_VALUE_LAW_NO_GO=TRUE
Q_ONE_CLOCK_SEMIGROUP_CLOSES_Q=FALSE
RESIDUAL_SCALAR=beta_gap-log((5+sqrt(21))/2)
```

## Next Strongest Route

The next Q route should invert the remaining assumption: instead of trying to
obtain `K_TL = 0` from carrier symmetry or semigroup positivity, test whether
a retained entropy/Legendre-dual normalization on the already-reduced
two-block source carrier uniquely forces the **identity point** without
silently importing source-freeness.  If that still leaves one scalar, preserve
it as an executable no-go and then pivot only to a delta route that attempts
to derive the physical selected-line Brannen phase from ambient APS without
assuming the equality.
