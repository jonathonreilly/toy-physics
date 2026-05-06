# PR230 Logdet Hessian Neutral-Mixing Attempt

Status: exact negative boundary / source-only staggered logdet Hessian does not
derive the neutral Higgs mixing bridge.

## Question

Can the staggered determinant itself supply the missing PR230 bridge?
Specifically, can the one-source logdet/Hessian surface for the PR230 mass
source determine the canonical neutral Higgs direction, source-Higgs Hessian
rows, or an off-diagonal neutral generator?

## Counterfamily

Use the two-source determinant family

```text
D(s,h; eps) = [[1+s, eps h],
               [eps h, 1]]

W_eps(s,h) = log det D = log(1+s - eps^2 h^2).
```

For every value of `eps`,

```text
W_eps(s,0) = log(1+s).
```

Thus every source-only derivative of the determinant is identical.  However,

```text
partial_h^2 W_eps |0 = -2 eps^2
partial_s partial_h^2 W_eps |0 = 2 eps^2
```

and the off-diagonal neutral generator norm also varies with `eps`.

The determinant stays positive near the origin for the tested values
`eps = 0, 0.25, 0.75`, so positivity does not select the bridge.

## Consequence

The current PR230 source-only determinant surface `W(s,0)` underdetermines the
two-source functional `W(s,h)`.  It names the source response tower, but it
does not define `h`, does not identify `O_H`, and does not produce
`C_sH/C_HH` or a neutral primitive transfer certificate.

This is narrower than the existing effective-potential Hessian no-go: it tests
the determinant/logdet route directly and shows why the missing object is not
a scalar curvature but a same-surface second source/operator.

## Firewalls

This attempt does not use:

- `H_unit`;
- `yt_ward_identity_derivation_theorem`;
- minimal-axioms y_t/m_t summary rows as proof authority;
- observed top mass or observed `y_t`;
- `alpha_LM`, plaquette, `u_0`, or `R_conn`;
- `y_t_bare`;
- `c2 = 1`, `Z_match = 1`, or `kappa_s = 1`.

## Verification

```bash
python3 scripts/frontier_yt_pr230_logdet_hessian_neutral_mixing_attempt.py
# SUMMARY: PASS=17 FAIL=0
```

## Exact Next Action

Either construct a two-source PR230 functional `Z(s,h)` with a same-surface
canonical `O_H` certificate, or derive a true neutral off-diagonal/primitive
transfer theorem.  Source-only determinant/Hessian data are not enough.
