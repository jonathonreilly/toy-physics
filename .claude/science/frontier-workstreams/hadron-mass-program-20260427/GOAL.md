# Hadron Mass Program Workstream

**Goal:** retain quantitative hadron mass predictions on the framework
surface — initially `m_p`, `m_n`, `m_pi`; later kaon, ρ, B-meson masses,
hadron spectroscopy, and form factors.

**User invocation:** `/frontier-workstream Lane 1 --mode run --runtime 12h`

**Target status:** `best-honest-status`. Retained closure if achievable;
substantial exact support, no-go, or import retirement otherwise. Pure
prose passes do not count.

## Lane reduction (per lane file)

Per
[`docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md`](../../../../docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md),
the **first parallel-worker target** is to reduce the lane to a sharp
pion/proton mass theorem plan using:

- current confinement (`T = 0` retained, √σ ≈ 465 MeV bounded);
- α_s running (`α_s(M_Z) = 0.1181` retained; running bridge to hadronic
  scale needed);
- Lane 3 quark-mass dependencies (currently bounded — five quark masses
  scaffolded; only top mass retained).

The lane file lists five derivation targets:

- **3A — Pion mass via Gell-Mann-Oakes-Renner** (Tier B once Lane 3
  lands quark masses): `m_π² f_π² = (m_u + m_d) Σ`.
- **3B — Proton/neutron mass ab initio QCD** (Tier C): standard
  lattice-QCD methodology adapted to framework substrate.
- **3C — Hadron spectroscopy** (Tier C): kaon, ρ, ω, B/D mesons,
  baryon octet/decuplet.
- **3D — Hadron form factors** (Tier C): B → π, K → π, nucleon EM,
  pion EM.
- **3E — √σ retained promotion** (Tier B; **runs parallel to Lane 3**):
  tighten EFT bridge + screening corrections to move √σ from bounded
  (5.6%) to retained.

Phase 1 of the lane file is "after Lane 3 lands quark masses": close 3A
(m_π via GMOR) and 3E (√σ promotion) in parallel. Phase 2: m_p ab
initio (3B). Phase 3: spectroscopy and form factors.

## Workstream priorities

In order of next-cycle execution:

1. **R2 — Lane 3 dependency audit + Lane 1 theorem plan (Tier A).** The
   lane file's first parallel-worker target. Map Lane 1 closure onto
   current retained content; identify what Lane 3 must land before each
   of 3A, 3B can proceed; identify the Lane-1-internal work that can
   proceed in parallel (3E primarily).
2. **R6 — Confinement / √σ EFT bridge audit (Tier B).** Identifies the
   gap between bounded √σ ≈ 465 MeV (5.6% above PDG 440) and a retained
   sub-percent or retention-budget claim. Lane-1-internal; runs parallel
   to Lane 3.
3. **R7 — Chiral condensate Σ structural attempt (Tier B-C).** Direct
   attack on the m_π entry point (3A): can the staggered-Dirac partition
   on `Cl(3)/Z³` deliver a retained Σ? Tier-C unless a clean structural
   path emerges.
4. **R8 — hadron-mass closed-route no-go.** If easy hadron-mass routes
   are excluded, prove a specific class-bounding negative.
5. Higher-tier routes (3A, 3B, 3C, 3D) are conditional on Lane 3
   retentions and lattice-QCD bridge work.

## Delivery

Science-only on branch `frontier/hadron-mass-program-20260427`. Push
that branch to `origin`. Do not open a PR. Do not push to `main`.
Proposed repo-wide weaving recorded in `HANDOFF.md` only.
