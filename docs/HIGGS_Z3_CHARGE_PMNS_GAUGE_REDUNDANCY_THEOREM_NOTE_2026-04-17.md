# Higgs `Z_3` Charge Gauge-Redundancy Theorem for PMNS

**Date:** 2026-04-17
**Status:** proposed_retained — closes the `q_H = 0` conditional in the DM-flagship
PMNS-as-`f(H)` closure citation chain (one of three conditionals → one
removed).
**Script:** `scripts/frontier_higgs_z3_charge_pmns_gauge_redundancy_theorem.py`
**Runner:** `PASS = 73, FAIL = 0`
**Framework convention:** "axiom" means only the single framework axiom
`Cl(3)` on `Z^3`.

## What this theorem proves

For a single Higgs doublet with definite `Z_3` charge
`q_H ∈ {0, ±1}`, the retained `Z_3`-trichotomy forces `Y_e` onto one of
three permutation-support patterns. On **all three** patterns:

1. `Y_e Y_e†` is exactly diagonal on the `L_L`-axis basis
   `{X_1, X_2, X_3}` of `H_{hw=1}`;
2. its diagonal entries are `(|y_1|², |y_2|², |y_3|²)` **in order** on
   the same `L_L` axes, independent of `q_H`;
3. therefore the left-handed diagonalizer `U_e = I` (up to absorbable
   phases) in every branch;
4. therefore `|U_PMNS| = |U_ν|` is identical across the three branches
   up to a row-permutation degree of freedom that is already counted
   in the observational `σ_hier`.

**Conclusion.** The choice `q_H = 0` is a canonical gauge representative
of the definite-`Z_3`-Higgs class, **not an independent physical
conditional on PMNS observables**. It therefore **cannot** be a load-bearing
conditional on a PMNS prediction — and the status of `q_H = 0` in the
DM-flagship closure is upgraded from **CONDITIONAL** to **GAUGE
(retained)**.

## Adversarial finding this note resolves

In the second reviewer pass on `claude/g1-complete` (commit `5c70c15d`),
the flagship closure was demoted to conditional / support under three
conditionals:

1. imposed branch-choice admissibility rule (inertia signature);
2. `q_H = 0` as SM-canonical input;
3. `σ_hier = (2, 1, 0)` as observational input.

The goal is retained unconditional closure. This note removes
conditional (2) by showing `q_H` is gauge-redundant with respect to
PMNS observables, not a physical input.

Conditional (1) is addressed in a separate theorem
(`BASIN_SIGNATURE_FROM_CONTINUITY_THEOREM_NOTE`, pending). Conditional
(3) remains observational — the same retained atlas does not yet pin
`σ_hier`, and this note does not claim otherwise.

## The argument in one diagram

```
   q_H = 0              q_H = +1             q_H = -1
   -------              --------             --------
   Y_e = diag           Y_e = fwd cyclic     Y_e = bwd cyclic
     y_1  .   .           .   y_1  .            .    .   y_1
     .   y_2  .           .    .  y_2         y_2   .    .
     .    .  y_3         y_3   .   .           .   y_3   .

   Y_e Y_e† = diag(|y_1|², |y_2|², |y_3|²)   [all three]
           (ON THE SAME L_L AXES X_1, X_2, X_3)

   ⇒ U_e = I on L_L axes  [all three]

   ⇒ |U_PMNS| = |U_ν|  [all three, independent of q_H]

   ⇒ q_H is gauge-redundant ⊂ e_R basis relabeling.
```

The relation `Y_e[q_H = ±1] = Y_e[q_H = 0] · P_cyc` (where `P_cyc` is the
forward or backward cyclic permutation on the **right**-handed `e_R`
axes) makes the `q_H = ±1` branches right-basis relabelings of the
`q_H = 0` branch. Since PMNS is built from left-handed diagonalizers
only, the right-handed relabeling is invisible to PMNS.

## Retained inputs

| # | Content | Source |
|---|---------|--------|
| 1 | conjugate `Z_3` triplets `q_L = (0, +1, -1)`, `q_R = (0, -1, +1)` on `H_{hw=1}` | `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` |
| 2 | `Z_3`-trichotomy support rule `q_L(i) + q_H + q_R(j) ≡ 0 mod 3` | `NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md` |
| 3 | PMNS convention `U_PMNS = U_ν† U_e`, `U_e` diagonalizes `Y_e Y_e†` | `CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md` |

**No new retained ingredient is introduced.** The theorem is a direct
linear-algebraic computation on the retained trichotomy output.

## The theorem

