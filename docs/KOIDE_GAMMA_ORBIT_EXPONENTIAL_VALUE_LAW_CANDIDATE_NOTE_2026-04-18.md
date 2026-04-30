# Koide `Gamma`-Orbit Exponential Value-Law Candidate

**Date:** 2026-04-18  
**Status:** positive one-parameter witness inside the exact one-clock semigroup
class on the `Gamma_i` / full-cube route  
**Runner:** `scripts/frontier_koide_gamma_orbit_exponential_value_law_candidate.py`

## Question

After the exact full-cube orbit law, the remaining positive basis-free target
is the microscopic value law for the three-slot template
```text
(u, v, w).
```

Once the full-cube route is reduced to a microscopic three-slot law `(u,v,w)`,
is there a simple positive generator choice already visible in the repo’s live
microscopic objects?

## Bottom line

Yes. There is a sharp one-parameter witness family.

Take the live Hermitian
```text
H_* = H(m_*, delta_*, q_+*)
```
from the repo’s neutrino-sector pin, and put the reachable `T_2` block on the
positive semigroup family
```text
X_beta = exp(beta H_*).
```

In the missing-axis `T_2` basis `(011, 101, 110)`, the axis-1 reachable slots
are `101` and `110`, so the exact orbit-slot values are
```text
v(beta) = [X_beta]_{110,110},
w(beta) = [X_beta]_{101,101}.
```

Then the pulled-back Koide selector fixes the `O_0` slot algebraically:
```text
u(beta) = 2(v+w) ± sqrt(3(v^2 + 4vw + w^2)).
```

The small-root branch is the charged-lepton candidate. At
```text
beta_* ~= 0.6335716
```
it gives:
```text
(u_*, v_*, w_*) ~= (0.0440617, 0.6337174, 2.5988159),
```
which lies **exactly** on the Koide cone and has amplitude-direction cosine
similarity
```text
0.999999999989
```
against the PDG `sqrt(m)` direction.

After one overall scale fit, the predicted amplitudes are within `0.03%` of
the observed charged-lepton `sqrt(m)` values.

By
`KOIDE_GAMMA_ORBIT_POSITIVE_ONE_CLOCK_SEMIGROUP_NOTE_2026-04-18.md`,
the exponential form is exactly the right class once repeated identical local
clock steps are required. So this note should now be read as an explicit
generator witness inside that exact class, not as a free-form ansatz.

## Exact setup

The earlier notes already proved:

1. one local full-cube template generates the exact `Gamma_i` orbit family  
   [KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md](./KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md)
2. the selector pulls back to the orbit-slot cone  
   [KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md)

So the only remaining choice is the value law on the three-slot template.

The simplest live generator choice on disk is:
```text
W_1(beta, u)
  = u P_{O_0} + X_beta on T_2,
X_beta = exp(beta H_*).
```

Because `H_*` is Hermitian, `exp(beta H_*)` is positive Hermitian for every
real `beta`. The companion one-clock semigroup note shows this is also the
exact finite-dimensional repeated-step class.

## Exact slot formulas

In the missing-axis `T_2` order `(011, 101, 110)`, the axis-1 reachable slots
are:

- species 2 -> `110`
- species 3 -> `101`

Therefore:
```text
v(beta) = [exp(beta H_*)]_{33},
w(beta) = [exp(beta H_*)]_{22}.
```

The orbit-slot cone
```text
u^2 + v^2 + w^2 = 4(uv + uw + vw)
```
is quadratic in `u`, so it fixes `u(beta)` exactly:
```text
u(beta) = 2(v+w) ± sqrt(3(v^2 + 4vw + w^2)).
```

So the candidate family is exact and explicit.

## Numerical charged-lepton fit

Optimizing the small-root branch against the observed `sqrt(m)` direction gives
```text
beta_* ~= 0.6335716.
```

At that value:
```text
(u_*, v_*, w_*) ~= (0.0440617, 0.6337174, 2.5988159).
```

These satisfy:
```text
(u_*^2 + v_*^2 + w_*^2) / (u_* + v_* + w_*)^2 = 2/3
```
exactly to machine precision, and the normalized amplitude direction is
```text
(0.016470, 0.236875, 0.971401),
```
versus the PDG direction
```text
(0.016473, 0.236877, 0.971400).
```

That is effectively exact at the level of this candidate search.

After one overall scale fit, the amplitudes are:
```text
(0.71468, 10.27891, 42.15285),
```
versus PDG
```text
(0.71484, 10.27903, 42.15282),
```
with maximum relative deviation below `0.03%`.

## Why this matters

This is the first genuinely small positive generator witness on the exact
physical-lattice route that:

- uses the exact three-slot `Gamma_i` template law,
- uses a positive spectral family already native to the repo,
- lands **exactly** on the Koide cone,
- and matches the charged-lepton amplitude direction essentially perfectly.

That is a much stronger positive foothold than “some unknown value law may
exist.”

## What it does not yet prove

This note does **not** yet prove a retained charged-lepton derivation.

It still uses:

- the observationally pinned neutrino-sector `H_*`,
- and the exact selector cone as an input fixing the `O_0` slot.

So this is a sharp positive generator witness, not a promoted retained theorem.

## Consequence

The live positive target is now even sharper than before:

1. explain why the physical charged-lepton route should select one Hermitian
   generator close to `H_*`;
2. explain why the relevant branch is the small-root cone branch;
3. then replace the observational `H_*` input by a retained charged-lepton
   microscopic generator if possible.

## Bottom line

The exact `Gamma_i` / full-cube route now has a concrete positive generator
witness:

```text
X_beta = exp(beta H_*) on T_2,
u(beta) fixed by the orbit-slot Koide cone,
beta_* ~= 0.6335716 on the small-root branch.
```

That candidate lands almost exactly on the observed charged-lepton amplitude
direction.
