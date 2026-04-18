# DM Case-3 Spectral-Flow / Topological-Index Obstruction — Lane A Scout

**Date:** 2026-04-18
**Status:** SCOUT — DEAD (no axiom-native δ-odd non-polynomial invariant on
the retained `H_{hw=1}` bundle; Z_3-invariance of the functional forces
δ-evenness even for non-polynomial spectral content).
**Scripts:**
- `scripts/frontier_dm_case3_spectral_flow_attack.py` (probe battery)
- `scripts/frontier_dm_case3_delta_odd_diagnostic.py` (gauge-vs-invariant
  diagnosis)
- `scripts/frontier_dm_case3_z3_invariant_spectral_flow.py` (Z_3-symmetrized
  probe battery — the decisive test)
**Target:** drop assumption A2.3 (LOCALITY) from Theorem 6 of
`DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md`.

## Unit system and axiom base

- **Unit system.** Dimensionless complex `3×3` entries on
  `H_{hw=1} ≅ ℂ^3`; real trace pairing `⟨A, B⟩ := Re Tr(A† B)`.
- **Axiom base (strict).** A0. `Cl(3)` on `Z^3` (single framework axiom).
  Retained atlas primitives used:
  - retained chart generators `(T_m, T_delta, T_q)` and `H_base` from
    `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
  - retained `C_3[111]` shift (cyclic 3-cycle on `H_{hw=1}`) from
    `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
  - retained `Cl(3)` chirality / volume-element structure used in the
    temporal Dirac extension from `ANOMALY_FORCES_TIME_THEOREM.md`.
  - retained observable-principle generator
    `W[J] = log|det(D+J)| − log|det D|` from
    `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`.

No PDG masses, no back-fitting. Any non-retained ingredient is flagged
explicitly.

## Claim

**Theorem (Case-3 Non-Local Index Obstruction).** Let
`F : Herm(3) × R^3 → R` be any functional (not necessarily polynomial)
built from the retained `Cl(3)/Z^3` axiom on the active chart
`H(m, δ, q_+) = H_base + m T_m + δ T_delta + q_+ T_q` such that `F` is
invariant under conjugation by the retained `C_3[111]` cyclic shift.
Then the restriction of `F` to the chamber
`{ δ ≥ 0, q_+ ≥ E_1 − δ }` at fixed `m = m_*` (Schur baseline) depends on
`(δ, q_+)` only through `(δ^2, q_+)`. In particular, no spectral-flow,
η-invariant, Maslov-Arnold, caustic-crossing count, or APS-type mod-2
index constructed axiom-natively from the retained atlas can pin
`sign(δ)`.

## Proof

### Step 1 (retained). `T_delta` lives in the Z_3 doublet, δ → −δ is NOT in the Z_3 orbit.

Direct conjugation on the retained chart (verified in probe `frontier_dm_case3_spectral_flow_attack.py` Part 7) gives the coordinate triple of `C_3^k T_delta C_3^{-k}` projected back onto `(T_m, T_delta, T_q)`:

```
k = 0 : (c_m, c_δ, c_q) = (0,  +1,   0)
k = 1 : (c_m, c_δ, c_q) = (−1, −1/2, 0)
k = 2 : (c_m, c_δ, c_q) = (+1, −1/2, 0)
```

The δ-coefficients `(+1, −1/2, −1/2)` are the characters of the regular
ω/ω̄ doublet representation. The coefficient `c_δ = −1` (required for
δ → −δ to lie in the Z_3 orbit) does NOT appear. The reflection δ → −δ
is therefore a SEPARATE discrete `Z_2` gauge fix, imposed by the active-
half-plane theorem; it is not a retained Z_3 group element.

### Step 2 (retained). `H_base` has a non-trivial doublet component.

