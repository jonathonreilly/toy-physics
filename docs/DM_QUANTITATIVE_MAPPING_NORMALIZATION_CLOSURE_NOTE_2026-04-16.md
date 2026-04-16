# DM Quantitative Mapping / Normalization Closure

**Date:** 2026-04-16  
**Script:** `scripts/frontier_dm_quantitative_mapping_normalization_closure.py`  
**Framework convention:** “axiom” means only `Cl(3)` on `Z^3`

## Question

After the transport-side exact chain and the PMNS-assisted selector program,
the remaining open quantitative DM question on the branch was:

> once the baryon denominator is fixed theorem-grade, does the canonical
> normalized DM numerator actually complete the final quantitative map?

This note closes that remaining quantitative gate.

## Inputs now used as authority

The theorem runner is downstream of four existing science surfaces:

1. **Theorem-grade PMNS selector closure**
   - unique global minimum on the exact reduced `N_e` seed surface
   - selected branch gives `eta / eta_obs = 1`

2. **Gauge-normalization rigidity**
   - no independent bare gauge-normalization parameter remains
   - canonical statement: `g_bare = 1`

3. **Direct-observable numerator authority**
   - `sigma v = C alpha^2 / m^2`
   - `C -> pi` on the physical continuum branch

4. **Lattice-native Coulomb bridge**
   - Sommerfeld enhancement uses the lattice Green's-function Coulomb kernel

So this closure theorem is not a new free fit. It is the composed quantitative
map on the now-fixed authority chain.

## Exact quantitative chain

The structural base ratio is exact:

\[
R_{\rm base}
  = \frac{3}{5}
    \frac{C_F \, \dim{\rm adj}(SU(3)) + C_2(SU(2)) \, \dim{\rm adj}(SU(2))}
         {C_2(SU(2)) \, \dim{\rm adj}(SU(2))}
  = \frac{31}{9}.
\]

Canonical normalization gives

\[
\alpha_{\rm bare} = \frac{1}{4\pi},
\qquad
\alpha_{\rm plaq} = 0.0922649926183602.
\]

On the retained freeze-out branch `x_F = 25`, the channel-weighted
Sommerfeld factor is

\[
S_{\rm vis} = 1.591795769509086.
\]

Therefore the final normalized dark-to-baryon ratio is

\[
R = R_{\rm base} S_{\rm vis}
  = 5.48285209497574.
\]

Using the theorem-grade PMNS-selected denominator (`eta / eta_obs = 1`), this
first fixes the baryon density through the standard BBN conversion

\[
\Omega_b h^2 = 3.6515 \times 10^{-3}\,\eta_{10},
\qquad
\eta_{10} = \eta / 10^{-10},
\]

so on the selected branch

\[
\Omega_b = 0.04919295758525652.
\]

The final DM density then maps to

\[
\Omega_{\rm DM} = R \, \Omega_b
                = 0.26971771055437643
\]

on the current branch normalization.

## Numerical read

With observed comparators only for validation:

- `Omega_b,obs = 0.049`
- `Omega_b = 0.04919295758525652`
- `Omega_b / Omega_b,obs = 1.003937909903`

- `R_obs = 5.469387755102041`
- `R = 5.48285209497574`
- `R / R_obs = 1.002462506`

and

- `Omega_DM,obs = 0.268`
- `Omega_DM = 0.26971771055437643`
- `Omega_DM / Omega_DM,obs = 1.006409367740`

So the final quantitative map is now closed at the percent level with no
observed `Omega_b` inserted on the authority path.

## Meaning

This closes the second live DM gate on the branch:

- theorem-grade PMNS selector closure: closed
- final quantitative mapping / normalization closure: closed

The old one-flavor theorem-native transport lane still undershoots badly by
itself, but the PMNS-assisted flagship route now has both the selector and the
final normalized quantitative map.

## Command

```bash
python3 scripts/frontier_dm_quantitative_mapping_normalization_closure.py
```
