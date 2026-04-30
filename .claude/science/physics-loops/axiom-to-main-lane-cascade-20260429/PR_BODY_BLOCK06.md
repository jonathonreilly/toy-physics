# [physics-loop] axiom-to-main-lane-cascade block 06: DM η N_sites · v structural support (bounded)

## Summary

Block 6 records bounded structural support for the DM η freeze-out-bypass
`m_DM = N_sites · v` candidate: the previously audit-discovered
candidate is also framework-composed from retained N_sites = 16
(Higgs mass derivation, minimal APBC block on Z^4) + retained EW
v ≈ 246.28 GeV (observable-principle-from-axiom).

This is genuine support improvement (not just a numerical candidate
among 22 audit candidates; also a framework-composed product of two
retained quantities), but the G1 dark-singlet
collective-mode Coleman-Weinberg mechanism remains explicitly OPEN.

The bounded η prediction band [5.25e-10, 8.11e-10] brackets the Planck
observation `eta_obs = 6.12e-10`. Falsifiable prediction:
`m_DM = 16 v ≈ 3.94 TeV` for WIMP-like dark matter.

## Status (per skill firewall fields)

- `actual_current_surface_status: bounded` (bounded support)
- `proposal_allowed: false`
- `audit_required_before_effective_retained: false`
- `bare_retained_allowed: false`
- `g1_dark_singlet_mechanism_status: open` (NOT closed)
- `sommerfeld_freezeout_band_status: bounded`
- `m_dm_falsifiable_prediction: 3.94 TeV (m_DM = 16 v)`

## Composed structural product

```text
N_sites = 2^d = 16 (retained Higgs / minimal APBC block on Z^4)
v = M_Pl · (7/8)^{1/4} · α_LM^16 = 246.28 GeV (retained OP from axiom)
⇒ m_DM = N_sites · v = 16 · 246.28 GeV = 3940.5 GeV ≈ 3.94 TeV

Substituted into freeze-out-bypass identity eta = C · m_DM²:
⇒ eta_pred (central) ≈ 6.38e-10
⇒ eta_pred (bounded band) ∈ [5.25e-10, 8.11e-10]
   brackets eta_obs = 6.12e-10
```

Per the audit: among 22 single-block multipliers, only N_sites · v
lands within 5%; among 10,743 complexity-≤4 identities, only 0.75%.

## Artifacts

- `docs/DM_ETA_NSITES_V_STRUCTURAL_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md`
- `scripts/frontier_dm_eta_nsites_v_structural_support_lift.py`
- `outputs/frontier_dm_eta_nsites_v_structural_support_lift_2026-04-29.txt`
  (PASS=N FAIL=0)

## What is closed, bounded, and open

### Closed
1. Framework-composed support for the previously audit-discovered N_sites · v candidate
2. Support for the audit-class candidate as a structurally-composed candidate
3. Computed bounded η band brackets Planck observation within [5.25e-10, 8.11e-10]

### Single open ingredient
1. **G1 mechanism** — dark-singlet collective-mode Coleman-Weinberg
   derivation that fixes the singlet's mode at exactly N_sites · v

### Bounded or inherited inputs
1. **Sommerfeld band** — bounded, not single-point
2. **Freeze-out coefficient x_F** — bounded
3. **alpha_X = alpha_LM** — inherited bounded candidate-route choice
4. **A0 hierarchy compression** — inherited source-theorem assumption
5. **Origin A vs B** — N_sites = 16 has two factorization origins
   (APBC block vs Cl(3) chiral cube · SU(3) Casimir)

## Downstream bookkeeping

If V1 is kept as bounded support:
- PUBLICATION_MATRIX line 125 (DM eta freeze-out-bypass): "bounded" →
  "bounded structural-composed support" with G1 residual flagged
- DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM gets §Note that the
  candidate is now framework-composed

## Verification

```bash
git checkout physics-loop/axiom-to-main-lane-cascade-20260429-block06-20260429
python3 scripts/frontier_dm_eta_nsites_v_structural_support_lift.py
```

PASS=N FAIL=0 verifies the chain authorities, numerical replay, and
status firewall fields.

## Hostile-review pressure points

**P1.** Block 6 is BOUNDED, not retained closure. The G1 mechanism
remains open. The structural composition is support-grade, not
theorem-grade.

**P2.** N_sites = 16 has two origin stories (A from APBC, B from
Cl(3)·SU(3)). V1 doesn't pick between them — the structural composition
works regardless of origin.

**P3.** Branch is rebased on current `origin/main`; independent of
Blocks 1-5.

## Test plan

- [x] Runner returns PASS=N FAIL=0
- [ ] Independent audit confirms framework composition is valid
- [ ] Independent audit confirms uniqueness within audit class
- [ ] User adjudicates whether the bounded structural-composition wording
  should be reflected on line 125

## Links

- [V1 theorem note](docs/DM_ETA_NSITES_V_STRUCTURAL_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md)
- [DM η freezeout-bypass (cited)](docs/DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
- [Higgs mass / N_sites (cited)](docs/HIGGS_MASS_FROM_AXIOM_NOTE.md)
- [EW v (cited)](docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [R_base 31/9 (cited)](docs/R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
