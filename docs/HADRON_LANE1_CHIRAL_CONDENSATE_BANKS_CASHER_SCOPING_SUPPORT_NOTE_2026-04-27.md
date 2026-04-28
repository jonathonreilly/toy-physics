# Lane 1 Chiral Condensate `Sigma` via Banks-Casher: Scoping Audit

**Date:** 2026-04-27
**Status:** support / open-lane scoping no-go on `main`; no theorem or
claim promotion. Audits the Lane-1-internal route to chiral condensate
`Sigma` retention via the Banks-Casher relation
`Sigma = pi * rho_Dirac(0)` on the framework's staggered-Dirac
partition. Verdict: **no clean structural retention route exists on
current framework content**; closing this would require either a
large-volume (`L >= 12-16`) dynamical lattice calculation or a new
structural identity connecting framework content to the chiral-limit
small-eigenvalue density.
**Lane:** 1 — Hadron mass program (route 3A entry; R7 in workstream
portfolio)
**Source workstream:** `hadron-mass-program-20260427`

---

## 0. Statement

Banks-Casher (1980): on a Euclidean lattice with massless fermions in
infinite volume,

```text
Sigma  =  pi * rho_Dirac(0)                                          (BC)
```

where `rho_Dirac(0)` is the spectral density of the Dirac operator
evaluated at zero, in the chiral-limit (`m_q -> 0`), thermodynamic-
limit (`V -> infinity`) order. Retaining `Sigma` from `(BC)` requires
retaining `rho_Dirac(0)` on the framework's staggered-Dirac partition
in the appropriate limits.

**Audit verdict.** The framework's currently retained content does
not deliver `rho_Dirac(0)` in the appropriate limits:

- (V1) **Volume too small.** Existing framework lattice data
  (`G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`) only
  scans `L = 4, 6`. At these volumes, the `rho(0)` observable shows
  `0.0260 at L = 4, beta = 6` and migrates to `0.0000 at L = 6, beta = 6`
  — a classical finite-volume lattice-free regime. Standard chiral-SB
  signal extraction requires `L >= 12-16`, off-budget for the
  existing framework runs.
- (V2) **No structural derivation of the small-eigenvalue density.**
  `rho_Dirac(0)` is non-universal: chiral random-matrix theory (chRMT)
  gives the universal *shape* of the small-eigenvalue distribution
  but the overall scale `Sigma` is non-universal. The framework's
  existing notes (CHIRAL_*, G_BARE_*) do not contain a structural
  identity that pins `Sigma` from `Cl(3)` algebraic content alone.

So R7's question — "can the staggered-Dirac partition on `Cl(3)/Z^3`
deliver retained `Sigma`?" — answers **not currently**. Two paths
remain open as future work:

- (P1) large-volume dynamical lattice run (compute resources, off
  this workstream's scope);
- (P2) a new structural identity (analog of the YT lane's
  `y_t / g_s = 1/sqrt(6)` Ward identity) connecting framework content
  to `rho_Dirac(0)`.

This audit produces the negative result and identifies what an honest
R7 closure would require, mirroring the (C3)-class audit-no-go from
the hubble-h0 workstream.

## 1. Premise (retained surface used)

| Identity | Authority |
|---|---|
| Finite local Grassmann / staggered-Dirac partition on `Cl(3)/Z^3` | `MINIMAL_AXIOMS_2026-04-11.md` (substrate) |
| `g_bare = 1`, `N_c = 3`, `beta = 6.0` (Wilson plaquette action) | `CONFINEMENT_STRING_TENSION_NOTE.md` §3 |
| Lattice scan of `<P>`, `\|<L>\|`, `ln\|det D\|/V`, `\|lambda_min\|`, spectral gap, `rho(0)` at `L = 4, 6`, `beta in [1, 30]` | `G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md` |
| Banks-Casher relation `Sigma = pi * rho_Dirac(0)` (textbook) | admitted convention (Banks-Casher 1980) |
| Chiral random-matrix theory universality of small-eigenvalue distribution | admitted convention (Verbaarschot 1994; Shuryak-Verbaarschot 1993) |

## 2. The Banks-Casher route

Banks-Casher gives, for `m_q -> 0` and `V -> infinity`:

```text
Sigma  =  pi * rho_Dirac(0)
```

with `rho_Dirac(lambda)` the eigenvalue density of the massless Dirac
operator (or, equivalently for staggered fermions, the eigenvalue
density of the staggered operator near zero, with the staggered →
continuum normalization).

To retain `Sigma`, we need `rho_Dirac(0)` retained as a numerical
quantity on the framework's substrate.

## 3. Available framework data

The g_bare obstruction note (2026-04-18) ran a uniform `beta` scan on
the framework's substrate (Cl(3)/Z^3 + Wilson SU(3) + staggered
Kogut-Susskind fermion at zero bare mass) at `L in {4, 6}`,
`L_t = L`, `beta in [1, 30]`. Among the six observables scanned was
the low-mode density:

