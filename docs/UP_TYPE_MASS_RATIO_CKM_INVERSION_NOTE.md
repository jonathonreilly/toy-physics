# Up-Type Mass Ratios from the CKM Inversion (Phase 2 of mass spectrum)

**Date:** 2026-04-17
**Status:** bounded secondary lane (one conditional partition)
**Primary runner:** `scripts/frontier_mass_ratio_up_sector.py`
**Depends on:** `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md` (Phase 1)

## Safe statement

Extending the promoted CKM atlas/axiom package and the Phase 1 down-type
mass-ratio dual to the up sector under a **parallel-bridge ansatz** (GST +
5/6 bridge applied symmetrically to both sectors with CP-orthogonal relative
phase) produces a one-parameter family of up-type mass ratios, parametrized
by the down-up partition fractions `(f_12, f_23) in [0,1]^2`:

- `m_d/m_s     = f_12^2 * (alpha_s(v)/2)`
- `m_u/m_c     = (1 - f_12^2) * (alpha_s(v)/2)`
- `m_s/m_b     = (f_23 * alpha_s(v)/sqrt(6))^(6/5)`
- `m_c/m_t     = ((1 - f_23^2)^(1/2) * alpha_s(v)/sqrt(6))^(6/5)`

The down-dominant edge `(f_12, f_23) = (1, 1)` reproduces the Phase 1
down-type dual exactly and sets the up-type ratios to zero.  The up-dominant
edge `(f_12, f_23) = (0, 0)` is the symmetric opposite.  Observed quark mass
ratios sit in the interior of this family.

No observed masses are used as derivation inputs.

This lane is **bounded**, not retained, because the partition parameters
`(f_12, f_23)` are not yet derivable from the retained core.  Three closure
candidates are tracked but not promoted:

1. the atlas CP phase `delta = arctan(sqrt(5))`;
2. the Jarlskog invariant `J`;
3. an isospin-partner EWSB cascade theorem (not yet constructed).

## Inputs and ansatz structure

### Promoted atlas inputs

- [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md):
  `alpha_s(v) = 0.103303816122` on the canonical plaquette surface.
- [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md):
  `|V_us| = sqrt(alpha_s(v)/2)`, `|V_cb| = alpha_s(v)/sqrt(6)`,
  `|V_ub| = alpha_s(v)^(3/2)/(6*sqrt(2))`, `delta = arctan(sqrt(5))`.
- [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](./DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md):
  Phase 1 down-type ratios from GST and the 5/6 bridge.
- Exact SU(3) group constants `C_F = 4/3`, `T_F = 1/2`, `C_F - T_F = 5/6`.

### Ansatz-conditioned inputs

- **Parallel bridges**: GST and 5/6 bridges apply to both sectors with the
  same exponent and coefficient structure.
- **CP-orthogonal relative phase**: the up-sector and down-sector NNI
  contributions to each CKM magnitude are relatively phased by `pi/2`, so
  they add in quadrature.
- **Partition `(f_12, f_23)`**: a free parameter in `[0, 1]^2` that
  distributes each atlas CKM magnitude's squared value between the two
  sectors.

## Phase 2 formulas

Under the parallel-bridge + CP-orthogonal ansatz:

$$
|V_{us}|^2 = \frac{m_d}{m_s} + \frac{m_u}{m_c} = \frac{\alpha_s(v)}{2},
$$

$$
|V_{cb}|^2 = \left(\frac{m_s}{m_b}\right)^{5/3} + \left(\frac{m_c}{m_t}\right)^{5/3}
 = \frac{\alpha_s(v)^2}{6}.
$$

Parametrizing by the down-sector share `f_12^2` and `f_23^2`:

$$
\frac{m_d}{m_s} = f_{12}^2 \cdot \frac{\alpha_s(v)}{2},
\quad
\frac{m_u}{m_c} = (1 - f_{12}^2) \cdot \frac{\alpha_s(v)}{2},
$$

$$
\frac{m_s}{m_b} = \left(f_{23} \cdot \frac{\alpha_s(v)}{\sqrt{6}}\right)^{6/5},
\quad
\frac{m_c}{m_t} = \left((1-f_{23}^2)^{1/2} \cdot \frac{\alpha_s(v)}{\sqrt{6}}\right)^{6/5}.
$$

Phase 1 is the edge `(f_12, f_23) = (1, 1)`.

## Current numerical surface

With `alpha_s(v) = 0.103303816122`:

### Edges (exactly predicted)

