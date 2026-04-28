# Lane 3 Route Portfolio

**Updated:** 2026-04-28T09:44:28Z

Scores use the physics-loop dramatic-step rubric: claim-state upgrade,
import retirement, review-blocker closure, artifactability, novelty, hard
residual pressure, and overclaim risk.

| Route | Type | Claim-state potential | Import-retirement potential | Artifactability in block 01 | Hard-residual pressure | Risk | Decision |
|---|---|---:|---:|---:|---:|---:|---|
| 3C-Q: quark direct Ward-free generation-matrix boundary | exact no-go / boundary theorem | 2 | 2 | 3 | 2 | low | execute first |
| 3C-S3: generation-equivariant Ward degeneracy boundary | exact no-go / representation theorem | 2 | 3 | 3 | 3 | low | executed in block 05 |
| 3C-C3: oriented cycle Ward splitter normal form | exact support/boundary theorem | 2 | 2 | 3 | 3 | low | executed in block 06 |
| 3C-Circulant: inherited `C3` hierarchy source-law boundary | exact support/boundary theorem | 2 | 2 | 3 | 3 | low | executed in block 07 |
| 3C-A1-Source: A1 scalar to quark source-domain bridge inventory | exact current-bank no-go | 2 | 3 | 3 | 3 | low | executed in block 08 |
| 3C-P1-Readout: positive-parent square-root quark readout boundary | exact current-bank no-go | 2 | 3 | 3 | 3 | low | executed in block 09 |
| 3B-RPSR-MassBoundary: retained up-amplitude support vs mass readout | exact support/boundary theorem | 2 | 3 | 3 | 3 | low | executed in block 10 |
| 3B-RPSR-SingleScalarReadout: one scalar vs two up-type ratios | exact readout underdetermination theorem | 2 | 3 | 3 | 3 | low | executed in block 11 |
| 3B/3C-RPSR-C3-JointRank: RPSR scalar plus C3 carrier readout | exact joint rank-boundary theorem | 2 | 3 | 3 | 3 | low | executed in block 12 |
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

## Completed Route 6: 3C-S3

Question:

```text
Can the retained S_3 generation carrier itself stratify quark Ward
eigenvalues if the Ward operator is S_3-equivariant?
```

Minimal premise set `A_min`:

1. retained `hw=1` generation triplet;
2. exact `S_3` action and `hw=1 ~= A_1 + E` support theorem;
3. Hermitian Ward endomorphism on the generation triplet;
4. no observed quark masses, fitted Yukawa entries, hidden generation labels,
   or unannounced symmetry breaking.

Result:

```text
The S_3 commutant on the generation triplet has dimension 2 and form
W = a I + b J. Its eigenvalues are a+3b on A_1 and a on E with multiplicity
2. If the readout is diagonal in the generation basis, S_3 equivariance makes
it scalar. A C3-oriented example can split three eigenvalues, but only by
breaking reflection, which is exactly a new premise.
Runner TOTAL PASS=44 FAIL=0.
```

Honest target status:

This is an exact negative boundary for the carrier-only 3C route. It does not
preclude a future source/readout primitive; it proves that such a primitive is
load-bearing.

## Completed Route 7: 3C-C3

Question:

```text
What exact Ward normal form is available if the retained C3[111] cycle is
allowed as an oriented source/readout primitive on the hw=1 triplet?
```

Minimal premise set `A_min`:

1. retained `hw=1` generation triplet;
2. exact induced `C3[111]` cycle from the retained three-generation observable
   theorem;
3. Hermitian Ward endomorphism on the generation triplet;
4. no observed quark masses, fitted Yukawa entries, hidden endpoint selectors,
   or CKM mixing data treated as mass eigenvalues.

Result:

```text
The Hermitian C3-equivariant Ward normal form is
W(a,b,c) = a I + b(C+C^2) + c(C-C^2)/(i sqrt(3)).
The c coefficient is reflection-odd. Generic nonzero c splits the S3 E
doublet into cyclic Fourier channels, while c=0 collapses back to the S3
two-value spectrum. A C3-equivariant readout diagonal in the generation basis
is scalar. Runner TOTAL PASS=51 FAIL=0.
```

Honest target status:

This is exact support/boundary for the missing 3C source/readout primitive.
It retires direct promotion of oriented `C3` as mass closure: the coefficients
`a,b,c` and the physical readout theorem remain open.

## Completed Route 8: 3C-Circulant

Question:

```text
Can the inherited C3 circulant hierarchy mechanism, together with A1/P1
support from the Koide lane, be imported as retained quark Ward source law?
```

Minimal premise set `A_min`:

1. retained `hw=1` generation triplet;
2. exact induced `C3[111]` cycle;
3. exact Hermitian circulant family `H(a,q) = a I + q C + conjugate(q) C^2`;
4. inherited `C3` hierarchy and Koide-circulant support with A1/P1 classified
   as open support, not retained Lane 3 inputs;
5. no observed quark masses, fitted Yukawa entries, CKM mass inputs, charged
   lepton phase import, or hidden species selectors.

Result:

```text
The C3 Hermitian circulant family is a valid Fourier-basis hierarchy carrier.
Without A1/P1 or an equivalent source/readout theorem it is
three-real-dimensional and can fit any real generation spectrum. With A1/P1
it supplies Q=2/3 for an amplitude triple but still leaves scale, phase,
species assignment, and quark Yukawa readout open. Runner TOTAL PASS=43
FAIL=0.
```

