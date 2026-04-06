# Claude Branch Retainability Note

**Date:** 2026-04-05  
**Scope:** branch-audit of `claude/distracted-napier` from a mainline-retainability perspective

This note is intentionally conservative. It does **not** merge branch claims
into `main`. It only asks which Claude-branch results look carryable onto
`main`, which ones are still interesting but branch-side, and which ones
currently fail our own bars.

Relevant branch-side anchors include:

- `scripts/qnm_scaling.py`
- `scripts/bmv_gravitational_entanglement.py`
- `scripts/distance_law_h2T_continuum.py`
- `scripts/complex_action_harness.py`
- `docs/BACKREACTION_NOTE.md`
- `docs/ASSUMPTION_DERIVATION_LEDGER.md`

## 0. Artifact-chain audit

The branch is uneven in an important way:

- **Complex-action / continuum / distance-law** work has the strongest
  retained-looking chain on the branch:
  - notes: `docs/COMPLEX_ACTION_NOTE.md`,
    `docs/CONTINUUM_LIMIT_NOTE.md`, `docs/CONTINUUM_CONVERGENCE_NOTE.md`,
    `docs/DISTANCE_LAW_NOTE.md`
  - logs: `logs/2026-04-05-complex-action-harness.txt`,
    `logs/2026-04-05-complex-action-grown.txt`,
    `logs/2026-04-05-h2-T-numpy-continuum.txt`,
    `logs/2026-04-05-h2-measure-continuum.txt`
- **QNM / BMV / entropy / ringdown / area-law / information-paradox**
  currently looks much more script-driven:
  - scripts exist for `qnm` and `bmv`
  - the branch-level docs/log inventory does **not** yet show a comparable
    dedicated note+log chain for the strongest-field claims
  - the later headline commits `e9f8eb8 feat(entropy)`,
    `5ba2c01 feat(area-law)`, `319ce8b feat(ringdown)`, and
    `a29e82a feat(unitarity)` sit on the same tree as the prior `BMV` commit,
    so they currently read as claim pushes without new artifact additions

That does not make the strong-field results false. It does mean they are
harder to promote safely onto `main` right now.

## 1. Likely retainable soon

These are the Claude-branch results that look closest to mainline-safe if they
are phrased narrowly.

- **Exact-lattice wavefield phase-ramp law**
  - strongest current mechanism lane
  - exact zero-source reduction survives
  - `TOWARD` survives
  - `F~M` stays near linear
  - the detector-line phase ramp is coherent and already compressible into a
    clean discriminator card
  - branch-side support is strongest where the phase-ramp slope and span scale
    approximately linearly with source strength

- **Exact-lattice complex-action harness**
  - the exact-lattice harness has the cleanest branch-side artifact chain in
    this lane:
    `scripts/complex_action_harness.py`,
    `docs/COMPLEX_ACTION_NOTE.md`,
    `logs/2026-04-05-complex-action-harness.txt`
  - exact `gamma = 0` reduction is frozen in the log
  - Born is machine-clean on the logged exact-lattice harness
  - the narrow safe phrasing is:
    one exact-lattice complex-action family shows a clean
    `TOWARD -> AWAY` transition while preserving the exact-lattice Born test
  - this should not yet be promoted as geometry-independent because the
    companion grown-geometry log
    `logs/2026-04-05-complex-action-grown.txt` is empty on the branch

- **Wide-lattice `h^2+T` distance-law replay**
  - strongest branch-side distance-law claim, but only in its narrower form
  - the script and branch notes support a finite-lattice replay with attractive
    far-field rows
  - the safe phrasing is finite-lattice only:
    far-field rows stay `TOWARD` and `F~M` stays near `1`
  - this is retainable only as a bounded replay / finite-size statement
  - it should not be promoted as a continuum theorem or universal
    `-1.5`-style claim

## 2. Interesting but still branch-side exploratory

These are scientifically meaningful, but they still need a much stronger
mainline reduction / control story before they should be treated as retained.

- **Self-consistent backreaction / Poisson self-gravity**
  - branch-side story: absorption threshold, horizon-like behavior, and
    complex-action-as-effective-theory language
  - branch-side evidence is real, but the effect is still small in the audited
    exact-lattice/control framing
  - the clean branch risk is that this remains a useful control family rather
    than a new mechanism lane

