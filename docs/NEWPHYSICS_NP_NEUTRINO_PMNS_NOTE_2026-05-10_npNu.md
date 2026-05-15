# New-Physics Probe — Neutrino PMNS Circulant Ansatz (npNu)

**Date:** 2026-05-10
**Type:** bounded_theorem (new-physics probe; numerical hypothesis test)
**Claim type:** bounded_theorem
**Status:** review-loop source-note proposal — sector-specific
`C_3[111]`-equivariant Hermitian circulant ansatz tested numerically on the
neutrino sector. No new positive theorem. No promotion of any retained
neutrino observable. Explicit named admissions for the BAE-analog amplitude
ratio `rho_nu`, the phase `delta_nu`, the `sqrt(m)` identification, and the
non-circulant tilt required to repair the `U_nu = DFT_3` over-mixing.
**Authority role:** source-note proposal — audit verdict and downstream
status set only by the independent audit lane.
**Loop:** newphysics-np-neutrino-pmns-20260510
**Primary runner:** [`scripts/cl3_np_neutrino_pmns_circulant_2026_05_10_npNu.py`](../scripts/cl3_np_neutrino_pmns_circulant_2026_05_10_npNu.py)
**Cache:** [`logs/runner-cache/cl3_np_neutrino_pmns_circulant_2026_05_10_npNu.txt`](../logs/runner-cache/cl3_np_neutrino_pmns_circulant_2026_05_10_npNu.txt)
**Runner status:** `PASS = 17, FAIL = 0`

## Authority disclaimer

This is a source-note proposal in the review-loop source-only policy. It
contributes (a) a single theorem note in `docs/`, (b) a paired runner in
`scripts/`, and (c) the cached runner output in `logs/runner-cache/`. No
output packet, lane promotion, or synthesis is included. Pipeline-derived
status (`audit_status`, `effective_status`) is generated only after the
independent audit lane reviews the claim, dependency chain, and runner.

## Naming-collision warning

This note uses the rename established in
[BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md):
the Brannen-Rivero amplitude-ratio constraint `|b|^2 / a^2 = 1/2` is
called **"Brannen Amplitude Equipartition (BAE)"** here. Legacy references
to "A1-condition" or "Brannen-Rivero A1" all alias to BAE.

## Question

The charged-lepton sector admits a `C_3[111]`-equivariant Hermitian
circulant ansatz on the retained `hw=1` triplet,

```text
H_e  =  a_e I  +  b_e C  +  b_e^conj C^2,                              (1)
```

with the BAE admission

```text
rho_e := |b_e|^2 / a_e^2  =  1/2,                                       (2)
```

yielding Koide `Q_e = 2/3` exactly under the `sqrt(m)` identification and
matching PDG charged-lepton masses to `<10^{-3}` at `delta_e = 2/9 rad`.
This circulant ansatz is a **bounded admission** on the charged-lepton
lane (see
[KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md);
the BAE selection principle remains open per the 17-probe campaign
[KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)).

The neutrino sector is currently retained at

| Retained input | Value | Source |
|---|---|---|
| `m_3` | `5.058 x 10^{-2} eV` | [DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md](DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md) |
| `Dm^2_31` | `2.539 x 10^{-3} eV^2` | same |
| normal ordering `m_1 < m_2 < m_3` | retained | [NEUTRINO_MASS_DERIVED_NOTE.md](NEUTRINO_MASS_DERIVED_NOTE.md) §"What Phase 4 retains" |
| `Sigma m_nu > 50.58 meV` | strict floor | [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md) Theorem 1 |
| `m_beta <= 50.58 meV` | PMNS-free | same, Theorem 2 |
| `m_betabeta <= 50.58 meV` | phase-free | same, Theorem 3 |
| `0 < Dm^2_21 < Dm^2_31` | structural | same, Theorem 4 |
| `U_e = I` on `hw=1` | retained | [CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md](CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md) |
| `theta_23` upper-octant prediction `s_23^2 >= 0.541` | conditional/support | [PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md](PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md) |

