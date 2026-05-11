# Quark Mass Ratios from the Taste-Staircase + EWSB Cascade

**Date:** 2026-04-25

**Status:** bounded zero-import support packet for the down-type quark
mass-ratio route. This note sharpens the existing bounded lane by giving
an explicit zero-import cascade presentation and a cubic-exact NNI
self-consistency check, but it does **not** promote the route to retained
or close the CKM gate on its own because the `m_s/m_b` step still depends
on the bounded `5/6` bridge and the `m_d/m_s` link still uses the GST /
NNI structural bridge.

**Primary runner:** `scripts/frontier_quark_mass_ratios_taste_staircase_support.py`
**Role:** bounded follow-up support note for the down-type quark mass-ratio
lane.

**Cross-references**
- [`ALPHA_S_DERIVED_NOTE.md`](./ALPHA_S_DERIVED_NOTE.md) — retained
  `alpha_s(v)` lane.
- [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](./ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md) — `alpha_LM^2 = alpha_bare * alpha_s(v)`.
- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) —
  promoted CKM atlas package.
- `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md` — `5/6 = C_F - T_F` bridge support.
- `CKM_FROM_MASS_HIERARCHY_NOTE.md` (GST relation provenance; backticked
  to avoid length-2 cycle — that note already cites this one as the
  load-bearing one-hop authority for the down-type mass-ratio readings
  in its PATH C cite-chain disposition).
- [`CL3_TASTE_GENERATION_THEOREM.md`](./CL3_TASTE_GENERATION_THEOREM.md) —
  generation structure from the taste cube.
- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) — hierarchy theorem `v = M_Pl (7/8)^{1/4} alpha_LM^16`.
- `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md` — predecessor bounded lane; this note sharpens that route with an explicit zero-import presentation and a cubic-exact NNI consistency check.

## 1. Support statement

On the retained plaquette / coupling-map (CMT) surface, together with the
existing GST / NNI structural bridge and the bounded `5/6` bridge support,
the down-type quark mass-ratio route takes the closed forms

```text
m_d / m_s   =  alpha_s(v) / n_pair                       =  alpha_s(v) / 2
m_s / m_b   = [alpha_s(v) / sqrt(n_quark)]^{1/(C_F - T_F)}
            = [alpha_s(v) / sqrt(6)]^{6/5}
m_d / m_b   = (m_d / m_s)(m_s / m_b)
            = alpha_s(v)^{11/5} / (2 * 6^{3/5})
```

with retained / exact internal inputs

```text
alpha_s(v) = alpha_bare / u_0^2                       (CMT, retained)
n_pair     = 2     (Higgs Z_2 doublet, EWSB residual)
n_quark    = 2 N_c = 6     (Q_L = (2,3) block dim)
C_F - T_F  = 4/3 - 1/2 = 5/6     (exact SU(3) Casimir difference)
```

The CKM atlas closure gives, as parallel zero-import outputs of the same
surface,

```text
|V_us|_atlas  =  sqrt(alpha_s(v) / n_pair)    =  sqrt(alpha_s(v) / 2)
|V_cb|_atlas  =  alpha_s(v) / sqrt(n_quark)   =  alpha_s(v) / sqrt(6)
```

and the two named bridge equations read

```text
GST identity     :  |V_us|^2     =  m_d / m_s
5/6 bridge       :  |V_cb|       = (m_s / m_b)^{5/6}
```

with no PDG quark masses entering the derivation. The route is still
**bounded** because those bridges are not both promoted on the retained
surface: GST remains a structural NNI bridge, and the `5/6` mechanism
remains bounded support.

## 2. What changes vs the prior bounded lane

The predecessor note
`DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`
derived the same down-type ratios by *inverting* the CKM atlas through
GST and the `5/6` bridge. It carried the bounded label because:

1. the bridges were treated as derivation-direction inputs (atlas to
   ratios), not as cross-checks;
2. the down-type ratios were therefore "extracted" rather than
   independently produced.

This note exhibits two algebraically matching presentations of the same
bounded route:

- **Path A (cascade presentation).** Inputs `alpha_s(v), n_pair,
  n_quark, C_F - T_F` give the same closed forms as Section 1.

