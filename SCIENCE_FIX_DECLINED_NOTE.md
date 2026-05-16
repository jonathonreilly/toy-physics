# science-fix declined: newton_law_derived_note

**Claim id:** `newton_law_derived_note`
**Source note:** `docs/NEWTON_LAW_DERIVED_NOTE.md`
**Runner:** `scripts/frontier_distance_law_definitive.py`
**Date:** 2026-05-16
**Decision:** decline — the auditor's `audited_conditional` verdict is faithful, the note hash and runner hash are unchanged since the audit, and the auditor-named "missing bridge" is the substantive `L^{-1} = G_0` derivation from the Cl(3)-on-Z^3 axiom that the source note's retained upstream dep itself explicitly identifies as the open D-row gap. Attempting to discharge it inside a 30-minute science-fix budget would either churn (re-state what the note already says) or overclaim (sneak unratified non-retained imports into the retained tier).

## What the PROMPT.md targets

- `audit_status`: `audited_conditional`
- `effective_status`: `audited_conditional`
- `claim_type`: `bounded_theorem`
- `load_bearing_step_class`: A
- `category`: `audited_conditional_missing_bridge_theorem`
- `transitive_descendants`: 779
- `deps`: `['gravity_full_self_consistency_note']`
- Auditor `verdict_rationale`: "Issue: the Newton-law derivation rests on two bounded admissions, especially BA-1, the lattice Poisson equation as the equation of motion. Why this blocks: the cited gravity self-consistency dependency is retained only as a conditional algebraic implication under a stipulated closure identity, so it does not derive BA-1 from the framework axiom. Repair target: provide a retained bridge theorem deriving BA-1 from Cl(3) on Z^3, and pin the BA-2 lattice Green's-function asymptotic as an accepted/retained mathematical input. Claim boundary until fixed: given BA-1 and BA-2, the class-A inverse-square/product-law derivation and finite-lattice runner support may be cited, but not an unconditional Newton-law derivation from the framework baseline."

## Why decline is the right call

### 1. The audit verdict is internally faithful, not a scope error

The auditor read the note correctly. The source note (`docs/NEWTON_LAW_DERIVED_NOTE.md`) already declares its `claim_type` as `bounded_theorem` and opens with the explicit statement:

> A prior independent audit of the unconditional framing found that the load-bearing Poisson equation was supported only by a cited authority itself conditional on a stipulated `L^{-1}=G_0` closure identity. This scope narrowing implements that audit's repair target: narrow the note to a bounded theorem conditional on the Poisson equation.

The note's §"Bounded admissions" enumerates the only two admissions — (BA-1) lattice Poisson as equation of motion, conditional on the `L^{-1} = G_0` closure supplied by `GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`; and (BA-2) the Maradudin et al. 1971 lattice Green's-function asymptotic, admitted as textbook math input. The §"Theorem / Claim (conditional on BA-1 and BA-2)" body, the §"What Is Actually Proved", and the §"What Remains Open" sections all keep the conditional framing.

`audited_conditional` is not a complaint that the note made false claims; it is a faithful record that the note's claim scope (conditional on BA-1 + BA-2) does not propagate to an unconditional Newton-law derivation from the framework baseline. The note already tells that truth in its own opening, theorem statement, and "What Remains Open" sections, and the "claim boundary until fixed" the auditor specifies ("given BA-1 and BA-2, the class-A inverse-square/product-law derivation and finite-lattice runner support may be cited, but not an unconditional Newton-law derivation from the framework baseline") is precisely the boundary the source note already enforces.

### 2. The auditor-named "missing bridge" is the explicit open D-row gap of the retained upstream dep

The single upstream dep `gravity_full_self_consistency_note` is `effective_status = retained_bounded`, `claim_type = bounded_theorem`, `chain_closes = true`, audited by `codex-audit-loop` on 2026-05-10. Its audited claim scope:

> Conditional algebraic implication that, if `G_0 = H^{-1}` and the stipulated closure identity `L^{-1} = G_0` hold, then `L = H = -Delta_lat`.

Its `chain_closure_explanation` is explicit:

> Within the stated conditional scope, the conclusion follows by inversion of the stipulated identity together with the definition `G_0 = H^{-1}`. The note does not claim, and this audit does not validate, a derivation of `L^{-1} = G_0` from the Cl(3)-on-Z^3 axiom.

Its `notes_for_re_audit_if_any` instructs second auditors to:

> verify that downstream citations preserve the bounded conditional scope and do not treat this row as deriving `L^{-1} = G_0` from A1.

And the dep's own §"What Remains Open" in `docs/GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md` says it directly:

> The hypothesis A2 (`L^{-1} = G_0`) is **stipulated**, not derived from A1 in this note. The audit verdict explicitly identifies the open derivation gap as: **a retained bridge theorem deriving `L^{-1} = G_0` from the Cl(3) on Z^3 axiom rather than identifying it by closure**. ... A retained bridge theorem closing this gap is the open D-row deliverable for this row.

The repair target the newton_law_derived_note auditor requests — "provide a retained bridge theorem deriving BA-1 from Cl(3) on Z^3" — is therefore the *exact same open D-row deliverable* that the retained upstream dep enumerates as its open work. It is not a packaging gap that can be folded inside the newton_law_derived_note row. It is the substantive bridge theorem that the gravity bundle itself has thoroughly named and characterized.

### 3. The note hash and runner hash are unchanged since the audit