- **QNM / BMV / entropy / ringdown / area-law cluster**
  - `QNM`: mode spacing depends on `G`, not on source mass
  - `BMV`: back-reaction induces a gravitational phase / decoherence signature
  - entropy / area-law / ringdown: rich strong-field phenomenology
  - concrete hardening gap:
    `QNM` and `BMV` have scripts but no dedicated note/log chain, while the
    later entropy / area-law / ringdown / information-paradox claims do not
    currently add new files at all
  - these are the most promising “physics-story” results on the branch, but
    they are still exploratory until they inherit the same hard control chain
    as the best mainline cards

- **Complex action / emergent gamma**
  - the exact-lattice harness is stronger than the backreaction-driven
    interpretation
  - useful as an effective description of the backreaction branch
  - conceptually interesting because it turns the horizon-like behavior into a
    single kernel
  - still exploratory as a broader theory because:
    the grown-geometry companion log is empty and the `epsilon -> gamma`
    mapping is not a clean quantitative law

## 3. Currently incompatible with mainline bars

These are the claims that are too strong for the current evidence chain.

- **A full self-gravity mechanism lane**
  - the exact `epsilon = 0` reduction is good
  - step-local Born can be good
  - but end-to-end Born is not machine-clean on the tested loop
  - that makes the lane control-only, not a retained self-gravity bridge

- **A universal continuum / asymptotic steepening claim**
  - any `-1.5`-style distance-law story is not yet mainline-safe
  - the branch-side `docs/DISTANCE_LAW_NOTE.md` overreaches relative to the
    artifact chain: it cites the wide script, but the note itself does not
    anchor a matching retained log and the fit is still window-sensitive
  - the branch evidence is still finite-lattice and window-sensitive
  - it should stay out of the mainline story until it is independently
    retained with a matching safe claim surface

- **A settled information-paradox resolution**
  - branch wording can suggest probability conservation or horizon
    thermodynamics
  - the `feat(unitarity)` claim currently arrives as an empty-commit style
    message push, not as a hardened script+log+note package
  - but that is not yet a mainline-retained result with the required control
    chain
  - it should be treated as an exploratory strong-field narrative, not a
    settled claim

- **A full BMV-style gravitational entanglement claim**
  - the branch script currently builds a witness/proxy rather than a joint
    state entanglement measure
  - that makes it interesting, but not yet mainline-safe as an entanglement
    result
  - it needs a stronger mediator-null and state-construction story before it
    should be promoted

## 4. Highest-value hardening shortlist

This section is intentionally different from the retainability ranking below.
It asks: if we spend more hardening effort on branch work, which claims have
the best value-adjusted upside?

Current shortlist:

1. **Complex-action unification**
   - strongest branch-side unification story if it can be replayed through one
     exact-lattice + grown-geometry + weak-field control chain
2. **Weak-field `h^2+T` continuum closure to `h = 0.125`**
   - high value because it would materially strengthen the continuum/credibility
     lane without depending on the weakest strong-field narratives
3. **Wide-lattice distance-law replay**
   - already close to mainline-safe in bounded form, but still needs one
     canonical asymptotic phrasing rather than competing `-1.5` / `-1.0` /
     widened-tail headlines
4. **Self-gravity critical scaling**
   - high upside, but only if the exact same loop also clears end-to-end Born
     and weak-field class checks
5. **QNM spectrum**
   - highest speculative upside in the strong-field cluster, but also the most
     vulnerable to analysis-choice and refinement collapse unless the non-Nyquist
     peaks survive harder controls

## Bottom Line

The mainline-retainability ranking is:

1. exact-lattice wavefield phase-ramp law
2. exact-lattice complex-action harness as an exact-lattice-only carryover
3. wide-lattice `h^2+T` distance-law replay as a finite-lattice claim
4. QNM / BMV / entropy / ringdown as branch-side exploratory strong-field
   physics
5. self-consistent backreaction only as a control family unless the Born / loop
   story improves

The safest takeaway is:

- the branch has produced real physics,
- the exact-lattice wavefield lane is still the strongest carryable claim,
- the exact-lattice complex-action harness is stronger than the broader
  geometry-independent complex-action story,
- the wide-lattice distance-law lane is only safe as a bounded finite-lattice
  replay,
- while the self-gravity / horizon / information-paradox cluster is still
  interesting but not yet retainable as a mechanism claim.