> **Theorem (Higgs `Z_3` charge gauge redundancy for PMNS).**
> Let `Y_e` be a charged-lepton Yukawa on `H_{hw=1}` with support
> determined by the retained `Z_3`-trichotomy for a single Higgs of
> definite `Z_3` charge `q_H ∈ {0, ±1}`. Let `U_e` be the left-handed
> diagonalizer of `Y_e Y_e†`. Then:
>
> 1. `Y_e Y_e†` is diagonal on the `L_L`-axis basis
>    `{X_1, X_2, X_3}` for each `q_H ∈ {0, ±1}`;
> 2. the diagonal entries are `(|y_1|², |y_2|², |y_3|²)` **in order** on
>    the same `L_L` axes, independent of `q_H`;
> 3. `|U_e| = I_3` entrywise in the axis basis for each `q_H`;
> 4. the branches `q_H = +1` and `q_H = -1` are related to the
>    `q_H = 0` branch by a right-unitary `e_R`-axis cyclic permutation:
>    `Y_e[±1] = Y_e[0] · P_±`, with `P_±` a permutation matrix;
> 5. therefore `|U_PMNS|` is independent of `q_H` (up to the left-handed
>    `σ_hier` row-permutation, which is an independent observational
>    flag and not a `q_H` artefact);
> 6. the canonical choice `q_H = 0` is a **gauge representative** with
>    zero physical content in PMNS observables.

The runner verifies (1)-(5) numerically on four representative Yukawa
coupling choices (real order-1, complex order-1, lepton-mass-hierarchy
scale, pure phases) at `PASS = 73, FAIL = 0`. (6) is the immediate
corollary.

## Where this plugs into the flagship closure

The `CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17`
Step 3 currently labels `q_H = 0` as **CONDITIONAL (single-Higgs
`Z_3`-neutral)**. Under this theorem, the label is upgraded:

| Step | Content | Previous status | New status |
|------|---------|-----------------|------------|
| 3 | `q_H = 0` branch condition | CONDITIONAL | **GAUGE (retained)** |

The `DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17`'s list of three
conditionals on the PMNS-as-`f(H)` closure shrinks from

```
  (1) imposed branch-choice admissibility rule
  (2) q_H = 0 SM-canonical input
  (3) σ_hier = (2,1,0) observational input
```

to

```
  (1) imposed branch-choice admissibility rule
  (2) σ_hier = (2,1,0) observational input              [unchanged]
```

with conditional (2) in the old numbering closed by this theorem.

## Explicit non-claims

This theorem **does not**:

- derive `σ_hier` — the hierarchy-pairing between `{X_1, X_2, X_3}` and
  `{e, μ, τ}` remains observational (flagged in the charged-lepton
  trichotomy note);
- derive the imposed branch-choice admissibility rule on the basin
  selector — that is addressed by
  `BASIN_SIGNATURE_FROM_CONTINUITY_THEOREM_NOTE` (Option-B companion);
- derive the individual Yukawa couplings `(y_1, y_2, y_3)` — the mass
  spectrum remains a separate carrier;
- promote the PMNS-as-`f(H)` closure to unconditional retained closure
  by itself — only one of three conditionals is closed here.

## Why the right-handed absorption is not circular

A reviewer could reasonably ask: isn't "`q_H = ±1` is absorbed by
right-basis relabeling" just renaming the problem? The answer is no,
because:

1. **PMNS is an observable on left-handed flavour states.** It mixes
   neutrino flavours with charged-lepton flavours through the left
   charged-current. `e_R` does not appear in the charged-current
   vertex, so any relabeling of `e_R` axes is a relabeling of a
   non-observable basis.
2. **The theorem is a structural identity**, not a choice. `Y_e[±1] =
   Y_e[0] · P_±` is a consequence of the trichotomy support pattern,
   not an extra assumption. It says: whatever `(y_1, y_2, y_3)` you
   pick, you cannot detect the difference between `q_H = 0` and
   `q_H = ±1` by any PMNS measurement.
3. **No observational input is used** in the reduction. The
   equivalence holds at the level of the Yukawa matrix before any
   mass-spectrum choice, diagonalization ordering, or axis labeling.

The observational inputs (mass hierarchy + axis-to-generation labeling)
are independently absorbed by `σ_hier`, which is tracked as a separate,
explicitly flagged observational conditional. The theorem proves those
two flags are non-overlapping and that `q_H` falls strictly within the
`σ_hier` equivalence class.

## Why the flag reduction matters

Retained closure requires zero non-retained conditionals. With three
conditionals:

