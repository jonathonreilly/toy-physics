# Koide Selected-Line Bare Resolvent Endpoint Boundary

**Date:** 2026-04-20  
**Status:** exact constructive boundary on the current ambient endpoint program  
**Runner:** `scripts/frontier_koide_selected_line_bare_resolvent_endpoint_boundary_2026_04_20.py`

## Question

The current `main` synthesis already reduced the live charged-lepton theorem
burden to one ambient one-clock endpoint law for the selected-line microscopic
scalar

```text
m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3.
```

Before introducing a more elaborate ambient transport law, the smallest local
constructive family worth testing is the **bare missing-axis resolvent family**
on the exact selected line:

```text
W_4(m; h_O0) = diag(h_O0, H_sel(m)),
R_{m,lambda} = (lambda I_4 - W_4(m; h_O0))^{-1},
Sigma_{m,lambda} = P_T1 Gamma_1 R_{m,lambda} Gamma_1 P_T1.
```

Does that family already select the current physical first-branch endpoint
`m_*`?

## Bottom Line

No.

The bare selected-line missing-axis resolvent family can imitate the
charged-lepton packet numerically, but only **away** from the physical
first-branch selected point supplied by the current exact selected-line stack.

For the two smallest exact `O_0` lifts audited here:

- `h_O0 = 0`,
- `h_O0 = Tr(H_sel(m))/3`,

the best first-branch fits both sit far from the physical point

```text
m_* ~= -1.160469470087.
```

For the canonical `h_O0 = 0` family:

- the best first-branch cosine fit is near `(m, lambda) = (0.0000, 0.0400)`,
- the best first-branch Koide fit is near `(m, lambda) = (-0.2102, 0.0300)`,
- the globally strongest cosine fit moves further to the wrong side, near
  positive `m` and small `lambda`,
- while the globally best Koide fit remains the same wrong first-branch
  imitator rather than moving to the physical selected point.

So the missing endpoint theorem is **not** a bare local selected-line
resolvent section.

## Exact Setup

The current selected-line stack already fixes:

- the exact selected generator line
  `H_sel(m) = H3(m, sqrt(6)/3, sqrt(6)/3)`,
- the first-branch positivity threshold
  `m_pos ~= -1.295794904067`,
- the current physical selected point `m_*` from the existing closed internal
  candidate route.

This note tests the smallest natural local ambient family on top of that line:

1. lift `H_sel(m)` to the missing-axis intermediate space `O_0 ⊕ T_2`,
2. apply a scalar resolvent parameter `lambda`,
3. read the returned species operator on `T_1`,
4. score the Hermitian eigenvalue packet against Koide and the charged-lepton
   direction.

That is the strongest reading of this bare family, because earlier
Higgs-dressed-propagator scans already showed the eigenvalue packet is the only
reading that comes close to the charged-lepton packet at all.

## Theorem 1: the bare family is only 2-real on the selected line

Once the exact selected line is fixed, the bare family carries only:

- the endpoint coordinate `m`,
- one local scalar resolvent parameter `lambda`.

So if this family were the missing law, it would already have enough room to
find the physical point.

## Theorem 2: the canonical `h_O0 = 0` family imitates the packet in the wrong place

On the audited first-branch search window

```text
m in [m_pos + 10^-3, 0],   lambda in [0.01, 1.0],
```

the canonical family does produce strong numerical imitators:

- best first-branch cosine fit:
  `m ~= 0.0000`, `lambda ~= 0.0400`,
  `cos ~= 0.99995`, `Q ~= 0.66620`;
- best first-branch Koide fit:
  `m ~= -0.2102`, `lambda ~= 0.0300`,
  `cos ~= 0.99875`, `Q ~= 0.666659`.

But both lie far from the physical first-branch selected point
`m_* ~= -1.16047`.

So the family can fake the packet, but not at the right selected endpoint.

## Theorem 3: the trace-mean `O_0` lift still misses the same endpoint

Replacing the `O_0` slot by the exact trace-mean lift

```text
h_O0 = Tr(H_sel(m)) / 3
```

does not fix the problem.

Its strongest first-branch fits remain near

- `m ~= -0.0052`, `lambda ~= 0.0400` for best cosine,
- `m ~= -0.0493`, `lambda ~= 0.0200` for best Koide,

again more than one unit of `m` away from `m_*`.

So the miss is not just an artifact of setting the singlet lift to zero.

## Theorem 4: widening the search still does not recover the physical endpoint

If the search window is widened to

```text
m in [m_pos + 10^-3, 0.2],
```

the global canonical family still fails in the same qualitative way:

- the globally strongest cosine fit moves to the nonphysical side near
  `m ~= 0.0603`, `lambda ~= 0.0400`,
- the globally best Koide fit remains near the same wrong first-branch point
  `m ~= -0.2093`, `lambda ~= 0.0300`.

So widening the family does not rescue it:

- its strongest directional pressure points to the wrong side of the line,
- and its best Koide-style imitation still sits far from the physical
  selected endpoint.

Either way, the physical endpoint is not selected.

## What This Changes

This note is not a closure. It is the right constructive boundary.

It sharpens the ambient endpoint program by ruling out the smallest obvious
local selected-line family:

- the endpoint law is not a bare local resolvent section of the missing-axis
  lift,
- even though that family is flexible enough to imitate the charged-lepton
  packet numerically,
- because it does so in the wrong place.

So the live theorem burden remains what the endpoint-target note said:

```text
one ambient one-clock endpoint law for m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3.
```

But now we know that law must involve more than a local selected-line
resolvent. The remaining possibilities are things like:

- nonlocal continuation / transport,
- extra ambient Wilson data,
- or a stronger branch law that is not visible inside this bare local family.

## What This Does Not Claim

- It does **not** rule out more structured resolvent families.
- It does **not** rule out ambient transport or Wilson endpoint laws.
- It does **not** alter the current exact selected-line reduction or the
  endpoint-target theorem.

It only closes the smallest local selected-line bare-resolvent hope honestly.
