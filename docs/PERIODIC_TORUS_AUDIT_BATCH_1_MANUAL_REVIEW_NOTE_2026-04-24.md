# Periodic Torus Audit — Batch 1 Manual Review

**Date:** 2026-04-24
**Status:** real falsifying finding plus regex tightening for the
"periodic 2D torus diagnostics" active-queue item.
**Predecessor:** [`PERIODIC_TORUS_DIAGNOSTICS_CODE_AUDIT_NOTE_2026-04-24.md`](PERIODIC_TORUS_DIAGNOSTICS_CODE_AUDIT_NOTE_2026-04-24.md)
**Runner:** `scripts/frontier_periodic_torus_diagnostics_audit.py` (regex tightened in this loop).

## 1. Question

The 2026-04-24 audit produced a 9-script `NEEDS_REVIEW` list. The
honest framing was that NEEDS_REVIEW != BUG. This batch confirms
each candidate by manual inspection and tightens the regex when
false positives are found.

## 2. Per-script verdicts

| Script | Verdict | Reason |
|---|---|---|
| `frontier_continuous_dirac_potential.py` | **CLEAN (false positive)** | Uses `min(abs(x-mp), n-abs(x-mp))` minimum-image idiom. |
| `frontier_correct_coupling.py` | **CLEAN (false positive)** | Same `min(abs(x-mp), n-abs(x-mp))` idiom. |
| `frontier_dirac_bottleneck_tests.py` | **CLEAN (false positive)** | Adjacency via `np.roll` (auto-periodic, no distance); source field uses `np.minimum(np.abs(...), n-np.abs(...))`. |
| `frontier_geometric_gravity_v2.py` | **CLEAN (false positive)** | `field_r` (line 57-67) uses `min(abs(x-mp[0]), n-abs(x-mp[0]))`; weighted_laplacian uses these minimum-image distances. |
| `frontier_graph_kg_16card.py` | **CLEAN (false positive)** | Same `min(abs(...), n-abs(...))` idiom. |
| `frontier_graph_kg_full_suite.py` | **CLEAN (false positive)** | `field_r` (line 34-42) uses `min(abs(x-mp[0]), n-abs(x-mp[0]))`. |
| `frontier_graph_laplacian_kg.py` | **CLEAN (false positive)** | Same idiom. |
| `frontier_shapiro_delay.py` | **TRUE BUG** | 1D periodic ring `adj_1d` (line 264) used by `_build_H` (line 91) which computes hopping weights from raw `math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])` (line 98). Wraparound edge gets weight `1/(n-1)` instead of `1/1`. |
| `frontier_staggered_3d_17card.py` | **CLEAN (false positive)** | `build_V_3d` (line 50) uses `min(abs(x-mass_pos[0]), n-abs(x-mass_pos[0]))`. |

## 3. Regex tightening

Two new minimum-image patterns added to the audit:

- `\b\w+\s*-\s*(?:np\.|numpy\.)?abs\(`: catches both `abs(...)` and
  `np.abs(...)` (with `numpy.` prefix variant) in expressions like
  `n - abs(...)` or `n - np.abs(...)`.
- The previously-added centered-modulo pattern
  `%\s*\w+\s*-\s*\w+\s*//\s*2` continues to catch the
  `(x + L // 2) % L - L // 2` idiom from `frontier_monopole_derived.py`.

After tightening, `NEEDS_REVIEW` shrinks from 9 to 1 (the genuine bug
in `frontier_shapiro_delay.py`).

## 4. Confirmed bug detail: frontier_shapiro_delay.py

The 1D periodic ring case (`run_shapiro("1d_lattice", ...)` at
line 270) uses:

```python
# line 264
adj_1d = {x: [((x+1) % n), ((x-1) % n)] for x in range(n)}
```

Then `_build_H(pos_1d, col_1d, adj_1d, n, phi)` (line 136 via
`run_shapiro`) builds the Hamiltonian:

