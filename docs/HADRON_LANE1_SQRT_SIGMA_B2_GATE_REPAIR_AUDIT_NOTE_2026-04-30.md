# Lane 1 `sqrt(sigma)` B2 Gate Repair Audit

**Date:** 2026-04-30
**Status:** support / open-lane gate-repair audit; no theorem or claim
promotion. This note repairs the next target for Lane 1 route 3E by
showing that the literal "single quenched-to-dynamical screening factor"
is not a retained observable until the full-QCD string-breaking boundary
is handled explicitly.
**Script:** `scripts/frontier_hadron_lane1_sqrt_sigma_b2_gate_repair.py`
**Lane:** 1 - Hadron mass program, route 3E `sqrt(sigma)` retained
promotion.

---

## 0. Statement

The 2026-04-27 gate audit isolates `(B2)` as the dominant residual in
the bounded string-tension readout:

```text
sqrt(sigma)_quenched   ~= 484 MeV
sqrt(sigma)_rough      ~= 465 MeV  (rough x0.96 screening)
comparator             ~= 440 +/- 20 MeV
```

That target is correct as a priority, but its current wording is too
coarse for a retained-with-budget upgrade. In full QCD with dynamical
quarks, the asymptotic static string breaks at the pair-production
threshold. So "the N_f=2+1 string tension" is not the same observable as
the quenched asymptotic string tension. A single multiplicative
screening factor is therefore a bounded phenomenological shorthand, not
a closure object.

**Gate repair.** Replace literal `(B2)` with two sub-gates:

```text
B2a: observable-definition gate
     Define which full-QCD quantity replaces quenched asymptotic sigma:
     pre-breaking effective flux-tube tension, static-force scale
     r0/r1/r2, or a specified static-energy fit window.

B2b: bridge-value gate
     Import or compute that N_f=2+1 quantity with an uncertainty budget,
     quark-mass policy, scale-setting policy, and explicit B5
     framework-to-standard-QCD residual.
```

Until `B2a` and `B2b` are both satisfied, the existing rough x0.96 factor
cannot promote `sqrt(sigma)` from bounded to retained.

## 1. Premise

| Item | Current status | Role |
|---|---|---|
| graph-first `SU(3)` gauge sector | retained/support packet, but audit ledger still marks the confinement-string-tension row conditional | framework-side gauge substrate |
| `g_bare = 1`, `N_c = 3`, `beta = 6.0` | arithmetic on the accepted surface | Wilson action coupling |
| `sqrt(sigma)_quenched ~= 484 MeV` | imported Method 2 lattice bridge | quenched comparator |
| rough x0.96 screening | bounded estimate | current `(B2)` placeholder |
| `sqrt(sigma) ~= 440 +/- 20 MeV` | comparator only | not allowed as a source for screening |
| string breaking in full QCD | external lattice-QCD fact | forces observable-definition gate |

The audit ledger entry for `CONFINEMENT_STRING_TENSION_NOTE.md` remains
binding here: the current packet is a bounded consistency story, not an
audit-retained zero-parameter string-tension theorem.

## 2. Arithmetic replay

Using the existing Method 2 constants:

```text
r0              = 0.472 fm
r0/a            = 5.37
sigma a^2       = 0.0465
hbar c          = 197.327 MeV fm
```

gives:

```text
a                         = 0.0879 fm
sqrt(sigma)_quenched      = 484.11 MeV
rough x0.96 value         = 464.75 MeV
factor needed for 440 MeV = 0.9089
factor band for 440+/-20  = [0.8676, 0.9502]
```

The rough x0.96 value reproduces the existing bounded 465 MeV number,
but it sits above the one-sigma comparator band. That is not by itself a
failure because the comparator is not a derivation input. It is enough
to show why x0.96 cannot be treated as a retained closure constant.

## 3. Why literal B2 is underdefined

In quenched `SU(3)` Yang-Mills, the large-distance static potential has
an asymptotic linear slope, so the string tension is a clean scale. In
full QCD, sea-quark pair creation makes the static string break. The
long-distance ground-state potential flattens into a two-meson channel.
That means a full-QCD "string tension" must specify an observable:

- an effective pre-breaking flux-tube tension over a finite distance
  window;
- a static-force scale such as `r0`, `r1`, or `r2`;
- a static-energy fit window that includes a Cornell-like linear term
  only below or around the string-breaking distance;
- or a direct framework ensemble observable with its own operator basis.

Without this definition, a single "screening factor" mixes unlike
objects: quenched asymptotic `sigma` and a full-QCD finite-window or
force-scale quantity.

## 4. No-go routes closed by this block

### 4.1 Rough x0.96 promotion

