# Lane 3 Route Portfolio

**Updated:** 2026-04-28T07:30:44Z

Scores use the physics-loop dramatic-step rubric: claim-state upgrade,
import retirement, review-blocker closure, artifactability, novelty, hard
residual pressure, and overclaim risk.

| Route | Type | Claim-state potential | Import-retirement potential | Artifactability in block 01 | Hard-residual pressure | Risk | Decision |
|---|---|---:|---:|---:|---:|---:|---|
| 3C-Q: quark direct Ward-free generation-matrix boundary | exact no-go / boundary theorem | 2 | 2 | 3 | 2 | low | execute first |
| 3B-R2: route-2 endpoint readout `beta_E/alpha_E = 21/4` stretch | constructive theorem / exact runner | 3 | 3 | 2 | 3 | medium | next if time remains |
| 3B-scalar shortlist provenance tightening | import-retirement audit / no-go | 1 | 2 | 3 | 1 | low | only after stretch |
| 3A local `5/6` NP proof framing | theorem target isolation | 2 | 3 | 1 | 2 | high | defer unless a sharp local theorem emerges |
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
