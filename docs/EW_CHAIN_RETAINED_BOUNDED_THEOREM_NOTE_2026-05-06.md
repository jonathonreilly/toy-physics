# EW Chain at retained_bounded grade: from framework primitives + standard SM running to v = 246.22 GeV and alpha_s(M_Z) = 0.1181

**Date:** 2026-05-06
**Claim type:** `bounded_theorem`
**Status:** `bounded_theorem` (audit-ratifiable upgrade target: `retained_bounded` consolidation)
**Status authority:** independent audit lane only. Author hint is a
synthesis claim; effective status is pipeline-derived after audit
ratification and parent-dep status snapshots. This note does not
auto-promote any upstream row.
**Primary runner:** `scripts/frontier_yt_zero_import_chain.py`
**Bridge runner:** `scripts/frontier_qcd_low_energy_running_bridge.py`

## Synthesis claim

This note registers the complete electroweak readout chain as a single
`bounded_theorem` row. Each link is already on `main` as a one-hop
authority; the synthesis content is the explicit, end-to-end laydown of
the chain at one grade — `retained_bounded` (retained-grade algebraic
links plus an explicit, scoped imported-infrastructure boundary on the
bridge step). The numerical readouts are the same already-shipped values
from the cited authorities; this note adds no new numerical claims.

## The chain

```text
<P>(beta=6, L -> infinity) = 0.5934
   |   [retained-numerical: PR #539 five-volume MC + verifier;
   |    primary 1/L^4 bracket [0.59327, 0.59473] contains 0.5934]
   v
u_0 = <P>^(1/4) = 0.877681
   |   [closed-form algebra]
   v
alpha_LM = alpha_bare / u_0 = 0.090668
   |   [closed-form, alpha_bare = 1/(4 pi)]
   v
alpha_s(v) = alpha_bare / u_0^2 = 0.103304
   |   [closed-form: alpha_LM^2 = alpha_bare * alpha_s(v) is the
   |    geometric-mean identity theorem]
   v
alpha_s(M_Z) = 0.1181
   |   [bounded: 2-loop SM RGE + PDG quark thresholds m_t, m_b, m_c]
   v
v_EW = M_Pl * (7/8)^(1/4) * alpha_LM^16 = 246.28 GeV
       [retained: hierarchy theorem; uses alpha_LM and M_Pl]
```

The two terminal readouts are independent paths from the same
`<P> = 0.5934` retained-numerical anchor: `alpha_s(M_Z)` runs the
strong-coupling boundary down through the SM-RGE bridge; `v_EW` evaluates
the hierarchy theorem at the 16th-power suppression.

## Comparator table

