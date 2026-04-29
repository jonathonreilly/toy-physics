# Lane 4F Phase-2 Attack Frame — Stuck Fan-Out

**Date:** 2026-04-28
**Status:** proposed_retained branch-local **stuck fan-out** note on
`frontier/neutrino-sigma-mnu-cosmology-20260428`. Cycle 3 of the 4F
loop. With 4F-α (structural functional form) RETAINED in Cycle 2,
Phase-2 (numerical `Σm_ν` retention) is the next target. Per Deep
Work Rules, before honest stop on the 4F block (or before another
stretch attempt), generate 4-6 orthogonal Phase-2 attack frames,
synthesize, identify the cleanest single-cycle continuation.
**Result: F3 (cross-lane bound from retained DM relic abundance
content) and F1 (Lane 5 (C1) absolute-scale gate audit) emerge as
the strongest single-cycle Phase-2 attack frames. F2, F4-F6 are
research-level distant.**
**Lane:** 4 — Neutrino quantitative closure (sub-target 4F)
**Loop:** `neutrino-sigma-mnu-cosmology-20260428`

---

## 0. Context

Cycle 1 produced the theorem plan; Cycle 2 retained 4F-α (structural
functional form). Both Deep Work Rules requirements (audit + stretch)
are satisfied. Phase-2 is numerical `Σm_ν` retention, which the
Cycle 2 audit identified as conditional on:

- Lane 5 (C1)+(C2)/(C3) gate closures → bounded `h`.
- Admitted-input promotions for `(Ω_b, Ω_DM)`.

Per Deep Work Rules: stuck fan-out before any "no route passes the
gate" stop. Six candidate Phase-2 attack frames generated.

## 1. Six candidate Phase-2 attack frames

### F1 — Lane 5 (C1) absolute-scale gate audit

**Premise:** the Lane 5 closure-pathway taxonomy retained the (C1)
absolute-scale gate as the one of two gates (along with one of
(C2)/(C3) cosmic-L) needed for `h` numerical retention.

**Mechanism:** audit the (C1) gate on the current retained surface,
identify any single-cycle attack frame that would close (C1) via
existing retained content (e.g., retained Λ-spectral-gap identity
plus retained scale identification might give a structural `H_0`
anchor on the retained surface).

**Constraint count:** (C1) requires deriving an absolute scale from
retained `R_Λ` plus some retained anchor. The 2026-04-26 audit had
isolated this as the gate without closing it.

**Status:** **HIGH** promise; single-cycle attemptable. Closure of
(C1) would unblock half of the `h` retention pathway and is the most
direct route to bounded `h` for 4F-β.

### F2 — Admitted-input promotion via baryogenesis structure

**Premise:** the framework's retained `η`-from-anomaly content (if
any) might give a structural `Ω_b h²` identity.

**Mechanism:** retained matter-asymmetry / baryogenesis structural
identity plus admitted photon density gives `Ω_b` directly.

**Constraint count:** depends on whether retained baryogenesis
content exists; per `ASSUMPTIONS_AND_IMPORTS.md`, `η` is admitted
observational layer per cosmology open-number reduction §1.

**Status:** speculative; no retained baryogenesis structural
identity currently known to deliver `Ω_b h²` numerically.

### F3 — DM relic abundance retained-content cross-bound

**Premise:** the framework has the DM Schur-suppression cluster
(`DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md`) and
the DM closed package (DM mass + cross-section retentions). If a
retained DM relic identity gives `Ω_DM h²` structurally, then the
4F-α identity simplifies:

```text
Σm_ν  =  (Ω_m,0 - Ω_b - Ω_DM) × C_ν × h²
      =  (Ω_m,0 - Ω_b - Ω_DM(retained)) × C_ν × h²
```

**Mechanism:** retained DM Schur-suppression + retained DM mass
might give `Ω_DM h²` as a structural function of retained inputs.