- **Path B (atlas + bridge presentation).** Inputs `V_us_atlas,
  V_cb_atlas` combine with GST and `5/6` to give the same two ratios.

Paths A and B agree algebraically (verified to machine precision in the
runner). That is useful support, but it does **not** upgrade the lane to
retained because both presentations still rely on the existing bridge
layer.

PDG values are used only as the post-derivation comparator.

## 3. Inputs and import audit

| Quantity | Value | Status | Provenance |
|----------|-------|--------|------------|
| `<P>` | `0.5934` | EVALUATED | retained plaquette MC |
| `u_0 = <P>^{1/4}` | `0.877681...` | DERIVED | tadpole improvement |
| `alpha_bare = 1/(4 pi)` | `0.0795775...` | DERIVED | bare gauge normalization |
| `alpha_LM = alpha_bare/u_0` | `0.0906678...` | DERIVED | LM coupling |
| `alpha_s(v) = alpha_bare/u_0^2` | `0.1033038...` | DERIVED | CMT, retained `alpha_s(v)` lane |
| `n_pair = 2` | `2` | DERIVED | Higgs Z_2 doublet (EWSB residual pair) |
| `n_quark = 2 N_c = 6` | `6` | DERIVED | Q_L block dim |
| `C_F = 4/3` | `4/3` | EXACT | SU(3) fundamental Casimir |
| `T_F = 1/2` | `1/2` | EXACT | SU(3) Dynkin index |
| `C_F - T_F = 5/6` | `5/6` | EXACT | Casimir difference |
| `|V_us|_atlas = sqrt(alpha_s(v)/2)` | `0.227271` | DERIVED | CKM atlas closure |
| `|V_cb|_atlas = alpha_s(v)/sqrt(6)` | `0.042174` | DERIVED | CKM atlas closure |
| GST identity `V_us^2 = m_d/m_s` | -- | STRUCTURAL | NNI texture algebra |
| `5/6` bridge `V_cb = (m_s/m_b)^{5/6}` | -- | BOUNDED | strong-coupling Casimir-difference exponentiation at `g=1` |
| PDG `m_d, m_s, m_b` | -- | COMPARATOR | post-derivation only |

**No row says IMPORTED.** Every quantity is either retained / derived
from the framework or used as a post-derivation comparator. The chain is
zero-import end-to-end.

## 4. Numerical surface

The retained inputs evaluate to

```text
m_d / m_s  =  0.051652
m_s / m_b  =  0.022390
m_d / m_b  =  0.001156
|V_us|     =  0.227271       (= sqrt(m_d/m_s) by GST)
|V_cb|     =  0.042174       (= (m_s/m_b)^{5/6} by 5/6 bridge)
|V_ub|     =  0.003913       (atlas, |V_ub|_0 = alpha_s(v)^{3/2}/(6 sqrt(2)))
```

versus the PDG threshold-local self-scale comparator

```text
m_d(2 GeV) / m_s(2 GeV)  =  4.67 / 93.4    =  0.050000
m_s(2 GeV) / m_b(m_b)    =  93.4 / 4180    =  0.022344
m_d(2 GeV) / m_b(m_b)    =  4.67 / 4180    =  0.001117
|V_us|_PDG               =  0.2243
|V_cb|_PDG               =  0.0422
```

| Observable | Framework | PDG | Deviation |
|------------|-----------|-----|-----------|
| `m_d / m_s` | `0.05165` | `0.05000` | `+3.30%` |
| `m_s / m_b` | `0.02239` | `0.02234` | `+0.20%` |
| `m_d / m_b` | `0.001156` | `0.001117` | `+3.51%` |
| `\|V_us\|`  | `0.22727` | `0.22430` | `+1.32%` |
| `\|V_cb\|`  | `0.04217` | `0.04220` | `-0.06%` |

The independent atlas path gives `|V_us|` and `|V_cb|` to the same
numerical values to machine precision (Path A equals Path B
algebraically). The mass-ratio comparators are reproduced to `+3.3%`
and `+0.2%` on the threshold-local self-scale convention.

## 5. NNI texture self-consistency

