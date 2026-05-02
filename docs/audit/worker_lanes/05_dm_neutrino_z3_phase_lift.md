# Lane 5: DM neutrino Z3 phase lift — replace renaming with derivation

**Status:** OPEN — accepting workers.
**Source claim:** [`dm_neutrino_z3_phase_lift_mixed_bridge_note_2026-04-15`](../../../docs/DM_NEUTRINO_Z3_PHASE_LIFT_MIXED_BRIDGE_NOTE_2026-04-15.md)
**Audit verdict:** `audited_renaming`
**Criticality:** `high` · **Transitive descendants:** 119 · **Load-bearing class:** E (definition)
**Runner:** `scripts/frontier_dm_neutrino_z3_phase_lift_bridge.py` (registered)

This is the only `audited_renaming` finding at high criticality. It
sits inside the dark-matter "flagship closed" package — a region the
existing publication-facing tables present as ratified but the audit
lane has flagged.

## Audit finding (verbatim from the ledger)

**Load-bearing step under audit:**

> Define `K_λ = d·I + r·(e^{iλδ_src} S + e^{−iλδ_src} S²)`, with
> `δ_src = 2π/3` and a new bridge amplitude `λ`, so
> `c_odd(λ) = r·sin(λδ_src)`.

**Why the chain does not close:**

The runner verifies **exact algebraic properties of the defined family**:
`λ=0` reproduces the even bank, nonzero `λ` turns on the odd slot, and
`λ=1` uses the `Z₃` phase. It does **not** derive the bridge amplitude
or the mixed-sector phase lift from the retained local stack. The
source note itself calls the family **invented / candidate** and
records a later mass-basis no-go for the exact `Z₃`-covariant
circulant class.

This is the cleanest worked example of definition-disguised-as-
derivation in the package: a new symbol (`λ`) is introduced, an
algebraic identity is shown to hold for the newly-defined family, and
the identity is then cited as if it were a derivation. The audit
correctly classifies this as `audited_renaming`.

**Unregistered / open dependencies:**

- Exact even local DM kernel `(d, r)` authority — not registered
  one-hop.
- Weak-only `Z₃` CP source `δ_src` theorem — not registered one-hop.
- Source-faithful `λ` branch theorem — not registered one-hop.
- Residual-`Z₂`-odd bridge / activator theorem — open.
- Mass-basis physical leptogenesis texture — no-go is unresolved.

## Repair target

A retained theorem and runner deriving the residual-`Z₂`-odd bridge
or activator from the **current stack** (rather than an invented
amplitude), with:

1. A **source-faithful** `λ` branch (the bridge amplitude derived from
   primitives, not introduced as a free parameter).
2. A **physical mass-basis texture that evades the no-go** the source
   note already flags. Without this, the renaming has nothing to be
   ratified against — the no-go is load-bearing in the opposite
   direction.

## Why this is high-leverage

119 transitive descendants. Sits inside the dark-matter "flagship
closed" package on `CLAIMS_TABLE.md`. Per the audit lane's hard rule,
that flagship designation must not be treated as retained-grade without
an independent scoped audit, and this audit finding is exactly why.

If the renaming cannot be replaced with a derivation, the DM "flagship
closed" claim's effective_status drops by inheritance — a claim
boundary correction with significant publication-surface impact.

## Claim boundary while this lane is open

Per the audit verdict:

- It is safe to use `K_λ` as an **algebraically controlled candidate
  family** showing how a `Z₃` phase would populate the odd slot.
- It is **not** safe to claim a retained DM-neutrino mixed bridge or
  leptogenesis closure.

The DM package's "flagship closed" status on the publication-facing
surface is therefore overstated until either this lane closes or the
DM package is re-scoped to exclude the mixed bridge.

## Suggested approach (worker-side)

Three plausible paths — pick one based on what the underlying physics
admits:

### Path A: derive the bridge amplitude
Source-faithful derivation of `λ` from the retained local stack.
Requires: registered authority for the exact even local DM kernel
`(d, r)`, plus a derivation showing what `λ` must equal given the
weak-only `Z₃` CP source. The challenge is the existing mass-basis
no-go — Path A only works if you can show a physical texture that
evades it.

### Path B: replace the parametric family with a structural identity
Instead of a free `λ`, find a structural reason the bridge amplitude
takes a specific value (e.g., `λ = 1` selected by the Z₃ phase
itself, with no free parameter). This eliminates the renaming by
removing the introduced symbol entirely.

### Path C: honest downgrade
Reclassify `K_λ` as a candidate algebraic family (which is what the
source note itself already says it is). Update the publication-facing
DM package surface to reflect that the mixed bridge is bounded /
support, not flagship-closed. Re-scope the DM "flagship closed"
package to exclude the mixed-bridge component.

Path A is the strongest if it works; Path B is cleaner; Path C is the
honest fallback if the no-go is genuinely unevadable.

## Success criteria

- Path A or B: `dm_neutrino_z3_phase_lift_mixed_bridge_note` re-audits
  as `audited_clean` (load-bearing step is class C — first-principles
  compute — rather than class E — definition). Cross-confirmation
  required if criticality stays high.
- Path C: source-note status downgraded to `support` or `bounded`;
  publication-facing DM surface narrowed; re-audit returns either
  `audited_clean` against the narrower claim or accepts the support
  tier without ratification. Downstream DM "flagship closed" rows
  are re-scoped accordingly.

## Branch / worker conventions

- Path A proposal: `claude/dm-neutrino-z3-bridge-derivation-2026-04-27`.
- Path B proposal: `claude/dm-neutrino-z3-bridge-structural-2026-04-27`.
- Path C proposal: `claude/dm-neutrino-z3-bridge-downgrade-2026-04-27`.
- Codex review branch: `codex/review-dm-neutrino-z3-bridge-2026-04-27`.

## What this lane is NOT

- Not a request to fight the "renaming" verdict. Defining a family
  that has the desired algebra is genuinely not the same as deriving
  the family from primitives, and the audit correctly distinguishes.
- Not a request to expand the DM-neutrino claim surface. All three
  paths either close existing claims or honestly narrow them.
- Not a place to re-litigate the existing mass-basis no-go. If the
  no-go stands, Path C is the right outcome.