```text
rho(0; beta)  :=  fraction of D_stag eigenmodes with |lambda| < 0.2.
```

At the framework's evaluation point `beta = 6`:

| `L` | `rho(0; beta = 6)` |
|---|---|
| 4 | 0.0260 |
| 6 | 0.0000 |

And in the broader scan the observable migrates with `L` and `beta`:

- at `L = 4, beta = 5`: `0.0469` (small-eigenvalue dominated, strong-
  coupling end of scan);
- at `L = 4, beta = 6`: `0.0260` (transitional);
- at `L = 4, beta = 7`: `0.0000` (lattice-free regime, no near-zero
  modes);
- at `L = 6, beta = 6`: `0.0000` (already in lattice-free regime at
  larger volume).

The g_bare obstruction note characterizes this as:

> The low-mode density has a crossover near `beta ~ 6-7` where
> near-zero modes disappear in small volumes (lattice-free regime).
> The location MIGRATES `beta = 6 -> beta = 7` going `L = 4 -> L = 6`,
> and the window gets narrower with volume — classical finite-volume
> effect sensitive to the smallest physical Dirac eigenvalue bound,
> not a framework-invariant point.

## 4. Why the existing data does not deliver `Sigma`

### 4.1 (V1) volume / chiral-limit ordering

Banks-Casher requires the orders:

```text
m_q -> 0  *first*,  then  V -> infinity.
```

At finite `V`, the chiral-limit Dirac spectrum has a non-trivial
small-eigenvalue gap that closes as `V -> infinity`. The framework's
`L = 4, 6` data is in the **lattice-free regime** where this gap is
not yet closed: the smallest eigenvalues are above the "Banks-Casher
bandwidth", and `rho(0)` is the wrong observable.

The standard chRMT diagnostic threshold is roughly:

```text
L >= 12-16  *and*  m_q a << 1
```

with `m_q a` controlled separately. The framework's existing data
satisfies neither.

### 4.2 (V2) non-universal scale `Sigma`

Even if a large-volume scan were performed, the resulting numerical
`Sigma` would be a quantity *measured* on the framework's substrate,
not a quantity *derived* from framework structural content. To retain
`Sigma` (rather than measure it), one of:

- a **structural identity** connecting `rho_Dirac(0)` (or `Sigma`) to
  retained framework quantities (analog of YT/top
  `y_t / g_s = 1/sqrt(6)` Ward identity), OR
- a **hard combinatorial / algebraic identity** on the staggered
  partition that fixes `rho_Dirac(0)` from the `Cl(3)/Z^3` action
  parameters

would be needed. Neither is present in the framework's currently
retained content.

### 4.3 chRMT does not help

Chiral random-matrix theory provides the **universal shape** of the
small-eigenvalue distribution `rho_Dirac(lambda)` near zero — the
"microscopic spectral density" — in the chiral limit at finite
volume. The shape is universal across all `Cl(3)/Z^3`-like SU(3)
theories and depends on Dyson index `beta_chRMT in {1, 2, 4}`, the
condensate `Sigma`, and the volume. But **`Sigma` itself sets the
scale and is non-universal.** chRMT cannot deliver retained `Sigma`.

## 5. What an honest R7 closure would require

### 5.1 (P1) large-volume dynamical lattice path

A `N_f = 2+1` dynamical-fermion lattice calculation at `beta = 6.0`,
volume `L >= 16`, with controlled chiral-limit extrapolation would
deliver `Sigma` numerically with sub-percent precision (standard
lattice-QCD result). This would be a **measured** `Sigma` on the
framework substrate, not retained from framework structure alone.

For YT-lane-style retained-with-budget statement, this is acceptable
provided the measurement is paired with the structural claim
"the framework's gauge sector + staggered-Dirac partition matches
standard SU(3) lattice QCD" (the same `(B5)` identification used in
the `sqrt(sigma)` retention gate audit, Cycle 2).

### 5.2 (P2) structural identity path

