# PR #230 No-Orthogonal-Top-Coupling Import Audit

```yaml
actual_current_surface_status: exact negative boundary / no-orthogonal-top-coupling import audit
proposal_allowed: false
bare_retained_allowed: false
```

This block checks a possible escape hatch for the same-source gauge-response
route.  If the current Cl(3)/Z3 surface already proved that every scalar
component orthogonal to the canonical Higgs radial mode has zero top coupling,
then the mixed-scalar obstruction would collapse and the same-source
top/W-response ratio would be much closer to a physical `y_t` readout.

The audit finds no such hidden theorem.

## Support That Does Exist

The Class #3 SUSY/2HDM analysis is useful, but narrower than the PR #230 LSZ
need.  It supports:

- no retained fundamental second scalar field in the bare action;
- no retained 2HDM up/down species split;
- D17 one-dimensional scalar-singlet support on the `Q_L` block.

Those facts exclude importing a retained 2HDM as a proof primitive.  They do
not identify the scalar pole created by the PR #230 source with the canonical
Higgs radial mode whose kinetic normalization defines `v`.

## Missing Premise

The same-source gauge-response route still needs at least one of:

- `source pole = canonical Higgs radial mode`;
- no orthogonal response component in the source pole;
- zero top coupling for every orthogonal scalar response component;
- direct production/theorem evidence fixing source-pole residue and purity.

The existing no-2HDM note does not derive any of these LSZ/source-pole
statements.  It is a bare-action and species-split authority, not a
source-pole residue or pole-purity certificate.

## Counterfamily

The runner keeps the Class #3 facts fixed:

```text
retained_fundamental_second_scalar_present = false
retained_2hdm_present = false
D17 Q_L scalar-singlet dimension = 1
fixed measured source-pole top coupling = 1
```

It then varies an open response-level parameter: the effective top coupling of
an orthogonal source-pole component.  The measured source-pole coupling can be
held fixed while the canonical-Higgs Yukawa changes.  This is not an admitted
new retained scalar model; it is a logical import audit showing that the
existing Class #3 authority does not contain the stronger LSZ purity theorem.

## Claim Firewall

This block does not claim retained or `proposed_retained` closure.  It does not
use `H_unit` matrix-element readout, `yt_ward_identity`, observed masses,
observed `y_t`, `alpha_LM`, plaquette, `u0`, `c2 = 1`, `Z_match = 1`, or
`kappa_s = 1`.

## Runner

```text
python3 scripts/frontier_yt_no_orthogonal_top_coupling_import_audit.py
# SUMMARY: PASS=14 FAIL=0
```

Output:

```text
outputs/yt_no_orthogonal_top_coupling_import_audit_2026-05-02.json
```

## Exact Next Action

Either derive the source-pole-to-canonical-Higgs/no-orthogonal-top-coupling
theorem directly, or continue seed-controlled FH/LSZ production and require a
separate pole-identity acceptance gate before any physical `y_t` claim.
