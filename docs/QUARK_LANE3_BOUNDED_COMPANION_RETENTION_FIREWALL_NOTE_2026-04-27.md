# Quark Lane 3 Bounded-Companion Retention Firewall

**Date:** 2026-04-27
**Type:** bounded_theorem (axiom-reset retag 2026-05-03; was positive_theorem)
**Admitted context inputs:** staggered-Dirac realization derivation target (canonical parent: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`).
**Status:** proposed_retained exact negative boundary for Lane 3 dependency
accounting. This is not a retained derivation of `m_u`, `m_d`, `m_s`, `m_c`,
or `m_b`.
**Script:** `scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py`
**Lane:** Lane 3 quark masses retention

## Question

Can the current CKM/quark-mass support packet honestly be promoted to retained
closure for the five non-top quark masses?

## Result

No.

The current quark package is strong bounded support, but it is not a retained
mass-spectrum theorem. The exact firewall is:

- the top mass is the only retained quark mass;
- the down-type ratios are bounded because they depend on GST, the `5/6`
  bridge, and threshold-local scale selection that are not yet theorem-core
  retention steps;
- the up-type package is bounded because the partition/scalar amplitude is
  not derived from the retained core;
- the retained `y_t` Ward identity cannot be applied species-uniformly to
  get `m_b`: that physical reading overshoots the bottom mass by about `35x`;
- CKM closure is a mixing theorem, not a mass-retention theorem.

Therefore Lane 3 remains open for `m_u`, `m_d`, `m_s`, `m_c`, and `m_b`.

## Theorem

**Theorem (Lane 3 bounded-companion retention firewall).** Adopt the current
Lane 3 support surface: retained `m_t`, retained top-channel Ward identity,
retained/promoted CKM atlas support, bounded down-type CKM-dual mass ratios,
bounded up-type extension, and the b-Yukawa species-uniform scope analysis.

Then no retained five-mass closure follows unless the branch supplies all of:

1. a theorem-core derivation of the down-type bridges and scale-selection rule
   if the down-type CKM-dual path is used;
2. a retained up-type partition or scalar amplitude law that fixes the
   remaining up-sector ratios without observation-comparator selection;
3. a species-differentiated Yukawa Ward or equivalent absolute-scale primitive
   for the non-top quark Yukawas.

Absent those premises, the existing packet remains bounded companion support.

## Why Ratios Are Not Absolute Masses

The down-type lane gives ratio formulas:

```text
m_d/m_s = alpha_s(v) / 2
m_s/m_b = [alpha_s(v) / sqrt(6)]^(6/5)
m_d/m_b = (m_d/m_s)(m_s/m_b)
```

These ratios are useful. They do not fix `m_b`, and therefore do not fix
absolute `m_s` or `m_d`. Changing the bottom anchor rescales all three
down-type masses while preserving the same ratios.

## Why CKM Closure Is Not Mass Closure

The retained CKM package supplies structural mixing magnitudes and CP
geometry. It can support mass-ratio bridges, but it does not itself supply
physical quark masses. Treating CKM closure as quark-mass retention would
silently import the exact bridge theorems, partition laws, scale-selection
rules, and species-differentiation primitive that Lane 3 explicitly lists as
open.

## What This Retires

This retires four fast-but-wrong upgrades:

```text
CKM closure => retained quark masses
```

```text
bounded down-type ratio match => retained m_d, m_s, m_b
```

```text
up-type candidate shortlist => retained m_u, m_c
```

```text
top-channel Ward identity applied species-uniformly => retained m_b
```

## What Remains Open

Lane 3 remains open. The exact next gates are:

- non-perturbative theorem-core proof of the `5/6` bridge and the
  threshold-local scale-selection rule;
- up-type amplitude/partition selection law, currently narrowed to a short
  candidate grammar but not framework-forced;
- generation-stratified or species-differentiated Yukawa Ward identities for
  the five non-top quark species;
- absolute scales for the five masses, chained only after ratio and Ward gates
  are retained.

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
```

Expected result:

```text
PASS=17 FAIL=0
```

Focused support runners:

```bash
PYTHONPATH=scripts python3 scripts/frontier_quark_mass_ratio_review.py
PYTHONPATH=scripts python3 scripts/frontier_yt_bottom_yukawa_retention.py
PYTHONPATH=scripts python3 scripts/frontier_yt_ward_identity_derivation.py
```

## Inputs And Import Roles

| Input | Role | Import class | Source |
|---|---|---|---|
| retained `m_t` and `y_t/g_s = 1/sqrt(6)` | top-channel retained anchor | retained | `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, Lane 3 stub |
| down-type CKM-dual ratios | bounded ratio support | bounded bridge | `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md` |
| up-type partition/scalar support | bounded ratio support | bounded candidate grammar | `QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md`, review packet |
| species-uniform b-Yukawa analysis | negative scope boundary for uniform Ward reuse | retention-analysis no-go | `YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md` |
| PDG quark mass values | comparator/sensitivity only | comparator | existing quark runners |

No observed quark mass is used as a derivation input in this note. Observed
values are used only to expose which current support routes remain bounded.

## Safe Wording

Can claim:

- Lane 3 has an executable firewall separating bounded companion matches from
  retained quark-mass closure;
- the down-type ratios are strong bounded support but not absolute mass
  retention;
- the up-type branch remains open at the partition/scalar law;
- species-uniform Ward reuse for `m_b` is closed negatively.

Cannot claim:

- `m_u`, `m_d`, `m_s`, `m_c`, or `m_b` are retained;
- CKM closure alone derives quark masses;
- the `5/6` bridge is theorem-core retained;
- the top Ward identity applies uniformly to all quark species as a physical
  Yukawa boundary condition.


## Hypothesis set used (axiom-reset 2026-05-03)

Per `MINIMAL_AXIOMS_2026-05-03.md`, this note depends on the **staggered-Dirac realization derivation target**, which is currently an open gate. The note's load-bearing claim defines or relies on fermion fields, fermion-number operators, fermion correlators, fermion bilinears, the staggered Dirac action, the BZ-corner doubler structure, the `hw=1` triplet, charged-lepton sector content, neutrino sector content, quark / hadron content, the Koide / PMNS / CKM observable surfaces, or the Grassmann CAR boundary structure — all of which depend on the staggered-Dirac realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`.

Canonical parent note: `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md` (`claim_type: open_gate`). In-flight supporting work (see `MINIMAL_AXIOMS_2026-05-03.md`):

- `PHYSICAL_LATTICE_NECESSITY_NOTE.md`
- `THREE_GENERATION_STRUCTURE_NOTE.md`
- `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`
- `scripts/frontier_generation_rooting_undefined.py`
- `GENERATION_AXIOM_BOUNDARY_NOTE.md` (preserved)

Therefore `claim_type: bounded_theorem` until that gate closes. When that gate closes, the lane becomes eligible for independent audit/governance retagging as `positive_theorem`; the audit pipeline recomputes `effective_status`, but it does not silently invent a new `claim_type`. The substantive science content of this note is unchanged by this retag.
