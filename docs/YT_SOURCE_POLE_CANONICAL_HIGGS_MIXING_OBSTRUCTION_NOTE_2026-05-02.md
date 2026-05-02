# Source-Pole Canonical-Higgs Mixing Obstruction

Status: exact negative boundary / source-pole canonical-Higgs mixing obstruction

Claim firewall:

```yaml
actual_current_surface_status: exact negative boundary / source-pole canonical-Higgs mixing obstruction
proposal_allowed: false
bare_retained_allowed: false
```

The same-source FH/LSZ readout can determine the top coupling to the scalar
pole created by the source operator `O_s`.  It becomes the physical top
Yukawa only after that pole is identified with the canonical Higgs radial mode
whose VEV defines `v`.

The obstruction is a two-scalar mixing freedom:

```text
|source pole> = cos(theta) |h_canonical> + sin(theta) |chi_orthogonal>
y_source = y_t cos(theta)        if the top couples only to h_canonical
y_t = y_source / cos(theta)
```

The runner holds the same-source pole residue, the same-source FH/LSZ readout,
and the static electroweak point fixed while varying `cos(theta)`.  The
canonical `y_t` changes unless `cos(theta) = 1` is derived or measured.

Current blockers:

- the canonical-Higgs pole identity gate remains blocking;
- the source-to-Higgs LSZ closure attempt remains blocking;
- the same-source sector-overlap identity is not derived;
- the denominator / `K'(pole)` stack is still open;
- static `v` and gauge masses cannot be used as proof selectors.

Verification:

```bash
python3 scripts/frontier_yt_source_pole_canonical_higgs_mixing_obstruction.py
# SUMMARY: PASS=11 FAIL=0
```

Boundary:

This does not close PR #230 and does not authorize `retained` or
`proposed_retained`.  It sharpens the route-1 theorem target: derive or
measure the source-pole-to-canonical-Higgs identity, excluding orthogonal
scalar admixture, and combine it with the isolated-pole derivative without
forbidden normalization imports.
