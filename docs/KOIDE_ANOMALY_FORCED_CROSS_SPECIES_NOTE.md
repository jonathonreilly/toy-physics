# Koide Cone — Anomaly-Forced 3+1 Cross-Species Attack Note

**Date:** 2026-04-17
**Status:** exact structural negative result — the retained anomaly-forced
`3+1` temporal surface is FLAVOR-TRIVIAL on the `hw=1` triplet and does NOT
generate cross-species matrix elements `b = K_{ij} \neq 0`. Verdict:
`ANOMALY_FORCED_MIXING_GENERATES_B=FALSE`.
**Script:** `scripts/frontier_koide_anomaly_forced_cross_species.py`
**Authority role:** successor-candidate closure note for gap `G5`
(charged-lepton Koide cone-forcing step). Rules out candidate (6) in the
five-agent G5 status note's successor list
(`docs/CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md`), namely
"anomaly-forced 3+1 cross-species propagator on a non-minimal temporal
block", as a viable Koide-cone-forcing mechanism. The retained anomaly-
forced `3+1` theorem does not break the pure-APBC translation-character
orthogonality that Agent 4 isolated as the structural obstruction.

## Safe statement

On the retained `Cl(3)/Z^3` framework surface, the runner
`frontier_koide_anomaly_forced_cross_species.py` symbolically establishes
the following facts:

1. **Retained anomaly arithmetic (re-validation, EXACT).** The left-handed
   content `(2,3)_{+1/3} + (2,1)_{-1}` has `Tr[Y]=0`, `Tr[Y^3]=-16/9 \neq 0`,
   `Tr[SU(3)^2 Y]=1/3 \neq 0` — the ABJ trigger. Augmented by the
   retained SM-branch right-handed singlet completion `u_R=(1,3)_{+4/3}`,
   `d_R=(1,3)_{-2/3}`, `e_R=(1,1)_{-2}`, `\nu_R=(1,1)_{0}`, all five
   anomaly traces `Tr[Y]`, `Tr[Y^3]`, `Tr[SU(3)^2 Y]`, `Tr[SU(2)^2 Y]`,
   Witten vanish identically. Chirality operator `\gamma_5` exists on the
   `3+1` surface because `d = d_s + d_t = 4` is even, so the Clifford
   volume element `\omega` anticommutes with every `\gamma_\mu`.

2. **Flavor-trivial action on `hw=1` triplet (EXACT).** Every retained
   anomaly-forced ingredient acts trivially on the `hw=1` flavor factor:

   - `\gamma_5` acts on spinor indices only (identity on species).
   - The RH singlet completion carries the SAME hypercharge across all
     three generations (`e_R : Y = -2`, etc.), so the RH-forced insertion
     is species-blind.
   - All five anomaly traces VANISH on the SM branch, so any anomaly-
     weighted insertion contributes zero.
   - The chirality-forcing Dirac mass bilinear
     `\psi_L^\dagger \gamma_0 \psi_R` is species-blind without a Higgs
     VEV / Yukawa input (explicitly G1 territory, out of scope).
   - The chirality projector `(1 \pm \gamma_5)/2` is species-blind.

3. **Non-minimal temporal block (EXACT).** On every tested APBC block
   with `L_t \in \{6, 8, 12, 16\}` augmented by the species-blind
   anomaly-forced insertion
   ```
   D \to D + (r/2) (1 + \gamma_5) m_\chi \cdot I_{hw=1}
   ```
   the perturbed resolvent still commutes with each lattice translation
   `T_x, T_y, T_z`. For every species pair `(i, j)` with `i \neq j`, the
   joint characters disagree on at least one translation axis, so
   `P_i (D + r m_\chi I)^{-1} P_j = 0` identically. The off-diagonal
   kernel `K_{ij}^{(\mathrm{anom})} = 0` on every tested `L_t > 4` block.

4. **Structural no-go extension (EXACT).** Agent 4's pure-APBC no-go
   `b = 0` extends unchanged through the anomaly-forced temporal
   insertion. The circulant `(a, b)` kernel on the `hw=1` triplet still
   collapses to `a \cdot I_3`; the spectral-amplitude vector still lives
   on the trivial `C_3` character (`|z| = 0`); the Koide cone
   `a_0^2 = 2 |z|^2` remains unreachable on this attack surface.

