# DM Wilson Direct-Descendant Transport-Fiber Minimal Local Spectral-Law No-Go

**Date:** 2026-04-19  
**Status:** exact search-plus-no-go on the completed local spectral carrier

After the same-day spectral-completion theorem, the unresolved direct-descendant
selector problem was no longer vague. The live local fiber above the canonical
transport column is exactly the `3`-scalar spectral carrier

```text
(T, Q, Delta) = (Tr(H_e), Tr(H_e^2), det(H_e)),
```

with

```text
H_e = (L_e^(-1) + (L_e^(-1))^*) / 2.
```

The honest next question is then:

> does a minimal exact law on those three local scalars already select the
> current interior physical-source candidate, or do the natural low-complexity
> classes still fail?

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_transport_fiber_minimal_local_spectral_law_no_go_2026_04_19.py`
(`PASS=17 FAIL=0`).

## Bottom line

No exact selector is found in the natural low-complexity local spectral
classes.

The result splits into one positive search outcome and one structural no-go.

### Positive search outcome

On the explicit competitor set

- the certified interior plateau witnesses `W0, W1, W2, W3`,
- the more-isotropic boundary-drifting certificate `B_major`,
- and the explicit shrinking-sign-floor boundary packet,

the unique minimal positive coefficient-free monomial that selects `W1` is

```text
Q Delta = Tr(H_e^2) det(H_e).
```

So the completed spectral carrier does support a first simple
boundary-suppressing candidate.

### Structural no-go

That still does **not** give an exact interior selector.

The exact reason is that the same-day spectral-completion theorem already made

```text
(T, Q, Delta)
```

local coordinates on the `3`-real transport fiber.

Therefore:

1. any nonconstant affine law in `(T, Q, Delta)` has constant nonzero gradient
   in those local coordinates, so it cannot have an interior exact maximizer;
2. any nontrivial monomial law

   ```text
   T^a Q^b Delta^c
   ```

   has gradient

   ```text
   law * (a/T, b/Q, c/Delta),
   ```

   which also never vanishes at a positive interior point unless the law is
   constant;
3. any scale-free law factors through the normalized pair

   ```text
   (q2, q3) = (Q/T^2, Delta/T^3),
   ```

   and that normalized map has rank `2` on the `3`-real transport fiber, so
   canonically normalized laws are locally under-complete: they leave a
   `1`-real local degeneracy.

So the completed spectral data identify the local selector coordinates, but no
natural exact low-complexity selector law on them survives.

## What the runner proves

### 1. No single completed scalar selects `W1`

On the explicit competitor set:

- `max T -> W0`,
- `max Q -> W0`,
- `max Delta ->` a boundary-drifting packet point,
- and the canonically normalized determinant ratio

  ```text
  q3 = Delta / T^3
  ```

  also prefers the boundary packet.

So the raw single-scalar and simplest normalized single-scalar routes are both
closed.

### 2. Scale-free laws are structurally too small

Because scale normalization collapses `(T, Q, Delta)` to `(q2, q3)`, any
scale-free law sees only two local spectral coordinates.

But the local transport fiber is `3`-real. The runner checks that the
restricted Jacobian of

```text
source5 -> (q2, q3)
```

has rank `2` at every known plateau witness.

So a scale-free local law cannot exactly isolate a point of the fiber. At
best it can reduce the `3`-real fiber to a `1`-real residual normalized-spectral
subfiber.

This is the exact local reason the earlier normalized Schur-isotropy and
`J_iso` programs could never have been the whole answer.

### 3. The first simple boundary-suppressing raw monomial is `Q Delta`

The runner searches positive coefficient-free monomials in `(T, Q, Delta)` by
total degree.

Results:

- degree `1`: no winner is `W1`;
- degree `2`: the unique `W1` winner is

  ```text
  Q Delta = Tr(H_e^2) det(H_e).
  ```

Moreover, on the explicit boundary-drift packet, `Q Delta` decreases as the
sign floor shrinks. So this candidate does exactly what one hoped a minimal
raw spectral law might do:

- it rejects the explicit normalized-isotropy drift;
- it keeps the current interior candidate `W1` above the known boundary packet.

### 4. Even that minimal candidate is not exact

The same runner then checks the exact transport-fiber tangent through `W1`.

For `Q Delta`, the projected transport-fiber gradient is nonzero:

```text
||P_fiber grad(Q Delta)(W1)|| = 0.080118232647...
```

and a small ascent step:

- increases `Q Delta`,
- keeps the favored column fixed to first order,
- keeps `eta_1` fixed to first order,
- and stays inside the constructive positive chamber.

So `Q Delta` is only a **packet-separating candidate**, not an exact local
selector.

This is not an accident of that one monomial. It is the generic monomial
no-go implied by the local-coordinate theorem above.

### 5. Affine laws are also not retained selector content

If one allows arbitrary coefficients, affine laws in `(T, Q, Delta)` can be
tuned to select `W1` on the finite competitor packet. But the same family can
also be tuned to select `B_major` instead.

So affine spectral laws fail for the same basic reason as the earlier
observable-affine lane:

> the coefficients are extra selector input, not derived physics.

And even beyond that discrete tuning issue, no nonconstant affine law can be
an exact interior selector because its gradient in the local spectral
coordinates is constant and nonzero.

## Verdict

The clean verdict on the completed local spectral carrier is:

```text
minimal exact low-complexity local spectral law: ruled out.
```

More sharply:

- **minimal explicit packet-separator found:**  
  `Q Delta = Tr(H_e^2) det(H_e)`;
- **exact selector in natural low-complexity classes:**  
  no-go for
  - scale-free / canonically normalized laws,
  - raw affine laws,
  - raw monomial laws.

The exact reason is now clear:

- normalized laws throw away one of the three required local spectral
  directions;
- raw affine/monomial laws keep all three directions but are too rigid to
  produce an interior critical selector on that local coordinate chart.

## Why this matters

This compresses the post-completion frontier further.

The branch no longer lacks the local data. It has the right local data exactly.
What it lacks is the **higher-order retained principle** that uses those three
scalars in a genuinely interior way.

So the remaining science is no longer

> “find some local scalar on `H_e`.”

It is now

> derive the retained local law on the completed spectral carrier that is
> neither merely scale-free nor merely low-order algebra in the raw
> coordinates.

## What this closes

- the hope that one raw completed scalar already selects the interior source;
- the hope that a canonically normalized scale-free spectral law can exactly
  fix the source after the `3`-scalar completion;
- the hope that the raw affine or monomial classes already contain the final
  selector.

## What this does not close

- a higher-order or otherwise retained local law on `(T, Q, Delta)`;
- a derivation from retained Wilson / `Cl(3)` physics of why one nontrivial
  interior law is physical;
- the final DM flagship selector.

## Cross-references

- [`docs/DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_NORMALIZED_SCHUR_DETERMINANT_SELECTOR_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_NORMALIZED_SCHUR_DETERMINANT_SELECTOR_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_J_ISO_DERIVATION_AND_SCHUR_ISOTROPY_NO_GO_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_J_ISO_DERIVATION_AND_SCHUR_ISOTROPY_NO_GO_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_OBSERVABLE_AFFINE_NO_GO_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_OBSERVABLE_AFFINE_NO_GO_NOTE_2026-04-19.md)

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_transport_fiber_minimal_local_spectral_law_no_go_2026_04_19.py
```

Expected:

- `PASS=17 FAIL=0`;
- no single raw or normalized scalar winner at `W1`;
- rank `3` for raw `(T,Q,Delta)` and rank `2` for normalized `(Q/T^2,Delta/T^3)`
  on the transport fiber;
- unique degree-2 packet-separating monomial `Q Delta`;
- exact no-go for normalized, affine, and monomial low-complexity laws.
