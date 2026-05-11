# DM A-BCC Retained Measurement Closure Theorem

**Date:** 2026-04-21
**Lane:** Dark-matter PMNS branch choice / A-BCC basin selection
**Status:** proposed_retained-MEASUREMENT CLOSURE ON THE CURRENT PACKAGE SURFACE. On
the retained measurement framework already carried in the package, the
physical basin choice is no longer open: the sigma-chain fixes `J_phys = Basin 1`, the retained P3
Sylvester theorem gives PMNS Non-Singularity on that physical path, and the
Sylvester signature-forcing theorem then puts the physical endpoint in
`C_base`. This closes A-BCC on the current package surface. At this stage of
the April 21 stack, the remaining current-package burden was the finer
right-sensitive microscopic selector law for the physical source branch /
point; the later same-day selector/current notes close that residual.
**Boundary:** This is **not** an axiom-native derivation of A-BCC from
`Cl(3)/Z^3` alone. The five-route assumptions audit still rules out a pure
algebraic sign closure, so the stricter axiom-native version remains outside
the current closure grade.
**Primary runner:**
`scripts/frontier_dm_abcc_retained_measurement_closure_2026_04_21.py`

---

## 0. Executive summary

The April 21 package already contains the full theorem stack needed to stop
treating A-BCC as a live DM blocker on the retained measurement surface.
What was missing was an integration theorem that states that fact plainly.

The closure chain is:

1. the active-chamber `chi^2 = 0` set is exactly `{Basin 1, Basin 2, Basin X}`;
2. the exact upper-octant / source-cubic selector fixes the active-chamber
   physical hierarchy pairing to `sigma_hier = (2,1,0)` and makes the
   negative PMNS CP sign a consequence;
3. under that retained sigma-chain, the physical source is `J_phys = J_{Basin 1}`;
4. the retained P3 Sylvester theorem gives
   `min_t det(H_base + t J_1) = 0.878... > 0`, so PMNS Non-Singularity holds
   on the physical path;
5. the PMNS Non-Singularity theorem and the Sylvester signature-forcing
   theorem then imply the physical endpoint lies in `C_base`.

That last statement is exactly A-BCC.

So on the retained measurement framework:

    chamber completeness
  + upper-octant / source-cubic selector
  + P3 Sylvester
  + Sylvester signature-forcing
  => A-BCC.

The current-package consequence is immediate: the DM flagship lane is no
longer blocked by branch choice. At this stage of the April 21 stack, the
only remaining current-package burden was the finer right-sensitive microscopic
selector law; that burden is later closed by the shifted same-law packet
theorem together with the ordered-chain current stack.

---

## 1. Inputs already retained on the branch

This note does **not** add a new scientific input. It integrates inputs and
theorems already carried elsewhere in the April 21 package:

- the retained affine Hermitian source family `H_base + J(m, delta, q_+)`;
- the chamber bound `q_+ + delta >= sqrt(8/3)`;
- the active-chamber `chi^2 = 0` completeness theorem;
- the exact chamber upper-octant law;
- the coefficient-free source-cubic selector `I_src(H) > 0`;
- the retained P3 Sylvester linear-path theorem on the physical basin;
- the PMNS Non-Singularity reduction theorem;
- the Sylvester signature-forcing theorem.

The existing assumptions audit remains in force: pure algebraic sign closure
of A-BCC from `Cl(3)/Z^3` alone is still ruled out.

---

## 2. Closure theorem

> **Theorem (A-BCC closes on the retained measurement framework).**
>
> On the retained measurement framework already carried in the package,
> the physical DM source is `J_phys = J_{Basin 1}` and the physical endpoint
> lies in the baseline-connected Sylvester chamber `C_base`.
>
> Equivalently: A-BCC is closed on the retained measurement surface.

### Proof

**Step 1: active-chamber completeness.**
The retained chamber-completeness theorem fixes the active-chamber
`chi^2 = 0` chart exactly as

    {Basin 1, Basin 2, Basin X}.

