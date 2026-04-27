# Lane 1 `sqrt(sigma)` Retention Gate Audit: EFT-Bridge Decomposition of the 5.6% Gap

**Date:** 2026-04-27
**Status:** retained branch-local audit note on
`frontier/hadron-mass-program-20260427`. Decomposes the 5.6% gap between
the bounded `sqrt(sigma) ≈ 465 MeV` derivation and PDG `440 ± 20 MeV`
into explicit EFT-bridge contributions. Identifies the residual budget
items that must be tightened to promote `sqrt(sigma)` from bounded to
retained (analog of the YT/top transport lane's `1.21%`/`0.755%`
explicit retention budget).
**Lane:** 1 — Hadron mass program (route 3E)
**Workstream:** `hadron-mass-program-20260427`

---

## 0. Statement

The current `sqrt(sigma)` derivation
(`docs/CONFINEMENT_STRING_TENSION_NOTE.md`) gives `~465 MeV` central
with range `[435, 484]` MeV vs PDG `440 ± 20 MeV`. The retained
component of the derivation is structural: confinement (`T = 0`) and
gauge sector identification (`framework SU(3) = standard SU(3) YM`).
The bounded component is the numerical extraction.

**Audit decomposition.** The 5.6% central-value gap and the `[435, 484]`
range arise from five identifiable EFT-bridge contributions:

| Bridge contribution | Magnitude | Type |
|---|---|---|
| (B1) `alpha_s(M_Z)` precision propagation | ~1.0% | retained-input precision |
| (B2) Quenched → dynamical screening factor | ~5% | bounded; needs proper `N_f = 2+1` lattice |
| (B3) `Lambda^(3)` two-loop threshold matching | ~2-3% | bounded; absorbed via Sommer-scale Method 2 |
| (B4) Method 1 (`Lambda_QCD`) vs Method 2 (Sommer) disagreement | ~10% | structural; resolved by selecting Method 2 with (B2) tightening |
| (B5) Framework `SU(3)` ↔ standard `SU(3) YM` identification | unquantified | structural |

**Retention gate.** `sqrt(sigma)` promotes from bounded to retained
when:

- (B1) propagates as a retained-input residual (already achievable;
  requires only declaring the propagation budget);
- (B2) is replaced by a proper `N_f = 2+1` dynamical lattice
  calculation at `beta = 6.0` (currently a rough ×0.96 screening
  factor); this is the **dominant residual** and the load-bearing
  open item for retention;
- (B3) is absorbed into the Sommer-scale Method 2 path (already done
  in the existing bounded derivation; no further work);
- (B4) is closed by selecting Method 2 as the retained route after
  (B2) tightens (already implicit in the current derivation);
- (B5) is sharpened to a structural identification with explicit
  declared residual budget.

**Net.** The single load-bearing open item is **(B2) — quenched →
dynamical screening factor for SU(3) Yang-Mills with `N_f = 2+1` flavors
at `beta = 6.0`**. Closing this with a proper lattice calculation
(rather than the current rough ×0.96 factor) plus declaring (B1) and
(B5) explicitly delivers the YT-lane-style retained-with-budget
statement.

## 1. Premise (retained surface used)

| Identity | Authority |
|---|---|
| `Cl(3)` on `Z^3` minimal axiom stack | `MINIMAL_AXIOMS_2026-04-11.md` |
| `g_bare = 1` and `N_c = 3` → `beta = 6.0` (Wilson plaquette action) | confinement note §3 (arithmetic) |
| `T = 0` confinement of SU(3) YM (Wilson criterion + decades of lattice) | confinement note §3 |
| `<P> = 0.5934` plaquette consistency at `beta = 6.0` | confinement note §3 (verified 0.7% on 4^4 lattice) |
| `alpha_s(M_Z) = 0.1181` retained quantitative (0.2% accuracy) | `ALPHA_S_DERIVED_NOTE.md` |
| Two-loop QCD running with flavor thresholds | textbook QCD running, admitted convention |

The retained component is the structural identification:

> **"The Cl(3)/Z^3 graph-first SU(3) gauge sector is standard SU(3)
> Yang-Mills at `beta = 6.0`."**

This identification is what makes the imported Sommer-scale and
Creutz-ratio lattice numerics applicable to the framework. (B5) below
is the audit of this identification's residual budget.

