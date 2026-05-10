# Abstract-Algebraic Core Extraction Technique

**Date:** 2026-05-10
**Status:** methodology note; not a physics authority surface and not
an audit verdict.
**Companion reference for agents:**
[`skills/physics-loop/references/abstract-algebraic-core-extraction.md`](skills/physics-loop/references/abstract-algebraic-core-extraction.md)

## Purpose

Abstract-algebraic core extraction is a review discipline for turning a
broad or stuck derivation attempt into the narrowest source note that is
actually supported by its proof artifact. It is useful when a branch mixes:

1. an algebraic or representation-theoretic skeleton;
2. physical, operational, or convention imports;
3. numerical checks or external comparisons.

The technique separates those layers before source-note drafting. The
algebraic skeleton may become a narrow theorem, bounded theorem, no-go,
or open gate. The imports and bridge steps stay explicit and out of
scope unless separately derived or already supported by retained-grade
dependencies.

This note does not promise that a result will retain, pass audit, or
promote a parent claim. It is a way to prepare cleaner review surfaces
for the independent audit lane.

## Protocol

Run these exercises before writing or revising a source note:

1. **Assumptions inventory.** List every premise used by the load-bearing
   step. Mark it as framework baseline, derived local theorem, retained
   dependency, admitted/imported input, observed/fitted value, or open gate.
2. **First-principles narrowing.** Ask what remains if conventions,
   observations, and parent-claim ambitions are stripped away. Keep only
   the theorem actually forced by the available algebra or cited retained
   dependencies.
3. **Literature check.** Use literature to identify standard theorem names
   and avoid incorrect reinvention. Do not let literature numerics become
   hidden derivation inputs.
4. **Math/artifact check.** Make the runner test the load-bearing bridge,
   not just downstream arithmetic after the bridge is assumed. Include a
   counterexample when a hypothesis is claimed to be necessary.

## Output Shape

Each source note produced through this technique should state:

- intended `claim_type`;
- exact claim scope;
- load-bearing dependencies as real markdown links when they are dependencies;
- imported or admitted inputs;
- what the note does not claim;
- paired runner and cache where applicable;
- independent-audit authority language.

The output may be `positive_theorem`, `bounded_theorem`, `no_go`,
`open_gate`, `decoration`, or `meta`. The review loop chooses the honest
claim type from the artifact; it does not use this technique to force a
positive result.

## Guardrails

- Do not add new axioms or repo-wide premises.
- Treat physical `Cl(3)` on `Z^3` as the existing framework baseline,
  not as a new assumption and not as automatic closure of downstream
  species/readout/selector claims.
- Do not write audit verdicts or effective-status outcomes into source
  notes.
- Do not use PR numbers, campaign counts, or branch-local success rates
  as science authority.
- Do not turn a literature citation into an unlabelled import.
- Do not claim parent promotion. If the parent still needs a bridge,
  say so.

## Relation To Review And Audit

Review-loop may use this technique to salvage a meaningful narrow result
from an overbroad PR. Audit-loop remains independent: it decides whether
the resulting claim row is retained, retained-bounded, retained-no-go,
failed, conditional, or otherwise.

The technique is successful when it leaves a smaller, auditable claim
boundary and makes any remaining physics work easier to find.