A structural identity that pins `rho_Dirac(0)` from the `Cl(3)/Z^3`
action parameters alone (without lattice numerics) would be the
preferred retention pathway. Candidate templates:

- **Anomaly-matching:** chiral anomaly + Ward identities. The retained
  graph-first SU(3) integration plus the recent SM gauge-cluster
  retentions (anomaly cancellations) constrain Ward identities, but
  do not pin `Sigma`.
- **Index theorem on `Z^3`:** `rho_Dirac(0)` is sensitive to the
  index `n_+ - n_-` of the Dirac operator. A retained index-theorem
  identity on the framework substrate could pin the contribution of
  zero modes to `rho(0)` but not the bulk small-eigenvalue density.
- **Explicit chRMT-style structural identity:** if the framework's
  Dirac operator is shown to fall in a specific chRMT universality
  class with fixed scale (rather than measured scale), `Sigma`
  would be pinned. No such identity is known.

None of these is currently retained or actively developed. Opening
(P2) requires a structurally new framework feature (analog to opening
a (C3)-class route in the hubble-h0 workstream).

## 6. Audit no-go statement

**No-Go (Lane 1 R7 chiral condensate `Sigma` audit, current framework
content).** On the framework's currently retained content, the
chiral condensate `Sigma` is not retainable via Banks-Casher because:

- (V1) the existing lattice data is in the finite-volume lattice-free
  regime, not the Banks-Casher chiral-thermodynamic regime;
- (V2) the framework lacks a structural identity that pins
  `rho_Dirac(0)` (or equivalently `Sigma`) from `Cl(3)/Z^3` action
  parameters alone.

Closing R7 requires opening one of:

- (P1) large-volume dynamical lattice run (off-workstream-budget);
- (P2) a new structural identity (currently no active route).

This mirrors the hubble-h0 (C3)-class audit-no-go: a class-bounding
negative on the currently retained framework surface, with explicit
hypothetical opening paths named.

## 7. Implications for the workstream

R7 is **not a productive single-cycle target** for this workstream
under the current framework content. The corresponding Lane-1 entry
target 3A (`m_pi` via GMOR) therefore depends on:

- Lane 3 closure of `m_u + m_d` (essential), AND
- Either a Lane-1-internal `f_pi` retention (separable from `Sigma`)
  *and* a Lane-1-internal `Sigma` retention via (P1) or (P2),
- Or, more likely in the near term: a measured `Sigma` from a
  large-volume lattice run paired with the YT-lane-style
  retained-with-budget identification.

The cleanest single-cycle Lane-1-internal work remains the
`sqrt(sigma)` retention gate audit (Cycle 2) and any subsequent
work on the `(B2)` quenched → dynamical screening calculation that
Cycle 2 identifies as load-bearing.

## 8. Cross-references

- `docs/HADRON_MASS_LANE1_THEOREM_PLAN_SUPPORT_NOTE_2026-04-27.md`
  — Lane 1 closure roadmap; §4.2 frames R7 as Tier B-C "depending on
  whether a clean structural path exists".
- `docs/HADRON_LANE1_SQRT_SIGMA_RETENTION_GATE_AUDIT_SUPPORT_NOTE_2026-04-27.md`
  (Cycle 2) — `sqrt(sigma)` gate audit, structurally similar
  retention-budget pattern.
- `docs/G_BARE_DYNAMICAL_FIXATION_OBSTRUCTION_NOTE_2026-04-18.md`
  — primary source for the framework's `L = 4, 6` lattice scan of
  `rho(0)` and other small-eigenvalue observables.
- `docs/CONFINEMENT_STRING_TENSION_NOTE.md` — retained `T = 0`
  confinement; bounded `sqrt(sigma)`; gauge sector identification.
- `docs/MINIMAL_AXIOMS_2026-04-11.md` — minimal accepted axiom
  stack (substrate for the staggered-Dirac partition).
- `docs/lanes/open_science/01_HADRON_MASS_PROGRAM_OPEN_LANE_2026-04-26.md`
  §3.1 — lane file framing of 3A `m_pi` via GMOR.

## 9. Boundary

This is an audit / scoping no-go, not a theorem and not a runner-
bearing cycle. It does not retire any input. It does not promote
`Sigma` from absent to retained. It identifies the gate that an
honest R7 closure must pass and the two hypothetical paths
(`(P1)` large-volume lattice run; `(P2)` structural identity)
that could open it.

A runner is not authored: the audit is structural review of
existing framework content; no new symbolic or numerical content
is introduced.