5. **Sector sensitivity (EXACT, but insufficient).** The anomaly theorem
   carries a sector-SCALE signal from the different hypercharges of
   `Q_L` vs `L_L`. The per-doublet `Tr[Y^3]` ratio is
   `Q_L : L_L = -1/27 : 1` and the per-doublet SU(2)^2 Y ratio is
   `Q_L : L_L = 1 : -1`. But within a single sector, all three generations
   carry the SAME Y, so the anomaly-forced operator is species-blind in
   each sector separately. The sector dependence therefore produces a
   global scale difference between leptons and quarks but CANNOT generate
   within-sector cross-species mixing. Agent 3's finding
   `Q_\ell = 2/3`, `Q_d \approx 0.73`, `Q_u \approx 0.85` is not
   resolvable from this mechanism.

## Three-outcome verdict

The task prompt's three expected outcomes were:

- `ANOMALY_FORCED_MIXING_FORCES_KOIDE=TRUE` — the anomaly-forced `3+1`
  structure both lifts `b = 0` AND forces `a_0^2 = 2|z|^2`.
  Massive positive result.

- `ANOMALY_FORCED_MIXING_GENERATES_B=PARTIAL` — the structure generates
  `b \neq 0` but does not force the Koide cone. Necessary but not sufficient.

- `ANOMALY_FORCED_MIXING_GENERATES_B=FALSE` — the anomaly-forced
  structure does NOT generate cross-species matrix elements at the
  relevant order. Candidate is cleanly ruled out.

The runner returns

```
ANOMALY_FORCED_MIXING_GENERATES_B=FALSE.
```

Step (a) (necessary) fails, so step (b) (sufficient) is moot. The
retained anomaly-forced `3+1` surface does not break the
translation-character orthogonality that isolates `b = 0` on pure APBC.

## Theorem (anomaly-forced hw=1 flavor triviality, EXACT)

> **Theorem (anomaly-forced flavor triviality on `hw=1`).**
> Let `D` be the framework-native staggered Dirac operator on a pure-APBC
> temporal block of length `L_t`, and let `\mathcal{O}_{\mathrm{anom}}` be
> any retained anomaly-forced insertion built from (a) the Clifford volume
> element `\gamma_5` on the `3+1` spacetime, (b) the anomaly-forced RH
> singlet completion hypercharges on the SM branch, (c) anomaly traces
> `Tr[Y], Tr[Y^3], Tr[SU(3)^2 Y], Tr[SU(2)^2 Y]`, or (d) the chirality
> projector `(1 \pm \gamma_5)/2`. Then on the retained `hw=1` triplet,
> `\mathcal{O}_{\mathrm{anom}}` acts as `c \cdot I_3` in species space for
> some scalar `c` (possibly zero). Consequently the perturbed resolvent
> `(D + \mathcal{O}_{\mathrm{anom}})^{-1}` commutes with each lattice
> translation `T_x, T_y, T_z`, and the off-diagonal observable-principle
> source-response kernel `K_{ij} = 0` for every `i \neq j` and every
> `L_t`. The circulant `(a, b)` form collapses to `a \cdot I_3`; the
> Koide cone `a_0^2 = 2|z|^2` with `|z| > 0` is NOT reachable from this
> mechanism.

**Proof sketch (fully symbolic in the runner).**
(i) `\gamma_5` is the phased Clifford volume element on the Dirac
spinor space and acts as the identity on flavor/species indices.
(ii) The SM-branch RH singlet completion assigns ONE hypercharge per
species type (`u_R : +4/3`, `d_R : -2/3`, `e_R : -2`, `\nu_R : 0`), and
the framework's retained content places all three generations of a given
sector in the SAME RH representation, so the RH-chirality mass-like
insertion is species-blind on the `hw=1` flavor factor.
(iii) All five anomaly traces vanish on the full SM branch (Part 0 of
the runner), so any anomaly-weighted flavor operator built from these
traces contributes zero.
(iv) The chirality-forcing Dirac mass bilinear requires a Higgs-VEV /
Yukawa insertion to carry flavor structure, which is explicitly G1
territory (out of scope).
(v) The chirality projector `(1 \pm \gamma_5)/2` is species-blind by
(i).
Hence every anomaly-forced ingredient is `c \cdot I_3` on species, so
the perturbed resolvent is still translation-invariant, and Agent 4's
translation-character orthogonality argument applies unchanged: for
every pair `(i, j)` with `i \neq j`, the characters `\chi_i, \chi_j`
disagree on at least one (in fact two) of `T_x, T_y, T_z`, and
`P_i (D + \mathcal{O}_{\mathrm{anom}})^{-1} P_j = 0`. QED.