No other active-chamber PMNS-compatible basin survives on that chart.

**Step 2: sigma-chain collapse.**
The retained parity reduction, exact chamber upper-octant law, and
coefficient-free source-cubic selector imply:

- only `sigma_hier = (2,1,0)` survives on the active chamber;
- the negative PMNS CP sign is a consequence, not a retained selector input;
- among the active-chamber `chi^2 = 0` points, only Basin 1 satisfies the
  full retained sigma-chain.

Hence the physical source is

    J_phys = J_{Basin 1}.

**Step 3: physical-path PMNS Non-Singularity.**
For Basin 1 the retained P3 Sylvester theorem computes

    min_{t in [0,1]} det(H_base + t J_1) = 0.878... > 0.

So the physical path is nonsingular:

    det(H_base + t J_phys) != 0   for all t in [0,1].

This is PMNS Non-Singularity, now as a derived property of the physical path
rather than as a residual axiom.

**Step 4: endpoint chamber identification.**
The PMNS Non-Singularity theorem gives the linear-path implication

    PNS => endpoint in C_base.

The Sylvester signature-forcing theorem upgrades the same mechanism to an
all-path topological statement: any path from `C_base` to `C_neg` must cross
`det = 0`. Since the physical path is nonsingular, the physical endpoint
cannot lie in `C_neg`.

Therefore

    H_base + J_phys in C_base,

which is exactly A-BCC. QED.

---

## 3. What is now closed, and what is not

### 3.1 Closed on the current package surface

- physical basin choice / A-BCC on the retained measurement surface;
- the old DM branch-choice blocker in the April 21 package.

### 3.2 Still open

- at this stage of the stack, the finer right-sensitive microscopic selector
  law for the physical source branch / point;
- any stricter axiom-native derivation of A-BCC from `Cl(3)/Z^3` alone,
  without the retained measurement stack.

The first item was still the live DM flagship blocker at the moment this
integration theorem landed. The later same-day packet/current notes close it.
The second item is a closure-grade boundary statement rather than a
current-package blocker.

---

## 4. Review-surface consequence

At the point of this theorem alone, the DM flagship lane is no longer:

    A-BCC  +  microscopic selector law.

It is now simply:

    microscopic selector law.

More precisely: the physical PMNS target already lies on the exact regular
local source manifold identified elsewhere on the branch, and the carrier-side
split-2 completeness question is now interval-certified closed. With A-BCC
also closed on the retained measurement surface, the only live burden at this
stage was the finer right-sensitive microscopic point-selection law. The later
same-day shifted same-law packet theorem plus the ordered-chain current stack
close that remaining burden on the current package surface.

---

## 5. Verification

The integration runner executes the theorem stack and verifies the branch-level
numerical consequences:

- chamber completeness runner
- upper-octant / source-cubic selector runner
- sigma-hier upper-octant selector runner
- retained P3 Sylvester runner
- PMNS Non-Singularity runner
- Sylvester signature-forcing runner
- sigma-chain attack-cascade runner

The runner also rechecks the direct basin-level endpoint facts:

- Basin 1 lies in the chamber and in `C_base`;
- Basin 2 and Basin X lie in `C_neg`.

See
`scripts/frontier_dm_abcc_retained_measurement_closure_2026_04_21.py`.

## Audit dependency repair links

This graph-bookkeeping section records explicit upstream authority
citations named by prior 2026-05-05 audit feedback for
`dm_abcc_retained_measurement_closure_theorem_note_2026-04-21`.
The prior feedback identified the dependency chain as the load-bearing
boundary: the conclusion depends on upstream theorems and dependency
runners named in the prose, while the local runner mostly executes
external scripts and checks their stdout plus hard-coded basin
coordinates. This addendum does not promote the row or change the claim
scope, which remains the integration-style closure of A-BCC on the
retained measurement framework already carried in the April 21 package.
Independent audit owns any current verdict or effective status after
this source change.