**Constraint count:** depends on the DM cluster's actual retention
content. Multiple recent audit-repair PRs (#137, #138, #164) are
narrowing the DM cluster's retained surface; status uncertain.

**Status:** **MEDIUM-HIGH** promise; needs sharper audit of the
DM cluster's retained content in Cycle 4. If `Ω_DM h²` is retained
or bounded, this is a strong Phase-2 attack frame.

### F4 — N_eff cross-validation lower-bound

**Premise:** retained `N_eff = 3.046` plus retained neutrino mass-
splittings (Δm²_21, Δm²_31) would give a structural lower bound on
`Σm_ν` via the mass hierarchy:

```text
Σm_ν  ≥  sqrt(Δm²_21) + sqrt(Δm²_31)  ≈ 0.06 eV  (NH lower bound)
```

**Mechanism:** retained `N_eff` doesn't directly bound `Σm_ν`, but
the framework's retained neutrino observable bounds plus oscillation
hierarchy might.

**Constraint count:** depends on Lane 4 4B/4C status (Δm² retention).

**Status:** distant; Δm² retention is open per Lane 4 4B/4C
sub-target status.

### F5 — Cross-lane Hubble structural-lock + 4F closed-form bound

**Premise:** the retained Hubble structural-lock theorem
(`HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md`) +
retained `R_Λ`-anchor admitted bound on `h` might give a bounded `h`
sufficient to give a bounded `Σm_ν` interval.

**Mechanism:** the structural-lock theorem retained `H_0(z)`
constancy at late times, but did not retain numerical `H_0`.
Combined with admitted `R_Λ`-anchor range, gives a bounded `h`
interval; substituted into 4F-α gives a bounded `Σm_ν` interval.

**Constraint count:** depends on accepted `R_Λ`-anchor admitted
bound width. The cosmology open-number reduction §1 lists
`R_Λ`-anchor as admitted observational layer.

**Status:** **MEDIUM** promise; would deliver a wide bounded
interval, not a tight retention. Could be a Cycle-4 follow-on
to F1.

### F6 — Direct Ω_ν retained identity via three-generation structure

**Premise:** the framework has retained three-generation matter
structure + `N_eff = 3.046` from three generations. If three-
generation structure directly constrains `Ω_ν h²` via some retained
representation-theoretic identity, that's a direct Phase-2 retention
without the matter-budget split.

**Mechanism:** speculative — would require a retained primitive
relating Cl(3) three-generation structure to neutrino-relic density.

**Status:** highly speculative; no retained content currently
connects three-generation structure to relic density numerically.

## 2. Synthesis

| Candidate | Promise | Single-cycle? | Dependencies |
|---|---|---|---|
| **F1 Lane 5 (C1) absolute-scale gate** | **HIGH** | **yes** | retained Λ + scale identity |
| F2 baryogenesis/η promotion | low | speculative | unestablished primitive |
| **F3 DM relic abundance cross-bound** | **MEDIUM-HIGH** | needs audit | DM cluster retained content uncertain |
| F4 N_eff + Δm² lower bound | low | distant | Δm² retention open |
| F5 Hubble lock + bounded `h` interval | medium | yes (wide bound) | admitted `R_Λ` anchor width |
| F6 three-gen direct Ω_ν | low | speculative | no current connection |

**Strongest:** F1 (Lane 5 (C1) absolute-scale gate audit). Reasons:

- Direct attack on `h` retention, the single highest-leverage
  admitted/open input for 4F-β.
- (C1) gate already isolated by 2026-04-26 audit work; substantial
  groundwork done.
- Single-cycle attemptable: gate audit is structural, not numerical.
- Closure of (C1) plus an existing one of (C2)/(C3) closes the
  Hubble two-gate dependency, unlocking 4F-β substantially.
- Same lane-progression pattern as Lane 6 charged-lepton: when
  primary target is research-level distant, attack the parallel-lane
  prerequisite.

**Backup:** F3 (DM relic abundance cross-bound). Reasons:

- Uses retained DM cluster (highest-confidence DM retention).
- Could deliver `Ω_DM h²` retention directly.
- Requires audit of current DM cluster content (Cycle 4 work).

**Reject:** F4, F6 as too distant. F2 as speculative. F5 as wide-
bound only (cycle-4 follow-on, not Phase-2 closure).

## 3. Cross-lane Phase-2 ordering

**Phase-2-A (Cycle 4 of this loop or fresh loop):** F1 Lane 5 (C1)
absolute-scale gate audit + structural-attempt. If (C1) closes,
half of `h` retention pathway is open.

**Phase-2-B (parallel):** F3 audit DM cluster retained content.
If `Ω_DM h²` is retained, 4F-α simplifies.

**Phase-2-C (after A or B):** combine retained `h` (from A) with
retained `Ω_DM h²` (from B) plus admitted `Ω_b h²` to retain `Σm_ν`
as bounded interval. Closes 4F-β.

## 4. Recommended next action

**Honest stop on this 4F loop after Cycle 3.** Both Phase-1 targets
retained (4F-α structural functional form + theorem plan +
fan-out). Phase-2 closure requires a dedicated fresh physics-loop
on Lane 5 (C1) gate (F1) — that's a different science block and
should get its own loop.

**Open PR for 4F block** (already done — PR #167).

**Recommended next loop:** `frontier/hubble-c1-absolute-scale-gate-20260428` —
fresh physics-loop on Lane 5 (C1) absolute-scale gate audit + structural
attempt. Phase-1 priority of that loop = (C1) gate closure attempt.

## 5. Loop status after this fan-out

Per Deep Work Rules requirements:
- Stretch attempts (Cycle 2): 1 ✓
- Stuck fan-out (this cycle): 1 ✓
- Both requirements satisfied for honest stop.
- Audit cycles (1, 3): 2 — within 2-consecutive max.

Honest stop on 4F block is justified; PR open; Phase-2 follow-on
identified for a fresh loop.

## 6. Cross-references

- Cycle 1 theorem plan:
  `docs/NEUTRINO_LANE4_4F_SIGMA_M_NU_THEOREM_PLAN_NOTE_2026-04-28.md`.
- Cycle 2 functional-form theorem:
  `docs/NEUTRINO_LANE4_4F_SIGMA_M_NU_FUNCTIONAL_FORM_THEOREM_NOTE_2026-04-28.md`.
- Lane 5 (C1) gate audit (existing):
  `docs/HUBBLE_LANE5_PLANCK_C1_GATE_AUDIT_NOTE_2026-04-26.md`
  (integrated upstream).
- Lane 5 two-gate dependency firewall:
  `docs/HUBBLE_LANE5_TWO_GATE_DEPENDENCY_FIREWALL_NOTE_2026-04-27.md`.
- DM Schur-suppression theorem (F3 anchor candidate):
  `docs/DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md`.
- Cosmology open-number reduction (4F-α anchor):
  `docs/COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`.
- Loop pack:
  `.claude/science/physics-loops/neutrino-sigma-mnu-cosmology-20260428/`.

## 7. Boundary

This is a stuck-fan-out artifact. It does not retain any input,
does not close 4F-β, and does not attempt F1 directly. It identifies
F1 (Lane 5 (C1) absolute-scale gate audit) as the cleanest single-
cycle Phase-2 attack frame, with F3 (DM relic abundance cross-bound)
as the strong backup.

The fan-out justifies honest stop on this 4F loop with PR #167
representing the science block. Phase-2 follow-on goes to a fresh
loop on Lane 5 (C1) gate.

A runner is not authored.
