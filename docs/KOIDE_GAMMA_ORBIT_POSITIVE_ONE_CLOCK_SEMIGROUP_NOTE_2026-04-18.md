# Koide `Gamma`-Orbit Positive One-Clock Semigroup

**Date:** 2026-04-18  
**Status:** exact reduction of the microscopic value-law target to one positive
generator plus a cone branch on the full-cube route  
**Runner:** `scripts/frontier_koide_gamma_orbit_positive_one_clock_semigroup.py`

## Question

After the exact full-cube `Gamma_i` orbit law, the charged-lepton Koide lane
has been reduced to:

1. a positive block on the reachable `T_2` carrier;
2. two reachable slot values `(v, w)` read from that block;
3. one exact orbit-slot selector cone fixing `u`.

The clean physical-lattice question is therefore:

> if the microscopic law really comes from repeated identical local clock steps
> in `3+1`, does that still leave an arbitrary positive family for `(u,v,w)`?

## Bottom line

No.

If the reachable `T_2` block is produced by a continuous repeated-step
positive Hermitian one-clock law, then the family is forced into the exact
exponential semigroup class
```text
X_beta = exp(beta G)
```
for one unique Hermitian generator `G = log(X_1)`.

So the open microscopic target is no longer:
```text
"find any value law for (u,v,w)".
```
It is now:
```text
"select one Hermitian T_2 generator G, then select one positive cone branch."
```

That is a real reduction.

## Input stack

The reduction uses three exact earlier closures:

1. the full-cube axis-covariant orbit law
   [KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md](./KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md)
2. the exact orbit-slot selector bridge
   [KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md)
3. the repo-wide physical `3+1` one-clock grammar already isolated in the
   determinant-dressed lane
   [DM_EFFECTIVE_PARENT_ONE_CLOCK_TRANSFER_BOUNDARY_THEOREM_NOTE_2026-04-18.md](./DM_EFFECTIVE_PARENT_ONE_CLOCK_TRANSFER_BOUNDARY_THEOREM_NOTE_2026-04-18.md)

The present note is the Koide-side reduction of that same repeated-step logic.

## Theorem 1: positive one-clock semigroup reduction on the reachable `T_2` block

Let `X_beta` be a family of operators on the reachable `T_2` block such that:

1. `X_0 = I`;
2. each `X_beta` is positive Hermitian;
3. repeated identical local clock steps compose:
   `X_(beta+gamma) = X_beta X_gamma`;
4. `beta -> X_beta` is continuous.

Then there exists one unique Hermitian generator `G` such that
```text
X_beta = exp(beta G)
```
for all `beta`.

### Proof

Because `X_1` is positive Hermitian, it has one unique Hermitian logarithm
```text
G = log(X_1).
```
Then
```text
exp(beta G)
```
is a continuous positive Hermitian semigroup with one-clock value `X_1`.

By the semigroup rule, integer powers are already fixed:
```text
X_n = X_1^n.
```
Spectral calculus fixes rational powers uniquely, and continuity fixes all
real `beta`. Therefore the whole family is uniquely determined by `X_1`, hence
by the Hermitian generator `G = log(X_1)`. □

## Corollary 1: the Koide value law is reduced to generator selection plus branch selection

On the exact axis-1 full-cube route, the reachable slot values are read from
the diagonal of `X_beta` in the missing-axis `T_2` basis `(011,101,110)`:
```text
v(beta) = [X_beta]_(110,110),
w(beta) = [X_beta]_(101,101).
```

The exact orbit-slot selector then fixes the `O_0` slot algebraically:
```text
u(beta) = 2(v+w) ± sqrt(3(v^2 + 4vw + w^2)).
```

So once the repeated-step positive law is imposed, the microscopic Koide lane
reduces exactly to:

1. choose one Hermitian generator `G` on `T_2`;
2. choose the physically relevant positive cone branch.

No arbitrary three-slot value family remains.

## Corollary 2: the live `H_*` witness sits inside the exact class

The repo already carries one live Hermitian `T_2` operator
```text
H_* = H(m_*, delta_*, q_+*).
```

Putting the reachable block on
```text
X_beta = exp(beta H_*)
```
therefore does **not** introduce an extra ansatz beyond the one-clock
semigroup class. It is simply one explicit generator choice inside the exact
class forced by Theorem 1.

The companion runner verifies:

- `X_1 = exp(H_*)` is positive Hermitian;
- `log(X_1) = H_*` exactly to machine precision;
- the semigroup law holds numerically:
  `X_(beta+gamma) = X_beta X_gamma`;
- the full family is therefore fixed by the one-clock block `X_1` alone.

## Charged-lepton witness

Inside this exact one-clock class, the small-root branch becomes positive at
one sharp threshold
```text
beta_c ~= 0.5933635.
```

Optimizing the small branch against the charged-lepton `sqrt(m)` direction
gives
```text
beta_* ~= 0.6335715
```
with:
```text
(u_*, v_*, w_*) ~= (0.0440617, 0.6337174, 2.5988159).
```

This candidate lies exactly on the Koide cone and has direction cosine
similarity
```text
0.999999999989
```
against the PDG `sqrt(m)` direction.

So the semigroup class is not empty or generic fluff. It already contains a
near-exact charged-lepton witness.

## Why this is the right positive reduction

This is the cleanest way to respect the user’s caution that the physical
lattice is `3d+1` and that the route should not be pre-cut by `hw=1`
assumptions:

- the argument lives on the full-cube `Gamma_i` route, not on a bare reduced
  `hw=1` triplet by itself;
- it uses repeated local clock composition, which is exactly the natural
  `3+1` physical-lattice question;
- it reduces the free value law to a generator law before any obstruction or
  no-go discussion.

## What remains open

This note does **not** yet derive the physical charged-lepton generator.

The companion note
[KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md)
pushes the exact reduction one step further on the native affine chart: after
the exact observable-selector slice, the generator search collapses to the
one-real line `G_m = H(m, sqrt(6)/3, sqrt(6)/3)`.

So the remaining positive targets are now sharper:

1. derive the charged-lepton `m`-selection law on that exact generator line;
2. derive why the physically relevant branch is the small positive cone branch;
3. if possible, replace the current affine-chart import by a retained
   charged-lepton microscopic generator law.

## Consequence

The Koide lane is on a good positive track.

The full-cube orbit law is exact. The selector bridge is exact. The repeated
local-step requirement now forces the value law into one positive semigroup
class. The exact selector slice then collapses that generator search to a
one-real line. So the next singular target is now:

```text
derive the m-selection law on the selected generator line and the branch selector.
```

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_gamma_orbit_positive_one_clock_semigroup.py
```
