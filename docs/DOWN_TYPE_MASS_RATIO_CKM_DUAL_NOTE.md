# Down-Type Mass Ratios from the CKM Dual

**Date:** 2026-04-16
**Status:** bounded secondary flavor-mass lane
**Primary runner:** `scripts/frontier_mass_ratio_ckm_dual.py`

## Safe statement

On the current live package surface, the promoted CKM atlas/axiom closure and
the canonical same-surface value `alpha_s(v) = 0.103303816122` imply a bounded
down-type flavor-mass lane:

- `m_d/m_s = alpha_s(v) / 2`
- `m_s/m_b = [alpha_s(v) / sqrt(6)]^(6/5)`
- `m_d/m_b = (m_d/m_s) (m_s/m_b)`

No observed quark masses are used as derivation inputs.

This lane is **bounded**, not retained or theorem-grade, because it depends on
two bridge steps outside the exact internal core:

- the standard leading-order GST relation for `|V_us|`
- the `|V_cb| = (m_s/m_b)^(5/6)` mass-ratio bridge

The lane is still useful. It converts the promoted CKM package into a reusable
down-type flavor-mass tool that can support later `y_b`, flavor-hierarchy, and
flavor-dependent cosmology / baryogenesis work.

## Inputs and bridge structure

### Internal package inputs

- [ALPHA_S_DERIVED_NOTE.md](./ALPHA_S_DERIVED_NOTE.md):
  canonical same-surface `alpha_s(v) = 0.103303816122`
- [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md):
  promoted CKM package on the canonical tensor/projector surface
  - `|V_us| = sqrt(alpha_s(v)/2)`
  - `|V_cb| = alpha_s(v)/sqrt(6)`
- exact SU(3) group constants:
  - `C_F = 4/3`
  - `T_F = 1/2`
  - `C_F - T_F = 5/6`

### Bridge-conditioned inputs

- GST:
  `|V_us| = sqrt(m_d/m_s)`
  as the standard leading-order NNI texture relation
- `5/6` bridge:
  `|V_cb| = (m_s/m_b)^(C_F - T_F)`
  used here as a bounded flavor-mass bridge rather than a retained theorem

## Down-type formulas

Equating the promoted CKM formulas with the bridge relations gives

$$
\left|V_{us}\right| = \sqrt{\frac{\alpha_s(v)}{2}}
= \sqrt{\frac{m_d}{m_s}}
\quad\Longrightarrow\quad
\frac{m_d}{m_s} = \frac{\alpha_s(v)}{2},
$$

and

$$
\left|V_{cb}\right| = \frac{\alpha_s(v)}{\sqrt{6}}
= \left(\frac{m_s}{m_b}\right)^{5/6}
\quad\Longrightarrow\quad
\frac{m_s}{m_b} =
\left[\frac{\alpha_s(v)}{\sqrt{6}}\right]^{6/5}.
$$

The chain ratio then follows algebraically:

$$
\frac{m_d}{m_b} =
\frac{m_d}{m_s}\frac{m_s}{m_b}
=
\frac{\alpha_s(v)^{11/5}}{2\,6^{3/5}}.
$$

## Current numerical surface

Using the canonical current `main` value `alpha_s(v) = 0.103303816122`:

| Ratio | Predicted | PDG mixed-scale comparator | Deviation |
|---|---|---|---|
| `m_d/m_s` | `0.05165` | `0.05000` | `+3.3%` |
| `m_s/m_b` | `0.02239` | `0.02234` | `+0.2%` |
| `m_d/m_b` | `0.001156` | `0.001117` | `+3.5%` |

The quoted PDG comparison uses the usual mixed-scale convention:

- `m_d(2 GeV) = 4.67 MeV`
- `m_s(2 GeV) = 93.4 MeV`
- `m_b(m_b) = 4.180 GeV`

## Scale qualifier

The best numerical agreement is with the PDG mixed-scale comparator
`m_s(2 GeV)/m_b(m_b)`.

If `m_s` is run to the common scale `m_b` using 1-loop QCD running, the same
formula gives

- `m_s(m_b)/m_b(m_b) = 0.01947`
- framework prediction `0.02239`
- deviation `+15.0%`

That means the current lane does **not** explain why the mixed-scale comparator
is the right comparison surface. The safe statement is therefore:

- the bounded lane matches the PDG mixed-scale convention well
- the same-scale interpretation of the `5/6` bridge remains open

## What this buys

This lane does not promote flavor masses to the retained theorem core.

It does provide a clean reusable bridge:

- promoted CKM closure
- canonical `alpha_s(v)`
- exact SU(3) constants
- bounded down-type flavor-mass extraction

That is useful downstream for:

- flavor-hierarchy organization
- future `y_b` / `m_b` anchor programs
- baryogenesis / flavor-weight packages
- future checks on whether the `5/6` bridge can be upgraded

## What is not claimed

- a retained or theorem-grade derivation of GST from the framework
- a retained or theorem-grade derivation of the `5/6` mass-ratio bridge on the
  full framework surface
- resolution of the mixed-scale versus same-scale ambiguity
- closure of the absolute bottom scale (`m_b` or `y_b`)
- closure of the up-type or charged-lepton mass sectors from this note

## Validation

Run:

```bash
python3 scripts/frontier_mass_ratio_ckm_dual.py
```

Current expected result on `main`:

- `PASS=18`
- `FAIL=0`

The runner verifies:

- the promoted CKM input formulas
- exact `C_F - T_F = 5/6`
- the bounded down-type dual extraction
- the algebraic closed forms
- the mixed-scale versus same-scale qualifier
- mild sensitivity to the canonical `alpha_s(v)` value
