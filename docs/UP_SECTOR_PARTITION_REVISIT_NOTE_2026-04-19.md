# Up-Sector Partition Revisit on the Newer Quark Package

**Date:** 2026-04-19  
**Status:** bounded - exact obstruction theorem for the old CP-orthogonal interior partition, plus a bounded phase-deformed edge update
**Primary runner:** `scripts/frontier_up_sector_partition_revisit.py`

## Safe statement

The newer quark projector/tensor package does **not** derive the old up-sector
interior partition variables `(f_12, f_23)`.

What it does sharpen is stronger than the old Phase 2 status:

1. an **exact obstruction theorem** for the old CP-orthogonal partition once
   retained Phase 1 exactness is respected;
2. a **bounded replacement** in which the successful newer quark solves sit on
   a narrow non-orthogonal interference edge instead of a live interior
   partition surface.

So the up-sector partition lane improves, but not to a retained derivation of
`(f_12, f_23)`.

## 1. Exact obstruction theorem

The old Phase 2 lane used the CP-orthogonal sum rules

```text
|V_us|^2 = (m_d/m_s) + (m_u/m_c)
|V_cb|^2 = (m_s/m_b)^(5/3) + (m_c/m_t)^(5/3)
```

with a unit-square partition `(f_12, f_23)`.

But the retained Phase 1 down-type lane already gives exact equalities

```text
m_d/m_s = |V_us|^2
(m_s/m_b)^(5/3) = |V_cb|^2
```

on the promoted CKM atlas surface.

Substituting those equalities into the old orthogonal partition formulas forces

```text
m_u/m_c = 0
(m_c/m_t)^(5/3) = 0
```

exactly.

That is the clean obstruction theorem:

> **retained Phase 1 exactness collapses the old CP-orthogonal interior
> partition back to the edge `f_12 = f_23 = 1`.**

So once the newer quark package is taken seriously, the old interior
orthogonal partition is no longer a live derivation surface.

## 2. What the newer quark closures actually imply

The right follow-on question is therefore not “which exact interior partition
is selected?” but:

> if the newer quark closures produce nonzero `m_u/m_c` and `m_c/m_t`, what is
> the sharpest old-partition-language statement that still survives?

The runner checks three current quark surfaces:

- minimal Schur-NNI magnitude solve;
- exact-support anchor;
- reduced projector-ray shared-phase closure.

### 2.1 Orthogonal back-projection

If one forcibly re-expresses those newer nonzero up-type ratios in the old
orthogonal partition language, the results are very stable:

```text
f_12 in [0.983407, 0.983587]
f_23 in [0.918268, 0.919084]
```

This is already a strong tightening of the old picture:

- the old `1-2` partition survives numerically near the historical
  `f_12 ≈ 0.984`;
- the old `2-3` partition does **not** survive near the historical
  `f_23 ≈ 0.998`;
- instead it collapses to `f_23 ≈ 0.918`.

But that back-projection is not promotable, because it breaks the retained
down-type exact lane. The implied down-type ratios become

```text
m_d/m_s ≈ 0.04996 - 0.04997
m_s/m_b ≈ 0.02021 - 0.02023
```

which are

- only about `0.06%` from the observation-facing `m_d/m_s` comparator, but
- about `3.26%` low versus retained Phase 1 `m_d/m_s`,
- and about `9.7%` low versus retained Phase 1 `m_s/m_b`.

So the old interior partition survives only as a bounded back-projection, not
as a theorem-grade coordinate system on the newer quark package.

## 3. Bounded replacement: phase-deformed edge

Once the retained Phase 1 down-type equalities are kept exact, the newer
nonzero up-type ratios can only re-enter through **destructive interference**
rather than through an orthogonal interior share.

For each of the three newer quark surfaces, the effective relative phases
required by

```text
|V_us|^2 = d_12 + u_12 + 2 sqrt(d_12 u_12) cos(psi_12)
|V_cb|^2 = d_23 + u_23 + 2 sqrt(d_23 u_23) cos(psi_23)
```

with retained Phase 1 down exactness are:

```text
psi_12 in [95.176171, 95.204263] deg
psi_23 in [101.363360, 101.418858] deg
```

with corresponding cosine windows

```text
cos(psi_12) in [-0.090707, -0.090218]
cos(psi_23) in [-0.197980, -0.197030]
```

So the sharpest bounded update is:

> the old interior partition is replaced by a **phase-deformed edge** that is
> nearly orthogonal in `1-2` and mildly destructive in `2-3`.

That is much sharper than the original Phase 2 statement.

## 4. Why J does not close the partition lane

One of the original closure candidates was the Jarlskog invariant `J`.

The newer package now gives three relevant quark surfaces spanning a large `J`
range:

- minimal Schur-NNI magnitude solve: `J/J_atlas ≈ 0.153`
- exact-support anchor: `J/J_atlas ≈ 0.992`
- reduced projector-ray closure: `J/J_atlas ≈ 1.002`

But the effective phase windows above hardly move across that entire span:

- `psi_12` moves by only about `0.028 deg`
- `psi_23` moves by only about `0.056 deg`

So the current bounded theorem-grade statement is:

> **J closure improves the full quark solve, but it is not what selects the old
> partition variables.**

The partition lane is already collapsed to the phase-deformed edge before `J`
is fully closed.

## 5. Isospin-cascade status

The old Phase 2 note listed an “isospin-partner EWSB cascade theorem” as a
future closure candidate. That status is unchanged on this branch.

The dedicated up-sector authority note still says that theorem is “not yet
constructed,” and the legacy runner still treats it as a future candidate.
Nothing in the newer quark projector/support/tensor package promotes an exact
or bounded isospin selector into the partition equations yet.

So the isospin route remains open, but it does not currently tighten
`(f_12, f_23)`.

## Exact endpoint

The clean endpoint for the up-sector partition lane is now:

1. **Exact theorem:** retained Phase 1 down exactness makes the old
   CP-orthogonal interior partition impossible for nonzero up-sector masses.
2. **Bounded update:** the successful newer quark closures all map to a narrow
   phase-deformed edge with
   `psi_12 ≈ 95.19 deg` and `psi_23 ≈ 101.40 deg`.
3. **Not promoted:** the orthogonal back-projection
   `f_12 ≈ 0.9835`, `f_23 ≈ 0.9183` is numerically stable but breaks the
   retained down-type theorem surface, so it is not a retained law.
4. **Still open:** neither `J` nor an isospin-partner cascade theorem currently
   derives a retained interior partition.

That is the sharpest current theorem-grade update on this lane.

## Validation

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_up_sector_partition_revisit.py
```

Current expected result on this branch:

- `frontier_up_sector_partition_revisit.py`: `PASS=12 FAIL=0`

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [quark_mass_ratio_full_solve_note_2026-04-18](QUARK_MASS_RATIO_FULL_SOLVE_NOTE_2026-04-18.md)
- [quark_projector_parameter_audit_note_2026-04-19](QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
- [quark_projector_ray_phase_completion_note_2026-04-18](QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md)
- [up_type_mass_ratio_ckm_inversion_note](UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md)
