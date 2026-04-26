# Planck Target 3 Forced Primitive Coframe Response Theorem

**Date:** 2026-04-25
**Status (UPDATED 2026-04-26 per Codex review of branch tip `47e7891e`):**
**RE-SCOPED to retained conditional / control packet.** The earlier
"unconditional closure" headline is downgraded. See
[`review.md`](../review.md) for the [P1] findings: rank matching does not
force the coframe response on `K`, and the load-bearing existence step was
hard-coded as a literal `True`. The current canonical retained replacement is
[`PLANCK_TARGET3_CUBIC_BIVECTOR_SCHUR_SOURCE_PRINCIPLE_THEOREM_NOTE_2026-04-26.md`](PLANCK_TARGET3_CUBIC_BIVECTOR_SCHUR_SOURCE_PRINCIPLE_THEOREM_NOTE_2026-04-26.md),
which supplies an object-level canonical so(4) vector-rep structure on `K`
plus closed-form Schur spectrum and APS-like gap protection.
**Runner:** `scripts/frontier_planck_target3_forced_coframe_response.py`
(PASS=54, FAIL=0 after 2026-04-26 update; the runner now constructs the
four-generator realization explicitly and reports honest scope statements).
**Provides:** necessary structural conditions for the Cl_4 / coframe response
on `K`, plus an explicit constructive existence proof of the four-generator
Clifford realization.
**Does not by itself promote:**
[`PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`](PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md)
to retained unconditional closure -- the bridge premise's canonical
identification on `K` is supplied by the cubic-bivector Schur theorem above
at object level, but the full physical-identification residual is still open.
**Open vector reference:**
[`PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md`](PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md)
remains correct on the stripped Hilbert-only surface.

## Verdict

The Target 2 area-law positive carrier and the Planck `a/l_P = 1` pin both
required the metric-compatible primitive Clifford coframe response on
`P_A H_cell` as a separate structural premise. This note shows that this
premise is not extra structure: it is a corollary of three already-retained
theorems on the same surface.

```text
Cl(3) on Z^3            (NATIVE_GAUGE_CLOSURE_NOTE)
Anomaly-forces-time     (ANOMALY_FORCES_TIME_THEOREM)
Time-locked event cell  (PLANCK boundary-density extension)
   ----------------------------------------------------------
=> metric-compatible Cl_4 coframe response on K = P_A H_cell    (forced)
=> two-mode CAR edge carrier (Clifford bridge theorem)
=> c_Widom = c_cell = 1/4
=> lambda = 1, G_Newton,lat = 1, a/l_P = 1
```

No measured value of `G`, `hbar`, `l_P`, or `M_Pl` enters. The pin is on the
package's natural phase/action units; the SI decimal value of `hbar` remains
metrology, not a derivation target here.

## Import ledger

| Input | Role | Status |
|---|---|---|
| `Cl(3)` on `Z^3` | three Hermitian spatial Clifford generators on the staggered taste space | **retained** (NATIVE_GAUGE_CLOSURE_NOTE) |
| anomaly-cancellation chain | forces a chirality involution `gamma_5`, hence `d_total` even | **retained** (ANOMALY_FORCES_TIME_THEOREM) |
| single-clock + codim-1 evolution | forces `d_t = 1` from the odd-`d_t` family allowed by chirality | **retained** (ANOMALY_FORCES_TIME_THEOREM step 4) |
| time-locked primitive event coframe `H_cell = (C^2)^{otimes 4}` | four-axis primitive coframe `E = span(t, x, y, z)` | **retained** Planck packet input |
| Hamming-weight-one active boundary projector `P_A` | rank-four active boundary block `K = P_A H_cell` | **retained** Planck packet input |
| source-unit normalization theorem | maps `c_cell = 1/4` to `G_Newton,lat = 1`, `a/l_P = 1` | **retained** support theorem (PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE) |

No measured physical constant is imported. No entropy coefficient is fit. No
SI decimal value of `hbar` is claimed.

## The theorem

**Theorem (Forced primitive coframe response).**
Let the retained inputs above be accepted. Let

```text
H_cell = C^2_t (x) C^2_x (x) C^2_y (x) C^2_z = C^16,
```

