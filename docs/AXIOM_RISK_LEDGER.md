# Axiom Risk Ledger

**Status:** reviewer-facing synthesis note  
**Date:** 2026-04-09

## Purpose

The repo now has enough evidence to separate three different questions:

- which axioms still look structurally sound
- which axioms look too vague or too strong
- which missing axiom-level constraint may be needed to explain the retained results

This note is not a proof that any axiom is false. It is a risk assessment based on the current retained and falsified lanes.

## Short version

- **Likely keep:** Axioms 1, 2, 3, 4, 5, 7, 9
- **Likely weaken / sharpen:** Axiom 6
- **Most at risk / likely needs rewrite:** Axiom 8
- **Probably demote from hard axiom to methodological preference:** Axiom 10
- **Likely missing:** an axiom or rule enforcing local linear / isometric transport before durable record formation

## Current assessment

| axiom | current risk | why |
|---|---|---|
| 1. evolving event-network ontology | low | None of the recent negative results argue against an event/network substrate. The trouble is in the propagation law, not the ontology. |
| 2. stable objects as persistent patterns | low-medium | Still plausible, but current source-spectrum work does not yet show that persistent patterns naturally select the attractive narrowband window. So the ontology survives, but one hoped-for dynamical consequence does not yet follow. |
| 3. space inferred from neighborhoods and delay | low | Still compatible with the retained program and with the viable kernel candidates based on neighborhood overlap / local continuation. |
| 4. duration as local update count | low | The recent failures do not pressure this directly. |
| 5. arrow of time tied to durable records | low | Decoherence / record-formation lanes remain conceptually aligned with this. |
| 6. free systems follow the locally simplest admissible continuation | medium | This is likely too underspecified. It helps motivate kernel families, but it does not yet uniquely determine the transport law or close the 3+1D kernel question. |
| 7. inertia is undisturbed natural continuation | low-medium | Still broadly plausible. The pressure is that the exact transport law needed for “undisturbed continuation” may have to be norm-preserving / isometric in a way not currently stated. |
| 8. gravity is natural continuation in a distorted continuation structure | high | This is the axiom under strongest pressure. Across architectures, “distortion” by itself does not robustly produce attraction. Raw transfer gives resonance-window attraction, local beam-splitter gives Born + locality + unitarity but gravity AWAY, and the dense global unitary gives attraction only in a nonlocal x-invariant medium. |
| 9. measurement is durable record formation that separates alternatives | low | Nothing in the recent gravity/unitarity failures pushes strongly against this. |
| 10. explain large-scale structure by persistent local mechanisms wherever possible | medium-high as a hard axiom, low as a preference | The best broadband attraction found so far comes from global polar-projected unitary operators, which are not local mechanisms. This suggests Axiom 10 is better treated as a methodological bias than as a strict physical axiom. |

## Evidence behind the risk calls

### Axiom 8 is the most pressured

The repo now has three qualitatively different outcomes:

- **Raw path-sum / transfer matrix:** attraction exists, but mainly in narrow resonance windows and does not survive honest broadband source-side controls.
- **Local beam-splitter unitary:** barrier Born test passes cleanly and the propagator is sparse and unitary, but gravity is AWAY in the retained Euclidean version and stays AWAY in the tested Lorentzian phase-advance / mixing-suppression fork.
- **Dense polar-projected unitary:** norm is exact and attractive spectral shifts can appear, but this is a global dense operator with immediate full-width support and an x-invariant medium rather than a localized mass harness.

That pattern argues against the strong reading of Axiom 8:

> “distorting the continuation structure naturally yields gravity”

What the evidence supports instead is weaker:

> gravity-like behavior, if it exists, is highly sensitive to the detailed continuation law, especially how causal advance, transverse mixing, locality, and norm preservation are implemented

### Axiom 6 probably needs sharpening, not abandonment

The turn-cost and Jaccard routes show that Axiom 6 can generate useful candidate kernels. That is a real positive. But:

- Route A still fits a scale parameter against the retained reference kernel
- the candidate kernels do not close 3+1D gravity
- Axiom 6 does not yet tell us whether the propagator should be raw path accumulation, dense polar projection, or local beam-splitter transport

So the problem is not that local simplicity is wrong. The problem is that it is not specific enough to select the actual transport law.

### Axiom 10 should probably be demoted

Taken as a preference, Axiom 10 is fine.

Taken as a strict axiom, it is now too strong. The best broadband-attraction result currently comes from a global, dense, nonlocal unitary projection. That does not mean the local program is wrong, but it does mean the data no longer support treating locality-first explanation as mandatory.

## Recommended rewrites

### Axiom 6

Current:

> Free systems follow the locally simplest admissible continuation.

Recommended rewrite:

> Free systems follow the locally most coherent admissible continuation, with the transport law required to preserve a stable amplitude or probability norm in the absence of durable record formation.

Why:

- preserves the spirit of local simplicity
- adds the missing pressure toward norm-preserving transport
- connects better to the empirical tension between raw amplification and cleaner unitary-like behavior

### Axiom 8

Current:

> Gravity is natural continuation in a distorted continuation structure.

Recommended rewrite:

> Gravity-like behavior, if it exists, must emerge from the local continuation law under asymmetric causal and transverse distortions. A generic distorted continuation structure need not attract.

Why:

- matches the actual results
- no longer implies that any delay/load distortion should bend TOWARD mass
- leaves room for the Lorentzian causal/transverse split to matter

### Axiom 10

Current:

> Observed large-scale structure should be explained by persistent local mechanisms wherever possible.

Recommended rewrite:

> Persistent local mechanisms are the preferred explanation unless a nonlocal effective operator is empirically retained and no comparable local construction yet reproduces the same behavior.

Why:

- keeps the methodological preference
- avoids overclaiming that locality has already been established

## Likely missing axiom

The current evidence suggests a missing constraint closer to:

> Before durable record formation, admissible propagation should be locally linear and approximately isometric.

This is not yet derived from the current ten axioms, but it is exactly the kind of condition the repo keeps rediscovering empirically:

- raw non-unitary propagation corrupts broadband gravity and continuum observables
- naive layer normalization fixes the spectrum but breaks the linear/Born structure
- dense global unitary fixes norm but loses locality
- local beam-splitter keeps locality and barrier Born, but the gravity sign is still wrong

So a missing “linear/isometric pre-measurement transport” axiom is a serious candidate, not an arbitrary patch.

## Practical conclusion

If one axiom is actually wrong, it is most likely **Axiom 8** as currently stated.

If one axiom is too strong, it is most likely **Axiom 10**.

If one axiom is too vague to do the work being asked of it, it is most likely **Axiom 6**.

If the axiom set is incomplete rather than wrong, the most plausible missing ingredient is:

- **local linear / isometric propagation before record formation**

That is the cleanest axiom-level summary of where the project now stands.
