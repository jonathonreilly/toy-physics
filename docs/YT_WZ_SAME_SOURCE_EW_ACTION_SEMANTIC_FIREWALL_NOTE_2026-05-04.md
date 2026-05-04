# PR #230 Same-Source EW Action Semantic Firewall

Date: 2026-05-04

Status: bounded-support / W/Z action-contract firewall only.

## Purpose

The W/Z physical-response bypass needs a same-source electroweak
SU(2)xU(1)/Higgs action block before W/Z mass-response rows can be load-bearing.
The existing action builder and gate record that this action is absent.  This
block hardens the future certificate contract so a syntactically filled
candidate cannot pass by pointing at static EW algebra, the current QCD/top
production harness, gate outputs, observed selectors, or candidate-local
proposal flags.

## Result

The builder now requires non-shortcut certificate references and allowed
certificate kinds for:

- canonical-Higgs operator identity;
- same-source sector-overlap identity;
- W/Z correlator mass-fit path.

The semantic firewall runner rejects spoof candidates using:

- static EW gauge-mass diagonalization as the canonical-Higgs/action reference;
- the current QCD/top FH/LSZ harness as the W/Z mass-fit path;
- gate or obstruction outputs as identity certificates;
- observed masses/couplings as selectors;
- H_unit or Ward authority;
- self-declared certificate kinds;
- candidate-local `proposal_allowed=true`.

## Certificate

```bash
python3 scripts/frontier_yt_wz_same_source_ew_action_certificate_builder.py
python3 scripts/frontier_yt_wz_same_source_ew_action_semantic_firewall.py
```

Outputs:

```text
outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json
outputs/yt_wz_same_source_ew_action_semantic_firewall_2026-05-04.json
```

This is not W/Z response evidence.  It supplies no EW action block, no W/Z
correlator rows, no sector-overlap identity, no canonical-Higgs identity, and
no retained/proposed-retained `y_t` closure.