- Ledger `note_hash`: `5e0781d773a9b3d0472977bed4cfb71d6b5c30d5a7c60f68b13cef446c72b16e`
- Local `sha256(docs/NEWTON_LAW_DERIVED_NOTE.md)`: `5e0781d773a9b3d0472977bed4cfb71d6b5c30d5a7c60f68b13cef446c72b16e`
- Ledger `audit_state_snapshot.runner_hash`: `f8f86ac9104aac9acfd1d446d48a8c96dcb88ad461f5bd684da1a4631ed1e554`
- Local `sha256(scripts/frontier_distance_law_definitive.py)`: `f8f86ac9104aac9acfd1d446d48a8c96dcb88ad461f5bd684da1a4631ed1e554`
- `logs/runner-cache/frontier_distance_law_definitive.txt` records exit_code 0, the same `runner_sha256`, and the finite-lattice 31^3..96^3 sweep reporting force exponent = -2.0010 +/- 0.0042 with the "SAFE CLAIMS" closeout block preserved.

No facts on the ground have drifted; the audit is operating on the same artifacts it saw on 2026-05-11. Re-audit on the same artifacts will return the same `audited_conditional` verdict; that is by construction.

### 4. A 30-minute science-fix attempt would land in the failure modes my prior runs explicitly flag

Memory directives that apply here:

- "Consistency equality is not derivation" — gauge-dimension equalities and numerical coincidences cannot load-bear retained closure; the runner must derive, not hard-code, the closure value. Pinning `L = -Delta_lat` by re-stipulating `L^{-1} = G_0` is consistency equality, not derivation.
- "Bridge gap = action-form derivation, not engineering" — the open path is "derive-the-action", not industrial SDP or algebraic relabeling. BA-1 is precisely the equation-of-motion form of a staggered scalar action that is currently admitted, not derived from Cl(3) on Z^3.
- "Retained-tier purity + package wiring" — N-way retained equalities cannot include support-tier routes; new retained theorems must wire into all canonical harness + publication control-plane indexes.
- "'New primitives' = derivations, not axioms" — user-authorized 'new primitives' means derivations from A1 + A2 + retained, NOT new axioms or imports. Re-introducing the closure identity as an axiom would be an import, not a derivation.
- "Physics-loop late-campaign corollary churn" — one-step relabelings of an already-landed conditional packet are churn even if technically correct.

A within-budget attempt at the auditor's repair target would have to either (a) supply a retained bridge theorem deriving the staggered-scalar lattice Poisson equation of motion from the Cl(3)-on-Z^3 axiom, which is the open D-row gap the retained upstream dep itself names and which the broader gravity bundle (see `docs/GRAVITY_SUB_BUNDLE_NOTE.md` Tier 1a entry referenced in `gravity_full_self_consistency_note`) marks as the deliverable required to upgrade Tier 1a beyond bounded; or (b) admit a new boundary-physics primitive (the closure identification, or a stipulated staggered-scalar action) and pretend it is retained. (a) is not a 30-minute job and is not algebraic-bridge work — it is action-form derivation. (b) is overclaiming.

### 5. The note already implements every non-bridge repair on the auditor's repair-target list

The auditor names three repair levers: (i) a retained bridge for BA-1; (ii) pinning BA-2 as accepted/retained math input; (iii) narrowing the claim scope to "given BA-1 and BA-2, the class-A inverse-square/product-law derivation and finite-lattice runner support may be cited, but not an unconditional Newton-law derivation from the framework baseline".

(iii) is already done verbatim: the note's title bracket, status header, §"Bounded admissions", theorem statement "Given (BA-1) and (BA-2)", §"What Is Actually Proved", §"What Remains Open", and §"How This Can Be Used" all carry exactly that boundary.

(ii) is already done at source-level: the note labels (BA-2) as "Standard result of lattice potential theory (Maradudin, Montroll, Weiss, *Theory of Lattice Dynamics in the Harmonic Approximation*, 1971); admitted as a textbook math input rather than derived in this note." Promoting BA-2 to a separately-audited retained math-input row is independent ledger plumbing, not an algebraic bridge, and would not change the audited-conditional status of this row because BA-1 (not BA-2) is the load-bearing residual the verdict flags.

(i) is the open D-row gap covered in §2 above.

There is no additional narrow / re-label / dep-edit that is both within budget and not already in the note.

## What this PR contains

Only this `SCIENCE_FIX_DECLINED_NOTE.md` at the worktree root. No edits to:

- the source note `docs/NEWTON_LAW_DERIVED_NOTE.md`
- the runner `scripts/frontier_distance_law_definitive.py`
- `logs/runner-cache/frontier_distance_law_definitive.txt`
- the upstream dep `docs/GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md`
- any file under `docs/audit/`, `docs/publication/`, or other ledger / pipeline indices

Per the science-fix rules, this PR is intended for review, not for landing changes to the audit or publication control planes.

## Recommended downstream

- Re-audit on the same artifacts will return the same `audited_conditional` verdict; that is by construction. The auditor and the source note already agree the chain is conditional on BA-1 + BA-2.
- The real next step is directed bridge work on the open D-row gap, tracked through the gravity bundle (`docs/GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md` §"What Remains Open", and the Tier-1a entry it references in `docs/GRAVITY_SUB_BUNDLE_NOTE.md`): a retained bridge theorem deriving `L^{-1} = G_0` from the Cl(3)-on-Z^3 axiom, i.e. an action-form derivation of the staggered-scalar lattice Poisson equation of motion. That is a research-level deliverable, not a 30-minute algebraic-bridge science-fix.
- Until that bridge lands, `audited_conditional` is the correct retained status for this row, and the source note's already-narrowed scope is the correct claim boundary.

## SCIENCE_FIX_DECLINED
