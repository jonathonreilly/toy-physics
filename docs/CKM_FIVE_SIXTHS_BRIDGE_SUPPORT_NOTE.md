# CKM Five-Sixths Bridge Support Note

**Date:** 2026-04-16 (bridge support layer); 2026-04-17 (retained structural origin of `5/6` + proposed primitive P-AT that, if accepted, upgrades the bridge to a leading-order retained theorem).
**Status:** numerical-support layer for the down-type CKM-dual mass-ratio lane.
- The structural origin of the `5/6` exponent is retained on `main`: it is
  the atlas `1+5` orthogonal-complement projector weight on `Q_L` (SI3 in
  the bridge-identity note below). The numerical coincidence with the
  SU(3) Casimir combination `C_F - T_F = 5/6` is a cross-check only.
- Under the proposed new retained primitive **P-AT** (atlas-projector-weighted
  `(2,3)` off-diagonal `M_d(2,3) = m_s^(5/6) · m_b^(1/6)`), the `5/6`
  bridge `|V_cb| = (m_s/m_b)^(5/6)` is leading-order exact in the
  hierarchical limit and the quantitative mass-ratio readout derives from
  the retained CKM atlas. P-AT is a framework-level proposal with review
  pending (see the bridge-identity note).
- The quantitative mass-ratio readout remains bounded downstream.
**Primary runner:** `scripts/frontier_ckm_five_sixths_bridge_support.py`
**Authority for structural `5/6` origin (Layer 1) and P-AT proposal (Layer 2):**
[CKM_DUAL_BRIDGE_IDENTITY_THEOREM_NOTE_2026-04-17.md](CKM_DUAL_BRIDGE_IDENTITY_THEOREM_NOTE_2026-04-17.md)

## Safe statement

On the current `main` surface:

- the retained structural origin of the `5/6` exponent is the atlas
  orthogonal-complement projector weight on the six-state left-handed
  quark block `Q_L = (2, 3)`: `1 - 1/n_quark = 5/6` with
  `n_quark = dim(Q_L) = 6`
- the numerical coincidence `C_F - T_F = 4/3 - 1/2 = 5/6` is recorded as a
  cross-check only; the retained origin is the atlas `1 + 5` projector split,
  not the Casimir identity
- the promoted CKM atlas package gives `|V_cb| = alpha_s(v) / sqrt(6)`, where
  `sqrt(6) = sqrt(n_quark) = sqrt(N_c · N_iso)` is the **same** Ward-theorem
  Clebsch-Gordan that normalizes `H_unit` on `Q_L`
- the `5/6` bridge gives
  `m_s/m_b = [alpha_s(v)/sqrt(6)]^(6/5)` as an **exact algebraic identity** on
  the retained identification surface of the bridge-identity theorem
  (theorem T2)

The bounded quantitative extraction matches the threshold-local self-scale
comparator `m_s(2 GeV)/m_b(m_b)` at `+0.20%`.

If `m_s` is first run to the common scale `m_b`, the same comparison moves to
`m_s(m_b)/m_b(m_b)` and the deviation widens to about `+15%`. The two
comparison surfaces are related by the standard 1-loop transport factor

$$
\frac{m_s(2\,\mathrm{GeV})}{m_b(m_b)}
=
\frac{m_s(m_b)}{m_b(m_b)}
\left[\frac{\alpha_s(2\,\mathrm{GeV})}{\alpha_s(m_b)}\right]^{12/25}.
$$

The retained structural identity of the `5/6` exponent is now fixed by the
atlas projector weights. What is **not** yet retained:

- a framework-internal RG/transport derivation that **forces** the mass-ratio
  identification `m_s/m_b := [alpha_s(v)/sqrt(6)]^(6/5)` from the retained
  Ward-theorem UV boundary. Absent that, the mass-ratio identification is an
  atlas-consistent identification surface, not a retained framework output;
- the exact scale-selection rule that singles out the threshold-local
  self-scale comparator.

## Exact content

The exact part of the support stack is narrow but real:

- `C_F = 4/3`
- `T_F = 1/2`
- `C_F - T_F = 5/6`
- promoted CKM closure gives `|V_cb| = alpha_s(v)/sqrt(6)`

So the only non-exact step in this note is the bridge from the CKM quantity to
the down-type mass ratio:

$$
|V_{cb}| = \left(\frac{m_s}{m_b}\right)^{5/6}.
$$

## Bounded bridge read

Using the canonical same-surface value `alpha_s(v) = 0.103303816122` gives

$$
|V_{cb}|_{\mathrm{atlas}} = \frac{\alpha_s(v)}{\sqrt{6}} = 0.0421736
$$

and therefore

$$
\left(\frac{m_s}{m_b}\right)_{\mathrm{pred}}
=
|V_{cb}|_{\mathrm{atlas}}^{6/5}
=
\left[\frac{\alpha_s(v)}{\sqrt{6}}\right]^{6/5}
=
0.0223897.
$$

The PDG threshold-local self-scale comparator is

$$
\frac{m_s(2\,\mathrm{GeV})}{m_b(m_b)} = \frac{93.4\,\mathrm{MeV}}{4.180\,\mathrm{GeV}}
= 0.0223445,
$$

so the bounded bridge misses by only `+0.20%`.

## Deviation decomposition

The current small residual error separates cleanly into:

1. **bridge intrinsic accuracy on the observation surface**

   $$
   \left(\frac{m_s}{m_b}\right)_{\mathrm{obs\ from}\ |V_{cb}|}
   =
   |V_{cb}|_{\mathrm{PDG}}^{6/5}
   =
   0.0224065,
   $$

   which differs from the threshold-local comparator by `+0.28%`;

2. **atlas `|V_cb|` shift**

   the promoted CKM package gives `|V_cb| = 0.0421736`, which is `-0.06%`
   relative to the current comparator value `0.0422`, and translates into a
   `-0.075%` shift on the extracted ratio.

These multiply exactly:

$$
\frac{(m_s/m_b)_{\mathrm{pred}}}{(m_s/m_b)_{\mathrm{self}}}
=
\frac{(m_s/m_b)_{\mathrm{pred}}}{(m_s/m_b)_{\mathrm{obs\ from}\ |V_{cb}|}}
\cdot
\frac{(m_s/m_b)_{\mathrm{obs\ from}\ |V_{cb}|}}{(m_s/m_b)_{\mathrm{self}}}.
$$

That is why the live `m_s/m_b` prediction lands at `+0.20%` rather than the
`+0.28%` bridge-only offset.

## Scale statement

The live comparison surface is now:

- **threshold-local self-scale comparator**
  `m_s(2 GeV)/m_b(m_b)`

The current safe interpretation is:

- the bounded bridge is numerically coherent on the threshold-local
  self-scale surface;
- forcing a common-scale comparison strips off the one-loop transport factor
  and creates the larger mismatch;
- a theorem-grade derivation that this is the unique exact framework scale
  surface is still open.

So the mass-ratio lane should not say only “mixed-scale works, same-scale is
open.” The sharper current statement is:

- threshold-local self-scale support is real;
- full scale-choice closure is not yet theorem-grade.

## What this buys

This note upgrades the down-type mass-ratio lane in two ways:

1. the `5/6` bridge is no longer a naked bounded phrase with no current-main
   support note;
2. the scale qualifier is no longer just an unexplained PDG convention
   coincidence.

The lane is still bounded, but it now carries an explicit current-main support
stack:

- GST support:
  [CKM_FROM_MASS_HIERARCHY_NOTE.md](./CKM_FROM_MASS_HIERARCHY_NOTE.md)
- `5/6` bridge support:
  this note
- down-type extraction:
  [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](./DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md)

## What is not claimed

- a retained or theorem-grade derivation of the `5/6` bridge on the full
  framework surface
- a theorem-grade derivation of the exact scale-selection rule
- a closure of absolute `m_b` or `y_b`
- an upgrade of the down-type mass-ratio lane to retained / theorem-grade

## Validation

Run:

```bash
python3 scripts/frontier_ckm_five_sixths_bridge_support.py
```

Current expected result on `main`:

- `EXACT PASS=5`
- `BOUNDED PASS=7`
- `FAIL=0`

The runner checks:

- exact `SU(3)` identity `C_F - T_F = 5/6`
- exact promoted CKM input `|V_cb| = alpha_s(v)/sqrt(6)`
- bounded `m_s/m_b` extraction from the `5/6` bridge
- threshold-local self-scale transport from same-scale to PDG comparator
- exact multiplicative decomposition of the remaining deviation