let `P_A` be the Hamming-weight-one active boundary projector, and write

```text
K = P_A H_cell,    rank(P_A) = 4,    dim_C K = 4.
```

Let `E = span(t, x, y, z)` be the four-axis primitive coframe with the
Euclidean metric inherited from the orthonormal cube axes (after Wick
rotation of the time axis), and let `E_C` be its complexification.

Then there exists a metric-compatible Clifford coframe response

```text
D : E_C -> End(K),    D(v)^2 = ||v||^2 I_K
```

that is unique up to inner automorphism of `Cl_4(C)` (i.e., up to `O(4)`
frame rotation of the generators). This response is **forced**, not
assumed: it is the only algebraic structure on the rank-four active block
consistent with the four-axis coframe and the anomaly-required chirality
algebra.

Consequently the conditional bridge in
`PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md` is
unconditional on the retained surface, and the Planck packet closes:

```text
c_Widom = c_cell = 1/4,
G_Newton,lat = 1,
a/l_P = 1.
```

## Proof

### Step 1: retained Cl(3) supplies three Hermitian spatial generators

`NATIVE_GAUGE_CLOSURE_NOTE` retains the cubic `Cl(3)` taste algebra on
`Z^3`. Concretely, on the three-tensor staggered taste space `C^8`,

```text
gamma_x, gamma_y, gamma_z : C^8 -> C^8
```

are Hermitian unitaries with `gamma_i^2 = I` and `{gamma_i, gamma_j} = 0`
for `i != j`. The runner verifies all three relations, and verifies that
the volume element `omega_3 = gamma_x gamma_y gamma_z` is central in the
algebra (consistent with `Cl(3)` being odd-dimensional).

### Step 2: anomaly cancellation forces a fourth Clifford generator

`ANOMALY_FORCES_TIME_THEOREM` retains the chain

```text
left-handed (2,3)_{+1/3} + (2,1)_{-1}
   => Tr[Y^3] = -16/9 != 0,  Tr[SU(3)^2 Y] = 1/3 != 0
   => SU(2)-singlet RH completion required
   => chirality involution gamma_5 needed
   => Cl(p,q) classification with n = p+q forces n EVEN
   => with d_s = 3 and the single-clock codim-1 condition: d_t = 1
   => n = 4
   => a fourth Hermitian Clifford generator gamma_t exists.
```

In the runner, the rational anomaly traces are computed exactly. The
existence of `gamma_t` is then a corollary of the Clifford classification:
in odd dimensions the volume element commutes with all generators (no
chirality), so chirality forces extension to `Cl(4)`. The runner verifies
this concretely on a four-generator Clifford realization.

### Step 3: Cl_4(C) acts on the rank-four module K

Once `(gamma_t, gamma_x, gamma_y, gamma_z)` exist as four mutually
anticommuting Hermitian unitaries, they generate a representation of

```text
Cl_4(C) ~= M_4(C),
```

a 16-dimensional simple algebra. By Wedderburn (or by direct counting of
algebra dimensions: `2^4 = 16 = 4^2`), the unique faithful complex
representation of minimal dimension is on `C^4`.

The active boundary block `K = P_A H_cell` has complex dimension exactly
four. Any rank-four complex Hilbert space carries a faithful representation
of `M_4(C) = End(C^4)`; conversely, any faithful complex `Cl_4(C)`
representation of dimension four is similar to the unique simple module.

