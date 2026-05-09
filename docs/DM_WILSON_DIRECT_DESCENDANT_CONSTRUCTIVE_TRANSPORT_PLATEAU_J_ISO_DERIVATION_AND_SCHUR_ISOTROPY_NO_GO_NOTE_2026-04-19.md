# DM Wilson Direct-Descendant Constructive Transport Plateau J_iso Derivation And Schur-Isotropy No-Go

**Date:** 2026-04-19  
**Status:** **(positive)** bounded support theorem — `J_iso` is the exact
law to test on the normalized cubic Schur-side carrier;
**(negative)** no-go — Schur-side spectral isotropy maximization does
**not** keep the certified `W1` winner on the full constructive transport
plateau (it does so only on the witness packet `W0, W1, W2, W3`). The
note is an exact positive-plus-negative closeout on the current DM
constructive-plateau lane; it does **not** promote any upstream lane.
**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_j_iso_derivation_and_schur_isotropy_no_go_2026_04_19.py`

## Question

After the earlier same-day selector notes, two narrower questions remained:

1. can one derive from the retained local Schur-side physics why

   ```text
   J_iso = 27 det(H_e) / Tr(H_e)^3
   ```

   is the law to test, rather than merely a convenient scalar representative;
2. does that same law, or more generally Schur-side spectral isotropy
   maximization, keep the certified `W1` winner on the full constructive
   transport plateau rather than only on the current witness packet
   `W0, W1, W2, W3`?

This note answers both.

## Verdict

The answer splits cleanly into one positive statement and one no-go.

### Positive statement

`J_iso` is indeed the exact law to test on the **normalized cubic Schur-side
carrier**.

Write the positive normalized Schur spectrum of

```text
H_e(L_e) = Herm(L_e^(-1))
```

as `p = (p_1, p_2, p_3)` with `p_i > 0` and `p_1 + p_2 + p_3 = 1`.

Among symmetric cubic laws on that spectrum, require:

- permutation symmetry between the three Schur channels;
- scale-freeness, so the law depends only on the normalized spectrum;
- boundary sensitivity, so the law vanishes whenever any one Schur channel
  collapses (`p_i = 0`);
- normalization to `1` at perfect isotropy
  `p = (1/3, 1/3, 1/3)`.

Those requirements force

```text
J_iso(p) = 27 p_1 p_2 p_3
         = 27 det(H_e) / Tr(H_e)^3
         = 27 Delta_src / (R11 + R22 + R33)^3.
```

So `J_iso` is not arbitrary. It is the unique normalized symmetric cubic law
that treats the three local Schur spectral directions equally and dies when
any one of them disappears.

### Negative statement

That still does **not** give the final retained selector. The global plateau
extension fails.

More sharply:

1. `W1` is not even stationary for `J_iso` on the full constructive
   transport-fiber tangent.
2. there are exact constructive plateau points with the same canonical
   transport column and strictly larger `J_iso` than `W1`;
3. one explicit positive plateau certificate has normalized Schur spectrum
   strictly more isotropic than `W1`, so the whole strictly Schur-concave
   symmetric family also loses `W1` beyond the certified witness set.

So the remaining missing physics is now explicit:

> not “which cubic isotropy scalar?” but “what retained law stops pure
> Schur-side isotropy maximization from running off the interior witness
> toward the plateau boundary?”

## The positive derivation: why J_iso is the exact cubic law

On the normalized spectral simplex, a generic symmetric cubic polynomial may
be written as

```text
F(p) = a sum_i p_i^3
     + b sum_{i != j} p_i^2 p_j
     + c p_1 p_2 p_3.