The rough factor has no branch-local `N_f=2+1` dynamical ensemble, no
operator-basis handling for string breaking, no uncertainty budget, and
no repaired `(B5)` framework-to-standard-QCD linkage. It remains useful
as an order-of-magnitude bridge, but cannot promote the claim.

### 4.2 PDG backsolve

Solving `f = 440 / 484 ~= 0.909` would tune the screening factor to the
target comparator. That is circular. Observed `sqrt(sigma)` values may
be used only as comparators or for sanity checks, not as the source of
the framework screening correction.

### 4.3 Pure quenched volume scaling

Large-volume pure-gauge Wilson loops can tighten `(B5)` for the
framework-to-standard-YM identification, but they do not close `(B2)`.
`(B2)` is specifically about dynamical sea-quark effects.

### 4.4 Literal asymptotic full-QCD sigma

Because the string breaks in full QCD, the asymptotic full-QCD string
tension is not the right target. The repaired gate must use an effective
pre-breaking or static-force observable.

## 5. Surviving routes

### Route A: external static-energy / static-force bridge

Import a modern `N_f=2+1` or `N_f=2+1+1` static-energy or force-scale
determination, then declare the residual. This is the nearest
single-cycle path to a retained-with-budget statement, but it remains a
bridge, not a zero-import derivation. It must report:

- ensemble family, lattice action, sea-quark masses, and scale setting;
- observable definition (`r0`, `r1`, `r2`, effective `sigma_eff`, or
  fit-window `sigma`);
- quoted uncertainty and chiral/continuum extrapolation;
- mapping from that observable back to the existing Method 2
  `sqrt(sigma)` row;
- `(B5)` residual for applying standard lattice-QCD data to the
  framework gauge substrate.

### Route B: direct framework dynamical ensemble

Run a `N_f=2+1` dynamical-fermion lattice calculation at the framework
`beta = 6.0` point, with an operator basis that can see both the
unbroken string and broken two-meson channels. This is the cleanest
conceptually, but it is a compute project and not a single local cycle.

### Route C: B5 first, then B2

First tighten the framework-to-standard-QCD identification with
large-volume pure-gauge Wilson loops or plaquette scaling. This helps
all imported lattice-QCD bridge work, but it does not by itself provide
dynamical screening.

## 6. Literature bridge snapshot

This block used external literature only to repair the gate definition,
not to land a numerical import.

- A 2025 `N_f=2+1` potential-scale determination reports modern `r0`
  and `r1` static-force scales and explicitly notes that in full QCD the
  string breaks, making a precise string-tension definition difficult:
  <https://link.springer.com/article/10.1140/epjc/s10052-025-14339-y>
- A 2023 `N_f=2+1+1` static-energy analysis determines `r0`, `r1`, and
  a fit-window `sigma` out to distances near 1 fm, and says its
  `r0 sqrt(sigma)` agrees with published `N_f=2+1` results:
  <https://arxiv.org/abs/2206.03156>
- A lattice string-breaking study observed sea-quark-induced string
  breaking in four-dimensional full QCD with `N_f=2` Wilson fermions:
  <https://arxiv.org/abs/hep-lat/0409137>

These references imply that the next B2 bridge should be formulated in
terms of static force/energy or pre-breaking effective flux-tube
observables, not as an unqualified asymptotic full-QCD string tension.

## 7. Claim-state movement

This block does not close `sqrt(sigma)`. It moves the lane by replacing
an underdefined target with an executable repaired gate:

```text
old B2: replace rough x0.96 with proper N_f=2+1 screening factor

new B2: define the full-QCD dynamical observable (B2a), then import or
        compute its value with uncertainty and B5 residual (B2b)
```

Safe current statement:

> Conditional on the framework gauge sector matching standard
> `SU(3)` lattice QCD at `beta = 6.0`, the current bounded
> `sqrt(sigma)` row remains a consistency window. The dynamical
> correction cannot be promoted until the full-QCD observable is
> defined and bridged with a residual budget.

## 8. Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_hadron_lane1_sqrt_sigma_b2_gate_repair.py
```

Expected result:

```text
PASS=16 FAIL=0
```

## 9. Next exact action

Run the external static-energy bridge scout as the next block:

1. collect `N_f=2+1` and `N_f=2+1+1` values for `r0`, `r1`,
   `r0 sqrt(sigma)`, and any quoted effective `sigma`;
2. reject entries that use only asymptotic quenched string tension or
   circular phenomenological matching;
3. produce a residual table separating scale-setting, chiral/continuum,
   string-breaking/window-definition, and `(B5)` framework-link
   uncertainty.

If that table is clean, a retained-with-explicit-budget interim
statement may become plausible. If not, B2 remains a compute-lane target.
