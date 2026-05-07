# PR230 Direct Source-Higgs Pole-Row Contract

**Status:** exact support / direct source-Higgs pole-row contract; `O_H` and
production `C_sH/C_HH` rows are absent

**Runner:** `scripts/frontier_yt_pr230_source_higgs_direct_pole_row_contract.py`

**Certificate:** `outputs/yt_pr230_source_higgs_direct_pole_row_contract_2026-05-07.json`

```yaml
actual_current_surface_status: exact-support / direct source-Higgs pole-row contract; O_H and production C_sH/C_HH rows are absent
conditional_surface_status: exact support for a future same-surface certified O_H_candidate plus C_ss/C_sH/C_HH pole-row packet that passes Gram purity, FV/IR/model-class, and retained-route gates
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

The strongest non-chunk route is the source-Higgs Gram-purity bridge.  The
source side is no longer arbitrary: the Legendre/LSZ construction supplies the
same-surface source-pole operator

```text
O_sp = sqrt(Dprime_ss at pole) O_s,
Res(C_sp,sp) = 1.
```

The missing object is the same-surface canonical Higgs radial operator and the
cross-pole rows connecting it to `O_sp`.

This note records the acceptance contract for that future row packet.  It does
not construct `O_H`, does not promote `C_sx/C_xx` aliases to `C_sH/C_HH`, and
does not claim closure.

## Contract

A future strict packet must provide:

- a certified same-surface `O_H_candidate` with identity and normalization
  certificates;
- production same-ensemble `C_ss/C_sH/C_HH` pole-residue rows;
- nondegenerate pole isolation plus FV/IR/zero-mode/model-class control;
- covariance/error fields for the residues;
- a clean forbidden-input firewall excluding `H_unit`, static EW algebra,
  `yt_ward_identity`, observed selectors, `alpha_LM`, plaquette/`u0`, and
  `C_sx/C_xx` aliases.

The existing pipeline then remains authoritative:

```text
source-Higgs pole-residue extractor
-> source-Higgs cross-correlator certificate builder
-> O_sp-Higgs Gram-purity postprocessor
-> full assembly / retained-route / campaign gates
```

## Witness

For pole residues,

```text
Delta = Res(C_ss) Res(C_HH) - Res(C_sH)^2
rho   = Res(C_sH) / sqrt(Res(C_ss) Res(C_HH)).
```

The runner checks a pure same-pole witness with `Delta=0` and `abs(rho)=1`,
including the opposite-sign convention, and a mixed witness where
`abs(rho)<1`.  The mixed witness fails the bridge condition even though the
source-pole side can remain normalized, which is exactly why source-only LSZ
is not enough.

## Boundary

Current PR230 has no canonical `O_H` certificate and no production
`C_sH/C_HH` pole rows.  The completed chunk rows marked as `C_sx/C_xx` are
bounded two-source support only; they are not this row packet.  The contract
is positive infrastructure for the next source-Higgs attempt, not present
evidence.

## Non-Claims

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not construct `O_H`, define `O_H` by fiat, set `kappa_s=1` or
`cos(theta)=1`, use `H_unit`, static EW algebra, `yt_ward_identity`, observed
targets, `alpha_LM`, plaquette/`u0`, or touch the live chunk worker.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_source_higgs_direct_pole_row_contract.py
python3 scripts/frontier_yt_pr230_source_higgs_direct_pole_row_contract.py
# SUMMARY: PASS=18 FAIL=0
```
