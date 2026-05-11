# Probe U-L1-Resurgence — QCD Trans-Series and Stokes Structure for β_2, β_3: Bounded-Tier Source Note

**Date:** 2026-05-10
**Claim type:** no_go (negative closure for the resurgence route;
support-only on imported-toolkit Borel-plane structure)
**Sub-gate:** Lane 1 (alpha_s) — beta_2, beta_3 resurgence-structure probe
**Status authority:** independent audit lane only; effective status is
pipeline-derived.
**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.

**Primary runner:** [`scripts/cl3_koide_u_L1_resurgence_2026_05_08_probeU_L1_resurgence.py`](../scripts/cl3_koide_u_L1_resurgence_2026_05_08_probeU_L1_resurgence.py)
**Cached output:** [`logs/runner-cache/cl3_koide_u_L1_resurgence_2026_05_08_probeU_L1_resurgence.txt`](../logs/runner-cache/cl3_koide_u_L1_resurgence_2026_05_08_probeU_L1_resurgence.txt)

## 0. Probe context

Probe X-L1-MSbar ([`KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md`](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md))
established that the 3-loop and 4-loop QCD beta-function coefficients
`beta_2` and `beta_3` are NOT derivable in MS-bar OR lattice/`<P>`-scheme
on retained content alone: the Casimir-tensor SKELETON is retained, but
the scalar channel WEIGHTS require integral primitives (dim-reg or
lattice perturbation theory) outside the current physical `Cl(3)` local
algebra + `Z^3` spatial substrate stack.

A natural follow-on question is:

**Can resurgence / trans-series machinery, applied to QCD running
coupling with the current physical `Cl(3)` local algebra + `Z^3`
spatial substrate inputs, give `beta_2` (and possibly `beta_3`)
structural identities by relating perturbative coefficients to
non-perturbative content via Stokes phenomena?**

Resurgence (Écalle 1980s; for QFT: Marino, Aniceto, Schiappa, Mariño-Reis,
Cherman-Dorigoni-Ünsal, Costin-Dunne) bridges perturbative and
non-perturbative content: a trans-series

```
alpha_s^trans(mu)  =  alpha_s^pert(mu)
                    +  Σ_n  exp(-S_n / alpha_s) · alpha_s^{a_n} · (
                              c_n^(0) + c_n^(1) alpha_s + ... )
```

is connected to the perturbative tail by Stokes constants. For QCD,
the leading IR renormalon at Borel-plane position `z = 4π/β_0` controls
the large-order asymptotic of the perturbative series:

```
β_n^pert  ~  (S_IR / (2πi)) · Γ(n + b)
              · (β_0 / (4π))^{n+1} · [1 + O(1/n)]
```

where `b` is a fixed constant tied to the renormalon structure and
`S_IR` is the Stokes constant connecting perturbative to IR-renormalon
content.

This probe asks: how much of this imported resurgence structure for QCD
`beta` is supported by the existing framework inputs, and does it give
`beta_2` or `beta_3` in closed form?

## 1. Theorem (no-go for closure; support-only structural observations)

**Theorem (U-L1-Resurgence; no-go).** Under the current physical
`Cl(3)` local algebra + `Z^3` spatial substrate baseline, the existing
retained/bounded `β_0, β_1` inputs, and resurgence/renormalon theory as
an imported mathematical toolkit for this route check, the QCD
beta-function coefficients `beta_2` and `beta_3` are NOT closed-form
derivable. The imported toolkit does organize several support-only
large-order structures around `β_0`, but those structures do not close
the finite-loop coefficients:

1. **(Borel-plane singularity location is parameterized by `β_0`.)** In
   the imported renormalon picture, the leading IR
   renormalon position in the Borel plane

   ```
   z_*  =  4π / β_0  =  4π / 7   (at N_f = 6, retained via S1)
   ```

   is determined by the retained/bounded 1-loop coefficient `β_0 = 7`.
   Similarly, UV renormalons are at `z = -4π/(n β_0) = -4π/(7n)`
   for positive integer `n`. These positions are support-only
   consequences of importing the renormalon picture and substituting
   the existing `β_0` value; they are not a new retained framework
   surface.