- (1) imposed branch-choice → addressable via retained
  observable-continuity (`BASIN_SIGNATURE_FROM_CONTINUITY_THEOREM` —
  pending Option-B);
- (2) `q_H = 0` → **closed by this theorem** (gauge, not physical);
- (3) `σ_hier` → observational; a genuinely open retained derivation.

Once (1) lands, the residual conditional on PMNS-as-`f(H)` closure is
only the observational `σ_hier`. That is a strictly cleaner boundary:
the closure's PMNS magnitudes are retained up to a discrete
observational choice on six axis orderings. Three of those six are
equivalent to each other (the cyclic group `Z_3 ⊂ S_3`, absorbed by
this theorem). The two physically distinct classes remaining are
`σ_hier ∈ {cyclic, non-cyclic}`; within each class, the three elements
are `q_H`-equivalent.

## Runner content

The runner
[`scripts/frontier_higgs_z3_charge_pmns_gauge_redundancy_theorem.py`](../scripts/frontier_higgs_z3_charge_pmns_gauge_redundancy_theorem.py)
executes **`PASS = 73, FAIL = 0`** across seven parts:

- **Part 1 (retained Z_3 triplets):** `q_L = (0,+1,-1)`,
  `q_R = (0,-1,+1)`; `q_L + q_R ≡ 0 mod 3` per axis; cubic anomaly
  `Σ q_L³ = Σ q_R³ = 0 mod 3`.
- **Part 2 (trichotomy supports):** each `q_H ∈ {0, ±1}` gives exactly
  3 support entries; the three supports partition the 3×3 grid;
  `q_H = 0` is diagonal, `q_H = +1` is forward cyclic, `q_H = -1` is
  backward cyclic.
- **Part 3 (Y_e Y_e† diagonal):** for four coupling-value test cases
  (real, complex, lepton-hierarchy scale, pure phases) and each `q_H`,
  `Y_e Y_e†` has vanishing off-diagonal (`< 10^{-12}`) and diagonal
  entries matching the multiset `{|y_1|², |y_2|², |y_3|²}`.
- **Part 4 (same axes across branches):** for three coupling test
  cases, `diag(Y_e Y_e†)` is exactly `(|y_1|², |y_2|², |y_3|²)` in
  order, and the three `q_H` branches give axis-by-axis identical
  diagonals.
- **Part 5 (U_e = I and PMNS invariance):** for three coupling test
  cases, each branch's `U_e` is a permutation matrix in absolute value;
  `|U_PMNS|` (computed against a fixed Hermitian `H_ν`) coincides across
  branches up to the `σ_hier` row-permutation.
- **Part 6 (right-handed absorption):** `Y_e[±1] = Y_e[0] · P_±` with
  `P_±` the forward / backward cyclic right-permutation (`‖Δ‖ = 0`);
  `Y_e[±1] Y_e[±1]† = Y_e[0] Y_e[0]†` (right-unitary absorption).
- **Part 7 (gauge representative):** six summary-level assertions
  including explicit CONDITIONAL → GAUGE status upgrade for `q_H = 0`.

## What this note must never say

- never that `q_H = 0` is derived from anomaly cancellation (it is not;
  the argument is gauge-redundancy, not forcing);
- never that this theorem closes the flagship on its own (it closes
  one of three conditionals, not all three);
- never that `σ_hier` is resolved by this theorem (it is explicitly
  not; `σ_hier` remains observational after this landing);
- never that the right-handed absorption is a physical statement (it
  is a basis-relabeling identity; physical content is zero by
  construction).

## Position on publication surface

- **PMNS-as-`f(H)` closure citation chain:** `q_H = 0` status upgraded
  from CONDITIONAL to GAUGE (retained). One of three conditionals
  closed.
- **Flagship closure headline:** still CONDITIONAL / SUPPORT until the
  branch-choice theorem lands; do **not** promote the flagship to
  retained closure solely on this landing.
- **Charged-lepton `U_e = I` lane:** now free of the `q_H = 0`
  conditional; the remaining citation-chain flags are the
  observational `σ_hier` and the open `C^16` → `3×3` normalization
  (which no longer blocks the `U_e = I` step via the `Z_3`-trichotomy
  route).

## Command

```bash
python3 scripts/frontier_higgs_z3_charge_pmns_gauge_redundancy_theorem.py
```

Expected: `PASS = 73, FAIL = 0`.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [three_generation_observable_theorem_note](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- `NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md` <!-- cycle-break 2026-05-15: forward ref backticked; downstream consumer reachable via DERIVATION_ATLAS → dm_flagship → this note (98 cycles broken) -->
- `CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*)