```

Now impose the retained physical requirements.

### 1. Vanish on complete one-channel collapse

At `p = (1, 0, 0)`,

```text
F(1,0,0) = a,
```

so boundary vanishing forces `a = 0`.

### 2. Vanish on any two-channel boundary face

At `p = (1/2, 1/2, 0)`,

```text
F(1/2,1/2,0) = (a + b) / 4 = b / 4,
```

so boundary vanishing forces `b = 0`.

### 3. Normalize at exact isotropy

At `p = (1/3, 1/3, 1/3)`,

```text
F(1/3,1/3,1/3) = c / 27,
```

so `F = 1` there forces `c = 27`.

Therefore

```text
F(p) = 27 p_1 p_2 p_3 = J_iso(p)
```

is unique.

This is the exact positive answer to the first remaining question. If one
insists on a normalized symmetric cubic Schur law that sees all three local
spectral directions and penalizes any channel collapse, `J_iso` is forced.

## The local no-go: W1 is not even stationary for J_iso on the full plateau

Let `W1` denote the previously certified interior plateau witness. The runner
computes the tangent space to the exact transport fiber through `W1` by
taking the kernel of the reduced favored-column Jacobian. As already known
from the same-day transport-fiber completion theorem, that kernel is `3`-real.

Now project the `J_iso` gradient onto that tangent space.

The result is nonzero:

```text
||P_fiber grad J_iso(W1)|| = 0.353137850840...
```

So `W1` is not stationary for `J_iso` on the full constructive plateau.

This matters because it kills the strongest optimistic reading immediately:
even before looking for a far-away competing plateau point, `W1` already
fails the first-order stationarity test for global `J_iso` maximization on
the exact transport fiber.

## The global no-go: an explicit more-isotropic constructive plateau point

The runner verifies the positive constructive plateau certificate

```text
B_major = (0.93953755, 0.36555755, 0.60460021, 0.12123763, 0.10081751)
```

in fixed-seed source coordinates.

Its observable pack is

```text
(eta_1, gamma, E1, E2, Delta_src)
= (1.052220313052..., 0.0183602566..., 0.0009999963...,
   1.2357727115..., 0.0214225421...).
```

It stays on the same constructive plateau and canonical transport-column
orbit as `W1`, but its normalized Schur spectrum is

```text
(0.83547695..., 0.09947708..., 0.06504596...),
```

while `W1` has

```text
(0.84665011..., 0.11897933..., 0.03437057...).
```

The partial sums satisfy

```text
0.83547695... < 0.84665011...
0.93495404... < 0.96562943...
```

so `B_major` is majorized by `W1`, i.e. it is strictly more isotropic.

Consequences:

- `J_iso(B_major) > J_iso(W1)`:

  ```text
  J_iso(W1)      = 0.093481561087...
  J_iso(B_major) = 0.145962610704...
  ```

- Shannon and Renyi entropies are larger at `B_major`;
- therefore every strictly Schur-concave symmetric law on the normalized
  Schur spectrum prefers `B_major` to `W1`.

So the entire Schur-concave isotropy family loses `W1` once one leaves the
certified witness packet.

## The exact reason: maximizing J_iso drives to the boundary

To see what goes wrong physically, the runner also verifies an explicit
continuation packet of constructive plateau points indexed by shrinking sign
floor `epsilon`:

```text
epsilon = 0.05, 0.02, 0.01, 0.005, 0.001.
```

Each point:

- stays on the exact constructive plateau (`eta_1 = eta_*`);
- keeps the same canonical favored transport column;
- remains constructive positive with `min(gamma, E1, E2) = epsilon`;
- and has source coordinate `y_2 = 10^-6`, i.e. it already sits on a
  constructive source-side boundary face.

Along this packet:

```text
J_iso = 0.1535585..., 0.1618871..., 0.1633249..., 0.1638253..., 0.1641268...
```

strictly increases as `epsilon` decreases.

So the failure mode is now explicit:

> global `J_iso` maximization does not retain the interior `W1` witness; it
> drives toward a constructive boundary face.

## What is now closed

This closes both remaining questions honestly.

### Closed positively

- why `J_iso` is the exact coefficient-free cubic law to test on the local
  Schur carrier;
- why it is not an arbitrary fitted observable combination.

### Closed negatively

- the hope that maximizing `J_iso` on the full constructive plateau retains
  `W1`;
- the stronger hope that the whole Schur-concave isotropy family retains
  `W1` globally.

## What remains open

The missing retained selector ingredient is now narrower:

- a retained law that acts before, or together with, Schur isotropy so that
  the selector does not evacuate to the constructive boundary;
- or an independent retained interior principle that fixes one point in the
  canonical `3`-real transport fiber, after which `J_iso` can remain a
  diagnostic rather than the final maximization principle.

In other words, the branch now knows both:

- the exact local cubic isotropy scalar; and
- the exact reason it is not yet the final retained selector.

## Cross-references

- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_SCHUR_SPECTRAL_ISOTROPY_SELECTOR_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_SCHUR_SPECTRAL_ISOTROPY_SELECTOR_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_NORMALIZED_SCHUR_DETERMINANT_SELECTOR_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_NORMALIZED_SCHUR_DETERMINANT_SELECTOR_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md)
- [`docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`](DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md)

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_constructive_transport_plateau_j_iso_derivation_and_schur_isotropy_no_go_2026_04_19.py
```

Expected:

- `PASS` with `FAIL=0`;
- unique cubic derivation of `J_iso`;
- explicit nonstationarity of `W1` on the full plateau;
- explicit more-isotropic constructive plateau certificate beyond `W0..W3`;
- explicit boundary-drift no-go for global `J_iso` maximization.
