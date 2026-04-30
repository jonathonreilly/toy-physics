# [physics-loop] axiom-to-main-lane-cascade-20260429 block 01: Koide Q OP-Locality Source-Domain Closure (proposed_retained)

## Summary

This block proposes a `proposed_retained` author proposal lifting the
charged-lepton Koide `Q = 2/3` closure from V4's defended hypothesis /
V7.3's conditional corollary to a structural unconditional theorem on
the `A_min` axiom surface, by composing five already-retained
authorities into a single axiom-to-readout chain.

The structural new piece is the argument that OP Theorem 2's
source-domain restriction to `span{P_x}` is forced (not chosen) on the
accepted one-axiom Hilbert/locality/information substrate, via
`PHYSICAL_LATTICE_NECESSITY_NOTE` §9.

## Status (per skill firewall fields)

- `actual_current_surface_status: proposed_retained`
- `proposal_allowed: true`
- `audit_required_before_effective_retained: true` (independent audit
  remains required before the repo treats this as effective retained)
- `bare_retained_allowed: false`

## Artifacts

- `docs/KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md`
  — V8 theorem note + structural argument
- `scripts/frontier_koide_q_op_locality_source_domain_closure.py`
  — runner audits 5 retained authorities from disk + algebraic identities
- `outputs/frontier_koide_q_op_locality_source_domain_closure_2026-04-29.txt`
  — paired output log; `PASS=29 FAIL=0`
- `.claude/science/physics-loops/axiom-to-main-lane-cascade-20260429/`
  — loop pack (GOAL, STATE, OPPORTUNITY_QUEUE, ASSUMPTIONS_AND_IMPORTS,
    NO_GO_LEDGER, ROUTE_PORTFOLIO, ARTIFACT_PLAN, HANDOFF,
    CLAIM_STATUS_CERTIFICATE)

## The chain (from A_min to Q = 2/3)

```text
A_min + accepted one-axiom Hilbert/locality/info substrate
   ⇒ "local" is structural, not a parameterization choice
     (PHYSICAL_LATTICE_NECESSITY §9)
OP Theorem 1 + Theorem 2
   ⇒ unique additive CPT-even scalar generator W = log|det(D+J)|
     has source domain span{P_x} for LOCAL scalar observables
ONSITE no-go
   ⇒ Z ∉ span{P_x} (Z has cross-site entries via cyclic shift R)
Canonical-descent Theorem 1
   ⇒ unique trace-preserving local descent of any K = sI + zZ ∈ A
     to span{I} is E_loc(K) = (s − z/3) I
CRIT
   ⇒ on the admitted normalized reduced carrier, E_loc kills the
     reduced traceless coordinate z; hence Y = I_2; hence Q = 2/3.
```

## Verification

```bash
git checkout physics-loop/axiom-to-main-lane-cascade-20260429-block01-20260429
python3 scripts/frontier_koide_q_op_locality_source_domain_closure.py
```

Expected: `PASS=29, FAIL=0`. Verifies:

- 5 retained authorities present on disk with load-bearing clauses;
- `Tr(Z_3D) = -1`;
- `E_loc(sI + zZ) = (s − z/3) I` (sympy);
- `Q(z) = 2/(3(1+z))` (sympy);
- `Q(0) = 2/3` (sympy);
- forbidden imports (`m_e`, `m_mu`, `m_tau`, `Q_obs`) not used as
  proof inputs;
- status firewall fields present in V8 note.

## Imports retired / exposed

**Retired (proposed):**
- charged-lepton observed `m_e`, `m_mu`, `m_tau` as load-bearing inputs
  for the `Q = 2/3` closure (still useful as comparators);
- `Q_obs ≈ 2/3` as load-bearing observation (still useful as comparator).

**Exposed (newly load-bearing on the V8 chain):**
- `PHYSICAL_LATTICE_NECESSITY_NOTE` §9 substrate-necessity clause —
  was already retained, but V8 promotes its role from "support note"
  to "load-bearing for V8 closure";
- the strict-reading inference (V8 §1.2) — V8 promotes from
  "interpretive" to "structural argument from OP T1 uniqueness +
  PHYSICAL_LATTICE_NECESSITY §9".

## Hostile-review pressure points (acknowledged)

**P1.** Strict-vs-loose reading at the inference layer. V8 §1.2 argues
that the strict reading is forced because non-local source-derivatives
do not produce local scalar observables on the substrate. This argument
is the load-bearing structural new piece. Independent audit should
verify it is sound; if it is judged to remain interpretive, the V8
status should be downgraded to `support` (V4 framing) or the chain
revised.

**P2.** The derivation chain promotes the dimensionless Koide Q to
proposed_retained, but does NOT yet address δ = 2/9 (Block 2 target),
the Brannen phase, the overall lepton scale `v_0`, or the down-type
quark cross-sector (Block 3 target).

**P3.** Branch is rebased on current `origin/main`
(`17789d49 audit: normalize replayed sweep surfaces`); no unrelated
packages touched.

## Cascade unlocked (proposed for later weaving)

If V8 is audit-ratified, the following PUBLICATION_MATRIX rows can be
proposed for promotion at the later integration step:

- line 192 (charged-lepton Koide bridge package): Q residual lifted
  from open to retained corollary
- line 166 (charged-lepton Koide support package Q=2/3, δ=2/9):
  Q half promotable
- line 167 (Q OP source-domain canonical descent): "does not prove"
  → "proves under structural strict reading"
- line 168 (Q SO(2) phase erasure support): role unchanged
- lines 158–162 (5 CKM Koide-bridge support rows): "no Koide closure"
  qualifier removable for Q
- line 157 (cross-sector Koide/CKM V_cb bridge): Q half landed

Total: 9 publication-matrix rows.

## Test plan

- [x] `python3 scripts/frontier_koide_q_op_locality_source_domain_closure.py`
  returns PASS=29 FAIL=0
- [ ] Independent audit confirms strict-reading inference (V8 §1.2) is
  structurally sound on the A_min surface
- [ ] Independent audit confirms each of 5 cited retained authorities
  carries the load-bearing clause as quoted in V8
- [ ] Reviewer adjudicates the 9-row cascade proposal at the later
  weaving step

## Links

- [V8 theorem note](docs/KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md)
- [V4 support note (cited)](docs/KOIDE_Q_OP_UNIQUENESS_SOURCE_DOMAIN_SUPPORT_NOTE_2026-04-25.md)
- [Canonical-descent T1 (cited)](docs/KOIDE_Q_SOURCE_DOMAIN_CANONICAL_DESCENT_THEOREM_NOTE_2026-04-25.md)
- [CRIT (cited)](docs/KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md)
- [ONSITE no-go (cited)](docs/KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md)
- [OP from axiom (cited)](docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY (cited)](docs/PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [Loop handoff](.claude/science/physics-loops/axiom-to-main-lane-cascade-20260429/HANDOFF.md)
- [Block claim certificate](.claude/science/physics-loops/axiom-to-main-lane-cascade-20260429/CLAIM_STATUS_CERTIFICATE.md)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