The **solar gap** `Dm^2_21` (~`7.41 x 10^{-5} eV^2`) is OPEN: the diagonal
benchmark over-predicts it (`~2.1 x 10^{-3}` vs observed `7.41 x 10^{-5}`),
and the PMNS-from-H-diagonalization pinning is a bounded P3 package, not a
sole-axiom theorem.

> **Question (Probe npNu).** Does the parallel circulant ansatz
> `H_nu = a_nu I + b_nu C + b_nu^conj C^2` admit a sector-specific
> `(rho_nu, delta_nu)` pair that reproduces, simultaneously,
> (i) the observed mass-squared splittings `Dm^2_21 / Dm^2_31`,
> (ii) a Koide-like relation `Q_nu` analogous to the charged-lepton
> `Q_e = 2/3` at BAE,
> (iii) the PMNS angles `(theta_12, theta_13, theta_23)` via
> `U_PMNS = U_e^dagger U_nu`,
> using only retained content and explicit named admissions?

We test four hypotheses:

| Hypothesis | `rho_nu` | `delta_nu` |
|---|---|---|
| **H_A** (BAE-inherited) | `1/2` (BAE) | `2/9` (charged-lepton phase) |
| **H_B** (Brannen neutrino conjecture) | `1/2` (BAE) | `2/9 + pi/12` |
| **H_C** (BAE, free delta) | `1/2` (BAE) | free, fit to `Dm^2_21 / Dm^2_31` |
| **H_D** (free rho, free delta) | free | free, fit numerically |

## Answer

**Bounded probe.** The circulant ansatz **alone** does NOT close the
neutrino sector: it produces

- a sector-independent `Q = 2/3` at BAE (so the test
  "Q_nu different from Q_e" forces `rho_nu != 1/2`, an explicit BAE
  violation in the neutrino sector that is not derived);

- a `U_nu = DFT_3` (trimaximal) PMNS pattern that over-predicts
  `sin^2 theta_13` by a factor `~15` (the retained PMNS package's
  non-circulant affine `H(m, delta, q_+)` tilt is therefore
  STRUCTURALLY REQUIRED on the neutrino side);

- a 1-parameter curve in the `(rho_nu, delta_nu)` plane along which
  `Dm^2_21 / Dm^2_31` matches the observed value, but no
  sole-axiom selection of a point on this curve.

The probe surfaces four open derivation targets (Section "Open targets"
below). It is consistent with all retained neutrino bounds; it does
not promote any of them.

## Section A — Pattern-A circulant kinematics (no admission)

This section uses only the Pattern-A theorem
[KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md).

For any Hermitian circulant on the `C_3[111]` orbit,

```text
H  =  a I  +  b C  +  b^conj C^2,         a in R, b in C,             (3)
```

the eigenvalues take the closed form

```text
lambda_k  =  a + 2 |b| cos(delta + 2 pi k / 3),   k = 0, 1, 2,        (4)
```

where `delta = arg(b)`. Define `rho := |b|^2 / a^2 >= 0`. Then
`2|b| = sqrt(2 rho) * a * 2`, so equivalently

```text
lambda_k  =  a (1 + sqrt(2 rho) * cos(delta + 2 pi k / 3)).            (5)
```

**Two algebraic identities** (verified in runner Part 1; symbolic in the
Pattern-A bridge note):

```text
sum_k lambda_k       =  3 a,                                          (I1)
sum_k lambda_k^2     =  3 a^2 + 6 |b|^2  =  3 a^2 (1 + 2 rho).        (I2)
```

This uses `sum_k cos(delta + 2 pi k / 3) = 0` (zero-sum of three
cosines spaced by `2 pi / 3`) and
`sum_k cos^2(delta + 2 pi k / 3) = 3 / 2`.

## Section B — Brannen Koide `Q` is sector-independent at BAE

Under the **Brannen amplitude identification** `lambda_k = sqrt(m_k)`
(open primitive `P1` per
[KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)),
the Koide ratio becomes

