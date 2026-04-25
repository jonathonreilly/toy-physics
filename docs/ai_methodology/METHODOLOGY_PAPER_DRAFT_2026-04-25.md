# AI-Assisted Theoretical Physics As Auditable Repository Science

**Date:** 2026-04-25
**Status:** first synthesized methods-paper draft; not submission-ready prose

## Abstract

Large language models can write physics-looking arguments very quickly. That
is useful, and dangerous. The useful part is speed: the models generate routes,
tests, no-go searches, and reviews faster than a small team could do by hand.
The dangerous part is that a fluent argument can hide a missing bridge.

This paper describes the control system used in the `Cl(3)/Z^3` framework
repository. The basic unit is not a model answer. It is a chain: claim,
assumptions, note, runner or proof surface, review, status label, and landing
decision. Case studies from Standard-Model algebra, electroweak/top structure,
CKM, dark-sector selectors, Koide, and wave/gravity simulations show the same
pattern. The model expands the search. The repo decides what survives.

## 1. Introduction

The practical problem is not getting an AI system to write physics text. It
will write plenty. The problem is knowing which sentence, if any, should be
believed.

The Cl(3)/Z^3 project developed under high AI involvement from Claude and
OpenAI Codex. The tools were used for theorem drafting, runner generation,
branch review, no-go discovery, claim-surface audit, and selective integration.
They were not treated as authors or final authorities. The human author chose
the framework, targets, acceptance criteria, interpretation, and publication
posture.

The rule that emerged is simple: a claim is not accepted because it sounds
right in a conversation. It becomes eligible only when it is attached to an
evidence chain and survives review.

## 2. The Artifact Chain

The basic unit of work is:

- a bounded lane question;
- a theorem/support/no-go note;
- a runner, retained log, exact derivation, or explicit theorem import;
- a status label;
- a review disposition;
- a landing or demotion decision.

This structure matters because the common failure is not nonsense. It is a
nearly right derivation with one missing bridge, one imported input, one fake
check, or one status label that is too strong.

The repository therefore distinguishes retained, bounded, support, open,
no-go, rejected, and historical material. Public paper-facing claims live in a
separate publication package. Raw prompt history is evidence for methodology,
not authority for physics.

## 3. Division Of Labor

The raw archive shows a three-role system.

The human author supplies target selection and final judgment. The forward AI
system generates candidate routes, notes, runners, and search programs. The
review/integration AI system applies pressure: it checks whether the runner
really proves the note, whether the status label is too strong, whether an
input is imported, and whether a branch should be landed, narrowed, demoted, or
kept off-main.

This separation is essential. A single model asked to produce and bless its own
work tends to collapse exploration and validation. The repo keeps them apart.

## 4. Reviewer Backpressure

Review is where the method earns its keep.

In the raw data, backpressure appears as user correction, hostile-review
prompts, Codex review packets, controlled vocabulary, active review queues, and
commit history that demotes or retires overclaims. The governing rule is the
narrowest honest fix: wording issues can be fixed; missing theorem steps must
remain open or be demoted; false routes should become no-go evidence rather
than being hidden.

The persistent review lesson is semantic: correct algebra can still be attached
to the wrong physical object. Review must attack symbol identification,
assumptions, and ontology, not only calculations.

## 5. Case Studies

The case studies are derivation stories. Each asks the same questions. What was
hard? What did the model make easier? What did the repo refuse to believe?

The `Cl(3)/Z^3` to Standard-Model algebra case shows AI-assisted operator
search being forced into exact artifacts: explicit Clifford generators,
hypercharge projectors, `SU(3)` embeddings, Fierz identities, generation
orbits, and a `95/95` regression runner. The output is support theorem
structure, not a vague "emergence" narrative.

The quantitative electroweak/top/hierarchy case shows how the method handles a
long normalization chain. AI proposed routes through source response, tadpole
improvement, color projection, and Ward identities; review forced every row to
declare whether it was a structural identity, canonical-surface readout,
running bridge, or bounded support result.

The CKM case shows theorem extraction from a dense atlas. AI split the atlas
into focused notes for CP phase, off-diagonal magnitudes, `epsilon_K`, and the
`B_s` phase, while runners and review prevented CKM-fit observables from being
smuggled in as derivation inputs.

The dark-sector case shows the positive use of no-go results. Obstruction
audits narrowed a selector problem into exact target-surface statements,
quantitative current-bank mapping, and a bounded freezeout-bypass candidate
whose mass-origin mechanism remains explicitly open.

The Koide case is a deliberate non-closure case study. AI found many plausible
routes, but reviewer backpressure exposed unchecked decisive steps and turned
the lane into bridge narrowing plus no-go surfaces rather than fake retained
closure.

The wave/gravity case shows frozen replay discipline. AI-generated simulation
lanes produced positives, but review and replay demoted standard-lensing and
amplification overclaims where controls or normalization did not support the
headline.

## 6. Reusable Protocol

The reusable protocol is:

1. open a lane off-main;
2. define the status gates before claiming success;
3. require a note plus evidence artifact;
4. review the evidence chain adversarially;
5. classify findings into fix, demotion, science-needed, reject, or historical;
6. selectively land the honest subset;
7. preserve no-go and negative results;
8. update the public claim boundary and governance memory.

This is what the accompanying LLM skill pack encodes.

## 7. Accountability And Limits

This method does not make AI output intrinsically trustworthy. It also does not
replace mathematical proof with execution in contexts where proof is required.
Its claim is narrower: AI-assisted theoretical work becomes more auditable when
the exploration is forced through explicit artifacts, status labels, review
pressure, and public/private surface separation. This draft is not yet a
comparative study against other AI-science workflows, does not prove
AI-assisted theory is generally superior, and does not make the raw prompt
archive a public reproduction package without sanitization.

The author remains responsible for all scientific claims. AI systems are
research and engineering instruments in the workflow, not authors or arbiters.

## 8. Conclusion

AI makes candidate generation cheap. Judgment is still scarce. The hard
questions are what to test, what to demote, what to keep as a no-go, and what
to let onto the public claim boundary.

The lesson is not to trust the model. The lesson is to make the model leave
something behind that can be attacked, rerun, narrowed, archived, or rejected.
