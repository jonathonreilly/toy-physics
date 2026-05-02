# PR #230 Effective-Mass Plateau Residue No-Go

**Status:** exact negative boundary / effective-mass plateau not scalar LSZ residue closure  
**Runner:** `scripts/frontier_yt_effective_mass_plateau_residue_no_go.py`  
**Certificate:** `outputs/yt_effective_mass_plateau_residue_no_go_2026-05-02.json`

## Claim Tested

This block tests a production-postprocess shortcut: once same-source scalar
two-point data exist, can a finite Euclidean-time effective-mass plateau fix
the source-pole residue needed for the FH/LSZ readout?

No.  A finite plateau window is not an LSZ amplitude theorem.

## Witness

The runner builds positive multi-exponential correlators

```text
C(t) = Z_0 exp(-m_0 t) + sum_i Z_i exp(-m_i t)
```

and holds the same finite time window fixed.  Since `C(t)` is identical on
that window, the effective masses `log(C(t)/C(t+1))` are identical as well.
The ground/source-pole residue `Z_0`, however, varies by a factor of ten across
the positive family.

## Result

Finite-time plateau evidence can be useful diagnostics for future production
data, but it cannot be load-bearing for PR #230 retained closure without an
extra acceptance premise:

- a spectral gap or pole-saturation theorem;
- a model-class or continuum certificate that makes the residue interval
  tight;
- FV/IR/zero-mode control;
- source-pole-to-canonical-Higgs identity.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It does
not set `kappa_s = 1`, `c2 = 1`, or `Z_match = 1`, and it does not use
`H_unit`, `yt_ward_identity`, observed top mass, observed `y_t`, `alpha_LM`,
plaquette, or `u0` as proof authority.

## Next Action

Process seed-controlled chunks through the combiner when they finish, but keep
finite-time plateau amplitudes non-load-bearing until a spectral-gap/model-
class/FV/IR/Higgs-identity certificate is present.