A standard nearest-neighbour-interaction mass matrix in the down-type
geometric-mean normalization,

```text
M_d  =  m_b * [[0,                  c_12 sqrt(m_d/m_s) sqrt(m_s/m_b),  0  ],
               [c_12 sqrt(m_d/m_s) sqrt(m_s/m_b),  0,  c_23 sqrt(m_s/m_b)],
               [0,                  c_23 sqrt(m_s/m_b),                1  ]],
```

admits the framework eigenvalue triple `(m_d, m_s, m_b)` exactly when
`(c_12, c_23)` are solved from the cubic eigenvalue invariants with the
canonical Fritzsch sign pattern `(+m_d, -m_s, +m_b)`. The runner verifies
the cubic-exact construction:

```text
c_12 = 1.0108     (O(1), admissible)
c_23 = 0.9738     (O(1), admissible)
```

so the NNI texture is internally consistent with the framework mass
ratios. The leading-order anchor `c_12 = c_23 = 1` reproduces the GST
identity to within the expected `O(m_s/m_b) ~ 2%` correction class.

## 6. Provenance of each closed-form factor

### 6.1 The 1-2 ratio: `m_d/m_s = alpha_s(v)/n_pair`

Provenance summary:

- The factor `alpha_s(v)` is the strong-gauge coupling at the EW scale
  on the CMT surface. It enters the CKM atlas as `lambda^2 =
  alpha_s(v)/n_pair`, and via GST it equals `m_d/m_s` exactly.
- The denominator `n_pair = 2` is the Higgs `Z_2` doublet pair
  responsible for EWSB. It is the same `n_pair` that fixes
  `lambda^2 = alpha_s(v)/n_pair` in the atlas.

Equivalently, one can read `m_d/m_s = alpha_s(v)/n_pair` as a direct
consequence of the EWSB-Yukawa cascade structure: the leading 1-2
mass-mixing operator carries the `1/n_pair` Higgs-pair selector and the
gauge-coupling factor `alpha_s(v)`.

### 6.2 The 2-3 ratio: `m_s/m_b = [alpha_s(v)/sqrt(n_quark)]^{1/(C_F-T_F)}`

Provenance summary:

- The base `alpha_s(v)/sqrt(n_quark) = alpha_s(v)/sqrt(6)` is the
  atlas-leading `|V_cb|`. It carries the geometric mean of the quark
  block: `sqrt(n_quark) = sqrt(2 N_c) = sqrt(6)`.
- The exponent `1/(C_F - T_F) = 6/5` is the inverse of the SU(3)
  Casimir difference. At lattice strong coupling `g = 1`, the
  Casimir-difference exponentiation maps the 2-3 mass-mixing amplitude
  to the mass-eigenvalue ratio with this power.

The same structure produces the `5/6` bridge: `V_cb = (m_s/m_b)^{5/6}`
is the inverse of `m_s/m_b = V_cb^{6/5}`.

### 6.3 The chain: `m_d/m_b = alpha_s(v)^{11/5} / (2 * 6^{3/5})`

The `11/5 = 1 + 6/5` exponent is the sum of the two stage exponents
(`1` for the 1-2 stage and `6/5` for the 2-3 stage). The numerator
`6^{3/5}` simplifies as `(sqrt(6))^{6/5}`. The combined formula is the
algebraic consequence of multiplying the two independent ratios.

## 7. What this sharpens

What this note improves over the older bounded dual note is narrower and
more honest:

- it removes PDG quark masses from the *route presentation* itself;
- it makes the closed forms explicit from the retained `alpha_s(v)`,
  `n_pair`, `n_quark`, `C_F - T_F` surface;
- it verifies that a cubic-exact NNI texture admits the resulting
  framework ratios with admissible `c_12, c_23 = O(1)`.

What it does **not** do is close the CKM gate on a retained surface.
The gate remains bounded at this layer because:

- `m_d/m_s` still leans on the GST / NNI bridge;
- `m_s/m_b` still leans on the bounded `5/6` bridge;
- the non-perturbative `g = 1` mechanism behind the `5/6`
  exponentiation is still open.

The match accuracy on the threshold-local self-scale comparator is

