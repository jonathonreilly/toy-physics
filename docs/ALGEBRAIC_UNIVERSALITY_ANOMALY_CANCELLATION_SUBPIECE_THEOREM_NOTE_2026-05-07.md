# Algebraic Universality on A_min — Anomaly Cancellation Sub-Piece

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support packaging the next sub-piece in the
algebraic-universality programme started in PR
[#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670):
the four anomaly-cancellation identities

```text
(E1)      Tr[Y]                  = 0,
(E2)      Tr[SU(3)² Y]           = 0,
(E3-LH)   Tr[Y³]_LH              = −16/9,
(E3-full) Tr[Y³]                 = 0,
```

are *lattice-realization-invariant* per the §2 definition introduced in
PR #670. The proof of each identity uses only (i) chiral-content
multiplicity counts, (ii) hypercharge values, (iii) the SU(3) Dynkin
index `T(fund) = 1/2`, and (iv) rational arithmetic — never any Wilson
plaquette / staggered-phase / BZ-corner / link-unitary content.
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_algebraic_universality_anomaly_cancellation_subpiece.py`

## 0. Question

PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)
landed the framing note that splits A_min's predictions into the
*algebraic class* (lattice-realization-invariant by direct proof
structure) and the *continuum-limit class* (Wilson-universality
asymptotic invariants), and proved the **first** algebraic-universality
sub-piece explicitly: SM hypercharges `(+4/3, −2/3, −2, 0)` are
realization-invariant because their proof in
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
walks only on chiral-content multiplicities + Dynkin indices + rational
arithmetic.

PR #670's §6 enumerated seven follow-on sub-pieces, each requiring its
own per-prediction proof-walk. This note ships sub-piece 5:

```text
Are the anomaly-cancellation identities (E1) Tr[Y] = 0, (E2)
Tr[SU(3)² Y] = 0, (E3-LH) Tr[Y³]_LH = −16/9, and (E3-full) Tr[Y³] = 0
themselves lattice-realization-invariant per PR #670's §2 definition?
```

## Answer

**Yes.** The proofs of these identities — as packaged in
[`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) and
[`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
— use only chiral-content multiplicity counts, hypercharge values, the
SU(3) Dynkin index `T(3) = 1/2`, and rational arithmetic. No step
invokes Wilson plaquette form, staggered-phase choice, BZ-corner
labels, link unitaries, lattice scale `a`, or any other lattice-
machinery quantity as a load-bearing input.

Combined with PR #670's hypercharge sub-piece, this closes the
algebraic-universality theorem-row for the perturbative anomaly
cancellation block of A_min's algebraic-class predictions: the entire
chain `(chiral content) → (anomaly arithmetic) → (E1, E2, E3-LH,
E3-full vanish)` is realization-invariant.

## 1. Framing recap

Per PR #670's §2 definition: a framework prediction `P` is
*lattice-realization-invariant* iff the proof of `P` cites no
lattice-machinery quantity as a load-bearing input. Equivalently: any
A_min-compatible realization producing the same chiral content +
retained gauge-group structure + retained anomaly-cancellation
conditions gives the same `P` by direct proof substitution.

The four anomaly identities live at A_min's algebraic / representation-
theory level: each is an arithmetic identity on multiplicities and
hypercharges, evaluated against a Dynkin-index normalization that is a
group-theoretic constant. They are the rational fingerprints of A_min's
chiral content and the proof of each is mechanical rational arithmetic.

## 2. Theorem (Anomaly Cancellation Algebraic Universality)

**Bounded theorem.** Under {A_min + retained-tier surface (LH content
`Q_L : (2,3)_{+1/3}` + `L_L : (2,1)_{−1}` + RH SU(2)-singlet completion
with `(Y(u_R), Y(d_R), Y(e_R), Y(ν_R)) = (+4/3, −2/3, −2, 0)` from
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
+ Dynkin index `T(3) = T(2) = 1/2`)}, the four anomaly identities

```text
(E1)      Tr[Y]                  = 0
(E2)      Tr[SU(3)² Y]           = 0
(E3-LH)   Tr[Y³]_LH              = −16/9
(E3-full) Tr[Y³]                 = 0
```

are *lattice-realization-invariant* per PR #670's §2 definition. Any
A_min-compatible lattice realization producing the same retained chiral
content + the same retained gauge-group structure + the same retained
anomaly-cancellation conditions produces the same identities via the
same proofs, which use no Wilson plaquette / staggered-phase /
BZ-corner / link-unitary content as load-bearing input.

## 3. Proof-walk verification

The four identities are proved across two upstream authority notes:

- (E1), (E3-LH), (E2-LH), (E4-LH = Witten) for the LH-only contributions
  in [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
  (`(C1)–(C5)` in that note's notation).
- (E1), (E2), (E3-full) full-content cancellation as part of the
  anomaly-cancellation step in
  [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  Step 1 + Step 2 (the table: `Tr[Y] = 0`, `Tr[Y³] = 0` cancel the LH
  values of `0` and `−16/9` after RH completion is added).

We walk each identity step by step.

### 3.1 Proof-walk of (E1) Tr[Y] = 0

Authority: `LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md` §(C1)
+ `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`
§2.1 (E1) under `(y_1, y_2, y_3, y_4) = (4/3, −2/3, −2, 0)`.

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| LH (C1) | `Tr[Y]_LH = 6·(1/3) + 2·(−1) = 2 − 2 = 0` | LH multiplicities `(6, 2)` from `(2 colors × 3) + (1 × 2 isospin)`; LH hypercharges `(+1/3, −1)` | NO — multiplicity counts come from chiral structure, hypercharges admitted retained |
| RH | RH contribution `−3y_1 − 3y_2 − y_3 − y_4 = −3(4/3 − 2/3) − (−2) − 0 = −2 + 2 = 0` | RH multiplicities `(3, 3, 1, 1)` from `3 colors × 1` for u_R, d_R; `1 × 1` for e_R, ν_R; RH hypercharges fixed by SMH | NO — algebraic substitution |
| Sum | `Tr[Y] = 0 + 0 = 0` | rational arithmetic | NO — pure rational arithmetic |

**Conclusion (E1).** Every step uses only (i) chiral-content
multiplicities, (ii) hypercharge values, or (iii) rational arithmetic.
No lattice machinery appears. ∎

### 3.2 Proof-walk of (E2) Tr[SU(3)² Y] = 0

Authority: `LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md` §(C3)
+ `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`
§2.1 (E2).

Only quark sectors contribute (SU(3) fundamentals); leptons sit in
SU(3)-singlet representations and contribute zero.

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| LH-quark trace | `Tr[SU(3)² Y]_LH = T(3) · 2 · (1/3) = (1/2)·(2/3) = 1/3` (per color factor; structural `T(3) = 1/2`) | SU(3) Dynkin index `T(3) = 1/2`; LH-quark weak-isospin multiplicity `2`; `Y(Q_L) = +1/3` | NO — Dynkin index is group-theoretic constant, multiplicity is structural |
| RH-quark trace | `Tr[SU(3)² Y]_RH-quark = T(3) · (−Y(u_R) − Y(d_R)) = (1/2) · (−4/3 − (−2/3)) = (1/2) · (−2/3) = −1/3` | same Dynkin index; RH-quark weak-isospin multiplicity `1`; RH hypercharges from SMH | NO — algebraic substitution |
| Sum | `Tr[SU(3)² Y] = 1/3 + (−1/3) = 0` | rational arithmetic | NO — pure rational arithmetic |

**Conclusion (E2).** Every step uses only (i) the Dynkin index
`T(3) = 1/2` (group-theoretic), (ii) chiral-content multiplicities,
(iii) hypercharge values, (iv) rational arithmetic. No lattice
machinery. ∎

### 3.3 Proof-walk of (E3-LH) Tr[Y³]_LH = −16/9

Authority: `LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md` §(C2).

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| Q_L cubic | `6 · (1/3)³ = 6/27 = 2/9` | LH-Q_L multiplicity `6`; `Y(Q_L) = +1/3`; cubing | NO — pure arithmetic |
| L_L cubic | `2 · (−1)³ = −2` | LH-L_L multiplicity `2`; `Y(L_L) = −1`; cubing | NO — pure arithmetic |
| Sum | `Tr[Y³]_LH = 2/9 − 2 = 2/9 − 18/9 = −16/9` | rational arithmetic | NO — pure rational arithmetic |

**Conclusion (E3-LH).** Every step uses only (i) chiral-content
multiplicities, (ii) hypercharge values, (iii) rational arithmetic. No
lattice machinery. The exact rational value `−16/9` is the LH-only
cubic fingerprint that the RH completion must cancel. ∎

### 3.4 Proof-walk of (E3-full) Tr[Y³] = 0

Authority: `STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`
§2.1 (E3) under `(y_1, y_2, y_3, y_4) = (4/3, −2/3, −2, 0)`.

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| LH-cubic | `Tr[Y³]_LH = 2/9 − 2 = −16/9` (from §3.3) | rational arithmetic + LH cubic identity (E3-LH) | NO — see §3.3 |
| RH-cubic | `−3 y_1³ − 3 y_2³ − y_3³ − y_4³ = −3·(4/3)³ − 3·(−2/3)³ − (−2)³ − 0³` | RH multiplicities; SMH RH hypercharges; cubing | NO — pure arithmetic |
| Compute RH | `= −3·(64/27) − 3·(−8/27) − (−8) − 0 = −192/27 + 24/27 + 8 = −168/27 + 216/27 = 48/27 = 16/9` | rational arithmetic | NO |
| Sum | `Tr[Y³] = −16/9 + 16/9 = 0` | rational arithmetic | NO — pure rational arithmetic |

**Conclusion (E3-full).** Every step uses only (i) chiral-content
multiplicities, (ii) hypercharge values, (iii) rational arithmetic. No
lattice machinery. The full-content cubic identity vanishes by exact
rational cancellation between LH and RH sectors. ∎

### 3.5 Aggregate verdict

Every step of every proof of (E1), (E2), (E3-LH), (E3-full) cites only
inputs from the algebraic class:

- (i) chiral-content multiplicity counts `(6, 2, 3, 3, 1, 1)`,
- (ii) hypercharge values `(+1/3, −1, +4/3, −2/3, −2, 0)` (algebraic
  per PR #670),
- (iii) Dynkin index `T(3) = 1/2` (group-theoretic constant),
- (iv) rational arithmetic.

No step cites Wilson plaquette form, staggered-phase choice, BZ-corner
labels, link unitaries, lattice scale `a`, Monte Carlo measurements, or
any other lattice-machinery quantity. The four identities are
*lattice-realization-invariant* per PR #670's §2 definition. ∎

## 4. Concrete realization-invariance test

Construct three hypothetical "alternative" A_min-compatible chiral
realizations (purely as mathematical sanity checks on the meta-claim),
each producing the same retained chiral content:

1. **Realization R_KS** (canonical Kogut-Susskind staggered-Dirac, A3-forced).
2. **Realization R_alt-A** (hypothetical: domain-wall-style chiral
   formulation producing the same `Q_L : (2, 3)`, `L_L : (2, 1)` plus
   RH SU(2)-singlet completion).
3. **Realization R_alt-B** (hypothetical: any other A_min-compatible
   realization with the same retained chiral content).

Across all three, the multiplicity counts `(6, 2, 3, 3, 1, 1)` are
identical (they are STRUCTURAL FACTS of the chiral content, not the
lattice realization), the hypercharges `(+1/3, −1, +4/3, −2/3, −2, 0)`
are identical (PR #670 algebraic-universality result), and the Dynkin
index `T(3) = 1/2` is identical (group-theoretic constant). So each of
the four anomaly traces evaluates identically across all three
realizations to:

```text
Tr[Y]         = 0    (E1)
Tr[SU(3)² Y]  = 0    (E2)
Tr[Y³]_LH     = −16/9 (E3-LH)
Tr[Y³]        = 0    (E3-full)
```

Hence anomaly-cancellation realization-invariance holds.

## 5. What this sub-piece does NOT close

- The chiral content itself (LH-doublet + RH SU(2)-singlet completion)
  IS realization-determined — A3 forces it via the canonical staggered-
  Dirac realization. This sub-piece, like PR #670, assumes the chiral
  content as retained-tier input and shows that *given* the chiral
  content, the anomaly-cancellation identities are realization-invariant.
- The *quantization-failure → cancellation-required* step itself
  (Adler-Bell-Jackiw → unitarity violation) is a standard QFT fact,
  cited by `ANOMALY_FORCES_TIME_THEOREM.md` as admission (i). This
  sub-piece does not address that admission; it only shows that the
  identity-level *evaluation* of the anomaly traces is realization-
  invariant.
- The Witten SU(2) Z₂ count cancellation `N_D(LH) = 4` (catalog row
  (C5)) is a separate identity (integer count, not a perturbative
  trace) and is out of scope for this sub-piece.
- The pure-color cubic `SU(3)³` cancellation
  ([`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`](SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md))
  is a separate identity that uses different multiplicity bookkeeping
  (chirality cancellation per color, not hypercharge weighting); its
  algebraic-universality is structurally analogous but is out of scope
  here.
- The B−L gauge-extension anomaly closure
  ([`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md))
  is a separate companion and out of scope.
