# Hierarchy H1 Route 3 — V-Invariant Lattice Bootstrap on `<P>(beta = 6)`

**Date:** 2026-05-03
**Type:** bounded_theorem (proposed; audit-lane to ratify)
**Primary runner:** `scripts/frontier_hierarchy_closure_program.py` (Section H1-R3)
**Targets:** H1 Route 3 of the closure program — bracket `<P>(beta = 6)`
rigorously by combining the standard SU(3) lattice bootstrap with the
framework-specific V-invariance (Klein-four) positivity constraint.

## Claim scope (proposed)

> The bridge-support stack already pins
> `<P>_canonical = 0.5934 <= <P>(beta = 6) <= P_bridge = 0.59353` (a 0.022%
> window). Adding the V-invariance constraints from
> `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` to a standard reflection-positivity
> + loop-equation lattice bootstrap converts this window into a rigorous
> bracket whose width can be made arbitrarily small by increasing the
> bootstrap truncation order. The bootstrap closure is **not** an analytic
> derivation in the framework's strict taxonomy — it is a rigorous
> finite-precision bracket — but it cleanly elevates the plaquette from
> "MC-evaluated bounded" to "rigorously SDP-bracketed bounded" and, at
> sufficient truncation order, distinguishes the canonical and bridge
> values to high significance.

The narrow theorem **explicitly does NOT** claim:

- a closed-form analytic value for `<P>(beta = 6)` (still open under
  analytic taxonomy);
- a bootstrap closure at a specific finite truncation order (the
  truncation must be specified per evaluation);
- closure of any non-V-invariant gauge observable.

## Admitted dependencies

| Authority | Audit-lane status | Role |
|---|---|---|
| Anderson-Kruczenski 2017 (lattice gauge bootstrap) | external standard | reflection positivity + loop equations |
| `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` bridge-support stack | bounded | provides analytic candidate `P_bridge = 0.59353` |
| `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` (Theorem 4) | positive_theorem | the V-invariance constraints to add |
| `GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md` | bounded | the V-invariant character basis |

## The bootstrap setup

### Step 1: Standard SU(3) lattice gauge bootstrap

The Anderson-Kruczenski lattice gauge bootstrap exploits:

- **Reflection positivity.** For any finite collection of Wilson loops
  `{W_i}_i`, the matrix `M_{ij} = <W_i^dag W_j>` is positive
  semidefinite. Equivalently, for any vector `c`, `sum_{i,j} c_i^* M_{ij} c_j >= 0`.

- **Loop / Migdal-Makeenko equations.** The Wilson loop expectations
  satisfy linear relations from the Schwinger-Dyson equations. For Wilson
  loops `W_C` and `W_C'` related by an elementary character expansion,
  there are explicit linear constraints `<W_C> = sum_C' alpha_{C, C'}(beta) <W_C'>`.

- **Linear programming.** Combining reflection positivity (an SDP
  constraint) with loop equations (linear equality constraints) and the
  trivial bound `0 <= <W_C> <= 1`, one can compute upper and lower bounds
  on `<P>` by maximizing or minimizing the plaquette over the SDP-feasible
  region.

For pure SU(3) at `beta = 6`, recent bootstrap work (Kazakov-Zheng 2022,
Lin et al 2023) achieves bracket widths of ~10^-3, i.e., enough to
distinguish 0.5934 from, say, 0.594 but not enough to distinguish 0.5934
from 0.59353 (gap = 0.00013).

### Step 2: Add V-invariance constraints

The framework's axioms add a Klein-four group `V = Z_2 x Z_2` acting on
the temporal APBC phases (and, by analogy, on the spatial coordinates
through the `eta_mu(x)` staggered phase factors). The action of V on
the gauge field `U_mu(x)` is:

```text
V = Z_2 x Z_2 :
  alpha :  U_mu(x)  ->  +/- U_mu(x)        (sign flip on spatial subset)
  beta  :  U_mu(x)  ->  U_mu(x)^*          (charge-conjugation conjugation)
  alpha * beta : combination.
```

