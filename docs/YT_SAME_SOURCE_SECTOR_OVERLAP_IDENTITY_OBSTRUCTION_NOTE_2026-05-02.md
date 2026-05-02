# Same-Source Sector-Overlap Identity Obstruction

Status: exact negative boundary / same-source sector-overlap identity obstruction

Claim firewall:

```yaml
actual_current_surface_status: exact negative boundary / same-source sector-overlap identity obstruction
proposal_allowed: false
bare_retained_allowed: false
```

The gauge-normalized Feynman-Hellmann route cancels a common scalar-source
rescaling, but it still assumes a second identity:

```text
dE_top/ds = k_top y_t / sqrt(2)
dM_W/ds   = k_gauge g2 / 2
y_readout = (g2 / sqrt(2)) (dE_top/ds) / (dM_W/ds)
          = y_t (k_top / k_gauge)
```

Therefore the ratio gives physical `y_t` only if the same-source overlap
identity `k_top = k_gauge` is derived or measured.  A common source coordinate
does not supply that equality by itself.  Common source reparametrizations
rescale `k_top` and `k_gauge` together and cancel in the ratio, but the
sector-overlap ratio `rho = k_top/k_gauge` remains load-bearing.

The runner constructs countermodels with the same static electroweak point and
the same scalar source coordinate.  Holding `rho` fixed, common source scaling
cancels.  Varying `rho` changes the inferred `y_t` while leaving the static
`M_W = g2 v / 2` point untouched.  This is exactly the missing canonical-Higgs
source identity.

Current blockers:

- the same-source W/Z mass-response observable is absent;
- the canonical-Higgs pole identity gate remains blocking;
- the source-to-Higgs LSZ closure attempt remains blocking;
- the gauge-VEV source-overlap no-go blocks using static `v` or observed gauge
  masses as selectors.

Verification:

```bash
python3 scripts/frontier_yt_same_source_sector_overlap_identity_obstruction.py
# SUMMARY: PASS=11 FAIL=0
```

Boundary:

This does not close PR #230 and does not authorize `retained` or
`proposed_retained`.  It sharpens the physical-response route: the next
positive move is a canonical-Higgs source identity theorem, a genuine
same-source W/Z response harness that certifies the shared sector overlap, or
continued seed-controlled FH/LSZ production toward a direct scalar pole
residue measurement.