One-hop authorities cited:

- [`DM_ABCC_PMNS_NONSINGULARITY_THEOREM_NOTE_2026-04-19.md`](DM_ABCC_PMNS_NONSINGULARITY_THEOREM_NOTE_2026-04-19.md)
  — audit row: `dm_abcc_pmns_nonsingularity_theorem_note_2026-04-19`.
  Upstream source authority for the PMNS Non-Singularity reduction
  theorem and the P3 Sylvester linear-path implication used in Step 3
  and Step 4 of the proof.
- [`DM_ABCC_SIGNATURE_FORCING_THEOREM_NOTE_2026-04-19.md`](DM_ABCC_SIGNATURE_FORCING_THEOREM_NOTE_2026-04-19.md)
  — audit row: `dm_abcc_signature_forcing_theorem_note_2026-04-19`.
  Upstream authority candidate for the Sylvester signature-forcing
  theorem that upgrades PMNS Non-Singularity to the all-path
  topological statement used in Step 4 of the proof.
- [`DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md`](DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md)
  — audit row:
  `dm_pmns_upper_octant_source_cubic_selector_theorem_note_2026-04-20`.
  Upstream authority for the exact upper-octant / source-cubic selector
  that fixes `sigma_hier = (2,1,0)` in Step 2 of the proof.
- `DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md`
  — audit row: `dm_sigma_hier_upper_octant_selector_theorem_note_2026-04-20`.
  Upstream authority candidate for the sigma-hier upper-octant selector
  layer used by Step 2.
- [`DM_ABCC_FIVE_BASIN_CHAMBER_DPLE_SUPPORT_THEOREM_NOTE_2026-04-21.md`](DM_ABCC_FIVE_BASIN_CHAMBER_DPLE_SUPPORT_THEOREM_NOTE_2026-04-21.md)
  — audit row:
  `dm_abcc_five_basin_chamber_dple_support_theorem_note_2026-04-21`.
  Sibling upstream authority for the corrected chamber+DPLE route on
  the five-basin chart that motivates Step 1 active-chamber
  completeness.
- `DM_ABCC_ASSUMPTIONS_AUDIT_NOTE_2026-04-19.md`
  — audit row: `dm_abcc_assumptions_audit_note_2026-04-19`.
  Boundary reference for the statement that the
  stricter axiom-native A-BCC target remains outside the current
  closure grade.

Open upstream gaps registered for independent audit:

- the Sylvester signature-forcing authority;
- the upper-octant / source-cubic selector authority;
- the sigma-hier upper-octant selector authority;
- the sibling chamber+DPLE authority.

The runner-checked content of this note (the integration runner
re-executes the chamber completeness, upper-octant / source-cubic
selector, sigma-hier upper-octant selector, retained P3 Sylvester,
PMNS Non-Singularity, Sylvester signature-forcing, and sigma-chain
attack-cascade runners; it also rechecks basin-level endpoint facts) is
verified composition over the cited authorities and is independent of
local rewriting of those authorities. The cite chain is what supplies
the upstream theorem chain that independent audit must evaluate.

## Honest auditor read

Prior audit feedback observed that the conclusion depends on upstream
theorems and dependency runners that were named but not cited as
authorities inside the restricted packet. The cite-chain repair above
wires the PMNS nonsingularity and assumptions-boundary anchors and
explicitly registers the remaining upstream authorities as open class D
upstream gaps. Closing those upstream rows is the path to a stronger
chain; local rewriting of this note does not by itself close that gap.

## Scope of this rigorization

This rigorization is class B (graph-bookkeeping citation) with an
explicit class D upstream gap registration. It does not change any
algebraic content, runner output, or load-bearing step classification.
It records the upstream authorities the prior feedback requested and
matches the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` rigorize
(commit `8e84f0c23`, PR #899) and the `dm_neutrino` bosonic candidates
trio (commit `7bb12badd`, PR #926).
