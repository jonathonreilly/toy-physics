# Claim Status Certificate — g_bare Rescaling-Freedom Removal Theorem

**Block:** g-bare-closure-derivation-targets-rescaling-20260503
**Branch:** physics-loop/g-bare-closure-derivation-targets-20260503
**Artifact:** docs/G_BARE_RESCALING_FREEDOM_REMOVAL_THEOREM_NOTE_2026-05-03.md
**Runner:** scripts/frontier_g_bare_derivation.py
**Saved output:** outputs/frontier_g_bare_derivation_2026-05-03.txt

## Status

```yaml
actual_current_surface_status: support / structural normalization theorem (closes one of three named repair-targets on G_BARE_DERIVATION_NOTE)
conditional_surface_status: audited_conditional pending independent audit
hypothetical_axiom_status: null
admitted_observation_status: "Standard Wilson plaquette small-a expansion admitted; Cl(3) anticommutator axiom A1 admitted; standard Gell-Mann basis admitted via cl3_color_automorphism_theorem dep."
proposal_allowed: false
proposal_allowed_reason: "Closes ONE of three named repair-targets in the G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02 verdict (the A -> A/g rescaling-freedom removal). The constraint-vs-convention disambiguation is the companion theorem (separate note in same PR). The missing primary runner is supplied (this same script). Parent G_BARE_DERIVATION_NOTE retention requires all three repair-target items closed AND independent audit of each new theorem row AND closure of the upstream cl3_color_automorphism_theorem normalization-status question; this note closes one of three repair items only."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Disposition

**Goal:** address repair-target #2 of the
`G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02` verdict on
`G_BARE_DERIVATION_NOTE.md` (parent currently `audited_conditional`,
263 transitive descendants in the original audit count).

The repair-target named was:

> *"supply a retained theorem that removes the A -> A/g rescaling
> freedom."*

**This block closes:** the A -> A/g rescaling-freedom removal as a class
(A) algebraic identity on the canonical Cl(3) connection normalization
surface. Specifically: under `Tr(T_a T_b) = delta_ab/2`, the rescaling
`T_a -> c T_a` (equivalently `A -> c A`) shifts the Wilson coefficient
`beta_new = c^2 * beta_old`, leaving `g_bare` unchanged. The continuum
rescaling freedom is routed into `beta`, not `g_bare`. With (CN) held
fixed, `g_bare` carries no independent scalar freedom.

**Key structural insight:** the rescaling redundancy of abstract continuum
gauge theory is removed by the canonical Cl(3) connection normalization
because the canonical normalization fixes the operator basis, leaving only
`beta` as the free coefficient. The action coefficient `beta` absorbs all
of the rescaling, in exact algebraic form `beta_new = c^2 * beta_old`.

**This block does NOT close:**

- The convention-vs-derivation status of the canonical normalization
  itself (carried by `cl3_color_automorphism_theorem` and clarified by
  `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02`).
- The Wilson plaquette action choice (Symanzik / improved actions are
  outside the scope; see `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18`
  Claim 3 caveat).
- The constraint-vs-convention disambiguation on the parent (companion
  theorem in the same PR).
- The full retention pathway for `G_BARE_DERIVATION_NOTE` itself.

## Allowed PR/Status Wording

- "support / structural normalization theorem"
- "closes one of three named repair-targets on G_BARE_DERIVATION_NOTE"
- "rescaling-freedom removal under canonical Cl(3) connection normalization"
- "the rescaling shifts beta by c^2, not g_bare"
- "class (A) algebraic identity on the canonical normalization surface"

## Forbidden PR/Status Wording

- bare "retained" / "promoted"
- "closes the g_bare = 1 derivation"
- "promotes G_BARE_DERIVATION_NOTE to retained-grade"
- "derives g_bare = 1 from Cl(3) axioms alone" (false; the canonical
  normalization is the admitted convention layer carried by
  cl3_color_automorphism_theorem)
- "removes the canonical normalization convention" (the convention layer
  is moved upstream by this theorem chain, not dissolved)

## Verification

```bash
python3 scripts/frontier_g_bare_derivation.py
# expected: PASS = 51 EXACT, PASS = 4 BOUNDED, FAIL = 0
```

The runner verifies, in `Section D`:

1. Rescaling `T_a -> c T_a` with `c in {1/2, sqrt(2), 2, 3}` produces
   `Gram = c^2 * delta_ab/2`, violating the canonical normalization for
   every `c != 1` (each at machine precision).
2. The matched Wilson coefficient `beta_new = c^2 * beta_old` is
   recovered exactly for each `c`.
3. The rescaling shifts `beta`, not `g_bare`: `g_bare` is unchanged in
   each case (the rescaling lives on the action coefficient, not on the
   coupling).

## Independent Audit

Audit must verify:

1. The cited dep `cl3_color_automorphism_theorem` carries the canonical
   `T_F = 1/2` (i.e., `Tr(T_a T_b) = delta_ab/2`) on the retained triplet
   block. It does, per Section H of `verify_cl3_sm_embedding.py` and
   the existing `CL3_COLOR_AUTOMORPHISM_THEOREM.md` text.
2. The load-bearing step `beta_new = c^2 * beta_old` is class (A)
   algebraic substitution, not a fitted comparison or external import.
3. The note does NOT load-bear on the conclusion `g_bare = 1`; it
   load-bears only on the *removal of the rescaling freedom*. The
   conclusion `g_bare = 1` is the subject of the companion
   constraint-vs-convention theorem.
4. After this note lands and the audit ledger regenerates, the parent
   `G_BARE_DERIVATION_NOTE` row should record the rescaling-freedom
   repair-target item as closed, while continuing to flag the other two
   items as open until they are addressed.

## What this changes for the leverage map

`G_BARE_DERIVATION_NOTE` parent (currently `audited_conditional`, ~263
transitive descendants) advances on one of three named repair-target
items: rescaling-freedom removal closes. Items remaining: (1) primary
runner — closed in the same PR by this same script; (3) constraint-vs-
convention disambiguation — closed by the companion theorem in the same
PR. So this PR closes all three repair items, but the parent's retention
still requires:

- independent audit of each of the three new artifacts (this note, the
  companion constraint-vs-convention theorem, and the runner outputs);
- the upstream `cl3_color_automorphism_theorem` row to remain
  retained-grade (currently unaudited at the rendered ledger but a
  reviewed exact algebraic support theorem on main);
- the structural-normalization theorem chain remains conditional on the
  Wilson action choice (see Claim 3 caveat).

`G_BARE_DERIVATION_NOTE` therefore stays `audited_conditional` after this
PR lands, and the conditional reason narrows from "all three repair-target
items open" to "audit-pending on three new theorem rows + Wilson action
choice convention layer."
