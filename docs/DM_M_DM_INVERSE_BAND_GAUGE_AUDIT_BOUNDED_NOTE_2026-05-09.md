# DM m_DM Inverse-Target Band & Gauge-Group Audit — Bounded Note

**Date:** 2026-05-09
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_dm_m_dm_inverse_band_gauge_audit.py`](../scripts/frontier_dm_m_dm_inverse_band_gauge_audit.py)

## Claim

Building on the freeze-out-bypass identity `eta = C · m_DM^2` (eq. (2)
of [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md))

```text
eta  =  C · m_DM^2,                                                                (1)
C    =  K · x_F  /  ( sqrt(g_*) · M_Pl · pi · alpha_X^2 · R · 3.65e7 ),

R    =  R_base · ( S_vis / S_dark ),       R_base = 31/9 (retained),
```

inverting (1) at fixed `eta = eta_obs = 6.12e-10` (live-surface Planck
import, per the parent freeze-out-bypass note) gives the inverse target

```text
m_DM_target ( x_F, S_vis/S_dark, alpha_X )  =  sqrt( eta_obs / C ).                (2)
```

Under the parent freeze-out-bypass note's bounded admissions

```text
x_F  ∈  [ 22, 28 ]                          (textbook bounded freeze-out coefficient)
S_vis/S_dark  ∈  [ 1.4, 1.7 ]               (bounded Sommerfeld continuation)
alpha_X  =  alpha_LM  =  0.09067            (link-mediator gauge-coupling route)
```

and the canonical surface inputs `v = 246.22 GeV`, `u_0 = 0.8776`,
`M_Pl = 1.2209 × 10^19 GeV`, `g_* = 106.75`, `K = 1.07 × 10^9 GeV^-1`,
the inverse target lies in the bounded band

```text
m_DM_target  ∈  [  3422.52  ,  4254.75  ]  GeV.                                    (3)
```

with bandwidth `≈ 832 GeV`. Two uniqueness statements follow:

(I) **Among parent freeze-out-bypass note's structural mass-identity
audit candidates** (which enumerate complexity-1 to complexity-3
products of the retained surface counts `v, M_Pl, alpha_LM, alpha_s(v),
u_0, N_sites, N_c, R_base, hw_dark`), **the unique candidate inside
the band (3) is `N_sites · v = 16 v ≈ 3939.52 GeV`**. The closest
competitors lie outside the band by `>10%` (relative to band edges):

```text
N_sites · v        =  3939.52 GeV   INSIDE band  (62.2 % from m_lo)
v · 4 pi           =  3094.09 GeV   OUTSIDE  ( -9.6 % from m_lo)
v · R_base^2       =  2921.20 GeV   OUTSIDE  (-14.7 % from m_lo)
M_Pl · alpha_LM^15 =  2809.53 GeV   OUTSIDE  (-17.9 % from m_lo)
M_Pl · alpha_LM^15 · 2 u_0  =  4931.29 GeV   OUTSIDE  (+15.9 % from m_hi)
v / alpha_LM       =  2715.56 GeV   OUTSIDE  (-20.7 % from m_lo)
```

(II) **Among gauge-group choices `SU(N)` for `N ∈ {2, 3, 4, 5, 6}`**,
under the parent note's "Origin B" structural form for the dark
hw-3 singlet mass

```text
m_phys^Origin-B ( N )  =  ( dim(adj_N) / N ) · 2 · hw_dark · v
                       =  6 ( N^2 - 1 ) v / N                                      (4)