| Observable | Framework | PDG | Deviation |
|------------|-----------|-----|-----------|
| `m_s / m_b` | `0.02239` | `0.02234` | `+0.20%` |
| `m_d / m_s` | `0.05165` | `0.05000` | `+3.30%` |
| `\|V_cb\|`  | `0.04217` | `0.04220` | `-0.06%` |
| `\|V_us\|`  | `0.22727` | `0.22430` | `+1.32%` |

The remaining `+3.3%` deviation on `m_d/m_s` is the inherent leading-order
GST class: it propagates to the `+1.3%` `V_us` framework prediction. The
leading-order Fritzsch NNI shows a comparable `~2%` class of corrections;
the cubic-exact NNI absorbs them into `c_12, c_23 = O(1)` admissible
texture coefficients (Section 5). No precision is borrowed from PDG.

## 8. What this note does NOT claim

1. A theorem-grade derivation of the `5/6` strong-coupling Casimir-
   difference exponentiation mechanism at `g = 1`. The bridge stays as
   bounded support, with the support stack already documented in
   `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md`.
2. Promotion of GST / NNI from structural bridge status to retained
   theorem-grade framework content.
3. A retained closure of the absolute bottom-quark scale `m_b` or the
   bottom Yukawa `y_b`. Only the down-type *ratios* are produced.
4. A retained derivation of the up-type ratios (`m_u/m_c`, `m_c/m_t`).
   Those remain bounded under the parallel-bridge ansatz of
   [`UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md`](./UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md)
   and are not addressed here.
5. A retained derivation of the CKM CP phase `delta` or the Jarlskog
   invariant. Those are carried by the existing CKM atlas / CP package.
6. Promotion of GST to a higher-order (beyond leading) identity. GST
   `V_us^2 = m_d/m_s` is exact at leading order; subleading `O(m_s/m_b)`
   corrections are absorbed into the cubic-exact NNI coefficients.
7. A unique prediction of the *threshold-local self-scale* comparator as
   the framework's natural scale. Section 3 of
   [`CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md`](./CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md)
   tracks the scale-convention question separately.

## 9. Validation

```bash
python3 scripts/frontier_quark_mass_ratios_taste_staircase_support.py
```

Expected output: `PASS=55, FAIL=0`.

The runner verifies:

1. retained zero-import inputs (Part 0): `<P>`, `u_0`, `alpha_bare`,
   `alpha_LM`, `alpha_s(v)`, `n_pair`, `n_quark`, `C_F`, `T_F`,
   `C_F - T_F`, `1/(C_F-T_F)`;
2. closed-form mass ratios (Part 1) and their algebraic consistency;
3. PDG threshold-local self-scale comparator (Part 2) at `+3.3%`,
   `+0.2%`, `+3.5%` deviations;
4. GST identity `V_us^2 = m_d/m_s` (Part 3) — algebraic and within
   `1.3%` of PDG `V_us`;
5. `5/6` bridge `V_cb = (m_s/m_b)^{5/6}` (Part 4) — algebraic and within
   `0.06%` of PDG `V_cb`;
6. NNI texture self-consistency (Part 5): leading-order Fritzsch
   anchor + cubic-exact construction with `c_12, c_23 = O(1)`;
7. independent path agreement (Part 6): cascade vs atlas+identities to
   machine precision;
8. round-trip (Part 7): mass ratios -> CKM -> match atlas;
9. import audit (Part 8): no IMPORTED rows;
10. bounded-route closeout (Part 9): `QUARK_MASS_RATIOS_TASTE_STAIRCASE_SUPPORT=TRUE`,
    `CKM_GATE_ZERO_IMPORT_RETAINED=FALSE`,
    `FIVE_SIXTHS_BRIDGE_NONPERTURBATIVE_MECHANISM_THEOREM_GRADE=FALSE`.

## 10. Reading rule

This note is a **bounded support follow-up** to
`DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`,
not a replacement for the repo's retained claim surface. Read it as the
cleanest current zero-import presentation of the down-type route plus an
explicit cubic-exact NNI admissibility check. The atlas / identities side
remains the controlling authority for `V_us, V_cb`, and the full quark
lane remains bounded.