```text
Q  =  (sum m_k) / (sum sqrt(m_k))^2  =  (sum lambda_k^2) / (sum lambda_k)^2.    (B1)
```

Substituting (I1, I2),

```text
Q  =  3 a^2 (1 + 2 rho) / (3 a)^2  =  (1 + 2 rho) / 3.                  (B2)
```

So `Q` depends **only on `rho`** (not on `delta`). Special cases:

| `rho` | `Q` | Comment |
|---|---|---|
| `0` (`b = 0`) | `1/3` | uniform spectrum, all `lambda_k = a`; degenerate masses |
| `1/2` (BAE) | `2/3` | charged-lepton retained value |
| `1` | `1` | not physical |

**Verification (runner Part 2).** A 24-point grid on `delta in [0, 2 pi)` at
`rho = 1/2` confirms `Q = 2/3` to `4.4 x 10^{-16}` accuracy uniformly.

### B1 — Foot-Brannen neutrino Koide `Q_nu ~ 1/3` requires `rho_nu = 0`

Literature reports neutrino Koide attempts at `Q_nu ~ 1/3` (Foot, Brannen).
By (B2), `Q_nu = 1/3` requires `rho_nu = 0`, i.e. `b_nu = 0`. This forces
`H_nu = a_nu I`, which gives degenerate masses `m_1 = m_2 = m_3 = a_nu^2`.
**This is empirically wrong** — observed neutrino masses have splittings
`Dm^2_21 ~ 7 x 10^{-5}` and `Dm^2_31 ~ 2.5 x 10^{-3}`. So the literature
"Q_nu ~ 1/3" framing is at best a coarse classification; it cannot be
sharp without splittings.

### B2 — A neutrino-specific Koide-like relation must be in `Q(rho_nu)` form

If one wants a Koide-like relation on neutrinos that is non-trivial
(`rho_nu != 0`) and distinct from `Q_e = 2/3` (`rho_nu != 1/2`), the
relation reduces to

```text
Q_nu  =  (1 + 2 rho_nu) / 3,        rho_nu in (0, 1/2) U (1/2, ...).    (B3)
```

We surface this as **bounded prediction (BP1)**: any sector-specific Koide
analog for neutrinos has `Q_nu` algebraically tied to `rho_nu` by (B3); it
is not a free relation. Observational determination of `rho_nu` would fix
`Q_nu` and vice versa.

**Note on the rho-vs-Q duality.** (B3) shows the Brannen
`Q`-as-an-observable framing is **equivalent** (under BAE-style
identification) to specifying the amplitude ratio `rho`. The two are
NOT independent observables in this framing.

## Section C — Hypothesis H_B: Brannen neutrino phase `delta_nu = 2/9 + pi/12`

Brannen's neutrino conjecture (literature) sets

```text
delta_nu  =  2/9 + pi/12  approx  0.484022 rad.                        (C1)
```

Under BAE (`rho_nu = 1/2`) the eigenvalues are

```text
lambda_k  =  a_nu (1 + sqrt(2) cos(delta_nu + 2 pi k / 3)).            (C2)
```

**Runner Part 3 result.** At `a_nu = 1`:

| `k` | `delta_nu + 2 pi k / 3` (rad) | `lambda_k` |
|---|---|---|
| `0` | `0.484022` | `+2.251764` |
| `1` | `2.578418` | `-0.195808` |
| `2` | `4.672815` | `+0.944044` |

The negative `lambda_1` is structurally important. Under the Brannen
amplitude convention `lambda = sqrt(m)`, this maps to a small-but-nonzero
`m_1`. The ratio `|lambda_min| / |lambda_max| ~ 0.087` corresponds to
`m_1^2 / m_3^2 ~ 0.0076`.

Computing `Dm^2 = lambda^2 - lambda_{lightest}^2`:

```text
Dm^2_21 / Dm^2_31 (H_B) = 0.1695   (PDG comparator: 0.0295).            (C3)
```