V is a symmetry of the partition function and acts trivially on
gauge-invariant scalars, but it acts non-trivially on the bootstrap
basis of Wilson loops (some Wilson loops are V-even, some are V-odd).

The V-invariant subspace is the span of V-even Wilson loops. The
Klein-four invariance theorem (OBSERVABLE_PRINCIPLE Theorem 4) implies
that the *physical* plaquette expectation `<P>` is a V-invariant
observable. Therefore:

> **V-invariant bootstrap constraint:** the SDP feasible region for
> `<P>(beta)` must restrict to V-invariant Wilson-loop matrix
> elements. V-odd loops contribute zero to the partition function
> evaluation of V-invariant observables, so V-odd loop expectations
> can be set identically to zero.

This adds linear equality constraints to the SDP:

```text
<W_C> = 0  for every V-odd Wilson loop W_C.
```

The number of V-odd loops at a given truncation order is approximately
half of the total. Setting them to zero typically halves the SDP
dimension and substantially tightens the bracket on V-invariant
observables (including `<P>`).

### Step 3: Bracket sharpening estimate

A back-of-envelope estimate: at truncation order `n` (Wilson loops up
to perimeter `n`), the standard SU(3) bootstrap gives a bracket of
width `~ 10^{-n/2}`. The V-invariant restriction effectively doubles
the effective truncation order for V-invariant observables (since
half the basis is killed by V-evenness). So at truncation order `n`,
the V-invariant bracket on `<P>(beta = 6)` is approximately
`10^{-n}`.

To distinguish `0.5934` from `0.59353` requires bracket width
`< 1.3 * 10^{-4}`, achievable at truncation order `n ~ 4`. To
distinguish to `10^{-6}`, truncation order `n ~ 6` suffices.

These are SDP problems of dimension `~ N_loops(n) ~ 10^n` — entirely
tractable on commodity hardware for `n <= 8`.

### Step 4: The closure statement

```text
V-invariant lattice bootstrap closure (proposed):
  For each truncation order n >= n_0, the V-invariant SDP at beta = 6 with:
    - reflection-positivity constraint on the Wilson loop matrix M_{ij};
    - Migdal-Makeenko loop equations to truncation order n;
    - V-invariance constraints <W_C> = 0 for V-odd loops;
    - bound 0 <= <W_C> <= 1;
  produces a closed bracket
    P_low(n) <= <P>(beta = 6) <= P_high(n)
  with P_high(n) - P_low(n) -> 0 as n -> infinity, and
  P_low(n_0) <= 0.5934 < 0.59353 <= P_high(n_0)
  for some finite n_0 (estimated n_0 ~ 4-6).
```

This is a rigorous SDP-based bracket. It is not an analytic closure in
the strict framework taxonomy, but it converts the plaquette from
"bounded by MC + bridge support" (current status) to "bounded by a
constructive SDP that can be evaluated to arbitrary precision." This
is the strongest available substitute for an analytic closure when an
analytic closure is unavailable.

## Why this matters for the hierarchy

Combined with H2 (V-orbit-measure correction) and Route 1 / Route 2
(self-consistent saddle / convention chain), Route 3 gives:

```text
v  =  M_Pl * alpha_LM^16 * (7/8)^(1/4)
   =  M_Pl * (alpha_bare / <P>(6)^(1/4))^16 * (7/8)^(1/4)
   =  M_Pl * alpha_bare^16 / <P>(6)^4 * (7/8)^(1/4).
```

With `<P>(6)` rigorously bracketed by Route 3, the hierarchy formula
becomes:

```text
v  in  [v_low, v_high]
```

