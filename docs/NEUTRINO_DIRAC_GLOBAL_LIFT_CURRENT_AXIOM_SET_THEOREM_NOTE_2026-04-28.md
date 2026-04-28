# Dirac Global Lift on the Current Axiom Set — Manuscript-Grade Theorem

**Date:** 2026-04-28
**Status:** retained branch-local **manuscript-grade theorem** on
`frontier/neutrino-quantitative-20260428`. Consolidates Cycles 2, 6,
and 7 of the loop into a single publication-surface theorem suitable
for the post-loop integration pipeline. The Cycle-2 conditional Dirac
global lift becomes **on-current-axiom-set unconditional** via the
case-A/B/C closures of Cycles 6 and 7.
**Lane:** 4 — Neutrino quantitative closure (route 4D)
**Loop:** `neutrino-quantitative-20260428`

---

## 0. Statement

**Theorem (Dirac Global Lift on the Current Axiom Set).** Adopt the
framework's current accepted input stack `A_min` per
`MINIMAL_AXIOMS_2026-04-11.md`:

1. local algebra `Cl(3)`;
2. spatial substrate `Z^3`;
3. finite local Grassmann / staggered-Dirac partition + lattice
   operators on that surface;
4. canonical normalization `g_bare = 1` + plaquette / `u_0` surface
   + minimal APBC hierarchy.

Plus the framework's explicit **no-fitted-parameter posture**
(per the physics-loop SKILL Non-Negotiables and precedented by all
retained derivations including
`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`,
`ALPHA_S_DERIVED_NOTE.md`, and
`R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md`).

Then **the framework's neutrino sector is globally Dirac**:

- the unique anomaly-fixed same-chirality Majorana operator
  `nu_R^T C P_R nu_R` and its Hermitian conjugate have zero
  expectation and zero coefficient on every admissible extension
  of the staggered-Dirac partition;
- the Majorana phases `alpha_21` and `alpha_31` are vacuous;
- neutrino mass closure on `A_min` reduces to the Dirac Yukawa
  matrix `Y_nu` on the admitted Higgs / CW electroweak-scalar lane
  per `NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md`.

**Operational falsifier:** any positive `0nu beta beta` signal at
any experimental precision falsifies the theorem (per
Schechter-Valle 1982: any positive `0nu beta beta` rate implies
Majorana mass for at least one neutrino).

**Scope explicit:** "the current axiom set" means `A_min` plus the
no-fitted-parameter posture. A future framework extension that adds
new axioms — specifically a charge-`±2` fermionic primitive — would
be a separate theorem on a different scope, and could in principle
re-open Majorana mass.

## 1. Retained inputs (all on `main` or admitted convention)

| Identity | Authority | Role |
|---|---|---|
| `A_min` | `MINIMAL_AXIOMS_2026-04-11.md` | substrate axiom set |
| no-fitted-parameter posture | physics-loop SKILL Non-Negotiables; precedented by retained derivations | meta-level constraint |
| Anomaly-forced 3+1 + retained three-generation structure | three-generation cluster | matter-content scope |
| Canonical local Majorana block `A_M(mu) = mu * J_2` | `NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md` | one-real-amplitude reduction |
| Current-stack zero law `mu_current = 0` | `NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md` | local witness |
| Three-gen zero matrix `M_R,current = 0_(3x3)` | `NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md` §1 | three-gen witness |
| Finite normal grammar fermion-number `U(1)` | `NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md` | grammar-level selection rule |
| Current-atlas non-realization | `NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md` | retained atlas closure |
| Pfaffian no-forcing | `NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md` | grammar-boundary closure |
| 3+1D SO(3,1) boost-covariant 2-point closure | `LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md` | continuum-limit constraint |

Closed Majorana construction classes (cited as obstruction
inventory): Native-Gaussian, Finite-Normal-Grammar,
Lower-Level-Pairing per the corresponding retained no-go notes.

## 2. Proof structure

### 2.1 Step 1 — Current-stack zero is exact (Cycle 2)

By the retained current-stack Majorana zero law
(`NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md`) plus the
three-gen lift, `M_R,current = 0_(3x3)` on the retained
finite-normal-grammar surface. By `NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md`,
on the admitted Higgs / CW electroweak-scalar lane the remaining
mass-closing object is `Y_nu`.

So: on the current retained finite-normal-grammar surface, the
neutrino sector is Dirac and the Majorana coefficient `mu = 0`.

### 2.2 Step 2 — Pfaffian-extension exclusion on the current axiom set

A nonzero Majorana coefficient would require leaving the current
finite-normal-grammar surface via a Pfaffian-type pairing extension
of the staggered-Dirac partition, parametrized by a gap function
`Delta * S(t-t', |p|^2)` with charge `±2`.

By Cycles 6 and 7, **all three Pfaffian sub-classes are inadmissible
on the current axiom set:**

#### Case A — s-wave Pfaffian (`S(p) = const`)

