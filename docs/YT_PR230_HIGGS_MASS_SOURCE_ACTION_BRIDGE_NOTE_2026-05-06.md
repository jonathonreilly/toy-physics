# PR230 Higgs Mass-Source Action Bridge

**Status:** conditional-support / Higgs mass-source action bridge; same-surface
EW/Higgs action and source-Higgs rows absent.

**Runner:** `scripts/frontier_yt_pr230_higgs_mass_source_action_bridge.py`

**Certificate:** `outputs/yt_pr230_higgs_mass_source_action_bridge_2026-05-06.json`

## Purpose

This note sharpens the clean action-first route.  The existing FMS theorem
derives the local composite expansion after a Higgs action is supplied.  This
bridge adds the source-coordinate part: if a future PR230 same-surface
EW/Higgs action couples the scalar source `s` to the Higgs mass/composite term,

```text
S_EW[s] = S_gauge + S_Higgs + s sum_x (Phi_x^dagger Phi_x - <Phi^dagger Phi>),
```

then

```text
dS_EW/ds = sum_x O_H(x),
O_H = Phi^dagger Phi - <Phi^dagger Phi>.
```

With `Phi^dagger Phi = ((v+h)^2 + pi^a pi^a)/2`, the centered source operator
has

```text
O_H = v h + h^2/2 + pi^a pi^a/2.
```

Thus a real same-surface Higgs mass-source action would supply the
degree-one radial premise with coefficient `v`, not by a symmetry label or FMS
method name.

## Current Result

The theorem checks algebraically and the runner passes `PASS=14 FAIL=0`, but
the current PR230 surface still lacks all load-bearing objects needed for
closure:

- same-source EW/Higgs action certificate;
- canonical `O_H` certificate;
- source-Higgs `C_ss/C_sH/C_HH` pole rows;
- canonical Higgs LSZ normalization, `v`, and Gram/FV/IR checks;
- retained-route approval.

Source rescaling only changes coordinate units; it does not authorize
`kappa_s = 1`.  The measured overlap contract remains
`kappa_spH = Res(C_sH)/sqrt(Res(C_ss) Res(C_HH))`.

## Claim Boundary

This is route support only.  It does not synthesize an EW/Higgs action, does
not write pole rows, does not identify taste-radial `C_sx/C_xx` rows with
canonical `C_sH/C_HH`, and does not claim retained or `proposed_retained`
top-Yukawa closure.

## Verification

```bash
python3 scripts/frontier_yt_pr230_higgs_mass_source_action_bridge.py
# SUMMARY: PASS=14 FAIL=0
```
