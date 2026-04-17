# PMNS Commutant Eigenoperator Selector

**Date:** 2026-04-16  
**Status:** positive native selector law from the projected commutant route, but not full microscopic closure  
**Script:** `scripts/frontier_pmns_commutant_eigenoperator_selector.py`

## Question

Can a non-`Cl(3)` projected commutant eigenoperator on the `hw=1` triplet
produce an axiom-native value law for the unresolved PMNS microscopic data?

## Bottom line

Yes, but only partially.

The projected commutant route produces an exact selector law on the `hw=1`
corner orbit:

- the `C3`-even Fourier mode is the passive offset class
- the `C3`-odd Fourier mode is the branch / orientation selector

So this route fixes:

- the sector-orientation selector, as one bit
- the passive offset class, as a `Z_3` label

It does **not** fix:

- the active seed pair
- the active `5`-real corner-breaking source

## Exact construction

Start from the exact `Cl(3)` on `Z^3` generation boundary:

- build the projected commutant on each `hw=1` corner
- pick a projected commutant generator outside the projected `Cl(3)` span
- lift that projected eigenoperator back to the ambient taste space
- compare its corner projections on `X_1, X_2, X_3`
- decompose the resulting corner profile into the `C3` Fourier modes

For the corner profile `v = (v_1, v_2, v_3)`, define

`v_0 = (v_1 + v_2 + v_3) / 3`

`v_1 = (v_1 + ω v_2 + ω^2 v_3) / 3`

`v_2 = (v_1 + ω^2 v_2 + ω v_3) / 3`

with `ω = exp(2πi/3)`.

Then:

- `v_0` is the `C3`-even passive mode
- `v_1, v_2` are the `C3`-odd orientation modes
- the odd mode is nonzero on the demonstrated projected non-`Cl(3)`
  generator

## Exact theorem statement

**Theorem (PMNS commutant eigenoperator selector).**  
On the `hw=1` triplet, the projected commutant eigenoperator route yields an
exact native selector law:

1. the `C3`-even Fourier mode of the lifted projected commutant generator
   fixes the passive offset class
2. the `C3`-odd Fourier mode fixes the branch / orientation selector
3. the route does not access enough data to determine the active seed pair or
   the active `5`-real corner-breaking source

Therefore the route gives a positive value law for the selector side, but it
is not a full PMNS microscopic closure theorem.

## Canonical demonstration

On the canonical projected generator used by the runner, the resulting reduced
selector law has:

- branch bit `tau = 0`
- passive offset label `q = 2`

Those are representative values of the selector law on the demonstrated
projected eigenoperator; the theorem-level content is the existence of the
`C3`-even / `C3`-odd split and the fact that it does not reach the active
`5`-real source.

## Consequence

This route closes the selector-parity subproblem, but it does not close the
full microscopic PMNS value problem. The unresolved active source still needs
a separate native law.

## Command

```bash
python3 scripts/frontier_pmns_commutant_eigenoperator_selector.py
```
