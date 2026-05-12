## 2026-05-12 complete-packet OS transfer / alias-firewall refresh

This checkpoint refreshes the OS transfer-kernel gate against the completed
finite taste-radial packet.

What changed:

- `scripts/frontier_yt_pr230_os_transfer_kernel_artifact_gate.py` now verifies
  the complete `63/63` packet;
- the gate records top tau correlators in all 63 chunks, but scalar
  Euclidean-time kernels in 0 chunks;
- it adds an explicit alias firewall: `C_sH/C_HH` schema fields are verified
  aliases of taste-radial `C_sx/C_xx`, with alias metadata in all 63 chunks
  and zero mismatches.

Validation:

- OS transfer gate: `PASS=13 FAIL=0`;
- `ready_chunks=63`;
- `combined_rows_written=true`;
- `chunks_with_top_tau_correlators=63`;
- `chunks_with_scalar_time_kernel=0`;
- `chunks_with_taste_radial_alias_metadata=63`;
- `taste_radial_alias_mismatch_count=0`.

Claim boundary: this is exact support plus a negative boundary only.  The
complete finite packet is not a scalar Euclidean-time kernel, not a transfer
generator, not a pole-residue packet, and not canonical source-Higgs overlap
authority.  No retained or `proposed_retained` closure is claimed; PR #230
remains draft/open.
