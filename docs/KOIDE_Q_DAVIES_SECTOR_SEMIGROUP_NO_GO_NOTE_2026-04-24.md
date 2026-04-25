# Koide Q Davies/sector semigroup no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_davies_sector_semigroup_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use an irreversible Markov/Davies semigroup on the retained center sectors to
derive a unique physical source state:

```text
retained sector semigroup -> stationary state -> K_TL = 0.
```

## Executable theorem

With rates

```text
plus -> perp : a
perp -> plus : b,
```

the generator is:

```text
L = [[-a,b],[a,-b]]
```

and the stationary state is:

```text
p_plus = b/(a+b)
p_perp = a/(a+b).
```

Source neutrality requires:

```text
a = b.
```

## Obstruction

Microstate-symmetric dynamics inherited from the rank-1/rank-2 carrier gives
effective sector rates:

```text
a:b = 2:1,
```

and therefore:

```text
(p_plus,p_perp) = (1/3,2/3)
Q = 1
K_TL = 3/8.
```

Quotient-label symmetric rates give:

```text
a:b = 1:1
(p_plus,p_perp) = (1/2,1/2)
Q = 2/3
K_TL = 0.
```

But label-symmetric rates are the missing source law unless independently
derived.

The runner now also verifies the exact microstate lumping.  The symmetric
three-microstate complete-graph generator on the retained carrier has uniform
microstate stationary distribution, but after lumping one singlet microstate
against two doublet microstates it gives:

```text
d p_plus / dt = -2 gamma p_plus + gamma p_perp
d p_perp / dt =  2 gamma p_plus - gamma p_perp
```

so the induced sector rates are again `a:b = 2:1`.

## Detailed-balance family

Detailed balance itself is not a selector.  For any chosen center state
`(u,1-u)`, the rates

```text
a = (1-u) lambda
b = u lambda
```

make that state stationary.  This realizes both:

```text
u = 1/3 -> rank state
u = 1/2 -> label state
```

so a Davies generator becomes a source law only after a retained physical
principle fixes the rate ratio.

## Residual

```text
RESIDUAL_SCALAR = sector_rate_a_minus_b_equiv_center_label_state
RESIDUAL_RATE = quotient_label_rate_equality_not_retained
```

## Why this is not closure

The semigroup route would be a physical source law if the rate ratio were
retained.  Detailed balance and Markov uniqueness do not set that ratio.  The
inherited microstate-symmetric rate ratio points to rank weights, not equal
labels.

## Falsifiers

- A retained Davies generator whose quotient-sector rates are provably equal.
- A physical principle forbidding microstate-symmetric rates in favor of
  label-symmetric rates.
- A derivation of the stationary center state `u=1/2` from irreversible
  dynamics without chosen rates.

## Boundaries

- Covers two-sector continuous-time Markov/Davies generators and detailed
  balance.
- Does not exclude a future retained sector dynamics with derived equal rates.

## Hostile reviewer objections answered

- **"A stationary distribution is physical."**  Yes, once the generator is
  physical.  The retained data do not fix the needed rate ratio.
- **"Equal rates are natural on the quotient."**  They are natural only after
  choosing quotient labels over inherited microstates.
- **"Detailed balance should fix it."**  Detailed balance expresses stationarity
  for a given rate ratio; it does not choose the ratio.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_davies_sector_semigroup_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_DAVIES_SECTOR_SEMIGROUP_NO_GO=TRUE
Q_DAVIES_SECTOR_SEMIGROUP_CLOSES_Q=FALSE
RESIDUAL_SCALAR=sector_rate_a_minus_b_equiv_center_label_state
RESIDUAL_RATE=quotient_label_rate_equality_not_retained
```