## What this does not claim

This note does **not** claim:

- that the anomaly-forced theorem is false, incomplete, or in any way
  diminished. The retained theorem
  (`docs/ANOMALY_FORCES_TIME_THEOREM.md`, runner `PASS=85+2`) remains
  fully in force. The claim is narrower: the theorem's temporal content
  is flavor-trivial on the `hw=1` triplet and cannot by itself be the
  Koide-cone-forcing primitive.

- that no combination of the anomaly-forced surface with a DIFFERENT
  retained primitive could produce `b \neq 0`. Specifically, the
  combinations `anomaly + Higgs-Yukawa` (G1 thread),
  `anomaly + SU(2)_L exchange` (Agent 7 lane), and
  `anomaly + color dressing` (Agent 6 lane) are NOT ruled out by this
  runner. This note rules out ONLY the stand-alone anomaly-forced
  surface as the Koide-cone-forcing primitive.

- that the anomaly-forced surface is observationally irrelevant. It
  still carries the global sector-scale signal (`Tr[Y^3]` and
  `Tr[SU(2)^2 Y]` ratios between `Q_L` and `L_L`) that distinguishes
  leptons from quarks at the anomaly-coefficient level.

- that the Wilson-improvement mechanism (Agent 4's Mechanism 3) fails.
  That is a different retained primitive (higher-derivative lattice
  operators) with a distinct scaling `b_{\mathrm{Wilson}} \sim r (a/L_t)^2`,
  and is not investigated here.

- any numerical match to observed charged-lepton masses, Koide `Q`, or
  sectoral mass-ratio ratios. No PDG inputs, no fitted values, no Higgs
  VEV insertions were imported. All symbolic output is framework-native.

- that the retained `C_F - T_F = 5/6` color structure providing the
  tantalizing `Q_d / Q_\ell \approx \sqrt{6/5}` fingerprint is relevant
  or irrelevant. That is Agent 6's lane.

## Relationship to retained authorities

This note is a successor-candidate closure note on the primary Koide lane
`CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md`. It specifically
closes the sixth successor candidate listed there ("anomaly-forced 3+1
cross-species propagator on a non-minimal temporal block") as cleanly
negative. Cross-references:

- [CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md)
  — G5 consolidated status note. This runner addresses successor
  candidate (6).
- [CHARGED_LEPTON_CURVATURE_LT_EXTENSION_NOTE.md](./CHARGED_LEPTON_CURVATURE_LT_EXTENSION_NOTE.md)
  — Agent 4's retained pure-APBC structural no-go. Inherited as boundary
  condition; this note shows the no-go survives the anomaly-forced
  insertion.
- [OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md](./OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE.md)
  — Agent 5's retained observable-principle character-symmetry
  insufficiency. Identified this lane as one concrete successor.
- [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md) —
  retained anomaly-forced `3+1` surface and RH singlet completion,
  providing the entire content universe tested here.
- [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](./ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
  — retained one-generation closure with the RH singlet assignments
  used as flavor-trivial inputs.
- [CPT_EXACT_NOTE.md](./CPT_EXACT_NOTE.md) — retained free-staggered
  CPT exactness, ensuring the chirality / RH completion does not spoil
  the CPT-even kernel structure that the observable principle relies on.
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
  — retained `hw=1` algebra, translation characters, and irreducibility
  that the no-go argument uses.
- [KOIDE_SECTORAL_UNIVERSALITY_NOTE.md](./KOIDE_SECTORAL_UNIVERSALITY_NOTE.md)
  — Agent 3's sectoral universality finding, which the anomaly surface
  cannot resolve.

Relationship to the four Part-B mechanisms in Agent 4's note:

- [MECH 1] Two-Higgs insertion — G1 thread, not in scope here.
- [MECH 2] `SU(2)_L` gauge exchange — Agent 7 lane, not overlapped here.
- [MECH 3] Wilson / improvement — distinct primitive, not tested.
- [MECH 4] Non-APBC temporal structure — partially overlapping with
  this runner's "non-minimal temporal block" scope but the target here
  is the ANOMALY-FORCED content on the block, not a generic non-APBC
  modification. The runner tests the non-minimal APBC block augmented
  by an anomaly-forced species-blind insertion; the result (`b = 0`)
  shows the anomaly-forced part is insufficient on its own, consistent
  with but stronger than Agent 4's more general Mechanism 4
  scaling `b_M \sim M_{ij}`.

Related G5 sister lanes (explicitly NOT overlapped):

- Agent 6 (color-theoretic sector correction, `C_F - T_F = 5/6`).
- Agent 7 (`SU(2)_L` gauge exchange cross-species propagator).

## Dependency contract

Retained authorities inherited by this runner (their runners must pass
before this result is trusted; this runner does not re-execute them):

- `frontier_anomaly_forces_time.py` — retained `3+1` surface and SM-
  branch anomaly cancellation (`PASS=85+2, FAIL=0` on main).
- `frontier_three_generation_observable_theorem.py` — retained `hw=1`
  algebra, translation characters, cycle structure (`PASS=47, FAIL=0`).
- `frontier_charged_lepton_curvature_lt_extension.py` — Agent 4's
  retained pure-APBC structural no-go (`PASS=44, FAIL=0`). The anomaly-
  forced no-go extension proved here strictly inherits this boundary
  condition.
- `frontier_observable_principle_character_symmetry.py` — Agent 5's
  retained observable-principle insufficiency (`PASS=30, FAIL=0`).
- `frontier_plaquette_self_consistency.py` — retained canonical `u_0`,
  `\langle P \rangle`, `\alpha_{LM}`; not numerically consumed here
  (the runner is symbolic in `m_i, u_0, L_t, r, m_\chi`), but
  interpretation inherits these as the retained physical scales.
- `frontier_right_handed_sector.py` — retained RH singlet completion
  used in Part 0 and Part 2 of this runner.

No observed charged-lepton masses, quark masses, Yukawa couplings,
gauge couplings, or Higgs VEV were imported. No PDG inputs, no fitted
values. All symbolic output is framework-native.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the retained anomaly-
> forced `3+1` temporal structure (Clifford volume element `\gamma_5`,
> SM-branch right-handed singlet completion with fixed hypercharges,
> vanishing anomaly traces on the SM branch) acts as `c \cdot I_3` on
> the retained `hw=1` flavor triplet. The perturbed observable-principle
> resolvent therefore commutes with each lattice translation
> `T_x, T_y, T_z`, and the off-diagonal source-response curvature
> `K_{ij}` vanishes for every `i \neq j` on every tested non-minimal
> APBC block `L_t \in \{6, 8, 12, 16\}`. The Koide cone
> `a_0^2 = 2|z|^2` is not reachable from the stand-alone anomaly-forced
> mechanism. The anomaly-forced surface carries a sector-SCALE signal
> (per-doublet `Tr[Y^3]` ratio `Q_L : L_L = -1/27 : 1`) but no within-
> sector cross-species mixing. This closes, cleanly and symbolically,
> the sixth successor candidate in the five-agent G5 status note,
> leaving the Higgs-Yukawa / `SU(2)_L` / Wilson / color-dressing lanes
> as the remaining concrete targets.

## Validation

- `scripts/frontier_koide_anomaly_forced_cross_species.py`

Current runner state:

- `frontier_koide_anomaly_forced_cross_species.py`: `PASS=42`, `FAIL=0`
- `ANOMALY_FORCED_MIXING_GENERATES_B=FALSE`

## Status

**PROPOSED** — structural negative result for the anomaly-forced 3+1
cross-species candidate. Rules out successor candidate (6) in the G5
status note. The Koide-cone attack now further shifts to the remaining
four candidates: (1) two-Higgs / Z_3 doublet-block (G1 thread),
(2) `SU(2)_L` gauge exchange (Agent 7), (3) Wilson / improvement,
(5) color-theoretic sector correction (Agent 6).