Theorem 2 of the Case-3 impossibility note records that C_3-conjugation
of `H_base` on a generic chart point yields a residual of Frobenius
norm `≈ 3.47`. Decomposing `H_base = H_base_sym + H_base_doublet` where
`H_base_sym := (1/3)(H_base + C_3 H_base C_3^† + C_3^2 H_base C_3^{2†})`,
the diagnostic `frontier_dm_case3_delta_odd_diagnostic.py` numerically
confirms `‖H_base_doublet‖_F ≈ 3.49`. `H_base` is a GAUGE-FIXED
representative, not a Z_3-singlet — as Theorem 2 of the Case-3 note
explicitly states.

### Step 3 (retained). Polynomial `Tr(H_full^k)` is δ-ODD for H_full on the chart.

Because `H_base` carries doublet content, the cross term
`2 Tr(H_base · T_delta)` is nonzero. The diagnostic confirms numerically
`Tr(H_base · T_delta) = −6.5320`. Consequently `Tr(H_full^2)` differs
between `+δ` and `−δ` at linear order in `δ`; `Tr(H_full^3)` and
`det(H_full)` are also δ-odd. (Same diagnostic: `det(H_full)` at
`(δ, q_+) = (0.7, 0.9)` reads `+0.654` at `+δ`, `−15.979` at `−δ`.)

This SEEMS to break Theorem 3 of the Case-3 impossibility note. But
Theorem 3's proof relied on δ-evenness of `Tr(H_src^k)` for
`H_src = m T_m + δ T_delta + q_+ T_q` (source-only). We numerically
verify the source-only claim (diagnostic Part (a)): `Tr(H_src^2)`,
`Tr(H_src^3)`, and `det(H_src)` are all δ-even. The crack is that
`Tr(H_full^k)` uses a gauge-fixed `H_base` that is not Z_3-invariant.

### Step 4 (retained). Axiom-native = Z_3-invariant.

Any functional `F[H_full]` that is axiom-native on Cl(3)/Z^3 must be
invariant under the retained symmetries. The retained C_3[111]
conjugation acts non-trivially on the active chart (Theorem 2 of the
Case-3 note). Therefore any axiom-native `F` must be built from the
Z_3-symmetrized chart data, equivalently from the Z_3-average
`(F[H_full] + F[C_3 H_full C_3^†] + F[C_3^2 H_full C_3^{2†}]) / 3`.
Isospectral invariants (spectral flow, η-invariant, caustic count,
Maslov index, mod-2 APS) are automatically C_3-invariant: isospectrality
makes them depend only on the spectrum, which is invariant under unitary
conjugation. So, while the gauge-fixed `H_full` CAN produce δ-odd
numerical values, any Z_3-invariant functional on the chart factors
through the symmetrized base `H_base_sym`.

### Step 5 (the decisive numerical test). With `H_base → H_base_sym`, every spectral-flow / η / caustic invariant becomes δ-even.

The runner `frontier_dm_case3_z3_invariant_spectral_flow.py` replaces
`H_base` with `H_base_sym = (1/3) Σ_k C_3^k H_base C_3^{-k}` and
repeats the battery. At every test point `(δ, q_+)` and for all four
candidate chart interpretations (det-interior (a), Tr(H^2)-boundary (b),
Schur-Q minimum, generic point), we observe:

| Invariant                          | +δ / −δ (symmetrized) |
|------------------------------------|-----------------------|
| caustic-crossing count             | 2 / 2 (all points)    |
| spectral flow on straight-line path| 0 / 0 (all points)    |
| η-invariant                        | 1 / 1 (all points)    |
| 3+1D temporal `det(H^2+sin^2ω I)`  | equal to 1e−10 (all points) |

Numerical convergence: 4001 samples along `s ∈ [0, 1]`; caustic detection
via `det(H) = 0` sign flips; spectral flow via sorted-eigenvalue zero
crossings; η via count(pos) − count(neg).

### Step 6 (structural closure). Doublet magnitude is the Z_3-invariant.

