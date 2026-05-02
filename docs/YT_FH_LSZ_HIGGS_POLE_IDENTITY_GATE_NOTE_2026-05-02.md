# FH/LSZ Canonical-Higgs Pole Identity Gate

Status: open / FH-LSZ canonical-Higgs pole identity gate blocking

Claim firewall:

```yaml
actual_current_surface_status: open / FH-LSZ canonical-Higgs pole identity gate blocking
proposal_allowed: false
bare_retained_allowed: false
```

The same-source FH/LSZ readout theorem gives a source-coordinate-invariant
formula,

```text
y_proxy = (dE_top/ds) * sqrt(dGamma_ss/dp^2 at pole)
```

for the scalar source used in both `dE_top/ds` and `C_ss(q)`.  That removes
the forbidden `kappa_s = 1` shortcut, but it does not by itself prove that the
measured scalar source pole is the canonical Higgs radial mode whose kinetic
normalization defines `v`.

This gate makes the remaining physical-identity requirement explicit.  Current
support is real:

- the same-source invariant formula is exact support;
- the same-source `C_ss(q)` measurement primitive is executable;
- the EW/Higgs gauge-mass theorem supplies a canonical-Higgs algebra after a
  canonical doublet is assumed.

The gate still blocks retained use because:

- no production pole fit or `dGamma_ss/dp^2` is present;
- the source-to-Higgs LSZ closure attempt remains blocked;
- existing EW/Higgs notes assume canonical `H` rather than deriving the source
  bridge from the Cl(3)/Z3 source functional;
- gauge-VEV overlap, scalar renormalization-condition, and contact-scheme
  shortcuts are blocked;
- the interacting scalar denominator and `K'(pole)` remain open.

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_higgs_pole_identity_gate.py
# SUMMARY: PASS=11 FAIL=0
```

Boundary:

This does not close PR #230 and does not authorize `retained` or
`proposed_retained`.  A future production FH/LSZ pole measurement still needs
an independent current-surface certificate that the measured pole is the
canonical Higgs radial mode used by `v`.