## 2. Decomposition of the bounded numerics

### 2.1 (B1) — `alpha_s(M_Z)` precision propagation

The framework retains `alpha_s(M_Z) = 0.1181` to `0.2%` accuracy. Per
confinement note §5: a `0.2%` change in `alpha_s(M_Z)` shifts
`sqrt(sigma)` by `~1.2%`. So:

```text
delta_sqrt_sigma / sqrt(sigma)  =  ~6 * (delta_alpha_s / alpha_s)
                                ≈  6 * 0.002  =  ~1.2% propagation
```

This is a **retained-input precision residual**, not a bounded item.
It propagates linearly from the retained input. For YT-lane-style
retention, this contributes `~1%` to the explicit budget.

### 2.2 (B2) — Quenched → dynamical screening

The Sommer-scale derivation at `beta = 6.0` gives:

```text
sqrt(sigma)_quenched   ≈  484 MeV    (pure-gauge SU(3) YM)
sqrt(sigma)_dynamical  ≈  460 MeV    (with N_f = 2+1 screening, rough ×0.96)
```

The `~5%` quenched-to-dynamical correction is the **dominant
residual** in the current bounded derivation. The `×0.96` screening
factor is a rough estimate. A proper `N_f = 2+1` lattice calculation
at `beta = 6.0` with the framework's quark-mass content (or, while
Lane 3 is open, with PDG light-quark masses as a comparator) would
sharpen this to sub-percent.

This is the load-bearing open budget item. Until it is replaced with
a proper dynamical calculation, `sqrt(sigma)` cannot promote past
bounded.

### 2.3 (B3) — `Lambda^(3)` two-loop threshold matching

Method 1 (`Lambda_QCD` route) gives `sqrt(sigma) ≈ 518 MeV` —
overestimates by `~18%` due to accumulated two-loop matching errors
in `Lambda^(3)`. The accumulation comes from:

- five-flavor → four-flavor matching at `m_b`,
- four-flavor → three-flavor matching at `m_c`.

These matchings are textbook QCD; their residuals at two loops are
quantified in PDG (`Lambda_MS-bar^(3)` is `~389 ± 30 MeV` at two
loops, `~3-7%` uncertainty depending on inputs).

Method 2 (Sommer scale at `beta = 6.0`) bypasses this accumulation —
it directly identifies the lattice spacing via `r_0 = 0.472 fm` and
`r_0/a = 5.37`, then reads `sigma a^2 = 0.0465` from the Creutz
ratio. No explicit `Lambda^(3)` is invoked.

So (B3) is **absorbed into the choice of Method 2** as the retained
route. Method 1 remains a consistency cross-check showing the order
of magnitude is correct, not the load-bearing extraction.

### 2.4 (B4) — Method 1 vs Method 2 disagreement

The `~10%` disagreement (`518` vs `460-484`) between the two
extraction methods is a genuine indicator of the bounded status.
However:

- Method 1 is known to be the worse route (accumulates `Lambda^(3)`
  matching errors).
- Method 2 is the standard lattice-QCD reading (Sommer-scale + Creutz
  ratio at `beta = 6.0`).

Selecting Method 2 as the retained route (and demoting Method 1 to
cross-check) closes (B4) **once (B2) is tightened**. Until then,
the methods' disagreement is an honest signal that the lattice-QCD
inputs being imported have their own residual.

### 2.5 (B5) — Framework SU(3) ↔ standard SU(3) YM identification

The structural identification

> "The Cl(3)/Z^3 graph-first SU(3) gauge sector at `beta = 6.0` is
> standard SU(3) Yang-Mills"

is what makes Sommer-scale and Creutz-ratio inputs applicable. Per
confinement note §5: this is the structural claim; the quantitative
string tension is bounded *through this identification*.

The plaquette consistency check (`<P>_framework = 0.5934`,
`<P>_MC at beta=6.0 = 0.5973 ± 0.0006`, 0.7% finite-size shift on
4^4) is the strongest existing support for this identification at
the level of the action. Asymptotic-volume consistency would
sharpen it.

For YT-lane-style retention, (B5) needs to be declared with an
explicit residual budget. Options:

- **Path A (volume scaling):** verify the plaquette consistency
  scales correctly to volumes ≥ 16^4, eliminating the 0.7%
  finite-size residual.
