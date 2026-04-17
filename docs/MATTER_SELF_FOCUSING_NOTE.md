# Matter Self-Focusing Attempt — Partial Improvement, Not Closure

**Date:** 2026-04-07
**Status:** retained negative (partial) — two-pass self-focusing propagator reduces equivalence-principle rel dev from 123% (matter_inertial_closure) to **44.05%** at best λ=1, but does not restore equivalence. Family portability collapses (R² drops to 0.09–0.18). Not a matter closure.

## Artifact chain

- [`scripts/matter_self_focusing.py`](../scripts/matter_self_focusing.py)
- [`logs/2026-04-07-matter-self-focusing.txt`](../logs/2026-04-07-matter-self-focusing.txt)

## Question

The previous matter closure attempt
([`MATTER_INERTIAL_CLOSURE_NOTE.md`](MATTER_INERTIAL_CLOSURE_NOTE.md))
failed the equivalence principle at 123% because narrow Gaussian
packets spread 4.68× during propagation and coupled to a larger
portion of the linear field gradient. The hypothesis: **a nonlinear
self-focusing mechanism that stabilizes packet width should restore
equivalence**.

Mechanism: a **two-pass propagator** with amplitude-density self-field.

- Pass 1: propagate the packet freely, record `|amp[i]|²` at each node
- Pass 2: propagate with modified action
  `S = L * (1 - f_external - λ * (density[i] + density[j]) / 2)`

Physical interpretation: the packet's own amplitude density acts as
an attractive field (Schrödinger-Newton / Gross-Pitaevskii-style
self-gravity). Where the packet is densest, the effective phase is
smallest, so paths through high-density regions interfere more
constructively, focusing the packet toward its own centroid.

## Result

### Persistence vs λ

| λ | narrow ratio | medium ratio | wide ratio |
| ---: | ---: | ---: | ---: |
| 0 (reference) | 4.68 | 1.63 | 1.08 |
| 1 | 5.14 | 1.89 | 1.20 |
| 10 | 4.20 | 2.23 | 1.10 |
| 100 | 4.20 | 1.93 | 1.68 |
| 500 | 3.72 | 1.36 | 1.43 |

Self-focusing does **not** stabilize the narrow packet at its initial
width. At best (λ=500) the narrow packet still spreads 3.72×. The
medium and wide packets get worse persistence at intermediate λ.

### Equivalence principle (slopes across packets)

| λ | narrow slope | medium slope | wide slope | rel dev |
| ---: | ---: | ---: | ---: | ---: |
| 0 | −73.45 | −7.05 | −18.28 | **123.07%** |
| 1 | −52.95 | −47.41 | −23.01 | **44.05%** |
| 10 | +41.29 | −3.32 | −27.35 | 1066.98% |
| 100 | −113.40 | −19.90 | +40.54 | 266.74% |
| 500 | +94.23 | −31.47 | +87.04 | 163.04% |

**Best equivalence: λ = 1 at 44.05%.** This is a **partial
improvement** over the λ = 0 reference (123.07%), but still far above
the 10% pass threshold. Stronger self-focusing (λ ∈ {10, 100, 500})
breaks the sign consistency and blows up rel dev.

### Null at best λ

At λ = 1, the null test (g = 0 → delta_z = 0) is exact for all three
packets.

### Family portability at best λ

| Family | slope | R² |
| --- | ---: | ---: |
| Fam1 | −47.41 | **0.0886** |
| Fam2 | +19.30 | 0.1368 |
| Fam3 | −63.47 | 0.1847 |

Family rel dev: **163.22%**. R² collapses to 0.09–0.18, meaning the
relationship between g and delta_z is no longer linear at λ = 1 —
the self-focusing term has introduced enough nonlinearity to break
the Newton regime altogether.

## Honest read

Self-focusing **partially** restores equivalence on Fam1 (rel dev
123% → 44%) but at the cost of destroying family portability and
breaking Newton linearity (R² drops from 0.96+ to 0.09). The trade
is a net loss: one criterion improves, three others degrade.

The mechanism is directionally correct (reducing the mismatch between
narrow and medium/wide packets) but the nonlinearity breaks other
properties. A non-iterative two-pass approximation is not enough;
a fully self-consistent soliton treatment would be needed to know
whether this path can work — and that is a structural change, not
a tweak.

## What this closes for the matter-closure line of attack

After two attempts (matter_inertial_closure + this lane), the
closure of the "fields but no matter" critique via **Gaussian-packet
+ simple force** routes is clearly negative. Both attempts fail
either equivalence (attempt #1), or family portability / linearity
(attempt #2). Further Gaussian-packet variants are not informative.

The next attack target on this critique must be **structurally
different**: soliton-like objects whose width is stabilized by a
self-consistent nonlinearity (iterated, not one-pass), topological
defects, or a modified action with an explicit mass term. All are
bigger lifts than the current harness supports.

## Frontier map adjustment

| Row | Update 3 (classifier closed) | Previous matter attempt | This lane |
| --- | --- | --- | --- |
| Matter / inertial closure via Gaussian packets | open, highest priority | **NEGATIVE** (equivalence 123%) | **still NEGATIVE** (best 44% via self-focus, but kills family portability + linearity) |
| The "fields but no matter" critique | stands | stands | **still stands** after two attempts |
| Non-Gaussian matter closure routes | not attempted | not attempted | **the remaining path**: soliton / topological defect / mass term in action |

## Bottom line

> "A two-pass self-focusing propagator with nonlinear self-field term
> `λ * density` reduces the equivalence-principle rel dev for
> Gaussian persistent packets from 123% to 44% at the best λ = 1,
> but at the cost of breaking family portability (rel dev 163%) and
> Newton linearity (R² drops from 0.96+ to 0.09). Self-focusing is
> directionally correct but a one-pass approximation is insufficient.
> Both Gaussian-packet matter-closure attempts on the grown-DAG
> propagator fail. The 'fields but no matter' critique stands; the
> remaining paths all require structural changes (iterated soliton,
> topological defect, or explicit mass term in the action), not
> further tuning."