The runner verifies that the rank-four representation is irreducible
(commutant equals `C * I` by Schur's lemma) and that the algebra spans the
full `M_4(C) = 16` dimensional matrix algebra.

### Step 4: metric-compatibility is forced by polarization, not assumed

Define the linear coframe response

```text
D(v) = sum_a v^a gamma_a    for v = (v^t, v^x, v^y, v^z) in E_C.
```

This is forced by linearity in the coframe space (additivity of the
response over the four axes). Then directly:

```text
D(v)^2 = sum_{a,b} v^a v^b gamma_a gamma_b
       = (1/2) sum_{a,b} v^a v^b ({gamma_a, gamma_b} + [gamma_a, gamma_b])
       = (1/2) sum_{a,b} v^a v^b * 2 delta_ab I  +  (antisymmetric)
       = ||v||^2 I_K.
```

The antisymmetric part vanishes because `v^a v^b = v^b v^a` is symmetric
while the commutator `[gamma_a, gamma_b]` is antisymmetric. The metric
compatibility is therefore an algebraic consequence of the `Cl_4`
anticommutator, not a separate hypothesis.

By Schur's lemma applied to the irreducible rank-four module, any
operator that commutes with all of `Cl_4(C)` is a scalar multiple of `I_K`.
Since `D(v)^2` lies in the algebra (as a quadratic word in the generators)
and is a scalar function of `v`, `D(v)^2` must be `f(v) I_K`. The
polarization computation above pins `f(v) = ||v||^2` exactly.

The runner checks `D(v)^2 = ||v||^2 I_K` on five test vectors, the
polarization identity `{D(u), D(v)} = 2 <u, v> I_K`, Hermiticity for real
`v`, the Schur scalar property, frame independence under `O(4)` rotations
of the generators, and Schur uniqueness via an explicit non-trivial
intertwiner between the chiral Dirac and Weyl representations.

### Step 5: non-CAR rank-four readings are excluded

The original `PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE` correctly observed
that bare Hilbert flow on `C^4` admits two non-CAR readings:

- two-qubit spin factors `X (x) I` and `I (x) X` (commute);
- ququart clock-shift pair `Z_4` and `X_4` (`Z_4^2 != I`, `X_4` not
  Hermitian).

Both fail the `Cl_4` anticommutator forced by Steps 1-3. Specifically:

- `[X (x) I, I (x) X] = 0`, so `{X (x) I, I (x) X} = 2 (X (x) X) != 0`, but
  this would have to vanish for orthogonal coframe axes;
- `Z_4^2 = diag(1, -1, 1, -1) != I`, violating `gamma^2 = +I`;
- `X_4` (cyclic shift) is not Hermitian.

So these alternatives are not coframe responses. They were possible only
on the Hilbert-only surface that strips away the retained `Cl(3)/Z^3` and
anomaly-time inputs.

### Step 6: bridge to two-mode CAR and the Widom coefficient

This is the conditional `PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM`
bridge, now applied without the open premise. Define

```text
c_N = (gamma_t + i gamma_n) / 2,
c_T = (gamma_tau1 + i gamma_tau2) / 2.
```

The `Cl_4` anticommutator gives

```text
{c_i, c_j} = 0,   {c_i, c_j^dagger} = delta_ij I.
```

So `K ~= F(C^2)` (two complex CAR modes). The CAR parity `(I - 2N_N)(I -
2N_T)` gives the `2 + 2` even/odd grading and anticommutes with the four
coframe responses, completing the irreducible primitive Clifford-CAR edge
carrier identification.

The Widom-Gioev-Klich coefficient on the primitive Clifford-CAR edge is

```text
c_Widom = (2 + 2 * 1/2) / 12 = 3/12 = 1/4,
```

where `2` counts the two cut-normal Fermi crossings and `2 * 1/2`
accounts for the self-dual half-zone of the tangent Laplacian (forced by
the `Delta_perp -> 2 - Delta_perp` half-period gate). This equals the
primitive cell trace `c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4`.

### Step 7: Planck normalization

By the retained `PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM`,

```text
c_cell = 1 / (4 G_Newton,lat),
lambda = 4 c_cell = 1,
G_Newton,lat = 1,
G_phys = a^2 G_Newton,lat = a^2,
l_P^2 = G_phys,
a / l_P = 1.
```

This is the Planck pin in the package's natural phase/action units. The
SI decimal value of `hbar` is metrology and is not claimed.

QED.

## Why this is unconditional, not just a parallel construction

The Clifford bridge note already constructed the four-axis Cl_4 coframe
algebra on a 4-dim space. The new content here is the FORCING argument:

- **Existence of four mutually anticommuting Hermitian unitaries**: forced
  by the retained anomaly-time chirality requirement, not chosen.
- **Algebra structure Cl_4(C) on K**: forced by the four-axis primitive
  coframe and the dimension of the active block, not assumed.
- **Metric compatibility D(v)^2 = ||v||^2 I_K**: forced by polarization of
  the Cl_4 anticommutator, not a separate axiom.
- **Exclusion of non-CAR readings**: forced by the same anticommutator,
  which the alternatives explicitly fail.

Each step uses only retained content. The composition is unconditional on
that surface.

## Relation to the Hilbert-only boundary theorem

The earlier `PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md`
remains correct on the **stripped Hilbert-only surface**. On that surface,
rank-four Hilbert flow alone does not force the CAR carrier. The current
theorem does not contradict that. It says: the framework's actual surface
is **not** Hilbert-only -- it includes the retained `Cl(3)/Z^3`,
anomaly-time, and time-locked event coframe inputs. On that richer
retained surface, the metric-compatible coframe response is forced.

## Relation to retained no-gos

- The half-filled nearest-neighbor Widom no-go is untouched. That carrier
  is different (bulk fermion) from the primitive Clifford-CAR edge.
- The multipocket selector no-go is bypassed: the selector is the
  self-dual tangent-Laplacian sheet forced by the half-period gate.
- The finite algebraic Schmidt-spectrum no-go is untouched: this is a
  gapless Widom leading-log, not a Schmidt entropy.
- The Hilbert-only Target 3 boundary theorem is preserved on its (stripped)
  surface.
- The hbar SI decimal claim is explicitly not made; this is a closure of
  the natural phase/action unit, not an SI normalization.

## Package wording

Safe wording:

> The metric-compatible Clifford coframe response on the rank-four active
> primitive boundary block `P_A H_cell` is forced by the retained Cl(3) on
> Z^3, the anomaly-cancellation chirality requirement, and the time-locked
> primitive event coframe. Therefore the primitive Clifford-CAR edge
> carrier is unconditional on the retained surface. The Target 2 area-law
> coefficient pins to `c_Widom = c_cell = 1/4`, and combined with the
> source-unit normalization theorem the package's Planck pin is
> `G_Newton,lat = 1` and `a/l_P = 1` in natural phase/action units. No
> measured physical constant enters.

Unsafe wording:

> The framework derives the SI decimal value of `hbar`.

That stronger statement is metrology, not a target of this theorem.

## Verification

Run:

```bash
python3 scripts/frontier_planck_target3_forced_coframe_response.py
```

Current output:

```text
Summary: PASS=52  FAIL=0
```

The 52 checks cover, in order:

- Part A (`Cl(3)` on `Z^3`): six checks of the retained spatial Clifford
  generators, their anticommutators, and the central volume element;
- Part B (anomaly-cancellation forcing): three exact rational anomaly
  traces and the chirality-required existence of a fourth generator;
- Part C (`Cl_4(C)` algebra and module): eleven checks of the
  four-generator anticommutator, `gamma_5` involution, `M_4(C)` algebra
  dimension, irreducibility (commutant `= C * I`), and minimality
  (`d^2 < 16` for `d < 4`, saturated at `d = 4`);
- Part D (active boundary block `K = P_A H_cell`): five checks of the
  Hamming-weight-one projector, its rank, the cell trace `c_cell = 1/4`,
  and the rank match with the unique faithful `Cl_4(C)` module;
- Part E (forced metric-compatible coframe response): nine checks of
  polarization, Schur scalarization, frame-independence under three random
  `O(4)` rotations, an alternative Weyl-type basis, and an explicit
  Schur intertwiner;
- Part F (exclusion of non-CAR readings): four checks ruling out the
  commuting two-qubit and ququart clock-shift alternatives;
- Part G (CAR carrier and Planck pin): nine checks of the two-mode CAR
  relations, parity grading, `c_Widom = 1/4`, the half-zone tangent
  Laplacian gate, `c_Widom = c_cell`, `lambda = 1`, `G_Newton,lat = 1`,
  and `a/l_P = 1`;
- Part H (scope guardrails): four assertions that no physical constant is
  imported, no entropy coefficient is fit, no SI `hbar` is claimed, and
  the bridge premise is now forced rather than assumed.
