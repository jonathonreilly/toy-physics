# Dimensional Gravity Table

**Status:** bounded finite-entry inventory. This note tabulates point-tested
results on the listed family/parameter rows. It does NOT claim universality
across all dimensions, all h values, or all parameter variations. The bolded
"1.00" entries are point-tested results, not universality theorems. (NARROWED
2026-05-02 in response to audit verdict requesting a finite-scope reframing.)

**Date:** 2026-04-04 (NARROWED 2026-05-02; CERTIFICATE RUNNER ADDED 2026-05-03)
**Action:** Valley-linear S = L(1-f)
**Kernel:** 1/L^(d-1) with h^(d-1) measure

**Primary runner:** [`scripts/dimensional_gravity_table_certificate_runner_2026_05_03.py`](/Users/jonreilly/Projects/Physics/scripts/dimensional_gravity_table_certificate_runner_2026_05_03.py) (structural certificate, PASS=5/0)

**Companion runner:** [`scripts/dimensional_gravity_card.py`](/Users/jonreilly/Projects/Physics/scripts/dimensional_gravity_card.py) — slow lattice card, invoke with `--dim 3` or `--dim 4` to reproduce individual table rows; unsuitable as the audit-lane runner because of runtime.

## Review-loop runner attachment (2026-05-03)

The 2026-05-03 audit flagged that the table's bolded "1.00" entries were
asserted by prose with no executable runner attached at the audit-packet
level. The repair adds the structural certificate runner above, which
verifies the table's *invariants* (kernel/field/measure powers, Newtonian
targets per d, the linear-mass identity for valley-linear S=L(1-f),
the sqrt-mass identity for spent-delay, and the 4D width-limited honest
read) without requiring a long lattice card to run inside the audit
window. Per-row lattice measurements remain reproducible via the
companion runner above.

## Tested entries

The following table reports point-tested results on the listed (d, kernel,
h, lattice family) rows only. Each "1.00" is a finite measurement at the
listed parameter point with the listed measurement quality, not a
universality claim.

| d | Kernel | F∝M | Distance tail | Born | Decoh | TOWARD |
|---|--------|-----|---------------|------|-------|--------|
| 2 | 1/L | **1.00** (point) | varies (2D = log) | <6e-16 | →50% | 7/7 at h≤0.5 |
| 3 | 1/L² | **1.00** (point) | **b^(-0.93)** | <4e-15 | →50% | 8/8 at h≤0.5 |
| 4 | 1/L³ | **0.99-1.00** (point) | bounded, width-limited (`W=7:-0.96`, `W=8:-0.54` companions) | 1.5e-15 .. 4.4e-15 | TBD | `3/3 .. 6/6` at h=0.5 |

The table above covers `d in {2, 3, 4}`, kernel = `1/L^(d-1)`, valley-linear
action `S = L(1-f)`, with `h <= 0.5` for d=2,3 and `h = 0.5` for d=4. No
entries are reported outside that scope.

## Newtonian predictions

| d | Newtonian deflection | Model (valley-linear) | Match? |
|---|---------------------|----------------------|--------|
| 2 | ln(b) | varies with h | consistent |
| 3 | 1/b | b^(-0.93) | **yes (~7% off)** |
| 4 | 1/b² | supportive but width-limited | needs wider lattice |

## Key properties on the tested entries

**Linear mass scaling F∝M ≈ 1.00 holds on every tested row above.** This is
a finite-entry observation across the listed (d, kernel, h, family) points,
not a universality theorem across all dimensions, all h values, or all
parameter choices. No theorem in this note proves F∝M = 1 outside the
tabulated scope. Future work could attempt that universality theorem; this
note does not.

**Decoherence is action-independent on the tested rows.** Valley-linear and
spent-delay give identical d_TV, MI, CL purity at the tested h points.
Decoherence depends on geometry, not the action formula. (Tested entries
only.)

**Born holds at machine precision on the tested rows.** This is a
mathematical property of the linear propagator on the tested
(d, kernel, h, family) points.

## Spent-delay comparison

| Property | Spent-delay | Valley-linear |
|----------|------------|---------------|
| F∝M | 0.50 (√M) | **1.00 (linear)** |
| 3D distance | b^(-0.52) | **b^(-0.93)** |
| Decoherence | identical | identical |
| Born | identical | identical |
| Gravity sign | identical | identical |

The ONLY difference is the mass/distance scaling. Everything else
is the same because decoherence and Born don't depend on the action.

## Update: Dimensional field profile (2026-04-04)

The field profile must also scale with dimension:
  f = s / r^(d-2) where d = number of spatial dimensions

| d | f(r) | Newtonian deflection | Measured tail |
|---|------|---------------------|---------------|
| 3 | s/r | 1/b | b^(-0.93) |
| 4 | s/r² | 1/b² | b^(-0.29) (early, W=7) |

The 4D tail is still at an early stage. The current frozen width note keeps
`W = 5..7`, and a heavier raw `W = 8` companion strengthens the support but
does not yet close the asymptotic law.

The complete dimensional prescription:
  Kernel: 1/L^(d-1)
  Field: s/r^(d-2)
  Action: S = L(1-f)
  Measure: h^(d-1)

All four ingredients scale with dimension d.

## 4D distance law frozen result (2026-04-04)

4D W=7, L=15, h=0.5, field f=s/r^2, valley-linear + 1/L^3:

| z | deflection | direction |
|---|-----------|-----------|
| 2 | +0.0000424 | TOWARD |
| 3 | +0.0000708 | TOWARD |
| 4 | +0.0000762 | TOWARD (peak) |
| 5 | +0.0000740 | TOWARD |
| 6 | +0.0000674 | TOWARD |

Tail from peak (z>=4): b^(-0.29), R²=0.884, 3 points
Far tail (z>=5): b^(-0.51), 2 points

This is at the SAME early stage as 3D when it showed -0.35
(which later improved to -1.07 at W=12). The 4D tail needs
W>=10 (~3M nodes in 4D) for a definitive measurement.

The honest read: 4D gravity is TOWARD with the correct field
profile and near-Newtonian mass scaling (F∝M=0.99), but the
distance exponent is unresolved due to lattice width limits.

Heavier same-family raw companion:

- `W = 8`, `L = 15`, `h = 0.5`
- Born: `4.43e-15`
- `F∝M = 1.00`
- `6/6` TOWARD on `z = 2..7`
- early tail from `z >= 4`: `b^(-0.54)`

That row is supportive, but still width-limited.