`H_B` overshoots the observed solar / atmospheric ratio by a factor `~6`.
At the **pure** Brannen literature phase `delta_nu = pi/12 = 0.2618 rad`
(not the `2/9 + pi/12` literature target), one eigenvalue is **exactly
zero** at BAE (KOIDE_A1_PROBE_OPERATOR_CLASS_BOUNDED_NOTE_2026-05-08
Observation 4). That gives an exactly massless lightest neutrino, also
not observed.

**Verdict on H_B:** does not match observed splittings. The literature
target `delta_nu = 2/9 + pi/12` is not derived from `Cl(3)/Z^3`
content (open admission **DELTA_NU_PI12**); we report this as a tested
phenomenological target that fails the numerical check, not as a
no-go.

## Section D — Hypothesis H_C: BAE, free `delta_nu`

At BAE, the only remaining parameter is `delta_nu`. Sweep
`delta in [0, 2 pi)` and find the `delta` minimizing
`|Dm^2_21 / Dm^2_31 - 0.0295|` (4001-point grid).

**Runner Part 4 result.**

```text
delta_best        =  1.977633 rad  =  113.31 deg
Dm^2_21 / Dm^2_31 =  0.029508       (target 0.029463, relative err 0.15%)
Sorted (m_k^2)    = (0.0240, 0.1939, 5.7820)  (units of a_nu^4)
```

H_C admits a delta that reproduces the observed splitting ratio.

**However:**
- `delta_best = 1.978 rad` is not at a structurally distinguished angle.
- It is NOT close to the literature `2/9 + pi/12 = 0.484` (distance `1.49`).
- It is NOT close to `2/9 = 0.222` (the charged-lepton value) or to
  `pi/12 = 0.262`.
- Modulo the `2 pi / 3` fundamental period (BAE-circulant cosine
  structure is `Z_3`-invariant up to spectral relabeling), the best delta
  remains at `1.978 rad`, also off any standard reference.

H_C therefore demonstrates **existence** of a BAE+phase fit to the
splitting ratio, but the phase is **not derived** — it is fit to data.

## Section E — Hypothesis H_D: free `(rho_nu, delta_nu)`

Sweep `rho in [0.05, 2.0]` and `delta in [0, 2 pi / 3)` (one fundamental
period) at `200 x 200` resolution, recording points where
`|Dm^2_21 / Dm^2_31 - 0.0295| / 0.0295 < 0.05`.

**Runner Part 5 result.** **710 grid points** in the `40000`-point sweep
match to `<5 %` relative. The matching locus is a 1-dimensional curve
in the plane; example samples:

| `rho_nu` | `delta_nu` (deg) | `Dm^2_21 / Dm^2_31` |
|---|---|---|
| `0.0794` | `2.41` | `0.030179` |
| `0.0794` | `117.59` | `0.030179` |
| `0.0892` | `2.41` | `0.029268` |
| ... | ... | ... |

The doubling at `delta` and `120 deg - delta` reflects the `Z_3` cyclic
symmetry of the cosine triple. The matching curve has small `rho_nu`
(approaching `0` from above) at small `delta`, with increasing `rho` as
`delta` moves into the second `2 pi / 3` arc.

**Pinning a unique `(rho_nu, delta_nu)` requires an additional sole-axiom
selection principle.** No such principle is derived.

## Section F — Best-fit numerics (Section E continued)

Running the fit at fixed `rho_nu` and `delta_nu` to reproduce
`Dm^2_21 / Dm^2_31 = 7.41 x 10^{-5} / 2.539 x 10^{-3}` exactly,
then rescaling so `Dm^2_31` matches the retained value:

**Runner Part 7 result.**

```text
rho_nu     =  0.4636
delta_nu   =  0.105778 rad  =  6.06 deg
Dm^2_21    =  7.4204e-05 eV^2     (PDG comparator 7.41e-05; rel err 0.14%)
m_1        =  4.26e-03 eV
m_2        =  9.61e-03 eV
m_3        =  5.06e-02 eV         (retained 5.058e-02; rel err 0.02%)
Sigma m_nu =  6.44e-02 eV         (above retained floor 50.58 meV)
```