Honest target status:

This is exact support/boundary for a future 3C source-law theorem. It retires
direct promotion of inherited `C3` circulant hierarchy support into retained
non-top quark masses.

## Completed Route 9: 3C-A1-Source

Question:

```text
Does the current repo support bank already contain a typed bridge from the
Koide A1 support scalar 1/2 to the physical quark C3 Ward source ratio
|q_quark|^2/a_quark^2 = 1/2?
```

Minimal premise set `A_min`:

1. retained `hw=1` generation triplet;
2. exact induced `C3[111]` cycle and Hermitian circulant algebra;
3. exact Koide/A1 support faces, including equal block power,
   `dim(spinor)/dim(Cl^+(3)) = 1/2`, and the `SU(2)_L` fundamental-weight
   match;
4. one-Higgs Yukawa gauge selection as a boundary;
5. no observed quark masses, fitted Yukawa entries, CKM mass inputs, or
   charged-lepton A1 physical bridge imported as species-universal.

Result:

```text
The A1 algebra is exact: |q|^2/a^2 = 1/2 is equivalent to Q=2/3 and
E_plus=E_perp on a C3 circulant carrier. Existing Koide support faces all hit
the scalar 1/2. But the current typed-edge inventory has no path from those
support faces to the physical quark C3 Ward source ratio. Adding exactly that
edge creates the desired path, so the edge is new theorem content rather than
latent support. Runner TOTAL PASS=50 FAIL=0.
```

Honest target status:

This is an exact current-bank no-go / support boundary. It sharpens the 3C A1
residual to a typed quark source-domain theorem, alternate source ratio, or a
P1/readout route that makes A1 unnecessary.

## Completed Route 10: 3C-P1-Readout

Question:

```text
Does the repo's exact positive-parent square-root dictionary already supply a
retained quark P1 readout theorem for eig(M_quark^(1/2))?
```

Minimal premise set `A_min`:

1. retained `hw=1` generation triplet;
2. exact induced `C3[111]` cycle and Hermitian circulant algebra;
3. exact finite-dimensional positive square-root theorem;
4. inherited Koide P1 square-root dictionary as support;
5. one-Higgs Yukawa gauge selection as a boundary;
6. no observed quark masses, fitted Yukawa entries, CKM mass inputs, charged
   lepton positive-parent import, or hidden quark parent/readout assumption.

Result:

```text
If a positive C3 parent M is supplied, M^(1/2) is positive, C3-covariant, and
has square-root eigenvalues. But for every positive amplitude triple there is
such a parent, so the dictionary is representational rather than predictive.
The current typed-edge inventory lacks both a physical quark positive parent
and a readout theorem identifying the square-root spectrum with quark Yukawa
amplitudes. Runner TOTAL PASS=54 FAIL=0.
```

Honest target status:

This is an exact current-bank no-go / support boundary. It sharpens P1 to a
physical quark parent theorem plus readout theorem, or an alternate readout
route that bypasses P1.

## Completed Route 11: 3B-RPSR-MassBoundary

Question:

```text
What exactly does the existing STRC/RPSR up-amplitude package retain, and
what remains missing before it becomes retained up-type mass-ratio closure?
```

Result:

```text
STRC/RPSR supplies exact retained support for a reduced up-sector amplitude:
a_u = sqrt(5/6) * (1 - 48/(49 sqrt(42))). The current bank has no typed
readout edge from this reduced amplitude to physical up-type Yukawa eigenvalue
ratios or absolute non-top masses. Runner TOTAL PASS=50 FAIL=0.
```

Honest target status:

This is constructive 3B support/boundary. It upgrades the loop's map of the
up-amplitude route while blocking direct promotion to retained `m_u` or `m_c`.

## Completed Route 12: 3B-RPSR-SingleScalarReadout

Question:

```text
Can the exact RPSR scalar plus top-scale normalization determine both
physical up-type ratios y_u/y_c and y_c/y_t without an independent readout
law?
```

Result:

```text
No. In the admissible scale-covariant power readout class
R_{p,q}(a_u) = (a_u^(p+q), a_u^q, 1), the same exact RPSR scalar supports a
continuum of ordered ratio pairs. The exponents p and q, or equivalent
readout functions plus generation-gap assignment, are extra theorem content.
Runner TOTAL PASS=80 FAIL=0.
```

Honest target status:

This is an exact readout underdetermination theorem. It does not weaken the
RPSR amplitude support; it sharpens the load-bearing residual to a derived
two-ratio readout law and top-compatible sector/scale bridge.

## Completed Route 13: 3B/3C-RPSR-C3-JointRank

Question:

```text
Does exact RPSR + exact C3 close the two-ratio up-type Yukawa readout without
adding a new source law for the C3 coefficients?
```

Result:

```text
No. The C3 normal form exactly represents the two-ratio surface, while RPSR
contributes one scalar. Product and middle-gap one-scalar identifications
each leave a continuum of C3-representable ordered ratio pairs. Runner
TOTAL PASS=87 FAIL=0.
```

Honest target status:

This is an exact joint rank-boundary theorem. It closes direct promotion of
RPSR+C3 carrier support into retained up-type ratios and sharpens the residual
to a C3 coefficient source law, physical Fourier-channel assignment,
two-ratio readout, and sector/scale bridge.
