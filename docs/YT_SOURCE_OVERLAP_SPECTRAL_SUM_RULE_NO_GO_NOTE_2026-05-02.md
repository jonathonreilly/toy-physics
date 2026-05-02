# PR #230 Source-Overlap Spectral Sum-Rule No-Go

```yaml
actual_current_surface_status: exact negative boundary / source-overlap spectral sum-rule no-go
proposal_allowed: false
bare_retained_allowed: false
```

This block tests whether finite positive spectral or moment sum rules for the
same-source scalar two-point function can fix the source-pole residue
`<0|O_s|h>^2`.  They cannot.

The runner constructs positive pole-plus-continuum spectral measures that keep
the first four moments exactly fixed while varying the source-pole residue by
a factor of ten.  The corresponding fixed-`dE/ds` physical-`y` proxy varies by
more than a factor of three.

This closes the finite-moment shortcut:

- D17 carrier uniqueness remains support only;
- same-source `C_ss`/`Gamma_ss` remains a measurement primitive only;
- finite shell/Stieltjes positivity remains underidentified;
- contact and renormalization schemes do not fix the isolated pole residue.

## Runner

```text
python3 scripts/frontier_yt_source_overlap_sum_rule_no_go.py
# SUMMARY: PASS=12 FAIL=0
```

Output:

```text
outputs/yt_source_overlap_sum_rule_no_go_2026-05-02.json
```

## Claim Firewall

This block does not claim retained or `proposed_retained` closure.  It does
not use `H_unit` matrix-element readout, `yt_ward_identity`, observed target
values, `alpha_LM`, plaquette, `u0`, `c2 = 1`, `Z_match = 1`, or
`kappa_s = 1`.

## Exact Next Action

Move to a microscopic scalar denominator / threshold theorem, or wait for
seed-controlled production data and apply the pole-fit model-class, FV/IR, and
Higgs-identity gates.