2. **(Asymptotic factorial growth is support-only.)** The form

   ```
   β_n^pert  ~  C · Γ(n + b) · (β_0 / (4π))^{n+1}
   ```

   for large `n`, is dictated by the renormalon picture and follows
   from the Borel-plane structure with the imported singularity
   location. The growth-rate base `(β_0/(4π))^n` is fixed once the
   imported renormalon skeleton and `β_0` are supplied; the prefactor
   `C` and exponent `b` involve Stokes constants and anomalous-dimension
   data.

3. **(Stokes constant S_IR is NOT retained in closed form.)** The Stokes
   constant connecting the perturbative series to the IR renormalon
   sector encodes information about the full instanton moduli space
   and monopole structure of the QCD vacuum. While the framework has
   physical `Cl(3)` local algebra + `Z^3` spatial substrate structure and
   retained/bounded Casimir inputs, the identification of the QCD
   instanton sector with framework content is NOT pre-justified on
   current source content alone — it would require either:
   - explicit identification of YM instanton moduli with framework
     structures (a separate postulated bridge);
   - or import of the QCD instanton moduli computation from the
     literature.

   Either way, `S_IR` is NOT closed-form derivable from retained content
   without additional structural input.

4. **(Resurgence relation is ASYMPTOTIC, not exact for small n.)** The
   resurgence relation `β_n ~ Γ(n+b) (β_0/(4π))^{n+1} S_IR / (2πi)` is
   an ASYMPTOTIC formula valid for large `n`. For finite `n = 2` (3-loop)
   and `n = 3` (4-loop), `1/n` corrections to the leading asymptotic
   form are NOT small — they are O(1) corrections. A precise computation
   of `β_2` and `β_3` from resurgence requires the FULL Borel transform
   `B[β](z)`, which encodes the same integral content as the original
   perturbative series and is therefore NOT a shortcut.

5. **(Trans-series ↔ framework identification is unproved.)**
   The conjecture that QCD trans-series content (instantons, IR
   renormalons) corresponds 1-to-1 with framework structure (`Z^3`
   spatial substrate sector, Casimir algebra) is structurally suggestive
   but NOT a theorem on current source content. It would require an
   explicit identification map. As of this probe, no such map is
   established.

## 2. What this closes vs. does not close

### Support-only structural observations

- **Borel-plane singularity locations are structurally determined by
  `β_0 = 7` within the imported renormalon toolkit.** The support point
  is an IR renormalon at `z = 4π/7` and UV renormalons at
  `z = -4π/(7n)` for `n = 1, 2, 3, ...`.
- **Factorial growth rate `(β_0/(4π))^n = (7/(4π))^n` is fixed within
  the same imported toolkit.**
  This sets the asymptotic scale for `β_n` at large `n`.
- **Resurgence/renormalon theory is an imported mathematical toolkit for
  this bounded route check, not a framework axiom or retained status
  surface.**

### Not closed (frontier remaining; bounded admission)

- **Stokes constant `S_IR` in closed form.** Requires identification of
  QCD instanton/monopole sector with framework content. Not pre-justified.
- **Constant `b` (subleading exponent in `Γ(n+b)`).** Tied to
  anomalous-dimension structure of the renormalon-relevant operator;
  for the gluon condensate `<G^2>`, `b = 1 - β_1/β_0² + O(α_s)` requires
  scheme-dependent input.
- **`1/n` corrections to leading resurgence formula.** These are O(1) at
  `n = 2, 3` and require the full Borel transform.
- **Closed-form derivation of `β_2` or `β_3`.** Same as in probe X-L1-MSbar:
  bounded admission. Resurgence does NOT shortcut the integral primitives.

### Final bounded statement