- **Path B (Wilson loop area-law verification):** at volumes ≥ 16^4,
  verify Wilson loops show clean asymptotic area-law decay matching
  standard SU(3) YM at `beta = 6.0`.
- **Path C (independent Creutz-ratio measurement):** measure
  `chi(R, R)` directly on the framework substrate at large `R`, and
  match to the imported `sigma a^2 = 0.0465`.

Any of (A, B, C) tightens (B5). None of these is directly Lane-1
work — they are framework-side methodology validation that the
existing confinement note flags as "Wilson loops on 4^4 lattice show
area-law behavior" (qualitative consistency only, per §6).

## 3. Retention budget table

For a YT-lane-analog retained-with-budget statement, the budget table
is:

| Bridge contribution | Current status | Residual | Path to tighten |
|---|---|---|---|
| (B1) `alpha_s(M_Z)` precision propagation | retained-input | ~1.2% | declare propagation only |
| (B2) Quenched → dynamical screening | bounded (rough ×0.96) | **~5% — dominant** | proper `N_f = 2+1` lattice at `beta = 6.0` |
| (B3) `Lambda^(3)` matching | absorbed via Method 2 | 0% | already done |
| (B4) Method-disagreement | structural choice | 0% | select Method 2 (after B2) |
| (B5) Framework ↔ standard SU(3) YM identification | structural | unquantified | volume-scaling / asymptotic Wilson loops |
| **Total** | bounded | **~5.6%** | **gated on (B2) + (B5) declaration** |

The `5.6%` central-value gap (465 vs 440) lines up cleanly with the
~5% (B2) contribution plus ~1% (B1) propagation. (B3), (B4) are
methodologically resolved; (B5) is structural.

## 4. The single load-bearing open item

**(B2) — quenched → dynamical screening factor for SU(3) Yang-Mills
with `N_f = 2+1` at `beta = 6.0`.**

This is the only bounded numerical residual in the current
derivation. Closing it requires:

- a proper `N_f = 2+1` dynamical-fermion lattice calculation at
  `beta = 6.0`, using the framework's substrate (Wilson or staggered
  fermions on `Z^3`);
- *or*, while Lane 3 quark masses remain open, importing the
  standard lattice-QCD `N_f = 2+1` literature value with PDG light-
  quark masses as a comparator and declaring the residual.

Either path replaces the rough ×0.96 with a sub-percent retention
budget. The first path is preferable for full retention; the second
path supplies a YT-lane-style retained-with-explicit-budget interim
statement.

## 5. What this audit closes and does not close

**Closes:**

- A specific 5-component EFT-bridge decomposition of the bounded
  `sqrt(sigma)` derivation.
- Identification of (B2) as the dominant residual and the single
  load-bearing open item for retention promotion.
- A structural placement of the YT-lane-style retained-with-budget
  pathway.

**Does not close:**

- Promotion of `sqrt(sigma)` from bounded to retained — that requires
  closing (B2).
- A retained `m_pi`, `m_p`, or any other hadron mass.
- The (B5) framework ↔ standard SU(3) YM identification audit (Path A
  / B / C) — that is methodology validation, separate from the (B2)
  numerical residual.

## 6. Cross-references

- `docs/CONFINEMENT_STRING_TENSION_NOTE.md` — primary source for the
  bounded derivation; §5 on coupling running and string tension; §7
  on what is exact vs bounded; §8 on what remains open.
- `docs/ALPHA_S_DERIVED_NOTE.md` — retained `alpha_s(M_Z) = 0.1181`,
  0.2% accuracy.
- `docs/HADRON_MASS_LANE1_THEOREM_PLAN_NOTE_2026-04-27.md` (Cycle 1)
  — Lane 1 closure roadmap; §2.5 on target 3E `sqrt(sigma)` retained
  promotion; §4.1 on Route R6 (this audit).
- `docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md`
  §3.5 — lane file's framing of 3E.
- `docs/MINIMAL_AXIOMS_2026-04-11.md` — minimal accepted axiom stack.

## 7. Boundary

This is an audit / EFT-bridge decomposition, not a theorem. It does
not promote `sqrt(sigma)` from bounded to retained. It does not
retire any input. It identifies the precise residual budget that
the retention promotion must close.

A runner is not authored: the audit is structural review of an
existing bounded derivation; no new symbolic or numerical content
is introduced.
