# PR230 FMS `O_H` Candidate/Action Packet

Date: 2026-05-07

Status: conditional-support / FMS `O_H` candidate-action packet; no current
PR230 closure

Runner:
`scripts/frontier_yt_pr230_fms_oh_candidate_action_packet.py`

Certificate:
`outputs/yt_pr230_fms_oh_candidate_action_packet_2026-05-07.json`

```yaml
actual_current_surface_status: conditional-support / FMS O_H candidate/action packet; current PR230 surface has no adopted same-surface EW/Higgs action, canonical O_H certificate, or C_ss/C_sH/C_HH pole rows
conditional_surface_status: exact-support only after the packet is converted into an accepted same-surface Cl(3)/Z^3 EW/Higgs action or explicitly admitted extension, a canonical O_H certificate, production C_ss/C_sH/C_HH time-kernel rows, pole/Gram/FV/IR authority, and aggregate route gates
hypothetical_axiom_status: external gauge-Higgs extension candidate if the action is adopted rather than derived from Cl(3)/Z^3
proposal_allowed: false
bare_retained_allowed: false
```

## Packet

This block turns the block16 open-surface intake into a concrete candidate
contract:

```text
O_H(x) = Phi(x)^dagger Phi(x) - <Phi^dagger Phi>
```

The packet requires a dynamic Higgs doublet `Phi`, a gauge-covariant lattice
kinetic term, a radial potential or substrate derivation producing nonzero
`v`, a canonical radial field `h`, and a scalar source whose derivative is
`sum_x O_H(x)` after additive-top subtraction or a no-independent-top source
theorem.

On an accepted BEH/FMS surface the local expansion is:

```text
O_H = v h + h^2/2 + pi^a pi^a/2
Res C_HH = v^2 Z_h
```

That gives the right gauge-invariant composite operator shape, but it does not
fix the PR230 source overlap.  `Res C_sH` or an equivalent source-coordinate
theorem remains load-bearing.

## Current-Surface Boundary

The packet is not an adopted current-surface action.  It explicitly records:

- `same_surface_cl3_z3_derived = false`;
- `accepted_current_surface = false`;
- `external_extension_required = true`;
- `launch_authorized_now = false`;
- `closure_authorized = false`.

It wires the candidate to the existing source-Higgs time-kernel manifest, but
does not launch rows.  Future acceptance requires same-ensemble production
`C_ss(t)`, `C_sH(t)`, and `C_HH(t)` rows, covariance, GEVP or isolated-pole
residue extraction, FV/IR and zero-mode limiting order, Gram flatness or a
source-overlap theorem, and strict scalar-LSZ/model-class authority.

## Claim Boundary

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not use `H_unit`, `yt_ward_identity`, observed top/y_t, observed W/Z or
`g2`, `alpha_LM`, plaquette, `u0`, reduced cold pilots, or value recognition.
It does not identify the taste-radial axis with canonical `O_H`, relabel
`C_sx` as `C_sH`, or set `kappa_s`, `c2`, `Z_match`, or `g2` to one.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_fms_oh_candidate_action_packet.py
python3 scripts/frontier_yt_pr230_fms_oh_candidate_action_packet.py
# SUMMARY: PASS=13 FAIL=0
```
