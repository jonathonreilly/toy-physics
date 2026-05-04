# PR #230 Complete Source-Spectrum Identity No-Go

```yaml
actual_current_surface_status: exact negative boundary / complete source spectrum not canonical-Higgs closure
proposal_allowed: false
bare_retained_allowed: false
```

This block tests the strongest source-only variant of the FH/LSZ route: assume
the complete same-source scalar spectrum `C_ss(p)` is known, including pole
masses and residues, and pair it with the same-source top response `dE_top/ds`.
Even then, the physical canonical-Higgs Yukawa is not fixed unless an
orthogonal neutral top coupling is forbidden or measured.

The runner constructs a two-scalar witness

```text
O_s = cos(theta) h_canonical + sin(theta) chi_orthogonal
dE_top/ds = cos(theta) y_h + sin(theta) y_chi
```

and keeps every sampled value of the complete source spectrum and the
same-source top response fixed while varying `y_h` by a factor greater than
four through finite positive `y_chi`.

The 2026-05-04 refresh also updates the parent-state checks for the newer
PR230 source-Higgs instrumentation.  The harness now has default-off
`C_ss/C_sH/C_HH` instrumentation, but it remains support-only because no
accepted canonical-Higgs operator certificate or production pole-residue rows
exist.  The W/Z side remains an absence/import-audit boundary with no
same-source W/Z response rows.

## Runner

```bash
python3 scripts/frontier_yt_complete_source_spectrum_identity_no_go.py
# SUMMARY: PASS=15 FAIL=0
```

Certificate:

```text
outputs/yt_complete_source_spectrum_identity_no_go_2026-05-02.json
```

## Claim Firewall

This does not claim retained or `proposed_retained` closure.  It does not set
`kappa_s = 1`, `cos(theta) = 1`, or the orthogonal scalar top coupling to zero.
It does not use `H_unit`, `yt_ward_identity`, observed target values,
`alpha_LM`, plaquette, `u0`, `c2 = 1`, or `Z_match = 1`.

## Exact Next Action

Close a non-source-only identity premise: implement same-surface `C_sH/C_HH`
Gram-purity measurements, implement a real same-source W/Z response with
sector-overlap identity certificates, or derive a theorem forbidding
orthogonal neutral top couplings.