```python
# lines 91-100
def _build_H(pos, col, adj, n, phi):
    H = lil_matrix((n,n), dtype=complex)
    par = np.where(col == 0, 1., -1.)
    H.setdiag((MASS + phi) * par)
    for i, nbs in adj.items():
        for j in nbs:
            if i >= j: continue
            d = math.hypot(pos[j,0]-pos[i,0], pos[j,1]-pos[i,1])
            w = 1./max(d, 0.5); H[i,j] += -0.5j*w; H[j,i] += 0.5j*w
    return H.tocsr()
```

For the wraparound edge between site `0` and site `n-1`, the raw
coordinate difference is `n-1` so `d = n-1`, giving weight
`w = 1/(n-1)` instead of the correct minimum-image value `w = 1/1 = 1`.

For the script's `n = 61` 1D ring (line 261), the wraparound weight
is `~1/60` — a 60× suppression. The 1D "periodic ring" effectively
acts as an open chain with a weak wraparound. Any Shapiro-delay
measurement on this configuration is on the wrong topology.

The 2D case (line 47) builds adjacency without wraparound, so it
is unaffected.

## 5. What this changes

### CLEAN (8 scripts moved from NEEDS_REVIEW to CLEAN_INLINE)

These 8 scripts use a valid minimum-image idiom that the prior
regex did not catch. They are not affected by the 2026-04-11 bug:

- frontier_continuous_dirac_potential.py
- frontier_correct_coupling.py
- frontier_dirac_bottleneck_tests.py
- frontier_geometric_gravity_v2.py
- frontier_graph_kg_16card.py
- frontier_graph_kg_full_suite.py
- frontier_graph_laplacian_kg.py
- frontier_staggered_3d_17card.py

### TRUE BUG (1 script flagged for follow-up)

`frontier_shapiro_delay.py` has the 2026-04-11 minimum-image bug
in its 1D periodic ring case. The 2D case is unaffected.

The script is exploratory and not on the canonical-retained
surface. Recommended dispositions, in order of preference:

1. Inline-fix `_build_H`/`_build_L` to use minimum-image distance for
   the periodic case (small change at lines 86, 98).
2. Quarantine the 1D ring driver (line 270) and keep only the 2D
   open-lattice driver.
3. Mark the script as historical/exploratory and add a comment in
   the header noting the 1D-case limitation.

This loop does NOT apply any of these dispositions; that is the
next concrete step.

## 6. Falsifier (of this note's claims)

- A "CLEAN (false positive)" script that, on closer inspection, does
  use raw periodic-edge distances at any Hamiltonian site (would
  re-flag it).
- A "TRUE BUG" reading that turns out to be incorrect — e.g., the
  1D ring driver in `frontier_shapiro_delay.py` is never actually
  used by any retained downstream consumer (would soften "BUG" to
  "historical limitation").

## 7. Active-queue update

The `periodic 2D torus diagnostics` item in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](repo/ACTIVE_REVIEW_QUEUE.md)
remains OPEN. The new content is two-fold:

- 8 of 9 prior `NEEDS_REVIEW` scripts are now `CLEAN_INLINE` after
  regex tightening; explicit per-script verdicts are recorded in
  Section 2.
- 1 confirmed TRUE BUG: `frontier_shapiro_delay.py` 1D ring case
  uses raw distance for periodic-edge weights. Recommended
  dispositions are listed in Section 5.

## 8. Next concrete step

Apply one of the three dispositions to `frontier_shapiro_delay.py`
in a follow-up loop — preferred is the inline `_build_H` fix that
pulls in `from periodic_geometry import minimum_image_distance` (or
inlines the same min-image computation) at lines 86, 98.

After that, the periodic-torus active-queue item can be re-evaluated
for whether it warrants closure (no remaining `NEEDS_REVIEW`).

## 9. Provenance

- Runner: `scripts/frontier_periodic_torus_diagnostics_audit.py`
  (regex tightened in this loop; see commit diff for the exact change).
- Audit summary after tightening: `5/5 PASS`,
  `NEEDS_REVIEW: 1`, `CLEAN_HELPER: 6`, `CLEAN_INLINE: 19`,
  `CLEAN_NO_DISTANCE: 35`, `NOT_APPLICABLE: 1988`, `ERROR: 0`.
- Wallclock: ~1 second.
- Reproducibility: deterministic regex scan; same input → same output.
- Runtime caveat: validation host Python 3.12.8; audit is pure
  filesystem + regex.
