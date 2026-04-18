# CKM-Dual Bridge Identity: Structural Identities + Proposed Texture Ansatz
## (Branch-Local Proposal — Not Wired Into The Live Package)

**Date:** 2026-04-17 (first draft); revised 2026-04-17 (review v1: three-layer
split); revised 2026-04-17 (review v2: branch-local scope, unaudited-K_R
claims backed off).
**Scope:** this note is a **branch-local proposal** on
`claude/angry-chatelet-2dc78c`. It is deliberately **not** wired into the
live publication/arXiv/front-door surfaces. Acceptance into the retained
framework would require additional work named at the bottom of this note.
**Primary runner:** `scripts/frontier_ckm_dual_bridge_identity.py`

This note has two independent layers with independent evidence status:

- **Layer 1 — structural constants identification (numerical, on this
  branch).** The `\sqrt{6}`, `1/n_{pair}`, and `5/6` constants that appear
  when the down-type CKM-dual lane is written algebraically are the same
  constants that appear in the retained Ward-identity theorem and the
  promoted CKM atlas. The runner certifies this as arithmetic identities
  on retained inputs.
- **Layer 2 — proposed mass-matrix texture ansatz (numerical, on this
  branch).** A specific `3x3` symmetric mass-matrix ansatz with
  NNI-geometric `(1,2)`, atlas-exponent `(2,3)` off-diagonal
  `m_s^{5/6} m_b^{1/6}`, and `(1,3) = 0` reproduces the GST and `5/6`
  bridge as leading-order-exact hierarchical identities under numerical
  diagonalization. The runner certifies this as numerical consequences of
  the chosen ansatz.

Neither layer is landed on the live publication surfaces by this note.

## What this note explicitly does not claim

To avoid the over-promotion flagged in the review series on this branch,
the following claims are **not** being made here:

1. It is **not** claimed that the proposed `3x3` texture ansatz is
   realized by, embedded in, or derived from the retained `Z_2` `hw=1`
   normal form of the down-type mass matrix
   ([Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md)).
   The retained normal form is a 5-real-parameter family; the ansatz
   below is a specific texture with two free ratios, and its embedding
   in that 5-parameter family is not audited by the runner.
2. It is **not** claimed that the atlas `1 + 5` projector structure on
   the `Q_L` block — specifically the bilinear tensor carrier `K_R` from
   [S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md](S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md)
   — forces the `(2,3)` off-diagonal to have the atlas-exponent form. The
   `K_R` language is used only as the **structural motivation** for why
   the exponents `(5/6, 1/6)` are the natural candidates; the runner does
   not audit any operator-level identification with `K_R`.
3. It is **not** claimed that GST or the `5/6` bridge are retained
   framework-output theorems in any sense. The runner certifies only
   (a) arithmetic identities on retained inputs and (b) numerical
   consequences of a chosen texture ansatz.
4. No publication/arXiv/front-door row is promoted, demoted, or otherwise
   altered by this note or by this branch.

## Retained inputs used (unchanged, cited only)

1. Ward-identity theorem:
   [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](YT_WARD_IDENTITY_DERIVATION_THEOREM.md)
   gives `y_t(M_Pl)/g_s(M_Pl) = 1/\sqrt{6}` with `Z^2 = N_c · N_{iso} = 6`
   on `Q_L`.