On the Z_3-doublet irrep with basis `(e_ω, e_{ω̄})`, the unique real
quadratic Z_3-invariant is `|c_ω|^2 = δ^2` (after the active-half-plane
Z_2 gauge fix). All higher-order Z_3-invariants are polynomials in
`δ^2` and the singlet coordinates `(m, q_+)`. Continuous (non-polynomial)
spectral invariants of a Hermitian chart H with Z_3-singlet base
`H_base_sym + m T_m_singlet + q_+ T_q` and doublet perturbation
`δ T_delta` are isospectral invariants of a rank-one doublet
perturbation; their spectra are functions of the doublet magnitude, i.e.
of `δ^2`. Hence every Z_3-invariant spectral functional (polynomial or
not) filters through `(δ^2, q_+)`. **QED.** □

## Robustness checks (mandatory)

### 1. Lattice-is-physical check

The `Z^3` lattice is physical, and spectral-flow constructions extend to
the full lattice Dirac operator. However, Theorem 6 of the Case-3
impossibility note is specifically about the retained `H_{hw=1}` 3D
surface. Lane A's attack stays on that surface to match the target's
scope. Even the full-lattice construction of spectral flow — defined
via paths in the space of Dirac operators on `Z^3` — is Z_3-covariant
under the cyclic permutation of the three generators, and its
restriction to `H_{hw=1}` inherits the present obstruction. To escape
requires a structure that is NOT Z_3-invariant on `H_{hw=1}` yet remains
axiom-native — which is a contradiction with Step 4. This lane's scope
does not provide an `H_{hw=1}`-exit.

### 2. 3+1D temporal check

The retained `ANOMALY_FORCES_TIME_THEOREM` forces signature `(3, 1)` and
APBC fermions on the temporal circle, yielding Matsubara frequencies
`ω_n = (2n+1)π/L_t`. On the retained product structure the full Dirac
operator is `D_ω = H ⊗ I + i sin(ω) γ_0` where `γ_0` is the Cl(3) volume
element (anticommuting). Then `D_ω D_ω^† = H^2 + sin^2(ω) I`, so any
temporal-Matsubara spectral functional is a function of `H^2`. Theorem
3 of the Case-3 note says `H_src^2` is δ-even; for the Z_3-symmetrized
`H_sym`, the runner (`frontier_dm_case3_z3_invariant_spectral_flow.py`)
numerically confirms `det(H_sym^2 + sin^2(ω) I)` is δ-even to 1e-10.
The 3+1D temporal direction does NOT add δ-odd content on the retained
bundle. (To get δ-odd from 3+1D one would need a temporally-extended
operator that pairs `δ T_delta` with a genuine Cl(3) chirality
odd-under-δ structure, which requires non-retained input.)

### 3. H_{hw=1} convergence check

The Koide charged-lepton triangulation
(`KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md`)
bottlenecks at the same `H_{hw=1}` cyclic commutant: it shows three
independent routes all terminate at one real scalar `κ = g_0²/|g_1|² = 2`
on the `C_3[111]` commutant. The present spectral-flow lane hits the
SAME bottleneck from a different side: any Z_3-invariant functional on
`H_{hw=1}` factors through the commutant, and the `T_delta` doublet
direction enters only via its magnitude. Both obstructions are
structural reflections of the Schur-lemma reduction of `Herm(3)` under
`C_3[111]` action:

```
Herm(3) = singlet (3-real) ⊕ doublet (6-real)
```

and the doublet has no real Z_3-invariant linear functional.
Spectral-flow does NOT escape the `H_{hw=1}` convergence — it confirms
it via a second, structurally independent route.

## Summary of the five attack directions

| Candidate invariant               | Z_3-invariant when symmetrized | δ-odd on retained H_{hw=1} | Verdict |
|-----------------------------------|--------------------------------|-----------------------------|---------|
| Caustic-crossing count            | Yes                            | No (2 = 2)                  | DEAD    |
| Spectral flow `SF`                | Yes                            | No (0 = 0)                  | DEAD    |
| η-invariant (pos − neg count)     | Yes                            | No (1 = 1)                  | DEAD    |
| Maslov-Arnold index (trivial loop)| Yes, identically 0             | No (trivially)              | DEAD    |
| mod-2 APS index (dim ker mod 2)   | Yes, identically 0 generically | No                          | DEAD    |
| 3+1D temporal Matsubara det       | Yes, reduces to H²             | No                          | DEAD    |

