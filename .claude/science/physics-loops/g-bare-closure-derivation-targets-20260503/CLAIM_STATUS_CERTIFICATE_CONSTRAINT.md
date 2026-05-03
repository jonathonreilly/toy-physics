# Claim Status Certificate — g_bare Constraint vs Convention Disambiguation Theorem

**Block:** g-bare-closure-derivation-targets-constraint-20260503
**Branch:** physics-loop/g-bare-closure-derivation-targets-20260503
**Artifact:** docs/G_BARE_CONSTRAINT_VS_CONVENTION_THEOREM_NOTE_2026-05-03.md
**Runner:** scripts/frontier_g_bare_derivation.py
**Saved output:** outputs/frontier_g_bare_derivation_2026-05-03.txt

## Status

```yaml
actual_current_surface_status: support / disambiguation theorem (closes one of three named repair-targets on G_BARE_DERIVATION_NOTE)
conditional_surface_status: audited_conditional pending independent audit
hypothetical_axiom_status: null
admitted_observation_status: "Standard Wilson plaquette small-a expansion admitted; canonical Cl(3) connection normalization Tr(T_a T_b) = delta_ab/2 admitted via rescaling-freedom-removal theorem dep -> cl3_color_automorphism_theorem two-hop chain."
proposal_allowed: false
proposal_allowed_reason: "Closes ONE of three named repair-targets in the G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02 verdict (the constraint-vs-convention disambiguation). The rescaling-freedom-removal is the companion theorem (separate note in same PR). The missing primary runner is supplied (this same script). Parent G_BARE_DERIVATION_NOTE retention requires all three repair-target items closed AND independent audit of each new theorem row AND closure of the upstream cl3_color_automorphism_theorem normalization-status question; this note closes one of three repair items only."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Disposition

**Goal:** address repair-target #3 of the
`G_BARE_DERIVATION_STATUS_CORRECTION_AUDIT_NOTE_2026-05-02` verdict on
`G_BARE_DERIVATION_NOTE.md` (parent currently `audited_conditional`,
263 transitive descendants in the original audit count).

The repair-target named was:

> *"the decisive step identifies the canonical Cl(3) connection
> normalization with unit gauge coupling, while the note explicitly
> leaves open whether that is a constraint or a convention."*

**This block closes:** the constraint-vs-convention ambiguity, by
explicitly disambiguating the two readings:

1. **Convention reading** (already on main): `g_bare = 1` is itself the
   Wilson canonical-normalization convention, classified by
   `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02` as an
   admitted convention.
2. **Constraint reading** (closed by this theorem): with the canonical
   Cl(3) connection normalization `Tr(T_a T_b) = delta_ab/2` carried by
   `cl3_color_automorphism_theorem` treated as the admitted convention
   layer, `g_bare = 1` follows as a structural constraint, not as a
   separate convention. The convention layer lives at the canonical
   normalization, not at `g_bare`.

**Key structural insight:** the parent's "constraint or convention?"
question conflates two distinct convention layers. The framework has
exactly one admitted convention layer in the `g_bare` chain — the
canonical normalization (CN) — and `g_bare = 1` is its derived class
(A) algebraic constraint. Any alternative `g_bare != 1` would either
violate (CN) (case a, forbidden by the rescaling-freedom-removal
companion theorem) or require an external scale that A1 + A2 do not
provide (case b).

**This block does NOT close:**

- The convention-vs-derivation status of (CN) itself. (CN) remains an
  admitted convention layer; promoting it to a derivation would require
  closing the deeper question of whether the canonical Gell-Mann
  normalization is uniquely forced by Cl(3) algebraic structure alone.
- The Wilson plaquette action choice (Symanzik / improved actions are
  outside the scope; see `G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18`
  Claim 3 caveat).
- The deeper question of whether `A4` (the framework's canonical
  normalization axiom) is derivable from `A1 + A2` alone.
- The full retention pathway for `G_BARE_DERIVATION_NOTE` itself.

## Allowed PR/Status Wording

- "support / disambiguation theorem"
- "closes one of three named repair-targets on G_BARE_DERIVATION_NOTE"
- "g_bare = 1 is a constraint relative to the canonical Cl(3)
  normalization"
- "the convention layer lives at the canonical normalization, not at
  g_bare"
- "constraint-vs-convention disambiguation"
- "class (A) algebraic constraint"

## Forbidden PR/Status Wording

- bare "retained" / "promoted"
- "closes the g_bare = 1 derivation"
- "promotes G_BARE_DERIVATION_NOTE to retained-grade"
- "derives g_bare = 1 from Cl(3) axioms alone" (false; the canonical
  normalization is the admitted convention layer carried by
  cl3_color_automorphism_theorem)
- "removes the canonical normalization convention" (the convention layer
  is moved upstream by this theorem chain, not dissolved)
- "settles the convention question" (the upstream convention question on
  (CN) itself is NOT settled here)

## Verification

```bash
python3 scripts/frontier_g_bare_derivation.py
# expected: PASS = 51 EXACT, PASS = 4 BOUNDED, FAIL = 0
```

The runner verifies, in `Section E`:

1. The canonical `beta = 2 N_c = 6` for `SU(3)` is computed exactly via
   `Fraction` arithmetic (no floating-point comparison).
2. The unique `g_bare^2 = 2 N_c / beta = 1` is derived as a class (A)
   exact rational; equivalently `g_bare = 1` is the unique compatible
   value.
3. Alternative `g^2` values (`1/2`, `2`, `4`) require `beta != 6`,
   incompatible with the canonical normalization-forced `beta = 2 N_c`.
4. The convention layer is explicitly identified at the canonical
   normalization carried by `cl3_color_automorphism_theorem`.
5. The constraint layer is explicitly identified: given (CN), `g_bare = 1`
   is structurally forced.

## Independent Audit

Audit must verify:

1. The cited one-hop dep
   `g_bare_rescaling_freedom_removal_theorem_note_2026-05-03` (companion
   theorem in the same PR) supplies the load-bearing identity that the
   rescaling A -> c * A under (CN) shifts beta = c^2 * beta, leaving
   g_bare unchanged. Without that identity, case (a) of the constraint
   load-bearing step would be open.
2. The load-bearing step `g_bare^2 = 2 N_c / beta = 1` is class (A)
   exact rational arithmetic, not a fitted match.
3. The case-(b) clause "A1 + A2 provide no external scale" is honest:
   `A1` is the Cl(3) anticommutator axiom and `A2` is the Z^3 substrate
   axiom; neither carries a scalar coupling parameter. Any alternative
   `g_bare` value would require an additional axiom or external import.
4. The note does NOT claim the canonical normalization (CN) is itself
   derived from A1 + A2. The convention status of (CN) remains open in
   this theorem; it is the admitted convention layer.
5. After this note lands and the audit ledger regenerates, the parent
   `G_BARE_DERIVATION_NOTE` row should record the constraint-vs-convention
   ambiguity as resolved (constraint reading closed, convention reading
   carried by the narrow convention theorem on main).

## What this changes for the leverage map

`G_BARE_DERIVATION_NOTE` parent (currently `audited_conditional`,
~263 transitive descendants) advances on one of three named repair-target
items: constraint-vs-convention disambiguation closes. Together with the
companion rescaling-freedom-removal theorem and the primary runner (all
in the same PR), all three repair items close. The parent's retention
still requires:

- independent audit of each of the three new artifacts;
- the upstream `cl3_color_automorphism_theorem` row to remain
  retained-grade (currently unaudited at the rendered ledger but a
  reviewed exact algebraic support theorem on main);
- the structural-normalization theorem chain remains conditional on the
  Wilson action choice (see Claim 3 caveat).

`G_BARE_DERIVATION_NOTE` therefore stays `audited_conditional` after this
PR lands, and the conditional reason narrows from "all three repair-target
items open" to "audit-pending on three new theorem rows + Wilson action
choice convention layer."

## Honest disambiguation language

For downstream rows depending on `g_bare = 1`, the safe wording is:

- *"The framework treats `g_bare = 1` as the canonical class (A)
  constraint relative to the canonical Cl(3) connection normalization
  `Tr(T_a T_b) = delta_ab/2`, which itself is the admitted framework
  convention carried by `cl3_color_automorphism_theorem`."*

The unsafe wording is:

- *"`g_bare = 1` is derived from Cl(3) axioms alone."* (false; the
  canonical normalization is admitted)
- *"`g_bare = 1` is just a convention."* (incomplete; the convention
  layer is one level upstream, and `g_bare = 1` is the derived constraint
  given that upstream convention)
