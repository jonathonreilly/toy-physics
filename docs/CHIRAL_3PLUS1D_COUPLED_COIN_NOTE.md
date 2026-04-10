# 3+1D Coupled-Coin Scan Note

This note records the first scan of a 3+1D chiral family that interpolates
between the current factorized `2x2 ⊕ 2x2 ⊕ 2x2` coin and a fully coupled
`6x6` unitary family.

## Setup

- Script: `scripts/frontier_chiral_3plus1d_coupled_coin_scan.py`
- Lattice: `n = 17`
- Gravity strength: `5e-4`
- Mass parameter: `theta0 = 0.3`
- Coupling scan: `mix in {0.00, 0.125, ..., 1.00}`

## What Was Tested

1. Low-k dispersion and isotropy
2. A 3D loop/plaquette response on a y-z square interferometer

The direct-sum coin is the `mix = 0` baseline. The coupled family adds a
unitary 6x6 cross-axis mixer on top of the local 2x2 chiral coins.

## Results

Best and worst points from the scan:

- Best KG fit: `mix = 1.00`, `R^2 = 0.4787`, direction CV `= 0.8670`
- Worst KG fit: `mix = 0.00`, `R^2 = 0.0627`, direction CV `= 0.0603`
- Best loop response: `mix = 0.875`, visibility `V = 0.9142`, `R^2 = 0.7004`
- Worst loop response: `mix = 0.00`, visibility `V = 0.0000`

Full scan takeaway:

- Cross-axis coupling materially improves both observables relative to the
  factorized baseline.
- The loop/plaquette response is the clearest win: it jumps from zero at the
  factorized point to a strong modulation near the coupled end of the family.
- The dispersion result improves too, but remains only moderate, so coupling
  is helping but not yet enough to recover a clean isotropic 3D KG law.

## Interpretation

Separability looks like a real blocker, but not the only one.

The factorized baseline is weak on both low-k isotropy and loop response. A
fully coupled coin helps both, which supports the hypothesis that axis
separability is a core architectural limitation. The remaining dispersion gap
suggests that coin coupling alone is not sufficient; the 3+1D transport law
likely still needs a better symmetry-matched generator.