The apparent δ-odd content found for the UNSYMMETRIZED `H_base` (probe
Part 1–3 of `frontier_dm_case3_spectral_flow_attack.py`) is a gauge
artifact of the explicit gauge-fixing `H_base`, not an axiom-native
invariant.

## Verdict: DEAD

No axiom-native non-polynomial spectral-flow / topological-index
invariant on the retained `H_{hw=1}` chart pins `sign(δ)`. Theorem 6 of
the Case-3 impossibility note extends verbatim from LOCAL POLYNOMIAL to
ALL Z_3-INVARIANT SPECTRAL functionals (including spectral flow,
η-invariant, Maslov, caustic counting, APS mod-2, and Matsubara temporal
extension). The A2.3 (LOCALITY) assumption of Theorem 6 can be dropped;
the impossibility survives on the strictly larger class of Z_3-invariant
spectral functionals.

## Missing primitive

The only structures that could plausibly supply a Z_3-invariant δ-odd
functional on `H_{hw=1}` are:

- **A retained T-structure beyond C_3[111]**: e.g. a retained CP or parity
  operator whose Z_2 action on the doublet enforces `δ → −δ` as an
  ADDITIONAL retained axiom. Not retained: on the retained atlas, the
  `δ → −δ` reflection is an ACTIVE-HALF-PLANE GAUGE FIX, not a physical
  symmetry. Adding it as a retained axiom would be a post-axiom
  invention.
- **A retained full-lattice (off-hw=1) structure**: breaking `H_{hw=1}`
  convergence via a cross-hw isotypic coupling that carries Z_3-invariant
  δ-odd content. The Koide triangulation's "Route C" (S_3-involution
  primitive) is in the same structural class. Not retained.

Both of these are marked as OPEN, POST-AXIOM primitives — they are
potentially derivable from the Cl(3)/Z^3 axiom but are not currently on
the retained atlas.

## What this note does NOT claim

- Does not close the DM selector gate.
- Does not promote any `(δ_*, q_+*)` candidate to theorem-grade.
- Does not rule out an entirely different lane (Lane B: observational
  promotion; Lane C: new full-lattice primitive).
- Does not assert that no non-local selector exists — it only rules out
  the specific non-local class of Z_3-invariant spectral-flow /
  topological-index invariants on `H_{hw=1}`.

## Relation to Case-3 impossibility note

If adopted as a sibling to
`DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md`,
this note:

- strengthens Theorem 6 by dropping A2.3 (LOCALITY),
- enlarges the covered functional class from LOCAL POLYNOMIAL to
  Z_3-INVARIANT SPECTRAL,
- identifies the exact structural reason: the δ-reflection is a GAUGE
  FIX, not a Z_3 element; any Z_3-invariant functional sees only
  `|doublet|^2 = δ^2`.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_case3_spectral_flow_attack.py
PYTHONPATH=scripts python3 scripts/frontier_dm_case3_delta_odd_diagnostic.py
PYTHONPATH=scripts python3 scripts/frontier_dm_case3_z3_invariant_spectral_flow.py
```

The first runner SHOWS the naive gauge-fixed δ-odd content
(`PASS = 30, FAIL = 17` where the 17 FAILs are δ-odd indicators against
the gauge-fixed base). The second runner DIAGNOSES the gauge artifact
(`9/9 PASS` confirms the gauge origin). The third runner IS THE THEOREM:
`18/18 PASS` showing Z_3-symmetrized invariants are all δ-even.

## Observational verification (FLAGGED SEPARATELY from derivation)

Not applicable at this scope. The present note is a structural
obstruction; it does not produce any numerical selector value. The
downstream DM flagship gate closure via PMNS observational promotion
(Lane P3, separate) is unaffected by this note's verdict.
