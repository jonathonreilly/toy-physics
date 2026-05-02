# FH/LSZ Numba Seed-Independence Audit

Status: exact negative boundary / FH-LSZ numba seed-independence audit

Claim firewall:

```yaml
actual_current_surface_status: exact negative boundary / FH-LSZ numba seed-independence audit
proposal_allowed: false
bare_retained_allowed: false
```

The completed L12_T24 FH/LSZ `chunk001` and `chunk002` outputs cannot be counted
as independent production evidence on the current surface.  Their metadata
seeds are different, but their gauge-evolution signature is identical:

- identical plaquette mean;
- identical selected mass fit;
- identical same-source `dE/ds` slope;
- no historical `numba_gauge_seed_v1` marker proving that numba gauge evolution
  was seeded inside `run_volume_numba`.

The scalar stochastic rows can differ because they use a separate NumPy RNG.
That does not rescue the gauge ensemble independence required for production
evidence.

Harness repair:

- `run_volume_numba` now calls `nb_seed(volume_rng_seed)` before thermalization;
- the volume seed is derived from the chunk base seed and volume;
- new outputs record `rng_seed_control.seed_control_version =
  numba_gauge_seed_v1`;
- the chunk combiner rejects chunks without that marker and chunks that share
  duplicate gauge-evolution signatures across distinct metadata seeds.

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_numba_seed_independence_audit.py
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0
```

Consequence:

Historical chunk001/chunk002 are production-format diagnostics only.  They must
be rerun under the patched harness, or excluded, before they can contribute to
L12 combination.  This is an evidence-quality gate and does not close `kappa_s`,
the scalar pole residue, L16/L24 scaling, FV/IR/zero-mode control, or retained
`y_t` closure.