| Partition | `m_d/m_s` | `m_s/m_b` | `m_u/m_c` | `m_c/m_t` |
|---|---|---|---|---|
| down-dominant `(1, 1)` | `0.05165` | `0.02239` | `0.00000` | `0.00000` |
| up-dominant `(0, 0)` | `0.00000` | `0.00000` | `0.05165` | `0.02239` |
| **observed** | `0.05000` | `0.02234` | `0.00172` | `0.00737` |

### Interior partition from observation comparator

Solving the partition equations using the observed ratios as comparator
values (**not** as derivation inputs) yields:

- `f_12 = sqrt((m_d/m_s)_obs / |V_us|^2) = 0.9839` (1-2 down-dominant at 1.6%)
- `f_23 = sqrt((m_s/m_b)^(5/3)_obs / |V_cb|^2) = 0.9983` (2-3 down-dominant at 0.2%)

The residual up-sector admits:

- `m_u/m_c = (1 - f_12^2) * |V_us|^2 = 1.65 x 10^-3`
  (obs: `1.70 x 10^-3`, **+2.6% deviation**)
- `m_c/m_t = ((1 - f_23^2) * |V_cb|^2)^(3/5) = 7.35 x 10^-4`
  (obs: `7.38 x 10^-3`, **-90% deviation**)

### Interpretation of numerical mismatch

The 1-2 sector `m_u/m_c` lands within 3% of the observed ratio at the
observation-comparator partition, consistent with the classic Cabibbo-Fritzsch
result `|V_us| ≈ sqrt(m_d/m_s) - phase(m_u/m_c)`.

The 2-3 sector `m_c/m_t` lands 10x too small.  The cause is visible in
the numerics: the Phase 1 down-sector bridge saturates `|V_cb|^2` to within
0.2%, leaving too little room for any up-sector contribution under the
CP-orthogonal ansatz.  The observed 2-3 sector requires a non-orthogonal
relative phase (`cos(psi) ≈ 0.2`, not `cos(psi) = 0`) and/or a modified
bridge combination rule.

This mismatch is a **structural signature** of the bounded status: the
parallel-bridge + CP-orthogonal ansatz is close to right for the 1-2 sector
and qualitatively right for the 2-3 sector, but the exact 2-3 combination
rule requires a retained derivation of the relative phase that is not yet
available.

## What this closes

- the up-type sector is no longer absent: both `m_u/m_c` and `m_c/m_t` now
  have explicit algebraic expressions in terms of promoted atlas CKM
  quantities;
- the structural dependence on `(f_12, f_23)` is explicit;
- the down-dominant edge recovers Phase 1 exactly;
- the 1-2 up-sector ratio `m_u/m_c` is closed within 3% at the
  observation-comparator partition;
- the sensitivity of each up-type ratio to the partition parameter is
  tabulated.

## What is not claimed

- a retained or theorem-grade derivation of `(f_12, f_23)` from the
  framework;
- a retained derivation of the relative-phase structure between up and
  down sectors;
- closure of `m_c/m_t` to sub-percent accuracy (the CP-orthogonal ansatz
  is a 10x-off approximation for 2-3);
- closure of the absolute top or bottom scale from this note (those are
  anchored elsewhere via `y_t` and `y_b`).

## What closes next (Phase 2b path)

Three closure candidates are flagged:

1. **CP-phase closure**: promote the atlas `delta = arctan(sqrt(5))` to
   a relative-phase assignment between up and down sectors, which would
   fix the non-orthogonal component of the 2-3 sector combination rule.
2. **Jarlskog closure**: compute the full Jarlskog invariant `J` under
   the parallel-bridge ansatz and require match to the atlas formula;
   this would give a second scalar constraint beyond `|V_ub|`.
3. **Isospin-partner EWSB cascade**: derive the up-down hierarchy
   asymmetry directly from the retained EWSB cascade; this would fix
   `(f_12, f_23)` from Higgs-sector physics rather than flavor sector.

Any of these would promote Phase 2 to retained status.

## Validation

Run:

```bash
python3 scripts/frontier_mass_ratio_up_sector.py
```

Current expected result on `main`:

- `frontier_mass_ratio_up_sector.py`: `PASS=23 FAIL=0`

The runner verifies:

- the promoted atlas CKM input formulas;
- the edge recovery (down-dominant matches Phase 1; up-dominant matches
  the symmetric mirror);
- the interior partition from the observation comparator;
- the isospin-partner pairing structure (O(1) geometric-mean ratio);
- the sensitivity of each up-type ratio to the partition parameter;
- the bounded-lane status and the closure candidates.
