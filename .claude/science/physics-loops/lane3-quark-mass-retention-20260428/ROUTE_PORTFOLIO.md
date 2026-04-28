# Lane 3 Route Portfolio

**Updated:** 2026-04-28T08:26:17Z

Scores use the physics-loop dramatic-step rubric: claim-state upgrade,
import retirement, review-blocker closure, artifactability, novelty, hard
residual pressure, and overclaim risk.

| Route | Type | Claim-state potential | Import-retirement potential | Artifactability in block 01 | Hard-residual pressure | Risk | Decision |
|---|---|---:|---:|---:|---:|---:|---|
| 3C-Q: quark direct Ward-free generation-matrix boundary | exact no-go / boundary theorem | 2 | 2 | 3 | 2 | low | execute first |
| 3B-R2: route-2 endpoint readout `beta_E/alpha_E = 21/4` stretch | constructive theorem / exact runner | 3 | 3 | 2 | 3 | medium | next if time remains |
| 3B-scalar shortlist provenance tightening | import-retirement audit / no-go | 1 | 2 | 3 | 1 | low | only after stretch |
| 3A local `5/6` scale-selection boundary | exact negative boundary / theorem target isolation | 2 | 3 | 3 | 3 | low | executed in block 04 |
| 3D absolute scale chain | downstream corollary | 3 | 2 | 1 | 0 | high | blocked until 3A/3B/3C move |
| Lane 1 pivot | handoff route | 1 | 1 | 2 | 0 | medium | only if Lane 3 produces actionable quark-mass handoff |

## Completed Route 1: 3C-Q

Question:

```text
Can retained one-Higgs gauge selection plus the top Ward template derive
generation-stratified quark Yukawa Ward identities for u, d, s, c, b?
```

Minimal premise set `A_min`:

1. retained SM one-Higgs Yukawa gauge-selection theorem;
2. retained top-channel Ward identity on `Q_L`;
3. retained three-generation structure;
4. retained CKM atlas as a mixing surface, not a mass input;
5. no observed quark masses, no fitted Yukawa matrices, no hidden generation
   selector.

Expected durable output:

- note: `docs/QUARK_GENERATION_STRATIFIED_WARD_FREE_MATRIX_NO_GO_NOTE_2026-04-28.md`;
- runner: `scripts/frontier_quark_generation_stratified_ward_free_matrix_no_go.py`;
- log: `logs/2026-04-28-quark-generation-stratified-ward-free-matrix-no-go.txt`.

Honest target:

This route is not expected to retain non-top masses. It should either expose a
usable theorem route for species-differentiated Ward identities or close a
direct but tempting route family negatively, making the next hard residual
sharper.

Result:

```text
Direct one-Higgs + top Ward + three-generation + CKM route closed negatively.
Runner TOTAL PASS=42 FAIL=0.
```

## Completed Route 2: 3B-R2

Question:

```text
Do the exact Route-2 carrier, endpoint algebra, and T-side candidates force
the missing E-channel readout entry beta_E/alpha_E = 21/4?
```

Minimal premise set `A_min`:

1. exact Route-2 restricted carrier columns;
2. exact endpoint algebra `q_E = 1 + rho_E/6`;
3. conditional T-side candidates `rho_T = -1` and `alpha_T/alpha_E = -2`;
4. no observed masses, no CKM/J target fitting, and no nearest-rational
   selection from the live E endpoint as a theorem step.

Result:

```text
Minimal naturality leaves rho_E free. The value 21/4 is equivalent to granting
the E-center ratio gamma_T(center)/gamma_E(center) = -8/9, or to using live
endpoint-distance evidence as a bounded selector. Runner TOTAL PASS=28 FAIL=0.
```

## Completed Route 3: 3B-R2-Rconn

Question:

```text
Can the retained SU(3) color projection R_conn = 8/9 supply the missing
Route-2 E-center ratio gamma_T(center)/gamma_E(center) = -8/9?
```

Minimal premise set `A_min`:

