# Assumptions And Imports

**Slug:** axiom-to-main-lane-cascade-20260429
**Date:** 2026-04-29

The minimal accepted axiom stack for the framework
([MINIMAL_AXIOMS_2026-04-11.md](../../../../docs/MINIMAL_AXIOMS_2026-04-11.md)):

1. **A1: Local algebra** — physical local algebra is `Cl(3)` (3D real Clifford,
   3 generators).
2. **A2: Spatial substrate** — physical spatial substrate is the cubic lattice
   `Z^3`.
3. **A3: Microscopic dynamics** — finite local Grassmann / staggered-Dirac
   partition with lattice operators on that surface.
4. **A4: Canonical normalization** — `g_bare = 1`; canonical plaquette / `u_0`
   surface; minimal APBC hierarchy block where applicable.

A4's `g_bare = 1` is independently retained on two routes
(operator-algebra + 1PI Ward) plus a Grassmann/spectral
dynamical-fixation obstruction.

The physical-lattice reading on A2 is now derived from A_min via
PHYSICAL_LATTICE_NECESSITY_NOTE.md (one-axiom Hilbert/locality/information).

## Ledger

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|
| `Cl(3)` (A1) | local algebra | zero-input structural | A_min | yes | yes | none required (axiom) | accepted |
| `Z^3` (A2) | spatial substrate | zero-input structural | A_min | yes | yes | none required (axiom); physical-lattice reading derived from A_min | accepted |
| Grassmann/staggered-Dirac (A3) | dynamics | zero-input structural | A_min | yes | yes | none required (axiom) | accepted |
| `g_bare = 1` (A4) | normalization | zero-input structural | A_min; two retained routes | yes | yes | independently retained | accepted |
| Plaquette `<P> = 0.5934` | numerical input | derived (lattice MC); analytic `P_cand(6) = 0.593530679977098` not yet final | PLAQUETTE_SELF_CONSISTENCY_NOTE | yes | yes | analytic β=6 Perron / boundary closure (Q7) | open analytic |
| `u_0 = <P>^(1/4)` | tadpole | derived (same-surface) | same | yes | yes | derives from `<P>` | accepted-derived |
| `α_LM`, `α_s(v)` | couplings | derived (same-surface) | ALPHA_S_DERIVED_NOTE | yes | yes | derives from `<P>` | accepted-derived |
| EW `v = 246.282818290129 GeV` | scale | derived | OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE | yes | yes | retained on conditional Planck packet | accepted-derived |
| Anomaly-forced `3+1` | spacetime | retained | (cited in MINIMAL_AXIOMS) | yes | for Q4 (Cl_4(C) extension) | already retained | accepted-derived |
| Three-generation matter (N_gen=3) | structure | retained on one-axiom Hilbert/locality/information surface | PHYSICAL_LATTICE_NECESSITY_NOTE; GENERATION_AXIOM_BOUNDARY_NOTE | yes | yes | already retained | accepted-derived |
| Native `SU(2)` | gauge | retained | NATIVE_GAUGE_CLOSURE_NOTE | yes | for Q4 | already retained | accepted-derived |
| Graph-first `SU(3)` | gauge | retained | GRAPH_FIRST_SU3_INTEGRATION_NOTE | yes | for Q4 | already retained | accepted-derived |
| Wald formula | universality input | literature theorem | external (Wald 1993) | yes for Q5 | yes | none required (literature on equal footing with Newton) | admitted-context |
| Cl_4(C) module on `P_A H_cell` (Axiom*) | extension | hypothetical (not adopted) | CL4C_CARRIER_AXIOM_CONSEQUENCE_MAP_NOTE | yes for (G1) closure | hypothetical | Q4: derive from A_min, OR prove no-go forcing adoption | open |
| Quark masses `m_q` | observational | observational comparator | PDG | yes for line 163-164 status | only for comparator | retire via Q3 (structural endpoint chain) | bounded |
| Charged-lepton masses `m_l` | observational | observational comparator | PDG | yes for charged-lepton-pickup | comparator only after Q1+Q2 land | retire via Q1 (Koide Q) + Q2 (Koide δ) + structural V_0 chain | open |
| η_obs (Planck baryon-to-photon ratio) | observational | observational comparator | Planck | yes for line 125 | comparator only | retire via Q6 (DM η closure) | bounded |
| Σm_ν observational comparator | observational | observational | cosmology | yes for line 123, 192 | comparator | (out of campaign scope) | bounded-comparator |
| C_ν = 93.14 eV | convention | admitted convention | T_CMB + N_eff | sigma-mnu loop | (out of campaign scope) | (admitted) | accepted-admitted |
| (T-4F-α-2) identity | structural | retained | sigma-mnu work | sigma-mnu loop | (out of campaign scope) | already retained | accepted-derived |