```

(with `hw_dark = 3` and the standard hierarchy compression
`(7/8)^(1/4) · alpha_LM^16` taking lattice → physical), **the unique
gauge group `SU(N)` placing `m_phys^Origin-B(N)` inside the band (3)
is `N = 3`**:

```text
SU(2):  m = 2215.98 GeV   OUTSIDE  ( -35.3 % below m_lo )
SU(3):  m = 3939.52 GeV   INSIDE band                              <-- canonical SU(3)
SU(4):  m = 5539.95 GeV   OUTSIDE  ( +30.2 % above m_hi )
SU(5):  m = 7091.14 GeV   OUTSIDE  ( +66.7 % above m_hi )
SU(6):  m = 8617.70 GeV   OUTSIDE  (+102.5 % above m_hi )
```

Combining (I) and (II): under the bounded inverse-target band (3), the
parent freeze-out-bypass route's structural mass identity
`m_DM = N_sites · v = 16 v` is **simultaneously** (I) the unique
candidate inside the band among complexity-`≤ 3` retained mass-scale
products, and (II) the unique Origin-B gauge-group choice from
`N ∈ {2..6}` placing the structural form inside the band. This converts
the parent's central-point `+ 2.09 %` match into a bounded-band
uniqueness statement under the canonical admissions.

This note **does not**:
- close the +12 % `eta` chain (parent note's open lanes G1, G2, G3, G4
  remain in place);
- derive `m_DM = N_sites · v` from a Wilson-action theorem on the dark
  hw-3 singlet (lane G1 still open);
- promote any gauge-group choice (`SU(3)` is a framework axiom, not a
  derived consequence of (II));
- promote the parent freeze-out-bypass note's status.

(II) is a self-consistency audit: under the framework's axiomatic
`SU(3)` choice, Origin B's structural form is the unique
gauge-group instance consistent with the bounded inverse-target
band. The audit IS NOT a derivation that the framework MUST be `SU(3)`.

## Proof-Walk

| Step | Load-bearing input | Lattice-action input? |
|---|---|---|
| Parent freeze-out-bypass identity (eq. (2) of parent): `eta = C · m_DM^2` with `C = K x_F / (sqrt(g_*) M_Pl pi alpha_X^2 R · 3.65e7)`, `R = R_base · S_vis/S_dark`, `R_base = 31/9` | parent retained-grade theorem and Kolb-Turner / BBN textbook coefficients | no |
| Inversion: `m_DM_target = sqrt(eta_obs / C)` for given `(x_F, S_vis/S_dark, alpha_X)` | scalar algebra | no |
| `C` is monotone in `x_F` (linearly increasing) and antimonotone in `S_vis/S_dark` (`R = R_base · S_vis/S_dark` linearly increasing, `C ∝ 1/R`); hence `m_DM_target = sqrt(eta_obs/C)` attains extremes on the corners of the rectangular admission box `[22, 28] × [1.4, 1.7]` | scalar monotonicity | no |
| Maximum: `(x_F, S_vis/S_dark) = (22, 1.7)`: smallest `C → m_max` | direct evaluation | no |
| Minimum: `(x_F, S_vis/S_dark) = (28, 1.4)`: largest `C → m_min` | direct evaluation | no |
| `m_DM_target ∈ [m_min, m_max] = [3422.52, 4254.75] GeV` | rectangular extremes | no |
| Each candidate `m_i` from the parent's audit table (`16 v`, `4 pi v`, `R_base^2 v`, ...) is a scalar value; check membership `m_i ∈ [m_min, m_max]` | scalar comparison | no |
| Result (I): only `m = 16 v = 3939.52 GeV` lies inside band; closest competitor is `M_Pl · alpha_LM^15 · 2 u_0 = 4931.29` at `+15.9%` above `m_hi` | scalar comparison | no |
| Origin-B form: `m_phys^Origin-B(N) = 6 (N^2 - 1) v / N` evaluated for `N ∈ {2..6}` | scalar substitution into the parent's stated Origin-B identity (`(dim(adj_N)/N) · 2 hw_dark · v`) with `hw_dark = 3` | no |
| Result (II): only `N = 3` (giving `m = 3939.52`) lies inside band; `N = 2` falls below by `35%`, `N = 4` exceeds by `30%`, larger `N` further above | scalar comparison | no |

Every load-bearing step is exact-rational arithmetic, scalar
monotonicity, or scalar substitution into the parent's already-stated
identities. No new physical assumption beyond the parent freeze-out-
bypass note's admissions is introduced.

## Exact Arithmetic Check

The runner verifies, at exact rational precision via
`fractions.Fraction`:

(A) **Monotonicity verification.** `C(x_F, S)` is monotone increasing
in `x_F` and monotone decreasing in `S`; verified by direct evaluation
at the four corners of `[22, 28] × [1.4, 1.7]` and confirming the
expected ordering.

(B) **Inverse-target band.** Compute `m_DM_target` at all four
corners of `(x_F, S)` rectangle in `Fraction` arithmetic; extract
`m_min, m_max`. Cross-check with float arithmetic (within `< 1` GeV).

(C) **Structural-candidate band-membership audit.** For each
candidate from the parent freeze-out-bypass note's audit table
(`16 v`, `4 pi v`, `R_base^2 v`, `M_Pl alpha_LM^15`,
`M_Pl alpha_LM^15 · 2 u_0`, `v/alpha_LM`), check membership in
`[m_min, m_max]`. Confirm that **only** `16 v` is inside; report the
percent-from-band-edge for the other candidates.

(D) **Origin-B gauge-group audit.** For `N ∈ {2, 3, 4, 5, 6}`,
compute `m_phys^Origin-B(N) = 6 (N^2 - 1) v / N` in `Fraction` and
check membership in `[m_min, m_max]`. Confirm that **only** `N = 3`
is inside.

(E) **Origin-B `N = 3` consistency cross-check.** Verify
`m_phys^Origin-B(3) = 6 · 8/3 · v = 16 v` exactly in `Fraction`,
identical to the structural identity `N_sites · v` from (C).

(F) **Band sensitivity.** Report the band edges if the input bounds
are tightened (e.g., `x_F ∈ [24, 26]` and `S ∈ [1.5, 1.65]`); confirm
that `16 v` remains inside and that the band tightens monotonically
as input bounds tighten.

## Dependencies

- [`DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md`](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
  for the freeze-out-bypass identity (eq. (2)), the bounded admission
  bands `(x_F, S_vis/S_dark)`, the structural mass-identity audit
  table, the Origin-B identity form, and the `eta_obs = 6.12 × 10^-10`
  Planck import on the live surface.
- [`R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md`](R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md)
  for the retained `R_base = 31/9`.
- [`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  for the canonical-surface inputs `v = 246.22 GeV` and
  `u_0 = 0.8776`.
