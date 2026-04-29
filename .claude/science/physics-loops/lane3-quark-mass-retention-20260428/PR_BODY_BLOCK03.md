# Summary

Block 03 continues Lane 3 quark mass retention from the block 02 Route-2
`R_conn` bridge obstruction.

It adds an exact current-bank source-domain bridge no-go:

- `docs/QUARK_ROUTE2_SOURCE_DOMAIN_BRIDGE_NO_GO_NOTE_2026-04-28.md`
- `scripts/frontier_quark_route2_source_domain_bridge_no_go.py`
- `logs/2026-04-28-quark-route2-source-domain-bridge-no-go.txt`

The result is deliberately not a retained quark-mass claim. It shows that
adding the missing bridge

```text
gamma_T(center)/gamma_E(center) = -R_conn
```

would force `beta_E/alpha_E = 21/4` exactly, but the current Route-2 and
SU(3) support bank has no typed edge from `su3_R_conn_8_9` to
`route2_rho_E_21_4`.

# Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_route2_source_domain_bridge_no_go.py
TOTAL: PASS=33, FAIL=0

python3 -m py_compile scripts/frontier_quark_route2_source_domain_bridge_no_go.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_rconn_center_ratio_bridge_obstruction.py
TOTAL: PASS=26, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py
TOTAL: PASS=28, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_exact_readout_map.py
PASS=11 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_endpoint_ratio_chain_law.py
PASS=14 FAIL=0

python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0

python3 scripts/frontier_quark_mass_ratio_review.py
TOTAL: PASS=46, FAIL=0
```

# Review Notes

The block keeps claim status `open`. It retires only the current-bank
promotion:

```text
R_conn is retained, and Route-2 needs -8/9, therefore the up-type E-channel
readout is derived.
```

The next exact theorem target is a genuinely new typed source-domain bridge,
an alternate 3B readout primitive, or a sharp 3A local theorem.