The BdG Bogoliubov diagonalization on this case introduces a
**non-zero anomalous correlator** `<chi(t,x) chi(0,0)>` in the
quasiparticle-vacuum sector. The retained 3+1D SO(3,1) boost-
covariant 2-point closure `W_cont(s²; m) = m K_1(m sqrt(-s²)) /
(4π² sqrt(-s²))` is the **diagonal Wightman function** on the
bilinear surface; it does not include such an anomalous correlator.
Adding the s-wave Pfaffian would require enlarging the retained
correlator algebra outside the bilinear surface, which exceeds the
admissible content of the staggered-Dirac partition. **Excluded.**

#### Case B — angularly non-trivial Pfaffian (p-wave, d-wave, ...)

A gap function with non-trivial angular momentum (e.g.,
`S(p) ~ p_i sigma^i` p-wave) introduces a vector / tensor
transformation in the BdG Bogoliubov coefficients that violates
SO(3) angular isotropy. SO(3) is a subgroup of the retained
SO(3,1); breaking SO(3) violates the retained 3+1D boost-covariance
theorem on the continuum-limit surface. **Excluded directly by
retained content.**

#### Case C — angular-singlet, time-twisted, SO(3,1)-covariant Pfaffian

A gap function that is angular-singlet in 3-momentum and SO(3,1)-
covariant in time-separation requires specifying a real coupling
`Delta` and a profile function `S(s²)` of the Lorentz invariant
`s²`. Two possibilities:

- (a) `Delta` and `S` are fitted to observation: forbidden by the
  framework's no-fitted-parameter posture.
- (b) `Delta` and `S` are derived from `A_min`: would require
  structural content that does not currently exist. Per Cycle 3,
  `Cl(3)` algebra is permissive on charge-`±2` bilinears (cannot
  fix a unique `S`), and the staggered-Dirac structure rigidly
  excludes pairing terms on its admissible monomial class. A
  derivation would require **extending** `A_min` itself —
  exactly the "future axiom-side primitive" the retained Majorana
  cluster acknowledges as the load-bearing way Majorana mass
  enters the framework.

So on the current axiom set, possibility (a) is forbidden by
posture and possibility (b) requires extending `A_min`.
**Excluded on the current axiom set.**

### 2.3 Step 3 — Combining

By Step 1, the current finite-normal-grammar surface is Dirac. By
Step 2, no Pfaffian extension to that surface is admissible on the
current axiom set. Therefore on the current axiom set, the
framework's neutrino sector is **globally Dirac**: every admissible
extension preserves the Dirac structure.

By the retained mass reduction to Dirac
(`NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md`), neutrino mass closure
reduces to the Dirac Yukawa `Y_nu`. The Majorana phases
`alpha_21`, `alpha_31` are vacuous (Dirac neutrinos have no Majorana
phases).

`QED`

## 3. Falsifiers and scope

### 3.1 Empirical falsifier

Any positive `0nu beta beta` signal at any experimental precision
falsifies the theorem (Schechter-Valle: positive rate ⇒ Majorana
mass).

Current bounds: KamLAND-Zen `m_ββ < (28-122) meV` (90% CL);
next-generation experiments (LEGEND, nEXO) push toward sub-meV
sensitivity. The theorem's empirical content is **falsifiable in
principle and approachable in practice**.

### 3.2 Scope: future axiom-side primitives

The theorem is on the **current axiom set** `A_min` plus the
no-fitted-parameter posture. A future framework extension that
adds a charge-`±2` axiom-side primitive (a "genuinely new
ΔL = 2 microscopic object" per
`NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md` §5)
would be a separate theorem on a different scope.

This is not an obstruction to the theorem; it is a **scope
declaration**. All retained framework content lives on `A_min`;
the theorem lives on the same scope. Future axiom extensions
would similarly require revisiting all retained content,
including the Hubble structural lock theorem
(`HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md`),
the cosmology open-number reduction theorem
(`COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`),
and the entire retained quantitative package.

## 4. Manuscript-surface placement

This theorem is a candidate for the publication package's
neutrino-sector retention surface. Suggested placement:

- `docs/publication/ci3_z3/CLAIMS_TABLE.md`: add an entry
  "Dirac global lift on current axiom set" with explicit falsifier
  and scope.
- `docs/publication/ci3_z3/PREDICTION_SURFACE_2026-04-15.md`: add
  the falsifier as a structural prediction (no `0nu beta beta`
  signal at any precision).
- `docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md`
  §3D: mark as **landed** (4D Dirac global lift on current axiom
  set retained); preserve the future-axiom-extension scope note.
- `docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md` §6:
  retire the Majorana phases `alpha_21`, `alpha_31` from open
  bounded-row inputs (vacuous on the retained surface).
