# PR230 Canonical O_H Hard-Residual Equivalence Gate

**Status:** exact negative boundary / canonical `O_H` hard residual not closed
on current PR230 surface

**Runner:** `scripts/frontier_yt_pr230_canonical_oh_hard_residual_equivalence_gate.py`

**Certificate:** `outputs/yt_pr230_canonical_oh_hard_residual_equivalence_gate_2026-05-07.json`

```yaml
actual_current_surface_status: exact negative boundary / canonical O_H hard residual not closed on current PR230 surface
conditional_surface_status: exact-support equivalence for future source-Higgs Gram flatness, neutral primitive-cone rank-one authority, or W/Z physical-response rows
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

After the parallel hard-residual probes, the missing bridge is no longer
diffuse.  The current surface does not prove

```text
O_sp = O_H,
```

but the exact routes that would close it are known.

This gate packages that equivalence and prevents further route cycling through
source-only, representation-theory, static EW, or positivity-only shortcuts.

## Equivalence

With the Legendre/LSZ source-pole normalization,

```text
Res(C_sp,sp) = 1.
```

For a future Higgs-side row, the normalized residue matrix has the form

```text
M = [[1, a],
     [a*, b]].
```

Reflection/OS/GNS positivity gives only

```text
b >= |a|^2.
```

The bridge requires the flat-extension equality:

```text
b = |a|^2,
Delta_spH = Res(C_HH) - |Res(C_sp,H)|^2 = 0,
|rho_spH| = 1.
```

The runner checks finite witnesses showing both facts: PSD rows with
`b>|a|^2` are allowed but do not close the bridge, while flat rows give the
Gram-purity condition.

Thus current PR230 can close the `O_sp/O_H` bridge only by one of three
non-shortcut artifacts:

- certified same-surface `O_H` plus production `C_ss/C_sH/C_HH` pole rows and
  Gram flatness;
- a same-surface neutral scalar primitive-cone / positivity-improving theorem
  that forces rank one at the lowest isolated scalar pole;
- same-source W/Z physical-response rows with accepted EW action,
  sector-overlap correction, matched covariance, and strict non-observed `g2`.

## Current Boundary

All three artifacts are absent on the current PR230 surface.  Existing
negative results are correctly scoped as current-surface shortcut blockers,
not permanent no-gos against future same-surface artifacts.

The runner verifies:

- source-only `O_sp -> O_H` identity remains blocked;
- canonical `O_H` certificate is absent;
- source-Higgs pole rows are absent;
- primitive-cone/irreducibility authority is absent;
- W/Z action, sector-overlap, response rows, covariance, and strict `g2` are
  absent;
- aggregate full-positive, retained-route, and campaign gates still reject
  proposal wording.

## Non-Claims

This block does not claim retained or `proposed_retained` top-Yukawa closure.
It does not construct `O_H`, identify `O_sp` with `O_H`, set `kappa_s=1`,
`cos(theta)=1`, or a flat extension by convention, treat positivity as
irreducibility, use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette/`u0`, or treat `C_sx/C_xx` aliases as `C_sH/C_HH`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_canonical_oh_hard_residual_equivalence_gate.py
python3 scripts/frontier_yt_pr230_canonical_oh_hard_residual_equivalence_gate.py
# SUMMARY: PASS=21 FAIL=0
```
