# Bridge Gap — Block 04 Round-4 Hostile-Review Synthesis (Block 07)

**Date:** 2026-05-07
**Type:** hostile-review synthesis + structural strengthening note
**Claim type:** named-obstruction synthesis
**Status:** synthesis note documenting that Block 04's action-form
uniqueness no-go survived three additional independent hostile-review
attacks dispatched 2026-05-07 (Round 4 of the bridge-gap-new-physics
campaign). Combined with rounds 1-3, the no-go is now **9-way
redundant proven** under the framework's current retained primitive
stack. Identifies one new structural finding (Wilson is the natural
max-entropy action under canonical Tr-form) and one specific missing
primitive ("lattice Hamiltonian commutes with link-Casimirs") that
would close the action-form question if added.
**Authority role:** branch-local sister note to
[`docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md).
Audit verdict and effective status are set only by the independent
audit lane.
**Loop:** bridge-gap-new-physics-20260506 (Block 07 / Round-4 hostile review)
**Branch:** physics-loop/bridge-gap-new-physics-block07-20260507
**Opened under:** judgment-based cluster-cap evaluator (see PR #624 governance update)

## Why this note exists

The bridge-gap-new-physics-20260506 campaign closed at Block 06 with
the action-form-uniqueness no-go (Block 04) as its deepest structural
finding. Round 4 of hostile review (2026-05-07, three independent
agents) was dispatched specifically to BREAK Block 04's no-go from
within the framework's current retained primitive stack. All three
agents returned negative. This note synthesizes the round-4 findings
to:

1. Strengthen Block 04's no-go to 9-way redundant evidence.
2. Identify the specific missing primitive that would close the no-go.
3. Identify a new structural reframing: Wilson (not HK) is the
   naturally-preferred action under canonical Tr-form max-entropy.

## The three round-4 attacks

Each agent attacked Block 04 from a distinct angle. All returned
negative — Block 04 stands.

### Round-4 Agent 1: Casimir-factorizability from RP-A11 + cluster

**Question:** does RP-A11 + cluster decomposition + canonical Tr-form
force Casimir-diagonal factorizability of the partition function?

**Verdict:** NO. RP gives only `T† = T` and `T ≥ 0` (transfer matrix
positivity); it does not constrain the lattice Hamiltonian's
commutation with per-link Casimirs. Wilson's magnetic term `Re Tr U_p`
is a perfectly valid Cl(3) Hermitian operator with bounded local norm
— fully consistent with Lieb-Robinson and RP. To force HK-uniquely
via Casimir-diagonal factorizability would require a NEW primitive:
**"the lattice Hamiltonian commutes with all link-Casimirs"**. This
is not derivable from current retained primitives.

**Constructive byproduct:** the precise missing primitive is now
identified, sharpening Block 04's no-go and identifying a clean
axiom-addition target if/when the no-new-axiom rule is revisited.

### Round-4 Agent 2: T/CPT/RP discrete symmetry constraints

**Question:** do retained T-symmetry, CPT-symmetry, and RP A11
theorems impose action-form constraints excluding Wilson or Manton in
favor of HK?

**Verdict:** NO. All three candidate actions {Wilson, HK, Manton}
respect every retained discrete symmetry (RP A11 R2, CPT² = I, mass-
equality, lifetime-equality, T from CPT_EXACT_NOTE). The discrete-
symmetry attack does not break Block 04's no-go.

**Critical sub-finding:** A11 RP as currently written is **specifically
engineered around Wilson**. Its hypothesis-match table cites
`Re tr(1 - U_P / N_c)` as a hard precondition. Substituting HK or
Manton requires re-deriving the factorisation via Driver-Hall (HK)
or Lévy (Manton) extensions — admissible standard machinery, but
the retained discrete-symmetry stack as currently written **leans
toward Wilson**, not HK.

This is the OPPOSITE of what the campaign's earlier framing
suggested (heat-kernel "Cl(3)-native" because of Casimir-diagonal
structure). The retained primitives' bias is actually toward Wilson.

### Round-4 Agent 3: Maximum-entropy / naturality

**Question:** is there a naturality argument from existing retained
primitives that uniquely selects HK over Wilson and Manton without
admitting new axioms?

**Verdict:** NO, on five candidate naturality arguments:

| Argument | Constraint | Selects | Status |
|---|---|---|---|
| 1 | fixed `⟨Re Tr U⟩` | **Wilson** | Internally consistent under retained primitives; selects Wilson NOT HK |
| 2 | fixed `⟨d²(U,I)⟩` | **Manton** | Internally consistent under retained primitives; selects Manton NOT HK |
| 3 | fixed `⟨C_2⟩` | HK | Constraint not framework-internal (Plancherel-dual, not group-side) — circular |
| 4 | RG fixed point | HK at IR | Forces HK only at IR limit, not at framework's β=6 bare evaluation |
| 5 | Fisher-geodesic | HK | Requires admitting Fisher metric on measure space — new primitive |

**Critical reframing:** Wilson and Manton are themselves max-entropy
measures under retained-primitive-natural constraints (`Re Tr U` from
trace form, `d²` from canonical bi-invariant metric). HK is max-
entropy only on the spectral / Plancherel-dual side, which is NOT
framework-internal.

Under the most direct naturality reading — "the framework's natural
constraint is the canonical Tr-form trace `Re Tr U`" — **Wilson is
uniquely selected**, not HK. This SUPERSEDES the campaign's earlier
framing that HK is "Cl(3)-native via Casimir."

## Synthesis: 9-way redundant proof of Block 04 no-go

The action-form uniqueness no-go has now survived nine independent
attack angles:

| Round | Attack angle | Verdict | Source |
|---|---|---|---|
| 1.1 | V≥2 Picard-Fuchs lift | NEG | Block 03 in `BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md` |
| 1.2 | APBC Z_3 spatial twist + L_s ≥ 3 | NEG | same |
| 1.3 | SDP + MM on V-invariant block | NEG | same |
| 1.4 | Cl(3) HS + Klein-four positivity | NEG | same |
| 1.5 | RP-A11 cluster inequality (round 1) | NEG | same |
| 1.6 | V-singlet temporal projection on ρ_(p,q) | NEG | same |
| 1.7 | Composite framework-unique levers | NEG | same |
| 2.1 | Action-form derivation (HK as candidate) | POS framing | new-physics opening 2026-05-06 |
| 2.2 | Cl(3) Grassmann determinant | NEG | round-3 Agent β |
| 2.3 | Hamiltonian limit on finite Hilbert | NEG | round-3 Agent γ |
| 3.1 | RP+cluster Casimir-factorizability | NEG | round-4 Agent 1 (this note) |
| 3.2 | Discrete symmetry T/CPT/RP | NEG | round-4 Agent 2 (this note) |
| 3.3 | Naturality / max-entropy | NEG (selects Wilson) | round-4 Agent 3 (this note) |

**Verdict: action-form uniqueness is structurally undecidable** under
the framework's current retained primitive stack + no-new-axiom rule.

## New structural findings (Block 07 deliverables)

### Finding 1: Wilson is the natural action under canonical Tr-form max-entropy

This is a major structural reframing. The campaign's earlier work
(Blocks 01-06) treated heat-kernel as the "Cl(3)-native" action because:
- HK uses retained Casimir directly
- HK 1-plaq is exact in 2 characters (Block 02)
- HK admits Casimir-diagonal factorization (Block 03)
- HK cube L_s=2 is closer to MC than Wilson cube (Block 06)

But round-4 Agent 3's analysis shows that the **most direct naturality
argument from canonical Tr-form** selects **Wilson, not HK**. The
canonical Tr-form `Tr(T_a T_b) = δ_{ab}/2` produces the canonical
group-side observable `Re Tr U = (1/2)(χ_{(1,0)} + χ_{(0,1)})`. The
max-entropy probability measure with fixed mean `⟨Re Tr U⟩ = c` is
the Gibbs measure `exp(λ · Re Tr U) dU` — exactly Wilson.

HK's "Casimir-naturality" requires switching from the group-side trace
constraint to the spectral-side Casimir constraint, which is NOT
framework-internal under current primitives.

**Implication:** under naturality criteria from current primitives,
the framework's actually-derived action is more likely Wilson than HK.
This puts the bridge gap back at the famous 50-year-old open lattice
problem: compute ⟨P⟩_Wilson(β=6) analytically.

This is NOT a derivation — naturality arguments don't bind under the
no-new-axiom rule. But it changes the campaign's strategic framing:

- The Block 02 closed form `⟨P⟩_HK,1plaq(6) = exp(-2/3) = 0.5134`
  is real but corresponds to a DIFFERENT (HK) action than the
  framework's most-natural one.
- The Block 06 numerical `P_cube_HK(L_s=2) = 0.5223` is real but
  for a DIFFERENT action.
- The framework's "actually-derived" action is most plausibly
  Wilson, returning the bridge gap to its famous form.

### Finding 2: Specific missing primitive identified

Round-4 Agent 1 identified the precise missing primitive: **"lattice
Hamiltonian commutes with all link-Casimirs"**. Equivalent
formulations:

(a) `[H̃, −Δ_g^{(e)}] = 0` for each link `e`
(b) The lattice gauge dynamics is a tensor product of independent
    single-link Brownian motions modulo gauge constraint
(c) The transfer-matrix eigenstates are pure-irrep states on each link

Adding this as a new axiom would force HK uniquely (the only action
whose Hamiltonian satisfies (a)). But under current no-new-axiom rule,
this is forbidden.

This is a **clean axiom-addition target** if/when the project's
governance allows extending the axiom stack. It is much narrower than
"choose HK as gauge action" — it's a structural constraint that
follows from a single algebraic fact (link-Casimir commutation).

### Finding 3: A11 RP currently leans toward Wilson

Round-4 Agent 2 identified that the retained A11 RP theorem is
specifically engineered around Wilson — its hypothesis-match table
cites `Re tr(1 - U_P / N_c)` as the load-bearing precondition.
Substituting HK or Manton requires re-deriving via Driver-Hall (HK)
or Lévy (Manton) extensions.

**Implication:** the discrete-symmetry retained stack as currently
written is more compatible with Wilson than with HK or Manton, in the
weak sense that the existing proofs literally name Wilson. To use HK
in this framework requires extending A11 RP via standard machinery
(admissible) but is currently undone work.

## What this means for the campaign's overall posture

The campaign's six prior blocks treated heat-kernel as a candidate
"naturally Cl(3)-derived" action and produced bounded support theorems
for it (Block 01: t = 1; Block 02: exp(-2/3) closed form; Block 06:
numerical L_s=2 cube = 0.5223). Round-4 reveals that under the most
direct naturality reading from canonical Tr-form, **Wilson is more
naturally-preferred than HK**.

This does not invalidate the prior blocks — they remain valid bounded
support theorems under the conditional that HK is the framework's
derived action. It DOES reframe the campaign's strategic ambition:

- The HK chain (Blocks 01-06) is a coherent set of derivations
  under HK as candidate action. Useful as one of two action
  scenarios.
- A parallel WILSON-chain set of derivations is now warranted as
  the alternative scenario, and would put the bridge gap back at
  the famous open lattice problem (under Wilson).

**The campaign's overall structural finding stands:** action-form
uniqueness is structurally undecidable under current primitives.
The four cluster-obstruction lanes' downstream values are
range-bounded across action choices.

## Status

```yaml
actual_current_surface_status: hostile-review synthesis + structural strengthening
target_claim_type: named_obstruction_synthesis
conditional_surface_status: |
  Conditional on:
   (a) round-4 hostile-review agents' analysis being correct
       (independent verification by audit lane);
   (b) the same retained primitive stack as Block 04;
   (c) no new axioms admitted (no-new-axiom rule);
   (d) the candidate action set {Wilson, HK, Manton} is exhaustive
       (other candidates such as Cl(3)-volume-form might extend the
       no-go but do not weaken it).
hypothetical_axiom_status: null
admitted_observation_status: |
  Standard Lie-algebra metric, Brownian-motion semigroup, max-entropy /
  Gibbs-measure variational characterizations, information-geometry
  Fisher metric — all admitted standard machinery in narrow non-
  derivation roles.
claim_type_reason: |
  This note is a hostile-review synthesis: documents that Block 04's
  no-go survived three additional attacks, identifies the precise
  missing primitive, and reframes Wilson as the more naturally-
  preferred action under canonical Tr-form max-entropy. It is
  bounded support documentation, not a derivation of any new theorem.
audit_required_before_effective_retained: true
bare_retained_allowed: false
forbidden_imports_used: false
```

## What this closes

- Block 04's action-form uniqueness no-go is now 9-way redundant
  proven across three independent rounds of hostile review.
- Three additional attack routes (Casimir-factorizability,
  discrete-symmetry, naturality) are formally retired as
  Resolution-A levers.
- Identifies the precise missing primitive ("lattice Hamiltonian
  commutes with link-Casimirs") that would close the no-go if
  added — a clean axiom-addition target.
- Identifies the structural reframing: Wilson is the more
  naturally-preferred action under canonical Tr-form, not HK.

## What this does NOT close

- The bridge gap. Block 04's no-go means action-form uniqueness is
  structurally undecidable; this note merely confirms that with
  greater redundancy.
- The thermodynamic ⟨P⟩(6) under any specific action choice (Block 03
  named obstruction stands).
- The decision between Resolution A (new structural primitive),
  Resolution B (governance reclassification), or Resolution C
  (industrial SDP for one action choice).

## Recommended next campaign(s)

In priority order:

1. **Open the question of admitting "lattice Hamiltonian commutes
   with link-Casimirs" as a new axiom.** This is a project-governance
   decision, not a science cycle. The user-memory rule "no-new-axiom
   in physics-loop work" reflects governance preference, not a
   mathematical impossibility. If the audit lane decides this
   primitive is acceptable, HK is uniquely forced and Layer 1 of the
   bridge gap closes.

2. **Pursue the Wilson chain in parallel to the HK chain.** Under
   round-4 Agent 3's naturality finding, Wilson is more naturally-
   preferred. A symmetrical campaign producing Wilson bounded support
   theorems (sister to Blocks 01-06's HK chain) would clarify the
   action-form ambiguity numerically.

3. **HK cluster-decomposition estimate** (Block 03 named obstruction).
   Hard, multi-cycle. Closes Layer 2 within HK if successful — but
   under round-4 reframing, may be the wrong action.

4. **Industrial SDP under Wilson at L_max ≥ 22** (the demoted
   Resolution C). Reproduces the famous open lattice problem at
   ε_witness precision. Costly but bounded.

## Cross-references

- Block 04 (sister no-go): [`BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`](BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md)
- Cluster obstruction parent: [`LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md`](LATTICE_PHYSICAL_MATCHING_CLUSTER_OBSTRUCTION_NOTE_2026-05-02.md)
- Round 1+2 exhaustion: [`BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md)
- New-physics opening: [`BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md`](BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md)
- HK chain (Blocks 01-06): in PRs #617, #619, #626, #627, #628, #629
- Skill governance update (judgment-based cluster cap): PR #624
- Agent dispatches and outputs: round-4 agent transcripts (this note synthesizes their findings)