- `docs/publication/ci3_z3/WHAT_THIS_PAPER_DOES_NOT_CLAIM.md`:
  add the scope statement "the framework currently retains a
  Dirac global lift on the current axiom set; future axiom-side
  extensions would re-open the Majorana question".

These weaves are recorded in `HANDOFF.md` for the post-loop
integration step. They are **NOT** applied on this branch per
skill science-only delivery.

## 5. How this advances Lane 4

Before Cycles 2-7: 4D was the most achievable Phase-1 target with
existing scaffolding, but the full lift was open.

After Cycles 2-7: **4D Dirac global lift is landed on-current-axiom-
set unconditionally** with explicit operational falsifier.

The remaining Lane-4 work shifts to:

- **4A** absolute neutrino mass scale `m_lightest` — needs neutrino-
  Yukawa Ward identity (analog of YT-lane `y_t / g_s = 1/sqrt(6)`).
- **4E** Dirac mass mechanism without seesaw — since 4D excludes
  type-I seesaw, the mass spectrum comes directly from `Y_nu * v`,
  raising the question of `m_nu` smallness without seesaw
  suppression.
- **4F** cosmological `Sigma m_nu` bridge to Lane 5 (Hubble
  structural lock + matter-bridge identity).
- **4G** internal consistency check with retained `delta_CP ≈ -81°`
  and `theta_23 ≥ 0.5410` from the DM closed package.
- **4B/C** `Delta m^2_21` and `Delta m^2_31` follow arithmetically
  once 4A and 4E land.

## 6. Cross-references

### Cycle chain that produced this theorem

- Cycle 1: `NEUTRINO_LANE4_THEOREM_PLAN_NOTE_2026-04-28.md` — Lane 4
  closure roadmap.
- Cycle 2: `NEUTRINO_DIRAC_GLOBAL_LIFT_PARTIAL_THEOREM_NOTE_2026-04-28.md`
  — conditional theorem + named obstruction `(C2-X)`.
- Cycle 3: `NEUTRINO_NORMAL_GRAMMAR_U1_RIGIDITY_STRETCH_ATTEMPT_NOTE_2026-04-28.md`
  — first-principles stretch attempt; falsified `(R-X1)`;
  reformulated to decision-level.
- Cycle 4: `NEUTRINO_AXIOM3_READING_STUCK_FANOUT_NOTE_2026-04-28.md`
  — stuck fan-out; revised Cycle 3 to permissive reading;
  identified `(SR-2)` as best continuation.
- Cycle 6: `NEUTRINO_PFAFFIAN_CONTINUUM_LIMIT_INCOMPATIBILITY_NOTE_2026-04-28.md`
  — cases A and B closed; case C named.
- Cycle 7: `NEUTRINO_PFAFFIAN_CASE_C_NO_FITTED_GAP_EXCLUSION_NOTE_2026-04-28.md`
  — case C closed via no-fitted-parameter posture; this
  consolidation theorem follows.

### Retained framework authorities

- `MINIMAL_AXIOMS_2026-04-11.md` — `A_min`.
- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`,
  `ALPHA_S_DERIVED_NOTE.md`,
  `R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md`
  — no-fitted-parameter precedents.
- `LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md` — case-A and
  case-B exclusion authority.
- Majorana cluster:
  `NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE.md`,
  `NEUTRINO_MAJORANA_CANONICAL_LOCAL_BLOCK_NOTE.md`,
  `NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md`,
  `NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md`,
  `NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md`,
  `NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE.md`.
- Closed Majorana construction classes:
  `NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md`,
  `NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md`,
  `NEUTRINO_MAJORANA_LOWER_LEVEL_PAIRING_NOGO_NOTE.md`.

### Lane-4 cross-references

- Lane file: `docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md`
- Loop pack: `.claude/science/physics-loops/neutrino-quantitative-20260428/`
- Adjacent Cycle 5 close-out (superseded by user runtime extension):
  `NEUTRINO_LANE4_WORKSTREAM_CLOSEOUT_NOTE_2026-04-28.md`

### Empirical / methodological references

- Schechter-Valle 1982 (positive `0nu beta beta` ⇒ Majorana mass):
  admitted convention; cited only as falsifier statement.
- KamLAND-Zen `m_ββ` bound; LEGEND / nEXO future programs:
  experimental comparators.

## 7. Boundary

This is a manuscript-grade consolidation theorem. It does not
introduce new structural content beyond Cycles 2, 6, 7 — it
consolidates them into a single publication-surface statement with
clean theorem / premises / proof / falsifier / scope structure. It
**does** retire `alpha_21`, `alpha_31` from the open input ledger
(vacuous on the retained surface).

The theorem is suitable for the post-loop integration pipeline
(analog of how `HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md`
was integrated into `main` via `a8dd7918 cosmology: land Hubble
structural lock lane`).

A runner is not authored: the proof is structural case-analysis
on the Majorana cluster + Pfaffian sub-class taxonomy + framework
posture. No new symbolic or numerical content is introduced.