1. exact Route-2 restricted carrier columns and endpoint algebra;
2. conditional T-side candidates `rho_T = -1` and `alpha_T/alpha_E = -2`;
3. retained `N_c=3` and `R_conn = (N_c^2 - 1)/N_c^2 = 8/9`;
4. no observed quark masses, fitted Yukawa entries, CKM/J target fitting, or
   nearest-live-endpoint selector.

Result:

```text
The conditional algebra is exact: imposing gamma_T(center)/gamma_E(center)
= -R_conn gives q_E=15/8 and rho_E=21/4. The source-domain identification is
not present in the current Route-2 carrier, so the result is a conditional
bridge target and import boundary, not retained up-type scalar closure.
Runner TOTAL PASS=26 FAIL=0.
```

## Stuck Fan-Out Frames

If no route passes after 3C-Q, emulate these frames sequentially before stop:

1. gauge/operator frame: classify all one-Higgs quark Yukawa monomials and
   check whether generation indices are gauge-selected;
2. Ward-normalization frame: ask what the top `sqrt(6)` normalization can and
   cannot distinguish inside `Q_L`;
3. CKM/singular-value frame: separate unitary mixing data from Yukawa singular
   values;
4. endpoint/readout frame: test whether route-2 quark endpoint data supplies a
   generation/source scalar law rather than another comparator fit;
5. down-type NP frame: isolate whether `5/6` has a local non-perturbative
   theorem target within existing retained primitives.

Block 02 satisfied the endpoint/readout frame and partially satisfied the
atlas-reuse/source-domain frame by checking the retained `R_conn` coincidence
without promoting it.

## Completed Route 4: 3B-R2-Source

Question:

```text
Does the current exact/retained support bank already contain a typed
source-domain bridge from R_conn to the Route-2 E/T center endpoint ratio?
```

Minimal premise set `A_min`:

1. exact Route-2 support carrier `K_R`;
2. exact restricted endpoint columns and endpoint algebra;
3. conditional T-side candidates `rho_T = -1` and `alpha_T/alpha_E = -2`;
4. retained `N_c = 3` and `R_conn = 8/9`;
5. finite typed-edge inventory over the current Route-2 and SU(3) support
   bank.

Result:

```text
No current typed edge connects su3_R_conn_8_9 to route2_rho_E_21_4.
Adding exactly the missing source-domain bridge creates the path and forces
rho_E = 21/4. Therefore the bridge is new theorem content, not latent
support in the current bank. Runner TOTAL PASS=33 FAIL=0.
```

Honest target status:

This is an exact current-bank no-go / exact negative boundary. It sharpens
the next 3B route to a genuinely new source-domain theorem or an alternate
up-type scalar/readout primitive. It does not retain `m_u` or `m_c`.

## Completed Route 5: 3A-Scale

Question:

```text
Can exact C_F - T_F = 5/6 plus the strong threshold-local match promote the
down-type 5/6 bridge without an independent scale-selection theorem?
```

Minimal premise set `A_min`:

1. exact `SU(3)` group theory `C_F = 4/3`, `T_F = 1/2`;
2. retained CKM atlas value `|V_cb| = alpha_s(v)/sqrt(6)`;
3. inherited comparator values and one-loop transport from the existing
   `5/6` support note;
4. no observed masses as derivation inputs, no fitted Yukawa entries, and no
   hidden scale selector.

Result:

```text
The threshold-local comparator gives p_self = 0.832890..., close to 5/6.
The common-scale comparator gives p_same = 0.803802..., and the same
prediction misses that surface by +14.98%. Therefore exact C_F - T_F = 5/6
is not a scale-selection theorem. Retained 3A still requires NP
exponentiation plus scale selection or RG-covariant transport.
Runner TOTAL PASS=34 FAIL=0.
```

Honest target status:

This is an exact negative boundary / theorem-target isolation for 3A. It
preserves the down-type bridge as strong bounded support and blocks direct
promotion to retained down-type mass ratios.
