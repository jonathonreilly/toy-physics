# Multi-Time Support Constraint Note

**Date:** 2026-04-25
**Status:** chronology-protection companion note; support-import classifier
**Probe:** `scripts/multi_time_support_constraint_probe.py`
**Companions:**
[ANOMALY_FORCES_TIME_THEOREM.md](ANOMALY_FORCES_TIME_THEOREM.md),
[CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md](CHRONOLOGY_IMPORT_CLASSIFICATION_NOTE.md)

## Role

This note makes the multi-time row of the chronology import classifier
concrete.

The retained framework has one Hamiltonian clock and arbitrary admissible local
data on one codimension-1 slice. Multi-time or ultrahyperbolic systems can be
mathematically meaningful, but they generally replace that retained local
Cauchy surface with a constrained support surface. The chronology-lane
classification is therefore:

```text
multi-time construction -> constrained nonlocal support surface
```

This is not a proof that every multi-time theory is inconsistent. It is a
boundary statement: such theories do not preserve the same graph-local
codimension-1 data semantics unless they supply an equivalent local Cauchy
surface without the imported support filter.

## Toy Model

Use one selected clock `t1`, one extra time coordinate `t2`, and one spatial
coordinate `x`:

```text
d_t1^2 phi + d_t2^2 phi - d_x^2 phi = 0.
```

Fourier transform only along the chosen `t1 = 0` slice coordinates `(t2, x)`.
For a mode `(omega2, k)`, the `t1` amplitude obeys

```text
a''(t1) + (k^2 - omega2^2) a(t1) = 0.
```

The simple admissibility constraint used by the probe is

```text
k^2 >= omega2^2.
```

Modes satisfying this are oscillatory in the selected clock. Modes with
`omega2^2 > k^2` are the forbidden ultrahyperbolic region in this toy support
classifier.

## Support Import

A delta-local field perturbation on the slice has nonzero Fourier coefficient
on every mode. The same is true for a delta-local normal-velocity perturbation.
Therefore arbitrary local slice data generally activate forbidden modes.

To make those data admissible under the multi-time support rule, one must apply
a projection:

```text
P_allowed: coefficient(omega2,k) -> 0 when omega2^2 > k^2.
```

That projection is nonlocal in slice variables. It is not a pointwise local
graph update; it is a global Fourier-space filter over the full slice.

## Probe Result

Run:

```bash
python3 -m py_compile scripts/multi_time_support_constraint_probe.py
python3 scripts/multi_time_support_constraint_probe.py
```

The finite lattice sample uses modes `omega2,k in [-4,4]`:

| quantity | value |
|---|---:|
| total modes | 81 |
| allowed modes, `k^2 >= omega2^2` | 49 |
| forbidden modes, `omega2^2 > k^2` | 32 |
| forbidden share | `32/81` |
| arbitrary field-plus-velocity Cauchy slots | 162 |
| constrained field-plus-velocity Cauchy slots | 98 |

The delta-local field datum and the delta-local velocity datum each activate
all 32 forbidden modes. The support projection removes exactly those forbidden
field modes.

The probe also includes an exact `Z2 x Z2` projection witness. Removing the
single forbidden mode `(omega2=1,k=0)` sends a point datum to

```text
(t2=0, x=0) ->  3/4
(t2=0, x=1) -> -1/4
(t2=1, x=0) ->  1/4
(t2=1, x=1) ->  1/4
```

So even the smallest exact support filter spreads a point perturbation across
the slice. The nonlocality is not numerical roundoff; it is the inverse
Fourier image of deleting a forbidden character.

## Chronology Classification

On the retained chronology surface, the graph supplies arbitrary local data on
one clock slice and evolves them by the single clock. A multi-time construction
that enforces a support condition like `k^2 >= omega2^2` instead admits only a
proper constrained subset of those data.

Thus apparent late-to-early or cross-time dependence in such a construction is
not classified as operational past signaling. It is classified as imported
global support structure:

```text
retained single-clock arbitrary local Cauchy surface: no
constrained multi-time support surface: yes
imported structure: nonlocal Fourier support projection/filter
```

The chronology lane should use this as a boundary classifier, not as a blanket
inconsistency theorem.

## Non-Claims

- This note does not disprove all multi-time or ultrahyperbolic theories.
- It does not claim the toy equation exhausts all possible multi-time
  formalisms.
- It does not use instability alone as the theorem. The load-bearing point is
  the loss of arbitrary graph-local codimension-1 data.
- A theory that starts from a constrained support surface may be studied as a
  different theory. It is not the retained `Cl(3)/Z^3` single-clock local-data
  surface.

## Retained Language

Use:

- "nonlocal Fourier support constraint"
- "constrained multi-time support surface"
- "outside arbitrary graph-local codimension-1 data"
- "support-filter import"

Avoid:

- "all multi-time theories are impossible"
- "extra time dimensions by themselves cause time travel"
- "forbidden modes prove backward signaling"
- "the support projection is a local graph operation"