- 3+1 spacetime forcing
  (`ANOMALY_FORCES_TIME_THEOREM.md`'s downstream Step 3+4) is a
  separate sub-piece in PR #670's §6 list and out of scope here.
- Continuum-limit predictions (`<P>`, `u_0`, mass values) require
  Wilson universality machinery, which is not provided here.

## 6. Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  This is a research-grade follow-on sub-piece extending PR #670's
  algebraic-universality programme. It walks the proofs of the four
  anomaly-cancellation identities (E1), (E2), (E3-LH), (E3-full) and
  verifies each step uses only algebraic-class inputs. Eligible for
  retention upgrade only after independent audit ratification of (a)
  PR #670's framing note + hypercharge sub-piece, (b) this sub-piece,
  (c) the upstream authorities ANOMALY_FORCES_TIME_THEOREM.md and
  LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md.
audit_required_before_effective_retained: true
bare_retained_allowed: false
new_axioms_introduced: 0
new_imports_introduced: 0
```

## 7. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_algebraic_universality_anomaly_cancellation_subpiece.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: anomaly-cancellation identities (E1) Tr[Y] = 0, (E2)
Tr[SU(3)² Y] = 0, (E3-LH) Tr[Y³]_LH = −16/9, and (E3-full) Tr[Y³] = 0
are lattice-realization-invariant per the §2 definition of PR #670.
The proofs in ANOMALY_FORCES_TIME_THEOREM.md and
LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md use only
chiral-content multiplicity counts + hypercharge values + Dynkin index
T(3) = 1/2 + rational arithmetic; no Wilson plaquette / staggered-
phase / BZ-corner / link-unitary content appears as load-bearing
input.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings (framing, definition, theorem,
   proof-walk tables for all four identities, follow-on list, scope
   guards).
2. **Premise-class consistency.** All cited authorities exist on disk.
3. **Anomaly-trace evaluation.** Each of (E1), (E2), (E3-LH),
   (E3-full) evaluated via exact `Fraction` arithmetic to its expected
   rational value (`0`, `0`, `−16/9`, `0`).
4. **LH-only / RH-only decomposition.** The runner confirms
   `Tr[Y³] = Tr[Y³]_LH + Tr[Y³]_RH` with `Tr[Y³]_LH = −16/9` and
   `Tr[Y³]_RH = +16/9`, sum `0`.
5. **Multiplicity-count invariance.** The traces depend on structural
   multiplicity counts `(6, 2, 3, 3, 1, 1)` from chiral content.
6. **Realization-invariance under hypothetical alternatives.** Three
   hypothetical "alternative realizations" each give the same trace
   values.
7. **Proof-walk audit.** Each step of each identity's proof uses only
   algebraic-class inputs (multiplicity counts, hypercharge values,
   Dynkin index, rational arithmetic) and never lattice machinery.
8. **Forbidden-import audit.** Stdlib only, no PDG pins.
9. **Boundary check.** Witten Z₂ count, SU(3)³ cubic, B−L closure,
   3+1 spacetime forcing, continuum-limit class predictions all
   explicitly NOT closed.
10. **Sister-PR pattern.** Cross-references to #670 (parent framing) +
    #655, #664, #667 (convention-admission analogues).

## 8. Cross-references

- Parent framing: PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670) — algebraic-universality framing + first sub-piece (hypercharges); parent of this sub-piece.
- Sister PRs (convention-admission pattern):
  - PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655) — SU(5) embedding consistency (admits SU(5) Killing form).
  - PR [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664) — A3 substep 4 closure (admits (LCL) labelling).
  - PR [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667) — A4 closure (admits (CKN) Killing form).
- Authorities being proof-walked:
  - [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  - [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
- Sister anomaly companion notes (out of scope for this sub-piece, but
  same upstream chain):
  - [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
  - [`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`](SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md)
  - [`BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md`](BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md)
- Hypercharge values used: [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- LH content: [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
- A3 realization gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- Minimal axioms parent: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## 9. Honest scope

**Branch-local theorem.** This note packages the next algebraic-
universality sub-piece in the PR #670 follow-on chain: the four
anomaly-cancellation identities (E1) Tr[Y]=0, (E2) Tr[SU(3)²Y]=0,
(E3-LH) Tr[Y³]_LH = −16/9, (E3-full) Tr[Y³]=0 are proved
realization-invariant by walking the upstream authorities and
verifying each step uses only algebraic-class inputs. It introduces no
new axioms, no new imports, and no PDG pins.

**Not in scope.**

- The Adler-Bell-Jackiw → unitarity-violation step that
  `ANOMALY_FORCES_TIME_THEOREM.md` invokes as admission (i). That is a
  bare external admission to standard QFT and is out of scope here.
- The Witten SU(2) Z₂ count cancellation, SU(3)³ cubic, B−L closure,
  3+1 spacetime forcing — each is a separate sub-piece.
- The framework's actual realization-uniqueness statement (A3 forces
  staggered-Dirac). This sub-piece, like PR #670, assumes the canonical
  realization and asks whether the algebraic predictions would survive
  realization variation IF such variation existed.
- Wilson's continuum-limit universality theorem for the continuum-
  limit-class predictions. That is standard QFT and is the candidate
  (1) work PR #670 partially addresses but does not complete.