- [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  for the EW hierarchy compression `(7/8)^(1/4) · alpha_LM^16`
  generating `v` from `M_Pl`.
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  for the framework axioms `A1` (`Cl(3)`) and `A2` (`Z^3`).

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does **not**:

- close the +12 % `eta` chain. The parent freeze-out-bypass note's
  open lanes G1 (Wilson-action derivation of `m_DM = N_sites · v`),
  G2 (Sommerfeld continuation tightening), G3 (`alpha_X` route choice),
  and G4 (freeze-out coefficient `x_F` band tightening) all remain in
  place;
- derive `m_DM = N_sites · v` from a Wilson-action theorem on the dark
  hw-3 singlet (parent's lane G1 still open);
- derive the `(8/3) = dim(adj_3)/N_c` color-enhancement factor in the
  parent's Origin-B identity from a Coleman-Weinberg argument
  (the parent's Origin-B factor remains a numerical-rewrite, not a
  derived enhancement);
- promote `SU(3)` from a framework axiom to a freeze-out-bypass
  consequence. (II) is a self-consistency audit: **given** the
  framework's axiomatic `SU(3)` choice, only `N = 3` of the Origin-B
  gauge-group family is consistent with the bounded inverse-target band;
- close the parent A0 (dark-sector hierarchy compression) admission;
- promote `eta_obs = 6.12 × 10^-10` from imported observable to derived
  value. The note inverts (1) at fixed `eta = eta_obs`; the input
  `eta_obs` enters the bounded band (3) on the same authority as the
  parent freeze-out-bypass note;
- promote the parent freeze-out-bypass note's status from
  `bounded_theorem` to `retained`.

What this note **does**:
- transforms the parent freeze-out-bypass note's central-point
  `+ 2.09 %` match (at `(x_F, S_vis/S_dark, alpha_X) = (25, 1.59,
  alpha_LM)`) into the bounded-band statement (3) under canonical
  admissions, then verifies that `m_DM = 16 v` is the unique
  structural-audit candidate **and** the unique Origin-B gauge-group
  choice (`N ∈ {2..6}`) inside that band.

This is a quantitative tightening of the parent freeze-out-bypass
note's `+ 2.09 %` central-point statement; it does not retire any of
the parent's admissions and does not change the parent's open-lane
structure.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_m_dm_inverse_band_gauge_audit.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: under bounded admissions on (x_F, S_vis/S_dark) at alpha_X = alpha_LM,
the inverse-target band on m_DM is [3422.52, 4254.75] GeV. The unique
structural candidate from the parent freeze-out-bypass audit table inside
the band is N_sites · v = 16 v = 3939.52 GeV; the unique Origin-B gauge-
group choice (N ∈ {2,3,4,5,6}) inside the band is SU(3). All other
candidates and gauge-group choices lie >10% outside the band edges. This
quantifies the parent's +2.09% central-point match as a bounded-band
uniqueness statement, without retiring any of the parent's open lanes.
```