The grid-best `rho_nu = 0.4636` lies near but not at BAE (`0.5`); the
distance `|rho_best - 1/2| = 0.036` is small but nonzero. The fact that
`rho_nu` is **near** but **not at** BAE is suggestive: a sole-axiom
selection principle returning `rho_nu = 1/2` exactly would push the
best-fit `delta_nu` somewhere on the H_C curve (Section D).

A higher-resolution / `scipy.optimize` minimization would sharpen these
to `rel err ~ 10^{-6}`; we leave the analytical pin as an open question.

## Section G — PMNS angles from pure-circulant `U_nu`

Under the retained `U_e = I` chain (Z_3 trichotomy on charged leptons,
[CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md](CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md)),

```text
U_PMNS  =  U_e^dagger U_nu  =  U_nu.                                  (G1)
```

The diagonalizing unitary of the Hermitian circulant `H_nu` is the
3-point discrete Fourier matrix

```text
[DFT_3]_{i k}  =  (1 / sqrt(3)) omega^{i k},   omega = e^{2 pi i / 3},  (G2)
```

INDEPENDENT of `(a_nu, b_nu)`. Therefore the pure-circulant PMNS prediction
is

```text
|U_PMNS|^2  =  |DFT_3|^2  =  (1/3) J_3,                                (G3)
```

where `J_3` is the all-ones `3 x 3` matrix.

**Runner Part 6 result.**

```text
sin^2 theta_13 (DFT_3) = |U_{e3}|^2                  =  1/3  =  0.333  (PDG ~0.022)
sin^2 theta_12 (DFT_3) = |U_{e2}|^2 / (1 - |U_{e3}|^2)
                       = (1/3) / (2/3)               =  1/2  =  0.500  (PDG ~0.307)
sin^2 theta_23 (DFT_3) = |U_{mu 3}|^2 / (1 - |U_{e3}|^2)
                       = (1/3) / (2/3)               =  1/2  =  0.500  (PDG ~0.545)
```

`sin^2 theta_13 = 1/3` is **15 x larger** than the observed `0.022`.
This is the well-known "trimaximal mixing" problem: pure-circulant
`U_nu = DFT_3` cannot accommodate the small `theta_13`.

### G1 — The retained PMNS package's non-circulant tilt is structurally required

The retained PMNS-as-`f(H)` map
([PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md](PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md))
uses an **affine** Hermitian `H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`,
which is NOT a pure `C_3[111]`-equivariant circulant. The affine tilts
`T_m, T_delta, T_q` break the `C_3[111]` symmetry that forces
`U_nu = DFT_3`, allowing `sin^2 theta_13` to deviate from `1/3`.

Our probe surfaces this as **(P3)**: the non-circulant tilt is not an
optional feature; it is **structurally required** to reproduce the
observed `sin^2 theta_13`. The pure-circulant ansatz fails the
PMNS-angle test by construction.

This is consistent with the retained PMNS package being a bounded P3
construction with an explicit non-circulant tilt, rather than a pure
circulant ansatz.

## Section H — Cross-check against retained bounds

The probe's best-fit point (Section F) satisfies all retained inequality
bounds:

| Bound | Retained | Probe at best-fit | Verdict |
|---|---|---|---|
| `m_3` | `5.058e-2 eV` | `5.057e-2 eV` (rel err 0.023%) | within 5% (PASS) |
| `Sigma m_nu` | `> 50.58 meV` | `64.44 meV` | PASS |
| `Dm^2_21 < Dm^2_31` | structural | `7.4e-5 < 2.5e-3` | PASS |
| `m_k >= 0` | structural | all positive | PASS |

(Runner Part 9.)

## Open targets surfaced

The probe surfaces four open derivation targets, each tractable:

1. **`rho_nu` selection principle.** What sole-axiom mechanism (analog
   of the BAE selection principle that remains open for `rho_e = 1/2`)
   selects `rho_nu` for the neutrino sector? Candidates flagged but
   not derived: sector-dependent Wilson-source amplitude factor,
   seesaw-induced renormalization of the circulant amplitudes, or a
   different `C_3[111]`-equivariant operator class for neutrinos.

2. **`delta_nu` derivation.** What sole-axiom mechanism selects the
   neutrino phase? The literature target `delta_nu = 2/9 + pi/12` fails
   the splitting-ratio test (Section C); the H_C best-fit
   `delta_nu ~ 1.978 rad` is not at a structurally distinguished
   angle; `pi/12` alone gives a massless lightest neutrino. Open.

3. **`sqrt(m)` identification primitive.** The Brannen amplitude
   identification `lambda_k = sqrt(m_k)` (P1 of
   `KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE`) is admitted; for
   neutrinos this is even less constrained than for charged leptons
   (charged-lepton mass operator is non-Majorana; neutrino sector
   may want a different positive parent).

4. **`U_nu = DFT_3` over-mixing fix.** The pure-circulant ansatz
   gives trimaximal `sin^2 theta_13 = 1/3` against observed `0.022`.
   The retained PMNS package's non-circulant affine tilt is
   structurally required. The relation between the circulant ansatz
   here and the retained P3 affine package is itself an open
   compatibility question.

## What this probe does NOT claim

This source-note explicitly does **not** claim:

1. A retained derivation of `Dm^2_21`, `delta_CP`, or PMNS angles
   from `Cl(3) on Z^3`. The fits in Sections D, E, F use admissions
   on `(rho_nu, delta_nu)` that are not derived.
2. A retained Koide-like relation for neutrinos. By (B3), any such
   relation is algebraically tied to `rho_nu`; without a
   `rho_nu`-selection principle, the relation has no independent
   content.
3. A promotion of the retained PMNS P3 package
   (`PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION`) to sole-axiom
   closure. The P3 package's open inputs (baseline-connected component,
   observational-hierarchy pairing) are not addressed here.
4. A new axiom. The probe respects A1 (`Cl(3)`) + A2 (`Z^3`) as the
   only mathematical axioms (per
   [MINIMAL_AXIOMS_2026-05-03.md](MINIMAL_AXIOMS_2026-05-03.md)).
5. A modification of the retained
   [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md)
   inequality bounds (`Sigma m_nu > 50.58 meV`, `m_beta <= 50.58 meV`,
   `m_betabeta <= 50.58 meV`, `0 < Dm^2_21 < Dm^2_31`). All four are
   verified by the probe.

## What this probe DOES contribute

1. **Algebraic identity (B3):** `Q_nu = (1 + 2 rho_nu) / 3` — a Brannen-
   Koide formula relating the neutrino Koide observable directly to
   the amplitude ratio. Establishes that `Q_nu` is **not** an
   independent observable from `rho_nu`. Foot-Brannen `Q_nu ~ 1/3`
   maps to `rho_nu = 0` (degenerate spectrum), which fails observed
   splittings.

2. **Verdict on H_B (literature `2/9 + pi/12`):** numerical failure on
   the splitting ratio (`r = 0.17` vs observed `0.029`). The
   `Q_brannen = 2/3` identity holds (since `rho = 1/2` is retained
   for H_B), but the splittings are wrong.

3. **Verdict on H_C (BAE + free delta):** existence of `delta` matching
   the splitting ratio, but `delta_nu ~ 1.978 rad` is not at any
   structurally distinguished angle. **Phase is fit to data, not
   derived.**

4. **Verdict on H_D (free rho, free delta):** a 1-dimensional matching
   curve in the `(rho, delta)` plane exists; pinning requires
   additional structure.

5. **PMNS angle obstruction (P3):** pure-circulant `U_nu = DFT_3` gives
   `sin^2 theta_13 = 1/3`, a factor `15` overshoot. The retained
   PMNS-as-`f(H)` package's non-circulant affine tilt is therefore
   **structurally required**, not optional.