## Forbidden imports per block

For each block, the following imports are forbidden as load-bearing proof
inputs. Comparator use (after the derivation closes) is allowed but must be
called out explicitly.

### Block 1 (Q1: Koide Q) forbidden imports
- observed `m_e`, `m_μ`, `m_τ`
- observed `Q_obs ≈ 2/3`
- any selector tuned to recover `Q = 2/3`
- any literature Koide-mechanism import
- A_min only; SO(2)/Z_3 source-rotation symmetries on the cubic graph
  axis are derived structures

### Block 2 (Q2: Koide δ) forbidden imports
- observed `δ_obs ≈ 2/9 rad`
- any period convention chosen to yield 2/9
- A_min + Q1 closure only

### Block 3 (Q3: quark mass ratios) forbidden imports
- observed quark mass ratios at any scale
- fitted CKM parameters
- A_min + retained gauge-vacuum plaquette stack only

### Block 4 (Q4: Cl_4(C) axiom) forbidden imports
- Axiom* itself (the loop's job is to derive or prove no-go)
- any literature Clifford-extension theorem (these are admitted-context only)
- A_min + retained anomaly-forced 3+1 + retained `Cl(3)` content only

### Block 5 (Q5: BH 1/4 carrier) forbidden imports
- any literature BH `S = A/4G` value (Wald formula is admitted as
  universal-physics input on equal footing with Newton)
- any tuning of the framework's `c_cell` to recover `1/4`

### Block 6 (Q6: DM η) forbidden imports
- observed `η_obs = 6.12e-10`
- any selector tuned to recover η_obs
- A_min + retained EW `v` + retained graph-first `SU(3)` lane only

## Retirement paths summary

| Import | Retirement route | Block | Expected outcome |
|---|---|---|---|
| `Q_obs` (charged-lepton Koide) | Q1 axiom-cyclic-line closure | 1 | retained Q=2/3 corollary OR exact no-go |
| `δ_obs` (Koide phase) | Q2 Berry-phase orbit closure | 2 | retained δ=2/9 corollary OR exact no-go |
| quark mass ratios | Q3 taste-staircase endpoint chain | 3 | exact endpoint structure OR bounded with named obstruction |
| Axiom* | Q4 extension derivation OR no-go | 4 | retain (G1) OR exact axiom-stack minimality theorem |
| Wald formula universality acceptance | Q5 BH carrier | 5 | retained BH `1/4` corollary on framework GR action |
| `η_obs` matching | Q6 N_sites · v derivation | 6 | retained DM eta corollary OR demote to no-go |
| analytic plaquette `P(6)` | Q7 explicit Perron solve | 7 | retained analytic `<P>` OR named obstruction |

## Nature-grade criteria check (per skill SKILL.md)

For any retained-grade closure proposed in this campaign, every load-bearing
item must be:
- derived from retained structure;
- retained/exact support with named bridge;
- explicitly admitted with narrow non-derivation role;
- quantitatively insensitive; or
- demoted out of the retained claim.

The campaign's bare `retained` / `promoted` wording in branch-local source
notes is BANNED per the skill firewall. Allowed: `proposed_retained`,
`proposed_promoted`, `exact support`, `bounded support`, `conditional /
support`, `open`, `no-go`, `demotion`, `hypothetical consequence map`.