2. CKM atlas closure:
   [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
   gives `|V_{us}|_{atlas} = \sqrt{\alpha_s(v)/2}`,
   `|V_{cb}|_{atlas} = \alpha_s(v)/\sqrt{6}`.
3. Atlas `1 + 5` projector split on `Q_L`:
   same atlas note; `CENTER\_EXCESS\_WEIGHT = 1/6`, `ORTHOGONAL\_PHASE\_WEIGHT = 5/6`.
4. Canonical `\alpha_s(v)`:
   [ALPHA_S_DERIVED_NOTE.md](ALPHA_S_DERIVED_NOTE.md).

## Layer 1 — structural constants identification

SI1, SI2, SI3 are arithmetic identities on retained framework inputs.

**SI1.** `\sqrt{6}` appearing in `|V_{cb}|_{atlas}` equals
`\sqrt{N_c · N_{iso}}` from the Ward identity; both derive from
`n_{quark} = \dim(Q_L) = 6`.

**SI2.** The exponent `1/2` that would appear in a GST relation
`|V_{us}| = (m_d/m_s)^{1/2}` equals `1/n_{pair}` with `n_{pair} = 2`
from the retained atlas EWSB residual pair count.

**SI3.** The exponent `5/6` that would appear in a bridge relation
`|V_{cb}| = (m_s/m_b)^{5/6}` equals the atlas orthogonal-complement
projector weight `1 - 1/n_{quark} = 5/6`. The coincidence
`C_F - T_F = 5/6` (SU(3) Casimir combination) is recorded as a
numerical coincidence, not an independent derivation.

The runner certifies SI1, SI2, SI3 as closed-form arithmetic on retained
constants. No mass-matrix ansatz is invoked for these checks.

## Layer 2 — proposed mass-matrix texture ansatz (branch-local)

**Texture ansatz P-AT.** On a `3x3` symmetric real mass-matrix in an
axis basis `(X_1, X_2, X_3)` with ordered masses
`m_d < m_s < m_b`:

```
    M_d(1,1) = m_d
    M_d(2,2) = m_s
    M_d(3,3) = m_b
    M_d(1,2) = M_d(2,1) = \sqrt{m_d · m_s}            (NNI geometric mean)
    M_d(2,3) = M_d(3,2) = m_s^{5/6} · m_b^{1/6}       (atlas-exponent ansatz)
    M_d(1,3) = M_d(3,1) = 0                           (NNI texture zero)
```

P-AT is a chosen texture ansatz. Its structural motivation is that the
atlas bilinear tensor carrier `K_R` on `Q_L` decomposes into CP-even
(weight `1/6`) and CP-odd (weight `5/6`) sectors, suggesting that the
bridge-inducing `(2,3)` mass-matrix element might inherit similar
exponents. This is a motivating heuristic, not a derivation.

**Numerical consequences under P-AT (what the runner certifies).**
Under numerical diagonalization of P-AT at a sequence of hierarchical
scalings `(m_d/m_s, m_s/m_b) = (\epsilon, \epsilon)` for
`\epsilon \in \{10^{-1}, 10^{-2}, 10^{-3}, 10^{-4}, 10^{-5}, 10^{-6}\}`,
assuming `U_u = I` (up-type diagonal in weak basis):

- `|V_{us}|_{P-AT} / \sqrt{m_d/m_s}` tends to `1` monotonically as
  `\epsilon \to 0`;
- `|V_{cb}|_{P-AT} / (m_s/m_b)^{5/6}` tends to `1` monotonically as
  `\epsilon \to 0`.

**Identification-surface arithmetic.** If one additionally imposes the
equations

```
    |V_{us}|_{P-AT} = |V_{us}|_{atlas}                                (A1)
    |V_{cb}|_{P-AT} = |V_{cb}|_{atlas}                                (A2)
```

with the leading-order P-AT expressions `\sqrt{m_d/m_s}` and
`(m_s/m_b)^{5/6}`, the arithmetic forces

```
    m_d/m_s  =  \alpha_s(v) / n_{pair}                                (I1)
    m_s/m_b  =  [\alpha_s(v)/\sqrt{n_{quark}}]^{n_{quark}/(n_{quark}-1)}
             =  [\alpha_s(v)/\sqrt{6}]^{6/5}                          (I2)
```

The runner treats (I1)–(I2) as definitions for the purpose of evaluating
the P-AT ansatz at the observed hierarchy; it does not claim (I1)–(I2)
are derived from retained framework objects.

## Numerical readout (reference only, not a publication lane)

At `\alpha_s(v) = 0.103303816122` the closed-form (I1)–(I2) give:

| Ratio | Closed form | PDG threshold-local comparator | Deviation |
|---|---|---|---|
| `m_d/m_s` | `0.0516519` | `0.0500000` | `+3.30%` |
| `m_s/m_b` | `0.0223897` | `0.0223445` | `+0.20%` |
| `m_d/m_b` | `0.001156` | `0.001117` | `+3.50%` |

These numbers are reported here as a record of where the P-AT ansatz
lands against standard PDG self-scale ratios. They are not claimed as a
promoted or retained quantitative lane, and the existing
`DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md` + `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md`
bounded lane on `main` is unchanged by this note.

## Named open work required for any future promotion

This branch-local note does not attempt these steps. They are named so
that future work on an accepting branch knows what would be required:

1. **Embedding in the retained `Z_2` `hw=1` normal form.** Show
   explicitly that the P-AT texture ansatz is a point (or a low-
   dimensional slice) of the retained 5-real-parameter family in
   [Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md](Z2_HW1_MASS_MATRIX_PARAMETRIZATION_NOTE.md),
   and identify the specific `Z_2` parameters `(a, b, c, d)` that
   realize it. The current runner does not do this.
2. **Operator-level derivation from `K_R`.** Show explicitly that the
   bilinear tensor carrier `K_R` in
   [S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md](S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md),
   projected onto the generation `hw=1` subspace, gives a `(2,3)`
   off-diagonal with exponents `(5/6, 1/6)` rather than, e.g., geometric-mean
   exponents `(1/2, 1/2)`. The current runner does not do this and the
   current heuristic does not do this.
3. **Up-type compatibility.** Check that the assumption `U_u = I` is
   compatible with a corresponding up-type texture on the same retained
   surface. The current runner uses `U_u = I` as a choice without
   auditing it against any retained up-type structure.
4. **Next-to-leading-order residuals under P-AT.** At the observed
   hierarchy, the P-AT diagonalization deviates from GST by roughly
   `O(m_d/m_s) ~ 5%` and from the `5/6` bridge by roughly
   `O(m_s/m_b) ~ 2%`. A systematic NLO account of these residuals
   would tighten or falsify the ansatz; none is done here.
5. **Scale-selection theorem for the observation comparator.** The
   threshold-local self-scale PDG comparator is used without a framework-
   internal derivation of its uniqueness. Unchanged from prior review.

Until at least items 1 and 2 are done, P-AT is a numerical proposal on
this branch and is deliberately kept out of the live publication
surfaces.

## Relation to prior notes (no content changes triggered)

This note links the existing bounded lane notes as reading material only.
It does not modify their status on `main`.

- [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md):
  bounded secondary flavor-mass lane on `main`.
- [CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md](CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md):
  bounded support tool on `main`; its runner certifies the Casimir
  arithmetic plus bounded self-scale numerics, which remains its honest
  scope.
- [CKM_FROM_MASS_HIERARCHY_NOTE.md](CKM_FROM_MASS_HIERARCHY_NOTE.md):
  bounded historical route for GST.

## Validation

Run:

```bash
python3 scripts/frontier_ckm_dual_bridge_identity.py
```

Expected on this branch:

- `RETAINED PASS` checks on SI1, SI2, SI3 structural-identity arithmetic;
- `P-AT PASS` checks on the hierarchical-limit numerical consequences of
  the chosen ansatz, plus the identification-surface arithmetic under
  (A1)–(A2);
- `BOUNDED PASS` reference comparisons against PDG threshold-local
  self-scale;
- `FAIL = 0`.

The runner's own summary explicitly frames this as "proposal with
numerics, not framework-primitive certification," consistent with the
named-open-work list above.