6. **Cross-check (P9):** the probe's best-fit point satisfies all
   retained inequality bounds.

## Cited dependencies

This source-note depends on the following retained / theorem-grade
inputs:

- [KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md](KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09.md)
  — Pattern-A circulant / character identities (T1, T2, T3); used in
  Section A.
- [KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
  — circulant / character bridge; BAE admission; charged-lepton
  retained `rho_e = 1/2`; comparator for neutrino sector.
- [DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md](DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md)
  — retained `m_3 = 5.058e-2 eV`, `Dm^2_31 = 2.539e-3 eV^2`.
- [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md)
  — retained inequality bounds; cross-check.
- [CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md](CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md)
  — `U_e = I` on `hw=1`.
- [BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md](BRANNEN_AMPLITUDE_EQUIPARTITION_BAE_RENAME_META_NOTE_2026-05-09.md)
  — name convention BAE.
- [MINIMAL_AXIOMS_2026-05-03.md](MINIMAL_AXIOMS_2026-05-03.md) —
  axiom set A1 + A2.

## Staggered-Dirac realization derivation target

Per [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md), this
note depends on the **staggered-Dirac realization derivation target**,
which is currently an open gate. The note's load-bearing claim defines
or relies on the `hw=1` triplet, charged-lepton sector content, neutrino
sector content, and the PMNS observable surface — all of which depend
on the staggered-Dirac realization derivation target listed in
`MINIMAL_AXIOMS_2026-05-03.md`. This admission is inherited from the
parent retained inputs; no new fermionic admission is introduced by this
probe.

## Forbidden-imports check

- **No PDG observed values consumed as DERIVATION INPUT.** PDG values
  used only as comparators in clearly-marked sections (Sections C-F).
  The retained chain produces `m_3`, `Dm^2_31`, normal ordering, and
  the `Sigma m_nu` floor independently of PDG comparators.
- **No lattice MC empirical measurements.** None used.
- **No fitted matching coefficients in the predictive chain.** The
  `(rho_nu, delta_nu)` admissions are explicit and named; they are
  not retained derivations.
- **No new axioms.** Probe respects A1 (`Cl(3)`) + A2 (`Z^3`) only.
- **Open derivation gates noted explicitly:** BAE-analog `rho_nu`
  selection, `delta_nu` derivation, `sqrt(m)` neutrino positive
  parent, `U_nu = DFT_3` over-mixing fix.

## Falsifiability

1. **Observed `theta_13` in the trimaximal regime.** A measurement
   of `sin^2 theta_13` consistent with `1/3` (currently excluded by
   `> 100 sigma`) would weaken the requirement for a non-circulant
   tilt. Already observationally falsified.

2. **Foot-Brannen `Q_nu = 1/3` literature claim.** By (B3) this
   requires `rho_nu = 0`, hence degenerate masses, hence
   `Dm^2_21 = Dm^2_31 = 0`. Observationally falsified.

3. **A sole-axiom derivation of `rho_nu`** would either reproduce
   the H_D best-fit `~0.464` (consistency with this probe) or
   produce a different value (contradicting one of the splitting
   ratio, `m_3`, or the `Sigma m_nu` floor — which would falsify
   the derivation chain, not the probe).

4. **A sole-axiom derivation of `delta_nu`** at any specific angle
   other than the H_C best-fit `~1.978 rad` (modulo `2 pi / 3`)
   would conflict with the observed splitting ratio under BAE; this
   provides a sharp target for any future selection theorem.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/cl3_np_neutrino_pmns_circulant_2026_05_10_npNu.py
```

Expected: `PASS = 17, FAIL = 0`.

## Cross-references

- Charged-lepton retained Koide chain:
  [`docs/CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md`](CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md).
- Neutrino retained status:
  [`docs/NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md`](NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md).
- PMNS theta_23 conditional/support prediction:
  [`docs/PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md`](PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md).
- 17-probe campaign on BAE selection:
  [`docs/KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md).
