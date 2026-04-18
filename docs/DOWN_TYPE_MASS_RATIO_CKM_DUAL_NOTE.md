# Down-Type Mass Ratios from the CKM Dual

**Date:** 2026-04-16 (original); 2026-04-17 (three-layer status: retained structural identities + proposed new retained primitive P-AT + bounded quantitative readout)
**Status:** three-layer (Layer 1 retained structural identities + Layer 2 proposed new retained primitive P-AT + Layer 3 bounded quantitative readout)
**Primary runner:** `scripts/frontier_mass_ratio_ckm_dual.py`
**Authority (Layer 1 retained identities + Layer 2 proposed primitive P-AT):**
[CKM_DUAL_BRIDGE_IDENTITY_THEOREM_NOTE_2026-04-17.md](CKM_DUAL_BRIDGE_IDENTITY_THEOREM_NOTE_2026-04-17.md)
(companion runner: `scripts/frontier_ckm_dual_bridge_identity.py`)

## Safe statement

On the current live package surface, the promoted CKM atlas/axiom closure and
the canonical same-surface value `alpha_s(v) = 0.103303816122` combine with
the CKM-Dual Bridge Identity Theorem to give a down-type flavor-mass lane
with the following three-layer status:

- **Layer 1 — retained structural identities (unconditional on `main`):**
  - `sqrt(6)` in `|V_cb| = alpha_s(v)/sqrt(6)` is the retained Ward-theorem
    Clebsch-Gordan `sqrt(N_c · N_iso) = sqrt(dim(Q_L))` (SI1)
  - GST exponent `1/2 = 1/n_pair` is the retained atlas EWSB residual
    pair count (SI2)
  - `5/6` bridge exponent = retained atlas `1+5` orthogonal-complement
    projector weight on the six-state `Q_L` block (SI3); the numerical
    coincidence with the SU(3) Casimir combination `C_F - T_F = 5/6` is
    recorded as a cross-check, not the retained origin

- **Layer 2 — proposed new retained primitive P-AT (framework-level review pending):**
  on the retained `hw=1` down-type mass matrix, the `(2,3)` off-diagonal
  has the atlas-projector-weighted form
  `M_d(2,3) = m_s^(5/6) · m_b^(1/6)` (lighter generation weighted by CP-odd
  `5/6`, heavier by CP-even `1/6`), with `(1,2)` off-diagonal =
  `sqrt(m_d · m_s)` (NNI geometric mean) and `(1,3)` = 0 (NNI texture zero).
  Under P-AT, in the hierarchical limit `m_d/m_s -> 0`, `m_s/m_b -> 0`:
  - T1: GST `|V_us| = sqrt(m_d/m_s)` is leading-order exact
  - T2: `5/6` bridge `|V_cb| = (m_s/m_b)^(5/6)` is leading-order exact
  - T3: combining with the retained CKM atlas values `|V_us|_atlas =
    sqrt(alpha_s(v)/n_pair)` and `|V_cb|_atlas = alpha_s(v)/sqrt(n_quark)`
    gives the identification surface
    - `m_d/m_s = alpha_s(v) / n_pair`
    - `m_s/m_b = [alpha_s(v)/sqrt(n_quark)]^(n_quark/(n_quark-1)) =
      [alpha_s(v)/sqrt(6)]^(6/5)`
    - `m_d/m_b = alpha_s(v)^(11/5) / (2 · 6^(3/5))`
    as framework output.
  P-AT is a **new framework proposal**, not a derivation from pre-existing
  retained primitives. Its structural motivation is that the atlas
  bilinear tensor carrier `K_R` on `Q_L` has CP-even and CP-odd sectors
  with weights `1/6` and `5/6`, and the bridge-inducing `(2,3)`
  mass-matrix element inherits the same weighting. The acceptance or
  rejection of P-AT is a framework-level decision with review pending.

- **Layer 3 — bounded quantitative readout:** the identification surface
  (I1)-(I2) gives
  - `m_d/m_s = 0.05165` (+3.30% vs PDG self-scale comparator)
  - `m_s/m_b = 0.02239` (+0.20%)
  - `m_d/m_b = 0.001156` (+3.50%)