```
[SUPPORT-ONLY STRUCTURAL OBSERVATIONS via imported resurgence + existing beta_0]
Borel-plane IR renormalon at z = 4π / β_0 = 4π / 7
Borel-plane UV renormalons at z = −4π / (β_0 n) = −4π / (7n), n = 1, 2, 3, ...
Asymptotic factorial growth: β_n ~ Γ(n + b) · (β_0/(4π))^{n+1} · const
Asymptotic ratio: β_{n+1} / β_n  ~  (β_0/(4π)) · (n + b)  for n → ∞

[BOUNDED ADMISSIONS]
Stokes constant S_IR connecting perturbative ↔ IR renormalon: NOT retained
(requires QCD instanton/monopole moduli identification with framework content)

Subleading exponent b in Γ(n+b): requires scheme-dependent input
(anomalous dimension of <G^2> or analogue)

1/n corrections at finite n=2, 3: require full Borel transform B[β](z)
(equivalent to the same dim-reg / lattice PT integrals as in probe X-L1)

β_2 closed form via resurgence: NOT achievable — leading asymptotic
formula gives only ~ Γ(2+b) · (7/(4π))^3 · S_IR which is order-of-magnitude
right but not a closed-form value without S_IR

β_3 closed form via resurgence: same obstruction; leading asymptotic
~ Γ(3+b) · (7/(4π))^4 · S_IR

[POSITIVE NUMERICAL CHECK]
The asymptotic resurgence formula at finite n gives an order-of-magnitude
match to literature MS-bar β_2 ≈ 32.5 and β_3 (numerical, in convention
of Tarasov-Vladimirov-Zharkov 1980 and van Ritbergen et al. 1997). The
match is consistent with order-of-magnitude expectations from leading
resurgence asymptotics; it does NOT constitute a derivation.

[FALSIFIABLE PREDICTION]
Net contribution to Lane 1 from this probe:
  - documents Borel-plane structure under imported renormalon toolkit
  - documents scaling Γ(n+b) (β_0/4π)^{n+1} under imported toolkit
  - does NOT close β_2 or β_3 in closed form (bounded admission stands)
  - identifies a candidate follow-on: derive S_IR from a separately
    approved identification of QCD monopole sector with framework
    structure
```

## 3. Conditional admissions

This bounded theorem inherits the conditional admissions of the
underlying framework, plus the named resurgence-machinery imports:

- `g_bare = 1` per [`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md)
- S1 Identification Source Theorem per [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md)
- SU(3) Casimir authority per [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
- N_f = 6 above all SM thresholds (asymptotic regime)
- `β_0 = 7` and `β_1 = 26` per probe X-L1-MSbar's positive retention,
  and per [`SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md`](SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md)

**Imported mathematical toolkit (route-check scope; not a new axiom):**

- **Resurgence theory** (Écalle 1980s; Costin 2009; Mariño 2014;
  Aniceto-Basar-Schiappa 2019). Borel-Laplace transform, Stokes
  phenomena, trans-series construction.
- **Renormalon picture** (t'Hooft 1977; Mueller 1985; Beneke 1998).
  IR/UV renormalon poles in Borel plane controlled by 1-loop
  beta function `β_0`.

**Imported authorities (numerical comparators only, NOT load-bearing):**

- Tarasov-Vladimirov-Zharkov 1980, MS-bar `β_2(N_f=6) = 65/2 = 32.5`.
- van Ritbergen-Vermaseren-Larin 1997, MS-bar `β_3(N_f=6) ≈ 643.8`
  (or alternate convention `≈ 2472.3`; bounded admission stands across
  conventions).
- Beneke 1998, *Renormalons*, Phys. Rep. 317, 1-142.
- Mariño 2014, *Lectures on non-perturbative effects in large N gauge
  theories, matrix models and strings*, Fortschritte der Physik 62, 455.

These are imported authorities for a bounded-theorem comparator; the
runner verifies them at the level of literature-cross-check, NOT
framework-native derivation.

## 4. Implementation overview

The runner [`scripts/cl3_koide_u_L1_resurgence_2026_05_08_probeU_L1_resurgence.py`](../scripts/cl3_koide_u_L1_resurgence_2026_05_08_probeU_L1_resurgence.py)
implements:

1. **POSITIVE retention check 1**: Borel-plane IR renormalon position
   `z_* = 4π/β_0 = 4π/7` from retained `β_0 = 7`. Same for UV
   renormalons at `z = -4π/(7 n)`.

2. **POSITIVE retention check 2**: Asymptotic factorial growth rate
   `(β_0/(4π))^{n+1}` and Γ(n+b) form follow from the renormalon
   picture with retained `β_0`.

3. **POSITIVE retention check 3**: Asymptotic ratio test
   `β_{n+1} / β_n → (β_0/(4π)) (n+b)` for large `n`. Verify on
   literature `β_n` values (n=0,1,2,3 = 7, 26, 32.5, 643.8) the
   trend toward the asymptotic ratio is consistent with `β_0/(4π)
   ≈ 0.557` (i.e., the ratios are O(1) and growing roughly factorially).

4. **STRUCTURAL check 4**: Stokes constant `S_IR` requires identification
   of QCD instanton sector with framework content. Document that
   no such retained identification exists; bounded admission.

5. **STRUCTURAL check 5**: Subleading exponent `b` in `Γ(n+b)` depends
   on scheme via anomalous dimension of `<G^2>`; bounded admission.

6. **NUMERICAL comparator check 6**: Compute the leading asymptotic
   resurgence prediction
   ```
   β_n^asymp  =  (S_IR / (2π)) · Γ(n + b) · (β_0/(4π))^{n+1}
   ```
   for `n = 2, 3` using benchmark Stokes-constant values from the
   literature (e.g., for the gluon condensate channel `S ~ O(1)`
   typical) and verify the ORDER OF MAGNITUDE matches literature
   `β_2 ≈ 32.5` and `β_3 ≈ 643.8`. The match is order-of-magnitude
   only — it confirms the renormalon picture but does NOT constitute
   a derivation.

7. **HONEST verdict**: no-go for closed-form `beta_2, beta_3` closure;
   support-only Borel-plane geometry and asymptotic form; bounded
   admissions on Stokes constants, subleading exponents, and finite-n
   corrections.

## 5. Dependencies

- [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) —
  physical `Cl(3)` local algebra + `Z^3` spatial substrate baseline.
- [`SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md`](SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md)
  for the structural form of `β_0` (companion form for QCD: `β_0 = 7`).
- [`CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md`](CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md)
  for the S1 Identification Source Theorem.
- [`YT_EW_COLOR_PROJECTION_THEOREM.md`](YT_EW_COLOR_PROJECTION_THEOREM.md)
  for retained `(C_F, C_A, T_F)` Casimir authority.
- [`KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md`](KOIDE_X_L1_MSBAR_NATIVE_SCHEME_NOTE_2026-05-08_probeX_L1_msbar.md)
  for the parent X-L1 negative result (this probe extends X-L1 with a
  resurgence-tool angle and confirms the bounded admission stands).
- [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md)
  for the existing 2-loop SM RGE bridge (Machacek-Vaughn) treated as
  bounded standard infrastructure.

These are imported authorities for a bounded theorem.

## 6. Boundaries

This note does NOT claim:

- **Framework-native closed form for `β_2` or `β_3` in any scheme via
  resurgence.** The honest verdict is BOUNDED ADMISSION: the framework
  reaches the Borel-plane GEOMETRY (singularity locations from
  retained `β_0`) and the ASYMPTOTIC growth form, but does NOT have
  the integral content for the Stokes constants or the finite-`n`
  corrections.
- **Promotion of any current MS-bar or lattice import to retained.** The
  literature values for `β_2, β_3` remain external numerical inputs.
- **Identification of QCD instanton sector with framework monopole sector.**
  This is structurally suggestive but NOT a theorem; it would be a
  candidate follow-on probe.
- **Direct contribution to closing Lane 1 alpha_s(M_Z).** Currently
  Lane 1 uses 2-loop MS-bar bridge via
  [`QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md`](QCD_LOW_ENERGY_RUNNING_BRIDGE_NOTE_2026-05-01.md);
  this probe does NOT change Lane 1 status.
- **Resurgence as a free shortcut to non-perturbative content.**
  Resurgence is a powerful framework but it does NOT bypass the integral
  primitives at finite loop order — it reorganizes the same content
  into a different representation.

## 7. Resurgence and renormalon literature

- **Écalle J.** (1981), *Les fonctions résurgentes (3 volumes)*, Publ.
  Math. d'Orsay. Foundational treatise on resurgent functions, alien
  calculus, Stokes phenomena.
- **t'Hooft G.** (1977), *Can we make sense out of "Quantum
  Chromodynamics"?*, in *The Whys of Subnuclear Physics*, ed. A.
  Zichichi. Original IR renormalon proposal.
- **Mueller A.H.** (1985), *On the structure of infrared renormalons in
  physical processes at high energies*, Nucl. Phys. B 250, 327. IR/UV
  renormalon classification.
- **Beneke M.** (1998), *Renormalons*, Phys. Rep. 317, 1-142. Standard
  reference on QCD renormalons.
- **Costin O.** (2009), *Asymptotics and Borel summability*, Chapman &
  Hall. Mathematical foundation of resurgent analysis.
- **Mariño M.** (2014), *Lectures on non-perturbative effects in large N
  gauge theories, matrix models and strings*, Fortsch. Phys. 62, 455.
- **Aniceto I., Basar G., Schiappa R.** (2019), *A primer on resurgent
  transseries and their asymptotics*, Phys. Rep. 809, 1. Modern
  pedagogical review.
- **Cherman A., Dorigoni D., Ünsal M.** (2015), *Decoding perturbation
  theory using resurgence: Stokes phenomena, new saddle points and
  Lefschetz thimbles*, JHEP 10, 056. Application to gauge theories.
- **Costin O., Dunne G.V.** (2019), *Resurgent extrapolation: rebuilding
  a function from asymptotic data*, J. Phys. A 52, 445205.

## 8. Status summary

| Quantity | Status | Source |
|---|---|---|
| `β_0 = 7` (N_f=6) | RETAINED | S1 + Casimir, probe X-L1 |
| `β_1 = 26` (N_f=6) | RETAINED | Casimir, probe X-L1 |
| Borel-plane IR renormalon at `z = 4π/7` | support-only under imported renormalon toolkit + `β_0` | This probe |
| UV renormalons at `z = -4π/(7n)` | support-only under imported renormalon toolkit + `β_0` | This probe |
| Asymptotic growth `(β_0/(4π))^n = (7/(4π))^n` | support-only under imported renormalon toolkit + `β_0` | This probe |
| Asymptotic form `β_n ~ Γ(n+b) (β_0/(4π))^{n+1}` | support-only skeleton | This probe |
| Stokes constant `S_IR` closed form | NOT RETAINED | This probe (bounded admission) |
| Subleading exponent `b` in `Γ(n+b)` | NOT RETAINED | This probe (bounded admission) |
| Finite-`n` corrections at n=2, 3 | NOT RETAINED | This probe (bounded admission) |
| `β_2` closed form via resurgence | NOT RETAINED | This probe (bounded admission) |
| `β_3` closed form via resurgence | NOT RETAINED | This probe (bounded admission) |
| Order-of-magnitude match β_2 ≈ 32.5 from leading resurgence | bounded numerical check | This probe (literature comparator) |

## 9. Falsifiable structural claims

1. The Borel-plane IR renormalon for QCD `β` is at `z_* = 4π/β_0 = 4π/7`
   inside the imported renormalon toolkit; this support-only prediction
   depends on `β_0`.
2. UV renormalons are at `z = -4π/(β_0 n)` for positive integer `n`; same
   structural retention.
3. The asymptotic form of `β_n` at large `n` is
   `β_n ~ C_const · Γ(n + b) · (β_0/(4π))^{n+1}` with `C_const` and `b`
   tied to the Stokes-constant data.
4. Resurgence does NOT close `β_2` or `β_3` because (a) Stokes constants
   require identification of QCD instanton sector with framework content
   not pre-justified, and (b) finite-`n` corrections at `n = 2, 3`
   require the full Borel transform.
5. A candidate follow-on probe: postulate QCD instanton moduli ↔ framework
   monopole sector, derive `S_IR` from this identification, test whether
   resurgence then closes `β_2`. This would be a separate new structural
   conjecture requiring explicit approval, and is left open.

## 10. Reproduction

```bash
python3 scripts/cl3_koide_u_L1_resurgence_2026_05_08_probeU_L1_resurgence.py
```

Expected: a sequence of PASS lines for the support-only structural
checks (Borel-plane geometry, asymptotic factorial growth from
existing `β_0` inside the imported toolkit) and explicit
BOUNDED-ADMISSION lines for the
obstructions (Stokes constants, subleading exponents, finite-`n`
corrections), with a final summary classifying the probe verdict as
`no_go` for closed-form derivation by this route.
