# Hadron Mass Program — No-Go Ledger

**Date:** 2026-04-27
**Workstream:** `hadron-mass-program-20260427`
**Purpose:** prior dead routes the workstream must not re-explore. Only
re-open a route when a new premise is named that breaks a specific
obstruction.

## 1. Direct hadron-mass no-gos

None on `main`. No prior note has ruled out a specific hadron-mass
derivation route. The workstream may therefore propose any
structurally honest route without re-treading prior ground here.

## 2. Adjacent BH-entropy / area-law no-gos (peripheral)

These no-gos are about the gravitational/area-law side of the program
(Planck lane). They affect Lane 1 only insofar as they constrain the
broader carrier theory; they do not directly close hadron-mass routes.

- `BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md` — bounded carrier reaches
  `c_Widom ≤ 1/6`, not `1/4`; relevant to Planck-lane (`(C1)`) but
  not to hadron masses directly.
- `AREA_LAW_*_NO_GO_*` series (2026-04-25) — area-law shortcut
  no-gos on the carrier identification; same scope.

**Implication for Lane 1:** none direct. Lane 1 proceeds independently.

## 3. Adjacent quark-mass / Lane 3 no-gos

The quark-mass lane (Lane 3) has work in progress; some routes have
been closed there. Lane 1 cycles must not propose hadron-mass
derivations that depend on a Lane-3 route already closed.

The current Lane-3 ground state (per the lane registry):

- `m_t (pole) = 172.57 GeV` retained via `y_t / g_s = 1/sqrt(6)` Ward
  identity.
- All five non-top quark masses (m_u, m_d, m_s, m_c, m_b) bounded /
  scaffolded.

No specific Lane-3 no-go is binding on Lane 1 routes at present.
Cycles that depend on Lane 3 must explicitly cite the Lane-3 entry
point (`docs/QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md` or the
lane file).

## 4. Adjacent confinement / string-tension routes

The retained `T = 0` confinement (`docs/CONFINEMENT_STRING_TENSION_NOTE.md`)
plus bounded `sqrt(sigma) ≈ 465 MeV` is the existing quantitative
piece of the QCD sector. No specific no-go closes the bounded → retained
promotion path; the issue is that the EFT bridge + screening-correction
budget has not been formally retained.

**Implication for Lane 1:** route 3E (√σ retained promotion) is open
work; no prior no-go forbids it.

## 5. Standard-physics routes that must not be silently imported

These are not framework no-gos but standard-physics conventions that
the workstream must explicitly declare rather than silently absorb:

- Standard lattice QCD methodology (Wilson / staggered fermion actions)
  — the framework's substrate language already supports these, but
  using lattice-QCD machinery to extract hadron masses requires
  declaring it as an admitted-convention bridge in the inputs ledger
  (already done in `ASSUMPTIONS_AND_IMPORTS.md` §4).
- Chiral perturbation theory — admitted convention; same handling.
- Standard SM running of `alpha_s` from `M_Z` to hadronic scale —
  bridge layer; same handling.

A cycle that uses these layers without explicit declaration in
`ASSUMPTIONS_AND_IMPORTS.md` fails the dramatic-step gate's import-
ledger check.

## 6. Workstream rule

Lane 1 has a clear-field at the level of direct hadron-mass no-gos.
The main rule is the import-ledger discipline (§5): standard-physics
bridges must be declared, not silently absorbed. Beyond that, all
five derivation targets (3A-3E) remain open.