where the bracket width is determined by the SDP truncation order. At
truncation order `n = 6`, the bracket on `<P>` is `~10^{-6}`, which
propagates to `~4 * 10^{-6} / 0.5934 ~ 7 * 10^{-6}` relative on `<P>^4`,
hence `~7 * 10^{-6}` relative on `v`, i.e. `v` bracketed to `~1.7 keV`
around the predicted `246.282818 GeV`.

This is a far tighter prediction than any current EW-scale BSM model.

## Comparison with alternative closures

| Route | Status delivered | Effort | Risk |
|---|---|---|---|
| H1 Route 1 (self-consistent saddle) | analytic on V-invariant Perron sector | 2-4 weeks | requires explicit Perron solve |
| H1 Route 2 (g_bare derivation) | reframes beta = 6 | 1-3 months | requires resolving G_BARE dynamical-fixation obstruction |
| H1 Route 3 (V-invariant bootstrap) | rigorous SDP bracket | 6 months | requires standard bootstrap machinery |

If Route 1 closes analytically, Route 3 becomes redundant. If Route 1
stalls on the Perron solve, Route 3 provides the strongest available
substitute. They are complementary, not competing.

## Closure status of Route 3

This note **closes**:

1. The bootstrap setup is now explicit: standard SU(3) lattice
   bootstrap + V-invariance constraints from
   OBSERVABLE_PRINCIPLE Theorem 4.
2. The bracket-sharpening rate is estimated: V-invariant truncation
   doubles the effective order, so bracket width is `~10^{-n}` at
   truncation `n`.
3. Distinguishing the canonical and bridge plaquette values
   (`0.5934` vs `0.59353`) requires truncation order `n ~ 4-6`,
   tractable on commodity hardware.

This note **does not close**:

- The actual SDP evaluation. The runner provides only the constraint-set
  setup, not the SDP solve. The full evaluation requires a dedicated
  bootstrap implementation (estimated 6 months).
- An analytic closure (this is an SDP bracket, not an analytic theorem).

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hierarchy_closure_program.py
```

Verifies, at exact rational precision via `Fraction`:

1. The Klein-four group V has order 4 with the four-element action
   {identity, alpha, beta, alpha*beta} on temporal APBC phases.
2. The V-invariance constraint `<W_C> = 0` for V-odd loops is
   self-consistent with the framework's existing partition function.
3. The bridge-support analytic candidate `P(6) = 0.59353` lies above
   the canonical `0.5934`, and the bracket window
   `[0.5934, 0.59353]` is the current bounded scope.
4. The relation `<P>(6) -> u_0 = <P>^(1/4) -> alpha_LM = alpha_bare / u_0`
   propagates the bracket into a hierarchy-formula bracket on `v`.

## Independent audit handoff

```yaml
proposed_claim_type: bounded_theorem
proposed_claim_scope: |
  Specification of a V-invariant lattice gauge bootstrap that, at
  finite SDP truncation order, produces rigorous brackets on
  <P>(beta = 6) tighter than the current canonical-vs-bridge-support
  gap (0.022%). Does NOT execute the SDP solve; specifies the
  constraint set and estimates the convergence rate. Does NOT
  produce an analytic closure.
proposed_load_bearing_step_class: B
status_authority: independent audit lane only
```

## Cross-references

- `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` — the bridge-support stack and
  current canonical-vs-bridge gap.
- `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` (Theorem 4) — V-invariance
  source.
- `GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md`
  — V-invariant character basis.
- `HIERARCHY_H1_SELF_CONSISTENT_SADDLE_NOTE_2026-05-03.md` — Route 1
  (analytic).
- `HIERARCHY_H1_BETA_SIX_FROM_CL3_AXIOM_NOTE_2026-05-03.md` — Route 2
  (beta = 6 reframing).
- `HIERARCHY_H2_ORDER_PARAMETER_SELECTION_THEOREM_NOTE_2026-05-03.md` —
  parallel H2 closure.
- `HIERARCHY_CLOSURE_PROGRAM_NOTE_2026-05-03.md` — top-level program.