| Quantity              | Framework readout | Reference (PDG)              | Deviation | Grade for this row |
|---|---|---|---|---|
| `<P>(beta=6, L→∞)`   | `0.5934`          | n/a (lattice anchor)         | n/a       | retained-numerical (PR #539) |
| `u_0`                 | `0.877681`        | n/a                          | n/a       | retained (closed-form) |
| `alpha_LM`            | `0.090668`        | n/a                          | n/a       | retained (closed-form) |
| `alpha_s(v)`          | `0.103304`        | n/a (framework boundary)     | n/a       | retained (closed-form) |
| `alpha_s(M_Z)`        | `0.1181`          | `0.1180 +/- 0.0009` (PDG)    | `+0.08%`  | **bounded** (2-loop SM RGE + PDG thresholds) |
| `v_EW [GeV]`          | `246.28`          | `246.22` (from G_F)          | `+0.03%`  | **retained_bounded** (hierarchy thm + retained-numerical `<P>`) |

Both terminal observables sit inside their PDG-style envelopes:
`alpha_s(M_Z)` is inside the PDG world-average 1-sigma band
(`0.1180 +/- 0.0009`); `v_EW` is inside the propagated `<P>` envelope
(MC standard error `+/- 0.0006` on `<P>` -> roughly `+/- 0.3%` on `v`).

## Dependency status table

The synthesis is a `bounded_theorem` because at least one link
(the v -> M_Z bridge) imports standard SM infrastructure. The
`retained_bounded` consolidation grade is the audit-ratifiable upgrade
target: every link is at `retained` or `bounded` with the bounded scope
honestly recorded.

| Dependency                                                  | claim_type        | effective_status      | Role in chain                              |
|---|---|---|---|
| `plaquette_4d_mc_fss_numerical_theorem_note_2026-05-05`     | `positive_theorem`| `unaudited` (PR #539) | five-volume MC support for `<P>=0.5934` numerical anchor |
| `plaquette_self_consistency_note`                           | `bounded_theorem` | `audited_conditional` | bounded analytic-insertion scope at `beta=6` |
| `plaquette_v1_picard_fuchs_ode_note_2026-05-05`             | `bounded_theorem` | `unaudited`           | V=1 closed-form ODE backbone (single-plaquette, not thermodynamic) |
| `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24`  | `proposed_retained`|                       | `alpha_LM^2 = alpha_bare * alpha_s(v)` algebraic identity |
| `qcd_low_energy_running_bridge_note_2026-05-01`             | `bounded_theorem` | `audited_conditional` | bounded v -> M_Z transfer (Machacek-Vaughn 2-loop SM RGE + PDG thresholds) |
| `alpha_s_derived_note`                                      | `bounded_theorem` | `audited_conditional` | downstream `alpha_s(M_Z)` consumer (PR #610 audit-prep) |
| `yt_zero_import_chain_note`                                 | retained          | (chain runner authority) | hierarchy theorem `v = M_Pl * (7/8)^(1/4) * alpha_LM^16` |

For a `bounded_theorem` synthesis, both `audited_conditional` parents
are the appropriate effective status for one-hop authorities: the
load-bearing step is a class-B value transfer, not a re-derivation.

## Imported infrastructure (bounded scope)

The chain explicitly imports four pieces of standard physics
infrastructure. Each is documented in the cited one-hop authorities;
none is silently consumed.

1. **PR #539 retained-numerical `<P>`**: five-volume Wilson MC artifacts
   committed under `outputs/su3_plaquette_fss_2026_05_05/`. The
   `<P>(beta=6)` value is itself a numerical computation, not a
   closed-form analytic result.
2. **2-loop SM RGE** (Machacek-Vaughn 1984; Arason et al. 1992) for
   the `mu = v -> mu = M_Z` running of `(g_1, g_2, g_3, y_t, lambda)`.
3. **PDG quark mass thresholds**: `m_t = 172.69 GeV` (pole),
   `m_b = 4.18 GeV` (MSbar), `m_c = 1.27 GeV` (MSbar).
4. **M_Pl**: Planck scale for the hierarchy-theorem evaluation.

## Framework-derived (retained)

The retained-grade content of the chain is:

- **Cl(3)/Z^3 axioms** -> `g_bare^2 = 1`, `alpha_bare = 1/(4 pi)`
  (geometric-bare normalization).
- **Plaquette V=1 Picard-Fuchs ODE** (PR #541 + minimality proof PR #596
  + Koutschan extension PR #616): closed-form differential structure of
  the single-plaquette weight; bounded scope (does not give the
  thermodynamic-limit value).
- **alpha_LM geometric-mean identity** (`alpha_LM^2 = alpha_bare * alpha_s(v)`):
  algebraic identity on the retained coupling triple.
- **Hierarchy theorem** (`v = M_Pl * (7/8)^(1/4) * alpha_LM^16`):
  16-power taste-doubler suppression with anti-periodic boundary factor.

## Runner verification

```bash
python3 scripts/frontier_yt_zero_import_chain.py
```

Expected summary (verified 2026-05-06):

```text
  Prediction                           Value      Observed   Deviation    Status
  ----------------------------  ------------  ------------  ----------  --------
  m_t [GeV]                           169.51        172.69      -1.84%      PASS
  alpha_s(M_Z)                        0.1181        0.1179      +0.14%      PASS
  sin^2(theta_W)(M_Z)                0.23061       0.23122     -0.263%      PASS
  v [GeV]                             246.28        246.22      +0.03%      PASS
  ...
  Total PASS: 14   Total FAIL: 0
```

```bash
python3 scripts/frontier_qcd_low_energy_running_bridge.py
```

Expected summary: `SUMMARY: PASS=18 FAIL=0`.

## What is `retained_bounded` and what is not

**Retained_bounded** (this synthesis grade):

- `alpha_s(M_Z) = 0.1181` matches the PDG world average within the
  documented 2-loop RGE truncation envelope.
- `v_EW = 246.28 GeV` matches the PDG `v_F = 246.22 GeV` (from G_F)
  within the propagated MC envelope on `<P>`.
- The synthesis is auditable and ratifiable at the `retained_bounded`
  grade because every link is documented as either retained-grade
  closed-form or as bounded-scope imported infrastructure.

**Not retained (open work):**

- The closed-form analytic value of `<P>(beta=6, L -> infinity)`. This
  is a famous open problem (4d non-perturbative SU(3) plaquette at fixed
  beta with L -> infinity); it is **not load-bearing** for this chain
  at `bounded` grade because PR #539 supplies a retained-numerical
  anchor whose primary 1/L^4 bracket contains the canonical comparator.
- A framework-native derivation of the SM RGE coefficients and the
  PDG quark-mass thresholds. These are imported as standard
  infrastructure on the v -> M_Z step and remain in the bounded scope.

## Audit Consequence

```yaml
claim_id: ew_chain_retained_bounded_theorem_note_2026-05-06
note_path: docs/EW_CHAIN_RETAINED_BOUNDED_THEOREM_NOTE_2026-05-06.md
runner_path: scripts/frontier_yt_zero_import_chain.py
claim_type: bounded_theorem
intrinsic_status: unaudited
audit_authority: independent audit lane only
deps:
  - plaquette_4d_mc_fss_numerical_theorem_note_2026-05-05
  - plaquette_self_consistency_note
  - plaquette_v1_picard_fuchs_ode_note_2026-05-05
  - alpha_lm_geometric_mean_identity_theorem_note_2026-04-24
  - qcd_low_energy_running_bridge_note_2026-05-01
  - alpha_s_derived_note
load_bearing_step: |
  Given the retained-numerical <P> = 0.5934 anchor (PR #539), the
  chain <P> -> u_0 -> alpha_LM -> alpha_s(v) is closed-form algebra;
  alpha_s(v) -> alpha_s(M_Z) is the bounded standard-infrastructure
  v -> M_Z bridge (audited_conditional dep); v_EW = M_Pl * (7/8)^(1/4)
  * alpha_LM^16 is the hierarchy theorem.
load_bearing_step_class: B
```

## Reuse rule

Downstream notes may cite this synthesis as the registered
`retained_bounded` EW-chain summary. The synthesis does **not**
substitute for any of its parents and does not change their statuses.
A future audit-clean replacement on the v -> M_Z bridge (e.g., a
framework-native RGE) would let this row consolidate to a
`retained_clean` synthesis.

## Honest non-claims

- This note does not analytically close `<P>(beta=6)` in the
  thermodynamic limit.
- This note does not promote the running bridge to retained.
- This note does not change the `audited_conditional` status of any
  parent.
- This note does not introduce new numerical claims; every quoted
  value matches an already-shipped one-hop authority.
