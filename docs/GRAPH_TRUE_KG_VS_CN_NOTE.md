# Graph True KG vs CN Note

Files:
- [frontier_graph_true_kg_vs_cn.py](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_graph_true_kg_vs_cn.py)

## Scope

This harness compares two scalar graph theories on the same graphs:

1. `CN` scalar lane
   `i dpsi/dt = (L + m^2 I + V) psi`
   evolved with Crank-Nicolson.

2. `True local KG` lane
   `dphi/dt = pi`
   `dpi/dt = -(L + m^2 I + V) phi`
   evolved with local leapfrog on the doubled state `(phi, pi)`.

The question is whether the current CN scalar lane is a faithful stand-in
for a true local graph KG theory in the tested regime.

## Graphs

- Cubic periodic lattice: `15^3 = 3375` nodes
- Random geometric graph: `140` nodes

The random-graph KG lane uses an exact dense positive-frequency initializer
for the doubled state, so the non-cubic comparison is not relying on a
crude `pi0 = -i m phi0` approximation.

## Measured Results

### 1. Free modal law

### Cubic

- `CN`: `R^2 = 0.963374`, axis slope `0.7055`, intercept `-0.0263`, isotropy `1.1728`
- `True KG`: `R^2 = 0.999809`, axis slope `0.9520`, intercept `0.0932`, isotropy `1.0309`
- KG target: `omega^2 = m^2 + lambda`, with `m^2 = 0.0900`

### Random graph

- `CN`: `R^2 = 0.955707`, slope `2.3094`, intercept `-0.6494`
- `True KG`: `R^2 = 1.000000`, slope `1.0000`, intercept `0.0900`

### Reading

This is the decisive result. The free modal laws are not the same theory.
The CN lane follows a first-order scalar Hamiltonian with mode frequencies
set by `m^2 + lambda`, while the true KG lane follows `omega = sqrt(m^2 + lambda)`.
The disagreement is not a small fit artifact; it is structural.

## 2. Cubic operating-point dynamics

- Gravity sign:
  - `CN`: `+1.2086e-05`
  - `True KG`: `+2.0048e-05`
- `F~M`:
  - `CN`: `R^2 = 1.000000`
  - `True KG`: `R^2 = 1.000000`
- `N`-growth:
  - `CN`: all TOWARD, monotone
  - `True KG`: all TOWARD, monotone
- Carrier-`k` response:
  - `CN`: same sign, `CV = 0.0009`
  - `True KG`: same sign, `CV = 0.0840`
- Invariant drift:
  - `CN` expectation drift: `6.33e-15`
  - `True KG` energy drift: `4.48e-05`

### Reading

On the tested cubic operating point, the two lanes agree qualitatively on
gravity sign, `F~M`, and monotone growth. This means the CN lane can mimic
some low-energy gravity rows even though the free theory is different.

## 3. Random-graph operating point

- Gravity sign:
  - `CN`: `+1.7245e-06`
  - `True KG`: `+7.7800e-07`
- `F~M`:
  - `CN`: `R^2 = 1.000000`
  - `True KG`: `R^2 = 0.999999`
- `N`-growth:
  - `CN`: all TOWARD, monotone
  - `True KG`: all TOWARD, not monotone
- Carrier-`k` response:
  - `CN`: same sign, `CV = 0.0031`
  - `True KG`: same sign, `CV = 0.0490`
- Invariant drift:
  - `CN` expectation drift: `2.26e-15`
  - `True KG` energy drift: `1.23e-07`

### Reading

The non-cubic graph preserves the main conclusion:
- the free modal laws still diverge strongly
- some gravity observables still line up qualitatively
- but the dynamic agreement is weaker away from the cubic operating point

## Verdict

The current CN scalar lane is **not** a faithful stand-in for a true local
graph KG theory in the tested regime.

What is true:
- it is a strong low-energy scalar control architecture
- it reproduces several gravity rows cleanly
- it is numerically stable and exactly norm-preserving

What is not true:
- it is not the same free equation as local doubled-state KG
- it should not be described as if its success automatically proves a true
  graph KG theory has passed the same card

## Practical implication

The scalar graph direction is still promising, but the branch should now
separate two claims:

1. `CN scalar graph lane`:
   retained as a clean scalar control/base layer

2. `True local graph KG lane`:
   still an open theory-development lane that must be tested directly

The correct next move is to decide explicitly whether the project wants:
- a scalar control theory that passes many core gravity rows, or
- a true local KG formulation on graphs that richer matter/spin structure
  must build on top of.
