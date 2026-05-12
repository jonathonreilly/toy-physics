# PR #230 OS Transfer-Kernel Artifact Gate

Date: 2026-05-07

This block sharpens the clean source-Higgs/neutral-transfer target.  The
current two-source taste-radial row packet contains finite equal-time
`C_ss/C_sx/C_xx` covariance rows over configurations.  It does not contain a
same-surface Euclidean-time scalar correlation matrix `C_ij(t)` that can
determine a transfer/action generator, pole residue, or canonical
source-to-Higgs overlap.

The runner is:

```text
python3 scripts/frontier_yt_pr230_os_transfer_kernel_artifact_gate.py
```

and it writes:

```text
outputs/yt_pr230_os_transfer_kernel_artifact_gate_2026-05-07.json
```

## Literature Refresh

The review uses the standard OS/transfer/GEVP route only as a contract for a
future same-surface artifact:

- Osterwalder and Schrader, "Axioms for Euclidean Green's functions. II",
  Commun. Math. Phys. 42 (1975) 281-305,
  https://www.osti.gov/biblio/4131077.
- Luscher, "Construction of a selfadjoint, strictly positive transfer matrix
  for Euclidean lattice gauge theories", Commun. Math. Phys. 54 (1977)
  283-292, https://doi.org/10.1007/BF01614090.
- Luscher and Wolff, "How to calculate the elastic scattering matrix in
  two-dimensional quantum field theories by numerical simulation", Nucl.
  Phys. B339 (1990) 222-252,
  https://courses.physics.ucsd.edu/2016/Spring/physics142/Labs/FinalProjects/LuscherWolff.pdf.

These sources support the positive target: construct the Hilbert/transfer or
GEVP pole data from Euclidean-time correlation matrices.  They do not turn a
static PR230 covariance row into canonical `O_H`, `kappa_s`, or a neutral
primitive transfer.

## Result

After the chunk063 final package, the complete row packet has `63/63` chunks
and `combined_rows_written=true`.  It has top correlators with a `tau` axis in
all 63 chunks, but the scalar source/taste-radial matrix rows have
configuration timeseries, not Euclidean-time matrix rows.  The refreshed
certificate therefore records:

- `os_transfer_kernel_artifact_present=false`
- `same_surface_transfer_or_gevp_present=false`
- `chunks_with_top_tau_correlators=63`
- `chunks_with_scalar_time_kernel=0`
- `chunks_with_taste_radial_alias_metadata=63`
- `taste_radial_alias_mismatch_count=0`
- `proposal_allowed=false`
- `bare_retained_allowed=false`

The alias check is load-bearing for the claim firewall: the schema fields
named `C_sH/C_HH` match the taste-radial `C_sx/C_xx` rows and are explicitly
marked as aliases, so they are not canonical source-Higgs pole rows on the
current surface.

The executable witness constructs two distinct positive self-adjoint transfer
candidates with the same equal-time Gram `C(0)=G`.  Since both candidates are
compatible with the same static `G` but produce different `C(1)` kernels,
finite `C_ss/C_sx/C_xx` covariance rows cannot select the physical
off-diagonal generator, pole residue, or source-Higgs overlap.

## Exact Next Artifact

Implement a same-surface scalar correlation-matrix production row:

- `C_ss(t)`, `C_sH(t)`, and `C_HH(t)` for a certified canonical `O_H`; or
- `C_ss(t)`, `C_sx(t)`, and `C_xx(t)` plus a same-surface theorem identifying
  `x` with canonical `O_H` or a physical neutral transfer basis.

The future certificate must include reflection-positive/GEVP pole extraction,
finite-volume/IR/threshold authority, overlap normalization, configuration
covariance, seed metadata, and all claim firewalls.  Configuration
timeseries, method names, exact-value recognition, static covariance,
`H_unit`, Ward identities, observed targets, `alpha_LM`, plaquette/u0,
reduced pilots, `c2=1`, `Z_match=1`, and `kappa_s=1` remain forbidden proof
inputs.

This is support plus a negative boundary only.  It does not authorize retained
or proposed-retained closure, and PR #230 remains draft/open.

## Verification

```text
python3 -m py_compile scripts/frontier_yt_pr230_os_transfer_kernel_artifact_gate.py
# OK
python3 scripts/frontier_yt_pr230_os_transfer_kernel_artifact_gate.py
# SUMMARY: PASS=13 FAIL=0
```
