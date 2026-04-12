# y_t Normalization Blocker: Missing Ward Identity

**Status:** bare UV normalization closed; renormalized matching open

The projector factor in the top-Yukawa lane is now rigorous:

- the staggered mass phase maps to `Gamma_5`
- the chiral projector `P_+ = (1 + Gamma_5)/2` has normalized trace `1/2`
- `N_c = 3` is the color factor

What is still missing is the renormalized matching theorem that turns those
pieces into the gauge-matching step used by the `y_t = g_s / sqrt(6)` relation.

## Missing identity

The exact missing statement is a lattice Ward/Slavnov-Taylor matching identity
of the form:

```text
Z_Y = Z_g
```

or, in the normalized-trace convention used in the lane,

```text
N_c * y_t^2 = g_s^2 * Tr(P_+)/dim(taste)
```

This repo does not currently derive that renormalized identity on the current
surface.

## Imported assumptions

The current theorem chain still imports the following at the renormalized step:

- the gauge and Yukawa vertices share the same lattice link normalization
- the gauge coupling `g_s` is the correct renormalized input to insert into
  the Yukawa normalization step
- no extra independent vertex factor appears between the lattice and
  continuum normalizations

## Honest theorem status

The strongest defensible statement today is:

```text
If the renormalized matching identity fixes the Yukawa normalization to the
gauge-link normalization, then `y_t = g_s / sqrt(6)`.
```

That is a conditional theorem, not a closed normalization derivation.