No observed quark masses are used as derivation inputs.

What remains open (named):
- a framework-internal operator-theoretic derivation of P-AT from the
  atlas bilinear tensor carrier `K_R` on `Q_L` that would elevate P-AT
  from proposed to retained;
- a sub-leading-order correction program beyond the hierarchical
  leading-order exact bridges under P-AT;
- a framework-internal scale-selection theorem that forces the
  threshold-local self-scale comparator.

The lane converts the promoted CKM package into a reusable down-type
flavor-mass tool with retained exponent structure (Layer 1) plus the
proposed P-AT primitive (Layer 2) that, if accepted, upgrades the
identification surface to a framework output.

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
  - support:
    [CKM_FROM_MASS_HIERARCHY_NOTE.md](./CKM_FROM_MASS_HIERARCHY_NOTE.md)
- `5/6` bridge:
  `|V_cb| = (m_s/m_b)^(C_F - T_F)`
  used here as a bounded flavor-mass bridge rather than a retained theorem
  - support:
    [CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md](./CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md)

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

| Ratio | Predicted | threshold-local self-scale comparator | Deviation |
|---|---|---|---|
| `m_d/m_s` | `0.05165` | `0.05000` | `+3.3%` |
| `m_s/m_b` | `0.02239` | `0.02234` | `+0.2%` |
| `m_d/m_b` | `0.001156` | `0.001117` | `+3.5%` |

The quoted comparison uses the usual threshold-local PDG self-scale
convention:

- `m_d(2 GeV) = 4.67 MeV`
- `m_s(2 GeV) = 93.4 MeV`
- `m_b(m_b) = 4.180 GeV`

## Scale qualifier

The live comparison surface is the threshold-local self-scale comparator
`m_s(2 GeV)/m_b(m_b)`.

If `m_s` is run to the common scale `m_b` using 1-loop QCD running, the same
formula gives

- `m_s(m_b)/m_b(m_b) = 0.01947`
- framework prediction `0.02239`
- deviation `+15.0%`

The two comparison surfaces are related by the standard one-loop transport law

$$
\frac{m_s(2\,\mathrm{GeV})}{m_b(m_b)}
=
\frac{m_s(m_b)}{m_b(m_b)}
\left[\frac{\alpha_s(2\,\mathrm{GeV})}{\alpha_s(m_b)}\right]^{12/25},
$$

with transport factor `1.14747` on the current observation surface.

So the sharper current safe statement is:

- the bounded lane matches the threshold-local self-scale comparator well;
- forcing a common-scale read removes a material transport factor and gives the
  larger mismatch;
- theorem-grade closure of the exact scale-selection rule remains open.

## What this buys

This lane does not promote flavor masses to the retained theorem core.

It does provide a clean reusable bridge:

- promoted CKM closure
- canonical `alpha_s(v)`
- exact SU(3) constants
- GST support
- bounded `5/6` bridge support
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
- theorem-grade closure of the exact scale-selection rule for `m_s/m_b`
- closure of the absolute bottom scale (`m_b` or `y_b`)
- closure of the up-type or charged-lepton mass sectors from this note

## Validation

Run:

```bash
python3 scripts/frontier_mass_ratio_ckm_dual.py
```

Current expected results on `main`:

- `frontier_mass_ratio_ckm_dual.py`: `PASS=23 FAIL=0`
- `frontier_ckm_five_sixths_bridge_support.py`: `EXACT PASS=5`, `BOUNDED PASS=7`, `FAIL=0`

The primary lane runner verifies:

- the promoted CKM input formulas
- exact `C_F - T_F = 5/6`
- the bounded down-type dual extraction
- the algebraic closed forms
- the threshold-local self-scale versus same-scale qualifier
- mild sensitivity to the canonical `alpha_s(v)` value

The support runner verifies:

- the exact `5/6` `SU(3)` identity
- bounded `m_s/m_b` extraction from `|V_cb|`
- one-loop transport from same-scale to threshold-local self-scale comparator
- exact multiplicative decomposition of the remaining `m_s/m_b` deviation
